"""Offline self-test for make.py's ffmpeg compose tail (T10 loudnorm): synthetic clips made
with ffmpeg lavfi -- no API, no manim, no render.
Run: python video/pipeline/_selftest_make_loudnorm.py"""
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import make  # noqa: E402
from pipeline import listening_pack  # noqa: E402


def _ff(*args):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *args], check=True, capture_output=True)


def _av_clip(path: Path, seconds: int = 4) -> Path:
    """A clip encoded like compose's segments (ENCODE_V + AAC 48 kHz stereo) with a tone."""
    path.parent.mkdir(parents=True, exist_ok=True)
    _ff("-f", "lavfi", "-i", f"color=c=0x0f1720:s=320x180:r=30:d={seconds}",
        "-f", "lavfi", "-i", f"sine=frequency=440:sample_rate=48000:duration={seconds}",
        "-map", "0:v:0", "-map", "1:a:0", *make.ENCODE_V, "-c:a", "aac", "-b:a", "192k",
        "-ar", "48000", "-ac", "2", "-shortest", str(path))
    return path


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
    # C-04 (code review 2026-09-23): on --reuse-audio the DELIVERED file is pass 2's own mux,
    # so it must carry T8's +faststart (moov ahead of mdat) just like _concat's output.
    with tempfile.TemporaryDirectory() as d:
        src = _av_clip(Path(d) / "concat.mp4")
        out = Path(d) / "final.mp4"
        make._loudnorm_final(src, out, "192k", make.HOUSE_LUFS)
        boxes = _top_level_boxes(out)
        assert boxes.index("moov") < boxes.index("mdat"), boxes


def test_loudnorm_final_in_non_ascii_dir():
    # A-05 (code review 2026-09-23): pass 1 decoded ffmpeg's stderr with the locale codec
    # (cp950); the UTF-8 input path in it blanked stderr, so a repo under a Chinese folder
    # silently shipped an un-normalized film.
    with tempfile.TemporaryDirectory() as d:
        src = _av_clip(Path(d) / "旁白測試" / "concat.mp4")
        out = src.with_name("final.mp4")
        make._loudnorm_final(src, out, "192k", make.HOUSE_LUFS)
        assert out.exists(), "pass 1 failed to read its own measurement under a non-ASCII path"
        loud = listening_pack.measure_loudness(out)
        assert abs(loud["I"] - make.HOUSE_LUFS) <= make.LOUDNORM_TOL_I, loud


def test_ffmpeg_failure_message_in_non_ascii_dir():
    # A-05: a failing ffmpeg under a Chinese path must raise the RuntimeError carrying its
    # stderr, not a TypeError from slicing the None that a cp950 decode failure left behind.
    with tempfile.TemporaryDirectory() as d:
        missing = Path(d) / "旁白測試" / "missing.mp4"
        try:
            make._ffmpeg(["ffmpeg", "-hide_banner", "-i", str(missing), "-f", "null", "-"])
        except RuntimeError as exc:
            assert "missing.mp4" in str(exc), exc
        else:
            raise AssertionError("ffmpeg on a missing input should have failed")


if __name__ == "__main__":
    for name in sorted(n for n in dir() if n.startswith("test_")):
        globals()[name]()
        print(f"  ok {name}")
    print("[selftest] make loudnorm green")
