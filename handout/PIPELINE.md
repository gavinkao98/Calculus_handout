# 完成一章的閘序（HTML 講義 chapter lifecycle）

> **本檔是什麼：** 把一章講義從 spine 素材（手稿或 canon 藍本）推到「定稿」要經過的**完整閘序**之**權威總覽**，兼任**各章狀態 dashboard**。
> 各閘的細節規格不在此重複——本檔給「順序、各閘用什麼、哪裡停下、產出什麼」，細節指向既有 sub-doc。
> 撰稿模式（Mode A／B／C、兩種變體）以 [`../CONTENT_AUTHORING_WORKFLOW.md`](../CONTENT_AUTHORING_WORKFLOW.md) 為準；內容撰寫規則以 [`../CONTENT_SPEC.md`](../CONTENT_SPEC.md) 為準；改課文只改 `fragments/`、再 `python build.py ch{NN}`（見 [`README.md`](README.md)）。

## 「做完一章」的定義

= **與 Ch1–Ch4 同級全跑，共七個閘家族**：
**Mode A（六階定稿）＋ Mode C gap-check ＋ 數學正確性 ＋ 圖機會／圖正確性 ＋ 去 AI 味 S·A·V ＋ 難度閘（learner-sim）＋ 收尾 dashboard 更新。**
（Ch1–Ch4 依手稿時代 gate 0–8 全跑完成，含 2026-07-03 補跑的難度閘；權威敘述見 [`../CONTENT_ROADMAP.md`](../CONTENT_ROADMAP.md) 各章 status 與 [`_audit/REVIEW-ch01-ch04-difficulty-mitigation-applied.html`](_audit/REVIEW-ch01-ch04-difficulty-mitigation-applied.html)。）

## 兩軌閘序（2026-07-07 起）

- **手稿章（Ch1–4，既成）**：原 gate 0–8 閘序已全數跑完，本檔尾端的 dashboard 記其狀態；該閘序的歷史細節見 git 歷史版 PIPELINE 與各章 `_dev-archive/ch{NN}/PLAN-ch{NN}.md`。
- **canon 章（Ch5 起，預設）**：採下方 **5-milestone 閘序**。Ch5 為過渡章——Mode A 已按 M1 完成（[`_dev-archive/ch05/PLAN-ch05.md`](_dev-archive/ch05/PLAN-ch05.md)），剩餘閘照 M2–M5 收。

## Canon 章 5-milestone 閘序（Ch6+ 預設；Ch6 為首個全程試點章，跑完一章後回顧定版）

| # | Milestone | 做什麼 | gate-1（Claude，免費） | gate-2（計費） | ⛳ 使用者停點 | 產物 | 權威 sub-doc |
|---|---|---|---|---|---|---|---|
| M1 | **Mode A′（canon 草擬）** | 章層 canon 盤點 → 逐節：brief（含例題計畫、軟深度計畫、`figure_opportunities`）→ 擴寫 → Codex ⑤（direction-conformance＋數學＋hypothesis hygiene）至 0 blocking → 章層收尾 sweep：**sympy 全例重算＋hypothesis ledger 覆核＋章層 Codex review（明列對應 M1–M8 各維，不可只稱「已吸收」）** | 各節 ④；章層 sweep | Codex ⑤（每節）＋章層 review（standing consent 內） | 章完成後過目 `REVIEW-ch{NN}-applied.html` | `sec-{N}.html`＋章 opener＋PLAN-ch{NN} ledger | [`../CONTENT_AUTHORING_WORKFLOW.md`](../CONTENT_AUTHORING_WORKFLOW.md)、[`../CONTENT_DIRECTION.md`](../CONTENT_DIRECTION.md)、[`_audit/MATH-CORRECTNESS-RUBRIC.md`](_audit/MATH-CORRECTNESS-RUBRIC.md)（M1–M8 維度定義） |
| M2 | **圖批次** | brief／擴增稽核第 7 項產出的候選 → 裁決「畫哪些」→ 繪圖（fragment＋FIGS 兩處同改）→ 圖正確性 D1–D8 | `handout-figure-opportunity-audit`（候選覆核）；`handout-figure-audit`（吃 `shot.mjs` 圖 PNG） | Codex 視覺第二讀者（`-i` 餵 PNG）——每章必跑，批次見「gate-2 全跑」 | **章批次裁決畫哪些**＋修法裁決 | `REVIEW-ch{NN}-figure-opportunity.html`、`REVIEW-ch{NN}-figure-audit.html` | [`_audit/FIGURE-OPPORTUNITY-RUBRIC.md`](_audit/FIGURE-OPPORTUNITY-RUBRIC.md)、[`_audit/FIGURE-AUDIT-RUBRIC.md`](_audit/FIGURE-AUDIT-RUBRIC.md) |
| M3 | **散文＋難度合一輪** | S·A·V 散文閘（三維：易懂 A／流暢 B／語意聲音 C）與 **≥3 份盲測 learner-sim**（盲測性質不可犧牲）同批跑，產**一份合併裁決稿** | `handout-prose-audit`＋`learner-sim` subagents | Codex prose S·A·V 複核——每章必跑，批次見「gate-2 全跑」 | 逐條裁決（一次） | `REVIEW-ch{NN}-prose-difficulty.html`（合併稿） | [`_audit/PROSE-AUDIT-RUBRIC.md`](_audit/PROSE-AUDIT-RUBRIC.md)、[`../CONTENT_SPEC.md`](../CONTENT_SPEC.md) §16、[`../.claude/agents/learner-sim.md`](../.claude/agents/learner-sim.md) |
| M4 | **Mode C 條件式 gap-check** | 單輪偵察（①補例＋②軟深度合一）；brief 覆蓋完整即記錄後跳過；有增補 → 必接範圍限定 Mode B | `mode-c-gapwalk`＋`example-supplement` | 選題稽核（僅動用題庫時） | 裁決補哪些 | `REVIEW-ch{NN}-modec-gapcheck.html`（單稿） | [`../CONTENT_AUTHORING_WORKFLOW.md`](../CONTENT_AUTHORING_WORKFLOW.md) §Mode C、[`../CONTENT_SOURCING.md`](../CONTENT_SOURCING.md) |
| M5 | **收尾** | dashboard 更新＋PLAN-ch{NN} 閘家族 checklist 補滿＋ROADMAP entry 收 Open questions | — | — | 確認 | 本檔 dashboard＋PLAN checklist | [`../CONTENT_ROADMAP.md`](../CONTENT_ROADMAP.md) |

> **順序不是死管線**：M2–M4 互相大致獨立，可依素材備妥程度調換；M4 宜在 M3 之前或同批（新增內容一併被散文／難度閘審到）——若 M4 在 M3 後補了內容，對增補部分補跑 scoped M3。每個 ⛳ 停下等使用者裁決。
> **三閘 gate-2 統一在 M4 之後、M5 之前批次跑**（不在各自 milestone 跑），確保覆蓋 M4 增補——每章必跑、不抽樣，見下方「gate-2 全跑」。

### gate-2 全跑：三閘每章必跑到定版（2026-07-10 使用者拍板，取代原風險分層）

**三個 gate-2（數學 M1–M8／散文 S·A·V／圖視覺）一律每章必跑到 0 blocking，該章才定版——取消「按章深度抽樣」「高風險才跑」「出版前抽樣」等所有分層與風險判斷。** 定案理由：Codex gate-2 走訂閱配額、邊際金錢≈0，分層省的只是配額／時間，卻要把 gate-2 延後＝章節不真正定版、出版前得回頭改已完成章（context 重載＋編號 cascade＋回歸滾雪球）；使用者取「心智負擔歸零＋章內不留 gate-2 債」，接受代價（散文／圖配額用在邊際較低處、潛在文風 churn）。gpt-5.5＋xhigh 對抗曾傾向「數學必跑＋散文／圖觸發式」的 A 案，使用者權衡後改採三閘全跑 B 案（詳見本次 commit body）。

- **統一位置＝M4 之後、M5 之前**跑「定版前跨模型複核批次」。理由：M4（Mode C gap-check）可能新增 example／caution／軟深度，動到編號與數學——**Ch5 的 [M7] blocking 正是 M4 新增的 caution**，數學 gate-2 若停在 M1 就會漏掉它；三閘一起在 M4 後跑，才覆蓋得到全部 as-built。
- **數學 M1–M8 gate-2**：Codex 依 [`_audit/MATH-CORRECTNESS-RUBRIC.md`](_audit/MATH-CORRECTNESS-RUBRIC.md) 全章複核。
- **散文 S·A·V gate-2**：Codex 依 [`_audit/PROSE-AUDIT-RUBRIC.md`](_audit/PROSE-AUDIT-RUBRIC.md) 全章複核（易懂性 blocking 主錨仍是 M3 的 learner-sim 盲測，見下節「易懂性單一錨」；S·A·V gate-2 為第二模型補充，非主錨）。
- **圖視覺 gate-2**：Codex 視覺第二讀者（`-i` 餵 render 後 PNG）。
- 實測成本參考：Ch4 數學 gate-2＝173,720 tok、S·A·V gate-2＝154,714 tok；一章三閘約 400–450k tok。撞額度牆時**分批／跨 session 跑，但都在該章定版前收完**（分批 ≠ 延後到出版前）。

### 易懂性單一錨（2026-07-07 與 Codex 收斂；取代三軌並行）

- **blocking 主證據＝M3 的 learner-sim 盲測**（stuck＝blocking；B 類先備違規＝blocking，可先 grep 機械預檢）。
- **S·A·V 維度 A 降為上游預篩**——其 findings 作為 sim 的觀察重點輸入；但 **U1–U4 類客觀缺陷（術語先用後定義、未解釋的邏輯跳躍等）prose gate 仍可直接判 blocking，不必等 sim**。
- 歷史上的獨立 readability 輪（`REVIEW-ch0{1..4}-readability-*.html`）對新章**停用**，其功能由本錨吸收。

## Mode C 兩波（scoped 定義保留，canon 章合一輪跑）

「Mode C 充實」的兩波定義不變（裁決與產物分開記時仍用）：**①波 補題目＝worked example**（[`../CONTENT_SOURCING.md`](../CONTENT_SOURCING.md)；subagent [`../.claude/agents/example-supplement.md`](../.claude/agents/example-supplement.md)）；**②波 軟深度**＝intuition/caution/application/strategy/summary/history（subagent [`../.claude/agents/mode-c-gapwalk.md`](../.claude/agents/mode-c-gapwalk.md)）。
兩波都標 `<!-- expansion:<cat> [pass: enrichment] [source: …] -->`（`[pass:]` 在 `[source:]` 前），且**都必接範圍限定的 Mode B**（[`../CONTENT_AUTHORING_WORKFLOW.md`](../CONTENT_AUTHORING_WORKFLOW.md) 硬規則）。
**canon 章（M4）合成單輪偵察、產單一裁決稿**；手稿章的既成紀錄仍是兩波兩稿（Ch1–4）。

## 難度閘（learner-sim；2026-07-03 新增，M3 的一半）

源起與首次全流程執行紀錄：[`_audit/REVIEW-ch01-ch04-difficulty-mitigation-applied.html`](_audit/REVIEW-ch01-ch04-difficulty-mitigation-applied.html)（Ch1–Ch4 難度評估＋修補＋複驗三輪；新章產物併入 M3 合併稿 `REVIEW-ch{NN}-prose-difficulty.html`）。規格：

- **Persona（釘死）**＝[`../CONTENT_SPEC.md`](../CONTENT_SPEC.md) §16.2 基線讀者：108 課綱數A（不含選修數甲）、無微積分先備、英文中等的自學大一新生；已讀過本章之前的所有章節（吸收不完美）。執行用具名 subagent [`../.claude/agents/learner-sim.md`](../.claude/agents/learner-sim.md)。
- **怎麼跑**：每章 ≥3 份**盲測** learner-sim（不要先告訴 sim 哪裡難），逐節回報：總判定 ok／effortful／stuck、卡點清單（locus＋引文＋severity：blocking／slowdown／minor）、逐節難度 1–5。
- **判準**：任何 **stuck（卡死需外援）＝blocking**；**B 類先備違規**（SPEC §16.2：未就地建立即使用）＝blocking——此項可先用 grep 對 B 類清單機械預檢。mainline 節難度上限＝「effortful 但可自行走完」（SPEC §16.1 難度預算）；超限者要嘛修、要嘛標 foundation／Proof track（[`TYPESETTING_GUIDE.md`](TYPESETTING_GUIDE.md) §10）。slowdown 級為 advisory，逐條裁決。
- **基線比對**：與 Ch1–Ch4 的難度曲線（Ch1–3≈3/5、Ch4=4/5、尖峰 §4.2=4.5——記錄於上述 audit HTML）比對；新章若出現高於 §4.2 的尖峰或整章 >4，屬**弧線層異常**，回 roadmap entry 的深度決策（SPEC §16.3）重議，不在散文層硬修。
- **修完必回歸**：blocking 修補後對修過的節**重跑盲測 sim**（比照 Ch1–Ch4 P3 複驗），確認卡點實際消失、且未引入新卡點。

## 通用紀律

- **雙閘精神不變、三閘每章全跑**：gate-1 Claude（免費）→ ⛳ 裁決 → 回歸審核 → gate-2 跨模型獨立複核（計費徵同意）。幻覺要穿過兩個獨立模型才會漏——這是雙閘的價值；2026-07-10 起 gate-2 三閘（數學／散文／圖）**每章必跑到定版**（取代原風險分層；見上方「gate-2 全跑」），章內不留 gate-2 債。
- **易懂性 reader-persona（M3，不新開關）：** 易懂性 A 以「**高中生／英文 L2／第一次線性讀**」為錨判（見 [`_audit/PROSE-AUDIT-RUBRIC.md`](_audit/PROSE-AUDIT-RUBRIC.md) 維度 A）。「先用後定義」的**結構性排序**宜更早在 Mode A 方向層攔（[`../CONTENT_DIRECTION.md`](../CONTENT_DIRECTION.md) §2），別留到散文閘才搬而 cascade 編號。
- **Codex 調用（實證，照這個）**：用 **PATH 上的 `codex`**（npm `codex-cli`，已登入 ChatGPT、走訂閱配額；**2026-07-10 起 0.144.1**，`~/.codex/config.toml` 預設 `model="gpt-5.6-terra"`／`model_reasoning_effort="xhigh"`／`service_tier="default"` 可直接跑、免加 `-m`。歷史坑：0.136.0 不認 terra 會 `400 requires a newer version`，升級前須 `-m gpt-5.5` 暫繞；`%LOCALAPPDATA%\OpenAI\Codex\bin` 底下的舊 build 亦可能拒新 model／config key，`tools/codex.cmd` shim 動態解析最新版避此坑，見 [`../ENVIRONMENT.md`](../ENVIRONMENT.md) ⑤）。指令：`codex exec -s read-only -C <repo> --output-schema <s.json> -o <out.json> - < <prompt.txt>`（Bash 工具、prompt 經 stdin 餵 raw UTF-8 避 PowerShell CJK 重編碼；prompt/schema 用 Write 寫檔不用 heredoc）。schema 全欄 required、`additionalProperties:false`、enum、無 min/max。每輪 ~120k tokens。**付費調用前一律先說明模型/用量/成本徵同意**（[`../CLAUDE.md`](../CLAUDE.md)）；read-only review 有 standing consent。
- **findings 留版控（raw 不進版控）**：Codex／外部模型原始輸出落 gitignored scratchpad、換機即失 → 摘要與裁決**轉錄**進 `handout/_dev-archive/ch{NN}/ch{NN}_<gate>-audit.md`（範本 `_dev-archive/ch03/ch03_example-supplement-audit.md`）或正式 REVIEW 報告；**`*.raw.txt` 一律不進版控**（2026-07-07 與 video 線統一）。
- **render 自驗**：node v22＋Chrome。`handout/_render/shot.mjs <url> <out/prefix> {full|figures}`（`figures` 逐圖截 2× PNG 餵圖閘）。驗收：0 KaTeX/MathJax err、0 未渲染 `\(`、env-num 連續無斷號、cross-ref 0 dangling、圖全 hydrate。
- **版面閘（顯示式斷行）**：`node handout/_render/linebreak-gate.mjs`（不帶參數＝掃全部 standalone；或接檔名只掃指定章）。抓被 MathJax `displayOverflow:'linebreak'` **自動硬斷**的顯示式（偵測 `mjx-linestack`，再對回原始 TeX），這類自動斷點常很醜。撰寫規則「寬式一律手動斷行」見 [`../CONTENT_SPEC.md`](../CONTENT_SPEC.md) §數學排版「寬顯示式的斷行」。驗收：自動斷行 0 條（退出碼 0）；改完數學式或新增章節後重建再跑一次。
- **編號 ledger 手動**（kit 無 auto-counter，**最大錯誤來源**）：每型獨立 counter、跨節連續；插 example/figure 會 cascade 其後全部編號＋散文 cross-ref。**先建完整編號地圖再動手**，改完 grep 核對連續性與引用解析。ledger 權威表在各章 `_dev-archive/ch{NN}/PLAN-ch{NN}.md` §5。
- **交付物「打開就能讀」**：含數學的待裁決/已套用報告產 standalone HTML（MathJax/KaTeX CDN、雙擊即開）。每完成一輪撰寫都產 `REVIEW-…-applied.html`。
- **commit**：經授權才 commit；繁中、body 逐條記裁決（供 `git log --grep` 撈回）、結尾 `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`。

## 工程注意：subagent 持久化

`.claude/` 被根 `.gitignore` 整個擋掉。要讓 gate subagent 進版控（換機/未來重用），須 **`git add -f .claude/agents/<name>.md`**。目前 `.claude/agents/` 下 **12 個 subagent 皆應 force-add 追蹤**：
handout 線 6 個（`example-supplement`、`handout-prose-audit`、`handout-figure-opportunity-audit`、`handout-figure-audit`、`mode-c-gapwalk`、`learner-sim`）＋ video 線 6 個（`hook-engineering-audit`、`narration-copyedit`、`narration-faithfulness-audit`、`visual-frame-audit`、`pedagogy-firstlearner-audit`、`video-amplification-audit`）。**新增 subagent 後務必 force-add**，否則換機即失。

## 各章狀態 dashboard（唯一章狀態表；2026-07-07）

> 本表為各章閘家族的**唯一狀態總表**（[`../CONTENT_ROADMAP.md`](../CONTENT_ROADMAP.md) entry 只留弧線／契約／open questions；as-built 編號與逐節 ledger 在各章 `PLAN-ch{NN}.md`，其閘家族 checklist 與本表同步）。

| 章 | Mode A | 數學 | 圖（機會／正確性） | 散文 S·A·V | 難度 sim | Mode C | 狀態 |
|---|---|---|---|---|---|---|---|
| Ch1 | ✅ 手稿六階 | ✅ 雙閘 | ✅／✅ 雙閘 | ✅ gate-1+2 | ✅（2026-07-03 首輪） | ✅ ①② | **全閘完成** |
| Ch2 | ✅ 手稿六階 | ✅ 雙閘 | ✅／✅ | ✅ gate-1+2 | ✅ | ✅ ①② | **全閘完成** |
| Ch3 | ✅ 手稿六階 | ✅ 雙閘（2026-06-27 補齊） | ✅／✅ | ✅ gate-1+2 | ✅ | ✅ ①② | **全閘完成** |
| Ch4 | ✅ 手稿六階 | ✅ 雙閘（gate-2 173.7k tok） | ✅／✅ | ✅ gate-1+2（154.7k tok） | ✅ | ✅ ①② | **全閘完成** |
| Ch5 | ✅ **canon M1**（2026-07-06） | ✅ M1 sweep＋**gate-2 全章**（1 blocking [M7] 修＋回歸→0；2026-07-07） | ✅／✅ **Figure 5.1–5.11**（D1–D8 gate-1 0/0；**視覺 gate-2 全跑 0/0**，2026-07-10） | ✅ **M3 gate-1**（三組 0 blocking；36 tighten/14 opt/2 voice 全 advisory）＋**S·A·V gate-2 0 blocking**（1 adv F4 已套用；2026-07-10） | ✅ **M3**（3 盲測 0 blocking/0 B類；均值≈3.2、尖峰 §5.7=4<§4.2 的 4.5） | ✅ **M4**（ADOPT 4：Ex 5.14/5.22＋2 軟深度；Ex 5.1–5.27） | **全閘完成·三閘 gate-2 全跑定版（canon 首例）** |
| App A–D | ✅ 自撰（無手稿先例） | A/B math-register gate-2 ✅ | — | — | — | — | 服務性附錄，按需維護 |
| Ch6 | ✅ **canon M1**（2026-07-10；深理論核心，FTC 兩部就地證） | ✅ M1 sweep **sympy 29/29**＋章層 review＋**三閘數學 gate-2**（1 blocking [Fig 6.2 caption overshoot 機制誤述] 修＋回歸→0；1 adv induction→telescoping；sol/max 2026-07-11） | ✅／✅ **Figure 6.1–6.9**（D1–D8 gate-1 0/0；**視覺 gate-2 全跑 0/0**，含 M4 semicircle；1 false-positive 複核駁回；2026-07-11） | ✅ **M3 gate-1**（5 節 0 blocking，§6.3 全乾淨）＋**S·A·V gate-2 0 blocking**（4 adv，3 客觀套用；2026-07-11） | ✅ **M3**（3 盲測 0 blocking／0 B類；曲線 [2,3,4,3,3]，尖峰 §6.3 FTC=4，≤§4.2 的 4.5） | ✅ **M4**（ADOPT 7/8：5 例題＋2 軟深度＋1 圖；Ex 6.1–6.21） | **全閘完成·三閘 gate-2 全跑定版·首個全程 5-milestone 試點章** |
| Ch7+ | 未開章（依 [`../CONTENT_ROADMAP.md`](../CONTENT_ROADMAP.md) 弧線骨架；canon 5-milestone 序列已於 Ch6 跑完定版） | | | | | | |
