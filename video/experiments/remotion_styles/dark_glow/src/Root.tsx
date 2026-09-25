import React from 'react';
import {Composition, Folder, Still} from 'remotion';
import './fonts';
import {F0Title} from './frames/F0Title';
import {F1Theorem} from './frames/F1Theorem';
import {F2SlopeHeight} from './frames/F2SlopeHeight';
import {F3Cycle} from './frames/F3Cycle';
import {MotionTest} from './motion/MotionTest';

export const RemotionRoot: React.FC = () => (
  <>
    <Folder name="StyleFrames">
      <Still id="F0-Title" component={F0Title} width={1920} height={1080} />
      <Still id="F1-Theorem" component={F1Theorem} width={1920} height={1080} />
      <Still id="F2-SlopeHeight" component={F2SlopeHeight} width={1920} height={1080} />
      <Still id="F3-Cycle" component={F3Cycle} width={1920} height={1080} />
    </Folder>
    <Composition id="MotionTest" component={MotionTest} durationInFrames={450} fps={30} width={1920} height={1080} />
  </>
);
