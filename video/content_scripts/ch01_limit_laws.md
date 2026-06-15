# Section 1.5 Limit Laws and Computational Techniques — 內容稿（正式版）

> **性質：正式產線內容稿**。依 REBUILD_STATUS「2026-06-13 全章影片計畫」啟動 §1.5（Phase 2 難度遞增序列 §1.3 → §1.4 → §1.2 → §1.5 → §1.6 之第四節）。以 HTML 講義權威檔逐節拆解、撰寫；narration **已於 2026-06-14 經使用者認可**（採 19 單元＋u15 口語收尾），工程稿已落地為 `storyboards/ch01_limit_laws.yml`。
> **來源（權威）：** [`../../handout/chapter1-print-standalone.html`](../../handout/chapter1-print-standalone.html) §1.5（`sec-no` 1.5，Limit Laws and Computational Techniques；編輯源 `fragments/ch01/sec-1-5.html`）。
> **deck id：** `ch01_limit_laws`（沿 §1.1 `ch01_inverse_functions`／§1.2 `ch01_inverse_trig`／§1.3 `ch01_limit_of_function`／§1.4 `ch01_one_sided_infinite`／§1.6 `ch01_precise_limit` 命名慣例）。
> **格式：** 純內容層，每單元 `id / source / learning_goal / kind / narration / visual_need / animation_cue`；**不含** template / `{show}` / accent / 視覺 payload（第二階段才填）。`narration` 為英文（旁白語言）；`visual_need` / `animation_cue` 為中文（內容溝通用）。客製動畫由 Claude 依 `animation_cue` 生成、經認可後接入工程稿 `# HOOK`。
> **複雜度定位（REBUILD_STATUS）：** 高複雜度、~75% 符號、建議 20–24 單元；教學重量主體為代數操作（極限律、直接代入、化簡不定式），幾何只在兩個子題目（piecewise 跳斷、squeeze 夾擠）為真——**套 §5 symbol-heavy 條件化例外**：squeeze 幾何＝anchor、$x^2\sin(1/x)$ 演示＝其 in-action、floor 跳斷＝唯一對比視覺；代數例題（u4/u6/u8/u9/u10/u17）與 squeeze 第二例（u15，$|x|$ 變體）**一律不配圖**，符號本身就是 beat。**新工程缺口（lazy build，第二階段）：floor 階梯／squeeze 三曲線／$x^2\sin(1/x)$ 包絡（多半 `graph_focus` 可吃）。**

---

## Deck meta（intro / outro 用）

```
chapter:       Chapter 1
chapter_title: Inverse Functions and Limits
section:       1.5
title:         Limit Laws and Computational Techniques
tagline:       Which limits can we just compute — and what do we do when substitution fails?
sections:      [1.1 Inverse Functions, 1.2 Inverse Trigonometric Functions,
                1.3 The Limit of a Function, 1.4 One-Sided and Infinite Limits,
                1.5 Limit Laws and Computational Techniques,
                1.6 The Precise Definition of a Limit]
```

---

## 教學單元

### 1. intro
- **source:** §1.5 整節 + 章定位（standalone `<title>`：Chapter 1 — Inverse Functions and Limits）
- **learning_goal:** —（純品牌開場）
- **kind:** `intro`
- **narration:** —（intro 無旁白）
- **visual_need:** Section Gate：章地圖聚焦 §1.5 → 標題 “Limit Laws and Computational Techniques” + tagline “Which limits can we just compute — and what do we do when substitution fails?”
- **animation_cue:** —（用 gen-2 既有 intro 模板）

### 2. from_guessing_to_computing
- **source:** chapter1-print-standalone.html §1.5 · opening prose（“In the previous sections we used tables and graphs to guess … We now record algebraic properties … a reliable tool-kit”）
- **learning_goal:** 理解本節的轉向——從用表格／圖像「猜」極限，改為用一組代數規則「算」極限。
- **kind:** `motivation`
- **narration:**
  > Up to now, every limit we have found came from a guess. We built a table of values, or we read a graph, and we inferred where the function seemed to be heading. That works, but it is slow, and it is never quite certain. In this section we change tactics: we collect a handful of algebraic rules that let us compute limits directly, with no table and no graph. These rules can be justified rigorously once we have the precise definition of a limit — that comes a little later — but even now, before any proof, they give us a dependable tool-kit for the limits we meet in practice.
- **visual_need:** 左側一張帶洞的數值表／粗略草圖（標「guess」），右側一行代數運算直達答案（標「compute」）；中間一個箭頭由表格指向算式，示意「估計 → 計算」的轉向。
- **animation_cue:** 左邊的數值表逐列填、停在問號（估計感）；箭頭亮起後右邊一行代數計算一筆寫到底、落在確定的答案上，凸顯「不再靠猜」。
- **備註（§3）：** opening prose 第一段 promote 成 motivation 單元。「justified rigorously once we have the precise definition … (see the next section)」與第三段（L1371）的「proved … in the next section」皆為向前語意，**fold 進此單元 takeaway 並改白話「that comes a little later」、不報節號**（§4 禁則）。

### 3. limit_laws
- **source:** chapter1-print-standalone.html §1.5 · Theorem 1.2（Limit laws：sum／difference／constant multiple／product／quotient／power）+ 其後 “Verbally: …” prose
- **learning_goal:** 掌握極限律——只要兩個極限都存在，和／差／常數倍／積／商／整數次方的極限，就等於各別極限的相同組合（商需分母極限非零）。
- **kind:** `theorem`
- **narration:**
  > Here is the heart of the tool-kit. Suppose both $\lim_{x \to a} f(x)$ and $\lim_{x \to a} g(x)$ exist. Then the limit slips straight through the basic operations. The limit of a sum is the sum of the limits; the same holds for a difference, and for a constant times a function. The limit of a product is the product of the limits. The limit of a quotient is the quotient of the limits — with one proviso: the denominator's limit must not be zero. And raising to a positive integer power behaves the same way, the limit of $[f(x)]^n$ being just $[\lim_{x \to a} f(x)]^n$. In plain words: every operation you already know commutes with taking the limit, as long as the individual pieces have limits to begin with.
- **visual_need:** 極限律總表（六條上下排列，左欄式子、右欄一句白話）：sum、difference、constant multiple、product、quotient（標紅字 “if $\lim g \ne 0$”）、power（$n$ 為正整數）。Theorem 標題列。
- **animation_cue:** —（靜態表即可；逐條揭示由工程層模板承載。）
- **備註（§2／§3）：** Theorem 1.2 為單一定理、無證明（證明留待下節），合一單元；narration **不逐字念表**（§4 禁則「逐字念條列」），改用白話轉述六條規律。“Verbally:” prose 即現成白話、fold 進 narration body。

### 4. apply_laws_abstractly
- **source:** chapter1-print-standalone.html §1.5 · Example 1.26 + Solution（$\lim_{x\to-1}f=-1$ → $\lim\frac{xf(x)+3}{2f(x)+1}=-4$）
- **learning_goal:** 看出極限律是「結構性」的——只知道一個極限值、沒有 $f$ 的公式，仍能算出一整個組合式的極限。
- **kind:** `example`
- **narration:**
  > Let us put the laws to work in a case where we are handed almost nothing. Suppose all we know is that $f(x) \to -1$ as $x \to -1$ — no formula, just that one limit. Can we still evaluate $\lim_{x \to -1} \frac{x f(x) + 3}{2 f(x) + 1}$? We can, entirely through the laws. By the product law, $x f(x)$ tends to $(-1)(-1)$, which is $1$, so the numerator tends to $1 + 3 = 4$. The denominator, $2 f(x) + 1$, tends to $2(-1) + 1$, which is $-1$ — and, crucially, that is not zero, so the quotient law is allowed. The whole expression tends to $4$ over $-1$, or $-4$. Notice we never needed to know what $f$ actually is; the laws carried the entire computation.
- **visual_need:** 已知 $\lim_{x\to-1}f(x)=-1$；分子推理 $xf(x)\to(-1)(-1)=1$、$+3\to4$；分母 $2f(x)+1\to-1$（標「$\ne 0$ ✓ → quotient law」）；結論 $\dfrac{4}{-1}=-4$。
- **animation_cue:** —（靜態即可；符號推理本身就是 beat，§5 不配圖。）
- **備註（§2 代表式涵蓋／§5）：** Example 1.26（expansion）帶來新模式「抽象套用極限律、無 $f$ 公式」，獨立成單元。純符號、不配圖（§5）。

### 5. direct_substitution
- **source:** chapter1-print-standalone.html §1.5 · prose（“A first consequence … behave in the easiest way possible”）+ Proposition 1.6（$\lim x=a$、$\lim x^n=a^n$、polynomial → $p(a)$、rational → $r(a)$）+ prose（“direct substitution is therefore the fastest route”）
- **learning_goal:** 知道極限律的直接推論——多項式、以及分母在 $a$ 不為零的有理函數，求極限就是把數字代進去（直接代入）。
- **kind:** `proposition`
- **narration:**
  > The laws have one immediate, very useful payoff. Begin with two facts that are almost self-evident: as $x$ approaches $a$, the function $x$ approaches $a$, and therefore $x^n$ approaches $a^n$. Feed those into the sum and product laws, and a whole class of functions falls into line. For any polynomial $p$, the limit as $x \to a$ is simply $p(a)$ — you get it by substitution. And for a rational function, a ratio of two polynomials, the same is true wherever the denominator is not zero at $a$: the limit is just the function's value there. So for polynomials and well-behaved rational functions, finding a limit is nothing more than plugging in the number. We call that direct substitution, and it should always be the first thing you try.
- **visual_need:** Proposition 標題列；基石 $\lim_{x\to a}x=a$、$\lim_{x\to a}x^n=a^n$；推論 $\lim_{x\to a}p(x)=p(a)$（polynomial）、$\lim_{x\to a}r(x)=r(a)$（rational，標「if $r(a)$ defined」）；底部標語「direct substitution — try this first」。
- **animation_cue:** —（靜態即可。）
- **備註（§3）：** 前 prose「A first consequence …」為 incorporative lead-in、後 prose「direct substitution is therefore the fastest route」為 takeaway，皆 fold 進本單元。Prop 1.6 與其演示例（Example 1.27）分拆為兩單元（規則 vs 套用），避免單元過載、且 u6 可用 repeat-pattern 省 setup。

### 6. direct_sub_in_action
- **source:** chapter1-print-standalone.html §1.5 · Example 1.27 + Solution（$\lim_{x\to1}\frac{x^3+2x^2-1}{5-3x}=1$）
- **learning_goal:** 在分母不為零的有理函數上實際執行直接代入。
- **kind:** `example`
- **narration:**
  > Take it for a spin on $\lim_{x \to 1} \frac{x^3 + 2x^2 - 1}{5 - 3x}$. Top and bottom are both polynomials, so each we evaluate by substitution. The numerator at $x = 1$ is $1 + 2 - 1$, which is $2$; the denominator is $5 - 3$, also $2$. The denominator's limit is two, not zero, so the quotient law applies and the answer is $2$ over $2$ — simply $1$. No table, no graph: one substitution and a glance at the denominator.
- **visual_need:** $\lim_{x\to1}\dfrac{x^3+2x^2-1}{5-3x}$；分子 $\to1+2-1=2$、分母 $\to5-3=2$（標「$\ne 0$」）；結論 $\dfrac{2}{2}=1$。
- **animation_cue:** —（靜態即可；§5 純符號不配圖。）
- **備註（§4 repeat-pattern）：** 直接代入規則已於 u5 建立，本單元 **不重述** setup，一句轉場「Take it for a spin」直接進計算。

### 7. why_zero_over_zero
- **source:** chapter1-print-standalone.html §1.5 · prose（“When direct substitution produces an indeterminate form such as $\tfrac00$ …”）+ Example 1.28 + Solution（$\tfrac00$ 可等於任何值）
- **learning_goal:** 理解 $\tfrac00$ 為何叫「不定式」——上下都趨零並不能決定比值，它可以是任何結果——因此判斷前必須先化簡。
- **kind:** `counterexample`
- **narration:**
  > Substitution is not always so kind. Very often the top and the bottom both head to zero, and you are left staring at zero over zero. The temptation is to call that one, or maybe zero — but neither is right, and here is why. Suppose $f$ and $g$ both tend to zero as $x \to 3$; what can their ratio do? If $f$ is ten times $g$ — say $f(x) = 10(x - 3)$ and $g(x) = x - 3$ — the ratio is ten everywhere, so the limit is ten. Replace ten by any constant you please, and the limit is that constant. Make the bottom shrink faster and the ratio blows up to infinity; flip a sign and it runs to minus infinity; pit $x - 3$ against $|x - 3|$ and the limit fails to exist at all. So zero over zero can come out as anything — which is precisely what indeterminate means. It is not an answer; it is a signal that we must reshape the expression before the limit will reveal itself.
- **visual_need:** 中央大字 $\dfrac00$ 標「indeterminate」；四個分岔卡：$\tfrac{10(x-3)}{x-3}\to10$（任意常數 $c$）、$\to+\infty$、$\to-\infty$、$\tfrac{x-3}{|x-3|}$ → DNE；底部一句「$\tfrac00$ = a signal to simplify, not an answer」。
- **animation_cue:** 中央 $\tfrac00$ 向外迸出四條分支，各自落到不同結局（$c$／$+\infty$／$-\infty$／DNE）依序亮起，凸顯「同樣是 $\tfrac00$，答案卻可以是任何東西」。
- **備註（§2／§7）：** Example 1.28（expansion）為概念性反例（「為何 $\tfrac00$ 不定」），屬 §7 反例項，獨立成 `counterexample` 單元——它是整個「代數化簡」子題的動機。前 prose「first simplify then take the limit」fold 進 lead-in。

### 8. factor_and_cancel
- **source:** chapter1-print-standalone.html §1.5 · Example 1.29 + Solution（$\lim_{x\to1}\frac{x-1}{x^2-1}=\tfrac12$，factor & cancel）
- **learning_goal:** 用「因式分解、約去」處理 $\tfrac00$ 不定式——消掉製造零的公因式後再代入。
- **kind:** `example`
- **narration:**
  > So when substitution gives zero over zero, our job is to rewrite the expression into a form substitution can handle — and the cleanest tool is factoring. Take $\lim_{x \to 1} \frac{x - 1}{x^2 - 1}$. Put in one and you get zero over zero, so factor the bottom: $x^2 - 1$ is $(x - 1)(x + 1)$. Now the troublesome $x - 1$ cancels top and bottom, and away from $x = 1$ the expression is just $\frac{1}{x + 1}$. That cancelled form agrees with the original at every point near one — which is all a limit ever looks at — so we substitute into it: $\frac{1}{1 + 1}$, one half. The factor that was forcing the zero is gone, and the limit simply appears.
- **visual_need:** $\dfrac{x-1}{x^2-1}\xrightarrow{\text{sub}}\tfrac00$；分解 $x^2-1=(x-1)(x+1)$；約去 $x-1$ → $\dfrac{1}{x+1}$（標「$x\ne1$」）；代入 $\dfrac{1}{1+1}=\tfrac12$。
- **animation_cue:** —（靜態即可；化簡鏈本身就是 beat，§5 純符號不配圖。`derivation` 模板可承載逐行揭示。）
- **備註（§2／§3 邊角）：** Example 1.29 帶來新技巧「factor & cancel」，獨立成單元。「$x\ne1$」忠實保留為「agrees at every point near one」（極限只看 $a$ 附近、不看 $a$ 本身）。

### 9. rationalize_numerator
- **source:** chapter1-print-standalone.html §1.5 · Example 1.30 + Solution（$\lim_{t\to0}\frac{\sqrt{t^2+9}-3}{t^2}=\tfrac16$，rationalise）
- **learning_goal:** 用「有理化（乘共軛）」處理含根號的 $\tfrac00$——清掉根號、逼出可約的公因式。
- **kind:** `example`
- **narration:**
  > Factoring is not the only way to break a zero over zero. When a square root is in the way, the move is to rationalise. Consider $\lim_{t \to 0} \frac{\sqrt{t^2 + 9} - 3}{t^2}$ — again zero over zero. Multiply top and bottom by the conjugate, $\sqrt{t^2 + 9} + 3$. The numerator becomes a difference of squares, $t^2 + 9 - 9$, which is just $t^2$ — and that $t^2$ cancels the one downstairs. What is left is $\frac{1}{\sqrt{t^2 + 9} + 3}$, and now substitution is harmless: at $t = 0$ the root is three, giving $\frac{1}{3 + 3}$, one sixth. The conjugate did the same job the factoring did — it exposed the hidden factor and let it cancel away.
- **visual_need:** $\dfrac{\sqrt{t^2+9}-3}{t^2}\xrightarrow{\text{sub}}\tfrac00$；乘共軛 $\dfrac{\sqrt{t^2+9}+3}{\sqrt{t^2+9}+3}$；分子 $t^2+9-9=t^2$ 約去 → $\dfrac{1}{\sqrt{t^2+9}+3}$；代入 $\dfrac{1}{3+3}=\tfrac16$。
- **animation_cue:** —（靜態即可；§5 純符號不配圖。）
- **備註（§4 repeat-pattern）：** 「$\tfrac00$ → 化簡」的 setup 已於 u8 建立，本單元 **不重述**，直接進「換一招：有理化」（一句轉場），凸顯新技巧本身。

### 10. combine_fractions
- **source:** chapter1-print-standalone.html §1.5 · Example 1.31 + Solution（$\lim_{t\to\frac12}\frac{\frac{1}{3t^2}+\frac{1}{t^2-1}}{2t-1}=-\tfrac{32}{9}$，combine fractions）
- **learning_goal:** 用「先通分合併內層分數」處理複合分數的 $\tfrac00$——合併後浮現可約的公因式。
- **kind:** `example`
- **narration:**
  > One more flavour of the same idea, for when the expression is a pile of fractions. Look at the limit as $t$ approaches one half of $\frac{\frac{1}{3t^2} + \frac{1}{t^2 - 1}}{2t - 1}$. Substitution gives zero over zero once again. The fix is to tidy the numerator first: put the two inner fractions over the common denominator $3t^2(t^2 - 1)$, and the top collects into $4t^2 - 1$ — which factors as $(2t - 1)(2t + 1)$. There is our cancelling factor: the $2t - 1$ on top kills the $2t - 1$ in the main denominator. Substitute $t = \tfrac12$ into what remains, and the limit works out to $-\tfrac{32}{9}$. Three examples, one lesson: before a stubborn limit will budge, reshape it by algebra until the factor forcing the zero cancels away.
- **visual_need:** $\dfrac{\frac{1}{3t^2}+\frac{1}{t^2-1}}{2t-1}\xrightarrow{\text{sub}}\tfrac00$；通分分子 $=\dfrac{4t^2-1}{3t^2(t^2-1)}=\dfrac{(2t-1)(2t+1)}{3t^2(t^2-1)}$；約去 $2t-1$ → $\dfrac{2t+1}{3t^2(t^2-1)}$；代入 $t=\tfrac12$ → $-\dfrac{32}{9}$。
- **animation_cue:** —（靜態即可；§5 純符號不配圖。）
- **備註（§4 repeat-pattern／§2）：** Example 1.31（expansion）帶來第三個化簡技巧「combine fractions」，獨立成單元；setup 不重述。末句為「代數化簡」三例（u8/u9/u10）的綜合 takeaway——同一課（reshape until the troublesome factor cancels）、三種招式，**收束本子題、不另立 summary 單元**。

### 11. piecewise_limits_agree
- **source:** chapter1-print-standalone.html §1.5 · prose（“Some limits are easiest to analyse by splitting into cases”）+ Example 1.32 + Solution（$\lim_{x\to0}|x|=0$，兩側一致）
- **learning_goal:** 用「兩個單側極限，各在自己的分支上算，再檢查是否一致」處理 piecewise 函數的極限。
- **kind:** `example`
- **narration:**
  > Not every function comes as a single formula. Some are defined in pieces, with different rules on different sides — and there the trick is to take the limit one side at a time. The plainest example is the absolute value, $|x|$, as $x$ approaches zero. To its right, $|x|$ is just $x$, which heads to zero. To its left, $|x|$ is $-x$, which also heads to zero. The two one-sided limits agree — both are zero — so the full two-sided limit exists and equals zero. The recipe is general: for a piecewise function, work out the limit from each side on the branch that applies there, and the ordinary limit exists exactly when those two answers match.
- **visual_need:** $|x|=\begin{cases}x,&x\ge0\\-x,&x<0\end{cases}$；$\lim_{x\to0^+}|x|=\lim x=0$、$\lim_{x\to0^-}|x|=\lim(-x)=0$；兩側相等 → $\lim_{x\to0}|x|=0$。
- **animation_cue:** —（靜態即可；簡單對稱、§5 不配圖，動態留給 u12 的真跳斷。）
- **備註（§3）：** 前 prose「split into cases」為 incorporative lead-in、fold 進此。本單元（兩側一致）與 u12（兩側相異）成對——先正面建立「兩側一致 → 極限存在」，再以 floor 反面演「兩側相異 → 不存在」。§1.4 單側極限為自足回扣、**不報節號**（§4）。

### 12. floor_function_jump
- **source:** chapter1-print-standalone.html §1.5 · Example 1.33 + Solution（$\lim_{x\to3}[x]$ DNE，兩側 $3\ne2$）+ Figure 1.18（data-fig: floor-function）
- **learning_goal:** 看一個兩側單側極限相異的 piecewise 情形——最大整數函數在每個整數跳一階——所以極限不存在。
- **kind:** `example`
- **narration:**
  > The same one-sided approach also tells us when a limit does not exist. Meet the greatest integer function, written $[x]$: it rounds down to the nearest integer, so $[4]$, $[4.1]$, and $[4.8]$ are all four. Ask for its limit as $x$ approaches three. Coming from the right, $x$ sits just above three, so $[x]$ is three. Coming from the left, $x$ sits just below three — not yet arrived — so $[x]$ is only two. The two sides give different answers, three and two, so the limit at three does not exist. And the staircase shows you why: at every integer the function leaps up by a whole step, and no single value can bridge a jump.
- **visual_need:** 最大整數函數 $y=[x]$ 的階梯圖（每整數一階，左實心端點、右空心端點）；focus 在 $x=3$：右側階值 $3$（實心 $(3,3)$）、左側階值 $2$（空心 $(3,2)$）；兩虛線拉到 $y$ 軸標 $3$、$2$；標「jump = 1 → limit DNE」。（重繪講義 Figure 1.18。）
- **animation_cue:** 兩個動點同時逼近 $x=3$：from the right 沿 $y=3$ 那階滑近 $(3,3)$（實心）、from the left 沿 $y=2$ 那階滑近 $(3,2)$（空心）；停住時兩條水平虛線拉到 $y$ 軸、夾出大小 $1$ 的縫隙閃示，凸顯「跨不過跳階 → 極限不存在」。
- **備註（§2／§5）：** Example 1.33 帶來新模式「兩側相異 → DNE」，與 u11 互補，獨立成單元。**此為 §5 條件化下的唯一「對比視覺」**——破壞「兩側一致」假設、極限失效的情形（§5「對比本身就是這課」）。Figure 1.18 重繪。

### 13. squeeze_theorem
- **source:** chapter1-print-standalone.html §1.5 · prose（“The limit laws require that both constituent limits exist, but sometimes one of the factors has no limit … trap the expression between two simpler functions”）+ Theorem 1.3（Squeeze theorem）+ Figure 1.19（data-fig: squeeze-theorem）
- **learning_goal:** 掌握夾擠定理——若一函數被夾在兩個有共同極限 $L$ 的函數之間，它被迫趨於同一個 $L$——用於極限律無法施力的情形。
- **kind:** `theorem`
- **narration:**
  > Here is a technique for limits the laws simply cannot reach. Sometimes a function is built from a piece that has no limit at all, so the product or quotient laws are off the table. The squeeze theorem rescues exactly these cases, and the picture is the whole idea. Suppose our function $f$ is trapped between a lower function $g$ and an upper function $h$ for all $x$ near $a$. If $g$ and $h$ are themselves both heading to the same value $L$ as $x \to a$, then $f$, caught between them, has nowhere else to go — it is squeezed to $L$ as well. The two outer functions close in like a vice, and whatever is pinned between them is dragged to the same limit.
- **visual_need:** 夾擠示意圖：上界 $h$、下界 $g$ 兩曲線在 $x=a$ 處交會於高度 $L$；中間 $f$ 在其間（可帶輕微擺動）被夾住、同樣抵達 $(a,L)$；標 $g\le f\le h$、$\lim g=\lim h=L$。（重繪講義 Figure 1.19。）
- **animation_cue:** 上界 $h$ 與下界 $g$ 自兩側朝 $(a,L)$ 收攏、像鉗子般夾近；夾縫中的 $f$ 被擠得越來越窄、最後被釘在 $(a,L)$；交會點短暫高亮，凸顯「無處可逃」。
- **備註（§5 anchor／§3）：** 前 prose「laws require both limits exist …」為 incorporative lead-in、fold 進此。Theorem 1.3 與其演示例（u14）分拆（定理 vs 套用），讓學生能在陳述後暫停（§3）。**此為 §5 條件化下的 anchor 視覺**——本節核心幾何直覺。

### 14. squeeze_in_action
- **source:** chapter1-print-standalone.html §1.5 · Example 1.34 + Solution（$\lim_{x\to0}x^2\sin\frac1x=0$）+ Figure 1.20（data-fig: squeeze-x2sin）
- **learning_goal:** 把夾擠定理套到 $x^2\sin(1/x)$——用 $\pm x^2$ 夾住狂震的振盪、兩界皆趨零——並看見包絡把它捏到原點。
- **kind:** `example`
- **narration:**
  > Let us watch the squeeze catch a genuinely wild function: $\lim_{x \to 0} x^2 \sin\!\frac{1}{x}$. The factor $\sin\frac1x$ oscillates faster and faster as $x$ nears zero — it has no limit, so the product law is useless. But it never escapes the band between minus one and one. Multiply that bound by $x^2$, which is never negative, and we get $-x^2 \le x^2 \sin\frac1x \le x^2$. Now both bounding functions, $-x^2$ and $x^2$, go to zero as $x \to 0$ — so the squeeze theorem pins our function to zero as well. The parabola $x^2$ and its mirror $-x^2$ form a closing envelope, and the frantic wiggling of the curve is trapped inside it, forced right down to the origin.
- **visual_need:** $y=x^2$、$y=-x^2$ 兩拋物線形成包絡；$y=x^2\sin(1/x)$ 在其間越近 $0$ 振盪越密、被夾向原點；標 $-x^2\le x^2\sin\frac1x\le x^2$、$\lim(\pm x^2)=0$ → 夾擠 $\to0$。（重繪講義 Figure 1.20。）
- **animation_cue:** 先畫 $\pm x^2$ 包絡；$x^2\sin(1/x)$ 曲線由外向 $0$ trace 出來、振盪在包絡內越收越密；包絡兩支朝原點夾合，把曲線捏到 $(0,0)$，凸顯「被夾到零」。
- **備註（§2 代表式涵蓋／§5）：** Example 1.34 為夾擠定理的代表演示（anchor in-action），唯一深入演示的代數例題配圖（§5 anchor 的 in-action）。其後同型的 Example 1.35（$x\cos\frac1x$）原折疊於本單元末句；**使用者 2026-06-14 認可拆回獨立單元 u15**（演 $|x|$ 變體、強化「同手法、不同界」）——故本單元末句已移除折疊句、收於 $x^2\sin$ 的包絡結論。

### 15. squeeze_abs_value_bound
- **source:** chapter1-print-standalone.html §1.5 · Example 1.35 + Solution（$\lim_{x\to0}x\cos\frac1x=0$；$|\cos(1/x)|\le1$ → $-|x|\le x\cos\frac1x\le|x|$）
- **learning_goal:** 把夾擠再用一次，但抓住關鍵差異——當前面的因式可能為負時，包絡要用 $\pm|x|$（而非 $\pm x^2$）：同手法、不同界。
- **kind:** `example`
- **narration:**
  > Let us run the squeeze once more, on $\lim_{x \to 0} x \cos\frac1x$, because it hides one subtlety worth seeing. Cosine, like sine, stays between minus one and one. But here is the twist: last time the bound was multiplied by $x^2$, which is never negative, so the inequality kept its direction. This time the multiplier is plain $x$, which can be negative — and multiplying an inequality by a negative number flips it. The clean way around that is to bound the size instead: since $|\cos\frac1x| \le 1$, we have $|x \cos\frac1x| \le |x|$, that is, $-|x| \le x \cos\frac1x \le |x|$. Both $\pm|x|$ go to zero, and you can check it for yourself — it runs exactly the same way, squeezing $x \cos\frac1x$ down to zero. Same method as before; only the envelope changed — reach for $|x|$ whenever the factor out front might be negative.
- **visual_need:** 與 u14 並列的「同手法、不同界」：$|\cos\frac1x|\le1$ → $-|x|\le x\cos\frac1x\le|x|$；強調包絡由 $\pm x^2$（u14）換成 $\pm|x|$（因 $x$ 可負、不能直接乘 $x$）；$\lim(\pm|x|)=0$ → 夾擠 $\to0$。
- **animation_cue:** —（靜態即可；§5 純符號，教學點是「界的選擇」而非圖。可選對比：$\pm|x|$ 的 V 形包絡 vs u14 的 $\pm x^2$ 拋物線包絡並置，凸顯「同手法、不同界」——惟講義未繪此圖，預設不加、認可時可定。）
- **備註（§2／§4 repeat-pattern／使用者 2026-06-14 認可拆分）：** Example 1.35 原折疊於 u14 末句；**使用者 2026-06-14 認可拆回獨立單元**，演 $|x|$ 變體、強化「同手法、不同界」的關鍵差異（為何用 $|x|$ 不用 $x$：$x$ 可負、乘負數會翻轉不等式）。§4 repeat-pattern：不重述夾擠定理 setup（u13），一句「once more」承接、直接進新差異點。純符號、不配圖（§5；與 u14 共用 anchor 概念，本身不新增視覺）。末句採使用者認可的口語收尾「you can check it for yourself — it runs exactly the same way」。

### 16. strategy_computing_limits
- **source:** chapter1-print-standalone.html §1.5 · Strategy 1.2（Computing a limit：① 直接代入 ② 不定式則化簡 ③ piecewise 則單側 ④ 夾擠 ⑤ 無界則 $\pm\infty$、$x=a$ 為鉛直漸近線）
- **learning_goal:** 擁有一套「遇到任何極限該怎麼下手」的決策流程——依序試：直接代入 → 化簡 → 單側 → 夾擠 → 無界判 $\pm\infty$／漸近線。
- **kind:** `procedure`
- **narration:**
  > We now have enough tools to lay out a game plan for almost any limit you will meet. First, always try direct substitution — for a polynomial, or a rational function with a nonzero denominator, you are finished on the spot. If substitution gives an indeterminate form like zero over zero, simplify before you judge: factor and cancel, rationalise a root, or combine fractions until the troublesome factor disappears. If the function is piecewise, take the limit from each side and check that the two agree. If it is trapped between two functions that share a limit, reach for the squeeze theorem. And if the values simply grow without bound, the limit is plus or minus infinity, and the line $x = a$ is a vertical asymptote. Run down that list in order, and most limits will tell you which tool they need.
- **visual_need:** 編號決策清單（五步，祈使句）：① try direct substitution；② indeterminate → simplify（factor / rationalise / combine）；③ piecewise → one-sided limits, check agreement；④ trapped → squeeze theorem；⑤ unbounded → $\pm\infty$, vertical asymptote $x=a$。
- **animation_cue:** —（靜態編號清單即可；逐步揭示由 `procedure_steps` 模板承載。）
- **備註（§3）：** Strategy 1.2 為判斷型 strategy（含條件分支），依 §3 **MUST NOT 因分支拆成多單元**——讓 narration 承載條件邏輯，合一 `procedure` 單元。第⑤步（無界 → $\pm\infty$／漸近線）忠實保留，銜接 §1.4，**不報節號**（§4）。

### 17. forcing_existence
- **source:** chapter1-print-standalone.html §1.5 · Example 1.36 + Solution（找常數 $a=\tfrac72$ 使 $\lim_{x\to-2}\frac{x^2+ax+3}{x^2+x-2}$ 存在，再求 $=\tfrac16$）
- **learning_goal:** 一個綜合題——用「極限必須存在」這個要求反推未知常數（分母趨零處分子也須趨零），再用本節技巧把極限算出來。
- **kind:** `example`
- **narration:**
  > Let us finish with a problem that turns the whole section on its head. We want the limit $\lim_{x \to -2} \frac{x^2 + a x + 3}{x^2 + x - 2}$ to exist, and we get to choose the constant $a$ to make that happen. The denominator factors as $(x + 2)(x - 1)$, which goes to zero at $x = -2$. If the numerator went to anything other than zero there, the fraction would blow up and the limit would fail — so the numerator is forced to vanish at $x = -2$ as well. Setting it to zero, $4 - 2a + 3 = 0$, pins down $a = \tfrac{7}{2}$. With that value the numerator factors as $(x + 2)(x + \tfrac{3}{2})$, the common $x + 2$ cancels, and substituting $x = -2$ into what is left gives $\frac{-\frac{1}{2}}{-3}$, or one sixth. Look at the shape of the reasoning: the bare demand that the limit exist fixed the constant, and then the routine techniques of this section finished the job.
- **visual_need:** 目標「$\lim_{x\to-2}\dfrac{x^2+ax+3}{x^2+x-2}$ exists」；分母 $(x+2)(x-1)\to0$；推理「分子也須 $\to0$」→ $4-2a+3=0$ → $a=\tfrac72$；代回因式 $(x+2)(x+\tfrac32)$ 約去 $x+2$ → $\dfrac{x+\frac32}{x-1}$ → 代入 $\dfrac{-\frac12}{-3}=\tfrac16$。
- **animation_cue:** —（靜態即可；推理鏈本身就是 beat，§5 純符號不配圖。`derivation` 模板可承載。）
- **備註（§2 代表式涵蓋／§5）：** Example 1.36（expansion）帶來新模式「用『極限存在』反推常數」，為全節綜合收束（先存在性定 $a$、再用本節技巧算），獨立成單元。純符號、不配圖（§5）。

### 18. recap
- **source:** §1.5 整節（recap 為增補單元）
- **learning_goal:** 四句帶走整個工具箱：極限律＋直接代入、$\tfrac00$ 則化簡、piecewise 則單側、被夾則夾擠。
- **kind:** `recap`
- **narration:**
  > Here is the whole tool-kit in one breath. First, when the limits exist they pass through sums, products, quotients, and powers — and for polynomials and honest rational functions that just means you substitute the number. Second, when substitution gives zero over zero, do not panic: factor, rationalise, or combine fractions until the troublesome factor cancels, then substitute. Third, for a function built in pieces, take the limit from each side and check they agree — when they disagree, as they do across a jump, the limit does not exist. And fourth, when a function is pinned between two others that share a limit, the squeeze theorem hands you that limit for free. Reach for them roughly in that order, and very few limits will hold out.
- **visual_need:** 四張 takeaway 卡：① 極限律 → 多項式／有理函數直接代入；② $\tfrac00$ → 化簡（factor／rationalise／combine）再代入；③ piecewise → 兩側單側，相異則 DNE；④ 被夾且兩界同極限 → squeeze。
- **animation_cue:** —（用 gen-2 既有 `recap_cards` 模板）
- **備註（§3 深度分層）：** recap 與 u16 strategy 刻意分層——strategy 是**操作流程**（how／when：依序試哪招），recap 是**概念帶走**（what：四個大觀念）；recap 給一行提醒、不重演 worked example（§3「總結不重新推導」）。兩者不同深度，非同深度炒冷飯。

### 19. outro
- **source:** —（品牌收尾）
- **learning_goal:** —
- **kind:** `outro`
- **narration:** —（outro 無旁白）
- **visual_need:** 暗轉亮橋接 → 最終 logo 字卡（`meta.section` 1.5 + `meta.title` 預設即可，無 end_slate 覆寫）。
- **animation_cue:** —（用 gen-2 既有 outro 模板）

---

## 內容層檢核（§7）自查記錄

- **環境覆蓋（grep 核實 §1.5）：2 定理、1 命題、11 例題、1 strategy、3 圖。**
  - Theorem 1.2（u3，極限律）、Theorem 1.3（u13，squeeze）——**全覆蓋**。
  - Proposition 1.6（u5，direct substitution）——**覆蓋**。
  - Example 1.26（u4）、1.27（u6）、1.28（u7）、1.29（u8）、1.30（u9）、1.31（u10）、1.32（u11）、1.33（u12）、1.34（u14）、1.35（u15）、1.36（u17）——**每個不同模式皆有代表單元**（§2 代表式涵蓋）：1.26＝抽象套律；1.27＝直接代入；1.28＝$\tfrac00$ 不定（概念反例）；1.29＝factor & cancel；1.30＝rationalise；1.31＝combine fractions；1.32＝piecewise 兩側一致；1.33＝piecewise 兩側相異 DNE；1.34＝squeeze in-action（$x^2\sin$）；1.35＝squeeze 第二例（$x\cos$、$|x|$ 變體）；1.36＝存在性反推常數（綜合）。
  - **Example 1.35（$x\cos\frac1x$）：使用者 2026-06-14 認可拆為獨立單元 u15**（原折疊於 u14 末句）——同型 squeeze（僅 $|x|$ 取代 $x^2$、因 $x$ 可負），現完整演示「同手法、不同界」的差異點，repeat-pattern 不重述夾擠定理 setup。
  - Strategy 1.2（u16，判斷型不拆分）——**覆蓋**。
  - 圖 1.18（u12 floor）、1.19（u13 squeeze anchor）、1.20（u14 x²sin in-action）——**全數有對應視覺單元**。
- **環境間 prose 歸類（無 silently drop）：** opening「tables/graphs to guess → algebraic properties」（promote → u2 motivation）；「justified rigorously … next section」＋「proved … next section」（u2 takeaway fold，改白話不報節號）；「Verbally: …」（u3 body fold）；「A first consequence … easiest way possible」（u5 lead-in）＋「direct substitution … fastest route」（u5 takeaway）；「When direct substitution produces an indeterminate form … simplify then take the limit」（u7 lead-in）；「Some limits … splitting into cases」（u11 lead-in）；「The limit laws require both limits exist … trap between two simpler functions」（u13 lead-in）。
- **forward-pointing prose：** 兩處「once we have the precise definition / proved in the next section」皆 fold 進 u2 takeaway、改白話「that comes a little later」、**不報節號**（§4）——不獨立 `forward_ref`（屬同一動機句，非後章系統概念的預告）。
- **§1.4 callback：** u11／u12（單側極限）、u16 第⑤步（$\pm\infty$／鉛直漸近線）自足回扣 §1.4、**不報節號**——每片自足（觀眾未必看過 §1.4）。
- **symbol-heavy 判定（§5，~75% 符號）：套條件化例外。** anchor＝squeeze 幾何（u13）＋其 in-action $x^2\sin(1/x)$（u14）；唯一對比視覺＝floor 跳斷（u12，破壞「兩側一致」假設→DNE）。**代數例題（u4/u6/u8/u9/u10/u17）一律不配圖**——極限律、直接代入、三招化簡、存在性反推皆純符號，符號本身就是 beat（§5「不為每個代數例子都加圖」）。**u15（squeeze 第二例）亦純符號不配圖**——其教學點是「界的選擇（$|x|$ vs $x^2$）」、講義未繪此圖，與 u14 共用 anchor 概念、本身不新增視覺。u2/u7 為動機／概念性輕視覺（轉向示意、$\tfrac00$ 分岔），非幾何圖。
- **動畫 cue：** u2（估計→計算轉向，輕）、u7（$\tfrac00$ 四分岔）、u12（floor 兩側逼近、夾出跳階縫隙）、u13（squeeze 鉗合 anchor）、u14（包絡捏到原點 in-action）——聚焦教學意圖、自然語言；本輪不接入（比照 §1.1／§1.2，第二輪生成）。
- **repeat-pattern：** u6（直接代入不重述 u5 setup）；u9／u10（化簡不重述 u8 的「$\tfrac00$→化簡」setup，只進新招）；u15（squeeze 第二例不重述夾擠定理 setup u13、一句「once more」承接，只演 $|x|$ 變體）。
- **register／禁則自查：** 全程 we／let us／祈使句；無 “see / as shown / in the diagram”；無節號／圖號／式號／`\cref` 目標；每段 hook→body→takeaway；數學多直讀 LaTeX（下標、分數、根號、$\pm\infty$、$\tfrac00$ 皆可讀），$\mathbb{R}$ 類一律白話（“all real numbers”、“every real value”）。
- **單元數：** **19（17 教學 + intro/outro）**——使用者 2026-06-14 認可把 Ex 1.35 拆回獨立 squeeze 第二例（u15，演 $|x|$ 變體、強化「同手法、不同界」），由原 18 升至 19，更貼近 REBUILD_STATUS 估計 20–24。命題／prose fold 仍照舊（非壓縮預算）。

### 稽核紀錄（2026-06-14，認可前回歸審核）

撰稿後跑一輪六-lens 對抗式稽核（faithfulness／decomposition／register／no-repeat／math-accuracy／completeness，Workflow `wf_546d3acb-9b5`，11 agents）＋逐 finding 獨立對抗式驗證（試 refute、過濾過度 triage／幻覺，比照 `review_pack.py` 紀律）：

- **math-accuracy：0 錯**——11 例題（1.26–1.36）＋折疊的 1.35 ＋ Theorem 1.2／1.3、Prop 1.6、Strategy 1.2 全部獨立重算，與講義及本稿 narration／visual_need 逐項一致（$-4$／$1$／$\tfrac12$／$\tfrac16$／$-\tfrac{32}{9}$／$a=\tfrac72\to\tfrac16$／DNE／squeeze $\to0$；含 $4t^2-1=(2t-1)(2t+1)$、$(x+2)(x+\tfrac32)$ 因式驗證）。
- **0 blocking、0 L1、0 幻覺。** 五條 raise 全收斂為 advisory，其中三條獨立驗證後 **refute／reject**：
  - **faithfulness（reject）：** u3 learning_goal 用「整數次方」概括冪次律（源頭 $n$ 為正整數）——但這是內容層中文 meta 欄、非觀眾可見；觀眾實際聽到的 narration「positive integer power」與螢幕 visual_need「$n$ 為正整數」皆精確，且源頭自己的「Verbally:」白話 gloss（L1369）同樣用寬鬆的 “integer power”。無數學加減到達觀眾，非缺陷。
  - **decomposition（refuted）：** 質疑「proved … in the next section」兩句該獨立成 forward_ref 單元——但 §3 forward-pointing 規則的範圍是「引入**後章才系統處理的概念**」；這兩句是對**本節自己**極限律的「證明留待後面」之 justification caveat，不引入也不教 ε-δ，落在規則範圍外，「永遠獨立成單元」不觸發。fold 進 u2 動機 takeaway、改白話「that comes a little later」、不報節號（§4），正確。
  - **no_repeat（reject）：** 質疑 u17 recap 與 u15 strategy 重疊——但兩者深度確實不同：u15 是操作流程（五步決策、含第⑤步 $\pm\infty$／漸近線、強制排序「Run down that list in order」），u17 是概念帶走（四個大觀念、含「極限律＋直接代入」「相異則 DNE」之收束、hedge 為「roughly in that order」）；化簡技巧清單重疊是**忠實度要求**（同 Strategy 1.2 step 2 源），非炒冷飯。§3 明文允許 how／what 分層、§7 強制 recap 單元。
- **2 條 confirmed advisory（author's-call 取捨，已交使用者裁決）：**
  - **u14 register（confirmed_real，softening 可選）：** 末句「the algebra is in the handout for you to confirm」是 §2 折疊 1.35 的 sanctioned「指回講義」idiom、未犯 §4 禁則。**使用者 2026-06-14 裁決：採口語化**——因 1.35 已拆為獨立單元 u15，此折疊句移除，改於 u15 末句採口語收尾「you can check it for yourself — it runs exactly the same way」。
  - **completeness（confirmed_real，escalate）：** 單元數 18 低於估計 20–24，為合理 fold 結果（§3「單元數不是預算」）、非缺陷。**使用者 2026-06-14 裁決：拆回 19 單元**——Ex 1.35 升格獨立 u15 squeeze 第二例（演 $|x|$ 變體、強化「同手法、不同界」）。
- **採納行動：2（依使用者 2026-06-14 認可裁決）。** ①Ex 1.35 拆為獨立 u15（19 單元）；②u15 末句採口語收尾。math／faithfulness／decomposition／no_repeat 皆無 blocking、無其他改動。
- **回歸審核（拆分後）：** u14 收於 $x^2\sin$ 包絡結論（移除折疊句）、u15 以 repeat-pattern「once more」承接、只演 $|x|$ 變體的差異點（為何 $|x|$ 不用 $x$：$x$ 可負、乘負數翻轉不等式）。**忠實度**：Ex 1.35 仍全覆蓋、math 不變（$x\cos\frac1x\to0$ 經 $-|x|\le x\cos\frac1x\le|x|$ 夾擠）；**no-repeat**：u15 只演與 u14 的差異（界的選擇），未重述夾擠 setup，深度有別、非炒冷飯；**register/§4**：u15 全程 we／let us、無禁則詞、無節號。拆分未引入新問題。

---

## 待辦／工程現況

1. ~~**narration 認可**（使用者）~~ ——✅ **使用者 2026-06-14 認可**（採 19 單元＋u15 口語收尾），可進工程稿。
2. ✅ **工程稿已完成：** `storyboards/ch01_limit_laws.yml`（19 場景）依認可旁白模板化；lint clean、sizecheck consistent；19 個 per-scene 480p mock 皆已產出並抽幀驗收。當前頂層 `output/ch01_limit_laws.mp4` 只有約 51 秒，是合併殘件，不可當整節預覽；需在無平行 Manim/TeX 快取競爭的乾淨窗口重跑 full compose。
3. **MiMo 旁白路線尚未開始本節 Step 1：** 下一步是寫 `ch01_limit_laws.spoken.yml`（口語 single-source、`{show}` 對齊正典）→ `derive_spoken --check` → Mode B → 收斂 → 報用量徵同意後 MiMo TTS。
4. **動畫**（第二輪）：u2／u7／u12／u13／u14 cue → 生成 manim → 認可 → `# HOOK` 接入。本版 storyboard 以靜態模板頂著，floor／squeeze／$x^2\sin(1/x)$ 已由 `graph_focus`/`value_table`/`derivation` 承載第一版視覺。
