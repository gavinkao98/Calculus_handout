"""Design system: NTU Calculus Video System — Direction D layout, all-LaTeX Plex type.

Port of the redesign (the "Manim Video Design System" handoff): a 3Blue1Brown-style
dark glowing teaching ground, four semantic accents, and IBM Plex Sans for all text with
Latin Modern math — set through LaTeX so it is kerned (Route A, 2026-06-24).

Tokens (colour, type scale, geometry, glow) mirror the redesign's tokens/*.css.

Two grounds:
- DARK  -> teaching frames (definition/derivation/theorem/procedure/graph/...)
- PAPER -> brand frames (intro / divider / outro), warm #f4f1e9 with the NTU lockup

Fonts (Route A, 2026-06-24): ALL on-screen text renders through LaTeX (Tex) -- IBM Plex
Sans for headings/prose, IBM Plex Mono for eyebrows/labels, Latin Modern for math. The
families live in the TeX preamble (_bootstrap.apply_tex_template); nothing goes through
Pango, so this module no longer carries Pango family names. (Was Pango Times/NCM text +
newtx/lmodern math.)

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

# Fonts are no longer named here: all text renders through LaTeX (Tex) and the families
# (Plex Sans / Plex Mono / Latin Modern) are set in _bootstrap.apply_tex_template. (Route
# A removed the FONT_DISPLAY/FONT_BODY/FONT_MONO Pango family names this module used to
# expose; nothing reads them now.)

# -- type scale -----------------------------------------------------------
# tokens give px @ 1920x1080. manim font_size is its own unit; PX_TO_FS converts.
# PX_TO_FS is the MATH (Latin Modern) anchor: math is unchanged across the Route A font
# swap AND across the 2026-09-13 text swap, so this stays at the established 0.698 (the
# NCM-era value the layout/zones were tuned for) and on-screen math keeps its size. TEXT is
# then scaled by TEXT_SCALE to reach its calibrated cap height -- one knob cannot size both,
# because sans caps are ~24% shorter per font_size than the math font, so calibrating
# PX_TO_FS to them (0.9145) would have inflated all math ~31% and overflowed dense scenes
# (Route A decouple, 2026-06-24; was 0.72 Times, 0.655 Inter Tight).
# INVARIANT (1): PX_TO_FS does not move when the TEXT family changes. Only TEXT_SCALE and
# brand._WIDTH_K do -- both are guarded by pipeline/_selftest_text_metrics.py.
PX_TO_FS = 0.698

# TEXT-only scale on top of the MATH-anchored PX_TO_FS. brand's text builders use
# _text_fs(size) = fs(size) * TEXT_SCALE; math (math_line/glyph/MathTex) uses fs(size)
# directly.
# INVARIANT (2): _text_fs(px) must render a cap height of 0.006624 u/px (the Times anchor
# the zones were laid out against), whatever the text family is. That fixes the value:
#   TEXT_SCALE = round(0.006624 / (Tex('H', font_size=fs).height / fs * PX_TO_FS), 4)
# Instrument Sans measures H/fs = 0.007444 -> 1.2748 (2026-09-13). Plex Sans measured
# H/fs = 0.007244 -> 1.3102, the previous value; the same formula reproduces it, so this
# is a recalibration of one constant, not a change of method. (Was TEX_TEXT_SCALE, the
# obsolete Pango<->Tex size-match factor, before the all-LaTeX Route A.)
TEXT_SCALE = 1.2748

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
    "statement": 44,  # canonical declarative statement line (theorem/definition/value_table/sign_chart) -- unify 2026-07-05; was scattered h3=44 / prose=42 / raw 40
    "math": 48, "math_sm": 40,
    "caption": 30, "eyebrow": 26, "numeral": 104, "ghost_numeral": 520,
    "tag": 30,   # mono nav/emphasis tag: derivation result-reason + part pager (was eyebrow=26 == floor; A/B may settle 32)
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


# Minimum readable on-screen font size in PX (1920x1080). Compared against the TRUE authored
# px recovered by sizecheck._effective_font_px (NOT _norm_size, which yields manim units and
# over-divides MathTex). Set at the smallest INTENTIONAL named size (eyebrow=26). Plan 4 / SPEC §8.
MIN_FONT_FLOOR = 26.0  # px; calibrated in PLAN-…-plan4 Task 5


# -- palettes (hex from the redesign tokens) ------------------------------
# Canonical Direction-D keys + back-compat aliases (old name -> new hue). color()
# falls back to 'primary' for any unknown role, so a stray name degrades to ink_1.
DARK: dict[str, str] = {
    # grounds (flat NTU-navy ink, 2026-06-24 Step 2-B1 A/B: was neutral near-black
    # #0c0f17; navy #0a1322 echoes brand_navy #16294e, drops the "near-black + neon"
    # default. Flat solid only -- no gradient, per VISUAL-FRAME-RUBRIC house style.)
    "bg_black": "#070e1a", "bg": "#0a1322", "bg_soft": "#0e1a2e",
    "panel": "#13233f", "panel_2": "#172a49",
    # ink (text on dark). ink_2 lifted #aab3c6 -> #c6cedd (2026-06-25): the navy ground +
    # lighter-weight Plex Sans made the old (near-black/Times-tuned) ink_2 read too dim for
    # teaching annotations/captions/aside bodies (the role="text" tier) at video distance --
    # the recurring "muted teaching text" finding. Still clearly below ink_1 (lum .62 vs .89)
    # so the primary↔secondary hierarchy holds; ink_3 (muted=decoration only) is unchanged.
    "ink_1": "#eef2fb", "ink_2": "#c6cedd", "ink_3": "#6b748a", "ink_faint": "#444c5e",
    # accents. 2026-09-12 Direction B ("對位"): every hue is now HUE-MATCHED to the
    # handout's own semantic axis in handout/latex/template/calcbook.sty, with lightness
    # raised for this navy ground. Previously the two production lines disagreed -- the
    # PDF said definition=ochre/theorem=blue, the video said definition=blue/theorem=amber,
    # so the same concept was a different colour in each medium. Hue is the contract;
    # `_selftest_semantic_palette.py` re-reads calcbook.sty and fails if either side drifts.
    "blue": "#4fa6de", "amber": "#d98f3c", "green": "#3ebe7c", "red": "#d96b6b",
    "violet": "#a493e6", "slate": "#96a0ae",
    # accent ink-tints (text on dark, slightly lifted)
    "blue_ink": "#79bfe8", "amber_ink": "#e8ab63", "green_ink": "#66d19a", "red_ink": "#e88f8f",
    "violet_ink": "#bfb1ef", "slate_ink": "#b3bbc7",
    # ---- semantic roles (the handout axis; these are what ACCENT_ROLE targets) ----
    "concept":  "#d98f3c",  # calcbook aConcept  #994a00 -- definition
    "result":   "#4fa6de",  # calcbook aResult   #0068a7 -- theorem/proposition/corollary/proof
    "practice": "#3ebe7c",  # calcbook aPractice #04773b -- example/solution
    "caution":  "#d96b6b",  # calcbook aCaution  #aa3333 -- caution
    "strategy": "#a493e6",  # calcbook aStrategy #6453a7 -- strategy/procedure
    "aside":    "#96a0ae",  # calcbook aAside    #5d646f -- remark
    "concept_ink": "#e8ab63", "result_ink": "#79bfe8", "practice_ink": "#66d19a",
    "caution_ink": "#e88f8f", "strategy_ink": "#bfb1ef", "aside_ink": "#b3bbc7",
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
    "text": "#c6cedd",        # -> ink_2  (body prose; lifted for navy+Plex, see ink_2 note)
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
    "blue": "#0068a7", "amber": "#994a00", "green": "#04773b", "red": "#aa3333",
    "violet": "#6453a7", "slate": "#5d646f",
    "blue_ink": "#0068a7", "amber_ink": "#994a00", "green_ink": "#04773b", "red_ink": "#aa3333",
    "violet_ink": "#6453a7", "slate_ink": "#5d646f",
    # ---- semantic roles. This is a PAPER ground, the same as the PDF, so these carry the
    #      handout's hexes VERBATIM -- no lifting. (Direction B, 2026-09-12.) ----
    "concept":  "#994a00",  # calcbook aConcept
    "result":   "#0068a7",  # calcbook aResult
    "practice": "#04773b",  # calcbook aPractice
    "caution":  "#aa3333",  # calcbook aCaution
    "strategy": "#6453a7",  # calcbook aStrategy
    "aside":    "#5d646f",  # calcbook aAside
    "concept_ink": "#994a00", "result_ink": "#0068a7", "practice_ink": "#04773b",
    "caution_ink": "#aa3333", "strategy_ink": "#6453a7", "aside_ink": "#5d646f",
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
    "blue": ("#4fa6de", 0.45), "amber": ("#d98f3c", 0.42),
    "green": ("#3ebe7c", 0.40), "red": ("#d96b6b", 0.42),
    "violet": ("#a493e6", 0.40), "slate": ("#96a0ae", 0.38),
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

# Settled: no coordinate grid is rendered on any template — the deep-ink ground
# carries the aesthetic. grid_line colours stay as a latent motif.
SHOW_GRID = False


def palette(ground: str) -> dict[str, str]:
    return LIGHT if ground == "light" else DARK


def color(ground: str, role: str) -> str:
    pal = palette(ground)
    return pal.get(role, pal["primary"])
