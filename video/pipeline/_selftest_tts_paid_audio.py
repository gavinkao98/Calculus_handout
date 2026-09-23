"""Offline self-test: tts.py never destroys, strands or re-bills audio that was already paid
for (code review 2026-09-23, batch T). MockTTSBackend + stub aligner + temp dirs only -- no
API, no whisper model, nothing under video/output.
Run: python video/pipeline/_selftest_tts_paid_audio.py

Every take is told apart by its LENGTH, not by trusting the manifest: hand-laid prior takes
get distinct durations (P=1.0 s, Q=2.0 s), and a fresh mock take is silence of
estimate_seconds(text), so the main()-driven tests use texts of distinct word counts.
--no-billing / --max-billed-calls are exercised as tts.BudgetedBackend around the mock
(build_backend never wraps mock), the aligner seam is stubbed where a scene unit needs it."""
import argparse
import io
import sys
import tempfile
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline import tts  # noqa: E402
from pipeline.audio import silence_pcm, wav_duration, write_pcm_wav  # noqa: E402
from pipeline.narration import estimate_seconds  # noqa: E402

TOL = 0.02
BEAT_ARGS = argparse.Namespace(model="m", style="", voice="Dean", empty_beat_seconds=0.4,
                               reuse_existing=True, unit="beat")


def _scene(say, scene_id="sceneA"):
    return {"id": scene_id, "kind": "content", "template": "derivation", "say": say}


def _lay_prior_beats(out: Path, say: str, secs, *, scene_number=3, scene_id="sceneA"):
    """Lay down the beat WAVs a real beats-mode run of `say` would have written (one distinct
    duration per beat) and return the prior manifest that records them."""
    beats = tts.scene_beats(_scene(say, scene_id))
    beat_dir = out / "beats" / f"{scene_number:02d}_{scene_id}"
    recorded = []
    for beat, seconds in zip(beats, secs):
        wav = beat_dir / f"{beat['index']:02d}_{tts.safe_stem(beat['reveal'] or beat['id'])}.wav"
        write_pcm_wav(wav, silence_pcm(seconds))
        recorded.append({**beat, "audio_file": str(wav.resolve()),
                         "text_hash": tts.text_hash(beat["text"]), "audio_seconds": seconds})
    return {"backend": "mock", "model": "m", "voice": "Dean", "style": "",
            "scenes": [{"scene_id": scene_id, "scene_number": scene_number,
                        "narration_mode": "beats", "beats": recorded}]}


def _run_beats(out: Path, prior, say, *, scene_number=3, backend=None):
    """One beats-mode scene against `prior`. Returns (entry | None, error | None, calls)."""
    backend = backend or tts.MockTTSBackend(0.4)
    try:
        with redirect_stdout(io.StringIO()):
            entry = tts._synthesize_scene_beats(
                backend=backend, meta={}, scene=_scene(say), scene_number=scene_number,
                output_dir=out, args=BEAT_ARGS, reuse_index=tts.build_reuse_index(prior))
        return entry, None, backend.stats["calls"]
    except Exception as exc:   # noqa: BLE001 -- the pre-fix failure mode IS an exception
        return None, f"{type(exc).__name__}: {exc}", backend.stats["calls"]


def _beat_seconds(entry):
    """[(text, seconds measured on disk)] for every beat the entry records."""
    return [(b["text"], round(wav_duration(Path(b["audio_file"])), 3)) for b in entry["beats"]]


def _assert_takes(entry, expected):
    got = _beat_seconds(entry)
    assert len(got) == len(expected), got
    for (text, seconds), want in zip(got, expected):
        assert abs(seconds - want) <= TOL, f"{text!r}: WAV is {seconds}s, its own take is {want}s ({got})"
    for beat in entry["beats"]:
        assert abs(beat["audio_seconds"] - wav_duration(Path(beat["audio_file"]))) <= TOL, beat


# ---- A-01 / F-01: beat reuse must never overwrite a take another beat has yet to adopt ----

def test_beat_reuse_swap_keeps_both_takes():
    """Two beats trade places (same reveals). Each prior WAV sits on the path the OTHER beat
    wants; moving one onto its new path used to overwrite the other before it was adopted."""
    with tempfile.TemporaryDirectory() as d:
        out = Path(d)
        prior = _lay_prior_beats(out, "{show a} P said here. {show b} Q said here.", [1.0, 2.0])
        entry, err, calls = _run_beats(out, prior, "{show a} Q said here. {show b} P said here.")
        assert err is None, f"swap crashed: {err}"
        assert calls == 0, "both texts are unchanged -- nothing to bill"
        _assert_takes(entry, [2.0, 1.0])


def test_beat_reuse_prepend_keeps_every_take_and_bills_once():
    """A new opening beat pushes every old beat one slot down: the new take used to be written
    straight onto 01_beat_01.wav, which still held P's paid take."""
    with tempfile.TemporaryDirectory() as d:
        out = Path(d)
        prior = _lay_prior_beats(out, "Opening sentence P. {show b} Second sentence Q.", [1.0, 2.0])
        new_text = "Brand new hook N here now and then some more words."
        n_secs = estimate_seconds(new_text)
        assert min(abs(n_secs - 1.0), abs(n_secs - 2.0)) > 0.2, "N must be distinguishable"
        entry, err, calls = _run_beats(
            out, prior, f"{new_text} {{show x}} Opening sentence P. {{show b}} Second sentence Q.")
        assert err is None, f"prepend crashed: {err}"
        assert calls == 1, f"only N is new; got {calls} calls"
        _assert_takes(entry, [n_secs, 1.0, 2.0])
        on_disk = sorted(p.name for p in (out / "beats").rglob("*.wav"))
        assert on_disk == ["01_beat_01.wav", "02_x.wav", "03_b.wav"], on_disk
        assert not list((out / "beats").rglob(".staging")), "staging must not outlive the scene"


def test_beat_reuse_rewrite_then_move_then_revert():
    """Beat 1 is rewritten (N) and P moves to where Q was; Q is dropped. Then the author reverts:
    P must come back from ITS take and Q is re-synthesized -- never N's audio under Q's text."""
    with tempfile.TemporaryDirectory() as d:
        out = Path(d)
        old_say = "{show a} P said here. {show b} Q said here."
        prior = _lay_prior_beats(out, old_say, [1.0, 2.0])
        new_text = "N brand new words that are clearly longer than the rest."
        n_secs = estimate_seconds(new_text)
        entry, err, calls = _run_beats(out, prior, f"{{show a}} {new_text} {{show b}} P said here.")
        assert err is None, f"rewrite-then-move crashed: {err}"
        assert calls == 1, f"only N is new; got {calls} calls"
        _assert_takes(entry, [n_secs, 1.0])
        # revert: the manifest now records THIS run (entry), as main() writes it
        after = {**prior, "scenes": [entry]}
        entry2, err, calls = _run_beats(out, after, old_say)
        assert err is None, f"revert crashed: {err}"
        assert calls == 1, f"only Q needs a take; got {calls} calls"
        _assert_takes(entry2, [1.0, estimate_seconds("Q said here.")])


# ---- A-03: a missing aligner is an environment fault, not a per-take alignment failure ----

def _write_deck(path: Path, scenes) -> Path:
    import yaml
    path.write_text(yaml.safe_dump({"meta": {"id": "demo", "section": "9.9", "title": "t"},
                                    "scenes": scenes}), encoding="utf-8")
    return path


def _run_main(argv, *, backend=None):
    """tts.main() with `argv`; build_backend is swapped for `backend` (a mock, possibly
    budgeted). Returns (exit: int | str, stdout, backend)."""
    backend = backend or tts.MockTTSBackend(0.4)
    saved_bb, saved_argv, buf = tts.build_backend, sys.argv, io.StringIO()
    tts.build_backend = lambda a: backend
    sys.argv = ["tts.py", *argv]
    try:
        with redirect_stdout(buf):
            code = tts.main()
    except SystemExit as exc:
        code = f"SystemExit: {exc}"
    finally:
        tts.build_backend, sys.argv = saved_bb, saved_argv
    return code, buf.getvalue(), backend


class _NoStableTs:
    """Make `import stable_whisper` raise ImportError, whatever this interpreter has."""
    def __enter__(self):
        self._saved = sys.modules.get("stable_whisper", "absent")
        sys.modules["stable_whisper"] = None
        return self

    def __exit__(self, *exc):
        if self._saved == "absent":
            sys.modules.pop("stable_whisper", None)
        else:
            sys.modules["stable_whisper"] = self._saved


_THREE_BEAT_SCENE = {"id": "s1", "kind": "content", "template": "derivation",
                     "say": "First sentence here. {show a} Second sentence here. "
                            "{show b} Third sentence here."}


def test_missing_stable_ts_fails_closed_before_any_call():
    """Without stable-ts every scene-unit scene used to 'fail alignment', walk the ladder
    (resynth billed) and bill every beat at the terminal: 5 calls for a 3-beat scene here,
    ~120 for a 21-scene deck under MiMo. It must stop before the first call instead."""
    with tempfile.TemporaryDirectory() as d, _NoStableTs():
        root = Path(d)
        deck = _write_deck(root / "d.yml", [_THREE_BEAT_SCENE])
        code, out, backend = _run_main(["--storyboard", str(deck), "--backend", "mock",
                                        "--unit", "auto", "--skip-qa",
                                        "--output-dir", str(root / "audio")])
        assert isinstance(code, str) and "stable-ts" in code, (code, out[-600:])
        assert "--unit beat" in code, "the message must name the way out"
        assert backend.stats["calls"] == 0, f"billed {backend.stats['calls']} calls first"
        assert not (root / "audio" / "manifest.json").exists()


def test_missing_stable_ts_is_flagged_by_dry_run():
    """The quote must say a real run would abort, instead of pricing it at 1 call/scene."""
    with tempfile.TemporaryDirectory() as d, _NoStableTs():
        root = Path(d)
        deck = _write_deck(root / "d.yml", [_THREE_BEAT_SCENE])
        code, out, _ = _run_main(["--storyboard", str(deck), "--backend", "mock", "--unit", "auto",
                                  "--output-dir", str(root / "audio"), "--dry-run"])
        assert code == 0, code
        assert "WOULD abort" in out and "stable-ts" in out, out


def test_beat_unit_needs_no_aligner():
    """The preflight is scoped to scene-unit scenes: --unit beat never aligns anything."""
    with tempfile.TemporaryDirectory() as d, _NoStableTs():
        root = Path(d)
        deck = _write_deck(root / "d.yml", [_THREE_BEAT_SCENE])
        code, out, backend = _run_main(["--storyboard", str(deck), "--backend", "mock",
                                        "--unit", "beat", "--output-dir", str(root / "audio")])
        assert code == 0, (code, out[-600:])
        assert backend.stats["calls"] == 3


def test_ladder_history_records_the_root_cause():
    """A rung that fails on an aligner abort must say WHY in fallback_history: the reason used
    to be a fixed string per rung, so the manifest showed four failed rungs and no cause."""
    from pipeline import scene_align as SA

    def _abort(wav_path, plan, **kw):
        raise SA.AlignmentError("simulated root cause XYZ")

    saved = SA.align_scene
    SA.align_scene = _abort
    try:
        with tempfile.TemporaryDirectory() as d, redirect_stdout(io.StringIO()):
            entry = tts.synthesize_scene(
                backend=tts.MockTTSBackend(0.4), meta={}, scene=_THREE_BEAT_SCENE, scene_number=1,
                output_dir=Path(d), reuse_index={}, scene_reuse_index={},
                args=argparse.Namespace(model="m", style="", voice="Dean", unit="scene",
                                        skip_qa=True, aligner_model="base.en",
                                        aligner_device="cpu", fallback_budget=2,
                                        empty_beat_seconds=0.4, reuse_existing=False))
    finally:
        SA.align_scene = saved
    history = entry["fallback_history"]
    failed = [h for h in history if h.get("status") == "fail"]
    assert failed, history
    for h in failed:
        if h["rung"] in ("arbiter", "resynth"):
            assert "simulated root cause XYZ" in h["reason"], h


# ---- A-02: an abort never strands a paid take, and the retry never pays for it again ----

def _fake_align(wav_path, plan, *, model="base.en", device="cpu", **_):
    """Stub aligner: tokens spread over the WAV by character share (always passes the gates)."""
    from pipeline import scene_align as SA
    tokens = SA.tokenize(plan["transcript"])
    dur = wav_duration(Path(wav_path)) * 0.95
    total, acc, words = sum(len(t) for t in tokens) or 1, 0, []
    for tok in tokens:
        start = dur * acc / total
        acc += len(tok)
        words.append({"word": tok, "start": round(start, 3), "end": round(dur * acc / total, 3),
                      "probability": 0.9})
    return {"words": words, "multi": {}, "segments": [],
            "summary": {"aligner": {"tool": "stub", "model": model}}}


class _StubAligner:
    """Swap in the stub aligner and tell main()'s preflight the aligner is installed."""
    def __enter__(self):
        from pipeline import scene_align as SA
        self._saved = (SA.align_scene, tts._scene_aligner_missing)
        SA.align_scene, tts._scene_aligner_missing = _fake_align, (lambda: None)
        return self

    def __exit__(self, *exc):
        from pipeline import scene_align as SA
        SA.align_scene, tts._scene_aligner_missing = self._saved


def _manifest(out: Path):
    import json
    return json.loads((out / "manifest.json").read_text(encoding="utf-8"))


def _disk_disagrees(manifest):
    """Every way the manifest's promises about files on disk are broken (a manifest written
    after an abort must still be one make.py --reuse-audio and a retry can trust)."""
    bad = []
    for e in manifest["scenes"]:
        if e.get("kind", "content") != "content":
            continue
        files = [(e["audio_file"], e["audio_seconds"])]
        files += [(b["audio_file"], b["audio_seconds"]) for b in e.get("beats", []) if b.get("audio_file")]
        for f, secs in files:
            if not Path(f).exists():
                bad.append(f"{e['scene_id']}: {Path(f).name} missing")
            elif abs(wav_duration(Path(f)) - secs) > TOL:
                bad.append(f"{e['scene_id']}: {Path(f).name} is {wav_duration(Path(f)):.2f}s, "
                           f"manifest says {secs}s")
        for key in ("words_file", "aligned_file"):
            f = (e.get("alignment") or {}).get(key)
            if f and not Path(f).exists():
                bad.append(f"{e['scene_id']}: {Path(f).name} missing")
    return bad


def _scene_deck(tag, *, divider=False):
    scenes = [{"id": f"s{i}", "kind": "content", "template": "derivation",
               "say": f"Scene {i} {tag} opening words here. {{show math.0}} "
                      f"Then the rest of scene {i} {tag} follows."} for i in (1, 2, 3)]
    return ([{"id": "div", "kind": "divider"}] if divider else []) + scenes


def test_budget_abort_retry_bills_only_the_unfinished_scene():
    """3 scenes all re-worded (and pushed down one slot by a new divider), cap 2: s1 and s2
    finish, s3 aborts on call #3. Those two paid takes used to be promoted onto disk while the
    manifest was only written at the very end -- so the retry could not see them and paid 3."""
    with tempfile.TemporaryDirectory() as d, _StubAligner():
        root, out = Path(d), Path(d) / "audio"
        common = ["--backend", "mock", "--unit", "scene", "--skip-qa", "--output-dir", str(out)]
        v1 = _write_deck(root / "v1.yml", _scene_deck("alpha"))
        code, log, _ = _run_main(["--storyboard", str(v1), *common])
        assert code == 0, log[-800:]
        m1 = {e["scene_id"]: e for e in _manifest(out)["scenes"]}
        v2 = _write_deck(root / "v2.yml", _scene_deck("beta gamma delta", divider=True))
        code, log, _ = _run_main(["--storyboard", str(v2), *common, "--reuse-existing"],
                                 backend=tts.BudgetedBackend(tts.MockTTSBackend(0.4), 2))
        assert isinstance(code, str) and "call #3" in code, (code, log[-800:])
        m2 = _manifest(out)
        assert _disk_disagrees(m2) == [], _disk_disagrees(m2)
        by_id = {e["scene_id"]: e for e in m2["scenes"]}
        for sid in ("s1", "s2"):
            assert by_id[sid]["scene_text_hash"] != m1[sid]["scene_text_hash"], \
                f"{sid}'s paid take is on disk but not in the manifest"
        assert by_id["s3"] == m1["s3"], "the interrupted scene keeps its prior entry"
        code, log, backend = _run_main(["--storyboard", str(v2), *common, "--reuse-existing"],
                                       backend=tts.BudgetedBackend(tts.MockTTSBackend(0.4), 10))
        assert code == 0, log[-800:]
        assert backend.stats["calls"] == 1, f"retry paid {backend.stats['calls']} calls, 1 was left"
        assert _disk_disagrees(_manifest(out)) == []
        assert sorted(p.name for p in (out / "scenes").glob("*.wav")) == \
            ["02_s1.wav", "03_s2.wav", "04_s3.wav"], "no WAV may linger under a stale number"


def _say(*parts):
    return " ".join(parts)


P5 = "Pee has five words here."                      # 5 words -> 2.0 s
Q8 = "Queue has eight words in this one here."        # 8 words -> 3.2 s
N10 = "En has ten words so it is longest of all."      # 10 words -> 4.0 s
R6 = "Are has six words right here."                  # 6 words -> 2.4 s
R7 = "Are has seven words right here now."            # 7 words -> 2.8 s


def _beats_deck(a_say, b_say, *, divider=False):
    scenes = [{"id": "A", "kind": "content", "template": "derivation", "say": a_say},
              {"id": "B", "kind": "content", "template": "derivation", "say": b_say}]
    return ([{"id": "div", "kind": "divider"}] if divider else []) + scenes


def test_beats_abort_then_revert_binds_each_beat_to_its_own_take():
    """A: N is written where P was and P moves to where Q was; B then aborts on the cap. The
    manifest still said 01_a=P / 02_b=Q while the disk held N / P, so reverting the edit
    silently bound N's voice to P's words (and P's to Q's) -- make.py's check accepted it."""
    with tempfile.TemporaryDirectory() as d:
        root, out = Path(d), Path(d) / "audio"
        common = ["--backend", "mock", "--unit", "beat", "--output-dir", str(out)]
        v1 = _write_deck(root / "v1.yml", _beats_deck(_say("{show a}", P5, "{show b}", Q8),
                                                      _say("{show c}", R6)))
        assert _run_main(["--storyboard", str(v1), *common])[0] == 0
        v2 = _write_deck(root / "v2.yml", _beats_deck(_say("{show a}", N10, "{show b}", P5),
                                                      _say("{show c}", R7)))
        code, log, backend = _run_main(["--storyboard", str(v2), *common, "--reuse-existing"],
                                       backend=tts.BudgetedBackend(tts.MockTTSBackend(0.4), 1))
        assert isinstance(code, str) and "--max-billed-calls 1" in code, (code, log[-800:])
        assert _disk_disagrees(_manifest(out)) == [], _disk_disagrees(_manifest(out))
        code, log, backend = _run_main(["--storyboard", str(v1), *common, "--reuse-existing"],
                                       backend=tts.BudgetedBackend(tts.MockTTSBackend(0.4), 5))
        assert code == 0, log[-800:]
        a = {e["scene_id"]: e for e in _manifest(out)["scenes"]}["A"]
        _assert_takes(a, [2.0, 3.2])
        assert backend.stats["calls"] == 1, "only Q's take was gone (Q left the deck in v2)"


def test_no_billing_abort_after_a_moved_beats_scene_retries_free():
    """A new divider moves A 01 -> 02 (text unchanged, reused for free) and B's text changed,
    so --no-billing aborts at B. A's old files were already deleted and the manifest still
    pointed at them: make.py --reuse-audio refused, and even after reverting B the free retry
    aborted with "prior WAV is gone" although A's take was sitting at its new path."""
    with tempfile.TemporaryDirectory() as d:
        root, out = Path(d), Path(d) / "audio"
        common = ["--backend", "mock", "--unit", "beat", "--output-dir", str(out)]
        a_say, b_say = _say("{show a}", P5, "{show b}", Q8), _say("{show c}", R6)
        v1 = _write_deck(root / "v1.yml", _beats_deck(a_say, b_say))
        assert _run_main(["--storyboard", str(v1), *common])[0] == 0
        v2 = _write_deck(root / "v2.yml", _beats_deck(a_say, _say("{show c}", R7), divider=True))
        code, log, _ = _run_main(["--storyboard", str(v2), *common, "--reuse-existing", "--no-billing"],
                                 backend=tts.BudgetedBackend(tts.MockTTSBackend(0.4), 0))
        assert isinstance(code, str) and "--max-billed-calls 0" in code, (code, log[-800:])
        assert _disk_disagrees(_manifest(out)) == [], _disk_disagrees(_manifest(out))
        v3 = _write_deck(root / "v3.yml", _beats_deck(a_say, b_say, divider=True))
        code, log, backend = _run_main(["--storyboard", str(v3), *common, "--reuse-existing",
                                        "--no-billing"],
                                       backend=tts.BudgetedBackend(tts.MockTTSBackend(0.4), 0))
        assert code == 0, (code, log[-800:])
        assert backend.stats["calls"] == 0
        assert _disk_disagrees(_manifest(out)) == []
        assert not (out / "beats" / "01_A").exists(), "A's stale-number directory must be gone"


def test_budget_abort_never_pays_for_half_a_beats_scene():
    """A beats scene whose three beats all changed, cap 2: it used to pay 2 calls and then
    abort, and those two takes -- never recorded -- were paid for again by the retry. The
    scene's calls are known before the first one, so it now stops before spending any."""
    with tempfile.TemporaryDirectory() as d:
        root, out = Path(d), Path(d) / "audio"
        common = ["--backend", "mock", "--unit", "beat", "--output-dir", str(out)]
        v1 = _write_deck(root / "v1.yml", [{"id": "A", "kind": "content", "template": "derivation",
                                            "say": _say(P5, "{show a}", Q8, "{show b}", R6)}])
        assert _run_main(["--storyboard", str(v1), *common])[0] == 0
        v2 = _write_deck(root / "v2.yml", [{"id": "A", "kind": "content", "template": "derivation",
                                            "say": _say(N10, "{show a}", R7, "{show b}", Q8 + " Too.")}])
        code, log, backend = _run_main(["--storyboard", str(v2), *common, "--reuse-existing"],
                                       backend=tts.BudgetedBackend(tts.MockTTSBackend(0.4), 2))
        assert isinstance(code, str) and "--max-billed-calls 2" in code, (code, log[-800:])
        assert backend.stats["calls"] == 0, f"paid {backend.stats['calls']} calls, then threw them away"
        code, log, backend = _run_main(["--storyboard", str(v2), *common, "--reuse-existing"],
                                       backend=tts.BudgetedBackend(tts.MockTTSBackend(0.4), 3))
        assert code == 0 and backend.stats["calls"] == 3, (code, backend.stats)


# ---- A-04: a take the small.en arbiter accepted is reused without paying for a new one ----

class _NamedMock(tts.MockTTSBackend):
    name = "mimo"      # the prior manifest's identity (a real run's backend.name)


def _arbiter_rescued_prior(out: Path, scene):
    """A scene_aligned entry exactly as the ladder leaves it when base.en failed on this WAV
    and the small.en arbiter accepted it."""
    from pipeline import scene_align as SA
    plan = SA.build_scene_plan(scene)
    wav = out / "scenes" / "26_recap.wav"
    write_pcm_wav(wav, silence_pcm(7.0))
    words, aligned = out / "align" / "26_recap.words.json", out / "align" / "26_recap.aligned.json"
    words.parent.mkdir(parents=True)
    words.write_text("{}", encoding="utf-8")
    aligned.write_text("{}", encoding="utf-8")
    return wav, {"backend": "mimo", "model": "m", "voice": "Dean", "style": "", "scenes": [{
        "scene_id": "recap", "scene_number": 26, "narration_mode": "scene_aligned",
        "scene_text_hash": plan["scene_text_hash"], "audio_file": str(wav), "audio_seconds": 7.0,
        "alignment": {"words_file": str(words), "aligned_file": str(aligned),
                      "aligner": {"tool": "stable-ts", "model": "small.en"}},
        "validation": {"status": "pass"},
        "fallback_history": [{"rung": "arbiter", "status": "pass",
                              "reason": "small.en arbiter re-align"}]}]}


def test_arbiter_rescued_scene_is_reused_for_free():
    """scene_reuse_ok (rightly) ignores the aligner, but the reuse re-align then ran base.en --
    the model that had already failed on this very WAV (stable-ts is deterministic) -- and
    fell straight through to a BILLED re-synthesis, overwriting the accepted take. With
    --no-billing such a scene could never be re-mapped at all."""
    from pipeline import scene_align as SA
    scene = {"id": "recap", "kind": "content", "template": "recap_cards",
             "say": "Here is what we found. {show point.0} Sine goes to cosine. "
                    "{show point.1} Cosine goes to minus sine."}
    calls = []

    def base_fails_small_passes(wav_path, plan, *, model="base.en", device="cpu", **kw):
        calls.append((Path(wav_path).name, model))
        if model == "base.en":
            raise SA.AlignmentError("stable-ts aborted: > 20% of words failed to align")
        return _fake_align(wav_path, plan, model=model)

    args = argparse.Namespace(model="m", style="", voice="Dean", aligner_model="base.en",
                              aligner_device="cpu", skip_qa=True, unit="auto", fallback_budget=2,
                              empty_beat_seconds=0.4, reuse_existing=True)
    saved = SA.align_scene
    SA.align_scene = base_fails_small_passes
    try:
        for label, cap in (("uncapped", None), ("--no-billing", 0)):
            with tempfile.TemporaryDirectory() as d:
                out = Path(d)
                wav, prior = _arbiter_rescued_prior(out, scene)
                inner = _NamedMock(0.4)
                backend = inner if cap is None else tts.BudgetedBackend(inner, cap)
                calls.clear()
                try:
                    with redirect_stdout(io.StringIO()):
                        entry = tts._synthesize_scene_aligned(
                            backend=backend, meta={}, scene=scene, scene_number=26,
                            output_dir=out, args=args, reuse_index={},
                            scene_reuse_index=tts.build_scene_reuse_index(prior))
                except SystemExit as exc:
                    raise AssertionError(f"{label}: aborted -- {str(exc)[:120]}") from None
                assert inner.stats["calls"] == 0, f"{label}: paid {inner.stats['calls']} for a kept take"
                assert entry["narration_mode"] == "scene_aligned", (label, entry["narration_mode"])
                assert entry["validation"]["status"] in ("pass", "pass_with_warnings"), label
                assert abs(wav_duration(wav) - 7.0) <= TOL, f"{label}: the accepted take was replaced"
                assert ("26_recap.wav", "small.en") in calls, (label, calls)
                assert [h["rung"] for h in entry["fallback_history"]] == ["arbiter"], \
                    (label, entry["fallback_history"])
    finally:
        SA.align_scene = saved


if __name__ == "__main__":
    test_beat_reuse_swap_keeps_both_takes()
    test_beat_reuse_prepend_keeps_every_take_and_bills_once()
    test_beat_reuse_rewrite_then_move_then_revert()
    test_missing_stable_ts_fails_closed_before_any_call()
    test_missing_stable_ts_is_flagged_by_dry_run()
    test_beat_unit_needs_no_aligner()
    test_ladder_history_records_the_root_cause()
    test_budget_abort_retry_bills_only_the_unfinished_scene()
    test_beats_abort_then_revert_binds_each_beat_to_its_own_take()
    test_no_billing_abort_after_a_moved_beats_scene_retries_free()
    test_budget_abort_never_pays_for_half_a_beats_scene()
    test_arbiter_rescued_scene_is_reused_for_free()
    print("OK tts paid-audio self-test (code review 2026-09-23 batch T)")
