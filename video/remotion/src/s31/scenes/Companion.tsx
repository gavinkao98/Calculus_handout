/** C10 — (1 − cosθ)/θ → 0, by the conjugate and the key limit. */
import React from "react";
import { color } from "../../theme";
import { Arrow, Kicker, Layer, M, Sheet, Txt, texW, useS } from "../kit";

const A = color.accent;
const XE = 800; // the column of "=" signs
const SZ = 64;
const R2 = "=\\frac{\\sin\\theta}{\\theta}\\cdot\\frac{\\sin\\theta}{1+\\cos\\theta}";

export const Companion: React.FC = () => {
  const { at, p, pf, atWord } = useS();
  // derivation page, camera locked: every line of the conjugate trick stays on the sheet.
  // The second factor's value inks as the narration names it ("...goes to zero over two").
  const evalAt = atWord("zero over two", { afterFrame: at("evaluate") }) ?? at("evaluate") + 50;
  const wEq = texW("=", SZ);
  const c1 = XE + (wEq + texW("=\\frac{\\sin\\theta}{\\theta}", SZ)) / 2;
  const c2 = XE + (texW("=\\frac{\\sin\\theta}{\\theta}\\cdot", SZ) + texW(R2, SZ)) / 2;
  const ev = p("evaluate", 26);
  const ev2 = pf(evalAt - 8, 26);
  const fin = p("evaluate", 34, 110);
  return (
    <Sheet folio={122} title="A companion limit">
      <Kicker x={470} y={140} p={p("start", 24)}>
        The key limit, reused
      </Kicker>
      <M x={XE - 24} y={320} align="right" size={SZ} p={p("start", 30, 10)} t="\frac{1-\cos\theta}{\theta}" />
      <M
        x={XE}
        y={320}
        size={SZ}
        p={p("conj", 30)}
        t={`=\\frac{1-\\cos\\theta}{\\theta}\\cdot{\\color{${A}}\\frac{1+\\cos\\theta}{1+\\cos\\theta}}`}
      />
      <M x={XE} y={480} size={SZ} p={p("pythag", 30)} t="=\frac{1-\cos^2\theta}{\theta\,(1+\cos\theta)}" />
      <M x={XE + texW("=\\frac{1-\\cos^2\\theta}{\\theta\\,(1+\\cos\\theta)}", SZ) + 20} y={480} size={SZ} p={p("pythag", 30, 50)} t={`=\\frac{{\\color{${A}}\\sin^2\\theta}}{\\theta\\,(1+\\cos\\theta)}`} />
      <Txt x={470} y={440} w={300} size={34} italic c={color.ink2} p={p("pythag", 24, 60)}>
        sin² + cos² = 1
      </Txt>
      <M x={XE} y={640} size={SZ} p={p("factor", 30)} t={R2} />
      <Layer>
        <Arrow x1={c1} y1={700} x2={c1} y2={760} p={ev} c={A} w={2.6} head={13} />
        <Arrow x1={c2} y1={710} x2={c2} y2={760} p={ev2} c={color.ink2} w={2.6} head={13} />
        <rect x={660} y={872} width={600} height={140} fill="none" stroke={A} strokeWidth={2.4} opacity={fin} />
      </Layer>
      <M x={c1} y={815} align="center" size={54} c={A} p={p("evaluate", 24, 12)} t="1" />
      <M x={c2} y={815} align="center" size={54} p={ev2} t="\frac{0}{2}=0" />
      <M x={960} y={962} align="center" size={70} p={fin} t={`\\lim_{\\theta\\to0}\\frac{1-\\cos\\theta}{\\theta}={\\color{${A}}0}`} />
    </Sheet>
  );
};
