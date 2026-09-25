/**
 * 「鏡頭」＝世界座標 → 螢幕座標的投影。
 * 所有幾何都在 JS 端投影成螢幕座標再畫，所以鏡頭推近時線寬、字級不變
 *（製圖線寬紀律），只有位置與間距放大。
 */
import React, { createContext, useContext } from "react";
import { interpolate, type EasingFunction } from "remotion";

export type View = {
  /** 鏡頭注視的世界座標 */
  cx: number;
  cy: number;
  /** 每一世界單位的像素 */
  s: number;
  /** 注視點落在螢幕的位置 */
  ox: number;
  oy: number;
};

export type Pt = [number, number];

export const project = (v: View, x: number, y: number): Pt => [
  v.ox + (x - v.cx) * v.s,
  v.oy - (y - v.cy) * v.s,
];

const ViewCtx = createContext<View>({ cx: 0, cy: 0, s: 100, ox: 960, oy: 540 });

export const ViewProvider: React.FC<{ view: View; children: React.ReactNode }> = ({
  view,
  children,
}) => <ViewCtx.Provider value={view}>{children}</ViewCtx.Provider>;

export const useView = () => useContext(ViewCtx);

/** 關鍵幀插值（每段各自 easing）；s 以對數插值，推拉的感知速度才均勻 */
export const cameraAt = (
  frame: number,
  keys: Array<{ f: number; v: View }>,
  easing: EasingFunction,
): View => {
  const fs = keys.map((k) => k.f);
  const opt = {
    extrapolateLeft: "clamp" as const,
    extrapolateRight: "clamp" as const,
    easing,
  };
  const pick = (sel: (v: View) => number) =>
    interpolate(
      frame,
      fs,
      keys.map((k) => sel(k.v)),
      opt,
    );
  return {
    cx: pick((v) => v.cx),
    cy: pick((v) => v.cy),
    s: Math.exp(pick((v) => Math.log(v.s))),
    ox: pick((v) => v.ox),
    oy: pick((v) => v.oy),
  };
};

/** 取樣函數成 polyline path（螢幕座標） */
export const fnPath = (
  v: View,
  f: (x: number) => number,
  x0: number,
  x1: number,
  yOff = 0,
  n = 240,
): string => {
  if (x1 <= x0) return "";
  const steps = Math.max(2, Math.round(n * Math.min(1, (x1 - x0) / 6)) + 8);
  let d = "";
  for (let i = 0; i <= steps; i++) {
    const x = x0 + ((x1 - x0) * i) / steps;
    const [px, py] = project(v, x, f(x) + yOff);
    d += `${i === 0 ? "M" : "L"}${px.toFixed(2)},${py.toFixed(2)}`;
  }
  return d;
};

export const clamp01 = (t: number) => Math.min(1, Math.max(0, t));

/** 不帶正號的讀數（−1、0、1） */
export const fmtPlain = (x: number, digits = 0) => {
  const r = Math.abs(x) < 0.5 * 10 ** -digits ? 0 : x;
  return (r < 0 ? "−" : "") + Math.abs(r).toFixed(digits);
};

/** 固定寬度讀數：+0.71 / −0.71（真正的減號、等寬） */
export const fmtSigned = (x: number, digits = 2) => {
  const r = Math.abs(x) < 0.5 * 10 ** -digits ? 0 : x;
  const s = Math.abs(r).toFixed(digits);
  return (r < 0 ? "−" : "+") + s;
};
