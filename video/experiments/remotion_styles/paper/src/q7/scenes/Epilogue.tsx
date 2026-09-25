/**
 * Epilogue, "beyond this problem": a shot of slope √2 never meets a lattice
 * point, so it never stops; left to run, its path fills the table. Shown, not
 * proved (unfolded, it is a straight line on a torus).
 */
import React from "react";
import { interpolate } from "remotion";
import { color, type } from "../../theme";
import { clamp } from "../../components/Type";
import { Ball, Kicker, Layer, M, Sheet, Table, Txt, World, dOf, useS } from "../kit";
import { polyAt, realPath, shot } from "../geo";

const PATH = realPath(shot([1, Math.SQRT2], 150));

export const Epilogue: React.FC = () => {
  const { f, dur, at, p } = useS();
  const W: World = { ox: 1180, oy: 580, u: 350 };
  const t0 = at("dense");
  const end = dur - 24;
  // accelerating: slow enough at first to follow the ball, then a blur of bounces
  const x = interpolate(f, [t0 + 10, end], [0, 1], clamp);
  const frac = 0.012 * x + 0.988 * Math.pow(x, 2.6);
  const { p: head, upto } = polyAt(PATH, frac);
  const bounces = upto.length - 2;
  return (
    <Sheet folio={18} title="Beyond this problem">
      <Layer>
        <Table W={W} real draw={p("start", 36)} />
        {frac > 0 && <path d={dOf(W, upto)} fill="none" stroke={color.ink} strokeWidth={1.7} strokeOpacity={0.55} strokeLinejoin="round" />}
        {frac > 0 && <Ball W={W} p={head} r={10} />}
      </Layer>
      <Kicker x={120} y={150} p={p("start", 22)}>
        Beyond this problem
      </Kicker>
      <Txt x={120} y={220} w={560} size={type.body} p={p("dense", 26)}>
        Shoot at slope
      </Txt>
      <M x={120} y={356} t="\tan\theta=\sqrt2" size={70} p={p("dense", 26, 16)} />
      <Txt x={120} y={410} w={560} size={type.caption} italic c={color.ink2} p={p("dense", 26, 60)}>
        Irrational: the line never meets a lattice point, so the ball never stops.
      </Txt>
      <Txt x={120} y={560} w={560} size={type.caption} italic c={color.ink2} p={interpolate(f, [t0 + 200, t0 + 230], [0, 1], clamp)}>
        Left to run, the path fills in the whole table.
      </Txt>
      <Txt x={120} y={700} w={560} size={type.label} c={color.ink3} p={interpolate(f, [t0 + 60, t0 + 80], [0, 1], clamp)} style={{ fontFeatureSettings: "'lnum' 1, 'tnum' 1" }}>
        bounces so far: {Math.max(0, bounces)}
      </Txt>
      <Txt x={120} y={900} w={560} size={30} italic c={color.ink3} p={interpolate(f, [t0 + 260, t0 + 290], [0, 1], clamp)}>
        (Unfolded, it is one straight line on a torus. Shown here, not proved.)
      </Txt>
    </Sheet>
  );
};
