"""Combine rules, link checks and the classifier into one verdict."""

from __future__ import annotations

from dataclasses import dataclass, field

from .. import i18n
from . import model as wording
from .normalize import clean, detect_language
from .signals import Hit, brand_mentions, find_signals
from .urls import find_links

LINK_WEIGHTS = {
    "link_lookalike": 0.8,
    "link_brand_in_subdomain": 0.85,
    "link_apk": 0.85,
    "link_punycode": 0.75,
    "link_ip": 0.7,
    "link_risky_tld": 0.4,
    "link_shortener": 0.35,
    "off_platform_link": 0.35,
}
BRAND_UNOFFICIAL_WEIGHT = 0.5
MODEL_WEIGHT = 0.7          # the classifier can add at most this much as one noisy-OR term
MODEL_FLAG_AT = 0.6         # show the "wording" flag from this probability up
SCAM_AT, SUSPICIOUS_AT = 0.75, 0.4

BRAND_KEYS = {
    "state bank": "sbi", "google pay": "gpay", "bank of baroda": "bob", "india post": "indiapost",
    "indiapost": "indiapost", "blue dart": "bluedart", "bluedart": "bluedart", "income tax": "incometax",
    "incometax": "incometax", "reserve bank": "rbi", "aadhar": "aadhaar",
}


@dataclass
class Result:
    text: str
    language: str
    verdict: str
    score: float
    rule_score: float
    model_probability: float | None
    hits: list = field(default_factory=list)
    links: list = field(default_factory=list)


def noisy_or(weights) -> float:
    p = 1.0
    for w in weights:
        p *= 1.0 - max(0.0, min(w, 1.0))
    return 1.0 - p


def analyse(raw: str) -> Result:
    text = clean(raw)
    hits: list[Hit] = find_signals(text)
    links = find_links(text)

    link_hits: dict[str, Hit] = {}
    for link in links:
        for flag_id, detail in link.flags:
            h = link_hits.setdefault(flag_id, Hit(flag_id, LINK_WEIGHTS[flag_id], [], detail))
            h.spans.append((link.start, link.end))

    brands = brand_mentions(text)
    unofficial = [l for l in links if not l.official and not l.flags]
    if brands and unofficial and not ({"link_lookalike", "link_brand_in_subdomain"} & link_hits.keys()):
        brand = BRAND_KEYS.get(brands[0], brands[0].replace(" ", ""))
        link_hits["brand_unofficial_link"] = Hit(
            "brand_unofficial_link", BRAND_UNOFFICIAL_WEIGHT,
            [(l.start, l.end) for l in unofficial], f"{brand}|{unofficial[0].registered_domain}",
        )
    hits.extend(link_hits.values())

    rule_score = noisy_or(h.weight for h in hits)
    p = wording.scam_probability(text) if text else None

    score = noisy_or([rule_score, MODEL_WEIGHT * (p or 0.0)])
    # Only official links and no rule hits: trust the links a little more than the wording.
    if links and all(l.official for l in links) and not hits:
        score *= 0.6
    if p is not None and p >= MODEL_FLAG_AT:
        hits.append(Hit("model_wording", round(MODEL_WEIGHT * p, 3), [], str(round(p * 100))))

    verdict = "scam" if score >= SCAM_AT else "suspicious" if score >= SUSPICIOUS_AT else "no_signs"
    hits.sort(key=lambda h: h.weight, reverse=True)
    return Result(text, detect_language(text), verdict, round(score, 3), round(rule_score, 3),
                  None if p is None else round(p, 3), hits, links)


def _fmt(template: str, detail: str) -> str:
    brand, _, domain = detail.partition("|")
    if not domain:
        domain = brand
    brand_name = i18n.BRAND_NAMES.get(brand, brand.upper() if len(brand) <= 4 else brand.title())
    return template.format(brand=brand_name, domain=domain, pct=detail)


def explain(res: Result, lang: str | None = None) -> dict:
    """A JSON-ready report in the requested language (defaults to the message's language)."""
    lang = lang if lang in i18n.LANGS else res.language
    label, headline = i18n.VERDICTS[res.verdict][lang]
    flags = []
    for h in res.hits:
        title, detail = i18n.FLAGS[h.id][lang]
        flags.append({
            "id": h.id,
            "weight": h.weight,
            "title": _fmt(title, h.detail),
            "detail": _fmt(detail, h.detail),
            "spans": [list(s) for s in h.spans],
        })
    return {
        "verdict": res.verdict,
        "label": label,
        "headline": headline,
        "score": res.score,
        "rule_score": res.rule_score,
        "model_probability": res.model_probability,
        "language": lang,
        "message_language": res.language,
        "text": res.text,
        "flags": flags,
        "links": [
            {"url": l.url, "host": l.host, "domain": l.registered_domain, "official": l.official,
             "flags": [f for f, _ in l.flags]}
            for l in res.links
        ],
        "actions": i18n.ACTIONS["clean" if res.verdict == "no_signs" else "warn"][lang],
    }


def check(raw: str, lang: str | None = None) -> dict:
    return explain(analyse(raw), lang)
