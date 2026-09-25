/** C14 — what we can't do yet (a function inside a function) → §3.2 the chain rule. End page with the lockup. */
import React from "react";
import { color, font, type } from "../../theme";
import { BrandLockup } from "../../components/Shell";
import { Rule, SmallCaps } from "../../components/Type";
import { M, Sheet, Txt, camPath, useS, wipe } from "../kit";

const A = color.accent;
const O = color.ochre;

export const Next: React.FC = () => {
  const { f, at, p, dur } = useS();
  const cam = camPath(f, { cx: 960, cy: 420, s: 1.3 }, [
    [at("chain") - 10, { cx: 960, cy: 540, s: 1 }, 60],
    [at("chain") + 60, { cx: 960, cy: 548, s: 1.03 }, dur - at("chain") - 60],
  ]);
  const inside = p("inside", 30);
  const out = 1 - 0.8 * p("chain", 30);
  return (
    <Sheet folio={126} title="" head={false} device={false} cam={cam}>
      <div style={{ opacity: out }}>
        <Txt x={960} y={120} w={900} align="center" size={type.caption} italic c={color.ink2} p={p("start", 24, 6)}>
          We can differentiate
        </Txt>
        <M x={960} y={320} align="center" size={96} p={p("start", 30, 14)} t={`{\\color{${A}}\\frac{d}{dx}}\\sin x`} />
        <M x={620} y={500} align="center" size={80} p={inside} t={`\\sin\\big(\\,{\\color{${O}}x^2}\\,\\big)`} />
        <M x={1300} y={500} align="center" size={80} p={p("inside", 30, 16)} t={`\\sin\\big(\\,{\\color{${O}}3x+1}\\,\\big)`} />
        <Txt x={960} y={396} w={600} align="center" size={40} italic c={A} p={inside}>
          but what about
        </Txt>
        <Txt x={960} y={560} w={900} align="center" size={type.caption} italic c={color.ink2} p={p("inside", 26, 50)}>
          a function inside a function
        </Txt>
      </div>

      {/* end page */}
      <Rule x={660} y={660} w={600} from={at("chain") + 10} len={30} />
      <div style={{ position: "absolute", left: 0, width: 1920, top: 690, textAlign: "center", ...wipe(p("chain", 26, 16), 0) }}>
        <SmallCaps color={A}>Next · Section 3.2</SmallCaps>
      </div>
      <Txt x={960} y={736} w={1200} align="center" size={type.h2 + 8} weight={500} p={p("chain", 30, 26)}>
        The Chain Rule
      </Txt>
      <div
        style={{
          position: "absolute",
          left: 960 - 243,
          top: 850,
          width: 490,
          height: 144,
          ...wipe(p("chain", 30, 60), 0),
        }}
      >
        <BrandLockup x={0} y={0} h={140} />
      </div>
      <div style={{ position: "absolute", left: 0, width: 1920, top: 1012, textAlign: "center", fontFamily: font.serif, ...wipe(p("chain", 26, 80), 0) }}>
        <SmallCaps color={color.ink3}>End of Section 3.1</SmallCaps>
      </div>
    </Sheet>
  );
};
