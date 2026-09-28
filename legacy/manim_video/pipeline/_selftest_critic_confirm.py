"""Self-test: `critic.py --confirm` reports failed VLM calls as failures. Run from video/:
    python -m pipeline._selftest_critic_confirm

What it pins (code review 2026-09-23 C-05). `run_critique` records a failed call and
carries on (one bad frame must not lose the batch), but `main()` returned `0 if results
else 1` -- so a batch where EVERY call failed (an expired MIMO_API_KEY: 21 x HTTP 401)
exited 0 and an orchestrator reading the exit code saw success; and `critique.md` wrote
each failure as "could not parse JSON; raw model output" over an empty block, so the
HTTP status that explained it never reached the human report.

Offline by construction: `critique_frame` -- the only function that opens a connection --
is replaced for the whole test, the key is a dummy set in this process only, and the
frames come from a synthesised clip.
"""
import io
import json
import os
import subprocess
import sys
import tempfile
import urllib.error
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline import critic  # noqa: E402  (import triggers _bootstrap.bootstrap())

import numpy as np  # noqa: E402


def _clip(path: Path) -> None:
    frames = np.zeros((60, 108, 192), dtype=np.uint8)
    frames[:, 20:60, 20:100] = 255
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "gray",
                    "-s", "192x108", "-r", "30", "-i", "-", "-c:v", "libx264",
                    "-pix_fmt", "yuv420p", str(path)],
                   input=frames.tobytes(), check=True, capture_output=True)


def _http_401(item, **_kw):
    raise urllib.error.HTTPError("https://example.invalid/chat/completions", 401,
                                 "Unauthorized", {}, io.BytesIO(b'{"error": "invalid api key"}'))


def _ok(item, **_kw):
    return {"raw": "{}", "usage": {}, "critique": {
        "visual_blocking_count": 0, "v_findings": [], "scores": {}, "defects": [],
        "overall": "clean"}}


def _confirm(critique_frame, scenes=("s1", "s2")) -> tuple:
    """Drive `critic.py --confirm` over a small deck with `critique_frame` replaced.
    Returns (exit code, critique.md text)."""
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as td:
        td = Path(td)
        clip = td / "clip.mp4"
        _clip(clip)
        sb = td / "deckc.yml"
        sb.write_text("meta: {id: deckc, section: '9.9'}\nscenes:\n" + "".join(
            f"  - {{id: {s}, kind: content, template: callout}}\n" for s in scenes),
            encoding="utf-8")
        manifest = {"deck_id": "deckc", "scenes": [{
            "scene_id": s, "narration_mode": "beats", "script": "x",
            "beats": [{"index": 1, "reveal": "r", "text": "x", "start_seconds": 0.0,
                       "end_seconds": 0.5}]} for s in scenes]}
        out = td / "out"
        saved = (critic.load_manifest, critic.find_scene_video, critic.critique_frame,
                 sys.argv, os.environ.get("MIMO_API_KEY"))
        critic.load_manifest = lambda deck_id, meta=None: manifest
        critic.find_scene_video = lambda deck_id, sid: clip
        critic.critique_frame = critique_frame
        os.environ["MIMO_API_KEY"] = "dummy-key-offline-selftest"
        sys.argv = ["critic.py", "--storyboard", str(sb), "--out", str(out), "--confirm"]
        try:
            rc = critic.main()
        finally:
            (critic.load_manifest, critic.find_scene_video, critic.critique_frame,
             sys.argv, key) = saved
            if key is None:
                os.environ.pop("MIMO_API_KEY", None)
            else:
                os.environ["MIMO_API_KEY"] = key
        return rc, (out / "critique.md").read_text(encoding="utf-8")


def test_a_batch_where_every_call_failed_exits_non_zero():
    rc, _md = _confirm(_http_401)
    assert rc != 0, "every VLM call failed and the run still exited 0"


def test_one_failed_call_in_a_batch_exits_non_zero():
    calls = []

    def first_fails(item, **kw):
        calls.append(item["scene_id"])
        return _http_401(item) if len(calls) == 1 else _ok(item)
    rc, _md = _confirm(first_fails)
    assert calls == ["s1", "s2"], "one bad frame must not stop the batch"
    assert rc != 0, "a partly failed gate-2 batch must not read as a clean run"


def test_critique_md_shows_the_error_not_a_json_parse_story():
    _rc, md = _confirm(_http_401)
    assert "HTTP 401" in md and "invalid api key" in md, md
    assert "could not parse JSON" not in md, md


def test_a_clean_batch_still_exits_zero_and_an_unparseable_reply_is_still_labelled_so():
    rc, _md = _confirm(_ok)
    assert rc == 0, rc
    rc, md = _confirm(lambda item, **kw: {"raw": "not json", "usage": {}, "critique": None})
    assert rc == 0 and "could not parse JSON" in md and "not json" in md, (rc, md)


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
