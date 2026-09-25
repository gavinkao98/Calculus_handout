// 建置期資產：render 時零網路、零 MathJax runtime。
// 1) TeX → 靜態 SVG（MathJax 4 + Pagella 數學字型）：讀 src/math/formulas.json → src/math/generated.ts。
//    每條式子存 viewBox（1000 單位 = 1em，基線在 y=0）與 SVG 內層 markup；
//    \class{tok-KEY}{…} 保留成 <g class="tok-KEY">，供 MathTex 上色、MorphTex 配對。
// 2) 品牌 logo：原樣讀 video/pipeline/assets/brand/*.svg（唯一真源，不改色不重繪）→ src/brand/generated.ts，
//    以便 inline 渲染（lockup 內含 <text>，inline 才吃得到 bundle 內的 Noto Sans TC）。
import {readFileSync, writeFileSync} from 'node:fs';
import {fileURLToPath, pathToFileURL} from 'node:url';
import {dirname, join} from 'node:path';
import MathJax from '@mathjax/src';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const brandDir = join(root, '../../../pipeline/assets/brand');

// ---------------------------------------------------------------- 1. TeX
const formulas = JSON.parse(readFileSync(join(root, 'src/math/formulas.json'), 'utf8'));

await MathJax.init({
  loader: {
    load: ['input/tex', 'output/svg', '[tex]/html'],
    paths: {'mathjax-pagella': '@mathjax/mathjax-pagella-font'},
    // Windows：import() 不吃 C:/ 絕對路徑，要轉成 file:// URL（套件名照常交給 import 解析）。
    require: (file) => import(/^[A-Za-z]:[\\/]/.test(file) ? pathToFileURL(file).href : file),
  },
  tex: {packages: {'[+]': ['html']}},
  output: {font: 'mathjax-pagella'},
  // fontCache none：每個字形直接是 <path>，多條式子同頁也不會 id 撞名；inline 不斷行。
  svg: {fontCache: 'none', linebreaks: {inline: false}},
});
const adaptor = MathJax.startup.adaptor;

// ---- token 外框：建置期直接由字形路徑算（控制點凸包，對動畫定位已足夠），render 時不必量 DOM。
const mul = (a, b) => [
  a[0] * b[0] + a[2] * b[1], a[1] * b[0] + a[3] * b[1],
  a[0] * b[2] + a[2] * b[3], a[1] * b[2] + a[3] * b[3],
  a[0] * b[4] + a[2] * b[5] + a[4], a[1] * b[4] + a[3] * b[5] + a[5],
];
const parseTransform = (t) => {
  let m = [1, 0, 0, 1, 0, 0];
  for (const [, fn, args] of (t || '').matchAll(/(\w+)\(([^)]*)\)/g)) {
    const v = args.split(/[\s,]+/).filter(Boolean).map(Number);
    if (fn === 'translate') m = mul(m, [1, 0, 0, 1, v[0], v[1] ?? 0]);
    else if (fn === 'scale') m = mul(m, [v[0], 0, 0, v[1] ?? v[0], 0, 0]);
    else if (fn === 'matrix') m = mul(m, v);
    else throw new Error(`unsupported transform ${fn}`);
  }
  return m;
};
const pathPoints = (d) => {
  const toks = d.match(/[A-Za-z]|-?(?:\d+\.?\d*|\.\d+)(?:e[-+]?\d+)?/g) ?? [];
  const pts = [];
  let cmd = 'M', cx = 0, cy = 0, i = 0;
  const num = () => Number(toks[i++]);
  while (i < toks.length) {
    if (/[A-Za-z]/.test(toks[i])) cmd = toks[i++];
    const rel = cmd === cmd.toLowerCase();
    const C = cmd.toUpperCase();
    if (C === 'Z') continue;
    const arity = {M: 2, L: 2, T: 2, H: 1, V: 1, C: 6, S: 4, Q: 4}[C];
    if (!arity) throw new Error(`unsupported path cmd ${cmd}`);
    const v = Array.from({length: arity}, num);
    if (C === 'H') { cx = rel ? cx + v[0] : v[0]; pts.push([cx, cy]); continue; }
    if (C === 'V') { cy = rel ? cy + v[0] : v[0]; pts.push([cx, cy]); continue; }
    for (let k = 0; k < arity; k += 2) pts.push([rel ? cx + v[k] : v[k], rel ? cy + v[k + 1] : v[k + 1]]);
    [cx, cy] = pts[pts.length - 1];
    if (C === 'M') cmd = rel ? 'l' : 'L';
  }
  return pts;
};
const tokenBoxes = (svgNode) => {
  const boxes = {};
  const walk = (n, m, toks) => {
    const tag = adaptor.kind(n);
    if (tag === '#text' || tag === '#comment') return;
    const mm = mul(m, parseTransform(adaptor.getAttribute(n, 'transform')));
    const cls = adaptor.getAttribute(n, 'class') || '';
    const here = [...toks, ...cls.split(/\s+/).filter((c) => c.startsWith('tok-')).map((c) => c.slice(4))];
    let pts = [];
    if (tag === 'path') pts = pathPoints(adaptor.getAttribute(n, 'd') || '');
    if (tag === 'rect') {
      const [x, y, w, h] = ['x', 'y', 'width', 'height'].map((a) => Number(adaptor.getAttribute(n, a) || 0));
      pts = [[x, y], [x + w, y + h]];
    }
    for (const [px, py] of pts) {
      const X = mm[0] * px + mm[2] * py + mm[4];
      const Y = mm[1] * px + mm[3] * py + mm[5];
      for (const k of here) {
        const b = (boxes[k] ??= [Infinity, Infinity, -Infinity, -Infinity]);
        b[0] = Math.min(b[0], X); b[1] = Math.min(b[1], Y); b[2] = Math.max(b[2], X); b[3] = Math.max(b[3], Y);
      }
    }
    for (const c of adaptor.childNodes(n)) walk(c, mm, here);
  };
  for (const c of adaptor.childNodes(svgNode)) walk(c, [1, 0, 0, 1, 0, 0], []);
  for (const k of Object.keys(boxes)) boxes[k] = boxes[k].map((v) => Math.round(v * 10) / 10);
  return boxes; // [x0, y0, x1, y1]，viewBox 座標（y 向下，基線 y=0）
};

const tex = {};
for (const [id, src] of Object.entries(formulas)) {
  if (id.startsWith('_')) continue;
  const node = await MathJax.tex2svgPromise(src, {display: true});
  const html = adaptor.outerHTML(node);
  if (/merror|data-mjx-error/.test(html)) throw new Error(`TeX error in ${id}: ${src}`);
  const vb = html.match(/viewBox="([^"]+)"/)[1].split(/\s+/).map(Number);
  const inner = html.replace(/^[\s\S]*?<svg[^>]*>/, '').replace(/<\/svg>[\s\S]*$/, '');
  const svgNode = adaptor.childNodes(node).find((c) => adaptor.kind(c) === 'svg');
  tex[id] = {viewBox: vb, tokens: tokenBoxes(svgNode), body: inner.replace(/ data-latex="[^"]*"/g, '')};
}
writeFileSync(
  join(root, 'src/math/generated.ts'),
  `// 由 scripts/prebuild.mjs 產生，勿手改（改 formulas.json 後 npm run prebuild）。\n` +
    `export type TexEntry = {viewBox: number[]; tokens: Record<string, number[]>; body: string};\n` +
    `export const TEX: Record<string, TexEntry> = ${JSON.stringify(tex)};\n`,
);

// ---------------------------------------------------------------- 2. brand
const brand = {};
for (const name of ['icon-white', 'lockup-white']) {
  brand[name] = readFileSync(join(brandDir, `${name}.svg`), 'utf8').trim();
}
writeFileSync(
  join(root, 'src/brand/generated.ts'),
  `// 由 scripts/prebuild.mjs 自 video/pipeline/assets/brand/ 原樣複製，勿手改。\n` +
    `export const BRAND: Record<'icon-white' | 'lockup-white', string> = ${JSON.stringify(brand)};\n`,
);

console.log(`prebuild: ${Object.keys(tex).length} formulas, ${Object.keys(brand).length} brand svgs`);
