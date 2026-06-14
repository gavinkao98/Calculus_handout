# §1.3 The Limit of a Function — 旁白口語版（版本 B · MiMo-V2.5-TTS 客製）

> **此檔為生成檔（DO NOT EDIT）。** 由 `content_scripts/ch01_limit_of_function.spoken.yml`（口語單一源） 經 `pipeline/derive_spoken.py` 生成。要改旁白請改 `.spoken.yml` 後重生。
> **性質：版本 B（口語 TTS 版）。** 英文散文逐字忠於內容稿已認可 `narration`，**只把數學攤成口語**（無 LaTeX），供不能直讀 LaTeX 的 TTS（MiMo）照念。對照閱讀版（版本 A，數學渲染）＝ `ch01_limit_of_function_narration.html`。
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

### u2 · ratio_of_changes
Calculus keeps circling back to one question: how fast is something changing right now? Suppose s of t is the position of a moving object at time t. Over the stretch from t to t plus h, its average velocity is the ratio s of the quantity t plus h, minus s of t, all over h -- change in position divided by change in time. But the average speed across an interval is not the speed at a single instant. To pin down that instantaneous velocity, we let h shrink toward zero and watch what the ratio settles on. The same move works for any function: the ratio f of y minus f of x, all over the quantity y minus x, measures how f changes between two inputs, and we ask what it approaches as y slides toward x without ever reaching it. That question -- what a quantity approaches -- is the idea of a limit.

### u3 · the_limit_defined
Here is the definition that captures "what a function approaches." We say the limit of f of x as x approaches a equals L if f of x can be made arbitrarily close to L whenever x is sufficiently close to a but not equal to a. That last clause is the entire personality of a limit: we care about inputs near a, never about a itself. The same idea has a lighter notation: f of x tends to L as x tends to a. Keep the picture in mind: x creeping toward a along the horizontal axis, while the heights f of x home in on L.

### u4 · limit_vs_value
Now the subtle part, and it is the heart of this section. A limit looks only at the neighborhood of a, never at the single point a itself -- so the value f of a gets no vote. Look at three functions side by side, all approaching the same height L as x approaches a. In the first, the point sits right where you expect, with f of a equals L. In the second, someone has lifted that one point off the curve, so f of a is not equal to L. In the third, the point is missing entirely and f of a is undefined. Three different situations at a, yet the limit is the same L in every case -- because near a, and near is all that counts, the three curves are identical.

### u5 · reading_a_graph
Let us read limits straight off a graph. Three inputs to inspect: x equals negative two, x equals zero, and x equals two. As x approaches negative two from either side, the curve rises toward height one, so the limit there is one. Approaching zero, the curve heads to height zero -- the limit is zero. Now x equals two is the interesting one: from both sides the curve climbs toward height two, and yet the graph marks a solid dot down at the point with coordinates two and negative two, and a hollow dot up at the point with coordinates two and two. So f of two is negative two, but the limit ignores the value at the point and reports where the curve was heading. The limit as x approaches two is two, even though f of two equals negative two.

### u6 · build_one_yourself
The same idea, now run backwards: instead of reading a graph, we build one. The task is a function with limit ten as x approaches three, but with f of three equals zero. Start with any curve that approaches height ten at x equals three -- a straight line through the point with coordinates three and ten will do. Then take that single point and drag it down to height zero: a hollow dot at the point with coordinates three and ten to mark where the curve is heading, and a solid dot at the point with coordinates three and zero for the actual value. Near x equals three the curve still approaches ten, while the relocated point sets f of three equals zero. Because the limit and the value are independent, nothing stops us from choosing them separately.

### u7 · estimate_from_a_table
What if there is no graph to read? Then we make our own data. Take the limit, as x approaches one, of the quantity x minus one, all over the quantity x squared minus one. Substituting x equals one gives zero over zero -- undefined, no answer there. So instead we sample inputs creeping toward one from both sides: 0.9, 0.99, 0.999, and then 1.001, 1.01, 1.1. Evaluate the expression at each, and the outputs march steadily toward one number -- 0.5263, 0.5025, 0.5003 from the left, and 0.4762, 0.4975, 0.4998 closing in from the right. They are squeezing in on one half, so we read the limit as one half.

### u8 · when_algebra_is_hard
One more, where the table really earns its keep. Consider the limit as t approaches zero of the square root of the quantity t squared plus nine, minus three, all over t squared. This time you cannot just factor your way to the answer -- the square root hides what is going on, and at t equals zero it is once again zero over zero. So we let the numbers talk. Sampling t equals negative 0.1, negative 0.01, 0.01, and 0.1, the expression returns about 0.16662, then 0.166666, and back out symmetrically. That is closing in on 0.16666 and so on, which we recognize as one sixth. When the algebra is not obvious, a table of nearby values is a perfectly good way to see where a function is headed.

### u9 · what_comes_next
Notice what we have been doing: guessing limits by peeking at nearby values, whether off a graph or out of a table. Guessing is a fine start, but it is not a proof, and tables can occasionally mislead. So next we build systematic methods -- rules that compute limits exactly, with no sampling at all. And we sharpen the idea itself: what happens when a function approaches different values from the left and from the right, or grows without bound near a point. The estimate you can make today becomes a calculation you can trust.

### u10 · recap
Here is the whole section in four ideas. A limit asks what value f of x approaches as x heads toward a -- written the limit of f of x as x approaches a equals L. It depends only on the behavior near a, never on f of a itself, which may not even be defined. You can read a limit off a graph by following the curve inward from both sides. And when there is no graph, a table of values at inputs creeping toward a will reveal the number the function is approaching.

---

## 四、備忘

- 口語文字單一源＝ `content_scripts/ch01_limit_of_function.spoken.yml`；本檔與 `storyboards/ch01_limit_of_function_mimo.yml` 皆由 `derive_spoken.py` 生成。
- `{show}` beat 切分與正典 storyboard 對齊（`derive_spoken.py --check` 守門）。
- 計費：MiMo 公測限免但屬外部 API；批次合成前依 `CLAUDE.md` 報用量、徵同意。
