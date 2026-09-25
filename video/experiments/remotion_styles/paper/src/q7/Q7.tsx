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
  outro: Outro,
};
export const Q7_ORDER = Object.keys(Q7_SCENES);

export type Q7Props = { manifest: string; show?: Show; id?: string };
export const Q7_DEFAULTS: Q7Props = { manifest: DEFAULT_MANIFEST };

const SheetSlot: React.FC<{ s: SceneT; first: boolean; last: boolean }> = ({ s, first, last }) => {
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
      <SceneCtx.Provider value={{ id: s.id, beats: s.beats, dur: s.dur, words: s.words }}>{Comp ? <Comp /> : null}</SceneCtx.Provider>
      {tout > 0 && <AbsoluteFill style={{ background: `rgba(40,28,12,${0.28 * tout})` }} />}
      {s.audio && (
        <Sequence from={LEAD} layout="none">
          <Audio src={staticFile(s.audio)} />
        </Sequence>
      )}
    </AbsoluteFill>
  );
};

export const Q7: React.FC<Q7Props> = ({ show, id }) => {
  if (!show) return null;
  const list = id ? show.scenes.filter((s) => s.id === id) : show.scenes;
  return (
    <AbsoluteFill style={{ backgroundColor: "#2F2A24" }}>
      {list.map((s, i) => (
        <Sequence key={s.id} from={id ? 0 : s.from} durationInFrames={s.dur} name={s.id}>
          <SheetSlot s={s} first={i === 0} last={i === list.length - 1} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
