# Madad — Kaggle Submission Checklist

Everything Claude built is in this repo. This doc is the **only** thing
Saif has to execute. Work top-to-bottom; each step has a time budget and
a "done when" acceptance criterion. Deadline: **2026-05-18 23:59 UTC**.

Total human time: roughly **2 working days** spread over 2 weeks, most of
which is waiting for GPU jobs to finish.

---

## Phase 0 — Local bring-up (90 min)

| # | Action | Done when |
|---|--------|-----------|
| 0.1 | Install [Ollama](https://ollama.com/download) and the Android Studio Hedgehog+. | `ollama --version` prints. |
| 0.2 | From repo root: `bash scripts/setup.sh`. | Script finishes with "done." |
| 0.3 | `ollama pull gemma4:e4b-it` (if the setup script didn't). | `ollama list` shows it. |
| 0.4 | Start backend + frontend (two terminals, see the script output). | `http://localhost:5173` loads; health badge is green. |
| 0.5 | In the UI click **Sign → Speech**, record a 2s clip of yourself waving. | A JSON-shaped caption comes back (quality will be poor pre-training — that is expected). |

If 0.5 fails, check `backend/logs` and the `/health` endpoint before moving on.

---

## Phase 1 — Data (half a day, mostly download time)

| # | Action | Done when |
|---|--------|-----------|
| 1.1 | Download **WLASL-2000** from Kaggle into `data/raw/wlasl/`. Kaggle has the CC-BY-NC version. | `data/raw/wlasl/videos/` has ~21k mp4s. |
| 1.2 | Download **INCLUDE-50** (ISL, CC-BY 4.0) into `data/raw/include50/`. | 50 class folders present. |
| 1.3 | Record **PSL-100**: 100 signs × 3 signers × 3 takes = 900 clips. Use your phone, 1080p, 30fps, plain wall. See `docs/DATA.md` for the sign list. | `data/raw/psl100/` has ~900 mp4s + `manifest.csv`. |
| 1.4 | `python backend/tests/../training/data_prep.py --all`. | `data/manifests/{train,val,test}.jsonl` exist, split is signer-disjoint. |

> **PSL-100 is the hardest step.** If you cannot record all 900 clips, record
> 100 (1 signer × 1 take per sign) — enough for the demo but mention it in
> the writeup.

---

## Phase 2 — Fine-tune on Kaggle (4–6h, mostly passive)

| # | Action | Done when |
|---|--------|-----------|
| 2.1 | Upload `data/manifests/` + a tarball of video frames to a new Kaggle dataset called `madad-psl-signing`. | Dataset is private, ~10 GB. |
| 2.2 | Create a new Kaggle notebook on a **T4×2** kernel. Enable GPU + Internet. | Kernel boots. |
| 2.3 | Upload `training/unsloth_finetune.ipynb`, attach the dataset, **Run All**. | 2 epochs complete; `outputs/madad-gemma4.Q4_K_M.gguf` appears. |
| 2.4 | Download the GGUF to `training/outputs/` locally. | File is ~2.5 GB. |
| 2.5 | `ollama create madad-gemma4 -f training/Modelfile`. | `ollama list` shows `madad-gemma4`. |
| 2.6 | Restart backend; rerun Phase 0.5 — captions should now be sensible. | A waved clip returns a reasonable gloss + urdu. |

---

## Phase 3 — Benchmark (1h)

| # | Action | Done when |
|---|--------|-----------|
| 3.1 | `python backend/tests/benchmark.py --manifest data/manifests/test.jsonl`. | Prints the table in `docs/EVALUATION.md`. |
| 3.2 | Copy the real numbers into `docs/EVALUATION.md` and `docs/KAGGLE_WRITEUP.md` (replacing the placeholders). | Both docs have matching numbers. |
| 3.3 | Commit: `git commit -am "eval: real PSL-100 numbers"`. | Clean working tree. |

---

## Phase 4 — Android build (half a day)

| # | Action | Done when |
|---|--------|-----------|
| 4.1 | `python mobile/litert_android/convert.py` — produces `madad-gemma4.task`. | File is ~1.8 GB int4. |
| 4.2 | Drop the `.task` into `mobile/litert_android/app/src/main/assets/`. | Present and committed via git-lfs. |
| 4.3 | Open the Android project in Studio, build a debug APK on your own phone. | App launches, permission grant, camera view shows. |
| 4.4 | Record a 10s clip in-app — verify offline (turn on aeroplane mode first). | Caption appears; aeroplane mode stayed on. |

---

## Phase 5 — Video pitch (1 day, the one thing no AI can do)

| # | Action | Done when |
|---|--------|-----------|
| 5.1 | Read `docs/VIDEO_SCRIPT.md` end to end; adjust anything that doesn't feel natural. | You can narrate it without the script. |
| 5.2 | Record the 6 scenes on your phone / laptop camera. Ideally include a real PSL signer (Deaf Reach intro in `docs/partners/deaf_reach.md`). | 6 clips in `.mov`. |
| 5.3 | Edit in CapCut / Resolve: under **3 minutes**, 1080p, loud clean audio, English captions baked in (judges scrub). | `madad-pitch.mp4` exists, ≤ 2:59. |
| 5.4 | Upload unlisted to YouTube. | You have a `youtu.be/...` link. |

> The pitch is 1 of the 3 judging pillars. Nail the opening 10 seconds —
> Ayesha's story. Show a real deaf user if you possibly can.

---

## Phase 6 — Cover image (15 min)

1. Follow `assets/cover_image_spec.md` in Figma.
2. Export 1200×630 PNG → `assets/cover.png`.

---

## Phase 7 — Partnerships (async, send today)

| # | Action |
|---|--------|
| 7.1 | Email the Deaf Reach letter (`docs/partners/deaf_reach.md`) to `info@deafreach.com`. |
| 7.2 | Email the NAD letter (`docs/partners/nad.md`). |
| 7.3 | Screenshot any **reply** — positive or "we'll review" — for the writeup. It doesn't have to be a formal endorsement; a reply letter is credibility. |

---

## Phase 8 — Final writeup polish (2h)

| # | Action | Done when |
|---|--------|-----------|
| 8.1 | Reread `docs/KAGGLE_WRITEUP.md` and drop in: real eval numbers (Phase 3), YouTube link (Phase 5), any partner reply screenshot (Phase 7). | No `TODO` strings remain in the writeup. |
| 8.2 | Sanity-read `README.md` from a fresh cloner's POV. Can they get to a working demo with only `scripts/setup.sh` + Phase 2.5? | Yes. |
| 8.3 | Tag: `git tag v1.0-kaggle && git push --tags`. | Tag visible on GitHub. |

---

## Phase 9 — Kaggle submission (30 min)

1. Kaggle → **Gemma 4 Good Hackathon** → New Writeup.
2. Cover image: `assets/cover.png`.
3. Paste the body of `docs/KAGGLE_WRITEUP.md` (Kaggle accepts Markdown).
4. Attach / link:
   - GitHub repo: `https://github.com/<you>/madad`
   - YouTube video (unlisted is fine)
   - Kaggle model: upload `madad-gemma4.Q4_K_M.gguf` as a public Kaggle Model
     named `madad-gemma4-e4b-psl-lora` (required for the **Gemma 4 Model Track**
     if we want to stack that prize).
5. Tick the prize tracks:
   - [x] Main track — Digital Equity & Inclusivity
   - [x] Unsloth Special Award
   - [x] LiteRT Special Award
   - [x] Gemma 4 Model Track (if you uploaded the GGUF above)
6. **Preview** the writeup. Scroll the whole thing on mobile. Then **Submit**.

Done when: Kaggle confirms submission and it appears on your profile.

---

## What Claude explicitly cannot help with

- Recording the PSL-100 videos (Phase 1.3) — needs real signers.
- The pitch video (Phase 5) — this is the human story.
- Clicking the final **Submit** button on Kaggle (Phase 9.6).

Everything else is either code in this repo or a shell command that runs
against this repo. If any step fails with output you don't understand,
open a new Claude session pointing at this repo — all the context it needs
is already checked in.

Good luck. 🤞
