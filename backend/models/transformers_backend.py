"""
HuggingFace transformers backend for Gemma 4. Used when we want the LoRA adapter
trained with Unsloth loaded directly, or when Ollama is unavailable.

This backend is heavier (requires PyTorch + GPU for reasonable speed) but gives
us full control over sampling and adapter loading.
"""
from __future__ import annotations

import json
import time

import structlog
from PIL import Image

from backend.core.prompts import (
    SIGN_TO_TEXT_SYSTEM,
    TEXT_TO_SIGN_SYSTEM,
    sign_to_text_user,
    text_to_sign_user,
)
from backend.core.schema import SignToTextResult, TextToSignResult
from backend.models.base import SignModel

log = structlog.get_logger(__name__)


class TransformersBackend(SignModel):
    name = "transformers"

    def __init__(
        self,
        model_id: str = "google/gemma-4-e4b-it",
        adapter_path: str | None = None,
        device: str = "auto",
    ) -> None:
        import torch
        from transformers import AutoProcessor, AutoModelForImageTextToText

        self.adapter = adapter_path
        self.device_name = (
            "cuda"
            if device == "auto" and torch.cuda.is_available()
            else ("mps" if device == "auto" and torch.backends.mps.is_available() else "cpu")
        )
        dtype = torch.bfloat16 if self.device_name != "cpu" else torch.float32

        log.info("loading.model", model=model_id, device=self.device_name, dtype=str(dtype))
        self.processor = AutoProcessor.from_pretrained(model_id)
        self.model = AutoModelForImageTextToText.from_pretrained(
            model_id, torch_dtype=dtype, device_map=self.device_name
        )

        if adapter_path:
            from peft import PeftModel
            log.info("loading.adapter", path=adapter_path)
            self.model = PeftModel.from_pretrained(self.model, adapter_path)

        self.model.eval()

    async def sign_to_text(
        self, frames: list[Image.Image], lang_hint: str = "ur"
    ) -> SignToTextResult:
        messages = [
            {"role": "system", "content": [{"type": "text", "text": SIGN_TO_TEXT_SYSTEM}]},
            {
                "role": "user",
                "content": [
                    *[{"type": "image", "image": f} for f in frames],
                    {"type": "text", "text": sign_to_text_user(lang_hint)},
                ],
            },
        ]
        raw = await self._generate(messages, max_new_tokens=256)
        data = _safe_json(raw, default={"glosses": [], "urdu": "", "english": "", "confidence": 0.0})
        return SignToTextResult(**data, backend=self.name, adapter=self.adapter)

    async def text_to_sign(
        self, text: str, vocabulary: list[str], source_lang: str = "ur"
    ) -> TextToSignResult:
        messages = [
            {"role": "system", "content": [{"type": "text", "text": TEXT_TO_SIGN_SYSTEM}]},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": text_to_sign_user(text, vocabulary, source_lang)},
                ],
            },
        ]
        raw = await self._generate(messages, max_new_tokens=512)
        data = _safe_json(raw, default={"clauses": [], "missing_vocab": []})
        return TextToSignResult(**data, backend=self.name)

    async def _generate(self, messages: list, max_new_tokens: int) -> str:
        import torch

        t0 = time.perf_counter()
        inputs = self.processor.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt",
        ).to(self.device_name)

        with torch.inference_mode():
            gen = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=False,
                temperature=0.1,
            )
        out = self.processor.decode(
            gen[0][inputs["input_ids"].shape[-1]:], skip_special_tokens=True
        )
        log.debug("generate.done", ms=int((time.perf_counter() - t0) * 1000))
        return out


def _safe_json(text: str, default: dict) -> dict:
    """Gemma usually emits clean JSON. Be defensive against a stray prefix."""
    text = text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        text = text.split("\n", 1)[1] if "\n" in text else text
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1:
            try:
                return json.loads(text[start : end + 1])
            except json.JSONDecodeError:
                pass
        log.warning("json.parse.failed", raw=text[:200])
        return default
