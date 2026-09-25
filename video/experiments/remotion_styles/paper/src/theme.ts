/**
 * 「紙本編輯排版」design tokens — the single source every component reads.
 * Units are px at 1920×1080 ("page px"; the Camera may scale the page).
 */
import { Easing } from "remotion";

// ── Colour ────────────────────────────────────────────────────────────────
// Two-ink print (black + rubric red) plus one "blue pencil" ink for cosine.
// Chromatic inks validated with the dataviz validator on #F4EFE4:
// crimson↔cobalt CVD ΔE 18.0 (protan), normal ΔE 28.9, contrast ≥ 3:1.
// Ink black is deliberately the neutral "text ink", not a categorical hue.
export const color = {
  paper: "#F4EFE4", // warm laid paper
  paperShade: "#E9E1CF", // plates, table fills, recessed areas
  ink: "#1F1B16", // primary text + the subject curve (sin)
  ink2: "#5A5249", // secondary text: captions, axis labels
  ink3: "#948A7C", // tertiary: folios, tick labels, leaders
  rule: "#C9BFAD", // hairlines, range frames
  accent: "#BA0C2F", // rubric red = brand crimson (derivative / tangent)
  cobalt: "#1F5E9E", // blue-pencil ink (cosine)
  ochre: "#A07C10", // §3.1 unguided: the angle θ as arc length / sector (validated all-pairs vs crimson ΔE 10.1 deutan, cobalt, ≥3:1)
} as const;

export const semantic = {
  sin: color.ink,
  cos: color.cobalt,
  derivative: color.accent,
  angle: color.ochre,
  tangent: color.accent,
  point: color.ink,
  text: color.ink,
  caption: color.ink2,
  label: color.ink3,
} as const;

// ── Type ──────────────────────────────────────────────────────────────────
export const font = {
  serif: "'EB Garamond', 'Garamond', serif", // text, display, small caps
  mathScale: 0.9, // Pagella has a larger x-height than Garamond: shrink math to match
} as const;

/**
 * Type scale (px at 1080p, *before* camera scale).  Act 3 raised the floor:
 * nothing a viewer must read is set below 28 px on screen (phone legibility),
 * so every label/caption/small-cap size here is ≥ 28 and scenes keep the
 * camera at s ≥ 1 whenever such text is the focal point.
 */
export const type = {
  display: 300, // section numeral on title cards
  title: 108,
  h2: 64,
  formula: 112, // display equations (theorem statements)
  proof: 70, // proof lines
  formulaSm: 76,
  body: 44,
  caption: 36,
  label: 34, // figure labels, readouts
  smallCaps: 28, // running heads, figure numbers: caps set small + tracked
  micro: 28, // sidenotes, table heads (floor)
} as const;

export const tracking = {
  smallCaps: "0.18em",
  label: "0.04em",
} as const;

/** OpenType feature strings (the @fontsource cut keeps onum/lnum/tnum, not smcp). */
export const features = {
  text: "'kern' 1, 'liga' 1, 'onum' 1",
  smallCaps: "'kern' 1, 'lnum' 1",
  figures: "'kern' 1, 'lnum' 1, 'tnum' 1", // live readouts: no jitter
} as const;

// ── Grid (1920 × 1080 page) ───────────────────────────────────────────────
// Tufte-style: a narrow sidenote column on the left, a wide main block.
export const grid = {
  w: 1920,
  h: 1080,
  marginX: 120,
  headY: 74, // running-head baseline
  headRuleY: 94,
  footY: 1022, // folio baseline
  side: { x: 120, w: 280 }, // sidenote / marginalia column
  main: { x: 460, w: 1340 }, // main text block
  gutter: 60,
  baseline: 12, // vertical rhythm unit
} as const;

// ── Strokes ───────────────────────────────────────────────────────────────
export const stroke = {
  hairline: 1.5,
  axis: 1.8,
  curve: 4.2,
  tangent: 3.4,
  emphasis: 5,
  dot: 7.5, // point radius
  ring: 2.5, // paper ring around dots
} as const;

// ── Motion ────────────────────────────────────────────────────────────────
export const fps = 30;
export const dur = {
  quick: 10,
  base: 18,
  slow: 32,
  draw: 42, // a full curve being inked
} as const;

export const ease = {
  /** Pen on paper: quick attack, long careful finish. */
  ink: Easing.bezier(0.3, 0, 0.12, 1),
  /** Rostrum-camera moves: symmetric, heavy. */
  camera: Easing.bezier(0.65, 0, 0.3, 1),
  out: Easing.bezier(0.16, 1, 0.3, 1),
  inOut: Easing.bezier(0.45, 0, 0.55, 1),
} as const;

export const springs = {
  settle: { damping: 200 }, // no bounce
  tangent: { damping: 11, stiffness: 150, mass: 0.7 }, // one visible overshoot
  token: { damping: 15, stiffness: 120, mass: 0.9 }, // formula glyph glide
  pop: { damping: 13, stiffness: 180, mass: 0.6 },
} as const;
