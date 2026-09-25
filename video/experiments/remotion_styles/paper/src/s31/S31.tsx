/**
 * §3.1 — Derivatives of Sine and Cosine (unguided cut).
 * One sheet per scene; each new sheet is slid over the previous one on the desk.
 * All timing from the tts.py manifest (see timing.ts).
 */
import React from "react";
import { AbsoluteFill, Sequence, interpolate, useCurrentFrame } from "remotion";
import { Audio } from "@remotion/media";
import { staticFile } from "remotion";
import { ease } from "../theme";
import { clamp } from "../components/Type";
import { SceneCtx } from "./kit";
import { DEFAULT_MANIFEST, LEAD, OVER, SceneT, Show } from "./timing";
import { Circle } from "./scenes/Circle";
import { Title } from "./scenes/Title";
import { Stuck } from "./scenes/Stuck";
import { Rewrite } from "./scenes/Rewrite";
import { Areas } from "./scenes/Areas";
import { Continuity } from "./scenes/Continuity";
import { Limit } from "./scenes/Limit";
import { Warnings } from "./scenes/Warnings";
import { Payoff } from "./scenes/Payoff";
import { Slope } from "./scenes/Slope";
import { Companion } from "./scenes/Companion";
import { Four } from "./scenes/Four";
import { Spring } from "./scenes/Spring";
import { Cycle } from "./scenes/Cycle";
import { Next } from "./scenes/Next";

export const S31_SCENES: Record<string, React.FC> = {
  circle: Circle,
  title: Title,
  stuck: Stuck,
  rewrite: Rewrite,
  areas: Areas,
  continuity: Continuity,
  limit: Limit,
  warnings: Warnings,
  payoff: Payoff,
  slope: Slope,
  companion: Companion,
  four: Four,
  spring: Spring,
  cycle: Cycle,
  next: Next,
};
export const S31_ORDER = Object.keys(S31_SCENES);

export type S31Props = { manifest: string; show?: Show; id?: string };
export const S31_DEFAULTS: S31Props = { manifest: DEFAULT_MANIFEST };

/** A sheet: slides in over the previous one (except the first), dims a touch as the next covers it. */
const SheetSlot: React.FC<{ s: SceneT; first: boolean; last: boolean }> = ({ s, first, last }) => {
  const f = useCurrentFrame();
  const Comp = S31_SCENES[s.id];
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
      <SceneCtx.Provider value={{ beats: s.beats, dur: s.dur }}>
        {Comp ? <Comp /> : null}
      </SceneCtx.Provider>
      {tout > 0 && <AbsoluteFill style={{ background: `rgba(40,28,12,${0.28 * tout})` }} />}
      {s.audio && (
        <Sequence from={LEAD} layout="none">
          <Audio src={staticFile(s.audio)} />
        </Sequence>
      )}
    </AbsoluteFill>
  );
};

export const S31: React.FC<S31Props> = ({ show, id }) => {
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
