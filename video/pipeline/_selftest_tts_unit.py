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


# ---- T2a: manifest status shape contract + preflight overwrite guard ----

def _write(p: Path, obj) -> None:
    p.write_text(json.dumps(obj), encoding="utf-8")


def test_read_manifest_status_shape_contract():   # R3-B1: 'ok' is a crash-safety promise
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "manifest.json"
        assert tts.read_manifest_status(Path(d) / "nope.json") == (None, "absent")
        corrupts = [
            {}, None, [],
            {"backend": 1, "scenes": []},                                       # backend not str
            {"backend": "m"},                                                   # no scenes
            {"backend": "m", "scenes": None},
            {"backend": "m", "scenes": [None]},
            {"backend": "m", "scenes": [{}]},                                   # no scene_id
            {"backend": "m", "scenes": [{"scene_id": ["x"]}]},                  # scene_id not str
            {"backend": "m", "scenes": [{"scene_id": "a", "beats": None}]},     # present-but-null
            {"backend": "m", "scenes": [{"scene_id": "a", "beats": [None]}]},
            {"backend": "m", "scenes": [{"scene_id": "a", "beats": [{"audio_file": 123}]}]},
            {"backend": "m", "scenes": [{"scene_id": "a", "narration_mode": "scene_aligned",
                                         "audio_seconds": "x"}]},               # audio_seconds not num
        ]
        for obj in corrupts:
            _write(p, obj)
            assert tts.read_manifest_status(p) == (None, "corrupt"), obj
        p.write_text('{"backend": "m", "scenes": [', encoding="utf-8")          # truncated JSON
        assert tts.read_manifest_status(p)[1] == "corrupt"
        oks = [
            {"backend": "m", "scenes": []},                                     # first run
            {"backend": "m", "scenes": [{"scene_id": "a",
                "beats": [{"audio_file": "x.wav", "text_hash": "h"}]}]},
            {"backend": "m", "scenes": [{"scene_id": "a",
                "narration_mode": "scene_aligned", "audio_seconds": 4.2}]},
            {"backend": "m", "scenes": [{"scene_id": "a",
                "narration_mode": "silent", "duration": 6.0}]},                 # silent, no beats
        ]
        for obj in oks:
            _write(p, obj)
            data, status = tts.read_manifest_status(p)
            assert status == "ok" and data == obj, obj


_BASE_ID = {"deck_id": "d", "backend": "mimo", "model": "m", "voice": "Dean", "style": "",
            "sample_rate": 24000, "channels": 1, "sample_width": 2, "output_dir": "/o"}


def test_overwrite_guard_states():
    with tempfile.TemporaryDirectory() as d:
        empty = Path(d) / "empty"; empty.mkdir()                    # no WAVs

        def guard(status, existing, intended, scene_sel="all", fbs=False, fc=False, output_dir=empty):
            return tts.overwrite_guard(status=status, existing=existing, intended=intended,
                                       scene_sel=scene_sel, output_dir=output_dir,
                                       force_backend_switch=fbs, force_clobber=fc)

        assert guard("ok", dict(_BASE_ID), dict(_BASE_ID)) is None            # clean identity match
        # corrupt -> abort unless --force-clobber AND --scene all
        assert guard("corrupt", None, dict(_BASE_ID)) is not None
        assert guard("corrupt", None, dict(_BASE_ID), scene_sel="b", fc=True) is not None
        assert guard("corrupt", None, dict(_BASE_ID), scene_sel="all", fc=True) is None
        # absent + WAVs present -> abort unless --force-clobber AND --scene all
        wavdir = Path(d) / "hasaudio"; (wavdir / "scenes").mkdir(parents=True)
        (wavdir / "scenes" / "a.wav").write_bytes(b"RIFF")
        assert guard("absent", None, dict(_BASE_ID), output_dir=wavdir) is not None
        assert guard("absent", None, dict(_BASE_ID), output_dir=wavdir, scene_sel="all", fc=True) is None
        # ok + voice differs + subset -> abort (subset can't merge into a different identity)
        assert guard("ok", dict(_BASE_ID), {**_BASE_ID, "voice": "Mia"}, scene_sel="a") is not None
        # ok + backend differs + --scene all -> needs --force-backend-switch
        assert guard("ok", dict(_BASE_ID), {**_BASE_ID, "backend": "mock"}, scene_sel="all", fbs=True) is None
        assert guard("ok", dict(_BASE_ID), {**_BASE_ID, "backend": "mock"}, scene_sel="all", fbs=False) is not None


def test_main_guard_blocks_before_synth():   # R3-A2: guard fires BEFORE any synth/write
    with tempfile.TemporaryDirectory() as d:
        outdir = Path(d) / "audio_mimo"; (outdir / "scenes").mkdir(parents=True)
        manifest = outdir / "manifest.json"
        sentinel = outdir / "scenes" / "07_sceneA.wav"
        _write(manifest, {**_BASE_ID, "backend": "mock", "voice": "Dean",
                          "scenes": [{"scene_id": "sceneA", "narration_mode": "scene_aligned",
                                      "audio_seconds": 4.0, "audio_file": str(sentinel)}]})
        sentinel.write_bytes(b"REAL-DEAN-AUDIO")
        before = sentinel.read_bytes()
        story = Path(d) / "deck.yml"       # meta.id NOT *_mimo -> freshness gate is a no-op here
        story.write_text("meta:\n  id: d\n  section: '9.9'\nscenes:\n"
                         "  - id: sceneA\n    kind: content\n    template: derivation\n    say: 'hi'\n",
                         encoding="utf-8")
        argv = ["tts.py", "--storyboard", str(story), "--backend", "mock", "--voice", "Mia",
                "--scene", "sceneA", "--reuse-existing", "--output-dir", str(outdir),
                "--manifest", str(manifest)]

        def _boom(*a, **k):
            raise AssertionError("build_backend must not run before the overwrite guard")

        real_bb, old_argv = tts.build_backend, sys.argv
        tts.build_backend = _boom
        try:
            sys.argv = argv
            try:
                tts.main()
                assert False, "expected the guard to abort the run"
            except SystemExit:
                pass
        finally:
            tts.build_backend, sys.argv = real_bb, old_argv
        assert sentinel.read_bytes() == before, "sentinel WAV must be untouched by an aborted run"


# ---- T2c: --scene subset merges into prior manifest (identity-checked) ----

def test_scene_subset_merges_into_prior_manifest():
    prior = {**_BASE_ID, "scenes": [{"scene_id": "a", "x": 1}, {"scene_id": "b", "x": 2}]}
    fresh = {**_BASE_ID, "scenes": [{"scene_id": "b", "x": 99}]}
    out = tts.merged_manifest(prior, fresh, ["a", "b", "c"])
    assert [e["scene_id"] for e in out["scenes"]] == ["a", "b"]        # order follows storyboard; c absent
    assert out["scenes"][0]["x"] == 1 and out["scenes"][1]["x"] == 99  # untouched a kept, b wins fresh
    assert tts.merged_manifest(None, fresh, ["b"]) is fresh            # no prior -> fresh as-is


def test_merge_refuses_identity_mismatch():
    prior = {**_BASE_ID, "scenes": [{"scene_id": "a", "x": 1}]}
    fresh = {**_BASE_ID, "voice": "Mia", "scenes": [{"scene_id": "b", "x": 2}]}   # voice differs
    try:
        tts.merged_manifest(prior, fresh, ["a", "b"])
        assert False, "should have raised"
    except SystemExit:
        pass


if __name__ == "__main__":
    test_unit_auto_allowlist_is_batch2()
    test_resolve_unit_for_scene()
    test_atomic_write_and_promote()
    test_scene_reuse_ok_freshness()
    test_read_manifest_status_shape_contract()
    test_overwrite_guard_states()
    test_main_guard_blocks_before_synth()
    test_scene_subset_merges_into_prior_manifest()
    test_merge_refuses_identity_mismatch()
    print("OK tts unit-routing self-test (Task 8)")
