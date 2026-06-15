# Assemble the Codex audit prompt for §3.3 by splicing the real source files
# (seed / brief / draft) between fixed header, figure-note, and rules sections.
# Reading the sources from disk keeps UTF-8 + LaTeX backslashes faithful (the
# reason the kickoff forbids heredoc / PowerShell-pipe assembly).
# Mirrors build_prompt_s32.py; §3.3 has NO figure, so the figure note says so.
import io, os

HERE = os.path.dirname(os.path.abspath(__file__))
CH03 = os.path.dirname(HERE)

def rd(p):
    with io.open(p, "r", encoding="utf-8") as f:
        return f.read().rstrip("\n")

seed  = rd(os.path.join(CH03, "seed_ch03_s3.md"))
brief = rd(os.path.join(CH03, "brief_s33.md"))
draft = rd(os.path.join(CH03, "sec-3-3.html"))

HEADER = r"""You are an ADVISORY adversarial reviewer of a calculus handout section (HTML format) that was expanded from the SEED below, following an approved DIRECTION BRIEF. You do NOT rewrite; you surface findings for a human.

This section, §3.3 "Applications of the Chain Rule", is the chapter's FINAL section. It applies the already-proven chain rule (Theorem 3.3, §3.2) to derive, as WORKED EXAMPLES, the derivatives of ln x, x^x (logarithmic differentiation), 2^x, x ln x - x, arcsin, arccos, and arctan. Scrutinize the mathematics hard: every derivation must reach the correct standard result with each step justified.

Hunt especially for:
(a) mathematical errors, fabricated theorems/identities, or over-generalized claims -- re-derive each of the seven results independently and check the draft line by line (especially: the sign of the square root in arcsin'/arccos', fixed by cos x >= 0 on [-pi/2, pi/2] resp. sin x >= 0 on [0, pi]; the Pythagorean step sec^2 = 1 + tan^2 in arctan'; the product-rule step in x^x and x ln x - x; the e^{x ln 2} rewrite in 2^x; the stated domains, open vs closed);
(b) drift from the seed's mathematics (the seed IS the manuscript's mathematical backbone; the inverse-function derivatives MUST follow the manuscript's composition-identity route -- differentiate an identity such as e^{ln x}=x or arcsin(sin x)=x and solve -- NOT an implicit-differentiation framework, and NOT a rigorous construction of ln);
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

A mathematically equivalent paraphrase is NOT a finding. Numbering note: this is §3.3, the chapter's THIRD and final section; per-type counters CONTINUE from §3.2 -- Example 3.6 through 3.12, Strategy 3.2, Remark 3.3, and an unnumbered Caution. §3.3 INTENTIONALLY mints NO new Theorem, Proposition, Definition, or Figure (its results are framed as worked examples, per the manuscript and the numbering ledger); the next free Theorem/Proposition 3.4, Definition 3.2, and Figure 3.3 are deliberately left unused. This is correct, not a discontinuity.

Set "converged": true when there are ZERO blocking findings (math correct, faithful to seed, conforms to direction brief), even if advisory formatting nits remain.

Return STRICT JSON only, no prose outside the JSON."""

FIG_NOTE = r"""=== FIGURE RENDERING NOTE ===
This section has NO figure -- this is intentional (decided at gate 3). The chapter's two figures are complete (Figure 3.1 sector-inequality in §3.1; Figure 3.2 composed-mapping in §3.2); the ROADMAP assigns no §3.3 figure, and the manuscript's sin<->arcsin / cos<->arccos reflection graphs illustrate the Chapter-1 inverse-function DEFINITION, not the derivative technique, so they are recalled in prose rather than redrawn here. Do NOT report "figure missing" or "Figure 3.3 missing": the absence is deliberate, and no figures.js entry is expected for this section.
=== END FIGURE NOTE ==="""

RULES = r"""=== KEY HTML WRITING RULES (advisory -- for house_rule findings) ===
- Semantic env classes: env-definition, env-theorem, env-proposition, env-corollary, env-example (inside .workedexample with env-solution), env-exercise, env-remark, env-proof, env-caution, env-strategy
- Math: inline \(...\), display \[...\], multi-line \begin{aligned}...\end{aligned}
- Manual numbering: env-num for examples/strategy/remark etc., sec-no for section numbers
- Per-type counters CONTINUE across Chapter 3: §3.3 has Example 3.6-3.12, Strategy 3.2 (continuing Strategy 3.1 from §3.2), Remark 3.3; Caution is unnumbered. NO new Theorem/Proposition/Definition/Figure is minted in §3.3 (intentional -- see numbering note).
- Cross-references: plain prose ("by the chain rule (Theorem 3.3)", "sin' = cos (Theorem 3.1)", "Example 3.2", "Chapter 2, §2.4, Theorem 2.5", "Chapter 2, §2.5, Theorem 2.6", "Chapter 1") -- NO \cref, NO hyperlinks
- Expansion markers: <!-- expansion:category --> HTML comment before each non-seed addition
- The seed-derived applications (ln, x^x, arcsin) rendered as worked examples are the section's manuscript backbone; only additions beyond the seed carry expansion markers
- No \cref, no auto-numbering, no \index

=== APPROVED DIRECTION DECISIONS (do NOT mis-flag these as errors or omissions) ===
- RESULTS-AS-EXAMPLES (approved at gate 3): the derivative results (ln', x^x', 2^x', (x ln x - x)', arcsin', arccos', arctan') are INTENTIONALLY framed as WORKED EXAMPLES (env-example + env-solution), NOT as numbered Theorems/Propositions. Do NOT flag "this should be a theorem" or "missing Proposition"; citability is provided by the chapter-summary recap.
- D8 (ln informal): ln x is INTENTIONALLY used informally as the inverse of e^x (only the relation e^{ln x}=x is used); its rigorous construction is deferred to Ch4 §4.5 with a one-line forward fence in Example 3.6. This is deliberate -- do NOT flag the absence of a rigorous ln construction, and do NOT call the informal use an error or circularity. (The standing assumption that ln and the inverse-trig functions are differentiable is the manuscript's chosen rigor level; the chain rule itself was already proven in §3.2.)
- D10 (no implicit differentiation): the inverse-function derivatives INTENTIONALLY follow the manuscript's composition-identity route (differentiate an identity, then solve), with NO implicit-differentiation framework or vocabulary. This is the correct, intended method -- do NOT ask for implicit differentiation. The §3.1 opener's phrase "inverse and implicitly defined functions" is pre-shipped §3.1 text; §3.3 satisfies the "implicit" sense loosely via logarithmic differentiation of x^x and introduces no implicit-diff section.
- tan' and sec' are NOT re-derived here: they were done in §3.1 Example 3.2(a)(b). Example 3.12 (arctan') only USES tan' = sec^2 (cited to §3.1 Example 3.2) plus the Pythagorean identity 1 + tan^2 = sec^2. Do NOT flag tan'/sec' as missing or as needing re-derivation.
- INVERSE-TRIG DEFINITIONS are recalled in prose and cross-referenced generically to "Chapter 1" (arcsin/arccos/arctan are DEFINED in Ch1 §1.2; Ch1's HTML is not yet drafted, so this generic prose cross-ref intentionally resolves to no env-num). Do NOT flag this as a dangling reference or a missing Definition; §3.3 deliberately does not re-mint these definitions.
- arctan' (Example 3.12) is SELF-AUTHORED (approved at gate 3) to honor two already-shipped promises -- the Chapter-3 opener (sec-3-1) and the §3.2 closing paragraph both name arctan -- plus the ROADMAP core skill. It uses ONLY the composition-identity method (arctan(tan x)=x) and inventory already in hand. This is intended, not fabrication.
- arccos' (Example 3.11) is a gate-3-approved promotion of a manuscript Homework item; it INTENTIONALLY uses the CORRECT identity arccos(cos x)=x on [0, pi] (NOT the manuscript's loose, unrestricted "cos^{-1}(cos y)=y", which the ①-verify step flagged as a manuscript slip and the author corrected with the user's authorization). 2^x' (Example 3.8) and (x ln x - x)' (Example 3.9) are likewise gate-3-approved Homework promotions.
- 2^x via 2^x = e^{x ln 2} (a forward chain-rule application) and (x ln x - x)' via the product rule are deliberately the simplest correct routes; the general formula d/dx a^x = a^x ln a is stated in prose (not minted as a theorem) and the recap displays it -- intended, not over-generalization.
- The chapter summary at the end (results recap + the §3.1/§3.2/§3.3 arc + the forward reference to Ch4 §4.3/§4.5 and the Mean Value Theorem) is the FINAL section's duty; it names Ch4's role without previewing MVT mechanics. This is intended.
=== END HTML WRITING RULES ===

Now review the DRAFT against the SEED, DIRECTION BRIEF, FIGURE NOTE, and HTML WRITING RULES. Return strict JSON."""

parts = [
    HEADER,
    "=== SEED (manuscript transcription) ===\n\n" + seed + "\n\n=== END SEED ===",
    "=== DIRECTION BRIEF (approved at gate 3) ===\n\n" + brief + "\n\n=== END DIRECTION BRIEF ===",
    "=== DRAFT (HTML fragment to review) ===\n\n" + draft + "\n\n=== END DRAFT ===",
    FIG_NOTE,
    RULES,
]
out = "\n\n".join(parts) + "\n"

dst = os.path.join(HERE, "prompt_s33.txt")
with io.open(dst, "w", encoding="utf-8", newline="\n") as f:
    f.write(out)
print("wrote", dst, "(%d chars, %d lines)" % (len(out), out.count("\n") + 1))
