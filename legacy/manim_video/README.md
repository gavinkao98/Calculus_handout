# legacy/manim_video/ — gen-2 Manim 講義影片產線（2026-09-28 封存）

## 是什麼

gen-2 影片產線的 **Manim 渲染引擎整包**：storyboard YAML → `make.py`（parse → synth →
render → compose）→ Manim 逐場渲染 → ffmpeg 合成成片。內容包括單一入口 `make.py`、
渲染側 `pipeline/` 模組（`scene`／`blocks`／`brand`／`focus`／`pacing`／`sizecheck`／
`floorprobe`／`texlock`／`texparts`／`critic`／`lint`／`schema`／`scene_roles`）、模板
（`pipeline/templates/`）、版面與主題（`pipeline/visuals/`）、LaTeX 用的 vendored 字型
Instrument Sans（`pipeline/fonts/`）、各節 hook 動畫（`animations/`）、五支正典 storyboard
與 20 支 `_demo_*`、以及綁在這套引擎上的 selftest 與設計／工單文檔。

gen-1（`legacy/scripts/manim_*`）是更早的另一套 Manim 產線，與本資料夾無關，說明見
[`../README.md`](../README.md)。

## 為何封存

2026-09-28 使用者拍板：「我現在正式決定，以後影片都走 remotion 這個路線。Manim 這個路線被
放棄了。」影片線自此只走 Remotion。這次搬移的契約、邊界規則、逐檔清單與驗收標準都在
[`../../video/KICKOFF-remotion-unification.md`](../../video/KICKOFF-remotion-unification.md)，
本檔不重述。

## 回退方式

回退錨點＝annotated tag **`archive/2026-09-28-manim-gen2-final`**（指向 `60c505e`，搬移前
最後一個 commit；本機建立，push 與否由使用者決定）。

```bash
git checkout archive/2026-09-28-manim-gen2-final -- video/   # 只還原 video 子樹
git diff archive/2026-09-28-manim-gen2-final -- video/        # 看封存後動了什麼
```

各檔用 `git mv` 搬入，個別歷史可用 `git log --follow legacy/manim_video/<路徑>` 追到
`video/<路徑>` 時代。

## 不再維護、不保證可執行

- **要跑請 checkout tag**（例如 `git worktree add ../manim-gen2 archive/2026-09-28-manim-gen2-final`），
  在封存前的佈局與環境下執行；環境層的 manim 依賴也以該 tag 的 `requirements.lock`／
  `ENVIRONMENT.md` 為準。
- 這裡的程式碼**原樣搬入、未改路徑**：`pipeline/_bootstrap.py` 的
  `REPO_ROOT = parents[2]` 在這裡會算成 `legacy/`；`make.py` 寫 `video/output/…`、
  selftest 呼叫 `video/pipeline/schema.py` 等，都是封存前的 `video/` 佈局。
- `pipeline/` 在這裡**只有渲染側**：共用層（`tts.py`、`audio.py`、`narration.py`、
  `timing.py`、`pauses.py` …）留在 `video/pipeline/`，所以本資料夾的 `make.py` 單獨
  import 不起來。這是刻意的——共用層只有一份、由 Remotion 線維護。

## 逐項對照表（從 → 到）

規則：`video/<相對路徑>` → `legacy/manim_video/<相對路徑>`，內部相對佈局不變。

### 程式（Task 1）

| 從 | 到 | 檔數 | 備註 |
|---|---|---|---|
| `video/make.py` | `legacy/manim_video/make.py` | 1 | 原樣；loudnorm 那段另抽一份到 `video/pipeline/loudnorm.py`（見下） |
| `video/scratch_frames.py` | `legacy/manim_video/scratch_frames.py` | 1 | 離線抽幀工具 |
| `video/pipeline/{scene,blocks,brand,focus,pacing,floorprobe,sizecheck,texlock,texparts,critic,lint,schema,scene_roles}.py` | `legacy/manim_video/pipeline/` | 13 | 渲染側模組 |
| `video/pipeline/templates/` | `legacy/manim_video/pipeline/templates/` | 15 | 整夾 |
| `video/pipeline/visuals/` | `legacy/manim_video/pipeline/visuals/` | 4 | 整夾（`layout`／`theme`／`graph_utils`） |
| `video/pipeline/fonts/` | `legacy/manim_video/pipeline/fonts/` | 43 | 整夾（Instrument Sans，LaTeX 用） |
| `video/pipeline/_bootstrap.py` | `legacy/manim_video/pipeline/_bootstrap.py` | 1 | **複製**完整版（含 `apply_tex_template`）；`video/` 原位留精簡版 |
| `video/pipeline/__init__.py` | `legacy/manim_video/pipeline/__init__.py` | 1 | **複製**；`video/` 原位保留 |
| `video/pipeline/_selftest_*.py`（59 支） | `legacy/manim_video/pipeline/` | 59 | 見下方名單 |
| `video/pipeline/_selftest_make_loudnorm.py` | `legacy/manim_video/pipeline/_selftest_make_loudnorm.py` | 1 | 原檔原樣（測 `make.compose` 的 loudnorm 尾段）；`video/` 那份改名 `_selftest_loudnorm.py`、改測 `pipeline/loudnorm.py` |
| （拆出）`video/pipeline/_selftest_pauses.py` 的 (c) 段 | `legacy/manim_video/pipeline/_selftest_pauses_schema.py` | 1 | 依賴 `schema.schema_storyboard`；其餘留在 `video/` |
| （拆出）`_selftest_{coverage,pedagogy,provenance}.py` 的 `test_schema_integration` | `legacy/manim_video/pipeline/_selftest_{coverage,pedagogy,provenance}_schema.py` | 3 | shell out 到 `schema.py`；檢查器本身的單元測試留在 `video/` |
| （拆出）`_selftest_scene_align_integration.py` 的 `test_tts_scene_path_and_make_consumers` | `legacy/manim_video/pipeline/_selftest_scene_align_integration_make.py` | 1 | 依賴 `make.py`；TTS 退階梯的六個測試留在 `video/`（`tts.py` 半段改名 `test_tts_scene_path` 留下） |
| `video/animations/` | `legacy/manim_video/animations/` | 4 | 各節 hook 動畫 |
| `video/storyboards/{ch01_inverse_functions,ch03_trig_derivatives,ch03_trig_derivatives_mimo,ch03_chain_rule,ch03_chain_rule_mimo}.yml` | `legacy/manim_video/storyboards/` | 5 | 正典 storyboard；§3.2 Phase A 的 beat 切分成果在 `ch03_chain_rule*.yml` |
| `video/storyboards/_demo_*.yml` | `legacy/manim_video/storyboards/` | 20 | 模板 demo |
| `video/storyboards/_fixtures/{fontfloor,layout_rules}.yml` | `legacy/manim_video/storyboards/_fixtures/` | 2 | 引擎 selftest 的 fixture |
| `video/_audit/design-template-system/` | `legacy/manim_video/_audit/design-template-system/` | 11 | 整夾 |
| `video/_audit/REVIEW-{pipeline-assessment-2026-09-07,transition-ab,worked-example-template-applied}.html` | `legacy/manim_video/_audit/` | 3 | 引擎相關稽核報告 |

搬走的 59 支 selftest（名稱省略 `_selftest_` 前綴）：all_six_table、answer_band_paced、
aside_rail、capacity、carry、carry_exit_conflict、carry_schema、chord_vs_arc、color_map、
continuity_argument、critic_confirm、critic_fullest、critic_pauses、critic_scene_aligned、
definition_math_label、derivation_hung、derivation_paced、derivation_rail、figure_labels、
floorprobe、focus_and_pacing、focus_reveal_order、graph_labels、graph_single、inset、
inset_lens、layout_rules、lint_registers、make_mock_subset、make_scene_aligned、
make_transition、pacing、pairing_and_opening、proof_transform、reveal_timing、scene_roles、
sector_inequality、semantic_palette、show_grammar、side_branch、sizecheck、stock_anim、
sweep、sync_gate、tail_clock、template_registry、tex_parts、texlock、text_metrics、
theorem_aside、theorem_proof_label、theorem_regime、title_by_id、transform、type_scale、
value_table、worked_example、wrap_mixed、zero_height_prose。

### 文檔（Task 2）

| 從 | 到 |
|---|---|
| `video/DESIGN.md` | `legacy/manim_video/DESIGN.md`（`video/` 另寫精簡新版，只承接與渲染器無關的節） |
| `video/CODE2VIDEO_STUDY.md` | `legacy/manim_video/CODE2VIDEO_STUDY.md` |
| `video/KICKOFF-motion-primitives.md` | `legacy/manim_video/KICKOFF-motion-primitives.md` |
| `video/KICKOFF-motion-language-gaps.md` | `legacy/manim_video/KICKOFF-motion-language-gaps.md` |
| `video/KICKOFF-motion-language-rollout.md` | `legacy/manim_video/KICKOFF-motion-language-rollout.md` |
| `video/KICKOFF-shared-layer-v1.md` | `legacy/manim_video/KICKOFF-shared-layer-v1.md` |
| `video/KICKOFF-worked-example-template.md` | `legacy/manim_video/KICKOFF-worked-example-template.md` |
| `video/KICKOFF-toolline-backlog-r1.md` | `legacy/manim_video/KICKOFF-toolline-backlog-r1.md` |
| `video/KICKOFF-toolline-backlog-r2.md` | `legacy/manim_video/KICKOFF-toolline-backlog-r2.md` |
| `video/KICKOFF-pipeline-hardening.md` | `legacy/manim_video/KICKOFF-pipeline-hardening.md` |
| `video/KICKOFF-round17-dispatch.md` | `legacy/manim_video/KICKOFF-round17-dispatch.md` |
| `video/KICKOFF-s31-amplify.md` | `legacy/manim_video/KICKOFF-s31-amplify.md` |
| `video/content_scripts/_audit/HOOK-ENGINEERING-RUBRIC.md` | `legacy/manim_video/content_scripts/_audit/HOOK-ENGINEERING-RUBRIC.md` |
| `video/content_scripts/_audit/PLAN-routeA-plex-latex.md` | `legacy/manim_video/content_scripts/_audit/PLAN-routeA-plex-latex.md` |

## 什麼留在 `video/`、為何

- **共用層（Remotion 在用）**：`pipeline/tts.py` 與全部 `tts_*.py`、`scene_align.py`、
  `scene_fallback.py`、`narration.py`、`audio.py`、`timing.py`、`atomicio.py`、
  `derived_check.py`、`derive_spoken.py`、`template_names.py`、`captions.py`、`pauses.py`、
  `stillness.py`、`rewatch_pack.py`、`house_audio.py`、`listening_pack.py`、`loudness_ab.py`、
  `mimo_preview.py`、`_regression_scene_align.py`、`run_selftests.py`、`_bootstrap.py`（精簡版：
  只剩 `bootstrap()` 的 `sys.path` 邏輯與 `section_output_dir`）。這些與渲染器無關，Remotion
  線（`video/remotion/`）的配音與成片步驟直接呼叫它們。
- **新增 `pipeline/loudnorm.py`**：自 `make.py` 原樣抽出 `HOUSE_LUFS`／`LOUDNORM_TP`／
  `LOUDNORM_TOL_I`、`_loudnorm_final` 與它直接呼叫的 `_ffmpeg`；Remotion 的
  `paper/scripts/loudnorm.py` 改從這裡 import，成片響度契約（−19 LUFS、TP −1.5 dBTP）不變。
- **內容層確定性檢查器**：`provenance.py`、`pedagogy.py`、`step_coverage.py`、
  `example_coverage.py`、`source_rev.py`、`review_pack.py`、`_screen_contract.py`、
  `narration_review.py`，以及 `storyboards/_fixtures/` 的五支內容層 fixture
  （`otf_provenance`／`sc_coverage`／`scaffold`／`pedagogy_audit`／`pedagogy_audit_draft`）。
  目前只被 `schema.py`（已封存）呼叫；未來接 Remotion storyboard 時重掛，所以與其單元測試
  一起留下。
- **內容層**：`content_scripts/`（旁白內容稿、口語版、rubric、稽核報告）——旁白文字與渲染器
  無關，五支正典 storyboard 的 `say:` 也都已在那裡完整保全。
- **品牌資產**：`pipeline/assets/`（品牌 logo＝Remotion 唯一沿用的固定元素，以及 house
  audio cue）。
- **selftest**：留下 24 支（`run_selftests.py` 全綠），都不 import manim、不碰 `make.py`／
  `schema.py`／`critic.py`。

## 封存後已知的懸空參照（未處理，列給後續輪次）

- `video/experiments/forced_alignment_dean/render_aligned_scene.py` 仍 `from manim import …`、
  `from pipeline.scene import LessonScene`；該實驗夾依 KICKOFF §2 原地不動（已結案），此檔
  已無法執行。
- 仍以 `video/storyboards/<正典 deck>.yml`（或 `video/animations/`）為預設路徑的留存程式：
  `pipeline/derive_spoken.py`（`STORY`）、`pipeline/rewatch_pack.py`（`main()` 讀 deck）、
  `pipeline/review_pack.py`（hook 路徑）、`pipeline/_regression_scene_align.py`、
  `video/_audit/_gen/worked_example_template.gen.py`、`content_scripts/_audit/_gen/` 的數支
  報告產生器。Remotion 版 storyboard 的位置與這些入口怎麼接，屬 KICKOFF §6 的後續輪次。
