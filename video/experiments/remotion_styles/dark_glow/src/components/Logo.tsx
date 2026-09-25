// 品牌 logo：原樣 inline video/pipeline/assets/brand/ 的 SVG（不改色、不重繪；深底選 white 變體）。
import React from 'react';
import {BRAND} from '../brand/generated';

const ASPECT = {'icon-white': 1, 'lockup-white': 1040 / 300} as const;

export const Logo: React.FC<{variant: keyof typeof ASPECT; height: number; style?: React.CSSProperties}> = ({variant, height, style}) => (
  <div
    className="dg-logo"
    style={{width: height * ASPECT[variant], height, ...style}}
    dangerouslySetInnerHTML={{__html: BRAND[variant]}}
  />
);
