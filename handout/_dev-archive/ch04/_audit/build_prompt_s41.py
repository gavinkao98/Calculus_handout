#!/usr/bin/env python3
"""Assemble the Codex gate-2 auditor prompt for §4.1 (mirrors ch03 _audit/build_prompt_s3*.py).
Reads seed + brief + draft + the Chapter 4 FIGS entry, wraps with header / figure note /
HTML rules / final instruction, writes prompt_s41.txt. Run: python build_prompt_s41.py"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SEED = ROOT / "handout/_dev-archive/ch04/seed_ch04_s1.md"
BRIEF = ROOT / "handout/_dev-archive/ch04/brief_s41.md"
DRAFT = ROOT / "handout/fragments/ch04/sec-4-1.html"
STANDALONE = ROOT / "handout/chapter4-print-standalone.html"
OUT = Path(__file__).resolve().parent / "prompt_s41.txt"

seed = SEED.read_text(encoding="utf-8")
brief = BRIEF.read_text(encoding="utf-8")
draft = DRAFT.read_text(encoding="utf-8")

m = re.search(r"  const FIGS = \{.*?\n  \};", STANDALONE.read_text(encoding="utf-8"), re.DOTALL)
figs = m.group(0) if m else "(FIGS block not found)"

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

Numbering note: this is Chapter 4's FIRST section, so all per-type counters start fresh (Definition 4.1; Theorem 4.1 Completeness, 4.2 convergence; Strategy 4.1; Example 4.1; Figure 4.1; Remark 4.1; Caution unnumbered) -- that is correct, not a discontinuity.

Chapter-opener note: the chapter opener (a separate <article> with chapter-head) carries chapter-WIDE learning objectives that mention §4.2-§4.5 topics (continuity, the exponent law, the rigorous derivative with the bound |(e^h-1)/h - 1| <= |h|, Rolle/MVT, ln x). This is brief-mandated chapter infrastructure (brief §B.2), NOT preview-creep into the §4.1 body. Do NOT flag the opener's whole-chapter objectives as out-of-scope.

Scope note for this section: the SEED is scoped to §4.1 (manuscript pp.1-3) and DELIBERATELY ends at the partial-sum tail bound. The draft adds, as MARKED expansions sanctioned by the brief (§D) and cross-checked against the signed legacy ground truth: the value of e (e ~= 2.71828), a partial-sums worked example (Example 4.1), the convergence figure (Figure 4.1), a "series defines, doesn't derive" Caution, a geometric-tail Strategy box, and an R-vs-Q Remark. Completeness (Theorem 4.1) is stated WITHOUT proof (manuscript calls it a "Property"; proving it is out of scope -- do NOT demand a proof). The irrational a^r question is fenced to §4.5 in one line. e^x is DEFINED for x>0 here; x<0 is deferred to §4.2. These are intended, not drift.

Set "converged": true when there are ZERO blocking findings (math correct, faithful to seed, conforms to direction brief), even if advisory formatting nits remain.

Return STRICT JSON only, no prose outside the JSON.
"""

FIG_NOTE = """=== FIGURE RENDERING NOTE ===
This section HAS one figure, Figure 4.1 (partial sums of the exponential series converging to e^x), rendered from the entry "partial-sums-exp" in the Chapter 4 figure registry (embedded below). It uses buildPlot() (a function-graph plotter). Do NOT report "figure missing": the figure exists and renders (verified: ready=true, 0 MathJax errors, figure hydrated, 6 print pages, 0 overflow).

GROUND TRUTH for Figure 4.1:
  Blue curve = e^x (cls "curve"). Gray curves = the partial sums P_k(x) = sum_{n=0}^k x^n/n! for k = 1,2,3,4 (cls "bubble"). All pass through (0,1) = e^0 (marked with a dot). Window x in [-2.1, 1.55], y in [-0.6, 4.6]. For x < 0 the low-order partial sums oscillate around e^x (this is the correct behaviour of the alternating partial sums and is intentional -- it previews why x<0 is harder, handled in §4.2); near x = 0 and for x > 0 they rise to meet e^x. Labels are limited to e^x and P_1 (label economy, CONTENT_SPEC §10). Plain SVG/foreignObject text labels are accepted house style and must NOT be flagged.

--- BEGIN Chapter 4 FIGS (the only entry is partial-sums-exp used by Figure 4.1) ---
""" + figs + """
--- END Chapter 4 FIGS ---
=== END FIGURE NOTE ===
"""

RULES = """=== KEY HTML WRITING RULES (advisory -- for house_rule findings) ===
- Semantic env classes: env-definition, env-theorem, env-proposition, env-corollary, env-example (inside .workedexample with env-solution), env-remark, env-proof, env-caution, env-strategy; NO env-exercise (the handout ships no exercises)
- Math (MathJax 4): inline \\(...\\), display \\[...\\], multi-line \\begin{aligned}...\\end{aligned}; \\tag{$*$}, \\binom, \\underbrace, \\lvert..\\rvert all render
- Manual numbering: env-num / fig-no / sec-no; per-type counters fresh for Chapter 4 (Definition 4.1; Theorem 4.1/4.2; Strategy 4.1; Example 4.1; Figure 4.1; Remark 4.1; Caution unnumbered)
- Cross-references: plain prose ("by Theorem 4.1", "the bound (*)", "§4.2", "§4.5", "Chapter 2") -- NO \\cref, NO hyperlinks
- Expansion markers: <!-- expansion:category --> HTML comment before each non-seed addition; valid categories: history, application, formula, summary, figure, example, intuition, strategy, caution
- The chapter opener (a separate <article>) and seed-derived definition/theorems/proofs are NOT seed-expansions and correctly carry no expansion marker
=== END HTML WRITING RULES ===

Now review the DRAFT against the SEED, DIRECTION BRIEF, FIGURE NOTE, and HTML WRITING RULES. Return strict JSON.
"""

parts = [
    HEADER,
    "=== SEED (manuscript transcription) ===\n\n" + seed + "\n=== END SEED ===\n",
    "=== DIRECTION BRIEF (approved at gate 3) ===\n\n" + brief + "\n=== END DIRECTION BRIEF ===\n",
    "=== DRAFT (HTML fragment to review) ===\n\n" + draft + "\n=== END DRAFT ===\n",
    FIG_NOTE,
    RULES,
]
OUT.write_text("\n".join(parts), encoding="utf-8")
print(f"wrote {OUT} ({OUT.stat().st_size} bytes); FIGS embedded: {'yes' if m else 'NO'}")
