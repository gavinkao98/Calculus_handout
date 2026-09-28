/**
 * Q7 language plumbing: one animation, two string tables (en.ts / zh.ts).
 * `LangCtx` is provided by the Q7 composition (`lang` prop); scenes read the
 * table through `useT()` in ../kit.tsx.
 */
import { createContext } from "react";
import { en, Strings } from "./en";
import { zh } from "./zh";
import { ExtStrings, extZh } from "./ext.zh";

export type Lang = "en" | "zh";
export type { Strings, ExtStrings };
export const TABLES: Record<Lang, Strings> = { en, zh };
/** scenes only one language has (the zh extension): their own table, per language that has them */
export const EXT: Partial<Record<Lang, ExtStrings>> = { zh: extZh };
export const LangCtx = createContext<Lang>("en");

/** fill `{n}`-style slots */
export const fmt = (s: string, vars: Record<string, string | number>) =>
  s.replace(/\{(\w+)\}/g, (m, k: string) => (k in vars ? String(vars[k]) : m));

/** every string in a table, with its dotted key path (for the font gate and the TeX check) */
export const walk = (v: unknown, path = ""): Array<{ path: string; s: string }> => {
  if (typeof v === "string") return [{ path, s: v }];
  if (Array.isArray(v)) return v.flatMap((x, i) => walk(x, `${path}[${i}]`));
  if (v && typeof v === "object") return Object.entries(v).flatMap(([k, x]) => walk(x, path ? `${path}.${k}` : k));
  return [];
};

/** Han ideographs + CJK punctuation / full-width forms */
export const CJK_RE = /[⺀-鿿豈-﫿︰-﹏＀-￯]/;
/** the prose of a string without its inline TeX ($…$): what the text fonts must draw */
export const prose = (s: string) => s.replace(/\$[^$]*\$/g, "");
/** the TeX a string carries: a `…Tex` field whole, else its $…$ segments */
export const texOf = (path: string, s: string): string[] => (/Tex$/.test(path) ? [s] : [...s.matchAll(/\$([^$]*)\$/g)].map((m) => m[1]));
