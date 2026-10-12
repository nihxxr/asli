"""Link analysis: find the domain a link really goes to and check it.

The most common trick is a link that mentions a bank or brand but points
somewhere else, like sbi-kyc-update.in or onlinesbi.verify-now.xyz.
"""

from __future__ import annotations

import ipaddress
import re
from dataclasses import dataclass, field

import tldextract

_extract = tldextract.TLDExtract(suffix_list_urls=())  # bundled list, no network

URL_RE = re.compile(
    r"(?i)\b((?:https?://|www\.)[^\s<>\"'()]+|"
    r"(?:[a-z0-9-]+\.)+(?:com|in|net|org|xyz|top|live|site|online|info|club|link|app|io|co|me|ly|gl|cc|tk|icu|shop|vip|buzz|sbi)\b(?:/[^\s<>\"'()]*)?)"
)

# Official domains for brands scammers impersonate in India.
OFFICIAL = {
    "sbi": ["sbi.co.in", "onlinesbi.sbi", "sbi.bank.in"],
    "hdfc": ["hdfcbank.com", "hdfc.bank.in"],
    "icici": ["icicibank.com", "icici.bank.in"],
    "axis": ["axisbank.com", "axis.bank.in"],
    "kotak": ["kotak.com", "kotak.bank.in"],
    "pnb": ["pnbindia.in", "pnb.bank.in"],
    "canara": ["canarabank.com", "canarabank.bank.in"],
    "paytm": ["paytm.com"],
    "phonepe": ["phonepe.com"],
    "gpay": ["pay.google.com", "google.com"],
    "amazon": ["amazon.in", "amazon.com"],
    "flipkart": ["flipkart.com"],
    "indiapost": ["indiapost.gov.in"],
    "irctc": ["irctc.co.in"],
    "bluedart": ["bluedart.com"],
    "delhivery": ["delhivery.com"],
    "fedex": ["fedex.com"],
    "dhl": ["dhl.com", "dhl.co.in"],
    "aadhaar": ["uidai.gov.in"],
    "uidai": ["uidai.gov.in"],
    "incometax": ["incometax.gov.in"],
    "epfo": ["epfindia.gov.in"],
    "npci": ["npci.org.in"],
    "rbi": ["rbi.org.in"],
    "trai": ["trai.gov.in"],
    "whatsapp": ["whatsapp.com"],
}
OFFICIAL_DOMAINS = {d for ds in OFFICIAL.values() for d in ds}
GOVT_SUFFIXES = ("gov.in", "nic.in")

SHORTENERS = {
    "bit.ly", "tinyurl.com", "t.co", "goo.gl", "is.gd", "cutt.ly", "rb.gy", "shorturl.at",
    "tiny.cc", "ow.ly", "rebrand.ly", "s.id", "shorturl.asia", "v.gd", "bitly.ws",
}
RISKY_TLDS = {
    "xyz", "top", "live", "site", "online", "info", "club", "link", "icu", "tk", "ml", "ga",
    "cf", "gq", "shop", "vip", "buzz", "cc", "work", "rest", "cyou", "sbs", "lol",
}
CHAT_HOSTS = {"t.me", "telegram.me", "wa.me", "chat.whatsapp.com"}


@dataclass
class LinkReport:
    url: str
    start: int
    end: int
    host: str = ""
    registered_domain: str = ""
    official: bool = False
    flags: list = field(default_factory=list)  # list of (flag_id, detail)


def _levenshtein(a: str, b: str) -> int:
    if a == b:
        return 0
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def _host_of(url: str) -> str:
    u = re.sub(r"(?i)^https?://", "", url)
    host = re.split(r"[/?#:]", u, maxsplit=1)[0].lower().rstrip(".")
    return host[4:] if host.startswith("www.") else host


def is_official(registered: str, host: str) -> bool:
    if registered in OFFICIAL_DOMAINS or host in OFFICIAL_DOMAINS:
        return True
    return any(host == s or host.endswith("." + s) for s in GOVT_SUFFIXES)


def analyse_url(url: str, start: int, end: int) -> LinkReport:
    rep = LinkReport(url=url, start=start, end=end)
    host = _host_of(url)
    rep.host = host
    ex = _extract(host)
    registered = ".".join(p for p in (ex.domain, ex.suffix) if p)
    rep.registered_domain = registered or host

    try:
        ipaddress.ip_address(host)
        rep.flags.append(("link_ip", host))
        return rep
    except ValueError:
        pass

    rep.official = is_official(registered, host)
    if rep.official:
        return rep

    if host.startswith("xn--") or ".xn--" in host:
        rep.flags.append(("link_punycode", host))
    if registered in SHORTENERS or host in SHORTENERS:
        rep.flags.append(("link_shortener", registered))
    if host in CHAT_HOSTS or registered in CHAT_HOSTS:
        rep.flags.append(("off_platform_link", host))
    if ex.suffix.split(".")[-1] in RISKY_TLDS:
        rep.flags.append(("link_risky_tld", "." + ex.suffix))
    if re.search(r"(?i)\.apk(\b|$)", url):
        rep.flags.append(("link_apk", url))

    label = ex.domain.lower()
    sub = ex.subdomain.lower()
    for brand, domains in OFFICIAL.items():
        brand_labels = {d.split(".")[0] for d in domains} | {brand}
        if any(_starts_token(sub, b) for b in brand_labels):
            rep.flags.append(("link_brand_in_subdomain", f"{brand}|{registered}"))
            break
        if any(_starts_token(label, b) for b in brand_labels) or any(
            len(b) >= 5 and 0 < _levenshtein(label, b) <= 2 for b in brand_labels
        ):
            rep.flags.append(("link_lookalike", f"{brand}|{registered}"))
            break
    return rep


def _starts_token(text: str, brand: str) -> bool:
    """True if brand starts a token in text: 'sbi-kyc', 'kyc-sbi', 'hdfcbank1' but not 'taxis'."""
    if len(brand) < 3 or not text:
        return False
    return re.search(rf"(^|[-_.\d]){re.escape(brand)}", text) is not None


def find_links(text: str) -> list[LinkReport]:
    out = []
    for m in URL_RE.finditer(text):
        url = m.group(1).rstrip(".,;:!?")
        out.append(analyse_url(url, m.start(1), m.start(1) + len(url)))
    return out
