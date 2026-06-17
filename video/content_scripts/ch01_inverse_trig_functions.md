# §1.2 Inverse Trigonometric Functions — 影片內容稿（content script）

> **產線：** 講義 → 影片，gen-2（2026-06-16 大重設後從 HTML 講義逐節重跑）。
> **權威來源：** [`../../handout/chapter1-print-standalone.html`](../../handout/chapter1-print-standalone.html) §1.2（編輯源 `handout/fragments/ch01/sec-1-2.html`）。
> **這是什麼：** 純內容中間產物（source of truth）。格式見 [`../CONTENT_METHODOLOGY.md`](../CONTENT_METHODOLOGY.md) §6——只含 `id`／`source`／`learning_goal`／`kind`／`narration`／`visual_need`／`animation_cue`，**不含**任何工程欄位（template／`{show}`／accent／payload）。工程是第二階段的事。
> **階段：** **DRAFT·六鏡＋潤稿 gate1 已收斂**（2026-06-17：六鏡 0 blocking／潤稿 gate1 採 3 條 wording；詳見 §7 checklist）。**待旁白 sign-off → LOCKED**（可選 copyedit gate2 Codex 收尾，計費徵同意）。narration 認可在編譯出的 `_narration.html` 上進行；本 `.md` 為權威，兩者 MUST 一致。

---

## meta（intro/outro 定位資訊）

- `id`: ch01_inverse_trig_functions
- `section`: 1.2
- `title`: Inverse Trigonometric Functions
- `chapter`: Chapter 1
- `chapter_title`: Inverse Functions and Limits
- `tagline`（intro 引導問題）: How do we turn a ratio back into an angle?
- 章內節次（intro 章節地圖用）：
  - 1.1 Inverse Functions
  - 1.2 Inverse Trigonometric Functions ← 本節
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
source: chapter1-print-standalone.html §1.2（Section Gate；定位資訊見上方 meta）
learning_goal: 知道本節在章內的位置，並帶著「怎麼把比值倒回角度」這個問題進入。
kind: motivation
narration: （無——intro 為純動畫）
visual_need: Section Gate——章節地圖 → 聚焦 1.2 → logo／節號／標題／tagline 字卡 → 暗場交接。
animation_cue: （由 intro 模板處理，內容稿不指定）
```

---

### unit: recovering_angles

```
id: recovering_angles
source: chapter1-print-standalone.html §1.2 · 開節散文第一段（"not one-to-one … recover an angle … restrict the domain of each trigonometric function"）
learning_goal: 知道反三角函數要解的問題（從比值還原角度），以及為何非得先把每個三角函數限定到一對一的區間。
kind: motivation
narration: |
  We can run the trigonometric functions forwards all day — feed in an
  angle, read off a ratio. This section runs them the other way: we are
  handed a ratio, and we want the angle that produced it. The slope of a
  ramp gives back an angle of inclination; a ratio of two sides of a right
  triangle gives back one of its angles. But there is an obstacle. The
  trig functions repeat their values endlessly, so on their full domains
  they are nowhere near one-to-one — and a function that is not one-to-one
  has no inverse. The way out is the move we already know: restrict each
  trig function to an interval where it is one-to-one, and invert that
  restricted piece. So the real work of this section is choosing the right
  interval for each one.
visual_need: |
  一句話動機（known ratio → recover angle，配 ramp／right-triangle 小圖示意）；
  一條提示：trig 在 ℝ 上週期重複 → 非一對一 → 必須限定到一對一區間再求逆。
animation_cue: （無——靜態示意即可；sine 的「失敗」交給下一單元動畫）
```

---

### unit: sine_is_not_one_to_one

```
id: sine_is_not_one_to_one
source: chapter1-print-standalone.html §1.2 · 開節散文第二段（"a horizontal line can intersect … more than once"）+ Figure 1.4（data-fig: sine-not-1to1）
learning_goal: 看見 sine 在 ℝ 上被同一個輸出值反覆命中，所以原樣不可逆——把週期性看成水平線穿很多次。
kind: counterexample
narration: |
  Start with sine, and watch exactly why it cannot be inverted as it
  stands. Slide a horizontal line across the graph of $y=\sin x$: at almost
  every height it crosses not once but over and over, marching off in both
  directions forever. Each of those crossings is a different angle with the
  very same sine. So a single value of sine comes from infinitely many
  angles, and there is no way to choose which one to send back. Sine is
  badly not one-to-one on the whole real line — and that is the problem we
  have to fix before any inverse can exist.
visual_need: |
  比照 Figure 1.4：連綿的 $y=\sin x$ 波；一條水平線 $y=c$（如 $y=\tfrac12$）與曲線
  多次相交，標出數個同高交點。註「not one-to-one on $\mathbb{R}$」。
animation_cue: |
  建議動畫：畫出向左右延伸的 sine 波。一條水平線從畫面上方滑入、停在某高度
  （如 $y=\tfrac12$），沿曲線同時閃示它命中的多個交點（往兩側延伸的無窮多個），
  每個交點落一個小點，凸顯「同一個輸出 → 無窮多個角度」。呼應 §1.1 的水平線測試。
```

---

### unit: restrict_sine_branch

```
id: restrict_sine_branch
source: chapter1-print-standalone.html §1.2 · "The inverse sine function" 小節散文（restrict to $-\tfrac\pi2\le x\le\tfrac\pi2$）+ Figure 1.5（data-fig: restricted-sine）
learning_goal: 看見限定到 $[-\tfrac\pi2,\tfrac\pi2]$ 後 sine 恢復一對一，且仍掃過整個值域 $[-1,1]$。
kind: visual
narration: |
  Here is the fix. Keep only the middle piece of the sine graph, the part
  between $-\tfrac{\pi}{2}$ and $\tfrac{\pi}{2}$. On that one interval sine
  climbs steadily from $-1$ up to $1$, never repeating a value along the
  way — so it is one-to-one there, and it still reaches every output from
  $-1$ to $1$. That restricted piece has exactly what we need: it can be
  reversed, and it gives up nothing in the range. This is the branch we
  are going to invert.
visual_need: |
  比照 Figure 1.5：完整 sine 波，只 highlight $[-\tfrac\pi2,\tfrac\pi2]$ 的中央分支
  （其餘淡化）；標該段從 $(-\tfrac\pi2,-1)$ 升到 $(\tfrac\pi2,1)$，值域填滿 $[-1,1]$。
animation_cue: |
  建議動畫：先顯示完整 sine 波。把 $[-\tfrac\pi2,\tfrac\pi2]$ 以外的部分淡出／灰掉，
  只留中央分支高亮；一個點沿中央分支從左端 $(-\tfrac\pi2,-1)$ 滑到右端 $(\tfrac\pi2,1)$，
  凸顯它單調遞增、把 $[-1,1]$ 恰好掃過一次。
```

---

### unit: arcsine_definition

```
id: arcsine_definition
source: chapter1-print-standalone.html §1.2 · Definition 1.3（arcsin）+ Caution 1.2（$\sin^{-1}$ 非倒數，折疊，見拆解註記 N1）
learning_goal: 認得 arcsin 的形式定義（值域釘在主值區間）與它的定義域／值域，並記住 $\sin^{-1}$ 不是倒數。
kind: definition
narration: |
  Now we can name the inverse. The inverse sine of $x$, written
  $\arcsin x$, is the angle in our restricted interval whose sine is $x$.
  In symbols, $\arcsin x = y$ means $\sin y = x$ with $y$ between
  $-\tfrac{\pi}{2}$ and $\tfrac{\pi}{2}$. Reading that straight off the
  branch, its domain is everything from $-1$ to $1$ — the values sine can
  produce — and its range is the interval from $-\tfrac{\pi}{2}$ to
  $\tfrac{\pi}{2}$. One warning about notation, the same one as before:
  $\arcsin x$ is often written $\sin^{-1} x$, but that $-1$ means inverse,
  not reciprocal — it is not $1$ over $\sin x$. When a source writes
  $\sin^{-1}$, check the context to see which is meant.
visual_need: |
  Def 1.3 卡：$\arcsin x = y \iff \sin y = x,\ -\tfrac\pi2\le y\le\tfrac\pi2$；
  domain $[-1,1]$、range $[-\tfrac\pi2,\tfrac\pi2]$。一條對比警示
  $\sin^{-1}x \ne \dfrac{1}{\sin x}$。
animation_cue: （無——靜態定義卡即可）
```

---

### unit: arcsine_identities

```
id: arcsine_identities
source: chapter1-print-standalone.html §1.2 · Proposition 1.2（Inverse sine identities）+ Caution 1.3（$\arcsin(\sin x)=x$ 僅在主值區間，折疊，見拆解註記 N2）
learning_goal: 知道 sin 與 arcsin 互相撤銷，但「先 sin 再 arcsin」只在主值區間內還原原角。
kind: proposition
narration: |
  Sine and arcsine undo each other — but you have to watch the direction.
  Going out and back, $\sin(\arcsin x)=x$ for every $x$ from $-1$ to $1$:
  hand in a legal ratio, take its angle, then take that angle's sine, and you
  land back on the ratio. The other order, $\arcsin(\sin x)=x$, only
  returns the original angle when that angle was already inside the
  restricted interval. Push outside it and arcsine cannot follow you home —
  take $x=\pi$: $\sin\pi$ is $0$, and $\arcsin 0$ is $0$, not $\pi$.
  Arcsine always answers with the angle in its own interval, even when that
  was not the angle you started from.
visual_need: |
  Prop 1.2 兩式：$\sin(\arcsin x)=x$ on $[-1,1]$；$\arcsin(\sin x)=x$ on
  $[-\tfrac\pi2,\tfrac\pi2]$。一條反例（guardrail）：$\arcsin(\sin\pi)=\arcsin 0=0\ne\pi$。
animation_cue: （無——靜態即可）
```

---

### unit: reference_triangle_method

```
id: reference_triangle_method
source: chapter1-print-standalone.html §1.2 · Strategy 1.2（The reference-triangle method）
learning_goal: 學會用一個直角三角形把「三角函數套在反三角式外面」的式子算出來，並從主值區間決定正負號。
kind: procedure
narration: |
  There is a clean recipe for evaluating something like the tangent of an
  arcsine — a trig function wrapped around an inverse-trig expression. Step
  one: name the inside. Set $\theta$ equal to the inverse-trig expression,
  which immediately hands you one ratio — if $\theta=\arcsin x$, then
  $\sin\theta=x$. Step two: draw a right triangle whose sides realise that
  ratio, using positive lengths for its magnitude. Step three: fill in the
  missing side with the Pythagorean theorem. Step four: read off whatever
  trig value you were after, straight from the completed triangle — and fix
  the sign separately, from the principal-value interval, not from the
  picture. The triangle gives you the size; the interval gives you the
  sign.
visual_need: |
  Strategy 1.2 四步驟（祈使句）：1) $\theta=$ 反三角式 → 讀出已知比值；
  2) 用正邊長畫直角三角形；3) Pythagoras 補缺邊；4) 讀值，正負號由主值區間定（非由圖）。
animation_cue: （無——程序步驟即可；三角形的「建構」動畫放在下個 example 單元）
```

---

### unit: evaluating_arcsin

```
id: evaluating_arcsin
source: chapter1-print-standalone.html §1.2 · Example 1.9（$\arcsin\tfrac12=\tfrac\pi6$；$\tan(\arcsin\tfrac13)$ via 三角形）+ Figure 1.6（data-fig: arcsin-triangle）
learning_goal: 親手算兩個 arcsin 值——一個直接由特殊角讀出，一個用參考三角形。
kind: example
narration: |
  Let us evaluate two. First, $\arcsin\tfrac{1}{2}$: we want the angle in
  our interval whose sine is a half, and that is $\tfrac{\pi}{6}$ — read
  straight off a special angle, no triangle needed. The second is the kind
  the recipe was built for: the tangent of $\arcsin\tfrac{1}{3}$. Set
  $\theta=\arcsin\tfrac{1}{3}$, so $\sin\theta$ is a third, an angle in the
  first quadrant. Draw a right triangle with opposite side $1$ and
  hypotenuse $3$; the adjacent side is $\sqrt{9-1}$, which is $2\sqrt{2}$.
  Tangent is opposite over adjacent, so $\tan\theta$ is $1$ over
  $2\sqrt{2}$. We never named the angle itself — but the triangle handed us
  its tangent anyway.
visual_need: |
  (a) $\arcsin\tfrac12=\tfrac\pi6$（特殊角）。
  (b) 比照 Figure 1.6：直角三角形，對邊 $1$、斜邊 $3$、鄰邊 $\sqrt8=2\sqrt2$，角 $\theta$；
  讀出 $\tan\theta=\dfrac{1}{2\sqrt2}$。
animation_cue: |
  建議動畫：以 $\sin\theta=\tfrac13$ 為起點，逐步建構直角三角形——先畫角 $\theta$、
  對邊 $1$ 與斜邊 $3$，再由 Pythagoras 讓鄰邊 $2\sqrt2$ 浮現，最後高亮對／鄰兩邊
  讀出 $\tan\theta=\dfrac{1}{2\sqrt2}$。凸顯「比值 → 三角形 → 想要的值」這條路。
```

---

### unit: restrict_cosine_branch

```
id: restrict_cosine_branch
source: chapter1-print-standalone.html §1.2 · inverse-cosine intuition 散文（expansion:intuition，"$[0,\pi]$ sweeps the entire range … exactly once"）+ "one-to-one on $0\le x\le\pi$" + Figure 1.7（data-fig: restricted-cosine）
learning_goal: 看見 cosine 在 $[0,\pi]$ 上單調由 $1$ 降到 $-1$、掃過 $[-1,1]$ 恰一次，是 arccos 的自然限定區間。
kind: visual
narration: |
  Cosine needs the same treatment, but a different interval — its own
  middle piece would fail, because cosine is symmetric across zero and
  would just repeat. So watch cosine instead on the interval from $0$ to
  $\pi$. It starts at $1$, slides down steadily, and ends at $-1$, hitting
  every value in between exactly once. On that interval cosine is
  one-to-one and still sweeps the full range — the natural counterpart of
  the interval we picked for sine. That is the branch we invert to get the
  inverse cosine.
visual_need: |
  比照 Figure 1.7：完整 cosine 波，highlight $[0,\pi]$ 分支（其餘淡化）；
  標從 $(0,1)$ 降到 $(\pi,-1)$，單調掃過 $[-1,1]$。
animation_cue: （無——靜態高亮即可；branch 隔離動畫已在 sine 演過，cosine 以類比承接，省動畫額度）
```

---

### unit: arccosine_definition

```
id: arccosine_definition
source: chapter1-print-standalone.html §1.2 · Definition 1.4（arccos）
learning_goal: 認得 arccos 的定義與定義域／值域（值域 $[0,\pi]$）。
kind: definition
narration: |
  The inverse cosine follows the very same script. The inverse cosine of
  $x$, written $\arccos x$, is the angle between $0$ and $\pi$ whose cosine
  is $x$: $\arccos x = y$ means $\cos y = x$ with $y$ from $0$ to $\pi$.
  Its domain is again everything from $-1$ to $1$ — the values cosine can
  take — and this time its range runs from $0$ to $\pi$. Same idea as
  arcsine, just anchored on cosine's interval instead of sine's.
visual_need: |
  Def 1.4 卡：$\arccos x = y \iff \cos y = x,\ 0\le y\le\pi$；
  domain $[-1,1]$、range $[0,\pi]$。
animation_cue: （無——靜態定義卡即可）
```

---

### unit: arccosine_identities

```
id: arccosine_identities
source: chapter1-print-standalone.html §1.2 · Proposition 1.3（Inverse cosine identities）
learning_goal: 知道 cos 與 arccos 的撤銷恆等式，並認得它與 arcsin 同一個「只有一個方向永遠安全」的結構。
kind: proposition
narration: |
  The cancellation identities copy straight over. Cosine of arccosine of
  $x$ equals $x$ for every $x$ from $-1$ to $1$ — out and back, no fine
  print. And arccosine of cosine of $x$ equals $x$ as well, but, exactly as
  with sine, only when the starting angle was already between $0$ and
  $\pi$. It is the same one-directional pattern as for sine — and we will
  pin it down for all three in just a moment.
visual_need: |
  Prop 1.3 兩式：$\cos(\arccos x)=x$ on $[-1,1]$；$\arccos(\cos x)=x$ on $[0,\pi]$。
animation_cue: （無——靜態即可）
```

---

### unit: domain_of_compositions

```
id: domain_of_compositions
source: chapter1-print-standalone.html §1.2 · Example 1.10（$f=\arcsin(\cos x)$、$h=\sin(\arccos x)$ 的定義域）+ 其後通則散文（inner 先合法、再 outer 接受 inner 輸出）
learning_goal: 學會求複合反三角函數的定義域——先看內層允許什麼輸入，再看外層接不接受內層的輸出。
kind: example
narration: |
  Inverse trig functions are fussy about what they will accept, so let us
  practise finding the domain of a composition. Take $f(x)=\arcsin(\cos
  x)$. Whatever $x$ is, $\cos x$ already lands between $-1$ and $1$ — and
  that is precisely what arcsine accepts — so every real number is allowed;
  the domain of $f$ is all of $\mathbb{R}$. Now flip the order:
  $h(x)=\sin(\arccos x)$. The inner function, arccosine, demands an input
  from $-1$ to $1$; its output is just an angle, and sine will swallow any
  angle, so the domain of $h$ is $-1$ to $1$. The rule behind both: first
  make sure the input is legal for the inner function, then make sure the
  inner function's output is legal for the outer one.
visual_need: |
  (a) $f(x)=\arcsin(\cos x)$：$\cos x\in[-1,1]=$ arcsin 定義域 → domain $\mathbb{R}$。
  (b) $h(x)=\sin(\arccos x)$：arccos 需 $x\in[-1,1]$，sin 接受任意角 → domain $[-1,1]$。
  一句通則：inner 先收得下、outer 再收得下 inner 的輸出。
animation_cue: （無——以推理為主）
```

---

### unit: principal_value_trap

```
id: principal_value_trap
source: chapter1-print-standalone.html §1.2 · Example 1.11（粒子上下振盪，$t=\arccos(1)$ 陷阱）
learning_goal: 看清反三角函數只回「一個主值」——arccos 不會回傳所有解，誤用會得到荒謬結論。
kind: counterexample
narration: |
  Here is a trap worth springing once, on purpose. A particle starts moving
  at time $t=10$ and bobs up and down, its height at time $t$ equal to
  $\cos t$. True or false: the particle has height $1$ at time
  $t=\arccos(1)$? It is false — and the reason is exactly what makes
  inverse trig subtle. The equation $\cos t = 1$ holds at infinitely many
  times, but arccosine returns only its one principal value, $t=0$. And at
  $t=0$ the particle is not even moving yet; its motion only begins at
  $t=10$. The particle really does reach height $1$, at the times
  $t=2\pi n$ once $n$ is large enough. But $\arccos(1)$ is $0$, which is not
  one of them. An inverse trig function gives you a single angle, never
  the whole family.
visual_need: |
  粒子高度 $h(t)=\cos t$（$t\ge10$）的波形；height $1$ 在 $t=2\pi n$ 反覆出現；
  $\arccos(1)=0$ 只給一個值（且 $t=0$ 粒子尚未啟動）。註「principal value only」。
animation_cue: |
  建議動畫：畫 $h=\cos t$ 波（$t\ge10$ 段）。一個小球沿波上下 bob；水平線
  $h=1$ 與波在 $t=2\pi n$（$n\ge2$）數處相切閃示為「真正到達高度 1」；對比把
  $\arccos(1)=0$ 單獨標在 $t=0$（粒子尚未啟動處，灰示），凸顯「反三角只回一個主值、
  不是全部解」。
```

---

### unit: restrict_tangent_branch

```
id: restrict_tangent_branch
source: chapter1-print-standalone.html §1.2 · inverse-tangent intuition 散文（expansion:intuition，"climbs … from $-\infty$ to $+\infty$ … every real number … exactly once"）+ "one-to-one on $-\tfrac\pi2<x<\tfrac\pi2$" + Figure 1.8（data-fig: restricted-tangent）
learning_goal: 看見 tangent 在 $(-\tfrac\pi2,\tfrac\pi2)$ 上由 $-\infty$ 爬到 $+\infty$、每個實數恰取一次，因此 arctan 接受全體實數。
kind: visual
narration: |
  Tangent gets the most dramatic interval of the three. On the open
  interval from $-\tfrac{\pi}{2}$ to $\tfrac{\pi}{2}$, tangent climbs
  without bound: it plunges toward $-\infty$ at the left edge, rises through
  $0$ in the middle, and races up toward $+\infty$ at the right edge. Along
  the way it passes through every real number, and through each one exactly
  once. That is why the inverse tangent is the generous one — where arcsine
  and arccosine only take inputs between $-1$ and $1$, arctangent accepts
  every real number you can hand it.
visual_need: |
  比照 Figure 1.8：tangent 在 $(-\tfrac\pi2,\tfrac\pi2)$ 的分支，兩側垂直漸近線
  $x=\pm\tfrac\pi2$；曲線由 $-\infty$ 升至 $+\infty$、過原點；註「每個實數取一次 → domain $\mathbb{R}$」。
animation_cue: |
  建議動畫：畫 $(-\tfrac\pi2,\tfrac\pi2)$ 上的 tangent 分支與兩條垂直漸近線。一個點
  沿曲線從左下（趨 $-\infty$）爬到右上（趨 $+\infty$）；同時一條水平線可停在任意高度，
  顯示它恰好命中曲線一次，凸顯「每個實數值都取得到、且只取一次 → arctan 接受全體 $\mathbb{R}$」。
```

---

### unit: arctangent_definition

```
id: arctangent_definition
source: chapter1-print-standalone.html §1.2 · Definition 1.5（arctan）
learning_goal: 認得 arctan 的定義與定義域／值域（定義域 $\mathbb{R}$、值域開區間 $(-\tfrac\pi2,\tfrac\pi2)$）。
kind: definition
narration: |
  So here is the inverse tangent. The inverse tangent of $x$, written
  $\arctan x$, is the angle strictly between $-\tfrac{\pi}{2}$ and
  $\tfrac{\pi}{2}$ whose tangent is $x$: $\arctan x = y$ means $\tan y = x$
  with $y$ in that open interval. Because tangent reached every real value,
  the domain of arctangent is all of $\mathbb{R}$ — no restriction on the
  input at all — and its range is the open interval from $-\tfrac{\pi}{2}$
  to $\tfrac{\pi}{2}$, edges never quite reached.
visual_need: |
  Def 1.5 卡：$\arctan x = y \iff \tan y = x,\ -\tfrac\pi2<y<\tfrac\pi2$；
  domain $\mathbb{R}$、range $(-\tfrac\pi2,\tfrac\pi2)$（開區間）。
animation_cue: （無——靜態定義卡即可）
```

---

### unit: arctangent_identities

```
id: arctangent_identities
source: chapter1-print-standalone.html §1.2 · Proposition 1.4（Inverse tangent identities）+ Caution 1.4（三函數共通的撤銷警示＋outer∘inner 永遠安全，折疊，見拆解註記 N3）
learning_goal: 知道 tan/arctan 的撤銷恆等式，並掌握貫通三者的通則——outer-undoes-inner 永遠安全、inner-undoes-outer 只在主值區間內成立。
kind: proposition
narration: |
  Tangent and arctangent undo each other on the same terms. Tangent of
  arctangent of $x$ is $x$ for every real $x$; arctangent of tangent of $x$
  is $x$ only when the angle was already in the open interval. And now the
  pattern across all three inverses is worth stating once and for all.
  Outer-undoes-inner is always safe on the natural domain — $\sin(\arcsin
  x)$, $\cos(\arccos x)$, and $\tan(\arctan x)$ each give back $x$ with no
  conditions. But inner-undoes-outer — $\arcsin(\sin x)$, $\arccos(\cos x)$,
  $\arctan(\tan x)$ — returns your angle only inside the principal interval.
  Step outside, and the inverse hands back the equivalent angle that does
  live there: $\arctan(\tan\pi)$, for instance, is $\arctan 0$, which is
  $0$, not $\pi$.
visual_need: |
  Prop 1.4 兩式：$\tan(\arctan x)=x$ on $\mathbb{R}$；$\arctan(\tan x)=x$ on
  $(-\tfrac\pi2,\tfrac\pi2)$。一張三函數通則對照：outer∘inner 永真；inner∘outer 僅主值區間。
  反例 $\arctan(\tan\pi)=\arctan 0=0\ne\pi$（並可並列 $\arccos(\cos 2\pi)=0\ne2\pi$）。
animation_cue: （無——靜態即可）
```

---

### unit: evaluating_inverse_trig

```
id: evaluating_inverse_trig
source: chapter1-print-standalone.html §1.2 · Example 1.12（$\sin(\arccos(-\tfrac12))$、$\sec(\arctan 10)$、$\tan(\arcsin(-\tfrac{2\sqrt5}{5}))$）+ Figure 1.9（data-fig: arctan10-triangle）
learning_goal: 在更難的情形套參考三角形＋主值定號：負輸入、鈍角主值、第四象限。
kind: example
narration: |
  Now the triangle method earns its keep on harder values — same recipe,
  trickier signs. First, the sine of arccosine of $-\tfrac{1}{2}$.
  Arccosine of a negative input always lands in the second quadrant, here
  at $\tfrac{2\pi}{3}$, and its sine is $\tfrac{\sqrt{3}}{2}$. Second, the
  secant of arctangent of $10$: set the angle with tangent $10$, build a
  triangle with opposite $10$ and adjacent $1$, and the hypotenuse is
  $\sqrt{101}$ — so the secant, hypotenuse over adjacent, is $\sqrt{101}$.
  Third, the tangent of arcsine of $-\tfrac{2\sqrt{5}}{5}$. The sine is
  negative, so the angle sits in the fourth quadrant, where cosine is
  positive; the triangle gives cosine $\tfrac{1}{\sqrt{5}}$, and the
  tangent works out to $-2$. Every time, the triangle set the size and the
  principal interval set the sign.
visual_need: |
  (a) $\sin(\arccos(-\tfrac12))$：主值 $\tfrac{2\pi}{3}$（第二象限），$\sin=\tfrac{\sqrt3}{2}$。
  (b) 比照 Figure 1.9：$\tan\theta=10$，對 $10$、鄰 $1$、斜 $\sqrt{101}$ → $\sec=\sqrt{101}$。
  (c) $\sin\theta=-\tfrac{2}{\sqrt5}$，第四象限 $\cos=\tfrac{1}{\sqrt5}$ → $\tan=-2$。
  每例強調正負號由主值區間（象限）決定，不是用猜的。
animation_cue: （無——三角形建構動畫已在 evaluating_arcsin 演過，此處 repeat-pattern 省略、以推理為主）
```

---

### unit: simplify_cos_arctan

```
id: simplify_cos_arctan
source: chapter1-print-standalone.html §1.2 · Example 1.13（化簡 $\cos(\arctan x)=\tfrac{1}{\sqrt{1+x^2}}$）+ Figure 1.10（data-fig: arctan-general-triangle）
learning_goal: 把參考三角形推廣到一般變數 $x$——化簡出一條恆等公式（而非單一數值）。
kind: example
narration: |
  One more, and this time the answer is a formula, not a number. Simplify
  the cosine of arctangent of $x$, for a general $x$. Let $y=\arctan x$, so
  $\tan y = x$ with $y$ in the open interval — and what we want is $\cos y$.
  Reach for the identity $1+\tan^2 y=\sec^2 y$: it turns $\sec^2 y$ into
  $1+x^2$. Since $y$ lives in the open interval, cosine is positive there,
  so secant is positive too, and $\sec y$ is $\sqrt{1+x^2}$. Cosine is $1$
  over secant — so the cosine of arctangent of $x$ is $\tfrac{1}{\sqrt{1+x^2}}$.
  A whole family of values, caught in one clean expression.
visual_need: |
  推導鏈：$y=\arctan x$、$\tan y=x$；$1+\tan^2 y=\sec^2 y \Rightarrow \sec^2 y=1+x^2$；
  $y\in(-\tfrac\pi2,\tfrac\pi2)\Rightarrow\cos y>0\Rightarrow\sec y=\sqrt{1+x^2}$；
  $\cos(\arctan x)=\dfrac{1}{\sqrt{1+x^2}}$。可附 Figure 1.10 一般三角形（鄰 $1$、對 $x$、斜 $\sqrt{1+x^2}$）。
animation_cue: （無——靜態推導鏈即可）
```

---

### unit: remaining_inverse_trig

```
id: remaining_inverse_trig
source: chapter1-print-standalone.html §1.2 · 小節散文（"used less frequently … same spirit"）+ Definition 1.6（arccsc）+ Definition 1.7（arcsec）+ Definition 1.8（arccot）+ 其後 domains 散文（見拆解註記 N4：三定義同一單元）
learning_goal: 認得其餘三個反三角函數（arccsc／arcsec／arccot），知道它們同樣靠選定主值區間定義，以及各自的定義域。
kind: definition
narration: |
  That completes the three main inverses; three more round out the set,
  used less often but built the same way. The inverse cosecant, inverse
  secant, and inverse cotangent each invert their function on a chosen
  principal range — the interval their output angle is pinned to. Cosecant
  and secant only take values of size at least $1$, so $\arccsc$ and
  $\arcsec$ accept inputs from $1$ outward in both directions — everything
  with absolute value at least $1$; cotangent, like tangent, reaches
  everything, so $\arccot$ has domain all of $\mathbb{R}$. The principal
  ranges this time are a little less tidy — built from two pieces apiece —
  but the principle has not changed at all: pick an interval where the
  function is one-to-one, and invert there.
visual_need: |
  三定義（簡列、皆呈現、不省）：
  $\arccsc x = y \iff \csc y = x,\ y\in(0,\tfrac\pi2]\cup(\pi,\tfrac{3\pi}2]$；
  $\arcsec x = y \iff \sec y = x,\ y\in[0,\tfrac\pi2)\cup[\pi,\tfrac{3\pi}2)$；
  $\arccot x = y \iff \cot y = x,\ y\in(0,\pi)$。
  定義域：arccsc／arcsec：$(-\infty,-1]\cup[1,\infty)$；arccot：$\mathbb{R}$。
animation_cue: （無——靜態定義卡即可）
```

---

### unit: conventions_change_answers

```
id: conventions_change_answers
source: chapter1-print-standalone.html §1.2 · Remark 1.3 + Remark 1.4（arcsec／arccsc 主值區間另有約定，本書固定其一，折疊為 lead-in，見拆解註記 N5）+ Example 1.14（$f=\arcsin x+\arccsc x$）
learning_goal: 看見「主值區間是一種約定、不是定律」——換約定就換答案，所以本書明確固定約定。
kind: example
narration: |
  Those principal ranges are choices, not laws — and the choice has visible
  consequences. Different books pick different intervals for arcsecant and
  arccosecant, and this text deliberately fixes one set, the one that keeps
  later formulas clean. Here is a function that exposes the stakes:
  $f(x)=\arcsin x + \arccsc x$. Arcsine needs $x$ between $-1$ and $1$;
  arccosecant needs $x$ of size at least $1$ — so the only inputs both
  allow are $x=1$ and $x=-1$, a domain of just two points. At $x=1$, both
  pieces are $\tfrac{\pi}{2}$, so $f$ is $\pi$. At $x=-1$, arcsine is
  $-\tfrac{\pi}{2}$, and under this text's convention arccosecant is
  $\tfrac{3\pi}{2}$ — so $f$ is $\pi$ again. The function is just the
  constant $\pi$. But switch to the other common convention, where
  $\arccsc(-1)$ is $-\tfrac{\pi}{2}$, and $f(-1)$ would come out $-\pi$
  instead — same function, different answer, purely from the branch choice.
  That is exactly why we fix a convention up front.
visual_need: |
  domain $=\{\pm1\}$（arcsin 需 $|x|\le1$、arccsc 需 $|x|\ge1$）。
  $f(1)=\tfrac\pi2+\tfrac\pi2=\pi$；$f(-1)=-\tfrac\pi2+\tfrac{3\pi}2=\pi$（本書約定）→ $f\equiv\pi$。
  對照：另一約定 $\arccsc(-1)=-\tfrac\pi2$ → $f(-1)=-\pi$。註「約定不同 → 答案不同」。
animation_cue: （無——以推理＋兩約定對照為主）
```

---

### unit: recap

```
id: recap
source: chapter1-print-standalone.html §1.2（全節重點凝煉；Key Takeaways 單元，有旁白）
learning_goal: 把本節串成一條線——限定分支、三個主反函數的區間、主值唯一性、參考三角形。
kind: recap
narration: |
  Let us pull the section together. Every inverse trig function starts the
  same way: a trig function is not one-to-one, so we restrict it to a branch
  where it is, and invert that branch. Arcsine lives on $-\tfrac{\pi}{2}$ to
  $\tfrac{\pi}{2}$, arccosine on $0$ to $\pi$, and arctangent on the open
  interval between — which is why arctangent alone accepts every real
  number, while arcsine and arccosine only take inputs from $-1$ to $1$.
  Each inverse returns a single principal value, never the whole family of
  angles, so the cancellation identities only run cleanly in the
  outer-undoes-inner direction. And to evaluate a trig function of an
  inverse-trig expression, draw the reference triangle for the size and read
  the sign off the principal interval. Restrict, invert, and mind the
  principal value — that is the whole section.
visual_need: |
  Key Takeaways 卡片（4 點）＋ remember-formula 卡：
  points：
    • Restrict each trig function to a one-to-one branch, then invert
      （arcsin: $[-\tfrac\pi2,\tfrac\pi2]$；arccos: $[0,\pi]$；arctan: $(-\tfrac\pi2,\tfrac\pi2)$）。
    • $\arctan$ accepts all of $\mathbb{R}$; $\arcsin$, $\arccos$ only $[-1,1]$。
    • Inverse trig returns one principal value → outer∘inner always holds; inner∘outer only on the principal interval。
    • Evaluate trig of inverse-trig: reference triangle for size, principal interval for sign。
  formulas（保持短，避免出框）：
    • $\arcsin x = y \iff \sin y = x$
    • $\sin(\arcsin x)=x$
    • $\sin^{-1}\ne 1/\sin$
animation_cue: （無——靜態卡片即可）
```

---

### unit: outro

```
id: outro
source: chapter1-print-standalone.html §1.2（節末品牌字卡）
learning_goal: （收尾；無教學內容）
kind: recap
narration: （無——outro 為純動畫，無 takeaways）
visual_need: 兩段式 outro——暗轉亮橋接 → 最終 logo／節號／標題字卡。
animation_cue: （由 outro 模板處理）
```

---

## §7 拆解註記與內容層品質檢核

### 拆解／折疊決策（就近註明，杜絕 silent drop）

- **N1 — Caution 1.2（$\sin^{-1}$ 非倒數）折疊進 `arcsine_definition`。** 依 CONTENT_METHODOLOGY §3「env-caution（1–3 句陷阱警示）併入其警示對象的單元」——警示對象正是該單元剛 introduce 的 $\arcsin$／$\sin^{-1}$ 記號。與 §1.1 把 Caution 1.1（$f^{-1}$ 非倒數）折進 inverse 定義單元的處理一致。
- **N2 — Caution 1.3（$\arcsin(\sin x)=x$ 僅在主值區間，含 $\arcsin(\sin\pi)=0\ne\pi$）折疊進 `arcsine_identities`** 作為 guardrail beat（§3「caution 併入其警示對象的單元」）——它警示的正是 Prop 1.2 的第二條 identity。
- **N3 — Caution 1.4（三函數共通的撤銷警示＋反向永遠安全）折疊進 `arctangent_identities`。** Caution 1.4 同時涵蓋 arccos 與 arctan，並把「outer∘inner 永真、inner∘outer 僅主值區間」收成通則；位置在 Prop 1.4 之後，折進 arctan identities 單元作為「三者通則」收尾最自然。`arccosine_identities` 僅以一句純前向指標（"we will pin it down for all three in just a moment"）承接、不預先講出通則內容，避免 arccos／arctan 兩處重述同一 caution（潤稿後已把原本預講通則的句子瘦身為純前向指標）。**此前向承諾鎖定 arccos→arctan 的相對場景順序**——若日後重排把 arctan 段移到 arccos 段之前，這句承諾會懸空，需連動改寫（六鏡 L2 advisory 之穩健性提醒，當前順序下無誤）。
- **N4 — Definitions 1.6／1.7／1.8（arccsc／arcsec／arccot）合為單一單元 `remaining_inverse_trig`。** 雖 CONTENT_METHODOLOGY §3 表訂「一個定義一個單元」，但本節這三個反函數由講義明文定位為「used less frequently, defined in the same spirit」、並在三定義後**集中**處理定義域，屬書本刻意的「批次」呈現；三條定義式**全數於 `visual_need` 呈現、無一省略**（不漏環境），教學重點凝聚為單一「同一招收尾其餘三個」。比照 §2「同型重複 MAY 折疊成代表＋就近註明」之精神延伸至此批定義。若日後視覺過載，再拆為三個定義單元。
- **N5 — Remark 1.3 + Remark 1.4（arcsec／arccsc 另有主值區間約定）折疊為 `conventions_change_answers` 的 lead-in。** 兩 remark 的教學重點（主值區間是約定、本書固定其一）正是 Example 1.14 要演示的命題；折進該 example 作為動機 lead-in，避免一個「純講約定、無計算」的過薄單元，且讓「約定 → 後果」在同一單元閉環（§3「短附註併入鄰段 narration」）。
- **散文歸類（§3，無 silent drop）：** 開節第一段（recover angle／restrict）→ `recovering_angles`（Incorporative/motivation）；第二段（sine not 1-to-1）→ `sine_is_not_one_to_one`；"The inverse sine function" 小節散文 → `restrict_sine_branch`；"The composition identities … take the following form" → `arcsine_identities` lead-in；inverse-cosine intuition（enrichment）→ `restrict_cosine_branch`；inverse-tangent intuition（enrichment）→ `restrict_tangent_branch`；"used less frequently … same spirit" + domains 散文 → `remaining_inverse_trig`；Example 1.10 收尾通則散文（"first make sure the input … inner … outer"）→ `domain_of_compositions`。

### 視覺／動畫盤點（§5；§1.2 約 45% 符號／55% 幾何，medium——不套 symbol-heavy 例外，視覺各司其職）

- 七張講義圖全覆蓋：Figure 1.4（sine-not-1to1）→ `sine_is_not_one_to_one`；Figure 1.5（restricted-sine）→ `restrict_sine_branch`；Figure 1.6（arcsin-triangle）→ `evaluating_arcsin`；Figure 1.7（restricted-cosine）→ `restrict_cosine_branch`；Figure 1.8（restricted-tangent）→ `restrict_tangent_branch`；Figure 1.9（arctan10-triangle）→ `evaluating_inverse_trig`；Figure 1.10（arctan-general-triangle）→ `simplify_cos_arctan`。
- 5 個 `animation_cue`（會動的概念才動，§5「Animate, not just display」，且兩兩不重複）：`sine_is_not_one_to_one`（水平線掃過 sine 波、多交點失敗）、`restrict_sine_branch`（隔離中央分支＋點掃過 $[-1,1]$）、`evaluating_arcsin`（建構參考三角形）、`restrict_tangent_branch`（沿漸近線爬升、每實數取一次）、`principal_value_trap`（粒子 bob＋主值單一）。restrict_cosine 刻意以類比承接、不重複 branch 隔離動畫；evaluating_inverse_trig 以 repeat-pattern 省略三角形建構動畫。生成的 manim code 視同 narration，**經使用者認可才定版**（§5）。

### 內容層 checklist（§7）

- [x] 每個 definition（1.3–1.8）／proposition（1.2–1.4）有單元覆蓋；strategy（1.2）有單元；每個不同模式 example（1.9–1.14）有代表單元，無同型 silent drop（六例皆帶新模式：特殊角＋三角形／複合定義域／主值陷阱／負輸入象限／一般化公式／約定後果）。
- [x] 無 exercise 內容洩入（本節 fragment 無 env-exercise）。
- [x] intro（定位＋tagline）／recap（takeaway 清單）／outro（無 takeaways）齊備。
- [x] 散文幾何主張（sine/cosine/tangent 分支、參考三角形）皆有視覺單元；symbol/幾何約 45/55，不套 §5 symbol-heavy 例外。
- [x] 每段環境之間散文已歸類（Incorporative／Bridge／Forward-pointing），fold 或 promote，無 silent drop（見上「散文歸類」）。
- [x] narration 為「說」而寫：開頭 hook、結尾 takeaway、未犯 §4 禁則（不報節號／圖號、不念螢幕標題、不用 see/as shown）、同型第二例（evaluating_inverse_trig 對 evaluating_arcsin）repeat-pattern 省 setup。
- [x] 數學讀得順（直讀 LaTeX 或白話；$\sin^{-1}$ 念 sine inverse、$\arcsin$ 念 arcsine、主值區間直接讀——口語攤平屬後續 `.spoken.yml`，不污染正典）。
- [x] 動畫建議用自然語言、聚焦教學意圖。
- [x] 每個 `id` 唯一、snake_case、描述教學重點。
- [x] **六鏡稽核 → 收斂（2026-06-17，6 個並行 audit agent＋refute-by-default）：0 blocking、6 advisory（全非阻斷）。** L1 忠實 clean（必納環境全覆蓋、source 錨點屬實、駁回 6 候選）／L2 拆解 0blk·3adv（N1–N5 折疊全站得住、散文無 silent drop；3 條皆跨單元順序/視覺負載前瞻提示）／L3 語域 0blk·2adv（長句朗讀 polish）／L4 不重複 0blk·1adv（arccos 通則句瘦身）／**L5 數學隔離盲算 clean（10 項獨立重算全 match：三角形邊長、象限、主值區間端點、約定後果 $f\equiv\pi$ vs $-\pi$）**／L6 完整 clean（6 def／3 prop／strategy／6 example／7 figure 全覆蓋）。
- [x] **散文潤稿 gate1（2026-06-17，narration-copyedit agent，鎖稿前）：3 tighten＋6 optional 全 advisory（blocking==0）。** 採納 3 條（多代理交集／零語義風險，純 wording）：principal_value_trap 長句拆兩句（L3＋copyedit 雙標）、arccosine_identities 通則句瘦身為純前向指標（L4，讓 arctan「once for all three」收束更有力）、arcsine_identities 三動作句加 "then" 一拍（L3）。其餘 6 條不採並記錄理由：arcsine_definition「not reciprocal」保留（與已 LOCKED §1.1 inverse_function_definition 平行措辭）、reference_triangle_method「for its magnitude」保留（撐起 step 4「sign 另定」的 magnitude/sign 分離）、conventions_change_answers「under this text's convention」保留（本單元核心即「約定歸屬」，不可模糊為 "here"）、其餘 optional 皆刻意 cadence（"forever"／"each one exactly once"／proposition 三胞胎平行開場／"no triangle needed" 對比）。**gate2 Codex（計費，徵同意後）：待裁決——六鏡已是 multi-agent 對抗稽核（無 gate2），僅 copyedit 可選擇性加跑 Codex gate2 收尾（比照 §1.1 曾再得 5 條 wording）。**
- [ ] 已編譯 `ch01_inverse_trig_functions_narration.html` 審核稿＋ `_audit/REVIEW-ch01_inverse_trig_functions-sixlens.html` 完工報告（產製中）。
- [ ] **旁白 sign-off（使用者）→ LOCKED**（待）。下一步：Stage 2 工程稿 `ch01_inverse_trig_functions.yml`（模板化、`{show}`／accent／payload）→ schema/lint/sizecheck → mock → 視覺稽核 → 5 客製動畫 → MiMo 口語軌＋NFA → MiMo TTS（計費，屆時徵同意）。
```
