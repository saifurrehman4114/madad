from __future__ import annotations

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from backend.api.avatar_vocab import DEFAULT_VOCAB
from backend.core.config import Settings, get_settings
from backend.core.schema import (
    HealthReport,
    SignToTextResult,
    TextToSignResult,
    TranslateTextRequest,
)
from backend.core.video import extract_frames
from backend.models.factory import get_model

router = APIRouter(tags=["translate"])


@router.get("/health", response_model=HealthReport)
async def health(settings: Settings = Depends(get_settings)) -> HealthReport:
    try:
        model = await get_model(settings)
        return HealthReport(
            status="ok",
            backend=model.name,
            model=(
                settings.ollama_model
                if model.name == "ollama"
                else settings.hf_model_id
            ),
            adapter=settings.adapter_path,
            device=getattr(model, "device_name", None),
        )
    except Exception as exc:  # noqa: BLE001
        return HealthReport(
            status=f"degraded: {exc}",
            backend="unknown",
            model="unknown",
        )


@router.post("/sign-to-text", response_model=SignToTextResult)
async def sign_to_text(
    clip: UploadFile = File(..., description="Short video clip (.mp4/.webm)"),
    lang_hint: str = "ur",
    settings: Settings = Depends(get_settings),
) -> SignToTextResult:
    if clip.size and clip.size > 25 * 1024 * 1024:
        raise HTTPException(413, "Clip too large; keep it under 25 MB")

    raw = await clip.read()
    try:
        frames = extract_frames(
            raw,
            target_fps=settings.target_fps,
            max_seconds=settings.max_video_seconds,
            short_edge=settings.target_frame_size,
        )
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc

    model = await get_model(settings)
    return await model.sign_to_text(frames, lang_hint=lang_hint)


@router.post("/text-to-sign", response_model=TextToSignResult)
async def text_to_sign(
    payload: TranslateTextRequest,
    settings: Settings = Depends(get_settings),
) -> TextToSignResult:
    if not payload.text.strip():
        raise HTTPException(400, "text is required")
    vocab = payload.vocabulary or DEFAULT_VOCAB
    model = await get_model(settings)
    return await model.text_to_sign(
        payload.text.strip(),
        vocabulary=vocab,
        source_lang=payload.source_lang,
    )


@router.get("/vocabulary")
async def vocabulary() -> JSONResponse:
    return JSONResponse({"count": len(DEFAULT_VOCAB), "signs": DEFAULT_VOCAB})
