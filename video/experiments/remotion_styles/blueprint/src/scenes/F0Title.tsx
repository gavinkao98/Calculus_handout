/**
 * F0 節標題卡：單位圓投影出正弦曲線的「作圖」＋在投影點上提問的切線。
 */
import React from "react";
import { AbsoluteFill } from "remotion";
import { Sheet } from "../components/Sheet";
import { TitleBlock } from "../components/TitleBlock";
import { Callout, DimensionLine, Svg } from "../components/Draft";
import { Axes, FunctionPlot, Node, ProjectionLine, Tangent } from "../components/Plot";
import { MathAt } from "../components/MathTex";
import { color, dash, font, mono, stroke, type } from "../theme";
import { project, ViewProvider, type View } from "../lib/view";

const view: View = { cx: 0, cy: 0, s: 110, ox: 520, oy: 800 };
const TH = 0.95; // 投影角
const R = view.s; // 單位圓與曲線同比例
const circleC: [number, number] = [view.ox - R - 150, view.oy];

export const F0Title: React.FC = () => {
  const P = project(view, TH, Math.sin(TH));
  const onCircle: [number, number] = [circleC[0] + R * Math.cos(TH), circleC[1] - R * Math.sin(TH)];
  const tanEnd = project(view, TH + 0.62, Math.sin(TH) + Math.cos(TH) * 0.62);
  const ticks = [
    { x: Math.PI / 2, tex: "\\tfrac{\\pi}{2}" },
    { x: Math.PI, tex: "\\pi" },
    { x: (3 * Math.PI) / 2, tex: "\\tfrac{3\\pi}{2}" },
    { x: 2 * Math.PI, tex: "2\\pi" },
  ];
  const arcR = 34;
  return (
    <Sheet view={view}>
      <ViewProvider view={view}>
        {/* ---------- 標題 ---------- */}
        <AbsoluteFill>
          <div style={{ position: "absolute", left: 136, top: 132, display: "flex", alignItems: "center", gap: 18 }}>
            <span style={{ ...mono(22, { fontWeight: 600 }), color: color.accent }}>§3.1</span>
            <span style={{ width: 64, height: 1.5, background: color.accent, opacity: 0.8 }} />
            <span style={{ ...mono(20), color: color.ink2 }}>CHAPTER 03 · DIFFERENTIATION</span>
          </div>
          <div
            style={{
              position: "absolute",
              left: 128,
              top: 176,
              fontFamily: font.display,
              fontWeight: 600,
              fontSize: type.hero,
              lineHeight: 0.94,
              letterSpacing: "-0.005em",
              color: color.ink,
            }}
          >
            Derivatives of
            <br />
            Sine <span style={{ fontWeight: 300, color: color.ink2 }}>and</span> Cosine
          </div>
        </AbsoluteFill>

        {/* ---------- 通用註記（圖紙 NOTES） ---------- */}
        <div style={{ position: "absolute", left: 1400, top: 132, color: color.ink3, ...mono(17), lineHeight: 1.75 }}>
          <div style={{ color: color.ink2, fontWeight: 600, marginBottom: 6 }}>NOTES</div>
          <div>1. ANGLES IN RADIANS.</div>
          <div>2. UNIT CIRCLE, r = 1.</div>
          <div>3. SLOPE PER UNIT RUN.</div>
        </div>

        {/* ---------- 作圖：單位圓 → 正弦 ---------- */}
        <Svg>
          {/* 圓的中心線 */}
          <line x1={circleC[0] - R - 26} x2={circleC[0] + R + 26} y1={circleC[1]} y2={circleC[1]} stroke={color.ink3} strokeWidth={stroke.thin} strokeDasharray={dash.center} />
          <line x1={circleC[0]} x2={circleC[0]} y1={circleC[1] - R - 26} y2={circleC[1] + R + 26} stroke={color.ink3} strokeWidth={stroke.thin} strokeDasharray={dash.center} />
          <circle cx={circleC[0]} cy={circleC[1]} r={R} fill="none" stroke={color.ink} strokeWidth={2.6} />
          {/* 半徑與角 */}
          <line x1={circleC[0]} y1={circleC[1]} x2={onCircle[0]} y2={onCircle[1]} stroke={color.ink} strokeWidth={2} />
          <path
            d={`M${circleC[0] + arcR},${circleC[1]} A${arcR},${arcR} 0 0 0 ${circleC[0] + arcR * Math.cos(TH)},${circleC[1] - arcR * Math.sin(TH)}`}
            fill="none"
            stroke={color.accent}
            strokeWidth={1.6}
          />
          <line x1={onCircle[0]} x2={onCircle[0]} y1={onCircle[1]} y2={circleC[1]} stroke={color.ink} strokeOpacity={0.9} strokeWidth={stroke.thin} strokeDasharray={dash.construction} />
        </Svg>
        <ProjectionLine a={onCircle} b={P} tint={color.ink2} />
        <MathAt x={circleC[0] + 52} y={circleC[1] - 24} tex="\theta" size={26} color={color.accent} anchor="c" />
        <Axes
          xMin={-0.35}
          xMax={2 * Math.PI + 0.45}
          yMin={-1.3}
          yMax={1.3}
          xTicks={ticks}
          xLabel="\theta"
          tickSize={24}
        />
        <FunctionPlot fn={Math.sin} from={0} to={2 * Math.PI} />
        <Tangent fn={Math.sin} dfn={Math.cos} x0={TH} halfLen={0.95} node={false} />
        <Node at={onCircle} />
        <Node at={P} ring={color.accent} />
        {/* 半徑尺寸 */}
        <DimensionLine p1={[circleC[0], circleC[1]]} p2={[circleC[0] + R, circleC[1]]} offset={R + 40} label="r = 1" size={18} />
        <MathAt x={project(view, 3 * Math.PI / 2 + 0.35, -1)[0]} y={project(view, 0, -1)[1] + 6} tex="y=\sin\theta" size={30} color={color.ink} anchor="tl" />
        <Callout
          anchor={tanEnd}
          elbow={[tanEnd[0] + 110, tanEnd[1] - 150]}
          shelf={560}
          lineColor={color.accent}
          textStyle={{ fontFamily: font.text, fontStyle: "italic", fontSize: 46, color: color.ink }}
        >
          How fast does sine change?
        </Callout>
        <TitleBlock right={1870} bottom={1030} dwg="§3.1" title="DERIV. OF SIN / COS" sheet="01 / 04" />
      </ViewProvider>
    </Sheet>
  );
};
