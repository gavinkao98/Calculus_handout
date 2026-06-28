# §3.1 Derivatives of Sine and Cosine — 影片內容稿（content script）

> **產線：** 講義 → 影片，gen-2。Chapter 3 第一節，從 HTML 講義逐節重跑。
> **權威來源：** [`../../handout/fragments/ch03/sec-3-1.html`](../../handout/fragments/ch03/sec-3-1.html)（建置版 `handout/chapter3-print-standalone.html` §3.1）。
> **這是什麼：** 純內容中間產物（source of truth）。格式見 [`../CONTENT_METHODOLOGY.md`](../CONTENT_METHODOLOGY.md) §6——只含 `id`／`source`／`learning_goal`／`kind`／`narration`／`visual_need`／`animation_cue`，**不含**任何工程欄位（template／`{show}`／accent／payload／divider）。工程是第二階段的事。
> **階段：** **LOCKED（detail-redo，2026-06-29 使用者 sign-off；`CONTENT_APPROVED=yes`）**——使用者裁決「影片講解最大詳細、少省略；選材可少但講解要清楚」，全節重拆旁白＋visual_need（第1檔忠實全展開為基準＋4 樞紐加第2檔直覺鷹架），continuity 拆 2 單元、把畫面承載步驟（和差化積來源、`lim_{h→0}` setup、sec′ 步驟）補上。**取代前一次 LOCK**（2026-06-28 sign-off 的壓縮版，git 留存）。本輪六鏡（blocking==0、6 鏡 clean、L5 盲算 11 組 match）＋copyedit（7 tighten 全採納）＋使用者 sign-off 已完成 → LOCKED；後續忠實性由 NFA 把關，post-lock 改稿須對動到單元跑 scoped NFA 回歸（§8）。規格／計畫見 [`_audit/SPEC-ch03-s31-detail-redo.md`](_audit/SPEC-ch03-s31-detail-redo.md)／[`_audit/PLAN-ch03-s31-detail-redo.md`](_audit/PLAN-ch03-s31-detail-redo.md)。narration 認可在編譯出的 `_narration.html` 上進行；本 `.md` 為權威，兩者 MUST 一致。

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
learning_goal: 看出三角函數的導數卡在一個代數攻不下的 0/0 極限 sinθ/θ，需要全新的幾何工具。
kind: motivation
narration: |
  Every derivative so far has yielded to algebra. For a polynomial we
  expanded $(x+h)^n$ and the binomial theorem handed us a factor of $h$ to
  cancel; for $e^x$ the power series did the same job. The trigonometric
  functions refuse to play along. Write down the difference quotient for
  $\sin x$ — $\dfrac{\sin(x+h)-\sin x}{h}$ — and try the usual move. You
  cannot simply set $h=0$: that gives $\dfrac{0}{0}$, which tells you
  nothing. And no identity cancels the $h$ in the denominator —
  $\sin(x+h)$ simply does not break into pieces that conveniently subtract.
  As we
  are about to see, the whole computation funnels down to a single limit,
  $\lim_{\theta\to 0}\dfrac{\sin\theta}{\theta}$ — again the indeterminate
  form zero over zero, and one that no algebra will crack. Prying it open
  takes a genuinely new tool: a geometric comparison of areas on the unit
  circle. And once we secure that one limit, it unlocks the derivatives of
  both sine and cosine at once. One ground rule, though: throughout, angles
  are measured in radians — an assumption that turns out to be essential.
visual_need: |
  逐步顯示（每步一個 reveal）：
   1. 差分商 $\dfrac{\sin(x+h)-\sin x}{h}$。
   2. 天真代入 $h=0$ → $\dfrac{0}{0}$（標「indeterminate — 無資訊」）。
   3. funnel 指向目標極限 $\displaystyle\lim_{\theta\to 0}\dfrac{\sin\theta}{\theta}$（標 0/0、no algebra）。
  收尾標籤：tool = 單位圓面積比較；ground rule = radians。
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
  So let us transform that difference quotient instead of fighting it
  head-on. The decisive step is one trigonometric identity — sum-to-product —
  which turns a difference of sines into a product:
  $\sin A-\sin B=2\cos\frac{A+B}{2}\sin\frac{A-B}{2}$. A product is exactly
  what we want, because we can pull it apart and take limits one factor at
  a time. Put $A=x+h$ and $B=x$. The numerator becomes
  $2\cos\!\left(x+\frac h2\right)\sin\frac h2$. Now divide by $h$ — and here
  is the small trick that makes everything line up: write $h$ as
  $2\cdot\frac h2$, so the denominator carries the very $\frac h2$ that sits
  inside the sine. The quotient cleans up to
  $\cos\!\left(x+\frac h2\right)\cdot\dfrac{\sin(h/2)}{h/2}$. Look at what we
  have now: a product of two factors, and as $h\to 0$ each one moves on its
  own. The first factor, $\cos\!\left(x+\frac h2\right)$, should slide to
  $\cos x$ — provided cosine is continuous. The second factor is exactly
  $\dfrac{\sin\theta}{\theta}$ in disguise, with $\theta=\frac h2$ shrinking
  to zero. So the entire derivative now hangs on just two facts: that sine
  and cosine are continuous, and the value of that one fundamental limit. We
  secure both, in that order, and then come straight back to finish.
visual_need: |
  推導鏈，逐行 reveal（每行一個 step）：
   1. 恆等式 $\sin A-\sin B=2\cos\tfrac{A+B}{2}\sin\tfrac{A-B}{2}$（理由：sum-to-product）。
   2. 代入 $A=x+h,\ B=x$：$\sin(x+h)-\sin x=2\cos(x+\tfrac h2)\sin\tfrac h2$。
   3. 除以 $h=2\cdot\tfrac h2$：$\dfrac{\sin(x+h)-\sin x}{h}=\cos(x+\tfrac h2)\cdot\dfrac{\sin(h/2)}{h/2}$。
   4. 兩因子標去向：$\cos(x+\tfrac h2)\xrightarrow{\,h\to0\,}\cos x$（需「連續」）；$\dfrac{\sin(h/2)}{h/2}\xrightarrow{\,h\to0\,}?$（即 $\dfrac{\sin\theta}{\theta}$，需「基本極限」）。
  收尾標籤：整個導數 = 兩因子的乘積 → 靠「連續」＋「基本極限」兩件事。
animation_cue: （無——靜態推導鏈即可；兩因子去向用引線/同色標記）
```

---

### unit: sector_inequality

```
id: sector_inequality
source: chapter3-print-standalone.html §3.1 · "A geometric inequality on the unit circle" 散文（含偶函數論證）+ Figure 3.1（data-fig: sector-inequality）
learning_goal: 在單位圓上用三塊嵌套面積，幾何地夾出 sinθ ≤ θ ≤ tanθ。
kind: visual
narration: |
  Here is that new tool. We compare three areas on a circle of radius one.
  But first, one convenience that saves us half the work. Replacing $\theta$
  by $-\theta$ flips the sign of both $\theta$ and $\sin\theta$, so their
  ratio $\sin\theta/\theta$ is left unchanged — it is an even function. That
  means whatever we learn for positive angles holds for negative ones, so it
  is enough to chase $\theta$ down to zero from the positive side. Now the
  geometry. On the unit circle, put $A$ at $(1,0)$ and let $B$ be the point at
  angle $\theta$, so $B=(\cos\theta,\sin\theta)$. Extend the radius until it
  meets the vertical tangent line at $A$, and call that meeting point
  $C=(1,\tan\theta)$. Three regions now nest one inside the next, and each
  area is easy to read off. The inner triangle $OAB$ has base one and height
  $\sin\theta$, so its area is $\frac12\sin\theta$. The circular sector $OAB$
  is the fraction $\theta$ over $2\pi$ of the whole disc, which comes out to
  $\frac12\theta$. And the outer triangle $OAC$ has base one and height
  $\tan\theta$, so its area is $\frac12\tan\theta$. Because each region sits
  strictly inside the next, their areas must line up in the same order:
  $\frac12\sin\theta \le \frac12\theta \le \frac12\tan\theta$. The whole
  argument hangs on that one picture — a triangle inside a sector inside a
  triangle.
visual_need: |
  單位圓（半徑 1），A=(1,0)、B=(cosθ,sinθ)、C=(1,tanθ)、射線 OB 延伸交切線於 C；
  三塊嵌套區域：內接 △OAB、扇形 OAB、外切 △OAC，各標面積 ½sinθ／½θ／½tanθ；
  逐塊高亮（內→中→外）以「一個包一個」成立；浮出 $\tfrac12\sin\theta \le \tfrac12\theta \le \tfrac12\tan\theta$；
  旁標偶函數一句記號 $\sin(-\theta)/(-\theta)=\sin\theta/\theta$（只看 θ>0）。
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
  Now turn that chain of areas into a statement about $\sin\theta/\theta$,
  one careful step at a time. Start by multiplying through by $2$ to clear the
  halves: $\sin\theta \le \theta \le \tan\theta$. Next, divide every part by
  $\sin\theta$, which is positive for these angles, and rewrite $\tan\theta$
  as $\sin\theta/\cos\theta$; that gives
  $1 \le \dfrac{\theta}{\sin\theta} \le \dfrac{1}{\cos\theta}$. We are close,
  but the middle is upside down — it has $\theta$ over $\sin\theta$, and we
  want $\sin\theta$ over $\theta$. So take reciprocals of all three parts. They
  are all positive, and flipping positive quantities reverses the inequalities,
  so the chain turns around and we land exactly on the bound we were after:
  $\cos\theta \le \dfrac{\sin\theta}{\theta} \le 1$, for $\theta$ between zero
  and $\frac\pi2$. One more thing worth pocketing before we move on: the very
  first inequality, $\sin\theta \le \theta$, also gives
  $0 \le |\sin\theta| \le |\theta|$ near zero — a small bound we will lean on
  twice in just a moment.
visual_need: |
  推導鏈，逐行 reveal（每行附理由）：
   1. $\sin\theta\le\theta\le\tan\theta$（理由：面積 ×2）。
   2. $1\le\dfrac{\theta}{\sin\theta}\le\dfrac{1}{\cos\theta}$（理由：÷sinθ>0、$\tan=\tfrac{\sin}{\cos}$）。
   3. $\cos\theta \le \dfrac{\sin\theta}{\theta} \le 1$（理由：取倒數→翻向；限 $0<\theta<\tfrac\pi2$）—— 標為「式 (1)」。
  附帶界（另起一行、標「keep for later」）：$0\le|\sin\theta|\le|\theta|$。
animation_cue: （無——靜態推導鏈即可；翻向那步可短暫強調不等號方向反轉）
```

---

### unit: continuity_statement_sin_limit

```
id: continuity_statement_sin_limit
source: chapter3-print-standalone.html §3.1 · Proposition 3.1（陳述）+ Proof 第一段（|sinθ|≤|θ| + squeeze ⇒ limθ→0 sinθ = 0）
learning_goal: 先抓住「連續＝角度動一點、值只動一點」的直覺，並用 |sinθ|≤|θ| 與夾擠證出 limθ→0 sinθ = 0。
kind: proposition
narration: |
  That little bound does more than help with the limit — it is also the key
  to continuity. And continuity here means something very concrete: nudge the
  angle by a little, and sine and cosine move only a little; they never jump.
  We even have the tool that says so. On the unit circle the half-chord
  $\sin\theta$ is always shorter than the arc $\theta$ above it, which is just
  $|\sin\theta| \le |\theta|$ read geometrically — close up the angle and you
  close up the sine. So here is the claim, made precise: $\sin x$ and $\cos x$
  are continuous at every real $x_0$. Build it from the ground up. Since
  $0 \le |\sin\theta| \le |\theta|$, and $|\theta|$ itself goes to zero as
  $\theta\to 0$, the squeeze theorem pins $|\sin\theta|$ between zero and
  something vanishing, and forces $\sin\theta \to 0$. That single limit,
  $\lim_{\theta\to 0}\sin\theta = 0$, is the seed; the full continuity grows
  straight out of it, which is what we do next.
visual_need: |
  Proposition 陳述卡：$\sin x,\ \cos x$ 在每個 $x_0$ 連續。
  直覺小圖（mini，弦≤弧）：單位圓上半弦 $\sin\theta$ 短於弧 $\theta$ → $|\sin\theta|\le|\theta|$。
  推導（逐行）：
   1. $0\le|\sin\theta|\le|\theta|$，且 $|\theta|\to 0$。
   2. squeeze ⇒ $\displaystyle\lim_{\theta\to 0}\sin\theta = 0$（標為下一場的「seed」）。
animation_cue: |
  （選用）建議動畫：單位圓上同時畫出半弦 $\sin\theta$ 與其上方的弧 $\theta$，讓
  角 θ 收小，弦與弧一起縮向 0，直觀呈現「弦 ≤ 弧、且一起趨 0」＝ $|\sin\theta|\le|\theta|\to0$。
```

---

### unit: continuity_argument

```
id: continuity_argument
source: chapter3-print-standalone.html §3.1 · Proposition 3.1 · Proof 第二段（sum-to-product 界住 |Δcos|、|Δsin| ≤ 2|sin((x−x₀)/2)| → squeeze ⇒ 連續）
learning_goal: 看見連續性如何從「sum-to-product 把函數的變化界住、再夾擠」完整推出——畫面上顯示恆等式來源，界不再憑空出現。
kind: proof
narration: |
  Now turn that seed into full continuity. Fix a point $x_0$, and ask how much
  $\cos x$ and $\sin x$ can change as $x$ moves toward it. Sum-to-product
  answers both at once. For cosine,
  $\cos x-\cos x_0=-2\sin\frac{x-x_0}{2}\sin\frac{x+x_0}{2}$; and for sine,
  $\sin x-\sin x_0=2\cos\frac{x+x_0}{2}\sin\frac{x-x_0}{2}$. In each line one
  factor carries the half-difference $\frac{x-x_0}{2}$, and the other carries
  the half-sum $\frac{x+x_0}{2}$ — and that second factor, a sine or a cosine,
  never exceeds one in size. Drop it to its largest size, one, and both
  differences are bounded by the same thing:
  $|\cos x-\cos x_0|$ and $|\sin x-\sin x_0|$ are each at most
  $2\,|\sin\frac{x-x_0}{2}|$. Now let $x\to x_0$. The half-angle
  $\frac{x-x_0}{2}$ goes to zero, so by the limit we just established that
  bound, $2\,|\sin\frac{x-x_0}{2}|$, collapses to zero. Squeeze one last time,
  and the differences are crushed to nothing: $\cos x\to\cos x_0$ and
  $\sin x\to\sin x_0$. Both functions are continuous everywhere.
visual_need: |
  證明鏈，逐行 reveal——關鍵：和差化積兩條恆等式**顯示在畫面上**（界的來源不再憑空）：
   1. $\cos x-\cos x_0=-2\sin\tfrac{x-x_0}{2}\sin\tfrac{x+x_0}{2}$（理由：sum-to-product）。
   2. $\sin x-\sin x_0=\phantom{-}2\cos\tfrac{x+x_0}{2}\sin\tfrac{x-x_0}{2}$（理由：sum-to-product，伴隨式）。
   3. 半和因子 $\bigl|\sin\tfrac{x+x_0}{2}\bigr|\le1$、$\bigl|\cos\tfrac{x+x_0}{2}\bigr|\le1$ ⇒ $|\cos x-\cos x_0|,\ |\sin x-\sin x_0|\le 2\bigl|\sin\tfrac{x-x_0}{2}\bigr|$。
   4. $x\to x_0 \Rightarrow \tfrac{x-x_0}{2}\to0 \Rightarrow 2\bigl|\sin\tfrac{x-x_0}{2}\bigr|\to0$（用上場 $\sin\theta\to0$）。
   5. squeeze ⇒ $\cos x\to\cos x_0,\ \sin x\to\sin x_0$（QED：兩者連續）。
animation_cue: （無——靜態證明鏈即可；步驟 3 可短暫強調「半和因子被丟成 1」這個放大動作）
```

---

### unit: fundamental_limit

```
id: fundamental_limit
source: chapter3-print-standalone.html §3.1 · Proposition 3.2（lim sinθ/θ = 1）+ Proof
learning_goal: 用 cosθ ≤ sinθ/θ ≤ 1、cosθ→1 與偶函數，夾擠出基本極限等於 1。
kind: proposition
narration: |
  Now we can finally close the limit that started all of this. The claim is
  as clean as it gets: $\lim_{\theta\to 0}\dfrac{\sin\theta}{\theta}=1$. And we
  already built the trap for it. For $\theta$ between zero and $\frac\pi2$, our
  bound reads $\cos\theta \le \dfrac{\sin\theta}{\theta} \le 1$ — the ratio is
  pinned between a floor and a ceiling. The ceiling is the constant one, going
  nowhere. The floor is $\cos\theta$, and now that we know cosine is
  continuous, $\cos\theta \to \cos 0 = 1$ as $\theta\to 0$. So the ratio is
  squeezed between two quantities both heading to one, and has nowhere to go
  but there — at least as $\theta$ approaches from the right. And here the
  even symmetry pays off: because $\sin\theta/\theta$ is unchanged when
  $\theta$ flips sign, its left-hand limit must equal its right-hand limit, so
  the full two-sided limit is one as well. That is the keystone — every result
  in the rest of the section rests on this single value.
visual_need: |
  Proposition 陳述卡：$\displaystyle\lim_{\theta\to0}\dfrac{\sin\theta}{\theta}=1$。
  證明鏈，逐行 reveal：
   1. 式(1)：$\cos\theta\le\dfrac{\sin\theta}{\theta}\le1$（$0<\theta<\tfrac\pi2$）——標「floor / ceiling」。
   2. ceiling $=1$；floor $\cos\theta\to\cos0=1$（理由：cos 連續，上場結果）。
   3. squeeze ⇒ $\dfrac{\sin\theta}{\theta}\to1$（右極限）。
   4. 偶函數 ⇒ 左 = 右 ⇒ 兩側極限 $=1$（標「keystone」）。
animation_cue: （無——靜態陳述＋證明鏈即可；可把 floor/ceiling 兩界向 1 收攏短暫示意）
```

---

### unit: squeeze_graph

```
id: squeeze_graph
source: chapter3-print-standalone.html §3.1 · Figure 3.2（data-fig: squeeze-limit；同一不等式讀成函數圖）
learning_goal: 把基本極限的夾擠看成一張圖——sinθ/θ 被困在 cosθ 與 1 之間，θ=0 處是極限不是值。
kind: visual
narration: |
  It helps to picture that squeeze. Plot the ratio
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
  One caution, because this result is easy to over-read. The statement is
  about the limit as $\theta\to 0$ — it is not an identity. At a fixed angle
  the ratio is generally not one. At $\theta=\frac\pi2$ it is
  $\dfrac{\sin(\pi/2)}{\pi/2}=\dfrac{1}{\pi/2}=\dfrac{2}{\pi}$, about $0.64$;
  and at $\theta=\pi$ it is $\dfrac{0}{\pi}$, which is just zero. The value one
  is reached only in the limit, as $\theta$ shrinks to nothing.
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
  formulas we are about to prove, $\sin'=\cos$ and $\cos'=-\sin$, hold only in
  radians. So radians are not a stylistic choice here — they are what keeps
  the calculus tidy.
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
learning_goal: 把連續與基本極限組裝起來，從差分商一路寫到 sin 的導數是 cos。
kind: theorem
narration: |
  Now the payoff, and it falls into our hands. The claim:
  $\dfrac{d}{dx}\sin x=\cos x$, for every real $x$. Start from the definition —
  the derivative is the limit of the difference quotient,
  $\dfrac{d}{dx}\sin x=\lim_{h\to 0}\dfrac{\sin(x+h)-\sin x}{h}$. But we
  already did the hard algebra: that quotient is
  $\cos\!\left(x+\frac h2\right)\cdot\dfrac{\sin(h/2)}{h/2}$. So the whole job
  is to take the limit of this product as $h\to 0$. The first factor,
  $\cos\!\left(x+\frac h2\right)$, tends to $\cos x$, because cosine is
  continuous — that is exactly what we proved continuity for. The second
  factor is $\dfrac{\sin(h/2)}{h/2}$, which is our fundamental limit with
  $\theta=\frac h2$, so it tends to one. A continuous thing times a limit:
  the product tends to $\cos x$ times one, which is simply $\cos x$. The
  derivative of sine is cosine.
visual_need: |
  Theorem 陳述卡：$\dfrac{d}{dx}\sin x=\cos x$（for all real $x$）。
  證明鏈，逐行 reveal（補回 setup 行）：
   1. $\dfrac{d}{dx}\sin x=\displaystyle\lim_{h\to0}\dfrac{\sin(x+h)-\sin x}{h}$（理由：定義）。
   2. $=\displaystyle\lim_{h\to0}\cos\!\left(x+\tfrac h2\right)\cdot\dfrac{\sin(h/2)}{h/2}$（理由：前面化簡）。
   3. $\cos(x+\tfrac h2)\to\cos x$（連續）；$\dfrac{\sin(h/2)}{h/2}\to1$（基本極限，$\theta=\tfrac h2$）。
   4. $=\cos x\cdot1=\cos x$（QED）。
animation_cue: （無——靜態陳述＋證明鏈即可）
```

---

### unit: derivative_of_cosine

```
id: derivative_of_cosine
source: chapter3-print-standalone.html §3.1 · Theorem 3.2（d/dx cos x = −sin x）+ Proof（伴隨恆等式）
learning_goal: 看出 cosine 走完全相同的機制（只換一條伴隨恆等式），導數是 −sin。
kind: theorem
narration: |
  Cosine falls to the very same machinery — only the identity changes, so we
  go quickly. This time use the companion sum-to-product formula,
  $\cos A-\cos B=-2\sin\frac{A+B}{2}\sin\frac{A-B}{2}$. With $A=x+h$ and
  $B=x$, the same division by $h=2\cdot\frac h2$ turns the difference quotient
  into $-\sin\!\left(x+\frac h2\right)\cdot\dfrac{\sin(h/2)}{h/2}$. Send $h$ to
  zero. The sine factor goes to $\sin x$ by continuity, the second factor goes
  to one by the fundamental limit, and the leading minus sign comes along for
  the ride — leaving $\dfrac{d}{dx}\cos x=-\sin x$. Same two tools, one extra
  minus sign. That is the derivative of cosine.
visual_need: |
  Theorem 陳述卡：$\dfrac{d}{dx}\cos x=-\sin x$（for all real $x$）。
  證明鏈，逐行 reveal——關鍵：**顯示伴隨恆等式**（唯一的新東西）：
   1. $\cos A-\cos B=-2\sin\tfrac{A+B}{2}\sin\tfrac{A-B}{2}$（理由：companion 恆等式）。
   2. $\dfrac{\cos(x+h)-\cos x}{h}=-\sin\!\left(x+\tfrac h2\right)\cdot\dfrac{\sin(h/2)}{h/2}$（理由：除以 $h=2\cdot\tfrac h2$）。
   3. $-\sin(x+\tfrac h2)\to-\sin x$（連續）；$\dfrac{\sin(h/2)}{h/2}\to1$（基本極限）。
   4. $=-\sin x$（QED）。
animation_cue: （無——靜態陳述＋證明鏈即可；differece-quotient setup 走 repeat-pattern、不重述，只顯示新恆等式那行）
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
  climbing at slope one. At $x=\frac\pi2$, the top of the hump, the tangent is
  flat — slope zero. At $x=\pi$ it is falling at slope minus one. Now lay
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
learning_goal: 看出微分把 sin、cos 循環送進彼此，四步回到原點（d⁴/dx⁴ sin = sin），並對照 e^x 的一步自我複製。
kind: proposition
narration: |
  Step back and watch the pattern these two derivatives make. Differentiation
  sends sine and cosine into each other, with a minus sign that turns over on
  every second step. Writing an arrow for one derivative:
  $\sin x \to \cos x \to -\sin x \to -\cos x \to \sin x$. Four derivatives,
  and you are back exactly where you started — so the fourth derivative of
  sine is sine again, and likewise for cosine. Compare that with $e^x$, which
  reproduces itself in a single step; sine and cosine reproduce themselves in
  a cycle of four. That is a kind of self-renewal, and it is exactly what lets
  these functions describe motion that oscillates forever without ever winding
  down — which is the application we turn to next.
visual_need: |
  四步循環圖：$\sin x \to \cos x \to -\sin x \to -\cos x \to \sin x$（一個 d/dx 一個箭頭）；
  標 $\tfrac{d^4}{dx^4}\sin x=\sin x$；旁標對照 $e^x$ 一步自我複製（$\tfrac{d}{dx}e^x=e^x$）。
animation_cue: |
  （選用）建議動畫：四個節點 sin x、cos x、−sin x、−cos x 排成環，箭頭依序
  點亮（每箭頭＝一次 d/dx），走完四步回到 sin x，凸顯「循環」與「四步歸位」；
  可在一旁放 e^x 的自我箭頭（一步即回）作對照。
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
  zero over zero, so we need a way in. The trick is to multiply top and bottom
  by $1+\cos\theta$ — the conjugate — which turns the numerator into a
  difference of squares: $(1-\cos\theta)(1+\cos\theta)=1-\cos^2\theta$. And
  $1-\cos^2\theta$ is just $\sin^2\theta$. So the expression becomes
  $\dfrac{\sin^2\theta}{\theta(1+\cos\theta)}$, which we split deliberately
  into two familiar pieces:
  $\dfrac{\sin\theta}{\theta}\cdot\dfrac{\sin\theta}{1+\cos\theta}$. Now let
  $\theta\to 0$. The first factor goes to one, by the fundamental limit we
  just proved. The second goes to $\dfrac{0}{1+1}$, which is zero. One times
  zero is zero — and there is the companion limit.
visual_need: |
  推導鏈，逐行 reveal（每步附理由）：
   1. $\dfrac{1-\cos\theta}{\theta}=\dfrac{(1-\cos\theta)(1+\cos\theta)}{\theta(1+\cos\theta)}=\dfrac{1-\cos^2\theta}{\theta(1+\cos\theta)}$（理由：乘共軛 1+cosθ）。
   2. $=\dfrac{\sin^2\theta}{\theta(1+\cos\theta)}=\dfrac{\sin\theta}{\theta}\cdot\dfrac{\sin\theta}{1+\cos\theta}$（理由：$1-\cos^2\theta=\sin^2\theta$、拆兩因子）。
   3. $\to 1\cdot\dfrac{0}{1+1}=0$（理由：基本極限 + 連續）。
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
  With sine and cosine in hand, the other four trig functions cost almost
  nothing — they are all just the quotient rule. Take $\tan x$, which is
  $\dfrac{\sin x}{\cos x}$. The quotient rule gives
  $\dfrac{(\cos x)(\cos x)-(\sin x)(-\sin x)}{\cos^2 x}$, and the numerator is
  $\cos^2 x+\sin^2 x$, which the Pythagorean identity collapses to one. So
  $\dfrac{d}{dx}\tan x=\dfrac{1}{\cos^2 x}=\sec^2 x$. Secant is the same idea
  on $\dfrac{1}{\cos x}$: the quotient rule, with a constant on top, gives
  $\dfrac{0\cdot\cos x-1\cdot(-\sin x)}{\cos^2 x}=\dfrac{\sin x}{\cos^2 x}$,
  which we read as $\dfrac{1}{\cos x}\cdot\dfrac{\sin x}{\cos x}=\sec x\tan x$.
  And the very same move on $\cot x=\dfrac{\cos x}{\sin x}$ and
  $\csc x=\dfrac{1}{\sin x}$ gives $-\csc^2 x$ and $-\csc x\cot x$. That
  completes the derivatives of all six trigonometric functions — every one
  built on $\sin'=\cos$ and $\cos'=-\sin$.
visual_need: |
  推導，逐行 reveal（tan、sec 完整顯示步驟；cot、csc repeat-pattern 帶過）：
   1. $\dfrac{d}{dx}\tan x=\dfrac{(\cos x)(\cos x)-(\sin x)(-\sin x)}{\cos^2 x}$（理由：商法則於 $\tfrac{\sin}{\cos}$）。
   2. $=\dfrac{\cos^2 x+\sin^2 x}{\cos^2 x}=\dfrac{1}{\cos^2 x}=\sec^2 x$（理由：Pythagorean）。
   3. $\dfrac{d}{dx}\sec x=\dfrac{0\cdot\cos x-1\cdot(-\sin x)}{\cos^2 x}=\dfrac{\sin x}{\cos^2 x}=\sec x\tan x$（理由：商法則於 $\tfrac1{\cos}$）。
   4. （帶過）$\dfrac{d}{dx}\cot x=-\csc^2 x,\quad \dfrac{d}{dx}\csc x=-\csc x\cot x$（理由：同手法）。
animation_cue: （無——靜態推導即可；cot/csc 走 repeat-pattern 帶過。若容量溢出，Stage 2 可拆 tan/sec 與 cot/csc 兩場、設 part:）
```

---

### unit: shm_compute

```
id: shm_compute
source: chapter3-print-standalone.html §3.1 · Example 3.3（彈簧 s(t)=sin t，求 s'、s''，得 s''=−s）
learning_goal: 只用 sin'/cos' 算出速度與加速度，發現加速度等於負的高度——簡諧運動的簽名。
kind: example
narration: |
  Let us put the new derivatives to work on something that moves. A weight
  bobbing on a spring sits at height $s(t)=\sin t$ above its rest level.
  Velocity is the derivative of height, so $s'(t)=\cos t$. Acceleration is the
  derivative of velocity, so $s''(t)=-\sin t$. But look at that last line:
  $-\sin t$ is just $-s(t)$. The acceleration is the negative of the height.
  So at every instant the weight is pushed back toward rest, and harder the
  farther it has strayed. That relation, $s''=-s$, is the signature of simple
  harmonic motion. And it is no accident that sine and cosine — the functions
  whose second derivative is their own negative — are exactly the ones that
  describe oscillation.
visual_need: |
  推導，逐行 reveal：
   1. $s(t)=\sin t$（height）。
   2. $s'(t)=\cos t$（velocity）。
   3. $s''(t)=-\sin t$（acceleration）。
   4. $-\sin t=-s(t)$ ⇒ $s''=-s$（標「signature of SHM」）。
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
  We can now differentiate every trigonometric function — but only in its bare
  form. We can handle $\sin x$, yet not $\sin(x^2)$ or $\sin(3x+1)$, where the
  angle is itself a function tucked inside. To reach a function buried inside
  another, we need one more rule: a way to differentiate a composition. That
  rule is the chain rule, and it is what comes next — and with it, every
  derivative we found today becomes the seed of a whole family more.
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
  $\dfrac{\sin\theta}{\theta}\to 1$ as $\theta\to 0$, which we cracked not with
  algebra but by squeezing it between $\cos\theta$ and one on the unit circle.
  That limit, together with the continuity of sine and cosine, gave the two
  derivatives at the heart of the section: $\sin'=\cos$ and $\cos'=-\sin$.
  From those two, the quotient rule delivered all the other trig derivatives.
  Keep the cycle in mind — differentiating runs
  $\sin\to\cos\to-\sin\to-\cos$ and back around, so the fourth derivative
  brings you home. And remember the fine print: all of it depends on measuring
  angles in radians.
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

### detail-redo（2026-06-29）相對前版的結構變動

- **continuity 拆 2 單元（D2 旗艦改造）：** 前版 `continuity_of_sin_cos` 為單一 `theorem` 單元、旁白走「邏輯鏈」、畫面只擺 2–3 行骨架（界 `2|sin((x−x₀)/2)|` 在畫面上憑空出現——2026-06-29 密度稽核標出的唯一真缺口）。本版拆成 `continuity_statement_sin_limit`（陳述＋`limθ→0 sinθ=0`＋第2檔「弦≤弧」直覺）＋ `continuity_argument`（**畫面顯示和差化積兩條恆等式**＋界＋squeeze ∎），讓界有可見來源。**此舉取代前版 §7「連續性證明未拆」之決策**（該決策在「畫面只放骨架」前提下成立；改為第1檔全展開後，完整證明含兩條恆等式逐行，單頁過載，依 CONTENT_METHODOLOGY §3「>4 步拆 statement/proof」拆場）。
- **第1檔忠實全展開（基準）：** 所有 proof/derivation 的 `visual_need` 改為**逐行列出畫面要顯示的承載步驟**（含理由），不再只寫「邏輯鏈」。具體補回：`derivative_of_sine` 的 `lim_{h→0}` 定義 setup 行；`derivative_of_cosine` 的伴隨恆等式行；`all_six_trig_derivatives` 的 sec′ 商法則步驟。Stage 2 據此把每步搬上畫面、超頁走 `part:`。
- **第2檔直覺鷹架（僅 4 樞紐）：** `difference_quotient_for_sine`（「product 才能逐因子取極限」的動機）、`sector_inequality`（偶函數＋三嵌套「一個包一個」）、`continuity_statement_sin_limit`（「角度動一點、值只動一點」＋弦≤弧小圖）、`fundamental_limit`（floor/ceiling 向 1 收攏）。**硬護欄：不增刪任何數學**（CONTENT_METHODOLOGY §1）——所有新增為呈現/直覺，數學內容仍逐單元回溯講義。
- **chord≤arc 小圖折進 `continuity_statement_sin_limit`（不另立場景）：** `|sinθ|≤|θ|` 的幾何直覺（弦短於弧）作為該單元的 mini-visual 與第2檔開場，不獨立成場（避免與 `sector_inequality` 已建立的 `sinθ≤θ` 重複）。
- **選材全保留（D3）：** companion limit／all-six／SHM 三個不同模式全留，無折疊（只把講解加詳）。

### 拆解／折疊決策（就近註明，杜絕 silent drop）

- **N1 — 開節「angles in radians」預告句折進 `why_trig_is_different` 收尾。** full caution 留在 `radians_essential`，預告以一句承接、不重複。
- **N2 — 偶函數論證折進 `sector_inequality` lead-in。** 講義在 Figure 3.1 前散文先講「even … enough to treat θ>0」，為 figure 動機，折進該視覺單元開頭。
- **N3 — cot′、csc′ 折進 `all_six_trig_derivatives`（repeat-pattern 帶過）。** 同商法則、無新技巧，旁白以「the very same move … gives」一句涵蓋，不另立單元。
- **N4 — expansion:intuition 過渡散文折進鄰接單元 lead-in（無 silent drop）：** 「With continuity secured …」→ `fundamental_limit`；「With continuity and the fundamental limit in hand …」→ `derivative_of_sine`；「Cosine yields to the very same machinery …」→ `derivative_of_cosine`；「The bound … makes sine and cosine continuous」→ `continuity_statement_sin_limit`。
- **兩個 Caution 各自獨立成單元（未折疊）：** `limit_not_identity`、`radians_essential` 各為獨立教學點（標準誤解／結構性前提），依 §3「自成教學點才獨立」各立一單元（kind: counterexample）。

### 例題：代表式涵蓋（§2；無同型 silent drop）

- 三個 example 各帶不同模式，全數納入：Ex 3.1 伴隨極限（另一個 0/0、乘共軛）／Ex 3.2 商法則推其餘四個三角導數（新手法：外推 sin'/cos'）／Ex 3.3 簡諧運動（application：只用 sin'/cos'、引出 s''=−s）。**無同型折疊**。

### 視覺／動畫盤點（§5；§3.1 約 50% 符號，medium——不套 symbol-heavy 例外，幾何吃重）

- 四張講義圖全覆蓋：Figure 3.1 → `sector_inequality`（**客製 hook**）；Figure 3.2 → `squeeze_graph`（stock graph）；Figure 3.3 → `slope_equals_height`（**客製 hook**）；Figure 3.4 → `shm_stacked_graphs`（**客製 hook**）。
- 另 detail-redo 新增一個輕量 mini-visual：`continuity_statement_sin_limit` 的「弦≤弧」（可選 hook 或 stock 弧/弦小圖）。
- 吃重 `animation_cue`：sector_inequality、slope_equals_height、shm_stacked_graphs（會動的概念才動）。生成 manim code 視同 narration，**經使用者認可才定版**（§5），render 失敗走「由小到大逐層修補」。

### 內容層 checklist（§7；detail-redo 本輪須重跑——前版 [x] 已作廢）

- [ ] 每個 proposition（3.1、3.2）／theorem（3.1、3.2）有單元覆蓋；每個不同模式 example（3.1–3.3）有代表單元，無同型 silent drop。
- [ ] 無 exercise 內容洩入。
- [ ] intro（定位＋tagline）／recap（5 點 takeaway）／outro（無 takeaways）齊備。
- [ ] 散文幾何主張（單位圓面積、弦≤弧、slope=height、SHM 鏡射）皆有視覺單元；其餘散文皆歸類折疊／升格，無 silent drop。
- [ ] 每段環境之間散文已歸類（Incorporative／Bridge／Forward-pointing）。
- [ ] narration 為「說」而寫：開頭 hook、結尾 takeaway、未犯 §4 禁則（不報節號／圖號、不念螢幕標題、不用 see/as shown）；cosine 導數＋cot/csc repeat-pattern 省 setup。
- [ ] 每個承載步驟在 `visual_need` 逐行列出（第1檔——畫面顯示、不藏進旁白）；4 樞紐有第2檔直覺；數學不增刪、逐單元回溯講義。
- [ ] 數學讀得順（直讀 LaTeX 或白話；對齊鏈不重念 LHS）。
- [ ] 動畫建議用自然語言、聚焦教學意圖。
- [ ] 每個 id 唯一、snake_case、描述教學重點。
- [x] **六鏡稽核重跑 → blocking==0**（Workflow `wf_2a33636d-17d`；6 鏡全 clean、refute-by-default 後 0 blocking）。L5 隔離盲算 11 組關鍵數全 match。2 條 tier-3 advisory 已採納：continuity_statement kind theorem→proposition、squeeze_graph「see」→「picture」。
- [x] **散文 copyedit pass 重跑（鎖稿前）**（`narration-copyedit` subagent；0 blocking、7 optional tighten 全採納——why_trig 雙從句拆＋radians 預告收、difference_quotient 去 fronting、sector 去「too」、continuity_argument「largest possible value of one」收、fundamental_limit 雙 one 去、all_six「riding on」→「built on」）。語義/數學未動。
- [x] **重編 `ch03_trig_derivatives_narration.html` 審核稿**（22 單元，採納六鏡＋copyedit 後重編）。
- [x] **使用者 sign-off（2026-06-29）→ LOCKED**。下一步：Stage 2 工程稿（模板化、拆場、`part:`、把每步搬上畫面）＋ 客製 hook → schema/lint/sizecheck → mock render → 視覺幀稽核 → HTML 報告。
```
