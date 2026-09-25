/**
 * outro — the colophon: end of the section, what comes next, the brand.
 * Silent (its length is the manifest's `duration`); set symmetrically, the
 * only centred page in the act, so it reads as an ending.
 */
import React from "react";
import { interpolate, useCurrentFrame } from "remotion";
import { color, features, font, semantic } from "../../theme";
import { BrandLockup } from "../../components/Shell";
import { InkReveal, Rule, SmallCaps, clamp } from "../../components/Type";
import { Curve, Dot, PlotFrame, Tangent } from "../../components/Plot";
import { PAGE, camPath, useTiming } from "../clock";
import { Layer, Sheet } from "./common";

const FL: PlotFrame = { ox: 960 - Math.PI * 60, oy: 250, ux: 60, uy: 56 };

export const Outro: React.FC = () => {
  const frame = useCurrentFrame();
  const { dur } = useTiming();
  const cam = camPath(frame, { cx: 960, cy: 540, s: 1.06 }, PAGE, [{ f: 0, to: { cx: 960, cy: 540, s: 1 }, len: 150 }]);
  const x0 = interpolate(frame, [10, Math.max(60, dur - 20)], [0.4, 2 * Math.PI - 0.4], clamp);
  const ink = interpolate(frame, [6, 40], [0, 1], clamp);
  const lockW = (130 * 1040) / 300;
  return (
    <Sheet cam={cam} head={null} device={false}>
      <Layer>
        <Curve f={FL} fn={Math.sin} a={0} b={2 * Math.PI} progress={ink} c={semantic.sin} width={3} />
        <Tangent f={FL} x0={x0} y0={Math.sin(x0)} m={Math.cos(x0)} half={70} width={2.8} grow={ink} />
        <Dot f={FL} x={x0} y={Math.sin(x0)} r={6} scale={ink} />
      </Layer>
      <InkReveal from={12} len={24} style={{ left: 460, top: 360, width: 1000, height: 40, textAlign: "center" }}>
        <SmallCaps color={color.accent}>End of Section 3.1</SmallCaps>
      </InkReveal>
      <InkReveal from={20} len={30} style={{ left: 260, top: 420, width: 1400, height: 90, textAlign: "center" }}>
        <div style={{ fontFamily: font.serif, fontStyle: "italic", fontSize: 50, color: color.ink2, fontFeatureSettings: features.text }}>
          Next
        </div>
      </InkReveal>
      <InkReveal from={30} len={34} style={{ left: 160, top: 488, width: 1600, height: 140, textAlign: "center" }}>
        <div style={{ fontFamily: font.serif, fontSize: 104, fontWeight: 500, color: color.ink, letterSpacing: "-0.01em", fontFeatureSettings: features.text }}>
          <span style={{ color: color.accent, fontStyle: "italic" }}>§</span>3.2&ensp;The Chain Rule
        </div>
      </InkReveal>
      <Rule x={880} y={690} w={160} weight={3} color={color.accent} from={44} len={20} />
      <InkReveal from={52} len={34} style={{ left: 960 - lockW / 2, top: 780, width: lockW, height: 140 }}>
        <BrandLockup x={0} y={0} h={130} />
      </InkReveal>
    </Sheet>
  );
};
