#!/usr/bin/env python3
"""Assemble the Codex gate-2 auditor prompt for §4.2 (mirrors build_prompt_s41.py).
Reads seed + brief + draft, wraps with header / §4.2 scope notes / HTML rules / final
instruction, writes prompt_s42.txt. §4.2 has NO figure. Run: python build_prompt_s42.py"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SEED = ROOT / "handout/_dev-archive/ch04/seed_ch04_s2.md"
BRIEF = ROOT / "handout/_dev-archive/ch04/brief_s42.md"
DRAFT = ROOT / "handout/fragments/ch04/sec-4-2.html"
OUT = Path(__file__).resolve().parent / "prompt_s42.txt"

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

This is a heavy real-analysis section; spend your effort on the MATH. Re-derive each step independently:
  - Theorem 4.3 continuity for x>0: the three-piece split e^x - e^{x0} = (e^x - P_k(x)) + (P_k(x) - P_k(x0)) + (P_k(x0) - e^{x0}); that both x, x0 lie in (0, x0+1) given delta < min{x0/2, 1/2}; the < 3*epsilon bookkeeping; correct use of the §4.1 tail bound (*).
  - Theorem 4.4 Bolzano-Weierstrass: the peak-point argument, BOTH cases (infinitely many peaks => non-increasing subsequence bounded below => Theorem 4.1 part (2); finitely many peaks => strictly increasing subsequence bounded above => Theorem 4.1 part (1)).
  - Theorem 4.5 convergent <=> Cauchy: both directions; "Cauchy => bounded" via epsilon=1; "bounded => convergent subsequence" via BW; "Cauchy + convergent subsequence => convergent".
  - Proposition 4.1 ((triangle) absolute convergence => convergence): its Cauchy-tail proof.
  - Theorem 4.7 exponent law (the riskiest): the product split P_k(x)P_k(y) = (I) + (II) grouped by total degree l = i+j; the binomial collapse (I) = P_k(x+y); the (II) tail bound <= (2L)^{n0}/n0! * (1/2)^{k-n0} and whether k > n0 > 8L delivers the geometric ratio; the four-term telescope as an EXACT algebraic identity; the use of (**) at x+y with |x+y| <= 2L; the double limit k -> infinity then L -> infinity.
  - Corollary 4.1 positivity: e^x = (e^{x/2})^2 and e^x e^{-x} = 1.

NUMBERING NOTE: §4.2 is NOT the chapter's first section. Per-type counters CONTINUE from §4.1 (which used Definition 4.1; Theorem 4.1 Completeness, 4.2 convergence; Strategy 4.1; Example 4.1; Figure 4.1; Remark 4.1). Therefore §4.2 correctly uses: Definition 4.2 (Cauchy); Theorem 4.3 (continuity x>0), 4.4 (Bolzano-Weierstrass), 4.5 (Cauchy criterion), 4.6 (continuity on R), 4.7 (exponent law); Proposition 4.1 (absolute convergence); Corollary 4.1 (positivity); Remark 4.2; Caution unnumbered. This continuation is CORRECT -- do NOT flag it as a discontinuity. Cross-references back to §4.1 ("Theorem 4.1", "Theorem 4.2", "the bound (*)") are correct, not missing content.

SCOPE / EXPANSION NOTE for §4.2: the SEED covers manuscript pp.3-10 ([e2] continuity for x>0 through the exponent law and the closing Summary). The draft adds, as MARKED expansions sanctioned by the brief (decisions D3-1/D3-2/§C) and cross-checked against the SIGNED LEGACY GROUND TRUTH (legacy/tex_handout/chapters/ch04_exponential_logarithm.tex §4.2):
  - The FULL Bolzano-Weierstrass theorem + peak-argument proof, and the convergent<=>Cauchy proof. The manuscript explicitly PUNTS here ("we shall not prove this theorem"); the handout SUPPLIES the proof on user direction (D3-1). Do NOT flag the BW/Cauchy proof as out-of-scope, and do NOT demand that it be left unproved.
  - Theorem 4.6 (continuity on all of R) named explicitly (the manuscript states full-line continuity only in its closing Summary).
  - Corollary 4.1 (positivity e^x>0), Remark 4.2 (why x<0 is harder), and the Bolzano-Weierstrass-dependency Caution.
  - The exponent law is written as a FULL multi-step proof (D3-2), not an outline.
  - Binomial coefficients use \\binom with a one-time cross-reference to the manuscript's C^n_k notation (D8).
These are INTENDED expansions, not drift.

DELIBERATELY OMITTED (brief 刻意不寫) -- these MUST NOT appear in the §4.2 body; flag as blocking direction-conformance ONLY if they actually appear:
  - re-proving or re-stating the Completeness theorem (it is only cited as Theorem 4.1);
  - re-proving the §4.1 tail bound (only cited as (*));
  - the difference quotient (e^{x+h}-e^x)/h, the limit (e^h-1)/h, or (e^x)' beyond a one-line §4.3 forward-fence (that is §4.3);
  - ln x or irrational powers a^x = e^{x ln a} (that is §4.5);
  - a PROOF of the binomial theorem (it is a stated tool);
  - Rolle's theorem / MVT (that is §4.4);
  - any self-invented "your turn" exercise.

This section has NO figure (it is a proof section); do NOT report "figure missing".

Set "converged": true when there are ZERO blocking findings (math correct, faithful to seed, conforms to direction brief), even if advisory formatting nits remain.

Return STRICT JSON only, no prose outside the JSON.
"""

RULES = """=== KEY HTML WRITING RULES (advisory -- for house_rule findings) ===
- Semantic env classes: env-definition, env-theorem, env-proposition, env-corollary, env-example (inside .workedexample with env-solution), env-remark, env-proof, env-caution, env-strategy; NO env-exercise (the handout ships no exercises). §4.2 uses env-proposition (Proposition 4.1) and env-corollary (Corollary 4.1); their bodies auto-italicize.
- Qualified proofs keep env-kicker "Proof" with the qualifier in env-name (e.g. "Proof of Proposition 4.1"); this is house style, not a finding.
- Math (MathJax 4): inline \\(...\\), display \\[...\\], multi-line \\begin{aligned}...\\end{aligned}; \\tag{$*$}/\\tag{$**$}, \\binom, \\underbrace, \\substack, \\lvert..\\rvert all render (verified: 0 MathJax errors, 13 print pages, 0 overflow).
- Manual numbering: env-num / sec-no; per-type counters CONTINUE Chapter 4 across sections (see NUMBERING NOTE above). The tail bound (*) is §4.1's; (**) is §4.2's absolute-value upgrade.
- Cross-references: plain prose ("by Theorem 4.4", "the bound (*)", "§4.1", "§4.3", "Chapter 2") -- NO \\cref, NO hyperlinks
- Expansion markers: <!-- expansion:category --> HTML comment before each non-seed addition; valid categories: history, application, formula, summary, figure, example, intuition, strategy, caution. Seed-derived theorems/proofs correctly carry no expansion marker.
=== END HTML WRITING RULES ===

Now review the DRAFT against the SEED, DIRECTION BRIEF, and HTML WRITING RULES. Return strict JSON.
"""

parts = [
    HEADER,
    "=== SEED (manuscript transcription, pp.3-10) ===\n\n" + seed + "\n=== END SEED ===\n",
    "=== DIRECTION BRIEF (approved at gate 3) ===\n\n" + brief + "\n=== END DIRECTION BRIEF ===\n",
    "=== DRAFT (HTML fragment to review) ===\n\n" + draft + "\n=== END DRAFT ===\n",
    RULES,
]
OUT.write_text("\n".join(parts), encoding="utf-8")
print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")
