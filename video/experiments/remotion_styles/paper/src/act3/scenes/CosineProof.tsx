/**
 * derivative_of_cosine — the facing page.  The scene opens on the finished
 * sine page (frozen, exactly the last frame of the previous scene), slides
 * across the spine to the recto, runs the same machinery faster, and ends by
 * pulling back off the page to show the open book on the desk: both theorems
 * side by side, the one extra minus sign ringed in red.
 */
import React from "react";
import { AbsoluteFill, Sequence, interpolate } from "remotion";
import { Camera, Page } from "../../components/Shell";
import { SceneClock, camPath, sceneTiming, useAct, useBeats } from "../clock";
import { PROOF_Y, ProofContent, cosineCues, layoutProof } from "../ProofPage";
import { extent } from "../../components/Stage";
import { SINE_END_CAM, SinePage } from "./SineProof";
import { HEAD, InkPath, Layer, ringPath } from "./common";

const PW = 1920;
const BOUNDS = { w: 2 * PW, h: 1080 };
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
export const DESK = "#2F2A24";

/** Two pages, spine at x = 1920, lying on the desk. */
export const Spread: React.FC<{ left: React.ReactNode; right: React.ReactNode; veil?: number; lift?: number }> = ({
  left,
  right,
  veil = 0,
  lift = 0,
}) => (
  <div style={{ position: "relative", width: 2 * PW, height: 1080 }}>
    {/* the book's shadow on the desk (only visible once the camera pulls off the page) */}
    <div style={{ position: "absolute", inset: 0, boxShadow: `0 ${30 * lift}px ${120 * lift}px rgba(0,0,0,${0.55 * lift})` }} />
    <div style={{ position: "absolute", left: 0, top: 0 }}>{left}</div>
    <div style={{ position: "absolute", left: PW, top: 0 }}>{right}</div>
    {/* veil: quiet everything below the statements when comparing */}
    {veil > 0 && (
      <div
        style={{
          position: "absolute",
          left: 0,
          top: 410,
          width: 2 * PW,
          height: 1080 - 410,
          background: `linear-gradient(180deg, rgba(244,239,228,0) 0px, rgba(244,239,228,${0.72 * veil}) 60px)`,
        }}
      />
    )}
    {/* the gutter: pages curve down into the spine */}
    <div
      style={{
        position: "absolute",
        left: PW - 140,
        top: 0,
        width: 280,
        height: 1080,
        background:
          "linear-gradient(90deg, rgba(60,40,15,0) 0%, rgba(60,40,15,0.05) 30%, rgba(60,40,15,0.22) 49.6%, rgba(60,40,15,0.30) 50%, rgba(60,40,15,0.2) 50.4%, rgba(60,40,15,0.05) 70%, rgba(60,40,15,0) 100%)",
      }}
    />
  </div>
);

export const CosineProof: React.FC = () => {
  const act = useAct();
  const sin = sceneTiming(act, "derivative_of_sine");
  const { frame, at } = useBeats();
  const c = cosineCues(at);
  const C = at("compare");
  const R = PW; // right page offset
  const cam = camPath(frame, SINE_END_CAM, BOUNDS, [
    { f: 8, to: { cx: R + 960, cy: 540, s: 1 }, len: 54 },
    { f: c.statement - 8, to: { cx: R + 800, cy: 330, s: 1.75 }, len: 40 },
    { f: c.definition - 4, to: { cx: R + 930, cy: 560, s: 1.1 }, len: 44 },
    { f: c.fly - 8, to: { cx: R + 840, cy: PROOF_Y.l2 - 40, s: 1.24 }, len: 44 },
    { f: c.lim1 - 6, to: { cx: R + 820, cy: 660, s: 1.22 }, len: 40 },
    { f: c.qed2, to: { cx: R + 900, cy: 520, s: 1.08 }, len: 40 },
    { f: C - 4, to: { cx: PW, cy: 470, s: 0.52 }, len: 56 },
  ]);
  const cmp = interpolate(frame, [C, C + 40], [0, 1], clamp);
  // compare: a second, heavier ring on the lone minus sign
  const lay = layoutProof("cos");
  const mx = extent(lay.P, lay.stmt, "sM");
  const ring = ringPath(mx.cx, PROOF_Y.stmt - 0.26 * lay.stmt.sM.size, 36, 30, 0);
  return (
    <AbsoluteFill style={{ backgroundColor: DESK }}>
      <Camera {...cam}>
        <Spread
          veil={cmp}
          lift={cmp}
          left={
            <SceneClock timing={sin}>
              {/* the finished sine page: its clock runs past its end, where every mark is settled
                  (a <Freeze> would clamp to THIS composition's shorter duration) */}
              <Sequence from={-sin.dur} layout="none">
                <Page head={{ ...HEAD, folio: "113" }}>
                  <SinePage />
                </Page>
              </Sequence>
            </SceneClock>
          }
          right={
            <Page head={{ ...HEAD, folio: "114" }}>
              <ProofContent v="cos" cues={c} />
              <Layer>
                <InkPath d={ring.d} len={ring.len} p={interpolate(frame, [C + 36, C + 60], [0, 1], clamp)} w={6} />
              </Layer>
            </Page>
          }
        />
      </Camera>
    </AbsoluteFill>
  );
};
