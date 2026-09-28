/**
 * The halfway test. Aim at the first (even, even) point on the ray, (2p, 2q)
 * with gcd(p, q) = 1; the only lattice points on the segment are its ends and
 * the midpoint (p, q). Both odd → a corner copy → pocketed halfway ((1,1));
 * one odd one even → safe → home ((1,2)); both even → impossible.
 */
import React from "react";
import { interpolate } from "remotion";
import { color, type } from "../../theme";
import { clamp } from "../../components/Type";
import { Ball, EDGE, Flash, HOMEC, HomeDot, Kicker, Layer, M, Mark, POCKET, Pocket, R_POCKET, Sheet, Txt, W_POCKET, World, dOf, mLbl, px, pxs, useS, useT } from "../kit";
import { V, polyAt } from "../geo";
import { Grid, PlaneMask } from "./Dictionary";

const W: World = { ox: 900, oy: 860, u: 100 };
const pts = (pred: (x: number, y: number) => boolean): V[] => {
  const out: V[] = [];
  for (let x = -1; x <= 9; x++) for (let y = -1; y <= 6; y++) if (pred(x, y)) out.push([x, y]);
  return out;
};
const ev = (v: number) => Math.abs(v) % 2 === 0;
const HOMES = pts((x, y) => ev(x) && ev(y));
const CORN = pts((x, y) => !ev(x) && !ev(y));
const MIX = pts((x, y) => ev(x) !== ev(y));
const same = (a: V, b: V) => a[0] === b[0] && a[1] === b[1];

export const Halfway: React.FC = () => {
  const { f, at, p, pf, atWord, has, guard } = useS();
  const { t, r, it } = useT();
  const T = t.halfway;
  const seg = p("start", 40, 20);
  const only = p("only", 24);
  const mid = p("mid", 24);
  // second sentence of `only` ("The only lattice points on the segment ..."): its own beat `list` where the
  // storyboard has one (the zh cut: beat-unit TTS, no word timing), else the spoken phrase; the mock has no word timing
  const tList = has("list") ? at("list") : atWord("The only lattice points", { afterFrame: at("only") }) ?? at("only", 0.42);
  const onlyList = pf(tList, 26);
  const onlyListM = pf(tList + 16, 26);
  const oddT = at("odd");
  const mixT = at("mixed");
  const demo = interpolate(f, [oddT, oddT + 20], [0, 1], clamp); // the generic segment steps back
  const onSeg: V[] = [
    [0, 0],
    [3, 2],
    [6, 4],
  ];
  const dimOther = 1 - 0.75 * only;
  const onD1: V[] = [
    [0, 0],
    [1, 1],
    [2, 2],
  ];
  const onD2: V[] = [
    [0, 0],
    [1, 2],
    [2, 4],
  ];

  // demo 1: (1,1) → pocketed at the midpoint
  const b1 = interpolate(f, [oddT + 40, oddT + 80], [0, 1], clamp);
  const b1end = f - (oddT + 80);
  // demo 2: (1,2) → through the safe midpoint (1,2), home at (2,4)
  const b2 = interpolate(f, [mixT + 30, mixT + 110], [0, 1], clamp);
  const b2end = f - (mixT + 110);
  const d1o = interpolate(f, [mixT, mixT + 20], [1, 0.2], clamp);

  const genO = 1 - demo;
  const mixOn = interpolate(f, [mixT, mixT + 20], [0, 1], clamp);
  // emphasis: the points on whichever segment is being discussed stay at full strength
  const alpha = (v: V) => {
    const on = (set: V[]) => (set.some((s) => same(s, v)) ? 1 : 0);
    const w = on(onSeg) * genO + on(onD1) * demo * (1 - mixOn) + on(onD2) * mixOn;
    return Math.max(dimOther, Math.min(1, w));
  };
  const L = {
    target: { x: px(W, [6, 4])[0], y: px(W, [6, 4])[1] - 34, align: "center" as const,t: "(2p,\\,2q)", size: 40, c: HOMEC, p: seg, o: genO },
    mid: { x: px(W, [3, 2])[0] + 22, y: px(W, [3, 2])[1] + 44, t: "(p,\\,q)", size: 40, c: EDGE, p: p("only", 24, 20), o: genO },
    d1: { x: px(W, [1, 1])[0] + 22, y: px(W, [1, 1])[1] + 46, t: "(1,\\,1)", size: 34, c: POCKET, p: interpolate(f, [oddT + 20, oddT + 40], [0, 1], clamp), o: 1 - mixOn },
    d2: { x: px(W, [1, 2])[0] + 22, y: px(W, [1, 2])[1] + 40, t: "(1,\\,2)", size: 34, c: color.ink2, p: interpolate(f, [mixT + 20, mixT + 40], [0, 1], clamp) },
    d2b: { x: px(W, [2, 4])[0], y: px(W, [2, 4])[1] - 34, align: "center" as const, t: "(2,\\,4)", size: 34, c: HOMEC, p: interpolate(f, [mixT + 20, mixT + 40], [0, 1], clamp) },
  };
  const marks: Mark[] = [
    ...[-1, 1, 3, 5, 7, 9].map((x): Mark => ({ name: `wall x=${x}`, pts: pxs(W, [[x, -8], [x, 9]]), w: 1.8 })),
    ...[-1, 1, 3, 5].map((y): Mark => ({ name: `wall y=${y}`, pts: pxs(W, [[-9, y], [11, y]]), w: 1.8 })),
    ...HOMES.map((v): Mark => ({ name: `home ${v}`, pts: [px(W, v)], w: 18 })),
    ...CORN.map((v): Mark => ({ name: `pocket ${v}`, pts: [px(W, v)], w: 2 * R_POCKET + W_POCKET })),
    ...MIX.map((v): Mark => ({ name: `lattice ${v}`, pts: [px(W, v)], w: 10 })),
    { name: "segment", pts: pxs(W, [[0, 0], [6, 4]]), w: 4, on: seg > 0 && genO > 0.05 },
    { name: "demo (1,1)", pts: pxs(W, [[0, 0], [1, 1]]), w: 4, on: b1 > 0 },
    { name: "demo (1,2)", pts: pxs(W, [[0, 0], [2, 4]]), w: 4, on: b2 > 0 },
  ];
  guard(marks, Object.entries(L).map(([k, l]) => mLbl(l, k)));

  const midGlow = mid * genO;
  const outcome = [POCKET, HOMEC, color.ink3];
  const cases: Array<[string, string, string, number]> = [
    [...T.cases[0], outcome[0], p("odd", 24)],
    [...T.cases[1], outcome[1], p("mixed", 24)],
    [...T.cases[2], outcome[2], p("mixed", 24, 110)],
  ];

  return (
    <Sheet folio={12} title={T.title}>
      <Layer>
        <PlaneMask id="q7-half" x={780} y={150} w={1080} h={860} />
        <g mask="url(#q7-half)">
          <Grid W={W} xs={[-1, 1, 3, 5, 7, 9]} ys={[-1, 1, 3, 5]} />
          {MIX.map((v, i) => {
            const [x, y] = px(W, v);
            return <circle key={i} cx={x} cy={y} r={5} fill={color.ink3} opacity={alpha(v)} />;
          })}
          {HOMES.map((v, i) => (
            <HomeDot key={i} W={W} p={v} r={9} o={alpha(v)} />
          ))}
          {CORN.map((v, i) => (
            <Pocket key={i} W={W} p={v} o={alpha(v)} />
          ))}
          {/* the generic segment and its midpoint */}
          {seg > 0 && <path d={dOf(W, [[0, 0], polyAt([[0, 0], [6, 4]], seg).p])} stroke={color.ink} strokeWidth={4} strokeLinecap="round" opacity={genO} />}
          {midGlow > 0 && <circle cx={px(W, [3, 2])[0]} cy={px(W, [3, 2])[1]} r={16 + 4 * Math.sin(f / 7)} fill="none" stroke={EDGE} strokeWidth={3.5} opacity={midGlow} />}
          {/* demo 1 */}
          {b1 > 0 && (
            <g opacity={d1o}>
              <path d={dOf(W, [[0, 0], polyAt([[0, 0], [1, 1]], b1).p])} stroke={color.ink} strokeWidth={4} strokeLinecap="round" />
              <path d={dOf(W, [[1, 1], [2, 2]])} stroke={color.ink3} strokeWidth={2.5} strokeDasharray="4 8" opacity={b1 >= 1 ? 1 : 0} />
              {b1end < 10 && <Ball W={W} p={polyAt([[0, 0], [1, 1]], b1).p} r={11 * interpolate(b1end, [0, 10], [1, 0.2], clamp)} />}
              <Flash W={W} p={[1, 1]} t={b1end / 26} c={POCKET} r1={50} />
            </g>
          )}
          {/* demo 2 */}
          {b2 > 0 && (
            <g>
              <path d={dOf(W, [[0, 0], polyAt([[0, 0], [2, 4]], b2).p])} stroke={color.ink} strokeWidth={4} strokeLinecap="round" />
              <circle cx={px(W, [1, 2])[0]} cy={px(W, [1, 2])[1]} r={16} fill="none" stroke={EDGE} strokeWidth={3.5} opacity={interpolate(b2, [0.42, 0.52], [0, 1], clamp)} />
              <Ball W={W} p={polyAt([[0, 0], [2, 4]], b2).p} />
              <Flash W={W} p={[2, 4]} t={b2end / 26} c={HOMEC} r1={50} />
              {b2end > 0 && <circle cx={px(W, [2, 4])[0]} cy={px(W, [2, 4])[1]} r={21} fill="none" stroke={HOMEC} strokeWidth={3} />}
            </g>
          )}
        </g>
      </Layer>
      {Object.entries(L).map(([k, l]) => (
        <M key={k} {...l} />
      ))}

      <Kicker x={120} y={150} p={p("start", 22)}>
        {T.kicker}
      </Kicker>
      <Txt x={120} y={216} w={640} size={type.body} p={p("start", 26, 10)}>
        {T.aim}
      </Txt>
      <M x={120} y={330} t={`{\\color{${HOMEC}}(2p,\\,2q)}`} size={64} p={p("start", 26, 30)} />
      <Txt x={400} y={284} w={380} size={type.caption} italic c={color.ink2} p={p("first", 24)}>
        {T.firstBlue}
      </Txt>
      <M x={400} y={374} t="\gcd(p,q)=1" size={52} p={p("first", 26, 20)} />
      <Txt x={120} y={410} w={640} size={type.caption} italic c={color.ink2} p={only}>
        {r(T.firstLattice)}
      </Txt>
      <Txt x={120} y={522} w={640} size={type.body} p={onlyList}>
        {T.onlyList}
      </Txt>
      <M x={120} y={648} t={`(0,0),\\quad {\\color{${EDGE}}(p,q)},\\quad (2p,2q)`} size={54} p={onlyListM} />
      <Txt x={120} y={672} w={640} size={type.caption} italic c={color.ink2} p={mid}>
        {r(T.hangs)}
      </Txt>

      <div style={{ position: "absolute", left: 120, top: 752, width: 620, height: 2, background: color.rule, opacity: p("odd", 20) }} />
      {cases.map(([a, b, c, q], i) => (
        <Txt key={i} x={120} y={772 + i * 58} w={720} size={type.caption} p={q}>
          {r(a)} <span style={it}>{T.arrow} <span style={{ color: c }}>{r(b)}</span></span>
        </Txt>
      ))}
    </Sheet>
  );
};
