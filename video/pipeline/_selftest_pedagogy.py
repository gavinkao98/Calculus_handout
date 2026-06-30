"""Stdlib assert self-test for pedagogy.py. Run: python video/pipeline/_selftest_pedagogy.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline import pedagogy as P  # noqa: E402


def test_registry_ok():
    data = {"meta": {"assumptions": [
        {"id": "radians", "text": "$\\theta$ in radians", "first_use_unit": "u1", "source": "doc:frag-sec-3-1"},
    ]}, "scenes": [{"id": "u1", "kind": "content", "scaffold": {"flag": "radians"}}]}
    assert P.assumptions_registry_issues(data, enforce=False) == []


def test_registry_absent_is_noop():
    assert P.assumptions_registry_issues({"meta": {}, "scenes": []}, enforce=False) == []


def test_registry_findings():
    data = {"meta": {"assumptions": [
        {"id": "radians", "text": "x", "first_use_unit": "missing", "source": "s"},   # unit not found
        {"id": "noflag", "text": "x", "first_use_unit": "u2", "source": "s"},          # scene lacks flag
        {"id": "blank", "text": "", "first_use_unit": "u2", "source": "s"},            # empty text
    ]}, "scenes": [
        {"id": "u2", "kind": "content"},                                               # no scaffold.flag
        {"id": "u3", "kind": "content", "scaffold": {"flag": "orphan"}},               # orphan flag
    ]}
    warns = P.assumptions_registry_issues(data, enforce=False)
    msgs = " | ".join(m for _, m in warns)
    assert all(s == "warn" for s, _ in warns)
    assert "missing" in msgs            # first_use_unit not a scene id
    assert "u2" in msgs                 # scene lacks required flag
    assert "blank" in msgs              # empty text field
    assert "orphan" in msgs             # orphan flag has no registry entry
    errs = P.assumptions_registry_issues(data, enforce=True)
    assert all(s == "error" for s, _ in errs)
    assert len(errs) == len(warns)


def test_pedagogy_issues():
    data = {"meta": {"pedagogy_profile": "first_time"}, "scenes": [
        {"id": "thm", "kind": "content", "template": "theorem_proof"},          # missing motive
        {"id": "der", "kind": "content", "template": "derivation",
         "scaffold": {"motive": "why"}},                                         # ok
        {"id": "def", "kind": "content", "template": "definition_math"},         # exempt (not deterministic)
        {"id": "div", "kind": "divider"},                                        # missing problem
    ]}
    warns = P.pedagogy_issues(data, enforce=False)
    msgs = " | ".join(m for _, m in warns)
    assert "thm" in msgs and "scaffold.motive" in msgs    # PD2 fires
    assert "div" in msgs and "scaffold.problem" in msgs   # PD3 fires
    assert "der:" not in msgs and "def:" not in msgs       # has motive / exempt (colon-suffix avoids substring hit on "divider")
    assert all(s == "warn" for s, _ in warns)
    errs = P.pedagogy_issues(data, enforce=True)
    assert all(s == "error" for s, _ in errs)

def test_pedagogy_profile_unknown_is_warn():
    data = {"meta": {"pedagogy_profile": "nonsense"}, "scenes": []}
    out = P.pedagogy_issues(data, enforce=True)   # even enforced, profile note stays warn
    assert any(s == "warn" and "pedagogy_profile" in m for s, m in out)


if __name__ == "__main__":
    test_registry_ok()
    test_registry_absent_is_noop()
    test_registry_findings()
    test_pedagogy_issues()
    test_pedagogy_profile_unknown_is_warn()
    print("OK pedagogy self-test")
