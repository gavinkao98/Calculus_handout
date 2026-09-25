/**
 * 繪圖原件：Axes、FunctionPlot（筆畫描繪）、Tangent（彈性切線）、SlopeTriangle、ProjectionLine。
 * 全部透過 useView() 把世界座標投影到螢幕，鏡頭改變時線寬不變。
 */
import React from "react";
import { color, dash, stroke } from "../theme";
import { clamp01, fnPath, project, useView, type Pt } from "../lib/view";
import { Arrowhead, Svg } from "./Draft";
import { MathAt } from "./MathTex";

export type Tick = { x: number; tex: string };

export const Axes: React.FC<{
  xMin: number;
  xMax: number;
  yMin: number;
  yMax: number;
  yOff?: number;
  progress?: number;
  xTicks?: Tick[];
  yTicks?: Array<{ y: number; tex: string }>;
  xLabel?: string;
  yLabel?: string;
  labelOpacity?: number;
  tickSize?: number;
}> = ({
  xMin,
  xMax,
  yMin,
  yMax,
  yOff = 0,
  progress = 1,
  xTicks = [],
  yTicks = [],
  xLabel = "x",
  yLabel,
  labelOpacity = 1,
  tickSize = 26,
}) => {
  const v = useView();
  const px = clamp01(progress / 0.8);
  const py = clamp01((progress - 0.2) / 0.8);
  const xe = xMin + (xMax - xMin) * px;
  const ye = yMin + (yMax - yMin) * py;
  const [ax0, ay] = project(v, xMin, yOff);
  const [ax1] = project(v, xe, yOff);
  const [oxs, oy0] = project(v, 0, yMin + yOff);
  const [, oy1] = project(v, 0, ye + yOff);
  const xTickPts = xTicks.map((t) => ({ ...t, p: project(v, t.x, yOff) }));
  return (
    <>
      <Svg>
        {px > 0 ? <line x1={ax0} y1={ay} x2={ax1} y2={ay} stroke={color.ink} strokeOpacity={0.9} strokeWidth={stroke.axis} /> : null}
        {py > 0 ? <line x1={oxs} y1={oy0} x2={oxs} y2={oy1} stroke={color.ink} strokeOpacity={0.9} strokeWidth={stroke.axis} /> : null}
        {px > 0.97 ? <Arrowhead tip={[ax1 + 16, ay]} dir={[1, 0]} fill={color.ink} /> : null}
        {py > 0.97 ? <Arrowhead tip={[oxs, oy1 - 16]} dir={[0, -1]} fill={color.ink} /> : null}
        {xTickPts.map((t) => {
          const on = clamp01((xe - t.x) * 4);
          return t.x === 0 ? null : (
            <line key={t.tex} x1={t.p[0]} x2={t.p[0]} y1={t.p[1] - 8 * on} y2={t.p[1] + 8 * on} stroke={color.ink} strokeWidth={stroke.axis} />
          );
        })}
        {yTicks.map((t) => {
          const [tx, ty] = project(v, 0, t.y + yOff);
          const on = clamp01((ye - t.y) * 4);
          return <line key={t.tex} x1={tx - 8 * on} x2={tx + 8 * on} y1={ty} y2={ty} stroke={color.ink} strokeWidth={stroke.axis} />;
        })}
      </Svg>
      {xTickPts.map((t) =>
        t.x === 0 ? null : (
          <MathAt
            key={t.tex}
            x={t.p[0]}
            y={t.p[1] + 16}
            tex={t.tex}
            size={tickSize}
            anchor="t"
            color={color.ink2}
            opacity={clamp01((xe - t.x) * 3) * labelOpacity}
          />
        ),
      )}
      {yTicks.map((t) => {
        const [tx, ty] = project(v, 0, t.y + yOff);
        return (
          <MathAt
            key={t.tex}
            x={tx - 18}
            y={ty}
            tex={t.tex}
            size={tickSize}
            anchor="r"
            color={color.ink2}
            opacity={clamp01((ye - t.y) * 3) * labelOpacity}
          />
        );
      })}
      <MathAt x={ax1 + 26} y={ay + 16} tex={xLabel} size={tickSize + 4} anchor="tl" color={color.ink2} opacity={clamp01((px - 0.9) * 10) * labelOpacity} />
      {yLabel ? (
        <MathAt x={oxs + 16} y={oy1 - 18} tex={yLabel} size={tickSize + 4} anchor="bl" color={color.ink2} opacity={clamp01((py - 0.9) * 10) * labelOpacity} />
      ) : null}
    </>
  );
};

/** 函數曲線；以截斷定義域描繪（虛線也不會被 draw-on 打亂） */
export const FunctionPlot: React.FC<{
  fn: (x: number) => number;
  from: number;
  to: number;
  progress?: number;
  /** 直接指定可見區間（覆寫 progress） */
  range?: [number, number];
  yOff?: number;
  stroke?: string;
  width?: number;
  dashArray?: string;
  opacity?: number;
}> = ({ fn, from, to, progress = 1, range, yOff = 0, stroke: sc = color.sin, width = stroke.object, dashArray, opacity = 1 }) => {
  const v = useView();
  const [a, b] = range ?? [from, from + (to - from) * clamp01(progress)];
  const d = fnPath(v, fn, a, b, yOff);
  if (!d) return null;
  return (
    <Svg opacity={opacity}>
      <path d={d} fill="none" stroke={color.paper} strokeWidth={width + 8} strokeOpacity={0.55} strokeLinejoin="round" />
      <path d={d} fill="none" stroke={sc} strokeWidth={width} strokeLinecap="round" strokeLinejoin="round" strokeDasharray={dashArray} />
    </Svg>
  );
};

/** 曲線上的點：白環＋紙色填心（製圖的「節點」） */
export const Node: React.FC<{ at: Pt; ring?: string; r?: number; opacity?: number; fill?: string }> = ({
  at,
  ring = color.ink,
  r = 7,
  opacity = 1,
  fill = color.paper,
}) => (
  <Svg opacity={opacity}>
    <circle cx={at[0]} cy={at[1]} r={r} fill={fill} stroke={ring} strokeWidth={2.4} />
  </Svg>
);

/** 切線：以接觸點為中心往兩側生長；grow 可 >1（彈簧回彈） */
export const Tangent: React.FC<{
  fn: (x: number) => number;
  dfn: (x: number) => number;
  x0: number;
  yOff?: number;
  halfLen?: number; // 世界單位（沿切線）
  grow?: number;
  stroke?: string;
  opacity?: number;
  node?: boolean;
}> = ({ fn, dfn, x0, yOff = 0, halfLen = 1, grow = 1, stroke: sc = color.accent, opacity = 1, node = true }) => {
  const v = useView();
  const m = dfn(x0);
  const y0 = fn(x0) + yOff;
  const k = (halfLen * Math.max(0, grow)) / Math.sqrt(1 + m * m);
  const p1 = project(v, x0 - k, y0 - m * k);
  const p2 = project(v, x0 + k, y0 + m * k);
  const c = project(v, x0, y0);
  return (
    <Svg opacity={opacity}>
      <line x1={p1[0]} y1={p1[1]} x2={p2[0]} y2={p2[1]} stroke={sc} strokeWidth={stroke.tangent} strokeLinecap="round" />
      {node ? <circle cx={c[0]} cy={c[1]} r={7.5} fill={color.paper} stroke={sc} strokeWidth={2.6} /> : null}
    </Svg>
  );
};

/** 斜率三角：run＝1 的水平段（虛線）＋ rise＝m 的鉛直段（實線） */
export const SlopeTriangle: React.FC<{
  fn: (x: number) => number;
  dfn: (x: number) => number;
  x0: number;
  yOff?: number;
  run?: number;
  progress?: number;
  tint?: string;
  runLabel?: boolean;
}> = ({ fn, dfn, x0, yOff = 0, run = 1, progress = 1, tint = color.accent, runLabel = true }) => {
  const v = useView();
  const m = dfn(x0);
  const y0 = fn(x0) + yOff;
  const pr = clamp01(progress / 0.5);
  const pv = clamp01((progress - 0.5) / 0.5);
  const P = project(v, x0, y0);
  const Q = project(v, x0 + run * pr, y0);
  const R = project(v, x0 + run, y0 + m * run * pv);
  if (Math.abs(m) < 0.02) return null;
  return (
    <Svg>
      <line x1={P[0]} y1={P[1]} x2={Q[0]} y2={Q[1]} stroke={tint} strokeOpacity={0.75} strokeWidth={stroke.thin} strokeDasharray={dash.construction} />
      {pv > 0 ? <line x1={Q[0]} y1={Q[1]} x2={R[0]} y2={R[1]} stroke={tint} strokeWidth={2.2} /> : null}
      {pv > 0 && Math.abs(m) > 0.08 ? (
        <path
          d={`M${Q[0] - 12},${Q[1]} L${Q[0] - 12},${Q[1] - Math.sign(m) * 12} L${Q[0]},${Q[1] - Math.sign(m) * 12}`}
          fill="none"
          stroke={tint}
          strokeOpacity={0.7}
          strokeWidth={1.2}
        />
      ) : null}
      {runLabel && pr > 0.9 ? (
        <text
          x={(P[0] + Q[0]) / 2}
          y={P[1] + (m >= 0 ? 26 : -12)}
          textAnchor="middle"
          fill={tint}
          opacity={clamp01((pr - 0.9) * 10) * 0.9}
          style={{ fontFamily: "IBM Plex Mono", fontSize: 19 }}
        >
          1
        </text>
      ) : null}
    </Svg>
  );
};

/** 投影線（製圖中心線：一長一短） */
export const ProjectionLine: React.FC<{ a: Pt; b: Pt; progress?: number; tint?: string; opacity?: number }> = ({
  a,
  b,
  progress = 1,
  tint = color.ink3,
  opacity = 1,
}) => {
  const p = clamp01(progress);
  return (
    <Svg opacity={opacity}>
      <line
        x1={a[0]}
        y1={a[1]}
        x2={a[0] + (b[0] - a[0]) * p}
        y2={a[1] + (b[1] - a[1]) * p}
        stroke={tint}
        strokeWidth={stroke.thin}
        strokeDasharray={dash.center}
      />
    </Svg>
  );
};
