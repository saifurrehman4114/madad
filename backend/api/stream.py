"""
WebSocket endpoint for near-real-time streaming translation.

Client sends base64-encoded JPEG frames at the configured fps. Every N frames
(default 16 = 4 seconds at 4 fps) the server runs a translation pass on the
rolling buffer and emits a partial caption. Lightweight enough for a laptop
Ollama demo; the mobile app uses LiteRT directly and doesn't call this.
"""
from __future__ import annotations

import asyncio
import base64
import io
import json

import structlog
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from PIL import Image

from backend.core.config import get_settings
from backend.models.factory import get_model

router = APIRouter()
log = structlog.get_logger(__name__)


@router.websocket("/ws/stream")
async def stream_signs(ws: WebSocket) -> None:
    await ws.accept()
    settings = get_settings()
    model = await get_model(settings)

    buffer: list[Image.Image] = []
    window = settings.target_fps * int(settings.max_video_seconds)
    stride = window // 2  # emit overlapping partials every 2 seconds

    frames_since_last = 0
    try:
        while True:
            msg = await ws.receive_text()
            data = json.loads(msg)
            if data.get("type") == "end":
                break
            if data.get("type") != "frame":
                continue

            img = Image.open(io.BytesIO(base64.b64decode(data["jpeg"])))
            buffer.append(img.convert("RGB"))
            if len(buffer) > window:
                buffer.pop(0)
            frames_since_last += 1

            if frames_since_last >= stride and len(buffer) == window:
                frames_since_last = 0
                asyncio.create_task(_translate_and_send(ws, model, list(buffer)))
    except WebSocketDisconnect:
        log.info("ws.client.disconnect")
    except Exception as exc:  # noqa: BLE001
        log.exception("ws.error", error=str(exc))
        await ws.close(code=1011)


async def _translate_and_send(ws: WebSocket, model, frames: list[Image.Image]) -> None:
    try:
        result = await model.sign_to_text(frames)
        await ws.send_text(
            json.dumps(
                {
                    "type": "partial",
                    "urdu": result.urdu,
                    "english": result.english,
                    "glosses": result.glosses,
                    "confidence": result.confidence,
                    "latency_ms": result.latency_ms,
                }
            )
        )
    except Exception as exc:  # noqa: BLE001
        log.warning("ws.translate.failed", error=str(exc))
