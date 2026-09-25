/**
 * Noto Serif TC (思源宋體, SIL OFL via @fontsource) for Q7's Chinese: the exam
 * card (both versions) and, in the zh version, every scene. Only the
 * unicode-range subset files the zh table needs are bundled (cjkFaces.ts,
 * generated from i18n/zh.ts + card.ts). Loaded lazily — the en version pays
 * for it only in the scenes that call useCjkReady (logo, exam); the zh
 * version gates every sheet on it (Q7.tsx) — and the render is held until the
 * glyphs are in. If a character is not covered, a TeX source carries Chinese,
 * or the face is not the one actually drawing the text, the render is
 * cancelled rather than falling back to a system font.
 */
import { useEffect, useState } from "react";
import { cancelRender, continueRender, delayRender } from "remotion";
import { CJK_FACES, LATIN_RANGE } from "./cjkFaces";
import { CJK_RE, prose, texOf, walk } from "./i18n";
import { zh } from "./i18n/zh";
import { extZh } from "./i18n/ext.zh";

export const CJK_FAMILY = "Noto Serif TC";
/** Garamond first (Latin, digits), Noto for the ideographs and full-width punctuation. */
export const CJK_STACK = `'EB Garamond', '${CJK_FAMILY}'`;
/**
 * size-adjust on the Noto faces: an ideograph fills ~0.9 em, Garamond's caps
 * ~0.65 em, so at equal font-size the Chinese looks a size too big next to the
 * digits. 0.86 brings the ideographs to ~1.2× cap height. Effective CJK size =
 * font-size × CJK_SCALE; keep that ≥ 28 px (STYLE.md 字級下限) → CJK_MIN.
 */
export const CJK_SCALE = 0.86;
/** smallest font-size for Chinese text: 34 × 0.86 ≈ 29 px ≥ the 28 px floor */
export const CJK_MIN = 34;

const inRange = (cp: number, range: string) =>
  range.split(",").some((r) => {
    const [a, b] = r.trim().replace(/^U\+/i, "").split("-");
    const lo = parseInt(a, 16);
    return cp >= lo && cp <= parseInt(b ?? a, 16);
  });

/** every zh-table string (the exam card included) */
const ZH_ALL = [...walk(zh), ...walk(extZh, "ext")];

let ready: Promise<void> | null = null;
const loadCjk = (): Promise<void> => {
  if (ready) return ready;
  ready = (async () => {
    // 0. no Chinese inside TeX: MathJax (lite adaptor) cannot measure it
    for (const { path, s } of ZH_ALL)
      for (const t of texOf(path, s))
        if (CJK_RE.test(t)) throw new Error(`zh.${path}: Chinese inside TeX ("${t}") — set the words as text next to the formula`);
    // 1. coverage: every character of Chinese prose that Garamond does not draw must fall in a
    //    bundled Noto subset, per weight (English placeholders are exempt: they are not Chinese yet)
    for (const w of new Set(CJK_FACES.map((f) => f.weight))) {
      const ranges = CJK_FACES.filter((f) => f.weight === w).map((f) => f.unicodeRange);
      for (const { path, s } of ZH_ALL) {
        if (!CJK_RE.test(s)) continue;
        for (const ch of prose(s)) {
          const cp = ch.codePointAt(0)!;
          if (!inRange(cp, LATIN_RANGE) && !ranges.some((r) => inRange(cp, r)))
            throw new Error(`Noto Serif TC ${w}: "${ch}" (zh.${path}) not bundled — run node scripts/cjk-subsets.mjs`);
        }
      }
    }
    // 2. register + load the faces
    await Promise.all(
      CJK_FACES.map(async ({ url, weight, unicodeRange }) => {
        const face = new FontFace(CJK_FAMILY, `url(${url}) format('woff2')`, {
          weight,
          unicodeRange,
          sizeAdjust: `${CJK_SCALE * 100}%`,
        } as FontFaceDescriptors);
        document.fonts.add(face);
        await face.load();
      }),
    );
    // 3. load for the actual strings, then prove the Noto face is the one drawing them:
    //    a system fallback would advance 1 em per ideograph, the size-adjusted Noto CJK_SCALE em.
    const all = ZH_ALL.map((x) => prose(x.s)).join("");
    const cjkOnly = [...new Set([...all].filter((c) => c.codePointAt(0)! > 0x2e7f))].join("");
    const ctx = document.createElement("canvas").getContext("2d")!;
    for (const w of new Set(CJK_FACES.map((f) => f.weight))) {
      await document.fonts.load(`${w} 40px '${CJK_FAMILY}'`, all);
      ctx.font = `${w} 100px '${CJK_FAMILY}', monospace`;
      const per = ctx.measureText(cjkOnly).width / [...cjkOnly].length;
      if (Math.abs(per - CJK_SCALE * 100) > 1.5)
        throw new Error(`Noto Serif TC ${w} not in use (advance ${per.toFixed(2)} px/char, expected ${CJK_SCALE * 100})`);
      console.log(`[cjk] Noto Serif TC ${w} in use: ${[...cjkOnly].length} ideographs, ${per.toFixed(2)} px/char @100px`);
    }
  })();
  return ready;
};

/** Holds the render until the Chinese glyphs are loaded; true once they are. */
export const useCjkReady = (): boolean => {
  const [ok, setOk] = useState(false);
  const [handle] = useState(() => delayRender("Noto Serif TC"));
  useEffect(() => {
    loadCjk()
      .then(() => {
        setOk(true);
        continueRender(handle);
      })
      .catch((e) => cancelRender(e));
  }, [handle]);
  return ok;
};
