from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
import pytest

from backend.core.video import extract_frames


@pytest.fixture
def tiny_clip(tmp_path: Path) -> Path:
    path = tmp_path / "clip.mp4"
    writer = cv2.VideoWriter(
        str(path), cv2.VideoWriter_fourcc(*"mp4v"), 24, (640, 480)
    )
    for i in range(96):  # 4 seconds @ 24 fps
        frame = np.full((480, 640, 3), (i * 3) % 255, dtype=np.uint8)
        writer.write(frame)
    writer.release()
    return path


def test_extract_frames_returns_expected_count(tiny_clip: Path):
    frames = extract_frames(tiny_clip, target_fps=4, max_seconds=4.0)
    assert 14 <= len(frames) <= 16  # sampling jitter tolerated


def test_extract_frames_downscales(tiny_clip: Path):
    frames = extract_frames(tiny_clip, short_edge=128)
    assert min(frames[0].size) == 128


def test_bad_source_raises(tmp_path: Path):
    bad = tmp_path / "nope.mp4"
    bad.write_bytes(b"not a video")
    with pytest.raises(ValueError):
        extract_frames(bad)
