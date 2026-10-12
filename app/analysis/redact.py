"""Remove personal data before a message is stored.

Stored checks feed retraining, so they keep the shape of the scam (wording,
links) and drop what identifies a person: phone numbers, account and card
numbers, OTPs, emails, UPI IDs and URL query strings.
"""

from __future__ import annotations

import re

URL = re.compile(r"(?i)\b((?:https?://|www\.)[^\s<>\"']+)")
EMAIL = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")
UPI = re.compile(r"\b[\w.\-]{2,}@[a-zA-Z]{2,}\b")
PHONE = re.compile(r"(?<!\d)(?:\+?91[\s-]?)?[6-9]\d{4}[\s-]?\d{5}(?!\d)")
LONG_NUMBER = re.compile(r"(?<!\d)\d(?:[\s-]?\d){8,18}(?!\d)")
SHORT_CODE = re.compile(r"(?<![\d₹.,])\b\d{4,8}\b(?![\d,.]*\s*(?:rs|inr|₹|/-))", re.IGNORECASE)


def _strip_query(match: re.Match) -> str:
    url = match.group(1)
    return re.split(r"[?#]", url, maxsplit=1)[0]


def redact(text: str) -> str:
    out = URL.sub(_strip_query, text)
    out = EMAIL.sub("[EMAIL]", out)
    out = UPI.sub("[UPI]", out)
    out = PHONE.sub("[PHONE]", out)
    out = LONG_NUMBER.sub("[NUMBER]", out)
    out = SHORT_CODE.sub("[CODE]", out)
    return out
