"""Score the full checker on the hand-written eval set in data/eval.csv.

Reports three systems side by side so you can see what each part adds:
rules and links only, the classifier only, and the combined checker.
A message counts as flagged when the verdict is "suspicious" or "scam".

Exits with status 1 if the combined checker falls below the thresholds,
so CI fails when a change makes detection worse.

Usage: python scripts/evaluate.py [--json models/eval_report.json]
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.analysis import engine  # noqa: E402

MIN_RECALL = 0.90          # share of scams flagged
MAX_FALSE_POSITIVE = 0.10  # share of normal messages wrongly flagged


def metrics(pairs):
    tp = sum(1 for y, p in pairs if y and p)
    fp = sum(1 for y, p in pairs if not y and p)
    fn = sum(1 for y, p in pairs if y and not p)
    tn = sum(1 for y, p in pairs if not y and not p)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    fpr = fp / (fp + tn) if fp + tn else 0.0
    return {"precision": round(precision, 3), "recall": round(recall, 3), "f1": round(f1, 3),
            "false_positive_rate": round(fpr, 3), "tp": tp, "fp": fp, "fn": fn, "tn": tn}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default=str(ROOT / "models" / "eval_report.json"))
    args = ap.parse_args()

    with (ROOT / "data" / "eval.csv").open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    combined, rules_only, model_only = [], [], []
    by_cat, by_lang = defaultdict(list), defaultdict(list)
    misses = []
    for r in rows:
        y = r["label"] == "1"
        res = engine.analyse(r["text"])
        flagged = res.verdict != "no_signs"
        combined.append((y, flagged))
        rules_only.append((y, res.rule_score >= engine.SUSPICIOUS_AT))
        model_only.append((y, (res.model_probability or 0) >= 0.5))
        by_cat[r["category"]].append((y, flagged))
        by_lang[r["lang"]].append((y, flagged))
        if y != flagged:
            misses.append({"text": r["text"][:110], "label": int(y), "verdict": res.verdict, "score": res.score,
                           "flags": [h.id for h in res.hits]})

    report = {
        "rows": len(rows),
        "combined": metrics(combined),
        "rules_and_links_only": metrics(rules_only),
        "classifier_only": metrics(model_only),
        "by_language": {k: metrics(v) for k, v in sorted(by_lang.items())},
        "by_category": {k: metrics(v) for k, v in sorted(by_cat.items())},
        "mistakes": misses,
    }

    print(f"Eval set: {len(rows)} hand-written messages\n")
    print(f"{'system':<22}{'precision':>10}{'recall':>8}{'F1':>7}{'FP rate':>9}")
    for name in ("rules_and_links_only", "classifier_only", "combined"):
        m = report[name]
        print(f"{name:<22}{m['precision']:>10.3f}{m['recall']:>8.3f}{m['f1']:>7.3f}{m['false_positive_rate']:>9.3f}")
    print("\nBy language (combined):")
    for k, m in report["by_language"].items():
        print(f"  {k:<10} recall {m['recall']:.2f}  FP rate {m['false_positive_rate']:.2f}  (n={m['tp'] + m['fp'] + m['fn'] + m['tn']})")
    if misses:
        print(f"\nMistakes ({len(misses)}):")
        for m in misses:
            kind = "missed scam" if m["label"] else "false alarm"
            print(f"  [{kind}] {m['verdict']} {m['score']:.2f} {m['flags']}  {m['text']}")

    Path(args.json).parent.mkdir(exist_ok=True)
    Path(args.json).write_text(json.dumps(report, indent=2, ensure_ascii=False))

    c = report["combined"]
    ok = c["recall"] >= MIN_RECALL and c["false_positive_rate"] <= MAX_FALSE_POSITIVE
    print(f"\n{'PASS' if ok else 'FAIL'}: recall {c['recall']:.3f} (min {MIN_RECALL}), "
          f"false positive rate {c['false_positive_rate']:.3f} (max {MAX_FALSE_POSITIVE})")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
