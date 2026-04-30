# Fine-tuning Gemma 4 with Unsloth for PSL

This is the walk-through that sits behind `training/unsloth_finetune.ipynb`.

## Why Unsloth specifically

Three reasons, all measurable:

1. **Memory.** Gemma 4 E4B in 4-bit via Unsloth's `FastVisionModel` fits a
   Kaggle T4 (16 GB). Plain HF loading OOMs.
2. **Speed.** Unsloth's fused attention + LoRA kernels cut step time by
   about 1.7× vs the reference `transformers + peft + bitsandbytes` stack.
3. **One-line GGUF export.** `model.save_pretrained_gguf()` gives us the
   Ollama-ready artefact and llama.cpp-ready artefact in one call, which
   lets us hit the Ollama and llama.cpp prize criteria as free side-effects.

## Recipe

```text
base        unsloth/gemma-4-e4b-it-bnb-4bit  (4-bit, vision + language)
adapter     LoRA r=16, α=32, dropout=0.05, bias=none
trainable   vision + language + attn + MLP (all four flags = True)
optim       adamw_8bit, lr=1.5e-4, cosine, 20 warmup steps
precision   bf16 activations, 4-bit weights
batch       2 × 8 grad-accum  ⇒  effective 16
epochs      2 on ~15 k clips  ⇒  ≈ 40 min on T4
data        WLASL-2000 + INCLUDE-50 + PSL-100 (see DATA.md)
loss        standard SFT (masking out the system + user turns)
```

## Prompt template used in training

Identical to what the backend uses at inference — kept byte-identical so
behaviour doesn't drift:

```json
{
  "messages": [
    {"role": "system",    "content": [{"type": "text",  "text": "<SIGN_TO_TEXT_SYSTEM>"}]},
    {"role": "user",      "content": [{"type": "image", ...} × 16,
                                      {"type": "text",  "text": "Translate this PSL clip..."}]},
    {"role": "assistant", "content": [{"type": "text",  "text": "<JSON answer>"}]}
  ]
}
```

Only the assistant span contributes to loss; everything else is masked.

## Schedule

| Stage | Epoch | Reason |
|---|---:|---|
| Vision adaptation on WLASL | 0 – 0.5 | Handles hand-shape distribution |
| Joint blend (all three datasets) | 0.5 – 2.0 | Rest of the run |

We deliberately do **not** over-fit PSL-100 — its 1 k clips would collapse
onto memorised glosses in 5 epochs, and we saw exactly that in ablation
runs. Two epochs over the full blend is the sweet spot.

## What didn't work

Tried, abandoned, worth documenting:

- **32-rank LoRA:** +0.3 pp accuracy at +70 % memory. Not worth it on T4.
- **Training with only text turns, then adding vision:** sign model
  learned the *schema* but not the signs — gloss top-1 stuck at 66 %.
- **Frame rate 8 fps:** 2× training time, −0.2 pp accuracy — Gemma 4's
  token budget starts to saturate.
- **Separate fine-tunes for sign-to-text vs text-to-sign:** two LoRAs
  work marginally better in isolation (+0.4 pp each) but we chose a single
  adapter for the on-device story — switching adapters on phone is slow.

## Reproducibility

All three pieces are public:

- Notebook: [`training/unsloth_finetune.ipynb`](../training/unsloth_finetune.ipynb)
- Data prep: [`training/data_prep.py`](../training/data_prep.py)
- Datasets: WLASL + INCLUDE-50 (open) + PSL-100 (ours, CC-BY 4.0)

One person, one laptop, one free Kaggle notebook. From clone to numbers
in ~70 minutes.
