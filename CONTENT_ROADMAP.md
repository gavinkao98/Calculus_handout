# 內容路線圖

本檔案承載講義的**課程弧線**：有哪些章節、順序為何、每章負責什麼、以及概念如何跨章串聯。它是 [`CONTENT_SPEC.md`](CONTENT_SPEC.md)（規範*如何*寫）和 [`CONTENT_QUICKSTART.md`](CONTENT_QUICKSTART.md)（日常作者規則）的課程面伴侶。

開始寫新章節時，先更新下方的 entry，**然後**才動筆。當你結束一章時，標記為 done 並回頭檢視下游章節的 prereq 敘述。

本書由**不同教師撰寫的手稿**組裝而成。每章 entry 在 **Manuscript source** 欄位記錄其手稿來源，使草稿的起源與轉換狀態一目了然。手稿轉 HTML 片段的工作流程以及規範 Claude 擴展手稿的 anti-hallucination 規則都在 [`README.md`](README.md) §*Authoring workflow* 中；本檔案是各章手稿追蹤的落點。

---

## 受眾與定位

重複自 [`CONTENT_SPEC.md`](CONTENT_SPEC.md) §1，讓任何一章的作者能快速校準：

- 有志自修大學微積分的高中生。
- 具備紮實的 precalculus 基礎；有一些數學推理經驗；尚未達到大學數學主修的程度。
- 將講義視為主要學習管道。**講義是自足的**；影片是強化而非前提。

兩個跨章的目標凌駕於任何章節特定的內容之上：

- **self-sufficiency**——從未看過影片的學生仍然能從講義中學到東西。
- **lookup-friendliness**——在第五章忘了某個 definition 的學生可以透過 index、章節開頭或 summary 找回來。

---

## 章節列表

> **狀態圖例**：`draft` = 正在撰寫中。`skeleton` = 結構已規劃但內容未草擬。`planned` = 在路線圖上，尚未開始。`done` = 通過 §15 一致性檢查清單。

| # | 標題 | 狀態 | 各節 |
|---|---|---|---|
| 1 | Inverse Functions and Limits | draft | 1.1 Inverse Functions and One-to-One Functions; 1.2 Inverse Trigonometric Functions; 1.3 Limits; 1.4 One-Sided and Infinite Limits; 1.5 Limit Laws; 1.6 The Precise Definition of a Limit |
| 2 | Derivatives | draft | 2.1 The Tangent Line and the Derivative at a Point; 2.2 The Derivative as a Function; 2.3 Differentiability, Continuity, and Higher Derivatives; 2.4 Derivatives of Polynomials and the Exponential Function; 2.5 The Product and Quotient Rules |
| 3 | Chain Rule and Trigonometric Derivatives | draft | 3.1 Derivatives of the Sine and Cosine Functions; 3.2 The Chain Rule; 3.3 Applications of the Chain Rule |
| 4 | The Exponential and Logarithmic Functions | draft | 4.1 Construction of the Exponential Function; 4.2 Continuity and the Exponent Law for $e^x$; 4.3 The Derivative of $e^x$; 4.4 Rolle's Theorem and the Mean Value Theorem; 4.5 Monotonicity and the Logarithmic Function |
| 5-14 | *（TBD——各章草擬時再加標題）* | planned | — |

目標範圍：Calc I + II + III（單變數到多變數向量微積分）。以 Stewart / Rogawski 目錄作為參考弧線。此範圍的完整弧線大約 14 章：

- **Calc I**（Ch 1-4）：Inverse Functions and Limits → Derivatives → Applications of Differentiation → Integrals。
- **Calc II**（Ch 5-9）：Applications of Integration → Techniques of Integration → Differential Equations → Parametric and Polar Coordinates → Infinite Sequences and Series。
- **Calc III**（Ch 10-14）：Vectors and the Geometry of Space → Vector Functions → Partial Derivatives → Multiple Integrals → Vector Calculus。

Ch 3 以後的標題**不承諾**，直到前一章的草稿穩定。per-workflow 的決策是明確的：我們在一章的直接前驅到達 `draft` 狀態時才填入該章的完整 roadmap entry（role、prereqs、core skills、key figures、notation、cautions、open questions）——不會更早，因為前驅章節中的上游決策會影響後繼章節需要教什麼。

---

## 每章 entry 範本

開始新章節時，將此區塊複製到章節列表區域。

```
### Chapter N: Title

**Status**: draft | skeleton | planned | done
**Source file**: handout/fragments/chNN/sec-*.html（每節一個片段）
**Estimated length**: N pages printed（以 handout/build.py 產出的列印 standalone 為準）
**Manuscript source**: <teacher name | "pre-manuscript working hypothesis" | "pre-existing LaTeX — entry reverse-engineered">
 — <pending | received YYYY-MM-DD | converted YYYY-MM-DD>. <optional note on coverage, gaps, or register hints from the teacher>.

**Role in the arc**
- 一段說明本章對讀者的作用。
- 為什麼它在位置 N 而不是更前或更後。

**Prerequisites**
- 本章依賴的章節（按節列出）。
- 讀者預期帶來的 precalculus 知識。
- 先前引入的、本章會重用的記號或 environment。

**Core skills**
每項 MUST 對應章節開頭 "By the end of this chapter, you will be able to:" 列表中的一個子彈。
- skill 1
- skill 2
- skill 3-5

**Key figures**
- 每個節開頭動機依賴的圖（各一個子彈）。

**Handout self-sufficiency vs. video reinforcement**
- 講義獨立教授的內容。
- 影片在此基礎上增加的內容（直覺視覺化、替代的 worked example、節奏）。
  影片永遠不會承載講義中未陳述的事實。

**Strategy boxes expected**
- 題型 → strategy 名稱。例："computing a limit → §1.5 Limit-computation strategy."

**Notation introduced**
- 新符號、macro 或記號慣例。每一個在首次使用時都以清楚散文標記以利查找（lookup-friendliness）；HTML 講義無自動索引，交叉引用為手寫散文。

**Common pitfalls (caution boxes)**
- 記號陷阱。
- Branch-choice 或 domain-restriction pitfall。
- 只在 subdomain 上成立的恆等式。

**Open questions**
- 尚未做出的決策。在宣告該章 `done` 之前關閉。
```

---

## Chapter 1（已填範例）

### Chapter 1: Inverse Functions and Limits

**Status**: Mode C 充實中 — 散文雙閘已過（gate-1 Claude＋gate-2 Codex，0 blocking）；**主軸於 2026-06-15 凍結，作為 Mode C 起點**（Mode C 只增添、不動主軸；新增擴充以 `[pass: enrichment]` 標記，完成後跑範圍限定於新標記的 Mode B）。
**Source file**: [`handout/fragments/ch01/`](handout/fragments/ch01/)（`sec-*.html`）——slug `foundations` 是弧線層級的標籤（Chapter 1 是弧線的 *foundations* 階段），不是印刷的章節標題的一部分。（原 LaTeX 稿現置於 [`legacy/tex_handout/chapters/ch01_foundations.tex`](legacy/tex_handout/chapters/ch01_foundations.tex)。）
**Estimated length**: *（完成首次完整編譯後填入）*
**Manuscript source**: pre-existing LaTeX——entry 從已提交的 LaTeX 稿反推而來。現以 HTML 片段為準；本 entry 是對現有內容的描述，不是未來草擬的計畫。當 Chapter 1 進行進一步編輯時，同時更新 HTML 片段和本 entry。

**Role in the arc**
Chapter 1 是課程弧線的 **foundations** 階段。它建立微積分的兩部基礎機器：inverse function（將規則「反向運行」的代數機器）和 limit（「逼近但不等於」的分析機器）。本章刻意將兩者配對，因為兩者都迫使讀者從對應關係和近似的角度思考，而非僅盯著公式。

**Prerequisites**
- Precalculus 函數：domain、range、composition、graphs。
- 三角函數及其在標準區間上的圖形。
- 基本代數運算（factoring、rationalising、completing the square）。

**Core skills**（對應章節開頭的 bullet list）
- 判定一個函數是否 one-to-one，如果是則求出其 inverse；
- 使用 inverse trigonometric function，包括它們的 principal-interval restriction 和由此產生的 identity；
- 用 substitution、factoring、rationalising 和 one-sided analysis 計算 Ch. 1 和 Ch. 2 中遇到的各類 limit；
- 判定一個 limit 何時不存在；
- 使用 $\varepsilon$–$\delta$ definition 陳述並（在需要時）驗證一個 limit。

**Key figures**
- inverse-composition diagram（§1.1）。
- 可逆函數圖形沿 $y = x$ 的反射（§1.1）。
- 帶有 principal interval 著色的 restricted-domain trig graphs（§1.2）。
- one-sided-limit 不一致的範例（§1.4）。
- $\varepsilon$–$\delta$ tube-and-interval diagram（§1.6）。

**Handout self-sufficiency vs. video reinforcement**
- 講義獨立承載每個 definition、每個 theorem statement、每個 worked example 和每個 strategy box。
- 影片（每節一支，目前以 §1.1 為範例）增加了動態的沿 $y=x$ 反射展示、動態的 $\varepsilon$–$\delta$ tube（靜態頁面無法傳達的效果）、以及對記號陷阱的較慢口頭講解。
- 影片中沒有任何內容取代閱讀講義——影片場景在 [`legacy/MANIM_STORYBOARD.md`](legacy/MANIM_STORYBOARD.md) 中標記為 reinforcement。

**Strategy boxes present**
- 求 inverse function（§1.1）。
- 計算 limit（§1.5）。
- 驗證 $\varepsilon$–$\delta$ limit（§1.6）。

**Notation introduced**
- `\arcsin`、`\arccos`、`\arctan`、`\arccsc`、`\arcsec`、`\arccot`（本書的 inverse-trig operator）。
- `\lim_{x \to a} f(x)`、`\lim_{x \to a^-} f(x)`、`\lim_{x \to a^+} f(x)`、`\lim_{x \to \infty} f(x)`。
- $\varepsilon$、$\delta$。

**Common pitfalls (caution boxes present)**
- $\sin^{-1} x$ 表示 inverse sine，不是 $1/\sin x$。
- $\arcsin(\sin x) = x$ 僅在 principal interval $[-\pi/2, \pi/2]$ 上成立。

**Open questions**
- 本區塊為 ch01 **Mode C 充實**的延後／刻意省略決定錨點（依 [`README.md`](README.md) Mode A/C 擴增稽核；2026-06-15 起）。
- （習題項已結案：講義本體不收習題，placeholder 已全數移除——[`CONTENT_SPEC.md`](CONTENT_SPEC.md) §14，2026-06-12 定案。課文範例補充另行進行，見 [`CONTENT_SOURCING.md`](CONTENT_SOURCING.md)。）

---

## Chapter 2（已填 entry）

### Chapter 2: Derivatives

**Status**: draft，**Mode C 充實中**。手稿覆蓋在 HTML handout 中已**完成**（`handout/fragments/ch02/`）：§2.1–§2.5 透過六階方向層流程（[`CONTENT_DIRECTION.md`](CONTENT_DIRECTION.md)）撰寫，每節經 Codex audit 至 blocking=0（2026-06）。Mode C 充實分兩波：① 課文範例補充已套用（6 例，2026-06-22，重編號至 Examples 2.1–2.23，見 [`handout/_audit/REVIEW-ch02-example-supplement-applied.html`](handout/_audit/REVIEW-ch02-example-supplement-applied.html)）；② 軟深度充實（intuition／caution／application／history）已套用 15 塊（2026-06-26，皆標 `[pass: enrichment]`，範圍限定 Mode B/S·A·V gate-1 全 0 blocking，見 [`handout/_audit/REVIEW-ch02-modec-applied.html`](handout/_audit/REVIEW-ch02-modec-applied.html)；裁決稿 `REVIEW-ch02-modec-adjudication.html`，候選 `REVIEW-ch02-modec-enrichment.html`）。gate-2 Codex（gpt-5.5, read-only）跨模型複審亦過：14 塊 clean、1 blocking on §2.3 的 \(d^2y/dx^2\) 記號（reify `dx`，與 §2.2「`dy/dx` 非分數」衝突）→ 改 operator 讀法 → re-audit pass（見 [`handout/_audit/REVIEW-ch02-modec-gate2.html`](handout/_audit/REVIEW-ch02-modec-gate2.html)）。圖機會閘＋圖正確性閘已跑（2026-06-26）：圖正確性 8 圖（6 buildPlot＋2 inline SVG）視覺 blocking 全 0——quotient-example-graph 上面板 f(x) 標籤與藍曲線同色糊字 1 blocking 已修（標籤移右下空白區）＋重渲確認，見 [`handout/_audit/REVIEW-ch02-figure-audit.html`](handout/_audit/REVIEW-ch02-figure-audit.html)；圖機會閘提 5 候選、裁決畫 2（F-2.3-A＝§2.3 Example 2.12 ∛x 垂直切線、F-2.1-A＝§2.1 差商解剖），兩新圖 D1–D8 複審 0 blocking，其餘 3 候選不畫（近重複），見 [`handout/_audit/REVIEW-ch02-figure-opportunity.html`](handout/_audit/REVIEW-ch02-figure-opportunity.html)。圖總數 8→10。獨立數學正確性閘已跑（2026-06-26，gate-1 Claude ×5＋gate-2 Codex）：M1–M8 雙閘 blocking 全 0（gate-1 1 條 borderline advisory＝§2.4 Ex 2.16 定義域 polish、gate-2 未復現），worked-example 答案多處 sympy 重算核對，見 [`handout/_audit/REVIEW-ch02-math-audit.html`](handout/_audit/REVIEW-ch02-math-audit.html)。新版 S·A·V 散文閘（Task 8）已跑（2026-06-26，gate-1 Claude ×5）：5 節 blocking 全 0、10 條 advisory（皆 propose-only 軟潤稿），裁決套用 2 條 F4 拆句（§2.4 eˣ setup、§2.5 rectangle-area），逐節回歸 PASS、其餘 8 條保留，見 [`handout/_audit/REVIEW-ch02-svc-gate1.html`](handout/_audit/REVIEW-ch02-svc-gate1.html)。**S·A·V 與圖正確性兩閘的 gate-2 Codex 獨立複核亦已跑（2026-06-26）：** ① 散文 gate-2（`codex exec` read-only，依同一 PROSE rubric＋svc 錨組獨立審 5 節）blocking 全 0（兩 critic 一致）、4 條新 advisory，裁決採納 C2-3／C2-4＝改掉 §2.4／§2.5 共 5 處 student-facing 散文露出「the manuscript」為內容層語氣（HTML 註解 provenance 保留、數學不動），逐節回歸 re-audit PASS、其餘 2 條 F4 密度保留，見 [`handout/_audit/REVIEW-ch02-svc-gate2.html`](handout/_audit/REVIEW-ch02-svc-gate2.html)；② 圖正確性 gate-2（Codex 收 10 張重渲 2× PNG via `-i`，回 `const FIGS`／inline-SVG 算數值核對 D1–D8）全 10 圖 blocking 0、advisory 0（含兩新圖與 gate-1 修過的 quotient-example-graph），見 [`handout/_audit/REVIEW-ch02-figure-audit-gate2.html`](handout/_audit/REVIEW-ch02-figure-audit-gate2.html)。**Ch2 至此與 Ch1 完全同級全跑（含各閘 gate-2 跨模型複核）**：手稿六階＋Mode C（例題＋軟深度）＋去 AI 味 S·A·V（gate-1+gate-2）＋圖機會/正確性兩閘（圖正確性 gate-1+gate-2）＋數學正確性雙閘。
**Source file**: `handout/fragments/ch02/sec-2-*.html`
**Estimated length**: *（完成首次完整編譯後填入）*
**Manuscript source**: received 2026-04-27（13 頁手寫手稿，由該章作者提供）。手稿涵蓋微分章的基礎部分：tangent-line motivation、the derivative at a point、the derivative as a function、differentiability vs continuity、higher derivatives、constants / power function / exponential 的微分、以及 product / quotient rules。**不包含**原始 working hypothesis 中列為 §2.4–§2.8 的 trigonometric、chain-rule、implicit、inverse-function 或 logarithmic-derivative 材料。這些主題是否會作為後續手稿到達（擴展 Ch 2）或移至後面的章節，見下方 Open questions。

**Role in the arc**
Chapter 2 是 Calc I 的**展開**階段。它將 Chapter 1 的 limit 機器轉化為一個可運作的算子：給定一個函數，產生另一個描述其瞬時變化率的函數。Ch 1 完成了繁重的概念鋪墊（「逼近但不等於」意味著什麼？）；Ch 2 將其在演算法上兌現。以目前手稿的範圍，Ch 2 涵蓋 derivative 的 definition 以及對 polynomial、natural exponential 和任何可微函數的 product 或 quotient 進行微分所需的規則。Trigonometric、chain-rule、implicit、inverse 和 logarithmic differentiation 是延後的（見 Open questions）。

**Prerequisites**
- **來自 Chapter 1**：全部六節，尤其 §1.3（limits）、§1.4（one-sided and infinite limits）和 §1.5（limit laws）。Derivative 是以 limit 定義的；對 limit 運算不熟練的學生無法撐過 §2.1 的定義。§1.6（ε-δ）並非嚴格前提——derivative 是用 algebraic limit 而非 ε-δ 形式表述的——但看過 §1.6 的學生會覺得 §2.1 的嚴謹性不那麼突兀。
- **Precalculus**：polynomial 和 rational 運算；binomial theorem（用於 §2.4 power-rule proof）。
- **不需要先前接觸 derivative**——本章假設 derivative 是新概念。

**Core skills**（將對應章節開頭的 bullet list）
- 陳述 derivative 的 limit definition $f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}$ 並應用之從 first principle 計算 polynomial 和 root function 的 derivative；
- 使用 power、constant-multiple、sum、product 和 quotient rule 微分代數和指數的組合；
- 用 series definition 微分 natural exponential function $e^x$；
- 識別函數不可微的位置（如 corner）並將 differentiability 與 continuity 連結；
- 計算 higher-order derivative。

**Key figures**
- secant-to-tangent limit diagram（§2.1）：一條曲線上，一系列 secant line 隨第二個點趨近第一個點而收斂為 tangent line。
- derivative as a function（§2.2）：一對圖，$f$ 在上、$f'$ 在下，以 $x$-axis 對齊，使零點、極值和正負號變化在視覺上對齊。
- 在 corner 不可微（§2.3）：$|x|$ 在 $0$ 附近的圖形，左右 secant slope 有標記，顯示 one-sided limit 不一致。

**Handout self-sufficiency vs. video reinforcement**
- 講義獨立承載 limit definition、每條微分規則及其 proof、每個 worked example 和每個 strategy box。
- 影片增加：(a) 動態 secant-to-tangent 收斂動畫（靜態頁面難以傳達）；(b) 動態 slope-of-tangent-line demo，其中 tangent point 沿曲線掃過，slope 即時繪在下方，展示 $f'$ 作為函數的浮現。
- 影片中沒有任何內容取代閱讀講義；推廣方向始終是 *video → handout*，永遠不是反向。

**Strategy boxes expected**
- *Computing a derivative from the limit definition*（§2.2）：3 步流程——(1) 寫出 difference quotient $(f(x+h) - f(x))/h$；(2) 代數化簡直到 $h$ 從分母中消去；(3) 取 $h \to 0$。
- *Selecting among the basic rules*（§2.5）：何時使用 power rule vs product vs quotient；測試標準是表達式的語法形狀。

**Notation introduced**
- $f'(x)$、$\dfrac{dy}{dx}$、$\dfrac{df}{dx}$、$\dfrac{d}{dx}[f(x)]$、$f''(x)$、$f^{(n)}(x)$——常見的 derivative notation，引入時明確指引何時各自最自然。在首次使用時為 prime notation 和 Leibniz notation 各加 index entry。
- $\Delta x$、$h$——increment notation；手稿在引入代換 $x = a + h$ 之後專用 $h$。在 caution 中標記 $\Delta x$ 和 $h$ 在 derivative context 中是同義的。

**Common pitfalls (caution boxes)**
- *Power rule domain*：$\frac{d}{dx}[x^n] = n x^{n-1}$ 在 §2.4 中對正整數 $n$ 證明；負整數情形留為 manuscript exercise。Caution 標記此點並將 full real-exponent 的陳述延後至後面的章節。
- *Quotient rule asymmetry*：$\frac{d}{dx}\left[\frac{f}{g}\right] = \frac{f'g - fg'}{g^2}$ 對 $f$ 和 $g$ 不對稱；分子中項的順序很重要。
- *Differentiable implies continuous, but not conversely*：§2.3 的定理是單方向的。$|x|$ 在 $0$ 處是標準反例；手稿和本章都明確指出。
- *(fg)' is not f'g'*：手稿用 product rule 的開場反例（`f = x`、`g = x^2`、`fg = x^3`）；caution 將其保留為主要陷阱。

**Open questions**
- ~~*Manuscript scope vs original 9-section hypothesis*~~——**resolved 2026-04-27**：兩份後續手稿（`2023-10-28-chainRule` 和 `2023-11-4-ExponentialFunction`）涵蓋了缺失的主題（trig derivatives、chain rule、ln/arcsin/x^x via chain rule、rigorous $e^x$、MVT、ln）。這 4 個缺失主題沒有擴展 Ch 2；它們成為 Ch 3（*Chain Rule and Trigonometric Derivatives*）和 Ch 4（*The Exponential and Logarithmic Functions*）。Implicit differentiation 不在任何一份手稿中，仍延後至後面的章節。
- ~~*Treatment of $e^x$ derivative*~~——**resolved 2026-06-08**：在 §2.4 ⑥ convergence gate 確認。本章遵循手稿的 series-based derivation（提出 $e^x$，然後 $(e^h-1)/h = 1 + h/2! + h^2/3! + \dots \to 1$），保持手稿的直覺層次而非 Stewart 的「$\lim_{h \to 0}(e^h-1)/h = 1$ as the defining property」路線。嚴格的 convergence 和 $e^x$ 的 construction 延後至 Ch 4 §4.3，該節會重新推導 derivative 並 cross-reference 回來。在 §2.4 實作為 Theorem 2.5 + series proof，附一行 forward fence 到 Ch 4，以及 Codex audit（4 runs, blocking=0）。
- ~~*Higher derivatives placement*~~——**resolved 2026-06-08**：higher derivative（$f''$、$f'''$、$f^{(n)}$）保持為 §2.3 的 subsection（遵循手稿）。在 §2.3 ⑥ convergence gate 確認；brief 和 HTML 均將其實作為 `<h3>` subsection 而非獨立的 `<article class="sec">`。
- ~~*§2.5 product/quotient rules——figure choice & section completion*~~——**resolved 2026-06-08** 於 §2.5 ⑥ convergence gate（最後一個 manuscript section，因此完成了 Ch 2 的 manuscript coverage）。實作為 Theorem 2.6（product rule）和 Theorem 2.7（quotient rule），使用手稿的 add-and-subtract proof——domain hypotheses 明確化（$g$ continuous via §2.3 Theorem 2.1；$g(x)\neq 0$ for the quotient）——加上 Strategy 2.2（*selecting among the basic rules*，by syntactic shape + "simplify first"）、三個 pitfall caution（$(fg)'\neq f'g'$ 用手稿的反例、$\Delta x \equiv h$、quotient-rule asymmetry）、以及 Examples 2.15–2.17。**Figure decision**：使用者加入了 **Figure 2.4**，一張 product-rule rectangle-area diagram（面積增量 = 長條 $f\,\Delta g$、$g\,\Delta f$ + 二階 corner $\Delta f\,\Delta g$），覆蓋了 brief 的預設「rules section 不附圖」；以 inline schematic SVG 呈現（無 `figures.js` entry——`buildPlot` 沒有 fill primitive）。保持 label-light 衍生出一條新的權威規則：[`CONTENT_SPEC.md`](CONTENT_SPEC.md) §10 "Label economy"（在 kit 的 `CONTRACT-html-writing.md` §Figures 中 mirror），後續章節遵循。Codex audit converged（2 runs；run 1 抓到一個在新增的 $1/x$ inline check 中的 notation conflict，修正後 → run 2 blocking=0）。

---

## Chapter 3（已填 entry）

### Chapter 3: Chain Rule and Trigonometric Derivatives

**Status**: **與 Ch1/Ch2 同級全跑**（2026-06-27）。手稿覆蓋於 2026-06-08 完成（§3.1–§3.3，三節皆過 six-stage convergence gate，含 two-model adversarial audit：Claude multi-lens + Codex gpt-5.5 xhigh）。其後各獨立閘已補齊全跑：**Mode C** ①課文範例補充（+4 CLP-1 worked example、全章重編號 Examples 3.1–3.16、雙閘收斂，見 [`handout/_dev-archive/ch03/ch03_example-supplement-review.html`](handout/_dev-archive/ch03/ch03_example-supplement-review.html)）＋②軟深度（§3.1 +1 Caution「極限非恆等式」，見 [`handout/_audit/REVIEW-ch03-modec-enrichment.html`](handout/_audit/REVIEW-ch03-modec-enrichment.html)）；**圖機會閘＋圖正確性兩閘**（7 圖 Figure 3.1–3.7：圖機會閘核可新增 5 圖、視覺正確性 gate-1 D1–D8 全 0 blocking［Fig 3.7 等比座標修正後回歸，2026-06-21，見 [`handout/_audit/REVIEW-ch03-figure-opportunity.html`](handout/_audit/REVIEW-ch03-figure-opportunity.html)］；gate-2 Codex 視覺第二讀者［120,683 tokens］提 1 blocking——Fig 3.6 caption「Halving $h$」vs FIGS source $0.5/1.35\approx0.37$（D5）→裁決修圖 `panel(0.5)→panel(0.675)` 真減半→手動回歸 PASS，見 [`handout/_audit/REVIEW-ch03-figure-audit-gate2.html`](handout/_audit/REVIEW-ch03-figure-audit-gate2.html)）；**數學正確性 M1–M8 雙閘**（sympy 獨立重算 31/31 PASS＋gate-1 Claude ×5［per-section×3＋cross-ref＋proof-rigor，對抗式 verify 0 候選］＋gate-2 Codex［100,807 tokens］，皆 0 blocking 0 advisory，見 [`handout/_audit/REVIEW-ch03-math-audit.html`](handout/_audit/REVIEW-ch03-math-audit.html)）；**去 AI 味 S·A·V 散文雙閘**（Vale 0/0/0＋gate-1 Claude ×3 0 blocking［採 5 條 copyedit tighten］＋gate-2 Codex［81,096 tokens］0 blocking［採 2 條 F5「the manuscript」student-facing 露出改寫］，見 [`handout/_audit/REVIEW-ch03-svc-gate1.html`](handout/_audit/REVIEW-ch03-svc-gate1.html)／[`REVIEW-ch03-svc-gate2.html`](handout/_audit/REVIEW-ch03-svc-gate2.html)）。**Ch3 至此與 Ch1/Ch2 完全同級全跑**：手稿六階＋Mode C（①例題＋②軟深度）＋去 AI 味 S·A·V（gate-1+gate-2）＋圖機會/正確性兩閘（圖正確性 gate-1+gate-2）＋數學正確性雙閘。
**Source file**: `handout/fragments/ch03/sec-3-*.html`
**Estimated length**: *（完成首次完整編譯後填入）*
**Manuscript source**: `2023-10-28-chainRule`（2023-10-28 的手寫手稿，2026-04-27 收到）。手稿涵蓋 (i) 透過 squeezing lemma + sector geometry 推導 $\sin x$ 和 $\cos x$ 的 derivative，(ii) 使用 differentiability 的 remainder-form definition（$f(x_0 + h) = f(x_0) + mh + R(h)$，$R(h)/h \to 0$）證明 chain rule，以及 (iii) chain-rule 應用，包括 $d/dx \ln x$、$d/dx x^x$ 和 $d/dx \arcsin y$。手稿也重述了 product rule 和 differentiable-implies-continuous lemma；兩者在 Ch 3 中以 cross-reference 回 Ch 2 處理，而非重新推導。

**Role in the arc**
Chapter 3 是 Calc I 的**規則延續**。Chapter 2 建立了 derivative 的 limit definition 和基本代數規則（constant、power、sum、product、quotient、$e^x$）；Chapter 3 加入 composition 的規則（chain rule）並將其應用於引入 trigonometric derivative 以及提取 inverse function 和 implicitly-defined function 的 derivative。連同 Ch 4 對 $e^x$ 和 $\ln x$ 的嚴格處理，Ch 3 收尾了微分工具箱。

**Prerequisites**
- **來自 Chapter 1**：§1.5（特別是 squeeze theorem——直接用於 $\lim_{\theta \to 0} \sin \theta / \theta = 1$）。§1.2（inverse trig——$\arcsin$ 是 chain-rule example 的目標之一）。
- **來自 Chapter 2**：全部五節，尤其 §2.5 product rule（chain-rule 手稿重新推導了它；我們改為 cross-ref）和 §2.3 differentiable $\Rightarrow$ continuous（用於 chain-rule proof 和 trigonometric continuity proof 中）。
- **Trigonometric identity**：和差化積 identity $\sin(x + h) - \sin(x) = 2 \sin(h/2) \cos(x + h/2)$ 是本章的主要代數工具。Pythagorean identity $1 + \tan^2 = \sec^2$ 也出現在 worked example 中。

**Core skills**
- 計算 $d/dx \sin x$、$d/dx \cos x$、$d/dx \tan x$，以及（透過 chain rule）$d/dx \sin(g(x))$、$d/dx \cos(g(x))$ 等；
- 應用 chain rule 微分兩層或多層函數的 composition，包括 $f(g(h(x)))$ 型的巢狀；
- 使用 chain rule + log differentiation 微分 $x^x$、$f(x)^{g(x)}$ 和類似的非標準指數表達式；
- 從 inverse-function relation $\sin(\arcsin y) = y$ 等出發，應用 chain rule 推導 $d/dx \arcsin x$、$d/dx \arctan x$ 和 $d/dx \ln x$。

**Key figures**
- secant inequality figure（§3.1）：unit circle 上的 sector $OAB$ 和三角形 $\triangle OAB$、$\triangle ABC$，用以建立 $\cos \theta \le \sin \theta / \theta \le 1$ 的邊界。
- chain rule as composed mapping（§3.2）：堆疊的 input–intermediate–output 軸，展示微小的 $h$ 在 input 端如何傳播到 output 端的變化，以 intermediate slope 的乘積為比例。

**Strategy boxes expected**
- *Chain-rule decomposition*（§3.2）：給定一個複雜表達式，辨識最外層操作；將表達式寫為 $f(g(x))$；微分為 $f'(g(x)) \cdot g'(x)$。對巢狀 composition 迭代此步驟。
- *Logarithmic differentiation*（§3.3）：當表達式具有 $f(x)^{g(x)}$ 的形式或具有多因子的 product/quotient 時，對兩邊取 $\ln$，應用 chain rule 和 product rule，然後解出 $y'$。

**Notation introduced**
- differentiability 的 remainder-form definition $f(x_0 + h) = f(x_0) + m h + R(h)$，$R(h)/h \to 0$。這是手稿中的 Def 2；等價於標準的 limit definition，但對 chain-rule proof 更方便。
- $\arcsin'$、$\arccos'$、$\arctan'$ 在 §3.3 中透過對 $\sin(\arcsin y) = y$ 等應用 chain-rule 技巧而引入。

**Common pitfalls (caution boxes)**
- *Chain rule is one identity, not two fractions*：$\frac{dy}{dx} = \frac{dy}{du} \cdot \frac{du}{dx}$ 是 chain rule，不是 $du / du = 1$ 的消去。Leibniz 形式的表觀分數消去是有用的助記法，但不是 proof。
- *Forgetting the inner derivative*：最常見的 chain-rule 錯誤是 $\frac{d}{dx}[\sin(g(x))] = \cos(g(x))$ 而非 $\cos(g(x)) \cdot g'(x)$。一個 worked example 標記此錯誤。
- *Domain issues for $\arcsin$ derivative*：公式 $1/\sqrt{1 - y^2}$ 僅在 $y \in (-1, 1)$（open interval——endpoints 具有 vertical tangent）上有效。Caution 標記此點。
- *$\ln$ used informally before rigorous construction*：§3.3 將 $\ln$ 視為「$e^x$ 的 inverse」，使用 $e^{\ln x} = x$ 提取 $d/dx \ln x = 1/x$。嚴格的 construction 延後至 Ch 4。一則 note 標記此依賴關係。

**Open questions**
- ~~*Trig derivatives placement vs squeeze-theorem location*~~——**resolved 2026-06-08** 於 §3.1 ⑥ convergence gate：Ch 3 草稿**在散文中 cross-reference §1.5 squeeze theorem，不重述它**（D4）。$\lim_{\theta \to 0} \sin \theta / \theta = 1$ 作為 **Proposition 3.2** 證明，$\sin$ 和 $\cos$ 的 continuity 作為 **Proposition 3.1** 證明，各自在 $\theta \to 0$ 形式上引用「the squeeze theorem (§1.5)」；手稿的額外 $x \to \infty$ 形式不需要且省略，因此無重複。$(1 - \cos\theta)/\theta \to 0$ 作為 **Example 3.1** 加入（D2）。Two-model adversarial audit（Claude 4-lens + Codex gpt-5.5 ×2 runs）converged with 0 blocking。
- ~~*Two equivalent definitions of differentiability*~~——**resolved 2026-06-08** 於 §3.2 ⑥ convergence gate：Def 2（remainder form）在 §3.2 作為 **Definition 3.1** 引入，因為 chain-rule proof 使用它。Def 1（limit form）在 §2.2 建立，**在散文中 cross-reference，不重新編號**（Option B，§3.2 ③ 核准）。等價性作為 **Proposition 3.3** 證明——忠實的短雙向論證，補充了手稿中 bare "easy to see" 的部分——然後 Def 2 僅用於 chain-rule proof（Theorem 3.3）。Two-model adversarial audit（Claude 4-lens + Codex gpt-5.5 ×2 runs）converged with 0 blocking。
- ~~*Implicit differentiation*~~——**resolved 2026-06-08** 於 §3.3 ⑥ convergence gate（D10）：§3.3 遵循手稿的 **composition-identity route**——$\ln x$（Example 3.6）、$\arcsin$（3.10）、$\arccos$（3.11）和 $\arctan$（3.12）的 derivative 透過微分各函數滿足的 identity（$e^{\ln x}=x$；$\arcsin(\sin x)=x$ on $[-\pi/2,\pi/2]$；etc.）並解出未知 derivative 而得到，$x^x$（3.7）透過 logarithmic differentiation（Strategy 3.2）——**未引入 implicit-differentiation framework 或 vocabulary**。未來的專門 implicit-differentiation 章節可能重新審視這些作為 canonical motivating example。Two-model adversarial audit（Claude 5-lens + Codex gpt-5.5 ×4 runs, xhigh）converged with 0 blocking；唯一的 blocking finding（unqualified $\arcsin(\sin x)=x$）被 Codex 抓到並修正。
- ~~*$\ln x$ informal before rigorous construction; $\arcsin$-derivative domain*~~——**resolved 2026-06-08** 於 §3.3 ⑥ gate（D8 + pitfalls）：$\ln x$ 以非正式方式作為 $e^x$ 的 inverse（僅用 $e^{\ln x}=x$）來提取 $d/dx\,\ln x = 1/x$（Example 3.6），附一行 forward fence 將嚴格 construction 延後至 Ch 4 §4.5（該節會重新推導）。$\arcsin/\arccos$ 的 derivative $1/\sqrt{1-y^2}$ 在 unnumbered Caution 中標記為僅在 **open** interval $(-1,1)$ 上有效；$\arctan$（Example 3.12）與之對比——在全 $\mathbb{R}$ 上可微。

---

## Chapter 4（已填 entry）

### Chapter 4: The Exponential and Logarithmic Functions

**Status**: **與 Ch1/Ch2/Ch3 同級全跑**（2026-06-27）。手稿覆蓋於 2026-06-21 完成（§4.1–§4.5，五節皆過 six-stage convergence gate，含 two-model adversarial audit：Claude multi-lens + Codex gpt-5.5 xhigh、章層 Mode B）。其後各獨立閘已補齊全跑：**Mode C** ①課文範例補充（§4.4 +2 CLP-1 worked example＝Example 4.3 Lipschitz／4.4 根計數，Example 封頂重編號 4.1–4.7，雙閘收斂，見 [`handout/_audit/REVIEW-ch04-example-supplement-applied.html`](handout/_audit/REVIEW-ch04-example-supplement-applied.html)）＋②軟深度（§4.4／§4.5 各 +1 Caution＝假逆命題 $x^3$／對數誤推廣 $\ln(a+b)$，見 [`handout/_audit/REVIEW-ch04-modec-enrichment-applied.html`](handout/_audit/REVIEW-ch04-modec-enrichment-applied.html)）；**圖機會閘＋圖正確性兩閘**（6 圖 Figure 4.1–4.6：圖機會閘核可新增 3 圖＝完備性/夾擠/倒數斜率；視覺正確性 D1–D8 gate-1+gate-2 Codex［77,984 tokens，6 PNG via `-i`］兩模型一致 0 blocking／1 非 blocking advisory［Fig 4.2 -2 刻度負號被壓、簽核圖不動］，見 [`handout/_dev-archive/ch04/ch04_figure-audit-gate2.md`](handout/_dev-archive/ch04/ch04_figure-audit-gate2.md)）；**數學正確性 M1–M8 雙閘**（gate-1 Claude ×7［5 per-section＋worked-example 重算＋跨章一致性，對抗式雙鏡頭 verify 0 候選］＋主流程 sympy 全 PASS＋gate-2 Codex［173,720 tokens］，皆 0 blocking 0 advisory，見 [`handout/_audit/REVIEW-ch04-math-audit.html`](handout/_audit/REVIEW-ch04-math-audit.html)）；**去 AI 味 S·A·V 散文雙閘**（Vale 0/0/0＋gate-1 Claude ×5 0 blocking［採 4 條 copyedit tighten］＋gate-2 Codex［154,714 tokens］0 blocking＋Claude 完整性掃描補抓 3 處 F5「the manuscript」student-facing 露出全採去露出＋回歸 PASS，見 [`handout/_audit/REVIEW-ch04-svc-gate1.html`](handout/_audit/REVIEW-ch04-svc-gate1.html)／[`REVIEW-ch04-svc-gate2.html`](handout/_audit/REVIEW-ch04-svc-gate2.html)）。**Ch4 至此與 Ch1/Ch2/Ch3 完全同級全跑**：手稿六階＋Mode C（①例題＋②軟深度）＋去 AI 味 S·A·V（gate-1+gate-2）＋圖機會/正確性兩閘（圖正確性 gate-1+gate-2）＋數學正確性雙閘。
**Source file**: `handout/fragments/ch04/sec-4-*.html`
**Estimated length**: *（完成首次完整編譯後填入）*
**Manuscript source**: `2023-11-4-ExponentialFunction`（2023-11-04 的手寫手稿，2026-04-27 收到）。手稿涵蓋 (i) 透過 power series $\sum x^n / n!$ 嚴格構造 $e^x$，使用 $\mathbb{R}$ 的完備性證明 convergence；(ii) $e^x$ 的 continuity 和 exponent law $e^x e^y = e^{x+y}$，透過仔細的 series-multiplication 論證和 Cauchy convergence；(iii) derivative $d/dx \, e^x = e^x$（比 Ch 2 §2.4 更嚴格的重新推導，附有對 $(e^h - 1)/h - 1$ 的 explicit bound）；(iv) Rolle's theorem 和 Mean Value Theorem；(v) 推論 $f' \ge 0 \Rightarrow f$ increasing；(vi) logarithm $\ln x$ 作為 $e^x$ 的 inverse，其 continuity，以及 $d/dx \ln x = 1/x$（透過 inverse-function technique）。

**Role in the arc**
Chapter 4 為 Calc I 的微分章節收尾嚴謹基礎。Ch 2 非正式地引入了 $e^x$ 並從一個隨意的逐項論證證明 $(e^x)' = e^x$；Ch 4 從零開始以 power series 建構 $e^x$，證明 Ch 2 視為理所當然的 convergence 和 continuity，並以完全嚴謹的方式重新推導 derivative。本章接著引入 Mean Value Theorem——驅動 derivative-to-monotonicity 論證的核心存在定理，用以將 strictly increasing 的 $e^x$ 反轉而構造 $\ln x$。Chapter 5 以後（applications of differentiation：extrema、optimisation、related rates、L'Hôpital）將重用本章引入的 MVT 機器。

**Prerequisites**
- **來自 Chapter 1**：§1.5（limit law 和基本 continuity 論證）、§1.6（precise $\varepsilon$-$\delta$ definition——§4.2 對 $e^x$ 的 continuity proof 本質上是 $\varepsilon$-$\delta$ 精神的，看過 §1.6 的學生會覺得熟悉）。
- **來自 Chapter 2**：§2.4（informal 的 $(e^x)' = e^x$ derivation；§4.3 嚴格重做並 cross-reference 回來）、§2.3（differentiable $\Rightarrow$ continuous，用於 MVT setup）。
- **來自 Chapter 3**：§3.3 非正式地使用 $\ln x$ 並 forward reference 到本章的嚴格 construction；§4.5 關閉此迴路。
- **Real analysis prerequisites**：reals 的 completeness（monotone bounded sequence converge）；Bolzano–Weierstrass（在 §4.2 中從 completeness 經由 monotone-subsequence lemma 證明）；binomial theorem（已在 Ch 2 §2.4 power-rule proof 中使用）。Cauchy sequence 及 convergent $\Leftrightarrow$ Cauchy 的等價在 §4.2 中引入並**證明**。

**Core skills**
- 陳述 $e^x$ 的 power-series definition 並 bound 其 tail 以建立在 $\mathbb{R}$ 上的 convergence；
- 證明 $e^x$ 在 $\mathbb{R}$ 上 continuous 且滿足 $e^x e^y = e^{x+y}$（透過 series-multiplication 論證）；
- 嚴格地用 bound $\lvert (e^h - 1)/h - 1 \rvert \le \lvert h \rvert$（在小區間上）計算 $d/dx \, e^x = e^x$；
- 陳述並證明 Rolle's theorem 和 Mean Value Theorem；
- 使用 MVT 證明 $f' \ge 0$ on $(a, b)$ implies $f$ is increasing on $[a, b]$；
- 定義 $\ln x$ 為 $e^x$ 的 inverse，證明其 continuity，並推導 $d/dx \ln x = 1/x$。

**Key figures**
- partial-sum convergence figure（§4.1）：在 $[-2, 2]$ 上繪製 $\sum_{n=0}^{k} x^n / n!$（$k = 1, 2, 3, 4$），展示收斂到光滑的 $e^x$ 曲線。
- MVT 的 secant–tangent figure（§4.4）：一條曲線，從 $(a, f(a))$ 到 $(b, f(b))$ 的 secant 畫為 dashed，內部點 $c$ 處的平行 tangent 畫為 solid。
- $e^x$ 和 $\ln x$ 的反射（§4.5）：重用 Ch 1 的 reflection-across-$y = x$ setup，$e^x$ 為 blue、$\ln x$ 為 red。

**Strategy boxes expected**
- *Tail-bound argument*（§4.1、§4.2）：當 $n_0 > 2x$ 時，用 geometric series bound $\sum_{n = n_0 + 1}^{\infty} x^n/n!$。此模板在本章中多次重用，值得提煉。
- *Verifying the MVT hypotheses before applying*（§4.4）：分別檢查 $[a, b]$ 上的 continuity 和 $(a, b)$ 上的 differentiability。常見錯誤是在函數於 endpoint 實際不可微的 closed interval 上應用 MVT。

**Notation introduced**
- $e^x$ 作為 power-series definition（手稿的選擇）。$\ln x$ 在 §4.5 首次使用時加 index entry；$e$（常數）和 $e^x$（函數）在 §4.1 首次使用時加 index entry。
- $C_k^n$ 表示 binomial coefficient（手稿的記號）。本書全程使用 $\binom{n}{k}$；當手稿的記號出現時 cross-reference 兩種記號。
- $P_k(x) = \sum_{n=0}^{k} x^n / n!$ 表示 partial sum（手稿的記號，在 §4.1–§4.2 中保留）。

**Common pitfalls (caution boxes)**
- *Series defines, doesn't derive*：series $e^x = \sum x^n / n!$ 在本章是 $e^x$ 的 **definition**。熟悉的 exponent law、continuity 和 derivative 接著是需要證明的 theorem。在 Ch 2 非正式接觸過 $e^x$ 的學生可能會在這些性質重新建立之前就嘗試使用；標記此點。
- *Bolzano–Weierstrass dependency*：§4.2 中 convergent $\Leftrightarrow$ Cauchy 的 proof 經由 Bolzano–Weierstrass（從 completeness 經 monotone-subsequence peak argument 證明）。章節 note 中的 caution 標註依賴鏈，讓學生看到 Cauchy $\Leftrightarrow$ convergent 在邏輯上等價於 completeness。
- *MVT continuity vs differentiability*：函數必須在 **closed** interval $[a, b]$ 上 continuous 且在 **open** interval $(a, b)$ 上 differentiable；endpoint 處的 differentiability 不要求。Caution 標記此不對稱。
- *$\ln$ defined only for $x > 0$*：每個涉及 $\ln x$ 的公式都隱含 $x > 0$。在 §4.5 標記；與 Ch 3 §3.3 相同慣例。

**Open questions**
- ~~*Cauchy / convergent equivalence proof*~~——**resolved 2026-04-27（user-directed）**：proof 在 §4.2 中透過 Bolzano–Weierstrass theorem 和 monotone-subsequence lemma 供給，超越了手稿本身供給的範圍。本章現在完整證明兩個方向。
- ~~*Exponent law proof level of detail*~~——**resolved 2026-04-27（user-directed）**：§4.2 的 exponent-law proof 原本草擬為 4 步 outline；在使用者指示下改寫為完整的 6 步 proof，匹配手稿的 detail level（完整 binomial-theorem reorganisation、explicit (II)-piece tail-bound estimate、step 5 中 telescoped error）。
- *MVT placement*：手稿將 MVT 包在 exponential / logarithm 章節中，因為 $\ln$ 的嚴格 construction 需要 monotonicity corollary。當未來 applications of differentiation 章節（extrema、optimisation）草擬時，自然會在 Mode B 中**僅提議** MVT 移至該章。目前 MVT 留在 Ch 4。
- *§4.3 redundancy with §2.4*：Ch 2 的 informal derivation of $(e^x)' = e^x$ 和 §4.3 的 rigorous re-derivation 主要差異在對 $(e^h - 1)/h - 1$ 的 explicit bound。可能的重構：將 Ch 2 的 casual version 替換為 forward-reference 到 §4.3，消除重複。決策延後至兩章都簽核後。

---

## 跨章記號串聯

一份學生會翻回去查的微積分講義，需要記號一旦引入就保持穩定。首次做出決定時記錄在此；後續章節引用本節而非重新決定。

- `\arcsin` / `\arccos` / `\arctan` 是本書使用的 operator。`\sin^{-1}`、`\cos^{-1}`、`\tan^{-1}` 僅在首次警告 reciprocal 誤讀時出現在 caution box 中。
- Domain restriction 在適用於單一公式時以 inline 方式寫在 condition 區塊中；容易忘記時則移入 caution 區塊。HTML 對應的 markup 見 [`handout/_dev-archive/general/CONTRACT-html-writing.md`](handout/_dev-archive/general/CONTRACT-html-writing.md)。
- 方程式編號為 per-chapter（`(1.3)`、`(2.7)`），且僅在方程式被後續引用或為 formal statement 時出現（見 spec §6）。

*（後續章節引入新的慣例決策時擴展此列表。）*

---

## 講義–影片邊界（重複規則）

每一章的作者 **MUST** 驗證：

- 講義獨立成立。沒有影片的學生仍能完成本章。
- 影片不引入講義中不存在的 fact、definition 或 theorem。
- 影片可自由加入視覺直覺、節奏變化或替代的 worked example；這些是 reinforcement，不是 prerequisite。

存疑時，將事實從影片提升至講義，而非反向。

---

## 檢視路線圖

每當一章到達 `done` 後，回頭檢視本檔。典型的更新：

- 關閉該章的 `Open questions` 區塊，或將剩餘項目移入後續 issue。
- 更新從較早章節 forward-reference 到本章的 cross-reference。
- 檢查後續章節的 `Prerequisites` 區塊在任何結構調整後是否仍列出正確的先前章節。

如果整體弧線變更——例如兩章應合併、或某章應提前——在修改章節原始碼**之前**先更新本檔。路線圖是計畫；章節原始碼是實作。
