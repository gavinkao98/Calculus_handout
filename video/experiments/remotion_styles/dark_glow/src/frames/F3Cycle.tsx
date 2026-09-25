// F3 導數循環：sin → cos → −sin → −cos → sin 排成一條軌道，每一次 d/dx 順時針轉四分之一圈。
import React from 'react';
import {color, font, safe, type as T} from '../theme';
import {SceneShell} from '../components/SceneShell';
import {CycleRing} from '../components/Cycle';
import {MathTex} from '../components/MathTex';
import {Eyebrow, Title} from '../components/Type';

export const F3Cycle: React.FC = () => {
  const cx = 1080;
  const cy = 600;
  return (
    <SceneShell
      focus={{x: cx, y: cy}}
      focusRadius={800}
      stage={
        <>
          <CycleRing
            cx={cx}
            cy={cy}
            r={290}
            comet={0.62}
            nodes={[
              {tex: 'node_sin', hue: 'sin'},
              {tex: 'node_cos', hue: 'cos'},
              {tex: 'node_msin', hue: 'sin'},
              {tex: 'node_mcos', hue: 'cos'},
            ]}
          />
          <MathTex id="fourth" size={40} x={cx} y={cy + 12} glowAmount={0.5} opacity={0.9} />
        </>
      }
    >
      <div style={{position: 'absolute', left: safe.x, top: safe.top - 8}}>
        <Eyebrow>The derivative cycle</Eyebrow>
        <Title style={{marginTop: 20}}>
          Four derivatives,
          <br />
          and you’re home.
        </Title>
        <div style={{marginTop: 28, maxWidth: 500, fontFamily: font.display, fontStyle: 'italic', fontSize: 36, lineHeight: 1.3, color: color.ink2}}>
          Each derivative is a quarter turn; the sign flips every second step.
        </div>
      </div>
    </SceneShell>
  );
};
