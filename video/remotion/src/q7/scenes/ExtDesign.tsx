/**
 * zh extension 1 (EXTENSION.zh.md §二): why corners + edge midpoints take the
 * answer from ∞ to 0. The lattice splits by parity into four classes — centre
 * (even, even) blue, corner (odd, odd) red, left/right midpoint (odd, even)
 * solid ochre ring, top/bottom midpoint (even, odd) dashed ochre ring — shown
 * on the plane and as a 2×2 parity dictionary. The first lattice point (p, q)
 * is never blue; (a) blocks one class, (b) all three. Then the variants: only
 * left/right midpoints (the vertical shot comes home), any one midpoint
 * missing (a shot comes home), and the bounce count |p|+|q| is odd.
 */
import React from "react";
import { interpolate, spring } from "remotion";
import { color, features, font, type } from "../../theme";
import { clamp } from "../../components/Type";
import {
  Ball,
  Caps,
  EDGE,
  Flash,
  HOMEC,
  Kicker,
  Layer,
  M,
  Mark,
  POCKET,
  R_POCKET,
  Sheet,
  Table,
  Txt,
  W_POCKET,
  World,
  dOf,
  mLbl,
  px,
  pxs,
  tableMarks,
  texW,
  useS,
  useT,
} from "../kit";
import { V, polyAt, realPath, shot } from "../geo";
import { Grid, PlaneMask } from "./Dictionary";

const HOMEPATH = realPath(shot([2, 1], 2));
const CUT = realPath(shot([2, 1], 1));

// ── The plane ───────────────────────────────────────────────────────────────
const PW: World = { ox: 1290, oy: 590, u: 110 };
const HERO: World = { ox: 1290, oy: 590, u: 230 };
type Cls = "home" | "corner" | "lr" | "tb";
const clsOf = ([x, y]: V): Cls => {
  const ox = Math.abs(x) % 2 === 1;
  const oy = Math.abs(y) % 2 === 1;
  return ox && oy ? "corner" : ox ? "lr" : oy ? "tb" : "home";
};
const LATTICE: V[] = [];
for (let x = -4; x <= 4; x++) for (let y = -3; y <= 3; y++) LATTICE.push([x, y]);
/** the order the narration names them */
const ORDER: Cls[] = ["home", "corner", "lr", "tb"];
const CUE = [0.21, 0.32, 0.46, 0.74];

/** an edge-midpoint ring: solid (left/right) or dashed (top/bottom) */
const MidRing: React.FC<{ x: number; y: number; dashed: boolean; r?: number; o?: number; k?: number }> = ({ x, y, dashed, r = R_POCKET, o = 1, k = 1 }) => (
  <circle
    cx={x}
    cy={y}
    r={Math.max(0.5, r * k)}
    fill={color.paper}
    stroke={EDGE}
    strokeWidth={W_POCKET}
    strokeDasharray={dashed ? `${(r * k * Math.PI) / 5} ${(r * k * Math.PI) / 7.5}` : undefined}
    opacity={o}
  />
);
const Sym: React.FC<{ c: Cls; x: number; y: number; r?: number; o?: number; k?: number }> = ({ c, x, y, r = R_POCKET, o = 1, k = 1 }) => {
  if (k <= 0.01) return null;
  if (c === "home") return <circle cx={x} cy={y} r={r * 0.75 * k} fill={HOMEC} opacity={o} />;
  if (c === "corner") return <circle cx={x} cy={y} r={r * k} fill={color.paper} stroke={POCKET} strokeWidth={W_POCKET} opacity={o} />;
  return <MidRing x={x} y={y} r={r} k={k} dashed={c === "tb"} o={o} />;
};

// ── The 2×2 parity dictionary (left column) ────────────────────────────────
const CX = [210, 450];
const CY = [300, 470];
const CW = 240;
const CH = 170;
/** cell of a class: column = parity of x, row = parity of y */
const CELL: Record<Cls, [number, number]> = { home: [0, 0], lr: [1, 0], tb: [0, 1], corner: [1, 1] };
/** where each class sits on the real table */
const ON_TABLE: Record<Cls, V[]> = {
  home: [[0, 0]],
  corner: [
    [1, 1],
    [-1, 1],
    [-1, -1],
    [1, -1],
  ],
  lr: [
    [1, 0],
    [-1, 0],
  ],
  tb: [
    [0, 1],
    [0, -1],
  ],
};

export const ExtDesign: React.FC = () => {
  const { f, fps, at, p, pf, guard } = useS();
  const { ext, r, tLbl } = useT();
  const T = ext.design;
  const tCl = at("classes");
  const tFirst = at("first");
  const tAb = at("ab");
  const tB = at("ab", 0.5);
  const tLr = at("lr");
  const tEach = at("each");
  const tOdd = at("odd");
  const win = (a: number, b: number, len = 18) => pf(a, len) * (1 - pf(b, len));
  const cue = (c: Cls) => at("classes", CUE[ORDER.indexOf(c)]);
  const pop = (t0: number, d = 0) => spring({ frame: f - t0 - d, fps, config: { damping: 14, stiffness: 170, mass: 0.6 } });

  // ── right-hand phases ──
  const heroIn = p("start", 34, 6);
  const morph = interpolate(f, [tCl, tCl + 40], [0, 1], { ...clamp, easing: (x) => 0.5 - 0.5 * Math.cos(Math.PI * x) });
  const planeO = 1 - pf(tAb, 18);
  const W: World = { ox: PW.ox, oy: PW.oy, u: HERO.u + (PW.u - HERO.u) * morph };
  const abO = win(tAb + 12, tLr);
  const lrO = win(tLr + 12, tEach);
  const eachO = win(tEach + 10, tOdd);
  const oddO = pf(tOdd + 10, 18);

  // ── dictionary state ──
  const dictO = pf(tCl + 6, 20) * (1 - 0.55 * pf(tEach, 18));
  const blueDim = 1 - 0.6 * win(tFirst + 20, tAb);
  const crossA = pf(tAb + 16, 18) * (1 - pf(tLr, 12)); // corner, from (a) on
  const crossB = pf(tB + 10, 18) * (1 - pf(tLr, 12)); // the two midpoint classes, (b)
  const passA = pf(tAb + 30, 18) * (1 - pf(tB + 4, 12));
  const crossLr = pf(tLr + 16, 18); // corner + left/right from the `lr` beat on
  const passTb = pf(tLr + 30, 18) * (1 - pf(tEach, 18));
  const crossAll = pf(tEach, 18);
  const crossed = (c: Cls) =>
    c === "home" ? 0 : Math.max(c === "corner" ? crossA : crossB, c === "tb" ? crossAll : Math.max(crossLr, crossAll));
  const passed = (c: Cls) => (c === "lr" ? passA : c === "tb" ? Math.max(passA, passTb) : 0);

  // ── the plane's first-point rays ──
  const rays: Array<{ d: V; c: Cls; t0: number }> = [
    { d: [1, 1], c: "corner", t0: tFirst + 12 },
    { d: [1, 0], c: "lr", t0: tFirst + 62 },
    { d: [2, 1], c: "tb", t0: tFirst + 112 },
  ];
  const rayP = (t0: number) => interpolate(f, [t0, t0 + 26], [0, 1], { ...clamp, easing: (x) => 1 - Math.pow(1 - x, 3) });
  const lblOf = (d: V, t0: number) => {
    const [a, b] = px(PW, d);
    const below = d[1] === 0;
    return { x: a + 22, y: below ? b + 50 : b - 24, t: `(${d[0]},\\,${d[1]})`, size: 32, c: color.ink, p: pf(t0 + 22, 18), o: planeO };
  };
  const rayLbls = rays.map((q) => lblOf(q.d, q.t0));

  // ── lr: the vertical shot ──
  const LR: World = { ox: 1290, oy: 600, u: 290 };
  const UP: V[] = [
    [0, 0],
    [0, 1],
    [0, 0],
  ];
  const upRun = interpolate(f, [at("lr", 0.4), at("lr", 0.4) + 48], [0, 1], clamp);
  const upHome = f - (at("lr", 0.4) + 48);
  const noHole = { s: T.noHole, x: 1316, y: px(LR, [0, 1])[1] - 66 };

  // ── each: four seven-pocket tables ──
  const EACH: Array<{ W: World; m: V; lbl: string }> = [
    { W: { ox: 1080, oy: 400, u: 130 }, m: [1, 0], lbl: T.missing[0] },
    { W: { ox: 1500, oy: 400, u: 130 }, m: [-1, 0], lbl: T.missing[1] },
    { W: { ox: 1080, oy: 800, u: 130 }, m: [0, 1], lbl: T.missing[2] },
    { W: { ox: 1500, oy: 800, u: 130 }, m: [0, -1], lbl: T.missing[3] },
  ];
  const eachRun = (i: number) => interpolate(f, [tEach + 24 + i * 38, tEach + 24 + i * 38 + 34], [0, 1], clamp);

  // ── odd: three shots that come home, counted ──
  const ODD: Array<{ d: V; W: World }> = [
    { d: [1, 0], W: { ox: 1010, oy: 500, u: 125 } },
    { d: [2, 1], W: { ox: 1340, oy: 500, u: 125 } },
    { d: [1, 4], W: { ox: 1670, oy: 500, u: 125 } },
  ];
  const oddPaths = ODD.map((o) => realPath(shot(o.d, 2)));
  const oddRun = (i: number) => interpolate(f, [tOdd + 30 + i * 62, tOdd + 30 + i * 62 + 56], [0, 1], clamp);

  // ── guard ──
  const marks: Mark[] = [
    ...[-5, -3, -1, 1, 3, 5].map((x): Mark => ({ name: `wall x=${x}`, pts: pxs(PW, [[x, -8], [x, 9]]), w: 1.8, on: morph >= 1 && planeO > 0.05 })),
    ...[-5, -3, -1, 1, 3, 5].map((y): Mark => ({ name: `wall y=${y}`, pts: pxs(PW, [[-9, y], [11, y]]), w: 1.8, on: morph >= 1 && planeO > 0.05 })),
    ...LATTICE.map((v): Mark => ({ name: `lattice ${v}`, pts: [px(PW, v)], w: 2 * R_POCKET + W_POCKET, on: morph >= 1 && planeO > 0.05 })),
    ...rays.map((q): Mark => ({ name: `ray ${q.d}`, pts: pxs(PW, [[0, 0], q.d]), w: 4, on: rayP(q.t0) > 0 && planeO > 0.05 })),
    ...tableMarks(LR, "lr table", [0, 0], "lr", true, lrO > 0.05),
    { name: "top ghost", pts: [px(LR, [0, 1])], w: 2 * R_POCKET + 2, on: lrO > 0.05 },
  ];
  guard(marks, [...rayLbls.map((l) => mLbl(l)), tLbl(noHole.s, noHole.x, noHole.y, type.caption, pf(tLr + 30, 20), lrO)]);

  const headO = 1 - pf(tCl, 16);
  const inf = texW("\\infty", 130);
  const arr = texW("\\to", 130);

  return (
    <Sheet folio={17} title={T.title}>
      <Layer>
        {/* start → classes: the (b) table becomes the real table of the plane */}
        {planeO > 0 && (
          <g opacity={planeO}>
            <PlaneMask id="q7-ext-design" x={800} y={190} w={1060} h={800} />
            <g mask="url(#q7-ext-design)">
              <Grid W={PW} o={morph} xs={[-5, -3, -1, 1, 3, 5]} ys={[-5, -3, -1, 1, 3, 5]} />
              <Table W={W} real draw={heroIn} pockets="all" split pocketO={1 - morph} home={morph < 0.5} />
              {LATTICE.map((v, i) => {
                const c = clsOf(v);
                const k = pop(cue(c), Math.hypot(v[0], v[1]) * 3);
                const [x, y] = px(PW, v);
                return <Sym key={i} c={c} x={x} y={y} k={Math.min(k, 1.15)} />;
              })}
              {rays.map((q) => {
                const g = rayP(q.t0);
                if (g <= 0) return null;
                return <path key={q.c} d={dOf(PW, [[0, 0], [q.d[0] * g, q.d[1] * g]])} stroke={color.ink} strokeWidth={4} strokeLinecap="round" />;
              })}
              {rays.map((q) => (
                <Flash key={q.c} W={PW} p={q.d} t={(f - q.t0 - 26) / 26} c={q.c === "corner" ? POCKET : EDGE} r1={50} />
              ))}
            </g>
          </g>
        )}

        {/* ab: (a) four pockets → ∞, (b) eight → 0 */}
        {abO > 0 && (
          <g opacity={abO}>
            <Table W={{ ox: 1080, oy: 470, u: 150 }} real draw={pf(tAb + 12, 24)} />
            <path d={dOf({ ox: 1080, oy: 470, u: 150 }, polyAt(HOMEPATH, interpolate(f, [tAb + 40, tAb + 110], [0, 1], clamp)).upto)} fill="none" stroke={color.ink} strokeWidth={3.2} strokeLinejoin="round" />
            <Table W={{ ox: 1560, oy: 470, u: 150 }} real draw={pf(tB, 24)} pockets="all" split />
            <path d={dOf({ ox: 1560, oy: 470, u: 150 }, polyAt(CUT, interpolate(f, [tB + 26, tB + 70], [0, 1], clamp)).upto)} fill="none" stroke={color.ink} strokeWidth={3.2} strokeLinejoin="round" />
            <Flash W={{ ox: 1560, oy: 470, u: 150 }} p={[0, 1]} t={(f - tB - 70) / 24} c={EDGE} r1={40} />
            <line x1={1320} y1={260} x2={1320} y2={880} stroke={color.rule} strokeWidth={1.5} />
          </g>
        )}

        {/* lr: only the left/right midpoints — straight up, off the empty top midpoint, home */}
        {lrO > 0 && (
          <g opacity={lrO}>
            <Table W={LR} real pockets="lr" split ghosts />
            {upRun > 0 && upHome < 40 && <path d={dOf(LR, polyAt(UP, upRun).upto)} fill="none" stroke={color.ink} strokeWidth={3.6} strokeLinecap="round" />}
            {upRun > 0 && <Ball W={LR} p={polyAt(UP, upRun).p} />}
            <Flash W={LR} p={[0, 0]} t={upHome / 26} c={HOMEC} r1={56} />
            {upHome > 0 && <circle cx={LR.ox} cy={LR.oy} r={22} fill="none" stroke={HOMEC} strokeWidth={3} />}
          </g>
        )}

        {/* each: eight pockets less one — a shot straight at the gap comes home */}
        {eachO > 0 && (
          <g opacity={eachO}>
            {EACH.map(({ W: E, m }, i) => {
              const run = eachRun(i);
              const path: V[] = [[0, 0], m, [0, 0]];
              const home = f - (tEach + 24 + i * 38 + 34);
              return (
                <g key={i}>
                  <Table W={E} real pockets={{ missing: m }} split ghosts lineW={3.4} pr={10} />
                  {run > 0 && home < 30 && <path d={dOf(E, polyAt(path, run).upto)} fill="none" stroke={color.ink} strokeWidth={3} strokeLinecap="round" />}
                  {run > 0 && <Ball W={E} p={polyAt(path, run).p} r={9} />}
                  <Flash W={E} p={[0, 0]} t={home / 24} c={HOMEC} r1={40} />
                  {home > 0 && <circle cx={E.ox} cy={E.oy} r={18} fill="none" stroke={HOMEC} strokeWidth={3} />}
                </g>
              );
            })}
          </g>
        )}

        {/* odd: |p| + |q| bounces, always odd */}
        {oddO > 0 && (
          <g opacity={oddO}>
            {ODD.map((o, i) => {
              const run = oddRun(i);
              const { p: head, upto } = polyAt(oddPaths[i], run);
              const home = f - (tOdd + 30 + i * 62 + 56);
              return (
                <g key={i}>
                  <Table W={o.W} real lineW={3.4} pr={10} />
                  {run > 0 && <path d={dOf(o.W, upto)} fill="none" stroke={color.ink} strokeWidth={3} strokeLinejoin="round" />}
                  {run > 0 && <Ball W={o.W} p={head} r={9} />}
                  <Flash W={o.W} p={[0, 0]} t={home / 24} c={HOMEC} r1={40} />
                  {home > 0 && <circle cx={o.W.ox} cy={o.W.oy} r={18} fill="none" stroke={HOMEC} strokeWidth={3} />}
                </g>
              );
            })}
          </g>
        )}

        {/* the dictionary's symbols, crosses and ticks */}
        {dictO > 0 &&
          ORDER.map((c) => {
            const [col, row] = CELL[c];
            const x0 = CX[col];
            const y0 = CY[row];
            const k = pop(cue(c));
            const o = dictO * (c === "home" ? blueDim : 1);
            const IW: World = { ox: x0 + 196, oy: y0 + 118, u: 28 };
            const xc = crossed(c);
            const ps = passed(c) * (1 - xc);
            return (
              <g key={c} opacity={o}>
                <rect x={x0} y={y0} width={CW} height={CH} fill="none" stroke={color.rule} strokeWidth={1.5} opacity={Math.min(1, k)} />
                <Sym c={c} x={x0 + 32} y={y0 + 46} r={13} k={Math.min(k, 1.15)} />
                {k > 0.5 && (
                  <g opacity={Math.min(1, (k - 0.5) * 2)}>
                    <path d={dOf(IW, [[-1, -1], [1, -1], [1, 1], [-1, 1], [-1, -1]])} fill="none" stroke={color.ink2} strokeWidth={2} />
                    {ON_TABLE[c].map((v, i) => {
                      const [x, y] = px(IW, v);
                      return <Sym key={i} c={c} x={x} y={y} r={6} />;
                    })}
                  </g>
                )}
                {/* blocked: a red wash (+ 「堵住」); let through: 「放行」 in ink3 */}
                {xc > 0 && <rect x={x0 + 1} y={y0 + 1} width={CW - 2} height={CH - 2} fill={POCKET} opacity={0.09 * xc} />}
                {ps > 0 && <rect x={x0 + 1} y={y0 + 1} width={CW - 2} height={CH - 2} fill="none" stroke={color.ink3} strokeWidth={2.5} strokeDasharray="6 6" opacity={ps} />}
              </g>
            );
          })}
      </Layer>

      <Kicker x={120} y={150} p={p("start", 22)}>
        {T.kicker}
      </Kicker>

      {/* start: the headline */}
      <div style={{ opacity: headO }}>
        <Txt x={120} y={232} w={600} size={56} p={p("start", 26, 10)}>
          {T.lead}
        </Txt>
        <M x={124} y={420} t="\infty" size={130} c={HOMEC} p={p("start", 24, 30)} />
        <M x={124 + inf + 24} y={420} t="\to" size={130} c={color.ink2} p={p("start", 24, 44)} />
        <M x={124 + inf + arr + 48} y={420} t="0" size={130} c={POCKET} p={p("start", 24, 58)} />
        <Txt x={120} y={470} w={600} size={type.caption} c={color.ink2} p={p("start", 24, 90)}>
          {T.after}
        </Txt>
      </div>

      {/* the dictionary: axes and labels */}
      <div style={{ opacity: dictO }}>
        <Txt x={120} y={236} w={120} size={type.caption} c={color.ink3} p={pf(tCl + 6, 20)}>
          {T.xAxis}
        </Txt>
        <Txt x={CX[0] + CW / 2} y={236} w={80} align="center" size={type.caption} c={color.ink2} p={pf(tCl + 6, 20)}>
          {T.even}
        </Txt>
        <Txt x={CX[1] + CW / 2} y={236} w={80} align="center" size={type.caption} c={color.ink2} p={pf(tCl + 6, 20)}>
          {T.odd}
        </Txt>
        <Txt x={172} y={CY[0] + CH / 2 - 24} w={40} align="center" size={type.caption} c={color.ink2} p={pf(tCl + 6, 20)}>
          {T.even}
        </Txt>
        <Txt x={172} y={CY[1] + CH / 2 - 24} w={40} align="center" size={type.caption} c={color.ink2} p={pf(tCl + 6, 20)}>
          {T.odd}
        </Txt>
        <div
          style={{
            position: "absolute",
            left: 112,
            top: CY[0] + 104,
            writingMode: "vertical-rl",
            fontSize: 36,
            color: color.ink3,
            letterSpacing: "0.1em",
            opacity: pf(tCl + 6, 20),
          }}
        >
          {T.yAxis}
        </div>
        {ORDER.map((c) => {
          const [col, row] = CELL[c];
          const lbl = { home: T.centre, corner: T.corner, lr: T.lrMid, tb: T.tbMid }[c];
          const o = c === "home" ? blueDim : 1;
          return (
            <React.Fragment key={c}>
              <Txt x={CX[col] + 18} y={CY[row] + 100} w={140} size={34} c={color.ink} o={o} p={pf(cue(c) + 8, 18)}>
                {lbl}
              </Txt>
              <Txt x={CX[col] + 56} y={CY[row] + 24} w={110} size={34} c={color.ink2} o={o} p={pf(cue(c) + 8, 18)}>
                {T.tags[c]}
              </Txt>
              <Txt x={CX[col] + CW - 10} y={CY[row] + 4} w={80} align="right" size={34} c={color.ink3} p={passed(c)} o={1 - crossed(c)}>
                {T.pass}
              </Txt>
              <Txt x={CX[col] + CW - 10} y={CY[row] + 4} w={80} align="right" size={34} c={POCKET} p={crossed(c)}>
                {T.block}
              </Txt>
            </React.Fragment>
          );
        })}
      </div>

      {/* left, lower: one block per beat */}
      <div style={{ opacity: win(tFirst + 6, tAb, 14) }}>
        <Txt x={120} y={680} w={600} size={40} lh={1.35} p={pf(tFirst + 6, 26)}>
          {r(T.firstLine)}
        </Txt>
        <Txt x={120} y={800} w={600} size={type.caption} c={HOMEC} p={pf(tFirst + 40, 22)}>
          {T.notBlue}
        </Txt>
      </div>
      <div style={{ opacity: win(tAb + 6, tLr, 14) }}>
        <Txt x={120} y={680} w={600} size={type.caption} p={pf(tAb + 16, 22)}>
          {T.aLine}
        </Txt>
        <Txt x={120} y={740} w={600} size={type.caption} p={pf(tB + 10, 22)}>
          {T.bLine}
        </Txt>
      </div>
      <div style={{ opacity: win(tLr + 6, tEach, 14) }}>
        <Txt x={120} y={680} w={600} size={type.body} p={pf(tLr + 10, 22)}>
          {T.lrLine}
        </Txt>
        <Txt x={120} y={746} w={720} size={type.caption} lh={1.4} c={color.ink2} p={pf(at("lr", 0.4), 22)}>
          {r(T.lrNote)}
        </Txt>
      </div>
      <div style={{ opacity: win(tEach + 6, tOdd, 14) }}>
        <Txt x={120} y={680} w={600} size={type.body} lh={1.35} p={pf(tEach + 10, 22)}>
          {T.eachLine}
        </Txt>
        <Txt x={120} y={816} w={600} size={type.caption} c={color.ink2} p={pf(at("each", 0.55), 22)}>
          {T.eachNote}
        </Txt>
      </div>
      <div style={{ opacity: pf(tOdd + 6, 14) }}>
        <Txt x={120} y={674} w={600} size={type.caption} c={color.ink2} p={pf(tOdd + 10, 20)}>
          {T.oddWhen}
        </Txt>
        <Txt x={120} y={726} w={600} size={48} lh={1.2} p={pf(tOdd + 24, 24)}>
          {r(T.oddLine)}
        </Txt>
        <Txt x={120} y={806} w={600} size={type.caption} c={color.ink2} p={pf(at("odd", 0.55), 22)}>
          {T.oddNote}
        </Txt>
      </div>

      {/* right-hand captions */}
      {rayLbls.map((l) => (
        <M key={l.t} {...l} />
      ))}
      <div style={{ opacity: abO }}>
        <div style={{ position: "absolute", left: 880, top: 238, width: 400, textAlign: "center" }}>
          <Caps color={color.ink2}>{T.aCap}</Caps>
        </div>
        <div style={{ position: "absolute", left: 1360, top: 238, width: 400, textAlign: "center", opacity: pf(tB, 20) }}>
          <Caps color={color.ink2}>{T.bCap}</Caps>
        </div>
        <M x={1080} y={800} t="\infty" size={150} align="center" c={HOMEC} p={pf(tAb + 40, 26)} />
        <div
          style={{
            position: "absolute",
            left: 1460,
            width: 200,
            top: 670,
            textAlign: "center",
            fontFamily: font.serif,
            fontSize: 150,
            lineHeight: 1,
            color: POCKET,
            fontFeatureSettings: features.figures,
            opacity: pf(tB + 40, 20),
          }}
        >
          0
        </div>
      </div>
      <div style={{ opacity: lrO }}>
        <Txt x={noHole.x} y={noHole.y} w={200} size={type.caption} c={color.ink3} p={pf(tLr + 30, 20)}>
          {noHole.s}
        </Txt>
        <div style={{ position: "absolute", left: LR.ox - 300, top: px(LR, [0, -1])[1] + 34, width: 600, textAlign: "center" }}>
          <Caps color={color.ink2}>{T.lrCap}</Caps>
        </div>
      </div>
      <div style={{ opacity: eachO }}>
        {EACH.map(({ W: E, lbl }, i) => (
          <div key={i} style={{ position: "absolute", left: E.ox - 150, top: E.oy - E.u - 62, width: 300, textAlign: "center" }}>
            <Caps color={color.ink2}>{lbl}</Caps>
          </div>
        ))}
      </div>
      <div style={{ opacity: oddO }}>
        {ODD.map((o, i) => {
          const { upto } = polyAt(oddPaths[i], oddRun(i));
          const n = oddRun(i) > 0 ? upto.length - 2 : 0;
          const done = oddRun(i) >= 1;
          return (
            <React.Fragment key={i}>
              <M x={o.W.ox} y={o.W.oy - o.W.u - 28} t={`(p,q)=(${o.d[0]},${o.d[1]})`} size={36} align="center" p={pf(tOdd + 16 + i * 62, 20)} />
              <div
                style={{
                  position: "absolute",
                  left: o.W.ox - 100,
                  width: 200,
                  top: o.W.oy + o.W.u + 30,
                  textAlign: "center",
                  fontFamily: font.serif,
                  fontSize: 120,
                  lineHeight: 1,
                  color: done ? EDGE : color.ink3,
                  fontFeatureSettings: features.figures,
                  opacity: pf(tOdd + 30 + i * 62, 12),
                }}
              >
                {n}
              </div>
            </React.Fragment>
          );
        })}
        <div style={{ position: "absolute", left: 860, top: 800, width: 960, textAlign: "center", opacity: pf(tOdd + 30, 20) }}>
          <Caps color={color.ink2}>{T.bounces}</Caps>
        </div>
      </div>
    </Sheet>
  );
};
