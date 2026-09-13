"""Self-test: `meta.color_map` -- the deck-level variable colour table (SPEC-motion-language
rule 5; KICKOFF-motion-language-gaps T1). Run from video/:
    python -m pipeline._selftest_color_map

Pins four things:
  * schema: the table is validated (mapping, non-empty keys, values are palette roles) at
    warn-default / error under meta.color_map_enforce -- because theme.color() silently falls
    back to `primary` on a role it does not know, a typo would otherwise render as plain ink
    with no other symptom.
  * brand.math_line: a mapped token takes its role colour INSIDE the line -- including inside
    a \\frac argument -- and a key never cuts a macro name (`h` leaves `\\theta` / `\\cosh`
    alone; manim's own tex_to_color_map would split them and LaTeX refuses to compile).
    A split LaTeX rejects falls back to one colour with ONE printed warning, never a crash.
  * _tex_with_map: a MIXED line (words + inline `$math$`, the Tex path -- math_line's mixed
    branch, _prose_lines, heading_rich) colours a mapped token INSIDE its `$...$` span too
    (round17 task B, 2026-09-13), via a dvisvgm colour push/pop special injected into the
    compiled LaTeX rather than manim `*parts` (a `$...$` span can't be cut without unbalancing
    its delimiters). No table, or no token hit in the line -> the old one-colour Tex, byte for
    byte (geometry never moves -- the special is zero-width). A mapped token as an unbraced
    macro argument falls back the same way as _math_tex.
  * plumbing: build_blocks reads the table off ctx["meta"] for every template and a deck
    without one reads an empty table -- no leak from the previous scene.
  * graph: the x/y axis labels take the table, and a plot with no colour of its own whose
    label names a mapped token takes that role (kickoff T1-3).
Zero behaviour change: with no table every path is the old single-colour MathTex/Tex.
"""
from pipeline import _bootstrap

_bootstrap.bootstrap()   # brand / templates import manim at module level -- bootstrap FIRST

import contextlib
import io
from collections import Counter

from manim import MathTex, Tex

from pipeline import brand
from pipeline import schema as S
from pipeline.templates import build_blocks
from pipeline.visuals import theme as T

_META = {"id": "_t", "chapter": "Chapter 9", "section": "9.9", "title": "T", "theme": "midnight"}
_MAP = {r"\sin": "result", "h": "caution", r"\theta": "concept"}


def _hex(mob) -> str:
    """The RENDERED colour: that of the first family member with points. A MathTexPart wrapper
    has no points of its own and keeps manim's default (white) attribute, so reading the
    wrapper would say every un-mapped part is white."""
    pts = mob.family_members_with_points()
    return str((pts[0] if pts else mob).get_color()).lower()


def _c(role: str) -> str:
    return T.color("dark", role).lower()


def _glyph_colors(mob) -> "Counter[str]":
    """Every family member with points, by its own rendered colour -- the granularity a
    mixed line's per-token injected colour needs. Unlike `_leaves` (which walks
    tex_string-tagged parts, one per manim `*parts` cut), a mixed Tex line compiles as ONE
    unsplit string: it has exactly one tex_string-tagged part regardless of how many glyphs
    a colour special painted, so `_leaves` cannot see inside it."""
    return Counter(str(g.get_color()).lower() for g in mob.family_members_with_points())


def _leaves(mob) -> "list[tuple[str, str]]":
    """(tex_string, colour) of every tex-bearing part with no tex-bearing children -- the
    finest level a colour can sit at. A plain MathTex has one leaf (the whole line). A part
    with no glyphs of its own (`\\frac{` -- the bar lands in the closing part) has no colour
    and is skipped."""
    out: list[tuple[str, str]] = []

    def walk(m):
        kids = [s for s in getattr(m, "submobjects", []) if hasattr(s, "tex_string")]
        if kids:
            for k in kids:
                walk(k)
        elif hasattr(m, "tex_string") and m.family_members_with_points():
            out.append((m.tex_string, _hex(m)))
    walk(mob)
    return out


# -- schema ------------------------------------------------------------------

def test_schema_is_silent_without_the_field():
    assert S._color_map_issues({}) == []
    assert S._color_map_issues({"id": "x"}) == []


def test_schema_accepts_a_well_formed_table():
    assert S._color_map_issues({"color_map": _MAP}) == []


def test_schema_warns_on_an_unknown_role_and_names_the_silent_fallback():
    issues = S._color_map_issues({"color_map": {"h": "cautionn"}})
    assert len(issues) == 1 and issues[0][0] == "warn", issues
    msg = issues[0][1]
    assert msg.startswith("meta.color_map['h']"), msg
    assert "not a palette role" in msg and "primary" in msg, msg


def test_schema_enforce_flips_to_error():
    issues = S._color_map_issues({"color_map": {"h": "cautionn"}, "color_map_enforce": True})
    assert [s for s, _ in issues] == ["error"], issues


def test_schema_rejects_a_non_mapping_and_empty_keys_and_missing_roles():
    assert any("mapping" in m for _, m in S._color_map_issues({"color_map": ["h"]}))
    assert any("non-empty" in m for _, m in S._color_map_issues({"color_map": {"": "result"}}))
    assert any("not a palette role" in m for _, m in S._color_map_issues({"color_map": {"h": None}}))


def test_schema_storyboard_carries_the_table_check():
    data = {"meta": {"id": "d", "section": "1.1", "color_map": {"h": "nope"}},
            "scenes": [{"id": "s", "kind": "divider"}]}
    assert any("meta.color_map['h']" in m for _, m in S.schema_storyboard(data))


# -- brand.math_line ---------------------------------------------------------

def test_no_table_is_the_old_single_colour_path():
    brand.set_color_map(None)
    src = r"\frac{\sin(h/2)}{h/2}"
    m = brand.math_line(src, "dark")
    assert isinstance(m, MathTex) and len(m.submobjects) == 1
    assert not getattr(m, "_ml_parts", False)
    assert _leaves(m) == [(src, _c("math"))], _leaves(m)


def test_mapped_tokens_take_their_role_even_inside_a_fraction():
    brand.set_color_map(_MAP)
    try:
        m = brand.math_line(r"\frac{\sin(h/2)}{h/2}", "dark")
    finally:
        brand.set_color_map(None)
    assert len(m.submobjects) == 1, "still ONE line at the top level (pacing walks top-level parts)"
    leaves = _leaves(m)
    by_tex: dict[str, set[str]] = {}
    for tex, col in leaves:
        by_tex.setdefault(tex, set()).add(col)
    assert by_tex[r"\sin"] == {_c("result")}, leaves
    assert by_tex["h"] == {_c("caution")} and sum(1 for t, _ in leaves if t == "h") == 2, leaves
    assert all(col == _c("math") for tex, col in leaves if tex not in (r"\sin", "h")), leaves
    assert not any(r"\theta" in tex for tex, _ in leaves), "an absent key must not split anything"


def test_a_key_never_cuts_a_macro_name():
    """`h` is a substring of `\\theta` and `\\cosh`; manim's tex_to_color_map would cut both and
    LaTeX fails on `\\t...eta` (probe 2026-09-13). Keys match whole tokens here."""
    brand.set_color_map(_MAP)
    try:
        m = brand.math_line(r"\theta + h", "dark")
        n = brand.math_line(r"\cosh x", "dark")
    finally:
        brand.set_color_map(None)
    leaves = dict(_leaves(m))
    assert leaves[r"\theta"] == _c("concept") and leaves["h"] == _c("caution"), leaves
    assert _leaves(n) == [(r"\cosh x", _c("math"))], _leaves(n)


def test_the_dollar_wrapped_form_is_coloured_too():
    brand.set_color_map(_MAP)
    try:
        m = brand.math_line("$h$", "dark", role="text")
    finally:
        brand.set_color_map(None)
    assert isinstance(m, MathTex) and _leaves(m) == [("h", _c("caution"))], _leaves(m)


def test_a_mixed_text_and_math_line_colours_mapped_tokens_inside_its_math_spans():
    """The Tex path (words + inline $math$) cannot be cut into manim `*parts` -- a cut inside
    a `$...$` span leaves the delimiters unbalanced, see `_math_tex` -- so a mapped token's
    colour rides inside the compiled LaTeX as a dvisvgm colour push/pop special
    (`_tex_with_map`, round17 task B). Every OTHER glyph, prose or math, keeps the line's own
    role colour; previously the whole line stayed one colour (superseded 2026-09-13)."""
    brand.set_color_map(_MAP)
    try:
        m = brand.math_line("if $\\theta>0$ then $\\sin\\theta$", "dark", role="text")
    finally:
        brand.set_color_map(None)
    assert isinstance(m, Tex) and not getattr(m, "_ml_parts", False)
    counts = _glyph_colors(m)
    assert counts[_c("concept")] == 2, counts    # the two \theta
    assert counts[_c("result")] == 3, counts     # \sin
    assert counts[_c("text")] == 8, counts       # "if", ">0", "then"


def test_no_table_leaves_a_mixed_line_untouched_and_geometry_never_moves():
    """Zero behaviour change: no meta.color_map, or a table with no token hit in the line, is
    the old single-colour Tex, byte for byte. And even where the table DOES hit, the injected
    special is zero-width (dvisvgm) -- the bounding box never moves, only glyph colour does."""
    src = "if $\\theta>0$ then $\\sin\\theta$"
    brand.set_color_map(None)
    plain = brand.math_line(src, "dark", role="text")
    assert isinstance(plain, Tex) and not getattr(plain, "_ml_parts", False)
    assert set(_glyph_colors(plain)) == {_c("text")}

    brand.set_color_map(_MAP)
    try:
        tinted = brand.math_line(src, "dark", role="text")
        absent = brand.math_line("if $x>0$ then $y$", "dark", role="text")  # no mapped token
    finally:
        brand.set_color_map(None)
    assert (tinted.width, tinted.height) == (plain.width, plain.height), (tinted.width, plain.width)
    assert set(_glyph_colors(absent)) == {_c("text")}


def test_prose_lines_two_line_wrap_matches_geometry_with_and_without_the_table():
    """`_wrap_mixed` decides line breaks from the ORIGINAL text before any colour is injected,
    and the injected specials add no width, so the table changes colour, never the wrap."""
    text = "The angle $\\theta$ grows slowly then $\\sin\\theta$ grows quickly here"
    brand.set_color_map(None)
    plain = brand._prose_lines(text, "dark", "text", "body", 6.0, "LEFT")
    brand.set_color_map(_MAP)
    try:
        tinted = brand._prose_lines(text, "dark", "text", "body", 6.0, "LEFT")
    finally:
        brand.set_color_map(None)
    assert len(plain.submobjects) == len(tinted.submobjects) == 2
    for p, t in zip(plain.submobjects, tinted.submobjects):
        assert (p.width, p.height) == (t.width, t.height)
    counts = _glyph_colors(tinted.submobjects[0])
    assert counts[_c("concept")] == 2 and counts[_c("result")] == 3, counts


def test_a_colour_injected_frac_argument_that_latex_refuses_falls_back_to_one_colour():
    """Same class of failure as `_math_tex`: a mapped token as `\\frac`'s UNBRACED argument
    makes the coloured source refuse to compile (inserting `\\special` before the token
    breaks the single-token argument grab) -- retry the plain source in one colour, warn
    once. Forced with a real case (`h` unbraced) rather than monkeypatching, since the
    injected source, not the *parts split, is what fails here."""
    out = io.StringIO()
    brand.set_color_map(_MAP)
    try:
        with contextlib.redirect_stdout(out):
            m = brand.math_line("the ratio $\\frac h2$ is small", "dark", role="text")
            again = brand.math_line("the ratio $\\frac h2$ is small", "dark", role="text")
    finally:
        brand.set_color_map(None)
    assert isinstance(m, Tex)
    assert set(_glyph_colors(m)) == {_c("text")}
    assert set(_glyph_colors(again)) == {_c("text")}
    lines = [ln for ln in out.getvalue().splitlines() if ln.startswith("[color_map]")]
    assert len(lines) == 1, out.getvalue()
    assert "the ratio $\\frac h2$ is small" in lines[0] and "one colour" in lines[0], lines


def test_a_split_latex_rejects_falls_back_to_one_colour_with_one_warning():
    """Forced deterministically (monkeypatched MathTex refuses any multi-part build) so the
    test does not depend on which tex LaTeX happens to reject today."""
    real = brand.MathTex

    def refusing(*parts, **kw):
        if len(parts) > 1:
            raise ValueError("latex error converting to dvi (forced by selftest)")
        return real(*parts, **kw)

    brand.set_color_map(_MAP)
    brand.MathTex = refusing
    out = io.StringIO()
    try:
        with contextlib.redirect_stdout(out):
            m = brand.math_line(r"\sin h", "dark")
            again = brand.math_line(r"\sin h", "dark")
    finally:
        brand.MathTex = real
        brand.set_color_map(None)
    assert _leaves(m) == [(r"\sin h", _c("math"))], _leaves(m)
    assert _leaves(again) == _leaves(m)
    lines = [ln for ln in out.getvalue().splitlines() if ln.startswith("[color_map]")]
    assert len(lines) == 1, out.getvalue()
    assert r"\sin h" in lines[0] and "one colour" in lines[0], lines


# -- plumbing: build_blocks sets the table from meta ---------------------------

def _derivation_spec():
    return {"id": "der", "kind": "content", "template": "derivation", "accent": "derivation",
            "title": "T", "say": "A. {show step.0} B. {show result} C.",
            "steps": [{"math": r"\sin(\theta+h) - \sin\theta", "reason": "numerator"}],
            "result": {"math": r"\cos\theta", "reason": "limit"}}


def _eq_leaves(blocks, bid):
    from pipeline.templates.derivation import _eq_core
    return _leaves(_eq_core(next(b for b in blocks if b.id == bid).mobject))


def test_build_blocks_reads_the_table_from_meta_and_does_not_leak():
    tinted = build_blocks(_derivation_spec(), {"ground": "dark", "meta": {**_META, "color_map": _MAP}})
    leaves = _eq_leaves(tinted, "step.0")
    assert (r"\theta", _c("concept")) in leaves and ("h", _c("caution")) in leaves, leaves
    assert (r"\sin", _c("result")) in leaves, leaves
    # the result row keeps its own role for the un-mapped glyphs and tints the mapped ones
    res = dict(_eq_leaves(tinted, "result"))
    assert res[r"\theta"] == _c("concept") and res[r"\cos"] == _c("result"), res

    plain = build_blocks(_derivation_spec(), {"ground": "dark", "meta": _META})
    assert _eq_leaves(plain, "step.0") == [(r"\sin(\theta+h) - \sin\theta", _c("primary"))]
    assert brand._COLOR_MAP == {}, "a deck without a table must leave no table behind"


# -- graph: axis labels + plot default role from its label --------------------

def _graph_spec():
    return {"id": "g", "kind": "content", "template": "graph", "accent": "derivation", "title": "G",
            "say": "A. {show plot.0} B. {show plot.1} C.",
            "axes": {"x_range": [-3.5, 3.5, 1], "y_range": [-1.4, 1.4, 0.5]},
            "plots": [{"kind": "function", "expression": "sin(x)", "x_range": [-3.3, 3.3],
                       "label": "$y=\\sin x$", "reveal": True},
                      {"kind": "function", "expression": "cos(x)", "x_range": [-3.3, 3.3],
                       "label": "$\\cos x$", "color_role": "secondary", "reveal": True}]}


def test_graph_axis_labels_and_unlabelled_plot_colour_follow_the_table():
    cmap = {"x": "practice", r"\sin": "result"}
    blocks = build_blocks(_graph_spec(), {"ground": "dark", "meta": {**_META, "color_map": cmap}})
    axes = next(b for b in blocks if b.id == "axes").mobject
    x_lab, y_lab = [s for s in axes.submobjects if isinstance(s, MathTex)][-2:]
    assert _leaves(x_lab) == [("x", _c("practice"))], _leaves(x_lab)
    assert _leaves(y_lab) == [("y", _c("text"))], _leaves(y_lab)

    plot0 = next(b for b in blocks if b.id == "plot.0").mobject     # VGroup(glow, curve, label)
    curve0 = plot0.submobjects[1]
    assert _hex(curve0) == _c("result"), "no color_role + a label naming \\sin -> sine's role"
    label0 = plot0.submobjects[2]
    leaves0 = dict(_leaves(label0))
    assert leaves0[r"\sin"] == _c("result") and leaves0["x"] == _c("practice"), leaves0

    plot1 = next(b for b in blocks if b.id == "plot.1").mobject
    assert _hex(plot1.submobjects[1]) == _c("secondary"), "an explicit color_role is untouched"


def test_graph_without_a_table_is_unchanged():
    blocks = build_blocks(_graph_spec(), {"ground": "dark", "meta": _META})
    axes = next(b for b in blocks if b.id == "axes").mobject
    x_lab, _ = [s for s in axes.submobjects if isinstance(s, MathTex)][-2:]
    assert _leaves(x_lab) == [("x", _c("text"))]
    plot0 = next(b for b in blocks if b.id == "plot.0").mobject
    assert _hex(plot0.submobjects[1]) == _c("secondary")


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
