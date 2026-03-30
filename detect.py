"""Language detection utilities for chat title generation."""
from __future__ import annotations

from collections import Counter
from typing import Iterable

from langdetect import DetectorFactory, detect

DetectorFactory.seed = 0

SUPPORTED_LANGS = {"en", "ar", "fr", "zh-cn", "zh-tw", "zh"}


def _normalize_lang(code: str) -> str:
    code = (code or "").lower().strip()
    if code in {"zh-cn", "zh-tw", "zh"}:
        return "zh"
    if code.startswith("en"):
        return "en"
    if code.startswith("ar"):
        return "ar"
    if code.startswith("fr"):
        return "fr"
    return "en"


def detect_language(text: str) -> str:
    """Return dominant language for a single string.

    Falls back to English for empty or ambiguous inputs.
    """
    if not text or not text.strip():
        return "en"
    try:
        return _normalize_lang(detect(text))
    except Exception:
        return "en"


def detect_language_from_messages(messages: Iterable[str]) -> str:
    """Detect dominant language from multiple messages.

    Uses majority vote across non-trivial messages.
    """
    counts: Counter[str] = Counter()
    for message in messages:
        if message and len(message.strip()) >= 4:
            counts[detect_language(message)] += 1
    if not counts:
        return "en"
    return counts.most_common(1)[0][0]
