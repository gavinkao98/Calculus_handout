# §3.2 The Chain Rule — 旁白口語版（版本 B · MiMo-V2.5-TTS 客製）

> **此檔為生成檔（DO NOT EDIT）。** 由 `content_scripts/ch03_chain_rule.spoken.yml`（口語單一源） 經 `pipeline/derive_spoken.py` 生成。要改旁白請改 `.spoken.yml` 後重生。
> **性質：版本 B（口語 TTS 版）。** 英文散文逐字忠於內容稿 `narration`，**只把數學攤成口語**（無 LaTeX），供不能直讀 LaTeX 的 TTS（MiMo）照念。對照閱讀版（版本 A，數學渲染）＝ `ch03_chain_rule_narration.html`。
> **NFA 稽核狀態：** 見 `content_scripts/_audit/`（每節各自記錄）。

---

## 一、MiMo 合成設定（現用）

| 項目 | 值 |
|------|----|
| `model` | `mimo-v2.5-tts`（builtin voice 模型；唯一模型） |
| `voice` | `Dean`（builtin；經 `audio.voice` 選定） |
| `audio.format` | `wav`（24kHz/mono/PCM16，與產線 `write_pcm_wav` 相容；beat WAV 自動裁頭尾靜音） |

**風格提示：** 無——builtin Dean 路線**不送 persona/style prompt**（2026-07-05 起，voice-design 模型與「Calm Professor」persona 已退役）。節奏靠口語稿標點與句構。

**Audio tag：** 維持預設**不啟用**（口語稿純文字）。

## 二、數學念法慣例（全節通用；NFA 裁定）

| 數學 | 口語念法 | 備註 |
|------|---------|------|
| $f^{-1}$（反函數記號） | **“f inverse”** | 絕不念 “f to the minus one”。例外：若課文**刻意對比** $\sin^{-1}$ 記號與 $1/\sin$，該處照字面念 “sine to the minus one” 並講清不是倒數。 |
| $x_1,\ x_2$（下標） | **“x sub one”, “x sub two”** | 正式定義／證明語境最無歧義。 |
| $x^2,\ x^3$ | “x squared”, “x cubed” | |
| $\sqrt[3]{x}$ / $\sqrt[3]{y-2}$ | “the cube root of x” / “…of **the quantity** y minus two” | 和/差根號加 “the quantity” 消歧義。 |
| $(\sqrt[3]{x-2})^3$ / $(f^{-1}(x))^2$ | “…, **all cubed**” / “…, **all squared**” | 外層次方蓋整體。 |
| 分數 $\tfrac{a}{b}$ | “a over b”（簡單分數念 “one half / one quarter / nine-fifths”…） | |
| 複雜分數（分子或分母含乘積／根號） | “…, all over …” 或 “… divided by the quantity …” | 例：$\tfrac{1}{2\sqrt2}$→“one over the quantity two root two”（“the quantity” 群組分母、防 (1/2)√2 誤聽）；$-\tfrac{2\sqrt5}{5}$→“negative two root five over five”（兩種群組同值、免 quantity）（NFA §1.2 D5）。 |
| 分子整個是和／差 $\tfrac{A+B}{2}$ | “**the quantity** A plus B, **all over** two” | 絕不念 “A plus B over two”（會被聽成 $A+\tfrac B2$）。注意與下一列方向相反：這一列是**和在分子內**。（§3.1 Task D 實證的 D3 blocking） |
| 加法在分數外 $x+\tfrac h2$ | “x plus **one half** h” | 絕不念 “x plus h over two”（會被聽成 $\tfrac{x+h}2$）。（§3.1 gate-2 實證的 D3 blocking） |
| 函數的和／差引數 $\sin(u+v)$ | “sine of **the quantity** u plus v” | 絕不念 “sine of u plus v”（會被聽成 $(\sin u)+v$）。$\sin\tfrac h2$ → “sine of h over two” 在**有上下文與畫面支撐時**可省群組詞，否則念 “sine of one half h”。（§3.1 Task D 實證的 D3 blocking） |
| 區間 $[a,b]$ / $(a,b)$ | “the (open) interval from a to b” | |
| 座標點 $(a,b)$ | **“the point with coordinates a and b”** | 無視覺符號時最清楚。 |
| $\pi/2$、$\arcsin$… | “pi over two”、“arcsine of …” | 反三角直接念 arc-名。 |
| domain $A$ / range $B$ | “domain A / range B” | |

## 三、逐段口語稿

> 每段 `uNN · id` 即該單元 `assistant` 訊息內容（`{show}` 已移除）。intro/outro 無旁白，不列。

### u3 · why_composition_is_missing
We can differentiate sine and cosine now -- but only in their bare form. We can handle sine x, yet nothing so far reaches sine of x squared or the square root of the quantity one plus x squared, where one function is fed into another. We built rules for sums, products, and quotients -- but never for composition, the operation of dropping one function inside another. That is the one gap left, and the chain rule fills it exactly -- and with it, the toolkit for differentiation is finally complete.

### u4 · rates_multiply_intuition
Here's the whole idea in one picture. Near a point, a differentiable function behaves like its tangent line -- it scales a small change in its input by its slope, with an error that shrinks faster than the change does. Now chain two together: g scales a small increment h by g prime of x, and then f scales that by f prime at g of x. The two magnifications stack -- so the composite scales h by the product f prime at g of x, times g prime of x. That's the chain rule; the proof, later, is just checking the two small errors stay negligible once chained.

### u5 · chain_rule_statement
Let's state it precisely. If g is differentiable at x sub zero, and f is differentiable at g of x sub zero, then the composition P of x equals f of g of x is differentiable at x sub zero too. And its derivative is the outer derivative at the inner function, times the inner derivative. Read it from the inside out. We'll earn this with a proof a little later -- for now, let's learn to use it.

### u6 · composed_mapping_figure
Picture the rule as a relay of two stretches. Start with a small increment h sitting at x sub zero. The first function g carries it forward and stretches it to about g prime of x sub zero, times h, now sitting at u sub zero equals g of x sub zero. The second function f stretches that again by its own slope there, landing at about f prime at g of x sub zero, times g prime of x sub zero, times h. Two stretches one after the other -- and stretching by one factor then another just multiplies the factors. That's why the composite's slope is the product of the two local slopes.

### u7 · leibniz_form
There's a second way to write the rule, and it's the one you'll actually compute with. Name the inner variable u equals g of x and the output y equals f of u. Then the chain rule takes its memorable shape: the rate of y per x equals the rate of y per u times the rate of u per x. It looks as though the d u's simply cancel -- a handy way to remember it, but not a proof. These aren't fractions with a common factor to strike out; each is a limit. What truly makes the rule work is the error argument we're about to give.

### u8 · decomposition_strategy
Here's a reliable way to take any composition apart -- work from the outside in. First, spot the outermost operation -- the last thing you'd do if you plugged in a number. That's the outer function f. Whatever it's applied to is the inner function u equals g of x. Differentiate the outside at the inside, keeping the inside whole. Then multiply by the inner derivative.

### u9 · decomposition_strategy_repeat
And if the inside is itself a composition, just run the steps again. So the square root of the quantity one plus x squared has outer root and inner one plus x squared; sine of x squared has outer sine and inner x squared.

### u11 · proof_strategy_bridge
The rule is already usable -- now let's earn it. To prove the two slopes really multiply, we handle both functions' tangent-line approximations at once -- and for that we repackage what differentiable means. Two facts we'll lean on without re-proving: the product rule, and that a differentiable function is continuous. We earlier called f differentiable at x sub zero when its difference quotient has a limit -- and that limit is f prime of x sub zero. We're about to say exactly the same thing, only phrased as approximation by a straight line.

### u12 · remainder_form_definition
Here's the form. We say f is differentiable at x sub zero if there's a number m and a function R with this equation, where the remainder over h goes to zero. The number m is just the derivative, f prime of x sub zero. Informally: f of the quantity x sub zero plus h equals its tangent-line value plus an error that dies faster than h itself. That "faster than h" is the whole point -- it's what lets these pieces compose.

### u13 · remainder_tangent_figure
Let's watch that error shrink. Here's the graph of f near x sub zero, hugging its tangent line. At a nearby point x sub zero plus h the two don't quite agree, and the little vertical gap between them is exactly the remainder R of h. Now halve h. The gap doesn't merely halve -- it collapses far faster, shrinking to nothing next to h. That's the picture of the remainder over h going to zero. And this single-curve fact is what's underneath the composition: up close, each function is almost its own tangent line, and it's those straight-line parts whose slopes multiply.

### u14 · two_forms_equivalent
Before we use this, let's check it's not a new idea -- just the old one rewritten. The claim: the limit form and the remainder form are equivalent, with the same m. One direction -- if the difference quotient tends to m, set R of h equals f of the quantity x sub zero plus h, minus f of x sub zero, minus m h; then the ratio of R of h to h is that quotient minus m, which goes to zero. The other way runs backward: divide the remainder equation by h and the quotient becomes m plus the ratio of R of h to h, which goes to m. Same property, same derivative -- two ways of saying one thing.

### u15 · proof_setup_substitution
Now the proof, and the remainder form does the heavy lifting. Because g is differentiable at x sub zero, write it in remainder form, with m sub one equals g prime of x sub zero. Because f is differentiable at g of x sub zero, apply its remainder form too -- with m sub one times h, plus R sub one of h, playing the role of h. Collect the part linear in h, and sweep everything else into a single remainder R sub three. Matched against the remainder form, that already gives the derivative we want -- provided the ratio of R sub three of h to h goes to zero. That one limit is all that's left.

### u16 · proof_easy_piece
Split that quotient into two pieces. The first is easy: m sub two is a constant and the ratio of R sub one of h to h goes to zero, so the whole first piece goes to zero. And note for later -- the inner increment m sub one times h, plus R sub one of h, itself goes to zero, since both m sub one times h and R sub one of h do. So the easy piece is settled; everything delicate now lives in the second piece.

### u17 · proof_delicate_choices
The second piece is the careful one -- a remainder of f at that wobbling inner increment, over h. Run an epsilon-delta argument; fix any epsilon greater than zero. Since the ratio of R sub two of y to y goes to zero, there's a delta so the relative remainder of f is below epsilon for zero less than the absolute value of y, less than delta. Since the inner increment goes to zero, there's an alpha keeping it below delta for zero less than the absolute value of h, less than alpha. Take such an h. If the inner increment is exactly zero, then R sub two of zero equals zero and the piece is just zero. So only the nonzero case is left.

### u18 · proof_delicate_bound
Take the nonzero case. Multiply and divide by the inner increment, splitting the piece into two factors. The second factor is below epsilon by our choice of delta, the first is bounded by the triangle inequality, and shrinking the window once more so the absolute value of the ratio of R sub one of h to h is less than one puts the whole piece below the quantity, the absolute value of m sub one, plus one, times epsilon. A fixed constant times epsilon, and epsilon was arbitrary -- so this piece vanishes too. Both pieces vanish, the ratio of R sub three of h to h goes to zero, and the chain rule is proved.

### u20 · example_single_composition
Time to use it -- two quick ones. For the square root of the quantity one plus x squared, the outer is the square root and the inner is one plus x squared: the outer derivative times two x tidies to x over the square root of the quantity one plus x squared. For sine of x squared, the outer is sine and the inner is x squared: cosine of the inside times two x. Notice that two x in each -- it's the inner derivative, and forgetting it is the single most common slip.

### u21 · caution_inner_derivative
Let's make that mistake explicit, so you never make it. The most common chain-rule error is to differentiate the outer function and then stop -- to write the derivative of sine of g of x as just cosine of g of x. That's wrong; the right answer carries the inner factor g prime of x. The two x back in sine of x squared is never optional.

### u22 · example_nested_three_layers
Now let the inside be a composition too -- the square root of the quantity one plus sine squared x is three layers deep, since sine squared x is itself sine x, all squared. The square root gives one over twice itself, times the derivative of the inside. That inside derivative is the square of sine x, which by the chain rule again is two sine x cosine x. Three layers, three factors -- and they simply multiply down the chain.

### u23 · example_chain_times_quotient
Sometimes the inner derivative is a small problem of its own. The outer is the square root, the inner is the fraction -- so the chain rule gives one over twice the root, times the derivative of the fraction. And that derivative is a quotient rule: it comes out to three over the square of the quantity x plus two. Tidy the front factor and multiply -- the answer is three over twice the product. The chain rule started the job; the quotient rule finished the inside.

### u24 · example_chain_times_product
Same story, a different partner rule. The outermost operation is a product, so start with the product rule. The leftover derivative needs the chain rule, since cosine squared x is cosine x, all squared -- giving minus two sine x cosine x. Put it together. The product rule split the work; the chain rule supplied the slope inside the second piece.

### u25 · example_leibniz_rates
Here's the Leibniz form earning its keep. Kelp K depends on the urchins U that eat it, and U on the otters O that eat them. Read each link: more urchins, less kelp, so d K over d U is negative; more otters, fewer urchins, so d U over d O is negative. The chain rule chains the two rates. A product of two negatives is positive -- so d K over d O is positive: more otters ultimately means more kelp. The signs multiply along the chain.

### u26 · toward_section_3_3
With the chain rule in hand, any function you build by composing the elementary ones can now be differentiated, almost mechanically. But the rule does something more interesting next -- it becomes a key, unlocking derivatives we couldn't otherwise reach: the inverse functions, and even something like x to the x through a clever trick. That's where we head next.

### u27 · recap
Pull the section together. The chain rule differentiates a composition: the outer derivative at the inner function, times the inner derivative. In Leibniz form, the rates multiply. To use it, decompose from the outside in -- every layer contributes one slope factor. The number-one pitfall is dropping the inner derivative; and underneath it all, each function is locally its tangent line, so the local slopes multiply.

---

## 四、備忘

- 口語文字單一源＝ `content_scripts/ch03_chain_rule.spoken.yml`；本檔與 `storyboards/ch03_chain_rule_mimo.yml` 皆由 `derive_spoken.py` 生成。
- `{show}` beat 切分與正典 storyboard 對齊（`derive_spoken.py --check` 守門）。
- 計費：MiMo 公測限免但屬外部 API；批次合成前依 `CLAUDE.md` 報用量、徵同意。
