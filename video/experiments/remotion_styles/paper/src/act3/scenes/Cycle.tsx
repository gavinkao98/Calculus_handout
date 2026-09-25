/**
 * derivative_cycle — the table page.  A booktabs table of successive
 * derivatives is filled row by row as the narration differentiates; then the
 * list "bends into a circle": each entry flies out of the table to its station
 * on the ring, and the last "sin x" lands on the first.  A red pen travels the
 * ring once (four quarter turns → home), and e^x's one-step loop is set beside
 * it for comparison.
 */
import React from "react";
import { interpolate } from "remotion";
import { color, ease, semantic, stroke } from "../../theme";
import { FormulaG } from "../../components/Formula";
import { Key, MathStage, Piece, Poses, pieceW } from "../../components/Stage";
import { SmallCaps, clamp } from "../../components/Type";
import { CycleArc } from "../../scenes/F3Cycle";
import { PAGE, camPath, useBeats } from "../clock";
import { Gloss, HEAD, InkPath, Layer, Sheet } from "./common";

const DEG = Math.PI / 180;
const T = { x0: 170, x1: 830, nX: 214, fX: 360, top: 238, head: 296, mid: 324, row0: 408, dy: 104 } as const;
const R = { cx: 1390, cy: 548, r: 252 } as const;
const SZ = { row: 64, node: 66 } as const;

const entries: { tex: string; c: string }[] = [
  { tex: "\\sin x", c: semantic.sin },
  { tex: "\\cos x", c: semantic.cos },
  { tex: "{-}\\!\\sin x", c: semantic.sin },
  { tex: "{-}\\!\\cos x", c: semantic.cos },
  { tex: "\\sin x", c: semantic.sin },
];
const ANG = [-90, 0, 90, 180, 270];
const GAP = [30, 20, 36, 20];

const P: Record<string, Piece> = Object.fromEntries(
  entries.flatMap((e, i) => [
    [`t${i}`, { tex: e.tex, color: e.c }],
    [`r${i}`, { tex: e.tex, color: e.c }],
  ]),
);

const rowY = (i: number) => T.row0 + i * T.dy;
const tablePose = (i: number): Poses[string] => ({ x: T.fX, y: rowY(i), size: SZ.row });
const nodePose = (i: number): Poses[string] => {
  const a = ANG[i] * DEG;
  const w = pieceW(P[`r${i}`], SZ.node);
  return { x: R.cx + R.r * Math.cos(a) - w / 2, y: R.cy + R.r * Math.sin(a) + 0.3 * SZ.node, size: SZ.node };
};

export const Cycle: React.FC = () => {
  const { frame, at, p, sp, dur } = useBeats();
  const rowAt = [0, at("d1"), at("d2"), at("d3"), at("d4")];
  const RING = at("ring");
  const F4 = at("fourth");
  const CMP = at("compare");

  // ── stage: table entries, then the ring copies ──
  const keys: Key[] = [];
  let snap: Poses = {};
  const push = (f: number, add: Poses) => {
    snap = { ...snap, ...add };
    keys.push({ at: f, poses: snap });
  };
  push(4, { t0: tablePose(0) });
  [1, 2, 3, 4].forEach((i) => push(rowAt[i] + 4, { [`t${i}`]: { ...tablePose(i), delay: 6 } }));
  push(RING - 1, Object.fromEntries([0, 1, 2, 3, 4].map((i) => [`r${i}`, { ...tablePose(i), o: 0 }])));
  push(RING + 8, {
    ...Object.fromEntries([0, 1, 2, 3, 4].map((i) => [`t${i}`, { ...tablePose(i), o: 0.32 }])),
    ...Object.fromEntries([0, 1, 2, 3].map((i) => [`r${i}`, { ...nodePose(i), delay: i * 7 }])),
    r4: { ...nodePose(0), delay: 4 * 7 + 6 },
  });
  push(RING + 70, { r4: { ...nodePose(0), o: 0 } });
  push(CMP, Object.fromEntries([0, 1, 2, 3, 4].map((i) => [`t${i}`, { ...tablePose(i), o: 0 }])));

  // ── camera: close on the table → the whole page as the ring forms → toward the ring ──
  const cam = camPath(
    frame,
    { cx: 560, cy: 350, s: 1.75 },
    PAGE,
    [
      { f: rowAt[1] - 6, to: { cx: 560, cy: 440, s: 1.72 }, len: 40 },
      { f: rowAt[3] - 6, to: { cx: 560, cy: 520, s: 1.7 }, len: 40 },
      { f: rowAt[4] + 6, to: { cx: 620, cy: 530, s: 1.42 }, len: 40 },
      { f: RING - 6, to: { cx: 960, cy: 540, s: 1 }, len: 50 },
      { f: F4 - 4, to: { cx: 1180, cy: 560, s: 1.22 }, len: 50 },
      { f: CMP - 4, to: { cx: 960, cy: 540, s: 1.02 }, len: 50 },
    ],
    0,
    dur,
  );

  // ── the pen goes round once: four quarter turns ──
  const dt = Math.max(18, Math.round((at("compare") - F4 - 20) / 4.6));
  let theta = -90;
  for (let k = 0; k < 4; k++) theta += 90 * interpolate(frame, [F4 + 8 + k * dt, F4 + 8 + k * dt + dt * 0.7], [0, 1], { ...clamp, easing: ease.inOut });
  // the pen slips under each station's glyph as it arrives (stations are every 90°)
  const nearNode = Math.abs((((theta + 90) % 90) + 90) % 90 - 45); // 45 = mid-arc, 0 = at a node
  const penO = interpolate(frame, [F4, F4 + 8, CMP + 10, CMP + 24], [0, 1, 1, 0], clamp) * interpolate(nearNode, [24, 36], [1, 0], clamp);
  const penX = R.cx + R.r * Math.cos(theta * DEG);
  const penY = R.cy + R.r * Math.sin(theta * DEG);
  const arrive = (k: number) => sp(F4 + 8 + k * dt + dt * 0.7, { damping: 10, stiffness: 170, mass: 0.6 });
  const home = arrive(3); // back at sin x

  // ── e^x's one-step loop (compare): the same ring, with a single station ──
  const eIn = p(CMP + 6, 20);
  const E = { cx: 520, cy: R.cy + 40, r: 120 };

  return (
    <Sheet cam={cam} head={{ ...HEAD, folio: "118" }}>
      {/* table furniture */}
      <div style={{ opacity: 1 - p(CMP, 20) }}>
        <div style={{ position: "absolute", left: T.x0, top: 172 }}>
          <SmallCaps>Table 3.2 · Successive derivatives</SmallCaps>
        </div>
        <Layer>
          <line x1={T.x0} y1={T.top} x2={T.x0 + (T.x1 - T.x0) * p(0, 24)} y2={T.top} stroke={color.ink} strokeWidth={2.6} />
          <line x1={T.x0} y1={T.mid} x2={T.x0 + (T.x1 - T.x0) * p(8, 24)} y2={T.mid} stroke={color.ink2} strokeWidth={1.4} />
          <line x1={T.x0} y1={rowY(4) + 46} x2={T.x0 + (T.x1 - T.x0) * p(rowAt[4] + 10, 24)} y2={rowY(4) + 46} stroke={color.ink} strokeWidth={2.6} />
          <g opacity={p(10, 16)}>
            <g transform={`translate(${T.nX} ${T.head})`}>
              <FormulaG tokens={[{ key: "n", tex: "n", color: color.ink2 }]} opts={{ size: 44, align: "center" }} />
            </g>
            <g transform={`translate(${T.fX} ${T.head})`}>
              <FormulaG tokens={[{ key: "f", tex: "\\dfrac{d^{\\,n}}{dx^{n}}\\sin x", color: color.ink2 }]} opts={{ size: 40 }} />
            </g>
          </g>
          {[0, 1, 2, 3, 4].map((i) => {
            const o = i === 0 ? p(6, 14) : p(rowAt[i] + 2, 14);
            return (
              <g key={i} opacity={o} transform={`translate(${T.nX} ${rowY(i)})`}>
                <FormulaG tokens={[{ key: "n", tex: String(i), color: color.ink2 }]} opts={{ size: 46, align: "center" }} />
              </g>
            );
          })}
          {/* d/dx hops between rows, on the right edge of the table */}
          {[1, 2, 3, 4].map((i) => {
            const q = p(rowAt[i] - 2, 18);
            const y0 = rowY(i - 1) - 20;
            const y1 = rowY(i) - 34;
            const x = 640;
            const d = `M${x} ${y0} C${x + 56} ${y0 + 10}, ${x + 56} ${y1 - 10}, ${x + 6} ${y1} M${x + 22} ${y1 - 16} L${x + 6} ${y1} L${x + 26} ${y1 + 8}`;
            return (
              <g key={`hop${i}`}>
                <InkPath d={d} len={200} p={q} w={3} />
                <g opacity={p(rowAt[i] + 6, 12)} transform={`translate(${x + 66} ${(y0 + y1) / 2 + 12})`}>
                  <FormulaG tokens={[{ key: "d", tex: "\\tfrac{d}{dx}", color: color.accent }]} opts={{ size: 44 }} />
                </g>
              </g>
            );
          })}
        </Layer>
      </div>

      <Layer>
        {/* the ring */}
        <circle cx={R.cx} cy={R.cy} r={R.r} fill="none" stroke={color.rule} strokeWidth={1.6} strokeDasharray="1.5 8" strokeLinecap="round" opacity={p(RING, 20)} />
        {[0, 1, 2, 3].map((i) => {
          const a1 = ANG[i] + GAP[i];
          const a2 = ANG[i + 1] - GAP[(i + 1) % 4];
          const q = p(RING + 16 + i * 9, 18);
          const mid = ((ANG[i] + ANG[i + 1]) / 2) * DEG;
          return (
            <g key={`arc${i}`}>
              <CycleArc cx={R.cx} cy={R.cy} r={R.r} a1={a1} a2={a2} progress={q} head={q >= 1 ? 1 : 0} />
              <g opacity={p(RING + 26 + i * 9, 12)} transform={`translate(${R.cx + (R.r + 66) * Math.cos(mid)} ${R.cy + (R.r + 66) * Math.sin(mid) + 14})`}>
                <FormulaG tokens={[{ key: "d", tex: "\\frac{d}{dx}", color: color.accent }]} opts={{ size: 40, align: "center" }} />
              </g>
            </g>
          );
        })}
        {/* node halos swell as the pen arrives */}
        {[0, 1, 2, 3].map((k) => {
          const g = arrive(k);
          const pulse = Math.max(0, Math.sin(Math.min(1, g) * Math.PI)) * (frame > F4 ? 1 : 0);
          const node = (k + 1) % 4;
          const a = ANG[node] * DEG;
          return pulse > 0.01 ? (
            <circle key={`pl${k}`} cx={R.cx + R.r * Math.cos(a)} cy={R.cy + R.r * Math.sin(a)} r={60 + 26 * pulse} fill={color.accent} opacity={0.1 * pulse} />
          ) : null;
        })}
        <MathStage pieces={P} keys={keys} />
        {penO > 0 && <circle cx={penX} cy={penY} r={11} fill={color.accent} stroke={color.paper} strokeWidth={stroke.ring} opacity={penO} />}

        {/* centre: four turns home */}
        <g opacity={p(at("fourth", 0.35), 18)} transform={`translate(${R.cx} ${R.cy + 16 - 6 * home})`}>
          <FormulaG tokens={[{ key: "c", tex: "\\frac{d^{4}}{dx^{4}}\\sin x=\\sin x" }]} opts={{ size: 42, align: "center" }} />
        </g>

        {/* e^x: renews itself in a single step */}
        <g opacity={eIn}>
          <circle cx={E.cx} cy={E.cy} r={E.r} fill="none" stroke={color.rule} strokeWidth={1.6} strokeDasharray="1.5 8" strokeLinecap="round" />
          <CycleArc cx={E.cx} cy={E.cy} r={E.r} a1={-90 + 34} a2={270 - 34} progress={p(CMP + 14, 30)} head={p(CMP + 14, 30) >= 1 ? 1 : 0} />
          <g transform={`translate(${E.cx} ${E.cy + E.r + 64})`}>
            <FormulaG tokens={[{ key: "d", tex: "\\frac{d}{dx}", color: color.accent }]} opts={{ size: 40, align: "center" }} />
          </g>
          <g transform={`translate(${E.cx} ${E.cy - E.r + 26})`}>
            <FormulaG tokens={[{ key: "e", tex: "e^{x}" }]} opts={{ size: 76, align: "center" }} />
          </g>
        </g>
      </Layer>
      <Gloss x={E.cx} w={520} align="center" y={R.cy + R.r + 74} size={40} opacity={p(CMP + 24, 18)}>
        one step
      </Gloss>
      <Gloss x={R.cx} w={520} align="center" y={R.cy + R.r + 74} size={40} opacity={p(at("compare", 0.35), 18)}>
        four steps
      </Gloss>
    </Sheet>
  );
};
