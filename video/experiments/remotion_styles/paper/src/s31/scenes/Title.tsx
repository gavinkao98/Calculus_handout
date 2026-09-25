/** Section opener: set like the first page of a chapter; the fleuron is the circle from the cold open. */
import React from "react";
import { color, features, font, stroke, type } from "../../theme";
import { BrandLockup } from "../../components/Shell";
import { Rule, SmallCaps } from "../../components/Type";
import { Arrow, Layer, Sheet, Txt, useS, wipe } from "../kit";

const contents: Array<[string, string]> = [
  ["i", "Why sine resists algebra"],
  ["ii", "Two debts, and how to pay them"],
  ["iii", "The two derivatives"],
  ["iv", "What follows from them"],
];

export const Title: React.FC = () => {
  const { f, pf } = useS();
  const O = { x: 330, y: 720 };
  const R = 120;
  const th = 0.9 + f * 0.012;
  const P = { x: O.x + R * Math.cos(th), y: O.y - R * Math.sin(th) };
  const tip = { x: P.x - R * 0.75 * Math.sin(th), y: P.y - R * 0.75 * Math.cos(th) };
  const circ = pf(20, 40);
  return (
    <Sheet folio={112} title="" head={false} device={false} >
      <div style={{ position: "absolute", left: 120, top: 112, ...wipe(pf(8, 22), 0) }}>
        <SmallCaps>Chapter 3 · Differentiation Rules</SmallCaps>
      </div>
      <div style={{ position: "absolute", right: 120, top: 112, ...wipe(pf(12, 22), 0) }}>
        <SmallCaps>Section 3.1</SmallCaps>
      </div>
      <Rule x={120} y={150} w={1680} from={6} len={30} />

      <Txt x={104} y={236} w={700} size={type.display} p={pf(14, 30)} lh={1} style={{ letterSpacing: "-0.02em", fontFeatureSettings: "'lnum' 1, 'kern' 1" }}>
        <span style={{ color: color.accent, fontStyle: "italic", fontSize: "0.78em", marginRight: "0.04em" }}>§</span>3.1
      </Txt>
      <Layer>
        <line x1={O.x - R - 40} y1={O.y} x2={O.x + R + 40} y2={O.y} stroke={color.rule} strokeWidth={1.5} opacity={circ} />
        <line x1={O.x} y1={O.y + R + 40} x2={O.x} y2={O.y - R - 40} stroke={color.rule} strokeWidth={1.5} opacity={circ} />
        <circle cx={O.x} cy={O.y} r={R} fill="none" stroke={color.ink} strokeWidth={2.6} strokeDasharray={`${2 * Math.PI * R * circ} 9999`} />
        <line x1={O.x} y1={O.y} x2={P.x} y2={P.y} stroke={color.ink2} strokeWidth={1.6} opacity={circ} />
        <Arrow x1={P.x} y1={P.y} x2={tip.x} y2={tip.y} p={pf(46, 22)} c={color.accent} w={3} head={13} />
        <circle cx={P.x} cy={P.y} r={stroke.dot - 1} fill={color.ink} stroke={color.paper} strokeWidth={stroke.ring} opacity={circ} />
      </Layer>

      <Rule x={800} y={262} w={560} vertical from={10} len={34} />

      <Txt x={870} y={250} w={930} size={type.title} weight={500} lh={1.02} p={pf(22, 32)} style={{ letterSpacing: "-0.012em" }}>
        Derivatives of
        <br />
        Sine and Cosine
      </Txt>
      <div style={{ position: "absolute", left: 870, top: 488, width: 84 * pf(40, 20), height: 3, background: color.accent }} />
      <Txt x={870} y={516} w={930} size={50} italic c={color.ink2} p={pf(46, 26)}>
        How fast does sine change?
      </Txt>
      {contents.map(([n, label], i) => (
        <div
          key={n}
          style={{
            position: "absolute",
            left: 870,
            top: 628 + i * 58,
            width: 930,
            display: "flex",
            alignItems: "baseline",
            fontFamily: font.serif,
            fontSize: type.caption + 2,
            color: color.ink,
            fontFeatureSettings: features.text,
            ...wipe(pf(58 + i * 7, 22)),
          }}
        >
          <span style={{ width: 60, color: color.accent, fontStyle: "italic" }}>{n}.</span>
          <span>{label}</span>
          <span style={{ flex: 1, borderBottom: `2px dotted ${color.rule}`, margin: "0 16px", translate: "0 -7px" }} />
          <span style={{ color: color.ink2, fontFeatureSettings: "'onum' 1" }}>{[113, 115, 119, 121][i]}</span>
        </div>
      ))}

      <Rule x={120} y={930} w={1680} from={70} len={30} />
      <div style={{ position: "absolute", left: 112, top: 950, width: 340, height: 100, ...wipe(pf(80, 30), 0) }}>
        <BrandLockup x={0} y={0} h={96} />
      </div>
      <div style={{ position: "absolute", right: 120, top: 985, ...wipe(pf(88, 22), 0) }}>
        <SmallCaps color={color.ink3}>Calculus · Video Notes</SmallCaps>
      </div>
    </Sheet>
  );
};
