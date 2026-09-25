/**
 * The exam card. Two stacked pages on one tall sheet:
 *   top    — who set the problem (set like a title page; the fleuron is a
 *            table whose ball keeps coming home);
 *   bottom — the problem statement with a clean redraw of the exam's figures.
 * One camera move (top → bottom) when the narration turns to the statement.
 */
import React from "react";
import { color, font, type } from "../../theme";
import { Rule, SmallCaps } from "../../components/Type";
import { Arrow, Ball, EDGE, HOMEC, Layer, Mark, Pocket, R_POCKET, Sheet, Table, Txt, World, arcPts, dOf, mLbl, M, px, pxs, tableMarks, useS, wipe, camPath } from "../kit";
import { V, polyAt, realPath, shot } from "../geo";

const HOMESHOT = shot([2, 1], 2); // the (2, 1) shot: centre → (1,½) → (0,1) → (−1,½) → centre
const HOMEPATH = realPath(HOMESHOT);

const TH = (30 * Math.PI) / 180;
const PATH1 = realPath(shot([Math.cos(TH), Math.sin(TH)], 3.35)); // a shot that bounces twice
const PATH2 = realPath(shot([1, 3], 1)); // one bounce off the top, into the bottom-right corner

const details: Array<[string, string]> = [
  ["Academic year", "115"],
  ["Held", "September 6, 2026"],
  ["Problem", "7 of 7"],
];

const DashedArrowPath: React.FC<{ W: World; pts: V[]; p: number }> = ({ W, pts, p }) => {
  if (p <= 0) return null;
  const { upto } = polyAt(pts, p);
  const P = pxs(W, upto);
  const a = P[P.length - 2];
  const b = P[P.length - 1];
  return (
    <g>
      <path d={dOf(W, upto)} fill="none" stroke={color.ink} strokeWidth={2.6} strokeDasharray="10 5 2 5" strokeLinecap="round" strokeLinejoin="round" />
      {p >= 1 && <Arrow x1={a[0] + (b[0] - a[0]) * 0.8} y1={a[1] + (b[1] - a[1]) * 0.8} x2={b[0]} y2={b[1]} c={color.ink} w={2.6} head={14} />}
    </g>
  );
};

export const Exam: React.FC = () => {
  const { f, at, p, pf, guard } = useS();
  const S = at("setup");
  const cam = camPath(f, { cx: 960, cy: 540, s: 1 }, [[S - 6, { cx: 960, cy: 1620, s: 1 }, 54]]);

  // ── top page: the fleuron table, its ball forever coming home ──
  const FW: World = { ox: 330, oy: 770, u: 104 };
  const loop = 150;
  const lf = ((f - 30) % loop + loop) % loop;
  const lap = f < 30 ? 0 : Math.min(1, lf / (loop - 30));
  const tableIn = pf(10, 40);

  // ── bottom page figures ──
  const W1: World = { ox: 1318, oy: 1370, u: 128 };
  const W2: World = { ox: 1662, oy: 1370, u: 128 };
  const W3: World = { ox: 1490, oy: 1806, u: 104 };
  const fig = p("setup", 36, 20);
  const path1 = p("setup", 60, 50);
  const path2 = p("setup", 50, 90);
  const th = p("theta", 26);
  const pa = p("parta", 30);
  const pb = p("partb", 30);
  const fig3 = p("partb", 36, 10);

  // θ at the start of figure 1: reference ray along the bottom-edge direction, arc, label in the wedge
  const O1 = px(W1, [0, 0]);
  const arcR = 52;
  const thLbl = { x: O1[0] + 86, y: O1[1] - 6, t: "\\theta", size: 36, c: color.ochre, p: th };

  const marks: Mark[] = [
    ...tableMarks(W1, "figure 1", [0, 0], "corners", true, fig > 0),
    { name: "figure 1 path", pts: pxs(W1, PATH1), w: 2.6, on: path1 > 0 },
    { name: "θ reference", pts: [O1, [O1[0] + 68, O1[1]]], w: 1.8, on: th > 0 },
    { name: "θ arc", pts: arcPts(O1[0], O1[1], arcR, 0, TH, 20), w: 2.4, on: th > 0 },
  ];
  guard(marks, [mLbl(thLbl, "θ")]);

  const para = (y: number, prog: number, children: React.ReactNode, label?: string, o = 1) => (
    <>
      {label && (
        <Txt x={120} y={y} w={70} size={40} italic c={color.accent} p={prog} o={o}>
          {label}
        </Txt>
      )}
      <Txt x={label ? 186 : 120} y={y} w={label ? 974 : 1040} size={40} lh={1.4} p={prog} o={o}>
        {children}
      </Txt>
    </>
  );

  return (
    <Sheet folio={7} title="Problem 7" h={2160} cam={cam} head={false}>
      {/* ═════ top page: the exam ═════ */}
      <div style={{ position: "absolute", left: 120, top: 112, ...wipe(pf(4, 22), 0) }}>
        <SmallCaps>Entrance Exam · Mathematics</SmallCaps>
      </div>
      <div style={{ position: "absolute", right: 120, top: 112, ...wipe(pf(8, 22), 0) }}>
        <SmallCaps>Translated from the Chinese</SmallCaps>
      </div>
      <Rule x={120} y={150} w={1680} from={2} len={30} />

      <div style={{ position: "absolute", left: 124, top: 222, ...wipe(pf(10, 22), 0) }}>
        <SmallCaps color={color.accent}>Problem</SmallCaps>
      </div>
      <Txt x={96} y={236} w={500} size={type.display} lh={1} p={pf(12, 30)} style={{ letterSpacing: "-0.02em", fontFeatureSettings: "'lnum' 1, 'kern' 1" }}>
        7
      </Txt>
      <Layer>
        <Table W={FW} real draw={tableIn} />
        {tableIn >= 1 && <PathLap W={FW} lap={lap} />}
      </Layer>

      <Rule x={620} y={236} w={660} vertical from={14} len={36} />

      <div style={{ position: "absolute", left: 690, top: 232, ...wipe(pf(16, 22), 0) }}>
        <SmallCaps color={color.accent}>National Taiwan University</SmallCaps>
      </div>
      <Txt x={690} y={278} w={1130} size={84} weight={500} lh={1.06} p={pf(20, 32)} style={{ letterSpacing: "-0.01em" }}>
        Northern Taiwan High School
        <br />
        Science Talent Program
      </Txt>
      <div style={{ position: "absolute", left: 692, top: 480, width: 90 * pf(40, 20), height: 3, background: color.accent }} />
      <Txt x={690} y={502} w={1130} size={50} italic c={color.ink2} p={pf(44, 26)}>
        Mathematics · 2026 Entrance Exam
      </Txt>
      {details.map(([k, v], i) => (
        <div
          key={k}
          style={{
            position: "absolute",
            left: 690,
            top: 624 + i * 62,
            width: 1110,
            display: "flex",
            alignItems: "baseline",
            fontFamily: font.serif,
            fontSize: 40,
            color: color.ink,
            fontFeatureSettings: "'kern' 1, 'lnum' 1",
            ...wipe(pf(56 + i * 8, 22)),
          }}
        >
          <span>{k}</span>
          <span style={{ flex: 1, borderBottom: `2.5px dotted ${color.rule}`, margin: "0 18px", translate: "0 -9px" }} />
          <span style={{ color: i === 2 ? color.accent : color.ink }}>{v}</span>
        </div>
      ))}
      <Rule x={120} y={930} w={1680} from={70} len={30} />
      <Txt x={120} y={950} w={1300} size={30} italic c={color.ink3} p={pf(80, 26)}>
        Academic year 115 of the Minguo calendar is the 2026–27 school year; the exam was held on September 6, 2026.
      </Txt>

      {/* ═════ bottom page: the problem ═════ */}
      <div style={{ position: "absolute", left: 120, top: 1160, ...wipe(p("setup", 22, 30), 0) }}>
        <div style={{ width: 56, height: 2.5, background: color.accent, marginBottom: 14 }} />
        <SmallCaps color={color.accent}>Problem 7 · Square billiards</SmallCaps>
      </div>
      {para(
        1230,
        p("setup", 60, 40),
        <>
          A square billiard table has a pocket at each of its four corners. A ball, treated as a point, is placed at the exact center of the table and
          struck. It travels in a straight line and bounces off the edges by the law of reflection; once it falls into a pocket, the motion ends.
        </>,
      )}
      {para(
        1466,
        th,
        <>
          Let <i style={{ color: color.ochre }}>θ</i> be the angle between the shot direction and the bottom edge.
        </>,
      )}
      {para(
        1590,
        pa,
        <>
          Our goal: after the shot, the ball returns to the center of the table before falling into any pocket. Prove that infinitely many angles{" "}
          <i>θ</i> ∈ [0, 2<i>π</i>) achieve this.
        </>,
        "(a)",
      )}
      {para(
        1790,
        pb,
        <>
          Now the table also has a pocket at the midpoint of each edge. How many angles satisfy the requirement in (a)? Explain.
        </>,
        "(b)",
      )}

      <Layer h={2160}>
        {/* figure 1: the ball's path, with θ */}
        <Table W={W1} real draw={fig} />
        {fig >= 1 && <DashedArrowPath W={W1} pts={PATH1} p={path1} />}
        {th > 0 && (
          <g opacity={th}>
            <line x1={O1[0]} y1={O1[1]} x2={O1[0] + 68} y2={O1[1]} stroke={color.ink2} strokeWidth={1.8} />
            <path d={`M${O1[0] + arcR} ${O1[1]} A${arcR} ${arcR} 0 0 0 ${O1[0] + arcR * Math.cos(TH)} ${O1[1] - arcR * Math.sin(TH)}`} fill="none" stroke={color.ochre} strokeWidth={2.4} />
          </g>
        )}
        {/* figure 2: into a pocket */}
        <Table W={W2} real draw={fig} />
        {fig >= 1 && <DashedArrowPath W={W2} pts={PATH2} p={path2} />}
        {/* figure 3: the table in (b) */}
        <g opacity={fig3}>
          <Table W={W3} real pockets="all" draw={fig3} />
        </g>
        {/* legend marks */}
        <g opacity={fig}>
          <circle cx={1330} cy={1590} r={8} fill={HOMEC} />
          <Pocket W={{ ox: 0, oy: 0, u: 1 }} p={[1560, -1590]} />
        </g>
        {fig3 > 0 && (
          <g opacity={fig3}>
            <Pocket W={{ ox: 0, oy: 0, u: 1 }} p={[1318, -1956]} c={EDGE} />
          </g>
        )}
      </Layer>
      <M {...thLbl} />
      <Txt x={W1.ox} y={1516} w={320} align="center" size={30} italic c={color.ink2} p={fig}>
        the ball’s path
      </Txt>
      <Txt x={W2.ox} y={1516} w={320} align="center" size={30} italic c={color.ink2} p={fig}>
        into a pocket: the end
      </Txt>
      <Txt x={1348} y={1570} w={240} size={30} italic c={color.ink2} p={fig}>
        start (center)
      </Txt>
      <Txt x={1560 + R_POCKET + 12} y={1570} w={240} size={30} italic c={color.ink2} p={fig}>
        pocket
      </Txt>
      <Txt x={1318 + R_POCKET + 12} y={1936} w={400} size={30} italic c={color.ink2} p={fig3}>
        the table in (b): eight pockets
      </Txt>
    </Sheet>
  );
};

/** the fleuron's ball: one lap of the (2,1) path, then it rests a beat at home */
const PathLap: React.FC<{ W: World; lap: number }> = ({ W, lap }) => {
  const { p, upto } = polyAt(HOMEPATH, lap);
  return (
    <g>
      <path d={dOf(W, HOMEPATH)} fill="none" stroke={color.rule} strokeWidth={2.2} strokeDasharray="2 7" strokeLinecap="round" />
      <path d={dOf(W, upto)} fill="none" stroke={color.ink} strokeWidth={3} strokeLinecap="round" strokeLinejoin="round" opacity={0.9} />
      <Ball W={W} p={p} r={9} />
      {lap >= 1 && <circle cx={px(W, [0, 0])[0]} cy={px(W, [0, 0])[1]} r={20} fill="none" stroke={HOMEC} strokeWidth={2.5} opacity={0.8} />}
    </g>
  );
};
