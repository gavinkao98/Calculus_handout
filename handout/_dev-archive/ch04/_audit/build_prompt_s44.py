#!/usr/bin/env python3
"""Assemble the Codex gate-2 auditor prompt for §4.4 (mirrors build_prompt_s43.py).
Reads seed + brief + draft, wraps with header / §4.4 scope notes / HTML rules / final
instruction, writes prompt_s44.txt. §4.4 HAS a figure (Figure 4.2, MVT secant-tangent),
but it is JS-rendered from the chapter FIGS registry; the auditor reviews the figure
CAPTION and the geometric claim, not a pixel image. Run: python build_prompt_s44.py"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SEED = ROOT / "handout/_dev-archive/ch04/seed_ch04_s4.md"
BRIEF = ROOT / "handout/_dev-archive/ch04/brief_s44.md"
DRAFT = ROOT / "handout/fragments/ch04/sec-4-4.html"
OUT = Path(__file__).resolve().parent / "prompt_s44.txt"

seed = SEED.read_text(encoding="utf-8")
brief = BRIEF.read_text(encoding="utf-8")
draft = DRAFT.read_text(encoding="utf-8")

HEADER = """You are an ADVISORY adversarial reviewer of a calculus handout section (HTML format) that was expanded from the SEED below, following an approved DIRECTION BRIEF. You do NOT rewrite; you surface findings for a human.

Hunt especially for:
(a) mathematical errors, fabricated theorems/identities, or over-generalized claims;
(b) drift from the seed's mathematics (the seed IS the manuscript's mathematical backbone);
(c) direction-conformance violations: did the draft cover what the brief specifies? did it include anything from the brief's "do-not-write" (kept under the heading 刻意不寫) list?

Tag EVERY finding with a CATEGORY and a BLOCKING flag (do not inflate):
  category: math | faithfulness | direction-conformance | house_rule | register | other
  blocking: true ONLY for:
    - a real MATH ERROR or fabricated/over-generalized claim (category=math)
    - DRIFT from the seed's mathematics (category=faithfulness)
    - VIOLATION of direction-conformance: missing a brief-mandated item OR including a brief-forbidden item (category=direction-conformance)
  Everything else MUST be blocking=false.

Formatting / house-rule items (missing expansion comments, register/style nits) are caught by a downstream DETERMINISTIC LINTER, so report them as ADVISORY (blocking=false); they MUST NOT block convergence.

Also give each finding a level for human triage:
  1 = real conflict (must fix)
  2 = discoverability gap (add doc/comment)
  3 = editorial drift (low priority)
  4 = non-finding (mathematically equivalent paraphrase, stylistic preference)

A mathematically equivalent paraphrase is NOT a finding.

This is the HEAVIEST, most proof-dense section of the chapter: four theorems (three with full proofs), a corollary with proof, a key figure, a strategy, and three worked examples. Its risk is the OPPOSITE of a thin section — it is that the proof ladder Theorem A -> Rolle -> MVT -> Corollary be RIGOROUS and unbroken, not that content be missing. Spend your effort on the MATH of each proof and on direction-conformance. Re-derive each step INDEPENDENTLY:
  - Theorem 4.10 (interior extremum / "Theorem A"): from f(xM) >= f(x) get f(xM+h) - f(xM) <= 0; for h>0 the difference quotient is <= 0 so the right-hand limit f'(xM) <= 0; for h<0 the quotient is >= 0 (nonpositive numerator over negative denominator) so the left-hand limit f'(xM) >= 0; a number both <=0 and >=0 is 0. Check the sign bookkeeping and that interiority (xM in open (a,b)) is what makes both one-sided increments available.
  - Theorem 4.11 (Rolle): EVT gives max xM and min xm. Case 1: m = M, combined with f(a)=f(b), forces f constant, so f'=0 everywhere. Case 2: m < M; since f(a)=f(b), at least one of f(xM) > f(a) or f(xm) < f(a) holds; the corresponding extremum is then interior, and Theorem 4.10 gives f'=0 there. VERIFY the Case-2 second branch is "f(xm) < f(a)" (the manuscript slip wrote f(xM); the draft is supposed to have CORRECTED it — if the draft still says f(xM) in the second branch, that IS a real error).
  - Theorem 4.12 (MVT): auxiliary g(x) = f(x) - [f(a) + ((f(b)-f(a))/(b-a))(x-a)]; verify g continuous on [a,b], differentiable on (a,b), g(a)=g(b)=0; Rolle yields c with g'(c)=0; g'(c) = f'(c) - (f(b)-f(a))/(b-a) (the bracket differentiates to the constant secant slope); hence f'(c) = (f(b)-f(a))/(b-a).
  - Corollary 4.3 (monotonicity, BOTH forms): apply MVT on [x1,x2]; (f(x2)-f(x1))/(x2-x1) = f'(c); denominator positive; f'>=0 gives non-decreasing, f'>0 gives strictly increasing. Check the strict/non-strict split is correct.
  - Example 4.2 (MVT on x^2 over [0,2]): average slope (4-0)/(2-0) = 2; f'(x)=2x; 2c=2 => c=1 in (0,2). Check.
  - Example 4.3 (sin on [0, pi/4]): (sin x)' = cos x > 0 there => strictly increasing. Example 4.4 (e^x on R): e^x > 0 everywhere (series for x>=0; exponent law e^x = 1/e^{-x} for x<0) => strictly increasing on every [x1,x2] => on R. Check the "every closed interval => all of R" extension is valid for strict monotonicity.
  - Theorem 4.9 (Extreme Value Theorem): stated correctly and used WITHOUT proof (as a black box, justified by completeness). The draft must NOT smuggle in a proof.
  - Figure 4.2 caption claim: the secant through (a,f(a)),(b,f(b)) has slope (f(b)-f(a))/(b-a) and some interior tangent is parallel to it — verify this is exactly the MVT statement, no false claim. (The figure itself is drawn by JS and renders cleanly; you are reviewing the caption's mathematical claim, not an image.)
Cross-check the math against the SIGNED LEGACY GROUND TRUTH legacy/tex_handout/chapters/ch04_exponential_logarithm.tex, section \\section{Rolle's Theorem and the Mean Value Theorem} (label sec:rolle-and-mvt) PLUS the monotonicity corollary at the head of the next section (label cor:monotonicity). NOTE: the legacy places the monotonicity corollary and the sin/e^x examples at the START of §4.5; the handout (following the manuscript's page order and the chapter PLAN) places them at the END of §4.4, closing with "e^x is strictly increasing on R". BOTH orderings are valid; this is the approved placement decision -- do NOT flag the corollary's presence in §4.4 as out-of-scope or as duplicating §4.5.

NUMBERING NOTE: §4.4 is NOT the chapter's first section. Per-type counters CONTINUE from §4.1-§4.3 (which used Definition 4.1/4.2; Theorem 4.1-4.8; Proposition 4.1/4.2; Corollary 4.1/4.2; Strategy 4.1; Example 4.1; Figure 4.1; Remark 4.1-4.3). Therefore §4.4 correctly uses: Definition 4.3 (max/min); Theorem 4.9 (Extreme Value Theorem), 4.10 (interior extremum "Theorem A"), 4.11 (Rolle), 4.12 (MVT); Corollary 4.3 (monotonicity); Strategy 4.2 (applying the MVT); Figure 4.2 (secant-tangent); Example 4.2 (MVT on x^2), 4.3 (sin), 4.4 (e^x); Remark 4.4. §4.4 mints NO new Proposition. Cross-references ("Theorem 4.1" completeness, "Theorem 4.7" exponent law, "Theorem 4.8" derivative of e^x, "Theorem 4.9/4.10/4.11/4.12", "Corollary 4.3", "Chapter 3") are correct, not missing content. This continuation is CORRECT -- do NOT flag it as a discontinuity.

SCOPE / EXPANSION NOTE for §4.4: the SEED covers manuscript pp.11-18 (the block the manuscript heads "§ Rolle's Theorem": max/min definition -> cos x example -> EVT "Fact" (stated unproved) -> Theorem A -> Rolle -> MVT -> monotonicity Corollary -> examples sin and e^x -> "e^x strictly increasing"). The draft adds, as MARKED expansions sanctioned by the brief (gate 3 approved "全照提案核可" PLUS all four optional add-ons) and cross-checked against the signed legacy ground truth:
  - An OPENER that frames the MVT as the existence bridge from pointwise derivative to interval behaviour, picking up §4.3's closing fence (monotonicity needs an existence theorem). INTENDED.
  - A ONE-SENTENCE history attribution of Rolle (Michel Rolle, 1691) and the MVT (Cauchy and the 19th-century analysts), marked [source: standard calculus-textbook historical note]. Optional add-on APPROVED. Do not demand a specific citation beyond the standard-note tag.
  - The Extreme Value Theorem NAMED as Theorem 4.9, stated WITHOUT proof, cross-referencing completeness (Theorem 4.1), with a compact note that both hypotheses (closed interval, continuity) are essential. INTENDED (the manuscript states it as a "Fact" without proof).
  - Figure 4.2 (MVT secant-tangent, ROADMAP key figure) and Strategy 4.2 (verifying MVT hypotheses, with the |x| on [-1,1] counterexample and the closed/open asymmetry folded in). ROADMAP-mandated. INTENDED.
  - A caution that Theorem 4.10 needs the extremum INTERIOR (endpoint counterexample f(x)=x on [0,1]). INTENDED.
  - Remark 4.4 (explicit box): the synthesis that Rolle is the MVT special case, the Theorem A -> Rolle -> MVT ladder, and the MVT as the central existence engine reused for monotonicity and later Taylor. Optional add-on APPROVED.
  - Corollary 4.3 stated in BOTH forms (non-strict and strict). The manuscript states only the non-strict form but its examples conclude strict; the strict form is REQUIRED downstream (§4.5 needs e^x strictly increasing for injectivity). INTENDED fill.
  - A one-line justification that e^x > 0 everywhere (Example 4.4) and a one-line note that strict monotonicity passes from every closed interval to all of R. INTENDED fills.
  - The two corollary examples SPLIT into Example 4.3 (sin) and Example 4.4 (e^x), and an EXTRA MVT numerical worked Example 4.2 (x^2 on [0,2], c=1). Optional add-ons APPROVED.
These are INTENDED expansions, not drift.

DELIBERATELY OMITTED (brief 刻意不寫) -- these MUST NOT appear in the §4.4 body; flag as blocking direction-conformance ONLY if they actually appear:
  - constructing, defining, or differentiating ln x (that is §4.5; only the hand-off sentence "e^x is strictly increasing, hence invertible, so the next section builds ln x" is allowed);
  - a PROOF of the Extreme Value Theorem (it is stated as a black box; the completeness-based proof is deferred);
  - Taylor's theorem, higher-order or Cauchy's generalized MVT, or L'Hopital's rule (later chapters);
  - re-proving §4.3's (e^x)'=e^x (it is only CITED as Theorem 4.8);
  - moving or proposing to move the MVT out of Chapter 4 (decision D4: it stays; only a forward-only fence to §4.5 is allowed);
  - an integral / antiderivative framing of monotonicity (the corollary goes through the MVT, not integration, which is not yet built);
  - concavity / the second-derivative test (out of scope);
  - any self-invented "your turn" / bare exercise;
  - OVER-EXPANSION: padding beyond the intended ladder. NOTE: this is the chapter's heaviest section by design -- four theorems + one corollary + one figure + one strategy + three worked examples + one remark is the APPROVED scope (gate 3 took all four optional add-ons), NOT over-expansion. Only flag genuinely redundant lemmas/examples/cautions beyond that.

This section HAS one figure (Figure 4.2, the MVT secant-tangent picture; ROADMAP key figure). It is drawn by the chapter's JS figure registry and renders cleanly (verified: 0 MathJax errors, 22 print pages for the chapter, 0 overflow, the tangent is numerically parallel to the secant and touches the curve at the interior c). Do NOT report "figure missing"; review only the figure CAPTION's mathematical claim.

Set "converged": true when there are ZERO blocking findings (math correct, faithful to seed, conforms to direction brief), even if advisory formatting nits remain.

Return STRICT JSON only, no prose outside the JSON.
"""

RULES = """=== KEY HTML WRITING RULES (advisory -- for house_rule findings) ===
- Semantic env classes: env-definition, env-theorem, env-proposition, env-corollary, env-example (inside .workedexample with env-solution), env-remark, env-proof, env-caution, env-strategy; NO env-exercise (the handout ships no exercises). §4.4 uses env-definition (Definition 4.3), env-theorem (Theorems 4.9-4.12), env-caution (Theorem A interior caution, unnumbered), env-strategy (Strategy 4.2), env-remark (Remark 4.4), env-corollary (Corollary 4.3), env-example/env-solution (Examples 4.2-4.4), env-proof; their bodies auto-italicize where applicable.
- Qualified proofs keep env-kicker "Proof"; env-name carries any qualifier. House style, not a finding. Caution is UNNUMBERED (matches ch02-ch04 precedent).
- Math (MathJax 4): inline \\(...\\), display \\[...\\], multi-line \\begin{aligned}; \\lvert..\\rvert, \\tfrac, \\frac, \\le/\\ge, \\mathbb{R} all render (verified: 0 MathJax errors, 22 print pages total, 0 overflow).
- Manual numbering: env-num / sec-no; per-type counters CONTINUE Chapter 4 across sections (see NUMBERING NOTE above).
- Cross-references: plain prose ("by the extreme value theorem (Theorem 4.9)", "by Theorem 4.10", "Corollary 4.3", "Theorem 4.8", "Chapter 3") -- NO \\cref, NO hyperlinks.
- Expansion markers: <!-- expansion:category --> HTML comment before each non-seed addition; valid categories: history, application, formula, summary, figure, example, intuition, strategy, caution. Seed-derived theorems/proofs correctly carry no expansion marker.
=== END HTML WRITING RULES ===

Now review the DRAFT against the SEED, DIRECTION BRIEF, and HTML WRITING RULES. Return strict JSON.
"""

parts = [
    HEADER,
    "=== SEED (manuscript transcription, pp.11-18) ===\n\n" + seed + "\n=== END SEED ===\n",
    "=== DIRECTION BRIEF (approved at gate 3) ===\n\n" + brief + "\n=== END DIRECTION BRIEF ===\n",
    "=== DRAFT (HTML fragment to review) ===\n\n" + draft + "\n=== END DRAFT ===\n",
    RULES,
]
OUT.write_text("\n".join(parts), encoding="utf-8")
print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")
