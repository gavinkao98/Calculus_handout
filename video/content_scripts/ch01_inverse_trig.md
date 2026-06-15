# Section 1.2 Inverse Trigonometric Functions — 內容稿（正式版）

> **性質：正式產線內容稿／工程稿已先行**。依 REBUILD_STATUS「2026-06-13 全章影片計畫」啟動 §1.2（使用者 2026-06-13 指示先做本節）。以 HTML 講義權威檔逐節拆解、撰寫；content audit 已通過，storyboard／MiMo spoken／Mode B 已依「先建工程、旁白另審」先行完成。narration **仍待使用者正式認可**；MiMo TTS 尚未執行，現有 `output/ch01_inverse_trig.mp4` 約 51 秒且缺 `when_arcsin_sin_breaks`，不可視為正式預覽。
> **來源（權威）：** [`../../handout/chapter1-print-standalone.html`](../../handout/chapter1-print-standalone.html) §1.2（`sec-no` 1.2，Inverse Trigonometric Functions；編輯源 `fragments/ch01/sec-1-2.html`）。
> **deck id：** `ch01_inverse_trig`（沿 §1.1 `ch01_inverse_functions`／§1.6 `ch01_precise_limit` 命名慣例）。
> **格式：** 純內容層，每單元 `id / source / learning_goal / kind / narration / visual_need / animation_cue`；**不含** template / `{show}` / accent / 視覺 payload（第二階段才填）。`narration` 為英文（旁白語言）；`visual_need` / `animation_cue` 為中文（內容溝通用）。客製動畫由 Claude 依 `animation_cue` 生成、經認可後接入工程稿 `# HOOK`。
> **複雜度定位（REBUILD_STATUS）：** 高複雜度、~55% 符號、建議 18–22 單元；幾何（限定分支、參考三角形、鏡射）比重高——**不**套 §5 symbol-heavy 例外。**新工程缺口（lazy build，第二階段）：reference-triangle 視覺（新模板或 hook）。**

---

## Deck meta（intro / outro 用）

```
chapter:       Chapter 1
chapter_title: Inverse Functions and Limits
section:       1.2
title:         Inverse Trigonometric Functions
tagline:       If we know the ratio, which angle gives it back?
sections:      [1.1 Inverse Functions, 1.2 Inverse Trigonometric Functions,
                1.3 The Limit of a Function, 1.4 One-Sided and Infinite Limits,
                1.5 Limit Laws and Computational Techniques,
                1.6 The Precise Definition of a Limit]
```

---

## 教學單元

### 1. intro
- **source:** §1.2 整節 + 章定位（standalone `<title>`：Chapter 1 — Inverse Functions and Limits）
- **learning_goal:** —（純品牌開場）
- **kind:** `intro`
- **narration:** —（intro 無旁白）
- **visual_need:** Section Gate：章地圖聚焦 §1.2 → 標題 “Inverse Trigonometric Functions” + tagline “If we know the ratio, which angle gives it back?”
- **animation_cue:** —（用 gen-2 既有 intro 模板）

### 2. angle_from_ratio
- **source:** chapter1-print-standalone.html §1.2 · opening prose（first paragraph：ratio → angle；ramp slope → $\arctan$，triangle sides → $\arcsin$／$\arccos$）
- **learning_goal:** 理解反三角函數要解的問題——已知一個比值，回推產生它的角度——並扣在一個具體情境上。
- **kind:** `motivation`
- **narration:**
  > Picture a ramp rising at a steady slope, and suppose you know that slope exactly — it climbs one unit for every two it runs forward. A natural question follows: what angle does the ramp make with the ground? You know the ratio; you want the angle back. That is the whole job of the inverse trigonometric functions. The ordinary trig functions turn an angle into a ratio — feed in an angle, read off a sine or a tangent. The inverse functions run that backwards: hand them a ratio, and they return the angle that produced it. From the slope of a ramp we recover its inclination; from the sides of a right triangle we recover its angles. Before we can build these inverses, though, there is one obstacle to clear.
- **visual_need:** 一個斜坡或直角三角形：已知比值（rise:run，如 1:2，或對邊/斜邊）標出，未知角 $\theta$ 處標問號；旁附「forward：angle → ratio」「inverse：ratio → angle」對照。
- **animation_cue:** 斜坡升起、比值 1:2 標出後，底角 $\theta$ 處閃問號；一個箭頭由「ratio」端反向指回「angle」端，示意反向運算（輕動畫即可）。
- **備註（§3）：** opening prose 第一段 promote 成 motivation 單元（先白話講動機）。末句「one obstacle to clear」為 bridge，引入 u3。

### 3. trig_not_one_to_one
- **source:** chapter1-print-standalone.html §1.2 · opening prose（“not one-to-one … restrict the domain”）+ Figure 1.4（data-fig: sine-not-1to1）
- **learning_goal:** 看出反三角函數的核心障礙——trig 函數在全定義域上非一對一——以及通用解法「先限定、再求逆」。
- **kind:** `counterexample`
- **narration:**
  > The obstacle is that none of the trig functions is one-to-one. Look at the sine curve running across the whole number line: it rises and falls forever, so a single horizontal line slices through it again and again. Many different angles share the very same sine — and a function whose outputs each come from many inputs simply cannot be run backwards. The cure is one we have seen before for functions that fail this way: cut the domain down to a single stretch on which the function never repeats a value. On that restricted piece the function is one-to-one, so it has an inverse. We will make this one move — restrict, then invert — for each trig function in turn.
- **visual_need:** $y=\sin x$ 在 $\mathbb{R}$ 上的完整波形；一條水平線 $y=c$ 與曲線多個交點（標 3–4 個）；旁注「many angles → same sine」。（重繪講義 Figure 1.4 數學內容。）
- **animation_cue:** 一條水平線由上往下 sweep（呼應 §1.1 的水平線測試），每個高度都掃出多個交點、交點同步閃示，凸顯 sine 在 $\mathbb{R}$ 上「非一對一」。
- **備註（§3 邊角／§1.1 callback）：** 具名概念（HLT）與其演示圖合一單元。「we have seen before」為自足回扣 §1.1「restrict then invert」原則，**不報節號**（§4 禁則；每片自足、觀眾未必看過前一節）。

### 4. restrict_sine
- **source:** chapter1-print-standalone.html §1.2 · prose（restrict $\sin$ to $[-\tfrac{\pi}{2},\tfrac{\pi}{2}]$，one-to-one，range $[-1,1]$）+ Figure 1.5（data-fig: restricted-sine）
- **learning_goal:** 認得 sine 的標準限定分支 $[-\tfrac{\pi}{2},\tfrac{\pi}{2}]$，理解它在此單調、值域 $[-1,1]$，是我們真正求逆的那條 sine。
- **kind:** `motivation`
- **narration:**
  > Let us carry that out for sine. The standard branch to keep is the interval from $-\tfrac{\pi}{2}$ to $\tfrac{\pi}{2}$. On that piece the sine curve climbs steadily from $-1$ up to $1$, hitting every value in between exactly once — so it is one-to-one there, and its outputs fill the range $[-1,1]$. That restricted, well-behaved branch is the sine we will actually invert. Other intervals would serve in principle, but this one is centred on the origin and symmetric about zero, which is why it became the standard choice.
- **visual_need:** 同一 $y=\sin x$ 曲線，只保留 $[-\tfrac{\pi}{2},\tfrac{\pi}{2}]$ 的單調遞增段（實色），其餘變灰退場；標端點 $(-\tfrac{\pi}{2},-1)$、$(\tfrac{\pi}{2},1)$ 與 range $[-1,1]$。（重繪講義 Figure 1.5。）
- **animation_cue:** 承 u3——水平線 sweep 停止後，$[-\tfrac{\pi}{2},\tfrac{\pi}{2}]$ 外的曲線轉灰淡出，只留單調分支實色；該分支上任一水平線只剩一個交點（短暫綠色強調），演出「限定後恢復一對一」。
- **備註（§3）：** restricted-sine prose 為 incorporative，鋪陳即將到來的 arcsin 定義；與 u3 分拆（u3 為全節通用障礙＋原則，u4 為 sine-specific 分支），避免單一單元過載、且後續 arccos／arctan 可用「同手法、不同區間」承接而不炒冷飯。

### 5. arcsin_definition
- **source:** chapter1-print-standalone.html §1.2 · Definition 1.3（$\arcsin$）+ Caution 1.1（$\sin^{-1}$ 記號 ≠ 倒數）
- **learning_goal:** 掌握 $\arcsin$ 的定義關係與 domain／range，並避開「$\sin^{-1}x$ 不是 $1/\sin x$」的記號陷阱。
- **kind:** `definition`
- **narration:**
  > Now we can name the inverse. The inverse sine function, written $\arcsin x$, takes a number between $-1$ and $1$ and returns the angle on our restricted branch whose sine is that number. Stated precisely: $\arcsin x = y$ means exactly that $\sin y = x$ and $y$ lies in $[-\tfrac{\pi}{2}, \tfrac{\pi}{2}]$. So its domain is $[-1,1]$ — the only ratios a sine can produce — and its range is that restricted interval of angles. One warning about notation: $\arcsin x$ is often written $\sin^{-1} x$, but that superscript $-1$ does not mean a reciprocal. $\sin^{-1} x$ is an angle; $1/\sin x$ is a number. Whenever a source writes $\sin^{-1}$, read the context to see which one is meant.
- **visual_need:** 定義關係式 $\arcsin x = y \iff \sin y = x,\ -\tfrac{\pi}{2}\le y\le\tfrac{\pi}{2}$；domain $[-1,1]$、range $[-\tfrac{\pi}{2},\tfrac{\pi}{2}]$ 標示；caution 區塊：$\sin^{-1}x \ne \dfrac{1}{\sin x}$（一邊是角、一邊是數）。
- **animation_cue:** —（靜態即可）
- **備註（§3）：** Caution 1.1（2 句記號警示）依 §3 fold 進其警示對象（$\arcsin$ 定義）的 narration，以警示語氣承載；不獨立成單元。

### 6. arcsin_identities
- **source:** chapter1-print-standalone.html §1.2 · prose（“The composition identities … take the following form”）+ Proposition 1.2（Inverse sine identities）
- **learning_goal:** 掌握 $\arcsin$ 的兩條 composition identities，並注意兩者成立區間不同（外逆內全域、內逆外僅限 range）。
- **kind:** `proposition`
- **narration:**
  > Because $\arcsin$ undoes the restricted sine, the two compose back to give the input — but watch the fine print on where each holds. One way, $\sin(\arcsin x) = x$ for every $x$ in $[-1,1]$: take a ratio, find its angle, take the sine, and you are back to the ratio. The other way, $\arcsin(\sin x) = x$ — but only when $x$ already lives in the restricted range $[-\tfrac{\pi}{2}, \tfrac{\pi}{2}]$. That asymmetry between the two is not a slip of the pen, and the next case shows exactly why it is there.
- **visual_need:** 兩條恆等式上下並列，各標其成立區間（$\sin(\arcsin x)=x$ on $[-1,1]$；$\arcsin(\sin x)=x$ on $[-\tfrac{\pi}{2},\tfrac{\pi}{2}]$）；第二條的區間限制視覺強調。
- **animation_cue:** —（靜態即可；逼近反例的動態留給 u7）
- **備註（§3）：** “composition identities take the following form” 為 1 句 incorporative bridge，fold 進本命題單元 lead-in。

### 7. when_arcsin_sin_breaks
- **source:** chapter1-print-standalone.html §1.2 · Caution 1.2（$\arcsin(\sin x)=x$ 僅在 $[-\tfrac{\pi}{2},\tfrac{\pi}{2}]$；$\arcsin(\sin\pi)=0\ne\pi$）
- **learning_goal:** 透過具體反例看清「$\arcsin$ 只回它 range 內的角」，學會在 $\arcsin(\sin x)$ 中先檢查 $x$ 是否落在 range。
- **kind:** `counterexample`
- **narration:**
  > Here is what happens when the inner angle sits outside the restricted range. Take $x = \pi$. Its sine is zero, so $\arcsin(\sin \pi) = \arcsin(0)$ — and $\arcsin$ always hands back the angle in $[-\tfrac{\pi}{2}, \tfrac{\pi}{2}]$, which is $0$, not $\pi$. So $\arcsin(\sin \pi) = 0$. The reason is structural: $\arcsin$ can only ever return an angle from its own narrow range, so feed it the sine of a far-away angle and it gives back the one angle in range that shares that sine. The habit to build: before simplifying $\arcsin(\sin x)$, check whether $x$ is already in the range — if it is not, the answer is the in-range angle with the same sine, not $x$ itself.
- **visual_need:** 反例計算 $\arcsin(\sin\pi)=\arcsin(0)=0\ne\pi$；可配單位圓示意 $\pi$ 與 $0$ 同 $\sin=0$，而 $\arcsin$ 只回 $[-\tfrac{\pi}{2},\tfrac{\pi}{2}]$ 內的 $0$。
- **animation_cue:** （可選）單位圓上 $\pi$ 角的 $\sin$ 投影落在 $0$；$\arcsin$ 把它「拉回」到 $0$ 角而非 $\pi$ 角，凸顯「只回範圍內的角」。
- **備註（§3／§7）：** Caution 1.2 自帶具體反例、屬「技巧何時失效」的標準教學點（§7 邊界/反例項），故 promote 成獨立 `counterexample` 單元，不 fold。

### 8. arcsin_evaluate
- **source:** chapter1-print-standalone.html §1.2 · Example 1.9 + Solution（(a) $\arcsin(\tfrac12)$；(b) $\tan(\arcsin(\tfrac13))$）+ Figure 1.6（data-fig: arcsin-triangle）
- **learning_goal:** 會直接求 $\arcsin$ 值，並學會「參考三角形」法——把反三角值化成一個直角三角形、讀出所需比值（本節招牌手法）。
- **kind:** `example`
- **narration:**
  > Let us evaluate two expressions. First, $\arcsin(\tfrac12)$: we want the angle in $[-\tfrac{\pi}{2}, \tfrac{\pi}{2}]$ whose sine is one half. That is $\tfrac{\pi}{6}$, so $\arcsin(\tfrac12) = \tfrac{\pi}{6}$. The second is more telling: $\tan(\arcsin(\tfrac13))$. We are not asked for the angle itself, only for its tangent — so let us draw a right triangle. Call the angle $\theta$, with $\sin\theta = \tfrac13$; that puts the side opposite $\theta$ at $1$ and the hypotenuse at $3$. By the Pythagorean theorem the adjacent side is $\sqrt{9 - 1} = 2\sqrt{2}$. Now tangent is opposite over adjacent, so $\tan(\arcsin(\tfrac13)) = \tfrac{1}{2\sqrt{2}}$. That triangle move — turn the inverse trig value into a labelled right triangle, then read off whatever ratio you need — is the workhorse of this whole section.
- **visual_need:** (a) $\arcsin(\tfrac12)=\tfrac{\pi}{6}$ 一行；(b) 直角三角形：角 $\theta$，對邊 $1$、斜邊 $3$、鄰邊 $2\sqrt2$（Pythagoras）；框出 $\tan\theta=\tfrac{1}{2\sqrt2}$。（重繪講義 Figure 1.6。）
- **animation_cue:** 由 $\sin\theta=\tfrac13$ 建三角形——先標對邊 $1$、斜邊 $3$，再以 $\sqrt{9-1}=2\sqrt2$ 補上鄰邊（短暫高亮 Pythagoras 步驟），最後框出 $\tan\theta=\tfrac{1}{2\sqrt2}$。
- **備註（§2 代表式涵蓋）：** 參考三角形法在本單元首次建立，後於 u13／u14 重用（repeat-pattern 省 setup）。

### 9. arccos_definition
- **source:** chapter1-print-standalone.html §1.2 · prose（$\cos$ one-to-one on $[0,\pi]$）+ Figure 1.7（data-fig: restricted-cosine）+ Definition 1.4（$\arccos$）+ Proposition 1.3（Inverse cosine identities）
- **learning_goal:** 把同一手法套到 cosine：限定在**不同**區間 $[0,\pi]$（遞減分支）得 $\arccos$，並知道其恆等式與 $\arcsin$ 同型、只是區間移動。
- **kind:** `definition`
- **narration:**
  > Cosine needs the same repair, but on a different stretch. Cosine is not one-to-one either, and the branch we keep is the interval from $0$ to $\pi$ — where the curve runs steadily downhill from $1$ to $-1$. On that branch every value is hit once, so we can invert it. The inverse cosine, $\arccos x$, is defined by $\arccos x = y$ exactly when $\cos y = x$ and $0 \le y \le \pi$; its domain is again $[-1,1]$ and its range is $[0, \pi]$. The composition identities read just like the ones for sine: $\cos(\arccos x) = x$ on $[-1,1]$, and $\arccos(\cos x) = x$ as long as $x$ stays in $[0,\pi]$. Same idea as before — only the interval of angles has moved.
- **visual_need:** $y=\cos x$ 限定於 $[0,\pi]$ 的遞減分支（實色，其餘灰）；定義式 $\arccos x = y \iff \cos y = x,\ 0\le y\le\pi$；domain $[-1,1]$、range $[0,\pi]$；兩條恆等式（同 $\arcsin$ 形式、區間改 $[0,\pi]$）。（重繪講義 Figure 1.7。）
- **animation_cue:** —（靜態即可；限定分支的動態已於 u3／u4 對 sine 演過，此處不重複，僅靜態高亮 $[0,\pi]$ 遞減段。）
- **備註（§4 repeat-pattern／§2）：** Proposition 1.3 與 Definition 1.4 緊耦合、恆等式與 $\arcsin$ 同型，故合一單元並以「Same idea as before」轉場；限定理由僅以一句（「every value is hit once, so we can invert it」）**壓縮**帶過、不像 u3／u4 那樣展開，避免同深度炒冷飯。命題仍被覆蓋（§2）。強調 cosine 的**差異點**（遞減、$[0,\pi]$）以拉開層次。

### 10. domain_of_composition
- **source:** chapter1-print-standalone.html §1.2 · Example 1.10 + Solution（$f(x)=\arcsin(\cos x)$ → $\mathbb{R}$；$h(x)=\sin(\arccos x)$ → $[-1,1]$）
- **learning_goal:** 會用「內函數可接受什麼 + 其輸出對外函數是否合法」決定合成函數的定義域。
- **kind:** `example`
- **narration:**
  > When inverse trig functions get composed with ordinary ones, the interesting question is often the domain. Take $f(x) = \arcsin(\cos x)$. Whatever $x$ is, $\cos x$ always lands in $[-1,1]$ — and $[-1,1]$ is exactly what $\arcsin$ accepts. So every real number is allowed: the domain of $f$ is all real numbers. Now flip the order: $h(x) = \sin(\arccos x)$. Here the inner function $\arccos$ demands an input in $[-1,1]$, and its output is an angle, which $\sin$ is happy to take. So the domain of $h$ is $[-1,1]$. The rule worth keeping: the domain of a composition is set by what the inner function accepts and whether its outputs are legal for the outer one.
- **visual_need:** 兩個合成的定義域推理並排：$f(x)=\arcsin(\cos x)$（$\cos x\in[-1,1]=\arcsin$ domain → $\mathbb{R}$）；$h(x)=\sin(\arccos x)$（需 $x\in[-1,1]$ → $[-1,1]$）；底部一句通則（inner accepts + outputs legal for outer）。
- **animation_cue:** —（靜態即可）
- **備註（§2 代表式涵蓋）：** Example 1.10（expansion）帶來新模式「合成的定義域」，非同型 drill，獨立成單元。

### 11. principal_value_trap
- **source:** chapter1-print-standalone.html §1.2 · Example 1.11 + Solution（particle height $\cos t$；$\arccos$ 只回主值）
- **learning_goal:** 抓住反三角函數最關鍵的觀念——它回傳**單一主值**，不是方程的全部解。
- **kind:** `counterexample`
- **narration:**
  > One more trap, and it carries the single most important idea about these functions. An object starts moving at time $t = 10$, bobbing so that its height afterwards is $\cos t$. True or false: it is at height $1$ at the time $t = \arccos(1)$? The answer is false. The equation $\cos t = 1$ holds at infinitely many times — $t = 0$, $2\pi$, $4\pi$, and so on — but $\arccos$ does not return all of them. It returns only its single principal value in $[0, \pi]$, which is $t = 0$. And $t = 0$ is before the object is even moving. An inverse trig function hands back one angle, never the whole family of solutions. The object really is up at height $1$ — at $t = 4\pi$, $6\pi$, and the multiples of $2\pi$ that fall after it starts moving — but $\arccos(1) = 0$ is none of those.
- **visual_need:** $y=\cos t$ 波形；$y=1$ 水平線與相切時刻 $t=0,2\pi,4\pi,6\pi,\dots$ 標出；標出起動時刻 $t=10$（其前的 $t=0,2\pi$ 在起動前）；$\arccos(1)$ 只回 $t=0$（高亮，但在起動前）；**真正**達到高度 $1$ 的時刻 $t=4\pi,6\pi,\dots$（起動後的 $2\pi$ 倍數）另色標出；標「principal value（單一）≠ 實際所有解」。
- **animation_cue:** $\cos t$ 波與 $y=1$ 相切的多點（$0,2\pi,4\pi,6\pi,\dots$）依序閃；$\arccos$ 的「指針」只停在 $t=0$（標「arccos 的答案」）；接著起動時刻 $t=10$ 落下，其左的 $t=0,2\pi$ 變灰，$t=4\pi,6\pi,\dots$ 以對比色亮起（標「實際達到高度 1 的時刻」），凸顯「主值只給一個、且未必是真正的解」。
- **備註（§2／§7）：** Example 1.11（expansion）帶來新模式「主值 vs 全部解」，且屬 §7 反例項，獨立成 `counterexample` 單元。

### 12. arctan_definition
- **source:** chapter1-print-standalone.html §1.2 · prose（$\tan$ one-to-one on $(-\tfrac{\pi}{2},\tfrac{\pi}{2})$）+ Figure 1.8（data-fig: restricted-tangent）+ Definition 1.5（$\arctan$）+ Proposition 1.4（Inverse tangent identities）
- **learning_goal:** 把手法套到 tangent，並抓住它的差異點：定義域是**全體實數**（任何比值都有角）、值域是**開區間**（漸近線、永不觸及端點）。
- **kind:** `definition`
- **narration:**
  > Tangent is the third we invert, and it brings a new twist. We restrict it to the open interval from $-\tfrac{\pi}{2}$ to $\tfrac{\pi}{2}$, where it climbs without ever repeating — but unlike sine and cosine, tangent shoots off toward infinity at the ends, so it takes every real value. That flips the domain story: $\arctan x = y$ means $\tan y = x$ with $y$ strictly between $-\tfrac{\pi}{2}$ and $\tfrac{\pi}{2}$, and its domain is all real numbers — any ratio at all has an angle. Its range is the open interval $(-\tfrac{\pi}{2}, \tfrac{\pi}{2})$, which it approaches but never reaches. The identities follow the usual pattern: $\tan(\arctan x) = x$ for every real $x$, and $\arctan(\tan x) = x$ on the open restricted interval. So $\arctan$ takes the entire number line and gently squeezes it into a band less than half a turn wide.
- **visual_need:** $y=\tan x$ 限定於 $(-\tfrac{\pi}{2},\tfrac{\pi}{2})$ 的遞增分支（實色），兩側 $x=\pm\tfrac{\pi}{2}$ 漸近線以虛線標；定義式 $\arctan x=y\iff\tan y=x,\ -\tfrac{\pi}{2}<y<\tfrac{\pi}{2}$；domain $\mathbb{R}$、range 開區間 $(-\tfrac{\pi}{2},\tfrac{\pi}{2})$；標「entire number line → band < half turn」。（重繪講義 Figure 1.8。）
- **animation_cue:** —（靜態即可；分支限定動態不重複，僅靜態高亮分支與漸近線。）
- **備註（§4 repeat-pattern／§2）：** Proposition 1.4 合進定義單元（同型恆等式，「usual pattern」一句帶過、不重述）。強調 tangent 差異點（domain $\mathbb{R}$、開區間、漸近線）拉開層次。命題仍被覆蓋。

### 13. signs_from_range
- **source:** chapter1-print-standalone.html §1.2 · Example 1.12 + Solution（(a) $\sin(\arccos(-\tfrac12))$；(b) $\sec(\arctan 10)$；(c) $\tan(\arcsin(-\tfrac{2\sqrt5}{5}))$）+ Figure 1.9（data-fig: arctan10-triangle）
- **learning_goal:** 對**負輸入**的合成，學會讓反函數的 **range** 決定象限與正負——不用猜。
- **kind:** `example`
- **narration:**
  > When the inputs go negative, signs are where people slip — but the range of the inverse function settles every sign for you. Start with $\sin(\arccos(-\tfrac12))$. Since $\arccos$ always lands in $[0,\pi]$, a negative input forces the angle into the second quadrant: $\arccos(-\tfrac12) = \tfrac{2\pi}{3}$, and its sine is $\tfrac{\sqrt{3}}{2}$. The same triangle method handles $\sec(\arctan 10)$: opposite $10$, adjacent $1$, hypotenuse $\sqrt{101}$, so the secant is $\sqrt{101}$. Now the delicate one: $\tan(\arcsin(-\tfrac{2\sqrt5}{5}))$. Here $\arcsin$ of a negative number lands in the fourth quadrant, where cosine is positive — so $\cos\theta = \tfrac{1}{\sqrt5}$ and $\tan\theta = -2$. Notice we never guessed a sign: each one came straight from the range of the inverse function.
- **visual_need:** 三小題：(a) $\arccos(-\tfrac12)=\tfrac{2\pi}{3}$ 落 $[0,\pi]$ 之第二象限 → $\sin=\tfrac{\sqrt3}{2}$；(b) 直角三角形 opp $10$／adj $1$／hyp $\sqrt{101}$ → $\sec=\sqrt{101}$（重繪 Figure 1.9）；(c) $\arcsin(-\tfrac{2\sqrt5}{5})$ 落第四象限 → $\cos\theta=\tfrac{1}{\sqrt5}$、$\tan\theta=-2$；統一標注「sign ← range」。
- **animation_cue:** （可選）兩道主值弧並示：$\arccos$ 的負輸入落在 $[0,\pi]$ 上半（QII，$\sin>0$）、$\arcsin$ 的負輸入落在 $[-\tfrac{\pi}{2},0)$（QIV，$\cos>0$），用弧上角位置「點亮」正負，凸顯象限由 range 決定。
- **備註（§4 repeat-pattern／§2）：** 統一教學點＝「sign from range」（與 u8 正輸入互補的新模式）。(b) 為 u8 三角形法的重用，以一句「same triangle method」帶過、不重述 setup（§4）。

### 14. simplify_cos_arctan
- **source:** chapter1-print-standalone.html §1.2 · Example 1.13 + Solution（$\cos(\arctan x)=\tfrac{1}{\sqrt{1+x^2}}$；$1+\tan^2=\sec^2$）+ Figure 1.10（data-fig: arctan-general-triangle）
- **learning_goal:** 把參考三角形／畢氏恆等式用在**變數**輸入上，將一個合成化簡成 $x$ 的封閉式——微積分裡反覆會用到的形態。
- **kind:** `example`
- **narration:**
  > The triangle method really shines when the input is a variable instead of a number. Let us simplify $\cos(\arctan x)$ for any $x$. Set $y = \arctan x$, so $\tan y = x$ with $y$ in the open interval $(-\tfrac{\pi}{2}, \tfrac{\pi}{2})$. One route is the Pythagorean identity $1 + \tan^2 y = \sec^2 y$, which gives $\sec^2 y = 1 + x^2$; since $y$ is in that interval, cosine is positive, so $\sec y = \sqrt{1 + x^2}$ and $\cos y = \tfrac{1}{\sqrt{1+x^2}}$. The triangle says the same thing at a glance: opposite side $x$, adjacent side $1$, hypotenuse $\sqrt{1+x^2}$, and cosine is adjacent over hypotenuse. Either way, $\cos(\arctan x) = \tfrac{1}{\sqrt{1+x^2}}$ — a messy composition collapsing to one clean expression in $x$, the kind of simplification you will reach for constantly once derivatives enter the picture.
- **visual_need:** 一般直角三角形：角 $y$，對邊 $x$、鄰邊 $1$、斜邊 $\sqrt{1+x^2}$；旁附 $1+\tan^2 y=\sec^2 y\Rightarrow\sec y=\sqrt{1+x^2}$；結論框 $\cos(\arctan x)=\tfrac{1}{\sqrt{1+x^2}}$。（重繪講義 Figure 1.10。）
- **animation_cue:** —（靜態即可；三角形法動態已於 u8 建立。）
- **備註（§4 repeat-pattern／§4 末句）：** 變數版（symbolic）為新模式。忠於講義以 $1+\tan^2=\sec^2$ 為主、三角形（Fig 1.10）佐證，兩法並陳。末句指向微分為向前語意、**不報章號**（§4 禁則）。

### 15. remaining_inverses
- **source:** chapter1-print-standalone.html §1.2 · Definition 1.6（$\arccsc$）、1.7（$\arcsec$）、1.8（$\arccot$）+ 其後 domains prose（$(-\infty,-1]\cup[1,\infty)$；$\arccot$ domain $\mathbb{R}$）
- **learning_goal:** 認識其餘三個反三角函數（同手法、較少用），並用一張對照表把六個反三角函數的 domain／range 一眼看盡。
- **kind:** `definition`
- **narration:**
  > Three inverse trig functions remain — inverse cosecant, inverse secant, and inverse cotangent — and they are built in exactly the same spirit, just used less often. Each one inverts its trig function on a chosen branch. Inverse cosecant and inverse secant take inputs whose absolute value is at least $1$ — that is, $(-\infty, -1] \cup [1, \infty)$ — because cosecant and secant never produce values strictly between $-1$ and $1$. Inverse cotangent, like inverse tangent, accepts every real number. Rather than memorize six separate boxes, it is cleaner to lay all six inverse functions side by side and compare what they accept and what interval of angles they return.
- **visual_need:** 六個反三角函數的 domain／range 對照表（列：$\arcsin$／$\arccos$／$\arctan$／$\arccsc$／$\arcsec$／$\arccot$；欄：domain、principal range）。$\arccsc$／$\arcsec$ 的 domain $(-\infty,-1]\cup[1,\infty)$、$\arccot$ domain $\mathbb{R}$ 視覺強調；principal ranges 照各定義（$\arccsc$：$(0,\tfrac{\pi}{2}]\cup(\pi,\tfrac{3\pi}{2}]$；$\arcsec$：$[0,\tfrac{\pi}{2})\cup[\pi,\tfrac{3\pi}{2})$；$\arccot$：$(0,\pi)$）。
- **animation_cue:** —（靜態表格即可；逐列揭示由工程層模板承載。）
- **備註（§2／§3）：** Definition 1.6/1.7/1.8 三定義「same spirit、used less often」，合為一個 family 單元（皆被覆蓋）。range 區間冗長拗口，narration **不逐字念**（§4 禁則「逐字念條列」），交給對照表視覺；narration 只講 domain 的關鍵差異。其後 domains prose（incorporative summary）fold 進本單元。

### 16. branch_conventions
- **source:** chapter1-print-standalone.html §1.2 · Remark 1.3（$\arcsec$ 慣例）+ Remark 1.4（$\arccsc$ 慣例）+ Example 1.14 + Solution（$f(x)=\arcsin x+\arccsc x$；慣例改答案）
- **learning_goal:** 理解 principal range 是**選擇**而非定律，不同慣例會給出不同的值——以一個具體例子看見「同式不同答案」。
- **kind:** `example`
- **narration:**
  > There is a subtlety hiding in those last three definitions: the branch we pick is a choice, not a law, and different texts choose differently. This text picks the branches that make the later differentiation formulas come out simplest, but you will meet other conventions in the wild — and the choice has visible consequences. Consider $f(x) = \arcsin x + \arccsc x$. Arcsine needs $|x| \le 1$ while arccosecant needs $|x| \ge 1$, so the only inputs satisfying both are $x = 1$ and $x = -1$. At $x = 1$, both terms equal $\tfrac{\pi}{2}$, so $f(1) = \pi$. At $x = -1$, under this text's convention $\arccsc(-1) = \tfrac{3\pi}{2}$, and with $\arcsin(-1) = -\tfrac{\pi}{2}$ we again get $f(-1) = \pi$ — so $f$ is the constant $\pi$ on its two-point domain. But under a different common convention, $\arccsc(-1)$ would be $-\tfrac{\pi}{2}$, which makes $f(-1) = -\pi$ instead. Same expression, different answer — which is exactly why a text fixes its conventions explicitly, and why you should always check the one in front of you.
- **visual_need:** Example 1.14 計算：domain $=\{\pm1\}$；$f(1)=\tfrac{\pi}{2}+\tfrac{\pi}{2}=\pi$；$f(-1)=-\tfrac{\pi}{2}+\tfrac{3\pi}{2}=\pi$（本書慣例）；對照框：另一慣例 $\arccsc(-1)=-\tfrac{\pi}{2}\Rightarrow f(-1)=-\pi$；標「same expression, different convention → different answer」。
- **animation_cue:** —（靜態即可；可選單位圓對照 $\arccsc(-1)$ 兩慣例落點 $\tfrac{3\pi}{2}$ vs $-\tfrac{\pi}{2}$。）
- **備註（§3／§2）：** Remark 1.3/1.4（具實質內容的慣例說明）fold 進本單元 narration 與對照框；Example 1.14（expansion，唯一演練 $\arccsc$／$\arcsec$ 的例題、且演示「慣例改答案」）獨立成單元。「differentiation formulas simplest」為向前語意、**不報章號**（§4）。作為全節收束的精緻教學點。

### 17. recap
- **source:** §1.2 整節（recap 為增補單元）
- **learning_goal:** 四句帶走整節：先限定再求逆（三函數三區間）、主值唯一、恆等式的區間限制、參考三角形＋range 定正負。
- **kind:** `recap`
- **narration:**
  > Here is the whole section in four moves. First, a trig function is not one-to-one, so we restrict it to a single branch and invert that — sine on $[-\tfrac{\pi}{2}, \tfrac{\pi}{2}]$, cosine on $[0, \pi]$, tangent on the open interval between. Second, each inverse returns just one angle, the principal value inside its range — never the whole family of solutions. Third, the composition identities undo the functions, but $\arcsin(\sin x)$ and its cousins only give back $x$ when $x$ already sits in the restricted range. And fourth, to evaluate a composition, build a right triangle from the inverse trig value and read off the ratio you need — and let the range of the inverse fix every sign.
- **visual_need:** 四張 takeaway 卡：① restrict-then-invert（三函數三區間）；② 主值——只回一個角；③ 恆等式只在限定區間回 $x$；④ 參考三角形 ＋ range 定正負。
- **animation_cue:** —（用 gen-2 既有 `recap_cards` 模板）

### 18. outro
- **source:** —（品牌收尾）
- **learning_goal:** —
- **kind:** `outro`
- **narration:** —（outro 無旁白）
- **visual_need:** 暗轉亮橋接 → 最終 logo 字卡（`meta.section` 1.2 + `meta.title` 預設即可，無 end_slate 覆寫）。
- **animation_cue:** —（用 gen-2 既有 outro 模板）

---

## 內容層檢核（§7）自查記錄

- **環境覆蓋（grep 核實 §1.2）：6 定義、3 命題、6 例題、2 caution、2 remark、7 圖。**
  - Definition 1.3（u5）、1.4（u9）、1.5（u12）、1.6／1.7／1.8（u15，family 合一）——**全覆蓋**。
  - Proposition 1.2（u6）、1.3（u9 fold）、1.4（u12 fold）——**全覆蓋**；1.3／1.4 同型恆等式 fold 進各自定義單元（§4 repeat-pattern，避免三段平行炒冷飯；命題陳述仍在畫面）。
  - Example 1.9（u8）、1.10（u10）、1.11（u11）、1.12（u13）、1.13（u14）、1.14（u16）——**每個不同模式皆有代表單元**（§2 代表式涵蓋）：1.9＝直接值＋參考三角形；1.10＝合成定義域；1.11＝主值 vs 全解；1.12＝負輸入的 sign-from-range；1.13＝變數版化簡；1.14＝慣例改答案。無同型 drill 需折疊（六例各帶新模式）。
  - Caution 1.1（u5 fold，記號）、Caution 1.2（u7 promote，反例）——依 §3：短記號警示 fold、自帶反例的 promote。
  - Remark 1.3／1.4（u16 fold，慣例實質說明＋對照框）。
  - 圖 1.4（u3）、1.5（u4）、1.6（u8）、1.7（u9）、1.8（u12）、1.9（u13）、1.10（u14）——**全數有對應視覺單元**。
- **環境間 prose 歸類（無 silently drop）：** opening 第一段 ratio→angle（promote → u2 motivation）；“not one-to-one … restrict” + sine 段（u3 body）；restricted-sine prose（u4 incorporative）；“composition identities take the following form”（u6 lead-in，fold）；cosine $[0,\pi]$ prose（u9 incorporative）；tangent $(-\tfrac{\pi}{2},\tfrac{\pi}{2})$ prose（u12 incorporative）；Example 1.10 例後 pattern prose（u10 takeaway）；remaining-functions “same spirit” + domains prose（u15 fold）。
- **forward-pointing prose：** 本節 HTML 無向後章系統預告；u14／u16 各有一句「微分公式」向前語意，**fold 進 takeaway、不報章號**（§4），不獨立 `forward_ref`。
- **§1.1 callback：** u3「we have seen before（restrict then invert）」自足回扣、不報節號——兌現 §1.1 u14 對反三角的鋪陳，但每片自足（觀眾未必看過 §1.1）。
- **symbol-heavy 判定：** 幾何（限定分支圖 ×3、參考三角形 ×3、單位圓主值、鏡射/象限）比重高，~55% 符號 → **不**套 §5 條件化例外；視覺單元充足（u2/u3/u4/u7/u8/u9/u11/u12/u13/u14/u15）。
- **動畫 cue：** u2（ratio→angle 反向，輕）、u3（水平線 sweep 非一對一）、u4（限定恢復一對一）、u7（可選，單位圓拉回）、u8（建參考三角形）、u11（主值只挑一點）、u13（可選，主值弧定象限）——聚焦教學意圖、自然語言；本輪不接入（比照 §1.1，第二輪生成）。
- **repeat-pattern：** 三段平行（arcsin 全展開；arccos／arctan 以「same idea／usual pattern」承接、只講差異點，不重述限定與恆等式 setup）；u13(b)、u14 重用參考三角形不重述。
- **register／禁則自查：** 全程 we／let us；無 “see / as shown / in the diagram”；無節號／圖號／式號；每段 hook→body→takeaway；數學多直讀 LaTeX、$\mathbb{R}$ 一律白話（“all real numbers”）。
- **單元數：** 18（16 教學 + intro/outro），落在 REBUILD_STATUS 估計 18–22 低端——平行結構的合理 fold 所致（非壓縮預算）。

### 稽核紀錄（2026-06-13，認可前回歸審核）

撰稿後跑了一輪六-lens 對抗式稽核（faithfulness／decomposition／register／no-repeat／math-accuracy／completeness），每條 actionable finding 再經獨立驗證過濾過度 triage／幻覺（比照 `review_pack.py` 紀律）：

- **math-accuracy：0 錯**——所有數值／正負／象限／區間端點／慣例例題經獨立重算，與講義逐項一致。
- **faithfulness／decomposition／no-repeat：無 L1**——16 教學單元全可回溯 §1.2 環境、無 silently drop、§7 各項自查經對源核實為真；三段平行（arcsin／arccos／arctan）以差異點＋壓縮 setup 通過 spiral 檢查。
- **採納並已修（1 項 + 2 項 polish）：**
  - **u11**：補回講義「particle 真正達到高度 1 的時刻」（$t=4\pi,6\pi,\dots$＝起動後的 $2\pi$ 倍數）——原稿只做主值否證、漏了結論；補回同時恢復忠實度並強化「主值 ≠ 全部解」對比。visual_need／animation_cue 同步：真正解另色標、非僅變灰。
  - **u3**：開場 cue「Picture」與 u2 重複 → 改「Look at」（§4 cue 少用）。
  - **u9 備註**：原稱「不重述限定理由」略過實——narration 以一句壓縮帶過，備註改稱「壓縮」以符實。
- **未動（L3 taste／設計取捨，列供認可時參考）：** u2 motivation 8 句、u16 收束例 ~9 句（皆在 kind 可接受上緣）；u12 arctan「整條數線擠進帶」可另加動畫（動畫密度屬第二輪設計取捨，暫不加，認可時可定）。

---

## 待辦／工程現況

1. **narration 認可仍待使用者確認**——本稿已完成內容層稽核與 `_narration.html` 交付；目前只是工程先行，不代表旁白已正式定稿。
2. **工程稿已先行完成到 storyboard／mock 層**——`storyboards/ch01_inverse_trig.yml`、`storyboards/ch01_inverse_trig_mimo.yml`、`ch01_inverse_trig.spoken.yml`、`ch01_inverse_trig_narration_spoken.md` 已存在；Mode B 已收斂到 clean。
3. **輸出需修補重組**——`output/ch01_inverse_trig.mp4` 目前約 51 秒，屬 partial；`output/_media/videos/1080p30/` 缺 `ch01_inverse_trig__when_arcsin_sin_breaks.mp4`，下一步先補該 scene，再 full compose。
4. **工程缺口（第二輪）：reference-triangle／branch 視覺 polish**——u8／u13／u14 需直角三角形＋標邊長＋角；u15 的六函數 domain/range 用既有 `value_table` 模板；限定分支（u3/u4/u9/u12）用 `graph_focus`／`graph_compare`。這些已可在現有 storyboard 上二修，不再是「認可後才開始」。
5. **正式聲音流程**——旁白認可後才進 MiMo TTS／critic／4K；若旁白口味有修改，需同步重跑 spoken derive 與 Mode B。
