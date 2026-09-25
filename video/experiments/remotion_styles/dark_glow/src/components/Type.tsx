// 文字元件：Eyebrow（等寬眉標）、Title（Cormorant 片名）、Readout（儀器讀數，SVG）。
import React from 'react';
import {color, font, type as T} from '../theme';

export const Eyebrow: React.FC<{children: React.ReactNode; style?: React.CSSProperties; rule?: boolean}> = ({children, style, rule = true}) => (
  <div
    style={{
      display: 'flex',
      alignItems: 'center',
      gap: 22,
      fontFamily: font.mono,
      fontSize: T.eyebrow.size,
      fontWeight: T.eyebrow.weight,
      letterSpacing: T.eyebrow.tracking,
      textTransform: 'uppercase',
      color: color.ink2,
      ...style,
    }}
  >
    {rule ? <span style={{width: 44, height: 1.5, background: color.deriv, boxShadow: `0 0 10px ${color.deriv}`, flex: 'none'}} /> : null}
    <span>{children}</span>
  </div>
);

/** 片名／場景標題。<em> 內的字以斜體＋語意色發光（在 children 裡用 <Glow hue>）。 */
export const Title: React.FC<{children: React.ReactNode; size?: number; style?: React.CSSProperties}> = ({children, size = T.title.size, style}) => (
  <div
    style={{
      fontFamily: font.display,
      fontWeight: T.title.weight,
      fontSize: size,
      lineHeight: T.title.lineHeight,
      letterSpacing: T.title.tracking,
      color: color.ink,
      ...style,
    }}
  >
    {children}
  </div>
);

export const GlowWord: React.FC<{hue: 'sin' | 'cos' | 'deriv'; children: React.ReactNode; italic?: boolean}> = ({hue, children, italic = true}) => (
  <span
    style={{
      color: color[hue],
      fontStyle: italic ? 'italic' : 'normal',
      textShadow: `0 0 18px ${color[hue]}66, 0 0 48px ${color[hue]}33`,
    }}
  >
    {children}
  </span>
);

type ReadoutProps = {
  x: number;
  y: number; // 數字基線
  label: string;
  value: string;
  hue?: 'sin' | 'cos' | 'deriv' | 'tangent' | 'ink';
  anchor?: 'start' | 'middle' | 'end';
  opacity?: number;
  size?: number;
  /** stack：標籤在上、數字在下；inline：同一基線（標籤在左） */
  layout?: 'stack' | 'inline';
};

/**
 * 儀器讀數：DM Mono 大寫小標籤＋Cormorant 等寬襯線數字（lining＋tabular，即時變動不跳位）。
 * 數字不用 DM Mono：它的 0 帶斜線，在數學畫面上會被讀成空集合 ∅。
 * valueX 給定時數字靠右對齊在 valueX（正負號出現時數字本身不移動）。
 */
export const Readout: React.FC<ReadoutProps & {valueX?: number}> = ({x, y, label, value, hue = 'ink', anchor = 'start', opacity = 1, size = T.readout.size, layout = 'stack', valueX}) => {
  if (opacity <= 0.001) return null;
  const c = hue === 'ink' ? color.ink : color[hue];
  const valueProps = {
    fontFamily: font.display,
    fontSize: size,
    fontWeight: 500,
    fill: c,
    style: {filter: `drop-shadow(0 0 12px ${c}66)`, fontVariantNumeric: 'lining-nums tabular-nums', whiteSpace: 'pre'} as React.CSSProperties,
  };
  const labelProps = {fontFamily: font.mono, fontSize: T.readoutLabel.size, letterSpacing: T.readoutLabel.tracking, fill: color.ink2, style: {textTransform: 'uppercase' as const}};
  if (layout === 'inline') {
    return (
      <text x={x} y={y} opacity={opacity} textAnchor={anchor}>
        <tspan {...labelProps}>{label}</tspan>
        <tspan dx={12} {...valueProps}>
          {value}
        </tspan>
      </text>
    );
  }
  return (
    <g opacity={opacity} textAnchor={anchor}>
      <text x={x} y={y - size * 0.86 - 8} {...labelProps}>
        {label}
      </text>
      <text x={valueX ?? x} y={y} textAnchor={valueX !== undefined ? 'end' : anchor} {...valueProps}>
        {value}
      </text>
    </g>
  );
};

/** 兩點之間的虛線連接（光由 from 色漸變到 to 色）：把「斜率」接到「高度」。 */
export const Connector: React.FC<{x1: number; y1: number; x2: number; y2: number; from: string; to: string; opacity?: number; id: string}> = ({x1, y1, x2, y2, from, to, opacity = 1, id}) => (
  <g opacity={opacity}>
    <defs>
      <linearGradient id={id} gradientUnits="userSpaceOnUse" x1={x1} y1={y1} x2={x2 + 0.01} y2={y2}>
        <stop offset="0" stopColor={from} />
        <stop offset="1" stopColor={to} />
      </linearGradient>
    </defs>
    <line x1={x1} y1={y1} x2={x2} y2={y2} stroke={`url(#${id})`} strokeWidth={2} strokeDasharray="2 9" strokeLinecap="round" opacity={0.85} />
  </g>
);

/** 讀數格式：真減號（U+2212）、固定小數位；搭配 Readout 的 valueX 靠右對齊。 */
export const fmt = (v: number, digits = 2) => {
  const r = Math.abs(v) < 0.5 * 10 ** -digits ? 0 : v;
  return (r < 0 ? '−' : '') + Math.abs(r).toFixed(digits);
};
