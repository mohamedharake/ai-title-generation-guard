"""Main title-generation pipeline with logging, validation, retry, and fallback."""
from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, List

from detect import detect_language, detect_language_from_messages
from generate import SimulatedTitleGenerator
from validate import ValidationResult, validate_title

LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "pipeline.log"

logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


@dataclass
class TitleDecision:
    input_language: str
    selected_title: str
    selected_stage: str
    validation_reason: str
    candidates_checked: List[str]

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False, indent=2)


class TitlePipeline:
    def __init__(self, generator: SimulatedTitleGenerator | None = None) -> None:
        self.generator = generator or SimulatedTitleGenerator()

    def _fallback_title(self, lang: str) -> str:
        defaults = {
            "en": "General Chat",
            "fr": "Discussion Générale",
            "ar": "محادثة عامة",
            "zh": "通用聊天",
        }
        return defaults.get(lang, "General Chat")

    def build_title(self, messages: Iterable[str] | str, forced_lang: str | None = None) -> TitleDecision:
        if isinstance(messages, str):
            message_list = [messages]
            joined_text = messages
        else:
            message_list = list(messages)
            joined_text = "\n".join(message_list)

        lang = forced_lang or detect_language_from_messages(message_list) or detect_language(joined_text)
        checked: List[str] = []

        # Stage 1: non-strict generation, may contain simulated bug
        for candidate in self.generator.generate(joined_text, lang=lang, strict=False, n=3):
            checked.append(candidate)
            result: ValidationResult = validate_title(candidate, lang)
            logging.info("stage=initial lang=%s candidate=%r valid=%s reason=%s", lang, candidate, result.is_valid, result.reason)
            if result.is_valid:
                return TitleDecision(lang, candidate, "initial", result.reason, checked)

        # Stage 2: strict regeneration
        for candidate in self.generator.generate(joined_text, lang=lang, strict=True, n=3):
            checked.append(candidate)
            result = validate_title(candidate, lang)
            logging.info("stage=strict lang=%s candidate=%r valid=%s reason=%s", lang, candidate, result.is_valid, result.reason)
            if result.is_valid:
                return TitleDecision(lang, candidate, "strict_regeneration", result.reason, checked)

        # Stage 3: deterministic fallback
        fallback = self._fallback_title(lang)
        result = validate_title(fallback, lang)
        checked.append(fallback)
        logging.info("stage=fallback lang=%s candidate=%r valid=%s reason=%s", lang, fallback, result.is_valid, result.reason)
        return TitleDecision(lang, fallback, "fallback", result.reason, checked)
