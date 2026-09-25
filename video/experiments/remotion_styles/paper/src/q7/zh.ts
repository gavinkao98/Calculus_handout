/**
 * Every Chinese string Q7 sets on screen (logo subtitle + exam title card).
 * `scripts/cjk-subsets.mjs` reads THIS file to pick the Noto Serif TC subset
 * files the bundle needs (→ `cjkFaces.ts`); after editing a string, rerun it.
 * `useCjkReady` refuses to render if a character here is not covered.
 */
export const ZH = {
  logoSub: "115 學年度北區人才培育計畫入學考第七題",
  kicker: "入學考試・數學組",
  numLabel: "題號",
  school: "國立臺灣大學",
  title1: "北區高中學生",
  title2: "科學研究人才培育計畫",
  subtitle: "數學組・115 學年度入學考試",
  rows: [
    ["學年度", "115"],
    ["測驗日期", "115 年 9 月 6 日（星期日）"],
    ["題號", "第 7 題（共 7 題）"],
  ] as Array<[string, string]>,
} as const;

/** flat list of every string above (for the font gate) */
export const ZH_ALL: string[] = Object.values(ZH).flatMap((v) => (Array.isArray(v) ? v.flat() : [v as string]));
