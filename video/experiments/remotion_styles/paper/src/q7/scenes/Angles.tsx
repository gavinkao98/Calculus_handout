/**
 * Back to θ: tan θ = q/p with p, q coprime and of opposite parity. The family
 * (1, 2k) gives slopes 2k — a fan of shots from the centre, each a different
 * angle — infinitely many. Irrational slopes: never a lattice point.
 */
import React from "react";
import { interpolate, spring } from "remotion";
import { color, type } from "../../theme";
import { clamp } from "../../components/Type";
import { HOMEC, Kicker, Layer, M, Mark, Sheet, Table, Txt, World, arcPts, mLbl, px, tableMarks, useS } from "../kit";
import { V } from "../geo";

const W: World = { ox: 1330, oy: 560, u: 330 };
const KS = [0, 1, -1, 2, -2, 3, -3, 4, -4, 6, -6, 9, -9];
/** where the ray from the centre in direction d meets the table's edge */
const edge = (d: V): V => {
  const t = 1 / Math.max(Math.abs(d[0]), Math.abs(d[1]));
  return [d[0] * t, d[1] * t];
};

export const Angles: React.FC = () => {
  const { f, fps, at, p, pf, atWord, guard } = useS();
  // "When p is not zero, tangent theta is q over p. And p equal to zero is the straight up-and-down shot."
  const tTan = atWord("When p is not zero", { afterFrame: at("start") }) ?? at("start", 0.5);
  const tVert = atWord("And p equal to zero", { afterFrame: at("start") }) ?? at("start", 0.76);
  const tbl = p("start", 30);
  const first = p("start", 30, 30);
  const fam = at("family");
  const th = Math.atan(2);
  const arcR = 0.3;
  const thLbl = { x: px(W, [0, 0])[0] + 0.46 * W.u * Math.cos(th / 2), y: px(W, [0, 0])[1] - 0.46 * W.u * Math.sin(th / 2) + 14, align: "center" as const, t: "\\theta", size: 44, c: color.ochre, p: p("start", 24, 50) };
  const O = px(W, [0, 0]);
  const marks: Mark[] = [
    ...tableMarks(W, "table"),
    { name: "ray k=1", pts: [O, px(W, edge([1, 2]))], w: 3.4, on: first > 0 },
    { name: "reference", pts: [O, px(W, [1, 0])], w: 1.8, on: first > 0 },
    { name: "θ arc", pts: arcPts(O[0], O[1], arcR * W.u, 0, th, 20), w: 3, on: first > 0 },
  ];
  guard(marks, [mLbl(thLbl, "θ")]);

  const list: Array<[string, string]> = [
    ["k=0", "\\tan\\theta=0"],
    ["k=1", "\\tan\\theta=2"],
    ["k=2", "\\tan\\theta=4"],
    ["k=3", "\\tan\\theta=6"],
  ];
  return (
    <Sheet folio={14} title="Back to the angle">
      <Layer>
        <Table W={W} real draw={tbl} />
        {/* the fan: (1, 2k) and (−1, −2k) */}
        {KS.map((k, i) => {
          const g = k === 1 ? first : spring({ frame: f - fam - 30 - i * 7, fps, config: { damping: 18, stiffness: 120 } });
          if (g <= 0.001) return null;
          return [1, -1].map((s) => {
            const e = edge([s, 2 * k * s]);
            const q = px(W, [e[0] * Math.min(1, g), e[1] * Math.min(1, g)]);
            return <line key={`${k}${s}`} x1={O[0]} y1={O[1]} x2={q[0]} y2={q[1]} stroke={color.ink} strokeWidth={k === 1 && s === 1 ? 3.4 : 2.4} strokeLinecap="round" opacity={k === 1 && s === 1 ? 1 : 0.8} />;
          });
        })}
        {first > 0 && (
          <g opacity={first}>
            <line x1={O[0]} y1={O[1]} x2={px(W, [1, 0])[0]} y2={O[1]} stroke={color.ink2} strokeWidth={1.8} />
            <path
              d={arcPts(O[0], O[1], arcR * W.u, 0, th, 30)
                .map(([x, y], i) => `${i ? "L" : "M"}${x.toFixed(1)} ${y.toFixed(1)}`)
                .join("")}
              fill="none"
              stroke={color.ochre}
              strokeWidth={3}
            />
          </g>
        )}
        {/* vertical (0, 1) */}
        <line x1={O[0]} y1={px(W, [0, 1])[1]} x2={O[0]} y2={px(W, [0, -1])[1]} stroke={HOMEC} strokeWidth={2.4} strokeDasharray="8 8" opacity={pf(tVert, 20)} />
        <circle cx={O[0]} cy={O[1]} r={9} fill={HOMEC} />
      </Layer>
      <M {...thLbl} />

      <Kicker x={120} y={150} p={p("start", 22)}>
        Back to the angle
      </Kicker>
      <M x={120} y={296} t="\text{direction}\ \ (p,\,q)" size={64} p={p("start", 26, 10)} />
      <Txt x={120} y={316} w={700} size={type.caption} italic c={color.ink2} p={p("start", 24, 40)}>
        no common factor; one odd, one even
      </Txt>
      <M x={120} y={452} t="\tan\theta=q/p\quad(p\neq0)" size={60} p={pf(tTan, 26)} />

      <M x={120} y={540} t="(p,q)=(1,\,2k)" size={60} p={p("family", 26)} />
      {list.map(([k, t], i) => {
        const q = interpolate(f, [fam + 30 + i * 14, fam + 50 + i * 14], [0, 1], clamp);
        return (
          <React.Fragment key={k}>
            <M x={120} y={620 + i * 58} t={k} size={40} c={color.ink2} p={q} />
            <M x={300} y={620 + i * 58} t={t} size={40} p={q} />
          </React.Fragment>
        );
      })}
      <M x={300} y={620 + 4 * 58 - 16} t="\vdots" size={40} c={color.ink2} p={interpolate(f, [fam + 100, fam + 120], [0, 1], clamp)} />
      <div
        style={{
          position: "absolute",
          left: 110,
          top: 890,
          padding: "10px 18px",
          border: `2.5px solid ${HOMEC}`,
          opacity: p("family", 20, 150),
        }}
      >
        <Txt x={0} y={0} w={660} size={type.body} c={HOMEC} p={p("family", 24, 150)} style={{ position: "relative" }}>
          Infinitely many angles. (a) is proved.
        </Txt>
      </div>
      <Txt x={1330} y={930} w={760} align="center" size={type.caption} italic c={color.ink2} p={p("irrational", 26)}>
        An irrational slope never meets another lattice point: never pocketed, never home.
      </Txt>
      <Txt x={O[0] + 16} y={px(W, [0, 1])[1] - 58} w={300} size={30} italic c={HOMEC} p={pf(tVert + 10, 20)}>
        (0, 1) works too
      </Txt>
    </Sheet>
  );
};
