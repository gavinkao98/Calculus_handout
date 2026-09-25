import React from "react";
import { CalculateMetadataFunction, Composition, Folder, Still } from "remotion";
import { MotionTest } from "./scenes/MotionTest";
import { F0Title } from "./scenes/F0Title";
import { F1Theorem } from "./scenes/F1Theorem";
import { F2Slope } from "./scenes/F2Slope";
import { F3Cycle } from "./scenes/F3Cycle";
import { Act3, ActProps, SceneComp } from "./act3/Act3";
import { DEFAULT_MANIFEST, ORDER, loadAct } from "./act3/timing";
import { S31, S31Props, S31_DEFAULTS, S31_ORDER } from "./s31/S31";
import { loadShow } from "./s31/timing";
import { Q7, Q7Props, Q7ZH_DEFAULTS, Q7_DEFAULTS, Q7_ORDER } from "./q7/Q7";
import { loadShow as loadQ7 } from "./q7/timing";

// §3.1 unguided cut (src/s31/): its own manifest-driven timing.
//   npx remotion render build S31 out/s31.mp4 --props='{"manifest":"audio/s31_mimo/manifest.json"}'
const s31Meta: CalculateMetadataFunction<S31Props> = async ({ props }) => {
  const show = await loadShow(props.manifest);
  const s = props.id ? show.scenes.find((x) => x.id === props.id) : null;
  if (props.id && !s) throw new Error(`no scene ${props.id}`);
  return { durationInFrames: s ? s.dur : show.total, props: { ...props, show } };
};

// NTU 2026 exam, Problem 7 (src/q7/): same manifest-driven timing as §3.1.
//   npx remotion render build Q7 out/q7.mp4 --props='{"manifest":"audio/q7_mimo/manifest.json"}'
// Q7ZH = the same animation set from the Chinese string table (lang "zh"), on its own manifest.
const q7Meta: CalculateMetadataFunction<Q7Props> = async ({ props }) => {
  const show = await loadQ7(props.manifest);
  const s = props.id ? show.scenes.find((x) => x.id === props.id) : null;
  if (props.id && !s) throw new Error(`no scene ${props.id}`);
  return { durationInFrames: s ? s.dur : show.total, props: { ...props, show } };
};

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
    <Folder name="S31">
      <Composition id="S31" component={S31} width={1920} height={1080} fps={30} durationInFrames={300} defaultProps={S31_DEFAULTS} calculateMetadata={s31Meta} />
      {S31_ORDER.map((id) => (
        <Composition
          key={id}
          id={`S31-${id}`}
          component={S31}
          width={1920}
          height={1080}
          fps={30}
          durationInFrames={300}
          defaultProps={{ ...S31_DEFAULTS, id }}
          calculateMetadata={s31Meta}
        />
      ))}
    </Folder>
    <Folder name="Q7">
      <Composition id="Q7" component={Q7} width={1920} height={1080} fps={30} durationInFrames={300} defaultProps={Q7_DEFAULTS} calculateMetadata={q7Meta} />
      <Composition id="Q7ZH" component={Q7} width={1920} height={1080} fps={30} durationInFrames={300} defaultProps={Q7ZH_DEFAULTS} calculateMetadata={q7Meta} />
      {Q7_ORDER.map((id) => (
        <Composition
          key={id}
          id={`Q7-${id}`}
          component={Q7}
          width={1920}
          height={1080}
          fps={30}
          durationInFrames={300}
          defaultProps={{ ...Q7_DEFAULTS, id }}
          calculateMetadata={q7Meta}
        />
      ))}
    </Folder>
  </>
);
