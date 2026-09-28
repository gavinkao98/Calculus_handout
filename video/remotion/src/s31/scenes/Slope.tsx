/** C9 — the slope of sin at x equals the height of cos at x; the circle from the cold open agrees. */
import React from "react";
import { Easing, interpolate } from "remotion";
import { color, labelGuard, semantic, stroke, type } from "../../theme";
import { clamp, measure } from "../../components/Type";
import { Curve, Dot, PlotFrame, RangeAxes, SlopeTriangle, Tangent, TangentNote, Tick, px } from "../../components/Plot";
import { FigureCaption } from "../../components/Marginalia";
import { Arrow, Layer, Lbl, M, Mark, Sheet, Txt, arcPts, arrowMarks, dotMark, mLbl, sample, tLbl, texBox, useS, wipe } from "../kit";

const PI = Math.PI;
const A: PlotFrame = { ox: 520, oy: 340, ux: 170, uy: 150 };
const B: PlotFrame = { ox: 520, oy: 790, ux: 170, uy: 150 };
const tick = (v: number, t: string): Tick => ({ v, label: [{ key: "t", tex: t }] });
const xT = [tick(PI / 2, "\\pi/2"), tick(PI, "\\pi"), tick((3 * PI) / 2, "3\\pi/2"), tick(2 * PI, "2\\pi")];
const yT = [tick(1, "1"), tick(-1, "{-}1")];
const fmt = (m: number) => (Math.abs(m) < 0.005 ? "0.00" : m < 0 ? `−${Math.abs(m).toFixed(2)}` : m.toFixed(2));

export const Slope: React.FC = () => {
  const { f, at, p, sp, dur, guard } = useS();
  const x = interpolate(
    f,
    [at("tangent") + 16, at("match"), at("peak"), at("peak") + 40, at("circle"), dur - 20],
    [0.15, 0.9, 1.3, PI / 2, PI / 2, 2 * PI - 0.6], // parks where its slope triangle clears the "2π" tick number
    { ...clamp, easing: Easing.inOut(Easing.sin) },
  );
  const m = Math.cos(x);
  const y = Math.sin(x);
  // camera locked: both panels and the margin are one composition; emphasis is the red bars.
  const axA = p("start", 30);
  const sinP = p("start", 50, 20);
  const grow = sp("tangent", 6);
  const note = p("tangent", 20, 20);
  const axB = p("cosine", 24);
  const cosP = p("cosine", 40, 6);
  const match = p("match", 26);
  const peak = interpolate(f, [at("peak") + 30, at("peak") + 46, at("circle") + 10, at("circle") + 30], [0, 1, 1, 0], clamp);
  const circ = p("circle", 30);
  const [bx, by0] = px(B, x, 0);
  const [, qy] = px(B, x, m);
  const [ax, ay] = px(A, x, y);
  // inset circle (margin): the same angle, the unit velocity, its vertical part = cos x
  const O = { x: 260, y: 640 };
  const R = 105;
  const P = { x: O.x + R * Math.cos(x), y: O.y - R * Math.sin(x) };
  const V = { x: -R * Math.sin(x), y: -R * Math.cos(x) };

  // ── the guard. The sliding point (tangent, triangle, bars, inset radius) is checked where it rests:
  // before it starts, parked at the peak, and at the end. "slope …" is lettered along the tangent
  // and "height" rides the bar; both travel with their own mark and are not graph labels at rest.
  const rest = f <= at("tangent") + 16 || (f >= at("peak") + 40 && f <= at("circle")) || f >= dur - 20;
  const [cx0, cy0] = px(A, x, y);
  const tl = Math.hypot(A.ux, m * A.uy);
  const th = 230 * Math.max(0, grow);
  const [rbx, ray] = px(A, x + 1, y);
  const [, rcy] = px(A, x + 1, y + m);
  const axes = (F: PlotFrame, on: boolean, name: string): Mark[] => [
    { name: `${name} x-axis`, pts: [px(F, 0, 0), px(F, 2 * PI, 0)], w: stroke.axis, on },
    { name: `${name} y-axis`, pts: [px(F, 0, -1), px(F, 0, 1)], w: stroke.axis, on },
    ...xT.map((t): Mark => ({ name: `${name} x tick`, pts: [px(F, t.v, 0), [px(F, t.v, 0)[0], F.oy + 9]], w: stroke.axis, on })),
    // a tick points at its own number (RangeAxes sets it 10 px off): exempt for that label only
    ...yT.map((t): Mark => ({ name: `${name} y tick`, pts: [px(F, 0, t.v), [F.ox - 9, px(F, 0, t.v)[1]]], w: stroke.axis, on, owner: t.label?.[0].tex })),
  ];
  // x tick labels of the top panel are set here (not by RangeAxes) one step lower than the axes
  // default, so the sine curve arriving at 2π from below keeps clear of "2π"
  const xTL = xT.map((t) => ({ t: t.label?.[0].tex ?? "", x: px(A, t.v, 0)[0], y: A.oy + 9 + type.label * 1.25 + 14, size: type.label, align: "center" as const, display: false, c: color.ink2, p: axA >= 1 ? 1 : 0, o: axA }));
  // the dotted plumb stops short of any tick number it would otherwise run through (it rests on π/2)
  const cut = labelGuard.clearance + 4;
  const plumb = xTL
    .map((q) => texBox(q.t, q.x, q.y, q.size, q.align, false))
    .filter((b) => bx >= b.l - cut && bx <= b.r + cut)
    .reduce<Array<[number, number]>>(
      (segs, b) => segs.flatMap(([a, z]): Array<[number, number]> => [[a, Math.min(z, b.t - cut)], [Math.max(a, b.b + cut), z]].filter(([u, v]) => v - u > 2) as Array<[number, number]>),
      [[ay + 12, qy - 12]],
    );
  const marks: Mark[] = [
    ...axes(A, axA > 0, "top"),
    ...axes(B, axB > 0, "bottom"),
    { name: "sine curve", pts: sample(Math.sin, 0, 2 * PI + 0.2, (v) => px(A, v, 0)[0], (v) => px(A, 0, v)[1]), w: stroke.curve, on: sinP > 0 },
    { name: "cosine curve", pts: sample(Math.cos, 0, 2 * PI + 0.2, (v) => px(B, v, 0)[0], (v) => px(B, 0, v)[1]), w: stroke.curve, on: cosP > 0 },
    { name: "tangent", owner: "slope note", pts: [[cx0 - (A.ux / tl) * th, cy0 + ((m * A.uy) / tl) * th], [cx0 + (A.ux / tl) * th, cy0 - ((m * A.uy) / tl) * th]], w: stroke.tangent, on: rest && grow > 0.05 },
    { name: "slope triangle", pts: [[cx0, cy0], [rbx, ray], [rbx, rcy]], w: stroke.emphasis, on: rest && match > 0 },
    { name: "red bar", pts: [[bx, by0], [bx, qy]], w: stroke.emphasis, on: rest && match > 0 },
    ...plumb.map(([a, z]): Mark => ({ name: "plumb line", pts: [[bx, a], [bx, z]], w: 1.5, on: rest && match > 0 })),
    dotMark("point on sin", ax, ay, rest && grow > 0.05),
    dotMark("point on cos", bx, qy, rest && axB > 0),
    { name: "inset circle", pts: arcPts(O.x, O.y, R, 0, 2 * PI, 72), w: 2.6, on: circ > 0 },
    { name: "inset crosshair", pts: [[O.x - R - 20, O.y], [O.x + R + 20, O.y]], w: 1.6, on: circ > 0 },
    { name: "inset crosshair", pts: [[O.x, O.y + R + 20], [O.x, O.y - R - 20]], w: 1.6, on: circ > 0 },
    { name: "inset radius", pts: [[O.x, O.y], [P.x, P.y]], w: 1.6, on: rest && circ > 0 },
    { name: "inset vertical part", pts: [[P.x, P.y], [P.x, P.y + V.y]], w: 4, on: rest && circ > 0 },
    ...arrowMarks("inset velocity", P.x, P.y, P.x + V.x, P.y + V.y, { w: 2.4, head: 11, on: rest && circ > 0 }),
  ];
  const yTL = (F: PlotFrame, on: number) =>
    yT.map((t) => mLbl({ t: t.label?.[0].tex ?? "", x: F.ox - 19, y: px(F, 0, t.v)[1] + type.label * 0.32, size: type.label, align: "right", display: false, p: on >= 1 ? 1 : 0 }));
  // "slope …" is lettered along the tangent on the side away from the curve: above it where sine
  // bends down (sin x > 0), below it where sine bends up
  const lift = interpolate(y, [-0.25, 0.25], [-40, 24], clamp);
  const na = Math.atan2(-m * A.uy, A.ux);
  const noteAt = { x: cx0 + Math.cos(na) * -150 + Math.sin(na) * lift, y: cy0 + Math.sin(na) * -150 - Math.cos(na) * lift };
  const noteW = measure("slope", type.label, { italic: true }) + measure(` ${fmt(m)}`, type.label);
  const noteL: Lbl = {
    name: "slope note",
    box: { l: -noteW / 2, r: noteW / 2, t: -type.label * 0.72, b: type.label * 0.22 },
    on: rest && note >= 1,
    rot: { a: na, x: noteAt.x, y: noteAt.y },
  };
  const peakAt = px(A, PI / 2, 1);
  const zeroAt = px(B, PI / 2, 0);
  guard(marks, [
    noteL,
    ...xTL.map((q) => mLbl(q)),
    ...yTL(A, axA),
    ...yTL(B, axB),
    mLbl({ x: 1560, y: 210, t: "y=\\sin x", size: 46, p: axA }),
    mLbl({ x: 1560, y: 960, t: "y=\\cos x", size: 46, p: axB }),
    tLbl("flat tangent", peakAt[0] + 170, peakAt[1] - 70, 30, peak, peak, { italic: true, align: "center" }),
    tLbl("cos = 0", zeroAt[0] + 16, zeroAt[1] - 52, 30, peak, peak, { italic: true }),
  ]);
  return (
    <Sheet folio={121} title="Slope equals height">
      <Layer>
        <defs>
          <clipPath id="slclip">
            <rect x={440} y={120} width={1400} height={420} />
          </clipPath>
        </defs>
        {/* plumb line joining the two panels at x */}
        {plumb.map(([a, z]) => (
          <line key={a} x1={bx} y1={a} x2={bx} y2={z} stroke={color.ink3} strokeWidth={1.5} strokeDasharray="1.5 6" strokeLinecap="round" opacity={match} />
        ))}
        <RangeAxes f={A} x={[0, 2 * PI]} y={[-1, 1]} xTicks={xT.map((t) => ({ v: t.v }))} yTicks={yT} progress={axA} labels={axA} />
        {axB > 0 && <RangeAxes f={B} x={[0, 2 * PI]} y={[-1, 1]} xTicks={xT.map((t) => ({ v: t.v }))} yTicks={yT} progress={axB} labels={axB} />}
        <Curve f={A} fn={Math.sin} a={0} b={2 * PI + 0.2} progress={sinP} c={semantic.sin} />
        <Curve f={B} fn={Math.cos} a={0} b={2 * PI + 0.2} progress={cosP} c={semantic.cos} />
        <SlopeTriangle f={A} x0={x} y0={y} m={m} progress={match} />
        {Math.abs(m) > 0.004 && match > 0 && <line x1={bx} y1={by0} x2={bx} y2={by0 + (qy - by0) * match} stroke={color.accent} strokeWidth={stroke.emphasis} strokeLinecap="round" />}
        <g clipPath="url(#slclip)">
          <Tangent f={A} x0={x} y0={y} m={m} half={230} grow={grow} />
        </g>
        {grow > 0.05 && <Dot f={A} x={x} y={y} />}
        {axB > 0 && <Dot f={B} x={x} y={m} c={semantic.cos} opacity={cosP} />}
        <TangentNote f={A} x0={x} y0={y} m={m} at={-150} lift={lift} opacity={note}>
          <tspan fontStyle="italic">slope</tspan> {fmt(m)}
        </TangentNote>

        {/* inset circle */}
        <g opacity={circ}>
          <line x1={O.x - R - 20} y1={O.y} x2={O.x + R + 20} y2={O.y} stroke={color.ink3} strokeWidth={1.6} />
          <line x1={O.x} y1={O.y + R + 20} x2={O.x} y2={O.y - R - 20} stroke={color.ink3} strokeWidth={1.6} />
          <circle cx={O.x} cy={O.y} r={R} fill="none" stroke={color.ink} strokeWidth={2.6} />
          <line x1={O.x} y1={O.y} x2={P.x} y2={P.y} stroke={color.ink2} strokeWidth={1.6} />
          <line x1={P.x} y1={P.y} x2={P.x} y2={P.y + V.y} stroke={color.accent} strokeWidth={4} strokeLinecap="round" />
        </g>
        <Arrow x1={P.x} y1={P.y} x2={P.x + V.x} y2={P.y + V.y} p={circ} c={color.accent} w={2.4} head={11} o={0.55} />
        {circ > 0 && <circle cx={P.x} cy={P.y} r={6} fill={color.ink} stroke={color.paper} strokeWidth={2} opacity={circ} />}
      </Layer>
      <Txt x={bx + 18} y={(by0 + qy) / 2 - 22} w={300} size={type.label} c={color.ink} p={match} o={1 - peak} style={{ fontFeatureSettings: "'lnum' 1, 'tnum' 1" }}>
        <i>height</i> {fmt(m)}
      </Txt>
      {xTL.map((q) => (
        <M key={q.t} {...q} />
      ))}
      <M x={1560} y={210} t="y=\sin x" size={46} p={axA} />
      <M x={1560} y={960} t="y=\cos x" size={46} c={semantic.cos} p={axB} />
      <Txt x={px(A, PI / 2, 1)[0] + 170} y={px(A, PI / 2, 1)[1] - 70} w={260} align="center" size={30} italic c={color.accent} p={peak} o={peak}>
        flat tangent
      </Txt>
      <Txt x={px(B, PI / 2, 0)[0] + 16} y={px(B, PI / 2, 0)[1] - 52} w={240} size={30} italic c={color.accent} p={peak} o={peak}>
        cos = 0
      </Txt>
      <div style={{ position: "absolute", left: 120, top: 140, ...wipe(p("match", 30, 30), 0) }}>
        <FigureCaption n="3.1" y={0} x={0} w={290}>
          The red rise of the tangent (per unit run) and the red bar below always have the same length.
        </FigureCaption>
      </div>
      <Txt x={120} y={790} w={300} size={30} italic c={color.ink2} p={circ}>
        The circle agrees: the point’s height changes at rate <span style={{ color: semantic.cos, fontStyle: "normal" }}>cos x</span>.
      </Txt>
    </Sheet>
  );
};
