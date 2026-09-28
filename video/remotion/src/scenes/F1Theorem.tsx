import React from "react";
import { color, features, font, type } from "../theme";
import { SceneShell } from "../components/Shell";
import { InlineTex, Para, SmallCaps } from "../components/Type";
import { AlignedEq, Anchor } from "../components/Formula";
import { EqNumber, NoteRef, Sidenote } from "../components/Marginalia";
import { dCosL, dCosR, dSinL, dSinR, HEAD } from "../content";

/** F1 — the theorem, set as in a book: rubric bar, numbered display equations, sidenotes. */
export const F1Theorem: React.FC = () => {
  const relX = 1010;
  return (
    <SceneShell head={HEAD}>
      {/* theorem bar */}
      <div style={{ position: "absolute", left: 436, top: 214, width: 3, height: 560, background: color.accent }} />

      <div style={{ position: "absolute", left: 470, top: 206, display: "flex", alignItems: "baseline", gap: 18 }}>
        <SmallCaps color={color.accent} size={24}>
          Theorem 3.1
        </SmallCaps>
        <span style={{ fontFamily: font.serif, fontStyle: "italic", fontSize: 38, color: color.ink2, fontFeatureSettings: features.text }}>
          (Derivatives of sine and cosine)
        </span>
      </div>
      <Para x={470} y={272} w={1300}>
        For every real number <InlineTex src="x" />,<NoteRef n="1" />
      </Para>

      <Anchor x={relX} y={488}>
        <AlignedEq left={dSinL} right={dSinR} size={type.formula} />
      </Anchor>
      <EqNumber y={454} n="3.1" />
      <Anchor x={relX} y={680}>
        <AlignedEq left={dCosL} right={dCosR} size={type.formula} />
      </Anchor>
      <EqNumber y={646} n="3.2" />

      <Para x={470} y={820} w={1330} size={type.caption + 2} color={color.ink2} lh={1.42}>
        <span style={{ fontStyle: "italic", color: color.ink }}>Proof sketch.</span> Expand{" "}
        <InlineTex src="\sin(x+h)=\sin x\cos h+\cos x\sin h" />, divide by <InlineTex src="h" />, and let{" "}
        <InlineTex src="h\to 0" /> using <InlineTex src="\frac{\sin h}{h}\to 1" /> and{" "}
        <InlineTex src="\frac{1-\cos h}{h}\to 0" />.<NoteRef n="2" /> Cosine follows the same way. ∎
      </Para>

      <Sidenote n="1" y={276}>
        Angles in radians. Measured in degrees, each derivative picks up a factor <InlineTex src="\pi/180" />.
      </Sidenote>
      <Sidenote n="2" y={836}>
        Both limits are proved geometrically in §3.1.1.
      </Sidenote>
      <div style={{ position: "absolute", left: 120, top: 470, width: 280 }}>
        <SmallCaps size={18} color={color.ink3}>
          Read it as
        </SmallCaps>
        <div style={{ marginTop: 10, fontFamily: font.serif, fontStyle: "italic", fontSize: 29, lineHeight: 1.3, color: color.ink2 }}>
          “the rate of change of sine is cosine.”
        </div>
      </div>
    </SceneShell>
  );
};
