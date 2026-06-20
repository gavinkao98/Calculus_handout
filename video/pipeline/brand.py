"""Brand visual primitives (Times serif UI + newtx math).

Builds the recurring design elements templates compose. Colours come from the
active ground's palette (dark/paper) via theme.py -- no hex literals here.

Fonts (2026-06-20 revert to Times New Roman; was Direction D's Inter Tight + CM):
headings + prose render in Times New Roman (Pango Text); labels/eyebrows in Courier
New; math in newtxtext/newtxmath (MathTex/Tex). body_text() renders prose via Pango
Text (Times); prose_tex()/heading_rich() handle the inline-$math$ path via Tex
(newtx), size-matched to the Pango prose by TEX_TEXT_SCALE. The font family always
flows through theme.FONT_* -- this module hardcodes no font name.

Glow recipe ("alive on dark"): glow_curve() = a wide low-alpha halo under a crisp
stroke (manim has no blur); text_glow() = a static halo behind emphasised glyphs.
accent_panel() is the bar+panel box (theorem/callout/recap). hero_curve/ghost_numeral/
progress_dots build the divider opener.
"""
from __future__ import annotations

import re
from pathlib import Path

import numpy as np
from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    CubicBezier,
    DashedLine,
    Dot,
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


# -- text wrapping (never breaks a word) ----------------------------------
#
# Width is ESTIMATED from character count, not measured by building a Text.
# The old approach created a throwaway Text per trial word-combination to read
# its .width; under disable_caching those measurement SVGs intermittently came
# out empty -> "ParseError: no element found". The estimate removes that whole
# class of failure (and is much faster -- no SVG per trial).
#
# Calibration (manim units per char*font_size), for Times New Roman advances.
# CJK glyphs are full-width, so they count as ~2x a latin advance. Use 0.0058 as a
# small safety margin (overflow is worse than a slightly short line). One global knob
# -- retune if fonts change (Direction D's wider Inter Tight needed 0.0068).

_WIDTH_K = 0.0058


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
    """Mono uppercase wide-tracked tag, e.g. '[ DEFINITION ]' (Courier New)."""
    return Text(label.upper(), font=T.FONT_MONO, font_size=T.fs("eyebrow"),
                color=T.color(ground, role), weight="MEDIUM")


def heading(text: str, ground: str, *, role: str = "primary", size: str = "h1",
            weight: str = "BOLD", max_width: float | None = None) -> Text:
    """Display heading -- Times New Roman BOLD. If *max_width* is
    given and the rendered line is wider, scale it down to fit -- the standalone-
    display-line exception to "wrap, don't shrink" (a hero title has no siblings to
    size-match, and manim Text does not centre multi-line cleanly, so clamp beats wrap)."""
    mob = Text(_pango_dashes(text), font=T.FONT_DISPLAY, font_size=T.fs(size),
               color=T.color(ground, role), weight=weight)
    if max_width is not None and mob.width > max_width:
        mob.scale_to_fit_width(max_width)
    return mob


def _pango_dashes(s: str) -> str:
    """LaTeX dash ligatures don't exist in Pango Text, so render the glyphs:
    ``---`` -> em dash, ``--`` -> en dash. (The Tex paths take the reverse.)"""
    return s.replace("---", "—").replace("--", "–")


def _tex_dashes(s: str) -> str:
    """A literal em/en dash an author typed -> LaTeX ligatures, so CM sets them."""
    return s.replace("—", "---").replace("–", "--")


def _escape_tex(text: str) -> str:
    """Escape characters that are special in LaTeX text mode."""
    text = text.replace("\\", r"\textbackslash{}")
    for ch in "&%$#_{}":
        text = text.replace(ch, "\\" + ch)
    text = text.replace("~", r"\textasciitilde{}")
    text = text.replace("^", r"\textasciicircum{}")
    return text


def body_text(text: str, ground: str, *, role: str = "text", size: str = "body",
              max_width: float | None = None, align: str = "LEFT"):
    """Body prose rendered via Pango Text (Times New Roman).

    (Was LaTeX \\text{}/newtx to match the old serif handout; Direction D sets prose
    in Times serif, so prose goes through Pango Text again.) If *max_width* is
    given, wraps at word boundaries (never mid-word) using the char-estimate width
    -- no throwaway measurement SVGs, which intermittently came out empty under
    disable_caching. Returns a single Text for one line, a VGroup of Text lines for
    multi-line.
    """
    col = T.color(ground, role)
    fsz = T.fs(size)

    def mk(s: str) -> Text:
        return Text(_pango_dashes(s), font=T.FONT_BODY, font_size=fsz, color=col)

    if max_width is None:
        return mk(text)

    words = text.split()
    if not words:
        return mk("")

    lines: list[str] = []
    cur: list[str] = []
    for w in words:
        trial = " ".join(cur + [w])
        if cur and estimate_text_width(trial, fsz) > max_width:
            lines.append(" ".join(cur))
            cur = [w]
        else:
            cur.append(w)
    if cur:
        lines.append(" ".join(cur))

    if len(lines) == 1:
        return mk(lines[0])

    group = VGroup(*[mk(s) for s in lines])
    if align == "LEFT":
        group.arrange(DOWN, buff=0.22, aligned_edge=LEFT)
    else:
        group.arrange(DOWN, buff=0.22)
    return group


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
    always render in the newtx math font alongside the math, regardless of the Pango
    body Text font's glyph coverage. (Originated in an earlier sans body-font era when
    that font lacked these and they tofu'd; routing through LaTeX keeps them uniform
    and font-change-proof.)
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

    Wrapped in ``\\mbox{}`` so LaTeX never line-breaks it into a centred paragraph:
    a long sentence stays ONE (wide) line, so prose()'s width check is a true
    single-line width and prose() can word-wrap it into LEFT-aligned lines itself
    (Direction D is left-flush, not the old centred LaTeX paragraph).
    """
    return Tex(r"\mbox{" + text + "}", color=T.color(ground, role),
               font_size=T.fs(size) * T.TEX_TEXT_SCALE)


_DESC_CHARS = set("gjpqy(),;[]{}/Q")


def _compose(text: str, ground: str, role: str, fsz: float, *, weight: str = "NORMAL",
             max_width: float | None = None, align: str = "LEFT", line_buff: float = 0.26):
    """Compose a line (or wrapped lines) of Times text + newtx math (serif text +
    serif math, ON THE SAME LINE). Runs are BASELINE-aligned (text by a
    descender-aware baseline, math by the optical math-axis); $...$ spans are atomic.
    Wraps at *max_width* if given (prose); otherwise one line (headings, then clamp).
    Shared by prose() and heading_rich() so titles and body match."""
    col = T.color(ground, role)
    xref_h = Text("x", font=T.FONT_BODY, font_size=fsz, weight=weight).height
    descent = max(Text("g", font=T.FONT_BODY, font_size=fsz, weight=weight).height - xref_h, 0.0)
    axis = 0.30 * xref_h
    space = max(Text("a a", font=T.FONT_BODY, font_size=fsz, weight=weight).width
                - Text("aa", font=T.FONT_BODY, font_size=fsz, weight=weight).width, 0.06)
    ref_mx = MathTex("x", font_size=fsz)
    math_scale = (xref_h / ref_mx.height) if ref_mx.height > 1e-6 else 1.0

    # tokenize: words, $...$ atomic, trailing punctuation merged onto its token
    tokens: list[str] = []
    for part in re.split(r"(\$[^$]*\$)", text):
        if part.startswith("$") and part.endswith("$") and len(part) >= 2:
            tokens.append(part)
        else:
            tokens.extend(part.split())
    merged: list[str] = []
    for tok in tokens:
        if merged and re.fullmatch(r"[,.;:!?]+", tok):
            merged[-1] += tok
        else:
            merged.append(tok)
    tokens = merged
    if not tokens:
        return Text("", font=T.FONT_BODY, font_size=fsz, weight=weight, color=col)

    # runs grouped by token: (mob, is_math, gap_before[, text]); intra-token runs
    # (e.g. "$y$.") are tight and stay together so a period never wraps off alone.
    token_groups: list[list] = []
    for ti, tok in enumerate(tokens):
        parts = [p for p in re.split(r"(\$[^$]*\$)", tok) if p]
        grp = []
        for pi, p in enumerate(parts):
            gap = space if (ti > 0 and pi == 0) else 0.0
            if p.startswith("$") and p.endswith("$") and len(p) >= 2:
                m = MathTex(p[1:-1], color=col, font_size=fsz).scale(math_scale)
                grp.append((m, True, gap))
            else:
                t = Text(_pango_dashes(p), font=T.FONT_BODY, font_size=fsz,
                         weight=weight, color=col)
                grp.append((t, False, gap, p))
        token_groups.append(grp)

    budget = max_width if max_width is not None else 1e9
    lines: list[list] = []
    cur: list = []
    cur_w = 0.0
    for grp in token_groups:
        gw = sum(r[0].width for r in grp)
        lead = space if cur else 0.0
        if cur and cur_w + lead + gw > budget:
            lines.append(cur)
            cur, cur_w = list(grp), gw
        else:
            cur.extend(grp)
            cur_w += lead + gw
    if cur:
        lines.append(cur)

    def place(line_runs) -> VGroup:
        x = 0.0
        for i, run in enumerate(line_runs):
            mob, is_math = run[0], run[1]
            if i > 0:
                x += run[2]
            if is_math or (run[3].strip() and all(c in "—–-·•*" for c in run[3].strip())):
                mob.move_to([0, axis, 0])              # math / mid-height glyph -> axis
            else:
                has_desc = any(c in _DESC_CHARS for c in run[3])
                base = mob.get_bottom()[1] + (descent if has_desc else 0.0)
                mob.shift([0, -base, 0])               # baseline -> 0
            mob.shift([x - mob.get_left()[0], 0, 0])   # left edge -> x
            x = mob.get_right()[0]
        return VGroup(*[r[0] for r in line_runs])

    line_grps = [place(ln) for ln in lines]
    if len(line_grps) == 1:
        return line_grps[0]
    grp = VGroup(*line_grps)
    if align == "LEFT":
        grp.arrange(DOWN, buff=line_buff, aligned_edge=LEFT)
    else:
        grp.arrange(DOWN, buff=line_buff)
    return grp


def _prose_mixed(text: str, ground: str, role: str, size: str,
                 max_width: float | None, align: str):
    """Inline-math prose composite (Times serif prose + newtx math). See _compose."""
    return _compose(text, ground, role, T.fs(size), weight="NORMAL",
                    max_width=max_width, align=align)


def prose(text: str, ground: str, *, role: str = "text", size: str = "body",
          max_width: float | None = None, align: str = "LEFT"):
    """Render an author prose field, routing by content so markup never garbles.

    The ONE place that decides how prose is set. Prose is Times serif, math is
    newtx serif -- ON THE SAME LINE.
    - Markup-free text -> ``body_text`` (plain Times Text, wraps at *max_width*).
    - Text with inline ``$math$`` -> ``_prose_mixed`` (Times text runs + newtx
      MathTex runs composited and word-wrapped) so a math-bearing line stays serif
      throughout, matching its pure-prose siblings (no font mismatch).
    - Text with an explicit ``\\\\`` break (no inline $) -> single ``prose_tex`` Tex
      (rare; the author controls the break).
    """
    if "$" not in text and "\\" not in text:
        return _mark_prose(body_text(text, ground, role=role, size=size,
                                     max_width=max_width, align=align))

    # explicit \\ break, no inline math: keep the author's break as one Tex line
    if "$" not in text and "\\\\" in text:
        mob = prose_tex(text, ground, role=role, size=size)
        if max_width is not None and mob.width > max_width:
            mob.scale_to_fit_width(max_width)
        return _mark_prose(mob)

    return _mark_prose(_prose_mixed(text, ground, role, size, max_width, align))


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


def heading_rich(text: str, ground: str, *, role: str = "primary", size: str = "h1",
                 max_width: float | None = None):
    """A display heading that may carry inline ``$math$``.

    Plain titles go through ``heading`` (Times BOLD). A title WITH ``$...$`` is
    composited the same way as prose (``_compose``): Times BOLD text runs +
    x-height-matched newtx MathTex runs, baseline-aligned on one line -- so a mixed
    title's text stays Pango Times like its pure-text siblings, with the math in newtx,
    instead of the whole line routing through Tex. *max_width* clamps a long
    title to fit (the standalone-display-line "shrink, don't wrap" exception).
    """
    if "$" not in text:
        return heading(text, ground, role=role, size=size, max_width=max_width)
    mob = _compose(text, ground, role, T.fs(size), weight="BOLD")  # one line
    if max_width is not None and mob.width > max_width:
        mob.scale_to_fit_width(max_width)
    return mob


def math_line(tex: str, ground: str, *, role: str = "math", size: str = "math"):
    """A math (or math+text) line, recoloured. newtx (Times) serif.

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


# -- glow recipe ("alive on dark") ----------------------------------------
#
# manim has no Gaussian blur, so the "6px crisp stroke under a 16px blurred halo"
# recipe is emulated with a wide low-opacity stroke copy UNDER the crisp stroke.
# stroke_width here is in manim stroke units (NOT px); callers pass a crisp width
# (~5-6 reads like the design's 6px) and the halo follows GLOW_HALO_RATIO.

def glow_curve(vmob, ground: str, *, role: str = "secondary", width: float = 6.0,
               halo_ratio: float | None = None, halo_opacity: float = 0.26) -> VGroup:
    """Restyle *vmob* as a glowing curve: a wide faint halo under a crisp stroke.

    Returns VGroup(halo, crisp). The crisp stroke is recoloured to the *role* hue
    (semantic: secondary=blue, accent=amber, success=green, warning=red); the halo
    uses the matching glow rgba. Pass a curve/line VMobject (e.g. axes.plot output).
    """
    ratio = T.GLOW_HALO_RATIO if halo_ratio is None else halo_ratio
    crisp_hex = T.color(ground, role)
    glow_hex, _a = T.glow_for(_glow_name(role))
    halo = vmob.copy().set_stroke(color=glow_hex, width=width * ratio,
                                  opacity=halo_opacity).set_fill(opacity=0)
    crisp = vmob.set_stroke(color=crisp_hex, width=width, opacity=1.0)
    return VGroup(halo, crisp)


def text_glow(mob, ground: str, *, role: str = "accent", width: float = 2.6,
              opacity: float = 0.5) -> VGroup:
    """Static persistent halo behind emphasised glyphs (the 'text-shadow' glow).

    Returns VGroup(wide-halo, near-halo, mob). The halos are stroke-only copies of
    *mob* (no fill -- the original carries the fill on top), in the glow hue, at two
    widths for a soft falloff that reads as a glow rather than a thick outline. (manim
    has no blur.) Distinct from blocks.write_glow (a reveal Flash); use when the glow
    must persist on the final frame.
    """
    glow_hex, _a = T.glow_for(_glow_name(role))
    wide = mob.copy().set_stroke(color=glow_hex, width=width * 2.2, opacity=opacity * 0.38)
    wide.set_fill(opacity=0)
    near = mob.copy().set_stroke(color=glow_hex, width=width, opacity=opacity * 0.85)
    near.set_fill(opacity=0)
    return VGroup(wide, near, mob)


def _glow_name(role: str) -> str:
    """Map a semantic role (secondary/accent/success/warning) -> a GLOW key."""
    return {"secondary": "blue", "accent": "amber", "success": "green",
            "warning": "red", "blue": "blue", "amber": "amber", "green": "green",
            "red": "red", "violet": "violet"}.get(role, "blue")


def dotted_leader(length: float, ground: str, *, role: str = "hairline_strong",
                  opacity: float = 0.5) -> DashedLine:
    """A short dotted leader (derivation reason rail, value-table guides)."""
    ln = DashedLine(ORIGIN, RIGHT * length, dash_length=0.055, dashed_ratio=0.42,
                    stroke_color=T.color(ground, role), stroke_width=1.5)
    ln.set_opacity(opacity)
    return ln


# -- accent-bar panel (theorem box / callout / recap card / worked strip) --

def accent_panel(content, ground: str, *, bar_role: str = "accent",
                 fill_role: str = "panel", radius: float | None = None,
                 bar_px: float = 5.0, pad: float = 0.45, pad_x: float | None = None,
                 fill_opacity: float = 1.0, hairline: bool = True) -> VGroup:
    """A raised panel with a flush coloured left accent bar, wrapping *content*.

    The dark ground is already the container, so a 5px bar + soft panel is enough
    weight (the design's "bar replaces the full box"). Returns VGroup(panel, bar,
    content); content keeps its position. z-order: panel, bar, then content on top.
    """
    radius = T.RADIUS_MD if radius is None else radius
    px = pad if pad_x is None else pad_x
    w = content.width + 2 * px
    h = content.height + 2 * pad
    panel = RoundedRectangle(
        corner_radius=radius, width=w, height=h,
        stroke_color=T.color(ground, "hairline"),
        stroke_width=1.5 if hairline else 0,
        fill_color=T.color(ground, fill_role), fill_opacity=fill_opacity,
    )
    panel.move_to(content.get_center())
    bar_w = T.BAR_W * (bar_px / 5.0)
    bar = RoundedRectangle(
        corner_radius=bar_w / 2, width=bar_w, height=h,
        stroke_width=0, fill_color=T.color(ground, bar_role), fill_opacity=1.0,
    )
    bar.move_to([panel.get_left()[0] + bar_w / 2, panel.get_center()[1], 0])
    return VGroup(panel, bar, content)


# -- divider / brand-opener builders --------------------------------------

def hero_curve(ground: str, *, role: str = "secondary", width: float = 6.0) -> VGroup:
    """A glowing cubic that sweeps bottom-left -> top-right and bleeds off the right
    edge (the divider's hero curve). Returns a glow_curve VGroup."""
    w, h = T.FRAME_W / 2, T.FRAME_H / 2
    curve = CubicBezier(
        np.array([-w * 0.95, -h * 0.78, 0]),
        np.array([-w * 0.35, -h * 0.95, 0]),
        np.array([w * 0.55, h * 0.30, 0]),
        np.array([w * 1.05, h * 0.92, 0]),
    )
    return glow_curve(curve, ground, role=role, width=width, halo_opacity=0.22)


def ghost_numeral(text: str, ground: str, *, opacity: float = 0.05) -> Text:
    """A huge faint numeral behind divider content (5% opacity ink-1)."""
    mob = Text(str(text), font=T.FONT_DISPLAY, font_size=T.fs("ghost_numeral"),
               color=T.color(ground, "ink_1"), weight="BOLD")
    mob.set_opacity(opacity)
    return mob


def progress_dots(current: int, total: int, ground: str, *, role: str = "accent",
                  gap: float = 0.34, r: float = 0.052) -> VGroup:
    """A row of progress dots; the *current* one is elongated into a pill + accent.
    current is 1-based."""
    items = []
    for i in range(total):
        if i == current - 1:
            pill = RoundedRectangle(corner_radius=r, width=r * 6, height=r * 2,
                                    stroke_width=0, fill_color=T.color(ground, role),
                                    fill_opacity=1.0)
            items.append(pill)
        else:
            items.append(Dot(radius=r, color=T.color(ground, "ink_faint")))
    return VGroup(*items).arrange(RIGHT, buff=gap)


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
# The official lockup SVG has Chinese text in <text> elements which manim's
# SVGMobject drops. _outline_text.py (in assets/) converts text to <path>
# outlines using fonttools; the result is lockup-color-outlined.svg which
# SVGMobject loads as pure vector geometry.

_ASSETS = Path(__file__).resolve().parent / "assets"


def logo_lockup_outlined(*, height: float = 1.7) -> SVGMobject:
    """Official NTU lockup from outlined SVG (all text converted to paths).

    Loads the designer-provided SVG with text elements pre-converted to vector
    path outlines via fonttools, so every detail matches the brand guide exactly
    while rendering at native vector resolution (no bitmap blur).
    """
    path = _ASSETS / "lockup-color-outlined.svg"
    svg = SVGMobject(str(path))
    svg.height = height
    return svg
