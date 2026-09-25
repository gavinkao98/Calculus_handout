/**
 * §3.1 kit: the beat clock, the sheet (page under the rostrum camera),
 * whole-formula TeX placement with an ink wipe, arrows, hatching, and the
 * margin "ledger" of the two debts the proof owes.
 */
import React, { createContext, useContext } from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { color, ease, features, font, springs, stroke, type } from "../theme";
import { Camera, Page } from "../components/Shell";
import { Vignette } from "../components/Paper";
import { SmallCaps, clamp, measure } from "../components/Type";
import { tex } from "../math/tex";
import { BeatT } from "./timing";

// ── Beat clock ────────────────────────────────────────────────────────────
export const SceneCtx = createContext<{ beats: BeatT[]; dur: number }>({ beats: [], dur: 300 });

export const useS = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const { beats, dur } = useContext(SceneCtx);
  const find = (id: string) => {
    const b = beats.find((x) => x.id === id);
    if (!b) throw new Error(`no beat "${id}" (have: ${beats.map((x) => x.id).join(", ")})`);
    return b;
  };
  /** frame at which beat `id` starts, plus `frac` of its length */
  const at = (id: string, frac = 0) => {
    const b = find(id);
    return b.start + (b.end - b.start) * frac;
  };
  const end = (id: string) => find(id).end;
  /** 0→1 over `len` frames starting `delay` frames after beat `id` */
  const p = (id: string, len = 24, delay = 0, easing = ease.ink) =>
    interpolate(f, [at(id) + delay, at(id) + delay + len], [0, 1], { ...clamp, easing });
  /** same, from an absolute frame */
  const pf = (from: number, len = 24, easing = ease.ink) => interpolate(f, [from, from + len], [0, 1], { ...clamp, easing });
  const sp = (id: string, delay = 0, config: Parameters<typeof spring>[0]["config"] = springs.pop) =>
    spring({ frame: f - at(id) - delay, fps, config });
  return { f, fps, dur, at, end, p, pf, sp };
};

// ── Camera path ───────────────────────────────────────────────────────────
export type Cam = { cx: number; cy: number; s: number };
const mix = (a: Cam, b: Cam, t: number): Cam => ({
  cx: a.cx + (b.cx - a.cx) * t,
  cy: a.cy + (b.cy - a.cy) * t,
  s: a.s * Math.pow(b.s / a.s, t),
});
/** moves: [start frame, target, length] applied in order (each blends from wherever the camera is) */
export const camPath = (f: number, start: Cam, moves: Array<[number, Cam, number?]>): Cam =>
  moves.reduce((c, [t0, to, len = 48]) => mix(c, to, interpolate(f, [t0, t0 + len], [0, 1], { ...clamp, easing: ease.camera })), start);
export const HOME: Cam = { cx: 960, cy: 540, s: 1 };
/** never show the desk: clamp the centre so the frame stays on the sheet (when the sheet is big enough) */
export const keepOnPage = (c: Cam, w: number, h: number): Cam => {
  const hw = 960 / c.s;
  const hh = 540 / c.s;
  const cx = w >= 2 * hw ? Math.min(Math.max(c.cx, hw), w - hw) : w / 2;
  const cy = h >= 2 * hh ? Math.min(Math.max(c.cy, hh), h - hh) : h / 2;
  return { cx, cy, s: c.s };
};

// ── The sheet ─────────────────────────────────────────────────────────────
export const HEAD_LEFT = "Chapter 3 · Differentiation Rules";
export const Sheet: React.FC<{
  folio: number;
  title: string;
  cam?: Cam;
  w?: number;
  h?: number;
  head?: boolean;
  device?: boolean;
  children: React.ReactNode;
}> = ({ folio, title, cam = HOME, w = 1920, h = 1080, head = true, device = true, children }) => (
  <AbsoluteFill style={{ backgroundColor: "#2F2A24" }}>
    <Camera {...keepOnPage(cam, w, h)}>
      <Page w={w} h={h} head={head ? { left: HEAD_LEFT, right: title, folio: String(folio) } : null} device={device}>
        {children}
      </Page>
    </Camera>
    <Vignette />
  </AbsoluteFill>
);

// ── Ink wipe (left → right, soft edge, small rise) ────────────────────────
export const wipe = (p: number, rise = 6): React.CSSProperties => {
  if (p >= 1) return {};
  if (p <= 0) return { opacity: 0 };
  const e = p * 130 - 15;
  const m = `linear-gradient(90deg, #000 ${e - 15}%, transparent ${e + 15}%)`;
  return { WebkitMaskImage: m, maskImage: m, translate: `0px ${(1 - p) * rise}px` };
};

// ── Whole-formula TeX, baseline-anchored at (x, y) ────────────────────────
export const texW = (src: string, size: number, display = true) => (tex(src, display).w / 1000) * size * font.mathScale;
export const M: React.FC<{
  x: number;
  y: number;
  t: string;
  size?: number;
  align?: "left" | "center" | "right";
  p?: number;
  c?: string;
  o?: number;
  display?: boolean;
  bg?: boolean; // paper knock-out behind the formula (labels set over hatching)
  style?: React.CSSProperties;
}> = ({ x, y, t, size = type.proof, align = "left", p = 1, c = color.ink, o = 1, display = true, bg, style }) => {
  const g = tex(t, display);
  const k = (size * font.mathScale) / 1000;
  const w = g.w * k;
  const left = align === "center" ? x - w / 2 : align === "right" ? x - w : x;
  if (p <= 0 || o <= 0) return null;
  return (
    <svg
      viewBox={`${g.minX} ${g.minY} ${g.w} ${g.h}`}
      width={w}
      height={g.h * k}
      style={{ position: "absolute", left, top: y + g.minY * k, overflow: "visible", color: c, opacity: o, ...(bg ? { background: color.paper, outline: `6px solid ${color.paper}`, borderRadius: 3 } : {}), ...wipe(p), ...style }}
      dangerouslySetInnerHTML={{ __html: g.body }}
    />
  );
};

/** Garamond text block (top-left at x, y) with the ink wipe */
export const Txt: React.FC<{
  x: number;
  y: number;
  w?: number;
  size?: number;
  italic?: boolean;
  c?: string;
  p?: number;
  o?: number;
  align?: "left" | "center" | "right";
  weight?: number;
  lh?: number;
  children: React.ReactNode;
  style?: React.CSSProperties;
}> = ({ x, y, w, size = type.body, italic, c = color.ink, p = 1, o = 1, align = "left", weight = 400, lh = 1.3, children, style }) => {
  if (p <= 0 || o <= 0) return null;
  const width = w ?? 1400;
  const left = align === "center" ? x - width / 2 : align === "right" ? x - width : x;
  return (
    <div
      style={{
        position: "absolute",
        left,
        top: y,
        width,
        textAlign: align,
        fontFamily: font.serif,
        fontSize: size,
        fontStyle: italic ? "italic" : "normal",
        fontWeight: weight,
        lineHeight: lh,
        color: c,
        opacity: o,
        fontFeatureSettings: features.text,
        textShadow: `0 0 3px ${color.paper}, 0 0 7px ${color.paper}`, // paper halo when set over a line
        ...wipe(p),
        ...style,
      }}
    >
      {children}
    </div>
  );
};

/** Small-caps kicker with a short rubric rule above it */
export const Kicker: React.FC<{ x: number; y: number; p?: number; c?: string; children: React.ReactNode; rule?: boolean }> = ({
  x,
  y,
  p = 1,
  c = color.accent,
  children,
  rule = true,
}) => (
  <div style={{ position: "absolute", left: x, top: y, ...wipe(p, 0) }}>
    {rule && <div style={{ width: 56, height: 2.5, background: color.accent, marginBottom: 14 }} />}
    <SmallCaps color={c}>{children}</SmallCaps>
  </div>
);

// ── Page-wide SVG layer ───────────────────────────────────────────────────
export const Layer: React.FC<{ w?: number; h?: number; children: React.ReactNode; style?: React.CSSProperties }> = ({
  w = 1920,
  h = 1080,
  children,
  style,
}) => (
  <svg width={w} height={h} style={{ position: "absolute", left: 0, top: 0, overflow: "visible", ...style }}>
    {children}
  </svg>
);

/** Print-style fills: hatching at 45° / 135°, and a stipple. */
export const Hatches: React.FC = () => (
  <defs>
    <pattern id="h45" width="14" height="14" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
      <line x1="0" y1="0" x2="0" y2="14" stroke={color.ink} strokeWidth="2.2" opacity="0.55" />
    </pattern>
    <pattern id="h135" width="16" height="16" patternUnits="userSpaceOnUse" patternTransform="rotate(-45)">
      <line x1="0" y1="0" x2="0" y2="16" stroke={color.ink2} strokeWidth="1.6" opacity="0.5" />
    </pattern>
    <pattern id="dots" width="12" height="12" patternUnits="userSpaceOnUse">
      <circle cx="6" cy="6" r="2.2" fill={color.ochre} opacity="0.7" />
    </pattern>
  </defs>
);

/** A pen-drawn arrow: the shaft inks from the tail, the head lands at the end. `bend` bows it (px, +left). */
export const Arrow: React.FC<{
  x1: number;
  y1: number;
  x2: number;
  y2: number;
  p?: number;
  c?: string;
  w?: number;
  head?: number;
  bend?: number;
  dash?: string;
  o?: number;
}> = ({ x1, y1, x2, y2, p = 1, c = color.ink, w = 3, head = 16, bend = 0, dash, o = 1 }) => {
  if (p <= 0) return null;
  const mx = (x1 + x2) / 2;
  const my = (y1 + y2) / 2;
  const L = Math.hypot(x2 - x1, y2 - y1) || 1;
  const nx = -(y2 - y1) / L;
  const ny = (x2 - x1) / L;
  const qx = mx + nx * bend;
  const qy = my + ny * bend;
  const pt = (t: number): [number, number] => [
    (1 - t) * (1 - t) * x1 + 2 * (1 - t) * t * qx + t * t * x2,
    (1 - t) * (1 - t) * y1 + 2 * (1 - t) * t * qy + t * t * y2,
  ];
  const n = 40;
  const pts: string[] = [];
  for (let i = 0; i <= n; i++) {
    const [a, b] = pt((i / n) * p);
    pts.push(`${i ? "L" : "M"}${a.toFixed(1)} ${b.toFixed(1)}`);
  }
  const [ex, ey] = pt(p);
  const [bx, by] = pt(Math.max(0, p - 0.02));
  const ang = Math.atan2(ey - by, ex - bx);
  const hp = interpolate(p, [0.75, 1], [0, 1], clamp);
  const h = head * hp;
  return (
    <g opacity={o}>
      <path d={pts.join("")} fill="none" stroke={c} strokeWidth={w} strokeLinecap="round" strokeDasharray={dash} />
      {h > 0.5 && (
        <path
          d={`M${ex - Math.cos(ang - 0.42) * h} ${ey - Math.sin(ang - 0.42) * h} L${ex} ${ey} L${ex - Math.cos(ang + 0.42) * h} ${ey - Math.sin(ang + 0.42) * h}`}
          fill="none"
          stroke={c}
          strokeWidth={w}
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      )}
    </g>
  );
};

/** A line drawn on from (x1,y1) */
export const Ln: React.FC<{ x1: number; y1: number; x2: number; y2: number; p?: number; c?: string; w?: number; dash?: string; o?: number }> = ({
  x1,
  y1,
  x2,
  y2,
  p = 1,
  c = color.ink,
  w = stroke.hairline,
  dash,
  o = 1,
}) =>
  p <= 0 ? null : (
    <line x1={x1} y1={y1} x2={x1 + (x2 - x1) * p} y2={y1 + (y2 - y1) * p} stroke={c} strokeWidth={w} strokeLinecap="round" strokeDasharray={dash} opacity={o} />
  );

// ── The ledger: two debts, written in the margin, struck through when paid ─
export type LedgerState = { show: number; items: Array<{ show: number; paid: number; focus?: number }> };
const DEBTS = [
  { n: "1", words: "cos is continuous" },
  { n: "2", t: String.raw`\dfrac{\sin\theta}{\theta}\to 1` },
];
export const Ledger: React.FC<{ x?: number; y?: number; st: LedgerState }> = ({ x = 120, y = 300, st }) => {
  if (st.show <= 0) return null;
  return (
    <div style={{ position: "absolute", left: x, top: y, width: 290, ...wipe(st.show, 0) }}>
      <div style={{ width: 56, height: 2.5, background: color.accent, marginBottom: 14 }} />
      <SmallCaps color={color.accent}>Owed</SmallCaps>
      {DEBTS.map((d, i) => {
        const it = st.items[i];
        if (!it || it.show <= 0) return null;
        const top = 70 + i * 170;
        const k = (48 * font.mathScale) / 1000;
        const g = d.t ? tex(d.t, true) : null;
        const W = g ? g.w * k : measure(d.words ?? "", 36, { italic: true });
        return (
          <div key={d.n} style={{ position: "absolute", left: 0, top, width: 290, height: 130, ...wipe(it.show, 4) }}>
            {/* focus bar */}
            <div
              style={{
                position: "absolute",
                left: -22,
                top: 0,
                width: 4,
                height: 80,
                background: color.accent,
                opacity: it.focus ?? 0,
              }}
            />
            <span
              style={{
                position: "absolute",
                left: 0,
                top: 10,
                fontFamily: font.serif,
                fontSize: 30,
                color: color.accent,
                fontFeatureSettings: "'lnum' 1",
              }}
            >
              {d.n}
            </span>
            {g ? (
              <svg
                viewBox={`${g.minX} ${g.minY} ${g.w} ${g.h}`}
                width={g.w * k}
                height={g.h * k}
                style={{ position: "absolute", left: 34, top: 40 + g.minY * k, overflow: "visible", color: color.ink, opacity: 1 - 0.45 * it.paid }}
                dangerouslySetInnerHTML={{ __html: g.body }}
              />
            ) : (
              <span
                style={{
                  position: "absolute",
                  left: 34,
                  top: 12,
                  fontFamily: font.serif,
                  fontSize: 36,
                  fontStyle: "italic",
                  whiteSpace: "nowrap",
                  color: color.ink,
                  opacity: 1 - 0.45 * it.paid,
                }}
              >
                {d.words}
              </span>
            )}
            {/* strike + stamp */}
            <div
              style={{
                position: "absolute",
                left: 28,
                top: g ? 27 : 36,
                width: (W + 16) * it.paid,
                height: 3,
                background: color.accent,
                rotate: "-3deg",
                transformOrigin: "0 50%",
              }}
            />
            <div style={{ position: "absolute", left: 34, top: g ? 96 : 64, ...wipe(interpolate(it.paid, [0.5, 1], [0, 1], clamp), 0) }}>
              <SmallCaps color={color.accent} size={26}>
                Paid in full
              </SmallCaps>
            </div>
          </div>
        );
      })}
    </div>
  );
};

/** Section-mark stamp used for margin cautions etc. */
export const Rubric: React.FC<{ x: number; y: number; h: number; p?: number }> = ({ x, y, h, p = 1 }) => (
  <div style={{ position: "absolute", left: x, top: y, width: 4, height: h * p, background: color.accent }} />
);
