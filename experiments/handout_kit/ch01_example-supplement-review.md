# Ch 1 課文範例補充——審核文件（待使用者裁決）

日期：2026-06-12
定位：依使用者 2026-06-12 澄清的正確框架——題庫補的是**課文內的 worked examples**，
不是節末習題（決策記錄見 [`CONTENT_EXERCISES.md`](../../CONTENT_EXERCISES.md) 適用範圍修正）。
題源原文全文見 [`ch01_candidate-review.md`](ch01_candidate-review.md)（pantry，以 C-ID 引用）。

選題鏡頭（與習題版的差異）：

1. **缺口＝教學點沒有示範**，不是「沒有練習」。基準是六個片段裡**既有的 22 個 worked
   examples**（下表），不是空集合。
2. **官方完整 solution 是硬條件**——範例必須帶解，所以只取解材完整的源（CLP／APEX ε-δ／
   Mooculus 講解段），APEX 那批只有最終答案的單題檔不再是好候選。
3. **數量克制**：每節補 1–3 個，補在手稿真正薄的點上，不是灌量。

## 怎麼回覆（裁決表）

```
核心 15 個（E 編號見下）：照單 / 去掉 ___ / 重議
選收 6 個：O1.1-d ___  O1.2-d ___  O1.3-b ___  O1.5-d ___  O1.6-c ___  O1.6-d(AI) ___
          （每個填：收 / 不收；O1.6-d 是 AI 出題，收=授權我出、你再審）
build：gen_standalone.py 支援 Ch 1 重生（建議，不回則照此做） / 手改 standalone
```

## 既有範例盤點（基準）

| 節 | 既有 examples | 內容 |
|---|---|---|
| §1.1 | 1.1–1.4（4 個） | 學號一對一；x vs x² 判一對一；x、x³ 求反函數；x³+2 求反函數＋單向驗證 |
| §1.2 | 1.5–1.6（2 個） | arcsin(1/2)、tan(arcsin ⅓)（三角形）；cos(arctan x)（恆等式法） |
| §1.3 | 1.7–1.8（2 個） | 兩個列表猜極限（(x−1)/(x²−1)、(√(t²+9)−3)/t²） |
| §1.4 | 1.9–1.12（4 個） | 分段函數單側極限；1/x²→∞；2x/(x−3) 漸近線符號分析；ln x→−∞ |
| §1.5 | 1.13–1.19（7 個） | 直接代入；因式分解；有理化；\|x\|；高斯符號 [x]；squeeze ×2 |
| §1.6 | 1.20–1.22（3 個） | 容差暖身（0.1→δ）；線性 ε-δ；二次 ε-δ（min{1, ε/4}） |

整體評語：手稿經 Mode A 擴寫後其實不算貧瘠；薄點是**系統性的**——§1.1 只示範失敗不示範修復、
§1.2 的 arccos／arctan／其餘三函數零數值範例、§1.5 的 limit laws 從未抽象演示、§1.6 缺
「定義的邏輯結構」示範。以下逐節補。

---

## §1.1 Inverse Functions（補 3，4→7）

**E1.1-a　代數判定一對一（直覺會失效的例子）** `[source: Mooculus digInInversesOfFunctions L293]`（C1.1-D）
- 缺口：既有 Example 1.2 的 x 與 x² 都「看一眼就知道」；沒有需要動手代數判定、且單調直覺失效的例子。
- 插入點：`sec-1-1.html` Example 1.2 之後、「The function \(g(x)=x^2\)…」段落之前。
- 擬改寫：

  > **Example.** Determine whether each function is one-to-one on \(\mathbb{R}\):
  > \[ h(x) = x^{3} - 4x, \qquad k(x) = x^{3} + 4. \]
  >
  > **Solution.** For \(h\), we look for two different inputs with the same output. Since
  > \(h(x) = x(x^{2}-4) = x(x-2)(x+2)\), we have \(h(0) = h(2) = 0\) with \(0 \neq 2\), so \(h\)
  > is *not* one-to-one — even though its formula looks similar to \(x^{3}\).
  > For \(k\), suppose \(k(x_{1}) = k(x_{2})\). Then \(x_{1}^{3} + 4 = x_{2}^{3} + 4\), so
  > \(x_{1}^{3} = x_{2}^{3}\), and taking cube roots gives \(x_{1} = x_{2}\). Therefore \(k\)
  > *is* one-to-one. The lesson: two formulas of the same general shape can behave differently;
  > when in doubt, test the definition directly.

**E1.1-b　限制定義域修復不可逆函數（x² → √x）** `[source: Mooculus L407–453]`（C1.1-I）
- 缺口：全節反覆說 x² 不可逆，但**從未示範「怎麼修」**——限制定義域是反三角函數一整節的前置觀念，目前只在 §1.2 開頭突然出現。
- 插入點：`sec-1-1.html` 鏡射段落（「Graphically, … reflections across the line \(y=x\)」）之後。
- 擬改寫：

  > **Example.** The function \(f(x) = x^{2}\) is not one-to-one on \(\mathbb{R}\). Restrict its
  > domain so that the restricted function is one-to-one, and find the inverse of the restricted
  > function.
  >
  > **Solution.** On the interval \([0, \infty)\) the function \(f(x) = x^{2}\) is one-to-one:
  > if \(x_{1}^{2} = x_{2}^{2}\) with \(x_{1}, x_{2} \ge 0\), then \(x_{1} = x_{2}\). To find the
  > inverse, write \(x = \bigl(f^{-1}(x)\bigr)^{2}\); since \(f^{-1}(x) \ge 0\), taking the
  > positive square root gives
  > \[ f^{-1}(x) = \sqrt{x}, \qquad x \ge 0. \]
  > This is exactly why \(\sqrt{x}\) means the *positive* square root: the convention makes the
  > square root the inverse of the restricted squaring function. Figure ⟨new⟩ shows the
  > restricted parabola, its inverse, and the mirror line \(y = x\). The same idea — restrict
  > first, then invert — is the key to the inverse trigonometric functions of the next section.

- 附圖：1 幅（restricted x²、√x、y=x 虛線；遵 redundant encoding）。
- 備註：結尾一句是 forward reference，正好把 §1.1 與 §1.2 的斷裂縫起來。

**E1.1-c　有理函數求反＋雙向驗證** `[source: APEX §2.7 #7]`（C1.1-G；APEX 僅給指示，解為本次撰寫、屬改作）
- 缺口：Example 1.4 只驗證了 \(f(f^{-1})\) 單向；Proposition 1.1 的雙向恆等式沒有完整示範；Strategy 1.1 沒在非多項式上跑過。
- 插入點：`sec-1-1.html` 末尾，Example 1.4 之後。
- 擬改寫：

  > **Example.** Find the inverse of \(f(x) = \dfrac{3}{x-5}\) (for \(x \neq 5\)), and verify
  > your answer by computing both \(f\bigl(f^{-1}(x)\bigr)\) and \(f^{-1}\bigl(f(x)\bigr)\).
  >
  > **Solution.** Let \(y = \dfrac{3}{x-5}\). Solving for \(x\): \(x - 5 = \dfrac{3}{y}\), so
  > \(x = 5 + \dfrac{3}{y}\). Interchanging the variables,
  > \[ f^{-1}(x) = 5 + \frac{3}{x} = \frac{5x+3}{x}, \qquad x \neq 0. \]
  > Verification, in both directions:
  > \[ f\bigl(f^{-1}(x)\bigr) = \frac{3}{\bigl(5 + \tfrac{3}{x}\bigr) - 5} = \frac{3}{3/x} = x,
  > \qquad
  > f^{-1}\bigl(f(x)\bigr) = 5 + \frac{3}{3/(x-5)} = 5 + (x - 5) = x. \]
  > Both compositions return the input, confirming Proposition 1.1. Note how the domains pair
  > up: \(f\) excludes \(x = 5\) and \(f^{-1}\) excludes \(x = 0\), matching the fact that
  > \(f\) never takes the value \(0\) and \(f^{-1}\) never takes the value \(5\).

**O1.1-d（選收）　應用：攝氏↔華氏** `[source: Mooculus L181–227]`（C1.1-H）
- 補 applied 面向（手稿的應用只有學號例）。插入 §1.1 末。內容同 pantry 擬改寫版。

---

## §1.2 Inverse Trigonometric Functions（補 3，2→5）

**E1.2-a　arccos／arctan 的精確值（含負輸入與鈍角主值）** `[source: Stitz-Zeager via Mooculus 10_06_ex_131-154]`（C1.2-D）
- 缺口：數值範例只有 arcsin（Example 1.5）；arccos 的鈍角主值、arctan 的三角形法、負輸入的符號處理全無示範。
- 插入點：`sec-1-2.html` Proposition 1.4 之後、「The remaining inverse trigonometric functions」小節之前。
- 擬改寫：

  > **Example.** Find the exact value of each expression.
  > (a) \(\sin\bigl(\arccos(-\tfrac{1}{2})\bigr)\)  (b) \(\sec(\arctan 10)\)
  > (c) \(\tan\bigl(\arcsin(-\tfrac{2\sqrt5}{5})\bigr)\)
  >
  > **Solution.** (a) Since \(\arccos(-\tfrac12)\) is the angle in \([0,\pi]\) whose cosine is
  > \(-\tfrac12\), we get \(\arccos(-\tfrac12) = \tfrac{2\pi}{3}\), and
  > \(\sin\tfrac{2\pi}{3} = \tfrac{\sqrt3}{2}\). Note the principal value lands in the *second*
  > quadrant — negative inputs to \(\arccos\) always do.
  > (b) Let \(\theta = \arctan 10\), so \(\tan\theta = 10\) with
  > \(\theta \in (0, \tfrac{\pi}{2})\). In a right triangle with opposite side \(10\) and
  > adjacent side \(1\), the hypotenuse is \(\sqrt{101}\), so
  > \(\sec(\arctan 10) = \sqrt{101}\).
  > (c) Let \(\theta = \arcsin\bigl(-\tfrac{2\sqrt5}{5}\bigr)\), so
  > \(\sin\theta = -\tfrac{2}{\sqrt5}\) with
  > \(\theta \in [-\tfrac{\pi}{2}, \tfrac{\pi}{2}]\). Because \(\sin\theta < 0\), the angle lies
  > in the fourth quadrant, where cosine is positive:
  > \(\cos\theta = \sqrt{1 - \tfrac45} = \tfrac{1}{\sqrt5}\). Therefore
  > \(\tan\theta = \dfrac{-2/\sqrt5}{1/\sqrt5} = -2\). The sign came from the *range* of
  > \(\arcsin\), not from guessing.

**E1.2-b　複合函數的定義域** `[source: CLP-1 §2.12 #1 (a)(c)]`（C1.2-B；官方詳解完整）
- 缺口：本節建立了六張 domain／range 表，但沒有任何範例**使用**它們；「值域餵進定義域」的鏈式思考零示範。
- 插入點：`sec-1-2.html` Proposition 1.3（arccos 恆等式）之後。
- 擬改寫：

  > **Example.** Find the domain of each function.
  > (a) \(f(x) = \arcsin(\cos x)\)  (b) \(h(x) = \sin(\arccos x)\)
  >
  > **Solution.** (a) Whatever \(x\) is, \(\cos x\) lies in \([-1,1]\), and \([-1,1]\) is
  > exactly the domain of \(\arcsin\). So every real \(x\) is allowed: the domain of \(f\) is
  > \(\mathbb{R}\).
  > (b) The inner function \(\arccos x\) requires \(x \in [-1,1]\); its output is an angle,
  > and \(\sin\) accepts any angle. So the domain of \(h\) is \([-1,1]\). The pattern in both
  > parts: the domain of a composition is governed by what the *inner* function accepts and
  > what its outputs feed the *outer* function.

**E1.2-c　其餘反三角函數的定義域＋本書分支約定的實際後果** `[source: CLP-1 §2.12 #5，依本書 arccsc 主值改作]`（C1.2-E）
- 缺口：「remaining functions」小節零範例；且 Remark 1.3/1.4 講分支約定會影響值，**沒有任何例子展示**。
- 插入點：`sec-1-2.html` 域/值域總結段（「The domains of \(\arccsc\)…」）之後、Remark 1.3 之前，加一句過場「The choice of principal range has visible consequences, as the next example shows.」
- 擬改寫：

  > **Example.** Let \(f(x) = \arcsin x + \arccsc x\). Find the domain of \(f\), and evaluate
  > \(f\) at every point of its domain.
  >
  > **Solution.** \(\arcsin\) requires \(|x| \le 1\) while \(\arccsc\) requires \(|x| \ge 1\),
  > so the domain is just the two points \(x = \pm 1\). At \(x = 1\):
  > \(\arcsin 1 = \tfrac{\pi}{2}\) and \(\arccsc 1 = \tfrac{\pi}{2}\) (the angle in
  > \(\bigl(0,\tfrac{\pi}{2}\bigr]\) with cosecant \(1\)), so \(f(1) = \pi\). At \(x = -1\):
  > \(\arcsin(-1) = -\tfrac{\pi}{2}\), and under this text's principal range for \(\arccsc\)
  > the angle with cosecant \(-1\) is \(\arccsc(-1) = \tfrac{3\pi}{2}\), so
  > \(f(-1) = -\tfrac{\pi}{2} + \tfrac{3\pi}{2} = \pi\). So \(f\) is the constant \(\pi\) on
  > its two-point domain. *Under the alternative convention of Remark 1.4*
  > (\(\arccsc(-1) = -\tfrac{\pi}{2}\)) one gets \(f(-1) = -\pi\) instead — a concrete instance
  > of branch conventions changing answers, which is why this text fixes its conventions
  > explicitly.
- 備註：CLP 原解用標準主值（f(−1)=−π）；本改作依 Definition 1.6 的本書主值重算（f(−1)=π），
  並把差異變成教學點，直接呼應 Remark 1.3/1.4。**這是全批改作幅度最大的一筆**，請特別過目。

**O1.2-d（選收）　主值的應用陷阱（粒子與 arccos(1)）** `[source: CLP-1 §2.12 #2]`（C1.2-C）
- 插入 Caution 區之後當概念範例。內容照 pantry。

---

## §1.3 The Limit of a Function（補 1，2→3）

**E1.3-a　從圖讀極限（含 lim ≠ f(a) 的點）** `[source: CLP-1 §1.3 #1]`（C1.3-D(i)；官方詳解完整）
- 缺口：Figure 1.7 畫了「同極限、不同函數值」但**沒有讀圖的 worked example**；兩個既有範例都是列表法。
- 插入點：`sec-1-3.html` Figure 1.7 之後、Example 1.7 之前。
- 擬改寫：

  > **Example.** The graph of a function \(f\) is shown. Evaluate the following, or state that
  > the limit does not exist:
  > (a) \(\lim_{x \to -2} f(x)\)  (b) \(\lim_{x \to 0} f(x)\)  (c) \(\lim_{x \to 2} f(x)\)
  >
  > **Solution.** (a) As \(x\) approaches \(-2\) from either side, the curve approaches height
  > \(1\), so the limit is \(1\). (b) As \(x\) approaches \(0\), the curve approaches height
  > \(0\), so the limit is \(0\). (c) As \(x\) approaches \(2\), the curve approaches height
  > \(2\) — the open dot at \((2,2)\) and the solid dot at \((2,-2)\) tell us \(f(2) = -2\),
  > but the limit ignores the value *at* the point: the limit is \(2\), even though
  > \(f(2) = -2\).
- 附圖：1 幅（連續波形，(2,2) 空心、(2,−2) 實心；CLP 原圖重畫）。

**O1.3-b（選收）　構造：畫一條 lim=10 而 f(3)=0 的曲線** `[source: CLP-1 §1.3 #5]`（C1.3-B）
- 學生自己畫，無附圖成本；與 E1.3-a 的教學點互補（讀 vs 造）。插入 E1.3-a 之後。

---

## §1.4 One-Sided and Infinite Limits（補 3，4→7）

**E1.4-a　1/x vs 1/x²：DNE 與 ∞ 的分界** `[source: CLP-1 §1.3 #13, #14, #15]`（C1.4-B；官方詳解互相對照）
- 缺口：手稿有 1/x²→∞（Example 1.10）但**沒有 1/x**——「左右一正一負所以 DNE、且不是 ±∞」這個經典對照完全缺席。
- 插入點：`sec-1-4.html` Example 1.10 之後、「To capture this behavior…」段之前（讓 ∞ 記號的引入同時服務兩個例子）。
- 擬改寫：

  > **Example.** Evaluate \(\displaystyle\lim_{x \to 0^{-}} \frac{1}{x}\),
  > \(\displaystyle\lim_{x \to 0^{+}} \frac{1}{x}\), and \(\displaystyle\lim_{x \to 0} \frac{1}{x}\),
  > and contrast the results with \(\displaystyle\lim_{x \to 0} \frac{1}{x^{2}}\).
  >
  > **Solution.** As \(x\) approaches \(0\) from the left, \(\tfrac1x\) is negative with larger
  > and larger magnitude, so \(\lim_{x \to 0^{-}} \tfrac1x = -\infty\). From the right,
  > \(\tfrac1x\) is positive and grows without bound, so \(\lim_{x \to 0^{+}} \tfrac1x = \infty\).
  > Because the two one-sided behaviors disagree, the two-sided limit does not exist — and since
  > the values do not all grow in the *same* signed direction, we do **not** write
  > \(\lim_{x \to 0} \tfrac1x = \infty\). Contrast \(\tfrac{1}{x^{2}}\): both sides grow
  > positively, so there we do write \(\lim_{x \to 0} \tfrac{1}{x^{2}} = \infty\).

**E1.4-b　由部分資訊推論：判準的雙向使用** `[source: CLP-1 §1.3 #8, #9]`（C1.4-A；官方詳解完整）
- 缺口：Proposition 1.5（兩側判準）只在「算出兩側→判定雙側」方向用過（Example 1.9）；「已知雙側→推單側」與「只知單側→資訊不足」從未演示。
- 插入點：`sec-1-4.html` Proposition 1.5 與其後一句之後、Example 1.9 之前。
- 擬改寫：

  > **Example.** Suppose \(f\) is defined on all of \(\mathbb{R}\).
  > (a) If \(\lim_{x \to -2} f(x) = 16\), what is \(\lim_{x \to -2^{-}} f(x)\)?
  > (b) If instead all we know is \(\lim_{x \to -2^{-}} f(x) = 16\), what can we say about
  > \(\lim_{x \to -2} f(x)\)?
  >
  > **Solution.** (a) For the two-sided limit to equal \(16\), *both* one-sided limits must
  > equal \(16\); in particular \(\lim_{x \to -2^{-}} f(x) = 16\).
  > (b) Not enough information. If the right-hand limit also equals \(16\), then
  > \(\lim_{x \to -2} f(x) = 16\); if it differs (or fails to exist), the two-sided limit does
  > not exist. The criterion transfers information from the two-sided limit to each side, but
  > only *both* sides together determine the two-sided limit.

**E1.4-c　分母為零不保證鉛直漸近線** `[source: CLP-1 §3.6.1 #1]`（C1.4-E；官方詳解完整）
- 缺口：Example 1.11 只示範了「候選點成功變成漸近線」；「候選點失敗」（洞）的一側從未出現，而這是學生最常見的誤判。
- 插入點：`sec-1-4.html` Example 1.11 之後、Figure 1.10 之後。
- 擬改寫：

  > **Example.** Suppose \(f(x) = \dfrac{g(x)}{x^{2}-9}\) for some function \(g\). Must the
  > line \(x = -3\) be a vertical asymptote of \(y = f(x)\)?
  >
  > **Solution.** No. The denominator does vanish at \(x = -3\), so \(x = -3\) is a
  > *candidate* — but whether it is an asymptote depends on the numerator. If \(g(x) = 1\),
  > then \(f(x) = \tfrac{1}{x^{2}-9}\) blows up near \(-3\), and \(x = -3\) is a vertical
  > asymptote. But if \(g(x) = x^{2}-9\), then \(f(x) = 1\) at every point of its domain, and
  > there is no asymptote at all. A zero denominator marks a place to *investigate* with
  > one-sided limits, not a guaranteed asymptote.

---

## §1.5 Limit Laws and Computational Techniques（補 3，7→10）

**E1.5-a　抽象地使用 limit laws** `[source: CLP-1 §1.4 #42]`（C1.5-G；官方解完整）
- 缺口：Theorem 1.2 之後直接跳到具體多項式；「不知道 f 是什麼、只知道它的極限」的抽象使用零示範——而這正是 laws 的本義。
- 插入點：`sec-1-5.html` Theorem 1.2 後的口頭重述段之後、「Direct substitution」小節之前。
- 擬改寫：

  > **Example.** Suppose \(\displaystyle\lim_{x \to -1} f(x) = -1\). Evaluate
  > \[ \lim_{x \to -1} \frac{x\,f(x) + 3}{2 f(x) + 1}. \]
  >
  > **Solution.** We never need a formula for \(f\). By the product law,
  > \(\lim_{x \to -1} x f(x) = (-1)(-1) = 1\); by the sum and constant-multiple laws the
  > numerator tends to \(1 + 3 = 4\) and the denominator tends to \(2(-1) + 1 = -1\). The
  > denominator's limit is nonzero, so the quotient law applies:
  > \[ \lim_{x \to -1} \frac{x f(x) + 3}{2 f(x) + 1} = \frac{4}{-1} = -4. \]

**E1.5-b　0/0 可以是任何值** `[source: CLP-1 §1.4 #2, #5]`（C1.5-J；官方解完整）
- 缺口：「indeterminate」一詞出現了，但**為什麼**不定（可以是任何值）沒有任何示範；學生普遍誤信 0/0 必為 1 或 0。
- 插入點：`sec-1-5.html` 「Algebraic simplification」小節首段之後、Example 1.14 之前。
- 擬改寫：

  > **Example.** (a) Find functions \(f\) and \(g\) with
  > \(\lim_{x \to 3} f(x) = \lim_{x \to 3} g(x) = 0\) and
  > \(\lim_{x \to 3} \dfrac{f(x)}{g(x)} = 10\).
  > (b) What are the possible values of \(\lim_{x \to 3} \dfrac{f(x)}{g(x)}\), given only that
  > both \(f\) and \(g\) tend to \(0\)?
  >
  > **Solution.** (a) Take \(f(x) = 10(x-3)\) and \(g(x) = x - 3\). Both tend to \(0\) at
  > \(3\), yet \(\dfrac{f(x)}{g(x)} = 10\) wherever it is defined, so the quotient's limit is
  > \(10\). (b) Replacing \(10\) by any constant \(c\) gives limit \(c\); choices such as
  > \(f(x) = x-3\), \(g(x) = (x-3)^{3}\) give \(\infty\); swapping signs gives \(-\infty\); and
  > \(f(x) = x - 3\), \(g(x) = |x-3|\) makes the limit fail to exist. A \(\tfrac00\) form can
  > therefore equal *anything* — which is exactly why it is called indeterminate, and why we
  > must simplify before judging.

**E1.5-c　反推常數使極限存在（壓軸綜合）** `[source: CLP-1 §1.4 #43]`（C1.5-G；官方解完整）
- 缺口：所有既有範例都「正向計算」；沒有一個需要先用 limit laws 推理（分母趨 0 ⟹ 分子必須趨 0）再計算的綜合題。Strategy 1.2 之後正缺一個收束全節的示範。
- 插入點：`sec-1-5.html` Strategy 1.2 之後（全節最末）。
- 擬改寫：

  > **Example.** Find the value of the constant \(a\) for which
  > \(\displaystyle\lim_{x \to -2} \frac{x^{2} + a x + 3}{x^{2} + x - 2}\) exists, and evaluate
  > the limit for that value of \(a\).
  >
  > **Solution.** The denominator factors as \((x+2)(x-1)\) and tends to \(0\) as
  > \(x \to -2\). If the numerator tended to a nonzero number, the quotient would blow up and
  > the limit could not exist; so the numerator must also tend to \(0\):
  > \(4 - 2a + 3 = 0\), giving \(a = \tfrac{7}{2}\). With this \(a\),
  > \[ \lim_{x \to -2} \frac{x^{2} + \tfrac{7}{2}x + 3}{x^{2} + x - 2}
  > = \lim_{x \to -2} \frac{(x+2)\bigl(x + \tfrac{3}{2}\bigr)}{(x+2)(x-1)}
  > = \lim_{x \to -2} \frac{x + \tfrac{3}{2}}{x - 1}
  > = \frac{-\tfrac12}{-3} = \frac{1}{6}. \]
  > Notice the flow of reasoning: the *existence* of the limit forced the value of \(a\), and
  > then the techniques of this section finished the computation.

**O1.5-d（選收）　通分化簡** `[source: CLP-1 §1.4 extra（prob_s1.4.tex:751）]`
- Strategy 1.2 第 2 步點名了「combine fractions」但沒有範例做過。
  \(\lim_{t \to 1/2}\frac{\frac{1}{3t^{2}}+\frac{1}{t^{2}-1}}{2t-1} = -\tfrac{32}{9}\)，官方解完整。
  代數較重，由你定奪。插入 Example 1.15 之後。

---

## §1.6 The Precise Definition of a Limit（補 2，3→5）

**E1.6-a　診斷一個寫錯的定義** `[source: APEX §1.2 #1, #2]`（C1.6-A/B；官方解完整）
- 缺口：定義的「量詞順序與蘊含方向」只靠 prose 講；沒有讓學生主動辨錯的示範——這是 ε-δ 最高頻的誤解。
- 插入點：`sec-1-6.html` Definition 1.13 後的解說段（「The condition \(0<|x-a|<\delta\)…」）之後、uniqueness 之前。
- 擬改寫：

  > **Example.** What is wrong with the following attempted definition of
  > \(\lim_{x \to a} f(x) = L\)?
  > *“Given any \(\delta > 0\), there exists \(\varepsilon > 0\) such that whenever
  > \(|f(x) - L| < \varepsilon\), we have \(0 < |x - a| < \delta\).”*
  >
  > **Solution.** Two things are reversed. First, the *order of the tolerances*: the challenge
  > must come on the \(y\)-side — “given any \(\varepsilon\)” — and \(\delta\) is our response;
  > the attempted version lets us pick the easy quantity after seeing the hard one. Second, the
  > *direction of the implication*: the definition must say that closeness of \(x\) to \(a\)
  > **forces** closeness of \(f(x)\) to \(L\), i.e. \(0 < |x-a| < \delta\) implies
  > \(|f(x) - L| < \varepsilon\) — not the other way around. Keeping both corrections gives
  > exactly Definition 1.13.

**E1.6-b　用已知不等式餵 ε-δ：lim sin x = 0** `[source: APEX §1.2 #8]`（C1.6-E；官方解完整）
- 缺口：既有兩個證明（線性、二次）都是「代數整理型」；「借一個已知不等式直接喂進定義」是第三種典型套路，且為 squeeze 式思維鋪路。
- 插入點：`sec-1-6.html` Example 1.22 之後、Definition 1.14 之前。
- 擬改寫：

  > **Example.** Using the fact that \(|\sin x| \le |x|\) for all \(x\), show from the
  > definition that \(\displaystyle\lim_{x \to 0} \sin x = 0\).
  >
  > **Solution.** Given \(\varepsilon > 0\), choose \(\delta = \varepsilon\). If
  > \(0 < |x - 0| < \delta\), then
  > \[ |\sin x - 0| = |\sin x| \le |x| < \delta = \varepsilon. \]
  > Therefore \(\lim_{x \to 0} \sin x = 0\). The borrowed inequality did all the work: no
  > factoring, no auxiliary bound — Step 2 of Strategy 1.3 was handed to us for free.

**O1.6-c（選收）　常數函數：任何 δ 都行** `[source: APEX §1.2 #3]`（C1.6-C）
- 「δ 可以隨便選」是個小而亮的觀念點（學生常以為 δ 必須是 ε 的某個函數）。插入 Example 1.21 之前。

**O1.6-d（選收，AI 出題）　Definition 1.14 的 M-δ 示範**
- Definition 1.14（無限極限的精確版）目前零示範。題庫無乾淨候選（先前缺口 B）。若收，
  我以 `[source: AI]` 出一題：用定義證 \(\lim_{x \to 0} \tfrac{1}{x^{2}} = \infty\)
  （給 \(M\)，取 \(\delta = 1/\sqrt{M}\)），與 Example 1.10 首尾呼應。出後由你審。

---

## 裁決後的 import pass（預告）

1. `gen_standalone.py` 增 Ch 1 重生支援（除非你選手改 standalone）。
2. 依各 E 編號的插入點寫入 `example-ch01/sec-*.html`：`workedexample` 包 `env-example`＋
   `env-solution`，每筆前加 `<!-- expansion:example — … [source: …] -->` 註解（沿用既有
   expansion-marker 慣例）。
3. **手動重編號稅**：插入會使後續 example 的 `env-num` 全部位移（如手稿 Example 1.3 變
   1.5），新圖也會使 Figure 1.7+ 位移且 prose 內的「Figure 1.x」引用需同步——import 後以
   grep 核對所有 `env-num`／`fig-no`／prose 引用一致（kit 無自動編號，這是合約已知的 authoring tax）。
4. 新附圖 2 幅（E1.1-b、E1.3-a）進該章 `figures.js`，遵 redundant encoding。
5. 建 `ch01_example-imports.md`：每筆收錄題源官方解全文、授權標記、改寫差異說明
   （特別是 E1.2-c 的主值改算）。
6. 重生 standalone 兩版，瀏覽器驗渲染。
