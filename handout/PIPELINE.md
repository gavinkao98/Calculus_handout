# 完成一章的閘序（HTML 講義 chapter lifecycle）

> **本檔是什麼：** 把一章講義從「手稿」推到「定稿」要經過的**完整閘序**之**權威總覽**。
> 各閘的細節規格不在此重複——本檔給「順序、各閘用什麼、哪裡停下、產出什麼」，細節指向既有 sub-doc。
> 內容撰寫規則以 [`../CONTENT_SPEC.md`](../CONTENT_SPEC.md) 為準；改課文只改 `fragments/`、再 `python build.py ch{NN}`（見 [`README.md`](README.md)）。

## 「做完一章」的定義

= **與 Ch1／Ch2 完全同級全跑**。權威敘述見 [`../CONTENT_ROADMAP.md`](../CONTENT_ROADMAP.md) 的 Ch2 status 行末句：
**手稿六階 ＋ Mode C（①例題＋②軟深度）＋ 去 AI 味 S·A·V（gate-1+2）＋ 圖機會/正確性兩閘（圖正確性 gate-1+2）＋ 數學正確性雙閘。**

## 閘序總表

| # | 階段 | 做什麼 | gate-1（Claude，免費） | gate-2（Codex，計費） | ⛳ | 產物 | 權威 sub-doc |
|---|---|---|---|---|---|---|---|
| 0 | **Mode A 六階定稿** | 手稿→教科書草稿，章內六階方向層收斂、雙模型對抗審至 blocking=0、使用者簽核 | 各節 ④/⑤ | Codex ⑤ | 多處 | `sec-{N}.html`＋章 opener | [`../CONTENT_DIRECTION.md`](../CONTENT_DIRECTION.md)（六階）、[`README.md`](README.md)（Mode A 擴增稽核 9 項） |
| 1 | **Mode B** | 審訂稽核（簽核前 或 Mode C 後**範圍限定**新 `[pass: enrichment]` 標記） | 主審/各 audit subagent | 可選 | 逐條 | commit body 裁決 | [`README.md`](README.md) §Mode B |
| 2a | **Mode C ①波 補題目** | 從題庫補 worked example（缺口分析→CLP-1 對症選題→改寫） | `example-supplement` subagent | Codex 選題稽核 | 裁決選哪些 | `ch{NN}_example-supplement-review.html`＋`-applied`＋`-audit.md` | [`../CONTENT_SOURCING.md`](../CONTENT_SOURCING.md) |
| 2b | **Mode C ②波 軟深度** | 補 intuition/caution/application/strategy/summary/history（**非** example） | `mode-c-gapwalk` subagent（9 鏡頭逐節偵察） | 可選 | 裁決選哪些 | `REVIEW-ch{NN}-modec-enrichment.html`（+applied） | [`README.md`](README.md) §Mode C |
| 3 | **圖機會閘** | 該不該加圖（出圖前） | `handout-figure-opportunity-audit` subagent | — | 裁決畫哪些 | `REVIEW-ch{NN}-figure-opportunity.html` | [`_audit/FIGURE-OPPORTUNITY-RUBRIC.md`](_audit/FIGURE-OPPORTUNITY-RUBRIC.md) |
| 4 | **圖正確性閘 D1–D8** | 畫出來對不對（render 後） | `handout-figure-audit` subagent（吃 `shot.mjs` 圖 PNG） | Codex 視覺第二讀者（`-i` 餵 PNG） | 修法裁決 | `REVIEW-ch{NN}-figure-audit{,-gate2}.html` | [`_audit/FIGURE-AUDIT-RUBRIC.md`](_audit/FIGURE-AUDIT-RUBRIC.md) |
| 5 | **數學正確性閘 M1–M8** | 教什麼、對不對 | Claude/Mode B 走查（sympy 重算 worked example） | Codex 獨立複核 | 逐條裁決 | `REVIEW-ch{NN}-math-audit.html`＋`-gate2.md` | [`_audit/MATH-CORRECTNESS-RUBRIC.md`](_audit/MATH-CORRECTNESS-RUBRIC.md) |
| 6 | **S·A·V 散文閘**（含易懂性 A／流暢性 B） | 去 AI 味語意收斂 | `handout-prose-audit` subagent（三維＋錨組） | Codex 同 rubric 複核 | 逐條裁決改寫/刪 | `REVIEW-ch{NN}-svc-gate{1,2}.html` | [`_audit/PROSE-AUDIT-RUBRIC.md`](_audit/PROSE-AUDIT-RUBRIC.md)、[`../PLAN-deai-semantic-critic-implementation.md`](../PLAN-deai-semantic-critic-implementation.md)（Task 8 逐章鋪） |
| 7 | **難度閘（初學者模擬）** | 定稿前實測難度：3 份以上盲測 learner-sim 逐節模擬閱讀＋難度 1–5 評分（見下方「難度閘」節） | learner-sim agents（免費；persona＝SPEC §16.2 基線讀者） | 可選（Codex 抽驗 sim 主張對回原文） | 裁決修不修 | `REVIEW-ch{NN}-difficulty-sim.html`＋逐節難度評分記入 ROADMAP entry | [`../CONTENT_SPEC.md`](../CONTENT_SPEC.md) §16 |
| 8 | **收尾** | ROADMAP status 標「與 Ch1/Ch2 同級全跑」 | — | — | 確認 | ROADMAP 更新 | [`../CONTENT_ROADMAP.md`](../CONTENT_ROADMAP.md) |

> **順序不是死管線**：0→1 是 Mode A 內建；簽核後 2–6 是可獨立補跑的閘（互相大致獨立，建議「數學→圖→散文」或「圖→數學→散文」皆可；②軟深度宜在數學/散文閘之前，使新增內容一併被後閘審到）。每個 ⛳ 停下等使用者裁決。

## Mode C 兩波（最易混淆，釘死）

「Mode C 充實」**分兩波、各有獨立 spec／subagent／產物**，不要混為一談（ROADMAP Ch2 status：「Mode C 充實分兩波 ①課文範例補充 ②軟深度充實」）：
- **①波 補題目＝worked example**：服務對象是 `example`＋`solution`；流程 [`../CONTENT_SOURCING.md`](../CONTENT_SOURCING.md)（手稿→題庫 CLP-1/APEX/Mooculus 對症選題→AI 備援）；subagent [`../.claude/agents/example-supplement.md`](../.claude/agents/example-supplement.md)；產 `ch{NN}_example-supplement-review.html`。
- **②波 軟深度**＝intuition/caution/application/strategy/summary/history（**不含 example**）；依 [`README.md`](README.md) §Mode C 的 9 鏡頭擴增檢查表；subagent [`../.claude/agents/mode-c-gapwalk.md`](../.claude/agents/mode-c-gapwalk.md)；產 `REVIEW-ch{NN}-modec-enrichment.html`。
- 兩波都標 `<!-- expansion:<cat> [pass: enrichment] [source: …] -->`（`[pass:]` 在 `[source:]` 前），且**都必接範圍限定的 Mode B**（README 硬規則）。

## 難度閘（gate 7，2026-07-03 新增）

源起與首次全流程執行紀錄：[`_audit/REVIEW-ch01-ch04-difficulty-mitigation-applied.html`](_audit/REVIEW-ch01-ch04-difficulty-mitigation-applied.html)（Ch1–Ch4 難度評估＋修補＋複驗三輪）。規格：

- **Persona（釘死）**＝[`../CONTENT_SPEC.md`](../CONTENT_SPEC.md) §16.2 基線讀者：108 課綱數A（不含選修數甲）、無微積分先備、英文中等的自學大一新生；已讀過本章之前的所有章節（吸收不完美）。
- **怎麼跑**：每章 ≥3 份**盲測** learner-sim（不要先告訴 sim 哪裡難），逐節回報：總判定 ok／effortful／stuck、卡點清單（locus＋引文＋severity：blocking／slowdown／minor）、逐節難度 1–5。
- **判準**：任何 **stuck（卡死需外援）＝blocking**；**B 類先備違規**（SPEC §16.2：未就地建立即使用）＝blocking——此項可先用 grep 對 B 類清單機械預檢。mainline 節難度上限＝「effortful 但可自行走完」（SPEC §16.1 難度預算）；超限者要嘛修、要嘛標 foundation／Proof track（[`TYPESETTING_GUIDE.md`](TYPESETTING_GUIDE.md) §10）。slowdown 級為 advisory，逐條裁決。
- **基線比對**：與 Ch1–Ch4 的難度曲線（Ch1–3≈3/5、Ch4=4/5、尖峰 §4.2=4.5——記錄於上述 audit HTML）比對；新章若出現高於 §4.2 的尖峰或整章 >4，屬**弧線層異常**，回 roadmap entry 的深度決策（SPEC §16.3）重議，不在散文層硬修。
- **修完必回歸**：blocking 修補後對修過的節**重跑盲測 sim**（比照 Ch1–Ch4 P3 複驗），確認卡點實際消失、且未引入新卡點。

## 通用紀律

- **雙閘**：gate-1 Claude（免費）→ ⛳ 裁決 → 回歸審核 → （計費徵同意後）gate-2 Codex 跨模型獨立複核。幻覺要穿過兩個獨立模型才會漏——這是雙閘的價值。
- **易懂性 reader-persona（Gate 6，不新開關）：** 易懂性 A 以「**高中生／英文 L2／第一次線性讀**」為錨判（見 [`_audit/PROSE-AUDIT-RUBRIC.md`](_audit/PROSE-AUDIT-RUBRIC.md) 維度 A）。可選**每章定稿前**用一個外部模型跑一輪 first-read 補強（gate-2 flavor），但**餵乾淨 inline 文字**（Codex 自讀檔在本機會把 UTF-8 解成亂碼＝假陽性）、raw 輸出過四級 triage 再裁決。其中「先用後定義」的**結構性排序**宜更早在 Mode A 方向層攔（[`../CONTENT_DIRECTION.md`](../CONTENT_DIRECTION.md) §2），別留到散文閘才搬而 cascade 編號。
- **Codex 調用（實證，照這個）**：用 **PATH 上的 `codex`**（npm `codex-cli 0.136.0`，已登入 ChatGPT、走訂閱配額；**勿**用絕對路徑 `%LOCALAPPDATA%\OpenAI\Codex\bin\codex.exe` 的 alpha 版——其與 `~/.codex/config.toml` 的 `service_tier="default"` 不相容會啟動失敗）。指令：`codex exec -s read-only -C <repo> --output-schema <s.json> -o <out.json> - < <prompt.txt>`（Bash 工具、prompt 經 stdin 餵 raw UTF-8 避 PowerShell CJK 重編碼；prompt/schema 用 Write 寫檔不用 heredoc）。schema 全欄 required、`additionalProperties:false`、enum、無 min/max。每輪 ~120k tokens。**付費調用前一律先說明模型/用量/成本徵同意**（[`../CLAUDE.md`](../CLAUDE.md)）。
- **findings 留版控**：Codex 原始輸出落 gitignored scratchpad、換機即失 → 轉錄進 `handout/_dev-archive/ch{NN}/ch{NN}_<gate>-audit.md`（範本 `_dev-archive/ch03/ch03_example-supplement-audit.md`）。
- **render 自驗**：node v22＋Chrome。`handout/_render/shot.mjs <url> <out/prefix> {full|figures}`（`figures` 逐圖截 2× PNG 餵圖閘）。驗收：0 KaTeX/MathJax err、0 未渲染 `\(`、env-num 連續無斷號、cross-ref 0 dangling、圖全 hydrate。
- **版面閘（顯示式斷行）**：`node handout/_render/linebreak-gate.mjs`（不帶參數＝掃全部四章 standalone；或接檔名只掃指定章）。抓被 MathJax `displayOverflow:'linebreak'` **自動硬斷**的顯示式（偵測 `mjx-linestack`，再對回原始 TeX），這類自動斷點常很醜。撰寫規則「寬式一律手動斷行」見 [`../CONTENT_SPEC.md`](../CONTENT_SPEC.md) §數學排版「寬顯示式的斷行」。驗收：自動斷行 0 條（退出碼 0）；改完數學式或新增章節後重建再跑一次。
- **編號 ledger 手動**（kit 無 auto-counter，**最大錯誤來源**）：每型獨立 counter、跨節連續；插 example/figure 會 cascade 其後全部編號＋散文 cross-ref。**先建完整編號地圖再動手**，改完 grep 核對連續性與引用解析。ledger 權威表在各章 `_dev-archive/ch{NN}/PLAN-ch{NN}.md` §5。
- **交付物「打開就能讀」**：含數學的待裁決/已套用報告產 standalone HTML（MathJax/KaTeX CDN、雙擊即開）。每完成一輪撰寫都產 `REVIEW-…-applied.html`。
- **commit**：經授權才 commit；繁中、body 逐條記裁決（供 `git log --grep` 撈回）、結尾 `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`。

## 工程注意：subagent 持久化

`.claude/` 被根 `.gitignore`（第 109 行）整個擋掉。要讓 gate subagent 進版控（換機/未來重用），須 **`git add -f .claude/agents/<name>.md`**。目前 `.claude/agents/` 下 **9 個 subagent 皆已 force-add 追蹤**：handout 線 5 個（`example-supplement`、`handout-prose-audit`、`handout-figure-opportunity-audit`、`handout-figure-audit`、`mode-c-gapwalk`）＋ video 線 4 個（`hook-engineering-audit`、`narration-copyedit`、`narration-faithfulness-audit`、`visual-frame-audit`）。**新增 subagent 後務必 force-add**，否則換機即失。

## 各章現況（2026-06-27）

| 章 | 狀態 |
|---|---|
| Ch1 | 全閘跑完（六閘齊） |
| Ch2 | 全閘跑完（與 Ch1 同級） |
| Ch3 | 全閘跑完（與 Ch1/Ch2 同級）——數學 M1–M8 雙閘／圖正確性 gate-2／S·A·V gate-1+2 於 2026-06-27 補齊收斂（執行紀錄 [`_dev-archive/ch03/PROMPT-ch03-remaining-gates.md`](_dev-archive/ch03/PROMPT-ch03-remaining-gates.md)） |
| Ch4 | 全閘跑完（與 Ch1/Ch2/Ch3 同級）——Mode C ①②波＋圖機會/正確性雙閘＋數學 M1–M8 雙閘（gate-2 Codex 173,720 tok）＋S·A·V gate-1+2（gate-2 Codex 154,714 tok，含完整性掃描 3 處 manuscript 去露出）於 2026-06-27 補齊收斂（執行紀錄 [`_dev-archive/ch04/PLAN-ch04.md`](_dev-archive/ch04/PLAN-ch04.md) §8） |
