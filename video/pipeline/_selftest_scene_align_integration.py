"""Offline end-to-end: tts.synthesize_scene scene path (stubbed aligner + synth) ->
schema-2 entry -> make.py reuse-validation + render-sync + ladder demotion. No API,
no whisper model, no ffmpeg. Run: python video/pipeline/_selftest_scene_align_integration.py"""
import argparse
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline import scene_align as SA           # noqa: E402
from pipeline import tts                          # noqa: E402
from pipeline.audio import write_pcm_wav, silence_pcm, wav_duration  # noqa: E402
import make                                       # noqa: E402

SCENE = {"id": "slope_equals_height", "kind": "content", "template": "graph",
         "say": "First point. {show g.0} Second point here now. {show g.1} Third and final point."}
META = {"id": "demo_mimo"}


def _args(**over):
    base = dict(backend="mock", model="mimo-v2.5-tts", voice="Dean", style="STY", unit="scene",
                skip_qa=True, aligner_model="base.en", aligner_device="cpu",
                fallback_budget=2, empty_beat_seconds=0.45, reuse_existing=False)
    base.update(over)
    return argparse.Namespace(**base)


def _fake_align(wav_path, plan, **kw):
    dur = wav_duration(wav_path)
    toks = SA.tokenize(plan["transcript"])
    step = dur / max(len(toks), 1)
    words = [{"word": t, "start": round(i * step, 3), "end": round(min((i + 1) * step, dur), 3),
              "probability": 0.85} for i, t in enumerate(toks)]
    summary = {"aligner": {"tool": "stable-ts", "version": "stub", "model": kw.get("model", "base.en"),
               "nonspeech_skip": 5.0, "failure_threshold": 0.2}, "word_count": len(words),
               "beat_boundary_in_multi_token_word": [], "prob_min": 0.85, "prob_mean": 0.85,
               "low_prob_words": 0, "low_prob_runs": []}
    return {"words": words, "summary": summary, "segments": [], "multi": {}}


def _fake_synth(seconds):
    def _f(backend, plan, out_path, voice, args):
        write_pcm_wav(out_path, silence_pcm(seconds))
    return _f


def _fake_synth_by_tokens(backend, plan, out_path, voice, args):
    # duration proportional to token count -> per-beat char-share stays ~1 (clean gates),
    # so the chunk-rescue test does not ride a char_share warn boundary.
    write_pcm_wav(out_path, silence_pcm(1.5 * max(len(SA.tokenize(plan["transcript"])), 1)))


def _fake_align_long_fails(wav_path, plan, **kw):
    # a long multi-sentence transcript aligns POORLY (low boundary prob -> gate fail); a
    # single sentence aligns well. This is exactly the premise of the sentence-chunk rung,
    # so it drives the ladder into chunk without any real model.
    prob = 0.05 if len(SA.split_sentence_chunks(plan["transcript"])) > 1 else 0.92
    dur = wav_duration(wav_path)
    toks = SA.tokenize(plan["transcript"])
    step = dur / max(len(toks), 1)
    words = [{"word": t, "start": round(i * step, 3), "end": round(min((i + 1) * step, dur), 3),
              "probability": prob} for i, t in enumerate(toks)]
    summary = {"aligner": {"tool": "stable-ts", "version": "stub", "model": kw.get("model", "base.en"),
               "nonspeech_skip": 5.0, "failure_threshold": 0.2}, "word_count": len(words),
               "beat_boundary_in_multi_token_word": [], "prob_min": prob, "prob_mean": prob,
               "low_prob_words": 0, "low_prob_runs": []}
    return {"words": words, "summary": summary, "segments": [], "multi": {}}


def test_tts_scene_path_and_make_consumers():
    saved = (SA.align_scene, tts._synth_scene_wav, make._probe_duration)
    SA.align_scene, tts._synth_scene_wav = _fake_align, _fake_synth(12.0)
    try:
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "audio_mimo"
            entry = tts.synthesize_scene(backend=tts.MockTTSBackend(0.45), meta=META, scene=SCENE,
                scene_number=7, output_dir=out, args=_args(), reuse_index={}, scene_reuse_index={})
            assert entry["narration_mode"] == "scene_aligned"
            assert entry["validation"]["status"] in ("pass", "pass_with_warnings")
            assert Path(entry["audio_file"]).exists()                        # WAV promoted
            assert not Path(entry["audio_file"] + ".tmp").exists()           # temp gone
            assert Path(entry["alignment"]["words_file"]).exists()
            assert Path(entry["alignment"]["aligned_file"]).exists()
            manifest = {"schema": 2, "deck_id": META["id"], "backend": "mimo", "model": "mimo-v2.5-tts",
                        "voice": "Dean", "style": "STY", "scenes": [entry]}
            make._check_manifest_schema(manifest)
            make._validate_reuse_manifest(META, [SCENE], manifest)           # raises if stale
            make._probe_duration = lambda p: 1.0 + entry["audio_seconds"] + 1.0
            assert make._audit_render_sync([SCENE], manifest,
                                           {SCENE["id"]: Path(entry["audio_file"])}, lead=1.0) is True
    finally:
        SA.align_scene, tts._synth_scene_wav, make._probe_duration = saved


def test_gate_fail_demotes_to_beats():
    saved = (SA.align_scene, tts._synth_scene_wav, SA.run_gates)
    SA.align_scene, tts._synth_scene_wav = _fake_align, _fake_synth(12.0)
    SA.run_gates = lambda *a, **k: {"status": "fail", "failures": ["forced"], "warnings": [], "metrics": {}}
    try:
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "audio_mimo"
            # budget 0: resynth skipped over budget; arbiter (free, also fails) -> beats terminal
            entry = tts.synthesize_scene(backend=tts.MockTTSBackend(0.45), meta=META, scene=SCENE,
                scene_number=7, output_dir=out, args=_args(fallback_budget=0),
                reuse_index={}, scene_reuse_index={})
            assert entry["narration_mode"] == "beats"
            assert any(h.get("rung") == "beats" for h in entry.get("fallback_history", []))
    finally:
        SA.align_scene, tts._synth_scene_wav, SA.run_gates = saved


def test_alignment_error_demotes_to_beats_not_crash():
    # a raising aligner (stable-ts abort / token break) must NOT crash the deck: the
    # scene routes through the ladder to the beats terminal (design: always shippable).
    def _raises(wav_path, plan, **kw):
        raise SA.AlignmentError("simulated stable-ts abort")
    saved = (SA.align_scene, tts._synth_scene_wav)
    SA.align_scene, tts._synth_scene_wav = _raises, _fake_synth(12.0)
    try:
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "audio_mimo"
            entry = tts.synthesize_scene(backend=tts.MockTTSBackend(0.45), meta=META, scene=SCENE,
                scene_number=7, output_dir=out, args=_args(), reuse_index={}, scene_reuse_index={})
            assert entry["narration_mode"] == "beats"   # demoted, not crashed
    finally:
        SA.align_scene, tts._synth_scene_wav = saved


def test_build_fallback_rungs_has_chunk():
    # the ladder wires the sentence-chunk rung between resynth and the beats terminal,
    # declared billed so run_ladder's budget gate applies to it.
    import tempfile as _tf
    with _tf.TemporaryDirectory() as d:
        rungs = tts._build_fallback_rungs(tts.MockTTSBackend(0.45), META, SCENE, 7,
                                          Path(d) / "audio_mimo", _args(),
                                          SA.build_scene_plan(SCENE), reuse_index={})
    names = [n for n, _b, _f in rungs]
    billed = {n: b for n, b, _f in rungs}
    assert names == ["arbiter", "resynth", "chunk", "beats"]
    # chunk is declared NOT billed to run_ladder: it fans out to N sub-synths and self-accounts
    # (reserves N budget units, declines if over) rather than being single-counted (Codex R-item2).
    assert billed["resynth"] is True and billed["chunk"] is False and billed["beats"] is False


def test_chunk_rung_rescues_when_full_scene_fails():
    # primary + resynth align the FULL transcript (fails); the chunk rung re-synths per
    # sentence (each aligns cleanly), concats + merges -> scene_aligned with chunks set.
    # budget=4 covers the fan-out (1 resynth + 3 chunk sub-synths); see the decline test below.
    saved = (SA.align_scene, tts._synth_scene_wav)
    SA.align_scene, tts._synth_scene_wav = _fake_align_long_fails, _fake_synth_by_tokens
    try:
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "audio_mimo"
            entry = tts.synthesize_scene(backend=tts.MockTTSBackend(0.45), meta=META, scene=SCENE,
                scene_number=7, output_dir=out, args=_args(fallback_budget=4),
                reuse_index={}, scene_reuse_index={})
            assert entry["narration_mode"] == "scene_aligned"
            assert entry["validation"]["status"] in ("pass", "pass_with_warnings")
            chunks = entry["alignment"]["chunks"]
            assert chunks is not None and len(chunks) == 3            # three sentences
            rungs = [h.get("rung") for h in entry.get("fallback_history", [])]
            assert rungs[:3] == ["arbiter", "resynth", "chunk"]       # arbiter/resynth fail -> chunk
            assert Path(entry["audio_file"]).exists()                 # chunk-concat promoted
            assert not Path(str(entry["audio_file"]) + ".chunk.tmp").exists()   # temp cleaned
    finally:
        SA.align_scene, tts._synth_scene_wav = saved


def test_chunk_declines_over_budget_demotes_to_beats():
    # a multi-sentence scene needs N chunk sub-synths; under the default budget (2, minus the
    # resynth's 1) that fan-out does not fit, so chunk DECLINES and the scene demotes to beats
    # -- the budget bounds real billed calls rather than being bypassed (Codex R-item2 blocking 1).
    saved = (SA.align_scene, tts._synth_scene_wav)
    SA.align_scene, tts._synth_scene_wav = _fake_align_long_fails, _fake_synth_by_tokens
    try:
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "audio_mimo"
            entry = tts.synthesize_scene(backend=tts.MockTTSBackend(0.45), meta=META, scene=SCENE,
                scene_number=7, output_dir=out, args=_args(fallback_budget=2),
                reuse_index={}, scene_reuse_index={})
            assert entry["narration_mode"] == "beats"                 # chunk declined -> beats terminal
            reasons = " | ".join(h.get("reason") or "" for h in entry.get("fallback_history", []))
            assert "chunk declined" in reasons                        # the budget guard fired
            # decline path synthesizes nothing, so no chunk temp dir is left behind
            assert not list((out / "scenes").glob("*.chunks")) if (out / "scenes").exists() else True
    finally:
        SA.align_scene, tts._synth_scene_wav = saved


def test_chunk_generic_error_demotes_to_beats_not_crash():
    # a non-AlignmentError during a chunk sub-synth (e.g. a transient HTTPError) must NOT crash
    # the deck: the chunk rung catches broadly and demotes to the beats terminal, cleaning its
    # temps on the way out (Codex R-item2 blocking 2 + advisory 1).
    def _synth_boom(backend, plan, out_path, voice, args):
        # full-scene synths (primary/resynth) succeed; a single-sentence chunk sub-synth blows up
        if len(SA.split_sentence_chunks(plan["transcript"])) < 2:
            raise RuntimeError("simulated transient synth error")
        write_pcm_wav(out_path, silence_pcm(1.5 * max(len(SA.tokenize(plan["transcript"])), 1)))
    saved = (SA.align_scene, tts._synth_scene_wav)
    SA.align_scene, tts._synth_scene_wav = _fake_align_long_fails, _synth_boom
    try:
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "audio_mimo"
            entry = tts.synthesize_scene(backend=tts.MockTTSBackend(0.45), meta=META, scene=SCENE,
                scene_number=7, output_dir=out, args=_args(fallback_budget=4),
                reuse_index={}, scene_reuse_index={})
            assert entry["narration_mode"] == "beats"                 # demoted, not crashed
            reasons = " | ".join(h.get("reason") or "" for h in entry.get("fallback_history", []))
            assert "chunk failed" in reasons
            assert not list((out / "scenes").glob("*.chunks")) if (out / "scenes").exists() else True
    finally:
        SA.align_scene, tts._synth_scene_wav = saved


if __name__ == "__main__":
    test_tts_scene_path_and_make_consumers()
    test_gate_fail_demotes_to_beats()
    test_alignment_error_demotes_to_beats_not_crash()
    test_build_fallback_rungs_has_chunk()
    test_chunk_rung_rescues_when_full_scene_fails()
    test_chunk_declines_over_budget_demotes_to_beats()
    test_chunk_generic_error_demotes_to_beats_not_crash()
    print("OK scene_align integration self-test (Task 11 + batch-2 chunk rung)")
