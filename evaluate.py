"""Offline evaluation harness.

Runs a small benchmark to measure mixed-language failures before and after the
validation + retry pipeline.
"""
from __future__ import annotations

import csv
from pathlib import Path
from typing import List

from detect import detect_language
from generate import SimulatedTitleGenerator
from pipeline import TitlePipeline
from validate import validate_title

DATASET_PATH = Path(__file__).parent / "data" / "samples.csv"


def load_samples() -> List[dict[str, str]]:
    rows: List[dict[str, str]] = []
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def evaluate() -> dict[str, float | int]:
    samples = load_samples()
    generator = SimulatedTitleGenerator(seed=7, bug_probability=0.55)
    pipeline = TitlePipeline(generator=generator)

    raw_failures = 0
    pipeline_failures = 0

    for sample in samples:
        text = sample["text"]
        lang = sample["lang"] or detect_language(text)

        raw_title = generator.generate(text, lang=lang, strict=False, n=1)[0]
        if not validate_title(raw_title, lang).is_valid:
            raw_failures += 1

        decision = pipeline.build_title(text, forced_lang=lang)
        if not validate_title(decision.selected_title, lang).is_valid:
            pipeline_failures += 1

    total = len(samples)
    return {
        "samples": total,
        "raw_failures": raw_failures,
        "pipeline_failures": pipeline_failures,
        "raw_failure_rate": round(raw_failures / total, 3),
        "pipeline_failure_rate": round(pipeline_failures / total, 3),
    }


if __name__ == "__main__":
    metrics = evaluate()
    print("Evaluation Results")
    for key, value in metrics.items():
        print(f"- {key}: {value}")
