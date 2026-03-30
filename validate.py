"""Validation rules for output language and script consistency."""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Tuple

LATIN_RE = re.compile(r"[A-Za-z]")
ARABIC_RE = re.compile(r"[\u0600-\u06FF]")
CJK_RE = re.compile(r"[\u3400-\u4DBF\u4E00-\u9FFF]")


@dataclass(frozen=True)
class ValidationResult:
    is_valid: bool
    reason: str


def contains_latin(text: str) -> bool:
    return LATIN_RE.search(text) is not None


def contains_arabic(text: str) -> bool:
    return ARABIC_RE.search(text) is not None


def contains_cjk(text: str) -> bool:
    return CJK_RE.search(text) is not None


def detect_scripts(text: str) -> Tuple[bool, bool, bool]:
    return contains_latin(text), contains_arabic(text), contains_cjk(text)


def validate_title(title: str, expected_lang: str) -> ValidationResult:
    if not title or not title.strip():
        return ValidationResult(False, "empty_title")

    has_latin, has_arabic, has_cjk = detect_scripts(title)

    if expected_lang == "en":
        if has_cjk:
            return ValidationResult(False, "english_title_contains_cjk")
        if has_arabic:
            return ValidationResult(False, "english_title_contains_arabic")
        if not has_latin:
            return ValidationResult(False, "english_title_missing_latin")

    elif expected_lang == "ar":
        if has_cjk:
            return ValidationResult(False, "arabic_title_contains_cjk")
        if has_latin and has_arabic:
            return ValidationResult(False, "arabic_title_mixed_with_latin")
        if not has_arabic:
            return ValidationResult(False, "arabic_title_missing_arabic")

    elif expected_lang == "fr":
        if has_cjk:
            return ValidationResult(False, "french_title_contains_cjk")
        if has_arabic:
            return ValidationResult(False, "french_title_contains_arabic")
        if not has_latin:
            return ValidationResult(False, "french_title_missing_latin")

    elif expected_lang == "zh":
        if has_arabic:
            return ValidationResult(False, "chinese_title_contains_arabic")
        if not has_cjk:
            return ValidationResult(False, "chinese_title_missing_cjk")

    return ValidationResult(True, "ok")
