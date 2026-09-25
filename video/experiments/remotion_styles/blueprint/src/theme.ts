/**
 * 藍圖工程（blueprint）設計 token。
 * 所有元件、風格幀、動態測試只從這裡取值；換風格＝換這一檔。
 */
import { Easing } from "remotion";

export const FRAME = { width: 1920, height: 1080, fps: 30 } as const;

/** 色彩：深普魯士藍底＋白線稿；青色＝cos 家族；琥珀＝唯一亮色（導數／切線）。 */
export const color = {
  paper: "#0B2446", // 圖紙底色（Prussian blue）
  paperLift: "#133563", // 暈影中心（紙面受光）
  paperDeep: "#061934", // 暈影邊緣
  gridMinor: "rgba(150,190,255,0.075)",
  gridMajor: "rgba(150,190,255,0.16)",
  ink: "#F2F6FC", // 主線稿／主文字
  ink2: "#B4C8E4", // 次文字
  ink3: "#7C97BE", // 註記、刻度、尺寸線
  rule: "rgba(242,246,252,0.42)", // 圖框、表格線
  sin: "#F2F6FC", // sin 家族＝白墨
  cos: "#5CC8F2", // cos 家族＝青藍鉛筆
  accent: "#FFAE3A", // 導數／切線／強調（全片唯一亮色）
  accentDim: "rgba(255,174,58,0.35)",
} as const;

/** 語意色：畫面上任何「sin / cos / 導數 / 切線」一律走這張表。 */
export const semantic = {
  sin: color.sin,
  cos: color.cos,
  derivative: color.accent,
  tangent: color.accent,
  /** 負號函數（−sin、−cos）沿用家族色，改用「隱藏線」虛線表示 */
  negDash: "14 10",
} as const;

export const font = {
  display: "Barlow Condensed", // 標題：工程字（DIN 系）
  text: "Barlow", // 內文
  mono: "IBM Plex Mono", // 註記、讀數、圖框
  math: "KaTeX_Main", // 數學（KaTeX）
} as const;

/** 字級（px，1080p） */
export const type = {
  hero: 138,
  h1: 92,
  h2: 60,
  math: 84,
  mathLg: 112,
  body: 40,
  label: 28,
  note: 24,
  micro: 17,
} as const;

/** 線寬階層（製圖標準：輪廓粗、尺寸細、格線最細） */
export const stroke = {
  object: 4, // 函數曲線
  tangent: 3,
  axis: 2,
  thin: 1.35, // 尺寸線、引線、投影線
  hair: 1,
} as const;

/** 虛線樣式 */
export const dash = {
  hidden: "14 10", // 隱藏線（負號函數）
  center: "26 7 4 7", // 中心線／投影線（一長一短）
  construction: "3 6",
} as const;

export const space = {
  sheetOuter: 24, // 外框內縮
  sheetInner: 50, // 內框內縮
  strip: 66, // 圖框下緣標題列高
  gutter: 32,
} as const;

/** 動態 token（幀，30fps） */
export const motion = {
  fast: 10,
  base: 18,
  slow: 34,
  /** 筆畫描繪：製圖筆先加速再收筆 */
  draft: Easing.bezier(0.6, 0.05, 0.3, 1),
  /** 鏡頭：長尾緩停 */
  camera: Easing.bezier(0.65, 0, 0.25, 1),
  /** 元素進場：out-expo */
  settle: Easing.bezier(0.16, 1, 0.3, 1),
  /** 彈簧：切線「彈」進場（有一次回彈） */
  springy: { damping: 11, stiffness: 170, mass: 0.9 },
  /** 彈簧：不回彈的推送 */
  soft: { damping: 200, stiffness: 120, mass: 1 },
  /** token 變形：每個 token 的錯開 */
  morphStagger: 3,
} as const;

export const mono = (px: number, extra: Record<string, unknown> = {}) => ({
  fontFamily: font.mono,
  fontSize: px,
  letterSpacing: "0.08em",
  fontFeatureSettings: '"tnum" 1, "zero" 1',
  ...extra,
});
