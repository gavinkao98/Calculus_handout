# REPORT — ch04 散文平實化回填 Codex gate-2（round 1，raw 照登）

> 調用：`codex exec -s read-only`｜模型 `gpt-5.6-terra`／reasoning effort `max`｜2026-07-26
> 材料全部 inline 進 prompt（116KB；本機讓 Codex 自讀 fragment 會把 UTF-8 解成亂碼）。
> 對應走查稿：[`REVIEW-ch04-plain-walk.html`](REVIEW-ch04-plain-walk.html)。
> **本檔為 raw 照登，未經 triage。** 專案慣例：reasoning 模型偏 over-report，raw 不可直接吃，
> 須接四級 triage 後才進 Gate 3；triage 結果見 applied 報告。

---

VERDICT: 42 adopt, 41 modify, 1 reject, 13 new

## (1) 84 筆逐條裁決

### §4.1

- C4-01 — MODIFY。`used it freely` 仍含糊；改為：`We have already used the natural exponential function \(e^{x}\) many times. It appeared in Chapter 2, where we wrote down its power series, computed its derivative \((e^{x})' = e^{x}\) by a quick term-by-term argument, and used it. In Chapter 3, we used it again alongside its inverse \(\ln x\).`

- C4-02 — ADOPT。`explicit error bound` 直接說出可驗證的內容。

- C4-03 — MODIFY。新版仍保留 `road ... passes through` 的路徑隱喻；改為：`Before we define the logarithm, we need two existence theorems: Rolle’s theorem and the Mean Value Theorem. Later chapters use both in applications of the derivative.`

- C4-04 — MODIFY。`tools ... are finally built` 仍把「證明結果」藏在建造隱喻中；改為：`This is the book’s <em>foundation chapter</em>, where the results used on credit since Chapter 2 are finally proved. More of this chapter is proof than computation.`

- C4-05 — ADOPT。刪除評價性 `honestly` 後，數學事實完整保留。

- C4-06 — REJECT。這是與 K-01 同型的有效成對破折號：清單只是界定 `everything` 的範圍，且章首重述有導覽用途；不應因重複而刪去。

- C4-07 — MODIFY。`as it always has` 後掛且冗餘；改為：`the symbol \(a^{n}\) means the product of \(n\) copies of \(a\).`

- C4-08 — ADOPT。後段是獨立的證明義務，分句正確。

- C4-09 — MODIFY。`floor` 仍是視覺隱喻；改為：`The guarantee we use is that a non-decreasing sequence that is bounded above must approach a limiting value. The corresponding statement holds for a non-increasing sequence that is bounded below.`

- C4-10 — ADOPT。因果方向維持為「完備性質支撐各存在定理」，沒有把清單錯掛到 `property` 上。

- C4-11 — ADOPT。符合既定的交易動詞政策，且拆開讀者指令是恰當的。

- C4-12 — ADOPT。`main tool` 清楚且可與後文保持一致。

- C4-13 — MODIFY。界限控制的是誤差的上界，不是必然的實際「gap」；改為：`The tail bound \((*)\) shows that the error decreases geometrically. Each additional term reduces the displayed error bound by a factor of \(1/2\).`

### §4.2

- C4-14 — ADOPT。存在性改為明說，範圍由後面的冒號內容補足。

- C4-15 — ADOPT。避免把記號寫成會「承諾」性質的主體。

- C4-16 — ADOPT。`rests on` 在此是可預測的結構關係，已去除 `engine`。

- C4-17 — MODIFY。`steepest` 與 `convergence machinery` 仍不夠字面；改為：`A word about what is ahead. This is the most demanding section of the book so far. It introduces Cauchy sequences and the Bolzano–Weierstrass theorem, topics usually first met in a dedicated analysis course. It consists entirely of proofs, with no worked examples. What the rest of the book uses are four facts:`

- C4-18 — MODIFY。應與 C4-23 的具體名詞一致；將 `what this machinery buys` 改為：`how these results are used`.

- C4-19 — ADOPT。命令句另起一句，指涉清楚。

- C4-20 — MODIFY。`not fussing over` 仍口語；改為：`A convention used repeatedly in the proofs below is to allow a fixed number of \(\varepsilon\)-sized errors without tracking the exact constant.`

- C4-21 — ADOPT。`use` 是直接且穩定的動詞。

- C4-22 — MODIFY。新版少了「尾和可任意小」這個關鍵理由；第三案見 (3b)。

- C4-23 — ADOPT。直接讓兩項工具當主詞，避免抽象的 `machinery`。

- C4-24 — MODIFY。`use instead` 的替代對象不清楚；改為：`no monotonicity that we can use`.

- C4-25 — ADOPT。逗號後的 `only` 結構清楚，未拆散定義。

- C4-26 — MODIFY。`cluster` 在分析課也可能聯想到 cluster point；改為：`the terms eventually become close to one another:`。

- C4-27 — ADOPT。拆句後依賴關係仍在，且 `in another form` 已消除服裝隱喻。

- C4-28 — MODIFY。定理不會 `use` 一個現象；改為：`That is exactly the phenomenon described by the theorem.`

- C4-29 — ADOPT。量詞敘述與白話重述的範圍沒有斷裂。

- C4-30 — ADOPT。後段是完整的結果句，分句正確。

- C4-31 — ADOPT。與 C4-27 術語一致。

- C4-32 — MODIFY。`every link breaks` 仍把三個失敗的定理藏成隱喻；改為：`Over the rationals, none of these results holds. There are bounded \(\mathbb{Q}\)-sequences that are Cauchy yet converge to no rational number (for instance, the partial sums of \(\sum 1/n!\), which approach \(e\), a number noted in §4.1 to be irrational).`

- C4-33 — MODIFY。`The tail is the gap` 沒說清楚數學關係；改為：`The tail bounds the difference between the partial sums`.

- C4-34 — ADOPT。`two-sided tool` 已足夠字面。

- C4-35 — ADOPT。`on a larger scale` 是可預測的比較說法。

- C4-36 — MODIFY。`\((**)\) to send the errors to zero` 仍把界限擬人化；改為：`and use \((**)\) to show that the errors tend to zero.`

- C4-37 — MODIFY。新版仍有 `assemble`、`carries`、`collapsed` 等承載數學內容的隱喻；改為：`the terms of total degree \(\ell \le 2\) sum exactly to \(1 + (x + y) + \tfrac{(x + y)^{2}}{2} = P_{2}(x + y)\), which is group (I). The remaining terms \(\tfrac{x^{2} y}{2} + \tfrac{x y^{2}}{2} + \tfrac{x^{2} y^{2}}{4}\) form group (II). Notice that group (II) has an incomplete degree-\(3\) part. Neither factor contains a power higher than \(2\), so \(x^{3}\) and \(y^{3}\) are absent. Therefore group (II) can only be bounded by a tail in Step 4, not rewritten by the binomial theorem.`

- C4-38 — MODIFY。`The completeness of \(\mathbb{R}\) reappears at every level` 仍不字面；改為：`and Bolzano–Weierstrass (Theorem 4.4). Both the Cauchy criterion and Bolzano–Weierstrass ultimately depend on the completeness of \(\mathbb{R}\).`

- C4-39 — MODIFY。只改 `leans on` 而留下 `machinery` 不一致；改為：`which uses the same partial-sum argument`.

### §4.3

- C4-40 — ADOPT。主題提前且去除 `owed` 的交易隱喻。

- C4-41 — MODIFY。應保留有效的成對清單破折號，並改掉 `correct in spirit`；改為：`That argument gave the correct result, yet it used three properties — convergence, continuity, and the exponent law — that had not been established at the time. Now that all three are theorems, we can re-derive the formula from them.`

- C4-42 — ADOPT。鬆散同位語改逗號合理。

- C4-43 — MODIFY。兩個好處是同一個說明動作，且 `unlike ...` 是合格的對比插入語；改為：`The series shows why the limit is \(1\), and — unlike the Chapter 2 derivation — also gives a numerical bound on the rate of approach.`

- C4-44 — MODIFY。`pinned` 應改成界限語言；例子清單可保留成對破折號：`Here the deviation of \(\frac{e^{h}-1}{h}\) from \(1\) is at most \(\lvert h\rvert\). For ordinary differentiation, the qualitative statement suffices, but later arguments that must track the size of a derivative error — Taylor remainders and numerical estimates — use the explicit bound rather than the limit statement alone.`

- C4-45 — ADOPT。公式 gloss 已獨立成一個明確教學動作。

- C4-46 — ADOPT。定理名稱提前，語意完整。

### §4.4

- C4-47 — MODIFY。`promise` 仍保留被 SPEC 點名的擬人化；改為：`Section 4.3 ended with a claim that still needs proof:`

- C4-48 — MODIFY。`bridge` 仍未字面化；改為：`is a statement about the function across a whole interval. No result proved so far connects these two kinds of information. This section establishes that connection. The key result is the <em>Mean Value Theorem</em> (MVT)`

- C4-49 — MODIFY。`where maxima and minima can sit` 仍是擬人搭配；改為：`After one preparatory result about where maxima and minima can occur, we reach it in two steps. The first is <em>Rolle’s theorem</em>, the special case where the average slope is zero; the second is the MVT itself.`

- C4-50 — MODIFY。`skips no value` 是關鍵數學內容，應直說；改為：`On a closed interval, the answer is always yes. Just as importantly, a continuous function on an interval takes every value between two values that it attains.`

- C4-51a — MODIFY。新版的 `it needs them differently` 指涉鬆散；改為：`The two parts require different hypotheses.`

- C4-51b — ADOPT。理由與另一個例子分開，邏輯清楚。

- C4-51c — MODIFY。改為：`The Intermediate Value Theorem (b) requires only continuity on an interval:`。

- C4-51d — ADOPT。`both conclusions hold` 明確而不口語。

- C4-53 — ADOPT。符合 `earn` 的既定處置，讀者指令也已分離。

- C4-54 — MODIFY。新版漏掉常函數情形，且 `turn around` 仍只是圖像直覺；改為：`Rolle’s theorem combines the two results above. Under its hypotheses, a function with equal endpoint values is either constant or has an interior extremum. At that interior extremum, the derivative is zero.`

- C4-55 — ADOPT。同位語改逗號恰當。

- C4-56 — ADOPT。後段是獨立的證明順序說明。

- C4-57 — MODIFY。`the one later chapters use` 不當地排除了另兩個結果；改為：`Of the three, the MVT is used most often in later chapters. It converts information about \(f'\) at individual points into information about \(f\) on an interval. We use it whenever we make that conversion: immediately below to deduce monotonicity from the sign of \(f'\), and later in Taylor’s theorem and in error estimates.`

- C4-58 — ADOPT。`guarantees` 是規範建議的中性動詞。

- C4-59 — MODIFY。`satisfies this step` 不自然且指稱太弱；改為：`still satisfies the differentiability requirement.)`

- C4-60 — ADOPT。破折號後確為獨立結論。

- C4-61 — ADOPT。與 C4-58 一致。

- C4-62 — ADOPT。先給全域可微，再推出 MVT 的前提，數學上成立。

- C4-63 — ADOPT。逗號的 `only` 結構清楚。

- C4-64 — ADOPT。`so` 正確標出推論。

- C4-65 — ADOPT。章節導覽句拆開後自然。

- C4-66 — MODIFY。`such a passage` 沒有明說轉換是什麼；改為：`Passing from bounded intervals to all of \(\mathbb{R}\) does not preserve every property. For example, boundedness can be lost, but strict monotonicity is preserved.)`

- C4-67 — MODIFY。`set out to reach` 仍是旅程隱喻；改為：`That last example proves that \(e^{x}\) is strictly increasing, the result needed for the next section.`

### §4.5

- C4-68 — MODIFY。新版仍有 `makes all of this work`、`come free`，且錯把存在性也歸給嚴格單調性；改為：`A one-to-one function can be inverted. The inverse of the exponential is the <em>natural logarithm</em>. Strict monotonicity gives the required uniqueness: no value can come from two different exponents. After we show that the range of \(e^{x}\) is \((0,\infty)\), it gives an inverse for every positive input. Strict monotonicity is also needed in every later proof about that inverse. The continuity and differentiability of \(\ln\) do not follow automatically from the definition;`

- C4-69 — ADOPT。拆句後不會拆散假設，且 `This time` 的回指明確。

- C4-70 — MODIFY。應先限定 \(x>0\)，且要說明是 \(1+x\) 之後的項；改為：`For \(x > 0\), the terms after \(1+x\) in the series are positive, so \(e^{x} > 1+x\). Therefore \(e^{x} > t\) once \(x\) is large enough. Since \(e^{-x} = 1/e^{x}\) (Theorem 4.7), \(e^{x} < t\) once \(x\) is sufficiently negative.`

- C4-71 — ADOPT。這正是逗號加 `so` 的位置。

- C4-72 — ADOPT。尾掛分詞子句本身不是缺陷，改逗號即可。

- C4-73 — ADOPT。`statement that \(\ln\) is continuous` 比同位語清楚。

- C4-74 — MODIFY。句點把 \(\exists\delta\,\forall d\) 的量詞範圍切開；改為：`that no input-closeness requirement can meet: for every \(d > 0\), some point \(y\) with \(0 < \lvert y - x_{0} \rvert < d\) has \(\lvert \ln y - \ln x_{0} \rvert \ge \delta\).`

- C4-75 — ADOPT。逗號加 `so` 保持同一推論鏈。

- C4-76 — MODIFY。`silently assumes` 仍不字面；改為：`with the chain rule, which assumes that \(\ln\) is differentiable without first proving it. We can now prove the formula without that assumption.`

- C4-77 — MODIFY。`presupposes` 在此不必用較難的字；改為：`to \(e^{\ln x} = x\), a derivation that <em>assumes</em> \(\ln\) is differentiable`

- C4-78 — MODIFY。`companion` 與 `borderline case` 沒交代結論；改為：`The next result is another consequence of the Mean Value Theorem. It handles the case \(f' = 0\) on an interval, where the conclusion is that the function is constant.`

- C4-79 — ADOPT。例子改成完整計算句，清楚。

- C4-80 — MODIFY。`the one identity that holds` 容易誤讀成只有一條對數恆等式成立；改為：`The proof above establishes the product law. It does not justify the similar-looking formulas.`

- C4-81 — ADOPT。回指已清楚地另成一句。

- C4-82 — MODIFY。應明說常數為何是 \(y(0)\)，且避免 `forces`；改為：`then \(y(t) = y(0)\,e^{kt}\). To see this, note that \((y(t)e^{-kt})' = (y'(t) - k\,y(t))e^{-kt} = 0\). Corollary 4.4 therefore shows that \(y(t)e^{-kt}\) is constant; at \(t=0\), its value is \(y(0)\). This model describes population growth`

## (2) DASH-KEEP 五處

- K-01 — KEEP 正確。清單只具體化 `Every fact we want to use` 的量詞範圍，主幹完整，沒有另開理由或結論。

- K-02 — 不應 KEEP。手稿來源不是四步仲裁的豁免；插入語本身就是待使用的獨立定理敘述。改為：`We need a more flexible convergence result. If a series of absolute values converges, then the original series converges. Together with the uniform tail bound \((*)\) and a careful product argument, this result also yields the continuity of \(e^{x}\) and the exponent law.`

- K-03 — KEEP 正確。`through the binomial theorem` 僅修飾同一個重組動作的手段，移除後主幹與論證均完整。

- K-04 — KEEP 正確。`not at an endpoint` 是 `strictly inside` 的對比澄清，正是應保留的成對破折號類型。

- K-05 — KEEP 正確，就破折號而言清單只界定 `Everything this chapter built`。但 `built` 的詞彙問題另列為 N-13，應改成 `established`，不必移除這組破折號。

## (3) 重點問題

### (3a) §4.3 清成 0 是否過頭？

是。零不是節級目標；密度目標不能推翻逐處四步仲裁。至少下列三組應保留：

- C4-41：`— convergence, continuity, and the exponent law —` 是如 K-01 的清單式限定。
- C4-43：`— unlike the Chapter 2 derivation —` 是規範明定可保留的對比修飾。
- C4-44 第二組：`— Taylor remainders and numerical estimates —` 只是限定「哪些後續論證」，沒有另開一個推論。

相對地，C4-40、C4-44 第一個單破折號、C4-45、C4-46 都應改。正確做法是保留上述合格成對破折號，同時以全章 canonical prose stream 檢查密度，而不是把本節機械壓到零。

### (3b) C4-22 的數學直覺

原句：

> `the original series should converge too — its terms cannot accumulate any net oscillation that the absolute series has already shown to be summable.`

gate 1 新句：

> `the original series should converge too, since the absolute series already bounds the total size of all the later terms.`

原句不夠字面，`net oscillation` 也不是絕對收斂的精確理由。新版方向正確，但不足以推出收斂：一個「有限的全域上界」本身不會使部分和成為 Cauchy。真正需要的是絕對值級數的每個充分後段和都能任意小，並以三角不等式控制原級數部分和之差。

第三案：

> `the original series should converge too, because the sum of the absolute values in any sufficiently late tail can be made as small as we wish.`

這樣既保留直覺，也預告後面正式證明的核心不等式。

### (3c) 五處拆段

五處切點都正確，沒有把單一論證從中間切斷。

- P-01：先交代本章要建立什麼，再說需要哪些存在定理；是「目標」與「路線」的自然邊界。
- P-02：先總述兩部分需要不同假設，再分別給 EVT 與 IVT 的反例／條件；切點正確。
- P-03：先講嚴格單調性的概念角色，再給本節工作清單；是概念段與路線圖段的自然分界。
- P-04a：先提出值域目標與 IVT，再開始固定 \(t\) 的構造；正確。
- P-04b：先建立上下夾住 \(t\) 的點，再套 IVT 並用嚴格單調性得唯一性；`Pick points \(p < q\)` 雖依賴前段，但正是下一個證明步驟，不會斷鏈。

## (4) gate 1 漏掉的 findings

- N-01 — §4.1 開頭的 `read properties off it freely` 與 `turn that around` 都是不透明慣用語。改為：`When \(e^{x}\) first appeared, we treated its power series as a fact about an already-known function and inferred properties directly from it. In this chapter, we reverse that order.`

- N-02 — §4.1 的 `trap the tail ... inside a geometric series` 與 `Theorem 4.1 hands us the limit` 把操作藏成隱喻。改為：`The plan is to bound the tail of the series \(\sum x^{n}/n!\) by a geometric series. Once the tail is controlled, the partial sums are non-decreasing and bounded above, so Theorem 4.1 guarantees that they have a limit.`

- N-03 — §§4.1–4.2 的 `close in on` 應統一為 `approach`：例如 `the partial sums approach \(e^{x}\) at a geometric rate.` 這是 R1 與 R3 的共同問題。

- N-04 — §4.2 的 `bridge we need`、`without an explicit limit in hand`、`The hinge is` 應字面化。改為：`The equivalence between convergence and the Cauchy condition lets us prove that \(\sum a_n\) converges without first knowing its limit. The next result supplies the existence statement used in the proof.`

- N-05 — §4.2 的 `Step 5: telescope the difference.` 不但不透明，也不是通常意義的 telescoping。改為：`Step 5: insert and subtract the partial sums.`

- N-06 — §4.2 的 `extends verbatim` 對 EFL 讀者不透明。改為：`With it, the same proof, with the same estimates, works for every real base point.`

- N-07 — §4.3 的 `fed the series into the difference quotient`、`drop out`、`collapses onto one limit` 都承載操作。可改為：`Chapter 2 substituted the series into the difference quotient and observed that the terms after the leading term tend to \(0\) as \(h \to 0\).` 以及 `The derivative therefore reduces to a single limit at \(0\):`

- N-08 — §4.4 的 `The pattern is general: a function whose derivative never vanishes has at most one root` 漏掉 MVT 所需的區間與正則性條件。改為：`More generally, if \(f\) is continuous on an interval and differentiable in its interior, and \(f'\) is never zero there, then \(f\) has at most one root on that interval.`

- N-09 — §4.4 的 `The three results form a ladder` 是關鍵依賴關係的隱喻。改為：`Theorem A is used to prove Rolle’s theorem, and Rolle’s theorem is used to prove the MVT.`

- N-10 — §4.5 定義後的 `land on \(x\)` 位於術語首次說明處，應直說：`In words, \(\ln x\) is the exponent to which \(e\) must be raised to obtain \(x\).`

- N-11 — §4.5 Caution 的 `silently carries the assumption` 是域限制的關鍵位置。改為：`Every formula in this section that contains \(\ln x\) is understood to require \(x > 0\).`

- N-12 — §4.5 的 product-law 證明直接套 Corollary 4.4，沒有明說前提。應在 `Applying Corollary 4.4 ...` 前補：`On every closed interval contained in \((0,\infty)\), \(f\) is differentiable and hence continuous.`

- N-13 — 章末仍有 `Everything this chapter built` 與摘要中的 `underwrites everything`。前者可改為：`All the results established in this chapter — the series definition, the exponent law, the rigorous derivatives, the inverse construction — are needed to show that these formulas are well-defined.` 後者應以 `provides the basis for the later results` 取代。
