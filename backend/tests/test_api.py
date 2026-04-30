"""
Smoke tests — no GPU / no model required. Exercises routing, schema, and
JSON parsing with a stub backend.
"""
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from PIL import Image

from backend.core.schema import SignToTextResult, TextToSignResult
from backend.main import app
from backend.models.base import SignModel


class StubBackend(SignModel):
    name = "stub"

    async def sign_to_text(self, frames, lang_hint="ur"):
        return SignToTextResult(
            glosses=["THANK-YOU", "DOCTOR"],
            urdu="شکریہ ڈاکٹر صاحب",
            english="thank you doctor",
            confidence=0.93,
            latency_ms=420,
            backend=self.name,
        )

    async def text_to_sign(self, text, vocabulary, source_lang="ur"):
        return TextToSignResult(
            clauses=[
                {
                    "source": text,
                    "glosses": ["Q:", "WHAT", "YOUR", "NAME"],
                    "duration_ms": 2400,
                }
            ],
            missing_vocab=[],
            latency_ms=180,
            backend=self.name,
        )


@pytest.fixture(autouse=True)
def patch_model():
    async def fake(*_args, **_kwargs):
        return StubBackend()

    with patch("backend.api.translate.get_model", side_effect=fake), \
         patch("backend.api.stream.get_model", side_effect=fake):
        yield


@pytest.fixture
def client():
    return TestClient(app)


def test_health(client):
    r = client.get("/api/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["backend"] == "stub"


def test_vocabulary(client):
    r = client.get("/api/vocabulary")
    body = r.json()
    assert body["count"] > 100
    assert "THANK-YOU" in body["signs"]


def test_text_to_sign(client):
    r = client.post(
        "/api/text-to-sign",
        json={"text": "aap ka naam kya hai?", "source_lang": "ur"},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["clauses"][0]["glosses"][0] == "Q:"


def test_text_to_sign_empty_rejected(client):
    r = client.post("/api/text-to-sign", json={"text": "   "})
    assert r.status_code == 400


def test_sign_to_text_with_stub_video(client, tmp_path: Path):
    # Build a tiny in-memory mp4 with OpenCV
    import cv2
    import numpy as np

    path = tmp_path / "clip.mp4"
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(path), fourcc, 12, (320, 240))
    for i in range(24):
        frame = np.full((240, 320, 3), i * 8 % 255, dtype=np.uint8)
        writer.write(frame)
    writer.release()

    with path.open("rb") as fh:
        r = client.post(
            "/api/sign-to-text",
            files={"clip": ("clip.mp4", fh, "video/mp4")},
        )
    assert r.status_code == 200
    body = r.json()
    assert body["urdu"].startswith("شکریہ")
    assert body["confidence"] > 0.9
