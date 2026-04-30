"""
Convert a fine-tuned Gemma 4 E4B model (base + LoRA adapter) into a LiteRT
(.tflite) asset ready for on-device inference on Android.

Usage
-----
    python mobile/litert_android/convert.py \
        --adapter training/madad-lora \
        --base google/gemma-4-e4b-it \
        --out mobile/litert_android/app/src/main/assets/madad.tflite
"""
from __future__ import annotations

import argparse
from pathlib import Path


def convert(base_id: str, adapter_path: Path | None, out: Path) -> None:
    """
    We lean on the Google AI Edge conversion path released alongside Gemma 4.

    Steps:
      1. load base Gemma 4 E4B in fp16
      2. merge LoRA adapter (if provided)
      3. re-export as a Torch ExportedProgram with example multimodal inputs
      4. run ai_edge_torch.convert() with int4 weight-only quantisation
         + mixed precision activations + NNAPI-friendly op selection
      5. write .tflite to ``out``
    """
    import torch
    from transformers import AutoProcessor, AutoModelForImageTextToText

    processor = AutoProcessor.from_pretrained(base_id)
    model = AutoModelForImageTextToText.from_pretrained(base_id, torch_dtype=torch.float16)

    if adapter_path is not None:
        from peft import PeftModel

        model = PeftModel.from_pretrained(model, adapter_path)
        model = model.merge_and_unload()

    model.eval()

    # Minimal example inputs driving the exporter. Shapes must match what the
    # Kotlin side will push at runtime.
    dummy_image = torch.zeros(1, 3, 384, 384, dtype=torch.float16)
    dummy_ids = torch.zeros(1, 128, dtype=torch.long)
    sample = (dummy_ids, dummy_image)

    import ai_edge_torch
    from ai_edge_torch.generative.quantize import quant_recipes

    recipe = quant_recipes.full_int4_weights_only_recipe()
    edge_model = ai_edge_torch.convert(
        model,
        sample,
        quant_config=recipe,
        _ai_edge_converter_flags={"enable_mlir_converter": True},
    )

    out.parent.mkdir(parents=True, exist_ok=True)
    edge_model.export(str(out))
    print(f"Wrote {out} ({out.stat().st_size / 1e9:.2f} GB)")

    # Save tokenizer alongside for Kotlin to mmap
    tok_out = out.parent / "tokenizer.model"
    processor.tokenizer.save_pretrained(tok_out.parent)
    print(f"Tokenizer at {tok_out}")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--base", default="google/gemma-4-e4b-it")
    p.add_argument("--adapter", type=Path, default=None)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    convert(args.base, args.adapter, args.out)


if __name__ == "__main__":
    main()
