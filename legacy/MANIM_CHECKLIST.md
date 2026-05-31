# Manim Workflow Checklist

The phase-by-phase operational checklist for producing a calculus teaching video through the **Manim animation pipeline** (LaTeX source → storyboard → rendered MP4). For the frozen static-slide/PDF path, see [`LEGACY_SLIDE_PIPELINE.md`](LEGACY_SLIDE_PIPELINE.md).

Related docs: [`MANIM_REFERENCE.md`](MANIM_REFERENCE.md) (full reference), [`MANIM_STORYBOARD.md`](MANIM_STORYBOARD.md) (LaTeX-to-YAML translation playbook), [`CONTENT_SPEC.md`](CONTENT_SPEC.md) (lecture-note authoring rules).

---

## Phase 0 — Environment Check (one-time)

```powershell
python -c "import manim; print(manim.__version__)"          # >= 0.20.1
ffmpeg -version                                               # any recent version
python -c "import torch; print(torch.cuda.is_available())"   # True preferred (GPU TTS)
python -c "import matplotlib; print(matplotlib.__version__)" # optional graph_focus debug preview
```

Optional (TTS only):

```powershell
python -c "import sys; sys.path.insert(0,'.deps'); from TTS.api import TTS; print('Coqui OK')"
python -c "import sys; sys.path.insert(0,'.deps_f5'); import f5_tts; print('F5 OK')"
```

---

## Phase 1 — Draft the Storyboard from the Chapter

The storyboard YAML is hand-written from the finalized LaTeX source. It does **not** regenerate from the chapter file; every change to `chapters/*.tex` that affects the target section requires a manual YAML revision.

Work through [`MANIM_STORYBOARD.md`](MANIM_STORYBOARD.md) for the full translation playbook (scene decomposition, environment-to-template mapping, voiceover rewriting, figure handling, `content_type` assignment, timing). The condensed flow:

1. Read the target section in `chapters/<chapter>.tex` end to end.
2. Sketch a scene list in order (one bullet per scene) including the required opening `title_bullets` and closing `recap_cards`.
3. Create `inputs/manim_storyboards/<DECK_ID>.yml` with the top-level `deck_id`, `language`, `theme`, `video`, and `scenes` fields (see `schemas/manim_storyboard.schema.json` for the contract).
4. Fill in each scene: `scene_id`, `template`, `content_type` (MUST on `definition_math` scenes), `title`, `voiceover`, `data`, `timing`, `scene_exit: "hold"` by default.

### Legacy bootstrap (optional)

A first-draft YAML can be seeded from an existing slide-pipeline deck JSON:

```powershell
python .\tools\manim_seed_storyboard.py --deck-id <DECK_ID>
```

Prerequisite: `artifacts/slide_spec/<DECK_ID>.json` exists. The seeded draft is a bootstrap, not a finished storyboard -- it must be hand-revised against `MANIM_STORYBOARD.md` before rendering.

Once the YAML exists (hand-written or seeded-and-revised), open it and verify: `deck_id`, `language`, scene count, template assignments.

---

## Phase 2 — Edit the Storyboard

The storyboard YAML is the **single source of truth**. Edit per scene:

| Field | Purpose | Written for |
|-------|---------|-------------|
| `voiceover` | Spoken narration | The ear (plain English, no raw LaTeX) |
| `voiceover_beats` | Optional beat-level narration | Synchronize spoken math with reveal timing |
| `data` | Visual content (bullets, math_lines, steps, axes, plots) | The eye (LaTeX math) |
| `template` | One of the 9 templates (see below) | Animation style |
| `content_type` | Accent colour: definition=cyan, theorem=gold, example=highlight, warning=coral | Visual meaning |
| `timing` | `lead_in_seconds`, `hold_after_seconds`, `minimum_duration_seconds` | Pacing |
| `hook` | Custom animation override (rare) | Special scenes only |
| `disabled` | `true` to skip a scene temporarily | Iteration |

**Rules:**
- One teaching idea per scene
- One spoken paragraph per `voiceover`
- `voiceover` and `data` complement each other, never duplicate
- Use `voiceover_beats` for long derivations whose formulas should appear only when spoken. Keep each beat to one sentence or one algebraic move.
- Use YAML block scalars (`|` / `>`) when narration paragraphs or LaTeX blocks become hard to read as one escaped line

### Template Selection Guide

| Template | Use when... | Required data |
|----------|-------------|---------------|
| `title_bullets` | Opening or overview | `bullets` |
| `definition_math` | Formal definition or proposition | `statement`, `math_lines` |
| `example_walkthrough` | Worked example with steps | `steps`, `takeaway`, `math_lines` (opt), `math_layout` (opt), `decay_previous` (opt) |
| `graph_focus` | Showing a graph/plot | `axes`, `plots`, `annotations` |
| `procedure_steps` | Step-by-step algorithm | `steps`, `worked_equations`, `math_layout` (opt) |
| `recap_cards` | End-of-section summary | `points`, `identities` |
| `section_transition` | Topic change interlude | `subtitle` (opt), `upcoming` (opt) |
| `theorem_proof` | Theorem + proof | `theorem_statement`, `proof_steps` |
| `comparison` | Side-by-side concepts | `left`, `right` (each: `label`, `items`, `math`) |

---

## Phase 3 — Preview Individual Scenes

Iterate on one scene at a time at preview quality:

```powershell
python .\tools\manim_preview_scene.py --deck-id <DECK_ID> --scene-id <SCENE_ID>
```

Watch the output at `artifacts/manim/<DECK_ID>/scenes/NN_<SCENE_ID>.mp4`.

Validate without rendering:

```powershell
python .\tools\manim_preview_scene.py --deck-id <DECK_ID> --scene-id <SCENE_ID> --dry-run
```

Force re-render after code changes:

```powershell
python .\tools\manim_preview_scene.py --deck-id <DECK_ID> --scene-id <SCENE_ID> --force
```

For `graph_focus` scenes, use the fast Matplotlib preview when you only need to tune a curve or `label_x`:

```powershell
python .\tools\manim_preview_graph_focus.py --deck-id <DECK_ID> --scene-id <SCENE_ID>
```

Repeat until every scene looks right.

---

## Phase 4 — Full Preview Render

Validate the complete lesson:

```powershell
python .\tools\manim_render_lesson.py --deck-id <DECK_ID> --quality preview --dry-run
```

Render and concatenate all scenes:

```powershell
python .\tools\manim_render_lesson.py --deck-id <DECK_ID> --quality preview
```

Watch `artifacts/video/<DECK_ID>_manim.mp4`. Check:
- [ ] All scenes present in correct order
- [ ] LaTeX renders without errors
- [ ] Midnight Canvas aesthetic intact
- [ ] Active equation stays visually dominant; old context dims cleanly
- [ ] Algebra derivations with multiple `=` lines feel stable rather than jumpy
- [ ] Transitions smooth

---

## Phase 5 — Generate TTS Audio

### 5a. Export bridge files

```powershell
python .\tools\manim_render_lesson.py --deck-id <DECK_ID> --quality preview --with-audio
```

This creates:
- `artifacts/manim/<DECK_ID>/tts_deck.json`
- `artifacts/manim/<DECK_ID>/narration.md`

It will fail with an error showing the exact TTS commands to run. This is expected.

### 5b. Run TTS

**Coqui XTTS (clone mode)** — best quality, requires `artifacts/voice/reference_30s.wav`:

```powershell
python .\tools\voice_synthesize_coqui.py `
  --deck-json artifacts\manim\<DECK_ID>\tts_deck.json `
  --script-file artifacts\manim\<DECK_ID>\narration.md `
  --output-dir artifacts\audio\<DECK_ID>_manim `
  --manifest artifacts\audio\<DECK_ID>_manim\manifest.json `
  --coqui-tos-agreed
```

**Coqui Jenny (builtin mode)** — no reference WAV needed:

```powershell
python .\tools\voice_synthesize_coqui.py `
  --deck-json artifacts\manim\<DECK_ID>\tts_deck.json `
  --script-file artifacts\manim\<DECK_ID>\narration.md `
  --output-dir artifacts\audio\<DECK_ID>_manim `
  --manifest artifacts\audio\<DECK_ID>_manim\manifest.json `
  --model-name "tts_models/en/jenny/jenny" `
  --voice-mode builtin
```

**F5-TTS (example mode)** — alternative, no reference WAV:

```powershell
python .\tools\voice_synthesize_f5.py `
  --deck-json artifacts\manim\<DECK_ID>\tts_deck.json `
  --script-file artifacts\manim\<DECK_ID>\narration.md `
  --output-dir artifacts\audio\<DECK_ID>_manim `
  --manifest artifacts\audio\<DECK_ID>_manim\manifest.json `
  --reference-mode example
```

Output: `artifacts/audio/<DECK_ID>_manim/01_<scene_id>.wav` through `NN_<scene_id>.wav`

### 5c. Listen and verify

Play individual WAV files. If a scene sounds wrong, adjust `voiceover` in the YAML, re-export bridge files (repeat 5a), and re-run TTS for that scene with `--max-slides N`.
Narration-only edits now reuse the cached silent Manim scene video, so you should not need to re-render the visuals unless the scene's visual data changed.

### 5d. Proofread narration with reveal markers

`narration.md` now contains 〔顯示式子〕 / 〔顯示步驟〕 / 〔顯示註記〕 / 〔顯示總結〕 markers wherever the rendered scene will pause for a dynamic reveal. They tell the proofreader exactly where the animation will trigger. **Do not delete or move the markers** — keep your edits to the prose between them. The hidden `<!-- bookmark-marks: ... -->` comment is the sync tool's ground truth; leaving both intact lets `manim_sync_narration_back.py` translate the markers back to `<bookmark .../>` form when writing to YAML.

If you accidentally drop a marker, the sync command refuses to write and prints which scene is inconsistent. Fix the markdown (re-add the missing 〔顯示...〕) and re-run.

---

## Phase 6 — Final Render with Audio

```powershell
python .\tools\manim_render_lesson.py --deck-id <DECK_ID> --quality final --with-audio
```

This:
1. Re-renders all scenes at 1920x1080, 30fps (caches scenes that haven't changed)
2. Muxes each scene video + WAV (applies lead-in, hold-after, padding)
3. Concatenates into `artifacts/video/<DECK_ID>_manim.mp4`

---

## Phase 7 — Quality Check

```powershell
ffprobe -v quiet -print_format json -show_format -show_streams artifacts\video\<DECK_ID>_manim.mp4
```

Checklist:
- [ ] Resolution: 1920x1080
- [ ] Frame rate: 30fps
- [ ] Audio stream present
- [ ] All scenes play with synchronized narration
- [ ] No audio cut-off or drift
- [ ] Lead-in silence feels natural
- [ ] Total duration reasonable for content
- [ ] Midnight Canvas style consistent

---

## Quick Reference

```
inputs/manim_storyboards/<DECK_ID>.yml     <- source of truth (edit this)
artifacts/manim/<DECK_ID>/scenes/          <- cached scene MP4s
artifacts/manim/<DECK_ID>/graph_previews/  <- fast graph debug PNGs
artifacts/manim/<DECK_ID>/segments/        <- muxed scene+audio MP4s
artifacts/manim/<DECK_ID>/tts_deck.json    <- TTS bridge deck
artifacts/manim/<DECK_ID>/narration.md     <- Manim narration (proofread here, sync back to YAML)
artifacts/audio/<DECK_ID>_manim/           <- scene WAV files
artifacts/video/<DECK_ID>_manim.mp4        <- final output
```

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError: manim` | `pip install manim` |
| `FFmpeg is not available` | Install ffmpeg or `pip install imageio-ffmpeg` |
| `matplotlib is not installed` | Install `matplotlib` if you want to use `manim_preview_graph_focus.py` |
| `Missing voice reference WAV` | Provide `artifacts/voice/reference_30s.wav` or use `--voice-mode builtin` / `--reference-mode example` |
| `XTTS v2 requires explicit agreement` | Add `--coqui-tos-agreed` |
| Scene not re-rendering after edits | Use `--force` (fingerprint may have matched) |
| `Hook could not be resolved` | Check the `hook` field points to an existing callable, preferably under `tools/manim_hooks/` |
| Audio too fast / robotic | Adjust `--speed` (default 1.03), `--max-chars-per-chunk` (default 220), `--inter-chunk-pause-ms` (default 120) |
| Video-audio sync drift | Increase `minimum_duration_seconds` in scene timing |
| MiKTeX download prompts | Run `miktex-console` and update packages |

---

## Timing Adjustment Tips

The mux step computes: `target_duration = max(video_duration, lead_in + audio_duration + hold_after, minimum_duration)`

- If audio is longer than video: video's last frame is cloned (frozen)
- If video is longer than audio: silence pads the audio
- If `voiceover_beats` is present: TTS writes per-beat durations to `manifest.json`, and Manim waits beat-by-beat before muxing.
- To lengthen a scene: increase `minimum_duration_seconds` or add more animation steps in `data`
- To add breathing room: increase `hold_after_seconds`
- Default timing: `lead_in=0.15s`, `hold_after=0.45s`, `minimum_duration=4.0s`
