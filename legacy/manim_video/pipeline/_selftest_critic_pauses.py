"""Self-test: critic.py times its frame grabs on the clock make.py rendered, `pauses:` included.
Run from video/:
    python -m pipeline._selftest_critic_pauses

What it pins (code review 2026-09-23 C-07 = B-02, critic side). make.py folds a scene's
`pauses:` into its IN-MEMORY manifest only (`pauses.apply_pauses`); the on-disk manifest
stays the TTS record. critic.py re-reads the on-disk one, so `--per beat` grabbed every
beat at and after a hold `seconds` too early -- a beat shorter than the hold plus its reveal
would be grabbed showing the PREVIOUS beat's composition, labelled as this one. The test
drives the real `main()` (manifest lookup and mp4 lookup stubbed; no render, no API) and
compares its `frame_plan.json` with the grab times the in-memory manifest gives.
"""
import copy
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline import critic  # noqa: E402  (import triggers _bootstrap.bootstrap())

import yaml  # noqa: E402

from pipeline import audio, pauses  # noqa: E402


def _disk_manifest(wav: Path) -> dict:
    beats, t = [], 0.0
    for i, (secs, reveal) in enumerate([(4.0, "step.0"), (5.0, "step.1"), (6.0, "step.2")], 1):
        beats.append({"index": i, "reveal": reveal, "text": f"beat {i}", "audio_seconds": secs,
                      "start_seconds": t, "end_seconds": t + secs})
        t += secs
    return {"deck_id": "deckp", "scenes": [{
        "scene_id": "s1", "scene_number": 1, "narration_mode": "beats", "script": "x",
        "audio_file": str(wav), "audio_seconds": t, "beats": beats}]}


def _plan(per: str) -> tuple[list, dict, dict]:
    """(frame_plan.json of `critic.py --per <per> --dry-run`, disk manifest, make.py's
    in-memory manifest) for one paused scene."""
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as td:
        tmp = Path(td)
        sb = tmp / "deckp.yml"
        sb.write_text("meta: {id: deckp, section: '9.9'}\nscenes:\n"
                      "  - {id: s1, kind: content, template: callout, "
                      "say: '{show step.0} a {show step.1} b {show step.2} c', "
                      "pauses: [{after: step.1, seconds: 1.5}]}\n", encoding="utf-8")
        wav = tmp / "01_s1.wav"
        audio.write_pcm_wav(wav, audio.silence_pcm(15.0))
        disk = _disk_manifest(wav)
        scenes = yaml.safe_load(sb.read_text(encoding="utf-8"))["scenes"]
        mem = pauses.apply_pauses(scenes, copy.deepcopy(disk), tmp / "paused")  # make.py's call
        out = tmp / "out"
        out.mkdir()

        orig = critic.load_manifest, critic.find_scene_video, sys.argv
        critic.load_manifest = lambda deck_id, meta=None: copy.deepcopy(disk)
        critic.find_scene_video = lambda deck_id, sid: None
        sys.argv = ["critic.py", "--storyboard", str(sb), "--per", per, "--dry-run",
                    "--out", str(out)]
        try:
            critic.main()
        finally:
            critic.load_manifest, critic.find_scene_video, sys.argv = orig
        return json.loads((out / "frame_plan.json").read_text(encoding="utf-8")), disk, mem


def _settled_on_the_rendered_clock(mem: dict) -> list:
    return [round(max(critic.LEAD_SECONDS + b["end_seconds"] - critic.BEAT_BACKOFF, 0.05), 3)
            for b in mem["scenes"][0]["beats"]]


def test_per_beat_grabs_are_timed_on_the_rendered_clock():
    plan, disk, mem = _plan("beat")
    want = _settled_on_the_rendered_clock(mem)
    assert [round(p["ts"], 3) for p in plan] == want, ([p["ts"] for p in plan], want)
    assert want[1] > disk["scenes"][0]["beats"][1]["end_seconds"] + 1.0, "fixture has no hold"


def test_per_scene_fullest_candidates_are_on_the_rendered_clock():
    """The fullest-frame pick only considers settled moments (C-02); those must be the
    rendered film's, or a candidate after the hold lands inside the next beat's reveal."""
    plan, _disk, mem = _plan("scene")
    assert [round(t, 3) for t in plan[0]["settled"]] == _settled_on_the_rendered_clock(mem), plan[0]


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
