// 發光原語：GlowDefs（濾鏡／漸層，一個 Stage 一份）、GlowPath（三層發光筆畫）、Sparkle（四角星光點，呼應 logo 的星）。
import React from 'react';
import {FRAME, glow, hue as hueOf, Hue} from '../theme';

const HUES: Hue[] = ['sin', 'cos', 'deriv', 'tangent', 'ink'];

// 濾鏡區域用 userSpaceOnUse 蓋滿整個畫面：水平切線（bbox 高度 0）用 objectBoundingBox 會整條消失。
const region = {
  filterUnits: 'userSpaceOnUse' as const,
  x: -400,
  y: -400,
  width: FRAME.width + 800,
  height: FRAME.height + 800,
};

export const GlowDefs: React.FC = () => (
  <defs>
    <filter id="dg-bloom" {...region}>
      <feGaussianBlur stdDeviation={glow.bloom.blur} />
    </filter>
    <filter id="dg-halo" {...region}>
      <feGaussianBlur stdDeviation={glow.halo.blur} />
    </filter>
    {HUES.map((h) => {
      const {main, core} = hueOf(h);
      return (
        <radialGradient key={h} id={`dg-spark-${h}`}>
          <stop offset="0%" stopColor={core} stopOpacity={0.95} />
          <stop offset="18%" stopColor={main} stopOpacity={0.55} />
          <stop offset="55%" stopColor={main} stopOpacity={0.12} />
          <stop offset="100%" stopColor={main} stopOpacity={0} />
        </radialGradient>
      );
    })}
  </defs>
);

type GlowPathProps = {
  d: string;
  hue: Hue;
  strength?: number; // 0..1+，乘在 bloom/halo 不透明度上
  width?: number; // 線寬倍率
  opacity?: number;
  dash?: string;
};

export const GlowPath: React.FC<GlowPathProps> = ({d, hue, strength = 1, width = 1, opacity = 1, dash}) => {
  const {main, core} = hueOf(hue);
  const common = {d, fill: 'none', strokeLinecap: 'round' as const, strokeLinejoin: 'round' as const, strokeDasharray: dash};
  return (
    <g opacity={opacity}>
      <path {...common} stroke={main} strokeWidth={glow.bloom.width * width} opacity={glow.bloom.opacity * strength} filter="url(#dg-bloom)" />
      <path {...common} stroke={main} strokeWidth={glow.halo.width * width} opacity={glow.halo.opacity * strength} filter="url(#dg-halo)" />
      <path {...common} stroke={core} strokeWidth={glow.core.width * width} opacity={0.35 + 0.65 * Math.min(1, strength)} />
      <path {...common} stroke={main} strokeWidth={glow.core.width * width * 0.55} opacity={0.5} />
    </g>
  );
};

/** 水平淡入遮罩：from→to（px）由黑暗浮現；reverse 則淡出。 */
export const FadeMask: React.FC<{id: string; from: number; to: number}> = ({id, from, to}) => (
  <defs>
    <linearGradient id={`${id}-g`} gradientUnits="userSpaceOnUse" x1={from} y1={0} x2={to} y2={0}>
      <stop offset="0" stopColor="#fff" stopOpacity={0} />
      <stop offset="1" stopColor="#fff" stopOpacity={1} />
    </linearGradient>
    <mask id={id} maskUnits="userSpaceOnUse" x={-400} y={-400} width={FRAME.width + 800} height={FRAME.height + 800}>
      <rect x={-400} y={-400} width={FRAME.width + 800} height={FRAME.height + 800} fill={`url(#${id}-g)`} />
    </mask>
  </defs>
);

type SparkleProps = {
  x: number;
  y: number;
  hue: Hue;
  size?: number; // 星芒半徑 px
  intensity?: number; // 0..1
  rotate?: number; // deg
};

/** 四角星光點：logo 星形的幾何語彙（細長十字＋柔光暈）。用在關鍵點、描線的筆頭。 */
export const Sparkle: React.FC<SparkleProps> = ({x, y, hue, size = 22, intensity = 1, rotate = 0}) => {
  if (intensity <= 0.001) return null;
  const {core} = hueOf(hue);
  const R = size;
  const r = size * 0.13;
  const star = `M0,${-R} L${r},${-r} L${R},0 L${r},${r} L0,${R} L${-r},${r} L${-R},0 L${-r},${-r} Z`;
  return (
    <g transform={`translate(${x},${y}) rotate(${rotate})`} opacity={intensity}>
      <circle r={size * 2.6} fill={`url(#dg-spark-${hue})`} />
      <path d={star} fill={core} opacity={0.9} />
      <circle r={size * 0.2} fill="#FFFFFF" />
    </g>
  );
};
