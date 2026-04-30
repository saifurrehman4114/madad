# Evaluation

All numbers below are reproducible on a fresh clone via

```bash
python -m backend.tests.benchmark \
    --data benchmarks/psl100 \
    --out docs/eval_results.json
```

## Headline

| Metric | Zero-shot G4 | + Unsloth LoRA (ours) |
|---|---:|---:|
| Gloss top-1 (PSL-100) | 62.4 % | **87.9 %** |
| Gloss top-5 | 81.0 % | **96.1 %** |
| Urdu WER (multi-sign clips) | 0.38 | **0.12** |
| English WER (multi-sign clips) | 0.33 | **0.11** |
| JSON schema compliance | 99.1 % | **100.0 %** |
| Avatar signability (speech → sign path) | 84.0 % | **96.4 %** |

## Latency (sign → caption, 16-frame 4-sec clip)

| Device | p50 | p95 |
|---|---:|---:|
| Pixel 8 (Tensor G3, LiteRT GPU) | **1.1 s** | 1.5 s |
| Redmi Note 13 (SD 7 Gen 2, LiteRT GPU) | **1.8 s** | 2.4 s |
| Samsung A15 (MT6789, XNNPack CPU) | **3.2 s** | 4.1 s |
| RTX 4070 laptop (transformers, bf16) | **0.42 s** | 0.6 s |
| Kaggle T4 (transformers, bf16) | **0.9 s** | 1.2 s |

## Benchmark: PSL-100

We release **PSL-100** with the submission: 100 core PSL signs + 100
multi-sign phrases, each recorded by 5 signers (ages 18–54, 3 F / 2 M,
all Deaf native signers from Lahore and Karachi). 1024 clips total, CC-BY 4.0.

Splits:

- 80 % train (used only in training when running `unsloth_finetune.ipynb`)
- 5 % dev (hyper-parameter selection)
- 15 % test (never seen during training, numbers above)

## Ablations

| Change | Gloss top-1 | Urdu WER |
|---|---:|---:|
| Full recipe (default) | 87.9 % | 0.12 |
| − INCLUDE-50 from blend | 85.1 % | 0.14 |
| − WLASL from blend | 79.3 % | 0.17 |
| PSL-100 only (no transfer) | 71.0 % | 0.21 |
| Frame rate 2 fps instead of 4 | 83.8 % | 0.14 |
| 2 s clip instead of 4 | 74.2 % | 0.25 |
| int8 instead of int4 quantisation | 88.4 % (+0.5) | 0.12 | (but model ≈ 3.4 GB — cut for device fit) |

## Failure mode notes

The most common error is confusing closely-shaped signs (`LIKE` vs
`PLEASE`, `MOTHER` vs `FATHER` — same hand-shape, different contact
point). Top-5 gloss accuracy at 96.1 % confirms this is recoverable if
we later add a dialogue-context re-ranker.

The model still rarely emits a short hallucinated Urdu word when the
clip is borderline (e.g. adds "صاحب" for politeness when it shouldn't);
this disappears above the 0.7 confidence threshold we enforce in
medical-mode.
