# Ch1/Ch2 開場＋章末 summary（本輪新寫）——S·A·V 散文閘 gate-2 紀錄（Codex 跨模型獨立複核）

依 [`../../_audit/PROSE-AUDIT-RUBRIC.md`](../../_audit/PROSE-AUDIT-RUBRIC.md)（A 易懂性 U1–U5／B 流暢性 F1–F5／C 語意·高度·聲音 S·A·V）＋錨組 [`../../_audit/anchors/svc-exemplars.md`](../../_audit/anchors/svc-exemplars.md)。
**findings 必須留版控**（Codex 原始輸出落 gitignored `scratchpad/`、換機即失），故本檔保存 findings 原文＋triage。範本沿用 [`../ch04/ch04_svc-gate2.md`](../ch04/ch04_svc-gate2.md)。

> **範圍：** 本輪只審「新寫入」的三段——Ch2 章開場（`fragments/ch02/sec-2-1.html` 第一個 `<article>`：concat 章標題＋lead＋learning objectives）、Ch1 章末 Chapter summary（`fragments/ch01/sec-1-6.html` 末 3 段）、Ch2 章末 Chapter summary（`fragments/ch02/sec-2-5.html` 末 4 段）。**非全章稽核**——各章本體為先前 session 已過閘基線。

> **時序：** gate-1（Claude `handout-prose-audit` ×3，0 blocking）→ 內容稽核 workflow（散文回歸 re-audit ×3 + 對抗式數學保真 ×2）抓到並修一處 Ch1 數學引用 blocking（`roots`→`rational functions`＋補引 Proposition 1.1）→ 使用者授權 → 本 **gate-2（Codex）** 複審 → **0 blocking／2 advisory** → **Claude 完整性掃描**（student-facing meta 露出）→ **0 露出（乾淨）** → ⛳ 2 advisory 皆裁決保留 → **S·A·V 雙閘收斂**。

## 稽核設定

- **工具：** Codex CLI（`codex-cli 0.136.0`，PATH npm 版；`codex exec -s read-only -C <repo>`，全程不改檔）。
- **認證／配額：** Logged in using ChatGPT——**ChatGPT 訂閱配額**（事前經使用者明確同意，2026-06-28）。
- **模型／用量：** `gpt-5.5`（reasoning xhigh）；本次 **103,619 tokens**、單輪收斂。
- **指令：** `codex exec -s read-only -C <repo> --output-schema svc_gate2_schema.json -o svc_gate2_out.json - < svc_gate2_prompt.txt`（prompt 經 bash stdin 餵 raw UTF-8；schema 全欄 required、`additionalProperties:false`、`dimension`/`severity` 用 enum、無 min/max）。
- **輸入：** 被審物＝gate-1 已套切句／聲音修正、且已修數學引用後的最新稿（三段新內容）。
- **ground truth：** Codex 自讀 `PROSE-AUDIT-RUBRIC.md`＋`anchors/svc-exemplars.md`＋`CONTENT_SPEC.md` §3/§4＋三段 fragment——獨立於 gate-1 裁決。
- **日期：** 2026-06-28。

## Findings（Codex gate-2 原始輸出，逐字）

```json
{
  "converged": true,
  "blocking_count": 0,
  "advisory_count": 2,
  "targets": [
    {
      "target": "Ch2 章開場 — handout/fragments/ch02/sec-2-1.html 第一個 <article>",
      "verdict": "0 blocking, 1 tighten, 0 optional, 0 voice",
      "findings": [
        {"dimension":"B-fluency","severity":"tighten","where":"learning outcomes bullet list（bullet 1 與 bullet 4）","quote":"state the limit definition ... move fluently between the equivalent forms ... and apply it ...; / differentiate any polynomial and the exponential function (e^x) using ... and the series-based derivation of (e^x)'=e^x, and compute higher-order derivatives ...","why":"兩個 bullet 各自承載多個動作，掃讀負荷偏高；讀者仍懂，但學習成果清單的 5 秒查閱性可再收緊。","suggestion":"每個 bullet 壓成一條主線（如以 equivalent limit definitions 為主動詞、series-based derivation 另起一句）。"}
      ],
      "clean_dimensions": "A-understandability、S-substance、A-altitude、V-voice 乾淨；章開場有明確前章銜接、核心 payoff、幾何/物理/代數三讀法，學習成果具體可操作。"
    },
    {
      "target": "Ch1 章末 Chapter summary — handout/fragments/ch01/sec-1-6.html 末 3 段",
      "verdict": "0 blocking, 0 tighten, 0 optional, 0 voice",
      "findings": [],
      "clean_dimensions": "A/B/S/A高度/V 皆乾淨；三段按 inverse → limits → ε-δ rigor → Ch2 derivative 弧線推進，重述密度符合章末 summary 查閱角色。"
    },
    {
      "target": "Ch2 章末 Chapter summary — handout/fragments/ch02/sec-2-5.html 末 4 段",
      "verdict": "0 blocking, 0 tighten, 1 optional, 0 voice",
      "findings": [
        {"dimension":"B-fluency","severity":"optional","where":"summary 最後一段（line 333）與緊鄰既有 line 318 section-closing 段落","quote":"With these rules we can differentiate any function assembled from powers and the exponential by adding, scaling, multiplying, and dividing. Two things still lie outside their reach: composition ...","why":"與前一既有段落的 toolkit／adding-scaling-multiplying-dividing／composition／chain-rule 高度重疊；summary 回收章末 fence 故不算缺陷，僅連讀時略有回音。","suggestion":"若要降重複，末段改為更總結式起手（如 \"the remaining debts are clear: composition ... and the power rule beyond integer exponents\"），保留 Ch3 fence 而少重複 toolkit 句。"}
      ],
      "clean_dimensions": "A-understandability、S-substance、A-altitude、V-voice 乾淨；四段按 point derivative → function/existence → rules → forward debts 推進，無空泛 AI 承諾句或高度跳步。"
    }
  ],
  "summary": "總 blocking 數為 0；gate 2 通過。全輪只有 2 個 advisory：Ch2 章開場 learning outcomes 可收緊掃讀負荷，Ch2 章末 summary 與緊鄰既有 section-closing 有輕微重複。"
}
```

## 完整性掃描（Claude，gate-2 後）

`grep -nE "manuscript|the author|these notes|this handout|seed file"` ×3 新內容 fragment：所有 `manuscript` 命中**全在頂部 `<!-- -->` provenance 註解**（`sec-2-1.html` 行 2、`sec-2-5.html` 行 2–3／22–23），規則保留；**student-facing 散文（開場 lead/objectives、兩段 summary）零 meta 露出**。Ch1 summary 完全無 `manuscript`。→ 完整性掃描乾淨，無補抓。

## Triage（Claude 處置）

- **Codex gate-2：converged，0 blocking／2 advisory**——與 gate-1（0 blocking）一致，跨模型確認三段散文無 U 卡關、無 S/A 空句、無高度錯誤。
- **Advisory 1（Ch2 opener objectives，tighten）→ 保留。** 理由：使用者明確指示 Ch2 opener 的 learning objectives「移植 legacy ch02 ＋核實」，多子句正是 legacy 原形；advisory-only、兩閘皆 0 blocking；壓縮＝改寫，違背移植決定。
- **Advisory 2（Ch2 summary 末段重疊，optional）→ 保留。** 理由：章末 summary 是獨立的永久查閱頁（§1/§3 lookup-protected），Codex 自評「不算缺陷」；gate-1／內容稽核 workflow／本 gate-2 三輪一致判 optional 並保留。
- 兩 advisory 皆不改 → 無內容變更 → 無回歸需求。
- **S·A·V 雙閘收斂（blocking = 0）**：gate-1（Claude ×3）＋ gate-2（Codex gpt-5.5 xhigh）皆 0 blocking；2 advisory 經 ⛳ 裁決保留並記錄理由。

## 留證

- Codex 原始 last-message JSON：gitignored `scratchpad/svc_gate2_out.json`（換機即失，已逐字轉錄於上）。
- 對應使用者交付：[`../../_audit/REVIEW-ch01-ch02-opener-summary-applied.html`](../../_audit/REVIEW-ch01-ch02-opener-summary-applied.html)（已寫入內容報告，含雙閘狀態）。
