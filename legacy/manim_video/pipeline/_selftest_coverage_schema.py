"""schema.py wiring of the SC step-coverage checker, over video/storyboards/_fixtures/sc_coverage.yml.

Split out of video/pipeline/_selftest_coverage.py on 2026-09-28, when schema.py moved here with
the Manim engine and the content-layer checker (step_coverage.py) plus its fixture stayed in
video/ (see video/KICKOFF-remotion-unification.md). Code unchanged: paths are the pre-archive
video/ layout -- checkout tag archive/2026-09-28-manim-gen2-final to run it.
"""
import sys
from pathlib import Path


def test_schema_integration():
    import subprocess
    py = sys.executable
    repo_root = Path(__file__).resolve().parent.parent.parent   # cwd-independent (run_selftests.py runs from video/)
    out = subprocess.run(
        [py, "video/pipeline/schema.py", "video/storyboards/_fixtures/sc_coverage.yml"],
        capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=repo_root)
    assert out.returncode == 0, out.stdout + out.stderr   # warn-default never aborts
    assert "[coverage]" in out.stdout
    assert "reduced" in out.stdout                          # SC2 surfaced as warn


if __name__ == "__main__":
    test_schema_integration()
    print("OK coverage schema-integration self-test")
