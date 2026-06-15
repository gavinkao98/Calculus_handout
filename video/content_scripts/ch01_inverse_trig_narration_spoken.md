# §1.2 Inverse Trigonometric Functions — 旁白口語版（版本 B · MiMo-V2.5-TTS 客製）

> **此檔為生成檔（DO NOT EDIT）。** 由 `content_scripts/ch01_inverse_trig.spoken.yml`（口語單一源） 經 `pipeline/derive_spoken.py` 生成。要改旁白請改 `.spoken.yml` 後重生。
> **性質：版本 B（口語 TTS 版）。** 英文散文逐字忠於內容稿 `narration`，**只把數學攤成口語**（無 LaTeX），供不能直讀 LaTeX 的 TTS（MiMo）照念。對照閱讀版（版本 A，數學渲染）＝ `ch01_inverse_trig_narration.html`。
> **Mode B 稽核狀態：** 見 `content_scripts/_audit/`（每節各自記錄）。

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

## 二、數學念法慣例（全節通用；Mode B 裁定）

| 數學 | 口語念法 | 備註 |
|------|---------|------|
| $f^{-1}$（反函數記號） | **“f inverse”** | 絕不念 “f to the minus one”。例外：若課文**刻意對比** $\sin^{-1}$ 記號與 $1/\sin$，該處照字面念 “sine to the minus one” 並講清不是倒數。 |
| $x_1,\ x_2$（下標） | **“x sub one”, “x sub two”** | 正式定義／證明語境最無歧義。 |
| $x^2,\ x^3$ | “x squared”, “x cubed” | |
| $\sqrt[3]{x}$ / $\sqrt[3]{y-2}$ | “the cube root of x” / “…of **the quantity** y minus two” | 和/差根號加 “the quantity” 消歧義。 |
| $(\sqrt[3]{x-2})^3$ / $(f^{-1}(x))^2$ | “…, **all cubed**” / “…, **all squared**” | 外層次方蓋整體。 |
| 分數 $\tfrac{a}{b}$ | “a over b”（簡單分數念 “one half / one quarter / nine-fifths”…） | |
| 複雜分數（分子或分母含乘積／根號） | “…, all over …” 或 “… divided by the quantity …” | 例：$\tfrac{1}{2\sqrt2}$→“one divided by the quantity two times the square root of two”；$-\tfrac{2\sqrt5}{5}$→“negative the quantity two times the square root of five, all over five”。防 (1/2)√2 之類誤聽（Mode B §1.2 D5）。 |
| 區間 $[a,b]$ / $(a,b)$ | “the (open) interval from a to b” | |
| 座標點 $(a,b)$ | **“the point with coordinates a and b”** | 無視覺符號時最清楚。 |
| $\pi/2$、$\arcsin$… | “pi over two”、“arcsine of …” | 反三角直接念 arc-名。 |
| domain $A$ / range $B$ | “domain A / range B” | |

## 三、逐段口語稿

> 每段 `uNN · id` 即該單元 `assistant` 訊息內容（`{show}` 已移除）。intro/outro 無旁白，不列。

### u2 · angle_from_ratio
Picture a ramp rising at a steady slope, and suppose you know that slope exactly — it climbs one unit for every two it runs forward. A natural question follows: what angle does the ramp make with the ground? You know the ratio; you want the angle back. That is the whole job of the inverse trigonometric functions. The ordinary trig functions turn an angle into a ratio — feed in an angle, read off a sine or a tangent. The inverse functions run that backwards: hand them a ratio, and they return the angle that produced it. From the slope of a ramp we recover its inclination; from the sides of a right triangle we recover its angles. Before we can build these inverses, though, there is one obstacle to clear.

### u3 · trig_not_one_to_one
The obstacle is that none of the trig functions is one-to-one. Look at the sine curve running across the whole number line: it rises and falls forever, so a single horizontal line slices through it again and again. Many different angles share the very same sine — and a function whose outputs each come from many inputs simply cannot be run backwards. The cure is one we have seen before for functions that fail this way: cut the domain down to a single stretch on which the function never repeats a value. On that restricted piece the function is one-to-one, so it has an inverse. We will make this one move — restrict, then invert — for each trig function in turn.

### u4 · restrict_sine
Let us carry that out for sine. The standard branch to keep is the interval from negative pi over two to pi over two. On that piece the sine curve climbs steadily from negative one up to one, hitting every value in between exactly once — so it is one-to-one there, and its outputs fill the range from negative one to one. That restricted, well-behaved branch is the sine we will actually invert. Other intervals would serve in principle, but this one is centred on the origin and symmetric about zero, which is why it became the standard choice.

### u5 · arcsin_definition
Now we can name the inverse. The inverse sine function, written arcsine of x, takes a number between negative one and one and returns the angle on our restricted branch whose sine is that number. Stated precisely: arcsine of x equals y means exactly that the sine of y equals x and y lies in the interval from negative pi over two to pi over two. So its domain is the interval from negative one to one — the only ratios a sine can produce — and its range is that restricted interval of angles. One warning about notation: arcsine of x is often written sine to the minus one of x, but that superscript minus one does not mean a reciprocal. Sine to the minus one of x is an angle; one over the sine of x is a number. Whenever a source writes sine to the minus one, read the context to see which one is meant.

### u6 · arcsin_identities
Because arcsine undoes the restricted sine, the two compose back to give the input — but watch the fine print on where each holds. One way, the sine of arcsine of x equals x for every x in the interval from negative one to one: take a ratio, find its angle, take the sine, and you are back to the ratio. The other way, arcsine of the sine of x equals x — but only when x already lives in the restricted range from negative pi over two to pi over two. That asymmetry between the two is not a slip of the pen, and the next case shows exactly why it is there.

### u7 · when_arcsin_sin_breaks
Here is what happens when the inner angle sits outside the restricted range. Take x equals pi. Its sine is zero, so arcsine of the sine of pi equals arcsine of zero — and arcsine always hands back the angle in the interval from negative pi over two to pi over two, which is zero, not pi. So arcsine of the sine of pi equals zero. The reason is structural: arcsine can only ever return an angle from its own narrow range, so feed it the sine of a far-away angle and it gives back the one angle in range that shares that sine. The habit to build: before simplifying arcsine of the sine of x, check whether x is already in the range — if it is not, the answer is the in-range angle with the same sine, not x itself.

### u8 · arcsin_evaluate
Let us evaluate two expressions. First, arcsine of one half: we want the angle in the interval from negative pi over two to pi over two whose sine is one half. That is pi over six, so arcsine of one half equals pi over six. The second is more telling: the tangent of arcsine of one third. We are not asked for the angle itself, only for its tangent — so let us draw a right triangle. Call the angle theta, with the sine of theta equal to one third; that puts the side opposite theta at one and the hypotenuse at three. By the Pythagorean theorem the adjacent side is the square root of the quantity nine minus one, which equals two times the square root of two. Now tangent is opposite over adjacent, so the tangent of arcsine of one third equals one divided by the quantity two times the square root of two. That triangle move — turn the inverse trig value into a labelled right triangle, then read off whatever ratio you need — is the workhorse of this whole section.

### u9 · arccos_definition
Cosine needs the same repair, but on a different stretch. Cosine is not one-to-one either, and the branch we keep is the interval from zero to pi — where the curve runs steadily downhill from one to negative one. On that branch every value is hit once, so we can invert it. The inverse cosine, arccosine of x, is defined by arccosine of x equals y exactly when the cosine of y equals x and zero is less than or equal to y is less than or equal to pi; its domain is again the interval from negative one to one and its range is the interval from zero to pi. The composition identities read just like the ones for sine: the cosine of arccosine of x equals x on the interval from negative one to one, and arccosine of the cosine of x equals x as long as x stays in the interval from zero to pi. Same idea as before — only the interval of angles has moved.

### u10 · domain_of_composition
When inverse trig functions get composed with ordinary ones, the interesting question is often the domain. Take f of x equals arcsine of the cosine of x. Whatever x is, the cosine of x always lands in the interval from negative one to one — and the interval from negative one to one is exactly what arcsine accepts. So every real number is allowed: the domain of f is all real numbers. Now flip the order: h of x equals the sine of arccosine of x. Here the inner function arccosine demands an input in the interval from negative one to one, and its output is an angle, which sine is happy to take. So the domain of h is the interval from negative one to one. The rule worth keeping: the domain of a composition is set by what the inner function accepts and whether its outputs are legal for the outer one.

### u11 · principal_value_trap
One more trap, and it carries the single most important idea about these functions. An object starts moving at time t equals ten, bobbing so that its height afterwards is the cosine of t. True or false: it is at height one at the time t equals arccosine of one? The answer is false. The equation cosine t equals one holds at infinitely many times — t equals zero, two pi, four pi, and so on — but arccosine does not return all of them. It returns only its single principal value in the interval from zero to pi, which is t equals zero. And t equals zero is before the object is even moving. An inverse trig function hands back one angle, never the whole family of solutions. The object really is up at height one — at t equals four pi, six pi, and the multiples of two pi that fall after it starts moving — but arccosine of one equals zero is none of those.

### u12 · arctan_definition
Tangent is the third we invert, and it brings a new twist. We restrict it to the open interval from negative pi over two to pi over two, where it climbs without ever repeating — but unlike sine and cosine, tangent shoots off toward infinity at the ends, so it takes every real value. That flips the domain story: arctangent of x equals y means the tangent of y equals x with y strictly between negative pi over two and pi over two, and its domain is all real numbers — any ratio at all has an angle. Its range is the open interval from negative pi over two to pi over two, which it approaches but never reaches. The identities follow the usual pattern: the tangent of arctangent of x equals x for every real x, and arctangent of the tangent of x equals x on the open restricted interval. So arctangent takes the entire number line and gently squeezes it into a band less than half a turn wide.

### u13 · signs_from_range
When the inputs go negative, signs are where people slip — but the range of the inverse function settles every sign for you. Start with the sine of arccosine of negative one half. Since arccosine always lands in the interval from zero to pi, a negative input forces the angle into the second quadrant: arccosine of negative one half equals two pi over three, and its sine is the square root of three, divided by two. The same triangle method handles secant of arctangent of ten: opposite ten, adjacent one, hypotenuse the square root of one hundred one, so the secant is the square root of one hundred one. Now the delicate one: the tangent of arcsine of negative the quantity two times the square root of five, all over five. Here arcsine of a negative number lands in the fourth quadrant, where cosine is positive — so the cosine of theta equals one over the square root of five and the tangent of theta equals negative two. Notice we never guessed a sign: each one came straight from the range of the inverse function.

### u14 · simplify_cos_arctan
The triangle method really shines when the input is a variable instead of a number. Let us simplify the cosine of arctangent of x for any x. Set y equals arctangent of x, so the tangent of y equals x with y in the open interval from negative pi over two to pi over two. One route is the Pythagorean identity one plus tangent squared y equals secant squared y, which gives secant squared y equals one plus x squared; since y is in that interval, cosine is positive, so secant y equals the square root of the quantity one plus x squared and the cosine of y equals one over the square root of the quantity one plus x squared. The triangle says the same thing at a glance: opposite side x, adjacent side one, hypotenuse the square root of the quantity one plus x squared, and cosine is adjacent over hypotenuse. Either way, the cosine of arctangent of x equals one over the square root of the quantity one plus x squared — a messy composition collapsing to one clean expression in x, the kind of simplification you will reach for constantly once derivatives enter the picture.

### u15 · remaining_inverses
Three inverse trig functions remain — inverse cosecant, inverse secant, and inverse cotangent — and they are built in exactly the same spirit, just used less often. Each one inverts its trig function on a chosen branch. Inverse cosecant and inverse secant take inputs whose absolute value is at least one — that is, everything from negative infinity to negative one, together with one to infinity — because cosecant and secant never produce values strictly between negative one and one. Inverse cotangent, like inverse tangent, accepts every real number. Rather than memorize six separate boxes, it is cleaner to lay all six inverse functions side by side and compare what they accept and what interval of angles they return.

### u16 · branch_conventions
There is a subtlety hiding in those last three definitions: the branch we pick is a choice, not a law, and different texts choose differently. This text picks the branches that make the later differentiation formulas come out simplest, but you will meet other conventions in the wild — and the choice has visible consequences. Consider f of x equals arcsine of x plus arccosecant of x. Arcsine needs the absolute value of x to be at most one while arccosecant needs the absolute value of x to be at least one, so the only inputs satisfying both are x equals one and x equals negative one. At x equals one, both terms equal pi over two, so f of one equals pi. At x equals negative one, under this text's convention arccosecant of negative one equals three pi over two, and with arcsine of negative one equals negative pi over two we again get f of negative one equals pi — so f is the constant pi on its two-point domain. But under a different common convention, arccosecant of negative one would be negative pi over two, which makes f of negative one equals negative pi instead. Same expression, different answer — which is exactly why a text fixes its conventions explicitly, and why you should always check the one in front of you.

### u17 · recap
Here is the whole section in four moves. First, a trig function is not one-to-one, so we restrict it to a single branch and invert that — sine on the interval from negative pi over two to pi over two, cosine on the interval from zero to pi, tangent on the open interval between. Second, each inverse returns just one angle, the principal value inside its range — never the whole family of solutions. Third, the composition identities undo the functions, but arcsine of the sine of x and its cousins only give back x when x already sits in the restricted range. And fourth, to evaluate a composition, build a right triangle from the inverse trig value and read off the ratio you need — and let the range of the inverse fix every sign.

---

## 四、備忘

- 口語文字單一源＝ `content_scripts/ch01_inverse_trig.spoken.yml`；本檔與 `storyboards/ch01_inverse_trig_mimo.yml` 皆由 `derive_spoken.py` 生成。
- `{show}` beat 切分與正典 storyboard 對齊（`derive_spoken.py --check` 守門）。
- 計費：MiMo 公測限免但屬外部 API；批次合成前依 `CLAUDE.md` 報用量、徵同意。
