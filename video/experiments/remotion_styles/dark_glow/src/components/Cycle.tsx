// CycleRing：四個節點排在一條「軌道」上，每一步 d/dx＝順時針四分之一圈；彗星沿軌道走。
import React from 'react';
import {color, hue as hueOf, type as T, Hue} from '../theme';
import {Sparkle} from './Glow';
import {MathTex} from './MathTex';

export type CycleNode = {tex: string; hue: Hue};

type Props = {
  cx: number;
  cy: number;
  r: number;
  nodes: CycleNode[]; // 由頂端開始順時針
  arcs?: number; // 已畫出的弧數（可為小數：0..4）
  comet?: number; // 彗星位置（0..4，單位＝弧）；< 0 不顯示
  nodeSize?: number;
  labelTex?: string;
};

const GAP_H = 21; // 頂／底節點（字寬）處的缺口角度
const GAP_V = 11; // 左／右節點處

const arcRange = (i: number) => {
  const a0 = -90 + i * 90;
  const start = a0 + (i % 2 === 0 ? GAP_H : GAP_V);
  const end = a0 + 90 - (i % 2 === 0 ? GAP_V : GAP_H);
  return [start, end] as const;
};

const pt = (cx: number, cy: number, r: number, deg: number) => {
  const t = (deg * Math.PI) / 180;
  return [cx + r * Math.cos(t), cy + r * Math.sin(t)] as const;
};

export const CycleRing: React.FC<Props> = ({cx, cy, r, nodes, arcs = 4, comet = -1, nodeSize = T.mathM, labelTex = 'ddx'}) => {
  const pos = [
    [cx, cy - r],
    [cx + r, cy],
    [cx, cy + r],
    [cx - r, cy],
  ];
  return (
    <g>
      <circle cx={cx} cy={cy} r={r} fill="none" stroke={color.ink} strokeOpacity={0.07} strokeWidth={1.5} />
      {[0, 1, 2, 3].map((i) => {
        const p = Math.max(0, Math.min(1, arcs - i));
        if (p <= 0) return null;
        const [s, e0] = arcRange(i);
        const e = s + (e0 - s) * p;
        const [x1, y1] = pt(cx, cy, r, s);
        const [x2, y2] = pt(cx, cy, r, e);
        const d = `M${x1},${y1} A${r},${r} 0 0 1 ${x2},${y2}`;
        const from = hueOf(nodes[i].hue).main;
        const to = hueOf(nodes[(i + 1) % 4].hue).main;
        // 箭頭：沿切線方向的細 V
        const t = (e * Math.PI) / 180;
        const tx = -Math.sin(t);
        const ty = Math.cos(t);
        const nx = Math.cos(t);
        const ny = Math.sin(t);
        const ah = 16;
        const arrow = `M${x2 - tx * ah + nx * ah * 0.55},${y2 - ty * ah + ny * ah * 0.55} L${x2},${y2} L${x2 - tx * ah - nx * ah * 0.55},${y2 - ty * ah - ny * ah * 0.55}`;
        const [lx, ly] = pt(cx, cy, r + 58, -45 + i * 90);
        return (
          <g key={i}>
            <defs>
              <linearGradient id={`cyc-${i}`} gradientUnits="userSpaceOnUse" x1={x1} y1={y1} x2={x2} y2={y2}>
                <stop offset="0" stopColor={from} />
                <stop offset="1" stopColor={to} />
              </linearGradient>
            </defs>
            <path d={d} fill="none" stroke={`url(#cyc-${i})`} strokeWidth={16} opacity={0.22} filter="url(#dg-bloom)" strokeLinecap="round" />
            <path d={d} fill="none" stroke={`url(#cyc-${i})`} strokeWidth={6} opacity={0.5} filter="url(#dg-halo)" strokeLinecap="round" />
            <path d={d} fill="none" stroke={`url(#cyc-${i})`} strokeWidth={2.6} strokeLinecap="round" />
            {p > 0.98 ? <path d={arrow} fill="none" stroke={to} strokeWidth={2.6} strokeLinecap="round" strokeLinejoin="round" /> : null}
            <MathTex id={labelTex} size={30} x={lx} y={ly + 10} opacity={p * 0.8} glowAmount={0.4} />
          </g>
        );
      })}
      {nodes.map((n, i) => (
        <MathTex key={i} id={n.tex} size={nodeSize} x={pos[i][0]} y={pos[i][1] + nodeSize * 0.22} />
      ))}
      {comet >= 0
        ? (() => {
            const i = Math.floor(comet) % 4;
            const [s, e] = arcRange(i);
            const deg = s + (e - s) * (comet - Math.floor(comet));
            const [x, y] = pt(cx, cy, r, deg);
            // 尾巴：沿軌道往回、逐段變細變淡的弧（連續筆畫，不是珠串）
            const N = 18;
            const trail = Array.from({length: N}, (_, k) => {
              const d0 = deg - k * 1.6;
              const d1 = deg - (k + 1) * 1.6;
              const [ax, ay] = pt(cx, cy, r, d0);
              const [bx, by] = pt(cx, cy, r, d1);
              const f = 1 - k / N;
              return <path key={k} d={`M${ax},${ay} A${r},${r} 0 0 0 ${bx},${by}`} stroke={hueOf('deriv').core} strokeWidth={6 * f} strokeLinecap="round" opacity={0.55 * f * f} fill="none" />;
            });
            return (
              <g>
                {trail}
                <Sparkle x={x} y={y} hue="deriv" size={22} rotate={deg + 90} />
              </g>
            );
          })()
        : null}
    </g>
  );
};
