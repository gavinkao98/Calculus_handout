# Kickoff prompt — Chapter 3 §3.3（Applications of the Chain Rule）

> 給「換 session」用：把下面 `=== 提示詞 ===` 之間整段貼進新的 Claude Code session。自帶脈絡。
> §3.3 **seed 尚未轉錄**——從 ① intake 起跑。本節是 ch03 **末節**（做完即完成手稿涵蓋）。

```
=== 提示詞 ===
# 任務：用 HTML handout-kit 產出 Chapter 3 §3.3（Applications of the Chain Rule）

你沒有先前對話的記憶。先讀檔建立脈絡，再動手。全程用繁體中文跟我溝通
（LaTeX／程式碼／套件名／檔名／識別碼／技術術語保留英文原樣）。

## 脈絡
- 專案：NTU 微積分多作者教科書整合。權威規則在 repo 根：CLAUDE.md、README.md、CONTENT_SPEC.md、CONTENT_ROADMAP.md。
- 排版用 HTML/CSS handout-kit（不是 LaTeX）。分支 experiment/seed-converge、沙盒 handout/exp-ch03/。
- Chapter 2 全章＋ch03 §3.1、§3.2 已過六階（converged、0 blocking），是你的風格／密度／編號校準基準。
- §3.3 是 ch03 第三（末）節，**seed 尚未轉錄**：先做 ① intake（手稿→seed→我 ①-verify）。

## 動手前依序讀（建立脈絡）
1. handout/exp-ch03/PLAN-ch03.md — **ch03 章層方向錨**。**最重要，先讀**（§1 手稿↔ROADMAP、§2 §3.3 範圍、決策 D8/D9/D10、§5 編號 ledger）。
2. handout/exp-ch03/seed_ch03_s1.md — §3.1 seed（seed 語法範本）。
3. handout/exp-ch03/sec-3-1.html、sec-3-2.html — §3.1/§3.2 成品（風格＋**編號接續來源**：讀 sec-3-2.html 末尾）。§3.2 的 chain rule（Theorem 號）、§3.1 的 cos′／tan′ 是本節常引用的對象。
4. handout/CONTRACT-html-writing.md — HTML 寫作契約（**特別 strategy box `<ol class="steps">`**）。
5. authoring/direction_layer/RULE.md — 六階流程＋方向 brief 九欄；**①「seed 轉錄語法」＋ §2「worked example 清單／自創題政策」務必讀**。
6. authoring/seed_converge/rules.md — register。
7. CONTENT_ROADMAP.md「Chapter 3 (filled entry)」(~line 211) — macro 北極星；§3.3 對齊 strategy（chain-rule decomposition、logarithmic differentiation）＋ pitfalls（arcsin 域、ln 非正式）。

## 流程：跑 direction_layer 六階（從 ① 起）
① intake：手稿 2023-10-28-chainRule（請我提供掃描）**pp.12–14（應用 ①②③）＋ pp.21–22（Homework）** → exp-ch03/seed_ch03_s3.md。
   **seed 用輕量可讀語法**（比照 seed_ch03_s1.md）。轉錄範圍：
   - 應用①：`d/dx ln x = 1/x`(x>0)，經 `x=e^{ln x}`＋chain rule（用 `(eˣ)′=eˣ`）；
   - 應用②：`d/dx xˣ = (1+ln x)xˣ`(x>0)，log differentiation（`g=ln W=x ln x` 兩邊取導）；
   - 應用③：`d/dy arcsin y = 1/√(1−y²)`(y∈(−1,1))，經 `x=sin⁻¹(sin x)`＋chain rule，注意 `cos x≥0` on `[−π/2,π/2]`；
   - Homework（pp.21–22，**忠實內容、D9 升格 worked example 候選**）：`d/dy arccos y`、`d/dx tan x`（已歸 §3.1 D1，
     §3.3 不重做）、`d/dx sec x`、`d/dx(x ln x − x)=ln x`、`d/dx 2ˣ = 2ˣ ln 2`；多項式 `f′`／求根（代數練習）。
   寫完**停下等我 ①-verify**。
② 方向 brief：填 exp-ch03/brief_s33.md（RULE.md §2 九欄）。納入 PLAN 決策 **D8（ln 非正式、嚴謹延 Ch4，一句 forward-note）、
   D9（HW 升格 worked example，須我 ③ 批准）、D10（不引入 implicit-diff 框架——照手稿 composition-identity 走）**。
   兩個 ROADMAP strategy box：chain-rule decomposition、logarithmic differentiation。
③ 方向閘：**停下等我核可 brief**（含 D9 各 worked example 逐一批准）。
④ 擴寫：寫 exp-ch03/sec-3-3.html（照 CONTRACT）；figure 進 exp-ch03/figures.js（append）；
   chapter3-screen.html／chapter3-print.html 的 fragments 追加 "sec-3-3"。收尾一段 chapter summary（ch03 末節）。
⑤ 審查（要才做，先問我同意）：Codex 唯讀 auditor。做法見 PLAN §6。
⑥ 收斂閘：我簽核；render 自驗；編號回填 PLAN §5；resolved 叉路回填 ROADMAP open questions；
   **三節全收斂後**經我確認可把 ROADMAP ch03 status 標為「manuscript coverage complete」。

## 編號狀態（§3.3 接 §3.2；見 PLAN §5）
**讀 sec-3-2.html 末尾**確認各型 counter，再續編。§3.3 例子多（ln/xˣ/arcsin/arccos/sec/x ln x−x/2ˣ）→ Example 號連續一串；
Strategy 兩個。交叉引用一律純文字（"by the chain rule (Theorem 3.x)"、"§3.1 的 cos′"、"§4.5 will construct ln rigorously"），寫完自查。

## ⚠ 正確性（務必）
- 應用照手稿的 **composition-identity ＋ chain rule** 走（`e^{ln x}=x`、`sin(arcsin y)=y` 取導），**不引入 implicit-diff 框架**（D10）。
- **ln x 在此非正式當「eˣ 反函數」用**，嚴謹建構延 Ch4 §4.5——一句 forward-note 標依賴（D8）。`d/dx 2ˣ`：`2ˣ=e^{x ln 2}` ⇒ `2ˣ ln 2`。
- arcsin 域：`1/√(1−y²)` 僅 `y∈(−1,1)`（端點垂直切線）——caution（ROADMAP pitfall）。
- 不杜撰定理／恆等式／具名結果／史實；不確定標出來丟我、不靜默改手稿；名結果／微妙證明人工查核。

## 題目政策（我 2026-06-07 定）
不自創 bare your-turn／章末練習題（deferred；root README §防護欄、CONTENT_SPEC §14）。**手稿 Homework 屬忠實內容**——
依 D9 可**升格為 worked example**（env-example＋env-solution，含完整解＋講解），但仍須在 ③ 經我逐一批准（題型彼此不同、非換數字同型題）。
多項式求根（HW 3,4）若要用，當 chain/power 計算錨或 deferred 習題，不自創無解練習。

## 接 kit 並渲染 / ⑤ Codex 做法 / 硬約束
- 渲染：python -m http.server 8753 --bind 127.0.0.1（在 handout/）；
  node handout/_render/shot.mjs "http://localhost:8753/chapter3-screen.html" handout/_render/s33 full。
  自驗：0 KaTeX 錯誤、編號連續、交叉引用對得上、無破版。**末節：順手全章 render（chapter3-print.html）複驗三節接起來無跳號、無破版。**
- ⑤ Codex（同意後）：codex exec -s read-only --output-schema exp-ch03/_audit/schema.json -o exp-ch03/_audit/result_s33.json - < exp-ch03/_audit/prompt_s33.txt；
  餵 prompt 用 Bash < file（UTF-8）、勿用 PowerShell pipe；prompt 用 Write 寫、別 heredoc；結構鏡像 exp-ch02/_audit/prompt_s24.txt。詳見 PLAN §6。
- 硬約束（CLAUDE.md）：只改 exp-ch03/、chapter3 HTML、PLAN／brief；不碰 chapters/*.tex、凍結 video/、main、未 push commit。
  付費／訂閱 API 先問我同意。跨對話知識寫進 git 文檔、不寫本地 memory。先給簡短計畫（步驟→驗證點）；多解讀全攤開問。

## 起手
先讀 PLAN-ch03.md（特別 §1/§2/D8/D9/D10/§5）與 sec-3-1.html／sec-3-2.html，再請我提供手稿掃描，做 ① intake：
轉錄手稿 pp.12–14＋pp.21–22 成 seed_ch03_s3.md，停下等我 ①-verify 後才進 ②。
=== 提示詞結束 ===
```

## 給使用者的備忘（不用貼進新 session）
- 開這個 session 時**把 chainRule 手稿掃描再丟一次**（需要 pp.12–14 應用、pp.21–22 Homework）。
- §3.3 例子最多——HW 的 arccos／sec／x ln x−x／2ˣ 會在 ③ 提案升格 worked example，等你逐一批准。
- 關鍵方向已在 PLAN 定好：**ln 非正式（嚴謹延 Ch4）、不引入 implicit-diff、tan′ 已歸 §3.1（這裡不重做）**。
- §3.3 做完、過 ⑥ 後即完成 ch03 手稿涵蓋——會跟你確認是否更新 ROADMAP ch03 status。
