/**
 * 「斜率＝高度」共用裝置：上視圖 sin、下視圖 cos（正投影排列），
 * 在同一個 x 上：sin 的切線＋斜率三角 ↔ cos 的高度段，兩段等長。
 * F2 靜態幀與動態測試共用。
 */
import React from "react";
import { color, mono, semantic } from "../theme";
import { fmtSigned, project, useView } from "../lib/view";
import { Node, ProjectionLine, SlopeTriangle, Tangent } from "../components/Plot";
import { Svg } from "../components/Draft";

/** 下視圖（cos）相對上視圖的世界座標下移量 */
export const D = 2.75;
/** 每個視圖的 y 範圍 */
export const YR = 1.2;

export const sinTicks = [
  { x: Math.PI / 2, tex: "\\tfrac{\\pi}{2}" },
  { x: Math.PI, tex: "\\pi" },
  { x: (3 * Math.PI) / 2, tex: "\\tfrac{3\\pi}{2}" },
  { x: 2 * Math.PI, tex: "2\\pi" },
];

export const SlopeProbe: React.FC<{
  x: number;
  grow?: number;
  triangle?: number;
  readout?: number;
  link?: number;
  height?: number;
  showNumbers?: boolean;
  halfLen?: number;
  readoutText?: (m: number) => string;
  heightText?: (h: number) => string;
}> = ({
  x,
  grow = 1,
  triangle = 1,
  readout = 1,
  link = 1,
  height = 1,
  showNumbers = true,
  halfLen = 1.05,
  readoutText = (m) => `slope ${fmtSigned(m)}`,
  heightText = (h) => `height ${fmtSigned(h)}`,
}) => {
  const v = useView();
  const m = Math.cos(x);
  const top = project(v, x, Math.sin(x));
  const pen = project(v, x, Math.cos(x) - D);
  const base = project(v, x, -D);
  const riseMid = project(v, x + 1, Math.sin(x) + m / 2);
  // 高度接近 0 時讀數抬到軸線上方，免得壓在曲線上
  const hMid = (base[1] + pen[1]) / 2 - Math.max(0, 1 - Math.abs(Math.cos(x)) * 4) * 26;
  return (
    <>
      <ProjectionLine a={top} b={[top[0], pen[1]]} progress={link} />
      <SlopeTriangle fn={Math.sin} dfn={Math.cos} x0={x} progress={triangle} />
      <Tangent fn={Math.sin} dfn={Math.cos} x0={x} grow={grow} halfLen={halfLen} />
      {height > 0 ? (
        <Svg opacity={height}>
          <line x1={base[0]} y1={base[1]} x2={pen[0]} y2={pen[1]} stroke={semantic.cos} strokeWidth={2.2} />
          <line x1={base[0] - 9} x2={base[0] + 9} y1={base[1]} y2={base[1]} stroke={semantic.cos} strokeWidth={2} />
        </Svg>
      ) : null}
      {height > 0 ? <Node at={pen} ring={semantic.cos} opacity={height} /> : null}
      {showNumbers ? (
        <Svg>
          <text
            x={riseMid[0] + 16}
            y={riseMid[1] + 8}
            fill={color.accent}
            opacity={readout}
            style={mono(24, { fontWeight: 500 })}
          >
            {readoutText(m)}
          </text>
          <text x={base[0] + 18} y={hMid + 8} fill={semantic.cos} opacity={readout * height} style={mono(24, { fontWeight: 500 })}>
            {heightText(Math.cos(x))}
          </text>
        </Svg>
      ) : null}
    </>
  );
};
