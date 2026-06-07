# Kickoff prompt — Chapter 2（導數）用新 HTML handout-kit 產出

> 給「換 session」用：把下面 `=== 提示詞 ===` 之間整段貼進新的 Claude Code session。
> 它自帶脈絡（新 session 沒有先前對話記憶）。ch03/ch04 照此改章號／ROADMAP 行號即可重用。

```
=== 提示詞 ===
# 任務：用新的 HTML handout-kit，把 Chapter 2（Derivatives）從手稿重新生成

你沒有先前對話的記憶。先讀檔建立脈絡，再動手。全程用繁體中文跟我溝通
（LaTeX／程式碼／套件名／檔名／scene id 等識別碼與技術術語保留英文原樣）。

## 脈絡
- 專案：NTU 微積分多作者教科書整合。權威規則在 repo 根：CLAUDE.md、README.md、
  CONTENT_SPEC.md、CONTENT_ROADMAP.md。
- 我們改用新的排版規範：一套 HTML/CSS handout-kit（不是 LaTeX）。內容用「語意標記」寫、
  shared/ 引擎自動套樣式，同一份小節檔同時出「線上閱讀版」與「A4 列印版」。
- 已驗證可行：上一個 session 把高風險節 §4.2 從 seed 直接生成 kit 的語意 HTML
  （244 個 KaTeX、0 錯誤、8 頁 A4，螢幕＋列印兩版）。這次照同法做 Chapter 2。

## 動手前務必依序讀（建立脈絡）
1. experiments/handout_kit/CONTRACT-html-writing.md  ← HTML 寫作契約，你要遵的主規範
2. experiments/handout_kit/new-chapter/sec-markup-reference.html  ← 完整標記詞彙（可整段複製改）
3. experiments/handout_kit/exp-ch04/sec-4-2.html  ← 一個完整成品範例，照它的寫法
4. experiments/handout_kit/RESULT-s42-html-poc.md  ← 上次的 findings 與坑（尤其「手動編號／交叉引用」）
5. experiments/handout_kit/README.md  ← 渲染指令 + 檔案地圖
6. experiments/direction_layer/RULE.md  ← 你要跑的「六階流程」＋方向 brief 模板（§2）
7. experiments/seed_converge/rules.md  ← register（語氣／密度，與 LaTeX 版共用）
8. CONTENT_ROADMAP.md 的「Chapter 2 (filled entry)」（約第 156 行起）＋總表第 33 行
   （5 節：2.1 切線與點導數／2.2 導函數／2.3 可微·連續·高階／2.4 多項式與指數函數的導數／
   2.5 乘積與商法則）。這是本章方向的 macro 北極星，brief 要對齊它、引用不複述。

## 輸入：ch02 還沒有 seed（這一步先跟我確認）
ch02 的真來源是老師 2026-04-27 的 13 頁手寫手稿（見 ROADMAP）。請先問我手稿來源，二選一：
- **預設（建議）**：我提供手稿掃描 → 你做 stage ①（逐節轉錄成 seed_ch02_sX.md，忠於手稿、
  含刻意省略）→ 我核對忠實度（①-verify）後才往下。
- **備案**：若我手邊沒掃描，可從 chapters/ch02_derivatives.tex 萃取「數學骨幹」成 seed
  （再走完整 brief→擴寫；這算「重新生成」非「轉檔」）——但你要明講這會 anchor 在舊版結構上，讓我決定。

**不要**逐字把 chapters/ch02_derivatives.tex 轉成 HTML（那是要被取代的舊版，會 anchor）。
內容真理來自「手稿→seed ＋ ROADMAP」。

## 流程：每節跑 direction_layer 六階；先做 §2.1 當「校準首跑」
① intake：手稿→seed（逐節）→ 我核對（①-verify）。**seed 用輕量可讀語法**：反引號行內＋Unicode
   （`lim_{h→0} (f(a+h)−f(a))/h`、`x²`、`x^(n−1)`、`√x`、`≤ ⟺ →`），**不要 `$$…$$`／`\[…\]`／
   `\frac` 等 LaTeX 顯示語法**；seed 是稀疏骨架（漂亮 KaTeX 留給 ④ 輸出）。風格範本：
   experiments/direction_layer/test/seed_s42.md；完整規則見 RULE.md ①。
② 方向 brief：依 seed＋薄度剖析＋ch02 ROADMAP 條目，填 brief（RULE.md §2 九欄模板）
③ 方向閘：我改／核可 brief ← 在此停下等我
④ 擴寫：你是唯一寫手，把該節寫成 experiments/handout_kit/exp-ch02/sec-2-1.html，照
   CONTRACT-html-writing.md：
   - 語意 class（env-definition/theorem/.../workedexample）、行內 \(…\)／獨立 \[…\]、多行 \begin{aligned}
   - **手動編號**（env-num／sec-no／fig-no，章內每型獨立 counter；如 Theorem 2.1, 2.2…）；
     **交叉引用一律純文字**（"Theorem 2.3"、"§1.4 的極限定律"）——kit 無 \cref/自動編號。
     這是上次唯一的真結構性缺口、也是最大錯誤來源：寫完務必自查每個編號引用都對得到一個存在的 env-num。
   - 每處超出 seed 的增添，前一行標 <!-- expansion:<category> — 一行說明 -->
   - 圖：<figure class="figure" data-fig="id"> 佔位 + exp-ch02/figures.js 登錄（buildPlot 或 inline SVG）；
     對齊 ROADMAP 的 key figures（如 §2.2 的 f 與 f' 上下對齊雙圖）。
   - 正確性硬約束：不杜撰定理／恆等式／具名結果／史實；不確定的數學標出來丟我，不靜默改手稿。
⑤ 審查（選配，要才做）：用 codex exec 唯讀 auditor（走 ChatGPT 訂閱、吃配額非按 token 計費）。
   **動手前先問我同意**（會耗我的訂閱配額）。沿用 RULE.md ⑤ 的 blocking/advisory＋四級契約。
⑥ 收斂閘：我簽核；你 render 螢幕＋列印自驗（見下）；把 resolved 的方向叉路回填 ch02 ROADMAP「Open questions」。

## 接上 kit 並渲染（零安裝；本機有 Python 3.12 + 系統 Chrome）
- 複製 experiments/handout_kit/template-screen.html 與 template-print.html → 改名（如 chapter2-screen.html／
  chapter2-print.html），只改最上面 CHAPTER 區塊：dir:"exp-ch04"→"exp-ch02"、fragments 列你的 sec-2-x、
  brand／runningHead 設 Chapter 2 標題（用 PowerShell [IO.File]::WriteAllText 以 UTF-8 無 BOM 寫，保住中文與破折號）。
- 在 experiments/handout_kit/ 起伺服：python -m http.server 8753 --bind 127.0.0.1
- 逐 A4 頁 2x 截圖（CDP，等分頁器跑完）：
  node _render/shot.mjs "http://127.0.0.1:8753/chapter2-print.html" "_render/ch02-print" sheets '(()=>{const b=document.getElementById("printBtn");return !!b && b.disabled===false;})()'
- 看 _render/ch02-*.png 自驗：0 KaTeX 錯誤、編號連續無跳號、交叉引用對得上、無破版（孤行標題／環境裂頁）。
  互動檢視可直接瀏覽器開 http://127.0.0.1:8753/chapter2-screen.html。

## 紀律（CLAUDE.md 的硬規則）
- 隔離沙盒：只動 experiments/handout_kit/exp-ch02/ 與你新建的 chapter2 HTML；**不碰**
  chapters/*.tex、凍結的 video/、main 分支、未 push 的 commit。分支留在 experiment/seed-converge。
- 付費 API 調用前一律先取得我同意；codex 走訂閱吃配額也先問。離線本地路徑（http.server、render）可逕跑。
- 跨對話知識寫進會 git 的文檔（仿 RESULT-s42-html-poc.md 寫一份 ch02 的 RESULT），不要只記本地 memory。
- 先給我一個簡短計畫（步驟→驗證點）再動手；有多種解讀就全攤開問，不要默默選一個。
- 內容散文密度照 Mode A「prefer richness、intuition before formalism」；register 見 rules.md。

## 成功標準（先以 §2.1 為準）
一份 exp-ch02/sec-2-1.html：從 seed 生成（非轉舊 .tex）、完全照 CONTRACT-html-writing.md、
螢幕＋列印兩版渲染 0 KaTeX 錯誤、章內編號與交叉引用一致、擴寫處皆標、過 ③ 與 ⑥ 兩道人閘。
校準 OK 後，再用同法續做 §2.2–§2.5。
=== 提示詞結束 ===
```

## 給使用者的備忘（不用貼進新 session）
- 新 session 第一件事會**問你 ch02 手稿來源**——把 13 頁掃描丟給它（或叫它走備案從 .tex 萃取骨幹）。
- 它會在 ③（方向閘）和 ⑥（收斂閘）停下等你；⑤ 若要用 codex 會先問你（吃 ChatGPT 配額）。
- 先只做 §2.1 校準，順了再續 2.2–2.5。ch03/ch04 把本檔章號與 ROADMAP 行號換掉即可重用。
