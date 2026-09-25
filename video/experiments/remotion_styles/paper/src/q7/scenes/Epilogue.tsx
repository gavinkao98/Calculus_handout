/**
 * Epilogue, "beyond this problem": a shot of slope √2 never meets a lattice
 * point, so it never stops; left to run, its path fills the table. Shown, not
 * proved (unfolded, it is a straight line on a torus).
 *
 * `ExtDense` (zh only, the last scene of the extension) is the same sheet on a
 * shorter clock: the slope is set on the `start` beat, the run is squeezed to
 * end HOLD frames before the sheet leaves, and the later lines follow the
 * `dense` beat by fraction instead of fixed frame offsets.
 */
import React from "react";
import { interpolate } from "remotion";
import { color, type } from "../../theme";
import { clamp } from "../../components/Type";
import { Ball, Kicker, Layer, M, Sheet, Table, Txt, World, dOf, useS, useT } from "../kit";
import { fmt } from "../i18n";
import { polyAt, realPath, shot } from "../geo";
import { HOLD } from "../timing";

const PATH = realPath(shot([1, Math.SQRT2], 150));

type Clock = { folio: number; short: boolean };
const Sqrt2Sheet: React.FC<Clock> = ({ folio, short }) => {
  const { f, dur, at, p } = useS();
  const { t, zh } = useT();
  const T = t.epilogue;
  const W: World = { ox: 1180, oy: 580, u: 350 };
  const t0 = at("dense");
  const end = short ? dur - 24 - HOLD.zh.ext_dense : dur - 24;
  const late = (frac: number, fixed: number) => (short ? at("dense", frac) : t0 + fixed);
  const set = short ? p("start", 26, 10) : p("dense", 26, 16);
  // accelerating: slow enough at first to follow the ball, then a blur of bounces
  const x = interpolate(f, [t0 + 10, end], [0, 1], clamp);
  const frac = 0.012 * x + 0.988 * Math.pow(x, 2.6);
  const { p: head, upto } = polyAt(PATH, frac);
  const bounces = upto.length - 2;
  return (
    <Sheet folio={folio} title={T.title}>
      <Layer>
        <Table W={W} real draw={p("start", 36)} />
        {frac > 0 && <path d={dOf(W, upto)} fill="none" stroke={color.ink} strokeWidth={1.7} strokeOpacity={0.55} strokeLinejoin="round" />}
        {frac > 0 && <Ball W={W} p={head} r={10} />}
      </Layer>
      <Kicker x={120} y={150} p={p("start", 22)}>
        {T.kicker}
      </Kicker>
      <Txt x={120} y={220} w={560} size={type.body} p={short ? p("start", 26) : p("dense", 26)}>
        {T.shoot}
      </Txt>
      <M x={120} y={356} t="\tan\theta=\sqrt2" size={70} p={set} />
      <Txt x={120} y={410} w={560} size={type.caption} italic c={color.ink2} p={p("dense", 26, 60)}>
        {T.irrational}
      </Txt>
      <Txt x={120} y={zh ? 588 : 560} w={560} size={type.caption} italic c={color.ink2} p={interpolate(f, [late(0.42, 200), late(0.42, 200) + 30], [0, 1], clamp)}>
        {T.dense}
      </Txt>
      <Txt x={120} y={zh ? 716 : 700} w={560} size={type.label} c={color.ink3} p={interpolate(f, [t0 + 60, t0 + 80], [0, 1], clamp)} style={{ fontFeatureSettings: "'lnum' 1, 'tnum' 1" }}>
        {fmt(T.count, { n: Math.max(0, bounces) })}
      </Txt>
      {/* zh: an opening 「（」 hangs half an em so the ideographs align with the column (STYLE.md 中文版排版 4) */}
      <Txt
        x={120}
        y={900}
        w={560}
        size={30}
        italic
        c={color.ink3}
        p={interpolate(f, [late(0.8, 260), late(0.8, 260) + 30], [0, 1], clamp)}
        style={zh && T.torus.startsWith("（") ? { textIndent: "-0.5em" } : undefined}
      >
        {T.torus}
      </Txt>
    </Sheet>
  );
};

export const Epilogue: React.FC = () => <Sqrt2Sheet folio={18} short={false} />;
export const ExtDense: React.FC = () => <Sqrt2Sheet folio={20} short />;
