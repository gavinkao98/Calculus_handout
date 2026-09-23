"""Offline self-test: tts.py never destroys, strands or re-bills audio that was already paid
for (code review 2026-09-23, batch T). MockTTSBackend + stub aligner + temp dirs only -- no
API, no whisper model, nothing under video/output.
Run: python video/pipeline/_selftest_tts_paid_audio.py

Every prior take below gets a DISTINCT duration (P=1.0 s, Q=2.0 s, R=3.0 s) and every fresh
mock take is silence of estimate_seconds(text), so "which take is this?" is answered by the
WAV's length, not by trusting the manifest."""
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


if __name__ == "__main__":
    test_beat_reuse_swap_keeps_both_takes()
    test_beat_reuse_prepend_keeps_every_take_and_bills_once()
    test_beat_reuse_rewrite_then_move_then_revert()
    print("OK tts paid-audio self-test (code review 2026-09-23 batch T)")
