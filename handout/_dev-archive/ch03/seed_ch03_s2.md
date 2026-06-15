# Seed — §3.2 The Chain Rule

> Transcribed from the handwritten manuscript `2023-10-28-chainRule`
> (manuscript pp. 11, 14–20; the chain-rule statement sits at the foot of p.11,
> the differentiation Def 1 / Def 2 and the remainder-form proof on pp.14–20).
> Manuscript's own section title: 「§ 乘法規則與連鎖規則」(Product rule and chain rule),
> which spans pp.9–20 — but its product-rule and diff⇒continuous material (pp.9–11)
> is already Ch2 (see "Cross-ref only" below; decision **D6**), and its applications
> (ln x, xˣ, arcsin, pp.12–14) are routed to §3.3 (**D7**). Only the chain-rule
> statement + the two definitions of differentiability + the proof belong to §3.2.
> Faithful to the manuscript: structure, order, notation, subscripts, and the
> deliberate "easy to see" gloss preserved.
> seed 語法＝輕量可讀（反引號行內＋Unicode；見 RULE.md ①）。漂亮 KaTeX 留給 ④。
> 可疑／非標準／手稿留白處標 **[請查核]**。

---

## Cross-ref only — NOT transcribed into §3.2 body (D6)

The manuscript section opens (pp.9–11, before the chain rule) by **re-stating and
re-proving** two results that Chapter 2 already owns. Per **D6** these are *not*
transcribed into §3.2; §3.2 only cites them. Confirmed against the scan so the
cross- references are accurate:

- **Product rule** (p.9 statement, pp.10–11 proof): `d/dx(f g)|_{x₀} = f′(x₀)g(x₀) + f(x₀)g′(x₀)`.
  Manuscript proof sets `P=fg`, splits the difference quotient as
  `[f(x₀+h)(g(x₀+h)−g(x₀)) + g(x₀)(f(x₀+h)−f(x₀))]/h`, then takes limits.
  → **Ch2 §2.5** (product rule). §3.2 does **not** re-prove.
  - (The same `Example ①` here re-derives `d/dx xⁿ = n xⁿ⁻¹` inductively from the
    product rule — also Ch2 material, not §3.2.)
- **Lemma: differentiable ⟹ continuous** (p.10): proof
  `lim_{x→x₀}(f(x)−f(x₀)) = lim ((f(x)−f(x₀))/(x−x₀))·(x−x₀) = f′(x₀)·0 = 0`.
  (手稿首行下標寫 `lim_{x→0}`、餘行 `lim_{x→x₀}`——首行係明顯筆誤；此為 cross-ref-only 摘要、不入正文。)
  → **Ch2 §2.3 Theorem 2.1** (differentiable ⟹ continuous). §3.2's chain-rule
    discussion may cite it, but does **not** re-prove. **[請查核 cross-ref 號]** 確切
    Ch2 節號／定理號（§2.5、§2.3 Thm 2.1）取自 `PLAN-ch03.md`；④ 寫 cross-ref 時對 Ch2 成品再核一次。

> Manuscript applications on pp.12–14 (`d/dx ln x = 1/x`; `d/dx xˣ = (1+ln x)xˣ`;
> `d/dy arcsin y = 1/√(1−y²)`) physically sit *between* the chain-rule statement
> (p.11) and the proof (pp.14–20), i.e. the manuscript computes **before** it proves.
> Per **D7** the handout reorders: §3.2 states + proves; the applications go to **§3.3**.
> They are **not** transcribed in this seed.

---

## Chain rule — statement (manuscript p.11)

**Chain rule.** Suppose `g(x)` is differentiable at `x₀`, and `f(y)` is differentiable
at `y = g(x₀)`. Then `P(x) = f(g(x))` is differentiable at `x₀`, and

`P′(x₀) = f′(g(x₀))·g′(x₀)`.

> (記號正規化：手稿在**陳述與 Def 1／Def 2** 把固定點寫成大寫 `X₀`，在**證明**裡寫小寫 `x₀`／`x`；
> 同一點，seed 一律用 `x₀`／`x`（與 §3.1 及全章一致）——純大小寫差異、無數學影響。)

---

## Two definitions of differentiability (manuscript pp.14–15)

The proof is preceded by a 「Concept: Differentiation」 box giving **two** definitions
of "differentiable at `x₀`" and asserting their equivalence.

**Def 1 (limit form, p.14).** `f(x)` is differentiable at `x₀` if there **exists** a real
number `m` such that

`lim_{x→x₀} (f(x) − f(x₀))/(x − x₀) = m`.

(手稿在 `∃` 旁有紅字「存在」標注。此 `m` 即 `f′(x₀)`。)

**Def 2 (remainder form, p.15).** `f(x)` is differentiable at `x₀` if

`f(x₀+h) = f(x₀) + mh + R(h)`

for some function `R(h)` such that `lim_{h→0} R(h)/h = 0`. (此 `m` 亦即 `f′(x₀)`。)

**Equivalence (p.15).** Manuscript states only: *"It is easy to see that Def 1 and
Def 2 are equivalent."* — and gives **no** argument.
> **[④ expansion]** 手稿只說 "easy to see"。④ 補一個忠實、簡短的**雙向**論證
> （標 `expansion:formula`）：Def1⟹Def2 取 `R(h)=f(x₀+h)−f(x₀)−mh`、`R(h)/h→0`；
> Def2⟹Def1 由 `(f(x₀+h)−f(x₀))/h = m + R(h)/h → m`。seed 不展開（忠於手稿留白）。

> **方向**：Def 2 (remainder form) 是 chain rule 證明的工具（線性近似可串接）。
> ROADMAP open question 確認 Def1/Def2 放此節（**D5**）。

---

## Chain rule — proof (manuscript pp.15–20, remainder form)

> 手稿在證明裡以 `x` 代表那個固定點（即陳述中的 `x₀`）；下標 `m₁,m₂` 為兩段斜率、
> `R₁,R₂,R₃` 為三段餘項。逐格對掃描核過。

**Setup (p.15).** Start from `P(x+h) = f(g(x+h))`. Apply **Def 2 to `g` at `x`**:

`g(x+h) = g(x) + m₁h + R₁(h)`,  where `m₁ = g′(x)` and `lim_{h→0} R₁(h)/h = 0`.

So `P(x+h) = f( g(x) + m₁h + R₁(h) )`.

**Apply Def 2 to `f` at `g(x)` (p.16).** With the increment `m₁h + R₁(h)` playing the
role of `h`:

`P(x+h) = f(g(x)) + m₂·[ m₁h + R₁(h) ] + R₂( m₁h + R₁(h) )`,

where `m₂ = f′(g(x))` and `lim_{y→0} R₂(y)/y = 0`.

**Collect terms (p.16).** Regroup the linear part and the leftover:

`P(x+h) = f(g(x)) + m₁m₂·h + [ m₂R₁(h) + R₂(m₁h + R₁(h)) ]`

`        = P(x) + ( g′(x)·f′(g(x)) )·h + R₃(h)`,

where `R₃(h) = m₂R₁(h) + R₂(m₁h + R₁(h))`.
> (手稿在中括號 `[ m₂R₁(h) + R₂(…) ]` 旁有紅字 `m₃` 標注，隨即正式命名為 `R₃(h)`；
> 即此括號＝餘項 `R₃`。`m₁m₂ = g′(x)f′(g(x))`，`f(g(x)) = P(x)`。**[請查核]** 手稿係數
> 順序寫成 `(g′(x)f′(g(x)))h`，與陳述 `f′(g(x))g′(x)` 同值（交換律），④ 保留手稿順序或統一即可。)

So `P(x+h) − P(x) = (g′(x)f′(g(x)))h + R₃(h)`. By **Def 2**, `P` is differentiable at `x`
with `P′(x) = g′(x)f′(g(x))` **provided** `lim_{h→0} R₃(h)/h = 0` — which is what remains
to prove.

**Goal (p.17):** prove `lim_{h→0} R₃(h)/h = 0`, where `R₃(h) = m₂R₁(h) + R₂(m₁h + R₁(h))`.

**Step ① — the easy facts (p.17).** By differentiability of `g` at `x`:

`lim_{h→0} R₁(h)/h = 0`,  and hence  `lim_{h→0} ( m₁h + R₁(h) ) = 0`.

> (`m₂R₁(h)/h = m₂·(R₁(h)/h) → m₂·0 = 0`，`m₂` 為常數。**[請查核]** 手稿把 ε-δ 火力
> 集中在較難的 `R₂(m₁h+R₁(h))/h` 項；`m₂R₁(h)/h → 0` 這一項手稿**未明寫**、由 ① 的
> `R₁(h)/h→0` 隱含。④ 可一句點明（標 `expansion:formula`），不算改手稿。)

**Step ② — the composed remainder term (pp.17–19), ε–δ.**

- **(i)** Since `lim_{y→0} R₂(y)/y = 0`: for given `ε > 0`, there exists `δ > 0` such that
  `| R₂(y)/y | < ε`  for  `0 < |y| < δ`.
- **(ii)** Since `lim_{h→0} ( m₁h + R₁(h) ) = 0`: there exists `α > 0` such that
  `| m₁h + R₁(h) | < δ`  for  `0 < |h| < α`.

Then for `0 < |h| < α`, the manuscript splits into two cases (writing `m₁h+R₁(h)` out **in full**,
no shorthand):

`| R₂(m₁h+R₁(h)) | / |h| = 0`  if `m₁h+R₁(h) = 0`;

`| R₂(m₁h+R₁(h)) | / |h| = ( |m₁h+R₁(h)|/|h| )·( |R₂(m₁h+R₁(h))|/|m₁h+R₁(h)| )`  if `m₁h+R₁(h) ≠ 0`.

From here the manuscript jumps **directly** to (p.19, opening line):

`| R₂(m₁h + R₁(h)) | / |h|  ≤  ( |m₁| + |R₁(h)|/|h| )·ε`.

> **[④ expansion]** 手稿從上方乘積式**直接**寫出此下界，略去兩個標準補步（seed **不**靜默補、忠於手稿跳步）：
> (a) 第二情形 `0 < |m₁h+R₁(h)| < δ`（由 (ii)），故由 (i) 得 `|R₂(m₁h+R₁(h))|/|m₁h+R₁(h)| < ε`；
> (b) `|m₁h+R₁(h)|/|h| = |m₁ + R₁(h)/h| ≤ |m₁| + |R₁(h)|/|h|`（三角不等式）。④ 補這兩步時標 `expansion:formula`。

Since `lim_{h→0} R₁(h)/h = 0`, there exists `α₁ ∈ (0, α)` such that `|R₁(h)|/|h| < 1` for
`0 < |h| < α₁`. Therefore for `|h| ∈ (0, α₁)`:

`| R₂(m₁h + R₁(h)) | / |h|  <  ( |m₁| + 1 )·ε`.

**Conclude (p.20).** 手稿由 `| R₂(m₁h+R₁(h)) | / |h| < (|m₁|+1)ε`（`ε` 任意）**直接**收尾:

`lim_{h→0} R₃(h)/h = 0`.

This completes the proof of the chain rule.

> (seed 補充組裝說明，**非手稿明文**——手稿在 p.20 直接寫出結論：
> `R₃(h)/h = m₂·R₁(h)/h + R₂(m₁h+R₁(h))/h`；第一項 `→ m₂·0 = 0`（Step ① 的 `R₁(h)/h→0`），
> 第二項由上界 `< (|m₁|+1)ε`、`ε` 任意而 `→ 0`；故和 `→ 0`。此層組裝即前面 `m₂R₁/h` 的 [請查核] 所指的手稿留白。)

---

## 手稿盤點摘要 / 刻意省略（給 ②③，非手稿正文）

手稿 §3.2 區塊（「乘法規則與連鎖規則」pp.9–20）**有**：product rule（陳述＋證，pp.9–11）→
diff⇒continuous lemma（陳述＋證，p.10）→ **chain rule 陳述**（p.11）→ 應用①②③（ln/xˣ/arcsin，
pp.12–14）→ Concept: Differentiation 的 **Def 1／Def 2** ＋「easy to see」等價（pp.14–15）→
**chain rule 證明**（remainder-form 串接 `m₁m₂` ＋ ε-δ 推 `R₃(h)/h→0`，pp.15–20）。

**§3.2 正文只取**（手稿主軸，照原順序、原記號）：chain rule 陳述、Def 1／Def 2＋等價、remainder-form 證明。

**§3.2 刻意不取**（餵 ②③／auditor 作 direction-conformance 反向檢查）：
- product rule 的重新陳述／重證（手稿 pp.9–11）→ **cross-ref Ch2 §2.5**，不重證（**D6**）。
- diff⇒continuous lemma 的重新陳述／重證（手稿 p.10）→ **cross-ref Ch2 §2.3 Theorem 2.1**，不重證（**D6**）。
- 應用 ln x／xˣ／arcsin y（手稿 pp.12–14，置於證明之前）→ 全移 **§3.3**；§3.2 至多一句 forward 帶到 §3.3（**D7**）。
- implicit-diff 框架：手稿 arcsin 走 composition-identity（`sin(sin⁻¹y)=y` 取導）→ 照手稿，不引入 implicit-diff（**D10**，且該段本就屬 §3.3）。

**手稿留白／待 ④ 處理：**
- Def1⇔Def2 等價：手稿只「easy to see」→ ④ 補忠實簡短雙向論證（`expansion:formula`），見上。
- `m₂R₁(h)/h → 0`：手稿未明寫（由 ① 隱含）→ ④ 可一句點明（`expansion:formula`）。

> **轉錄忠實度待你核對（①-verify）**：請逐字對掃描 pp.11、14–20，**特別** remainder-form 證明
> 每一步的下標 `m₁/m₂/R₁/R₂/R₃`、`R₃=m₂R₁+R₂(m₁h+R₁(h))`、ε-δ 的 `δ/α/α₁` 與
> `(|m₁|+1)ε` 收尾。上方 **[請查核]** 三處（cross-ref 號、係數順序、`m₂R₁/h` 留白）一併確認。
> 通過後才進 ② 方向 brief。
</content>
</invoke>
