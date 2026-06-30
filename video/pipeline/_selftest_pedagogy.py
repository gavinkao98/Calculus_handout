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


def test_pedagogy_issues_non_dict_data():
    assert P.pedagogy_issues(None, enforce=False) == []
    assert P.pedagogy_issues([], enforce=False) == []
    # fail-closed on a present-but-null / non-dict `meta` (Plan 2 final-review finding):
    # data.get("meta", {}) returns None when the key exists with a null value.
    assert P.pedagogy_issues({"meta": None}, enforce=True) == []
    assert P.pedagogy_issues({"meta": "x", "scenes": []}, enforce=False) == []
    assert P.assumptions_registry_issues({"meta": None}, enforce=False) == []
    assert P.assumptions_registry_issues({"meta": "x"}, enforce=True) == []


def test_schema_integration():
    import subprocess
    py = sys.executable
    repo_root = Path(__file__).resolve().parent.parent.parent
    out = subprocess.run(
        [py, "video/pipeline/schema.py", "video/storyboards/_fixtures/scaffold.yml"],
        capture_output=True, text=True, cwd=repo_root)
    assert out.returncode == 0                       # warn-default never aborts
    assert "[pedagogy]" in out.stdout
    assert "thm_no_motive" in out.stdout             # PD2
    assert "div_no_problem" in out.stdout            # PD3
    assert "uses_radians" not in out.stdout          # satisfied -> no finding


if __name__ == "__main__":
    test_registry_ok()
    test_registry_absent_is_noop()
    test_registry_findings()
    test_pedagogy_issues()
    test_pedagogy_profile_unknown_is_warn()
    test_pedagogy_issues_non_dict_data()
    test_schema_integration()
    print("OK pedagogy self-test")
