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
"""
from pipeline import _bootstrap

_bootstrap.bootstrap()

import contextlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

from pipeline import rewatch_pack as RP


@contextlib.contextmanager
def fake_repo(deck: str, say: str = "hello {show body} world"):
    """A throwaway repo root holding one storyboard `<deck>.yml` with one content scene
    `s1`; yields (root, section output dir). rewatch_pack's REPO and section lookup point
    at it for the duration."""
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as td:
        root = Path(td)
        (root / "video" / "storyboards").mkdir(parents=True)
        (root / "video" / "storyboards" / f"{deck}.yml").write_text(
            f"meta: {{id: {deck}, section: '9.1'}}\n"
            f"scenes:\n  - {{id: s1, kind: content, template: callout, say: '{say}'}}\n",
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
