# §3.1 Derivatives of Sine and Cosine — 旁白口語版（版本 B · MiMo-V2.5-TTS 客製）

> **此檔為生成檔（DO NOT EDIT）。** 由 `content_scripts/ch03_trig_derivatives.spoken.yml`（口語單一源） 經 `pipeline/derive_spoken.py` 生成。要改旁白請改 `.spoken.yml` 後重生。
> **性質：版本 B（口語 TTS 版）。** 英文散文逐字忠於內容稿 `narration`，**只把數學攤成口語**（無 LaTeX），供不能直讀 LaTeX 的 TTS（MiMo）照念。對照閱讀版（版本 A，數學渲染）＝ `ch03_trig_derivatives_narration.html`。
> **NFA 稽核狀態：** 見 `content_scripts/_audit/`（每節各自記錄）。

---

## 一、MiMo 合成設定（現用）

| 項目 | 值 |
|------|----|
| `model` | `mimo-v2.5-tts-voicedesign` |
| `voice design` | `Calm Professor`（預設角色；不送 `audio.voice`） |
| `audio.format` | `wav`（24kHz/mono/PCM16，與產線 `write_pcm_wav` 相容；beat WAV 自動裁頭尾靜音） |
| `optimize_text_preview` | `false`（照原旁白念，不讓平台自動改稿） |

**全域 voice-design prompt（放每次呼叫的 `user` 訊息）：**

```
A mature American university professor in his early 50s, clear baritone voice,
calm and authoritative without sounding stiff. Warm but precise, measured medium
pace, careful articulation of mathematical expressions, with short natural pauses
at clause boundaries.
```

**Audio tag：** 維持預設**不啟用**（口語稿純文字，節奏靠風格指令＋標點）。

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
| 區間 $[a,b]$ / $(a,b)$ | “the (open) interval from a to b” | |
| 座標點 $(a,b)$ | **“the point with coordinates a and b”** | 無視覺符號時最清楚。 |
| $\pi/2$、$\arcsin$… | “pi over two”、“arcsine of …” | 反三角直接念 arc-名。 |
| domain $A$ / range $B$ | “domain A / range B” | |

## 三、逐段口語稿

> 每段 `uNN · id` 即該單元 `assistant` 訊息內容（`{show}` 已移除）。intro/outro 無旁白，不列。

### u3 · why_trig_is_different
Every derivative so far has yielded to algebra. For a polynomial we expanded the quantity x plus h, to the n, and the binomial theorem handed us a factor of h to cancel; for e to the x the power series did the same job. The trigonometric functions refuse to play along. Write down the difference quotient for sine x and try the usual move. You cannot simply set h equal to zero: that gives zero over zero, which tells you nothing. And no identity cancels the h in the denominator -- sine of the quantity x plus h simply does not break into pieces that conveniently subtract. As we are about to see, the whole computation funnels down to a single limit, the limit of sine theta over theta -- again the indeterminate form zero over zero, and one that no algebra will crack. Prying it open takes a genuinely new tool: a geometric comparison of areas on the unit circle. And once we secure that one limit, it unlocks the derivatives of both sine and cosine at once. One ground rule, though: throughout, angles are measured in radians -- an assumption that turns out to be essential.

### u4 · difference_quotient_for_sine
So let us transform that difference quotient instead of fighting it head-on. The decisive step is one trigonometric identity -- sum-to-product -- which turns a difference of sines into a product. Here it is; and a product is exactly what we want, because we can pull it apart and take limits one factor at a time. Put A equals x plus h and B equals x, and the numerator becomes two cosine of the quantity x plus one half h, times sine of h over two. Now divide by h -- and here is the small trick that makes everything line up: write h as two times h over two, so the denominator carries the very h over two inside the sine. The quotient cleans up to cosine of the quantity x plus one half h, times sine of h over two, all over h over two. Look at what we have: a product of two factors. The first slides to cosine x, provided cosine is continuous; the second is exactly sine theta over theta with theta equals h over two. So the whole derivative hangs on just two facts -- continuity, and that fundamental limit. We secure both now.

### u6 · sector_inequality
Here is that new tool. We compare three areas on a circle of radius one. But first, one convenience that saves us half the work. Replacing theta by negative theta flips the sign of both theta and sine theta, so the ratio sine theta over theta is even -- whatever we learn for positive angles holds for negative ones, so it is enough to chase theta down to zero from the positive side. Now the geometry. On the unit circle, A is at the point with coordinates one and zero, B is the point at angle theta, and extending the radius to the tangent at A gives C equals the point with coordinates one and tangent theta. The inner triangle O A B has base one and height sine theta, so its area is one half sine theta. The sector O A B is the fraction theta over two pi of the disc -- area one half theta. And the outer triangle O A C has height tangent theta, so its area is one half tangent theta. Each region sits inside the next, so the areas line up in order: one half sine theta, then one half theta, then one half tangent theta. The whole argument hangs on that one picture.

### u7 · squeeze_to_the_bound
Now turn that chain of areas into a statement about sine theta over theta, one careful step at a time. Multiply through by two to clear the halves: sine theta at most theta at most tangent theta. Divide every part by sine theta, positive here, and rewrite tangent theta as sine theta over cosine theta -- giving one at most theta over sine theta at most one over cosine theta. The middle is upside down, so take reciprocals of all three. They are positive, and flipping positives reverses the inequalities, so the chain turns around: cosine theta at most sine theta over theta at most one, for theta between zero and pi over two. And pocket one more consequence: from sine theta at most theta we also get zero at most the absolute value of sine theta at most the absolute value of theta near zero -- a bound we lean on twice in a moment.

### u8 · continuity_statement_sin_limit
That little bound does more than help with the limit -- it is the key to continuity. And continuity here means something concrete: nudge the angle a little, and sine and cosine move only a little; they never jump. We even have the tool that says so -- on the unit circle the half-chord sine theta is always shorter than the arc theta above it, which is just the absolute value of sine theta at most the absolute value of theta read geometrically. So here is the claim, made precise: sine x and cosine x are continuous at every real x sub zero. Build it from the ground up. Since zero at most the absolute value of sine theta at most the absolute value of theta, and the absolute value of theta itself goes to zero, the squeeze theorem forces sine theta to go to zero. That single limit is the seed; the full continuity grows straight out of it, which is what we do next.

### u9 · continuity_argument
Now turn that seed into full continuity. Fix a point x sub zero, and ask how much cosine x and sine x can change as x moves toward it. Sum-to-product answers both at once. For cosine, cosine x minus cosine x sub zero is negative two sine of the quantity x minus x sub zero, over two, times sine of the quantity x plus x sub zero, over two; and for sine, sine x minus sine x sub zero is two cosine of the quantity x plus x sub zero, over two, times sine of the quantity x minus x sub zero, over two. In each, the half-sum factor never exceeds one in size. Drop it to its largest size, one, and both differences are bounded by the same thing -- twice the absolute value of sine of the quantity x minus x sub zero, over two. Now let x go to x sub zero: the half-angle goes to zero, so that bound collapses to zero. Squeeze one last time, and cosine x goes to cosine x sub zero, sine x goes to sine x sub zero -- both continuous everywhere.

### u10 · fundamental_limit
Now we can finally close the limit that started all of this. The claim is as clean as it gets: sine theta over theta tends to one as theta goes to zero. And we already built the trap. For theta between zero and pi over two, the ratio is pinned between a floor and a ceiling: cosine theta at most sine theta over theta at most one. The ceiling is the constant one. The floor is cosine theta, which tends to one now that we know cosine is continuous -- so the squeeze pins the ratio to one from the right. And because the ratio is even, its left limit matches its right, so the two-sided limit is one as well. That is the keystone.

### u11 · squeeze_graph
It helps to picture that squeeze. Here runs cosine theta, the dashed floor. And the ceiling -- the constant line at height one. Between them, the ratio sine theta over theta, caught in the narrowing gap. As theta slides toward zero the floor rises to one and the ceiling already is one, so the curve is squeezed right to one. Notice the open circle at theta equals zero: the ratio is undefined there, zero over zero. So what equals one is the limit -- the height the curve is forced toward, not a value it ever takes.

### u12 · limit_not_identity
One caution, because this result is easy to over-read. The statement is about the limit as theta goes to zero -- not an identity. At a fixed angle the ratio is generally not one: at theta equals pi over two it is two over pi, about zero point six four, and at theta equals pi it is zero. The value one is reached only in the limit.

### u13 · radians_essential
A second caution, and this one is structural. Everything here depends on radians. The sector area one half theta -- and with it the limit -- uses radian measure. Switch to degrees and the limit is pi over one hundred eighty, not one, so the derivative drags that factor along. The clean formulas sine prime equals cosine and cosine prime equals negative sine hold only in radians.

### u15 · derivative_of_sine
Now the payoff, and it falls into our hands. The claim: the derivative of sine x is cosine x, for every real x. Start from the definition -- the derivative is the limit of the difference quotient. But we already did the hard algebra: that quotient is cosine of the quantity x plus one half h, times sine of h over two, all over h over two. Let h go to zero: the first factor tends to cosine x by continuity, the second to one by the fundamental limit. A continuous thing times a limit -- the product is cosine x times one, just cosine x.

### u16 · derivative_of_cosine
Cosine falls to the very same machinery -- only the identity changes, so we go quickly. The claim: the derivative of cosine x is negative sine x. This time use the companion sum-to-product formula. The same division by h turns the difference quotient into negative sine of the quantity x plus one half h, times sine of h over two, all over h over two. Send h to zero: the sine factor tends to sine x by continuity, the second to one by the fundamental limit. The leading minus sign comes along -- leaving negative sine x. Same two tools, one extra minus sign.

### u17 · slope_equals_height
Here is what that theorem looks like on the graph. Draw y equals sine x, and check the slope of its tangent at a few points. At x equals zero it is climbing at slope one. At x equals pi over two, the top of the hump, the tangent is flat -- slope zero. At x equals pi it is falling at slope minus one. Now lay y equals cosine x on top, and read its heights at those same points: one, zero, minus one. They match exactly -- the slope of sine is the height of cosine, the theorem drawn.

### u18 · derivative_cycle
Step back and watch the pattern these two derivatives make. Differentiation sends sine and cosine into each other, with a minus sign that turns over every second step. Writing an arrow for one derivative: sine x to cosine x to negative sine x to negative cosine x, and back to sine x. Four derivatives and you are home -- the fourth derivative of sine is sine again. Where e to the x reproduces itself in a single step, these do it in a cycle of four: the self-renewal that lets them oscillate forever without winding down.

### u20 · companion_limit
The fundamental limit has a companion worth knowing: the quantity one minus cosine theta, over theta tends to zero. It is again zero over zero, so we need a way in. Multiply top and bottom by the conjugate one plus cosine theta; the numerator becomes a difference of squares, one minus cosine squared theta. And one minus cosine squared theta is just sine squared theta, so the whole thing splits into sine theta over theta times sine theta over the quantity one plus cosine theta. Let theta go to zero: the first factor goes to one, the second to zero over two. One times zero is zero.

### u21 · all_six_tan_sec
With sine and cosine in hand, the other four cost almost nothing -- just the quotient rule. Take tangent x equals sine x over cosine x. The quotient rule gives this. The numerator is cosine squared x plus sine squared x, which is one -- so the derivative of tangent x is secant squared x. Secant is the same idea on one over cosine x: the quotient rule, with a constant on top, gives this. Clean it up, and secant's derivative is secant x tangent x.

### u22 · all_six_cot_csc
The last two run exactly the same way. Take cotangent x equals cosine x over sine x. The quotient rule gives this. The numerator is minus the quantity sine squared x plus cosine squared x, again one -- so cotangent x differentiates to negative cosecant squared x. And cosecant x is one over sine x: the same rule lands this. Cleaned up, that is negative cosecant x cotangent x -- and all six are done, every one built on sine prime equals cosine and cosine prime equals negative sine.

### u23 · shm_compute
Let us put the new derivatives to work on something moving. A weight on a spring has height s of t equals sine t. Velocity is its derivative, s prime of t equals cosine t. Acceleration is the next derivative, s double prime of t equals negative sine t. But negative sine t is just negative s of t -- at every instant the weight is pushed back toward rest. That relation, s double prime equals negative s, is the signature of simple harmonic motion; sine and cosine are exactly the functions that describe it.

### u24 · shm_stacked_graphs
Stack the three graphs over one time axis and the relationship jumps out. On top, the height s equals sine t. In the middle, the velocity s prime equals cosine t. On the bottom, the acceleration s double prime equals negative sine t. Watch where the height hits a peak or a trough -- there the velocity passes through zero, because at the extremes the weight momentarily stops. And hold the bottom graph against the top: it is the top one flipped upside down. That is s double prime equals negative s, drawn -- the very picture of an oscillation.

### u25 · toward_the_chain_rule
We can now differentiate every trigonometric function -- but only in its bare form. We can handle sine x, yet not sine of x squared or sine of the quantity three x plus one, where the angle is itself a function tucked inside. To reach a function buried inside another, we need one more rule -- a way to differentiate a composition. That is the chain rule, and it is what comes next; with it, every derivative we found today becomes the seed of a whole family more.

### u26 · recap
Pull the section together. Everything grew from one limit: sine theta over theta tends to one, cracked by squeezing areas on the unit circle. That limit, with continuity, gave the two derivatives at the heart of the section -- sine differentiates to cosine, cosine to negative sine. From those two, the quotient rule delivered all the other trig derivatives -- tangent, cotangent, secant, cosecant. And keep the cycle in mind -- four derivatives of sine or cosine bring you home -- with the fine print that it all depends on radians.

---

## 四、備忘

- 口語文字單一源＝ `content_scripts/ch03_trig_derivatives.spoken.yml`；本檔與 `storyboards/ch03_trig_derivatives_mimo.yml` 皆由 `derive_spoken.py` 生成。
- `{show}` beat 切分與正典 storyboard 對齊（`derive_spoken.py --check` 守門）。
- 計費：MiMo 公測限免但屬外部 API；批次合成前依 `CLAUDE.md` 報用量、徵同意。
