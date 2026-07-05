"""Offline self-test for tts.py scene-unit routing (no API, no model).
Run: python video/pipeline/_selftest_tts_unit.py"""
import argparse
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline import tts  # noqa: E402

SCENE_ALLOWLIST = tts.SCENE_UNIT_TEMPLATES


def test_unit_auto_allowlist_is_batch2():
    # batch-2 (2026-07-06): the full content-template set goes scene under --unit auto
    # (first real deck: derivation 6/6 + theorem_proof 3/5 scene-aligned; FA failures safe-demote)
    assert {"definition_math", "graph", "callout", "recap_cards",
            "derivation", "theorem_proof"} <= SCENE_ALLOWLIST


def test_resolve_unit_for_scene():
    assert tts.resolve_unit("beat", {"template": "graph"}) == "beat"
    assert tts.resolve_unit("scene", {"template": "derivation"}) == "scene"       # explicit override
    assert tts.resolve_unit("auto", {"template": "graph"}) == "scene"
    assert tts.resolve_unit("auto", {"template": "derivation"}) == "scene"        # batch-2: now scene
    assert tts.resolve_unit("auto", {"template": "theorem_proof"}) == "scene"     # batch-2: now scene
    assert tts.resolve_unit("auto", {"template": "unknown_xyz"}) == "beat"        # unknown template -> beat
    assert tts.resolve_unit("auto", {}) == "beat"                                 # no template -> beat


def test_atomic_write_and_promote():
    from pipeline import atomicio
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        p = tmp / "sub" / "x.json"
        atomicio.atomic_write_json(p, {"a": 1})
        assert p.exists() and not p.with_name(p.name + ".tmp").exists()   # tmp cleaned by os.replace
        assert json.loads(p.read_text(encoding="utf-8"))["a"] == 1
        src = tmp / "y.tmp"; src.write_text("hi", encoding="utf-8")
        atomicio.promote(src, tmp / "y.txt")
        assert (tmp / "y.txt").read_text(encoding="utf-8") == "hi" and not src.exists()


def test_scene_reuse_ok_freshness():
    from pipeline.audio import write_pcm_wav, silence_pcm, wav_duration
    from pipeline import scene_align as SA
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        plan = SA.build_scene_plan({"id": "s", "say": "a b {show m.0} c d"})
        wav = tmp / "07_s.wav"
        write_pcm_wav(wav, silence_pcm(4.0))
        args = argparse.Namespace(model="mimo-v2.5-tts", style="STY", aligner_model="base.en", voice="Dean")
        prior = {"backend": "mimo", "model": "mimo-v2.5-tts", "voice": "Dean", "style": "STY",
                 "scene_text_hash": plan["scene_text_hash"], "audio_file": str(wav),
                 "audio_seconds": round(wav_duration(wav), 3)}
        assert tts.scene_reuse_ok(prior, plan, wav, backend_name="mimo", voice="Dean", args=args) is True
        # each WAV-affecting field, mutated, flips the verdict to False:
        assert tts.scene_reuse_ok({**prior, "scene_text_hash": "X"}, plan, wav, backend_name="mimo", voice="Dean", args=args) is False
        assert tts.scene_reuse_ok({**prior, "voice": "Mia"}, plan, wav, backend_name="mimo", voice="Dean", args=args) is False
        assert tts.scene_reuse_ok(None, plan, wav, backend_name="mimo", voice="Dean", args=args) is False
        # aligner-model change does NOT force resynth (§3: reuse WAV, re-align only) -> still True
        assert tts.scene_reuse_ok(prior, plan, wav, backend_name="mimo", voice="Dean",
                                  args=argparse.Namespace(**{**vars(args), "aligner_model": "small.en"})) is True


if __name__ == "__main__":
    test_unit_auto_allowlist_is_batch2()
    test_resolve_unit_for_scene()
    test_atomic_write_and_promote()
    test_scene_reuse_ok_freshness()
    print("OK tts unit-routing self-test (Task 8)")
