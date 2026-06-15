# Section 1.4 One-Sided and Infinite Limits — 內容稿（正式版）

> **性質：正式產線內容稿／no-audio preview 已先行**。依方法論（[`../CONTENT_METHODOLOGY.md`](../CONTENT_METHODOLOGY.md)）從 HTML 講義權威檔逐節拆解、撰寫；content audit clean，storyboard 與 16 段 480p mock preview 已依「先影片後旁白」先行完成。**narration 仍待使用者認可**；正式 MiMo spoken／TTS 尚未開始。
> **來源（權威）：** [`../../experiments/handout_kit/chapter1-print-standalone.html`](../../experiments/handout_kit/chapter1-print-standalone.html) §1.4（`sec-no` 1.4，One-Sided and Infinite Limits）。環境／圖編號已核實：Def 1.10/1.11/1.12、Prop 1.5、Example 1.19–1.25、Figure 1.13–1.17。
> **格式：** 純內容層，每單元 `id / source / learning_goal / kind / narration / visual_need / animation_cue`；**不含** template / `{show}` / accent / 視覺 payload（第二階段才填）。`narration` 為英文（旁白語言）；`visual_need` / `animation_cue` 為中文（內容溝通用）。客製動畫由 Claude 依 `animation_cue` 生成，認可後接入工程稿 `# HOOK`。
> **複雜度（盤點表）：** 中、符號 ~50% → 全視覺處理，**不**套 §5 symbol-heavy 例外（本節幾何份量重：跳斷、漸近線、四型無限圖）。

---

## Deck meta（intro / outro 用）

```
chapter:       Chapter 1
chapter_title: Inverse Functions and Limits
section:       1.4
title:         One-Sided and Infinite Limits
tagline:       What if the two sides disagree, or the values blow up?
sections:      [1.1 Inverse Functions, 1.2 Inverse Trigonometric Functions,
                1.3 The Limit of a Function, 1.4 One-Sided and Infinite Limits,
                1.5 Limit Laws and Computational Techniques,
                1.6 The Precise Definition of a Limit]
```

---

## 教學單元

### 1. intro
- **source:** §1.4 整節 + 章定位（standalone `<title>`：Chapter 1 — Inverse Functions and Limits）
- **learning_goal:** —（純品牌開場）
- **kind:** `intro`
- **narration:** —（intro 無旁白）
- **visual_need:** Section Gate：章地圖聚焦 §1.4 → 標題 “One-Sided and Infinite Limits” + tagline “What if the two sides disagree, or the values blow up?”
- **animation_cue:** —（用 gen-2 既有 intro 模板）

### 2. two_ways_limits_break
- **source:** §1.4 · opening prose（“Near a point $a$, a function can behave differently depending on which side… and in some cases the values… do not approach any finite number at all.”）+ “One-sided limits” subsec lead-in
- **learning_goal:** 看出 §1.3 的「極限＝單一有限數」會以兩種方式破裂——左右兩側不一致、以及值無界增長——並知道本節先談前者。
- **kind:** `motivation`
- **narration:**
  > So far, a limit has been a single number that a function settles toward as $x$ approaches a point. Now we meet two ways that clean picture can break down. First, a function can behave differently depending on which side we approach from — sliding in from the left it may head one way, and from the right another. Second, the values might not approach any finite number at all; they can climb without bound. One-sided behavior and runaway values — those are the two new ideas of this section, and we take them in that order.
- **visual_need:** 一句話的雙主題路線圖：左/右兩側方向不同的小示意 ＋「值衝出畫面」的小示意，點明本節兩條主線。
- **animation_cue:** —（靜態即可；roadmap 性質，動態重點留給後續具體單元）

### 3. one_sided_definition
- **source:** chapter1-print-standalone.html §1.4 · Definition 1.10（left-hand / right-hand limit）+ Figure 1.13（data-fig: one-sided-limits）
- **learning_goal:** 認得單邊極限的記號與意義：$a^-$＝從小於 $a$ 那側逼近，$a^+$＝從大於 $a$ 那側逼近；兩側可落在不同高度。
- **kind:** `definition`
- **narration:**
  > When the two sides disagree, we need language for each side on its own. The left-hand limit, written $\lim_{x \to a^{-}} f(x) = L$, describes what happens as $x$ approaches $a$ through values *less* than $a$ — the approach from the left. The right-hand limit, $\lim_{x \to a^{+}} f(x) = L$, is the mirror image: $x$ approaches $a$ through values *greater* than $a$, coming in from the right. The little minus and plus riding on $a$ are the whole notation — they record which side of $a$ you are arriving from. And on a graph that jumps, the left approach can settle at one height while the right approach settles at another.
- **visual_need:** 一條在 $a$ 處有跳斷的函數圖；左側分支逼近 $a$ 落在高度 $L^-$（空心點）、右側分支落在不同高度 $L^+$（空心點）；標出 $\lim_{x\to a^-}$、$\lim_{x\to a^+}$ 記號。（重繪講義 Figure 1.13 的數學內容。）
- **animation_cue:** 一個點沿左側分支由遠而近滑向 $a$、停在 $L^-$（空心圈標出），再一個點沿右側分支滑向 $a$、停在不同高度 $L^+$（空心圈）；兩高度以淡色水平虛線延伸到 $y$ 軸標出 $L^-\ne L^+$，凸顯「同一個 $a$、兩側落點不同」。

### 4. two_sided_criterion
- **source:** chapter1-print-standalone.html §1.4 · Proposition 1.5（env-name: Criterion for a two-sided limit）+ 前後 prose（“two one-sided limits together determine…”／“If the two one-sided limits differ, then the two-sided limit does not exist.”）
- **learning_goal:** 掌握判準：雙邊極限存在且等於 $L$ ⟺ 兩個單邊極限都等於 $L$；兩側一不合，雙邊極限即不存在。
- **kind:** `proposition`
- **narration:**
  > How do the two one-sided limits relate to the ordinary, two-sided limit from before? Exactly as you would hope: the two-sided limit equals $L$ if and only if *both* one-sided limits equal $L$. For the full limit to exist, the function has to approach the same value from both directions. So the moment the left and right limits disagree, the two-sided limit simply does not exist — there is no single number the function is heading toward. This is how one-sided limits earn their keep: they diagnose whether the two-sided limit is there at all.
- **visual_need:** 判準式卡：$\lim_{x\to a} f = L \iff \lim_{x\to a^-} f = L \text{ and } \lim_{x\to a^+} f = L$；旁註一行「differ $\Rightarrow$ two-sided DNE」。
- **animation_cue:** —（靜態即可；可選回放 u3 跳斷圖一拍、標 $L^-\ne L^+ \Rightarrow$ 雙邊 DNE，作為判準的視覺佐證——非必要）

### 5. criterion_both_directions
- **source:** chapter1-print-standalone.html §1.4 · Example 1.19 + Solution（`prompt-list`／`sol-list` 兩小題）
- **learning_goal:** 雙向操作判準：雙邊極限 $\Rightarrow$ 每個單邊（資訊由整體流向兩側）；單一單邊 $\not\Rightarrow$ 雙邊（資訊不足）。
- **kind:** `example`
- **narration:**
  > Let us put the criterion to work in both directions. Suppose the two-sided limit of $f$ at $-2$ equals $16$. What must the left-hand limit be? Since the full limit exists, both sides are forced to match it, so the left-hand limit is $16$ as well — information flows from the two-sided limit outward to each side. Now reverse it: suppose all we are told is that the left-hand limit at $-2$ is $16$. Can we name the two-sided limit? No — not enough information. The right side might agree, making the two-sided limit $16$, or it might do something else entirely, in which case the two-sided limit fails to exist. One side alone never settles the question; only both sides together do.
- **visual_need:** 兩小題並排：(1) given $\lim_{x\to -2} f = 16 \Rightarrow \lim_{x\to -2^-} f = 16$（箭頭：整體 → 單邊）；(2) given $\lim_{x\to -2^-} f = 16 \Rightarrow$ 雙邊「not enough information」（兩種結局：右側合則 $=16$、右側不合則 DNE）。
- **animation_cue:** —（靜態逐步揭示即可；此例純邏輯、無函數圖）

### 6. jump_example
- **source:** chapter1-print-standalone.html §1.4 · Example 1.20 + Solution + Figure 1.14（data-fig: piecewise-jump）
- **learning_goal:** 對具體分段函數算出左右極限（$3$ 與 $2$）、由判準斷定雙邊 DNE，並把它扣回跳斷圖。
- **kind:** `example`
- **narration:**
  > Here is a function built from two different formulas, with the split exactly at $x = 2$: it is $x + 1$ when $x$ is below $2$, and $4 - x$ from $2$ onward. Approaching from the left, we are on the first piece, $x + 1$, which heads toward $2 + 1$, that is $3$. Approaching from the right, we are on the second piece, $4 - x$, heading toward $4 - 2$, that is $2$. The left limit is $3$, the right limit is $2$ — they disagree, so by our criterion the two-sided limit at $2$ does not exist. The graph shows the break plainly: the curve jumps at $x = 2$, the left piece ending at height $3$ and the right piece starting at height $2$.
- **visual_need:** 分段函數圖 $f(x)=x+1\,(x<2)$、$4-x\,(x\ge2)$；$x=2$ 處跳斷——左支終點 $(2,3)$ 空心圈、右支起點 $(2,2)$ 實心點；標 $\lim_{x\to2^-}=3$、$\lim_{x\to2^+}=2$。（重繪講義 Figure 1.14。）
- **animation_cue:** 兩條直線分支依序畫出；一個點沿左支滑向 $x=2$ 停在 $(2,3)$（空心圈閃出），再一個點沿右支滑向 $x=2$ 停在 $(2,2)$（實心點閃出）；兩高度差以短雙箭頭標出「跳了一格」，凸顯左右落點不同 $\Rightarrow$ 雙邊不存在。
- **備註（§4 repeat-pattern）：** 同樣套 u4 判準，但屬不同教學模式（u5 純邏輯推理、本單元具體分段函數計算＋圖），依代表式涵蓋（§2）兩者皆保留。

### 7. values_blow_up
- **source:** chapter1-print-standalone.html §1.4 · “Infinite limits” subsec lead-in prose（“values… do not approach any finite number… grow arbitrarily large”）+ Example 1.21 + Solution（$f(x)=1/x^2$）
- **learning_goal:** 看見 $1/x^2$ 在 $x\to0$ 無界增長：嚴格意義下極限不存在，但「有秩序地衝高」這個失敗模式值得專屬記號。
- **kind:** `example`
- **narration:**
  > Now the second kind of breakdown: values that refuse to settle anywhere finite. Take $f(x) = \frac{1}{x^{2}}$ and push $x$ toward $0$. Squaring makes the denominator a tiny positive number, and one over a tiny positive number is huge. Watch the scale: at $x = 0.1$ the value is $100$; at $x = 0.01$ it has already jumped to ten thousand. The closer $x$ gets to $0$, the larger $\frac{1}{x^{2}}$ becomes, with no ceiling at all. There is no finite number $L$ that these values approach, so in the strict sense the limit does not exist — but notice *how* it fails. The function is not wandering aimlessly; it is climbing without bound, and that orderly blow-up deserves a notation of its own.
- **visual_need:** $y=1/x^2$ 圖（兩支皆向上衝、夾著 $y$ 軸）；旁附小數值表 $\dfrac{1}{(0.1)^2}=100$、$\dfrac{1}{(0.01)^2}=10{,}000$ 凸顯增速。
- **animation_cue:** 曲線從外側往 $x=0$ 描繪、兩支沿 $y$ 軸節節攀高、衝出畫面頂端；同步數值表逐列亮出（$100 \to 10{,}000$），數字越跳越大，演出「逼近 $0$、值無上限」。
- **備註（§3 prose）：** 「Infinite limits」subsec 的 incorporative lead-in 併入本單元開場（§3）。

### 8. sign_decides_infinity
- **source:** chapter1-print-standalone.html §1.4 · Example 1.22 + Solution（$1/x$ 左右 vs $1/x^2$）
- **learning_goal:** 看出「衝向無限」必須兩側同向：$1/x$ 左 $-\infty$、右 $+\infty$ 兩側反向 $\Rightarrow$ 不寫 $=\infty$；$1/x^2$ 兩側同向上 $\Rightarrow$ 可寫 $=\infty$。
- **kind:** `example`
- **narration:**
  > But that orderly blow-up needs the values all running the *same* way, and $\frac{1}{x}$ shows why. Approach $0$ from the left, where $x$ is negative: $\frac{1}{x}$ is negative and grows huge in magnitude, diving toward minus infinity. Approach from the right, where $x$ is positive: $\frac{1}{x}$ shoots up toward positive infinity. The two sides race off in *opposite* directions, so there is no single tendency to record — and here we do *not* write that the limit is infinity. Contrast $\frac{1}{x^{2}}$, where both sides climb the same way, upward: there we are entitled to write that the limit equals infinity. So it comes down to agreement in direction — a same-signed runaway on both sides earns the infinity symbol; a split between the sides does not.
- **visual_need:** $y=1/x$ 圖：左支沉向 $-\infty$、右支衝向 $+\infty$（兩側反向）；旁並列 $1/x^2$ 縮圖（兩側同向上）。標 $\lim_{x\to0^-}\tfrac1x=-\infty$、$\lim_{x\to0^+}\tfrac1x=+\infty$、雙邊 DNE；$1/x^2$ 標 $=\infty$。
- **animation_cue:** —（靜態並排對比即可；兩圖反向 vs 同向的對照本身即教學點，過度動畫反稀釋）
- **備註（§4 repeat-pattern／§2）：** 緊接 u7 同以 $1/x^n$ 談無限增長，但教學點不同（u7＝無界增長本身、本單元＝方向是否一致決定能否寫 $\infty$）；以一句轉場「that orderly blow-up needs the values all running the same way」直接進新內容、不重述 setup（§4）。$\infty$ 記號此處先口語使用，下一單元 u9 才形式定義（忠於書序：先建直覺再形式化）。

### 9. infinite_limit_definition
- **source:** chapter1-print-standalone.html §1.4 · Definition 1.11（infinite limit $=\pm\infty$）+ 前一段 ∞-notation prose（“The symbol $\infty$ does not represent a real number…”）
- **learning_goal:** 形式化無限極限記號 $\lim_{x\to a} f=\infty$／$=-\infty$，並牢記 $\infty$ 不是數、等式是「無界增長」的速記而非賦值。
- **kind:** `definition`
- **narration:**
  > Let us make the notation official. When the values of $f$ can be made arbitrarily large by taking $x$ sufficiently close to $a$, we write $\lim_{x \to a} f(x) = \infty$, and we call this an infinite limit. If instead the values grow arbitrarily large in the negative direction, we write $\lim_{x \to a} f(x) = -\infty$. One caution that genuinely matters: the symbol infinity is not a number, and this equation is not claiming the limit *is* some value. It is shorthand — a compact way to record that the function's values grow without bound, in one definite direction.
- **visual_need:** 定義卡：$\lim_{x\to a} f(x) = \infty$（值可任意大）／$\lim_{x\to a} f(x) = -\infty$（值任意大負）；醒目附註「$\infty$ is not a number — it records unbounded growth」。
- **animation_cue:** —（靜態即可）

### 10. four_one_sided_cases
- **source:** chapter1-print-standalone.html §1.4 · one-sided infinite prose（“One-sided versions… defined analogously”）+ Figure 1.15（data-fig: one-sided-infinite，four typical cases）
- **learning_goal:** 認得單邊無限極限的四種基本型（左/右 × $+\infty$/$-\infty$），每一型都是曲線沿 $x=a$ 衝出畫面上下緣。
- **kind:** `visual`
- **narration:**
  > Everything we just did has one-sided versions too. The values can run off to infinity as $x$ approaches $a$ from the left alone, or from the right alone, and in either the positive or the negative direction. That gives four basic shapes — left-side up, left-side down, right-side up, right-side down — each one a curve hugging the vertical line at $a$ and sprinting off the top or the bottom of the frame. These four little pictures are the whole vocabulary of how a function can explode on just one side of a point.
- **visual_need:** 四格小圖（panel）：每格一條曲線貼著垂直線 $x=a$、分別從左/右側衝向 $+\infty$/$-\infty$；標題對應四式 $\lim_{x\to a^\mp} f = \pm\infty$。（重繪講義 Figure 1.15。）
- **animation_cue:** 四格依序亮出，每格曲線沿 $x=a$ 那條虛線快速描繪、衝出該格上緣或下緣，配合該格的單邊記號逐一點亮——把「四型」當成一組詞彙一次建立。

### 11. vertical_asymptote_definition
- **source:** chapter1-print-standalone.html §1.4 · “Vertical asymptotes” subsec bridge prose（“Infinite limits are closely related to vertical asymptotes.”）+ Definition 1.12（vertical asymptote）
- **learning_goal:** 掌握垂直漸近線定義：$x=a$ 處至少一個單邊極限為 $\pm\infty$，即稱 $x=a$ 為 $y=f(x)$ 的垂直漸近線——它是無限極限的幾何身影。
- **kind:** `definition`
- **narration:**
  > These infinite limits have a familiar geometric name. When a function blows up near $x = a$ — on either side, toward either infinity — the vertical line $x = a$ is called a vertical asymptote of the curve. The graph runs closer and closer to that line without ever touching it, shooting upward or downward right alongside it. So a vertical asymptote is simply the visual signature of an infinite limit: a wall the curve chases but never reaches.
- **visual_need:** 定義卡：$x=a$ 為垂直漸近線 $\iff$ $\lim_{x\to a^-} f=\pm\infty$ 或 $\lim_{x\to a^+} f=\pm\infty$（至少一個成立）；附一條垂直虛線與貼線衝高的曲線小圖示意。
- **animation_cue:** —（靜態即可；漸近線的「動態貼牆」留給下一單元的具體例子演示）

### 12. finding_an_asymptote
- **source:** chapter1-print-standalone.html §1.4 · Example 1.23 + Solution + Figure 1.16（data-fig: vertical-asymptote）
- **learning_goal:** 完整跑一遍「找垂直漸近線」：定位分母零點為候選 $x=3$，左右側各做符號分析得 $\pm\infty$，據定義斷定 $x=3$ 為漸近線。
- **kind:** `example`
- **narration:**
  > Let us hunt for an asymptote. Consider $y = \frac{2x}{x - 3}$. A vertical asymptote can only happen where the function misbehaves, and for a fraction that means where the denominator hits zero — here, $x = 3$. So $3$ is our one candidate; now we test it from each side. Coming in from the right, $x - 3$ is a small *positive* number while the top stays near $6$, and $6$ divided by something tiny and positive is enormous and positive — the limit is plus infinity. From the left, $x - 3$ is small and *negative*, so the same near-$6$ top over a tiny negative gives minus infinity. Either one-sided infinity is enough on its own, so the line $x = 3$ is a vertical asymptote: the curve rockets up on one side of it and plunges down on the other.
- **visual_need:** $y=\frac{2x}{x-3}$ 圖；$x=3$ 處垂直虛線（漸近線）；右支沿線衝 $+\infty$、左支沿線墜 $-\infty$；標 $\lim_{x\to3^+}=\infty$、$\lim_{x\to3^-}=-\infty$。（重繪講義 Figure 1.16。）
- **animation_cue:** 先畫垂直虛線 $x=3$；曲線兩支分別描繪——右支沿虛線右側往上飆出畫面、左支沿虛線左側往下墜出畫面；逼近時各閃示 $x-3$ 的「小正／小負」標記與對應的 $+\infty$／$-\infty$，演出「分母趨零、值沿牆衝走」。

### 13. zero_denominator_not_enough
- **source:** chapter1-print-standalone.html §1.4 · Example 1.24 + Solution（$g(x)/(x^2-9)$，零分母不保證漸近線）
- **learning_goal:** 破除「分母為零 $\Rightarrow$ 必有垂直漸近線」的誤解：零分母只是「待查候選」，結果取決於分子（$g=1$ 有漸近線；$g=x^2-9$ 則 $f\equiv1$ 無漸近線）。
- **kind:** `counterexample`
- **narration:**
  > But be careful — a zero in the denominator is only a *candidate*, not a verdict. Suppose $f(x) = \frac{g(x)}{x^{2} - 9}$ for some function $g$ we have not pinned down, and ask whether $x = -3$ must be an asymptote. The denominator does vanish at $-3$, so it is certainly worth investigating. But the answer hinges on the top. If $g$ is just $1$, then $f = \frac{1}{x^{2} - 9}$ genuinely blows up near $-3$, and yes, there is an asymptote. But if $g$ is itself $x^{2} - 9$, the whole fraction collapses to $1$ everywhere it is defined — a flat line, no asymptote at all. Same zero denominator, opposite outcomes. So a vanishing denominator marks a spot to *check* with one-sided limits; it is never a guarantee on its own.
- **visual_need:** 對照兩列：候選 $x=-3$（$x^2-9=0$）；分支 A $g=1\Rightarrow f=\frac{1}{x^2-9}$ 在 $-3$ 暴增（有漸近線、✓）；分支 B $g=x^2-9\Rightarrow f\equiv1$ 平直（無漸近線、✗）。凸顯「同分母零點、結果相反」。
- **animation_cue:** —（靜態對照即可；兩分支「同前提、相反結論」的並列本身即教學點）
- **備註（§2／§3）：** Example 1.24 是標準「破除誤解」反例，依方法論定為 `counterexample` 獨立單元；緊接 u12 正例（有漸近線）後，正反相映。

### 14. log_asymptote
- **source:** chapter1-print-standalone.html §1.4 · Example 1.25 + Solution + Figure 1.17（data-fig: ln-asymptote）
- **learning_goal:** 看見漸近線不限於有理函數：$\ln x$ 因定義域只在右側、$\lim_{x\to0^+}\ln x=-\infty$，故 $x=0$ 為其垂直漸近線（單邊即足）。
- **kind:** `example`
- **narration:**
  > Asymptotes are not just a rational-function story. Take the natural logarithm, $\ln x$. It is only defined for positive inputs, so we can only approach $0$ from the right — and as $x$ slides down toward $0$ from above, $\ln x$ falls without bound, off toward minus infinity. That single one-sided infinite limit is all the definition asks for, so $x = 0$ is a vertical asymptote of the logarithm. Here the curve presses against the $y$-axis from the right, sinking lower and lower the closer it gets.
- **visual_need:** $y=\ln x$ 圖（僅 $x>0$）；$x=0$（$y$ 軸）為垂直虛線漸近線；曲線右側貼軸下沉；標 $\lim_{x\to0^+}\ln x=-\infty$。（重繪講義 Figure 1.17。）
- **animation_cue:** —（靜態即可；可選曲線沿 $y$ 軸右側往下描繪、貼線下沉的輕動畫，非必要）
- **備註（§4 repeat-pattern／§2）：** 第二個漸近線例，以「Asymptotes are not just a rational-function story」一句轉場、不重述 setup（§4）；帶來新 flavor（超越函數＋僅單邊可逼近的漸近線），非同型 drill，依代表式涵蓋（§2）保留。

### 15. recap
- **source:** §1.4 整節（recap 為增補單元）
- **learning_goal:** 四句帶走整節：單邊極限記號、雙邊判準、無限極限與 $\infty$ 記號（同向才寫）、垂直漸近線（候選→單邊極限確認）。
- **kind:** `recap`
- **narration:**
  > Four ideas to carry out of this section. First, one-sided limits: the left-hand and right-hand limits describe the approach to $a$ from below and from above, written with a little minus or plus riding on $a$. Second, the criterion that ties them together — the two-sided limit exists exactly when both one-sided limits exist and agree; let them disagree, and the limit is gone. Third, infinite limits: when values grow without bound in a single direction we write the limit as plus or minus infinity, always remembering that infinity is not a number but a description of runaway growth. And fourth, vertical asymptotes: a line $x = a$ that the graph chases toward infinity — found by spotting where a function can blow up, then confirming with one-sided limits.
- **visual_need:** 四張 takeaway 卡：① 單邊極限 $a^-$／$a^+$；② 判準（雙邊 $\iff$ 兩單邊一致；differ $\Rightarrow$ DNE）；③ 無限極限＋$\infty$ 非數（同向才寫 $=\infty$）；④ 垂直漸近線（零分母候選 → 單邊極限確認）。
- **animation_cue:** —（用 gen-2 既有 recap_cards 模板）

### 16. outro
- **source:** —（品牌收尾）
- **learning_goal:** —
- **kind:** `outro`
- **narration:** —（outro 無旁白）
- **visual_need:** 暗轉亮橋接 → 最終 logo 字卡（`meta.section` + `meta.title` 預設即可，無 end_slate 覆寫）。
- **animation_cue:** —（用 gen-2 既有 outro 模板）

---

## 內容層檢核（§7）自查記錄

- **環境覆蓋（MUST）：** Definition 1.10（u3）、Proposition 1.5（u4）、Definition 1.11（u9）、Definition 1.12（u11）——三定義一命題**全覆蓋**。Examples：1.19（u5）、1.20（u6）、1.21（u7）、1.22（u8）、1.23（u12）、1.24（u13）、1.25（u14）——**七例全收**（各帶不同教學模式，見下）。Figures 1.13（u3）、1.14（u6）、1.15（u10）、1.16（u12）、1.17（u14）——**五圖全覆蓋**。本節 HTML **無 `env-exercise`**，無習題洩入。
- **例題代表式涵蓋（§2）判定：** 七例皆屬不同教學模式、無同型 drill 可折疊——1.19 判準純邏輯（資訊不足）、1.20 分段函數計算＋跳斷圖、1.21 無界增長（motivate $\infty$）、1.22 方向決定能否寫 $\infty$、1.23 找漸近線正例、1.24 零分母不保證（反例）、1.25 超越函數＋單邊漸近線。故**全收**，無折疊註記。
- **環境間 prose 歸類（§3，無 silently drop）：** opening 雙主題 prose＋one-sided subsec lead-in（promote → u2 motivation）；“two one-sided limits together determine…”／“If… differ… DNE”（併入 u4）；Infinite-limits subsec lead-in（incorporative → u7 lead-in）；∞-notation prose “The symbol $\infty$…”（併入 u9 lead-in）；one-sided infinite “defined analogously”（併入 u10）；Vertical-asymptotes bridge “Infinite limits are closely related…”（併入 u11 lead-in）。**全部歸類，無漏。**
- **forward-pointing prose：** 本節 HTML 無向後章預告（Example 1.24 的「investigate with one-sided limits」屬本節內方法、非跨章），無 `forward_ref` 單元。
- **symbol-heavy 判定：** 符號 ~50%，且幾何份量重（跳斷圖、$1/x^2$／$1/x$ 暴增、四型無限、兩例漸近線）——**不**套 §5 條件化例外，全視覺處理。視覺／動畫單元：u2/u3/u6/u7/u8/u10/u12/u13/u14。
- **動畫 cue：** u3（左右滑入落不同高度）、u6（分段滑入跳斷）、u7（曲線衝出＋數值表）、u10（四型逐格衝出）、u12（兩支沿漸近線飆走）——聚焦教學意圖、自然語言、未寫 manim。u8/u13 刻意靜態（對照本身即教學點）。
- **§4 禁則自查：** 無念螢幕標題、無逐字念條列、無報節號/圖號/式號、無「see／as shown／in the diagram」（u6 改「The graph shows the break plainly」、u10「these four little pictures」皆為描述非指涉）、無「In this scene…」開場。
- **repeat-pattern（§4）：** u8（接 u7）、u14（接 u12）皆以一句轉場直接進新內容、不重述 setup。
- **id 唯一性：** 16 個 id 全唯一、snake_case、描述教學重點。
- **單元數：** 14 內容單元＋intro／outro＝16；落在盤點表建議的 14–18 區間。

### 稽核紀錄（2026-06-14，認可前對抗式稽核）

撰稿後跑了一輪六-lens 對抗式稽核（faithfulness／decomposition／register／no-repeat／math-accuracy／completeness，Workflow `wnjdeyacd`），每條 raw finding 再經獨立 refute-by-default 驗證過濾過度 triage／幻覺（比照 §1.2、`review_pack.py` 紀律）：

- **六個內容維度全 clean**——raw 1 → confirmed 1，逐 finding 驗證後：
  - **math-accuracy：0 錯**——七例的數值／正負／單邊方向經獨立重算逐項一致：u5 雙邊→單邊（資訊不足）、u6 分段左 $3$／右 $2$→DNE、u7 $1/(0.1)^2=100$／$1/(0.01)^2=10000$、u8 $1/x$ 左 $-\infty$／右 $+\infty$ vs $1/x^2$ 同向、u12 $2x/(x-3)$ 右 $+\infty$／左 $-\infty$、u13 $g=1$ 有／$g=x^2-9$ 無漸近線、u14 $\ln x\to-\infty$。
  - **faithfulness／decomposition／register／no-repeat：無 L1、無幻覺**——14 教學單元全可回溯 §1.4 環境（Def 1.10–1.12、Prop 1.5、Ex 1.19–1.25、Fig 1.13–1.17）、無 silently drop；七例經驗證皆屬不同模式（無可折疊同型 drill）；§4 禁則與 repeat-pattern（u8 接 u7、u14 接 u12）自查經對源核實為真。
- **唯一 confirmed finding（advisory，非內容問題）：** 缺方法論 §6 要求的 `_narration.html` 審核交付物——**已補**（[`ch01_one_sided_infinite_narration.html`](ch01_one_sided_infinite_narration.html)，14 段旁白逐字一致經程式核對、結構驗證通過）。
- **回歸：** 稿本體零內容修改（六維度 clean），故無「修後複驗」需求；補 HTML 後逐單元比對 narration 與 `.md` 14/14 一致。
- **未動（L3 taste／設計取捨，列供認可時參考）：** u2 motivation 6 句、u8 ~7 句（皆在 kind 可接受範圍）；u3/u6/u7/u10/u12 的動畫密度屬第二輪設計取捨，認可旁白後再定。

---

## 待辦／工程現況

1. **preview 可審看**——`storyboards/ch01_one_sided_infinite.yml` 已完成；`output/ch01_one_sided_infinite_preview.mp4` 是 16 段 no-audio 480p full preview（約 10:56），供先看節奏、畫面與數學呈現。
2. **正式輸出尚未定稿**——`output/ch01_one_sided_infinite.mp4` 目前約 54 秒，屬 partial／舊 compose，不可當作本節完成品；目前以 `_preview.mp4` 為準。
3. **旁白待認可**——內容稿與 `_narration.html` 已對齊，但使用者尚未正式核准旁白口味；如有改稿，需同步更新 storyboard cue。
4. **MiMo 流程尚未開始**——下一步是撰寫 `ch01_one_sided_infinite.spoken.yml`、derive spoken markdown、跑 Mode B，再依使用者同意進 TTS。
5. **二輪動畫／hook**——u3/u6/u7/u10/u12 是主要動畫密度決策點；審看 preview 後再決定哪些要升級 hook 或保持 gen-2。
