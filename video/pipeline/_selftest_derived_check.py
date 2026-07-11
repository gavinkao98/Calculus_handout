"""Offline self-test for pipeline/derived_check.py (no API, no manim).
Run: python video/pipeline/_selftest_derived_check.py"""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline.derived_check import stamp_for, text_sha256, check_derived_freshness  # noqa: E402


def _fixture(d: Path, canon_text="a: 1\n", spoken_text="s: 1\n"):
    """Lay out storyboards/ + content_scripts/ like the real repo and return the
    generated deck path with a fresh two-input stamp."""
    (d / "storyboards").mkdir()
    (d / "content_scripts").mkdir()
    canon = d / "storyboards" / "deck.yml"
    spoken = d / "content_scripts" / "deck.spoken.yml"
    canon.write_text(canon_text, encoding="utf-8")
    spoken.write_text(spoken_text, encoding="utf-8")
    derived = d / "storyboards" / "deck_mimo.yml"
    data = {"meta": {"id": "deck_mimo", "derived_from": stamp_for(derived, canon, spoken)}}
    return derived, canon, spoken, data


def test_non_generated_deck_is_ignored():
    assert check_derived_freshness(Path("x.yml"), {"meta": {"id": "ch99_demo"}}) is None


def test_malformed_data_is_left_for_schema():   # B2: no AttributeError
    assert check_derived_freshness(Path("d_mimo.yml"), ["not", "a", "mapping"]) is None
    assert check_derived_freshness(Path("d_mimo.yml"), None) is None
    assert check_derived_freshness(Path("d_mimo.yml"), {"meta": ["bad"]}) is None


def test_missing_stamp_is_flagged():
    msg = check_derived_freshness(Path("d_mimo.yml"), {"meta": {"id": "d_mimo"}})
    assert msg and "derived_from" in msg


def test_fresh_then_canonical_stale():
    with tempfile.TemporaryDirectory() as d:
        derived, canon, _spoken, data = _fixture(Path(d))
        assert check_derived_freshness(derived, data) is None
        canon.write_text("a: 2\n", encoding="utf-8")          # canonical moves on
        assert "STALE" in (check_derived_freshness(derived, data) or "")


def test_spoken_change_is_stale():   # B1: spoken.yml is a stamped input too
    with tempfile.TemporaryDirectory() as d:
        derived, _canon, spoken, data = _fixture(Path(d))
        spoken.write_text("s: 2\n", encoding="utf-8")         # spoken edited, no re-derive
        assert "STALE" in (check_derived_freshness(derived, data) or "")


def test_crlf_lf_hash_is_stable():   # B1: autocrlf must not false-flag
    with tempfile.TemporaryDirectory() as d:
        crlf = Path(d) / "x_crlf.yml"; crlf.write_bytes(b"a: 1\r\nb: 2\r\n")
        lf = Path(d) / "x_lf.yml";     lf.write_bytes(b"a: 1\nb: 2\n")
        assert text_sha256(crlf) == text_sha256(lf)


if __name__ == "__main__":
    for name in sorted(n for n in dir() if n.startswith("test_")):
        globals()[name]()
        print(f"  ok {name}")
    print("[selftest] derived_check green")
