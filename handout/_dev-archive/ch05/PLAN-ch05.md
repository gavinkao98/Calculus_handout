# PLAN-ch05 — Chapter 5: Applications of Differentiation

Chapter-level direction anchor + cross-session state. **First manuscript-free chapter.**

## Workflow (manuscript-free, autonomous)

- **Spine = canon** (Stewart ET 9e Ch4 primary; Thomas 14e / Rogawski 4e cross-check), authored to full-gate tier. No teacher manuscript exists Ch5–16.
- **Provenance:** each fragment carries a `<!-- section-source: … -->` header naming the canonical section(s) it is built from; pedagogical add-ons keep the `expansion:<cat>` tag system.
- **Human gates → Codex** (user 2026-07-06 autonomy grant: "決策點自行調用 codex 討論到收斂再實行，不用再問我"). So ③ direction gate and ⑤ advisory review both run against **Codex** (read-only, standing consent), not the user. Per section: draft against the brief + hypothesis ledger → Codex adversarial review (direction-conformance + math correctness + hypothesis hygiene) → iterate to 0 blocking.
- **Anti-hallucination backstops** (replacing the lost ①-verify): (1) the section brief + hypothesis ledger reviewed before/at draft; (2) Codex adversarial; (3) the math double-gate (sympy recompute worked examples) at chapter end. Codex noted sympy checks numbers, not theorem hygiene — hence the **hypothesis ledger** per section (domains, continuity/differentiability assumptions, denominator ≠ 0, endpoint type, exported deps).
- **Depth:** standard-rigorous (roadmap). Applications are computation-led; the one real theorem (L'Hôpital) is fully proved from a Generalized MVT introduced in §5.7.

## Roster (Codex-reordered; roadmap "全局 seam ledger")

| § | Title | new machinery | key imports |
|---|---|---|---|
| 5.1 | Implicit Differentiation | implicit-diff framework (closes Ch3 open-q) | chain rule **Thm 3.3** |
| 5.2 | Related Rates | \(dy/dt\) | §5.1; chain rule |
| 5.3 | Linear Approximation & Differentials | \(L(x)\), \(dy\) vs \(\Delta y\) | derivative **Def 2.2**; remainder-form **Def 3.1** |
| 5.4 | Maximum and Minimum Values | critical numbers, closed-interval method, 1st-deriv test | **EVT 4.9(a)**, **Fermat 4.10**, **monotonicity Cor 4.3** |
| 5.5 | Optimization Problems | applied extrema | §5.4 |
| 5.6 | Shape of a Graph | concavity, inflection, **2nd-deriv test** (NEW) | **MVT 4.12**, Cor 4.3 |
| 5.7 | L'Hôpital's Rule | **Generalized MVT (Cauchy's form)** lemma + indeterminate forms | **MVT 4.12** |
| 5.8 | Curve Sketching | synthesis + asymptotes | §5.4–5.7; infinite limits **Def 1.11** |
| 5.9 | Newton's Method | Newton iteration | §5.3; **IVT 4.9(b)** (root existence) |

Excluded (roadmap): antiderivatives (→Ch6), graphing-with-technology.

## Cross-chapter EXPORT (forward contract; keep exact)

- **Generalized MVT (Cauchy's form)** §5.7 → Ch11 Taylor remainder.
- **Linear approximation / differentials** §5.3 → Ch6 (\(du\)), Ch11, Ch14 tangent planes.
- **Concavity / 2nd-derivative test** §5.6 → Ch14 Hessian (§C.4).

## Per-section seam / fence guards (from full-arc Codex seam-hunt)

- **§5.1:** do NOT state the general \(F_x/F_y\) implicit-function formula (needs Ch14 partials) — operational/branch-based; assume the implicitly-defined quantity is differentiable where the method is used. Re-derive an inverse-function derivative (e.g. \(\arcsin'\), \(\ln'\)) via the framework — connects to Ch3's composition-identity route.
- **§5.3:** cross-ref Ch3 remainder-form differentiability (Def 3.1) — linear approximation is that idea, not wholly new.
- **§5.6:** 2nd-derivative test — state clearly; the test is inconclusive when \(f''=0\) (caution).
- **§5.7:** name the lemma "Generalized Mean Value Theorem (Cauchy's form)" (avoid clash with the Cauchy criterion, Thm 4.5). Fully prove the clean \(0/0\) finite case; \(\infty/\infty\) and \(x\to\infty\) — prove one carefully-stated extension or fence to Proof-Track (hypothesis sprawl risk, not truth). Make explicit: indeterminate forms beyond \(0/0,\infty/\infty\) (\(0\cdot\infty,\ \infty-\infty,\ 1^\infty,\ 0^0,\ \infty^0\)) via algebraic recasting.
- **§5.8:** all asymptote types incl. slant; growth comparison \(\ln x \ll x^p \ll e^x\).
- **§5.9:** convergence/failure discussion benefits from §5.6 concavity; may cite IVT 4.9(b).

## Numbering ledger (Ch5 counters reset fresh; per-type continuous across sections)

**Fill as each section reaches draft.** Cautions are UNNUMBERED (Ch1–4 convention).

| type | allocated so far | next |
|---|---|---|
| Definition | — | 5.1 |
| Theorem | — | 5.1 |
| Proposition | — | 5.1 |
| Corollary | — | 5.1 |
| Lemma | — | 5.1 |
| Strategy | — | 5.1 |
| Example | — | 5.1 |
| Figure | — | 5.1 |
| Remark | — | 5.1 |

> Chapter opener (chapter-head + "By the end…") lives in **sec-5-1.html** (first `<article>`), per handout convention (four chapters + appendices all do this).

## Per-section status

**Mode A (draft + ⑤ Codex) COMPLETE 2026-07-06 — all 9 sections + Appendix D §D.3.** Each section: build ✔ / linebreak-gate 0 / render katex 0 / Codex ⑤ 0 blocking (advisories applied). Full-chapter sweep: linebreak 0/0 (ch05+appD), katex 0, math=917.

| § | stage | env minted | Codex ⑤ |
|---|---|---|---|
| 5.1 Implicit Differentiation | ✅ draft | Strategy 5.1; Ex 5.1–5.4 | 0 blocking, 3 adv applied |
| 5.2 Related Rates | ✅ draft | Strategy 5.2; Ex 5.5–5.7 | 0 blocking (clean) |
| 5.3 Linear Approx & Differentials | ✅ draft | Def 5.1–5.2; Ex 5.8–5.10 | 0 blocking, 3 adv applied |
| 5.4 Max and Min Values | ✅ draft | Def 5.3–5.4; Thm 5.1 (FDT); Strategy 5.3; Ex 5.11–5.13 | 0 blocking, 2 adv (FDT proof rigor) applied |
| 5.5 Optimization | ✅ draft | Strategy 5.4; Ex 5.14–5.16 | **1 blocking** (5.16 quarter-not-half) fixed + adv |
| 5.6 Shape of a Graph | ✅ draft | Def 5.5–5.6; Thm 5.2 (Concavity), 5.3 (2nd-deriv); Ex 5.17–5.18 | 0 blocking, 3 adv (proof rigor) applied |
| 5.7 L'Hôpital's Rule | ✅ draft | Thm 5.4 (Generalized MVT), 5.5 (L'Hôpital); Strategy 5.5; Ex 5.19–5.21; **+appD §D.3** | **2 blocking** (§D.3 reduction, x^x=Ex 3.10 not 3.7) fixed + adv |
| 5.8 Curve Sketching | ✅ draft | Def 5.7 (asymptotes); Strategy 5.6; Ex 5.22–5.23 | 0 blocking, 3 adv applied |
| 5.9 Newton's Method | ✅ draft | Strategy 5.7; Ex 5.24–5.25; **chapter summary** | **2 blocking** (cubic has Cardano; summary EVT/Fermat) fixed + adv |

**Final numbering ledger (as-built, updated 2026-07-07):** Definition 5.1–5.7 · Theorem 5.1–5.5 · Strategy 5.1–5.7 · **Example 5.1–5.27**（M4 新增 5.14＝FDT on x^{3/5}(4−x)、5.22＝ln x/x at 0⁺；舊 5.14–5.20→5.15–5.21、5.21–5.25→5.23–5.27 一次 cascade）· **Figure 5.1–5.11**（M2 圖批次 2026-07-07，tier-1/2 全採）· Corollary/Proposition/Lemma/Remark: none in Ch5（另 +2 個 M4 unnumbered enrichment：§5.3 Leibniz-notation intuition、§5.8 asymptote-crossing caution）. Appendix D grew to §D.1–§D.3 (Lemma D.1; proofs of Thm 4.9(a)/(b), Thm 5.5 ∞/∞).

**Gate status (2026-07-06):** ✅ 逐節 Codex ⑤（0 blocking；5 blocking 沿途修）· ✅ **sympy 數學閘 33/33 PASS** · ✅ **章層 Codex review**（0 blocking，5 cross-section adv 套）· ✅ **圖機會閘**（13 候選：essential 6/strong 5/med 3/low 2，駁 6；見 `handout/_audit/REVIEW-ch05-figure-opportunity.html`）。
**剩餘（後續 session，較大、宜 fresh context）：** 圖**繪製**＋圖正確性閘 D1–D8（採 tier-1/2 候選）· math M1–M8 gate-2（依 PIPELINE 風險判準：Ch5 屬標準嚴謹章＝抽樣層）· S·A·V＋難度 learner-sim（PIPELINE M3 合一輪）· Mode C 條件式 gap-check（PIPELINE M4）。

## Gate-family checklist（與 `handout/PIPELINE.md` dashboard 同步；2026-07-07 制）

| 閘家族 | 狀態 | 日期／備註 |
|---|---|---|
| M1 Mode A′（brief＋⑤＋sympy＋章層 review） | ✅ | 2026-07-06；5 blocking 沿途修 |
| M2 圖機會（候選） | ✅ | 2026-07-06；13 候選 |
| M2 圖繪製＋D1–D8 | ✅ | 2026-07-07；tier-1/2 共 11 張（Figure 5.1–5.11）；gate-1 **blocking=0, advisory=0**（自檢修 7 缺陷後送審）；視覺 gate-2 依頻率矩陣＝出版前抽樣 |
| 數學 M gate-2（跨模型） | ✅ | 2026-07-07；Ch5 作抽樣層樣本章全章複核：**1 blocking [M7]**（M4 新增 caution 的 VA 絕對化陳述）→ 修＋scoped 回歸「解除、無新問題」→ **blocking=0**；紀錄 `ch05_math-gate2-audit.md` |
| M3 散文 S·A·V＋難度 learner-sim（合一輪） | ✅ | 2026-07-08（新 session 重跑，分兩批避額度牆）；**blocking=0**：散文 gate-1 三組 0 blocking（36 tighten／14 opt／2 voice 全 advisory）＋難度盲測 ×3 全 **0 blocking／0 B 類違規**。難度曲線均值 §5.1→5.9＝2.7/3.0/3.2/3.7/3.2/3.3/**4.0(§5.7 尖峰)**/3.2/2.5，尖峰 4<Ch4 §4.2 的 4.5、全章<4 → 無弧線層異常。**1 客觀修復落地**：P1-12（§5.3 Leibniz 段「single symbol」caution 誤引 Remark 3.2→改「a caution in §2.2」＋同步修註解）＋scoped §5.3 回歸「0/0/0/0、無新問題」。彎撇號-as-prime 經隔離渲染證實 render-safe→另開衛生 chip；ch02 §2.2「we do not do in this book」被 Def 5.2 推翻→另開跨章 chip。合併裁決稿 `_audit/REVIEW-ch05-prose-difficulty.html`；S·A·V gate-2 依頻率矩陣＝非高風險章不跑 |
| M4 Mode C gap-check（①②合一） | ✅ | 2026-07-07；偵察 Layer-1=0；Codex 裁決 **ADOPT 4**（Ex 5.14、Ex 5.22、§5.3 intuition、§5.8 caution）／DEFER 5；sympy 驗證＋scoped Mode B 過；報告 `_audit/REVIEW-ch05-modec-gapcheck.html`、imports `ch05_example-imports.md` |
| M5 收尾（dashboard＋ROADMAP open-q） | ✅ | 2026-07-08；PIPELINE dashboard Ch5→「全閘完成（canon 首例）」、本 checklist M3/M5→✅、ROADMAP Ch5 弧線 entry 補 gates-complete＋M3 難度曲線一行＋Open questions 收（無懸而未決方向叉路） |

## Chapter opener — "By the end of this chapter you will be able to"

- use implicit differentiation to find \(dy/dx\) for curves defined by an equation;
- solve related-rates problems by differentiating a relation with respect to time;
- use linear approximation and differentials to estimate values and bound errors;
- locate absolute and local extrema, and solve optimization problems;
- determine concavity and inflection points, and apply the first- and second-derivative tests;
- evaluate limits of indeterminate form with L'Hôpital's rule;
- sketch a curve from its analytic features;
- approximate a root with Newton's method.
