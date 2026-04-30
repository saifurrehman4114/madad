#!/usr/bin/env bash
# Kaggle submission script for Madad.
#
# Prerequisites — do these ONCE:
#   1. Go to https://www.kaggle.com/settings  → API section
#   2. Click "Create New Token"  →  a file called kaggle.json downloads
#   3. Move it:   mkdir -p ~/.kaggle && mv ~/Downloads/kaggle.json ~/.kaggle/
#   4. chmod 600 ~/.kaggle/kaggle.json
#   5. Run this script:   bash scripts/kaggle_submit.sh

set -euo pipefail
RED='\033[0;31m'; GRN='\033[0;32m'; YEL='\033[1;33m'; NC='\033[0m'
info() { printf "${GRN}==>${NC} %s\n" "$*"; }
err()  { printf "${RED}xx ${NC} %s\n" "$*" >&2; exit 1; }

# ── 1. Check Kaggle CLI ───────────────────────────────────────────────────
if ! command -v kaggle >/dev/null 2>&1; then
  info "installing kaggle CLI…"
  pip3 install --break-system-packages --quiet kaggle \
    || pip3 install --quiet kaggle \
    || err "Could not install kaggle CLI — run: pip3 install kaggle"
fi

if [ ! -f "$HOME/.kaggle/kaggle.json" ]; then
  err "~/.kaggle/kaggle.json not found.
  1. Go to https://www.kaggle.com/settings → API → Create New Token
  2. Move the downloaded file: mkdir -p ~/.kaggle && mv ~/Downloads/kaggle.json ~/.kaggle/
  3. chmod 600 ~/.kaggle/kaggle.json
  4. Re-run this script."
fi
chmod 600 "$HOME/.kaggle/kaggle.json"

# ── 2. Join competition (safe to run even if already joined) ──────────────
info "joining competition…"
kaggle competitions list | grep -q gemma-4-good-hackathon \
  || kaggle competitions join gemma-4-good-hackathon 2>/dev/null || true

# ── 3. Push notebook ──────────────────────────────────────────────────────
info "pushing notebook to Kaggle…"
cd "$(dirname "$0")/../training"
kaggle kernels push .

info "notebook pushed — it will run on Kaggle's T4 GPU (≈25 min)."
printf "${YEL}Track progress:${NC} https://www.kaggle.com/code/saifurrehman4114/madad-psl-interpreter\n"

# ── 4. Wait for kernel to finish (poll every 60s) ─────────────────────────
info "waiting for kernel to finish (Ctrl-C to skip, check manually)…"
STATUS="running"
WAIT=0
while [[ "$STATUS" == "running" || "$STATUS" == "queued" ]]; do
  sleep 60
  WAIT=$((WAIT+60))
  STATUS=$(kaggle kernels status saifurrehman4114/madad-psl-interpreter \
           2>/dev/null | awk '{print $NF}' | tr -d '",' || echo "unknown")
  printf "  [%ds] status: %s\n" "$WAIT" "$STATUS"
  if [ "$WAIT" -gt 3600 ]; then
    printf "${YEL}Timed out — check manually at the URL above.${NC}\n"
    break
  fi
done

if [[ "$STATUS" == "complete" ]]; then
  info "kernel finished successfully!"
  printf "${GRN}Your submission is live:${NC}\n"
  printf "  Notebook: https://www.kaggle.com/code/saifurrehman4114/madad-psl-interpreter\n"
  printf "  Repo    : https://github.com/saifurrehman4114/madad\n"
  printf "\nRemaining manual steps:\n"
  printf "  1. Upload your pitch video to YouTube (unlisted OK)\n"
  printf "  2. Post the YouTube URL in the competition Discussion tab\n"
  printf "  3. Tick the prize tracks in the competition entry form\n"
else
  printf "${YEL}Kernel status: %s — check the URL above for errors.${NC}\n" "$STATUS"
fi
