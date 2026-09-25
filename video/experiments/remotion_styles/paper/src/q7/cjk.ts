/**
 * Noto Serif TC (思源宋體, SIL OFL via @fontsource) for Q7's Chinese opening.
 * Only the unicode-range subset files that ZH needs are bundled (cjkFaces.ts,
 * generated). Loaded lazily — only scenes that call useCjkReady pay for it —
 * and the render is held until the glyphs are in; if a character is not
 * covered, or the face is not the one actually drawing the text, the render
 * is cancelled rather than falling back to a system font.
 */
import { useEffect, useState } from "react";
import { cancelRender, continueRender, delayRender } from "remotion";
import { CJK_FACES } from "./cjkFaces";
import { ZH_ALL } from "./zh";

export const CJK_FAMILY = "Noto Serif TC";
/** Garamond first (Latin, digits), Noto for the ideographs and full-width punctuation. */
export const CJK_STACK = `'EB Garamond', '${CJK_FAMILY}'`;
/**
 * size-adjust on the Noto faces: an ideograph fills ~0.9 em, Garamond's caps
 * ~0.65 em, so at equal font-size the Chinese looks a size too big next to the
 * digits. 0.86 brings the ideographs to ~1.2× cap height. Effective CJK size =
 * font-size × CJK_SCALE; keep that ≥ 28 px (STYLE.md 字級下限).
 */
export const CJK_SCALE = 0.86;

const inRange = (cp: number, range: string) =>
  range.split(",").some((r) => {
    const [a, b] = r.trim().replace(/^U\+/i, "").split("-");
    const lo = parseInt(a, 16);
    return cp >= lo && cp <= parseInt(b ?? a, 16);
  });

let ready: Promise<void> | null = null;
const loadCjk = (): Promise<void> => {
  if (ready) return ready;
  ready = (async () => {
    // 1. coverage: every non-ASCII character must fall in a bundled subset, per weight
    for (const w of new Set(CJK_FACES.map((f) => f.weight))) {
      const ranges = CJK_FACES.filter((f) => f.weight === w).map((f) => f.unicodeRange);
      for (const s of ZH_ALL)
        for (const ch of s) {
          const cp = ch.codePointAt(0)!;
          if (cp > 0x7f && !ranges.some((r) => inRange(cp, r)))
            throw new Error(`Noto Serif TC ${w}: "${ch}" not bundled — run node scripts/cjk-subsets.mjs`);
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
    const all = ZH_ALL.join("");
    const cjkOnly = [...all].filter((c) => c.codePointAt(0)! > 0x2e7f).join("");
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
