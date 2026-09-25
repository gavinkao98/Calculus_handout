/**
 * 製圖語彙原件：箭頭、尺寸線、引線註記、編號氣球、繪圖頭（reticle）。
 * 每個原件自帶一層全幅 SVG（螢幕座標），可直接疊放；progress ∈ [0,1] 控制描繪進度。
 */
import React from "react";
import { color, font, FRAME, mono, stroke } from "../theme";
import { clamp01, type Pt } from "../lib/view";

export const Svg: React.FC<{ children: React.ReactNode; opacity?: number; style?: React.CSSProperties }> = ({
  children,
  opacity = 1,
  style,
}) => (
  <svg
    width={FRAME.width}
    height={FRAME.height}
    style={{ position: "absolute", inset: 0, overflow: "visible", opacity, ...style }}
  >
    {children}
  </svg>
);

/** 細長實心箭頭（製圖 3:1），tip 為箭尖，dir 為指向 */
export const Arrowhead: React.FC<{ tip: Pt; dir: Pt; fill?: string; len?: number; half?: number; opacity?: number }> = ({
  tip,
  dir,
  fill = color.ink,
  len = 17,
  half = 4.2,
  opacity = 1,
}) => {
  const m = Math.hypot(dir[0], dir[1]) || 1;
  const ux = dir[0] / m;
  const uy = dir[1] / m;
  const bx = tip[0] - ux * len;
  const by = tip[1] - uy * len;
  const d = `M${tip[0]},${tip[1]} L${bx - uy * half},${by + ux * half} L${bx + uy * half},${by - ux * half} Z`;
  return <path d={d} fill={fill} opacity={opacity} />;
};

const monoWidth = (text: string, size: number) => text.length * size * (0.6 + 0.08);

/**
 * 尺寸線：p1→p2 的量測，往法線方向 offset 像素；延伸線＋雙箭頭＋中斷處置中的水平讀數
 *（單向標註法：文字一律水平）。
 */
export const DimensionLine: React.FC<{
  p1: Pt;
  p2: Pt;
  offset?: number;
  label?: string;
  labelColor?: string;
  lineColor?: string;
  size?: number;
  progress?: number;
  textOpacity?: number;
  /** 讀數放在線外側（短尺寸用） */
  labelOutside?: Pt;
}> = ({
  p1,
  p2,
  offset = 0,
  label,
  labelColor = color.ink,
  lineColor = color.ink3,
  size = 22,
  progress = 1,
  textOpacity = 1,
  labelOutside,
}) => {
  const dx = p2[0] - p1[0];
  const dy = p2[1] - p1[1];
  const L = Math.hypot(dx, dy);
  if (L < 0.5) return null;
  const ux = dx / L;
  const uy = dy / L;
  const nx = -uy;
  const ny = ux;
  const a: Pt = [p1[0] + nx * offset, p1[1] + ny * offset];
  const b: Pt = [p2[0] + nx * offset, p2[1] + ny * offset];
  const mid: Pt = [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2];
  const ext = clamp01(progress / 0.3);
  const grow = clamp01((progress - 0.15) / 0.85);
  const w = label ? monoWidth(label, size) : 0;
  const gap = label && !labelOutside ? Math.abs(ux) * (w + 18) + Math.abs(uy) * (size + 16) : 0;
  const half = (L / 2) * grow;
  const showGap = gap > 0 && gap < L - 30;
  const segs: Array<[Pt, Pt]> = showGap
    ? [
        [
          [mid[0] - ux * half, mid[1] - uy * half],
          [mid[0] - ux * Math.min(half, gap / 2), mid[1] - uy * Math.min(half, gap / 2)],
        ],
        [
          [mid[0] + ux * Math.min(half, gap / 2), mid[1] + uy * Math.min(half, gap / 2)],
          [mid[0] + ux * half, mid[1] + uy * half],
        ],
      ]
    : [
        [
          [mid[0] - ux * half, mid[1] - uy * half],
          [mid[0] + ux * half, mid[1] + uy * half],
        ],
      ];
  const sgn = offset >= 0 ? 1 : -1;
  const extLine = (p: Pt, key: string) =>
    Math.abs(offset) > 2 ? (
      <line
        key={key}
        x1={p[0] + nx * sgn * 6}
        y1={p[1] + ny * sgn * 6}
        x2={p[0] + nx * (offset + sgn * 10) * ext}
        y2={p[1] + ny * (offset + sgn * 10) * ext}
        stroke={lineColor}
        strokeWidth={stroke.thin}
      />
    ) : null;
  const arrowsOn = grow > 0.98 && L > 40;
  const lp = labelOutside ?? mid;
  return (
    <Svg>
      {extLine(p1, "e1")}
      {extLine(p2, "e2")}
      {segs.map(([s, e], i) => (
        <line key={i} x1={s[0]} y1={s[1]} x2={e[0]} y2={e[1]} stroke={lineColor} strokeWidth={stroke.thin} />
      ))}
      {arrowsOn ? (
        <>
          <Arrowhead tip={a} dir={[-ux, -uy]} fill={lineColor} len={14} half={3.6} />
          <Arrowhead tip={b} dir={[ux, uy]} fill={lineColor} len={14} half={3.6} />
        </>
      ) : null}
      {label ? (
        <text
          x={lp[0]}
          y={lp[1] + size * 0.36}
          textAnchor="middle"
          fill={labelColor}
          opacity={textOpacity * clamp01((progress - 0.5) / 0.4)}
          style={mono(size, { fontWeight: 500 })}
        >
          {label}
        </text>
      ) : null}
    </Svg>
  );
};

/**
 * 引線註記：錨點小圓 → 斜引線 → 水平擱板，文字坐在擱板上。
 * children 為 HTML（可放 KaTeX），會對齊擱板。
 */
export const Callout: React.FC<{
  anchor: Pt;
  elbow: Pt;
  shelf: number;
  side?: "right" | "left";
  lineColor?: string;
  progress?: number;
  children?: React.ReactNode;
  textStyle?: React.CSSProperties;
  dot?: boolean;
}> = ({ anchor, elbow, shelf, side = "right", lineColor = color.ink2, progress = 1, children, textStyle, dot = true }) => {
  const p1 = clamp01(progress / 0.45);
  const p2 = clamp01((progress - 0.45) / 0.3);
  const pt = clamp01((progress - 0.55) / 0.45);
  const ex = anchor[0] + (elbow[0] - anchor[0]) * p1;
  const ey = anchor[1] + (elbow[1] - anchor[1]) * p1;
  const dir = side === "right" ? 1 : -1;
  const sx = elbow[0] + dir * shelf * p2;
  return (
    <>
      <Svg>
        {dot ? <circle cx={anchor[0]} cy={anchor[1]} r={4} fill={lineColor} opacity={clamp01(progress * 6)} /> : null}
        <line x1={anchor[0]} y1={anchor[1]} x2={ex} y2={ey} stroke={lineColor} strokeWidth={stroke.thin} />
        {p2 > 0 ? (
          <line x1={elbow[0]} y1={elbow[1]} x2={sx} y2={elbow[1]} stroke={lineColor} strokeWidth={stroke.thin} />
        ) : null}
      </Svg>
      <div
        style={{
          position: "absolute",
          left: side === "right" ? elbow[0] + 6 : undefined,
          right: side === "left" ? FRAME.width - elbow[0] + 6 : undefined,
          bottom: FRAME.height - elbow[1] + 8,
          opacity: pt,
          translate: `0px ${(1 - pt) * 10}px`,
          whiteSpace: "nowrap",
          color: color.ink,
          ...textStyle,
        }}
      >
        {children}
      </div>
    </>
  );
};

/** 編號氣球（BOM 項次）：圓圈＋字母 */
export const Balloon: React.FC<{ at: Pt; label: string; r?: number; stroke?: string; fill?: string; progress?: number }> = ({
  at,
  label,
  r = 20,
  stroke: sc = color.ink,
  fill = color.paper,
  progress = 1,
}) => {
  const p = clamp01(progress);
  return (
    <Svg>
      <circle
        cx={at[0]}
        cy={at[1]}
        r={r}
        fill={fill}
        stroke={sc}
        strokeWidth={1.6}
        strokeDasharray={`${2 * Math.PI * r * p} 999`}
        transform={`rotate(-90 ${at[0]} ${at[1]})`}
      />
      <text
        x={at[0]}
        y={at[1] + 7}
        textAnchor="middle"
        fill={sc}
        opacity={clamp01((p - 0.6) / 0.4)}
        style={{ fontFamily: font.mono, fontSize: 20, fontWeight: 600 }}
      >
        {label}
      </text>
    </Svg>
  );
};

/** 繪圖頭：十字準星＋座標讀數（筆尖正在畫的位置） */
export const Reticle: React.FC<{
  at: Pt;
  tint?: string;
  opacity?: number;
  readout?: string;
  readoutSide?: "right" | "left";
}> = ({ at, tint = color.ink, opacity = 1, readout, readoutSide = "right" }) => {
  const [x, y] = at;
  const r = 11;
  const arm = 22;
  return (
    <Svg opacity={opacity}>
      <circle cx={x} cy={y} r={r} fill="none" stroke={tint} strokeWidth={1.4} />
      <circle cx={x} cy={y} r={3.2} fill={tint} />
      {[
        [1, 0],
        [-1, 0],
        [0, 1],
        [0, -1],
      ].map(([a, b]) => (
        <line
          key={`${a}${b}`}
          x1={x + a * (r + 4)}
          y1={y + b * (r + 4)}
          x2={x + a * (r + arm)}
          y2={y + b * (r + arm)}
          stroke={tint}
          strokeWidth={1.4}
        />
      ))}
      {readout ? (
        <text
          x={readoutSide === "right" ? x + 26 : x - 26}
          y={y - 40}
          textAnchor={readoutSide === "right" ? "start" : "end"}
          fill={tint}
          style={mono(17)}
        >
          {readout}
        </text>
      ) : null}
    </Svg>
  );
};

/** 角標框：只畫四角的 L 形（視窗／細部圖框） */
export const CornerFrame: React.FC<{
  x: number;
  y: number;
  w: number;
  h: number;
  len?: number;
  stroke?: string;
  progress?: number;
  full?: boolean;
}> = ({ x, y, w, h, len = 22, stroke: sc = color.ink2, progress = 1, full = false }) => {
  const l = len * clamp01(progress);
  const d = [
    `M${x},${y + l} L${x},${y} L${x + l},${y}`,
    `M${x + w - l},${y} L${x + w},${y} L${x + w},${y + l}`,
    `M${x + w},${y + h - l} L${x + w},${y + h} L${x + w - l},${y + h}`,
    `M${x + l},${y + h} L${x},${y + h} L${x},${y + h - l}`,
  ].join(" ");
  return (
    <Svg>
      {full ? (
        <rect x={x} y={y} width={w} height={h} fill="none" stroke={color.rule} strokeWidth={stroke.hair} opacity={clamp01(progress)} />
      ) : null}
      <path d={d} fill="none" stroke={sc} strokeWidth={2} />
    </Svg>
  );
};
