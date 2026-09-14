"""Self-test: critic.py `--per scene` picks the FULLEST frame, not the last one.

Run: python video/pipeline/_selftest_critic_fullest.py

What it pins (backlog #10, KICKOFF-shared-layer-v1.md §8; task contract
KICKOFF-toolline-backlog-r1.md §2.C). `plan_frames()` used to hard-code
`ts = 1e9`, which `extract_frames()` then clamps to `duration - 0.05` -- the LAST
held frame. For a scene with `exit:` the picture is already cleared by then, so
gate 1's frame audit was reading a blank frame and auditing nothing (scenes 06,
23, 2026-09-14 gate-1 pass over ch03_trig_derivatives_mimo).

`_fullest_frame_ts()` fixes this by decoding the whole scene clip the same way
rewatch_pack.motion_stats does (ffmpeg, 4 fps, 192x108, gray) and picking the
frame with the most "ink" (pixels that differ from the scene's background gray
level) instead of the last one. Two things must both hold, tested against the
real ffmpeg/numpy arithmetic (not a mock of it):

  1. A scene that clears itself (content, then a bare background tail) must pick
     a frame from the content half, not the cleared tail.
  2. A scene whose ink only ever grows (no `exit:`, the common case) must still
     pick the last frame -- so every deck without an `exit:` sees ZERO change
     from this fix (the 99%-of-peak override).

A third test pins the `--dry-run` contract: `extract_frames(..., compute_fullest=
False)` must never call `_fullest_frame_ts` at all, so `--dry-run` stays free
(no full-clip decode) and keeps working before a render exists.
"""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline import critic  # noqa: E402  (import triggers _bootstrap.bootstrap())

import numpy as np  # noqa: E402

W, H = 192, 108        # same size critic.py's ink decode uses -- makes the ffmpeg
                       # `scale=192:108` step a no-op, so test frames map 1:1
BG, INK = 0, 255       # max contrast: survives libx264 quantisation noise cleanly


def _frame(ink_frac: float) -> np.ndarray:
    """One (H, W) gray frame: background BG with the first `ink_frac` share of
    pixels set to INK. Placement doesn't matter to the ink measure, only the count."""
    f = np.full((H, W), BG, dtype=np.uint8)
    n_ink = int(round(ink_frac * H * W))
    if n_ink:
        f.reshape(-1)[:n_ink] = INK
    return f


def _encode(frames: np.ndarray, path: Path) -> None:
    import subprocess
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "gray",
         "-s", f"{W}x{H}", "-r", str(critic.INK_FPS), "-i", "-",
         "-c:v", "libx264", "-pix_fmt", "yuv420p", str(path)],
        input=frames.tobytes(), check=True, capture_output=True)


def test_exit_scene_picks_the_content_frame_not_the_cleared_end():
    # 8 frames (2.0 s @ 4 fps) with content, then 4 frames (1.0 s) of bare
    # background -- mirrors a scene with `exit:` clearing the picture at the end.
    frames = np.stack([_frame(0.10)] * 8 + [_frame(0.0)] * 4)
    with tempfile.TemporaryDirectory() as td:
        clip = Path(td) / "exit.mp4"
        _encode(frames, clip)
        found = critic._fullest_frame_ts(clip)
    assert found is not None, "could not decode the synthesised clip"
    ts, ratio = found
    assert ts < 2.0, found                      # from the content half, not the cleared tail
    assert ts == 7 / critic.INK_FPS, found       # 8 tied-max frames -> tie-break picks the latest
    assert ratio is None, found                  # cleared end has exactly zero ink: undefined ratio


def test_pure_accumulation_still_picks_the_last_frame():
    # ink only ever grows -- no exit, the common case. The fix must not move the
    # pick off the end here, or every deck without an `exit:` would see spurious
    # frame changes.
    fracs = [0.05 * (i + 1) for i in range(12)]
    frames = np.stack([_frame(f) for f in fracs])
    with tempfile.TemporaryDirectory() as td:
        clip = Path(td) / "accum.mp4"
        _encode(frames, clip)
        found = critic._fullest_frame_ts(clip)
    assert found is not None, "could not decode the synthesised clip"
    ts, ratio = found
    assert ts == 11 / critic.INK_FPS, found      # last frame, same as the old behaviour
    assert ratio == 1.0, found


def test_dry_run_skips_the_expensive_decode():
    """--dry-run must never trigger the full-clip decode -- extract_frames() takes
    a compute_fullest flag for exactly this, and main() passes `not args.dry_run`."""
    calls = []
    orig_fullest = critic._fullest_frame_ts
    orig_find = critic.find_scene_video
    critic._fullest_frame_ts = lambda video: (calls.append(video), (0.0, 1.0))[1]
    try:
        with tempfile.TemporaryDirectory() as td:
            clip = Path(td) / "any.mp4"
            _encode(np.stack([_frame(0.0)] * 8), clip)   # ~2 s, just needs to exist
            critic.find_scene_video = lambda deck_id, sid: clip
            item = {"scene_id": "s", "scene_number": 1, "title": "t", "beat_index": 0,
                    "final": True, "ts": 1e9, "fullest_ts": None, "ink_ratio_vs_last": None,
                    "narration": "", "reveal": None, "revealed_so_far": []}
            plan = critic.extract_frames("deck", [dict(item)], Path(td),
                                         compute_fullest=False)
    finally:
        critic._fullest_frame_ts = orig_fullest
        critic.find_scene_video = orig_find
    assert calls == [], "compute_fullest=False must not decode the scene video"
    assert plan[0]["ts"] == 1e9 and plan[0]["fullest_ts"] is None, plan[0]


if __name__ == "__main__":
    test_exit_scene_picks_the_content_frame_not_the_cleared_end()
    test_pure_accumulation_still_picks_the_last_frame()
    test_dry_run_skips_the_expensive_decode()
    print("OK critic fullest-frame self-test (backlog #10 / task C)")
