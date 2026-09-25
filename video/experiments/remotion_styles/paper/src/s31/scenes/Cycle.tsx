/** C13 — the four-step derivative cycle; e^x returns in one step, sin/cos flip sign in two. */
import React from "react";
import { color } from "../../theme";
import { Arrow, Kicker, Layer, M, Mark, Sheet, Txt, Pt, arcPts, arrowMarks, mLbl, tLbl, useS } from "../kit";

const A = color.accent;
const C = color.cobalt;
const O = { x: 760, y: 600 };
const R = 280;
// top, right, bottom, left (clockwise = one derivative per step)
const nodes = [
  { t: "\\sin x", c: color.ink, a: -Math.PI / 2 },
  { t: "\\cos x", c: C, a: 0 },
  { t: "-\\sin x", c: color.ink, a: Math.PI / 2 },
  { t: "-\\cos x", c: C, a: Math.PI },
];
const pos = (a: number, r = R) => ({ x: O.x + r * Math.cos(a), y: O.y + r * Math.sin(a) });
// arrows stop short of the node labels: further at the wide top/bottom labels than at the sides
const GAP_V = 0.5; // rad, at sin x / −sin x
const GAP_H = 0.33; // rad, at cos x / −cos x
const arrowEnds = (i: number) => {
  const a = nodes[i].a;
  const vertical = i % 2 === 0; // arrow i leaves node i (top/bottom for even i)
  const s0 = pos(a + (vertical ? GAP_V : GAP_H));
  const s1 = pos(a + Math.PI / 2 - (vertical ? GAP_H : GAP_V));
  return { s0, s1 };
};
const BEND = -R * 0.3;
const RH = R + 100; // the half-turn arc runs outside the right node's label

export const Cycle: React.FC = () => {
  const { at, p, pf, atWord, guard } = useS();
  const steps = ["step1", "step2", "step3", "step4"];
  // captions ink as the narration lands on their payoff word
  const step4At = atWord("home", { afterFrame: at("step4") }) ?? at("step4") + 90;
  const compareBackAt = atWord("spring law", { afterFrame: at("compare") }) ?? at("compare") + 200;
  // camera locked on the full page (a push-in here would clip the running head); the e^x
  // comparison fills the right half when its beat arrives.
  const half = p("compare", 40, 170);

  const nodeL = nodes.map((nd, i) => {
    const pt = pos(nd.a);
    return { x: pt.x, y: pt.y + 22, align: "center" as const, size: 70, c: nd.c, p: i === 0 ? p("start", 26, 10) : p(steps[i - 1], 26, 10), t: nd.t };
  });
  const dL = nodes.map((nd, i) => {
    const mid = pos(nd.a + Math.PI / 4, R - 64);
    return { x: mid.x, y: mid.y + 14, align: "center" as const, size: 46, c: A, p: p(steps[i], 20, 14), display: false, t: "\\frac{d}{dx}" };
  });
  const fourL = { x: O.x, y: O.y + 20, align: "center" as const, size: 50, p: p("step4", 30, 60), t: "\\frac{d^4}{dx^4}\\sin x=\\sin x" };
  const expL = { x: 1455, y: 470, align: "center" as const, size: 72, p: p("compare", 26), t: "e^x" };
  const d2L = { x: 1240, y: 650, size: 52, c: color.ochre, p: half, t: "\\frac{d^2}{dx^2}\\sin x=-\\sin x" };
  const loop: Pt[] = Array.from({ length: 41 }, (_, k) => {
    const t = k / 40;
    const b = (a: number, b1: number, c: number, d: number) => (1 - t) ** 3 * a + 3 * (1 - t) ** 2 * t * b1 + 3 * (1 - t) * t * t * c + t ** 3 * d;
    return [b(1428, 1370, 1540, 1482), b(392, 260, 260, 386)];
  });
  const marks: Mark[] = [
    ...nodes.flatMap((_, i) => {
      const { s0, s1 } = arrowEnds(i);
      return arrowMarks(`arrow ${i + 1}`, s0.x, s0.y, s1.x, s1.y, { bend: BEND, head: 16, on: (i === 0 ? p("step1", 26) : p(steps[i], 26)) > 0 });
    }),
    { name: "half-turn arc", pts: arcPts(O.x, O.y, RH, Math.PI / 2, -Math.PI / 2, 96), w: 6, on: half > 0 },
    { name: "e^x loop", pts: loop, w: 3, on: p("compare", 20) > 0 },
    ...arrowMarks("e^x loop head", 1488, 366, 1482, 388, { head: 14, on: p("compare", 10, 40) > 0 }),
  ];
  guard(marks, [
    ...[...nodeL, ...dL].map((q, i) => mLbl(q, `${q.t} #${i}`)),
    mLbl(fourL),
    mLbl(expL),
    mLbl(d2L),
    tLbl("four steps, and home", O.x, O.y + 66, 30, pf(Math.min(step4At - 14, at("compare") - 70), 26), 1, { italic: true, align: "center" }),
  ]);
  return (
    <Sheet folio={125} title="The derivative cycle">
      <Kicker x={470} y={140} p={p("start", 24)}>
        Differentiate again, and again
      </Kicker>
      <Layer>
        {/* four arcs, clockwise, each one derivative */}
        {nodes.map((nd, i) => {
          const q = i === 0 ? p("step1", 26) : p(steps[i], 26);
          const { s0, s1 } = arrowEnds(i);
          return <Arrow key={i} x1={s0.x} y1={s0.y} x2={s1.x} y2={s1.y} p={q} c={A} w={3} head={16} bend={BEND} />;
        })}
        {/* the half turn: two steps give the negative */}
        {half > 0 && (
          <path
            d={`M${O.x} ${O.y - RH} A${RH} ${RH} 0 0 1 ${O.x} ${O.y + RH}`}
            fill="none"
            stroke={color.ochre}
            strokeWidth={6}
            strokeLinecap="round"
            strokeDasharray={`${Math.PI * RH * half} 9999`}
            opacity={0.9}
          />
        )}
        {/* e^x: a one-step loop */}
        {p("compare", 20) > 0 && (
          <g opacity={p("compare", 20)}>
            <path d="M1428 392 C 1370 260, 1540 260, 1482 386" fill="none" stroke={A} strokeWidth={3} strokeDasharray={`${330 * p("compare", 30, 10)} 999`} />
            <Arrow x1={1488} y1={366} x2={1482} y2={388} p={p("compare", 10, 40)} c={A} w={3} head={14} />
          </g>
        )}
      </Layer>
      {[...nodeL, ...dL, fourL].map((q, i) => (
        <M key={i} {...q} />
      ))}
      <Txt x={O.x} y={O.y + 66} w={400} align="center" size={30} italic c={color.ink2} p={pf(Math.min(step4At - 14, at("compare") - 70), 26)}>
        four steps, and home
      </Txt>

      {/* compare */}
      <M {...expL} />
      <Txt x={1560} y={420} w={260} size={34} italic c={color.ink2} p={p("compare", 26, 20)}>
        one step back to itself
      </Txt>
      <M {...d2L} />
      <Txt x={1240} y={690} w={560} size={32} italic c={color.ink2} p={pf(compareBackAt - 20, 26)}>
        half a turn: two steps give the negative — the spring law <span style={{ fontStyle: "normal", color: A }}>s″ = −s</span>
      </Txt>
    </Sheet>
  );
};
