/** "How to write it on the exam": a static four-step proof skeleton, one step per beat. */
import React from "react";
import { color, font, type } from "../../theme";
import { Kicker, Sheet, Txt, ZH_FONT, useS, useT } from "../kit";

const BEATS = ["s1", "s2", "s3", "s4"];

export const Writeup: React.FC = () => {
  const { p } = useS();
  const { t, r, zh } = useT();
  const T = t.writeup;
  return (
    <Sheet folio={17} title={T.title}>
      <Kicker x={120} y={150} p={p("start", 22)}>
        {T.kicker}
      </Kicker>
      <Txt x={120} y={214} w={900} size={type.h2 - 4} italic p={p("start", 26, 10)}>
        {T.solution}
      </Txt>
      <div style={{ position: "absolute", left: 120, top: 300, width: 4, height: 660 * p("s1", 40), background: color.accent, opacity: 0.8 }} />
      {T.steps.map(([head, body], i) => {
        const beat = BEATS[i];
        const q = p(beat, 30);
        return (
          <React.Fragment key={beat}>
            <Txt x={160} y={300 + i * 168} w={60} size={type.body} c={color.accent} p={q} style={{ fontFeatureSettings: "'lnum' 1" }}>
              {`${i + 1}.`}
            </Txt>
            <Txt x={220} y={300 + i * 168} w={1560} size={40} lh={1.38} p={q}>
              <span style={{ fontWeight: 600, fontFamily: zh ? ZH_FONT : font.serif }}>{head}</span> {r(body)}
            </Txt>
          </React.Fragment>
        );
      })}
    </Sheet>
  );
};
