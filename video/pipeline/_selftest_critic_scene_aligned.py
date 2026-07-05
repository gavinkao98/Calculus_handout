"""Run: python video/pipeline/_selftest_critic_scene_aligned.py"""
import sys
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


if __name__ == "__main__":
    test_plan_frames_includes_scene_aligned()
    print("OK critic scene_aligned self-test (Task 10)")
