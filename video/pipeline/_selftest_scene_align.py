"""Offline self-test for scene_align.py. Run: python video/pipeline/_selftest_scene_align.py
Needs no whisper model: every function under test consumes plain dicts/fixtures."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline import scene_align as SA  # noqa: E402


def test_tokenize_matches_word_re():
    # canonical tokenizer: hyphen/apostrophe compounds are one token, punctuation splits
    assert SA.tokenize("sum-to-product, cosine's") == ["sum-to", "product", "cosine's"]
    assert SA.tokenize("") == []


def test_build_scene_plan_token_ranges_and_transcript():
    scene = {"id": "s", "say": "A is true. {show m.0} Here is why. {show m.1} And so."}
    plan = SA.build_scene_plan(scene)
    # transcript = join of beat texts; scene_text_hash covers it
    assert plan["transcript"] == "A is true. Here is why. And so."
    assert plan["word_count"] == len(SA.tokenize(plan["transcript"]))
    beats = plan["beats"]
    assert [b["reveal"] for b in beats] == [None, "m.0", "m.1"]
    # contiguous, non-overlapping [word_start, word_end) covering the whole transcript
    assert beats[0]["word_start"] == 0
    for a, b in zip(beats, beats[1:]):
        assert a["word_end"] == b["word_start"]
    assert beats[-1]["word_end"] == plan["word_count"]
    # the transcript slice for each beat equals that beat's own tokenization (the invariant)
    toks = SA.tokenize(plan["transcript"])
    for b in beats:
        assert toks[b["word_start"]:b["word_end"]] == SA.tokenize(b["text"])
    # per-beat text_hash present (freshness), scene_text_hash present
    assert all(b["text_hash"] for b in beats)
    assert plan["scene_text_hash"]


def test_build_scene_plan_reveal_only_beat_has_zero_width_range():
    # a {show} with no following words -> reveal-only beat: contributes no tokens
    scene = {"id": "s", "say": "Look here. {show m.0}"}
    plan = SA.build_scene_plan(scene)
    assert plan["beats"][-1]["reveal"] == "m.0"
    assert plan["beats"][-1]["word_start"] == plan["beats"][-1]["word_end"]


def test_explode_splits_multitoken_words_by_char_share():
    # stable-ts follows transcript whitespace: "sum-to-product." is ONE aligner word;
    # WORD_RE gives ["sum-to", "product"]. Explode splits the span by character share.
    aligned = [{"text": "sum-to-product.", "start": 0.0, "end": 1.0, "probability": 0.9}]
    words, multi = SA.explode_to_plan_tokens(aligned)
    assert [w["word"] for w in words] == ["sum-to", "product"]
    assert words[0]["start"] == 0.0 and words[-1]["end"] == 1.0   # last token snaps to parent end
    assert words[0]["end"] == words[1]["start"]                   # contiguous
    assert 1 in multi and multi[1]["ordinal"] == 1 and multi[1]["tokens"] == 2


def test_explode_drops_punctuation_only_words():
    aligned = [{"text": "here", "start": 0.0, "end": 0.5, "probability": 0.9},
               {"text": "--", "start": 0.5, "end": 0.7, "probability": None},
               {"text": "there", "start": 0.7, "end": 1.0, "probability": 0.9}]
    words, multi = SA.explode_to_plan_tokens(aligned)
    assert [w["word"] for w in words] == ["here", "there"]   # "--" drops; its span is inter-word gap
    assert multi == {}


def test_verify_plan_index_raises_on_mismatch():
    plan = SA.build_scene_plan({"id": "s", "say": "alpha beta gamma."})
    ok = [{"word": w, "start": i, "end": i + 1, "probability": 0.9}
          for i, w in enumerate(["alpha", "beta", "gamma"])]
    SA.verify_plan_index(ok, plan)  # no raise
    bad = [{"word": w, "start": i, "end": i + 1, "probability": 0.9}
           for i, w in enumerate(["alpha", "GONE", "gamma"])]
    try:
        SA.verify_plan_index(bad, plan)
    except SA.AlignmentError as exc:
        assert "index 1" in str(exc)
    else:
        raise AssertionError("expected AlignmentError on token mismatch")


def test_map_to_beats_boundaries_and_shape():
    # 3 beats over 6 tokens [0,2)[2,4)[4,6); words linear at 1s each, audio=6.0s
    plan = SA.build_scene_plan({"id": "s", "say": "a b {show m.0} c d {show m.1} e f"})
    words = [{"word": w, "start": float(i), "end": float(i) + 0.9, "probability": 0.8}
             for i, w in enumerate(["a", "b", "c", "d", "e", "f"])]
    beats = SA.map_to_beats(plan, words, audio_seconds=6.0)
    # start = first-word onset of each beat; end = next beat start; last -> audio end
    assert [b["start_seconds"] for b in beats] == [0.0, 2.0, 4.0]
    assert [b["end_seconds"] for b in beats] == [2.0, 4.0, 6.0]
    assert [b["audio_seconds"] for b in beats] == [2.0, 2.0, 2.0]
    # beats[] shape shared with beats mode + word_start/word_end + boundary
    b0 = beats[0]
    assert set(b0) >= {"index", "id", "reveal", "text", "text_hash",
                       "audio_seconds", "start_seconds", "end_seconds",
                       "word_start", "word_end", "boundary"}
    assert beats[1]["boundary"]["prob"] == 0.8            # boundary word's probability
    assert beats[1]["boundary"]["interpolated"] is False  # not from a multi-token parent


def test_map_to_beats_leading_reveal_only_then_spoken_boundary_has_prob():
    # Consecutive {show} => a real leading reveal-only beat (word_start==word_end==0),
    # then a spoken beat that ALSO starts at word_start==0. parse_say drops only the
    # very first empty+no-reveal beat, so beat[0] here keeps reveal m.0 (0 words) and
    # beat[1] is spoken from word 0. (A single leading {show} would be dropped, which
    # is why the earlier draft's "{show m.0} hello world" tested the wrong thing.)
    plan = SA.build_scene_plan({"id": "s", "say": "{show m.0} {show m.1} hello world"})
    assert plan["beats"][0]["word_start"] == plan["beats"][0]["word_end"] == 0   # reveal-only
    assert plan["beats"][1]["word_start"] == 0                                    # spoken from word 0
    words = [{"word": "hello", "start": 0.3, "end": 0.8, "probability": 0.9},
             {"word": "world", "start": 0.8, "end": 1.2, "probability": 0.9}]
    beats = SA.map_to_beats(plan, words, audio_seconds=1.2)
    assert beats[0]["start_seconds"] == 0.0
    # beat[1] is a boundary beat starting at word 0 -> its boundary prob must be set
    # (0 <= word_start), so run_gates gate 3 can inspect it. 0<word_start would drop it.
    assert beats[1]["boundary"]["prob"] == 0.9


def test_map_to_beats_interpolated_boundary_flagged():
    # boundary token that came from a multi-token parent -> interpolated True
    plan = SA.build_scene_plan({"id": "s", "say": "sum-to {show m.0} product now"})
    # aligner emitted "sum-to-product" as ONE word; explode makes token 1 ("product") a boundary
    aligned = [{"text": "sum-to-product", "start": 0.0, "end": 1.0, "probability": 0.7},
               {"text": "now", "start": 1.0, "end": 1.4, "probability": 0.9}]
    words, multi = SA.explode_to_plan_tokens(aligned)
    beats = SA.map_to_beats(plan, words, audio_seconds=1.4, multi=multi)
    assert beats[1]["boundary"]["interpolated"] is True


def _linear_words(tokens, per=1.0, prob=0.9):
    return [{"word": t, "start": i * per, "end": i * per + per * 0.9, "probability": prob}
            for i, t in enumerate(tokens)]


def test_run_gates_pass_clean_scene():
    plan = SA.build_scene_plan({"id": "s", "say": "a b {show m.0} c d {show m.1} e f"})
    words = _linear_words(SA.tokenize(plan["transcript"]))
    beats = SA.map_to_beats(plan, words, audio_seconds=6.0)
    v = SA.run_gates(plan, words, beats, audio_seconds=6.0)
    assert v["status"] == "pass"


def test_run_gates_fail_nonmonotonic_timestamps():
    plan = SA.build_scene_plan({"id": "s", "say": "a b {show m.0} c d"})
    words = _linear_words(SA.tokenize(plan["transcript"]))
    words[2]["start"] = 0.1  # token 2 (beat 2 boundary) jumps back before token 1
    beats = SA.map_to_beats(plan, words, audio_seconds=4.0)
    v = SA.run_gates(plan, words, beats, audio_seconds=4.0)
    assert v["status"] == "fail"
    assert any("monotonic" in w.lower() for w in v["failures"])


def test_run_gates_fail_overlapping_word_timestamps():
    # design §5 row 3 is "non-monotonic OR overlapping". Starts stay ordered but a word
    # ends AFTER the next word starts -> overlap -> FAIL (aligner anomaly).
    plan = SA.build_scene_plan({"id": "s", "say": "a b {show m.0} c d"})
    words = _linear_words(SA.tokenize(plan["transcript"]))
    words[1]["end"] = words[2]["start"] + 0.5   # token 1 overruns token 2's onset
    beats = SA.map_to_beats(plan, words, audio_seconds=4.0)
    v = SA.run_gates(plan, words, beats, audio_seconds=4.0)
    assert v["status"] == "fail"
    assert any("overlap" in w.lower() for w in v["failures"])


def test_run_gates_tolerates_trailing_silence():
    # design §5: the char-share gate computes the LAST beat from "last word end,
    # excluding tail silence" -- trailing silence is deliberately NOT a fail gate.
    plan = SA.build_scene_plan({"id": "s", "say": "a b {show m.0} c d"})
    words = _linear_words(SA.tokenize(plan["transcript"]))   # speech ends ~3.6s
    beats = SA.map_to_beats(plan, words, audio_seconds=12.0)  # 8s+ of trailing silence
    v = SA.run_gates(plan, words, beats, audio_seconds=12.0)
    assert v["status"] in ("pass", "pass_with_warnings")     # not failed by tail silence


def test_run_gates_fail_low_boundary_probability():
    plan = SA.build_scene_plan({"id": "s", "say": "a b {show m.0} c d"})
    words = _linear_words(SA.tokenize(plan["transcript"]))
    words[2]["probability"] = 0.05  # beat-2 boundary word far below 0.15
    beats = SA.map_to_beats(plan, words, audio_seconds=4.0)
    v = SA.run_gates(plan, words, beats, audio_seconds=4.0)
    assert v["status"] == "fail"
    assert any("boundary" in w.lower() for w in v["failures"])


def test_run_gates_fail_large_interior_gap():
    plan = SA.build_scene_plan({"id": "s", "say": "a b {show m.0} c d"})
    words = _linear_words(SA.tokenize(plan["transcript"]))
    words[3]["start"] = words[2]["end"] + 3.0  # 3s hole not at a beat boundary
    words[3]["end"] = words[3]["start"] + 0.5
    beats = SA.map_to_beats(plan, words, audio_seconds=8.0)
    v = SA.run_gates(plan, words, beats, audio_seconds=8.0)
    assert v["status"] == "fail"
    assert any("gap" in w.lower() for w in v["failures"])


def test_run_gates_warn_only_interior_low_prob_run():
    plan = SA.build_scene_plan({"id": "s", "say": "a b c {show m.0} d e f"})
    words = _linear_words(SA.tokenize(plan["transcript"]))
    words[1]["probability"] = 0.2  # interior (not a boundary) low-prob run
    words[2]["probability"] = 0.2
    beats = SA.map_to_beats(plan, words, audio_seconds=6.0)
    v = SA.run_gates(plan, words, beats, audio_seconds=6.0)
    assert v["status"] == "pass_with_warnings"
    assert v["failures"] == []
    assert any("low-prob" in w.lower() for w in v["warnings"])


if __name__ == "__main__":
    test_tokenize_matches_word_re()
    test_build_scene_plan_token_ranges_and_transcript()
    test_build_scene_plan_reveal_only_beat_has_zero_width_range()
    test_explode_splits_multitoken_words_by_char_share()
    test_explode_drops_punctuation_only_words()
    test_verify_plan_index_raises_on_mismatch()
    test_map_to_beats_boundaries_and_shape()
    test_map_to_beats_leading_reveal_only_then_spoken_boundary_has_prob()
    test_map_to_beats_interpolated_boundary_flagged()
    test_run_gates_pass_clean_scene()
    test_run_gates_fail_nonmonotonic_timestamps()
    test_run_gates_fail_overlapping_word_timestamps()
    test_run_gates_tolerates_trailing_silence()
    test_run_gates_fail_low_boundary_probability()
    test_run_gates_fail_large_interior_gap()
    test_run_gates_warn_only_interior_low_prob_run()
    print("OK scene_align self-test (Tasks 1-4)")
