/** C5 — sinθ/θ trapped between cosθ and 1; both go to 1; squeeze. Debt 2 paid. */
import React from "react";
import { interpolate } from "remotion";
import { color, stroke, type } from "../../theme";
import { clamp } from "../../components/Type";
import { HOME, Kicker, Layer, Ledger, Ln, M, Mark, Sheet, Txt, camPath, dotMark, mLbl, sample, tLbl, toD, useS } from "../kit";

const PI = Math.PI;
const G = { x: 1130, y: 720, ux: 205, uy: 300 };
const gx = (v: number) => G.x + v * G.ux;
const gy = (v: number) => G.y - v * G.uy;
const sinc = (v: number) => (Math.abs(v) < 1e-6 ? 1 : Math.sin(v) / v);
const path = (fn: (v: number) => number, a: number, b: number, n = 200) => toD(sample(fn, a, b, gx, gy, n));
const CLIP_B = 900; // the figure's clip rect ends here
const COS_END = Math.acos((G.y - CLIP_B) / G.uy); // |θ| where the clipped cos curve leaves the figure
const AX_TOP = 1.15; // the y-axis stops short of the verdict above it

export const Limit: React.FC = () => {
  const { f, at, p, guard } = useS();
  // one of the film's two hero push-ins (the other is the cold open): lean into the pinch at θ → 0,
  // then come back to the full page BEFORE the verdict is written. Nothing is written during either move.
  const cam = camPath(f, HOME, [
    [at("pinch") - 6, { cx: 1130, cy: 560, s: 1.4 }, 46],
    [at("value") - 48, HOME, 44],
  ]);
  const pushed = interpolate(cam.s, [1, 1.4], [0, 1], clamp); // marginal type the push would clip fades out
  const ax = p("start", 30, 4);
  const cur = p("start", 50, 30);
  const one = p("bounds", 30);
  const cosP = p("bounds", 44, 50);
  const band = p("bounds", 30, 90);
  const th = interpolate(f, [at("pinch") + 50, at("value") - 20], [1.35, 0.06], { ...clamp, easing: (t) => 1 - Math.pow(1 - t, 2.2) });
  const mark = interpolate(f, [at("pinch") + 40, at("pinch") + 56, at("value") + 10, at("value") + 30], [0, 1, 1, 0], clamp);
  const bandPath = (() => {
    const d = path(() => 1, -PI / 2, PI / 2, 2);
    let back = "";
    for (let i = 0; i <= 200; i++) {
      const v = PI / 2 - (PI * i) / 200;
      back += `L${gx(v).toFixed(1)} ${gy(Math.cos(v)).toFixed(1)}`;
    }
    return d + back + "Z";
  })();
  const val = p("value", 34);
  const paid = p("paid", 30, 20);

  // labels live in empty paper: the ratio's name in the open corner above its left tail, cosine's
  // below the axis beside its own (blue) branch, "y = 1" on its line's far end with air under it.
  const L = {
    sinc: { x: 500, y: 520, t: "y=\\frac{\\sin\\theta}{\\theta}", size: 46, p: cur },
    one: { x: gx(PI) - 6, y: gy(1) - 26, t: "y=1", size: 42, align: "right" as const, c: color.ink2, p: one },
    cos: { x: gx(-2.3) + 34, y: 842, t: "y=\\cos\\theta", size: 42, align: "right" as const, c: color.cobalt, p: cosP },
    mPi: { x: gx(-PI), y: G.y + 52, t: "-\\pi", size: type.label, align: "center" as const, c: color.ink2, p: ax },
    pi: { x: gx(PI), y: G.y + 52, t: "\\pi", size: type.label, align: "center" as const, c: color.ink2, p: ax },
    zero: { x: G.x + 16, y: G.y + 44, t: "0", size: type.label, c: color.ink2, p: ax },
    verdict: { x: 1130, y: 280, align: "center" as const, size: 84, p: val, t: `\\lim_{\\theta\\to0}\\frac{\\sin\\theta}{\\theta}={\\color{${color.accent}}1}` },
  };
  const trapped = { x: G.x + 26, y: gy(1) - 70 };
  const caption = "cos θ → 1 because cosine is continuous — the debt we paid first";
  const capY = 900;

  const marks: Mark[] = [
    { name: "θ-axis", pts: [[gx(-PI) - 20, G.y], [gx(PI) + 20, G.y]], w: stroke.axis, on: ax > 0 },
    { name: "y-axis", pts: [[G.x, gy(-0.55)], [G.x, gy(AX_TOP)]], w: stroke.axis, on: ax > 0 },
    ...[-PI, PI].map((v): Mark => ({ name: `tick ${v > 0 ? "π" : "−π"}`, pts: [[gx(v), G.y], [gx(v), G.y + 10]], w: stroke.axis, on: ax > 0 })),
    { name: "line y = 1", pts: [[gx(-PI), gy(1)], [gx(PI), gy(1)]], w: 2.6, on: one > 0 },
    { name: "cos curve", pts: sample(Math.cos, -COS_END, COS_END, gx, gy), w: stroke.curve, on: cosP > 0 },
    { name: "sinθ/θ curve", pts: sample(sinc, -PI, PI, gx, gy), w: stroke.curve + 0.6, on: cur > 0 },
    { name: "hole at θ = 0", pts: [[G.x, gy(1)]], w: 2 * (9 + 14 * val) + 3, on: cur > 0.5 },
    ...[th, -th].flatMap((v): Mark[] => [
      { name: "pinch bar", pts: [[gx(v), gy(Math.cos(v))], [gx(v), gy(1)]], w: 3.2, on: mark > 0.05 },
      dotMark("pinch dot", gx(v), gy(sinc(v)), mark > 0.05, stroke.dot * 0.8),
    ]),
  ];
  guard(marks, [
    ...Object.values(L).map((q) => mLbl(q)),
    tLbl("trapped", trapped.x, trapped.y, 30, mark, mark, { italic: true }),
    tLbl(caption, 1130, capY, type.caption, p("value", 26, 50), 1, { italic: true, align: "center" }),
  ]);

  return (
    <Sheet folio={118} title="Debt 2: the key limit" cam={cam}>
      <div style={{ opacity: 1 - pushed }}>
        <Kicker x={470} y={140} p={p("start", 24)}>
          The squeeze
        </Kicker>
      </div>
      <Layer>
        <defs>
          <clipPath id="limclip">
            <rect x={400} y={200} width={1450} height={CLIP_B - 200} />
          </clipPath>
        </defs>
        <g clipPath="url(#limclip)">
          <path d={bandPath} fill={color.paperShade} opacity={band} />
          <Ln x1={gx(-PI) - 20} y1={G.y} x2={gx(PI) + 20} y2={G.y} p={ax} c={color.ink2} w={stroke.axis} />
          <Ln x1={G.x} y1={gy(-0.55)} x2={G.x} y2={gy(AX_TOP)} p={ax} c={color.ink2} w={stroke.axis} />
          {one > 0 && <path d={path(() => 1, -PI, -PI + 2 * PI * one, 2)} fill="none" stroke={color.ink2} strokeWidth={2.6} />}
          {cosP > 0 && <path d={path(Math.cos, -PI, -PI + 2 * PI * cosP)} fill="none" stroke={color.cobalt} strokeWidth={stroke.curve} strokeLinecap="round" />}
          {cur > 0 && <path d={path(sinc, -PI, -PI + 2 * PI * cur)} fill="none" stroke={color.ink} strokeWidth={stroke.curve + 0.6} strokeLinecap="round" />}
          {/* the pinch: at ±θ the ratio sits between cos θ and 1 */}
          {[th, -th].map((v, i) => (
            <g key={i} opacity={mark}>
              <line x1={gx(v)} y1={gy(Math.cos(v))} x2={gx(v)} y2={gy(1)} stroke={color.accent} strokeWidth={3.2} />
              <circle cx={gx(v)} cy={gy(sinc(v))} r={stroke.dot * 0.8} fill={color.ink} stroke={color.paper} strokeWidth={stroke.ring} />
            </g>
          ))}
        </g>
        {/* the hole at θ = 0: the ratio is undefined there */}
        {cur > 0.5 && <circle cx={G.x} cy={gy(1)} r={9} fill={color.paper} stroke={color.ink} strokeWidth={3} />}
        {val > 0 && <circle cx={G.x} cy={gy(1)} r={9 + 14 * val} fill="none" stroke={color.accent} strokeWidth={3} opacity={val} />}
        {[-PI, PI].map((v) => (
          <line key={v} x1={gx(v)} y1={G.y} x2={gx(v)} y2={G.y + 10} stroke={color.ink2} strokeWidth={stroke.axis} opacity={ax} />
        ))}
      </Layer>
      <M {...L.mPi} />
      <M {...L.pi} />
      <M {...L.zero} />
      <M {...L.sinc} />
      <M {...L.one} />
      <M {...L.cos} />
      <Txt x={trapped.x} y={trapped.y} w={260} size={30} italic c={color.accent} p={mark} o={mark}>
        trapped
      </Txt>

      {/* the verdict */}
      <M {...L.verdict} />
      <Txt x={1130} y={capY} w={900} align="center" size={type.caption} italic c={color.ink2} p={p("value", 26, 50)}>
        {caption}
      </Txt>
      <Ledger x={120} y={330} st={{ show: p("paid", 24), items: [{ show: 1, paid: 1 }, { show: 1, paid, focus: 1 - paid }] }} />
    </Sheet>
  );
};
