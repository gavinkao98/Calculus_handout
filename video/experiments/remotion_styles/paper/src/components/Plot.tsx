/**
 * Figure primitives, drawn in page px inside an <svg>.  A PlotFrame maps
 * math units to the page; every mark takes a 0..1 progress so it can be
 * inked on.  Axes follow Tufte's range-frame: lines only span the data.
 */
import React from "react";
import { color, features, font, stroke, tracking, type } from "../theme";
import { FormulaG, Token } from "./Formula";

export type PlotFrame = { ox: number; oy: number; ux: number; uy: number };
export const px = (f: PlotFrame, x: number, y: number): [number, number] => [f.ox + x * f.ux, f.oy - y * f.uy];

const polyline = (f: PlotFrame, fn: (x: number) => number, a: number, b: number, n: number) => {
  const pts: [number, number][] = [];
  for (let i = 0; i <= n; i++) {
    const x = a + ((b - a) * i) / n;
    pts.push(px(f, x, fn(x)));
  }
  return pts;
};
const d = (pts: [number, number][]) => pts.map((p, i) => `${i ? "L" : "M"}${p[0].toFixed(2)} ${p[1].toFixed(2)}`).join("");

/** A function inked from a toward b; `progress` advances the pen along x. */
export const Curve: React.FC<{
  f: PlotFrame;
  fn: (x: number) => number;
  a: number;
  b: number;
  progress?: number;
  c?: string;
  width?: number;
  nib?: boolean;
  opacity?: number;
  dash?: string;
}> = ({ f, fn, a, b, progress = 1, c = color.ink, width = stroke.curve, nib = true, opacity = 1, dash }) => {
  if (progress <= 0) return null;
  const end = a + (b - a) * progress;
  const pts = polyline(f, fn, a, end, Math.max(2, Math.ceil(240 * progress)));
  const head = pts[pts.length - 1];
  const inking = nib && progress < 1;
  return (
    <g opacity={opacity}>
      <path d={d(pts)} fill="none" stroke={c} strokeWidth={width} strokeLinecap="round" strokeLinejoin="round" strokeDasharray={dash} />
      {inking && <circle cx={head[0]} cy={head[1]} r={width * 1.25} fill={c} />}
    </g>
  );
};

export type Tick = { v: number; label?: Token[] };

/** Range-frame axes: x from x0..x1 on y = 0, y from y0..y1 on x = 0. */
export const RangeAxes: React.FC<{
  f: PlotFrame;
  x: [number, number];
  y: [number, number];
  xTicks?: Tick[];
  yTicks?: Tick[];
  progress?: number;
  labels?: number; // 0..1 opacity of tick labels
}> = ({ f, x, y, xTicks = [], yTicks = [], progress = 1, labels = 1 }) => {
  const [ax0, ay] = px(f, x[0], 0);
  const [ax1] = px(f, x[0] + (x[1] - x[0]) * progress, 0);
  const [yx, yTop] = px(f, 0, y[1]);
  const [, yBot] = px(f, 0, y[0]);
  const ym = (yTop + yBot) / 2;
  const half = ((yBot - yTop) / 2) * progress;
  const tl = 9;
  return (
    <g>
      <line x1={ax0} y1={ay} x2={ax1} y2={ay} stroke={color.ink2} strokeWidth={stroke.axis} strokeLinecap="round" />
      <line x1={yx} y1={ym - half} x2={yx} y2={ym + half} stroke={color.ink2} strokeWidth={stroke.axis} strokeLinecap="round" />
      {xTicks.map((t) => {
        const [tx] = px(f, t.v, 0);
        return (
          <g key={`x${t.v}`} opacity={progress >= 1 ? 1 : 0}>
            <line x1={tx} y1={ay} x2={tx} y2={ay + tl} stroke={color.ink2} strokeWidth={stroke.axis} />
            {t.label && (
              <g className="halo" opacity={labels} transform={`translate(${tx} ${ay + tl + type.label * 1.25})`}>
                <FormulaG tokens={t.label.map((k) => ({ color: color.ink2, ...k }))} opts={{ size: type.label, align: "center" }} />
              </g>
            )}
          </g>
        );
      })}
      {yTicks.map((t) => {
        const [, ty] = px(f, 0, t.v);
        return (
          <g key={`y${t.v}`} opacity={progress >= 1 ? 1 : 0}>
            <line x1={yx - tl} y1={ty} x2={yx} y2={ty} stroke={color.ink2} strokeWidth={stroke.axis} />
            {t.label && (
              <g className="halo" opacity={labels} transform={`translate(${yx - tl - 10} ${ty + type.label * 0.32})`}>
                <FormulaG tokens={t.label.map((k) => ({ color: color.ink2, ...k }))} opts={{ size: type.label, align: "right" }} />
              </g>
            )}
          </g>
        );
      })}
    </g>
  );
};

/** Tangent to fn at x0 (slope m), visual half-length in page px; grow 0..1+ (spring). */
export const Tangent: React.FC<{
  f: PlotFrame;
  x0: number;
  y0: number;
  m: number;
  half?: number;
  grow?: number;
  c?: string;
  width?: number;
  opacity?: number;
}> = ({ f, x0, y0, m, half = 190, grow = 1, c = color.accent, width = stroke.tangent, opacity = 1 }) => {
  const [cx, cy] = px(f, x0, y0);
  // direction in page px (y down)
  const dx = f.ux;
  const dy = -m * f.uy;
  const L = Math.hypot(dx, dy);
  const h = half * Math.max(0, grow);
  if (h < 0.5) return null; // a zero-length line would still paint a round-cap dot
  return (
    <line
      x1={cx - (dx / L) * h}
      y1={cy - (dy / L) * h}
      x2={cx + (dx / L) * h}
      y2={cy + (dy / L) * h}
      stroke={c}
      strokeWidth={width}
      strokeLinecap="round"
      opacity={opacity}
    />
  );
};

/**
 * A note set along a tangent, like lettering engraved on a ruler:
 * `at` px from the point along the line, `lift` px above it.
 */
export const TangentNote: React.FC<{
  f: PlotFrame;
  x0: number;
  y0: number;
  m: number;
  at: number;
  lift?: number;
  children: React.ReactNode;
  opacity?: number;
  size?: number;
}> = ({ f, x0, y0, m, at, lift = 14, children, opacity = 1, size = type.label }) => {
  const [cx, cy] = px(f, x0, y0);
  const dx = f.ux;
  const dy = -m * f.uy;
  const L = Math.hypot(dx, dy);
  const ux = dx / L;
  const uy = dy / L;
  const ang = (Math.atan2(dy, dx) * 180) / Math.PI;
  const x = cx + ux * at + uy * lift;
  const y = cy + uy * at - ux * lift;
  return (
    <text
      className="halo"
      transform={`translate(${x} ${y}) rotate(${ang})`}
      textAnchor="middle"
      opacity={opacity}
      fill={color.ink}
      style={{ fontFamily: font.serif, fontSize: size, fontFeatureSettings: features.figures }}
    >
      {children}
    </text>
  );
};

/** Slope triangle: dashed run of 1 unit, solid rise of m units (the derivative). */
export const SlopeTriangle: React.FC<{
  f: PlotFrame;
  x0: number;
  y0: number;
  m: number;
  run?: number;
  progress?: number;
  opacity?: number;
}> = ({ f, x0, y0, m, run = 1, progress = 1, opacity = 1 }) => {
  if (progress <= 0) return null;
  const [ax, ay] = px(f, x0, y0);
  const [bx] = px(f, x0 + run, y0);
  const [, cy] = px(f, x0 + run, y0 + m * run);
  const p1 = Math.min(1, progress * 2);
  const p2 = Math.max(0, progress * 2 - 1);
  return (
    <g opacity={opacity}>
      <line x1={ax} y1={ay} x2={ax + (bx - ax) * p1} y2={ay} stroke={color.ink3} strokeWidth={stroke.hairline * 1.3} strokeDasharray="2 7" strokeLinecap="round" />
      {p2 > 0 && <line x1={bx} y1={ay} x2={bx} y2={ay + (cy - ay) * p2} stroke={color.accent} strokeWidth={stroke.emphasis} strokeLinecap="round" />}
    </g>
  );
};

/** A point with a 2.5px paper ring so it separates from the line under it. */
export const Dot: React.FC<{ f: PlotFrame; x: number; y: number; c?: string; r?: number; scale?: number; opacity?: number }> = ({
  f,
  x,
  y,
  c = color.ink,
  r = stroke.dot,
  scale = 1,
  opacity = 1,
}) => {
  const [cx, cy] = px(f, x, y);
  return <circle cx={cx} cy={cy} r={r * scale} fill={c} stroke={color.paper} strokeWidth={stroke.ring} opacity={opacity} />;
};

/** Figure label text in Garamond (SVG, baseline-exact). */
export const Label: React.FC<{
  x: number;
  y: number;
  children: React.ReactNode;
  size?: number;
  c?: string;
  italic?: boolean;
  anchor?: "start" | "middle" | "end";
  opacity?: number;
  figures?: boolean;
  caps?: boolean;
}> = ({ x, y, children, size = type.label, c = color.ink2, italic, anchor = "start", opacity = 1, figures, caps }) => (
  <text
    x={x}
    y={y}
    fill={c}
    textAnchor={anchor}
    opacity={opacity}
    style={{
      fontFamily: font.serif,
      fontSize: size,
      fontStyle: italic ? "italic" : "normal",
      fontFeatureSettings: caps ? features.smallCaps : figures ? features.figures : features.text,
      letterSpacing: caps ? tracking.smallCaps : undefined,
      textTransform: caps ? "uppercase" : undefined,
      fontWeight: caps ? 500 : undefined,
    }}
  >
    {children}
  </text>
);
