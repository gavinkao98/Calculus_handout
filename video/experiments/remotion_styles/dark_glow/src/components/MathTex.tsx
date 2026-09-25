// MathTex：把建置期產好的 MathJax SVG 放進 Stage（巢狀 <svg>），token 可定址（上色、單獨顯示、單獨淡化）。
// token 外框（viewBox 座標）建置期已算好 → 對齊、morph 都不必量 DOM。
import React, {useId} from 'react';
import {TEX, TexEntry} from '../math/generated';
import {glow} from '../theme';

export type Box = {x: number; y: number; w: number; h: number}; // px，相對於畫面

export const tex = (id: string): TexEntry => {
  const e = TEX[id];
  if (!e) throw new Error(`MathTex: unknown formula "${id}" (run npm run prebuild)`);
  return e;
};

export type HAnchor = 'left' | 'center' | 'right';

/** 依錨點算出式子左上角與縮放（px）。alignToken：以該 token 的水平中心對齊 x。 */
export const layoutTex = (id: string, size: number, x: number, y: number, anchor: HAnchor = 'center', alignToken?: string) => {
  const e = tex(id);
  const s = size / 1000;
  const [vx, vy, vw, vh] = e.viewBox;
  const w = vw * s;
  const h = vh * s;
  let left = anchor === 'left' ? x : anchor === 'right' ? x - w : x - w / 2;
  if (alignToken) {
    const b = e.tokens[alignToken];
    left = x - ((b[0] + b[2]) / 2 - vx) * s;
  }
  const top = y + vy * s; // y＝基線
  const box = (k: string): Box => {
    const b = e.tokens[k];
    return {x: left + (b[0] - vx) * s, y: top + (b[1] - vy) * s, w: (b[2] - b[0]) * s, h: (b[3] - b[1]) * s};
  };
  return {left, top, w, h, s, box, entry: e};
};

type Props = {
  id: string;
  size: number; // px / em
  x: number;
  y: number; // 基線
  anchor?: HAnchor;
  alignToken?: string;
  opacity?: number;
  glowAmount?: number; // 0 = 無光暈，1 = 標準
  only?: string[]; // 只顯示這些 token
  tokenOpacity?: Record<string, number>;
  style?: React.CSSProperties;
};

export const MathTex: React.FC<Props> = ({id, size, x, y, anchor = 'center', alignToken, opacity = 1, glowAmount = 1, only, tokenOpacity, style}) => {
  const uid = 'mtx' + useId().replace(/[^a-zA-Z0-9]/g, '');
  const L = layoutTex(id, size, x, y, anchor, alignToken);
  const [vx, vy, vw, vh] = L.entry.viewBox;
  const rules: string[] = [];
  if (only) rules.push(`.${uid} [class*="tok-"]{visibility:hidden}`, ...only.map((k) => `.${uid} .tok-${k}{visibility:visible}`));
  if (tokenOpacity) for (const [k, o] of Object.entries(tokenOpacity)) rules.push(`.${uid} .tok-${k}{opacity:${o}}`);
  if (opacity <= 0.001) return null;
  return (
    <svg
      className={`mtx ${uid}`}
      x={L.left}
      y={L.top}
      width={L.w}
      height={L.h}
      viewBox={`${vx} ${vy} ${vw} ${vh}`}
      overflow="visible"
      opacity={opacity}
      style={style}
    >
      {rules.length ? <style>{rules.join('\n')}</style> : null}
      <defs>
        <filter id={`${uid}-f`} x="-30%" y="-80%" width="160%" height="260%">
          <feGaussianBlur in="SourceGraphic" stdDeviation={glow.math.bloom} result="bloom" />
          <feGaussianBlur in="SourceGraphic" stdDeviation={glow.math.blur} result="halo" />
          <feComponentTransfer in="bloom" result="bloomA">
            <feFuncA type="linear" slope={glow.math.bloomOpacity * glowAmount} />
          </feComponentTransfer>
          <feComponentTransfer in="halo" result="haloA">
            <feFuncA type="linear" slope={glow.math.haloOpacity * glowAmount} />
          </feComponentTransfer>
          <feMerge>
            <feMergeNode in="bloomA" />
            <feMergeNode in="haloA" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
      </defs>
      <g filter={glowAmount > 0 ? `url(#${uid}-f)` : undefined} dangerouslySetInnerHTML={{__html: L.entry.body}} />
    </svg>
  );
};
