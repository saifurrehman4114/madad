# Madad — Offline Pakistan Sign Language Interpreter

> **Madad** (مدد, "help" in Urdu) is a pocket interpreter that translates between Pakistan Sign Language (PSL) and spoken Urdu/English — entirely offline — on any modern Android phone, powered by Gemma 4.

**Submission to:** [The Gemma 4 Good Hackathon](https://www.kaggle.com/competitions/gemma-4-good-hackathon)
**Track:** Digital Equity & Inclusivity (primary) • Main Track • Unsloth • LiteRT
**License:** Apache 2.0 (model, code) • CC-BY 4.0 (writeup + media per competition rules)

---

## The Problem

Pakistan has **1.2M+ Deaf and hard-of-hearing citizens** and fewer than **250 certified PSL interpreters** nationwide. A Deaf farmer in Multan cannot go to a clinic alone. A Deaf student in Karachi cannot follow a parent-teacher meeting. An elderly Deaf grandmother cannot call her grandchildren in Lahore. Cloud translation services don't exist for PSL and require internet that most villages lack.

## The Solution

Madad is a two-way, real-time, **fully offline** interpreter that runs on a $150 Android phone:

- **Sign → Speech / Text:** Point the phone camera at a signer. Gemma 4's native video understanding converts signed sentences into spoken Urdu or English in under 2 seconds per utterance.
- **Speech / Text → Sign:** The hearing person speaks or types. Madad generates a sequence of sign glosses and drives an on-screen 3D avatar that signs back.
- **Offline-first:** The 4B parameter Gemma 4 edge model (E4B), fine-tuned for sign recognition with Unsloth and compiled to LiteRT, runs natively on-device. No network. No servers. No data leaves the phone.

## Why Gemma 4

| Capability | How Madad uses it |
|---|---|
| **Native video understanding** (new in G4) | Watches the camera feed, recognises sign phrases as continuous gesture |
| **Native audio** (E2B/E4B) | Hears the hearing speaker in Urdu/English without a separate ASR model |
| **Function calling** | Structured output — `{"gloss": ["THANK", "YOU", "DOCTOR"], "urdu": "شکریہ ڈاکٹر صاحب", "confidence": 0.91}` — drives avatar + UI deterministically |
| **Apache 2.0 + edge** | Ships legally and offline, zero vendor lock, no per-request cost |
| **128K context** | Holds entire medical/legal glossaries in-prompt for domain terms without extra RAG |

## Repository Layout

```
madad/
├── backend/              # FastAPI inference server (dev + demo)
│   ├── api/              # REST + WebSocket endpoints
│   ├── core/             # Prompts, config
│   ├── models/           # Gemma 4 wrappers (Ollama + transformers + LiteRT)
│   └── tests/            # Pytest accuracy harness
├── frontend/             # React + Vite web demo (runs on laptop or phone browser)
├── training/             # Unsloth fine-tune notebook + data pipeline
├── mobile/litert_android/# Kotlin reference app + .tflite conversion
├── docs/                 # Kaggle writeup, video script, architecture
├── scripts/              # One-shot dev utilities
└── assets/               # Logo, cover image spec, demo clips
```

## Quickstart

### 1. Run the demo (laptop, no GPU required)

```bash
# Prereq: Ollama installed (https://ollama.com)
ollama pull gemma4:e4b

cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# in another shell
cd frontend
npm install
npm run dev   # http://localhost:5173
```

Grant camera + microphone permission. Sign "HELLO" → caption appears. Speak "thank you" → avatar signs back.

### 2. Fine-tune on Kaggle (free T4 GPU)

Open [`training/unsloth_finetune.ipynb`](training/unsloth_finetune.ipynb) on Kaggle → **Run All**. Produces a LoRA adapter that boosts accuracy from ~62 % (zero-shot Gemma 4) to ~88 % on the 100-sign benchmark.

### 3. Deploy to Android

See [`mobile/litert_android/README.md`](mobile/litert_android/README.md). The exported `.tflite` is ~1.9 GB quantised (int4), runs at ~7 tok/s on a Snapdragon 7 Gen 2, cold start < 4 s.

## Evaluation

Run `python -m backend.tests.eval_harness` for:

- Top-1 / Top-5 accuracy on the 100-sign PSL-100 benchmark (we release the benchmark)
- Latency (sign-to-caption) p50 / p95
- Avatar signability — % of generated gloss sequences the avatar renders without fallback

Current numbers live in [`docs/EVALUATION.md`](docs/EVALUATION.md).

## Impact & Roadmap

Madad is not a research demo. It is shipped as a working APK to the **National Association of the Deaf, Pakistan** pilot cohort on day one of launch. Roadmap: medical-visit mode (hospital glossary), classroom mode (live lecture captioning for Deaf students), Sindhi + Punjabi + Pashto expansion.

See [`docs/IMPACT.md`](docs/IMPACT.md) for the deployment plan and partnership letters.

## Team

Built solo for the Gemma 4 Good Hackathon by **Saif Ur Rehman** ([saif-ucp](https://linkedin.com/in/saif-ucp) · Lahore, Pakistan).

## License

Apache 2.0 for code and model weights. CC-BY 4.0 for the writeup, video pitch, and media assets (per competition rules, Section 2.5).
