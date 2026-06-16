# HTML writing contract — handout-kit section fragment

The HTML analog of [`../../../authoring/seed_converge/rules.md`](../../../authoring/seed_converge/rules.md). That file tells a
drafter how to expand a seed into a **LaTeX** `\section` body; this file tells a drafter how to
expand the same seed into a **handout-kit** `sec-*.html` fragment. Register and correctness rules
are identical (they are format-independent); only the surface markup changes.

> **Why this exists:** the experiment in [`RESULT-s42-html-poc.md`](RESULT-s42-html-poc.md) showed
> that pointing the generation step at this contract (instead of `rules.md`) is the whole change
> needed to make the pipeline emit HTML that renders directly through the kit — screen + print, no
> `.tex` and no conversion step. Distilled from
> [`new-chapter/sec-markup-reference.html`](new-chapter/sec-markup-reference.html) and
> [`讀我-排版指南.md`](讀我-排版指南.md); validated by authoring §4.2 (244 KaTeX nodes, 0 errors).

---

## Output shape

Emit **one fragment per section**: a single `<article class="sec" lang="en">` whose only direct
structural child after the header is content. **Do not** emit `<!doctype>`, `<html>`, `<head>`, CDN
links, or `<style>` — the chapter template and `shared/` supply all rendering. The fragment is
loaded verbatim by `template-screen.html` / `template-print.html`.

```html
<article class="sec" lang="en">
  <header class="sec-head">
    <h2 class="sec-title"><span class="sec-no">N.M</span>Section Title</h2>
  </header>
  <p>Prose. Inline math \(a^2+b^2=c^2\); display \[ \int_0^1 x^2\,dx=\tfrac13. \]</p>
  <!-- environments follow -->
</article>
```

A chapter opener instead uses `<header class="chapter-head">` with `.ch-kicker` + `.ch-title`, a
`.lead` paragraph, and a learning-objectives list (see `new-chapter/sec-intro.html`).

## Register (identical to `rules.md`)

- Stewart / Rogawski self-study tone: accessible to a motivated high-schooler, full sentences with
  explicit connectives, intuition before formalism, warm but not chatty. Default pronoun **we**.
- Every formal statement (definition / theorem / proposition / corollary) is **preceded** by 1–2
  paragraphs of intuition explaining why it is worth introducing. A definition body MAY end with one
  *“Informally, …”* gloss, marked `<p class="informal">…</p>`.

## Semantic environments — use these, do not invent; never write inline `style=`

Color = teaching role, applied automatically by `shared/skin-hs.css`. The full vocabulary:

| class on `<section class="env …">` | role | notes |
|---|---|---|
| `env-definition` | concept (teal) | defined term in `<em>`; optional `<p class="informal">` gloss |
| `env-theorem` / `env-proposition` / `env-corollary` | result (blue) | body **auto-italic** (theorem/proposition; see caveat in RESULT for corollary), math stays upright |
| `env-example` + `env-solution` | practice (green) | always paired inside `<div class="workedexample">` — no solo example |
| `env-exercise` | — (do not emit) | the handout ships **no exercises** (separate workbook; user decision 2026-06-12, `CONTENT_SPEC.md` §14). The kit CSS still styles this class, but fragments must not use it. |
| `env-remark` | aside (gray) | lighter, smaller |
| `env-proof` | subordinate | end body with `<span class="qed qed-proof"></span>` |
| `env-caution` | ⚠ red **solid box** | one trap, 1–3 sentences |
| `env-strategy` | violet **solid box** | numbered method; steps in `<ol class="steps">` |

Every environment has the same internal skeleton:

```html
<section class="env env-theorem">
  <p class="env-head"><span class="env-kicker">Theorem</span><span class="env-num">N.M</span><span class="env-name">Optional name</span></p>
  <div class="env-body"> … <span class="qed"></span></div>
</section>
```

- `env-kicker` = the word (Theorem, Definition, …). `env-num` = the **manual** number. `env-name` =
  optional italic descriptive name.
- **Qualified proofs** (e.g. *Proof of Theorem N.M (⇒ direction)*, *Proof (sketch)*): keep
  `env-kicker` = `Proof` and put the qualifier in `env-name`. (Validated in §4.2.)
- Worked example end mark: `<span class="qed"></span>` on the solution; proof end mark adds
  `qed-proof`.

## Math (KaTeX)

- Inline `\( … \)`; display `\[ … \]`. **One display mode per local unit** — don't mix an inline
  result and a multi-line derivation in the same step.
- Multi-line aligned derivations: `\[ \begin{aligned} a &= b \\ &= c. \end{aligned} \]`
- **Verified to render in the kit's KaTeX** (real-analysis grade): `\tag{*}` / `\tag{**}` (right-
  aligned equation tags), `\binom`, `\underbrace{…}_{\text{(I)}}`, `\lvert … \rvert`,
  `\bigl…\bigr`, `\mathbb{R}`, `\varepsilon`, `\tfrac`, `\operatorname`. Section-specific operators
  go in the chapter template's `macros: {}` block (e.g. `\arccsc`).
- KaTeX runs with `throwOnError:false`; a malformed expression renders as red source text — that is
  the signal to fix it.

## Numbering and cross-references — the one big difference from LaTeX

The kit has **no auto-counter and no `\label`/`\cref`**. Therefore:

- **All numbers are hand-written text**: `sec-no`, `env-num`, `fig-no`. Use per-type counters within
  the chapter (Theorem 4.1, 4.2, …; Proposition 4.1, 4.2, …; Definition 4.1, …), continuing across
  sections of the same chapter.
- **Every cross-reference is plain prose** citing that manual number: `by Theorem 4.2`,
  `Proposition 4.1`, `the completeness theorem of §4.1`. There is no `\cref`, `\eqref`, or hyperlink.
- Consequence: the drafter must **assign numbers and keep references consistent by hand**, and a
  downstream lint should verify that every “Theorem N.M”-style reference resolves to an existing
  `env-num`. Renumbering is manual — this is the main authoring tax (see RESULT §gaps).

## Marking expansion (carried over from `rules.md`)

Mark every addition beyond the seed with an **HTML comment** on the line immediately before it:

```html
<!-- expansion:<category> — <one-line description> -->
```

Categories unchanged: `history`, `application`, `formula`, `summary`, `figure`, `example`,
`intuition`, `strategy`, `caution`. (Comments are inert in the page; they are the audit trail.)

## Prose typography

- Emphasis: `<em>` only — no `<b>`/`<strong>` in prose.
- Use real Unicode directly (files are UTF-8): curly quotes “ ”, en/em dashes – —, ×, ≤, … in prose
  (math symbols go through KaTeX, not Unicode).
- Mini heading inside a section: `<p class="para-head">…</p>`. Sub-section heading: `<h3 class="subsec-head">`.
- Lists: plain `<ul>`/`<ol>`; warm-up observations `<ol class="warmup">` (auto (a)(b)(c)); method
  steps `<ol class="steps">`; example prompts `<ol class="prompt-list">`; solution parts
  `<ol class="sol-list">`.

## Figures

Placeholder in the fragment, drawing registered in the standalone HTML's `FIGS` object:

```html
<figure class="figure" data-fig="my-plot">
  <figcaption><span class="fig-no">Figure N.M</span> Sentence-case caption ending with a period.</figcaption>
</figure>
```

The `FIGS` entry returns `{ layout, panels:[{ svg: buildPlot(cfg), note }] }`; labels use real
`\( … \)` TeX so figure symbols match the prose. Inline SVG is also allowed for schematic diagrams
(see `example-ch01/sec-1-1.html` Figure 1.2). A section with no figures simply registers no `FIGS`
entry (the loader degrades gracefully).

**Keep figures label-light.** Put only the minimum on the drawing — axis/dimension labels, curve
labels, and at most one short anchor — and name the regions, areas, formulas, and any extended
explanation in the caption and the body prose instead. A figure whose interior reads like a
paragraph is over-labelled; move the detail into the surrounding text. (Authoritative rule:
[`../../../CONTENT_SPEC.md`](../../../CONTENT_SPEC.md) §10 "Label economy"; established by §2.5 Figure 2.4,
whose rectangle keeps only its side lengths and an `fg` anchor.)

## Correctness (hard constraint, identical to `rules.md`)

Every mathematical claim MUST be correct and standard. Do NOT invent theorems, identities, named
results, or historical attributions. If unsure a claim is true, omit it rather than guess. Named
results, subtle proofs, and historical notes are human-checked.

## Not available in the kit (do not emit; handle as noted)

| LaTeX feature | in the kit | do instead |
|---|---|---|
| `\label` / `\cref` / `\Cref` | none | manual prose reference to the hand-written number |
| `\eqref` / equation labels | none | `\tag{*}` renders the tag; reference it as plain “(\*)” in prose |
| `\index{…}` | none | drop (no per-section index); flag if a book-level index is wanted |
| automatic theorem/figure/section numbering | none | manual `env-num` / `fig-no` / `sec-no` |
| `\cite` / bibliography | none | name the source inline, per the `history` policy |
