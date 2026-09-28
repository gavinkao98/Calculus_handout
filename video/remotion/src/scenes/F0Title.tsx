import React from "react";
import { color, features, font, type } from "../theme";
import { SceneShell, BrandLockup } from "../components/Shell";
import { InlineTex, Rule, SmallCaps } from "../components/Type";
import { Curve, Dot, PlotFrame, Tangent } from "../components/Plot";

const contents: Array<[string, React.ReactNode, string]> = [
  ["i", <>The key limit <InlineTex src="\sin h / h \to 1" /></>, "0:40"],
  ["ii", <>The derivative of sine</>, "2:15"],
  ["iii", <>Slope equals height</>, "4:05"],
  ["iv", <>The four-step cycle</>, "6:30"],
];

/** F0 — section opener, set like a chapter-opening page. */
export const F0Title: React.FC = () => {
  // fleuron: one period of sine under the numeral, tangent at the origin
  const f: PlotFrame = { ox: 190, oy: 740, ux: 84, uy: 44 };
  return (
    <SceneShell head={null} device={false}>
      {/* top band */}
      <div style={{ position: "absolute", left: 120, top: 112 }}>
        <SmallCaps>Chapter 3 · Differentiation Rules</SmallCaps>
      </div>
      <div style={{ position: "absolute", right: 120, top: 112 }}>
        <SmallCaps>Section 3.1</SmallCaps>
      </div>
      <Rule x={120} y={150} w={1680} color={color.rule} />

      {/* the numeral */}
      <div
        style={{
          position: "absolute",
          left: 108,
          top: 250,
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
      <svg width={1920} height={1080} style={{ position: "absolute", left: 0, top: 0 }}>
        <Curve f={f} fn={Math.sin} a={0} b={2 * Math.PI} c={color.ink} width={2.6} nib={false} />
        <line x1={190} y1={740} x2={190 + 2 * Math.PI * 84} y2={740} stroke={color.rule} strokeWidth={1.5} />
        <Tangent f={f} x0={0} y0={0} m={1} half={70} width={2.6} />
        <Dot f={f} x={0} y={0} r={6} />
      </svg>

      {/* column rule */}
      <Rule x={800} y={262} w={560} vertical color={color.rule} />

      {/* title block */}
      <div style={{ position: "absolute", left: 870, top: 250, width: 930 }}>
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
        <div style={{ width: 84, height: 3, background: color.accent, margin: "40px 0 30px" }} />
        <div
          style={{
            fontFamily: font.serif,
            fontSize: 50,
            fontStyle: "italic",
            color: color.ink2,
            fontFeatureSettings: features.text,
          }}
        >
          How fast does sine change?
        </div>
        {/* contents with leaders */}
        <div style={{ marginTop: 64, display: "flex", flexDirection: "column", gap: 10 }}>
          {contents.map(([n, label, t]) => (
            <div
              key={n}
              style={{
                display: "flex",
                alignItems: "baseline",
                fontFamily: font.serif,
                fontSize: type.caption,
                color: color.ink,
                fontFeatureSettings: features.text,
              }}
            >
              <span style={{ width: 54, color: color.accent, fontStyle: "italic" }}>{n}.</span>
              <span>{label}</span>
              <span style={{ flex: 1, borderBottom: `2px dotted ${color.rule}`, margin: "0 16px", translate: "0 -7px" }} />
              <span style={{ color: color.ink2, fontFeatureSettings: "'onum' 1, 'tnum' 1" }}>{t}</span>
            </div>
          ))}
        </div>
      </div>

      {/* foot */}
      <Rule x={120} y={930} w={1680} color={color.rule} />
      <BrandLockup x={112} y={950} h={96} />
      <div style={{ position: "absolute", right: 120, top: 985 }}>
        <SmallCaps color={color.ink3}>Calculus · Video Notes</SmallCaps>
      </div>
    </SceneShell>
  );
};
