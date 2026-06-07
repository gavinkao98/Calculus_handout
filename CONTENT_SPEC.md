# Calculus Handout: Master Typesetting Guide

**Version 3.1** — refinement pass on v3.0 after the documentation framework was split into spec + quickstart + roadmap + exercises skeleton, and the preamble/template implementation landed. v3.0 was the from-scratch rewrite replacing versions 1.x and 2.x, reorganizing the rulebook around a specific product definition: a single-sided A4 English handout for high-school students preparing to self-study college calculus, paired with companion videos, written in Stewart / Rogawski register. v3.1 adds content-level refinements (remark usefulness test with good-vs-bad examples, figure redundant-encoding rule for grayscale and accessibility, index lookup test, per-section exercise numbering) on top of that foundation. The Changelog (§16) summarises concrete differences.

---

## 1. Purpose and Audience

This project produces a **calculus handout** for high-school students who want to prepare for or self-study college calculus.

- **Format**: single-sided A4 PDF, printed and distributed as a handout (not bound into a book). Layout is set at 12 pt Times with 3.3 cm symmetric margins; see [`README.md`](README.md) for the preamble-level justification.
- **Audience**: motivated high-school students. They have strong precalculus, some exposure to mathematical reasoning, and enough maturity to stop at a confusing passage and try to work it out themselves, but they are not yet at an undergraduate-math-major level.
- **Companion medium**: video lessons that reinforce the handout.
- **Reader relationship to the text**: **the handout is self-sufficient**. A student who never watches the video should still be able to read the handout end-to-end and absorb the material. The video is reinforcement, not the primary channel. This is the single most important positioning decision and drives most of the rules that follow.

Every rule in this document serves one of three goals:

1. **Clarity over compactness.** A self-study reader must not get stuck. If a rule forces a thicker book but a clearer reading experience, the rule is right.
2. **Consistency across multiple authors.** The book draws on manuscripts from several instructors; the rules exist so that a reader moving from Chapter 3 to Chapter 7 does not feel the change in voice.
3. **Lookup-friendliness.** Self-study readers flip back. Index entries, per-type counters, labeled formal statements, and a chapter-end Summary all support this.

---

## 2. How to Read These Rules

### Conformance keywords

This document uses three levels of obligation:

- **MUST** — the rule is binding. Violations are defects.
- **SHOULD** — the rule is the default. Deviations are acceptable when the rationale shifts in a specific case, but the author must be able to explain the deviation to a reviewer.
- **MAY** — the option is permitted. Absence of usage is not a defect.

A rule without a keyword is equivalent to SHOULD.

### Rationale

Most rules are followed by a **Rationale** paragraph that explains why the rule exists. Rules are the normative layer ("what to do"); rationales are the interpretive layer ("why this rule and not its opposite"). When a new situation falls outside the literal text of a rule, the Rationale is the primary guide for resolving the edge case — extrapolate from purpose, not from mechanical application.

### Relationship to other files

- [`README.md`](README.md) — repository layout, preamble structure, build instructions.
- [`video/README.md`](video/README.md) — current (second-generation) video pipeline (primary media path).
- [`legacy/MANIM_REFERENCE.md`](legacy/MANIM_REFERENCE.md), [`legacy/MANIM_STORYBOARD.md`](legacy/MANIM_STORYBOARD.md), [`legacy/MANIM_CHECKLIST.md`](legacy/MANIM_CHECKLIST.md) — first-generation Manim animation pipeline (frozen; archived under `legacy/`).
- [`legacy/LEGACY_SLIDE_PIPELINE.md`](legacy/LEGACY_SLIDE_PIPELINE.md) — frozen static-slide/PDF path (reference only).
- [`CONTENT_QUICKSTART.md`](CONTENT_QUICKSTART.md) — short daily-reference companion to this file.
- [`CONTENT_ROADMAP.md`](CONTENT_ROADMAP.md) — course arc, chapter order, prerequisites, core skills per chapter.
- [`CONTENT_EXERCISES.md`](CONTENT_EXERCISES.md) — minimum exercise skeleton ahead of the full deferred design round.
- [`chapters/_chapter_template.tex`](chapters/_chapter_template.tex) — starter skeleton for new chapters, encoding the rules in this file.

When repository layout or preamble decisions change, `README.md` is authoritative. When writing or typesetting rules change, **this file** is authoritative.

---

## 3. Register and Voice

### Target register

The handout is written in the register of **Stewart / Rogawski**: accessible to self-study high-school readers, warm without being chatty, rigorous about mathematics without being cold to the reader.

For calibration:

- **Too formal**: Spivak, Apostol, Rudin. Short declarative sentences, "we" only, intuition lives outside formal environments, historical and applied notes are rare. A motivated undergraduate can read these; a high-school student self-studying often cannot.
- **Too informal**: some lecture-note PDFs, pop-math books. Incomplete sentences, heavy slang, ad-hoc structure.
- **Target**: Stewart. Full sentences with explicit connectives, intuition woven through prose and occasionally into definition environments, motivation paragraphs at chapter and section openings, generous worked examples, frequent figures.

Register is **not** an excuse for informal mathematics. Definitions are still precise; proofs are still complete; limit laws are still limit laws. The loosening is in the prose surrounding the mathematics, not in the mathematics itself.

### Pronoun policy

The primary pronoun is **"we"**, including the reader in the argument. This is the Stewart / Apostol tradition.

**"You"** is permitted in two specific contexts:

1. **Gentle reminders or verifications**, turning briefly to the reader: *"You should verify that $f^{-1}(f(x)) = x$ in this example."*
2. **Forward references** that address the reader's future work: *"You will use this idea again when we study derivatives in Chapter 3."*

**"I" / "the author"** — never. This is a multi-author text; first-person singular does not apply.

Imperative mood is standard for setup and observation: *"Let $f$ be a one-to-one function."*, *"Consider the behavior near $x = 0$."*, *"Observe that both sides vanish at $x = 0$."*

### Signposting phrases

The following phrases are encouraged and help the self-study reader track the argument. They are not MUST — overusing any single phrase is worse than leaving a transition implicit — but a draft with zero signposts almost always feels too tight for the target register.

- *Notice that...* / *Observe that...* — drawing attention to a feature just demonstrated.
- *Let us now...* — announcing a new step.
- *In other words...* — paraphrasing a just-given formalism in plainer language.
- *To see why this matters...* — leading into a motivation paragraph.
- *We are ready to state...* — transitioning from setup to a formal statement.
- *Before we proceed...* — pausing for an aside or reminder.

Avoid fillers (*basically*, *actually*, *essentially* used as hedges), over-familiarity (*you guys*, *super easy*), and blackboard shorthand (*iff*, *w.r.t.*, *s.t.* in running prose — expand these out).

### Intuition before formalism

A formal statement (definition, theorem, proposition, corollary) **SHOULD** be preceded by one or two paragraphs of prose that explain why the concept is worth introducing and what it should mean intuitively.

A `definition` body **MAY** end with one sentence of the form *"Informally, this means..."* giving a vernacular restatement, **when the formal statement is syntactically heavy** — that is, when it uses nested quantifiers (e.g., $\varepsilon$-$\delta$), multiple logical clauses, or symbol-dense notation that is hard to parse on first reading. **Skip the inline gloss when the formal statement already reads as near-English with one or two symbols** (e.g., $f^{-1}(y) = x \Longleftrightarrow f(x) = y$); in that case any motivation belongs in prose **before** the definition or in a following remark.

The informal sentence **MUST NOT** introduce examples, figures, or new notation — if the restatement needs those, promote it to a separate remark or prose paragraph following the definition.

Rationale: Stewart register plus self-sufficient handout means the reader cannot rely on a teacher to "translate" the formal statement in real time. The handout itself must do that translation, usually twice — once in motivation prose before the formal statement and once (when syntactically heavy formalism warrants it, e.g., $\varepsilon$-$\delta$) as an inline gloss inside the definition. The "skip when near-English" clause exists to prevent the inline gloss from becoming a reflex: a definition whose symbolic body is already vernacular gains nothing from a paraphrase.

### Style do / don't

**Prefer:**
- concise mathematical prose, complete sentences, direct statements, clear transitions;
- guided worked examples (see §5);
- explicit logical connectives (*therefore*, *because*, *in other words*);
- motivation paragraphs before heavy formalism.

**Avoid:**
- lecture-note fragmentation;
- casual spoken fillers or slang;
- unexplained logical jumps;
- multi-sentence "meta" commentary about what the chapter is doing (trust the structure and the bullet list in the chapter opening to do that job);
- inline abbreviations like *iff*, *w.r.t.*, *s.t.* in prose — write them out.

### Voice reference sample

The following passage exemplifies the target voice. When in doubt about register, compare your draft against this sample.

> Not every function can be reversed. If two different inputs produce the same output, we cannot recover the input from the output uniquely. To build a rigorous version of this idea, we first need a name for the functions that avoid this problem.
>
> **Definition.** A function $f$ with domain $A$ is *one-to-one* if $f(x_1) \ne f(x_2)$ whenever $x_1 \ne x_2$. *Informally, a function is one-to-one when different inputs always give different outputs.*
>
> Notice how this condition rules out exactly the problem described above. If two different inputs $x_1$ and $x_2$ gave the same output, there would be no way to decide which one was "the" input corresponding to that output, and the reverse direction would be ambiguous.
>
> To check whether a specific function is one-to-one, we can use a graphical test that you have likely seen before in precalculus...

Key features of this voice:

- A motivation paragraph precedes the definition ("Not every function can be reversed...").
- Intuition appears inside the definition body (the italicised *"Informally, ..."* sentence).
- Prose after the definition unpacks the condition (*"Notice how this condition rules out..."*).
- Explicit bridges (*Notice how*, *To check...*) guide the reader through each transition.
- "We" is the default; "you" appears as a gentle forward-reference ("you have likely seen...").

---

## 4. Document Structure

### Heading hierarchy

Use four levels:

1. `\chapter{...}` — Title Case.
2. `\section{...}` — Title Case.
3. `\subsection{...}` — sentence case.
4. `\paragraph{...}` — sentence case, unnumbered, not in the table of contents.

**MUST NOT** use `\subsubsection`. When a subsection needs to be split into more than about four subtopics, either break it into two subsections (preferred) or use `\paragraph{...}` headings for each subtopic.

Rationale: limiting numbered depth to three levels keeps the table of contents readable. `\paragraph` provides a lightweight fourth tier for short parallel subtopics without inflating the ToC.

### Heading capitalisation

- `\chapter{...}` and `\section{...}`: **Title Case** (e.g., *Inverse Functions and Limits*, *The Precise Definition of a Limit*).
- `\subsection{...}` and `\paragraph{...}`: **sentence case** (e.g., *Computing limits algebraically*, *Restricted sine and arcsine*).
- Proper nouns stay capitalised regardless of case style (e.g., *Newton's method*, *Stewart's notation*).

Rationale: the capitalisation contrast signals hierarchy visually. Title-cased sections read as named landmarks that a student looks up in the ToC; sentence-cased subsections read as continuations of the running argument.

### Section title content

A section title **MUST NOT** substantially repeat the chapter title. Name the specific theme a section develops, not the chapter's overall topic.

*Example.* A chapter titled *Inverse Functions and One-to-One Functions* should have sections such as *Inverse Functions* and *One-to-One Functions*, not another *Inverse Functions and One-to-One Functions*.

A subsection title **SHOULD** name the unifying theme of its content, not merely enumerate the objects inside. Prefer *Limits of piecewise-defined functions* over *The absolute value function and the greatest integer function*.

### Chapter opening

Every chapter **MUST** open with the following two elements, in order, placed immediately after `\chapter{...}` and before the first `\section{...}`:

1. **An overview** of 1-2 paragraphs of prose, which:
   - names the mathematical territory the chapter covers;
   - connects the chapter to earlier chapters (if any);
   - previews the central results the reader will see.
2. **A learning-outcomes bullet list** headed *"By the end of this chapter, you will be able to:"* (or equivalent), containing 3-5 concrete outcomes and occupying at most half a page.

The overview is prose, not a definition, theorem, or remark. It **MUST NOT** introduce new notation or state formal results.

The bullet list uses verbs that describe what the reader will be able to *do* (*solve*, *compute*, *recognise*, *prove*), not what the chapter will "cover" or "discuss".

*Example.*

```latex
\chapter{Inverse Functions and Limits}

This chapter develops two themes that together form the starting point of calculus.
The first is ... (1-2 paragraphs of prose)

\paragraph{By the end of this chapter, you will be able to:}
\begin{itemize}
    \item determine when a function has an inverse, and construct the inverse when it exists;
    \item work with the inverse trigonometric functions and their principal ranges;
    \item estimate limits from tables and graphs, and compute them using the limit laws;
    \item state and apply the precise $\varepsilon$-$\delta$ definition of a limit.
\end{itemize}

\section{Inverse Functions}
...
```

Rationale: self-study readers open a chapter asking *"what am I going to learn here?"* The bullet list answers that question in five seconds. The overview answers *"how does this fit with what I already know?"* in half a minute. Both must be present.

### Section opening

Every section **SHOULD** open with 1-2 paragraphs of motivation, intuition, or applied context before the first formal environment.

Exception: a short section whose content is purely computational (e.g., *Direct substitution*, *Algebraic simplification of limits*) **MAY** start with a single connecting sentence that links it to the preceding section, skipping the motivation paragraph.

Rationale: self-study readers need a reason to care before they invest reading effort. A section that starts with *"Definition 1.1."* on its first line asks the reader to take the reward on faith.

### Chapter closing

Every chapter **MUST** close with a `\section*{Summary}` block, half a page to one page long, containing three parts in order:

1. **Key definitions** — a bulleted list of definition terms introduced in the chapter, in order of appearance, each as a single line referencing the definition by name (no restatement of the full formal body).
2. **Key theorems, propositions, and corollaries** — a bulleted list of named formal results with a one-sentence plain-English restatement each.
3. **Key formulas and identities** — the 3-8 most important formulas the reader should memorise, presented compactly.

The Summary does not introduce new content. It does not appear in the numbered section sequence (note `\section*`). It **SHOULD** appear before any end-of-section exercise TODO marker for the last section (see §14).

Rationale: this is the reader's permanent reference page. A student who read the chapter a month ago and wants to review it should be able to re-absorb the skeleton in under five minutes using only the Summary.

### Chapter-level toggles

`main.tex` carries two top-level toggles worth knowing about:

- `\ifprintbibliography` — controls whether the bibliography is emitted in the final PDF.
- `\ifincludescratchchapter` — controls whether `chapters/_scratch.tex` is included (default: off, so work-in-progress content does not accidentally ship).

Do not modify these from inside chapter files.

---

## 5. Environment Set

The project uses exactly **12 environments**. New chapter content **MUST** use one of these; new environments **MUST NOT** be introduced without updating this document.

### The 12 environments

**Formal statements** (each has its own counter, chapter-scoped; see §6):

| Environment | Role |
|---|---|
| `definition` | Introduces a new mathematical term. |
| `theorem` | Main / important formal result. |
| `proposition` | Formal result that is useful but not a section's headline result. |
| `corollary` | Immediate consequence of a nearby theorem or proposition, worth naming for pedagogy. |

**Worked material**:

| Environment | Role |
|---|---|
| `example` | Example prompt. Always wrapped in `workedexample`, always paired with `solution`. |
| `solution` | Worked solution to an `example`. |
| `proof` | Proof of a theorem, proposition, or corollary. |
| `exercise` | Problem statement intended for student practice (full design deferred; see §14). |

**Aside and scaffolding** (each has its own counter):

| Environment | Role |
|---|---|
| `remark` | Genuine aside, notation comment, historical note, forward reference. |
| `caution` | Warning about a common error or notation trap. Visually distinct (see §8, §10). |
| `strategy` | Problem-solving strategy or method box. |

**Semantic wrapper** (no counter, no output of its own):

| Environment | Role |
|---|---|
| `workedexample` | Wraps exactly one `example` + one `solution` as a single pagination unit. |

### Translating manuscript labels

Source manuscripts use varied labels. Translate by mathematical role, not surface wording:

| Manuscript label | Target environment |
|---|---|
| Def / Definition | `definition` |
| Property / Thm / Theorem | `theorem` or `proposition` (by role) |
| Note / 註記 | `remark` |
| Warning / ⚠ / 注意 | `caution` |
| Method / Procedure / 解題技巧 | `strategy` |
| Homework / Practice | `exercise` |
| Worked calculation | `example` + `solution`, wrapped in `workedexample` |

### Deliberately excluded

The project does **not** use:

- `lemma` — for the HS audience, the cognitive cost of distinguishing lemma from theorem outweighs the benefit. Results that would be lemmas in a graduate-level book are either absorbed into proofs or promoted to `proposition`.
- `subsubsection` — see §4.
- Any `boxed`, `tip`, or `note` environment — the roles are covered by `remark`, `caution`, or `strategy`.

### Rules per environment

#### `definition`

Use only when introducing a new mathematical term for the first time.

Definitions **MUST** be precise, formal, and concise.

A definition body **MAY** end with one sentence of the form *"Informally, this means..."* giving a vernacular restatement. The informal sentence **MUST NOT** introduce examples, figures, or new notation.

**MUST NOT** open a `definition` for a term that the chapter will not use or develop again. Forward-looking previews of terms to be defined later go in prose, optionally with an `\index{...}` entry, not in a formal environment.

Rationale: a formal definition is a promise that the term is now available for reuse. Using `definition` for terms the chapter never invokes again dilutes that promise and clutters the cross-reference graph.

#### `theorem`

Reserved for main / important results that students are expected to remember and reuse.

Named theorems (Mean Value Theorem, Intermediate Value Theorem, Rolle's Theorem, Fundamental Theorem of Calculus, Squeeze Theorem, and so on) **MUST**:

1. use `\begin{theorem}[Name]` with Name in Title Case and spelled out in full (`[Mean Value Theorem]`, not `[MVT]`);
2. carry an `\index{Name}` entry inside or immediately after the theorem body.

Rationale: named theorems are the most common lookup target after definitions. The combination of a descriptive title and a matching index entry is the reader's primary path into the book.

#### `proposition`

Formal result that is useful and often reusable, but not a section's headline result. Typical uses: algebraic properties of inverse functions, composition identities for inverse trigonometric functions, uniqueness of limits, the two-sided-limit criterion from one-sided limits.

#### `corollary`

Immediate consequence of a theorem or proposition, named because the consequence is worth calling out for pedagogy. Typical uses: the increasing-function test as a corollary of the Mean Value Theorem; existence of $n$-th roots as a corollary of the Intermediate Value Theorem.

Do not add corollaries mechanically.

#### `example` and `solution`

Every `example` **MUST** be paired with exactly one `solution`, and both **MUST** be wrapped in a single `workedexample` environment.

The `solution` environment is visually distinct from `proof`: a bold "Solution." label (not italic), upright body text, trailing QED box.

- Keep "Solution." inline when the solution body begins with prose.
- If the first real content of the solution is a block (`enumerate`, `itemize`, display math), place `\solutionbreak` at the start of the body so the "Solution." label stands on its own line.
- If the last line of the solution body is display math, place `\qedhere` on that line so the closing QED box stays attached to the formula.

#### `proof`

Use only for genuine proofs of mathematical statements. Do not label worked calculations as `proof`.

A theorem, proposition, or corollary **MAY** appear without a proof. Include a proof when at least one of the following holds:

- the manuscript contains one;
- the proof is logically important for the chapter;
- the proof is pedagogically important for student understanding.

Do not add proofs mechanically.

#### `exercise`

Used inside `\subsection*{Exercises}` blocks at section end. Full exercise-system design (difficulty markers, hints, answer appendix, inline self-check variants) is **deferred** until the book's main content is complete; see §14.

While content is being drafted, every section end **MUST** carry a placeholder:

```latex
% TODO: add \subsection*{Exercises} block with end-of-section problems for Section N.M.
```

#### `remark`

Genuine aside, notation comment, warning about a subtle restriction (when the warning is prose-shaped rather than trap-shaped; see `caution` for trap-shaped warnings), short historical note (2-5 sentences), or forward reference to a later chapter.

Per-chapter **pedagogical target**: roughly **2-3 remarks per section** (so 12-18 per chapter of 6 sections). This is a target, not a production quota. A section with zero natural remarks should stay at zero rather than carry padding to hit the number; a section with five genuinely useful remarks should keep all five rather than drop two to land in range. The usefulness test below is authoritative when the count would force the wrong call.

A `remark` **MUST NOT** carry main-line knowledge that every student must read. If the content is part of the logical flow of the section, write it as prose.

**Usefulness test.** Before adding a `remark`, ask: *would a reader lose something if this paragraph were silently removed?* If the honest answer is "nothing, it just padded the section," drop it. If the answer is "a bit of context, motivation, historical colour, or a future connection that would be missed," keep it.

**Good uses** — these belong in `remark`:

- *Historical note*: *"Euler introduced this notation in 1748 in his* Introductio in Analysin Infinitorum*, where he also first treated $e$ as a limit rather than as the base of the natural logarithm."*
- *Applied motivation*: *"Exponential functions model radioactive decay, continuously compounded interest, and population growth under constant per-capita rates. We will return to each in §3.6."*
- *Forward reference*: *"The composition $f \circ f^{-1}$ we just computed will reappear as the setup for the inverse-function derivative in §4.3."*
- *Prose-shaped subtle restriction*: *"The identity holds for real $a > 0$; extending to complex or negative $a$ requires choosing a branch of the logarithm, which is outside this book's scope."*

**Bad uses** — these do not belong in `remark`; rewrite as indicated:

- *Main-line fact in disguise*: *"Note that the limit laws we just proved also apply when both limits are infinite."* → the reader needs this; promote it to prose, a `proposition`, or a `corollary`.
- *Definition restatement as padding*: *"In other words, a one-to-one function never sends two different inputs to the same output."* → if the definition needs a vernacular gloss, put the *"Informally, ..."* sentence inside the `definition` body, not in a separate `remark`.
- *Example in disguise*: *"For instance, when $x = 2$ we have $f(2) = 5$, which illustrates..."* → if it illustrates, it is an `example` + `solution` inside a `workedexample`, not a `remark`.
- *Trivial tautology*: *"This follows from the theorem above."* → if a reader should notice it, write one sentence of prose connecting the two; a standalone `remark` saying only this is padding.

Short historical or applied motivation notes (2-5 sentences) at chapter or section openings, or immediately before a key concept, are a good use of `remark` and directly support the target register.

#### `caution`

Warning about a common error, notation trap, or easy-to-miss restriction. Visually distinct from `remark` (left red accent bar plus "Caution." label; see §10).

Typical uses:

- Notation trap: *"$\sin^{-1} x$ denotes the inverse sine; it does not mean the reciprocal $1/\sin x$."*
- Domain restriction easy to forget: *"The identity $\arcsin(\sin x) = x$ holds only when $x \in [-\pi/2, \pi/2]$."*
- Sign-error or branch-choice pitfall in a computation.

A `caution` is typically 1-3 sentences. If it is longer, it is probably a `remark` in disguise.

#### `strategy`

Explicit problem-solving strategy or method box. This is the highest-leverage self-study aid the project supplies; use it whenever a section's worked examples would otherwise leave the reader asking *"in general, how do I approach a problem of this type?"*

Typical uses:

- *"Strategy for computing limits: (1) Try direct substitution. (2) If the result is an indeterminate form such as $0/0$, simplify by factoring or rationalising. (3) If neither works, try the squeeze theorem or rewrite using a known limit."*
- *"Strategy for finding an inverse: (1) Verify the function is one-to-one (optionally by the horizontal line test). (2) Solve $y = f(x)$ for $x$. (3) Swap $x$ and $y$."*

A `strategy` is typically a short numbered list, occasionally a paragraph.

Rationale: Stewart-style problem-solving strategy boxes are one of the features that self-study readers most clearly benefit from. The environment makes strategies discoverable by scanning rather than requiring the reader to re-read the worked examples and reverse-engineer the pattern.

#### `workedexample`

Semantic wrapper that measures the combined `example` + `solution` body (capped at 16 baselines) and reserves that much vertical space, so a short example cannot be stranded at a page bottom while its solution slides onto the next page.

**MUST** contain exactly one `example` followed by one `solution`. No nesting; no bundling multiple example-solution pairs into a single wrapper.

**MUST NOT** contain `\footnote`, `\marginpar`, or manual `\hypertarget` inside a `workedexample` body: the body is measured in a box before final placement, so page-anchored material may not relocate correctly.

Maintainer note: `workedexample` depends on a one-shot capture of its body. Do not replace it with a wrapper that re-expands the example/solution body, or the counter and pagination assumptions will drift out of sync.

---

## 6. Numbering and Cross-References

### Counters

Each formal-statement environment has its **own counter**, chapter-scoped:

- `definition` → Definition 1.1, 1.2, 1.3, ...
- `theorem` → Theorem 1.1, 1.2, ...
- `proposition` → Proposition 1.1, 1.2, ...
- `corollary` → Corollary 1.1, 1.2, ...

Aside environments also have their own chapter-scoped counters:

- `example` → Example 1.1, 1.2, ...
- `remark` → Remark 1.1, 1.2, ...
- `caution` → Caution 1.1, 1.2, ...
- `strategy` → Strategy 1.1, 1.2, ...

Figures, tables, and numbered equations also reset per chapter: Figure 1.1, (1.1).

Exercises are the exception and are numbered differently because they sit inside per-section `\subsection*{Exercises}` blocks that are primarily consumed locally:

- `exercise` → Exercise 1, 2, ..., restarting at each `\section`. No chapter or section prefix appears in the displayed number. See [`CONTENT_EXERCISES.md`](CONTENT_EXERCISES.md) for exercise-system rationale; cross-section references to a specific exercise use the label + `\cref` convention in §6 below.

Rationale: high-school self-study readers flip back and ask *"where was Definition 1.3?"*, expecting "Definition 1.3" to be the **third definition** in Chapter 1. A shared counter (used in earlier versions of this project) would break that expectation — "Definition 1.3" might be preceded by intervening theorems and propositions, making the number less informative for lookup. Per-env chapter-scoped counters match the reader's mental model for formal statements and aside environments. Exercises break the rule because a student who has just finished §1.3 and turns to the end-of-section exercises thinks *"Exercise 1, Exercise 2, ..."* rather than *"Exercise 1.3.1, Exercise 1.3.2, ..."*; the book-wide prefix is friction, not information, in that local reading context.

Implementation note: `preamble/theorem_setup.tex` declares each environment with its own `\newtheorem{...}{Label}[chapter]`. The previous `aliascnt`-based shared-counter pattern is removed in v3.0.

### Manual numbering

**MUST NOT** number environments, figures, equations, or section headings by hand. Let the project templates handle numbering.

### Equation numbering

Number a display equation **if and only if** at least one of the following holds:

- the equation is referenced later in the same chapter via `\eqref{...}` or `\cref{...}`;
- the equation is referenced from a later chapter;
- the equation is the formal statement of a theorem, proposition, or corollary.

Otherwise use unnumbered display math `\[...\]` or unnumbered `align*` / `gather*`.

Rationale: an equation number is a promise that the equation will be named later. Numbers that no one references clutter the page and weaken the signal value of the numbers that do matter.

### Labels and cross-references

All cross-references **MUST** use `cleveref`:

- `\cref{label}` for in-prose references (the package inserts the prefix: *Figure*, *Theorem*, *Section*, etc.);
- `\Cref{label}` when the reference begins a sentence;
- `\eqref{label}` for equation references (inserts the parentheses).

**MUST NOT** write `Figure~\ref{...}`, `Theorem~\ref{...}`, or any other manual prefix.

**Label format**: `type:short-description` with hyphens between words. The `type` prefix is drawn from:

`def`, `thm`, `prop`, `cor`, `ex`, `sol`, `exer`, `rem`, `caut`, `strat`, `fig`, `eq`, `sec`, `subsec`.

- Good: `fig:horizontal-line-test`, `thm:squeeze`, `def:limit-precise`, `caut:sin-inverse-vs-reciprocal`.
- Bad: `fig1`, `eq2`, `thm-important`, `horizontal_line`.

Labels on `caution` and `strategy` are **optional**; add them only when the entry is genuinely expected to be cross-referenced.

Rationale: mixing `\cref` and manual `\ref` produces inconsistent spacing and capitalisation. Centralising on `\cref` also means a later decision to abbreviate *Theorem* as *Thm.* in running text is a single package configuration change, not a find-replace across two hundred files.

### Paired definitions at different precision levels

When a concept receives both an informal and a precise (e.g., $\varepsilon$-$\delta$) definition:

1. **MUST** use distinct label keys that indicate the precision level, such as `def:limit-informal` and `def:limit-precise`.
2. The precise definition **MUST** explicitly cross-reference the informal one, e.g., *"This formalises the informal notion introduced in \cref{def:limit-informal}."*
3. The informal definition **MUST** forward-reference the precise one, e.g., *"A precise formulation is given in \cref{def:limit-precise}."*
4. Both count as separate `definition` environments and each increments the `definition` counter.

Rationale: students returning to look up *limit* should find both versions and immediately see the relationship between them. Silent duplication without cross-linking is a common source of confusion in multi-author calculus texts.

---

## 7. Formula Display

The project uses **five** formula display modes. All other variants (manual `align`, `gather`, `eqnarray`, ad-hoc vertical spacing with `\\` and `\vspace`) are forbidden in chapter source unless declared under the Exception Protocol.

### The five modes

1. **Inline math** `\(...\)` — formulas that read as part of a sentence.
2. **Display math** `\[...\]` — formulas that are the visual focus of a paragraph.
3. **`aligneddisplay`** — stacked aligned chain (a sequence of related equations sharing an `=` anchor).
4. **`conditiondisplay`** — formula followed by a domain / range / branch condition as a trailing column.
5. **`\pairdisplay{A}{B}`** — exactly two short comparable formulas displayed side-by-side (auto-stacks if either side is too wide).

The equivalence helpers `\iffstackeddisplay` and `\iffwithconditions` from earlier versions are **removed** in v3.0. Use ordinary display math with `\Longleftrightarrow` plus an inline or prose condition instead.

### When to use each

**Inline math** for:

- single symbols, short expressions, short intervals;
- short conclusions in prose (*"...and hence $f'(0) = 0$."*);
- short target expressions in example prompts that fit comfortably in the sentence.

**Display math** for:

- the central formula in a definition, theorem, proposition, or corollary;
- multi-step calculations the reader should scan vertically;
- formulas using `cases`, `aligned`, or comparable tall structures;
- formulas that are the visual focus of a paragraph rather than part of the sentence flow.

**`aligneddisplay`** when two or more formulas form a list, progression, hypothesis set, or chain of equalities sharing a vertical anchor.

**`conditiondisplay`** when a formula carries a trailing domain, range, or branch condition that benefits from a dedicated column rather than being crammed into the formula or tossed into prose.

**`\pairdisplay`** only when exactly two short formulas are being compared left-to-right (not top-to-bottom). If either side grows past roughly `0.45\linewidth`, the template stacks them automatically; do not rely on the stacking fallback to rescue long content.

Rationale: five modes is the point where semantic distinction stops helping authors and starts imposing decision cost. Earlier versions had seven modes; the two removed in v3.0 (`\iffstackeddisplay`, `\iffwithconditions`) addressed use cases that ordinary display math with `\Longleftrightarrow` plus an inline condition handles cleanly.

### Display block cohesion

Within one local math unit (a single derivation, a single theorem statement, a single solution step), authors **SHOULD** use one display grammar consistently.

This rule is SHOULD, not MUST: mixing grammars when a *genuinely new idea* follows a derivation — for example an `aligneddisplay` chain followed by a final inline conclusion — is natural and acceptable. What the rule forbids is the jumble of one centred display, one `aligneddisplay`, one prose-embedded formula, and one `conditiondisplay` all doing algebraic work in the same three-sentence span.

Concrete guidance:

- If several formulas are peers in one derivation, group them in a single `aligneddisplay`; do not scatter them across separate `\[...\]` blocks.
- If a short follow-up formula reads naturally after prose, keep it inline.
- Do not attach a condition like *"provided that $x \ne 1$"* as an extra alignment column when the condition applies to only one of the aligned rows; move it into prose before or after the display block.

### Inline fractions: `\frac` vs `\dfrac`

Default to `\frac` in inline math. Use `\dfrac` only when the inline fraction becomes genuinely hard to read at reduced size, or when matching a nearby display formula materially helps.

Reserve `\dfrac` for:

- fractions with substantial numerator or denominator structure: $\dfrac{f(x+h) - f(x)}{h}$;
- fractions tracking a specific $\varepsilon$-$\delta$ bound: $\dfrac{\varepsilon}{4}$, when the fraction itself is the object of discussion;
- inline fractions visually paired with an adjacent display equation using the same expression.

Keep `\frac` for running-prose fractions ($\frac{1}{x}$, $\frac{1}{x^2}$, $\frac{\pi}{2}$).

In tables, prefer `\tfrac` or plain-text forms to keep rows compact.

All `\frac` inside display math renders at full size automatically; `\dfrac` inside display math is redundant.

### Inline `\displaystyle`

Use `\(\displaystyle ...\)` **sparingly**, only when both of the following hold:

- the formula must remain inside the sentence, and
- it contains a large fraction, integral, sum, or limit that becomes hard to read at inline size.

*Example permitted*: *"the difference quotient $\displaystyle \frac{f(x+h) - f(x)}{h}$"*.

Do not use `\displaystyle` as a default way to make formulas look "important". If a formula is important enough to stand out, move it to display math.

### Delimiter sizing

- Use `\left...\right` when the enclosed expression contains tall objects (full-size fractions, nested radicals, large operators).
- Use fixed-size delimiters for short expressions: prefer `(x+1)` over `\left(x+1\right)`.
- For interval notation with displayed fractions, `\left[-\tfrac{\pi}{2}, \tfrac{\pi}{2}\right]` is appropriate because `\tfrac` keeps the fraction at reduced height.

### House rule cheatsheet

| Situation | Helper |
|---|---|
| short formula inside a sentence | inline math |
| main formula or visually central expression | display math |
| chain of aligned equations | `aligneddisplay` |
| formula with trailing domain/range/branch condition | `conditiondisplay` |
| exactly two short comparable formulas, side by side | `\pairdisplay{...}{...}` |
| formal equivalence of two statements | display math with `\Longleftrightarrow` |
| inline formula with a large operator, sentence must not break | `\(\displaystyle ...\)` |

---

## 8. Typography

### Dashes

- Hyphen (`-`): hyphenated words such as *one-to-one*, *left-hand*, *real-valued*.
- En dash (`--`): numerical and page ranges such as *pages 12--15*.
- Em dash (`---`): parenthetical interruptions in prose. Use sparingly; a comma or a pair of parentheses is usually better.

### Ellipses

Use `\dots` (context-aware). Do not hard-code `\ldots` or three literal periods.

- In text: *the sequence $a_1, a_2, \dots, a_n$*.
- In display with operators: *$a_1 + a_2 + \dots + a_n$* — LaTeX chooses `\cdots` automatically.

### Quotation marks

- Double quotes in prose: `` ``...'' `` (double backtick open, double apostrophe close).
- Single quotes: `` `...' ``.
- **MUST NOT** use straight ASCII `"..."` in chapter files. This is enforced by `tools/book_style_lint.py`.

### Emphasis

`\emph{...}` is the single permitted emphasis mechanism in running prose.

- `\emph{term}` **MUST** mark the introduction of a new term inside a `definition` body.
- `\emph{term}` **MAY** mark the first occurrence of a term in motivation prose that precedes the formal definition. Use at most once per term.
- **MUST NOT** use `\textbf{...}` or `\textit{...}` in running prose for emphasis. Bold is reserved for environment labels and theorem headings, which the template handles automatically.
- **MUST NOT** emphasise the same term twice.

Rationale: a single emphasis mechanism means the reader learns one visual cue. Multiple emphasis mechanisms in running prose dilute the signal and force authors into style choices that should be pre-decided.

### Visual label of new environments

The `caution` and `strategy` environments use a **left-side coloured accent bar plus a text label**, no icons.

- `caution` — red (`\colorcaution` from `preamble/colors.tex`) accent bar, "Caution." label.
- `strategy` — blue (`\colorprimary`) accent bar, "Strategy." label.

Rationale: Unicode icons (`⚠`, `🔑`) create font-compatibility issues under `newtxtext` + `pdflatex` and are not worth the added complexity for a text-first handout. A coloured accent bar is visually sufficient to distinguish the environment and matches the colour convention in §10.

### Math spacing

- Binary relations and operators: rely on LaTeX's built-in spacing (`\ne`, `\le`, `\ge`, `+`, `-`).
- Differentials in integrals: thin space before the differential (`\int_a^b f(x)\,dx`).
- Function application: no space (`f(g(x))`, not `f( g(x) )`).
- Use `\,`, `\;`, or `\quad` only when alignment or readability genuinely requires it.

---

## 9. Notation

Notation **MUST** remain consistent across all chapters. Use the following standard forms unless a specific manuscript convention is being preserved (in which case a `caution` or `remark` **SHOULD** note the convention choice).

| Concept | Preferred notation |
|---|---|
| Inverse trigonometric functions | `\arcsin x`, `\arccos x`, `\arctan x`, `\arccsc x`, `\arcsec x`, `\arccot x` |
| Logarithms and exponentials | `\ln` (natural log), `\exp` or `e^x` |
| Trigonometric functions | `\sin`, `\cos`, `\tan`, etc. (all via `\operatorname`-style macros, not italicised letters) |
| Derivative | `f'(x)` for the general derivative; `\dfrac{d}{dx}` for an explicit differential operator |
| Two-sided limit | `\lim_{x\to a} f(x) = L` |
| One-sided limits | `\lim_{x\to a^-}`, `\lim_{x\to a^+}` |
| Infinite limits | `\lim_{x\to a} f(x) = \infty`, `\lim_{x\to a} f(x) = -\infty` |
| Real line | `\mathbb{R}` |
| Interval notation | `(a,b)`, `[a,b]`, `[a,b)`, `(a,b]`; for unbounded endpoints, `(-\infty, a)`, `[a, \infty)` |

Do not switch notation style from chapter to chapter without a strong reason. If a manuscript adopts a less-common but mathematically legitimate convention (for example, a non-standard principal range for an inverse trigonometric function), preserve it, and add a `caution` noting a common alternative at first use.

The use of `\sin^{-1}` for the inverse sine is **not** the house notation. If it must be mentioned (e.g., because a reader might encounter it elsewhere), introduce it in a `caution` that disambiguates it from the reciprocal $1/\sin x$.

Rationale: notation drift is one of the most visible inconsistencies in multi-author textbooks. Fixing a small canonical list at the rule level eliminates a whole class of editorial decisions and makes the index far cleaner.

---

## 10. Figures and Colour

### When to use a figure

Figures are pedagogy, not decoration. Add a figure only when it genuinely helps.

**SHOULD** add a figure at or near:

- every important definition, especially geometric or graphical concepts;
- every important theorem with a visualisable statement;
- approximately every 2-3 examples in a computational section.

Do not add decorative figures. Do not add a figure whose purpose is to fill a half-empty page.

Rationale: self-study readers depend heavily on visual intuition. A chapter with one figure per five pages is too sparse for high-school readers; Stewart-density (close to one figure per page on visually rich topics) is the right neighbourhood.

### Tool choice

- **`pgfplots`** — coordinate graphs, plotted functions, asymptotes, analytic behaviour.
- **`TikZ`** — conceptual diagrams, mapping diagrams, intervals, arrows, geometric sketches.

### Multi-panel comparison figures

When two or three related images belong together (e.g., restricted sine / cosine / tangent branches; left-hand / right-hand / two-sided limit graphs), arrange them as a single `figure` environment with side-by-side `minipage` panels.

Rules:

- Horizontal layout of 2 or 3 panels. More than 3 is too cramped; stack vertically in that case.
- A single shared caption describing what the comparison illustrates.
- A small in-panel label under each panel naming that panel (e.g., *Restricted sine*, *Restricted cosine*).

### Callouts and annotations

Figures **MAY** include arrows with short text labels ("callouts") pointing to specific features (*"Here the function is not defined."*, *"Inflection point."*, *"Asymptote."*).

Callout text **SHOULD** be a complete sentence or a complete noun phrase; sentences end with a period, noun phrases do not.

Rationale: self-study readers absorb information from annotated figures significantly faster than from unannotated ones. Stewart-style callouts are the single highest-leverage visual element for the target register.

### Label economy

A figure carries only the labels needed to *read* it: axis names, the dimensions or points the reader must identify, curve labels (see "Redundant encoding" below), and short callouts. Everything else — naming each region or area, restating a formula, spelling out a construction — belongs in the **caption and the body prose**, not crammed onto the drawing.

- **SHOULD** keep in-figure text to the minimum that makes the picture legible. When a label would carry a clause's worth of explanation, move that explanation into the surrounding text and leave only a short anchor on the figure.
- A diagram whose interior reads like a paragraph is over-labelled. Prefer a clean drawing plus a sentence of prose to a drawing dense with formulas.

Rationale: an uncluttered figure is scanned faster, and the body prose is where a self-study reader expects the reasoning to live. (Worked instance: a product-rule area rectangle is labelled only with its side lengths and one anchor for the original area; the strip and corner areas are named in the text, not on the figure.)

### Colour convention

The project uses a three-colour palette, defined once in `preamble/colors.tex` and referenced by macro throughout:

| Colour | Macro | Role | Typical use |
|---|---|---|---|
| Blue | `\colorprimary` | primary / main object | the principal function, the main curve, the focus of the figure; also `strategy` accent bar |
| Red | `\colorcaution` | warning / asymptote | asymptotes, dashed reference lines, visual warnings; `caution` accent bar |
| Gray | `\colorauxiliary` | auxiliary / structural | axis elements, guide lines, reference constructions |

Working-draft hex values: blue `#1f4e79`, red `#c0392b`, gray `#7f7f7f`. Exact values may be tuned at implementation time; the semantic assignment above is fixed.

Additional colours **MUST** be introduced via Exception Protocol (see §13) and documented at the chapter level.

### Redundant encoding for grayscale and accessibility

Colour carries pedagogical meaning but **MUST NOT be the only channel** carrying it. Every figure that uses colour to distinguish curves, lines, regions, or points **MUST** also distinguish them by at least one of:

- **line style** — solid for primary curves, `dashed` for reference lines and asymptotes, `dotted` for auxiliary / scaffolding constructions;
- **labels** — each curve or line labelled near its body (*$f$*, *$f^{-1}$*, *$y = x$*), not only via a colour legend;
- **markers** — `$\bullet$` / `$\circ$` / `$\square$` at key points so labelled points remain distinguishable when colour is lost.

House conventions:

- primary curve: blue (`\colorprimary`), solid, labelled;
- inverse or paired curve: solid or dashed depending on its role in the pair, labelled;
- asymptote or reference line (including `$y = x$`): dashed, red (`\colorcaution`) if it is a warning/asymptote, gray (`\colorauxiliary`) if it is scaffolding; labelled with its equation where space permits;
- auxiliary construction (guide lines, midpoints, reference rectangles): gray, dotted;
- key points: marker `$\bullet$` for filled, `$\circ$` for open, labelled with coordinates or a name.

Figures **MUST** remain readable in grayscale — colour is semantic, layered on top of line-style and marker information, not in place of it.

Rationale: students print on single-sided black-and-white printers, photocopy sections, or read under display conditions that wash colour out. A figure that says "the red curve vs. the blue curve" collapses into two identical grey curves when colour is lost. The existing grayscale-readability target is a promise, not a spot check; redundant encoding is how it gets kept. Redundant encoding also supports colour-blind readers without requiring a separate accessibility pass.

### Placement

- Default to `[H]` (requires the `float` package) so figures stay exactly where the source places them.
- If `[H]` would produce excessive white space on a page, first try to adjust the surrounding prose (reword, trim, or reorder a nearby paragraph).
- If prose adjustment does not resolve the problem, fallback to `[htbp]` or a manual `\newpage` is permitted as a **documented exception** under the Exception Protocol.
- Keep figures sized so that they fit on the same page as the prose that introduces them.

Rationale: for a teaching-oriented handout, proximity of figure to prose is pedagogically important. `[H]` pins the figure in place; `\raggedbottom` (enabled globally in `preamble/layout.tex`) absorbs the extra vertical space. When this trade-off fails locally, an exception is fine, but it must be recorded.

### Captions

- Sentence case.
- Concise and mathematical.
- End with a period.
- Describe the figure's mathematical purpose, not just its contents.

Good: *Geometric interpretation of the horizontal line test.*, *The sine function on $\mathbb{R}$ is not one-to-one.*

Bad: *Graph.*, *Diagram of sine function.*

### Worked-example figures must not reveal the answer

If an `example` asks the reader to compute a side length, angle, or coordinate, the accompanying figure **MUST NOT** show the computed value in its labels. Label the unknown with a variable ($a$, $\theta$) and let the prose derive the value.

Rationale: a diagram that already shows "$3$" next to the side the student is asked to find turns the example into a picture to be copied rather than a calculation to be worked.

### Manuscript priority

If the manuscript already contains a figure idea, preserve its mathematical purpose. Redraw in the clean textbook style specified above; do not preserve handwritten or blackboard styling.

---

## 11. Index Policy

The book has a back-of-book index compiled by `imakeidx`. Build wiring (three-pass compile, automatic under `latexmk -pdf main.tex`) is documented in [`README.md`](README.md).

### The lookup test

Before adding any `\index{...}` entry — mandatory or optional — apply the **lookup test**: *will a reader want to find this item later without remembering which chapter introduced it?* If yes, it belongs in the index.

Items that fail the lookup test do **not** belong in the index, even if the author happens to give them names: a one-off substitution variable inside a single proof, a throwaway example label used only in its own paragraph, an intermediate lemma-style claim the proof never references again, a mnemonic only meaningful in context. Adding these clutters the index and degrades the items that readers actually need to find.

The mandatory and optional lists below are the default answers to the lookup test for their categories. When a specific item in a mandatory category genuinely fails the test in its context (for example, a one-shot applied setting used only for flavour), the lookup test wins: leave it out and note the omission in an exception comment.

### Mandatory entries

An `\index{...}` entry **MUST** appear at the first occurrence of:

1. **Every term introduced by a `definition`** — the primary term and any synonyms used elsewhere.
2. **Every named theorem** — *Squeeze Theorem*, *Intermediate Value Theorem*, *Mean Value Theorem*, *Fundamental Theorem of Calculus*, and so on.
3. **Every notation the book introduces** — `\arcsin`, `\lim`, `\int`, etc., using the sort-key-plus-display form: `\index{arcsine@$\arcsin$}`, `\index{limit@$\lim$}`, `\index{integral@$\int$}`.
4. **Every key example** the book expects readers to remember by name — the $1/x$-near-$0$ example, the $x^{2}\sin(1/x)$ squeeze example, and so on. Format: `\index{1/x near 0@$1/x$ near $0$}`, `\index{x^2 sin(1/x) example@$x^{2}\sin(1/x)$ example}`. "Expects readers to remember by name" is the lookup test: if the example is referenced later in the book or is a canonical counterexample the field itself names, index it. Purely local illustrations of a method do not need an entry.
5. **Every notation trap** that could confuse readers — *sine inverse vs reciprocal*, *absolute value vs interval brackets*, etc. Format: `\index{sine inverse vs reciprocal@$\sin^{-1}$ vs $1/\sin$}`.
6. **Every applied setting that introduces new terminology or will be reused** — *instantaneous velocity*, *tangent line*, *rate of change*, *slope*, *area under a curve*. Purely incidental applications used once for flavour (a beaker of water in an introduction, a numerical example framed around a dropped ball that is never revisited) do not need an entry.

### Optional entries

- Named mathematicians when first mentioned in a historical note.
- Additional example keywords beyond (4).

### Rules

1. Place `\index{...}` at the **first occurrence** of the term, not at every later mention.
2. Use **sentence-case** keys: `\index{one-to-one function}`, not `\index{One-to-One Function}`.
3. Use **sub-entries** via `!`: `\index{limit!one-sided}`, `\index{limit!infinite}`, `\index{asymptote!vertical}`.
4. For notation, always use the sort-key-plus-display form `key@$\text{symbol}$` so the index sorts alphabetically by spelled-out key while displaying the glyph.

Rationale: the index is a self-study reader's primary navigation tool when returning to the book after a gap. A sparse index forces the reader to skim chapters looking for where a concept was introduced; a dense, well-cross-linked index turns every later concept into a two-second lookup. The cost of adding an index entry while writing is tiny; the cost of reconstructing the index later is substantial, and the reconstruction is never as accurate.

---

## 12. Source Hygiene and CI

### What chapter files MAY contain

- `\chapter{...}`, `\section{...}`, `\subsection{...}`, `\paragraph{...}` structure.
- The 12 approved environments from §5.
- The 5 approved formula-display helpers from §7.
- `\index{...}`, `\label{...}`, `\cref{...}`, `\eqref{...}`.
- Prose, including `\emph{...}` per §8.

### What chapter files MUST NOT contain

- Custom macro definitions (`\newcommand`, `\renewcommand`, `\def`, `\newenvironment`, `\providecommand`).
- Manual page breaks (`\newpage`, `\pagebreak`, `\clearpage`).
- Manual cross-reference prefixes (`Figure~\ref{...}`, `Theorem~\ref{...}`, etc.).
- ASCII straight quotes (`"..."`).
- `\textbf{...}` or `\textit{...}` for emphasis in running prose.
- `\footnote{...}`, `\marginpar{...}`, or manual `\hypertarget{...}{...}` inside a `workedexample` body.

Rationale for the no-custom-macro rule: this is a multi-author project. Per-chapter macros produce notational inconsistency (the same concept written different ways in different chapters) and make individual chapters harder to read cold (every reader must first scan a macro block). The shared helpers in `preamble/` already cover recurring cases; if a new case arises, the right response is to add the helper to the preamble (and document it here), not to define it per-chapter.

### Preamble responsibility

New environments, new display helpers, and new colour definitions belong in `preamble/`. When declaring a new environment that wraps `\[...\]` (or any display-math construct), use the `\newdisplayenv{name}{begin}{end}` helper from `preamble/layout.tex`, never plain `\newenvironment`. The helper attaches `\@doendpe` via `\AfterEndEnvironment` so continuation prose after the environment is not spuriously indented.

### CI checks

The continuous-integration pipeline ([`.github/workflows/latex-checks.yml`](.github/workflows/latex-checks.yml)) runs four checks on every push and pull request:

1. **`tools/book_style_lint.py`** — regex-based linter that enforces, at minimum:
   - no manual cross-reference prefixes;
   - no `\newpage` / `\pagebreak` / `\clearpage` in chapter or `main.tex` source;
   - no ASCII `"..."` quotes;
   - no `\textbf{...}` or `\textit{...}` in chapter prose;
   - every `\begin{definition}` body contains at least one `\index{...}`;
   - every `\begin{theorem}[Name]` has a matching `\index{Name}` nearby;
   - every chapter file opens with `\chapter{...}` followed by an overview paragraph and a learning-outcomes bullet list.
2. **`tools/book_preamble_smoketest.py`** — compiles `preamble_smoketest.tex` and verifies that continuation prose after `aligneddisplay` / `conditiondisplay` is not spuriously indented.
3. **`tools/book_docs_lint.py`** — scans repository markdown for stale `tools/<name>.py` command references and broken relative links, so doc-rename drift is caught automatically rather than at review.
4. **`latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error main.tex`** — full build, catching structural errors, missing references, and malformed source.

All four checks **MUST** pass on the feature branch before a chapter is considered ready for review.

---

## 13. Exception Protocol

Individual chapters will occasionally need to deviate from a rule in this document. When that happens, the deviation **MUST** be recorded, not hidden.

### Declaring an exception

Place a comment at the top of the chapter file, immediately after `\chapter{...}`, in the form:

```latex
% Exception: uses [htbp] placement for Figure 3.9 to avoid a full blank page.
% Rule: Figure Placement (§10, default [H]).
% Reason: the four-panel figure is taller than the typical [H] budget,
%         and forcing it produces a near-blank page.
```

### Escalation

If an exception recurs across chapters (three or more instances of the same deviation), raise it for rule revision rather than compounding local exceptions. Rule revision is done by:

1. proposing the change in a pull request that modifies this file and bumps the version number;
2. discussing the change with the project owner;
3. documenting the revision in the Changelog (§16).

### Silent deviations

A chapter without an exception comment is presumed to follow every rule in this document. Silent deviations are defects.

Rationale: rules evolve. An explicit exception record turns a deviation from noise into data, so the rulebook can be revised based on where rules actually fail in practice. The consistency claim ("the book follows its own rules") is verifiable only if exceptions are declared.

---

## 14. Exercises — Deferred Design

Full exercise-system design (environment variants, difficulty markers, hints, answer appendix, inline self-check variants) is **deferred** until the book's main content is complete. Designing the exercise system against real content will produce better choices than designing it in advance against hypothetical content.

### Current obligation during content drafting

Every section end **MUST** carry a placeholder comment of the form:

```latex
% TODO: add \subsection*{Exercises} block with end-of-section problems for Section N.M.
```

The placeholder makes the missing exercise block visible in source and auditable by CI. A section without either a real `\subsection*{Exercises}` block or the TODO placeholder is out of compliance.

### When exercise design opens

When a solid majority of chapters have complete main content (definitions, theorems, examples, prose), the exercise system will be designed in a dedicated round, following the same Q/A consultation structure that produced this document.

---

## 15. Consistency Check Before Final Output

Before committing a chapter or declaring it ready for review, verify:

**Positioning and register**
- [ ] The chapter reads as self-sufficient — a student with no access to the companion video could work through it.
- [ ] Pronouns follow §3: "we" as default; "you" only for gentle reminders or forward references.
- [ ] Intuition paragraphs precede formal environments; the *"Informally, ..."* gloss is used where helpful.

**Structure**
- [ ] Chapter opens with a 1-2 paragraph overview and a *"By the end of this chapter, you will be able to:"* bullet list (3-5 items).
- [ ] Each section opens with 1-2 paragraphs of motivation, or a single connecting sentence for a purely computational section.
- [ ] Chapter closes with `\section*{Summary}` containing the three required blocks (definitions, theorems, formulas).
- [ ] Section titles use Title Case; subsection titles use sentence case.
- [ ] No `\subsubsection`.

**Environments**
- [ ] Every `definition` introduces a term the chapter actually uses.
- [ ] Every named theorem uses `\begin{theorem}[Name]` and has an `\index{Name}` entry.
- [ ] `example` + `solution` pairs are wrapped in `workedexample`.
- [ ] `remark` is aside material, not main-line knowledge.
- [ ] `caution` is used for notation traps and easy-to-miss restrictions; `strategy` is used for method boxes.
- [ ] No `lemma` (removed from the environment set in v3.0).

**Formula display**
- [ ] Each display situation uses exactly one of the five approved modes.
- [ ] Display block cohesion is maintained within each local math unit.
- [ ] `\qedhere` appears on the last display line of any `solution` that ends in display math.
- [ ] Equation numbers appear only when the equation is referenced later or is a formal statement.

**Typography**
- [ ] No `\textbf{...}` or `\textit{...}` in prose.
- [ ] `\emph{...}` is used for new terms (once each), and only in the contexts allowed in §8.
- [ ] TeX-style quotes `` ``...'' ``; no ASCII straight quotes.
- [ ] Dashes and ellipses follow §8.

**Notation**
- [ ] Symbols and macros follow the canonical list in §9.
- [ ] Any manuscript-specific convention preserved is flagged by a `caution` or `remark` on first use.

**Figures**
- [ ] Figure density is adequate — roughly one figure at each important definition / theorem, and every 2-3 examples in computational sections.
- [ ] Captions are sentence case, end with a period, and describe mathematical purpose.
- [ ] Colour palette stays within blue / red / gray (or an exception is declared).
- [ ] `[H]` placement, or a declared exception.
- [ ] Worked-example figures do not reveal the quantity the example asks the reader to compute.

**Index**
- [ ] Every defined term, named theorem, notation, key example, notation trap, and first-mention applied setting has an `\index{...}` at its first occurrence.

**Cross-references**
- [ ] All in-prose references use `\cref` / `\Cref`; no manual prefixes.
- [ ] Equation references use `\eqref`.
- [ ] Label format is `type:short-desc` with hyphens.

**Source hygiene**
- [ ] No custom macros in the chapter file.
- [ ] No manual page breaks.
- [ ] Exception comment at chapter top if any rule in this document is deviated from.

**Exercises**
- [ ] Every section end has either a real `\subsection*{Exercises}` block or a TODO placeholder.

**CI**
- [ ] `python tools/book_style_lint.py` passes.
- [ ] `python tools/book_preamble_smoketest.py` passes.
- [ ] `latexmk -pdf` builds without errors.

---

## 16. Changelog

- **v3.1** — framework split and implementation landed. The v3.0 document was split into four author-facing files keyed to how authors actually use them: this file (authoritative spec), [`CONTENT_QUICKSTART.md`](CONTENT_QUICKSTART.md) (1-2 page daily reference), [`CONTENT_ROADMAP.md`](CONTENT_ROADMAP.md) (course arc, chapter order, prerequisites, per-chapter core skills), and [`CONTENT_EXERCISES.md`](CONTENT_EXERCISES.md) (minimum exercise skeleton ahead of the full deferred design round). The preamble and template implementation flagged as pending under v3.0 has now landed: per-env chapter-scoped counters via individual `\newtheorem`, `caution` and `strategy` environments via `\newmdtheoremenv`, the three-role semantic palette in `preamble/colors.tex`, expanded `tools/book_style_lint.py` rules, and the updated `_chapter_template.tex`. Content-level refinements added in this pass: remark policy expanded with a usefulness test and explicit good-vs-bad examples; figures gain a "Redundant encoding for grayscale and accessibility" subsection in §10 requiring line-style / label / marker alongside colour; index policy gains an overarching "lookup test" judgement criterion in §11. The `example` + `solution` pairing rule in §5 is now aligned between this document and `chapters/_chapter_template.tex` (every `example` MUST be wrapped in `workedexample`; standalone `example` is no longer allowed). Exercise numbering is now per-section (Exercise 1, 2, ..., resetting at each `\section`) rather than chapter-scoped, reflecting that end-of-section exercise blocks are consumed locally.

- **v3.0** — from-scratch rewrite. Target register shifted from Spivak / Apostol (shared formal-statement counter, austere pronouns, strict definition purity, sparing figures and remarks) to Stewart / Rogawski (per-type counters, "you" permitted in specific contexts, *"Informally, ..."* gloss allowed inside `definition`, denser figures and more generous remarks). New environments `caution` and `strategy` added to support notation-trap warnings and problem-solving strategy boxes; `lemma` dropped. Display-helper set reduced from 7 to 5 (removed `\iffstackeddisplay` and `\iffwithconditions`). Display Block Cohesion downgraded from MUST to SHOULD. Index policy expanded to cover key examples, notation traps, and first-mention applied settings. Chapter opening gains a mandatory learning-outcomes bullet list; chapter closing gains a mandatory `\section*{Summary}` block. `\emph{...}` permitted in motivation prose for the first mention of a term. Exercise-system design deferred until main content is complete. CI checks expanded to cover the new rules. Notation policy consolidated into its own section (§9). The voice reference sample is rewritten in Stewart tone.

  (v3.0 was the positioning-level rewrite; the concrete preamble and template implementation it flagged as pending has since landed — see v3.1 above.)

- **v2.x** — earlier versions (v2.0 through v2.0.11) accreted rule additions through per-chapter review; the resulting document was organised by date of addition rather than by topic. Notable decisions from v2.x preserved verbatim in v3.0 include: cleveref-only cross-references, `[H]` default figure placement with Exception Protocol, shared formula-display helpers `aligneddisplay` / `conditiondisplay` / `\pairdisplay`, chapter-scoped counters, paired-definition cross-reference rule, `workedexample` wrapper semantics, `\qedhere` on final display line of `solution`, and the three-layer CI (style lint + preamble smoketest + latexmk).

- **v1.0** — initial version.
