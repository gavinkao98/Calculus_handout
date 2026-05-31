# Manim Storyboard Authoring: LaTeX Handout to YAML

**Version 1.6** -- adds the reveal-strategy layer (manim-voiceover migration). Three strategies (`all_at_once`, `beat_paced`, `hybrid`) plus an `hybrid_auto` heuristic decide *when* each visual element appears relative to the narration. Defaults per template are enumerated in [`MANIM_REFERENCE.md`](MANIM_REFERENCE.md#reveal-strategy-動畫顯示時機); authors usually only write `template + voiceover + data` and inherit the predicted timing. Bookmark syntax (`<bookmark mark='math_line_0'/>` in `voiceover`) lets you nail a specific cue. `voiceover_beats` remain permanently supported as the readable form for "every element waits for narration" scenes. The choice rule is: pure prose / overview -> `all_at_once`; algorithmic walkthrough -> `beat_paced` (with `voiceover_beats` for clarity); everything else -> `hybrid` (default) and only escalate to `hybrid_auto` when you want anchor heuristics to place bookmarks for you.

**Version 1.5** -- voiceover sentence-count rule recalibrated after `tools/manim_storyboard_lint.py` was first run against the corpus and produced four warnings on the already-signed-off `ch01_inverse_functions.yml`. The warnings were not defects in that storyboard; they were gaps in the rule. Two carve-outs added (`theorem_proof` 5-9 sentences, `recap_cards` 5-8 sentences), and a +1 boundary tolerance added to the standard 3-6 range so a scene that lands at exactly 7 sentences is acceptable without comment when no other carve-out applies. The lint tool was updated to match. Net effect: rules now describe what the corpus actually does, instead of asking the corpus to shrink to fit the rules.

**Version 1.4** -- second exemplar (Sec. 1.6 *The Precise Definition of a Limit*) added as a deliberately contrasting calibration point. Sec. 1.6 is symbol-heavy where Sec. 1.1 is graph-heavy; the rules added in this revision come from the gaps that surfaced when Sec. 1.1's patterns were applied to Sec. 1.6. New material: (a) classification and treatment of *prose-only scenes* (chapter content that lives outside any LaTeX environment); (b) a `% expansion:` category-to-storyboard mapping table aligned with the chapter authoring system; (c) a new "Forward-reference scenes" pattern; (d) a fourth hook trigger for figures with dense schematic markup; (e) a wedge between *strategy* (judgment-type) and *procedure* (linear-type) that share the `procedure_steps` template; (f) a SHOULD on voiceover savings for repeat-pattern examples; (g) three explicit conditions for the 9-sentence carve-out; (h) an `\varepsilon`-`\delta` extension to the spoken-math table and a new "Aligned chains in voiceover" rule; (i) conditioning the "visual over textual" commitment for symbol-heavy sections; (j) widened `section_transition` use to cover concept transitions inside a section; (k) guidance for proofs whose body is an aligned algebraic chain.

**Version 1.3** -- adds a SHOULD rule for `example_walkthrough` `data.decay_previous`: scenes whose voiceover calls back verbally to an earlier `math_line` or `step` should set it to `false` so the scene does not dim the line the narration is about to re-read. Also adds a matching pre-render checklist item. v1.2 (below) remains the current voiceover sentence-count rule.

**Version 1.1** -- adds a conformance legend (MUST / SHOULD / MAY), two worked before/after examples (LaTeX source -> YAML -> voiceover), softens the single-exemplar dependency on Sec. 1.1, aligns the "direct from LaTeX" workflow across `README.md`, `MANIM_REFERENCE.md`, and `MANIM_CHECKLIST.md`, and replaces non-ASCII punctuation (em-dash, en-dash, arrow) in body text so the file reads cleanly in terminal contexts.

Derived originally by reverse-engineering the Sec. 1.1 *Inverse Functions* storyboard ([`inputs/manim_storyboards/ch01_inverse_functions.yml`](inputs/manim_storyboards/ch01_inverse_functions.yml)) against [`chapters/ch01_foundations.tex`](chapters/ch01_foundations.tex), and re-calibrated against the Sec. 1.6 *Precise Definition of a Limit* storyboard ([`inputs/manim_storyboards/ch01_precise_limit.yml`](inputs/manim_storyboards/ch01_precise_limit.yml)) for v1.4. The two exemplars are deliberately contrasting: Sec. 1.1 is graph-heavy with light symbolic content, Sec. 1.6 is symbol-heavy with two anchor graphs. Rules in this guide should hold across both; when one exemplar produces a rule the other contradicts, treat it as a signal to review both. As more chapters are storyboarded, rules should converge on the common denominator across them, not on any single section.

This guide is the translation methodology layer. It is distinct from:

- [`MANIM_REFERENCE.md`](MANIM_REFERENCE.md) -- field reference, template catalog, rendering commands, visual design system.
- [`CONTENT_SPEC.md`](CONTENT_SPEC.md) -- textbook writing rules (authority over the `.tex` source).
- [`MANIM_CHECKLIST.md`](MANIM_CHECKLIST.md) -- operational steps for running the pipeline.

Read those for *what the machinery is* and *how to operate it*. Read this guide for *what to put in the YAML when staring at a chapter section*.

---

## Conformance Keywords

This document uses RFC 2119-style keywords to make load-bearing rules unambiguous:

- **MUST** / **MUST NOT** -- hard requirement. A storyboard that violates a MUST is out of compliance and SHOULD be fixed before rendering.
- **SHOULD** / **SHOULD NOT** -- strong recommendation. Deviation is acceptable only with a concrete reason; record the reason in a YAML comment near the deviating scene so a later editor can judge whether the deviation still applies.
- **MAY** -- optional. Use when it helps; the storyboard is equally valid without it.

Outside these keywords, words like *always added*, *encouraged*, *acceptable*, and *rare* describe current practice without carrying formal compliance weight. If a practice turns out to be load-bearing in review, it earns a MUST or SHOULD rewrite in a later revision.

---

## Purpose

A storyboard YAML is hand-written. It does **not** regenerate from the LaTeX handout. When `chapters/*.tex` changes, someone must re-read the section and revise the storyboard by hand.

This guide answers: *given a finalized section in the book, what storyboard do we write?*

The answer has several layers:

1. **Scope** -- what to include in the video, what to leave in the book.
2. **Decomposition** -- how to split a section into scenes.
3. **Mapping** -- how to pick a template for each scene.
4. **Voiceover rewriting** -- how to turn written prose into spoken narration.
5. **Figure handling** -- how to translate book figures into Manim.
6. **Pacing** -- how long scenes should run.

Each layer has rules below, grounded in the Sec. 1.1 exemplar.

---

## Overall Philosophy

The video is **a class**, not a book being read aloud. Three commitments follow:

1. **Detail over compression.** When in doubt, make a scene rather than merging content. The Sec. 1.1 storyboard has 16 scenes for ~300 lines of LaTeX -- roughly one scene per formal environment plus added visualizations. A 4-minute highlight reel is not the goal.
2. **Conversational over formal.** Narration is spoken English. Contractions stay light (prefer "let us" over "let's" for consistency with the classroom register), but the sentence rhythm is spoken, not printed. The book says "Determine which of these functions are one-to-one"; the video says "Now let us test two mathematical functions."
3. **Visual over textual, with one exception.** When a concept can be shown on a graph, add a `graph_focus` scene even if the book only states it in prose. Reflections across `y = x`, counterexamples shown on a curve, and the horizontal line test all deserve their own visual scenes. *Exception (added v1.4):* in a symbol-heavy section -- defined operationally as one whose teaching weight is at least seventy percent symbolic / logical / quantifier-driven (`epsilon`-`delta`, convergence tests, Bolzano-Weierstrass, Riemann sums) -- restrict `graph_focus` scenes to the section's anchor concept plus at most one contrasting case. Forcing a graph onto every algebraic example dilutes the symbolic core. See *When the section is symbol-heavy* below for the operational rule.

---

## Pre-flight: Inputs You Need

Before writing a line of YAML, have these open:

- The target section in `chapters/<chapter>.tex` -- read it start to end, including the chapter opening prose if this is the first section.
- [`MANIM_REFERENCE.md`](MANIM_REFERENCE.md) -- the **Templates (9)** table and the **Midnight Canvas** color semantics.
- An existing storyboard (start with Sec. 1.1) for cross-reference on style and field usage.
- The `schemas/manim_storyboard.schema.json` if you need the exact field contract.

Do **not** seed from the deck JSON. The modern workflow designs directly from LaTeX. Seeding is legacy.

---

## Step-by-Step Workflow

1. **Read the source section** end to end. Identify every `\begin{definition}`, `\begin{theorem}`, `\begin{proposition}`, `\begin{remark}`, `\begin{example}`, `\begin{figure}`, and every subsection boundary. Note each one with its line number.
2. **Sketch a scene list** on paper or in a comment block -- one bullet per scene, in video order, before touching YAML. Decide per bullet: what template, what teaching idea.
3. **Drop in opening and closing scenes** -- an opening hook (`title_bullets`) and a recap (`recap_cards`). These are always added, never present in the book.
4. **Add transitions** between subsections if the section has enough structural breaks -- a `section_transition` scene is 3-4 seconds of relief between conceptual blocks.
5. **Add supplementary visualizations** where prose-only content in the book benefits from a graph (reflection across `y = x`, counterexamples on curves, domain restrictions). These are not in the book; they are added for pedagogy.
6. **Write each scene** -- `scene_id`, `template`, `content_type` if ambiguous, `title`, `voiceover`, `data`, `timing`. See per-field rules below.
7. **Preview every new `graph_focus` scene** with `tools/manim_preview_graph_focus.py` before committing -- this is faster than a full Manim render and catches most expression/labeling mistakes.
8. **Proofread the full narration** by exporting `narration.md` and reading it top to bottom as if you were a student. Edit in place, then `manim_sync_narration_back.py`.
9. **Render with audio** and watch the whole thing at 1x speed. Anything that sounds awkward or looks cramped is a signal to re-edit, not ship.

---

## Scene Decomposition

### Rule: one teaching idea per scene

A scene **MUST** hold exactly one thing a student should take away. If the voiceover needs two topic sentences, split the scene.

Concretely, each of the following is its own scene:

- one `\begin{definition}` environment
- one `\begin{theorem}` or `\begin{proposition}` statement
- one `\begin{proof}` (can combine with its theorem in a `theorem_proof` scene, or be its own scene after the statement)
- one `\begin{example}` + `\begin{solution}` pair
- one `\begin{remark}` **if** it rises to the level of a named rule (e.g., the horizontal line test); trivial remarks can be folded into nearby voiceover
- one book `\begin{figure}` that the video will redraw
- one standalone procedure / enumerated list (e.g., the 3-step "how to find an inverse")
- one added visualization that is not in the book

A storyboard **MUST NOT** cram a definition and its example into one scene, and **MUST NOT** merge two examples into one scene even if they are visually similar.

### Rule: added scenes are expected, not exceptional

The Sec. 1.1 storyboard has **six scenes with no direct source in the book**:

| Added scene | Why |
|---|---|
| `opening_hook` | Framing / motivation via title_bullets. Every video opens with one. |
| `why_x_squared_fails` | Turns a prose claim into a `graph_focus` visualization. |
| `transition_to_inverses` | `section_transition` between subsec 1.1.1 and 1.1.2. |
| `cubic_graph_reflection` | Reflection across `y = x` -- stated as prose in book, deserves a graph. |
| `restricted_parabola_graph` | Same -- domain restriction made visual. |
| `recap` | Closing `recap_cards`. Every video closes with one. |

A storyboard **MUST** include an opening-hook scene and a closing recap scene. A storyboard **SHOULD** include a `section_transition` scene between conceptual blocks when the source section has three or more subsections. The same scene **MAY** also be used to mark a *concept transition* inside a section that has no formal subsections -- for example, the jump from a numerical instance to an arbitrary `\varepsilon` in Sec. 1.6 (`tolerance_to_general` in `ch01_precise_limit.yml`); when used this way, the `subtitle` field names the conceptual stage and `upcoming` previews the next two or three scenes. A storyboard **SHOULD** add a supplementary `graph_focus` scene whenever the book makes a geometric claim (reflection, intersection, shape) in prose alone -- subject to the symbol-heavy exception in *Overall Philosophy* #3.

### Rule: scene count is not a budget

Do not try to keep the scene count low. Sec. 1.1 runs 16 scenes; a shorter or simpler section can be 8, a denser one can be 20. Count is an output of good decomposition, not a constraint on it.

---

## Environment -> Template Mapping

This is the single most common authoring decision. Use the following table as a first cut; the notes below handle the edge cases.

| Source environment | Default template | `content_type` | Notes |
|---|---|---|---|
| `\begin{definition}` | `definition_math` | `definition` | The template is built around statement + math_lines. |
| `\begin{theorem}` with a `\begin{proof}` | `theorem_proof` | `theorem` | Statement + proof_steps in one scene. |
| `\begin{theorem}` without a proof | `definition_math` | `theorem` | Template handles this cleanly; content_type flags the gold accent. |
| `\begin{proposition}` | `definition_math` | `proposition` | Same as theorem-without-proof visually. |
| `\begin{lemma}` / `\begin{corollary}` | `definition_math` | `proposition` | Rare; treat as propositions visually. |
| `\begin{example}` + `\begin{solution}` | `example_walkthrough` | `example` | Each step becomes one `steps` entry, math_lines show the algebra. |
| `\begin{remark}` that names a rule (e.g., horizontal line test) | `definition_math` | `proposition` | Treat it as a lightweight proposition in the video. |
| `\begin{remark}` that is a short aside | (fold into voiceover of neighboring scene) | -- | A 2-sentence warning does not need its own scene. |
| Enumerated procedure / algorithm list | `procedure_steps` | `procedure` | Use `worked_equations` for the symbolic template of the procedure. |
| `\begin{figure}` with a function graph | `graph_focus` | inherit or `example` | Redraw in Manim axes + plots. |
| `\begin{figure}` with a conceptual diagram (mapping, interval, arrows) | `graph_focus` + custom `hook` | -- | Templates cannot draw arbitrary TikZ; write a hook. |
| Subsection boundary with a named transition | `section_transition` | -- | Optional; use it when it genuinely helps pacing. |
| (always add) Opening motivation | `title_bullets` | `definition` | Bullets preview the question the video will answer. |
| (always add) Closing summary | `recap_cards` | `recap` | 4-6 `points`, 1-2 canonical `identities`. |
| (add when useful) Reflection / geometric visualization stated in prose | `graph_focus` | `example` | Two curves + `y = x` dashed; see `cubic_graph_reflection`. |
| (add when useful) Side-by-side concept comparison | `comparison` | -- | Use only when contrast is the lesson. |

### Edge case: two formal statements close together

If a `\begin{definition}` is followed immediately by a short `\begin{proposition}` that is really just a domain/range restatement of the definition, it is acceptable to put the proposition in the `supporting_bullets` of the definition scene. But if the proposition gets its own label in the book and is referenced later, give it its own scene.

### Edge case: proof that is longer than its statement

If the proof has more than ~4 steps, split into a `definition_math` scene for the statement and a `theorem_proof` scene (with the statement repeated) for the proof. Students can then pause after the statement before watching the proof.

### Edge case: proof whose body is an aligned algebraic chain

If the proof's central beat is a derivation aligned on `=`, `\le`, or `<` (typical of triangle-inequality and squeeze-style arguments), `theorem_proof`'s schema is too thin: `proof_steps` is a flat string array with no `math_layout` option, so the alignment is lost in rendering. **Two-scene workaround**: write the statement as `definition_math` with `content_type: theorem`, then write the proof as `example_walkthrough` with `math_layout: "equals_aligned"` and `decay_previous: false`, treating the algebraic chain as the derivation in `math_lines` and the proof's logical beats as `steps`. This is the route taken by `uniqueness_statement` + `uniqueness_proof` in `ch01_precise_limit.yml`. The cost is one extra scene; the gain is that the chain `|L - M| = ... \le ... < 2\varepsilon = |L - M|` reads as a coherent line-up of inequalities rather than four detached strings. A future schema revision should add `math_layout` and a structured `math_lines` field to `theorem_proof` so the workaround becomes unnecessary.

### Worked example: definition -> `definition_math` scene

This is the first formal statement in the source of Sec. 1.1. It illustrates the typical `definition` -> `definition_math` mapping, spoken-math rewriting, and the role of `animation: "highlight"`.

**LaTeX source** (`chapters/ch01_foundations.tex`, Sec. 1.1.1):

~~~latex
\begin{definition}
Let \(f\) be a function with domain \(A\). We say that \(f\) is \emph{one-to-one}\index{one-to-one function} if
\[
f(x_1)\ne f(x_2)
\qquad \text{whenever } x_1\ne x_2.
\]
Equivalently, \(f\) is one-to-one if
\[
f(x_1)=f(x_2) \implies x_1=x_2.
\]
\end{definition}
~~~

**Scene YAML** (from [`inputs/manim_storyboards/ch01_inverse_functions.yml`](inputs/manim_storyboards/ch01_inverse_functions.yml)):

~~~yaml
- scene_id: "one_to_one_definition"
  template: "definition_math"
  content_type: "definition"
  scene_exit: "hold"
  title: "One-to-One Functions"
  voiceover: >
    The key property is called one-to-one. A function is one-to-one when
    different inputs always produce different outputs. No two distinct x-values
    ever land on the same y-value. There is an equivalent way to say this: if
    you know that f of x one equals f of x two, then you can conclude that x
    one must equal x two. Both statements capture the same idea, but the second
    form is often easier to use in a proof.
  timing:
    lead_in_seconds: 0.2
    hold_after_seconds: 0.6
    minimum_duration_seconds: 5.0
  data:
    statement: "A function \\(f\\) is one-to-one if different inputs always produce different outputs."
    math_lines:
      - "\\[f(x_1) \\ne f(x_2) \\qquad \\text{whenever } x_1 \\ne x_2.\\]"
      - text: "\\[f(x_1) = f(x_2) \\;\\Longrightarrow\\; x_1 = x_2.\\]"
        animation: "highlight"
~~~

**What the rewrite does:**

- The book's two equivalent symbolic forms become two `math_lines` in the same order. The second form (the one the book calls "often easier to use in a proof") is flagged `animation: "highlight"` so it visibly flashes as the payoff.
- The book's hedging verb ("We say that `f` is one-to-one if ...") is stripped from `statement`. The statement on screen is a single declarative sentence; the teacherly register returns in the voiceover.
- `\emph{...}` and `\index{...}` are dropped -- they have no video analog.
- The voiceover does not read the math aloud symbol-by-symbol. `f(x_1) \ne f(x_2)` becomes "f of x one is different from f of x two" in spoken form, and the voiceover paraphrases that at "no two distinct x-values ever land on the same y-value" for variety.
- The voiceover does not say the title, does not reference a definition number, and does not open with "In this scene".
- `content_type: "definition"` is explicit so `definition_math` renders with the cyan accent -- this satisfies the MUST on `content_type` for `definition_math` scenes.
- `scene_exit: "hold"` keeps the final frame visible while the TTS finishes the five-sentence narration.

---

## What to Include vs Skip

### Always include

- Every `\begin{definition}`.
- Every `\begin{theorem}` and `\begin{proposition}`.
- Every `\begin{example}` -- manuscript examples are the primary teaching currency.
- Any procedure or algorithm that the book explicitly numbers.
- Any figure whose geometric content is part of the learning.

### Conditionally include

- `\begin{proof}` -- include when the argument is short, pedagogically instructive, or when the manuscript already includes it. Skip when the proof is either trivial or so technical that watching it animate provides less than reading it.
- `\begin{remark}` -- include as its own scene when the remark names a rule or flags a pitfall students often miss; otherwise fold into voiceover of the neighboring scene.
- `\begin{figure}` conceptual diagrams -- include when the diagram teaches something the prose alone cannot. Skip when the diagram is only a decorative restatement of the prose.

### Always skip

- `\begin{exercise}` and `\subsection*{Exercises}` blocks **MUST NOT** appear in any scene. They are for student self-practice on the book only; they never enter the video. See the Media scope note in [`README.md`](README.md).
- Index commands (`\index{...}`) -- no video analog.
- Cross-references (`\cref{...}`) to objects outside the current section -- paraphrase the referenced result rather than pointing to it; the student watching a video has no page to flip to.
- Chapter overview paragraphs that are already incorporated into the opening hook.

### Section summary at the end

If the book has a `\section*{Summary}`, use it as raw material for the `recap_cards` scene. If the book does not, still write a recap -- every video closes with one.

---

## Prose-Only Scenes

The Environment -> Template Mapping table covers content inside `\begin{...}` environments. But a chapter section often carries pedagogically load-bearing prose that lives *between* environments -- setup paragraphs, bridging paragraphs, post-figure summaries, forward-pointing previews. v1.3 had no rule for these; v1.4 adds one because the Sec. 1.6 storyboard had four such paragraphs and the choice between *fold* and *promote* changed the scene count by three.

Classify every non-environment paragraph into one of three roles:

| Role | What it does | Default treatment |
|---|---|---|
| **Incorporative** | Sets up the next environment (defines the function under study, motivates the upcoming definition, names the variables). | Fold into the *lead-in sentence* of the next environment's voiceover. The Sec. 1.6 piecewise-function setup at L1339-1347 is folded into the `piecewise_motivation` scene's voiceover this way. |
| **Bridge** | Joins two conceptual blocks; carries no new formal statement but contains a teaching beat the next scene depends on. | One to two sentences: fold into the *closing sentence* of the previous scene or the lead-in of the next. Three or more sentences with a genuine concept jump (e.g., from a specific number to "for every \(\varepsilon\)"): promote to its own scene, typically `section_transition` with a `subtitle` naming the jump. The Sec. 1.6 tightening-tolerance prose at L1365 is promoted as `tolerance_to_general`. |
| **Forward-pointing** | Introduces a concept that will be developed in a later chapter; ends with "we will study this systematically later". | Always its own scene. See *Forward-Reference Scenes* in *Ordering Heuristics* below. The Sec. 1.6 continuity preview at L1581-1586 is `continuity_preview`, a `definition_math` scene with a single math line. |

A storyboard **MUST NOT** silently drop incorporative or bridge prose. Either fold the content into a neighbouring voiceover or promote it to its own scene, but not both, and never neither. The audit hook: when reading the source section end to end, every paragraph between `\end{...}` and the next `\begin{...}` is a candidate; count them and decide each one before drafting YAML.

---

## Expansion Marker -> Storyboard Treatment

Mode A and Mode C drafting expands chapter sources with `% expansion:<category>` markers (see [`README.md`](README.md) for the chapter-authoring rules). Each category has a default storyboard treatment so the storyboard author does not have to re-classify the same paragraph the chapter author already classified.

| Category | Default storyboard treatment |
|---|---|
| `history` | Fold into the `opening_hook` voiceover. Do not give it its own scene; history is a framing device, not a teaching beat. |
| `intuition` (chapter or section opener) | Fold into the `opening_hook` voiceover (chapter opener) or the lead-in voiceover of the first content scene (section opener). |
| `intuition` (informally gloss inside a definition) | Already part of the definition; carry into the same `definition_math` scene's `statement` or voiceover. |
| `application` | If the tie-in is a single sentence, fold into the nearest scene. If it carries a worked tie-in (a real-world quantity, an applied formula), promote to its own `example_walkthrough` or `graph_focus` scene. |
| `formula` (derived identity) | Usually its own scene -- a derived identity is a teaching beat. The Sec. 1.6 `% expansion:formula` for the uniqueness proof becomes the `uniqueness_statement` + `uniqueness_proof` pair; the `% expansion:formula` for the continuity preview becomes `continuity_preview`. |
| `figure` (drawn or implied) | A scene candidate by default -- if the figure teaches something, redraw it. See *Figures: Redrawing the Book in Manim*. |
| `example` (supplementary `workedexample`) | Standard `example_walkthrough` mapping. No special handling. |
| `strategy` (`strategy` box) | `procedure_steps` if the steps are linear; if the strategy contains conditional branches ("if X, then Y"), still `procedure_steps` but with `worked_equations` showing the *target shape* the strategy aims to produce rather than a literal output. See *data > procedure_steps* for the strategy-vs-procedure split. |
| `caution` (`caution` box) | One sentence: fold into the nearest scene's voiceover with a "watch out: ..." beat. A caution that names a recurring pitfall: promote to its own scene with `content_type: warning`. |
| `summary` (chapter-end Summary) | Raw material for the `recap_cards` scene's `points` and `identities`. |

When the default does not fit a particular paragraph, deviate -- but record the deviation in a YAML comment near the affected scene so a later editor knows it was deliberate.

---

## Voiceover: Writing for Speech

This is the layer where authoring most often goes wrong. Book prose reads well on a page and sounds stilted when spoken. Rewrite every narration line for the ear.

### Voice and register

- **"We" for the class, imperative for setup, "you" sparingly and only for direct call-outs.** Book: "We obtain `x = ...`." Video: same, or "We obtain x equals ..." when the math is read aloud. Avoid "the reader" and "I".
- **Contractions are usually open.** Prefer "let us", "that is", "do not" over "let's", "i.e.", "don't". The Sec. 1.1 storyboard is consistent on this. Exception: when a contraction genuinely improves flow, it is allowed.
- **Classroom filler is OK in small doses.** Phrases like "Here is the idea", "Notice that", "The lesson:", "Watch what happens", "Now look at" pull the student along. Do not overuse them.
- **Forbidden in voiceover**: section numbers, equation labels, "as we will see in Chapter 3", LaTeX command names, and the words "above", "below", "on the left of this page". The video has no page.

### Spoken math

Math symbols must be rewritten as speech. Do **not** let the TTS pronounce `f(x_1)` as "f paren x sub 1 close paren".

| Written | Spoken in voiceover |
|---|---|
| `f(x)` | "f of x" |
| `f(x_1)` | "f of x one" (not "x sub one") |
| `f^{-1}` | "f inverse" |
| `f^{-1}(y)` | "f inverse of y" |
| `x \ne y` | "x is different from y" or "x does not equal y" |
| `x_1 \ne x_2 \Rightarrow f(x_1) \ne f(x_2)` | "if x one is different from x two, then f of x one is different from f of x two" |
| `\sqrt{x}` | "the square root of x" |
| `\sqrt[3]{x-2}` | "the cube root of x minus two" |
| `x \in A` | "x in A" or "x belongs to A" |
| `y \in B` | "y in B" |
| `\frac{1}{4}` | "one fourth" (or "one over four" if disambiguation needed) |
| `x^2` | "x squared" |
| `x^3` | "x cubed" |
| `x^n` | "x to the n" |
| `\le`, `\ge` | "less than or equal to", "greater than or equal to" |
| `[-1, 1]` | "minus one to one" or "the interval minus one to one" |
| `\Leftrightarrow` | "if and only if" |
| `\lim_{x \to a} f(x)` | "the limit of f of x as x approaches a" |
| `f'(x)` | "f prime of x" |
| `\sin^{-1}(x)` | "inverse sine of x" (or "arc sine of x", follow CONTENT_SPEC.md) |

#### `\varepsilon`-`\delta` and quantifier vocabulary (added v1.4)

| Written | Spoken in voiceover |
|---|---|
| `\varepsilon`, `\epsilon` | "epsilon" |
| `\delta` | "delta" |
| `\varepsilon > 0` | "any positive epsilon" (smoother than "epsilon greater than zero") |
| `\delta_1`, `\delta_2` | "delta one", "delta two" (consistent with `x_1` -> "x one"; do not say "sub one") |
| `\forall \varepsilon > 0` | "for every positive epsilon" |
| `\exists \delta > 0` | "there exists a positive delta" |
| `|x - a|` | "the absolute value of x minus a" or "the distance from x to a" |
| `0 < |x - a| < \delta` | "x is within delta of a, and x is not equal to a" |
| `\Rightarrow`, `\implies` | "implies" or "so" |
| `\min\{a, b\}` | "the smaller of a and b" (not "min of a and b") |
| `\max\{a, b\}` | "the larger of a and b" |
| `\tfrac{\varepsilon}{2}` | "half epsilon" preferred; "epsilon over two" acceptable when disambiguation needed |
| `M`, `N` (infinite-limit thresholds) | "M" and "N" -- name them as letters, then gloss "any positive threshold M" / "any negative threshold N" the first time |

When the source uses `\forall` and `\exists` symbolically inside a `definition_math.math_lines` block, the *voiceover* still spells them as English ("for every", "there exists"). The on-screen quantifier notation and the spoken English coexist; do not let the TTS pronounce a literal `\forall`.

Numbers: write "minus one half", not "negative one-half", to match how the Sec. 1.1 narration reads.

### Aligned chains in voiceover

Sec. 1.6 surfaced a recurring need: how to read aloud a derivation aligned on `=`, `\le`, or `<` without making the TTS chant the LHS once per line. The rule is:

1. **First line**: read the entire equation, including the LHS. *"The absolute value of L minus M equals the absolute value of L minus f-of-x plus f-of-x minus M."*
2. **Middle lines**: read only the connector + RHS, suppressing the LHS that the alignment is preserving. *"...which is at most the sum of the absolute values..."* / *"...strictly less than two epsilon..."*
3. **Closing line**: if the chain returns to the original LHS (a contradiction setup like `< 2\varepsilon = |L - M|`), name the closure explicitly. *"...which equals the absolute value of L minus M itself -- a contradiction."*

This convention applies to any `example_walkthrough`, `procedure_steps`, or proof scene whose `math_lines` use `math_layout: "equals_aligned"`. Reading the LHS on every line turns a 30-second derivation into a 60-second listing; the alignment is doing the visual repetition for you, so the voiceover **MUST NOT** repeat it verbally.

### Per-scene structure

A voiceover block should have three parts in this order, not necessarily all present:

1. **Hook or transition** -- 1 sentence connecting to what just happened or stating what this scene is about. "Now let us test two mathematical functions." "Here is the definition."
2. **Body** -- 2-4 sentences carrying the content. This is where the math is spoken and the logic is walked.
3. **Takeaway or bridge** -- 1 sentence summarizing what the student should remember, or pointing to the next scene. "The lesson: ask whether a single output can be traced back to two different inputs."

Three to six sentences is the target range for standard content scenes (`definition_math`, `graph_focus`, ordinary `example_walkthrough`, `procedure_steps`). A scene that lands at exactly seven sentences is acceptable without invoking a carve-out -- the +1 boundary tolerance acknowledges that a single extra sentence is often the cost of a clean takeaway, not a defect. The actual SHOULD limit, beyond which a carve-out is required, is eight sentences for standard scenes. Four carve-outs (added v1.4 and v1.5):

- **`section_transition` scenes** SHOULD be 1-2 sentences. They are brief interludes; a 3-sentence transition stops feeling like relief and starts feeling like content. The "concept transition" use added in v1.4 (a transition inside a section that has no formal subsections) MAY run 3-5 sentences when the conceptual jump genuinely needs the extra space (e.g., the Sec. 1.6 `tolerance_to_general` scene that takes the leap from a specific tolerance to "for every \(\varepsilon\)").
- **`example_walkthrough` scenes that bundle a procedure plus its verification, or that enumerate 4+ distinct algebraic moves,** MAY run up to 9 sentences. The scene still holds one teaching idea ("apply the procedure and verify the answer" is one idea, not two), so splitting would harm cohesion more than length helps it. **The 9-sentence carve-out applies when all three of the following hold:** (1) the solution contains three or more distinct algebraic moves beyond setup and answer; (2) the scene includes a verification, reflection, or back-substitution step that returns to the original expression; (3) splitting into two scenes would break the *procedure -> verification* time-order link. The Sec. 1.6 `quadratic_epsilon_delta` scene is the worked test case (moves: simplify, pre-restrict, force the bound below `\varepsilon`, take the minimum; the verification is the closing chain `4|x-1| < 4 \cdot \varepsilon/4 = \varepsilon`). When even one condition fails, fall back to the six-sentence cap.
- **`theorem_proof` scenes** MAY run 5-9 sentences (added v1.5). A `theorem_proof` scene carries two beats -- the statement and the proof's logical chain -- and even a short proof typically adds 2-3 sentences over a standard `definition_math`. Eight sentences is comfortable for a clean two-line proof; nine is acceptable when the proof has 4+ logical steps. If the proof would push past nine, split into a `definition_math` statement scene plus an `example_walkthrough`-or-`theorem_proof` proof scene per the *Edge case: proof that is longer than its statement* rule.
- **`recap_cards` scenes** MAY run 5-8 sentences (added v1.5). Recap voiceover walks through the takeaway list, devoting roughly one sentence per take-away plus a short framing sentence at top. With four to six bullet points (the standard `recap_cards.points` count), a five-to-eight-sentence narration is the natural shape; demanding 3-6 sentences would force two takeaways per sentence and make the recap feel rushed.

Outside those carve-outs, longer than seven sentences and the scene probably needs splitting; shorter than three and the visual is probably doing work the narration should reinforce.

### Repeat-pattern examples: skip the setup the second time

When a section contains two or more `example_walkthrough` scenes that share the same outer pattern (e.g., two `\varepsilon`-`\delta` verifications, two integration-by-parts examples, two limit-law applications), the second and subsequent scenes **MUST NOT** re-establish the setup the first scene already built. The first scene carries the full opening ("Given a positive epsilon, we want a delta such that..."); the second opens with a transition ("For this one,..." / "The same goal, applied to..." / "Same idea, but the algebra is more delicate, because...") and goes straight to the new content. This rule exists because re-stating the setup causes the second scene's first 30-45 seconds to play as a near-replay of the first scene -- listener attention drops, and the new technique gets less airtime than it deserves. The Sec. 1.6 `linear_epsilon_delta` scene establishes the setup; `quadratic_epsilon_delta` opens with "Same goal as before, but the algebra is more delicate" and goes immediately into the factorisation.

### What voiceover and `data` should share

- `data` is what appears on screen: the statement, the math_lines, the bullets, the steps.
- `voiceover` is what is said over the screen.
- They should cover the same material but **not word-for-word**. Book `data.statement`: "A function `f` is one-to-one if different inputs always produce different outputs." Voiceover: "The key property is called one-to-one. A function is one-to-one when different inputs always produce different outputs. No two distinct x-values ever land on the same y-value."

Rule of thumb: `data` is terse and symbolic, voiceover is expanded and narrative. If the TTS reads the narration while the statement is on screen, both layers should reinforce the same idea without sounding like a teleprompter.

**Example of good separation:**
```yaml
title: "One-to-One Functions"
voiceover: >
  The key property is called one-to-one. A function is one-to-one when different 
  inputs always produce different outputs. No two distinct x-values ever land 
  on the same y-value.
data:
  statement: |
    A function is one-to-one if different inputs always produce different outputs.
  math_lines:
    - "x_1 \\ne x_2 \\implies f(x_1) \\ne f(x_2)"
```

### Things the voiceover MUST NOT do

- **MUST NOT** say the scene title. The title is already on screen.
- **MUST NOT** enumerate on-screen bullets verbatim. Paraphrase or elaborate.
- **MUST NOT** reference equation numbers, figure numbers, section numbers, or any `\cref{...}` target from the book.
- **MUST NOT** use "see", "refer to", "as shown", "in the diagram below / above".
- **MUST NOT** open with "In this scene we will...". Just start teaching.

### Voiceover SHOULD guidelines

- Voiceover length **SHOULD** land in the 3-to-6-sentence range for standard content scenes. `section_transition` scenes **SHOULD** be 1-2 sentences; `example_walkthrough` scenes that bundle procedure plus verification **MAY** run up to 9 sentences. The underlying target is cohesion (one teaching idea per scene), not a hard sentence count.
- Math symbols **MUST** be rewritten as spoken English (see the table above). TTS mispronunciation of raw LaTeX is a hard failure.
- The opening sentence of each voiceover **SHOULD** be a hook or transition, and the closing sentence **SHOULD** be a takeaway or bridge.

---

## `data`: What Goes on Screen

Each template has required `data` fields; the rules below are additional shaping.

### `definition_math` / theorem / proposition statements

- `statement`: one English sentence, terse, no narrative padding. The statement earns its place on screen.
- `math_lines`: the formal symbolic content. Use the extended-dict form (`text:` + `animation:`) to draw the eye to the key line. `highlight` on the final clinching form of an if-and-only-if is a common pattern.
- `supporting_bullets`: optional short consequences (e.g., domain-and-range corollaries).

Do not repeat the `statement` inside `math_lines`. If the statement is a formula, put it in `math_lines` and use the English version for `statement`.

### `example_walkthrough`

- `steps`: 3-5 short strings, one per logical move. These appear as text steps that build in sequence.
- `math_lines`: the symbolic scratch-work. Use `math_layout: "equals_aligned"` when the derivation is a chain of equations that shares an `=` anchor (it almost always does for solve-for-x problems).
- Use `animation: "transform_from_previous"` between math lines that evolve from each other (e.g., `y = x^3 + 2` -> `x = \sqrt[3]{y-2}`). Use `highlight` on the final line.
- `takeaway`: one sentence. This is where "always verify the cancellation equation" or "a single counterexample is enough" belongs.
- `data.decay_previous` (opt, default `true`) controls whether earlier `math_lines` fade to low opacity as later ones are introduced. **SHOULD** set to `false` whenever any `voiceover` sentence verbally refers back to an earlier `math_line` or `step` in the same scene (for example, a verification pass that re-reads an earlier result, or a procedure + verification bundle where the verification line plugs a prior expression back in). If the narration calls back to a line that has already dimmed, the scene and the voiceover desynchronize.

#### Worked example: example + solution -> `example_walkthrough` scene

This illustrates the typical `example` + `solution` -> `example_walkthrough` mapping, including `equals_aligned` layout and the interplay of `transform_from_previous` and `highlight`.

**LaTeX source** (`chapters/ch01_foundations.tex`, Sec. 1.1.3):

~~~latex
\begin{example}
Find the inverse of
\(
f(x)=x^3+2.
\)
\end{example}

\begin{solution}
Let
\[
y=x^3+2.
\]
Then
\[
x^3=y-2,
\]
so
\[
x=\sqrt[3]{\,y-2\,}.
\]
Interchanging \(x\) and \(y\), we obtain
\[
f^{-1}(x)=\sqrt[3]{\,x-2\,}.
\]
We check this by composition:
\[
f\bigl(f^{-1}(x)\bigr)
= \left(\sqrt[3]{\,x-2\,}\right)^3+2
= x-2+2
= x.
\]
Thus the inverse is correct.
\end{solution}
~~~

**Scene YAML** (from [`inputs/manim_storyboards/ch01_inverse_functions.yml`](inputs/manim_storyboards/ch01_inverse_functions.yml)):

~~~yaml
- scene_id: "example_cubic"
  template: "example_walkthrough"
  content_type: "example"
  scene_exit: "hold"
  title: "Worked Example: $f(x) = x^3 + 2$"
  voiceover: >
    Let us apply the procedure to f of x equals x cubed plus two. Step one:
    write y equals x cubed plus two. Step two: subtract two, giving x cubed
    equals y minus two. Then take the cube root: x equals the cube root of y
    minus two. Step three: interchange x and y. So f inverse of x equals the
    cube root of x minus two. Finally, let us verify. Compute f of f inverse
    of x: plug the cube root of x minus two into x cubed plus two. The cube
    and the cube root cancel, giving x minus two plus two, which is x. The
    cancellation equation checks out.
  timing:
    lead_in_seconds: 0.2
    hold_after_seconds: 0.6
    minimum_duration_seconds: 7.0
  data:
    steps:
      - "Write \\(y = x^3 + 2\\)."
      - "Solve: \\(x^3 = y - 2\\), so \\(x = \\sqrt[3]{\\,y - 2\\,}\\)."
      - "Swap: \\(f^{-1}(x) = \\sqrt[3]{\\,x - 2\\,}\\)."
      - "Verify: \\(f(f^{-1}(x)) = (\\sqrt[3]{x-2})^3 + 2 = x\\). \\(\\checkmark\\)"
    takeaway: "Always verify the cancellation equation after finding the inverse."
    math_layout: "equals_aligned"
    math_lines:
      - "\\[y = x^3 + 2\\]"
      - text: "\\[x = \\sqrt[3]{\\,y - 2\\,}\\]"
        animation: "transform_from_previous"
      - text: "\\[f^{-1}(x) = \\sqrt[3]{\\,x - 2\\,}\\]"
        animation: "highlight"
~~~

**What the rewrite does:**

- The book's four displayed equations (`y=x^3+2`, `x^3=y-2`, `x=\sqrt[3]{y-2}`, `f^{-1}(x)=\sqrt[3]{x-2}`) collapse to three `math_lines`. The intermediate `x^3 = y-2` is absorbed into the voiceover as a spoken step rather than an on-screen frame -- it does not mark a distinct stage worth its own animation beat. This is a SHOULD: when two adjacent equations are one algebraic move apart, the earlier one **MAY** be elided from `math_lines` if the voiceover carries it.
- `math_layout: "equals_aligned"` pins the `=` sign across all three lines so the derivation reads as a coherent chain rather than three separate formulas.
- `animation: "transform_from_previous"` on the middle line makes the first equation visibly morph into the solved form.
- `animation: "highlight"` on the final line flashes `f^{-1}(x) = \sqrt[3]{x-2}` as the answer. One `highlight` per scene is the SHOULD; two dilutes the signal.
- The verification step lives in `steps` (with a trailing `\\checkmark`), not in `math_lines`. The reason is that verification is bookkeeping rather than derivation, and the voiceover carries its logic adequately. Putting it in `math_lines` would force a fourth `equals_aligned` frame that pedagogically reads as part of the derivation, which it is not.
- `takeaway` is added even though the book has no explicit takeaway sentence. Every `example_walkthrough` scene **SHOULD** carry a one-sentence takeaway; it is the part of the example a student should write down.
- `minimum_duration_seconds: 7.0` is higher than the default 5.0 because the voiceover is long (two teaching beats: procedure and verification).
- The voiceover rewrites the book's displayed `\bigl(f^{-1}(x)\bigr)` composition into spoken form ("f of f inverse of x") and narrates the cancellation step-by-step rather than presenting it as a finished equation chain.

### `graph_focus`

- Stay inside the expression-helper vocabulary: `sin`, `cos`, `tan`, `sqrt`, `exp`, `log`, `cbrt`, `abs`, `pi`, `e`. `graph_focus` expressions **MUST** use `cbrt(...)` for cube roots and **MUST NOT** use `**(1/3)`; the latter produces complex numbers on negative bases and breaks Manim's plotter. ([MANIM_REFERENCE.md:220-233](MANIM_REFERENCE.md#L220-L233))
- Set `x_range` on a plot to the restricted domain if you are illustrating a restriction; do not rely on axis clipping.
- Use `label_side` and `label_x` when two curves are close together or a label might overlap the `y = x` line. Preview with `manim_preview_graph_focus.py` to verify.
- Keep `annotations` to one short sentence each, 6.5 units wide at most.
- For the Midnight Canvas color assignment: primary curve cool cyan `#4cc9f0`, inverse/contrast curve warm gold `#f9a825`, `y = x` reflection line faded grey `#c8c8d8` dashed, counterexample lines coral `#ff6b6b` dashed, highlighted points gold.

#### Graph scene conventions (added v1.6)

These rules cover visual semantics that authoring decisions get wrong if left to default behaviour. The lint enforces what it can; the rest is documentation that hooks must also follow because the lint cannot reach inside hook Python code.

1. **Function labels are mandatory.** Every `kind: function` plot **MUST** have at least one `label` field per unique `expression` (a piecewise function split into multiple segments only needs one label between segments). The label is the function expression in math mode, e.g. `label: "$f(x) = 2x - 1$"`. A graph without a function label is unreadable to a viewer who joins mid-scene. Hooks are responsible for rendering their own labels with `MathTex(...)`.
   - **Lint rule:** `graph-focus-function-needs-label` (ERROR), skipped when the scene has a `hook`.
   - **Position guidance (template plots):** for steep curves (slope `\\geq 2`), `label_side: "right"` keeps a horizontal label off the curve; for flat or moderate curves, `label_side: "up"` is fine. Pick `label_x` at a value where the curve is interior to the chart and far from any vertical / horizontal feature. The `_label_at_curve_edge` helper uses `axes.input_to_graph_point(...)` so `label_x` is interpreted as a chart x-coordinate, not a proportion.
   - **Position guidance (hooks):** place the label in the *empty wedge adjacent to the curve*, not in a far corner of the chart. The wedge is the empty region bounded on one side by the curve and on the other by a chart edge or a dashed band line. A label in the wedge reads as "this is the curve's name"; a label in the opposite corner of the chart reads as a free-floating annotation that the eye does not attach to the curve. The Sec. 1.6 `\\varepsilon`-`\\delta` hook places `f(x) = 2^{x}` at chart-coord `(1.5, 5.5)` -- below the curve's middle rise and above the lower part of the curve, in the lower-left wedge between the curve and the `L - \\varepsilon` band line. An earlier draft placed the label at `(0.85, 12.2)` in the upper-left corner, which a reviewer correctly flagged as "too far from the curve, reads as disconnected".
   - **Footprint check:** before fixing a label position, sample the curve at `label_x \\pm half_width` (where `half_width` is the label's chart-x extent). If the curve at either sample is between the label's top and bottom, the label crosses the curve; move it. For a rising curve `f`, "above the curve at `xc`" means label centre y `> f(xc + half_width) + buff`; the curve's value at the *right* edge of the label is the binding constraint, not at `xc`.

2. **Hollow vs solid dot is a semantic choice; declare it.** Every `kind: point` plot **MUST** set `hollow: true` or `hollow: false` explicitly.
   - `hollow: true` means *the function is undefined at this x, or its value disagrees with the limit* -- the dot marks a "would-be" point that the curve does not include. Drawn stroke-only (`fill_opacity: 0`).
   - `hollow: false` means *a real point on the curve or chart* -- an intersection, a marked function value, an `\\varepsilon`-`\\delta` box corner, etc. Drawn solid.
   - Defaulting to solid silently has produced wrong renders before (a hollow circle at a continuous point falsely suggests `f(a)` is undefined when it equals `L`). Forcing the explicit choice prevents that.
   - **Lint rule:** `graph-focus-point-hollow-explicit` (WARN).

3. **Equal-scale opt-in for geometric figures.** When the figure's pedagogical message depends on the *visual* ratio of x to y -- slopes, reflections about `y = x`, `\\varepsilon`-`\\delta` boxes, circle / conic geometry -- set `axes.equal_scale: true`. The lint then enforces `x_length / x_span == y_length / y_span` (within 1%).
   - When `equal_scale` is omitted or `false`, the chart can stretch or squash and lint says nothing. Useful for symbol-heavy figures where the curve is just a generic illustration and the slope value is not the point.
   - Common consequence of `equal_scale: true`: the chart becomes tall-and-narrow when the y-span is larger than the x-span, or short-and-wide otherwise. Adjust `x_length` and `y_length` together (typically `0.5` to `0.7` manim units per chart unit fit comfortably between title and bottom annotation).
   - **Lint rule:** `graph-focus-axes-equal-scale-mismatch` (ERROR).

4. **`\\varepsilon`-`\\delta` picture canonical pattern.** When a hook draws the geometric reading of the `\\varepsilon`-`\\delta` definition with a curve `f`:
   - Use a custom hook (`graph_focus.annotations` is too thin -- see *Hooks*).
   - The "limit" dot at `(a, L)` is **solid** if `f` is continuous at `a` (i.e., `f(a) = L`), and **hollow** if `f(a) \\neq L` or `f(a)` is undefined. Picking the wrong one misleads about whether the limit looks at the function value.
   - Place the boundary dots **at the box corners** `(a \\pm \\delta, L \\pm \\varepsilon)`, not at the on-curve points `(a \\pm \\delta, f(a \\pm \\delta))`. The corner choice keeps the picture symmetric about the band lines; the curve passes visibly inside the box at both boundaries, which *is* the message of "the graph over the `\\delta`-strip lies inside the `\\varepsilon`-band".
   - **Why the corners cannot also lie on the curve (for a non-linear `f`):** for the curve to pass through both `(a - \\delta, L - \\varepsilon)` and `(a + \\delta, L + \\varepsilon)` we would need `f(a + \\delta) - L = -(f(a - \\delta) - L)`, i.e. `f` is odd-symmetric about `(a, L)`. By Taylor expansion this forces `f''(a) = 0` (more generally, all even-order derivatives at `a` to vanish). Strictly convex / concave functions like `2^{x}` or `\\sqrt{x}` never satisfy this, so the triple coincidence "corner = strip-line = band-line = curve point" is achievable *only* for linear `f` (or a carefully crafted cubic). A linear `f` would deliver the triple coincidence but loses the curvature that makes "`\\varepsilon`-`\\delta` on a curve" the pedagogical point. The Sec. 1.6 hook keeps `f(x) = 2^{x}` and accepts that the curve sits visibly inside the box at the corners.
   - Choose `\\delta` small enough that the actual values `f(a \\pm \\delta)` are visibly inside the `\\varepsilon`-band (not on the band lines). Aim for at least 20% of the band's half-width as the gap on each side. The Sec. 1.6 hook uses `\\varepsilon = 1.5`, `\\delta = 0.20` for `f(x) = 2^{x}` at `a = 3`; both gaps land at 0.31 and 0.46 chart-y, comfortably inside.

5. **Function honesty.** The `label` text **MUST** match the function actually plotted. Do not draw `1.15 * x**2` and label it `f(x) = x^{2}` -- a careful student will check. Either change the function to plain `x**2` or include the coefficient in the label. The Sec. 1.1 horizontal-line-test hook used to draw `1.15 * x**2`; it now draws `x**2` so the `f(x) = x^{2}` label is honest, with the intersection dots adjusted to `\\pm \\sqrt{1.25}`.

### `procedure_steps`

- `steps`: imperative sentences in order. One verb each: "Write", "Solve", "Interchange".
- `worked_equations`: a schematic of what the procedure produces, typically a single line with `\cdots` placeholders showing the shape.

#### Strategy boxes vs procedural algorithms (added v1.4)

A `\begin{strategy}` block in the source can be one of two flavours, and both map to the `procedure_steps` template but use `worked_equations` differently:

- **Procedural algorithm** -- a linear sequence of mechanical steps, each producing a definite output (e.g., the Sec. 1.1.3 "Finding the inverse" three-step: write `y = f(x)`, solve, swap names). For these, `worked_equations` holds the *literal output shape*, often a single line of the form `y = f^{-1}(x) = \cdots` showing what falls out at the end.
- **Judgment-type strategy** -- a sequence of moves that includes conditional branches ("if the bound carries an x-dependent factor, ..."), where the steps are *recommendations* that the author applies with judgment (e.g., the Sec. 1.6 four-step `\varepsilon`-`\delta` verification). For these, `worked_equations` holds the *target shape* the strategy aims to produce: the inequality `0 < |x - a| < \delta \Rightarrow |f(x) - L| < \varepsilon` for `\varepsilon`-`\delta` verification, the inequality `|f(x) - L| \le K \cdot |x - a|^p` for a Lipschitz-style bound, etc. The schematic shape is the *goal*, not the *output*.

The template renders both the same way; the distinction is in the author's expectation. Do not split judgment-type strategies into multiple scenes just because the steps are conditional -- that fragments the strategy. Keep them in one `procedure_steps` scene and let the voiceover carry the conditional logic.

### `recap_cards`

- `points`: 4-6 bullets. Each is a one-sentence crystallization of one scene's lesson. These are not a list of topics covered; they are the takeaways.
- `identities`: 1-3 canonical formulas worth memorizing from this video.

---

## Figures: Redrawing the Book in Manim

### Principle

Book figures are authoritative for **what** to show, not **how** to show it. Redraw, do not reproduce.

The book uses TikZ / pgfplots on a light background. The video uses Manim on the Midnight Canvas dark background. Colors, stroke weights, and labeling conventions all differ. A faithful reproduction of the book figure would look wrong in the video design system.

### Workflow

1. **Read the book figure.** Identify the mathematical objects (axes range, function expression, domain, key points, annotations) and the pedagogical purpose (what the student is supposed to notice).
2. **Pick the template.** Function graph -> `graph_focus`. Mapping diagram, interval, arrows -> `graph_focus` with a custom `hook`, or consider the `comparison` template if the figure is genuinely two parallel ideas.
3. **Re-express in Manim terms.** Convert TikZ coordinates to `axes.x_range` / `y_range` and plot `expression`s. Drop decorative TikZ styling (custom arrow tips, colored fills, background grids); the Midnight Canvas defaults handle the visual language.
4. **Animate, do not just display.** A static book figure is a single page; a Manim scene can have the curve trace out with `Create`, the horizontal test line sweep in, and the intersection points flash. Make the motion carry a teaching moment.

### When to use a custom `hook`

Templates cover the common shapes. Reach for a custom hook (an import path under `tools/manim_hooks/`) when:

- The figure is a side-by-side comparison of two graphs with specific coordinated animations (e.g., horizontal line test: "works on the left, fails on the right" with synchronized line sweeps). See `horizontal_line_test_figure` in the Sec. 1.1 storyboard.
- The figure is a mapping diagram with arrows, labels, and bent connectors that no template templates.
- The figure requires composition of multiple graph transforms whose timing needs to be hand-controlled.

Do **not** reach for a hook to avoid learning the template. Most figure jobs fit `graph_focus` with a thoughtful `plots` list.

### When to skip a book figure entirely

If the book figure is a conceptual diagram whose content is already animated inside another scene's `data.math_lines` or `data.steps`, the figure can be skipped. Example: the Sec. 1.1 inverse-composition mapping diagram (`fig:inverse-composition`) is not a separate Manim scene -- its content is already carried by the `composition_identities` scene's math and the `cubic_graph_reflection` scene's geometry. Skipping is legitimate; silently replacing is not. Document the skip in a YAML comment above the neighboring scene so a later editor knows it was deliberate.

### Add Manim visualizations that are not in the book

Far more important than redrawing book figures is adding video-native visualizations where the book only uses prose. The Sec. 1.1 storyboard does this three times:

- `why_x_squared_fails` -- book states in one sentence ("the value 1/4 comes from both 1/2 and -1/2"); video gives it a whole graph scene.
- `cubic_graph_reflection` -- book states reflection across `y = x` in prose; video shows the two curves and the mirror line.
- `restricted_parabola_graph` -- same reflection idea applied to `x^2` and `\sqrt{x}`.

Any prose claim about "the graph is a reflection", "the curve crosses here", "one function is shifted", "domain restriction changes the shape" is a candidate for its own `graph_focus` scene -- *unless* the section is symbol-heavy in the sense of the next subsection.

### When the section is symbol-heavy

Some sections are about logic, quantifiers, and inequalities, not about shapes. The Sec. 1.6 `\varepsilon`-`\delta` definition is the canonical example: its teaching weight lies in the order of quantifiers, the manipulation of absolute-value inequalities, and the construction of a `\delta` from an `\varepsilon`, with at most a single anchor figure to ground the geometric reading. Other examples in the curriculum: convergence tests, Bolzano-Weierstrass, Riemann sums, the formal definition of continuity, induction proofs, integration by parts in its full generality.

For sections of this kind, the "Visual over textual" commitment is **conditioned**, not abandoned:

- **Anchor figure** -- one `graph_focus` scene that captures the section's central geometric idea (for `\varepsilon`-`\delta`: the band-and-strip picture; for convergence: the eventually-bounded-by-`\varepsilon` picture).
- **Contrast figure (optional)** -- one additional `graph_focus` scene only when the contrast itself is the lesson (counterexample, broken hypothesis, divergent case).
- **No supplementary `graph_focus` scenes for individual algebraic worked examples.** Adding a graph to each `\varepsilon`-`\delta` verification would distract from the inequality manipulation, which is the actual content of the scene.

Operational test: estimate, before drafting YAML, what fraction of the section's teaching weight is symbolic / logical (quantifier order, inequality manipulation, definition unpacking) versus geometric (curves, regions, slopes, areas). If symbolic >= 70%, apply the conditioned rule. Sec. 1.6 is roughly 90% symbolic and gets two `graph_focus` scenes (anchor + motivating piecewise function). Sec. 1.1 is roughly 40% symbolic and gets seven `graph_focus` scenes -- each pulling its weight.

This rule does not say "fewer figures". It says "figures earn their place by carrying a teaching beat the symbols cannot, and in symbol-heavy sections the symbols themselves are the beat."

---

## Titles and Scene IDs

### `scene_id`

- snake_case, short, descriptive of the teaching idea not the book structure.
- Good: `one_to_one_definition`, `why_x_squared_fails`, `cubic_graph_reflection`, `existence_theorem`.
- Bad: `scene_3`, `def_1_1_1`, `subsection_1`, `fig_1_1`.
- Must be unique within the storyboard; used as cache keys by the renderer.

### `title` (on-screen scene title)

- Sentence- or Title-case English that a student could read as a standalone thought.
- Use `$...$` for math symbols in titles: `"Why $x^2$ Cannot Be Inverted"`, `"Graphs of $f$ and $f^{-1}$"`. Rendered inside `\textbf{}` -- math stays in math weight, surrounding text is bold.
- Never use the book's section or subsection heading verbatim. The Sec. 1.1 book has `\subsection{One-to-one functions}`; the video opens with `"Inverse Functions"` and the one-to-one scene is titled `"One-to-One Functions"` -- similar but adjusted for standalone reading.
- Descriptive > structural. Prefer `"How to Find an Inverse"` over `"Section 1.1.3"`.
- A little flavor is acceptable for added scenes -- `"A Concrete Example"`, `"Testing with Algebra"`, `"Key Takeaways"`. Do not force it.

---

## Timing and Scene Exits

### `scene_exit`

A scene **SHOULD** use `scene_exit: "hold"`. The voiceover is almost always longer than the animation, and `hold` keeps the final frame visible while the TTS finishes. `scene_exit: "fade"` is appropriate only for genuinely brief `section_transition` scenes. A storyboard **SHOULD NOT** use `scene_exit: "none"` without a specific reason recorded in a YAML comment.

### `timing`

Three fields, all in seconds:

- `lead_in_seconds`: `0.2-0.3`. Small breathing room before animations begin.
- `hold_after_seconds`: `0.4-1.0`. How long the final frame lingers after the last animation. Use higher values (`0.8-1.0`) for graph scenes and the recap, so the student can absorb. Use lower values (`0.4`) for transitions.
- `minimum_duration_seconds`: a floor, not a cap. Use `3.0` for transitions, `5.0-6.0` for standard content scenes, `7.0` for theorem_proof with multi-step proofs or long example walkthroughs.

The renderer caches scenes on the **visual payload** (template, title, data, theme, hook). Changing `voiceover` or `timing` does **not** force a re-render -- narration-only edits are cheap. Use this to iterate on the spoken script without paying the Manim cost.

---

## `content_type`: Accent Color Disambiguation

The `content_type` field sets the scene's accent color per the Midnight Canvas content-type map. Most templates infer a reasonable default, but the following patterns are worth making explicit:

| Scene flavor | `content_type` | Accent role |
|---|---|---|
| Formal definition | `definition` | cool cyan (`secondary`) |
| Main theorem / key result | `theorem` | warm gold (`accent`) |
| Secondary formal statement | `proposition` | cool cyan |
| Worked example | `example` | yellow highlight |
| Counterexample, pitfall, failure mode | `warning` | coral red |
| Numbered procedure | `procedure` | neutral |
| Closing summary | `recap` | neutral gathered |

`content_type` **MUST** be set explicitly on every `definition_math` scene, because that template carries definitions, theorems, and propositions and the renderer cannot infer which one from the template alone.

Set `warning` for counterexample scenes like `why_x_squared_fails`. This is how the "watch out, this is where the failure is" moment gets its coral accent.

---

## Ordering Heuristics

The scene order is not just the order things appear in the book. Rearrange freely for pedagogy.

Preferred flow for a single section:

1. **Open.** `title_bullets` with 2-3 bullets that preview the question of the video.
2. **Motivation / first concept.** The definition that opens the section, spoken plainly before formalism.
3. **Concrete example of the new concept.** If the book has a real-world or numerical example, put it before the algebraic example. Students attach the definition to the concrete case first.
4. **Algebraic example.** Symbolic treatment of the same idea.
5. **Visual/graphical support** if prose makes a geometric claim.
6. **Supporting proposition / lemma** if stated in the book.
7. **Section transition** if the section has distinct subsections.
8. **Next concept -- repeat 2-6 as needed.**
9. **Procedure** if the section codifies an algorithm.
10. **Worked example applying the procedure.**
11. **Any reflection / symmetry / graphical visualization of the worked example.**
12. **Domain-restriction / edge-case example** if the book has one.
13. **Graphical support for the edge case.**
14. **Recap.** 4-6 takeaway points + 1-2 canonical identities.

The Sec. 1.1 storyboard follows this flow closely; compare scene by scene if uncertain.

### Forward-reference scenes (added v1.4)

Some chapter sections close with a paragraph that introduces a concept whose systematic study belongs to a later chapter -- e.g., the Sec. 1.6 *continuity* preview, which says "if the limit at `a` equals the value at `a`, we call `f` continuous at `a`; we will study this in a later chapter." These paragraphs are *forward-pointing* (per *Prose-Only Scenes* above) and **SHOULD** be promoted to their own scene rather than folded into the recap. Pattern:

- **Template**: usually `definition_math` (the preview almost always carries one equation worth animating). `section_transition` is acceptable only if no equation is involved -- rare.
- **`content_type`**: `definition` even though the formal definition belongs to a later chapter; the on-screen content reads as a definition-shaped statement.
- **Voiceover register**: open with a "before we close, here is a glimpse of where this leads" framing; close with "we will study this systematically in a later chapter". **Do not name the chapter number** -- the video's life cycle is independent of the book's chapter ordering.
- **Position**: *between* the section's main content and the `recap`. The forward reference is part of the recap's lead-up, not the recap itself.

The Sec. 1.6 `continuity_preview` scene is the worked example; treat it as the canonical pattern when promoting a forward reference.

---

## Hooks

A `hook` is a dotted Python path to a custom animation function (e.g., `tools.manim_hooks.ch01_inverse_functions.horizontal_line_test_comparison`). It overrides the default template rendering for that scene.

### When to use a hook

- The scene needs a layout no template provides (two small graphs side by side with coordinated line sweeps).
- The scene needs an animation sequence that cannot be expressed via `math_lines` animation hints alone.
- The scene reuses a non-trivial motion that will appear in multiple chapters (define it once in a hooks module, reuse).
- **The scene is a single graph but carries dense schematic markup that exceeds `graph_focus.annotations`** -- e.g., paired horizontal-and-vertical dashed bands forming an `\varepsilon`-`\delta` cross-hair, projection lines that link points across both axes, hollow markers distinguishing limit values from function values, double-arrow labels for band widths. `graph_focus.annotations` are short captions (six and a half units wide), not schematic primitives. The Sec. 1.6 `epsilon_delta_picture` scene takes this route -- its hook is `tools.manim_hooks.ch01_precise_limit.epsilon_delta_picture`.

### When not to use a hook

- The scene is a mild variation on `definition_math` or `example_walkthrough`. Stick with the template; use `animation: "highlight"` and `math_layout: "equals_aligned"` to get what you need.
- The scene's visual would fit `graph_focus` with the right `plots` list. Every added `graph_focus` scene in Sec. 1.1 is hook-free except the one that genuinely needs side-by-side panels.
- You have not tried the template yet. Templates are richer than they look; read the template catalog before writing a hook.

### Where to put hooks

- Chapter-scoped: `tools/manim_hooks/ch<NN>_<topic>.py`. The Sec. 1.1 hooks live in `tools/manim_hooks/ch01_inverse_functions.py`.
- Cross-chapter motion primitives: `tools/manim_templates/animations.py` (but only if the primitive is genuinely template-level).

---

## Pre-render Checklist

Before running `manim_render_lesson.py`:

### Content
- [ ] Every `\begin{definition}`, `\begin{theorem}`, `\begin{proposition}`, and `\begin{example}` in the source section is covered by a scene.
- [ ] No `\begin{exercise}` content leaked into the storyboard.
- [ ] Opening hook and closing recap are present.
- [ ] Every prose claim about graph shape, reflection, or geometric behavior has a visualization scene (or a deliberate skip noted in a comment) -- subject to the symbol-heavy exception in *Overall Philosophy* #3 and *When the section is symbol-heavy*.
- [ ] Every non-environment paragraph in the source has been classified as Incorporative / Bridge / Forward-pointing and either folded into a neighbouring scene or promoted to its own scene per *Prose-Only Scenes*.
- [ ] Every `% expansion:` marker in the source has been handled per *Expansion Marker -> Storyboard Treatment*; deviations carry a YAML comment.
- [ ] Forward-pointing prose (preview of a later chapter's concept) has its own scene, not folded into the recap.

### Voiceover
- [ ] Every `voiceover` is 3-7 sentences for standard content scenes (`definition_math` / `graph_focus` / `procedure_steps`, with +1 boundary tolerance applied); 1-2 for `section_transition` (3-5 for the v1.4 concept-transition use); up to 9 for `example_walkthrough` with bundled verification *and* satisfying the three carve-out conditions; 5-9 for `theorem_proof`; 5-8 for `recap_cards`.
- [ ] No voiceover references section numbers, figure numbers, equation labels, or "see above/below".
- [ ] Math symbols are written as spoken English (`f of x one`, not `f(x_1)`); `\varepsilon`-`\delta` and quantifier vocabulary follow the spoken-math table.
- [ ] Opening sentence of every voiceover is a hook or transition, not "In this scene...".
- [ ] Closing sentence is a takeaway or bridge.
- [ ] In a section with two or more same-pattern `example_walkthrough` scenes, the second and later scenes do not re-establish the setup.
- [ ] Aligned algebraic chains are read with the LHS on the first line only; middle lines read connector + RHS; closing line names a return-to-LHS contradiction explicitly when applicable.

### Data
- [ ] Every `definition_math` scene has both `statement` (English) and `math_lines` (symbolic).
- [ ] `example_walkthrough` scenes use `equals_aligned` when the algebra shares an `=` anchor.
- [ ] `example_walkthrough` scenes whose voiceover calls back to an earlier `math_line` or `step` set `data.decay_previous: false`.
- [ ] `transform_from_previous` is used between evolving equations, `highlight` on the final line.
- [ ] Every `graph_focus` plot has its `x_range` set to the restricted domain if relevant, and `label_side` / `label_x` set when labels could overlap.
- [ ] `cbrt(...)` is used for cube roots, not `**(1/3)`.
- [ ] Every `graph_focus` `kind: function` plot has a `label` (or shares a labelled segment with the same expression). Hook scenes render their own function label inside the hook code, placed in the empty wedge adjacent to the curve (not in a far corner).
- [ ] Every `graph_focus` `kind: point` plot sets `hollow: true|false` explicitly. Hooks draw hollow circles via `Dot(..., fill_opacity=0, stroke_width=2)`.
- [ ] Scenes whose pedagogical message depends on the visual x:y ratio (slopes, reflections about `y = x`, `\\varepsilon`-`\\delta` boxes, geometric figures) set `axes.equal_scale: true`.
- [ ] Every graph scene has been previewed with `manim_preview_graph_focus.py`.

### Metadata
- [ ] `content_type` is explicit on every `definition_math` scene.
- [ ] `scene_exit: "hold"` is set everywhere except short transitions.
- [ ] `timing.hold_after_seconds` is `0.8-1.0` on graph scenes and the recap.
- [ ] Every `scene_id` is unique, snake_case, and descriptive.
- [ ] Every `title` reads as a standalone thought.

### Sanity
- [ ] Export `narration.md` and read the entire thing end to end. If any paragraph sounds like a textbook, rewrite it.
- [ ] Estimate total duration: (sum of `minimum_duration_seconds`) x 1.5 is a rough lower bound. A one-section video in the 6-10 minute range is healthy.

---

## Maintenance: When the Handout Changes

When `chapters/*.tex` changes in a way that affects a section already storyboarded:

1. **Diff the section.** Identify which formal environments were added, removed, or rewritten.
2. **Update the relevant scenes.** A renamed variable, a rewritten example, or a new definition each requires surgical edits -- not a full storyboard rewrite.
3. **Re-check voiceover for consistency.** If the handout's notation changed, voiceovers that reference that notation must be updated too.
4. **Re-preview changed graph scenes** before rendering.
5. **Do not regenerate the storyboard from the deck JSON.** The storyboard is the source of truth; regeneration would lose all manual authoring.

If the handout changes are large (an entire subsection rewritten), a partial rewrite of the storyboard is appropriate. In that case, keep the old file as `<deck_id>_vN.yml.bak` temporarily, but delete the backup once the new version is rendered and accepted.

---

## Changelog

- **v1.6** -- added the *Graph scene conventions* sub-section under `### graph_focus` and four matching pre-render checklist items, after a Sec. 1.6 review session surfaced four authoring traps that the v1.5 rules did not cover. Each rule has a mechanical lint counterpart where possible:
  - **Function labels mandatory.** Every unique `kind: function` expression in a non-hook `graph_focus` scene MUST carry a `label`. Lint rule `graph-focus-function-needs-label` (ERROR). Multi-segment piecewise functions only need one label between segments. Hooks are responsible for their own labels.
  - **Hook label placement** -- in hook code, the function label belongs in the *empty wedge adjacent to the curve*, not in a far corner of the chart. A label in the wedge reads as the curve's name; a corner label reads as a free-floating annotation that the eye does not attach. The Sec. 1.6 `\\varepsilon`-`\\delta` hook initially placed `f(x) = 2^{x}` at the upper-left corner `(0.85, 12.2)`; a reviewer flagged this as "too far from the curve". Moved to `(1.5, 5.5)` -- in the lower-left wedge between the curve and the `L - \\varepsilon` band line -- with a footprint check (sample the curve at `label_x \\pm half_width` and require the curve's right-edge value to clear the label vertically) so the label cannot accidentally cross the rising curve.
  - **Hollow vs solid dot is explicit.** Every `kind: point` MUST set `hollow: true|false`. Lint rule `graph-focus-point-hollow-explicit` (WARN). Defaulting silently to solid had produced a wrong render where a hollow circle appeared at a continuous point, suggesting `f(a)` was undefined when it equalled `L`.
  - **Equal-scale opt-in.** New `axes.equal_scale: bool` field (default `false`). When `true`, lint rule `graph-focus-axes-equal-scale-mismatch` (ERROR) enforces `x_length / x_span == y_length / y_span` so slopes and geometric ratios render faithfully. Use this on any figure whose pedagogical message depends on visual proportion.
  - **`\\varepsilon`-`\\delta` canonical pattern.** Codified the box-corner dot placement (boundary dots at `(a \\pm \\delta, L \\pm \\varepsilon)`, not at on-curve points) and the continuity-of-`L`-dot rule. Comes from a Sec. 1.6 hook that originally used a hollow `L`-dot for a continuous `f` and on-curve boundary dots, both of which produced asymmetric / misleading renders. A round-trip with the reviewer asking "make the corners triple-coincide with the curve as well" surfaced the deeper constraint: that triple coincidence forces `f''(a) = 0` (Taylor argument on the symmetry between `f(a + \\delta) - L` and `L - f(a - \\delta)`), so it is achievable only by a linear `f`. The pedagogical trade-off -- linear `f` for triple-coincident corners vs. curved `f` with corners visibly off-curve -- is now spelled out in rule 4 so the next author does not re-litigate it.
  - **Function honesty.** The label text MUST match the plotted expression. Documentation only -- the rule is hard to lint mechanically without parsing both, but keeping function and label in sync is a SHOULD all hook authors are expected to follow.
  - Two template-side bugs were fixed in the same pass and are now load-bearing for the lint rules to make sense: `graph_focus` now respects `hollow: true` (previously silently ignored, every dot rendered solid) and `label_x` now resolves through `axes.input_to_graph_point(...)` (previously fell through to a `NumberLine.point_to_proportion` call that does not exist on Manim Community, so every `label_x` setting silently fell back to bounding-box positioning).

- **v1.5** -- voiceover sentence-count rule recalibrated against actual lint output. The first run of [`tools/manim_storyboard_lint.py`](tools/manim_storyboard_lint.py) against `ch01_inverse_functions.yml` produced four `voiceover-sentence-count` warnings (`existence_theorem` 8, `recap` 7, `composition_identities` 7, `why_x_squared_fails` 7); on review, none were defects in the storyboard. They were gaps in the v1.4 rule. Three changes:
  - **`theorem_proof` carve-out (5-9 sentences)** -- a `theorem_proof` carries statement + proof beats and lands above six sentences as the normal case, not the exception.
  - **`recap_cards` carve-out (5-8 sentences)** -- recap voiceover walks four to six bullet points plus a framing sentence; squeezing this into 3-6 forces two takeaways per sentence.
  - **+1 boundary tolerance for standard scenes** -- a standard `definition_math` / `graph_focus` / `procedure_steps` scene that lands at exactly seven sentences is acceptable. The actual SHOULD limit is now eight. Buying a clean takeaway with one extra sentence is not a defect.
  Lint tool updated to match. The pre-render checklist's voiceover line was rewritten to reflect the new ranges.

- **v1.4** -- added Sec. 1.6 *The Precise Definition of a Limit* ([`inputs/manim_storyboards/ch01_precise_limit.yml`](inputs/manim_storyboards/ch01_precise_limit.yml)) as a deliberately contrasting second exemplar -- symbol-heavy where Sec. 1.1 was graph-heavy. The rules that follow came from the pressure test of taking Sec. 1.1's patterns through a section where they had not been calibrated. Substantive additions:
  - **Prose-Only Scenes** -- a new section classifying non-environment paragraphs as Incorporative / Bridge / Forward-pointing and prescribing fold-vs-promote rules. Sec. 1.6 had four such paragraphs the v1.3 mapping table did not cover.
  - **Expansion Marker -> Storyboard Treatment** -- a new section mapping each `% expansion:<category>` from the chapter authoring system to a default storyboard handling, so authors do not re-classify what the chapter author already classified.
  - **Forward-reference scenes** -- a new pattern in *Ordering Heuristics* for closing previews of later-chapter concepts (e.g., the Sec. 1.6 continuity preview). These get their own scene with a "before we close, here is a glimpse" register.
  - **When the section is symbol-heavy** -- a new section conditioning the *Visual over textual* commitment for sections whose teaching weight is at least 70% symbolic / logical. In such sections, `graph_focus` is restricted to one anchor figure plus an optional contrast figure.
  - **Aligned chains in voiceover** -- a new sub-section under *Voiceover* prescribing how to read aloud a derivation aligned on `=` / `\le` / `<` without making the TTS chant the LHS once per line.
  - **`\varepsilon`-`\delta` and quantifier extension** to the spoken-math table -- previously the table was tuned for inverse functions; it now covers `\varepsilon`, `\delta`, `\delta_1`, absolute-value distance, `\min`/`\max`, and the spoken-English forms of `\forall` and `\exists`.
  - **Repeat-pattern voiceover savings (MUST)** -- second and later same-pattern examples in a section must not re-establish the setup the first example built; they open with a transition phrase and go straight to the new content.
  - **9-sentence carve-out conditions** -- the carve-out now lists three explicit conditions (three or more distinct algebraic moves; presence of a verification beat; splitting would break the procedure -> verification time order). When any one fails, fall back to the six-sentence cap.
  - **Strategy boxes vs procedural algorithms** -- a sub-rule under `procedure_steps` distinguishing judgment-type strategies (with conditional branches) from linear algorithms; both use the same template but `worked_equations` plays different roles (target shape vs literal output).
  - **Hook trigger #4** -- a single graph with dense schematic markup (paired bands, projection lines, hollow markers, double-arrow labels) now warrants a hook even without side-by-side panels. The `epsilon_delta_picture` figure was the trigger.
  - **`section_transition` widened** -- the template now also covers concept transitions inside a section that has no formal subsections, with a 3-5 sentence carve-out for jumps that need genuinely more space than a brief interlude.
  - **Edge case: proof whose body is an aligned algebraic chain** -- `theorem_proof`'s schema cannot align an inequality chain on its relation symbol; the prescribed workaround is to split into a `definition_math` statement scene and an `example_walkthrough` proof scene with `math_layout: equals_aligned`.

- **v1.3** -- added a SHOULD rule for `example_walkthrough` `data.decay_previous`: scenes whose voiceover calls back to an earlier `math_line` or `step` should set it to `false`. Added a matching pre-render checklist item. Motivated by the Sec. 1.1 v2 preview render, where `example_walkthrough` scenes with default `decay_previous: true` dimmed earlier lines before the TTS narration reached its verbal reference to them.
- **v1.2** -- refined the voiceover sentence-count SHOULD based on audit findings from the Sec. 1.1 v2 rewrite. The 3-to-6-sentence target was being violated in 10 of 19 scenes, but on review the violations were not defects: `section_transition` scenes are naturally 1-2 sentences (they are interludes), and `example_walkthrough` scenes that bundle procedure plus verification are naturally 7-9 sentences (one cohesive teaching idea, not two). Two carve-outs now written into the rule and into the pre-render checklist. No other rules weakened.
- **v1.1** -- added a Conformance Keywords section (MUST / SHOULD / MAY) and rewrote load-bearing rules (scene decomposition, exercise exclusion, voiceover must-nots, `cbrt` usage, `content_type` on `definition_math`, `scene_exit` default) to use the new keywords. Added two worked before/after examples: Sec. 1.1.1 one-to-one definition (definition -> `definition_math`) and Sec. 1.1.3 cubic inverse example (example + solution -> `example_walkthrough`). Softened the single-exemplar framing so Sec. 1.1 is a reference calibration point rather than a tiebreaker. Replaced em-dash, en-dash, arrow, section-sign, and multiplication-sign in body text with ASCII equivalents so the file reads cleanly in terminals that degrade non-ASCII to `?`. Paired with cross-doc updates to `README.md`, `MANIM_REFERENCE.md`, and `MANIM_CHECKLIST.md` that unify "direct from LaTeX" as the recommended workflow and demote seeding to a legacy bootstrap path.
- **v1.0** -- initial guide. Derived from reverse-engineering the Sec. 1.1 *Inverse Functions* storyboard against `chapters/ch01_foundations.tex`. Covered scope, scene decomposition, environment->template mapping, voiceover rewriting, `data` shaping, figure handling, titles, timing, `content_type`, ordering heuristics, hook usage, a pre-render checklist, and handout-change maintenance.
