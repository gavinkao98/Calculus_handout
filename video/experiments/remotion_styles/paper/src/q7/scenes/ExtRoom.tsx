/**
 * zh extension 2 (EXTENSION.zh.md §三): the (b) table cut by its four
 * symmetry axes into eight isosceles right triangles; folding the square into
 * one of them (y=0, x=0, y=x — three page turns, exact: extGeo.ts) turns the
 * ball into a ball in the triangle, and sends all eight pockets to its two
 * other vertices (edge midpoints → the right angle M, corners → K). So (b)'s
 * zero says: light from a 45° corner, absorbed at vertices, never returns to
 * it. Then the illumination problem — a SCHEMATIC room tiled from such
 * triangles (not Tokarsky's room: no computed rays, captioned as such).
 */
import React from "react";
import { interpolate } from "remotion";
import { color, type } from "../../theme";
import { clamp } from "../../components/Type";
import { EDGE, Flash, HomeDot, Kicker, Layer, M, Mark, POCKET, Pocket, Pt, R_POCKET, Sheet, Txt, W_POCKET, World, arcPts, dOf, mLbl, px, pxs, toD, useS, useT } from "../kit";
import { V, polyAt, realPath, shot } from "../geo";
import { SQUARE, foldPath, foldPt, paperAt, triFold } from "../extGeo";

const BIG: World = { ox: 1300, oy: 570, u: 320 };
const TRI: World = { ox: 1000, oy: 880, u: 640 };
const ICON: World = { ox: 1600, oy: 330, u: 160 };
const O: V = [0, 0];
const MV: V = [1, 0];
const KV: V = [1, 1];
const RIM: V[] = [
  [1, 0],
  [1, 1],
  [0, 1],
  [-1, 1],
  [-1, 0],
  [-1, -1],
  [0, -1],
  [1, -1],
];
const HOLES: Array<{ v: V; mid: boolean }> = RIM.map((v) => ({ v, mid: v[0] === 0 || v[1] === 0 }));
const AXES: V[][] = [
  [
    [0, -1],
    [0, 1],
  ],
  [
    [-1, 0],
    [1, 0],
  ],
  [
    [-1, -1],
    [1, 1],
  ],
  [
    [-1, 1],
    [1, -1],
  ],
];
const CUT = realPath(shot([2, 1], 1)); // (0,0) → (1,½) → (0,1): the top midpoint pocket
/** light from O: square (b) shots folded into the triangle; each ends on M (mixed parity) or K (odd, odd) */
const LIGHT: Array<{ pts: V[]; end: V; mid: boolean }> = (
  [
    [2, 1],
    [3, 1],
    [3, 2],
    [5, 2],
    [4, 3],
    [5, 3],
  ] as V[]
).map((d) => {
  const pts = triFold(realPath(shot(d, 1)));
  const mid = (d[0] + d[1]) % 2 === 1;
  return { pts, end: mid ? MV : KV, mid };
});

/** the schematic room: ten 45°-45°-90° tiles (units of one leg) — made up, not any published room */
const ROOM: V[] = [
  [0, 0],
  [3, 0],
  [3, 1],
  [4, 2],
  [2, 2],
  [1, 1],
  [0, 1],
];
const SEAMS: V[][] = [
  [
    [1, 0],
    [1, 1],
  ],
  [
    [2, 0],
    [2, 1],
  ],
  [
    [0, 0],
    [1, 1],
  ],
  [
    [1, 0],
    [2, 1],
  ],
  [
    [2, 0],
    [3, 1],
  ],
  [
    [1, 1],
    [3, 1],
  ],
  [
    [2, 1],
    [2, 2],
  ],
  [
    [2, 1],
    [3, 2],
  ],
  [
    [3, 1],
    [3, 2],
  ],
];
const RW: World = { ox: 850, oy: 840, u: 190 };
const LAMP: V = [0.55, 0.42];
const DARK: V = [3.3, 1.62];

const lerpW = (a: World, b: World, t: number): World => ({ ox: a.ox + (b.ox - a.ox) * t, oy: a.oy + (b.oy - a.oy) * t, u: a.u * Math.pow(b.u / a.u, t) });
const smooth = (x: number) => 0.5 - 0.5 * Math.cos(Math.PI * Math.max(0, Math.min(1, x)));

export const ExtRoom: React.FC = () => {
  const { f, at, p, pf, guard } = useS();
  const { ext, r, tLbl } = useT();
  const T = ext.room;
  const tTri = at("tri");
  const tFold = at("fold");
  const tEq = at("equiv");
  const tRoom = at("room");
  const win = (a: number, b: number, len = 16) => pf(a, len) * (1 - pf(b, len));

  // ── the world: big square → the triangle alone → a small icon ──
  const zoom = smooth(interpolate(f, [tEq + 4, tEq + 44], [0, 1], clamp));
  const shrink = smooth(interpolate(f, [tRoom + 4, tRoom + 40], [0, 1], clamp));
  const W = lerpW(lerpW(BIG, TRI, zoom), ICON, shrink);

  // ── start: outline, four axes, eight triangles ──
  const draw = p("start", 30, 4);
  const axisP = AXES.map((_, i) => interpolate(f, [at("start", 0.3) + i * 16, at("start", 0.3) + i * 16 + 22], [0, 1], clamp));
  const tFlash = at("start", 0.5);
  const pick = pf(tFlash + 8 * 8, 16);

  // ── fold: the (2,1) shot, then three page turns ──
  const cutP = interpolate(f, [tFold + 6, tFold + 46], [0, 1], clamp);
  const f0 = tFold + 70;
  const stage = [0, 1, 2].reduce((s, k) => s + smooth(interpolate(f, [f0 + k * 46, f0 + k * 46 + 40], [0, 1], clamp)), 0);
  const folded = f0 + 3 * 46 - 6;
  const squareO = (1 - zoom) * (stage > 0 ? 1 : 1);
  // angle marks: all three on `tri`; on `equiv` only the 45° at O, labelled outside (the light fills the angle)
  const angTri = pf(tTri + 6, 20) * (1 - pf(tFold, 12));
  const angEq = pf(tEq + 50, 20) * (1 - pf(tRoom, 12));
  const angO = angTri + angEq;

  // ── equiv: light from O ──
  const lightT = (i: number) => tEq + 60 + i * 34;
  const lightP = (i: number) => interpolate(f, [lightT(i), lightT(i) + 44], [0, 1], clamp);
  const lightO = 1 - pf(tRoom, 14);

  // ── room ──
  const roomIn = pf(tRoom + 30, 40);
  const seamsIn = pf(tRoom + 60, 30);
  const glow = pf(tRoom + 90, 40);
  const darkIn = pf(tRoom + 130, 24);

  // triangle outline at the current world
  const triPts = [O, MV, KV, O];
  const paper = paperAt(stage);
  const holeAt = (v: V) => foldPt(v, stage);
  const pathNow = foldPath(CUT, stage);

  // angle marks (ink2: the vertices carry the semantic colours)
  const Ow = px(W, O);
  const Mw = px(W, MV);
  const Kw = px(W, KV);
  const ar = 0.2 * W.u;
  const sq = 0.09 * W.u;
  const lbl45O =
    angEq > 0
      ? { x: Ow[0] - 34, y: Ow[1] + 12, t: "45^\\circ", size: 40, align: "right" as const, c: color.ink2, p: angEq, o: angEq }
      : { x: Ow[0] + 0.34 * W.u * Math.cos(Math.PI / 8), y: Ow[1] - 0.34 * W.u * Math.sin(Math.PI / 8) + 14, t: "45^\\circ", size: 32, align: "center" as const, c: color.ink2, p: angTri, o: angTri };
  const lbl45K = { x: Kw[0] - 0.34 * W.u * Math.sin(Math.PI / 8), y: Kw[1] + 0.34 * W.u * Math.cos(Math.PI / 8) + 10, t: "45^\\circ", size: 32, align: "center" as const, c: color.ink2, p: angTri, o: angTri };
  const lbl90 = { x: Mw[0] - 0.2 * W.u, y: Mw[1] - 0.12 * W.u, t: "90^\\circ", size: 32, align: "center" as const, c: color.ink2, p: angTri, o: angTri };

  const absorb = { s: T.absorb, x: px(TRI, MV)[0], y: px(TRI, MV)[1] + 26 };
  const tileLbl = { s: T.tile, x: px(ICON, [0.5, 0])[0], y: px(ICON, [0, 0])[1] + 30 };
  // callouts outside the room (a leader line to each; the room's tiles leave no 40 px gap inside)
  const lampLbl = { s: T.lamp, x: px(RW, LAMP)[0], y: px(RW, [0, 0])[1] + 34 };
  const darkLbl = { s: T.dark, x: px(RW, DARK)[0] + 110, y: px(RW, DARK)[1] - 24 };
  const lampLead: Pt[] = [
    [px(RW, LAMP)[0], px(RW, LAMP)[1] + 16],
    [px(RW, LAMP)[0], lampLbl.y + 8],
  ];
  const darkLead: Pt[] = [
    [px(RW, DARK)[0] + 20, px(RW, DARK)[1]],
    [darkLbl.x - 10, px(RW, DARK)[1]],
  ];
  const schem = { s: T.schematic, x: px(RW, [4, 0])[0], y: px(RW, [0, 0])[1] + 26 };

  const eqOnly = zoom >= 1 && shrink <= 0;
  const marks: Mark[] = [
    { name: "triangle", pts: pxs(W, triPts), w: 4.2, on: eqOnly || shrink >= 1 },
    ...LIGHT.map((l, i): Mark => ({ name: `light ${i}`, pts: pxs(W, l.pts), w: 2.4, on: eqOnly && lightP(i) > 0 && lightO > 0.05 })),
    { name: "M ring", pts: [Mw], w: 2 * R_POCKET + W_POCKET, on: true },
    { name: "K ring", pts: [Kw], w: 2 * R_POCKET + W_POCKET, on: true },
    { name: "O dot", pts: [Ow], w: 18, on: true },
    { name: "room", pts: pxs(RW, [...ROOM, ROOM[0]]), w: 5, on: roomIn >= 1 },
    ...SEAMS.map((s, i): Mark => ({ name: `seam ${i}`, pts: pxs(RW, s), w: 1.6, on: seamsIn >= 1 })),
    { name: "lamp", pts: [px(RW, LAMP)], w: 20, on: glow > 0 },
    { name: "lamp leader", pts: lampLead, w: 1.6, on: glow > 0, owner: T.lamp },
    { name: "dark leader", pts: darkLead, w: 1.6, on: darkIn > 0, owner: T.dark },
    { name: "dark", pts: [px(RW, DARK)], w: 34, on: darkIn > 0 },
  ];
  guard(marks, [
    mLbl(lbl45O, "45° at O"),
    mLbl(lbl45K, "45° at K"),
    mLbl(lbl90, "90° at M"),
    tLbl(absorb.s, absorb.x, absorb.y, 34, pf(tEq + 20, 20) * (eqOnly ? 1 : 0), lightO, { align: "right" }),
    tLbl(tileLbl.s, tileLbl.x, tileLbl.y, 34, pf(tRoom + 40, 20), 1, { align: "center" }),
    tLbl(lampLbl.s, lampLbl.x, lampLbl.y, 34, glow, 1, { align: "center" }),
    tLbl(darkLbl.s, darkLbl.x, darkLbl.y, 34, darkIn),
    tLbl(schem.s, schem.x, schem.y, 34, roomIn, 1, { align: "right" }),
  ]);

  return (
    <Sheet folio={18} title={T.title}>
      <Layer>
        <defs>
          <radialGradient id="q7-lamp">
            <stop offset="0" stopColor={color.ochre} stopOpacity={0.42} />
            <stop offset="0.45" stopColor={color.ochre} stopOpacity={0.16} />
            <stop offset="1" stopColor={color.ochre} stopOpacity={0} />
          </radialGradient>
          <clipPath id="q7-room">
            <path d={dOf(RW, ROOM) + "Z"} />
          </clipPath>
        </defs>

        {/* the square (fades as the triangle takes over) */}
        {squareO > 0 && (
          <g opacity={squareO}>
            {stage > 0 && <path d={dOf(W, [...SQUARE, SQUARE[0]])} fill="none" stroke={color.ink3} strokeWidth={1.6} strokeDasharray="6 8" />}
            {/* the eight triangles, each lit in turn, then the one we keep */}
            {stage <= 0 &&
              RIM.map((a, i) => {
                const b = RIM[(i + 1) % 8];
                const t = f - tFlash - i * 8;
                const o = i === 0 ? pick : t > 0 && t < 22 ? Math.sin((Math.PI * t) / 22) * 0.9 : 0;
                return o > 0 ? <path key={i} d={dOf(W, [O, a, b]) + "Z"} fill={color.paperShade} opacity={o} /> : null;
              })}
            {stage <= 0 && <path d={dOf(W, [...SQUARE, SQUARE[0]])} fill="none" stroke={color.ink} strokeWidth={4.2} strokeDasharray={draw < 1 ? `${8 * W.u * draw} ${8 * W.u}` : undefined} />}
            {stage <= 0 &&
              AXES.map((ax, i) =>
                axisP[i] > 0 ? (
                  <path key={i} d={dOf(W, [ax[0], [ax[0][0] + (ax[1][0] - ax[0][0]) * axisP[i], ax[0][1] + (ax[1][1] - ax[0][1]) * axisP[i]]])} stroke={color.ink3} strokeWidth={2} strokeDasharray="7 7" />
                ) : null,
              )}
            {/* the paper while folding: still part + turning flap */}
            {stage > 0 && (
              <g>
                <path d={dOf(W, [...paper.still, paper.still[0]])} fill={color.paperShade} opacity={0.55} />
                <path d={dOf(W, [...paper.still, paper.still[0]])} fill="none" stroke={color.ink} strokeWidth={4.2} strokeLinejoin="miter" />
                {paper.flap.length > 2 && (
                  <g>
                    <path d={dOf(W, [...paper.flap, paper.flap[0]])} fill={color.paperShade} opacity={0.85} />
                    <path d={dOf(W, [...paper.flap, paper.flap[0]])} fill="none" stroke={color.ink2} strokeWidth={2.4} />
                  </g>
                )}
              </g>
            )}
          </g>
        )}

        {/* the kept triangle, from tri on */}
        {pick > 0 && stage <= 0 && <path d={dOf(W, triPts)} fill="none" stroke={color.ink} strokeWidth={3} opacity={pf(tTri, 16)} />}
        {stage >= 3 && (
          <g>
            <path d={dOf(W, triPts) + "Z"} fill={color.paperShade} opacity={0.55 * (1 - shrink * 0.3)} />
            <path d={dOf(W, triPts)} fill="none" stroke={color.ink} strokeWidth={4.2} strokeLinejoin="miter" />
          </g>
        )}

        {/* angle marks */}
        {angO > 0 && (
          <g opacity={angO} fill="none" stroke={color.ink2} strokeWidth={2.6}>
            <path d={toD(arcPts(Ow[0], Ow[1], ar, 0, Math.PI / 4, 24))} />
            <path d={`M${Mw[0] - sq} ${Mw[1]} L${Mw[0] - sq} ${Mw[1] - sq} L${Mw[0]} ${Mw[1] - sq}`} opacity={angTri / angO} />
            <path d={toD(arcPts(Kw[0], Kw[1], ar, (5 * Math.PI) / 4, (3 * Math.PI) / 2, 24))} opacity={angTri / angO} />
          </g>
        )}

        {/* the (2,1) path, folded with the paper */}
        {cutP > 0 && lightO > 0 && zoom < 1 && (
          <path d={dOf(W, stage > 0 ? pathNow : polyAt(CUT, cutP).upto)} fill="none" stroke={color.ink} strokeWidth={3.6} strokeLinecap="round" strokeLinejoin="round" opacity={1 - zoom} />
        )}
        <Flash W={W} p={[0, 1]} t={(f - tFold - 46) / 24} c={EDGE} r1={50} />

        {/* pockets (folded with the paper) and the centre */}
        {draw >= 1 &&
          HOLES.map((h, i) => {
            const q = holeAt(h.v);
            return <Pocket key={i} W={W} p={q} c={h.mid ? EDGE : POCKET} r={shrink > 0 ? R_POCKET * (1 - 0.3 * shrink) : R_POCKET} />;
          })}
        {draw >= 1 && <HomeDot W={W} p={O} r={shrink > 0 ? 8 - 2 * shrink : 8} />}
        <Flash W={W} p={MV} t={(f - folded) / 26} c={EDGE} r1={54} />
        <Flash W={W} p={KV} t={(f - folded - 8) / 26} c={POCKET} r1={54} />

        {/* equiv: light from the 45° corner O, absorbed at M or K */}
        {zoom > 0 && lightO > 0 && (
          <g opacity={lightO}>
            {LIGHT.map((l, i) => {
              const g = lightP(i);
              if (g <= 0) return null;
              return <path key={i} d={dOf(W, polyAt(l.pts, g).upto)} fill="none" stroke={color.ink} strokeWidth={2.4} strokeOpacity={0.62} strokeLinejoin="round" />;
            })}
            {LIGHT.map((l, i) => (
              <Flash key={`f${i}`} W={W} p={l.end} t={(f - lightT(i) - 44) / 22} c={l.mid ? EDGE : POCKET} r1={44} />
            ))}
          </g>
        )}

        {/* room: a schematic of the illumination problem */}
        {roomIn > 0 && (
          <g>
            <g clipPath="url(#q7-room)">
              <path d={dOf(RW, ROOM) + "Z"} fill={color.paperShade} opacity={0.5 * roomIn} />
              {glow > 0 && <circle cx={px(RW, LAMP)[0]} cy={px(RW, LAMP)[1]} r={290 * glow} fill="url(#q7-lamp)" />}
            </g>
            {SEAMS.map((s, i) => (
              <path key={i} d={dOf(RW, s)} stroke={color.ink3} strokeWidth={1.6} strokeDasharray="5 6" opacity={seamsIn} />
            ))}
            <path
              d={dOf(RW, [...ROOM, ROOM[0]])}
              fill="none"
              stroke={color.ink}
              strokeWidth={5}
              strokeLinejoin="miter"
              strokeDasharray={roomIn < 1 ? `${roomIn * 14 * RW.u} ${14 * RW.u}` : undefined}
            />
            {glow > 0 && (
              <g opacity={glow}>
                <circle cx={px(RW, LAMP)[0]} cy={px(RW, LAMP)[1]} r={9} fill={color.ink} stroke={color.paper} strokeWidth={2.5} />
                {[0, 1, 2, 3, 4, 5, 6, 7].map((k) => {
                  const a = (k * Math.PI) / 4 + Math.PI / 8;
                  const [x, y] = px(RW, LAMP);
                  return <line key={k} x1={x + 16 * Math.cos(a)} y1={y - 16 * Math.sin(a)} x2={x + 26 * Math.cos(a)} y2={y - 26 * Math.sin(a)} stroke={color.ochre} strokeWidth={2.4} strokeLinecap="round" />;
                })}
              </g>
            )}
            {glow > 0 && <path d={toD(lampLead)} stroke={color.ink3} strokeWidth={1.6} opacity={glow} />}
            {darkIn > 0 && <path d={toD(darkLead)} stroke={color.ink3} strokeWidth={1.6} opacity={darkIn} />}
            {darkIn > 0 && (
              <g opacity={darkIn}>
                <circle cx={px(RW, DARK)[0]} cy={px(RW, DARK)[1]} r={15} fill="none" stroke={color.ink2} strokeWidth={2} strokeDasharray="4 4" />
                <circle cx={px(RW, DARK)[0]} cy={px(RW, DARK)[1]} r={7} fill={color.ink} />
              </g>
            )}
          </g>
        )}
      </Layer>

      <M {...lbl45O} />
      <M {...lbl45K} />
      <M {...lbl90} />

      {/* the kicker hands over to the illumination problem on `room` */}
      <div style={{ opacity: 1 - pf(tRoom, 12) }}>
        <Kicker x={120} y={150} p={p("start", 22)}>
          {T.kicker}
        </Kicker>
      </div>
      <Kicker x={120} y={150} p={pf(tRoom + 6, 22)}>
        {T.problem}
      </Kicker>

      {/* left column: start → tri → fold stack up; equiv and room replace them */}
      <div style={{ opacity: 1 - pf(tEq, 14) }}>
        <Txt x={120} y={228} w={600} size={type.body} lh={1.4} p={p("start", 26, 40)}>
          {T.cut}
        </Txt>
        <Txt x={120} y={386} w={600} size={type.body} c={color.ink} p={pf(tTri + 4, 22)}>
          <span style={{ fontWeight: 600 }}>{T.isoceles}</span>
        </Txt>
        <Txt x={120} y={450} w={640} size={type.caption} c={color.ink2} p={pf(tTri + 30, 22)}>
          {r(T.angles)}
        </Txt>
        <Txt x={120} y={556} w={600} size={type.body} lh={1.4} p={pf(tFold + 4, 22)}>
          {T.foldLine}
        </Txt>
        <Txt x={120} y={690} w={600} size={type.caption} c={color.ink2} p={pf(folded, 22)}>
          {T.holesTo}
        </Txt>
      </div>
      <div style={{ opacity: win(tEq + 4, tRoom) }}>
        <Txt x={120} y={236} w={620} size={56} lh={1.35} p={pf(at("equiv", 0.55), 26)}>
          {r(T.never)}
        </Txt>
        <Txt x={120} y={500} w={600} size={type.caption} c={color.ink2} p={pf(tEq + 10, 22)}>
          {T.equiv}
        </Txt>
        <Txt x={absorb.x} y={absorb.y} w={400} align="right" size={34} c={color.ink2} p={pf(tEq + 20, 20) * (eqOnly ? 1 : 0)}>
          {T.absorb}
        </Txt>
      </div>
      <div style={{ opacity: pf(tRoom + 4, 16) }}>
        <Txt x={120} y={232} w={620} size={type.body} lh={1.4} p={pf(tRoom + 10, 24)}>
          {T.question}
        </Txt>
        <Txt x={120} y={392} w={620} size={type.body} c={color.ink2} p={pf(at("room", 0.2), 24)}>
          {T.who}
        </Txt>
        <Txt x={120} y={476} w={620} size={type.caption} lh={1.45} c={color.ink2} p={pf(at("room", 0.45), 24)}>
          {T.built}
        </Txt>
        <Txt x={tileLbl.x} y={tileLbl.y} w={340} align="center" size={34} c={color.ink3} p={pf(tRoom + 40, 20)}>
          {T.tile}
        </Txt>
        <Txt x={lampLbl.x} y={lampLbl.y} w={120} align="center" size={34} c={color.ink2} p={glow}>
          {T.lamp}
        </Txt>
        <Txt x={darkLbl.x} y={darkLbl.y} w={200} size={34} c={color.ink2} p={darkIn}>
          {T.dark}
        </Txt>
        <Txt x={schem.x} y={schem.y} w={600} align="right" size={34} c={color.ink2} p={roomIn}>
          {T.schematic}
        </Txt>
      </div>
    </Sheet>
  );
};
