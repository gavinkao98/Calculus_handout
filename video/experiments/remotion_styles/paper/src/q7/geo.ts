/**
 * Square billiards, in math units. The real table is [-1,1]^2 with the ball
 * starting at the origin. Mirroring the table across its walls tiles the plane
 * with copies; the copy containing a point has centre (2a, 2b), and walls sit
 * on the odd lines x = odd, y = odd.
 *
 *   fold(x)  : the plane → the real table (triangle wave of period 4)
 *   toTile   : the real table → the copy with centre index a (2a)
 *
 * A shot with direction (dx, dy) is the straight line P(t) = t·(dx, dy) in the
 * plane; its real path is fold(P(t)). Everything below is exact (the fold is
 * piecewise linear, so a path is the polyline through its wall crossings).
 */
export type V = [number, number];

const par = (a: number) => (Math.abs(a) % 2 === 1 ? -1 : 1);
/** index of the copy (centre 2a) containing coordinate x (strictly inside) */
export const tileIdx = (x: number) => Math.round(x / 2);
/** the plane → the real table [-1, 1] (one coordinate) */
export const fold1 = (x: number) => {
  const a = tileIdx(x);
  return (x - 2 * a) * par(a);
};
/** the real table → copy a (one coordinate) */
export const toTile1 = (r: number, a: number) => 2 * a + par(a) * r;
export const fold = ([x, y]: V): V => [fold1(x), fold1(y)];
export const intoTile = (p: V, [a, b]: V): V => [toTile1(fold1(p[0]), a), toTile1(fold1(p[1]), b)];

export type Wall = { axis: "x" | "y"; at: number }; // x = at (vertical) or y = at (horizontal)
export type Shot = {
  dir: V;
  T: number; // the line runs t ∈ [0, T]
  cross: number[]; // crossing parameters t_1 < … < t_n (strictly inside (0, T))
  walls: Wall[][]; // walls crossed at each t_i (two at a corner)
  tiles: V[]; // tiles[i] = copy containing the line on (t_i, t_{i+1}); tiles[0] = [0,0]
};

const EPS = 1e-9;
const isOdd = (v: number) => Math.abs(v - Math.round(v)) < 1e-7 && Math.abs(Math.round(v)) % 2 === 1;

export const at = (s: Shot, t: number): V => [s.dir[0] * t, s.dir[1] * t];

/** the straight line from the origin in direction dir, for t ∈ [0, T] */
export const shot = (dir: V, T: number): Shot => {
  const ts: number[] = [];
  for (const k of [0, 1] as const) {
    const d = dir[k];
    if (Math.abs(d) < EPS) continue;
    const reach = Math.abs(d * T);
    for (let m = 1; m < reach + 1; m += 2) {
      const t = m / Math.abs(d);
      if (t < T - 1e-7) ts.push(t);
    }
  }
  ts.sort((a, b) => a - b);
  const cross: number[] = [];
  for (const t of ts) if (!cross.length || t - cross[cross.length - 1] > 1e-7) cross.push(t);
  const walls = cross.map((t) => {
    const [x, y] = at({ dir, T, cross: [], walls: [], tiles: [] }, t);
    const w: Wall[] = [];
    if (isOdd(x)) w.push({ axis: "x", at: Math.round(x) });
    if (isOdd(y)) w.push({ axis: "y", at: Math.round(y) });
    return w;
  });
  const bounds = [0, ...cross, T];
  const tiles = bounds.slice(0, -1).map((t0, i) => {
    const m = (t0 + bounds[i + 1]) / 2;
    return [tileIdx(dir[0] * m), tileIdx(dir[1] * m)] as V;
  });
  return { dir, T, cross, walls, tiles };
};

/** the real (bouncing) path: fold of the line, as the polyline through its bounces */
export const realPath = (s: Shot, t0 = 0, t1 = s.T): V[] => {
  const pts: V[] = [fold(at(s, t0))];
  for (const t of s.cross) if (t > t0 + 1e-9 && t < t1 - 1e-9) pts.push(fold(at(s, t)));
  pts.push(fold(at(s, t1)));
  return pts;
};

/** the part of the line after t0, folded into tile `tile` */
export const foldedInto = (s: Shot, t0: number, tile: V): V[] => {
  const pts: V[] = [intoTile(at(s, t0), tile)];
  for (const t of s.cross) if (t > t0 + 1e-9) pts.push(intoTile(at(s, t), tile));
  pts.push(intoTile(at(s, s.T), tile));
  return pts;
};

/** polyline length and point at arc-length fraction */
export const polyLen = (pts: V[]) => pts.slice(1).reduce((L, p, i) => L + Math.hypot(p[0] - pts[i][0], p[1] - pts[i][1]), 0);
export const polyAt = (pts: V[], frac: number): { p: V; upto: V[] } => {
  const L = polyLen(pts);
  let need = Math.max(0, Math.min(1, frac)) * L;
  const upto: V[] = [pts[0]];
  for (let i = 1; i < pts.length; i++) {
    const a = pts[i - 1];
    const b = pts[i];
    const l = Math.hypot(b[0] - a[0], b[1] - a[1]);
    if (need <= l) {
      const k = l > 0 ? need / l : 0;
      const p: V = [a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k];
      upto.push(p);
      return { p, upto };
    }
    need -= l;
    upto.push(b);
  }
  return { p: pts[pts.length - 1], upto };
};

/** the reflection across a wall, blended: σ = 1 → mirrored, σ = −1 → identity (a page turning over the wall) */
export const flip = (p: V, w: Wall, sigma: number): V =>
  w.axis === "x" ? [w.at + (p[0] - w.at) * -sigma, p[1]] : [p[0], w.at + (p[1] - w.at) * -sigma];
