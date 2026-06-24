"""Design system: NTU Calculus Video System — Direction D layout, Times serif type.

Port of the redesign (the "Manim Video Design System" handoff): a 3Blue1Brown-style
dark glowing teaching ground, four semantic accents, and Times New Roman serif type
throughout (headings/prose + newtx math) — the classic textbook look (the Direction D
Inter Tight / CM type was reverted to Times on 2026-06-20).

Tokens (colour, type scale, geometry, glow) mirror the redesign's tokens/*.css.

Two grounds:
- DARK  -> teaching frames (definition/derivation/theorem/procedure/graph/...)
- PAPER -> brand frames (intro / divider / outro), warm #f4f1e9 with the NTU lockup

Fonts (Times revert, 2026-06-20): headings + prose use "Times New Roman" (Pango);
labels/eyebrows use "Courier New"; math (MathTex/Tex) uses newtxtext/newtxmath (set in
_bootstrap._set_tex_template). All are Windows system fonts / a LaTeX package -- nothing
is vendored (Direction D's vendored Inter Tight / JetBrains Mono / CM were removed).

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
# New Computer Modern serif for display + prose (NCM switch 2026-06-24, to match the
# handout's 2026-06-22 NCM move); Courier New for labels/eyebrows. The NCM text family
# "NewComputerModern10" is registered with Pango in _bootstrap._register_ncm_fonts()
# (located via kpsewhich from the MiKTeX newcomputermodern package, not vendored).
# (Was Times New Roman, the 2026-06-20 revert.)
FONT_DISPLAY = "NewComputerModern10"
FONT_BODY = "NewComputerModern10"
FONT_MONO = "Courier New"

# -- type scale -----------------------------------------------------------
# tokens give px @ 1920x1080. manim font_size is its own unit; PX_TO_FS converts.
# One global knob — retune if fonts change. Calibrated to keep cap heights CONSTANT
# across font swaps: cap_height(px) = px * PX_TO_FS * (H/fs). The Times anchor was
# PX_TO_FS 0.72 at H/fs 0.00920 (= 0.006624 u/px). Plex Sans via LaTeX measures
# H/fs 0.007244 (shorter caps per fs), so 0.9145 = 0.72*0.00920/0.007244 preserves that
# cap height, layout unchanged (Route A, 2026-06-24; was 0.698 NCM-Pango, 0.72 Times,
# 0.655 Inter Tight).
PX_TO_FS = 0.9145

# Route A: ALL text now renders via LaTeX (Tex), so there is no Pango↔Tex size gap to
# correct — prose and inline-$math$ Tex share one code path at one font_size. Held at
# 1.0 (no-op multiplier) so prose_tex and any other call site that still reads it stays
# correct. (Historical: Pango-Text-vs-Tex needed 1.36 for Times/newtx, 1.34 for
# NCM-Pango/lmodern, 1.42 for Inter Tight — all obsolete now that no text is Pango.)
TEX_TEXT_SCALE = 1.0

# Inline math inside a DISPLAY HEADING (heading_rich). Provisional 1.0 for Route A:
# LaTeX sets text + inline math on one line with native baseline/sizing, so a heading's
# $f(x)=x^n$ no longer towers over the bold words the way the old composited
# (x-height-matched MathTex) path did — which needed 0.78 to rein it in. Finalised in
# Task 5 after rendering headings that carry math; 1.0 = no reduction.
HEADING_MATH_SCALE = 1.0

# Density B px @ 1920x1080. New Direction-D names + back-compat aliases (old callers
# pass these; most per-frame sizes are raw px overrides via fs(<number>)).
_SCALE_PX = {
    # Direction-D scale
    "hero": 112, "h1": 78, "h2": 58, "h3": 44,  # h1 82->78: titles read as over-dominant on many scenes (Codex, both rounds)
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
    # grounds (flat NTU-navy ink, 2026-06-24 Step 2-B1 A/B: was neutral near-black
    # #0c0f17; navy #0a1322 echoes brand_navy #16294e, drops the "near-black + neon"
    # default. Flat solid only -- no gradient, per VISUAL-FRAME-RUBRIC house style.)
    "bg_black": "#070e1a", "bg": "#0a1322", "bg_soft": "#0e1a2e",
    "panel": "#13233f", "panel_2": "#172a49",
    # ink (text on dark)
    "ink_1": "#eef2fb", "ink_2": "#aab3c6", "ink_3": "#6b748a", "ink_faint": "#444c5e",
    # accents (4 working + 1 reserved)
    "blue": "#5cc8ec", "amber": "#f2b13c", "green": "#54d199", "red": "#fb6a5d",
    "violet": "#9d8cf2",
    # accent ink-tints (text on dark, slightly lifted)
    "blue_ink": "#8fdcf6", "amber_ink": "#f7c469", "green_ink": "#79e0b4", "red_ink": "#ff8f86",
    # hairlines (low-alpha ink flattened over navy bg #0a1322; retuned with the navy ground)
    "hairline": "#22324f", "hairline_strong": "#33456a", "hairline_faint": "#1a2840",
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
    "card_fill": "#13233f",   # -> panel
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
# Body placement: short content vertically centred in the title->bottom zone drifts
# to ~y=-0.6 (below frame centre), reading as disconnected from the title. We instead
# centre but CLAMP the title->content gap to this max, so short content sits in the
# upper-middle (anchored to the title like theorem_proof/procedure_steps), while tall
# content still uses the full zone. Tunable; ~1 prose line of air below TITLE_GAP.
BODY_TOP_GAP_MAX = 84 / PX_PER_UNIT_Y  # ~0.62 u extra below TITLE_GAP before clamp.
#   History: 0.71 -> 1.0 (gate-1 audit: at 0.71 short content sat ~y=+0.5, "top-heavy,
#   empty lower half"). That tune predated row-spreading. Now BODY_FILL_FRAC spreads
#   short content to fill the LOWER zone, so a tighter top gap no longer strands content
#   up top -- it just closes the dead band a Codex 2026-06-21 review flagged on ~12
#   scenes ("title-to-body gap too large"). 0.62 sits content ~one text line below the
#   title while the spread keeps the lower third occupied.
LINE_GAP = 28 / PX_PER_UNIT_Y         # between display math lines
ROW_GAP = 44 / PX_PER_UNIT_Y          # between list rows / steps
# Short content in a tall body zone leaves BOTH a "dead band under the title" and an
# empty lower third (a Codex 2026-06-21 review flagged this on ~12 scenes). Rather than
# yanking the block toward the title (which only trades one empty band for another), the
# teaching templates SPREAD their inter-row spacing so short content fills ~this fraction
# of the body zone before placement. Tall content already exceeds it and is untouched.
BODY_FILL_FRAC = 0.72

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
