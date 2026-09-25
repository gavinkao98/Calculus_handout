/**
 * F3 導數循環：四個視圖（VIEW A–D）順時針排列，弧形箭頭＝d/dx；
 * 負號函數沿用家族色、改用「隱藏線」虛線。
 */
import React from "react";
import { Sheet } from "../components/Sheet";
import { Arrowhead, CornerFrame, Svg } from "../components/Draft";
import { Axes, FunctionPlot } from "../components/Plot";
import { MathAt } from "../components/MathTex";
import { color, mono, semantic, stroke } from "../theme";
import { clamp01, ViewProvider, type View } from "../lib/view";
import { Eyebrow } from "./F1Theorem";

type Panel = {
  id: string;
  fn: (x: number) => number;
  tex: string;
  tint: string;
  dashed: boolean;
  x: number;
  y: number;
};

const PW = 560;
const PH = 280;
const CX = 960;
const CY = 540;
const GX = 170; // 面板與中心的水平間距（半）
const GY = 64;

const panels: Panel[] = [
  { id: "A", fn: Math.sin, tex: "\\sin x", tint: semantic.sin, dashed: false, x: CX - GX - PW, y: CY - GY - PH },
  { id: "B", fn: Math.cos, tex: "\\cos x", tint: semantic.cos, dashed: false, x: CX + GX, y: CY - GY - PH },
  { id: "C", fn: (x) => -Math.sin(x), tex: "-\\sin x", tint: semantic.sin, dashed: true, x: CX + GX, y: CY + GY },
  { id: "D", fn: (x) => -Math.cos(x), tex: "-\\cos x", tint: semantic.cos, dashed: true, x: CX - GX - PW, y: CY + GY },
];

export const CyclePanel: React.FC<{ p: Panel; progress?: number; highlight?: number }> = ({ p, progress = 1, highlight = 0 }) => {
  const s = 48;
  const v: View = { cx: 0, cy: 0, s, ox: p.x + 222, oy: p.y + PH / 2 + 14 };
  return (
    <>
      <CornerFrame x={p.x} y={p.y} w={PW} h={PH} full stroke={highlight > 0 ? color.accent : color.ink2} />
      <div style={{ position: "absolute", left: p.x + 22, top: p.y + 18, color: color.ink3, ...mono(15, { fontWeight: 600 }) }}>
        VIEW {p.id}
      </div>
      <MathAt x={p.x + 24} y={p.y + PH / 2 + 12} tex={p.tex} size={44} color={p.tint} anchor="l" />
      <ViewProvider view={v}>
        <Axes xMin={-0.25} xMax={2 * Math.PI + 0.25} yMin={-1.3} yMax={1.3} xTicks={[{ x: Math.PI, tex: "\\pi" }, { x: 2 * Math.PI, tex: "2\\pi" }]} xLabel="" tickSize={20} />
        <FunctionPlot fn={p.fn} from={0} to={2 * Math.PI} progress={progress} stroke={p.tint} width={3.2} dashArray={p.dashed ? "12 8" : undefined} />
      </ViewProvider>
    </>
  );
};

/** 弧形 d/dx 箭頭：以中心為圓心的圓弧，a0→a1（度，順時針為正） */
export const CycleArrow: React.FC<{ a0: number; a1: number; r: number; label: string; labelR: number; progress?: number }> = ({
  a0,
  a1,
  r,
  label,
  labelR,
  progress = 1,
}) => {
  const p = clamp01(progress);
  const rad = (d: number) => (d * Math.PI) / 180;
  const ae = a0 + (a1 - a0) * p;
  const P = (a: number, rr = r): [number, number] => [CX + rr * Math.cos(rad(a)), CY + rr * Math.sin(rad(a))];
  const [x0, y0] = P(a0);
  const [x1, y1] = P(ae);
  const tip = P(ae);
  const tangent: [number, number] = [-Math.sin(rad(ae)), Math.cos(rad(ae))];
  const mid = (a0 + a1) / 2;
  const [lx, ly] = P(mid, labelR);
  return (
    <>
      <Svg>
        <path d={`M${x0},${y0} A${r},${r} 0 0 1 ${x1},${y1}`} fill="none" stroke={color.accent} strokeWidth={2.4} />
        {p > 0.95 ? <Arrowhead tip={[tip[0] + tangent[0] * 6, tip[1] + tangent[1] * 6]} dir={tangent} fill={color.accent} len={20} half={6} /> : null}
      </Svg>
      <MathAt x={lx} y={ly} tex={label} size={34} color={color.accent} opacity={clamp01((p - 0.5) * 2)} />
    </>
  );
};

export const F3Cycle: React.FC = () => {
  const r = 150;
  return (
    <Sheet view={{ cx: 0, cy: 0, s: 104, ox: CX, oy: CY }} gridOpacity={0.8} strip={{ section: "§3.1", title: "The derivative cycle", sheet: "SHEET 04 / 04" }}>
      <Eyebrow label="THE DERIVATIVE CYCLE · PERIOD 4" />
      {panels.map((p) => (
        <CyclePanel key={p.id} p={p} />
      ))}
      {/* 中心：循環圈 */}
      <Svg>
        <circle cx={CX} cy={CY} r={r} fill="none" stroke={color.rule} strokeWidth={stroke.hair} strokeDasharray="2 6" />
      </Svg>
      <MathAt x={CX} y={CY - 8} tex="\frac{d^4}{dx^4}\sin x = \sin x" size={30} color={color.ink2} />
      <div style={{ position: "absolute", left: CX, top: CY + 40, transform: "translateX(-50%)", color: color.ink3, whiteSpace: "nowrap", ...mono(15) }}>
        PERIOD 4
      </div>
      <CycleArrow a0={-128} a1={-52} r={r} label="\tfrac{d}{dx}" labelR={r + 44} />
      <CycleArrow a0={-38} a1={38} r={r} label="\tfrac{d}{dx}" labelR={r + 50} />
      <CycleArrow a0={52} a1={128} r={r} label="\tfrac{d}{dx}" labelR={r + 44} />
      <CycleArrow a0={142} a1={218} r={r} label="\tfrac{d}{dx}" labelR={r + 50} />
      <div style={{ position: "absolute", left: 232, top: 906, color: color.ink3, ...mono(17), display: "flex", gap: 40, alignItems: "center" }}>
        <span style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <svg width={44} height={6}>
            <line x1={0} x2={44} y1={3} y2={3} stroke={color.ink} strokeWidth={3} />
          </svg>
          f
        </span>
        <span style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <svg width={44} height={6}>
            <line x1={0} x2={44} y1={3} y2={3} stroke={color.ink} strokeWidth={3} strokeDasharray="12 8" />
          </svg>
          −f (HIDDEN-LINE CONVENTION)
        </span>
        <span>FOUR TURNS RETURN TO THE START.</span>
      </div>
    </Sheet>
  );
};
