# Section 1.6 The Precise Definition of a Limit — 內容稿

> **性質：symbol-heavy 壓力測試節**（產線第二節，繼 §1.1 校準樣本之後）。目的是壓測 [`../CONTENT_METHODOLOGY.md`](../CONTENT_METHODOLOGY.md) 的 **§5 symbol-heavy 例外路徑**、theorem/proof 拆單元、repeat-pattern、對齊鏈 narration——對應 [`../REBUILD_STATUS.md`](../REBUILD_STATUS.md) 標記的「§1.6 symbol-heavy 第二校準節」。
> **來源：** [`chapter1-print-standalone.html`](../../experiments/handout_kit/chapter1-print-standalone.html) §1.6（L1655–1884）。**（2026-06-14 漂移修復：原指 `chapters/ch01_foundations.tex` §1.6 L1332–1588，已重指定稿 HTML 權威檔；環境現行編號見各單元 `source:`，新增例題見文末漂移修復筆記。）**
> **格式：** 純內容層，每單元 `id / source / learning_goal / kind / narration / visual_need / animation_cue`；**不含** template / `{show}` / accent / 視覺 payload（第二階段才填）。`narration` 為英文（旁白語言）；`visual_need` / `animation_cue` 為中文（內容溝通用）。動畫一律**客製 manim，由 Claude 依 `animation_cue` 自然語言生成**（認可後接入工程稿 `# HOOK`）——內容稿本身只給自然語言、不寫 code。
> **視覺預算（§5 symbol-heavy 例外）：** 本節教學重量 ~90% 落在符號／邏輯／量詞，故**只配兩個圖形視覺**——unit 7 的 ε-δ 管狀圖（**anchor**）與 unit 3 的動機圖（line + 挖空點）。其餘所有定義／定理／證明／procedure／例題（含定義診斷與 M-δ 無窮極限驗證）／無窮極限定義／forward-ref／recap **皆純符號，不配圖**（符號本身就是 beat；診斷單元用符號 compare、驗證例題用推導鏈呈現）。

---

## Deck meta（intro / outro 用）

```
chapter:       Chapter 1
chapter_title: Inverse Functions and Limits
section:       1.6
title:         The Precise Definition of a Limit
tagline:       How close is close enough?
sections:      [1.1 Inverse Functions, 1.2 Inverse Trigonometric Functions,
                1.3 The Limit of a Function, 1.4 One-Sided and Infinite Limits,
                1.5 Limit Laws and Computational Techniques,
                1.6 The Precise Definition of a Limit]
next:          Up next — Derivatives
```

> **running example（本節貫穿例）：** $f(x)=2x-1$（在 $x=3$ 強制 $f(3)=6$），$a=3$、$L=5$。unit 3→4→5→6→7 全用它當具體載體——把抽象定義扣在同一條線上（symbol-heavy 節給定義一根具體脊梁）。

---

## 教學單元

### 1. intro
- **source:** §1.6 整節 + 章定位
- **learning_goal:** —（純品牌開場）
- **kind:** `intro`
- **narration:** —（intro 無旁白）
- **visual_need:** Section Gate：章地圖聚焦 §1.6 → 標題 “The Precise Definition of a Limit” + tagline “How close is close enough?”
- **animation_cue:** —（用 gen-2 既有 intro 模板）

### 2. why_close_is_not_enough
- **source:** `chapter1-print-standalone.html` §1.6 · opener prose（history／foundations + 「close」須精確化，L1664–1666）
- **learning_goal:** 體會「f(x) 靠近 L」這種口語不夠用，本節要把「靠近」換成可量的距離。
- **kind:** `motivation`
- **narration:**
  > For two centuries calculus solved real problems — orbits, areas, the motion of the planets — while its logical foundations stayed shaky. The arguments leaned on infinitesimals, quantities imagined as vanishingly small but never pinned down, and on vague phrases like "$x$ is close to $a$" and "$f(x)$ is close to $L$." But how close is close? The nineteenth century answered by throwing the word "close" out entirely and replacing it with a measurable distance. That single move is the whole project of this section: make "close" precise enough to compute with.
- **visual_need:** —（純動機；無圖。一句 thesis 「replace ‘close’ with measurable distance」可上字卡，但不畫數學圖。）
- **animation_cue:** —（靜態即可）

### 3. the_broken_function
- **source:** `chapter1-print-standalone.html` §1.6 · motivating function prose（the broken function $f$，L1668–1670）
- **learning_goal:** 看見極限只看「逼近的行為」、不理會 $f$ 在該點的實際值。
- **kind:** `motivation`
- **narration:**
  > Here is a deliberately broken function to sharpen the question. Let $f(x)=2x-1$ everywhere except at $x=3$, where we force the value to be $6$. As $x$ moves close to $3$, the output $2x-1$ moves close to $5$ — so we expect the limit to be $5$, even though the function's actual value there is $6$. The limit watches how $f$ behaves on the approach, not where it lands at the point itself. But "close to $5$" is the very phrase we promised to make precise, so let us ask the sharp question: how close can we force $f(x)$ to be?
- **visual_need:** 動機圖（§5 例外允許的第二個視覺）：畫直線 $y=2x-1$；在 $(3,5)$ 挖空（hollow，極限值、非函數值），在 $(3,6)$ 放實心點（$f(3)=6$ 的實際值）；標 $x=3$。凸顯「實際值 6 ≠ 極限 5」。
- **animation_cue:** —（靜態即可；可讓 $x$ 沿線從兩側滑向 3、輸出滑向 5，但非必要——留待動畫階段定。）

### 4. tolerance_game_point_one
- **source:** `chapter1-print-standalone.html` §1.6 · Example 1.37（tolerance 0.1，L1672–1687）
- **learning_goal:** 把「夠近」當成一個附帶數字的挑戰，用代數算出對應的輸入半徑。
- **kind:** `example`
- **narration:**
  > Let us play it as a game with a number attached. Suppose someone demands that $f(x)$ land within $0.1$ of $5$ — can we deliver? Measure the gap: $|f(x)-5|$ equals $|(2x-1)-5|$, which is $|2x-6|$, which is $2|x-3|$. So the demand $2|x-3|<0.1$ is just $|x-3|<0.05$. Keep $x$ within $0.05$ of $3$, and $f(x)$ is guaranteed within $0.1$ of $5$ — a precise promise, answered with a precise radius.
- **visual_need:** —（純代數例，§5「不為每個代數例題配圖」；推導鏈以符號呈現即可：$|f(x)-5|=2|x-3|<0.1 \Rightarrow |x-3|<0.05$。）
- **animation_cue:** —（靜態即可；對齊鏈逐行揭示）

### 5. every_tolerance_at_once
- **source:** `chapter1-print-standalone.html` §1.6 · generalization prose（0.01 → every $\varepsilon$ → $\delta=\varepsilon/2$，L1689）
- **learning_goal:** 跨過關鍵概念跳躍——不是回答某個容差，而是回答**每一個** $\varepsilon>0$。
- **kind:** `motivation`
- **narration:**
  > One answered demand is not enough, though. Tighten the tolerance to $0.01$ and the very same algebra returns $|x-3|<0.005$; halve the tolerance and the radius halves with it. The pattern is mechanical: for any tolerance $\varepsilon>0$, we get $|f(x)-5|<\varepsilon$ whenever $|x-3|<\tfrac{\varepsilon}{2}$, so the choice $\delta=\tfrac{\varepsilon}{2}$ always works. This is what "arbitrarily close" really means — not close for one lucky tolerance, but answerable for every $\varepsilon>0$. That little phrase "for every $\varepsilon$" is the engine of the definition we are about to write down.
- **visual_need:** —（純符號概念跳躍；無圖。可上 $\varepsilon \to \delta=\tfrac{\varepsilon}{2}$ 的對應字卡。）
- **animation_cue:** —（靜態即可）

### 6. precise_limit_definition
- **source:** `chapter1-print-standalone.html` §1.6 · Definition 1.13（ε-δ limit，L1691–1699）
- **learning_goal:** 認得 ε-δ 定義，並把它讀成「你出 ε、我給 δ」的挑戰—應答結構。
- **kind:** `definition`
- **narration:**
  > Now we can state it cleanly. Let $f$ be defined on an open interval around $a$, except possibly at $a$ itself. We say $\lim_{x\to a}f(x)=L$ if for every $\varepsilon>0$ there exists a $\delta>0$ such that $|f(x)-L|<\varepsilon$ whenever $0<|x-a|<\delta$. Read it as a challenge and a response: you name any tolerance $\varepsilon$, however cruelly small, and I must produce a radius $\delta$ that keeps every nearby $f(x)$ inside it. If I can always answer, the limit is $L$.
- **visual_need:** 定義字卡：$\lim_{x\to a}f(x)=L \iff$ 「$\forall \varepsilon>0\ \exists \delta>0$ s.t. $|f(x)-L|<\varepsilon$ whenever $0<|x-a|<\delta$」。強調量詞 $\forall\varepsilon\,\exists\delta$。
- **animation_cue:** —（靜態即可，定義逐句揭示；幾何在下一單元）

### 7. epsilon_delta_tube
- **source:** `chapter1-print-standalone.html` §1.6 · geometric-reading prose + Figure 1.21（fig:precise-limit，L1701–1707）
- **learning_goal:** 把定義看成一張圖：δ-區間「餵進」ε-帶，且 **δ 隨 ε 而變**。
- **kind:** `visual`（**anchor**——本節唯一核心幾何視覺）
- **narration:**
  > The definition hides a clean picture. Mark the target on the $y$-axis: a horizontal band from $L-\varepsilon$ to $L+\varepsilon$, the strip we want the outputs to land in. Mark the inputs on the $x$-axis: a vertical band from $a-\delta$ to $a+\delta$, with the single point $a$ punched out. The definition says exactly this — as long as $x$ stays in the input band, the graph carries it into the target band. And here is the part to feel in your bones: shrink the target strip toward $L$, and the input interval must shrink too, or the curve escapes the band. The radius $\delta$ is not fixed; it answers to $\varepsilon$.
- **visual_need:** 用本節 running example $f(x)=2x-1$（$a=3$、$L=5$）當具體載體畫定義圖：水平帶 $L-\varepsilon \le y \le L+\varepsilon$（目標帶）、垂直帶 $a-\delta \le x \le a+\delta$（輸入帶），$x=a$ 處挖空；軸上標 $a-\delta,\ a,\ a+\delta$ 與 $L-\varepsilon,\ L,\ L+\varepsilon$。（以具體 line 示範書本散文的一般定義圖——§5「視覺單元 MAY 用具體函數示範一般主張」，增補呈現、不增刪內容。）
- **animation_cue:** |
  客製 manim（**anchor，本節最關鍵動畫**）：先畫水平 ε-帶與垂直 δ-帶、在交會處框出中央矩形；接著**收緊 ε**——ε-帶從上下向 $L$ 收窄，δ-帶隨之向 $a$ 收窄（兩者連動），曲線始終被夾在框內；換兩三個遞減的 ε 重複，凸顯「ε 你定、δ 來應」與「δ 隨 ε 而變」。這支動畫獨力承載整個定義的量詞直覺，是本節視覺的重心。
- **anim 實作（已生成）：** [`../animations/ch01_precise_limit_hooks.py`](../animations/ch01_precise_limit_hooks.py) `EpsilonDeltaTube`。實作改用**凸函數 $f(x)=\tfrac12x^2$**（非靜態頂著版的直線）——直線時框角恆落在線上、δ 擬合不可見；凸曲線才演得出「ε 縮 → 舊 δ 失守、曲線戳出帶子 → 縮 δ 收回」，端點以紅／綠示「出框／收住」。靜態 storyboard 仍頂著線性版，整合時由本動畫取代。（注：HTML Figure 1.21 亦用拋物線；2026-06-14 動畫診斷出三項待修——挖空點誤導、曲線/參數與 running example 不連貫、ε 過小時構圖擁擠，見 [`../REBUILD_STATUS.md`](../REBUILD_STATUS.md)。）

### 8. diagnose_wrong_definition
- **source:** `chapter1-print-standalone.html` §1.6 · Example 1.38（diagnose a wrong definition，L1709–1724；import expansion，audit-approved）
- **learning_goal:** 透過抓出一個寫錯的定義，鞏固「ε 先出、δ 回應」的量詞順序，以及「x 近 a ⟹ f(x) 近 L」的蘊含方向。
- **kind:** `counterexample`
- **narration:**
  > Before we put the definition to work, let us make sure we can recognize a broken one — that is the surest test of whether we have really understood it. Here is a tempting but wrong attempt: given any $\delta>0$, there exists an $\varepsilon>0$ such that whenever $|f(x)-L|<\varepsilon$, we have $0<|x-a|<\delta$. Two things are reversed. First, the order of the challenge: the tolerance $\varepsilon$ must come first, on the output side — you name $\varepsilon$, and $\delta$ is the response — but this version hands us the easy quantity only after we have seen the hard one. Second, the implication points the wrong way: the definition must say that closeness of $x$ to $a$ forces closeness of $f(x)$ to $L$, that is $0<|x-a|<\delta$ implies $|f(x)-L|<\varepsilon$, not the other way around. Repair both, and you land exactly on the definition we just wrote.
- **visual_need:** 並排對比兩版定義——**錯誤版**（標紅兩處：量詞順序 $\forall\delta\,\exists\varepsilon$、蘊含方向 $|f(x)-L|<\varepsilon \Rightarrow 0<|x-a|<\delta$）vs **正確版**（$\forall\varepsilon\,\exists\delta$、$0<|x-a|<\delta \Rightarrow |f(x)-L|<\varepsilon$）。純符號 compare（§5 不另配圖；邏輯結構本身就是 beat）。
- **animation_cue:** —（選用：把錯誤版兩處「翻正」——量詞 $\forall\delta\exists\varepsilon$ 對調成 $\forall\varepsilon\exists\delta$、蘊含箭頭反轉——動態演出「兩處都反了」；靜態並排亦可，留待動畫階段定。）

### 9. uniqueness_statement_and_trap
- **source:** `chapter1-print-standalone.html` §1.6 · Proposition 1.7 [Uniqueness of limits] statement + 反證 setup（L1726–1740）
- **learning_goal:** 知道極限一旦存在就唯一；看懂反證法的關鍵布局：取 $\varepsilon=\tfrac{|L-M|}{2}$。
- **kind:** `theorem`
- **narration:**
  > The definition earns its keep immediately: it guarantees that a limit, once it exists, is unique. Why even worry? Because nothing so far forbids two different numbers $L$ and $M$ from both passing the test — so suppose, for contradiction, that they do. Here is the clever move that breaks it: let $\varepsilon$ be half the gap between them, $\varepsilon=\tfrac{|L-M|}{2}$. Since $L\ne M$, this $\varepsilon$ is strictly positive, so it is a perfectly legal tolerance we are allowed to feed the definition. We have set a trap; the next step springs it.
- **visual_need:** 命題陳述「If $\lim_{x\to a}f(x)$ exists, it is unique」；反證 setup：assume $L\ne M$、令 $\varepsilon=\tfrac{|L-M|}{2}>0$。（純符號）
- **animation_cue:** —（靜態即可；陳述與 setup 兩段揭示）

### 10. uniqueness_proof_triangle
- **source:** `chapter1-print-standalone.html` §1.6 · Proof（triangle-inequality contradiction，L1740–1746）
- **learning_goal:** 用三角不等式把 $|L-M|$ 逼成「嚴格小於自己」，得出矛盾、收掉唯一性。
- **kind:** `proof`
- **narration:**
  > Now spring it. Feed that $\varepsilon$ to each limit: there is a $\delta_1$ that makes $f(x)$ hug $L$, and a $\delta_2$ that makes it hug $M$. Take any $x$ nearer to $a$ than both — closer than the smaller of $\delta_1$ and $\delta_2$ — and both promises hold at once. Now watch the gap collapse: $|L-M|$ rewrites as $|L-f(x)+f(x)-M|$, which by the triangle inequality is at most $|L-f(x)|+|f(x)-M|$, and since each piece is below $\varepsilon$, the total is below $2\varepsilon$. But $2\varepsilon$ was defined to be exactly $|L-M|$. We have forced $|L-M|$ to be strictly less than itself — impossible. The only way out is that there was no gap at all: $L=M$.
- **visual_need:** 對齊推導鏈：$|L-M| = |L-f(x)+f(x)-M| \le |L-f(x)|+|f(x)-M| < 2\varepsilon = |L-M|$；末行回到 $|L-M|$ 標「矛盾」。（純符號；不配圖）
- **animation_cue:** —（靜態即可；推導逐行、矛盾收尾那行強調）

### 11. epsilon_delta_recipe
- **source:** `chapter1-print-standalone.html` §1.6 · Strategy 1.3 [Verifying a limit from the ε-δ definition]（L1750–1761）
- **learning_goal:** 掌握 ε-δ 驗證的通用四步，含「雜散因子→取 min」的條件分支。
- **kind:** `procedure`
- **narration:**
  > Every verification that follows runs on one recipe. Start from a generic $\varepsilon>0$ — that is the challenge, and your job is to manufacture a $\delta$. Take the quantity $|f(x)-L|$ and bound it above by something times $|x-a|$, because $|x-a|$ is the thing $\delta$ controls. Then choose $\delta$ to drive that bound below $\varepsilon$. One wrinkle decides the difficulty: if the bound still carries a stray factor depending on $x$, first pen $x$ into a small interval around $a$ to cap that factor, then take $\delta$ to be the minimum of that interval's radius and your $\varepsilon$-based bound. The examples that follow run exactly this recipe — first a degenerate case where any $\delta$ works, then a clean linear one, then a quadratic where a stray factor must be tamed.
- **visual_need:** 四步驟編號列：1. start from generic $\varepsilon>0$；2. bound $|f(x)-L| \le (\text{factor})\cdot|x-a|$；3. choose $\delta$（雜散因子時：先框住 $x$ 上界、再取 $\delta=\min\{\text{radius},\ \varepsilon\text{-bound}\}$）；4. conclude $0<|x-a|<\delta \Rightarrow |f(x)-L|<\varepsilon$。（判斷型 strategy 不因分支拆單元——條件邏輯由 narration 承載。）
- **animation_cue:** —（靜態即可，四步逐一揭示）

### 12. verify_constant_limit
- **source:** `chapter1-print-standalone.html` §1.6 · Example 1.39（constant function, any $\delta$，L1763–1777；import expansion，audit-approved）
- **learning_goal:** 看見 ε-δ 的退化極端——常數函數 gap 恆為 0，任何 δ 都成立，δ 不必依賴 ε。
- **kind:** `example`
- **narration:**
  > Start with the easiest case the recipe will ever meet: show that $\lim_{x\to 2}5=5$. Given any $\varepsilon>0$, we need $|5-5|<\varepsilon$ whenever $0<|x-2|<\delta$. But that gap is simply $0$, and $0$ is below every positive $\varepsilon$, no matter where $x$ sits. So any $\delta$ at all does the job — take $\delta=\varepsilon$, or $\delta=1$, it makes no difference. This is the one situation where $\delta$ need not depend on $\varepsilon$ at all: when the output never moves, there is nothing for $\delta$ to control.
- **visual_need:** 推導：$|5-5|=0<\varepsilon$ always ⟹ any $\delta$ works（$\delta=\varepsilon$ 或 $\delta=1$）。（純符號；§5 不配圖）
- **animation_cue:** —（靜態即可）

### 13. verify_linear_limit
- **source:** `chapter1-print-standalone.html` §1.6 · Example 1.40（$\lim_{x\to3}(4x-5)=7$，L1779–1798）
- **learning_goal:** 在線性函數上跑完整的 ε-δ 驗證——無雜散因子，δ 直接落出。
- **kind:** `example`
- **narration:**
  > Now the recipe earns its keep — take the clean linear case: show $\lim_{x\to 3}(4x-5)=7$. Given a tolerance $\varepsilon$, measure the gap: $|(4x-5)-7|$ is $|4x-12|$, which factors as $4|x-3|$. We want that under $\varepsilon$, so we demand $|x-3|<\tfrac{\varepsilon}{4}$ — which hands us the choice $\delta=\tfrac{\varepsilon}{4}$. Check it: whenever $0<|x-3|<\delta$, the gap $4|x-3|$ is below $4\cdot\tfrac{\varepsilon}{4}$, which is exactly $\varepsilon$. The function is linear, there is no stray factor, and $\delta$ falls straight out of the algebra.
- **visual_need:** 對齊推導：$|(4x-5)-7|=|4x-12|=4|x-3|$；choose $\delta=\tfrac{\varepsilon}{4}$；verify $0<|x-3|<\delta \Rightarrow 4|x-3|<\varepsilon$。（純符號；§5 不配圖）
- **animation_cue:** —（靜態即可）
- **fold（代表式涵蓋，§2）：** **Example 1.42**（$\lim_{x\to0}\sin x=0$，借已知不等式 $|\sin x|\le|x|$ 得 $\delta=\varepsilon$，L1825–1841）與本線性例**同型**（無雜散因子、δ 直接落出；差別只在 bound 來源是「借來的不等式」而非代數因式分解）。依代表式涵蓋折疊於此、不另立單元；其 drill 留講義。若要在影片補一句口語指涉（如「有時 bound 由已知不等式白送、Step 2 免費」），於旁白認可時加入線性單元收尾。

### 14. verify_quadratic_limit
- **source:** `chapter1-print-standalone.html` §1.6 · Example 1.41（$\lim_{x\to1}(x^2-5x+6)=2$，L1800–1823）
- **learning_goal:** 在帶雜散因子的二次例上用「框住 + 取 min」化解 procedure 的條件分支。
- **kind:** `example`（**repeat-pattern：第二個同型例，MUST NOT 重述 ε-δ setup**）
- **narration:**
  > Same goal, but now the algebra fights back: show $\lim_{x\to 1}(x^2-5x+6)=2$. The gap is $|x^2-5x+4|$, which factors as $|x-1|\,|x-4|$. The first factor is what $\delta$ controls, but the second, $|x-4|$, drifts as $x$ moves — that is the stray factor the recipe warned about. So cap it: insist first that $|x-1|<1$, which traps $x$ between $0$ and $2$ and forces $|x-4|<4$. Now the gap is below $4|x-1|$, and to push that under $\varepsilon$ we also need $|x-1|<\tfrac{\varepsilon}{4}$ — so take $\delta=\min\{1,\tfrac{\varepsilon}{4}\}$, and both demands hold together. The minimum is not a trick; it is the recipe's wrinkle, made concrete.
- **visual_need:** 推導：$|x^2-5x+4|=|x-1||x-4|$；框住 $|x-1|<1 \Rightarrow 0<x<2 \Rightarrow |x-4|<4$；故 $<4|x-1|$；再要 $|x-1|<\tfrac{\varepsilon}{4}$；$\delta=\min\{1,\tfrac{\varepsilon}{4}\}$（強調 $\min$）。（純符號）
- **animation_cue:** —（靜態即可；$\min$ 與「框住 $x$」那步可閃示）

### 15. precise_infinite_limit
- **source:** `chapter1-print-standalone.html` §1.6 · Definition 1.14（infinite limit）+ 直覺散文（L1843–1859）
- **learning_goal:** 看出同一套 ε-δ 機器如何改寫無窮極限——量詞只是把目標換成「超過任意高度」。
- **kind:** `definition`
- **narration:**
  > The same machine handles limits that run off to infinity. We met those informally a little earlier; now we can say them precisely. We write $\lim_{x\to a}f(x)=\infty$ to mean: for every threshold $M>0$, there is a $\delta>0$ such that $f(x)>M$ whenever $0<|x-a|<\delta$. Notice the quantifier has only changed its target — instead of trapping $f$ near a value, we force it above any height you name. Pick $M$ as large as you like, a hundred or a googol; once $x$ is close enough to $a$, the function clears it. The $-\infty$ case is the mirror image: for every negative $N$, eventually $f(x)$ drops below it.
- **visual_need:** 兩條定義字卡：$\lim_{x\to a}f(x)=\infty \iff \forall M>0\ \exists\delta>0:\ f(x)>M$ when $0<|x-a|<\delta$；$=-\infty$ 同理（$\forall N<0\ \dots\ f(x)<N$）。對照 unit 6 的有限版量詞。（純符號）
- **animation_cue:** —（靜態即可）
- **note:** 講義此處 `\cref` 回指 §1.4 的非正式無窮極限定義——跨節 cref，narration **MUST NOT** 報節號，已轉述為 “a little earlier”。

### 16. verify_infinite_limit
- **source:** `chapter1-print-standalone.html` §1.6 · Example 1.43（M-δ proof $\lim_{x\to0}\tfrac{1}{x^2}=\infty$，L1861–1880；import expansion，AI-authored、audit-approved）
- **learning_goal:** 在無窮極限上跑一次 M-δ 驗證——選 $\delta=\tfrac{1}{\sqrt{M}}$ 讓 $\tfrac{1}{x^2}$ 超過任意高度 $M$，把 Definition 1.14 落到具體。
- **kind:** `example`（**repeat-pattern：承 unit 15 的 M-δ 定義，跳過量詞 setup、直接驗證**）
- **narration:**
  > The infinite-limit definition deserves a worked case of its own. Let us prove that $\lim_{x\to 0}\tfrac{1}{x^2}=\infty$. Now the challenge is a height $M$, however large, and our job is to force $\tfrac{1}{x^2}$ above it. Work backwards: $\tfrac{1}{x^2}>M$ exactly when $x^2<\tfrac{1}{M}$, which is when $|x|<\tfrac{1}{\sqrt{M}}$. So choose $\delta=\tfrac{1}{\sqrt{M}}$; then whenever $0<|x|<\delta$, we have $x^2<\tfrac{1}{M}$, and so $\tfrac{1}{x^2}$ clears $M$. Every height, no matter how enormous, is beaten once $x$ is close enough to $0$ — the rigorous version of the infinite limit we could only sketch earlier.
- **visual_need:** 對齊推導鏈：$\tfrac{1}{x^2}>M \iff x^2<\tfrac{1}{M} \iff |x|<\tfrac{1}{\sqrt{M}}$；choose $\delta=\tfrac{1}{\sqrt{M}}$；verify $0<|x|<\delta \Rightarrow x^2<\tfrac{1}{M} \Rightarrow \tfrac{1}{x^2}>M$。（純符號；§5 不配圖。）
- **animation_cue:** —（靜態即可；M-δ 對齊鏈逐行揭示）
- **note:** 講義此例 prose 回指 §1.4 的非正式 Example（無窮極限）——跨節引用，narration 轉述為 “we could only sketch earlier”、**不報例號**（§4）。

### 17. continuity_preview
- **source:** `chapter1-print-standalone.html` §1.6 · continuity prose（L1882–1884）
- **learning_goal:** 認得「連續」的定義雛形（$\lim_{x\to a}f(x)=f(a)$），知道它是極限語言的直接產物。
- **kind:** `forward_ref`（向前預告——獨立成單元，置於主內容與 recap 之間，**不報章號**）
- **narration:**
  > Before we gather up, the precise definition quietly hands us one more idea. Suppose $f$ is defined not just near $a$ but at $a$ as well, and suppose the limit equals the actual value: $\lim_{x\to a}f(x)=f(a)$. When that happens, we say $f$ is continuous at $a$. Look back at our broken function — its limit was $5$ but its value was $6$, so it failed exactly this test; continuity is the case where the approach and the destination finally agree. A full study of continuity comes later; we name it here only because the limit language expresses it so directly.
- **visual_need:** 一條字卡：$f$ continuous at $a \iff \lim_{x\to a}f(x)=f(a)$；一句回扣 unit 3 的 broken function（limit $5\ne$ value $6$ → 不連續）。（純符號 + 回扣，不另畫圖）
- **animation_cue:** —（靜態即可）

### 18. recap
- **source:** 全節綜合（書本 §1.6 無獨立 Summary；recap 為必有單元）
- **learning_goal:** 收攏本節主線：定義、圖像、唯一性、驗證 recipe。
- **kind:** `recap`
- **narration:**
  > Let us gather the thread. The vague word "close" became a precise contract: for every $\varepsilon>0$ there is a $\delta>0$ forcing $|f(x)-L|<\varepsilon$ whenever $0<|x-a|<\delta$. The picture to keep is the strip and the interval — inputs within $\delta$ of $a$ get carried into the band within $\varepsilon$ of $L$, and $\delta$ always answers to $\varepsilon$. The first payoff was uniqueness: a limit, once it exists, cannot be two numbers. And to verify a limit by hand, bound $|f(x)-L|$ by a multiple of $|x-a|$, choose $\delta$, and take a minimum whenever a stray factor needs taming. Every informal limit we computed in the earlier sections now stands on this one definition.
- **visual_need:** 重點 4 條 + 要記公式：定義式 $\forall\varepsilon\,\exists\delta:\ |f(x)-L|<\varepsilon$ when $0<|x-a|<\delta$；$\delta=\min\{\dots\}$（驗證時）。
- **animation_cue:** —（靜態即可）

### 19. outro
- **source:** 全節收尾（章末——§1.6 為 Chapter 1 最後一節）
- **learning_goal:** —（純品牌收尾）
- **kind:** `outro`
- **narration:** —（outro 無旁白）
- **visual_need:** 純品牌收尾字卡（暗轉亮橋接 → 最終 logo 字卡）。**不含 Key Takeaways**——重點在 unit 18 recap（有旁白的 `recap_cards` 場景）。（向前預告 `next:` 目前 outro 模板未渲染，故省略。）
- **animation_cue:** —（用 gen-2 既有 outro 模板，兩段式）

---

## 校準筆記（回饋給 CONTENT_METHODOLOGY.md）

本節是 **symbol-heavy 路徑的第一次實跑**（§1.1 約 40% 符號、七視覺；§1.6 約 90% 符號）。浮現幾點：

1. **§5 視覺預算如預期落地。** 16 單元只配 **2 個視覺**（anchor ε-δ 管狀圖 + 動機圖），正中 §5 校準註記預言的「§1.6 只有 anchor + 一個動機圖」。所有定義／定理／證明／procedure／兩個 ε-δ 例題／無窮極限定義／forward-ref/recap **皆純符號**——印證「不為每個代數例題配圖，符號本身就是 beat」。**建議方法論 §5 加一句明示：symbol-heavy 節的兩視覺通常是 (a) 核心定義的 anchor、(b) 一個動機／反差圖；代數驗證單元預設不配圖。**（2026-06-14 漂移修復新增的 3 個例題單元同樣全純符號，§5 結論不變——見文末漂移修復筆記。）

2. **theorem/proof 拆單元（§3）首次實跑。** §1.1 的 iff 證明只有 2 行、留在單一單元；§1.6 的唯一性證明是多步反證（取 $\varepsilon=\tfrac{|L-M|}{2}$ → 三角不等式 → $|L-M|<|L-M|$ 矛盾），依 §3「證明 >~4 步就拆」拆成 **unit 9（陳述＋反證布局）+ unit 10（三角不等式收尾）**，讓學生在「設好陷阱」後能暫停。這正是選 §1.6 要壓測的 theorem_proof 路徑。

3. **repeat-pattern（§4）首次實跑於 canonical 案例。** 兩個 ε-δ 例題：unit 13（線性、無雜散因子）建立 setup，unit 14（二次、$\delta=\min\{1,\varepsilon/4\}$）**以「Same goal, but now the algebra fights back」開場、跳過 setup**。ε-δ 雙例正是 §4 repeat-pattern 的教科書場景。

4. **對齊鏈 narration（§4）吃重。** 唯一性證明與兩例題都用對齊推導；narration 一律「首行念全式、中段只念連接詞＋RHS」，唯一性結尾回到 $|L-M|$ 時明白點出「strictly less than itself — impossible」（§4 規定的矛盾收尾點名）。symbol-heavy 節是這條規則的主要受力點。

5. **running example 當「定義的脊梁」。** unit 3→4→5→6→7 全用同一條 $f(x)=2x-1$（$a=3,L=5$）：動機（值 6≠極限 5）→ 容差遊戲（0.1）→ 推廣到每個 ε → 定義 → anchor 圖。**單一具體函數貫穿多單元**，給抽象 ε-δ 一根具體脊梁；unit 17 forward-ref 再回扣同一函數示範「不連續」。**建議方法論補：symbol-heavy 節 SHOULD 選一個 running example 串起動機→定義→圖，避免定義懸空。** （比 §1.1 unit 12 的孤立鏡射例更進一步。）

6. **跨節 cref 轉述。** unit 15 講義 `\cref` 回指 §1.4 的非正式無窮極限，narration 轉述為 “a little earlier”、不報節號——確認 §4「不報 cref 目標」不只適用跨章，跨節亦然。

### render 階段實跑發現（第二階段工程，補記）

走完 storyboard→mock 成片後，render 階段抓到兩個 **lint 與 sizecheck 都漏掉**的問題，皆 symbol-heavy 節特有，值得回饋：

7. **prose sibling 內嵌 inline math → 被縮小而非 wrap → sizecheck error。** `procedure_steps` 的 step text 與 `recap_cards` 的 points 一旦內嵌 `$math$` 就 route 到 Tex（單行、不 wrap），過長被 `scale_to_fit` 縮小，與相鄰純文字 sibling 字級不一致，觸發 sizecheck（recipe row.2=14.6 vs 23；recap point.1/3=18.x vs 23）。**修法：這些 stacked-prose sibling 欄位（procedure step text、recap points）改為純英文，符號留給專屬的 math 欄／formula card。** symbol-heavy 節最易犯——每個 bullet 都想塞符號。

8. **recap formula card 過寬 → 靜默出框被裁，lint 與 sizecheck 都不擋。** recap formula 走 `math_line`（不 wrap、不 width-fit），右欄又窄，長公式直接溢出畫面右緣；lint 只查標記/`$` 平衡、sizecheck 只比 sibling 字級，**出框寬度無任何守門員**——只有看 frame 才發現。**修法：沿 §1.1 慣例「recap formula 必須短」，把 ε-δ 拆成兩個短半式（`0<|x-a|<δ`、`|f(x)-L|<ε`）。建議 DESIGN.md Authoring checklist 增一列：recap/formula card 不 wrap、過寬會靜默出框；保持短或工程上加 width guard。**

9. **graph_focus 無填色帶狀，但 dashed-line 重現足矣（無 template 缺口）。** ε-δ 管狀圖 anchor 用 4 條 dashed `line`（兩水平 ε、兩垂直 δ）+ `function` + hollow `point` 重現，忠於講義 fig:precise-limit（書本本身也用虛線界線、非填色）。確認 §5 的 anchor 不需要新增 template 能力，現有 3 種 plot kind（function/line/point）已足夠。兩個 hollow-point lint warn（值不存在的洞）為正當例外，非錯誤。

### 漂移修復（2026-06-14，內容權威換源 HTML §1.6）

依 [`../REBUILD_STATUS.md`](../REBUILD_STATUS.md) 標記的 §1.6 significant drift，本節內容稿由舊 `ch01_foundations.tex` 重指定稿 HTML [`chapter1-print-standalone.html`](../../experiments/handout_kit/chapter1-print-standalone.html) §1.6（L1655–1884）：

10. **provenance 全面重指＋記錄環境編號。** 14 個既有單元的 `source:` 自 `.tex` 行號改指 HTML §1.6＋手寫編號：**Definition 1.13**（ε-δ limit）、**Definition 1.14**（infinite limit）、**Proposition 1.7**（Uniqueness of limits）、**Strategy 1.3**、**Figure 1.21**（fig:precise-limit）、**Example 1.37/1.40/1.41**。narration 主幹零刪改（既有單元逐字保留）。

11. **採納 HTML import 的 3 個新例題（代表式涵蓋，§2；三者皆 audit-approved）：**
    - **Example 1.38**（診斷寫錯的定義）→ 新 **unit 8 `diagnose_wrong_definition`**：新概念模式（量詞順序＋蘊含方向），緊接定義／anchor 之後鞏固結構。
    - **Example 1.39**（常數函數、任意 δ）→ 新 **unit 12 `verify_constant_limit`**：補「δ 不必依賴 ε」的退化極端，置於 recipe 之後、線性例之前（最簡 warm-up）。
    - **Example 1.43**（$\tfrac{1}{x^2}=\infty$ 的 M-δ 證）→ 新 **unit 16 `verify_infinite_limit`**：補 Definition 1.14 唯一 worked example，緊接無窮極限定義。
    recipe（unit 11）收尾原述「next two examples」改述為「退化／線性／二次」三例，以容納新增的常數例；連帶 unit 13 線性例開場由「Take the clean case first」改為「Now the recipe earns its keep — take the clean linear case」（六-lens 稽核抓到的序位 stale，見下節）。**這兩處是唯一改動到既有單元 narration 之處，需重新認可。**

12. **折疊 Example 1.42**（$\lim\sin x=0$ via $|\sin x|\le|x|$）於 unit 13 線性例（同型：無雜散因子、δ 直接落出，差別僅 bound 來源）；就近 fold 註見 unit 13。

13. **§5 視覺預算不變。** 三個新單元皆純符號（診斷用 compare、兩驗證用推導鏈），**未新增任何圖形視覺**；anchor（unit 7）＋動機圖（unit 3）仍是僅有的兩個圖形視覺。

> **待辦：** 新增單元（u8/u12/u16）旁白＋兩處改動的既有旁白（u11 recipe 收尾、u13 線性例開場）**待使用者認可**（§6 交付形式：重編 `ch01_precise_limit_narration.html` 審核稿）。認可後才進第二階段工程（storyboard 同步重指＋新場景＋scene 7 凸曲線）。本次修復**未動**動畫與計費 API。

### 六-lens 對抗式稽核（2026-06-14，Workflow `wfjunb6w2`，6 lens 並行）

Scoped 到漂移修復的新材料（u8/u12/u16＋Ex 1.42 fold＋recipe reword），對照定稿 HTML §1.6＋方法論。結果：

- **clean：** math-accuracy（**0 錯**，獨立重推 u8 兩處反轉、u12 `|5-5|=0<ε` 任意 δ、u16 `δ=1/√M ⟹ x²<1/M ⟹ 1/x²>M` 皆通過）、register（§4 無違規、u16 確走 repeat-pattern、未報例號）、faithfulness（新單元忠於 HTML、Ex 1.42 折疊判定 defensible）、no-repeat、completeness（§1.6 全環境覆蓋、無缺漏無雙覆）。
- **1 條 tier-2 actionable（decomposition）：** u13 線性例開場「Take the clean case **first**」在插入常數例（u12）＋recipe 改述三例後變 stale、序位自相矛盾 → **已改**為「Now the recipe earns its keep — take the clean linear case」。
- **tier-3 editorial（不改，均判 defensible）：** u16 backward-derivation 改寫（與 HTML forward 證等價、更適口語）；u12／u13 皆述 ε-δ setup（u12 退化 warm-up、u13 才首建機制供 u14 repeat-pattern 繼承，深度不同）；running example $2x-1$ 不另行正式 ε-δ 驗證（其角色為錨定定義／圖，且 u4/u5 已 informally 處理 tolerance 遊戲）。
- **回歸：** 僅改 u13 開場一句，未觸及 `{show}`／數學內容，未引入新問題。原始 finding 見 Workflow 結果。
