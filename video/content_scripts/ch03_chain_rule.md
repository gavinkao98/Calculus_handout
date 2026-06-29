# §3.2 The Chain Rule — 影片內容稿（content script）

> **產線：** 講義 → 影片，gen-2。Chapter 3 第二節，從 HTML 講義逐節重跑。
> **權威來源：** [`../../handout/fragments/ch03/sec-3-2.html`](../../handout/fragments/ch03/sec-3-2.html)（建置版 `handout/chapter3-print-standalone.html` §3.2）。
> **這是什麼：** 純內容中間產物（source of truth）。格式見 [`../CONTENT_METHODOLOGY.md`](../CONTENT_METHODOLOGY.md) §6——只含 `id`／`source`／`learning_goal`／`kind`／`narration`／`visual_need`／`animation_cue`，**不含**任何工程欄位（template／`{show}`／accent／payload／divider）。工程是第二階段的事。
> **階段：** **LOCKED（`CONTENT_APPROVED=yes`；2026-06-29 使用者 sign-off）**——本輪只做 Stage 1 內容稿（使用者裁決 2026-06-29：先做內容稿到 sign-off 暫停）。Thm 3.3 證明走 **full ε-δ 全展開**（使用者裁決），切 4 個 proof 單元。計畫見 [`_audit/PLAN-ch03-s32-video.md`](_audit/PLAN-ch03-s32-video.md)。本輪六鏡 blocking==0（Workflow `wf_d53afe59-4f2`、L5 盲算全 match）＋ copyedit（6 tighten＋9 optional 全採納）＋ 使用者 sign-off 已完成 → LOCKED；後續忠實性由 NFA 把關，post-lock 改稿須對動到單元跑 scoped NFA 回歸（§8）。Stage 2（storyboard／hooks／render／視覺閘）達範圍同意後續做。narration 認可在編譯出的 `_narration.html` 上進行；本 `.md` 為權威，兩者 MUST 一致。

---

## meta（intro/outro 定位資訊）

- `id`: ch03_chain_rule
- `section`: 3.2
- `title`: The Chain Rule
- `chapter`: Chapter 3
- `chapter_title`: Chain Rule and Trigonometric Derivatives
- `tagline`（intro 引導問題）: Why do the slopes multiply?
- 章內節次（intro 章節地圖用）：
  - 3.1 Derivatives of the Sine and Cosine Functions
  - 3.2 The Chain Rule ← 本節
  - 3.3 Applications of the Chain Rule
- `outro` next：next_section `3.3`、next_title `Applications of the Chain Rule`。

> intro 與 outro 為純動畫、**無 narration**（gen-2 first-class）。Key Takeaways 在 `recap` 教學單元（有旁白），不在 outro。Stage divider（章內分段開場：The Rule You Can Use／Why the Rule Is True／Using the Rule）是第二階段 storyboard 的結構元素，**不在本內容稿**。

---

## 教學單元（依教學自由重排；忠實仍可逐單元回溯講義）

---

### unit: intro

```
id: intro
source: chapter3-print-standalone.html §3.2（Section Gate；定位資訊見上方 meta）
learning_goal: 知道本節在章內的位置，並帶著「合成函數的斜率為何相乘」這個問題進入。
kind: motivation
narration: （無——intro 為純動畫）
visual_need: Section Gate——Chapter 3 章節地圖 → 聚焦 3.2 → logo／節號／標題／tagline 字卡 → 暗場交接。
animation_cue: （由 intro 模板處理，內容稿不指定）
```

---

### unit: why_composition_is_missing

```
id: why_composition_is_missing
source: chapter3-print-standalone.html §3.2 · 開節 para 1（expansion:intuition，"We can differentiate sin x, yet nothing so far reaches sin(x²) … the chain rule fills exactly this gap"）
learning_goal: 認清現有規則處理不了「函數套函數」的合成，連鎖律正是補這個洞、完成微分工具箱。
kind: motivation
narration: |
  We can now differentiate sine and cosine — but only in their bare form. We
  can handle $\sin x$, and yet nothing so far reaches $\sin(x^2)$, or
  $\sqrt{1+x^2}$, where one function is fed into another. We already built
  rules for sums, for products, for quotients — but never for composition, the
  operation of dropping one function inside another. That is the one gap left,
  and the chain rule fills it exactly. Once we have it, the whole toolkit for
  differentiation is finally complete.
visual_need: |
  對比卡：能做 $\sin x$；搆不到 $\sin(x^2)$、$\sqrt{1+x^2}$（一個函數餵進另一個）。
  Ch2 工具清單：和／積／商 ✓、composition ✗ → 連鎖律補上 ✗ 那格、工具箱 complete。
animation_cue: （無——靜態即可）
```

---

### unit: rates_multiply_intuition

```
id: rates_multiply_intuition
source: chapter3-print-standalone.html §3.2 · 開節 para 2（expansion:intuition，"Near a point, a differentiable function behaves like its tangent line … the two magnifications stack"）
learning_goal: 抓住連鎖律的核心直覺——可微函數近處像切線，串兩個函數時兩個放大率（斜率）疊乘。
kind: motivation
narration: |
  Here's the whole idea in one picture. Near a point, a differentiable
  function behaves like its tangent line — it takes a small change in its input
  and just scales it by its slope. The only catch is that this is approximate:
  there's an error, but the error shrinks faster than the change does. Now
  chain two such functions together. If $g$ scales a small increment $h$ by
  $g'(x)$, and then $f$ scales that result by $f'(g(x))$, the two
  magnifications stack — the composite scales $h$ by the product
  $f'(g(x))\,g'(x)$. That's the chain rule. And the proof, when we get
  to it, is nothing more than checking that the two small errors, once chained,
  are still negligible.
visual_need: |
  兩段放大示意：增量 $h$ → 過 $g$ 放大 $g'(x)$ → 再過 $f$ 放大 $f'(g(x))$ →
  合成放大 $f'(g(x))\,g'(x)$。標「兩個放大率疊乘 ＝ 連鎖律」。
animation_cue: （無——靜態即可；完整映射動畫交給 composed_mapping_figure）
```

---

### unit: chain_rule_statement

```
id: chain_rule_statement
source: chapter3-print-standalone.html §3.2 · Theorem 3.3（the chain rule）
learning_goal: 記住連鎖律的精確陳述：合成的導數＝外函數在內點的導數 × 內函數的導數。
kind: theorem
narration: |
  Let us state it precisely. Suppose $g$ is differentiable at a point $x_0$,
  and $f$ is differentiable at $g(x_0)$ — the place $g$ sends $x_0$ to. Then the
  composition $P(x)=f(g(x))$ is differentiable at $x_0$ as well, and its
  derivative is $P'(x_0)=f'(g(x_0))\,g'(x_0)$. Read it from the inside out: the
  derivative of the outer function, evaluated at the inner one, times the
  derivative of the inner function. We'll earn this with a proof a little
  later — for now, let's learn to use it.
visual_need: |
  Theorem 陳述卡：g 在 $x_0$ 可微、f 在 $g(x_0)$ 可微 ⇒ $P=f\circ g$ 在 $x_0$ 可微，
  $P'(x_0)=f'(g(x_0))\,g'(x_0)$。標「outer′(inner) × inner′」、「證明留後」。
animation_cue: （無——靜態陳述卡即可）
```

---

### unit: composed_mapping_figure

```
id: composed_mapping_figure
source: chapter3-print-standalone.html §3.2 · Figure 3.5（data-fig: composed-mapping；連鎖律＝合成映射，兩段局部斜率相乘）
learning_goal: 在「兩段放大」的合成映射圖上看見兩個局部斜率相乘＝複合的導數。
kind: visual
narration: |
  Picture the rule as a relay of two stretches. Start with a small increment
  $h$ sitting at $x_0$. The first function, $g$, carries it forward and
  stretches it to about $g'(x_0)\,h$ — a new increment, now sitting at
  $u_0=g(x_0)$. The second function, $f$, picks that up and stretches it again
  by its own slope there, landing at about $f'(g(x_0))\,g'(x_0)\,h$. Two
  stretches, one after the other — and stretching by one factor and then
  another simply multiplies the factors. That is why the composite's slope is
  the product of the two local slopes.
visual_need: |
  合成映射圖（三條平行軸：x-軸、u-軸、y-軸）：x₀ 處標增量 $h$；箭頭 $g$ 帶到 u-軸、
  增量伸縮為 $g'(x_0)\,h$（於 $u_0=g(x_0)$）；箭頭 $f$ 帶到 y-軸、再伸縮為
  $f'(g(x_0))\,g'(x_0)\,h$（於 $y_0$）。標兩段伸縮率、收尾標「兩率相乘」。
animation_cue: |
  建議動畫：先排出三條平行軸（x、u、y）。在 x₀ 標出一小段增量 $h$；沿箭頭 $g$
  把這段平移到 u-軸，同時把長度由 $h$ 伸縮成 $g'(x_0)\,h$（伸縮倍率可視覺強調）。
  再沿箭頭 $f$ 把它平移到 y-軸、長度伸縮成 $f'(g(x_0))\,g'(x_0)\,h$。最後把兩個
  伸縮倍率並排相乘，凸顯「一段接一段的伸縮 ＝ 倍率相乘」。
```

---

### unit: leibniz_form

```
id: leibniz_form
source: chapter3-print-standalone.html §3.2 · Remark 3.2（the Leibniz form；含「mnemonic-not-proof」告誡）
learning_goal: 認得連鎖律的 Leibniz 記法 $dy/dx=dy/du\cdot du/dx$，並知道「du 約掉」只是助記、不是證明。
kind: proposition
narration: |
  There's a second way to write the rule, and it's the one you'll actually
  compute with. Name the inner variable $u=g(x)$ and the output $y=f(u)$. Then
  the chain rule takes the memorable shape
  $\dfrac{dy}{dx}=\dfrac{dy}{du}\cdot\dfrac{du}{dx}$ — the rate of $y$ per $x$
  equals the rate of $y$ per $u$, times the rate of $u$ per $x$. It looks as
  though the $du$'s simply cancel, and that's a handy way to remember it — but
  it's not a proof. These are not fractions with a common factor to strike
  out; $\dfrac{dy}{du}$ and $\dfrac{du}{dx}$ are each limits. What truly makes
  the rule work is the error argument we are about to give, not a literal
  cancellation.
visual_need: |
  Leibniz 形式卡：$u=g(x)$、$y=f(u)$ ⇒ $\dfrac{dy}{dx}=\dfrac{dy}{du}\cdot\dfrac{du}{dx}$；
  白話唸法「(y per x) = (y per u)(u per x)」。
  告誡列：「$du$ 約掉」＝助記，**非**證明（$dy/du$、$du/dx$ 是極限、不是分數）。
animation_cue: （無——靜態卡即可；可短暫示意「$du$ 約掉」再打叉提醒非證明）
```

---

### unit: decomposition_strategy

```
id: decomposition_strategy
source: chapter3-print-standalone.html §3.2 · Strategy 3.1（differentiating a composition；ol.steps）
learning_goal: 學會「由外而內」分解合成式的固定步驟：認外函數、認內函數、外導乘內導，逐層重複。
kind: procedure
narration: |
  Here is a reliable way to take any composition apart — work from the outside
  in. First, spot the outermost operation: the very last thing you would do if
  you plugged in a number. Call that the outer function $f$. Whatever it is
  applied to is the inner function, $u=g(x)$. Differentiate the outer one at the
  inner one — that is $f'(g(x))$ — treating the whole inside as a single block
  you leave untouched for now. Then multiply by the derivative of that inside,
  $g'(x)$. And if the inside is itself a composition, just run the same steps on
  it again; every layer hands you one slope factor, and the factors all
  multiply. So for $\sqrt{1+x^2}$ the last operation is the square root — outer
  $\sqrt{\;}$, inner $1+x^2$; and for $\sin(x^2)$ the outer is sine, the inner
  is $x^2$.
visual_need: |
  步驟卡（祈使句，由外而內）：① 認最外層運算＝外函數 $f$ ② 裡頭＝內函數 $u=g(x)$
  ③ 作 $f'(g(x))$（內部當整塊不動）④ 乘 $g'(x)$ ⑤ 裡頭還是複合 → 重複①–④，
  每層一斜率因子、相乘。底部兩個分解例：$\sqrt{1+x^2}$（外 $\sqrt{\;}$、內 $1+x^2$）、
  $\sin(x^2)$（外 $\sin$、內 $x^2$）。
animation_cue: |
  （選用）建議動畫：拿一個合成式（如 $\sqrt{1+x^2}$），由最外層往內逐層用框
  把「外函數」與「內部整塊」框起來、依序點亮步驟①–④，最後在內部再框一次示意
  「裡頭還是複合就重複」。
```

---

### unit: proof_strategy_bridge

```
id: proof_strategy_bridge
source: chapter3-print-standalone.html §3.2 · "Why the rule is true" 引文（"The rule is already usable … repackage what differentiable means"）+ 開節 para 3（借用 product rule §2.5、可微⇒連續 §2.3）
learning_goal: 理解要證連鎖律得同時控制兩個函數的線性逼近，因此把「可微」重新打包成餘項形式；並知道我們借用積法則與「可微⇒連續」。
kind: motivation
narration: |
  The rule is already usable — now let's earn it. To prove that the two slopes
  really do multiply, we have to handle both functions' tangent-line
  approximations at once, and for that it helps to repackage what
  "differentiable" even means. Two facts from before we'll simply lean on,
  without re-proving them: the product rule, and the fact that a differentiable
  function is continuous. Now the repackaging. We earlier called $f$
  differentiable at $x_0$ when its difference quotient
  $\dfrac{f(x_0+h)-f(x_0)}{h}$ has a limit — and that limit is $f'(x_0)$. We're
  about to say exactly the same thing, only phrased as approximation by a
  straight line.
visual_need: |
  橋接卡：目標＝證「兩斜率相乘」→ 需同時握住兩個線性逼近 → 把「可微」改寫成餘項形式。
  借用工具列（標 given，不重證）：product rule、differentiable ⇒ continuous。
  舊定義（極限形式）回顧：$f$ 在 $x_0$ 可微 ⇔ $\dfrac{f(x_0+h)-f(x_0)}{h}$ 有極限 ＝ $f'(x_0)$。
animation_cue: （無——靜態橋接卡即可）
```

---

### unit: remainder_form_definition

```
id: remainder_form_definition
source: chapter3-print-standalone.html §3.2 · Definition 3.1（differentiability, remainder form）+ informal gloss
learning_goal: 認得可微的「餘項形式」：函數值＝切線值＋一個比 h 更快趨零的餘項。
kind: definition
narration: |
  Here is the form. We say $f$ is differentiable at $x_0$ if there is a number
  $m$ and a function $R$ so that $f(x_0+h)=f(x_0)+m\,h+R(h)$, with
  $\dfrac{R(h)}{h}\to 0$ as $h\to 0$. The number $m$ is just the derivative,
  $f'(x_0)$. Informally, it says $f(x_0+h)$ equals its tangent-line value,
  $f(x_0)+m\,h$, plus an error $R(h)$ that dies away faster than $h$ itself. So
  the tangent line is not merely close — it's close to first order, the error
  negligible next to $h$. That "faster than $h$" is the whole point, and it's
  exactly what lets these pieces compose.
visual_need: |
  Definition 卡：$f(x_0+h)=f(x_0)+m\,h+R(h)$，$\displaystyle\lim_{h\to0}\dfrac{R(h)}{h}=0$；$m=f'(x_0)$。
  白話列（informal gloss）：函數值 ＝ 切線值 $f(x_0)+m\,h$ ＋ 比 $h$ 更快消失的誤差 $R(h)$（first-order fit）。
animation_cue: （無——靜態卡即可；幾何在 remainder_tangent_figure 動畫呈現）
```

---

### unit: remainder_tangent_figure

```
id: remainder_tangent_figure
source: chapter3-print-standalone.html §3.2 · Figure 3.6（data-fig: remainder-tangent；可微＝一階貼合，間隙 R(h) 比 h 更快縮）
learning_goal: 在圖上看見餘項＝曲線與切線的垂直間隙，且 h 減半時間隙縮得遠比 h 快（R(h)/h→0 的幾何）。
kind: visual
narration: |
  Let us watch that error shrink. Draw the graph of $f$ near $x_0$, and draw
  its tangent line right alongside. At a nearby point $x_0+h$ the two do not
  quite agree, and the little vertical gap between them is exactly the remainder
  $R(h)$. Now halve $h$ — step in twice as close. The gap does not merely halve;
  it collapses far faster, shrinking to nothing next to $h$. That headlong
  shrinking is the picture of $\dfrac{R(h)}{h}\to 0$. And this single-curve
  picture is the local fact underneath the whole composition: up close, each
  function in the chain is almost exactly its own tangent line — and it is those
  straight-line parts whose slopes we get to multiply.
visual_need: |
  曲線 $y=f(x)$（實線）近 $x_0$ 貼著切線（虛線）；在 $x_0+h$ 標出兩者的垂直間隙 ＝ $R(h)$。
  第二格（或同框）把 $h$ 減半：間隙縮得遠比 $h$ 快 → 標「$R(h)/h\to0$」。
  收尾標：此為合成背後的單函數事實（每個函數近處≈自身切線，斜率相乘）。
animation_cue: |
  建議動畫：先畫曲線與其在 $x_0$ 的切線。在 $x_0+h$ 拉一條垂直線段、標其長為 $R(h)$。
  接著讓 $h$ 連續縮小（或一步減半）：明顯看到 $h$ 線性縮、而垂直間隙 $R(h)$ 縮得快得多，
  幾乎瞬間貼平，凸顯「間隙比 $h$ 更快趨零」＝ $R(h)/h\to0$。
```

---

### unit: two_forms_equivalent

```
id: two_forms_equivalent
source: chapter3-print-standalone.html §3.2 · Proposition 3.3（兩形式等價）+ Proof（雙向）
learning_goal: 看出兩種可微定義等價、且 m 相同——餘項形式不是新概念，只是改寫。
kind: proposition
narration: |
  Before we use this, let's check it's not a new idea — just the old one
  rewritten. The claim: the limit form and this remainder form are equivalent,
  and the $m$ is the same in both. One direction first. Suppose the limit form
  holds, with the difference quotient tending to $m$, and define
  $R(h)=f(x_0+h)-f(x_0)-m\,h$. Then $\dfrac{R(h)}{h}$ is just that difference
  quotient minus $m$, which goes to $m-m=0$ — so the remainder form holds, with
  the same $m$. The other direction runs backward: start from
  $f(x_0+h)=f(x_0)+m\,h+R(h)$, divide by $h$, and the difference quotient
  becomes $m+\dfrac{R(h)}{h}$, which goes to $m$. Same property, same
  derivative — two ways of saying one thing.
visual_need: |
  Proposition 陳述卡：極限形式（差分商有極限）⇔ 餘項形式（Definition 3.1），同一 $m=f'(x_0)$。
  證明，逐行 reveal（雙向）：
   1. (⇒) 設 $R(h)=f(x_0+h)-f(x_0)-m\,h$ ⇒ $\dfrac{R(h)}{h}=\dfrac{f(x_0+h)-f(x_0)}{h}-m\to m-m=0$。
   2. (⇐) $f(x_0+h)=f(x_0)+m\,h+R(h)$ ÷$h$ ⇒ $\dfrac{f(x_0+h)-f(x_0)}{h}=m+\dfrac{R(h)}{h}\to m$。
   3. ∴ 同性質、同導數（QED）。
animation_cue: （無——靜態陳述＋證明鏈即可）
```

---

### unit: proof_setup_substitution

```
id: proof_setup_substitution
source: chapter3-print-standalone.html §3.2 · Proof of Theorem 3.3 第一段（g、f 寫成餘項形式、代入、收線性項、其餘併 R₃ → 只剩 R₃/h→0）
learning_goal: 把兩個函數都寫成餘項形式、代入合成，看到線性項給出 g'·f'、其餘併成單一餘項 R₃，於是只剩證 R₃/h→0。
kind: proof
narration: |
  Now the proof itself, and the remainder form does the heavy lifting. Because
  $g$ is differentiable at $x_0$, write $g(x_0+h)=g(x_0)+m_1 h+R_1(h)$, where
  $m_1=g'(x_0)$ and $\dfrac{R_1(h)}{h}\to 0$. Because $f$ is differentiable at
  $g(x_0)$, apply its remainder form too — but with the increment
  $m_1 h+R_1(h)$ playing the role of $h$. That gives
  $P(x_0+h)=f(g(x_0))+m_2\bigl[m_1 h+R_1(h)\bigr]+R_2\bigl(m_1 h+R_1(h)\bigr)$,
  where $m_2=f'(g(x_0))$. Now collect the part that is linear in $h$ and sweep
  everything else into a single remainder $R_3$:
  $P(x_0+h)=P(x_0)+\bigl(g'(x_0)f'(g(x_0))\bigr)h+R_3(h)$, with
  $R_3(h)=m_2 R_1(h)+R_2\bigl(m_1 h+R_1(h)\bigr)$. Compare that with the
  remainder form: it says $P$ is differentiable at $x_0$ with exactly the
  derivative we want — provided we can show $\dfrac{R_3(h)}{h}\to 0$. That one
  limit is all that is left.
visual_need: |
  證明鏈，逐行 reveal（每行附理由）：
   1. $g(x_0+h)=g(x_0)+m_1 h+R_1(h)$，$m_1=g'(x_0)$，$\dfrac{R_1(h)}{h}\to0$（理由：g 可微，餘項形式）。
   2. $P(x_0+h)=f(g(x_0))+m_2[m_1 h+R_1(h)]+R_2(m_1 h+R_1(h))$，$m_2=f'(g(x_0))$（理由：f 餘項形式，增量＝$m_1 h+R_1(h)$）。
   3. 收線性項、其餘併 $R_3$：$P(x_0+h)=P(x_0)+(g'(x_0)f'(g(x_0)))h+R_3(h)$，$R_3=m_2 R_1(h)+R_2(m_1 h+R_1(h))$。
   4. 對照餘項形式 ⇒ $P'(x_0)=f'(g(x_0))g'(x_0)$，**只剩證** $\dfrac{R_3(h)}{h}\to0$（標為下一步目標）。
animation_cue: （無——靜態證明鏈即可；步驟 3「收線性項／掃進 R₃」可用顏色分群強調）
```

---

### unit: proof_easy_piece

```
id: proof_easy_piece
source: chapter3-print-standalone.html §3.2 · Proof of Theorem 3.3（R₃/h 拆兩塊；第一塊 m₂R₁(h)/h→0；附記 m₁h+R₁(h)→0）
learning_goal: 把 R₃/h 拆兩塊，看出第一塊（含常數 m₂）直接趨零；並記下內增量 m₁h+R₁(h)→0 供下一步。
kind: proof
narration: |
  Split that quotient into its two natural pieces:
  $\dfrac{R_3(h)}{h}=m_2\,\dfrac{R_1(h)}{h}+\dfrac{R_2(m_1 h+R_1(h))}{h}$. The
  first piece is easy. $m_2$ is just a constant, and $\dfrac{R_1(h)}{h}\to 0$
  because $g$ is differentiable, so that whole first piece goes to zero. And
  while we're here, note one thing for later: the inner increment
  $m_1 h+R_1(h)$ itself goes to zero as $h\to 0$ — $m_1 h$ does, and so does
  $R_1(h)$, since $\dfrac{R_1(h)}{h}\to 0$ forces $R_1(h)$ to zero as well. So
  the easy piece is settled; everything delicate now lives in the second piece.
visual_need: |
  推導，逐行 reveal：
   1. $\dfrac{R_3(h)}{h}=m_2\dfrac{R_1(h)}{h}+\dfrac{R_2(m_1 h+R_1(h))}{h}$（拆兩塊）。
   2. 第一塊：$m_2$ 常數、$\dfrac{R_1(h)}{h}\to0$ ⇒ $m_2\dfrac{R_1(h)}{h}\to0$（標「easy」）。
   3. 附記（標「keep for later」）：$m_1 h+R_1(h)\to0$（$m_1 h\to0$；$R_1(h)\to0$，因 $R_1(h)/h\to0$）。
   4. 第二塊 $\dfrac{R_2(m_1 h+R_1(h))}{h}$ 標「delicate → next」。
animation_cue: （無——靜態推導即可）
```

---

### unit: proof_delicate_choices

```
id: proof_delicate_choices
source: chapter3-print-standalone.html §3.2 · Proof of Theorem 3.3（棘手塊 ε-δ：選 δ、選 α；零情形 R₂(0)=0）
learning_goal: 對棘手塊起 ε-δ：用 R₂ 的定義選 δ、用內增量趨零選 α，並處理內增量恰為零的情形。
kind: proof
narration: |
  The second piece is the careful one — it is a remainder of $f$, but evaluated
  at that wobbling inner increment, then divided by $h$. Let us run an
  epsilon-delta argument. Fix any $\varepsilon>0$. First, since
  $\dfrac{R_2(y)}{y}\to 0$, there is a $\delta>0$ small enough that
  $\left|\dfrac{R_2(y)}{y}\right|<\varepsilon$ whenever $0<|y|<\delta$. Second,
  since the inner increment $m_1 h+R_1(h)$ goes to zero, there is an $\alpha>0$
  so that $|m_1 h+R_1(h)|<\delta$ whenever $0<|h|<\alpha$. Now take any $h$ with
  $0<|h|<\alpha$. One case is free. If that inner increment is exactly zero,
  then $R_2$ of zero is zero — the remainder relation forces $R_2(0)=0$ — so
  the piece is simply zero. So the only real work is the case where the inner
  increment is nonzero, and that is where we go next.
visual_need: |
  ε-δ 設定，逐行 reveal：
   1. 固定 $\varepsilon>0$。
   2. $\dfrac{R_2(y)}{y}\to0$ ⇒ ∃$\delta>0$：$0<|y|<\delta \Rightarrow \left|\dfrac{R_2(y)}{y}\right|<\varepsilon$。
   3. $m_1 h+R_1(h)\to0$ ⇒ ∃$\alpha>0$：$0<|h|<\alpha \Rightarrow |m_1 h+R_1(h)|<\delta$。
   4. 取 $0<|h|<\alpha$；零情形 $m_1 h+R_1(h)=0$ ⇒ $R_2(0)=0$ ⇒ 商 $=0$。
   5. 標「剩非零情形 → next」。
animation_cue: （無——靜態 ε-δ 設定即可；δ→α 的「先選誤差容忍、再回推 h 範圍」可用箭頭示意因果）
```

---

### unit: proof_delicate_bound

```
id: proof_delicate_bound
source: chapter3-print-standalone.html §3.2 · Proof of Theorem 3.3（非零情形：乘一除一分解、ε 界＋三角不等式、取 α₁ → (|m₁|+1)ε；合併 R₃/h→0，QED）
learning_goal: 非零情形用「乘一除一」分解、ε 界＋三角不等式界住，取 α₁ 收尾，得棘手塊→0，合併證畢。
kind: proof
narration: |
  Take the nonzero case, so $0<|m_1 h+R_1(h)|<\delta$. The trick is to multiply
  and divide by that inner increment, splitting the piece into two factors:
  $\dfrac{|R_2(m_1 h+R_1(h))|}{|h|}=\dfrac{|m_1 h+R_1(h)|}{|h|}\cdot\dfrac{|R_2(m_1 h+R_1(h))|}{|m_1 h+R_1(h)|}$.
  The second factor is below $\varepsilon$, straight from our choice of
  $\delta$. The first factor is $\left|m_1+\dfrac{R_1(h)}{h}\right|$, which the
  triangle inequality bounds by $|m_1|+\dfrac{|R_1(h)|}{|h|}$. So the whole
  piece is at most $\left(|m_1|+\dfrac{|R_1(h)|}{|h|}\right)\varepsilon$.
  Finally, since $\dfrac{R_1(h)}{h}\to 0$, shrink the window once more — pick an
  $\alpha_1$ so that $\dfrac{|R_1(h)|}{|h|}<1$ — and the bound becomes just
  $(|m_1|+1)\,\varepsilon$. That's a fixed constant times $\varepsilon$, and
  $\varepsilon$ was arbitrary, so this piece tends to zero too. Both pieces
  vanish, $\dfrac{R_3(h)}{h}\to 0$, and the chain rule is proved.
visual_need: |
  證明鏈，逐行 reveal：
   1. 非零：$0<|m_1 h+R_1(h)|<\delta$。
   2. 乘一除一：$\dfrac{|R_2(m_1 h+R_1(h))|}{|h|}=\dfrac{|m_1 h+R_1(h)|}{|h|}\cdot\dfrac{|R_2(m_1 h+R_1(h))|}{|m_1 h+R_1(h)|}$。
   3. 第二因子 $<\varepsilon$（由 $\delta$）；第一因子 $=\left|m_1+\dfrac{R_1(h)}{h}\right|\le|m_1|+\dfrac{|R_1(h)|}{|h|}$（三角不等式）。
   4. ⇒ $\le\left(|m_1|+\dfrac{|R_1(h)|}{|h|}\right)\varepsilon$；取 $\alpha_1$ 使 $\dfrac{|R_1(h)|}{|h|}<1$ ⇒ $<(|m_1|+1)\varepsilon$。
   5. $\varepsilon$ 任意 ⇒ 第二塊 $\to0$；合併 ⇒ $\dfrac{R_3(h)}{h}\to0$（QED：連鎖律成立）。
animation_cue: （無——靜態證明鏈即可；步驟 2 的「乘一除一」可短暫高亮分子分母同插入 $|m_1 h+R_1(h)|$）
```

---

### unit: example_single_composition

```
id: example_single_composition
source: chapter3-print-standalone.html §3.2 · Example 3.4 (a)(b)（√(1+x²)、sin(x²)）
learning_goal: 用 Strategy 套兩個一層合成：√(1+x²) 與 sin(x²)，明確標出內導數因子 2x。
kind: example
narration: |
  Time to use it — two quick ones. For $\sqrt{1+x^2}$, the outermost operation
  is the square root, so the outer function is $u^{1/2}$ and the inner is
  $1+x^2$. The outer derivative is $\tfrac12 u^{-1/2}$, the inner derivative is
  $2x$, and multiplying gives $\dfrac{1}{2\sqrt{1+x^2}}\cdot 2x$, which tidies to
  $\dfrac{x}{\sqrt{1+x^2}}$. For $\sin(x^2)$, the outer is sine and the inner is
  $x^2$; the outer derivative is cosine of the inside, the inner derivative is
  $2x$, so we get $\cos(x^2)\cdot 2x$, or $2x\cos(x^2)$. Notice that $2x$ in
  each — it is the inner derivative, and forgetting it is the single most common
  slip with the chain rule.
visual_need: |
  兩個推導並列／堆疊，逐行 reveal：
   (a) $\sqrt{1+x^2}$：外 $u^{1/2}$、內 $1+x^2$ → $\dfrac{1}{2\sqrt{1+x^2}}\cdot 2x=\dfrac{x}{\sqrt{1+x^2}}$。
   (b) $\sin(x^2)$：外 $\sin$、內 $x^2$ → $\cos(x^2)\cdot 2x=2x\cos(x^2)$。
  兩式各把內導數因子 $2x$ 高亮（標「inner derivative」）。
animation_cue: （無——靜態推導即可；兩式的 $2x$ 同色高亮，串到下一個 caution 單元）
```

---

### unit: caution_inner_derivative

```
id: caution_inner_derivative
source: chapter3-print-standalone.html §3.2 · Caution（頭號陷阱：漏內導數，cos(g(x)) 之誤）
learning_goal: 牢記頭號陷阱：只微分外函數、漏掉內導數因子 g'(x)。
kind: counterexample
narration: |
  Let's make that mistake explicit, so you never make it. The most common
  chain-rule error is to differentiate the outer function and then just stop —
  to write $\dfrac{d}{dx}\sin(g(x))$ as $\cos(g(x))$, full stop. That is wrong;
  the right answer is $\cos(g(x))\cdot g'(x)$. The inner factor $g'(x)$ — the
  $2x$ back in $\sin(x^2)$ — is never optional. Every layer you peel owes you
  one slope factor, and skipping even one leaves the derivative simply
  incomplete.
visual_need: |
  警示卡（✗ / ✓ 對照）：
   ✗ $\dfrac{d}{dx}\sin(g(x))=\cos(g(x))$（漏內導數）。
   ✓ $\dfrac{d}{dx}\sin(g(x))=\cos(g(x))\cdot g'(x)$。
  標：內因子 $g'(x)$（$\sin(x^2)$ 的 $2x$）永遠不可省。
animation_cue: （無——靜態警示即可；漏掉的 $g'(x)$ 因子可閃示補回）
```

---

### unit: example_nested_three_layers

```
id: example_nested_three_layers
source: chapter3-print-standalone.html §3.2 · Example 3.5（√(1+sin²x)，三層合成）
learning_goal: 把 Strategy 迭代到三層合成 √(1+sin²x)，看每層各出一個斜率因子相乘。
kind: example
narration: |
  Now let the inside be a composition too. Take $\sqrt{1+\sin^2 x}$ — three
  layers deep, because $\sin^2 x$ is itself $(\sin x)^2$. Peel from the outside:
  the square root of $1+\sin^2 x$ gives $\dfrac{1}{2\sqrt{1+\sin^2 x}}$ times the
  derivative of the inside. That inside derivative is the square of $\sin x$,
  which by the chain rule again is $2\sin x\cdot\cos x$. Put it together and we
  get $\dfrac{\sin x\cos x}{\sqrt{1+\sin^2 x}}$. Three layers, three factors —
  $\tfrac12 u^{-1/2}$ from the root, $2\sin x$ from the squaring, $\cos x$ from
  the sine — and they simply multiply down the chain.
visual_need: |
  推導鏈，逐行 reveal（三層；每層標出貢獻的因子）：
   1. $\dfrac{d}{dx}\sqrt{1+\sin^2 x}=\dfrac{1}{2\sqrt{1+\sin^2 x}}\cdot\dfrac{d}{dx}(1+\sin^2 x)$（外＝√）。
   2. $\dfrac{d}{dx}(1+\sin^2 x)=2\sin x\cdot\cos x$（中＝平方 → 鏈式；底＝$\sin$）。
   3. $=\dfrac{\sin x\cos x}{\sqrt{1+\sin^2 x}}$。
  收尾標三因子 $\tfrac12 u^{-1/2}$、$2\sin x$、$\cos x$（每層一因子、相乘）。
animation_cue: （無——靜態推導鏈即可；三個因子可由外而內依層點亮）
```

---

### unit: example_chain_times_quotient

```
id: example_chain_times_quotient
source: chapter3-print-standalone.html §3.2 · Example 3.6（√((x−1)/(x+2))，x>1；鏈式×商法則）
learning_goal: 看連鎖律的內導數本身是商法則計算——兩規則接力。
kind: example
narration: |
  Sometimes the inner derivative is a small problem of its own. Differentiate
  $\sqrt{\dfrac{x-1}{x+2}}$, for $x>1$. The outer operation is the square root
  and the inner is the fraction $\dfrac{x-1}{x+2}$, so the chain rule gives
  $\dfrac{1}{2\sqrt{(x-1)/(x+2)}}$ times the derivative of that fraction. And
  that derivative is a quotient rule:
  $\dfrac{(x+2)\cdot 1-(x-1)\cdot 1}{(x+2)^2}=\dfrac{3}{(x+2)^2}$. Tidy the front
  factor — $\dfrac{1}{2\sqrt{(x-1)/(x+2)}}$ is $\dfrac{\sqrt{x+2}}{2\sqrt{x-1}}$
  — multiply, and the answer is $\dfrac{3}{2\sqrt{x-1}\,(x+2)^{3/2}}$. The chain
  rule started the job; it took the quotient rule to finish the inner piece.
visual_need: |
  推導鏈，逐行 reveal：
   1. 外＝√、內＝$\dfrac{x-1}{x+2}$：$\dfrac{d}{dx}\sqrt{\dfrac{x-1}{x+2}}=\dfrac{1}{2\sqrt{(x-1)/(x+2)}}\cdot\dfrac{d}{dx}\!\left(\dfrac{x-1}{x+2}\right)$。
   2. 內導＝商法則：$\dfrac{(x+2)\cdot1-(x-1)\cdot1}{(x+2)^2}=\dfrac{3}{(x+2)^2}$。
   3. 整理前因子 $\dfrac{1}{2\sqrt{(x-1)/(x+2)}}=\dfrac{\sqrt{x+2}}{2\sqrt{x-1}}$。
   4. $=\dfrac{3}{2\sqrt{x-1}\,(x+2)^{3/2}}$（$x>1$）。
  標：內導本身是個小問題（商法則）。
animation_cue: （無——靜態推導鏈即可；內導數那一塊可框起標「a quotient rule of its own」）
```

---

### unit: example_chain_times_product

```
id: example_chain_times_product
source: chapter3-print-standalone.html §3.2 · Example 3.7（(1+x²)cos²x；積法則×鏈式）
learning_goal: 看積法則與連鎖律協作——外層是積、其中一個因子 cos²x 要鏈式。
kind: example
narration: |
  Same story, a different partner rule. Differentiate $y=(1+x^2)\cos^2 x$. The
  outermost operation here is a product, so start with the product rule:
  $y'=(2x)\cos^2 x+(1+x^2)\dfrac{d}{dx}(\cos^2 x)$. That leftover derivative
  needs the chain rule, since $\cos^2 x$ is $(\cos x)^2$ — outer is the
  squaring, inner is cosine — giving $2\cos x\cdot(-\sin x)=-2\sin x\cos x$. So
  $y'=2x\cos^2 x-2(1+x^2)\sin x\cos x$. The product rule split the work in two;
  the chain rule supplied the slope inside the second piece — neither alone
  would have done it.
visual_need: |
  推導鏈，逐行 reveal（repeat-pattern：「outer/inner」框架不重述）：
   1. 外＝積 → 積法則：$y'=(2x)\cos^2 x+(1+x^2)\dfrac{d}{dx}(\cos^2 x)$。
   2. $\cos^2 x=(\cos x)^2$ → 鏈式：$\dfrac{d}{dx}(\cos^2 x)=2\cos x\cdot(-\sin x)=-2\sin x\cos x$。
   3. $y'=2x\cos^2 x-2(1+x^2)\sin x\cos x$。
  標：積法則 + 連鎖律協作（缺一不可）。
animation_cue: （無——靜態推導鏈即可）
```

---

### unit: example_leibniz_rates

```
id: example_leibniz_rates
source: chapter3-print-standalone.html §3.2 · Example 3.8（kelp/urchin/otter；Leibniz 形式、符號沿鏈相乘）
learning_goal: 用 Leibniz 形式把「一連串依賴關係」的符號沿鏈相乘，判斷 dK/dO 的正負。
kind: example
narration: |
  Here is the Leibniz form earning its keep. In a harbour, the amount of kelp
  $K$ depends on the urchin population $U$ — urchins eat kelp — and $U$ depends
  on the otter population $O$, since otters eat urchins. We want the sign of
  $\dfrac{dK}{dO}$. Read off each link: more urchins means less kelp, so
  $\dfrac{dK}{dU}<0$; more otters means fewer urchins, so $\dfrac{dU}{dO}<0$.
  The chain rule chains the two rates:
  $\dfrac{dK}{dO}=\dfrac{dK}{dU}\cdot\dfrac{dU}{dO}$, a product of two negatives,
  which is positive. So $\dfrac{dK}{dO}>0$: more otters ultimately means more
  kelp. Each factor carries the sign of one link, and the signs just multiply
  along the chain.
visual_need: |
  依賴鏈圖：$O \to U \to K$（otters → urchins → kelp），每段標 sign。
  推導，逐行 reveal：
   1. $\dfrac{dK}{dU}<0$（urchins eat kelp）；$\dfrac{dU}{dO}<0$（otters eat urchins）。
   2. $\dfrac{dK}{dO}=\dfrac{dK}{dU}\cdot\dfrac{dU}{dO}$（Leibniz 形式鏈接）。
   3. 負×負 ＝ 正 ⇒ $\dfrac{dK}{dO}>0$（more otters → more kelp）。
animation_cue: |
  （選用）建議動畫：畫 $O\to U\to K$ 三節點兩箭頭，各箭頭打上「−」號；
  沿鏈把兩個「−」相乘浮出「＋」於 $O\to K$，凸顯「符號沿鏈相乘」。
```

---

### unit: toward_section_3_3

```
id: toward_section_3_3
source: chapter3-print-standalone.html §3.2 · 收尾散文（forward-ref：連鎖律解鎖反函數 ln/arcsin/arctan、對數微分 x^x）
learning_goal: 認清連鎖律不只是又一條規則，它是解鎖反函數、對數、指數新導數的鑰匙。
kind: forward_ref
narration: |
  With the chain rule in hand, any function you build by composing the
  elementary ones can now be differentiated, almost mechanically. But the rule does something more
  interesting next: it becomes a key. It unlocks derivatives we could not
  otherwise reach at all — the inverse functions $\ln x$, $\arcsin x$, and
  $\arctan x$ — and, through a clever trick called logarithmic differentiation,
  even something like $x^x$. That is where we head next.
visual_need: |
  「下一步解鎖」卡：連鎖律 → 新導數（目前搆不到）：$\ln x$、$\arcsin x$、$\arctan x$，
  以及對數微分下的 $x^x$。標「a key, not just another rule」。**MUST NOT 報節號。**
animation_cue: （無——靜態即可）
```

---

### unit: recap

```
id: recap
source: chapter3-print-standalone.html §3.2（全節重點凝煉；Key Takeaways 單元，有旁白）
learning_goal: 把本節串成一條線——一條規則（外導×內導）、Leibniz 記法、由外而內分解、頭號陷阱、餘項形式證明。
kind: recap
narration: |
  Let us gather the section. The chain rule differentiates a composition:
  $P'(x_0)=f'(g(x_0))\,g'(x_0)$ — the outer derivative at the inner function,
  times the inner derivative. In Leibniz form that is
  $\dfrac{dy}{dx}=\dfrac{dy}{du}\cdot\dfrac{du}{dx}$, the rates multiplying. To
  use it, decompose from the outside in; every layer contributes one slope
  factor. The number-one pitfall is dropping the inner derivative — never
  forget that factor. And underneath it all is a single clean idea: up close,
  each function is almost its tangent line, and the chain rule is just those
  local slopes multiplying.
visual_need: |
  Key Takeaways 卡片（5 點）＋ remember-formula 卡：
  points：
    • 連鎖律：$P'(x_0)=f'(g(x_0))\,g'(x_0)$（外導在內點 × 內導）。
    • Leibniz 形式：$\dfrac{dy}{dx}=\dfrac{dy}{du}\cdot\dfrac{du}{dx}$（rates 相乘）。
    • 用法：由外而內分解，每層一斜率因子、相乘。
    • 頭號陷阱：別漏內導數 $g'(x)$。
    • 為何成立：餘項形式——近處各函數≈切線，局部斜率相乘。
  formulas（保持短，避免出框）：
    • $P'(x_0)=f'(g(x_0))\,g'(x_0)$
    • $\dfrac{dy}{dx}=\dfrac{dy}{du}\cdot\dfrac{du}{dx}$
animation_cue: （無——靜態卡片即可）
```

---

### unit: outro

```
id: outro
source: chapter3-print-standalone.html §3.2（節末品牌字卡）
learning_goal: （收尾；無教學內容）
kind: recap
narration: （無——outro 為純動畫，無 takeaways）
visual_need: 兩段式 outro——暗轉亮橋接 → 最終 logo／節號／標題字卡（Next 3.3 Applications of the Chain Rule）。
animation_cue: （由 outro 模板處理）
```

---

## §7 拆解註記與內容層品質檢核

### 拆解／折疊決策（就近註明，杜絕 silent drop）

- **N1 — 開節 para 3「借用工具」（積法則 §2.5、可微⇒連續 §2.3）折進 `proof_strategy_bridge`。** 講義在 statement 前先聲明「take both as established and use them freely」；影片在進證明的橋接單元一句帶過（given，不重證），不獨立成場。
- **N2 — 「Why the rule is true」子節標題＋其後 intuition 散文折進 `proof_strategy_bridge` 與 `proof_setup_substitution` 的 lead-in。** 「The rule is already usable — the rest earns it」「With the remainder form available, the chain rule comes out by substitution」兩段過渡分別折入橋接與證明開場，不 silent drop。
- **N3 — Ex 3.7（chain×product）套 repeat-pattern。** 與 Ex 3.6（chain×quotient）同屬「連鎖律＋另一條規則協作」模式；第二個（3.7）以「Same story, a different partner rule」一句轉場，不重述「outer/inner」分解框架（§4 repeat-pattern）。**兩例皆保留**（不同 partner rule＝不同教學情形：商 vs 積；§2 代表式涵蓋判準「有沒有帶來新東西」），無 silent drop。
- **Caution 獨立成單元（未折疊）：** `caution_inner_derivative` 為標準誤解（頭號陷阱、ROADMAP #1 pitfall），依 §3「自成教學點才獨立」立一單元（kind: counterexample），緊接它隔離的對象 Ex 3.4。
- **Remark 3.2 升格為 `proposition` 單元（具名規則 Leibniz form）。** 依 §3「env-remark 具 env-name → 當輕量命題」；含「mnemonic-not-proof」告誡（ROADMAP pitfall），非 2 句短附註，故獨立。
- **Strategy 3.1 → `procedure` 單元（祈使句）。** 判斷型 strategy 含「裡頭還是複合就重複」的迭代分支，依 §3「MUST NOT 因分支拆多單元」由 narration 承載條件邏輯，單一單元。

### Definition 處理（忠實 ③ D5：Option B）

- 講義只鑄**餘項形式**為 Definition 3.1、把 §2.2 極限定義以散文交叉引用（不重編號）；等價性為 Proposition 3.3。內容稿照此：`remainder_form_definition`（Def 3.1）＋`two_forms_equivalent`（Prop 3.3＋雙向證），§2.2 極限定義在 `proof_strategy_bridge`／`two_forms_equivalent` 以白話回顧（**不報節號**）。

### 證明深度（使用者裁決：full ε-δ 全展開）

- Thm 3.3 證明忠實搬講義全部步驟（餘項代入 → 收線性項＋R₃ → R₃/h→0 拆兩塊 → 易塊 → 棘手塊 ε-δ：選 δ/α、零情形、乘一除一、三角不等式、α₁ 收尾）。為畫面可讀依 §3「>4 步拆 statement/proof」切 4 個 proof 單元（`proof_setup_substitution`／`proof_easy_piece`／`proof_delicate_choices`／`proof_delicate_bound`），每個收斂一個邏輯塊，讓學生能在塊間暫停。Prop 3.3 證另立 `two_forms_equivalent`。

### 視覺／動畫盤點（§5；§3.2 概念＋符號混合，medium——不套 symbol-heavy 例外）

- 整節非 ≥70% 符號：前段 statement/figure/Leibniz/strategy 與後段 5 個例子皆吃重教學圖與代數；證明段（Act 2）符號吃重但不主導全節。故**不套 §5 symbol-heavy 條件化**。
- 兩張講義圖全覆蓋並做動畫：Figure 3.5 → `composed_mapping_figure`（**客製 hook**：合成映射兩段伸縮）；Figure 3.6 → `remainder_tangent_figure`（**客製 hook**：間隙比 h 更快縮）。
- 吃重 `animation_cue`：composed_mapping_figure、remainder_tangent_figure（會動的概念才動：伸縮、間隙收斂）。其餘為靜態推導鏈／陳述卡。生成 manim code 視同 narration，**經使用者認可才定版**（§5），render 失敗走「由小到大逐層修補」——屬 Stage 2，本輪不做。

### 內容層 checklist（§7；本輪 Stage 1）

- [x] 每個 definition（3.1）／proposition（3.3、及 Leibniz 升格）／theorem（3.3）有單元覆蓋；每個不同模式 example（3.4–3.8）有代表單元，無同型 silent drop（Ex 3.6/3.7 repeat-pattern 已註明）。（L6 clean 確認）
- [x] 無 exercise 內容洩入（§3.2 無 env-exercise，自編例題即 worked example）。
- [x] intro（定位＋tagline）／recap（5 點 takeaway）／outro（無 takeaways）齊備。
- [x] 散文幾何主張（合成映射兩段伸縮、餘項＝切線間隙且更快縮）皆有視覺單元；其餘散文皆歸類折疊／升格，無 silent drop。
- [x] 每段環境之間散文已歸類（Incorporative／Bridge／Forward-pointing）。（L2 clean；fold notes N1–N3 經獨立複驗）
- [x] narration 為「說」而寫：開頭 hook、結尾 takeaway、未犯 §4 禁則（不報節號／圖號、不念螢幕標題、不用 see/as shown）；Ex 3.7 repeat-pattern 省 setup。（L3／L4 clean；toward_section_3_3 未報節號經確認）
- [x] 每個承載步驟在 `visual_need` 逐行列出（含理由）；數學不增刪、逐單元回溯講義。（L1 clean）
- [x] 數學讀得順（直讀 LaTeX 或白話；對齊鏈不重念 LHS）。
- [x] 動畫建議用自然語言、聚焦教學意圖（composed_mapping_figure／remainder_tangent_figure）。
- [x] 每個 id 唯一、snake_case、描述教學重點。
- [x] **六鏡稽核 → blocking==0**（Workflow `wf_d53afe59-4f2`；6 鏡全 clean、refute-by-default 後 0 tier-1/2 finding；**L5 隔離盲算** 每個 example 3.4–3.8、Prop 3.3 雙向、Thm 3.3 full ε-δ 全 match）。3 條 tier-3 advisory（不強制）：L1 prose-locus 引用（合規）、L2 proof_strategy_bridge 為最密單元（fold 正確，可選）、L3 register 偏正式 → 已交 copyedit。
- [x] **散文 copyedit pass（鎖稿前）**（`narration-copyedit`；C1–C5、語義不動）：6 tighten ＋ 9 optional **全採納**——register relax（多處 full-form → 縮寫，對齊 §4 口語預設與 §3.1 peer，保留 deliberate-formal proof 開場）、rates_multiply C2「the product/That product」去重、proof_delicate_choices C4「One case is free」斷句、toward_section_3_3 C5 去與開節「toolkit complete」回音（保留「any function … differentiated, almost mechanically」忠實句）。語義/數學未動。
- [x] **編譯 `ch03_chain_rule_narration.html` 審核稿**（24 單元，採納 copyedit 後重編）：數學渲染正確、與 `.md` 一致。
- [x] **使用者 sign-off（2026-06-29）→ LOCKED**（之後 NFA 把關；post-lock 改稿跑 scoped NFA 回歸）。
```
