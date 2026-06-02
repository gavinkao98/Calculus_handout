"""Brand visual primitives for Direction B (Blueprint Grid).

Builds the recurring design elements templates compose. Colours come from the
active ground's palette (light/dark) via theme.py -- no hex literals here.

Key helper: wrap_text() greedily wraps a string to a max width by inserting
newlines ONLY at spaces, so words never break mid-glyph (the recurring bug).
"""
from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Line,
    MathTex,
    Polygon,
    RoundedRectangle,
    SVGMobject,
    Tex,
    Text,
    VGroup,
)

from .visuals import theme as T

FRAME_W = T.FRAME_W
FRAME_H = T.FRAME_H
_BRAND = (
    Path(__file__).resolve().parents[1]
    / "design_handoff" / "from_designer" / "handoff" / "source" / "assets" / "brand"
)


# -- text wrapping (never breaks a word) ----------------------------------
#
# Width is ESTIMATED from character count, not measured by building a Text.
# The old approach created a throwaway Text per trial word-combination to read
# its .width; under disable_caching those measurement SVGs intermittently came
# out empty -> "ParseError: no element found". The estimate removes that whole
# class of failure (and is much faster -- no SVG per trial).
#
# Calibration (manim units per char*font_size), measured with CMU Serif:
#   "Inverse fx 0123"       (15 latin) @ fs48 -> width 4.336 => K = 0.00602
#   "Distinct outputs always." (24)    @ fs23 -> width 3.400 => K = 0.00616
#   "Testing with Algebra"  (20 latin) @ fs45 -> width 5.686 => K = 0.00632
# CJK glyphs are full-width, so they count as ~2x a latin advance.
# Upper bound of measurements is 0.00632; use 0.0064 as a small safety margin
# (overflow is worse than a slightly short line).

_WIDTH_K = 0.0064


def _char_weight(ch: str) -> float:
    """Approx advance weight: CJK/full-width ~2x a latin char, spaces ~0.5."""
    if ch == " ":
        return 0.5
    return 2.0 if ord(ch) >= 0x2E80 else 1.0


def estimate_text_width(text: str, font_size: float) -> float:
    """Estimated rendered width in manim units (no Text/SVG created)."""
    weighted = sum(_char_weight(c) for c in text)
    return weighted * font_size * _WIDTH_K


def wrap_text(text: str, font: str, font_size: float, max_width: float) -> str:
    """Insert newlines at spaces so each line fits max_width. Words stay whole.

    *font* is kept in the signature for call-site compatibility but width is now
    font-family-independent (estimate_text_width); the per-family difference is
    within the slack already built into _WIDTH_K.
    """
    words = text.split()
    if not words:
        return text
    lines: list[str] = []
    cur: list[str] = []
    for w in words:
        trial = " ".join(cur + [w])
        if cur and estimate_text_width(trial, font_size) > max_width:
            lines.append(" ".join(cur))
            cur = [w]
        else:
            cur.append(w)
    if cur:
        lines.append(" ".join(cur))
    return "\n".join(lines)


# -- background grid ------------------------------------------------------

def coordinate_grid(ground: str, *, opacity: float = 1.0) -> VGroup:
    col = T.color(ground, "grid_line")
    step = T.GRID_CELL
    lines = []
    x = -FRAME_W / 2
    while x <= FRAME_W / 2 + 1e-6:
        lines.append(Line([x, -FRAME_H / 2, 0], [x, FRAME_H / 2, 0],
                          stroke_color=col, stroke_width=1.0, stroke_opacity=opacity))
        x += step
    y = -FRAME_H / 2
    while y <= FRAME_H / 2 + 1e-6:
        lines.append(Line([-FRAME_W / 2, y, 0], [FRAME_W / 2, y, 0],
                          stroke_color=col, stroke_width=1.0, stroke_opacity=opacity))
        y += step
    return VGroup(*lines)


# -- text primitives ------------------------------------------------------

def eyebrow(label: str, ground: str, *, role: str = "secondary") -> Text:
    """Mono uppercase wide-tracked tag, e.g. '[ DEFINITION ]'."""
    return Text(label.upper(), font=T.FONT_MONO, font_size=T.fs("eyebrow"),
                color=T.color(ground, role), weight="MEDIUM")


def heading(text: str, ground: str, *, role: str = "primary", size: str = "h1",
            max_width: float | None = None) -> Text:
    """Display heading (plain Text, SEMIBOLD). If *max_width* is given and the
    rendered line is wider, scale it down to fit -- the standalone-display-line
    exception to "wrap, don't shrink" (a hero title has no siblings to size-match,
    and manim Text does not centre multi-line cleanly, so a clamp beats a wrap)."""
    mob = Text(text, font=T.FONT_DISPLAY, font_size=T.fs(size),
               color=T.color(ground, role), weight="SEMIBOLD")
    if max_width is not None and mob.width > max_width:
        mob.scale_to_fit_width(max_width)
    return mob


def body_text(text: str, ground: str, *, role: str = "text", size: str = "body",
              max_width: float | None = None, align: str = "LEFT") -> Text:
    """CMU Serif body text. If max_width given, wraps at spaces (never mid-word).

    NOTE: *align* is accepted for caller intent but multi-line justification is
    not yet applied (manim Text defaults to left). TODO: centre multi-line when
    align == "CENTER". Single-line text is unaffected.
    """
    fsz = T.fs(size)
    content = wrap_text(text, T.FONT_BODY, fsz, max_width) if max_width else text
    return Text(content, font=T.FONT_BODY, font_size=fsz,
                color=T.color(ground, role), line_spacing=1.0)


def heading_rule(width: float, ground: str, *, role: str = "secondary") -> Line:
    return Line(LEFT * width / 2, RIGHT * width / 2,
                stroke_color=T.color(ground, role), stroke_width=T.HEADING_RULE_W)


def plot_dot(ground: str, *, role: str = "accent", r: float = 0.06):
    """Small filled coordinate-point bullet (the design's PlotDot motif)."""
    from manim import Dot
    return Dot(radius=r, color=T.color(ground, role))


def vrule(height: float, ground: str, *, role: str = "hairline",
          width: float = 1.5, opacity: float = 1.0) -> Line:
    """A thin vertical divider line (column separators, step rules)."""
    ln = Line([0, height / 2, 0], [0, -height / 2, 0],
              stroke_color=T.color(ground, role), stroke_width=width)
    ln.set_opacity(opacity)
    return ln


def hrule(width: float, ground: str, *, role: str = "hairline",
          stroke: float = 1.5, opacity: float = 1.0) -> Line:
    """A thin horizontal divider line."""
    ln = Line(LEFT * width / 2, RIGHT * width / 2,
              stroke_color=T.color(ground, role), stroke_width=stroke)
    ln.set_opacity(opacity)
    return ln


_GLYPH_TEX = {"check": r"\checkmark", "cross": r"\times", "qed": r"\blacksquare"}


def glyph(name: str, ground: str, *, role: str, size: str = "math"):
    """Render a special symbol via LaTeX, not a font character.

    ✓ ✗ ∎ are drawn as MathTex (\\checkmark / \\times / \\blacksquare) so they
    always render in Computer Modern alongside the math, regardless of the body
    Text font's glyph coverage. (Originated in the sans body-font era, when Hanken
    lacked these and they tofu'd; the body font is Computer Modern now, but routing
    through LaTeX keeps them uniform and font-change-proof.)
    """
    return MathTex(_GLYPH_TEX[name], color=T.color(ground, role), font_size=T.fs(size))


def prose_tex(text: str, ground: str, *, role: str = "text", size: str = "body"):
    """Prose that may carry LaTeX markup -- inline ``$math$`` and/or a ``\\\\``
    line break -- rendered in Tex *text mode*.

    Use this (not ``body_text``) whenever a prose field can contain ``$...$`` or
    ``\\\\``: plain ``Text`` shows that markup literally (the ``$f$`` / ``\\\\``
    garble). Unlike ``math_line``, this never routes to MathTex, so a markup-free
    word like "Identity" stays upright text, not math italics.

    font_size is scaled by ``TEX_TEXT_SCALE`` so this sits at the same visual size
    as ``body_text`` (Text and Tex render the same font_size differently). Prefer
    the ``prose()`` router below over calling this directly.
    """
    return Tex(text, color=T.color(ground, role), font_size=T.fs(size) * T.TEX_TEXT_SCALE)


def _wrap_prose_tex(text: str, ground: str, role: str, size: str, max_width: float):
    """Greedily word-wrap markup prose into prose_tex lines that each fit max_width.

    ``$...$`` spans are atomic tokens, so a wrap never lands inside math (which
    would split a span and break the LaTeX). Returns a list of prose_tex mobjects.
    """
    tokens: list[str] = []
    for part in re.split(r"(\$[^$]*\$)", text):
        if part.startswith("$") and part.endswith("$") and len(part) >= 2:
            tokens.append(part)
        else:
            tokens.extend(part.split())

    lines: list = []
    cur: list[str] = []
    for tok in tokens:
        if cur and prose_tex(" ".join(cur + [tok]), ground, role=role, size=size).width > max_width:
            lines.append(prose_tex(" ".join(cur), ground, role=role, size=size))
            cur = [tok]
        else:
            cur.append(tok)
    if cur:
        lines.append(prose_tex(" ".join(cur), ground, role=role, size=size))
    return lines


def prose(text: str, ground: str, *, role: str = "text", size: str = "body",
          max_width: float | None = None, align: str = "LEFT"):
    """Render an author prose field, routing by content so markup never garbles.

    The ONE place that decides Text-vs-Tex for prose: markup-free text goes to
    ``body_text`` (plain Text, wraps at *max_width*); text with LaTeX markup
    (inline ``$math$`` or a ``\\\\`` break) goes to ``prose_tex`` (Tex text-mode,
    size-matched). Templates call this for statements, step text, takeaways,
    recap points -- any field an author might put ``$`` / ``\\`` into.

    Tex can't word-wrap natively, so an over-wide *inline-math* line is wrapped at
    word boundaries into stacked lines at full size (matching the plain prose
    beside it -- NOT shrunk, which used to make a math-bearing recap point look
    smaller than its neighbours). Text with explicit ``\\\\`` breaks is left as
    authored (only scaled down if a line still overflows).
    """
    if "$" not in text and "\\" not in text:
        return _mark_prose(body_text(text, ground, role=role, size=size,
                                     max_width=max_width, align=align))

    mob = prose_tex(text, ground, role=role, size=size)
    if max_width is None or mob.width <= max_width or "\\" in text:
        if max_width is not None and mob.width > max_width:
            mob.scale_to_fit_width(max_width)   # explicit-break line still too wide
        return _mark_prose(mob)

    # inline math, over-wide, no explicit breaks: wrap at word boundaries
    lines = _wrap_prose_tex(text, ground, role, size, max_width)
    group = VGroup(*lines)
    if align == "LEFT":
        group.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
    else:
        group.arrange(DOWN, buff=0.2)
    return _mark_prose(group)


def _mark_prose(mob):
    """Tag the Text/Tex nodes a prose() call produced, so sizecheck.py can find
    the prose lines in a built scene and compare their (scale-aware) font_size
    across stacked siblings. The tag rides through any later .scale()."""
    if isinstance(mob, (Text, Tex, MathTex)):
        mob._brand_prose = True
    else:
        for sub in mob.submobjects:
            _mark_prose(sub)
    return mob


def heading_rich(text: str, ground: str, *, role: str = "primary", size: str = "h1"):
    """A display heading that may carry inline ``$math$``.

    Plain headings go through ``heading`` (Text, SEMIBOLD). When the title has
    ``$...$`` (e.g. "Worked Example: $f(x)=x^3+2$"), split on ``$`` and alternate
    SEMIBOLD Text with MathTex so the math renders instead of printing literally.
    Callers clamp width themselves (titles vary a lot in length).
    """
    if "$" not in text:
        return heading(text, ground, role=role, size=size)
    fsz = T.fs(size)
    col = T.color(ground, role)
    mobs = []
    for i, part in enumerate(text.split("$")):
        if not part:
            continue
        if i % 2:  # odd segments are the spans that were between $...$
            mobs.append(MathTex(part, color=col, font_size=fsz))
        else:
            mobs.append(Text(part, font=T.FONT_DISPLAY, font_size=fsz,
                             color=col, weight="SEMIBOLD"))
    return VGroup(*mobs).arrange(RIGHT, buff=0.24, aligned_edge=DOWN)


def math_line(tex: str, ground: str, *, role: str = "math", size: str = "math"):
    """A math (or math+text) line, recoloured. Computer Modern serif.

    Two forms are accepted, auto-detected:
    - Pure math, no '$' (e.g. r"f(x_1) \\ne f(x_2)") -> MathTex (whole string
      is math mode).
    - Mixed text + inline math with '$...$' (e.g. "$f(x_1)$ whenever $x_1$")
      -> Tex (text mode; the $...$ spans are the math). Passing this to MathTex
      would nest math mode inside align* and crash ("Missing }"), which is the
      bug this guards against.
    """
    col = T.color(ground, role)
    fsz = T.fs(size)
    if "$" in tex:
        return Tex(tex, color=col, font_size=fsz)
    return MathTex(tex, color=col, font_size=fsz)


# -- math card ------------------------------------------------------------

def math_card(content: VGroup, ground: str, *, pad: float = 0.55) -> RoundedRectangle:
    card = RoundedRectangle(
        corner_radius=0.08,
        width=content.width + 2 * pad,
        height=content.height + 2 * pad,
        stroke_color=T.color(ground, "hairline"),
        stroke_width=1.5,
        fill_color=T.color(ground, "card_fill"),
        fill_opacity=0.6 if ground == "dark" else 0.5,
    )
    card.move_to(content.get_center())
    return card


# -- summit-bars motif ----------------------------------------------------

def _four_point_star(radius: float, col: str, opacity: float) -> Polygon:
    r, inner = radius, radius * 0.38
    pts = [[0, r, 0], [inner, inner, 0], [r, 0, 0], [inner, -inner, 0],
           [0, -r, 0], [-inner, -inner, 0], [-r, 0, 0], [-inner, inner, 0]]
    return Polygon(*pts, color=col, fill_color=col, fill_opacity=opacity, stroke_width=0)


def summit_bars(ground: str, *, height: float = 0.5, color_role: str = "muted",
                star: bool = False, opacity: float = 0.5) -> VGroup:
    """7 ascending rounded bars (+ optional gold star). Brand DNA, not the logo."""
    heights = [0.32, 0.56, 0.78, 1.0, 0.78, 0.56, 0.32]
    bar_w = height * 0.16
    gap = height * 0.09
    col = T.color(ground, color_role)
    bars = [RoundedRectangle(corner_radius=bar_w / 2, width=bar_w, height=h * height,
                             stroke_width=0, fill_color=col, fill_opacity=opacity)
            for h in heights]
    group = VGroup(*bars).arrange(RIGHT, buff=gap, aligned_edge=DOWN)
    if star:
        s = _four_point_star(height * 0.12, T.color(ground, "brand_gold"), opacity)
        s.next_to(group[3], UP, buff=height * 0.1)
        group = VGroup(group, s)
    return group


# -- logo -----------------------------------------------------------------
#
# The official lockup SVG places its Chinese name in <text> elements, which
# manim's SVGMobject does NOT render (it only draws <rect>/<path>/<line>), so
# loading it dropped the whole wordmark. Instead we rebuild the lockup from
# manim primitives + a system CJK font (Noto Sans TC, the family the design
# specifies and which is present on this machine). Brand colours are fixed here
# -- this is the one place hard-coded hex is correct, because it's the logo.

_NAVY = "#16294E"
_RED = "#BA0C2F"
_GOLD = "#B6892B"
_GREY = "#6B7280"
_CJK = "Noto Sans TC"


def _summit_logo_mark(unit: float) -> VGroup:
    """The summit-bars + gold-star mark in brand colours (centre bar = navy)."""
    heights = [0.244, 0.467, 0.689, 1.0, 0.689, 0.467, 0.244]
    bw = unit * 0.144
    gap = unit * 0.056
    bars = [
        RoundedRectangle(corner_radius=bw * 0.45, width=bw, height=h * unit,
                         stroke_width=0, fill_color=(_NAVY if i == 3 else _RED),
                         fill_opacity=1.0)
        for i, h in enumerate(heights)
    ]
    row = VGroup(*bars).arrange(RIGHT, buff=gap, aligned_edge=DOWN)
    star = _four_point_star(unit * 0.2, _GOLD, 1.0)
    star.next_to(row[3], UP, buff=unit * 0.12)
    return VGroup(row, star)


def logo_lockup(*, height: float = 1.7) -> VGroup:
    """Full NTU lockup: summit mark | divider | 3-line Chinese wordmark + pill.

    Rebuilt from primitives so the Chinese renders (see note above). Scaled to
    *height* at the end so callers size it in manim units.
    """
    mark = _summit_logo_mark(1.0)

    divider = Line([0, 0.62, 0], [0, -0.62, 0], stroke_color=_NAVY, stroke_width=2)
    divider.set_opacity(0.3)

    small = Text("國立臺灣大學 ｜ NTU", font=_CJK, font_size=15, color=_GREY)
    line1 = Text("北區高中學生科學研究", font=_CJK, weight="BOLD", font_size=28, color=_NAVY)
    line2 = Text("人才培育計畫", font=_CJK, weight="BOLD", font_size=28, color=_NAVY)

    pill_label = Text("數學組", font=_CJK, weight="BOLD", font_size=17, color="#FFFFFF")
    pill = RoundedRectangle(corner_radius=0.08, width=pill_label.width + 0.34,
                            height=pill_label.height + 0.22, stroke_width=0,
                            fill_color=_RED, fill_opacity=1.0)
    pill_label.move_to(pill.get_center())
    pill_group = VGroup(pill, pill_label)

    words = VGroup(small, line1, line2, pill_group).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    lockup = VGroup(mark, divider, words).arrange(RIGHT, buff=0.34)
    lockup.scale_to_fit_height(height)
    return lockup


def logo_svg(name: str, *, height: float = 1.4) -> SVGMobject | None:
    """Load an icon SVG (pure geometry, no <text>) -- e.g. 'icon-color'.

    Safe only for the icon marks, which are all rect/path. Do NOT use for the
    lockup (its <text> wordmark would be dropped); use logo_lockup() instead.
    """
    path = _BRAND / f"{name}.svg"
    if not path.exists():
        return None
    svg = SVGMobject(str(path))
    svg.height = height
    return svg
