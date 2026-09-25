/** C3 — three nested shapes on the unit circle → sinθ ≤ θ ≤ tanθ → cosθ ≤ sinθ/θ ≤ 1. */
import React from "react";
import { Easing, interpolate } from "remotion";
import { color, stroke, type } from "../../theme";
import { clamp } from "../../components/Type";
import { EqNumber } from "../../components/Marginalia";
import { Hatches, Kicker, Layer, Ln, M, Sheet, Txt, camPath, useS } from "../kit";

const PI = Math.PI;
const O = { x: 210, y: 930 };
const R = 640;
const TH = 0.78;
const H = 1330;
const X = 1110; // right column

const Swatch: React.FC<{ y: number; fill: string; p: number }> = ({ y, fill, p }) =>
  p <= 0 ? null : <rect x={X} y={y - 34} width={44} height={34} fill={fill} stroke={color.ink} strokeWidth={1.6} opacity={p} />;

export const Areas: React.FC = () => {
  const { f, at, p } = useS();
  const th = interpolate(f, [20, at("points") - 10], [0.3, TH], { ...clamp, easing: Easing.inOut(Easing.cubic) });
  const c = Math.cos(th);
  const s = Math.sin(th);
  const t = Math.tan(th);
  const A = { x: O.x + R, y: O.y };
  const B = { x: O.x + R * c, y: O.y - R * s };
  const C = { x: O.x + R, y: O.y - R * t };

  const axes = p("start", 30, 4);
  const arcP = p("start", 44, 10);
  const pts = p("points", 24);
  const tan = p("points", 30, 60);
  const t1 = p("tri1", 30);
  const sc = p("sector", 30);
  const t2 = p("tri2", 30);
  const focus = (id: string) => interpolate(f, [at(id), at(id) + 14], [0, 1], clamp);
  // the shape being talked about is full strength; the others recede once all three are down
  const dimOthers = p("chain", 30);

  const cam = camPath(f, { cx: 620, cy: 640, s: 1.35 }, [
    [at("points") + 40, { cx: 700, cy: 560, s: 1.2 }, 50],
    [at("tri1"), { cx: 980, cy: 520, s: 1.05 }, 60],
    [at("chain"), { cx: 1420, cy: 640, s: 1.4 }, 60],
    [at("divide", 0.45), { cx: 1400, cy: 800, s: 1.3 }, 50],
    [at("even"), { cx: 960, cy: 820, s: 1.05 }, 60],
    [at("bonus"), { cx: 960, cy: 790, s: 1 }, 60],
  ]);

  const sector = `M${O.x} ${O.y} L${A.x} ${A.y} A${R} ${R} 0 0 0 ${B.x} ${B.y} Z`;
  const triB = `M${O.x} ${O.y} L${A.x} ${A.y} L${B.x} ${B.y} Z`;
  const triC = `M${O.x} ${O.y} L${A.x} ${A.y} L${C.x} ${C.y} Z`;
  const outline = (d: string, q: number, w = 2.6) => (q > 0 ? <path d={d} fill="none" stroke={color.ink} strokeWidth={w} strokeLinejoin="round" opacity={q} /> : null);

  return (
    <Sheet folio={116} title="Paying the debts: areas" cam={cam} h={H}>
      <Layer h={H}>
        <Hatches />
        {/* fills, largest first */}
        {t2 > 0 && <path d={triC} fill="url(#h135)" opacity={t2 * (1 - 0.3 * dimOthers)} />}
        {sc > 0 && <path d={sector} fill="url(#dots)" opacity={sc} />}
        {t1 > 0 && <path d={triB} fill="url(#h45)" opacity={t1} />}
        {/* axes */}
        <Ln x1={O.x - 40} y1={O.y} x2={O.x + R + 150} y2={O.y} p={axes} c={color.ink2} w={stroke.axis} />
        <Ln x1={O.x} y1={O.y + 40} x2={O.x} y2={O.y - R - 60} p={axes} c={color.ink2} w={stroke.axis} />
        {/* quarter circle */}
        <path
          d={`M${A.x} ${A.y} A${R} ${R} 0 0 0 ${O.x} ${O.y - R}`}
          fill="none"
          stroke={color.ink}
          strokeWidth={3.4}
          strokeDasharray={`${(PI / 2) * R * arcP} 9999`}
        />
        {/* tangent line x = 1 */}
        <Ln x1={A.x} y1={O.y + 30} x2={A.x} y2={O.y - R * 1.12} p={tan} c={color.ink3} w={2} dash="2 8" />
        {/* shape outlines */}
        {outline(triC, t2 * focus("tri2"), 3)}
        {outline(sector, sc * focus("sector") * (1 - t2 * 0.6), 3)}
        {outline(triB, t1 * (1 - sc * 0.6), 3)}
        {/* radius to B and the angle */}
        <Ln x1={O.x} y1={O.y} x2={B.x} y2={B.y} p={arcP} c={color.ink} w={2.6} />
        <path
          d={`M${O.x + 110} ${O.y} A110 110 0 0 0 ${O.x + 110 * c} ${O.y - 110 * s}`}
          fill="none"
          stroke={color.ochre}
          strokeWidth={4}
          opacity={arcP}
        />
        {/* sin θ height (plumb from B) during tri1 */}
        <Ln x1={B.x} y1={O.y} x2={B.x} y2={B.y} p={t1} c={color.ink} w={2} dash="3 7" />
        {[
          [O, 1],
          [A, pts],
          [B, pts],
          [C, pts],
        ].map(([q, o], i) => (
          <circle key={i} cx={(q as typeof O).x} cy={(q as typeof O).y} r={stroke.dot} fill={color.ink} stroke={color.paper} strokeWidth={stroke.ring} opacity={(o as number) * (i === 0 ? axes : 1)} />
        ))}
      </Layer>

      {/* figure labels */}
      <M x={O.x + 150} y={O.y - 30} t="\theta" size={50} c={color.ochre} p={arcP} />
      <M x={O.x - 22} y={O.y + 50} t="O" size={46} align="right" p={axes} />
      <M x={A.x + 18} y={A.y + 52} t="A=(1,0)" size={44} p={pts} />
      <M x={B.x - 44} y={B.y + 8} t="B=(\cos\theta,\sin\theta)" size={44} align="right" p={pts} />
      <M x={C.x - 22} y={C.y + 10} t="C=(1,\tan\theta)" size={44} align="right" p={pts} />
      <M x={B.x + 14} y={(B.y + O.y) / 2 + 40} t="\sin\theta" size={40} c={color.ink2} bg p={t1} o={1 - dimOthers} />
      <M x={A.x + 18} y={(C.y + O.y) / 2} t="\tan\theta" size={40} c={color.ink2} bg p={t2} o={1 - dimOthers} />
      <Txt x={O.x + R * 0.45} y={O.y + 20} w={200} size={type.label} italic c={color.ink2} p={t1} o={1 - dimOthers}>
        base 1
      </Txt>

      {/* right column: the three areas */}
      <Kicker x={X} y={150} p={p("tri1", 20)}>
        Three nested areas
      </Kicker>
      <Layer h={H}>
        <Swatch y={290} fill="url(#h45)" p={t1} />
        <Swatch y={390} fill="url(#dots)" p={sc} />
        <Swatch y={490} fill="url(#h135)" p={t2} />
      </Layer>
      <M x={X + 70} y={290} size={52} p={t1} t="\triangle OAB:\ \ \tfrac12\cdot1\cdot\sin\theta" />
      <M x={X + 70} y={390} size={52} p={sc} t={`\\text{sector}\\ OAB:\\ \\ \\tfrac12\\,{\\color{${color.ochre}}\\theta}`} />
      <Txt x={X + 450} y={352} w={320} size={type.caption} italic c={color.ochre} p={p("sector", 24, 40)}>
        true in radians
      </Txt>
      <M x={X + 70} y={490} size={52} p={t2} t="\triangle OAC:\ \ \tfrac12\cdot1\cdot\tan\theta" />

      {/* the chain */}
      <M x={X} y={640} size={60} p={p("chain", 30)} t="\tfrac12\sin\theta\ \le\ \tfrac12\theta\ \le\ \tfrac12\tan\theta" />
      <Txt x={X} y={680} w={100} size={type.caption} italic c={color.accent} p={p("chain", 20, 70)}>
        × 2
      </Txt>
      <M x={X + 90} y={740} size={66} p={p("chain", 30, 70)} t="\sin\theta\ \le\ \theta\ \le\ \tan\theta" />
      <Txt x={X} y={790} w={600} size={type.caption} italic c={color.ink2} p={p("divide", 20)}>
        divide by sin θ, then take reciprocals:
      </Txt>
      <M x={X + 90} y={920} size={60} p={p("divide", 30, 20)} t="1\ \le\ \frac{\theta}{\sin\theta}\ \le\ \frac{1}{\cos\theta}" />
      {/* the result, boxed */}
      <Layer h={H}>
        <rect x={X - 10} y={975} width={640} height={170} fill="none" stroke={color.accent} strokeWidth={2.4} opacity={p("divide", 24, 110)} />
      </Layer>
      <M x={X + 30} y={1085} size={74} p={p("divide", 34, 90)} t="\cos\theta\ \le\ \frac{\sin\theta}{\theta}\ \le\ 1" />
      <EqNumber y={1040} n="1" opacity={p("divide", 24, 120)} />

      {/* even + bonus */}
      <Kicker x={160} y={1030} p={p("even", 24)}>
        Negative θ
      </Kicker>
      <M x={160} y={1160} size={54} p={p("even", 30, 16)} t="\frac{\sin(-\theta)}{-\theta}=\frac{-\sin\theta}{-\theta}=\frac{\sin\theta}{\theta}" />
      <Txt x={160} y={1200} w={700} size={type.caption} italic c={color.ink2} p={p("even", 24, 40)}>
        an even function: the same bounds hold on both sides
      </Txt>
      <Kicker x={X} y={1180} p={p("bonus", 24)}>
        Bonus
      </Kicker>
      <M x={X + 190} y={1235} size={62} p={p("bonus", 30, 10)} t="|\sin\theta|\ \le\ |\theta|" />
    </Sheet>
  );
};
