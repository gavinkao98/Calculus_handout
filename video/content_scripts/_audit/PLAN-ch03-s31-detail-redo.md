# §3.1 影片「最大詳細」全重做 — 實作計畫（Implementation Plan）

> **For agentic workers:** REQUIRED SUB-SKILL：用 `superpowers:subagent-driven-development`（建議）或 `superpowers:executing-plans` 逐 task 執行。步驟用 `- [ ]` 追蹤。
> **驗證模型（本產線特性，非 pytest）：** 此管線不靠單元測試，靠 **免費 gate-1 稽核 subagent（六鏡／copyedit／視覺幀）＋確定性腳本（schema／lint／sizecheck）＋離線抽幀目視＋使用者 sign-off**。每個會動內容/視覺的 task 以「編 HTML→讀／跑稽核」或「render→看圖／跑三閘」為驗證點。
> **計費紀律（CLAUDE.md）：** 全程離線／免費。任何計費呼叫（MiMo TTS、Codex gate-2、VLM critic gate-2）一律先停下、報價、徵同意——本計畫**不含**任何計費步驟。

**Goal:** 把 §3.1 影片內容稿用「最大詳細、最少省略」重新拆寫（第1檔基準＋核心加第2檔），到 mock render ＋ 視覺稽核 blocking==0，達成與方法論「detail over compression」合規。

**Architecture:** 兩階段。**Stage 1（內容）** 重拆 `content_scripts/ch03_trig_derivatives.md`（SSOT）→ 編審核 HTML → 六鏡＋copyedit → 使用者 sign-off → LOCK。**Stage 2（工程）** 重模板化 storyboard、調 hook → schema/lint/sizecheck → mock render → 視覺幀稽核 → HTML 報告。權威規格見 [`SPEC-ch03-s31-detail-redo.md`](SPEC-ch03-s31-detail-redo.md)。

**Tech Stack:** manim 0.20.1（Route A：Plex Sans/Mono＋Latin Modern；pdflatex→dvi→dvisvgm）；`make.py`（mock backend）；gate-1 稽核走 `.claude/agents/` 具名 subagent ＋ 六鏡 multi-agent Workflow。

**關鍵路徑（已驗 CLI）：**
- storyboard：`video/storyboards/ch03_trig_derivatives.yml`
- 內容稿：`video/content_scripts/ch03_trig_derivatives.md`（SSOT）／審核稿 `..._narration.html`
- 忠實來源：`handout/fragments/ch03/sec-3-1.html`
- schema：`python video/pipeline/schema.py <yml> --list`／lint：`python video/pipeline/lint.py <yml>`／sizecheck：`python video/pipeline/sizecheck.py <yml>`
- 單景 mock：`python video/make.py --storyboard <yml> --scene <id> --backend mock --quality low`
- 全片 mock 1080p：`python video/make.py --storyboard <yml> --scene all --backend mock --quality high`
- 抽幀（零計費）：`python video/pipeline/critic.py --storyboard <yml> --dry-run`

---

## File Structure（會建/動到的）

- **動** `video/content_scripts/ch03_trig_derivatives.md` — Stage 1 內容稿重拆（外科式重寫，非覆蓋重生）。
- **動** `video/content_scripts/ch03_trig_derivatives_narration.html` — 重編審核稿。
- **動** `video/storyboards/ch03_trig_derivatives.yml` — Stage 2 重模板化（拆場、`part:`、reveal 對齊）。
- **動** `video/animations/ch03_trig_derivatives_hooks.py` — 調 3 hook；若採用 `chord_le_arc` 則加第 4。
- **動** `video/DESIGN.md` — 加一行防漂移護欄（§6/Task 14）。
- **建** `video/content_scripts/_audit/REVIEW-ch03-s31-detail-redo-applied.html` — 完成 HTML 報告。
- **動** `video/REBUILD_STATUS.md` — 進度錨。
- **不動** `video/pipeline/templates/`（缺視覺走 hook；預設不動模板——Karpathy §3）。

---

## Stage 1 — 內容稿重拆

### Task 0 — 前置與基線就位
**Files:** 讀 only。
- [ ] 確認分支 `video/template-redesign-navy-spine`、工作樹狀態：`git status`。
- [ ] 讀基線：現有 `ch03_trig_derivatives.md`、`handout/fragments/ch03/sec-3-1.html`、`REVIEW-ch03-s31-density-audit.html`、`SPEC-ch03-s31-detail-redo.md`。
- [ ] 環境：`python tools/doctor.py`（fonts 段綠：plex-sans/plex-mono/lmodern）。
- **驗證點：** 基線可讀、doctor 全綠、SPEC §3 場景藍圖在手。

### Task 1 — 重拆 Stage-1 段（why_trig_is_different、difference_quotient_for_sine）
**Files:** Modify `ch03_trig_derivatives.md`
- [ ] `why_trig_is_different`：保留課本 sum-to-product 路線、funnels to `lim sinθ/θ`（0/0）；加一個 beat 把 0/0 障礙講生動（**不引入 angle-addition 新路線**）。
- [ ] `difference_quotient_for_sine`（**第2檔**）：sum-to-product → 分子 → 除以 h（顯示 `h=2·h/2`）→ 兩因子形 → 點名兩因子各需「連續」「基本極限」；加 `lim_{h→0}` framing ＋「整個導數掛在兩件事上」直覺 beat。每步一 `{show}` 對齊位。
- **驗證點：** 通讀兩段 narration 像「說出來的課」、未犯方法論 §4 禁則（不念標題/不報節號/不用 see/as shown）；difference_quotient 的每個承載步驟都有對應顯示位。

### Task 2 — 重拆 Stage-2 段（幾何擠壓 + continuity 旗艦改造）
**Files:** Modify `ch03_trig_derivatives.md`
- [ ] `sector_inequality`（**第2檔**）：維持圖的教學意圖；偶函數論證獨立 beat；三面積嵌套逐步 build。
- [ ] **(可選新增)** `chord_le_arc`（**第2檔 mini-visual**）：單位圓「弦 ≤ 弧」示 `|sinθ|≤|θ|`，寫 `visual_need`／`animation_cue`；若併入 sector hook 則就近註明不獨立。
- [ ] `squeeze_to_the_bound`（**第2檔**）：每步成 beat——×2 → `sinθ≤θ≤tanθ` → ÷sinθ＋`tan=sin/cos` → 取倒數翻向 → `cosθ≤sinθ/θ≤1`；附帶 `0≤|sinθ|≤|θ|`。
- [ ] **`continuity_of_sin_cos` 拆 2 單元（旗艦改造）：**
  - `continuity_statement_sin_limit`（statement 場）：陳述 sin、cos 處處連續 ＋ 由界＋squeeze 得 `lim_{θ→0} sinθ=0`；開場第2檔直覺「連續＝角度動一點、sin/cos 也只動一點」。
  - `continuity_argument`（proof 場）：**顯示**和差化積兩條恆等式（cos、sin）→「中間因子 ≤1」→ 界 `|Δcos|,|Δsin| ≤ 2|sin((x−x₀)/2)|` → `x→x₀ ⟹ RHS→0` → squeeze ⟹ 連續 ∎。
- [ ] `fundamental_limit`（**第2檔**）：statement ＋ `cosθ≤sinθ/θ≤1` ＋ `cosθ→1`（連續）＋ 偶⟹兩側；每步成 beat ＋ 直覺扣回擠壓圖。
- [ ] `limit_not_identity`、`radians_essential`：維持（callout 本就輕），僅一致性微調。
- **驗證點：** continuity proof 場的界 `2|sin((x−x₀)/2)|` 有**可見來源**（和差化積那兩行）——修掉密度稽核唯一真缺口；每個 def/thm/prop 有單元覆蓋；散文 fold/promote 無 silently drop。

### Task 3 — 重拆 Stage-3 段（derivative_of_sine/cosine、slope、cycle）
**Files:** Modify `ch03_trig_derivatives.md`
- [ ] `derivative_of_sine`（**第1檔補回**）：顯示 `lim_{h→0}`(差分商) = `lim cos(x+h/2)·sin(h/2)/(h/2)` → `cos x·1 = cos x`，兩極限事實各引用（連續、基本極限）；補上前版省掉的 setup 行。
- [ ] `derivative_of_cosine`（**第1檔補回**）：repeat-pattern 省 setup，但**顯示伴隨恆等式** `cos A−cos B = −2 sin((A+B)/2) sin((A−B)/2)`，再走鏡像論證。
- [ ] `slope_equals_height`：維持。
- [ ] `derivative_cycle`：強化 `e^x` 一步 vs 四步循環呼應 beat（忠實 Remark 3.1）。
- **驗證點：** Thm 3.1/3.2 各有單元；sin′ 場顯示 `lim_{h→0}` setup、cos′ 場顯示伴隨恆等式；repeat-pattern 落實。

### Task 4 — 重拆 Stage-4 段（companion、all-six、shm、forward、recap）
**Files:** Modify `ch03_trig_derivatives.md`
- [ ] `companion_limit`（Ex 3.1）：每步成 beat（已忠實，確保逐步顯示）。
- [ ] `all_six_trig_derivatives`（Ex 3.2，**第1檔補回**）：**全保留**（D3）；顯示 sec′ 的商法則步驟（前版只給結果）；視容量就近註明是否拆 `tan′/sec′`（worked）與 `cot′/csc′`（stated）兩單元。
- [ ] `shm_compute`（Ex 3.3）：維持（已乾淨）。
- [ ] `toward_the_chain_rule`：維持（**MUST NOT 報節號**）。
- [ ] `recap`：takeaway 對齊加詳後的四支柱。
- **驗證點：** 三個例題模式全保留；sec′ 步驟顯示；recap 有 takeaway；折疊掉的同型就近註明。

### Task 5 — 重編 narration HTML 審核稿 ＋ 通讀
**Files:** Modify `ch03_trig_derivatives_narration.html`
- [ ] 由 `.md` 重編 standalone HTML（MathJax/KaTeX CDN、逐單元 narration＋可展開 learning_goal/visual_need/animation_cue）。
- [ ] 瀏覽器開啟，確認數學渲染正確、與 `.md` 逐字一致。
- [ ] **通讀整份 narration**：任何一段像教科書 → 就地重寫。
- **驗證點：** HTML 雙擊即開、數學即渲染、與 `.md` narration 一致。

### Task 6 — 六鏡對抗式稽核（gate-1，免費 Workflow）→ blocking==0
**Files:** Modify `.md`（依裁決）；稽核紀錄入 `_audit/`。
- [ ] 跑六鏡 multi-agent Workflow（SSOT `content_scripts/_audit/CONTENT-SIXLENS-RUBRIC.md`）：L1 忠實／L2 拆解／L3 語域／L4 不重複／**L5 數學正確（每個證明/例題隔離盲算）**／L6 完整；refute-by-default、四級分級、逐條複驗。
- [ ] 對每條 blocking 外科式修 `.md`，**回歸再審**改動項（CLAUDE.md meta-rule），重編 HTML。
- **驗證點／收斂線：** 六鏡 **blocking==0**（advisory 逐筆人裁）；L5 對 §3.1 尤關鍵（弧度/偶函數/squeeze/商法則/和差化積易錯）。

### Task 7 — 散文 copyedit pass（gate-1，免費）→ tighten
**Files:** Modify `.md`（lock 前唯一改措辭窗口）。
- [ ] 跑 `narration-copyedit` subagent（SSOT `NARRATION-COPYEDIT-RUBRIC.md`）：C1–C5 贅字／冗餘／朗讀流暢／句長／跨單元回音。硬護欄：語義不得改。
- [ ] 採納 tighten、重編 HTML。
- **驗證點：** 冗餘/贅字在 lock 前清掉。

### Task 8 — 使用者 sign-off ＋ 鎖稿 ＋ commit Stage 1
**Files:** Modify `.md`（DRAFT→LOCKED）；commit。
- [ ] 交付 `_narration.html` 給使用者審核旁白。**等使用者明確認可**（不可自行宣告）。
- [ ] 認可後 `.md` 檔頭階段標記改 LOCKED、設 `CONTENT_APPROVED`。
- [ ] commit Stage 1：`SPEC-…md` ＋ `PLAN-…md` ＋ `.md` ＋ `_narration.html` ＋ `REVIEW-ch03-s31-density-audit.html` ＋ 六鏡/copyedit 裁決紀錄。
- **驗證點：** 使用者書面認可；source 自此凍結（後續唯讀）。

---

## Stage 2 — 工程

### Task 9 — storyboard 重模板化（拆場、`part:`、reveal 對齊）
**Files:** Modify `ch03_trig_derivatives.yml`
- [ ] 把新內容稿模板化：填/改 `template`／`accent`／`say`（內嵌 `{show ...}` 對齊新 narration）／payload。continuity 拆兩場、長場視 sizecheck 加 `part: {current,total}`、每頁重貼 header。
- [ ] divider/intro/outro 的 progress 與計數若因拆場改變則同步。
- **驗證點：** `python video/pipeline/schema.py video/storyboards/ch03_trig_derivatives.yml --list` 無 error、所有 `{show}` 目標 resolve、無 stale marker。

### Task 10 — 客製 hook 調整（含 `chord_le_arc` 若採用）
**Files:** Modify `ch03_trig_derivatives_hooks.py`；Modify storyboard。
- [ ] 既有 3 hook（`sector_inequality`／`slope_equals_height`／`shm_stacked_graphs`）隨新 reveal id／beat 調整。
- [ ] 若採用 `chord_le_arc`：依 `animation_cue` 生成 manim code（單位圓弦≤弧），緊迴路修補（局部→hook 函式→整支重生，方法論 §5）。
- [ ] 單景 mock render 驗每個改動 hook：`python video/make.py --storyboard <yml> --scene <id> --backend mock --quality low`。
- **驗證點：** 改動 hook 單景 render EXIT 0；抽幀目視端態數學對、reveal 對齊。

### Task 11 — 三閘全過（schema / lint / sizecheck）
**Files:** Modify storyboard（修閘報問題）。
- [ ] schema / lint / sizecheck 各跑。
- [ ] sizecheck 的「拆 ~N 頁」warn 逐筆判——作為拆場/`part:` 依據（不靠縮字救）。
- **驗證點：** schema/lint **0 error**；sizecheck 0 error（within-frame advisory warn 逐筆記錄）。

### Task 12 — 全片 mock render（1080p）
**Files:** 產 `video/output/...`（gitignore、可重生）。
- [ ] `python video/make.py --storyboard <yml> --scene all --backend mock --quality high`。
- [ ] REBUILD_STATUS 教訓：render 與 sizecheck/critic 不同時跑（Tex-cache race）；transient flake 刪 0-byte 快取＋retry。
- **驗證點：** 三閘過 → 全場 render → compose → mp4（h264 1080p）；hook 端態數學全對、零 runtime 錯。

### Task 13 — 視覺幀稽核（gate-1 visual-frame-audit，免費）→ blocking==0
**Files:** Modify storyboard/hooks（依裁決）。
- [ ] 抽幀：`python video/pipeline/critic.py --storyboard <yml> --dry-run`。
- [ ] 每場跑 `visual-frame-audit` subagent（SSOT `VISUAL-FRAME-RUBRIC.md`）：V1–V8 blocking ＋ A1–A7 magnitude。可用 Workflow 並行、refute-by-default。
- [ ] 修 blocking → 重渲改動場 → 回歸再審。
- **驗證點／收斂線：** 視覺 **blocking==0**；advisory 逐筆記錄。

### Task 14 — 防漂移護欄加到 DESIGN.md
**Files:** Modify `video/DESIGN.md`
- [ ] 在 §「Authoring checklist——反覆出現的錯誤」表加一行：
  > **Don't** 在低填充幀只放證明骨架／把 >4 步證明壓成 2–3 行 ｜ **Do** proof >4 步拆 statement＋proof 場、超頁走 `part:`、一步一 beat ｜ **原因** detail over compression（CONTENT_METHODOLOGY §1）；ch03 §3.1 第一版壓縮漂移學費（2026-06-29 密度稽核）。
- **驗證點：** 該行格式與既有表一致；指向的 SSOT 連結正確。

### Task 15 — HTML 報告 ＋ 進度錨 ＋ commit Stage 2
**Files:** Create `REVIEW-ch03-s31-detail-redo-applied.html`；Modify `REBUILD_STATUS.md`。
- [ ] 產 self-contained HTML 報告（base64 內嵌新關鍵幀＋逐單元旁白＋六鏡/copyedit/視覺閘裁決＋與前版對照），比照 `REVIEW-ch03-s31-density-audit.html`。
- [ ] `REBUILD_STATUS.md` 新增一節記 §3.1 詳細重做（密度標準、continuity 拆場、護欄、各閘收斂）。
- [ ] commit Stage 2（storyboard＋hooks＋DESIGN 護欄＋報告＋status）。
- **驗證點：** 報告雙擊即開、數學即渲染；REBUILD_STATUS 對得上；working tree 乾淨。

---

## 收斂定義（「做完＝與方法論合規」）

內容稿 LOCKED（六鏡＋copyedit blocking==0、使用者 sign-off）＋ storyboard 三閘 0 error ＋ 全片 mock render 成功 ＋ visual-frame-audit blocking==0 ＋ DESIGN.md 護欄行已加 ＋ HTML 報告與 REBUILD_STATUS 就位。

## 計費閘（deferred — 達 mock 里程碑後、各自報價徵同意才跑）

- spoken derive ＋ NFA（MiMo 路線，TTS 延後故一併延後）。
- MiMo TTS 合成（計費）；Codex gate-2（計費）；VLM critic gate-2（需同意）。
