/** C11 — tan by the quotient rule; the other three in a booktabs table; the "co-" minus signs. */
import React from "react";
import { color } from "../../theme";
import { SmallCaps } from "../../components/Type";
import { Kicker, Layer, M, Sheet, Txt, useS, wipe } from "../kit";

const A = color.accent;
const C = color.cobalt;
const FX = 300; // derivation column (no marginalia on this page: the block is centred as a whole)
const TX = 1280; // table left
const rows: Array<{ f: string; d: string; co: boolean; dCo: string }> = [
  { f: "\\tan x", d: "\\sec^2 x", co: false, dCo: "" },
  { f: "\\sec x", d: "\\sec x\\,\\tan x", co: false, dCo: "" },
  { f: "\\cot x", d: "-\\csc^2 x", co: true, dCo: `{\\color{${A}}-}\\csc^2 x` },
  { f: "\\csc x", d: "-\\csc x\\,\\cot x", co: true, dCo: `{\\color{${A}}-}\\csc x\\,\\cot x` },
];

export const Four: React.FC = () => {
  const { at, p, pf, atWord } = useS();
  // camera locked on the page. Focus shifts by dimming: the finished derivation recedes while the
  // table fills; the "co-" minus signs turn red as the narration names the pattern.
  const coAt = atWord("co", { afterFrame: at("co") }) ?? at("co", 0.4);
  const co = pf(coAt - 6, 30);
  const recede = 1 - 0.45 * p("table", 30);
  const rowY = (i: number) => 470 + i * 100;
  const rowP = (i: number) => (i === 0 ? p("sec", 30, 30) : p("table", 26, 30 + (i - 1) * 40));
  return (
    <Sheet folio={123} title="The other four">
      <div style={{ opacity: recede }}>
      <Kicker x={FX} y={140} p={p("start", 24)}>
        Quotient rule
      </Kicker>
      <M x={FX} y={290} size={62} p={p("tan", 30)} t={`{\\color{${A}}\\frac{d}{dx}}\\tan x={\\color{${A}}\\frac{d}{dx}}\\frac{\\sin x}{{\\color{${C}}\\cos x}}`} />
      <M
        x={FX}
        y={460}
        size={60}
        p={p("quotient", 34)}
        t={`=\\frac{{\\color{${C}}\\cos x}\\cdot{\\color{${C}}\\cos x}-\\sin x\\cdot(-\\sin x)}{{\\color{${C}}\\cos^2 x}}`}
      />
      <M x={FX} y={630} size={60} p={p("one", 30)} t={`=\\frac{{\\color{${A}}\\cos^2x+\\sin^2x}}{\\cos^2 x}=\\frac{{\\color{${A}}1}}{\\cos^2x}`} />
      <M x={FX} y={790} size={76} p={p("sec", 30)} t={`=\\sec^2 x`} />
      <Txt x={FX} y={850} w={600} size={30} italic c={color.ink2} p={p("sec", 24, 40)}>
        wherever cos x ≠ 0
      </Txt>
      </div>

      {/* booktabs table */}
      <div style={{ position: "absolute", left: TX, top: 330, ...wipe(p("table", 24, 0), 0) }}>
        <SmallCaps color={A}>Table 3.1</SmallCaps>
      </div>
      <Layer>
        <line x1={TX} y1={378} x2={TX + 520} y2={378} stroke={color.ink} strokeWidth={2.6} opacity={p("sec", 20, 10)} />
        <line x1={TX} y1={420} x2={TX + 520} y2={420} stroke={color.ink} strokeWidth={1.3} opacity={p("sec", 20, 16)} />
        <line x1={TX} y1={500 + 3 * 100} x2={TX + 520} y2={500 + 3 * 100} stroke={color.ink} strokeWidth={2.6} opacity={p("table", 20, 150)} />
        {co > 0 &&
          [2, 3].map((i) => <line key={i} x1={TX} y1={rowY(i) + 12} x2={TX + 34} y2={rowY(i) + 12} stroke={A} strokeWidth={3} opacity={co} />)}
      </Layer>
      <M x={TX} y={408} size={36} c={color.ink2} p={p("sec", 20, 16)} t="f(x)" />
      <M x={TX + 260} y={408} size={36} c={color.ink2} p={p("sec", 20, 16)} t="f'(x)" />
      {rows.map((r, i) => (
        <React.Fragment key={r.f}>
          <M x={TX} y={rowY(i)} size={52} p={rowP(i)} t={r.f} />
          <M x={TX + 260} y={rowY(i)} size={52} p={rowP(i)} o={r.co ? 1 - co : 1} t={r.d} />
          {r.co && <M x={TX + 260} y={rowY(i)} size={52} p={co} t={r.dCo} />}
        </React.Fragment>
      ))}
      <Txt x={TX} y={830} w={520} size={30} italic c={color.ink2} p={p("table", 24, 170)}>
        each wherever its denominator is not zero
      </Txt>
      <Txt x={TX} y={890} w={520} size={36} italic c={A} p={p("co", 26, 30)}>
        Every co-function picks up a minus sign.
      </Txt>
    </Sheet>
  );
};
