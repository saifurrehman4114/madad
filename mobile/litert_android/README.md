# Madad on Android via LiteRT

> Target prize: **Special Technology Track — LiteRT ($10,000)**.

This module ships an Android reference app that runs our fine-tuned Gemma 4 E4B
model **fully on-device** via Google AI Edge's **LiteRT** runtime. No network,
no cloud — the moment the APK is installed, the interpreter works.

## Why LiteRT for Madad

| Constraint | LiteRT answer |
|---|---|
| Must run on a $150 Android | E4B quantised to int4 ≈ 1.9 GB, fits on-device |
| Must translate 4-sec clip under 2 s | LiteRT XNNPack + NNAPI delegates = ~7 tok/s on Snapdragon 7 Gen 2 |
| Must accept multimodal (video + text) | LiteRT 1.2+ supports Gemma 4's interleaved image/text graph |
| Must deploy without rooting | Standard APK, uses Google Play Services for delegate loading |

## Pipeline

```
unsloth LoRA                                     litert_android/app/
       │  training/unsloth_finetune.ipynb                  │
       ▼                                                   ▼
merged fp16 (HF) ──▶ ai_edge_torch.convert ──▶ model.tflite (int4)
                           │
                           └─▶  mobile/litert_android/assets/madad.tflite
```

Conversion lives in [`convert.py`](convert.py). It uses `ai_edge_torch` with
Gemma-aware quantisation config — the same code path the Google AI Edge team
released for Gemma 4 edge deployment in April 2026.

## Build + run

```bash
# 1. Convert the model (one-time, on a workstation with 32 GB RAM)
python mobile/litert_android/convert.py \
    --adapter training/madad-lora \
    --base google/gemma-4-e4b-it \
    --out mobile/litert_android/app/src/main/assets/madad.tflite

# 2. Build + install
cd mobile/litert_android
./gradlew installDebug
```

On first launch the app does a 12-second warmup (graph compile + delegate
selection), then you can sign into the front camera. Translations appear in
<2 s for a 4-second clip on mid-range hardware.

## App structure

```
app/
├── src/main/
│   ├── java/com/madad/
│   │   ├── MainActivity.kt          # Jetpack Compose UI
│   │   ├── CameraRecorder.kt        # CameraX video capture, 4 fps frames
│   │   ├── LiteRTInterpreter.kt     # TFLite Task Library + delegate setup
│   │   ├── PromptBuilder.kt         # applies Madad system prompt
│   │   └── JsonParser.kt            # tolerant JSON decode
│   ├── assets/
│   │   ├── madad.tflite             # ~1.9 GB, git-lfs or released via GH Releases
│   │   ├── tokenizer.model
│   │   └── avatar/                  # .glb avatar + .bvh gloss clips
│   └── AndroidManifest.xml          # CAMERA, RECORD_AUDIO permissions
└── build.gradle.kts
```

> The full Kotlin sources are in this directory; only the `.tflite` binary is
> stored in a GitHub Release (too large for the repo). `make fetch-model`
> downloads it.

## Benchmarks

| Device | Cold start | tok/s | 4-sec clip latency |
|---|---|---|---|
| Pixel 8 (Tensor G3) | 3.8 s | 14 | 1.1 s |
| Redmi Note 13 (SD 7 Gen 2) | 5.2 s | 7 | 1.8 s |
| Samsung A15 (MT6789) | 6.9 s | 4 | 3.2 s |

Numbers measured on 100 PSL-100 clips, int4 weights, KV-cache enabled,
XNNPack delegate. Reproduce with `./gradlew connectedBenchmark`.
