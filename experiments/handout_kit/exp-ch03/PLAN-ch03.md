# Chapter 3 「大方向」—— 方向 map + 跨 session 狀態錨

> **Chapter 3: Chain Rule and Trigonometric Derivatives.**
> 每個小節各開**新 session** 執行；新 session 先讀本檔，再讀對應的 `PROMPT-s3X-kickoff.md`。
> 本檔是 ch03 的**章層方向錨**：手稿↔ROADMAP 對應、逐節範圍、章層方向決策、編號 ledger、工程坑、狀態。
> 隔離：`experiment/seed-converge` 分支、`exp-ch03/` 沙盒。**不碰** `chapters/*.tex`、凍結的 `video/`、`main`、未 push 的 commit。
>
> **權威依據（引用、不複述）：**
> - 六階流程＋方向 brief 九欄模板：[`../../direction_layer/RULE.md`](../../direction_layer/RULE.md)
> - HTML 寫作契約（env 詞彙、手動編號、figures.js）：[`../CONTRACT-html-writing.md`](../CONTRACT-html-writing.md)
> - register（語氣／密度，與 LaTeX 版共用）：[`../../seed_converge/rules.md`](../../seed_converge/rules.md)
> - **macro 北極星**：[`../../../CONTENT_ROADMAP.md`](../../../CONTENT_ROADMAP.md)「Chapter 3 (filled entry)」(~line 211)
> - 校準成品：ch02 全章 [`../exp-ch02/`](../exp-ch02/)（sec-2-1…2-5，皆過六階＋Codex audit、blocking=0）；designer 黃金範例 [`../example-ch01/`](../example-ch01/)
> - 標記詞彙整段可抄：[`../new-chapter/sec-markup-reference.html`](../new-chapter/sec-markup-reference.html)

---

## 0. 手稿

- 來源：`2023-10-28-chainRule`（手寫掃描；使用者本機 `C:\Users\user\Downloads\2023-10-28-chainRule (1).pdf`）。**未進版控**（掃描為二進位、屬使用者私有輸入）。
- 已讀 **pp.1–22**（pdftoppm 可渲染的全部頁）。內容止於 Homework。
  > ⚠ 檔案 metadata 報 39 頁、實際可渲染 22 頁——多半是尾端空白頁或 metadata 誤差。**若 Homework 之後尚有解答頁，請使用者確認**（不影響分節，但會多出 §3.3 worked-example 素材）。
- **手稿自有分節 ≠ ROADMAP 分節**（見 §1 對應表）——這是 ch03 最關鍵的 intake 發現。

---

## 1. 手稿 → ROADMAP §3.1/§3.2/§3.3 對應（非 1:1，務必照此切）

| 手稿區塊 | 頁 | 內容 | → ROADMAP 去向 |
|---|---|---|---|
| 「§ 三角函數的微分」 | 1–9 | sin 差分商→夾擠原理→扇形不等式→`sinθ/θ→1`→**`sin′=cos`**；sin/cos 連續性 lemma→**`cos′=−sin`** | **§3.1** |
| 「§ 乘法規則與連鎖規則」product rule＋證明 | 9–11 | `(fg)′=f′g+fg′`、反例、加減同項證明 | **不入 ch03**：已是 **Ch2 §2.5**（[`../exp-ch02/sec-2-5.html`](../exp-ch02/sec-2-5.html)）→ §3.2 開頭一句 cross-ref，**不重證** |
| diff⇒continuous lemma | 10 | 可微 ⇒ 連續 | **不入 ch03**：已是 **Ch2 §2.3 Theorem 2.1** → cross-ref；§3.2 chain rule 證明會引用 |
| chain rule 陳述 | 11 | `P=f∘g`，`P′(x₀)=f′(g(x₀))·g′(x₀)` | **§3.2**（headline 定理） |
| 應用 ①②③ | 12–14 | `d/dx ln x = 1/x`(x>0)；`d/dx xˣ = (1+ln x)xˣ`(x>0)；`d/dy arcsin y = 1/√(1−y²)`(y∈(−1,1)) | **§3.3**（⚠ 手稿置於**證明前**；handout **重排到 §3.2 證明之後**——見 D7） |
| Def 1 / Def 2 ＋ 等價 | 14–15 | Def1＝極限式；**Def2＝remainder-form** `f(x₀+h)=f(x₀)+mh+R(h), R(h)/h→0` | **§3.2**（Def2 為 chain rule 證明的工具；ROADMAP open Q 確認放此） |
| chain rule 證明 | 15–20 | 用 Def2 的 remainder-form 串接 + ε-δ tail bound（`R₃(h)/h→0`） | **§3.2** |
| Homework | 21–22 | `d/dy arccos y`、**`d/dx tan x`**、`d/dx sec x`、`d/dx(x ln x − x)`、`d/dx 2ˣ`、多項式 `f′` 與求根 | tan′＋**sec′**→**§3.1**（D1＋③ 移入，Example 3.2）；arccos/(x ln x−x)/2ˣ→**§3.3** worked examples（D9）；多項式 f′→§3.2/§3.3 計算錨或 deferred 習題 |

**一句話：** §3.1 ≈ 手稿 pp.1–9 ＋ HW 的 tan′；§3.2 ＝ chain rule 陳述＋Def1/Def2＋證明（product rule／diff⇒cont 只 cross-ref Ch2，不重證）；§3.3 ＝ 全部應用（ln, xˣ, arcsin, arccos, sec, x ln x−x, 2ˣ）。

---

## 2. 逐節範圍（scope）

### §3.1 Derivatives of the Sine and Cosine Functions
- **seed**：[`seed_ch03_s1.md`](seed_ch03_s1.md) ✅ 已轉錄（手稿 pp.1–9），**待使用者 ①-verify**（特別 p.3 扇形面積排序 `[請查核]`）。
- **忠實主軸**：`sin′=cos`、`cos′=−sin`（含其所需的 `sinθ/θ→1` 與 sin/cos 連續性）。
- **加法（待 ③）**：tan′（D1）、`(1−cosθ)/θ→0`（D2）、連續性素材瘦身（D3）、squeeze 重述 vs cross-ref §1.5（D4）。
- **首節責任**：建章 opener、`chapter3-screen/print.html`、`exp-ch03/figures.js`（見 §4）。

### §3.2 The Chain Rule
- **seed**：⏳ 待轉錄（手稿 **pp.11, 14–20**：chain rule 陳述＋Def1/Def2＋等價＋remainder-form 證明）。
- **忠實主軸**：chain rule 陳述、Def2、用 Def2 的 remainder-form 證明（ε-δ tail bound）。
- **cross-ref 不重證（D6）**：product rule＝Ch2 §2.5、diff⇒continuous＝Ch2 §2.3 Theorem 2.1。手稿 pp.9–11 的這兩段**只在 §3.2 開頭用一句帶過**，不搬進來。
- **承重直覺**：chain rule 是「外層導數 × 內層導數」，remainder-form 把它變成可乘的線性近似串接。
- **可能 figure**：ROADMAP key figure「chain rule as composed mapping」（input→intermediate→output 三軸，小 h 經兩段斜率放大）。

### §3.3 Applications of the Chain Rule
- **seed**：⏳ 待轉錄（手稿 **pp.12–14** 應用①②③ ＋ **pp.21–22** Homework 的可升格項）。
- **忠實主軸**：`d/dx ln x = 1/x`、`d/dx xˣ`（log differentiation）、`d/dy arcsin y`。
- **加法（D9）**：arccos′、`(x ln x − x)′ = ln x`、`2ˣ′ = 2ˣ ln 2`（皆手稿 HW，升格為 worked example）。**sec′ 已於 §3.1 Example 3.2(b) 處理（③ 移入），§3.3 不重做。**
- **forward-fence（D8）**：ln x 在此**當「eˣ 的反函數」非正式用**（`e^{ln x}=x` 取導），嚴謹建構**延到 Ch4**——一句 note 標明依賴。
- **strategy（ROADMAP 指派）**：Chain-rule decomposition、Logarithmic differentiation 兩個 strategy box。

---

## 3. 章層方向決策（提案；**各節 ③ 方向閘由使用者核可**，非預先定死）

> 依 RULE.md「模型提案、人定奪」。下列為我依手稿＋ROADMAP 提的章層方向；落地時各節 brief 會再細化、停在 ③ 等核可。

- **D1 — tan′ 放 §3.1（升格 HW）。** ROADMAP core skill 明列「derive d/dx tan x using the quotient rule」於 §3.1；手稿 HW(2)(i) 有 tan′。→ §3.1 補一個 tan′ worked example（`tan=sin/cos`、quotient rule、`=sec²x`），manuscript-faithful。
- **D2 — `(1−cosθ)/θ→0` 放 §3.1（真 expansion）。** ROADMAP 學習目標列了，全手稿無。標準短證（`(1−cosθ)/θ = (1−cos²θ)/(θ(1+cosθ)) = (sinθ/θ)·(sinθ/(1+cosθ))→1·0`）。低風險加法。
- **D3 — §3.1 連續性素材瘦身。** 手稿 §A 內含「連續定義＋Dirichlet 處處不連續例＋odd/even 定義」——與 **Ch1 §1.3** 重疊。提案：**保留** cos/sin 連續性的證明（`cos′/sin′` 的極限真的需要它），但連續性「定義」與 odd/even「定義」**cross-ref Ch1、不重新定義**；**Dirichlet 例降為一句 remark 或略去**（屬 Ch1 風味的離題）。待 ③。
- **D4 — squeeze 重述 vs cross-ref §1.5。** ROADMAP open question。手稿完整重述夾擠原理（兩式）。提案：**cross-ref §1.5**，只在 §3.1 用到的 `θ↘0` 形式上一句帶過，不整段重貼。待 ③。
- **D5 — Def1/Def2 放 §3.2。** ROADMAP open question確認：Def2（remainder-form）在 §3.2 引入（chain rule 證明所需），證 Def1⇔Def2 等價後只用 Def2 證 chain rule。
- **D6 — product rule／diff⇒continuous 不重證、cross-ref Ch2。** 手稿 pp.9–11 重證了 Ch2 已有的兩件事；ch03 **只 cross-ref**（§2.5 product rule、§2.3 Theorem 2.1）。嚴禁在 §3.2 重新展開 product rule 證明。
- **D7 — 應用重排到證明之後。** 手稿先用 chain rule 算 ln/xˣ/arcsin（pp.12–14）才證（pp.15–20）。handout 照 ROADMAP：**§3.2 先 state＋prove chain rule，§3.3 才應用**。理由：handout 自足性要求「用之前先證」；手稿的「先用後證」是課堂節奏，不是邏輯順序。
- **D8 — ln x 在 §3.3 非正式、嚴謹建構延 Ch4。** §3.3 用 `e^{ln x}=x`＋chain rule 取出 `d/dx ln x=1/x`；ln 的嚴謹定義（eˣ 反函數）是 Ch4 §4.5。一句 forward-note 標依賴（同 ROADMAP ch03 pitfall）。
- **D9 — HW 應用升格 worked example。** arccos′（同 arcsin 技巧）、`(x ln x−x)′`、`2ˣ′` 為手稿 HW → 升格為 §3.3 worked examples（**manuscript-faithful 內容**，非自創題；含解＋講解）。**sec′ 原列此處，③（2026-06-08）已移入 §3.1 Example 3.2(b)（同 quotient-rule 技巧，與 tan′ 並列）；§3.3 不再包含 sec′。**多項式 f′／求根（HW 3,4）屬代數練習，可作 §3.2 chain/power 計算錨或 deferred 習題。**bare your-turn exercise 一律不自創**（root README §防護欄、CONTENT_SPEC §14）。
- **D10 — 隱函數微分（implicit diff）不開。** ROADMAP open question：arcsin/xˣ 本質是 implicit-diff 包裝成 composition-identity chain rule。手稿就走 composition-identity（`sin(arcsin y)=y` 取導）——**照手稿**，不引入 implicit-diff 框架（延到未來專章）。

> **餵 auditor（direction-conformance 反向檢查）：** 各節 brief 的「刻意不寫」清單須含——§3.2 不得重證 product rule（D6）、不得提前做應用（D7 邊界）；§3.3 不得做 ln 的嚴謹建構（D8）、不得引入 implicit-diff 框架（D10）、不得自創 bare exercise（D9）。

---

## 4. 章基礎建設（**§3.1 session 建一次**，後續節沿用）

1. **`chapter3-screen.html` / `chapter3-print.html`**：複製 [`../template-screen.html`](../template-screen.html)、[`../template-print.html`](../template-print.html)，只改最上 CHAPTER 區塊：`dir:"exp-ch03"`、`fragments:[...]`（先 `sec-3-1`，後續節 append）、`brand`／`runningHead`＝「Chapter 3 · Chain Rule and Trigonometric Derivatives」。**用 PowerShell `[IO.File]::WriteAllText` 以 UTF-8 無 BOM 寫**（保中文／破折號）。math `macros:{}` 區塊：若需 `\arccsc` 等比照 ch02。
2. **章 opener**：用 `<header class="chapter-head">`（`.ch-kicker`+`.ch-title`）＋`.lead`＋learning-objectives list，照 [`../new-chapter/sec-intro.html`](../new-chapter/sec-intro.html)。**放在 `sec-3-1.html` 開頭**（ch02 的做法：開章節併在首節檔；不另開 sec-intro，除非 §3.1 session 覺得太長）。learning objectives 對齊 ROADMAP ch03 core skills。
3. **`exp-ch03/figures.js`**：每節 figure 進此檔（**append、別覆蓋**）；buildPlot 或 inline SVG，labels 用真 `\(…\)` TeX。**label economy**（CONTRACT §Figures）：圖內只留最小標註，其餘進 caption／散文。

---

## 5. 編號 ledger（手動；kit 無 auto-counter，跨 session 最大風險點）

- **規則**：章內**每型獨立 counter、跨節連續**（Theorem 3.1, 3.2, …；Example 3.1, 3.2, …；Figure 3.1, …）。Caution **無編號**（比照 ch02）。交叉引用**一律純文字**（"by Theorem 3.2"、"§3.1 的 `sinθ/θ→1`"、"Ch2 §2.5 的 product rule"）——無 `\cref`／`\eqref`。
- **接續機制**：§3.2／§3.3 的 session **先讀前一節成品 HTML 末尾**（`sec-3-1.html`／`sec-3-2.html`）確認各型 counter 用到哪，再續編。寫完**自查每個編號引用都對得到一個存在的 `env-num`**（kit 唯一的真結構性稅，ch02 最大錯誤來源）。
- **§3.1／§3.2／§3.3 皆已落定（④/⑥ 回填，2026-06-08）。下表為各節實際用到的編號：**

  | 型別 | §3.1 實際用到 | §3.2 實際用到 | §3.3 實際用到 |
  |---|---|---|---|
  | Theorem | `3.1`= sin′=cos、`3.2`= cos′=−sin | `3.3`= chain rule | —（§3.3 無新定理；`3.4` 未用） |
  | Proposition | `3.1`= sin & cos 連續、`3.2`= `lim sinθ/θ=1` | `3.3`= Def1⇔Def2 等價 | —（§3.3 無；`3.4` 未用） |
  | Definition | （§3.1 無；連續/odd-even cross-ref Ch1） | **`3.1`= remainder form（只此一個；Option B：limit form 的 Def 1 cross-ref §2.2、不另編號）** | —（§3.3 無；arcsin/arccos/arctan 定義 cross-ref Ch1；`3.2` 未用） |
  | Example | `3.1`= companion limit、`3.2`= tan′ & sec′（兩 part）、`3.3`= SHM | `3.4`= √(1+x²)&sin(x²)、`3.5`= √(1+sin²x) 巢狀 | `3.6`= ln′、`3.7`= xˣ、`3.8`= 2ˣ、`3.9`= (x ln x−x)′、`3.10`= arcsin′、`3.11`= arccos′、`3.12`= arctan′ |
  | Figure | `3.1`= 扇形不等式 | `3.2`= composed-mapping（inline SVG） | —（§3.3 無圖；`3.3` 未用） |
  | Remark | `3.1`= 導數四循環 | `3.2`= Leibniz form | `3.3`= one lever for many derivatives |
  | Caution | 無編號（radian 慣例） | 無編號（忘內層導數） | 無編號（arcsin/arccos 域 `(−1,1)`） |
  | Strategy | （§3.1 無） | `3.1`= chain-rule decomposition | `3.2`= logarithmic differentiation |

  > **出入 PLAN 原提案（③ 核可）**：tan′ 採 Example（非 Theorem 3.3）→ §3.2 自 Theorem **3.3** 起；新增 **Proposition** 型（承載連續性與基本極限）；**sec′ 由 §3.3 移入 §3.1** Example 3.2(b)（同 quotient-rule 技巧）→ §3.3 的 D9 清單移除 sec′。交叉引用已自查（DOM audit 確認 0 dangling）。
  > **§3.2 落定（④/⑥ 回填，2026-06-08）**：採 **Option B**——limit form 的 Def 1 cross-ref §2.2、不另編號，§3.2 只用 **Definition 3.1**（remainder form）；等價收 **Proposition 3.3**。chain rule = **Theorem 3.3**；composed-mapping = **Figure 3.2**；Leibniz = **Remark 3.2**；decomposition = **Strategy 3.1**；worked example **3.4/3.5**（皆自創、③ 批准、§3.2 導數庫內）。⑤ 兩模型（Claude 4-lens＋Codex gpt-5.5 ×2 runs）皆 converged、0 blocking。交叉引用自查 0 dangling、render screen 0 KaTeX err／print 13 頁。
  > **§3.3 落定（④/⑥ 回填，2026-06-08）**：applications 全寫 **worked example**（手稿/ledger framing）→ §3.3 **不 mint** 新 Theorem/Proposition/Definition/Figure（`3.4`/`3.4`/`3.2`/`3.3` 留給後續）。Example **3.6–3.12**（ln′/xˣ/2ˣ/(x ln x−x)′/arcsin′/arccos′/arctan′）；Strategy **3.2**（log diff）；Remark **3.3**；Caution 無編號（arcsin/arccos 域）。**arctan′（3.12）為 ③ 核可的自創**，補齊 §3.1 opener＋§3.2 收尾已 shipped 的 arctan 承諾（同 composition-identity 技巧、只用 §3.1 tan′=sec²）。**arccos 用正確 identity `arccos(cos x)=x`**（非手稿 loose 形，①-verify 經使用者授權更正）。⑤ 兩模型（Claude 5-lens＋Codex gpt-5.5 ×4 runs，xhigh，`result_s33{,_r2,_r3,_r4}.json`）：run1 1 blocking（`arcsin(sin x)=x` 未標分支，係我 ⑤ 編輯引入→**獨立 Codex 擋下**）＋advisory 皆修，run2/3/4 連三次 `converged` 0 blocking；幻覺未穿過任一模型。render screen 545 KaTeX/0 err、print 18 頁/0 overflow（§3.3 ≈5 頁）；交叉引用 0 dangling（Ch1/Ch2/Ch4 跨章 ref 為 generic prose、非 defect）。**本機無 node/codex 於 PATH**：render 走 Claude_Preview MCP；Codex 由 `%LOCALAPPDATA%\OpenAI\Codex\bin\codex.exe` 絕對路徑叫（MSIX WindowsApps 版受 ACL 鎖、不可直叫）。

---

## 6. 工程坑（承 ch01/ch02，後續節沿用）

- **⑤ Codex prompt 編碼**：餵 prompt 用 **Bash 的 `< file` 重導**（原始 UTF-8 bytes），**勿**用 PowerShell `Get-Content | pipe`（會把中文／Unicode 數學符號編成亂碼）。prompt 檔**用 Write 工具寫、別用 heredoc**（heredoc 把 `\\`→`\` 弄壞路徑）。
- **⑤ prompt 結構**：鏡像 [`../exp-ch02/_audit/prompt_s24.txt`](../exp-ch02/_audit/prompt_s24.txt)：header → SEED → DIRECTION BRIEF → DRAFT(HTML) → **FIGURE RENDERING NOTE（有圖才把 figures.js 該節 entry 原始碼嵌進去**，否則 auditor 誤報「figure missing」；無圖則寫「no figure, intentional」）→ HTML WRITING RULES → 最後指令。schema：[`../exp-ch02/_audit/schema.json`](../exp-ch02/_audit/schema.json)。
- **⑤ 判讀**：blocking 只留 math／faithfulness／direction-conformance；格式 nit 走 advisory 交 linter。reasoning 模型 run-to-run 會飄 → 重要判斷多跑取聯集、停在一次乾淨 audit（converged、0 blocking）。配額是真成本（per-5h／每週上限），per-section 限次、**動手前先問使用者同意**。
- **渲染自驗**：`python -m http.server 8753 --bind 127.0.0.1`（在 `../`＝handout_kit/ 起）＋ `node ../_render/shot.mjs "http://localhost:8753/chapter3-screen.html" ../_render/s3X full`。自驗：**0 KaTeX 錯誤**（shot.mjs 印 `katex-errors=`）、編號連續無跳號、交叉引用對得上、無破版（孤行標題／環境裂頁）。
  - **機器無 node 時的替代渲染路徑（§3.2 實證，2026-06-08）**：部分機器未裝 node（`shot.mjs` 跑不動）。改用 **Claude_Preview MCP**：建 `.claude/launch.json`（一個 config：`runtimeExecutable`＝python 絕對路徑、`runtimeArgs`＝`["-m","http.server","<port>","--bind","127.0.0.1","--directory","<…/handout_kit 絕對路徑>"]`、`port`）→ `preview_start` → `preview_eval` 在頁面內 `location.href='http://localhost:<port>/chapter3-screen.html'`、輪詢 `document.querySelectorAll('.katex-error').length`（應為 0）、`.katex` 數、`[data-fig] svg` 數；print 版另 `location.href=…chapter3-print.html`、查 `.sheet` 數與各 `.sheet-body` 是否 `scrollHeight>clientHeight`（overflow=破版）。screenshot 工具偶會 timeout（DOM eval 不受影響、以 eval 為準）。launch.json 為一次性 QA 用，驗完可刪。
- **figures.js／chapter HTML**：append 不覆蓋。
- **（LaTeX-only，HTML 不適用）**：ch01 的「TikZ 只用 colorprimary/caution/auxiliary 三色」是 `.tex` 流程的坑；HTML kit 走 `shared/skin-hs.css` 自動上色，不適用。

---

## 7. 逐節狀態（每節 ⑥ 後更新）

| 節 | ① seed | ①-verify | ② brief | ③ gate | ④ draft (sec-3-X.html) | ⑤ audit | ⑥ |
|---|---|---|---|---|---|---|---|
| §3.1 Sine & Cosine | ✅ `seed_ch03_s1.md` | ✅ p.3 掃描校對 | ✅ `brief_s31.md` | ✅ 2026-06-08 | ✅ `sec-3-1.html`＋章 opener＋`figures.js`（render 0 KaTeX err、print 7 頁；Claude 4-dim 對抗審 blocking=0） | ✅ Codex 2 runs（`_audit/result_s31*.json`；run1 2 blocking 修正→run2 **converged**，1 advisory 已套）| ✅ 2026-06-08 使用者簽核 |
| §3.2 Chain Rule | ✅ `seed_ch03_s2.md`（手稿 pp.11,14–20） | ✅ 對掃描校對（3-lens 忠實度檢查＋使用者核；remainder-form 下標逐格對） | ✅ `brief_s32.md`（3-lens design panel 綜合） | ✅ 2026-06-08（Def Option B、intuition-first、收 Fig 3.2、批准 Ex 3.4+3.5） | ✅ `sec-3-2.html`＋Fig 3.2（composed-mapping）＋chapter fragments；render 驗證 screen 370 KaTeX/**0 err**、2 圖 hydrated；print 13 頁/0 overflow（§3.2 ≈6 頁） | ✅ **converged（兩模型 0 blocking）**。Claude 4-lens 對抗審 0 blocking（1 advisory `R₂(0)=0` 已修）＋ Codex gpt-5.5 ×2 runs（xhigh，`result_s32.json`/`_r2.json`）皆 `converged`：run1 0 findings、run2 1 advisory house_rule（level2 marker gap）已補 2 個 expansion 標記。幻覺未穿過任一模型。render 複驗 373 KaTeX/0 err | ✅ 2026-06-08 使用者簽核 |
| §3.3 Applications | ✅ `seed_ch03_s3.md`（手稿 pp.12–14＋21–22；3 份獨立轉錄對賬） | ✅ 對掃描校對（HW(4) 筆誤→`(x−1)⁴`、HW(1) arccos 恆等式逐字確認） | ✅ `brief_s33.md`（3-lens design panel 綜合） | ✅ 2026-06-08（補 arctan′、omit figure、D9 三項全收、results＝worked example） | ✅ `sec-3-3.html`＋chapter fragments（無圖）；render screen 545 KaTeX/**0 err**、print 18 頁/0 overflow（§3.3 ≈5 頁） | ✅ **converged（兩模型 0 blocking）**。Claude 5-lens 0 blocking（2 advisory 已修）＋Codex gpt-5.5 ×4 runs（xhigh，`result_s33{,_r2,_r3,_r4}.json`）：run1 1 blocking（`arcsin(sin x)=x` 未標分支，⑤ 編輯引入→Codex 擋下）＋advisory 皆修，run2/3/4 連三次 `converged`。幻覺未穿過任一模型 | ✅ 2026-06-08 使用者簽核 |

**狀態（2026-06-08）**：§3.1／§3.2／§3.3 **三節皆過 ⑥ 收斂閘**（使用者簽核）——**ch03 手稿涵蓋完成**（§3.1–§3.3 全數落地）。編號 ledger（§5）與 ROADMAP ch03 open questions（D8 ln-informal／D10 implicit-diff）已回填。**唯一待辦**：ROADMAP ch03 status 由 `draft` 改標「manuscript coverage complete」——待使用者最終確認後執行（kickoff 約定「三節全收斂後經使用者確認」）。

**ROADMAP 回填**：各節 ⑥ resolved 的方向叉路（尤其 D3/D4 squeeze 與連續性處理、D5 Def2 placement、D10 implicit-diff）回填 [`../../../CONTENT_ROADMAP.md`](../../../CONTENT_ROADMAP.md) ch03 條目的「Open questions」。全章三節收斂後，經使用者確認可把 ch03 status 由 `draft` 標為「manuscript coverage complete（§3.1–§3.3 全數落地）」。
