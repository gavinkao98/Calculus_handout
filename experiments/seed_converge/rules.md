# House rules (distilled) — calculus handout section

A distilled subset of CONTENT_SPEC.md / CONTENT_QUICKSTART.md, given to both
models. Not the full spec (keeps prompts and cost down).

## Register
- Stewart / Rogawski self-study tone: accessible to a motivated high-schooler,
  full sentences with explicit connectives, intuition before formalism, warm but
  not chatty. Default pronoun **we**.
- Every formal statement (definition / theorem / proposition / corollary) is
  **preceded** by 1–2 paragraphs of intuition explaining why it is worth
  introducing. A `definition` body MAY end with one *"Informally, ..."* gloss.

## LaTeX environments (use these; do not invent new ones)
- `definition`, `theorem[Name]`, `proposition`, `corollary`.
- `example` + `solution`, always wrapped in `workedexample` (no solo `example`).
- `remark` (aside / notation note), `caution` (one notation trap, 1–3 sentences),
  `strategy` (numbered method box).
- figures in TikZ, placement `[H]`, caption sentence-case ending with a period.
- `\index{...}` at first occurrence of each defined term, named theorem, notation.

## Formula display (one mode per local unit)
- inline `\(...\)`; display `\[...\]`; aligned derivation steps; a condition
  display with a trailing domain/branch condition; two compared formulas side by
  side. Do not mix modes inside one step.

## Prose typography
- emphasis: `\emph{...}` only — **no** `\textbf{...}` / `\textit{...}` in prose.
- TeX quotes ``` ``...'' ``` — no ASCII `"..."`.
- `\dots` (not literal `...`); `---` for aside dashes; `--` for numeric ranges.
- cross-references: `\cref{...}` / `\Cref{...}` — never manual `Theorem~\ref{...}`.

## The seed is a seed
- You MAY reorganize, rewrite, and add motivating prose, extra worked examples,
  figures, and strategy / caution boxes. Richness is wanted; thin translation is
  not the target.
- Mark every addition that goes beyond the seed with a comment on the line
  immediately before it:
  `% expansion:<category> — <one-line description>`
  Categories: `history`, `application`, `formula`, `summary`, `figure`,
  `example`, `intuition`, `strategy`, `caution`.

## Correctness (hard constraint)
- Every mathematical claim MUST be correct and standard. Do NOT invent theorems,
  identities, named results, or historical attributions. If you are unsure a
  claim is true, omit it rather than guess.
