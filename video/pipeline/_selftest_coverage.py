"""Stdlib assert self-test for _screen_contract.py + step_coverage.py.
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
    from pipeline import step_coverage as coverage
    contract = SC.parse_block([
        "  required_steps:",
        "    - id: def",
        "      tex: \"a=b\"",
        "    - id: mid",
        "      tex: \"b=c\"",
    ])
    contracts = {"u": contract}
    sb_missing = {"scenes": [{"id": "s1", "kind": "content", "ref": "md:u", "covers": ["def"]}]}
    warns = coverage.coverage_issues(sb_missing, contracts, enforce=False)
    msgs = " | ".join(m for _, m in warns)
    assert all(sev == "warn" for sev, _ in warns)
    assert "[SC1]" in msgs and ".mid" in msgs and "u." in msgs   # mid (plain must-show) uncovered
    assert not any("[SC1]" in m and ".def" in m for _, m in warns)  # def IS covered -> not flagged
    sb_ok = {"scenes": [{"id": "s1", "kind": "content", "ref": "md:u", "covers": ["def", "mid"]}]}
    assert coverage.coverage_issues(sb_ok, contracts, enforce=False) == []
    sb_orphan = {"scenes": [{"id": "s1", "kind": "content", "ref": "md:u",
                             "covers": ["def", "mid", "typo"]}]}
    assert any("typo" in m for _, m in coverage.coverage_issues(sb_orphan, contracts, enforce=False))
    errs = coverage.coverage_issues(sb_missing, contracts, enforce=True)
    assert errs and all(sev == "error" for sev, _ in errs)


def test_sc2_and_missing_contract():
    from pipeline import step_coverage as coverage
    # a recap_required back-ref, uncovered -> SC2 ONLY (not double-reported as SC1)
    contract = SC.parse_block([
        "  required_steps:",
        "    - id: reduced",
        "      depends_on: e.result",
        "      recap_required: true",
    ])
    sb = {"scenes": [{"id": "s1", "kind": "content", "ref": "md:u", "covers": []}]}
    msgs = " | ".join(m for _, m in coverage.coverage_issues(sb, {"u": contract}, enforce=False))
    assert "[SC2]" in msgs and "reduced" in msgs
    assert "[SC1]" not in msgs                       # partition: recap step is SC2's job only
    # missing contract on a proof/derivation scene, enforce=True -> error
    sb2 = {"scenes": [{"id": "p", "kind": "content", "template": "theorem_proof",
                       "ref": "md:nocontract", "covers": []}]}
    errs = coverage.coverage_issues(sb2, {}, enforce=True)
    assert any(sev == "error" and "nocontract" in m and "screen_contract" in m for sev, m in errs)
    # same, enforce=False -> no missing-contract noise (warn-default zero-behavior-change)
    assert not any("screen_contract" in m for _, m in coverage.coverage_issues(sb2, {}, enforce=False))
    # exempt unit -> no missing-contract error even under enforce
    exempt = {"nocontract": SC.parse_block(["  coverage_exempt: true"])}
    assert not any("nocontract" in m for _, m in coverage.coverage_issues(sb2, exempt, enforce=True))


def test_schema_integration():
    import subprocess
    py = sys.executable
    out = subprocess.run(
        [py, "video/pipeline/schema.py", "video/storyboards/_fixtures/sc_coverage.yml"],
        capture_output=True, text=True, encoding="utf-8", errors="replace")
    assert out.returncode == 0, out.stdout + out.stderr   # warn-default never aborts
    assert "[coverage]" in out.stdout
    assert "reduced" in out.stdout                          # SC2 surfaced as warn


def test_non_dict_storyboard():
    from pipeline import step_coverage as coverage
    # A malformed deck (yaml top-level null / scalar / list) must NOT crash the
    # coverage block -- schema_storyboard already reports the schema error; coverage
    # stays quiet (returns []/{}) rather than AttributeError or SC-spam. (Codex R4.)
    c = {"u": {"required_steps": [{"id": "x", "tex": "a"}]}}
    assert coverage.coverage_issues(None, c, enforce=True) == []
    assert coverage.coverage_issues([1, 2], c, enforce=True) == []
    assert coverage.coverage_issues("scalar", c, enforce=False) == []
    assert coverage.covers_by_unit(None) == {}


if __name__ == "__main__":
    test_parse_block()
    test_parser_wiring()
    test_sc1_and_orphan()
    test_sc2_and_missing_contract()
    test_schema_integration()
    test_non_dict_storyboard()
    print("OK coverage self-test")
