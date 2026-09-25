/** Logo open (silent): the brand lockup inks on in the middle of a blank sheet, as on the §3.1 title page. */
import React from "react";
import { interpolate } from "remotion";
import { color } from "../../theme";
import { BrandLockup } from "../../components/Shell";
import { Rule, clamp } from "../../components/Type";
import { Sheet, useS, wipe } from "../kit";
import { CJK_STACK, useCjkReady } from "../cjk";
import { ZH } from "../zh";

/** the lockup artwork sits in the left part of its 1040×300 box: its visual centre is at 36.45 % of the width */
export const INK_CENTRE = 0.3645;

export const Logo: React.FC = () => {
  const { f, pf } = useS();
  const cjk = useCjkReady();
  const H = 250;
  const W = (H * 1040) / 300;
  const s = interpolate(f, [0, 110], [1.05, 1], { ...clamp });
  return (
    <Sheet folio={0} title="" head={false} device={false} cam={{ cx: 960, cy: 540, s }}>
      <div style={{ position: "absolute", left: 960 - INK_CENTRE * W, top: 430 - H / 2, width: W, height: H, ...wipe(pf(6, 34), 0) }}>
        <BrandLockup x={0} y={0} h={H} />
      </div>
      <Rule x={960 - 150} y={600} w={300} from={34} len={22} color={color.accent} weight={2.5} />
      {cjk && (
        <div
          style={{
            position: "absolute",
            left: 0,
            width: 1920,
            top: 632,
            textAlign: "center",
            fontFamily: CJK_STACK,
            fontSize: 38,
            letterSpacing: "0.1em",
            paddingLeft: "0.1em", // balance the tracking after the last glyph
            color: color.ink2,
            fontFeatureSettings: "'kern' 1, 'lnum' 1",
            whiteSpace: "nowrap",
            ...wipe(pf(44, 22), 0),
          }}
        >
          {ZH.logoSub}
        </div>
      )}
    </Sheet>
  );
};
