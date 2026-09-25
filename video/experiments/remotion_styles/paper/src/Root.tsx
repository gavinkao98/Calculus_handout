import React from "react";
import { Composition, Folder, Still } from "remotion";
import { MotionTest } from "./scenes/MotionTest";
import { F0Title } from "./scenes/F0Title";
import { F1Theorem } from "./scenes/F1Theorem";
import { F2Slope } from "./scenes/F2Slope";
import { F3Cycle } from "./scenes/F3Cycle";

export const RemotionRoot: React.FC = () => (
  <>
    <Folder name="Frames">
      <Still id="F0-Title" component={F0Title} width={1920} height={1080} />
      <Still id="F1-Theorem" component={F1Theorem} width={1920} height={1080} />
      <Still id="F2-Slope" component={F2Slope} width={1920} height={1080} />
      <Still id="F3-Cycle" component={F3Cycle} width={1920} height={1080} />
    </Folder>
    <Composition id="MotionTest" component={MotionTest} width={1920} height={1080} fps={30} durationInFrames={450} />
  </>
);
