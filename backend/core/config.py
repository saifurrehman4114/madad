from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ROOT / ".env",
        env_prefix="MADAD_",
        extra="ignore",
    )

    backend: str = Field(default="ollama", description="ollama | transformers")
    ollama_host: str = Field(default="http://127.0.0.1:11434")
    ollama_model: str = Field(default="gemma4:e4b")
    hf_model_id: str = Field(default="google/gemma-4-e4b-it")

    adapter_path: str | None = Field(
        default=None,
        description="Path to Unsloth LoRA adapter; None = base weights only",
    )

    max_video_seconds: float = 4.0
    target_fps: int = 4
    target_frame_size: int = 384

    default_source_lang: str = "psl"
    default_target_lang: str = "ur"

    log_level: str = "INFO"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
