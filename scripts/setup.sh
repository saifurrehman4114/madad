#!/usr/bin/env bash
# Madad one-shot bootstrap.
#
# Run from the repo root:
#   bash scripts/setup.sh
#
# What this does, in order:
#   1. Sanity-checks required tooling (python3, node, npm, ollama).
#   2. Creates a Python venv and installs backend deps.
#   3. Installs frontend deps.
#   4. Pulls the base Gemma 4 model into Ollama (user still has to create the
#      fine-tuned variant with `ollama create` after training — see step 5).
#   5. Prints the next commands for training + running the demo.

set -euo pipefail

RED='\033[0;31m'
GRN='\033[0;32m'
YEL='\033[1;33m'
NC='\033[0m'

info() { printf "${GRN}==>${NC} %s\n" "$*"; }
warn() { printf "${YEL}!! ${NC} %s\n" "$*"; }
err()  { printf "${RED}xx ${NC} %s\n" "$*" 1>&2; }

require() {
  if ! command -v "$1" >/dev/null 2>&1; then
    err "missing required tool: $1"
    exit 1
  fi
}

info "checking toolchain"
require python3
require node
require npm
if ! command -v ollama >/dev/null 2>&1; then
  warn "ollama not found — install from https://ollama.com/download before the demo"
fi

info "creating .env if missing"
if [ ! -f .env ]; then
  cp .env.example .env
  info "  wrote .env (edit if you want the transformers backend)"
fi

info "setting up backend venv"
python3 -m venv backend/.venv
# shellcheck disable=SC1091
source backend/.venv/bin/activate
pip install --upgrade pip wheel
pip install -r backend/requirements.txt
deactivate

info "installing frontend deps"
( cd frontend && npm install )

if command -v ollama >/dev/null 2>&1; then
  info "pulling base Gemma 4 E4B (this is large — a few GB)"
  ollama pull gemma4:e4b-it || warn "pull failed — run manually later"
fi

cat <<'EOF'

========================================================================
Next steps
========================================================================

1) Train the LoRA adapter (Kaggle T4 or Colab A100):
     - open training/unsloth_finetune.ipynb
     - set WANDB off, run all cells
     - download training/outputs/madad-gemma4.Q4_K_M.gguf

2) Register the fine-tuned model with Ollama:
     ollama create madad-gemma4 -f training/Modelfile

3) Run the demo locally:
     # terminal 1
     source backend/.venv/bin/activate
     uvicorn main:app --reload --app-dir backend
     # terminal 2
     cd frontend && npm run dev
     # open http://localhost:5173

4) Or run everything in Docker:
     docker compose up --build

5) Run the PSL-100 benchmark:
     source backend/.venv/bin/activate
     python backend/tests/benchmark.py --manifest data/psl100/manifest.jsonl

6) Build the Android APK (after LiteRT conversion — see docs/FINE_TUNING.md):
     cd mobile/litert_android && ./gradlew assembleRelease

EOF

info "done."
