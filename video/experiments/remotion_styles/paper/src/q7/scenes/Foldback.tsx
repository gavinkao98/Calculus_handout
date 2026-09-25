/**
 * Fold back to the real table, with a bounce counter. (1,0): the straight
 * line to (2,0) folds once — one bounce off the right wall, home. (2,1): the
 * line to (4,2) folds three times — three bounces; it is the hook's shot 4.
 * Then the count: the line crosses |p| vertical and |q| horizontal walls.
 */
import React from "react";
import { interpolate, spring } from "remotion";
import { color, features, font, type } from "../../theme";
import { SmallCaps, clamp } from "../../components/Type";
import { Ball, EDGE, Flash, HOMEC, Kicker, Layer, M, Sheet, Txt, Unfold, World, dOf, px, useS } from "../kit";
import { V, polyAt, polyLen, realPath, shot } from "../geo";

const W: World = { ox: 980, oy: 700, u: 140 };
const A = shot([1, 0], 2); // → (2, 0)
const B = shot([2, 1], 2); // → (4, 2)
const PA = realPath(A);
const PB = realPath(B);
const ease = (x: number) => 0.5 - 0.5 * Math.cos(Math.PI * Math.max(0, Math.min(1, x)));

export const Foldback: React.FC = () => {
  const { f, fps, at, p } = useS();
  const tF1 = at("fold1");
  const tN = at("next");
  const tF2 = at("fold2");
  const tC = at("count");

  // ── (1, 0) ──
  const aIn = p("start", 30, 10);
  const aFold = ease(interpolate(f, [tF1 + 6, tF1 + 56], [0, 1], clamp));
  const aRun = interpolate(f, [tF1 + 64, tF1 + 64 + (polyLen(PA) / 0.05)], [0, 1], clamp);
  const aHome = f - (tF1 + 64 + polyLen(PA) / 0.05);
  const aO = interpolate(f, [tN, tN + 16], [1, 0], clamp);

  // ── (2, 1) ──
  const bIn = interpolate(f, [tN + 14, tN + 50], [0, 1], clamp);
  const folds = [0, 1, 2].map((i) => ease(interpolate(f, [tF2 + 4 + i * 50, tF2 + 44 + i * 50], [0, 1], clamp)));
  const reunfold = ease(interpolate(f, [tC + 4, tC + 64], [0, 1], clamp));
  const bStage = 3 - folds[0] - folds[1] - folds[2] + 3 * reunfold;
  const bRunFrom = tF2 + 4 + 150 + 6;
  const bRun = interpolate(f, [bRunFrom, bRunFrom + polyLen(PB) / 0.07], [0, 1], clamp);
  const bHome = f - (bRunFrom + polyLen(PB) / 0.07);
  const bO = bIn * interpolate(f, [tC, tC + 4], [1, 1], clamp);

  const count = f < tN ? (aFold >= 1 ? 1 : 0) : Math.round(folds.reduce((s, x) => s + (x >= 1 ? 1 : 0), 0));
  const lastTick = f < tN ? tF1 + 56 : [0, 1, 2].map((i) => tF2 + 44 + i * 50).filter((t) => f >= t).pop() ?? -999;
  const popK = spring({ frame: f - lastTick, fps, config: { damping: 12, stiffness: 200, mass: 0.6 } });

  const which = f < tN ? "a" : "b";
  const wallsO = interpolate(f, [tC + 60, tC + 80], [0, 1], clamp);

  const mark = (v: V, o: number) => (
    <circle cx={px(W, v)[0]} cy={px(W, v)[1]} r={16} fill="none" stroke={EDGE} strokeWidth={3.5} opacity={o} />
  );

  return (
    <Sheet folio={13} title="Fold it back">
      <Layer>
        {/* (1, 0) */}
        {aO > 0 && aIn > 0 && (
          <g opacity={aO}>
            <Unfold W={W} s={A} stage={1 - aFold} lineFrac={aIn} copiesO={1} />
            {aFold < 0.02 && aIn >= 1 && mark([1, 0], 1)}
            {aRun > 0 && <Ball W={W} p={polyAt(PA, aRun).p} />}
            <Flash W={W} p={[0, 0]} t={aHome / 26} c={HOMEC} r1={54} />
            {aHome > 0 && <circle cx={W.ox} cy={W.oy} r={21} fill="none" stroke={HOMEC} strokeWidth={3} />}
          </g>
        )}
        {/* (2, 1) */}
        {bIn > 0 && (
          <g opacity={bO}>
            <Unfold W={W} s={B} stage={bStage} lineFrac={f < tF2 ? bIn : 1} />
            {folds[0] < 0.02 && bIn >= 1 && mark([2, 1], 1)}
            {reunfold >= 1 && mark([2, 1], wallsO)}
            {wallsO > 0 && (
              <g opacity={wallsO}>
                {[
                  [
                    [1, -1],
                    [1, 1],
                  ],
                  [
                    [3, 1],
                    [3, 3],
                  ],
                  [
                    [1, 1],
                    [3, 1],
                  ],
                ].map((seg, i) => (
                  <path key={i} d={dOf(W, seg as V[])} stroke={EDGE} strokeWidth={7} strokeLinecap="round" opacity={0.85} />
                ))}
                <path d={dOf(W, [[0, 0], [4, 2]])} stroke={color.ink} strokeWidth={4} strokeLinecap="round" />
              </g>
            )}
            {bRun > 0 && reunfold <= 0 && <Ball W={W} p={polyAt(PB, bRun).p} />}
            {reunfold <= 0 && <Flash W={W} p={[0, 0]} t={bHome / 26} c={HOMEC} r1={54} />}
            {bHome > 0 && reunfold <= 0 && <circle cx={W.ox} cy={W.oy} r={21} fill="none" stroke={HOMEC} strokeWidth={3} />}
          </g>
        )}
      </Layer>

      <Kicker x={120} y={150} p={p("start", 22)}>
        Fold it back
      </Kicker>
      <div style={{ position: "absolute", left: 0, top: 0, opacity: which === "a" ? aO : 0 }}>
        <M x={120} y={290} t="(p,q)=(1,0)" size={60} p={p("start", 26, 8)} />
        <Txt x={120} y={320} w={620} size={type.caption} italic c={color.ink2} p={p("start", 24, 20)}>
          aim at (2, 0); the midpoint (1, 0) is safe
        </Txt>
      </div>
      <div style={{ position: "absolute", left: 0, top: 0, opacity: which === "b" ? bIn : 0 }}>
        <M x={120} y={290} t="(p,q)=(2,1)" size={60} p={bIn} />
        <Txt x={120} y={320} w={620} size={type.caption} italic c={color.ink2} p={bIn}>
          aim at (4, 2); the midpoint (2, 1) is safe
        </Txt>
      </div>

      {/* the counter */}
      <div style={{ position: "absolute", left: 120, top: 440, ...{ opacity: p("start", 20, 30) } }}>
        <SmallCaps color={color.ink2}>Bounces</SmallCaps>
      </div>
      <div
        style={{
          position: "absolute",
          left: 112,
          top: 470,
          fontFamily: font.serif,
          fontSize: 190,
          lineHeight: 1,
          color: EDGE,
          fontFeatureSettings: features.figures,
          scale: `${1 + 0.18 * (1 - popK) * (lastTick > 0 ? 1 : 0)}`,
          transformOrigin: "30% 60%",
          opacity: p("start", 20, 30),
        }}
      >
        {count}
      </div>

      <Txt x={120} y={730} w={660} size={type.caption} p={p("count", 26, 60)}>
        It crosses <span style={{ color: EDGE }}>|p| vertical</span> and <span style={{ color: EDGE }}>|q| horizontal</span> walls:
      </Txt>
      <M x={120} y={880} t={`\\text{bounces} = |p|+|q| = 2+1 = {\\color{${EDGE}}3}`} size={52} p={p("count", 30, 90)} />
    </Sheet>
  );
};
