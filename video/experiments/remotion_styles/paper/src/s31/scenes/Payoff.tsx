/** C7, C8 — both debts paid: the limits of the two factors give d/dx sin = cos; cos goes the same way. */
import React from "react";
import { interpolate } from "remotion";
import { color } from "../../theme";
import { SmallCaps, clamp } from "../../components/Type";
import { Arrow, HOME, Kicker, Layer, M, Sheet, Txt, camPath, texW, useS, wipe } from "../kit";

const C = color.cobalt;
const A = color.accent;
const SZ = 66; // both quotient rows (sine and cosine) are the same object at the same size
const H = 1280;
const LHS = "\\frac{\\sin(x+h)-\\sin x}{h}=";
const COSF = `{\\color{${C}}\\cos\\!\\left(x+\\tfrac{h}{2}\\right)}`;
const RATIO = "\\frac{\\sin(h/2)}{h/2}";
const SINROW = LHS + COSF + "\\cdot" + RATIO;
const COSROW = `\\frac{{\\color{${C}}\\cos(x+h)-\\cos x}}{h}=-\\sin\\!\\left(x+\\tfrac{h}{2}\\right)\\cdot${RATIO}\\ \\longrightarrow\\ -\\sin x`;

const TheoremBox: React.FC<{ x: number; y: number; n: string; t: string; p: number }> = ({ x, y, n, t, p }) => (
  <>
    {/* label sits above the rule so the full-size d/dx numerator has the whole box height */}
    <div style={{ position: "absolute", left: x, top: y - 38, ...wipe(p, 0) }}>
      <SmallCaps color={A}>Theorem {n}</SmallCaps>
    </div>
    <div style={{ position: "absolute", left: x, top: y, width: 5, height: 170 * p, background: A }} />
    <M x={x + 30} y={y + 124} size={104} p={p} t={t} />
  </>
);

export const Payoff: React.FC = () => {
  const { f, at, p, pf, atWord } = useS();
  // the block is set flush-left on a common edge, centred on the page by its widest line
  // (the cosine row) so the resting page is balanced and nothing runs into the right margin.
  const X = Math.round(960 - Math.max(texW(SINROW, SZ), texW(COSROW, SZ)) / 2);
  const w0 = texW(LHS, SZ);
  const w1 = texW(LHS + COSF, SZ);
  const w2 = texW(LHS + COSF + "\\cdot", SZ);
  const w3 = texW(LHS + COSF + "\\cdot" + RATIO, SZ);
  const cA = X + (w0 + w1) / 2;
  const cB = X + (w2 + w3) / 2;
  // two regions on a tall sheet: sine (top 1080) then cosine (bottom). ONE move, in the gap after
  // Theorem 1 has inked and before the cosine line is written; the sine rows stay in view below it.
  const cam = camPath(f, HOME, [[at("cosine") - 44, { cx: 960, cy: H - 540, s: 1 }, 40]]);
  const kick = 1 - interpolate(cam.cy, [540, 600], [0, 1], clamp); // the kicker would be clipped: fade it
  const lim = p("limits", 30);
  // the second factor's limit value ("1") appears as the narration names it ("...goes to one")
  const oneAt = atWord("one", { afterFrame: at("limits") }) ?? at("limits") + Math.round((at("theorem") - at("limits")) * 0.45);
  const lim2 = pf(oneAt, 30);
  return (
    <Sheet folio={120} title="The two derivatives" cam={cam} h={H}>
      <div style={{ opacity: kick }}>
        <Kicker x={X} y={140} p={p("start", 24)}>
          Collecting
        </Kicker>
      </div>
      <M x={X} y={300} size={SZ} p={p("start", 34, 8)} t={SINROW} />
      <Layer h={H}>
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
        y={600}
        n="1"
        p={p("theorem", 34)}
        t={`{\\color{${A}}\\frac{d}{dx}}\\sin x={\\color{${C}}\\cos x}`}
      />

      {/* a side remark (inline), then the cosine row at the same size as the sine row */}
      <M
        x={X}
        y={842}
        size={40}
        c={color.ink2}
        display={false}
        p={p("cosine", 26)}
        t="\text{with}\quad \cos A-\cos B=-2\sin\tfrac{A+B}{2}\,\sin\tfrac{A-B}{2}:"
      />
      <M x={X} y={942} size={SZ} p={p("cosine", 34, 60)} t={COSROW} />
      <TheoremBox x={X} y={1046} n="2" p={p("theorem2", 34)} t={`{\\color{${A}}\\frac{d}{dx}}{\\color{${C}}\\cos x}=-\\sin x`} />
    </Sheet>
  );
};
