"""The wording classifier: character n-gram TF-IDF with logistic regression.

Character n-grams cope with Hinglish spellings ("bhejo", "bhej do"),
Devanagari and Kannada without a tokenizer per language. Links get replaced
by a placeholder so the model learns wording and urls.py judges links.
"""

from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path

from .urls import URL_RE

MODEL_PATH = Path(__file__).resolve().parents[2] / "models" / "classifier.joblib"
DIGITS = re.compile(r"\d")


def prepare(text: str) -> str:
    text = URL_RE.sub(" LINK ", text)
    text = DIGITS.sub("0", text)
    return text.lower()


def build_pipeline():
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import Pipeline

    return Pipeline([
        ("tfidf", TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 5), min_df=2, sublinear_tf=True, max_features=60000)),
        ("clf", LogisticRegression(max_iter=2000, C=4.0, class_weight="balanced")),
    ])


@lru_cache(maxsize=1)
def load(path: str = str(MODEL_PATH)):
    p = Path(path)
    if not p.exists():
        return None
    import joblib

    return joblib.load(p)


def scam_probability(text: str) -> float | None:
    model = load()
    if model is None:
        return None
    return float(model.predict_proba([prepare(text)])[0][1])
