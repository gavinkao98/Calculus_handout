/**
 * The exam card. Two stacked pages on one tall sheet:
 *   top    — who set the problem (set like a title page; the fleuron is a
 *            table whose ball keeps coming home);
 *   bottom — the problem statement with a clean redraw of the exam's figures.
 * One camera move (top → bottom) when the narration turns to the statement.
 */
import React from "react";
import { color, type } from "../../theme";
import { Rule } from "../../components/Type";
import { Arrow, Ball, Caps, EDGE, HOMEC, Layer, Mark, Pocket, R_POCKET, Sheet, Table, Txt, World, arcPts, dOf, mLbl, M, px, pxs, tableMarks, useS, useT, wipe, camPath } from "../kit";
import { V, polyAt, realPath, shot } from "../geo";
import { CJK_STACK, useCjkReady } from "../cjk";

/** Chinese setting: Garamond digits (lining) + Noto Serif TC ideographs, tracked a touch */
const zh = (size: number, c: string, track: number): React.CSSProperties => ({
  fontFamily: CJK_STACK,
  fontSize: size,
  fontWeight: 400,
  color: c,
  letterSpacing: `${track}em`,
  fontFeatureSettings: "'kern' 1, 'lnum' 1",
  whiteSpace: "nowrap",
});

const HOMESHOT = shot([2, 1], 2); // the (2, 1) shot: centre → (1,½) → (0,1) → (−1,½) → centre
const HOMEPATH = realPath(HOMESHOT);

const TH = (30 * Math.PI) / 180;
const PATH1 = realPath(shot([Math.cos(TH), Math.sin(TH)], 3.35)); // a shot that bounces twice
const PATH2 = realPath(shot([1, 3], 1)); // one bounce off the top, into the bottom-right corner

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
  const { t, r } = useT();
  const T = t.exam;
  const C = T.card;
  const cjk = useCjkReady();
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
    <Sheet folio={7} title={T.title} h={2160} cam={cam} head={false}>
      {/* ═════ top page: the exam (set in Chinese, as the original) ═════ */}
      {cjk && (
        <>
          <div style={{ position: "absolute", left: 120, top: 104, ...zh(34, color.ink2, 0.24), ...wipe(pf(4, 22), 0) }}>{C.kicker}</div>
          <div style={{ position: "absolute", left: 124, top: 214, ...zh(36, color.accent, 0.3), ...wipe(pf(10, 22), 0) }}>{C.numLabel}</div>
        </>
      )}
      <Rule x={120} y={150} w={1680} from={2} len={30} />

      <Txt x={96} y={236} w={500} size={type.display} lh={1} p={pf(12, 30)} style={{ letterSpacing: "-0.02em", fontFeatureSettings: "'lnum' 1, 'kern' 1" }}>
        7
      </Txt>
      <Layer>
        <Table W={FW} real draw={tableIn} />
        {tableIn >= 1 && <PathLap W={FW} lap={lap} />}
      </Layer>

      <Rule x={620} y={236} w={660} vertical from={14} len={36} />

      {cjk && (
        <>
          <div style={{ position: "absolute", left: 690, top: 222, ...zh(36, color.accent, 0.3), ...wipe(pf(16, 22), 0) }}>{C.school}</div>
          <div style={{ position: "absolute", left: 690, top: 280, ...zh(86, color.ink, 0.04), fontWeight: 500, lineHeight: 1.28, ...wipe(pf(20, 32), 0) }}>
            {C.title1}
            <br />
            {C.title2}
          </div>
          <div style={{ position: "absolute", left: 692, top: 516, width: 90 * pf(40, 20), height: 3, background: color.accent }} />
          <div style={{ position: "absolute", left: 690, top: 540, ...zh(46, color.ink2, 0.08), ...wipe(pf(44, 26), 0) }}>{C.subtitle}</div>
          {C.rows.map(([k, v], i) => (
            <div
              key={k}
              style={{
                position: "absolute",
                left: 690,
                top: 660 + i * 68,
                width: 1110,
                display: "flex",
                alignItems: "baseline",
                ...zh(42, color.ink, 0.06),
                ...wipe(pf(56 + i * 8, 22)),
              }}
            >
              <span>{k}</span>
              <span style={{ flex: 1, borderBottom: `2.5px dotted ${color.rule}`, margin: "0 22px", translate: "0 -9px" }} />
              {/* a full-width ） carries half an em of air on its right: hang it so the column ends flush with "115" */}
              <span style={{ color: i === 2 ? color.accent : color.ink, letterSpacing: 0, marginRight: v.endsWith("）") ? "-0.36em" : 0 }}>{v}</span>
            </div>
          ))}
        </>
      )}
      <Rule x={120} y={930} w={1680} from={70} len={30} />

      {/* ═════ bottom page: the problem ═════ */}
      <div style={{ position: "absolute", left: 120, top: 1160, ...wipe(p("setup", 22, 30), 0) }}>
        <div style={{ width: 56, height: 2.5, background: color.accent, marginBottom: 14 }} />
        <Caps color={color.accent}>{T.kicker}</Caps>
      </div>
      {/* the English page is a translation: say so where it is true, set as a footnote (the zh page is the original) */}
      {T.footnote && (
        <>
          <Rule x={120} y={2016} w={180} from={at("setup") + 40} len={20} />
          <Txt x={120} y={2028} w={900} size={32} italic c={color.ink3} p={p("setup", 44, 30)}>
            {T.footnote}
          </Txt>
        </>
      )}
      {para(1230, p("setup", 60, 40), r(T.setup))}
      {para(1466, th, r(T.theta))}
      {para(1590, pa, r(T.parta), T.labelA)}
      {para(1790, pb, r(T.partb), T.labelB)}

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
        {/* legend marks (the zh page words it as the exam does, in one caption line instead) */}
        {T.legendStart && (
          <g opacity={fig}>
            <circle cx={1330} cy={1590} r={8} fill={HOMEC} />
            <Pocket W={{ ox: 0, oy: 0, u: 1 }} p={[1560, -1590]} />
          </g>
        )}
        {fig3 > 0 && (
          <g opacity={fig3}>
            <Pocket W={{ ox: 0, oy: 0, u: 1 }} p={[1318, -1956]} c={EDGE} />
          </g>
        )}
      </Layer>
      <M {...thLbl} />
      <Txt x={W1.ox} y={1516} w={320} align="center" size={30} italic c={color.ink2} p={fig}>
        {T.figPath}
      </Txt>
      <Txt x={W2.ox} y={1516} w={320} align="center" size={30} italic c={color.ink2} p={fig}>
        {T.figEnd}
      </Txt>
      {T.legendStart && (
        <>
          <Txt x={1348} y={1570} w={240} size={30} italic c={color.ink2} p={fig}>
            {T.legendStart}
          </Txt>
          <Txt x={1560 + R_POCKET + 12} y={1570} w={240} size={30} italic c={color.ink2} p={fig}>
            {T.legendPocket}
          </Txt>
        </>
      )}
      {T.figNote && (
        // an opening full-width 「（」 carries half an em of air on its left: hang it so the ideographs align at the figure's edge
        <Txt
          x={W1.ox - 128}
          y={1572}
          w={W2.ox + 128 - (W1.ox - 128)}
          size={30}
          lh={1.35}
          c={color.ink2}
          p={fig}
          style={T.figNote.startsWith("（") ? { textIndent: "-0.5em" } : undefined}
        >
          {r(T.figNote)}
        </Txt>
      )}
      <Txt x={1318 + R_POCKET + 12} y={1936} w={400} size={30} italic c={color.ink2} p={fig3}>
        {T.fig3}
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
