# PLAN-ch06 — Chapter 6: Integrals

Chapter-level direction anchor + cross-session state. **Second manuscript-free chapter; first full 5-milestone pilot** (Ch5 was the transitional M1-only chapter; Ch6 runs M1–M5 end to end, then the milestone sequence is reviewed and frozen — see [`../../PIPELINE.md`](../../PIPELINE.md)).

## Workflow (manuscript-free, autonomous)

- **Spine = canon** (Stewart ET 9e Ch5 primary; Thomas 14e / Rogawski 4e cross-check), authored to full-gate tier. No teacher manuscript exists Ch5–16.
- **Provenance:** each fragment carries a `<!-- section-source: … -->` header naming the canonical section(s) it is built from; pedagogical add-ons keep the `expansion:<cat>` tag system.
- **Human gates → Codex** (user 2026-07-06 autonomy grant). ③ direction gate and ⑤ advisory review both run against **Codex** (read-only, standing consent), not the user. Per section: draft against the brief + hypothesis ledger → Codex adversarial review (direction-conformance + math correctness + hypothesis hygiene) → iterate to 0 blocking.
- **Anti-hallucination backstops** (replacing the lost ①-verify): (1) the section brief + hypothesis ledger reviewed before/at draft; (2) Codex adversarial ⑤; (3) the math double-gate (sympy recompute worked examples) at chapter end. sympy checks numbers, not theorem hygiene — hence the **hypothesis ledger** per section (domains, continuity assumptions, endpoint type, exported deps).
- **Depth: 深理論核心 (Ch4-level — the highest tier).** This is heavier than Ch5 (標準嚴謹). The two parts of the **FTC are proved on the spot**; the **integrability characterization (continuous ⟹ integrable, via uniform continuity) is fenced to the Proof Track** (Appendix D / GAP-D). Expect the difficulty curve to run at/above Ch5; §6.2–6.3 are the crux. Per PIPELINE difficulty gate: a peak above §4.2's 4.5 or a whole-chapter mean > 4 is an **arc-level** anomaly → revisit the ROADMAP depth decision (SPEC §16.3), not a prose-layer fix.

## Roster (roadmap §6 provisional; Stewart ET 9e Ch5)

| § | Title | new machinery | key imports |
|---|---|---|---|
| 6.1 | Areas and Distances | area problem + distance problem as **limits of Riemann sums**; L/R/midpoint sums; sigma notation | **power sums Prop A.6 (§A.3)**; limit laws **Thm 1.2** |
| 6.2 | The Definite Integral | \(\int_a^b f\,dx\) = limit of Riemann sums; integrability; properties (linearity, additivity, comparison) | §6.1; continuity (Ch1); **fence: continuous ⟹ integrable** |
| 6.3 | The Fundamental Theorem of Calculus | **FTC-1** (\(g(x)=\int_a^x f\Rightarrow g'=f\)) + **FTC-2** (evaluation), **both proved** (export FTC) | integral MVT (**EVT 4.9(a)**+**IVT 4.9(b)**, App D §D.1–D.2); **MVT 4.12**; const-difference **Cor 4.4**; §6.2 |
| 6.4 | Indefinite Integrals & the Net Change Theorem | antiderivative family \(\int f\,dx\); basic table; Net Change; **\(\int\frac1x\,dx=\ln\lvert x\rvert+C\)** (export) | §6.3; derivative table Ch2–4; \((\ln x)'\) **Thm 4.14** |
| 6.5 | The Substitution Rule | u-substitution (indefinite + definite, change-of-limits); even/odd symmetry | **chain rule Thm 3.3**; differentials §5.3 (\(du\)); §6.3–6.4 |

Excluded (roadmap → later chapters): applications of integration = area between curves / volumes / work / average value → **Ch7**; techniques (parts, trig, partial fractions, improper, numerical) → **Ch8**. §6.5 does **only** u-substitution.

## Cross-chapter EXPORT (forward contract; keep exact)

- **FTC** §6.3 → Ch7–8 · 11 (integral test) · 13 · 15–16. The single most-imported export of the chapter.
- **\(\int\frac1x\,dx=\ln\lvert x\rvert+C\)** §6.4 → Ch8 (partial fractions, \(\int\tan\), …), Ch9 (separable/linear ODE). New forward export flagged in the roadmap seam-hunt.
- **Definite integral / Riemann-sum machinery** §6.1–6.2 → Ch7 (area/volume/arc length **as** integrals), Ch11 (integral test).

## Per-section seam / fence guards (from full-arc Codex seam-hunt + depth policy)

- **§6.1:** sigma notation is prerequisite (App A) — gloss briefly, **import power sums Prop A.6** (§A.3, retitled "Sigma Notation, Power Sums, and the Geometric Series") for \(\sum i,\sum i^2\) closed forms so a Riemann sum can be evaluated **from the definition**. Twin motivating problems: area under a curve (L/R/midpoint sums) **and** distance from velocity (\(\int v\,dt\)). Do **not** define the definite integral formally here — that is §6.2; §6.1 is the motivating limit-of-sums.
- **§6.2:** define \(\int_a^b f\,dx\) as a limit of Riemann sums (regular partition + norm → 0, Stewart register). **Fence: state "if \(f\) is continuous on \([a,b]\) then \(f\) is integrable" as a theorem and cite that the proof needs uniform continuity (compactness) → Proof Track.** Do **not** prove a general Riemann-integrability criterion. Properties (linearity, additivity over intervals, order/comparison, \(\lvert\int f\rvert\le\int\lvert f\rvert\)) — state; short proofs from Riemann sums are fine. **Open decision (→ §6.2 brief / ⑤):** whether to actually write the continuous⟹integrable proof as a new **App D §D.4** (GAP-D's first customer for this specific result) or fence it citation-only. Roadmap depth = "嚴謹陳述＋最重的 fence" → default fence; add §D.4 only if ⑤ judges it carries its weight. **〔2026-07-10 resolved〕 fenced on-credit, NO §D.4** — Codex ⑤ (§6.2 A2): add the full uniform-continuity proof only when a later chapter has concrete use for it. Theorem 6.2 (properties) is stated for **continuous** f (not "integrable"), so all four parts are fully proved via Theorem 6.1 without the fenced general-integrability machinery.
- **§6.3:** **FTC proved on the spot (深理論核心 crux).** FTC-1: \(g(x)=\int_a^x f(t)\,dt\Rightarrow g'(x)=f(x)\) for \(f\) continuous — proof via the difference quotient + the **integral Mean Value Theorem** (needs EVT 4.9(a) + IVT 4.9(b), both proved in **App D §D.1–D.2**). FTC-2 (evaluation): \(\int_a^b f=F(b)-F(a)\) — proof from FTC-1 + the constant-difference **Cor 4.4**. Name the integral MVT explicitly when used. Cautions: the dummy variable \(t\) vs the limit \(x\); \(g\) is an antiderivative **even when \(f\) has no elementary antiderivative** (e.g. \(\int_0^x e^{-t^2}dt\)).
- **§6.4:** indefinite integral = antiderivative family, the "\(+C\)". Table of basic antiderivatives (reverse the Ch2–4 derivative table). **\(\int\frac1x\,dx=\ln\lvert x\rvert+C\)** — justify the absolute value (the \(x<0\) branch: \(\frac{d}{dx}\ln(-x)=\frac1x\)); flag as forward export. Net Change Theorem: \(\int_a^b F'(x)\,dx=F(b)-F(a)\) reread as net change; honest applications (displacement vs total distance, marginal cost). Caution: \(\int f\,dx\) (a **family**) vs \(\int_a^b f\,dx\) (a **number**).
- **§6.5:** substitution = chain rule in reverse; \(du=g'(x)\,dx\) ties back to §5.3 differentials. Indefinite: \(\int f(g(x))g'(x)\,dx=\int f(u)\,du\). Definite: **change the limits** (Stewart's preferred form) — caution to convert the limits **or** back-substitute, never mix. Even/odd symmetry as a substitution corollary. Fence: **only** u-substitution here; parts/trig/partial fractions are Ch8. Hypothesis: \(g\) differentiable with \(g'\) continuous, \(f\) continuous on the range of \(g\).

## Numbering ledger (Ch6 counters reset fresh; per-type continuous across sections)

**Fill as each section reaches draft.** Cautions are UNNUMBERED (Ch1–5 convention).

| type | allocated so far | next |
|---|---|---|
| Definition | 6.1 (Area), 6.2 (Def. integral), 6.3 (Antiderivative), 6.4 (Indef. integral) | — (Ch6 complete) |
| Theorem | 6.1 (integrability), 6.2 (properties), 6.3 (FTC-1), 6.4 (FTC-2), 6.5 (Net Change), 6.6 (Substitution), 6.7 (definite sub), 6.8 (symmetry) | — |
| Proposition | — (none in Ch6) | — |
| Corollary | — (none in Ch6) | — |
| Lemma | — (none in Ch6) | — |
| Strategy | 6.1 (evaluate by FTC-2), 6.2 (substitution) | — |
| Example | 6.1–6.21 (M4 +5: 6.6, 6.7, 6.10, 6.15, 6.19) | — |
| Figure | 6.1–6.9 (M2 6.1–6.8 + M4 6.5 semicircle) | — |
| Remark | — (none in Ch6) | — |

**As-built numbering ledger (M1 complete; M2 figures; M4 Mode C additions):** Definition 6.1–6.4 · Theorem 6.1–6.8 · Strategy 6.1–6.2 · **Example 6.1–6.21** (M1 minted 6.1–6.16; M4 inserted 5 with full renumber cascade — §6.2 Ex 6.6 semicircle-geometry & Ex 6.7 linearity-numeric, §6.3 Ex 6.10 FTC-1 lower-limit/both-limits, §6.4 Ex 6.15 arctan→π/4, §6.5 Ex 6.19 substitution→log) · Cautions unnumbered (Ch1–5 convention) · **Figures 6.1–6.9** (M2 minted 6.1–6.8; M4 added Fig 6.5 semicircle-area, cascading old Fig 6.5–6.8 → 6.6–6.9). No Proposition/Corollary/Lemma/Remark in Ch6.

> Chapter opener (chapter-head + "By the end…") lives in **sec-6-1.html** (first `<article>`), per handout convention (five chapters + appendices all do this).

## Chapter opener — "By the end of this chapter you will be able to"

- express areas and distances as limits of Riemann sums;
- define the definite integral and evaluate simple cases from the definition;
- state and apply both parts of the Fundamental Theorem of Calculus;
- use the Fundamental Theorem to evaluate definite integrals through antiderivatives;
- find indefinite integrals and read the integral of a rate as a net change;
- evaluate integrals by the substitution rule, including definite integrals and symmetry.

## Per-section status

**M1 (draft + ⑤ Codex + chapter sweep) COMPLETE 2026-07-10 — all 5 sections.** Each: build ✔ / linebreak 0 / render katex 0 / Codex ⑤ 0 blocking. Chapter sweep: **sympy 29/29 PASS** · **章層 Codex review M1–M8 clean** (1 cross-ref blocking [§6.6→Ex 6.6] + 1 metadata advisory, both fixed) · full-chapter render math=612, katex 0. Sweep record: `ch06_chapter-sweep-audit.md`.

| § | stage | env minted | Codex ⑤ |
|---|---|---|---|
| 6.1 Areas and Distances | ✅ draft | Def 6.1 (Area under a curve); Ex 6.1–6.3 | **0 blocking** (4 fixed: B1 direction, B2 math [false L-vs-R], B3/B4 hygiene) + 2 regressions; `ch06_s6-1-codex5-audit.md` |
| 6.2 The Definite Integral | ✅ draft | Def 6.2; Thm 6.1 (integrability, on-credit fence), Thm 6.2 (properties); Ex 6.4–6.6 | **0 blocking** (4 fixed: M1 additivity-partition gap, H1 hyp+notation clash, H2 √x integ, D1 FTC leak) + 2 regressions; `ch06_s6-2-codex5-audit.md` |
| 6.3 The Fundamental Theorem of Calculus | ✅ draft | Def 6.3 (Antiderivative); Thm 6.3 (FTC-1, **proved**), Thm 6.4 (FTC-2, **proved**); Strategy 6.1; Ex 6.7–6.9 | **0 blocking** (2 hyp-hygiene fixed: B1 antideriv interval/Cor 4.4, B2 g-continuity) + 1 regression; `ch06_s6-3-codex5-audit.md` |
| 6.4 Indefinite Integrals & Net Change | ✅ draft | Def 6.4 (Indef. integral); Thm 6.5 (Net Change); Ex 6.10–6.12; **∫1/x=ln\|x\| export shipped** | **0 blocking** (2 fixed: H table domains, M Ex 6.12 signs/closing) + 1 regression; `ch06_s6-4-codex5-audit.md` |
| 6.5 The Substitution Rule (+ Ch summary) | ✅ draft | Thm 6.6 (Sub Rule), 6.7 (definite sub), 6.8 (symmetry) — all **proved**; Strategy 6.2; Ex 6.13–6.16; **Chapter summary** | **0 blocking (clean first pass)**; `ch06_s6-5-codex5-audit.md` |

## Gate-family checklist（與 `../../PIPELINE.md` dashboard 同步）

| 閘家族 | 狀態 | 日期／備註 |
|---|---|---|
| M1 Mode A′（brief＋⑤＋sympy＋章層 review） | ✅ | 2026-07-10：§6.1–6.5 全數 Codex ⑤ 0 blocking＋**sympy 29/29 PASS**＋**章層 review M1–M8 clean**（1 cross-ref blocking [§6.6→Ex 6.6]＋1 metadata advisory 修）。as-built: Def 6.1–6.4／Thm 6.1–6.8／Strategy 6.1–6.2／Ex 6.1–6.16／0 figures。exports shipped: FTC §6.3、∫1/x=ln\|x\| §6.4。`ch06_chapter-sweep-audit.md` |
| M2 圖（機會→繪製→D1–D8＋gate-2） | ✅ | 2026-07-10：機會稽核 done（4 subagent）＋`buildPlot` fill primitive（rect/area）加＋**Figure 6.1–6.8 全數 drawn+rendered**。**gate-1（`handout-figure-audit` D1–D8）0 blocking**（8 圖逐一回原始碼核對，含 m_h/M_h·u_h/v_h 小字級複核、6.2 no-`=1/3` 確認）＋**gate-2（Codex `-i` 視覺第二讀者，v0.144.1）8 圖全 clean 0 blocking**。報告 `_audit/REVIEW-ch06-figure-audit.html`（render 圖＋雙閘結果）＋raw `ch06_figure-audit.md` |
| M3 散文 S·A·V＋難度 learner-sim（合一輪） | ✅ gate-1 完成（裁決套用畢）；散文 gate-2 待 M4 後批次 | 2026-07-10 gate-1：5 節 `handout-prose-audit`＋3 份盲測 `learner-sim`。**gate-1 = 0 blocking**（3 sim 全 0 stuck、0 B 類先備違規；難度曲線一致 [2,3,4,3,3]，尖峰 §6.3 FTC effortful-not-stuck、≤§4.2 之 4.5，非弧線異常；散文 5 節皆 0 blocking，§6.3 全乾淨）。**2026-07-11 逐條裁決後套用**：建議套用 5 項（P-6.2-a Thm 6.2 比較句拆分＋點名 g−f≥0／P-6.2-b reason about it／P-6.4-a Def 6.4 拆句／P-6.4-c 反三角表補 Ch3 出處／P-6.5-a §6.5 章末去 cleft）＋使用者裁決 2 項照建議（**P-6.1-a §6.1 距離線統一 speed**：Ex 6.3 ×2＋收尾＋Fig 6.3 caption／**P-6.4-b §6.4 one→we** ×2）；選配 glosses（P-6.1-b/c、P-6.2-c/d）依建議略過；P-6.1-d（lead）declined。全部 rebuild＋linebreak 0＋render katex 0 驗過。**P-6.1-e（拼寫）＝全書 §15 US-vs-corpus-British drift，不在 M3／非 Ch6 issue**，轉全書一致性 sweep（見 `CONTENT_SPEC.md` §15 註記，建議書近完成時一次過跑）。合併裁決稿 `_audit/REVIEW-ch06-prose-difficulty.html`。散文 gate-2（Codex）依「gate-2 全跑」批次留待 M4 後 |
| M4 Mode C gap-check（①②合一） | ✅ 偵察＋裁決＋套用＋回歸 done | 2026-07-11：`mode-c-gapwalk`＋`example-supplement` 唯讀偵察（Ch6 M1 覆蓋紮實、8 候選、§6.1 clean）→ 裁決稿 `_audit/REVIEW-ch06-modec-gapcheck.html`。**使用者裁決採 7/8**（除 6.5-E2）：5 例題（6.2-E2 semicircle／6.2-E1 linearity／6.3-E1 FTC-1 diff／6.4-E1 arctan／6.5-E1 sub→log）＋2 軟深度（6.5-1 對稱幾何直覺／6.1-1 單調性 caution）＋1 新圖（Fig 6.5 semicircle）。**套用＋回歸 done**：全編號 cascade（Ex→6.1–6.21、Fig→6.1–6.9 連續）、5 新例 **sympy 5/5 PASS**、**圖 gate-1 = 0 blocking**（semicircle，1 D6 advisory 已修等比例）、**scoped Mode B = 0 blocking**（3 客觀 advisory 已套：§6.1 integrand→f 守 seam guard、§6.2 forward-term 軟化、summed→evaluated）、linebreak 0＋katex 0。三閘 gate-2（含此批新內容）留待此後批次。applied 報告 `_audit/REVIEW-ch06-modec-applied.html` |
| 三閘 gate-2（數學／散文／圖，全跑到 0 blocking） | ✅ 0 blocking（fixes 套用＋回歸畢） | 2026-07-11：Codex **gpt-5.6-sol／effort=max**，三獨立閘。**數學 M1–M8**：1 blocking（Fig 6.2 caption 誤把 overshoot-above-curve 說成「單一末端長條 1/n」——那是 R−L gap，非 R−A=1/(2n)+1/(6n²)；改為 qualitatively 正確敘述、不洩 A）＋1 advisory（Σi² 交叉引用「by induction」→「by telescoping」對齊 App A §A.3 實際證法）；**5 個 M4 authored 例題、FTC 兩證、換元三證獨立複核皆 PASS**。**散文 S·A·V**：0 blocking＋4 advisory（3 客觀套用：§6.3 Two chapters→sections 事實、constant-of-integration→any-added-constant forward-term、§6.5 對稱直覺精確化；1 結構性 held）。**圖視覺**：8 clean＋1 **false-positive**（Fig 6.9 ylabel 實為 \(v\)，VLM 把斜體 v 誤讀為 y；未依誤讀改標，改修 readability＝加頂 headroom，zoom 複驗 v 清晰）。全部 rebuild＋linebreak 0＋katex 0＋env-num 6.1–6.21 連續。報告 `_audit/REVIEW-ch06-gate2.html` |
| M5 收尾（dashboard＋ROADMAP open-q） | ✅ | 2026-07-11：三閘 gate-2 0 blocking → **Ch6 定版**。PIPELINE dashboard Ch6 列更新；ROADMAP Ch6 status→done。as-built 凍結：Def 6.1–6.4／Thm 6.1–6.8／Strategy 6.1–6.2／Example 6.1–6.21／Figure 6.1–6.9／Cautions unnumbered。**Ch6＝首個全程 5-milestone 試點章，M1–M5 端到端跑完**——milestone 序列可回顧定版。open-q：全書 §15 拼寫 sweep（見 CONTENT_SPEC §15 註記＋背景任務 chip） |

## M2 figure batch (2026-07-10 — COMPLETE)

**gate-1 圖機會稽核 DONE**: 4 `handout-figure-opportunity-audit` subagents (§6.1–6.4) + my brief candidates consolidated. §6.5 (substitution) = no figure (algebraic technique; low value — recorded, not drawn). All sections were 0-figure (deferred, not declined) → no D3 override.

**Kit prerequisite DONE**: `buildPlot` (chapter6 standalone) extended with **`rect`** (filled rectangle: x1,x2,y1,y0) + **`area`** (filled region under fn between domain[0..1], to base) items + CSS fill classes (`.fill-area/.fill-pos/.fill-neg/.rect-lo/.rect-hi/.rect-sum`). Persists across `build.py` (outside content region). **Validated end-to-end by Figure 6.1** (renders correctly).

**Adopted batch (essential + strong; contiguous reading-order numbering):**

| Fig | § | locus | what | tier | key domain facts (a correct drawing MUST respect) | status |
|---|---|---|---|---|---|---|
| 6.1 | §6.1 | after Ex 6.1 | Riemann L₄ vs R₄ rectangles under x², `pair` | ess | f=x² increasing; left rects under (leftmost height 0 = absent), right rects over, tallest→(1,1); sums 7/32,15/32 in text only | ✅ drawn+audited (`riemann-lr-x2`) |
| 6.2 | §6.1 | Ex 6.1→6.2 | refinement R₄→R₈→R₁₆ closing bracket, `triple` | strong | same curve; gap = single end-rect 1/n→0; no "=1/3" annotation (Ex 6.2's answer) | ✅ drawn+audited |
| 6.3 | §6.1 | Ex 6.3 | v–t step graph, distance=area, `single` | strong | pts (0,0)(1,4)(2,7)(3,9)(4,10)(5,10); left-sum first rect height 0, right-sum last two both 10; **discrete data — any interpolating curve dashed/soft, NOT solid** | ✅ drawn+audited |
| 6.4 | §6.2 | Ex 6.5 | net signed area, two congruent triangles of y=x−1, `single` | ess | crosses axis at x=1; [0,1] below (−, area ½), [1,2] above (+, area ½); **+/− by label+tone, not colour (D8)**; net 0 vs total 1 in caption | ✅ drawn+audited |
| 6.5 | §6.2 | Ex 6.6 | min/max bounding rectangles of √x on [1,4], `single` | strong | √x incr+concave-down; m=1 at left (1,1), M=2 at right (4,2); inscribed y=1 (rect-lo), circumscribed y=2 (rect-hi); touch only at endpoints | ✅ drawn+audited |
| 6.6 | §6.3 | accumulation subsec | accumulation g(x)=area-so-far + sliver f(x)h, `single` | ess | f>0 on window (literal "under graph"); shade [a,x]=g(x), sliver [x,x+h]; **h exaggerated, label "not to scale"**; height ≈f(x) | ✅ drawn+audited |
| 6.7 | §6.3 | FTC-1 proof | difference-quotient trapped: inscribed m_h vs circumscribed M_h rectangles on [x,x+h], `single` | strong | m_h=min f (below curve), M_h=max f (above); both→f(x) as h→0 (callout); h>0, f>0 | ✅ drawn+audited |
| 6.8 | §6.4 | Ex 6.12 | velocity v=t²−4 signed regions, displacement vs distance, `single` | ess | right half of up-parabola on [0,3]; v(0)=−4, root v(2)=0, v(3)=5; [0,2) below (−, 16/3), (2,3] above (+, 7/3); regions meet at (2,0); **+/− label+tone (D8)** | ✅ drawn+audited |

**Deferred (considered, recorded — add later if desired, would renumber):** §6.2 arbitrary-sample-points, general signed schematic, additivity-split; §6.3 inverse-processes capstone diagram; §6.4 antiderivative-family (+C), ln|x| two-branches.

**M2 steps — all DONE (2026-07-10):** ✅ drew 6.2–6.8 (FIGS fn + fragment `<figure>` marker, reading order) → `build.py ch06` (katex 0, math 741) → `linebreak-gate` 0 → `shot.mjs … figures` (8× 2× PNG) → self-check每圖 PNG（矩形碰對曲線、陰影區、grayscale 皆確認）→ **gate-1 `handout-figure-audit` D1–D8 = 0 blocking**（8 圖逐一回原始碼核對）→ **gate-2 Codex `-i` 視覺 = 8 圖全 clean 0 blocking** → `REVIEW-ch06-figure-audit.html`. **一次過、無 blocking 迭代**（繪圖前置的 `buildPlot` rect/area primitive＋Fig 6.1 範式讓 6.2–6.8 首繪即正確）。sec-6-1..6-4 header 的 figure ledger 註解已更新。`--fig-6-*` width vars 未加：8 圖皆以 buildPlot inline width（single 250–320px、triple 215px、pair 250px）render 正常，無 sizing 需求。

**Audit reports:** `REVIEW-ch06-figure-opportunity.html` (opportunity decision); **`REVIEW-ch06-figure-audit.html`** (render 圖＋D1–D8＋gate-2，✅ 產出 2026-07-10；8 圖 embedded PNG＋雙閘 0 blocking，MathJax standalone 雙擊即讀). Raw findings 摘要 → `ch06_figure-audit.md`（不進版控）.

## Scaffolding notes (2026-07-10)

- `chapter6-print-standalone.html` cloned from chapter5 via `scratchpad/scaffold_ch6.py`: title → Chapter 6, `FIGS` emptied to `{}`, content region cleared (build.py refills), 22 dead `--fig-5-*` CSS lines stripped. MathJax config + macros (`arccsc`/`arcsec`/`arccot`) + paginator carried verbatim.
- **Post-clone manual fixes the script missed** (record for a reusable template recipe, e.g. the linalg repo): the paginator `CHAPTER.brand` + `CHAPTER.runningHead` (the **per-page running header**, "Chapter 5 · Applications of Differentiation") and the two `figures.js — Chapter N figure registry` comments were still "Chapter 5" → patched to Chapter 6. A complete clone recipe must patch **title + brand + runningHead + FIGS + content region + figure CSS + registry comments** (7 chapter-specific loci; the ch05 `--fig-N` figure CSS is stripped, re-added in M2).
- `build.py` CHAPTERS registry: **add `"ch06"` entry when `sec-6-1.html` first exists** (registry must never point at a missing fragment — keeps `python build.py` all-chapters valid). Fragments appended incrementally as each section reaches draft (ch05 pattern).
- **M2 figure debt:** when ch06 figures land, add fresh `--fig-6-*` width vars + `.paper figure[data-fig=…]` rules to the shell (the ch05 block was stripped, not renamed).
