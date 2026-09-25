/**
 * 15 秒動態測試（共同分鏡）。
 * 0–2.5s 軸＋sin 描繪 → 2.5–4.5s 推近 x=0、切線彈入 → 4.5–8.5s 切線滑到 π、cos 被「畫」出來
 * → 8.5–10.5s 拉遠平移讓位 → 10.5–13.5s token 變形 → 13.5–15s 收束、標題欄簽核。
 */
import React from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { Sheet } from "../components/Sheet";
import { CornerFrame, Reticle, Svg } from "../components/Draft";
import { Axes, FunctionPlot } from "../components/Plot";
import { Formula, MathAt, TokenMorph, type Tok } from "../components/MathTex";
import { TitleBlock } from "../components/TitleBlock";
import { color, motion, mono, semantic } from "../theme";
import { cameraAt, clamp01, project, ViewProvider, type View } from "../lib/view";
import { D, SlopeProbe, sinTicks, YR } from "./slopeRig";

const PI = Math.PI;
const XMIN = -0.55;
const XMAX = 2 * PI + 0.4;

/** 分鏡時間表（幀，30fps） */
export const T = {
  axes: [0, 24],
  sinDraw: [14, 66],
  sinLabel: [56, 74],
  push: [72, 128],
  tangent: 90,
  triangle: [104, 124],
  readout: [112, 126],
  reframe: [130, 168],
  cosAxes: [136, 162],
  slide: [158, 252],
  pull: [256, 314],
  cosRest: [262, 306],
  formulaIn: [300, 326],
  morph: [334, 398],
  box: [398, 418],
  endmark: [404, 436],
} as const;

const V0: View = { cx: PI, cy: 0, s: 168, ox: 960, oy: 500 };
const V1: View = { cx: 0.55, cy: 0.2, s: 340, ox: 880, oy: 520 };
const V2: View = { cx: 2.75, cy: -D / 2, s: 160, ox: 960, oy: 507 };
const V2b: View = { cx: 3.25, cy: -D / 2, s: 160, ox: 960, oy: 507 };
const V3: View = { cx: 2.9, cy: -D / 2, s: 122, ox: 612, oy: 507 };

const cams = [
  { f: 0, v: V0 },
  { f: T.push[0], v: V0 },
  { f: T.push[1], v: V1 },
  { f: T.reframe[0], v: V1 },
  { f: T.reframe[1], v: V2 },
  { f: T.slide[1], v: V2b },
  { f: T.pull[0], v: V2b },
  { f: T.pull[1], v: V3 },
];

const src: Tok[][] = [
  [
    { id: "slope", text: "slope of", color: color.accent, weight: 500 },
    { id: "sin", tex: "\\sin", gap: 0.3 },
    { id: "at1", text: "at", color: color.ink2, gap: 0.3 },
    { id: "x1", tex: "x", gap: 0.25 },
  ],
  [
    { id: "eq", tex: "=" },
    { id: "height", text: "height of", color: color.ink2, gap: 0.4 },
    { id: "cos", tex: "\\cos", color: semantic.cos, gap: 0.3 },
    { id: "at2", text: "at", color: color.ink2, gap: 0.3 },
    { id: "x2", tex: "x", gap: 0.25 },
  ],
];
const dst: Tok[][] = [
  [
    { id: "ddx", tex: "\\dfrac{d}{dx}", color: color.accent },
    { id: "sin", tex: "\\sin", gap: 0.1 },
    { id: "x1", tex: "x", gap: 0.16 },
    { id: "eq", tex: "=", gap: 0.32 },
    { id: "cos", tex: "\\cos", color: semantic.cos, gap: 0.32 },
    { id: "x2", tex: "x", gap: 0.16 },
  ],
];

const FS = 64;

const clampOpt = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

export const MotionTest: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const view = cameraAt(frame, cams, motion.camera);

  const ramp = (r: readonly [number, number], easing = motion.settle) =>
    interpolate(frame, r as unknown as number[], [0, 1], { ...clampOpt, easing });

  // ---- sin
  const axesP = ramp(T.axes, motion.draft);
  const sinP = ramp(T.sinDraw, motion.draft);
  const sinTip = XMIN + (XMAX - 0.15 - XMIN) * sinP;
  const penOn = frame >= T.sinDraw[0] && frame < T.sinDraw[1] + 6;

  // ---- tangent
  const grow = frame < T.tangent ? 0 : spring({ frame: frame - T.tangent, fps, config: motion.springy });
  const tri = ramp(T.triangle, motion.draft);
  const readout = ramp(T.readout);
  const x0 = interpolate(frame, T.slide as unknown as number[], [0, PI], { ...clampOpt, easing: motion.camera });

  // ---- cos
  const cosAxesP = ramp(T.cosAxes, motion.draft);
  const sliding = frame >= T.slide[0];
  const rest = ramp(T.cosRest, motion.draft);
  const cosRange: [number, number] = [0 - (0 - XMIN) * rest, x0 + (XMAX - 0.15 - PI) * rest];
  const heightOn = ramp([T.slide[0] - 8, T.slide[0] + 4]);
  const link = ramp([T.slide[0] - 12, T.slide[0] + 6], motion.draft);

  // ---- formula
  const formulaIn = frame >= T.formulaIn[0];
  const morphP = interpolate(frame, T.morph as unknown as number[], [0, 1], clampOpt);
  const box = ramp(T.box, motion.draft);
  const endmark = ramp(T.endmark, motion.draft);
  const probeDim = interpolate(frame, [T.pull[0], T.pull[1]], [1, 0.7], clampOpt);
  const readoutFade = 1 - ramp([T.pull[0], T.pull[0] + 24]);

  const FX = 1505;
  const FY = 500;
  const tipPt = project(view, sinTip, Math.sin(sinTip));
  const penPt = project(view, x0, Math.cos(x0) - D);

  return (
    <Sheet
      view={view}
      strip={{ section: "§3.1", title: "Derivatives of sine and cosine", sheet: "MOTION TEST" }}
      overlay={
        endmark > 0 ? (
          <TitleBlock right={1870} bottom={1030} dwg="§3.1" title="DERIV. OF SIN / COS" sheet="END OF TEST" reveal={endmark} />
        ) : null
      }
    >
      <ViewProvider view={view}>
        {/* 上視圖：sin */}
        <Axes xMin={XMIN} xMax={XMAX} yMin={-YR} yMax={YR} progress={axesP} xTicks={sinTicks} yLabel="" />
        <FunctionPlot fn={Math.sin} from={XMIN} to={XMAX - 0.15} progress={sinP} />
        {penOn ? <Reticle at={tipPt} readout={`x ${sinTip.toFixed(2)}`} opacity={1 - clamp01((frame - T.sinDraw[1]) / 6)} /> : null}
        <MathAt
          x={project(view, 4.05, 0.9)[0]}
          y={project(view, 4.05, 0.9)[1]}
          tex="y=\sin x"
          size={34}
          color={semantic.sin}
          anchor="l"
          opacity={ramp(T.sinLabel)}
        />

        {/* 下視圖：cos */}
        {cosAxesP > 0 ? (
          <Axes xMin={XMIN} xMax={XMAX} yMin={-YR} yMax={YR} yOff={-D} progress={cosAxesP} xTicks={[]} yLabel="" />
        ) : null}
        {sliding ? (
          <FunctionPlot fn={Math.cos} from={XMIN} to={XMAX} range={cosRange} yOff={-D} stroke={semantic.cos} />
        ) : null}
        <MathAt
          x={project(view, 4.25, 0.9 - D)[0]}
          y={project(view, 4.25, 0.9 - D)[1]}
          tex="y=\cos x"
          size={34}
          color={semantic.cos}
          anchor="l"
          opacity={ramp([T.cosRest[1] - 10, T.cosRest[1] + 8])}
        />

        {/* 切線探針 */}
        {grow > 0 ? (
          <AbsoluteFill style={{ opacity: probeDim }}>
            <SlopeProbe
              x={x0}
              grow={grow}
              triangle={tri * readoutFade}
              readout={readout * readoutFade}
              link={link}
              height={heightOn}
              halfLen={0.95}
            />
          </AbsoluteFill>
        ) : null}
        {heightOn > 0 && frame < T.pull[1] ? (
          <Reticle at={penPt} tint={semantic.cos} opacity={heightOn * (1 - ramp(T.pull))} />
        ) : null}
      </ViewProvider>

      {/* 公式區 */}
      {formulaIn && frame < T.morph[0] ? (
        <Formula
          lines={src}
          x={FX}
          y={FY}
          size={FS}
          lineGap={22}
          align="center"
          opacity={(id) => {
            const order = ["slope", "sin", "at1", "x1", "eq", "height", "cos", "at2", "x2"].indexOf(id);
            return interpolate(frame, [T.formulaIn[0] + order * 2, T.formulaIn[0] + order * 2 + 12], [0, 1], clampOpt);
          }}
        />
      ) : null}
      {frame >= T.morph[0] ? (
        <TokenMorph from={src} to={dst} x={FX} y={FY} size={FS} lineGap={22} alignFrom="center" alignTo="center" progress={morphP} pair={{ slope: "ddx" }} stagger={0.05} arc={0.3} />
      ) : null}
      {formulaIn ? (
        <>
          <Svg opacity={ramp([T.formulaIn[0], T.formulaIn[0] + 14])}>
            <line x1={1175} x2={1175} y1={FY - 190} y2={FY + 190} stroke={color.rule} strokeWidth={1} />
          </Svg>
          {[
            ["OBSERVATION", 1 - ramp([T.morph[0] + 20, T.morph[0] + 40])],
            ["RESULT", ramp([T.morph[0] + 30, T.morph[0] + 50])],
          ].map(([t, o]) => (
            <div
              key={t as string}
              style={{
                position: "absolute",
                left: 1215,
                top: FY - 190,
                color: color.ink3,
                opacity: (o as number) * ramp([T.formulaIn[0], T.formulaIn[0] + 14]),
                ...mono(18, { fontWeight: 600 }),
              }}
            >
              {t as string}
            </div>
          ))}
        </>
      ) : null}
      {box > 0 ? <CornerFrame x={FX - 282} y={FY - 84} w={564} h={168} len={24} stroke={color.accent} progress={box} /> : null}
    </Sheet>
  );
};
