# Data

Madad is trained on a blend of three sign-language corpora. This document
tracks licences, provenance, and reproducibility.

## PSL-100 (ours)

First released Pakistan Sign Language benchmark with Urdu sentence-level
gold. Released under **CC-BY 4.0** with this submission.

- **Size:** 1 024 clips — 100 core signs × 5 signers × ≈2 tokens (single +
  multi-sign utterances).
- **Signers:** 5 Deaf native PSL signers, ages 18–54, 3 F / 2 M, Lahore
  (3) + Karachi (2).
- **Recording:** Android Pixel 7a front camera, neutral grey background,
  1080p / 30 fps → downsampled to 480p.
- **Labels:** gloss (English UPPERCASE) + Urdu sentence (Nastaliq) +
  English paraphrase. Double-labelled by two different signers; conflicts
  resolved with a third.
- **Link:** Kaggle Datasets · `saifrh/psl-100` (flips public on
  submission deadline).

## WLASL-2000

Word-level American Sign Language. We use only its ~10 k most frequent
clips. **CC-BY-NC 4.0.** Because it is non-commercial, we use WLASL only
as fine-tune input and we do **not** redistribute it; users fetch it
directly from the original authors' release.

## INCLUDE-50

Indian Sign Language benchmark from IIT Madras. Research licence.
Overlaps with PSL in ~55 % of common signs (per community surveys) so it
provides useful hand-shape transfer.

## Train / test discipline

- PSL-100 test split (15 %, stratified by signer) is **never** seen in
  training. We ensure signer-disjoint splits to prevent leakage.
- WLASL and INCLUDE-50 are used only for training — all reported metrics
  are on the PSL-100 test split.

## Bias notes

- Signer skew: 3/5 signers are from Lahore. Regional PSL dialects are
  under-represented. Flagged as roadmap item for PSL-500.
- Age skew: range 18-54, no children signers. Children produce visually
  different signs (smaller hand-shapes) and should be included in v2.

## Ethical clearance

PSL-100 signers each signed an Urdu-language release form (available on
request, redacted for signer privacy) explicitly granting CC-BY 4.0
release and commercial downstream use.
