"""schema.py wiring of the pedagogy (PD) checker, over video/storyboards/_fixtures/scaffold.yml.

Split out of video/pipeline/_selftest_pedagogy.py on 2026-09-28, when schema.py moved here with
the Manim engine and the content-layer checker (pedagogy.py) plus its fixture stayed in video/
(see video/KICKOFF-remotion-unification.md). Code unchanged: paths are the pre-archive video/
layout -- checkout tag archive/2026-09-28-manim-gen2-final to run it.
"""
import sys
from pathlib import Path


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
    test_schema_integration()
    print("OK pedagogy schema-integration self-test")
