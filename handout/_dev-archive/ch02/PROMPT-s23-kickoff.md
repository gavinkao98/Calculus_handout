# Kickoff prompt — Chapter 2 §2.3（Differentiability, Continuity, Higher Derivatives）

> 給「換 session」用：把下面 `=== 提示詞 ===` 之間整段貼進新的 Claude Code session。
> 自帶脈絡（新 session 沒有先前對話記憶）。§2.4／§2.5 照此改節號、seed 檔名、編號狀態即可重用。

```
=== 提示詞 ===
# 任務：用 HTML handout-kit 產出 Chapter 2 §2.3（Differentiability, Continuity, and Higher Derivatives）

你沒有先前對話的記憶。先讀檔建立脈絡，再動手。全程用繁體中文跟我溝通
（LaTeX／程式碼／套件名／檔名／識別碼／技術術語保留英文原樣）。

## 脈絡
- 專案：NTU 微積分多作者教科書整合。權威規則在 repo 根：CLAUDE.md、README.md、
  CONTENT_SPEC.md、CONTENT_ROADMAP.md。
- 排版用 HTML/CSS handout-kit（不是 LaTeX）：語意標記寫內容、shared/ 引擎自動套樣式，
  同一份小節檔同出「線上閱讀版」與「A4 列印版」。分支 experiment/seed-converge。
- §2.1、§2.2 已完成並通過六階＋Codex 審核（converged、0 blocking）。它們是你的
  **風格／密度／編號校準基準**——照它們的寫法。

## 動手前依序讀（建立脈絡）
1. handout/CONTRACT-html-writing.md — HTML 寫作契約（主規範；env 詞彙在此）
2. authoring/direction_layer/RULE.md — 六階流程＋方向 brief 模板（§2 九欄）。
   **務必讀 §2「worked example 清單」列的「自創題政策」**（見下「題目政策」）。
3. handout/exp-ch02/sec-2-1.html 與 sec-2-2.html — 兩個完成的校準成品，
   照它們的結構／密度／手動編號／交叉引用寫法。
4. handout/exp-ch02/brief_s21.md、brief_s22.md — brief 範例（九欄怎麼填）。
5. authoring/seed_converge/rules.md — register（語氣／密度，與 LaTeX 版共用）。
6. CONTENT_ROADMAP.md 的「Chapter 2 (filled entry)」（約 156 行起）——本章 macro 北極星；
   brief 對齊它的 core skills／key figures／pitfalls／open questions，引用不複述。
7. seed：handout/exp-ch02/seed_ch02_s3.md（手稿 pp. 6–7）。

## 流程：跑 direction_layer 六階
② 方向 brief：依 seed＋薄度剖析＋ROADMAP，填 brief_s23.md（RULE.md §2 九欄模板）。
③ 方向閘：**停下等我核可 brief**（先於任何擴寫）。
④ 擴寫：你是唯一寫手，寫 exp-ch02/sec-2-3.html（照 CONTRACT）；Figure 進
   exp-ch02/figures.js（**追加，別覆蓋** secant-to-tangent、f-and-fprime）；章範本
   chapter2-screen.html／chapter2-print.html 的 fragments 陣列追加 "sec-2-3"。
⑤ 審查（要才做）：Codex CLI 唯讀 auditor（走 ChatGPT 訂閱、吃配額非按 token 計費）。
   **動手前先問我同意。** 做法見下。
⑥ 收斂閘：我簽核；你 render 自驗；resolved 的方向叉路回填 ROADMAP「Open questions」。

## 編號狀態（§2.3 從這裡接續；手動編號，kit 無自動 counter）
讀 sec-2-2.html 末尾確認後，續編（章內每型獨立 counter、跨節連續）：
- Definition → **2.3**（differentiable）
- Theorem → **2.1**（本章首個定理：differentiable ⇒ continuous）
- Example → **2.11**（接 §2.2 的 Example 2.10）
- Remark → **2.5**（接 §2.2 的 Remark 2.4）
- Figure → **2.3**（|x| corner）
- Strategy → **2.2**（若需要；§2.3 未必有）
- 章內 **Exercise = 0**（見題目政策）。交叉引用一律純文字（"by Theorem 2.1"、"see §2.2"），
  寫完自查每個引用都對得到一個存在的編號。

## §2.3 內容範圍（從 seed；忠於手稿）
- Definition 2.3：differentiable at a；on an interval。
- Example（不可微）：f(x)=|x| 在 x=0，lim_{h→0} |h|/h 左 −1、右 +1 → 不存在。
- Figure 2.3（ROADMAP key figure）：|x| 的 V 形，標左右單側割線斜率不一致。
- Theorem 2.1 ＋ 證明：differentiable ⇒ continuous。**證明照手稿結構**：
  f(x)−f(a) = [(f(x)−f(a))/(x−a)]·(x−a)，兩極限都存在 → 乘積 = f'(a)·0 = 0。
  逆不成立（|x|）。用 env-theorem ＋ env-proof（證明結尾 <span class="qed qed-proof"></span>）。
- Caution（ROADMAP pitfall）：differentiable ⇒ continuous 是單向；|x| 在 0 是標準反例。
  用 env-caution。
- Higher derivatives 子節：f''、f'''、…、f^(n)，引入記號。
  **ROADMAP Open question：高階導數放 §2.3 子節 vs 獨立節——在 brief 標記待我簽核。**

## ⚠ 高風險節（務必）
§2.3 是本章**首個含具名定理＋證明**的節。數學正確性與**對手稿的忠實度**是硬約束：
- 證明照手稿方法走，不另創證法、不發明引理。
- 不杜撰定理／恆等式／具名結果／史實；不確定標出來丟我，不靜默改手稿。
- 名結果／微妙證明／史實一律人工查核。

## 題目政策（我 2026-06-07 定，務必遵守）
- **不自創 bare your-turn／章末練習題**（無解練習題）——習題設計 deferred
  （root README.md §防護欄「自創習題——習題庫來自手稿」、CONTENT_SPEC.md §14）。
- **但**可自創新題，須：(1) **經我批准**、(2) 題型與既有 example **不同**（非換數字／係數的同型題）、
  (3) 寫進課文時**一律當 worked example**（env-example＋env-solution，含完整解題過程＋講解）。
- 手稿自帶的 example／exercise 照收（那是忠實內容）。
- 詳見 RULE.md §2「worked example 清單」列。

## 接 kit 並渲染（零安裝；本機 Python 3.12 + 系統 Chrome）
- 在 handout/ 起伺服：python -m http.server 8753 --bind 127.0.0.1
- 截圖自驗：node handout/_render/shot.mjs
  "http://localhost:8753/chapter2-screen.html" handout/_render/s23 full
- 自驗：0 KaTeX 錯誤（shot.mjs 會印 katex-errors=）、編號連續無跳號、交叉引用對得上、無破版。
- 互動檢視：瀏覽器開 http://localhost:8753/chapter2-screen.html。
- 要單看某環境可裁切：用 CDP 取元素 rect 後 Page.captureScreenshot（參考 §2.2 做法）。

## ⑤ Codex 審核做法（取得我同意後）
- 工具：codex exec -s read-only --output-schema exp-ch02/_audit/schema.json
  -o exp-ch02/_audit/result_s23.json - < exp-ch02/_audit/prompt_s23.txt
- **餵 prompt 用 Bash 的 `< file` 重導**（原始 UTF-8 bytes＋EOF）；**勿**用 PowerShell
  Get-Content | pipe——會把中文／Unicode 數學符號編碼成亂碼。
- prompt 結構鏡像 exp-ch02/_audit/prompt_s22.txt：instructions header → SEED → DIRECTION BRIEF
  → DRAFT(HTML) → FIGURE RENDERING NOTE（**把 figures.js 的該節 entry 原始碼嵌進去**，
  否則 auditor 會誤報「figure missing」，因它只看到靜態空 <figure>）→ HTML WRITING RULES → 最後指令。
- blocking 只留 math／faithfulness／direction-conformance；格式 nit 走 advisory。
- reasoning 模型 run-to-run 會飄 → 重要判斷多跑取聯集；停在一次乾淨 audit（converged=true、0 blocking）。
- 配額是真成本（per-5h／每週上限），per-section 限次。

## 硬約束（CLAUDE.md）
- 只改 handout/exp-ch02/、chapter2 HTML、以及策略／紀錄文檔（RULE.md、briefs）；
  **不碰** chapters/*.tex、凍結的 video/、main 分支、未 push 的 commit。
- 付費／訂閱 API（Codex）調用前一律先取得我同意。離線本地路徑（http.server、render、mock）可逕跑。
- 跨對話知識寫進會 git 的文檔（不寫本地 Claude memory）。
- 先給我簡短計畫（步驟→驗證點）再動手；有多種解讀全攤開問，不要默默選一個。

## 起手
先讀 seed_ch02_s3.md，再讀 sec-2-1.html／sec-2-2.html 與 RULE.md，然後產出 §2.3 的
② direction brief（brief_s23.md），停下等我核可後才進 ④。一節做完、過 ⑥ 後再做下一節。
=== 提示詞結束 ===
```

## 給使用者的備忘（不用貼進新 session）
- 接續編號的權威來源是 `sec-2-2.html`（末尾的 Example 2.10、Remark 2.4 等）；新 session 會自行核對。
- §2.3 是高風險節（首個定理＋證明）——正好壓測「兩模型會不會一起替幻覺背書」。⑤ 多跑幾次取聯集。
- 高階導數放 §2.3 子節 vs 獨立節，是 ROADMAP 的 open question，會在 ③ 等你拍板。
- §2.4／§2.5 重用本檔：改節號、seed 檔名（s4／s5）、編號狀態（讀當時的 sec-2-3／sec-2-4 末尾）。
