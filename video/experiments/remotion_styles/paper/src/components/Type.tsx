import React from "react";
import { interpolate, useCurrentFrame } from "remotion";
import { tex } from "../math/tex";
import { color, ease, features, font, tracking, type } from "../theme";

// ── Measurement ─────────────────────────────────────────────────────────
let ctx: CanvasRenderingContext2D | null = null;
const widths = new Map<string, number>();
/** Advance width of a Garamond string (fonts must be loaded — see FontGate). */
export const measure = (
  text: string,
  size: number,
  opts: { italic?: boolean; weight?: number } = {},
): number => {
  const f = `${opts.italic ? "italic " : ""}${opts.weight ?? 400} ${size}px "EB Garamond"`;
  const k = `${f}|${text}`;
  const hit = widths.get(k);
  if (hit !== undefined) return hit;
  if (!ctx) ctx = document.createElement("canvas").getContext("2d")!;
  ctx.font = f;
  const w = ctx.measureText(text).width;
  widths.set(k, w);
  return w;
};

// ── Progress helpers ────────────────────────────────────────────────────
export const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
export const useProgress = (from: number, len: number, easing = ease.ink) => {
  const frame = useCurrentFrame();
  return interpolate(frame, [from, from + len], [0, 1], { ...clamp, easing });
};

// ── Small caps (tracked) ────────────────────────────────────────────────
export const SmallCaps: React.FC<{
  children: React.ReactNode;
  size?: number;
  color?: string;
  style?: React.CSSProperties;
}> = ({ children, size = type.smallCaps, color: c = color.ink2, style }) => (
  <span
    style={{
      fontFamily: font.serif,
      fontSize: size, // cap size in px (the web cut has no smcp: caps set small + tracked)
      fontWeight: 500,
      fontFeatureSettings: features.smallCaps,
      letterSpacing: tracking.smallCaps,
      color: c,
      textTransform: "uppercase",
      whiteSpace: "nowrap",
      ...style,
    }}
  >
    {children}
  </span>
);

// ── Hairline rule that draws on from its left end ───────────────────────
export const Rule: React.FC<{
  x: number;
  y: number;
  w: number;
  weight?: number;
  color?: string;
  from?: number;
  len?: number;
  vertical?: boolean;
}> = ({ x, y, w, weight = 1.5, color: c = color.rule, from, len = 20, vertical }) => {
  const q = useProgress(from ?? 0, len);
  const p = from === undefined ? 1 : q;
  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y - weight / 2,
        width: vertical ? weight : w,
        height: vertical ? w : weight,
        background: c,
        transformOrigin: vertical ? "50% 0%" : "0% 50%",
        scale: vertical ? `1 ${p}` : `${p} 1`,
      }}
    />
  );
};

// ── "Set in type": a soft left→right wipe, as if ink is being laid ──────
export const InkReveal: React.FC<{
  from: number;
  len?: number;
  children: React.ReactNode;
  style?: React.CSSProperties;
  rise?: number;
}> = ({ from, len = 22, children, style, rise = 8 }) => {
  const p = useProgress(from, len, ease.out);
  const edge = p * 130 - 15;
  const m = `linear-gradient(90deg, #000 ${edge - 15}%, transparent ${edge + 15}%)`;
  return (
    <div
      style={{
        position: "absolute",
        WebkitMaskImage: p >= 1 ? undefined : m,
        maskImage: p >= 1 ? undefined : m,
        translate: `0px ${(1 - p) * rise}px`,
        ...style,
      }}
    >
      {children}
    </div>
  );
};

// ── Inline math that sits on the text baseline ──────────────────────────
export const InlineTex: React.FC<{ src: string; color?: string; scale?: number }> = ({
  src,
  color: c,
  scale = 1,
}) => {
  const g = tex(src);
  const k = font.mathScale * scale;
  return (
    <svg
      viewBox={`${g.minX} ${g.minY} ${g.w} ${g.h}`}
      style={{
        display: "inline-block",
        width: `${(g.w / 1000) * k}em`,
        height: `${(g.h / 1000) * k}em`,
        verticalAlign: `${(-(g.h + g.minY) / 1000) * k}em`,
        overflow: "visible",
        color: c,
        margin: "0 0.06em",
      }}
      dangerouslySetInnerHTML={{ __html: g.body }}
    />
  );
};

/** A paragraph of body text on the grid. */
export const Para: React.FC<{
  x: number;
  y: number;
  w: number;
  size?: number;
  lh?: number;
  italic?: boolean;
  color?: string;
  children: React.ReactNode;
  style?: React.CSSProperties;
}> = ({ x, y, w, size = type.body, lh = 1.32, italic, color: c = color.ink, children, style }) => (
  <div
    style={{
      position: "absolute",
      left: x,
      top: y,
      width: w,
      fontFamily: font.serif,
      fontSize: size,
      lineHeight: lh,
      fontStyle: italic ? "italic" : "normal",
      fontFeatureSettings: features.text,
      color: c,
      hyphens: "auto",
      ...style,
    }}
  >
    {children}
  </div>
);
