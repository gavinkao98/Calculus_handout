# §1.6 The Precise Definition of a Limit — 旁白口語版（版本 B · MiMo-V2.5-TTS 客製）

> **此檔為生成檔（DO NOT EDIT）。** 由 `content_scripts/ch01_precise_limit.spoken.yml`（口語單一源） 經 `pipeline/derive_spoken.py` 生成。要改旁白請改 `.spoken.yml` 後重生。
> **性質：版本 B（口語 TTS 版）。** 英文散文逐字忠於內容稿已認可 `narration`，**只把數學攤成口語**（無 LaTeX），供不能直讀 LaTeX 的 TTS（MiMo）照念。對照閱讀版（版本 A，數學渲染）＝ `ch01_precise_limit_narration.html`。
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

### u2 · why_close_is_not_enough
For two centuries calculus solved real problems -- orbits, areas, the motion of the planets -- while its logical foundations stayed shaky. The arguments leaned on infinitesimals, quantities imagined as vanishingly small but never pinned down, and on vague phrases like "x is close to a" and "f of x is close to L." But how close is close? The nineteenth century answered by throwing the word "close" out entirely and replacing it with a measurable distance. That single move is the whole project of this section: make "close" precise enough to compute with.

### u3 · the_broken_function
Here is a deliberately broken function to sharpen the question. Let f of x equal two x minus one everywhere except at x equals three, where we force the value to be six. As x moves close to three, the output two x minus one moves close to five -- so we expect the limit to be five, even though the function's actual value there is six. The limit watches how f behaves on the approach, not where it lands at the point itself. But "close to five" is the very phrase we promised to make precise, so let us ask the sharp question: how close can we force f of x to be?

### u4 · tolerance_game_point_one
Let us play it as a game with a number attached. Suppose someone demands that f of x land within zero point one of five -- can we deliver? Measure the gap: the absolute value of f of x minus five equals the absolute value of the quantity two x minus one, minus five, which is the absolute value of two x minus six, which is two times the absolute value of x minus three. So the demand that two times the absolute value of x minus three is less than zero point one is just the absolute value of x minus three is less than zero point zero five. Keep x within zero point zero five of three, and f of x is guaranteed within zero point one of five -- a precise promise, answered with a precise radius.

### u5 · every_tolerance_at_once
One answered demand is not enough, though. Tighten the tolerance to zero point zero one and the very same algebra returns the absolute value of x minus three is less than zero point zero zero five; halve the tolerance and the radius halves with it. The pattern is mechanical: for any tolerance epsilon greater than zero, we get the absolute value of f of x minus five is less than epsilon whenever the absolute value of x minus three is less than epsilon over two, so the choice delta equals epsilon over two always works. This is what "arbitrarily close" really means -- not close for one lucky tolerance, but answerable for every epsilon greater than zero. That little phrase "for every epsilon" is the engine of the definition we are about to write down.

### u6 · precise_limit_definition
Now we can state it cleanly. Let f be defined on an open interval around a, except possibly at a itself. We say the limit of f of x as x approaches a equals L if for every epsilon greater than zero there exists a delta greater than zero such that the absolute value of f of x minus L is less than epsilon whenever zero is less than the absolute value of x minus a, which is less than delta. Read it as a challenge and a response: you name any tolerance epsilon, however cruelly small, and I must produce a radius delta that keeps every nearby f of x inside it. If I can always answer, the limit is L.

### u7 · epsilon_delta_tube
The definition hides a clean picture. Mark the target on the vertical axis: a horizontal band from L minus epsilon to L plus epsilon, the strip we want the outputs to land in. Mark the inputs on the horizontal axis: a vertical band from a minus delta to a plus delta, with the single point a punched out. The definition says exactly this -- as long as x stays in the input band, the graph carries it into the target band. And here is the part to feel in your bones: shrink the target strip toward L, and the input interval must shrink too, or the curve escapes the band. The radius delta is not fixed; it answers to epsilon.

### u8 · uniqueness_statement_and_trap
The definition earns its keep immediately: it guarantees that a limit, once it exists, is unique. Why even worry? Because nothing so far forbids two different numbers L and M from both passing the test -- so suppose, for contradiction, that they do. Here is the clever move that breaks it: let epsilon be half the gap between them, epsilon equals the absolute value of L minus M, over two. Since L is not equal to M, this epsilon is strictly positive, so it is a perfectly legal tolerance we are allowed to feed the definition. We have set a trap; the next step springs it.

### u9 · uniqueness_proof_triangle
Now spring it. Feed that epsilon to each limit: there is a delta sub one that makes f of x hug L, and a delta sub two that makes it hug M. Take any x nearer to a than both -- closer than the smaller of delta sub one and delta sub two -- and both promises hold at once. Now watch the gap collapse: the absolute value of L minus M rewrites as the absolute value of the quantity L minus f of x plus f of x minus M, which by the triangle inequality is at most the absolute value of L minus f of x, plus the absolute value of f of x minus M, and since each piece is below epsilon, the total is below two epsilon. But two epsilon was defined to be exactly the absolute value of L minus M. We have forced the absolute value of L minus M to be strictly less than itself -- impossible. The only way out is that there was no gap at all: L equals M.

### u10 · epsilon_delta_recipe
Every verification that follows runs on one recipe. Start from a generic epsilon greater than zero -- that is the challenge, and your job is to manufacture a delta. Take the quantity, the absolute value of f of x minus L, and bound it above by something times the absolute value of x minus a, because the absolute value of x minus a is the thing delta controls. Then choose delta to drive that bound below epsilon. One wrinkle decides the difficulty: if the bound still carries a stray factor depending on x, first pen x into a small interval around a to cap that factor, then take delta to be the minimum of that interval's radius and your epsilon-based bound. The next two examples are exactly this recipe -- once without the wrinkle, once with it.

### u11 · verify_linear_limit
Take the clean case first: show the limit of four x minus five as x approaches three equals seven. Given a tolerance epsilon, measure the gap: the absolute value of the quantity four x minus five, minus seven is the absolute value of four x minus twelve, which factors as four times the absolute value of x minus three. We want that under epsilon, so we demand the absolute value of x minus three is less than epsilon over four. That hands us the choice delta equals epsilon over four: whenever zero is less than the absolute value of x minus three, which is less than delta, the gap four times the absolute value of x minus three is below four times epsilon over four, exactly epsilon. The function is linear, there is no stray factor, and delta falls straight out of the algebra.

### u12 · verify_quadratic_limit
Same goal, but now the algebra fights back: show the limit of x squared minus five x plus six as x approaches one equals two. The gap is the absolute value of x squared minus five x plus four, which factors as the absolute value of x minus one, times the absolute value of x minus four. The first factor is what delta controls, but the second drifts as x moves -- so cap it: insist first that the absolute value of x minus one is less than one, which traps x between zero and two and forces the absolute value of x minus four to be less than four. Now the gap is below four times the absolute value of x minus one, and to push that under epsilon we also need the absolute value of x minus one to be less than epsilon over four. So take delta equals the minimum of one and epsilon over four, and both demands hold together. The minimum is not a trick; it is the recipe's wrinkle, made concrete.

### u13 · precise_infinite_limit
The same machine handles limits that run off to infinity. We met those informally a little earlier; now we can say them precisely. We write the limit of f of x as x approaches a equals infinity to mean: for every threshold M greater than zero, there is a delta greater than zero such that f of x is greater than M whenever zero is less than the absolute value of x minus a, which is less than delta. Notice the quantifier has only changed its target -- instead of trapping f near a value, we force it above any height you name. Pick M as large as you like, a hundred or a googol; once x is close enough to a, the function clears it. The negative infinity case is the mirror image: for every negative N, eventually f of x drops below it.

### u14 · continuity_preview
Before we gather up, the precise definition quietly hands us one more idea. Suppose f is defined not just near a but at a as well, and suppose the limit equals the actual value: the limit of f of x as x approaches a equals f of a. When that happens, we say f is continuous at a. Look back at our broken function -- its limit was five but its value was six, so it failed exactly this test; continuity is the case where the approach and the destination finally agree. A full study of continuity comes later; we name it here only because the limit language expresses it so directly.

### u15 · recap
Let us gather the thread. The vague word "close" became a precise contract: for every epsilon greater than zero there is a delta greater than zero so that, whenever zero is less than the absolute value of x minus a, which is less than delta, the output obeys the absolute value of f of x minus L is less than epsilon. The picture to keep is the strip and the interval -- inputs within delta of a are carried into the band within epsilon of L, and delta always answers to epsilon. The first payoff was uniqueness: a limit, once it exists, cannot be two numbers. And to verify a limit by hand, bound the absolute value of f of x minus L by a multiple of the absolute value of x minus a, choose delta, and take a minimum when a stray factor needs taming. Every informal limit we computed in the earlier sections now stands on this one definition.

---

## 四、備忘

- 口語文字單一源＝ `content_scripts/ch01_precise_limit.spoken.yml`；本檔與 `storyboards/ch01_precise_limit_mimo.yml` 皆由 `derive_spoken.py` 生成。
- `{show}` beat 切分與正典 storyboard 對齊（`derive_spoken.py --check` 守門）。
- 計費：MiMo 公測限免但屬外部 API；批次合成前依 `CLAUDE.md` 報用量、徵同意。
