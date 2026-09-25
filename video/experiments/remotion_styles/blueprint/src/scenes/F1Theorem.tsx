/**
 * F1 定理陳述：兩條規則＝兩個「零件」，編號氣球＋引線註記。
 */
import React from "react";
import { Sheet } from "../components/Sheet";
import { Balloon, Callout, CornerFrame, Svg } from "../components/Draft";
import { Formula, type Tok } from "../components/MathTex";
import { color, font, mono, semantic, stroke, type } from "../theme";
import type { View } from "../lib/view";

const view: View = { cx: 0, cy: 0, s: 120, ox: 960, oy: 540 };

const rule1: Tok[][] = [
  [
    { id: "d", tex: "\\dfrac{d}{dx}", color: semantic.derivative },
    { id: "s", tex: "\\sin x", gap: 0.12 },
    { id: "e", tex: "=", gap: 0.4 },
    { id: "c", tex: "\\cos x", color: semantic.cos, gap: 0.4 },
  ],
];
const rule2: Tok[][] = [
  [
    { id: "d", tex: "\\dfrac{d}{dx}", color: semantic.derivative },
    { id: "c", tex: "\\cos x", color: semantic.cos, gap: 0.12 },
    { id: "e", tex: "=", gap: 0.4 },
    { id: "n", tex: "-", color: semantic.derivative, gap: 0.4 },
    { id: "s", tex: "\\sin x", gap: 0.08 },
  ],
];

export const Eyebrow: React.FC<{ label: string; x?: number; y?: number }> = ({ label, x = 136, y = 118 }) => (
  <div style={{ position: "absolute", left: x, top: y, display: "flex", alignItems: "center", gap: 18 }}>
    <span style={{ ...mono(22, { fontWeight: 600 }), color: color.accent }}>§3.1</span>
    <span style={{ width: 64, height: 1.5, background: color.accent, opacity: 0.8 }} />
    <span style={{ ...mono(20), color: color.ink2 }}>{label}</span>
  </div>
);

export const F1Theorem: React.FC = () => {
  const X = 340;
  const Y1 = 425;
  const Y2 = 695;
  const size = type.math + 4;
  const leader = (y: number, x2: number) => (
    <Svg>
      <line x1={194} y1={y} x2={x2} y2={y} stroke={color.ink3} strokeWidth={stroke.thin} />
    </Svg>
  );
  return (
    <Sheet view={view} gridOpacity={0.8} strip={{ section: "§3.1", title: "Derivatives of sine and cosine", sheet: "SHEET 02 / 04" }}>
      <Eyebrow label="THEOREM · DERIVATIVE RULES" />
      <div
        style={{
          position: "absolute",
          left: 132,
          top: 160,
          fontFamily: font.display,
          fontWeight: 500,
          fontSize: type.h2,
          color: color.ink,
          letterSpacing: "0.01em",
        }}
      >
        Two rules, <span style={{ fontWeight: 300, color: color.ink2 }}>one quarter-turn apart</span>
      </div>

      <CornerFrame x={250} y={286} w={1330} h={548} len={30} stroke={color.ink2} />
      <Svg>
        <line x1={300} x2={1530} y1={560} y2={560} stroke={color.rule} strokeWidth={stroke.hair} strokeDasharray="2 7" />
      </Svg>

      <Formula lines={rule1} x={X} y={Y1} size={size}>
        {(b) => (
          <>
            {leader(Y1, b.d.x - 22)}
            <Balloon at={[170, Y1]} label="1" r={24} />
            <Callout
              anchor={[b.c.x + b.c.w + 14, Y1 - 4]}
              elbow={[b.c.x + b.c.w + 74, Y1 - 64]}
              shelf={420}
              lineColor={semantic.cos}
              textStyle={{ ...mono(22), color: color.ink2 }}
            >
              <span style={{ color: semantic.cos }}>HEIGHT OF cos</span> = SLOPE OF sin
            </Callout>
          </>
        )}
      </Formula>

      <Formula lines={rule2} x={X} y={Y2} size={size}>
        {(b) => (
          <>
            {leader(Y2, b.d.x - 22)}
            <Balloon at={[170, Y2]} label="2" r={24} />
            <Callout
              anchor={[b.n.x + b.n.w * 0.5, Y2 + 30]}
              elbow={[b.n.x + b.n.w * 0.5 + 56, Y2 + 96]}
              shelf={540}
              lineColor={color.accent}
              textStyle={{ ...mono(22), color: color.ink2 }}
            >
              <span style={{ color: color.accent }}>SIGN FLIPS</span>: cos FALLS WHILE sin &gt; 0
            </Callout>
          </>
        )}
      </Formula>

      {/* 圖例列 */}
      <div style={{ position: "absolute", left: 252, top: 872, display: "flex", gap: 44, color: color.ink3, ...mono(17) }}>
        {[
          [semantic.sin, "sin FAMILY"],
          [semantic.cos, "cos FAMILY"],
          [semantic.derivative, "DERIVATIVE / SIGN"],
        ].map(([c, t]) => (
          <span key={t} style={{ display: "flex", alignItems: "center", gap: 14 }}>
            <span style={{ width: 34, height: 3, background: c, display: "inline-block" }} />
            {t}
          </span>
        ))}
        <span>x IN RADIANS · VALID FOR ALL REAL x</span>
      </div>
    </Sheet>
  );
};
