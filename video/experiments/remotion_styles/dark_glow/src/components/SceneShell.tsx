// SceneShell：夜空底（焦點微光＋暗角＋細顆粒）＋ 全畫面 Stage SVG ＋ HTML 疊層 ＋ 品牌角標。
// 每個場景／風格幀都包在這裡，背景與 logo 位置因此一致可繼承。
import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {color, FRAME} from '../theme';
import {GlowDefs} from './Glow';
import {Logo} from './Logo';

type Props = {
  /** 夜空微光的焦點（px），通常放在畫面主角後方 */
  focus?: {x: number; y: number};
  focusRadius?: number;
  /** 右下角品牌角標（icon-white）不透明度；0 = 不顯示 */
  bug?: number;
  /** SVG 內容（座標＝畫面 px） */
  stage?: React.ReactNode;
  /** HTML 疊層（標題、眉標等文字） */
  children?: React.ReactNode;
};

const TOKEN_CSS = `
.mtx .tok-sin{color:${color.sin}}
.mtx .tok-cos{color:${color.cos}}
.mtx .tok-op{color:${color.deriv}}
.mtx .tok-eq,.mtx .tok-neg{color:${color.ink}}
.mtx .tok-dim{color:${color.ink2}}
.mtx .tok-slope,.mtx .tok-height,.mtx .tok-at1,.mtx .tok-at2,.mtx .tok-x1,.mtx .tok-x2{color:${color.ink}}
.dg-logo svg{width:100%;height:100%;display:block}
`;

export const SceneShell: React.FC<Props> = ({focus = {x: 960, y: 560}, focusRadius = 900, bug = 0.55, stage, children}) => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{backgroundColor: color.bg, overflow: 'hidden'}}>
      <style>{TOKEN_CSS}</style>
      {/* 夜空微光：焦點處略帶藍的抬升，讓純黑有深度 */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(${focusRadius}px ${focusRadius * 0.62}px at ${focus.x}px ${focus.y}px, ${color.bgLift} 0%, rgba(20,26,42,0.45) 45%, rgba(7,8,12,0) 100%)`,
        }}
      />
      <svg width={FRAME.width} height={FRAME.height} viewBox={`0 0 ${FRAME.width} ${FRAME.height}`} style={{position: 'absolute', inset: 0, overflow: 'visible'}}>
        <GlowDefs />
        {stage}
      </svg>
      <AbsoluteFill>{children}</AbsoluteFill>
      {/* 暗角 */}
      <AbsoluteFill style={{background: 'radial-gradient(ellipse 75% 70% at 50% 50%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.55) 100%)', pointerEvents: 'none'}} />
      {/* 細顆粒：抖色防止暗部色帶，也給一點膠片質地（每 2 幀換種子） */}
      <svg width={FRAME.width} height={FRAME.height} style={{position: 'absolute', inset: 0, opacity: 0.045, mixBlendMode: 'screen', pointerEvents: 'none'}}>
        <filter id="dg-grain">
          <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves={2} seed={Math.floor(frame / 2) % 97} />
          <feColorMatrix type="saturate" values="0" />
        </filter>
        <rect width="100%" height="100%" filter="url(#dg-grain)" />
      </svg>
      {bug > 0 ? <Logo variant="icon-white" height={46} style={{position: 'absolute', right: 60, bottom: 50, opacity: bug}} /> : null}
    </AbsoluteFill>
  );
};
