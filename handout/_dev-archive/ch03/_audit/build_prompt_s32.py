# Assemble the Codex audit prompt for §3.2 by splicing the real source files
# (seed / brief / draft / figures.js) between fixed header, figure-note, and
# rules sections. Reading the sources from disk keeps UTF-8 + LaTeX backslashes
# faithful (the reason the kickoff forbids heredoc / PowerShell-pipe assembly).
# Mirrors build_prompt.py (§3.1); only the section-specific text differs.
import io, os

HERE = os.path.dirname(os.path.abspath(__file__))
CH03 = os.path.dirname(HERE)

def rd(p):
    with io.open(p, "r", encoding="utf-8") as f:
        return f.read().rstrip("\n")

seed  = rd(os.path.join(CH03, "seed_ch03_s2.md"))
brief = rd(os.path.join(CH03, "brief_s32.md"))
draft = rd(os.path.join(CH03, "sec-3-2.html"))
figjs = rd(os.path.join(CH03, "figures.js"))

HEADER = r"""You are an ADVISORY adversarial reviewer of a calculus handout section (HTML format) that was expanded from the SEED below, following an approved DIRECTION BRIEF. You do NOT rewrite; you surface findings for a human.

This section, §3.2 "The Chain Rule", is the chapter's HIGHEST-RISK section: it contains a remainder-form proof of the chain rule (epsilon-delta tail bound). Scrutinize the mathematics hard.

Hunt especially for:
(a) mathematical errors, fabricated theorems/identities, or over-generalized claims;
(b) drift from the seed's mathematics (the seed IS the manuscript's mathematical backbone; the chain-rule proof must follow the manuscript's remainder-form chaining m1=g', m2=f'(g(x)), R3=m2*R1+R2(m1*h+R1(h)), NOT a substituted standard proof);
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

A mathematically equivalent paraphrase is NOT a finding. Numbering note: this is §3.2, the chapter's SECOND section; per-type counters CONTINUE from §3.1 (Theorem 3.3, Proposition 3.3, Example 3.4/3.5, Figure 3.2, Remark 3.2), while Definition 3.1 and Strategy 3.1 are the chapter's FIRST of their type (correct, not a discontinuity, because §3.1 used no Definition and no Strategy).

Set "converged": true when there are ZERO blocking findings (math correct, faithful to seed, conforms to direction brief), even if advisory formatting nits remain.

Return STRICT JSON only, no prose outside the JSON."""

FIG_NOTE = r"""=== FIGURE RENDERING NOTE ===
This section HAS one figure, Figure 3.2 (the chain rule as a composed mapping), rendered from the entry "composed-mapping" in exp-ch03/figures.js. The figure source is embedded below so you can review it as if rendered. Do NOT report "figure missing": the figure exists and renders (verified live in the kit: 0 KaTeX errors, SVG hydrated with all axes, arrows, and labels). Plain SVG <text> labels in the figure are accepted house style (CONTENT_SPEC label-economy + the §3.1/§2.5 schematic-SVG precedent) and must NOT be flagged.

WHAT Figure 3.2 SHOWS (a schematic, NOT a function plot): three stacked horizontal axes -- input x (top), intermediate u = g(x) (middle), output y = f(u) (bottom) -- drawn with their base points x0, u0, y0 aligned. A small increment h on the input axis is carried by g to a wider increment (about g'(x0)*h) on the u-axis, then by f to a wider one still (about f'(g(x0))*g'(x0)*h) on the y-axis: the increment widths GROW down the stack, picturing the two local slopes multiplying. The display stretch ratios drawn in the SVG are ILLUSTRATIVE ("about"); the exact algebra (net stretch = f'(g(x0))*g'(x0)*h) lives in the caption + body prose, which is correct first-order linear-approximation reasoning, NOT a false exactness claim. On-drawing labels are single symbols (x, u, y, h, x0, u0, y0) plus the two arrow factors (x g'(x0), x f'(g(x0))) -- label-economy compliant; do NOT flag as over- or under-labelled.

--- BEGIN exp-ch03/figures.js (full; contains the §3.1 "sector-inequality" entry AND the §3.2 "composed-mapping" entry used by Figure 3.2) ---"""

RULES = r"""=== KEY HTML WRITING RULES (advisory -- for house_rule findings) ===
- Semantic env classes: env-definition, env-theorem, env-proposition, env-corollary, env-example (inside .workedexample with env-solution), env-exercise, env-remark, env-proof, env-caution, env-strategy
- Math: inline \(...\), display \[...\], multi-line \begin{aligned}...\end{aligned}
- Manual numbering: env-num for theorems/propositions/definitions/examples etc., fig-no for figures, sec-no for section numbers
- Per-type counters CONTINUE across Chapter 3: §3.2 has Theorem 3.3, Proposition 3.3, Definition 3.1 (the chapter's FIRST Definition -- §3.1 used none, so 3.1 is correct), Example 3.4/3.5, Figure 3.2, Remark 3.2, Strategy 3.1 (the chapter's FIRST Strategy); Caution is unnumbered
- Cross-references: plain prose ("by Theorem 3.1", "the limit definition of §2.2", "Chapter 2", "§2.3 Theorem 2.1", "Figure 3.2") -- NO \cref, NO hyperlinks
- Expansion markers: <!-- expansion:category --> HTML comment before each non-seed addition
- The seed-derived statement and proof are NOT seed-expansions and correctly carry no expansion marker; only additions beyond the seed do
- No \cref, no auto-numbering, no \index

=== APPROVED DIRECTION DECISIONS (do NOT mis-flag these as errors or omissions) ===
- DEFINITION TREATMENT = Option B (approved at gate 3): the §2.2 limit definition of the derivative is INTENTIONALLY cross-referenced in prose and NOT re-stated as a new numbered Definition; only the remainder form is minted, as Definition 3.1. The equivalence of the two is Proposition 3.3. This is deliberate, not a missing definition.
- D6: the product rule (Ch2 §2.5) and "differentiable implies continuous" (Ch2 §2.3 Theorem 2.1) are INTENTIONALLY cross-referenced and NOT re-stated or re-proven (the manuscript re-proves them, but Chapter 2 already owns them). A one-sentence cross-ref is correct; do NOT flag the absence of these proofs.
- D7: applications (d/dx ln x, d/dx x^x, d/dy arcsin y, logarithmic differentiation) are INTENTIONALLY deferred to §3.3; §3.2 contains only a one-line forward reference NAMING them, with nothing computed. Do NOT flag these as missing.
- D10: implicit differentiation is INTENTIONALLY not introduced.
- The remainder-form proof INTENTIONALLY fills three gaps the manuscript leaves implicit -- (i) the m2*R1(h)/h -> 0 term, (ii) the two skipped epsilon-delta sub-steps (the epsilon bound from bullet (i) and the triangle inequality), (iii) the Def1<=>Def2 "easy to see" equivalence (now Proposition 3.3) -- each marked expansion:formula. These are APPROVED expansions faithful to the manuscript's method; do NOT flag them as either drift or as fabrication.
- Worked Examples 3.4 and 3.5 are self-authored (approved at gate 3), use ONLY derivatives available by §3.2 (sin/cos from §3.1, power rule from Ch2), and are written with full solutions. This is intended.
=== END HTML WRITING RULES ===

Now review the DRAFT against the SEED, DIRECTION BRIEF, FIGURE NOTE, and HTML WRITING RULES. Return strict JSON."""

parts = [
    HEADER,
    "=== SEED (manuscript transcription) ===\n\n" + seed + "\n\n=== END SEED ===",
    "=== DIRECTION BRIEF (approved at gate 3) ===\n\n" + brief + "\n\n=== END DIRECTION BRIEF ===",
    "=== DRAFT (HTML fragment to review) ===\n\n" + draft + "\n\n=== END DRAFT ===",
    FIG_NOTE + "\n" + figjs + "\n--- END exp-ch03/figures.js ---\n=== END FIGURE NOTE ===",
    RULES,
]
out = "\n\n".join(parts) + "\n"

dst = os.path.join(HERE, "prompt_s32.txt")
with io.open(dst, "w", encoding="utf-8", newline="\n") as f:
    f.write(out)
print("wrote", dst, "(%d chars, %d lines)" % (len(out), out.count("\n") + 1))
