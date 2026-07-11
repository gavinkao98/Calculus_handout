"""Offline self-test for pipeline/loudness_ab.py (no API, no manim, no render).
Run: python video/pipeline/_selftest_loudness_ab.py"""
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline import loudness_ab as LA  # noqa: E402


def test_cli_runs_direct_no_module_error():   # Codex blocking-3: direct CLI must self-bootstrap
    with tempfile.TemporaryDirectory() as d:
        script = str(Path(__file__).resolve().parent / "loudness_ab.py")
        out = subprocess.run([sys.executable, script, "--sample", str(Path(d) / "nope.wav"),
                              "--out-dir", str(Path(d) / "o"), "--deck", "t"],
                             capture_output=True, text=True, timeout=120,
                             cwd=str(Path(__file__).resolve().parents[2]))   # repo root, where it used to break
        assert "ModuleNotFoundError" not in out.stderr, out.stderr
        assert out.returncode == 0, out.stderr    # missing sample degrades gracefully (error cells), no crash


def test_parse_loudnorm_json():
    stderr = """[Parsed_loudnorm_0 @ 0000] noise before
{
	"input_i" : "-24.53",
	"input_tp" : "-6.20",
	"input_lra" : "5.20",
	"input_thresh" : "-34.71",
	"output_i" : "-19.02",
	"target_offset" : "0.02"
}
trailing log after"""
    d = LA._parse_loudnorm_json(stderr)
    assert d["input_i"] == "-24.53" and d["target_offset"] == "0.02" and d["input_lra"] == "5.20"


def test_parse_loudnorm_json_missing():
    assert LA._parse_loudnorm_json("no json at all") == {}
    assert LA._parse_loudnorm_json('{"unrelated": 1}') == {}   # no input_i -> {}


def test_row_html_escapes():
    # a target's row must escape any text it renders
    row = LA._version_html("t<1>", {"I": -19.0, "TP": -1.6}, "sample<x>.wav")
    assert "t&lt;1&gt;" in row and "sample&lt;x&gt;.wav" in row and "-19.0" in row


if __name__ == "__main__":
    for name in sorted(n for n in dir() if n.startswith("test_")):
        globals()[name]()
        print(f"  ok {name}")
    print("[selftest] loudness_ab green")
