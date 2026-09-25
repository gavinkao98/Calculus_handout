/**
 * MathTex：KaTeX 排版（本地字型）＋可逐 token 定址的公式。
 * - <Tex>：單段 TeX
 * - <MathAt>：放在螢幕座標上的 TeX 標籤
 * - <TokenMorph>：兩種排版之間的 token 變形（同 id 滑行、不同內容交叉淡化、無對應者淡出／淡入）
 * - <Formula>：靜態 token 排版，並回報每個 token 的方框（供引線註記對位）
 */
import katex from "katex";
import React, { useLayoutEffect, useMemo, useRef, useState } from "react";
import { continueRender, delayRender, Easing, interpolate } from "remotion";
import { fontsReady } from "../fonts";
import { color, font } from "../theme";
import { clamp01 } from "../lib/view";

const cache = new Map<string, string>();
export const texHtml = (tex: string) => {
  let h = cache.get(tex);
  if (!h) {
    h = katex.renderToString(tex, { throwOnError: false, output: "html" });
    cache.set(tex, h);
  }
  return h;
};

export const Tex: React.FC<{ tex: string; size: number; color?: string; style?: React.CSSProperties }> = ({
  tex,
  size,
  color: c = color.ink,
  style,
}) => (
  <span
    style={{ fontSize: size, color: c, lineHeight: 1, display: "inline-block", ...style }}
    dangerouslySetInnerHTML={{ __html: texHtml(tex) }}
  />
);

type Anchor = "c" | "t" | "b" | "l" | "r" | "tl" | "tr" | "bl" | "br";
const anchorShift: Record<Anchor, [string, string]> = {
  c: ["-50%", "-50%"],
  t: ["-50%", "0%"],
  b: ["-50%", "-100%"],
  l: ["0%", "-50%"],
  r: ["-100%", "-50%"],
  tl: ["0%", "0%"],
  tr: ["-100%", "0%"],
  bl: ["0%", "-100%"],
  br: ["-100%", "-100%"],
};

export const MathAt: React.FC<{
  x: number;
  y: number;
  tex: string;
  size?: number;
  color?: string;
  anchor?: Anchor;
  opacity?: number;
  bg?: string;
}> = ({ x, y, tex, size = 28, color: c = color.ink2, anchor = "c", opacity = 1, bg }) => {
  const [ax, ay] = anchorShift[anchor];
  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        transform: `translate(${ax}, ${ay})`,
        opacity,
        whiteSpace: "nowrap",
        background: bg,
        padding: bg ? "2px 6px" : undefined,
      }}
    >
      <Tex tex={tex} size={size} color={c} />
    </div>
  );
};

// ---------------------------------------------------------------- tokens

export type Tok = {
  id: string;
  tex?: string;
  text?: string;
  color?: string;
  /** 文字 token 的字體 */
  face?: "text" | "mono" | "display";
  italic?: boolean;
  /** 與前一個 token 的額外間距（em） */
  gap?: number;
  weight?: number;
};

const TokenInner: React.FC<{ t: Tok; size: number }> = ({ t, size }) => {
  if (t.tex !== undefined) return <Tex tex={t.tex} size={size} color={t.color ?? color.ink} />;
  const fam = t.face === "mono" ? font.mono : t.face === "display" ? font.display : font.text;
  return (
    <span
      style={{
        fontFamily: fam,
        fontSize: size * (t.face === "mono" ? 0.62 : t.face === "display" ? 0.86 : 0.8),
        fontStyle: t.italic ? "italic" : "normal",
        fontWeight: t.weight ?? (t.face === "display" ? 500 : 400),
        letterSpacing: t.face === "mono" ? "0.06em" : t.face === "display" ? "0.02em" : undefined,
        textTransform: t.face === "mono" || t.face === "display" ? "uppercase" : undefined,
        color: t.color ?? color.ink,
        lineHeight: 1,
      }}
    >
      {t.text}
    </span>
  );
};

type Box = { x: number; y: number; w: number; h: number };
type Layout = { boxes: Record<string, Box>; w: number; h: number };

/** 隱藏量測：把 lines 用 flex 排好，量出每個 token 相對區塊左上角的方框 */
const useLayout = (lines: Tok[][], size: number, lineGap: number, align: "left" | "center") => {
  const ref = useRef<HTMLDivElement>(null);
  const [handle] = useState(() => delayRender("Measuring formula"));
  const [layout, setLayout] = useState<Layout | null>(null);
  const key = JSON.stringify(lines) + size + lineGap + align;
  useLayoutEffect(() => {
    let alive = true;
    fontsReady.then(() => {
      if (!alive || !ref.current) return;
      const root = ref.current;
      const boxes: Record<string, Box> = {};
      root.querySelectorAll<HTMLElement>("[data-tok]").forEach((el) => {
        boxes[el.dataset.tok as string] = {
          x: el.offsetLeft,
          y: el.offsetTop,
          w: el.offsetWidth,
          h: el.offsetHeight,
        };
      });
      setLayout({ boxes, w: root.offsetWidth, h: root.offsetHeight });
      continueRender(handle);
    });
    return () => {
      alive = false;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [key]);
  const probe = (
    <div
      ref={ref}
      style={{
        position: "absolute",
        left: 0,
        top: 0,
        visibility: "hidden",
        display: "flex",
        flexDirection: "column",
        alignItems: align === "center" ? "center" : "flex-start",
        rowGap: lineGap,
        width: "max-content",
      }}
    >
      {lines.map((line, li) => (
        <div key={li} style={{ display: "flex", alignItems: "baseline", whiteSpace: "nowrap" }}>
          {line.map((t, i) => (
            <span
              key={t.id}
              data-tok={t.id}
              style={{ marginLeft: i === 0 ? 0 : `${t.gap ?? 0.28}em`, fontSize: size, lineHeight: 1, display: "inline-block" }}
            >
              <TokenInner t={t} size={size} />
            </span>
          ))}
        </div>
      ))}
    </div>
  );
  return { layout, probe };
};

const origin = (l: Layout, x: number, y: number, align: "left" | "center") =>
  align === "center" ? [x - l.w / 2, y - l.h / 2] : [x, y - l.h / 2];

/** 靜態公式：children(boxes) 拿到每個 token 的螢幕方框 */
export const Formula: React.FC<{
  lines: Tok[][];
  x: number;
  y: number;
  size: number;
  lineGap?: number;
  align?: "left" | "center";
  opacity?: (id: string) => number;
  children?: (boxes: Record<string, Box>) => React.ReactNode;
}> = ({ lines, x, y, size, lineGap = 0, align = "left", opacity, children }) => {
  const { layout, probe } = useLayout(lines, size, lineGap, align);
  const all = lines.flat();
  if (!layout) return probe;
  const [ox, oy] = origin(layout, x, y, align);
  const screen: Record<string, Box> = {};
  for (const [id, b] of Object.entries(layout.boxes)) screen[id] = { ...b, x: b.x + ox, y: b.y + oy };
  return (
    <>
      {probe}
      {all.map((t) => {
        const b = screen[t.id];
        return (
          <div
            key={t.id}
            style={{ position: "absolute", left: b.x, top: b.y, fontSize: size, lineHeight: 1, opacity: opacity ? opacity(t.id) : 1 }}
          >
            <TokenInner t={t} size={size} />
          </div>
        );
      })}
      {children ? children(screen) : null}
    </>
  );
};

/**
 * Token 變形。progress 0→1。
 * pair：from 的 id → to 的 id（未列出者以相同 id 配對）。
 */
export const TokenMorph: React.FC<{
  from: Tok[][];
  to: Tok[][];
  x: number;
  y: number;
  size: number;
  progress: number;
  pair?: Record<string, string>;
  lineGap?: number;
  alignFrom?: "left" | "center";
  alignTo?: "left" | "center";
  stagger?: number;
  arc?: number;
}> = ({ from, to, x, y, size, progress, pair = {}, lineGap = 0, alignFrom = "center", alignTo = "center", stagger = 0.06, arc = 0.25 }) => {
  const A = useLayout(from, size, lineGap, alignFrom);
  const B = useLayout(to, size, 0, alignTo);
  const fromToks = from.flat();
  const toToks = to.flat();
  const toById = useMemo(() => Object.fromEntries(toToks.map((t) => [t.id, t])), [toToks]);
  if (!A.layout || !B.layout)
    return (
      <>
        {A.probe}
        {B.probe}
      </>
    );
  const [ax, ay] = origin(A.layout, x, y, alignFrom);
  const [bx, by] = origin(B.layout, x, y, alignTo);
  const centerOf = (b: Box, ox: number, oy: number) => [ox + b.x + b.w / 2, oy + b.y + b.h / 2];
  const n = fromToks.length;
  const span = 1 - stagger * (n - 1);
  const ease = Easing.bezier(0.65, 0, 0.3, 1);
  const matchedTo = new Set<string>();
  const nodes: React.ReactNode[] = [];

  fromToks.forEach((t, i) => {
    const tid = pair[t.id] ?? t.id;
    const target = toById[tid];
    const local = clamp01((progress - i * stagger) / span);
    const e = ease(local);
    const [fx, fy] = centerOf(A.layout!.boxes[t.id], ax, ay);
    if (target) {
      matchedTo.add(tid);
      const [tx, ty] = centerOf(B.layout!.boxes[tid], bx, by);
      const cx = fx + (tx - fx) * e;
      const cy = fy + (ty - fy) * e - Math.sin(Math.PI * e) * arc * size;
      const same = (t.tex ?? t.text) === (target.tex ?? target.text) && t.color === target.color;
      if (same) {
        nodes.push(
          <div key={`m-${t.id}`} style={{ position: "absolute", left: cx, top: cy, transform: "translate(-50%,-50%)", lineHeight: 1, fontSize: size }}>
            <TokenInner t={t} size={size} />
          </div>,
        );
      } else {
        // 內容不同：原 token 縮小淡出、新 token 由 0.7 放大淡入，兩者共用滑行中心
        const kOut = interpolate(e, [0, 1], [1, 0.8]);
        const kIn = interpolate(e, [0, 1], [0.7, 1]);
        nodes.push(
          <div
            key={`x-${t.id}`}
            style={{
              position: "absolute",
              left: cx,
              top: cy,
              transform: `translate(-50%,-50%) scale(${kOut})`,
              opacity: 1 - clamp01((e - 0.1) / 0.45),
              lineHeight: 1,
              fontSize: size,
              filter: `blur(${Math.sin(Math.PI * e) * 2}px)`,
            }}
          >
            <TokenInner t={t} size={size} />
          </div>,
          <div
            key={`y-${tid}`}
            style={{
              position: "absolute",
              left: cx,
              top: cy,
              transform: `translate(-50%,-50%) scale(${kIn})`,
              opacity: clamp01((e - 0.35) / 0.5),
              lineHeight: 1,
              fontSize: size,
              filter: `blur(${Math.sin(Math.PI * e) * 2}px)`,
            }}
          >
            <TokenInner t={target} size={size} />
          </div>,
        );
      }
    } else {
      // 無對應：原地淡出，微微下沉
      const o = 1 - clamp01(local / 0.45);
      nodes.push(
        <div
          key={`o-${t.id}`}
          style={{
            position: "absolute",
            left: fx,
            top: fy + (1 - o) * 0.18 * size,
            transform: "translate(-50%,-50%)",
            opacity: o,
            lineHeight: 1,
            fontSize: size,
          }}
        >
          <TokenInner t={t} size={size} />
        </div>,
      );
    }
  });
  toToks.forEach((t) => {
    if (matchedTo.has(t.id)) return;
    const o = clamp01((progress - 0.55) / 0.4);
    const [tx, ty] = centerOf(B.layout!.boxes[t.id], bx, by);
    nodes.push(
      <div
        key={`i-${t.id}`}
        style={{ position: "absolute", left: tx, top: ty - (1 - o) * 0.18 * size, transform: "translate(-50%,-50%)", opacity: o, lineHeight: 1, fontSize: size }}
      >
        <TokenInner t={t} size={size} />
      </div>,
    );
  });
  return (
    <>
      {A.probe}
      {B.probe}
      {nodes}
    </>
  );
};

/** 取得 TokenMorph 目標排版的外框（畫結果框用） */
export const useMeasuredBlock = (lines: Tok[][], size: number, align: "left" | "center" = "center") => {
  const { layout, probe } = useLayout(lines, size, 0, align);
  return { layout, probe };
};
