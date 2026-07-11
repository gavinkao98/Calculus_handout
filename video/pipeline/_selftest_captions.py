"""Offline self-test for pipeline/captions.py (no API, no manim, no render).
Run: python video/pipeline/_selftest_captions.py"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline import captions as C  # noqa: E402


def _fixtures():
    manifest = {"scenes": [
        {"scene_id": "intro", "beats": []},                                   # brand frame, no narration
        {"scene_id": "s1", "narration_mode": "beats", "beats": [
            {"text": "hello", "start_seconds": 0.0, "end_seconds": 1.5},
            {"text": "  ", "start_seconds": 1.5, "end_seconds": 2.0},          # empty -> no cue
            {"text": "world", "start_seconds": 2.0, "end_seconds": 3.0}]},
    ]}
    timeline = {"deck_id": "d", "lead_seconds": 2.0, "scenes": [
        {"scene_id": "intro", "kind": "intro", "start": 0.0, "end": 6.0,
         "chapter_title": "Inverse Functions"},
        {"scene_id": "s1", "kind": "content", "start": 6.0, "end": 12.0, "narration_mode": "beats"},
    ]}
    return manifest, timeline


def test_beat_spans_normalizes_and_drops_empty():
    entry = {"beats": [{"text": "a", "start_seconds": 0, "end_seconds": 1},
                       {"text": "  ", "start_seconds": 1, "end_seconds": 2},   # empty
                       {"text": "b", "start_seconds": 2, "end_seconds": 3}]}
    assert C.beat_spans(entry) == [("a", 0.0, 1.0), ("b", 2.0, 3.0)]
    assert C.beat_spans({"beats": []}) == []


def test_vtt_uses_timeline_lead_and_skips_empty():
    manifest, timeline = _fixtures()
    vtt = C.to_vtt(manifest, timeline)
    assert vtt.startswith("WEBVTT")
    # cue = scene.start(6) + timeline.lead(2) + beat_start -- lead=2.0 proves it isn't the render's 1s
    assert "00:00:08.000 --> 00:00:09.500" in vtt      # "hello" at beat 0.0-1.5
    assert "00:00:10.000 --> 00:00:11.000" in vtt      # "world" at beat 2.0-3.0
    assert vtt.count("-->") == 2                        # the blank beat produced no cue
    starts = re.findall(r"(\d\d:\d\d:\d\d\.\d\d\d) -->", vtt)
    assert starts == sorted(starts)                    # monotonic


def test_chapters_first_is_zero_and_titled_from_timeline():
    _manifest, timeline = _fixtures()
    lines = C.to_chapters(timeline).strip().splitlines()
    assert lines[0].startswith("0:00 ") and "Inverse Functions" in lines[0]


def test_chapters_synthesizes_zero_when_first_is_late():
    timeline = {"scenes": [
        {"scene_id": "d1", "kind": "divider", "start": 12.0, "chapter_title": "Act Two"}]}
    lines = C.to_chapters(timeline).strip().splitlines()
    assert lines[0].startswith("0:00 ")                # a 0:00 chapter is prepended (YouTube requires it)


def test_chapter_title_fallback_order():   # NB3: title -> tagline -> meta.title -> id
    assert C.chapter_title({"id": "intro", "tagline": "run backwards?"}, {"title": "Meta"}) == "run backwards?"
    assert C.chapter_title({"id": "x", "title": "Explicit"}, {"title": "Meta"}) == "Explicit"
    assert C.chapter_title({"id": "y"}, {"title": "Meta"}) == "Meta"
    assert C.chapter_title({"id": "z"}, {}) == "z"


if __name__ == "__main__":
    for name in sorted(n for n in dir() if n.startswith("test_")):
        globals()[name]()
        print(f"  ok {name}")
    print("[selftest] captions green")
