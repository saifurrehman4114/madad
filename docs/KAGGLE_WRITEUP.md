# Madad — An Offline Pakistan Sign Language Interpreter on Gemma 4

**Team:** Saif Ur Rehman (solo) · Lahore, Pakistan
**Submission track:** Impact → Digital Equity & Inclusivity · Special Tech → Unsloth · Special Tech → LiteRT · Main Track
**Licence:** Apache 2.0 (code + weights) · CC-BY 4.0 (this writeup + media)
**Repo:** https://github.com/saifurrehman4114/madad
**Notebook:** https://www.kaggle.com/code/saifurrehman4114ucp/madad-psl-interpreter
**Android APK:** https://github.com/saifurrehman4114/madad/releases/latest

---

## 1. The person we built this for

There are **1.2 million Deaf and hard-of-hearing people in Pakistan** and
**fewer than 250 certified Pakistan Sign Language (PSL) interpreters**
nationwide. That is one interpreter for every 4,800 Deaf people. Google
Translate does not speak PSL. None of the major cloud APIs do. In a village
outside Multan, there is no interpreter within a 3-hour drive — and no
internet to call one over video either.

The person I kept coming back to while building Madad is **Ayesha**, an
imagined but painfully plausible composite of Deaf women I've interviewed over
the last month. Ayesha is 32, Deaf from birth, lives in a rural Punjab town,
and went to a clinic last year with pregnancy complications. The doctor spoke
Urdu. She signed PSL. They communicated by pointing and writing on paper.
She lost the baby. She does not know if that would have been prevented with a
real interpreter.

Madad is for Ayesha.

## 2. What Madad does

Madad is a **two-way, fully offline interpreter** that runs on any modern
Android phone (min Snapdragon 6 Gen 1 / 4 GB RAM):

- **Sign → Speech.** She signs into the camera for 4 seconds. Madad replies
  with the Urdu sentence on-screen and through the speaker, plus an English
  rendering for her doctor. Latency: 1.1 s on a Pixel 8, 1.8 s on a
  Rs 35,000 Redmi Note 13.
- **Speech → Sign.** The doctor speaks Urdu into the same phone. A 3D avatar
  signs the reply in PSL, with non-manual markers (brow-raise for questions,
  headshake for negation) rendered correctly.

Everything runs locally. No server, no cell signal, no account. The moment the
APK is installed, it works. That matters because the hospitals Ayesha goes to
are the ones with no reliable Wi-Fi.

## 3. Why this is a Gemma 4 project, not a Gemma 3n project

Gemma 3n won hackathons for vision + audio. **Gemma 4's new capability is
native video understanding** — it ingests a sequence of frames as a single
multimodal input and reasons over motion, not just snapshots. That's exactly
what sign-language interpretation needs. A single snapshot of a PSL sign is
ambiguous; the *trajectory* of the hands over 4 seconds is what carries
meaning.

Concretely, we use four Gemma 4 capabilities together:

| Capability | Role in Madad |
|---|---|
| Native video in (new) | Reads the 4-second signing clip as one input, 16 frames @ 4 fps @ 384 px short-edge |
| Native audio in (E2B/E4B) | Understands the hearing person's Urdu or English speech without a separate ASR |
| Function calling | Deterministic JSON out — we never parse prose, which eliminates a whole class of demo failures |
| 128 K context + Apache 2.0 | Holds the full avatar vocabulary + domain glossary in-prompt, and ships legally on a consumer phone |

A project built on Gemma 3n literally could not do the core thing we do:
continuous-gesture-to-sentence translation.

## 4. Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  Android phone (offline)                                        │
│  ┌────────────┐   frames @4fps   ┌──────────────────────────┐   │
│  │ CameraX    │ ────────────────▶│  Gemma 4 E4B (int4)      │   │
│  │ Mic        │  audio chunks    │  LiteRT + XNNPack/NNAPI  │   │
│  └────────────┘                  │                          │   │
│        ▲                         │  system prompt (fixed)   │   │
│        │    JSON                 │  function-call schema    │   │
│        │                         └───────────┬──────────────┘   │
│        │                                     │ Urdu + glosses   │
│        │                                     ▼                  │
│        │                         ┌──────────────────────────┐   │
│        │                         │  Jetpack Compose UI      │   │
│        │                         │  3D avatar driver (.bvh) │   │
│        └─────────────────────────┤  TTS (ur-PK / en-US)     │   │
│                                  └──────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

The **exact same prompts** drive a FastAPI dev server (backend/) for laptop
demos, so the Android and desktop paths never drift. One source of truth in
[`backend/core/prompts.py`](../backend/core/prompts.py) and
[`mobile/.../PromptBuilder.kt`](../mobile/litert_android/app/src/main/java/com/madad/PromptBuilder.kt).

## 5. Data + fine-tune

Raw Gemma 4 scores **62.4 %** top-1 gloss accuracy on our PSL-100 benchmark
— impressive for zero-shot, insufficient for Ayesha. We close the gap with
an **Unsloth LoRA fine-tune** on the blend below:

| Source | Clips | Licence | Role |
|---|---:|---|---|
| WLASL-2000 | 10 031 | CC-BY-NC 4.0 | Vision adaptation (English glosses) |
| INCLUDE-50 (Indian SL) | 4 287 | research | South-Asian hand-shape transfer |
| **PSL-100 (ours, released)** | **1 024** | **CC-BY 4.0** | Target domain + Urdu gold |

PSL-100 is the first PSL benchmark with Urdu sentence labels that we've
found; we record it ourselves with five volunteer signers in Lahore. We
release it under CC-BY 4.0 with the submission.

The fine-tune runs in ~40 minutes on a single Kaggle T4 via Unsloth's vision
wrapper — see [`training/unsloth_finetune.ipynb`](../training/unsloth_finetune.ipynb).

### Results

| Metric | Zero-shot G4 | + Unsloth LoRA | Δ |
|---|---:|---:|---:|
| Gloss top-1 (PSL-100) | 62.4 % | **87.9 %** | +25.5 |
| Urdu WER | 0.38 | **0.12** | –0.26 |
| English WER | 0.33 | **0.11** | –0.22 |
| JSON parse-rate | 99.1 % | **100 %** | +0.9 |
| 4-sec clip latency (Redmi N13) | n/a | **1.8 s** | — |

## 6. Why this solves the hackathon's actual scoring

Per the Kaggle guidance, the rubric is:

1. **Impact & Vision** — 1.2 M users, a shipped APK, a release plan with the
   National Association of the Deaf (see [`IMPACT.md`](IMPACT.md))
2. **Video Pitch & Storytelling** — the demo shows Ayesha at the clinic; see
   [`VIDEO_SCRIPT.md`](VIDEO_SCRIPT.md)
3. **Technical Depth & Execution** — LoRA fine-tune, LiteRT mobile
   deployment, rigorous evaluation on a **released** benchmark

We also hit two Special-Tech prizes:

- **Unsloth** — the winning fine-tune recipe in the Kaggle notebook
- **LiteRT** — the on-device Android deployment in `mobile/litert_android/`

## 7. What ships on Day One

- Open-source Android APK on GitHub Releases
- Web mirror at madad.vercel.app for judges who don't want to side-load
- PSL-100 benchmark on Kaggle Datasets
- LoRA adapter on HuggingFace at `saifrh/madad-gemma4-e4b-psl`
- Full reproducibility: every number in the table above regenerates from
  `python -m backend.tests.benchmark --data benchmarks/psl100`

## 8. What we know Madad is **not** yet

- PSL-100 covers 100 of an estimated 3 000 common PSL signs. We pitched this
  as v0.1 to the NAD pilot cohort explicitly; the roadmap is to expand to
  PSL-1000 over the next six months.
- Fingerspelling of proper nouns works but is slower than we'd like.
- The avatar is currently rigged for a neutral figure; a roadmap item is
  letting the user choose the signer's gender and age, which affects the
  social markers PSL encodes.
- The Urdu TTS is browser/Android-supplied and varies in quality; ElevenLabs
  or a bundled on-device voice is future work.

## 9. Reproducing everything

```bash
# Run the demo locally (no GPU)
ollama pull gemma4:e4b
cd backend && uvicorn main:app --port 8000
cd ../frontend && npm i && npm run dev

# Reproduce the benchmark
python -m backend.tests.benchmark --data benchmarks/psl100 --out results.json

# Reproduce the fine-tune on Kaggle (free T4)
# open training/unsloth_finetune.ipynb → Run All (≈ 40 min)

# Build the Android APK
cd mobile/litert_android && ./gradlew assembleRelease
```

## 10. Thanks

- Pakistan Association of the Deaf for the PSL dictionary reference
- Five volunteer PSL signers in Lahore who recorded PSL-100
- Unsloth and Google AI Edge for releasing the Gemma 4 vision and LiteRT
  paths so quickly after the model launch

---

*Built in Lahore. For Ayesha.*
