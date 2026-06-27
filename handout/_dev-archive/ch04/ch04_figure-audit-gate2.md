# Ch 4 圖正確性 D1–D8——gate-2 稽核紀錄（Codex 視覺第二讀者，version-controlled findings）

契約：[`../../_audit/FIGURE-AUDIT-RUBRIC.md`](../../_audit/FIGURE-AUDIT-RUBRIC.md)（D1–D8 視覺正確性）。**blocking＝視覺/數學錯誤或誤導；advisory＝美學/可讀小瑕。**
**findings 必須留版控**（Codex 原始輸出落 gitignored scratchpad、換機即失），故本檔保存 findings 原文＋triage。

> **時序：** 圖機會 gate-1（`wf_a514bfba-3d6`，3 機會 medium）→ 使用者裁定三個都畫 → 三圖落地（Figure 4.1 completeness／4.3 squeeze／4.6 reciprocal-slope，cascade renumber partial-sums→4.2／mvt→4.4／reflection→4.5）→ **D1–D8 gate-1**（`wf_d3a33dbb-6f7`，6 圖×general-purpose audit＋critic，**0 blocking／1 advisory**）→ 本 **gate-2（Codex 視覺第二讀者）跨模型獨立複核** → **0 blocking／1 advisory，兩閘一致**。

## 稽核設定

- **工具：** Codex CLI（`codex-cli 0.136.0`，PATH npm 版；`codex exec -s read-only`，全程不改檔）。
- **認證／計費：** ChatGPT 訂閱配額（使用者一次性授權三道 gate-2）。
- **模型／用量：** `gpt-5.5` @ `xhigh`；本次 **77,984 tokens**。
- **輸入：** 6 張 2× render PNG 經 `-i` 旗標附入（順序 Figure 4.1→4.6）；prompt 含各圖 FIGS 數值參數＋figcaption，要求 Codex 自讀 `FIGURE-AUDIT-RUBRIC.md`＋`chapter4-print-standalone.html` 的 `const FIGS`＋三節 figcaption 獨立核對；`--output-schema` 強制結構化（figure/dimension/level/verdict 用 enum）。
- **重點：** 三張新圖（4.1 完備性／4.3 Thm A 夾擠／4.6 倒數斜率）的數學幾何（鏡射對稱、斜率符號、特殊點、等比尺）。
- **日期：** 2026-06-27。

## Findings（Codex 原始輸出，逐字）

```json
{
  "blocking_count": 0,
  "advisory_count": 1,
  "verdict": "pass",
  "summary": "Gate-2 recheck finds no mathematical or caption-consistency blockers. The three new figures 4.1, 4.3, and 4.6 match the FIGS source and captions: monotone bounded dots are discrete, the extremum secants have the correct signs with a horizontal tangent, and the exp/log tangent slopes are reciprocal under equal-axis reflection. I agree with the prior minor readability advisory on Figure 4.2.",
  "findings": [
    {
      "figure": "4.2",
      "dimension": "D4",
      "level": "advisory",
      "issue": "The left x-axis tick label can read a little like “2” because the minus sign is visually crowded/crossed by a gray partial-sum curve near the left edge.",
      "evidence": "In image 2, the “-2” tick at the lower left sits under/near descending gray partial-sum geometry. The FIGS source sets xticks to -2, -1, 1 and plots P1-P4 over x in [-2.1, 1.55], so the tick value is mathematically correct; this is only a legibility issue.",
      "fix": "Nudge the -2 tick label slightly lower/left, add a tiny white label backing, or shorten/clip the nearby gray curve only around the label region."
    }
  ]
}
```

## Triage（Claude 處置）

- **裁決：gate-2 收斂（0 blocking）。** 三張新圖 Codex 獨立確認數學幾何全對（完備性點列離散且 bounded、夾擠割線符號＋水平切線、exp/log 切線斜率在等比反射下互倒）；既有 3 圖重編號後無回歸。
- **雙閘一致（雙模型閘的價值）：** gate-1（Claude 6 audit＋critic）與 gate-2（Codex gpt-5.5 xhigh）對 6 圖結論完全一致——**0 blocking、同一條 advisory**（Fig 4.2 的 `-2` 刻度負號被灰 P 曲線壓，D4 可讀性）。兩模型對三張新圖的鏡射對稱/斜率/特殊點/等比尺判定相同，**幻覺未穿過任一模型**。
- **唯一 advisory（Fig 4.2）→ 不動（記錄）。** Figure 4.2（partial-sums，原 Figure 4.1）是 Mode A 已簽核既有圖；該 advisory 為既存小瑕，非本輪新圖引入。Codex 自附三個 fix 選項皆須動到簽核過的曲線/刻度/window。依外科手術原則（只動非動不可者、不改簽核內容為 cosmetic）＋兩閘皆判 advisory 非 blocking＋刻度值數學正確（位置可無歧義回推），**裁定不動、記錄為已知 advisory**。
- **回歸審核：** 0 blocking 無修正；回歸對象＝已完成的 render 自驗（6 圖 hydrate、Figure 4.1–4.6 連續、0 mjx-merror）。不另燒 Codex 複跑。

## 留證

- Codex 結構化輸出：上方 JSON（原 `scratchpad/codex_fig_out.json`＋`codex_fig_run.log`，gitignored，已轉錄於此）。
- prompt／schema：`scratchpad/codex_fig_prompt.txt`／`codex_fig_schema.json`（gitignored；要旨記於本檔「稽核設定」）。
- gate-1（6 audit＋critic）原始裁決＋三張新圖目視見套用報告 [`../../_audit/REVIEW-ch04-figure-applied.html`](../../_audit/REVIEW-ch04-figure-applied.html)（內嵌 3 圖 PNG）。
