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

The `--dry-run` contract (code review 2026-09-23 C-01). r1 Task C made `--dry-run`
skip the fullest-frame decode to "stay free", but `--dry-run` IS gate 1's documented
invocation (REVIEW_GATES layer 7, the visual-frame-audit agent, VISUAL-FRAME-RUBRIC),
so gate 1 went on reading the cleared end frame of every `exit:` scene. The decode is
local and costs no API call -- which is all "dry" promises -- so `--dry-run` now picks
the fullest frame too (the old "dry-run never decodes" test is replaced). Two more
failures on the same path: the end clamp `dur - 0.05` fell past the last frame's
timestamp below 20 fps (480p15 `--quality low` got no frame at all) -- it is now half a
frame before the last one, from the stream's own fps; and a planned frame that cannot
be extracted used to leave the run at exit 0 -- it now fails the run.
"""
import json
import subprocess
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


def _encode(frames: np.ndarray, path: Path, fps: int = critic.INK_FPS) -> None:
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "gray",
         "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
         "-c:v", "libx264", "-pix_fmt", "yuv420p", str(path)],
        input=frames.tobytes(), check=True, capture_output=True)


def _png_ink(png: Path) -> float:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(png), "-vf",
                          f"scale={W}:{H},format=gray", "-f", "rawvideo", "-"],
                         capture_output=True, check=True).stdout
    return float((np.frombuffer(raw, dtype=np.uint8) > 127).mean())


def _run_main(td: Path, clips: dict, flags: list, beats=((0.0, 1.0),)) -> tuple:
    """Drive critic.main() over a one-scene-per-clip deck: `clips` maps scene id -> mp4
    (None = not rendered). Only the manifest and mp4 lookups are stubbed -- plan_frames,
    extract_frames, ffmpeg and ffprobe all run for real. Returns (rc, plan)."""
    sb = td / "deckx.yml"
    sb.write_text("meta: {id: deckx, section: '9.9'}\nscenes:\n" + "".join(
        f"  - {{id: {sid}, kind: content, template: callout}}\n" for sid in clips),
        encoding="utf-8")
    manifest = {"deck_id": "deckx", "scenes": [{
        "scene_id": sid, "narration_mode": "beats", "script": "x",
        "beats": [{"index": i, "reveal": f"r{i}", "text": "x", "start_seconds": a,
                   "end_seconds": b} for i, (a, b) in enumerate(beats, 1)]} for sid in clips]}
    out = td / "out"
    out.mkdir()
    orig = critic.load_manifest, critic.find_scene_video, sys.argv
    critic.load_manifest = lambda deck_id, meta=None: manifest
    critic.find_scene_video = lambda deck_id, sid: clips[sid]
    sys.argv = ["critic.py", "--storyboard", str(sb), "--out", str(out), *flags]
    try:
        rc = critic.main()
    finally:
        critic.load_manifest, critic.find_scene_video, sys.argv = orig
    return rc, json.loads((out / "frame_plan.json").read_text(encoding="utf-8"))


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


def test_dry_run_hands_gate_1_the_fullest_frame_of_an_exit_scene():
    """`--dry-run` is how gate 1 is run; it must extract what gate 1 is told it reads."""
    # 30 fps like the 1080p30 render: 2 s of content, then 1 s cleared (an `exit:` tail)
    frames = np.stack([_frame(0.10)] * 60 + [_frame(0.0)] * 30)
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as td:
        td = Path(td)
        clip = td / "exit.mp4"
        _encode(frames, clip, fps=30)
        rc, plan = _run_main(td, {"s1": clip}, ["--dry-run"])
        ink = _png_ink(Path(plan[0]["frame_path"]))
    assert rc == 0, rc
    assert plan[0]["fullest_ts"] is not None and plan[0]["fullest_ts"] < 2.0, plan[0]
    assert ink > 0.05, f"--dry-run extracted the cleared end frame (ink {ink:.3f})"


def test_the_end_frame_is_reachable_at_15_fps():
    """`--quality low` renders 480p15: one frame lasts 0.067 s, so `dur - 0.05` asked for
    a moment after the last frame and ffmpeg returned nothing, for every scene."""
    frames = np.stack([_frame(0.02 * (i // 5 + 1)) for i in range(45)])   # 3 s, ink only grows
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as td:
        td = Path(td)
        clip = td / "low.mp4"
        _encode(frames, clip, fps=15)
        rc, plan = _run_main(td, {"s1": clip}, ["--dry-run"])
        ink = _png_ink(Path(plan[0]["frame_path"])) if plan[0]["frame_path"] else None
    assert plan[0]["frame_path"], f"no frame extracted at 15 fps: {plan[0]}"
    assert rc == 0, rc
    assert abs(ink - 0.18) < 0.01, ink       # the last (fullest) frame, not an earlier one


def test_a_planned_frame_that_cannot_be_extracted_fails_the_run():
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as td:
        td = Path(td)
        clip = td / "s1.mp4"
        _encode(np.stack([_frame(0.10)] * 60), clip, fps=30)
        rc, plan = _run_main(td, {"s1": clip, "s2": None}, ["--dry-run"])
    assert [bool(p["frame_path"]) for p in plan] == [True, False], plan
    assert rc != 0, "a gate that silently audits fewer frames than it planned must not pass"


if __name__ == "__main__":
    import traceback
    fails = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn(); print(f"PASS {name}")
            except Exception:
                fails += 1; print(f"FAIL {name}"); traceback.print_exc()
    sys.exit(1 if fails else 0)
