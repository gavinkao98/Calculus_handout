<!--
Mode B narration-audit prompt TEMPLATE (reusable across sections).

USAGE: copy to PROMPT-<deck>-narration-modeB.md, fill the {{...}} placeholders,
then feed to the reviewer:
    codex exec -s read-only < PROMPT-<deck>-narration-modeB.md > REPORT-<deck>-narration-modeB.raw.txt 2>&1

1.2 (Inverse Trigonometric Functions)        e.g. "1.1 (Inverse Functions)"
video/content_scripts/ch01_inverse_trig.md      content script with the narration: field
video/content_scripts/ch01_inverse_trig_narration.html           Version A (HTML reading) path
video/content_scripts/ch01_inverse_trig_narration_spoken.md      Version B (spoken) path
no  "yes" if the narration content was already user-approved, else "no"
                      -> when "no", dimension D7 (math-content correctness) is REQUIRED.
-->
You are a **Mode B reviewer (審訂審查)** for a calculus teaching-video narration. You AUDIT and report findings; you do NOT edit any files.

# What you are reviewing

Section 1.2 (Inverse Trigonometric Functions), dual-version narration route. From one narration source, two derived versions:

1. **Source narration:** `video/content_scripts/ch01_inverse_trig.md` — the `narration:` field of each unit (English + inline LaTeX). Content was user-approved: **no**.
2. **Version A — HTML reading:** `video/content_scripts/ch01_inverse_trig_narration.html` — renders the math via MathJax.
3. **Version B — spoken (MiMo):** `video/content_scripts/ch01_inverse_trig_narration_spoken.md` — every LaTeX expression spelled into spoken English (no symbols) for a TTS that cannot read LaTeX.

Read all three. Silent units (intro/outro) have no narration — audit only the spoken units.

# Framing (project review norms — follow strictly)

- Separate four tiers; report only tiers 1–2: (1) real error / faithfulness break / would-not-render / math wrong; (2) genuine ambiguity or readability defect introduced by the transformation; (3) pure style/editorial drift → at most one line, low-priority; (4) non-findings (semantic-equivalent wording) → omit.
- Do NOT over-report; over-reporting dilutes real findings.
- If CONTENT_APPROVED is "yes": treat the source narration's teaching content/pedagogy as authorized; do not re-litigate it (but still run D7 if you spot an outright math error).

# Audit dimensions

**D1 — Faithfulness of Version A (HTML).** Each unit's narration text matches the source verbatim (markdown `*x*` → `<em>x</em>` ok); no dropped/added/altered words; no malformed LaTeX; correct kind badge; all units present, right ids/order.

**D2 — Faithfulness of Version B (spoken).** English prose word-for-word identical to source, only math notation converted to spoken words; flag any paraphrase/drop/addition or changed teaching content.

**D3 — Math naturalization correctness in Version B (HIGH PRIORITY).** Every spoken math rendering is (a) mathematically equivalent to the written math and (b) unambiguous to a listener with no symbols. Hunt: radical/power/fraction grouping scope; subscripts; inverse-function notation read as "… inverse" not a reciprocal (unless the text is deliberately discussing the `^{-1}` symbol); anything mis-hearable as a different expression. Quote source LaTeX + spoken form per issue.

**D4 — Register / readability of Version B.** Reads naturally aloud in a calm lecture register; no awkwardness from the spell-out; disambiguators like "the quantity …" used only where grouping truly needs it.

**D5 — Convention decisions.** Recommend one option (with a one-line reason) for any open reading-convention choice the spoken doc flags.

**D6 — TTS setup factual sanity.** The documented synth config (model/voice/format/sample rate/message shape) is internally consistent and plausible. Flag only clear internal inconsistencies.

**D7 — Math-content correctness no=no → REQUIRED; =yes → only flag outright errors.** Independently re-derive every numeric value, sign, interval endpoint, quadrant, and final result in the narration; confirm each matches the mathematics (not merely the spoken-vs-written equivalence of D3). Quote any discrepancy.

# Output (final message; write no files)

First line: `VERDICT: <X> blocking, <Y> advisory`.
Then findings: `- [Blocking|Advisory] [D#] unit-id — issue (quote exact text) → Verdict: Keep|Rewrite|Cut → exact replacement if Rewrite`.
Then `## Convention recommendations (D5)`, `## TTS sanity (D6)`, and (if D7 ran) `## Math-content check (D7)`.
Be terse; quote locations; if a dimension is clean, say so in one line.
