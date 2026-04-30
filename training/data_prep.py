"""
One-shot data preparation for Madad.

Builds manifest.csv files for three open sign-language datasets so the Unsloth
notebook can consume them uniformly.

Datasets:
    WLASL-2000      CC-BY-NC 4.0  — used for vision-pretraining only
    INCLUDE-50 (ISL) research     — South-Asian hand-shape transfer
    PSL-100         CC-BY 4.0     — our curated Pakistan Sign Language bench

Manifest schema:
    path,gloss,urdu,english,source_dataset
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path


def wlasl_manifest(root: Path, out: Path) -> int:
    """Expects `nslt_2000.json` and `videos/` subdir (standard WLASL layout)."""
    meta = json.loads((root / "nslt_2000.json").read_text())
    rows = []
    for vid, v in meta.items():
        clip = root / "videos" / f"{vid}.mp4"
        if not clip.exists():
            continue
        rows.append(
            {
                "path": str(clip),
                "gloss": v["action"][0].upper().replace(" ", "-"),
                "urdu": "",
                "english": v["action"][0],
                "source_dataset": "wlasl2000",
            }
        )
    return _write(out, rows)


def include50_manifest(root: Path, out: Path) -> int:
    """INCLUDE-50 distributes one folder per class."""
    rows = []
    for cls_dir in sorted(root.iterdir()):
        if not cls_dir.is_dir():
            continue
        gloss = cls_dir.name.upper().replace("_", "-")
        for clip in cls_dir.glob("*.mp4"):
            rows.append(
                {
                    "path": str(clip),
                    "gloss": gloss,
                    "urdu": "",
                    "english": cls_dir.name.replace("_", " "),
                    "source_dataset": "include50",
                }
            )
    return _write(out, rows)


def psl100_manifest(root: Path, out: Path) -> int:
    """Our own benchmark. Expects `labels.csv` with columns path,gloss,urdu,english."""
    src = root / "labels.csv"
    rows = []
    with src.open() as fh:
        for row in csv.DictReader(fh):
            clip = root / row["path"]
            if not clip.exists():
                continue
            rows.append(
                {
                    "path": str(clip),
                    "gloss": row["gloss"].upper(),
                    "urdu": row["urdu"],
                    "english": row["english"],
                    "source_dataset": "psl100",
                }
            )
    return _write(out, rows)


def _write(path: Path, rows: list[dict]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(
            fh, fieldnames=["path", "gloss", "urdu", "english", "source_dataset"]
        )
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


def main() -> None:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    for name, fn in (
        ("wlasl", wlasl_manifest),
        ("include50", include50_manifest),
        ("psl100", psl100_manifest),
    ):
        s = sub.add_parser(name)
        s.add_argument("--root", type=Path, required=True)
        s.add_argument("--out", type=Path, required=True)
        s.set_defaults(fn=fn)

    args = p.parse_args()
    n = args.fn(args.root, args.out)
    print(f"{args.cmd}: wrote {n} rows to {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
