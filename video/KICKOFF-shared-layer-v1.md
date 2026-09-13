# KICKOFF — 共用層 v1 凍結（字體／字級／sizecheck 規則／`worked_example`）

> 2026-09-13 立檔。本檔給**新 session** 直接開工：§0 可整段貼進對話當啟動提示；§2 是本檔作者
> 逐條 grep 核過的 code 事實（**行號為 2026-09-13 快照、會漂，用 grep 重找**）；§5 是任務、§6 是驗收。
>
> **這是工具線的一輪**，不是某一節的內容輪。它的存在理由只有一個：**四項共用層改動在鋪開之後再改，
> 代價是 N 節重做。** 原始描述在 [`KICKOFF-s31-amplify.md`](KICKOFF-s31-amplify.md) §7.1（設計畫布
> 與 [`_audit/design-template-system/`](_audit/design-template-system/) 的 `.dc.html` 工作檔＋README）；
> 本檔把它轉成可執行的 task，並補上那份 §7.1 沒有的 code 事實與驗收迴圈。

---

## 0. 給新 session 的啟動提示（可整段貼）

> 讀 `video/KICKOFF-shared-layer-v1.md` 然後照它做。背景：2026-09-13 使用者裁決「原語路線推廣到
> 全部小節、教義定案；§3.2 解凍；先把流程用 §3.2 串行走一遍變成熟，再並行處理後面的章節」。
> **並行之前必須先凍結共用層 v1**，使用者選了四項全做：① 字體換 Instrument Sans ② 數學字級收成
> 三階＋取消 `math_sm 40`（與 `prose_sm`／`tag` 放大併案）③ 版面 4 條／數學 5 條規則裡能自動的寫進
> `sizecheck` ④ `worked_example` 新模板。本檔 §5 是四個 task 的契約，§6 是共同驗收。全程零計費
> （mock render＋現有 Dean 音檔 reuse，不碰 TTS／agy／Codex）。**兩個必停點：T1 的字型安裝要先徵詢
> （根 `CLAUDE.md`「缺套件先問」），以及 T1 做完的 go／no-go 人閘。** 其餘中途不要停下來問，
> 除非 §3 護欄被觸發。每個 task 一個 worktree 一個 commit，先寫會紅的測試再讓它綠。

---

## 1. 目標與裁決摘要（這是契約）

| # | 裁決（2026-09-13 使用者） | 內容 |
|---|---|---|
| A | **教義定案** | 原語路線（motion primitive 鋪滿）**推廣到全部小節**，不再是 §3.1 的試點 |
| B | **§3.2 解凍** | `ch03_chain_rule` 從「凍結至 A/B 裁決」（`REBUILD_STATUS.md` 各節狀態表）解除 |
| C | **節奏** | **先把流程用 §3.2 串行走一遍變成熟，再並行處理後面的章節**（每節一個 session） |
| D | **前置條件** | 並行之前**凍結共用層 v1**＝本檔的四個 task，四項全做 |

**為什麼是這四項、為什麼是現在：**

- 四項每一項都改**所有節共用的東西**（字體改全部文字度量、字級改全部數學、`sizecheck` 改全部閘、
  `worked_example` 是所有例題場的模板）。鋪開之後再改＝N 節重做。
- 全書 8 章共 **198 個 `envexample` 例題單元**（ch01 43／ch02 23／ch03 16／ch04 7／ch05 27／
  ch06 21／ch07 23／ch08 38；含附錄 A/B/C 的 7／11／4 則為 220，即 §7.1 引的數字）。§3.2 的鏈鎖律
  有 5 個例題（`ex:3.4`–`ex:3.8`），**非 ④ 不可**——現況只能靠 `derivation` ＋ `prompt:` 硬撐
  （見 §2「例題現況」，這一條與 §7.1 的描述不同，已更正）。

### 凍結後的規則（本輪 merge 完就生效，寫進 `REBUILD_STATUS.md`）

> **任何共用層改動一律走工具線。** 共用層＝`pipeline/templates/`、`pipeline/visuals/theme.py`、
> `pipeline/brand.py`、`pipeline/sizecheck.py`、`pipeline/blocks.py`、原語相關模組
> （`focus.py`／`pacing.py`／`texparts.py`／`stillness.py`）。走工具線的意思是：
> **紅測試先行 → 全 deck 零行為改變證據 → 一個 worktree 一個 commit**，
> **不在某一節的對話裡順手改**。某節需要共用層改動時，開一個工具線的 task，不要就地動手。

---

## 2. 已驗證的 code 事實（2026-09-13 快照；行號會漂，用 grep）

### 2.1 型階與字體（T1、T2 用）

- **`pipeline/visuals/theme.py:65-76` `_SCALE_PX`**（px＠1920×1080）：
  `hero 112`／`h1 78`／`h2 58`／`h3 44`／`prose 42`／**`prose_sm 35`**（`:68`）／`statement 44`（`:69`）／
  `math 48`／**`math_sm 40`**（`:70`）／`caption 30`／`eyebrow 26`／`numeral 104`／`ghost_numeral 520`／
  **`tag 30`**（`:72`，註解寫著「was eyebrow=26 == floor; **A/B may settle 32**」）；
  back-compat alias `display/body/step/label`、`intro_headline 92`／`intro_subtitle 35`／`outro_headline 78`。
  **`_SCALE_PX` 裡沒有 `result` 這一階**——`DESIGN.md:1211` 型階表列的「result 54」是
  `templates/derivation.py:136` 的 **raw px `size=54`**（`brand.math_line(..., size=54)`），
  走 `theme.fs()` 的 raw-px 分支（`theme.py:86-88`）。T2 要動「結論 62 px」就是動這個 54。
- **`theme.py:94` `MIN_FONT_FLOOR = 26.0`**（px；註解：設在最小的**刻意**字級 eyebrow=26；
  比對對象是 `sizecheck._effective_font_px` 還原出來的 authored px，不是 `_norm_size`）。
- **兩個換算常數，換字體要重校的是後者：**
  - `theme.py:47` **`PX_TO_FS = 0.698`** ＝ **MATH（Latin Modern）錨**。註解明說 Route A 換字體時它
    不動，因為數學沒換字。
  - `theme.py:54` **`TEXT_SCALE = 1.3102`** ＝ **TEXT-only 縮放**，`1.3102 = 0.9145 / 0.698`，
    目的是把 Plex 文字拉到 Times 錨定的 cap height `0.006624 u/px`。`brand.py:190-195`
    `_text_fs(size) = T.fs(size) * T.TEXT_SCALE`，`brand` 的所有文字建構器都經它；
    math（`math_line`／`glyph`／`MathTex`）直接用 `T.fs(size)`。
    → **換文字字體＝重校 `TEXT_SCALE`（新字的 cap-height per fs），不是重校 `PX_TO_FS`。**
- **`brand.py:67` `_WIDTH_K = 0.00507`**：`estimate_text_width(text, font_size)`
  （`:77-80`，權重＝CJK ×2、空格 ×0.5，`_char_weight` `:70-75`）→ `wrap_text`（`:83-97`）的
  唯一行寬來源（Route A 之後不再用 `Text` 量真實 SVG 寬）。校準註解在 `:59-65`：
  **「Plex Sans via LaTeX measures ~0.004973 per char\*fs（Route A, 2026-06-24）；
  0.00507 = that + 2%」**，且明說「retune if fonts change」。
- **字型設在哪：`pipeline/_bootstrap.py:45-88` `apply_tex_template()`**。preamble（`:73-87`）逐行：
  `\usepackage{lmodern}`（數學，註解標 locked）／`\usepackage{plex-sans}`／`\usepackage{plex-mono}`／
  `\renewcommand{\familydefault}{\sfdefault}`／`\usepackage{microtype}`／`\everymath{\displaystyle}`／
  三個 `\DeclareMathOperator{\arccsc,\arcsec,\arccot}`。
  **必須 per-scene 重套**（`:57-66` 的 docstring：`tempconfig` 不保留 `config.tex_template`，
  退出任何 `tempconfig` 就掉回 manim 預設的 serif CM）——`LessonScene.construct()` 已經在呼叫它。
- **硬約束：只能 pdflatex**（`ENVIRONMENT.md:100-105`、`_bootstrap.py:11-14` docstring）——
  lualatex/xelatex 會破壞 manim 的 `\special{dvisvgm:raw}` 數學子部件定址，所以需要 fontspec 的路都封死。
- **Instrument Sans 現況（2026-09-13 本機探測）：**
  - `kpsewhich plex-sans.sty` → `C:/Users/Kao/AppData/Local/Programs/MiKTeX/tex/latex/plex/plex-sans.sty`（有）
  - `kpsewhich instrument-sans.sty` → **無**。CTAN 沒有 Instrument Sans 的 pdflatex 套件
    （它是 2023 年的 Google Font／OFL，只有 OTF/TTF）。對照組：`raleway.sty`／`sourcesanspro.sty`／
    `firasans.sty` 在本機 MiKTeX 都找得到——**有 CTAN 套件的 sans 才是「裝一下就能用」的。**
  - **但工具鏈在：** `which otftotfm` → `.../MiKTeX/miktex/bin/x64/otftotfm`、
    `which autoinst` → 同目錄（MiKTeX 自帶 lcdf-typetools）。所以路徑是
    **「下載 OTF → `autoinst` 生 pdflatex 字型支援 → vendored 進 repo」**，不是 `\usepackage{}` 一行。
  - **vendoring 前例：** `handout/latex/template/fonts/inter/*.otf`＋`LICENSE.txt` 在版控裡
    （六個字重）。但那條線是 **lualatex+fontspec**（`ENVIRONMENT.md:122-127` ③b），與本線的
    pdflatex 硬約束不同，**不能照抄，只能照抄「OTF 進版控＋帶 LICENSE」這個做法**。
- **設計畫布的 mockup 連數學字體也換了：** `_audit/design-template-system/DirectionB.dc.html:12,14`
  ——文字 `'Instrument Sans', system-ui, sans-serif`，**數學 `'Source Serif 4', Georgia, serif`**。
  §7.1 只說「字體：Direction B 的 mockup 用 Instrument Sans」，沒提數學那半。
  **T1 的範圍問題必須在開工時講清楚**（見 §5 T1-0）。

### 2.2 `math_sm`／`prose_sm`／`tag` 的 call site（T2 的爆炸半徑）

`math_sm`（`pipeline/` 內）：`templates/graph.py:121,128,145,146`（曲線標籤、軸標 `x`／`y`）、
`graph.py:406`（`default_label_size`，註解記著它是從 `label` 30px 升上來的）、
`templates/theorem_proof.py:175`（QED glyph）、`templates/sign_chart.py:129`、
`templates/procedure_steps.py:115,117`。
**hook 內另有約 20 處**：`animations/ch03_trig_derivatives_hooks.py:310,815,818,819,910,1064,1139,1273,1475,2510,2512,2514`、
`animations/ch03_chain_rule_hooks.py:142,214`、`animations/ch01_inverse_functions_hooks.py:102,103,116,231,232,238,239,249,250`。
其中 `ch03_trig_derivatives_hooks.py:2508` 與 `:1137` 的註解記著**上一輪視覺幀稽核剛把 `label`(30) 升到 `math_sm`(40)**
——取消 `math_sm` 就是再動這兩處剛修好的東西，幀對照必看。

`prose_sm`：`templates/_common.py:430`（`build_aside` body）、`:483`（`scaffold.motive`）、
`templates/value_table.py:118`（表頭）、`templates/derivation.py:68`
（`_REASON_PX = T._SCALE_PX["prose_sm"]`，註解「一般 reason 的 authored px（**A/B 開放值：35 或 38**）」）。

`tag`：`templates/_common.py:283,379`（part pager）、`templates/derivation.py:301`（result reason eyebrow）、
`:382`（floor clamp 用 `T._SCALE_PX["tag"]`，註解明說這是為了讓 `_REASON_PX` 不會漂離 guard）。

→ **`prose_sm 35 或 38` 與 `tag 30 或 32` 是兩個「A/B 尚未收斂」的開放值**，這就是使用者說的
「與 `prose_sm`／`tag` 放大併案」：三階收斂時一次把這兩個也定死。

守門測試：`pipeline/_selftest_type_scale.py`（`statement` 階不得漂）、
`pipeline/_selftest_semantic_palette.py`（重讀 `handout/latex/template/calcbook.sty` 比對色相）。

### 2.3 `sizecheck.py` 現況（T3 用）

`check_scenes(meta, scenes, deck=None)` `sizecheck.py:605`，回傳 `list[(severity, msg)]`，
severity ∈ {`error`, `warn`}；`make.py` 有 error 即 abort（`--skip-sizecheck` 可繞）。逐項：

| 檢查 | 函式／行 | 分級 | 適用 kind |
|---|---|---|---|
| 出框／進安全邊界 | `_overflow_issues` `:82`，呼叫 `:634` | error／warn | 全部 |
| **F9**：`{show <target>}` 指到不存在的 block | inline `:637-645` | error | 全部 |
| `focus[].dim` id 不存在 | inline `:652-658` | error | 全部 |
| `focus[].indicate` id 不存在 | inline `:659-664` | error | 全部 |
| `exit:` id 不存在 | inline `:669-672` | error | 全部 |
| 兩個 content block 重疊 | `_overlap_issues` `:159`（`OVERLAP_FRAC=0.20` `:36`） | warn | content |
| 兩個 graph 標籤疊住 | `_graph_label_overlap_issues` `:220`（`LABEL_OVERLAP_FRAC=0.30` `:37`） | warn | content |
| 最緊間距也裝不下一頁 | `_capacity_issues` `:331` | warn | content |
| 單一 block 把 body zone 晾著 | `_sparse_issues` `:481` | warn | content |
| theorem statement 長到變色帶 | `_statement_regime_issues` `:530` | warn | content |
| stacked sibling 字級不一 | inline `:697-714`（`SIBLING_PREFIXES` `:34`、`TOLERANCE=1.06` `:35`） | error | content |
| 教學散文用 muted 色 | inline `:716-730` | warn | content |
| 字級低於 `MIN_FONT_FLOOR` | `_floor_issues` `:588` / `_floor_findings` `:580` | **warn-default，`meta.fontfloor_enforce` 才 error** | content |

- **`meta.*_enforce` 旗標模式的兩個範本：**
  ① `sizecheck.py:732-734`——`enforce = bool(meta.get("fontfloor_enforce"))` 直接傳進檢查函式；
  ② `pipeline/pedagogy.py:10-15` `assumptions_registry_issues(data, enforce)`——
  `sev = "error" if enforce else "warn"`，**且「registry 不存在 → 回 []」＝零行為改變直到 opt-in**。
  T3 的新規則照 ② 寫（沒宣告就沒 finding）。
- **已知盲點（寫在 `REVIEW_GATES.md` §一 層 6 與 `DESIGN.md`）：** `sizecheck` 只查
  `brand.prose` tag 過的節點，**直接構造的 `MathTex`／`Text` 不查**。T3 的版面規則若要量「結論 vs 鋪陳」
  的字級，會踩到這個盲點（結論常是 `math_line` 出來的 `MathTex`）——`_effective_font_px` `:558`
  是現成的還原器，但 `_prose_nodes` `:40` 只收 `_brand_prose` 標記過的。**這是 T3 最先要決定的事。**
- 版面規則 3 要的「右欄」**已經存在**：`_common.build_aside` `:422`（`{label?, body, accent?}`），
  `callout`／`definition_math`／`derivation`／`theorem_proof` 都收 `aside`。
  用過的 deck 只有 `_demo_aside.yml`／`_demo_registers.yml`／`ch01_inverse_functions.yml`——
  **兩個 ch03 deck（§3.1 27 場、§3.2）一次都沒用過**，§7.1 的「27 場一次都沒用過」核實無誤。

### 2.4 template registry 與回歸 deck（T4 用）

- **加一個 template 要同時改兩處，否則 parity selftest 會紅：**
  `pipeline/templates/__init__.py:40-54` `REGISTRY`（12 個：9 個 content ＋ `intro`／`outro`／`divider`）
  與 `pipeline/template_names.py:7-10` `CONTENT_TEMPLATES`（9 個 tuple，manim-free 單一源）。
  守門＝`pipeline/_selftest_template_registry.py`。
  **連帶效果：`pipeline/tts.py:35,59` 的 `SCENE_UNIT_TEMPLATES = frozenset(CONTENT_TEMPLATES)`**
  ——新 template 自動變成 scene-level TTS 單位（這是想要的，但 `RUNBOOK-mimo-narration-route.md:67`
  寫死「全部 content template（**9 個**）」那句要同輪改成 10）。
- **`build_blocks` 的組裝順序**（`templates/__init__.py:56-84`）：
  `brand.set_color_map(meta.color_map)` → intro/outro/divider 早退 → `REGISTRY[template](spec, ctx)` →
  dark 才前置 `scene_spine` → `_apply_carry` → `_apply_hook` → `_scaffold_reveal_timing` → `pacing.apply`。
  新 template 只要回 `list[Block]`，原語 1（`{show}`）／4（`focus:`）／5（`carry:`）／7（`paced:`）
  **自動適用**；原語 2（`anim: transform`）與 3（`sweep`／`inset`）是 `derivation`／`graph` 各自實作的，
  **新 template 想要就得自己接**。
- **回歸 deck 清單：T4 併入前 22 個、併入後 23 個 `.yml`**（2026-09-13）＝ 18 個 `_demo_*.yml`
  （`aside`／`asymptote`／`capacity`／`carry`／`color_map`／`derivation`／`graph_compare`／`graph_muted`／
  `graph_reveal`／`inset`／`label_overlap`／`multipage`／`registers`／`sign_chart`／`tall_rows`／
  `tex_parts`／`theorem_regime`／`value_table`）＋ `ch01_inverse_functions`／`ch03_chain_rule`／
  `ch03_trig_derivatives`／`ch03_trig_derivatives_mimo`，**＋ T4 新增的 `_demo_worked_example`（第 23 個）**。
  **`REBUILD_STATUS.md` 品質補強輪 ⑦ 寫的「18 個 deck」是 2026-09-12 的數字**，
  之後輪 ⑭ 新增了 `_demo_color_map`／`_demo_inset`／`_demo_carry`／`_demo_tex_parts` 四個。
  **T1–T3 的零行為改變證據要蓋 23 個**（T4 併入前的 Phase 0 基線只有 22 個；`_demo_worked_example`
  的基線＝T4 併入後那次）。
- **`pipeline/_selftest_*.py`：T4 併入前 42 支、併入後 43 支**（多了 `_selftest_worked_example`；
  `run_selftests.py --list` 實測 2026-09-13）。

### 2.5 例題現況（T4 的真正起點；**與 §7.1 的描述不同，以此為準**）

- **講義端結構**（`handout/latex/src/ch03/chapter3.tex`）：
  ```latex
  \begin{workedexample}                          % 外層包裝
  \begin{envexample}{Example}{ex:3.1}{}          % 題目（:136）
  Establish the companion limit \(\lim_{\theta\to 0}\frac{1-\cos\theta}{\theta}=0\).
  \end{envexample}
  \begin{envsolution}{Solution}{}{}              % 解答（:139）
  ... 散文 + \[ \begin{aligned} ... \end{aligned} \] 多步驟 ...
  \end{envsolution}
  \end{workedexample}                            % :152
  ```
  多小題的形態＝**題目一句話帶 (a)(b)、解答分段**（`ex:3.2` `:154-181`：「differentiate (a) `\tan x` and
  (b) `\sec x`」，解答兩塊 `aligned` ＋ 收尾一句把 `cot`／`csc` 一併交代）。
  `ex:3.3` `:183-193` 是應用題（物理情境 → 兩次微分 → 一句詮釋）。
- **節歸屬**：`\sechead{3.1}` `:30`、`\sechead{3.2}` `:208`、`\sechead{3.3}` `:417`。
  → **§3.1 只有 3 個例題（`ex:3.1`–`ex:3.3`），不是 16；16 是整個 ch03。**
  （§7.1「§3.1 有 16 個例題」是把章數當節數，本檔更正。）
- **`pipeline/example_coverage.py`**：`_TEX_SECHEAD` `:44`、`_TEX_EXAMPLE` `:45`
  （`\\begin\{envexample\}\{[^}]*\}\{(ex:[^}\s]+)\}`）；`ex:` **是章序不是節序**，歸節只看
  `\sechead` 區間（docstring `:29-36`）。內容稿端宣告＝代表單元的 `examples:`／`folds:`
  （`content_scripts/ch03_trig_derivatives.md:601,643,713`；`ch03_chain_rule.md:445,498,526,556,584`）。
  **閘只查宣告存不存在**（docstring `:11-17` 自己寫著 `covered` 是記帳不是教學）；
  只接 `schema.py:main()`、不接 `make.py`；deck 無 `.md` 整個跳過。
  `EX1` 在 `meta.example_coverage_enforce` 開時才 error（§3.1 deck 目前**沒設**這個旗標）。
- **影片端不是「一場都沒有」**：§3.1 deck 有 **4 個帶 `prompt:` 的場**
  （`companion_limit`／`all_six_tan_sec`／`all_six_cot_csc`／`shm_compute`），§3.2 deck 有 **5 個**
  （`example_*`），**全部走 `template: derivation`**，由 `_common.example_head` `:354-365` 畫成
  `[ EXAMPLE ]` eyebrow ＋題目當 headline ＋細線 ＋ `SOLUTION` lead
  （契約在 `DESIGN.md:465-479`「Worked-example 題目結構」，`lint._example_missing_prompt` 在把關）。
  → **T4 的缺口不是「沒有例題場」，是「例題場只有推導鏈的形狀」。**
  mockup（`_audit/design-template-system/WorkedExample.dc.html`）比現況多的是三樣：
  ① `STRATEGY` 策略卡（一句話說為什麼這樣下手）
  ② `WHAT EACH FACTOR DOES` 逐因子欄（每個因子 → 它的極限 → 引用 `PROP 3.2` 這種出處）
  ③ 底部 `ANSWER` 結論帶（帶語意色、字級最大）。
  **T4 要做的是這三樣，不是重寫 `example_head`。**

> **⚠ 本節（§2.5）與 §5 T4 原是在不知道 `worked_example` 已有一條完成分支的情況下寫的。
> 2026-09-13 該分支（`claude/unruffled-antonelli-db3c3e`，5 commit）已併入 main，
> 以下以落地現況為準——契約全文見 [`KICKOFF-worked-example-template.md`](KICKOFF-worked-example-template.md)
> 的 D1–D14 與 §7，驗收報告見 [`_audit/REVIEW-worked-example-template-applied.html`](_audit/REVIEW-worked-example-template-applied.html)。**
>
> - **欄位名以落地為準（不是本節上文的 factors／answer）：**
>   `strategy:`（字串，rail 上段）／`notes: [{math, text, ref}]`＋`notes_label:`（rail 下段，`ref` 是靠右的藍色引用 tag）／
>   **`result: {math, reason}`＝答案框**（`reason` 是答案框右端的 mono tag 字，預設 `answer`）。
>   另有 `prompt:`（必填）、`number:`／`title:`（tagline）、`steps[]`／`check`、`part:`、`scaffold:`。
> - **reveal id：** `step.N`／`result`／`check`／`strategy`／`note.N`
>   （`strategy`／`note.N` 寫了 `{show …}` 才動態；`result` 恆動態）。
> - **masthead 是模板內自建**（D10），但**沿用 `example_head` 的五個 block id**
>   （`eyebrow`／`part`／`prompt`／`solrule`／`sollead`），所以 `sizecheck` 的 `HEADER` 集合與
>   `scene_spine` 找 `prompt` 都不用改；`_common.example_head` 本體一行未動。
> - **D14 已含完整的稽核模組清單**（`template_names`／`schema._worked_example_issues`＋`_seg_roles_issues`＋
>   與 derivation 共用的 `_row_anim_issues`／`step_coverage._SCOPED_TEMPLATES`／`provenance._present_text_fields`；
>   `pedagogy._MOTIVE_TEMPLATES` 與 `lint` 判定不加）——**T4-1 的「先列清單」交付物已由該分支完成**。
> - **`sizecheck._capacity_issues` 有一處配套改動**（子代理的契約外判斷，已覆核接受）：
>   **完全落在 `extra_bottom` 保留帶內的 block 不計入縱向堆疊**，否則答案框會被算兩次、每個有答案框的場都誤報拆頁；
>   溢出保留帶的列照算。證據＝22 個既有 deck 的 `sizecheck` 輸出逐字相同。
- §3.1 deck 統計：27 場＝`intro` 1／`divider` 4／**`content` 21**／`outro` 1；
  content 模板分布 `derivation` 6／`theorem_proof` 5／`graph` 4／`definition_math` 3／`callout` 2／`recap_cards` 1。
  `meta`：`fontfloor_enforce`／`coverage_enforce`／`otf_enforce`/`pedagogy_enforce` 皆 `True`，
  `color_map = {"\\theta": "strategy"}`，`example_coverage_enforce` 未設。

### 2.6 硬閘與零行為改變的證據做法（§4、§6 用）

- **層 6 sync guard 硬閘**：`pipeline/timing.py:18` `SYNC_HARD_GATE_FRAMES = 2`
  （render 後 ffprobe 實測每個 content 場長度，偏差 > 2 影格 → error、compose 前 abort；
  `SYNC_TOLERANCE_SECONDS = 0.12` `:11` 留給手改 manifest 的 beat 總和檢查）。契約在 `REVIEW_GATES.md:73`。
- **層 7 `[still-gate]` 硬閘**：`pipeline/rewatch_pack.py:415` `--gate-still` **預設 12.0、沒有關閉開關**；
  `:418` `--baseline <pack dir>` 比對來源 mp4 的 fps 與畫面尺寸，**不同或舊 pack 沒紀錄 → exit 2、什麼都不寫**
  （docstring `:14-20`）。只審 `content` 場、量 0.05% 細門檻的最長靜止。**不接進 `make.py`**，
  由輪次協定規定 render 後必跑（`REVIEW_GATES.md` §6.4）。
- **輪次協定** `REVIEW_GATES.md` §六：6.1 一輪＝收齊 must → 併行派工 → **一次 merge → 一次 render →
  一次再審**；6.2 輪內只跑回歸清單、**生成式盲審不跑**（里程碑才跑六鏡）；6.3 四條停止條件；
  6.4 開工清單；6.5 契約進測試（G6 紅測試先行）。
- **零行為改變的證據做法**（`REBUILD_STATUS.md` ⑦ 原文＝「18 個 deck 的 schema／lint／sizecheck
  報表逐字相同」＋`doctor --smoke`＋`run_selftests`）。**現在的正確指令：**
  ```bash
  python tools/doctor.py --smoke            # 正典 deck 的離線閘（schema＋provenance＋lint＋derive --check）
  python video/pipeline/run_selftests.py    # 42 支，manim-backed 的幾支要數分鐘
  ```
  **⚠ 在 git worktree 裡 `--smoke` 會整段跳過**（實測回報 `video-smoke [info] 略過：無 .venv`）——
  `.venv` 只在主 checkout（`C:/Users/Kao/Downloads/Calculus_handout/.venv`，gitignored）。
  worktree 內要跑，用主 checkout 的直譯器：
  `C:/Users/Kao/Downloads/Calculus_handout/.venv/Scripts/python.exe video/pipeline/run_selftests.py`
  （已實測可跑；`.deps`／`.deps_voiceover` 本機皆不存在，manim 直接裝在 venv 裡）。
  另：本機 `doctor` 另有一項既存 FAIL（`pdftotext` 是 xpdf 版不是 poppler 版，講義線用，
  §7.2 open item，**不是本輪造成的，不要順手修**）。
- §3.1 成片＝`video/output/ch03/s3.1/ch03_trig_derivatives_mimo.mp4`（~16.2 分、1080p、30 fps、21 content 場）。

---

## 3. 全域護欄（每個 task 都適用）

1. **紅測試先行（G6）。** 任何「本來就該成立」的行為，改之前先寫會紅的 selftest 再讓它綠
   （`REVIEW_GATES.md` §6.5、根 `CLAUDE.md` Karpathy §4）。`run_selftests.py` 全綠才算一個 task 完成。
2. **一個 task 一個 worktree 一個 commit；主對話只做審核＋merge。**
   worktree 開分支後先 `git merge main`（分支點可能落後）。子代理回報必須含：改了哪些檔、
   測試數字、沒做到的條款（根 `CLAUDE.md` 任務分派節）。
3. **不動任何 storyboard 的內容與旁白。** 四個 task 都是 code／模板層。
   `_demo_worked_example.yml`（T4 新增）與 T1／T2 為了看幀而改的**試點 deck 欄位**是唯二例外，
   且不得動 `say:` 一個字（旁白 LOCKED，NFA 不重開）。
4. **零計費。** 不碰 TTS（真旁白只走 `make.py --reuse-audio`）、不開 agy／Codex／VLM。
   本地 Manim render 與 subagent 稽核（`visual-frame-audit`）是免費的，可逕行。
5. **字型安裝要先徵詢（根 `CLAUDE.md`「缺套件／軟體先問」）。** T1 要下載 Instrument Sans 的
   OTF、要跑 `autoinst` 生字型、可能要 vendoring 進 repo——**這三件都要先說明「裝什麼／為什麼／
   怎麼裝」並等使用者同意**。使用者另有「下載前先問」的長期要求（佔網路頻寬）。
   裝完同一輪補齊 `ENVIRONMENT.md`（③／①b 兩列）、`tools/doctor.py`（新檢查項）、
   `requirements.lock`／`tools/setup.ps1`（若有 pip 面的東西）——**驗收＝新機 `doctor.py` 能對齊到全綠**。
6. **改共用層的證據＝兩份：**
   ① **意圖不變的 deck**：22 個 deck 的 `schema`／`lint`／`sizecheck` 報表**逐字相同**（diff 為空）；
   ② **意圖改變的 deck**：抽最終幀與 Phase 0 基線幀**並排對照**，逐條說明「這個差異是我要的」。
   只有 ① 沒有 ② 等於沒證明（⑬ 的教訓：selftest 全綠、五道閘全過，實心色塊仍是肉眼看出來的）。
7. **卡住就停。** §2 事實與實況不符、或設計撞上既有契約而需要改契約時，先寫下衝突再問使用者，
   不要默默繞。**T1 的 go／no-go 是本輪唯一的中途人閘**（§5 T1-5）。
8. **不碰別人的工作樹。** 開工先 `git status`；已被別的 session 改而非本 kickoff 的檔一律不動；
   `git add` 只加自己的路徑，**絕不 `git add -A` / `git commit -a`**。

---

## 4. Phase 0 — 基線（~40 分鐘，其中 render 0 次）

> 基線存 **repo 外**（例如 `%TEMP%\shared-layer-v1-baseline\`），不要進版控。
>
> **⚠ 數字已因 T4 併入而變**（2026-09-13）：**T4 併入 main 之後**重跑 Phase 0 的話，
> P0-1 是 **43/43**、P0-2 是 **23 個 deck**。下方寫的 42／22 是 T4 併入**之前**的基線
> （T4 自己的零行為改變證據就是對那份 22 deck 基線做的，66 份報表逐字相同）。
      `python tools/doctor.py --smoke` 9/9；**兩份 stdout 存成 `before-selftests.txt`／`before-smoke.txt`**。
      worktree 內跑不到 `--smoke` 時改在主 checkout 跑（§2.6）。
- [ ] **P0-2** **22 個 deck 的三份報表逐 deck 存底**（`before/<deck>.{schema,lint,sizecheck}.txt`）。
      一支一次性腳本跑完即可（寫進 scratchpad，不進版控）：
      `python video/pipeline/schema.py <yml>`、`python video/pipeline/lint.py <yml>`、
      `python video/pipeline/sizecheck.py <yml>`。
- [ ] **P0-3** 對 §3.1 成片跑 `python video/pipeline/rewatch_pack.py --deck ch03_trig_derivatives_mimo
      --out %TEMP%\shared-layer-v1-baseline\rewatch_pack_v0`。這包就是 §6 最後 A/B 的 `--baseline`
      （它記錄 fps 與畫面尺寸；§6 的 render 必須同 fps 同尺寸，否則 `--baseline` 直接 exit 2）。
- [ ] **P0-4** 抽三張基線幀留底（字體看 `theorem_proof` 場、字級看 `derivation` 場、例題看
      `companion_limit`），對象＝`video/output/ch03/s3.1/` 既有的 `mimo_fullest_frames/`；
      沒有就用 `critic.py --dry-run` 抽一次（離線免費）。這三張是 §6 人閘的 before。
- [ ] **P0-5** `git log -1 -- video/pipeline/visuals/theme.py video/pipeline/brand.py
      video/pipeline/sizecheck.py video/pipeline/templates/__init__.py` 確認 §2 行號仍對；漂了就 grep 更新本檔。

---

## 5. Tasks

> **順序＝T1 → T2 → T3，T4 可並行。** 理由：T1 改變**所有文字的度量**（`TEXT_SCALE`／`_WIDTH_K` 一動，
> 每一行 wrap 位置都可能變），所以字級（T2）必須對**最終字體**決定，`sizecheck` 的新規則（T3）
> 必須對**最終字級**校準。T4 動的是一個新檔，與 T1–T3 零重疊，可同時開發，**但最後要對 v1 的
> 字體字級回歸一次**。

### T1 — 字體換 Instrument Sans（先做；派 **opus**）

**為什麼先做：** 它是唯一會改變所有文字度量的一項。放在後面做＝T2 的字級與 T3 的閘門檻全部作廢重來。

- [ ] **T1-0 開工第一件事：把範圍與代價攤開給使用者，等回答。**（Karpathy §1，不要默默選一個）
  1. **mockup 的數學字體也換了**（`DirectionB.dc.html:14` `Source Serif 4`）。
     本 task 預設**只換文字（Instrument Sans），數學維持 Latin Modern**——理由是
     `PX_TO_FS` 是數學錨、換數學字體會連帶動所有版面 zone，且 `lmodern` 在 preamble 標了 locked。
     **要不要連數學一起換，請使用者裁決。**
  2. **裝什麼**：Instrument Sans 沒有 CTAN 的 pdflatex 套件（§2.1 實測），要
     ① 下載 OFL 的 OTF（Google Fonts）② 用本機已有的 `autoinst`／`otftotfm` 生 pdflatex 字型支援
     ③ vendoring 進 repo（比照 `handout/latex/template/fonts/inter/` 的 OTF＋LICENSE 做法）。
     **這三件都要先徵詢**（§3 護欄 5）。
  3. **退路**：使用者若不想動字型鏈，本機已有 CTAN 套件的 sans 候選是
     `sourcesanspro`／`firasans`／`raleway`（實測 `.sty` 都在），換字只要改 preamble 一行＋重校兩個常數。
     **把這個便宜選項講出來，不要自己決定。**
- [ ] **T1-1 preamble 切換。** 只改 `pipeline/_bootstrap.apply_tex_template()` 的 `:73-87`：
      `plex-sans` → 新字（`plex-mono` 的 eyebrow 是否同步換，一併在 T1-0 問）。
      **`lmodern`、`\familydefault=\sfdefault`、`microtype`、`\everymath{\displaystyle}`、
      三個 `\DeclareMathOperator` 一律不動。**
- [ ] **T1-2 重校兩個常數（不是一個）。** 照 `content_scripts/_audit/PLAN-routeA-plex-latex.md:98-120`
      Task 2 的量測配方（那是 Plex 上一次換字時用過的、已驗證的方法）：
      ```python
      # bootstrap()（已套新 preamble）之後：
      from manim import Tex
      fs = 100.0
      H = Tex(r'H').height / fs                        # 新字的 cap height per font_size
      s = 'A function is one-to-one when different inputs'
      w = Tex(s.replace(' ', r'\ ')).width             # \  保留空格寬
      w_per_char = w / (sum(0.5 if c == ' ' else 1 for c in s) * fs)

      # theme.TEXT_SCALE = round(0.006624 / (H * theme.PX_TO_FS), 4)
      #   推導：cap_height(u) = H * font_size 且 font_size = px * PX_TO_FS * TEXT_SCALE，
      #   要讓 cap_height/px 維持 0.006624（Times 錨），就得到上式。
      #   自我檢查：用 Plex 現值 H≈0.007243 代進去應該回到 1.3102。
      # brand._WIDTH_K  = round(w_per_char * 1.02, 5)  # 實量 + 2% 安全邊際（治 wrap 溢出）
      ```
      **不變式（T1 的驗收契約，寫進註解）：**
      ① `PX_TO_FS = 0.698` 不動（數學錨）；
      ② 換字後 `_text_fs(size)` 渲出來的 **cap height 仍是 0.006624 u/px**（→ 決定 `TEXT_SCALE`）；
      ③ `estimate_text_width` 必須**略高於**真實 advance（→ `_WIDTH_K` 的 +2%）。
      量測腳本寫進 scratchpad（一次性、量完刪，比照 Route A 的做法），量到的值與腳本輸出貼進 commit body。
- [ ] **T1-3 紅測試先行。** 新增 `pipeline/_selftest_text_metrics.py`：
      ① `Tex('H').height / 100.0 * TEXT_SCALE * PX_TO_FS` 落在 `0.006624 ± 2%`（cap height 不變式）；
      ② 對一組固定字串，`estimate_text_width(s, fs) >= Tex(s).width`（估寬不得低估，否則 wrap 溢出）；
      ③ `Tex` 真的用到新字族（查 preamble 字串即可，避免脆弱的 glyph 比對）。
      **先讓它在舊常數下紅（②會紅在新字上），再改常數讓它綠。**
- [ ] **T1-4 抽幀＋稽核。** 三場 mock render（`theorem_proof` 的 `continuity_statement_sin_limit`、
      `derivation` 的 `difference_quotient_for_sine`、`graph` 的 `squeeze_graph`），
      抽最終幀，派 `visual-frame-audit` subagent（免費 gate 1）看 V1–V10。
      **重點看 wrap**：`_WIDTH_K` 若校偏，最先炸的是 recap／annotation 的長行。
- [ ] **T1-5 go／no-go 人閘（本輪唯一中途停點）。** 三張新幀＋P0-4 的三張舊幀並排交使用者，
      **由使用者決定採用新字或退回 Plex**。
      **退回也要留下校準方法**：即使 no-go，T1-2 的量測腳本與 T1-3 的 selftest 留著
      （它們守的是「換字必須重校兩個常數」這條契約，與選哪個字無關），
      並把「Instrument Sans 需要 autoinst 生字型」這個事實寫進 §8 backlog 與 `ENVIRONMENT.md`。
- **改哪些檔：** `pipeline/_bootstrap.py`（preamble）、`pipeline/visuals/theme.py`（`TEXT_SCALE`）、
  `pipeline/brand.py`（`_WIDTH_K`）、`pipeline/_selftest_text_metrics.py`（新）、
  `ENVIRONMENT.md`／`tools/doctor.py`（若真的裝了字型）、`video/README.md` §文字渲染＋`DESIGN.md` §Text rendering（字族那句）。
- **不准動：** `PX_TO_FS`、`lmodern`、任何 storyboard、`MIN_FONT_FLOOR`、`_SCALE_PX`（那是 T2）。
- **零行為改變怎麼證明：** 這一項**不可能零行為改變**（換字必然改所有文字幾何）。
  證據改成：22 個 deck 的 `schema`／`lint` 報表逐字相同（結構沒動），
  `sizecheck` 的 **error 數必須仍為 0**，warn 的增減逐條解釋（wrap 位置變是預期的）。
- **DoD：** T1-3 綠、`run_selftests` 全綠、三場幀 `visual-frame-audit` 0 blocking、
  使用者在 T1-5 給出 go 或 no-go 且結果已落地、文檔同輪補齊。

### T2 — 數學字級收成三階＋取消 `math_sm 40`（對最終字體做；派 **opus**）

**規則來源**（`_audit/design-template-system/MathRules.dc.html` 規則 5 逐字）：
> 數學字級只有三階：**conclusion 62 px／body 48 px／rail·inline 34 px**。
> 取消 `math_sm 40` 這一階——實測它與 48 在螢幕上分不出來，只製造不一致。

- [ ] **T2-1 決定三階怎麼映射到 `_SCALE_PX`，寫進 commit body。** 現況 → 目標：
      結論 `derivation.py:136` 的 **raw `size=54` → 62**（並且**升成具名 token**，不要再 raw px）；
      body `math 48` 不動；rail/inline **`math_sm 40` → 34**。
      同時把兩個 A/B 開放值定死：**`prose_sm` 35→?（開放值 35 或 38）**、**`tag` 30→?（開放值 30 或 32）**
      ——使用者說的「放大併案」就是這兩個。34 這一階與 `prose_sm`／`tag` 的關係要在此講清楚
      （三者會不會撞成同一個數字？撞了就該合併成一個 token）。
- [ ] **T2-2 紅測試先行。** 擴充 `pipeline/_selftest_type_scale.py`（它已經在守 `statement` 階）：
      新增「數學階只有三個值」的斷言——把 `pipeline/templates/` 下所有
      `brand.math_line(..., size=X)` 與 `T.fs(X)` 的 `X` 收集起來，assert 它們落在三階
      ∪ `{MIN_FONT_FLOOR 相關的例外}`。**先讓它紅**（現況有 40／54／raw px 落單）。
- [ ] **T2-3 逐處改。** §2.2 列的 call site：`pipeline/` 內 7 處 `math_sm`（graph 5／theorem_proof 1／
      sign_chart 1／procedure_steps 2）、`prose_sm` 4 處、`tag` 4 處；
      `animations/` 內約 20 處（三個 hook 檔）。**`math_sm` 這個鍵要不要保留成 alias**：
      建議**不保留**（`_SCALE_PX` 已有一堆 back-compat alias，再加一個違反 Karpathy §2），
      改成刪掉 → 所有 call site 一次改完 → `KeyError` 就是編譯期的閘。
- [ ] **T2-4 `MIN_FONT_FLOOR` 關係要檢查。** floor 是 **26 px**；新的 rail 階 34 px 與
      `tag`／`eyebrow 26` 的距離變近。逐項確認：
      ① `derivation.py:382` 的 `floor_px = T._SCALE_PX["tag"] if result else _REASON_PX` 仍成立；
      ② `graph.py:406` 的 `default_label_size` 從 `math_sm`(40) 降到 34 之後，**曲線標籤仍 ≥ 刻度**
      （`graph.py:87,116,123` 的刻度尺寸），這是 P-A1 的既有契約；
      ③ 現有 `fontfloor_enforce: true` 的 §3.1 deck **不得新增任何 floor error**。
- [ ] **T2-5 會動到的 deck 與幀對照。** 用 `math_sm`／`prose_sm`／`tag` 的 deck＝
      `ch01_inverse_functions`、`ch03_trig_derivatives{,_mimo}`、`ch03_chain_rule`、
      以及 `_demo_graph_*`／`_demo_sign_chart`／`_demo_value_table`／`_demo_registers`／`_demo_aside`。
      **意圖改變**的 deck 全部抽最終幀與 P0-4／P0-2 的基線並排；
      **意圖不變**的（不含這三個 token 的 demo）報表必須逐字相同。
      特別看 `derivative_cycle`（場 18）——它的 `d/dx` 就是上一輪剛從 `label`(30) 升到 `math_sm`(40)
      才修好 blocking 的（`REBUILD_STATUS.md` ⑬），降到 34 要確認沒把它推回 floor 以下。
- **改哪些檔：** `pipeline/visuals/theme.py`（`_SCALE_PX`）、`pipeline/templates/{graph,theorem_proof,sign_chart,procedure_steps,derivation,_common,value_table}.py`、
  `animations/ch0*_hooks.py` ×3、`pipeline/_selftest_type_scale.py`、`DESIGN.md:1211` 型階表。
- **不准動：** `PX_TO_FS`／`TEXT_SCALE`（T1 已定）、`MIN_FONT_FLOOR`（動它要另案）、任何 storyboard 的 `say:`。
- **零行為改變怎麼證明：** 不含這三個 token 的 deck 報表逐字相同；含的 deck 逐場幀對照＋逐條說明。
- **DoD：** T2-2 綠、`run_selftests` 全綠、§3.1 deck `sizecheck` 0 error 且 floor warn 不增、
  幀對照交付、`DESIGN.md` 型階表同輪改對。

### T3 — 把版面 4 條／數學 5 條裡能自動的寫進 `sizecheck`（派 **opus**）

**第一步是分流，不是寫 code。** 逐條判「可自動／只能人審」，把判斷寫進 commit body 與 `REVIEW_GATES.md`。
下表是本檔作者的初判，**開工時要自己覆核**（規則原文在 `_audit/design-template-system/LayoutRules.dc.html`
的 `RULES` 陣列與 `MathRules.dc.html`）：

| # | 規則（原文摘要） | 畫布自帶的 check | 初判 |
|---|---|---|---|
| L1 | 結論必須是畫面上最重的元素（字級不得小於同場任何鋪陳元素，且必須帶語意色） | `assert fs(conclusion) >= max(fs(x) for x in scene.blocks)` | **可自動**，但要先解 §2.3 的盲點（結論多半是 `MathTex`，`_prose_nodes` 收不到）——用 `_effective_font_px` 走全樹 |
| L2 | 下三分之一不得長期空置（最滿幀 y>720 的墨覆蓋 > 0.15） | `assert ink_coverage(y > 720) > 0.15` | **可自動**（bbox 面積近似，不必真的量墨）；門檻要對 22 個 deck 校準到零誤報再上 |
| L3 | 右欄有條件展開（主內容寬 < 58% 時必須有 aside 或置中） | `if main_width < 0.58*W: require(aside or centered)` | **可自動**；`aside` 機制已存在（`_common.build_aside`），但 27 場沒人用過 → 會一次噴很多 warn，**必須 warn-default** |
| L4 | 三種佔比依章體質選（`single`／`major_minor`／`figure_led`） | `layout: single \| major_minor \| figure_led` | **只能人審**（這是 authoring 選擇，不是幾何事實）。可自動的只有「宣告了就要跟宣告一致」，但目前沒有這個欄位 → **本輪不做，進 §8** |
| M1 | 數學行內不得混入散文（說明進右側 rail） | — | **可自動**：`math_line` 的輸入含 `\text{}`／`\mbox{}`／連續兩個以上英文單字 → warn |
| M2 | 註解 rail 只有兩種語域（整段數學，或整段 sans small-caps） | — | **可自動**：一個 reason 欄位同時含 `$...$` 與裸英文 → warn |
| M3 | 正斜體照數學慣例（變數斜體；運算元／函數名／數字正體） | — | **半自動**：可查已知運算元名（`sin`/`cos`/`lim`/`max`/`log`…）有沒有寫成裸字母序列（少 `\`）→ warn。**完整的正斜體判斷只能人審** |
| M4 | ∎ 是字形不是元件（現在渲成綠色圓角方框） | — | **只能人審**（是 `brand.glyph("qed")` 的視覺做法問題，不是可量的幾何）→ 改法進 §8，或併進 T2 的字級輪一起看幀 |
| M5 | 數學字級只有三階 | — | **已由 T2 的 selftest 覆蓋**，不必再寫成 sizecheck 規則 |

- [ ] **T3-1 逐條分流定案**（上表覆核＋理由），寫進 commit body。**判「只能人審」的要說清楚為什麼**，
      並確認它在既有的判斷閘裡有家（VISUAL-FRAME 的 V／A 維度，或 pedagogy）。
- [ ] **T3-2 每條可自動的規則一個紅測試。** `pipeline/_selftest_layout_rules.py`（新）：
      每條規則一組 fixture（一個違反、一個不違反），**先紅再綠**。
      fixture 用 `storyboards/_fixtures/` 既有慣例，不要動正典 deck。
- [ ] **T3-3 實作，全部 warn-default ＋ 各自的 `meta.*_enforce`。**
      照 `pedagogy.assumptions_registry_issues` 的形狀（`sev = "error" if enforce else "warn"`，
      **沒宣告就回 `[]`**）。旗標名建議 `meta.layout_enforce`（L 系）與 `meta.mathtype_enforce`（M 系），
      比照 `fontfloor_enforce` 接在 `sizecheck.check_scenes` 尾段。
- [ ] **T3-4 校準到零誤報。** 對 22 個 deck 跑一遍，**每一條 warn 都要能說出「這是真的違反」**。
      說不出來的就是門檻錯了，改門檻不要改 deck。
- [ ] **T3-5 升硬閘要等一節驗證後。** 本輪**只上 warn-default**；
      `meta.<flag>_enforce: true` 由 §3.2 那一節開工時自己決定要不要開，
      開了跑完一節沒誤報，下一輪才考慮改預設。**不要在本輪把任何新規則設成預設 error。**
- **改哪些檔：** `pipeline/sizecheck.py`、`pipeline/_selftest_layout_rules.py`（新）、
  `storyboards/_fixtures/`（新 fixture）、`REVIEW_GATES.md` §一 層 6 的 `sizecheck` 列（新規則與旗標）、
  `DESIGN.md`（新規則契約）。
- **不准動：** 既有 11 項檢查的分級與門檻（`OVERLAP_FRAC`／`LABEL_OVERLAP_FRAC`／`TOLERANCE`／
  `MIN_FONT_FLOOR`）、任何正典 deck、`schema.py`。
- **零行為改變怎麼證明：** 22 個 deck 的 `sizecheck` **error 行逐字相同**（新規則全是 warn）；
  新 warn 逐條列出並說明。`schema`／`lint` 報表完全不動。
- **DoD：** 分流表定案、每條可自動規則一支紅→綠測試、22 deck 零誤報、
  `REVIEW_GATES.md` §一 `sizecheck` 列同輪更新、`run_selftests` 全綠。

### T4 — `worked_example` 新模板（可與 T1–T3 並行；派 **opus**）

> **狀態（2026-09-13 回寫）：T4-1～T4-4、T4-6 ✅ 已由分支 `claude/unruffled-antonelli-db3c3e`
> 完成並併入 main；T4-2 的 RUNBOOK「9 個 → 10 個」那句 ✅ 由本次併入的補缺 commit 補上；
> 只剩 T4-5 ⏳（等 T1／T2 merge 後做）。** 本小節以下的條文是**開工前**寫的，
> 部分敘述（欄位名 `factors:`／`answer:`、reveal id `factor.N`／`answer`）與落地不符——
> **一律以 §2.5 的回寫框、[`KICKOFF-worked-example-template.md`](KICKOFF-worked-example-template.md)
> D1–D14 與 §7 為準**，下方逐條已標注。

**契約（這是 T4 的成功標準，開工前先確認每一條都懂）：**

1. **storyboard 欄位要對得上講義的 `envexample` 結構**（§2.5）：題目（一句話，可帶 (a)(b)）＋
   解答（多步驟，每步有理由）＋收尾詮釋。
2. **要對得上 `examples:`／`folds:` 宣告**：`example_coverage.py` 的閘查的是內容稿 `.md` 的宣告，
   **不讀 storyboard**（docstring `:25-30` 明說，理由是場序是影片的事）。
   → **T4 不需要改 `example_coverage.py`**，但新 template 的場**應該**帶 `source:` 指回
   `Example N.N`（`lint._example_missing_prompt` 已在查 `derivation` 的這件事，新 template 要比照）。
3. **原語 1–7 適用**：1（`{show}`）／4（`focus:`）／5（`carry:`）／7（`paced:`）由
   `templates/__init__.build_blocks` 自動套用，新 template 不必做事（§2.4）；
   **2（`anim: transform`）與 3（`inset`／`frame`／`indicate`）要自己接**——
   解答步驟鏈是 `derivation` 的形狀，**應該直接重用 `derivation` 的 row 建構與 transform 機制**，
   不要另寫一套（Karpathy §2）。
4. **比現況多的只有三樣**（§2.5）：`strategy:` 策略卡、`factors:` 逐因子欄（含出處引用）、
   `answer:` 結論帶。現有的 `[ EXAMPLE ] ＋題目＋細線＋SOLUTION` 由 `_common.example_head` 供應，**照用**。
   → **落地更正（D10／D14）：** 欄位名是 **`notes:`**（不是 `factors:`）與 **`result:`**（不是 `answer:`）；
   masthead **在模板檔內自建**、只沿用 `example_head` 的五個 block id，`example_head` 本體未動。

- [x] **T4-1 先列清單，再寫 code。✅（分支已做，D14 就是那份清單）** 開工第一件事是把「**各稽核模組要不要改**」逐個列出來並判定，
      寫進 commit body。至少要看這幾個（每個都 grep 一次它有沒有 dispatch on `template`）：
      `pipeline/schema.py`（`:295-360` 有 `derivation`／`theorem_proof` 專屬檢查）、
      `pipeline/lint.py`（`:112-115` graph mode dispatch、`:241` derivation prompt、`:368` theorem statement）、
      `pipeline/sizecheck.py`（`SIBLING_PREFIXES` 要不要加新前綴）、
      `pipeline/pedagogy.py`、`pipeline/step_coverage.py`、`pipeline/provenance.py`、
      `pipeline/example_coverage.py`、`pipeline/critic.py`／`review_pack.py`／`rewatch_pack.py`。
      **判「不用改」的也要寫出來**，這份清單本身就是交付物。
- [x] **T4-2 registry 兩處同步 ＋ RUNBOOK 那句。✅**（registry 兩處＝分支 `c79372c`；
      RUNBOOK 那句＝本次併入的補缺 commit）
      `pipeline/templates/__init__.py` 的 `REGISTRY` ＋ `pipeline/template_names.py` 的
      `CONTENT_TEMPLATES`（否則 `_selftest_template_registry` 紅）；
      `RUNBOOK-mimo-narration-route.md:67` 的「全部 content template（9 個）」→ 10 個。
- [x] **T4-3 紅測試先行。✅**（`_selftest_worked_example.py`，28 支 assert）
      `pipeline/_selftest_worked_example.py`（新）：
      ① registry parity（既有 selftest 自動涵蓋）；
      ② 必填欄位缺了要有明確錯誤（不是 `KeyError`）；
      ③ `{show}` 目標 id 集合＝契約寫的那組（**落地＝`step.N`／`result`／`check`／`strategy`／`note.N`**，
      本行原寫的 `factor.N`／`answer` 是開工前的暫名）；
      ④ `result` 的字級 ≥ 同場任何 `step.N`（這條與 T3 的 L1 是同一條規則，**在這裡先自證**）。
- [x] **T4-4 `_demo_worked_example.yml` 回歸 deck。✅**（四場：完整形狀／`no_rail`／`capacity_over`／`multipage_p1`）
      用 `ex:3.1`（`companion_limit`，
      mockup 畫的就是它）當內容——**只放到 demo deck 裡，不要動 `ch03_trig_derivatives*.yml`**。
      它是第 23 個 deck，加進 §3/§6 的報表清單。
- [ ] **T4-5 最後對 v1 字體字級回歸。⏳（本輪唯一未完成的 T4 子項）** T1／T2 merge 之後，
      重跑 T4-3 與 demo deck 的三份報表＋抽幀，並跑 `visual-frame-audit`（免費 gate 1）；
      `result` 的 62 px 與 rail 的 34 px **目前是 `worked_example.py` 內的模板常數**（D6），
      **T2 要把它們升成 `theme._SCALE_PX` 的具名 token，模板改讀 token、不再自帶 raw px**。
- [x] **T4-6 文檔同輪。✅**（`DESIGN.md` Template catalog 一列＋專節＋Authoring Playbook 一列、`README.md`）
      `DESIGN.md` §Template catalog 加一列（教學形狀／payload 欄位／reveal target）＋
      `README.md` 模板段；`DESIGN.md:465` 的「Worked-example 題目結構」節要說清楚
      **`derivation` + `prompt:` 與 `worked_example` 的分工**（什麼時候用哪個；舊場要不要遷移——
      建議**不遷移**，`derivation` + `prompt:` 是合法的輕量形態，遷移是另一輪的事）。
- **改哪些檔：** `pipeline/templates/worked_example.py`（新）、`pipeline/templates/__init__.py`、
  `pipeline/template_names.py`、`pipeline/_selftest_worked_example.py`（新）、
  `storyboards/_demo_worked_example.yml`（新）、`DESIGN.md`、`README.md`、`RUNBOOK-mimo-narration-route.md`、
  ＋T4-1 清單判定要改的稽核模組。
- **不准動：** 任何正典 deck、`_common.example_head`（照用，不要改它的形狀）、
  `example_coverage.py`、`derivation.py` 的既有行為（可以 import 重用，不可改）。
  **落地例外（已覆核接受）：`sizecheck._capacity_issues` 改了一處保留帶規則**——見 §2.5 的回寫框。
- **零行為改變怎麼證明：** 22 個既有 deck 的三份報表逐字相同（新 template 沒人用＝零影響）；
  `_selftest_template_registry` 綠；新增的第 23 個 deck 自己的報表**除了刻意超量的 `capacity_over`
  壓測場之外 0 error**（實測 2 error／3 warn 全落在該場）。
  **✅ 併入 main 時複驗：66 份報表逐字相同、`_demo_worked_example` 2 error／3 warn 全在 `capacity_over`。**
- **DoD：** T4-1 清單交付 ✅、T4-3 綠 ✅、`run_selftests` 全綠（43 支）✅、demo deck mock render 過全部閘 ✅、
  `visual-frame-audit` 對 demo 幀 0 blocking ⏳（併 T4-5 一起做）、文檔同輪 ✅。

---

## 6. 驗收迴圈（四項 merge 之後，**全片只 render 一次**）

> `REVIEW_GATES.md` §6.1：一輪＝一次 merge → **一次 render** → 一次再審。
> **這次 render 同時就是 §3.1 的「v1 版成片」**——之後 §3.1 的 4K final 以它為準，不要為了驗收再多 render 一次。

1. **一次 render**：`python video/make.py --storyboard video/storyboards/ch03_trig_derivatives_mimo.yml
   --reuse-audio --quality high`（**不重 TTS**；`--reuse-audio` 讀既有 `audio_mimo/manifest.json`）。
   **render 前先確認 `tts.py` 不會被叫到**（`make.py` 本身只有 `--backend mock`，真音檔一律走 `--reuse-audio`）。
2. **兩道硬閘**（render 後必跑，§6.4）：
   - `[sync]`：`make.py` 內建，偏差 > `SYNC_HARD_GATE_FRAMES`(2) 就自己 abort。
   - `[still-gate]`：`python video/pipeline/rewatch_pack.py --deck ch03_trig_derivatives_mimo
     --gate-still 12 --out <新 pack> --baseline %TEMP%\shared-layer-v1-baseline\rewatch_pack_v0`。
     **fps／畫面尺寸與基線不同會 exit 2 什麼都不寫**——所以第 1 步的 `--quality high` 不能改。
3. **確定性閘**：`schema`／`lint`／`sizecheck` ——**正典 deck 0 error；`_demo_*` 壓測 fixture
   （`_demo_capacity`／`_demo_aside`／`_demo_multipage`／`_demo_tall_rows`，以及 T4 的
   `_demo_worked_example` 中刻意超量的 `capacity_over` 場）的刻意 error 要與 Phase 0 基線逐字相同**
   ——這些 fixture 存在的意義就是讓閘報錯，「0 error」對它們是錯的驗收標準；
   `python video/pipeline/run_selftests.py` 全綠；`python tools/doctor.py --smoke` 9/9；
   **23 個 deck 的三份報表對 Phase 0 做 diff**，逐條分類成「意圖不變＝必須逐字相同」與
   「意圖改變＝附幀對照」。
4. **`visual-frame-audit`（免費 gate 1）**：21 個 content 場的最終幀全跑，**blocking = 0**。
   首輪有 blocking 就修完**回歸再跑一次**（根 `CLAUDE.md`「finding 修完必須回歸審核」）。
5. **人閘（唯一停點）**：三場幀交使用者——**字體一場、字級一場、例題模板一場**
   （建議：`continuity_statement_sin_limit` 看字體／`difference_quotient_for_sine` 看字級／
   `_demo_worked_example` 看新模板），各附 Phase 0 的 before 幀。

> **生成式盲審（REWATCH 六鏡）本輪不跑**——`REVIEW_GATES.md` §6.2：輪內不跑，一節收斂時才跑。
> 本輪是工具線，不是一節的收斂。

---

## 7. 明確不做（本輪）

- **畫面語法缺口的 T2–T4**（[`KICKOFF-motion-language-gaps.md`](KICKOFF-motion-language-gaps.md) §8 的
  backlog：`{{}}` 段級 role、hook 自建 MathTex 不吃色表、palette 的 `accent`／`concept` 撞色、
  `play_block` 與 `STOCK_ANIM_SECONDS` 四處不一致）→ **進 §8 backlog**，
  除非 §3.2 開視覺時證明非做不可。
- **不改任何內容稿**（`content_scripts/*.md`）與任何 storyboard 的 `say:`。
- **不動 §3.2**。§3.2 雖已解凍，但它是**下一個 session** 的事（裁決 C：共用層凍結之後，
  先把 §3.2 串行走一遍）。本輪只保證共用層對 §3.2 是穩定的。
- **不做** 場間真 crossfade、鏡頭 zoom、`math_sm` 的 back-compat alias、
  `worked_example` 對既有 9 個 `derivation` + `prompt:` 場的遷移、
  版面規則 L4（`layout:` 佔比宣告欄位）、數學規則 M4（∎ 的視覺重做）。

---

## 8. Backlog（本檔查證時發現，不在本輪修）

- **`_SCALE_PX` 沒有 `result` token**，`derivation.py:136` 用 raw `size=54`；
  `DESIGN.md:1211` 的型階表卻把它列成一階。T2 會順手修掉（升成具名 token），
  但表裡的 `divider 92` 同樣是 alias（`intro_headline`）——表與 code 的對應關係值得整節重寫一次。
- **`sizecheck` 只看 `brand.prose`** 的盲點（`REVIEW_GATES.md` 層 6 已記）。T3 的 L1 會被它咬到；
  若 T3 為了 L1 做了「全樹 `_effective_font_px`」，**那是一個共用層改動**，
  應該考慮讓既有的 muted／floor 檢查也吃這條路（但不要在 T3 裡順手改，那違反外科手術原則）。
- **Instrument Sans 沒有 CTAN pdflatex 套件**（§2.1）。若 T1-5 是 no-go，
  這個事實要寫進 `ENVIRONMENT.md`，免得下一個人再查一次。
- **mockup 的數學字體是 Source Serif 4**（`DirectionB.dc.html:14`），與落地的 Latin Modern 不同。
  設計畫布與 code 之間的這個落差應該回寫進 `_audit/design-template-system/README.md` 的「已知限制」。
- **`RUNBOOK-mimo-narration-route.md:67` 寫死「9 個」**（2026-09-13 T4 併入時已改 10）——這種硬寫數字的地方值得全面掃一次
  （`REVIEW_GATES.md`／`README.md`／`REBUILD_STATUS.md` 裡的 deck 數、selftest 數同理；
  本檔 §2.4 已記錄「18 → 22」這個漂移）。
- **`meta.example_coverage_enforce` 未開**（§7.2 open item）。§3.2 開工時是自然的時機。
- **9 個既有 `derivation` + `prompt:` 例題場的遷移**（§3.1 四場、§3.2 五場）：
  等 `worked_example` 在一節跑順再議。

---

## 9. 完成定義（DoD）

1. **四項全部進 `main`**：T1（或 T1 的 no-go 結論＋校準方法留存）、T2、T3、T4 各一個 commit。
2. **文檔同輪補齊：**
   - `DESIGN.md`：§Template catalog 加 `worked_example` 一列、§Worked-example 題目結構說明兩者分工、
     §型階與量測表改成三階、§Text rendering 的字族。
   - `README.md`：模板段加 `worked_example`、§文字渲染的字族。
   - `REVIEW_GATES.md` §一 層 6 的 `sizecheck` 列：新規則與 `meta.*_enforce` 旗標。
   - `ENVIRONMENT.md`／`tools/doctor.py`／`requirements.lock`：**只在真的裝了字型時才動**。
   - `RUNBOOK-mimo-narration-route.md:67`：9 → 10。
   - `_audit/design-template-system/README.md`：四項的落地狀態（§7.1 那行「都還沒做」要改）。
3. **`REBUILD_STATUS.md` 記一條「共用層 v1 凍結」**（日期、四個 commit hash），
   並**明文宣告**：凍結後任何共用層改動一律走工具線（§1 的框內規則逐字抄過去）。
4. **驗收數字**：`run_selftests` 全綠（預期 **45 支＝43（已含 T4 的 `_selftest_worked_example`）＋T1＋T3**）、
   `doctor --smoke` 9/9、**23 deck `sizecheck`：正典 deck 0 error；`_demo_*` 壓測 fixture
   （含 `_demo_worked_example` 的 `capacity_over`）的刻意 error 與 Phase 0 基線逐字相同**、
   `[sync]` 0、`[still-gate]` PASS、`visual-frame-audit` 21 場 0 blocking、人閘通過。

### 預估（工時／render 次數）

| Task | 工時 | render 次數 |
|---|---|---|
| Phase 0 | ~40 min | 0（只跑閘與 pack） |
| T1 字體 | 半天～一天半（取決於 T1-0 走 CTAN 套件還是 `autoinst` 生字型；後者要加半天） | 3 場 mock ×1–2 輪 |
| T2 字級 | 半天（call site 約 35 處，但機械） | 5–8 場 mock ×1–2 輪 |
| T3 sizecheck | 一天（分流＋7 條規則＋22 deck 校準，校準最花時間） | 0（build-only，不 render） |
| T4 worked_example | 一天～一天半（新模板＋稽核模組清單＋demo deck） | demo deck mock ×2–3 輪 |
| §6 驗收 | 半天 | **§3.1 全片 1080p ×1**（`--reuse-audio`，不重 TTS） |

**全輪 render 預算：mock 若干（免費、快）＋ 1080p 全片 1 次。真 TTS 0 次、計費 API 0 次。**
