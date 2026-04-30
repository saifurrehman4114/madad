"""
PSL-100 benchmark runner.

Usage:
    python -m backend.tests.benchmark --data benchmarks/psl100 --out results.json

Expected layout:
    benchmarks/psl100/
        manifest.csv         # columns: path,gloss,urdu,english,source_dataset
        clips/
            0001.mp4
            0002.mp4
            ...

Metrics reported:
    - gloss top-1 accuracy     (single-sign clips)
    - WER on Urdu sentence     (multi-sign clips)
    - WER on English sentence  (multi-sign clips)
    - sign-to-caption p50 / p95 latency (ms)
"""
from __future__ import annotations

import argparse
import asyncio
import csv
import json
import statistics
from pathlib import Path

from backend.core.config import get_settings
from backend.core.video import extract_frames
from backend.models.factory import get_model


def wer(ref: str, hyp: str) -> float:
    """Simple word error rate."""
    r, h = ref.strip().split(), hyp.strip().split()
    if not r:
        return 0.0 if not h else 1.0
    # Levenshtein on tokens
    d = [[0] * (len(h) + 1) for _ in range(len(r) + 1)]
    for i in range(len(r) + 1):
        d[i][0] = i
    for j in range(len(h) + 1):
        d[0][j] = j
    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            d[i][j] = min(
                d[i - 1][j] + 1,
                d[i][j - 1] + 1,
                d[i - 1][j - 1] + (0 if r[i - 1] == h[j - 1] else 1),
            )
    return d[-1][-1] / len(r)


async def run(data_dir: Path, out_path: Path) -> None:
    manifest = list(csv.DictReader((data_dir / "manifest.csv").open()))
    settings = get_settings()
    model = await get_model(settings)

    results = []
    for row in manifest:
        clip = data_dir / "clips" / row["path"]
        try:
            frames = extract_frames(clip, target_fps=settings.target_fps)
        except ValueError:
            continue
        pred = await model.sign_to_text(frames, lang_hint="ur")
        results.append(
            {
                "path": row["path"],
                "ref_gloss": row["gloss"],
                "ref_urdu": row["urdu"],
                "ref_english": row["english"],
                "hyp_gloss": " ".join(pred.glosses),
                "hyp_urdu": pred.urdu,
                "hyp_english": pred.english,
                "confidence": pred.confidence,
                "latency_ms": pred.latency_ms,
            }
        )

    top1 = sum(1 for r in results if r["ref_gloss"].split()[0] in r["hyp_gloss"].split()) / len(results)
    wer_ur = statistics.mean(wer(r["ref_urdu"], r["hyp_urdu"]) for r in results)
    wer_en = statistics.mean(wer(r["ref_english"], r["hyp_english"]) for r in results)
    latencies = sorted(r["latency_ms"] for r in results)
    p50 = latencies[len(latencies) // 2]
    p95 = latencies[int(len(latencies) * 0.95)]

    summary = {
        "n": len(results),
        "gloss_top1": round(top1, 4),
        "urdu_wer": round(wer_ur, 4),
        "english_wer": round(wer_en, 4),
        "latency_p50_ms": p50,
        "latency_p95_ms": p95,
        "backend": model.name,
        "adapter": getattr(model, "adapter", None),
    }
    out_path.write_text(json.dumps({"summary": summary, "rows": results}, indent=2))
    print(json.dumps(summary, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=Path("results.json"))
    args = parser.parse_args()
    asyncio.run(run(args.data, args.out))


if __name__ == "__main__":
    main()
