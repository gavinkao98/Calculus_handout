/**
 * intro — the section's opening page.  Cold open is a close-up of a sine
 * fleuron being inked with a tangent already riding it (the question, drawn);
 * the camera then pulls back to reveal the chapter-opening page around it.
 */
import React from "react";
import { interpolate } from "remotion";
import { color, features, font, semantic, stroke, type } from "../../theme";
import { BrandLockup } from "../../components/Shell";
import { InkReveal, Rule, SmallCaps } from "../../components/Type";
import { Curve, Dot, PlotFrame, Tangent, TangentNote } from "../../components/Plot";
import { PAGE, camPath, useBeats } from "../clock";
import { Layer, Sheet } from "./common";

const PI = Math.PI;
const FL: PlotFrame = { ox: 150, oy: 760, ux: 92, uy: 118 }; // fleuron: one period under the numeral

const contents: [string, string, string][] = [
  ["i", "The derivative of sine", "113"],
  ["ii", "The derivative of cosine", "114"],
  ["iii", "Slope equals height", "116"],
  ["iv", "The four-step cycle", "118"],
];

const fmt = (m: number) => (Math.abs(m) < 0.005 ? "0.00" : m < 0 ? `−${Math.abs(m).toFixed(2)}` : m.toFixed(2));

export const Intro: React.FC = () => {
  const { frame, at, p, sp, dur } = useBeats();
  const T = at("title");

  const cam = camPath(
    frame,
    { cx: 470, cy: 700, s: 1.9 },
    PAGE,
    [
      { f: 0, to: { cx: 470, cy: 690, s: 2.0 }, len: T },
      { f: T - 4, to: { cx: 960, cy: 540, s: 1.0 }, len: 54 },
    ],
    0.035,
    dur,
  );

  // the tangent rides the whole period during the scene: the question, asked by the picture
  const x0 = interpolate(frame, [18, dur - 10], [0.25, 2 * PI - 0.2]);
  const m = Math.cos(x0);
  const inkSin = p(2, 40);
  const tanIn = sp(22);
  const note = p(34, 14);

  return (
    <Sheet cam={cam} head={null} device={false}>
      {/* top band */}
      <InkReveal from={T + 6} len={26} style={{ left: 120, top: 100, width: 800, height: 40 }}>
        <SmallCaps>Chapter 3 · Differentiation Rules</SmallCaps>
      </InkReveal>
      <InkReveal from={T + 10} len={26} style={{ left: 1500, top: 100, width: 300, height: 40, textAlign: "right" }}>
        <SmallCaps>Section 3.1</SmallCaps>
      </InkReveal>
      <Rule x={120} y={150} w={1680} from={T + 4} len={34} />

      {/* the numeral */}
      <InkReveal from={T - 6} len={34} style={{ left: 100, top: 220, width: 700, height: 330 }}>
        <div
          style={{
            fontFamily: font.serif,
            fontSize: type.display,
            lineHeight: 1,
            color: color.ink,
            fontFeatureSettings: "'lnum' 1, 'kern' 1",
            letterSpacing: "-0.02em",
          }}
        >
          <span style={{ color: color.accent, fontStyle: "italic", fontSize: "0.78em", marginRight: "0.04em" }}>§</span>3.1
        </div>
      </InkReveal>

      {/* fleuron: sine with a live tangent */}
      <Layer>
        <line x1={FL.ox} y1={FL.oy} x2={FL.ox + 2 * PI * FL.ux} y2={FL.oy} stroke={color.rule} strokeWidth={stroke.axis} opacity={inkSin > 0 ? 1 : 0} />
        <Curve f={FL} fn={Math.sin} a={0} b={2 * PI} progress={inkSin} c={semantic.sin} width={3.6} />
        <Tangent f={FL} x0={x0} y0={Math.sin(x0)} m={m} half={120} grow={tanIn} width={3.2} />
        <Dot f={FL} x={x0} y={Math.sin(x0)} scale={tanIn} r={7} />
        <TangentNote f={FL} x0={x0} y0={Math.sin(x0)} m={m} at={m > 0 ? -70 : 70} lift={26} opacity={note} size={30}>
          <tspan fontStyle="italic">slope</tspan> {fmt(m)}
        </TangentNote>
      </Layer>

      {/* column rule */}
      <Rule x={800} y={236} w={620} vertical from={T + 8} len={40} />

      {/* title block */}
      <InkReveal from={T + 8} len={30} style={{ left: 870, top: 222, width: 960, height: 250 }}>
        <div
          style={{
            fontFamily: font.serif,
            fontSize: type.title,
            lineHeight: 1.02,
            color: color.ink,
            fontWeight: 500,
            letterSpacing: "-0.012em",
            fontFeatureSettings: features.text,
          }}
        >
          Derivatives of
          <br />
          Sine and Cosine
        </div>
      </InkReveal>
      <Rule x={872} y={500} w={96} weight={3.5} color={color.accent} from={T + 24} len={18} />
      <InkReveal from={T + 28} len={26} style={{ left: 870, top: 526, width: 960, height: 80 }}>
        <div style={{ fontFamily: font.serif, fontSize: 56, fontStyle: "italic", color: color.ink2, fontFeatureSettings: features.text }}>
          How fast does sine change?
        </div>
      </InkReveal>

      {/* contents, one row per clause of the narration */}
      {contents.map(([n, label, pg], i) => {
        const from = at("contents", [0.04, 0.2, 0.42, 0.66][i]);
        return (
          <React.Fragment key={n}>
            <InkReveal from={from} len={20} style={{ left: 870, top: 652 + i * 62, width: 930, height: 56 }}>
              <div
                style={{
                  display: "flex",
                  alignItems: "baseline",
                  width: 930,
                  fontFamily: font.serif,
                  fontSize: 40,
                  color: color.ink,
                  fontFeatureSettings: features.text,
                }}
              >
                <span style={{ width: 62, color: color.accent, fontStyle: "italic" }}>{n}.</span>
                <span>{label}</span>
                <span style={{ flex: 1, borderBottom: `2.5px dotted ${color.rule}`, margin: "0 18px", translate: "0 -9px" }} />
                <span style={{ color: color.ink2, fontFeatureSettings: "'onum' 1, 'tnum' 1" }}>{pg}</span>
              </div>
            </InkReveal>
          </React.Fragment>
        );
      })}

      {/* foot */}
      <Rule x={120} y={930} w={1680} from={T + 30} len={30} />
      <InkReveal from={T + 36} len={30} style={{ left: 112, top: 950, width: 340, height: 100 }}>
        <BrandLockup x={0} y={0} h={96} />
      </InkReveal>
      <InkReveal from={T + 44} len={24} style={{ left: 1300, top: 985, width: 500, height: 40, textAlign: "right" }}>
        <SmallCaps color={color.ink3}>Calculus · Video Notes</SmallCaps>
      </InkReveal>
    </Sheet>
  );
};
