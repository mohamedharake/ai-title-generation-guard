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

## Why this is stronger than a tiny script
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

That makes it much more defensible on GitHub and on a CV than just "I noticed a bug."

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
```

## From zero: exact steps

### 1) Create a folder
On your computer, make a folder called:
```bash
multilingual-chat-title-guard
```

### 2) Open it in VS Code
- Open VS Code
- File -> Open Folder
- Choose `multilingual-chat-title-guard`

### 3) Create a Python virtual environment
Open the terminal inside VS Code and run:

**Windows**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Mac/Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4) Install dependencies
```bash
pip install -r requirements.txt
```

### 5) Run the CLI
```bash
python main.py "don't yap too much is an 8-bit computer a good project or no. 1-10 fast" --lang en --json
```

You should get structured output showing:
- detected language
- selected title
- stage used
- checked candidates

### 6) Run the benchmark
```bash
python evaluate.py
```

This shows the raw failure rate of the buggy generator versus the improved pipeline.

### 7) Run tests
```bash
pytest -q
```

### 8) Run the API locally
```bash
uvicorn api:app --reload
```

Then open:
- `http://127.0.0.1:8000/docs`

Use the `/generate-title` endpoint with JSON like:
```json
{
  "text": "don't yap too much is an 8-bit computer a good project or no. 1-10 fast",
  "forced_lang": "en"
}
```

### 9) Push to GitHub
Create an empty GitHub repo named:
```text
multilingual-chat-title-guard
```

Then run:
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/multilingual-chat-title-guard.git
git push -u origin main
```

## What to say on your CV
Use something like:

- Built a multilingual AI title-generation pipeline with language detection, script-based validation, retry logic, and deterministic fallback handling.
- Reproduced and mitigated mixed-language output failures in an LLM-style title-generation workflow.
- Exposed the pipeline as a FastAPI service and added offline evaluation to compare raw versus guarded generation failure rates.

## What to say honestly in interviews
Say this exactly:
- "I saw a real mixed-language title bug in a product UI."
- "I did not have the company's internal code."
- "So I built my own replica pipeline that reproduces the same bug class and then added validation, retry, fallback, testing, and an API around it."

That is credible.

## Good upgrades if you want version 2
- replace the simulated generator with a real model/API
- add SQLite logging for decisions
- add Prometheus metrics
- add Docker support
- deploy on Render or Railway
- add a tiny frontend
