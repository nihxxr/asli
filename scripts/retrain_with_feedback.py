"""Retrain the classifier on the synthetic set plus labelled user feedback.

When someone answers "Was this result right?", the stored (redacted) message
gets a label: the verdict if they said yes, the opposite if they said no.
This script adds those rows to data/train.csv's rows, retrains, and runs the
eval. Keep the new model only if the eval still passes.

Usage: DATABASE_URL=... python scripts/retrain_with_feedback.py
"""

from __future__ import annotations

import csv
import os
import subprocess
import sys
from pathlib import Path

import joblib

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.analysis.model import MODEL_PATH, build_pipeline, prepare  # noqa: E402
from app.db import Store  # noqa: E402


def main() -> int:
    store = Store(os.environ.get("DATABASE_URL", "sqlite:///./asli.db"))
    feedback = store.labelled_examples()
    with (ROOT / "data" / "train.csv").open(encoding="utf-8") as f:
        rows = [(r["text"], int(r["label"])) for r in csv.DictReader(f)]
    print(f"{len(rows)} synthetic rows + {len(feedback)} feedback rows")
    if not feedback:
        print("No feedback yet. Nothing to do.")
        return 0

    data = rows + feedback * 3  # real examples count for more than templates
    pipe = build_pipeline().fit([prepare(t) for t, _ in data], [y for _, y in data])
    backup = MODEL_PATH.with_suffix(".previous.joblib")
    MODEL_PATH.replace(backup)
    joblib.dump(pipe, MODEL_PATH, compress=3)

    result = subprocess.run([sys.executable, str(ROOT / "scripts" / "evaluate.py")])
    if result.returncode != 0:
        backup.replace(MODEL_PATH)
        print("Eval failed with the new model, restored the previous one.")
        return 1
    print("Eval passed. New model saved; the previous one is at", backup)
    return 0


if __name__ == "__main__":
    sys.exit(main())
