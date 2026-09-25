/**
 * F2 斜率＝高度：上視圖 sin 三條切線（A/B/C），正投影到下視圖 cos 的高度；右欄零件表（BOM）。
 */
import React from "react";
import { Sheet } from "../components/Sheet";
import { Balloon, Svg } from "../components/Draft";
import { Axes, FunctionPlot } from "../components/Plot";
import { MathAt } from "../components/MathTex";
import { color, font, mono, semantic, stroke, type } from "../theme";
import { fmtPlain, project, ViewProvider, type View } from "../lib/view";
import { D, SlopeProbe, sinTicks, YR } from "./slopeRig";
import { Eyebrow } from "./F1Theorem";

const view: View = { cx: 0, cy: -D / 2, s: 150, ox: 215, oy: 507 };

const probes = [
  { id: "A", x: 0, tex: "0", m: "1" },
  { id: "B", x: Math.PI / 2, tex: "\\tfrac{\\pi}{2}", m: "0" },
  { id: "C", x: Math.PI, tex: "\\pi", m: "-1" },
];

export const BomTable: React.FC<{ x: number; y: number; rows: typeof probes; reveal?: number }> = ({ x, y, rows }) => {
  const cols = [72, 118, 176, 176];
  const w = cols.reduce((a, b) => a + b, 0);
  const hh = 58;
  const rh = 70;
  const h = hh + rh * rows.length;
  const xs = cols.reduce<number[]>((acc, c) => [...acc, acc[acc.length - 1] + c], [x]);
  const heads = ["ITEM", "x", "SLOPE OF sin", "HEIGHT OF cos"];
  const headColor = [color.ink3, color.ink3, color.accent, semantic.cos];
  return (
    <>
      <Svg>
        <rect x={x} y={y} width={w} height={h} fill={color.paper} fillOpacity={0.85} stroke={color.ink} strokeOpacity={0.8} strokeWidth={2} />
        <line x1={x} x2={x + w} y1={y + hh} y2={y + hh} stroke={color.ink} strokeOpacity={0.6} strokeWidth={stroke.thin} />
        {rows.slice(1).map((_, i) => (
          <line key={i} x1={x} x2={x + w} y1={y + hh + rh * (i + 1)} y2={y + hh + rh * (i + 1)} stroke={color.rule} strokeWidth={stroke.hair} />
        ))}
        {xs.slice(1, -1).map((cx) => (
          <line key={cx} x1={cx} x2={cx} y1={y} y2={y + h} stroke={color.rule} strokeWidth={stroke.hair} />
        ))}
      </Svg>
      {heads.map((t, i) => (
        <div
          key={t}
          style={{
            position: "absolute",
            left: xs[i],
            width: cols[i],
            top: y,
            height: hh,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            color: headColor[i],
            ...mono(15, { fontWeight: 600 }),
          }}
        >
          {t}
        </div>
      ))}
      {rows.map((r, j) => {
        const cy = y + hh + rh * j + rh / 2;
        return (
          <React.Fragment key={r.id}>
            <Balloon at={[xs[0] + cols[0] / 2, cy]} label={r.id} r={18} />
            <MathAt x={xs[1] + cols[1] / 2} y={cy} tex={r.tex} size={34} color={color.ink} />
            <MathAt x={xs[2] + cols[2] / 2} y={cy} tex={r.m} size={36} color={color.accent} />
            <MathAt x={xs[3] + cols[3] / 2} y={cy} tex={r.m} size={36} color={semantic.cos} />
          </React.Fragment>
        );
      })}
    </>
  );
};

const Swatch: React.FC<{ c: string }> = ({ c }) => (
  <span style={{ display: "inline-block", width: 30, height: 3, background: c, marginRight: 14, verticalAlign: "middle" }} />
);

export const F2Slope: React.FC = () => {
  const balloonAt = (x: number, dy: number): [number, number] => {
    const p = project(view, x, Math.sin(x));
    return [p[0] - 34, p[1] + dy];
  };
  return (
    <Sheet view={view} strip={{ section: "§3.1", title: "Slope of sin = height of cos", sheet: "SHEET 03 / 04" }}>
      <ViewProvider view={view}>
        <Axes xMin={-0.5} xMax={2 * Math.PI + 0.35} yMin={-YR} yMax={YR} xTicks={sinTicks} yLabel="" />
        <Axes xMin={-0.5} xMax={2 * Math.PI + 0.35} yMin={-YR} yMax={YR} yOff={-D} xTicks={[]} yLabel="" />
        <FunctionPlot fn={Math.sin} from={-0.5} to={2 * Math.PI + 0.1} />
        <FunctionPlot fn={Math.cos} from={-0.5} to={2 * Math.PI + 0.1} yOff={-D} stroke={semantic.cos} />
        {probes.map((p) => (
          <SlopeProbe
            key={p.id}
            x={p.x}
            halfLen={0.8}
            readoutText={(m) => `m = ${fmtPlain(m)}`}
            heightText={(h) => `h = ${fmtPlain(h)}`}
          />
        ))}
        <Balloon at={balloonAt(0, -52)} label="A" r={18} />
        <Balloon at={balloonAt(Math.PI / 2, -60)} label="B" r={18} />
        <Balloon at={balloonAt(Math.PI, -58)} label="C" r={18} />
        <MathAt x={project(view, 4.1, 0)[0]} y={project(view, 0, 0.9)[1]} tex="y=\sin x" size={34} color={semantic.sin} anchor="l" />
        <MathAt x={project(view, 4.3, 0)[0]} y={project(view, 0, 0.9 - D)[1]} tex="y=\cos x" size={34} color={semantic.cos} anchor="l" />
      </ViewProvider>

      <Eyebrow label="SLOPE = HEIGHT" x={1290} y={118} />
      <div
        style={{
          position: "absolute",
          left: 1286,
          top: 158,
          width: 560,
          fontFamily: font.display,
          fontWeight: 500,
          fontSize: type.h2,
          lineHeight: 1.02,
          color: color.ink,
        }}
      >
        Read the slope of <span style={{ color: semantic.sin, fontWeight: 600 }}>sin</span>
        <br />
        <span style={{ fontWeight: 300, color: color.ink2 }}>off the height of</span>{" "}
        <span style={{ color: semantic.cos, fontWeight: 600 }}>cos</span>
      </div>
      <BomTable x={1290} y={360} rows={probes} />
      <div style={{ position: "absolute", left: 1290, top: 640, width: 540, color: color.ink3, ...mono(17), lineHeight: 1.7 }}>
        <div>
          <Swatch c={color.accent} /> RISE PER UNIT RUN ON sin
        </div>
        <div>
          <Swatch c={semantic.cos} /> HEIGHT ABOVE AXIS ON cos
        </div>
        <div style={{ marginTop: 10, color: color.ink2 }}>SAME x, SAME LENGTH.</div>
      </div>
    </Sheet>
  );
};
