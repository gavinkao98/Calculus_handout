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


if __name__ == "__main__":
    test_tokenize_matches_word_re()
    test_build_scene_plan_token_ranges_and_transcript()
    test_build_scene_plan_reveal_only_beat_has_zero_width_range()
    test_explode_splits_multitoken_words_by_char_share()
    test_explode_drops_punctuation_only_words()
    test_verify_plan_index_raises_on_mismatch()
    print("OK scene_align self-test (Tasks 1-2)")
