"""Self-test: value_table cells -- the accent column/row ink (code review 2026-09-23 D2-01).

Run from video/:  python -m pipeline._selftest_value_table

D2-01: the punchline column/row is tinted in the SCENE's accent -- the background tint via
`T.color(ground, role)`, the cells via the matching lifted ink `f"{role}_ink"` (DESIGN
catalog: "punchline 欄／列鋪 scene accent 同色 tint + 抬升 ink"). The ink used to come from a
private map keyed by the pre-Direction-B role names (secondary/accent/success/warning);
`accent_role()` now only returns semantic roles, so every accent missed the map and every
accent cell fell back to blue_ink -- a green `example` column carried blue numbers.

D2-05: a cell routes like every author field (brand.prose): a whole-cell single `$...$` is
display math at the math anchor (unchanged), plain words are text, and MIXED words + inline
`$math$` are text too -- at the text scale. `_cell` used to send anything with a `$` to
math_line, whose mixed branch sets the line at the math anchor WITHOUT TEXT_SCALE, so
"exists at $x=2$" came out at 1/1.2748 = 78% of the "exists" cell above it, with no prose
tag for the sibling / floor gates to measure.
"""
from pipeline import _bootstrap

_bootstrap.bootstrap()   # templates import manim at module level -- bootstrap FIRST (repo rule)

from pipeline.blocks import ACCENT_ROLE, accent_role   # noqa: E402
from pipeline.templates import build_blocks            # noqa: E402
from pipeline.visuals import theme as T                # noqa: E402

_META = {"id": "_t", "chapter": "Chapter 9", "section": "9.9", "title": "T", "theme": "midnight"}


def _hex(mob) -> str:
    """The RENDERED colour: that of the first family member with points."""
    pts = mob.family_members_with_points()
    return str((pts[0] if pts else mob).get_color()).lower()


def _table(**extra) -> dict:
    return {"id": "vt", "kind": "content", "template": "value_table", "title": "A Table",
            "say": "Look. {show row.0} {show row.1}",
            "header": ["$x$", "$f(x)$", "$g(x)$"],
            "rows": [["$1$", "$2$", "$3$"], ["$4$", "$5$", "$6$"]], **extra}


def _blocks(spec):
    return {b.id: b for b in build_blocks(spec, {"ground": "dark", "meta": _META})}


def test_accent_col_cells_take_the_scene_accent_ink():
    """Every accent value: the accent column's cells are `<role>_ink`, the same hue as the
    column's tint -- never the old blue_ink fallback."""
    for accent in sorted(ACCENT_ROLE):
        spec = _table(accent=accent, accent_col=2)
        role = accent_role(spec)
        by = _blocks(spec)
        want = T.color("dark", f"{role}_ink").lower()
        for rid in ("row.0", "row.1"):
            got = _hex(by[rid].mobject[2])
            assert got == want, f"accent={accent} ({role}) {rid} accent cell {got} != {role}_ink {want}"
        assert _hex(by["header"].mobject[2]) == want, f"accent={accent}: header accent cell"
        tint = by["col_tint"].mobject.get_fill_color().to_hex().lower()
        assert tint == T.color("dark", role).lower(), (accent, tint)


def test_accent_row_cells_take_the_scene_accent_ink():
    spec = _table(accent="example", accent_row=1)
    by = _blocks(spec)
    want = T.color("dark", "practice_ink").lower()
    for j in range(3):
        assert _hex(by["row.1"].mobject[j]) == want, j
    assert _hex(by["row.0"].mobject[2]) != want   # an ordinary body cell is untouched


def test_ch01_when_inversion_fails_accent_column_is_practice_green():
    """The live case the review found: `accent: example` -> practice, col 2 tinted green but
    its cells were blue."""
    spec = _table(accent="example", accent_col=2)
    by = _blocks(spec)
    assert _hex(by["row.0"].mobject[2]) == T.color("dark", "practice_ink").lower()
    assert _hex(by["row.0"].mobject[2]) != T.color("dark", "blue_ink").lower()


def _property_table() -> dict:
    """value_table's own docstring use case: a property comparison with a mixed cell."""
    return _table(accent="theorem", header=["side", "value", "limit"],
                  rows=[["left", "$3$", "exists"], ["right", "$5$", "exists at $x=2$"]])


def test_mixed_text_and_math_cell_renders_at_the_plain_text_cell_size():
    by = _blocks(_property_table())
    plain = by["row.0"].mobject[2]           # "exists"
    mixed = by["row.1"].mobject[2]           # "exists at $x=2$"
    assert abs(float(mixed.font_size) - float(plain.font_size)) < 1e-6, (
        f"mixed cell font_size {float(mixed.font_size):.2f} != plain {float(plain.font_size):.2f}")
    # prose-tagged, so sizecheck's sibling / floor gates can see it
    assert getattr(mixed, "_brand_prose", False), "mixed cell carries no brand.prose tag"


def test_whole_math_cell_keeps_the_math_anchor_size():
    """The pure `$...$` cell path is unchanged: display MathTex at T.fs(size)."""
    by = _blocks(_property_table())
    math_cell = by["row.0"].mobject[1]       # "$3$"
    assert abs(float(math_cell.font_size) - T.fs("prose")) < 1e-6, float(math_cell.font_size)
    head = by["header"].mobject[1]           # "value" (plain header, prose_sm)
    assert abs(float(head.font_size) - T.fs("prose_sm") * T.TEXT_SCALE) < 1e-6


if __name__ == "__main__":
    import sys
    import traceback
    fails = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"PASS {name}")
            except Exception:
                fails += 1
                print(f"FAIL {name}")
                traceback.print_exc()
    sys.exit(1 if fails else 0)
