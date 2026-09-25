/** C6 — two cautions: a limit, not an identity; radians only (degrees bring π/180). */
import React from "react";
import { color, stroke, type } from "../../theme";
import { Kicker, Layer, Ln, M, Sheet, Txt, useS } from "../kit";

const PI = Math.PI;
const A = color.accent;
const G = { x: 520, y: 640, ux: 165, uy: 290 };
const gx = (v: number) => G.x + v * G.ux;
const gy = (v: number) => G.y - v * G.uy;
const sinc = (v: number) => (Math.abs(v) < 1e-6 ? 1 : Math.sin(v) / v);

export const Warnings: React.FC = () => {
  const { at, p } = useS();
  // two columns, camera locked. Focus moves by dimming: once caution 2 starts, caution 1 recedes.
  const recede = 1 - 0.5 * p("degrees", 30);
  const id = p("identity", 30);
  const cur = p("identity", 44, 20);
  const d1 = p("identity", 24, 80);
  const d2 = p("identity", 24, Math.round((at("degrees") - at("identity")) * 0.5));
  const curve = (() => {
    let d = "";
    const n = Math.max(2, Math.ceil(160 * cur));
    for (let i = 0; i <= n; i++) {
      const v = 0.001 + (PI + 0.25) * cur * (i / n);
      d += `${i ? "L" : "M"}${gx(v).toFixed(1)} ${gy(sinc(v)).toFixed(1)}`;
    }
    return d;
  })();
  const R = 150;
  const S = { x: 1560, y: 470 };
  const th = 0.85;
  return (
    <Sheet folio={119} title="Two cautions">
      <Layer>
        <Ln x1={1130} y1={170} x2={1130} y2={960} p={p("start", 30)} c={color.rule} />
      </Layer>
      {/* caution 1 */}
      <div style={{ opacity: recede }}>
      <Kicker x={470} y={140} p={p("start", 24, 4)}>
        Caution 1
      </Kicker>
      <Txt x={470} y={190} w={640} size={50} p={p("start", 26, 12)}>
        A limit, not an identity
      </Txt>
      <Layer>
        <Ln x1={G.x} y1={G.y} x2={gx(PI + 0.35)} y2={G.y} p={id} c={color.ink2} w={stroke.axis} />
        <Ln x1={G.x} y1={G.y + 10} x2={G.x} y2={gy(1.1)} p={id} c={color.ink2} w={stroke.axis} />
        <Ln x1={G.x} y1={gy(1)} x2={gx(PI + 0.3)} y2={gy(1)} p={id} c={color.rule} w={1.6} dash="4 8" />
        {cur > 0 && <path d={curve} fill="none" stroke={color.ink} strokeWidth={stroke.curve} strokeLinecap="round" />}
        <circle cx={G.x} cy={gy(1)} r={8} fill={color.paper} stroke={color.ink} strokeWidth={3} opacity={cur > 0 ? 1 : 0} />
        <g opacity={d1}>
          <line x1={gx(PI / 2)} y1={G.y} x2={gx(PI / 2)} y2={gy(2 / PI)} stroke={A} strokeWidth={3.4} />
          <circle cx={gx(PI / 2)} cy={gy(2 / PI)} r={stroke.dot} fill={color.ink} stroke={color.paper} strokeWidth={stroke.ring} />
        </g>
        <g opacity={d2}>
          <circle cx={gx(PI)} cy={G.y} r={stroke.dot} fill={A} stroke={color.paper} strokeWidth={stroke.ring} />
        </g>
      </Layer>
      <M x={G.x - 14} y={gy(1) + 12} t="1" size={type.label} align="right" c={color.ink2} p={id} />
      <M x={gx(PI / 2)} y={G.y + 50} t="\pi/2" display={false} size={type.label} align="center" c={color.ink2} p={id} />
      <M x={gx(PI)} y={G.y + 50} t="\pi" size={type.label} align="center" c={color.ink2} p={id} />
      <M x={gx(PI / 2) + 18} y={gy(2 / PI) - 20} t="2/\pi\approx0.64" display={false} size={40} bg p={d1} />
      <M x={470} y={800} size={50} p={d1} t={`\\frac{\\sin(\\pi/2)}{\\pi/2}=\\frac{2}{\\pi}\\approx{\\color{${A}}0.64}`} />
      <M x={470} y={930} size={50} p={d2} t={`\\frac{\\sin\\pi}{\\pi}={\\color{${A}}0}`} />
      <Txt x={760} y={884} w={360} size={type.caption} italic c={color.ink2} p={p("identity", 24, Math.round((at("degrees") - at("identity")) * 0.72))}>
        Only near 0 is the ratio close to 1.
      </Txt>
      </div>

      {/* caution 2 */}
      <Kicker x={1190} y={140} p={p("degrees", 24)}>
        Caution 2
      </Kicker>
      <Txt x={1190} y={190} w={620} size={50} p={p("degrees", 26, 8)}>
        Radians are not optional
      </Txt>
      <Layer>
        <g opacity={p("degrees", 30, 20)}>
          <path d={`M${S.x} ${S.y} L${S.x + R} ${S.y} A${R} ${R} 0 0 0 ${S.x + R * Math.cos(th)} ${S.y - R * Math.sin(th)} Z`} fill={color.paperShade} stroke={color.ink} strokeWidth={2.4} />
          <path d={`M${S.x + R} ${S.y} A${R} ${R} 0 0 0 ${S.x + R * Math.cos(th)} ${S.y - R * Math.sin(th)}`} fill="none" stroke={color.ochre} strokeWidth={6} />
        </g>
      </Layer>
      <M x={S.x + R + 14} y={S.y - 50} t="\theta" size={44} c={color.ochre} p={p("degrees", 30, 20)} />
      <M x={1190} y={380} size={52} p={p("degrees", 30, 30)} t={`\\text{sector area}=\\frac12\\,{\\color{${color.ochre}}\\theta}`} />
      <Txt x={1190} y={410} w={330} size={type.caption} italic c={color.ink2} p={p("degrees", 24, 60)}>
        holds only when θ is the arc length — radians
      </Txt>
      <M x={1190} y={640} size={52} p={p("factor", 30)} t={`\\lim_{x\\to0}\\frac{\\sin(x^\\circ)}{x}={\\color{${A}}\\frac{\\pi}{180}}`} />
      <Txt x={1190} y={690} w={600} size={type.caption} italic c={color.ink2} p={p("factor", 24, 50)}>
        and the factor follows you into the derivative:
      </Txt>
      <M x={1190} y={830} size={56} p={p("factor", 34, 90)} t={`\\frac{d}{dx}\\sin(x^\\circ)={\\color{${A}}\\frac{\\pi}{180}}\\cos(x^\\circ)`} />
    </Sheet>
  );
};
