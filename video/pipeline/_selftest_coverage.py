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


def test_parser_wiring():
    from pipeline import review_pack, narration_review
    md = Path(__file__).resolve().parent.parent / "content_scripts" / "_fixtures" / "sc_coverage.md"
    units = review_pack.parse_content_script(md)["units"]
    u = next(x for x in units if x["id"] == "proved_here")
    assert isinstance(u["screen_contract"], dict)
    assert [s["id"] for s in u["screen_contract"]["required_steps"]] == ["def", "reduced"]
    # freeform source: with :, ·, em-dash, quotes survives (NOT yaml-parsed)
    assert "em—dash" in u["source"] and u["source"].startswith("chapter3")
    # narration_review mirror ignores the block and still returns the narration
    nu = next(x for x in narration_review.parse_content_script(md)["units"] if x["id"] == "proved_here")
    assert nu["narration"].strip() == "A one line narration." and "screen_contract" not in nu


def test_sc1_and_orphan():
    from pipeline import coverage
    contract = SC.parse_block([
        "  required_steps:",
        "    - id: def",
        "      tex: \"a=b\"",
        "    - id: reduced",
        "      depends_on: e.result",
        "      recap_required: true",
    ])
    contracts = {"u": contract}
    sb_missing = {"scenes": [{"id": "s1", "kind": "content", "ref": "md:u", "covers": ["def"]}]}
    warns = coverage.coverage_issues(sb_missing, contracts, enforce=False)
    msgs = " | ".join(m for _, m in warns)
    assert all(sev == "warn" for sev, _ in warns)
    assert "[SC1]" in msgs and "reduced" in msgs and "u." in msgs  # reduced (recap) uncovered
    assert not any("[SC1]" in m and ".def" in m for _, m in warns)  # def IS covered -> not flagged
    sb_ok = {"scenes": [{"id": "s1", "kind": "content", "ref": "md:u", "covers": ["def", "reduced"]}]}
    assert coverage.coverage_issues(sb_ok, contracts, enforce=False) == []
    sb_orphan = {"scenes": [{"id": "s1", "kind": "content", "ref": "md:u",
                             "covers": ["def", "reduced", "typo"]}]}
    assert any("typo" in m for _, m in coverage.coverage_issues(sb_orphan, contracts, enforce=False))
    errs = coverage.coverage_issues(sb_missing, contracts, enforce=True)
    assert errs and all(sev == "error" for sev, _ in errs)


if __name__ == "__main__":
    test_parse_block()
    test_parser_wiring()
    test_sc1_and_orphan()
    print("OK coverage self-test")
