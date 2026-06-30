"""Stdlib assert self-test for provenance.py. Run: python video/pipeline/_selftest_provenance.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline import provenance as P  # noqa: E402


def test_parse_ref():
    assert P.parse_ref("md:why_trig") == ("md", "why_trig")
    assert P.parse_ref("doc:frag-sec-3-1") == ("doc", "frag-sec-3-1")
    assert P.parse_ref("doc:sector-inequality") == ("doc", "sector-inequality")
    assert P.parse_ref("nope:x") is None
    assert P.parse_ref("plain string") is None
    assert P.parse_ref("") is None
    assert P.parse_ref("md:") is None          # empty token rejected


def test_constants():
    assert "statement" in P.TEACHING_TEXT_FIELDS
    assert "title" not in P.TEACHING_TEXT_FIELDS
    assert P.OTF_EXEMPT_KINDS == frozenset({"intro", "outro"})
    assert P.OTF_KINDS == frozenset({"content", "divider"})


if __name__ == "__main__":
    test_parse_ref()
    test_constants()
    print("OK provenance self-test")
