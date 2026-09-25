/**
 * The key idea, slowly: the shot that came home (2,1), unfolded one bounce
 * per beat. At each bounce the next copy of the table turns over the wall
 * like a page (the wall glows ochre: the hinge) and the bounced segment
 * becomes the straight continuation. Then the copies tile the plane.
 */
import React from "react";
import { interpolate } from "remotion";
import { color, type } from "../../theme";
import { clamp } from "../../components/Type";
import { EDGE, Flash, HOMEC, Kicker, Layer, Mark, Sheet, Txt, Unfold, World, camPath, dOf, px, pxs, tableMarks, useS, useT } from "../kit";
import { V, polyAt, realPath, shot } from "../geo";

const S = shot([2, 1], 2);
const W: World = { ox: 960, oy: 690, u: 125 };
const smooth = (x: number) => 0.5 - 0.5 * Math.cos(Math.PI * Math.max(0, Math.min(1, x)));

export const Unfolding: React.FC = () => {
  const { f, at, p, guard } = useS();
  const { t, r, tLbl, zh } = useT();
  const T = t.unfold;
  const F1 = at("first");
  const cam = camPath(f, { cx: 960, cy: 690, s: 1.6 }, [[F1, { cx: 960, cy: 540, s: 1 }, 46]]);

  const roll = interpolate(f, [at("start") + 16, at("start") + 16 + 96], [0, 1], clamp);
  const s1 = smooth(interpolate(f, [F1 + 54, F1 + 104], [0, 1], clamp));
  const s2 = smooth(interpolate(f, [at("second") + 4, at("second") + 50], [0, 1], clamp));
  const s3 = smooth(interpolate(f, [at("third") + 4, at("third") + 50], [0, 1], clamp));
  const stage = s1 + s2 + s3;

  const L = at("line");
  const run = interpolate(f, [L + 10, L + 70], [0, 1], { ...clamp, easing: (x) => x });
  const arrive = f - (L + 70);
  const plane = p("plane", 40);
  const rays = p("plane", 40, 40);

  // the ball: rolls the real path at stage 0; later runs the straight line
  let ball: V | null = null;
  if (stage === 0 && roll > 0) ball = polyAt(realPath(S), roll).p;
  if (run > 0) ball = polyAt([[0, 0], [4, 2]], run).p;

  // zh: 「回到中心」 is wider than the copy's half-width: centred above the centre (the line arrives from below-left)
  const homeLbl = zh
    ? { s: T.home, x: px(W, [4, 2])[0], y: px(W, [4, 2])[1] - 74, align: "center" as const, w: 200 }
    : { s: T.home, x: px(W, [4, 2])[0] + 22, y: px(W, [4, 2])[1] + 20, align: "left" as const, w: 200 };
  const realLbl = { s: T.real, x: W.ox, y: W.oy + W.u + 28 };
  const marks: Mark[] = [
    ...tableMarks(W, "real table"),
    ...tableMarks(W, "copy 3", [4, 2], "corners", false, stage >= 3),
    { name: "straight line", pts: pxs(W, [[0, 0], [4, 2]]), w: 4, on: stage >= 3 },
  ];
  guard(marks, [
    tLbl(homeLbl.s, homeLbl.x, homeLbl.y, type.label, interpolate(arrive, [10, 30], [0, 1], clamp), 1, { italic: true, align: homeLbl.align }),
    tLbl(realLbl.s, realLbl.x, realLbl.y, type.label, p("first", 24, 50), 1, { italic: true, align: "center" }),
  ]);

  // the tiled plane: walls on the odd lines
  const gridX = [-5, -3, -1, 1, 3, 5, 7, 9];
  const gridY = [-3, -1, 1, 3, 5];
  const others: V[][] = [
    [
      [0, 0],
      [3.6, 10.8],
    ],
    [
      [0, 0],
      [9, -3.3],
    ],
    [
      [0, 0],
      [-6, 4.4],
    ],
  ];

  const steps: Array<[string, number]> = [
    [T.steps[0], p("first", 22, 54)],
    [T.steps[1], p("second", 22)],
    [T.steps[2], p("third", 22)],
  ];

  return (
    <Sheet folio={10} title={T.title} cam={cam}>
      <Layer>
        <defs>
          <filter id="q7-feather" x="-10%" y="-10%" width="120%" height="120%">
            <feGaussianBlur stdDeviation="40" />
          </filter>
          <mask id="q7-plane" maskUnits="userSpaceOnUse" x="0" y="0" width="1920" height="1080">
            <rect x={760} y={170} width={1120} height={800} fill="#fff" filter="url(#q7-feather)" />
          </mask>
        </defs>
        {plane > 0 && (
          <g mask="url(#q7-plane)" opacity={plane}>
            {gridX.map((x) => (
              <path key={`x${x}`} d={dOf(W, [[x, -6], [x, 8]])} stroke={color.rule} strokeWidth={1.6} />
            ))}
            {gridY.map((y) => (
              <path key={`y${y}`} d={dOf(W, [[-8, y], [12, y]])} stroke={color.rule} strokeWidth={1.6} />
            ))}
            {others.map((o, i) => (
              <path key={i} d={dOf(W, [o[0], polyAt(o, rays).p])} stroke={color.ink3} strokeWidth={2.4} strokeDasharray="10 8" />
            ))}
            <path d={dOf(W, [[4, 2], polyAt([[4, 2], [8, 4]], rays).p])} stroke={color.ink} strokeWidth={4} strokeLinecap="round" />
          </g>
        )}
        <Unfold W={W} s={S} stage={stage} lineFrac={stage === 0 ? roll : 1} ball={ball} />
        {arrive > 0 && <Flash W={W} p={[4, 2]} t={arrive / 28} c={HOMEC} r1={60} />}
        {arrive > 0 && (
          <circle cx={px(W, [4, 2])[0]} cy={px(W, [4, 2])[1]} r={20} fill="none" stroke={HOMEC} strokeWidth={3} opacity={interpolate(arrive, [6, 20], [0, 1], clamp)} />
        )}
      </Layer>
      <Txt x={homeLbl.x} y={homeLbl.y} w={homeLbl.w} align={homeLbl.align} size={type.label} italic c={HOMEC} p={interpolate(arrive, [10, 30], [0, 1], clamp)}>
        {homeLbl.s}
      </Txt>
      <Txt x={realLbl.x} y={realLbl.y} w={320} align="center" size={type.label} italic c={color.ink2} p={p("first", 24, 50)}>
        {realLbl.s}
      </Txt>

      {/* notes column (visible once the camera has pulled back) */}
      <Kicker x={120} y={150} p={p("first", 22, 40)}>
        {T.kicker}
      </Kicker>
      <Txt x={120} y={222} w={480} size={type.body} p={p("first", 26, 44)}>
        {T.easy}
      </Txt>
      <Txt x={120} y={352} w={600} size={type.caption} italic c={color.ink2} p={p("first", 22, 50)}>
        {T.across}
      </Txt>
      {steps.map(([s, q], i) => (
        <div key={s} style={{ position: "absolute", left: 120, top: 408 + i * 56, opacity: q > 0 ? 1 : 0 }}>
          <Txt x={0} y={0} w={60} size={type.caption} c={EDGE} p={q}>
            {`${i + 1}.`}
          </Txt>
          <Txt x={44} y={0} w={420} size={type.caption} p={q}>
            {s}
          </Txt>
        </div>
      ))}
      <Txt x={120} y={600} w={480} size={type.body} p={p("line", 26, 70)}>
        {r(T.line)}
      </Txt>
      <Txt x={120} y={820} w={480} size={type.caption} italic c={color.ink2} p={p("plane", 26, 30)}>
        {T.plane}
      </Txt>
    </Sheet>
  );
};
