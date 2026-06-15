# §1.1 Inverse Functions — 旁白口語版（版本 B · MiMo-V2.5-TTS 客製）

> **此檔為生成檔（DO NOT EDIT）。** 由 `content_scripts/ch01_inverse_functions.spoken.yml`（口語單一源） 經 `pipeline/derive_spoken.py` 生成。要改旁白請改 `.spoken.yml` 後重生。
> **性質：版本 B（口語 TTS 版）。** 英文散文逐字忠於內容稿已認可 `narration`，**只把數學攤成口語**（無 LaTeX），供不能直讀 LaTeX 的 TTS（MiMo）照念。對照閱讀版（版本 A，數學渲染）＝ `ch01_inverse_functions_narration.html`。
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
| 區間 $[a,b]$ / $(a,b)$ | “the (open) interval from a to b” | |
| 座標點 $(a,b)$ | **“the point with coordinates a and b”** | 無視覺符號時最清楚。 |
| $\pi/2$、$\arcsin$… | “pi over two”、“arcsine of …” | 反三角直接念 arc-名。 |
| domain $A$ / range $B$ | “domain A / range B” | |

## 三、逐段口語稿

> 每段 `uNN · id` 即該單元 `assistant` 訊息內容（`{show}` 已移除）。intro/outro 無旁白，不列。

### u2 · can_we_go_backwards
Every function is a one-way machine: feed it an input, and it hands you an output. This section asks the reverse question -- starting from the output, can we recover the input that produced it? Watch two quick cases. For f of x equals x on the interval from zero to one, every input keeps its own value: zero stays at zero, one half stays at one half. But for f of x equals x squared on the interval from negative one to one, something breaks: both one half and negative one half are sent to one quarter. In the first case, each output points back to exactly one input; in the second, the output one quarter cannot tell us which input it came from -- and that difference is the whole story of this section.

> _per-unit 風格：_ 到 “something breaks” 給一絲好奇的輕揚，收尾句放緩、定下基調。

### u3 · one_to_one_definition
The property that separates the two cases has a name: one-to-one. A function f is one-to-one if f of x sub one is not equal to f of x sub two whenever x sub one is not equal to x sub two -- different inputs always produce different outputs. The same condition can be turned around: if f of x sub one equals f of x sub two, then x sub one equals x sub two. Both forms say the same thing, but the second one is the workhorse in computations: assume two outputs agree, and deduce that the inputs were equal all along.

### u4 · ids_before_algebra
Here is the definition at work in a setting with no formulas at all. Assign every student in a class an identification number, making sure no two students share one. Is the rule sending each student to their ID number one-to-one? Yes -- distinct students always receive distinct numbers, which is precisely the defining condition. The habit worth keeping: one-to-one is a question about the matching itself, not about algebra.

### u5 · checking_with_algebra
Now back to the two functions from the opening, this time as a formal check. On the interval from zero to one, the function f of x equals x sends every input to itself, so distinct inputs automatically give distinct outputs -- one-to-one. For g of x equals x squared on the interval from negative one to one, compute both values: g of one half equals one quarter, and g of negative one half equals one quarter as well. Two different inputs share one output, so g is not one-to-one. And the consequence matters: no rule can send one quarter back to a single input, so g cannot be reversed on this interval.

### u6 · horizontal_line_test
There is a way to read one-to-one straight off the graph. A horizontal line y equals c crosses the graph of f wherever f of x equals c, so every crossing is one input that produces the output c. That gives the test: a function is one-to-one exactly when no horizontal line meets its graph more than once. Two crossings on one line would mean two inputs with the same output -- exactly the failure we saw with x squared. So sweep horizontal lines down the graph and count: at most one crossing at every height is what passing looks like.

### u7 · inverse_definition
For a one-to-one function, every output traces back to exactly one input -- so the backwards assignment is itself a function. We call it the inverse of f, written f inverse. If f has domain A and range B, then f inverse has domain B and range A, and its rule is the defining relation: f inverse of y equals x exactly when f of x equals y. Note the trade: the outputs of f become the inputs of f inverse, and domain and range swap places.

### u8 · reading_the_notation
One notational habit before we continue. We usually prefer x as the input letter of whatever function we are currently studying -- including f inverse itself. After renaming the variables, the defining relation reads: f inverse of x equals y exactly when f of y equals x. Same statement, new letters -- and this renaming is the reason the procedure at the end of this section will ask us to interchange x and y.

### u9 · inverse_iff_one_to_one
We introduced one-to-one as the property that makes reversing possible; the theorem pins that down. A function has an inverse if and only if it is one-to-one. There are no hidden conditions: the property we can already check -- by the definition or by horizontal lines -- is the complete story of invertibility. Let us walk through why both directions hold.

### u10 · proof_both_directions
First, suppose f has an inverse. If f of x sub one equals f of x sub two, apply f inverse to both sides -- f inverse of f of x sub one equals f inverse of f of x sub two -- and by the defining relation each side collapses back to its input, so x sub one equals x sub two. Equal outputs force equal inputs: f is one-to-one. Now the converse. Let f be one-to-one with domain A and range B. Every y in B is hit by at least one x in A -- that is what being the range means -- and one-to-one guarantees at most one. Exactly one input for each output: sending each y to that unique x is a well-defined function from B to A, and it is precisely the inverse of f.

### u11 · first_inverses
Time to find actual inverses, starting small. The identity function f of x equals x leaves every input untouched, so reversing it changes nothing either: f is its own inverse, f inverse of x equals x. Next, g of x equals x cubed. Write y equals x cubed and solve for the input: x equals the cube root of y, so after renaming the variable, g inverse of x equals the cube root of x. And the answer checks out: g of g inverse of x equals the cube root of x, all cubed, which is x -- feeding the inverse's output back into g returns exactly where we started.

> _per-unit 風格：_ “starting small” 帶一點鼓勵、輕快；驗證句給確認感。

### u12 · composition_identities
That final check was not a coincidence -- it is a law that every inverse obeys. Because f inverse of y equals x means exactly the same thing as f of x equals y, going forward and then backwards always lands you where you started: f inverse of f of x equals x for every x in A, and in the other direction, f of f inverse of y equals y for every y in B. In words: f and f inverse undo each other, in both orders. These two identities are also the practical test -- to certify that a claimed inverse is correct, compose the two and watch everything cancel.

### u13 · graphs_mirror_across_y_x
The algebra of inverses leaves a picture behind. If the point with coordinates a and b lies on the graph of f, then f of a equals b, which is the same as f inverse of b equals a -- so the point with coordinates b and a lies on the graph of f inverse. Swapping the two coordinates of a point is exactly a reflection across the line y equals x. So the two graphs are mirror images: take g of x equals x cubed and its inverse, the cube root of x, fold the plane along the line y equals x, and each curve lands precisely on the other.

### u14 · repair_by_restricting
Remember x squared -- the very first function that failed us, because one half and negative one half both land on one quarter. We can repair it. Restrict the domain to the interval from zero to infinity, keeping only the non-negative inputs, and the collision is gone: if x sub one squared equals x sub two squared, with x sub one and x sub two both greater than or equal to zero, then x sub one equals x sub two. The restricted function is one-to-one, so now it has an inverse. Solving x equals f inverse of x, all squared, and keeping the non-negative root gives f inverse of x equals the square root of x -- which is exactly why the square-root symbol means the positive root: it is defined to undo the restricted squaring function. And the move we just made -- restrict first, then invert -- is exactly what makes the inverse trigonometric functions possible, since sine and cosine are not one-to-one on their own either.

> _per-unit 風格：_ 開頭回收開場反例，用會心、略帶默契的語氣；“positive” 一字輕微加重。

### u15 · the_procedure
The cube-root computations secretly followed a recipe, and it works for any one-to-one function. Step one: write y equals f of x. Step two: solve this equation for x in terms of y. Step three: interchange the names x and y -- the result reads y equals f inverse of x. All the real work lives in step two; the final swap is just the variable-naming habit we set up earlier.

### u16 · procedure_in_action
Same recipe, one notch up: f of x equals x cubed plus two. From y equals x cubed plus two, isolate the input -- x cubed equals y minus two, then x equals the cube root of the quantity y minus two. Interchange the names, and the inverse appears: f inverse of x equals the cube root of the quantity x minus two. Finally the certificate: f of f inverse of x equals the cube root of the quantity x minus two, all cubed, plus two; that is x minus two, plus two, which is x. Everything cancels back to x, so this really is the inverse.

### u17 · temperature_conversion
One last inverse, and this one means something outside the page. The function f of t equals nine-fifths t plus thirty-two takes a Celsius temperature and returns the Fahrenheit reading. So what does its inverse do? It runs the conversion backwards -- hand it a Fahrenheit number and it gives you the Celsius. The recipe is unchanged: solve t equals nine-fifths times f inverse of t, plus thirty-two, for the inverse, which gives f inverse of t equals five-ninths times the quantity t minus thirty-two. And the check is reassuring -- go to Fahrenheit and back, f inverse of f of t equals five-ninths times the quantity nine-fifths t plus thirty-two minus thirty-two, which is t, landing exactly where we began. Here an inverse is not an abstraction; it is the formula on the other side of the thermometer.

### u18 · recap
Here is the whole section in four moves. A function is one-to-one when different inputs never share an output -- and on a graph, horizontal lines detect exactly that. A function has an inverse precisely when it is one-to-one, with domain and range trading places. The inverse undoes the original -- f inverse of f of x equals x and f of f inverse of y equals y -- and graphically the two curves mirror across the line y equals x. And to compute one: write y equals f of x, solve for x, then swap the names.

> _per-unit 風格：_ 整段放緩半拍、收束感；四個 take-away 之間各留一個明顯停頓。

---

## 四、備忘

- 口語文字單一源＝ `content_scripts/ch01_inverse_functions.spoken.yml`；本檔與 `storyboards/ch01_inverse_functions_mimo.yml` 皆由 `derive_spoken.py` 生成。
- `{show}` beat 切分與正典 storyboard 對齊（`derive_spoken.py --check` 守門）。
- 計費：MiMo 公測限免但屬外部 API；批次合成前依 `CLAUDE.md` 報用量、徵同意。
