/** Outro (silent): the colophon, centred like the act-3 outro — end mark, the answer, the lockup. */
import React from "react";
import { interpolate, useCurrentFrame } from "remotion";
import { color, features, font } from "../../theme";
import { BrandLockup } from "../../components/Shell";
import { InkReveal, Rule, SmallCaps, clamp } from "../../components/Type";
import { Ball, HOMEC, Layer, POCKET, Sheet, Table, World, dOf } from "../kit";
import { polyAt, realPath, shot } from "../geo";
import { INK_CENTRE } from "./Logo";

const HOMEPATH = realPath(shot([2, 1], 2));

export const Outro: React.FC = () => {
  const f = useCurrentFrame();
  const s = interpolate(f, [0, 150], [1.05, 1], clamp);
  const W: World = { ox: 960, oy: 250, u: 80 };
  const lap = interpolate(((f - 20) % 110 + 110) % 110, [0, 90], [0, 1], clamp);
  const ink = interpolate(f, [4, 34], [0, 1], clamp);
  const lockW = (130 * 1040) / 300;
  return (
    <Sheet folio={0} title="" head={false} device={false} cam={{ cx: 960, cy: 540, s }}>
      <Layer>
        <Table W={W} real draw={ink} />
        {ink >= 1 && (
          <g>
            <path d={dOf(W, HOMEPATH)} fill="none" stroke={color.rule} strokeWidth={2} strokeDasharray="2 7" />
            <path d={dOf(W, polyAt(HOMEPATH, lap).upto)} fill="none" stroke={color.ink} strokeWidth={2.6} strokeLinejoin="round" />
            <Ball W={W} p={polyAt(HOMEPATH, lap).p} r={8} />
          </g>
        )}
      </Layer>
      <InkReveal from={16} len={24} style={{ left: 460, top: 380, width: 1000, height: 40, textAlign: "center" }}>
        <SmallCaps color={color.accent}>End of Problem 7</SmallCaps>
      </InkReveal>
      <InkReveal from={26} len={34} style={{ left: 160, top: 430, width: 1600, height: 130, textAlign: "center" }}>
        <div style={{ fontFamily: font.serif, fontSize: 92, fontWeight: 500, color: color.ink, letterSpacing: "-0.01em", fontFeatureSettings: features.text }}>
          Square Billiards
        </div>
      </InkReveal>
      <InkReveal from={40} len={30} style={{ left: 260, top: 560, width: 1400, height: 70, textAlign: "center" }}>
        <div style={{ fontFamily: font.serif, fontStyle: "italic", fontSize: 46, color: color.ink2, fontFeatureSettings: features.text }}>
          (a) <span style={{ color: HOMEC }}>infinitely many</span> &ensp;·&ensp; (b) <span style={{ color: POCKET }}>none</span>
        </div>
      </InkReveal>
      <Rule x={880} y={690} w={160} weight={3} color={color.accent} from={50} len={20} />
      <InkReveal from={58} len={34} style={{ left: 960 - INK_CENTRE * lockW, top: 780, width: lockW, height: 140 }}>
        <BrandLockup x={0} y={0} h={130} />
      </InkReveal>
    </Sheet>
  );
};
