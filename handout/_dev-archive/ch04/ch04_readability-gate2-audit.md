# Ch4 可讀性回填 — gate-2（Codex）原始輸出轉錄

> 本檔為**版控紀錄**：gate-2 原始輸出落 gitignored scratchpad、換機即失，依 `handout/PIPELINE.md`「findings 留版控」轉錄於此。對應審核稿 `handout/_audit/REVIEW-ch04-readability-gate2.html`。2026-06-28。

## Run 設定

- **模型／CLI：** PATH 上的 `codex`（`codex-cli 0.136.0`，登入 ChatGPT 走訂閱配額）；`~/.codex/config.toml`：`model="gpt-5.5"`、`model_reasoning_effort="xhigh"`、`service_tier="default"`。
- **指令（逐節，Bash、prompt 經 stdin 餵 raw UTF-8）：** `codex exec -s read-only -C <repo> --output-schema schema.json -o out-<sec>.json - < prompt-<sec>.txt`
- **硬紀律：** 每節 fragment（**套用 gate-1 5 條後的定稿版**）以 UTF-8 clean-inline 餵入，**絕不讓 Codex 用 `-C` 自讀 fragment**（本機自讀會把 UTF-8 解成亂碼＝假陽性）。先一節 smoke test 驗 schema／編碼，再續跑其餘。
- **編碼驗收：** 5 節輸出 JSON 各 **U+FFFD = 0**（編碼正常）。
- **檢查項：** ① reader-persona first-read ＋ ② introduce-before-use（與 gate-1 同兩條，跨模型獨立、prompt 未餵 gate-1 findings）。fragment 為套用後版本，故 gate-2 同時擔任「抓 gate-1 套用迴歸」之用。

| 節 | token | findings | U+FFFD |
|---|---|---|---|
| sec-4-1 | 19,049 | 2 | 0 |
| sec-4-2 | 35,598 | 4 | 0 |
| sec-4-3 | 14,411 | 1 | 0 |
| sec-4-4 | 23,252 | 1 | 0 |
| sec-4-5 | 27,862 | 3 | 0 |
| **合計** | **120,172** | **11** | **0** |

全章共 11 raw findings，全 tier 1–2、0 blocking、0 structural-reorder。下方為逐節原始 JSON 萃取（未經 triage 的 Codex 原話）；四級 triage 裁決見 HTML 審核稿。

## sec-4-1　§4.1 Construction of the Exponential Function

**reader_note：** Overall this is unusually clean for a first rigorous construction: the main proof path is motivated, but two small first-read snags remain where a nonessential term and a compressed tail-bound step arrive without enough local support.

**findings（2）：**

### sec-4-1-1　[reader-persona / U3 / Slowed / tier 2]
- **locus：** paragraph immediately before displayed bound (*)
- **verbatim_quote：** `bounding each term by \(x^{n}/n! \le L^{n}/n!\) and repeating the geometric collapse from the proof gives, for \(k > n_{0}\),`
- **what_stalls：** The displayed estimate starts at the k-th tail, but the text says only to repeat the earlier collapse. A first reader may not see why the bound becomes \(L^{k}/k!\), rather than reusing the older \(L^{n_0}/n_0!\) as the leading term.
- **minimal_unstick（add one because/bridge clause）：** Add one bridge clause such as: “starting the same ratio argument at the index \(k\)” before the displayed bound.

### sec-4-1-2　[introduce-before-use / U4 / Minor / tier 2]
- **locus：** paragraph after the definition of e
- **verbatim_quote：** `The number \(e\) is known to be both irrational and transcendental, though we prove neither fact here.`
- **what_stalls：** “Transcendental” is not standard precalculus vocabulary and is not glossed. Since it is only a historical aside, an L2 first reader may pause on a term that is not needed for the argument.
- **minimal_unstick（local gloss）：** Add a brief appositive gloss: “transcendental, meaning not a root of any nonzero polynomial with integer coefficients.”

**clean_checks：**
- Chapter and section openers clearly frame the role reversal: the series is now a definition, not a borrowed property.
- Completeness is introduced before it is used, with an informal explanation and a concrete ℝ-vs-ℚ contrast.
- Theorem 4.2’s geometric-tail proof is locally motivated by Strategy 4.1 and does not require lowering the rigor.
- The notation P_k(x), the tail estimate (*), and the later use of (*) are introduced in a usable order.
- No structural introduce-before-use issue requiring reorder was found.

## sec-4-2　§4.2 Continuity and the Exponent Law for e^x

**reader_note：** 整體首讀可跟；主要摩擦集中在 subsequence 未先定義，以及指數律證明中幾個可用一句 because／量詞橋接補齊的地方。

**findings（4）：**

### sec-4-2-1　[introduce-before-use / U4 / Slowed / tier 1]
- **locus：** Theorem 4.4 (Bolzano–Weierstrass), statement
- **verbatim_quote：** `Every bounded sequence of real numbers has a convergent subsequence.`
- **what_stalls：** subsequence 是首次作為正式術語使用，但本節此前沒有定義「從原序列取遞增指標的一串項」。precalc/L2 首讀者會知道結論想說有一部分項收斂，卻未必能立即解析後面的 \(a_{p_j}\)、\(a_{n_j}\) 記法。
- **minimal_unstick（local gloss）：** 在 theorem statement 或前一句加就地 gloss："subsequence (a sequence formed by choosing terms with increasing indices)"。

### sec-4-2-2　[reader-persona / U3 / Slowed / tier 2]
- **locus：** Theorem 4.5 proof, Cauchy ⇒ convergent paragraph, sentence choosing \(n_j\)
- **verbatim_quote：** `Given \(\varepsilon > 0\), choose \(N_{0}\) with \(\lvert a_{m} - a_{n} \rvert < \varepsilon/2\) for \(m, n \ge N_{0}\), and choose an index \(n_{j} \ge N_{0}\) with \(\lvert a_{n_{j}} - A \rvert < \varepsilon/2\).`
- **what_stalls：** 這一句同時要求同一個 subsequence term 滿足 \(n_j\ge N_0\) 與接近 \(A\)。理由是 subsequence 指標會無界增長且 \(a_{n_j}\to A\)，但當下沒有說出來。
- **minimal_unstick（because bridge）：** 改成「choose \(j\) large enough that both \(n_j\ge N_0\) and \(\lvert a_{n_j}-A\rvert<\varepsilon/2\)」。

### sec-4-2-3　[reader-persona / U3 / Slowed / tier 2]
- **locus：** Theorem 4.7 proof, Step 1: two estimates
- **verbatim_quote：** `Also \(\lvert e^{y} \rvert \le \sum_{n=0}^{\infty} \lvert y \rvert^{n}/n! = e^{\lvert y \rvert} \le e^{L}\), and likewise \(\lvert P_{k}(x) \rvert \le e^{L}\).`
- **what_stalls：** \(e^{\lvert y\rvert}\le e^L\) 和 \(\lvert P_k(x)\rvert\le e^L\) 看起來像在使用尚未證明的 monotonicity of \(e^t\)。可重建的真正理由是非負項的逐項比較，但這個 because 沒有落在使用處。
- **minimal_unstick（because bridge）：** 加一句或括號：「since \(0\le \lvert x\rvert,\lvert y\rvert\le L\) and the comparison is term-by-term with nonnegative terms」。

### sec-4-2-4　[reader-persona / U3 / Slowed / tier 2]
- **locus：** Theorem 4.7 proof, Step 6 heading
- **verbatim_quote：** `Step 6: let \(k \to \infty\), then \(L \to \infty\).`
- **what_stalls：** 前面是固定 \(x,y\) 後選一個 \(L\)，估計真正需要的是在固定 \(L,n_0\) 下令 \(k\to\infty\)，再用「每個固定 pair 都落在某個 bounded interval」推到全體。標題的 \(L\to\infty\) 會讓首讀者疑惑 \(n_0>8L\) 是否也要跟著變。
- **minimal_unstick（scope clarification）：** 把標題或首句改為「let \(k\to\infty\) with \(L,n_0\) fixed; then let the bounded interval be arbitrary」。

**clean_checks：**
- §4.1 已建立的 \(P_k\)、\((*)\)、Theorem 4.1/4.2 在本節使用前都有足夠回指。
- Cauchy sequence 的正式定義後立刻有 Informally 重述，對 ε-δ 形式沒有過度簡化。
- Bolzano–Weierstrass 的 peak 證明先定義 peak 再分情況使用，線性順序清楚。
- 絕對收斂用於延拓 \(e^x\) 的動機清楚；\((** )\) 的角色在後文使用前已說明。
- 指數律 Step 2–4 的重整、binomial collapse 與 (II) tail 分組有足夠局部標記。

## sec-4-3　§4.3 The Derivative of e^x

**reader_note：** The core proof reads cleanly on a first pass; the only avoidable snag is in the final forward-looking modelling hook, where new ODE notation arrives faster than the local gloss.

**findings（1）：**

### sec-4-3-1　[introduce-before-use / U4 / Slowed / tier 2]
- **locus：** Final summary paragraph, first sentence after Corollary 4.2 proof
- **verbatim_quote：** `The identity \(\frac{d}{dx} e^{x} = e^{x}\) — slope equal to value at every point — is exactly the property that makes the exponential the natural model for any quantity whose rate of change is proportional to its current size: the relation \(y' = k\,y\), solved by \(y = y(0)\,e^{kt}\).`
- **what_stalls：** The modelling notation introduces \(k\), \(t\), \(y'\), and \(y(0)\) in one compressed clause. A first-time L2 reader can infer the broad idea from “rate of change is proportional,” but may not know whether \(k\) is a constant, why the variable switches from \(x\) to \(t\), or what role \(y(0)\) plays.
- **minimal_unstick（local gloss）：** Add a parenthetical local gloss, e.g. “where \(t\) is the input variable, \(k\) is a constant, and \(y(0)\) is the initial value.”

**clean_checks：**
- The difference-quotient reduction is introduced before use and tied explicitly to Theorem 4.7.
- The Proposition 4.2 proof supplies the missing algebraic and bounding steps, including the geometric comparison for the trailing sum.
- Theorem 4.8 uses the explicit bound in a first-readable way; no hidden epsilon-delta work is needed here.
- Higher-derivative notation is locally glossed by “Every higher derivative” and then proved by induction.
- Mean Value Theorem and Rolle’s theorem are framed as upcoming tools, not assumed prerequisites.

## sec-4-4　§4.4 Rolle's Theorem and the Mean Value Theorem

**reader_note：** 整體首讀路線清楚，主要定理鏈接與例題都已就地搭橋；我只看到一處會讓首讀者短暫卡住的局部術語摩擦。

**findings（1）：**

### sec-4-4-1　[introduce-before-use / U4 / Minor / tier 2]
- **locus：** Caution after Corollary 4.3, final sentence
- **verbatim_quote：** `The corollary is a sufficient test, not a characterisation.`
- **what_stalls：** “sufficient test” and “characterisation” carry precise one-way-versus-if-and-only-if meaning, but “characterisation” has not been introduced or glossed; an L2 precalc reader may not map it immediately to the false-converse warning just stated.
- **minimal_unstick（local gloss）：** Add a tiny local gloss, e.g. “not a characterisation (not an if-and-only-if test).”

**clean_checks：**
- Rolle → MVT 的輔助函數 g(x) 已先說明戰術目的，再進入計算，沒有憑空構造感。
- Theorem A 的左右差商符號翻轉逐步交代，代數與極限方向對首讀者可跟上。
- MVT hypotheses 的 closed/open asymmetry 在 Strategy 4.2 中已充分拆解，不需要再加 gloss。
- Example 4.3 的 existence-only 用法有明確提醒，不會要求讀者找出 c。
- Example 4.6 從每個閉區間推到全 ℝ 的步驟已有一句橋接與括號提醒，讀者不需自行補全。

## sec-4-5　§4.5 Monotonicity and the Logarithmic Function

**reader_note：** The section is mostly first-read friendly for a rigorous treatment; the remaining friction is concentrated in a few places where a proof-use or application claim is asserted faster than this persona can justify on the spot.

**findings（3）：**

### sec-4-5-1　[reader-persona / U3 / Slowed / tier 2]
- **locus：** Theorem 4.13 proof, first paragraph after the contradiction assumption
- **verbatim_quote：** `In either case the failure is witnessed by a sequence: there is a number \(\delta &gt; 0\) and points \(y_{j} \to x_{0}\) (all in \((0, \infty)\)) with`
- **what_stalls：** The jump from “not continuous” to a fixed positive gap plus a convergent violating sequence uses the sequential negation of continuity. A first linear reader may accept the statement but cannot reconstruct why this sequence exists without a bridge.
- **minimal_unstick（one-sentence proof bridge）：** Add one local bridge, e.g. “By the sequential form of failure of continuity, choose \(y_j\) within \(1/j\) of \(x_0\) while keeping the logarithm at least \(\delta\) away.”

### sec-4-5-2　[reader-persona / U3 / Slowed / tier 2]
- **locus：** Example 4.7, opening paragraph before the requested verifications
- **verbatim_quote：** `This agrees with the usual meaning when \(x\) is rational and extends it to all real \(x\).`
- **what_stalls：** The compatibility with rational powers is important because the chapter is closing the deferred question about arbitrary powers, but the claim is asserted before any check is shown.
- **minimal_unstick（local algebra bridge）：** Add a short parenthetical bridge: for \(x=m/n\), the new value has nth power \(a^m\), so it is the usual positive nth root.

### sec-4-5-3　[reader-persona / U1/U3 / Slowed / tier 2]
- **locus：** Why these functions are unavoidable, first paragraph
- **verbatim_quote：** `If \(y(t)\) obeys \(y'(t) = k\,y(t)\) for a constant \(k\), then \(y(t) = y(0)\,e^{kt}\) — the model behind population growth (\(k &gt; 0\)), radioactive decay (\(k &lt; 0\)), and continuously compounded interest.`
- **what_stalls：** For this persona, the differential-equation conclusion appears suddenly: checking that the displayed formula works is easy, but the “if … then” uniqueness step is not motivated or cited.
- **minimal_unstick（one-sentence motivation/citation bridge）：** Add a compact because-bridge, such as “indeed, differentiating \(y(t)e^{-kt}\) gives zero, so Corollary 4.4 makes it constant.”

**clean_checks：**
- Definition of \(\ln x\), its domain \(x>0\), and the inverse identities are introduced before use and reinforced by the caution.
- The derivative proof introduces \(y_0\) and \(y\), explains why division by \(y-y_0\) is legitimate, and ties the limit back to the known derivative of \(e^x\).
- The logarithm product law uses a locally defined auxiliary function and standard prior tools: chain rule, Theorem 4.14, and Corollary 4.4.
- Figure captions, cautions, and summary language do not create genuine introduce-before-use issues; specialized phrases are either standard in context or locally glossed.
- No structural reorder is needed.

---

## 四級 triage 裁決（Claude 對抗 verifier，11 條＋1 重跑）

> Codex raw 一律過四級 triage（gate-2 系統性偏嚴）。逐條由獨立 Claude verifier 複核：誠實重評 severity、查 no-dumbing、②是否 genuine、與 gate-1 已套用 5 條之交集。**結果：2 adopt / 5 optional / 4 reject、0 blocking、0 迴歸。** 對應審核稿 `handout/_audit/REVIEW-ch04-readability-gate2.html`。

| G2 | locus | check | 裁決 | 理由 |
|---|---|---|---|---|
| G2-1 | §4.1 (*) @G1-1 位置 | ① U3 | **reject** | over-gloss/dumbing；確認 G1-1 已完整、無迴歸 |
| G2-2 | §4.1 transcendental | ② U4 | **optional** | genuine ② 但 terminal history aside、無下游承載 → Minor/3 |
| G2-3 | §4.2 Thm4.4 subsequence | ② U4 | **optional** | genuine ② 但 peak 證明就地以遞增指標自構造 → Minor/3 |
| G2-4 | §4.2 Thm4.5 選 n_j | ① U3 | **optional** | 兩事實同段前句已給、Cauchy 標準 extraction → Minor/4，建議 leave |
| G2-5 | §4.2 Thm4.7 Step1 | ① U3 | **ADOPT** | e^|y|≤e^L 若讀成 e^t 單調＝循環（單調性 §4.4 才證）；正解為非負逐項比較。Minor/2，加固嚴謹非 dumbing |
| G2-6 | §4.2 Step6 標題 L→∞ | ① U3 | **optional** | body 已『Since L was arbitrary』；如採僅把標題 L→∞ 換 L arbitrary → Minor/3 |
| G2-7 | §4.3 forward-hook y'=ky | ② U4 | **reject** | 已白話 gloss、符號標準；§C-4 刻意輕量 hook，由 §4.5 capstone(G2-11) 承接。dumbing/越界 |
| G2-8 | §4.4 characterisation | ② U4 | **reject** | 同段 x^3 反例＋對舉 sufficient test 已 locally-glossed → tier-4 |
| G2-9 | §4.5 Thm4.13 sequential negation | ① U3 | **reject** | lead-in(line93)＋『witnessed by a sequence』＋就地不等式三重 scaffolding；提議近重述 → over-gloss |
| G2-10 | §4.5 Example4.7 rational-agreement | ① U3 | **optional** | 脈絡陳述、補驗屬 scope 擴張 → Minor/3，建議 leave |
| G2-11 | §4.5 capstone y'=ky | ① U1/U3 | **ADOPT** | capstone 未自證；fix 引本章 Corollary 4.4（複用 line200 的 (·)e^{-kt} 招）、補 §C-4 deferred 承諾。Slowed/2，高價值 |

**收斂結論：**

- **adopt 2：** G2-5（§4.2 防潛在循環論證——`e^{|y|}≤e^L` 改標明非負逐項比較，因 `e^t` 單調性要到 §4.4 才證）、G2-11（§4.5 capstone 補一句引 Corollary 4.4 自證 `y'=ky⟹y=y(0)e^{kt}`）。
- **跨模型確認 gate-1 5 條套用無迴歸**：gate-2 讀套用後文字，未在 G1-1/2/4/7/8 任一處發現問題；G2-1（G1-1 位置殘餘細節）被判 over-gloss reject ＝確認 G1-1 已完整。
- **G1-9（§4.5 ε/δ 命名與 §4.2 慣例相反）**：gate-2 讀同一 Theorem 4.13 證明**未獨立提出**此點 → 無跨模型佐證、gate-1 verifier 已評 Minor/rename-or-leave → **建議維持原樣（不改名）**。