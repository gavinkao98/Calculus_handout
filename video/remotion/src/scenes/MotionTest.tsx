import React from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { color, ease, semantic, springs, stroke, type } from "../theme";
import { BrandLockup, Camera, Page } from "../components/Shell";
import { Vignette } from "../components/Paper";
import { InkReveal, InlineTex, Para, Rule, SmallCaps, clamp } from "../components/Type";
import { FormulaG, FormulaMorph, LayoutOpts } from "../components/Formula";
import { Curve, Dot, Label, PlotFrame, RangeAxes, SlopeTriangle, Tangent, TangentNote, px } from "../components/Plot";
import { EqNumber, FigureCaption } from "../components/Marginalia";
import { HEAD, symbols, words } from "../content";
import { PanelTitle, xTicks, yTicks } from "./F2Slope";

const PI = Math.PI;
// The page is a 2400 × 1350 spread (16:9 at s = 0.8); the camera frames parts of it.
const PW = 2400;
const PH = 1350;
const A: PlotFrame = { ox: 600, oy: 390, ux: 150, uy: 132 };
const B: PlotFrame = { ox: 600, oy: 890, ux: 150, uy: 132 };
const X0 = -0.35;
const X1 = 2 * PI + 0.3;
const COL = 1650; // right text column (x): the formula lives here
const RIGHT = PW - 120;

// beat boundaries (frames @30fps): the shared 15 s script
const T = { push: 75, slide: 135, pull: 255, morph: 318, hold: 405 } as const;

type Cam = { cx: number; cy: number; s: number };
const mix = (a: Cam, b: Cam, t: number): Cam => ({
  cx: a.cx + (b.cx - a.cx) * t,
  cy: a.cy + (b.cy - a.cy) * t,
  s: a.s * Math.pow(b.s / a.s, t), // log-space zoom reads as constant speed
});
const fmt2 = (m: number) => (Math.abs(m) < 0.005 ? "0.00" : m < 0 ? `−${Math.abs(m).toFixed(2)}` : m.toFixed(2));

export const MotionTest: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // ── the moving x: 0 → π with a heavy ease ──
  const xt = interpolate(frame, [T.slide + 3, T.pull - 5], [0, PI], { ...clamp, easing: ease.inOut });
  const m = Math.cos(xt);
  const y = Math.sin(xt);

  // ── rostrum camera ──
  const open: Cam = { cx: 960, cy: 545, s: 1.0 };
  const push: Cam = { cx: 890, cy: 402, s: 2.0 };
  const track: Cam = { cx: 900 + (xt / PI) * 24, cy: 632, s: 1.2 };
  const wide: Cam = { cx: PW / 2, cy: PH / 2, s: 0.8 };
  let cam = mix(open, { ...open, s: 1.025 }, interpolate(frame, [0, T.push], [0, 1], clamp)); // breathing drift
  cam = mix(cam, push, interpolate(frame, [T.push, T.slide], [0, 1], { ...clamp, easing: ease.camera }));
  cam = mix(cam, track, interpolate(frame, [T.slide, T.slide + 42], [0, 1], { ...clamp, easing: ease.camera }));
  cam = mix(cam, wide, interpolate(frame, [T.pull, T.morph - 4], [0, 1], { ...clamp, easing: ease.camera }));

  // ── beat 1: both frames ink in; sin draws on ──
  const axA = interpolate(frame, [8, 32], [0, 1], { ...clamp, easing: ease.ink });
  const axB = interpolate(frame, [16, 40], [0, 1], { ...clamp, easing: ease.ink });
  const lblA = interpolate(frame, [30, 44], [0, 1], clamp);
  const sinP = interpolate(frame, [22, 72], [0, 1], { ...clamp, easing: ease.ink });
  const titleA = interpolate(frame, [58, 74], [0, 1], clamp);

  // ── beat 2: tangent springs in at x = 0 ──
  const dotP = spring({ frame: frame - 84, fps, config: springs.pop });
  const grow = spring({ frame: frame - 92, fps, config: springs.tangent });
  const tri = interpolate(frame, [104, 126], [0, 1], { ...clamp, easing: ease.ink });
  const note = interpolate(frame, [108, 122], [0, 1], clamp);

  // ── beat 3: cos inks in behind the tracker ──
  const titleB = interpolate(frame, [150, 166], [0, 1], clamp);
  const cosEnd =
    frame < T.pull
      ? frame < 150
        ? interpolate(frame, [140, 150], [0, 0.02], clamp)
        : xt
      : interpolate(frame, [T.pull, T.pull + 45], [PI, X1], { ...clamp, easing: ease.ink });
  // cos starts at the y-axis (x = 0) so it never runs through the "1" tick label
  const cosP = frame < 140 ? 0 : cosEnd / X1;
  const trackO = interpolate(frame, [146, 162], [0, 1], clamp);

  // ── beats 4–5: the sentence, then sentence → symbols ──
  const origin = { x: COL, y: 520 };
  const fromOpts: LayoutOpts = { size: 56, leading: 1.38 };
  const toOpts: LayoutOpts = { size: 84 };
  const target = { x: COL, y: 688 };
  const toOffset: [number, number] = [target.x - origin.x, target.y - origin.y];
  const wordsIn = (i: number) => interpolate(frame, [284 + i * 2.5, 298 + i * 2.5], [0, 1], clamp);
  const headIn = interpolate(frame, [276, 290], [0, 1], clamp);
  // the heading waits for the words on line 1 to clear before it slides down onto the equation
  const headSwap = interpolate(frame, [T.morph + 26, T.morph + 46], [0, 1], { ...clamp, easing: ease.inOut });
  const headY = interpolate(frame, [T.morph + 28, T.morph + 60], [398, 532], { ...clamp, easing: ease.camera });

  const [pxP, pyP] = px(A, xt, y);
  const [, pyQ] = px(B, xt, m);
  const [bx, by0] = px(B, xt, 0);

  return (
    <AbsoluteFill style={{ backgroundColor: color.paper }}>
      <Camera {...cam}>
        <Page w={PW} h={PH} head={HEAD} headFrom={4} headRight={interpolate(frame, [T.pull + 20, T.morph], [0, 1], clamp)} device={false}>
          <svg width={PW} height={PH} style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }}>
            <defs>
              <clipPath id="mtClipA">
                <rect x={470} y={130} width={1200} height={500} />
              </clipPath>
            </defs>

            {/* connector: plumb line from the sine point to the cosine point (under the labels' halos) */}
            <line x1={pxP} y1={pyP + 12} x2={pxP} y2={pyQ - 12} stroke={color.ink3} strokeWidth={1.5} strokeDasharray="1.5 6" strokeLinecap="round" opacity={trackO} />

            {/* panel frames */}
            <RangeAxes f={A} x={[0, 2 * PI]} y={[-1, 1]} xTicks={xTicks} yTicks={yTicks} progress={axA} labels={lblA} />
            <RangeAxes f={B} x={[0, 2 * PI]} y={[-1, 1]} xTicks={xTicks.map((t) => ({ v: t.v }))} yTicks={yTicks} progress={axB} labels={lblA} />
            <PanelTitle x={1400} y={262} letter="a" tokens={[{ key: "y", tex: "y=\\sin x" }]} opacity={titleA} />
            <PanelTitle x={1400} y={1052} letter="b" tokens={[{ key: "y", tex: "y=\\cos x", color: semantic.cos }]} opacity={titleB} />

            <Curve f={A} fn={Math.sin} a={X0} b={X1} progress={sinP} c={semantic.sin} />

            <Curve f={B} fn={Math.cos} a={0} b={X1} progress={cosP} c={semantic.cos} />

            {/* equal red bars: rise of the tangent per unit run  =  height of cos */}
            <SlopeTriangle f={A} x0={xt} y0={y} m={m} progress={tri} />
            {Math.abs(m) > 0.004 && (
              <line x1={bx} y1={by0} x2={bx} y2={pyQ} stroke={color.accent} strokeWidth={stroke.emphasis} strokeLinecap="round" opacity={trackO} />
            )}
            <g clipPath="url(#mtClipA)">
              <Tangent f={A} x0={xt} y0={y} m={m} half={240} grow={grow} />
            </g>
            <Dot f={A} x={xt} y={y} scale={dotP} />
            <Dot f={B} x={xt} y={m} c={semantic.cos} opacity={trackO} scale={trackO} />

            <TangentNote f={A} x0={xt} y0={y} m={m} at={118 * Math.max(-1, Math.min(1, m * 3))} lift={22} opacity={note}>
              <tspan fontStyle="italic">slope</tspan> {fmt2(m)}
            </TangentNote>
            <g className="halo" opacity={trackO}>
              <Label x={bx + 20} y={pyQ + interpolate(m, [-1, 0], [44, -18], clamp)} c={color.ink} figures>
                <tspan fontStyle="italic">height</tspan> {fmt2(m)}
              </Label>
            </g>

            {/* the sentence, then the token morph */}
            <g transform={`translate(${origin.x} ${origin.y})`}>
              {frame < T.morph ? (
                <FormulaG tokens={words} opts={fromOpts} reveal={wordsIn} />
              ) : (
                <FormulaMorph from={words} to={symbols} fromOpts={fromOpts} toOpts={toOpts} toOffset={toOffset} start={T.morph} stagger={4} order={["eq", "cos", "x2", "op", "sin", "x1"]} />
              )}
            </g>
          </svg>

          <InkReveal from={40} len={30} style={{ left: 120, top: 250, width: 300, height: 360 }}>
            <FigureCaption n="3.3" x={0} y={0} w={290}>
              The tangent to <span style={{ fontStyle: "normal" }}>sin</span> slides from 0 to π; its slope is always the
              height of <span style={{ fontStyle: "normal", color: semantic.cos }}>cos</span> directly below.
            </FigureCaption>
          </InkReveal>

          {/* right column heading: "In words" → "In symbols", sliding down to sit on the equation */}
          <div style={{ position: "absolute", left: COL, top: headY, opacity: headIn }}>
            <div style={{ width: 56, height: 2.5, background: color.accent, marginBottom: 18 }} />
            <div style={{ position: "relative", height: 30 }}>
              <div style={{ position: "absolute", opacity: 1 - headSwap }}>
                <SmallCaps>In words</SmallCaps>
              </div>
              <div style={{ position: "absolute", opacity: headSwap }}>
                <SmallCaps>In symbols</SmallCaps>
              </div>
            </div>
          </div>
          <EqNumber y={target.y - 36} n="3.3" right={RIGHT} opacity={interpolate(frame, [384, 400], [0, 1], clamp)} />
          <InkReveal from={392} len={26} style={{ left: COL, top: 780, width: RIGHT - COL, height: 140 }}>
            <Para x={0} y={0} w={RIGHT - COL} size={type.caption + 1} color={color.ink2} italic lh={1.5}>
              Likewise, the slope of <span style={{ fontStyle: "normal", color: semantic.cos }}>cos</span> is the height of{" "}
              <span style={{ fontStyle: "normal" }}>−sin</span>:
              <br />
              <InlineTex src={`{\\color{${color.accent}}\\dfrac{d}{dx}}\\,{\\color{${semantic.cos}}\\cos x}={-}\\!\\sin x`} scale={1.05} color={color.ink} />
            </Para>
          </InkReveal>

          {/* colophon band */}
          <Rule x={120} y={1160} w={PW - 240} from={392} len={26} />
          <InkReveal from={398} len={28} style={{ left: RIGHT - 333, top: 1178, width: 333, height: 96 }}>
            <BrandLockup x={0} y={0} h={96} />
          </InkReveal>
          <InkReveal from={404} len={24} style={{ left: 120, top: 1214, width: 700, height: 40 }}>
            <SmallCaps color={color.ink3} size={type.smallCaps}>
              Next · the four-step cycle
            </SmallCaps>
          </InkReveal>
        </Page>
      </Camera>
      <Vignette />
    </AbsoluteFill>
  );
};
