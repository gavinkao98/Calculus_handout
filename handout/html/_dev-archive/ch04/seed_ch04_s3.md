# Seed — §4.3 The Derivative of e^x

> stage ① 產物。Transcribed from the handwritten manuscript `2023-11-4-ExponentialFunction`,
> **pp.10–11** (the section headed "§ The derivative of the exponential function", from the
> difference quotient `(e^{x+h}−e^x)/h = ((e^h−1)/h)e^x` through `d/dx e^x = e^x`; the next
> item "§ Rolle's Theorem" begins §4.4).
> Manuscript heads this with its own title "§ The derivative of the exponential function"
> (handout maps it to §4.3 per ROADMAP).
> Faithful to the manuscript: structure, order, notation, and deliberate omissions preserved.
> seed 語法＝輕量可讀（反引號行內＋Unicode；見 CONTENT_DIRECTION ① / `seed_ch04_s1.md`）。漂亮 KaTeX 留給 ④。可疑／非標準處標 **[請查核]**。
> **數學 cross-check（非手稿）**：legacy `ch04_exponential_logarithm.tex` 的 §4.3 段（`\section{The Derivative of e^x}`，LaTeX→HTML 轉移前已簽核；D1：僅盲算對賬，不照抄散文／結構）。

---

## §4.1 / §4.2 依賴（承前；非本節新內容，僅備援引）

§4.3 用到前兩節的兩件既成事實：

1. **§4.1 級數定義**：`e^h := Σ_{n=0}^∞ hⁿ/n!`（對全 ℝ；§4.2 Summary 已把定義域延拓到 ℝ）。本節把 `e^h` 的級數代回差分商。
2. **§4.2 指數律（Theorem 4.7）**：`e^{x+h} = e^x · e^h`（對全 x, h ∈ ℝ）。差分商第一步的因式分解 `(e^{x+h}−e^x)/h = ((e^h−1)/h)e^x` **就靠這條**——把 `e^{x+h}` 拆成 `e^x e^h`、提出與 h 無關的 `e^x`。

（§4.2 還證了 `e^x` 在 ℝ 上連續；本節導數論證主要用指數律＋級數，連續性是背景。）

---

## § The derivative of the exponential function（手稿原文）

Consider the difference quotient

`(e^{x+h} − e^x)/h = ((e^h − 1)/h) · e^x`.

（手稿直接寫出此等式。推導：`e^{x+h} = e^x e^h`（§4.2 指數律）⟹ `e^{x+h} − e^x = e^x(e^h − 1)` ⟹ 除以 h 並提出 `e^x`。手稿未顯式寫這一步，視為由指數律直接得。）

To find `d/dx e^x`, we only need to find the limit

`lim_{h→0} (e^h − 1)/h`.

The factor `e^x` is independent of `h`, so the whole derivative reduces to this one limit.

### Note（手稿的 bound 推導）

`e^h = 1 + h + h²/2! + h³/3! + ⋯`   （§4.1 級數定義，代 x=h）

故

`(e^h − 1)/h − 1 = h/2 + h²/3! + ⋯ + h^{n−1}/n! + ⋯`

（逐項：`e^h − 1 = h + h²/2! + h³/3! + ⋯`；除以 h 得 `(e^h−1)/h = 1 + h/2! + h²/3! + ⋯`；減 1 把常數項 1 消掉，剩 `h/2! + h²/3! + ⋯`，其中 `h/2! = h/2`。）

⟹

`|(e^h − 1)/h − 1| ≤ |h| · [ 1/2 + |h|/3! + ⋯ + |h|^{n−2}/n! + ⋯ ]`

（每項提出一個 `|h|`：`h/2 = |h|·(1/2)`、`h²/3! = |h|·|h|/3!`、…、`h^{n−1}/n! = |h|·|h|^{n−2}/n!`。三角不等式逐項取絕對值。）

`            ≤ |h|`   for `h ∈ (−1/2, 1/2)`.

**[請查核]**：末步「中括號 `[ 1/2 + |h|/3! + ⋯ ] ≤ 1`（當 `|h| < 1/2`）」手稿只給結論、未展開。落地時補一句證明：對 `|h| < 1/2`，括號 `= 1/2 + Σ_{n≥3} |h|^{n−2}/n! ≤ 1/2 + Σ_{n≥3} (1/2)^{n−2}/n! < 1`（首項 1/2，餘項以 `(1/2)^{n−2}/n!` 的幾何/階乘尾界壓住，總和 < 1/2）。屬 ④ 方向（補嚴格化的一句）。cross-check legacy §4.3 的對應 Proposition。

### 結論

Hence,

`lim_{h→0} ( (e^h − 1)/h − 1 ) = 0`,   i.e.   `lim_{h→0} (e^h − 1)/h = 1`.

This implies

**`d/dx e^x = e^x`.**

（因 `(e^{x+h}−e^x)/h = ((e^h−1)/h) e^x → 1 · e^x = e^x`，h→0。手稿在此結束本節，緊接 §4.4「§ Rolle's Theorem」。）

---

## §4.3 / §4.4 boundary

手稿緊接著寫 **§ Rolle's Theorem**：先給 max/min 的 Def 1、`cos x` 在 0 取最大的 ex、EVT「Fact」（[a,b] 連續⟹有最大／最小點，不證）、Thm A（內部極值⟹`f'=0`）…——**這是 §4.4 的開頭**，不屬本 seed。

---

## 手稿刻意省略／特徵（忠實記錄）

- **無 Ch2 cross-ref**：手稿不提「Ch2 曾非正式算過 `(e^x)'=e^x`」。ROADMAP open Q／PLAN §2 指出 Ch2 §2.4 有 informal 版；§4.3 是嚴格重做、差別在 explicit bound。**開頭 cross-ref Ch2「這次補上 bound」屬 handout 加法（legacy §4.3 opener 即如此做）**，非手稿原文——屬 ② brief 方向。
- **無 higher-derivative corollary**：手稿只得 `d/dx e^x = e^x`，未推「每階導數都是 `e^x`」。legacy §4.3 有 `Corollary`（`(e^x)^{(n)} = e^x`，迭代即得）——**屬 handout 可選加法**，待 ②/③。
- **差分商第一步**（`e^{x+h}−e^x = e^x(e^h−1)`）手稿未顯式寫中間步，直接給結果（靠 §4.2 指數律）。落地補一句。
- **中括號 ≤ 1 的細節**手稿從略（見上 [請查核]）。
- **`(e^h−1)/h` 的下標寫法**：手稿用「`h^{n−1}/n!`」表通項、省略號連接，未寫成 Σ 記號。落地可保留省略號型或改寫 Σ（`(e^h−1)/h − 1 = Σ_{n≥2} h^{n−1}/n!`）——屬 ④ 排版選擇。
- worked example：**0 個**。圖：**0**。動機散文：**極少**（僅「To find d/dx e^x, we only need to find the limit…」一句承上啟下）。caution／strategy／named-result 索引：**無**（具名化 Theorem/Def 屬 ④ 落地）。
- 記號：差分商變數 `h`；級數沿用 §4.1 的 `Σ hⁿ/n!`；無新記號。

---

## 對照 ground truth（評分用，非手稿）

已簽核 `legacy/tex_handout/chapters/ch04_exponential_logarithm.tex` 的 §4.3 段（`\section{The Derivative of e^x}`，`sec:rigorous-derivative-of-exp`）是同一手稿的 LaTeX→HTML 前簽核版，**僅作盲算對賬的 ground truth**（D1），不照抄其散文／結構。其結構：
- **opener**：點明 Ch2 `thm:derivative-of-exp` 曾用 casual term-by-term 論證、假設了收斂／連續／指數律；本節以 explicit bound 重證。
- **difference-quotient setup**：`(e^{x+h}−e^x)/h = ((e^h−1)/h)e^x`，提出 `e^x`、化約到 `lim(e^h−1)/h`。
- **Proposition（bound）**：`|(e^h−1)/h − 1| ≤ |h|`（`h ∈ (−1/2, 1/2)`），由級數逐項＋幾何尾界。
- **Remark**：此 bound 是 Ch2 casual 論證的嚴格版——把「高次項 vanish」量化成 explicit rate `|h|`（至少線性）。
- **Theorem（derivative formula）**：`d/dx e^x = e^x`。
- **Corollary（higher derivatives）**：迭代得 `(e^x)^{(n)} = e^x`（手稿無此推論）。

**§4.2 落地後的編號接續（PLAN §5 ledger）：** §4.1–§4.2 已 mint 到 Definition 4.2、Theorem 4.7、Proposition 4.1、Corollary 4.1、Strategy 4.1、Example 4.1、Figure 4.1、Remark 4.2。**§4.3 因此自 Theorem 4.8、Definition 4.3（若需）、Proposition 4.2、Corollary 4.2、Remark 4.3 起編號。** 本 seed 為手稿原貌（pp.10–11）；具名化與編號落在 ④。

**ROADMAP 已標的 §4.3 open question（待 ③ 方向閘確認）：**
- **與 Ch2 §2.4 的 redundancy**：Ch2 有 informal `(e^x)'=e^x`；§4.3 是嚴格重做、差別在 explicit bound。**§4.3 開頭 cross-ref Ch2、點明「這次補上 bound」**（legacy 做法）。重構（Ch2 改 forward-ref）**延後至兩章都簽核後——本章不動 Ch2**（PLAN §2）。
