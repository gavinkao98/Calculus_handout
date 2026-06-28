# §3.1 Derivatives of Sine and Cosine — 影片內容稿（content script）

> **產線：** 講義 → 影片，gen-2。Chapter 3 第一節，從 HTML 講義逐節重跑。
> **權威來源：** [`../../handout/fragments/ch03/sec-3-1.html`](../../handout/fragments/ch03/sec-3-1.html)（建置版 `handout/chapter3-print-standalone.html` §3.1）。
> **這是什麼：** 純內容中間產物（source of truth）。格式見 [`../CONTENT_METHODOLOGY.md`](../CONTENT_METHODOLOGY.md) §6——只含 `id`／`source`／`learning_goal`／`kind`／`narration`／`visual_need`／`animation_cue`，**不含**任何工程欄位（template／`{show}`／accent／payload／divider）。工程是第二階段的事。
> **階段：** **LOCKED**（2026-06-28 使用者認可旁白；`CONTENT_APPROVED=yes`）。DRAFT 階段六鏡稽核收斂（blocking==0）＋散文 copyedit（6 條緊縮）已收尾。鎖稿後 source 凍結、忠實性由 NFA 把關（鎖稿後不改措辭）；任何 post-lock 改稿須對動到的單元跑 scoped NFA 回歸（CONTENT_METHODOLOGY §8）。narration 認可在編譯出的 `_narration.html` 上進行；本 `.md` 為權威，兩者 MUST 一致。

---

## meta（intro/outro 定位資訊）

- `id`: ch03_trig_derivatives
- `section`: 3.1
- `title`: Derivatives of Sine and Cosine
- `chapter`: Chapter 3
- `chapter_title`: Chain Rule and Trigonometric Derivatives
- `tagline`（intro 引導問題）: How fast does sine change?
- 章內節次（intro 章節地圖用）：
  - 3.1 Derivatives of the Sine and Cosine Functions ← 本節
  - 3.2 The Chain Rule
  - 3.3 Applications of the Chain Rule

> intro 與 outro 為純動畫、**無 narration**（gen-2 first-class）。Key Takeaways 在 `recap` 教學單元（有旁白），不在 outro。Stage divider（章內分段開場）是第二階段 storyboard 的結構元素，**不在本內容稿**。

---

## 教學單元（依教學自由重排；忠實仍可逐單元回溯講義）

---

### unit: intro

```
id: intro
source: chapter3-print-standalone.html §3.1（Section Gate；定位資訊見上方 meta）
learning_goal: 知道本節在章內的位置，並帶著「sine 變化得多快」這個問題進入。
kind: motivation
narration: （無——intro 為純動畫）
visual_need: Section Gate——Chapter 3 章節地圖 → 聚焦 3.1 → logo／節號／標題／tagline 字卡 → 暗場交接。
animation_cue: （由 intro 模板處理，內容稿不指定）
```

---

### unit: why_trig_is_different

```
id: why_trig_is_different
source: chapter3-print-standalone.html §3.1 · 開節散文（expansion:intuition，"So far every derivative has yielded to algebra … funnels down to a single limit"）+ "angles are measured in radians" 預告句
learning_goal: 看出三角函數的導數卡在一個代數攻不下的極限 sinθ/θ，需要全新的幾何工具。
kind: motivation
narration: |
  Every derivative so far has yielded to algebra. For a polynomial we
  expanded $(x+h)^n$ and canceled the factor of $h$; for $e^x$ the power
  series did the same job. The trigonometric functions are different in
  kind. Write down the difference quotient for $\sin x$ —
  $\dfrac{\sin(x+h)-\sin x}{h}$ — and the usual move stalls: no identity
  cancels that $h$ in the denominator, because $\sin(x+h)$ does not split
  into pieces that conveniently subtract. As we are about to see, the whole
  computation funnels down to a single limit, $\lim_{\theta\to 0}
  \dfrac{\sin\theta}{\theta}$, which has the indeterminate form zero over
  zero and which no algebra will crack. Breaking it open takes a
  genuinely new tool — a geometric comparison of areas on the unit circle.
  And once we secure that one limit, it unlocks the derivatives of both
  sine and cosine at once. One ground rule before we start: throughout,
  angles are measured in radians, and that assumption turns out to be
  essential.
visual_need: |
  差分商 $\dfrac{\sin(x+h)-\sin x}{h}$；指向目標極限 $\lim_{\theta\to 0}\dfrac{\sin\theta}{\theta}$（標 0/0）。
animation_cue: （無——靜態即可；funnel 的視覺收斂交給後續單元）
```

---

### unit: difference_quotient_for_sine

```
id: difference_quotient_for_sine
source: chapter3-print-standalone.html §3.1 · "The difference quotient for sine" 子節（sum-to-product 化簡 → cos(x+h/2)·sin(h/2)/(h/2)）
learning_goal: 把 sine 的差分商化成「一個會趨近 cos x 的因子 × 一個基本極限因子」，看出整個導數靠哪兩件事。
kind: derivation
narration: |
  So let us transform that difference quotient. The decisive step is a
  sum-to-product identity: $\sin A - \sin B = 2\cos\frac{A+B}{2}
  \sin\frac{A-B}{2}$. Take $A=x+h$ and $B=x$, and the numerator becomes
  $2\cos\!\left(x+\frac h2\right)\sin\frac h2$. Now divide by $h$, but write
  $h$ as $2$ times $\frac h2$ so it matches the $\frac h2$ tucked inside the
  sine. The quotient cleans up to $\cos\!\left(x+\frac h2\right)\cdot
  \dfrac{\sin(h/2)}{h/2}$. Look at what we have: two factors, and as
  $h\to 0$ each one moves. The cosine factor should slide to
  $\cos x$ — provided cosine is continuous — and the second factor is exactly
  $\dfrac{\sin\theta}{\theta}$ with $\theta=\frac h2$. So the whole derivative
  rests on just two facts: that sine and cosine are continuous, and the value
  of that fundamental limit. We secure both now.
visual_need: |
  推導鏈：$\sin(x+h)-\sin x = 2\cos(x+\tfrac h2)\sin\tfrac h2$ →
  $\dfrac{\sin(x+h)-\sin x}{h}=\cos(x+\tfrac h2)\cdot\dfrac{\sin(h/2)}{h/2}$；
  標出兩個因子各自的去向（→cos x；→基本極限）。
animation_cue: （無——靜態推導鏈即可）
```

---

### unit: sector_inequality

```
id: sector_inequality
source: chapter3-print-standalone.html §3.1 · "A geometric inequality on the unit circle" 散文（含偶函數論證）+ Figure 3.1（data-fig: sector-inequality）
learning_goal: 在單位圓上用三塊嵌套面積，幾何地夾出 sinθ ≤ θ ≤ tanθ。
kind: visual
narration: |
  First, one convenience. Replacing $\theta$ by $-\theta$ flips
  the sign of both $\theta$ and $\sin\theta$, so their ratio
  $\sin\theta/\theta$ is left unchanged — it is an even function, and that
  means it is enough to chase $\theta$ down to zero from the positive side.
  Now the geometry. On the unit circle, put $A$ at $(1,0)$ and let $B$ be the
  point at angle $\theta$, so $B=(\cos\theta,\sin\theta)$. Extend the radius
  until it meets the vertical tangent line at $A$, and call that point
  $C=(1,\tan\theta)$. Three regions now nest one inside the next. The inner
  triangle $OAB$ has base one and height $\sin\theta$, so its area is
  $\frac12\sin\theta$. The circular sector $OAB$ is the fraction $\theta$ over
  $2\pi$ of the whole disc, which comes out to $\frac12\theta$. And the outer
  triangle $OAC$ has base one and height $\tan\theta$, so its area is
  $\frac12\tan\theta$. Because each region sits inside the next, their areas
  line up in that same order: $\frac12\sin\theta \le \frac12\theta \le
  \frac12\tan\theta$.
visual_need: |
  單位圓（半徑 1），A=(1,0)、B=(cosθ,sinθ)、C=(1,tanθ)、射線 OB 延伸交切線於 C；
  三塊嵌套區域：內接 △OAB、扇形 OAB、外切 △OAC，各標面積 ½sinθ／½θ／½tanθ；
  浮出 $\tfrac12\sin\theta \le \tfrac12\theta \le \tfrac12\tan\theta$。
animation_cue: |
  建議動畫：先畫單位圓與 A。掃出角 θ 標出 B，延伸 OB 交切線得 C。依序高亮
  並標面積——內接三角形（½sinθ）→ 扇形（½θ）→ 外切三角形（½tanθ），讓「一個包
  一個」在視覺上逐層成立，最後浮出三者面積的不等式。θ 可從中等角緩緩縮小，
  預告後續要把它推向 0。
```

---

### unit: squeeze_to_the_bound

```
id: squeeze_to_the_bound
source: chapter3-print-standalone.html §3.1 · Fig 3.1 後代數（×2、÷sinθ、取倒數翻向 → 式(1)）+ "0 ≤ |sinθ| ≤ |θ|" 附帶界
learning_goal: 把三塊面積的不等式代數地整理成 cosθ ≤ sinθ/θ ≤ 1，並收下 |sinθ|≤|θ| 這個附帶界。
kind: derivation
narration: |
  Now turn that chain of areas into a statement about $\sin\theta/\theta$.
  Multiply through by $2$: $\sin\theta \le \theta \le \tan\theta$. Divide by
  $\sin\theta$, which is positive here, and rewrite $\tan\theta$ as
  $\sin\theta/\cos\theta$ — that gives $1 \le \dfrac{\theta}{\sin\theta} \le
  \dfrac{1}{\cos\theta}$. Every term is positive, so taking reciprocals
  reverses the inequalities, and we land on the bound we were after:
  $\cos\theta \le \dfrac{\sin\theta}{\theta} \le 1$, for $\theta$ between zero
  and $\frac\pi2$. Tuck one more consequence in your pocket while we are here:
  from $\sin\theta \le \theta$ we also get $0 \le |\sin\theta| \le |\theta|$
  near zero — a small bound we will lean on twice in just a moment.
visual_need: |
  推導鏈：$\sin\theta\le\theta\le\tan\theta$ → $1\le\tfrac{\theta}{\sin\theta}\le\tfrac{1}{\cos\theta}$
  → （取倒數翻向）$\cos\theta \le \tfrac{\sin\theta}{\theta} \le 1$（標式 1，限 0<θ<π/2）；
  附帶界 $0\le|\sin\theta|\le|\theta|$。
animation_cue: （無——靜態推導鏈即可）
```

---

### unit: continuity_of_sin_cos

```
id: continuity_of_sin_cos
source: chapter3-print-standalone.html §3.1 · Proposition 3.1（sin、cos 連續）+ Proof
learning_goal: 用 |sinθ|≤|θ| 與夾擠定理證明 sine、cosine 處處連續——這正是差分商兩因子收斂所需。
kind: theorem
narration: |
  That little bound does more than help with the limit — it is also what
  makes sine and cosine continuous, which is exactly what those two factors
  of the difference quotient needed in order to settle down. Here is the
  claim: $\sin x$ and $\cos x$ are continuous at every real $x_0$. Start
  small. Since $0 \le |\sin\theta| \le |\theta|$ and $|\theta|$ goes to zero,
  the squeeze theorem forces $\sin\theta \to 0$ as $\theta\to 0$. Now fix a
  point $x_0$. The sum-to-product identities let us bound the change in each
  function by the same quantity: both $|\cos x-\cos x_0|$ and
  $|\sin x-\sin x_0|$ are at most $2\,|\sin\frac{x-x_0}{2}|$, since the other
  factor never exceeds one in size. As $x$ approaches $x_0$ that half-angle
  goes to zero, so by what we just showed both bounds collapse to zero.
  Squeeze once more, and $\cos x\to\cos x_0$ and $\sin x\to\sin x_0$ — both
  functions are continuous.
visual_need: |
  Proposition 陳述卡（sin、cos 在每個 x₀ 連續）＋證明邏輯鏈：
  $0\le|\sin\theta|\le|\theta|$ + squeeze ⇒ $\lim_{\theta\to0}\sin\theta=0$；
  $|\cos x-\cos x_0|,\,|\sin x-\sin x_0|\le 2|\sin\tfrac{x-x_0}{2}|\to0$ ⇒ 連續。
animation_cue: （無——靜態陳述＋證明鏈即可）
```

---

### unit: fundamental_limit

```
id: fundamental_limit
source: chapter3-print-standalone.html §3.1 · Proposition 3.2（lim sinθ/θ = 1）+ Proof
learning_goal: 用 cosθ ≤ sinθ/θ ≤ 1、cosθ→1 與偶函數，夾擠出基本極限等於 1。
kind: proposition
narration: |
  Now we can finish the limit that started all this. The claim is clean:
  $\lim_{\theta\to 0}\dfrac{\sin\theta}{\theta}=1$. We already have the trap.
  For $\theta$ between zero and $\frac\pi2$, $\cos\theta \le
  \dfrac{\sin\theta}{\theta} \le 1$. The ceiling is the constant one. The
  floor is $\cos\theta$, which tends to $\cos 0 = 1$ now that we know cosine
  is continuous. So the ratio is pinned between two quantities both heading to
  one — the squeeze theorem says it must head to one as well, at least from
  the right. And because $\sin\theta/\theta$ is even, its left-hand limit
  matches its right, so the full two-sided limit is one too. That is the
  keystone; the rest of the section rests on it.
visual_need: |
  Proposition 陳述卡（$\lim_{\theta\to0}\tfrac{\sin\theta}{\theta}=1$）＋證明鏈：
  式(1) squeeze、$\cos\theta\to1$（連續）、偶 ⇒ 兩側極限相等。
animation_cue: （無——靜態陳述＋證明鏈即可）
```

---

### unit: squeeze_graph

```
id: squeeze_graph
source: chapter3-print-standalone.html §3.1 · Figure 3.2（data-fig: squeeze-limit；同一不等式讀成函數圖）
learning_goal: 把基本極限的夾擠看成一張圖——sinθ/θ 被困在 cosθ 與 1 之間，θ=0 處是極限不是值。
kind: visual
narration: |
  It helps to see that squeeze as a picture. Plot the ratio
  $\dfrac{\sin\theta}{\theta}$ near zero — the solid curve. Below it runs
  $\cos\theta$, dashed, and above it sits the constant line at height one. The
  ratio is trapped in the narrowing gap between them. As $\theta$ slides
  toward zero, the floor $\cos\theta$ rises to one while the ceiling already
  is one, so the curve caught between them is squeezed right up to one. And
  notice the open circle at $\theta=0$: the ratio is undefined there — zero
  over zero — so what equals one is the limit, the height the curve is forced
  toward, not a value it ever actually takes.
visual_need: |
  函數圖（θ 近 0）：$\tfrac{\sin\theta}{\theta}$（實線）夾在 $\cos\theta$（虛線，下）
  與常數 $1$（上）之間；θ=0 處開圓（open circle，標 undefined）；兩界皆 →1。
animation_cue: |
  建議動畫：先畫常數線 y=1 與 cosθ（虛線）。再 trace 出 sinθ/θ 落在兩者之間。
  讓 θ 從兩側滑向 0，cosθ 抬升到 1、ratio 被擠到 1；最後在 θ=0 標一個空心圓，
  凸顯「是極限、不是值」。
```

---

### unit: limit_not_identity

```
id: limit_not_identity
source: chapter3-print-standalone.html §3.1 · Caution（Proposition 3.2 是極限敘述、非恆等式；θ=π/2、θ=π 的值）
learning_goal: 別把基本極限誤讀成恆等式——固定角下 sinθ/θ 一般不等於 1。
kind: counterexample
narration: |
  One caution, because this is easy to over-read. The statement is about the
  limit as $\theta\to 0$ — it is not an identity. At a fixed angle the ratio
  is generally not one. At $\theta=\frac\pi2$ it is
  $\dfrac{\sin(\pi/2)}{\pi/2}=\dfrac{1}{\pi/2}=\dfrac{2}{\pi}$, about
  $0.64$; and at $\theta=\pi$ it is $\dfrac{0}{\pi}$, which is just zero. The
  value one is reached only in the limit, as $\theta$ shrinks to nothing.
visual_need: |
  警示卡：$\lim_{\theta\to0}\tfrac{\sin\theta}{\theta}=1$ 但固定角 ≠ 1——
  $\tfrac{\sin(\pi/2)}{\pi/2}=\tfrac{2}{\pi}\approx0.64$、$\tfrac{\sin\pi}{\pi}=0$。
animation_cue: （無——靜態警示即可）
```

---

### unit: radians_essential

```
id: radians_essential
source: chapter3-print-standalone.html §3.1 · Caution（弧度制必要；度數下極限為 π/180、sin' 帶 π/180 因子）
learning_goal: 懂得弧度制不是慣例而是 sin'=cos、cos'=−sin 成立的前提——度數下公式會帶醜因子。
kind: counterexample
narration: |
  A second caution, and this one is structural: everything here depends on
  measuring angles in radians. The sector area $\frac12\theta$ — and through
  it the limit $\sin\theta/\theta\to 1$ — relies on radian measure, where the
  arc cut off on the unit circle has length exactly $\theta$. Switch to
  degrees and the limit is no longer one. Since $x$ degrees is
  $\frac{\pi}{180}x$ radians, you get $\lim_{x\to 0}\dfrac{\sin(x^\circ)}{x}=
  \dfrac{\pi}{180}$, and the derivative drags that factor along:
  $\dfrac{d}{dx}\sin(x^\circ)=\dfrac{\pi}{180}\cos(x^\circ)$. The clean
  formulas we are about to prove, $\sin'=\cos$ and $\cos'=-\sin$, hold only
  in radians. So radians are not a stylistic choice here — they are what
  keeps the calculus tidy.
visual_need: |
  警示卡：弧度 → $\sin\theta/\theta\to1$、$\sin'=\cos$；度數 →
  $\lim_{x\to0}\tfrac{\sin(x^\circ)}{x}=\tfrac{\pi}{180}$、
  $\tfrac{d}{dx}\sin(x^\circ)=\tfrac{\pi}{180}\cos(x^\circ)$。
animation_cue: （無——靜態警示即可）
```

---

### unit: derivative_of_sine

```
id: derivative_of_sine
source: chapter3-print-standalone.html §3.1 · Theorem 3.1（d/dx sin x = cos x）+ Proof
learning_goal: 把連續與基本極限組裝起來，證出 sin 的導數是 cos。
kind: theorem
narration: |
  Now the payoff. With continuity and the fundamental limit in hand, the
  difference quotient for sine all but evaluates itself. The claim:
  $\dfrac{d}{dx}\sin x=\cos x$, for every real $x$. We already rewrote the
  quotient as $\cos\!\left(x+\frac h2\right)\cdot\dfrac{\sin(h/2)}{h/2}$. Let
  $h\to 0$. The first factor tends to $\cos x$, because cosine is continuous;
  the second tends to one, by the fundamental limit, with $\theta=\frac h2$.
  Their product tends to $\cos x$ times one — which is just $\cos x$. The
  derivative of sine is cosine.
visual_need: |
  Theorem 陳述卡（$\tfrac{d}{dx}\sin x=\cos x$）＋證明鏈：
  $\lim_{h\to0}\cos(x+\tfrac h2)\cdot\tfrac{\sin(h/2)}{h/2}=\cos x\cdot1=\cos x$。
animation_cue: （無——靜態陳述＋證明鏈即可）
```

---

### unit: derivative_of_cosine

```
id: derivative_of_cosine
source: chapter3-print-standalone.html §3.1 · Theorem 3.2（d/dx cos x = −sin x）+ Proof（伴隨恆等式）
learning_goal: 看出 cosine 走完全相同的機制（只換一條恆等式），導數是 −sin。
kind: theorem
narration: |
  Cosine falls to the very same machinery — only the identity changes. This
  time use $\cos A-\cos B=-2\sin\frac{A+B}{2}\sin\frac{A-B}{2}$. With $A=x+h$
  and $B=x$, the difference quotient becomes
  $-\sin\!\left(x+\frac h2\right)\cdot\dfrac{\sin(h/2)}{h/2}$. Send $h$ to
  zero: the sine factor goes to $\sin x$ by continuity, the other to one by
  the fundamental limit, and we are left with
  $\dfrac{d}{dx}\cos x=-\sin x$. Same two tools, one extra minus sign — that
  is the derivative of cosine.
visual_need: |
  Theorem 陳述卡（$\tfrac{d}{dx}\cos x=-\sin x$）＋證明鏈：
  $\tfrac{\cos(x+h)-\cos x}{h}=-\sin(x+\tfrac h2)\cdot\tfrac{\sin(h/2)}{h/2}\to-\sin x$。
animation_cue: （無——靜態陳述＋證明鏈即可；setup 走 repeat-pattern，不重述）
```

---

### unit: slope_equals_height

```
id: slope_equals_height
source: chapter3-print-standalone.html §3.1 · Figure 3.3（data-fig: sin-cos-slope；sin'=cos 讀成 slope=height）
learning_goal: 在圖上看見「sin 的切線斜率 ＝ cos 的高度」，把 Theorem 3.1 視覺化。
kind: visual
narration: |
  Here is what $\sin'=\cos$ looks like on the graph. Draw $y=\sin x$, and
  check the slope of its tangent at a few points. At $x=0$ the sine curve is
  climbing at slope one. At $x=\frac\pi2$, the top of the hump, the tangent
  is flat — slope zero. At $x=\pi$ it is falling at slope minus one. Now lay
  $y=\cos x$ on top and read its heights at those same points: one, zero,
  minus one. They match exactly. The slope of sine at each $x$ is the height
  of cosine right there — that is the theorem, drawn. And one more derivative
  tips cosine down to $-\sin x$, which is where the next idea comes from.
visual_need: |
  同框 $y=\sin x$（實）與 $y=\cos x$（虛）；在 x=0,π/2,π 對 sin 畫切線段，
  標斜率 1,0,−1；cos 在那三點放點、標高度 1,0,−1，一一對上「斜率＝高度」。
animation_cue: |
  建議動畫：先 trace 出 sin x。在 x=0、π/2、π 依序畫出切線小段、標其斜率
  1／0／−1。再 trace 出 cos x（虛線），在同樣三個 x 放實心點、標高度
  1／0／−1，用同色/引線把「sin 的斜率」對到「cos 的高度」上，凸顯兩者相等。
```

---

### unit: derivative_cycle

```
id: derivative_cycle
source: chapter3-print-standalone.html §3.1 · Remark 3.1（sin/cos 的四步導數循環；呼應 §2.4 e^x 自我複製）
learning_goal: 看出微分把 sin、cos 循環送進彼此，四步回到原點（d⁴/dx⁴ sin = sin）。
kind: proposition
narration: |
  Step back and watch the pattern. Differentiation sends sine and cosine into
  each other, with a minus sign that turns over on every second step. Writing
  an arrow for one derivative: $\sin x \to \cos x \to -\sin x \to -\cos x \to
  \sin x$. Four derivatives, and you are back where you started — so the
  fourth derivative of sine is sine again, and the same holds for cosine.
  Where $e^x$ reproduces itself in a single step, sine and cosine reproduce
  themselves in a cycle of four. It is a kind of self-renewal — and it is
  exactly what lets these functions describe motion that oscillates forever
  without ever winding down.
visual_need: |
  四步循環圖：$\sin x \to \cos x \to -\sin x \to -\cos x \to \sin x$（一個 d/dx 一個箭頭）；
  標 $\tfrac{d^4}{dx^4}\sin x=\sin x$。
animation_cue: |
  （選用）建議動畫：四個節點 sin x、cos x、−sin x、−cos x 排成環，箭頭依序
  點亮（每箭頭＝一次 d/dx），走完四步回到 sin x，凸顯「循環」與「四步歸位」。
```

---

### unit: companion_limit

```
id: companion_limit
source: chapter3-print-standalone.html §3.1 · Example 3.1（伴隨極限 (1−cosθ)/θ → 0）
learning_goal: 用「乘 1+cosθ」把另一個 0/0 極限化成基本極限的形式，得 0。
kind: example
narration: |
  The fundamental limit has a companion worth knowing:
  $\lim_{\theta\to 0}\dfrac{1-\cos\theta}{\theta}=0$. It is again of the form
  zero over zero, and the trick is to multiply top and bottom by
  $1+\cos\theta$. The numerator turns into $1-\cos^2\theta$, which is
  $\sin^2\theta$, so the whole expression rearranges into
  $\dfrac{\sin\theta}{\theta}\cdot\dfrac{\sin\theta}{1+\cos\theta}$. Now let
  $\theta\to 0$. The first factor goes to one, by the limit we just proved;
  the second goes to $\dfrac{0}{1+1}$, which is zero. One times zero is zero —
  and there is the companion limit.
visual_need: |
  推導鏈：$\tfrac{1-\cos\theta}{\theta}=\tfrac{1-\cos^2\theta}{\theta(1+\cos\theta)}
  =\tfrac{\sin^2\theta}{\theta(1+\cos\theta)}=\tfrac{\sin\theta}{\theta}\cdot
  \tfrac{\sin\theta}{1+\cos\theta}\to1\cdot0=0$。
animation_cue: （無——靜態推導鏈即可）
```

---

### unit: all_six_trig_derivatives

```
id: all_six_trig_derivatives
source: chapter3-print-standalone.html §3.1 · Example 3.2（tan'、sec' 用商法則；cot'、csc' 同法帶過）
learning_goal: 用商法則把 sin'/cos' 推到其餘四個三角函數，補齊全部六個導數。
kind: example
narration: |
  With sine and cosine handled, the other four trig functions cost almost
  nothing — just the quotient rule. Take $\tan x=\dfrac{\sin x}{\cos x}$. The
  quotient rule gives $\dfrac{\cos x\cos x-\sin x(-\sin x)}{\cos^2 x}$, and
  the numerator is $\cos^2 x+\sin^2 x$, which is one. So
  $\dfrac{d}{dx}\tan x=\dfrac{1}{\cos^2 x}=\sec^2 x$. Secant is the same idea
  on $\dfrac{1}{\cos x}$: the quotient rule lands
  $\dfrac{d}{dx}\sec x=\sec x\tan x$. And the very same move on $\cot x$ and
  $\csc x$ gives $-\csc^2 x$ and $-\csc x\cot x$. That completes the
  derivatives of all six trigonometric functions — every one of them riding
  on $\sin'=\cos$ and $\cos'=-\sin$.
visual_need: |
  推導：$\tfrac{d}{dx}\tan x=\tfrac{\cos^2x+\sin^2x}{\cos^2x}=\sec^2x$；
  $\tfrac{d}{dx}\sec x=\sec x\tan x$；帶過 $\cot'=-\csc^2x$、$\csc'=-\csc x\cot x$。
animation_cue: （無——靜態推導即可；cot/csc 走 repeat-pattern 帶過）
```

---

### unit: shm_compute

```
id: shm_compute
source: chapter3-print-standalone.html §3.1 · Example 3.3（彈簧 s(t)=sin t，求 s'、s''，得 s''=−s）
learning_goal: 只用 sin'/cos' 算出速度與加速度，發現加速度等於負的高度——簡諧運動的簽名。
kind: example
narration: |
  Let us put the new derivatives to work on something moving. A weight
  bobbing on a spring sits at height $s(t)=\sin t$ above its rest level.
  Velocity is the derivative of height, so $s'(t)=\cos t$; acceleration is
  the derivative of velocity, so $s''(t)=-\sin t$. But $-\sin t$ is just
  $-s(t)$ — the acceleration is the negative of the height. So at every
  instant the weight is pushed back toward rest, and harder the farther it
  has strayed. That relation, $s''=-s$, is the signature of simple harmonic
  motion. And it is no accident that sine and cosine — the functions whose
  second derivative is their own negative — are exactly the ones that
  describe oscillation.
visual_need: |
  $s(t)=\sin t$ → $s'(t)=\cos t$ → $s''(t)=-\sin t=-s(t)$；標出簽名 $s''=-s$。
animation_cue: （無——靜態推導即可；幾何面交給 shm_stacked_graphs）
```

---

### unit: shm_stacked_graphs

```
id: shm_stacked_graphs
source: chapter3-print-standalone.html §3.1 · Figure 3.4（data-fig: shm-triple；s/s'/s'' 三層堆疊，s''=−s 鏡像）
learning_goal: 在三層共軸的圖上看見「峰谷處速度過零」與「加速度＝高度上下翻」＝ s''=−s。
kind: visual
narration: |
  Stack the three graphs over one time axis and the relationship jumps out.
  On top, the height $s=\sin t$. In the middle, the velocity $s'=\cos t$. On
  the bottom, the acceleration $s''=-\sin t$. Watch the dashed lines where the
  height hits a peak or a trough — at those instants the velocity, in the
  middle graph, is passing through zero, because at the extremes the weight
  momentarily stops. Now hold the bottom graph against the top: it is the top
  one flipped upside down. That is $s''=-s$, drawn — acceleration mirroring
  height, the very picture of an oscillation.
visual_need: |
  三層共用一條時間軸 t∈[0,2π]：頂 $s=\sin t$、中 $s'=\cos t$、底 $s''=-\sin t$；
  t=π/2、3π/2 拉垂直虛線（頂峰/谷 ↔ 中圖過零）；底圖＝頂圖上下翻（$s''=-s$）。
animation_cue: |
  建議動畫：三個小圖垂直堆疊、共用時間軸。依序 trace 出 s（頂）、s'（中）、
  s''（底）。在 t=π/2、3π/2 落下垂直虛線，凸顯頂圖峰/谷處中圖正好過零。
  最後把底圖與頂圖並比（或底圖由頂圖翻摺生成），點出 s''=−s 的上下鏡射。
```

---

### unit: toward_the_chain_rule

```
id: toward_the_chain_rule
source: chapter3-print-standalone.html §3.1 · 收尾散文（forward-ref：只能微分裸三角函數，sin(x²) 等需連鎖律）
learning_goal: 認清目前只能微分「裸」三角函數，要處理 sin(x²) 之類的合成需要下一個工具。
kind: forward_ref
narration: |
  We can now differentiate every trigonometric function — but only in its
  bare form. We can handle $\sin x$, yet not $\sin(x^2)$ or $\sin(3x+1)$,
  where the angle is itself a function tucked inside. To reach a function
  buried inside another, we need one more rule: a way to differentiate a
  composition. That rule is the chain rule, and it is what comes next — and
  with it, every derivative we found today becomes the seed of a whole family
  more.
visual_need: |
  對比：能做 $\sin x$；不能直接做 $\sin(x^2)$、$\sin(3x+1)$（角度是內層函數）→
  指向「下一個工具：連鎖律」。MUST NOT 報節號。
animation_cue: （無——靜態即可）
```

---

### unit: recap

```
id: recap
source: chapter3-print-standalone.html §3.1（全節重點凝煉；Key Takeaways 單元，有旁白）
learning_goal: 把本節串成一條線——一個極限 → 兩個導數 → 其餘四個 → 四步循環 → 全靠弧度。
kind: recap
narration: |
  Pull the section together. Everything grew from one limit:
  $\dfrac{\sin\theta}{\theta}\to 1$ as $\theta\to 0$, which we cracked not
  with algebra but by squeezing it between $\cos\theta$ and one on the unit
  circle. That limit, together with the continuity of sine and cosine, gave
  the two derivatives at the heart of the section: $\sin'=\cos$ and
  $\cos'=-\sin$. From those two, the quotient rule delivered all the other
  trig derivatives. Keep the cycle in mind — differentiating runs
  $\sin\to\cos\to-\sin\to-\cos$ and back around, so the fourth derivative
  brings you home. And remember the fine print: all of it depends on
  measuring angles in radians.
visual_need: |
  Key Takeaways 卡片（5 點）＋ remember-formula 卡：
  points：
    • 基本極限：$\sin\theta/\theta \to 1$（θ→0），靠單位圓上的夾擠證得。
    • $\tfrac{d}{dx}\sin x=\cos x$、$\tfrac{d}{dx}\cos x=-\sin x$。
    • 由這兩個＋商法則，得全部六個三角函數的導數。
    • 導數四步循環：$\sin\to\cos\to-\sin\to-\cos\to\sin$。
    • 一切以弧度為前提。
  formulas（保持短，避免出框）：
    • $\lim_{\theta\to0}\dfrac{\sin\theta}{\theta}=1$
    • $\dfrac{d}{dx}\sin x=\cos x,\quad \dfrac{d}{dx}\cos x=-\sin x$
animation_cue: （無——靜態卡片即可）
```

---

### unit: outro

```
id: outro
source: chapter3-print-standalone.html §3.1（節末品牌字卡）
learning_goal: （收尾；無教學內容）
kind: recap
narration: （無——outro 為純動畫，無 takeaways）
visual_need: 兩段式 outro——暗轉亮橋接 → 最終 logo／節號／標題字卡（Next 3.2 The Chain Rule）。
animation_cue: （由 outro 模板處理）
```

---

## §7 拆解註記與內容層品質檢核

### 拆解／折疊決策（就近註明，杜絕 silent drop）

- **N1 — 開節「angles in radians」預告句折疊進 `why_trig_is_different` 收尾。** 講義開節有一句「Throughout this section angles are measured in radians; this assumption turns out to be essential, as we note below」作為預告；其**完整處理**＝ `radians_essential`（Caution②）。預告以一句口語「One ground rule … angles are measured in radians」承接，full caution 留在 unit 9，不重複。
- **N2 — 偶函數論證（sinθ/θ 為偶、故只看 θ>0）折疊進 `sector_inequality` lead-in。** 講義在 Figure 3.1 前的散文先講「Because both θ and sinθ reverse sign … it is even … enough to treat θ>0」；此為 figure 的動機，折進該視覺單元開頭最自然。
- **N3 — cot′、csc′ 折疊進 `all_six_trig_derivatives`（repeat-pattern 帶過）。** 講義 Example 3.2 末句以「The same technique … gives cot′=−csc²x and csc′=−csc x cot x」帶過；同商法則、無新技巧，旁白以「the very same move … gives」一句涵蓋（§4 repeat-pattern），不另立單元。
- **N4 — 各段 expansion:intuition 過渡散文折進鄰接單元 lead-in（無 silent drop）：** 「With continuity secured, we can finally squeeze …」→ `fundamental_limit` lead-in；「With continuity and the fundamental limit in hand …」→ `derivative_of_sine` lead-in；「Cosine yields to the very same machinery …」→ `derivative_of_cosine` lead-in；「The bound … is also what makes sine and cosine continuous」→ `continuity_of_sin_cos` lead-in。
- **連續性證明（Prop 3.1）未拆 statement/proof：** 證明邏輯鏈為「界→squeeze→limit sinθ=0；sum-to-product 界住差→squeeze→連續」，旁白走邏輯鏈（非逐行代數），單一 `theorem` 單元承載得下、不超載，故不拆（CONTENT_METHODOLOGY §3「證明超過~4 步才拆」的判準下屬可不拆）。
- **兩個 Caution 各自獨立成單元（未折疊）：** `limit_not_identity`（極限≠恆等式）與 `radians_essential`（弧度制）各自是獨立教學點（標準誤解／結構性前提），非 1–3 句順帶提醒，故依 §3「自成教學點才獨立」各立一單元（kind: counterexample——皆為「破壞天真假設」的反向警示）。

### 例題：代表式涵蓋（§2；無同型 silent drop）

- 三個 example 各帶不同模式，全數納入：Ex 3.1 伴隨極限（另一個 0/0、不同代數技巧＝乘共軛）／Ex 3.2 用商法則推其餘四個三角導數（新手法：把 sin'/cos' 外推）／Ex 3.3 簡諧運動（application：只用 sin'/cos'、引出 s''=−s）。**無同型折疊**。

### 散文歸類（§3，無 silent drop）

- 開節三段散文（差分商卡 0/0、radian 預告、difference-quotient 子節）→ `why_trig_is_different`（motivation）＋ `difference_quotient_for_sine`（derivation）。
- Figure 3.1 前的面積/偶函數散文 → `sector_inequality` lead-in（N2）。
- 「The bound … makes sine and cosine continuous」→ `continuity_of_sin_cos` lead-in。
- 「With continuity secured …」→ `fundamental_limit` lead-in（N4）。
- 「With continuity and the fundamental limit in hand …」→ `derivative_of_sine` lead-in（N4）。
- 「Cosine yields to the very same machinery …」→ `derivative_of_cosine` lead-in（N4）。
- 收尾段「We can now differentiate every trig function … but only in its bare form … the chain rule」→ `toward_the_chain_rule`（forward-pointing，獨立成單元，§3；**不報節號**）。

### 視覺／動畫盤點（§5；§3.1 約 50% 符號，medium——不套 symbol-heavy 例外，幾何吃重）

- 四張講義圖全覆蓋：Figure 3.1（sector-inequality）→ `sector_inequality`（**客製 hook**）；Figure 3.2（squeeze-limit）→ `squeeze_graph`（stock graph）；Figure 3.3（sin-cos-slope）→ `slope_equals_height`（**客製 hook**）；Figure 3.4（shm-triple）→ `shm_stacked_graphs`（**客製 hook**，graph 無原生 3-up）。
- 3 個吃重 `animation_cue`（會動的概念才動，§5「Animate, not just display」）：sector_inequality（三嵌套面積逐層比較）、slope_equals_height（切線斜率 ↔ cos 高度對應）、shm_stacked_graphs（三層共軸 ＋ 上下翻鏡射）。另 squeeze_graph、derivative_cycle 為輕量／選用動畫（stock 或可省）。生成的 manim code 視同 narration，**經使用者認可才定版**（§5），render 失敗走「由小到大逐層修補」。

### 內容層 checklist（§7）

- [ ] 每個 proposition（3.1、3.2）／theorem（3.1、3.2）有單元覆蓋；每個不同模式 example（3.1–3.3）有代表單元，無同型 silent drop。
- [ ] 無 exercise 內容洩入（本節 fragment 無 env-exercise；自著題已寫成 worked example）。
- [ ] intro（定位＋tagline）／recap（5 點 takeaway）／outro（無 takeaways）齊備。
- [ ] 散文幾何主張（單位圓面積、slope=height、SHM 鏡射）皆有視覺單元；其餘散文皆歸類折疊／升格，無 silent drop。
- [ ] 每段環境之間散文已歸類（Incorporative／Bridge／Forward-pointing）。
- [ ] narration 為「說」而寫：開頭 hook、結尾 takeaway、未犯 §4 禁則（不報節號／圖號、不念螢幕標題、不用 see/as shown）、cosine 導數＋cot/csc repeat-pattern 省 setup。
- [ ] 數學讀得順（直讀 LaTeX 或白話；對齊鏈不重念 LHS；f^{-1}、下標等口語攤平屬 .spoken.yml，不污染正典）。
- [ ] 動畫建議用自然語言、聚焦教學意圖（3 客製 hook 由 Claude 依此生成、經認可定版）。
- [ ] 每個 id 唯一、snake_case、描述教學重點。
- [x] **六鏡稽核 → 收斂（Workflow `wf_5d6bb72f-2c1`，6 鏡並行 refute-by-default 複驗）：raw 0、blocking==0、advisory==0。** L5 數學鏡盲算獨立重算 11 組（sum-to-product 化簡／三塊面積與嵌套／不等式取倒數翻向／連續性界／基本極限／sin'=cos·cos'=−sin／伴隨極限／六導數商法則／SHM s''=−s／弧度→度數 π/180／2π≈0.64、sinπ/π=0）全 match；作者另獨立 spot-check 最易錯數組佐證。六鏡乾淨＝忠實/拆解/語域/不重複/完整皆無 blocking。
- [x] **散文潤稿 pass（gate1 `narration-copyedit`，鎖稿前）：0 blocking、5 tighten＋6 optional（全 advisory）；採納 6 條純措辭緊縮**（why_trig 去「no amount of」、difference_quotient「about to do something」→「each one moves」、limit_not_identity 去「all the way」、sector_inequality「Before the figure」→「First」、shm_compute 拆長句、recap 去「Let us」cross-unit echo）。declines：radians_essential 四次「radians」為結構性警示刻意強調／continuity「in size」是 magnitude 精確性／derivative_cycle 拆句與 shm「Let us」屬可有可無。語義/數學未動。
- [x] **已編譯 `ch03_trig_derivatives_narration.html` 審核稿**（Task 5；採納 copyedit 後重編）。
- [x] **旁白 sign-off（使用者，2026-06-28）：通過 → LOCKED。** 下一步：Stage 2 工程稿 `ch03_trig_derivatives.yml`（模板化、`{show}`／accent／payload）＋ 3 客製 hook（Fig 3.1/3.3/3.4）→ schema/lint/sizecheck → mock render → 視覺稽核 → HTML 報告。MiMo 口語軌＋NFA＋TTS（計費）屆時另徵同意。
