"""Design system: NTU Calculus Video System -- Direction B (Blueprint Grid).

Port of the designer handoff (video/design_handoff/from_designer): tokens.json +
video-system.css are the source of truth for colour, type scale and layout
metrics. TWO values intentionally deviate from the tokens, by settled project
decision: the text fonts (see "Fonts" below) and the coordinate grid (see
SHOW_GRID). Everything else tracks the tokens.

Two grounds:
- DARK  -> teaching frames (definition/example/procedure/theorem/recap/graph)
- LIGHT -> brand frames (intro / outro), paper ground with the NTU lockup

Fonts (DEVIATION from tokens, settled): all non-math text uses Computer Modern
Unicode (CMU Serif / CMU Typewriter Text), NOT the sans token families (Space
Grotesk / Hanken / JetBrains Mono). Chosen so prose and LaTeX math share one
family, the OTF embeds in-repo (no Google Fonts fetch), and the glyphs the sans
body font lacked (checkmark/times/QED) never tofu. Registered at runtime by
_bootstrap.register_design_fonts from the vendored OTF files in assets/fonts/.
Math (MathTex/Tex) is also Computer Modern via LaTeX. CJK text in the NTU logo
uses Noto Sans TC (system font, not vendored).
"""
from __future__ import annotations

# -- fonts (family names as registered by manimpango) ---------------------
FONT_DISPLAY = "CMU Serif"
FONT_BODY = "CMU Serif"
FONT_MONO = "CMU Typewriter Text"

# -- type scale -----------------------------------------------------------
# tokens.json gives px @ 1920x1080. manim font_size is its own unit; PX_TO_FS
# converts. Calibrated so design h1 (62px) -> ~45 manim fs. One global knob.
# NOTE: PX_TO_FS was tuned against the *Text* (Pango) path, which is what FONT_*
# headings/body use.
PX_TO_FS = 0.72

# manim renders Text (Pango) and Tex/MathTex (LaTeX) at *different* visual sizes
# for the same font_size: a Text is ~1.34x taller than a Tex at equal font_size
# (measured, CMU Serif vs LaTeX Computer Modern). So prose rendered via Tex must
# be scaled up by this factor to sit at the same size as body_text beside it --
# otherwise a markup row (Tex) looks smaller than a plain row (Text) in the same
# column. Applied in brand.prose_tex; math (brand.math_line) is intentionally its
# own size role and is left unscaled. One global knob -- retune if fonts change.
TEX_TEXT_SCALE = 1.34

_SCALE_PX = {
    "display": 104, "h1": 62, "h2": 46, "math": 46, "math_sm": 36,
    "body": 38, "step": 32, "eyebrow": 24, "label": 28,
    "intro_headline": 88, "intro_subtitle": 34, "outro_headline": 78,
}


def fs(role) -> float:
    """Font size in manim units.

    *role* is either a scale-name string ('h1', 'body', ...) or a raw px number
    (e.g. 34) for the per-frame size overrides the design uses. px is converted
    through the same PX_TO_FS constant so everything stays proportional.
    """
    if isinstance(role, (int, float)):
        return float(role) * PX_TO_FS
    return _SCALE_PX[role] * PX_TO_FS


# -- palettes (hex from tokens.json) --------------------------------------
DARK: dict[str, str] = {
    "bg": "#0a0e1a",
    "bg_soft": "#121a2e",
    "primary": "#eef0f7",
    "secondary": "#4cc9f0",   # definitions / propositions (cyan)
    "accent": "#f4b13a",      # theorems / key emphasis (gold)
    "math": "#7df9ff",        # math expressions (electric blue)
    "warning": "#ff6b6b",     # counter-examples (coral)
    "success": "#06d6a0",     # verification / QED (emerald)
    "text": "#c8ccdb",        # body narration (light slate)
    "muted": "#7e8497",       # retired / faded prior content
    "hairline": "#243049",    # faint rules, ticks, borders
    "grid_line": "#1b2740",   # faint blue-grey (flattened rgba)
    "brand_red": "#BA0C2F",
    "brand_red_bright": "#e23a57",
    "brand_navy": "#16294E",
    "brand_gold": "#B6892B",
    "card_fill": "#0a0e1a",
}

LIGHT: dict[str, str] = {
    "bg": "#eef1f6",          # paper
    "primary": "#16294E",     # navy headline / wordmark
    "heading": "#16294E",
    "subtitle": "#5a6478",
    "text": "#2b3242",        # list / body on light
    "accent": "#BA0C2F",      # eyebrows, numbering, dots, rules (brand red)
    "muted": "#5a6478",
    "grid_line": "#e2e6ee",   # faint navy grid (flattened)
    "brand_red": "#BA0C2F",
    "brand_navy": "#16294E",
    "brand_gold": "#B6892B",
    "card_fill": "#ffffff",
}

# -- layout (manim units; 16:9 frame is 14.222 x 8.0) ---------------------
FRAME_W = 14.222
FRAME_H = 8.0
PX_PER_UNIT_X = 1920 / FRAME_W
PX_PER_UNIT_Y = 1080 / FRAME_H
SAFE_MARGIN = 96 / PX_PER_UNIT_X      # ~0.71 u
SIDE_GUTTER = 220 / PX_PER_UNIT_X     # ~1.63 u
GRID_CELL = 80 / PX_PER_UNIT_Y        # ~0.59 u
HEADING_RULE_W = 3.0

FONTS = {"display": FONT_DISPLAY, "body": FONT_BODY, "mono": FONT_MONO}

# Settled decision: the "Blueprint Grid" coordinate grid is NOT rendered on any
# template (intro, outro, and all content scenes) -- the deep-navy engineering
# ground carries the aesthetic without it. The name is kept; grid_line colours
# stay in the palettes as a latent motif (re-enable by emitting
# brand.coordinate_grid), but no template emits a grid Block today.
SHOW_GRID = False


def palette(ground: str) -> dict[str, str]:
    return LIGHT if ground == "light" else DARK


def color(ground: str, role: str) -> str:
    pal = palette(ground)
    return pal.get(role, pal["primary"])
