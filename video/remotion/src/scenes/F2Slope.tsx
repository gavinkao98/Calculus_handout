import React from "react";
import { color, features, font, semantic, stroke, type } from "../theme";
import { SceneShell } from "../components/Shell";
import { InlineTex, SmallCaps } from "../components/Type";
import { FormulaG, Token } from "../components/Formula";
import { Curve, Dot, Label, PlotFrame, RangeAxes, SlopeTriangle, Tangent, TangentNote, px, Tick } from "../components/Plot";
import { FigureCaption } from "../components/Marginalia";
import { HEAD } from "../content";

const PI = Math.PI;
export const xTicks: Tick[] = [
  { v: PI / 2, label: [{ key: "t", tex: "\\pi/2" }] },
  { v: PI, label: [{ key: "t", tex: "\\pi" }] },
  { v: (3 * PI) / 2, label: [{ key: "t", tex: "3\\pi/2" }] },
  { v: 2 * PI, label: [{ key: "t", tex: "2\\pi" }] },
];
export const yTicks: Tick[] = [
  { v: 1, label: [{ key: "t", tex: "1" }] },
  { v: -1, label: [{ key: "t", tex: "{-}1" }] },
];
const fmt = (m: number) => (Math.abs(m) < 1e-9 ? "0" : m < 0 ? `−${Math.abs(m)}` : `${m}`);

/** Panel title: "(a)" + math, top-left of a panel. */
export const PanelTitle: React.FC<{ x: number; y: number; letter: string; tokens: Token[]; opacity?: number }> = ({
  x,
  y,
  letter,
  tokens,
  opacity = 1,
}) => (
  <g opacity={opacity}>
    <Label x={x} y={y} italic c={color.ink2} size={type.label + 2}>
      ({letter})
    </Label>
    <g transform={`translate(${x + 46} ${y})`}>
      <FormulaG tokens={tokens} opts={{ size: type.label + 8 }} />
    </g>
  </g>
);

/** F2 — slope of sin at 0, π/2, π equals the height of cos there. */
export const F2Slope: React.FC = () => {
  const A: PlotFrame = { ox: 580, oy: 318, ux: 172, uy: 128 };
  const B: PlotFrame = { ox: 580, oy: 760, ux: 172, uy: 128 };
  const xs = [0, PI / 2, PI];
  return (
    <SceneShell head={HEAD}>
      <svg width={1920} height={1080} style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }}>
        {/* plumb lines first, so tick labels' paper halos knock them out */}
        {xs.map((x) => {
          const [x1, y1] = px(A, x, Math.sin(x));
          const [, y2] = px(B, x, Math.cos(x));
          return <line key={x} x1={x1} y1={y1 + 12} x2={x1} y2={y2 - 12} stroke={color.ink3} strokeWidth={1.4} strokeDasharray="1.5 6" strokeLinecap="round" />;
        })}
        <PanelTitle x={1540} y={196} letter="a" tokens={[{ key: "y", tex: "y=\\sin x" }]} />
        <PanelTitle x={1540} y={908} letter="b" tokens={[{ key: "y", tex: "y=\\cos x", color: semantic.cos }]} />
        <RangeAxes f={A} x={[0, 2 * PI]} y={[-1, 1]} xTicks={xTicks} yTicks={yTicks} />
        {/* small multiples share x: panel (b) keeps ticks, drops repeated labels */}
        <RangeAxes f={B} x={[0, 2 * PI]} y={[-1, 1]} xTicks={xTicks.map((t) => ({ v: t.v }))} yTicks={yTicks} />
        <defs>
          <clipPath id="f2clipA">
            <rect x={470} y={110} width={1330} height={400} />
          </clipPath>
        </defs>

        <Curve f={A} fn={Math.sin} a={-0.35} b={2 * PI + 0.3} c={semantic.sin} />
        <Curve f={B} fn={Math.cos} a={0} b={2 * PI + 0.3} c={semantic.cos} />

        {xs.map((x) => (
          <g key={`t${x}`}>
            <SlopeTriangle f={A} x0={x} y0={Math.sin(x)} m={Math.cos(x)} run={1} />
            <g clipPath="url(#f2clipA)">
              <Tangent f={A} x0={x} y0={Math.sin(x)} m={Math.cos(x)} half={250} />
            </g>
            <Dot f={A} x={x} y={Math.sin(x)} />
          </g>
        ))}
        {xs.map((x) => {
          const [bx, by] = px(B, x, 0);
          const [, qy] = px(B, x, Math.cos(x));
          return (
            <g key={`h${x}`}>
              {Math.abs(Math.cos(x)) > 1e-6 && <line x1={bx} y1={by} x2={bx} y2={qy} stroke={color.accent} strokeWidth={stroke.emphasis} strokeLinecap="round" />}
              <Dot f={B} x={x} y={Math.cos(x)} c={semantic.cos} />
            </g>
          );
        })}

        {/* readouts: slopes lettered along the tangents; heights beside the bars */}
        {xs.map((x, i) => {
          const m = Math.round(Math.cos(x));
          const [bx, by] = px(B, x, m / 2);
          const at = [118, 150, -118][i];
          return (
            <g key={`r${x}`}>
              <TangentNote f={A} x0={x} y0={Math.sin(x)} m={m} at={at} lift={22}>
                <tspan fontStyle="italic">slope</tspan> {fmt(m)}
              </TangentNote>
              <g className="halo">
                <Label x={bx + 18} y={m === 0 ? by - 20 : by + 10} size={type.label} c={color.ink} figures>
                  <tspan fontStyle="italic">height</tspan> {fmt(m)}
                </Label>
              </g>
            </g>
          );
        })}
      </svg>

      <FigureCaption n="3.3" y={172}>
        At each marked <InlineTex src="x" />, the tangent to <InlineTex src="\sin" /> rises, per unit of run, by exactly the
        height of <InlineTex src="\cos" color={semantic.cos} /> at the same <InlineTex src="x" />. The red bars have equal
        length.
      </FigureCaption>

      {/* booktabs table in the margin */}
      <div style={{ position: "absolute", left: 120, top: 560, width: 280 }}>
        <SmallCaps size={18} color={color.ink3}>
          Table 3.1
        </SmallCaps>
        <table
          style={{
            marginTop: 12,
            width: "100%",
            borderCollapse: "collapse",
            fontFamily: font.serif,
            fontSize: 28,
            color: color.ink,
            fontFeatureSettings: features.figures,
            borderTop: `2.2px solid ${color.ink}`,
            borderBottom: `2.2px solid ${color.ink}`,
          }}
        >
          <thead>
            <tr style={{ borderBottom: `1px solid ${color.ink2}` }}>
              <th style={{ textAlign: "left", fontWeight: 400, padding: "8px 0" }}>
                <InlineTex src="x" />
              </th>
              <th style={{ textAlign: "right", fontWeight: 400, fontStyle: "italic", fontSize: 24 }}>slope</th>
              <th style={{ textAlign: "right", fontWeight: 400 }}>
                <InlineTex src="\cos x" color={semantic.cos} />
              </th>
            </tr>
          </thead>
          <tbody>
            {([["0", "1"], ["\\tfrac{\\pi}{2}", "0"], ["\\pi", "−1"]] as const).map(([x, v]) => (
              <tr key={x}>
                <td style={{ padding: "7px 0" }}>
                  <InlineTex src={x} />
                </td>
                <td style={{ textAlign: "right" }}>{v}</td>
                <td style={{ textAlign: "right", color: semantic.cos }}>{v}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </SceneShell>
  );
};
