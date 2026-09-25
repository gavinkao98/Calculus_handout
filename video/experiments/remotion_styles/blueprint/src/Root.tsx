import "./fonts";
import React from "react";
import { Composition, Still } from "remotion";
import { FRAME } from "./theme";
import { F0Title } from "./scenes/F0Title";
import { F1Theorem } from "./scenes/F1Theorem";
import { F2Slope } from "./scenes/F2Slope";
import { F3Cycle } from "./scenes/F3Cycle";
import { MotionTest } from "./scenes/MotionTest";

export const RemotionRoot: React.FC = () => {
  const size = { width: FRAME.width, height: FRAME.height };
  return (
    <>
      <Still id="F0-title" component={F0Title} {...size} />
      <Still id="F1-theorem" component={F1Theorem} {...size} />
      <Still id="F2-slope-height" component={F2Slope} {...size} />
      <Still id="F3-cycle" component={F3Cycle} {...size} />
      <Composition id="MotionTest" component={MotionTest} durationInFrames={450} fps={FRAME.fps} {...size} />
    </>
  );
};
