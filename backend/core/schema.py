from __future__ import annotations

from pydantic import BaseModel, Field


class SignToTextResult(BaseModel):
    glosses: list[str] = Field(default_factory=list)
    urdu: str = ""
    english: str = ""
    confidence: float = 0.0
    notes: str | None = None

    latency_ms: int = 0
    backend: str = "ollama"
    adapter: str | None = None


class SignClause(BaseModel):
    source: str
    glosses: list[str]
    duration_ms: int


class TextToSignResult(BaseModel):
    clauses: list[SignClause] = Field(default_factory=list)
    missing_vocab: list[str] = Field(default_factory=list)
    latency_ms: int = 0
    backend: str = "ollama"


class TranslateTextRequest(BaseModel):
    text: str
    source_lang: str = "ur"  # "ur" | "en"
    vocabulary: list[str] | None = None


class HealthReport(BaseModel):
    status: str
    backend: str
    model: str
    adapter: str | None = None
    device: str | None = None
