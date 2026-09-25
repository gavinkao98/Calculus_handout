/** C13 — the four-step derivative cycle; e^x returns in one step, sin/cos flip sign in two. */
import React from "react";
import { color } from "../../theme";
import { Arrow, Kicker, Layer, M, Sheet, Txt, camPath, useS } from "../kit";

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

export const Cycle: React.FC = () => {
  const { f, at, p, atWord } = useS();
  const steps = ["step1", "step2", "step3", "step4"];
  // the camera settles as the narration lands on the payoff word of each beat
  const step4At = atWord("home", { afterFrame: at("step4") }) ?? at("step4", 0.5);
  const compareBackAt = atWord("spring law", { afterFrame: at("compare") }) ?? at("compare", 0.7);
  const cam = camPath(f, { cx: 760, cy: 560, s: 1.45 }, [
    [step4At, { cx: 900, cy: 560, s: 1.1 }, 60],
    [at("compare"), { cx: 1100, cy: 560, s: 1.05 }, 60],
    [compareBackAt, { cx: 960, cy: 540, s: 1 }, 60],
  ]);
  const half = p("compare", 40, 170);
  return (
    <Sheet folio={125} title="The derivative cycle" cam={cam}>
      <Kicker x={470} y={140} p={p("start", 24)}>
        Differentiate again, and again
      </Kicker>
      <Layer>
        {/* four arcs, clockwise, each one derivative */}
        {nodes.map((nd, i) => {
          const q = i === 0 ? p("step1", 26) : p(steps[i], 26);
          const a0 = nd.a + 0.33;
          const a1 = nd.a + Math.PI / 2 - 0.33;
          const s0 = pos(a0);
          const s1 = pos(a1);
          return <Arrow key={i} x1={s0.x} y1={s0.y} x2={s1.x} y2={s1.y} p={q} c={A} w={3} head={16} bend={-R * 0.41} />;
        })}
        {/* the half turn: two steps give the negative */}
        {half > 0 && (
          <path
            d={`M${O.x} ${O.y - R - 78} A${R + 78} ${R + 78} 0 0 1 ${O.x} ${O.y + R + 78}`}
            fill="none"
            stroke={color.ochre}
            strokeWidth={6}
            strokeLinecap="round"
            strokeDasharray={`${Math.PI * (R + 78) * half} 9999`}
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
      {nodes.map((nd, i) => {
        const q = i === 0 ? p("start", 26, 10) : p(steps[i - 1], 26, 10);
        const pt = pos(nd.a);
        return <M key={i} x={pt.x} y={pt.y + 22} align="center" size={70} c={nd.c} p={q} bg t={nd.t} />;
      })}
      {nodes.map((nd, i) => {
        const mid = pos(nd.a + Math.PI / 4, R - 64);
        return <M key={`d${i}`} x={mid.x} y={mid.y + 14} align="center" size={40} c={A} p={p(steps[i], 20, 14)} t="\tfrac{d}{dx}" />;
      })}
      <M x={O.x} y={O.y + 20} align="center" size={50} p={p("step4", 30, 60)} t={`\\frac{d^4}{dx^4}\\sin x=\\sin x`} />
      <Txt x={O.x} y={O.y + 44} w={400} align="center" size={30} italic c={color.ink2} p={p("step4", 26, 90)}>
        four steps, and home
      </Txt>

      {/* compare */}
      <M x={1455} y={470} align="center" size={72} p={p("compare", 26)} t="e^x" />
      <Txt x={1560} y={420} w={260} size={34} italic c={color.ink2} p={p("compare", 26, 20)}>
        one step back to itself
      </Txt>
      <M x={1240} y={650} size={52} c={color.ochre} p={half} t={`\\frac{d^2}{dx^2}\\sin x=-\\sin x`} />
      <Txt x={1240} y={690} w={560} size={32} italic c={color.ink2} p={p("compare", 26, 200)}>
        half a turn: two steps give the negative — the spring law <span style={{ fontStyle: "normal", color: A }}>s″ = −s</span>
      </Txt>
    </Sheet>
  );
};
