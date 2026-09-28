/**
 * NTU Science Talent Program 2026, Problem 7 — square billiards.
 * One sheet per scene; each new sheet slides in over the previous one (as §3.1).
 * All timing from the tts.py manifest (see timing.ts).
 */
import React from "react";
import { AbsoluteFill, Sequence, interpolate, staticFile, useCurrentFrame } from "remotion";
import { Audio } from "@remotion/media";
import { ease } from "../theme";
import { clamp } from "../components/Type";
import { SceneCtx } from "../s31/kit";
import { DEFAULT_MANIFEST, LEAD, OVER, SceneT, Show } from "./timing";
import { Logo } from "./scenes/Logo";
import { Exam } from "./scenes/Exam";
import { Hook } from "./scenes/Hook";
import { Mirror } from "./scenes/Mirror";
import { Unfolding } from "./scenes/Unfolding";
import { Dictionary } from "./scenes/Dictionary";
import { Halfway } from "./scenes/Halfway";
import { Foldback } from "./scenes/Foldback";
import { Angles } from "./scenes/Angles";
import { Twist } from "./scenes/Twist";
import { Recap } from "./scenes/Recap";
import { Writeup } from "./scenes/Writeup";
import { Epilogue } from "./scenes/Epilogue";
import { Outro } from "./scenes/Outro";
import { ExtDesign } from "./scenes/ExtDesign";
import { ExtRoom } from "./scenes/ExtRoom";
import { ExtFamily } from "./scenes/ExtFamily";
import { ExtDense } from "./scenes/Epilogue";
import { Lang, LangCtx } from "./i18n";
import { ZH_FONT } from "./kit";
import { useCjkReady } from "./cjk";

/** every sheet either language uses; which ones, and in what order, is Q7_ORDER[lang] */
export const Q7_SCENES: Record<string, React.FC> = {
  logo: Logo,
  exam: Exam,
  hook: Hook,
  mirror: Mirror,
  unfold: Unfolding,
  dictionary: Dictionary,
  halfway: Halfway,
  foldback: Foldback,
  angles: Angles,
  twist: Twist,
  recap: Recap,
  writeup: Writeup,
  epilogue: Epilogue,
  ext_design: ExtDesign,
  ext_room: ExtRoom,
  ext_family: ExtFamily,
  ext_dense: ExtDense,
  outro: Outro,
};
/**
 * Each language has its own scene list (2026-09-26: only the zh cut changed —
 * writeup and epilogue out, the four-scene extension in). The manifest must
 * list exactly these scenes, in this order (checked in Root's calculateMetadata).
 */
const COMMON = ["logo", "exam", "hook", "mirror", "unfold", "dictionary", "halfway", "foldback", "angles", "twist", "recap"];
export const Q7_ORDER: Record<Lang, string[]> = {
  en: [...COMMON, "writeup", "epilogue", "outro"],
  zh: [...COMMON, "ext_design", "ext_room", "ext_family", "ext_dense", "outro"],
};

/** `lang`: which string table the sheets are set from (i18n/); the animation is the same */
export type Q7Props = { manifest: string; lang?: Lang; show?: Show; id?: string };
export const Q7_DEFAULTS: Q7Props = { manifest: DEFAULT_MANIFEST, lang: "en" };
export const Q7ZH_DEFAULTS: Q7Props = { manifest: "audio/q7zh_mock/manifest.json", lang: "zh" };

/** zh: hold every sheet until Noto Serif TC is in (a sheet never renders Chinese in a fallback font) */
const CjkGate: React.FC<{ children: React.ReactNode }> = ({ children }) => (useCjkReady() ? <>{children}</> : null);

/**
 * zh scope: the Chinese stack on everything and no synthesized italic/bold
 * anywhere — a safety net under the lang-aware Txt/Caps/Kicker (kit.tsx), so a
 * shared component that sets Garamond (running head, small caps) cannot draw
 * an ideograph in a system font or slant one.
 */
const ZhScope: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <AbsoluteFill className="q7-zh" lang="zh-Hant">
    <style>{`.q7-zh, .q7-zh * { font-family: ${ZH_FONT} !important; font-synthesis: none !important; }`}</style>
    {children}
  </AbsoluteFill>
);

const SheetSlot: React.FC<{ s: SceneT; first: boolean; last: boolean; zh: boolean }> = ({ s, first, last, zh }) => {
  const f = useCurrentFrame();
  const Comp = Q7_SCENES[s.id];
  const tin = first ? 1 : interpolate(f, [0, OVER], [0, 1], { ...clamp, easing: ease.camera });
  const tout = last ? 0 : interpolate(f, [s.dur - OVER, s.dur], [0, 1], { ...clamp, easing: ease.camera });
  return (
    <AbsoluteFill
      style={{
        translate: `${(1 - tin) * 1990 - tout * 70}px ${(1 - tin) * 26}px`,
        rotate: `${(1 - tin) * 1.6}deg`,
        boxShadow: tin < 1 ? `-30px 0 60px rgba(30,20,10,${0.35 * (1 - tin * 0.6)})` : undefined,
      }}
    >
      <SceneCtx.Provider value={{ id: s.id, beats: s.beats, dur: s.dur, words: s.words }}>{Comp ? zh ? <CjkGate><Comp /></CjkGate> : <Comp /> : null}</SceneCtx.Provider>
      {tout > 0 && <AbsoluteFill style={{ background: `rgba(40,28,12,${0.28 * tout})` }} />}
      {s.audio && (
        <Sequence from={LEAD} layout="none">
          <Audio src={staticFile(s.audio)} />
        </Sequence>
      )}
    </AbsoluteFill>
  );
};

export const Q7: React.FC<Q7Props> = ({ show, id, lang = "en" }) => {
  if (!show) return null;
  const zh = lang === "zh";
  const list = id ? show.scenes.filter((s) => s.id === id) : show.scenes;
  const sheets = (
    <AbsoluteFill style={{ backgroundColor: "#2F2A24" }}>
      {list.map((s, i) => (
        <Sequence key={s.id} from={id ? 0 : s.from} durationInFrames={s.dur} name={s.id}>
          <SheetSlot s={s} first={i === 0} last={i === list.length - 1} zh={zh} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
  return <LangCtx.Provider value={lang}>{zh ? <ZhScope>{sheets}</ZhScope> : sheets}</LangCtx.Provider>;
};
