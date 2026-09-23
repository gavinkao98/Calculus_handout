"""Self-test: a rewatch pack's evidence is the film that was rendered, timed the way it was
rendered. Run from video/:
    python -m pipeline._selftest_rewatch_pack_evidence

The pack is the ONE shared input of every REWATCH lens, so anything it gets wrong every lens
gets wrong together. Code review 2026-09-23 (batch R) found three ways it could describe a
film other than the one on disk, each pinned here by driving the real `main()` over a fake
repo (synthesised mp4s, hand-written manifests; nothing under video/output is touched):

  B-03  the audio manifest is picked by the deck id -- `audio_mimo/` for an `_mimo` deck,
        `audio/` otherwise, the rule make.py and critic.py already pick by -- and never by
        falling back to whichever subdir exists. The two decks of a section share one output
        dir, so the fallback timed a mock render against the real-voice beats. A manifest
        whose `deck_id` names another deck is refused (exit 2, nothing written).
  B-01  every run extracts its frames afresh. Frames used to be grabbed only when the file
        was missing, and the name is just (index, sample time) -- so re-packing a re-render
        whose timing had not changed (`--reuse-audio`, or an unchanged mock estimate) into
        the same dir kept the PREVIOUS render's pictures beside this render's motion numbers.
  B-02  the pack times beats on the clock make.py rendered. make.py folds `pauses:` into its
        IN-MEMORY manifest only; the pack read the on-disk one, so after every hold each
        reveal time, each "beat N reveal" tile, the dead-zone beat (`_beat_at`) and the
        forced-alignment words were `seconds` early. The expected values here are computed
        by the very call make.py makes (`pauses.apply_pauses`).
"""
from pipeline import _bootstrap

_bootstrap.bootstrap()

import contextlib
import copy
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml
from PIL import Image

from pipeline import audio, pauses
from pipeline import rewatch_pack as RP
from pipeline.timing import SCENE_LEAD_SECONDS as LEAD, SCENE_TAIL_SECONDS as TAIL


@contextlib.contextmanager
def fake_repo(deck: str, say: str = "hello {show body} world", extra: str = ""):
    """A throwaway repo root holding one storyboard `<deck>.yml` with one content scene
    `s1` (`extra` = more flow-mapping fields for it); yields (root, section output dir).
    rewatch_pack's REPO and section lookup point at it for the duration."""
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as td:
        root = Path(td)
        (root / "video" / "storyboards").mkdir(parents=True)
        (root / "video" / "storyboards" / f"{deck}.yml").write_text(
            f"meta: {{id: {deck}, section: '9.1'}}\n"
            f"scenes:\n  - {{id: s1, kind: content, template: callout, say: '{say}'{extra}}}\n",
            encoding="utf-8")
        sec = root / "video" / "output" / "ch09" / "s9.1"
        orig = RP.REPO, RP._bootstrap.section_output_dir
        RP.REPO = root
        RP._bootstrap.section_output_dir = lambda meta: sec
        try:
            yield root, sec
        finally:
            RP.REPO, RP._bootstrap.section_output_dir = orig


def write_manifest(sec: Path, sub: str, deck_id: str, beat_end: float) -> None:
    d = sec / sub
    d.mkdir(parents=True, exist_ok=True)
    (d / "manifest.json").write_text(json.dumps({"deck_id": deck_id, "scenes": [{
        "scene_id": "s1", "narration_mode": "beats",
        "beats": [{"index": 1, "reveal": "body", "start_seconds": 0.0,
                   "end_seconds": beat_end, "text": f"beat from {deck_id}"}]}]}),
        encoding="utf-8")


def render(root: Path, deck: str, color: str = "red", seconds: float = 4.0) -> None:
    """The per-scene A/V file compose would have left: a flat-colour clip."""
    av = root / "video" / "output" / "_av" / deck
    av.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i",
                    f"color=c={color}:s=320x180:r=30:d={seconds}", "-pix_fmt", "yuv420p",
                    str(av / "s1.mp4")], check=True, capture_output=True)


def run(deck: str, *extra: str) -> int:
    argv = sys.argv
    sys.argv = ["rewatch_pack.py", "--deck", deck, *extra]
    try:
        return RP.main()
    except SystemExit as exc:            # a refusal raised rather than returned
        return exc.code if isinstance(exc.code, int) else 1
    finally:
        sys.argv = argv


def pack(sec: Path) -> dict:
    return json.loads((sec / "rewatch_pack" / "pack.json").read_text(encoding="utf-8"))


# ---- B-03: the manifest belongs to the deck being packed -----------------------------

def test_canonical_deck_reads_audio_even_when_audio_mimo_exists():
    with fake_repo("demo_deck") as (root, sec):
        write_manifest(sec, "audio", "demo_deck", 2.0)             # what make.py wrote for it
        write_manifest(sec, "audio_mimo", "demo_deck_mimo", 0.5)   # the real-voice deck's
        render(root, "demo_deck")
        assert run("demo_deck") == 0
        beat = pack(sec)["scenes"][0]["beats"][0]
    assert beat["text"] == "beat from demo_deck" and beat["end_seconds"] == 2.0, beat


def test_mimo_deck_reads_audio_mimo_even_when_audio_exists():
    with fake_repo("demo_deck_mimo") as (root, sec):
        write_manifest(sec, "audio", "demo_deck", 2.0)
        write_manifest(sec, "audio_mimo", "demo_deck_mimo", 0.5)
        render(root, "demo_deck_mimo")
        assert run("demo_deck_mimo") == 0
        beat = pack(sec)["scenes"][0]["beats"][0]
    assert beat["text"] == "beat from demo_deck_mimo" and beat["end_seconds"] == 0.5, beat


def test_no_fallback_to_the_other_decks_manifest():
    """Only the real-voice deck's manifest exists: a canonical-deck pack must stop, not
    borrow it."""
    with fake_repo("demo_deck") as (root, sec):
        write_manifest(sec, "audio_mimo", "demo_deck_mimo", 0.5)
        render(root, "demo_deck")
        rc = run("demo_deck")
        wrote = (sec / "rewatch_pack" / "pack.json").exists()
    assert rc != 0 and not wrote, (rc, wrote)


def test_a_manifest_naming_another_deck_is_refused_before_anything_is_written():
    with fake_repo("demo_deck") as (root, sec):
        write_manifest(sec, "audio", "some_other_deck", 2.0)
        render(root, "demo_deck")
        rc = run("demo_deck")
        wrote = (sec / "rewatch_pack").exists()
    assert rc == 2 and not wrote, (rc, wrote)


# ---- B-01: a re-pack shows this render, not the last one -----------------------------

def _frames(sec: Path) -> list[Path]:
    return sorted((sec / "rewatch_pack" / "01_s1").glob("*.jpg"))


def test_a_repack_into_the_same_dir_extracts_the_new_renders_frames():
    with fake_repo("demo_deck") as (root, sec):
        write_manifest(sec, "audio", "demo_deck", 2.0)
        render(root, "demo_deck", "red")
        assert run("demo_deck") == 0
        first = [Image.open(p).convert("RGB").getpixel((5, 5)) for p in _frames(sec)]
        render(root, "demo_deck", "blue")      # same timing, different picture
        assert run("demo_deck") == 0
        second = [Image.open(p).convert("RGB").getpixel((5, 5)) for p in _frames(sec)]
    assert first and all(r > 200 and b < 60 for r, _g, b in first), first
    assert second and all(b > 200 and r < 60 for r, _g, b in second), second


def test_the_scene_folder_holds_exactly_the_frames_this_pack_lists():
    """A frame left over from an earlier pack (other sample times) must not sit among this
    pack's close-reading frames looking like one of them."""
    with fake_repo("demo_deck") as (root, sec):
        write_manifest(sec, "audio", "demo_deck", 2.0)
        render(root, "demo_deck")
        fdir = sec / "rewatch_pack" / "01_s1"
        fdir.mkdir(parents=True)
        (fdir / "f_07_+099.9s.jpg").write_bytes(b"left over from an older pack")
        assert run("demo_deck") == 0
        listed = {s["file"] for s in pack(sec)["scenes"][0]["samples"]}
        on_disk = {p.name for p in fdir.iterdir()}
    assert on_disk == listed, (sorted(on_disk), sorted(listed))


# ---- B-02: `pauses:` -- the pack's clock is the rendered one ---------------------------

PAUSED_SAY = "{show a} one two {show b} three four {show c} five six"
PAUSED_EXTRA = ", pauses: [{after: b, seconds: 1.5}]"
BOX_X = {"a": 20, "b": 120, "c": 220}           # where each reveal's white box is drawn


def _paused_fixture(root: Path, sec: Path, deck: str) -> dict:
    """Disk manifest + FA words for a 3-beat scene_aligned scene (a [0,2], b [2,4], c [4,6])
    whose storyboard holds 1.5 s after `b`; renders the clip make.py would have rendered
    (each box appears at its PAUSED reveal time) and returns make.py's in-memory entry."""
    adir = sec / "audio_mimo"
    (adir / "align").mkdir(parents=True)
    wav = adir / "01_s1.wav"
    audio.write_pcm_wav(wav, audio.silence_pcm(6.0))
    words = [{"word": w, "start": float(i), "end": float(i + 1)}
             for i, w in enumerate("one two three four five six".split())]
    wf = adir / "align" / "01_s1.words.json"
    wf.write_text(json.dumps({"words": words}), encoding="utf-8")
    beats = [{"index": i + 1, "reveal": r, "text": t, "audio_seconds": 2.0,
              "start_seconds": 2.0 * i, "end_seconds": 2.0 * (i + 1)}
             for i, (r, t) in enumerate([("a", "one two"), ("b", "three four"), ("c", "five six")])]
    disk = {"deck_id": deck, "scenes": [{
        "scene_id": "s1", "scene_number": 1, "narration_mode": "scene_aligned",
        "audio_file": str(wav), "audio_seconds": 6.0, "beats": beats,
        "alignment": {"words_file": str(wf)}}]}
    (adir / "manifest.json").write_text(json.dumps(disk), encoding="utf-8")

    scenes = yaml.safe_load((root / "video" / "storyboards" / f"{deck}.yml")
                            .read_text(encoding="utf-8"))["scenes"]
    mem = pauses.apply_pauses(scenes, copy.deepcopy(disk), sec / "_paused")["scenes"][0]
    dur = LEAD + mem["audio_seconds"] + TAIL
    boxes = ",".join(f"drawbox=x={BOX_X[b['reveal']]}:y=60:w=80:h=60:color=white:t=fill:"
                     f"enable='gte(t,{LEAD + b['start_seconds']})'" for b in mem["beats"])
    av = root / "video" / "output" / "_av" / deck
    av.mkdir(parents=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i",
                    f"color=c=black:s=320x180:r=30:d={dur}", "-vf", boxes,
                    "-pix_fmt", "yuv420p", str(av / "s1.mp4")], check=True, capture_output=True)
    return mem


def test_a_paused_scene_is_packed_on_the_rendered_clock():
    deck = "demo_deck_mimo"
    with fake_repo(deck, PAUSED_SAY, PAUSED_EXTRA) as (root, sec):
        mem = _paused_fixture(root, sec, deck)
        disk_beats = json.loads((sec / "audio_mimo" / "manifest.json")
                                .read_text(encoding="utf-8"))["scenes"][0]["beats"]
        assert run(deck) == 0
        rec = pack(sec)["scenes"][0]
        md = (sec / "rewatch_pack" / "01_s1.md").read_text(encoding="utf-8")
        c_tile = next(s for s in rec["samples"] if s["why"] == "beat 3 reveal -> c")
        c_px = Image.open(sec / "rewatch_pack" / "01_s1" / c_tile["file"]).convert("RGB") \
            .getpixel((BOX_X["c"] + 40, 90))
    mb = mem["beats"]
    # reveal times and the beat table
    assert rec["reveal_times"] == [round(LEAD + b["start_seconds"], 2) for b in mb], rec["reveal_times"]
    assert [(b["start_seconds"], b["end_seconds"]) for b in rec["beats"]] == \
        [(b["start_seconds"], b["end_seconds"]) for b in mb], rec["beats"]
    # the "beat 3 reveal" tile is taken after c really appears, and shows it
    assert c_tile["t_video"] == round(LEAD + mb[2]["start_seconds"] + RP.POST_REVEAL, 2), c_tile
    assert c_px[0] > 200, f"tile {c_tile['file']} does not show block c yet: {c_px}"
    # the FA words moved with the audio: at that instant the voice is on "five"
    assert "[five]" in c_tile["words"], c_tile["words"]
    # the dead zone is attributed to the beat it sits in on the rendered clock
    span = rec["motion"]["fine_longest_still_span"]
    want = RP._beat_at(span, mb)
    assert want != RP._beat_at(span, disk_beats), "fixture does not tell the two clocks apart"
    assert f"{want}  <-- LOCATE DEAD ZONES HERE" in md, (want, span)


if __name__ == "__main__":
    import traceback
    fails = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn(); print(f"PASS {name}")
            except Exception:
                fails += 1; print(f"FAIL {name}"); traceback.print_exc()
    sys.exit(1 if fails else 0)
