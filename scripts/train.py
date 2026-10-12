"""Train the wording classifier on data/train.csv and save models/classifier.joblib.

Usage: python scripts/train.py
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import joblib
from sklearn.model_selection import StratifiedKFold, cross_val_score

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.analysis.model import MODEL_PATH, build_pipeline, prepare  # noqa: E402


def main() -> None:
    with (ROOT / "data" / "train.csv").open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    X = [prepare(r["text"]) for r in rows]
    y = [int(r["label"]) for r in rows]

    pipe = build_pipeline()
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    f1 = cross_val_score(pipe, X, y, cv=cv, scoring="f1")
    print(f"{len(rows)} rows. 5-fold F1 on the synthetic set: {f1.mean():.3f} (this is optimistic; see scripts/evaluate.py)")

    pipe.fit(X, y)
    MODEL_PATH.parent.mkdir(exist_ok=True)
    joblib.dump(pipe, MODEL_PATH, compress=3)
    (MODEL_PATH.parent / "train_meta.json").write_text(json.dumps({"rows": len(rows), "cv_f1": round(float(f1.mean()), 4)}, indent=2))
    print(f"Saved {MODEL_PATH} ({MODEL_PATH.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
