# Ch 3 S·A·V 散文閘——gate-2 稽核紀錄（Codex 跨模型獨立複核，version-controlled findings）

依 [`../../_audit/PROSE-AUDIT-RUBRIC.md`](../../_audit/PROSE-AUDIT-RUBRIC.md)（A 易懂性 U／B 流暢性 F／C 語意·高度·聲音 S·A·V）＋錨組 [`../../_audit/anchors/svc-exemplars.md`](../../_audit/anchors/svc-exemplars.md)。
**findings 必須留版控**（Codex 原始輸出落在 gitignored `scratchpad/`、換機即失），故本檔保存 findings 原文＋triage 處置。

> **時序：** Vale pre-flag（3 檔 0/0/0）→ gate-1（Claude ×3 逐節，0 blocking、advisory；裁決套 5 條 tighten、逐節回歸 PASS，裁決稿 [`../../_audit/REVIEW-ch03-svc-gate1.html`](../../_audit/REVIEW-ch03-svc-gate1.html)）→ 本 **gate-2（Codex）跨模型獨立複核** → **0 blocking、2 advisory（F5「the manuscript」露出）→ 使用者裁決採兩條 → 回歸 PASS**。

## 稽核設定

- **工具：** Codex CLI（`codex-cli 0.136.0`，PATH npm 版；`codex exec -s read-only -C <repo>`，全程不改檔）。
- **認證：** `Logged in using ChatGPT`——ChatGPT 訂閱配額（事前經使用者明確同意，2026-06-27）。
- **模型／用量：** `gpt-5.5` @ xhigh；本次 **81,096 tokens**。
- **輸入：** prompt 經 stdin 餵 raw UTF-8；`--output-schema codex_prose_schema.json` 強制結構化（全欄 required、`additionalProperties:false`、`verdict`/`level`/`dimension`/`section` 用 enum、無 min/max）。Codex 自讀 `PROSE-AUDIT-RUBRIC.md`＋`anchors/svc-exemplars.md`＋3 fragment（gate-1 已套 5 tightening 後的版本）——獨立於 gate-1 裁決。
- **日期：** 2026-06-27。

## Findings（Codex 原始輸出，逐字）

```json
{
  "verdict": "clean",
  "blocking_count": 0,
  "advisory_count": 2,
  "summary": "Convergence: blocking_count=0, so Chapter 3 passes gate-2. No reader-stranding U issues or load-bearing empty S/A defects found; only two local advisory register slips from visible manuscript-meta phrasing.",
  "findings": [
    {
      "section": "3.1",
      "locus": "sec-3-1.html:92, geometric inequality proof",
      "dimension": "F5",
      "level": "advisory",
      "issue": "Student-facing proof briefly shifts into source-manuscript commentary; the mathematical explanation is clear, but the register becomes editorial.",
      "original_text": "(The manuscript reads the same picture by splitting the outer triangle as OAC = OAB ∪ ABC; the corner piece ABC is what OAC adds to the inscribed triangle OAB, and it contains the circular segment between the chord AB and the arc.)",
      "recommendation": "Rewrite without the source-note frame: \"Equivalently, split the outer triangle as OAC = OAB ∪ ABC: the corner piece ABC is what OAC adds to the inscribed triangle OAB, and it contains the circular segment between the chord AB and the arc.\""
    },
    {
      "section": "3.2",
      "locus": "sec-3-2.html:45, pre-theorem setup",
      "dimension": "F5",
      "level": "advisory",
      "issue": "Visible reference to the source manuscript pulls the paragraph out of the handout's direct teaching voice.",
      "original_text": "The manuscript this chapter follows develops the chain rule alongside two results that already belong to Chapter 2 — the product rule (§2.5) and the fact that a differentiable function is continuous (§2.3, Theorem 2.1).",
      "recommendation": "Rewrite as: \"Two Chapter 2 results will be used freely here: the product rule (§2.5) and the fact that a differentiable function is continuous (§2.3, Theorem 2.1).\""
    }
  ]
}
```

## Triage（Claude 處置）

- **裁決：採納兩條 advisory（皆 F5「the manuscript」露出 student-facing 散文）。** 兩處皆非 blocking（gate 早在 blocking=0 收斂），但**正中 prompt 明訂規則**「student-facing 散文不可露出『the manuscript』等內容層語氣（HTML 註解 provenance 保留即可）——ch03 一併查」，且 **Ch2 gate-2 已採同類修正**（C2-3/C2-4，見 `REVIEW-ch02-svc-gate2.html`）。故從嚴採納。
  - **完整性掃描（Claude）：** `grep "manuscript"` 三 fragment 共 19 處——除上述 2 處 student-facing `<p>` 外，其餘 17 處全在 `<!-- -->` provenance 註解內（規則明文保留），無遺漏。Codex 抓到的 2 處即全部 student-facing 露出。
  - **C2-1 — §3.1:94（F5）→ 改。** 「(The manuscript reads the same picture by splitting…)」→「Equivalently, split the outer triangle as \(OAC = OAB \cup ABC\): …」。去掉 source-note frame 與括號、保留完整數學內容（角片 ABC＝OAC−OAB 的幾何解讀）。採 Codex 改寫。
  - **C2-2 — §3.2:45（F5）→ 改。** 「The manuscript this chapter follows develops the chain rule alongside two results…」→「**Alongside the chain rule, this section draws on** two results…」。改主詞去 manuscript meta、保留第二句「We take both as established and use them freely, without re-proving them here.」不變（避免 Codex 原議「will be used freely here」與第二句「use them freely」重複）。
- **回歸審核（CLAUDE.md 2026-06-12，手動比對）：PASS。** 改動屬外科手術級（兩句各換主詞框架、保語意、不動數學、不碰教學順序）。重 build＋render：`grep` 確認 student-facing「The manuscript reads…」「The manuscript this chapter follows…」皆 0、rendered content region 的「manuscript」全數落在 `<!-- -->` 註解、0 KaTeX err、math 653、7/7 圖 hydrate。兩處改寫文意與原句等價（仍交代「另一種切法看面積序」「兩條 Ch2 結果在此自由引用、不重證」）。不另燒 Codex 複跑（契約允許手動比對）。
- **收斂＝S/A blocking 全 0（兩閘）。** gate-1（Claude ×3）0 blocking＋gate-2（Codex）0 blocking；兩閘 advisory 皆經使用者逐條裁決（gate-1 採 5 tighten、gate-2 採 2 F5），無一擋稿。**prose gate 雙閘收斂。**

## 留證

- Codex 結構化輸出：上方 JSON（原 `scratchpad/codex_prose_out.json`＋`codex_prose_run.log`，gitignored scratch，已逐字轉錄於此）。
- prompt／schema：`scratchpad/codex_prose_prompt.txt`／`codex_prose_schema.json`（gitignored scratch；要旨記於本檔「稽核設定」）。
- gate-1（Claude ×3）裁決＋ Vale 0/0/0 見裁決稿 [`../../_audit/REVIEW-ch03-svc-gate1.html`](../../_audit/REVIEW-ch03-svc-gate1.html)；本 gate-2 裁決稿 [`../../_audit/REVIEW-ch03-svc-gate2.html`](../../_audit/REVIEW-ch03-svc-gate2.html)。
