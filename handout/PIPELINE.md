# 完成一章的閘序（HTML 講義 chapter lifecycle）

> **⚠️ 2026-08-09 拍板（LaTeX 統一）**：`latex/src/<ch>/*.tex` 升格唯一內容源、HTML 撰稿線退役
> （遷移計畫＝[`latex/KICKOFF-latex-unification.md`](latex/KICKOFF-latex-unification.md)，supersede 本檔
> 「兩線分工拍板」段與「改課文只改 `../legacy/html_handout/fragments/`」指示——**ch03 已改為改 `latex/src/ch03/chapter3.tex`**；
> 其餘章升格前照舊）。閘序本身（M1–M5、gate-2 全跑、雙閘紀律）**不變**，僅輸入載體隨 P3 rubric 改寫換為 `.tex`。

> **本檔是什麼：** 把一章講義從 spine 素材（手稿或 canon 藍本）推到「定稿」要經過的**完整閘序**之**權威總覽**，兼任**各章狀態 dashboard**。
> 各閘的細節規格不在此重複——本檔給「順序、各閘用什麼、哪裡停下、產出什麼」，細節指向既有 sub-doc。
> 撰稿模式（Mode A／B／C、兩種變體）以 [`../CONTENT_AUTHORING_WORKFLOW.md`](../CONTENT_AUTHORING_WORKFLOW.md) 為準；內容撰寫規則以 [`../CONTENT_SPEC.md`](../CONTENT_SPEC.md) 為準；改課文只改 `latex/src/<ch>/<name>.tex`、再 `python latex/build.py <ch>`（標記契約見 [`latex/CONTRACT-latex-writing.md`](latex/CONTRACT-latex-writing.md)）。

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
| M1 | **Mode A′（canon 草擬）** | 章層 canon 盤點 → 逐節：brief（含例題計畫、軟深度計畫、`figure_opportunities`）→ 擴寫 → Codex ⑤（direction-conformance＋數學＋hypothesis hygiene）至 0 blocking → 章層收尾 sweep：**sympy 全例重算＋hypothesis ledger 覆核＋章層 Codex review（明列對應 M1–M8 各維，不可只稱「已吸收」）** | 各節 ④；章層 sweep | Codex ⑤（每節）＋章層 review（**逐次徵詢**，見下方「通用紀律」） | 章完成後過目 `REVIEW-ch{NN}-applied.html` | `sec-{N}.html`＋章 opener＋PLAN-ch{NN} ledger | [`../CONTENT_AUTHORING_WORKFLOW.md`](../CONTENT_AUTHORING_WORKFLOW.md)、[`../CONTENT_DIRECTION.md`](../CONTENT_DIRECTION.md)、[`_audit/MATH-CORRECTNESS-RUBRIC.md`](_audit/MATH-CORRECTNESS-RUBRIC.md)（M1–M8 維度定義） |
| M2 | **圖批次** | brief／擴增稽核第 7 項產出的候選 → 裁決「畫哪些」→ 繪圖（`.tex` `figureblock`＋figkit `FIGS` 兩處同改＋`export_figs` 匯 PDF）→ 圖正確性 D1–D8 | `handout-figure-opportunity-audit`（候選覆核）；`handout-figure-audit`（吃 `shot.mjs` 圖 PNG） | Codex 視覺第二讀者（`-i` 餵 PNG）——每章必跑，批次見「gate-2 全跑」 | **章批次裁決畫哪些**＋修法裁決 | `REVIEW-ch{NN}-figure-opportunity.html`、`REVIEW-ch{NN}-figure-audit.html` | [`_audit/FIGURE-OPPORTUNITY-RUBRIC.md`](_audit/FIGURE-OPPORTUNITY-RUBRIC.md)、[`_audit/FIGURE-AUDIT-RUBRIC.md`](_audit/FIGURE-AUDIT-RUBRIC.md) |
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
- **判準**：任何 **stuck（卡死需外援）＝blocking**；**B 類先備違規**（SPEC §16.2：未就地建立即使用）＝blocking——此項可先用 grep 對 B 類清單機械預檢。mainline 節難度上限＝「effortful 但可自行走完」（SPEC §16.1 難度預算）；超限者要嘛修、要嘛標 foundation／Proof track（[`../legacy/html_handout/TYPESETTING_GUIDE.md`](../legacy/html_handout/TYPESETTING_GUIDE.md) §10）。slowdown 級為 advisory，逐條裁決。
- **基線比對**：與 Ch1–Ch4 的難度曲線（Ch1–3≈3/5、Ch4=4/5、尖峰 §4.2=4.5——記錄於上述 audit HTML）比對；新章若出現高於 §4.2 的尖峰或整章 >4，屬**弧線層異常**，回 roadmap entry 的深度決策（SPEC §16.3）重議，不在散文層硬修。
- **修完必回歸**：blocking 修補後對修過的節**重跑盲測 sim**（比照 Ch1–Ch4 P3 複驗），確認卡點實際消失、且未引入新卡點。

## 通用紀律

- **雙閘精神不變、三閘每章全跑**：gate-1 Claude（免費）→ ⛳ 裁決 → 回歸審核 → gate-2 跨模型獨立複核（計費徵同意）。幻覺要穿過兩個獨立模型才會漏——這是雙閘的價值；2026-07-10 起 gate-2 三閘（數學／散文／圖）**每章必跑到定版**（取代原風險分層；見上方「gate-2 全跑」），章內不留 gate-2 債。
- **易懂性 reader-persona（M3，不新開關）：** 易懂性 A 以「**高中生／英文 L2／第一次線性讀**」為錨判（見 [`_audit/PROSE-AUDIT-RUBRIC.md`](_audit/PROSE-AUDIT-RUBRIC.md) 維度 A）。「先用後定義」的**結構性排序**宜更早在 Mode A 方向層攔（[`../CONTENT_DIRECTION.md`](../CONTENT_DIRECTION.md) §2），別留到散文閘才搬而 cascade 編號。
- **Codex 調用（實證，照這個）**：用 **PATH 上的 `codex`**（npm `codex-cli`，已登入 ChatGPT、走訂閱配額；**2026-07-10 起 0.144.1**，`~/.codex/config.toml` 預設 `model="gpt-5.6-terra"`／`model_reasoning_effort="max"`／`service_tier="default"` 可直接跑、免加 `-m`（**2026-07-18 使用者定案：預設 terra/max**；`gpt-5.6-sol` 能力更強但較耗訂閱配額，僅特定 run 值得時才以 `-m gpt-5.6-sol` 升級。註：Ch5–7 定版時 config 一度漂為 `sol/max`、gate-2 即以 sol 跑完並記於各章 `_dev-archive/ch{NN}/ch{NN}_gate2-audit.md`；2026-07-18 已對齊回 terra）。歷史坑：0.136.0 不認 terra 會 `400 requires a newer version`，升級前須 `-m gpt-5.5` 暫繞；`%LOCALAPPDATA%\OpenAI\Codex\bin` 底下的舊 build 亦可能拒新 model／config key，`tools/codex.cmd` shim 動態解析最新版避此坑，見 [`../ENVIRONMENT.md`](../ENVIRONMENT.md) ⑤）。指令：`codex exec -s read-only -C <repo> --output-schema <s.json> -o <out.json> - < <prompt.txt>`（Bash 工具、prompt 經 stdin 餵 raw UTF-8 避 PowerShell CJK 重編碼；prompt/schema 用 Write 寫檔不用 heredoc）。schema 全欄 required、`additionalProperties:false`、enum、無 min/max。每輪 ~120k tokens。**付費調用前一律先說明模型/用量/成本徵同意**（[`../CLAUDE.md`](../CLAUDE.md)）；**read-only review 亦須逐次徵詢**（2026-07-17 使用者裁決：本檔原寫「read-only review 有 standing consent」，與 [`../CLAUDE.md`](../CLAUDE.md)「Codex 唯讀調用…需逐次徵詢」直接衝突；使用者裁定 **CLAUDE.md 為準**，本檔兩處 standing consent 字樣同批改正）。
- **開長閘前先從 `main` 更新，並看有沒有人撞過同一面牆**（2026-07-26 ch04 實證立）：平行輪是一章一 worktree，分支從開輪那一刻的 `main` 岔出去就不再動。**跨章的長閘**——Gate 7／LaTeX rollout、圖匯出、字形閘、`convert.py` 方言 mapping 這類**動共用工具**的——開跑前先 `git fetch`／看一次 `git log main`，確認基準沒有落後，並掃一下別的章有沒有已經解過同型問題。**代價是實測出來的**：ch04 的 Gate 7 花了六輪去試「讓 Chrome 用 TeX 樹的 NewCM OTF」（file://、`--allow-file-access-from-files`、`--disable-web-security`、同目錄相對路徑、loopback HTTP、wrapper 同源供出），最後用五個剝表變體＋Inter 對照組證明 Chrome 的 OTS 就是不收那個檔——而 ch03 輪早在 `e443070` 把同一結論寫進 `export_figs.mjs` 的註解，連「Bold／BoldItalic 剛好會過、Regular／Italic 不會」都記了。ch04 的 worktree 基準是 `942ccea`，做 Gate 7 時 `main` 已前進二十餘筆，看不到那份紀錄。**共用工具的坑會被重複踩**，散文輪各改各的 fragment 則不受此影響。同理，回報「某章缺了某個檔」之前先確認那不是刻意的設計（ch04 曾把 `chapters/ch01/figs/` 未提交報成缺口，實際上圖匯出中間物本就不進版控，見 `.gitignore`）。
- **findings 留版控（raw 不進版控）**：Codex／外部模型原始輸出落 gitignored scratchpad、換機即失 → 摘要與裁決**轉錄**進 `handout/_dev-archive/ch{NN}/ch{NN}_<gate>-audit.md`（範本 `_dev-archive/ch03/ch03_example-supplement-audit.md`）或正式 REVIEW 報告；**`*.raw.txt` 一律不進版控**（2026-07-07 與 video 線統一）。
- **編譯自驗（2026-08-09 起）**：改完源跑 `python latex/build.py <ch>`——編譯閘（0 error／0 missing char）＋overfull 逐條列出＋字形閘內建，成品進 `dist/`。log 不得有 undefined reference（`\ref` 全解析）。圖鏈自驗：`node figkit/shot.mjs figkit/figs-<ch>.html <out/prefix> figures`（逐圖 2× PNG 餵圖閘）＋`node latex/export_figs.mjs figkit/figs-<ch>.html latex/chapters/<ch>/figs`（改圖後重匯；**pull 進別台改過的 `figs-<ch>.html` 後也要重匯**——匯出品 gitignored、`build.py` 不比新鮮度，本機舊圖會照樣編進有版控的 dist PDF）。〔歷史 HTML 自驗（KaTeX err／hydrate／linebreak-gate）隨撰稿線凍結退役——寬顯示式斷行由 TeX 原生＋overfull 閘接手，撰寫規則不變（[`../CONTENT_SPEC.md`](../CONTENT_SPEC.md) §數學排版）。〕
- **編號語意化（2026-08-09 P2 起；原手動 ledger 退場）**：環境 num 參數給 label key（`{thm:ibp}`）＝auto-counter＋`\label`，文內引用 `Theorem \ref{thm:ibp}`——**插入不再 cascade、新內容不得手寫編號**（[`latex/CONTRACT-latex-writing.md`](latex/CONTRACT-latex-writing.md) §Numbering）。各章 as-built ledger（`_dev-archive/ch{NN}/PLAN-ch{NN}.md` §5）自此為**歷史快照**——現行編號以編譯輸出為準；跨章引用仍字面、被引章重編號時書層 sweep 批改。
- **交付物「打開就能讀」**：含數學的待裁決/已套用報告產 standalone HTML（MathJax/KaTeX CDN、雙擊即開）。每完成一輪撰寫都產 `REVIEW-…-applied.html`。
- **commit**：經授權才 commit；繁中、body 逐條記裁決（供 `git log --grep` 撈回）、結尾 `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`。

## 出版排版線（HTML→LaTeX；pilot GO 2026-07-17）

上面的內容 QA 閘鏈讀 **`latex/src/` 源**（2026-08-09 統一前＝fragment）、與排版引擎無關；下段為 2026-07-17 兩線時代的出版線敘述——**已被 LaTeX 統一 supersede**（工具已退役、rollout 已完畢），現況見 [`latex/README.md`](latex/README.md)、留此供讀 DIALECT 等歷史資產——當時排版是一條**下游線**在
[`latex/`](latex/)：`convert.py`（確定性轉換：數學逐位元組 pass-through、
表外標記硬錯、fragment 唯讀）→ `template/calcbook.sty`（memoir；語意層＋樣式層分離，
模板拍板紀錄 [`latex/template/M-B1-DECISIONS.md`](latex/template/M-B1-DECISIONS.md)）→
`latexmk -lualatex` 出 A4 PDF，四閘驗收（編譯／版面／完整性／人眼，kickoff §4.5）；**成品收在 `latex/dist/<ch>/`（每單元恰兩檔：pdf＋自足 tex，`make_dist.py` 產）**。
appB pilot 已 GO（收案當時：同內容 HTML 20 頁 → LaTeX 14 頁，四閘全綠）；**2026-07-17 appB 加 §B.6 後重跑並重新凍結＝24 頁、四閘仍全綠**，成品 `latex/dist/appB/` 已更新（沿革見 [`latex/KICKOFF-latex-pilot.md`](latex/KICKOFF-latex-pilot.md) 頭段）。**逐章 rollout**（建議順序
ch03→ch01→ch06→其餘附錄；屆時另開計畫）每章＝方言差集盤點（`dialect_inventory.py`）→
補 mapping（權威表 `chapters/<ch>/DIALECT-<ch>.md`）→ 四閘；完整沿革與 rollout 預告見
[`latex/KICKOFF-latex-pilot.md`](latex/KICKOFF-latex-pilot.md)。

**rollout 現況（成品有無，唯一速查）**：

| 單元 | DIALECT | `dist/` 成品 | 上線日 |
|---|---|--:|---|
| appB | ✅ | 25 頁 | pilot；2026-07-17 加 §B.6 後重新凍結 |
| ch01 | ✅ | 44 頁 | 2026-07-25（多 panel 圖 grid 版面 07-26 補） |
| ch02 | ✅ | 35 頁 | 2026-07-26 |
| ch03 | ✅ | 22 頁 | 2026-07-26 |
| ch04 | ✅ | 32 頁 | 2026-07-26（字形閘加 glyf 比對路徑） |
| ch05 | ✅ | 36 頁 | 2026-07-26 |
| **ch06** | ✅ | **28 頁** | 2026-07-26（方言差集 0——裸 `span.qed` 已由 ch04 那輪補上） |
| **ch07** | ✅ | **39 頁** | 2026-07-26（**六閘全過**——含人眼閘與**使用者 GO**（2026-07-26）；方言差集 0；全書圖最多的一章＝23 圖／27 panel。**修共用工具一項**：字形閘在「整條輪廓全 off-curve」的合法 TrueType 構造上 crash，觸發者是圖面板文字裡的 `?`——見 [`latex/chapters/ch07/DIALECT-ch07.md`](latex/chapters/ch07/DIALECT-ch07.md) §3）。**人眼閘抓到 3 條**平實化輪造成、HTML 線看不出來的缺陷（含一處 figcaption 整句重複），已修並補程式化前哨 `tools/dup_scan.py`——見同檔 §4b |
| ch08 | ✅ | 50 頁 | 2026-08-09 P1 首轉（方言差集 0；自動閘全綠；**人眼閘待過目**；內容側 gate-2 債見 dashboard） |
| appA／appC／appD | ✅ | appA 17／appC 6／appD 6 頁 | 2026-08-09 P1 首轉（方言差集皆 0；自動閘全綠；**人眼閘待過目**）。overfull 已全清（2026-08-10）：appA×3 於 pill 度量 merge 後自然消失；appD×1／ch04×1／ch06×1 以零語義措辭微調修訖（as required／Thus／Now 級），**全書 12 單元 overfull＝0** |

HTML standalone 在兩線時代定位＝撰稿預覽＋圖閘 render 載體（D2／D6）；**2026-08-09 起
撰稿線凍結**——圖閘 render 載體改 figkit harness、撰稿預覽改 dist PDF。

> **兩線分工拍板（2026-07-17 使用者裁決）**：**整體仍先做 HTML 講義**（`html/`＝撰稿製作線，
> 內容撰寫、QA 閘鏈、圖系統照舊在此線推進）；**「為了好看，最後定稿的講義把 HTML 轉成 LaTeX」**
> （`latex/`＝定稿出版線，rollout 時點跟各章／全書定稿走，不搶在內容前面）。fragment 仍是唯一
> 內容源、`.tex` 是 build 產物不進版控（無雙源）。**本拍板 supersede kickoff §9 的 rollout
> 時點**（原「pilot GO 即全面 rollout」→ 逐章轉換改跟定稿走）；kickoff 的 D2「排版的家＝LaTeX，
> 現在就定」與 §9 的建議順序不受影響。同日資料夾重整：`handout/` 依兩線分家——
> 原 `handout/tex_export/` → `handout/latex/`（章節資產再各歸 `latex/chapters/<ch>/`）；fragment／standalone／`_render`／`_audit`／
> `_dev-archive`（撰稿部分）→ `handout/html/`；standalone 集中進 `../legacy/html_handout/standalone/`。

## 工程注意：subagent 持久化

`.claude/` 被根 `.gitignore` 整個擋掉。要讓 gate subagent 進版控（換機/未來重用），須 **`git add -f .claude/agents/<name>.md`**。目前 `.claude/agents/` 下 **12 個 subagent 皆應 force-add 追蹤**：
handout 線 6 個（`example-supplement`、`handout-prose-audit`、`handout-figure-opportunity-audit`、`handout-figure-audit`、`mode-c-gapwalk`、`learner-sim`）＋ video 線 6 個（`narration-copyedit`、`narration-faithfulness-audit`、`visual-frame-audit`、`pedagogy-firstlearner-audit`、`video-amplification-audit`、`motion-designer`；原 `hook-engineering-audit` 已於 2026-09-28 隨 Manim gen-2 刪除，見 [`../video/KICKOFF-remotion-unification.md`](../video/KICKOFF-remotion-unification.md)）。**新增 subagent 後務必 force-add**，否則換機即失。

## 各章狀態 dashboard（唯一章狀態表；2026-07-07）

> 本表為各章閘家族的**唯一狀態總表**（[`../CONTENT_ROADMAP.md`](../CONTENT_ROADMAP.md) entry 只留弧線／契約／open questions；as-built 編號與逐節 ledger 在各章 `PLAN-ch{NN}.md`，其閘家族 checklist 與本表同步）。

| 章 | Mode A | 數學 | 圖（機會／正確性） | 散文 S·A·V | 難度 sim | Mode C | 狀態 |
|---|---|---|---|---|---|---|---|
| Ch1 | ✅ 手稿六階 | ✅ 雙閘 | ✅／✅ 雙閘 | ✅ gate-1+2 | ✅（2026-07-03 首輪） | ✅ ①② | **全閘完成** |
| Ch2 | ✅ 手稿六階 | ✅ 雙閘／**✅ 2026-07-26 兩處數學待辦已結案**——① §2.3「no single tangent direction」複查後判**非缺陷**（該句只斷言角點沒有單一切線方向，方向正確；Definition 2.3 的白話重述本就寫明排除 vertical spike），改為補上該節自己示範過的第二種失效模式（`or a vertical tangent`）以求完整；② §2.4 `\(y' = ky\)` 補明 `\(k\)` 為常數。**未採** Codex 建議的 `\(Ce^{kx}\)`——微分 `\(e^{kx}\)` 需鏈鎖法則（Ch3），在本章的 on-credit 紀律下不宜再加當下無法驗證的斷言。證據：[`latex/chapters/ch02/DIALECT-ch02.md`](latex/chapters/ch02/DIALECT-ch02.md) §6 | ✅／✅ | ✅ gate-1+2 | ✅ | ✅ ①② | **全閘完成**；**LaTeX 出版線亦收尾**（2026-07-26：五閘全過含人眼閘，`latex/dist/ch02/` 已產出） |
| Ch3 | ✅ 手稿六階 | ✅ 雙閘（2026-06-27 補齊） | ✅／✅ | ✅ gate-1+2 | ✅ | ✅ ①② | **全閘完成** |
| Ch4 | ✅ 手稿六階 | ✅ 雙閘（gate-2 173.7k tok）＋**scoped 補正 3 處**（2026-07-26）：N-08 Example 4.4 收尾的一般化補上 MVT／Rolle 所需的區間與可微前提、N-12 Proposition 4.3 證明補上 Corollary 4.4 的前提、§4.5 應用段補「代 \(t=0\) 定出常數＝\(y(0)\)」。三者由 ch04 平實化輪的 Codex gate-2 指出，該散文輪不動數學故延到此輪。證據：[`_audit/REPORT-ch04-plain-codex-round1-raw.md`](_audit/REPORT-ch04-plain-codex-round1-raw.md) §(4) | ✅／✅ | ✅ gate-1+2（154.7k tok） | ✅ | ✅ ①② | **全閘完成**；**LaTeX 出版線四閘全綠**（2026-07-26，`dist/ch04/`＝chapter4.pdf 32 頁＋自足 .tex；方言差集與排除紀錄見 [`latex/chapters/ch04/DIALECT-ch04.md`](latex/chapters/ch04/DIALECT-ch04.md)） |
| Ch5 | ✅ **canon M1**（2026-07-06） | ✅ M1 sweep＋**gate-2 全章**（1 blocking [M7] 修＋回歸→0；2026-07-07） | ✅／✅ **Figure 5.1–5.11**（D1–D8 gate-1 0/0；**視覺 gate-2 全跑 0/0**，2026-07-10） | ✅ **M3 gate-1**（三組 0 blocking；36 tighten/14 opt/2 voice 全 advisory）＋**S·A·V gate-2 0 blocking**（1 adv F4 已套用；2026-07-10） | ✅ **M3**（3 盲測 0 blocking/0 B類；均值≈3.2、尖峰 §5.7=4<§4.2 的 4.5） | ✅ **M4**（ADOPT 4：Ex 5.14/5.22＋2 軟深度；Ex 5.1–5.27） | **全閘完成·三閘 gate-2 全跑定版（canon 首例）**；**LaTeX 出版線四閘全綠**（2026-07-26，`dist/ch05/`＝chapter5.pdf 36 頁＋自足 .tex；方言差集 1 項〔env-kicker 內含數學〕與「U+2019 誤當 prime」內容缺陷紀錄見 [`latex/chapters/ch05/DIALECT-ch05.md`](latex/chapters/ch05/DIALECT-ch05.md)） |
| App A–D | ✅ 自撰（無手稿先例） | A/B math-register gate-2 ✅ | — | — | — | — | 服務性附錄，按需維護 |
| Ch6 | ✅ **canon M1**（2026-07-10；深理論核心，FTC 兩部就地證） | ✅ M1 sweep **sympy 29/29**＋章層 review＋**三閘數學 gate-2**（1 blocking [Fig 6.2 caption overshoot 機制誤述] 修＋回歸→0；1 adv induction→telescoping；sol/max 2026-07-11） | ✅／✅ **Figure 6.1–6.9**（D1–D8 gate-1 0/0；**視覺 gate-2 全跑 0/0**，含 M4 semicircle；1 false-positive 複核駁回；2026-07-11） | ✅ **M3 gate-1**（5 節 0 blocking，§6.3 全乾淨）＋**S·A·V gate-2 0 blocking**（4 adv，3 客觀套用；2026-07-11） | ✅ **M3**（3 盲測 0 blocking／0 B類；曲線 [2,3,4,3,3]，尖峰 §6.3 FTC=4，≤§4.2 的 4.5） | ✅ **M4**（ADOPT 7/8：5 例題＋2 軟深度＋1 圖；Ex 6.1–6.21） | **全閘完成·三閘 gate-2 全跑定版·首個全程 5-milestone 試點章**（2026-07-11）。**下游兩線亦已收（2026-07-26）**：平實化回填 em-dash 12.5→**1.4**/1000（[`_audit/REVIEW-ch06-plain-applied.html`](_audit/REVIEW-ch06-plain-applied.html)）＋LaTeX 出版線四閘全綠、成品 `latex/dist/ch06/`（[`latex/chapters/ch06/DIALECT-ch06.md`](latex/chapters/ch06/DIALECT-ch06.md)）。**2026-08-09 Ch8 gate-2 連動修正一句**：Thm 6.5 證成的「applies verbatim」超額宣稱（EF1，兩個獨立模型確認與 §8.1 開區間要求不相容）→ 改如實描述＋指向 Thm 8.2 證明的建構；使用者裁決、重編全綠（[`_dev-archive/ch08/ch08_gate2-audit.md`](_dev-archive/ch08/ch08_gate2-audit.md) §5） |
| Ch7 | ✅ **canon M1**（2026-07-18；標準嚴謹，積分 MVT／C¹ 弧長／表面積三定理就地全證，零新增 fence） | M1 側 ✅：**sympy 48/48**＋逐節 ⑤ 0 blocking＋章層 review **M1–M8 全維 CLEAN 0/0**＋**數學 gate-2（sol/max）0 blocking**（23 例最終答案＋Thm 7.1–7.4 四證皆對；1 adv Ex 7.15 端點退化精確化已套） | ✅／✅：機會覆核（7 subagent，23 張採納）→ 2.5D pattern Codex 收斂 → **Figure 7.1–7.23 全繪**→ **D1–D8 gate-1 23/23 歸零**（首輪 3 blocking＋6 advisory 全修＋回歸 clean；2026-07-18；`REVIEW-ch07-figure-audit.html`）；**視覺 gate-2 0 blocking**（23 PNG 餵 Codex；1 D7 Fig 7.16 定義圖 spoiler→使用者裁 (B) 輕修 caption、22 clean） | ✅ **M3 gate-1（applied）**（7 節 0 blocking；17+1 修補套用）＋**S·A·V gate-2 0 blocking**（確認 M3/M4 橋接；4 adv F3/F4 套用） | ✅ **M3**（3 盲測 0 stuck／0 B 類；曲線 [2,3,3,3.5–4,3,3.5–4,4–4.5]、尖峰 §7.7 表面積證明 ≈Ch4 §4.2；scoped 回歸 0 stuck） | ✅ **M4**（ADOPT 4/4：Ex 7.8 §7.2 shifted-axis＋3 軟深度〔avg-velocity 橋／Neile 史脈／Strategy 7.4〕；Example 7.1–7.23＝cap；scoped Mode B＋sim 皆 0 blocking／0 stuck） | **全閘完成·三閘 gate-2 全跑 0 blocking·定版**（2026-07-18；canon 第 3 章，繼 Ch5/Ch6）；as-built ledger 見 [`_dev-archive/ch07/PLAN-ch07.md`](_dev-archive/ch07/PLAN-ch07.md)。**下游兩線亦已收（2026-07-26）**：平實化回填 em-dash 17.5→**1.6**/1000（全書超額最多的單元，執行 146 條＋Codex gate-2 ADOPT 116／MODIFY 39；[`_audit/REVIEW-ch07-plain-applied.html`](_audit/REVIEW-ch07-plain-applied.html)）＋§7.7 frustum 推導補上 \(r_1=0\) 覆蓋（Codex 範圍外發現）＋LaTeX 出版線四閘全綠、成品 `latex/dist/ch07/`（39 頁；[`latex/chapters/ch07/DIALECT-ch07.md`](latex/chapters/ch07/DIALECT-ch07.md)） |
| Ch8 | ✅ **canon M1**（2026-07-26；標準/計算工具箱章；**首個 SPEC §3 平實條款生成端章**——em-dash 0.0/1000（歷史 canon 初稿 14.4）、家族命中 1.9/1000 自修至 ≈0，生成端驗證**達標**；整章一次生成（kickoff v3）；恰兩筆 on-credit＝§8.4 FTA fact＋§8.7 誤差界→Ch11 §11.9；Thm 8.3 Comparison 主線全證；Ex 7.12 shell–washer 承諾 §8.1 scoped 兌現） | M1 側 ✅：**sympy 65/65**＋逐節 ⑤ 批次 15B+3A 全修/裁決＋章層 review **M1–M8 逐維（M7 1B 已修，餘 clean）**＋scoped 回歸 **R1–R15 全 clean**；render math=1007/0 err；ledger 連續、xref 48/0 dangling。數學 gate-2 依「三閘 M4 後批次」規則留待 | ✅／✅ **gate-1 側完成（2026-07-26）**：機會覆核 7 subagent（9 標記→13 候選＋32 駁回；§8.4/§8.5 刻意零圖成立）→ 使用者裁決 **adopt-all-13** → **Figure 8.1–8.13 全繪**（kit 擴充 fill-ghost/fill-aux＋triple 版面收斂；作者自查修 9 處，Fig 8.11 區間 [1,3] 偏離記錄）→ **D1–D8 gate-1 13/13 blocking 歸零**（4 D1 advisory——3 條 vline 越軸同根因＋1 label 擦線——全修）→ 回歸 R1–R4 clean。`REVIEW-ch08-figure-opportunity.html`／`REVIEW-ch08-figure-audit.html`（13 圖內嵌）；視覺 gate-2 留 M4 後批次 | ✅ **M3 gate-1（applied，2026-07-26）**（`handout-prose-audit` ×7：7 節 **0 blocking**、advisory ≈94；紅旗 G1-8.6-10〔§8.6 兩處逾越 ③ B-02 的 e^{−x²} scope 紀律〕列必修；使用者親裁「照建議套用」→ **裁決項 66＋必修 1＋回歸殘項 2＋補測 7＋複核 3 ＝ 108 處文字替換全落地**〔spelling DEFER 書層 sweep；初版紀錄「69＋2 編輯點」為壓縮前粗估，已於 2026-07-27 更正口徑〕；**scoped 散文複核 ×3 皆 0 blocking**——修補句無新缺陷、B-02 措辭驗證乾淨；em-dash 修後仍 **0.0**/1000〔N=8214〕）；S·A·V gate-2 留 M4 後批次 | ✅ **M3**（3 盲測 **0 stuck／0 B 類**；尖峰 §8.3／§8.6≈3.5（局部 4）＜§4.2 的 4.5——「標準/計算」深度成立、無弧線異常；**scoped 回歸盲測 ×3 獨立實例（§8.1/§8.6/§8.7）0 blocking／0 stuck／0 B 類，gate PASS**——難度 §8.1=3–3.5／§8.6=3–3.5／§8.7=2.5–3，三份皆判與 Ch1–Ch4 基線持平偏低；兩份補派實例另抓出 7 條單一實例漏掉的客觀缺陷〔§8.7「constant 一半」撞義讀來為假、§8.6 未宣告別名 monotone convergence theorem、§8.1 shell–washer 單調性缺步與收尾抵消、§8.7 Simpson 的 \(i\) 範圍、Thm 8.2 轉折未承認、章開場「唯一沒倒著跑的法則」與 Thm 2.7 衝突〕，使用者親裁全修＋其複核 0 blocking＋3 advisory 就地再修） | ✅ **M4**（2026-07-27，CLOSED）：gate-1 偵察 **4 獨立實例**（`mode-c-gapwalk` ×2 順序／逆序全章＋`example-supplement` ×2 分半章，依 M3 補正輪教訓派雙實例）→ ①波 **4 候選全 Layer 1**（皆為「本書自己陳述或證明過卻從未示範」：Thm 8.4 的 Simpson 界、Thm 8.3**(b)**、Ex 8.6 的 reduction formula、Strategy 8.2 step 2）＋②波 34 筆去重候選，**12 缺口雙實例命中、1 缺口跨波命中**；§8.3/§8.4/§8.5 例題判乾淨。使用者裁決：①波採 2＋轉形 1、②波採到 T3、四個品味題全採。**落地 26 處**（2 example＋24 段不編號），**Example 8.1–8.38 ＝ 38 ＝ D1 硬上限**，cascade 僅 4 位移（`8.1-E1` 轉不編號推導段省下 30 個重編號）。回歸：Mode B ×3 → 4 blocking 全修，複核 ×2 → **0 blocking**＋另抓出 7 條修補自身引入的缺陷全修；盲測 ×3 **0 stuck／0 B 類**＋scoped §8.6 回歸 0 stuck。sympy **59/59**、render math 1378／err 0／13-13 圖／dangling 0、**em-dash 仍 0.0/1000**。裁決稿 [`_audit/REVIEW-ch08-modec-gapcheck.html`](_audit/REVIEW-ch08-modec-gapcheck.html)；紀錄 `ch08_modec-gapcheck-audit.md` | **全閘完成·三閘 gate-2 全跑 0 blocking·定版**（2026-08-09；gate-2 債於 P5 償清——**首個在 LaTeX 源上跑 gate-2 的章**，Codex terra/max、`.tex` 全文 inline＋figkit harness PNG）。三閘結果：數學 1 blocking〔G2M-1＝EF5 確認：§8.4 無條件宣稱 vs case-IV 留白〕＋1 advisory〔G2M-2＝EF8：Ex 8.31 引 Thm 6.2 於不連續點〕、M1–M6 clean；散文 0 blocking 0 新 finding；圖 13/13 全 clean。既有發現 7 條全裁決（EF1 跨章矛盾確認為真→使用者裁修 Ch6；EF3/EF4 判非缺陷；餘確認 advisory）。使用者逐題裁決後落地 9 處措辭級修補（ch08×8＋**ch06×1**＝Thm 6.5「applies verbatim」超額宣稱改如實描述）；回歸＝兩章重編全綠、0 undefined ref。紀錄＝[`_dev-archive/ch08/ch08_gate2-audit.md`](_dev-archive/ch08/ch08_gate2-audit.md)。**M5 收尾（2026-07-27）**：PLAN 閘家族 checklist 補滿＋本 dashboard 行更新＋CONTENT_ROADMAP Ch8 entry 回填 as-built 並收 open questions＋Ch11 entry 補記雙向 seam 義務（§11.3 import Def 8.1/Prop 8.2/Thm 8.3；§11.9 discharge Thm 8.4）。as-built 凍結：Def 8.1–8.2／Thm 8.1–8.4／Prop 8.1–8.2／Strategy 8.1–8.6／**Example 8.1–8.38**／Figure 8.1–8.13／Caution ×17；恰兩筆 on-credit。as-built ledger＝[`_dev-archive/ch08/PLAN-ch08.md`](_dev-archive/ch08/PLAN-ch08.md)。**gate-2 開跑時的輸入＝`ch08_modec-gapcheck-audit.md` §8 的既有內容發現 7 條**，最重要一條為**跨章矛盾：Ch6 Thm 6.5 的「applies verbatim from Thm 6.4」vs Ch8 Thm 8.2 證明的「Theorem 6.4 cannot be cited directly」**，已逐字驗證、判 §8.1 嚴謹／§6.4 超額宣稱，因 Ch6 已定版（含 LaTeX 線）故交數學 gate-2 由第二模型定奪 |
| Ch9+ | 未開章（依 [`../CONTENT_ROADMAP.md`](../CONTENT_ROADMAP.md) 弧線骨架） | | | | | | |
