# 講義圖稽核 — RUBRIC（figure audit）

> **本審契約（單一真相來源）。** gate 1 = Claude `handout-figure-audit` subagent；視覺層的 Codex 第二讀者退為**定稿前的信心複核**（非每輪必跑，計費需同意）。
> **被審物：** 一張 **render 後的 PNG**（由 [`../_render/shot.mjs`](../_render/shot.mjs) 從 standalone 截圖產出），可參照該節 fragment 的 `figcaption`／`FIGS` 原始碼當語境。
> **依據：** [`../../CONTENT_SPEC.md`](../../CONTENT_SPEC.md) §10（圖規則）＋本檔維度（從 ch01 圖稽核實證蒸餾，見 `../_dev-archive/ch01/ch01_figure-audit.md`）。
> **性質：** 唯讀、advisory＋blocking 分流、不改檔。審「**畫出來**對不對、讀不讀得懂」，不是 copyedit。

## 維度（D1–D8；每條標 Blocking / Advisory）

**可讀性（看得清嗎）**
- **D1 Label collision／overlap**：label 互撞、撞軸、撞曲線或出界。**蓋住資訊 → Blocking**；輕微偏移不蓋字 → advisory。
- **D2 Out-of-bounds／clipping**：關鍵元素（轉折、交點、漸近線、標記點）被裁出可視區。**→ Blocking**。
- **D3 Viewing-window readability**：x/y-range 過大或過小，使曲線貼線／爆框、定性行為（漸近線、截距、彎曲、方向）不可辨。**→ Blocking**（等同畫錯）。
- **D4 Tick labels present／legible**：承載教學值的軸（讀圖題、需讀值處）缺刻度文字（如 `tex` 欄缺失、fallback 不認整數）。**讀者無法讀值 → Blocking**；非承載軸缺刻度 → advisory。

**心智模型（傳達對的觀念嗎）**
- **D5 Figure ↔ caption／prose 一致**：圖與 figcaption／定義／範例陳述矛盾（如雙側極限題只畫單側、ε-strip 標「對稱」卻畫不對稱）。**→ Blocking**。
- **D6 Math correctness vs source**（需 `FIGS` 原始碼）：座標／數值與課文不符 **→ Blocking**；純示意比例（標籤數學正確、形狀近似）**→ advisory**（沿用 ch01 A1 慣例，不修）。
- **D7 No-spoiler**：worked-example 圖洩露要學生算的量。**→ Blocking**。

**編碼穩健（§10）**
- **D8 Color-only／grayscale survival**：資訊只靠顏色區分、灰階印出後無法區辨（缺 redundant encoding：線型／標記／直接 label）。**→ Blocking**；palette 越界（非 blue／red／gray、無宣告）→ advisory。

## Non-findings（別當 finding）
- 刻意的示意近似比例（如直角三角形示意圖，標籤數學正確）。
- §10 允許的 callout、redundant curve label、宣告過的 palette exception。
- 純美學偏好（色深、字級），除非已影響可讀性。

## 輸出格式
1. `VERDICT` 行：視覺 blocking 數。
2. 逐條 finding：`圖 ID｜Figure #｜維度 D?｜Blocking|Advisory｜證據（座標/檔行/PNG 觀察）｜為何｜建議修法`。
3. 各乾淨維度一行（「D? 乾淨」）。
4. 末行結論：本圖／本節「**視覺 blocking 是否歸零**」。

**不 over-report、乾淨圖是有效結果。** 你是提議、不是行動：findings 交回裁決，不改檔（本來也唯讀）。
