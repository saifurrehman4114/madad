from __future__ import annotations

from abc import ABC, abstractmethod

from PIL import Image

from backend.core.schema import SignToTextResult, TextToSignResult


class SignModel(ABC):
    """Backend-agnostic interface. Both Ollama and HF transformers implement this."""

    name: str = "base"

    @abstractmethod
    async def sign_to_text(
        self, frames: list[Image.Image], lang_hint: str = "ur"
    ) -> SignToTextResult: ...

    @abstractmethod
    async def text_to_sign(
        self, text: str, vocabulary: list[str], source_lang: str = "ur"
    ) -> TextToSignResult: ...
