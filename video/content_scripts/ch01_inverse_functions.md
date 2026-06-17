# §1.1 Inverse Functions — 影片內容稿（content script）

> **產線：** 講義 → 影片，gen-2（2026-06-16 大重設後從 HTML 講義逐節重跑）。
> **權威來源：** [`../../handout/chapter1-print-standalone.html`](../../handout/chapter1-print-standalone.html) §1.1（編輯源 `handout/fragments/ch01/sec-1-1.html`）。
> **這是什麼：** 純內容中間產物（source of truth）。格式見 [`../CONTENT_METHODOLOGY.md`](../CONTENT_METHODOLOGY.md) §6——只含 `id`／`source`／`learning_goal`／`kind`／`narration`／`visual_need`／`animation_cue`，**不含**任何工程欄位（template／`{show}`／accent／payload）。工程是第二階段的事。
> **階段：** **LOCKED**（2026-06-17 使用者認可旁白；六鏡收斂＋潤稿 gate1/gate2 收尾）。鎖稿後忠實性以 NFA（鎖稿後、不改措辭）把關；任何 post-lock 改稿須跑 scoped NFA 回歸（CONTENT_METHODOLOGY §8）。narration 認可在編譯出的 `_narration.html` 上進行；本 `.md` 為權威，兩者 MUST 一致。

---

## meta（intro/outro 定位資訊）

- `id`: ch01_inverse_functions
- `section`: 1.1
- `title`: Inverse Functions
- `chapter`: Chapter 1
- `chapter_title`: Inverse Functions and Limits
- `tagline`（intro 引導問題）: When can a function be run backwards?
- 章內節次（intro 章節地圖用）：
  - 1.1 Inverse Functions ← 本節
  - 1.2 Inverse Trigonometric Functions
  - 1.3 The Limit of a Function
  - 1.4 One-Sided and Infinite Limits
  - 1.5 Limit Laws and Computational Techniques
  - 1.6 The Precise Definition of a Limit

> intro 與 outro 為純動畫、**無 narration**（gen-2 first-class）。Key Takeaways 在 `recap` 教學單元（有旁白），不在 outro。

---

## 教學單元（依教學自由重排；忠實仍可逐單元回溯講義）

---

### unit: intro

```
id: intro
source: chapter1-print-standalone.html §1.1（Section Gate；定位資訊見上方 meta）
learning_goal: 知道本節在章內的位置，並帶著「函數能不能倒著跑」這個問題進入。
kind: motivation
narration: （無——intro 為純動畫）
visual_need: Section Gate——章節地圖 → 聚焦 1.1 → logo／節號／標題／tagline 字卡 → 暗場交接。
animation_cue: （由 intro 模板處理，內容稿不指定）
```

---

### unit: can_we_run_it_backwards

```
id: can_we_run_it_backwards
source: chapter1-print-standalone.html §1.1 · 開節散文（"the reverse process … recovering the input from the output"）+ warmup ol（f(x)=x、f(x)=x^2）+ 其後「the difference … is the central point」散文
learning_goal: 看出「把函數倒著跑」要成立，靠的是每個輸出只來自一個輸入；輸出撞在一起就壞了。
kind: motivation
narration: |
  We know how to run a function forwards — feed it an input, read off the
  output. The real question of this section is whether we can run it
  backwards, recovering the input from the output. Sometimes we can,
  sometimes we can't, and two quick examples show the difference. Take
  $f(x)=x$ on the interval from $0$ to $1$: zero goes to zero, a half goes
  to a half, an eighth goes to an eighth — every output traces back to
  exactly one input, so going backwards is unambiguous. Now take
  $f(x)=x^2$ on the interval from $-1$ to $1$: a half squares to a quarter,
  but so does negative a half, so the output a quarter came from two
  different inputs. That collision is the whole obstacle — when one output
  can be traced to two inputs, there is no honest way back, and pinning
  down exactly when that never happens is where we begin.
visual_need: |
  兩個小映射示意：左 f(x)=x 每個輸入箭頭落到自己獨有的輸出；
  右 f(x)=x^2 把 1/2 與 -1/2 兩個輸入都射到同一個輸出 1/4。
animation_cue: |
  建議動畫：左右兩欄點（左＝輸入、右＝輸出）。先演 f(x)=x —— 幾個輸入
  各自一條箭頭落到不同輸出，乾淨的一對一。再演 f(x)=x^2 —— 從 1/2 與
  -1/2 各拉一條箭頭，兩條同時匯聚到同一個輸出 1/4 上（匯流處閃紅），
  凸顯「兩個輸入 → 一個輸出」正是倒著跑會壞掉的地方。
```

---

### unit: one_to_one_definition

```
id: one_to_one_definition
source: chapter1-print-standalone.html §1.1 · "One-to-one functions" 小節散文（"A function can be reversed only when each output comes from exactly one input"）+ Definition 1.1
learning_goal: 認得讓函數可逆的形式條件——one-to-one——以及它在證明裡實際在用的等價形式。
kind: definition
narration: |
  A function can be run backwards only when each output comes from exactly
  one input, and that property has a name: one-to-one. Formally, that means
  different inputs always give different outputs — $f(x_1)\ne f(x_2)$
  whenever $x_1\ne x_2$. There is an
  equivalent form that turns out to be the one you actually use in a proof:
  if $f(x_1)=f(x_2)$, then $x_1=x_2$. The two say the same thing from
  opposite sides — the first forbids a collision outright, the second says
  that if a collision did happen, the two inputs must have been equal all
  along. When you need to prove a function is one-to-one, reach for that
  second form.
visual_need: |
  一句白話定義（different inputs → different outputs）＋兩條等價數學式：
  $f(x_1)\ne f(x_2)$ whenever $x_1\ne x_2$；$f(x_1)=f(x_2)\implies x_1=x_2$。
animation_cue: （無——靜態即可）
```

---

### unit: student_id_is_one_to_one

```
id: student_id_is_one_to_one
source: chapter1-print-standalone.html §1.1 · Example 1.1（student identification numbers）
learning_goal: 用一個不需代數的真實例子，把 one-to-one 的定義扣在具體個案上。
kind: example
narration: |
  Let us start with a one-to-one function that needs no algebra at all.
  Picture a class where every student is assigned an identification number,
  set up so that no two students ever share a number. Let $f$ send each
  student to their identification number — is it one-to-one? It is: by
  construction, two different students always end up with two different
  numbers, so distinct inputs give distinct outputs. That is the definition
  in plain words, before a single equation — no two inputs are allowed to
  collide.
visual_need: |
  小映射：幾個「學生」輸入各自連到一個獨有的「ID 號碼」輸出，無任何箭頭交會。
animation_cue: （無——靜態映射即可；動態映射已在 motivation 用過，此處不重複）
```

---

### unit: testing_x_and_x_squared

```
id: testing_x_and_x_squared
source: chapter1-print-standalone.html §1.1 · Example 1.2（f(x)=x、g(x)=x^2）+ 其前「Now we return to the two mathematical examples」橋接散文
learning_goal: 把開場的直覺對比變成對定義的正式檢驗——一個通過、一個被同一輸出撞翻。
kind: example
narration: |
  We met these two at the very start; now let us run them through the
  definition. On $0$ to $1$, $f(x)=x$ sends every input to itself, so
  different inputs always land on different outputs — $f$ is one-to-one.
  But $g(x)=x^2$ on $-1$ to $1$ fails, and we can pin it down cleanly: $g$
  of a half is a quarter, and $g$ of negative a half is also a quarter.
  Two different inputs, one shared output — exactly the collision the
  definition rules out. So $g$ is not one-to-one on this interval — which is
  exactly why it needs careful handling later.
visual_need: |
  並排兩格：左 y=x 一對一；右 y=x^2 標出 1/2 與 -1/2 兩點同高（都到 1/4）。
animation_cue: （無——靜態即可；x^2 的幾何撞線交給 horizontal_line_test 單元動畫）
```

---

### unit: shape_can_mislead

```
id: shape_can_mislead
source: chapter1-print-standalone.html §1.1 · Example 1.3（h(x)=x^3-4x、k(x)=x^3+4）
learning_goal: 同樣貌的公式可以有相反結論；圖不在手邊時就直接驗定義。
kind: example
narration: |
  Here is a case where the formula can fool you. Compare $h(x)=x^3-4x$ with
  $k(x)=x^3+4$ on the whole real line — both look like cousins of $x^3$. But
  factor the first: $h(x)=x(x-2)(x+2)$, so $h$ of $0$ and $h$ of $2$ are
  both zero even though $0$ and $2$ are different inputs; $h$ is not
  one-to-one. The second behaves oppositely: if $k(x_1)=k(x_2)$, then
  $x_1^3=x_2^3$, and taking cube roots forces $x_1=x_2$, so $k$ is
  one-to-one. Same general shape, opposite verdicts — when the graph is not
  in front of you, test the definition directly.
visual_need: |
  （選用）h(x)=x^3-4x 的曲線略示其有兩個輸入同高（如 h(0)=h(2)=0）；
  主要靠代數，圖為輔。
animation_cue: （無——以代數為主）
```

---

### unit: horizontal_line_test

```
id: horizontal_line_test
source: chapter1-print-standalone.html §1.1 · Remark 1.1（Horizontal line test，具名規則）+ Figure 1.1（data-fig: hlt）+ 其前「Looking at the graph … a quick way」散文
learning_goal: 用一條水平線一眼判定 one-to-one；把代數上的「輸出撞在一起」看成幾何上的「線穿兩次」。
kind: proposition
narration: |
  When you do have the graph, there is a one-glance test. A horizontal line
  $y=c$ meets the graph of $f$ wherever $f(x)=c$, so a single output value
  showing up twice is the same as that line crossing the graph twice. That
  gives the rule: a function is one-to-one exactly when no horizontal line
  crosses its graph more than once. A straight line like $y=x$ passes —
  every horizontal line meets it just once. A parabola fails — a horizontal
  line slices clean through both arms, and those two crossings are exactly the
  pair of inputs sharing an output we found with algebra. One-to-one,
  in a single glance: no horizontal line gets to cross twice.
visual_need: |
  比照 Figure 1.1（hlt）的兩格對照：
  左格——直線（如 y=x），水平線 y=c 只交一次，標一個交點，註「one-to-one」；
  右格——拋物線（y=x^2 樣式），水平線 y=c 交兩次，標兩交點 (x_1,c)、(x_2,c)，註「not one-to-one」。
animation_cue: |
  建議動畫：左右兩格並排。一條水平線從畫面上方緩緩下移、掃過兩張圖。
  左格——它始終只碰到直線一次（保持綠色，過關）。右格——下移到碰上拋物線
  時切出兩個交點，閃示兩點、各拉一條虛線回 x 軸顯示兩個不同輸入（轉紅）。
  凸顯「交一次＝one-to-one、交兩次＝不是」。
```

---

### unit: inverse_function_definition

```
id: inverse_function_definition
source: chapter1-print-standalone.html §1.1 · "Inverse functions" 小節散文（"a second function that undoes f"）+ expansion:intuition 角色互換散文 + Definition 1.2 + Caution 1.1（折疊，見下方拆解註記 N1）
learning_goal: 知道反函數把輸入與輸出的角色對調（定義域與值域互換），並記住 f^{-1} 的記號不是倒數。
kind: definition
narration: |
  Once a function is one-to-one, we can build a second function that undoes
  it. The idea is simply to read the same correspondence backwards. Where
  $f$ asks "given the input, what is the output?", the inverse asks "given
  that output, which input produced it?" So the outputs of $f$ become the
  inputs of the inverse, and the domain and range trade places. We write
  the inverse as $f$ inverse, and define it like this: $f^{-1}(y)=x$ exactly
  when $f(x)=y$. One warning about the notation: that $-1$ means inverse
  function, not a reciprocal. $f^{-1}(x)$ is the inverse evaluated at $x$,
  which is a completely different thing from $1$ over $f(x)$ — and the same
  caution will matter for $\sin^{-1}$ shortly.
visual_need: |
  反函數的定義式 $f^{-1}(y)=x \iff f(x)=y$；一句「domain 與 range 互換」
  （f: A→B，f^{-1}: B→A）；一條對比警示 $f^{-1}(x)\ne \dfrac{1}{f(x)}$。
animation_cue: （無——靜態即可；對應的往返動畫放在 composition_identities）
```

---

### unit: inverse_iff_one_to_one

```
id: inverse_iff_one_to_one
source: chapter1-print-standalone.html §1.1 · Theorem 1.1 + Proof
learning_goal: 把「one-to-one」與「可逆」釘成同一件事，並看懂兩個方向各自為何成立。
kind: theorem
narration: |
  This ties the two halves of the section into one clean statement: a
  function has an inverse if and only if it is one-to-one. One direction is
  quick. Suppose $f$ already has an inverse and $f(x_1)=f(x_2)$; apply $f$
  inverse to both sides — the left collapses to $x_1$, the right to $x_2$,
  so $x_1=x_2$, and $f$ was one-to-one all along. The other direction
  builds the inverse: if $f$ is one-to-one, then every output $y$ in the
  range comes from exactly one input $x$, and sending each $y$ back to its
  unique $x$ is precisely the inverse function. So "one-to-one" and
  "invertible" are just two names for the same thing.
visual_need: |
  Theorem 陳述卡（has an inverse ⟺ one-to-one）＋兩段證明的關鍵步：
  forward 方向 $f^{-1}(f(x_1))=f^{-1}(f(x_2))\Rightarrow x_1=x_2$；
  backward 方向「每個 y∈B 有唯一 x，對應 y↦x 即 f^{-1}」。
animation_cue: （無——靜態即可）
```

---

### unit: first_inverses

```
id: first_inverses
source: chapter1-print-standalone.html §1.1 · Example 1.4（f(x)=x 自逆；g(x)=x^3 → ∛x，含 check）
learning_goal: 第一次親手算反函數——「解出輸入、再對調名字」這個動作，並用 composition 驗證。
kind: example
narration: |
  Let us compute a couple of inverses. Start with $f(x)=x$ — it
  leaves every input untouched, so undoing it does nothing either; $f$ is
  its own inverse, $f^{-1}(x)=x$. Now $g(x)=x^3$: set $y=x^3$, solve to get
  $x$ equals the cube root of $y$, then rename the variables to land on
  $g^{-1}(x)$ equals the cube root of $x$. And we can check it — $g$ of its
  inverse is the cube root of $x$, all cubed, which is just $x$ again. Solve
  for the input, swap the names; that is the move, and we are about to make
  it routine.
visual_need: |
  兩小段推導：f(x)=x ⇒ f^{-1}(x)=x；g(x)=x^3 ⇒ y=x^3, x=∛y, g^{-1}(x)=∛x，
  check $g(g^{-1}(x))=(\sqrt[3]{x})^3=x$。
animation_cue: （無——靜態推導步驟即可）
```

---

### unit: composition_identities

```
id: composition_identities
source: chapter1-print-standalone.html §1.1 · "The defining relation … yields two composition identities" 散文 + Proposition 1.1 + Figure 1.2（id fig-map）
learning_goal: 知道 f 與 f^{-1} 互為「精確的撤銷」，雙向皆然，並在 A↔B 映射上看見這趟往返。
kind: proposition
narration: |
  Undoing and then redoing should leave you exactly where you started —
  worth stating outright. For a one-to-one $f$, applying $f$ and
  then $f$ inverse returns the original input: $f^{-1}(f(x))=x$ for every
  $x$ in the domain. Going the other way works too: $f(f^{-1}(y))=y$ for
  every $y$ in the range. Picture an input $x$ in the set $A$; $f$ carries
  it across to its output in the set $B$, and $f$ inverse carries that
  output right back to the same $x$ — a round trip that lands home. Each
  function is the other's exact undo, in both directions.
visual_need: |
  比照 Figure 1.2（fig-map）：兩個集合泡泡 A、B，A 中一點 x，B 中對應點 f(x)；
  上方箭頭 f（A→B）、下方箭頭 f^{-1}（B→A）；兩條 identity 式
  $f^{-1}(f(x))=x$、$f(f^{-1}(y))=y$。
animation_cue: |
  建議動畫：A、B 兩泡泡，A 中一點 x。先沿上方箭頭 f 把 x 送到 B 的 f(x)；
  再沿下方箭頭 f^{-1} 把 f(x) 送回 A，落回原本那個 x（閃示確認是同一點）。
  凸顯「出去再回來、回到原點」的往返；可再從 B 的某點 y 反向走一趟。
```

---

### unit: reflection_across_y_equals_x

```
id: reflection_across_y_equals_x
source: chapter1-print-standalone.html §1.1 · 散文「the two graphs are reflections … across y=x；(a,b) on f ⟺ (b,a) on f^{-1}」（以 Example 1.4 的 x^3／∛x 具體示範，CONTENT_METHODOLOGY §5）
learning_goal: 把「取反函數」看成幾何動作——對 y=x 鏡射，座標 (a,b) 換成 (b,a)。
kind: visual
narration: |
  There is a clean picture of what taking an inverse does to a graph. If you
  draw $f$ and its inverse in the same plane, the two graphs are mirror
  images across the line $y=x$. The reason is the same swap: a point $(a,b)$
  sits on the graph of $f$ exactly when $(b,a)$ sits on the graph of the
  inverse, and reflecting across $y=x$ is precisely what trades a point's
  two coordinates. You can watch it on the cube and the cube root from a
  moment ago — fold the graph of $x^3$ over the line $y=x$ and it lands
  right on the graph of the cube root. Inverse, geometrically: reflect
  across $y=x$.
visual_need: |
  同一平面畫 y=x^3 與 y=∛x，虛線 y=x；標一對對應點 (a,b) 在 cube 上、
  (b,a) 在 cube-root 上。
animation_cue: |
  建議動畫：先畫 y=x^3 與虛線 y=x。取曲線上一個標好的點 (a,b)，animate 它
  對 y=x 鏡射到 (b,a)。接著把整條 x^3 曲線沿 y=x 翻摺／掃過，疊到 ∛x 曲線上
  完全吻合。凸顯座標對調與鏡射。
```

---

### unit: repair_by_restricting

```
id: repair_by_restricting
source: chapter1-print-standalone.html §1.1 · Example 1.5（restrict x^2 到 [0,∞)，inverse √x；為何 √ 取正根）+ Figure 1.3（data-fig: restrict-x2）
learning_goal: 看見「先限定定義域、再求逆」如何修好一個本來不可逆的函數，並懂這是 √ 取正根的由來。
kind: example
narration: |
  What about a function that fails the one-to-one test — is it hopeless? Not
  necessarily. Take $f(x)=x^2$, which we already know is not one-to-one on
  the whole line. But chop its domain down to the nonnegative numbers, from
  $0$ onwards, and it becomes one-to-one: if two nonnegative inputs square
  to the same value, they were equal to begin with. Now we can invert it —
  solving gives $f^{-1}(x)=\sqrt{x}$, and because the inputs were
  nonnegative we take the positive root. That is why the square
  root symbol means the positive root: it is the convention that makes
  square root the genuine inverse of squaring. Restrict first, then invert
  — and that exact move is the key that unlocks the inverse trigonometric
  functions coming up.
visual_need: |
  比照 Figure 1.3（restrict-x2）：同一平面畫限定到 [0,∞) 的 y=x^2、其反函數
  y=√x，以及虛線鏡射軸 y=x；標 f(x)=x^2 與 f^{-1}(x)=√x。
animation_cue: |
  建議動畫：先畫整條拋物線 y=x^2（含 x<0 左臂）。把左臂（x<0）淡出／丟棄，
  只留右臂（x≥0）。再把保留的右臂沿 y=x（虛線）鏡射，生成 √x 曲線。
  凸顯「限定 → 鏡射」修好可逆性。
```

---

### unit: finding_the_inverse_strategy

```
id: finding_the_inverse_strategy
source: chapter1-print-standalone.html §1.1 · Strategy 1.1（Finding the inverse of a one-to-one function）+ Remark 1.2（以 x 為反函數自變數，折疊，見拆解註記 N2）+ 其後「this procedure assumes f is already one-to-one … ±√y」警示散文（折疊，見 N3）
learning_goal: 把求逆的動作收成三步程序，並守住「必須先是 one-to-one」這道前提。
kind: procedure
narration: |
  We have inverted a few functions by hand; let us package the moves into a
  procedure. Step one: write $y=f(x)$. Step two: solve that equation for $x$
  in terms of $y$. Step three: interchange the names $x$ and $y$ — the
  result reads $y=f^{-1}(x)$. That last swap is just the habit of using
  $x$ for the inverse's own input. One guardrail, though: this only works
  if $f$ is already one-to-one. Apply it blindly to $y=x^2$ and step two
  hands you $x=\pm\sqrt{y}$ — two values, not a function. So always check
  one-to-one first, or restrict the domain the way we just did.
visual_need: |
  三步程序（祈使句）：1) Write $y=f(x)$；2) Solve for $x$ in terms of $y$；
  3) Interchange $x$ and $y$ → $y=f^{-1}(x)$。附一條警示：blind on $y=x^2$
  ⇒ $x=\pm\sqrt{y}$（not a function）。
animation_cue: （無——靜態程序步驟即可）
```

---

### unit: inverse_of_a_cubic

```
id: inverse_of_a_cubic
source: chapter1-print-standalone.html §1.1 · Example 1.6（f(x)=x^3+2 → ∛(x-2)，含 check）
learning_goal: 第一次照三步程序乾淨地跑一個例子，並用 composition 驗證。
kind: example
narration: |
  Now run the procedure on a fresh function: $f(x)=x^3+2$. Write
  $y=x^3+2$. Solve for $x$ — subtract to get $x^3=y-2$, then take the cube
  root, $x=\sqrt[3]{y-2}$. Interchange the names and you have
  $f^{-1}(x)=\sqrt[3]{x-2}$. Check it by composing: $f$ of the inverse is
  the cube root of $x-2$, all cubed, plus $2$ — the cube and cube root
  cancel, leaving $x-2$ plus $2$, which is $x$. Three steps, one check,
  done.
visual_need: |
  推導鏈：y=x^3+2 → x^3=y-2 → x=∛(y-2) → f^{-1}(x)=∛(x-2)；
  check $f(f^{-1}(x))=(\sqrt[3]{x-2})^3+2=(x-2)+2=x$。
animation_cue: （無——靜態推導鏈即可）
```

---

### unit: inverse_of_a_rational

```
id: inverse_of_a_rational
source: chapter1-print-standalone.html §1.1 · Example 1.7（f(x)=3/(x-5) → (5x+3)/x，雙向驗證 + 定義域配對）
learning_goal: 在有理函數上跑同一程序，並以「雙向 composition」誠實驗證，順帶看定義域如何配對。
kind: example
narration: |
  Same three steps, but now the algebra is a touch more delicate — a
  rational function, $f(x)=\dfrac{3}{x-5}$. Set $y=\dfrac{3}{x-5}$. Solving,
  $x-5=\dfrac{3}{y}$, so $x=5+\dfrac{3}{y}$; interchanging gives
  $f^{-1}(x)=5+\dfrac{3}{x}$, which we can also write as
  $\dfrac{5x+3}{x}$. This time let us verify both directions: $f$ of the
  inverse and the inverse of $f$ each come back to $x$, exactly the
  composition identities at work. And notice the domains pair up: $f$ cannot take $x=5$, the inverse
  cannot take $x=0$, mirroring the fact that $f$ never outputs $0$ and the
  inverse never outputs $5$.
visual_need: |
  推導：y=3/(x-5) → x-5=3/y → x=5+3/y → f^{-1}(x)=5+3/x=(5x+3)/x；
  雙向驗證 $f(f^{-1}(x))=x$、$f^{-1}(f(x))=x$；一句定義域配對註記
  （f 排除 x=5、f^{-1} 排除 x=0）。
animation_cue: （無——靜態推導＋驗證即可）
```

---

### unit: inverse_in_an_application

```
id: inverse_in_an_application
source: chapter1-print-standalone.html §1.1 · Example 1.8（f(t)=9/5·t+32 攝氏→華氏；f^{-1} 答什麼問題 + 求式 + check）
learning_goal: 看見反函數不只是代數——它把同一關係讀成有用的方向（華氏讀回攝氏）。
kind: example
narration: |
  One more, where the inverse answers a real question. The function
  $f(t)=\tfrac{9}{5}t+32$ turns a Celsius temperature into Fahrenheit. So
  what does its inverse do? It runs the conversion in reverse —
  Fahrenheit back to Celsius. Solving $t=\tfrac{9}{5}f^{-1}(t)+32$ for the
  inverse gives $f^{-1}(t)=\tfrac{5}{9}(t-32)$. For the check, feed a
  Celsius reading through $f$ and then through the inverse: the $32$s cancel,
  the nine-fifths and five-ninths undo each other, and you get $t$ back. An inverse is not just algebra — it is the same
  relationship read in the direction you happen to need.
visual_need: |
  f(t)=9/5·t+32（C→F）；f^{-1}(t)=5/9·(t-32)（F→C）；
  check $f^{-1}(f(t))=\tfrac{5}{9}(\tfrac{9}{5}t+32-32)=t$。
animation_cue: （無——靜態即可）
```

---

### unit: recap

```
id: recap
source: chapter1-print-standalone.html §1.1（全節重點凝煉；Key Takeaways 單元，有旁白）
learning_goal: 把本節串成一條線——one-to-one ⇒ 可逆 ⇒ 對 y=x 鏡射 ⇒ 解出再對調求得。
kind: recap
narration: |
  Let us gather what we have built. A function is one-to-one when distinct
  inputs give distinct outputs — and you can spot it at a glance with the
  horizontal line test, where no line is allowed to cross twice. A function
  is invertible exactly when it is one-to-one, and its inverse swaps inputs
  with outputs, so its graph is the mirror image across $y=x$. To find an
  inverse you solve $y=f(x)$ for $x$ and swap the names — after checking
  one-to-one, or restricting the domain to get there. And keep the notation
  straight: $f$ inverse undoes $f$; it is not $1$ over $f$. One-to-one,
  invertible, reflected across $y=x$ — that is the whole arc of the section.
visual_need: |
  Key Takeaways 卡片（4 點）＋ remember-formula 卡：
  points：
    • One-to-one ＝ different inputs give different outputs（horizontal line test：no line crosses twice）。
    • Invertible ⟺ one-to-one。
    • Inverse swaps domain and range; graph reflects across y=x。
    • Find it: solve $y=f(x)$ for $x$, then interchange $x$ and $y$（after checking one-to-one）。
  formulas（保持短，避免出框）：
    • $f^{-1}(y)=x \iff f(x)=y$
    • $f^{-1}(f(x))=x,\; f(f^{-1}(y))=y$
    • $f^{-1}\ne 1/f$
animation_cue: （無——靜態卡片即可）
```

---

### unit: outro

```
id: outro
source: chapter1-print-standalone.html §1.1（節末品牌字卡）
learning_goal: （收尾；無教學內容）
kind: recap
narration: （無——outro 為純動畫，無 takeaways）
visual_need: 兩段式 outro——暗轉亮橋接 → 最終 logo／節號／標題字卡。
animation_cue: （由 outro 模板處理）
```

---

## §7 拆解註記與內容層品質檢核

### 拆解／折疊決策（就近註明，杜絕 silent drop）

- **N1 — Caution 1.1（f^{-1} 非倒數）折疊進 `inverse_function_definition`。** 依 CONTENT_METHODOLOGY §3「env-caution（1–3 句陷阱警示）併入其警示對象的單元」——警示對象正是該單元剛introduce 的 $f^{-1}$ 記號；定義＋緊接的記號警示讀為同一個教學重點（「反函數是什麼、它的記號是／不是什麼意思」）。Caution 提到的「同樣警示適用於下一節的 $\sin^{-1}$」以口語「shortly」承接、**不報節號**（§4）。
- **N2 — Remark 1.2（以 x 為反函數自變數）折疊進 `finding_the_inverse_strategy`。** 依 §3「短附註併入鄰段 narration」——此記號慣例正是 Strategy 步驟 3「interchange x and y」的理由，折進該步最自然（「That last swap is just the habit of using $x$ for the inverse's own input」）。
- **N3 — Strategy 後的警示散文（盲套 $y=x^2$ ⇒ $\pm\sqrt y$）折疊進 `finding_the_inverse_strategy`** 作為 guardrail beat（§3 caution 併入其對象單元）。
- **例題：全 8 例皆帶不同教學模式，全數納入（代表式涵蓋，§2）：** 1.1 真實世界 one-to-one（不需代數）／1.2 對定義的正式檢驗（x vs x^2）／1.3 同貌公式相反結論（cubic 陷阱）／1.4 首次求逆（自逆＋cube root）／1.5 限定定義域修復＋√取正根（橋接 §1.2）／1.6 程序首次乾淨套用（cubic）／1.7 有理函數＋雙向驗證＋定義域配對／1.8 應用（攝氏華氏）。**無同型折疊**（無一例純為另一例的 drill）。1.6／1.7／1.8 雖同為「套程序求逆」，但各帶新情形（多項式／有理／應用＋雙向驗證），且 1.7／1.8 以 repeat-pattern 省去程序複述（§4）。
- **散文歸類（§3，無 silent drop）：** 開節三階段散文＋warmup＋「difference is central point」→ `can_we_run_it_backwards`（Incorporative/motivation）；「A function can be reversed only when…」→ `one_to_one_definition` lead-in；「Now we return to the two…」→ `testing_x_and_x_squared` lead-in；「Looking at the graph…」→ `horizontal_line_test` lead-in；「If f is one-to-one … undoes f」＋角色互換 gloss → `inverse_function_definition` lead-in；「The defining relation … yields two composition identities」→ `composition_identities` lead-in；「Graphically … reflections across y=x」→ `reflection_across_y_equals_x`（散文幾何主張升格視覺單元，§5）；「When f is one-to-one … short procedure」→ `finding_the_inverse_strategy` lead-in。

### 視覺／動畫盤點（§5；§1.1 約 55% 符號，medium——不套 symbol-heavy 例外，視覺各司其職）

- 三張講義圖全覆蓋：Figure 1.1（hlt）→ `horizontal_line_test`；Figure 1.2（fig-map）→ `composition_identities`；Figure 1.3（restrict-x2）→ `repair_by_restricting`。
- 散文幾何主張升格視覺：對 y=x 鏡射 → `reflection_across_y_equals_x`（以 x^3／∛x 具體示範，§5 允許「一般主張用具體函數示範」、呼應本節已出現的 Example 1.4）。
- 5 個 `animation_cue`（會動的概念才動，§5「Animate, not just display」）：can_we_run_it_backwards（兩進一出映射）、horizontal_line_test（水平線掃描）、composition_identities（A↔B 往返）、reflection_across_y_equals_x（對 y=x 翻摺）、repair_by_restricting（限定後鏡射）。生成的 manim code 視同 narration，**經使用者認可才定版**（§5）。

### 內容層 checklist（§7）

- [x] 每個 definition（1.1、1.2）／theorem（1.1）／proposition（1.1）有單元覆蓋；strategy（1.1）有單元；每個不同模式 example（1.1–1.8）有代表單元，無同型 silent drop。
- [x] 無 exercise 內容洩入（本節 fragment 無 env-exercise）。
- [x] intro（定位＋tagline）／recap（takeaway 清單）／outro（無 takeaways）齊備。
- [x] 散文幾何主張（鏡射）有視覺單元；其餘散文皆歸類折疊／升格，無 silent drop。
- [x] 每段環境之間散文已歸類（Incorporative／Bridge／Forward-pointing）。
- [x] narration 為「說」而寫：開頭 hook、結尾 takeaway、未犯 §4 禁則（不報節號／圖號、不念螢幕標題、不用 see/as shown）、同型第二例（1.7/1.8）repeat-pattern 省 setup。
- [x] 數學讀得順（直讀 LaTeX 或白話；下標念 sub、f^{-1} 念 f inverse——口語攤平屬 .spoken.yml，不污染正典）。
- [x] 動畫建議用自然語言、聚焦教學意圖。
- [x] 每個 id 唯一、snake_case、描述教學重點。
- [x] **六鏡稽核 → 收斂（2026-06-17）：0 blocking、0 advisory**（Workflow `wf_c4490aab-0bd`，六鏡並行→refute-by-default 複驗；L5 數學隔離盲算，每例題／因式分解／composition／定義域配對獨立重算全 match）。
- [x] **散文潤稿 pass（2026-06-17，gate1 Claude，鎖稿前）：4 tighten＋6 optional 全 advisory（blocking==0）**；採納 7 條純 wording 緊縮（語義/數學未動）——testing_x_and_x_squared 收尾、horizontal_line_test 收尾、first_inverses 去「actually」、composition_identities 去 padding、repair_by_restricting 去「actually」、inverse_of_a_cubic 開場去「Let us」echo、inverse_in_an_application「the other way→in reverse」。gate2 Codex（計費）已於本輪補跑（見下行）。
- [x] **散文潤稿 gate2（2026-06-17，Codex `gpt-5.5` xhigh，read-only，計費、使用者授權）：3 tighten＋2 optional 全 advisory**；5 條全採（純 wording、語義/數學未動）——one_to_one_definition 去 name-then-define tic、finding_the_inverse_strategy 拆分詞冗、inverse_of_a_rational 去三重「comes back to x」、inverse_function_definition 長句拆三、inverse_in_an_application「composes back to the start」改順口。報告 [`_audit/REPORT-ch01_inverse_functions-narration-copyedit.raw.txt`](_audit/REPORT-ch01_inverse_functions-narration-copyedit.raw.txt)。
- [x] 已編譯 `ch01_inverse_functions_narration.html` 審核稿＋ `REVIEW-ch01_inverse_functions-sixlens.html` 完工報告（均已同步 gate2 後措辭）。
- [x] **旁白 sign-off（使用者，2026-06-17）：通過 → LOCKED。** 下一步：Stage 2 工程稿 `ch01_inverse_functions.yml`（模板化、`{show}`／accent／payload）→ schema/lint/sizecheck → mock → 視覺稽核 → 5 客製動畫 → MiMo 口語軌＋NFA → MiMo TTS（計費，屆時徵同意）。
```
