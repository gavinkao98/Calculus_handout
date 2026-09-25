// F1 定理陳述：兩條式子在畫面中央呼吸，以「=」對齊；背後極淡的 sin／cos 光絲當空氣。
import React from 'react';
import {color, font, safe} from '../theme';
import {SceneShell} from '../components/SceneShell';
import {makeView} from '../components/Camera';
import {FunctionPlot} from '../components/Plot';
import {MathTex} from '../components/MathTex';
import {Eyebrow} from '../components/Type';

export const THEOREM_LAYOUT = {eqX: 1000, y1: 440, y2: 720, size: 108} as const;

export const F1Theorem: React.FC = () => {
  const {eqX, y1, y2, size} = THEOREM_LAYOUT;
  const bg = makeView({cx: 0, cy: 0, zoom: 1}, 150, 960, 590);
  return (
    <SceneShell
      focus={{x: 960, y: 590}}
      stage={
        <>
          <g opacity={0.14}>
            <FunctionPlot view={bg} f={Math.sin} domain={[-7, 7]} hue="sin" strength={0.5} />
            <FunctionPlot view={bg} f={Math.cos} domain={[-7, 7]} hue="cos" strength={0.5} />
          </g>
          <MathTex id="thm_sin" size={size} x={eqX} y={y1} alignToken="eq" />
          <MathTex id="thm_cos" size={size} x={eqX} y={y2} alignToken="eq" />
        </>
      }
    >
      <Eyebrow style={{position: 'absolute', left: safe.x, top: safe.top + 8}}>Theorem · Derivatives of sine and cosine</Eyebrow>
      <div
        style={{
          position: 'absolute',
          left: 0,
          right: 0,
          top: 868,
          textAlign: 'center',
          fontFamily: font.display,
          fontStyle: 'italic',
          fontSize: 42,
          color: color.ink2,
        }}
      >
        Each one’s derivative is the other — cosine picks up a minus sign.
      </div>
    </SceneShell>
  );
};
