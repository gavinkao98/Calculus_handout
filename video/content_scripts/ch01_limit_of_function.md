# Section 1.3 The Limit of a Function — 內容稿（正式版）

> **性質：正式產線內容稿**。依 REBUILD_STATUS「2026-06-13 全章影片計畫」Phase 2 第一站（§1.3）。以 HTML 講義權威檔逐節拆解、撰寫；內容層已通過六-lens 稽核。2026-06-14 依「先影片後旁白」路線已先落地工程稿／mock preview／MiMo spoken Step 1–3；narration **仍待使用者正式認可**。
> **來源（權威）：** [`../../handout/chapter1-print-standalone.html`](../../handout/chapter1-print-standalone.html) §1.3（`sec-no` 1.3，The Limit of a Function）。
> **格式：** 純內容層，每單元 `id / source / learning_goal / kind / narration / visual_need / animation_cue`；**不含** template / `{show}` / accent / 視覺 payload（第二階段才填）。`narration` 為英文（旁白語言）；`visual_need` / `animation_cue` 為中文（內容溝通用）。客製動畫由 Claude 依 `animation_cue` 生成、經認可後接入工程稿 `# HOOK`（本節數值表動畫多半由 `value_table` 模板的 `reveal: cols` 原生承載）。
> **複雜度定位（REBUILD_STATUS）：** 低複雜度、~45% 符號、建議 10–14 單元；本節為「直覺低谷」，圖形／數值表為教學主體——**不**套 §5 symbol-heavy 例外。

---

## Deck meta（intro / outro 用）

```
chapter:       Chapter 1
chapter_title: Inverse Functions and Limits
section:       1.3
title:         The Limit of a Function
tagline:       What value does a function approach?
sections:      [1.1 Inverse Functions, 1.2 Inverse Trigonometric Functions,
                1.3 The Limit of a Function, 1.4 One-Sided and Infinite Limits,
                1.5 Limit Laws and Computational Techniques,
                1.6 The Precise Definition of a Limit]
```

---

## 教學單元

### 1. intro
- **source:** §1.3 整節 + 章定位（standalone `<title>`：Chapter 1 — Inverse Functions and Limits）
- **learning_goal:** —（純品牌開場）
- **kind:** `intro`
- **narration:** —（intro 無旁白）
- **visual_need:** Section Gate：章地圖聚焦 §1.3 → 標題 “The Limit of a Function” + tagline “What value does a function approach?”
- **animation_cue:** —（用 gen-2 既有 intro 模板）

### 2. ratio_of_changes
- **source:** chapter1-print-standalone.html §1.3 · opening prose（average velocity $\frac{s(t+h)-s(t)}{h}$ → instantaneous velocity；一般比值 $\frac{f(y)-f(x)}{y-x}$ as $y\to x$）
- **learning_goal:** 從「平均變化率 → 瞬時變化率」看出極限要回答的問題：當一個輸入滑向另一個（但不相等）時，比值趨近什麼。
- **kind:** `motivation`
- **narration:**
  > Calculus keeps circling back to one question: how fast is something changing right now? Suppose $s(t)$ is the position of a moving object at time $t$. Over the stretch from $t$ to $t+h$, its average velocity is the ratio $\frac{s(t+h)-s(t)}{h}$ — change in position divided by change in time. But the average speed across an interval is not the speed at a single instant. To pin down that instantaneous velocity, we let $h$ shrink toward zero and watch what the ratio settles on. The same move works for any function: the ratio $\frac{f(y)-f(x)}{y-x}$ measures how $f$ changes between two inputs, and we ask what it approaches as $y$ slides toward $x$ without ever reaching it. That question — what a quantity approaches — is the idea of a limit.
- **visual_need:** 一條曲線上兩點 $(x,f(x))$、$(y,f(y))$ 與連接它們的割線；標出 rise $f(y)-f(x)$ 與 run $y-x$、比值 $\frac{f(y)-f(x)}{y-x}$。
- **animation_cue:** 曲線上右側點 $(y,f(y))$ 沿曲線緩緩滑向左側固定點 $(x,f(x))$，割線隨之轉動、愈來愈短；滑近時頓住，凸顯「$y\to x$ 時比值趨近某個值」——**不畫到重合**（$y\ne x$，呼應極限「接近但不等於」）。
- **備註（§3／§5）：** 開場散文 promote 成 motivation 單元（先白話講清楚再形式化）。講義此處為散文鋪陳、無書圖；依 §5 用一條具體曲線把「比值隨 $y\to x$ 趨近」演成動畫——增補呈現、不增刪內容；刻意不命名 tangent（屬後章）。

### 3. the_limit_defined
- **source:** chapter1-print-standalone.html §1.3 · Definition 1.9 + 替代記法 prose（$f(x)\to L$ as $x\to a$）
- **learning_goal:** 掌握極限的（非正式）定義與兩種記法，並抓住關鍵字「$x$ 趨近 $a$ 但不等於 $a$」。
- **kind:** `definition`
- **narration:**
  > Here is the definition that captures “what a function approaches.” We say the limit of $f(x)$ as $x$ approaches $a$ equals $L$, written $\lim_{x\to a} f(x) = L$, if $f(x)$ can be made arbitrarily close to $L$ whenever $x$ is sufficiently close to $a$ but not equal to $a$. That last clause is the entire personality of a limit: we care about inputs near $a$, never about $a$ itself. The same idea has a lighter notation — $f(x)\to L$ as $x\to a$ — read “$f(x)$ tends to $L$ as $x$ tends to $a$.” Keep the picture in mind: $x$ creeping toward $a$ along the horizontal axis, while the heights $f(x)$ home in on $L$.
- **visual_need:** 定義宣告句 $\lim_{x\to a}f(x)=L$ + 一句白話（$f(x)$ 任意接近 $L$ ⟸ $x$ 足夠接近 $a$ 但 $\ne a$）+ 替代記法 $f(x)\to L$ as $x\to a$；「$\ne a$」視覺強調。
- **animation_cue:** —（靜態即可；逼近的動態留給下一單元的三圖）
- **備註（§3）：** 替代記法 prose 為 1–2 句 bridge，fold 進本定義單元 narration。

### 4. limit_vs_value
- **source:** chapter1-print-standalone.html §1.3 · prose（“concerned with values of $f(x)$ for $x$ near $a$, not $f(a)$ … $f(a)$ need not be defined”）+ Figure 1.11（data-fig: limit-same-near-a）
- **learning_goal:** 理解極限只看 $a$ 附近的值、與 $f(a)$ 無關——$f(a)$ 可以等於、不等於、或根本沒定義，極限都一樣。
- **kind:** `visual`
- **narration:**
  > Now the subtle part, and it is the heart of this section. A limit looks only at the neighborhood of $a$, never at the single point $a$ itself — so the value $f(a)$ gets no vote. Look at three functions side by side, all approaching the same height $L$ as $x\to a$. In the first, the point sits right where you expect, with $f(a) = L$. In the second, someone has lifted that one point off the curve, so $f(a)\ne L$. In the third, the point is missing entirely and $f(a)$ is undefined. Three different situations at $a$, yet the limit is the same $L$ in every case — because near $a$, and near is all that counts, the three curves are identical.
- **visual_need:** 三個並排小圖，同一條趨近 $L$ 的曲線、同一條虛線 $y=L$ 與 $x=a$ 標記；面板一實心點 $(a,L)$ 在曲線上（$f(a)=L$）；面板二曲線在 $a$ 處斷開、空心點留原位、實心點移到別處（$f(a)\ne L$）；面板三 $a$ 處只剩空心點（$f(a)$ undefined）。重繪講義 Figure 1.11。
- **animation_cue:** 三圖同步：一支標記從 $a$ 左右兩側沿 x 軸滑向 $a$，三圖對應的曲線高度都收斂到同一條 $y=L$ 虛線（短暫高亮 $L$）；強調無論 $a$ 處那一點「在線上／被移走／不存在」，逼近的高度都一樣。
- **備註（§3 邊角）：** 散文幾何主張與其演示圖（Figure 1.11）為同一教學重點，合一單元。

### 5. reading_a_graph
- **source:** chapter1-print-standalone.html §1.3 · Example 1.15 + Solution + Figure 1.12（data-fig: read-limit-graph）
- **learning_goal:** 會從圖形兩側讀出極限，並親眼確認 $x=2$ 處極限（$2$）與函數值 $f(2)=-2$ 可以不同。
- **kind:** `example`
- **narration:**
  > Let us read limits straight off a graph. Three inputs to inspect: $x=-2$, $x=0$, and $x=2$. As $x$ approaches $-2$ from either side, the curve rises toward height $1$, so the limit there is $1$. Approaching $0$, the curve heads to height $0$ — the limit is zero. Now $x=2$ is the interesting one: from both sides the curve climbs toward height $2$, and yet the graph marks a solid dot down at $(2,-2)$ and a hollow dot up at $(2,2)$. So $f(2)$ is $-2$, but the limit ignores the value at the point and reports where the curve was heading. The limit as $x\to 2$ is $2$, even though $f(2)$ equals $-2$.
- **visual_need:** 單一函數圖（重繪 Figure 1.12）：$x=-2$ 趨近高度 $1$、$x=0$ 趨近高度 $0$、$x=2$ 趨近高度 $2$；$x=2$ 處空心點 $(2,2)$＋實心點 $(2,-2)$；標 $y=f(x)$。
- **animation_cue:** 依序處理三個 $x$ 值：在 $-2$、$0$、$2$ 各放一支從兩側沿曲線滑向該處的標記，逼近高度用虛線引到 y 軸標出（$1$、$0$、$2$）；到 $x=2$ 時特別停頓——逼近虛線停在 $y=2$（空心點），同時閃示下方 $y=-2$ 的實心點，凸顯「極限看趨勢、不看那一點」。
- **備註（§3）：** 具體 worked example 緊接 limit_vs_value 之後，把抽象主張扣到一張可讀的圖上。

### 6. build_one_yourself
- **source:** chapter1-print-standalone.html §1.3 · Example 1.16 + Solution
- **learning_goal:** 反向操作——給定目標極限與函數值，自己畫出一條符合的曲線，鞏固「極限與函數值各自獨立」。
- **kind:** `example`
- **narration:**
  > The same idea, now run backwards: instead of reading a graph, we build one. The task is a function with limit $10$ as $x\to 3$, but with $f(3) = 0$. Start with any curve that approaches height $10$ at $x=3$ — a straight line through $(3,10)$ will do. Then take that single point and drag it down to height $0$: a hollow dot at $(3,10)$ to mark where the curve is heading, and a solid dot at $(3,0)$ for the actual value. Near $x=3$ the curve still approaches $10$, while the relocated point sets $f(3) = 0$. Because the limit and the value are independent, nothing stops us from choosing them separately.
- **visual_need:** 一條過 $(3,10)$ 的直線（趨近高度 $10$）；$x=3$ 處空心點 $(3,10)$＋實心點 $(3,0)$；標 $\lim_{x\to3}f(x)=10$、$f(3)=0$。
- **animation_cue:** 先畫過 $(3,10)$ 的直線（在 $x=3$ 留空心點）；接著把該點「抓下來」——一個點從 $(3,10)$ 垂直下移到 $(3,0)$ 變實心、原位留空心點；兩條虛線分別引到 $y=10$（limit）與 $y=0$（value），並列標示兩者互不相干。
- **備註（§2）：** 與 reading_a_graph 同談「極限 vs 函數值」，但屬**反向技能**（由條件構造圖，非讀圖）——帶來新認知動作，非同型 drill，獨立成單元。

### 7. estimate_from_a_table
- **source:** chapter1-print-standalone.html §1.3 · Example 1.17 + Solution（數值表 $\lim_{x\to1}\frac{x-1}{x^2-1}$）
- **learning_goal:** 在看不出答案時，用「在 $a$ 附近取值列表」估計極限；讀出 $\frac{x-1}{x^2-1}\to\tfrac12$。
- **kind:** `example`
- **narration:**
  > What if there is no graph to read? Then we make our own data. Take $\lim_{x\to 1}\frac{x-1}{x^2-1}$. Substituting $x=1$ gives zero over zero — undefined, no answer there. So instead we sample inputs creeping toward $1$ from both sides: $0.9$, $0.99$, $0.999$, and then $1.001$, $1.01$, $1.1$. Evaluate the expression at each, and the outputs march steadily toward one number — $0.5263$, $0.5025$, $0.5003$ from the left, and $0.4762$, $0.4975$, $0.4998$ closing in from the right. They are squeezing in on one half, so we read the limit as $\tfrac12$.
- **visual_need:** value_table（§1.3 數值逼近型）：表頭 $x$ ＝ 0.9, 0.99, 0.999, 1.001, 1.01, 1.1；列 $\frac{x-1}{x^2-1}$ ＝ 0.5263, 0.5025, 0.5003, 0.4998, 0.4975, 0.4762；結論列 $\lim_{x\to1}\frac{x-1}{x^2-1}=\tfrac12$。
- **animation_cue:** 表格欄位由兩端向中間逐欄揭示（最外側 0.9／1.1 先亮，往 $x=1$ 收）；每揭一欄，函數值同步亮出，數字逐步逼近 $\tfrac12$；揭完高亮「趨近值 $\tfrac12$」。
- **備註（§2／工程）：** 數值表為本節招牌新技巧；對應 `value_table` 模板的 `reveal: cols`（§1.3 節奏，REBUILD_STATUS 已備）——逐欄揭示動畫由模板原生承載，不另寫 hook。

### 8. when_algebra_is_hard
- **source:** chapter1-print-standalone.html §1.3 · Example 1.18 + Solution（數值表 $\lim_{t\to0}\frac{\sqrt{t^2+9}-3}{t^2}$）
- **learning_goal:** 看見數值法在「代數一眼看不穿」時不可或缺；讀出 $\to\tfrac16$。
- **kind:** `example`
- **narration:**
  > One more, where the table really earns its keep. Consider $\lim_{t\to 0}\frac{\sqrt{t^2+9}-3}{t^2}$. This time you cannot just factor your way to the answer — the square root hides what is going on, and at $t=0$ it is once again zero over zero. So we let the numbers talk. Sampling $t = -0.1$, $-0.01$, $0.01$, and $0.1$, the expression returns about $0.16662$, then $0.166666$, and back out symmetrically. That is closing in on $0.16666\ldots$, which we recognize as $\tfrac16$. When the algebra is not obvious, a table of nearby values is a perfectly good way to see where a function is headed.
- **visual_need:** value_table（同型）：表頭 $t$ ＝ −0.1, −0.01, 0.01, 0.1；列 $\frac{\sqrt{t^2+9}-3}{t^2}$ ＝ 0.166620, 0.166666, 0.166666, 0.166620；結論列 $\lim_{t\to0}=\tfrac16$。
- **animation_cue:** 同 estimate_from_a_table 的逐欄揭示（兩端向 $t=0$ 收），函數值對稱逼近 $0.16666\ldots$；揭完高亮 $\tfrac16$。
- **備註（§4 repeat-pattern／§2）：** 同型第二個數值表例題，以「One more」一句轉場、**不重述列表法 setup**（§4）。**保留理由（代表式涵蓋 §2）：** 1.17 是可因式分解的有理式（學生能用代數驗證答案），1.18 的根式無從速解、$0/0$ 形式真正不透明——凸顯數值法在代數失效時的**不可或缺**，帶來新教學點（method is essential，非僅 convenient），非冗餘 drill。

### 9. what_comes_next
- **source:** chapter1-print-standalone.html §1.3 · 收尾 prose（“guessed by looking at function values … develop systematic methods … one-sided limits and infinite limits”）
- **learning_goal:** 知道「猜值」只是起點，接下來會學系統化的求極限方法，以及單側／無窮極限等更細緻的行為。
- **kind:** `forward_ref`
- **narration:**
  > Notice what we have been doing: guessing limits by peeking at nearby values, whether off a graph or out of a table. Guessing is a fine start, but it is not a proof, and tables can occasionally mislead. So next we build systematic methods — rules that compute limits exactly, with no sampling at all. And we sharpen the idea itself: what happens when a function approaches different values from the left and from the right, or grows without bound near a point. The estimate you can make today becomes a calculation you can trust.
- **visual_need:** 簡短文字卡：from guessing → to computing；列出即將到來的主題（systematic methods、one-sided limits、infinite limits），**不報節號**。
- **animation_cue:** —（靜態即可）
- **備註（§3）：** forward-pointing prose 永遠獨立成單元，置於本節主內容與 recap **之間**；MUST NOT 報節號（“next”、“later” 取代）。

### 10. recap
- **source:** §1.3 整節（recap 為增補單元）
- **learning_goal:** 四句帶走整節：極限＝趨近值、與 $f(a)$ 無關、可從圖讀、可用數值表估。
- **kind:** `recap`
- **narration:**
  > Here is the whole section in four ideas. A limit asks what value $f(x)$ approaches as $x$ heads toward $a$ — written $\lim_{x\to a}f(x)=L$. It depends only on the behavior near $a$, never on $f(a)$ itself, which may not even be defined. You can read a limit off a graph by following the curve inward from both sides. And when there is no graph, a table of values at inputs creeping toward $a$ will reveal the number the function is approaching.
- **visual_need:** 四張 takeaway 卡：① 極限＝趨近值 $\lim_{x\to a}f(x)=L$；② 只看 $a$ 附近、與 $f(a)$ 無關（可 undefined）；③ 從圖兩側讀；④ 數值表估計。
- **animation_cue:** —（用 gen-2 既有 recap_cards 模板）

### 11. outro
- **source:** —（品牌收尾）
- **learning_goal:** —
- **kind:** `outro`
- **narration:** —（outro 無旁白）
- **visual_need:** 暗轉亮橋接 → 最終 logo 字卡（`meta.section` + `meta.title` 預設即可，無 end_slate 覆寫）。
- **animation_cue:** —（用 gen-2 既有 outro 模板）

---

## 內容層檢核（§7）自查記錄

- **環境覆蓋：** Definition 1.9（u3）、Figure 1.11（u4）、Example 1.15＋Figure 1.12（u5）、Example 1.16（u6）、Example 1.17（u7）、Example 1.18（u8）——**全覆蓋**。本節 HTML **無** theorem／proposition／corollary／strategy／remark／caution／env-exercise（grep 核實），故無對應單元、**無 exercise 洩入**。
- **例題代表式涵蓋（§2）：** 四個 example 分屬四種不同模式——讀圖（1.15）、反向構造（1.16）、數值表·有理式（1.17）、數值表·根式（1.18）。1.17／1.18 雖同為「數值表」，但 1.18 帶來「代數失效時數值法不可或缺」的新教學點，故保留為 repeat-pattern 第二例（u8，省 setup），非同型冗餘 drill。**無 silently drop。**
- **環境間 prose 歸類：** opening prose（promote → motivation u2）；替代記法 prose（fold → u3）；“concerned with values near $a$…”（u4 body，與 Figure 1.11 合一）；收尾 prose（promote → forward_ref u9）——**無 silently drop**。
- **forward-pointing：** 收尾 prose → u9，以「next／later」轉述，**未報任何節號**（§4 禁則）。
- **symbol-heavy 判定：** 低複雜度、圖形／數值表為教學主體（視覺單元 u2/u4/u5/u6/u7/u8），符號比重遠低於 70%——**不**套 §5 條件化例外。
- **動畫 cue 共 5 個**（u2 割線滑近、u4 三圖同步逼近、u5 讀圖＋$x=2$ punchline、u7／u8 數值表逐欄揭示），自然語言、聚焦教學意圖。u7／u8 由 `value_table` 模板 `reveal: cols` 原生承載；u2／u4/u5 為客製 hook 候選（第二輪生成、認可後接入）。
- **narration 自查：** 各段 3–7 句、開頭 hook、結尾 takeaway；未念螢幕標題／條列／節號；未用「see／as shown／below」；u8 以「One more」轉場、不重述 setup（§4 repeat-pattern）；數值直讀順口（LaTeX 直讀已驗證）。
- **每個 `id` 唯一、snake_case、描述教學重點。**

### 稽核紀錄（2026-06-14，認可前對抗式稽核）

本稿由前一個 session 撰寫但**未經對抗式稽核**（與 §1.2 stage-1 不同——§1.2 有六-lens 稽核紀錄，本稿原本沒有）。為帶到同等的「可認可」狀態，撰稿後補跑一輪**六-lens 對抗式稽核**（faithfulness／decomposition／register／no-repeat／math-accuracy／completeness，Workflow `w2ammaffw`），每條 actionable finding 再經獨立對抗式驗證（比照 §1.2／`review_pack.py` 紀律，預設嘗試 refute、過濾過度 triage）：

- **結果：0 條 confirmed actionable finding。** 五個 lens（faithfulness／decomposition／register／no-repeat／math-accuracy）全 PASS、零 L1/L2；completeness lens 的 agent 未回結構化輸出，其獨有檢查改由人工直接核實（見下）＋與其他 lens 重疊覆蓋。
- **math-accuracy：0 錯**——兩張數值表獨立重算（`python`）與講義／本稿逐位一致：Ex 1.17 `(x-1)/(x^2-1)=1/(x+1)` → `0.5263, 0.5025, 0.5003, 0.4998, 0.4975, 0.4762`、limit $\tfrac12$；Ex 1.18 `(\sqrt{t^2+9}-3)/t^2` → `0.166620, 0.166666, 0.166666, 0.166620`、limit $\tfrac16=0.16666\ldots$。u5 讀圖（limits $1,0,2$；$f(2)=-2$、空心 $(2,2)$／實心 $(2,-2)$）、u6 構造（$(3,10)$／$(3,0)$）、u2 比值式、u3 定義式皆與講義 Example 1.15／1.16 逐項一致。
- **faithfulness／decomposition：無 L1/L2**——9 教學單元全可回溯 §1.3 環境（u2→opening prose、u3→Def 1.9＋替代記法、u4→“values near $a$” prose＋Fig 1.11、u5→Ex 1.15＋Fig 1.12、u6→Ex 1.16、u7→Ex 1.17、u8→Ex 1.18、u9→收尾 prose）；環境間 prose 全數歸類無 silent drop；1.17／1.18 雙數值表以「代數失效時數值法不可或缺」的 §2 理由各自保留（u8 「One more」省 setup），非冗餘 drill。
- **register：無 L1/L2**——各段為口語英文、3–7 句（recap 5）、hook→body→takeaway；無 §4 禁則（無念標題／念條列／報節號圖號／“see”/“as shown”／“In this scene”）；節號圖號僅出現在非旁白的 `source`／`visual_need`／備註欄。
- **no-repeat：clean**——u4／u5／u6（「極限與 $f(a)$ 無關」）三種不同認知動作（abstract 三圖宣告／讀圖／反向構造），u7／u8 spiral 正確（u8 省 setup＋新教學點）；recap 為逐項提醒非重教。
- **completeness（人工直接核實）：** grep §1.3 源（HTML L984–1114）確認**僅** 1 Definition（1.9）＋4 Example（1.15–1.18）＋2 Figure（1.11/1.12）——**無** theorem／proposition／corollary／strategy／remark／caution／exercise，與 §7 自查的 grep 主張一致、**無 exercise 洩入**；intro（u1，tagline＋章定位）／outro（u11）齊備；forward_ref（u9）位於主內容與 recap **之間**、narration 以「next／later」轉述、**未報節號**。
- **未動（L3/L4，列供認可參考）：** u9「tables can occasionally mislead」＝忠於講義「guessing 是 provisional」的認識論註腳（L4，非杜撰數學）；recap「the whole section」為指涉性用語、非報節號（L4）；u4／u5 皆借「heart of the section」框架但處於不同深度、非同深度炒冷飯（L3 drift，非 finding）。

**結論：本稿內容層通過稽核，math 0 錯、無 L1，達 §1.2 同級認可門檻。** 旁白本體仍待使用者正式認可；工程稿與 mock preview 已依放寬閘門先行完成，後續改字成本低、可重渲 mock 免費。

---

## 待辦／工程現況

1. **使用者認可 narration**（u2–u10 共 9 段）——審核版見同名 standalone HTML（`ch01_limit_of_function_narration.html`，數學即渲染、雙擊即開）。Mode B 已把 canonical 表格值修正到 `.md`／HTML／storyboard／spoken。
2. ✅ **工程稿已完成並 commit（`cb98ebf`）：** `storyboards/ch01_limit_of_function.yml`，11 場景，`say`＝narration 原文＋`{show}`，u2/u4/u5 標 `# HOOK(第二輪)`；u4 三圖以 `graph_compare` 兩 panel＋annotation 頂著，真三圖 hook 留第二輪。
3. ✅ **守門／mock preview 已過：** lint clean、sizecheck 0-error、11/11 mock render 抽幀驗收；`output/ch01_limit_of_function.mp4` 為 480p mock preview（約 6:59，gitignored）。
4. ✅ **MiMo spoken Step 1–3 已完成：** `ch01_limit_of_function.spoken.yml` → `_mimo.yml`＋`_narration_spoken.md`，derive parity OK；Mode B round 2 剩 1 個 taste advisory（是否把 nested radical fraction 念成 numerator/denominator 顯式形式），目前依使用者裁定維持輕量慣例。
5. **下一步：** 使用者拍板旁白／taste advisory → 第二輪動畫（u2/u4/u5 hook）→ 報用量徵同意後 MiMo TTS（或其他 TTS）→ critic 複核 → 4K。
