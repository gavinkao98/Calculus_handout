/**
 * derivative_of_sine — the theorem page (verso).  The camera works the page
 * like a reader's eye: statement close-up → proof line → over to the margin
 * for the identity → back as the product flies home → down to the limits →
 * pull back to the whole page (which is exactly where the facing-page slide
 * of the next scene picks up).
 */
import React from "react";
import { Cam, PAGE, camPath, useBeats } from "../clock";
import { PROOF_Y, ProofContent, sineCues } from "../ProofPage";
import { HEAD, Sheet } from "./common";

export const SINE_END_CAM: Cam = { cx: 960, cy: 540, s: 1 };

export const SinePage: React.FC = () => {
  const { at } = useBeats();
  return <ProofContent v="sin" cues={sineCues(at)} />;
};

export const SineProof: React.FC = () => {
  const { frame, at, dur } = useBeats();
  const c = sineCues(at);
  const cam = camPath(
    frame,
    { cx: 960, cy: 540, s: 1 },
    PAGE,
    [
      { f: c.statement - 8, to: { cx: 1135, cy: 330, s: 1.75 }, len: 40 },
      { f: c.definition - 4, to: { cx: 1060, cy: 470, s: 1.25 }, len: 48 },
      { f: c.idA - 4, to: { cx: 690, cy: 600, s: 1.4 }, len: 40 },
      { f: c.fly - 8, to: { cx: 1030, cy: PROOF_Y.l2 - 60, s: 1.26 }, len: 44 },
      { f: c.lim1 - 6, to: { cx: 1060, cy: 660, s: 1.22 }, len: 40 },
      { f: c.qed2, to: SINE_END_CAM, len: Math.min(46, dur - c.qed2 - 2) },
    ],
  );
  return (
    <Sheet cam={cam} head={{ ...HEAD, folio: "113" }}>
      <SinePage />
    </Sheet>
  );
};
