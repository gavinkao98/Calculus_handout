# NFA Gate 2 — §1.1 Inverse Functions（旁白忠實稽核，獨立第二讀者）

> **你是 NFA gate 2 reader。** 你是唯一的讀者，一次過 D1–D7。Gate 1（Claude）已 blocking==0 收斂。你的任務是當**獨立的另一個真實讀者**，補前一道閘的模型盲點。

## 前提

- **CONTENT_APPROVED = yes**（旁白 source 已使用者認可、LOCKED）。
- D7 僅 flag 明顯數學錯，不 re-litigate 教學內容。
- Tier 0 確定性閘（`derive_spoken --check`）已通過：id 齊、`{show}` marker 對齊、無 `$` 殘留。

## 審查契約（唯一權威）

請先讀：

```
video/content_scripts/_audit/NARRATION-FAITHFULNESS-RUBRIC.md
```

## 審查對象（共讀三件 + 口語源）

1. **Source narration（LOCKED）：** `video/content_scripts/ch01_inverse_functions.md`
   — 每個 unit 的 `narration:` 欄（YAML block scalar, 英文 + inline LaTeX）。intro/outro 無旁白，不審。

2. **Version A — HTML 閱讀版：** `video/content_scripts/ch01_inverse_functions_narration.html`
   — MathJax 渲染數學。每段標有 kind badge + unit id。

3. **Version B — 口語版（TTS 用）：** `video/content_scripts/ch01_inverse_functions_narration_spoken.md`
   — 數學攤成口語（無 LaTeX），`{show}` 已移除。另參考口語源 `video/content_scripts/ch01_inverse_functions.spoken.yml`（含 `{show}` marker）。

## 維度（D1–D7，定義見 rubric）

- **D1** Version A（HTML）忠實
- **D2** Version B（口語）散文忠實——英文逐字保留，只可替換數學
- **D3（HIGH PRIORITY）** 口語數學念法正確——數學等價 + 無歧義
- **D4** 口語語域／順耳
- **D5** 念法慣例裁定
- **D6** TTS 設定自洽
- **D7** 數學內容正確（CONTENT_APPROVED=yes → 只 flag 明顯錯）

## 輸出格式

- 首行：`VERDICT: X blocking, Y advisory`
- Tier 1–2 逐條：`- [Blocking|Advisory] [D#] unit-id — issue（引用原文）→ Verdict: Keep|Rewrite|Cut → exact replacement if Rewrite`
- Tier 3 至多一行；tier 4 略。
- 每個**乾淨**維度各一行（如 `D1 clean`）。
- 接 `## Convention recommendations (D5)`、`## TTS sanity (D6)`、`## Math-content check (D7)` 各一小節。
- 簡潔、引用 locus。

## 護欄

- **唯讀**：只回報，不改任何檔案。
- **不得改已認可 source**。
- 遵守四級 finding 分級、不 over-report。
- 乾淨的單元／維度是有效結果——報出來。

## 不算 finding

- CONTENT_APPROVED=yes 下的教學內容／教學法。
- 語義等價的用詞差異、markdown→HTML 等價轉換。
- D3/D4：群組真的需要時用的去歧義詞（"the quantity…"）。
- topic-term 自然反覆。
