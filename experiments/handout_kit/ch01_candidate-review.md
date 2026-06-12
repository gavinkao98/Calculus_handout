# Ch 1 候選題全文節錄（題源 pantry）

> **2026-06-12 框架更正：本檔的「節末習題」框架已作廢**——使用者澄清：題庫補的是**課文內的
> worked examples（教學範例）**，講義本體不收節末習題（習題日後另出獨立習題本）。因此本檔的
> 裁決表、各節擬定題數、四類配比統計**不再適用**；新的裁決文件是
> [`ch01_example-supplement-review.md`](ch01_example-supplement-review.md)。
> 本檔保留價值＝**45 組候選的原文節錄、檔案行號、官方解材狀態與授權核驗**（C-ID 索引），
> 新文件以 C-ID 引用之。

日期：2026-06-12
前置：[`ch01_coverage-matrix.md`](ch01_coverage-matrix.md)（覆蓋矩陣＋候選短摘要）。
本檔是矩陣「Proposed next review pass」的全文版：每組候選附**題目原文**（節錄，TikZ 圖以
【圖】描述代替）、**官方解材狀態**、**擬改寫**與建議。所有原文已逐條對到本機
`problem_banks/` 的檔案與行號，皆可覆核。

## 怎麼回覆（裁決表）

複製下方區塊、填完傳回即可。「照單」＝接受該節的擬定清單；「去掉」＝照單但剔除指定題號。

```
§1.1（擬 10 題）：照單 / 去掉 ___ / 重議
§1.2（擬 7–8 題）：照單 / 去掉 ___ / 重議
§1.3（擬 7 題）：照單 / 去掉 ___ / 重議
§1.4（擬 9 題）：照單 / 去掉 ___ / 重議
§1.5（擬 14 題）：照單 / 去掉 ___ / 重議
§1.6（擬 7–8 題）：照單 / 去掉 ___ / 重議
缺口 A（§1.6 limit 唯一性）：AI 出一題引導式證明（建議） / 不練
缺口 B（§1.6 精確無限極限定義）：不練，§1.4 非正式版已足（建議） / AI 出題
裁量 C（C1.2-F 三角形化簡，源自導數題）：收 inversesTrig7 替代版（建議） / 收 CLP 版 / 都不收
裁量 D（§1.5 追加題 C1.5-J，矩陣未列）：收（建議） / 不收
build：gen_standalone.py 支援 Ch 1 重生（建議，不回則照此做） / 手改 standalone
```

## 全章總覽

| 節 | 擬定題數 | 預算帶 | 四類分布（c/p/r/a） | 附圖需求 |
|---|---|---|---|---|
| §1.1 | 10 | 8–10 | 4/3/2/1 | 2 幅 |
| §1.2 | 7–8 | ~8 | 2/3/2/1 | 0（三角形畫在解答，不進題幹） |
| §1.3 | 7 | 6–8 | 3/2/2/0 | 2 幅 |
| §1.4 | 9 | 8–10 | 2/4/3/0 | 1 幅 |
| §1.5 | 14 | 12–15 | 2/8/3/1 | 0 |
| §1.6 | 7–8 | 6–8 | 2/3/3/0 | 0 |
| 合計 | 54–56 |  | 章層級約 28% c / 42% p / 27% r / 6% a — 落在全書先驗內 | ~5 幅 |

附圖：原題的 TikZ 圖需重畫為 kit 的 `figures.js` SVG（遵 CONTENT_SPEC §10 redundant
encoding）。這是 import pass 最大的工作量，先列出讓你知道成本。

授權核驗（全部 NC 家族 ✓）：CLP-1＝CC BY-NC-SA 4.0（逐檔檔頭可證）；APEX＝CC BY-NC 4.0；
Mooculus 逐題檔＝CC BY-NC 3.0（Gubkin／Lakos 等）；`10_06_ex_131-154.tex`＝Stitz-Zeager
轉收，檔頭 `\license{CC-By-SA-NC}`＝CC BY-NC-SA。

矩陣勘誤（本檔已修正）：
1. **#39 重複指派**——`CLP-1 §1.4 #39`（`3+|x|/x`）同時被 C1.4-C 與 C1.5-E 引用。
   裁定：歸 §1.4（教學點是單側極限不一致），§1.5 的絕對值 cluster 改用 #40、#41。
2. **C1.3-D／C1.4-A 邊界**——`§1.3 #3`（五小題單側極限讀圖）矩陣放 §1.3，但它通篇單側，
   移到 §1.4 當讀圖題更對位。
3. **C1.2-D 來源更正**——「Mooculus 10_06_ex_131-154」實為 Mooculus repo 內轉收的
   Stitz-Zeager 題（`mooculus/derivativesOfInverseFunctions/exercises/10_06_ex_131-154.tex`）。

---

## §1.1 Inverse Functions（擬 10 題）

**1. C1.1-A** `[source: APEX §2.7 #1]` `APEXCalculusV5/exercises/02_07_ex_01.tex`
- 原文：`T/F: Every function has an inverse.`（答案：F）
- 官方解材：僅 T/F 答案。
- 擬改寫（APEX 太簡，補要求說理）：
  > True or false: every function has an inverse. If true, explain why; if false, give a
  > counterexample and explain what goes wrong.
- 建議：收。開場概念題。

**2. C1.1-B** `[source: APEX §2.7 #2]` `02_07_ex_02.tex`
- 原文：`In your own words explain what it means for a function to be "one to one."`
- 擬改寫：照原文，加一句 `…and explain why this property is exactly what an invertible function needs.`
- 建議：收。

**3. C1.1-C** `[source: Mooculus digInInversesOfFunctions L268]`（CC BY-NC 3.0）
- 原文（selectAll 互動題）：Which of the following are functions that are also one-to-one?
  選項：字典單字→字義／直線前進的跑者時間→位置／人→生日／母親→子女。
  官方 feedback 逐項解釋（字義不唯一故非函數；跑者是一對一；生日多人共享故非一對一；母親可有多子女故非函數）。
- 擬改寫（互動→靜態，要求逐項判斷）：
  > For each of the following rules, decide (i) whether it defines a function, and (ii) if so,
  > whether that function is one-to-one. Justify each answer.
  > (a) Assigning to each word its meaning in a dictionary.
  > (b) Assigning to each time the position of a runner racing forward on a straight path.
  > (c) Assigning to each person his or her birth date.
  > (d) Assigning to each mother her children.
- 建議：收。生活情境暖身，順帶複習「函數」本身。

**4. C1.1-D** `[source: Mooculus L293]`
- 原文（selectAll）：Which of the following functions are one to one? `x`, `x²`, `x³−4x`, `x³+4`（正解 x 與 x³+4）。
- 擬改寫：
  > Determine which of the following functions are one-to-one. Justify your answers.
  > \(f(x)=x\), \(g(x)=x^2\), \(h(x)=x^3-4x\), \(k(x)=x^3+4\)
- 建議：收。h 是亮點（單調性直覺失效，需找兩輸入同輸出）。

**5. C1.1-E** `[source: Mooculus L344–385]`【圖：三次曲線，x 軸標 A–E 五點】
- 原文（selectAll）：On which of the following intervals is f one-to-one? `[A,B]`✓ `[A,C]` `[B,D]`✓ `[C,E]` `[C,D]`✓
- 擬改寫：
  > The graph of a function \(f\) is shown, with five points \(A,B,C,D,E\) marked on the
  > \(x\)-axis. For each of the intervals \([A,B]\), \([A,C]\), \([B,D]\), \([C,E]\), \([C,D]\),
  > use the horizontal line test to decide whether \(f\) is one-to-one on that interval.
- 附圖：需重畫（三次曲線＋五標記點）。
- 建議：收。水平線測試的主力練習。

**6. C1.1-F** `[source: Mooculus L79–93]`
- 原文（填空）：If the point (1,9) is on the graph of f, what point must be on the graph of f⁻¹?（答 (9,1)，feedback 給一般規則）
- 擬改寫：
  > Suppose the point \((1,9)\) lies on the graph of \(f\). What point must lie on the graph of
  > \(f^{-1}\)? State the general rule your answer illustrates.
- 建議：收。

**7. C1.1-G** `[source: APEX §2.7 #5, #7]` `02_07_ex_05.tex`, `02_07_ex_07.tex`
- 原文：兩組函數對，指示為 compose 雙向驗證 inverse：
  (i) `f(x)=2x+6`, `g(x)=½x−3`；(ii) `f(x)=3/(x−5) (x≠5)`, `g(x)=(3+5x)/x (x≠0)`。
- 擬改寫（兩組併一題）：
  > For each pair, verify that \(g\) is the inverse of \(f\) by computing both \(f(g(x))\) and
  > \(g(f(x))\): (a) \(f(x)=2x+6\), \(g(x)=\tfrac12 x-3\); (b) \(f(x)=\dfrac{3}{x-5}\) for
  > \(x\ne 5\), \(g(x)=\dfrac{3+5x}{x}\) for \(x\ne 0\).
- 建議：收。組合恆等式的計算主力。

**8. C1.1-J** `[source: APEX §2.7 #6]` `02_07_ex_06.tex`
- 原文：`f(x)=x²+6x+11, x≥3` 與 `g(x)=√(x−2)−3, x≥2`，compose 雙向驗證。
- 擬改寫：照原文格式併入上題形態，但獨立成題並追問：
  > Verify that \(g(x)=\sqrt{x-2}-3\) (for \(x\ge 2\)) is the inverse of
  > \(f(x)=x^2+6x+11\) (for \(x\ge 3\)) by computing both compositions. Where does the
  > restriction on the domain of \(f\) enter your computation?
- 建議：收。把「限制定義域」跟「組合驗證」綁在一起。

**9. C1.1-H** `[source: Mooculus L181–227]`（原為 worked example，改寫為題）
- 原文：攝氏轉華氏 `f(t)=(9/5)t+32`，問反函數的意義並求 `f⁻¹(t)=(5/9)(t−32)`，雙向驗證。
- 擬改寫：
  > The function \(f(t)=\tfrac95 t+32\) converts a temperature of \(t\) degrees Celsius into
  > degrees Fahrenheit. What practical question does \(f^{-1}\) answer? Find a formula for
  > \(f^{-1}(t)\), and verify your formula by computing \(f^{-1}(f(t))\).
- 建議：收。本節唯一 applied 題。（原文是教學例非習題，但授權允許改作；出處照標。）

**10. C1.1-I** `[source: Mooculus L407–522]`【圖：解答用，題幹可不附圖】
- 原文：x² 不一對一→限制到 [0,∞) 得 √x（worked example）＋圖上限制 [1,2] 求 f⁻¹ 定義域等（互動題）。
- 擬改寫（合併為一道構造題）：
  > The function \(f(x)=x^2\) is not one-to-one on \(\mathbb{R}\). (a) Restrict the domain of
  > \(f\) so that the restricted function is one-to-one and find its inverse. (b) On one set of
  > axes, sketch the restricted \(f\), your \(f^{-1}\), and the line \(y=x\). (c) Explain why
  > \(g(x)=x^3\) needs no restriction.
- 建議：收。壓軸綜合（restriction＋反函數圖像＋y=x 反射）。

---

## §1.2 Inverse Trigonometric Functions（擬 7–8 題）

**1. C1.2-A** `[source: Mooculus L95–118]`
- 原文：warning（sin⁻¹ vs (sin)⁻¹ 兩行對照）＋ multipleChoice：哪個記號代表 sin 在 [−π/2,π/2] 的反函數。
- 擬改寫（記號陷阱，正面要求區分；本書行文用 arcsin，此題刻意並陳兩記號）：
  > Explain the difference between \(\sin^{-1}(x)\) and \((\sin x)^{-1}\). Which one does the
  > notation \(\arcsin x\) stand for? Evaluate both at \(x=1\) to illustrate the difference.
- 建議：收。對應 CONTENT_SPEC §9 的 notation-trap 要求。

**2. C1.2-B** `[source: CLP-1 §2.12 #1]` `prob_s2.12.tex:14`
- 原文：Give the domains of (a) `arcsin(cos x)` (b) `arccsc(cos x)` (c) `sin(arccos x)`。
- 官方解材：hint＋answer＋逐項詳解（(a) 全實數 (b) nπ (c) [−1,1]）。
- 擬改寫：照原文；(b) 維持但在 import 時標為較難（排序靠後）。
- 建議：收。值域→定義域的鏈式思考，正中本節要害。

**3. C1.2-C** `[source: CLP-1 §2.12 #2]` `prob_s2.12.tex:38`
- 原文：粒子 t=10 起算、高度 cos t。True or false: the particle has height 1 at `t=arccos(1)`。
- 官方解材：hint＋answer＋詳解（arccos 只回主值 0，不在運動時段內）。
- 擬改寫：照原文（變數與時點不動）。
- 建議：收。主值範圍的「反例式」理解，全場最好的 principal-range 題。

**4. C1.2-D** `[source: Stitz-Zeager via Mooculus 10_06_ex_131-154.tex]`（CC BY-NC-SA）
- 原文：14 小題求精確值清單（sin(arccos(−½))、cos(arctan √7)、sec(arctan 10)…）。
- 擬改寫（依矩陣建議選 5，由易到難）：
  > Find the exact value of each expression.
  > (a) \(\sin\bigl(\arccos(-\tfrac12)\bigr)\)  (b) \(\cos\bigl(\arcsin(-\tfrac{5}{13})\bigr)\)
  > (c) \(\tan\bigl(\arccos(-\tfrac12)\bigr)\)  (d) \(\cos\bigl(\arctan\sqrt{7}\bigr)\)
  > (e) \(\sec(\arctan 10)\)
- 建議：收。計算主力；(a)(c) 用特殊角、(b)(d)(e) 用三角形法，正好銜接下一題。

**5. 裁量 C（建議版）** `[source: Mooculus inversesTrig7]`（CC BY-NC 3.0；取前半，導數部分捨棄）
- 原文：Use a right triangle to find `cos(tan⁻¹(5))=1/√26`；再對 x>0 一般化 `cos(tan⁻¹(x))=1/√(1+x²)`（後半接導數，不取）。
- 擬改寫：
  > Use a right triangle to find the exact value of \(\cos(\arctan 5)\). Then, for \(x>0\),
  > use the same triangle idea to show \(\cos(\arctan x)=\dfrac{1}{\sqrt{1+x^2}}\).
- 建議：收這個當三角形法主題（比 C1.2-F 乾淨：它本來就是 pre-derivative 題）。

**6. 裁量 C（CLP 版，與上題擇一或並收）C1.2-F** `[source: CLP-1 §2.12 #16]` `prob_s2.12.tex:374`
- 原文：`Show that d/dx{sin(arctan x)} = (x²+1)^{−3/2}`——hint／解答的前半正是三角形化簡 `sin(arctan x)=x/√(x²+1)`，後半是求導。
- 擬改寫（只取化簡半）：
  > Draw a right triangle to simplify \(\sin(\arctan x)\) for \(x>0\), and check your answer at
  > \(x=\sqrt{3}\) using special angles.
- 建議：可收可不收（與上題同型；若兩題都收，§1.2 變 8 題仍在帶內）。改寫幅度較大（從導數題拆出），由你裁量。

**7. C1.2-E** `[source: CLP-1 §2.12 #5]` `prob_s2.12.tex:155`
- 原文：`f(x)=arcsin x + arccsc x`，求 domain（差異化部分問 differentiable，捨棄）。
- 官方解材：hint＋answer＋詳解（domain = {±1}）。
- 擬改寫：
  > Let \(f(x)=\arcsin x+\arccsc x\). Find the domain of \(f\), and evaluate \(f\) at every
  > point of that domain.
- 建議：收。其餘四個反三角函數定義域的點睛題（答案出乎意料地小）。

---

## §1.3 The Limit of a Function（擬 7 題）

**1. C1.3-D(i)** `[source: CLP-1 §1.3 #1]` `prob_s1.3.tex:12`【圖：連續波形＋x=2 處空心/實心點】
- 原文：Given the function shown below, evaluate (a) lim_{x→−2} f(x) (b) lim_{x→0} f(x) (c) lim_{x→2} f(x)。
- 官方解材：answer＋詳解（(c)＝2，「我們忽略 x=2 那一點的值」——hole 上方、實值在下方）。
- 擬改寫：照原文。附圖重畫。
- 建議：收。第一題就讓「極限≠函數值」可視化。

**2. C1.3-D(ii)** `[source: CLP-1 §1.3 #2]` `prob_s1.3.tex:45`【圖：x=0 處左右兩支斷開】
- 原文：evaluate lim_{x→0} f(x)（答 DNE，左右不一致）。
- 擬改寫：照原文。附圖重畫。
- 建議：收。為 §1.4 單側極限埋線。

**3. C1.3-A** `[source: CLP-1 §1.3 #4]` `prob_s1.3.tex:119`
- 原文：Draw a curve y=f(x) with lim_{x→3} f(x)=f(3)=10。
- 擬改寫：照原文。
- 建議：收。構造題（學生畫圖，無附圖成本）。

**4. C1.3-B** `[source: CLP-1 §1.3 #5]` `prob_s1.3.tex:147`
- 原文：Draw a curve with lim_{x→3} f(x)=10 and f(3)=0。（hint：函數不必連續）
- 擬改寫：照原文。
- 建議：收。與上題成對。

**5. C1.3-C** `[source: CLP-1 §1.3 #6, #7]` `prob_s1.3.tex:184,195`（兩題併一題兩問）
- 原文：T/F: lim_{x→3} f(x)=10 ⟹ f(3)=10？／T/F: f(3)=10 ⟹ lim_{x→3} f(x)=10？（皆 false）
- 擬改寫：
  > True or false — justify each answer with a sketch or a counterexample.
  > (a) If \(\lim_{x\to 3}f(x)=10\), then \(f(3)=10\).
  > (b) If \(f(3)=10\), then \(\lim_{x\to 3}f(x)=10\).
- 建議：收。本節核心辨析。

**6. C1.3-E** `[source: CLP-1 §1.3 #10, #12, #16]` `prob_s1.3.tex:244,264,311`（三題併一題三問）
- 原文：lim_{t→0} sin t／lim_{y→3} y²／lim_{x→3} 1/10。
- 擬改寫：
  > Evaluate each limit. If you are unsure, sketch the function first.
  > (a) \(\lim_{t\to 0}\sin t\)  (b) \(\lim_{y\to 3}y^2\)  (c) \(\lim_{x\to 3}\dfrac{1}{10}\)
- 建議：收。輕計算；(c) 常數極限是隱形地雷。

**7. C1.3-F** `[source: CLP-1 §1.3 #17]` `prob_s1.3.tex:325`
- 原文：piecewise `sin x (x≤2.9) / x² (x>2.9)`，求 lim_{x→3} f(x)（答 9；hint：只看 3 附近）。
- 擬改寫：照原文。
- 建議：收。「極限只看局部」的妙題，收尾兼過渡到 §1.4。

---

## §1.4 One-Sided and Infinite Limits（擬 9 題）

**1. C1.4-A(i)** `[source: CLP-1 §1.3 #8]` `prob_s1.3.tex:209`
- 原文：f 定義在全 ℝ，lim_{x→−2} f(x)=16，問 lim_{x→−2⁻} f(x)（答 16）。
- 擬改寫：照原文。
- 建議：收。

**2. C1.4-A(ii)** `[source: CLP-1 §1.3 #9]` `prob_s1.3.tex:222`
- 原文：lim_{x→−2⁻} f(x)=16，問 lim_{x→−2} f(x)（答：資訊不足）。
- 擬改寫：照原文，加 `Explain what additional information would settle the question.`
- 建議：收。與上題成對，雙向不對稱是重點。

**3. 移入：讀圖題** `[source: CLP-1 §1.3 #3]` `prob_s1.3.tex:71`【圖：三段斜線、多處空心點】
- 原文：五小問——lim_{x→−1⁻}、lim_{x→−1⁺}、lim_{x→−1}、lim_{x→−2⁺}、lim_{x→2⁻}（答 2/−2/DNE/0/0）。
- 矩陣原放 §1.3；本檔裁定移入 §1.4（通篇單側）。
- 擬改寫：照原文。附圖重畫。
- 建議：收。單側極限的讀圖主力。

**4. C1.4-B** `[source: CLP-1 §1.3 #11, #13, #14, #15]` `prob_s1.3.tex:254,275,285,299`（四題併一題四問）
- 原文：lim_{x→0⁺} log x＝−∞／lim_{x→0⁻} 1/x＝−∞／lim_{x→0} 1/x＝DNE／lim_{x→0} 1/x²＝∞。
- 擬改寫（log 改 ln 以合 §9 notation）：
  > Evaluate each limit, writing \(\infty\), \(-\infty\), or DNE where appropriate, and explain
  > the difference between the last two answers.
  > (a) \(\lim_{x\to 0^+}\ln x\)  (b) \(\lim_{x\to 0^-}\dfrac1x\)
  > (c) \(\lim_{x\to 0}\dfrac1x\)  (d) \(\lim_{x\to 0}\dfrac{1}{x^2}\)
- 建議：收。DNE vs ±∞ 記號規約一次講清（(c)(d) 對照是 CLP 原版設計，解答互相引用）。

**5. C1.4-C** `[source: CLP-1 §1.4 #39]` `prob_s1.4.tex:778`
- 原文：Evaluate lim_{x→0}(3+|x|/x)（答 DNE；解附完整分段展開＋圖）。
- 擬改寫：照原文。
- 建議：收。**已自 §1.5 的 cluster 移除以免重複（勘誤 1）。**

**6. C1.4-D(i)** `[source: CLP-1 §1.4 #29]` `prob_s1.4.tex:572`
- 原文：lim_{r→−5} r/(r²+10r+25)（答 −∞；分母 (r+5)² 恆正、分子趨 −5）。
- 擬改寫：照原文。
- 建議：收。符號分析入門。

**7. C1.4-D(ii)** `[source: CLP-1 §1.4 #31]` `prob_s1.4.tex:609`
- 原文：lim_{x→0} (x²+2x+1)/(3x⁵−5x³)（答 DNE；左右一正一負）。
- 擬改寫：照原文。
- 建議：收。與上題對照：分母零次方奇偶決定 ±∞ 還是 DNE。

**8. C1.4-E** `[source: CLP-1 §3.6.1 #1]` `prob_s3.6.1.tex:11`
- 原文：f(x)=g(x)/(x²−9)。True or false: f 在 x=−3 有 vertical asymptote。（答：一般而言 false；g(x)=x+3 即反例）
- 擬改寫：照原文。
- 建議：收。「分母為零⇏鉛直漸近線」的概念警示，正對 caution 環境的精神。

**9. C1.4-F** `[source: CLP-1 §3.6.1 #4]` `prob_s3.6.1.tex:155`（改寫幅度中）
- 原文：Find all asymptotes of f(x)=x(2x+1)(x−7)/(3x³−81)（垂直 x=3＋水平 y=2/3）。
- 擬改寫（水平漸近線超出本節範圍，裁掉）：
  > Find all vertical asymptotes of \(f(x)=\dfrac{x(2x+1)(x-7)}{3x^3-81}\), and verify each one
  > by computing the relevant one-sided limits.
- 建議：收。官方解的垂直段照搬可用；水平段在 import 紀錄中註明「未用」。

---

## §1.5 Limit Laws and Computational Techniques（擬 14 題）

**1. C1.5-A** `[source: CLP-1 §1.4 #1]` `prob_s1.4.tex:11`
- 原文：lim f=0、lim g=0，四個極限哪些可直接算？（f/2、2/f、f/g、fg；答：f/2 與 fg）
- 擬改寫：照原文，要求逐項說明依據哪條 limit law、哪些為何失效。
- 建議：收。開場概念題，「0/0 不是 0 也不是 1」。

**2. 裁量 D（追加，矩陣未列）C1.5-J** `[source: CLP-1 §1.4 #2, #5]` `prob_s1.4.tex:28,66`
- 原文：#2 構造 f,g 使兩者極限為 0 且 f/g→10（答例 f=10(x−3), g=x−3）；#5 問 lim f/g 可能值（任意實數／±∞／DNE）。
- 擬改寫（兩題併一題）：
  > Suppose \(\lim_{x\to 3}f(x)=\lim_{x\to 3}g(x)=0\). (a) Find functions \(f\) and \(g\) with
  > \(\lim_{x\to 3}\dfrac{f(x)}{g(x)}=10\). (b) What are all possible values of
  > \(\lim_{x\to 3}\dfrac{f(x)}{g(x)}\)?
- 建議：收。reasoning 缺格最強的補位題（indeterminate form 的本質）；因不在矩陣候選列，標為追加，由你定奪。

**3. 直接代入 cluster** `[source: CLP-1 §1.4 #6, #8, #19]` `prob_s1.4.tex:90,114,297`（三併一）
- 原文：lim_{t→10} 2(t−10)²/t＝0／lim_{x→3}((4x−2)/(x+2))⁴＝16／lim_{t→2} ½t⁴−3t³+t＝−14。
- 擬改寫：三小問一題，指示 `Evaluate using the limit laws; justify the key step.`
- 建議：收。（#7 cos 分母版略去：cos 在 §1.2 後可用但增益小，留 import 彈性。）

**4. 因式分解 (i)** `[source: CLP-1 §1.4 #16]` `prob_s1.4.tex:240` — lim_{x→4}(x²−4x)/(x²−16)＝1/2。照原文。收。
**5. 因式分解 (ii)** `[source: CLP-1 §1.4 #17]` `prob_s1.4.tex:259` — lim_{x→2}(x²+x−6)/(x−2)＝5。照原文。收。
**6. 因式分解 (iii)** `[source: CLP-1 §1.4 #28]` `prob_s1.4.tex:547` — lim_{w→5}(2w²−50)/((w−5)(w−1))＝5。照原文（解答有「兩函數僅差一點故極限相等」的關鍵說明，import 全收）。收。

**7. 有理化 (i)** `[source: CLP-1 §1.4 #20]` `prob_s1.4.tex:310` — lim_{x→−1}(√(x²+8)−3)/(x+1)＝−1/3。照原文。收。
**8. 有理化 (ii)** `[source: CLP-1 §1.4 #24]` `prob_s1.4.tex:424` — lim_{t→1}(3t−3)/(2−√(5−t))＝12（共軛乘在分母側）。照原文。收。

**9. 絕對值 (i)** `[source: CLP-1 §1.4 #40]` `prob_s1.4.tex:825` — lim_{d→−4}|3d+12|/(d+4)＝DNE。照原文。收。
**10. 絕對值 (ii)（反差題）** `[source: CLP-1 §1.4 #41]` `prob_s1.4.tex:866` — lim_{x→0}(5x−9)/(|x|+2)＝−9/2（什麼怪事都沒發生）。照原文。收。

**11. Squeeze (i)** `[source: CLP-1 §1.4 #25]` `prob_s1.4.tex:450`
- 原文：lim_{x→0} −x²cos(3/x)＝0。官方解含「為何不能用乘法律」與書寫規範叮嚀，import 全收。
- 擬改寫：照原文。收。
**12. Squeeze (ii)** `[source: CLP-1 §1.4 #34]` `prob_s1.4.tex:666`
- 原文：lim_{x→1}(x−1)²sin[((x²−3x+2)/(x²−2x+1))²+15]＝0（「裡面多可怕都不用管」）。
- 擬改寫：照原文。收。（#27 x sin²(1/x) 的單側界版本較難，不入正選；import 紀錄列為備選。）

**13. 方法選擇 (i)** `[source: CLP-1 §1.4 #42]` `prob_s1.4.tex:884` — 已知 lim_{x→−1} f(x)=−1，求 lim (xf(x)+3)/(2f(x)+1)＝−4。照原文。收。
**14. 方法選擇 (ii)** `[source: CLP-1 §1.4 #43]` `prob_s1.4.tex:898` — 求常數 a 使 lim_{x→−2}(x²+ax+3)/(x²+x−2) 存在（a=7/2，順帶算出極限 1/6）。照原文。收。壓軸。

**15. 應用（選收）C1.5-H** `[source: CLP-1 §1.4 #47]` `prob_s1.4.tex:1198`
- 原文：白球位置 s(t)、紅球 2s(t)；白球 t=1 速度 5，問紅球速度（用 §1.2 的速度定義＋limit laws；答 10）。
- 擬改寫：照原文（速度定義引用改為本講義對應節）。
- 建議：收則 §1.5 為 15 題（帶內上緣）；其 applied 格唯一候選。預設收。

（C1.5-I 圖像題 `§1.4 #45` 依矩陣標 optional，不入正選；import 紀錄列為備選。）

---

## §1.6 The Precise Definition of a Limit（擬 7–8 題）

**1. C1.6-A** `[source: APEX §1.2 #1]` `01_02_ex_01.tex`
- 原文：What is wrong with the following "definition" of a limit?（給一個 ε/δ 順序顛倒、蘊含方向反置的假定義；官方答案點出兩處錯誤）
- 擬改寫：照原文。
- 建議：收。邏輯結構題，全場最好的 ε-δ 概念題。

**2. C1.6-B** `[source: APEX §1.2 #2]` `01_02_ex_02.tex`
- 原文：Which is given first in establishing a limit, the x-tolerance or the y-tolerance?（答：y）
- 擬改寫：照原文＋`Explain why the order matters.`
- 建議：收。

**3. C1.6-C(i)** `[source: APEX §1.2 #3]` `01_02_ex_03.tex` — 證 lim_{x→2} 5＝5（官方完整 ε-δ 證明）。照原文（`Prove, using the precise definition…`）。收。
**4. C1.6-C(ii)** `[source: APEX §1.2 #12]` `01_02_ex_12.tex` — 證 lim_{x→4}(2x+5)＝13（線性，δ=ε/2）。照原文。收。
（#4 `3−x→−2` 負斜率版列備選。）

**5. C1.6-D** `[source: APEX §1.2 #5]` `01_02_ex_05.tex`
- 原文：證 lim_{x→3}(x²−3)＝6——需局部界 2<x<4、δ=ε/7（官方證明完整含界的推導）。
- 擬改寫：照原文。
- 建議：收。本節主菜（auxiliary bound）。（#13 `2x²+3x+1→6` 同型，列備選／挑戰。）

**6. C1.6-E** `[source: APEX §1.2 #8]` `01_02_ex_08.tex`
- 原文：證 lim_{x→0} sin x＝0，hint 給 |sin x|≤|x|（官方證明 δ=ε 一行收尾）。
- 擬改寫：照原文。
- 建議：收。用已知不等式餵 ε-δ，連到 §1.5 squeeze 的味道。

**7. C1.6-F** `[source: CLP-1 §1.6 #7, #8]` `prob_s1.6.tex:110,125`（兩題併一題；continuity preview）
- 原文：T/F: f 在 t=5 連續 ⟹ 5 在定義域內（真）；T/F: lim=17 且連續 ⟹ f(5)=17（真）。
- 擬改寫：
  > Suppose \(f\) is continuous at \(t=5\). True or false — justify briefly:
  > (a) \(t=5\) is in the domain of \(f\).  (b) If moreover \(\lim_{t\to 5}f(t)=17\), then \(f(5)=17\).
- 建議：收（若認為 continuity preview 不該配題，去掉此題即 6 題，仍在帶內）。

**缺口 A（uniqueness of limits）**——題庫無乾淨候選。建議 AI 出一題引導式：
> Suppose \(\lim_{x\to a}f(x)=L\) and \(\lim_{x\to a}f(x)=M\) with \(L\ne M\). Apply the precise
> definition with \(\varepsilon=\tfrac{|L-M|}{2}\) to both limits and derive a contradiction.
（出題後照 `[source: AI]` 標記＋你審核。）

**缺口 B（precise infinite-limit definition）**——建議不練：§1.4 已有非正式無限極限操作，
此處正式版（∀M ∃δ…）在本講義層級屬 prose/theorem 即可，硬配題會超綱。

---

## 你裁決之後的 import pass（預告）

1. `gen_standalone.py` 增 Ch 1 重生支援（從 `example-ch01/` 生成，與 ch2/3 同路徑；除非你選手改）。
2. 各節在 `</article>` 前插入 `Exercises` 區塊（`env-exercise`、節內從 1 重編、`[source:]` 留 HTML 註解）。
3. 重畫 ~5 幅附圖進 `figures.js`（遵 redundant-encoding）。
4. 建 `ch01_exercise-imports.md`：每題收錄官方 hint／answer／solution 全文＋授權標記＋改寫紀錄（含未用的解答段與備選題）。
5. 重生 standalone 兩版，瀏覽器驗渲染，更新 coverage matrix 為「已 import」狀態。
