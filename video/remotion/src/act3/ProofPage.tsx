/**
 * The theorem page — one layout for both derivatives (sine on a verso, cosine
 * on the facing recto, margins on the outside edge like a real book).
 *
 *   margin            main column
 *   ────────          ─────────────────────────────────────────────
 *   THEOREM 3.x       d/dx sin x = cos x                (statement)
 *                     Proof.  d/dx sin x = lim [sin(x+h) − sin x]/h   (L1)
 *   SUM TO PRODUCT            = lim  2cos(x+h/2) sin(h/2) / h          (L2)
 *   sin(x+h) − sin x          → cos(x+h/2) · sin(h/2)/(h/2)   (the 2 slides down)
 *   = 2cos(x+h/2)                  ↓            ↓
 *     · sin(h/2)                 cos x          1        (limits)
 *                             = cos x · 1 = cos x  ∎    (the limits become L3)
 *
 * Every glyph that moves is a MathStage piece: the statement's d/dx sin x is
 * carried down into L1, L1's numerator flies to the margin, the margin's
 * product flies back into L2, the limit values rise into the result line.
 */
import React from "react";
import { color, font, semantic, type } from "../theme";
import { Key, MathStage, Piece, Poses, extent, row, withPose } from "../components/Stage";
import { SmallCaps } from "../components/Type";
import { InkReveal } from "../components/Type";
import { useBeats } from "./clock";
import { Gloss, InkPath, Layer, arrowDown, ringPath } from "./scenes/common";

export type Variant = "sin" | "cos";

export type Cues = {
  statement: number;
  definition: number;
  idA: number; // L1 numerator → margin
  idB: number; // the product is written in the margin
  fly: number; // product → L2
  rewrite: number;
  lim1: number;
  lim2: number;
  qed1: number;
  qed2: number;
};

/** Geometry of the page (verso = margin left, recto = margin right). */
export const pageGeo = (v: Variant) =>
  v === "sin"
    ? { side: 120, sideW: 280, main: 470, mainR: 1800, stmtX: 1135, barX: 436 }
    : { side: 1520, sideW: 280, main: 150, mainR: 1450, stmtX: 800, barX: 1484 };

const Y = { stmt: 300, l1: 520, l2: 716, lab: 892, l3: 892, margin: 520 } as const;
const SZ = { stmt: type.formula - 8, proof: 66, margin: 42, lab: 62 } as const;

const pieces = (v: Variant): Record<string, Piece> => {
  const S = v === "sin";
  const fn = S ? "\\sin x" : "\\cos x";
  const fc = S ? semantic.sin : semantic.cos;
  const fac = S ? "\\cos\\!\\left(x+\\tfrac h2\\right)" : "\\sin\\!\\left(x+\\tfrac h2\\right)";
  const facC = S ? semantic.cos : semantic.sin;
  const P: Record<string, Piece> = {
    sD: { tex: "\\frac{d}{dx}", color: semantic.derivative },
    sF: { tex: fn, color: fc },
    sE: { tex: "=" },
    sR: { tex: S ? "\\cos x" : "\\sin x", color: S ? semantic.cos : semantic.sin },
    aD: { tex: "\\frac{d}{dx}", color: semantic.derivative },
    aF: { tex: fn, color: fc },
    aE: { tex: "=" },
    aL: { tex: "\\lim_{h\\to 0}" },
    aN: { tex: S ? "\\sin(x+h)-\\sin x" : "\\cos(x+h)-\\cos x" },
    aB: { bar: true },
    aH: { tex: "h" },
    mN: { tex: S ? "\\sin(x+h)-\\sin x" : "\\cos(x+h)-\\cos x" },
    mE: { tex: "=" },
    m2: { tex: "2" },
    mC: { tex: fac, color: facC },
    mS: { tex: "\\cdot\\,\\sin(h/2)" },
    bE: { tex: "=" },
    bL: { tex: "\\lim_{h\\to 0}" },
    n2: { tex: "2" },
    nC: { tex: fac, color: facC },
    nS: { tex: "\\sin(h/2)" },
    bB: { bar: true },
    bH: { tex: "h" },
    bSl: { tex: "/" },
    lC: { tex: S ? "\\cos x" : "{-}\\!\\sin x", color: S ? semantic.cos : semantic.sin },
    l1: { tex: "1" },
    cE: { tex: "=" },
    cDot: { tex: "\\cdot" },
    cE2: { tex: "=" },
    cR: { tex: S ? "\\cos x" : "{-}\\!\\sin x", color: S ? semantic.cos : semantic.sin },
  };
  if (!S) {
    P.sM = { tex: "{-}", color: semantic.sin };
    P.mM = { tex: "{-}" };
    P.nM = { tex: "{-}" };
  }
  return P;
};

/** All poses of the derivation, by state. */
export const layoutProof = (v: Variant) => {
  const S = v === "sin";
  const P = pieces(v);
  const G = pageGeo(v);
  const stmt = row(P, S ? ["sD", "sF", ["sE", 0.3], ["sR", 0.3]] : ["sD", "sF", ["sE", 0.3], ["sM", 0.3], ["sR", 0.03]], G.stmtX, Y.stmt, SZ.stmt, "center");
  const x0 = G.main + 190; // after "Proof."
  const L1 = row(P, ["aD", "aF", ["aE", 0.3], ["aL", 0.3], { num: ["aN"], den: ["aH"], bar: "aB", gap: 0.18 }], x0, Y.l1, SZ.proof);
  const eqX = L1.aE.x;
  const numItems = S ? ["n2", ["nC", 0.06], ["nS", 0.12]] : ["nM", ["n2", 0.02], ["nC", 0.06], ["nS", 0.12]];
  const L2a = row(P, ["bE", ["bL", 0.3], { num: numItems as never, den: ["bH"], bar: "bB", gap: 0.18 }], eqX, Y.l2, SZ.proof);
  const L2b = row(
    P,
    [
      "bE",
      ["bL", 0.3],
      ...((S ? [] : [["nM", 0.3]]) as never[]),
      ["nC", S ? 0.3 : 0.03],
      { num: ["nS"], den: ["bH", ["bSl", 0.02], ["n2", 0.02]], bar: "bB", gap: 0.16 },
    ],
    eqX,
    Y.l2,
    SZ.proof,
  );
  // margin: numerator, then "= 2 cos(...)" and "· sin(h/2)" (cosine: "= −2 sin(...)")
  const mx = G.side;
  const M1 = row(P, ["mN"], mx, Y.margin + 70, SZ.margin);
  const M2 = row(P, S ? ["mE", ["m2", 0.24], ["mC", 0.06]] : ["mE", ["mM", 0.24], ["m2", 0.02], ["mC", 0.06]], mx, Y.margin + 150, SZ.margin);
  const M3 = row(P, ["mS"], mx + 40, Y.margin + 222, SZ.margin);
  // flying copies start exactly on their margin twins
  const fromMargin: Poses = {
    n2: { ...M2.m2, o: 0 },
    nC: { ...M2.mC, o: 0 },
    nS: { ...M3.mS, x: M3.mS.x + 0.2 * SZ.margin, o: 0 },
    ...(S ? {} : { nM: { ...M2.mM, o: 0 } }),
  };
  // limits hang under the two factors of L2b
  const eC = extent(P, L2b, "nC");
  const eF = extent(P, L2b, "bB");
  const cxC = S ? eC.cx : (L2b.nM.x + eC.x1) / 2;
  const labC = row(P, ["lC"], cxC, Y.lab, SZ.lab, "center");
  const lab1 = row(P, ["l1"], eF.cx, Y.lab, SZ.lab, "center");
  const L3 = row(P, ["cE", ["lC", 0.3], ["cDot", 0.22], ["l1", 0.22], ["cE2", 0.3], ["cR", 0.3]], eqX, Y.l3, SZ.proof);
  return { P, G, stmt, L1, L2a, L2b, M1, M2, M3, fromMargin, labC, lab1, L3, cxC, fracCx: eF.cx, eqX };
};

type Lay = ReturnType<typeof layoutProof>;

export const proofKeys = (L: Lay, c: Cues, v: Variant): Key[] => {
  const keys: Key[] = [];
  let snap: Poses = {};
  const push = (at: number, add: Poses, drop: string[] = []) => {
    snap = { ...snap, ...add };
    drop.forEach((k) => delete snap[k]);
    keys.push({ at, poses: snap });
  };
  const d = (p: Poses, delay: number) => withPose(p, { delay });
  // the carried copies sit exactly on the statement (invisible twins) until they peel off
  push(c.statement, { ...L.stmt, aD: L.stmt.sD, aF: L.stmt.sF });
  push(c.definition, {
    aD: L.L1.aD,
    aF: { ...L.L1.aF, delay: 3 },
    ...d({ aE: L.L1.aE }, 12),
    ...d({ aL: L.L1.aL }, 16),
    ...d({ aB: L.L1.aB }, 22),
    ...d({ aN: L.L1.aN }, 28),
    ...d({ aH: L.L1.aH }, 34),
    mN: { ...L.L1.aN, o: 0 },
  });
  push(c.idA, { mN: L.M1.mN });
  push(c.idB, {
    mE: L.M2.mE,
    ...(v === "cos" ? d({ mM: L.M2.mM }, 4) : {}),
    ...d({ m2: L.M2.m2 }, 6),
    ...d({ mC: L.M2.mC }, 12),
    ...d({ mS: L.M3.mS }, 22),
    ...L.fromMargin,
  });
  const flying = v === "sin" ? ["n2", "nC", "nS"] : ["nM", "n2", "nC", "nS"];
  push(c.fly, {
    ...withPose(Object.fromEntries(Object.entries(L.L1)), { o: 0.42 }),
    bE: L.L2a.bE,
    ...d({ bL: L.L2a.bL }, 4),
    ...d({ bB: L.L2a.bB }, 8),
    ...d({ bH: L.L2a.bH }, 12),
    ...Object.fromEntries(flying.map((k, i) => [k, { ...L.L2a[k], delay: 10 + i * 5 }])),
  });
  push(c.rewrite, {
    // order matters: the bar retracts, the cos factor steps out, the 2 drops under the h, and only
    // then does sin(h/2) slide left into its new fraction (so no two glyphs cross)
    ...Object.fromEntries(
      ["bE", "bL", "bB", "bH", ...flying].map((k) => [k, { ...L.L2b[k], delay: ({ bB: 0, nM: 10, nC: 10, n2: 12, bH: 12, nS: 24 } as Record<string, number>)[k] ?? 0 }]),
    ),
    bSl: { ...L.L2b.bSl, delay: 18 },
  });
  push(c.lim1, { lC: { ...L.labC.lC, delay: 16 } });
  push(c.lim2, { l1: { ...L.lab1.l1, delay: 16 } });
  push(c.qed1, {
    lC: L.L3.lC,
    l1: { ...L.L3.l1, delay: 5 },
    ...d({ cE: L.L3.cE }, 8),
    ...d({ cDot: L.L3.cDot }, 12),
  });
  push(c.qed2, { ...d({ cE2: L.L3.cE2 }, 0), ...d({ cR: L.L3.cR }, 6) });
  return keys;
};

/** The page's content (no camera, no paper): used by the scene and by the facing-page spread. */
export const ProofContent: React.FC<{ v: Variant; cues: Cues; dimRest?: number }> = ({ v, cues: c, dimRest = 1 }) => {
  const { p, frame } = useBeats();
  const L = layoutProof(v);
  const keys = proofKeys(L, c, v);
  const G = L.G;
  const S = v === "sin";
  const num = S ? "3.1" : "3.2";

  // annotations under L2b (they give way to the result line at qed)
  const annoOut = 1 - p(c.qed1, 14);
  const a1 = p(c.lim1, 20);
  const a2 = p(c.lim2, 20);
  const arrTop = Y.l2 + 62;
  const arrBot = Y.lab - 60;
  const A1 = arrowDown(L.cxC, arrTop, arrBot);
  const A2 = arrowDown(L.fracCx, arrTop, arrBot);
  // tombstone + a pen ring round the statement's right-hand side at the end
  const tomb = p(c.qed2 + 14, 12);
  const eR = extent(L.P, L.stmt, "sR");
  const x0r = S ? eR.x0 : L.stmt.sM.x;
  const ring = ringPath((x0r + eR.x1) / 2 + 4, Y.stmt - 0.26 * SZ.stmt, (eR.x1 - x0r) / 2 + 34, 0.6 * SZ.stmt);
  const ringP = p(c.qed2 + 10, 30);
  const rest = dimRest;

  return (
    <>
      {/* theorem label in the margin, with the rubric bar */}
      <div style={{ position: "absolute", left: G.barX - 1.5, top: 214, width: 3.5, height: 150, background: color.accent }} />
      <InkReveal from={0} len={1} style={{ left: G.side, top: 228, width: G.sideW + 20, height: 140 }}>
        <SmallCaps color={color.accent}>Theorem {num}</SmallCaps>
        <div style={{ marginTop: 10, fontFamily: font.serif, fontStyle: "italic", fontSize: type.caption, lineHeight: 1.25, color: color.ink2, whiteSpace: "nowrap" }}>
          Derivative of {S ? "sine" : "cosine"}
        </div>
      </InkReveal>
      <Gloss x={G.stmtX} w={900} align="center" y={Y.stmt + 44} opacity={p(c.statement + 26, 18) * rest} size={type.caption}>
        for every real number <span style={{ fontStyle: "normal" }}>x</span> (in radians)
      </Gloss>

      {/* Proof. */}
      <Gloss x={G.main} y={Y.l1 - 42} size={type.body} c={color.ink} opacity={p(c.definition, 16) * rest}>
        Proof.
      </Gloss>

      {/* margin note: sum to product */}
      <div style={{ position: "absolute", left: G.side, top: Y.margin - 24, opacity: p(c.idA, 16) * rest }}>
        <SmallCaps color={color.ink2}>Sum to product</SmallCaps>
      </div>

      {/* annotation glosses */}
      <Gloss x={L.cxC} w={420} align="center" y={Y.lab + 16} size={30} opacity={a1 * annoOut * rest}>
        {S ? "cos is continuous" : "sin is continuous"}
      </Gloss>
      <Gloss x={L.fracCx} w={420} align="center" y={Y.lab + 16} size={30} opacity={a2 * annoOut * rest}>
        the fundamental limit
      </Gloss>

      <Layer>
        <g opacity={rest}>
          <InkPath d={A1.d} len={A1.len} p={a1} w={3.2} opacity={annoOut} />
          <InkPath d={A2.d} len={A2.len} p={a2} w={3.2} opacity={annoOut} />
          <text
            x={extent(L.P, L.L3, "cR").x1 + 34}
            y={Y.l3}
            style={{ fontFamily: font.serif, fontSize: 44 }}
            fill={color.ink}
            opacity={tomb}
          >
            ∎
          </text>
        </g>
        <MathStage pieces={L.P} keys={keys} opacity={frame >= 0 ? 1 : 0} />
        <InkPath d={ring.d} len={ring.len} p={ringP} w={3.4} />
      </Layer>
    </>
  );
};

/** Cue frames from the sine scene's beats. */
export const sineCues = (at: (id: string, k?: number) => number): Cues => ({
  statement: at("statement"),
  definition: at("definition"),
  idA: at("identity", 0.02),
  idB: at("identity", 0.38),
  fly: at("identity", 0.8),
  rewrite: at("rewrite", 0.05),
  lim1: at("limits", 0.02),
  lim2: at("limits", 0.5),
  qed1: at("qed"),
  qed2: at("qed", 0.45),
});

/** Cosine moves faster: the definition and identity share one beat. */
export const cosineCues = (at: (id: string, k?: number) => number): Cues => ({
  statement: at("statement"),
  definition: at("identity"),
  idA: at("identity", 0.12),
  idB: at("identity", 0.3),
  fly: at("identity", 0.84),
  rewrite: at("rewrite", 0.05),
  lim1: at("limits", 0.02),
  lim2: at("limits", 0.45),
  qed1: at("qed"),
  qed2: at("qed", 0.45),
});

export const PROOF_Y = Y;
