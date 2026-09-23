"""Self-test: a ZERO-HEIGHT prose node must not crash sizecheck (code-review-2026-09-23 D2-04).
Run from video/:
    python -m pipeline._selftest_zero_height_prose

value_table's blank cell (a property-comparison table's empty top-left corner) goes through
`brand.prose("")` -> `Tex("")`: height 0, initial_height 0, and still tagged prose. manim's
`font_size` is `height / initial_height / ...`, so reading it raised ZeroDivisionError out of
`_effective_font_px` (floor check) and `_norm_size` (sibling check), past `check_scenes`, and
killed make.py's preflight with a traceback instead of a finding. The run-time twin
(floorprobe._effective_px) already returned None for such a node; the static gate now does too.
"""
from pipeline import _bootstrap

_bootstrap.bootstrap()   # manim + the Plex TeX template -- bootstrap FIRST

from manim import Tex

from pipeline import sizecheck as S
from pipeline.visuals import theme as T


def test_a_zero_height_node_has_no_size():
    node = Tex("")
    assert node.height == 0 and node.initial_height == 0, (node.height, node.initial_height)
    assert S._effective_font_px(node) is None
    assert S._norm_size(node, T.TEXT_SCALE) is None


def test_value_table_with_a_blank_corner_cell_is_checked_not_crashed():
    meta = {"id": "_t", "section": "0.0", "title": "probe"}
    scene = {"id": "blank_corner", "kind": "content", "template": "value_table",
             "accent": "example", "title": "Left and right limits",
             "say": "Compare the two sides. {show row.0} Three against five.",
             "header": ["", "$x\\to 2^-$", "$x\\to 2^+$"],
             "rows": [["$f(x)$", "$3$", "$5$"]]}
    issues = S.check_scenes(meta, [scene])       # raised ZeroDivisionError before the fix
    assert not [m for s, m in issues if s == "error"], issues


if __name__ == "__main__":
    for name in sorted(n for n in dir() if n.startswith("test_")):
        globals()[name]()
        print(f"  ok {name}")
    print("[selftest] zero_height_prose green")
