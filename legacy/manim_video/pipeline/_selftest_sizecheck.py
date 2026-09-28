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


def test_show_cross_check_flags_missing_target():   # T5 / F9: {show} target vs built block ids
    meta = {"id": "demo", "section": "0.0", "title": "T", "chapter": "0", "sections": []}
    bad = {"id": "xcheck", "kind": "content", "template": "definition_math",
           "accent": "definition", "title": "T", "statement": "A statement.",
           "math": ["a = b", "c = d"],                        # -> blocks math.0, math.1
           "say": "one {show math.0} two {show math.9} three"}   # math.9 has NO block
    xerrs = [m for s, m in S.check_scenes(meta, [bad])
             if s == "error" and "no matching block" in m]
    assert len(xerrs) == 1 and "math.9" in xerrs[0], xerrs
    good = {**bad, "say": "one {show math.0} two {show math.1} three"}   # all targets exist
    xerrs2 = [m for s, m in S.check_scenes(meta, [good])
              if s == "error" and "no matching block" in m]
    assert xerrs2 == [], xerrs2


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


def test_clamp_cur_size_nonpositive_uses_fit():
    # cur_size<=0 -> floor_scale falls back to fit -> just the fit factor
    assert abs(B._clamp_scale(10.0, 5.0, 0.0, 26.0) - 0.5) < 1e-9


def test_clamp_none_max_w_safe():
    assert B._clamp_scale(5.0, None, 40.0, 26.0) == 1.0


def test_floor_findings_tolerates_clamp_boundary():
    # a node the clamp held AT the floor recovers to 26 - ~1e-14 (build drift); must NOT warn
    assert S._floor_findings("sc", [("held", 26.0 - 1e-14)], 26.0, enforce=False) == []
    # genuinely-too-small text still fires (1px below floor is far past the tolerance)
    flagged = S._floor_findings("sc", [("tiny", 25.0)], 26.0, enforce=False)
    assert len(flagged) == 1 and "tiny" in flagged[0][1]


def _rect_at(bottom: float, top: float, width: float = 2.0):
    """A Rectangle whose bounding box is exactly [bottom, top] in y -- render-free
    geometry for the G3 sparse-union tests below (no Tex build needed)."""
    from manim import Rectangle

    h = top - bottom
    r = Rectangle(width=width, height=h)
    r.move_to([0.0, bottom + h / 2.0, 0.0])
    return r


def test_sparse_single_block_warns():
    """G3 pure sparse: a lone small `body` block in an otherwise-empty zone still warns
    (the common case this check exists for, unchanged by the union rewrite)."""
    from pipeline.blocks import Block

    title_bottom = 2.0
    title = _rect_at(title_bottom, title_bottom + 0.01, width=1.0)
    zone_top = title_bottom - T.TITLE_GAP
    body = _rect_at(zone_top - 0.3, zone_top)   # a thin top-anchored slice
    scene = {"id": "sparse_probe", "template": "callout", "body": "x"}
    warns = S._sparse_issues(scene, [Block(id="title", mobject=title),
                                     Block(id="body", mobject=body)])
    assert len(warns) == 1 and "single-block fill" in warns[0][1] and "sparse_probe" in warns[0][1]


def test_sparse_silent_when_graph_block_fills_zone():
    """G3 measurement blind spot (hook-13-degrees): a hook's `layer: graph` block filling
    the rest of the zone below a small `body` must silence the advisory -- the fix measures
    the UNION of body+graph, not `body` alone."""
    from pipeline.blocks import Block

    title_bottom = 2.0
    title = _rect_at(title_bottom, title_bottom + 0.01, width=1.0)
    zone_top = title_bottom - T.TITLE_GAP
    zone_bottom = -T.FRAME_H / 2 + T.SAFE_MARGIN
    body = _rect_at(zone_top - 0.3, zone_top)                 # same thin slice as above
    fig = _rect_at(zone_bottom, zone_top - 0.3, width=4.0)    # fills the rest of the zone
    scene = {"id": "graph_fill_probe", "template": "callout", "body": "x"}
    blocks = [Block(id="title", mobject=title), Block(id="body", mobject=body),
              Block(id="degfig", mobject=fig, layer="graph")]
    assert S._sparse_issues(scene, blocks) == []


def test_sparse_ok_still_acks():
    """`sparse_ok: true` still short-circuits the advisory outright, unchanged."""
    from pipeline.blocks import Block

    title = _rect_at(2.0, 2.01, width=1.0)
    body = _rect_at(-0.05, 0.05)   # tiny -- would warn without the ack
    scene = {"id": "acked", "template": "callout", "body": "x", "sparse_ok": True}
    blocks = [Block(id="title", mobject=title), Block(id="body", mobject=body)]
    assert S._sparse_issues(scene, blocks) == []


def test_sibling_prose_size_mismatch_is_caught():
    """r2 Task J: `carriers`'s `isinstance(n, Tex) and not isinstance(n, MathTex)` clause
    is dead in this manim version -- `Tex` SUBCLASSES `MathTex` (tex_mobject.py:607, the
    same order trap floorprobe._effective_px's docstring documents), so that clause is
    always False; Route A also ended manim `Text` output entirely (brand.py never imports
    it), so `carriers` was permanently [] and the sibling gate a silent no-op since Route A
    landed. Proves it fires again: two point.* siblings, one a Route-A body_text Tex
    scaled down well past TOLERANCE (the 'shrunk not wrapped' anti-pattern this gate
    exists to catch), must trip the 'different sizes' error."""
    from pipeline.blocks import Block
    import pipeline.templates as templates_mod

    from manim import DOWN

    def carrier(px, shift=0.0):
        node = Tex("hello")
        node.font_size = px * T.PX_TO_FS * T.TEXT_SCALE
        node._brand_prose = True
        if shift:
            node.shift(shift * DOWN)
        return node

    blocks = [Block(id="point.0", mobject=carrier(38.0)),
              Block(id="point.1", mobject=carrier(20.0, shift=1.0))]   # ratio 1.9x >> TOLERANCE 1.06x

    orig = templates_mod.build_blocks
    templates_mod.build_blocks = lambda scene, ctx: blocks
    try:
        meta = {"id": "demo", "chapter": "0", "section": "0.0", "title": "T", "sections": []}
        issues = S.check_scenes(meta, [{"id": "sib", "kind": "content"}])
    finally:
        templates_mod.build_blocks = orig

    errs = [m for sev, m in issues if sev == "error" and "different sizes" in m]
    assert len(errs) == 1 and "'point' siblings" in errs[0], issues


def test_pure_mathtex_sibling_is_not_a_carrier():
    """A prose line that is nothing but inline math (brand.math_line, e.g. a reason rail
    "$h(0)=h(2)=0$") is tagged _brand_prose like every other prose output but renders as
    a bare MathTex, not a Tex -- _norm_size's TEX_TEXT_SCALE relation does not apply to it
    (brand._compose x-height-matches it separately, per _block_prose_size's own docstring),
    so it must stay excluded from `carriers` even after the isinstance fix: two such nodes
    at wildly different font_size must not manufacture a sibling finding."""
    node_a = MathTex("x")
    node_a.font_size = 40.0 * T.PX_TO_FS
    node_a._brand_prose = True
    node_b = MathTex("y")
    node_b.font_size = 20.0 * T.PX_TO_FS
    node_b._brand_prose = True
    assert S._block_prose_size(node_a, T.TEXT_SCALE) is None
    assert S._block_prose_size(node_b, T.TEXT_SCALE) is None


if __name__ == "__main__":
    test_effective_px_recovers_authored_size()
    test_floor_findings_flags_below()
    test_floor_findings_enforce_is_error()
    test_floor_findings_empty_when_all_pass()
    test_floor_uses_theme_constant()
    test_floor_issues_enforce_propagation()
    test_show_cross_check_flags_missing_target()
    test_clamp_no_shrink_when_fits()
    test_clamp_fits_when_result_above_floor()
    test_clamp_stops_at_floor()
    test_clamp_never_enlarges()
    test_clamp_zero_width_safe()
    test_clamp_cur_size_nonpositive_uses_fit()
    test_clamp_none_max_w_safe()
    test_floor_findings_tolerates_clamp_boundary()
    test_sparse_single_block_warns()
    test_sparse_silent_when_graph_block_fills_zone()
    test_sparse_ok_still_acks()
    test_sibling_prose_size_mismatch_is_caught()
    test_pure_mathtex_sibling_is_not_a_carrier()
    print("OK sizecheck self-test")
