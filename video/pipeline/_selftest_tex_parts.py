"""Self-test: `{{...}}` segments in a math line, `anim: transform` upgraded to part matching,
`anim: cancel` (two-stage elimination) and `frame: true` (the pre-morph frame). KICKOFF-motion-
language-gaps T3-1..T3-3 + T2-2; SPEC-motion-language rules 2 and 3. Run from video/:
    python -m pipeline._selftest_tex_parts

Render-free: the row callables are exercised against a fake scene that records what it was
asked to play (as _selftest_transform / _selftest_pacing do); the segment splitter and the
schema validator are pure string / dict logic.
"""
from pipeline import _bootstrap

_bootstrap.bootstrap()   # derivation imports manim at module level -- bootstrap FIRST

from manim import (Create, FadeOut, MathTex, SurroundingRectangle, TransformMatchingShapes,
                   TransformMatchingTex)

from pipeline import brand
from pipeline import schema as S
from pipeline import texparts
from pipeline.templates import build_blocks
from pipeline.templates import derivation as D
from pipeline.timing import STOCK_ANIM_SECONDS
from pipeline.visuals import theme as T

_META = {"id": "_t", "chapter": "Chapter 9", "section": "9.9", "title": "T", "theme": "midnight"}


# -- the splitter (manim-free; schema counts segments with it) -----------------

def test_segments_follow_manims_double_brace_rule():
    assert texparts.split_segments(r"{{a}} = {{b}}") == ["a", "=", "b"]
    assert texparts.split_segments(r"{{\frac{a}{b}}} + c") == [r"\frac{a}{b}", "+ c"]
    assert texparts.split_segments(r"{{ a }} + {{ b }} = {{ c }}") == ["a", "+", "b", "=", "c"]
    assert texparts.split_segments("a = b") == ["a = b"]
    # manim opens a group only at the start of the string or after whitespace -- so does this
    # (pinned so an author learns to write `{{a}} = {{b}}`, not `{{a}}={{b}}`)
    assert texparts.split_segments(r"{{a}}={{b}}") == ["a", "={{b}}"]
    assert texparts.split_segments(r"x^{{2}} + {{y}}") == ["x^{{2}} +", "y"]
    assert texparts.has_segments(r"{{a}} + b") and not texparts.has_segments(r"a^{{2}}")


def test_segments_match_manims_own_split():
    for s in [r"{{a}} = {{b}}", r"{{a}}={{b}}", r"{{\frac{a}{b}}} + c", r"x^{{2}} + {{y}}",
              r"{{ a }} + {{ b }} = {{ c }}", r"{{a^{b^{c}}}} - {{\{x\}}}", r"\\{{a}} b"]:
        theirs = [p.strip() for p in MathTex._split_double_braces(s) if p.strip()]
        assert texparts.split_segments(s) == theirs, (s, texparts.split_segments(s), theirs)


def test_tokens_match_whole_macros_longest_key_first():
    assert texparts.split_tokens(r"\theta + h", ["h", r"\theta"]) == \
        [(r"\theta", r"\theta"), (" + ", None), ("h", "h")]
    assert texparts.split_tokens(r"\cosh x", ["h"]) == [(r"\cosh x", None)]
    assert texparts.split_tokens(r"d\theta", ["d", r"d\theta"]) == [(r"d\theta", r"d\theta")]
    assert texparts.split_tokens("h", ["h"]) == [("h", "h")]
    assert texparts.split_tokens("abc", []) == [("abc", None)]
    assert texparts.split_tokens("abc", [""]) == [("abc", None)], "an empty key matches nothing"


# -- math_line: one submobject per author segment ----------------------------

def test_a_segmented_line_has_one_submobject_per_segment():
    brand.set_color_map(None)
    m = brand.math_line(r"{{a}} = {{b}}", "dark")
    assert [s.tex_string for s in m.submobjects] == ["a", "=", "b"]
    assert getattr(m, "_ml_parts", False) is True
    plain = brand.math_line("a = b", "dark")
    assert len(plain.submobjects) == 1 and not getattr(plain, "_ml_parts", False)


def test_segments_and_the_colour_table_nest():
    """Colour splits happen INSIDE a segment: the top level is still the author's segments (so
    transform/cancel key on them), the mapped token is a coloured part one level down."""
    brand.set_color_map({"h": "caution"})
    try:
        m = brand.math_line(r"{{\sin(x+h)}} = {{2\cos(x+h/2)}}", "dark")
    finally:
        brand.set_color_map(None)
    assert [s.tex_string for s in m.submobjects] == [r"\sin(x+h)", "=", r"2\cos(x+h/2)"]
    inner = [(p.tex_string, str(p.get_color()).lower()) for p in m.submobjects[0].submobjects
             if hasattr(p, "tex_string")]
    assert ("h", T.color("dark", "caution").lower()) in inner, inner


# -- derivation rows -----------------------------------------------------------

def _spec(*, seg: bool, anim1="transform", frame=False, cancel=None):
    def s(t):
        return t if seg else t.replace("{{", "").replace("}}", "")
    step1 = {"math": s(r"{{\lim_{h\to 0}}} {{\frac{h}{h}}} \cdot {{(1+h)}}"), "reason": "factor",
             "anim": anim1}
    if frame:
        step1["frame"] = True
    if cancel is not None:
        step1["cancel"] = cancel
    return {"id": "der", "kind": "content", "template": "derivation", "accent": "example",
            "title": "T", "say": "A. {show step.0} B. {show step.1} C. {show result} D.",
            "steps": [{"math": s(r"{{\lim_{h\to 0}}} {{\frac{h + h^2}{h}}}"), "reason": "start"},
                      step1],
            "result": {"math": s(r"{{\lim_{h\to 0}}} {{(1+h)}} = 1"), "reason": "done",
                       "anim": "transform"}}


def _blocks(**kw):
    return build_blocks(_spec(**kw), {"ground": "dark", "meta": _META})


def _b(blocks, bid):
    return next(x for x in blocks if x.id == bid)


class _FakeScene:
    def __init__(self):
        self.added, self.played = [], []

    def add(self, *mobs):
        self.added.extend(mobs)

    def play(self, *anims, **kw):
        self.played.append((anims, float(kw.get("run_time") or 0.0)))


def _names(anims):
    return [type(a).__name__ for a in anims]


def test_segments_do_not_move_the_row():
    """Geometry parity: segmentation is a reveal aid, not a layout change."""
    plain, seg = _blocks(seg=False), _blocks(seg=True)
    for bid in ("step.0", "step.1", "result"):
        a, b = _b(plain, bid).mobject, _b(seg, bid).mobject
        assert abs(a.get_left()[0] - b.get_left()[0]) < 1e-6, bid
        assert abs(a.get_center()[1] - b.get_center()[1]) < 1e-6, bid
        assert abs(a.width - b.width) < 1e-6 and abs(a.height - b.height) < 1e-6, bid


def test_transform_matches_parts_when_both_rows_are_segmented():
    block = _b(_blocks(seg=True), "step.1")
    scene = _FakeScene()
    assert block.anim(scene, block.mobject, "dark") == STOCK_ANIM_SECONDS["transform"]
    assert len(scene.played) == 1
    anims, run_time = scene.played[0]
    assert run_time == STOCK_ANIM_SECONDS["transform"]
    assert any(isinstance(a, TransformMatchingTex) for a in anims), _names(anims)
    assert block.anim_seconds == STOCK_ANIM_SECONDS["transform"]


def test_transform_keeps_glyph_matching_when_a_row_is_not_segmented():
    block = _b(_blocks(seg=False), "step.1")
    scene = _FakeScene()
    block.anim(scene, block.mobject, "dark")
    anims, _ = scene.played[0]
    assert any(isinstance(a, TransformMatchingShapes) for a in anims), _names(anims)
    assert not any(isinstance(a, TransformMatchingTex) for a in anims)


def test_cancel_fades_the_named_segments_first_then_morphs_the_survivors():
    blocks = _blocks(seg=True, anim1="cancel", cancel=[1])
    block = _b(blocks, "step.1")
    assert callable(block.anim) and block.anim_seconds == STOCK_ANIM_SECONDS["cancel"] == 1.2
    scene = _FakeScene()
    secs = block.anim(scene, block.mobject, "dark")
    assert secs == STOCK_ANIM_SECONDS["cancel"]
    assert len(scene.played) == 2, _names(scene.played[0][0])
    (first, t1), (second, t2) = scene.played
    assert t1 == D.CANCEL_FADE_SECONDS == 0.4 and abs(t2 - 0.8) < 1e-9, (t1, t2)
    assert any(isinstance(a, FadeOut) for a in first), _names(first)
    assert not any(isinstance(a, (TransformMatchingTex, TransformMatchingShapes)) for a in first)
    assert any(isinstance(a, TransformMatchingTex) for a in second), _names(second)
    # the ghost put on screen is a segmented copy of the previous row, and after stage 1 the
    # cancelled segment is no longer part of it -- so stage 2 morphs only the survivors
    ghost = scene.added[0]
    assert getattr(ghost, "_ml_parts", False)
    assert [s.tex_string for s in ghost.submobjects] == [r"\lim_{h\to 0}"], \
        [s.tex_string for s in ghost.submobjects]


def test_cancel_removes_exactly_the_indexed_segments():
    blocks = _blocks(seg=True, anim1="cancel", cancel=[0])
    block = _b(blocks, "step.1")
    scene = _FakeScene()
    block.anim(scene, block.mobject, "dark")
    assert [s.tex_string for s in scene.added[0].submobjects] == [r"\frac{h + h^2}{h}"]


def test_cancel_on_an_unsegmented_previous_row_degrades_to_transform():
    """schema reports it; at render a plain transform beats an IndexError mid-scene."""
    block = _b(_blocks(seg=False, anim1="cancel", cancel=[1]), "step.1")
    assert block.anim_seconds == STOCK_ANIM_SECONDS["transform"]
    scene = _FakeScene()
    block.anim(scene, block.mobject, "dark")
    assert len(scene.played) == 1
    assert any(isinstance(a, TransformMatchingShapes) for a in scene.played[0][0])


def test_frame_draws_a_rectangle_around_the_previous_row_before_the_morph():
    block = _b(_blocks(seg=True, frame=True), "step.1")
    assert block.anim_seconds == STOCK_ANIM_SECONDS["transform"] + D.FRAME_SECONDS
    scene = _FakeScene()
    secs = block.anim(scene, block.mobject, "dark")
    assert secs == STOCK_ANIM_SECONDS["transform"] + D.FRAME_SECONDS
    assert len(scene.played) == 2
    (first, t1), (second, t2) = scene.played
    assert t1 == D.FRAME_SECONDS == 0.4 and t2 == STOCK_ANIM_SECONDS["transform"]
    creates = [a for a in first if isinstance(a, Create)]
    assert len(creates) == 1 and isinstance(creates[0].mobject, SurroundingRectangle), _names(first)
    rect = creates[0].mobject
    assert str(rect.get_color()).lower() == T.color("dark", "hairline_strong").lower()
    prev_eq = D._eq_core(_b(_blocks(seg=True, frame=True), "step.0").mobject)
    assert rect.width > prev_eq.width and rect.height > prev_eq.height
    assert any(isinstance(a, FadeOut) and a.mobject is rect for a in second), _names(second)


def test_frame_with_cancel_adds_its_seconds_and_a_third_play():
    block = _b(_blocks(seg=True, anim1="cancel", cancel=[1], frame=True), "step.1")
    assert block.anim_seconds == STOCK_ANIM_SECONDS["cancel"] + D.FRAME_SECONDS
    scene = _FakeScene()
    assert abs(block.anim(scene, block.mobject, "dark") - 1.6) < 1e-9
    got = [t for _, t in scene.played]
    assert len(got) == 3 and all(abs(a - b) < 1e-9 for a, b in zip(got, [0.4, 0.4, 0.8])), got


def test_default_rows_are_untouched():
    block = _b(_blocks(seg=True), "step.1")
    scene = _FakeScene()
    block.anim(scene, block.mobject, "dark")
    assert len(scene.played) == 1, "no frame -> exactly the one morph play, as before"
    assert _b(_blocks(seg=False), "step.0").anim == "write"
    assert STOCK_ANIM_SECONDS["transform"] == 1.2


def test_back_compat_lines_accept_cancel_and_frame():
    spec = {"id": "der2", "kind": "content", "template": "derivation", "accent": "example",
            "title": "T", "say": "A. {show line.0} B. {show line.1} C.",
            "lines": [r"{{a}} + {{b}}", {"tex": r"{{a}}", "anim": "cancel", "cancel": [1], "frame": True}]}
    block = _b(build_blocks(spec, {"ground": "dark", "meta": _META}), "line.1")
    assert callable(block.anim) and block.anim_seconds == 1.6


# -- schema --------------------------------------------------------------------

def _errs(scene):
    scene = {"template": "derivation", **scene}
    return [m for sev, m in S._derivation_issues("s1", scene) if sev == "error"]


def test_schema_accepts_a_well_formed_cancel_and_frame():
    assert _errs({"steps": [{"math": "{{a}} + {{b}}"},
                            {"math": "{{a}}", "anim": "cancel", "cancel": [1]}],
                  "result": {"math": "a", "anim": "transform", "frame": True}}) == []
    assert _errs({"lines": ["{{a}} + {{b}}", {"tex": "{{a}}", "anim": "cancel", "cancel": [1]}]}) == []


def test_schema_rejects_an_index_outside_the_previous_row():
    errs = _errs({"steps": [{"math": "{{a}} + {{b}}"}, {"math": "{{a}}", "anim": "cancel", "cancel": [1, 3]}]})
    assert len(errs) == 1 and "cancel[3]" in errs[0] and "3 segment" in errs[0], errs


def test_schema_rejects_cancel_with_no_previous_row_or_an_unsegmented_one():
    errs = _errs({"steps": [{"math": "{{a}}", "anim": "cancel", "cancel": [0]}]})
    assert len(errs) == 1 and "no previous row" in errs[0], errs
    errs = _errs({"steps": [{"math": "a + b"}, {"math": "a", "anim": "cancel", "cancel": [0]}]})
    assert len(errs) == 1 and "{{...}}" in errs[0], errs
    errs = _errs({"result": {"math": "{{a}}", "anim": "cancel", "cancel": [0]}})
    assert len(errs) == 1 and "no previous row" in errs[0], errs


def test_schema_rejects_a_malformed_cancel_list_and_stray_fields():
    errs = _errs({"steps": [{"math": "{{a}} + {{b}}"}, {"math": "a", "anim": "cancel", "cancel": "1"}]})
    assert len(errs) == 1 and "list of segment indexes" in errs[0], errs
    errs = _errs({"steps": [{"math": "{{a}} + {{b}}"}, {"math": "a", "anim": "cancel", "cancel": []}]})
    assert len(errs) == 1 and "list of segment indexes" in errs[0], errs
    errs = _errs({"steps": [{"math": "{{a}} + {{b}}"}, {"math": "a", "anim": "cancel", "cancel": [True]}]})
    assert len(errs) == 1, errs
    errs = _errs({"steps": [{"math": "a"}, {"math": "b", "frame": True}]})
    assert len(errs) == 1 and ".frame" in errs[0], errs
    errs = _errs({"steps": [{"math": "{{a}} + {{b}}"}, {"math": "b", "anim": "transform", "cancel": [0]}]})
    assert len(errs) == 1 and ".cancel" in errs[0] and "anim: cancel" in errs[0], errs


def test_schema_is_silent_for_other_templates_and_plain_rows():
    assert S._derivation_issues("s1", {"template": "graph", "steps": [{"math": "a", "cancel": [0]}]}) == []
    assert _errs({"steps": [{"math": "a"}, {"math": "b", "anim": "transform"}]}) == []


def test_schema_storyboard_carries_the_row_check():
    data = {"meta": {"id": "d", "section": "1.1"},
            "scenes": [{"id": "s", "kind": "content", "template": "derivation",
                        "say": "A {show step.0} B {show step.1}",
                        "steps": [{"math": "{{a}} + {{b}}"},
                                  {"math": "a", "anim": "cancel", "cancel": [5]}]}]}
    assert any(sev == "error" and "cancel[5]" in m for sev, m in S.schema_storyboard(data))


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
