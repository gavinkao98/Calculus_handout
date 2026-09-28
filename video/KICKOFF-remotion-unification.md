# KICKOFF — 影片線統一走 Remotion，Manim gen-2 封存（2026-09-28）

> **立檔：2026-09-28**（使用者拍板當日）。本檔是這次搬移的**契約與紀錄**：裁決原文、
> 搬／留的邊界規則與逐檔清單、三個並行 task 的驗收標準、回退方式。之後的 REBUILD_STATUS／
> README／legacy README 都指向本檔，不重述。比照講義線的
> [`../handout/latex/KICKOFF-latex-unification.md`](../handout/latex/KICKOFF-latex-unification.md)。

---

## 0. 裁決（使用者，2026-09-28）

| # | 裁決原文（照抄） | 對本檔的意思 |
|---|---|---|
| 1 | 「我現在正式決定，以後影片都走 remotion 這個路線。Manim 這個路線被放棄了。」 | Remotion 是影片線唯一正式渲染器；Manim gen-2 引擎（`make.py`＋`pipeline/` 渲染側＋模板＋storyboard＋hook）全數封存到 `legacy/manim_video/` |
| 2 | 「你看一下有哪些檔案可以保留的，哪些檔案不需要的。把不需要的移到 legacy 裡面。」 | 保留＝Remotion 正在用的共用層（TTS／對齊／音訊）＋與渲染器無關的內容層；其餘搬走，`git mv` 保留歷史 |
| 3 | 「需不需要新 commit 起來……你標記一下」→ 已建 tag | **回退錨點＝annotated tag `archive/2026-09-28-manim-gen2-final`**（指向 `60c505e`，搬移前最後一個 commit；本機建立，push 與否由使用者決定） |
| 4 | 「都按照你建議的處理吧。」 | 採納 §1 的六項建議：目的地 `legacy/manim_video/`；DESIGN.md 整份搬走＋新開精簡版；五支正典 storyboard 跟引擎走；`paper/` 升格**另開一輪**；環境層退役 manim；文檔改寫同一輪內做完 |

**回退方式**（後悔時）：

```bash
git checkout archive/2026-09-28-manim-gen2-final -- video/   # 只還原 video 子樹
git diff archive/2026-09-28-manim-gen2-final -- video/        # 看封存後動了什麼
```

## 1. 六項建議（已採納）

1. **目的地**：`legacy/manim_video/`（gen-2 Manim 引擎整包；gen-1 在 `legacy/scripts/manim_*`）。**規則＝`video/<相對路徑>` → `legacy/manim_video/<相對路徑>`**，內部相對佈局不變，`git log --follow` 找得到。
2. **`DESIGN.md`**：183 KB、九成是 storyboard 格式／Lectern 版面／模板目錄／容量契約，整份搬走；另開精簡的新 `video/DESIGN.md`，只承接與渲染器無關的節（Data flow、`{show}` 旁白文法與 beat 契約、配音工作流設計、語意色軸的講義對照表）。
3. **五支正典 storyboard**（`ch01_inverse_functions`、`ch03_trig_derivatives{,_mimo}`、`ch03_chain_rule{,_mimo}`）跟引擎走；旁白文字已在 `content_scripts/`（`.md`／`.spoken.yml`／`_narration_spoken.md`）完整保全。§3.2 Phase A 的 beat 切分成果就在 `legacy/manim_video/storyboards/ch03_chain_rule*.yml`，Remotion 版 §3.2 要參考就去那裡讀。
4. **`experiments/remotion_styles/paper/` 這輪不升格**（不改路徑），升格另開一輪，免得 `tts_workflow/README.md` 與 `REBUILD_STATUS.md` 幾十處路徑同時在動。
5. **環境層**：`tools/doctor.py` 拿掉 manim／ManimPango／manim-Tex 檢查；MiKTeX 對影片線降為非必要（講義線仍必要，不能整個刪）；`requirements.lock` 拆掉 manim 一族；`tools/setup.ps1` 拿掉 Instrument Sans 的 MiKTeX 註冊步驟（字型隨 `pipeline/fonts/` 進 legacy）。**本機 gitignored 遺留**：`video/media/`（Tex 快取，純可重生）刪；`video/output/`（含付費 TTS 原音）**不動**；`.deps_voiceover/` 本機不存在。
6. **文檔改寫同一輪**：`video/README.md`、`REBUILD_STATUS.md`、`REVIEW_GATES.md`、根 `CLAUDE.md`／`README.md` 等在同一 commit 系列內改完，否則新 session 讀到的仍是「Manim 現役」。§3.2 KICKOFF 的 Phase B 重寫成 Remotion 版另開。

## 2. 邊界規則（先於清單）

| 判準 | 結果 |
|---|---|
| 直接 `import manim`，或 import 了任何本輪搬走的模組（傳遞閉包） | **搬** |
| selftest 對 `make.py`／`schema.py`／`critic.py` shell out，或 import 搬走的模組 | **搬**（純 docstring 提到 make.py 不算，要看實際執行路徑） |
| Remotion `paper/` 目前實際呼叫的（`tts.py` 一族、loudnorm、logo 資產） | **留** |
| 內容層（內容稿、口語版、rubric、稽核報告、教學 SPEC、方法論） | **留**（含 Manim 時代 §3.1 的稽核報告，那是歷史紀錄，`content_scripts/_audit/` 原地不動） |
| 內容層確定性檢查器（`provenance`／`pedagogy`／`step_coverage`／`example_coverage`／`source_rev`／`review_pack`（內容稿解析器）／`_screen_contract`／`narration_review`）及其 fixtures | **留**（目前只被 `schema.py` 呼叫；未來接 Remotion storyboard 時重掛） |
| 只綁 Manim 引擎的工單／設計文檔（motion primitive、共用層 v1、模板、工具線 backlog、硬化清單） | **搬** |
| 已結案的實驗夾（`experiments/forced_alignment_dean/`）、`video/_archive/` | **原地不動**（已是歷史夾） |

## 3. 逐檔清單

### 3.1 搬到 `legacy/manim_video/`（`git mv`，相對路徑不變）

**程式（Task 1 擁有）**

- `video/make.py`、`video/scratch_frames.py`
- `video/pipeline/`：`scene.py`、`blocks.py`、`brand.py`、`focus.py`、`pacing.py`、`floorprobe.py`、`sizecheck.py`、`texlock.py`、`texparts.py`、`critic.py`、`lint.py`、`schema.py`、`scene_roles.py`
- `video/pipeline/templates/`（整夾）、`video/pipeline/visuals/`（整夾：`layout.py`／`theme.py`／`graph_utils.py`）、`video/pipeline/fonts/`（整夾，LaTeX 用 Instrument Sans）
- `video/pipeline/_bootstrap.py`：**複製**完整版到 legacy（archive 自洽），原位保留精簡版（見 §4 Task 1）
- `video/pipeline/__init__.py`：**複製**一份到 legacy（原位保留）
- `video/pipeline/_selftest_*.py`：凡直接 `import manim`（27 支）、或 import 搬走模組（`_selftest_capacity`、`_carry_exit_conflict`、`_carry_schema`、`_chord_vs_arc`、`_critic_*`×4、`_definition_math_label`、`_focus_reveal_order`、`_graph_labels`、`_graph_single`、`_inset`、`_inset_lens`、`_lint_registers`、`_reveal_timing`、`_semantic_palette`、`_show_grammar`、`_side_branch`、`_template_registry`、`_theorem_aside`、`_theorem_proof_label`、`_title_by_id`、`_type_scale`、`_value_table`、`_wrap_mixed`、`_answer_band_paced`）、或實際跑 `make.py`（`_make_mock_subset`、`_make_transition`、`_make_scene_aligned`、`_sync_gate`；其餘名字含 make 的要逐支看實際執行路徑）→ 搬。**`_selftest_make_loudnorm.py` 例外**：改名 `_selftest_loudnorm.py`，改測新的 `pipeline/loudnorm.py`（留）。**`_selftest_pauses.py` 例外**：`pauses.py` 留，selftest 留，只把依賴 `schema.schema_storyboard` 的 (c) 段拆出隨 schema 搬（或刪並在 commit body 說明）。
- `video/animations/`（整夾）
- `video/storyboards/`：五支正典 `ch01_inverse_functions.yml`、`ch03_trig_derivatives.yml`、`ch03_trig_derivatives_mimo.yml`、`ch03_chain_rule.yml`、`ch03_chain_rule_mimo.yml`；全部 20 支 `_demo_*.yml`；`_fixtures/fontfloor.yml`、`_fixtures/layout_rules.yml`。**留**：`_fixtures/otf_provenance.yml`、`sc_coverage.yml`、`scaffold.yml`、`pedagogy_audit.yml`、`pedagogy_audit_draft.yml`（內容層 selftest 的 fixture）。
- `video/_audit/design-template-system/`（整夾）、`video/_audit/REVIEW-pipeline-assessment-2026-09-07.html`、`video/_audit/REVIEW-transition-ab.html`、`video/_audit/REVIEW-worked-example-template-applied.html`

**文檔（Task 2 擁有）**

- `video/DESIGN.md`（搬走後另寫新版，見 §4 Task 2）
- `video/CODE2VIDEO_STUDY.md`
- `video/KICKOFF-motion-primitives.md`、`KICKOFF-motion-language-gaps.md`、`KICKOFF-motion-language-rollout.md`、`KICKOFF-shared-layer-v1.md`、`KICKOFF-worked-example-template.md`、`KICKOFF-toolline-backlog-r1.md`、`KICKOFF-toolline-backlog-r2.md`、`KICKOFF-pipeline-hardening.md`、`KICKOFF-round17-dispatch.md`、`KICKOFF-s31-amplify.md`
- `video/content_scripts/_audit/HOOK-ENGINEERING-RUBRIC.md`、`video/content_scripts/_audit/PLAN-routeA-plex-latex.md`

### 3.2 留在 `video/`（不動路徑）

- **共用層（Remotion 在用）**：`pipeline/tts.py`、`scene_align.py`、`scene_fallback.py`、`narration.py`、`audio.py`、`timing.py`、`atomicio.py`、`derived_check.py`、`derive_spoken.py`、`template_names.py`、`_bootstrap.py`（精簡版）、`_regression_scene_align.py`、全部 `tts_*.py`（8 支）、`mimo_preview.py`、`captions.py`、`pauses.py`、`stillness.py`、`rewatch_pack.py`、`house_audio.py`、`listening_pack.py`、`loudness_ab.py`、**新增 `loudnorm.py`**、`run_selftests.py`、`pipeline/assets/`（品牌 logo＝Remotion 唯一固定元素＋house audio cue）
- **內容層檢查器**：`provenance.py`、`pedagogy.py`、`step_coverage.py`、`example_coverage.py`、`source_rev.py`、`review_pack.py`、`_screen_contract.py`、`narration_review.py`
- **內容層**：`content_scripts/`（全部，含 `_audit/` 的 rubric／PROMPT／REPORT／REVIEW／`_gen/`，只搬走 §3.1 列的兩份）、`storyboards/_fixtures/` 的五支內容層 fixture
- **實驗線**：`experiments/remotion_styles/`、`remotion_pilot/`、`tts_workflow/`、`reference_frames/`、`forced_alignment_dean/`
- **文檔**：`README.md`（改寫）、`REBUILD_STATUS.md`（改寫）、`REVIEW_GATES.md`（改寫）、`REVIEW_MODEL_DECISIONS.md`、`RUNBOOK-mimo-narration-route.md`（改寫）、`CONTENT_METHODOLOGY.md`（微改）、`SPEC-motion-language.md`（改指標）、`SPEC-pedagogy-firstlearner-{framework,expansion}.md`、`PROPOSAL-scope-packaging-coverage.md`、`KICKOFF-process-reform.md`（加註）、`KICKOFF-s32-chain-rule.md`（加註 Phase B 作廢）、本檔
- `_audit/`：其餘全部（TTS 試聽頁、loudness A/B、code review 2026-09-23 等）
- `_archive/`、`requirements.txt`（改內容）

### 3.3 直接刪除

- `.claude/agents/hook-engineering-audit.md`（審 Manim hook code；rubric 已入 legacy）
- 本機：`video/media/`（Tex 快取）、`video/.git`（空目錄殘留）、兩個已併入 main 的 locked worktree（`.claude/worktrees/agent-a2e1af99bff46677c`、`agent-a4355a6273de952b0`）與其分支

## 4. 三個並行 task（各自 worktree、一 task 一 commit、主對話 merge＋審核）

**共同紀律**：worktree 開分支後先 `git merge main`；只動自己那欄的檔；commit subject ≤70 字、body 繁中逐條（改了什麼、為何、證據）、結尾 `Co-Authored-By`；回報＝改了哪些檔、驗收數字、沒做到的條款。**全程離線零計費。** 不動 `video/output/`、不動 `experiments/remotion_styles/paper/` 除下列指定檔。

### Task 1 — 引擎搬移（opus）

改：§3.1「程式」全部 `git mv`；新增 `video/pipeline/loudnorm.py`（從 `make.py` 抽出 `HOUSE_LUFS`、`_loudnorm_final` 與其直接依賴的 helper；legacy 的 `make.py` 保持原樣自洽）；`video/experiments/remotion_styles/paper/scripts/loudnorm.py` 改 import 新模組；`video/pipeline/_bootstrap.py` 精簡（拿掉 `apply_tex_template` 與 manim 相關 docstring，保留 `bootstrap()` 的 sys.path 邏輯與 `section_output_dir`）；`_selftest_make_loudnorm.py` → `_selftest_loudnorm.py`；`_selftest_pauses.py` 拆 (c)；新增 `legacy/manim_video/README.md`（繁中：是什麼、為何、tag 回退、逐項對照表「從→到」含 §3.1 文檔那欄、什麼留在 `video/` 與為何）；`legacy/README.md` 加 gen-2 一節並更新開頭。

驗收：
1. `.venv\Scripts\python video\pipeline\run_selftests.py` 剩下的 selftest **全綠**，回報「N 支／N 綠」與耗時。
2. `.venv\Scripts\python -c "import sys; sys.path.insert(0,'video'); import pipeline.tts, pipeline.scene_align, pipeline.derive_spoken, pipeline.provenance, pipeline.pedagogy, pipeline.loudnorm, pipeline.rewatch_pack, pipeline.captions"` 無錯。
3. `cd video/experiments/remotion_styles/paper && python scripts/loudnorm.py --help`（或等價的 import 檢查）證明 loudnorm 仍可用。
4. `git grep -n "import manim\|from manim" -- video/` **零命中**（`video/_archive/scratch/` 除外）。
5. `python video/pipeline/tts.py --help` 正常。
6. `git status` 乾淨、`git log --follow legacy/manim_video/make.py` 能追到舊歷史。

不准動：`video/*.md`（Task 2）、`tools/`、`ENVIRONMENT.md`、`requirements.lock`、`.claude/agents/`（Task 3）。

### Task 2 — 文檔（opus）

改：§3.1「文檔」全部 `git mv`；新寫精簡 `video/DESIGN.md`（承接節見 §1.2；每節開頭註明「承自 legacy/manim_video/DESIGN.md §…」）；改寫 `video/README.md`（開頭、結構樹＝§3.2 的實況、狀態、指令；拿掉 make.py／Manim 路線，Remotion 重現指令指向 `experiments/remotion_styles/README.md`）；`REBUILD_STATUS.md`「現役路線」頂部加 2026-09-28 拍板條目（指向本檔＋tag）、各節狀態表加註 §3.1 Manim 成片＝封存、§3.2 Phase A 有效／Phase B 作廢待 Remotion 版；`REVIEW_GATES.md` 層 5（manim hook code）退役、層 6／7 中 schema／lint／sizecheck／critic／`[sync]` 等 Manim 閘標退役、七份 rubric → 六份、§六 G4 開工清單去 Manim 項；`RUNBOOK-mimo-narration-route.md` 去 `make.py` 步驟；`KICKOFF-s32-chain-rule.md` 頂部加註（Phase A 成果有效、Phase B 作廢、Remotion 版另開）；`KICKOFF-process-reform.md` 頂部加註；`SPEC-motion-language.md` 實作契約層指標改指 legacy；`CONTENT_METHODOLOGY.md` §5 的「Claude 依 `animation_cue` 生成 manim code／hook-engineering-audit」改為 Remotion 場景 code、稽核閘待定；根 `README.md`（產線描述、文檔索引表、`legacy/` 段落）、根 `CLAUDE.md`（產線一覽表、常用指令去 `make.py`、「影片渲染解析度」改 Remotion 1080p、付費 API 段的「本地 Manim render」改「本地 Remotion render」、任務分派段不動）、`CONTENT_SPEC.md` 第 44–45 行。

驗收：
1. `git grep -n -i "manim" -- video/*.md README.md CLAUDE.md CONTENT_SPEC.md` 的每一處命中都是**歷史敘述或指向 legacy 的連結**，沒有一處把 Manim 寫成現役；逐條列在回報裡。
2. `python tools/doc_lint.py`（若存在且適用）綠；所有新增／改動的相對連結用腳本逐條檢查目標存在（含指到 `legacy/manim_video/…` 的，**依 §3.1 清單推定路徑**，Task 1 尚未合併時允許暫時不存在，但要列出）。
3. 新 `video/DESIGN.md` 不含任何 Manim 模板／Lectern／容量契約內文。
4. `git status` 乾淨。

不准動：`legacy/README.md`（Task 1）、`ENVIRONMENT.md`（Task 3）、任何 `.py`／`.yml`。

### Task 3 — 環境層（opus）

改：`tools/doctor.py`（拿掉 manim／ManimPango critical 檢查、manim Tex 編譯 smoke、Instrument Sans vendored fonts 區、`--smoke` 裡對 schema／lint 的呼叫；MiKTeX 檢查保留但說明改為講義線；Node ≥21 說明加上 Remotion；新增一條 WARN：`video/experiments/remotion_styles/paper/node_modules` 不存在時提示 `npm ci`）；`tools/setup.ps1`（拿掉第 4 步 Instrument Sans MiKTeX 註冊；標頭註解同步）；`requirements.lock`（拆掉 manim 及**只被 manim 一族依賴**的傳遞套件——每一個刪除都要用 `.venv\Scripts\python -m pip show <pkg>` 的 `Required-by` 鏈證明根在 manim；TTS／對齊路線用的 numpy／torch／whisper／stable-ts 等一律不動）；`video/requirements.txt`（去 manim 行、更新註解）；`ENVIRONMENT.md`（①／①b／③ 改寫：manim 退場、MiKTeX 改講義線專用、Instrument Sans 註冊步驟退役；④ Node 段加 Remotion 為影片線正式依賴；本機驗證版本列表去 manim）；刪 `.claude/agents/hook-engineering-audit.md`；改 `.claude/agents/visual-frame-audit.md`（抽幀來源從 `critic.py --dry-run` 改為 `pipeline/rewatch_pack.py` 的 contact sheet 或 ffmpeg 抽幀；rubric 路徑不變）。

驗收：
1. `.venv\Scripts\python tools\doctor.py` 跑完，回報每一列狀態；不得有因本次改動新增的 FAIL。
2. lock 的每個刪除項附 `Required-by` 鏈；**最強證明**＝scratchpad 建乾淨 venv `pip install -r requirements.lock` 成功；若 torch 等太重，改用 `pip install --dry-run -r requirements.lock` 的 resolver 結果。
3. `git grep -n -i "manim" -- tools/ ENVIRONMENT.md requirements.lock video/requirements.txt .claude/agents/` 每一處命中都是歷史敘述；逐條列出。
4. `git status` 乾淨。

不准動：`video/**`（除 `video/requirements.txt`）、`legacy/**`、`CLAUDE.md`、`README.md`。若發現 `CLAUDE.md` 需要配套改動，寫進回報，不要動手。

## 5. 收案紀錄（2026-09-28，主對話 merge＋審核）

三個 task 各一個 opus 子代理、各自 worktree、各一個 commit，依 Task 1 → Task 3 → Task 2 併入 main：

| Task | 子代理 commit | merge commit | 實際結果 |
|---|---|---|---|
| 1 引擎搬移 | `01c757c` | `c7e0d34` | `git mv` 182 檔；新增 `pipeline/loudnorm.py`（自 `make.py` 逐字抽出 5 個定義）、`_selftest_loudnorm.py`；`_bootstrap.py` 精簡；`legacy/manim_video/README.md`＋`legacy/README.md` gen-2 節。selftest **83 → 24 支全綠（約 10 秒）**；共用層 import 不載入 manim；`paper/scripts/loudnorm.py` 對合成測試片實跑 I=−19.0 LUFS |
| 3 環境層 | `e0095e0` | `d0b0514` | `requirements.lock` **38 → 7 套**（31 項 `Required-by` 鏈全根在 manim，表在該 commit body；乾淨 venv 實裝＋`pip check` 通過）；doctor 去 manim／字型／Tex smoke，加 Remotion `node_modules` WARN；setup.ps1 去 Instrument Sans 註冊；ENVIRONMENT.md ①／①b／③／④ 改寫；刪 `hook-engineering-audit` agent、改 `visual-frame-audit` 抽幀來源 |
| 2 文檔 | `6af9f53` | `e94d3ab` | `git mv` 14 份文檔；新 `video/DESIGN.md`（約 29 KB，四塊承接）；改寫 README／REBUILD_STATUS／REVIEW_GATES／RUNBOOK／KICKOFF 頂註／SPEC-motion-language／CONTENT_METHODOLOGY／根 README／CLAUDE.md／CONTENT_SPEC，另修 `content_scripts/_audit/` 等 14 處連結 |

merge 後在 main 上重驗：`run_selftests.py` 24／24 綠、`tools/doc_lint.py` clean、`git grep "import manim" -- 'video/*.py'` 只剩 `_archive/scratch/`（既有歷史夾）與 `experiments/forced_alignment_dean/render_aligned_scene.py`（見例外 ②）。
主對話收尾 commit：`review_pack.py` 的 rubric 預設路徑改指 legacy、`experiments/remotion_styles/README.md` 的「沿用 `make.py` 的 loudnorm」改指 `pipeline/loudnorm.py`、REBUILD_STATUS 補收案數字。

**主對話裁決的例外（偏離 §3／§4 字面，均接受）：**

1. **四支 selftest 只拆函式、不整檔搬**（`_selftest_{coverage,pedagogy,provenance}.py` 的 `test_schema_integration`、`_selftest_scene_align_integration.py` 的 make 依賴測試→ legacy 各成獨立檔）。理由：整檔搬會讓 §2 要留下的內容層檢查器在 `video/` 沒有任何測試，§3.2 保留的 fixture 也沒人用。
2. **`experiments/forced_alignment_dean/render_aligned_scene.py` 仍 import manim。** 依 §2「已結案實驗夾原地不動」，此檔自此無法執行；它是 scene-level FA 路線的歷史起源，留作紀錄。Task 1 驗收 4 的「零命中」以此為唯一例外。
3. **doctor 多刪了 plex-mono／lmodern／microtype 與 dvisvgm／dvipng 檢查。** 前四者只服務 Manim Tex；`microtype` 講義線也用，但 MiKTeX 首編自動補裝，且原檢查只是 WARN，接受。
4. **`video/requirements.txt` 首行加 `# -*- coding: utf-8 -*-`**（修既有 bug：繁中 Windows 上 pip 用 cp950 讀含中文註解的檔會 UnicodeDecodeError）；另補列 numpy、pillow（`rewatch_pack.py` 直接 import，原由 manim 間接帶入）。
5. Task 3 順手改了 `handout/PIPELINE.md` 的 subagent 清單（去 hook-engineering-audit、補漏列的 motion-designer）與 doctor／ENVIRONMENT 裡提到 `make.py`／`critic.py` 的過期文字；Task 2 順手修了 `authoring/seed_converge/README.md`、`pipeline/assets/audio/house/README.md` 的連結。皆為零行為改變的文字修正。

**既有、非本輪造成的問題（留紀錄）：** `doctor.py` 在本機 Git Bash 下報 `pdftotext 不是 poppler 版`——Git for Windows 的 xpdf 版排在 MiKTeX 前面，用 tag 上的舊 doctor 跑結果相同，修法早在 ENVIRONMENT.md ③b（2026-07-27）。

**本機清理（不進 git）：** 刪 `video/media/`（Tex 快取 55 MB）、空目錄 `video/.git`、兩個已併入 main 的 locked 舊 worktree（`agent-a2e1af99bff46677c`、`agent-a4355a6273de952b0`）及其分支、一個未登記的 9-14 殘留夾（`agent-ac4d8696b5d83aebb`，只剩 pipeline 複本與 Tex 快取）。`video/output/`（含付費 TTS 原音）**未動**；`.deps_voiceover/` 本機不存在。

**tag `archive/2026-09-28-manim-gen2-final` 仍只在本機**，要帶到其他電腦：`git push origin archive/2026-09-28-manim-gen2-final`。

## 6. 另開的後續（不在本輪）

1. **已完成（2026-09-28）**：`experiments/remotion_styles/paper/` 升格為正式目錄 `video/remotion/`（目錄名由使用者確認；純 `git mv`＝commit `cffc8bf`，路徑引用全面更新、`remotion/scripts/loudnorm.py` 的 sys.path、`tools/doctor.py`／`ENVIRONMENT.md`／根 `CLAUDE.md`／根 `README.md`／`.claude/agents/motion-designer.md` 同步＝其後一個 commit）。`blueprint/`、`dark_glow/` 與風格探索紀錄留在 `experiments/remotion_styles/`；本機 gitignored 的 `out/`、`public/audio/`、`node_modules/` 以檔案系統一併搬到新目錄。本檔 §1.4／§4／§5 的 `experiments/remotion_styles/paper/` 為當日歷史敘述，不改。
2. ✅ **已完成（2026-09-28）**：§3.2 Phase B 的 Remotion 版 KICKOFF＝[`KICKOFF-s32-remotion-phaseB.md`](KICKOFF-s32-remotion-phaseB.md)（Phase A 產物→`s32.yml` 的派生規則、沿用／退役閘表與三個新確定性檢查、motion-designer 派工形狀、成本欄位；另記 Phase A 音檔本機遺失的事實，重對映／重配音待使用者裁決）。
3. ✅ **已完成（2026-09-28 晚，獨立輪次）**：內容層確定性檢查器（provenance／pedagogy／coverage）接 Remotion storyboard yml 的 schema——
   SPEC＝[`SPEC-remotion-storyboard-schema.md`](SPEC-remotion-storyboard-schema.md)、入口＝[`pipeline/check_storyboard.py`](pipeline/check_storyboard.py)
   （結構驗證＋串 provenance／source_rev／pedagogy／step_coverage／example_coverage；`tools/doctor.py --smoke` 重掛為對 `remotion/*/*.yml` 全跑）；
   對現行四支分鏡的實跑結果記在 [`REVIEW_GATES.md`](REVIEW_GATES.md) 層 6 新列；待裁決項（場級 `ref:` 缺失 WARN／ERROR、PD2 的 Remotion 場角色欄）見 SPEC §6。
4. `.claude/launch.json` 的 `remotion-review` 條目指向舊 session 的 scratchpad 路徑，需修。
