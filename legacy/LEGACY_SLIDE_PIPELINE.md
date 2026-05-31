# Legacy Slide/PDF Pipeline

> **Status: frozen.** This pipeline still runs, but it is no longer the primary path. New media work goes through the Manim storyboard pipeline — see [`MANIM_CHECKLIST.md`](MANIM_CHECKLIST.md), [`MANIM_REFERENCE.md`](MANIM_REFERENCE.md), and [`MANIM_STORYBOARD.md`](MANIM_STORYBOARD.md). This file consolidates what used to be `SLIDES_README.md`, `SLIDES_CHECKLIST.md`, `SCRIPT_README.md`, `VIDEO_README.md`, and `inputs/media_plans/README.md` into a single reference so the frozen machinery is documented in one place.

The pipeline turns a finalized lecture-note section into:

- a slide deck JSON
- a Beamer `.tex` + slide PDF
- a narration draft markdown
- a narration final markdown
- per-slide TTS audio
- a final MP4

Do not develop this pipeline further. Fix bugs to keep it runnable; do not extend.

---

## When to use

- you want a static-slide MP4 (not an animated Manim lesson).
- you have a finalized section in `chapters/*.tex` and a corresponding media plan in `inputs/media_plans/<deck_id>.json`.
- the currently checked-in exemplar is `ch01_inverse_functions`.

If you are starting a new piece of media from scratch, prefer the Manim path.

---

## End-to-end checklist

### 1. Finalize the lecture-note section

- finish the section in `chapters/*.tex` first.
- do not start polishing narration before the mathematical structure is stable.
- if the section structure changes later, expect the slide plan to need updates too.

### 2. Check or edit the slide plan

Open `inputs/media_plans/<deck_id>.json`. Confirm:

- `source_file`
- `source_section`
- `deck_id`
- slide order
- per-slide `slide_id`, `title`, `learning_goal`, `bullets`, `script_draft`

If you want to change slide selection rules for one section, edit this plan file. Do not modify the generator for section-local changes.

### 3. Generate slides and narration files

```powershell
python .\tools\slides_generate_section_media.py --deck-id ch01_inverse_functions --compile auto
```

Regenerated artifacts:

- `artifacts/slide_spec/<deck_id>.json`
- `artifacts/slides/<deck_id>.tex`
- `artifacts/slides/<deck_id>.pdf`
- `artifacts/scripts/<deck_id>_draft.md`

First-time-only:

- `artifacts/scripts/<deck_id>_final.md` is seeded once if absent; subsequent runs preserve it.

JSON + TeX + draft markdown only (skip PDF):

```powershell
python .\tools\slides_generate_section_media.py --deck-id ch01_inverse_functions --compile never
```

### 4. Edit the final narration

Edit only `artifacts/scripts/<deck_id>_final.md`. Never hand-edit `*_draft.md` (it is regenerated and disposable).

Keep these structural lines intact — the TTS layer parses on them:

- `## Slide N: ...`
- `Slide ID: ...`
- `Narration:`

Allowed edits inside a slide's `Narration:` block:

- smoother transitions
- shorter or longer explanations
- warnings about common mistakes
- spoken emphasis
- a light joke or brief aside
- better pacing for video delivery

Constraints:

- do not renumber slides by hand.
- do not delete the `Narration:` marker.
- do not change a slide id in the final file without regenerating the deck.
- do not leave raw LaTeX inside a `Narration:` block — TTS validation now rejects it.
- spoken math should sound like speech ("x squared on minus one to one"), not raw LaTeX source.

Quality pass before moving on:

- each slide narration has one main teaching job.
- neighbouring slides complement each other instead of repeating the same logic.
- warning or example slides do not fully consume a theorem that is supposed to land later.
- the recap slide closes the loop back to the opening motivation, question, or representative example.

### 5. Validate before TTS

```powershell
python .\tools\voice_synthesize_coqui.py --deck-id ch01_inverse_functions --dry-run
python .\tools\voice_synthesize_f5.py --deck-id ch01_inverse_functions --reference-mode clone --dry-run
```

Both commands confirm:

- the final narration file exists.
- each slide still has a narration block.
- slide numbering and slide ids still match the current deck.

If dry-run fails, do not start a long synthesis run.

### 6. Run TTS

Coqui clone:

```powershell
python .\tools\voice_synthesize_coqui.py --deck-id ch01_inverse_functions --coqui-tos-agreed
```

F5 clone:

```powershell
python .\tools\voice_synthesize_f5.py --deck-id ch01_inverse_functions --reference-mode clone
```

Check that WAV filenames match current slide ids. If `--reference-text` is passed to F5, it **must** match the reference WAV's spoken content word for word.

### 7. Validate video inputs

```powershell
python .\tools\slides_render_section_video.py --deck-id ch01_inverse_functions --dry-run
```

Common failure causes: missing audio, stale audio filenames from an older deck version, slide count mismatch between PDF and deck JSON.

### 8. Render the MP4

```powershell
python .\tools\slides_render_section_video.py --deck-id ch01_inverse_functions
```

With a custom audio set:

```powershell
python .\tools\slides_render_section_video.py `
  --deck-id ch01_inverse_functions `
  --audio-dir artifacts\audio\ch01_inverse_functions_f5_clone `
  --output artifacts\video\ch01_inverse_functions_f5_clone.mp4
```

### 9. If the deck changes later

- regenerate slides first.
- re-check `*_draft.md`.
- keep `*_final.md` but manually sync it if slide ids or slide count changed. The generator preserves the final file; it does **not** reconcile structural drift for you.
- re-run TTS for the new deck version.
- re-run video dry-run before rendering.

---

## Media plan format

Each plan file controls one section deck. Top-level fields:

- `deck_id`
- `source_file`
- `source_section`
- `language`
- `defaults.render_hints`
- `slides`

Each slide entry usually contains:

- `slide_id`
- `title`
- `learning_goal`
- `slide_type`
- `bullets`
- `math_blocks`
- `tikz_code`
- `script_draft`
- `source_refs`
- optional `render_hints`

### Selector pattern

Selectors point to LaTeX environments inside one section:

```json
{
  "kind": "definition",
  "index": 0
}
```

Supported usage:

- `math_blocks`: either a literal LaTeX string or an object with `block` (a selector) and `math_index` (zero-based display-math index inside that block).
- `tikz_code`: either `null`, a literal LaTeX string, or an object with `block` pointing at a `figure`.
- `source_refs`: optional traceability selectors that must resolve successfully, even when slide content is editorial rather than directly extracted.

### Plan guidance

Plans should stay slide-native:

- one slide, one learning goal.
- cover the whole section, not just the opening subsection.
- keep formal definitions, theorem statements, assumptions, and final formulas mathematically exact.
- compress prose-heavy remarks into short bullets.
- keep examples focused on one key computation or one key warning.
- prefer a figure slide when the graph or diagram teaches faster than text.
- leave transitions and extra explanation to narration instead of overloading the slide.

---

## Narration drafting rules

### Draft vs. final

- `artifacts/scripts/<deck_id>_draft.md` — regenerated, disposable, normally gitignored.
- `artifacts/scripts/<deck_id>_final.md` — user-owned, tracked, the version TTS reads.

Workflow:

1. generate or regenerate slides.
2. generator rewrites `*_draft.md`.
3. generator seeds `*_final.md` once if it does not exist.
4. after that, edit only `*_final.md`.
5. TTS reads only `*_final.md`.
6. commit the final file when narration changes should persist.

### Mathematical guardrail

Narration can sound less like a textbook, but it must not break the math. Keep these accurate regardless of narration style:

- definitions
- theorem statements
- assumptions and domain restrictions
- final conclusions
- any statement a student could later quote as mathematics

### Narration quality rules

- each slide narration has one main teaching job.
- adjacent slides complement each other instead of repeating the same logic.
- warning or example slides should not fully consume a theorem that is supposed to land later.
- spoken math should sound like speech, not raw LaTeX.
- the recap slide closes the loop by recalling the opening motivation, question, or representative example.

Examples:

- a definition slide explains the rule; a figure slide reads the picture.
- a warning slide shows failure; the theorem slide states the full criterion.
- say "x squared on minus one to one" rather than leaving raw inline LaTeX for TTS to stumble over.

### Where to change narration rules

- per-section narration wording — edit `artifacts/scripts/<deck_id>_final.md`.
- seeded draft wording for future regenerations — edit `inputs/media_plans/<deck_id>.json`.
- markdown structure and parser rules — edit `tools/slides_script_workflow.py`.

---

## Voice reference preparation

Use the preprocessor when you want a cleaned reference clip for voice cloning:

```powershell
python .\tools\voice_preprocess_reference.py
```

Custom input:

```powershell
python .\tools\voice_preprocess_reference.py `
  --input inputs\voice\sample_reference.wav `
  --output artifacts\voice\sample_reference_30s.wav
```

Reference-script notes:

- keep reference inputs under `inputs/voice/` as `.wav` files.
- `inputs/voice/reference_script_en.txt` is a starter script for recording a new F5 reference clip.
- if you pass `--reference-text` to F5 clone mode, it **must** be the verbatim transcript of the exact reference WAV.
- do not reuse `reference_script_en.txt` as the transcript for unrelated sample clips unless the clip was recorded from that script.
- if `--reference-text` is omitted, the wrapper auto-transcribes the reference clip locally.

---

## TTS: Coqui

Script: `tools/voice_synthesize_coqui.py`

What it does:

- reads the deck JSON.
- reads the final narration markdown.
- synthesizes one WAV per slide.
- writes a synthesis manifest.

Default example:

```powershell
python .\tools\voice_synthesize_coqui.py `
  --deck-id ch01_inverse_functions `
  --coqui-tos-agreed
```

Useful options:

- `--deck-id`
- `--script-file`
- `--reference-wav`
- `--voice-mode clone|builtin`
- `--device auto|cpu|cuda`
- `--max-slides`
- `--dry-run`

Notes:

- XTTS v2 requires explicit agreement to Coqui CPML terms.
- TTS reads the final narration file only.
- built-in voices can be routed to a custom output directory to keep multiple audio variants.
- these tools are also usable from the Manim path via bridge files; see [`MANIM_REFERENCE.md`](MANIM_REFERENCE.md).

---

## TTS: F5

Script: `tools/voice_synthesize_f5.py`

Clone example:

```powershell
python .\tools\voice_synthesize_f5.py `
  --deck-id ch01_inverse_functions `
  --reference-mode clone
```

Example-reference mode:

```powershell
python .\tools\voice_synthesize_f5.py `
  --deck-id ch01_inverse_functions `
  --reference-mode example
```

Useful options:

- `--deck-id`
- `--script-file`
- `--reference-mode clone|example`
- `--reference-wav`
- `--reference-text`
- `--device auto|cpu|cuda`
- `--max-slides`
- `--dry-run`

Clone-mode notes:

- F5 clone quality depends on `reference_wav` and `reference_text` matching exactly.
- a mismatched transcript can leak stray words from the reference prompt into every slide audio.
- the wrapper auto-transcribes the reference clip locally when `--reference-text` is omitted.

---

## Video rendering

Script: `tools/slides_render_section_video.py`

What it does:

- validates that slide PDF, slide count, and audio filenames match the current deck.
- renders slide images from the PDF.
- pairs each image with its slide audio.
- creates one MP4 segment per slide.
- concatenates the segments into a final MP4.

Basic render:

```powershell
python .\tools\slides_render_section_video.py --deck-id ch01_inverse_functions
```

With custom audio:

```powershell
python .\tools\slides_render_section_video.py `
  --deck-id ch01_inverse_functions `
  --audio-dir artifacts\audio\ch01_inverse_functions_f5_clone `
  --output artifacts\video\ch01_inverse_functions_f5_clone.mp4
```

Useful options:

- `--deck-id`
- `--audio-dir`
- `--output`
- `--dry-run`
- `--dpi-scale`
- `--lead-in-seconds`
- `--target-width`
- `--target-height`
- `--crf`

---

## Recommended end-to-end commands

### Path A — Coqui clone

```powershell
python .\tools\voice_preprocess_reference.py
python .\tools\voice_synthesize_coqui.py --deck-id ch01_inverse_functions --dry-run
python .\tools\voice_synthesize_coqui.py --deck-id ch01_inverse_functions --coqui-tos-agreed
python .\tools\slides_render_section_video.py --deck-id ch01_inverse_functions --dry-run
python .\tools\slides_render_section_video.py --deck-id ch01_inverse_functions
```

### Path B — F5 clone

```powershell
python .\tools\voice_preprocess_reference.py
python .\tools\voice_synthesize_f5.py `
  --deck-id ch01_inverse_functions `
  --reference-mode clone `
  --dry-run
python .\tools\voice_synthesize_f5.py `
  --deck-id ch01_inverse_functions `
  --reference-mode clone
python .\tools\slides_render_section_video.py `
  --deck-id ch01_inverse_functions `
  --audio-dir artifacts\audio\ch01_inverse_functions_f5_clone `
  --dry-run
python .\tools\slides_render_section_video.py `
  --deck-id ch01_inverse_functions `
  --audio-dir artifacts\audio\ch01_inverse_functions_f5_clone `
  --output artifacts\video\ch01_inverse_functions_f5_clone.mp4
```

---

## Generator behaviour worth knowing

- the draft narration file is always regenerated.
- the final narration file is seeded once and then preserved.
- if the preserved final file no longer matches the current deck, the generator warns instead of overwriting your edits.
- the generator validates plan structure and fails fast when a selector no longer matches the LaTeX section.
- default `--compile auto`; `--compile never` skips PDF compilation; `--compile require` fails if prerequisites are missing.
- Beamer compilation depends on `latexmk`, `pdflatex`, and `beamer.cls`. The compile command enables MiKTeX's installer.

### Where to change pipeline rules

- section-specific slide content, wording, or draft narration — `inputs/media_plans/<deck_id>.json`.
- repo-wide slide selection or density — `tools/slides_generate_section_media.py`.
- repo-wide Beamer layout — `tools/slides_generate_section_media.py`.
- narration markdown format — `tools/slides_script_workflow.py`.
- allowed slide types or render-hint schema — `schemas/slide_deck.schema.json` (and keep the generator in sync).
- audio/video path defaults — `tools/shared_media_paths.py`.

---

## Version-control rules

- commit `artifacts/slides/<deck_id>.tex` when you want the generated Beamer source in history.
- commit `artifacts/scripts/<deck_id>_final.md` when narration edits should persist.
- do not commit `*_draft.md`, slide PDFs, or LaTeX build artifacts.

---

## Troubleshooting

### Generator fails after lecture-note edits

- a `math_index` no longer matches the display-math blocks inside a referenced environment.
- a `figure` selector points to the wrong figure after the section changed.
- an environment occurrence index in the plan is no longer correct.

Fix the plan file, not the generated JSON.

### PDF does not compile

Check `latexmk`, `pdflatex`, `beamer.cls`, and that MiKTeX package installation has been resolved for unattended runs.

### Slide deck changes but final narration stays old

Expected. The generator preserves the final narration file on purpose. Manually sync when slide ids or count change.

### TTS dry-run fails

- the final narration markdown file is missing.
- a `Narration:` block is empty.
- slide numbering or slide ids no longer match the current deck.

### Render dry-run fails (missing audio)

- TTS has not been run yet.
- the audio directory belongs to an older deck version.
- slide ids changed after regeneration, so old WAV filenames are stale.

`slides_render_section_video.py --dry-run` exists precisely to catch this before a long ffmpeg run.

### XTTS run fails before synthesis

- `--coqui-tos-agreed` was not provided.
- the reference WAV is missing.
- CUDA was requested but is not available.

### Final MP4 render fails

- slide PDF missing.
- narration WAVs missing or misnamed.
- PDF page count does not match deck JSON.
- ffmpeg could not be resolved through `imageio_ffmpeg`.

### Two neighbouring slides sound repetitive

One of them should narrow its job:

- definition slide — keep the logical rule.
- figure slide — keep the reading of the picture.
- theorem slide — keep the formal criterion.
- recap slide — add closure rather than repeating the theorem.

### You accidentally edited the draft file

Regenerate the section media. The draft is disposable.

### You want to keep a funny line without risking the math

Put the joke in narration (`Narration:` block in `*_final.md`), not in slide bullets or extracted formulas.

---

## Crossing to the Manim path

If you decide a section should become a Manim lesson instead, you have two starting points:

- **hand-write the storyboard directly from the LaTeX source**, following [`MANIM_STORYBOARD.md`](MANIM_STORYBOARD.md). This is the recommended path.
- **seed a first-draft storyboard from an existing slide deck JSON**:

  ```powershell
  python .\tools\manim_seed_storyboard.py --deck-id ch01_inverse_functions
  ```

  The seeded YAML still needs substantial hand-revision before it matches the Manim quality bar.

Once the Manim storyboard is the source of truth for a section, narration drift between the two paths is the author's responsibility — the slide/PDF `*_final.md` and the storyboard's per-scene `voiceover` are independent artifacts.
