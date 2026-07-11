"""Offline self-test for pipeline/listening_pack.py (no API, no manim, no render).
Run: python video/pipeline/_selftest_listening_pack.py"""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline import listening_pack as LP  # noqa: E402


def _manifest():
    return {"deck_id": "d", "scenes": [
        {"scene_id": "clean_fast", "narration_mode": "scene_aligned", "audio_seconds": 6.0,
         "script": "w " * 20, "validation": {"status": "pass", "warnings": [],
         "qa": {"status": "ran", "verdict": "ok"}}},                          # 200 wpm > 175 -> rank 5
        {"scene_id": "failed", "narration_mode": "scene_aligned", "audio_seconds": 10.0,
         "script": "a b c", "validation": {"status": "fail", "warnings": ["x"],
         "qa": {"status": "ran"}}},                                           # rank 1 (fail beats warnings)
        {"scene_id": "terminal_beat", "narration_mode": "beats", "audio_seconds": 10.0,
         "script": "a b c", "fallback_history": [{"rung": "beats"}]},         # rank 2
        {"scene_id": "warned", "narration_mode": "scene_aligned", "audio_seconds": 10.0,
         "script": "a b c", "validation": {"status": "pass_with_warnings",
         "warnings": ["low prob"], "qa": {"status": "ran"}}},                 # rank 3
        {"scene_id": "legacy", "narration_mode": "scene_aligned", "audio_seconds": 10.0,
         "script": "a b c", "validation": {"status": "pass", "warnings": [], "metrics": {}}},  # no qa -> rank 4
        {"scene_id": "quiet", "narration_mode": "silent", "duration": 6.0},   # rank 6
    ]}


def test_wpm():
    assert abs(LP._wpm("w " * 20, 6.0) - 200.0) < 0.01     # 20 words / 6s -> 200 wpm
    assert LP._wpm("", 6.0) == 0.0
    assert LP._wpm("a b", 0.0) == 0.0                       # audio_seconds guard (no div-by-zero)
    assert LP._wpm("a b", -3.0) == 0.0


def test_qa_three_state():
    assert LP._qa_state({"qa": {"status": "ran"}}) == "ran"
    assert LP._qa_state({"qa": {"status": "skipped", "reason": "x"}}) == "skipped"
    assert LP._qa_state({"qa": {"status": "error"}}) == "error"
    assert LP._qa_state({"status": "pass"}) == "legacy-missing"     # no qa key (pre-T4 manifest)
    assert LP._qa_state({"qa": None}) == "legacy-missing"           # present-but-null


def test_rows_ranking_and_wpm():
    rows = LP.rows_from_manifest(_manifest())
    order = [r["scene_id"] for r in rows]
    assert order == ["failed", "terminal_beat", "warned", "legacy", "clean_fast", "quiet"], order
    cf = next(r for r in rows if r["scene_id"] == "clean_fast")
    assert cf["wpm"] == 200.0 and cf["risk_rank"] == 5
    assert next(r for r in rows if r["scene_id"] == "legacy")["qa_state"] == "legacy-missing"


def test_measure_loudness_is_error_safe():
    with tempfile.TemporaryDirectory() as d:
        out = LP.measure_loudness(Path(d) / "nonexistent.wav")
        assert isinstance(out, dict) and "error" in out    # missing file -> {"error":...}, never raises


def test_html_escapes_user_text():
    rows = [{"scene_id": "s<1>", "narration_mode": "scene_aligned", "script": "a < b & c",
             "audio_file": None, "audio_seconds": 5.0, "wpm": 10.0, "status": "pass",
             "warnings": [], "qa_state": "ran", "fallback_history": [], "risk_rank": 6}]
    doc = LP.render_html(rows, "deck", Path("."))
    assert "a &lt; b &amp; c" in doc and "s&lt;1&gt;" in doc   # escaped, not raw injection


if __name__ == "__main__":
    for name in sorted(n for n in dir() if n.startswith("test_")):
        globals()[name]()
        print(f"  ok {name}")
    print("[selftest] listening_pack green")
