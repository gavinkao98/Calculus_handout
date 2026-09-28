"""Offline self-test for make.py scene_aligned consumers (no render, no ffmpeg).
Run: python video/pipeline/_selftest_make_scene_aligned.py"""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import make  # noqa: E402  (video/ is on sys.path via _bootstrap in make)


def _scene_aligned_entry():
    return {"scene_number": 7, "scene_id": "s", "kind": "content",
            "narration_mode": "scene_aligned", "audio_file": "/x/07_s.wav",
            "audio_seconds": 6.0, "scene_text_hash": "h",
            "script": "a b c d e f", "beat_count": 3,
            "beats": [{"index": i + 1, "id": f"beat_{i+1:02d}", "reveal": None,
                       "text": "a b", "text_hash": "t", "audio_seconds": 2.0,
                       "start_seconds": 2.0 * i, "end_seconds": 2.0 * (i + 1),
                       "word_start": 2 * i, "word_end": 2 * (i + 1),
                       "boundary": {"prob": 0.8, "interpolated": False}} for i in range(3)]}


def test_beat_durations_accepts_scene_aligned():
    m = {"scenes": [_scene_aligned_entry()]}
    assert make._beat_durations(m) == {"s": [2.0, 2.0, 2.0]}


def test_schema_guard_rejects_future_schema():
    try:
        make._check_manifest_schema({"schema": 3, "scenes": []})
    except SystemExit:
        pass
    else:
        raise AssertionError("expected SystemExit on schema>2")
    make._check_manifest_schema({"schema": 2, "scenes": []})   # ok
    make._check_manifest_schema({"scenes": []})                # missing -> schema 1, ok


def test_validate_scene_aligned_freshness():
    # a FRESH scene_aligned entry passes _validate_scene_aligned with NO problems, and
    # each mutated freshness field produces exactly one problem (and NO per-beat
    # audio_file is ever required).
    from pipeline.narration import parse_say
    from pipeline.timing import text_hash
    from pipeline.audio import write_pcm_wav, silence_pcm, wav_duration
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        say = "a b. {show m.0} c d."
        scene = {"id": "s", "kind": "content", "say": say}
        beats = parse_say(say)
        transcript = " ".join(b.text for b in beats if b.text).strip()
        wav = tmp / "07_s.wav"; write_pcm_wav(wav, silence_pcm(4.0))
        words_f = tmp / "07_s.words.json"; words_f.write_text("{}", encoding="utf-8")
        aligned_f = tmp / "07_s.aligned.json"; aligned_f.write_text("{}", encoding="utf-8")

        def entry():
            return {"scene_id": "s", "narration_mode": "scene_aligned", "audio_file": str(wav),
                    "audio_seconds": round(wav_duration(wav), 3), "scene_text_hash": text_hash(transcript),
                    "beats": [{"reveal": b.reveal, "text_hash": text_hash(b.text)} for b in beats],
                    "alignment": {"words_file": str(words_f), "aligned_file": str(aligned_f),
                                  "aligner": {"model": "base.en"}},
                    "validation": {"status": "pass"}}

        p = []; make._validate_scene_aligned("s", scene, beats, entry(), p); assert p == [], p
        # each mutation -> at least one problem, no per-beat audio_file demanded. (Aligner
        # model is intentionally NOT checked by make.py -- it is tts.py's freshness job.)
        for mutate in (
            lambda e: e.update(scene_text_hash="STALE"),
            lambda e: e.update(audio_file="/nope.wav"),
            lambda e: e["alignment"].update(words_file="/nope.json"),
            lambda e: e.__setitem__("validation", {"status": "fail"}),
            lambda e: e["beats"][1].update(reveal="m.999"),
        ):
            e = entry(); mutate(e); p = []; make._validate_scene_aligned("s", scene, beats, e, p)
            assert p, "expected a freshness problem after mutation, got none"
        # aligner-model change must NOT be flagged by make.py (whatever produced the alignment renders)
        e = entry(); e["alignment"]["aligner"]["model"] = "small.en"
        p = []; make._validate_scene_aligned("s", scene, beats, e, p); assert p == [], p


if __name__ == "__main__":
    test_beat_durations_accepts_scene_aligned()
    test_schema_guard_rejects_future_schema()
    test_validate_scene_aligned_freshness()
    print("OK make scene_aligned self-test (Task 9)")
