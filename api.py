"""FastAPI service exposing the title pipeline."""
from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel, Field

from pipeline import TitlePipeline

app = FastAPI(title="Multilingual Chat Title Guard", version="1.0.0")
pipeline = TitlePipeline()


class TitleRequest(BaseModel):
    text: str = Field(..., description="Chat text or combined conversation text")
    forced_lang: str | None = Field(default=None, description="Optional language override")


class TitleResponse(BaseModel):
    input_language: str
    selected_title: str
    selected_stage: str
    validation_reason: str
    candidates_checked: list[str]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/generate-title", response_model=TitleResponse)
def generate_title(payload: TitleRequest) -> dict:
    decision = pipeline.build_title(payload.text, forced_lang=payload.forced_lang)
    return {
        "input_language": decision.input_language,
        "selected_title": decision.selected_title,
        "selected_stage": decision.selected_stage,
        "validation_reason": decision.validation_reason,
        "candidates_checked": decision.candidates_checked,
    }
