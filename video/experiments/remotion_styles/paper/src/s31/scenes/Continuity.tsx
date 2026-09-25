/** C4 — |sinθ| ≤ |θ| squeezes sinθ → 0; the product identity bounds the gap; sin, cos continuous. Debt 1 paid. */
import React from "react";
import { interpolate } from "remotion";
import { color, stroke, type } from "../../theme";
import { clamp } from "../../components/Type";
import { Kicker, Layer, Ledger, Ln, M, Sheet, Txt, camPath, useS } from "../kit";

const C = color.cobalt;
const X = 470;
const G = { x: 1610, y: 480, u: 90 };

export const Continuity: React.FC = () => {
  const { f, at, p } = useS();
  const cam = camPath(f, { cx: 960, cy: 500, s: 1.1 }, [
    [at("squeeze") + 20, { cx: 1100, cy: 420, s: 1.12 }, 60],
    [at("gap"), { cx: 1000, cy: 640, s: 1.2 }, 60],
    [at("cosgap"), { cx: 1000, cy: 720, s: 1.15 }, 40],
    [at("paid"), { cx: 960, cy: 540, s: 1 }, 50],
  ]);
  const plot = p("squeeze", 30);
  const th = interpolate(f, [at("squeeze") + 30, at("gap") - 20], [1.9, 0.02], { ...clamp, easing: (t) => 1 - Math.pow(1 - t, 2) });
  const gx = (v: number) => G.x + v * G.u;
  const gy = (v: number) => G.y - v * G.u;
  const path = (fn: (v: number) => number) => {
    let d = "";
    for (let i = 0; i <= 120; i++) {
      const v = -2.1 + (4.2 * i) / 120;
      d += `${i ? "L" : "M"}${gx(v).toFixed(1)} ${gy(fn(v)).toFixed(1)}`;
    }
    return d;
  };
  const band = (() => {
    let top = "";
    let bot = "";
    for (let i = 0; i <= 120; i++) {
      const v = -2.1 + (4.2 * i) / 120;
      top += `${i ? "L" : "M"}${gx(v).toFixed(1)} ${gy(Math.abs(v)).toFixed(1)}`;
      bot = `L${gx(v).toFixed(1)} ${gy(0).toFixed(1)}` + bot;
    }
    return top + bot + "Z";
  })();
  const paid = p("paid", 30, 10);
  return (
    <Sheet folio={117} title="Debt 1: continuity" cam={cam}>
      <Ledger x={120} y={330} st={{ show: 1 - p("squeeze", 30, 10) + p("paid", 30), items: [{ show: 1, paid, focus: 1 - paid }, { show: 1, paid: 0 }] }} />
      <Kicker x={X} y={140} p={p("start", 24)}>
        From the bonus
      </Kicker>
      <M x={X} y={270} size={66} p={p("start", 30, 6)} t="|\sin\theta|\ \le\ |\theta|" />
      <M x={X} y={400} size={50} p={p("squeeze", 30, 40)} t="0\ \le\ |\sin\theta|\ \le\ |\theta|\ \ \Longrightarrow\ \ \lim_{\theta\to0}\sin\theta=0" />

      {/* squeeze figure */}
      <Layer>
        <path d={band} fill={color.paperShade} opacity={plot * 0.9} />
        <Ln x1={gx(-2.2)} y1={G.y} x2={gx(2.2)} y2={G.y} p={plot} c={color.ink2} w={stroke.axis} />
        <path d={path(Math.abs)} fill="none" stroke={color.ink3} strokeWidth={2.6} opacity={plot} />
        <path d={path((v) => Math.abs(Math.sin(v)))} fill="none" stroke={color.ink} strokeWidth={stroke.curve} opacity={plot} />
        {plot > 0 && (
          <g opacity={interpolate(f, [at("squeeze") + 30, at("squeeze") + 44, at("gap") - 10, at("gap") + 10], [0, 1, 1, 0], clamp)}>
            <line x1={gx(th)} y1={G.y} x2={gx(th)} y2={gy(th)} stroke={color.accent} strokeWidth={3} />
            <circle cx={gx(th)} cy={gy(Math.abs(Math.sin(th)))} r={stroke.dot} fill={color.ink} stroke={color.paper} strokeWidth={stroke.ring} />
          </g>
        )}
      </Layer>
      <M x={gx(2.1) + 10} y={gy(2.1) + 10} size={40} c={color.ink2} p={plot} t="|\theta|" />
      <M x={gx(1.2)} y={gy(0.2)} size={36} bg p={plot} t="|\sin\theta|" />

      {/* the gap between two nearby values */}
      <Kicker x={X} y={470} p={p("gap", 24)}>
        Two nearby points
      </Kicker>
      <M x={X} y={600} size={56} p={p("gap", 34, 10)} t="|\sin x-\sin x_0|=2\,\Big|\cos\tfrac{x+x_0}{2}\Big|\,\Big|\sin\tfrac{x-x_0}{2}\Big|" />
      <M x={X + 320} y={700} size={56} p={p("gap", 30, 120)} t="\le\ 2\,\Big|\sin\tfrac{x-x_0}{2}\Big|" />
      <Txt x={X} y={668} w={300} size={type.caption} italic c={color.ink2} p={p("gap", 24, 130)}>
        since |cos| ≤ 1
      </Txt>
      <M x={X + 690} y={700} size={56} p={p("shrink", 30)} t={`\\le\\ |x-x_0|\\ \\xrightarrow{\\ x\\to x_0\\ }\\ {\\color{${color.accent}}0}`} />
      <M x={X + 320} y={810} size={60} p={p("shrink", 30, 70)} t="\lim_{x\to x_0}\sin x=\sin x_0" />
      <M x={X} y={960} size={52} p={p("cosgap", 30)} t={`|{\\color{${C}}\\cos x-\\cos x_0}|\\ \\le\\ 2\\,\\Big|\\sin\\tfrac{x-x_0}{2}\\Big|`} />
      <M x={X + 700} y={960} size={52} p={p("cosgap", 30, 20)} t={`\\Longrightarrow\\ \\lim_{x\\to x_0}{\\color{${C}}\\cos x}={\\color{${C}}\\cos x_0}`} />
    </Sheet>
  );
};
