#!/usr/bin/env python3
"""Assemble the Codex gate-2 auditor prompt for §4.3 (mirrors build_prompt_s42.py).
Reads seed + brief + draft, wraps with header / §4.3 scope notes / HTML rules / final
instruction, writes prompt_s43.txt. §4.3 has NO figure. Run: python build_prompt_s43.py"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SEED = ROOT / "handout/_dev-archive/ch04/seed_ch04_s3.md"
BRIEF = ROOT / "handout/_dev-archive/ch04/brief_s43.md"
DRAFT = ROOT / "handout/fragments/ch04/sec-4-3.html"
OUT = Path(__file__).resolve().parent / "prompt_s43.txt"

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

This is the SHORTEST, purely-deductive section of the chapter; its single risk is OVER-expansion, not missing content. Spend your effort on the MATH and on direction-conformance. Re-derive each step independently:
  - The difference-quotient factorization (e^{x+h} - e^x)/h = ((e^h - 1)/h) e^x via the exponent law e^{x+h} = e^x e^h (Theorem 4.7); the pull-out of the h-independent factor e^x reducing everything to lim_{h->0} (e^h - 1)/h.
  - Proposition 4.2: |(e^h - 1)/h - 1| <= |h| for 0 < |h| < 1/2. Check the index shift (e^h - 1)/h - 1 = sum_{n>=2} h^{n-1}/n!; the term-by-term absolute value and the factoring of one |h|; and ESPECIALLY the "trailing sum <= 1" step: |h|^{n-2} <= 1 (since |h| < 1, n >= 2), then sum_{n>=2} 1/n! <= sum_{n>=2} 1/2^{n-1} = 1 via n! >= 2^{n-1}. Verify n! >= 2^{n-1} for n >= 2, verify the geometric sum equals 1, and verify the chain actually yields <= |h|.
  - Theorem 4.8: bound => lim (e^h - 1)/h = 1 (squeeze, RHS |h| -> 0); pull e^x out of the limit; difference quotient -> 1 * e^x = e^x; differentiability on R.
  - Corollary 4.2: induction (e^x)^{(n)} = e^x, base = Theorem 4.8, step (e^x)^{(n+1)} = (e^x)' = e^x.
Cross-check the math against the SIGNED LEGACY GROUND TRUTH legacy/tex_handout/chapters/ch04_exponential_logarithm.tex §4.3 (label sec:rigorous-derivative-of-exp). NOTE: the legacy proof bounds the bracket via 1/(1-|h|) <= 2 on |h| <= 1/2; the handout instead uses n! >= 2^{n-1} giving sum 1/n! <= 1. BOTH are valid; the handout's self-contained route is the brief's §C-1 decision -- do NOT flag the divergence in proof style as an error.

NUMBERING NOTE: §4.3 is NOT the chapter's first section. Per-type counters CONTINUE from §4.1-§4.2 (which used Definition 4.1/4.2; Theorem 4.1-4.7; Proposition 4.1; Corollary 4.1; Strategy 4.1; Example 4.1; Figure 4.1; Remark 4.1/4.2). Therefore §4.3 correctly uses: Theorem 4.8 (derivative); Proposition 4.2 (the bound); Corollary 4.2 (higher derivatives); Remark 4.3. §4.3 mints NO new Definition (the derivative was defined in Chapter 2). This continuation is CORRECT -- do NOT flag it as a discontinuity. Cross-references ("Theorem 4.7", "Corollary 4.1", "Strategy 4.1", "Section 4.2", "Chapter 2") are correct, not missing content.

SCOPE / EXPANSION NOTE for §4.3: the SEED covers manuscript pp.10-11 (the section "The derivative of the exponential function": difference quotient -> reduce to lim(e^h-1)/h -> series Note bound <= |h| on (-1/2,1/2) -> d/dx e^x = e^x). The draft adds, as MARKED expansions sanctioned by the brief (decisions §C/§D, all approved at gate 3 with "全照提案核可") and cross-checked against the signed legacy ground truth §4.3:
  - An OPENER that cross-references Chapter 2's informal term-by-term derivation of (e^x)' = e^x and frames this section as the rigorous redo with an explicit bound. Chapter 2 is NOT edited (only referenced in prose). Do NOT demand the Ch2 cross-ref be removed, and do NOT flag it as editing Chapter 2.
  - The "bracket <= 1" detail (the manuscript only ASSERTS [1/2 + |h|/3! + ...] <= 1; the handout SUPPLIES the one-line geometric comparison). This is the brief's §C-1 fill -- INTENDED, not drift.
  - Proposition 4.2 NAMING the bound, and Remark 4.3 framing the bound as the rigorous (explicit-rate) upgrade of Chapter 2's "vanishes as h->0".
  - Corollary 4.2 (higher derivatives (e^x)^{(n)} = e^x) -- the manuscript stops at the first derivative; the handout adds the corollary on user direction (§C-3 approved). Do NOT flag it as out-of-scope.
  - ONE forward-hook sentence noting that slope = value makes e^x the model for y' = ky (solved by y = y(0) e^{kt}); the full ODE/half-life treatment is DEFERRED to the chapter end (§C-4 approved). This single sentence is sanctioned.
  - A LIGHT back-reference to Strategy 4.1 at the geometric-tail step (§C-5 approved).
These are INTENDED expansions, not drift.

DELIBERATELY OMITTED (brief 刻意不寫) -- these MUST NOT appear in the §4.3 body; flag as blocking direction-conformance ONLY if they actually appear:
  - the chain rule, or derivatives of composites d/dx e^{kx}, d/dx e^{g(x)} (that is Chapter 2/3 material; this section does only the base d/dx e^x). NOTE: writing y = y(0) e^{kt} as the SOLUTION of an ODE in the one sanctioned hook sentence is NOT differentiating a composite -- do not flag it.
  - constructing or differentiating ln x (that is §4.5);
  - Rolle's theorem / MVT / a proof that positive derivative implies increasing (that is §4.4; only a one-line forward-fence to it is allowed);
  - EDITING or restructuring Chapter 2 (only a plain-prose cross-reference is allowed);
  - a full ODE / half-life / compound-interest treatment (only the single forward-hook sentence is allowed);
  - re-proving §4.1 series convergence or the §4.2 exponent law (they are only CITED);
  - any self-invented "your turn" exercise;
  - OVER-EXPANSION: padding this shortest section beyond its single main line (one Proposition + one Theorem + one Corollary + one Remark + opener + closer). If the draft balloons with extra lemmas/examples/figures, flag as direction-conformance.

This section has NO figure (it is a proof section; no ROADMAP key figure); do NOT report "figure missing".

Set "converged": true when there are ZERO blocking findings (math correct, faithful to seed, conforms to direction brief), even if advisory formatting nits remain.

Return STRICT JSON only, no prose outside the JSON.
"""

RULES = """=== KEY HTML WRITING RULES (advisory -- for house_rule findings) ===
- Semantic env classes: env-definition, env-theorem, env-proposition, env-corollary, env-example (inside .workedexample with env-solution), env-remark, env-proof, env-caution, env-strategy; NO env-exercise (the handout ships no exercises). §4.3 uses env-proposition (Proposition 4.2), env-theorem (Theorem 4.8), env-corollary (Corollary 4.2), env-remark (Remark 4.3); their bodies auto-italicize where applicable.
- Qualified proofs keep env-kicker "Proof" with any qualifier in env-name; this is house style, not a finding.
- Math (MathJax 4): inline \\(...\\), display \\[...\\], multi-line \\begin{aligned}...\\end{aligned}; \\binom, \\lvert..\\rvert, sums all render (verified: 0 MathJax errors, 15 print pages total for the chapter, 0 overflow).
- Manual numbering: env-num / sec-no; per-type counters CONTINUE Chapter 4 across sections (see NUMBERING NOTE above).
- Cross-references: plain prose ("by Theorem 4.7", "Corollary 4.1", "Strategy 4.1", "Section 4.2", "Chapter 2") -- NO \\cref, NO hyperlinks.
- Expansion markers: <!-- expansion:category --> HTML comment before each non-seed addition; valid categories: history, application, formula, summary, figure, example, intuition, strategy, caution. Seed-derived theorems/proofs correctly carry no expansion marker.
=== END HTML WRITING RULES ===

Now review the DRAFT against the SEED, DIRECTION BRIEF, and HTML WRITING RULES. Return strict JSON.
"""

parts = [
    HEADER,
    "=== SEED (manuscript transcription, pp.10-11) ===\n\n" + seed + "\n=== END SEED ===\n",
    "=== DIRECTION BRIEF (approved at gate 3) ===\n\n" + brief + "\n=== END DIRECTION BRIEF ===\n",
    "=== DRAFT (HTML fragment to review) ===\n\n" + draft + "\n=== END DRAFT ===\n",
    RULES,
]
OUT.write_text("\n".join(parts), encoding="utf-8")
print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")
