# Codex gate-2 raw：ch02 散文平實化回填（合併 sweep）逐條裁決

- **調用**：`codex exec -s read-only`（stdin 餵 UTF-8 prompt、`-o/--output-last-message` 收檔；材料**全 inline**、未讓 Codex 讀檔——遵循 2026-06-28 編碼坑紀律），codex-cli 0.144.1，模型走 `~/.codex/config.toml` 預設 **gpt-5.6-terra**。
- **日期**：2026-07-26。**授權**：使用者本輪明示「跑 Gate 2」（`CLAUDE.md` 2026-07-01 Codex 唯讀逐次徵詢條款）。
- **受審材料**（prompt 109.9 KB）：gate-1 走查的 100 條改點（前→後全句）＋ `CONTENT_SPEC.md` §3〈平實英文條款〉RC 條款節錄 ＋ `PROSE-AUDIT-RUBRIC.md` R 維度與擋稿線 ＋ 已裁詞彙先例 ＋ **ch02 provenance 背景（含推翻「手稿章」前提的 Gate 0 實測）** ＋ 逐節量測與段落層數據 ＋ 判 KEEP 的 2 對 ＋ 四對四步仲裁邊界案 ＋ 「刻意不動」七項清單 ＋ 本輪範圍五節的**完整散文**（canonical stream 逐段，289 段）＋ Q1–Q7。
- **走查稿**：[`REVIEW-ch02-plain-walk.html`](REVIEW-ch02-plain-walk.html)；**整合裁決與執行結果**：`REVIEW-ch02-plain-applied.html`（Gate 3 後產出）。
- 本檔為 **raw 輸出照登**（未刪改一字）。折入時的逐條處置（含我未完全照抄 Codex 措辭的地方與理由）記在 applied 報告與該輪 commit body。

**摘要**：`VERDICT: ADOPT 74 / MODIFY 25 / REJECT 1`。

三個值得特別記下的結果：

1. **唯一 REJECT 是 `P22`**——Codex 判它應 KEEP（成對 dash 只修飾同一個 power-rule 操作的適用範圍），正是 gate-1 自己標為「四步③下 KEEP 可成立」的四對邊界案之一。另三對（`P05`／`P17`／`P20`）Codex 同意重寫。
2. **Q6 抓到三處精確性問題**，其中 `P15` 是 gate-1 改寫**引入**的真缺陷（把 \(h \ne 0\) 的 scope 暫時鬆開，使正性主張涵蓋 \(h = 0\)）；`S20` 則是**課文原有**的不精確（把可微等同於「有一個確定的切線方向」，與 §2.3 自己的 vertical tangent 例子牴觸）；`S41` 的 `no extra constant` 應為 `constant factor`。
3. **Q5（未改處）抓到一條 R blocking**：§2.5 章摘要末段的 `lie outside their reach` 與 `no rule here touches` 是該範圍結論的唯一載體，兩者都是比喻——gate-1 漏掉。另有約十條 advisory 級的未改處（`grazes the curve`、`in hand` ×2、`play the same trick`、`sanity check`、`buys us`、`claims that this pattern never breaks` 等）。

---

VERDICT: ADOPT 74 / MODIFY 25 / REJECT 1

### A. 單破折號尾巴

- S01 ADOPT — `so` 已完整標示結果關係，逗號足夠。
- S02 ADOPT — `but` 已標示對比，改逗號自然。
- S03 ADOPT — 後段是清楚的名詞同位語。
- S04 MODIFY — 逗號同位語略彆扭，改稿：`If you zoom in on the curve at \(a\), the curve looks increasingly like its tangent line.`
- S05 MODIFY — `This` 不能精確指向「rotation」；改稿：`The tangent slope at \(P\) is therefore \(2\), the value the secant slopes converge to. Figure 2.1 shows the secant lines approaching the tangent as their slopes converge to \(2\).`
- S06 MODIFY — AFTER 保留了交易隱喻 `traded`；改稿：`In each case, local linearity uses a straight-line approximation near a point of interest to simplify a curved problem. That is the practical value of local linearity.`
- S07 MODIFY — 公式與「正是 difference quotient」是同一動作，不宜機械拆句；改稿：`Over the short interval from \(t\) to \(t+h\), the car’s average velocity is the change in position divided by the elapsed time: \(\bigl(s(t+h) - s(t)\bigr)/h\), exactly the difference quotient of §2.1.`
- S08 ADOPT — 「關心每一時刻」與「把 velocity 視為 function」可分開教。
- S09 ADOPT — 定義句與等價讀法分開，指涉清楚。
- S10 ADOPT — 計算便利性與 symbolic-point 的程序說明是兩個動作。
- S11 ADOPT — 逗號後的 `precisely` 同位語自然。
- S12 ADOPT — \(x>0\) 條件仍完整，域的結論另句合理。
- S13 ADOPT — 「未計算」與「已知 \(f'\) 後解輸入」可獨立成立。
- S14 ADOPT — 圖形核對與三段符號描述分句更清楚。
- S15 MODIFY — `The slope and the rate of change` 容易把 interpretation 與 quantity 混同；改稿：`The slope interpretation and the rate-of-change interpretation are two ways of reading the same limit: \(f'(x)\) measures how fast the output of \(f\) changes per unit change in the input, whether that output is read as a height (slope) or a position (velocity).`
- S16 ADOPT — acceleration 的定義與前瞻 §2.3 是可分的教學動作。
- S17 ADOPT — `but` 已承擔對比。
- S18 ADOPT — 保住 `Informally` gloss，只改清單接法。
- S19 ADOPT — 幾何結論獨立後更醒目。
- S20 MODIFY — 原 AFTER 仍把 differentiability 說成「有一個 tangent direction」，與 vertical tangent 的 finite-limit 要求不夠精確；改稿：`If \(f\) is differentiable at \(a\), its difference quotient approaches one finite value, so the tangent line has a finite slope. A jump or any other discontinuity prevents such a finite limit, so differentiability implies continuity.`
- S21 ADOPT — 與全書 run-in label 體例一致。
- S22 ADOPT — 同 S21。
- S23 ADOPT — `and` 連接的兩個子句可用逗號。
- S24 ADOPT — 定義與身體經驗的例子是不同教學動作。
- S25 ADOPT — 記號否定與其字面解釋分開正確。
- S26 ADOPT — 名詞同位語清楚。
- S27 MODIFY — AFTER 還留有 `tie`／`in place` 的比喻性搭配；改稿：`Now that we have introduced differentiability, its connection to continuity, and higher-order derivatives, we turn in the next sections to rules that make differentiation <em>efficient</em>. These rules are systematic shortcuts that avoid computing each derivative from the limit definition.`
- S28 ADOPT — `computed ... the slow way` 與 `working ... out in full` 已是直白說法。
- S29 MODIFY — 公式 payload 不必拆成新句；改稿：`In each one, the exponent becomes a multiplier and the power decreases by one, giving \(n\,x^{n-1}\).`
- S30 MODIFY — `same question` 指涉偏虛；改稿：`The factorization argument, by contrast, uses no infinitesimal at all. It establishes the same result using ordinary algebra.`
- S31 ADOPT — `which` 明確回指常數 \(1\)／其斜率。
- S32 ADOPT — \(x\ne0\) 留在主結論中，沒有遺失 scope。
- S33 MODIFY — 兩句只是同一個因果 payload，且 AFTER 留有 `did all the work`；改稿：`No limit was computed: the rules give the result directly without returning to the limit definition.`
- S34 ADOPT — 計算結果與後設核對是獨立動作。
- S35 ADOPT — 課前知識的可能性與「不假定」的保證可分句。
- S36 ADOPT — `infinite sum` 與 `power series` 的命名仍完整。
- S37 ADOPT — 暫借結果與 Caution 指路是不同動作。
- S38 ADOPT — `on credit` 與其既有 gloss 保留，冒號適合交付 gloss。
- S39 ADOPT — `only on` 的限制範圍清楚。
- S40 MODIFY — `This is again the fact that` 不自然，且 `differentiated away` 未完全字面化；改稿：`The polynomial part eventually becomes zero under repeated differentiation, while the \(e^{x}\) term remains unchanged at every step. This again shows that \(e^{x}\) is its own derivative.`
- S41 MODIFY — `no extra constant` 應明說是 factor；改稿：`Notice that the extra factor \(\ln b\) equals \(1\) precisely when \(b = e\). This is another way to see why base \(e\) is the natural choice: only for that base does the derivative equal the original exponential with no extra constant factor.`
- S42 ADOPT — 公式陳述與操作指令確為兩個動作。
- S43 ADOPT — 缺少何種規則與反例提醒可分開。
- S44 MODIFY — `behave just as simply, with ...` 仍偏鬆散；改稿：`It is tempting to hope that products and quotients obey equally simple derivative rules, and in particular that the derivative of a product is the product of the derivatives.`
- S45 ADOPT — 代數兩項與 Figure 2.9 對應可獨立表述。
- S46 ADOPT — 公式與兩種 marginal-revenue effect 應分開。
- S47 ADOPT — 補回 `the two terms`，消除 dangling modifier。
- S48 ADOPT — 具體 \(1/x\) 例子與一般 quotient rule 的歸納可分開。
- S49 ADOPT — 鬆散同位語改逗號合適。
- S50 ADOPT — run-in label 一致。
- S51 ADOPT — run-in label 一致。
- S52 ADOPT — 直接命名「dropping the square」更清楚。

### B. 成對插入語

- P02 ADOPT — 首見 `increment` 的 gloss 與「不是 input」分開後仍完整。
- P03 ADOPT — 具體應用與 local-linearity 指認各有獨立教學用途。
- P04 ADOPT — 消除模糊的 `move we just made`。
- P05 ADOPT — 等價讀法有獨立用途，且改稿修復 `slope ... at that point` 的 scope。
- P06 ADOPT — 記號設定與後續 limit 程序分開合理。
- P07 ADOPT — 清單型插入語改括號符合 CUT palette；後段定理事實可另句。
- P08 ADOPT — 操作指令、三步模式與結果是不同動作。
- P09 ADOPT — `operator` 的首見釋義完整保留，記號理由另句。
- P10 MODIFY — `it recalls` 仍近似擬人；改稿：`The notation was chosen to reflect that the derivative is defined as the limit of the quotient \(\Delta y / \Delta x\). But until those parts are defined on their own (which we do not do in this book), read \(dy/dx\) as one indivisible name for \(f'(x)\).`
- P12 ADOPT — roadmap 中「何時存在」與後兩項工作可分開。
- P13 ADOPT — theorem 的內容與 higher derivatives 的延伸是不同工作。
- P14 MODIFY — `This happens when` 容易誤作窮盡所有 failure mode；改稿：`When it cannot, the function is <em>not</em> differentiable at that point. This can happen when the left-hand and right-hand limits disagree or when the quotient grows without bound.`
- P15 MODIFY — AFTER 的 `whatever the sign of \(h\)` 暫時鬆開 \(h\ne0\) scope，對 \(h=0\) 不正確；改稿：`For every \(h \ne 0\), \(h^{2/3} = \bigl(h^{1/3}\bigr)^{2} > 0\), because the square of a nonzero cube root is positive. Therefore the quotient is always positive.`
- P16 ADOPT — 兩個例子的 one-sided-limit 對照可分句。
- P17 ADOPT — dash 本身可保留，但整句確有兩個 notation 說明；分句合理。
- P18 ADOPT — 四項清單置括號是明示規則的直接適用。
- P19 ADOPT — 個別例子與一般 formula 是不同教學動作。
- P20 ADOPT — 插入語不只給條件，也說明以 logarithm 定義的構造；移入主幹後 \(x>0\) scope 更安全。
- P21 MODIFY — `come straight out` 與 `business of` 仍不夠字面；改稿：`Notice that differentiation distributes over addition and that a constant factor remains outside the derivative. Multiplication does not behave so simply. In general, \((fg)' \ne f'g'\), so the correct rule for a product requires more care. Section 2.5 gives that rule.`
- P22 REJECT — 原成對 dash 只修飾同一個 operation 的適用範圍，四步③應 KEEP；改成 `and using` 不必要地把它變成第二個操作。
- P23 MODIFY — `which is the case` 指涉鬆；改稿：`For \(4\sqrt{x}\), the exponent \(\tfrac{1}{2}\) is not an integer, a case for which the Caution above defers a general proof. This particular derivative has already been established: §2.2 Example 2.7 found \(\dfrac{d}{dx}\sqrt{x} = \dfrac{1}{2\sqrt{x}}\) straight from the definition.`
- P24 ADOPT — 規則的兩個 literal 操作已直接說出。
- P25 ADOPT — 移除 `governs the world`，因果內容保留。
- P26 ADOPT — 真分式的理由與 quotient-rule 適用分開清楚。
- P27 ADOPT — 改掉模糊的 `the skill ... organizes`。
- P28 ADOPT — \(x\ne0\) 同時約束化簡等式與後續 rule 選擇。
- P29 ADOPT — composition 的命名、形式與 chain rule 前瞻分開。
- P30 ADOPT — 純重複再命名可安全併入主幹。
- P31 ADOPT — `linearity` 首見說明已併進名詞片語。
- P32 MODIFY — 應同時去掉 `business of Chapter 3`；改稿：`Both are addressed in Chapter 3, which begins with the chain rule for compositions and uses it to extend the power rule and to differentiate the trigonometric, logarithmic, and inverse functions.`

### C. 詞彙層

- R01 ADOPT — `hugs` 的曲線擬人已換成字面距離關係。
- R02 ADOPT — `shows a direct link` 比 `exposes a vivid link` 更中性明白。
- R03 ADOPT — `requires` 是規範指定的中性動詞。
- R04 MODIFY — `come on` 仍偏口語；改稿：`engineers keep it small when designing elevators and trains so that changes in acceleration are gradual rather than abrupt.`
- R05 ADOPT — `long row of primes` 是 literal gloss。
- R06 MODIFY — `that repetition` 指涉略空；改稿：`This section ends the need to repeat that calculation.`
- R07 ADOPT — 規則、性質與結論都改為字面表述。
- R08 ADOPT — 兩個 proof 的關係說得直接。
- R09 ADOPT — `quick to apply` 足以替代 reflex，未改動數學內容。
- R10 MODIFY — `behave simply` 仍是空泛評價；改稿：`Each rule follows directly from the corresponding limit law of Chapter 1.`
- R12 MODIFY — `used constantly` 太絕對；改稿：`This corollary is used frequently in kinematics.`
- R13 ADOPT — `different kind` 是直白類別說法。
- R14 ADOPT — 導數如何得到已改為字面程序。
- R15 MODIFY — AFTER 仍保留 `singles out`；改稿：`That same slope-equals-height rule characterizes \(e^{x}\) among exponential functions. For this reason, it is called the <em>natural</em> exponential: at every point its rate of change equals its current value.`
- R16 ADOPT — degree 與 unchanged 的描述清楚。
- R17 MODIFY — `differentiation behaves simply` 仍空泛；改稿：`In §2.4 we learned the addition rule for derivatives: the derivative of a sum is the sum of the derivatives, and the same holds for differences (Theorem 2.4).`
- R18 ADOPT — 已去除 earn 隱喻。
- R19 ADOPT — `proved` 精確替代 `secured`。

### Q1

有：S07、S29、S33 的原 AFTER 都把單一公式／因果 payload 機械拆成兩句。我已改回單句。其餘拆句大致都有可獨立辨識的教學動作；不會形成三句等長、等節奏的連續散文。

### Q2

有一處實質 scope 問題：P15 的 AFTER 先說「a cube root squared is positive whatever the sign of \(h\)」，會暫時涵蓋 \(h=0\)。我的改稿把 `For every \(h\ne0\)` 放到整個正性主張前。

其餘指定點安全：

- S12：\(f'\) 的 \(x>0\) 條件仍在前句完整說出。
- S32：`wherever \(x\ne0\)` 仍直接約束 power-rule 延伸。
- P20：`every \(x>0\)` 已移入一般命題主幹。
- P28：\(x\ne0\) 仍約束等式與「simplifies first」的結論。

### Q3

(a) P01、P11 都應 KEEP。P01 是同一趨近條件的符號重述；P11 是規則明列允許的對比修飾。

(b) 邊界案：

- P05：重寫。`equivalently ...` 是可獨立使用的第二種讀法，且原句切開了 `slope ... at that one point`。
- P17：重寫。dash 單獨可 KEEP，但全句確有 expression 意義與 superscript 意義兩個教學動作。
- P20：重寫。它包含 \(x>0\) 條件外，還含以 logarithm 定義 \(x^r\) 的構造說明。
- P22：KEEP。只是同一個 power-rule 操作的範圍修飾，沒有第二個獨立教學動作。

(c) 30 對重寫中，P22 是唯一我判其實應 KEEP 的成對 dash。其餘重寫均有定義、理由、例外、指令、完整事實或清單等獨立功能。

### Q4

沒有一條原始 R1 finding 是「無證據的純同義詞美化」：每條都能指出隱喻、交易語彙、戲劇性動詞、空泛評價或不透明搭配。

但若照原 AFTER 直接採用，S06、S27、S33、S40、S41、S44、P10、P21、P32、R04、R06、R10、R12、R15、R17 仍有殘留的比喻、空泛性或不精確性，所以我改為 MODIFY。

沒有動到 §3-protected 的 `Informally, ...` gloss、連接詞、`we`、`jump`，或 `on credit` 機制用語。

### Q5

有漏項；其中一項達 R blocking。

- R blocking：§2.5 [2-5-¶50] 的 `outside their reach`／`no rule here touches` 是節末範圍結論的唯一載體，兩者都是比喻。應改為：`These rules do not yet cover two things: composition \(f\bigl(g(x)\bigr)\), for which this chapter has not given a rule, and the power rule for noninteger exponents.` 後句可接我在 P32 的改稿。

其他是 advisory，但建議補：

- §2.1 [2-1-¶01]：`principal payoff of that machinery` 與 S06 已處理的 `practical payoff` 同族；可改 `The main use of those limit methods...`。
- §2.1 [2-1-¶02]：首見 tangent-line 的 `grazes the curve` 對 EFL 讀者不夠直白；可改為 `the line through that point whose direction matches the curve there`。因後面有正式 limit 定義，未達 blocking。
- §2.2 [2-2-¶10]：`the single formula delivers` 可改 `the single formula gives`；[2-2-¶20] 的 `run forward ... backward ... buys us` 應改為明說「由 input 求 slope，及在可能時由 prescribed slope 求 input」。
- §2.3 [2-3-¶04]：`The definition asks`／`settle on a single value` 可改為 `The definition requires the difference quotient to approach one finite value`。
- §2.4 [2-4-¶08]：`The power rule claims that this pattern never breaks` 應改為 `The power rule states that the formula holds for every positive integer \(n\)`。
- §2.4 [2-4-¶47]：若保留 \(y'=ky\)，最好明說 \(k\) 是 constant，並以 \(Ce^{kx}\) 補足「built from \(e^x\)」；這是 R2 清晰度補強。
- §2.5 [2-5-¶10]、[2-5-¶36] 的兩個 `in hand` 應一致改為 `established` 或 `available`；[2-5-¶20] 的 `play the same trick` 改為 `use the same algebraic step`；[2-5-¶27] 的 `sanity check` 改為受保護且更直白的 `As a check`.

第六節的刻意不動項中，1–5 都正確；6、7 的段落結構也可保留，只需上述局部詞彙補修，無須拆段。

### Q6

有三個需修正的精確性問題：

- P15 如上，\(h\ne0\) scope 在原 AFTER 中被鬆開。
- S20 的原 AFTER 把 differentiability 等同於「one definite tangent direction」，但 §2.3 已以 vertical tangent 說明：有幾何 tangent 方向不代表 derivative 的 finite limit 存在。我已改成 finite-value／finite-slope 的說法。
- S41 的 `no extra constant` 應為 `no extra constant factor`，避免把 multiplier 誤讀成 additive constant。

除此以外，我未發現候選改寫改動公式、量詞、條件、編號或 cross-ref；P20、P28、S12、S32 的域條件在修訂後都保持正確。

### Q7

兩個段落都可 KEEP：

- §2.1 的 173 詞 lead 是連貫的 chapter roadmap，不需為字數拆段。
- §2.4 的 137 詞開場也是單一轉場／roadmap；雖預告 polynomial rules 與 \(e^x\)，尚不足以要求拆段。

但不宜立成「chapter lead 不套 ≥150 詞觸發器」的全書豁免。較好的先例是：chapter lead 仍觸發人工判讀，但只要它維持一個連貫的 overview 動作、順序清楚、沒有混入獨立證明或操作指令，就可以保留。這樣可一致處理 ch04、ch06、ch07 的長 lead，而不把字數規則誤變成自動拆段規則。
