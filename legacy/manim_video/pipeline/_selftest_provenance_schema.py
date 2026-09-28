"""schema.py wiring of the OTF provenance checker, over video/storyboards/_fixtures/otf_provenance.yml.

Split out of video/pipeline/_selftest_provenance.py on 2026-09-28, when schema.py moved here with
the Manim engine and the content-layer checker (provenance.py) plus its fixture stayed in video/
(see video/KICKOFF-remotion-unification.md). Code unchanged: paths are the pre-archive video/
layout -- checkout tag archive/2026-09-28-manim-gen2-final to run it.
"""
import sys
from pathlib import Path


def test_schema_integration():
    import subprocess
    py = sys.executable
    repo_root = Path(__file__).resolve().parent.parent.parent   # video/pipeline/_selftest_provenance.py -> repo root
    out = subprocess.run(
        [py, "video/pipeline/schema.py", "video/storyboards/_fixtures/otf_provenance.yml"],
        capture_output=True, text=True, cwd=repo_root)
    assert out.returncode == 0                      # warn-default never aborts
    assert "[provenance]" in out.stdout
    assert "bad_missing.statement" in out.stdout
    assert "bad_unresolvable.statement" in out.stdout
    assert "bad_divider.problem" in out.stdout         # Fix 2: divider kind produces finding
    assert "bad_nested_reason.steps.0.reason" in out.stdout   # Codex follow-up: nested reason scanned
    # Scope the negatives to the provenance-finding form `<id>.<field>` (matches the
    # positives above): bare `ok_inherited`/`intro` also surface in the [pedagogy] block,
    # which shares stdout since Task 3 wired it in -- the provenance form stays absent
    # (ok_inherited resolves via md:unit_a; intro is exempt).
    assert "ok_inherited.statement" not in out.stdout and "intro.statement" not in out.stdout


# NOTE: make.py provenance wiring is verified manually (see verification step 2/3 in
# SP1 Plan 1 task-6-fixes-report.md). A permanent automated test is omitted because
# running the fixture through make.py exits at the sizecheck gate (the minimal fixture
# lacks complete scene templates), making the subprocess nondeterministic. The logic
# guard is test_schema_integration (schema.py standalone), which mirrors the proven
# make.py block verbatim. The make.py block is a direct copy -- if one regresses the
# other will catch it.


if __name__ == "__main__":
    test_schema_integration()
    print("OK provenance schema-integration self-test")
