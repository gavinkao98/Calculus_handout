# Chapter 4 「大方向」—— 方向 map + 跨 session 狀態錨

> **Chapter 4: The Exponential and Logarithmic Functions.**
> 每個小節各開**新 session** 執行；新 session 先讀本檔，再讀對應的 `PROMPT-s4X-kickoff.md`（待建）。
> 本檔是 ch04 的**章層方向錨**：手稿↔ROADMAP 對應、逐節範圍、章層方向決策、編號 ledger、工程坑、狀態。
> 隔離：`experiment/seed-converge` 分支。**不碰** `legacy/tex_handout/chapters/*.tex`（凍結）、凍結的 `video/`、`main`、未 push 的 commit。
>
> **權威依據（引用、不複述）：**
> - 六階流程＋方向 brief 九欄模板：[`../../../CONTENT_DIRECTION.md`](../../../CONTENT_DIRECTION.md)（已畢業頂層文件，取代舊 `direction_layer/RULE.md`）
> - Mode A/B/C 零件（expansion 類別、具名內容政策、密度校準、擴增稽核）：[`../../../README.md`](../../../README.md) §撰稿工作流程
> - HTML 寫作契約（env 詞彙、手動編號、figures.js）：[`../general/CONTRACT-html-writing.md`](../general/CONTRACT-html-writing.md)
> - 排版／環境集／顯示／記號（HOW，權威）：[`../../../CONTENT_SPEC.md`](../../../CONTENT_SPEC.md)
> - register（語氣／密度）：[`../../../authoring/seed_converge/rules.md`](../../../authoring/seed_converge/rules.md)
> - **macro 北極星**：[`../../../CONTENT_ROADMAP.md`](../../../CONTENT_ROADMAP.md)「Chapter 4（已填 entry）」(~line 262)
> - 校準成品：ch03 全章 [`../../fragments/ch03/`](../../fragments/ch03/)（sec-3-1…3-3，皆過六階＋Codex audit、blocking=0）＋其編排檔 [`../ch03/PLAN-ch03.md`](../ch03/PLAN-ch03.md)
> - **§4.2（重跑中，2026-06-21）**：舊 POC `sec-4-2.html` 與舊 test-pipeline seed/紀錄（`seed_s42.md`／`RESULT_s42.md`）**已刪除**（使用者決定棄 POC、併進正式章流程重跑）；新 ① 產物 [`seed_ch04_s2.md`](seed_ch04_s2.md)（手稿 pp.3–10 重新轉錄）。
> - **signed 數學 cross-check（評分／盲算用、非手稿）**：[`../../../legacy/tex_handout/chapters/ch04_exponential_logarithm.tex`](../../../legacy/tex_handout/chapters/ch04_exponential_logarithm.tex)（LaTeX→HTML 轉移前已簽核的整章；§4.2 重跑以其 §4.2 段為 ground truth 盲算對賬）

---

## 0. 手稿

- 來源：`2023-11-4-ExponentialFunction`（2023-11-04 手寫掃描；2026-04-27 收到；使用者本機 PDF）。**未進版控**（掃描為二進位、屬使用者私有輸入）。
- 已讀 **pp.1–24**（PDF 可渲染全部頁）。內容止於 Homework（pp.23–24）。
- **手稿自有分節 ≠ ROADMAP 分節**（見 §1 對應表）。手稿是「課堂線性節奏」：先用後證、把 Rolle/MVT 夾在指數／對數之間（因 `ln` 的建構需要 monotonicity corollary）。handout 須照 ROADMAP 五節重切。

---

## 1. 手稿 → ROADMAP §4.1–§4.5 對應（非 1:1，務必照此切）

| 手稿區塊 | 頁 | 內容 | → ROADMAP 去向 |
|---|---|---|---|
| § Construction of the Exponential function | 1 | `aⁿ`（n copies）、`a^(1/n)`＝`xⁿ−a=0` 正根、`a^q=(a^(1/m))ⁿ`、有理數指數律、Q: `a^r` for r∉ℚ? | **§4.1** |
| Def + 完備性 + 收斂(x>0) | 2–3 | `e^x:=Σ x^n/n!`（x>0）；完備性（單調有界收斂 ×2）；**[e1]** `e^x<∞ ∀x>0` 的尾界證明；末尾的部分和尾界 `0≤e^x−P_k(x)≤(L^{n0}/n0!)(1/2)^{k−n0}` | **§4.1**（收斂 x>0；尾界是 §4.2 的依賴） |
| [e2] 連續性(x>0) + [e3] + (△) + Cauchy + 指數律 | 3–10 | `e^x` 連續(x>0) 的 P_k 三段拆證；`0<e^y<∞`(y<0)；**(△)** 絕對收斂⟹收斂；Cauchy def；收斂⟺Cauchy（手稿 punt）；延拓 x<0；指數律 `e^x e^y=e^{x+y}`（二項式＋雙和拆 (I)(II)） | **§4.2**（已有 POC `sec-4-2.html`） |
| § The derivative of the exponential function | 10–11 | 差分商 `(e^{x+h}−e^x)/h=((e^h−1)/h)e^x`；`|(e^h−1)/h−1|≤|h|`（h∈(−½,½)）；`lim_{h→0}(e^h−1)/h=1` → **`d/dx e^x=e^x`** | **§4.3** |
| § Rolle's Theorem | 11–17 | max/min 定義；ex `cos x`；Fact（[a,b] 連續有最大／最小，不證）；**Thm A**（內部極值 ⟹ `f'=0`）＋證；**Rolle 定理**＋證（Case 1/2）；**MVT**＋證（輔助 `g(x)`） | **§4.4** |
| Corollary + examples + § Logarithmic function | 18–22 | `f'≥0 ⟹ f` increasing（MVT 推論）＋ex（sin on [0,π/4]、`e^x` strictly increasing）；**`ln x`** 定義為 `e^x` 反函數；`ln` 連續（反證）；`ln` 可微 → **`d/dx ln x=1/x`** | **§4.4**（推論）＋**§4.5**（monotonicity→log） |
| Homework | 23–24 | (1) `f'=0⟹f` const；(2) `ln a+ln b=ln(ab)`；(3) 函數方程 `g(x)g(y)=g(x+y), g(1)=e ⟹ g=e^x`；(4) `a^x:=e^{x ln a}`、`a^x b^x=(ab)^x`、`(a^x)^y=a^{xy}=(a^y)^x` | **§4.4／§4.5 worked-example 升格候選**（見 D7；bare exercise 不入 handout body） |

**一句話：** §4.1 ≈ 手稿 pp.1–3（construction＋series def＋completeness＋convergence x>0）；§4.2 ＝ pp.3–10（continuity＋Cauchy/abs-conv＋x<0 延拓＋exponent law；**POC 已存在**）；§4.3 ＝ pp.10–11（derivative of `e^x`）；§4.4 ＝ pp.11–18（Rolle's Thm＋MVT＋monotonicity corollary）；§4.5 ＝ pp.18–22（`ln x` 建構＋連續＋導數）＋HW 升格項。

---

## 2. 逐節範圍（scope）

### §4.1 Construction of the Exponential Function
- **seed**：[`seed_ch04_s1.md`](seed_ch04_s1.md) ✅ 已轉錄（手稿 pp.1–3），**待使用者 ①-verify**。
- **忠實主軸**：有理數指數 `a^q` 建立 → 以 power series **定義** `e^x`（x>0）→ 用完備性＋尾界證 `Σ x^n/n!` 收斂（x>0）。
- **加法（待 ③）**：`e≈2.71828` 與部分和 worked example（D5）、partial-sum 收斂圖（ROADMAP key figure）、「series defines, doesn't derive」caution、geometric-tail strategy box、`a^x=e^{x ln a}` 一行 forward-fence 到 §4.5。
- **首節責任**：建章 opener（learning objectives ← ROADMAP core skills）、`chapter4` standalone／fragments 骨架、`ch04` figures（見 §4）。

### §4.2 Continuity and the Exponent Law for `e^x`
- **狀態：已有 POC 草稿 [`sec-4-2.html`](sec-4-2.html)**（首跑六階收斂、Codex 抓到一處過度推廣已修；見 `RESULT_s42.md`）。seed＝[`seed_s42.md`](../../../authoring/direction_layer/test/seed_s42.md)。
- **本章決策（D2）**：POC 在 §4.1 落地**之前**寫成，其編號（Thm 4.1…、Def 4.1、Prop 4.1–4.3…）假設自己是章首 → **§4.1 落地後必須 renumber**（見 §5）。是否原樣升格 live、或併進正式章流程重跑一遍，**待使用者裁決**。
- **忠實主軸＋已 resolved 方向**：continuity(x>0) P_k 三段拆；(△) abs-conv⟹conv；Cauchy；**收斂⟺Cauchy 展開成完整 Bolzano–Weierstrass＋monotone-subsequence**（ROADMAP resolved、超出手稿——手稿 punt）；x<0 延拓；**指數律完整 6 步證**（ROADMAP resolved）。

### §4.3 The Derivative of `e^x`
- **seed**：⏳ 待轉錄（手稿 pp.10–11）。
- **忠實主軸**：差分商 `((e^h−1)/h)e^x`；bound `|(e^h−1)/h−1|≤|h|`（用 §4.1 的 series＋尾界）；`lim(e^h−1)/h=1` → `d/dx e^x=e^x`。
- **redundancy 注意（ROADMAP open Q）**：Ch2 §2.4 有 informal `(e^x)'=e^x`；§4.3 是嚴格重做，差別在 explicit bound。§4.3 開頭 cross-ref Ch2、點明「這次補上 bound」。重構（Ch2 改 forward-ref）**延後至兩章都簽核後**——本章不動 Ch2。

### §4.4 Rolle's Theorem and the Mean Value Theorem
- **seed**：⏳ 待轉錄（手稿 pp.11–18）。
- **忠實主軸**：max/min 定義；Fact（EVT，陳述不證——手稿明言不證）；Thm A（內部極值⟹`f'=0`）＋證；Rolle＋證；MVT＋證（輔助 g）；推論 `f'≥0⟹increasing`。
- **ROADMAP key figure**：MVT secant–tangent 圖（secant dashed、平行 tangent solid 於內部 c）。
- **strategy（ROADMAP 指派）**：「套用 MVT 前先驗 hypotheses」（[a,b] 連續 vs (a,b) 可微，不對稱）。

### §4.5 Monotonicity and the Logarithmic Function
- **seed**：⏳ 待轉錄（手稿 pp.18–22 ＋ HW 升格項）。
- **忠實主軸**：由 `f'≥0` 得 `e^x` strictly increasing → 定義 `ln x`＝`e^x` 反函數（x>0）→ `ln` 連續（反證）→ `ln` 可微 `d/dx ln x=1/x`（inverse-function 技巧）。
- **加法（D7，待 ③）**：HW `ln a+ln b=ln(ab)`、`a^x=e^{x ln a}` 及其指數律升格 worked example（manuscript-faithful）。
- **ROADMAP key figure**：`e^x`／`ln x` 對 `y=x` 反射（重用 Ch1 reflection setup；`e^x` blue、`ln x` red）。
- **forward-loop close**：Ch3 §3.3 曾非正式用 `ln`、forward-ref 到此 → §4.5 關閉迴路。

---

## 3. 章層方向決策（提案；**各節 ③ 方向閘由使用者核可**，非預先定死）

> 依 CONTENT_DIRECTION「模型提案、人定奪」。下列為我依手稿＋ROADMAP 提的章層方向；落地時各節 brief 會再細化、停在 ③ 等核可。

- **D1 — legacy tex 當 signed 數學 cross-check（非手稿、非內容來源）。** 手稿＝數學主軸；`legacy/tex_handout/chapters/ch04_exponential_logarithm.tex` 是 LaTeX→HTML 前已簽核的同章，**只當盲算對賬的 ground truth**（§4.2 POC 即此用法），不照抄其散文／結構。新具名結果（Bolzano–Weierstrass、Cauchy 等價）一律人工查核。
- **D2 — §4.2 POC 的處置（待使用者裁決）。** `sec-4-2.html` 已收斂但住 `_dev-archive/`、且編號假設自己是章首。選項：(a) §4.1 落地後**renumber 並升格** live（省一次重跑、POC 已過審）；(b) 併進正式章流程**重跑** ⑤（一致性最高、成本一次 Codex）。**預設傾向 (a)**（POC 已端到端收斂、Codex 抓過真問題），但 renumber 後仍須一次 scoped re-audit。
- **D3 — ROADMAP 已 resolved 的兩個方向叉路照辦（§4.2）。** ① 收斂⟺Cauchy **展開**成完整 Bolzano–Weierstrass＋monotone-subsequence（超出手稿；user-directed 2026-04-27）。② 指數律寫**完整 6 步**（非 4 步 outline；user-directed）。POC 已照此。
- **D4 — MVT 留在 §4.4（ROADMAP open Q）。** 手稿把 Rolle/MVT 夾在指數章是因 `ln` 建構需要 monotonicity corollary。未來 applications-of-differentiation 專章草擬時，再於 Mode B **僅提議**移走。本章不移。
- **D5 — §4.1 補 `e` 的值＋部分和（真 expansion，待 ③）。** 手稿**無** `e≈2.718`、無部分和表、無收斂圖。ROADMAP key figure 指定 §4.1 partial-sum 收斂圖。提案：補一個「算 `e` 前幾項部分和」worked example＋收斂圖（低風險 `expansion:example`/`figure`）。
- **D6 — `a^r`(r∉ℚ) 的處理照手稿＋legacy 框架（待 ③）。** 手稿 p.1 拋出「how about `a^r`?」即跳到 series 定義 `e^x`。提案：照 legacy 的「limit-of-rationals 較笨重 → 改走 series，且 `a^x:=e^{x ln a}` 留到 §4.5」一句帶過，不在 §4.1 真的建構 `a^r`（forward-fence 到 §4.5）。
- **D7 — Homework 升格 worked example（待 ③）。** 手稿 HW（pp.23–24）：`ln a+ln b=ln(ab)`（→§4.5，重要對數律）、`a^x=e^{x ln a}`＋其指數律（→§4.5，定義一般指數）、`f'=0⟹const`（→§4.4，MVT 直接推論）皆 **manuscript-faithful**、升格 worked example（含解）。函數方程刻畫 `g(x)g(y)=g(x+y),g(1)=e⟹g=e^x`（HW3）較進階、低優先，**提案略過或降為 remark**，待 ③。**bare your-turn exercise 一律不自創**（root README §防護欄、CONTENT_SPEC §14）。
- **D8 — binomial 記號（§4.2）。** 手稿用 `C^n_k`；本書全程 `\binom{n}{k}`（ROADMAP notation）。POC 已用 `\binom`、首見處 cross-ref 手稿記號。
- **D9 — `P_k` 部分和記號保留（§4.1–§4.2，手稿記號）。** `e`（常數）／`e^x`（函數）在 §4.1 首見加 index；`ln x` 在 §4.5 首見加 index。

> **餵 auditor（direction-conformance 反向檢查）：** 各節 brief 的「刻意不寫」清單須含——§4.1 不在此真的建構 `a^r`（D6 邊界）、不提前做 continuity/exponent law（屬 §4.2）；§4.3 不重證 Ch2 §2.4（cross-ref）；§4.4 不把 MVT 移出本章（D4）；§4.5 不自創 bare exercise（D7）、`ln` 只對 x>0。

---

## 4. 章基礎建設（**§4.1 session 建一次**，後續節沿用）

> 落地細節以 [`../general/CONTRACT-html-writing.md`](../general/CONTRACT-html-writing.md) 與 build 腳本 [`../../build.py`](../../build.py) 為準；比照 ch03（[`../ch03/PLAN-ch03.md`](../ch03/PLAN-ch03.md) §4）。**§4.1 session 開工前先讀 build.py＋一個既有章（如 ch03）確認當前 standalone／fragments 組裝慣例**（避免照本檔臆測）。

1. **章 standalone**：比照 `chapter3-print-standalone.html` 建 `chapter4-*-standalone.html`（由 `build.py` 從 `fragments/ch04/sec-4-*.html` 組裝）。runningHead／brand＝「Chapter 4 · The Exponential and Logarithmic Functions」。寫檔用 UTF-8 無 BOM（保中文／破折號）。
2. **章 opener**：`<header class="chapter-head">`（kicker＋title）＋`.lead`＋learning-objectives list，對齊 ROADMAP ch04 core skills（六條）。放在 `sec-4-1.html` 開頭（ch02/ch03 做法：開章併首節檔）。
3. **figures**：每節 figure append（別覆蓋）；label economy（CONTRACT §Figures）。ROADMAP key figures：§4.1 partial-sum 收斂、§4.4 MVT secant–tangent、§4.5 `e^x`/`ln x` 反射。

---

## 5. 編號 ledger（手動；kit 無 auto-counter，跨 session 最大風險點）

- **規則**：章內**每型獨立 counter、跨節連續**（Theorem 4.1, 4.2, …；Example 4.1, …；Figure 4.1, …）。Caution **無編號**（比照 ch02/ch03）。交叉引用**一律純文字**（"by Theorem 4.x"、"§4.1 的尾界"），無 `\cref`／`\eqref`。
- **接續機制**：後節 session **先讀前節成品 HTML 末尾**確認各型 counter 用到哪，再續編；寫完**自查每個編號引用都對得到一個存在的 `env-num`**。
- **⚠️ §4.2 POC 編號待修（D2 連動）**：`sec-4-2.html` 目前用 Thm `4.1`(continuity x>0)、`4.2`(conv⟺Cauchy)、`4.3`(BW)、`4.4`(continuity ℝ)、`4.5`(exponent law)、Def `4.1`(Cauchy)、Prop `4.1–4.3`、Cor `4.1`、Example `4.1`、Caution `4.1–4.2`。**但 §4.1 會先 mint 數個編號** → §4.2 全部須往後移。**§4.1 落地後立即在此回填 §4.1 實際編號，再據以 renumber §4.2 POC。**
- **§4.1 提案編號（brief ③ 核可後落定、④ 回填）**：

  | 型別 | §4.1 提案 |
  |---|---|
  | Definition | `4.1`＝natural exponential function（power series） |
  | Theorem | `4.1`＝Completeness（單調有界收斂）、`4.2`＝`Σ x^n/n!` converges for x>0 |
  | Strategy | `4.1`＝bounding a series by a geometric tail（D5 加法） |
  | Example | `4.1`＝partial sums of `e`（D5 加法） |
  | Figure | `4.1`＝partial-sum 收斂圖（D5 加法） |
  | Remark | `4.1`＝completeness 區分 ℝ/ℚ（加法） |
  | Caution | 無編號＝series defines, doesn't derive（加法） |

> **§4.1 ④ 落定（2026-06-21）：實際用到的編號＝上表提案原樣**（Definition 4.1；Theorem 4.1 Completeness／4.2 convergence；Strategy 4.1；Example 4.1；Figure 4.1；Remark 4.1；Caution 無編號）。**§4.2 POC 因此自 Theorem 4.3、Definition 4.2 起 renumber（D2 落地時處理）。** 交叉引用（"by Theorem 4.1"／"Theorem 4.2"／"bound (∗)"／"§4.2"）已自查、render 無 dangling。

---

## 6. 工程坑（承 ch01/ch02/ch03，後續節沿用）

- **⑤ Codex prompt 編碼**：餵 prompt 用 **Bash 的 `< file` 重導**（原始 UTF-8 bytes），**勿**用 PowerShell `Get-Content | pipe`（會把中文／Unicode 數學符號編成亂碼——§4.2 首跑實證，見 CONTENT_DIRECTION §5）。prompt 檔用 Write 工具寫、別用 heredoc。
- **⑤ 計費**：Codex 走訂閱／API，配額是真成本（per-5h／每週上限）。**動手前先說明模型＋預估＋徵得使用者同意**（root CLAUDE.md「付費 API 調用須先經同意」）。blocking 只留 math／faithfulness／direction-conformance；格式 nit 走 advisory。reasoning 模型 run-to-run 會飄 → 重要判斷多跑取聯集、停在一次乾淨 audit。
- **渲染自驗**：node `_render/shot.mjs` 或（機器無 node 時）Claude_Preview MCP；查 **0 KaTeX 錯誤**、編號連續無跳號、交叉引用對得上、print 無破版（孤行標題／環境裂頁）。ch04 數學重（多行 aligned 級數、雙和、`\binom`）→ 特別留意 print overflow。
- **figures／chapter HTML**：append 不覆蓋。寫檔 UTF-8 無 BOM。

---

## 7. 逐節狀態（每節 ⑥ 後更新）

| 節 | ① seed | ①-verify | ② brief | ③ gate | ④ draft | ⑤ audit | ⑥ |
|---|---|---|---|---|---|---|---|
| §4.1 Construction | ✅ `seed_ch04_s1.md`（pp.1–3） | 🟢 accepted-by-proceeding（2026-06-21；pending 更正） | ✅ `brief_s41.md` | ✅ 2026-06-21（照提案核可） | ✅ `fragments/ch04/sec-4-1.html`＋章 opener＋`chapter4-print-standalone.html`＋Figure 4.1＋`build.py` ch04（render：0 MathJax err／154 nodes／6 print 頁／0 overflow） | ✅ **converged**。free 4-lens（`wf_b32c202e`）0 blocking／7 advisory（套 1：curly `’`）。Codex gate-2（gpt-5.5 xhigh，使用者同意計費）：**run1** 1 blocking（§4.1 提 `e^0=1` 違 brief 刻意不寫→移除）＋1 advisory（`L^k/k!` 中間步→補回 (∗) 鏈）；**run2 converged 0 blocking**＋2 advisory 皆套（Remark 4.1 根存在補 `a>0`、§4.2 預告措辭精準化＝歸功 (∗)＋product argument）。`result_s41.json`／`result_s41_r2.json`。gate 報告 `_audit/REVIEW-ch04_s41-gate1.html`／`-gate2.html`。render 重驗 0 err／6 頁／0 overflow | ✅ **2026-06-21 使用者簽核** |
| §4.2 Continuity & Exponent Law | ✅ `seed_s42.md` | ✅（2026-06-03） | ✅（首跑） | ✅（首跑） | 🟡 **POC** `sec-4-2.html`（待 D2：renumber 升格／重跑） | 🟡 首跑收斂 | ⏳ 待併入正式章 |
| §4.3 Derivative of `e^x` | ⏳ pp.10–11 | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ |
| §4.4 Rolle & MVT | ⏳ pp.11–18 | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ |
| §4.5 Monotonicity & Logarithm | ⏳ pp.18–22＋HW | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ |

**每節交付物（CLAUDE.md 2026-06-15；gate 報告比照 ch01 慣例分檔）**：除 `chapter4-print-standalone.html`（成品），每節 gate 裁決後**必產兩份獨立 standalone HTML 審核報告**（雙擊即開、MathJax CDN、各含「審核對象」單元 provenance 表＋該閘 verdict＋finding cards）：
> - `_audit/REVIEW-ch04_sNM-gate1.html` — gate 1（免費 Claude 4-lens 對抗審）
> - `_audit/REVIEW-ch04_sNM-gate2.html` — gate 2（計費 Codex，讀 `result_sNM*.json`）
>
> 單一產生器 `_audit/REVIEW-sNM.gen.py` 同時產兩檔（gate-2 讀 JSON、gate-1／單元 map 內嵌）。§4.1 已產：[`_audit/REVIEW-ch04_s41-gate1.html`](_audit/REVIEW-ch04_s41-gate1.html)、[`_audit/REVIEW-ch04_s41-gate2.html`](_audit/REVIEW-ch04_s41-gate2.html)（render 0 MathJax err）。**§4.2 起比照辦理。**

**狀態（2026-06-21）**：§4.1 跑完 ①→⑤——**free 4-lens ＋ Codex gate-2 兩審皆 converged（0 blocking）**，`sec-4-1.html`＋章 opener＋`chapter4-print-standalone.html`＋Figure 4.1 render-clean（0 err／6 頁／0 overflow）。**⑥ 已簽核（2026-06-21 使用者）——§4.1 完成、已 commit。** 下一步：進 §4.2（D2：把既有 POC `sec-4-2.html` renumber 自 Theorem 4.3／Definition 4.2 起、併進正式章流程）。本輪 commit 範圍僅 ch04 §4.1（build.py ch04 entry＋chapter4 standalone＋fragments/ch04＋_dev-archive/ch04）；其餘工作樹既有變更（video/ pipeline、ch03、scratch）不在本輪、未動。**ROADMAP ch04 已填 entry**（含三條 resolved/open question：Cauchy⟺conv、exponent-law detail、MVT placement、§4.3 redundancy）。
