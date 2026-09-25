/**
 * The dictionary: coordinates on the tiled plane. Copies of the centre sit at
 * (even, even) — blue, "home"; copies of the corner pockets at (odd, odd) —
 * red rings, "pocket". The problem becomes: does the ray from the origin hit
 * blue before red?
 */
import React from "react";
import { interpolate, spring } from "remotion";
import { color, type } from "../../theme";
import { clamp } from "../../components/Type";
import { Flash, HOMEC, HomeDot, Kicker, Layer, Ln, M, Mark, POCKET, Pocket, R_POCKET, Sheet, Txt, W_POCKET, World, dOf, mLbl, px, pxs, tLbl, useS } from "../kit";
import { V, polyAt } from "../geo";

export const PLANE_W: World = { ox: 1190, oy: 610, u: 120 };
const W = PLANE_W;
const XS = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6];
const YS = [-4, -3, -2, -1, 0, 1, 2, 3, 4, 5];
const inView = ([x, y]: V) => {
  const [a, b] = px(W, [x, y]);
  return a > 740 && a < 1860 && b > 150 && b < 990;
};
const even = (v: number) => Math.abs(v) % 2 === 0;
export const HOMES: V[] = XS.flatMap((x) => YS.map((y) => [x, y] as V)).filter(([x, y]) => even(x) && even(y) && inView([x, y]));
export const CORNERS: V[] = XS.flatMap((x) => YS.map((y) => [x, y] as V)).filter(([x, y]) => !even(x) && !even(y) && inView([x, y]));
export const MIXED: V[] = XS.flatMap((x) => YS.map((y) => [x, y] as V)).filter(([x, y]) => even(x) !== even(y) && inView([x, y]));

/** the feathered window the plane is seen through */
export const PlaneMask: React.FC<{ id: string; x?: number; y?: number; w?: number; h?: number }> = ({ id, x = 780, y = 170, w = 1100, h = 800 }) => (
  <defs>
    <filter id={`${id}-f`} x="-10%" y="-10%" width="120%" height="120%">
      <feGaussianBlur stdDeviation="36" />
    </filter>
    <mask id={id} maskUnits="userSpaceOnUse" x="0" y="0" width="1920" height="1080">
      <rect x={x} y={y} width={w} height={h} fill="#fff" filter={`url(#${id}-f)`} />
    </mask>
  </defs>
);
export const Grid: React.FC<{ W: World; o?: number; xs?: number[]; ys?: number[] }> = ({ W, o = 1, xs = [-7, -5, -3, -1, 1, 3, 5, 7], ys = [-5, -3, -1, 1, 3, 5, 7] }) => (
  <g opacity={o}>
    {xs.map((x) => (
      <path key={`x${x}`} d={dOf(W, [[x, -8], [x, 9]])} stroke={color.rule} strokeWidth={1.8} />
    ))}
    {ys.map((y) => (
      <path key={`y${y}`} d={dOf(W, [[-9, y], [11, y]])} stroke={color.rule} strokeWidth={1.8} />
    ))}
  </g>
);
/** a coordinate label: under a centre copy, or tucked into the upper-right quadrant of a grid corner */
export const coordLbl = (W: World, [x, y]: V, kind: "home" | "corner", size = 32) => {
  const [a, b] = px(W, [x, y]);
  const t = `(${x < 0 ? "-" : ""}${Math.abs(x)},\\,${y < 0 ? "-" : ""}${Math.abs(y)})`;
  return kind === "home" ? { x: a, y: b + 50, t, size, align: "center" as const } : { x: a + 22, y: b - 24, t, size };
};

export const Dictionary: React.FC = () => {
  const { f, fps, at, p, guard } = useS();
  const grid = p("start", 40);
  const real = p("start", 30, 10);
  const brace = p("start", 26, 60);
  const cen = at("centers");
  const cor = at("corners");
  const q = p("question", 26);
  const pop = (t0: number, v: V) => spring({ frame: f - t0 - Math.hypot(v[0], v[1]) * 3, fps, config: { damping: 14, stiffness: 170, mass: 0.6 } });

  const hl: V[] = [
    [0, 0],
    [2, 0],
    [2, 2],
    [-2, 2],
  ];
  const cl: V[] = [
    [1, 1],
    [3, 1],
    [-3, -1],
  ];
  const lblO = 1 - 0.6 * q;
  const HL = hl.map((v) => ({ ...coordLbl(W, v, "home"), c: HOMEC, p: p("centers", 24, 30), o: lblO }));
  const CL = cl.map((v) => ({ ...coordLbl(W, v, "corner"), c: POCKET, p: p("corners", 24, 30), o: lblO }));

  // the two test rays
  const r1 = interpolate(f, [at("question") + 50, at("question") + 100], [0, 1], clamp);
  const r2 = interpolate(f, [at("question") + 110, at("question") + 140], [0, 1], clamp);
  const ray1: V[] = [
    [0, 0],
    [4, 2],
  ];
  const ray2: V[] = [
    [0, 0],
    [1, 1],
  ];

  // bracket over the real table: "2 units"
  const by = 1.28;
  const two = { x: W.ox, y: px(W, [0, by])[1] - 14, t: "2", size: 36, align: "center" as const, c: color.ink2, p: brace };
  const realLbl = { s: "the real table", x: W.ox, y: px(W, [0, -1])[1] + 20 };

  const marks: Mark[] = [
    ...[-7, -5, -3, -1, 1, 3, 5, 7].map((x): Mark => ({ name: `wall x=${x}`, pts: pxs(W, [[x, -8], [x, 9]]), w: 1.8, on: grid > 0 })),
    ...[-5, -3, -1, 1, 3, 5, 7].map((y): Mark => ({ name: `wall y=${y}`, pts: pxs(W, [[-9, y], [11, y]]), w: 1.8, on: grid > 0 })),
    ...HOMES.map((v): Mark => ({ name: `home ${v}`, pts: [px(W, v)], w: 18, on: f > cen })),
    ...CORNERS.map((v): Mark => ({ name: `pocket ${v}`, pts: [px(W, v)], w: 2 * R_POCKET + W_POCKET, on: f > cor })),
    { name: "bracket", pts: pxs(W, [[-1, by], [1, by]]), w: 2, on: brace > 0 },
    { name: "ray 1", pts: pxs(W, ray1), w: 4, on: r1 >= 1 },
    { name: "ray 2", pts: pxs(W, ray2), w: 4, on: r2 >= 1 },
  ];
  guard(marks, [...HL.map((l) => mLbl(l)), ...CL.map((l) => mLbl(l)), mLbl(two, "2 units"), tLbl(realLbl.s, realLbl.x, realLbl.y, type.label, real, 1, { italic: true, align: "center" })]);

  return (
    <Sheet folio={11} title="A dictionary">
      <Layer>
        <PlaneMask id="q7-dict" />
        <g mask="url(#q7-dict)">
          <Grid W={W} o={grid} />
          {HOMES.map((v, i) => {
            const k = pop(cen, v);
            return k > 0.01 ? <HomeDot key={i} W={W} p={v} r={9 * k} /> : null;
          })}
          {CORNERS.map((v, i) => {
            const k = pop(cor, v);
            return k > 0.01 ? <Pocket key={i} W={W} p={v} sx={k} sy={k} /> : null;
          })}
          <path d={dOf(W, [[-1, -1], [1, -1], [1, 1], [-1, 1], [-1, -1]])} fill="none" stroke={color.ink} strokeWidth={4.2} opacity={real} />
          {brace > 0 && (
            <g opacity={brace}>
              <Ln x1={px(W, [-1, by])[0]} y1={px(W, [0, by])[1]} x2={px(W, [1, by])[0]} y2={px(W, [0, by])[1]} p={brace} c={color.ink2} w={2} />
              <line x1={px(W, [-1, by])[0]} y1={px(W, [0, by])[1] - 9} x2={px(W, [-1, by])[0]} y2={px(W, [0, by])[1] + 9} stroke={color.ink2} strokeWidth={2} />
              <line x1={px(W, [1, by])[0]} y1={px(W, [0, by])[1] - 9} x2={px(W, [1, by])[0]} y2={px(W, [0, by])[1] + 9} stroke={color.ink2} strokeWidth={2} opacity={brace >= 1 ? 1 : 0} />
            </g>
          )}
          {r1 > 0 && <path d={dOf(W, [ray1[0], polyAt(ray1, r1).p])} stroke={color.ink} strokeWidth={4} strokeLinecap="round" />}
          {r2 > 0 && <path d={dOf(W, [ray2[0], polyAt(ray2, r2).p])} stroke={color.ink} strokeWidth={4} strokeLinecap="round" />}
          <Flash W={W} p={[4, 2]} t={(f - at("question") - 100) / 26} c={HOMEC} r1={56} />
          <Flash W={W} p={[1, 1]} t={(f - at("question") - 140) / 26} c={POCKET} r1={56} />
        </g>
      </Layer>
      {HL.map((l) => (
        <M key={l.t} {...l} />
      ))}
      {CL.map((l) => (
        <M key={l.t} {...l} />
      ))}
      <M {...two} />
      <Txt x={realLbl.x} y={realLbl.y} w={300} align="center" size={type.label} italic c={color.ink2} p={real}>
        {realLbl.s}
      </Txt>

      {/* key */}
      <Kicker x={120} y={150} p={p("start", 22)}>
        Coordinates
      </Kicker>
      <Txt x={120} y={222} w={600} size={type.body} p={p("start", 26, 20)}>
        The real table is
      </Txt>
      <M x={120} y={340} t="[-1,1]\times[-1,1]" size={60} p={p("start", 26, 40)} />
      <Txt x={120} y={372} w={600} size={type.caption} italic c={color.ink2} p={brace}>
        so every copy is 2 units wide.
      </Txt>

      <Layer>
        <circle cx={140} cy={497} r={11} fill={HOMEC} opacity={p("centers", 20)} />
        <circle cx={140} cy={647} r={R_POCKET} fill={color.paper} stroke={POCKET} strokeWidth={W_POCKET} opacity={p("corners", 20)} />
      </Layer>
      <Txt x={176} y={468} w={560} size={type.body} p={p("centers", 26)}>
        (even, even)
      </Txt>
      <Txt x={176} y={524} w={560} size={type.caption} italic c={HOMEC} p={p("centers", 26, 20)}>
        a copy of the center: the ball is home
      </Txt>
      <Txt x={176} y={618} w={560} size={type.body} p={p("corners", 26)}>
        (odd, odd)
      </Txt>
      <Txt x={176} y={674} w={560} size={type.caption} italic c={POCKET} p={p("corners", 26, 20)}>
        a copy of a corner: the ball falls in
      </Txt>

      <div style={{ position: "absolute", left: 120, top: 780, width: 560, height: 2, background: color.rule, opacity: q }} />
      <Txt x={120} y={806} w={600} size={type.body} p={q}>
        Does the ray from the origin hit a <span style={{ color: HOMEC }}>blue</span> point before a <span style={{ color: POCKET }}>red</span> one?
      </Txt>
    </Sheet>
  );
};
