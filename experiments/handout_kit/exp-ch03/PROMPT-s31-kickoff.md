# Kickoff prompt — Chapter 3 §3.1（Derivatives of the Sine and Cosine Functions）

> 給「換 session」用：把下面 `=== 提示詞 ===` 之間整段貼進新的 Claude Code session。自帶脈絡。
> §3.1 是 ch03 **首節**——seed 已轉錄、待 ①-verify；本節額外負責建**章基礎建設**（chapter3 HTML、figures.js、章 opener）。

```
=== 提示詞 ===
# 任務：用 HTML handout-kit 產出 Chapter 3 §3.1（Derivatives of the Sine and Cosine Functions）

你沒有先前對話的記憶。先讀檔建立脈絡，再動手。全程用繁體中文跟我溝通
（LaTeX／程式碼／套件名／檔名／識別碼／技術術語保留英文原樣）。

## 脈絡
- 專案：NTU 微積分多作者教科書整合。權威規則在 repo 根：CLAUDE.md、README.md、CONTENT_SPEC.md、CONTENT_ROADMAP.md。
- 排版用 HTML/CSS handout-kit（不是 LaTeX）：語意標記寫內容、shared/ 引擎自動套樣式，同一份小節檔同出
  「線上閱讀版」與「A4 列印版」。分支 experiment/seed-converge、沙盒 experiments/handout_kit/exp-ch03/。
- Chapter 2 全章（§2.1–§2.5）已過六階＋Codex audit（converged、0 blocking），是你的風格／密度／編號校準基準。
- §3.1 是 ch03 第一節，且 seed 已轉錄完成（手稿 pp.1–9，待我 ①-verify）。

## 動手前依序讀（建立脈絡）
1. experiments/handout_kit/exp-ch03/PLAN-ch03.md — **ch03 章層方向錨**（手稿↔ROADMAP 對應、逐節範圍、
   章層決策 D1–D10、編號 ledger、章基礎建設、工程坑）。**最重要，先讀。**
2. experiments/handout_kit/exp-ch03/seed_ch03_s1.md — 本節 seed（手稿 pp.1–9）。
3. experiments/handout_kit/CONTRACT-html-writing.md — HTML 寫作契約（env 詞彙、手動編號、figures.js）。
4. experiments/direction_layer/RULE.md — 六階流程＋方向 brief 九欄模板（§2）。
5. experiments/handout_kit/exp-ch02/sec-2-1.html、sec-2-4.html — 校準成品（§2.1 開章節範本；§2.4 定理＋證明密集處理）；
   brief 範例 experiments/handout_kit/exp-ch02/brief_s21.md。
6. experiments/handout_kit/new-chapter/sec-intro.html、sec-markup-reference.html — 章 opener 範本＋標記詞彙。
7. experiments/seed_converge/rules.md — register（語氣／密度）。
8. CONTENT_ROADMAP.md「Chapter 3 (filled entry)」(~line 211) — macro 北極星；§3.1 對齊其 core skills／
   key figures／pitfalls，引用不複述。

## 流程：跑 direction_layer 六階（seed 已完成，從 ② 起）
② 方向 brief：依 seed＋薄度剖析＋ROADMAP，填 exp-ch03/brief_s31.md（RULE.md §2 九欄）。
   **務必納入 PLAN-ch03.md 章層決策 D1–D4**（tan′ 升格、(1−cosθ)/θ、連續性瘦身、squeeze cross-ref §1.5）——§3.1 的方向叉路。
③ 方向閘：**停下等我核可 brief**（先於任何擴寫）。
④ 擴寫：你是唯一寫手，寫 exp-ch03/sec-3-1.html（照 CONTRACT）。**首節基礎建設**（見 PLAN §4）：
   建 chapter3-screen.html／chapter3-print.html、章 opener（chapter-head＋lead＋learning objectives，併入 sec-3-1.html 開頭）、
   起 exp-ch03/figures.js（扇形不等式圖）。
⑤ 審查（要才做）：Codex CLI 唯讀 auditor（走 ChatGPT 訂閱、吃配額）。**動手前先問我同意。** 做法見 PLAN §6。
⑥ 收斂閘：我簽核；你 render 自驗；把 §3.1 實際編號回填 PLAN §5 ledger、resolved 叉路回填 ROADMAP「Open questions」。

## 編號狀態（§3.1 fresh 起；見 PLAN §5）
各型 counter 從 X.1 起。提案：Theorem 3.1（sin′=cos）、3.2（cos′=−sin）、3.3（tan′，若採 D1）；Example 3.1 起；
Figure 3.1（扇形不等式）。Caution 無編號。④ 落定後**回填 PLAN §5 表**。交叉引用一律純文字，寫完自查每個引用對得到存在編號。

## §3.1 內容範圍（從 seed；忠於手稿）
seed 主軸（pp.1–9）：sin 差分商 → 夾擠原理 → 扇形/三角形幾何不等式 (1) → lim sinθ/θ=1 → sin′=cos；
sin/cos 連續性 → cos′=−sin。章層決策（PLAN D1–D4，待我 ③）：
- D1 tan′：補 §3.1 worked example（tan=sin/cos、quotient rule、=sec²x；手稿 HW(2)(i) 升格、manuscript-faithful）。
- D2 (1−cosθ)/θ→0：真 expansion（ROADMAP 學習目標；標準短證）。
- D3 連續性瘦身：cos/sin 連續性「證明」保留（導數極限需要）；連續性「定義」與 odd/even「定義」cross-ref Ch1 §1.3、
  不重新定義；Dirichlet 例降 remark 或略。
- D4 squeeze：cross-ref §1.5，只一句帶用到的 θ↘0 形式，不整段重貼。
- key figure：扇形 OAB＋三角形面積不等式圖（ROADMAP「secant inequality figure」）。

## ⚠ 高風險（務必）
§3.1 含具名定理＋證明（sin′、cos′）＋一個 [請查核]：seed 標了 p.3 扇形面積排序書寫不一致（最終 cosθ≤sinθ/θ≤1 是對的）。
**我會先給你 ①-verify 結果**；擴寫用正確的標準排序，別照抄可能筆誤的中間式。其餘：不杜撰定理／恆等式／具名結果／史實；
不確定標出來丟我、不靜默改手稿；名結果／微妙證明人工查核。

## 題目政策（我 2026-06-07 定）
不自創 bare your-turn／章末練習題（deferred；root README §防護欄、CONTENT_SPEC §14）。可自創新題但須
(1) 我批准、(2) 題型與既有 example 不同、(3) 寫成 worked example（含解＋講解）。手稿自帶／HW 升格的例子照收（忠實內容）；
tan′（D1）即手稿 HW 升格，屬忠實內容。

## 接 kit 並渲染（零安裝；本機 Python 3.12＋系統 Chrome）
- 在 experiments/handout_kit/ 起伺服：python -m http.server 8753 --bind 127.0.0.1
- 截圖自驗：node experiments/handout_kit/_render/shot.mjs "http://localhost:8753/chapter3-screen.html"
  experiments/handout_kit/_render/s31 full
- 自驗：0 KaTeX 錯誤（shot.mjs 印 katex-errors=）、編號連續、交叉引用對得上、無破版。互動檢視瀏覽器開 chapter3-screen.html。
- chapter3-screen.html／chapter3-print.html 用 PowerShell [IO.File]::WriteAllText 以 UTF-8 無 BOM 寫（保中文／破折號）。

## ⑤ Codex 審核做法（取得我同意後；詳見 PLAN §6）
- codex exec -s read-only --output-schema exp-ch03/_audit/schema.json -o exp-ch03/_audit/result_s31.json - < exp-ch03/_audit/prompt_s31.txt
- 餵 prompt 用 Bash 的 < file 重導（原始 UTF-8）；勿用 PowerShell Get-Content | pipe。prompt 檔用 Write 工具寫、別用 heredoc。
- prompt 結構鏡像 exp-ch02/_audit/prompt_s24.txt（含 FIGURE RENDERING NOTE：有圖把 figures.js 該節 entry 原始碼嵌進去）。
  schema 從 exp-ch02/_audit/schema.json 複製到 exp-ch03/_audit/。
- blocking 只留 math／faithfulness／direction-conformance；格式走 advisory。多跑取聯集、停在一次乾淨 audit。

## 硬約束（CLAUDE.md）
- 只改 experiments/handout_kit/exp-ch03/、新建的 chapter3 HTML、策略／紀錄文檔（PLAN、brief）；
  不碰 chapters/*.tex、凍結 video/、main、未 push commit。
- 付費／訂閱 API（Codex）調用前一律先取得我同意。離線本地路徑可逕跑。
- 跨對話知識寫進會 git 的文檔（PLAN-ch03.md／brief），不寫本地 Claude memory。
- 先給我簡短計畫（步驟→驗證點）再動手；有多種解讀全攤開問，不要默默選一個。

## 起手
先讀 PLAN-ch03.md 與 seed_ch03_s1.md，再讀 sec-2-1／sec-2-4 與 RULE.md／CONTRACT，然後產出 §3.1 的
② direction brief（brief_s31.md），停下等我核可後才進 ④。提醒：我會先給你 ①-verify 結果（含 p.3 面積排序的真相）。
=== 提示詞結束 ===
```

## 給使用者的備忘（不用貼進新 session）
- **先做 ①-verify**：對掃描 pp.1–9 核對 seed_ch03_s1.md，特別 **p.3 扇形面積排序**（seed 標了 `[請查核]`）。把結果告訴新 session。
- §3.1 是首節，會多花在建 chapter3 HTML／figures.js／章 opener（一次性，後續節沿用）。
- 章層決策 **D1–D4** 在 ③ 等你拍板（tan′ 是否補、(1−cosθ)/θ 是否補、連續性怎麼瘦身、squeeze 重述或 cross-ref）。
- §3.2／§3.3 用各自的 PROMPT-s32／s33-kickoff.md（從 ① intake 起，seed 尚未轉錄）。
