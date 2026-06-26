# Ch3 收尾 — 剩餘三閘執行 prompt（新對話貼這份）

> **用法：** 開新對話，把本檔內容貼上（或說「執行 `handout/_dev-archive/ch03/PROMPT-ch03-remaining-gates.md`」）。本檔自足，不需先前對話記憶。
> **目標：** 把 Chapter 3 從目前狀態推到「與 Ch1/Ch2 完全同級全跑」，補完最後三道閘，最後更新 ROADMAP status。

---

## 0. 現況（2026-06-27，已 commit）

ch03 三節（§3.1 Sine & Cosine、§3.2 Chain Rule、§3.3 Applications）已完成：
- **Mode A 六階定稿**（2026-06-08，Claude＋Codex 雙模型對抗審 0 blocking、使用者簽核）。
- **圖機會閘＋圖正確性視覺 gate-1**（2026-06-21，7 圖 Figure 3.1–3.7，D1–D8 視覺 gate-1 過、Fig 3.7 一條 D6 修正後回歸）。
- **Mode C ①波 課文範例補充**（commit `b80dd42`）：+4 worked example（CLP-1），全章 Example 重編號 **3.1–3.16**，雙閘收斂（gate-1 Claude 0 blocking、gate-2 Codex 2 blocking→修→回歸）。
- **Mode C ②波 軟深度**（commit `bc8ccee`）：§3.1 +1 caution（極限非恆等式）。

內容檔：`handout/fragments/ch03/sec-3-{1,2,3}.html`（**改課文只改 fragment**，再 `python build.py ch03` 重組 `handout/chapter3-print-standalone.html`）。編號 ledger 權威表：`handout/_dev-archive/ch03/PLAN-ch03.md` §5。章層「刻意不寫」D-邊界：同檔 §3。
分支：`video/template-redesign-navy-spine`（handout 工作都在此，**勿切 main**）。

**還缺三道閘**（這是本任務）：① 數學正確性 M1–M8（gate-1+2）② 圖正確性 gate-2（Codex）③ S·A·V 去 AI 味散文（gate-1+2，含易懂性 A／流暢性 B）。

**「同級」定義（權威）：** `CONTENT_ROADMAP.md` 的 Ch2 status 行末句——「手稿六階＋Mode C（例題＋軟深度）＋去 AI 味 S·A·V（gate-1+2）＋圖機會/正確性兩閘（圖正確性 gate-1+2）＋數學正確性雙閘」。ch03 已有前四項，補這三道即同級。

---

## 1. 通用：雙閘 + Codex 調用紀律（每道閘都照這個）

- **gate-1 = Claude（免費）**：用對應 subagent／rubric 走查 → 出 findings → **⛳ 使用者逐條裁決**（propose-only，套用獲准修正、保語意/數學）→ 回歸審核（改過的重審）。
- **gate-2 = Codex（計費，跨模型獨立複核）**：**動用前必徵使用者同意**（說明模型/用量/成本，CLAUDE.md「付費 API 須先同意」）。
- **Codex 調用實證（重要，照這個才不踩坑）：**
  - 用 **PATH 上的 `codex`**（npm 版 `codex-cli 0.136.0`，已 `Logged in using ChatGPT`、走訂閱配額）。**勿**用絕對路徑 `%LOCALAPPDATA%\OpenAI\Codex\bin\codex.exe`（那是 0.130.0-alpha.5，會因 `~/.codex/config.toml` 的 `service_tier="default"` 不相容而啟動失敗）。
  - config 預設已是 `model=gpt-5.5`、`model_reasoning_effort=xhigh`，不必再傳。
  - 指令樣板（**用 Bash 工具**，prompt 經 stdin 餵 raw UTF-8、避 PowerShell CJK 重編碼）：
    ```bash
    codex exec -s read-only -C "C:/Users/Kao/Downloads/Calculus_handout" \
      --output-schema "<schema.json>" -o "<out.json>" - < "<prompt.txt>"
    ```
  - prompt／schema **用 Write 工具寫檔**（別用 heredoc，會壞 `\\`）。schema：全欄 `required`、`additionalProperties:false`、`level`/`verdict` 用 `enum`、無 `min/max`。
  - 每輪 ~120k tokens。**findings 必須留版控**：Codex 原始輸出落在 gitignored scratchpad，換機即失 → 轉錄進 `handout/_dev-archive/ch03/ch03_<gate>-audit.md`（範本見同目錄 `ch03_example-supplement-audit.md`）。
- **render 自驗工具**：node v22＋Chrome 在本機。`handout/_render/shot.mjs <url> <out/prefix> <mode>`：`full`／`figures`（逐 `<figure>` 截 2× PNG 餵圖閘）。URL 可用 `file:///C:/Users/Kao/Downloads/Calculus_handout/handout/chapter3-print-standalone.html`。印 `ready/math/katex-errors`。DOM 細檢可仿 ch03 ①波用過的 CDP 小檢查（mjx-merror、未渲染 `\(`、env-num 連續、figure svg）。
- **每道閘完成**：`build.py ch03` 重組 → 產 `REVIEW-ch03-<gate>-…applied/gate2.html` 報告（含數學即渲染，比照 ch02 同名檔）→ **取得授權後 commit**（繁中、body 逐條記裁決、結尾 `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`）。
- **建議順序**（互相獨立，可調）：先**數學 M1–M8**（教學內容正確性最高優先）→ **圖正確性 gate-2**（補半套）→ **S·A·V 散文**（去味、polish，最後）。

---

## 2. 閘 A — 數學正確性 M1–M8（gate-1 Claude + gate-2 Codex）

- **契約：** `handout/_audit/MATH-CORRECTNESS-RUBRIC.md`（M1–M8 維度）。參考成品：`handout/_audit/REVIEW-ch02-math-audit.html`、`REVIEW-ch01-math-audit-gate{1,2}.html`。
- **gate-1（Claude）：** 對 §3.1–§3.3 全部定理/命題/例題的數學逐項走查（陳述、證明、worked-example 答案、定義域、符號）。worked-example 答案建議用 **sympy 重算**核對（本機有 python；注意 cp950 終端對 unicode 的限制，輸出純 ASCII）。findings 框架一律「請查核 X」。可多開幾個獨立 auditor 取聯集（ch02 用 ×5）。出 `REVIEW-ch03-math-audit.html`（gate-1 區）。⛳ 使用者裁決。
- **gate-2（Codex，計費徵同意）：** 同 rubric 獨立複核，特別重算 worked example 與定義域。findings 轉錄 `ch03_math-audit-gate2.md`。
- **注意 ch03 已知點**（①波 gate-2 已處理、勿重開）：Ex 3.6 已標 `for x>1`、Ex 3.13 已標 `x>0` 並揭露；arcsin/arccos 域 `(−1,1)`、arccos 用 `arccos(cos x)=x`。
- **收斂＝M1–M8 blocking 全 0**（兩閘）。

## 3. 閘 B — 圖正確性 gate-2（Codex 視覺第二讀者，D1–D8）

- **契約：** `handout/_audit/FIGURE-AUDIT-RUBRIC.md`（D1–D8 視覺正確性）。gate-1 已於 2026-06-21 過（Claude 多 auditor）；**本閘只補 gate-2（Codex）**。參考：`REVIEW-ch02-figure-audit-gate2.html`、`PROMPT-ch02-figure-audit-gate2.md`、`REPORT-ch02-figure-gate2-raw.md`。
- **做法：** `node handout/_render/shot.mjs "file:///…/chapter3-print-standalone.html" <out/s3fig> figures` → 得 7 張 2× PNG（Figure 3.1–3.7：sector-inequality／squeeze-limit／sin-cos-slope／shm-triple／composed-mapping／remainder-tangent／arcsin-vertical-tangent）。把 PNG 用 `codex exec ... -i <png…>` 連同各圖的 `const FIGS` 繪圖源碼／inline-SVG 餵 Codex，依 D1–D8 數值核對（domain、特殊點、標記文字 vs 散文、座標等比與否）。Fig 3.7 須等比座標（slope-1 切線呈 45°，①gate-1 修過）。
- findings 轉錄 `ch03_figure-audit-gate2.md`，出 `REVIEW-ch03-figure-audit-gate2.html`。**收斂＝7 圖 blocking 全 0。**

## 4. 閘 C — S·A·V 去 AI 味散文（gate-1 + gate-2；含易懂性 A／流暢性 B）

- **契約：** `handout/_audit/PROSE-AUDIT-RUBRIC.md`（三維 A 易懂性／B 流暢性／C 語意聲音 S·A·V）＋錨組 `handout/_audit/anchors/svc-exemplars.md`。權威流程：`PLAN-deai-semantic-critic-implementation.md` Task 8（逐章鋪，順序 Ch2→**Ch3**→Ch4，ch3 正是下一棒）。參考成品：`REVIEW-ch02-svc-gate1.html`、`REVIEW-ch02-svc-gate2.html`。
- **gate-1（Claude）：** 派 `handout-prose-audit` subagent（已收編三維＋載錨組）審 §3.1–§3.3 每節散文。S/A blocking＝空句佔承載位或高度錯；其餘 advisory。出 `REVIEW-ch03-svc-gate1.html`。⛳ 使用者逐條裁決改寫/刪（**保語意、不動數學、不碰教學順序**，copyedit 級硬護欄）→ 套用→逐節回歸。
- **gate-2（Codex，計費徵同意）：** 同 PROSE rubric＋svc 錨組獨立審 5… 此處 3 節。findings 轉錄 `ch03_svc-gate2.md`（或併 prose-gate2-raw）。注意 ch02 的 student-facing 散文不可露出「the manuscript」等內容層語氣（HTML 註解 provenance 保留即可）——ch03 一併查。
- Vale 為免費 pre-flag 護欄（`vale handout/fragments/ch03/sec-3-*.html`），非決定性 gate。
- **收斂＝S/A blocking 全 0**（兩閘）。

---

## 5. 收尾 — ROADMAP status

三閘全 0 blocking 後，經使用者確認，把 `CONTENT_ROADMAP.md` 的 **Chapter 3 status** 由
「manuscript coverage complete（§3.1–§3.3，2026-06-08）」改為
**「與 Ch1/Ch2 同級全跑」**（比照 Ch2 status 行的全閘集敘述：手稿六階＋Mode C 例題+軟深度＋S·A·V gate-1+2＋圖機會/正確性 gate-1+2＋數學 M1–M8 雙閘）。

## 6. 順帶（可選，非必要）

- `.claude/agents/handout-figure-opportunity-audit.md` 在工作樹但**被 `.gitignore`（`.claude/`）擋、未版控**——與 `example-supplement.md` 同病（後者①波已 `git add -f` 進版控）。若要讓圖機會閘 subagent 也持久化，`git add -f` 進版控（比照既有作法），經授權後 commit。
