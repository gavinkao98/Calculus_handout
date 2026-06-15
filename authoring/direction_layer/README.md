# direction_layer —— 六階方向層流程的驗證紀錄

> 六階「方向層」流程已**畢業**為頂層正式文件 [`../../CONTENT_DIRECTION.md`](../../CONTENT_DIRECTION.md)。
> 本資料夾保留該流程的**端到端驗證紀錄**（哪幾節怎麼跑、收斂結果），作為 provenance。

## 這資料夾是什麼

「方向層」在「老師掃描手稿 → 完整講義一節」之間補上一道**方向閘**，讓「**這是不是我要的方向**」從不可檢核變可檢核——一節可以數學全對、稽核 8/8，仍然是「往錯方向收斂得很精緻」。流程的權威定義見 [`../../CONTENT_DIRECTION.md`](../../CONTENT_DIRECTION.md)。

本資料夾是它的驗證留存：

- [`ch01/`](ch01/) — ch01 §1.1／§1.2 逐節的 seed／brief／draft／audit findings 與 [`RESULT_ch01.md`](ch01/RESULT_ch01.md)（含整章狀態）。
- [`test/`](test/) — §4.2 高風險節端到端首跑（[`RESULT_s42.md`](test/RESULT_s42.md)）。

> 註：這些早期驗證跑在 LaTeX 格式上（draft 為 `.tex`），是流程**驗證的歷史紀錄**；流程本身後續換源到 HTML（見 [`../../CONTENT_DIRECTION.md`](../../CONTENT_DIRECTION.md) ④）。

## 與 seed_converge 的分工

| 資料夾 | 管什麼 |
|---|---|
| [`../seed_converge/`](../seed_converge/) | **機制**：雙模型自動收斂、多模態圖 critic、訂閱制 review 迴圈（零件與壓測）。 |
| `direction_layer/`（本資料夾） | **流程**的驗證紀錄；流程定義已畢業至 [`../../CONTENT_DIRECTION.md`](../../CONTENT_DIRECTION.md)。 |
