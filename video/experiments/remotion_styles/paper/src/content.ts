/** Shared token lists for §3.1 (one source for stills and motion). */
import { Token } from "./components/Formula";
import { semantic } from "./theme";

export const HEAD = { left: "Chapter 3 · Differentiation Rules", right: "Derivatives of Sine and Cosine", folio: "112" };

const D: Token = { key: "d", tex: "\\frac{d}{dx}", color: semantic.derivative };

/** d/dx sin x = cos x, split at the relation for alignment */
export const dSinL: Token[] = [D, { key: "sin", tex: "\\sin", gap: 0.14 }, { key: "x1", tex: "x", gap: 0.16 }];
export const dSinR: Token[] = [
  { key: "cos", tex: "\\cos", color: semantic.cos },
  { key: "x2", tex: "x", gap: 0.16, color: semantic.cos },
];
export const dCosL: Token[] = [
  D,
  { key: "cos", tex: "\\cos", gap: 0.14, color: semantic.cos },
  { key: "x1", tex: "x", gap: 0.16, color: semantic.cos },
];
export const dCosR: Token[] = [
  { key: "neg", tex: "{-}" },
  { key: "sin", tex: "\\sin", gap: 0.02 },
  { key: "x2", tex: "x", gap: 0.16 },
];

/** Motion test: the sentence and its symbolic form (shared keys glide). */
export const words: Token[] = [
  { key: "op", text: "the slope of", italic: true },
  { key: "sin", tex: "\\sin", gap: 0.3 },
  { key: "at1", text: "at", italic: true, gap: 0.3 },
  { key: "x1", tex: "x", gap: 0.26 },
  { key: "eq", tex: "=", br: true },
  { key: "ht", text: "the height of", italic: true, gap: 0.3 },
  { key: "cos", tex: "\\cos", gap: 0.3, color: semantic.cos },
  { key: "at2", text: "at", italic: true, gap: 0.3 },
  { key: "x2", tex: "x", gap: 0.26, color: semantic.cos },
];
export const symbols: Token[] = [
  { key: "op", tex: "\\frac{d}{dx}", color: semantic.derivative },
  { key: "sin", tex: "\\sin", gap: 0.14 },
  { key: "x1", tex: "x", gap: 0.16 },
  { key: "eq", tex: "=", gap: 0.3 },
  { key: "cos", tex: "\\cos", gap: 0.3, color: semantic.cos },
  { key: "x2", tex: "x", gap: 0.16, color: semantic.cos },
];
