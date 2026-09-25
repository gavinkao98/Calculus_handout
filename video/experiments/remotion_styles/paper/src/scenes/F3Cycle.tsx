import React from "react";
import { color, semantic, stroke } from "../theme";
import { SceneShell } from "../components/Shell";
import { InlineTex, SmallCaps } from "../components/Type";
import { FormulaG, Token } from "../components/Formula";
import { FigureCaption, Sidenote } from "../components/Marginalia";
import { HEAD } from "../content";

const DEG = Math.PI / 180;

export const cycleNodes: { tokens: Token[]; ang: number; gap: number }[] = [
  { tokens: [{ key: "f", tex: "\\sin x" }], ang: -90, gap: 20 },
  { tokens: [{ key: "f", tex: "\\cos x", color: semantic.cos }], ang: 0, gap: 13 },
  { tokens: [{ key: "f", tex: "{-}\\!\\sin x" }], ang: 90, gap: 24 },
  { tokens: [{ key: "f", tex: "{-}\\!\\cos x", color: semantic.cos }], ang: 180, gap: 13 },
];

/** Clockwise arc from a1 to a2 (deg) with an arrowhead; progress inks it on. */
export const CycleArc: React.FC<{ cx: number; cy: number; r: number; a1: number; a2: number; progress?: number; head?: number }> = ({
  cx,
  cy,
  r,
  a1,
  a2,
  progress = 1,
  head = 1,
}) => {
  if (progress <= 0) return null;
  const e = a1 + (a2 - a1) * progress;
  const p = (a: number) => [cx + r * Math.cos(a * DEG), cy + r * Math.sin(a * DEG)];
  const [x1, y1] = p(a1);
  const [x2, y2] = p(e);
  const large = e - a1 > 180 ? 1 : 0;
  // tangent direction (clockwise on screen) at the end
  const tx = -Math.sin(e * DEG);
  const ty = Math.cos(e * DEG);
  const L = 20;
  const wing = (s: number) => {
    const c = Math.cos(s * 26 * DEG);
    const sn = Math.sin(s * 26 * DEG);
    const bx = -(tx * c - ty * sn);
    const by = -(tx * sn + ty * c);
    return `M${x2} ${y2} L${x2 + bx * L} ${y2 + by * L}`;
  };
  return (
    <g>
      <path d={`M${x1} ${y1} A${r} ${r} 0 ${large} 1 ${x2} ${y2}`} fill="none" stroke={color.accent} strokeWidth={stroke.tangent} strokeLinecap="round" />
      <path d={`${wing(1)} ${wing(-1)}`} stroke={color.accent} strokeWidth={stroke.tangent} strokeLinecap="round" opacity={head} fill="none" />
    </g>
  );
};

export const CycleRing: React.FC<{
  cx: number;
  cy: number;
  r: number;
  size: number;
  arcP?: (i: number) => number;
  nodeP?: (i: number) => number;
}> = ({ cx, cy, r, size, arcP = () => 1, nodeP = () => 1 }) => (
  <g>
    <circle cx={cx} cy={cy} r={r} fill="none" stroke={color.rule} strokeWidth={1.4} strokeDasharray="1.5 7" strokeLinecap="round" />
    {cycleNodes.map((n, i) => {
      const next = cycleNodes[(i + 1) % 4];
      const a1 = n.ang + n.gap;
      const a2 = (next.ang < n.ang ? next.ang + 360 : next.ang) - next.gap;
      const mid = ((n.ang + (next.ang < n.ang ? next.ang + 360 : next.ang)) / 2) * DEG;
      const lx = cx + (r + 64) * Math.cos(mid);
      const ly = cy + (r + 64) * Math.sin(mid);
      const p = arcP(i);
      return (
        <g key={i}>
          <CycleArc cx={cx} cy={cy} r={r} a1={a1} a2={a2} progress={p} head={p >= 1 ? 1 : 0} />
          <g transform={`translate(${lx} ${ly + size * 0.2})`} opacity={Math.min(1, p * 1.5)}>
            <FormulaG tokens={[{ key: "d", tex: "\\tfrac{d}{dx}", color: color.accent }]} opts={{ size: size * 0.62, align: "center" }} />
          </g>
        </g>
      );
    })}
    {cycleNodes.map((n, i) => {
      const x = cx + r * Math.cos(n.ang * DEG);
      const y = cy + r * Math.sin(n.ang * DEG);
      const o = nodeP(i);
      return (
        <g key={`n${i}`} opacity={o} transform={`translate(${x} ${y + size * 0.26 + (1 - o) * 14})`}>
          <FormulaG tokens={n.tokens} opts={{ size, align: "center" }} />
        </g>
      );
    })}
  </g>
);

/** F3 — the derivative cycle as a four-station ring. */
export const F3Cycle: React.FC = () => {
  const cx = 1130;
  const cy = 590;
  return (
    <SceneShell head={HEAD}>
      <svg width={1920} height={1080} style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }}>
        <CycleRing cx={cx} cy={cy} r={290} size={76} />
        <g transform={`translate(${cx} ${cy + 22})`}>
          <FormulaG tokens={[{ key: "c", tex: "\\frac{d^{4}}{dx^{4}}\\sin x=\\sin x" }]} opts={{ size: 46, align: "center" }} />
        </g>
      </svg>
      <div style={{ position: "absolute", left: cx - 200, top: cy - 78, width: 400, textAlign: "center" }}>
        <SmallCaps size={16} color={color.ink3}>
          Four turns home
        </SmallCaps>
      </div>

      <FigureCaption n="3.4" y={172}>
        Each application of <InlineTex src="\tfrac{d}{dx}" color={color.accent} /> carries a function one quarter-turn
        clockwise; after four, sine is back where it started.
      </FigureCaption>
      <Sidenote y={640}>
        Compare multiplication by <InlineTex src="i" />: <InlineTex src="1\to i\to -1\to -i\to 1" />. The same period-four
        rhythm, and not by accident.
      </Sidenote>
    </SceneShell>
  );
};
