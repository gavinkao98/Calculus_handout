import React from "react";
import { CalculateMetadataFunction, Composition, Folder, Still } from "remotion";
import { MotionTest } from "./scenes/MotionTest";
import { F0Title } from "./scenes/F0Title";
import { F1Theorem } from "./scenes/F1Theorem";
import { F2Slope } from "./scenes/F2Slope";
import { F3Cycle } from "./scenes/F3Cycle";
import { Act3, ActProps, SceneComp } from "./act3/Act3";
import { DEFAULT_MANIFEST, ORDER, loadAct } from "./act3/timing";

// Act 3 timing comes from the TTS manifest (mock now, MiMo later):
//   npx remotion render build Act3 out/act3.mp4 --props='{"manifest":"audio/act3_mimo/manifest.json"}'
const actMeta: CalculateMetadataFunction<ActProps> = async ({ props }) => {
  const act = await loadAct(props.manifest);
  return { durationInFrames: act.total, props: { ...props, act } };
};
const sceneMeta: CalculateMetadataFunction<ActProps & { id: string }> = async ({ props }) => {
  const act = await loadAct(props.manifest);
  const s = act.scenes.find((x) => x.id === props.id);
  if (!s) throw new Error(`no scene ${props.id}`);
  return { durationInFrames: s.dur, props: { ...props, act } };
};

export const RemotionRoot: React.FC = () => (
  <>
    <Folder name="Frames">
      <Still id="F0-Title" component={F0Title} width={1920} height={1080} />
      <Still id="F1-Theorem" component={F1Theorem} width={1920} height={1080} />
      <Still id="F2-Slope" component={F2Slope} width={1920} height={1080} />
      <Still id="F3-Cycle" component={F3Cycle} width={1920} height={1080} />
    </Folder>
    <Composition id="MotionTest" component={MotionTest} width={1920} height={1080} fps={30} durationInFrames={450} />
    <Composition
      id="Act3"
      component={Act3}
      width={1920}
      height={1080}
      fps={30}
      durationInFrames={300}
      defaultProps={{ manifest: DEFAULT_MANIFEST } as ActProps}
      calculateMetadata={actMeta}
    />
    <Folder name="Act3-Scenes">
      {ORDER.map((o) => (
        <Composition
          key={o.id}
          id={`S-${o.id.replace(/_/g, "-")}`}
          component={SceneComp}
          width={1920}
          height={1080}
          fps={30}
          durationInFrames={300}
          defaultProps={{ manifest: DEFAULT_MANIFEST, id: o.id } as ActProps & { id: string }}
          calculateMetadata={sceneMeta}
        />
      ))}
    </Folder>
  </>
);
