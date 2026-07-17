#!/usr/bin/env python3
"""Assemble the Codex gate-2 auditor prompt for §4.5 (mirrors build_prompt_s44.py).
Reads seed + brief + draft, wraps with header / §4.5 scope notes / HTML rules / final
instruction, writes prompt_s45.txt. §4.5 HAS a figure (Figure 4.3, the e^x/ln x
reflection across y=x), JS-rendered from the chapter FIGS registry; the auditor reviews
the figure CAPTION and the geometric claim, not a pixel image. Run: python build_prompt_s45.py"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SEED = ROOT / "handout/_dev-archive/ch04/seed_ch04_s5.md"
BRIEF = ROOT / "handout/_dev-archive/ch04/brief_s45.md"
DRAFT = ROOT / "handout/fragments/ch04/sec-4-5.html"
OUT = Path(__file__).resolve().parent / "prompt_s45.txt"

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

This is the FINAL section of the chapter. Its core manuscript content is SHORT (define ln x as the inverse of e^x; prove ln continuous; derive (ln x)'=1/x), but it is EXPANSION-RICH: three Homework items were promoted to lettered results, plus a reflection figure, an application capstone, and a 4-strand chapter summary. So its risk has TWO faces: (1) the two manuscript proofs (continuity, derivative) must be RIGOROUS and unbroken; (2) the expansions must stay within the approved scope and not smuggle in forbidden material (a rigorous proof of the range of e^x; a full table of logarithm laws; the multi-step Cauchy functional-equation proof). Spend your effort on the MATH of the two proofs + the promoted results, and on direction-conformance. Re-derive each step INDEPENDENTLY:
  - Theorem 4.13 (ln continuous), proof by contradiction: negating continuity at x0>0 yields delta>0 and a sequence y_j -> x0 (all in (0,inf)) with |ln y_j - ln x0| >= delta for all j. Each j gives ln y_j <= ln x0 - delta OR ln y_j >= ln x0 + delta. Apply the strictly increasing e^x: case 1 gives x0 - y_j = e^{ln x0} - e^{ln y_j} >= e^{ln x0} - e^{ln x0 - delta} > 0; case 2 gives y_j - x0 >= e^{ln x0 + delta} - e^{ln x0} > 0. With epsilon = min of the two (strictly positive) gaps, |y_j - x0| = |e^{ln y_j} - e^{ln x0}| >= epsilon for all j, contradicting y_j -> x0. CHECK every inequality direction, that epsilon is genuinely > 0, that the identity y_j = e^{ln y_j} is used correctly, and that the contradiction actually follows.
  - Theorem 4.14 ((ln x)' = 1/x), inverse-function technique: with y0 = ln x, y = ln(x+h), one has e^{y0}=x, e^y=x+h, so e^y - e^{y0} = h; then (ln(x+h)-ln x)/h = (y-y0)/(e^y-e^{y0}) = 1/[(e^y-e^{y0})/(y-y0)]. The flip requires y != y0, justified because ln is strictly increasing (inverse of strictly increasing e^x), so h != 0 forces y != y0. As h->0, continuity of ln (Thm 4.13) gives y->y0 (and y != y0 throughout), so the denominator -> (d/dy e^y)|_{y0} = e^{y0} = e^{ln x} = x (using Thm 4.8). Hence the derivative is 1/x. CHECK there is no division-by-zero gap, and that taking the reciprocal of the limit is legitimate (the inner limit is x != 0 since x>0).
  - Corollary 4.4 (f'=0 on (a,b) => f constant): MVT on [x1,x2] gives c with f(x2)-f(x1)=f'(c)(x2-x1)=0, so f(x2)=f(x1); f constant. Check.
  - Proposition 4.3 (ln(ab)=ln a+ln b): set f(x)=ln(ax)-ln x; f'(x) = a*(1/(ax)) - 1/x = 1/x - 1/x = 0 (chain rule + Thm 4.14); Corollary 4.4 => f constant on the closed interval between 1 and x; f(1) = ln a - ln 1 = ln a (using ln 1 = 0, since e^0 = 1); setting x=b gives ln(ab)-ln b = ln a. CHECK the chain-rule derivative of ln(ax), the ln 1 = 0 step, and that Corollary 4.4 (stated on a closed [a,b]) is legitimately applied to the closed interval with endpoints 1 and x regardless of which is larger.
  - Example 4.5 (general powers a^x := e^{x ln a}): (i) a^x b^x = e^{x ln a} e^{x ln b} = e^{x ln a + x ln b} = e^{x(ln a + ln b)} = e^{x ln(ab)} = (ab)^x (exponent law Thm 4.7 + product law Prop 4.3); (ii) ln(a^x) = ln(e^{x ln a}) = x ln a, so (a^x)^y = e^{y ln(a^x)} = e^{xy ln a} = a^{xy}, symmetric in x,y so = (a^y)^x. CHECK every exponent manipulation.
  - Definition 4.4 (ln x): the unique a with e^a = x (x>0); identities e^{ln x}=x (x>0) and ln(e^x)=x (all real x). Quantifiers correct. The range of e^x = (0,inf) is ASSERTED, not proved; the draft must NOT smuggle in a proof of the two limits / surjectivity (it states a one-line dependency note only).
  - Remark 4.6 (Cauchy functional equation): "the only continuous g: R -> (0,inf) with g(x)g(y)=g(x+y) and g(1)=e is e^x" -- stated as a one-sentence remark with the proof OMITTED. The draft must NOT include the multi-step proof.
  - Application capstone: y'=ky => y = y(0) e^{kt}; t = (ln y* - ln y(0))/k; half-life t_half = ln 2 / |k| for the case y* = y(0)/2 (k<0). Check these formulas.
  - Figure 4.3 caption claim: the graphs of e^x and ln x are reflections across y = x, with (0,1) on e^x reflecting to (1,0) on ln x -- verify this is the correct geometric statement of the inverse relation, no false claim. (The figure itself is drawn by JS and renders cleanly; review the caption's mathematical claim, not an image.)
Cross-check the math against the SIGNED LEGACY GROUND TRUTH legacy/tex_handout/chapters/ch04_exponential_logarithm.tex, section \\subsection{Defining $\\ln x$} / \\subsection{Continuity of $\\ln x$} / \\subsection{The derivative of $\\ln x$} (labels def:logarithm, thm:ln-continuous, thm:ln-derivative-rigorous, fig:exp-and-log-reflection) plus the chapter Summary (\\section*{Summary}). NOTE on placement: the legacy puts the monotonicity Corollary and the sin/e^x examples at the START of §4.5; the handout (following the manuscript's page order and the chapter PLAN) already placed those at the END of §4.4. Therefore §4.5 here does NOT restate the monotonicity corollary or those examples -- it opens directly at the logarithm. Do NOT flag the absence of the monotonicity corollary from §4.5 as missing content.

NUMBERING NOTE: §4.5 is the chapter's LAST section. Per-type counters CONTINUE from §4.1-§4.4 (which used Definition 4.1-4.3; Theorem 4.1-4.12; Proposition 4.1/4.2; Corollary 4.1-4.3; Strategy 4.1/4.2; Example 4.1-4.4; Figure 4.1/4.2; Remark 4.1-4.4). Therefore §4.5 correctly uses: Definition 4.4 (natural logarithm); Theorem 4.13 (ln continuous), 4.14 ((ln x)'=1/x); Proposition 4.3 (logarithm product law); Corollary 4.4 (vanishing derivative => constant); Example 4.5 (general powers a^x); Figure 4.3 (e^x/ln x reflection); Remark 4.5 (rigorous vs Ch3 chain-rule), 4.6 (Cauchy functional equation); plus one UNNUMBERED Caution (ln only for x>0). §4.5 mints NO new Strategy and NO new Definition beyond 4.4. Cross-references ("Theorem 4.6" continuity of e^x, "Theorem 4.7" exponent law, "Theorem 4.8" derivative of e^x, "Theorem 4.12" MVT, "Corollary 4.3" monotonicity, "Example 4.4" e^x strictly increasing, "Chapter 3 / §3.3", "§4.1") are correct, not missing content. This continuation is CORRECT -- do NOT flag it as a discontinuity.

SCOPE / EXPANSION NOTE for §4.5: the SEED covers manuscript pp.18-22 (the block the manuscript heads "§ Logarithmic function": define ln's domain via lim e^x -> Definition of ln x -> continuity "Property" + contradiction proof -> differentiability + inverse-function proof -> (ln x)'=1/x) PLUS the chapter Homework pp.23-24 (HW1 f'=0=>const; HW2 ln(ab)=ln a+ln b; HW3 Cauchy functional equation; HW4 a^x:=e^{x ln a} exponent laws). The draft adds, as MARKED expansions sanctioned by the brief (gate 3 approved "全照提案核可" PLUS all THREE optional add-ons) and cross-checked against the signed legacy ground truth:
  - An OPENER framing strict monotonicity as the engine that both builds and powers the inverse, and closing BOTH forward fences -- Ch3 §3.3's informal ln and §4.1's deferred a^r for irrational r. INTENDED.
  - The range of e^x = (0,inf) ASSERTED with a one-line dependency note (continuity + the two limits + intermediate values), NOT proved. INTENDED (manuscript + legacy both assert).
  - An UNNUMBERED Caution that ln x is defined only for x>0 (ln 0, ln(-1) undefined since e^a>0). ROADMAP-mandated pitfall. INTENDED.
  - Figure 4.3 (the e^x/ln x reflection across y=x, ROADMAP key figure) with caption. INTENDED.
  - Remark 4.5 contrasting this rigorous derivation with Ch3 §3.3's chain-rule pass (which presupposed differentiability), closing that forward-reference loop. ROADMAP prerequisite. INTENDED.
  - Corollary 4.4 = HW1 (f'=0 => constant) promoted, placed just before the logarithm laws that use it. INTENDED.
  - Proposition 4.3 = HW2 (ln(ab)=ln a+ln b) promoted to a NAMED result (optional add-on (c): a named Proposition rather than a worked example). INTENDED.
  - Example 4.5 = HW4 (general powers a^x := e^{x ln a}, exponent laws (i)(ii)) promoted, closing §4.1's deferred a^r question. INTENDED.
  - Remark 4.6 = HW3 (Cauchy functional equation) retained as a ONE-SENTENCE remark with the proof OMITTED (optional add-on (b)). INTENDED.
  - A short application capstone (exponential growth/decay, the y=y0 e^{kt} model, half-life ln2/|k|), optional add-on (a). INTENDED.
  - A chapter-level 4-strand Summary (exponential / real-analysis machinery / existence theorems / logarithm). INTENDED (this is the chapter's final section).
These are INTENDED expansions, not drift.

DELIBERATELY OMITTED (brief 刻意不寫) -- these MUST NOT appear in the §4.5 body; flag as blocking direction-conformance ONLY if they actually appear:
  - the INTEGRAL definition of ln (ln x = integral of dt/t) -- this book builds ln as the inverse of e^x; mixing routes would contradict the manuscript;
  - the general logarithm log_b x or change-of-base formulas;
  - a full logarithm-law TABLE beyond the product law (manufactured ln(a/b)=ln a-ln b, ln(a^r)=r ln a) -- only ln(ab) (HW2) is in scope;
  - a RIGOROUS PROOF of the range of e^x / the two limits / surjectivity (must stay asserted with a one-line note);
  - the complex logarithm;
  - the MULTI-STEP proof of HW3's Cauchy functional equation (must stay a one-sentence remark, proof omitted);
  - Taylor's theorem / L'Hopital for ln, or the integral of ln;
  - REWRITING Chapter 3 §3.3's informal ln (only a cross-reference is allowed; the chapter does not edit Ch3);
  - a full monotonicity/concavity curve analysis of ln (the reflection figure suffices);
  - any self-invented "your turn" / bare exercise (the Homework items are promoted only as worked results, never as bare exercises);
  - OVER-EXPANSION: padding the final section. NOTE: a definition + two proofs + one promoted corollary + one promoted proposition + one promoted example + one figure + two remarks + one caution + one short application paragraph + a 4-strand chapter summary is the APPROVED scope (gate 3 took all three optional add-ons), NOT over-expansion. Only flag genuinely redundant lemmas/examples/cautions beyond that.

This section HAS one figure (Figure 4.3, the e^x/ln x reflection across y=x; ROADMAP key figure). It is drawn by the chapter's JS figure registry and renders cleanly (verified: 0 MathJax errors, 28 print pages for the chapter, 0 overflow; e^x in blue and ln x in red are mirror images across the dashed y=x line, with the (0,1)<->(1,0) reflected pair marked). Do NOT report "figure missing"; review only the figure CAPTION's mathematical claim.

Set "converged": true when there are ZERO blocking findings (math correct, faithful to seed, conforms to direction brief), even if advisory formatting nits remain.

Return STRICT JSON only, no prose outside the JSON.
"""

RULES = """=== KEY HTML WRITING RULES (advisory -- for house_rule findings) ===
- Semantic env classes: env-definition, env-theorem, env-proposition, env-corollary, env-example (inside .workedexample with env-solution), env-remark, env-proof, env-caution, env-strategy; NO env-exercise (the handout ships no exercises). §4.5 uses env-definition (Definition 4.4), env-caution (ln-domain, unnumbered), env-theorem (Theorems 4.13/4.14), env-proof, env-remark (Remarks 4.5/4.6), env-corollary (Corollary 4.4), env-proposition (Proposition 4.3), env-example/env-solution (Example 4.5); their bodies auto-italicize where applicable.
- Qualified proofs keep env-kicker "Proof"; env-name carries any qualifier. House style, not a finding. Caution is UNNUMBERED (matches ch02-ch04 precedent).
- Math (MathJax 4): inline \\(...\\), display \\[...\\], multi-line \\begin{aligned}; \\lvert..\\rvert, \\tfrac, \\frac, \\le/\\ge, \\mathbb{R}, \\ln all render (verified: 0 MathJax errors, 28 print pages total, 0 overflow).
- Manual numbering: env-num / sec-no; per-type counters CONTINUE Chapter 4 across sections (see NUMBERING NOTE above).
- Cross-references: plain prose ("by Theorem 4.13", "Theorem 4.8", "the Mean Value Theorem (Theorem 4.12)", "Corollary 4.4", "Chapter 3", "§4.1") -- NO \\cref, NO hyperlinks.
- Expansion markers: <!-- expansion:category --> HTML comment before each non-seed addition; valid categories: history, application, formula, summary, figure, example, intuition, strategy, caution. Seed-derived theorems/proofs correctly carry no expansion marker.
=== END HTML WRITING RULES ===

Now review the DRAFT against the SEED, DIRECTION BRIEF, and HTML WRITING RULES. Return strict JSON.
"""

parts = [
    HEADER,
    "=== SEED (manuscript transcription, pp.18-22 + Homework pp.23-24) ===\n\n" + seed + "\n=== END SEED ===\n",
    "=== DIRECTION BRIEF (approved at gate 3) ===\n\n" + brief + "\n=== END DIRECTION BRIEF ===\n",
    "=== DRAFT (HTML fragment to review) ===\n\n" + draft + "\n=== END DRAFT ===\n",
    RULES,
]
OUT.write_text("\n".join(parts), encoding="utf-8")
print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")
