/**
 * 字型全部來自本地 npm 套件（@fontsource、katex），render 時不連網。
 * 模組載入即開始下載，delayRender 擋住截圖直到字型與 KaTeX 字型都就緒。
 */
import { continueRender, delayRender } from "remotion";
import "katex/dist/katex.min.css";

import bc500 from "@fontsource/barlow-condensed/files/barlow-condensed-latin-500-normal.woff2";
import bc600 from "@fontsource/barlow-condensed/files/barlow-condensed-latin-600-normal.woff2";
import bc300 from "@fontsource/barlow-condensed/files/barlow-condensed-latin-300-normal.woff2";
import b400 from "@fontsource/barlow/files/barlow-latin-400-normal.woff2";
import b400i from "@fontsource/barlow/files/barlow-latin-400-italic.woff2";
import b500 from "@fontsource/barlow/files/barlow-latin-500-normal.woff2";
import m400 from "@fontsource/ibm-plex-mono/files/ibm-plex-mono-latin-400-normal.woff2";
import m500 from "@fontsource/ibm-plex-mono/files/ibm-plex-mono-latin-500-normal.woff2";
import m600 from "@fontsource/ibm-plex-mono/files/ibm-plex-mono-latin-600-normal.woff2";
import { font } from "./theme";

const faces: Array<[string, string, string, string]> = [
  [font.display, bc300, "300", "normal"],
  [font.display, bc500, "500", "normal"],
  [font.display, bc600, "600", "normal"],
  [font.text, b400, "400", "normal"],
  [font.text, b400i, "400", "italic"],
  [font.text, b500, "500", "normal"],
  [font.mono, m400, "400", "normal"],
  [font.mono, m500, "500", "normal"],
  [font.mono, m600, "600", "normal"],
];

const handle = delayRender("Loading fonts");

export const fontsReady: Promise<void> = Promise.all([
  ...faces.map(async ([family, url, weight, style]) => {
    const f = new FontFace(family, `url(${url}) format("woff2")`, {
      weight,
      style,
    });
    await f.load();
    document.fonts.add(f);
  }),
  // KaTeX 的 @font-face 由 katex.min.css 宣告，這裡主動觸發載入
  ...[
    "20px KaTeX_Main",
    "italic 20px KaTeX_Math",
    "20px KaTeX_Size1",
    "20px KaTeX_Size2",
    "bold 20px KaTeX_Main",
  ].map((spec) => document.fonts.load(spec)),
])
  .then(() => document.fonts.ready)
  .then(() => {
    continueRender(handle);
  })
  .catch((e) => {
    console.error("[fonts] failed", e);
    continueRender(handle);
  });
