// MorphTex：token 級公式變形。配對的 token 從舊位置滑到新位置（彈簧、左到右錯開），途中交叉淡化；
// 沒配對的舊 token 先上飄淡出，沒配對的新 token 最後淡入。位置全部來自建置期的 token 外框。
import React from 'react';
import {interpolate, spring, useVideoConfig} from 'remotion';
import {ease, springs} from '../theme';
import {layoutTex, MathTex} from './MathTex';

type Side = {id: string; size: number};

type Props = {
  from: Side;
  to: Side;
  x: number; // 水平中心
  y: number; // 共同基線
  t: number; // 自變形開始起的幀數（< 0 = 尚未開始，只顯示 from）
  pairs: [string, string][]; // [fromKey, toKey]，依滑行先後排
  stagger?: number;
  glowTo?: number; // 結束後新式子的光暈量
};

const smooth = (v: number, a: number, b: number) =>
  interpolate(v, [a, b], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: ease.fade});

export const MorphTex: React.FC<Props> = ({from, to, x, y, t, pairs, stagger = 4, glowTo = 1}) => {
  const {fps} = useVideoConfig();
  const A = layoutTex(from.id, from.size, x, y);
  const B = layoutTex(to.id, to.size, x, y);
  const aKeys = Object.keys(A.entry.tokens);
  const bKeys = Object.keys(B.entry.tokens);
  const matchedA = new Set(pairs.map((p) => p[0]));
  const matchedB = new Set(pairs.map((p) => p[1]));

  if (t <= 0) return <MathTex id={from.id} size={from.size} x={x} y={y} />;

  const layers: React.ReactNode[] = [];

  // 未配對的舊 token：上飄 18px 淡出
  aKeys
    .filter((k) => !matchedA.has(k))
    .forEach((k) => {
      const q = smooth(t, 0, 14);
      layers.push(
        <g key={`a-${k}`} transform={`translate(0 ${-18 * q})`}>
          <MathTex id={from.id} size={from.size} x={x} y={y} only={[k]} opacity={1 - q} />
        </g>,
      );
    });

  // 配對 token：彈簧滑行＋交叉淡化
  pairs.forEach(([ka, kb], i) => {
    const p = spring({frame: t - 6 - i * stagger, fps, config: springs.morph});
    const a = A.box(ka);
    const b = B.box(kb);
    const acx = a.x + a.w / 2;
    const acy = a.y + a.h / 2;
    const bcx = b.x + b.w / 2;
    const bcy = b.y + b.h / 2;
    const sc = to.size / from.size;
    const s = 1 + (sc - 1) * p;
    const dx = (bcx - acx) * p;
    const dy = (bcy - acy) * p;
    // 同字形：交接在中段（幾乎看不見）；不同字形（如 "slope of" → d/dx）：早早溶掉，免得被後面滑來的 token 撞字
    const fade = ka === kb ? smooth(p, 0.25, 0.75) : smooth(p, 0.02, 0.4);
    // 舊 token：以自身中心為原點縮放並位移
    layers.push(
      <g key={`m-a-${ka}`} transform={`translate(${acx + dx} ${acy + dy}) scale(${s}) translate(${-acx} ${-acy})`}>
        <MathTex id={from.id} size={from.size} x={x} y={y} only={[ka]} opacity={1 - fade} />
      </g>,
    );
    // 新 token：從舊位置（反向變換）一路走回自己的位置
    const s2 = s / sc;
    const bdx = (acx + dx) - bcx;
    const bdy = (acy + dy) - bcy;
    layers.push(
      <g key={`m-b-${kb}`} transform={`translate(${bcx + bdx} ${bcy + bdy}) scale(${s2}) translate(${-bcx} ${-bcy})`}>
        <MathTex id={to.id} size={to.size} x={x} y={y} only={[kb]} opacity={fade} glowAmount={glowTo} />
      </g>,
    );
  });

  // 未配對的新 token：最後淡入（由下方 14px 升起）
  const last = 6 + pairs.length * stagger;
  bKeys
    .filter((k) => !matchedB.has(k))
    .forEach((k) => {
      const q = smooth(t, last + 6, last + 22);
      layers.push(
        <g key={`b-${k}`} transform={`translate(0 ${14 * (1 - q)})`}>
          <MathTex id={to.id} size={to.size} x={x} y={y} only={[k]} opacity={q} glowAmount={glowTo} />
        </g>,
      );
    });

  return <g>{layers}</g>;
};
