/**
 * Hook: four plates, four shots from the centre — into a corner; one bounce
 * then a corner; a wanderer that never settles; and one that comes home after
 * three bounces. Camera locked; each plate plays when the narration names it.
 */
import React from "react";
import { interpolate } from "remotion";
import { color, type } from "../../theme";
import { SmallCaps, clamp } from "../../components/Type";
import { Flash, HOMEC, Layer, POCKET, Rolling, Sheet, Table, Txt, World, useS, wipe } from "../kit";
import { V, polyAt, polyLen, realPath, shot } from "../geo";

const SPEED = 0.055; // math units per frame
const GOLD = (Math.sqrt(5) - 1) / 2;
const SHOTS: Array<{ pts: V[]; end: "pocket" | "home" | "none" }> = [
  { pts: realPath(shot([1, 1], 1)), end: "pocket" },
  { pts: realPath(shot([1, 3], 1)), end: "pocket" },
  { pts: realPath(shot([1, GOLD], 60)), end: "none" },
  { pts: realPath(shot([2, 1], 2)), end: "home" },
];
const LENS = SHOTS.map((s) => polyLen(s.pts));
const XS = [330, 750, 1170, 1590];
const OY = 520;
const U = 150;

export const Hook: React.FC = () => {
  const { f, at, p } = useS();
  const starts = [at("corner", 0.02), at("corner", 0.5), at("wander", 0.02), at("home", 0.02)];
  const plates = p("start", 30, 4);
  const q = p("question", 30);
  const q2 = p("question", 26, 60);
  const captions = [
    <>
      straight into a <span style={{ color: POCKET }}>corner</span>
    </>,
    <>
      one bounce, then a <span style={{ color: POCKET }}>corner</span>
    </>,
    <>still going …</>,
    <>
      <span style={{ color: HOMEC }}>home</span>, after three bounces
    </>,
  ];
  return (
    <Sheet folio={8} title="A few shots">
      <Layer>
        {SHOTS.map((s, i) => {
          const W: World = { ox: XS[i], oy: OY, u: U };
          const t = f - starts[i];
          const L = LENS[i];
          const frac = Math.max(0, (t * SPEED) / L);
          const done = t * SPEED >= L;
          const tEnd = done ? t - L / SPEED : -1;
          const endP = s.pts[s.pts.length - 1];
          // the wanderer: its trail thins as it grows, so the table stays readable
          const trailO = s.end === "none" ? interpolate(frac * L, [0, 30], [1, 0.55], clamp) : 1;
          const ballO = s.end === "pocket" && done ? interpolate(tEnd, [0, 10], [1, 0], clamp) : 1;
          const ballR = s.end === "pocket" && done ? interpolate(tEnd, [0, 10], [1, 0.3], clamp) : 1;
          const head = polyAt(s.pts, Math.min(1, frac)).p;
          return (
            <g key={i}>
              <Table W={W} real draw={interpolate(plates, [i * 0.12, 0.64 + i * 0.12], [0, 1], clamp)} />
              {t > 0 && (
                <>
                  <Rolling W={W} pts={s.pts} frac={Math.min(1, frac)} ball={false} w={s.end === "none" ? 2.6 : 3.6} o={trailO} />
                  {ballO > 0 && <circle cx={W.ox + head[0] * U} cy={W.oy - head[1] * U} r={11 * ballR} fill={color.ink} stroke={color.paper} strokeWidth={3} opacity={ballO} />}
                  {s.end === "pocket" && done && tEnd > 6 && <circle cx={W.ox + endP[0] * U} cy={W.oy - endP[1] * U} r={7} fill={POCKET} />}
                  {done && <Flash W={W} p={endP} t={tEnd / 26} c={s.end === "home" ? HOMEC : POCKET} r1={54} />}
                  {s.end === "home" && done && <circle cx={W.ox} cy={W.oy} r={22} fill="none" stroke={HOMEC} strokeWidth={3} opacity={interpolate(tEnd, [6, 18], [0, 1], clamp)} />}
                </>
              )}
            </g>
          );
        })}
      </Layer>
      {XS.map((x, i) => {
        const L = LENS[i];
        const resolved = i === 2 ? starts[i] + 40 : starts[i] + L / SPEED + 6;
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: x - 150, top: OY - U - 70, ...wipe(interpolate(plates, [i * 0.12, 0.5 + i * 0.12], [0, 1], clamp), 0) }}>
              <SmallCaps color={color.ink3}>{`Shot ${i + 1}`}</SmallCaps>
            </div>
            <Txt x={x} y={OY + U + 34} w={400} align="center" size={type.label} italic c={color.ink2} p={interpolate(f, [resolved, resolved + 20], [0, 1], clamp)}>
              {captions[i]}
            </Txt>
          </React.Fragment>
        );
      })}
      <Txt x={960} y={800} w={1500} align="center" size={76} italic p={q}>
        Which shots come <span style={{ color: HOMEC }}>home</span>?
      </Txt>
      <Txt x={960} y={912} w={1500} align="center" size={type.caption} italic c={color.ink2} p={q2}>
        Chasing bounces one by one is hopeless — we need a better picture.
      </Txt>
    </Sheet>
  );
};
