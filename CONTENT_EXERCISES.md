# Exercises: Minimum Skeleton

Full exercise-system design is deferred until the book's main content is largely complete (see [`CONTENT_SPEC.md`](CONTENT_SPEC.md) §14). This file is the **minimum skeleton** — the decisions that should be locked before chapters start accumulating real exercises, so that later work does not have to retrofit every section.

Anything in this file marked *(TBD)* is explicitly open. Anything not marked *(TBD)* is a working decision that authors should follow until this file revises it.

---

## What lives in the spec vs. here

[`CONTENT_SPEC.md`](CONTENT_SPEC.md) §5 (`exercise` environment) + §14 (deferred design) establish:

- every section end **MUST** carry either a real `\subsection*{Exercises}` block or the TODO placeholder comment `% TODO: add \subsection*{Exercises} block with end-of-section problems for Section N.M.`
- exercises are **book-only** — they do not flow into slides, narration, or Manim storyboards (see [`README.md`](README.md) *Media scope*).
- the full exercise system (difficulty markers, answer appendix, inline self-check variants, hint format) is **deferred**.

This file sits between the placeholder rule and the full deferred design. It pins down the minimum so that when the full design opens, it is refining existing structure, not inventing from scratch.

---

## Per-section budget *(working decision — default band, coverage is authoritative)*

- **Default band: 8–12 exercises per section.** Short single-skill sections naturally land lower (5–6); strongly computational sections may go as high as 15.
- The band is a calibration default, **not a quota**. The authoritative criterion is the section's **coverage matrix** (see *Sourcing workflow* below): every definition, theorem, and strategy the section teaches gets exercised at the depth its learning outcomes demand.
- **Compliance is matrix-based, not count-based.** A section is out of compliance when a taught item has no exercise, or when the block pads with near-duplicates to reach the band — not when a genuinely covered section sits at 6, nor when a five-skill section needs 16.
- A section landing outside the band needs no separate exception comment during the skeleton stage; its coverage matrix is the justification.

Rationale: section content varies too much for one fixed count — a one-technique section and a five-skill section should not share a quota. The band survives as the default because most sections do land in it and it remains the right sanity check during gap-fill (enough repeated practice for self-study readers, few enough that working every exercise does not burn a weekend). The matrix is authoritative whenever the count would force the wrong call, mirroring the remark-target idiom in [`CONTENT_SPEC.md`](CONTENT_SPEC.md) §5 ("a target, not a production quota").

---

## Type taxonomy and mix *(working decision — taxonomy fixed, per-section mix content-driven)*

The four-type taxonomy is fixed; every exercise belongs to one of:

| Type | Purpose |
|---|---|
| `conceptual` | "why" or "what fails if" — forces the reader to state a definition or decide whether a condition holds. |
| `computational` | direct application of a method to a clean input. |
| `reasoning` | short proofs, counterexample construction, "for which inputs does this identity hold?" |
| `applied` *(optional)* | physics / economics / geometry setup where applicable. |

**Per-section mix is content-driven, not quota-driven.** The coverage matrix decides: an ε-δ section is legitimately reasoning-heavy, a techniques section legitimately computational-heavy, and early chapters naturally skew conceptual + computational. A section includes a type only when its content gives that type real work to do.

**Book-level default priors** — the starting distribution the gap-fill step aims for, and the chapter-level sanity check:

> `conceptual` ≥ 20% · `computational` 40–60% · `reasoning` ≥ 10% · `applied` 0–20%

Audit these shares **per chapter, not per section**: chapter-wide totals should land near the priors even while individual sections skew. A chapter missing the priors overall usually signals under-provisioned conceptual / reasoning work (the recurring failure mode), not a content-driven skew.

The type marker inside the `exercise` environment itself is *(TBD)* — possible options include a `type=` key-value argument, a `\begin{exercise}[conceptual]` optional label, or no in-source marker (type enforced only by author judgment). Pick one in the full design round.

---

## Sourcing workflow *(working decision — manuscript first, bank fill, AI fallback)*

Exercises enter a section from three sources, in priority order, with provenance tracked per exercise.

1. **Manuscript problems — mandatory core.** Every problem in the instructor's manuscript ships. They seed the coverage matrix.
2. **Open problem banks — gap fill.** After the section's main content is drafted:
   1. Build the **coverage matrix**: rows = every definition / theorem / strategy the section teaches; columns = the four types. Mark which cells the manuscript problems already cover.
   2. Search the local banks ([`problem_banks/README.md`](problem_banks/README.md)) for candidates filling the empty cells; produce a candidate list for human curation. Bank taxonomies are a **search index only** — gaps are defined by the section's own content, never by what a bank happens to contain.
   3. Adapt accepted problems to house register and notation ([`CONTENT_SPEC.md`](CONTENT_SPEC.md) §3, §9).
3. **AI-authored problems — fallback.** Only for cells no bank fills (typically extensions tightly coupled to a manuscript running example). Human review required, as before.

### Provenance and licensing

- Every non-manuscript exercise carries a source marker at import time: `[source: CLP-1 §1.3 #2]`, `[source: APEX §6.1 #14]`, `[source: AI]`. Until the full design round decides whether/how markers appear in shipped output, keep them as comments next to the exercise in source.
- The banks in `problem_banks/` are all CC BY / CC BY-NC / CC BY-NC-SA — they compose legally into a handout distributed **free of charge under CC BY-NC-SA 4.0** with a credits page. Do not import from share-alike-only sources (CC BY-SA, e.g. Active Calculus) or "free to view but not openly licensed" sources (e.g. Paul's Online Math Notes).
- **Capture the bank's official hint / answer / solution at import time** into the chapter's import record (`exercise-imports.md` beside the chapter source). This is raw material for the future answer appendix, not the appendix itself — losing it at import means re-deriving every solution later.

---

## Answers and hints *(working decision)*

Two decisions are load-bearing:

- **do exercises carry an answer at all?**
  Working default: **selected computational exercises carry a final numerical or symbolic answer** at the end of the book, so a self-study reader can check their work without seeing a full solution. Conceptual and reasoning exercises default to no answer key.
- **do exercises carry hints?**
  Working default: **no inline hints for exercises**. If an exercise needs a hint to be approachable, it is probably set up wrong, and a preceding worked example should carry the idea instead.

The answer-appendix format (end of chapter vs. end of book, selection criterion, encoding in source) is *(TBD)*.

---

## Difficulty markers *(deferred)*

Deliberately not decided yet. The full design round will choose between:

- no markers at all (simplest — order within section carries difficulty).
- ⭐ / ⭐⭐ / ⭐⭐⭐ inline markers.
- letter codes (`A`, `B`, `C`).
- separate `\subsection*{Exercises}` and `\subsection*{Challenge Problems}` blocks.

Until that decision lands, **do not** encode difficulty in exercise sources. Ordering within the block is the only allowed difficulty signal.

---

## Numbering and labels *(working decision)*

- exercises are numbered per section: `1`, `2`, ..., restart at each new section.
- labels follow the project label convention in [`CONTENT_QUICKSTART.md`](CONTENT_QUICKSTART.md): `ex:sectionslug-descriptor`. Example: `ex:limits-squeeze-1`.
- labels **SHOULD** appear on exercises that later sections will cite. Most exercises do not need labels.

---

## Format inside `\subsection*{Exercises}` *(working decision)*

```latex
\subsection*{Exercises}

\begin{exercise}
  Prompt text.
\end{exercise}

\begin{exercise}
  Another prompt. May contain display math, inline math, and short
  multi-part structure using \texttt{enumerate}.
\end{exercise}
```

Multi-part exercises use `enumerate` inside the `exercise` body. Do not invent new environments for sub-parts until the full design round.

---

## What NOT to do before the full design round

These are the traps we want to avoid accumulating before the exercise system is designed properly:

- **do not** invent per-chapter exercise macros. If a shortcut seems helpful, note it in the chapter's open-questions list in [`CONTENT_ROADMAP.md`](CONTENT_ROADMAP.md) rather than adding a `\newcommand`.
- **do not** mix slide or narration content into exercise prompts — exercises are book-only.
- **do not** seed the answer appendix until the selection criterion and format are locked. (Capturing bank-provided solutions in a chapter's `exercise-imports.md` is fine — that is import raw material, not the appendix.)
- **do not** mark difficulty in the source.
- **do not** include hints inline.

---

## When this file is upgraded

Trigger: **a solid majority of chapters have complete main content** (per spec §14).

At that point, the dedicated exercise design round will:

1. audit what's already in the TODO placeholders and the real exercise blocks that have accumulated.
2. decide the deferred items: difficulty markers, answer appendix format, hint policy, in-source type taxonomy, environment variants (self-check, challenge).
3. replace this skeleton file with the full spec, bumping a version number.
4. retrofit existing exercise blocks to the new spec, one chapter at a time.

Until then, anything not covered here should err on the side of **simple and reversible** — treat exercises as prose-with-a-frame rather than as a domain-specific sub-system.
