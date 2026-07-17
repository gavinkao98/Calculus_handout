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
- **狀態：✅ ①→⑥ 完成（2026-06-21 重跑、使用者簽核）。** 舊 POC＋test-pipeline seed 已刪（ab5f330）；從手稿 pp.3–10 重新轉錄、併進正式章流程。seed＝[`seed_ch04_s2.md`](seed_ch04_s2.md)、brief＝[`brief_s42.md`](brief_s42.md)、成品 fragment＝[`../../fragments/ch04/sec-4-2.html`](../../fragments/ch04/sec-4-2.html)（已併入 `build.py` ch04＋`chapter4-print-standalone.html`）。
- **本章決策（D2）已裁決**：使用者選 (b) 併進正式流程重跑（非 renumber 舊 POC）；編號自 Theorem 4.3／Definition 4.2 起接 §4.1（見 §5）。
- **忠實主軸＋已 resolved 方向**：continuity(x>0) P_k 三段拆；(△) abs-conv⟹conv；Cauchy；**收斂⟺Cauchy 展開成完整 Bolzano–Weierstrass＋monotone-subsequence**（ROADMAP resolved、超出手稿——手稿 punt）；x<0 延拓；**指數律完整 6 步證**（ROADMAP resolved）。

### §4.3 The Derivative of `e^x`
- **狀態：✅ ①→⑥ 完成（2026-06-21、使用者簽核）。** seed＝[`seed_ch04_s3.md`](seed_ch04_s3.md)、brief＝[`brief_s43.md`](brief_s43.md)、成品 fragment＝[`../../fragments/ch04/sec-4-3.html`](../../fragments/ch04/sec-4-3.html)（已併入 `build.py` ch04＋`chapter4-print-standalone.html`）。雙閘皆 run1 直接 converged（gate-1 0 blocking／gate-2 Codex run1 0 finding——本章首個 run1 全清的節）。
- **seed**：✅ `seed_ch04_s3.md`（手稿 pp.10–11，2026-06-21 轉錄）。
- **忠實主軸**：差分商 `((e^h−1)/h)e^x`；bound `|(e^h−1)/h−1|≤|h|`（用 §4.1 的 series＋尾界）；`lim(e^h−1)/h=1` → `d/dx e^x=e^x`。
- **redundancy 注意（ROADMAP open Q）**：Ch2 §2.4 有 informal `(e^x)'=e^x`；§4.3 是嚴格重做，差別在 explicit bound。§4.3 開頭 cross-ref Ch2、點明「這次補上 bound」。重構（Ch2 改 forward-ref）**延後至兩章都簽核後**——本章不動 Ch2。

### §4.4 Rolle's Theorem and the Mean Value Theorem
- **狀態：✅ ①→⑥ 完成（2026-06-21、使用者簽核）。** seed＝[`seed_ch04_s4.md`](seed_ch04_s4.md)、brief＝[`brief_s44.md`](brief_s44.md)、成品 fragment＝[`../../fragments/ch04/sec-4-4.html`](../../fragments/ch04/sec-4-4.html)（已併入 `build.py` ch04＋`chapter4-print-standalone.html`，含新 Figure 4.2＝`mvt-secant-tangent` FIGS entry＋`.secant`/`.tangent` CSS）。雙閘收斂：gate-1（`wf_39f59234`）4-lens 0 blocking；Codex gate-2 run1 1 blocking（收尾越界預覽 §4.5）→run2 converged。render 0 err／22 頁／0 overflow。
- **seed**：✅ `seed_ch04_s4.md`（手稿 pp.11–18，2026-06-21 轉錄；含兩處 [請查核]：Rolle Case 2 (ii) 筆誤、Corollary strict/non-strict 缺口，均於 ④ 修正）。
- **忠實主軸**：max/min 定義；Fact（EVT，陳述不證——手稿明言不證）；Thm A（內部極值⟹`f'=0`）＋證；Rolle＋證；MVT＋證（輔助 g）；推論 `f'≥0⟹increasing`（落地寫成雙條，補 strict 版供 §4.5）。
- **ROADMAP key figure**：✅ Figure 4.2 MVT secant–tangent 圖（secant dashed、平行 tangent solid 於內部 c；JS FIGS 數值求 c 使 tangent 既觸線又平行）。
- **strategy（ROADMAP 指派）**：✅ Strategy 4.2「套用 MVT 前先驗 hypotheses」（[a,b] 連續 vs (a,b) 可微，不對稱；`|x|` on [−1,1] 反例）。
- **四項選配全取（③ 核可）**：Rolle/MVT 史實一句、Remark 4.4 顯式立框、Example 拆 4.3(sin)/4.4(e^x)、額外 MVT 數值 Example 4.2(x² on [0,2]，c=1)。

### §4.5 Monotonicity and the Logarithmic Function
- **狀態：✅ ①→⑥ 完成（2026-06-21、使用者簽核）。全章最後一節。** seed＝[`seed_ch04_s5.md`](seed_ch04_s5.md)、brief＝[`brief_s45.md`](brief_s45.md)、成品 fragment＝[`../../fragments/ch04/sec-4-5.html`](../../fragments/ch04/sec-4-5.html)（已併入 `build.py` ch04＋`chapter4-print-standalone.html`，含新 Figure 4.3＝`exp-log-reflection` FIGS entry＋`.curve-log`/`.idline` CSS）。
- **seed**：✅ `seed_ch04_s5.md`（手稿 pp.18–22＋HW pp.23–24，2026-06-21 轉錄；**無 [請查核] 級數學疑點**——§4.5 數學乾淨、與 legacy 逐步一致，僅三處筆跡瑕疵已標注）。
- **忠實主軸**：由 §4.4 收割的 `e^x` strictly increasing（⟹單射）→ 定義 `ln x`＝`e^x` 反函數（x>0；range (0,∞) 斷言不證）→ `ln` 連續（反證、雙 case＋ε=min）→ `ln` 可微 `d/dx ln x=1/x`（inverse-function 技巧）。
- **③ 全照提案核可＋三項選配全取**：(a) application capstone（短版 growth/decay／half-life）、(b) HW3 降一句 Remark 4.6、(c) HW2 `ln(ab)` 改判**具名 Proposition 4.3**（非 worked example）。
- **D7 Homework 升格**：HW1→Corollary 4.4（`f'=0⟹const`）、HW2→Proposition 4.3（對數積律）、HW4→Example 4.5（`a^x:=e^{x ln a}` 指數律，**收束 §4.1 D6 的 `a^r` fence**）、HW3→Remark 4.6（Cauchy 函數方程一句）。
- **ROADMAP key figure**：✅ Figure 4.3 `e^x`／`ln x` 對 `y=x` 反射（`e^x` blue `.curve`、`ln x` red `.curve-log`、`y=x` 灰虛線 `.idline`、(0,1)↔(1,0) dots；等比例尺保 45°）。
- **forward-loop close**：✅ Ch3 §3.3（Example 3.6 非正式用 `ln`）forward-ref 到此 → Remark 4.5 關閉迴路（嚴格 vs chain-rule；本章不改 Ch3）。
- **章末 Summary**：✅ 4-strand（exponential／analysis machinery／existence theorems／logarithm；CONTENT_SPEC §4，末節責任）。
- **雙閘**：gate-1（4-lens 並行 subagents）**0 blocking**（math／faithfulness／direction 各 0 finding／prose 0 blocking）／6 prose advisory（套 3 留 3）；Codex gate-2（gpt-5.5 xhigh，使用者同意計費）**四輪收斂**——run1 1 blocking（Remark 4.5 過度推廣）→run2 3（Summary bound 漏 |h|<½、Remark 4.6 證明骨架、capstone 缺條件）→run3 1（Remark 4.5 磁鐵句、刪除）→**run4 converged 0**（5 findings 全採納；4 修 1 刪）。render 0 err／28 頁／0 overflow。

---

## 3. 章層方向決策（提案；**各節 ③ 方向閘由使用者核可**，非預先定死）

> 依 CONTENT_DIRECTION「模型提案、人定奪」。下列為我依手稿＋ROADMAP 提的章層方向；落地時各節 brief 會再細化、停在 ③ 等核可。

- **D1 — legacy tex 當 signed 數學 cross-check（非手稿、非內容來源）。** 手稿＝數學主軸；`legacy/tex_handout/chapters/ch04_exponential_logarithm.tex` 是 LaTeX→HTML 前已簽核的同章，**只當盲算對賬的 ground truth**（§4.2 即此用法），不照抄其散文／結構。新具名結果（Bolzano–Weierstrass、Cauchy 等價）一律人工查核。
- **D2 — §4.2 POC 的處置（已裁決，2026-06-21）。** 使用者選 **(b) 併進正式章流程重跑**：舊 POC `sec-4-2.html` 與舊 test-pipeline seed/紀錄已刪（ab5f330），§4.2 從手稿 pp.3–10 重新轉錄（`seed_ch04_s2.md`）走完整六階、編號自 Theorem 4.3／Definition 4.2 起。①→⑥ 已完成、兩閘收斂（gate-1 0 blocking；Codex gate-2 run1 1 blocking→run2 converged）。
- **D3 — ROADMAP 已 resolved 的兩個方向叉路照辦（§4.2）。** ① 收斂⟺Cauchy **展開**成完整 Bolzano–Weierstrass＋monotone-subsequence（超出手稿；user-directed 2026-04-27）。② 指數律寫**完整 6 步**（非 4 步 outline；user-directed）。§4.2 成品已照此。
- **D4 — MVT 留在 §4.4（ROADMAP open Q）。** 手稿把 Rolle/MVT 夾在指數章是因 `ln` 建構需要 monotonicity corollary。未來 applications-of-differentiation 專章草擬時，再於 Mode B **僅提議**移走。本章不移。
- **D5 — §4.1 補 `e` 的值＋部分和（真 expansion，待 ③）。** 手稿**無** `e≈2.718`、無部分和表、無收斂圖。ROADMAP key figure 指定 §4.1 partial-sum 收斂圖。提案：補一個「算 `e` 前幾項部分和」worked example＋收斂圖（低風險 `expansion:example`/`figure`）。
- **D6 — `a^r`(r∉ℚ) 的處理照手稿＋legacy 框架（待 ③）。** 手稿 p.1 拋出「how about `a^r`?」即跳到 series 定義 `e^x`。提案：照 legacy 的「limit-of-rationals 較笨重 → 改走 series，且 `a^x:=e^{x ln a}` 留到 §4.5」一句帶過，不在 §4.1 真的建構 `a^r`（forward-fence 到 §4.5）。
- **D7 — Homework 升格 worked example（待 ③）。** 手稿 HW（pp.23–24）：`ln a+ln b=ln(ab)`（→§4.5，重要對數律）、`a^x=e^{x ln a}`＋其指數律（→§4.5，定義一般指數）、`f'=0⟹const`（→§4.4，MVT 直接推論）皆 **manuscript-faithful**、升格 worked example（含解）。函數方程刻畫 `g(x)g(y)=g(x+y),g(1)=e⟹g=e^x`（HW3）較進階、低優先，**提案略過或降為 remark**，待 ③。**bare your-turn exercise 一律不自創**（root README §防護欄、CONTENT_SPEC §14）。
- **D8 — binomial 記號（§4.2）。** 手稿用 `C^n_k`；本書全程 `\binom{n}{k}`（ROADMAP notation）。§4.2 成品已用 `\binom`、首見處 cross-ref 手稿記號。
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
- **✅ §4.2 ④ 落定編號（2026-06-21 重跑，接 §4.1 ledger）**：Definition `4.2`(Cauchy)；Theorem `4.3`(continuity x>0)、`4.4`(Bolzano–Weierstrass)、`4.5`(Cauchy criterion)、`4.6`(continuity ℝ)、`4.7`(exponent law)；Proposition `4.1`((△) abs-conv⟹conv)；Corollary `4.1`(positivity)；Remark `4.2`；Caution 無編號。交叉引用（"Theorem 4.1/4.2"、"bound (∗)"、"(∗∗)"、"Strategy 4.1"、"§4.1"）已自查、render 0 dangling。**→ §4.3 自 Theorem `4.8`、Definition `4.3`、Proposition `4.2`、Corollary `4.2`、Remark `4.3` 起接續。**
- **✅ §4.3 ④ 落定編號（2026-06-21 簽核，接 §4.2 ledger）**：Theorem `4.8`(`d/dx e^x=e^x`)；Proposition `4.2`(bound `|(e^h−1)/h−1|≤|h|`)；Corollary `4.2`(higher derivatives `(e^x)^{(n)}=e^x`)；Remark `4.3`(explicit-rate)。**§4.3 不 mint 新 Definition**（導數定義 Ch2 已給；Definition `4.3` 留給 §4.4/§4.5）。交叉引用（"Theorem 4.7"／"Corollary 4.1"／"Strategy 4.1"／"§4.2"／"Chapter 2"／"Figure 4.1"）已自查、render 0 dangling。**→ §4.4 自 Theorem `4.9`、Definition `4.3`、Proposition `4.3`、Corollary `4.3`、Remark `4.4` 起接續。**
- **✅ §4.4 ④ 落定編號（2026-06-21 簽核，接 §4.3 ledger）**：Definition `4.3`(max/min point)；Theorem `4.9`(Extreme Value Theorem，陳述不證)、`4.10`(Interior Extremum「Theorem A」)、`4.11`(Rolle)、`4.12`(MVT)；Corollary `4.3`(monotonicity 雙條：`f'≥0⟹`non-decreasing／`f'>0⟹`strictly increasing)；Strategy `4.2`(Applying the MVT)；Figure `4.2`(MVT secant–tangent)；Example `4.2`(MVT on x²，c=1)、`4.3`(sin on [0,π/4])、`4.4`(e^x strictly increasing on ℝ)；Remark `4.4`(existence-engine synthesis)；Caution 無編號(Thm A interior 必要)。**§4.4 不 mint 新 Proposition**（EVT/Thm A/Rolle/MVT 皆 Theorem；Proposition `4.3` 留給 §4.5）。交叉引用（"Theorem 4.1 完備性"／"Theorem 4.7 指數律"／"Theorem 4.8 (e^x)'"／"Theorem 4.9–4.12"／"Corollary 4.3"／"Chapter 3"）已自查、render 0 dangling。**→ §4.5 自 Definition `4.4`(ln x)、Theorem `4.13`、Proposition `4.3`、Corollary `4.4`、Strategy `4.3`、Example `4.5`、Figure `4.3`、Remark `4.5` 起接續。**
- **✅ §4.5 ④ 落定編號（2026-06-21 簽核，接 §4.4 ledger；全章末節）**：Definition `4.4`(natural logarithm ln x)；Theorem `4.13`(ln continuous)、`4.14`(`d/dx ln x=1/x`)；Proposition `4.3`(logarithm product law `ln(ab)=ln a+ln b`，③ add-on (c) 由 worked example 改判具名)；Corollary `4.4`(`f'=0⟹`constant，HW1 升格)；Example `4.5`(general powers `a^x:=e^{x ln a}`，HW4 升格)；Figure `4.3`(`e^x`/`ln x` 對 `y=x` 反射)；Remark `4.5`(rigorous vs Ch3 chain-rule)、`4.6`(Cauchy functional equation，HW3 一句)；Caution 無編號(ln 只 x>0)。**§4.5 不 mint 新 Strategy**（ROADMAP 未指派；Strategy `4.3` 留給後章）。交叉引用（"Theorem 4.6 連續"／"Theorem 4.7 指數律"／"Theorem 4.8 (e^x)'"／"Theorem 4.12 MVT"／"Corollary 4.3 單調性"／"Example 4.4 e^x strictly increasing"／"Chapter 3 §3.3"／"§4.1"）已自查、render 0 dangling。**→ Chapter 4 至此編號封頂（Definition 4.4／Theorem 4.14／Proposition 4.3／Corollary 4.4／Strategy 4.2／Example 4.5／Figure 4.3／Remark 4.6）；Chapter 5 counters 重置（自 5.1 起）。**
- **✅ Mode C ①波 補題目（2026-06-27 import，gate-1+2 收斂）——Example counter 封頂由 `4.5` 改為 `4.7`**：§4.4 緊跟 Example 4.2（MVT 找 c）、Corollary 4.3 之前插入兩 worked example——**Example `4.3`**（`|sin a−sin b|≤|a−b|` via MVT＝Lipschitz 估計，Strategy 4.2「只用存在性」的首個正面落地；[source: CLP-1 §2.13] variant、解 authored）、**Example `4.4`**（`3x−sin x` 恰一根 via Rolle 反用＝根計數；[source: CLP-1 §2.13] 輕改）。連帶 **cascade renumber**：§4.4 舊 Example `4.3`(sin)→**`4.5`**、`4.4`(e^x)→**`4.6`**；§4.5 `4.5`(general powers)→**`4.7`**。**唯一 student-facing prose cross-ref 更新**：§4.5 Theorem 4.13（ln 連續）證明處「strictly increasing (Example 4.4)」→「(Example 4.6)」。其餘型別封頂不變（Definition 4.4／Theorem 4.14／Proposition 4.3／Corollary 4.4／Strategy 4.2／Figure 4.3／Remark 4.6）。**雙閘**：gate-1（example-supplement ×5＋章層 completeness critic，`wf_a9a30cfa-c0e`）**0 blocking**（4 節 clean、§4.4 浮 2 候選、critic 建議全留）；gate-2（Codex gpt-5.5 xhigh，使用者同意計費，74,207 tokens）**run1 收斂 0 blocking**（E1 authored 解＋E2 補算行皆獨立查核正確）。`build.py ch04`＋render 重驗：Example **4.1–4.7 連續**、0 dangling cross-ref、0 mjx-merror、0 未渲染。產物 [`ch04_example-supplement-review.html`](ch04_example-supplement-review.html)（gate-1 候選＋裁決）、[`ch04_example-supplement-audit.md`](ch04_example-supplement-audit.md)（gate-2 findings 轉錄）。
- **✅ 圖機會閘 → 三圖落地（2026-06-27 import）——Figure counter 封頂由 `4.3` 改為 `4.6`**：圖機會 gate-1（`handout-figure-opportunity-audit` ×5＋critic，`wf_a514bfba-3d6`）掃出 3 個 medium 機會，使用者裁定**三個都畫**。新增三圖（FIGS entry 在 standalone shell、fragment 加 `<figure>`）：**Figure `4.1`**＝`completeness-bound`（§4.1，單調有界⟹收斂階梯，after Remark 4.1）、**Figure `4.3`**＝`interior-extremum-squeeze`（§4.4，Thm A 兩側夾擠 f′(x_M)=0，after Thm 4.10 證明）、**Figure `4.6`**＝`reciprocal-slope-log`（§4.5，倒數斜率 rise/run 對調⟹1/x，after Thm 4.14 證明）。**cascade renumber**（皆插在既有圖之前/中）：partial-sums `4.1`→**`4.2`**、mvt-secant-tangent `4.2`→**`4.4`**、exp-log-reflection `4.3`→**`4.5`**。**Ch4 全章無 student-facing prose 引用 figure 編號**（grep 證；所有「Figure 4.x」皆 figcaption 定義或 dev 註解）→ 零 prose cross-ref 風險，只改 6 figcaption＋header 註解。render 自驗：6 圖全 hydrate、Figure 4.1–4.6 連續、0 mjx-merror、新圖目視幾何正確（夾擠峰頂水平切線＋兩側反斜割線、倒數斜率鏡射對稱 slope 2↔½ 等比尺、完備性點列離散逼近 L 在 M 下）。**待 D1–D8 圖正確性閘**（gate-1 `wf_d3a33dbb-6f7` 進行中；gate-2 Codex 待徵同意）。其餘型別封頂不變。產物 [`REVIEW-ch04-figure-opportunity.html`](REVIEW-ch04-figure-opportunity.html)。
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
| §4.2 Continuity & Exponent Law | ✅ `seed_ch04_s2.md`（pp.3–10，2026-06-21 重轉錄） | 🟢 accepted-by-proceeding（2026-06-21） | ✅ `brief_s42.md` | ✅ 2026-06-21（照提案核可） | ✅ `fragments/ch04/sec-4-2.html`（Thm 4.3–4.7／Def 4.2／Prop 4.1／Cor 4.1／Rem 4.2／Caution 無編號）＋併入 `build.py` ch04＋`chapter4-print-standalone.html`（render：0 MathJax err／13 print 頁／0 overflow） | ✅ **converged**。free 4-lens（`wf_3f10e703`）0 blocking／8 advisory（套 4：M1 (I) 自然形、Strategy 4.1 回指、美式拼寫、開場拆句）。Codex gate-2（gpt-5.5 xhigh，使用者同意計費）：**run1** 1 blocking（收尾 forward-fence 點名 `(e^h−1)/h` 越界→改 generic）；**run2 converged 0 blocking**＋2 advisory 皆套（Thm 4.3 區間下界明寫、Caution `e` 無理 cross-ref §4.1）。`result_s42.json`／`result_s42_r2.json`。gate 報告 `_audit/REVIEW-ch04_s42-gate1.html`／`-gate2.html`。render 重驗 0 err／13 頁／0 overflow | ✅ **2026-06-21 使用者簽核** |
| §4.3 Derivative of `e^x` | ✅ `seed_ch04_s3.md`（pp.10–11，2026-06-21） | 🟢 accepted-by-proceeding（2026-06-21） | ✅ `brief_s43.md` | ✅ 2026-06-21（全照提案核可，含 C-3/C-4/C-5 選配） | ✅ `fragments/ch04/sec-4-3.html`（Prop 4.2／Rem 4.3／Thm 4.8／Cor 4.2；不 mint 新 Definition）＋併入 `build.py` ch04＋`chapter4-print-standalone.html`（render：0 MathJax err／15 print 頁／0 overflow） | ✅ **converged**。free 4-lens：**0 blocking**（math／faithfulness 兩 lens 0 finding；direction／prose 6 advisory→5 卡，套 3：建模解 `e^{kt}`、收尾拆句、opener 拆句）。Codex gate-2（gpt-5.5 xhigh，使用者同意計費）：**run1 即 converged、0 blocking／0 finding**（~33.7k tokens；本章首個 run1 全清的節）。`result_s43.json`。gate 報告 `_audit/REVIEW-ch04_s43-gate1.html`／`-gate2.html`。回歸 render 重驗 0 err／15 頁／0 overflow | ✅ **2026-06-21 使用者簽核** |
| §4.4 Rolle & MVT | ✅ `seed_ch04_s4.md`（pp.11–18，2026-06-21） | 🟢 accepted-by-proceeding（2026-06-21） | ✅ `brief_s44.md` | ✅ 2026-06-21（全照提案核可＋四項選配全取） | ✅ `fragments/ch04/sec-4-4.html`（Def 4.3／Thm 4.9–4.12／Cor 4.3／Strat 4.2／Fig 4.2／Ex 4.2–4.4／Rem 4.4／Caution 無編號）＋併入 `build.py` ch04＋`chapter4-print-standalone.html`（新 `.secant`/`.tangent` CSS＋`mvt-secant-tangent` FIGS）（render：0 MathJax err／22 print 頁／0 overflow／Fig 4.2 數值平行+觸線） | ✅ **converged**。free 4-lens（`wf_39f59234`）**0 blocking**（math／faithfulness 0 finding，4 證對賬 legacy 全等）／7 advisory（套 4：Ex 4.4 x=0 精準化、Rem 4.4 拆 which、Ex 4.4 拆雙層括、Strat 4.2 step3 措辭；保留 3：Thm 4.10 略 continuous＝更銳利、Strat √x 旁白、forward-fence）。Codex gate-2（gpt-5.5 xhigh，使用者同意計費）：**run1** 1 blocking（收尾越界預覽 §4.5 continuity/derivative→裁去只留最小交棒）；**run2 converged 0 finding**（run1≈48.1k＋run2≈54.5k tokens）。`result_s44.json`／`result_s44_r2.json`。gate 報告 `_audit/REVIEW-ch04_s44-gate1.html`／`-gate2.html`。回歸 render 重驗 0 err／22 頁／0 overflow | ✅ **2026-06-21 使用者簽核** |
| §4.5 Monotonicity & Logarithm | ✅ `seed_ch04_s5.md`（pp.18–22＋HW，2026-06-21） | 🟢 accepted-by-proceeding（2026-06-21；無 [請查核]） | ✅ `brief_s45.md` | ✅ 2026-06-21（全照提案核可＋三項選配全取） | ✅ `fragments/ch04/sec-4-5.html`（Def 4.4／Thm 4.13-4.14／Prop 4.3／Cor 4.4／Ex 4.5／Fig 4.3／Rem 4.5-4.6／Caution 無號＋application capstone＋4-strand 章末 Summary）＋併入 `build.py` ch04＋`chapter4-print-standalone.html`（新 `.curve-log`/`.idline` CSS＋`exp-log-reflection` FIGS）（render：0 MathJax err／28 print 頁／0 overflow／Fig 4.3 鏡像幾何正確） | ✅ **converged**。gate-1（4-lens 並行 subagents）**0 blocking**（math／faithfulness／direction 各 0 finding／prose 0 blocking）／6 prose advisory（套 3 留 3）。Codex gate-2（gpt-5.5 xhigh，使用者同意計費）**四輪收斂**：run1 1 blocking（Remark 4.5 過度推廣）→run2 3（Summary bound 漏 |h|<½、Remark 4.6 證明骨架、capstone 缺條件）→run3 1（Remark 4.5 磁鐵句→刪）→**run4 converged 0**（5 findings 全採納；4 修 1 刪、tokens 四輪≈259.7k）。`result_s45.json`／`_r2`／`_r3`／`_r4`。gate 報告 `_audit/REVIEW-ch04_s45-gate1.html`／`-gate2.html`。回歸 render 重驗 0 err／28 頁／0 overflow | ✅ **2026-06-21 使用者簽核** |

**每節交付物（CLAUDE.md 2026-06-15；gate 報告比照 ch01 慣例分檔）**：除 `chapter4-print-standalone.html`（成品），每節 gate 裁決後**必產兩份獨立 standalone HTML 審核報告**（雙擊即開、MathJax CDN、各含「審核對象」單元 provenance 表＋該閘 verdict＋finding cards）：
> - `_audit/REVIEW-ch04_sNM-gate1.html` — gate 1（免費 Claude 4-lens 對抗審）
> - `_audit/REVIEW-ch04_sNM-gate2.html` — gate 2（計費 Codex，讀 `result_sNM*.json`）
>
> 單一產生器 `_audit/REVIEW-sNM.gen.py` 同時產兩檔（gate-2 讀 JSON、gate-1／單元 map 內嵌）。§4.1 已產：[`_audit/REVIEW-ch04_s41-gate1.html`](_audit/REVIEW-ch04_s41-gate1.html)、[`_audit/REVIEW-ch04_s41-gate2.html`](_audit/REVIEW-ch04_s41-gate2.html)（render 0 MathJax err）。**§4.2 起比照辦理。**

**狀態（2026-06-21）**：§4.1 跑完 ①→⑤——**free 4-lens ＋ Codex gate-2 兩審皆 converged（0 blocking）**，`sec-4-1.html`＋章 opener＋`chapter4-print-standalone.html`＋Figure 4.1 render-clean（0 err／6 頁／0 overflow）。**⑥ 已簽核（2026-06-21 使用者）——§4.1 完成、已 commit。** **§4.2 已於 2026-06-21 重跑完成**（D2 裁定棄舊 POC、從手稿 pp.3–10 重轉錄、併進正式流程；①→⑥ 兩閘收斂、已簽核、已併入 `build.py` ch04＋`chapter4-print-standalone.html`）。**§4.3 已於 2026-06-21 完成**（手稿 pp.10–11；①→⑥ 兩閘**皆 run1 直接 converged**——本章首個 run1 全清的節；已簽核、已併入 `build.py` ch04＋`chapter4-print-standalone.html`、render 0 err／15 頁）。**§4.4 已於 2026-06-21 完成**（Rolle's Theorem & MVT，手稿 pp.11–18；全章最重節＝4 定理＋Figure 4.2＋Strategy 4.2＋Corollary，③ 取全部四項選配；①→⑥ 兩閘收斂——gate-1（`wf_39f59234`）4-lens 0 blocking／7 advisory（4 套 3 留）、Codex gate-2 run1 1 blocking（§4.5 scope leak）→run2 converged；已簽核、已併入 `build.py` ch04＋`chapter4-print-standalone.html`（新增 Figure 4.2＝`mvt-secant-tangent` FIGS＋`.secant`/`.tangent` CSS）、render 0 err／22 頁／0 overflow）。**§4.5 已於 2026-06-21 完成**（Monotonicity & the Logarithmic Function，手稿 pp.18–22＋HW；全章末節，③ 取全部三項選配——application capstone／HW3 一句 Remark／HW2 改判具名 Proposition；①→⑥ 兩閘收斂——gate-1 4-lens 0 blocking／6 prose advisory（套 3 留 3）、Codex gate-2 **四輪收斂**（run1 1→run2 3→run3 1→run4 converged，5 findings 全採納）；已簽核、已併入 `build.py` ch04＋`chapter4-print-standalone.html`（新 Figure 4.3＝`exp-log-reflection` FIGS＋`.curve-log`/`.idline` CSS）、render 0 err／28 頁／0 overflow；關閉 Ch3 §3.3 與 §4.1 `a^r` 兩 forward-fence、收束章末 4-strand Summary）。**🎉 Chapter 4 全章 §4.1–§4.5 ①→⑥ 全部完成、編號封頂（Def 4.4／Thm 4.14／Prop 4.3／Cor 4.4／Strat 4.2／Ex 4.5／Fig 4.3／Rem 4.6）。** 各輪 commit 僅含該節 ch04 產物；其餘工作樹既有變更（video/ pipeline、ch03、scratch）不在範圍、未動。**ROADMAP ch04 已填 entry**（含三條 resolved/open question：Cauchy⟺conv、exponent-law detail、MVT placement、§4.3 redundancy）。

---

## 8. 收尾閘進度（Mode A 之後的獨立閘 → 推到「與 Ch1/Ch2 同級全跑」）

> 權威閘序見 [`../../PIPELINE.md`](../../PIPELINE.md)。Ch4 在 Mode A 六階＋章層 Mode B 之後，補跑 Mode C（①例題＋②軟深度）＋圖機會/正確性＋數學 M1–M8＋S·A·V，全 0 blocking 後改 ROADMAP status。建議序（內容先進場再被後閘審）：Mode C ①→②→圖機會→數學 M1–M8→圖正確性 D1–D8→S·A·V→收尾。

| 閘 | gate-1（Claude，免費） | gate-2（Codex，計費） | 狀態 |
|---|---|---|---|
| **Mode C ①波 補題目** | ✅ example-supplement ×5＋critic（`wf_a9a30cfa-c0e`）0 blocking | ✅ Codex gpt-5.5 xhigh，74,207 tok，run1 收斂 0 blocking | ✅ **完成（2026-06-27）**：§4.4 +2 例（Ex 4.3 Lipschitz／4.4 根計數），Example 封頂 4.5→4.7，已 import＋build＋render-clean。產物 `ch04_example-supplement-{review.html,audit.md}`。**已 commit `707c975`。** |
| **Mode C ②波 軟深度** | ✅ 9鏡頭×5＋anti-padding critic（`wf_e4cbacd9-00d`）0 blocking | —（本波數學單純，gate-2 以範圍限定 Mode B 代之） | ✅ **完成（2026-06-27）**：§4.1/§4.2/§4.3 clean、§4.4 +1 caution（假逆命題 strictly increasing ⇏ f′>0，x³ 反例，精簡版）、§4.5 +1 caution（log 誤推廣 ln(a+b)≠ln a+ln b）。皆無編號＝零 cascade。**範圍限定 Mode B**（`handout-prose-audit`，README 硬規則）：兩條 Keep、0 blocking（math／faithfulness／Mode C 合規／A易懂／B流暢／C去AI味 全 clean）。build＋render-clean（編號仍 4.1–4.7、0 mjx-merror）。產物 `REVIEW-ch04-modec-enrichment{,-applied}.html`。**已 commit `707c975`。** |
| **圖機會閘** | ✅ ×5＋critic（`wf_a514bfba-3d6`）3 機會全 medium | — | ✅ **完成（2026-06-27）**：使用者裁定三個都畫 → Figure 4.1（完備性）/4.3（夾擠）/4.6（倒數斜率）落地，Figure 封頂 4.3→4.6，render-clean。 |
| **數學 M1–M8** | ✅ Claude ×7（5 per-section 全 M1–M8＋worked-example 重算專員＋跨章 M6/M7/M8 一致性，每候選對抗式雙鏡頭 verify，`wf_ea8a0ceb-39a`）0 blocking/0 advisory＋主流程 sympy 全 PASS | ✅ gate-2 Codex gpt-5.5 xhigh，173,720 tok，**run1 收斂** 0 blocking/0 advisory | ✅ **完成（2026-06-27）**：7 auditor＋對抗 verify 全 clean、raw 候選 = 0（無 over-report）；Codex 獨立重算 Ex 4.1–4.7（七題 agrees=true）＋尾界 (∗)＋指數律 6 步＋積律／反函數導數＋依賴鏈無循環，雙閘對 M1–M8 結論完全一致。內容**零修改**（gate 全 clean，無回歸需求）。產物 `REVIEW-ch04-math-audit.html`（gate-1+2 雙欄）、`ch04_math-audit-gate2.md`（Codex findings 轉錄）。**未 commit。** |
| **圖正確性 D1–D8** | ✅ gate-1（`wf_d3a33dbb-6f7`，6 圖×audit＋critic）**0 blocking／1 advisory** | ✅ gate-2 Codex gpt-5.5 xhigh（77,984 tok，6 PNG 經 `-i`）**0 blocking／1 advisory** | ✅ **完成（2026-06-27）**：兩閘一致。新 3 圖（4.1/4.3/4.6）數學幾何兩模型獨立確認全對；既有 3 圖重編號無回歸；唯一 advisory＝Fig 4.2「-2 刻度負號被灰 P 曲線壓」（兩閘皆判非 blocking、簽核圖不動、記錄）。findings 轉錄 `ch04_figure-audit-gate2.md`。 |
| **S·A·V 散文** | ✅ `handout-prose-audit` ×5 逐節（`wf_18dcf9d6-64b`）0 blocking／17 advisory＋Vale 0/0/0 | ✅ Codex gpt-5.5 xhigh，154,714 tok，run1 0/0 | ✅ **完成（2026-06-27）**：gate-1 0 blocking（易懂性＋S/A 全清），⛳ 套 4 條建議採 copyedit（G1-4.2-1／4.3-1／4.5-1／4.5-2，純切句/去重）；gate-2 Codex 複審後版本 0/0。**Claude 完整性掃描另抓 3 處 student-facing「the manuscript」露出（L1 §4.1、L2/L3 §4.2，兩閘皆漏）→ ⛳ 全採去露出＋手動回歸 PASS**（L3 觸 D8、保留 C^ℓ_m 橋接）。build＋render 重驗 1011 math／0 KaTeX err、編號仍連續。產物 `REVIEW-ch04-svc-gate{1,1-applied,2}.html`、`ch04_svc-gate2.md`。**未 commit。** |
| **收尾** | — | — | ✅ **完成（2026-06-27）**：ROADMAP Ch4 Status `draft`→「**與 Ch1/Ch2/Ch3 同級全跑**」（含各閘 gate-2 跨模型複核敘述）；`PIPELINE.md` 各章現況 Ch4 行更新為「全閘跑完」；本 §8 全列 ✅。**待 commit 本輪（數學+S·A·V 兩閘＋收尾文檔）。** |
