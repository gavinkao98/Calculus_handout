/**
 * §3.1 Act 3 — the whole act as one timeline, built from the TTS manifest.
 * Scenes overlap by TURN frames where they hand over with a page turn; the
 * earlier scene is drawn on top so its leaf turns away to reveal the next.
 */
import React from "react";
import { AbsoluteFill, Sequence } from "remotion";
import { Audio } from "@remotion/media";
import { color } from "../theme";
import { Vignette } from "../components/Paper";
import { ActCtx, SceneClock, sceneTiming } from "./clock";
import { PageTurnOut } from "./PageTurn";
import type { ActTiming, SceneTiming } from "./timing";
import { Intro } from "./scenes/Intro";
import { SineProof } from "./scenes/SineProof";
import { CosineProof } from "./scenes/CosineProof";
import { SlopeHeight } from "./scenes/SlopeHeight";
import { Cycle } from "./scenes/Cycle";
import { Outro } from "./scenes/Outro";

export const SCENES: Record<string, React.FC> = {
  intro: Intro,
  derivative_of_sine: SineProof,
  derivative_of_cosine: CosineProof,
  slope_equals_height: SlopeHeight,
  derivative_cycle: Cycle,
  outro: Outro,
};


/** One scene with its clock, narration and (if it hands over by turning) the leaf. */
export const SceneBody: React.FC<{ s: SceneTiming }> = ({ s }) => {
  const C = SCENES[s.id];
  const body = (
    <SceneClock timing={s}>
      <AbsoluteFill>
        <C />
      </AbsoluteFill>
    </SceneClock>
  );
  return (
    <>
      {s.out === "turn" ? <PageTurnOut dur={s.dur}>{body}</PageTurnOut> : body}
      {s.audio && (
        <Sequence from={s.lead} layout="none">
          <Audio src={s.audio} />
        </Sequence>
      )}
    </>
  );
};

export type ActProps = { manifest: string; act?: ActTiming };

export const Act3: React.FC<ActProps> = ({ act }) => {
  if (!act) return null;
  return (
    <ActCtx.Provider value={act}>
      <AbsoluteFill style={{ backgroundColor: color.paper }}>
        {[...act.scenes].reverse().map((s) => (
          <Sequence key={s.id} name={s.id} from={s.from} durationInFrames={s.dur}>
            <SceneBody s={s} />
          </Sequence>
        ))}
        <Vignette />
      </AbsoluteFill>
    </ActCtx.Provider>
  );
};

/** A single scene as its own composition (same clock, starts at 0). */
export const SceneComp: React.FC<ActProps & { id: string }> = ({ act, id }) => {
  if (!act) return null;
  const s = sceneTiming(act, id);
  return (
    <ActCtx.Provider value={act}>
      <AbsoluteFill style={{ backgroundColor: color.paper }}>
        <SceneBody s={{ ...s, from: 0 }} />
        <Vignette />
      </AbsoluteFill>
    </ActCtx.Provider>
  );
};
