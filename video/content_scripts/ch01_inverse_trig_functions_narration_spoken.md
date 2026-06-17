# §1.2 Inverse Trigonometric Functions — 旁白口語版（版本 B · MiMo-V2.5-TTS 客製）

> **此檔為生成檔（DO NOT EDIT）。** 由 `content_scripts/ch01_inverse_trig_functions.spoken.yml`（口語單一源） 經 `pipeline/derive_spoken.py` 生成。要改旁白請改 `.spoken.yml` 後重生。
> **性質：版本 B（口語 TTS 版）。** 英文散文逐字忠於內容稿 `narration`，**只把數學攤成口語**（無 LaTeX），供不能直讀 LaTeX 的 TTS（MiMo）照念。對照閱讀版（版本 A，數學渲染）＝ `ch01_inverse_trig_functions_narration.html`。
> **NFA 稽核狀態：** 見 `content_scripts/_audit/`（每節各自記錄）。

---

## 一、MiMo 合成設定（現用）

| 項目 | 值 |
|------|----|
| `model` | `mimo-v2.5-tts` |
| `audio.voice` | `Mia`（英文女聲）／備選 Dean·Milo·Chloe |
| `audio.format` | `wav`（24kHz/mono/PCM16，與產線 `write_pcm_wav` 相容；beat WAV 自動裁頭尾靜音） |

**全域風格指令（放每次呼叫的 `user` 訊息）— YouTube 科普風、正常語速：**

```
Read like the narrator of a polished YouTube science explainer: clear, engaging,
and conversational, at a normal talking pace — natural momentum, not slow or drawn
out, and no long dramatic pauses, just ordinary pauses at sentence ends. Warm and
lightly energetic, curious rather than solemn, like explaining an idea to a smart
friend. Pronounce every mathematical expression clearly and correctly.
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

### u2 · recovering_angles
We can run the trigonometric functions forwards all day — feed in an angle, read off a ratio. This section runs them the other way: we are handed a ratio, and we want the angle that produced it. The slope of a ramp gives back an angle of inclination; a ratio of two sides of a right triangle gives back one of its angles. But there is an obstacle. The trig functions repeat their values endlessly, so on their full domains they are nowhere near one-to-one — and a function that is not one-to-one has no inverse. The way out is the move we already know: restrict each trig function to an interval where it is one-to-one, and invert that restricted piece. So the real work of this section is choosing the right interval for each one.

### u3 · sine_is_not_one_to_one
Start with sine, and watch exactly why it cannot be inverted as it stands. Slide a horizontal line across the graph of y equals sine x: at almost every height it crosses not once but over and over, marching off in both directions forever. Each of those crossings is a different angle with the very same sine. So a single value of sine comes from infinitely many angles, and there is no way to choose which one to send back. Sine is badly not one-to-one on the whole real line — and that is the problem we have to fix before any inverse can exist.

### u4 · restrict_sine_branch
Here is the fix. Keep only the middle piece of the sine graph, the part between negative pi over two and pi over two. On that one interval sine climbs steadily from negative one up to one, never repeating a value along the way — so it is one-to-one there, and it still reaches every output from negative one to one. That restricted piece has exactly what we need: it can be reversed, and it gives up nothing in the range. This is the branch we are going to invert.

### u5 · arcsine_definition
Now we can name the inverse. The inverse sine of x, written arcsine of x, is the angle in our restricted interval whose sine is x. In symbols, arcsine of x equals y means sine of y equals x, with y between negative pi over two and pi over two. Reading that straight off the branch, its domain is everything from negative one to one — the values sine can produce — and its range is the interval from negative pi over two to pi over two. One warning about notation, the same one as before: arcsine of x is often written sine inverse of x, but that negative one means inverse, not reciprocal — it is not one over sine x. When a source writes sine inverse, check the context to see which is meant.

### u6 · arcsine_identities
Sine and arcsine undo each other — but you have to watch the direction. Going out and back, sine of arcsine of x equals x for every x from negative one to one: hand in a legal ratio, take its angle, then take that angle's sine, and you land back on the ratio. The other order, arcsine of sine of x equals x, only returns the original angle when that angle was already inside the restricted interval. Push outside it and arcsine cannot follow you home — take x equals pi: sine of pi is zero, and arcsine of zero is zero, not pi. Arcsine always answers with the angle in its own interval, even when that was not the angle you started from.

### u7 · reference_triangle_method
There is a clean recipe for evaluating something like the tangent of an arcsine — a trig function wrapped around an inverse-trig expression. Step one: name the inside. Set theta equal to the inverse-trig expression, which immediately hands you one ratio — if theta equals arcsine of x, then sine of theta equals x. Step two: draw a right triangle whose sides realise that ratio, using positive lengths for its magnitude. Step three: fill in the missing side with the Pythagorean theorem. Step four: read off whatever trig value you were after, straight from the completed triangle — and fix the sign separately, from the principal-value interval, not from the picture. The triangle gives you the size; the interval gives you the sign.

### u8 · evaluating_arcsin
Let us evaluate two. First, arcsine of one half: we want the angle in our interval whose sine is a half, and that is pi over six — read straight off a special angle, no triangle needed. The second is the kind the recipe was built for: the tangent of arcsine of one third. Set theta equals arcsine of one third, so sine of theta is a third, an angle in the first quadrant. Draw a right triangle with opposite side one and hypotenuse three; the adjacent side is the square root of nine minus one, which is two root two. Tangent is opposite over adjacent, so tangent of theta is one over the quantity two root two. We never named the angle itself — but the triangle handed us its tangent.

### u9 · restrict_cosine_branch
Cosine needs the same treatment, but a different interval — its own middle piece would fail, because cosine is symmetric across zero and would just repeat. So watch cosine instead on the interval from zero to pi. It starts at one, slides down steadily, and ends at negative one, hitting every value in between exactly once. On that interval cosine is one-to-one and still sweeps the full range — the natural counterpart of the interval we picked for sine. That is the branch we invert to get the inverse cosine.

### u10 · arccosine_definition
The inverse cosine follows the very same script. The inverse cosine of x, written arccosine of x, is the angle between zero and pi whose cosine is x: arccosine of x equals y means cosine of y equals x, with y from zero to pi. Its domain is again everything from negative one to one — the values cosine can take — and this time its range runs from zero to pi. Same idea as arcsine, just anchored on cosine's interval instead of sine's.

### u11 · arccosine_identities
The cancellation identities copy straight over. Cosine of arccosine of x equals x for every x from negative one to one — out and back, no fine print. And arccosine of cosine of x equals x as well, but, exactly as with sine, only when the starting angle was already between zero and pi. It is the same one-directional pattern as for sine — and we will pin it down for all three in just a moment.

### u12 · domain_of_compositions
Inverse trig functions are fussy about what they will accept, so let us practise finding the domain of a composition. Take f of x equals arcsine of cosine of x. Whatever x is, cosine x already lands between negative one and one — and that is precisely what arcsine accepts — so every real number is allowed; the domain of f is all of the real numbers. Now flip the order: h of x equals sine of arccosine of x. The inner function, arccosine, demands an input from negative one to one; its output is just an angle, and sine will swallow any angle, so the domain of h is negative one to one. The rule behind both: first make sure the input is legal for the inner function, then make sure the inner function's output is legal for the outer one.

### u13 · principal_value_trap
Here is a trap worth springing once, on purpose. A particle starts moving at time t equals ten and bobs up and down, its height at time t equal to cosine t. True or false: the particle has height one at time t equals arccosine of one? It is false — and the reason is exactly what makes inverse trig subtle. The equation cosine t equals one holds at infinitely many times, but arccosine returns only its one principal value, t equals zero. And at t equals zero the particle is not even moving yet; its motion only begins at t equals ten. The particle really does reach height one, at the times t equals two pi n once n is large enough. But arccosine of one is zero, which is not one of them. An inverse trig function gives you a single angle, never the whole family.

### u14 · restrict_tangent_branch
Tangent gets the most dramatic interval of the three. On the open interval from negative pi over two to pi over two, tangent climbs without bound: it plunges toward negative infinity at the left edge, rises through zero in the middle, and races up toward positive infinity at the right edge. Along the way it passes through every real number, and through each one exactly once. That is why the inverse tangent is the generous one — where arcsine and arccosine only take inputs between negative one and one, arctangent accepts every real number you can hand it.

### u15 · arctangent_definition
So here is the inverse tangent. The inverse tangent of x, written arctangent of x, is the angle strictly between negative pi over two and pi over two whose tangent is x: arctangent of x equals y means tangent of y equals x, with y in that open interval. Because tangent reached every real value, the domain of arctangent is all of the real numbers — no restriction on the input at all — and its range is the open interval from negative pi over two to pi over two, edges never quite reached.

### u16 · arctangent_identities
Tangent and arctangent undo each other on the same terms. Tangent of arctangent of x is x for every real x; arctangent of tangent of x is x only when the angle was already in the open interval. And now the pattern across all three inverses is worth stating once and for all. Outer-undoes-inner is always safe on the natural domain — sine of arcsine of x, cosine of arccosine of x, and tangent of arctangent of x each give back x with no conditions. But inner-undoes-outer returns your angle only inside the principal interval. Step outside, and the inverse hands back the equivalent angle that does live there: arctangent of tangent of pi is arctangent of zero, which is zero, not pi.

### u17 · evaluating_inverse_trig
Now the triangle method earns its keep on harder values — same recipe, trickier signs. First, the sine of arccosine of negative one half. Arccosine of a negative input always lands in the second quadrant, here at two pi over three, and its sine is root three over two. Second, the secant of arctangent of ten: set the angle with tangent ten, build a triangle with opposite ten and adjacent one, and the hypotenuse is the square root of one hundred and one — so the secant, hypotenuse over adjacent, is the square root of one hundred and one. Third, the tangent of arcsine of negative two root five over five. The sine is negative, so the angle sits in the fourth quadrant, where cosine is positive; the triangle gives cosine one over root five, and the tangent works out to negative two. Every time, the triangle set the size and the principal interval set the sign.

### u18 · simplify_cos_arctan
One more, and this time the answer is a formula, not a number. Simplify the cosine of arctangent of x, for a general x. Let y equals arctangent of x, so tangent of y equals x, with y in the open interval — and what we want is cosine of y. Reach for the identity one plus tangent squared y equals secant squared y: it turns secant squared y into one plus x squared. Since y lives in the open interval, cosine is positive there, so secant is positive too, and secant of y is the square root of the quantity one plus x squared. Cosine is one over secant — so the cosine of arctangent of x is one over the square root of the quantity one plus x squared. A whole family of values, caught in one clean expression.

### u19 · remaining_inverse_trig
That completes the three main inverses; three more round out the set, used less often but built the same way. The inverse cosecant, inverse secant, and inverse cotangent each invert their function on a chosen principal range — the interval their output angle is pinned to. Cosecant and secant only take values of size at least one, so inverse cosecant and inverse secant accept inputs from one outward in both directions; cotangent, like tangent, reaches everything, so inverse cotangent has domain all of the real numbers. The principal ranges this time are a little less tidy — built from two pieces apiece — but the principle has not changed at all: pick an interval where the function is one-to-one, and invert there.

### u20 · conventions_change_answers
Those principal ranges are choices, not laws — and the choice has visible consequences. Different books pick different intervals for inverse secant and inverse cosecant, and this text deliberately fixes one set, the one that keeps later formulas clean. Here is a function that exposes the stakes: f of x equals arcsine of x plus inverse cosecant of x. Arcsine needs x between negative one and one; inverse cosecant needs x of size at least one — so the only inputs both allow are x equals one and x equals negative one, a domain of just two points. At x equals one, both pieces are pi over two, so f is pi. At x equals negative one, arcsine is negative pi over two, and under this text's convention inverse cosecant is three pi over two — so f is pi again. The function is just the constant pi. But switch to the other common convention, where inverse cosecant of negative one is negative pi over two, and f of negative one would come out negative pi instead — same function, different answer, purely from the branch choice. That is exactly why we fix a convention up front.

### u21 · recap
Let us pull the section together. Every inverse trig function starts the same way: a trig function is not one-to-one, so we restrict it to a branch where it is, and invert that branch. Arcsine lives on negative pi over two to pi over two, arccosine on zero to pi, and arctangent on the open interval between — which is why arctangent alone accepts every real number, while arcsine and arccosine only take inputs from negative one to one. Each inverse returns a single principal value, never the whole family of angles, so the cancellation identities only run cleanly in the outer-undoes-inner direction. And to evaluate a trig function of an inverse-trig expression, draw the reference triangle for the size and read the sign off the principal interval. Restrict, invert, and mind the principal value — that is the whole section.

---

## 四、備忘

- 口語文字單一源＝ `content_scripts/ch01_inverse_trig_functions.spoken.yml`；本檔與 `storyboards/ch01_inverse_trig_functions_mimo.yml` 皆由 `derive_spoken.py` 生成。
- `{show}` beat 切分與正典 storyboard 對齊（`derive_spoken.py --check` 守門）。
- 計費：MiMo 公測限免但屬外部 API；批次合成前依 `CLAUDE.md` 報用量、徵同意。
