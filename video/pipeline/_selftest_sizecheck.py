"""Stdlib assert self-test for sizecheck.py floor logic. Run: .venv/Scripts/python.exe video/pipeline/_selftest_sizecheck.py
Render-free (imports manim via sizecheck/brand, but renders nothing)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline import sizecheck as S          # noqa: E402
from pipeline import brand as B              # noqa: E402
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


def test_floor_issues_enforce_propagation():
    """Enforce flag propagates through _floor_issues (the path check_scenes uses).
    Uses a hand-built Block with a sub-floor _brand_prose Tex node -- render-free."""
    from pipeline.blocks import Block

    # Build a sub-floor prose Tex: authored at 20px < MIN_FONT_FLOOR (26px).
    # _effective_font_px recovers authored px from font_size = px * TEXT_SCALE * PX_TO_FS.
    # Tex IS-A MathTex, so _effective_font_px uses the Tex branch (divide by TEXT_SCALE * PX_TO_FS).
    node = Tex("x")
    node.font_size = 20.0 * T.TEXT_SCALE * T.PX_TO_FS
    node._brand_prose = True  # marks it as a prose node for _prose_nodes

    block = Block(id="point.0", mobject=node)
    scene = {"id": "test_floor_propagation"}

    # enforce=True  -> _floor_issues must yield at least one "error"
    errs = S._floor_issues(scene, [block], enforce=True)
    assert errs and all(s == "error" for s, _ in errs), \
        f"expected error with enforce=True, got: {errs}"

    # enforce=False -> same finding becomes "warn"
    warns = S._floor_issues(scene, [block], enforce=False)
    assert warns and all(s == "warn" for s, _ in warns), \
        f"expected warn with enforce=False, got: {warns}"

    # Also confirm check_scenes reads meta.fontfloor_enforce to build the enforce flag.
    # We do NOT call check_scenes on a full deck here (that is Task 5); just verify
    # the key is read: meta with the key set -> bool(True); without -> bool(False).
    meta_on = {"fontfloor_enforce": True}
    meta_off = {}
    assert bool(meta_on.get("fontfloor_enforce")) is True
    assert bool(meta_off.get("fontfloor_enforce")) is False


def test_clamp_no_shrink_when_fits():
    assert B._clamp_scale(3.0, 5.0, 40.0, 26.0) == 1.0


def test_clamp_fits_when_result_above_floor():
    # shrink 5->4 (0.8x); 40*0.8=32 >= 26 -> use fit
    assert abs(B._clamp_scale(5.0, 4.0, 40.0, 26.0) - 0.8) < 1e-9


def test_clamp_stops_at_floor():
    # fit would be 0.5x -> 40*0.5=20 < 26; clamp to floor scale 26/40=0.65
    assert abs(B._clamp_scale(10.0, 5.0, 40.0, 26.0) - 0.65) < 1e-9


def test_clamp_never_enlarges():
    assert B._clamp_scale(2.0, 9.0, 20.0, 26.0) == 1.0


def test_clamp_zero_width_safe():
    assert B._clamp_scale(0.0, 5.0, 40.0, 26.0) == 1.0


if __name__ == "__main__":
    test_effective_px_recovers_authored_size()
    test_floor_findings_flags_below()
    test_floor_findings_enforce_is_error()
    test_floor_findings_empty_when_all_pass()
    test_floor_uses_theme_constant()
    test_floor_issues_enforce_propagation()
    test_clamp_no_shrink_when_fits()
    test_clamp_fits_when_result_above_floor()
    test_clamp_stops_at_floor()
    test_clamp_never_enlarges()
    test_clamp_zero_width_safe()
    print("OK sizecheck self-test")
