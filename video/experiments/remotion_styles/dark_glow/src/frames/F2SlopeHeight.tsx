// F2 斜率＝高度：sin 上三道切線光刃（x = 0, π/2, π），各以虛線光接到 cos 上同一 x 的星點；
// 讀數成對出現（SLOPE 金／HEIGHT 長春花藍），數字相同。
import React from 'react';
import {color, safe, type as T} from '../theme';
import {SceneShell} from '../components/SceneShell';
import {makeView} from '../components/Camera';
import {Axes, FunctionPlot, Tangent} from '../components/Plot';
import {Sparkle} from '../components/Glow';
import {MathTex} from '../components/MathTex';
import {Connector, Eyebrow, GlowWord, Readout, Title} from '../components/Type';

const PI = Math.PI;
export const GRAPH_TICKS = {
  x: [
    {v: PI / 2, tex: 'tick_pi2'},
    {v: PI, tex: 'tick_pi'},
  ],
  y: [
    {v: 1, tex: 'tick_1'},
    {v: -1, tex: 'tick_m1'},
  ],
};

export const F2SlopeHeight: React.FC = () => {
  const v = makeView({cx: 1.6, cy: 0, zoom: 1}, 280, 960, 628);
  const pts = [0, PI / 2, PI];
  return (
    <SceneShell
      focus={{x: 960, y: 620}}
      stage={
        <>
          <Axes view={v} x={[-0.62, 3.85]} y={[-1.32, 1.32]} xTicks={GRAPH_TICKS.x} xLabelDx={-16} xLabelAnchor="right" />
          <FunctionPlot view={v} f={Math.cos} domain={[-0.5, 3.72]} hue="cos" strength={0.8} />
          <FunctionPlot view={v} f={Math.sin} domain={[-0.5, 3.72]} hue="sin" strength={1.1} />
          {pts.map((x, i) => (
            <Connector key={i} id={`f2-c${i}`} x1={v.X(x)} y1={v.Y(Math.sin(x))} x2={v.X(x)} y2={v.Y(Math.cos(x))} from={color.tangent} to={color.cos} opacity={0.7} />
          ))}
          {pts.map((x, i) => (
            <Tangent key={i} view={v} x0={x} y0={Math.sin(x)} slope={Math.cos(x)} length={330} />
          ))}
          {pts.map((x, i) => (
            <Sparkle key={i} x={v.X(x)} y={v.Y(Math.cos(x))} hue="cos" size={16} />
          ))}
          {/* x = 0 */}
          <Readout x={v.X(0) - 34} y={v.Y(0) - 34} anchor="end" label="slope" value="1" hue="deriv" />
          <Readout x={v.X(0) + 34} y={v.Y(1) - 34} anchor="start" label="height" value="1" hue="cos" layout="inline" />
          {/* x = π/2 */}
          <Readout x={v.X(PI / 2)} y={v.Y(1) - 40} anchor="middle" label="slope" value="0" hue="deriv" />
          <Readout x={v.X(PI / 2) + 36} y={v.Y(0) - 30} anchor="start" label="height" value="0" hue="cos" />
          {/* x = π */}
          <Readout x={v.X(PI) + 40} y={v.Y(0) - 30} anchor="start" label="slope" value="−1" hue="deriv" />
          <Readout x={v.X(PI)} y={v.Y(-1) + 74} anchor="middle" label="height" value="−1" hue="cos" layout="inline" />
          <MathTex id="y_sin" size={T.mathS} x={v.X(2.72)} y={v.Y(0.86)} anchor="left" />
          <MathTex id="y_cos" size={T.mathS} x={v.X(1.9)} y={v.Y(-1.02)} anchor="left" />
        </>
      }
    >
      <div style={{position: 'absolute', left: safe.x, top: safe.top - 8}}>
        <Eyebrow>Slope = height</Eyebrow>
        <Title style={{marginTop: 20}}>
          The slope of <GlowWord hue="sin">sine</GlowWord> is the height of <GlowWord hue="cos">cosine</GlowWord>
        </Title>
      </div>
    </SceneShell>
  );
};
