"""Brand visual primitives for Direction B (Blueprint Grid).

Builds the recurring design elements templates compose. Colours come from the
active ground's palette (light/dark) via theme.py -- no hex literals here.

Key helper: wrap_text() greedily wraps a string to a max width by inserting
newlines ONLY at spaces, so words never break mid-glyph (the recurring bug).
"""
from __future__ import annotations

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


def heading(text: str, ground: str, *, role: str = "primary", size: str = "h1") -> Text:
    return Text(text, font=T.FONT_DISPLAY, font_size=T.fs(size),
                color=T.color(ground, role), weight="SEMIBOLD")


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

    ✓ ✗ ∎ are absent from the sans body font (Hanken) and render as tofu boxes.
    Drawing them as MathTex (\\checkmark / \\times / \\blacksquare) uses Computer
    Modern, which has them, so they always appear.
    """
    return MathTex(_GLYPH_TEX[name], color=T.color(ground, role), font_size=T.fs(size))


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
