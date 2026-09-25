/** C7, C8 — both debts paid: the limits of the two factors give d/dx sin = cos; cos goes the same way. */
import React from "react";
import { color } from "../../theme";
import { SmallCaps } from "../../components/Type";
import { Arrow, Kicker, Layer, M, Sheet, Txt, camPath, texW, useS, wipe } from "../kit";

const C = color.cobalt;
const A = color.accent;
const X = 470;
const SZ = 66;
const LHS = "\\frac{\\sin(x+h)-\\sin x}{h}=";
const COSF = `{\\color{${C}}\\cos\\!\\left(x+\\tfrac{h}{2}\\right)}`;
const RATIO = "\\frac{\\sin(h/2)}{h/2}";

const TheoremBox: React.FC<{ x: number; y: number; n: string; t: string; p: number }> = ({ x, y, n, t, p }) => (
  <>
    <div style={{ position: "absolute", left: x, top: y, width: 5, height: 170 * p, background: A }} />
    <div style={{ position: "absolute", left: x + 30, top: y + 4, ...wipe(p, 0) }}>
      <SmallCaps color={A}>Theorem {n}</SmallCaps>
    </div>
    <M x={x + 30} y={y + 130} size={104} p={p} t={t} />
  </>
);

export const Payoff: React.FC = () => {
  const { f, at, p, pf, atWord } = useS();
  const w0 = texW(LHS, SZ);
  const w1 = texW(LHS + COSF, SZ);
  const w2 = texW(LHS + COSF + "\\cdot", SZ);
  const w3 = texW(LHS + COSF + "\\cdot" + RATIO, SZ);
  const cA = X + (w0 + w1) / 2;
  const cB = X + (w2 + w3) / 2;
  const cam = camPath(f, { cx: 1000, cy: 360, s: 1.3 }, [
    [at("theorem") - 6, { cx: 960, cy: 540, s: 1 }, 50],
    [at("cosine"), { cx: 1000, cy: 800, s: 1.2 }, 60],
    [at("theorem2"), { cx: 960, cy: 620, s: 1 }, 60],
  ]);
  const lim = p("limits", 30);
  // the second factor's limit value ("1") appears as the narration names it ("...goes to one")
  const oneAt = atWord("one", { afterFrame: at("limits") }) ?? at("limits") + Math.round((at("theorem") - at("limits")) * 0.45);
  const lim2 = pf(oneAt, 30);
  return (
    <Sheet folio={120} title="The two derivatives" cam={cam} h={1240}>
      <Kicker x={X} y={140} p={p("start", 24)}>
        Collecting
      </Kicker>
      <M x={X} y={300} size={SZ} p={p("start", 34, 8)} t={LHS + COSF + "\\cdot" + RATIO} />
      <Layer h={1240}>
        <Arrow x1={cA} y1={352} x2={cA} y2={420} p={lim} c={C} w={2.6} head={13} />
        <Arrow x1={cB} y1={372} x2={cB} y2={420} p={lim2} c={A} w={2.6} head={13} />
      </Layer>
      <M x={cA} y={480} align="center" size={56} c={C} p={p("limits", 24, 16)} t="\cos x" />
      <Txt x={cA} y={500} w={420} align="center" size={30} italic c={color.ink2} p={p("limits", 24, 30)}>
        by continuity ¹
      </Txt>
      <M x={cB} y={480} align="center" size={56} c={A} p={lim2} t="1" />
      <Txt x={cB} y={500} w={420} align="center" size={30} italic c={color.ink2} p={pf(oneAt + 14, 24)}>
        by the key limit ²
      </Txt>
      <TheoremBox
        x={X}
        y={580}
        n="1"
        p={p("theorem", 34)}
        t={`{\\color{${A}}\\tfrac{d}{dx}}\\sin x={\\color{${C}}\\cos x}`}
      />

      <M
        x={X}
        y={815}
        size={40}
        c={color.ink2}
        p={p("cosine", 26)}
        t="\text{with}\quad \cos A-\cos B=-2\sin\tfrac{A+B}{2}\,\sin\tfrac{A-B}{2}:"
      />
      <M
        x={X}
        y={915}
        size={62}
        p={p("cosine", 34, 60)}
        t={`\\frac{{\\color{${C}}\\cos(x+h)-\\cos x}}{h}=-\\sin\\!\\left(x+\\tfrac{h}{2}\\right)\\cdot${RATIO}\\ \\longrightarrow\\ -\\sin x`}
      />
      <TheoremBox x={X} y={990} n="2" p={p("theorem2", 34)} t={`{\\color{${A}}\\tfrac{d}{dx}}{\\color{${C}}\\cos x}=-\\sin x`} />
    </Sheet>
  );
};
