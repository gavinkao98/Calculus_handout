/**
 * §3.1 kit: the beat clock, the sheet (page under the rostrum camera),
 * whole-formula TeX placement with an ink wipe, arrows, hatching, and the
 * margin "ledger" of the two debts the proof owes.
 */
import React, { createContext, useContext } from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { color, ease, features, font, labelGuard, springs, stroke, type } from "../theme";
import { Camera, Page } from "../components/Shell";
import { Vignette } from "../components/Paper";
import { SmallCaps, clamp, measure } from "../components/Type";
import { tex } from "../math/tex";
import { AlignedWord, findWord } from "../lib/words";
import { BeatT, LEAD } from "./timing";

// ── Beat clock ────────────────────────────────────────────────────────────
export const SceneCtx = createContext<{ id?: string; beats: BeatT[]; dur: number; words?: AlignedWord[] }>({ beats: [], dur: 300 });

export const useS = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const { id: scene = "?", beats, dur, words } = useContext(SceneCtx);
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
  /**
   * Frame at which `phrase` is spoken in this scene's narration (the Nth
   * occurrence, default first), or `undefined` if the scene has no
   * word-level alignment (mock manifest) — callers must then fall back to
   * `at(...)`. `afterFrame` (e.g. a beat's `at(id)`) disambiguates a phrase
   * that recurs earlier in the scene.
   */
  const atWord = (phrase: string, opts: { occurrence?: number; afterFrame?: number } = {}): number | undefined => {
    const afterSeconds = opts.afterFrame === undefined ? undefined : (opts.afterFrame - LEAD) / fps;
    const seconds = findWord(words, phrase, { occurrence: opts.occurrence, afterSeconds });
    return seconds === undefined ? undefined : LEAD + Math.round(seconds * fps);
  };
  /** graph-label collision guard for this scene at this frame (see `checkLabels`) */
  const guard = (marks: Mark[], labels: Lbl[]) => checkLabels(scene, f, marks, labels);
  return { f, fps, dur, at, end, p, pf, sp, atWord, guard };
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
  { n: "2", t: String.raw`\sin\theta/\theta\to 1` }, // marginalia: inline, like the running text beside it
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
        const g = d.t ? tex(d.t, false) : null;
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

// ── Graph-label guard (STYLE.md「圖上標籤」) ─────────────────────────────────
// A graph scene lists the marks drawn at this frame (curves as sampled polylines, axes and ticks as
// segments, dots as points, filled regions by their boundary) and the boxes of the labels set on the
// figure, all in page px. Every frame, each label that has finished inking and is visible is measured
// against every visible mark; closer than `labelGuard.clearance` → throw, so the render fails rather
// than ship a label touching the graph. Things that move (a spinning point, a sliding tangent) are
// registered only at their resting pose. A mark with `owner` (a leader line) is exempt for that one
// label only. A paper knock-out (`bg`) does not excuse a stroke underneath: same clearance, same throw.
export type Pt = [number, number];
export type Box = { l: number; t: number; r: number; b: number };
/** `w` = full stroke width (a dot: its diameter incl. the paper ring); `on: false` = not drawn now.
 *  `owner`: a leader line or tick that points at one label — exempt for that label only. */
export type Mark = { name: string; pts: Pt[]; w: number; on?: boolean; owner?: string };
/** `on` = fully inked and visible now. `rot`: the box is in a frame rotated by `a` rad about (x, y)
 *  (lettering set along a line), and marks are measured in that frame. */
export type Lbl = { name: string; box: Box; on: boolean; bg?: boolean; rot?: { a: number; x: number; y: number } };

/** glyph box of an `M` placed with the same props */
export const texBox = (t: string, x: number, y: number, size: number, align: "left" | "center" | "right" = "left", display = true): Box => {
  const g = tex(t, display);
  const k = (size * font.mathScale) / 1000;
  const w = g.w * k;
  const l = align === "center" ? x - w / 2 : align === "right" ? x - w : x;
  return { l, t: y + g.minY * k, r: l + w, b: y + (g.minY + g.h) * k };
};
/** glyph box of a one-line `Txt` with the same props (x is the anchor for `align`) */
export const txtBox = (s: string, x: number, y: number, size: number, o: { italic?: boolean; align?: "left" | "center" | "right"; lh?: number } = {}): Box => {
  const width = measure(s, size, { italic: o.italic });
  const l = o.align === "center" ? x - width / 2 : o.align === "right" ? x - width : x;
  const em = y + (((o.lh ?? 1.3) - 1) * size) / 2; // top of the em box inside the line box
  return { l, t: em + size * 0.12, r: l + width, b: em + size * 1.0 };
};
/** sample y = fn(v), v ∈ [a, b], into page px */
export const sample = (fn: (v: number) => number, a: number, b: number, X: (v: number) => number, Y: (v: number) => number, n = 200): Pt[] =>
  Array.from({ length: n + 1 }, (_, i) => {
    const v = a + ((b - a) * i) / n;
    return [X(v), Y(fn(v))] as Pt;
  });
/** circular arc in page px (angles counter-clockwise as on paper) */
export const arcPts = (cx: number, cy: number, r: number, a0: number, a1: number, n = 48): Pt[] =>
  Array.from({ length: n + 1 }, (_, i) => {
    const a = a0 + ((a1 - a0) * i) / n;
    return [cx + r * Math.cos(a), cy - r * Math.sin(a)] as Pt;
  });
export const toD = (pts: Pt[]) => pts.map(([x, y], i) => `${i ? "L" : "M"}${x.toFixed(1)} ${y.toFixed(1)}`).join("");

const segBox = (a: Pt, b: Pt, q: Box): number => {
  const inside = (p: Pt) => p[0] >= q.l && p[0] <= q.r && p[1] >= q.t && p[1] <= q.b;
  if (inside(a) || inside(b)) return 0;
  const C: Pt[] = [
    [q.l, q.t],
    [q.r, q.t],
    [q.r, q.b],
    [q.l, q.b],
  ];
  const cross = (p1: Pt, p2: Pt, p3: Pt, p4: Pt) => {
    const d = (p2[0] - p1[0]) * (p4[1] - p3[1]) - (p2[1] - p1[1]) * (p4[0] - p3[0]);
    if (Math.abs(d) < 1e-9) return false;
    const u = ((p3[0] - p1[0]) * (p4[1] - p3[1]) - (p3[1] - p1[1]) * (p4[0] - p3[0])) / d;
    const v = ((p3[0] - p1[0]) * (p2[1] - p1[1]) - (p3[1] - p1[1]) * (p2[0] - p1[0])) / d;
    return u >= 0 && u <= 1 && v >= 0 && v <= 1;
  };
  for (let i = 0; i < 4; i++) if (cross(a, b, C[i], C[(i + 1) % 4])) return 0;
  const ptBox = (p: Pt) => Math.hypot(Math.max(q.l - p[0], 0, p[0] - q.r), Math.max(q.t - p[1], 0, p[1] - q.b));
  const ptSeg = (p: Pt) => {
    const dx = b[0] - a[0];
    const dy = b[1] - a[1];
    const L = dx * dx + dy * dy || 1;
    const t = Math.max(0, Math.min(1, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / L));
    return Math.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy);
  };
  return Math.min(ptBox(a), ptBox(b), ...C.map(ptSeg));
};
/** gap (px) between a label box and a mark's outer edge; negative = overlap */
export const gap = (m: Mark, q: Box): number => {
  let d = m.pts.length === 1 ? segBox(m.pts[0], m.pts[0], q) : Infinity;
  for (let i = 1; i < m.pts.length && d > 0; i++) d = Math.min(d, segBox(m.pts[i - 1], m.pts[i], q));
  return d - m.w / 2;
};
export const checkLabels = (scene: string, frame: number, marks: Mark[], labels: Lbl[], clear: number = labelGuard.clearance) => {
  for (const l of labels) {
    if (!l.on) continue;
    for (const m of marks) {
      if (m.on === false || m.pts.length === 0 || m.owner === l.name) continue;
      const r = l.rot;
      const local = r
        ? { ...m, pts: m.pts.map(([x, y]): Pt => [(x - r.x) * Math.cos(r.a) + (y - r.y) * Math.sin(r.a), -(x - r.x) * Math.sin(r.a) + (y - r.y) * Math.cos(r.a)]) }
        : m;
      const d = gap(local, l.box);
      if (d < clear)
        throw new Error(
          `[label-guard] scene "${scene}" frame ${Math.round(frame)}: label "${l.name}" is ${d.toFixed(1)} px from mark "${m.name}" ` +
            `(clearance ${clear} px${l.bg ? "; a paper knock-out may not hide a stroke" : ""}). Move the label into empty space or add a leader line.`,
        );
    }
  }
};
/** the marks of an `Arrow` drawn with the same geometry (shaft + both head strokes), fully drawn */
export const arrowMarks = (name: string, x1: number, y1: number, x2: number, y2: number, o: { bend?: number; w?: number; head?: number; on?: boolean } = {}): Mark[] => {
  const { bend = 0, w = 3, head = 16, on = true } = o;
  const L = Math.hypot(x2 - x1, y2 - y1) || 1;
  const qx = (x1 + x2) / 2 - ((y2 - y1) / L) * bend;
  const qy = (y1 + y2) / 2 + ((x2 - x1) / L) * bend;
  const pt = (t: number): Pt => [(1 - t) * (1 - t) * x1 + 2 * (1 - t) * t * qx + t * t * x2, (1 - t) * (1 - t) * y1 + 2 * (1 - t) * t * qy + t * t * y2];
  const shaft = Array.from({ length: 41 }, (_, i) => pt(i / 40));
  const [bx, by] = pt(0.98);
  const ang = Math.atan2(y2 - by, x2 - bx);
  const wing = (s: number): Pt[] => [[x2 - Math.cos(ang + s * 0.42) * head, y2 - Math.sin(ang + s * 0.42) * head], [x2, y2]];
  return [
    { name, pts: shaft, w, on },
    { name: `${name} (head)`, pts: wing(-1), w, on },
    { name: `${name} (head)`, pts: wing(1), w, on },
  ];
};
/** the mark of a dot (radius r plus its paper ring) */
export const dotMark = (name: string, x: number, y: number, on = true, r: number = stroke.dot): Mark => ({ name, pts: [[x, y]], w: 2 * r + stroke.ring, on });
type MProps = React.ComponentProps<typeof M>;
/** the guard entry for an `M` rendered with the same props: `<M {...q} />` + `mLbl(q)` */
export const mLbl = (q: MProps, name: string = q.t): Lbl => ({
  name,
  box: texBox(q.t, q.x, q.y, q.size ?? type.proof, q.align, q.display ?? true),
  on: (q.p ?? 1) >= 1 && (q.o ?? 1) > 0.05,
  bg: q.bg,
});
/** the guard entry for a one-line `Txt` (pass the same x, y, size, italic, align as the Txt) */
export const tLbl = (s: string, x: number, y: number, size: number, p: number, o = 1, opt: { italic?: boolean; align?: "left" | "center" | "right"; lh?: number } = {}): Lbl => ({
  name: s,
  box: txtBox(s, x, y, size, opt),
  on: p >= 1 && o > 0.05,
});
