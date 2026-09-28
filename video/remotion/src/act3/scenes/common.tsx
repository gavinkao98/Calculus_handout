/** Shared bits for the act's scenes. */
import React from "react";
import { AbsoluteFill } from "remotion";
import { color, font, features, type } from "../../theme";
import { Camera, Page, ShellProps } from "../../components/Shell";
import type { Cam } from "../clock";

export const HEAD = { left: "Chapter 3 · Differentiation Rules", right: "Derivatives of Sine and Cosine" };

/** A page (or spread) under the rostrum camera. */
export const Sheet: React.FC<ShellProps & { cam: Cam }> = ({ cam, children, ...page }) => (
  <AbsoluteFill style={{ backgroundColor: color.paper }}>
    <Camera {...cam}>
      <Page {...page}>{children}</Page>
    </Camera>
  </AbsoluteFill>
);

/** Full-page SVG layer in page coordinates. */
export const Layer: React.FC<{ w?: number; h?: number; children: React.ReactNode; opacity?: number }> = ({
  w = 1920,
  h = 1080,
  children,
  opacity = 1,
}) => (
  <svg width={w} height={h} style={{ position: "absolute", left: 0, top: 0, overflow: "visible", opacity }}>
    {children}
  </svg>
);

/** Italic Garamond line (captions, glosses) positioned by baseline-ish top. */
export const Gloss: React.FC<{
  x: number;
  y: number;
  size?: number;
  c?: string;
  italic?: boolean;
  opacity?: number;
  align?: "left" | "center" | "right";
  w?: number;
  weight?: number;
  children: React.ReactNode;
  style?: React.CSSProperties;
}> = ({ x, y, size = type.caption, c = color.ink2, italic = true, opacity = 1, align = "left", w, weight, children, style }) => (
  <div
    style={{
      position: "absolute",
      left: align === "center" ? x - (w ?? 0) / 2 : align === "right" ? x - (w ?? 0) : x,
      top: y,
      width: w,
      textAlign: align,
      fontFamily: font.serif,
      fontSize: size,
      fontStyle: italic ? "italic" : "normal",
      fontWeight: weight,
      lineHeight: 1.3,
      color: c,
      opacity,
      fontFeatureSettings: features.text,
      ...style,
    }}
  >
    {children}
  </div>
);

/** An ink stroke that draws on (hand-marked emphasis: underline, ellipse, arrow). */
export const InkPath: React.FC<{ d: string; len: number; p: number; c?: string; w?: number; opacity?: number }> = ({
  d,
  len,
  p,
  c = color.accent,
  w = 4,
  opacity = 1,
}) =>
  p <= 0 ? null : (
    <path
      d={d}
      fill="none"
      stroke={c}
      strokeWidth={w}
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeDasharray={`${len} ${len}`}
      strokeDashoffset={len * (1 - Math.min(1, p))}
      opacity={opacity}
    />
  );

/** A hand-drawn ellipse around (cx, cy) — slightly open and tilted, like a pen ring. */
export const ringPath = (cx: number, cy: number, rx: number, ry: number, tilt = -6) => {
  const pts: string[] = [];
  const t0 = (-150 * Math.PI) / 180;
  const n = 64;
  const a = (tilt * Math.PI) / 180;
  for (let i = 0; i <= n; i++) {
    const t = t0 + (i / n) * Math.PI * 2.12;
    const r = 1 + 0.06 * Math.sin(3 * t);
    const x = rx * r * Math.cos(t);
    const y = ry * r * Math.sin(t);
    pts.push(`${i ? "L" : "M"}${(cx + x * Math.cos(a) - y * Math.sin(a)).toFixed(1)} ${(cy + x * Math.sin(a) + y * Math.cos(a)).toFixed(1)}`);
  }
  return { d: pts.join(""), len: Math.PI * (rx + ry) * 1.1 };
};

/** Downward arrow (for "tends to" annotations under a factor). */
export const arrowDown = (x: number, y0: number, y1: number) => ({
  d: `M${x} ${y0} L${x} ${y1} M${x - 11} ${y1 - 14} L${x} ${y1} L${x + 11} ${y1 - 14}`,
  len: y1 - y0 + 40,
});
