# PLAN-ch07 — Chapter 7: Applications of Integration

Chapter-level direction anchor + cross-session state. Third manuscript-free chapter; the 5-milestone
sequence was piloted end-to-end and frozen on Ch6 (see [`../../PIPELINE.md`](../../PIPELINE.md)).

## Workflow (manuscript-free, autonomous)

- **Spine = canon** (Stewart ET 9e Ch6 + Ch8.1–8.2 primary; Thomas 14e / Rogawski 4e cross-check),
  authored to full-gate tier. No teacher manuscript exists Ch5–16.
- **Provenance:** each fragment carries a `<!-- section-source: … -->` header; pedagogical add-ons
  keep the `expansion:<cat>` tag system.
- **Human gates → Codex.** ③ direction gate and ⑤ advisory review run against **Codex**
  (read-only). **This chapter's session grant (2026-07-18): the user authorized standing Codex
  calls for the whole conversation and delegated 拍板 decisions to Claude-⇄-Codex convergence**
  (per-call consent not required within that conversation; the CLAUDE.md per-call-consultation rule
  stays in force for future sessions).
- **Anti-hallucination backstops:** (1) per-section brief + hypothesis ledger; (2) Codex
  adversarial ⑤ (direction-conformance + math + hypothesis hygiene) to 0 blocking; (3) chapter-end
  sympy recompute of all worked examples.
- **Depth: 標準嚴謹 (Ch5-level).** Lighter than Ch6 (深理論核心). The chapter's honest-construction
  obligations: the **Mean Value Theorem for Integrals is proved on the spot** (EVT 4.9(a) + IVT
  4.9(b) + comparison Thm 6.2); the **C¹ arc length theorem is proved on the spot** (MVT 4.12 +
  Def 6.2's any-sample-point clause + Thm 6.1). Volume / work / surface area rest on *modeling
  definitions* (slab / shell / frustum decompositions) — the modeling step is stated as the
  definition, not smuggled. Everything else is computation at Stewart register.

## Roster (roadmap §7 provisional; Stewart ET 9e Ch6 + §8.1–8.2) — ③ RESOLVED 2026-07-18 (Codex, one round; audit: `ch07_ch-direction-codex3-audit.md`)

| § | Title | new machinery | key imports |
|---|---|---|---|
| 7.1 | Areas Between Curves | Def: area between graphs \(A=\int(f-g)\); crossing curves → split via \(\int\lvert f-g\rvert\); integrating along \(y\) | FTC-2 **Thm 6.4**; properties **Thm 6.2**; §6.1–6.2 Riemann machinery |
| 7.2 | Volumes | Def: volume by cross-sections \(V=\int A(x)\,dx\); solids of revolution: disks, washers | Def 6.2; **Thm 6.1** (existence); FTC-2 |
| 7.3 | Volumes by Cylindrical Shells | shell method \(V=\int 2\pi x f(x)\,dx\); midpoint sample-point derivation | §7.2; Def 6.2 (any-sample-point); Thm 6.1 |
| 7.4 | Work | Def: \(W=\int F(x)\,dx\); Hooke's law spring; cable/rope lift; pumping a tank | §6.1–6.2 slice-and-sum; Net Change reading §6.4 |
| 7.5 | Average Value of a Function | Def: \(f_{\text{ave}}=\frac{1}{b-a}\int_a^b f\); **Mean Value Theorem for Integrals (proved)** | **EVT 4.9(a)**, **IVT 4.9(b)**; comparison **Thm 6.2(4)**; FTC-2 |
| 7.6 | Arc Length | Def: \(L=\lim\sum\lvert P_{i-1}P_i\rvert\); **C¹ arc length theorem (proved)**; arc length function \(s(x)\); differential \(ds\) | **MVT Thm 4.12**; Def 6.2; Thm 6.1; FTC-1 **Thm 6.3** (for \(s'(x)\)) |
| 7.7 | Area of a Surface of Revolution | Def: frustum-band limit; formula \(S=\int 2\pi f(x)\,ds\) (both axes) | §7.6 (\(ds\), arc machinery); MVT 4.12; Def 6.2 |

**Excluded (roadmap 選材節制 — Stewart 6/8 material deliberately dropped):** hydrostatic pressure,
moments/centers of mass, Pappus (Stewart 8.3); economics/biology applications (8.4); probability
(8.5). Numerical/improper integrals → Ch8. Parametric arc length → Ch10; curvature → Ch13; general
surface integrals → Ch16.

## Cross-chapter EXPORT (forward contract; keep exact)

- **Mean Value Theorem for Integrals** §7.5 → Ch15 as *average-value normalization + the
  one-dimensional attainment template* (the attainment step silently uses the interval's
  connectedness — Ch15 must NOT restate attainment for disconnected regions without compactness +
  connectedness hypotheses; ③ advisory #12). Closes the seam-hunt premise "積分均值(EVT+IVT)".
- **Arc length formula + \(ds\)** §7.6 → Ch10 §10.2 (parametric arc length), Ch13 §13.3
  (arc length & curvature); closes the seam-hunt premise "C¹ 弧長定理".
- **Surface-of-revolution formula** §7.7 → Ch16 (parametric surfaces / surface integrals, soft).
- **Cross-section volume principle** §7.2 → Ch15 (double integrals as volumes; Fubini echo, soft).

## Chapter-level direction decisions — ③ RESOLVED 2026-07-18 (Codex one round, all adopted; full record `ch07_ch-direction-codex3-audit.md`)

- **[D1 roster — RESOLVED: keep 7, capped]** Full 7-section roster kept. **Hard cap 23 worked
  examples chapter-wide** (planned 22); §7.4 exactly 3; **§7.7 at most 2** (the about-\(y\)-axis
  and direct-u-sub examples merged into one); Schwarz-lantern digression NOT written. Grounds =
  course scope (NTU 甲 = Stewart 1–10), NOT sec-6-5's summary promise (which names only areas /
  volumes / arc lengths).
- **[D2 integral MVT — RESOLVED with degeneracy discipline]** §7.5 mints **Theorem 7.2 (Mean Value
  Theorem for Integrals)**, hypotheses \(f\) continuous on \([a,b]\) **with \(a<b\)** (Definition
  7.4 likewise \(a<b\); no reversed-limits convention imported into averages), conclusion
  \(c\in[a,b]\). Proof: EVT 4.9(a) gives attained \(m=f(x_m)\), \(M=f(x_M)\); comparison Thm 6.2(4)
  gives \(m \le f_{\text{ave}} \le M\); **case \(m=M\)**: \(f\) constant, any \(c\) serves; **case
  \(m<M\)**: set \(\alpha=\min\{x_m,x_M\}\), \(\beta=\max\{x_m,x_M\}\) and apply IVT 4.9(b) on
  \([\alpha,\beta]\). FTC-route alternative: ONE sentence naming Thm 6.3 + Thm 4.12, no second
  proof. Ch6 §6.3 minted no such theorem (checked: \(m_h/M_h\) squeeze) — fresh mint closes the
  seam premise.
- **[D3 arc length — RESOLVED with C¹ notation minted in place]** §7.6: **Definition 7.5** = limit
  of regular-partition inscribed-polygon lengths, a **finite** limit if it exists; \(L=0\) when the
  interval degenerates; NO reversed-orientation convention (length is unsigned). **Theorem 7.3
  (Arc Length Formula)**: \(a<b\) and \(f \in C^1([a,b])\) — the notation DEFINED in place:
  continuous on \([a,b]\), differentiable with \(f'\) extending continuously to the endpoints
  (one-sided there); call such \(f\) *smooth on \([a,b]\)*. Proof: MVT 4.12 per strip (closed-strip
  continuity + open-strip differentiability granted by the blanket hypothesis — bridge sentence
  mandatory), then Riemann sum of continuous \(\sqrt{1+f'^2}\) → Thm 6.1 + Def 6.2's
  any-sample-point clause. Terminology: **graph arc length**; Ch10 parametric = forward-ref only.
- **[D4 surface area — RESOLVED: direct proof, NO fence]** §7.7 defines \(S\) as the frustum-band
  limit (**Definition 7.6**) and proves **Theorem 7.4**: for smooth \(f\ge0\),
  \(S=\int_a^b 2\pi f(x)\sqrt{1+f'(x)^2}\,dx\). The originally proposed named uniform-continuity
  fence is **dropped** (no App D entry exists = an address-less proof debt); instead the C¹
  hypothesis closes the gap on the spot: \(K=\max\lvert f'\rvert\), \(B=\max\sqrt{1+f'^2}\) (EVT);
  MVT gives \(\bigl\lvert\tfrac{f(x_{i-1})+f(x_i)}{2}-f(\xi_i)\bigr\rvert\le K\Delta x\), so the
  total height-replacement error is \(\le 2\pi BK(b-a)\Delta x \to 0\) — fully proved, zero new
  fences. Presentation unified as \(S=\int 2\pi\rho\,ds\): about the \(x\)-axis \(\rho=f\ge0\);
  about the \(y\)-axis \(0\le a<b\), \(\rho=x\) (curve entirely on one side of the axis — no
  cross-axis overlap). Frustum lemma: derive \(\pi(r_1+r_2)\ell\) from cone sectors AND verify the
  \(r_1=r_2\) cylinder case separately by unrolling (the similar-cone subtraction divides by
  \(r_2-r_1\)); 108 課綱 S-9 makes the cone geometry an A-class short bridge — show, don't cite.
- **[D5 shells — RESOLVED with wording discipline]** §7.3 mints **Theorem 7.1 (shell method)**,
  hypotheses \(f\) continuous, \(f\ge0\), \(0\le a<b\). "Exact" describes ONLY the approximating
  annular cylinder of height \(f(\bar x_i)\) — never the original solid's radial band. Order:
  name the shell-stack model first (same modeling tier as §7.2's slabs, said explicitly), then the
  midpoint algebra display \(\pi(x_i^2-x_{i-1}^2)f(\bar x_i)=2\pi\bar x_i f(\bar x_i)\Delta x\),
  then Def 6.2 (midpoints are legitimate sample points) + Thm 6.1. Shifted-axis mention (Strategy
  7.2 line only): region entirely on one side, radius \(\lvert x-c\rvert\). Washer-vs-shell: one
  comparison example, numbers must agree; general equivalence deferred (Ch8 parts / Ch15 change of
  variables) in a one-line remark.
- **[D6 選材 — RESOLVED as proposed, no mods]** §7.4 SI primary (J, N, m), one ft-lb mention,
  exactly 3 examples (spring / cable / pumping); §7.5 no RMS; dropped further-apps stay dropped.
  Plus ③ advisory #10: Hooke's \(F=kx\) is the *applied* force (restoring \(-kx\)) — the spring
  example computes work done *against* the spring; cable densities given directly as weight
  density (N/m), never bare kg/m.
- **[D7 opener — RESOLVED: schema kept, outcomes 6→5]** Stewart order; the opener names the
  slice–approximate–sum–refine schema once; per-section openers instantiate (not restate) it.
  ③ caught the opener's learning-outcome list at SIX bullets vs SPEC §4's mandatory 3–5 → the
  arc-length and surface-area bullets merge into one (five total). Fixed in sec-7-1.html.

## Per-section seam / fence guards (read before drafting each brief)

- **§7.1:** area *between* graphs is a NEW definition (Def 6.1 covers only \(f\ge 0\) vs the axis) —
  state \(A=\int(f-g)\) for \(f\ge g\) as a Definition, with a one-sentence consistency check vs
  Def 6.1 when \(g=0\), and the sign-shift invariance intuition (raising both graphs by the same
  constant leaves \(f-g\) unmoved — so negativity is no obstacle). Crossing curves: total area
  \(=\int\lvert f-g\rvert\), computed by splitting at intersections — intersection-finding is Step 1
  of every worked solution. Sideways regions \(x=g(y)\): one worked example + strategy line, not a
  second definition. NO centroids, NO parametric-curve areas (Ch10), NO improper regions (Ch8).
- **§7.2:** Definition (Volume by cross-sections): \(V=\lim\sum A(x_i^*)\Delta x=\int A\,dx\) for
  continuous \(A\) — existence by Thm 6.1, cite explicitly. Disks/washers = instances (compute
  \(A(x)\) from the geometry, then apply the definition — no separate "disk theorem"). Sphere
  example doubles as sanity anchor (recovers \(\tfrac43\pi r^3\); same move as Ch6's semicircle
  Ex 6.6). Washer subtraction \(A=\pi(R_{\text{out}}^2-r_{\text{in}}^2)\) + the standard Caution
  \(\pi(R^2-r^2)\ne\pi(R-r)^2\). NO Pappus; general solids only through the cross-section principle.
- **§7.3:** shells per D5 (midpoint algebra display mandatory). Setup discipline: the shell
  variable measures distance to the rotation axis. "Washer or shell?" strategy box. One comparison
  example computing the SAME solid both ways (numbers must agree; choose \(f\) monotone so the
  washer leg's inversion \(x=g(y)\) is honest and quick). NO shells about arbitrary lines beyond
  one shifted-axis example; NO general equivalence proof (one-line deferral remark).
- **§7.4:** Definition (Work): \(W=\int_a^b F(x)\,dx\) for continuous force along a line; the
  constant-force product \(W=Fd\) is the physics input, the integral is the slice-and-sum upgrade.
  Hooke's law stated as empirical model (source tag). Cable and pumping slice DIFFERENT things
  (cable: the rope by position; tank: the water by depth) — each solution names what is sliced
  BEFORE integrating (the section's transferable skill). Water weight density \(9800\ \text{N/m}^3\)
  given in-example; units tracked. Exactly 3 examples. NO hydrostatic pressure, NO centroids.
- **§7.5:** Definition (average value) motivated from the arithmetic mean of \(n\) samples →
  integral (the ONE new intuition); then MVT for Integrals per D2. Geometric reading: mean-height
  rectangle with area \(=\int f\) — essential figure opportunity. Caution: \(f_{\text{ave}}\)
  depends on the interval, not just \(f\). NO RMS; NO probability mean.
- **§7.6:** arc length per D3 (bridging sentence mandatory). Definition first (inscribed polygons,
  regular partitions), Theorem for C¹. Examples restricted to the current antiderivative toolkit:
  \(y=x^{3/2}\) (u-sub); \(y=\frac{x^3}{6}+\frac{1}{2x}\) (perfect square);
  \(y=\frac{x^2}{8}-\ln x\) type (uses §6.4 \(\int dx/x\)) — pick 2–3. Arc length function
  \(s(x)\), its derivative via FTC-1 (Thm 6.3), differential \(ds=\sqrt{1+(dy/dx)^2}\,dx\) minted
  HERE (ties to §5.3 differentials; export to §7.7/Ch10/Ch13). NO parametric (Ch10), NO curvature
  (Ch13), NO \(\int\sec\)-type integrands (Ch8).
- **§7.7:** surface area per D4-resolved (direct C¹ error-bound proof, NO fence). Frustum lemma
  \(\pi(r_1+r_2)\ell\) from cone sectors + separate \(r_1=r_2\) cylinder check by unrolling
  (③ blocking #5). Unified \(S=\int 2\pi\rho\,ds\); about \(y\)-axis only with \(0\le a<b\)
  (③ blocking #6) — radius = distance to axis, caution. Examples (**exactly 2**, ③ D1):
  **Ex 7.21** spherical zone (theorem-compliant sanity anchor; hat-box punchline; \(4\pi r^2\) as
  explicitly-flagged limiting preview — full sphere fails C¹ at the poles, ③ blocking #4);
  **Ex 7.22** \(y=x^2\), \(x\in[0,1]\), about the \(y\)-axis (y-axis discipline + u-sub, one
  example two jobs). NO Pappus, NO general surfaces (Ch16), NO Schwarz-lantern (③ D1: not
  written). Chapter summary follows in this fragment.

## Numbering ledger (Ch7 counters reset fresh; per-type continuous across sections)

**Fill as each section reaches draft.** Cautions are UNNUMBERED (Ch1–6 convention). The table below
is the PLANNED allocation implied by the roster; as-built numbers get written here as sections land.

| type | planned (per roster; subject to draft) | allocated so far (as-built, drafts pre-⑤-close) |
|---|---|---|
| Definition | §7.1 area-between, §7.2 volume, §7.4 work, §7.5 average value, §7.6 arc length, §7.7 surface area | **7.1** (Area between curves, §7.1) · **7.2** (Volume by cross-sections, §7.2) · **7.3** (Work, §7.4) · **7.4** (Average value, §7.5) · **7.5** (Arc length, §7.6) · **7.6** (Surface area of revolution, §7.7) |
| Theorem | §7.3 shell method, §7.5 MVT for Integrals, §7.6 Arc Length Formula, §7.7 Surface Area Formula | **7.1** (Shell method, §7.3) · **7.2** (MVT for Integrals, §7.5, proved) · **7.3** (Arc Length Formula, §7.6, proved) · **7.4** (Surface Area Formula, §7.7, proved) |
| Proposition | none expected | — (none minted) |
| Corollary | none expected | — (none minted) |
| Strategy | §7.1 area setup, §7.3 washer-or-shell, §7.4 work-integral setup | **7.1** (Setting up an area integral, §7.1) · **7.2** (Washer or shell?, §7.3) · **7.3** (Setting up a work integral, §7.4) |
| Example | 4+4+3+3+3+3+2 per §7.1–§7.7 = **22 planned** (③ hard cap 23) | **7.1–7.4** (§7.1) · **7.5–7.8** (§7.2) · **7.9–7.11** (§7.3) · **7.12–7.14** (§7.4) · **7.15–7.17** (§7.5) · **7.18–7.20** (§7.6) · **7.21–7.22** (§7.7) = 22 ✓ |
| Figure | M2 batch | — (**23** `[FIGURE-OPPORTUNITY]` markers: 18 at M1 close + 1 ds-triangle 〔§7.6 ⑤ ADV-FIG-01〕 + 4 from the M2 coverage audit 〔§7.1 enclosed-lens、§7.3 motivating-failure、§7.7 unrolled-band（brief 有列漏落地）、§7.7 zone equal-width bands〕; per-section 4+4+4+3+1+3+4) |
| Remark | as needed | — (none minted; asides carried as marked prose / cautions) |

> Chapter opener (chapter-head + "By the end…") lives in **sec-7-1.html** (first `<article>`), per
> handout convention.

## Chapter opener — "By the end of this chapter you will be able to" (③-final: five bullets)

- compute the area of a region bounded by curves, slicing along either axis;
- compute volumes by cross-sections, by disks and washers, and by cylindrical shells;
- set up and evaluate work integrals for springs, cables, and pumping problems;
- compute the average value of a function and locate a point where it is attained;
- compute the length of a smooth curve and the area of a surface of revolution, and work with the arc length function.

## Per-section status

| § | stage | env minted | Codex ⑤ |
|---|---|---|---|
| 7.1 Areas Between Curves | ✅ draft | Def 7.1; Strategy 7.1; Ex 7.1–7.4 | **CLOSED 0 blocking**（r1: 2 blocking fixed〔B1 velocity-gap 假設＋過度泛化、B2 水平切片漏連續〕；r2 回歸 clean）`ch07_s7-1-codex5-audit.md` |
| 7.2 Volumes | ✅ draft | Def 7.2; Ex 7.5–7.8 | **CLOSED 0 blocking**（r1: 3 blocking fixed〔DIR-01 opener 重列 schema、HYP-01 washer 漏連續、HYP-02 金字塔 0/0〕＋§7.4 contagion 修；r2 回歸 clean）`ch07_s7-2-codex5-audit.md` |
| 7.3 Volumes by Cylindrical Shells | ✅ draft | Thm 7.1; Strategy 7.2; Ex 7.9–7.11 | **PASS 0 blocking／0 advisory（clean first pass）** `ch07_s7-3-codex5-audit.md` |
| 7.4 Work | ✅ draft | Def 7.3; Strategy 7.3; Ex 7.12–7.14 | **CLOSED 0 blocking**（r1: 1 blocking fixed〔7.4-B1 力主詞/正負號〕；r2 回歸 R-74 clean）`ch07_s7-4-codex5-audit.md` |
| 7.5 Average Value of a Function | ✅ draft | Def 7.4; Thm 7.2 (MVT for Integrals, proved); Ex 7.15–7.17 | **PASS 0 blocking／0 advisory（clean first pass）** `ch07_s7-5-codex5-audit.md` |
| 7.6 Arc Length | ✅ draft | Def 7.5; Thm 7.3 (Arc Length Formula, proved); Ex 7.18–7.20 | **CLOSED 0 blocking**（1 advisory ADV-FIG-01 漏標 ds 三角形 figure 機會→補標，marker-only 免回歸；證明判嚴密、seam 關閉）`ch07_s7-6-codex5-audit.md` |
| 7.7 Surface Area (+ Ch summary) | ✅ draft | Def 7.6; Thm 7.4 (Surface Area Formula, proved); Ex 7.21–7.22; Ch summary | **CLOSED 0 blocking**（r1: 4 blocking fixed〔B1 跨軸過度普遍化、B2 總結漏 Def 7.6、B3 力主詞重現、B4 Two→Three〕；證明本體/兩例/frustum lemma r1 即 clean；r2 回歸 4/4 clean on 章層 review）`ch07_s7-7-codex5-audit.md` |

> 進度註（2026-07-18，M1 收案）：七節 ⑤ 全數 CLOSED 0 blocking；章層 review M1–M8 全維 CLEAN；機械閘終值 build ✔／linebreak 0／quote lint clean ×7／render **math=813**、katex-errors 0／sympy **48/48**／xref 51 條 0 dangling＋counter 連續。（Ex 7.21 的 √ 合併為 sympy 分支限制，改平方恆等式＋數值抽點驗，非內容錯誤。）期間一次電腦重開機中斷三個進行中 call，原 prompt 重跑無資料損失。

## Gate-family checklist（與 `../../PIPELINE.md` dashboard 同步）

| 閘家族 | 狀態 | 日期／備註 |
|---|---|---|
| M1 Mode A′（brief＋⑤＋sympy＋章層 review） | ✅ | 2026-07-18：③ 章層方向閘對 Codex 單輪收斂（D1–D7 全採納＋8 blocking/5 advisory 落地）→ §7.1–7.7 全數 Codex ⑤ **0 blocking**（r1 blocking 計 10：§7.1×2、§7.2×3、§7.4×1、§7.7×4；§7.3/§7.5 clean first pass；回歸全 clean）＋**sympy 48/48 PASS**＋**章層 review M1–M8 全維 CLEAN、0 blocking/0 advisory**。as-built: Def 7.1–7.6／Thm 7.1–7.4（7.2/7.3/7.4 proved）／Strategy 7.1–7.3／Ex 7.1–7.22／0 figures（19 機會標記留 M2）。exports shipped: 積分 MVT §7.5、C¹ 弧長＋\(ds\) §7.6、表面積 §7.7。Codex 用量 ≈1.41M tok/9 call。`ch07_chapter-sweep-audit.md` |
| M2 圖（機會→繪製→D1–D8；gate-2 留 M4 後批次） | ✅ **gate-1 側完成（2026-07-18）** | ①機會覆核：7 subagent 平行——19 既有標記全 KEEP＋4 新增＝**23 張採納**、24 駁回、1 記錄不畫（裁決稿 `_audit/REVIEW-ch07-figure-opportunity.html`）。②2.5D pattern 與 Codex 收斂定案（`ch07_25d-pattern-codex-audit.md`；axis-relative oblique、0.35 橢圓比、物件專屬 geometry contract）。③**Figure 7.1–7.23 全數繪製**（buildPlot＋hand SVG；kit 擴充=areaBetween ×1）＋作者自查修 9 處（含 7.17/7.18/7.21 曲線太平重寫）。④**D1–D8 gate-1：7 subagent＋1 回歸——23/23 視覺 blocking 歸零**（首輪 3 blocking〔全在 §7.2：7.6 標籤夾殺、7.8 歸屬錯亂＋inset 非正方〕＋6 advisory 全修；§7.2 回歸 0/0 無新缺陷）。終值 build ✔／linebreak 0／render math=986、katex 0。報告（23 圖內嵌）`_audit/REVIEW-ch07-figure-audit.html`；紀錄 `ch07_figure-audit.md`。**圖視覺 gate-2 依「三閘 M4 後批次」規則留待後續（非 M2 範圍）** |
| M3 散文 S·A·V＋難度 learner-sim（合一輪） | ⬜ | 待跑 |
| M4 Mode C gap-check（①②合一） | ⬜ | 待跑 |
| 三閘 gate-2（數學／散文／圖） | ⬜ | M4 後批次 |
| M5 收尾（dashboard＋ROADMAP open-q） | ⬜ | 待跑 |

## Scaffolding notes

- `chapter7-print-standalone.html` to be cloned from chapter6 per the 7-loci recipe (PLAN-ch06
  Scaffolding notes): title + brand + runningHead + FIGS `{}` + content region + figure CSS strip
  + registry comments.
- `build.py` CHAPTERS registry: add `"ch07"` when `sec-7-1.html` first exists.
- M2 figure debt: fresh `--fig-7-*` width vars when figures land; `buildPlot` has rect/area fill
  primitives since Ch6; §7.2/§7.3/§7.7 solids need schematic inline SVG (new pattern for this
  book — candidates: light 2.5D "profile + swept outline" SVG, grayscale-survivable).
