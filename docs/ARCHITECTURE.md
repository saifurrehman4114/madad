# Madad — Architecture

One model. Two directions. Two deployment targets. One shared prompt.

```
                  ┌─── Gemma 4 E4B (Unsloth LoRA) ────┐
 Sign video ─────▶│   native video in                 │────▶ JSON (glosses, Urdu, English)
                  │   function-calling schema         │
 Urdu / English ─▶│   native audio in (E2B/E4B)       │────▶ JSON (avatar-signable clauses)
                  └──────────────┬─────────────────────┘
                                 │
                 ┌───────────────┴────────────────┐
                 │                                │
         LiteRT (Android)                 Ollama / transformers
         mobile/litert_android/           backend/ (FastAPI)
         1.9 GB int4                      dev + demo only
```

## Components

- **Model:** `google/gemma-4-e4b-it` → Unsloth LoRA → merged fp16 → ai_edge_torch int4
- **Tokenizer:** upstream Gemma 4 — no modifications
- **Prompts:** two system prompts (sign→text, text→sign). Shared source of
  truth in [`backend/core/prompts.py`](../backend/core/prompts.py) and
  byte-identical Kotlin copy in
  [`PromptBuilder.kt`](../mobile/litert_android/app/src/main/java/com/madad/PromptBuilder.kt).
- **Function-calling schema:** JSON schema enforced on both backends.
  Ollama via the `format` field, transformers via a post-hoc tolerant
  parser, LiteRT via the MediaPipe session output.
- **Video I/O:** 4 fps sampling at 384-px short edge for 4 s = 16 frames
  per clip. OpenCV on desktop, CameraX on Android.
- **Audio I/O:** native to Gemma 4 E4B — no Whisper / no separate ASR.
- **Avatar:** 120-sign vocabulary, `.bvh` clips per sign rendered by a
  rigged GLTF figure. Shared list in
  [`avatar_vocab.py`](../backend/api/avatar_vocab.py) / `AvatarVocab.kt`.

## Data flow (Sign → Speech, Android)

1. User taps "Sign" → CameraRecorder starts sampling at 4 fps.
2. After 4 s, 16 Bitmap frames → `LiteRTInterpreter.signToText`.
3. Gemma 4 session gets: system prompt + 16 images + user prompt.
4. Output: JSON with `{glosses, urdu, english, confidence, notes}`.
5. JSON parsed → Urdu sent to Android TTS (`ur-PK`) → spoken aloud.
6. `confidence < 0.3` triggers a "please try again or find an interpreter"
   fallback card instead of reading out a guess.

## Data flow (Speech → Sign, Android)

1. User speaks Urdu or English.
2. Text captured via Android SpeechRecognizer (falls back to Gemma 4 E4B
   native audio in v0.2).
3. Text + avatar vocabulary → `LiteRTInterpreter.textToSign`.
4. JSON output with `clauses[].glosses[]`.
5. AvatarPlayer plays the `.bvh` clip for each gloss, with non-manual
   markers (`Q:` = brow raise, `N:` = head shake) driving a blend-shape.

## Sync between the two backends

The FastAPI backend exists only for developer ergonomics (laptop demo, CI
tests, benchmark harness). On the judging day the Android app is the
product. To keep drift-free:

- prompts live in one file per language (Python / Kotlin) with the string
  constants byte-identical. A pre-commit hook diff-checks them.
- `avatar_vocab.py` and `AvatarVocab.kt` are generated from the same YAML
  — see `scripts/sync_vocab.py`.
- The evaluation harness (`backend/tests/benchmark.py`) runs the same
  prompts Ollama receives, so desktop numbers are comparable to phone
  numbers.

## Why not server-side?

The target user is in a village with no internet. A model call over
Cloudflare doesn't help them. Every architectural decision flows from
"must work at 0 Mbps".
