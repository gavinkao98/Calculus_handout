"""Self-test: the `pauses:` scene field (an authored silent hold after a reveal). Run from video/:
    python -m pipeline._selftest_pauses

`pauses` is a pure narration transform (pipeline/pauses.py): silence is spliced into the
scene WAV at the paused beat's onset and that beat's duration grows by the same amount, so
render (beat_durations), compose (mux) and the sidecars (timeline/vtt) all read ONE clock
and the player needs no new concept. This test pins:
  (a) the beat table -- the paused beat grows, every later beat shifts, the scene total grows
  (b) the WAV splice -- new length == old + seconds, and the samples on each side are intact
  (c) schema -- a `pauses[].after` naming no {show} reveal in `say` is an ERROR (a typo'd
      pause would otherwise silently do nothing)
  (d) zero behaviour change -- a scene with no `pauses` key is returned untouched

Manim-free: operates on plain dicts + WAV files.
"""
import json
import tempfile
from pathlib import Path

from pipeline import audio, pauses, schema

_SR = audio.DEFAULT_SAMPLE_RATE


def _scene(pauses_field=None):
    s = {
        "id": "s1", "kind": "content", "template": "derivation",
        "say": "One. {show step.0} Two. {show step.1} Three.",
    }
    if pauses_field is not None:
        s["pauses"] = pauses_field
    return s


def _tone_wav(path: Path, per_beat: list[float], *, value: int = 1000) -> None:
    """A WAV whose Nth beat window carries the constant sample value N+1, so a splice
    can be checked by reading which value sits where."""
    pcm = bytearray()
    for i, secs in enumerate(per_beat):
        frames = int(round(secs * _SR))
        pcm += (value * (i + 1)).to_bytes(2, "little", signed=True) * frames
    audio.write_pcm_wav(path, bytes(pcm))


def _entry(wav: Path, per_beat: list[float]) -> dict:
    beats, t = [], 0.0
    for i, secs in enumerate(per_beat, start=1):
        beats.append({"index": i, "id": f"beat_{i:02d}",
                      "reveal": None if i == 1 else f"step.{i - 2}",
                      "text": f"beat {i}", "audio_seconds": round(secs, 3),
                      "start_seconds": round(t, 3), "end_seconds": round(t + secs, 3)})
        t += secs
    return {"scene_number": 1, "scene_id": "s1", "kind": "content",
            "narration_mode": "scene_aligned", "audio_file": str(wav),
            "audio_seconds": round(t, 3), "beat_count": len(beats), "beats": beats}


def _apply(pauses_field, per_beat=(2.0, 3.0, 4.0)):
    tmp = Path(tempfile.mkdtemp())
    wav = tmp / "scene.wav"
    _tone_wav(wav, list(per_beat))
    manifest = {"deck_id": "d", "scenes": [_entry(wav, list(per_beat))]}
    out = pauses.apply_pauses([_scene(pauses_field)], manifest, tmp / "paused")
    return out["scenes"][0], tmp


# -- (d) no `pauses` key -> byte-identical manifest ---------------------------

def test_no_pauses_field_is_untouched():
    entry, _ = _apply(None)
    assert entry["audio_seconds"] == 9.0
    assert [b["start_seconds"] for b in entry["beats"]] == [0.0, 2.0, 5.0]
    assert entry["audio_file"].endswith("scene.wav"), "no pause -> original WAV, no copy"


def test_empty_pauses_list_is_untouched():
    entry, _ = _apply([])
    assert entry["audio_seconds"] == 9.0 and entry["audio_file"].endswith("scene.wav")


# -- (a) the beat table ------------------------------------------------------

def test_paused_beat_grows_and_later_beats_shift():
    entry, _ = _apply([{"after": "step.0", "seconds": 1.5}])
    beats = entry["beats"]
    # beat 2 is the one revealing step.0
    assert beats[0]["audio_seconds"] == 2.0 and beats[0]["start_seconds"] == 0.0
    assert beats[1]["audio_seconds"] == 4.5, "paused beat absorbs the hold"
    assert beats[1]["start_seconds"] == 2.0 and beats[1]["end_seconds"] == 6.5
    assert beats[2]["start_seconds"] == 6.5 and beats[2]["end_seconds"] == 10.5
    assert entry["audio_seconds"] == 10.5
    assert sum(b["audio_seconds"] for b in beats) == entry["audio_seconds"]


def test_two_pauses_accumulate():
    entry, _ = _apply([{"after": "step.0", "seconds": 1.0},
                       {"after": "step.1", "seconds": 0.5}])
    beats = entry["beats"]
    assert beats[1]["audio_seconds"] == 4.0 and beats[2]["audio_seconds"] == 4.5
    assert beats[2]["start_seconds"] == 6.0
    assert entry["audio_seconds"] == 10.5


def test_pause_on_the_last_beat():
    entry, _ = _apply([{"after": "step.1", "seconds": 2.0}])
    assert entry["beats"][2]["audio_seconds"] == 6.0
    assert entry["audio_seconds"] == 11.0


# -- (b) the WAV splice ------------------------------------------------------

def test_wav_grows_by_exactly_the_pause_and_keeps_both_sides():
    entry, _tmp = _apply([{"after": "step.0", "seconds": 1.5}])
    out = Path(entry["audio_file"])
    assert out.name == "scene.wav" and out.parent.name == "paused"
    assert abs(audio.wav_duration(out) - 10.5) < 1e-6
    pcm, sr, ch, sw = audio.read_wav_pcm(out)
    assert (sr, ch, sw) == (_SR, 1, 2)

    def val(at_seconds):
        i = int(at_seconds * _SR) * 2
        return int.from_bytes(pcm[i:i + 2], "little", signed=True)

    assert val(1.0) == 1000          # beat 1 audio, before the splice
    assert val(2.0 + 0.75) == 0      # the inserted silence sits at beat 2's onset
    assert val(2.0 + 1.5 + 1.0) == 2000   # beat 2's speech, intact after the splice
    assert val(6.5 + 1.0) == 3000    # beat 3, shifted whole


def test_original_wav_is_not_modified():
    entry, tmp = _apply([{"after": "step.0", "seconds": 1.5}])
    assert abs(audio.wav_duration(tmp / "scene.wav") - 9.0) < 1e-6


# -- pause naming a reveal this scene never makes ----------------------------

def test_unknown_after_raises():
    try:
        _apply([{"after": "step.9", "seconds": 1.0}])
    except KeyError as exc:
        assert "step.9" in str(exc)
    else:
        raise AssertionError("a pause whose `after` names no beat must not pass silently")


# -- (c) schema gate ---------------------------------------------------------

def _errors(scene):
    data = {"meta": {"id": "d", "section": "1.1"}, "scenes": [scene]}
    return [m for s, m in schema.schema_storyboard(data) if s == "error"]


def test_schema_accepts_a_well_formed_pause():
    assert not _errors(_scene([{"after": "step.1", "seconds": 1.2}]))


def test_schema_rejects_pause_after_unrevealed_id():
    errs = _errors(_scene([{"after": "step.9", "seconds": 1.2}]))
    assert any("pauses" in e and "step.9" in e for e in errs), errs


def test_schema_rejects_malformed_pause_entries():
    assert any("pauses" in e for e in _errors(_scene([{"seconds": 1.0}])))          # no `after`
    assert any("pauses" in e for e in _errors(_scene([{"after": "step.0"}])))       # no `seconds`
    assert any("pauses" in e for e in _errors(_scene([{"after": "step.0", "seconds": 0}])))
    assert any("pauses" in e for e in _errors(_scene({"after": "step.0"})))         # not a list


def test_schema_pause_on_non_content_scene_is_an_error():
    errs = _errors({"id": "d1", "kind": "divider", "pauses": [{"after": "x", "seconds": 1}]})
    assert any("pauses" in e for e in errs), errs


if __name__ == "__main__":
    import sys, traceback
    fails = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn(); print(f"PASS {name}")
            except Exception:
                fails += 1; print(f"FAIL {name}"); traceback.print_exc()
    sys.exit(1 if fails else 0)
