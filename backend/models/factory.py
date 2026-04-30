from __future__ import annotations

import structlog

from backend.core.config import Settings
from backend.models.base import SignModel

log = structlog.get_logger(__name__)

_model: SignModel | None = None


async def get_model(settings: Settings) -> SignModel:
    global _model
    if _model is not None:
        return _model

    if settings.backend == "ollama":
        from backend.models.ollama_backend import OllamaBackend

        backend = OllamaBackend(
            host=settings.ollama_host,
            model=settings.ollama_model,
            adapter=settings.adapter_path,
        )
        if not await backend.ping():
            log.warning("ollama.unreachable.falling_back", host=settings.ollama_host)
            _model = _load_transformers(settings)
        else:
            _model = backend
    else:
        _model = _load_transformers(settings)

    return _model


def _load_transformers(settings: Settings) -> SignModel:
    from backend.models.transformers_backend import TransformersBackend

    return TransformersBackend(
        model_id=settings.hf_model_id,
        adapter_path=settings.adapter_path,
    )


async def shutdown_model() -> None:
    global _model
    if _model is None:
        return
    close = getattr(_model, "aclose", None)
    if close is not None:
        await close()
    _model = None
