/**
 * SceneShell：一張「圖紙」。
 * 底色暈影＋紙纖維雜訊＋世界格線（隨鏡頭）＋雙線圖框與分區標記（固定）＋下緣標題列。
 */
import React from "react";
import { AbsoluteFill, Img } from "remotion";
import iconWhite from "../../../../../pipeline/assets/brand/icon-white.svg";
import { color, font, FRAME, mono, space, stroke } from "../theme";
import { project, type View } from "../lib/view";

const W = FRAME.width;
const H = FRAME.height;
const I = space.sheetInner;
const O = space.sheetOuter;

export const DEFAULT_VIEW: View = { cx: 0, cy: 0, s: 160, ox: 960, oy: 540 };

/** 世界格線：1/4 單位細格、1 單位粗格；鏡頭推近時淡入 1/8 單位格 */
export const WorldGrid: React.FC<{ view: View; opacity?: number }> = ({
  view,
  opacity = 1,
}) => {
  const lines: React.ReactNode[] = [];
  const x0 = view.cx - (view.ox - I) / view.s;
  const x1 = view.cx + (W - I - view.ox) / view.s;
  const y1 = view.cy + (view.oy - I) / view.s;
  const y0 = view.cy - (H - I - view.oy) / view.s;
  const fine = Math.min(1, Math.max(0, (view.s - 240) / 160));
  const step = fine > 0 ? 0.125 : 0.25;
  const idx = (v: number) => Math.round(v / step);
  for (let i = Math.ceil(x0 / step); i <= Math.floor(x1 / step); i++) {
    const x = i * step;
    const major = Math.abs(x - Math.round(x)) < 1e-6;
    const eighth = idx(x) % 2 !== 0 && step === 0.125;
    const [px] = project(view, x, 0);
    lines.push(
      <line
        key={`v${i}`}
        x1={px}
        x2={px}
        y1={I}
        y2={H - I}
        stroke={major ? color.gridMajor : color.gridMinor}
        strokeOpacity={eighth ? fine * 0.7 : 1}
        strokeWidth={stroke.hair}
      />,
    );
  }
  for (let j = Math.ceil(y0 / step); j <= Math.floor(y1 / step); j++) {
    const y = j * step;
    const major = Math.abs(y - Math.round(y)) < 1e-6;
    const eighth = idx(y) % 2 !== 0 && step === 0.125;
    const [, py] = project(view, 0, y);
    lines.push(
      <line
        key={`h${j}`}
        y1={py}
        y2={py}
        x1={I}
        x2={W - I}
        stroke={major ? color.gridMajor : color.gridMinor}
        strokeOpacity={eighth ? fine * 0.7 : 1}
        strokeWidth={stroke.hair}
      />,
    );
  }
  return (
    <svg
      width={W}
      height={H}
      style={{ position: "absolute", inset: 0, opacity }}
      shapeRendering="crispEdges"
    >
      {lines}
    </svg>
  );
};

/** 圖框：外細線＋內粗線，夾層放分區編號（1–8／A–D） */
const Border: React.FC = () => {
  const cols = 8;
  const rows = 4;
  const cw = (W - 2 * I) / cols;
  const rh = (H - 2 * I) / rows;
  const band = (I + O) / 2;
  const z: React.ReactNode[] = [];
  for (let c = 0; c < cols; c++) {
    const cx = I + cw * (c + 0.5);
    for (const y of [band, H - band]) {
      z.push(
        <text
          key={`c${c}${y}`}
          x={cx}
          y={y + 5}
          textAnchor="middle"
          fill={color.ink3}
          style={mono(14)}
        >
          {c + 1}
        </text>,
      );
    }
    if (c > 0) {
      const x = I + cw * c;
      z.push(
        <line key={`ct${c}`} x1={x} x2={x} y1={O} y2={I} stroke={color.rule} strokeWidth={stroke.hair} />,
        <line key={`cb${c}`} x1={x} x2={x} y1={H - I} y2={H - O} stroke={color.rule} strokeWidth={stroke.hair} />,
      );
    }
  }
  for (let r = 0; r < rows; r++) {
    const cy = I + rh * (r + 0.5);
    const L = "ABCD"[r];
    for (const x of [band, W - band]) {
      z.push(
        <text key={`r${r}${x}`} x={x} y={cy + 5} textAnchor="middle" fill={color.ink3} style={mono(14)}>
          {L}
        </text>,
      );
    }
    if (r > 0) {
      const y = I + rh * r;
      z.push(
        <line key={`rl${r}`} y1={y} y2={y} x1={O} x2={I} stroke={color.rule} strokeWidth={stroke.hair} />,
        <line key={`rr${r}`} y1={y} y2={y} x1={W - I} x2={W - O} stroke={color.rule} strokeWidth={stroke.hair} />,
      );
    }
  }
  return (
    <svg width={W} height={H} style={{ position: "absolute", inset: 0 }} shapeRendering="crispEdges">
      <rect x={O} y={O} width={W - 2 * O} height={H - 2 * O} fill="none" stroke={color.rule} strokeWidth={stroke.hair} />
      <rect x={I} y={I} width={W - 2 * I} height={H - 2 * I} fill="none" stroke={color.ink} strokeOpacity={0.8} strokeWidth={2} />
      {/* 對位中心標記（製圖紙四邊中點的三角） */}
      <path d={`M${W / 2 - 9},${O} L${W / 2 + 9},${O} L${W / 2},${O + 12} Z`} fill={color.ink3} />
      <path d={`M${W / 2 - 9},${H - O} L${W / 2 + 9},${H - O} L${W / 2},${H - O - 12} Z`} fill={color.ink3} />
      {z}
    </svg>
  );
};

/** 下緣標題列：logo｜節名｜比例｜圖號 */
export const TitleStrip: React.FC<{ section: string; title: string; sheet: string; note?: string }> = ({
  section,
  title,
  sheet,
  note = "SCALE 1:1",
}) => {
  const y = H - I - space.strip;
  const cells = [
    { w: 92 },
    { w: 0 },
    { w: 230 },
    { w: 230 },
  ];
  const xRight = W - I;
  const xs = [I, I + cells[0].w, xRight - cells[2].w - cells[3].w, xRight - cells[3].w];
  const mid = y + space.strip / 2;
  return (
    <AbsoluteFill>
      <svg width={W} height={H} style={{ position: "absolute", inset: 0 }} shapeRendering="crispEdges">
        <rect x={I} y={y} width={W - 2 * I} height={space.strip} fill={color.paper} fillOpacity={0.94} />
        <line x1={I} x2={W - I} y1={y} y2={y} stroke={color.ink} strokeOpacity={0.8} strokeWidth={2} />
        {xs.slice(1).map((x) => (
          <line key={x} x1={x} x2={x} y1={y} y2={H - I} stroke={color.rule} strokeWidth={stroke.hair} />
        ))}
      </svg>
      <Img
        src={iconWhite}
        style={{ position: "absolute", left: I + 25, top: mid - 21, width: 42, height: 42, opacity: 0.95 }}
      />
      <div
        style={{
          position: "absolute",
          left: xs[1] + 28,
          top: y,
          height: space.strip,
          display: "flex",
          alignItems: "center",
          gap: 22,
          color: color.ink2,
          ...mono(19),
        }}
      >
        <span style={{ color: color.accent, fontWeight: 600 }}>{section}</span>
        <span style={{ textTransform: "uppercase" }}>{title}</span>
      </div>
      {[note, sheet].map((t, i) => (
        <div
          key={t}
          style={{
            position: "absolute",
            left: xs[2 + i],
            width: cells[2 + i].w,
            top: y,
            height: space.strip,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            color: color.ink3,
            ...mono(18),
          }}
        >
          {t}
        </div>
      ))}
    </AbsoluteFill>
  );
};

/** 紙面：暈影＋纖維雜訊 */
const Paper: React.FC = () => (
  <>
    <AbsoluteFill
      style={{
        background: `radial-gradient(120% 95% at 42% 38%, ${color.paperLift} 0%, ${color.paper} 52%, ${color.paperDeep} 100%)`,
      }}
    />
    <svg width={W} height={H} style={{ position: "absolute", inset: 0, opacity: 0.22, mixBlendMode: "soft-light" }}>
      <filter id="fiber">
        <feTurbulence type="fractalNoise" baseFrequency="0.0035 0.006" numOctaves={3} seed={7} />
        <feColorMatrix type="saturate" values="0" />
      </filter>
      <rect width={W} height={H} filter="url(#fiber)" />
    </svg>
  </>
);

export const Sheet: React.FC<{
  view?: View;
  gridOpacity?: number;
  strip?: { section: string; title: string; sheet: string; note?: string } | null;
  children?: React.ReactNode;
  /** 疊在標題列之上的層（片尾標題欄等） */
  overlay?: React.ReactNode;
}> = ({ view = DEFAULT_VIEW, gridOpacity = 1, strip, children, overlay }) => (
  <AbsoluteFill style={{ backgroundColor: color.paper, fontFamily: font.text, color: color.ink }}>
    <Paper />
    <WorldGrid view={view} opacity={gridOpacity} />
    {/* 世界內容裁切在內框之內 */}
    <AbsoluteFill style={{ clipPath: `inset(${I}px)` }}>{children}</AbsoluteFill>
    {strip ? <TitleStrip {...strip} /> : null}
    {overlay}
    <Border />
  </AbsoluteFill>
);
