# Kickoff prompt — Chapter 2 §2.5（The Product and Quotient Rules）

> 給「換 session」用：把下面 `=== 提示詞 ===` 之間整段貼進新的 Claude Code session。
> 自帶脈絡（新 session 沒有先前對話記憶）。§2.5 是手稿最後一節（pp. 11–13 of 13），做完即完成本章手稿涵蓋。

```
=== 提示詞 ===
# 任務：用 HTML handout-kit 產出 Chapter 2 §2.5（The Product and Quotient Rules）

你沒有先前對話的記憶。先讀檔建立脈絡，再動手。全程用繁體中文跟我溝通
（LaTeX／程式碼／套件名／檔名／識別碼／技術術語保留英文原樣）。

## 脈絡
- 專案：NTU 微積分多作者教科書整合。權威規則在 repo 根：CLAUDE.md、README.md、
  CONTENT_SPEC.md、CONTENT_ROADMAP.md。
- 排版用 HTML/CSS handout-kit（不是 LaTeX）：語意標記寫內容、shared/ 引擎自動套樣式，
  同一份小節檔同出「線上閱讀版」與「A4 列印版」。分支 experiment/seed-converge。
- §2.1、§2.2、§2.3、§2.4 已完成並通過六階＋Codex 審核（converged、0 blocking）。它們是你的
  **風格／密度／編號校準基準**——照它們的寫法。§2.5 是手稿（pp. 11–13 of 13）的**最後一節**。

## 動手前依序讀（建立脈絡）
1. handout/CONTRACT-html-writing.md — HTML 寫作契約（主規範；env 詞彙在此）
2. authoring/direction_layer/RULE.md — 六階流程＋方向 brief 模板（§2 九欄）。
   **務必讀 §2「worked example 清單」列的「自創題政策」**（見下「題目政策」）。
3. handout/exp-ch02/sec-2-1.html、sec-2-2.html、sec-2-3.html、sec-2-4.html —
   四個完成的校準成品。**特別照 sec-2-4.html**（同為規則＋證明密集節：多 Theorem＋多 proof＋
   Caution＋worked example 的可讀性處理）與 sec-2-3.html（定理＋證明結構）。
4. handout/exp-ch02/brief_s22.md、brief_s23.md、brief_s24.md — brief 範例
   （九欄怎麼填；s24 最近、最貼近本節的「規則密集」型態）。
5. authoring/seed_converge/rules.md — register（語氣／密度，與 LaTeX 版共用）。
6. CONTENT_ROADMAP.md 的「Chapter 2 (filled entry)」（約 156 行起）——本章 macro 北極星；
   brief 對齊它的 core skills／key figures／pitfalls／open questions，引用不複述。
   **本節相關 pitfalls 有三個（見下「特別注意」），務必落實。**
7. seed：handout/exp-ch02/seed_ch02_s5.md（手稿 pp. 11–13）。

## 流程：跑 direction_layer 六階
② 方向 brief：依 seed＋薄度剖析＋ROADMAP，填 brief_s25.md（RULE.md §2 九欄模板）。
③ 方向閘：**停下等我核可 brief**（先於任何擴寫）。
④ 擴寫：你是唯一寫手，寫 exp-ch02/sec-2-5.html（照 CONTRACT）；Figure 若需要進
   exp-ch02/figures.js（**追加，別覆蓋** 既有 entries）；章範本
   chapter2-screen.html／chapter2-print.html 的 fragments 陣列追加 "sec-2-5"。
⑤ 審查（要才做）：Codex CLI 唯讀 auditor（走 ChatGPT 訂閱、吃配額非按 token 計費）。
   **動手前先問我同意。** 做法見下。
⑥ 收斂閘：我簽核；你 render 自驗；resolved 的方向叉路回填 ROADMAP「Open questions」。

## 編號狀態（§2.5 從這裡接續；手動編號，kit 無自動 counter）
讀 sec-2-4.html 末尾確認後，續編（章內每型獨立 counter、跨節連續）：
- Theorem → **2.6**（接 §2.4 的 Theorem 2.5；本節：Product Rule、Quotient Rule 兩個）
- Example → **2.15**（接 §2.4 的 Example 2.14）
- Strategy → **2.2**（接 §2.2 的 Strategy 2.1；ROADMAP 指派本節「selecting among the basic rules」）
- Remark → **2.7**（接 §2.4 的 Remark 2.6；若需要）
- Definition → **2.4**（接 §2.3 的 Definition 2.3；§2.4 未用；本節若需要才用）
- Corollary → **2.2**（接 §2.4 的 Corollary 2.1；本節若需要才用）
- Figure → **2.4**（接 §2.3 的 Figure 2.3；§2.4 未用；本節多半不需圖，brief 決定）
- Caution = **無編號**（比照 §2.3／§2.4 的 Caution）
- 章內 **Exercise = 0**（見題目政策）。交叉引用一律純文字（"by Theorem 2.6"、"see §2.4"、
  "the sum rule of §2.4"），寫完自查每個引用都對得到一個存在的編號。

## §2.5 內容範圍（從 seed；忠於手稿）
seed 兩大塊（外加開頭 recall §2.4 的 sum/difference rule）：
1. **Product rule：**
   - 先打臉：`(fg)' ≠ f'·g'`，**手稿自帶反例** `f=x, g=x² ⇒ fg=x³, (fg)'=3x²`，但 `f'·g'=1·2x=2x`。
   - Proof（定義法＋加減同項技巧）：`f(x+h)g(x+h) − f(x)g(x)
     = (f(x+h)−f(x))·g(x+h) + f(x)·(g(x+h)−g(x))`，除以 `h` 取極限 → `(fg)' = f'g + fg'`。
   - **手稿 Example**：`h(x)=x·eˣ ⇒ h'(x)=eˣ + x·eˣ = eˣ(1+x)`（**用到 §2.4 的 `(eˣ)'=eˣ`**，照收並交叉引用）。
2. **Quotient rule：**
   - Proof（定義法＋加減同項；**手稿這裡改用 `Δx` 記號**）：分子加減 `f(x)g(x)` →
     `(f/g)' = (f'·g − f·g') / g²`。

### 特別注意（三個 ROADMAP pitfalls 都在本節落地）
- **`(fg)' ≠ f'g'` 是本章 headline pitfall**：用 env-caution 收手稿的反例（`f=x, g=x²`）。
  §2.4 已用一句 prose fence 預告過「乘法不像加法那麼乖」；**本節要把它展成正式 caution**（呼應該預告）。
- **Quotient rule asymmetry pitfall**：`(f/g)' = (f'g − fg')/g²` 對 `f`、`g` **不對稱**，分子項序不可顛倒。
  用 env-caution 提醒（符號錯置是最常見錯誤）。
- **`Δx ≡ h` pitfall**：手稿在 quotient 證明改用 `Δx`。§2.2 的 brief **刻意把這個 caution 留到 §2.5**
  （ROADMAP「increment notation」）。用 env-caution 一句點明 `Δx` 與 `h` 在導數脈絡同義。
- **Strategy box（ROADMAP 指派本節）**：`Strategy 2.2 "Selecting among the basic rules"`——
  依算式的**語法形狀**判斷該用 power / product / quotient（哪個 rule）。用 env-strategy＋`<ol class="steps">`。
- 本節密集，**可讀性是寫作挑戰**（兩定理＋兩證明＋多 caution＋strategy＋worked examples）：
  比照 sec-2-4.html 的處理——每條規則前 1 段直覺、規則後行內小示例、worked example 打散公式牆。
- 收尾：§2.5 結束本章的微分法則；可一句 forward-fence 到 Ch3（chain rule／合成函數，本節未涵蓋）。
  **不要**偷跑 chain rule。

## ⚠ 本節特性（規則＋證明密集節，比照 §2.3／§2.4）
§2.5 含**兩個具名定理＋兩個證明**（product、quotient）。數學正確性與**對手稿的忠實度**是硬約束：
- 兩個證明都**照手稿的加減同項技巧**走，不另創證法、不發明引理。
- 不杜撰定理／恆等式／具名結果／史實；不確定標出來丟我，不靜默改手稿。
- 名結果／微妙證明／史實一律人工查核。
- quotient 證明注意定義域前提（`g(x) ≠ 0`、且 `g` 在該點連續使 `g(x+Δx)→g(x)`）——
  忠實補上必要的 domain 條件（§2.4 audit 的教訓：規則陳述別漏定義域）。

## 題目政策（我 2026-06-07 定，務必遵守）
- **不自創 bare your-turn／章末練習題**（無解練習題）——習題設計 deferred
  （root README.md §防護欄「自創習題——習題庫來自手稿」、CONTENT_SPEC.md §14）。
- **但**可自創新題，須：(1) **經我批准**、(2) 題型與既有 example **不同**（非換數字／係數的同型題）、
  (3) 寫進課文時**一律當 worked example**（env-example＋env-solution，含完整解題過程＋講解）。
- 手稿自帶的 example／exercise 照收（那是忠實內容）——本節手稿只有 product rule 的 `x·eˣ` 例、
  **quotient rule 無例**，故 brief 多半要提案新增 worked example（至少一個 quotient rule 例；經我批准）。
- 詳見 RULE.md §2「worked example 清單」列。

## 接 kit 並渲染（零安裝；本機 Python 3.12 + 系統 Chrome）
- 在 handout/ 起伺服：python -m http.server 8753 --bind 127.0.0.1
- 截圖自驗：node handout/_render/shot.mjs
  "http://localhost:8753/chapter2-screen.html" handout/_render/s25 full
- 自驗：0 KaTeX 錯誤（shot.mjs 會印 katex-errors=）、編號連續無跳號、交叉引用對得上、無破版。
- 互動檢視：瀏覽器開 http://localhost:8753/chapter2-screen.html。
- 全頁圖很高（整章四節以上）不好讀；要單看 §2.5 可裁切：用 CDP 取 `article.sec` 第 N 個的
  rect 後 Page.captureScreenshot（§2.4 對話用過 $TEMP 的 shot-sec.mjs，可重建；或直接看全頁底部）。

## ⑤ Codex 審核做法（取得我同意後）
- 工具：codex exec -s read-only --output-schema exp-ch02/_audit/schema.json
  -o exp-ch02/_audit/result_s25.json - < exp-ch02/_audit/prompt_s25.txt
- **餵 prompt 用 Bash 的 `< file` 重導**（原始 UTF-8 bytes＋EOF）；**勿**用 PowerShell
  Get-Content | pipe——會把中文／Unicode 數學符號編碼成亂碼。
- prompt 結構鏡像 exp-ch02/_audit/prompt_s24.txt：instructions header → SEED → DIRECTION BRIEF
  → DRAFT(HTML) → FIGURE RENDERING NOTE（**有圖才把 figures.js 的該節 entry 原始碼嵌進去**，
  否則 auditor 會誤報「figure missing」；**無圖則照 s24 寫「no figure, intentional」**）
  → HTML WRITING RULES → 最後指令。**用 Write 工具寫 prompt 檔，別用 heredoc**（heredoc 會把
  `\\` 收斂成 `\` 弄壞路徑；§2.4 對話踩過）。
- blocking 只留 math／faithfulness／direction-conformance；格式 nit 走 advisory。
- reasoning 模型 run-to-run 會飄 → 重要判斷多跑取聯集；停在一次乾淨 audit（converged=true、0 blocking）。
  （§2.4 經驗：每 run 飄出不同的 level-2/3 advisory 屬正常 drift，別追；blocking 取聯集即可。）
- 配額是真成本（per-5h／每週上限），per-section 限次。

## 硬約束（CLAUDE.md）
- 只改 handout/exp-ch02/、chapter2 HTML、以及策略／紀錄文檔（RULE.md、briefs、
  本 kickoff、CONTENT_ROADMAP 的 Open questions 回填）；
  **不碰** chapters/*.tex、凍結的 video/、main 分支、未 push 的 commit。
- 付費／訂閱 API（Codex）調用前一律先取得我同意。離線本地路徑（http.server、render、mock）可逕跑。
- 跨對話知識寫進會 git 的文檔（不寫本地 Claude memory）。
- 先給我簡短計畫（步驟→驗證點）再動手；有多種解讀全攤開問，不要默默選一個。

## 起手
先讀 seed_ch02_s5.md，再讀 sec-2-1.html～sec-2-4.html 與 RULE.md，然後產出 §2.5 的
② direction brief（brief_s25.md），停下等我核可後才進 ④。§2.5 是手稿最後一節——做完、過 ⑥ 後，
本章手稿涵蓋即完整（可在 ⑥ 後跟我確認是否更新 ROADMAP 的 Chapter 2 status）。
=== 提示詞結束 ===
```

## 給使用者的備忘（不用貼進新 session）
- 接續編號的權威來源是 `sec-2-4.html`（末尾的 Theorem 2.5、Corollary 2.1、Example 2.14、
  Remark 2.6）；新 session 會自行核對。next：Theorem 2.6、Example 2.15、Strategy 2.2。
- §2.5 是規則＋證明密集節（兩定理＋兩證明），且要落實**三個** ROADMAP pitfalls
  （`(fg)'≠f'g'` headline、quotient asymmetry、`Δx≡h`）＋一個 strategy box——⑤ 多跑幾次取聯集。
- 手稿 quotient rule **無 example**；brief 會提案新增 worked example（至少一個 quotient 例），在 ③ 等你批准。
- §2.4 audit 教訓已折入本檔：規則陳述別漏定義域；prompt 檔用 Write 別用 heredoc。
- §2.5 做完即完成手稿 13 頁全部涵蓋；之後 chain rule／trig 等屬 Ch3（另一份手稿）。
