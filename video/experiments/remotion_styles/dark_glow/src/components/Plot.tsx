// 作圖元件：Axes（髮絲座標軸，兩端淡出）、FunctionPlot（依 x 描出＋星光筆頭）、Tangent（一道光）。
// 全部吃 View（世界→畫面映射），所以相機推拉時線寬恆定。
import React, {useId} from 'react';
import {color, type as T, Hue} from '../theme';
import {View} from './Camera';
import {GlowPath, Sparkle} from './Glow';
import {MathTex} from './MathTex';

export const fnPath = (f: (x: number) => number, a: number, b: number, v: View, n = 240) => {
  if (b <= a) return '';
  let d = '';
  for (let i = 0; i <= n; i++) {
    const x = a + ((b - a) * i) / n;
    d += `${i ? 'L' : 'M'}${v.X(x).toFixed(2)},${v.Y(f(x)).toFixed(2)}`;
  }
  return d;
};

type Tick = {v: number; tex: string};

type AxesProps = {
  view: View;
  x: [number, number];
  y: [number, number];
  xTicks?: Tick[];
  yTicks?: Tick[];
  progress?: number; // 0..1：由原點向外長出
  labelOpacity?: number;
  /** x 刻度標籤相對刻度的水平位移與錨點（曲線穿過刻度正下方時，把標籤讓到一側） */
  xLabelDx?: number;
  xLabelAnchor?: 'left' | 'center' | 'right';
};

export const Axes: React.FC<AxesProps> = ({view: v, x, y, xTicks = [], yTicks = [], progress = 1, labelOpacity = 1, xLabelDx = 0, xLabelAnchor = 'center'}) => {
  const uid = 'ax' + useId().replace(/[^a-zA-Z0-9]/g, '');
  const p = progress;
  if (p <= 0) return null;
  const x0 = v.X(x[0] * p);
  const x1 = v.X(x[1] * p);
  const y0 = v.Y(y[0] * p);
  const y1 = v.Y(y[1] * p);
  const ox = v.X(0);
  const oy = v.Y(0);
  return (
    <g>
      <defs>
        <linearGradient id={`${uid}-h`} gradientUnits="userSpaceOnUse" x1={x0} y1={0} x2={x1} y2={0}>
          <stop offset="0" stopColor={color.ink} stopOpacity={0} />
          <stop offset="0.12" stopColor={color.ink} stopOpacity={0.24} />
          <stop offset="0.88" stopColor={color.ink} stopOpacity={0.24} />
          <stop offset="1" stopColor={color.ink} stopOpacity={0} />
        </linearGradient>
        <linearGradient id={`${uid}-v`} gradientUnits="userSpaceOnUse" x1={0} y1={y1} x2={0} y2={y0}>
          <stop offset="0" stopColor={color.ink} stopOpacity={0} />
          <stop offset="0.2" stopColor={color.ink} stopOpacity={0.16} />
          <stop offset="0.8" stopColor={color.ink} stopOpacity={0.16} />
          <stop offset="1" stopColor={color.ink} stopOpacity={0} />
        </linearGradient>
      </defs>
      <line x1={x0} y1={oy} x2={x1} y2={oy} stroke={`url(#${uid}-h)`} strokeWidth={1.5} />
      <line x1={ox} y1={y0} x2={ox} y2={y1} stroke={`url(#${uid}-v)`} strokeWidth={1.5} />
      {xTicks.map((t) => (
        <g key={t.tex} opacity={labelOpacity}>
          <line x1={v.X(t.v)} x2={v.X(t.v)} y1={oy - 7} y2={oy + 7} stroke={color.hairStrong} strokeWidth={1.5} />
          <MathTex id={t.tex} size={T.tick} x={v.X(t.v) + xLabelDx} y={oy + 52} anchor={xLabelAnchor} glowAmount={0} style={{color: color.ink2}} />
        </g>
      ))}
      {yTicks.map((t) => (
        <g key={t.tex} opacity={labelOpacity}>
          <line x1={ox - 7} x2={ox + 7} y1={v.Y(t.v)} y2={v.Y(t.v)} stroke={color.hairStrong} strokeWidth={1.5} />
          <MathTex id={t.tex} size={T.tick} x={ox - 18} y={v.Y(t.v) + 11} anchor="right" glowAmount={0} style={{color: color.ink2}} />
        </g>
      ))}
    </g>
  );
};

type PlotProps = {
  view: View;
  f: (x: number) => number;
  domain: [number, number];
  hue: Hue;
  progress?: number; // 0..1：依 x 由左向右描出
  strength?: number;
  head?: number; // 筆頭星光強度（描線時 1，描完淡掉）
  opacity?: number;
};

export const FunctionPlot: React.FC<PlotProps> = ({view: v, f, domain, hue, progress = 1, strength = 1, head = 0, opacity = 1}) => {
  const [a, b] = domain;
  const xe = a + (b - a) * Math.max(0, Math.min(1, progress));
  if (progress <= 0) return null;
  return (
    <g>
      <GlowPath d={fnPath(f, a, xe, v, Math.max(8, Math.round(360 * progress)))} hue={hue} strength={strength} opacity={opacity} />
      <Sparkle x={v.X(xe)} y={v.Y(f(xe))} hue={hue} size={20} intensity={head * opacity} rotate={0} />
    </g>
  );
};

type TangentProps = {
  view: View;
  x0: number;
  y0: number;
  slope: number;
  length: number; // 畫面 px（相機推拉時不變長）
  scale?: number; // 0..1+（彈簧）
  opacity?: number;
  point?: number; // 切點星光強度
  pointHue?: Hue;
};

/** 切線＝一道暖白的光刃，兩端漸細淡出；切點是一顆星。 */
export const Tangent: React.FC<TangentProps> = ({view: v, x0, y0, slope, length, scale = 1, opacity = 1, point = 1, pointHue = 'tangent'}) => {
  const uid = 'tg' + useId().replace(/[^a-zA-Z0-9]/g, '');
  const px = v.X(x0);
  const py = v.Y(y0);
  const n = Math.hypot(1, slope);
  const hl = (length / 2) * Math.max(0, scale);
  const dx = (hl * 1) / n;
  const dy = (-hl * slope) / n;
  if (opacity <= 0.001) return null;
  return (
    <g opacity={opacity}>
      <defs>
        <linearGradient id={`${uid}-g`} gradientUnits="userSpaceOnUse" x1={px - dx} y1={py - dy} x2={px + dx} y2={py + dy}>
          <stop offset="0" stopColor={color.tangent} stopOpacity={0} />
          <stop offset="0.14" stopColor={color.tangent} stopOpacity={0.95} />
          <stop offset="0.86" stopColor={color.tangent} stopOpacity={0.95} />
          <stop offset="1" stopColor={color.tangent} stopOpacity={0} />
        </linearGradient>
      </defs>
      {hl > 0.5 ? (
        <>
          <line x1={px - dx} y1={py - dy} x2={px + dx} y2={py + dy} stroke={color.tangent} strokeWidth={14} opacity={0.14} filter="url(#dg-bloom)" strokeLinecap="round" />
          <line x1={px - dx} y1={py - dy} x2={px + dx} y2={py + dy} stroke={`url(#${uid}-g)`} strokeWidth={7} opacity={0.4} filter="url(#dg-halo)" strokeLinecap="round" />
          <line x1={px - dx} y1={py - dy} x2={px + dx} y2={py + dy} stroke={`url(#${uid}-g)`} strokeWidth={2.8} strokeLinecap="round" />
        </>
      ) : null}
      <Sparkle x={px} y={py} hue={pointHue} size={18} intensity={point} />
    </g>
  );
};
