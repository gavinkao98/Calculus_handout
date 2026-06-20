"""Design system: NTU Calculus Video System — Direction D (sans UI + CM math).

Port of the redesign (the "Manim Video Design System" handoff): a 3Blue1Brown-style
dark glowing teaching ground, four semantic accents, Inter-Tight sans headings/prose,
and Computer Modern math — the modern science-explainer sans/serif contrast.

Tokens (colour, type scale, geometry, glow) mirror the redesign's tokens/*.css.

Two grounds:
- DARK  -> teaching frames (definition/derivation/theorem/procedure/graph/...)
- PAPER -> brand frames (intro / divider / outro), warm #f4f1e9 with the NTU lockup

Fonts (Direction D): headings + prose use "Inter Tight" (Pango); labels/eyebrows use
"JetBrains Mono"; math (MathTex/Tex) uses Computer Modern (manim's default template,
newtx dropped in _bootstrap._set_tex_template). The TTFs are vendored under
pipeline/assets/fonts and registered process-locally by _bootstrap.register_design_fonts.

Colour contract (reference SEMANTIC roles, not raw hues):
- blue   -> definitions, default curve, default highlight     (role secondary / blue)
- amber  -> theorems, key results, the second curve, emphasis (role accent / amber)
- green  -> positive sign, success, QED, increasing           (role success / green)
- red    -> negative sign, warning, counterexample, decreasing (role warning / red)
Math defaults to bright ink (ink_1) and is *tinted* blue/amber only for emphasis.
violet is a RESERVED third-object accent — use sparingly.

Back-compat: the old Direction-B role names (secondary/accent/math/warning/...) are kept
as live ALIASES pointing at the new hues, so the existing templates resolve unchanged;
only blocks.ACCENT_ROLE needed remapping.
"""
from __future__ import annotations

# -- fonts (Pango family names) -------------------------------------------
# Direction D: Inter Tight sans for display + prose, JetBrains Mono for labels.
FONT_DISPLAY = "Inter Tight"
FONT_BODY = "Inter Tight"
FONT_MONO = "JetBrains Mono"

# -- type scale -----------------------------------------------------------
# tokens give px @ 1920x1080. manim font_size is its own unit; PX_TO_FS converts.
# Re-measured for Inter Tight: a Times "H" was 0.00920 u/fs, Inter Tight is 0.01011
# (≈10% taller per fs), so the old 0.72 (Times) over-sizes. 0.72*0.920/1.011 = 0.655
# keeps a given design-px at the same physical size across the font swap; the larger
# Direction-D px scale (h1 62->82) then gives the intended bigger type. One global knob.
PX_TO_FS = 0.655

# manim renders Text (Pango) and Tex/MathTex (LaTeX) at *different* visual sizes for
# the same font_size. Re-measured for Inter Tight vs Computer Modern text-mode: an
# Inter-Tight "Rg" is 1.42x a CM \text{Rg} at equal font_size. So prose rendered via
# Tex (the inline-$math$ path) must be scaled up by this to size-match the plain
# Inter-Tight prose beside it. Pure math (math_line/MathTex) is its own size role,
# left unscaled. One global knob — retune if fonts change.
TEX_TEXT_SCALE = 1.42

# Density B px @ 1920x1080. New Direction-D names + back-compat aliases (old callers
# pass these; most per-frame sizes are raw px overrides via fs(<number>)).
_SCALE_PX = {
    # Direction-D scale
    "hero": 112, "h1": 82, "h2": 58, "h3": 44,
    "prose": 42, "prose_sm": 35,
    "math": 48, "math_sm": 40,
    "caption": 30, "eyebrow": 26, "numeral": 104, "ghost_numeral": 520,
    # back-compat aliases (old Direction-B names -> nearest Direction-D size)
    "display": 112, "body": 42, "step": 42, "label": 30,
    "intro_headline": 92, "intro_subtitle": 35, "outro_headline": 78,
}


def fs(role) -> float:
    """Font size in manim units.

    *role* is either a scale-name string ('h1', 'prose', ...) or a raw px number
    (e.g. 34) for the per-frame overrides. px is converted through the same
    PX_TO_FS constant so everything stays proportional.
    """
    if isinstance(role, (int, float)):
        return float(role) * PX_TO_FS
    return _SCALE_PX[role] * PX_TO_FS


# -- palettes (hex from the redesign tokens) ------------------------------
# Canonical Direction-D keys + back-compat aliases (old name -> new hue). color()
# falls back to 'primary' for any unknown role, so a stray name degrades to ink_1.
DARK: dict[str, str] = {
    # grounds
    "bg_black": "#07090f", "bg": "#0c0f17", "bg_soft": "#10131d",
    "panel": "#141927", "panel_2": "#1a2031",
    # ink (text on dark)
    "ink_1": "#eef2fb", "ink_2": "#aab3c6", "ink_3": "#6b748a", "ink_faint": "#444c5e",
    # accents (4 working + 1 reserved)
    "blue": "#5cc8ec", "amber": "#f2b13c", "green": "#54d199", "red": "#fb6a5d",
    "violet": "#9d8cf2",
    # accent ink-tints (text on dark, slightly lifted)
    "blue_ink": "#8fdcf6", "amber_ink": "#f7c469", "green_ink": "#79e0b4", "red_ink": "#ff8f86",
    # hairlines (low-alpha ink flattened over bg #0c0f17)
    "hairline": "#20232b", "hairline_strong": "#2f333b", "hairline_faint": "#171a22",
    # brand (theme-independent constants; used on paper frames + carried for continuity)
    "brand_red": "#ba0c2f", "brand_red_bright": "#e23a57",
    "brand_navy": "#16294e", "brand_gold": "#b6892b",
    "grid_line": "#1b2740",   # latent (SHOW_GRID=False)
    # ---- back-compat aliases (old Direction-B role names) ----
    "primary": "#eef2fb",     # -> ink_1
    "secondary": "#5cc8ec",   # -> blue   (definitions / default highlight)
    "accent": "#f2b13c",      # -> amber  (theorems / key)
    "math": "#eef2fb",        # -> ink_1  (was electric cyan; math is bright ink now)
    "warning": "#fb6a5d",     # -> red
    "success": "#54d199",     # -> green
    "text": "#aab3c6",        # -> ink_2  (body prose)
    "muted": "#6b748a",       # -> ink_3  (captions / faded)
    "heading": "#eef2fb",     # -> ink_1
    "subtitle": "#6b748a",    # -> ink_3
    "card_fill": "#141927",   # -> panel
}

LIGHT: dict[str, str] = {
    # warm paper ground for brand frames (intro / divider / outro)
    "bg_black": "#e7e2d6", "bg": "#f4f1e9", "bg_soft": "#efebe1",
    "panel": "#ffffff", "panel_2": "#faf7ef",
    "ink_1": "#161a22", "ink_2": "#444b59", "ink_3": "#767d8c", "ink_faint": "#aab0bd",
    # accents darkened so they read on light paper
    "blue": "#1f8fc0", "amber": "#c98414", "green": "#1ba272", "red": "#d8453b",
    "violet": "#6a55c8",
    "blue_ink": "#1f8fc0", "amber_ink": "#c98414", "green_ink": "#1ba272", "red_ink": "#d8453b",
    "hairline": "#dad8d2", "hairline_strong": "#c9c7c2", "hairline_faint": "#e7e4dd",
    "brand_red": "#ba0c2f", "brand_red_bright": "#d8453b",
    "brand_navy": "#16294e", "brand_gold": "#b6892b",
    "grid_line": "#e2e6ee",
    # ---- back-compat aliases ----
    "primary": "#16294e",     # -> brand_navy (navy headline / wordmark)
    "secondary": "#1f8fc0",   # -> blue
    "accent": "#ba0c2f",      # -> brand_red (eyebrows / numbering / rules)
    "math": "#161a22",        # -> ink_1
    "warning": "#d8453b",     # -> red
    "success": "#1ba272",     # -> green
    "text": "#444b59",        # -> ink_2
    "muted": "#767d8c",       # -> ink_3
    "heading": "#16294e",     # -> brand_navy
    "subtitle": "#767d8c",    # -> ink_3
    "card_fill": "#ffffff",   # -> panel
}

# -- glow (the dark-ground "it's alive" recipe) ---------------------------
# manim set_stroke wants (color, opacity) separately, not a single rgba. A curve gets
# a wide low-alpha halo under a crisp stroke; emphasised text gets a tighter halo.
GLOW: dict[str, tuple[str, float]] = {
    "blue": ("#5cc8ec", 0.45), "amber": ("#f2b13c", 0.42),
    "green": ("#54d199", 0.40), "red": ("#fb6a5d", 0.42),
    "violet": ("#9d8cf2", 0.40),
}
ACCENT_DIM = 0.22       # sub-emphasis fill/stroke opacity (column tint, leaders)
GLOW_HALO_RATIO = 2.7   # halo stroke width = crisp width * this (6px crisp -> ~16px halo)


def glow_for(role: str) -> tuple[str, float]:
    """(hex, opacity) for a glow accent name; falls back to blue."""
    return GLOW.get(role, GLOW["blue"])


# -- layout (manim units; 16:9 frame is 14.222 x 8.0) ---------------------
FRAME_W = 14.222
FRAME_H = 8.0
PX_PER_UNIT_X = 1920 / FRAME_W   # = 135
PX_PER_UNIT_Y = 1080 / FRAME_H   # = 135

# Density B: tighter margins so frames fill the screen / read on a phone.
SAFE_MARGIN = 74 / PX_PER_UNIT_X      # ~0.548 u  (top/bottom safe margin)
SIDE_GUTTER = 100 / PX_PER_UNIT_X     # ~0.741 u  (left/right content gutter)
GRID_CELL = 80 / PX_PER_UNIT_Y        # latent
HEADING_RULE_W = 3.0

# vertical rhythm tokens (px -> units) templates consume for consistent spacing
EYEBROW_GAP = 22 / PX_PER_UNIT_Y      # eyebrow -> title
TITLE_GAP = 56 / PX_PER_UNIT_Y        # title -> content zone
LINE_GAP = 28 / PX_PER_UNIT_Y         # between display math lines
ROW_GAP = 44 / PX_PER_UNIT_Y          # between list rows / steps

# corner radii (px -> units)
RADIUS_SM = 6 / PX_PER_UNIT_Y
RADIUS_MD = 12 / PX_PER_UNIT_Y
RADIUS_LG = 18 / PX_PER_UNIT_Y
BAR_W = 5 / PX_PER_UNIT_X             # accent-bar left-edge width

FONTS = {"display": FONT_DISPLAY, "body": FONT_BODY, "mono": FONT_MONO}

# Settled: no coordinate grid is rendered on any template — the deep-ink ground
# carries the aesthetic. grid_line colours stay as a latent motif.
SHOW_GRID = False


def palette(ground: str) -> dict[str, str]:
    return LIGHT if ground == "light" else DARK


def color(ground: str, role: str) -> str:
    pal = palette(ground)
    return pal.get(role, pal["primary"])
