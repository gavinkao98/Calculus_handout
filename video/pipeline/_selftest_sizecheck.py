"""Stdlib assert self-test for sizecheck.py floor logic. Run: .venv/Scripts/python.exe video/pipeline/_selftest_sizecheck.py
Render-free (imports manim via sizecheck/brand, but renders nothing)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline import sizecheck as S          # noqa: E402
from pipeline.visuals import theme as T      # noqa: E402
from manim import MathTex, Tex               # noqa: E402


def test_effective_px_recovers_authored_size():
    # a text Tex authored at 26px renders at fs(26)*TEXT_SCALE; recover -> ~26
    text = Tex("x"); text.font_size = 26 * T.PX_TO_FS * T.TEXT_SCALE
    assert abs(S._effective_font_px(text) - 26.0) < 0.5
    # a MathTex authored at 40px renders at fs(40) (no TEXT_SCALE); recover -> ~40
    math = MathTex("x"); math.font_size = 40 * T.PX_TO_FS
    assert abs(S._effective_font_px(math) - 40.0) < 0.5


def test_floor_findings_flags_below():
    sizes = [("reason.0", 22.0), ("reason.1", 26.0), ("statement", 40.0)]  # only reason.0 < 26
    warns = S._floor_findings("sc", sizes, 26.0, enforce=False)
    msgs = " | ".join(m for _, m in warns)
    assert all(s == "warn" for s, _ in warns) and len(warns) == 1
    assert "reason.0" in msgs and "sc" in msgs
    assert "reason.1" not in msgs and "statement" not in msgs   # at/above floor pass


def test_floor_findings_enforce_is_error():
    errs = S._floor_findings("sc", [("a", 10.0)], 26.0, enforce=True)
    assert errs and all(s == "error" for s, _ in errs)


def test_floor_findings_empty_when_all_pass():
    assert S._floor_findings("sc", [("a", 26.0), ("b", 99.0)], 26.0, enforce=False) == []


def test_floor_uses_theme_constant():
    assert isinstance(T.MIN_FONT_FLOOR, float) and T.MIN_FONT_FLOOR > 0


if __name__ == "__main__":
    test_effective_px_recovers_authored_size()
    test_floor_findings_flags_below()
    test_floor_findings_enforce_is_error()
    test_floor_findings_empty_when_all_pass()
    test_floor_uses_theme_constant()
    print("OK sizecheck self-test")
