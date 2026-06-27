# Ch 4 S·A·V 散文閘——gate-2 稽核紀錄（Codex 跨模型獨立複核）＋ 完整性掃描（version-controlled findings）

依 [`../../_audit/PROSE-AUDIT-RUBRIC.md`](../../_audit/PROSE-AUDIT-RUBRIC.md)（A 易懂性 U1–U5／B 流暢性 F1–F5／C 語意·高度·聲音 S·A·V）＋錨組 [`../../_audit/anchors/svc-exemplars.md`](../../_audit/anchors/svc-exemplars.md)。
**findings 必須留版控**（Codex 原始輸出落在 gitignored `scratchpad/`、換機即失），故本檔保存 findings 原文＋triage。範本沿用同目錄 [`ch04_math-audit-gate2.md`](ch04_math-audit-gate2.md)。

> **時序：** gate-1（Claude ×5 逐節 `handout-prose-audit`，0 blocking／17 advisory，⛳ 套 4 條建議採 copyedit，裁決稿 [`../../_audit/REVIEW-ch04-svc-gate1.html`](../../_audit/REVIEW-ch04-svc-gate1.html)＋[`-applied`](../../_audit/REVIEW-ch04-svc-gate1-applied.html)）→ 使用者授權 → 本 **gate-2（Codex）** 複審後版本 → **0 blocking／0 advisory** → 但 **Claude 完整性掃描** 另抓 3 處 student-facing「the manuscript」露出（兩閘皆漏）→ ⛳ 裁決 3 條全採、去露出＋手動回歸 PASS → **S·A·V 雙閘收斂**。

## 稽核設定

- **工具：** Codex CLI（`codex-cli 0.136.0`，PATH npm 版；`codex exec -s read-only -C <repo>`，全程不改檔）。
- **認證／配額：** Logged in using ChatGPT——**ChatGPT 訂閱配額**（事前經使用者明確同意，2026-06-27）。
- **模型／用量：** `gpt-5.5`（`model_reasoning_effort=xhigh`）；本次 **154,714 tokens**、單輪收斂。
- **輸入：** prompt 經 bash `codex exec - < prompt.txt` 餵 raw UTF-8；`--output-schema schema_ch04_svc.json`（全欄 required、`additionalProperties:false`、`verdict`/`category` 用 enum、無 min/max）；`-o` 寫 last message。被審物 ＝ gate-1 已套 4 copyedit 後的 `fragments/ch04/sec-4-{1..5}.html`。
- **ground truth：** Codex 自讀 `PROSE-AUDIT-RUBRIC.md`＋`anchors/svc-exemplars.md`＋`CLAUDE.md`＋`PLAN-ch04.md §3`＋5 fragment——獨立於 gate-1 裁決。
- **日期：** 2026-06-27。

## Findings（Codex gate-2 原始輸出，逐字）

```json
{
  "verdict": "converged",
  "blocking_count": 0,
  "advisory_count": 0,
  "per_section": [
    {"section":"§4.1","blocking":0,"advisory":0,"note":"Checked chapter opener, section motivation, definition glosses, convergence setup, tail-bound explanation, and handoff to §4.2."},
    {"section":"§4.2","blocking":0,"advisory":0,"note":"Checked continuity motivation, Cauchy/Bolzano-Weierstrass explanatory bridges, sign-change setup, exponent-law proof narration, and section recap."},
    {"section":"§4.3","blocking":0,"advisory":0,"note":"Checked the Chapter 2 contrast, difference-quotient reduction, explicit-bound explanation, derivative proof bridge, and forward handoff to MVT."},
    {"section":"§4.4","blocking":0,"advisory":0,"note":"Checked Rolle/MVT motivation, extrema definitions and glosses, theorem lead-ins, strategy prose, examples' explanatory text, and logarithm handoff."},
    {"section":"§4.5","blocking":0,"advisory":0,"note":"Checked logarithm motivation, inverse/range setup, continuity and derivative proof narration, product-law caution, general-powers bridge, capstone, and chapter summary."}
  ],
  "findings": [],
  "overall_conclusion": "Gate-2 converges: I found 0 blocking issues in comprehensibility or S/A altitude/substance, and no reportable Tighten/Optional/Voice advisory in the current post-edit prose. The chapter reads substantive and pedagogically bridged throughout; neutral passages are doing explanatory work rather than occupying empty motivational slots."
}
```

## 完整性掃描（Claude，gate-2 後）——3 處 student-facing「the manuscript」露出（兩閘皆漏）

`grep -i "manuscript"` ×5 fragment：~33 處，其中 **3 處在 student-facing `<p>`**、其餘皆在 `<!-- -->` provenance 註解（規則保留）。3 處 F5 register slip（student 看不到手稿、露出即內容層語氣），比照 Ch2（commit `cb1bf3f` 套 5 處）／Ch3（gate-2 套 2 處）去露出慣例。⛳ 使用者裁決 **3 條全採**：

| id | locus | diff（去露出，保語意/數學） |
|---|---|---|
| L1 | `sec-4-1.html` 行 99（Completeness env-body） | `(`~~`The manuscript records this as a basic Property`~~ → `This is a basic structural property`~~`）`~~` of ℝ; we take it as a stated theorem and do not prove it here.)` |
| L2 | `sec-4-2.html` 行 101（Cauchy 導入） | ~~`The manuscript states this equivalence and uses it directly. We instead prove it, because`~~ → `This equivalence is often taken for granted and used directly; we prove it here instead, because` …（後接依賴鏈論點不變） |
| L3 | `sec-4-2.html` 行 220（指數律 Step 3） | `(`~~`with the manuscript's notation`~~ → `also written` `\binom{ℓ}{m}=C^{ℓ}_{m}` `in older notation)`——**觸 D8**（§4.2 首見 cross-ref 手稿記號）：**保留** `C^{ℓ}_{m}` 橋接、只去「manuscript」字眼 |

**回歸（manual regression）：** 改 `sec-4-{1,2}.html` → `python build.py ch04` → render `1011 math nodes／0 KaTeX err`；回歸 `grep` 確認 **0 student-facing「manuscript」露出**（其餘全在註解）。

## Triage（Claude 處置）

- **Codex gate-2 裁決：converged，0 finding**——Codex 獨立複核五節（含 gate-1 已套 4 copyedit），無 U 卡關、無 S/A 空句、無可報 advisory，與 gate-1（0 blocking）一致。
- **完整性掃描 3 處 F5：兩閘皆漏、由人工 `grep` 掃描補抓**——印證「自動閘 + 人工完整性掃描」雙保險的價值（Ch3 gate-2 同樣靠此掃描抓到 2 處）。3 條經 ⛳ 全採、去露出、手動回歸 PASS。**未動 HTML 註解 provenance**（規則保留）。L3 觸 D8：保留 `C^{ℓ}_{m}` 橋接、僅去 meta 字眼，未違 D8 用意。
- **S·A·V 雙閘收斂（blocking = 0）**：gate-1（Claude ×5）+ gate-2（Codex gpt-5.5）皆 0 blocking；完整性掃描 3 處 F5 advisory 全採並回歸。

## 留證

- Codex 結構化輸出：上方 JSON（原 `scratchpad/result_ch04_svc.json`＋`codex_ch04_svc.log`，gitignored scratch，已逐字轉錄）。
- prompt／schema：`scratchpad/prompt_ch04_svc.txt`／`schema_ch04_svc.json`（gitignored scratch；要旨記於「稽核設定」）。
- 裁決稿：[`../../_audit/REVIEW-ch04-svc-gate2.html`](../../_audit/REVIEW-ch04-svc-gate2.html)（gate-2 0/0 ＋ 完整性掃描 3 處已套・回歸 PASS）。gate-1 見 [`../../_audit/REVIEW-ch04-svc-gate1.html`](../../_audit/REVIEW-ch04-svc-gate1.html)＋[`-applied`](../../_audit/REVIEW-ch04-svc-gate1-applied.html)。
