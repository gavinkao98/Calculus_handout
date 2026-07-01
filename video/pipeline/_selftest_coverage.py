"""Stdlib assert self-test for _screen_contract.py + coverage.py.
Run: C:/Users/user/Desktop/Calculus_handout/.venv/Scripts/python.exe video/pipeline/_selftest_coverage.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline import _screen_contract as SC  # noqa: E402


def test_parse_block():
    lines = [
        "  required_steps:",
        "    - id: def",
        "      tex: \"a=b\"",
        "    - id: reduced",
        "      depends_on: other.result",
        "      recap_required: true",
    ]
    c = SC.parse_block(lines)
    assert [s["id"] for s in SC.required_steps(c)] == ["def", "reduced"]
    assert SC.is_exempt(c) is False
    # must_show keeps `reduced` because it has recap_required
    assert [s["id"] for s in SC.must_show(c)] == ["def", "reduced"]
    # a pure back-ref (depends_on & not recap_required) is dropped from must_show
    c2 = SC.parse_block(["  required_steps:", "    - id: x", "      depends_on: y.z"])
    assert [s["id"] for s in SC.required_steps(c2)] == ["x"]
    assert [s["id"] for s in SC.must_show(c2)] == []
    # exemption
    assert SC.is_exempt(SC.parse_block(["  coverage_exempt: true"])) is True
    # fail-closed: malformed / non-dict / empty -> None
    assert SC.parse_block(["}{ : not : yaml"]) is None
    assert SC.parse_block(["just a scalar"]) is None
    assert SC.parse_block([]) is None
    assert SC.required_steps(None) == []
    assert SC.must_show(None) == []
    assert SC.is_exempt(None) is False


if __name__ == "__main__":
    test_parse_block()
    print("OK coverage self-test")
