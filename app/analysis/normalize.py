"""Text clean-up and script detection.

Scam messages often hide words with zero-width characters or mix scripts,
so the checker strips invisible characters before anything else. All later
offsets (for highlighting) refer to the cleaned text this returns.
"""

from __future__ import annotations

import re
import unicodedata

INVISIBLE = re.compile("[​‌‍⁠﻿­]")
SPACES = re.compile(r"[ \t ]+")

DEVANAGARI = re.compile(r"[ऀ-ॿ]")
KANNADA = re.compile(r"[ಀ-೿]")
LATIN = re.compile(r"[A-Za-z]")


def clean(text: str) -> str:
    text = unicodedata.normalize("NFC", text or "")
    text = INVISIBLE.sub("", text)
    text = SPACES.sub(" ", text)
    return text.strip()


def detect_language(text: str) -> str:
    """Return 'kn', 'hi' or 'en' from the dominant script.

    Romanised Hindi (Hinglish) counts as 'en' for replies, because people who
    type Hinglish usually read Latin script more easily than Devanagari.
    """
    kn = len(KANNADA.findall(text))
    hi = len(DEVANAGARI.findall(text))
    la = len(LATIN.findall(text))
    total = kn + hi + la
    if not total:
        return "en"
    if kn / total >= 0.3:
        return "kn"
    if hi / total >= 0.3:
        return "hi"
    return "en"
