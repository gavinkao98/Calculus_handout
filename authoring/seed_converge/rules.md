# House rules (distilled) — calculus handout section

> **Frozen artifact (LaTeX-era).** This is the distilled writing contract that was
> fed to the seed_converge experiment, which ran against the LaTeX format. The live
> handout switched to HTML on 2026-06-13 and now has its own writing contract at
> [`handout/CONTRACT-html-writing.md`](../../handout/html/CONTRACT-html-writing.md)
> (typesetting in [`handout/TYPESETTING_GUIDE.md`](../../handout/html/TYPESETTING_GUIDE.md)).
> The LaTeX-mechanics rules below (environments, `\index`, TikZ/`[H]`, math delimiters,
> `\emph`/`\textbf`, TeX quotes, `\cref`, `% expansion:` comment syntax) describe the
> frozen experiment; for the current handout follow the HTML contract instead. The
> format-independent substance (register, expansion-marker categories, correctness)
> still holds.

A distilled subset of CONTENT_SPEC.md / CONTENT_QUICKSTART.md, given to both
models. Not the full spec (keeps prompts and cost down).

## Register
- Stewart / Rogawski self-study tone: accessible to a motivated high-schooler,
  full sentences with explicit connectives, intuition before formalism, warm but
  not chatty. Default pronoun **we**.
- Every formal statement (definition / theorem / proposition / corollary) is
  **preceded** by 1–2 paragraphs of intuition explaining why it is worth
  introducing. A `definition` body MAY end with one *"Informally, ..."* gloss.

## Environments / semantic blocks (use these; do not invent new ones)
*(LaTeX-era environment names; for the HTML handout these are the structural blocks in
[`CONTRACT-html-writing.md`](../../handout/html/CONTRACT-html-writing.md).)*
- `definition`, `theorem[Name]`, `proposition`, `corollary`.
- `example` + `solution`, always wrapped in `workedexample` (no solo `example`).
- `remark` (aside / notation note), `caution` (one notation trap, 1–3 sentences),
  `strategy` (numbered method box).
- figures (LaTeX-era: TikZ, placement `[H]`); caption sentence-case ending with a
  period (the caption convention is format-independent and still holds).
- mark the first occurrence of each defined term, named theorem, notation
  (LaTeX-era: `\index{...}`).

## Formula display (one mode per local unit)
*(LaTeX-era delimiters below; in the HTML handout math goes through MathJax/KaTeX — see
[`TYPESETTING_GUIDE.md`](../../handout/html/TYPESETTING_GUIDE.md). The one-mode-per-unit intent
is format-independent.)*
- inline `\(...\)`; display `\[...\]`; aligned derivation steps; a condition
  display with a trailing domain/branch condition; two compared formulas side by
  side. Do not mix modes inside one step.

## Prose typography
*(LaTeX-era markup below; in the HTML handout emphasis/quotes/dashes are HTML or Unicode
and cross-references are plain-prose references to the hand-written number (no `\cref`, no hyperlink) — see
[`CONTRACT-html-writing.md`](../../handout/html/CONTRACT-html-writing.md).
Each rule's intent is format-independent.)*
- emphasis: `\emph{...}` only — **no** `\textbf{...}` / `\textit{...}` in prose
  (HTML: `<em>` only, no `<b>`/`<strong>`).
- TeX quotes ``` ``...'' ``` — no ASCII `"..."` (HTML: Unicode curly quotes).
- `\dots` (not literal `...`); `---` for aside dashes; `--` for numeric ranges
  (HTML: Unicode `…` / `—` / `–`).
- cross-references: `\cref{...}` / `\Cref{...}` — never manual `Theorem~\ref{...}`
  (HTML: point to hand-written numbers, e.g. "by Theorem 4.2", "as in §1.3"; no `\cref`).

## The seed is a seed
- You MAY reorganize, rewrite, and add motivating prose, extra worked examples,
  figures, and strategy / caution boxes. Richness is wanted; thin translation is
  not the target.
- Mark every addition that goes beyond the seed with a comment on the line
  immediately before it. In the HTML handout the marker is an HTML comment:
  `<!-- expansion:<category> — <one-line description> -->`
  (LaTeX-era form was `% expansion:<category> — <one-line description>`).
  Categories: `history`, `application`, `formula`, `summary`, `figure`,
  `example`, `intuition`, `strategy`, `caution`.

## Correctness (hard constraint)
- Every mathematical claim MUST be correct and standard. Do NOT invent theorems,
  identities, named results, or historical attributions. If you are unsure a
  claim is true, omit it rather than guess.
