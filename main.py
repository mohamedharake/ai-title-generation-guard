"""CLI entrypoint for multilingual chat title guard."""
from __future__ import annotations

import argparse
from pathlib import Path

from pipeline import TitlePipeline


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate language-consistent chat titles.")
    parser.add_argument("text", nargs="?", help="Conversation text")
    parser.add_argument("--file", help="Read conversation text from a file")
    parser.add_argument("--lang", help="Force a language, e.g. en/ar/fr/zh")
    parser.add_argument("--json", action="store_true", help="Print structured JSON output")
    return parser.parse_args()


def read_input(args: argparse.Namespace) -> str:
    if args.file:
        return Path(args.file).read_text(encoding="utf-8")
    if args.text:
        return args.text
    return input("Enter chat content: ").strip()


if __name__ == "__main__":
    args = parse_args()
    text = read_input(args)
    pipeline = TitlePipeline()
    decision = pipeline.build_title(text, forced_lang=args.lang)

    if args.json:
        print(decision.to_json())
    else:
        print(f"Detected language: {decision.input_language}")
        print(f"Selected title: {decision.selected_title}")
        print(f"Stage used: {decision.selected_stage}")
        print(f"Validation reason: {decision.validation_reason}")
        print("Candidates checked:")
        for idx, candidate in enumerate(decision.candidates_checked, start=1):
            print(f"  {idx}. {candidate}")
