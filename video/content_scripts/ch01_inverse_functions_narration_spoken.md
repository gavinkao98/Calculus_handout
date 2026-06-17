# §1.1 Inverse Functions — 旁白口語版（版本 B · MiMo-V2.5-TTS 客製）

> **此檔為生成檔（DO NOT EDIT）。** 由 `content_scripts/ch01_inverse_functions.spoken.yml`（口語單一源） 經 `pipeline/derive_spoken.py` 生成。要改旁白請改 `.spoken.yml` 後重生。
> **性質：版本 B（口語 TTS 版）。** 英文散文逐字忠於內容稿 `narration`，**只把數學攤成口語**（無 LaTeX），供不能直讀 LaTeX 的 TTS（MiMo）照念。對照閱讀版（版本 A，數學渲染）＝ `ch01_inverse_functions_narration.html`。
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

### u2 · can_we_run_it_backwards
We know how to run a function forwards — feed it an input, read off the output. The real question of this section is whether we can run it backwards, recovering the input from the output. Sometimes we can, sometimes we can't, and two quick examples show the difference. Take f of x equals x on the interval from zero to one: zero goes to zero, a half goes to a half, an eighth goes to an eighth — every output traces back to exactly one input, so going backwards is unambiguous. Now take f of x equals x squared on the interval from negative one to one: a half squares to a quarter, but so does negative a half, so the output a quarter came from two different inputs. That collision is the whole obstacle — when one output can be traced to two inputs, there is no honest way back, and pinning down exactly when that never happens is where we begin.

### u3 · one_to_one_definition
A function can be run backwards only when each output comes from exactly one input, and that property has a name: one-to-one. Formally, that means different inputs always give different outputs — f of x sub one is not equal to f of x sub two whenever x sub one is not equal to x sub two. There is an equivalent form that turns out to be the one you actually use in a proof: if f of x sub one equals f of x sub two, then x sub one equals x sub two. The two say the same thing from opposite sides — the first forbids a collision outright, the second says that if a collision did happen, the two inputs must have been equal all along. When you need to prove a function is one-to-one, reach for that second form.

### u4 · student_id_is_one_to_one
Let us start with a one-to-one function that needs no algebra at all. Picture a class where every student is assigned an identification number, set up so that no two students ever share a number. Let f send each student to their identification number — is it one-to-one? It is: by construction, two different students always end up with two different numbers, so distinct inputs give distinct outputs. That is the definition in plain words, before a single equation — no two inputs are allowed to collide.

### u5 · testing_x_and_x_squared
We met these two at the very start; now let us run them through the definition. On zero to one, f of x equals x sends every input to itself, so different inputs always land on different outputs — f is one-to-one. But g of x equals x squared on negative one to one fails, and we can pin it down cleanly: g of a half is a quarter, and g of negative a half is also a quarter. Two different inputs, one shared output — exactly the collision the definition rules out. So g is not one-to-one on this interval — which is exactly why it needs careful handling later.

### u6 · shape_can_mislead
Here is a case where the formula can fool you. Compare h of x equals x cubed minus four x with k of x equals x cubed plus four on the whole real line — both look like cousins of x cubed. But factor the first: h of x equals x times the quantity x minus two, times the quantity x plus two, so h of zero and h of two are both zero even though zero and two are different inputs; h is not one-to-one. The second behaves oppositely: if k of x sub one equals k of x sub two, then x sub one cubed equals x sub two cubed, and taking cube roots forces x sub one equals x sub two, so k is one-to-one. Same general shape, opposite verdicts — when the graph is not in front of you, test the definition directly.

### u7 · horizontal_line_test
When you do have the graph, there is a one-glance test. A horizontal line y equals c meets the graph of f wherever f of x equals c, so a single output value showing up twice is the same as that line crossing the graph twice. That gives the rule: a function is one-to-one exactly when no horizontal line crosses its graph more than once. A straight line like y equals x passes — every horizontal line meets it just once. A parabola fails — a horizontal line slices clean through both arms, and those two crossings are exactly the pair of inputs sharing an output we found with algebra. One-to-one, in a single glance: no horizontal line gets to cross twice.

### u8 · inverse_function_definition
Once a function is one-to-one, we can build a second function that undoes it. The idea is simply to read the same correspondence backwards. Where f asks "given the input, what is the output?", the inverse asks "given that output, which input produced it?" So the outputs of f become the inputs of the inverse, and the domain and range trade places. We write the inverse as f inverse, and define it like this: f inverse of y equals x exactly when f of x equals y. One warning about the notation: that negative one means inverse function, not a reciprocal. f inverse of x is the inverse evaluated at x, which is a completely different thing from one over f of x — and the same caution will matter for sine inverse shortly.

### u9 · inverse_iff_one_to_one
This ties the two halves of the section into one clean statement: a function has an inverse if and only if it is one-to-one. One direction is quick. Suppose f already has an inverse and f of x sub one equals f of x sub two; apply f inverse to both sides — the left collapses to x sub one, the right to x sub two, so x sub one equals x sub two, and f was one-to-one all along. The other direction builds the inverse: if f is one-to-one, then every output y in the range comes from exactly one input x, and sending each y back to its unique x is precisely the inverse function. So "one-to-one" and "invertible" are just two names for the same thing.

### u10 · first_inverses
Let us compute a couple of inverses. Start with f of x equals x — it leaves every input untouched, so undoing it does nothing either; f is its own inverse, f inverse of x equals x. Now g of x equals x cubed: set y equals x cubed, solve to get x equals the cube root of y, then rename the variables to land on g inverse of x equals the cube root of x. And we can check it — g of its inverse is the cube root of x, all cubed, which is just x again. Solve for the input, swap the names; that is the move, and we are about to make it routine.

> _per-unit 風格：_ “starting small” 帶一點鼓勵、輕快；驗證句給確認感。

### u11 · composition_identities
Undoing and then redoing should leave you exactly where you started — worth stating outright. For a one-to-one f, applying f and then f inverse returns the original input: f inverse of f of x equals x for every x in the domain. Going the other way works too: f of f inverse of y equals y for every y in the range. Picture an input x in the set A; f carries it across to its output in the set B, and f inverse carries that output right back to the same x — a round trip that lands home. Each function is the other's exact undo, in both directions.

### u12 · reflection_across_y_equals_x
There is a clean picture of what taking an inverse does to a graph. If you draw f and its inverse in the same plane, the two graphs are mirror images across the line y equals x. The reason is the same swap: a point with coordinates a and b sits on the graph of f exactly when the point with coordinates b and a sits on the graph of the inverse, and reflecting across y equals x is precisely what trades a point's two coordinates. You can watch it on the cube and the cube root from a moment ago — fold the graph of x cubed over the line y equals x and it lands right on the graph of the cube root. Inverse, geometrically: reflect across y equals x.

### u13 · repair_by_restricting
What about a function that fails the one-to-one test — is it hopeless? Not necessarily. Take f of x equals x squared, which we already know is not one-to-one on the whole line. But chop its domain down to the nonnegative numbers, from zero onwards, and it becomes one-to-one: if two nonnegative inputs square to the same value, they were equal to begin with. Now we can invert it — solving gives f inverse of x equals the square root of x, and because the inputs were nonnegative we take the positive root. That is why the square root symbol means the positive root: it is the convention that makes square root the genuine inverse of squaring. Restrict first, then invert — and that exact move is the key that unlocks the inverse trigonometric functions coming up.

> _per-unit 風格：_ 開頭回收開場反例，用會心、略帶默契的語氣；“positive” 一字輕微加重。

### u14 · finding_the_inverse_strategy
We have inverted a few functions by hand; let us package the moves into a procedure. Step one: write y equals f of x. Step two: solve that equation for x in terms of y. Step three: interchange the names x and y — the result reads y equals f inverse of x. That last swap is just the habit of using x for the inverse's own input. One guardrail, though: this only works if f is already one-to-one. Apply it blindly to y equals x squared and step two hands you x equals plus or minus the square root of y — two values, not a function. So always check one-to-one first, or restrict the domain the way we just did.

### u15 · inverse_of_a_cubic
Now run the procedure on a fresh function: f of x equals x cubed plus two. Write y equals x cubed plus two. Solve for x — subtract to get x cubed equals y minus two, then take the cube root, x equals the cube root of the quantity y minus two. Interchange the names and you have f inverse of x equals the cube root of the quantity x minus two. Check it by composing: f of the inverse is the cube root of the quantity x minus two, all cubed, plus two — the cube and cube root cancel, leaving x minus two plus two, which is x. Three steps, one check, done.

### u16 · inverse_of_a_rational
Same three steps, but now the algebra is a touch more delicate — a rational function, f of x equals three over the quantity x minus five. Set y equals three over the quantity x minus five. Solving, x minus five equals three over y, so x equals five plus three over y; interchanging gives f inverse of x equals five plus three over x, which we can also write as five x plus three, all over x. This time let us verify both directions: f of the inverse and the inverse of f each come back to x, exactly the composition identities at work. And notice the domains pair up: f cannot take x equals five, the inverse cannot take x equals zero, mirroring the fact that f never outputs zero and the inverse never outputs five.

### u17 · inverse_in_an_application
One more, where the inverse answers a real question. The function f of t equals nine-fifths t plus thirty-two turns a Celsius temperature into Fahrenheit. So what does its inverse do? It runs the conversion in reverse — Fahrenheit back to Celsius. Solving t equals nine-fifths f inverse of t plus thirty-two for the inverse gives f inverse of t equals five-ninths times the quantity t minus thirty-two. For the check, feed a Celsius reading through f and then through the inverse: the thirty-twos cancel, the nine-fifths and five-ninths undo each other, and you get t back. An inverse is not just algebra — it is the same relationship read in the direction you happen to need.

### u18 · recap
Let us gather what we have built. A function is one-to-one when distinct inputs give distinct outputs — and you can spot it at a glance with the horizontal line test, where no line is allowed to cross twice. A function is invertible exactly when it is one-to-one, and its inverse swaps inputs with outputs, so its graph is the mirror image across y equals x. To find an inverse you solve y equals f of x for x and swap the names — after checking one-to-one, or restricting the domain to get there. And keep the notation straight: f inverse undoes f; it is not one over f. One-to-one, invertible, reflected across y equals x — that is the whole arc of the section.

> _per-unit 風格：_ 整段放緩半拍、收束感；四個 take-away 之間各留一個明顯停頓。

---

## 四、備忘

- 口語文字單一源＝ `content_scripts/ch01_inverse_functions.spoken.yml`；本檔與 `storyboards/ch01_inverse_functions_mimo.yml` 皆由 `derive_spoken.py` 生成。
- `{show}` beat 切分與正典 storyboard 對齊（`derive_spoken.py --check` 守門）。
- 計費：MiMo 公測限免但屬外部 API；批次合成前依 `CLAUDE.md` 報用量、徵同意。
