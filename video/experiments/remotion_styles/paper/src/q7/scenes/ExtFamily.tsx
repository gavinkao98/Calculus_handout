/**
 * zh extension 3 (EXTENSION.zh.md §四): the same move — unfold, straighten,
 * find the first point of the same class — on two other problems. A 5×3
 * table with corner pockets, shot at 45° from a corner: six bounces, into the
 * top-right pocket; unfolded, the line y = x first meets a corner image at
 * (15, 15). Then 2002 AIME I #11 (restated): a cube of side 12, light from A
 * through P = (12, 7, 5); unfolded into the cube lattice, the first point with
 * all three coordinates multiples of 12 is (144, 84, 60), length 12√218.
 */
import React from "react";
import { interpolate } from "remotion";
import { color, font, type } from "../../theme";
import { clamp } from "../../components/Type";
import { Ball, EDGE, Flash, HOMEC, HomeDot, Kicker, Layer, M, Mark, POCKET, Pocket, Pt, Sheet, Txt, World, dOf, mLbl, px, pxs, texW, toD, useS, useT, Caps } from "../kit";
import { V, polyAt } from "../geo";
import { rectShot } from "../extGeo";

const smooth = (x: number) => 0.5 - 0.5 * Math.cos(Math.PI * Math.max(0, Math.min(1, x)));
const lerpW = (a: World, b: World, t: number): World => ({ ox: a.ox + (b.ox - a.ox) * t, oy: a.oy + (b.oy - a.oy) * t, u: a.u * Math.pow(b.u / a.u, t) });

// ── the 5×3 table ──
const A = 5;
const B = 3;
const RP = rectShot(A, B, [1, 1], 15); // (0,0) (3,3) (5,1) (4,0) (1,3) (0,2) (2,0) (5,3)
const R0: World = { ox: 900, oy: 790, u: 150 };
const R1: World = { ox: 900, oy: 940, u: 52 };
const CROSSED: V[][] = [
  [
    [5, 3],
    [5, 6],
  ],
  [
    [10, 9],
    [10, 12],
  ],
  [
    [0, 3],
    [5, 3],
  ],
  [
    [5, 6],
    [10, 6],
  ],
  [
    [5, 9],
    [10, 9],
  ],
  [
    [10, 12],
    [15, 12],
  ],
];
const CORNER_IMGS: V[] = [];
for (let a = 0; a <= 3; a++) for (let b = 0; b <= 5; b++) CORNER_IMGS.push([5 * a, 3 * b]);

// ── the cube (oblique projection; y is depth) ──
type P3 = [number, number, number];
/** cabinet-style oblique: depth at 45°, foreshortened to 0.5 */
const proj = (o: { ox: number; oy: number; k: number }, [x, y, z]: P3): Pt => [o.ox + o.k * (x + 0.354 * y), o.oy - o.k * (z + 0.354 * y)];
const CUBE = { ox: 1060, oy: 870, k: 30 };
const V3: Record<string, P3> = {
  A: [0, 0, 0],
  B: [12, 0, 0],
  C: [12, 12, 0],
  F: [12, 12, 12],
  G: [12, 0, 12],
  D: [0, 12, 0],
  E: [0, 0, 12],
  H: [0, 12, 12],
};
const EDGES: Array<[string, string, boolean]> = [
  ["A", "B", false],
  ["B", "C", false],
  ["C", "D", true],
  ["D", "A", true],
  ["E", "G", false],
  ["G", "F", false],
  ["F", "H", false],
  ["H", "E", false],
  ["A", "E", false],
  ["B", "G", false],
  ["C", "F", false],
  ["D", "H", true],
];
const P: P3 = [12, 7, 5];
const Q1: P3 = [12 - 60 / 7, 12, 5 + 25 / 7]; // after the reflection at P, the next wall is y = 12
const LAT = { ox: 900, oy: 890, k: 14 };

export const ExtFamily: React.FC = () => {
  const { f, at, p, pf, guard } = useS();
  const { ext, r, tLbl } = useT();
  const T = ext.family;
  const tRect = at("rect");
  const tUnf = at("unfold");
  const tCube = at("cube");
  const tSame = at("same");
  const win = (a: number, b: number, len = 16) => pf(a, len) * (1 - pf(b, len));

  // mnemonic: which steps are lit
  const lit = [
    Math.max(win(at("start", 0.1), tRect + 10), win(tUnf, tCube), pf(tSame + 4, 16)),
    Math.max(win(at("start", 0.3), tRect + 10), win(tUnf + 60, tCube), pf(tSame + 40, 16)),
    Math.max(win(at("start", 0.5), tRect + 10), win(at("unfold", 0.45), tCube), pf(at("same", 0.3), 16)),
  ];

  // ── start: this problem, in miniature ──
  const miniO = win(at("start", 0.15), tRect);
  const MINI: World = { ox: 1110, oy: 700, u: 90 };
  const miniLine = interpolate(f, [at("start", 0.3), at("start", 0.3) + 40], [0, 1], clamp);

  // ── rect → unfold ──
  const zoom = smooth(interpolate(f, [tUnf + 4, tUnf + 44], [0, 1], clamp));
  const RW = lerpW(R0, R1, zoom);
  const rectO = win(tRect + 4, tCube);
  const run = interpolate(f, [at("rect", 0.3), at("rect", 0.3) + 150], [0, 1], clamp);
  const runEnd = at("rect", 0.3) + 150;
  const pathO = 1 - pf(tUnf + 40, 20);
  const tilesIn = (a: number, b: number) => pf(tUnf + 30 + (a + b) * 7, 16);
  const lineP = interpolate(f, [tUnf + 90, tUnf + 160], [0, 1], clamp);
  const lineEnd = tUnf + 160;
  const wallsO = pf(lineEnd - 20, 20);

  // ── cube → same ──
  const cubeO = win(tCube + 6, tSame);
  const cubeIn = pf(tCube + 6, 30);
  const faceIn = pf(tCube + 40, 20);
  const pIn = pf(at("cube", 0.45), 20);
  const rayP = interpolate(f, [at("cube", 0.5), at("cube", 0.5) + 36], [0, 1], clamp);
  const ray2 = interpolate(f, [at("cube", 0.5) + 40, at("cube", 0.5) + 70], [0, 1], clamp);
  const sameO = pf(tSame + 10, 20);
  const latIn = pf(tSame + 10, 30);
  const latLine = interpolate(f, [tSame + 40, tSame + 110], [0, 1], clamp);

  const Cp = (k: string) => proj(CUBE, V3[k]);
  const vLbl = (k: string, dx: number, dy: number) => ({ x: Cp(k)[0] + dx, y: Cp(k)[1] + dy, t: k, size: 38, align: "center" as const, p: cubeIn, o: cubeO });
  const VL = [vLbl("A", -26, 36), vLbl("B", -14, 46), vLbl("C", 30, 30), vLbl("F", 26, -12), vLbl("G", -26, -14)];
  const Pp = proj(CUBE, P);
  const pLbl = { x: Pp[0] + 16, y: Pp[1] - 16, t: "P", size: 38, align: "left" as const, p: pIn, o: cubeO };
  // P's distance to edge BG is its y = 7: shown as a dimension line along BC, from B to the foot (12, 7, 0)
  const DIM = 16; // px, outward (down-right, off the cube)
  const dimA: Pt = [Cp("B")[0] + DIM * 0.707, Cp("B")[1] + DIM * 0.707];
  const five = proj(CUBE, [12, 7, 0]);
  const dimB: Pt = [five[0] + DIM * 0.707, five[1] + DIM * 0.707];
  const l7 = { x: (dimA[0] + dimB[0]) / 2 + 22, y: (dimA[1] + dimB[1]) / 2 + 34, t: "7", size: 32, align: "center" as const, c: color.ink2, p: pIn, o: cubeO };
  const l5 = { x: (Pp[0] + five[0]) / 2 + 16, y: (Pp[1] + five[1]) / 2 + 2, t: "5", size: 32, align: "left" as const, c: color.ink2, p: pIn, o: cubeO };
  const lcmLbl = { x: px(R1, [15, 15])[0] + 20, y: px(R1, [15, 15])[1] + 12, t: "(15,\\,15)", size: 34, c: POCKET, p: pf(lineEnd, 16), o: rectO * (zoom >= 1 ? 1 : 0) };
  const startLbl = { s: T.start, x: px(R0, [0, 0])[0] - 20, y: px(R0, [0, 0])[1] + 18 };
  const dirLbl = { s: T.dir, x: Cp("A")[0] - 24, y: Cp("A")[1] - 190 };

  const cubeMarks: Mark[] = EDGES.map(([a, b]) => ({ name: `edge ${a}${b}`, pts: [Cp(a), Cp(b)], w: 3, on: cubeIn >= 1 && cubeO > 0.05 }));
  const marks: Mark[] = [
    ...cubeMarks,
    { name: "ray AP", pts: [Cp("A"), Pp], w: 3.4, on: rayP >= 1 && cubeO > 0.05 },
    { name: "dimension 7", pts: [dimA, dimB], w: 1.6, on: pIn > 0 && cubeO > 0.05 },
    { name: "P to BC", pts: [Pp, five], w: 1.6, on: pIn > 0 && cubeO > 0.05 },
    { name: "line y=x", pts: pxs(R1, [[0, 0], [15, 15]]), w: 3.6, on: zoom >= 1 && lineP > 0 && rectO > 0.05 },
    { name: "grid right", pts: pxs(R1, [[15, 0], [15, 15]]), w: 2, on: zoom >= 1 && rectO > 0.05 },
    { name: "grid top", pts: pxs(R1, [[0, 15], [15, 15]]), w: 2, on: zoom >= 1 && rectO > 0.05 },
    { name: "table", pts: pxs(R0, [[0, 0], [5, 0], [5, 3], [0, 3], [0, 0]]), w: 4.2, on: zoom <= 0 && rectO > 0.05 },
    { name: "start pocket", pts: [px(R0, [0, 0])], w: 28, on: zoom <= 0 && rectO > 0.05 },
  ];
  guard(marks, [...VL.map((l) => mLbl(l)), mLbl(pLbl), mLbl(l7, "7"), mLbl(l5, "5"), mLbl(lcmLbl, "(15,15)"), tLbl(startLbl.s, startLbl.x, startLbl.y, 34, pf(tRect + 20, 20), rectO * (zoom <= 0 ? 1 : 0), { align: "right" }), tLbl(dirLbl.s.replace(/\$/g, ""), dirLbl.x, dirLbl.y, 34, rayP, cubeO, { align: "right" })]);

  // lattice of 3×2×2 cubes (not to scale), for `same`
  const latLines: Array<[P3, P3]> = [];
  for (const y of [0, 12, 24]) for (const z of [0, 12, 24]) latLines.push([[0, y, z], [36, y, z]]);
  for (const x of [0, 12, 24, 36]) for (const z of [0, 12, 24]) latLines.push([[x, 0, z], [x, 24, z]]);
  for (const x of [0, 12, 24, 36]) for (const y of [0, 12, 24]) latLines.push([[x, y, 0], [x, y, 24]]);
  const LA = proj(LAT, [0, 0, 0]);
  const LB = proj(LAT, [36, 21, 15]); // where the line leaves the drawn block (x = 36)
  const LC = proj(LAT, [42, 24.5, 17.5]);

  return (
    <Sheet folio={19} title={T.title}>
      <Layer>
        {/* start: this problem's line, (0,0) → (4,2) */}
        {miniO > 0 && (
          <g opacity={miniO}>
            {[-1, 1, 3, 5].map((x) => (
              <path key={`x${x}`} d={dOf(MINI, [[x, -1], [x, 3]])} stroke={color.ink3} strokeWidth={1.6} />
            ))}
            {[-1, 1, 3].map((y) => (
              <path key={`y${y}`} d={dOf(MINI, [[-1, y], [5, y]])} stroke={color.ink3} strokeWidth={1.6} />
            ))}
            <path d={dOf(MINI, [[-1, -1], [1, -1], [1, 1], [-1, 1], [-1, -1]])} fill="none" stroke={color.ink} strokeWidth={3.4} />
            {[0, 2, 4].flatMap((x) => [0, 2].map((y) => <HomeDot key={`${x}${y}`} W={MINI} p={[x, y]} r={7} />))}
            {[-1, 1, 3, 5].flatMap((x) => [-1, 1, 3].map((y) => <Pocket key={`${x}${y}`} W={MINI} p={[x, y]} r={9} />))}
            <path d={dOf(MINI, [[0, 0], [4 * miniLine, 2 * miniLine]])} stroke={color.ink} strokeWidth={3.6} strokeLinecap="round" />
            <Flash W={MINI} p={[4, 2]} t={(f - at("start", 0.3) - 40) / 24} c={HOMEC} r1={44} />
          </g>
        )}

        {/* the 5×3 table, then its unfolding */}
        {rectO > 0 && (
          <g opacity={rectO}>
            {zoom > 0 &&
              [0, 1, 2].flatMap((a) =>
                [0, 1, 2, 3, 4].map((b) =>
                  a + b === 0 ? null : (
                    <path key={`${a}${b}`} d={dOf(RW, [[5 * a, 3 * b], [5 * a + 5, 3 * b], [5 * a + 5, 3 * b + 3], [5 * a, 3 * b + 3], [5 * a, 3 * b]])} fill="none" stroke={color.ink2} strokeWidth={2} opacity={tilesIn(a, b)} />
                  ),
                ),
              )}
            <path d={dOf(RW, [[0, 0], [5, 0], [5, 3], [0, 3], [0, 0]])} fill="none" stroke={color.ink} strokeWidth={4.2} strokeDasharray={pf(tRect, 30) < 1 ? `${pf(tRect, 30) * 16 * RW.u} ${16 * RW.u}` : undefined} />
            {wallsO > 0 && CROSSED.map((s, i) => <path key={i} d={dOf(RW, s)} stroke={EDGE} strokeWidth={6} strokeLinecap="round" opacity={0.85 * wallsO} />)}
            {pf(tRect, 30) >= 1 &&
              CORNER_IMGS.map((v, i) => {
                const real = v[0] <= 5 && v[1] <= 3;
                const o = real ? 1 : tilesIn(Math.max(0, v[0] / 5 - 1), Math.max(0, v[1] / 3 - 1));
                return o > 0 ? <Pocket key={i} W={RW} p={v} r={real ? 12 * (1 - 0.35 * zoom) : 7} o={o} /> : null;
              })}
            {run > 0 && pathO > 0 && (
              <g opacity={pathO}>
                <path d={dOf(RW, polyAt(RP, run).upto)} fill="none" stroke={color.ink} strokeWidth={3.4} strokeLinejoin="round" strokeLinecap="round" />
                {f < runEnd + 8 && <Ball W={RW} p={polyAt(RP, run).p} r={10} />}
              </g>
            )}
            <Flash W={RW} p={[5, 3]} t={(f - runEnd) / 24} c={POCKET} r1={46} />
            {lineP > 0 && <path d={dOf(R1, [[0, 0], [15 * lineP, 15 * lineP]])} stroke={color.ink} strokeWidth={3.6} strokeLinecap="round" />}
            <Flash W={R1} p={[15, 15]} t={(f - lineEnd) / 24} c={POCKET} r1={44} />
          </g>
        )}

        {/* cube */}
        {cubeO > 0 && (
          <g opacity={cubeO}>
            <path d={toD([Cp("B"), Cp("C"), Cp("F"), Cp("G")]) + "Z"} fill={color.paperShade} opacity={0.8 * faceIn} />
            {EDGES.map(([a, b, hidden]) => (
              <line key={a + b} x1={Cp(a)[0]} y1={Cp(a)[1]} x2={Cp(a)[0] + (Cp(b)[0] - Cp(a)[0]) * cubeIn} y2={Cp(a)[1] + (Cp(b)[1] - Cp(a)[1]) * cubeIn} stroke={hidden ? color.ink3 : color.ink} strokeWidth={hidden ? 2 : 3} strokeDasharray={hidden ? "7 7" : undefined} />
            ))}
            {pIn > 0 && (
              <g opacity={pIn}>
                <line x1={dimA[0]} y1={dimA[1]} x2={dimB[0]} y2={dimB[1]} stroke={color.ink2} strokeWidth={1.6} />
                {[dimA, dimB].map(([x, y], i) => (
                  <line key={i} x1={x - 6} y1={y + 6} x2={x + 6} y2={y - 6} stroke={color.ink2} strokeWidth={1.6} transform={`rotate(90 ${x} ${y})`} />
                ))}
                <line x1={Pp[0]} y1={Pp[1]} x2={five[0]} y2={five[1]} stroke={color.ink2} strokeWidth={1.6} strokeDasharray="4 5" />
              </g>
            )}
            {rayP > 0 && <line x1={Cp("A")[0]} y1={Cp("A")[1]} x2={Cp("A")[0] + (Pp[0] - Cp("A")[0]) * rayP} y2={Cp("A")[1] + (Pp[1] - Cp("A")[1]) * rayP} stroke={color.ink} strokeWidth={3.4} strokeLinecap="round" />}
            {ray2 > 0 && (
              <line
                x1={Pp[0]}
                y1={Pp[1]}
                x2={Pp[0] + (proj(CUBE, Q1)[0] - Pp[0]) * ray2}
                y2={Pp[1] + (proj(CUBE, Q1)[1] - Pp[1]) * ray2}
                stroke={color.ink}
                strokeWidth={2.6}
                strokeDasharray="8 7"
                opacity={0.6}
              />
            )}
            {pIn > 0 && <circle cx={Pp[0]} cy={Pp[1]} r={7} fill={color.ink} stroke={color.paper} strokeWidth={2.5} opacity={pIn} />}
            <circle cx={Cp("A")[0]} cy={Cp("A")[1]} r={8} fill={color.ink} stroke={color.paper} strokeWidth={2.5} opacity={cubeIn} />
          </g>
        )}

        {/* same: the cube lattice (a few cells, not to scale) and the straight line */}
        {sameO > 0 && (
          <g opacity={sameO}>
            {latLines.map(([a, b], i) => {
              const pa = proj(LAT, a);
              const pb = proj(LAT, b);
              return <line key={i} x1={pa[0]} y1={pa[1]} x2={pa[0] + (pb[0] - pa[0]) * latIn} y2={pa[1] + (pb[1] - pa[1]) * latIn} stroke={color.ink3} strokeWidth={1.5} />;
            })}
            {latLine > 0 && <line x1={LA[0]} y1={LA[1]} x2={LA[0] + (LB[0] - LA[0]) * latLine} y2={LA[1] + (LB[1] - LA[1]) * latLine} stroke={color.ink} strokeWidth={3.6} strokeLinecap="round" />}
            {latLine >= 1 && <line x1={LB[0]} y1={LB[1]} x2={LC[0]} y2={LC[1]} stroke={color.ink} strokeWidth={3} strokeDasharray="3 9" strokeLinecap="round" opacity={pf(tSame + 110, 16)} />}
            <circle cx={LA[0]} cy={LA[1]} r={8} fill={color.ink} stroke={color.paper} strokeWidth={2.5} />
          </g>
        )}
      </Layer>

      {/* cube labels */}
      {VL.map((l) => (
        <M key={l.t} {...l} />
      ))}
      <M {...pLbl} />
      <M {...l7} />
      <M {...l5} />
      <M {...lcmLbl} />
      <div style={{ opacity: miniO }}>
        <div style={{ position: "absolute", left: MINI.ox + 2 * MINI.u - 200, top: px(MINI, [0, 3])[1] - 70, width: 400, textAlign: "center" }}>
          <Caps color={color.ink2}>{T.thisOne}</Caps>
        </div>
      </div>
      <div style={{ opacity: cubeO }}>
        <Txt x={dirLbl.x} y={dirLbl.y} w={320} align="right" size={34} c={color.ink2} p={rayP}>
          {r(dirLbl.s)}
        </Txt>
      </div>
      <div style={{ opacity: rectO * (1 - zoom) }}>
        <Txt x={startLbl.x} y={startLbl.y} w={120} align="right" size={34} c={color.ink2} p={pf(tRect + 20, 20)}>
          {startLbl.s}
        </Txt>
      </div>
      {sameO > 0 && (
        <div style={{ opacity: sameO }}>
          <M x={LC[0] - 50} y={LC[1] - 26} t="(144,\,84,\,60)" size={40} c={POCKET} p={pf(at("same", 0.4) + 16, 20)} />
          <Txt x={LA[0]} y={LA[1] + 24} w={600} size={34} c={color.ink3} p={latIn}>
            {T.lattice}
          </Txt>
        </div>
      )}

      <Kicker x={120} y={150} p={p("start", 22)}>
        {T.kicker}
      </Kicker>
      {/* the three-step mnemonic */}
      {T.steps.map((s, i) => {
        const on = lit[i];
        return (
          <div key={i} style={{ position: "absolute", left: 120, top: 226 + i * 60, display: "flex", alignItems: "baseline", gap: 18, opacity: pf(at("start", 0.1 + 0.2 * i), 16) }}>
            <span style={{ fontFamily: font.serif, fontSize: 44, color: on > 0.5 ? color.accent : color.ink3, fontFeatureSettings: "'lnum' 1", width: 26 }}>{i + 1}</span>
            <span style={{ fontSize: 44, color: on > 0.5 ? color.ink : color.ink3, fontWeight: on > 0.5 ? 600 : 400 }}>{s}</span>
            {i < 2 && <span style={{ fontSize: 34, color: color.ink3 }}>→</span>}
          </div>
        );
      })}
      <div style={{ position: "absolute", left: 120, top: 414, width: 560, height: 2, background: color.rule, opacity: pf(tRect, 16) }} />

      {/* rect */}
      <div style={{ opacity: win(tRect + 4, tUnf, 14) }}>
        <Txt x={120} y={444} w={600} size={type.body} lh={1.4} p={pf(tRect + 6, 24)}>
          {r(T.rectLine)}
        </Txt>
        <Txt x={120} y={660} w={600} size={type.caption} c={color.ink2} p={pf(runEnd, 20)}>
          {T.rectNote}
        </Txt>
      </div>
      {/* unfold */}
      <div style={{ opacity: win(tUnf + 4, tCube, 14) }}>
        <Txt x={120} y={444} w={600} size={type.body} p={pf(lineEnd, 22)}>
          {r(T.lcm)}
        </Txt>
        <Txt x={120} y={520} w={600} size={48} lh={1.2} p={pf(lineEnd + 10, 24)}>
          {r(T.bounceLine)}
        </Txt>
        <Txt x={120} y={610} w={720} size={type.caption} lh={1.4} c={color.ink2} p={pf(at("unfold", 0.7), 22)}>
          {r(T.lcmNote)}
        </Txt>
      </div>
      {/* cube */}
      <div style={{ opacity: win(tCube + 4, tSame, 14) }}>
        <Txt x={120} y={440} w={620} size={34} lh={1.5} p={pf(tCube + 30, 30)}>
          {r(T.cube)}
        </Txt>
      </div>
      <Txt x={120} y={960} w={700} size={34} c={color.ink3} p={pf(tCube + 30, 20)} o={1 - pf(at("same", 0.9), 14)}>
        {T.source}
      </Txt>
      {/* same */}
      <div style={{ opacity: pf(tSame + 4, 14) }}>
        <Txt x={120} y={440} w={620} size={34} c={color.ink2} p={pf(tSame + 20, 20)}>
          {T.firstVertex}
        </Txt>
        <Txt x={120} y={506} w={700} size={40} lh={1.3} p={pf(tSame + 40, 24)}>
          {r(T.sLine)}
        </Txt>
        <M x={120} y={640} t="12\times(12,7,5)=" size={44} p={pf(at("same", 0.4), 24)} />
        <M x={120 + texW("12\\times(12,7,5)=", 44) + 12} y={640} t="(144,\,84,\,60)" size={44} c={POCKET} p={pf(at("same", 0.4) + 16, 24)} />
        <M x={120} y={740} t="L=12\sqrt{144+49+25}=12\sqrt{218}" size={44} p={pf(at("same", 0.62), 24)} />
        <Txt x={120} y={790} w={600} size={type.caption} c={color.ink2} p={pf(at("same", 0.8), 22)}>
          {r(T.answer)}
        </Txt>
      </div>
    </Sheet>
  );
};
