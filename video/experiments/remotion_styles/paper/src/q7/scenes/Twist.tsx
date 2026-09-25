/**
 * Part (b): the edge-midpoint pockets. Their copies are the mixed-parity
 * points, so every lattice point but (even, even) is a pocket; the midpoint
 * (p, q) of any trip home is never (even, even) — every trip is cut halfway.
 * (1,0) now drops into the right-edge pocket; (2,1) into the top one. Answer 0.
 */
import React from "react";
import { interpolate, spring } from "remotion";
import { color, type } from "../../theme";
import { clamp } from "../../components/Type";
import { Ball, EDGE, Flash, HOMEC, HomeDot, Kicker, Layer, M, Mark, POCKET, Pocket, R_POCKET, Sheet, Table, Txt, W_POCKET, World, dOf, mLbl, px, pxs, tableMarks, useS } from "../kit";
import { V, polyAt, polyLen, realPath, shot } from "../geo";
import { Grid, PlaneMask } from "./Dictionary";

const T: World = { ox: 540, oy: 770, u: 170 };
const P: World = { ox: 1330, oy: 740, u: 110 };
const pts = (pred: (x: number, y: number) => boolean): V[] => {
  const out: V[] = [];
  for (let x = -3; x <= 7; x++) for (let y = -3; y <= 6; y++) if (pred(x, y)) out.push([x, y]);
  return out;
};
const ev = (v: number) => Math.abs(v) % 2 === 0;
const HOMES = pts((x, y) => ev(x) && ev(y));
const CORN = pts((x, y) => !ev(x) && !ev(y));
const MIX = pts((x, y) => ev(x) !== ev(y));
const PATH10 = realPath(shot([1, 0], 1)); // → the right-edge pocket (1, 0)
const PATH21 = realPath(shot([2, 1], 1)); // → (1, ½) → the top pocket (0, 1)

export const Twist: React.FC = () => {
  const { f, fps, at, p, guard } = useS();
  const t0 = at("start");
  const tc = at("copies");
  const tr = at("revisit");
  const tbl = p("start", 30);
  const mids = spring({ frame: f - t0 - 30, fps, config: { damping: 13, stiffness: 180, mass: 0.6 } });
  const plane = p("start", 36, 20);
  const pop = (v: V) => spring({ frame: f - tc - 16 - Math.hypot(v[0], v[1]) * 3, fps, config: { damping: 14, stiffness: 170, mass: 0.6 } });

  // (1,0) on the real table
  const s1 = interpolate(f, [tr + 10, tr + 10 + polyLen(PATH10) / 0.04], [0, 1], clamp);
  const e1 = f - (tr + 10 + polyLen(PATH10) / 0.04);
  // (2,1) on the real table + on the plane
  const r2 = tr + 120;
  const s2 = interpolate(f, [r2, r2 + polyLen(PATH21) / 0.04], [0, 1], clamp);
  const e2 = f - (r2 + polyLen(PATH21) / 0.04);
  const seg = interpolate(f, [r2, r2 + polyLen(PATH21) / 0.04], [0, 1], clamp);

  const drop = (e: number) => (e <= 0 ? 1 : interpolate(e, [0, 10], [1, 0], clamp));

  const L = {
    p10: { x: px(T, [1, 0])[0] + 26, y: px(T, [1, 0])[1] + 12, t: "(1,\\,0)", size: 36, c: EDGE, p: interpolate(e1, [4, 20], [0, 1], clamp) },
    p01: { x: px(T, [0, 1])[0] - 24, y: px(T, [0, 1])[1] - 18, t: "(0,\\,1)", size: 36, c: EDGE, align: "right" as const, p: interpolate(e2, [4, 20], [0, 1], clamp) },
    m21: { x: px(P, [2, 1])[0] + 24, y: px(P, [2, 1])[1] + 44, t: "(2,\\,1)", size: 34, c: EDGE, p: interpolate(e2, [4, 20], [0, 1], clamp) },
  };
  const marks: Mark[] = [
    ...tableMarks(T, "real table", [0, 0], "all"),
    { name: "shot (1,0)", pts: pxs(T, PATH10), w: 3.6, on: s1 > 0 },
    { name: "shot (2,1)", pts: pxs(T, PATH21), w: 3.6, on: s2 > 0 },
    ...[-3, -1, 1, 3, 5, 7].map((x): Mark => ({ name: `wall x=${x}`, pts: pxs(P, [[x, -8], [x, 9]]), w: 1.8 })),
    ...[-3, -1, 1, 3, 5].map((y): Mark => ({ name: `wall y=${y}`, pts: pxs(P, [[-9, y], [11, y]]), w: 1.8 })),
    ...HOMES.map((v): Mark => ({ name: `home ${v}`, pts: [px(P, v)], w: 18 })),
    ...[...CORN, ...MIX].map((v): Mark => ({ name: `pocket ${v}`, pts: [px(P, v)], w: 2 * R_POCKET + W_POCKET })),
    { name: "plane segment", pts: pxs(P, [[0, 0], [2, 1]]), w: 4, on: seg > 0 },
    { name: "plane dashes", pts: pxs(P, [[2, 1], [4, 2]]), w: 3, on: seg >= 1 },
  ];
  guard(marks, Object.entries(L).map(([k, l]) => mLbl(l, k)));

  const ans = p("answer", 30);
  return (
    <Sheet folio={15} title="Part (b)">
      <Layer>
        {/* the real table, now with eight pockets */}
        <Table W={T} real draw={tbl} pockets="corners" />
        {tbl >= 1 &&
          ([
            [1, 0],
            [0, 1],
            [-1, 0],
            [0, -1],
          ] as V[]).map((v, i) => (mids > 0.01 ? <Pocket key={i} W={T} p={v} c={EDGE} sx={mids} sy={mids} /> : null))}
        {s1 > 0 && (
          <g>
            <path d={dOf(T, polyAt(PATH10, s1).upto)} stroke={color.ink} strokeWidth={3.6} strokeLinecap="round" fill="none" />
            {drop(e1) > 0 && <Ball W={T} p={polyAt(PATH10, s1).p} r={11 * (0.3 + 0.7 * drop(e1))} o={drop(e1)} />}
            <Flash W={T} p={[1, 0]} t={e1 / 26} c={EDGE} r1={52} />
            {e1 > 8 && <circle cx={px(T, [1, 0])[0]} cy={px(T, [1, 0])[1]} r={6} fill={EDGE} />}
          </g>
        )}
        {s2 > 0 && (
          <g>
            <path d={dOf(T, polyAt(PATH21, s2).upto)} stroke={color.ink} strokeWidth={3.6} strokeLinecap="round" strokeLinejoin="round" fill="none" />
            {drop(e2) > 0 && <Ball W={T} p={polyAt(PATH21, s2).p} r={11 * (0.3 + 0.7 * drop(e2))} o={drop(e2)} />}
            <Flash W={T} p={[0, 1]} t={e2 / 26} c={EDGE} r1={52} />
            {e2 > 8 && <circle cx={px(T, [0, 1])[0]} cy={px(T, [0, 1])[1]} r={6} fill={EDGE} />}
          </g>
        )}

        {/* the plane */}
        <PlaneMask id="q7-twist" x={1100} y={210} w={770} h={730} />
        <g mask="url(#q7-twist)" opacity={plane}>
          <Grid W={P} xs={[-3, -1, 1, 3, 5, 7]} ys={[-3, -1, 1, 3, 5]} />
          <path d={dOf(P, [[-1, -1], [1, -1], [1, 1], [-1, 1], [-1, -1]])} fill="none" stroke={color.ink} strokeWidth={3.6} />
          {HOMES.map((v, i) => (
            <HomeDot key={i} W={P} p={v} r={9} />
          ))}
          {CORN.map((v, i) => (
            <Pocket key={i} W={P} p={v} />
          ))}
          {MIX.map((v, i) => {
            const k = pop(v);
            return k > 0.01 ? <Pocket key={i} W={P} p={v} c={EDGE} sx={k} sy={k} /> : null;
          })}
          {seg > 0 && <path d={dOf(P, [[0, 0], polyAt([[0, 0], [2, 1]], seg).p])} stroke={color.ink} strokeWidth={4} strokeLinecap="round" />}
          {seg >= 1 && <path d={dOf(P, [[2, 1], [4, 2]])} stroke={color.ink3} strokeWidth={3} strokeDasharray="4 9" strokeLinecap="round" />}
          <Flash W={P} p={[2, 1]} t={e2 / 26} c={EDGE} r1={52} />
          {e2 > 0 && <circle cx={px(P, [2, 1])[0]} cy={px(P, [2, 1])[1]} r={6} fill={EDGE} />}
        </g>
      </Layer>
      {Object.entries(L).map(([k, l]) => (
        <M key={k} {...l} />
      ))}

      <Kicker x={120} y={150} p={p("start", 22)}>
        Part (b)
      </Kicker>
      <Txt x={120} y={216} w={860} size={type.body} p={p("start", 26, 10)}>
        Add a pocket at the middle of every edge.
      </Txt>
      <Txt x={120} y={282} w={860} size={type.caption} p={p("copies", 24)}>
        Their copies: <span style={{ color: EDGE }}>(odd, even)</span> and <span style={{ color: EDGE }}>(even, odd)</span>.
      </Txt>
      <Txt x={120} y={334} w={860} size={type.caption} p={p("copies", 24, 40)}>
        Now every lattice point is a pocket, except <span style={{ color: HOMEC }}>(even, even)</span>.
      </Txt>
      <M x={120} y={440} t={`\\gcd(p,q)=1\\ \\Rightarrow\\ {\\color{${EDGE}}(p,q)}\\neq(\\text{even},\\text{even})`} size={46} p={p("test", 26)} />
      <Txt x={120} y={470} w={860} size={type.caption} italic c={POCKET} p={p("test", 24, 50)}>
        The midpoint is always a pocket: every trip home is cut halfway.
      </Txt>

      <div style={{ position: "absolute", left: 0, top: 0, opacity: ans }}>
        <Txt x={850} y={640} w={260} size={type.caption} italic c={color.ink2} p={ans}>
          angles in (b):
        </Txt>
        <Txt x={850} y={680} w={260} size={200} lh={1} c={POCKET} p={ans} style={{ fontFeatureSettings: "'lnum' 1" }}>
          0
        </Txt>
      </div>
    </Sheet>
  );
};
