/**
 * Synchronous TeX → SVG glyph data via MathJax 4 (Pagella / Palatino math).
 * Output geometry is in MathJax units: 1000 = 1em, baseline at y = 0,
 * y grows downward (minY < 0 is the ascent).  Deterministic, cached.
 */
import { mathjax } from "@mathjax/src/js/mathjax.js";
import { TeX } from "@mathjax/src/js/input/tex.js";
import { SVG } from "@mathjax/src/js/output/svg.js";
import { liteAdaptor } from "@mathjax/src/js/adaptors/liteAdaptor.js";
import { RegisterHTMLHandler } from "@mathjax/src/js/handlers/html.js";
import "@mathjax/src/js/input/tex/base/BaseConfiguration.js";
import "@mathjax/src/js/input/tex/ams/AmsConfiguration.js";
import "@mathjax/src/js/input/tex/color/ColorConfiguration.js";
import { MathJaxPagellaFont } from "@mathjax/mathjax-pagella-font/js/svg.js";

export type Glyphs = {
  body: string; // inner SVG markup (fill = currentColor)
  minX: number;
  minY: number; // = −ascent
  w: number;
  h: number;
};

const adaptor = liteAdaptor();
RegisterHTMLHandler(adaptor);
const doc = mathjax.document("", {
  InputJax: new TeX({ packages: ["base", "ams", "color"] }),
  OutputJax: new SVG({ fontData: MathJaxPagellaFont, fontCache: "none", linebreaks: { inline: false } }),
});

const cache = new Map<string, Glyphs>();

export const tex = (src: string, display = false): Glyphs => {
  const key = `${display ? "D" : "I"}:${src}`;
  const hit = cache.get(key);
  if (hit) return hit;
  const node = doc.convert(src, { display });
  const html = adaptor.outerHTML(node) as string;
  const vb = /viewBox="([-\d.]+) ([-\d.]+) ([-\d.]+) ([-\d.]+)"/.exec(html);
  if (!vb) throw new Error(`MathJax produced no viewBox for ${src}`);
  const open = html.indexOf(">", html.indexOf("<svg"));
  const close = html.lastIndexOf("</svg>");
  const out: Glyphs = {
    body: html.slice(open + 1, close),
    minX: parseFloat(vb[1]),
    minY: parseFloat(vb[2]),
    w: parseFloat(vb[3]),
    h: parseFloat(vb[4]),
  };
  cache.set(key, out);
  return out;
};
