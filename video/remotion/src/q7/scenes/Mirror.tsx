/**
 * Why a bounce is a mirror: equal angles at the wall, so the bounced segment
 * is the mirror image of the straight continuation. The segment turns over
 * the wall like a page and lands on the dashed line.
 */
import React from "react";
import { interpolate } from "remotion";
import { color, type } from "../../theme";
import { clamp } from "../../components/Type";
import { EDGE, Kicker, Layer, Ln, Mark, Pt, Sheet, Txt, arcPts, mLbl, M, useS, useT } from "../kit";

const H: Pt = [1120, 560];
const A: Pt = [700, 820];
const B: Pt = [700, 300];
const C: Pt = [1540, 300];
const WALL = { x: 1120, y0: 200, y1: 900 };

const lerp = (a: Pt, b: Pt, t: number): Pt => [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t];

export const Mirror: React.FC = () => {
  const { f, at, p, guard } = useS();
  const { t, r, tLbl } = useT();
  const T = t.mirror;
  const wall = p("start", 26);
  const inc = p("start", 34, 12);
  const refl = p("equal", 30);
  const ang = p("equal", 24, 26);
  const cont = p("image", 30);
  // the page-turn: starts once the dashed continuation is down
  const tf = interpolate(f, [at("image") + 40, at("image") + 90], [0, 1], { ...clamp, easing: (x) => 0.5 - 0.5 * Math.cos(Math.PI * x) });
  const sigma = Math.cos(Math.PI * tf); // 1 = where it bounced, −1 = mirrored across the wall
  const mapX = (x: number) => WALL.x + (x - WALL.x) * sigma;
  const landed = interpolate(f, [at("image") + 90, at("image") + 104], [0, 1], clamp);
  const note = p("image", 26, 100);

  const ballAt: Pt | null = inc < 1 ? lerp(A, H, inc) : refl < 1 ? lerp(H, B, refl) : null;

  const aDir = Math.atan2(-(A[1] - H[1]), A[0] - H[0]); // paper angles (y up)
  const bDir = Math.atan2(-(B[1] - H[1]), B[0] - H[0]);
  const R = 74;
  const mid1 = (-Math.PI / 2 + aDir) / 2;
  const mid2 = (Math.PI / 2 + bDir) / 2;
  const lab1 = { x: H[0] + 116 * Math.cos(mid1), y: H[1] - 116 * Math.sin(mid1) + 14, t: "\\alpha", size: 44, c: color.ochre, align: "center" as const, p: ang };
  const lab2 = { x: H[0] + 116 * Math.cos(mid2), y: H[1] - 116 * Math.sin(mid2) + 14, t: "\\alpha", size: 44, c: color.ochre, align: "center" as const, p: ang };

  const marks: Mark[] = [
    { name: "wall", pts: [[WALL.x, WALL.y0], [WALL.x, WALL.y1]], w: 6, on: wall > 0 },
    { name: "incoming", pts: [A, H], w: 4, on: inc >= 1 },
    { name: "bounced", pts: [H, B], w: 4, on: refl >= 1 },
    { name: "continuation", pts: [H, C], w: 3, on: cont > 0 },
    { name: "arc in", pts: arcPts(H[0], H[1], R, -Math.PI / 2, aDir, 16), w: 3, on: ang > 0 },
    { name: "arc out", pts: arcPts(H[0], H[1], R, bDir, Math.PI / 2, 16), w: 3, on: ang > 0 },
  ];
  guard(marks, [mLbl(lab1, "α in"), mLbl(lab2, "α out"), tLbl(T.beyond, 1160, 760, type.caption, wall, 1, { italic: true })]);

  return (
    <Sheet folio={9} title={T.title}>
      <Layer>
        {/* beyond the wall */}
        <rect x={WALL.x} y={WALL.y0} width={560 * wall} height={WALL.y1 - WALL.y0} fill={color.paperShade} opacity={0.7} />
        <Ln x1={WALL.x} y1={WALL.y0} x2={WALL.x} y2={WALL.y1} p={wall} c={color.ink} w={6} />
        {/* equal angles */}
        {ang > 0 && (
          <g opacity={ang}>
            <path d={toArc(H, R, -Math.PI / 2, aDir)} fill="none" stroke={color.ochre} strokeWidth={3} />
            <path d={toArc(H, R, bDir, Math.PI / 2)} fill="none" stroke={color.ochre} strokeWidth={3} />
          </g>
        )}
        {/* the straight continuation */}
        <Ln x1={H[0]} y1={H[1]} x2={C[0]} y2={C[1]} p={cont} c={color.ink3} w={3} dash="10 9" />
        {/* incoming + bounced */}
        <Ln x1={A[0]} y1={A[1]} x2={H[0]} y2={H[1]} p={inc} c={color.ink} w={4} />
        {refl > 0 && <Ln x1={H[0]} y1={H[1]} x2={B[0]} y2={B[1]} p={refl} c={color.ink} w={4} />}
        {/* the bounced segment turning over the wall */}
        {tf > 0 && (
          <>
            <line x1={H[0]} y1={H[1]} x2={mapX(B[0])} y2={B[1]} stroke={EDGE} strokeWidth={4.5 + 1.5 * (1 - landed)} strokeLinecap="round" />
          </>
        )}
        {ballAt && <circle cx={ballAt[0]} cy={ballAt[1]} r={11} fill={color.ink} stroke={color.paper} strokeWidth={3} />}
        <circle cx={H[0]} cy={H[1]} r={6} fill={color.ink} opacity={inc >= 1 ? 1 : 0} />
      </Layer>
      <M {...lab1} />
      <M {...lab2} />
      <Txt x={1160} y={760} w={420} size={type.caption} italic c={color.ink3} p={wall}>
        {T.beyond}
      </Txt>

      <Kicker x={120} y={150} p={p("start", 22)}>
        {T.kicker}
      </Kicker>
      <Txt x={120} y={230} w={500} size={type.body} p={ang}>
        {r(T.law)}
      </Txt>
      <Txt x={120} y={330} w={500} size={type.body} p={cont}>
        {r(T.image)}
      </Txt>
      <Txt x={120} y={520} w={500} size={type.caption} italic c={color.ink2} p={note}>
        {T.note}
      </Txt>
    </Sheet>
  );
};

const toArc = (c: Pt, r: number, a0: number, a1: number) => {
  const pts = arcPts(c[0], c[1], r, a0, a1, 24);
  return pts.map(([x, y], i) => `${i ? "L" : "M"}${x.toFixed(1)} ${y.toFixed(1)}`).join("");
};
