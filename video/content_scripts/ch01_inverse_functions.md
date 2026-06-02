# Section 1.1 Inverse Functions — 內容稿（校準樣本）

> **性質：校準樣本**，用來驗證 [`../CONTENT_METHODOLOGY.md`](../CONTENT_METHODOLOGY.md) 是否可操作——**不是**產線輸出（§1.1 原型將全面棄用）。
> **來源：** [`../../chapters/ch01_foundations.tex`](../../chapters/ch01_foundations.tex) §1.1（L16–268）。
> **格式：** 純內容層，每單元 `id / source / learning_goal / kind / narration / visual_need / animation_cue`；**不含** template / `{show}` / accent / 視覺 payload（第二階段才填）。`narration` 為英文（旁白語言）；`visual_need` / `animation_cue` 為中文（內容溝通用）。動畫一律**客製 manim、使用者自畫**——這裡只給自然語言建議。

---

## Deck meta（intro / outro 用）

```
chapter:       Chapter 1
chapter_title: Inverse Functions and Limits
section:       1.1
title:         Inverse Functions
tagline:       When can a process be run backwards?
sections:      [1.1 Inverse Functions, 1.2 Inverse Trigonometric Functions,
                1.3 The Limit of a Function, 1.4 One-Sided and Infinite Limits,
                1.5 Limit Laws and Computational Techniques,
                1.6 The Precise Definition of a Limit]
next:          Up next — Inverse Trigonometric Functions
```

---

## 教學單元

### 1. intro
- **source:** §1.1 整節 + 章定位（L1–19）
- **learning_goal:** —（純品牌開場）
- **kind:** `intro`
- **narration:** —（intro 無旁白）
- **visual_need:** Section Gate：章地圖聚焦 §1.1 → 標題 “Inverse Functions” + tagline “When can a process be run backwards?”
- **animation_cue:** —（用 gen-2 既有 intro 模板）

### 2. why_reverse_needs_one_to_one
- **source:** §1.1 opener prose + numeric warm-ups（L18–27）
- **learning_goal:** 看出「反轉一個過程」自然要求每個輸出只來自一個輸入。
- **kind:** `motivation`
- **narration:**
  > We begin with a simple question: when can a process be run backwards? If a rule turns each input into an output, we often want to recover the input from the output. Watch two quick cases. For $f(x)=x$ on $[0,1]$, every input keeps its own value, so each output came from exactly one input. But for $f(x)=x^2$ on $[-1,1]$, both $\tfrac12$ and $-\tfrac12$ produce $\tfrac14$ — one output from two inputs. Reversing only makes sense in the first case, and that is the property we need to pin down.
- **visual_need:** 兩組對應示意：$f(x)=x$ 幾個輸入各射向不同輸出（一對一）；$f(x)=x^2$ 的 $\tfrac12$、$-\tfrac12$ 都指向 $\tfrac14$（兩進一出）。
- **animation_cue:** 客製 manim：左 $f(x)=x$，數個輸入點各畫一條箭頭到相異輸出；右 $f(x)=x^2$，$\tfrac12$ 與 $-\tfrac12$ 兩條箭頭匯聚到同一個 $\tfrac14$，匯聚瞬間閃一下，凸顯「兩進一出、無從回頭」。

### 3. one_to_one_definition
- **source:** §1.1.1 `\begin{definition}`（L33–45）
- **learning_goal:** 認得讓函數可逆的形式條件——one-to-one。
- **kind:** `definition`
- **narration:**
  > The property is called one-to-one. A function is one-to-one when different inputs always give different outputs: $f(x_1)\ne f(x_2)$ whenever $x_1\ne x_2$. There is an equivalent form that is easier to use inside a proof — if $f(x_1)=f(x_2)$, then $x_1=x_2$. Both say the same thing: no two distinct inputs can ever land on the same output.
- **visual_need:** 一句白話定義 + 兩條等價式（$f(x_1)\ne f(x_2)$ whenever $x_1\ne x_2$；$f(x_1)=f(x_2)\implies x_1=x_2$），第二式強調（證明常用）。
- **animation_cue:** —（靜態即可）

### 4. student_id_is_one_to_one
- **source:** §1.1.1 `workedexample`（L48–60）
- **learning_goal:** 先在日常情境套定義，建立「看對應、別急著看符號」的習慣。
- **kind:** `example`
- **narration:**
  > Before any algebra, here is the idea in plain terms. Assign each student in a class an ID number, with no two students sharing a number. Is the rule from student to ID one-to-one? Yes — distinct students always get distinct numbers, exactly the condition we just wrote down. The habit to build early: ask whether one output could trace back to two different inputs.
- **visual_need:** 學生 → ID 的一對一對應（幾名學生各連到不同號碼，連線互不交會）。
- **animation_cue:** —（靜態即可；連線可逐條畫出）

### 5. testing_x_and_x_squared
- **source:** §1.1.1 `workedexample`（L64–83）
- **learning_goal:** 用代數判定一個函數是不是 one-to-one。
- **kind:** `example`
- **narration:**
  > Now test two functions algebraically. On $[0,1]$, $f(x)=x$ sends each input to itself, so distinct inputs give distinct outputs — one-to-one. Now take $g(x)=x^2$ on $[-1,1]$: compute $g(\tfrac12)=\tfrac14$ and $g(-\tfrac12)=\tfrac14$. Two different inputs, the same output, so $g$ is not one-to-one. A single colliding pair is all it takes to fail.
- **visual_need:** 兩欄：$f(x)=x$ 標 one-to-one；$g(x)=x^2$ 顯示 $g(\tfrac12)=\tfrac14=g(-\tfrac12)$ 標 collide。
- **animation_cue:** —（靜態即可；collide 那行可閃示）

### 6. why_square_cannot_invert
- **source:** §1.1.1 prose（L85）
- **learning_goal:** 看見「重複輸出」如何讓反函數無法定義。
- **kind:** `counterexample`
- **narration:**
  > Why does that collision matter so much? If we tried to run $g(x)=x^2$ backwards on $[-1,1]$, the output $\tfrac14$ would have to return two different inputs, $\tfrac12$ and $-\tfrac12$. A function is not allowed to send one input to two outputs, so no inverse rule can exist here. That is the whole reason one-to-one is the condition we insist on.
- **visual_need:** parabola $y=x^2$ on $[-1,1]$；水平線 $y=\tfrac14$；兩交點 $x=\pm\tfrac12$。
- **animation_cue:** 客製 manim：水平線從畫面上方緩緩下移、掃過 parabola；落到 $y=\tfrac14$ 時停住，同時在 $x=-\tfrac12$、$x=\tfrac12$ 閃示兩個實心點，各拉一條虛線回 x 軸，凸顯「一個輸出 ← 兩個輸入」，反函數無從決定回哪一個。

### 7. horizontal_line_test
- **source:** §1.1.1 `remark[Horizontal line test]` + `figure`（L89–134）
- **learning_goal:** 把 one-to-one 的定義轉成可在圖上一眼判讀的幾何測試。
- **kind:** `proposition`（具名規則）
- **narration:**
  > Here is the graphical version. A horizontal line $y=c$ meets the graph wherever $f(x)=c$. So a function is one-to-one exactly when no horizontal line crosses its graph more than once. If some line hits twice, two inputs share the output $c$ — not one-to-one. If every line hits at most once, each output traces back to a single input. Same condition as before, now readable at a glance.
- **visual_need:** 並排兩圖。左：遞增直線，水平線只交一次（one-to-one）；右：parabola，水平線交兩次，標 $(x_1,c)$、$(x_2,c)$（not one-to-one）。
- **animation_cue:** 客製 manim（對應 gen-1 的 side-by-side hook）：左右兩圖並排，各放一條水平線從上往下 sweep；左圖始終只有一個交點（綠、通過），右圖掃到某高度時冒出兩個交點（紅、閃示），直觀對比「通過 vs 失敗」。

### 8. inverse_function_definition
- **source:** §1.1.2 `\begin{definition}` + `remark`（L140–152）
- **learning_goal:** 把反函數理解成「把對應關係反過來」的函數。
- **kind:** `definition`
- **narration:**
  > Once $f$ is one-to-one, we can define its inverse. With domain $A$ and range $B$, the inverse $f^{-1}$ has domain $B$ and range $A$, defined by: $f^{-1}(y)=x$ means exactly $f(x)=y$. Domain and range swap roles — the outputs of $f$ become the inputs of $f^{-1}$. Sometimes we relabel and write $x$ as the input of $f^{-1}$, but that is only renaming; the content is that the inverse reverses the original correspondence.
- **visual_need:** 定義式 $f^{-1}(y)=x \Longleftrightarrow f(x)=y$；標示 domain/range 互換（$A\leftrightarrow B$）。
- **animation_cue:** —（靜態即可；與單元 11 的映射圖呼應，此處可不重複）

### 9. inverse_exists_iff_one_to_one
- **source:** §1.1.2 `theorem` + `proof`（L154–165）
- **learning_goal:** 用「有反函數 ⟺ one-to-one」這個完整判準。
- **kind:** `theorem`
- **narration:**
  > This theorem ties it together: a function has an inverse if and only if it is one-to-one. One direction — if $f$ has an inverse and $f(x_1)=f(x_2)$, apply $f^{-1}$ to both sides to get $x_1=x_2$, so $f$ is one-to-one. The other direction — if $f$ is one-to-one, then every output $y$ in the range comes from exactly one input $x$, and sending $y$ back to that $x$ defines the inverse. So the property we studied is not merely useful; it is exactly the right condition.
- **visual_need:** 定理陳述（iff）；證明兩方向各一行（⇒：對 $f(x_1)=f(x_2)$ 施 $f^{-1}$ 得 $x_1=x_2$；⇐：每個 $y$ 唯一 $x$，$y\mapsto x$ 定義 $f^{-1}$）。
- **animation_cue:** —（靜態即可，兩方向逐步揭示）

### 10. first_inverses_x_and_cube
- **source:** §1.1.2 `workedexample`（L167–187）
- **learning_goal:** 在已知 one-to-one 的函數上實際算出反函數，並用合成檢查。
- **kind:** `example`
- **narration:**
  > Two quick inverses. The identity $f(x)=x$ leaves every input alone, so it is its own inverse: $f^{-1}(x)=x$. For $g(x)=x^3$, set $y=x^3$, solve to get $x=\sqrt[3]{y}$, then rename to $g^{-1}(x)=\sqrt[3]{x}$. Check by composition: $g(g^{-1}(x))=(\sqrt[3]{x})^3=x$. The cube and the cube root undo each other, exactly as an inverse should.
- **visual_need:** 兩例：$f^{-1}(x)=x$；$g$：$y=x^3 \to x=\sqrt[3]{y} \to g^{-1}(x)=\sqrt[3]{x}$，檢查 $g(g^{-1}(x))=x$。
- **animation_cue:** —（靜態即可）

### 11. composition_identities
- **source:** §1.1.2 `proposition` + `figure`（L189–230）
- **learning_goal:** 記住認證反函數的兩個合成恆等式。
- **kind:** `proposition`
- **narration:**
  > The defining relation gives two identities worth remembering. Apply $f$ then $f^{-1}$ and you return to the start: $f^{-1}(f(x))=x$ for every $x$ in $A$. Apply them the other way and the same thing happens: $f(f^{-1}(y))=y$ for every $y$ in $B$. Going out and coming back lands you exactly where you began — that round trip is what 'inverse' really means.
- **visual_need:** 兩式 $f^{-1}(f(x))=x$、$f(f^{-1}(y))=y$；映射圖：$A\leftrightarrow B$，$f$ 與 $f^{-1}$ 反向箭頭。
- **animation_cue:** 客製 manim：$x\in A$ 沿 $f$ 箭頭走到 $f(x)\in B$，再沿 $f^{-1}$ 箭頭走回原本的 $x$（回到原位時閃一下）；另一組 $y\in B$ 同理往返，凸顯「出去再回來、回到原點」。

### 12. reflection_across_y_equals_x
- **source:** §1.1.2 prose（L232–233）
- **learning_goal:** 看見 $f$ 與 $f^{-1}$ 的圖互為對 $y=x$ 的鏡射。
- **kind:** `visual`
- **narration:**
  > There is a clean picture behind all of this. Draw $f$ and its inverse in the same plane, and the two graphs are mirror images across the line $y=x$. The reason is the swap: $(a,b)$ lies on $f$ exactly when $(b,a)$ lies on $f^{-1}$, and reflecting across $y=x$ is precisely what trades a point's two coordinates. So the inverse's graph is just the original, flipped over the diagonal.
- **visual_need:** 同一平面畫 $y=x^3$ 與 $y=\sqrt[3]{x}$，虛線 $y=x$；標一對對應點 $(a,b)$、$(b,a)$。（用 $x^3/\sqrt[3]{x}$ 呼應單元 10——以具體函數示範散文的一般主張。）
- **animation_cue:** 客製 manim：先畫 $f(x)=x^3$，再畫對角虛線 $y=x$，然後讓曲線「對 $y=x$ 翻摺」生成 $f^{-1}(x)=\sqrt[3]{x}$；過程中標一點 $(a,b)$ 翻到 $(b,a)$，凸顯座標對調。

### 13. procedure_find_inverse
- **source:** §1.1.3 `strategy`（L239–245）
- **learning_goal:** 掌握求反函數的標準三步驟代數程序。
- **kind:** `procedure`
- **narration:**
  > When $f$ is one-to-one, a short recipe finds the inverse. Step one: write $y=f(x)$. Step two: solve that equation for $x$ in terms of $y$. Step three: interchange the names $x$ and $y$, and the result is $y=f^{-1}(x)$. That last swap is not cosmetic — it rewrites the answer as a function of $x$, ready to use.
- **visual_need:** 三步驟編號列：1. $y=f(x)$；2. solve for $x$；3. swap → $y=f^{-1}(x)$。
- **animation_cue:** —（靜態即可，三步逐一揭示）

### 14. worked_inverse_cubic_shift
- **source:** §1.1.3 `workedexample`（L247–266）
- **learning_goal:** 把三步驟套到具體函數，並用合成驗證答案。
- **kind:** `example`
- **narration:**
  > Apply the recipe to $f(x)=x^3+2$. Write $y=x^3+2$. Solving for $x$ gives $x^3=y-2$, then $x=\sqrt[3]{y-2}$. Interchange the names to get $f^{-1}(x)=\sqrt[3]{x-2}$. Always check by composition: $f(f^{-1}(x))$ is $(\sqrt[3]{x-2})^3+2$, which is $(x-2)+2$, which is $x$. It returns $x$, so the inverse is correct.
- **visual_need:** 對齊推導：$y=x^3+2$；$x^3=y-2$；$x=\sqrt[3]{y-2}$；$f^{-1}(x)=\sqrt[3]{x-2}$（強調）。驗證鏈 $f(f^{-1}(x))=(\sqrt[3]{x-2})^3+2=(x-2)+2=x$。
- **animation_cue:** —（靜態即可；推導逐行、最終答案強調）

### 15. recap
- **source:** 全節綜合（書本無 Summary，recap 為必有單元）
- **learning_goal:** 收攏本節主線。
- **kind:** `recap`
- **narration:**
  > Let us gather the thread. One-to-one means no two inputs collide on the same output. The horizontal line test is the visual version of that check. A function has an inverse exactly when it is one-to-one, and the two composition identities certify any candidate. To build an inverse: write $y=f(x)$, solve for $x$, swap the names. And keep the picture in mind — the inverse's graph is the original, reflected across $y=x$.
- **visual_need:** 重點 4–5 條 + 要記公式：$f(x_1)=f(x_2)\Rightarrow x_1=x_2$、$f^{-1}(f(x))=x$。
- **animation_cue:** —（靜態即可）

### 16. outro
- **source:** 全節收尾
- **learning_goal:** —（純品牌收尾）
- **kind:** `outro`
- **narration:** —（outro 無旁白）
- **visual_need:** 純品牌收尾字卡（暗轉亮橋接 → 最終 logo 字卡）。**不含 Key Takeaways**——重點在 unit 15 recap（有旁白的 `recap_cards` 場景）。（向前預告 `next:` 目前 outro 模板未渲染，故省略。）
- **animation_cue:** —（用 gen-2 既有 outro 模板，兩段式）

---

## 校準筆記（回饋給 CONTENT_METHODOLOGY.md）

走完一節後，浮現幾個方法論可補的細則：

1. **具名規則 + 其演示圖的合／拆**：本稿把「水平線測試」的 `remark`（規則）與 `figure`（兩情形圖）併成**一個**單元（單元 7），因為「規則」與「讀它的圖」是同一個教學重點；gen-1 曾拆成兩 slide。建議方法論加一句：*具名規則與其演示圖，若共一個教學重點則合為一個單元，narration 過載才拆。*
2. **視覺單元 MAY 選具體函數示範一般主張**：講義 L232–233 只給「對 $y=x$ 鏡射」的一般原理，本稿在單元 12 選 $x^3/\sqrt[3]{x}$ 來示範。這屬「增補呈現、不增刪內容」，但值得在 §5 明說：*視覺單元 MAY 挑一個具體函數，把散文的一般幾何主張畫出來。*
3. **動畫密度**：16 單元中 5 個帶 `animation_cue`（motivation、why-x²-fails、line-test、composition、reflection），全是「過程／對應／掃描／鏡射」型；定義、定理、計算、procedure、recap 皆靜態。比例自然，印證 §5 的「會動的概念才動」。
4. **detail over compression 對齊**：16 單元對 ~250 行講義，與 gen-1 的 16 scenes 吻合，且每單元可回溯講義行號（忠實度成立）。
