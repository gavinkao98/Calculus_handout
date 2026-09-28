"""Offline self-test for pipeline/loudnorm.py (the house T10 two-pass loudnorm the Remotion
line's paper/scripts/loudnorm.py finishes a film with): synthetic clips made with ffmpeg
lavfi -- no API, no render.
Run: python video/pipeline/_selftest_loudnorm.py

Was _selftest_make_loudnorm.py (make.py's compose tail) until 2026-09-28; the compose-level
cases stay with make.py in legacy/manim_video/pipeline/_selftest_make_loudnorm.py, and the
C-03 contract they pinned is asserted here at the function the caller branches on."""
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline import listening_pack  # noqa: E402
from pipeline import loudnorm  # noqa: E402


def _ff(*args):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *args], check=True, capture_output=True)


def _av_clip(path: Path, audio_src: str = "sine=frequency=440:sample_rate=48000:duration=4",
             seconds: int = 4) -> Path:
    """An H.264 + AAC 48 kHz stereo clip -- the shape a finished render hands to loudnorm."""
    path.parent.mkdir(parents=True, exist_ok=True)
    _ff("-f", "lavfi", "-i", f"color=c=0x0f1720:s=320x180:r=30:d={seconds}",
        "-f", "lavfi", "-i", audio_src,
        "-map", "0:v:0", "-map", "1:a:0", "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-shortest", str(path))
    return path


def test_normalizes_to_the_house_target():
    with tempfile.TemporaryDirectory() as d:
        src = _av_clip(Path(d) / "raw.mp4")
        out = Path(d) / "final.mp4"
        ok, loud = loudnorm._loudnorm_final(src, out, "192k", loudnorm.HOUSE_LUFS)
        assert ok and out.exists(), loud
        assert abs(loud["I"] - loudnorm.HOUSE_LUFS) <= loudnorm.LOUDNORM_TOL_I, loud


def test_keeps_the_normalized_film_when_only_the_measurement_fails():
    # C-03 (code review 2026-09-23): pass 2 has already written the normalized film when the
    # after-the-fact ebur128 measurement fails (e.g. its 120 s timeout on a 4K final). That is
    # (True, {'error': ...}) -- the film is kept, never thrown away.
    real = listening_pack.measure_loudness
    with tempfile.TemporaryDirectory() as d:
        src = _av_clip(Path(d) / "raw.mp4", "sine=frequency=500:sample_rate=24000:duration=4")
        out = Path(d) / "final.mp4"
        listening_pack.measure_loudness = lambda p: {"error": "ffmpeg unavailable: TimeoutExpired (simulated)"}
        try:
            ok, loud = loudnorm._loudnorm_final(src, out, "192k", loudnorm.HOUSE_LUFS)
        finally:
            listening_pack.measure_loudness = real
        assert ok is True and "error" in loud and out.exists(), (ok, loud)
        measured = real(out)
        assert abs(measured["I"] - loudnorm.HOUSE_LUFS) <= loudnorm.LOUDNORM_TOL_I, measured


def test_reports_failure_on_an_all_silent_film():
    # C-03: an all-silent film measures -inf in pass 1, which pass 2 rejects ("Value -inf for
    # parameter 'measured_I'"). That must come back as (False, {'error': ...}) -- not escape as
    # a RuntimeError -- so the caller can fall back to the un-normalized film.
    with tempfile.TemporaryDirectory() as d:
        src = _av_clip(Path(d) / "raw.mp4", "anullsrc=r=48000:cl=stereo:d=4")
        ok, loud = loudnorm._loudnorm_final(src, Path(d) / "final.mp4", "192k", loudnorm.HOUSE_LUFS)
        assert ok is False and "error" in loud, (ok, loud)


def _top_level_boxes(path: Path) -> list[str]:
    data = path.read_bytes()
    i, order = 0, []
    while i + 8 <= len(data):
        size = int.from_bytes(data[i:i + 4], "big")
        order.append(data[i + 4:i + 8].decode("latin1"))
        if size == 1:
            size = int.from_bytes(data[i + 8:i + 16], "big")
        if size < 8:
            break
        i += size
    return order


def test_loudnorm_final_output_is_faststart():
    # C-04 (code review 2026-09-23): the DELIVERED file is pass 2's own mux, so it must carry
    # +faststart (moov ahead of mdat).
    with tempfile.TemporaryDirectory() as d:
        src = _av_clip(Path(d) / "concat.mp4")
        out = Path(d) / "final.mp4"
        loudnorm._loudnorm_final(src, out, "192k", loudnorm.HOUSE_LUFS)
        boxes = _top_level_boxes(out)
        assert boxes.index("moov") < boxes.index("mdat"), boxes


def test_loudnorm_final_in_non_ascii_dir():
    # A-05 (code review 2026-09-23): pass 1 decoded ffmpeg's stderr with the locale codec
    # (cp950); the UTF-8 input path in it blanked stderr, so a repo under a Chinese folder
    # silently shipped an un-normalized film.
    with tempfile.TemporaryDirectory() as d:
        src = _av_clip(Path(d) / "旁白測試" / "concat.mp4")
        out = src.with_name("final.mp4")
        loudnorm._loudnorm_final(src, out, "192k", loudnorm.HOUSE_LUFS)
        assert out.exists(), "pass 1 failed to read its own measurement under a non-ASCII path"
        loud = listening_pack.measure_loudness(out)
        assert abs(loud["I"] - loudnorm.HOUSE_LUFS) <= loudnorm.LOUDNORM_TOL_I, loud


def test_ffmpeg_failure_message_in_non_ascii_dir():
    # A-05: a failing ffmpeg under a Chinese path must raise the RuntimeError carrying its
    # stderr, not a TypeError from slicing the None that a cp950 decode failure left behind.
    with tempfile.TemporaryDirectory() as d:
        missing = Path(d) / "旁白測試" / "missing.mp4"
        try:
            loudnorm._ffmpeg(["ffmpeg", "-hide_banner", "-i", str(missing), "-f", "null", "-"])
        except RuntimeError as exc:
            assert "missing.mp4" in str(exc), exc
        else:
            raise AssertionError("ffmpeg on a missing input should have failed")


if __name__ == "__main__":
    for name in sorted(n for n in dir() if n.startswith("test_")):
        globals()[name]()
        print(f"  ok {name}")
    print("[selftest] loudnorm green")
