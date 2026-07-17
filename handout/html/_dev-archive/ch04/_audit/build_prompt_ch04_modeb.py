#!/usr/bin/env python3
"""Assemble the Codex gate-2 prompt for the WHOLE-CHAPTER Chapter 4 Mode B audit.
Embeds all five committed fragments (sec-4-1 .. sec-4-5) and frames a CROSS-SECTION
consistency review (the gate-1 free workflow already passed; this is the paid
second-model cross-check). Writes prompt_ch04_modeb.txt. Run: python build_prompt_ch04_modeb.py"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
FRAGDIR = ROOT / "handout/fragments/ch04"
OUT = Path(__file__).resolve().parent / "prompt_ch04_modeb.txt"

secs = {n: (FRAGDIR / f"sec-4-{n}.html").read_text(encoding="utf-8") for n in range(1, 6)}

HEADER = """You are a SECOND-MODEL adversarial reviewer performing a WHOLE-CHAPTER "Mode B" audit of Chapter 4 (sections 4.1-4.5) of an HTML calculus handout. Each section already passed its own per-section audit at authoring time, AND the whole chapter just passed a free first-pass cross-section audit (gate 1). YOUR JOB is an INDEPENDENT second-model cross-check focused on CROSS-SECTION CONSISTENCY and chapter-level coherence -- the things a per-section pass cannot see. You do NOT rewrite; you surface findings for a human.

Hunt for genuine CROSS-SECTION problems:
(a) NUMBERING & CROSS-REFERENCES: per-type counters (Definition/Theorem/Proposition/Corollary/Strategy/Example/Figure/Remark) must be unique-within-type and continuous chapter-wide with no gap/duplicate/skip; every prose cross-reference ("Theorem 4.x", "Corollary 4.y", "Proposition 4.z", "Example 4.v", "Figure 4.u", "Remark 4.s", "Strategy 4.t", "Definition 4.w", "Chapter N", "section N.m") must resolve to a target that ACTUALLY EXISTS and is correctly typed/named -- flag any dangling or mislabelled reference;
(b) NOTATION & TERMINOLOGY: symbols used consistently across sections (P_k partial sums, e constant vs e^x function, \\binom, \\lvert..\\rvert, extremum points x_M/x_m, increment h, inverse-function variables y/y_0); named results called the same name across sections (exponent law, Extreme Value Theorem, "Theorem A"/Interior Extremum, Mean Value Theorem); American spelling throughout; section-range form §X-§Y;
(c) CROSS-SECTION MATHEMATICS: a fact stated in one section and reused in another must be stated consistently (e.g. the bound |(e^h-1)/h - 1| <= |h| must carry its |h|<1/2 restriction everywhere it is precisely restated, including the chapter Summary; e^x>0; range of e^x = (0,infty); ln defined only for x>0; strict vs non-strict monotonicity); no hypothesis silently dropped on reuse; the dependency chain must be acyclic and no result used before it is established;
(d) REGISTER & FLOW: consistent voice/density across sections; section openers/closers connect (each closer hands off to the next opener); forward-fences and loop-closures are reciprocated (4.1 defers a^r-for-irrational-r -> 4.5 Example 4.5 closes it; Ch3 section 3.3 informal-ln loop -> 4.5 Remark 4.5 closes it);
(e) REDUNDANCY & GAPS: no UNINTENDED re-definition/re-proof across sections; nothing referenced but never established; no narrative promise ("we will show...") left undelivered.

FOUR-LEVEL TRIAGE -- tag EVERY finding, do NOT inflate:
  level 1 = REAL CONFLICT / violation of an established rule -> actionable (blocking=true)
  level 2 = discoverability gap (a doc/comment would help; NOT a contradiction)
  level 3 = editorial drift (low priority; not to fix now)
  level 4 = non-finding (semantically-equivalent wording, stylistic preference, example-coverage difference)
Only level 1 is blocking. OVER-REPORTING DILUTES THE REAL ITEMS -- be conservative. A semantically-equivalent paraphrase is NOT a finding. A richer phrasing in one section vs a leaner one elsewhere is NOT a conflict.

NUMBERING LEDGER (authoritative, manual, continuous across sections -- verify against this):
  Definition 4.1-4.4; Theorem 4.1-4.14; Proposition 4.1-4.3; Corollary 4.1-4.4; Strategy 4.1-4.2; Example 4.1-4.5; Figure 4.1-4.3; Remark 4.1-4.6; Caution UNNUMBERED.
  Theorem 4.1=Completeness, 4.7=exponent law, 4.8=(e^x)', 4.9=Extreme Value Theorem, 4.10=Interior Extremum "Theorem A", 4.11=Rolle, 4.12=MVT, 4.13=ln continuous, 4.14=(ln x)'=1/x; Corollary 4.3=monotonicity, 4.4=vanishing-derivative=>constant; Proposition 4.3=logarithm product law; Example 4.5=general powers a^x.

SETTLED DECISIONS -- do NOT report these as findings (deliberate, recorded in the chapter PLAN):
- The Mean Value Theorem lives in Chapter 4 (not moved out).
- The Extreme Value Theorem (Theorem 4.9) is stated WITHOUT proof -- deliberate.
- The monotonicity Corollary 4.3 and the sin / e^x examples are at the END of section 4.4 (not 4.5); section 4.5 opens directly at ln -- deliberate placement.
- Cauchy<=>convergent is EXPANDED to Bolzano-Weierstrass + monotone subsequence in 4.2; the exponent law is a full multi-step proof -- user-directed.
- Section 2.4 (Chapter 2, outside this chapter) derives (e^x)'=e^x informally and 4.3 re-derives it rigorously -- an INTENTIONAL spiral; section 4.4 Example 4.4 restating e^x>0 inline (rather than citing Corollary 4.1) is the deliberate fulfilment of brief item C-7. Do not flag these as duplication.
- ln x is defined only for x>0 -- deliberate.
- Section-range cross-references use the house form §X-§Y, NOT the double-section-sign §§ form. Caution boxes are unnumbered.

CONTEXT -- THE GATE-1 OUTCOME you are cross-checking (the fragments below are the CURRENT state, AFTER gate-1 fixes):
- Gate 1 found the chapter CLEAN (zero level-1) on numbering/cross-reference, cross-section mathematics, register/flow, and redundancy/gaps.
- Gate 1 found and FIXED two level-1 spelling conflicts (British->American): "behaviour"->"behavior" (sec 4.4) and "characterised"/"normalisation"->"characterized"/"normalization" (sec 4.5). The fragments below already contain the American forms; do not expect to see the old British spellings.
- Gate 1 REFUTED two level-1 candidates (you should INDEPENDENTLY agree or challenge): (i) the apostrophe glyph differs across sections -- curly U+2019 in 4.1/4.2 vs straight ASCII in 4.3/4.4/4.5 -- judged level-3 typography drift (and a book-wide spec-vs-practice conflict), not a chapter Mode B level-1; (ii) section 4.4 Example 4.4 re-derives e^x>0 inline instead of citing Corollary 4.1 -- judged a settled C-7 decision, not unintended duplication.
- Gate 1 noted one level-3 advisory: "extreme value theorem" is lowercase in running prose but Title Case as its env-name.

YOUR DELIVERABLE: independently audit the five fragments below for CROSS-SECTION level-1 conflicts. Specifically: (1) do you find ANY level-1 cross-section conflict gate-1 missed? (2) do you AGREE with the two refutations and the advisory, or do you judge any of them differently? Report every finding with category, blocking flag, level (1-4), and severity. Set "converged": true if and only if you find ZERO new level-1 cross-section conflicts (i.e. you agree the current chapter is cross-section-clean at level 1). Put your verdict on the two refuted items and the advisory in the "summary".

Return STRICT JSON only, no prose outside the JSON. category: math | faithfulness | direction-conformance | notation | numbering | register | redundancy | other. blocking=true ONLY for a genuine level-1 cross-section conflict.
"""

RULES = """=== HTML WRITING NOTES (context, not findings) ===
- Semantic env classes: env-definition/theorem/proposition/corollary/example (in .workedexample with env-solution)/remark/proof/caution/strategy. Caution is UNNUMBERED by house style. env-num carries the manual number.
- Math is MathJax (inline \\(..\\), display \\[..\\]); the chapter renders with 0 MathJax errors across 28 print pages (already verified) -- do NOT review rendering, only the cross-section CONTENT.
- Cross-references are plain prose citing manual numbers (no \\cref). HTML comments <!-- expansion:cat --> mark non-seed additions and are dev notes, not reader-facing prose.
=== END NOTES ===

Now perform the whole-chapter cross-section Mode B cross-check on the five fragments above. Return strict JSON.
"""

parts = [HEADER]
for n in range(1, 6):
    parts.append(f"=== FRAGMENT sec-4-{n}.html (section 4.{n}) ===\n\n" + secs[n] + f"\n=== END sec-4-{n}.html ===\n")
parts.append(RULES)
OUT.write_text("\n".join(parts), encoding="utf-8")
print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")
