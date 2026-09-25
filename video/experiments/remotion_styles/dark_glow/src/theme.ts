// dark_glow「Nocturne」設計 token —— 一切顏色／字型／間距／動態參數的唯一來源。
// 元件只讀這裡；換風格＝換這個檔。
import {Easing} from 'remotion';

export const FRAME = {width: 1920, height: 1080, fps: 30} as const;

// ---------------------------------------------------------------- colour
// 深藍黑夜空底 + 暖白墨；語意色只有三個色相（sin 餘燼珊瑚／cos 暮光長春花藍／導數 金），
// 切線是「純光」（暖白）。配色經 dataviz validate_palette.js 驗過 CVD 與常態視覺分離
// （worst ΔE deutan 10.0、normal 17.2）；亮度刻意高於圖表帶——這是發光筆畫，不是填色。
export const color = {
  bg: '#07080C',
  bgLift: '#141A2A', // 焦點處的夜空微光
  ink: '#EEEAE2', // 主要文字（暖白）
  ink2: '#A8A59D', // 次要文字
  ink3: '#6B6964', // 註記、刻度
  hair: 'rgba(238,234,226,0.13)', // 髮絲線（座標軸）
  hairStrong: 'rgba(238,234,226,0.28)',

  sin: '#FF8676', // ember
  sinCore: '#FFD9D0',
  cos: '#8C9EFF', // lumen
  cosCore: '#DCE2FF',
  deriv: '#E4CF8C', // champagne gold：d/dx、斜率讀數
  derivCore: '#FFF3D6',
  tangent: '#FFF2DE', // 切線＝一道光
  tangentCore: '#FFFFFF',
} as const;

export type Hue = 'sin' | 'cos' | 'deriv' | 'tangent' | 'ink';
export const hue = (h: Hue) =>
  h === 'ink'
    ? {main: color.ink, core: '#FFFFFF'}
    : {main: color[h], core: color[`${h}Core` as const]};

// ---------------------------------------------------------------- type
export const font = {
  display: '"Cormorant Garamond", serif', // 標題：電影片名感的高反差襯線
  mono: '"DM Mono", monospace', // 儀器讀數、眉標（等寬＝數字不跳動）
  // 數學式：MathJax 4 + Pagella（Palatino 系），建置期轉 SVG，見 scripts/prebuild.mjs
} as const;

export const type = {
  display: {size: 124, weight: 500, lineHeight: 1.0, tracking: '-0.01em'},
  title: {size: 64, weight: 500, lineHeight: 1.1, tracking: '-0.005em'},
  lead: {size: 46, weight: 400, lineHeight: 1.25, tracking: '0'},
  eyebrow: {size: 22, weight: 400, tracking: '0.34em'}, // DM Mono 大寫
  readoutLabel: {size: 20, weight: 400, tracking: '0.3em'},
  readout: {size: 44, weight: 400, tracking: '0.02em'},
  // 數學字級（px / em）
  mathXL: 128,
  mathL: 96,
  mathM: 68,
  mathS: 48,
  tick: 34,
} as const;

// ---------------------------------------------------------------- space
export const space = {s1: 8, s2: 16, s3: 24, s4: 40, s5: 64, s6: 104, s7: 168} as const;
export const safe = {x: 128, top: 104, bottom: 96} as const;

// ---------------------------------------------------------------- glow
// 每條發光筆畫 = 三層：bloom（寬、重模糊、低不透明）→ halo（中）→ core（細、近白）。
export const glow = {
  bloom: {width: 20, blur: 20, opacity: 0.26},
  halo: {width: 7, blur: 5, opacity: 0.6},
  core: {width: 2.8},
  math: {blur: 30, bloom: 120, bloomOpacity: 0.16, haloOpacity: 0.26}, // 數學字：viewBox 單位（1000 = 1em）
} as const;

// ---------------------------------------------------------------- motion
export const ease = {
  glide: Easing.bezier(0.16, 1, 0.3, 1), // 進場、token 滑行
  camera: Easing.bezier(0.6, 0, 0.25, 1), // 鏡頭推拉：慢起、長尾
  draw: Easing.bezier(0.45, 0.05, 0.2, 1), // 筆畫描出
  slide: Easing.bezier(0.5, 0, 0.5, 1), // 沿曲線滑動
  fade: Easing.bezier(0.33, 0, 0.2, 1),
} as const;

export const springs = {
  pop: {damping: 11, stiffness: 150, mass: 0.7}, // 切線彈入：一次輕微回彈
  settle: {damping: 22, stiffness: 110, mass: 1}, // 落定：幾乎不彈
  morph: {damping: 16, stiffness: 90, mass: 1}, // 公式 token 滑行
} as const;

export const dur = {quick: 12, base: 20, slow: 36, draw: 54} as const; // frames @30fps
