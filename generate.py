"""Candidate title generation logic.

This project intentionally simulates a multilingual bug in non-strict mode,
so the validation layer has something realistic to catch.
"""
from __future__ import annotations

import random
import re
from typing import List

BUG_SUFFIXES = {
    "en": "点评",  # Chinese word meaning review/commentary
    "fr": "点评",
    "ar": "点评",
}


STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "but", "by", "do", "for",
    "from", "good", "how", "i", "in", "is", "it", "its", "just", "my", "no",
    "of", "ok", "on", "or", "please", "project", "the", "this", "to", "too",
    "very", "what", "why", "with", "you", "your",
}


def _tokenize(text: str) -> List[str]:
    return re.findall(r"[A-Za-z0-9\-']+", text.lower())


KEYWORD_LABELS = [
    ("8-bit computer", "8-bit Computer Project"),
    ("ipv6", "IPv6 Discussion"),
    ("ipv5", "Why No IPv5"),
    ("chat title", "Chat Title Bug"),
    ("title", "Title Generation"),
    ("translation", "Translation Request"),
    ("inductor", "Inductor Initial Condition"),
    ("laplace", "Laplace Transform Question"),
    ("network", "Networking Question"),
    ("eece321", "EECE321 Prep"),
    ("hair", "Hair Treatment Discussion"),
]


def _extract_topic(text: str) -> str:
    lowered = text.lower()
    for needle, label in KEYWORD_LABELS:
        if needle in lowered:
            return label

    tokens = [t for t in _tokenize(text) if t not in STOPWORDS]
    if not tokens:
        return "General Chat"

    phrase = " ".join(tokens[:4])
    return phrase.title()


LANG_SUFFIX = {
    "en": "Review",
    "fr": "Revue",
    "ar": "مراجعة",
    "zh": "点评",
}


class SimulatedTitleGenerator:
    """A tiny offline generator that mimics an LLM pipeline.

    In non-strict mode, it can intentionally produce a mixed-language title to
    reproduce the bug class the user observed.
    """

    def __init__(self, seed: int = 7, bug_probability: float = 0.35) -> None:
        self.random = random.Random(seed)
        self.bug_probability = bug_probability

    def generate(self, text: str, lang: str = "en", strict: bool = False, n: int = 3) -> List[str]:
        topic = _extract_topic(text)
        clean_suffix = LANG_SUFFIX.get(lang, "Review")
        candidates: List[str] = []

        for i in range(n):
            if not strict and i == 0 and lang in BUG_SUFFIXES and self.random.random() < self.bug_probability:
                candidates.append(f"{topic}{BUG_SUFFIXES[lang]}")
                continue

            if lang == "en":
                if topic.endswith("Discussion") or topic.endswith("Question") or topic.endswith("Prep"):
                    candidates.append(topic)
                else:
                    candidates.append(f"{topic} {clean_suffix}")
            elif lang == "fr":
                candidates.append(f"{topic} {clean_suffix}")
            elif lang == "ar":
                candidates.append(f"{clean_suffix} {topic}")
            elif lang == "zh":
                candidates.append(f"{topic}{clean_suffix}")
            else:
                candidates.append(f"{topic} Review")

        # prefer shorter unique candidates first
        seen = set()
        unique = []
        for c in candidates:
            if c not in seen:
                unique.append(c)
                seen.add(c)
        return unique
