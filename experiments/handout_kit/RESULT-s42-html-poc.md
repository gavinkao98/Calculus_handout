# RESULT — §4.2 as a handout-kit HTML section (free POC)

> **One line:** authored §4.2 (e^x continuity + exponent law) **directly into the kit's semantic
> HTML** from its seed — no `.tex`, no conversion — and rendered it screen + print. The markup is an
> adequate generation target for hard, proof-dense content; the one structural cost is the loss of
> LaTeX's auto-numbering / cross-referencing.

## What this tested

The user's question was: our previous pipeline produced `.tex` (drafter expands a seed per
[`../seed_converge/rules.md`](../seed_converge/rules.md), auditor reviews) — **can the model instead
generate HTML directly per the new typesetting template?** This POC answers it the cheapest way:
Claude Code (the *writer* role of the project's subscription review loop) authored one real section
directly in the kit markup — no paid API, no `.tex`.

- **Input:** [`../direction_layer/test/seed_s42.md`](../direction_layer/test/seed_s42.md) — the
  manuscript spine (the only existing seed inside the ch02–ch04 range the user named). §4.2 is the
  designated *high-risk* section (Cauchy⟺convergent, Bolzano–Weierstrass, the exponent-law proof),
  so it stresses the markup hardest.
- **Authoring target:** [`CONTRACT-html-writing.md`](CONTRACT-html-writing.md) (the HTML analog of
  `rules.md`, written alongside this POC).
- **Correctness anchor:** math cross-checked against the human-signed
  `signed_s42_body.tex` (local working file, never committed; the committed trail of that audit is
  [`../direction_layer/test/draft_s42.tex`](../direction_layer/test/draft_s42.tex) plus its
  `audit_findings_s42*.txt`) so no proof step was invented. Generated **from the seed**, not
  transliterated from the `.tex`.
- **Output:** [`exp-ch04/sec-4-2.html`](exp-ch04/sec-4-2.html), rendered via `poc-screen.html` and
  `poc-print.html` (template-era render shells, since removed in the standalone consolidation — see
  [`README.md`](README.md)).

## How it was rendered (zero-install recipe)

The kit needs an HTTP server (screen template `fetch()`es fragments) and a browser (CDN KaTeX/fonts
+ the print paginator). Both are already on this machine — no downloads.

```powershell
# 1) serve the kit
python -m http.server 8753 --bind 127.0.0.1     # run from experiments/handout_kit/
# 2) screen overview (Chrome headless, top-of-page)
& "C:\Program Files\Google\Chrome\Application\chrome.exe" --headless=new --hide-scrollbars `
  --window-size=1000,6200 --virtual-time-budget=30000 --screenshot="_render\poc-screen-full.png" `
  "http://127.0.0.1:8753/poc-screen.html"
# 3) per-A4-page print capture at 2x (CDP; waits for the paginator to finish)
node _render\shot.mjs "http://127.0.0.1:8753/poc-print.html" "_render\poc-print" sheets `
  '(()=>{const b=document.getElementById("printBtn");return !!b && b.disabled===false;})()'
```

[`_render/shot.mjs`](_render/shot.mjs) is a small dependency-free CDP screenshotter (Node ≥21 global
`WebSocket`); it waits for render-complete, then captures each `.sheet` (A4 page) or the full page at
2×. Reusable for any future kit render.

## Result

- **244 KaTeX expressions, 0 errors.** Every construct rendered, including the ones `example-ch01`
  never exercised: `\tag{*}`/`\tag{**}` (right-aligned eq tags), `\binom`, `\underbrace{…}_{(I)}`,
  and many multi-line `\begin{aligned}` derivations.
- **8 clean A4 pages.** The content-aware paginator split the long exponent-law proof across pages
  5→6→7 via `env-cont` continuations, carried headings, and kept running heads + page numbers + the
  binding margin. No orphaned headings or broken environments.
- **Both outputs from one source fragment** — the “same content → screen + print” promise holds for
  proof-dense material, not just the easy §1.1-style content.

Screenshots: `_render/poc-print-p01.png … p08.png`, `_render/poc-screen-full.png`.

## What worked (markup adequacy)

1. **The environment vocabulary was sufficient — nothing had to be invented.** §4.2 needed
   definition, theorem, proposition, corollary, remark, caution, proof, and worked example; all
   exist with the right semantics.
2. **Auto-italic theorem/proposition bodies with upright math** match the LaTeX `amsthm` look.
3. **Qualified proof headers** (“Proof *of Theorem 4.2 (⇒ direction)*”, “Proof *sketch*”) expressed
   cleanly via `env-name`.
4. **Expansion audit trail** carried over as `<!-- expansion:cat — … -->` comments (inert, lintable).

## Findings (four-level triage — see CLAUDE.md; deliberately not over-reported)

**① Real issue — worth the designer's call**

- **No cross-reference / auto-numbering system.** The source used `\cref`/`\label` ~20×; in the kit
  every number is hand-typed and every reference is plain prose (“Theorem 4.2”). For a
  cross-reference-dense section this is the main authoring tax **and the main correctness risk** —
  renumbering means manually re-finding every reference. *Direct evidence:* I introduced a
  proposition-numbering slip (counter started at 4.2) and caught it only on review. → If this kit is
  adopted, the generation contract must require the drafter to assign+track numbers, and a
  deterministic lint should verify every “Theorem N.M” reference resolves to an existing `env-num`.
  (This is a property of the kit, not a defect to fix in it.)
- **Corollary bodies are not auto-italicized, but theorem/proposition bodies are.**
  `skin-hs.css` groups `env-corollary` with theorem/proposition for *color* but omits it from the
  `font-style: italic` rule. So a Corollary renders upright while neighbouring results render
  italic — a within-family inconsistency vs. the usual textbook convention. Likely a one-line
  oversight; flagged for the designer rather than patched here (it's their spec under test).

**② Discoverability gap (not a conflict — just undocumented)**

- The kit has a richer vocabulary than `sec-markup-reference.html` shows: `env-cont` (environment
  continued onto the next page) is created by the paginator and styled, but isn't in the reference.
  Worth documenting if authors ever hand-split.
- `\tag` works but isn't mentioned in the guide; the contract now records the verified KaTeX feature
  set.

**③ Editorial-drift risk (low priority)**

- `<!-- expansion: -->` has no HTML-side linter yet (the LaTeX side keys off `% expansion:`). Easy to
  add later; noted in the contract so the convention is at least uniform.

**④ Not findings (recorded so they aren't re-raised)**

- No `\index` in the kit — fine for a per-section handout; only matters if a book-level index is
  wanted (scope, not defect).
- Print toolbar overlaps the top-right of page 1 *in a full-bleed screenshot* — a capture artifact
  (the toolbar is `position:fixed`); it does not affect actual Print/PDF. Harness-only.
- Title wrapping to two lines on page 1 — expected for a long section title.

## Implications for “generate HTML directly” (the forward path)

1. **The swap is real and small.** Point the drafter at
   [`CONTRACT-html-writing.md`](CONTRACT-html-writing.md) instead of `rules.md`; it emits a
   `sec-*.html` fragment; `shared/` renders it. Nothing else in the flow changes.
2. **Add a numbering/reference lint** to the ⑤ review stage — the one thing LaTeX gave for free that
   the kit doesn't. Cheap, deterministic, advisory.
3. **Close the loop on subscriptions — no paid API.** The project already pivoted off the original
   API↔API `run.py` to the subscription CLI↔CLI loop (see
   [`../seed_converge/PLAN_codex_subscription_loop.md`](../seed_converge/PLAN_codex_subscription_loop.md),
   smoke-tested §9, and used for the §1.1/§1.2/§4.2 audits): **Claude Code = single writer**, **`codex
   exec` = read-only auditor** on the ChatGPT subscription. This POC's authoring step *is* that writer
   role, now emitting HTML. To audit HTML, point the existing auditor prompt at the `.html` draft +
   this contract + the numbering/reference check. Cost is ChatGPT-subscription **quota, not money**.

## Status & next steps

- **Status:** POC complete and verified on one high-risk section. Markup is an adequate generation
  target; cross-referencing is the only structural gap.
- **Next (await user direction):** (a) port the numbering/reference lint; (b) try a second section
  with **figures** (§4.2 is figure-light — the figure path is only smoke-tested via the demo plot);
  (c) source seeds for ch02/ch03 (none exist yet) to extend beyond §4.2; (d) close the subscription
  ⑤ loop on this HTML draft — run the `codex exec` read-only auditor over `sec-4-2.html` (the writer
  half is already done here). No paid API; uses ChatGPT-subscription quota.
