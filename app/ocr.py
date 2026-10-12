"""Read text from a screenshot with Tesseract.

The Docker image installs the English, Hindi and Kannada language packs.
Images are processed in memory and never written to disk.
"""

from __future__ import annotations

import io
from functools import lru_cache

WANTED = ("eng", "hin", "kan")


class OCRUnavailable(RuntimeError):
    pass


@lru_cache(maxsize=1)
def _languages() -> str:
    try:
        import pytesseract

        have = set(pytesseract.get_languages(config=""))
    except Exception as exc:  # binary missing or not runnable
        raise OCRUnavailable("Tesseract is not installed") from exc
    langs = [l for l in WANTED if l in have]
    if not langs:
        raise OCRUnavailable("No Tesseract language packs found")
    return "+".join(langs)


def available() -> bool:
    try:
        _languages()
        return True
    except OCRUnavailable:
        return False


def image_to_text(data: bytes) -> str:
    import pytesseract
    from PIL import Image, ImageOps

    img = Image.open(io.BytesIO(data))
    img = ImageOps.exif_transpose(img).convert("L")
    if img.width < 1000:  # small screenshots read better upscaled
        scale = 1000 / img.width
        img = img.resize((int(img.width * scale), int(img.height * scale)))
    text = pytesseract.image_to_string(img, lang=_languages())
    return " ".join(line.strip() for line in text.splitlines() if line.strip())
