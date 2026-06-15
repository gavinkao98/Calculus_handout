# Section 1.1 Inverse Functions — 內容稿 v2（正式版）

> **性質：正式產線內容稿（v2）**。依 2026-06-10 拍板**從零重走**：不繼承 v1 校準樣本的 narration，全文以 HTML 講義權威檔重新拆解、重新撰寫（v1 為方法論校準原型，已隨本檔覆寫棄用）。**原 15 段 narration 已於 2026-06-10 經使用者認可；u14 `repair_by_restricting`、u17 `temperature_conversion` 為 2026-06-13 依代表式涵蓋（§2）新增（Example 1.5／1.8），narration 同日經使用者認可。**
> **來源（權威）：** [`../../experiments/handout_kit/chapter1-print-standalone.html`](../../experiments/handout_kit/chapter1-print-standalone.html) §1.1（`sec-no` 1.1，Inverse Functions）。
> **格式：** 純內容層，每單元 `id / source / learning_goal / kind / narration / visual_need / animation_cue`；**不含** template / `{show}` / accent / 視覺 payload（第二階段才填）。`narration` 為英文（旁白語言）；`visual_need` / `animation_cue` 為中文（內容溝通用）。客製動畫由 Claude 依 `animation_cue` 生成（本節依拍板**第二輪**才接入；本輪工程稿以模板靜態頂著）。

---

## Deck meta（intro / outro 用）

```
chapter:       Chapter 1
chapter_title: Inverse Functions and Limits
section:       1.1
title:         Inverse Functions
tagline:       When can a function be undone?
sections:      [1.1 Inverse Functions, 1.2 Inverse Trigonometric Functions,
                1.3 The Limit of a Function, 1.4 One-Sided and Infinite Limits,
                1.5 Limit Laws and Computational Techniques,
                1.6 The Precise Definition of a Limit]
```

---

## 教學單元

### 1. intro
- **source:** §1.1 整節 + 章定位（standalone `<title>`：Chapter 1 — Inverse Functions and Limits）
- **learning_goal:** —（純品牌開場）
- **kind:** `intro`
- **narration:** —（intro 無旁白）
- **visual_need:** Section Gate：章地圖聚焦 §1.1 → 標題 “Inverse Functions” + tagline “When can a function be undone?”
- **animation_cue:** —（用 gen-2 既有 intro 模板）

### 2. can_we_go_backwards
- **source:** §1.1 · opening prose + `ol.warmup` (a)(b) + 例後 central-point prose（Definition 1.1 之前）
- **learning_goal:** 從兩個具體函數看出：能否「由輸出回推輸入」取決於每個輸出來自幾個輸入。
- **kind:** `motivation`
- **narration:**
  > Every function is a one-way machine: feed it an input, and it hands you an output. This section asks the reverse question — starting from the output, can we recover the input that produced it? Watch two quick cases. For $f(x)=x$ on $[0,1]$, every input keeps its own value: $0$ stays at $0$, one half stays at one half. But for $f(x)=x^2$ on $[-1,1]$, something breaks: both $\tfrac12$ and $-\tfrac12$ are sent to $\tfrac14$. In the first case, each output points back to exactly one input; in the second, the output $\tfrac14$ cannot tell us which input it came from — and that difference is the whole story of this section.
- **visual_need:** 兩組對應示意並排：左 $f(x)=x$ 數個輸入各自連到自己的輸出；右 $f(x)=x^2$ 的 $\tfrac12$、$-\tfrac12$ 同時連到 $\tfrac14$。
- **animation_cue:** 左圖幾條箭頭依序亮起、各入各位；右圖 $\tfrac12$ 與 $-\tfrac12$ 兩條箭頭匯聚到同一個 $\tfrac14$，匯聚瞬間頓一下並強調該點，凸顯「兩進一出——回不去」。

### 3. one_to_one_definition
- **source:** chapter1-print-standalone.html §1.1 · Definition 1.1（含 `informal` gloss）
- **learning_goal:** 認得 one-to-one 的形式定義與其等價形式，知道後者是計算裡實際用的。
- **kind:** `definition`
- **narration:**
  > The property that separates the two cases has a name: one-to-one. A function $f$ is one-to-one if $f(x_1) \ne f(x_2)$ whenever $x_1 \ne x_2$ — different inputs always produce different outputs. The same condition can be turned around: if $f(x_1) = f(x_2)$, then $x_1 = x_2$. Both forms say the same thing, but the second one is the workhorse in computations: assume two outputs agree, and deduce that the inputs were equal all along.
- **visual_need:** 一句白話定義 + 兩條等價式（$f(x_1)\ne f(x_2)$ whenever $x_1\ne x_2$；$f(x_1)=f(x_2)\implies x_1=x_2$），第二式視覺強調（計算常用形）。
- **animation_cue:** —（靜態即可）

### 4. ids_before_algebra
- **source:** chapter1-print-standalone.html §1.1 · Example 1.1 + Solution（student ID）
- **learning_goal:** 在無公式的日常情境先套用定義，建立「一對一是對應問題、不是代數問題」的直覺。
- **kind:** `example`
- **narration:**
  > Here is the definition at work in a setting with no formulas at all. Assign every student in a class an identification number, making sure no two students share one. Is the rule sending each student to their ID number one-to-one? Yes — distinct students always receive distinct numbers, which is precisely the defining condition. The habit worth keeping: one-to-one is a question about the matching itself, not about algebra.
- **visual_need:** 學生 → ID 號碼的對應圖（數名學生各連到不同號碼，連線互不匯聚）。
- **animation_cue:** —（靜態即可）

### 5. checking_with_algebra
- **source:** chapter1-print-standalone.html §1.1 · Example 1.2 + Solution + 例後 prose（“illustrates why not every function can be reversed”）
- **learning_goal:** 會用定義對具體函數做正式驗證，並看到 not one-to-one 直接堵死「回推」。
- **kind:** `example`
- **narration:**
  > Now back to the two functions from the opening, this time as a formal check. On $[0,1]$, the function $f(x)=x$ sends every input to itself, so distinct inputs automatically give distinct outputs — one-to-one. For $g(x)=x^2$ on $[-1,1]$, compute both values: $g(\tfrac12)=\tfrac14$, and $g(-\tfrac12)=\tfrac14$ as well. Two different inputs share one output, so $g$ is not one-to-one. And the consequence matters: no rule can send $\tfrac14$ back to a single input, so $g$ cannot be reversed on this interval.
- **visual_need:** 兩欄並排：左 $f(x)=x$ 一行論證；右 $g(x)=x^2$ 的兩行計算（$g(\tfrac12)=\tfrac14$、$g(-\tfrac12)=\tfrac14$）與結論。
- **animation_cue:** —（靜態即可；動態重點留給下一單元的水平線測試）

### 6. horizontal_line_test
- **source:** chapter1-print-standalone.html §1.1 · Remark 1.1（env-name: Horizontal line test）+ Figure 1.1（data-fig: hlt）
- **learning_goal:** 會用水平線測試從圖形直接判讀一對一，並理解它為何成立。
- **kind:** `proposition`
- **narration:**
  > There is a way to read one-to-one straight off the graph. A horizontal line $y=c$ crosses the graph of $f$ wherever $f(x)=c$, so every crossing is one input that produces the output $c$. That gives the test: a function is one-to-one exactly when no horizontal line meets its graph more than once. Two crossings on one line would mean two inputs with the same output — exactly the failure we saw with $x^2$. So sweep horizontal lines down the graph and count: at most one crossing at every height is what passing looks like.
- **visual_need:** 兩圖並排（一個單調遞增函數 vs parabola），各配一條水平線與交點標記；通過／不通過對比。
- **animation_cue:** 同一條水平線在兩圖同步由上往下 sweep：左圖任何高度都只有一個交點（短暫綠色強調）；右圖掃到某高度出現兩個交點（紅色強調），sweep 在該高度停住，兩交點各拉虛線落回 x 軸，標出兩個不同輸入。
- **備註（§3 邊角）：** 具名規則與其演示圖為同一教學重點，合一單元。

### 7. inverse_definition
- **source:** chapter1-print-standalone.html §1.1 · Definition 1.2 + 其前一句鋪陳 prose（“a second function that undoes $f$”）
- **learning_goal:** 掌握反函數的定義：定義關係 $f^{-1}(y)=x \iff f(x)=y$，以及 domain／range 互換。
- **kind:** `definition`
- **narration:**
  > For a one-to-one function, every output traces back to exactly one input — so the backwards assignment is itself a function. We call it the inverse of $f$, written $f^{-1}$. If $f$ has domain $A$ and range $B$, then $f^{-1}$ has domain $B$ and range $A$, and its rule is the defining relation: $f^{-1}(y) = x$ exactly when $f(x) = y$. Note the trade: the outputs of $f$ become the inputs of $f^{-1}$, and domain and range swap places.
- **visual_need:** 定義關係式 $f^{-1}(y)=x \iff f(x)=y$ + domain/range 互換的標示（$A \leftrightarrow B$）。
- **animation_cue:** —（靜態即可；往返動態留給 composition_identities 單元）

### 8. reading_the_notation
- **source:** chapter1-print-standalone.html §1.1 · Remark 1.2（變數改名）
- **learning_goal:** 看懂 $f^{-1}(x)=y \iff f(y)=x$ 的變數改名，為之後 procedure 的「互換 $x$、$y$」鋪路。
- **kind:** `definition`
- **narration:**
  > One notational habit before we continue. We usually prefer $x$ as the input letter of whatever function we are currently studying — including $f^{-1}$ itself. After renaming the variables, the defining relation reads: $f^{-1}(x) = y$ exactly when $f(y) = x$. Same statement, new letters — and this renaming is the reason the procedure at the end of this section will ask us to interchange $x$ and $y$.
- **visual_need:** 兩條 iff 式上下對照（$y$-form 與改名後的 $x$-form），對應變數以顏色呼應。
- **animation_cue:** —（靜態即可）
- **備註（偏離註記）：** Remark 1.2 僅 2 句，照 §3 預設應併入鄰段；此處 promote 成獨立單元，理由：變數互換是學生高頻混淆點，且 Strategy 1.1 第 3 步的根據在此——值得單獨停留一拍。

### 9. inverse_iff_one_to_one
- **source:** chapter1-print-standalone.html §1.1 · Theorem 1.1
- **learning_goal:** 記住可逆性的完整刻畫：有反函數 ⟺ 一對一。
- **kind:** `theorem`
- **narration:**
  > We introduced one-to-one as the property that makes reversing possible; the theorem pins that down. A function has an inverse if and only if it is one-to-one. There are no hidden conditions: the property we can already check — by the definition or by horizontal lines — is the complete story of invertibility. Let us walk through why both directions hold.
- **visual_need:** 定理陳述卡（iff 雙向箭頭視覺化：has inverse ⟺ one-to-one）。
- **animation_cue:** —（靜態即可）
- **備註（§3 拆分）：** 證明兩方向合計超過 ~4 步，依 §3 拆成 statement 單元＋proof 單元。

### 10. proof_both_directions
- **source:** chapter1-print-standalone.html §1.1 · Proof（Theorem 1.1）
- **learning_goal:** 走通兩個方向：有反函數 ⇒ 一對一（兩邊作用 $f^{-1}$）；一對一 ⇒ 可構造反函數（唯一原像）。
- **kind:** `proof`
- **narration:**
  > First, suppose $f$ has an inverse. If $f(x_1) = f(x_2)$, apply $f^{-1}$ to both sides — $f^{-1}(f(x_1)) = f^{-1}(f(x_2))$ — and by the defining relation each side collapses back to its input, so $x_1 = x_2$. Equal outputs force equal inputs: $f$ is one-to-one. Now the converse. Let $f$ be one-to-one with domain $A$ and range $B$. Every $y$ in $B$ is hit by at least one $x$ in $A$ — that is what being the range means — and one-to-one guarantees at most one. Exactly one input for each output: sending each $y$ to that unique $x$ is a well-defined function from $B$ to $A$, and it is precisely the inverse of $f$.
- **visual_need:** 兩半並列或依序：⇒ 方向的兩行推導（$f(x_1)=f(x_2) \Rightarrow f^{-1}(f(x_1))=f^{-1}(f(x_2)) \Rightarrow x_1=x_2$）；⇐ 方向的構造句（each $y \mapsto$ its unique $x$）。
- **animation_cue:** —（靜態逐步揭示即可）

### 11. first_inverses
- **source:** chapter1-print-standalone.html §1.1 · Example 1.4 + Solution（`prompt-list`／`sol-list` 兩小題）
- **learning_goal:** 算出第一批具體反函數（$f(x)=x$ 自反；$g(x)=x^3 \to \sqrt[3]{x}$），並第一次見到「compose 驗證」。
- **kind:** `example`
- **narration:**
  > Time to find actual inverses, starting small. The identity function $f(x)=x$ leaves every input untouched, so reversing it changes nothing either: $f$ is its own inverse, $f^{-1}(x) = x$. Next, $g(x)=x^3$. Write $y = x^3$ and solve for the input: $x = \sqrt[3]{y}$, so after renaming the variable, $g^{-1}(x) = \sqrt[3]{x}$. And the answer checks out: $g(g^{-1}(x)) = (\sqrt[3]{x})^3 = x$ — feeding the inverse's output back into $g$ returns exactly where we started.
- **visual_need:** 兩小題並排：(a) $f^{-1}(x)=x$ 一行；(b) $y=x^3 \to x=\sqrt[3]{y} \to g^{-1}(x)=\sqrt[3]{x}$ 加 check 式。
- **animation_cue:** —（靜態逐步揭示即可）

### 12. composition_identities
- **source:** chapter1-print-standalone.html §1.1 · Proposition 1.1 + 其前 bridge prose（“The defining relation … yields two composition identities”）+ Figure 1.2（inline SVG：$A \leftrightarrow B$ 往返）
- **learning_goal:** 掌握兩條 composition identities，理解「互相抵銷」是反函數的代數本質、也是驗證工具。
- **kind:** `proposition`
- **narration:**
  > That final check was not a coincidence — it is a law that every inverse obeys. Because $f^{-1}(y) = x$ means exactly the same thing as $f(x) = y$, going forward and then backwards always lands you where you started: $f^{-1}(f(x)) = x$ for every $x$ in $A$, and in the other direction, $f(f^{-1}(y)) = y$ for every $y$ in $B$. In words: $f$ and $f^{-1}$ undo each other, in both orders. These two identities are also the practical test — to certify that a claimed inverse is correct, compose the two and watch everything cancel.
- **visual_need:** $A$、$B$ 兩集合與往返箭頭（$f$ 上弧、$f^{-1}$ 下弧；重繪講義 Figure 1.2 的數學內容）+ 兩條恆等式。
- **animation_cue:** 點 $x$ 沿上弧（$f$）走到 $B$ 中的 $f(x)$，再沿下弧（$f^{-1}$）走回原處、原點閃一下示意「回到自己」；第二趟由 $B$ 中的 $y$ 出發反向走一輪，對應第二條恆等式。
- **備註（§3 邊角）：** 命題與其演示圖（Figure 1.2）為同一教學重點，合一單元。

### 13. graphs_mirror_across_y_x
- **source:** chapter1-print-standalone.html §1.1 · Figure 1.2 後的 prose 幾何主張（“reflections of one another across the line $y=x$；$(a,b)$ ↔ $(b,a)$”）
- **learning_goal:** 理解「$(a,b)$ 在 $f$ 上 ⟺ $(b,a)$ 在 $f^{-1}$ 上」如何給出兩圖對 $y=x$ 鏡射。
- **kind:** `visual`
- **narration:**
  > The algebra of inverses leaves a picture behind. If the point $(a,b)$ lies on the graph of $f$, then $f(a) = b$, which is the same as $f^{-1}(b) = a$ — so the point $(b,a)$ lies on the graph of $f^{-1}$. Swapping the two coordinates of a point is exactly a reflection across the line $y = x$. So the two graphs are mirror images: take $g(x) = x^3$ and its inverse $\sqrt[3]{x}$, fold the plane along $y = x$, and each curve lands precisely on the other.
- **visual_need:** 同一座標系：$y=x^3$、$y=\sqrt[3]{x}$、虛線 $y=x$；一組對應點 $(a,b)$ 與 $(b,a)$ 標示。
- **animation_cue:** 先畫 $y=x^3$ 與虛線 $y=x$；曲線沿 $y=x$「翻摺」生成 $\sqrt[3]{x}$；接著一組具體點對（如 $(a,b) \to (b,a)$）以連接線跨過鏡線對應閃示；收在兩曲線＋鏡線並存的全圖。
- **備註（§5）：** 講義此處為散文一般主張、無書圖；依 §5 用具體函數（$x^3$／$\sqrt[3]{x}$，呼應 first_inverses 單元）示範——增補呈現、不增刪內容。

### 14. repair_by_restricting
- **source:** chapter1-print-standalone.html §1.1 · Example 1.5 + Solution + Figure 1.3（data-fig: restrict-x2）
- **learning_goal:** 看見「限定定義域」如何把不可逆的 $x^2$ 修成一對一、得到 $f^{-1}(x)=\sqrt{x}$，並認出「先限定、再求逆」就是反三角函數的關鍵手法。
- **kind:** `example`
- **narration:**
  > Remember $x^2$ — the very first function that failed us, because $\tfrac12$ and $-\tfrac12$ both land on $\tfrac14$. We can repair it. Restrict the domain to $[0,\infty)$, keeping only the non-negative inputs, and the collision is gone: if $x_1^2 = x_2^2$ with $x_1, x_2 \ge 0$, then $x_1 = x_2$. The restricted function is one-to-one, so now it has an inverse. Solving $x = (f^{-1}(x))^2$ and keeping the non-negative root gives $f^{-1}(x) = \sqrt{x}$ — which is exactly why the square-root symbol means the *positive* root: it is defined to undo the restricted squaring function. And the move we just made — restrict first, then invert — is exactly what makes the inverse trigonometric functions possible, since sine and cosine are not one-to-one on their own either.
- **visual_need:** 同一座標系：限定在 $[0,\infty)$ 的拋物線 $y=x^2$、其反函數 $y=\sqrt{x}$、虛線鏡線 $y=x$；標一組對應點 $(2,4)\leftrightarrow(4,2)$，凸顯兩曲線對 $y=x$ 互為鏡射。（重繪講義 Figure 1.3 的數學內容。）
- **animation_cue:** 先畫完整拋物線 $y=x^2$（淡）；左半 $x<0$ 轉灰退場、只留 $[0,\infty)$ 右半實色——演出「砍掉一半定義域以消除重複輸出」；限定後的曲線沿虛線 $y=x$ 翻摺生成 $\sqrt{x}$；對應點 $(2,4)\to(4,2)$ 跨鏡線閃示對應。
- **備註（§3 placement／§5／§2）：** 書序在 reflection prose 後、Strategy 前，置於 u13 與 u15 之間；回收開場 $x^2$ 反例（callback）。單一前向概念橋接（→反三角）摺進 takeaway，不獨立成 `forward_ref`、不報節號。為**代表式涵蓋**（§2，2026-06-13）新增：帶來「域限定修復可逆性」新教學點＋新圖，非同型 drill。

### 15. the_procedure
- **source:** chapter1-print-standalone.html §1.1 · Strategy 1.1（env-name: Finding the inverse of a one-to-one function；`ol.steps` 三步）
- **learning_goal:** 把找反函數定型成三步 procedure，並知道工作量集中在「解 $x$」。
- **kind:** `procedure`
- **narration:**
  > The cube-root computations secretly followed a recipe, and it works for any one-to-one function. Step one: write $y = f(x)$. Step two: solve this equation for $x$ in terms of $y$. Step three: interchange the names $x$ and $y$ — the result reads $y = f^{-1}(x)$. All the real work lives in step two; the final swap is just the variable-naming habit we set up earlier.
- **visual_need:** 三步驟卡（祈使句），step 2 視覺強調為核心步。
- **animation_cue:** —（靜態逐步揭示即可）

### 16. procedure_in_action
- **source:** chapter1-print-standalone.html §1.1 · Example 1.6 + Solution（$f(x)=x^3+2$）
- **learning_goal:** 完整跑一遍 procedure（解 $x$ 兩步、互換、compose 驗證）。
- **kind:** `example`
- **narration:**
  > Same recipe, one notch up: $f(x) = x^3 + 2$. From $y = x^3 + 2$, isolate the input — $x^3 = y - 2$, then $x = \sqrt[3]{y - 2}$. Interchange the names, and the inverse appears: $f^{-1}(x) = \sqrt[3]{x - 2}$. Finally the certificate: $f(f^{-1}(x)) = (\sqrt[3]{x-2})^3 + 2 = (x-2) + 2 = x$. Everything cancels back to $x$, so this really is the inverse.
- **visual_need:** 解方程的對齊推導（$x^3 = y-2 \to x = \sqrt[3]{y-2}$）+ 互換結果 + check 式一行收斂到 $x$。
- **animation_cue:** —（靜態逐步揭示即可）
- **備註（§4 repeat-pattern）：** 同型第二例，跳過 first_inverses 已建立的 setup，一句轉場直接進演算。

### 17. temperature_conversion
- **source:** chapter1-print-standalone.html §1.1 · Example 1.8 + Solution（攝氏↔華氏）
- **learning_goal:** 看見反函數回答一個真實問題（華氏→攝氏），並把三步 procedure 套在線性應用函數上、確認 $f^{-1}$ 的「意義」而不只是公式。
- **kind:** `example`
- **narration:**
  > One last inverse, and this one means something outside the page. The function $f(t) = \tfrac{9}{5}t + 32$ takes a Celsius temperature and returns the Fahrenheit reading. So what does its inverse do? It runs the conversion backwards — hand it a Fahrenheit number and it gives you the Celsius. The recipe is unchanged: solve $t = \tfrac{9}{5}f^{-1}(t) + 32$ for the inverse, which gives $f^{-1}(t) = \tfrac{5}{9}(t - 32)$. And the check is reassuring — go to Fahrenheit and back, $f^{-1}(f(t)) = \tfrac{5}{9}\bigl(\tfrac{9}{5}t + 32 - 32\bigr) = t$, landing exactly where we began. Here an inverse is not an abstraction; it is the formula on the other side of the thermometer.
- **visual_need:** example_walkthrough 風格：題目一句（$f(t)=\tfrac95 t+32$，C→F，問 $f^{-1}$ 意義）；求解兩步（$t=\tfrac95 f^{-1}(t)+32 \to f^{-1}(t)=\tfrac59(t-32)$）；check 式一行收斂到 $t$；takeaway「$f^{-1}$＝把溫度計反過來讀（F→C）」。
- **animation_cue:** —（靜態逐步揭示即可；可選 $0^\circ\text{C}=32^\circ\text{F}$、$100^\circ\text{C}=212^\circ\text{F}$ 雙溫標對照小圖，非必要）
- **備註（§4 repeat-pattern／§2）：** 同走三步 procedure，但 narration 以「The recipe is unchanged」一句轉場、不重述 setup（§4）。為**代表式涵蓋**新增：帶來「真實世界應用＋詮釋 $f^{-1}$ 意義」新 flavor，非冗餘代數 drill；置於 u16 procedure_in_action 後、recap 前作收束。

### 18. recap
- **source:** §1.1 整節（recap 為增補單元）
- **learning_goal:** 四句帶走整節：定義＋測試、存在性定理、composition identities＋鏡射、procedure。
- **kind:** `recap`
- **narration:**
  > Here is the whole section in four moves. A function is one-to-one when different inputs never share an output — and on a graph, horizontal lines detect exactly that. A function has an inverse precisely when it is one-to-one, with domain and range trading places. The inverse undoes the original — $f^{-1}(f(x)) = x$ and $f(f^{-1}(y)) = y$ — and graphically the two curves mirror across $y = x$. And to compute one: write $y = f(x)$, solve for $x$, then swap the names.
- **visual_need:** 四張 takeaway 卡：① one-to-one ＋水平線測試；② 存在性（iff）＋ domain/range 互換；③ 兩條恆等式＋鏡射；④ 三步 procedure。
- **animation_cue:** —（用 gen-2 既有 recap_cards 模板）

### 19. outro
- **source:** —（品牌收尾）
- **learning_goal:** —
- **kind:** `outro`
- **narration:** —（outro 無旁白）
- **visual_need:** 暗轉亮橋接 → 最終 logo 字卡（`meta.section` + `meta.title` 預設即可，無 end_slate 覆寫）。
- **animation_cue:** —（用 gen-2 既有 outro 模板）

---

## 內容層檢核（§7）自查記錄

- 環境覆蓋：Definition 1.1（u3）、Example 1.1（u4）、Example 1.2（u5）、Remark 1.1＋Figure 1.1（u6）、Definition 1.2（u7）、Remark 1.2（u8）、Theorem 1.1（u9）、Proof（u10）、Example 1.4（u11）、Proposition 1.1＋Figure 1.2（u12）、reflection prose（u13）、Example 1.5＋Figure 1.3（u14）、Strategy 1.1（u15）、Example 1.6（u16）、Example 1.8（u17）——**全覆蓋，無 exercise 洩入**（本節 HTML 無 `env-exercise`）。
- 注（2026-06-13 import 後）：HTML §1.1 經 commit `eb5c53e` 新增 Example 1.3（一對一判別 $h=x^3-4x$）、1.5（限定 $x^2$ 域＋新 Figure 1.3）、1.7（有理函數雙向驗證）、1.8（攝氏↔華氏），既有例題重編號——本稿 u11（$g\to\sqrt[3]{x}$）現為 **Example 1.4**、u15（$x^3+2$）現為 **Example 1.6**，source 已更新。依**代表式涵蓋**（方法論 §2，2026-06-13 拍板）：1.3／1.7 屬同型 drill（折疊、不另開單元）；1.5（帶新圖、橋接反三角）與 1.8（真實世界應用）**已採納為新單元 u14／u17**（2026-06-13 使用者拍板），narration 同日認可；1.3／1.7 仍折疊。
- 環境間 prose 歸類：opening prose＋warmup（u2 lead-in／body）；“Now we return…”（u5 lead-in）；Example 1.2 例後 prose（u5 takeaway）；“Looking at the graph…”（u6 lead-in）；“a second function that undoes…”（u7 lead-in）；“The defining relation … yields…”（u12 lead-in）；reflection prose（promote → u13，§5 具體函數示範）；“When $f$ is one-to-one … short procedure”（u14 lead-in）——**無 silently drop**。
- forward-pointing prose：本節 HTML 無向後章預告，無 `forward_ref` 單元。
- symbol-heavy 判定：幾何／對應比重高（視覺單元 u2/u4/u5/u6/u12/u13），**不**套 §5 條件化例外。
- 動畫 cue 共 4 個（u2、u6、u12、u13），自然語言、聚焦教學意圖；本輪不接入（拍板：第二輪）。
- repeat-pattern：u15 開頭一句轉場、不重述 setup。對齊鏈（u15）首行念全式、後續不重念 LHS。
