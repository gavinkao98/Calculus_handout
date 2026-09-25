/** C5 — sinθ/θ trapped between cosθ and 1; both go to 1; squeeze. Debt 2 paid. */
import React from "react";
import { interpolate } from "remotion";
import { color, stroke, type } from "../../theme";
import { clamp } from "../../components/Type";
import { Kicker, Layer, Ledger, Ln, M, Sheet, Txt, camPath, useS } from "../kit";

const PI = Math.PI;
const G = { x: 1130, y: 720, ux: 205, uy: 300 };
const gx = (v: number) => G.x + v * G.ux;
const gy = (v: number) => G.y - v * G.uy;
const sinc = (v: number) => (Math.abs(v) < 1e-6 ? 1 : Math.sin(v) / v);
const path = (fn: (v: number) => number, a: number, b: number, n = 200) => {
  let d = "";
  for (let i = 0; i <= n; i++) {
    const v = a + ((b - a) * i) / n;
    d += `${i ? "L" : "M"}${gx(v).toFixed(1)} ${gy(fn(v)).toFixed(1)}`;
  }
  return d;
};

export const Limit: React.FC = () => {
  const { f, at, p } = useS();
  const cam = camPath(f, { cx: 1100, cy: 560, s: 1.1 }, [
    [at("pinch") + 10, { cx: 1130, cy: 480, s: 2.3 }, 70],
    [at("value"), { cx: 1000, cy: 540, s: 1.02 }, 60],
    [at("paid"), { cx: 960, cy: 540, s: 1 }, 40],
  ]);
  const ax = p("start", 30, 4);
  const cur = p("start", 50, 30);
  const one = p("bounds", 30);
  const cosP = p("bounds", 44, 50);
  const band = p("bounds", 30, 90);
  const th = interpolate(f, [at("pinch") + 50, at("value") - 20], [1.35, 0.06], { ...clamp, easing: (t) => 1 - Math.pow(1 - t, 2.2) });
  const mark = interpolate(f, [at("pinch") + 40, at("pinch") + 56, at("value") + 10, at("value") + 30], [0, 1, 1, 0], clamp);
  const bandPath = (() => {
    const d = path(() => 1, -PI / 2, PI / 2, 2);
    let back = "";
    for (let i = 0; i <= 200; i++) {
      const v = PI / 2 - (PI * i) / 200;
      back += `L${gx(v).toFixed(1)} ${gy(Math.cos(v)).toFixed(1)}`;
    }
    return d + back + "Z";
  })();
  const val = p("value", 34);
  const paid = p("paid", 30, 20);
  return (
    <Sheet folio={118} title="Debt 2: the key limit" cam={cam}>
      <Kicker x={470} y={140} p={p("start", 24)}>
        The squeeze
      </Kicker>
      <Layer>
        <defs>
          <clipPath id="limclip">
            <rect x={400} y={200} width={1450} height={700} />
          </clipPath>
        </defs>
        <g clipPath="url(#limclip)">
          <path d={bandPath} fill={color.paperShade} opacity={band} />
          <Ln x1={gx(-PI) - 20} y1={G.y} x2={gx(PI) + 20} y2={G.y} p={ax} c={color.ink2} w={stroke.axis} />
          <Ln x1={G.x} y1={gy(-0.55)} x2={G.x} y2={gy(1.25)} p={ax} c={color.ink2} w={stroke.axis} />
          {one > 0 && <path d={path(() => 1, -PI, -PI + 2 * PI * one, 2)} fill="none" stroke={color.ink2} strokeWidth={2.6} />}
          {cosP > 0 && <path d={path(Math.cos, -PI, -PI + 2 * PI * cosP)} fill="none" stroke={color.cobalt} strokeWidth={stroke.curve} strokeLinecap="round" />}
          {cur > 0 && <path d={path(sinc, -PI, -PI + 2 * PI * cur)} fill="none" stroke={color.ink} strokeWidth={stroke.curve + 0.6} strokeLinecap="round" />}
          {/* the pinch: at ±θ the ratio sits between cos θ and 1 */}
          {[th, -th].map((v, i) => (
            <g key={i} opacity={mark}>
              <line x1={gx(v)} y1={gy(Math.cos(v))} x2={gx(v)} y2={gy(1)} stroke={color.accent} strokeWidth={3.2} />
              <circle cx={gx(v)} cy={gy(sinc(v))} r={stroke.dot * 0.8} fill={color.ink} stroke={color.paper} strokeWidth={stroke.ring} />
            </g>
          ))}
        </g>
        {/* the hole at θ = 0: the ratio is undefined there */}
        {cur > 0.5 && <circle cx={G.x} cy={gy(1)} r={9} fill={color.paper} stroke={color.ink} strokeWidth={3} />}
        {val > 0 && <circle cx={G.x} cy={gy(1)} r={9 + 14 * val} fill="none" stroke={color.accent} strokeWidth={3} opacity={val} />}
        {[-PI, PI].map((v) => (
          <line key={v} x1={gx(v)} y1={G.y} x2={gx(v)} y2={G.y + 10} stroke={color.ink2} strokeWidth={stroke.axis} opacity={ax} />
        ))}
      </Layer>
      <M x={gx(-PI)} y={G.y + 52} t="-\pi" size={type.label} align="center" c={color.ink2} p={ax} />
      <M x={gx(PI)} y={G.y + 52} t="\pi" size={type.label} align="center" c={color.ink2} p={ax} />
      <M x={G.x + 14} y={G.y + 44} t="0" size={type.label} c={color.ink2} p={ax} />
      <M x={gx(2.3)} y={gy(sinc(2.3)) - 44} t="y=\frac{\sin\theta}{\theta}" size={46} bg p={cur} />
      <M x={gx(PI) - 6} y={gy(1) - 18} t="y=1" size={42} align="right" c={color.ink2} p={one} />
      <M x={gx(-1.8) - 14} y={gy(Math.cos(1.8)) + 14} t="y=\cos\theta" size={42} align="right" c={color.cobalt} bg p={cosP} />
      <Txt x={G.x + 24} y={gy(1) - 58} w={260} size={30} italic c={color.accent} p={mark} o={mark}>
        trapped
      </Txt>

      {/* the verdict */}
      <M x={1130} y={300} align="center" size={84} p={val} t={`\\lim_{\\theta\\to0}\\frac{\\sin\\theta}{\\theta}={\\color{${color.accent}}1}`} />
      <Txt x={1130} y={880} w={900} align="center" size={type.caption} italic c={color.ink2} p={p("value", 26, 50)}>
        cos θ → 1 because cosine is continuous — the debt we paid first
      </Txt>
      <Ledger x={120} y={330} st={{ show: p("paid", 24), items: [{ show: 1, paid: 1 }, { show: 1, paid, focus: 1 - paid }] }} />
    </Sheet>
  );
};
