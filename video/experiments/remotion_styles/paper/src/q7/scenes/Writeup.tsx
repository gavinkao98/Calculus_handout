/** "How to write it on the exam": a static four-step proof skeleton, one step per beat. */
import React from "react";
import { color, font, type } from "../../theme";
import { InlineTex as T } from "../../components/Type";
import { EDGE, HOMEC, Kicker, POCKET, Sheet, Txt, useS } from "../kit";

export const Writeup: React.FC = () => {
  const { p } = useS();
  const steps: Array<[string, React.ReactNode, string]> = [
    [
      "Unfold.",
      <>
        Reflect the table across its walls. The path becomes a straight ray from the origin, in direction{" "}
        <T src="(\cos\theta,\,\sin\theta)" />, across a plane tiled by copies of <T src="[-1,1]^2" />.
      </>,
      "s1",
    ],
    [
      "Name the points.",
      <>
        Copies of the center: <T src="(2m,\,2n)" color={HOMEC} />. Corner pockets: <span style={{ color: POCKET }}>(odd, odd)</span>. In (b), the edge
        pockets add <span style={{ color: EDGE }}>(odd, even)</span> and <span style={{ color: EDGE }}>(even, odd)</span>.
      </>,
      "s2",
    ],
    [
      "Check the midpoint.",
      <>
        Coming home means reaching some <T src="(2p,\,2q)" />, <T src="\gcd(p,q)=1" />, first. The only lattice point strictly between is{" "}
        <T src="(p,\,q)" color={EDGE} />.
      </>,
      "s3",
    ],
    [
      "Conclude.",
      <>
        (a) If <T src="p+q" /> is odd, <T src="(p,q)" /> is no pocket; <T src="\tan\theta=2k" /> for every integer <T src="k" /> gives infinitely many{" "}
        <T src="\theta" />. (b) <T src="(p,q)" /> is never (even, even), so it is always a pocket: <span style={{ color: POCKET }}>no angle works</span>.
        &ensp;∎
      </>,
      "s4",
    ],
  ];
  return (
    <Sheet folio={17} title="Writing it up">
      <Kicker x={120} y={150} p={p("start", 22)}>
        How to write it on the exam
      </Kicker>
      <Txt x={120} y={214} w={900} size={type.h2 - 4} italic p={p("start", 26, 10)}>
        Solution.
      </Txt>
      <div style={{ position: "absolute", left: 120, top: 300, width: 4, height: 660 * p("s1", 40), background: color.accent, opacity: 0.8 }} />
      {steps.map(([head, body, beat], i) => {
        const q = p(beat, 30);
        return (
          <React.Fragment key={beat}>
            <Txt x={160} y={300 + i * 168} w={60} size={type.body} c={color.accent} p={q} style={{ fontFeatureSettings: "'lnum' 1" }}>
              {`${i + 1}.`}
            </Txt>
            <Txt x={220} y={300 + i * 168} w={1560} size={40} lh={1.38} p={q}>
              <span style={{ fontWeight: 600, fontFamily: font.serif }}>{head}</span> {body}
            </Txt>
          </React.Fragment>
        );
      })}
    </Sheet>
  );
};
