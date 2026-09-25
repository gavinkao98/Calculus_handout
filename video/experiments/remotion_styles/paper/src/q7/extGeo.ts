/**
 * Exact geometry for the zh extension (ext_room, ext_family). Everything is a
 * piecewise-linear map applied to polylines split at its break lines, so the
 * drawn paths are the true ones (no sampling).
 *
 *   triFold   : the square [-1,1]^2 → the triangle O(0,0) M(1,0) K(1,1),
 *               (x, y) ↦ (max(|x|,|y|), min(|x|,|y|)); breaks on x=0, y=0, y=±x
 *   foldSteps : the same fold as three paper folds (y=0, then x=0, then y=x),
 *               each blendable 0→1 for the animation
 *   rectShot  : a shot from the corner (0,0) of the a×b table [0,a]×[0,b]
 */
import { V } from "./geo";

const EPS = 1e-9;

// ── Lines through the origin, as unit normals n: the line is n·p = 0 ────────
type Line = V;
const dot = (a: V, b: V) => a[0] * b[0] + a[1] * b[1];
const R2 = Math.SQRT1_2;

/** split a polyline where it crosses any of `lines` (inserting the exact crossing points) */
export const splitAt = (pts: V[], lines: Line[]): V[] => {
  const out: V[] = [pts[0]];
  for (let i = 1; i < pts.length; i++) {
    const a = pts[i - 1];
    const b = pts[i];
    const ts: number[] = [];
    for (const n of lines) {
      const da = dot(n, a);
      const db = dot(n, b);
      if ((da < -EPS && db > EPS) || (da > EPS && db < -EPS)) ts.push(da / (da - db));
    }
    ts.sort((x, y) => x - y);
    for (const t of ts) out.push([a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t]);
    out.push(b);
  }
  return out;
};

const TRI_BREAKS: Line[] = [
  [1, 0],
  [0, 1],
  [R2, -R2],
  [R2, R2],
];
export const triFold1 = ([x, y]: V): V => [Math.max(Math.abs(x), Math.abs(y)), Math.min(Math.abs(x), Math.abs(y))];
/** a square path folded into the triangle (exact: split at the fold lines first) */
export const triFold = (pts: V[]): V[] => splitAt(pts, TRI_BREAKS).map(triFold1);

// ── The fold as three paper folds ────────────────────────────────────────
/** fold k reflects the side n·p < 0 onto the side n·p > 0 */
export const FOLDS: Line[] = [
  [0, 1], // y = 0: the bottom half up
  [1, 0], // x = 0: the left half over
  [R2, -R2], // y = x: the upper-left triangle down
];
/** the reflection across fold n, blended: g = 0 identity, g = 1 mirrored (normal component × cos πg: a page turning over) */
const turn = (p: V, n: Line, g: number): V => {
  const d = dot(n, p);
  if (d >= 0) return p;
  const k = Math.cos(Math.PI * g);
  return [p[0] - d * n[0] + k * d * n[0], p[1] - d * n[1] + k * d * n[1]];
};
/** a point after folds 0..k-1 done and fold k at progress g (stage = k + g ∈ [0, 3]) */
export const foldPt = (p: V, stage: number): V => {
  let q = p;
  for (let k = 0; k < FOLDS.length; k++) {
    const g = Math.max(0, Math.min(1, stage - k));
    if (g <= 0) break;
    q = turn(q, FOLDS[k], g);
  }
  return q;
};
/** a polyline at a fold stage (split at every fold line first, so each piece moves rigidly) */
export const foldPath = (pts: V[], stage: number): V[] => {
  // split in the frame of each fold in turn: after fold k the path lives on its image
  let cur = pts;
  let out = pts;
  for (let k = 0; k < FOLDS.length; k++) {
    const g = Math.max(0, Math.min(1, stage - k));
    cur = splitAt(cur, [FOLDS[k]]);
    out = cur.map((p) => turn(p, FOLDS[k], g));
    if (g < 1) return out;
    cur = out;
  }
  return out;
};

/** Sutherland–Hodgman: the part of a convex polygon on the side n·p ≥ 0 (or ≤ 0) */
export const clip = (poly: V[], n: Line, keep: 1 | -1): V[] => {
  const out: V[] = [];
  for (let i = 0; i < poly.length; i++) {
    const a = poly[i];
    const b = poly[(i + 1) % poly.length];
    const da = keep * dot(n, a);
    const db = keep * dot(n, b);
    if (da >= -EPS) out.push(a);
    if ((da > EPS && db < -EPS) || (da < -EPS && db > EPS)) {
      const t = da / (da - db);
      out.push([a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t]);
    }
  }
  return out;
};
export const SQUARE: V[] = [
  [-1, -1],
  [1, -1],
  [1, 1],
  [-1, 1],
];
/**
 * The paper at a fold stage: the part lying still, and the flap turning over
 * (empty between folds). After all three folds: the triangle O M K.
 */
export const paperAt = (stage: number): { still: V[]; flap: V[] } => {
  let paper = SQUARE;
  for (let k = 0; k < FOLDS.length; k++) {
    const g = Math.max(0, Math.min(1, stage - k));
    if (g <= 0) return { still: paper, flap: [] };
    const still = clip(paper, FOLDS[k], 1);
    if (g >= 1) {
      paper = still;
      continue;
    }
    return { still, flap: clip(paper, FOLDS[k], -1).map((p) => turn(p, FOLDS[k], g)) };
  }
  return { still: paper, flap: [] };
};

// ── Rectangle a×b, corner pockets, shot from the corner (0,0) ────────────
const tri = (x: number, a: number) => {
  const m = ((x % (2 * a)) + 2 * a) % (2 * a);
  return m <= a ? m : 2 * a - m;
};
/**
 * The real path of the line t·dir, t ∈ [0, T], on [0,a]×[0,b]: its bounce
 * points are where the line meets x ∈ aZ or y ∈ bZ.
 */
export const rectShot = (a: number, b: number, dir: V, T: number): V[] => {
  const ts = new Set<number>();
  for (const [d, L] of [
    [dir[0], a],
    [dir[1], b],
  ] as const) {
    if (Math.abs(d) < EPS) continue;
    for (let m = 1; m * L < Math.abs(d) * T + EPS; m++) {
      const t = (m * L) / Math.abs(d);
      if (t < T - EPS) ts.add(Math.round(t * 1e9) / 1e9);
    }
  }
  const all = [0, ...[...ts].sort((x, y) => x - y), T];
  return all.map((t) => [tri(dir[0] * t, a), tri(dir[1] * t, b)] as V);
};
