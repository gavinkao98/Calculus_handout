/** C12 — a weight on a spring: s = sin t, s' = cos t, s'' = −sin t = −s. */
import React from "react";
import { color, stroke } from "../../theme";
import { Arrow, Hatches, Kicker, Layer, Ln, M, Mark, Sheet, Txt, mLbl, sample, tLbl, useS } from "../kit";

const PI = Math.PI;
const A = color.accent;
const REST = 560;
const AMP = 170;
const WX = 330; // weight centre x
const GX = 820;
const GW = 640;
const rowsY = [330, 570, 810];
const UY = 80;

export const Spring: React.FC = () => {
  const { f, p, guard } = useS();
  const t = Math.max(0, (f - 10) / 30) * 1.55;
  const s = Math.sin(t);
  const wy = REST - s * AMP;
  // camera locked: weight, the three graphs and the law read as one plate.
  // coil from the ceiling (y 150) to the top of the weight
  const top = 150;
  const bot = wy - 50;
  const n = 14;
  let coil = `M${WX} ${top} L${WX} ${top + 20}`;
  for (let i = 0; i < n; i++) {
    const y = top + 20 + ((bot - top - 40) * (i + 0.5)) / n;
    coil += ` L${WX + (i % 2 ? -34 : 34)} ${y.toFixed(1)}`;
  }
  coil += ` L${WX} ${bot - 20} L${WX} ${bot}`;
  const tc = t % (2 * PI);
  const fns = [Math.sin, Math.cos, (v: number) => -Math.sin(v)];
  const cols = [color.ink, color.cobalt, A];
  const labels = ["s(t)=\\sin t", "s'(t)=\\cos t", "s''(t)=-\\sin t"];
  const shows = [p("position", 30), p("velocity", 30), p("accel", 30)];
  const gxv = (v: number) => GX + (v / (2 * PI)) * GW;
  const curve = (fn: (v: number) => number, y0: number) => {
    let d = "";
    for (let i = 0; i <= 160; i++) {
      const v = (2 * PI * i) / 160;
      d += `${i ? "L" : "M"}${gxv(v).toFixed(1)} ${(y0 - fn(v) * UY).toFixed(1)}`;
    }
    return d;
  };
  const arrowP = p("arrow", 24);
  // guard: the plates' axes, curves and the law's box against the plate labels (the cursor sweeps
  // continuously and has no resting pose; the weight and its arrow sit apart on the left)
  const lawP = p("law", 24, 20);
  const words = ["height", "velocity", "acceleration"];
  guard(
    [
      ...rowsY.flatMap((y0, i): Mark[] => [
        { name: `plate ${i + 1} t-axis`, pts: [[GX, y0], [GX + GW + 20, y0]], w: stroke.axis, on: shows[i] > 0 },
        { name: `plate ${i + 1} s-axis`, pts: [[GX, y0 - UY - 10], [GX, y0 + UY + 10]], w: stroke.axis, on: shows[i] > 0 },
        { name: `plate ${i + 1} curve`, pts: sample(fns[i], 0, 2 * PI, gxv, (v) => y0 - v * UY, 160), w: stroke.curve, on: shows[i] > 0 },
      ]),
      { name: "law box", pts: [[GX, 930], [GX + 560, 930], [GX + 560, 1040], [GX, 1040], [GX, 930]], w: 2.4, on: lawP > 0 },
    ],
    [
      ...rowsY.map((y0, i) => mLbl({ x: GX + GW + 50, y: y0 + 14, size: 50, p: shows[i], t: labels[i] })),
      ...rowsY.map((y0, i) => tLbl(words[i], GX + GW + 50, y0Label(y0), 28, shows[i], 1, { italic: true })),
      mLbl({ x: GX + 280, y: 1005, align: "center", size: 68, p: p("law", 30), t: "s''=-\\,s" }),
    ],
  );
  return (
    <Sheet folio={124} title="A weight on a spring">
      <Layer>
        <Hatches />
        {/* ceiling */}
        <rect x={WX - 130} y={130} width={260} height={20} fill="url(#h45)" />
        <line x1={WX - 130} y1={150} x2={WX + 130} y2={150} stroke={color.ink} strokeWidth={3} />
        {/* rest line, carried across to the graphs */}
        <Ln x1={WX - 150} y1={REST} x2={WX + 170} y2={REST} p={1} c={color.ink3} w={1.6} dash="3 8" />
        <path d={coil} fill="none" stroke={color.ink} strokeWidth={3} strokeLinejoin="round" />
        <rect x={WX - 60} y={wy - 50} width={120} height={100} rx={10} fill={color.ink} />
        <circle cx={WX} cy={wy} r={6} fill={color.paper} />
        {/* acceleration: always toward rest, proportional to distance */}
        {arrowP > 0 && Math.abs(s) > 0.06 && (
          <Arrow x1={WX + 110} y1={wy} x2={WX + 110} y2={wy + s * AMP * 0.9} p={arrowP} c={A} w={4.5} head={16} />
        )}
        {/* graphs */}
        {rowsY.map((y0, i) =>
          shows[i] > 0 ? (
            <g key={i}>
              <Ln x1={GX} y1={y0} x2={GX + GW + 20} y2={y0} p={shows[i]} c={color.ink2} w={stroke.axis} />
              <Ln x1={GX} y1={y0 - UY - 10} x2={GX} y2={y0 + UY + 10} p={shows[i]} c={color.ink2} w={stroke.axis} />
              <path d={curve(fns[i], y0)} fill="none" stroke={cols[i]} strokeWidth={stroke.curve} strokeLinecap="round" strokeDasharray={`${1600 * shows[i]} 3000`} />
              <line x1={gxv(tc)} y1={y0 - UY - 14} x2={gxv(tc)} y2={y0 + UY + 14} stroke={color.ink3} strokeWidth={1.4} opacity={shows[i]} />
              <circle cx={gxv(tc)} cy={y0 - fns[i](tc) * UY} r={stroke.dot} fill={cols[i]} stroke={color.paper} strokeWidth={stroke.ring} opacity={shows[i]} />
            </g>
          ) : null,
        )}
      </Layer>
      {rowsY.map((y0, i) => (
        <M key={i} x={GX + GW + 50} y={y0 + 14} size={50} p={shows[i]} t={labels[i]} c={i === 2 ? A : i === 1 ? color.cobalt : color.ink} />
      ))}
      <Txt x={GX + GW + 50} y={y0Label(rowsY[0])} w={300} size={28} italic c={color.ink2} p={shows[0]}>
        height
      </Txt>
      <Txt x={GX + GW + 50} y={y0Label(rowsY[1])} w={300} size={28} italic c={color.ink2} p={shows[1]}>
        velocity
      </Txt>
      <Txt x={GX + GW + 50} y={y0Label(rowsY[2])} w={300} size={28} italic c={color.ink2} p={shows[2]}>
        acceleration
      </Txt>
      {/* the law */}
      <Layer>
        <rect x={GX} y={930} width={560} height={110} fill="none" stroke={A} strokeWidth={2.4} opacity={p("law", 24, 20)} />
      </Layer>
      <M x={GX + 280} y={1005} align="center" size={68} p={p("law", 30)} t={`s''=-\\,s`} />
      <Kicker x={120} y={800} p={arrowP}>
        Simple harmonic motion
      </Kicker>
      <Txt x={120} y={850} w={560} size={34} c={color.ink} p={p("arrow", 26, 20)}>
        The pull is always back toward rest, and grows with the distance from it. Sine and cosine both obey it.
      </Txt>
    </Sheet>
  );
};

const y0Label = (y0: number) => y0 - 72;
