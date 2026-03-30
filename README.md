# Multilingual Chat Title Guard

A small but structured software project that reproduces and mitigates a **mixed-language chat title bug**.

Example failure:
- Input chat is in English
- Bad generated title becomes `8-bit Computer Project点评`
- Pipeline catches the wrong script and regenerates a clean English title

## What this project is
This is **not OpenAI's code** and it does **not fix ChatGPT production**.

It is a **replica project** that models the same class of failure:
- language detection mismatch
- multilingual generation bug
- validation and retry guardrails
- logging and evaluation
- API exposure for a more production-like setup

This repo includes:
- a title-generation pipeline
- language detection
- script validation
- strict regeneration
- deterministic fallback
- logging to file
- offline evaluation over a sample dataset
- FastAPI service
- tests

## Project structure
```text
multilingual-chat-title-guard/
├── api.py
├── data/
│   └── samples.csv
├── detect.py
├── evaluate.py
├── generate.py
├── logs/
├── main.py
├── pipeline.py
├── README.md
├── requirements.txt
├── tests/
│   └── test_pipeline.py
└── validate.py
