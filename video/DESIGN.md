# Video Pipeline — Design (2nd generation)

This is the redesigned handout → lesson-video pipeline. Input is the HTML handout
kit (`../experiments/handout_kit/`; per-chapter authoritative file listed in
[README.md](README.md) — switched from `chapters/*.tex` on 2026-06-10). It supersedes the
first-generation system (`tools/manim_*`, `MANIM_STORYBOARD.md`,
`MANIM_REFERENCE.md`, `MANIM_CHECKLIST.md`), which is frozen, not deleted.

Status: **partially implemented**. The storyboard → TTS → audio-driven render → mux
path now works end-to-end (validated on §1.1); the remaining sections marked (TODO)
are not implemented yet.

---

## Why a redesign

The first generation worked but accreted three sources of friction:

1. **Two reveal mechanisms coexisting.** A timing-based path (`_run_voiceover_beats`,
   hand-estimated seconds) and a bookmark path (`reveal_strategy` + manim-voiceover)
   ran side by side, gated at render time. Authors had to know both.
2. **A heavy spoken-math rewrite layer.** Every `f(x_1)` had to be hand-rewritten to
   "f of x one" in a separate `voiceover` field, governed by a large rules table,
   because the old TTS could not read LaTeX.
3. **Three overlapping narration fields.** `voiceover` + `voiceover_beats` +
   `bookmark`/`reveal_groups` all encoded "what is said" and "when things appear",
   kept in sync by hand.

Two decisions collapse all three:

- **Gemini TTS reads LaTeX directly** using the model's preset voice names
  (`meta.voice` / `--voice`). No voice cloning or reference audio is used. The
  spoken-math rewrite layer is deleted. Narration is written once, with LaTeX inline.
- **One narration field with inline reveal markers.** `say` carries both the words and
  the timing cues. No separate beats/bookmark/reveal arrays.

Plus a new product requirement: **every section gets an intro and an outro animation**,
so scene `kind` is first-class and silent (no-narration) scenes are supported.

---

## Carried over vs rewritten

| Ported verbatim (validated, no gain in rewriting) | Rewritten from scratch |
|---|---|
| `visuals/theme.py` (Midnight Canvas palette + typography + layout metrics) | storyboard schema + format |
| `visuals/graph_utils.py` (safe expr eval + sampling) | narration → beats compiler |
| `visuals/layout.py` (16:9 zone layout) | scene templates |
| ffmpeg mux/concat logic *(done fresh as `pipeline/mux.py`)* | TTS backend (Gemini) |
| Midnight Canvas visual philosophy + animation language | CLI / orchestration |

Ported assets were copied key-for-key from the real source dicts
(`DEFAULT_THEME` in `legacy/scripts/manim_render_lesson.py`, `SceneLayout` in
`legacy/scripts/manim_templates/layout.py`, `safe_eval_expression` in
`legacy/scripts/manim_templates/graph_utils.py`), not reconstructed from the docs.

The methodology *spirit* of `MANIM_STORYBOARD.md` (one teaching idea per scene,
detail over compression, conversational narration, visual over textual, symbol-heavy
exception) carries forward. Its mechanical rules (spoken-math table, sentence-count
carve-outs, bookmark syntax) do not — they were artifacts of the old constraints.

---

## Storyboard format

One YAML file per section. Top-level: `meta` + `scenes`.

```yaml
meta:
  id: ch01_inverse_functions      # deck id, also output dir name
  section: "1.1"                  # shown by intro/outro templates
  title: "Inverse Functions"
  language: en
  theme: midnight
  voice: Kore                     # Gemini preset voice name
  video: { w: 3840, h: 2160, fps: 60 }   # delivery standard: 4K60 (manim fourk_quality)

scenes:
  - id: <unique snake_case>
    kind: intro | content | outro
    ...
```

**Resolution convention.** Testing and preview renders use **1080p**
(`make.py --quality high`, the default) — crisp enough for visual QA and VLM frame
critique without 4K's render cost. **Only the final delivery uses 4K**
(`--quality 4k`): the project standard `3840×2160@60` (manim `fourk_quality`),
declared per section in `meta.video` and defaulted when omitted. `--quality low` /
`medium` (480p/720p) are fast scratch previews. The layout is resolution-independent
(the manim frame is a fixed 14.222×8 units), so a 1080p test and the 4K master are
pixel-for-pixel the same composition — only sampling density and render time differ.

### Scene kinds

- **`content`** — a teaching scene. Has `template`, `say`, and visual data. This is
  the workhorse; everything below about `say`/reveal applies to it.
- **`intro`** — section opener. **No `say`** (pure animation). Consumes
  `meta.chapter`, `meta.chapter_title`, `meta.sections`, `meta.section`,
  `meta.title`, an optional `tagline`, optional `bgm`, `duration`. The reusable
  template is a Section Gate: first show the chapter map, focus the current
  section, resolve into the logo / section / title / tagline slate, then add a
  short dark handoff so the first teaching scene does not feel like an abrupt
  color cut.
- **`outro`** — section closer. **No `say`**. Consumes optional `bgm`, `duration`,
  and an optional `end_slate` override. The template is two-stage: a short
  dark-to-light bridge from the teaching ground, then a final centered logo slate
  so the viewer clearly feels the video has ended. **Key Takeaways are NOT in the
  outro** — they live in the preceding `recap_cards` content scene, which carries
  narration (a silent takeaways slate read weaker than a narrated recap). The end
  slate defaults to `meta.section` + `meta.title`; use optional `end_slate.label`,
  `end_slate.title`, or `end_slate.logo_height` only when a section overrides the
  standard ending. (Any `recap`/`next` keys on an outro are vestigial — the
  template ignores them.)

`intro`/`outro` are defined **once** as parameterized templates and reused for every
section — authors never hand-build them per section.

Minimal reusable outro:

```yaml
- id: outro
  kind: outro
  duration: 8.0
  # optional: bgm, and an end_slate override (label / title / logo_height)
  # Key Takeaways are a separate recap_cards scene, not the outro.
```

Minimal reusable intro:

```yaml
meta:
  chapter: "Chapter 1"
  chapter_title: "Inverse Functions and Limits"
  section: "1.1"
  title: "Inverse Functions"
  sections:
    - { id: "1.1", title: "Inverse Functions" }
    - { id: "1.2", title: "Inverse Trigonometric Functions" }

scenes:
  - id: intro
    kind: intro
    tagline: "When can a function be run backwards?"
    duration: 6.0
```

### `content` scene fields

| Field | Required | Meaning |
|---|---|---|
| `template` | yes | which scene template (see catalog, TODO) |
| `accent` | for definition-family | colour role: `definition` / `theorem` / `proposition` / `example` / `warning` / `procedure` / `recap`. Replaces old `content_type`. |
| `title` | yes | on-screen scene title; `$...$` allowed for math |
| `say` | yes | the single narration field (see below) |
| `statement`, `math`, `steps`, `plots`, … | per template | the on-screen visual payload |
| `hook` | no | dotted path to a custom animation fn (escape hatch, unchanged concept) |

### Template selection: discrete steps vs a derivation chain

Computation scenes come in two shapes, and picking the wrong template is how a
long formula runs out of room — the two-column templates' math column tops out
around ~5 manim units, while a real chain line (the ch02 slope-from-definition
computation) needs 7–9:

- **`example_walkthrough` / `procedure_steps`** — DISCRETE steps: each step is
  a short formula whose reasoning text is worth *reading* beside it. Capacity:
  3–4 rows, math column ~5 units.
- **`derivation`** — a CONTINUOUS transformation chain (derivative from the
  definition, limit-law rewrites, identity proofs): one aligned full-width
  chain (~11 units), revealed line by line via `{show line.N}`; the per-step
  "why" lives in the narration, not on screen. Line 0 carries the LHS; later
  lines written in the "= ..." continuation style x-align their relation
  symbol under line 0's (`align_on`, default `=`). `anim: highlight` marks the
  result line (accent colour). An optional centred `statement` states the
  problem — but a full-capacity chain should hand that job to the narration's
  first beat instead (measured: statement + four fraction-height lines +
  result line overflows the zone by ~0.5).
- **Capacity before SPLITTING the scene** (a content-layer decision, same
  spirit as methodology §3's proof split): ~5 fraction-height lines without a
  statement, ~4 with one; ~7 single-height lines. `sizecheck` flags the
  overflow; the fix is a split, not a squeeze. Demo / reference storyboard:
  `storyboards/_demo_derivation.yml` (the real ch02 chain + a 6-line probe).

### `say`: narration + inline reveal (the core change)

`say` is **what is spoken**, with **LaTeX written inline** (`$f(x_1)$`), and **reveal
markers** `{show <target>}` interleaved.

```yaml
say: |
  The property we need is called one-to-one. A function is one-to-one
  when different inputs always give different outputs.
  {show math.0} No two distinct inputs ever land on the same output.
  {show math.1} Equivalently, if $f(x_1) = f(x_2)$ then $x_1 = x_2$.
```

Rules:

- **`{show <target>}`** marks "reveal this element now". Targets name an element in the
  scene's visual payload: `math.0`, `math.1`, `step.0`, `bullet.0`, `plot.0`,
  `statement`, `takeaway`, … (the index is into the corresponding list).
- A **beat** is the run of text from one marker (or scene start) up to the next marker.
- Static elements (title, axes, statement) appear at scene start by default; only
  elements named by a `{show ...}` wait for their beat. (This is the old static/dynamic
  split, now expressed inline instead of in a per-template table.)
- LaTeX in `say` is passed to Gemini TTS as-is. **No spoken-math rewrite.** If a specific
  phrase reads better a particular way, just write it that way in `say`.

### `math` and other visual payload

```yaml
math:
  - "$f(x_1) \\ne f(x_2)$ whenever $x_1 \\ne x_2$"     # plain string
  - { tex: "$f(x_1)=f(x_2)\\implies x_1=x_2$", anim: highlight }   # with animation
```

`anim` options (carried over): `write` (default), `highlight`, `transform_from_previous`.
The *when* (reveal timing) lives in `say` via `{show math.N}`; the *how* (animation
style) lives here. Clean separation.

### Text rendering: prose vs math (no garble)

On-screen text takes one of two render paths. Both are Computer Modern, but manim
sizes them differently for the same `font_size`, and only one understands LaTeX:

| Path | Engine | Understands `$math$` / `\\`? | Used by |
|---|---|---|---|
| `Text` | Pango (OTF font) | **No** — markup prints literally (the garble) | `brand.body_text`, `brand.heading` |
| `Tex` / `MathTex` | LaTeX | Yes | `brand.prose`, `brand.heading_rich`, `brand.math_line` |

A `Text` is ~1.34× taller than a `Tex` at equal `font_size`, so prose rendered via
Tex is scaled up by `theme.TEX_TEXT_SCALE` to sit at the same size as `body_text`
beside it. Math (`math_line`) keeps its own size role and is left unscaled.

**The rule (templates must follow it):** any field an author might put `$` or `\`
into — `title`, `statement`, step `text`, `takeaway`, recap `points` — is rendered
through **`brand.prose`** (body prose) or **`brand.heading_rich`** (titles). These
are the single decision point for Text-vs-Tex: markup → Tex, otherwise → wrapped
Text. Never call `body_text` / `heading` directly on an author prose field. Pure
math fields (`math`, `formulas`, `proof`, `worked`) go through `brand.math_line`.

Plain-Text-only fields are the intro/outro brand labels (`meta.chapter`,
`meta.chapter_title`, `meta.section`, `meta.title`, `meta.tagline`,
`meta.sections[].title`) — keep markup out of these. `pipeline/lint.py` enforces
all of the above statically (see Data flow) and runs before every render.

**Sizing rule — wrap, don't shrink (for stacked prose).** When a prose line is
too wide, `brand.prose` *wraps* it to more lines at full size; it never
`scale_to_fit_width`s a single line down. This matters for **stacked siblings**
(recap points, proof steps, graph annotations, example steps): if one long line
were shrunk while its short neighbours were not, they would render at visibly
different sizes (this was a real bug). So any group of prose lines that sit
together must go through `brand.prose` with a `max_width` — not `math_line` +
`scale_to_fit_width`. `$...$` spans are atomic to the wrapper, so a wrap never
splits math. The only place `scale_to_fit_width` is acceptable is a **standalone
display line with no siblings to match** — a `heading`/`heading_rich` title — and
even there, prefer wrapping when it reads well. Math grids (`math`, `formulas`,
`worked`) are their own size role and are exempt.

Enforced automatically: `pipeline/sizecheck.py` builds each scene (no render),
finds the `brand.prose`-tagged lines in every stacked-sibling group (`point`,
`proof`, `step`, `annotation`, `row`) and flags a group whose lines render at
different (scale-aware) font sizes. `make.py` runs it before rendering the
selected scenes (`--skip-sizecheck` to bypass), alongside the garble `lint.py`.

**Colour / readability.** Text that carries teaching content uses `text`/`primary`
or a semantic accent — never `muted`. This covers prose (statements, step text,
graph annotations, recap points) **and direct `MathTex`/`Text` value labels** —
e.g. the numbers on a mapping diagram (`½`, `−½`, `¼`) or point coordinates are
content, so `text`, not `muted` (both were real misses, faint at video distance).
`muted` (`#7e8497`) is for *decoration and de-emphasis only*: the summit-bars
motif, non-current section-map entries, retired content, and pure reference labels
(a `y=x` guide line, set `A`/`B` tags).

> Guard blind spot: `sizecheck` flags `muted` only on `brand.prose` text. A
> **directly-constructed `MathTex`/`Text` label in `muted` is NOT caught** —
> because some such labels (the reference/decoration ones above) are legitimately
> muted, so a blanket rule would false-positive. For direct labels this is
> convention + review, not an automated guard.

**No manual line breaks in prose.** Author a step/point/annotation/statement as a
plain sentence — do **not** insert a LaTeX `\\` to force a line break. `brand.prose`
wraps automatically at the column `max_width`: a short line stays on one line, a
long line wraps at a word boundary. A manual `\\` forces an arbitrary break (e.g.
"Solve $y=x^3$\\ for $x$." snapped a one-line phrase into two) — that is an
authoring artifact, not layout. Reserve `\\` for a *deliberate* stylistic break,
which is rare here.

---

### Authoring checklist — recurring mistakes, do not repeat

Each of these shipped as a real bug this project already paid for. When writing a
storyboard or a template, hold to them. Severity: **error** aborts the render
(definitely broken); **warn** prints but does not block (has rare legitimate
exceptions). Both run in `make.py` before render.

| Don't | Do | Why / guard |
|---|---|---|
| `$math$` or `\` in a plain-Text field (`title`, `meta.*` labels) | put math only in markup-capable fields | prints literally; **lint error** |
| odd number of `$` | balance every `$…$` | LaTeX crash; **lint error** |
| `body_text`/`heading` on a field that may hold `$`/`\` | `brand.prose` / `brand.heading_rich` | garble; routing is centralised there |
| `math_line` + `scale_to_fit_width` on stacked prose | `brand.prose(..., max_width=…)` (wraps) | size mismatch; **sizecheck error** |
| manual `\\` break in prose | plain sentence, let prose wrap | arbitrary break; **lint warn** |
| `muted` for teaching content (prose **or** direct `MathTex`/`Text` value labels) | `text`/`primary` or a semantic accent | too faint; **sizecheck warn** on prose only — direct labels are convention |
| hollow `○` dot for an attained value (point on a curve / intersection) | solid `●` (`hollow: false`); for a deliberately excluded value, add `hollow_reason: <why>` to the point | `○` means *value absent*; **lint warn** (hollow on an interior curve point), suppressed when `hollow_reason` is set |
| an element wider/taller than the frame (formula/recap card, long statement, unclamped headline) | shorten it, clamp the width, or split it | silently clipped off-frame; **sizecheck error** (off-frame) / **warn** (spills past the safe margin) |

---

### Visual QA — the whole-video acceptance pass

The authoring checklist above catches *known per-element mistakes* statically. This
is its complement: a **five-dimension pass over the finished video** (or its key
frames), watched end-to-end before a section ships. The dimensions are adapted from
Code2Video's AES rubric; in that study aesthetic score correlated **r ≈ 0.97** with
measured learning gain, so visual clarity is teaching efficacy, not polish. The same
table doubles as the rubric for a future VLM critic (see
[`CODE2VIDEO_STUDY.md`](CODE2VIDEO_STUDY.md) P1/P3).

| Dimension | Concrete check for this pipeline |
|---|---|
| **Element Layout** | No two content blocks overlap (now caught automatically by `sizecheck._overlap_issues`); everything sits inside `SAFE_MARGIN`; the frame reads balanced, not lopsided. |
| **Attractiveness** | Each animation earns its place — it *animates* a concept (a sweep, a trace, a reflection across `y=x`), not just a static slide reveal (methodology §5, "Animate, not just display"). |
| **Logic Flow** | Reveal order tracks the narration beats; one teaching idea per scene; nothing appears on screen before the narration speaks to it. |
| **Visual Consistency** | Accent role is consistent (definition = cyan, theorem = gold, example = electric blue, …); one font and size scale throughout; intro and outro match the brand bookends. |
| **Accuracy & Depth** | Faithful to the handout, the math is correct, and each scene's `learning_goal` (content script, methodology §6) is actually delivered — on screen *and* in narration. |

This pass is run by the **VLM critic** (`pipeline/critic.py`, the Code2Video P1
adoption): it extracts the fullest frame of each scene and has a vision model
(MiMo-V2.5) score it against these five dimensions and list concrete defects. It is
**advisory** — it writes a report (`output/critic/<deck>/critique.{json,md}`), never
edits the storyboard; the human stays the layout authority. Commands and the cost
gate are in [`README.md`](README.md) (§ VLM 視覺批改).

**The review loop.** A finding is an opinion to weigh, not a command. Run it as an
iteration, not a one-shot:

1. **Critique** — run the critic over the scene/section; read its scores, defects,
   and suggestions.
2. **Judge & adopt** — decide which to act on. Adopt anything that, *in your
   judgement, makes the video better* — **not only outright bugs**. A suggestion that
   improves clarity, pacing, or teaching is worth taking even when nothing was
   "wrong". Decline one only when it would *hurt* (e.g. break cross-scene
   consistency) or conflict with a deliberate house decision (the flat, no-grid
   aesthetic; a declined typesetting choice). When a suggestion is genuinely
   **contentious** — arguable either way, or a design call that is the author's to
   make — surface it for the human to decide rather than settling it yourself. The
   VLM proposes; you decide, and escalate the close calls.
3. **Modify** — apply the adopted changes (storyboard / template), re-render the
   affected scene.
4. **Re-verify** — run the critic again on the changed frame: confirm the defect is
   gone and no new one appeared. The judge that raised it confirms the fix — your own
   eyes are not enough (this rule was set after a fix was eyeballed but not re-checked).
5. **Final check** — your own read of the result.
6. **Iterate** — repeat until the critic surfaces nothing further worth adopting.

Vet every suggestion: the critic has proposed off-screen coordinates and, against the
house style, gradients/grids. Apply judgement, never blind — the prompt already tells
the model the style is deliberately flat to damp that bias.

---

## Data flow (target)

```
handout-kit HTML  (per-chapter authoritative file, see README「輸入」)
   │  (author reads section, writes storyboard by hand — NOT auto-generated)
   ▼
video/storyboards/<id>.yml
   │
   ├─ lint.py              errors: markup in plain-Text fields, unbalanced $;    (DONE)
   │                       warns: manual \\ in prose, hollow point on a curve
   │                       (a point with hollow_reason: <why> is exempt)
   ├─ sizecheck.py         builds scenes (no render). error: stacked siblings    (DONE)
   │                       at different sizes, or an element clipped off-frame;
   │                       warn: teaching prose in muted, a spill past the safe
   │                       margin, or two content blocks overlapping
   ├─ schema.py            validate format, list reveal targets                  (TODO)
   │
   ▼
narration.parse_say        split each `say` into beats at {show} markers          (DONE)
   │                        → ordered (beat_text, reveal_target) list per scene
   ▼
synth                      one clip per beat; mock = silence sized by word count   (DONE)
   │                        (real billed Gemini = pipeline/tts.py); measure
   │                        duration → audio/<id>/… + manifest.json
   ▼
render (scene.py)          Manim renders each scene silent; a reveal fires at the  (DONE)
   │                        start of its beat; the measured audio duration drives
   │                        the hold (reads manifest.json). Silent MP4 per scene.
   ▼
compose (ffmpeg)           lay each scene's narration under its video (delayed to  (DONE)
   │                        the first reveal), silent track for intro/outro, concat.
   ▼
video/output/<id>.mp4
```

**Orchestrator:** `make.py` is the single entry point — one command runs
parse → synth → render → compose in one process (`make.py --storyboard <yml>
--backend mock`), the pre-render `lint.py` / `sizecheck.py` guards included. It is
**offline only**: mock synthesis (silent clips sized by word count), no billing. Real
Gemini TTS is billed and intentionally NOT wired into make.py (see CLAUDE.md), so a
narrated master still runs through the retained lower-level chain `pipeline/tts.py` →
`build.py` → `mux.py` — superseded by make.py for offline work but kept, not deleted.
Per-stage caching keyed on the visual payload (so editing `say` re-synthesizes audio
but does not re-render Manim) is still (TODO).

### Alignment, restated (so it is not lost in the rewrite)

The first-gen insight survives: alignment does **not** depend on TTS returning
word-level timestamps. We synthesize **one clip per beat**, measure its real duration,
and that duration *is* the reveal hold. Gemini changes the synthesizer, not the
alignment model. (Confirmed: Gemini returns 24 kHz mono 16-bit raw PCM, wrapped to
WAV and measured locally; validated end-to-end on §1.1 — each reveal lands within
~1 frame of its narration beat.)

---

## Open questions / not yet decided

- Template catalog for gen-2: keep the old 9 names, or reshape now that intro/outro are
  separate kinds? (Leaning: keep the content templates, drop nothing yet.)
- BGM: source, ducking, licensing.
- `{show ...}` target grammar: dotted (`math.0`) vs bracketed (`math[0]`). Currently dotted.
- Gemini specifics (resolved): model id `gemini-3.1-flash-tts-preview` (CLI-configurable);
  voice `meta.voice` / `Kore` as a prebuilt voice name; output is 24 kHz mono 16-bit raw
  PCM wrapped to WAV and measured locally. Paid tier confirmed working; the free tier is
  capped at ~10 requests/day for this model, so batch synthesis needs paid billing. `tts.py`
  honors the per-minute 429 `retryDelay` and fails fast on the per-day cap.
