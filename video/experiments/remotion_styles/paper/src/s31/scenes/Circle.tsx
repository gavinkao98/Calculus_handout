/**
 * Cold open: a point rides the unit circle; its height traces sine; the
 * velocity arrow (unit length, because radians = arc length) predicts the
 * derivative before we prove anything.
 */
import React from "react";
import { Easing, interpolate } from "remotion";
import { color, semantic, stroke, type } from "../../theme";
import { clamp, measure } from "../../components/Type";
import { Arrow, HOME, Kicker, Layer, Ln, M, Sheet, Txt, camPath, useS } from "../kit";

const PI = Math.PI;
const O = { x: 540, y: 580 };
const R = 250;
const G = { x: 940, y: 580, ux: 800 / (2 * PI) }; // graph: same vertical unit as the circle
const TH = 0.9; // where the point parks

export const Circle: React.FC = () => {
  const { f, at, p, pf, atWord } = useS();
  const fT = at("trace");
  const fS = at("speed");
  const omega = (2 * PI) / Math.max(90, at("question") - fT);

  // ── the angle: constant spin, then it glides to rest at TH ──
  let phi = omega * (f - fT);
  if (f > fS) {
    const phiS = omega * (fS - fT);
    const base = phiS + 0.9;
    const target = base + ((((TH - base) % (2 * PI)) + 2 * PI) % (2 * PI));
    const len = Math.max(30, Math.round(((target - phiS) / omega) * 1.7));
    phi = phiS + (target - phiS) * interpolate(f, [fS, fS + len], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  }
  const P = { x: O.x + R * Math.cos(phi), y: O.y - R * Math.sin(phi) };
  const parked = interpolate(f, [fS + 40, fS + 70], [0, 1], clamp);

  // ── reveals ──
  const circ = pf(4, 46);
  const axes = pf(20, 30);
  const hgt = p("height", 18);
  const graph = p("trace", 26);
  const inGraph = phi >= 0 ? Math.min(phi, 2 * PI) : 0;
  const curveEnd = f >= fT ? inGraph : 0;
  const graphO = interpolate(f, [fS, fS + 30], [1, 0], clamp);
  const q = p("question", 30, 0, Easing.out(Easing.cubic));
  const arc = p("speed", 40);
  const note1 = p("speed", 26, 10);
  // the velocity arrow appears as the narration names it ("...an arrow of length one")
  const arrowAt = atWord("arrow", { afterFrame: fS }) ?? fS + Math.round((at("vertical") - fS) * 0.5);
  const arrow = pf(arrowAt, 34);
  const note2 = pf(arrowAt + 14, 26);
  const vert = p("vertical", 30);
  const guess = p("guess", 30);
  const cav = p("caveat", 26, 8);

  // hero open: close on the circle while it inks, then ONE pull back to the page (before
  // the height is drawn); from there the camera is locked for the rest of the scene.
  const cam = camPath(f, { cx: 640, cy: O.y, s: 1.5 }, [[58, HOME, 56]]);

  // graph marker
  const gx = (x: number) => G.x + x * G.ux;
  const gy = (y: number) => G.y - y * R;
  const mphi = ((phi % (2 * PI)) + 2 * PI) % (2 * PI);
  const sinPts = (end: number) => {
    const n = Math.max(2, Math.ceil(160 * (end / (2 * PI))));
    let d = "";
    for (let i = 0; i <= n; i++) {
      const x = (end * i) / n;
      d += `${i ? "L" : "M"}${gx(x).toFixed(1)} ${gy(Math.sin(x)).toFixed(1)}`;
    }
    return d;
  };
  const graphLive = f >= fT && graphO > 0;
  const mx = f < fT + (at("question") - fT) ? Math.min(Math.max(phi, 0), 2 * PI) : mphi;

  // velocity arrow (unit tangent) at the parked point
  const V = { x: -R * Math.sin(phi), y: -R * Math.cos(phi) };
  const tip = { x: P.x + V.x, y: P.y + V.y };

  // arc A→P (radians = arc length)
  const arcPath = (() => {
    const e = Math.max(0.001, TH * arc);
    return `M${O.x + R} ${O.y} A${R} ${R} 0 0 0 ${O.x + R * Math.cos(e)} ${O.y - R * Math.sin(e)}`;
  })();

  return (
    <Sheet folio={111} title="" head={false} cam={cam}>
      <Layer>
        {/* crosshair through the centre */}
        <Ln x1={O.x - R * 1.22} y1={O.y} x2={O.x + R * 1.22} y2={O.y} p={axes} c={color.ink3} w={stroke.axis} />
        <Ln x1={O.x} y1={O.y + R * 1.22} x2={O.x} y2={O.y - R * 1.22} p={axes} c={color.ink3} w={stroke.axis} />
        {/* the circle, inked */}
        <circle
          cx={O.x}
          cy={O.y}
          r={R}
          fill="none"
          stroke={color.ink}
          strokeWidth={stroke.curve * 0.8}
          strokeDasharray={`${2 * PI * R * circ} ${2 * PI * R}`}
          transform={`rotate(0 ${O.x} ${O.y})`}
        />
        {/* the arc = the angle */}
        {arc > 0 && <path d={arcPath} fill="none" stroke={color.ochre} strokeWidth={9} strokeLinecap="round" opacity={0.85} />}
        {/* radius */}
        <line x1={O.x} y1={O.y} x2={P.x} y2={P.y} stroke={color.ink2} strokeWidth={stroke.hairline * 1.4} opacity={circ} />
        {/* height of the point */}
        {hgt > 0 && <line x1={P.x} y1={O.y} x2={P.x} y2={O.y + (P.y - O.y) * hgt} stroke={color.ink} strokeWidth={stroke.emphasis + 1} strokeLinecap="round" />}

        {/* graph */}
        {graph > 0 && (
          <g opacity={graphO}>
            <Ln x1={gx(0)} y1={G.y} x2={gx(2 * PI) + 20} y2={G.y} p={graph} c={color.ink2} w={stroke.axis} />
            <Ln x1={gx(0)} y1={gy(-1)} x2={gx(0)} y2={gy(1)} p={graph} c={color.ink2} w={stroke.axis} />
            {[PI, 2 * PI].map((v) => (
              <line key={v} x1={gx(v)} y1={G.y} x2={gx(v)} y2={G.y + 10} stroke={color.ink2} strokeWidth={stroke.axis} opacity={graph} />
            ))}
            {curveEnd > 0 && <path d={sinPts(curveEnd)} fill="none" stroke={semantic.sin} strokeWidth={stroke.curve} strokeLinecap="round" />}
            {graphLive && (
              <>
                <line x1={P.x} y1={P.y} x2={gx(mx)} y2={P.y} stroke={color.ink3} strokeWidth={1.6} strokeDasharray="2 7" strokeLinecap="round" />
                <line x1={gx(mx)} y1={G.y} x2={gx(mx)} y2={gy(Math.sin(phi))} stroke={color.ink} strokeWidth={stroke.emphasis + 1} strokeLinecap="round" />
                <circle cx={gx(mx)} cy={gy(Math.sin(phi))} r={stroke.dot} fill={color.ink} stroke={color.paper} strokeWidth={stroke.ring} />
              </>
            )}
          </g>
        )}

        {/* velocity: a unit arrow tangent to the circle */}
        <Arrow x1={P.x} y1={P.y} x2={tip.x} y2={tip.y} p={arrow * parked} c={color.accent} w={4.5} head={20} />
        {/* its vertical and horizontal parts */}
        {vert > 0 && (
          <>
            <Ln x1={tip.x} y1={tip.y} x2={P.x} y2={tip.y} p={vert} c={color.ink3} w={2} dash="3 8" />
            <Ln x1={P.x} y1={P.y} x2={P.x} y2={tip.y} p={vert} c={color.accent} w={stroke.emphasis + 1} />
          </>
        )}
        <circle cx={P.x} cy={P.y} r={stroke.dot + 1} fill={color.ink} stroke={color.paper} strokeWidth={stroke.ring} opacity={circ} />
        <circle cx={O.x} cy={O.y} r={4.5} fill={color.ink2} opacity={axes} />
      </Layer>

      {/* labels */}
      <Txt x={P.x + 14} y={(P.y + O.y) / 2 - 24} size={type.label} italic c={color.ink2} p={hgt} o={1 - parked} w={200}>
        height
      </Txt>
      <M x={P.x - 14} y={(P.y + O.y) / 2 + 14} t="\sin\theta" size={40} align="right" p={parked * hgt} />
      <M x={O.x + R * Math.cos(TH / 2) + 22} y={O.y - R * Math.sin(TH / 2) + 8} t="\theta" size={46} c={color.ochre} p={arc} />
      <M x={P.x + 18} y={(P.y + tip.y) / 2 + 12} t="\cos\theta" size={44} c={color.cobalt} p={vert} />
      <Txt x={tip.x - 60} y={tip.y - 66} size={type.label} italic c={color.accent} p={arrow * parked} w={220}>
        speed 1
      </Txt>
      {graph > 0 && (
        <>
          <M x={gx(PI)} y={G.y + 50} t="\pi" size={type.label} align="center" c={color.ink2} p={graph} o={graphO} />
          <M x={gx(2 * PI)} y={G.y + 50} t="2\pi" size={type.label} align="center" c={color.ink2} p={graph} o={graphO} />
          <M x={gx(2 * PI) + 40} y={G.y + 12} t="\theta" size={40} c={color.ink2} p={graph} o={graphO} />
          <M x={gx(PI / 2) - 30} y={gy(1) - 28} t="y=\sin\theta" size={44} p={graph} o={graphO} />
        </>
      )}

      {/* the question */}
      <Txt x={960} y={140} w={1400} align="center" size={78} italic p={q} o={1 - p("speed", 30)}>
        How fast does sine change?
      </Txt>

      {/* notes column */}
      <Kicker x={1100} y={300} p={note1}>
        Radians
      </Kicker>
      <Txt x={1100} y={352} w={680} size={type.body} p={note1} c={color.ink}>
        The angle <i style={{ color: color.ochre }}>θ</i> is the length of the gold arc.
      </Txt>
      <Txt x={1100} y={430} w={680} size={type.body} p={note2} c={color.ink}>
        So <i>P</i> moves at speed 1: its velocity is a <span style={{ color: color.accent }}>unit arrow</span>, tangent to the
        circle.
      </Txt>
      <Txt x={1100} y={590} w={680} size={type.body} p={vert} c={color.ink}>
        Its vertical part has length
      </Txt>
      <M x={1100 + measure("Its vertical part has length", type.body) + 14} y={632} t="\cos\theta." size={52} c={color.cobalt} p={vert} />
      <Kicker x={1100} y={690} p={guess}>
        The guess
      </Kicker>
      <M
        x={1100}
        y={884}
        t={`{\\color{${color.accent}}\\frac{d}{d\\theta}}\\sin\\theta\\;\\overset{?}{=}\\;{\\color{${color.cobalt}}\\cos\\theta}`}
        size={84}
        p={guess}
      />
      <Txt x={1100} y={944} w={700} size={type.caption} italic c={color.accent} p={cav}>
        A prediction read off a picture — not yet a proof.
      </Txt>
    </Sheet>
  );
};
