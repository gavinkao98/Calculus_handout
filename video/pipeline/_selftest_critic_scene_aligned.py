"""Run: python video/pipeline/_selftest_critic_scene_aligned.py"""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline import critic  # noqa: E402


def test_plan_frames_includes_scene_aligned():
    storyboard = {"meta": {}, "scenes": [{"id": "s", "title": "T"}]}
    manifest = {"scenes": [{"scene_id": "s", "scene_number": 7,
                            "narration_mode": "scene_aligned", "script": "hello",
                            "beats": [{"index": 1, "id": "beat_01", "reveal": None,
                                       "text": "hello", "end_seconds": 1.0}]}]}
    plan = critic.plan_frames(storyboard, manifest, "all", per="scene")
    assert len(plan) == 1 and plan[0]["scene_id"] == "s"


def _content_entry(sid, stale_scene_number):
    return {"scene_id": sid, "scene_number": stale_scene_number,
            "narration_mode": "scene_aligned", "script": "hello",
            "beats": [{"index": 1, "id": "beat_01", "reveal": None,
                       "text": "hello", "end_seconds": 1.0}]}


def test_scene_number_is_the_full_deck_storyboard_order_not_the_manifest_value():
    """Pins the 2026-09-13 bug: a manifest merged across renders can carry a stale
    scene_number (two different scenes both stamped 17). critic must number from the
    STORYBOARD's own full scene order (intro/divider/content/outro all take a slot,
    matching rewatch_pack.py and a fresh tts.py manifest), never from the manifest
    entry, so a stale manifest can no longer collide or diverge."""
    storyboard = {"meta": {}, "scenes": [
        {"id": "intro", "kind": "intro"},
        {"id": "divider_a", "kind": "divider"},
        {"id": "sine", "kind": "content", "title": "sine"},
        {"id": "cosine", "kind": "content", "title": "cosine"},
        {"id": "slope", "kind": "content", "title": "slope"},
        {"id": "outro", "kind": "outro"},
    ]}
    # stale manifest: "cosine" and "slope" both carry the same wrong scene_number,
    # as actually happened after a scene was inserted/removed between renders.
    manifest = {"scenes": [
        _content_entry("sine", 12),
        _content_entry("cosine", 17),
        _content_entry("slope", 17),
    ]}
    plan = critic.plan_frames(storyboard, manifest, "all", per="scene")
    numbers = {p["scene_id"]: p["scene_number"] for p in plan}
    # full-deck 1-based position: intro=1, divider_a=2, sine=3, cosine=4, slope=5, outro=6
    assert numbers == {"sine": 3, "cosine": 4, "slope": 5}, numbers
    assert len(set(numbers.values())) == len(numbers), "scene numbers must not collide"


def test_reset_frames_dir_clears_stale_frames_but_tolerates_a_missing_dir():
    with tempfile.TemporaryDirectory() as td:
        out_dir = Path(td)
        # a missing frames/ must not raise
        critic.reset_frames_dir(out_dir)
        frames = out_dir / "frames" / "17_old_scene"
        frames.mkdir(parents=True)
        (frames / "final.png").write_bytes(b"stale")
        critic.reset_frames_dir(out_dir)
        assert not (out_dir / "frames").exists()


if __name__ == "__main__":
    test_plan_frames_includes_scene_aligned()
    test_scene_number_is_the_full_deck_storyboard_order_not_the_manifest_value()
    test_reset_frames_dir_clears_stale_frames_but_tolerates_a_missing_dir()
    print("OK critic scene_aligned self-test (Task 10)")
