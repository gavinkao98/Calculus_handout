/** C2 — sum-to-product; the "2" slides under the h; two factors, two debts. */
import React from "react";
import { color, type } from "../../theme";
import { MathStage, Piece, extent, row } from "../../components/Stage";
import { Arrow, Kicker, Layer, Ledger, M, Sheet, Txt, useS } from "../kit";

const C = color.cobalt;
const SZ = 72;
const Y = 650;
const X = 470;

const P: Record<string, Piece> = {
  lhs: { tex: "\\dfrac{\\sin(x+h)-\\sin x}{h}" },
  eq: { tex: "=" },
  two: { tex: "2" },
  cosf: { tex: "\\cos\\!\\left(x+\\tfrac{h}{2}\\right)", color: C },
  sinf: { tex: "\\sin(h/2)" },
  hden: { tex: "h" },
  sl: { tex: "/" },
  dot: { tex: "\\cdot" },
  bar: { bar: true },
};

export const Rewrite: React.FC = () => {
  const { at, p, atWord } = useS();
  const k1 = row(P, ["lhs", ["eq", 0.3], { num: ["two", ["cosf", 0.08], ["sinf", 0.1]], den: ["hden"], bar: "bar", gap: 0.3 }], X, Y, SZ);
  const k2 = row(P, ["lhs", ["eq", 0.3], ["cosf", 0.3], ["dot", 0.14], { num: ["sinf"], den: ["hden", ["sl", 0.02], ["two", 0.02]], bar: "bar", gap: 0.14 }], X, Y, SZ);
  // the substituted formula lands as the narration finishes naming A and B ("...and B equal to x")
  const k1At = atWord("B equal to", { afterFrame: at("substitute") }) ?? at("substitute", 0.35);
  const keys = [
    { at: k1At, poses: k1 },
    { at: at("split") + 8, poses: k2 },
  ];
  const ec = extent(P, k2, "cosf");
  const eb = extent(P, k2, "bar");
  // a derivation: the camera is locked on the whole page; the identity, the substitution and the
  // rewritten quotient all stay in view while the two debts are drawn beneath it.
  const o1 = p("owe1", 26);
  const o2 = p("owe2", 26);
  const led = p("ledger", 26, 10);
  return (
    <Sheet folio={115} title="Two debts">
      <Kicker x={X} y={140} p={p("start", 24, 10)}>
        Sum to product
      </Kicker>
      <M
        x={X}
        y={300}
        size={76}
        p={p("identity", 34)}
        t={`\\sin A-\\sin B=2\\,{\\color{${C}}\\cos\\tfrac{A+B}{2}}\\,\\sin\\tfrac{A-B}{2}`}
      />
      <M x={X} y={400} size={40} c={color.ink2} p={p("identity", 30, 90)} t="\text{from}\quad \sin(u+v)-\sin(u-v)=2\cos u\,\sin v" />
      <M x={X} y={500} size={50} c={color.ink2} p={p("substitute", 26)} t="A=x+h,\qquad B=x" />
      <Layer>
        <MathStage pieces={P} keys={keys} />
        {/* debt 1: the cosine factor */}
        <Arrow x1={ec.cx} y1={Y + 62} x2={ec.cx} y2={Y + 132} p={o1} c={C} w={2.6} head={13} />
        {/* debt 2: the ratio */}
        <Arrow x1={eb.cx} y1={Y + 128} x2={eb.cx} y2={Y + 190} p={o2} c={color.accent} w={2.6} head={13} />
      </Layer>
      <M x={ec.cx} y={Y + 196} align="center" size={56} c={C} p={p("owe1", 24, 12)} t="\cos x" />
      <Txt x={ec.cx} y={Y + 222} w={560} align="center" size={type.caption} italic c={color.ink2} p={p("owe1", 24, 30)}>
        if cos is continuous<sup style={{ color: color.accent, fontStyle: "normal", fontSize: "0.7em" }}> 1</sup>
      </Txt>
      <M x={eb.cx - 30} y={Y + 110} align="right" size={40} c={color.ink2} p={p("owe2", 24, 4)} display={false} t="\theta=h/2\to0" />
      <M x={eb.cx} y={Y + 290} align="center" size={56} p={p("owe2", 24, 12)} t={`\\frac{\\sin\\theta}{\\theta}\\to{\\color{${color.accent}}\\,?}`} />
      <Txt x={eb.cx} y={Y + 326} w={560} align="center" size={type.caption} italic c={color.ink2} p={p("owe2", 24, 30)}>
        we need this to be 1<sup style={{ color: color.accent, fontStyle: "normal", fontSize: "0.7em" }}> 2</sup>
      </Txt>
      <Ledger
        x={120}
        y={560}
        st={{ show: led, items: [{ show: p("ledger", 24, 30), paid: 0 }, { show: p("ledger", 24, 60), paid: 0 }] }}
      />
    </Sheet>
  );
};
