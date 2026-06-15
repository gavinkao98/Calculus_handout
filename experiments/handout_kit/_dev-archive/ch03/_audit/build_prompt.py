# Assemble the Codex audit prompt for §3.1 by splicing the real source files
# (seed / brief / draft / figures.js) between fixed header, figure-note, and
# rules sections. Reading the sources from disk keeps UTF-8 + LaTeX backslashes
# faithful (the reason the kickoff forbids heredoc / PowerShell-pipe assembly).
import io, os

HERE = os.path.dirname(os.path.abspath(__file__))
CH03 = os.path.dirname(HERE)
KIT = os.path.dirname(CH03)

def rd(p):
    with io.open(p, "r", encoding="utf-8") as f:
        return f.read().rstrip("\n")

seed  = rd(os.path.join(CH03, "seed_ch03_s1.md"))
brief = rd(os.path.join(CH03, "brief_s31.md"))
draft = rd(os.path.join(CH03, "sec-3-1.html"))
figjs = rd(os.path.join(CH03, "figures.js"))

HEADER = r"""You are an ADVISORY adversarial reviewer of a calculus handout section (HTML format) that was expanded from the SEED below, following an approved DIRECTION BRIEF. You do NOT rewrite; you surface findings for a human.

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

A mathematically equivalent paraphrase is NOT a finding. Numbering note: this is Chapter 3's first section, so all per-type counters start fresh at 3.1 (that is correct, not a discontinuity).

Set "converged": true when there are ZERO blocking findings (math correct, faithful to seed, conforms to direction brief), even if advisory formatting nits remain.

Return STRICT JSON only, no prose outside the JSON."""

FIG_NOTE = r"""=== FIGURE RENDERING NOTE ===
This section HAS one figure, Figure 3.1 (the sector inequality on the unit circle), rendered from the entry "sector-inequality" in exp-ch03/figures.js. The figure source is embedded below so you can review it as if rendered. Do NOT report "figure missing": the figure exists and renders (verified: 0 KaTeX errors). Plain SVG <text> labels in the figure are accepted house style (CONTENT_SPEC label-economy + the §2.5 precedent) and must NOT be flagged.

GROUND TRUTH for Figure 3.1 (verified by the user against the manuscript scan, p.3):
  O = circle centre; A = (1,0) on the circle and the x-axis; B = (cos T, sin T) at angle T;
  C = (1, tan T), where radius OB extended meets the vertical tangent at A (so B lies on segment OC).
  Areas: triangle OAB = (1/2) sin T;  sector OAB = (1/2) T;  triangle OAC = (1/2) tan T  ( = OAB + corner ABC ).
  Correct ordering:  (1/2) sin T  <=  (1/2) T  <=  (1/2) tan T   ==>   cos T <= (sin T)/T <= 1.
  IMPORTANT: the seed's transcribed middle inequality "a_(triangle ABC) <= a_sector <= a_(triangle OAB)" was a manuscript / transcription SLIP. The draft deliberately uses the standard correct ordering above (approved at gate 3, see brief section C item 1). Do NOT flag the draft for departing from that slipped line; the departure is correct and intended.

--- BEGIN exp-ch03/figures.js (full; the only entry is sector-inequality used by Figure 3.1) ---"""

RULES = r"""=== KEY HTML WRITING RULES (advisory -- for house_rule findings) ===
- Semantic env classes: env-definition, env-theorem, env-proposition, env-corollary, env-example (inside .workedexample with env-solution), env-exercise, env-remark, env-proof, env-caution, env-strategy
- Math: inline \(...\), display \[...\], multi-line \begin{aligned}...\end{aligned}
- Manual numbering: env-num for theorems/propositions/examples etc., fig-no for figures, sec-no for section numbers
- Per-type counters start fresh for Chapter 3: Proposition 3.1/3.2, Theorem 3.1/3.2, Example 3.1/3.2/3.3, Figure 3.1, Remark 3.1; Caution is unnumbered
- Cross-references: plain prose ("by Proposition 3.2", "the squeeze theorem (§1.5)", "Chapter 1") -- NO \cref, NO hyperlinks
- Expansion markers: <!-- expansion:category --> HTML comment before each non-seed addition
- The chapter opener (a separate <article>) and seed-derived theorems/proofs are NOT seed-expansions and correctly carry no expansion marker
- No \cref, no auto-numbering, no \index
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

dst = os.path.join(HERE, "prompt_s31.txt")
with io.open(dst, "w", encoding="utf-8", newline="\n") as f:
    f.write(out)
print("wrote", dst, "(%d chars, %d lines)" % (len(out), out.count("\n") + 1))
