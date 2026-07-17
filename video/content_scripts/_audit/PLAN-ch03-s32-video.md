# §3.2 The Chain Rule 影片 實作計畫（ch03 · The Chain Rule）

> **For agentic workers:** REQUIRED SUB-SKILL — 用 `superpowers:subagent-driven-development`（建議）或 `superpowers:executing-plans` 逐 task 執行。步驟用 `- [ ]` 追蹤。
> **驗證模型（本產線特性，非 pytest）：** 內容稿階段靠 **gate-1 稽核 multi-agent Workflow（六鏡，免費）＋散文 copyedit（免費）＋使用者 sign-off**；工程階段（Stage 2，本輪不做）才靠離線抽幀＋確定性腳本（schema/lint/sizecheck）＋visual-frame-audit。每個會動內容的 task 以「編 HTML→讀／跑稽核」為驗證點。
> **計費紀律（CLAUDE.md）：** 全程離線／免費。任何計費呼叫（Codex gate-2、MiMo TTS、VLM critic）一律先停下、報價、徵使用者同意——本輪 Stage 1 **不含**任何計費步驟（見文末「計費閘（deferred）」）。

**本輪範圍（使用者裁決 2026-06-29）：** **只做 Stage 1（內容稿）** — 寫 content script → 編 narration HTML → 六鏡＋copyedit gate-1 → 使用者 sign-off → 鎖稿（LOCKED）就**暫停**。Stage 2（storyboard／hooks／render／視覺閘）達 sign-off 後**另徵範圍續做**（本檔文末保留 Stage 2 forward 大綱，不在本輪執行）。

**證明深度裁決（2026-06-29）：** Thm 3.3 的證明走 **full ε-δ 全展開**——忠實搬講義的餘項形式代入＋ε-δ 餘項估計，不壓縮；為畫面可讀切成 4 個 proof 單元（11–14）。

**Goal（本輪）：** 把講義 §3.2〈The Chain Rule〉做成一份與 §3.1 同級的 Stage 1 內容稿，到 **六鏡 blocking==0 ＋ copyedit 採納 ＋ 使用者 sign-off → LOCKED** 為止。

**Tech / 方法論：** 內容方法論 [`../../CONTENT_METHODOLOGY.md`](../../CONTENT_METHODOLOGY.md)（§1 硬規則、§2 scope、§3 拆解、§4 narration、§5 視覺、§6 格式、§7 checklist）；六鏡契約 [`CONTENT-SIXLENS-RUBRIC.md`](CONTENT-SIXLENS-RUBRIC.md)；copyedit 契約 [`NARRATION-COPYEDIT-RUBRIC.md`](NARRATION-COPYEDIT-RUBRIC.md)。

---

## 開工前必讀：現況與脈絡（新對話零脈絡也能照做）

- **倉庫：** 影片產線在 `video/`。**分支：續用 `video/template-redesign-navy-spine`**（不另開分支）。
- **講義輸入源（權威、忠實對象）：** [`../../../handout/html/fragments/ch03/sec-3-2.html`](../../../handout/html/fragments/ch03/sec-3-2.html)（建置版 `handout/html/standalone/chapter3-print-standalone.html` §3.2）。檔頭含編號契約：Thm 3.3（chain rule）、Prop 3.3（兩形式等價）、Def 3.1（餘項形式）、Ex 3.4–3.8、Fig 3.5（composed mapping）／3.6（remainder-tangent）、Remark 3.2（Leibniz）、Strategy 3.1（分解）、未編號 Caution。③ 決策 D5（Def 用 Option B：§2.2 極限定義不重編，只鑄餘項形式為 Def 3.1、等價為 Prop 3.3）、敘事 intuition-first、D6（積法則 §2.5／可微⇒連續 §2.3 Thm 2.1 引用不重證）、D7（ln／arcsin／x^x 留 §3.3）、D10（不做隱函數微分）。
- **格式範本（照抄結構與風格）：** [`../ch03_trig_derivatives.md`](../ch03_trig_derivatives.md)（§3.1 內容稿，LOCKED）＋其審核稿 [`../ch03_trig_derivatives_narration.html`](../ch03_trig_derivatives_narration.html)。
- **deck id：** `ch03_chain_rule`。**承接：** §3.1 outro 指向「3.2 The Chain Rule」；本節 intro 接續 §3.1（「sin x 會微，但 sin(x²) 不會」），outro 指向「3.3 Applications of the Chain Rule」。
- **§3.2 教學重量：** 概念＋符號混合，但證明段（Stage 2「Why」）符號吃重（餘項形式＋ε-δ）。整節**非 ≥70% 符號**（前有 statement/figure/strategy、後有 5 個例子），故**不套 §5 symbol-heavy 條件化**，但 Fig 3.5／3.6 兩張圖吃重、全視覺處理。

---

## 檔案結構（本輪會建/動到的）

- **建** [`../ch03_chain_rule.md`](../ch03_chain_rule.md) — Stage 1 內容稿（source of truth）。
- **建** [`../ch03_chain_rule_narration.html`](../ch03_chain_rule_narration.html) — 給使用者審核的可讀稿（每改 `.md` 重編）。
- **建** `video/pipeline/narration_review.py` — `.md → _narration.html` 生成器（reuse `review_pack.parse_content_script`，§3.1 未committed、本輪定版供 §3.2/3.3 沿用）。
- **建** `REVIEW-ch03_chain_rule-applied.html` — 完成一輪後的 HTML 報告（逐單元旁白＋locus＋六鏡/copyedit 裁決）。
- **動** [`../../REBUILD_STATUS.md`](../../REBUILD_STATUS.md) — 完成後新增一節記 Stage 1 進度錨。

---

## §3.2 教學單元規格（locked design 2026-06-29；narration 於 T1–T4 撰寫、T6 稽核）

> 每單元 `narration` 是 T1–T4 的產出、T6 六鏡稽核的對象。忠實護欄＝下表「必載數學」欄：narration 可口語重寫措辭，但不得增刪/竄改該欄數學（CONTENT_METHODOLOGY §1 硬規則）。intro/outro 無 narration（純動畫）。Stage divider 是 Stage 2 storyboard 的結構元素，**不在內容稿**（此處列出僅供 Stage 2 參考）。⚙️＝需客製 hook（cue 於本輪寫，code 留 Stage 2）。

**meta：** id=`ch03_chain_rule`、chapter=`Chapter 3`、chapter_title=`Chain Rule and Trigonometric Derivatives`、section=`3.2`、title=`The Chain Rule`、sections 清單＝3.1/3.2/3.3、tagline=`Why do the slopes multiply?`。

### Act 1 — The Rule You Can Use（statement 先給，證明留 Act 2）

| # | id | kind | source（sec-3-2.html） | 必載數學 / 視覺需求 |
|---|---|---|---|---|
| — | intro | — | Section Gate（定位） | Chapter 3 map → 聚焦 §3.2；tagline |
| 1 | why_composition_is_missing | motivation | 開節 para 1 | 能微分 `sin x`，搆不到 `sin(x²)`、`√(1+x²)`；Ch2 有和/積/商、缺 composition；連鎖律補洞、完成工具箱 |
| 2 | rates_multiply_intuition | motivation | 開節 para 2 | 可微函數近處≈切線（把 Δinput 乘斜率，誤差更快縮）；串兩個：g 把 h 放大 `g'(x)`、f 再放大 `f'(g(x))` → 疊乘 → 複合把 h 乘 `f'(g(x))g'(x)` |
| 3 | chain_rule_statement | theorem | Theorem 3.3 | g 在 x₀ 可微、f 在 g(x₀) 可微 ⇒ `P=f∘g` 在 x₀ 可微，`P'(x₀)=f'(g(x₀))g'(x₀)`（證明留 Act 2）|
| 4 | composed_mapping_figure ⚙️ | visual | Figure 3.5 | 增量 h 在 x₀ → g 帶到 ≈`g'(x₀)h` 於 u₀=g(x₀) → f 帶到 ≈`f'(g(x₀))g'(x₀)h` 於 y₀；兩局部斜率相乘 |
| 5 | leibniz_form | proposition | Remark 3.2（具名：Leibniz form）| `dy/dx = dy/du·du/dx`；唸法「rate of y per x = (y per u)(u per x)」；「du 約掉」是記憶法**不是**證明（dy/du、du/dx 是極限非分數）|
| 6 | decomposition_strategy | procedure | Strategy 3.1 | 由外而內：①最外層運算＝外函數 f ②裡頭＝內函數 u=g(x) ③作 `f'(g(x))`（內部當整塊）④乘 `g'(x)` ⑤裡頭還是複合就重複；每層一斜率因子、相乘。例 `√(1+x²)`→f=√,g=1+x²；`sin(x²)`→外 sin 內 x² |

### Act 2 — Why the Rule Is True（餘項形式 → 等價 → full ε-δ 證明）

| # | id | kind | source | 必載數學 / 視覺需求 |
|---|---|---|---|---|
| 7 | proof_strategy_bridge | motivation | "Why the rule is true" 引文＋para before proof | 規則已可用；要證兩斜率相乘需同時握住兩線性逼近 → 把「可微」改寫成餘項形式。（折入開節 para 3：借用積法則 §2.5、可微⇒連續 §2.3 為既定）|
| 8 | remainder_form_definition | definition | Definition 3.1 ＋ informal gloss | `f(x₀+h)=f(x₀)+mh+R(h)`, `lim_{h→0}R(h)/h=0`；m=f'(x₀)。直覺：切線值＋比 h 更快消失的誤差 |
| 9 | remainder_tangent_figure ⚙️ | visual | Figure 3.6 | 曲線（實）貼切線（虛）；x₀+h 處垂直間隙＝R(h)；h 減半→間隙縮得遠比 h 快（`R(h)/h→0` 幾何）；此為 Fig 3.5 背後單函數事實 |
| 10 | two_forms_equivalent | proposition | Proposition 3.3 ＋ Proof | 極限形式(§2.2)⇔餘項形式，同一 m。(⇒) 設 `R(h)=f(x₀+h)−f(x₀)−mh`，`R(h)/h=`差分商−m→0；(⇐) 除以 h：差分商=m+R(h)/h→m |
| 11 | proof_setup_substitution | proof | Thm 3.3 Proof ① | g 餘項：`g(x₀+h)=g(x₀)+m₁h+R₁(h)`；對 f 用餘項形式（增量=m₁h+R₁(h)）：`P(x₀+h)=f(g(x₀))+m₂[m₁h+R₁(h)]+R₂(m₁h+R₁(h))`；收線性項、其餘併 R₃ → `P(x₀+h)=P(x₀)+(g'(x₀)f'(g(x₀)))h+R₃(h)`，`R₃=m₂R₁(h)+R₂(m₁h+R₁(h))`；剩證 R₃/h→0 |
| 12 | proof_easy_piece | proof | Thm 3.3 Proof ② | 拆 `R₃/h = m₂·R₁(h)/h + R₂(m₁h+R₁(h))/h`；第一塊：m₂ 常數、R₁(h)/h→0 ⇒→0。並記 `m₁h+R₁(h)→0` |
| 13 | proof_delicate_choices | proof | Thm 3.3 Proof ③ | 棘手塊 ε-δ：固定 ε>0；(i) R₂(y)/y→0 ⇒ ∃δ：`0<\|y\|<δ ⇒ \|R₂(y)/y\|<ε`；(ii) m₁h+R₁(h)→0 ⇒ ∃α：`0<\|h\|<α ⇒ \|m₁h+R₁(h)\|<δ`；零情形 R₂(0)=0 ⇒ 商=0 |
| 14 | proof_delicate_bound | proof | Thm 3.3 Proof ④ | 非零時 `\|R₂(·)\|/\|h\| = (\|m₁h+R₁(h)\|/\|h\|)·(\|R₂(·)\|/\|m₁h+R₁(h)\|)`；第二因子<ε，第一因子=`\|m₁+R₁(h)/h\|≤\|m₁\|+\|R₁(h)\|/\|h\|`；取 α₁ 使 R₁/h<1 →`<(\|m₁\|+1)ε`；ε 任意 ⇒→0。合併 R₃/h→0，連鎖律成立 |

### Act 3 — Using the Rule（5 個不同模式例子＋頭號 caution）

| # | id | kind | source | 必載數學 / 視覺需求 |
|---|---|---|---|---|
| 15 | example_single_composition | example | Example 3.4 (a)(b) | (a) `√(1+x²)`：f=u^{1/2},g=1+x² → `1/(2√(1+x²))·2x = x/√(1+x²)`；(b) `sin(x²)`：`cos(x²)·2x = 2x cos(x²)`。2x＝內導數 |
| 16 | caution_inner_derivative | counterexample | Caution | 頭號錯＝漏內導數：`d/dx sin(g(x))=cos(g(x))` ✗，正解 `cos(g(x))·g'(x)`；g'(x)（sin(x²) 的 2x）永遠不可省 |
| 17 | example_nested_three_layers | example | Example 3.5 | `√(1+sin²x)` 三層：`1/(2√(1+sin²x))·2 sin x·cos x = sin x cos x/√(1+sin²x)`；每層一因子（½u^{-1/2}、2sin x、cos x）相乘 |
| 18 | example_chain_times_quotient | example | Example 3.6 | `√((x−1)/(x+2))`, x>1：外√、內商；內導＝商法則 `3/(x+2)²`；`1/(2√…)=√(x+2)/(2√(x−1))` → `3/(2√(x−1)(x+2)^{3/2})`。內導本身是個小問題 |
| 19 | example_chain_times_product | example | Example 3.7 | `(1+x²)cos²x`：先積法則 `(2x)cos²x+(1+x²)d/dx(cos²x)`；`cos²x=[cos x]²` 鏈式 `2cos x(−sin x)=−2 sin x cos x`；`y'=2x cos²x−2(1+x²)sin x cos x` |
| 20 | example_leibniz_rates | example | Example 3.8 | 海獺/海膽/海帶：`dK/dU<0`、`dU/dO<0`；`dK/dO=dK/dU·dU/dO`；負×負=正 ⇒ `dK/dO>0`。符號沿鏈相乘（Remark 3.2）|
| 21 | toward_section_3_3 | forward_ref | 收尾散文 | 工具箱基本完成；連鎖律解鎖新導數：反函數 `ln x`、`arcsin x`、`arctan x`，及對數微分下的 `x^x`。**MUST NOT 報節號** |
| 22 | recap | recap | 全節綜整 | `P'=f'(g(x))g'(x)`；Leibniz `dy/dx=dy/du·du/dx`；由外而內、斜率相乘；頭號陷阱＝內導數；餘項形式證明（局部線性逼近相乘）|
| — | outro | — | — | next_section "3.3" / next_title "Applications of the Chain Rule" |

**可折疊／就近註記（執行時若 narration 過載/過短再裁決）：** Ex 3.6 與 3.7 同屬「連鎖律＋另一條規則協作」，第二個套 §4 repeat-pattern 省 setup（不重述「outer/inner」框架）；若整體過長，Ex 3.6 或 3.7 之一可降為一句帶過（保一個代表＋註明折疊哪個、為何）。開節 para 3「借用工具」折入 unit 7、不獨立成場、不 silent drop。

---

## Tasks（Stage 1）

### Task 0 — 前置與範本就位
- [ ] 確認分支 `video/template-redesign-navy-spine`、工作樹狀態：`git status`。
- [ ] 通讀 [`sec-3-2.html`](../../../handout/html/fragments/ch03/sec-3-2.html) 與 §3.1 內容稿範本（已讀）。
- **驗證點：** 範本可讀、§3.2 編號契約掌握。

### Task 1 — 內容稿：header＋meta＋intro＋Act 1（units 1–6）
**Files:** Create [`../ch03_chain_rule.md`](../ch03_chain_rule.md)
- [ ] 寫檔頭（比照 §3.1：產線/權威來源/這是什麼/階段=DRAFT）＋ `## meta`（上表 meta 欄位＋節次清單）。
- [ ] 寫 intro（純動畫）＋ units 1–6 完整欄位（id/source/learning_goal/kind/narration/visual_need/animation_cue）。narration 依 §4：口語、3–7 句、hook→body→takeaway、數學直讀 LaTeX、對齊鏈不重念 LHS。
- **驗證點：** 通讀 narration、未犯 §4 禁則（不念標題/不報節號/不用 see/as shown）。

### Task 2 — 內容稿：Act 2（units 7–14，full ε-δ 證明）
**Files:** Modify `ch03_chain_rule.md`
- [ ] 寫 units 7–14。proof 單元（11–14）忠實逐步搬餘項形式代入＋ε-δ；narration 走「把每步講出來」、visual_need 逐行列承載步驟（含理由）。
- [ ] equivalence（10）走雙向短證；proof 切 4 場讓 ε-δ 可讀。
- **驗證點：** Def 3.1／Prop 3.3／Thm 3.3 各有覆蓋；證明每行可回溯講義；無 silent drop。

### Task 3 — 內容稿：Act 3（units 15–20）
**Files:** Modify `ch03_chain_rule.md`
- [ ] 寫 5 個例子＋caution。Ex 3.6/3.7 第二個套 repeat-pattern；caution 緊接 Ex 3.4 的內導數陷阱。
- **驗證點：** 每個不同模式 example 有代表單元；折疊就近註明。

### Task 4 — 內容稿：forward_ref＋recap＋outro（units 21–22＋outro）
**Files:** Modify `ch03_chain_rule.md`
- [ ] toward_section_3_3 forward-pointing、**MUST NOT 報節號**；recap takeaway 清單（5 點）；outro meta（next 3.3）記於 meta（outro 無 narration）。
- [ ] 收尾 `## §7 拆解註記與內容層品質檢核` 段（fold 決策、視覺盤點、checklist）。
- **驗證點：** recap 有 takeaway；§7 註記齊備、checklist 就位（待跑項 `- [ ]`）。

### Task 5 — 生成器＋編 `_narration.html` 審核稿
**Files:** Create `video/pipeline/narration_review.py`；Create `ch03_chain_rule_narration.html`
- [ ] 寫 `narration_review.py`：import `review_pack.parse_content_script`，讀 `.md` meta＋units → 產 standalone HTML（MathJax CDN，逐單元 narration＋可展開 source/goal/visual/animation），版型比照 §3.1 `_narration.html`。
- [ ] 跑生成器產出 HTML；通讀整份 narration（任何一段像教科書 → 重寫 `.md`、重編）。
- **驗證點：** HTML 雙擊即開、數學渲染正確、與 `.md` narration 一致。

### Task 6 — 六鏡對抗式稽核（gate-1，免費 Workflow）→ blocking==0
**Files:** Modify `.md`（依裁決）；裁決紀錄入報告。
- [ ] 跑六鏡 multi-agent Workflow（SSOT [`CONTENT-SIXLENS-RUBRIC.md`](CONTENT-SIXLENS-RUBRIC.md)）：L1 忠實／L2 拆解／L3 語域／L4 不重複／**L5 數學正確（對每個 example/proof 獨立隔離盲算）**／L6 完整；refute-by-default、每條過四級、Claude 逐條複驗。
- [ ] 對每條 blocking 外科式修 `.md`、**回歸再審**改動項（CLAUDE.md meta-rule）、重編 HTML。
- **驗證點：** 六鏡 **blocking==0**（advisory 逐筆人裁）。L5 對 §3.2 尤關鍵（ε-δ 估計、商/積/鏈協作、符號正負號易錯）。

### Task 7 — 散文 copyedit pass（gate-1，免費）→ tighten
**Files:** Modify `.md`（lock 前唯一改措辭窗口）。
- [ ] 跑 `narration-copyedit` subagent（SSOT [`NARRATION-COPYEDIT-RUBRIC.md`](NARRATION-COPYEDIT-RUBRIC.md)）：C1–C5。硬護欄：語義不得改。
- [ ] 採納 tighten、重編 HTML。
- **驗證點：** 冗餘/贅字在 lock 前清掉。

### Task 8 — HTML 報告＋使用者 sign-off＋鎖稿
**Files:** Create `REVIEW-ch03_chain_rule-applied.html`；Modify `.md`（DRAFT→LOCKED）；Modify `REBUILD_STATUS.md`。
- [ ] 產 self-contained HTML 報告（逐單元旁白＋locus＋`[source:]`＋六鏡/copyedit 裁決），比照 [`REVIEW-ch03_trig_derivatives-applied.html`](REVIEW-ch03_trig_derivatives-applied.html)。
- [ ] 交付 `_narration.html` ＋報告給使用者審核旁白。**等使用者明確認可。**
- [ ] 認可後 `.md` 階段標記改 LOCKED、設 `CONTENT_APPROVED`；`REBUILD_STATUS.md` 記 Stage 1 進度錨。
- **驗證點：** 使用者書面認可；source 自此凍結（後續 NFA 唯讀；post-lock 改稿走 scoped NFA 回歸）。

---

## 收斂定義（本輪「做完」）

Stage 1 完成 ＝ 內容稿六鏡 blocking==0 ＋ copyedit 採納 ＋ `_narration.html`／報告就位 ＋ 使用者 sign-off → `.md` LOCKED ＋ REBUILD_STATUS 進度錨。

## Stage 2（deferred — 達 Stage 1 sign-off 後另徵範圍才做）

storyboard 骨架（meta＋intro/dividers/outro＋stock 場景）→ 客製 hook ①`composed_mapping`（Fig 3.5）②`remainder_tangent`（Fig 3.6）→ schema/lint/sizecheck 三閘 → 全片 mock render（1080p）→ visual-frame-audit gate-1 blocking==0 → HTML 報告。比照 §3.1 PLAN Task 9–16。

## 計費閘（deferred — 達 mock 里程碑後、各自單獨報價徵同意才跑）

spoken derive＋NFA（MiMo 路線）／MiMo TTS 合成（計費）／Codex gate-2（計費，copyedit 近定稿時單次）／VLM critic gate-2（需同意）。
