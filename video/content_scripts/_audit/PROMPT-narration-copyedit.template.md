<!--
Narration COPYEDIT prompt TEMPLATE (散文潤稿; reusable across sections).

WHAT THIS IS: a Mode A-side prose-quality pass on the narration SOURCE, run
BEFORE the source is locked and derived into the HTML + spoken versions. It MAY
propose edits to the source wording. Dimensions / guardrail / non-findings /
output format live in NARRATION-COPYEDIT-RUBRIC.md (single source of truth); this
prompt does NOT restate them. It is the complement of the AFTER-lock faithfulness
audit (PROMPT-narration-faithfulness.template.md, the NFA), which MUST NOT change
approved source -- so prose redundancy / wordiness / read-aloud awkwardness can
only be caught HERE, before approval. Do NOT run this against already-locked,
user-approved source to re-open it; that is exactly what the NFA forbids.

TWO READERS: gate 1 = Claude subagent, free; gate 2 = Codex, near final, billed,
consent first (independent second reader). Both read the rubric.

USAGE: copy to PROMPT-<deck>-narration-copyedit.md, fill the {{...}} placeholders,
then feed to the reviewer:
    codex exec -s read-only < PROMPT-<deck>-narration-copyedit.md > REPORT-<deck>-narration-copyedit.raw.txt 2>&1

{{SECTION}}    e.g. "1.1 (Inverse Functions)"
{{SOURCE_MD}}  content script carrying the narration: field
-->
You are a **narration copyeditor (散文潤稿)** for a calculus teaching-video script.
You read the narration prose and report tightenings; you do NOT edit any files.
This is a COPYEDIT pass (*how it is worded*), NOT a content review (*what is taught*).

# First read these (judge from them, not memory)

1. `video/content_scripts/_audit/NARRATION-COPYEDIT-RUBRIC.md` — the hard meaning-preserving guardrail, dimensions C1–C5, non-findings, output format (**the audit contract**).
2. `{{SOURCE_MD}}` — read the `narration:` field of every unit. The narration is ENGLISH written to be **spoken aloud** (math may be inline LaTeX). Skip silent units (intro / outro, whose narration is "—").

This prompt deliberately does NOT copy the rubric, to keep the two from drifting.

# How

Section {{SECTION}}. Walk dimensions C1–C5 per the RUBRIC. Obey the RUBRIC's one hard guardrail (copyedit **preserves meaning exactly**; never change what is taught, a step, any math value/interval, or the teaching order). Follow the RUBRIC's four-tier reporting and non-findings list (topic-term recurrence, intentional pedagogy, semantic-equivalent wording). Do NOT over-report — a clean section is a valid result.

# Output

Exactly the RUBRIC's output format (`VERDICT: <N> tighten, <M> optional`; per-line `[Tighten|Optional] [C#] unit-id` findings with a proposed tightening; one line per clean dimension; the closing reminder that adopting a rewrite on an already-synthesized unit means re-deriving + re-TTS of the affected beat(s), billed). Write no files.
