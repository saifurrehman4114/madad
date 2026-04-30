"""
Frame extraction utilities. Gemma 4 accepts a sequence of images as video input.
We sample at a fixed FPS and downscale to a consistent short-edge size.
"""
from __future__ import annotations

import io
from pathlib import Path

import cv2
import numpy as np
from PIL import Image


def extract_frames(
    source: Path | bytes,
    target_fps: int = 4,
    max_seconds: float = 4.0,
    short_edge: int = 384,
) -> list[Image.Image]:
    """Decode a video and return up to ``target_fps * max_seconds`` PIL frames.

    ``source`` may be a filesystem path or raw bytes (e.g. from an upload).
    """
    if isinstance(source, (str, Path)):
        cap = cv2.VideoCapture(str(source))
    else:
        tmp = Path("/tmp/_madad_clip.mp4")
        tmp.write_bytes(source)
        cap = cv2.VideoCapture(str(tmp))

    if not cap.isOpened():
        raise ValueError("Could not open video source")

    src_fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    stride = max(int(round(src_fps / target_fps)), 1)
    max_frames = int(target_fps * max_seconds)

    frames: list[Image.Image] = []
    idx = 0
    while len(frames) < max_frames:
        ok, bgr = cap.read()
        if not ok:
            break
        if idx % stride == 0:
            frames.append(_to_pil(bgr, short_edge))
        idx += 1
    cap.release()

    if not frames:
        raise ValueError("No frames decoded from video source")
    return frames


def _to_pil(bgr: np.ndarray, short_edge: int) -> Image.Image:
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    h, w = rgb.shape[:2]
    scale = short_edge / min(h, w)
    if scale < 1.0:
        rgb = cv2.resize(
            rgb, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA
        )
    return Image.fromarray(rgb)


def frames_to_bytes(frames: list[Image.Image], fmt: str = "JPEG") -> list[bytes]:
    out: list[bytes] = []
    for f in frames:
        buf = io.BytesIO()
        f.save(buf, format=fmt, quality=88)
        out.append(buf.getvalue())
    return out
