/** Recap: (a) ∞ beside (b) 0, each over its table; then the two ideas that did the work. */
import React from "react";
import { interpolate } from "remotion";
import { color, features, font, type } from "../../theme";
import { clamp } from "../../components/Type";
import { Ball, Caps, EDGE, HOMEC, Layer, POCKET, Pocket, Sheet, Table, Txt, World, dOf, useS, useT, wipe } from "../kit";
import { polyAt, realPath, shot } from "../geo";

const HOMEPATH = realPath(shot([2, 1], 2));
const CUT = realPath(shot([2, 1], 1)); // (b): the same shot, cut at the top pocket

export const Recap: React.FC = () => {
  const { f, p } = useS();
  const { t, r } = useT();
  const T = t.recap;
  const A: World = { ox: 560, oy: 390, u: 125 };
  const B: World = { ox: 1360, oy: 390, u: 125 };
  const tin = p("start", 30);
  const loop = interpolate(f, [30, 130], [0, 1], clamp);
  const cut = interpolate(f, [60, 115], [0, 1], clamp);
  const cutEnd = f - 115;
  const ideas = p("ideas", 26);
  const ideas2 = p("ideas", 26, 90);

  const big = (x: number, s: string, c: string, prog: number) => (
    <div
      style={{
        position: "absolute",
        left: x - 200,
        width: 400,
        top: 540,
        textAlign: "center",
        fontFamily: font.serif,
        fontSize: 170,
        lineHeight: 1,
        color: c,
        fontFeatureSettings: features.figures,
        ...wipe(prog),
      }}
    >
      {s}
    </div>
  );

  return (
    <Sheet folio={16} title={T.title}>
      <Layer>
        <Table W={A} real draw={tin} />
        {tin >= 1 && (
          <g>
            <path d={dOf(A, polyAt(HOMEPATH, loop).upto)} fill="none" stroke={color.ink} strokeWidth={3.4} strokeLinejoin="round" />
            <Ball W={A} p={polyAt(HOMEPATH, loop).p} r={10} />
            {loop >= 1 && <circle cx={A.ox} cy={A.oy} r={20} fill="none" stroke={HOMEC} strokeWidth={3} />}
          </g>
        )}
        <Table W={B} real draw={tin} pockets="all" />
        {tin >= 1 && (
          <g>
            <path d={dOf(B, polyAt(CUT, cut).upto)} fill="none" stroke={color.ink} strokeWidth={3.4} strokeLinejoin="round" />
            {cutEnd < 10 && <Ball W={B} p={polyAt(CUT, cut).p} r={10 * interpolate(cutEnd, [0, 10], [1, 0.3], clamp)} />}
            {cutEnd > 6 && <Pocket W={B} p={[0, 1]} c={EDGE} fill={EDGE} r={9} />}
          </g>
        )}
        <line x1={960} y1={170} x2={960} y2={760} stroke={color.rule} strokeWidth={1.5} opacity={tin} />
      </Layer>
      <div style={{ position: "absolute", left: 360, top: 170, width: 400, textAlign: "center", ...wipe(tin, 0) }}>
        <Caps color={color.ink2}>{T.a}</Caps>
      </div>
      <div style={{ position: "absolute", left: 1160, top: 170, width: 400, textAlign: "center", ...wipe(tin, 0) }}>
        <Caps color={color.ink2}>{T.b}</Caps>
      </div>
      {big(560, "∞", HOMEC, p("start", 30, 40))}
      {big(1360, "0", POCKET, p("start", 30, 60))}
      <Txt x={560} y={712} w={500} align="center" size={type.caption} italic c={color.ink2} p={p("start", 26, 60)}>
        {T.many}
      </Txt>
      <Txt x={1360} y={712} w={500} align="center" size={type.caption} italic c={color.ink2} p={p("start", 26, 80)}>
        {T.none}
      </Txt>

      <div style={{ position: "absolute", left: 360, top: 806, width: 1200, height: 2, background: color.rule, opacity: ideas }} />
      <Txt x={960} y={836} w={1500} align="center" size={type.body} p={ideas}>
        {r(T.idea1)}
      </Txt>
      <Txt x={960} y={906} w={1500} align="center" size={type.body} p={ideas2}>
        {r(T.idea2)}
      </Txt>
    </Sheet>
  );
};

