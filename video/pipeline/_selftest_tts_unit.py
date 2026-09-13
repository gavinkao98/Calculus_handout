"""Offline self-test for tts.py scene-unit routing (no API, no model).
Run: python video/pipeline/_selftest_tts_unit.py"""
import argparse
import io
import json
import sys
import tempfile
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline import tts  # noqa: E402
from pipeline.template_names import CONTENT_TEMPLATES  # noqa: E402

SCENE_ALLOWLIST = tts.SCENE_UNIT_TEMPLATES


def test_unit_auto_matches_content_templates():
    # --unit auto routes EVERY content template to scene; the allowlist derives from the
    # single manim-free source (template_names.py) so it can't drift from the registry (F10).
    assert SCENE_ALLOWLIST == set(CONTENT_TEMPLATES)


def test_resolve_unit_for_scene():
    assert tts.resolve_unit("beat", {"template": "graph"}) == "beat"
    assert tts.resolve_unit("scene", {"template": "derivation"}) == "scene"       # explicit override
    assert tts.resolve_unit("auto", {"template": "graph"}) == "scene"
    assert tts.resolve_unit("auto", {"template": "derivation"}) == "scene"        # batch-2: now scene
    assert tts.resolve_unit("auto", {"template": "theorem_proof"}) == "scene"     # batch-2: now scene
    assert tts.resolve_unit("auto", {"template": "procedure_steps"}) == "scene"   # T3: was missing from allowlist
    assert tts.resolve_unit("auto", {"template": "value_table"}) == "scene"       # T3: was missing
    assert tts.resolve_unit("auto", {"template": "sign_chart"}) == "scene"        # T3: was missing
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


# ---- tts-reuse-key: beat reuse is keyed by CONTENT, not by the output path ----
#
# Both 2026-09-13 re-bills were path-key misses with nothing to do with what is spoken:
# (a) a scene moved (derivative_of_cosine 16 -> 17), shifting `beats/<NN>_<id>/`, and
# (b) a {show} marker was added, renaming the beat file and renumbering its successors.
# Either way every beat missed the index and the whole scene was re-synthesized.

def _prior_beats_manifest(beat_dir: Path, texts, *, names=None, scene_id="sceneA",
                          seconds=1.5, **identity):
    """Write one WAV per text under `beat_dir` and return the prior manifest that
    describes them (beats mode)."""
    from pipeline.audio import write_pcm_wav, silence_pcm
    beat_dir.mkdir(parents=True, exist_ok=True)
    names = names or [f"old_reveal_{i}" for i in range(1, len(texts) + 1)]
    beats = []
    for i, (text, name) in enumerate(zip(texts, names), start=1):
        wav = beat_dir / f"{i:02d}_{name}.wav"
        write_pcm_wav(wav, silence_pcm(seconds))
        beats.append({"index": i, "id": f"beat_{i:02d}", "text": text,
                      "audio_file": str(wav), "text_hash": tts.text_hash(text)})
    return {"backend": "mock", "model": "m", "voice": "Dean", "style": "", **identity,
            "scenes": [{"scene_id": scene_id, "scene_number": 3,
                        "narration_mode": "beats", "beats": beats}]}


def _reuse_beat(index, request_text, new_wav, *, occurrence=0, scene_id="sceneA",
                voice="Dean", model="m"):
    """Drive synthesize_beat for one beat against `index`; return (backend, SynthesizedBeat,
    captured stdout)."""
    backend = tts.MockTTSBackend(0.4)
    buf = io.StringIO()
    with redirect_stdout(buf):
        synth = tts.synthesize_beat(
            backend,
            tts.TTSRequest(text=request_text, model=model, voice=voice, style=""),
            new_wav, reuse_existing=True, empty_seconds=0.4, backend_name="mock",
            reuse_index=index,
            reuse_key=(scene_id, tts.text_hash(request_text), occurrence))
    return backend, synth, buf.getvalue()


def test_beat_reuse_survives_a_moved_scene_and_a_renamed_reveal():
    """(a) Same scene, same words, brand-new path (scene 03 -> 04 AND the reveal renamed):
    reuse must still hit, and the WAV must be MOVED onto the path the current deck wants."""
    with tempfile.TemporaryDirectory() as d:
        out = Path(d)
        prior = _prior_beats_manifest(out / "beats" / "03_sceneA", ["hello world"])
        old_wav = Path(prior["scenes"][0]["beats"][0]["audio_file"])
        index = tts.build_reuse_index(prior)
        new_wav = out / "beats" / "04_sceneA" / "01_renamed_reveal.wav"
        backend, synth, log = _reuse_beat(index, "hello world", new_wav)
        assert backend.stats["calls"] == 0, "a word-for-word identical beat must not be re-synthesized"
        assert new_wav.exists(), "the reused WAV must be put where the current deck wants it"
        assert not old_wav.exists(), "the stale path must not linger as unmanaged audio"
        assert not old_wav.parent.exists(), "the emptied scene-number directory is pruned"
        assert abs(synth.duration - 1.5) < 0.05, "the reused duration is the WAV's, not an estimate"
        assert "reused" in log and "moved from" in log, log


def test_beat_reuse_hits_in_place_without_moving_anything():
    """The ordinary case (nothing moved) still reuses, and says nothing about moving."""
    with tempfile.TemporaryDirectory() as d:
        out = Path(d)
        prior = _prior_beats_manifest(out / "beats" / "03_sceneA", ["hello world"])
        same_wav = Path(prior["scenes"][0]["beats"][0]["audio_file"])
        backend, _, log = _reuse_beat(tts.build_reuse_index(prior), "hello world", same_wav)
        assert backend.stats["calls"] == 0 and same_wav.exists()
        assert "moved from" not in log, log


def test_beat_reuse_refuses_when_the_text_changed():
    """(b) The counterpart guarantee: content-addressing must not make a CHANGED beat
    reusable just because it lands on a path some prior beat owned."""
    with tempfile.TemporaryDirectory() as d:
        out = Path(d)
        prior = _prior_beats_manifest(out / "beats" / "03_sceneA", ["hello world"])
        index = tts.build_reuse_index(prior)
        new_wav = out / "beats" / "03_sceneA" / "01_old_reveal_1.wav"
        backend, _, log = _reuse_beat(index, "hello there", new_wav)
        assert backend.stats["calls"] == 1, "a beat whose words changed must be re-synthesized"
        assert "not reusing" in log and "text changed" in log, log


def test_beat_reuse_refuses_on_identity_and_missing_audio():
    """Voice/model/style are still part of the key, and a prior entry whose WAV is gone
    is not a hit (the index describes a manifest, the WAV is the thing being reused)."""
    with tempfile.TemporaryDirectory() as d:
        out = Path(d)
        prior = _prior_beats_manifest(out / "beats" / "03_sceneA", ["hello world"])
        index = tts.build_reuse_index(prior)
        req = tts.TTSRequest(text="hello world", model="m", voice="Mia", style="")
        key = ("sceneA", tts.text_hash("hello world"), 0)
        src, reason = tts.reusable_existing_beat(req, backend_name="mock",
                                                 reuse_index=index, key=key)
        assert src is None and reason == "voice changed"
        Path(prior["scenes"][0]["beats"][0]["audio_file"]).unlink()
        src, reason = tts.reusable_existing_beat(
            tts.TTSRequest(text="hello world", model="m", voice="Dean", style=""),
            backend_name="mock", reuse_index=index, key=key)
        assert src is None and reason.startswith("prior WAV is gone"), reason


def test_two_beats_with_identical_text_pair_off_by_index():
    """Rare but real: the same sentence twice in one scene. Each prior take is handed out
    once, in index order -- never the same WAV registered under two beats."""
    with tempfile.TemporaryDirectory() as d:
        out = Path(d)
        prior = _prior_beats_manifest(out / "beats" / "03_sceneA", ["same words", "same words"])
        first, second = (Path(b["audio_file"]) for b in prior["scenes"][0]["beats"])
        index = tts.build_reuse_index(prior)
        assert len(index) == 2, "identical text must not collapse to one index entry"
        new_a = out / "beats" / "04_sceneA" / "01_a.wav"
        new_b = out / "beats" / "04_sceneA" / "02_b.wav"
        backend_a, _, _ = _reuse_beat(index, "same words", new_a, occurrence=0)
        backend_b, _, _ = _reuse_beat(index, "same words", new_b, occurrence=1)
        assert backend_a.stats["calls"] == 0 and backend_b.stats["calls"] == 0
        assert new_a.exists() and new_b.exists() and not first.exists() and not second.exists()
        assert index == {}, "each prior take is consumed exactly once"


# ---- tts-reuse-key: the SCENE path gets the same treatment (scene WAV + align sidecars) ----
#
# Keying build_scene_reuse_index by scene_id was always right about WHICH audio belongs to a
# scene; what re-billed was that scene_reuse_ok was handed TODAY's path, while the WAV sits at
# `scenes/<old scene_number>_<scene_id>.wav`. A reordered deck therefore found nothing and
# re-synthesized a scene whose words never changed -- the beat bug, one level up.

_MOVED_SCENE = {"id": "sceneA", "kind": "content", "template": "derivation",
                "say": "a b {show m.0} c d"}


def _prior_scene_aligned(out: Path, number: int):
    """Lay down one scene_aligned scene's artifacts at `number` and return
    (prior manifest, plan, {audio_file/words_file/aligned_file: Path})."""
    from pipeline.audio import silence_pcm, wav_duration, write_pcm_wav
    from pipeline import scene_align as SA
    (out / "scenes").mkdir(parents=True, exist_ok=True)
    (out / "align").mkdir(parents=True, exist_ok=True)
    paths = {"audio_file": out / "scenes" / f"{number:02d}_sceneA.wav",
             "words_file": out / "align" / f"{number:02d}_sceneA.words.json",
             "aligned_file": out / "align" / f"{number:02d}_sceneA.aligned.json"}
    write_pcm_wav(paths["audio_file"], silence_pcm(4.0))
    paths["words_file"].write_text("{}", encoding="utf-8")
    paths["aligned_file"].write_text("{}", encoding="utf-8")
    plan = SA.build_scene_plan(_MOVED_SCENE)
    prior = {"backend": "mock", "model": "m", "voice": "Dean", "style": "", "scenes": [{
        "scene_id": "sceneA", "scene_number": number, "narration_mode": "scene_aligned",
        "scene_text_hash": plan["scene_text_hash"],
        "audio_file": str(paths["audio_file"]),
        "audio_seconds": round(wav_duration(paths["audio_file"]), 3),
        "alignment": {"words_file": str(paths["words_file"]),
                      "aligned_file": str(paths["aligned_file"])}}]}
    return prior, plan, paths


def _scene_args(**over):
    return argparse.Namespace(**{"model": "m", "style": "", "voice": "Dean",
                                 "aligner_model": "base.en", "aligner_device": "cpu",
                                 "skip_qa": True, "unit": "auto", "fallback_budget": 2,
                                 "empty_beat_seconds": 0.4, "reuse_existing": True, **over})


def test_scene_aligned_reuse_relocates_a_moved_scene_then_hits():
    """The deck moved sceneA 20 -> 14. Nothing was said differently, so the prior WAV and
    both align sidecars must be MOVED onto 14 and the freshness check must then pass."""
    with tempfile.TemporaryDirectory() as d:
        out = Path(d)
        prior, plan, old = _prior_scene_aligned(out, 20)
        index = tts.build_scene_reuse_index(prior)
        assert index["sceneA"]["words_file"] == str(old["words_file"]), "sidecars are indexed"
        args = _scene_args()
        new = {"audio_file": out / "scenes" / "14_sceneA.wav",
               "words_file": out / "align" / "14_sceneA.words.json",
               "aligned_file": out / "align" / "14_sceneA.aligned.json"}
        # the miss this commit removes: the WAV is at 20_, the check is asked about 14_
        assert tts.scene_reuse_ok(index["sceneA"], plan, new["audio_file"],
                                  backend_name="mock", voice="Dean", args=args) is False
        adopted, moved_from = tts.adopt_prior_scene_artifacts(
            index["sceneA"], scene_wav=new["audio_file"], words_file=new["words_file"],
            aligned_file=new["aligned_file"])
        assert moved_from == str(old["audio_file"])
        for key in new:
            assert new[key].exists(), key
            assert not old[key].exists(), f"{key} must be moved, not copied"
            assert adopted[key] == str(new[key])
        assert tts.scene_reuse_ok(adopted, plan, new["audio_file"],
                                  backend_name="mock", voice="Dean", args=args) is True
        # already in place -> nothing to move, and the verdict is unchanged
        again, moved_again = tts.adopt_prior_scene_artifacts(
            adopted, scene_wav=new["audio_file"], words_file=new["words_file"],
            aligned_file=new["aligned_file"])
        assert moved_again is None and again == adopted


def test_synthesize_scene_aligned_reuses_a_moved_scene_with_zero_backend_calls():
    """The seam above, wired into the scene path: a reordered deck must cost NOTHING.
    _align_and_gate is stubbed (it needs a whisper model); what is under test is that TTS
    is skipped and that the re-align is pointed at the relocated WAV."""
    with tempfile.TemporaryDirectory() as d:
        out = Path(d)
        prior, _, old = _prior_scene_aligned(out, 20)
        index = tts.build_scene_reuse_index(prior)
        backend = tts.MockTTSBackend(0.4)
        seen = {}

        def fake_align_and_gate(plan_, wav, scene_number, words_file, aligned_file, args_,
                                *, audio_file, promote_from, aligner_model=None):
            seen.update(wav=Path(wav), promote_from=promote_from, number=scene_number)
            return {"scene_id": plan_["scene_id"], "narration_mode": "scene_aligned",
                    "audio_file": str(audio_file), "scene_number": scene_number,
                    "validation": {"status": "pass", "warnings": [], "metrics": {}},
                    "fallback_history": []}

        saved, buf = tts._align_and_gate, io.StringIO()
        tts._align_and_gate = fake_align_and_gate
        try:
            with redirect_stdout(buf):
                entry = tts._synthesize_scene_aligned(
                    backend=backend, meta={}, scene=_MOVED_SCENE, scene_number=14,
                    output_dir=out, args=_scene_args(), reuse_index={},
                    scene_reuse_index=index)
        finally:
            tts._align_and_gate = saved
        assert backend.stats["calls"] == 0, "a reordered scene must not be re-synthesized"
        assert entry["validation"]["status"] == "pass"
        assert seen["wav"] == out / "scenes" / "14_sceneA.wav", seen["wav"]
        assert seen["promote_from"] is None, "reuse re-aligns in place; nothing to promote"
        assert not old["audio_file"].exists(), "the stale-numbered WAV must not linger"
        log = buf.getvalue()
        assert "reused 14_sceneA.wav" in log and "moved from" in log, log


def test_scene_aligned_relocates_even_when_the_text_changed():
    """Relocation is unconditional: the moved WAV is what a failed re-synth falls back on
    (promotion only happens after gates pass), and leaving it under the old number would
    strand an orphan WAV. The verdict must still be "not reusable"."""
    with tempfile.TemporaryDirectory() as d:
        out = Path(d)
        prior, plan, old = _prior_scene_aligned(out, 20)
        index = tts.build_scene_reuse_index(prior)
        index["sceneA"]["scene_text_hash"] = "SOMETHING-ELSE"      # the words changed
        new_wav = out / "scenes" / "14_sceneA.wav"
        adopted, moved_from = tts.adopt_prior_scene_artifacts(
            index["sceneA"], scene_wav=new_wav,
            words_file=out / "align" / "14_sceneA.words.json",
            aligned_file=out / "align" / "14_sceneA.aligned.json")
        assert moved_from == str(old["audio_file"]) and new_wav.exists()
        assert tts.scene_reuse_ok(adopted, plan, new_wav, backend_name="mock",
                                  voice="Dean", args=_scene_args()) is False


def test_adopt_prior_scene_artifacts_tolerates_a_missing_alignment_block():
    """A scene_aligned entry with no alignment block (or null paths) must not crash:
    read_manifest_status type-checks the fields its consumers dereference, and the
    alignment block is not among them."""
    with tempfile.TemporaryDirectory() as d:
        out = Path(d)
        assert tts.adopt_prior_scene_artifacts(None, scene_wav=out / "a.wav",
                                               words_file=out / "w", aligned_file=out / "a") \
            == (None, None)
        prior, _, old = _prior_scene_aligned(out, 20)
        prior["scenes"][0].pop("alignment")
        index = tts.build_scene_reuse_index(prior)
        assert index["sceneA"]["words_file"] is None
        adopted, moved_from = tts.adopt_prior_scene_artifacts(
            index["sceneA"], scene_wav=out / "scenes" / "14_sceneA.wav",
            words_file=out / "align" / "14_sceneA.words.json",
            aligned_file=out / "align" / "14_sceneA.aligned.json")
        assert moved_from == str(old["audio_file"])
        assert adopted["words_file"] is None and adopted["aligned_file"] is None


# ---- tts-reuse-key: a subset merge re-stamps scene_number from the current storyboard ----

def test_renumber_scenes_restamps_from_the_current_storyboard_order():
    """(c) 2026-09-13: a --scene subset merge left derivative_of_cosine and
    slope_equals_height BOTH numbered 17, because carried-over prior entries keep whatever
    number the deck had when they were last synthesized. Numbers now come from today's
    full-deck order (intro/divider take a number too -- same counting as critic.py)."""
    from pipeline.audio import write_pcm_wav, silence_pcm
    with tempfile.TemporaryDirectory() as d:
        out = Path(d)
        (out / "scenes").mkdir()
        (out / "align").mkdir()
        stale_wav = out / "scenes" / "17_slope.wav"
        write_pcm_wav(stale_wav, silence_pcm(1.0))
        stale_words = out / "align" / "17_slope.words.json"
        stale_words.write_text("{}", encoding="utf-8")
        stale_beat = out / "beats" / "17_slope" / "01_x.wav"
        stale_beat.parent.mkdir(parents=True)
        write_pcm_wav(stale_beat, silence_pcm(1.0))
        prior_entry = {"scene_id": "slope", "scene_number": 17, "narration_mode": "beats",
                       "audio_file": str(stale_wav), "beats": [{"audio_file": str(stale_beat)}],
                       "alignment": {"words_file": str(stale_words), "aligned_file": None}}
        fresh_entry = {"scene_id": "cosine", "scene_number": 17}       # freshly synthesized
        merged = tts.merged_manifest({**_BASE_ID, "scenes": [prior_entry]},
                                     {**_BASE_ID, "scenes": [fresh_entry]},
                                     ["intro", "divider", "cosine", "slope"])
        assert [e["scene_number"] for e in merged["scenes"]] == [17, 17]   # the bug, pre-fix
        out_manifest = tts.renumber_scenes(
            merged, {sid: i for i, sid in enumerate(["intro", "divider", "cosine", "slope"], 1)})
        numbers = [e["scene_number"] for e in out_manifest["scenes"]]
        assert numbers == [3, 4], numbers
        assert len(set(numbers)) == len(numbers), "scene_number must be unique per manifest"
        moved = out_manifest["scenes"][1]
        assert moved["audio_file"].endswith("04_slope.wav")
        assert moved["alignment"]["words_file"].endswith("04_slope.words.json")
        assert moved["alignment"]["aligned_file"] is None, "a null path stays null"
        assert moved["beats"][0]["audio_file"] == str(out / "beats" / "04_slope" / "01_x.wav")
        for old in (stale_wav, stale_words, stale_beat):
            assert not old.exists(), f"{old} should have been moved, not copied"
        for new in (out / "scenes" / "04_slope.wav", out / "align" / "04_slope.words.json",
                    out / "beats" / "04_slope" / "01_x.wav"):
            assert new.exists(), new
        assert tts.renumber_scenes(out_manifest, {"cosine": 3, "slope": 4}) == out_manifest


# ---- tts-reuse-key: --dry-run prices a marker-only edit at zero ----

def test_dry_run_prices_a_marker_only_edit_at_zero_calls():
    """(3) "does adding a {show} marker cost anything?" has to be answerable BEFORE the
    call. The deck below moved the scene 03 -> 04 and renamed both reveals; not one word
    changed, so planned calls must be 0 -- and the note must warn that the 0 depends on
    --reuse-existing actually being passed."""
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        outdir = root / "audio_mimo"
        texts = ["first line here", "second line here"]
        identity = {"deck_id": "d", "model": "m", "voice": "Dean", "style": "",
                    "sample_rate": 24000, "channels": 1, "sample_width": 2,
                    "output_dir": str(outdir.resolve())}
        prior = _prior_beats_manifest(outdir / "beats" / "03_sceneA", texts, **identity)
        _write(outdir / "manifest.json", prior)
        story = root / "deck.yml"          # meta.id NOT *_mimo -> freshness gate is a no-op
        story.write_text(
            "meta:\n  id: d\n  section: '9.9'\nscenes:\n"
            "  - id: intro\n    kind: intro\n"
            "  - id: divider_inserted\n    kind: divider\n"        # <- pushes sceneA 03 -> 04
            "  - id: pad\n    kind: divider\n"
            "  - id: sceneA\n    kind: content\n    template: unknown_xyz\n"
            "    say: '{show new.a} first line here {show new.b} second line here'\n",
            encoding="utf-8")
        argv = ["tts.py", "--storyboard", str(story), "--backend", "mock", "--model", "m",
                "--voice", "Dean", "--style", "", "--output-dir", str(outdir), "--dry-run"]
        old_argv, buf = sys.argv, io.StringIO()
        try:
            sys.argv = argv
            with redirect_stdout(buf):
                assert tts.main() == 0
        finally:
            sys.argv = old_argv
        out = buf.getvalue()
        assert "planned first-round calls=0" in out, out
        assert "(no-reuse: 2)" in out, out
        assert "ASSUMES --reuse-existing" in out, out
        assert not (outdir / "beats" / "04_sceneA").exists(), "dry-run must move nothing"
        assert Path(prior["scenes"][0]["beats"][0]["audio_file"]).exists()


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


# ---- T2d: backend billing stats feed the manifest receipt ----

def test_mock_backend_counts_calls():
    b = tts.MockTTSBackend(0.4)
    assert b.stats == {"calls": 0, "retries": 0}
    b.synthesize(tts.TTSRequest(text="hi", model="m", voice="v", style=""))
    b.synthesize(tts.TTSRequest(text="", model="m", voice="v", style=""))   # empty still counts a call here;
    assert b.stats["calls"] == 2 and b.stats["retries"] == 0                 # main() just never calls synth for empties


# ---- T4: ASR QA verdict persists into manifest (F8), three-state, loud on silent skip ----

def test_no_billing_wraps_the_billed_backend_and_refuses_to_spend():
    """--no-billing is the guarantee behind "a marker edit costs nothing" -- which is
    otherwise only a hope: 2026-09-12 a marker-only re-map of 5 scenes billed 13 calls
    because --reuse-existing was omitted, so the reuse index was empty and scene_reuse_ok
    was never consulted. --fallback-budget would not have caught it either (the beats
    terminal is budget-exempt); this flag does."""
    inner = tts.MockTTSBackend(0.4)
    guarded = tts.BudgetedBackend(inner, 0)
    assert guarded.name == inner.name and guarded.stats is inner.stats
    try:
        guarded.synthesize(tts.TTSRequest(text="hi", model="m", voice="v", style=""))
    except SystemExit as exc:
        assert "--max-billed-calls 0" in str(exc)
    else:
        raise AssertionError("--no-billing must abort instead of synthesizing")
    assert inner.stats["calls"] == 0, "the guard must refuse BEFORE the backend is reached"


def test_the_cap_allows_exactly_n_calls_then_aborts():
    """--max-billed-calls N is the bound on a RECOVERY run ("spend a few more"), and it
    covers the beats terminal too, which --fallback-budget does not."""
    inner = tts.MockTTSBackend(0.4)
    guarded = tts.BudgetedBackend(inner, 2)
    req = tts.TTSRequest(text="hi", model="m", voice="v", style="")
    guarded.synthesize(req)
    guarded.synthesize(req)
    try:
        guarded.synthesize(req)
    except SystemExit as exc:
        assert "call #3" in str(exc)
    else:
        raise AssertionError("the cap must abort on the call that would exceed it")
    assert inner.stats["calls"] == 2


def test_no_billing_is_off_by_default_and_never_wraps_mock():
    args = argparse.Namespace(backend="mock", empty_beat_seconds=0.4)
    assert isinstance(tts.build_backend(args), tts.MockTTSBackend)


def test_build_entry_carries_qa():   # T4-3 serialization: qa lands in validation
    from pipeline import scene_align as SA
    entry = SA.build_scene_aligned_entry(
        scene_number=7, plan={"scene_id": "s", "scene_text_hash": "h"},
        beats=[{"text": "hi"}], audio_seconds=1.0, audio_file="x.wav",
        summary={"aligner": "base.en"}, words_file="w.json", aligned_file="a.json",
        gates={"status": "pass", "warnings": [], "metrics": {},
               "qa": {"status": "skipped", "reason": "x"}})
    assert entry["validation"]["qa"] == {"status": "skipped", "reason": "x"}


def _run_finalize(monkey_asr, *, skip_qa=False, qa_wav_none=False, qa_verdict="ok"):
    """Drive _finalize_aligned with fake SA primitives + a monkeypatched
    _asr_probe_tokens; return (entry, captured_stdout). Fully offline (no model)."""
    from pipeline import scene_align as SA
    keys = ("map_to_beats", "run_gates", "qa_diff", "boundary_weak_spans", "tokenize")
    saved = {k: getattr(SA, k) for k in keys}
    saved_probe = tts._asr_probe_tokens
    SA.map_to_beats = lambda plan, words, secs, multi=None: [{"text": "hi", "start_seconds": 0.0, "end_seconds": 1.0}]
    SA.run_gates = lambda *a, **k: {"status": "pass", "warnings": [], "metrics": {}, "failures": []}
    SA.qa_diff = lambda *a, **k: {"verdict": qa_verdict, "score": 1.0}
    SA.boundary_weak_spans = lambda beats: []
    SA.tokenize = lambda text: text.split()
    tts._asr_probe_tokens = monkey_asr
    buf = io.StringIO()
    try:
        with tempfile.TemporaryDirectory() as d, redirect_stdout(buf):
            dd = Path(d)
            plan = {"scene_id": "s", "transcript": "hi there", "scene_text_hash": "h"}
            entry = tts._finalize_aligned(
                plan=plan, words=[{"probability": 0.9}], multi={}, segments=[],
                summary={"aligner": "base.en"}, audio_seconds=1.0, scene_number=7,
                words_file=dd / "w.json", aligned_file=dd / "a.json", audio_file=dd / "07_s.wav",
                args=argparse.Namespace(skip_qa=skip_qa, aligner_model="base.en", aligner_device="cpu"),
                qa_wav=None if qa_wav_none else dd / "qa.wav", promote_from=None)
    finally:
        for k, v in saved.items():
            setattr(SA, k, v)
        tts._asr_probe_tokens = saved_probe
    return entry, buf.getvalue()


def test_finalize_records_qa_state():   # F8 / Adv2 / B5: control flow, not just serialization
    entry, out = _run_finalize(lambda w, a: (["w"], "ran"), qa_verdict="fail")      # ran + fail
    assert entry["validation"]["qa"]["status"] == "ran"
    assert entry["validation"]["status"] == "fail"                                  # qa fail overrides
    entry, out = _run_finalize(lambda w, a: (None, "skipped: whisper_timestamped not installed"))
    assert entry["validation"]["qa"]["status"] == "skipped" and "WARN" in out and "NOT a pass" in out
    entry, out = _run_finalize(lambda w, a: (None, "error: boom"))                  # probe error
    assert entry["validation"]["qa"]["status"] == "error" and "WARN" in out
    entry, out = _run_finalize(lambda w, a: (None, "unused"), skip_qa=True)         # intentional opt-out
    assert entry["validation"]["qa"]["status"] == "skipped" and "WARN" not in out   # silent by policy
    entry, out = _run_finalize(lambda w, a: (None, "unused"), qa_wav_none=True)     # should-have-but-didn't
    assert entry["validation"]["qa"]["status"] == "skipped" and "WARN" in out


if __name__ == "__main__":
    test_unit_auto_matches_content_templates()
    test_resolve_unit_for_scene()
    test_atomic_write_and_promote()
    test_scene_reuse_ok_freshness()
    test_beat_reuse_survives_a_moved_scene_and_a_renamed_reveal()
    test_beat_reuse_hits_in_place_without_moving_anything()
    test_beat_reuse_refuses_when_the_text_changed()
    test_beat_reuse_refuses_on_identity_and_missing_audio()
    test_two_beats_with_identical_text_pair_off_by_index()
    test_scene_aligned_reuse_relocates_a_moved_scene_then_hits()
    test_synthesize_scene_aligned_reuses_a_moved_scene_with_zero_backend_calls()
    test_scene_aligned_relocates_even_when_the_text_changed()
    test_adopt_prior_scene_artifacts_tolerates_a_missing_alignment_block()
    test_renumber_scenes_restamps_from_the_current_storyboard_order()
    test_dry_run_prices_a_marker_only_edit_at_zero_calls()
    test_read_manifest_status_shape_contract()
    test_overwrite_guard_states()
    test_main_guard_blocks_before_synth()
    test_scene_subset_merges_into_prior_manifest()
    test_merge_refuses_identity_mismatch()
    test_mock_backend_counts_calls()
    test_no_billing_wraps_the_billed_backend_and_refuses_to_spend()
    test_the_cap_allows_exactly_n_calls_then_aborts()
    test_no_billing_is_off_by_default_and_never_wraps_mock()
    test_build_entry_carries_qa()
    test_finalize_records_qa_state()
    print("OK tts unit-routing self-test (Task 8)")
