# §3.1 三角函數導數 影片 實作計畫（ch03 · Derivatives of Sine and Cosine）

> **For agentic workers:** REQUIRED SUB-SKILL — 用 `superpowers:subagent-driven-development`（建議）或 `superpowers:executing-plans` 逐 task 執行。步驟用 `- [ ]` 追蹤。
> **驗證模型（本產線特性，非 pytest）：** 此管線不靠單元測試，靠 **離線抽幀（`scratch_frames.py` / `critic.py --dry-run`，零計費）＋目視＋確定性腳本（`schema`/`lint`/`sizecheck`）＋gate-1 稽核 subagent（免費）**。每個會動內容/視覺的 task 以「編 HTML→讀／跑稽核」或「render→看圖／跑 schema+lint+sizecheck」為驗證點。
> **計費紀律（CLAUDE.md）：** 全程離線／免費。任何計費呼叫（Codex gate-2、MiMo TTS、VLM critic gate-2）一律先停下、報價、徵使用者同意——本計畫**不含**任何計費步驟（見文末「計費閘（deferred）」）。

**Goal:** 把講義 §3.1〈Derivatives of the Sine and Cosine Functions〉做成一支與 §1.1 同級的 mock 教學影片（1080p、靜音/mock TTS），到 **mock render + 視覺稽核 blocking==0** 為止。

**Architecture:** 兩階段。**Stage 1（內容）**＝依 `CONTENT_METHODOLOGY.md` 從講義拆教學單元、寫 `content_scripts/ch03_trig_derivatives.md`（source of truth）→ 編 `_narration.html` → 六鏡＋copyedit gate-1 → 使用者 sign-off 鎖稿。**Stage 2（工程）**＝把內容稿模板化成 `storyboards/ch03_trig_derivatives.yml`、為 Fig 3.1/3.3/3.4 生成 3 個客製 manim hook → `schema/lint/sizecheck` → mock render → visual-frame-audit gate-1 → HTML 報告。

**Tech Stack:** manim 0.20.1（Route A：全 LaTeX 文字＝IBM Plex Sans/Mono、Latin Modern 數學；pdflatex→dvi→dvisvgm）；`make.py`（mock backend、本地 render）；gate-1 稽核走 `.claude/agents/` 具名 subagent ＋ 六鏡 multi-agent Workflow。

---

## 開工前必讀：現況與脈絡（新對話零脈絡也能照做）

- **倉庫：** `C:\Users\Kao\Downloads\Calculus_handout`。影片產線在 `video/`。**分支：續用 `video/template-redesign-navy-spine`**（Route A Plex+LaTeX 最新模板，render 時自動套，**不另開分支**）。
- **講義輸入源（權威、忠實對象）：** [`handout/fragments/ch03/sec-3-1.html`](../../../handout/fragments/ch03/sec-3-1.html)。檔頭含本節的編號契約（Prop 3.1/3.2、Thm 3.1/3.2、Ex 3.1/3.2/3.3、Fig 3.1–3.4、Remark 3.1、兩個未編號 Caution）與 ③ 決策 D1–D4。
- **跑 manim 的方式：** deps 在 repo 根 `.deps_voiceover`（manim 0.20.1）、`.deps`（PyYAML）；`video/pipeline/_bootstrap.bootstrap()` 會把它們上 `sys.path` 並設 TeX template（每景重套，見 REBUILD_STATUS「tempconfig 坑」）。環境檢查：`python tools/doctor.py` 應全綠（manim／MiKTeX `plex-sans`/`plex-mono`/`lmodern`／ffmpeg）。
- **確切指令（已驗 CLI）：**
  - 結構驗證＋列舉 reveal 目標：`python video/pipeline/schema.py <yml> --list`
  - 文字 garble lint：`python video/pipeline/lint.py <yml>`
  - 字級/出框 sizecheck：`python video/pipeline/sizecheck.py <yml>`
  - 離線抽「最滿幀」目視（零計費）：`python video/scratch_frames.py --storyboard <yml> [--scene <id>]`
  - 單景 mock render（緊迴路修 hook）：`python video/make.py --storyboard <yml> --scene <id> --backend mock --quality low`
  - 全片 mock render（1080p QA）：`python video/make.py --storyboard <yml> --scene all --backend mock --quality high`（make.py 會先跑 schema→lint→sizecheck，error 則 abort；`--skip-*` 可繞但不要繞）
  - 視覺 gate-1 抽幀（零計費，給 visual-frame-audit 讀）：`python video/pipeline/critic.py --storyboard <yml> --dry-run`
- **已決定、不要再議：** 只做 §3.1 一節（跳過 ch02，使用者裁決）；走完整兩階段方法論；終點＝mock 成片、**TTS 延後**；deck id＝`ch03_trig_derivatives`；分支不另開。
- **關鍵範本（照抄結構與風格）：**
  - 內容稿格式：`git show 9329a0b:video/content_scripts/ch01_inverse_functions.md`（header＋meta＋`### unit:`＋圍欄欄位；格式契約見 `CONTENT_METHODOLOGY.md` §6）。
  - 工程 storyboard 格式／旁白風格／reveal marker：[`video/storyboards/ch01_inverse_functions.yml`](../../storyboards/ch01_inverse_functions.yml)（同分支唯一正典 storyboard，檔頭有 decomposition fold 註記範例）。
  - `_narration.html` 審核稿樣板：第一次編時定版（MathJax/KaTeX CDN、逐單元列 narration、可展開 learning_goal/visual_need/animation_cue），之後沿用。
- **§3.1 教學重量：** 幾何＋符號各半（**非** symbol-heavy，三張圖都吃重）→ 全視覺處理，不套 §5 symbol-heavy 條件化。

---

## 檔案結構（會建/動到的）

- **建** `video/content_scripts/ch03_trig_derivatives.md` — Stage 1 內容稿（source of truth）。
- **建** `video/content_scripts/ch03_trig_derivatives_narration.html` — 給使用者審核的可讀稿（每次改 `.md` 都重編）。
- **建** `video/storyboards/ch03_trig_derivatives.yml` — Stage 2 工程 storyboard。
- **建** `video/animations/ch03_trig_derivatives_hooks.py` — 3 個客製動畫 hook（`sector_inequality`、`slope_equals_height`、`shm_stacked_graphs`）。
- **建** `video/content_scripts/_audit/REVIEW-ch03_trig_derivatives-applied.html` — 完成一輪後的 HTML 報告（base64 內嵌幀＋逐單元旁白＋閘結果）。
- **動** `video/REBUILD_STATUS.md` — 完成後新增一節記進度錨。
- **可能動** `video/pipeline/templates/`（僅當 §3.1 暴露出真正缺的模板能力時；預設**不動模板**，缺的視覺一律走 hook——見 Karpathy §3 外科手術式修改）。

---

## §3.1 教學單元規格（locked design；narration 於 Task 1–4 撰寫、Task 6 稽核）

> 每單元的 `narration` 是 Task 1–4 的產出、Task 6 六鏡稽核的對象——這裡鎖定 id／kind／template／source／learning_goal／必載數學／視覺需求。**忠實護欄＝「必載數學」欄**：narration 可口語重寫措辭，但不得增刪/竄改該欄的數學內容（`CONTENT_METHODOLOGY.md` §1 硬規則）。intro/divider/outro 無 narration（純動畫）。

**meta：** id=`ch03_trig_derivatives`、chapter=`Chapter 3`、chapter_title=`Chain Rule and Trigonometric Derivatives`、section=`3.1`、title=`Derivatives of Sine and Cosine`、sections 清單＝3.1/3.2/3.3、tagline=`How fast does sine change?`。

| # | id | kind | template | source（sec-3-1.html） | 必載數學 / 視覺需求 |
|---|---|---|---|---|---|
| — | intro | — | intro | Section Gate（定位） | Chapter 3 map → 聚焦 §3.1；tagline |
| | **▸ divider** `stage_limit` | divider | divider | — | eyebrow "Stage 1"／title "The Limit Behind the Slope"／ghost 1／progress 1·4 |
| 1 | why_trig_is_different | motivation | derivation | 開節散文（expansion:intuition） | 差分商 `[sin(x+h)−sin x]/h`；funnels to `lim_{θ→0} sinθ/θ`（0/0，代數無解）|
| 2 | difference_quotient_for_sine | derivation | derivation | 「difference quotient for sine」子節 | sum-to-product → `[sin(x+h)−sinx]/h = cos(x+h/2)·sin(h/2)/(h/2)`；兩因子各需「連續」與「基本極限」|
| | **▸ divider** `stage_squeeze` | divider | divider | — | "Stage 2"／"A Geometric Squeeze"／ghost 2／2·4 |
| 3 | sector_inequality ⚙️ | visual | graph + **hook** | Figure 3.1 ＋ 面積散文 | 單位圓 A=(1,0)、B=(cosθ,sinθ)、C=(1,tanθ)；△OAB⊆扇形⊆△OAC → `½sinθ ≤ ½θ ≤ ½tanθ`；`sinθ/θ` 為偶函數（故只看 θ>0）|
| 4 | squeeze_to_the_bound | derivation | derivation | Fig 3.1 後代數 | `sinθ≤θ≤tanθ` →÷sinθ、取倒數翻向 → `cosθ ≤ sinθ/θ ≤ 1`（式 1）；附帶 `0≤|sinθ|≤|θ|` |
| 5 | continuity_of_sin_cos | theorem+proof | theorem_proof | Prop 3.1 ＋ Proof | Prop 3.1：sin、cos 在每個 x₀ 連續。證：`|sinθ|≤|θ|`+squeeze ⇒ `limθ→0 sinθ=0`；sum-to-product 界住 `|cos x−cos x₀|`、`|sin x−sin x₀|` ≤ `2|sin((x−x₀)/2)|` → 0 |
| 6 | fundamental_limit | proposition+proof | theorem_proof | Prop 3.2 ＋ Proof | `lim_{θ→0} sinθ/θ = 1`。證：式 1 squeeze、`cosθ→1`（Prop 3.1）、偶 ⇒ 兩側極限 |
| 7 | squeeze_graph | visual | graph (single) | Figure 3.2（**stock，無 hook**）| `sinθ/θ`（實線）夾在 `cosθ`（虛線下）與常數 `1` 之間；θ=0 處開圓（極限非值=1）|
| 8 | limit_not_identity | caution | callout (caution) | Caution① | 極限≠恆等式：`θ=π/2` 時 `sinθ/θ=2/π≈0.64`、`θ=π` 時 `=0`；只有 θ→0 才趨 1 |
| 9 | radians_essential | caution | callout (caution) | Caution② | 弧度制必要：扇形面積 `½θ` 用弧度；度數下 `lim sin(x°)/x = π/180`，故 `sin'=cos`、`cos'=−sin` 只在弧度成立 |
| | **▸ divider** `stage_derivatives` | divider | divider | — | "Stage 3"／"The Two Derivatives"／ghost 3／3·4 |
| 10 | derivative_of_sine | theorem+proof | theorem_proof | Thm 3.1 ＋ Proof | `d/dx sin x = cos x`。證：差分商化簡式 → `cos(x+h/2)→cosx`（連續）、`sin(h/2)/(h/2)→1`（基本極限）|
| 11 | derivative_of_cosine | theorem+proof | theorem_proof | Thm 3.2 ＋ Proof（repeat-pattern 省 setup）| `d/dx cos x = −sin x`。同機制，伴隨恆等式 `cosA−cosB=−2 sin((A+B)/2) sin((A−B)/2)` |
| 12 | slope_equals_height ⚙️ | visual | graph + **hook** | Figure 3.3 | `y=sin x` 在 x=0,π/2,π 切線斜率 1,0,−1 ＝ `y=cos x` 在那些點的高度（點）|
| 13 | derivative_cycle | remark | definition_math | Remark 3.1 | `sin x → cos x → −sin x → −cos x → sin x`；`d⁴/dx⁴ sin x = sin x`；呼應 e^x 自我複製（§2.4）|
| | **▸ divider** `stage_apply` | divider | divider | — | "Stage 4"／"Consequences & Applications"／ghost 4／4·4 |
| 14 | companion_limit | example | derivation | Example 3.1 | `lim_{θ→0} (1−cosθ)/θ = 0`；×(1+cosθ) → `sinθ/θ · sinθ/(1+cosθ) → 1·0` |
| 15 | all_six_trig_derivatives | example | derivation | Example 3.2 | 商法則：`tan'=sec²x`（Pyth 恆等式收斂）、`sec'=sec x tan x`；`cot'=−csc²x`、`csc'=−csc x cot x` 帶過（repeat-pattern）|
| 16 | shm_compute | example | derivation | Example 3.3 | `s(t)=sin t`→`s'(t)=cos t`、`s''(t)=−sin t=−s(t)`；SHM 簽名 `s''=−s` |
| 17 | shm_stacked_graphs ⚙️ | visual | **hook** | Figure 3.4 | s/s'/s'' 三層共用時間軸；峰谷處（t=π/2,3π/2）velocity 過零；底圖＝頂圖上下翻（`s''=−s`）|
| 18 | toward_the_chain_rule | forward_ref | definition_math | 收尾散文 | 能微分 `sin x` 但不能 `sin(x²)`/`sin(3x+1)`；需連鎖律（**MUST NOT 報節號**）|
| 19 | recap | recap | recap_cards | 全節綜整 | 基本極限=1；`sin'=cos`、`cos'=−sin`；幾何擠壓法；弧度制；導數四步循環 |
| — | outro | — | outro | — | next_section "3.2" / next_title "The Chain Rule" |

**可折疊項（執行時若 narration 過載/過短再裁決，就近註明）：** unit 8+9 兩 Caution 可併一場；unit 16+17 SHM 計算＋圖可併；unit 5 連續性證明偏長，可走「statement 場＋proof 場」拆法或精簡（影片只需邏輯鏈：界 → squeeze → 連續，不必每行代數）。

---

## 三個客製 hook 的 `animation_cue` 規格（Stage 2 依此生成 manim code）

> hook 機制：storyboard 場景加 `hook: "animations.ch03_trig_derivatives_hooks:<fn>"`；factory 收 template blocks、回傳最終 list（可換 mobject 保留 reveal id、翻 static→dynamic、掛 anim）。生成 code **經使用者過目認可**再定版；render 失敗走「由小到大逐層修補」（`CONTENT_METHODOLOGY.md` §5）。reveal id 對齊 narration 的 `{show ...}`。

1. **`sector_inequality`（Fig 3.1）** — 單位圓（半徑 1）、A=(1,0)。畫出 B=(cosθ,sinθ) 與射線 OB 延伸交切線於 C=(1,tanθ)。依序高亮三塊嵌套區域並標面積：內接 △OAB（`½sinθ`）→ 扇形 OAB（`½θ`）→ 外切 △OAC（`½tanθ`），讓「一個包一個」在視覺上成立 → 浮出 `½sinθ ≤ ½θ ≤ ½tanθ`。θ 可從中等角緩縮小，暗示後續取極限。reveal id：`tri_inner`／`sector`／`tri_outer`／`ineq`。
2. **`slope_equals_height`（Fig 3.3）** — 同框畫 `y=sin x`（實）與 `y=cos x`（虛）。在 x=0,π/2,π 對 sin 畫切線段，標斜率 1,0,−1；同時在 cos 上那三個 x 放點，標高度 1,0,−1，用引線/同色把「sin 的斜率 ＝ cos 的高度」一一對上。reveal id：`tan_0`／`tan_halfpi`／`tan_pi`／`cos_dots`。
3. **`shm_stacked_graphs`（Fig 3.4）** — 三個垂直堆疊的小圖共用一條時間軸 t∈[0,2π]：頂 `s=sin t`、中 `s'=cos t`、底 `s''=−sin t`。在 t=π/2、3π/2 拉垂直虛線：標頂圖峰/谷處、中圖（velocity）正好過零。視覺點出「底圖＝頂圖上下翻」＝`s''=−s`。reveal id：`g_s`／`g_v`／`g_a`／`mirror`。

---

## Tasks

### Task 0 — 前置與範本就位
**Files:** 讀 only（撈範本）。
- [ ] 確認在分支 `video/template-redesign-navy-spine`、工作樹乾淨：`git status`。
- [ ] 撈內容稿格式範本到 scratch 供對照：`git show 9329a0b:video/content_scripts/ch01_inverse_functions.md`（只讀、抄結構，不覆蓋）。
- [ ] 確認環境：`python tools/doctor.py`（fonts 段需綠：plex-sans/plex-mono/lmodern）。
- **驗證點：** doctor 全綠、範本可讀。

### Task 1 — Stage 1 內容稿：header＋meta＋intro＋Stage 1（units 1–2）
**Files:** Create `video/content_scripts/ch03_trig_derivatives.md`
- [ ] 寫檔頭（比照 ch01.md：產線/權威來源/這是什麼/階段=DRAFT）＋ `## meta` 段（上表 meta 欄位＋章內節次清單 3.1/3.2/3.3）。
- [ ] 寫 `### unit: intro`（純動畫、narration「（無）」）。
- [ ] 寫 `### unit: why_trig_is_different`、`### unit: difference_quotient_for_sine` 的完整欄位（id/source/learning_goal/kind/narration/visual_need/animation_cue）。narration 依 §4：口語、3–7 句、hook→body→takeaway、數學直讀 LaTeX、對齊鏈不重念 LHS。
- **驗證點：** 通讀兩段 narration，聽起來像「說出來的課」、未犯 §4 禁則（不念標題/不報節號/不用「see/as shown」）。

### Task 2 — Stage 1 內容稿：Stage 2（units 3–9）
**Files:** Modify `video/content_scripts/ch03_trig_derivatives.md`
- [ ] 寫 `stage_squeeze` divider 之後的 7 個單元：sector_inequality、squeeze_to_the_bound、continuity_of_sin_cos、fundamental_limit、squeeze_graph、limit_not_identity、radians_essential。
- [ ] sector_inequality、squeeze_graph 寫 `animation_cue`／`visual_need`（聚焦教學意圖、自然語言、不寫座標/manim 物件名）。
- [ ] 兩個證明單元（5、6）narration 走「邏輯鏈」而非逐行代數；continuity 若超 ~4 步，就近註記是否拆 statement/proof。
- **驗證點：** 每個 def/thm/prop 有單元覆蓋；散文間 prose 都歸類（fold/promote、無 silently drop）；兩 Caution 各自獨立或就近註記折疊。

### Task 3 — Stage 1 內容稿：Stage 3（units 10–13）
**Files:** Modify `video/content_scripts/ch03_trig_derivatives.md`
- [ ] 寫 `stage_derivatives` divider 後 4 單元：derivative_of_sine、derivative_of_cosine、slope_equals_height、derivative_cycle。
- [ ] derivative_of_cosine 套 repeat-pattern：一句轉場（"Same machinery, companion identity…"）直接進新內容，不重述差分商 setup。
- [ ] slope_equals_height 寫 `animation_cue`（Fig 3.3 規格）。
- **驗證點：** Thm 3.1/3.2 各有單元；repeat-pattern 落實；derivative_cycle 忠實 Remark 3.1（含 e^x 呼應）。

### Task 4 — Stage 1 內容稿：Stage 4（units 14–19）＋ recap
**Files:** Modify `video/content_scripts/ch03_trig_derivatives.md`
- [ ] 寫 `stage_apply` divider 後 6 單元：companion_limit、all_six_trig_derivatives、shm_compute、shm_stacked_graphs、toward_the_chain_rule、recap。
- [ ] shm_stacked_graphs 寫 `animation_cue`（Fig 3.4 規格）。
- [ ] toward_the_chain_rule：forward-pointing，**MUST NOT 報節號**；recap：takeaway 清單（5 點，對齊上表）。
- **驗證點：** 折疊掉的同型例題就近註明；recap 有 takeaway；outro meta 的 next_section/next_title 就位（在 storyboard，不在內容稿，此處只記）。

### Task 5 — 編 `_narration.html` 審核稿 ＋ 通讀
**Files:** Create `video/content_scripts/ch03_trig_derivatives_narration.html`
- [ ] 寫一個小生成步驟（讀 `.md` → standalone HTML，MathJax/KaTeX CDN、逐單元 narration＋可展開 learning_goal/visual_need/animation_cue）。第一次定版型，記下供 §3.2/3.3 沿用。
- [ ] 瀏覽器開啟，確認數學渲染正確、與 `.md` 一致。
- [ ] **通讀整份 narration**：任何一段聽起來像教科書 → 就地重寫。
- **驗證點：** HTML 雙擊即開、數學即渲染、與 `.md` narration 逐字一致。

### Task 6 — 六鏡對抗式稽核（gate-1，免費 Workflow）→ 修到 blocking==0
**Files:** Modify `.md`（依裁決）；稽核紀錄入 `_audit/`。
- [ ] 跑六鏡 multi-agent Workflow（SSOT `content_scripts/_audit/CONTENT-SIXLENS-RUBRIC.md`）：L1 忠實／L2 拆解／L3 語域／L4 不重複／**L5 數學正確（對每個證明/例題獨立重算、隔離盲算）**／L6 完整；refute-by-default、每條過四級分級、Claude 逐條複驗。
- [ ] 對每條 blocking 外科式修 `.md`，**回歸再審**改動項（CLAUDE.md meta-rule），重編 `_narration.html`。
- **驗證點：** 六鏡 **blocking==0**（advisory 逐筆人裁、不強制歸零）；L5 對 §3.1 尤關鍵（弧度/偶函數/squeeze/商法則易錯）。
- **收斂線：** blocking findings == 0。

### Task 7 — 散文 copyedit pass（gate-1，免費）→ tighten
**Files:** Modify `.md`（lock 前唯一改措辭窗口）。
- [ ] 跑 `narration-copyedit` subagent（SSOT `NARRATION-COPYEDIT-RUBRIC.md`）：C1–C5 贅字／冗餘／朗讀流暢／句長／跨單元回音。硬護欄：語義不得改（不動數值/區間/步驟）。
- [ ] 採納 tighten、重編 `_narration.html`。
- **驗證點：** 冗餘/贅字在 lock 前清掉（lock 後 NFA 不再動措辭）。

### Task 8 — 使用者 sign-off ＋ 鎖稿
**Files:** Modify `.md`（階段標記 DRAFT→LOCKED）。
- [ ] 交付 `_narration.html` 給使用者審核旁白。**等使用者明確認可。**
- [ ] 認可後把 `.md` 檔頭階段標記改 LOCKED、設 `CONTENT_APPROVED`；commit Stage 1（內容稿＋HTML＋六鏡/copyedit 裁決紀錄）。
- **驗證點：** 使用者書面認可；source 自此凍結（後續稽核唯讀）。

### Task 9 — Stage 2 storyboard 骨架（meta＋intro/4 divider/outro＋stock-template 場景）
**Files:** Create `video/storyboards/ch03_trig_derivatives.yml`
- [ ] 比照 `ch01_inverse_functions.yml`：寫 meta（id/chapter/section/title/sections/theme/voice/video）＋檔頭 decomposition fold 註記。
- [ ] 把 19 內容單元模板化：填 `template`／`accent`／`say`（內嵌 `{show ...}` reveal marker，對齊內容稿 narration）／payload（statement/math/steps/result/proof/points/header/rows/plots/axes…）。**stock 模板場景先做**（definition_math/derivation/theorem_proof/callout/recap_cards/graph-single），3 個 hook 場景先放 stock fallback。
- [ ] intro／4 個 divider（ghost 1–4、progress n·4）／outro（next 3.2）就位。
- **驗證點：** `python video/pipeline/schema.py video/storyboards/ch03_trig_derivatives.yml --list` 無 error、列出的 `{show}` 目標全部 resolve、無 stale marker。

### Task 10 — 客製 hook ①：`sector_inequality`（Fig 3.1）
**Files:** Create `video/animations/ch03_trig_derivatives_hooks.py`（`sector_inequality` factory）；Modify storyboard（unit 3 加 `hook:`）。
- [ ] 依上方 `animation_cue` 規格生成 manim code（reveal id：tri_inner/sector/tri_outer/ineq）。
- [ ] 緊迴路：`python video/make.py --storyboard <yml> --scene sector_inequality --backend mock --quality low` → 抽幀目視。render 失敗走「局部修→放大到 hook 函式→才整支重生」階梯。
- **驗證點：** 單景 render EXIT 0；抽幀：三嵌套區域正確、面積標註對、不等式端態數學對。

### Task 11 — 客製 hook ②：`slope_equals_height`（Fig 3.3）
**Files:** Modify hooks.py（加 `slope_equals_height`）；Modify storyboard（unit 12 加 `hook:`）。
- [ ] 生成 code（reveal id：tan_0/tan_halfpi/tan_pi/cos_dots）：sin 三切線斜率 1/0/−1 對上 cos 三高度點。
- [ ] 單景 render＋抽幀；失敗走修補階梯。
- **驗證點：** 切線斜率與 cos 高度視覺對齊正確、標註無壓線。

### Task 12 — 客製 hook ③：`shm_stacked_graphs`（Fig 3.4）
**Files:** Modify hooks.py（加 `shm_stacked_graphs`）；Modify storyboard（unit 17 加 `hook:`）。
- [ ] 生成 code（reveal id：g_s/g_v/g_a/mirror）：三層共軸堆疊、t=π/2,3π/2 虛線、底＝頂上下翻。
- [ ] 單景 render＋抽幀；失敗走修補階梯。
- **驗證點：** 三圖共用時間軸對齊、峰谷↔過零對應正確、`s''=−s` 鏡射視覺成立。

### Task 13 — 三閘全過（schema / lint / sizecheck）
**Files:** Modify storyboard（修閘報的問題）。
- [ ] `python video/pipeline/schema.py <yml>`（結構＋reveal 目標）
- [ ] `python video/pipeline/lint.py <yml>`（純文字欄無 `$`/反斜線、`$` 成對）
- [ ] `python video/pipeline/sizecheck.py <yml>`（同層字級一致、無出框）
- **驗證點：** schema/lint **0 error**；sizecheck 0 error（within-frame advisory warn 逐筆判、記錄）。

### Task 14 — 全片 mock render（1080p）
**Files:** 產 `video/output/...`（gitignore、可重生）。
- [ ] `python video/make.py --storyboard <yml> --scene all --backend mock --quality high`。
- [ ] 注意 REBUILD_STATUS 教訓：**render 與 sizecheck/critic 不可同時跑**（Tex-cache race）；transient flake 刪 0-byte 快取＋retry。
- **驗證點：** 三閘過 → 全 25 場 render → compose → mp4 產出（h264 1080p）；3 hook 端態數學全對、零 runtime 錯。

### Task 15 — 視覺幀稽核（gate-1 visual-frame-audit，免費）→ 修到 blocking==0
**Files:** Modify storyboard/hooks（依裁決）。
- [ ] 抽幀：`python video/pipeline/critic.py --storyboard <yml> --dry-run`（零計費，抽每場最滿幀）。
- [ ] 對每場跑 `visual-frame-audit` subagent（SSOT `VISUAL-FRAME-RUBRIC.md`）：V1–V9 blocking（數學渲染完整、圖正確、reveal 同步、端點實心/空心、✓/✗ 正確、不出框/不相撞）＋A1–A7 magnitude。可用 Workflow 並行（每場一 agent，refute-by-default）。
- [ ] 修 blocking → 重渲改動場 → 複驗（回歸再審）。
- **驗證點：** 視覺 **blocking==0**；advisory 逐筆記錄。
- **收斂線：** 視覺 blocking findings == 0。

### Task 16 — HTML 報告 ＋ 進度錨 ＋ commit
**Files:** Create `video/content_scripts/_audit/REVIEW-ch03_trig_derivatives-applied.html`；Modify `video/REBUILD_STATUS.md`。
- [ ] 產 self-contained HTML 報告（base64 內嵌關鍵幀＋逐單元旁白＋6 鏡/copyedit/視覺閘裁決），比照 `REVIEW-ch01_inverse_functions-*`。
- [ ] `REBUILD_STATUS.md` 新增一節記 §3.1 進度（到 mock 里程碑、TTS 延後、3 hook、各閘收斂）。
- [ ] commit Stage 2（storyboard＋hooks＋報告＋status）。
- **驗證點：** 報告雙擊即開、數學即渲染；REBUILD_STATUS 對得上；working tree 乾淨。

---

## 收斂定義（「做完＝與 §1.1 同級」）

mock 里程碑達成 ＝ 內容稿 LOCKED（六鏡＋copyedit blocking==0、使用者 sign-off）＋ storyboard 三閘 0 error ＋ 全片 mock render 成功 ＋ visual-frame-audit blocking==0 ＋ HTML 報告與 REBUILD_STATUS 就位。

## 計費閘（deferred — 達 mock 里程碑後、各自單獨報價徵同意才跑）

- **spoken derive ＋ NFA**：`derive_spoken.py --deck ch03_trig_derivatives --check`（免費 parity）後跑 `narration-faithfulness-audit`（gate-1 免費）—— 屬 MiMo TTS 路線，TTS 延後故一併延後。
- **MiMo TTS 合成**（計費）：`tts.py --backend mimo`（先 `--dry-run` 估量）。
- **Codex gate-2**（計費）：六鏡不疊 Codex；copyedit/NFA 近定稿時單次。
- **VLM critic gate-2**（外部 API、公測免費仍需同意）：`critic.py --confirm`。
