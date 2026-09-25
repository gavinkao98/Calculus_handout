// 15 秒共同分鏡動態測試（三個方向同一份 beat script，只比風格）。
//  0.0– 2.5s  座標軸長出 → y = sin x 描出（星光筆頭）→ 標籤
//  2.5– 4.5s  鏡頭推向 x = 0；切線光刃彈入；讀數 SLOPE 1.00
//  4.5– 8.5s  切線沿 sin 從 0 滑到 π，讀數即時；cos 上的點追同一個 x，身後描出 cos；虛線＋高度柱連接
//  8.5–10.5s  鏡頭拉遠、下移，讓出上方給公式
// 10.5–13.5s  "slope of sin at x = height of cos at x" → d/dx sin x = cos x（token 滑行／淡出）
// 13.5–15.0s  落定；品牌角標
import React from 'react';
import {interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {color, ease, safe, springs, type as T} from '../theme';
import {SceneShell} from '../components/SceneShell';
import {cameraAt, makeView} from '../components/Camera';
import {Axes, FunctionPlot, Tangent} from '../components/Plot';
import {Sparkle} from '../components/Glow';
import {MathTex} from '../components/MathTex';
import {MorphTex} from '../components/MorphTex';
import {Connector, fmt, Readout} from '../components/Type';
import {GRAPH_TICKS} from '../frames/F2SlopeHeight';

const PI = Math.PI;
const DOMAIN: [number, number] = [-1.65, 4.75];
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

// 節拍（幀）
const B = {
  axes: [0, 20],
  drawSin: [8, 64],
  sinLabel: [52, 72],
  push: [75, 128],
  tangentIn: 86,
  slopeIn: [100, 116],
  slide: [138, 250],
  follow: [132, 222],
  pull: [256, 316],
  hudOut: [252, 276],
  cosRest: [262, 312],
  words: [298, 318],
  morph: 346,
  settle: [396, 430],
} as const;

export const MotionTest: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const r = (range: readonly [number, number], e = ease.glide) => interpolate(frame, range as [number, number], [0, 1], {...clamp, easing: e});

  // ---------------- 相機
  const cam = cameraAt(frame, [
    {f: 0, cx: 1.55, cy: 0, zoom: 1},
    {f: B.push[0], cx: 1.55, cy: 0, zoom: 1.02},
    {f: B.push[1], cx: 0.3, cy: 0.42, zoom: 1.85},
    {f: B.follow[0], cx: 0.3, cy: 0.42, zoom: 1.85},
    {f: B.follow[1], cx: 1.62, cy: 0.3, zoom: 1.38},
    {f: B.pull[0], cx: 1.62, cy: 0.3, zoom: 1.38},
    {f: B.pull[1], cx: 1.57, cy: 0.98, zoom: 0.8},
    {f: 450, cx: 1.57, cy: 0.98, zoom: 0.78},
  ]);
  const v = makeView(cam, 230, 960, 560);

  // ---------------- 描線
  const axesP = r(B.axes, ease.glide);
  const sinP = r(B.drawSin, ease.draw);
  const sinHead = interpolate(frame, [B.drawSin[0], B.drawSin[0] + 4, B.drawSin[1] - 2, B.drawSin[1] + 10], [0, 1, 1, 0], clamp);
  const sinLabel = r(B.sinLabel) * (1 - r([B.push[0], B.push[0] + 16]));

  // ---------------- 切線與滑動
  const tanSpring = spring({frame: frame - B.tangentIn, fps, config: springs.pop});
  const slideT = r(B.slide, ease.slide);
  const xT = PI * slideT;
  const hudOut = r(B.hudOut, ease.fade);
  const tanOpacity = interpolate(frame, [B.tangentIn, B.tangentIn + 3], [0, 1], clamp) * (1 - hudOut);
  const slopeIn = r(B.slopeIn);
  const cosTrack = interpolate(frame, [B.slide[0] - 6, B.slide[0] + 8], [0, 1], clamp) * (1 - hudOut);

  // cos：先由追蹤點在身後描出 [0, xT]，拉遠時補齊兩側
  const rest = r(B.cosRest, ease.draw);
  const cosA = 0 + (DOMAIN[0] - 0) * rest;
  const cosB = xT + (DOMAIN[1] - xT) * rest;
  const cosVisible = frame >= B.slide[0];

  // ---------------- 公式
  const wordsIn = r(B.words);
  const settle = interpolate(frame, [B.settle[0], B.settle[0] + 10, B.settle[1]], [1, 1.7, 1.15], clamp);
  const formulaY = 318;
  const labelsBack = r([B.pull[1] - 20, B.pull[1] + 6]);

  const bug = interpolate(frame, [0, 20, 400, 430], [0, 0.5, 0.5, 0.85], clamp);
  const focus = {x: 960, y: interpolate(frame, [B.pull[0], B.pull[1]], [560, 470], {...clamp, easing: ease.camera})};

  const slope = Math.cos(xT);
  return (
    <SceneShell
      focus={focus}
      bug={bug}
      stage={
        <>
          <Axes view={v} x={[-2.1, 5.2]} y={[-1.4, 1.4]} xTicks={GRAPH_TICKS.x} yTicks={GRAPH_TICKS.y} progress={axesP} labelOpacity={r([14, 34])} />

          {/* cos 由追蹤點描出 */}
          {cosVisible ? <FunctionPlot view={v} f={Math.cos} domain={[cosA, cosB]} hue="cos" strength={0.85} progress={1} /> : null}
          <FunctionPlot view={v} f={Math.sin} domain={DOMAIN} hue="sin" progress={sinP} head={sinHead} strength={1.1} />

          {/* 連接：sin 上的切點 ↔ cos 上的點；高度柱 */}
          {cosTrack > 0 ? (
            <g opacity={cosTrack}>
              <Connector id="mt-conn" x1={v.X(xT)} y1={v.Y(Math.sin(xT))} x2={v.X(xT)} y2={v.Y(Math.cos(xT))} from={color.tangent} to={color.cos} opacity={0.75} />
              <line x1={v.X(xT)} y1={v.Y(0)} x2={v.X(xT)} y2={v.Y(Math.cos(xT))} stroke={color.cos} strokeWidth={10} opacity={0.25} filter="url(#dg-halo)" />
              <line x1={v.X(xT)} y1={v.Y(0)} x2={v.X(xT)} y2={v.Y(Math.cos(xT))} stroke={color.cosCore} strokeWidth={3} strokeLinecap="round" />
              <Sparkle x={v.X(xT)} y={v.Y(Math.cos(xT))} hue="cos" size={18} />
            </g>
          ) : null}

          <Tangent view={v} x0={xT} y0={Math.sin(xT)} slope={slope} length={1000} scale={tanSpring} opacity={tanOpacity} point={tanSpring} />

          {/* 曲線標籤（世界座標錨定、字級恆定） */}
          <MathTex id="y_sin" size={T.mathS} x={v.X(2.45)} y={v.Y(1.02)} anchor="left" opacity={sinLabel} />
          <MathTex id="y_sin" size={40} x={v.X(DOMAIN[1]) + 28} y={v.Y(Math.sin(DOMAIN[1])) + 12} anchor="left" opacity={labelsBack} />
          <MathTex id="y_cos" size={40} x={v.X(DOMAIN[1]) + 28} y={v.Y(Math.cos(DOMAIN[1])) + 12} anchor="left" opacity={labelsBack} />

          {/* 公式：文字式 → 導數式 */}
          <g opacity={wordsIn} transform={`translate(0 ${16 * (1 - wordsIn)})`}>
            <MorphTex
              from={{id: 'words', size: 60}}
              to={{id: 'deriv', size: 108}}
              x={960}
              y={formulaY}
              t={frame - B.morph}
              pairs={[
                ['slope', 'op'],
                ['sin', 'sin'],
                ['x1', 'x1'],
                ['eq', 'eq'],
                ['cos', 'cos'],
                ['x2', 'x2'],
              ]}
              glowTo={settle}
              stagger={3}
            />
          </g>

          {/* HUD 讀數（固定在畫面左上，數字不追著曲線跑） */}
          <g opacity={slopeIn * (1 - hudOut)}>
            <text x={safe.x} y={safe.top + 40} fill={color.ink3}>
              <tspan fontFamily='"DM Mono", monospace' fontSize={20} letterSpacing="0.3em">AT X =</tspan>
              <tspan dx={8} fontFamily='"Cormorant Garamond", serif' fontSize={30} fontWeight={500} fill={color.ink2} style={{fontVariantNumeric: 'lining-nums tabular-nums'}}>
                {fmt(xT)}
              </tspan>
            </text>
            <Readout x={safe.x} y={safe.top + 150} label="slope of sin" value={fmt(slope)} hue="deriv" size={56} />
            <g opacity={cosTrack}>
              <text x={safe.x + 300} y={safe.top + 146} fontFamily='"Cormorant Garamond", serif' fontSize={64} fill={color.ink2}>
                =
              </text>
              <Readout x={safe.x + 380} y={safe.top + 150} label="height of cos" value={fmt(Math.cos(xT))} hue="cos" size={56} />
            </g>
          </g>
        </>
      }
    />
  );
};
