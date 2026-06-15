# Kickoff prompt — Chapter 3 §3.2（The Chain Rule）

> 給「換 session」用：把下面 `=== 提示詞 ===` 之間整段貼進新的 Claude Code session。自帶脈絡。
> §3.2 **seed 尚未轉錄**——從 ① intake 起跑。本節是 ch03 最高風險節（remainder-form chain rule 證明）。

```
=== 提示詞 ===
# 任務：用 HTML handout-kit 產出 Chapter 3 §3.2（The Chain Rule）

你沒有先前對話的記憶。先讀檔建立脈絡，再動手。全程用繁體中文跟我溝通
（LaTeX／程式碼／套件名／檔名／識別碼／技術術語保留英文原樣）。

## 脈絡
- 專案：NTU 微積分多作者教科書整合。權威規則在 repo 根：CLAUDE.md、README.md、CONTENT_SPEC.md、CONTENT_ROADMAP.md。
- 排版用 HTML/CSS handout-kit（不是 LaTeX）。分支 experiment/seed-converge、沙盒 experiments/handout_kit/exp-ch03/。
- Chapter 2 全章＋ch03 §3.1 已過六階（converged、0 blocking），是你的風格／密度／編號校準基準。
- §3.2 是 ch03 第二節，**seed 尚未轉錄**：你要先做 ① intake（手稿→seed→我 ①-verify）。

## 動手前依序讀（建立脈絡）
1. experiments/handout_kit/exp-ch03/PLAN-ch03.md — **ch03 章層方向錨**。**最重要，先讀**（特別 §1 手稿↔ROADMAP 對應、§2 §3.2 範圍、決策 D5/D6/D7、§5 編號 ledger）。
2. experiments/handout_kit/exp-ch03/seed_ch03_s1.md — §3.1 seed（seed 語法範本＋本章記號）。
3. experiments/handout_kit/exp-ch03/sec-3-1.html — §3.1 成品（風格／密度／**編號接續來源**；讀末尾確認 counter 用到哪）。
4. experiments/handout_kit/CONTRACT-html-writing.md — HTML 寫作契約。
5. experiments/direction_layer/RULE.md — 六階流程＋方向 brief 九欄模板（§2）；**①「seed 轉錄語法」務必讀**。
6. experiments/handout_kit/exp-ch02/sec-2-4.html、exp-ch03/seed/brief（§3.1 的 brief_s31.md）— 定理＋證明密集節的處理範例。
7. experiments/seed_converge/rules.md — register。
8. CONTENT_ROADMAP.md「Chapter 3 (filled entry)」(~line 211) — macro 北極星；**特別讀 ch03 open questions 的 Def2 placement 與 squeeze**。

## 流程：跑 direction_layer 六階（從 ① 起）
① intake：手稿 2023-10-28-chainRule（請我提供掃描）**pp.11 ＋ pp.14–20** → 轉錄成 exp-ch03/seed_ch03_s2.md。
   **seed 用輕量可讀語法**（反引號行內＋Unicode，見 RULE.md ①、比照 seed_ch03_s1.md）。轉錄範圍：
   - chain rule 陳述（p.11：`P=f∘g`，`P′(x₀)=f′(g(x₀))·g′(x₀)`）；
   - Def 1（極限式）／Def 2（remainder-form `f(x₀+h)=f(x₀)+mh+R(h)`, `R(h)/h→0`）＋等價（pp.14–15）；
   - chain rule 證明（pp.15–20：remainder-form 串接 m₁m₂，R₃(h)=m₂R₁+R₂(...)，ε-δ 證 `R₃(h)/h→0`）。
   - **手稿 pp.9–11 的 product rule＋diff⇒continuous lemma 不轉進 seed 正文**（已是 Ch2 §2.5／§2.3）；
     在 seed 記一句「手稿此處重證 product rule／diff⇒cont → ch03 cross-ref Ch2，不重證」（決策 D6）。
   寫完**停下等我 ①-verify**（逐字對掃描，特別 remainder-form 證明的每一步 m/R 下標）。
② 方向 brief：填 exp-ch03/brief_s32.md（RULE.md §2 九欄）。納入 PLAN 決策 **D5（Def1/Def2 放此）、D6（product/diff⇒cont 只 cross-ref Ch2、不重證）、D7（不做應用——ln/xˣ/arcsin 是 §3.3）**。
③ 方向閘：**停下等我核可 brief**。
④ 擴寫：寫 exp-ch03/sec-3-2.html（照 CONTRACT）；figure 進 exp-ch03/figures.js（append，如 composed-mapping 圖）；
   chapter3-screen.html／chapter3-print.html 的 fragments 追加 "sec-3-2"。
⑤ 審查（要才做，先問我同意）：Codex 唯讀 auditor。做法見 PLAN §6。**本節是壓測「兩模型會不會一起替幻覺背書」的高風險節，⑤ 多跑取聯集。**
⑥ 收斂閘：我簽核；render 自驗；編號回填 PLAN §5、resolved 叉路（Def2 placement 等）回填 ROADMAP open questions。

## 編號狀態（§3.2 接 §3.1；見 PLAN §5）
**讀 sec-3-1.html 末尾**確認 Theorem／Example／Figure／Definition counter 用到哪，再續編（章內每型獨立、跨節連續）。
§3.2 預期：chain rule = 下一個 Theorem 號；Def 1／Def 2 = Definition 號（§3.1 多半沒用 Definition，從 3.1 起或接續）。
交叉引用一律純文字（"by Theorem 3.x"、"Ch2 §2.5 的 product rule"、"Ch2 §2.3 Theorem 2.1（diff⇒continuous）"、"§3.1 的 cos′"），寫完自查。

## ⚠ 高風險節（務必）—— remainder-form chain rule 證明
數學正確性與**對手稿的忠實度**是硬約束：
- 證明**照手稿的 Def2 remainder-form 串接走**（m₁=g′(x)、m₂=f′(g(x))、R₃=m₂R₁+R₂(m₁h+R₁)，ε-δ 推 R₃/h→0），不另創證法、不發明引理。
- **不重證 product rule、不重證 diff⇒continuous**（D6；cross-ref Ch2）。**不提前做應用**（D7；ln/xˣ/arcsin 屬 §3.3，這裡頂多一句 forward 帶到 §3.3）。
- 不杜撰定理／恆等式／具名結果／史實；不確定標出來丟我、不靜默改手稿；名結果／微妙證明人工查核。
- Def1⇔Def2 等價手稿只說「easy to see」——補一個忠實的簡短雙向論證（標 expansion:formula），別當顯然跳過。

## 題目政策（我 2026-06-07 定）
不自創 bare your-turn／章末練習題（deferred）。可自創新題須 (1) 我批准、(2) 題型與既有 example 不同、(3) 寫成 worked example（含解）。
§3.2 以陳述＋證明為主；若要補「辨識 composition 並套 chain rule」的 worked example（ROADMAP strategy「chain-rule decomposition」），在 ③ 提案等我批准。

## 接 kit 並渲染 / ⑤ Codex 做法 / 硬約束
- 渲染：python -m http.server 8753 --bind 127.0.0.1（在 experiments/handout_kit/）；
  node experiments/handout_kit/_render/shot.mjs "http://localhost:8753/chapter3-screen.html" experiments/handout_kit/_render/s32 full。
  自驗：0 KaTeX 錯誤、編號連續、交叉引用對得上、無破版（長證明小心環境裂頁）。
- ⑤ Codex（同意後）：codex exec -s read-only --output-schema exp-ch03/_audit/schema.json -o exp-ch03/_audit/result_s32.json - < exp-ch03/_audit/prompt_s32.txt；
  餵 prompt 用 Bash < file（UTF-8）、勿用 PowerShell pipe；prompt 用 Write 寫、別 heredoc；結構鏡像 exp-ch02/_audit/prompt_s24.txt。詳見 PLAN §6。
- 硬約束（CLAUDE.md）：只改 exp-ch03/、chapter3 HTML、PLAN／brief；不碰 chapters/*.tex、凍結 video/、main、未 push commit。
  付費／訂閱 API 先問我同意。跨對話知識寫進 git 文檔、不寫本地 memory。先給簡短計畫（步驟→驗證點）；多解讀全攤開問。

## 起手
先讀 PLAN-ch03.md（特別 §1/§2/D5/D6/D7/§5）與 sec-3-1.html，再請我提供手稿掃描，做 ① intake：
轉錄手稿 pp.11＋pp.14–20 成 seed_ch03_s2.md，停下等我 ①-verify 後才進 ②。
=== 提示詞結束 ===
```

## 給使用者的備忘（不用貼進新 session）
- 開這個 session 時**把 chainRule 手稿掃描再丟一次**（新 session 沒有記憶；需要 pp.11、pp.14–20）。
- §3.2 是高風險節（remainder-form chain rule 證明）——正好壓測幻覺假說；⑤ 建議跑、且多跑取聯集。
- 關鍵方向已在 PLAN 定好：**不重證 product rule／diff⇒continuous（cross-ref Ch2）、應用留到 §3.3、Def2 放這節**。③ 會再讓你確認。
- 編號接 §3.1：新 session 會讀 sec-3-1.html 末尾自行續編。
