# TODO — 影片模板重設計（“The Lectern”）＋ Codex review 彙總

> **跨機器交接錨**（2026-06-24）。狀態：**方向定調中**——尚未動任何 Manim 程式碼、尚未 commit 任何視覺改動。
> 本檔是換電腦後接著做的入口。相關產物都已落版控、會隨 git 過去。

## 產物（皆已在 repo）

| 檔 | 是什麼 |
|---|---|
| [`REVIEW-template-redesign-v1.html`](REVIEW-template-redesign-v1.html) | 提案一「The Lectern」：左 spine ＋ 底部 meta footer ＋ 深藍墨 navy 底 ＋ Fraunces 顯示字 ＋ 內容左 flush ＋ 右 rail aside ＋ 標題內聯數學修正。雙擊即開、KaTeX 即渲。 |
| [`REVIEW-prose-math-layout.html`](REVIEW-prose-math-layout.html) | 提案二「左右 vs 上下」決定性規則 ＋ 同內容 A/B 對照 ＋ 用真實 storyboard 內容的逐模板裁決。 |
| [`CODEX-review-redesign-v1.md`](CODEX-review-redesign-v1.md) | Codex 對兩份提案的完整 read-only review 原稿。 |

## Codex 總評（已逐項核實）

> 不建議整包核准 v1。可採納核心＝**固定 rail＋prose 保留完整 measure**；navy／spine／footer／Fraunces **拆成獨立決策逐一驗證**。

下列 ①②③④ 我已查證屬實（附證據），是要處理的真衝突。

## A. 要處理的真衝突（blocking）

- [ ] **① gradient 違反 flat house style。** 提案用了 radial/linear gradient 當底色與 panel，但 [`VISUAL-FRAME-RUBRIC.md:45`](VISUAL-FRAME-RUBRIC.md) 明文「dark flat 純深色、**無 gradient／noise／grid**」是 house style。→ 提案改**純色** navy。
- [ ] **② 字體論證過期。** [`handout/TYPESETTING_GUIDE.md:279`](../../../handout/TYPESETTING_GUIDE.md)：handout 已於 2026-06-22 改 **New Computer Modern**，不再 Times → 「維持 Times 連結 handout」理由作廢。Fraunces 不只 vendoring：含數學標題走 [`brand.py:279`](../../pipeline/brand.py) `_compose()` 用 `FONT_BODY`，會變「純標題 Fraunces／數學標題 Times」分裂；Space Mono 也非系統字體。
- [ ] **③ spine/footer 非單純共用件。** [`_common.py:38`](../../pipeline/templates/_common.py) `SPINE_X` 就是內容左緣，直接畫線會壓字 → 需新增 `DECOR_SPINE_X`（勿挪用 `SPINE_X`）。footer 吃 body zone／worked strip／motif 空間，且 scene ordinal 尚未傳入 template context（[`scene.py`](../../pipeline/scene.py)）→ 要動 layout/capacity/data flow。
- [ ] **④ BEFORE 非 current tree。** 現行 `definition_math` 已單欄 statement→math＋上偏＋可見 aside；純 `derivation` 鏈[刻意置中](../../pipeline/templates/derivation.py)（非缺陷）。→ 提案別把已完成的當「新修復」，別提純 derivation 改左 flush。真正的 delta 只有 navy／spine／footer／字體。

## B. 順手挖到的 doc bug（與提案無關、該修）

- [ ] [`DESIGN.md:236`](../../DESIGN.md) 說 `definition_math` 兩欄、[`:295`](../../DESIGN.md) 又說已退兩欄——自相矛盾，刪舊述。
- [ ] [`DESIGN.md:488`](../../DESIGN.md) 說 `body_text` 用 Tex，但 [`brand.py:163`](../../pipeline/brand.py) 實際用 Pango `Text`——更正。

## C. 左右 vs 上下（規則確立，修正一處）

核心原則正確：**寬度給容得下寬度的元素（數學／卡片／短 tag／數字），絕不給整句英文。**

- [ ] **撤掉「>45 字改上下」的 lint 提案**——真實 recap points 已 50–60 字會誤報。長 procedure prose 改**拆 scene／改寫**，不卡固定字數。
- 逐模板（沿用即可，無需改）：`derivation` 左右（理由是 1–3 字 tag）｜`procedure_steps` 短指令左右、長句拆｜`recap_cards` 兩個獨立 gallery 左右｜`definition_math`／`theorem_proof` 上下（已是）｜figure（graph／value_table／sign_chart）置中＝house rule，非 finding。

## D. 修正後的執行計畫（採 Codex「一次只動一個變因」）

- [ ] **Step 0 — 先修敘述（便宜、明確該做）：** 兩份 REVIEW html 拿掉 gradient、更正 current-tree／字體敘述；修上面 B 的兩個 `DESIGN.md` doc bug。
- [ ] **Step 1 — 只做 3 張 1080p Manim A/B：** `definition`、`procedure`＋worked、`graph`。用**真 render** 比（離線 `critic.py --dry-run`／`save_last_frame` 抽幀、零計費），不再用 HTML 猜。
- [ ] **Step 2 — 第一輪只測「flat navy ＋ 克制 spine」：** 新增 `DECOR_SPINE_X`（不挪 `SPINE_X`）、**保持現行字體、無 footer、無 gradient**、隔離變因。
- [ ] **Step 3 — 延後各自單測：** footer（要動 capacity/data flow）、Fraunces（要先決定字體方向）。`HEADING_MATH_SCALE` **不照 CSS `.84em` 改**（KaTeX≠newtx 指標），要動就在 Manim 裡實測校（現行 0.78 已是 Manim 校準值）。

## E. 待你拍板的決策

- [ ] **字體（比 Fraunces 更該先決定）：** video 要不要跟 handout 改 **NCM**（重建 handout↔video 一致）／維持 **Times**／試 **Fraunces**（成本高、要改 `_compose` 才不分裂）？
- [ ] **navy 底**採不採（可試，須保純色 ＋ 同步重調 panel／hairline）。
- [ ] **spine** 採不採（先小範圍 prototype）。
- [ ] **footer** v1 暫不採——認可暫緩？

## F. 別重蹈的既定約束（house rules，不要動）

- dark **flat**、無 gradient／grid（[`VISUAL-FRAME-RUBRIC.md:45`](VISUAL-FRAME-RUBRIC.md)）。
- 字級恆定、**wrap-don't-shrink**、**否決 auto-fit 縮字**、固定 body zone 容量契約（[`DESIGN.md`](../../DESIGN.md) §容量契約）。
- figure 置中是 house rule（非 drift）。
- 四色語意系統、Lectern 對齊網格（`SPINE_X`/`RAIL_X`）不動。

---

**下一步（回來時）：** 建議直接做 Step 0（修兩份 html ＋ DESIGN.md），同時請使用者先回 E 的字體決策，再進 Step 1–2 的 Manim A/B。
