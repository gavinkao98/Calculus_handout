/**
 * slope_equals_height — the figure plate (Figure 3.3), a page wider than the
 * frame: the two panels fill the left, the "in words / in symbols" column
 * waits off-frame on the right.  One live tangent rides sine the whole scene
 * (0 → π/2 → π, then a free sweep to 2π), leaving an inked stamp at each
 * stop; cosine's heights are read off with red bars equal to the rises.
 */
import React from "react";
import { interpolate } from "remotion";
import { color, ease, semantic, stroke, type } from "../../theme";
import { InkReveal, SmallCaps, clamp } from "../../components/Type";
import { FormulaG, FormulaMorph, LayoutOpts } from "../../components/Formula";
import { Curve, Dot, Label, PlotFrame, RangeAxes, SlopeTriangle, Tangent, TangentNote, Tick, px } from "../../components/Plot";
import { EqNumber } from "../../components/Marginalia";
import { symbols, words } from "../../content";
import { camPath, useBeats } from "../clock";
import { Gloss, HEAD, Layer, Sheet } from "./common";

const PI = Math.PI;
const PW = 2700;
const A: PlotFrame = { ox: 250, oy: 330, ux: 205, uy: 150 };
const B: PlotFrame = { ox: 250, oy: 790, ux: 205, uy: 150 };
const X1 = 2 * PI + 0.28;
const COL = 1880;
const RIGHT = PW - 130;

const xTicks: Tick[] = [
  { v: PI / 2, label: [{ key: "t", tex: "\\pi/2" }] },
  { v: PI, label: [{ key: "t", tex: "\\pi" }] },
  { v: (3 * PI) / 2, label: [{ key: "t", tex: "3\\pi/2" }] },
  { v: 2 * PI, label: [{ key: "t", tex: "2\\pi" }] },
];
const yTicks: Tick[] = [
  { v: 1, label: [{ key: "t", tex: "1" }] },
  { v: -1, label: [{ key: "t", tex: "{-}1" }] },
];
const fmt2 = (m: number) => (Math.abs(m) < 0.005 ? "0" : m < 0 ? `−${Math.abs(m).toFixed(2)}` : m.toFixed(2)).replace(/\.00$/, "");

/** Panel title: "(a)" + math. */
const PanelTitle: React.FC<{ x: number; y: number; letter: string; tex: string; c?: string; opacity?: number }> = ({ x, y, letter, tex, c, opacity = 1 }) => (
  <g opacity={opacity}>
    <Label x={x} y={y} italic c={color.ink2} size={type.label + 4}>
      ({letter})
    </Label>
    <g transform={`translate(${x + 52} ${y})`}>
      <FormulaG tokens={[{ key: "y", tex, color: c }]} opts={{ size: type.label + 12 }} />
    </g>
  </g>
);

export const SlopeHeight: React.FC = () => {
  const { frame, at, atWord, p, sp } = useBeats();
  const tH = at("tanhalf");
  const tP = at("tanpi");
  const sw = at("sweep");
  const W = at("words");
  const S = at("symbols");

  // ── the live x ── each leg lands on the word that names its destination
  // (the tangent visibly goes flat right as "flat" is said, etc.); a mock
  // manifest has no alignment, so fall back to the old fixed fraction.
  const tanhalfEnd = atWord("flat", { afterFrame: tH }) ?? at("tanhalf", 0.5);
  const tanpiEnd = atWord("negative one", { afterFrame: tP }) ?? at("tanpi", 0.6);
  const sweepEnd = atWord("it", { afterFrame: sw }) ?? at("sweep", 0.88);
  const xt =
    frame < tP
      ? interpolate(frame, [tH + 4, tanhalfEnd], [0, PI / 2], { ...clamp, easing: ease.inOut })
      : frame < sw
        ? interpolate(frame, [tP + 2, tanpiEnd], [PI / 2, PI], { ...clamp, easing: ease.inOut })
        : interpolate(frame, [sw + 8, sweepEnd], [PI, 2 * PI], { ...clamp, easing: ease.inOut });
  const m = Math.cos(xt);
  const y = Math.sin(xt);

  // ── camera: full plate → panel (a), riding the tangent → full plate → the words column ──
  const [txp] = px(A, xt, 0);
  const cam = camPath(
    frame,
    { cx: 960, cy: 540, s: 1 },
    { w: PW, h: 1080 },
    [
      { f: at("sine") + 10, to: { cx: 860, cy: 345, s: 1.6 }, len: 50 },
      { f: at("tan0") - 4, to: { cx: txp + 330, cy: 345, s: 1.65 }, len: 36 },
      { f: at("cosine") - 6, to: { cx: 960, cy: 548, s: 1.0 }, len: 44 },
      { f: sw, to: { cx: 1000, cy: 548, s: 1.04 }, len: 60 },
      { f: W - 6, to: { cx: PW - 900, cy: 540, s: 1.0 }, len: 50 },
      { f: S + 30, to: { cx: PW - 900, cy: 560, s: 1.08 }, len: 60 },
    ],
  );

  // ── inking ──
  const axA = p(4, 26);
  const axB = p(12, 26); // both frames are on the plate from the start; only (a) is filled first
  const lblA = p(20, 16);
  const lblB = p(at("cosine") + 6, 16);
  const sinP = p(at("sine"), 44);
  const cosP = p(at("cosine") + 4, 40);
  const tanIn = sp(at("tan0") + 2, { damping: 11, stiffness: 150, mass: 0.7 });
  const liveNote = p(at("tan0") + 14, 12);
  const tri = p(at("tan0") + 16, 20);
  const sweepDim = interpolate(frame, [sw, sw + 20], [1, 0.4], clamp);
  const stampText = 1 - p(sw, 16); // stamp readouts step aside for the live ones

  // stamps left behind at 0, π/2, π
  const stamps = [
    { x: 0, from: tH + 4 },
    { x: PI / 2, from: tP + 2 },
    { x: PI, from: sw + 8 },
  ];
  // heights read at the same three points — anchored to the words that name
  // them ("...one, zero, negative one"), falling back to the old fractions
  // when the scene has no word-level alignment
  const heightsStart = at("heights");
  const heightCues = [
    { w: "one", k: 0.4 },
    { w: "zero", k: 0.53 },
    { w: "negative one", k: 0.64 },
  ];
  const heights = heightCues.map((h, i) => ({ x: stamps[i].x, from: atWord(h.w, { afterFrame: heightsStart }) ?? at("heights", h.k) }));
  const matchAt = atWord("match", { afterFrame: heightsStart }) ?? at("heights", 0.8);
  const match = interpolate(frame, [matchAt, matchAt + 10, matchAt + 30], [0, 1, 0], clamp);
  const liveB = p(sw + 4, 14); // the live cosine reading joins for the sweep
  const [bx0, by0] = px(B, xt, 0);
  const [, byq] = px(B, xt, m);
  const [pxA, pyA] = px(A, xt, y);

  // ── words → symbols ──
  const fromOpts: LayoutOpts = { size: 54, leading: 1.42 };
  const toOpts: LayoutOpts = { size: 80 };
  const origin = { x: COL, y: 530 };
  const target = { x: COL + 6, y: 850 };
  const toOffset: [number, number] = [target.x - origin.x, target.y - origin.y];
  const wordsIn = (i: number) => interpolate(frame, [W + 6 + i * 4, W + 20 + i * 4], [0, 1], clamp);

  return (
    <Sheet cam={cam} w={PW} head={{ ...HEAD, folio: "116" }}>
      <Layer w={PW}>
        <defs>
          <clipPath id="shA">
            <rect x={150} y={120} width={1560} height={420} />
          </clipPath>
        </defs>
        {/* plumb lines from sine's points down to cosine's (under the halos) */}
        {heights.map((h) => {
          const o = p(h.from - 6, 12);
          const [x1, y1] = px(A, h.x, Math.sin(h.x));
          const [, y2] = px(B, h.x, Math.cos(h.x));
          return <line key={`pl${h.x}`} x1={x1} y1={y1 + 14} x2={x1} y2={y2 - 14} stroke={color.ink3} strokeWidth={1.6} strokeDasharray="1.5 7" strokeLinecap="round" opacity={o * sweepDim} />;
        })}
        <line x1={pxA} y1={pyA + 14} x2={pxA} y2={byq - 14} stroke={color.ink3} strokeWidth={1.6} strokeDasharray="1.5 7" strokeLinecap="round" opacity={liveB} />

        <RangeAxes f={A} x={[0, 2 * PI]} y={[-1, 1]} xTicks={xTicks} yTicks={yTicks} progress={axA} labels={lblA} />
        <RangeAxes f={B} x={[0, 2 * PI]} y={[-1, 1]} xTicks={xTicks.map((t) => ({ v: t.v }))} yTicks={yTicks} progress={axB} labels={lblB} />
        <PanelTitle x={1500} y={170} letter="a" tex="y=\sin x" opacity={p(at("sine") + 20, 16)} />
        <PanelTitle x={1500} y={1000} letter="b" tex="y=\cos x" c={semantic.cos} opacity={p(at("cosine") + 20, 16)} />

        <Curve f={A} fn={Math.sin} a={-0.3} b={X1} progress={sinP} c={semantic.sin} />
        <Curve f={B} fn={Math.cos} a={0} b={X1} progress={cosP} c={semantic.cos} />

        {/* stamps: the tangent's past positions, inked and left on the page */}
        {stamps.map((s) => {
          const o = p(s.from, 10) * sweepDim;
          if (o <= 0) return null;
          const mm = Math.round(Math.cos(s.x));
          return (
            <g key={`st${s.x}`} opacity={o}>
              <g clipPath="url(#shA)">
                <Tangent f={A} x0={s.x} y0={Math.sin(s.x)} m={mm} half={230} width={2.6} opacity={0.75} />
              </g>
              <SlopeTriangle f={A} x0={s.x} y0={Math.sin(s.x)} m={mm} />
              {match > 0 && mm !== 0 && (
                <SlopeTriangleGlow f={A} x0={s.x} y0={Math.sin(s.x)} m={mm} k={match} />
              )}
              <Dot f={A} x={s.x} y={Math.sin(s.x)} />
              <TangentNote f={A} x0={s.x} y0={Math.sin(s.x)} m={mm} at={[112, 150, -112][stamps.indexOf(s)]} lift={24} opacity={stampText}>
                <tspan fontStyle="italic">slope</tspan> {fmt2(mm)}
              </TangentNote>
            </g>
          );
        })}

        {/* cosine's heights: red bars the same length as the rises above */}
        {heights.map((h) => {
          const g = sp(h.from, { damping: 12, stiffness: 160, mass: 0.7 });
          const o = Math.min(1, g) * sweepDim;
          if (g <= 0.001) return null;
          const v = Math.round(Math.cos(h.x));
          const [bx, by] = px(B, h.x, 0);
          const [, qy] = px(B, h.x, v * Math.min(1.08, g));
          return (
            <g key={`h${h.x}`} opacity={o}>
              {v !== 0 && <line x1={bx} y1={by} x2={bx} y2={qy} stroke={color.accent} strokeWidth={stroke.emphasis + 3 * match} strokeLinecap="round" />}
              <Dot f={B} x={h.x} y={v} c={semantic.cos} scale={Math.min(1, g)} />
              <g className="halo" opacity={stampText}>
                <Label x={bx + 20} y={v === 0 ? by - 24 : v > 0 ? by - 50 : by + 60} c={color.ink} figures>
                  <tspan fontStyle="italic">height</tspan> {fmt2(v)}
                </Label>
              </g>
            </g>
          );
        })}

        {/* the live tangent */}
        <g clipPath="url(#shA)">
          <Tangent f={A} x0={xt} y0={y} m={m} half={250} grow={tanIn} />
        </g>
        <SlopeTriangle f={A} x0={xt} y0={y} m={m} progress={tri} />
        <Dot f={A} x={xt} y={y} scale={tanIn} />
        {/* the live readout rides BELOW its line; the stamps keep theirs above, so they never collide */}
        <TangentNote f={A} x0={xt} y0={y} m={m} at={-130 * Math.max(-1, Math.min(1, m * 4))} lift={-52} opacity={liveNote}>
          <tspan fontStyle="italic">slope</tspan> {fmt2(m)}
        </TangentNote>

        {/* the live cosine reading (sweep only) */}
        {liveB > 0 && (
          <g opacity={liveB}>
            {Math.abs(m) > 0.004 && <line x1={bx0} y1={by0} x2={bx0} y2={byq} stroke={color.accent} strokeWidth={stroke.emphasis} strokeLinecap="round" />}
            <Dot f={B} x={xt} y={m} c={semantic.cos} />
            <g className="halo">
              <Label x={bx0 + 20} y={byq + (m < 0 ? 60 : -30)} c={color.ink} figures>
                <tspan fontStyle="italic">height</tspan> {fmt2(m)}
              </Label>
            </g>
          </g>
        )}

        {/* words → symbols */}
        <g transform={`translate(${origin.x} ${origin.y})`}>
          {frame < S ? (
            <FormulaG tokens={words} opts={fromOpts} reveal={wordsIn} />
          ) : (
            <g opacity={interpolate(frame, [S, S + 30], [0, 0.42], clamp)}>
              <FormulaG tokens={words} opts={fromOpts} />
            </g>
          )}
          {frame >= S && (
            <FormulaMorph from={words} to={symbols} fromOpts={fromOpts} toOpts={toOpts} toOffset={toOffset} start={S} stagger={4} order={["eq", "cos", "x2", "op", "sin", "x1"]} />
          )}
        </g>
      </Layer>

      {/* figure caption, top of the right column */}
      <InkReveal from={at("cosine") + 20} len={30} style={{ left: COL, top: 160, width: RIGHT - COL, height: 220 }}>
        <SmallCaps color={color.accent}>Figure 3.3</SmallCaps>
        <Gloss x={0} y={46} w={RIGHT - COL} size={type.caption}>
          Each tangent to <span style={{ fontStyle: "normal" }}>sin</span> rises, per unit of run, by the height of{" "}
          <span style={{ fontStyle: "normal", color: semantic.cos }}>cos</span> below it.
        </Gloss>
      </InkReveal>

      {/* "In words", then "In symbols" under it: the sentence stays (dimmed) above its formula */}
      {[
        { label: "In words", top: 390, o: p(W, 14) },
        { label: "In symbols", top: 690, o: p(S + 20, 16) },
      ].map((h) => (
        <div key={h.label} style={{ position: "absolute", left: COL, top: h.top, opacity: h.o }}>
          <div style={{ width: 60, height: 3, background: color.accent, marginBottom: 18 }} />
          <SmallCaps>{h.label}</SmallCaps>
        </div>
      ))}
      <EqNumber y={target.y - 40} n="3.1" right={RIGHT} opacity={p(S + 50, 16)} />
    </Sheet>
  );
};

/** A brief swelling of a slope triangle's red rise ("they match"). */
const SlopeTriangleGlow: React.FC<{ f: PlotFrame; x0: number; y0: number; m: number; k: number }> = ({ f, x0, y0, m, k }) => {
  const [bx, ay] = px(f, x0 + 1, y0);
  const [, cy] = px(f, x0 + 1, y0 + m);
  return <line x1={bx} y1={ay} x2={bx} y2={cy} stroke={color.accent} strokeWidth={stroke.emphasis + 3 * k} strokeLinecap="round" />;
};
