"""Offline self-test for scene_align.py. Run: python video/pipeline/_selftest_scene_align.py
Needs no whisper model: every function under test consumes plain dicts/fixtures."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline import scene_align as SA  # noqa: E402
from pipeline import scene_fallback as FB  # noqa: E402


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


def test_qa_diff_info_when_fa_region_healthy():
    plan_tokens = "the quantity x plus one half h times sine".split()
    asr_tokens = "the quantity x plus sine".split()   # ASR dropped a cluster (>=3)
    # FA says that region is high-probability and no gate flagged it -> ASR artifact, INFO
    fa_probs = [0.9] * len(plan_tokens)
    res = SA.qa_diff(plan_tokens, asr_tokens, fa_probs, weak_spans=[])
    assert res["verdict"] == "info"
    assert res["clusters"]


def test_qa_diff_fail_on_deletion_over_fa_weakness():
    plan_tokens = "alpha beta gamma delta epsilon zeta".split()
    asr_tokens = "alpha zeta".split()                  # dropped 4-token cluster [1,5)
    fa_probs = [0.9, 0.1, 0.1, 0.1, 0.1, 0.9]          # FA weak exactly there
    res = SA.qa_diff(plan_tokens, asr_tokens, fa_probs, weak_spans=[])
    assert res["verdict"] == "fail"                    # local FA weakness inside the cluster


def test_qa_diff_insertion_uses_neighborhood_window():
    # ASR INSERTED tokens -> opcode span is empty on the plan side (i1==i2). Co-location
    # must look at a WINDOW around the insertion point, not the empty slice fa_probs[i1:i2].
    plan_tokens = "alpha beta gamma delta".split()
    asr_tokens = "alpha beta XXX YYY ZZZ gamma delta".split()   # 3-token insertion after "beta"
    fa_probs = [0.9, 0.1, 0.1, 0.9]                    # FA weak around the insertion point (idx ~2)
    res = SA.qa_diff(plan_tokens, asr_tokens, fa_probs, weak_spans=[], window=2)
    assert res["verdict"] == "fail"


def test_qa_diff_gate_weakness_must_be_colocated_not_global():
    # A weak span FAR from the diff cluster must NOT make the cluster fail (design §6:
    # "同區" = same region, local; the earlier draft's bool(gate_failures) was global).
    plan_tokens = "alpha beta gamma delta epsilon zeta eta theta".split()
    asr_tokens = "alpha beta gamma eta theta".split()            # drop 3-token cluster [3,6)
    fa_probs = [0.9] * len(plan_tokens)                          # FA healthy everywhere
    far = SA.qa_diff(plan_tokens, asr_tokens, fa_probs, weak_spans=[(0, 1)])   # weak span at token 0
    assert far["verdict"] == "info"                             # not co-located -> not fail
    near = SA.qa_diff(plan_tokens, asr_tokens, fa_probs, weak_spans=[(4, 5)])  # weak span in cluster
    assert near["verdict"] == "fail"


def test_qa_diff_ignores_small_clusters():
    plan_tokens = "alpha beta gamma".split()
    asr_tokens = "alpha gamma".split()                 # single-token drop (<3)
    res = SA.qa_diff(plan_tokens, asr_tokens, [0.9, 0.9, 0.9], weak_spans=[])
    assert res["verdict"] == "clean"


def test_build_scene_aligned_entry_shape():
    plan = SA.build_scene_plan({"id": "difference_quotient_for_sine",
                                "say": "a b {show m.0} c d {show m.1} e f"})
    words = _linear_words(SA.tokenize(plan["transcript"]))
    beats = SA.map_to_beats(plan, words, audio_seconds=6.0)
    gates = SA.run_gates(plan, words, beats, audio_seconds=6.0)
    entry = SA.build_scene_aligned_entry(
        scene_number=7, plan=plan, beats=beats, audio_seconds=6.0,
        audio_file="/x/scenes/07_difference_quotient_for_sine.wav",
        summary={"aligner": {"tool": "stable-ts", "version": "2.19.1", "model": "base.en",
                             "nonspeech_skip": 5.0, "failure_threshold": 0.2}},
        gates=gates,
        words_file="/x/align/07.words.json", aligned_file="/x/align/07.aligned.json")
    assert entry["narration_mode"] == "scene_aligned"
    assert entry["kind"] == "content"
    assert entry["scene_text_hash"] == plan["scene_text_hash"]
    assert entry["beat_count"] == len(beats) == len(entry["beats"])
    assert entry["audio_seconds"] == 6.0
    assert entry["alignment"]["aligner"]["tool"] == "stable-ts"
    assert entry["alignment"]["chunks"] is None
    assert entry["validation"]["status"] in ("pass", "pass_with_warnings")
    assert entry["fallback_history"] == []
    # script == space-join of beat texts (same field beats mode exposes to critic)
    assert entry["script"] == "a b c d e f"
    # no per-beat audio_file (beat WAVs do not exist in scene_aligned)
    assert all("audio_file" not in b for b in entry["beats"])
    # sum(beat durations) ~= audio_seconds (make.py asserts this)
    assert abs(sum(b["audio_seconds"] for b in entry["beats"]) - entry["audio_seconds"]) < 0.01


def test_fallback_ladder_stops_at_first_pass():
    calls = []
    def rung(name, status):
        def _f(ctx):
            calls.append(name)
            return {"status": status, "entry": {"narration_mode": "scene_aligned", "rung": name}}
        return _f
    # rung spec is (name, billed, callable): billedness is explicit up front (no name
    # convention, no self-report). arbiter is free; resynth/chunk billed; beats exempt.
    result = FB.run_ladder(
        scene_id="s",
        rungs=[("arbiter", False, rung("arbiter", "fail")),
               ("resynth", True, rung("resynth", "pass")),
               ("chunk", True, rung("chunk", "pass")),
               ("beats", False, rung("beats", "pass"))],
        budget=FB.RetryBudget(max_billed=2))
    assert calls == ["arbiter", "resynth"]           # stopped at first pass
    assert result["entry"]["rung"] == "resynth"
    assert [h["rung"] for h in result["history"]] == ["arbiter", "resynth"]


def test_fallback_ladder_budget_stops_before_overrun():
    def billed_fail(ctx):
        return {"status": "fail", "entry": None}
    def beats_ok(ctx):
        return {"status": "pass", "entry": {"narration_mode": "beats"}}
    result = FB.run_ladder(
        scene_id="s",
        rungs=[("resynth", True, billed_fail), ("chunk", True, billed_fail),
               ("beats", False, beats_ok)],      # beats is the always-allowed terminal
        budget=FB.RetryBudget(max_billed=1))     # only 1 billed retry allowed
    # resynth consumes the 1 billed retry and fails; chunk is billed but over budget -> skipped;
    # ladder falls straight to the beats terminal (budget-exempt, always runs).
    assert result["entry"]["narration_mode"] == "beats"
    assert any(h.get("skipped_over_budget") for h in result["history"])


def test_split_sentence_chunks():
    # multi-sentence -> one chunk per sentence, TILING the transcript's WORD_RE tokens
    t = "First point here. Second point now! Third and final?"
    chunks = SA.split_sentence_chunks(t)
    assert chunks == ["First point here.", "Second point now!", "Third and final?"]
    assert [tok for c in chunks for tok in SA.tokenize(c)] == SA.tokenize(t)   # tiling invariant
    # no interior break -> single chunk (rung then declines: nothing to gain over resynth)
    assert SA.split_sentence_chunks("just some words") == ["just some words"]
    assert SA.split_sentence_chunks("   ") == []
    # split points sit on whitespace, so an abbreviation over-splits but never cuts a token
    over = "Use e.g. this rule. Done."
    assert [tok for c in SA.split_sentence_chunks(over) for tok in SA.tokenize(c)] == SA.tokenize(over)


def _chunk_res(text, dur, prob):
    toks = SA.tokenize(text)
    step = dur / len(toks)
    words = [{"word": t, "start": round(i * step, 3), "end": round((i + 1) * step, 3),
              "probability": prob} for i, t in enumerate(toks)]
    return {"words": words, "multi": {}, "segments": [{"id": 0}],
            "summary": {"aligner": {"tool": "stable-ts", "version": "x", "model": "base.en"}}}


def test_merge_chunk_alignments():
    plan = SA.build_scene_plan({"id": "s", "say": "Look here now. {show g.0} Then we go."})
    chunk_texts = SA.split_sentence_chunks(plan["transcript"])
    assert chunk_texts == ["Look here now.", "Then we go."]
    merged = SA.merge_chunk_alignments(
        [_chunk_res("Look here now.", 1.5, 0.9), _chunk_res("Then we go.", 1.2, 0.8)],
        [1.5, 1.2], chunk_texts, plan)
    # merged word list reproduces the plan token order (merge asserts this internally too)
    assert [w["word"] for w in merged["words"]] == SA.tokenize(plan["transcript"])
    # chunk 1's words are offset by chunk 0's WAV duration (1.5s)
    tail = merged["words"][len(SA.tokenize("Look here now.")):]
    assert tail[0]["word"] == "Then" and abs(tail[0]["start"] - 1.5) < 1e-6
    # per-chunk metadata: contiguous token ranges tiling the transcript + durations + prob_min
    chunks = merged["chunks"]
    assert [c["word_start"] for c in chunks] == [0, 3]
    assert chunks[0]["word_end"] == chunks[1]["word_start"] == 3
    assert chunks[-1]["word_end"] == plan["word_count"]
    assert (chunks[0]["audio_seconds"], chunks[1]["audio_seconds"]) == (1.5, 1.2)
    assert chunks[0]["prob_min"] == 0.9
    # summary carries the sentence_chunk marker + aggregate stats (feeds entry assembly)
    assert merged["summary"]["aligner"]["mode"] == "sentence_chunk"
    assert merged["summary"]["word_count"] == plan["word_count"]
    # threads through map_to_beats + entry assembly with chunks populated
    beats = SA.map_to_beats(plan, merged["words"], 2.7, multi=merged["multi"])
    entry = SA.build_scene_aligned_entry(
        scene_number=1, plan=plan, beats=beats, audio_seconds=2.7, audio_file="/x.wav",
        summary=merged["summary"], gates={"status": "pass", "warnings": [], "metrics": {}},
        words_file="/w.json", aligned_file="/a.json", chunks=merged["chunks"])
    assert entry["alignment"]["chunks"] == merged["chunks"]


def test_merge_chunk_alignments_raises_on_token_break():
    # soundness gate: a chunk whose tokens don't reproduce the plan slice must raise, so a
    # broken chunk alignment can never be promoted as if it mapped cleanly.
    plan = SA.build_scene_plan({"id": "s", "say": "Look here. {show g.0} Then go."})
    chunk_texts = SA.split_sentence_chunks(plan["transcript"])
    bad = {"words": [{"word": "WRONG", "start": 0.0, "end": 0.5, "probability": 0.9}],
           "multi": {}, "segments": [], "summary": {"aligner": {}}}
    good = _chunk_res("Then go.", 0.6, 0.9)
    try:
        SA.merge_chunk_alignments([bad, good], [0.5, 0.6], chunk_texts, plan)
        assert False, "expected AlignmentError on token mismatch"
    except SA.AlignmentError:
        pass


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
    test_qa_diff_info_when_fa_region_healthy()
    test_qa_diff_fail_on_deletion_over_fa_weakness()
    test_qa_diff_insertion_uses_neighborhood_window()
    test_qa_diff_gate_weakness_must_be_colocated_not_global()
    test_qa_diff_ignores_small_clusters()
    test_build_scene_aligned_entry_shape()
    test_fallback_ladder_stops_at_first_pass()
    test_fallback_ladder_budget_stops_before_overrun()
    test_split_sentence_chunks()
    test_merge_chunk_alignments()
    test_merge_chunk_alignments_raises_on_token_break()
    print("OK scene_align self-test (Tasks 1-7 + batch-2 chunk rung)")
