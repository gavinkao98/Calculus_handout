/**
 * 標題欄（工程圖右下角的 title block）：品牌 lockup＋圖號／圖名／比例／張次。
 * 用於節標題卡與片尾；reveal ∈ [0,1] 讓表格線依序畫出。
 */
import React from "react";
import { Img } from "remotion";
import lockupWhite from "../../../../../pipeline/assets/brand/lockup-white.svg";
import { color, mono, stroke } from "../theme";
import { clamp01 } from "../lib/view";
import { Svg } from "./Draft";

export const TitleBlock: React.FC<{
  right: number;
  bottom: number;
  w?: number;
  dwg: string;
  title: string;
  sheet: string;
  reveal?: number;
}> = ({ right, bottom, w = 540, dwg, title, sheet, reveal = 1 }) => {
  const logoH = 150;
  const logoW = Math.min(w - 64, 440);
  const rowH = 46;
  const h = logoH + rowH * 2;
  const x = right - w;
  const y = bottom - h;
  const r = clamp01(reveal);
  const line = (x1: number, y1: number, x2: number, y2: number, k: string, t = r) => (
    <line key={k} x1={x1} y1={y1} x2={x1 + (x2 - x1) * t} y2={y1 + (y2 - y1) * t} stroke={color.rule} strokeWidth={stroke.hair} />
  );
  const cell = (cx: number, cy: number, cw: number, cap: string, val: string, accent = false) => (
    <div
      style={{
        position: "absolute",
        left: cx + 14,
        top: cy,
        width: cw - 20,
        height: rowH,
        display: "flex",
        alignItems: "center",
        gap: 12,
        opacity: clamp01((r - 0.4) / 0.6),
        whiteSpace: "nowrap",
      }}
    >
      <span style={{ ...mono(13), color: color.ink3 }}>{cap}</span>
      <span style={{ ...mono(17, { fontWeight: 500 }), color: accent ? color.accent : color.ink2 }}>{val}</span>
    </div>
  );
  const c1 = 190;
  return (
    <>
      <Svg>
        {/* 底板由下往上擦出（蓋住下方的標題列），再畫表格線 */}
        <rect x={x} y={y + h * (1 - clamp01(r * 2.5))} width={w} height={h * clamp01(r * 2.5)} fill={color.paper} />
        {line(x, y, x + w, y, "t")}
        {line(x, y, x, y + h, "l")}
        {line(x, y + logoH, x + w, y + logoH, "m1")}
        {line(x, y + logoH + rowH, x + w, y + logoH + rowH, "m2")}
        {line(x + c1, y + logoH, x + c1, y + h, "v1")}
        <rect x={x} y={y} width={w} height={h} fill="none" stroke={color.ink} strokeOpacity={0.8 * r} strokeWidth={2} />
      </Svg>
      <Img
        src={lockupWhite}
        style={{
          position: "absolute",
          left: x + (w - logoW) / 2,
          top: y + (logoH - logoW / 3.467) / 2,
          width: logoW,
          opacity: clamp01((r - 0.3) / 0.5),
        }}
      />
      {cell(x, y + logoH, c1, "DWG", dwg, true)}
      {cell(x + c1, y + logoH, w - c1, "TITLE", title)}
      {cell(x, y + logoH + rowH, c1, "SCALE", "1 : 1")}
      {cell(x + c1, y + logoH + rowH, w - c1, "SHEET", sheet)}
    </>
  );
};
