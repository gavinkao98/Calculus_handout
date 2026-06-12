# Ch 1 課文範例補充——Codex 選題稽核紀錄

> 為什麼有這份檔：Codex 的原始輸出寫在 `.tmp/`（gitignored、換機即失），
> 使用者看不到也帶不走。依 docs-first 規則，把兩輪 findings 原文留進版控。
> 被審物：[`ch01_example-supplement-review.html`](ch01_example-supplement-review.html)；
> 稽核 prompt：[`PROMPT-ch01-example-selection-audit.md`](PROMPT-ch01-example-selection-audit.md)；
> 流程依據：[`CONTENT_SOURCING.md`](../../CONTENT_SOURCING.md) 2.4。

## 環境

- 日期：2026-06-12（公司機）。
- 引擎：`codex exec --sandbox read-only`，桌面 app 捆的 CLI 0.130.0-alpha.5，
  model `gpt-5.5`、reasoning effort `xhigh`、唯讀沙盒。
- 配額：全量稽核 ~161k tokens、範圍限定複審 ~60k tokens（走 ChatGPT 訂閱）。
- 三次嘗試才跑通（PATH 無 codex → 0.119 舊 CLI 拒 gpt-5.5 → 0.130 成功；
  `service_tier="priority"` 需暫時註解，已還原）。細節見稽核 prompt 檔末備忘。

---

## 第一輪：全量稽核（findings 原文）

> 21 筆候選的數學驗算全數通過；1 blocking ＋ 2 advisory。

- **[blocking] Mooculus 授權標示與本地題庫授權檔不一致。**
  證據：被審物標 `Mooculus …（CC BY-NC 3.0）` 與 `Mooculus 逐題＝CC BY-NC 3.0`
  （review:68、review:370）；但本地 Mooculus 授權檔為
  `Attribution-NonCommercial-ShareAlike` 且指向 `by-nc-sa/4.0`
  （`problem_banks/mooculus/license.md:2`、`:5`）。
  建議修法：把 Mooculus 授權標示改成 `CC BY-NC-SA 4.0`；若確有逐題 `CC BY-NC 3.0`
  依據，需在 source/import record 補可查證據。

- **[advisory] O1.2-d 的插入點早於 `arccos` 定義。**
  證據：被審物說插入「兩個 Caution 之後」（review:174），但兩個 Caution 在
  `sec-1-2.html` 第 35、51 行，`Definition 1.4` 才在第 94 行引入 `arccos`。
  建議修法：改插在 `Definition 1.4`／`Proposition 1.3` 之後，或放在 E1.2-a 附近。

- **[advisory] E1.2-c 插在 Remark 1.3 前，但解答正文引用尚未出現的 Remark 1.4。**
  證據：插入點標為「Remark 1.3 之前」（review:158），解答卻寫
  `Under the alternative convention of Remark 1.4`（review:169）；現有 Remark 1.3、1.4
  分別在 `sec-1-2.html:182`、`:189`。
  建議修法：移到 Remark 1.4 之後，或刪掉對 Remark 1.4 的前置引用。

> 數學驗算未發現錯誤；E1.2-c 依 Definition 1.6 重算 \(f(-1)=\pi\) 正確。**blocking 共 1 條。**

### Claude 的 triage 與處置（→ commit `88846a7`）

| Codex finding | 級別 | 裁定 | 處置 |
|---|---|---|---|
| Mooculus 授權標示 | blocking | 採納（屬實——我把 inversesTrig1-6 的逐檔檔頭過度泛化） | 改標 repo 授權 CC BY-NC-SA 4.0；本批引用各檔（digInInversesOfFunctions.tex、inversesTrig7.tex）皆無逐檔 \license 行。仍在 NC 家族，組合結論不變。 |
| O1.2-d 插入點 | advisory | 採納（真順序錯誤） | 改為 Proposition 1.3 之後、E1.2-b 接續。 |
| E1.2-c 前向引用 | advisory | 採納（真前向引用） | 改為 Remark 1.4 之後，引用成回溯。 |

---

## 第二輪：範圍限定複審（findings 原文）

> 只驗三處修正是否到位、有無新問題。

1. **pass**：E1.1-a 已標為 Mooculus repo 授權 CC BY-NC-SA 4.0
   （review:68）；repo 授權見 `mooculus/license.md:5`，Stitz-Zeager 逐檔授權見
   `10_06_ex_131-154.tex:6`，文末亦分列於 review:370–374。
2. **pass**：O1.2-d 插入於 Proposition 1.3 之後（review:174）；arccos 的
   Definition 1.4 在 `sec-1-2.html:94–97`，早於 Proposition 1.3 的 `:103`。
3. **pass**：E1.2-c 已改插入 Remark 1.4 之後（review:158）；解答引用 Remark 1.4
   在 review:168–169，而原文 Remark 1.4 在 `sec-1-2.html:189–191`，已是回溯引用。

> **blocking 共 0 條。複審通過，blocking=0，可交使用者裁決。**

---

## 結論

選題稽核**通過**。21 筆候選數學無誤、來源授權核實、插入順序修正。
下一步：使用者填 [`ch01_example-supplement-review.html`](ch01_example-supplement-review.html)
頂部裁決表 → Claude 跑 import → import 後另有一輪輕量整合稽核（編號位移／prose 引用／渲染）。
