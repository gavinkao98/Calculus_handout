/** C9 — the slope of sin at x equals the height of cos at x; the circle from the cold open agrees. */
import React from "react";
import { Easing, interpolate } from "remotion";
import { color, semantic, stroke, type } from "../../theme";
import { clamp } from "../../components/Type";
import { Curve, Dot, PlotFrame, RangeAxes, SlopeTriangle, Tangent, TangentNote, Tick, px } from "../../components/Plot";
import { FigureCaption } from "../../components/Marginalia";
import { Arrow, Layer, M, Sheet, Txt, camPath, useS, wipe } from "../kit";

const PI = Math.PI;
const A: PlotFrame = { ox: 520, oy: 340, ux: 170, uy: 150 };
const B: PlotFrame = { ox: 520, oy: 790, ux: 170, uy: 150 };
const tick = (v: number, t: string): Tick => ({ v, label: [{ key: "t", tex: t }] });
const xT = [tick(PI / 2, "\\pi/2"), tick(PI, "\\pi"), tick((3 * PI) / 2, "3\\pi/2"), tick(2 * PI, "2\\pi")];
const yT = [tick(1, "1"), tick(-1, "{-}1")];
const fmt = (m: number) => (Math.abs(m) < 0.005 ? "0.00" : m < 0 ? `−${Math.abs(m).toFixed(2)}` : m.toFixed(2));

export const Slope: React.FC = () => {
  const { f, at, p, sp, dur } = useS();
  const x = interpolate(
    f,
    [at("tangent") + 16, at("match"), at("peak"), at("peak") + 40, at("circle"), dur - 20],
    [0.15, 0.9, 1.3, PI / 2, PI / 2, 2 * PI - 0.35],
    { ...clamp, easing: Easing.inOut(Easing.sin) },
  );
  const m = Math.cos(x);
  const y = Math.sin(x);
  const cam = camPath(f, { cx: 1000, cy: 360, s: 1.35 }, [
    [at("cosine") - 10, { cx: 1000, cy: 560, s: 1.05 }, 50],
    [at("peak"), { cx: 1020, cy: 560, s: 1.2 }, 40],
    [at("circle"), { cx: 960, cy: 540, s: 1 }, 50],
  ]);
  const axA = p("start", 30);
  const sinP = p("start", 50, 20);
  const grow = sp("tangent", 6);
  const note = p("tangent", 20, 20);
  const axB = p("cosine", 24);
  const cosP = p("cosine", 40, 6);
  const match = p("match", 26);
  const peak = interpolate(f, [at("peak") + 30, at("peak") + 46, at("circle") + 10, at("circle") + 30], [0, 1, 1, 0], clamp);
  const circ = p("circle", 30);
  const [bx, by0] = px(B, x, 0);
  const [, qy] = px(B, x, m);
  const [ax, ay] = px(A, x, y);
  // inset circle (margin): the same angle, the unit velocity, its vertical part = cos x
  const O = { x: 260, y: 640 };
  const R = 105;
  const P = { x: O.x + R * Math.cos(x), y: O.y - R * Math.sin(x) };
  const V = { x: -R * Math.sin(x), y: -R * Math.cos(x) };
  return (
    <Sheet folio={121} title="Slope equals height" cam={cam}>
      <Layer>
        <defs>
          <clipPath id="slclip">
            <rect x={440} y={120} width={1400} height={420} />
          </clipPath>
        </defs>
        {/* plumb line joining the two panels at x */}
        <line x1={ax} y1={ay + 12} x2={bx} y2={qy - 12} stroke={color.ink3} strokeWidth={1.5} strokeDasharray="1.5 6" strokeLinecap="round" opacity={match} />
        <RangeAxes f={A} x={[0, 2 * PI]} y={[-1, 1]} xTicks={xT} yTicks={yT} progress={axA} labels={axA} />
        {axB > 0 && <RangeAxes f={B} x={[0, 2 * PI]} y={[-1, 1]} xTicks={xT.map((t) => ({ v: t.v }))} yTicks={yT} progress={axB} labels={axB} />}
        <Curve f={A} fn={Math.sin} a={0} b={2 * PI + 0.2} progress={sinP} c={semantic.sin} />
        <Curve f={B} fn={Math.cos} a={0} b={2 * PI + 0.2} progress={cosP} c={semantic.cos} />
        <SlopeTriangle f={A} x0={x} y0={y} m={m} progress={match} />
        {Math.abs(m) > 0.004 && match > 0 && <line x1={bx} y1={by0} x2={bx} y2={by0 + (qy - by0) * match} stroke={color.accent} strokeWidth={stroke.emphasis} strokeLinecap="round" />}
        <g clipPath="url(#slclip)">
          <Tangent f={A} x0={x} y0={y} m={m} half={230} grow={grow} />
        </g>
        {grow > 0.05 && <Dot f={A} x={x} y={y} />}
        {axB > 0 && <Dot f={B} x={x} y={m} c={semantic.cos} opacity={cosP} />}
        <TangentNote f={A} x0={x} y0={y} m={m} at={-150} lift={24} opacity={note}>
          <tspan fontStyle="italic">slope</tspan> {fmt(m)}
        </TangentNote>

        {/* inset circle */}
        <g opacity={circ}>
          <line x1={O.x - R - 20} y1={O.y} x2={O.x + R + 20} y2={O.y} stroke={color.ink3} strokeWidth={1.6} />
          <line x1={O.x} y1={O.y + R + 20} x2={O.x} y2={O.y - R - 20} stroke={color.ink3} strokeWidth={1.6} />
          <circle cx={O.x} cy={O.y} r={R} fill="none" stroke={color.ink} strokeWidth={2.6} />
          <line x1={O.x} y1={O.y} x2={P.x} y2={P.y} stroke={color.ink2} strokeWidth={1.6} />
          <line x1={P.x} y1={P.y} x2={P.x} y2={P.y + V.y} stroke={color.accent} strokeWidth={4} strokeLinecap="round" />
        </g>
        <Arrow x1={P.x} y1={P.y} x2={P.x + V.x} y2={P.y + V.y} p={circ} c={color.accent} w={2.4} head={11} o={0.55} />
        {circ > 0 && <circle cx={P.x} cy={P.y} r={6} fill={color.ink} stroke={color.paper} strokeWidth={2} opacity={circ} />}
      </Layer>
      <Txt x={bx + 18} y={(by0 + qy) / 2 - 22} w={300} size={type.label} c={color.ink} p={match} o={1 - peak} style={{ fontFeatureSettings: "'lnum' 1, 'tnum' 1" }}>
        <i>height</i> {fmt(m)}
      </Txt>
      <M x={1560} y={210} t="y=\sin x" size={46} p={axA} />
      <M x={1560} y={960} t="y=\cos x" size={46} c={semantic.cos} p={axB} />
      <Txt x={px(A, PI / 2, 1)[0] + 170} y={px(A, PI / 2, 1)[1] - 70} w={260} align="center" size={30} italic c={color.accent} p={peak} o={peak}>
        flat tangent
      </Txt>
      <Txt x={px(B, PI / 2, 0)[0] + 16} y={px(B, PI / 2, 0)[1] - 52} w={240} size={30} italic c={color.accent} p={peak} o={peak}>
        cos = 0
      </Txt>
      <div style={{ position: "absolute", left: 120, top: 140, ...wipe(p("match", 30, 30), 0) }}>
        <FigureCaption n="3.1" y={0} x={0} w={290}>
          The red rise of the tangent (per unit run) and the red bar below always have the same length.
        </FigureCaption>
      </div>
      <Txt x={120} y={790} w={300} size={30} italic c={color.ink2} p={circ}>
        The circle agrees: the point’s height changes at rate <span style={{ color: semantic.cos, fontStyle: "normal" }}>cos x</span>.
      </Txt>
    </Sheet>
  );
};
