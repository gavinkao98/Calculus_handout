# Ch 3 圖正確性閘——gate-2 稽核紀錄（Codex 視覺第二讀者 D1–D8，version-controlled findings）

依 [`../../_audit/FIGURE-AUDIT-RUBRIC.md`](../../_audit/FIGURE-AUDIT-RUBRIC.md)（D1–D8 視覺正確性／可讀性，propose-only、不確定降級、D5/D6 指控必回繪圖原始碼逐字核對）。
**findings 必須留版控**（Codex 原始輸出落在 gitignored `scratchpad/`、換機即失），故本檔保存 findings 原文＋triage 處置。範本沿用同目錄 [`ch03_example-supplement-audit.md`](ch03_example-supplement-audit.md)。

> **時序：** 圖機會閘＋視覺 gate-1（2026-06-21，Claude 多 auditor，Fig 3.7 一條 D6 等比座標修正後回歸，餘 0 blocking）→ 本 **gate-2（Codex 視覺第二讀者）跨模型獨立複核** → **1 blocking（Fig 3.6 D5 caption↔source）→ 使用者裁決 Option A 修圖 → 手動回歸 PASS** → 7 圖 blocking 全 0、收斂。

## 稽核設定

- **工具：** Codex CLI（`codex-cli 0.136.0`，PATH npm 版；`codex exec -s read-only -C <repo> -i <png…>`，全程不改檔）。
- **認證：** `Logged in using ChatGPT`——ChatGPT 訂閱配額（事前經使用者明確同意，2026-06-27）。
- **模型／用量：** `gpt-5.5` @ xhigh；本次 **120,683 tokens**。
- **輸入：** 7 張 2× PNG（`shot.mjs … figures` 逐 `<figure>` 截）依序 `-i` 附上：Fig 3.1 sector-inequality／3.2 squeeze-limit／3.3 sin-cos-slope／3.4 shm-triple／3.5 composed-mapping／3.6 remainder-tangent／3.7 arcsin-vertical-tangent。prompt 經 stdin 餵 raw UTF-8；`--output-schema codex_fig_schema.json` 強制結構化（全欄 required、`additionalProperties:false`、`overall_verdict`/`level`/`dimension` 用 enum、無 min/max）。
- **ground truth：** Codex 自讀 `handout/_audit/FIGURE-AUDIT-RUBRIC.md`、`handout/chapter3-print-standalone.html` 的 `const FIGS`（7 圖繪圖源碼）、`handout/fragments/ch03/sec-3-{1,2,3}.html`（figcaption／散文）——獨立於 gate-1 與本 session 框架。
- **日期：** 2026-06-27。

## Findings（Codex 原始輸出，逐字）

```json
{
  "overall_verdict": "needs_fixes",
  "total_blocking": 1,
  "total_advisory": 0,
  "summary": "Gate 2 is not clear: there is one blocking figure-caption mismatch in Figure 3.6. The other six Chapter 3 figures pass the visual correctness and readability audit.",
  "per_figure_clean": [
    "3.1 sector-inequality — D1-D8 clean",
    "3.2 squeeze-limit — D1-D8 clean",
    "3.3 sin-cos-slope — D1-D8 clean",
    "3.4 shm-triple — D1-D8 clean (dashed extrema align with velocity zeros; source formulas match caption)",
    "3.5 composed-mapping — D1-D8 clean (schematic increment widths intentional)",
    "3.7 arcsin-vertical-tangent — D1-D8 clean (endpoint hollow markers, vertical tangents, centre slope-1)"
  ],
  "finding": {
    "figure_id": "remainder-tangent",
    "figure_num": "3.6",
    "dimension": "D5",
    "level": "blocking",
    "evidence": "The caption says \"Halving h (right panel)\", but the source draws the pair as panel(1.35, \"larger h\") and panel(0.5, \"smaller h\") on the same plot scale, so the right interval is 0.5/1.35 ≈ 0.37 of the left, not one half.",
    "why": "A same-scale comparison that is described as halving h should show the right x0-to-x0+h spacing as half the left spacing; the current coordinates contradict that caption claim.",
    "fix": "Either set the right-panel h to 0.675, half of 1.35, or revise the caption/prose to say \"making h smaller\" instead of \"halving h\"."
  }
}
```

## Triage（Claude 處置）

- **驗證（rubric verifier 紀律：D5 指控回繪圖原始碼逐字核對）：** confirmed real。源碼 `chapter3-print-standalone.html:1628` `panels: [panel(1.35, "larger h"), panel(0.5, "smaller h")]`；caption `fragments/ch03/sec-3-2.html:104`「Halving \(h\) (right panel) …」。0.5/1.35 = 0.370 ≠ 0.5 → caption「Halving」與圖實畫的 0.37× 矛盾，D5 blocking 成立。非 PNG 像素誤讀（由源碼數值即可判定）。gate-1（2026-06-21）漏掉、gate-2 跨模型補上——雙閘價值體現。
- **裁決：採納 1 blocking。使用者選 Option A（修圖、令「Halving」屬實）。**
  - **B1 — Figure 3.6（D5）→ 修圖。** `panel(0.5, "smaller h")` → `panel(0.675, "smaller h")`（=1.35/2）。本例 remainder 恰為純二次 `R(h)=0.34 h²`，故 h 減半 → gap 成四分之一（左 R≈0.620 → 右 R≈0.155），正是 caption「shrinks that gap far faster than \(h\) itself — the geometric content of \(R(h)/h \to 0\)」最漂亮的視覺：減半的 h 配上四分之一的 gap。選 Option A（非 B 改 caption）係因 caption 刻意以「Halving」承載 R/h→0 的量化直覺，修圖最忠於原作意圖、且強化教學點。FIGS 源碼註解（standalone:1597–1602「halving h … SAME scale」）本就如此描述，修圖後反而與註解一致。
  - 改動屬外科手術級（standalone FIGS 單一數值 0.5→0.675；fragment／caption／編號／其餘 6 圖皆未動）。
- **回歸審核（CLAUDE.md 2026-06-12，「Codex 或手動比對均可」）：手動回歸 PASS。**
  - 源碼算術：0.675 = 1.35/2，右 panel `x₀→x₀+h` 恰為左之半；xe = 1.675 < xmax 2.85（在框內）；右 R = 0.34·0.675² = 0.155，左 R = 0.34·1.35² = 0.620（gap 成四分之一）。
  - 重 render（`shot.mjs … figures`）＋目視：兩 panel 同尺度、右側增量為左之半、R(h) gap 明顯縮小、labels（R(h)/x₀/x₀+h/f）無碰撞無裁切、0 KaTeX err、7/7 圖 hydrate。D5 現與 caption 一致，D1–D8 全 clean。
  - 改動單一座標、使 caption 屬實、且經源碼＋render 雙重確認無新問題 → 不另燒一次 Codex 複跑（契約允許手動比對）。
- **收斂＝7 圖視覺 blocking 全 0**（達成：1 blocking 已修＋回歸 PASS；其餘 6 圖兩閘皆 clean）。

## 留證

- Codex 結構化輸出：上方 JSON（原 `scratchpad/codex_fig_out.json`＋`codex_fig_run.log`，gitignored scratch，已轉錄於此；per-figure clean_note 摘錄）。
- prompt／schema／7 PNG：`scratchpad/codex_fig_prompt.txt`／`codex_fig_schema.json`／`render/s3fig-*.png`（gitignored scratch；要旨記於本檔「稽核設定」）。
- gate-1（圖機會＋視覺 D1–D8）見 [`../../_audit/REVIEW-ch03-figure-opportunity.html`](../../_audit/REVIEW-ch03-figure-opportunity.html)；本 gate-2 裁決稿 [`../../_audit/REVIEW-ch03-figure-audit-gate2.html`](../../_audit/REVIEW-ch03-figure-audit-gate2.html)。
