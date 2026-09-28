"""Self-test: the `pauses:` scene field (an authored silent hold after a reveal). Run from video/:
    python -m pipeline._selftest_pauses

`pauses` is a pure narration transform (pipeline/pauses.py): silence is spliced into the
scene WAV at the paused beat's onset and that beat's duration grows by the same amount, so
render (beat_durations), compose (mux) and the sidecars (timeline/vtt) all read ONE clock
and the player needs no new concept. This test pins:
  (a) the beat table -- the paused beat grows, every later beat shifts, the scene total grows
  (b) the WAV splice -- new length == old + seconds, and the samples on each side are intact
  (c) [moved 2026-09-28 with schema.py to legacy/manim_video/pipeline/_selftest_pauses_schema.py]
  (d) zero behaviour change -- a scene with no `pauses` key is returned untouched
  (e) the timing-only transform (code review 2026-09-23 B-02) -- `apply_pauses_timing` gives
      the beat table apply_pauses gives, reads and writes no file, and `shift_words` moves
      forced-alignment word times by the same cut the WAV splice makes. rewatch_pack and
      critic re-read the ON-DISK manifest and apply this, so they time the film make.py
      rendered rather than one `seconds` early after every hold.

Manim-free: operates on plain dicts + WAV files.
"""
import copy
import json
import tempfile
from pathlib import Path

from pipeline import audio, pauses

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


# -- (e) the timing-only transform the review tools re-apply ------------------

def _disk(per_beat=(2.0, 3.0, 4.0)):
    tmp = Path(tempfile.mkdtemp())
    wav = tmp / "scene.wav"
    _tone_wav(wav, list(per_beat))
    return {"deck_id": "d", "scenes": [_entry(wav, list(per_beat))]}, tmp


def test_timing_only_transform_gives_apply_pauses_beat_table_and_writes_nothing():
    field = [{"after": "step.0", "seconds": 1.0}, {"after": "step.1", "seconds": 0.5}]
    disk, tmp = _disk()
    before = sorted(tmp.rglob("*"))
    timed = pauses.apply_pauses_timing([_scene(field)], disk)
    assert sorted(tmp.rglob("*")) == before, "the timing transform must not touch a file"
    assert disk["scenes"][0]["beats"][2]["start_seconds"] == 5.0, "the input stays the disk copy"
    full = pauses.apply_pauses([_scene(field)], copy.deepcopy(disk), tmp / "paused")
    t_entry, f_entry = timed["scenes"][0], full["scenes"][0]
    assert t_entry["audio_seconds"] == f_entry["audio_seconds"] == 10.5
    for key in ("start_seconds", "end_seconds", "audio_seconds"):
        assert [b[key] for b in t_entry["beats"]] == [b[key] for b in f_entry["beats"]], key
    assert t_entry["audio_file"] == str(tmp / "scene.wav"), "no WAV -> the audio file is not swapped"


def test_timing_only_transform_without_pauses_is_the_same_object():
    disk, _ = _disk()
    assert pauses.apply_pauses_timing([_scene(None)], disk) is disk
    assert pauses.apply_pauses_timing([_scene([])], disk) is disk


def test_fa_words_move_by_the_same_cut_the_wav_splice_makes():
    field = [{"after": "step.0", "seconds": 1.5}]            # beat 2 starts at 2.0
    disk, tmp = _disk()
    words = [{"word": "one", "start": 0.2, "end": 2.0},        # ends exactly at the cut: stays
             {"word": "two", "start": 2.0, "end": 4.8},        # starts at the cut: moves
             {"word": "three", "start": 5.1, "end": 8.9}]      # beat 3: moves
    timed = pauses.apply_pauses_timing([_scene(field)], disk)
    moved = pauses.shift_words(words, timed["scenes"][0]["pause_splices"])
    assert [(w["word"], w["start"], w["end"]) for w in moved] == [
        ("one", 0.2, 2.0), ("two", 3.5, 6.3), ("three", 6.6, 10.4)], moved
    assert words[1]["start"] == 2.0, "the caller's word list is not modified"
    # and each moved word still sits on its own speech in the spliced WAV
    full = pauses.apply_pauses([_scene(field)], copy.deepcopy(disk), tmp / "paused")
    pcm, _sr, _ch, _sw = audio.read_wav_pcm(Path(full["scenes"][0]["audio_file"]))

    def val(at_seconds):
        i = int(at_seconds * _SR) * 2
        return int.from_bytes(pcm[i:i + 2], "little", signed=True)

    assert [val((w["start"] + w["end"]) / 2) for w in moved] == [1000, 2000, 3000]
    assert pauses.shift_words(words, None) is words and pauses.shift_words(None, [(2.0, 1.5)]) is None


# -- pause naming a reveal this scene never makes ----------------------------

def test_unknown_after_raises():
    try:
        _apply([{"after": "step.9", "seconds": 1.0}])
    except KeyError as exc:
        assert "step.9" in str(exc)
    else:
        raise AssertionError("a pause whose `after` names no beat must not pass silently")


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
