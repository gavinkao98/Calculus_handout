# Ch 2 課文範例補充——選題稽核紀錄（Codex，version-controlled findings）

依 [`CONTENT_SOURCING.md`](../../CONTENT_SOURCING.md) §流程 3.iii「裁決前先過一輪選題稽核」建立。
契約沿用 [`CONTENT_DIRECTION.md`](../../CONTENT_DIRECTION.md) ⑤：**math／faithfulness／aptness（對症性）＝blocking；source-license／format＝advisory**。
**findings 必須留版控**（Codex 原始輸出落在 gitignored `.tmp/`、換機即失），故本檔保存 findings 原文＋triage 處置。

> **時序註：** ch02 的選題稽核在 2026-06-22 import **之後**才補跑（裁決＝使用者「六題全部補上」先於本稽核）。
> 因此 Codex 審到的是**已套用且已過內部回歸審核**的版本（含對 Ex 2.13 歸因、Ex 2.17 Caution 矛盾兩條 advisory 的修正）。
> 與 ch01「裁決前稽核」的時序不同，但稽核維度與留證要求相同。

## 稽核設定

- **工具：** Codex CLI（`codex-cli 0.136.0`，`codex exec`），`--sandbox read-only`（全程不改檔，single-writer 紀律）。
- **認證：** `codex login status` → 「Logged in using ChatGPT」——走 **ChatGPT 訂閱配額**，非 API key 計費。
- **模型／用量：** 預設 `gpt-5.5` @ `xhigh` reasoning；本次 **125,346 tokens**（吃訂閱額度）。
- **輸入：** prompt 以 bash `cat … | codex exec -` 餵 raw UTF-8 bytes（避開 PowerShell ANSI／CJK 重編碼坑，見 CONTENT_DIRECTION §5）；`--output-schema` 強制結構化輸出（schema：全欄 required、無 `min/max`、`level` 用 enum、`additionalProperties:false`）。
- **ground truth：** Codex 自行讀取 `handout/fragments/ch02/sec-2-1…2-5.html`（5 個 fragment），對 6 筆新例（2.12、2.13、2.16、2.17、2.21、2.23）做四維稽核——獨立於本 session 的框架。
- **日期：** 2026-06-22。

## Findings（Codex 原始輸出，逐字）

```json
{
  "blocking_count": 0,
  "advisory_count": 0,
  "verdict": "clean",
  "summary": "All six imported examples check out against the chapter sequence: the math and algebra are correct, the potentially delicate negative- and fractional-exponent uses are acknowledged and grounded in prior text, the claimed gaps are real enough relative to the existing examples, and the CLP-1 source/license framing is internally consistent. No blocking or advisory findings.",
  "findings": []
}
```

## Triage（Claude 處置）

- **裁決：`clean`（0 blocking／0 advisory）——無 finding，無需修改、無需 re-audit。**
- **與內部回歸審核相互印證：** 本 session 先前已跑一輪內部對抗式回歸審核（6 數學 agent ＋ 1 完整性 agent，見 [`ch02_example-imports.md`](ch02_example-imports.md) §回歸審核），結論同為「數學 6/6 正確、編號／交叉引用 clean」，並已修兩條內部一致性 advisory。Codex 審到修正後的版本，**獨立判定 clean**——兩條獨立路徑（內部 Claude agents ＋ 外部 Codex/gpt-5.5）一致，無 blocking 穿過。
- **特別印證點：** Codex summary 明確點名「the potentially delicate negative- and fractional-exponent uses are **acknowledged and grounded in prior text**」——正是先前內部稽核對 Ex 2.16（負指數引 Caution）與 Ex 2.17（分數指數加延後保留＋§2.2 Example 2.7 立論）所做修正的目標；外部模型確認該處理已足。
- **核心幻覺假說（CONTENT_DIRECTION §5 open question）旁證：** 本批為低幻覺加法（題庫官方解為主、僅一筆 authored），非最硬的具名結果壓測；兩模型一致 clean 屬正面但低資訊量的樣本，不推進該 open question。

## 留證

- Codex 結構化輸出：上方 JSON（原 `.tmp/ch02-codex-audit/findings.json`，gitignored，已轉錄於此）。
- prompt／schema：`.tmp/ch02-codex-audit/{prompt.txt,schema.json}`（gitignored scratch，稽核後清理；prompt 全文要旨已記於本檔「稽核設定」）。
