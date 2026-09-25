/**
 * Q7 kit: the sheet (own running head), the math → page map, and the billiard
 * drawing primitives — a table with its pockets, a path with a rolling ball,
 * and the unfolding view (copies of the table turning over their walls like
 * pages). Beat clock, TeX, arrows and the label guard come from the §3.1 kit.
 */
import React from "react";
import { AbsoluteFill } from "remotion";
import { color, stroke } from "../theme";
import { Camera, Page } from "../components/Shell";
import { Vignette } from "../components/Paper";
import { Cam, HOME, Mark, Pt, keepOnPage } from "../s31/kit";
import { Shot, V, Wall, at, flip, foldedInto, polyAt } from "./geo";

export * from "../s31/kit";

// ── Palette roles (validated inks of the paper system) ────────────────────
export const HOMEC = color.cobalt; // copies of the centre: "home"
export const POCKET = color.accent; // corner pockets (odd, odd)
export const EDGE = color.ochre; // edge-midpoint pockets (odd, even) / (even, odd); also the mirror hinge

// ── The sheet ─────────────────────────────────────────────────────────────
export const HEAD_LEFT = "NTU Science Talent Program · 2026 Exam";
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

// ── Math → page ───────────────────────────────────────────────────────────
export type World = { ox: number; oy: number; u: number };
export const px = (W: World, [x, y]: V): Pt => [W.ox + x * W.u, W.oy - y * W.u];
export const dOf = (W: World, pts: V[]) => pts.map((p, i) => `${i ? "L" : "M"}${px(W, p)[0].toFixed(1)} ${px(W, p)[1].toFixed(1)}`).join("");
export const pxs = (W: World, pts: V[]): Pt[] => pts.map((p) => px(W, p));

export const R_POCKET = 12;
export const W_POCKET = 3.4;
export const R_BALL = 11;

/** a pocket: a hollow ring (squashed to an ellipse while its table is turning over) */
export const Pocket: React.FC<{ W: World; p: V; c?: string; o?: number; sx?: number; sy?: number; r?: number; fill?: string }> = ({
  W,
  p,
  c = POCKET,
  o = 1,
  sx = 1,
  sy = 1,
  r = R_POCKET,
  fill = color.paper,
}) => {
  const [x, y] = px(W, p);
  return <ellipse cx={x} cy={y} rx={Math.max(0.5, r * sx)} ry={Math.max(0.5, r * sy)} fill={fill} stroke={c} strokeWidth={W_POCKET} opacity={o} />;
};
export const HomeDot: React.FC<{ W: World; p: V; o?: number; r?: number; sx?: number; sy?: number }> = ({ W, p, o = 1, r = 8, sx = 1, sy = 1 }) => {
  const [x, y] = px(W, p);
  return <ellipse cx={x} cy={y} rx={Math.max(0.5, r * sx)} ry={Math.max(0.5, r * sy)} fill={HOMEC} opacity={o} />;
};
export const Ball: React.FC<{ W: World; p: V; o?: number; r?: number }> = ({ W, p, o = 1, r = R_BALL }) => {
  const [x, y] = px(W, p);
  return <circle cx={x} cy={y} r={r} fill={color.ink} stroke={color.paper} strokeWidth={stroke.ring + 0.5} opacity={o} />;
};

export type PocketSet = "corners" | "all" | "none";
const CORNERS: V[] = [
  [1, 1],
  [-1, 1],
  [-1, -1],
  [1, -1],
];
const MIDS: V[] = [
  [1, 0],
  [0, 1],
  [-1, 0],
  [0, -1],
];

/**
 * One copy of the table with centre c (math units). `map` bends every point
 * (used for the page-turn); `sx`/`sy` squash round things the same way.
 */
export const Table: React.FC<{
  W: World;
  c?: V;
  pockets?: PocketSet;
  real?: boolean;
  o?: number;
  draw?: number; // 0→1 the outline inks on
  home?: boolean; // show the centre mark
  fill?: string;
  fillO?: number;
  map?: (p: V) => V;
  sx?: number;
  sy?: number;
  lineW?: number;
  lineC?: string;
  pocketO?: number;
}> = ({ W, c = [0, 0], pockets = "corners", real, o = 1, draw = 1, home = true, fill, fillO = 1, map = (p) => p, sx = 1, sy = 1, lineW, lineC, pocketO = 1 }) => {
  if (o <= 0) return null;
  const q = (p: V): V => map([c[0] + p[0], c[1] + p[1]]);
  const outline = [q([-1, -1]), q([1, -1]), q([1, 1]), q([-1, 1]), q([-1, -1])];
  const per = 4 * 2 * W.u;
  const lw = lineW ?? (real ? 4.2 : 2.2);
  return (
    <g opacity={o}>
      {fill && <path d={dOf(W, outline) + "Z"} fill={fill} opacity={fillO} />}
      <path
        d={dOf(W, outline)}
        fill="none"
        stroke={lineC ?? (real ? color.ink : color.ink2)}
        strokeWidth={lw}
        strokeLinejoin="miter"
        strokeDasharray={draw < 1 ? `${per * draw} ${per}` : undefined}
      />
      {home && draw >= 1 && <HomeDot W={W} p={q([0, 0])} sx={sx} sy={sy} r={real ? 8 : 7} />}
      {pockets !== "none" && draw >= 1 && CORNERS.map((p, i) => <Pocket key={`c${i}`} W={W} p={q(p)} sx={sx} sy={sy} o={pocketO} />)}
      {pockets === "all" && draw >= 1 && MIDS.map((p, i) => <Pocket key={`m${i}`} W={W} p={q(p)} c={EDGE} sx={sx} sy={sy} o={pocketO} />)}
    </g>
  );
};

/** guard marks for a table drawn by `Table` (outline + pockets + centre) */
export const tableMarks = (W: World, name: string, c: V = [0, 0], pockets: PocketSet = "corners", real = true, on = true): Mark[] => {
  const q = (p: V): V => [c[0] + p[0], c[1] + p[1]];
  const ms: Mark[] = [
    { name: `${name} outline`, pts: pxs(W, [q([-1, -1]), q([1, -1]), q([1, 1]), q([-1, 1]), q([-1, -1])]), w: real ? 4.2 : 2.2, on },
    { name: `${name} centre`, pts: [px(W, q([0, 0]))], w: 16, on },
  ];
  if (pockets !== "none") CORNERS.forEach((p) => ms.push({ name: `${name} pocket`, pts: [px(W, q(p))], w: 2 * R_POCKET + W_POCKET, on }));
  if (pockets === "all") MIDS.forEach((p) => ms.push({ name: `${name} edge pocket`, pts: [px(W, q(p))], w: 2 * R_POCKET + W_POCKET, on }));
  return ms;
};

/** a path (math polyline) inked up to `frac` of its length, with the ball at its head */
export const Rolling: React.FC<{
  W: World;
  pts: V[];
  frac: number;
  ball?: boolean;
  c?: string;
  w?: number;
  o?: number;
  ballO?: number;
  dash?: string;
}> = ({ W, pts, frac, ball = true, c = color.ink, w = 3.6, o = 1, ballO = 1, dash }) => {
  if (frac <= 0 || o <= 0) return null;
  const { p, upto } = polyAt(pts, frac);
  return (
    <g opacity={o}>
      <path d={dOf(W, upto)} fill="none" stroke={c} strokeWidth={w} strokeLinecap="round" strokeLinejoin="round" strokeDasharray={dash} />
      {ball && <Ball W={W} p={p} o={ballO} />}
    </g>
  );
};

/** an expanding ring (arrival flash) */
export const Flash: React.FC<{ W: World; p: V; t: number; c: string; r0?: number; r1?: number }> = ({ W, p, t, c, r0 = 12, r1 = 46 }) => {
  if (t <= 0 || t >= 1) return null;
  const [x, y] = px(W, p);
  return <circle cx={x} cy={y} r={r0 + (r1 - r0) * t} fill="none" stroke={c} strokeWidth={4 * (1 - t) + 0.5} opacity={1 - t} />;
};

// ── The unfolding view ────────────────────────────────────────────────────
/**
 * `stage` ∈ [0, n]: k = ⌊stage⌋ reflections done, and the (k+1)-th copy is
 * turning over its wall with progress stage − k. At stage k the line is
 * straight through copies 0..k and its remainder is folded back into copy k;
 * stage 0 is the real bouncing path, stage n the straight line.
 */
export const Unfold: React.FC<{
  W: World;
  s: Shot;
  stage: number;
  pockets?: PocketSet;
  lineFrac?: number; // how much of the path is inked (0→1 of the full length)
  pathC?: string;
  hinge?: boolean;
  ball?: V | null;
  copiesO?: number;
}> = ({ W, s, stage, pockets = "corners", lineFrac = 1, pathC = color.ink, hinge = true, ball = null, copiesO = 1 }) => {
  const n = s.cross.length;
  const st = Math.max(0, Math.min(n, stage));
  const k = Math.min(n, Math.floor(st + 1e-9));
  const u = st - k;
  const sigma = Math.cos(Math.PI * u);
  const tK1 = k < n ? s.cross[k] : s.T; // end of the straight part
  const straight: V[] = [
    [0, 0],
    at(s, tK1),
  ];
  const wall: Wall | null = k < n ? s.walls[k][0] : null;
  const turning = u > 1e-4 && wall && k + 1 <= n;
  // remainder after the straight part
  let rest: V[] = [];
  if (k < n) {
    if (turning) rest = foldedInto(s, tK1, s.tiles[k + 1]).map((p) => flip(p, wall!, sigma));
    else rest = foldedInto(s, tK1, s.tiles[k]);
  }
  const full = [...straight, ...rest.slice(1)];
  const shown = lineFrac >= 1 ? full : polyAt(full, lineFrac).upto;
  const squash = Math.abs(sigma);
  const sx = turning && wall!.axis === "x" ? squash : 1;
  const sy = turning && wall!.axis === "y" ? squash : 1;
  // hinge: the wall being turned over, along the side of copy k
  const hingeSeg: V[] | null = wall
    ? wall.axis === "x"
      ? [
          [wall.at, 2 * s.tiles[k][1] - 1],
          [wall.at, 2 * s.tiles[k][1] + 1],
        ]
      : [
          [2 * s.tiles[k][0] - 1, wall.at],
          [2 * s.tiles[k][0] + 1, wall.at],
        ]
    : null;
  const hingeO = turning ? Math.sin(Math.PI * u) : 0;
  return (
    <g>
      {s.tiles.slice(0, k + 1).map((c, i) => (
        <Table key={i} W={W} c={[2 * c[0], 2 * c[1]]} real={i === 0} pockets={pockets} o={i === 0 ? 1 : copiesO} />
      ))}
      {turning && (
        <Table
          W={W}
          c={[2 * s.tiles[k + 1][0], 2 * s.tiles[k + 1][1]]}
          map={(p) => flip(p, wall!, sigma)}
          sx={sx}
          sy={sy}
          pockets={pockets}
          fill={color.paperShade}
          fillO={0.35 + 0.5 * (1 - squash)}
          o={copiesO}
        />
      )}
      {hinge && hingeSeg && hingeO > 0 && (
        <path d={dOf(W, hingeSeg)} stroke={EDGE} strokeWidth={7} strokeLinecap="round" opacity={0.85 * hingeO} />
      )}
      <path d={dOf(W, shown)} fill="none" stroke={pathC} strokeWidth={4} strokeLinecap="round" strokeLinejoin="round" />
      {ball && <Ball W={W} p={ball} />}
    </g>
  );
};
