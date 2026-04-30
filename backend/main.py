from __future__ import annotations

from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api import stream, translate
from backend.core.config import get_settings
from backend.models.factory import get_model, shutdown_model

log = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    log.info("startup", backend=settings.backend, model=settings.ollama_model)
    await get_model(settings)  # warm the model
    yield
    await shutdown_model()


app = FastAPI(
    title="Madad — Offline PSL Interpreter",
    description="Gemma 4 powered Pakistan Sign Language interpreter for the "
                "Gemma 4 Good Hackathon.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(translate.router, prefix="/api")
app.include_router(stream.router, prefix="/api")


@app.get("/")
async def root() -> dict:
    return {
        "name": "Madad",
        "tagline": "Offline Pakistan Sign Language interpreter on Gemma 4",
        "docs": "/docs",
    }
