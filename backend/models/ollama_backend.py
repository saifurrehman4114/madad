"""
Ollama backend for Gemma 4. Default for local laptop demo.

Requires `ollama pull gemma4:e4b`. Ollama 0.4+ accepts a list of image bytes
in the `images` field on each message and returns structured output when
`format` is a JSON schema.
"""
from __future__ import annotations

import base64
import json
import time

import httpx
import structlog
from PIL import Image

from backend.core.prompts import (
    SIGN_TO_TEXT_SYSTEM,
    TEXT_TO_SIGN_SYSTEM,
    sign_to_text_user,
    text_to_sign_user,
)
from backend.core.schema import SignToTextResult, TextToSignResult
from backend.core.video import frames_to_bytes
from backend.models.base import SignModel

log = structlog.get_logger(__name__)


SIGN_TO_TEXT_SCHEMA = {
    "type": "object",
    "properties": {
        "glosses": {"type": "array", "items": {"type": "string"}},
        "urdu": {"type": "string"},
        "english": {"type": "string"},
        "confidence": {"type": "number"},
        "notes": {"type": ["string", "null"]},
    },
    "required": ["glosses", "urdu", "english", "confidence"],
}


TEXT_TO_SIGN_SCHEMA = {
    "type": "object",
    "properties": {
        "clauses": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "source": {"type": "string"},
                    "glosses": {"type": "array", "items": {"type": "string"}},
                    "duration_ms": {"type": "integer"},
                },
                "required": ["source", "glosses", "duration_ms"],
            },
        },
        "missing_vocab": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["clauses", "missing_vocab"],
}


class OllamaBackend(SignModel):
    name = "ollama"

    def __init__(self, host: str, model: str, adapter: str | None = None) -> None:
        self.host = host.rstrip("/")
        self.model = model
        self.adapter = adapter
        self._client = httpx.AsyncClient(base_url=self.host, timeout=60.0)

    async def sign_to_text(
        self, frames: list[Image.Image], lang_hint: str = "ur"
    ) -> SignToTextResult:
        images_b64 = [
            base64.b64encode(b).decode("ascii") for b in frames_to_bytes(frames)
        ]

        payload = {
            "model": self.model,
            "stream": False,
            "format": SIGN_TO_TEXT_SCHEMA,
            "options": {"temperature": 0.1, "num_predict": 256},
            "messages": [
                {"role": "system", "content": SIGN_TO_TEXT_SYSTEM},
                {
                    "role": "user",
                    "content": sign_to_text_user(lang_hint),
                    "images": images_b64,
                },
            ],
        }

        t0 = time.perf_counter()
        r = await self._client.post("/api/chat", json=payload)
        r.raise_for_status()
        elapsed = int((time.perf_counter() - t0) * 1000)

        content = r.json()["message"]["content"]
        data = json.loads(content)
        return SignToTextResult(
            **data,
            latency_ms=elapsed,
            backend=self.name,
            adapter=self.adapter,
        )

    async def text_to_sign(
        self, text: str, vocabulary: list[str], source_lang: str = "ur"
    ) -> TextToSignResult:
        payload = {
            "model": self.model,
            "stream": False,
            "format": TEXT_TO_SIGN_SCHEMA,
            "options": {"temperature": 0.2, "num_predict": 512},
            "messages": [
                {"role": "system", "content": TEXT_TO_SIGN_SYSTEM},
                {
                    "role": "user",
                    "content": text_to_sign_user(text, vocabulary, source_lang),
                },
            ],
        }

        t0 = time.perf_counter()
        r = await self._client.post("/api/chat", json=payload)
        r.raise_for_status()
        elapsed = int((time.perf_counter() - t0) * 1000)

        data = json.loads(r.json()["message"]["content"])
        return TextToSignResult(
            **data,
            latency_ms=elapsed,
            backend=self.name,
        )

    async def ping(self) -> bool:
        try:
            r = await self._client.get("/api/tags")
            return r.status_code == 200
        except Exception as exc:
            log.warning("ollama.ping.failed", error=str(exc))
            return False

    async def aclose(self) -> None:
        await self._client.aclose()
