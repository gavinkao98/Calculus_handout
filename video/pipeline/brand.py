"""Brand visual primitives (all-LaTeX type: Plex Sans/Mono text + Latin Modern math).

Builds the recurring design elements templates compose. Colours come from the
active ground's palette (dark/paper) via theme.py -- no hex literals here.

Fonts (Route A, 2026-06-24): ALL on-screen text renders through LaTeX (Tex) so it is
kerned -- manim Text (Pango) does not kern. heading()/heading_rich() set IBM Plex Sans
Bold, body_text()/prose() set IBM Plex Sans, eyebrow() sets IBM Plex Mono; math
(MathTex/Tex) is Latin Modern. The fonts live in the TeX preamble
(_bootstrap.apply_tex_template), so this module hardcodes no font name and no longer
touches Pango at all -- every text mobject it builds (heading, body, eyebrow, glyph,
ghost_numeral) is a Tex/MathTex.

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
# Calibration (manim units per char*font_size). CJK glyphs are full-width, so they count
# as ~2x a latin advance. One global knob -- retune if fonts change (Times advance ~0.0060,
# used 0.0058; Inter Tight 0.0068; NCM-Pango 0.0065). Plex Sans via LaTeX measures
# ~0.004973 per char*fs (Route A, 2026-06-24); 0.00507 = that + 2% so the estimate sits
# just above the real advance (overflow is worse than a slightly short line). The font_size
# fed to estimate_text_width is the TEXT size (_text_fs = fs(size)*TEXT_SCALE), so this is
# keyed to the rendered Plex text size and is unaffected by the math-anchored PX_TO_FS.

_WIDTH_K = 0.00507


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

def _clamp_scale(cur_w, max_w, cur_size, floor):
    """Scale factor to fit max_w without shrinking effective size below `floor`. Never enlarges."""
    if max_w is None or max_w <= 0 or cur_w <= max_w or cur_w <= 0:
        return 1.0
    fit = max_w / cur_w
    floor_scale = floor / cur_size if cur_size > 0 else fit
    return min(1.0, max(fit, floor_scale))


def _clamp_shrink(mob, max_w, cur_size_px):
    """In-place: shrink mob to fit max_w but not below theme.MIN_FONT_FLOOR. The caller passes
    cur_size_px (the role's authored px) -- required for VGroup reasons with no single font_size.
    Drop-in for mob.scale_to_fit_width(max_w) at the single-line sites (SPEC §8)."""
    factor = _clamp_scale(mob.width, max_w, float(cur_size_px), T.MIN_FONT_FLOOR)
    if factor < 1.0:
        mob.scale(factor)
    return mob


def eyebrow(label: str, ground: str, *, role: str = "secondary") -> Tex:
    """Mono uppercase tag, e.g. '[ DEFINITION ]' -- IBM Plex Mono via Tex ``\\texttt{}``.
    (Route A: was Pango Courier New.) No microtype ``\\textls`` tracking: it triggers a
    missing-Metafont makemf error on Plex Mono, and the mono advance already reads as a
    tracked tag."""
    return Tex(r"\texttt{" + _tex_text(label.upper()) + "}",
               font_size=_text_fs("eyebrow"), color=T.color(ground, role))


def heading(text: str, ground: str, *, role: str = "primary", size: str = "h1",
            max_width: float | None = None) -> Tex:
    """Display heading -- IBM Plex Sans Bold (Tex ``\\textbf{}``). (Route A: was Pango
    Times/NCM bold.) If *max_width* is given and the rendered line is wider, scale it
    down to fit -- the standalone-display-line exception to "wrap, don't shrink" (a hero
    title has no siblings to size-match)."""
    mob = Tex(r"\textbf{" + _tex_text(text) + "}", font_size=_text_fs(size),
              color=T.color(ground, role))
    if max_width is not None and mob.width > max_width:
        _clamp_shrink(mob, max_width, T.fs(size) / T.PX_TO_FS)
    return mob


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


def _tex_text(s: str) -> str:
    """A plain-text segment -> LaTeX text-mode source: escape specials, set dashes."""
    return _tex_dashes(_escape_tex(s))


def _text_fs(size) -> float:
    """Font size for TEXT (Plex Sans/Mono), in manim units. theme.PX_TO_FS is the MATH
    (Latin Modern) anchor, so TEXT is scaled up by theme.TEXT_SCALE to its calibrated cap
    height -- this keeps math at its established size while text matches the prior visual
    size (Plex caps are smaller per font_size, so the single PX_TO_FS knob can't size both)."""
    return T.fs(size) * T.TEXT_SCALE


def body_text(text: str, ground: str, *, role: str = "text", size: str = "body",
              max_width: float | None = None, align: str = "LEFT"):
    """Body prose rendered via LaTeX (Tex) in IBM Plex Sans (the \\sfdefault family).

    (Route A, 2026-06-24: was Pango Text -- manim Text does not kern, LaTeX does.)
    Handles pure text only; the prose() router sends any inline-$math$ line through the
    mixed path instead. If *max_width* is given, wraps at word boundaries (never
    mid-word) using the char-estimate width -- no throwaway measurement SVGs, which
    intermittently came out empty under disable_caching. Returns a single Tex for one
    line, a VGroup of LEFT-arranged Tex lines for multi-line.
    """
    col = T.color(ground, role)
    fsz = _text_fs(size)

    def mk(s: str) -> Tex:
        return Tex(_tex_text(s), color=col, font_size=fsz)

    if max_width is None:
        return mk(text)

    words = text.split()
    if not words:
        return VGroup()

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


def _escape_prose(text: str) -> str:
    """Escape the plain-text segments of a prose string for LaTeX text mode, leaving
    any ``$...$`` math spans untouched (they are already math-mode source)."""
    out: list[str] = []
    for part in re.split(r"(\$[^$]*\$)", text):
        if part.startswith("$") and part.endswith("$") and len(part) >= 2:
            out.append(part)
        elif part:
            out.append(_tex_text(part))
    return "".join(out)


def _math_render_width(span: str, fsz: float) -> float:
    """Actual rendered width of a ``$...$`` math span (manim units)."""
    inner = span.strip("$")
    return MathTex(inner, font_size=fsz).width


_math_width_cache: dict[tuple[str, float], float] = {}


def _token_width(tok: str, fsz: float) -> float:
    """Width of one token: rendered width for math spans, char estimate for text.

    Handles math spans with trailing punctuation glued on (e.g. ``$...$,``)
    by splitting into math width + punctuation width.
    """
    if tok.startswith("$"):
        dollar_end = tok.rfind("$", 1)
        if dollar_end > 0:
            math_part = tok[:dollar_end + 1]
            tail = tok[dollar_end + 1:]
            key = (math_part, fsz)
            if key not in _math_width_cache:
                _math_width_cache[key] = _math_render_width(math_part, fsz)
            w = _math_width_cache[key]
            if tail:
                w += estimate_text_width(tail, fsz)
            return w
    return estimate_text_width(tok, fsz)


def _wrap_mixed(text: str, fsz: float, max_width: float | None) -> list[str]:
    """Word-wrap prose that may carry inline ``$math$`` into line strings.

    A ``$...$`` span is one atomic token (never broken, even across its inner spaces);
    trailing punctuation is glued onto its token so a period never wraps off alone.
    Text tokens use the char estimate; math spans use their actual rendered width
    so display-style formulas don't get over-estimated and pushed to a new line.
    Each returned line still carries its ``$...$`` spans for prose() to render as one Tex.
    """
    tokens: list[str] = []
    for part in re.split(r"(\$[^$]*\$)", text):
        if part.startswith("$") and part.endswith("$") and len(part) >= 2:
            tokens.append(part)
        else:
            tokens.extend(part.split())
    merged: list[str] = []
    for tok in tokens:
        if merged and re.fullmatch(r"[,.;:!?)\]}]+", tok):
            merged[-1] += tok
        else:
            merged.append(tok)
    tokens = merged
    if not tokens:
        return []
    if max_width is None:
        return [" ".join(tokens)]
    space_w = estimate_text_width(" ", fsz)
    lines: list[str] = []
    cur: list[str] = []
    cur_w: float = 0.0
    for tok in tokens:
        tw = _token_width(tok, fsz)
        trial_w = cur_w + (space_w if cur else 0) + tw
        if cur and trial_w > max_width:
            lines.append(" ".join(cur))
            cur = [tok]
            cur_w = tw
        else:
            cur.append(tok)
            cur_w = trial_w
    if cur:
        lines.append(" ".join(cur))
    return lines


def _prose_lines(text: str, ground: str, role: str, size: str,
                 max_width: float | None, align: str):
    """Prose with inline ``$math$`` and/or explicit ``\\\\`` breaks, set as LaTeX.

    Each output line is ONE ``Tex`` in text mode: LaTeX lays text + inline math on the
    same line with native baselines and kerning (Plex Sans text, Latin Modern math), so
    the old Pango/Tex baseline compositing (_compose) is gone. Author ``\\\\`` breaks
    split first, then each segment word-wraps to *max_width*; lines are LEFT-stacked.
    """
    col = T.color(ground, role)
    fsz = _text_fs(size)
    line_strs: list[str] = []
    for seg in re.split(r"\\\\", text):
        seg = seg.strip()
        if seg:
            line_strs.extend(_wrap_mixed(seg, fsz, max_width))
    if not line_strs:
        return VGroup()
    mobs = [Tex(_escape_prose(ls), color=col, font_size=fsz) for ls in line_strs]
    if len(mobs) == 1:
        return mobs[0]
    grp = VGroup(*mobs)
    if align == "LEFT":
        grp.arrange(DOWN, buff=0.22, aligned_edge=LEFT)
    else:
        grp.arrange(DOWN, buff=0.22)
    return grp


def prose(text: str, ground: str, *, role: str = "text", size: str = "body",
          max_width: float | None = None, align: str = "LEFT"):
    """Render an author prose field, routing by content so markup never garbles.

    The ONE place that decides how prose is set. Route A: all text is LaTeX (Plex Sans),
    math is Latin Modern -- on the same line.
    - Single ``$...$`` wrapping pure math -> ``math_line`` (display mode, Latin Modern).
    - Markup-free text -> ``body_text`` (Plex Sans Tex, wraps at *max_width*).
    - Text with inline ``$math$`` and/or an explicit ``\\\\`` break -> ``_prose_lines``
      (one Tex per wrapped line; text + inline math sit native on each line).
    """
    stripped = text.strip()
    if stripped.startswith("$") and stripped.endswith("$") and stripped.count("$") == 2:
        mob = math_line(stripped, ground, role=role, size=size)
        if max_width is not None and mob.width > max_width:
            _clamp_shrink(mob, max_width, T.fs(size) / T.PX_TO_FS)
        return _mark_prose(mob)
    if "$" not in text and "\\" not in text:
        return _mark_prose(body_text(text, ground, role=role, size=size,
                                     max_width=max_width, align=align))
    return _mark_prose(_prose_lines(text, ground, role, size, max_width, align))


def _mark_prose(mob):
    """Tag the Text/Tex nodes a prose() call produced, so sizecheck.py can find
    the prose lines in a built scene and compare their (scale-aware) font_size
    across stacked siblings. The tag rides through any later .scale()."""
    if isinstance(mob, (Tex, MathTex)):
        mob._brand_prose = True
    else:
        for sub in mob.submobjects:
            _mark_prose(sub)
    return mob


def heading_rich(text: str, ground: str, *, role: str = "primary", size: str = "h1",
                 max_width: float | None = None):
    """A display heading that may carry inline ``$math$``.

    Plain titles go through ``heading`` (Plex Sans Bold). A title WITH ``$...$`` is set
    as ONE ``Tex``: the words become ``\\textbf{}`` (Plex Bold), the ``$...$`` spans stay
    math (Latin Modern). LaTeX lays text + math on one line with native baselines, so the
    old Pango/Tex compositing (_compose) is gone. *max_width* clamps a long title to fit
    (the standalone-display-line "shrink, don't wrap" exception).
    """
    if "$" not in text:
        return heading(text, ground, role=role, size=size, max_width=max_width)
    pieces: list[str] = []
    for p in re.split(r"(\$[^$]*\$)", text):
        if not p:
            continue
        if p.startswith("$") and p.endswith("$") and len(p) >= 2:
            pieces.append(p)
        else:
            pieces.append(r"\textbf{" + _tex_text(p) + "}")
    mob = Tex("".join(pieces), color=T.color(ground, role), font_size=_text_fs(size))
    if max_width is not None and mob.width > max_width:
        _clamp_shrink(mob, max_width, T.fs(size) / T.PX_TO_FS)
    return mob


def math_line(tex: str, ground: str, *, role: str = "math", size: str = "math"):
    """A math (or math+text) line, recoloured. newtx (Times) serif.

    Three forms are accepted, auto-detected:
    - Pure math, no '$' (e.g. r"f(x_1) \\ne f(x_2)") -> MathTex (display).
    - Single '$...$' wrapping pure math (e.g. "$\\frac{a}{b}$") -> strip the
      delimiters and use MathTex (display).  This is the common storyboard
      convention; without stripping, Tex would render in text mode (inline).
    - Multiple '$...$' spans mixed with text (e.g. "if $f(x)=0$ then $x=a$")
      -> Tex (text mode).  Passing this to MathTex would nest math mode inside
      align* and crash ("Missing }"), which is the bug this guards against.
    """
    col = T.color(ground, role)
    fsz = T.fs(size)
    stripped = tex.strip()
    if stripped.startswith("$") and stripped.endswith("$") and stripped.count("$") == 2:
        return MathTex(stripped[1:-1], color=col, font_size=fsz)
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


def text_glow(mob, ground: str, *, role: str = "accent", width: float = 2.0,
              opacity: float = 0.42) -> VGroup:
    """Wrap *mob* in a VGroup (no-op pass-through; glow disabled 2026-06-29)."""
    return VGroup(mob)


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


def ghost_numeral(text: str, ground: str, *, opacity: float = 0.05) -> Tex:
    """A huge faint numeral behind divider content (5% opacity ink-1), Plex Bold via Tex."""
    mob = Tex(r"\textbf{" + _tex_text(str(text)) + "}", font_size=_text_fs("ghost_numeral"),
              color=T.color(ground, "ink_1"))
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
