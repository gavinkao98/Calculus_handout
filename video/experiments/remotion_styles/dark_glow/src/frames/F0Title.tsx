// F0 節標題卡：左側片名，右側一條從黑暗中浮現的 sin 光絲，在 x=0 處被一道切線光刃穿過——「多快？」的答案。
import React from 'react';
import {color, safe, type as T} from '../theme';
import {SceneShell} from '../components/SceneShell';
import {makeView} from '../components/Camera';
import {FunctionPlot, Tangent} from '../components/Plot';
import {FadeMask} from '../components/Glow';
import {Eyebrow, GlowWord, Title} from '../components/Type';
import {Logo} from '../components/Logo';

export const F0Title: React.FC = () => {
  const v = makeView({cx: 0, cy: 0, zoom: 1}, 210, 1300, 640);
  const tx = v.X(0);
  const ty = v.Y(0);
  return (
    <SceneShell
      focus={{x: 1300, y: 600}}
      focusRadius={1000}
      bug={0}
      stage={
        <>
          <FadeMask id="f0-fade" from={700} to={1060} />
          <g mask="url(#f0-fade)">
            <FunctionPlot view={v} f={Math.cos} domain={[-3.2, 3.3]} hue="cos" strength={0.45} opacity={0.4} />
            <FunctionPlot view={v} f={Math.sin} domain={[-3.2, 3.3]} hue="sin" strength={1.1} />
          </g>
          <Tangent view={v} x0={0} y0={0} slope={1} length={980} point={1} />
          <text x={tx + 34} y={ty + 56} fontFamily='"DM Mono", monospace' fontSize={20} letterSpacing="0.28em" fill={color.ink3}>
            TANGENT  ·  SLOPE 1
          </text>
        </>
      }
    >
      <Logo variant="lockup-white" height={132} style={{position: 'absolute', left: safe.x - 22, top: 72, opacity: 0.92}} />
      <div style={{position: 'absolute', left: safe.x, top: 356}}>
        <Eyebrow>Chapter 3 · Section 3.1</Eyebrow>
        <Title size={T.display.size} style={{marginTop: 34, lineHeight: 1.02}}>
          Derivatives of
          <br />
          <GlowWord hue="sin">Sine</GlowWord> and <GlowWord hue="cos">Cosine</GlowWord>
        </Title>
        <div style={{marginTop: 44, fontFamily: '"Cormorant Garamond", serif', fontStyle: 'italic', fontSize: T.lead.size, color: color.ink2}}>
          How fast does sine change?
        </div>
      </div>
    </SceneShell>
  );
};
