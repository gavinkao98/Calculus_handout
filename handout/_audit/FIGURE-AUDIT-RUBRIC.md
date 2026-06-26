# 講義圖稽核 — RUBRIC（figure audit）

> **本審契約（單一真相來源）。** gate 1 = Claude `handout-figure-audit` subagent；視覺層的 Codex 第二讀者退為**定稿前的信心複核**（非每輪必跑，計費需同意）。
> **被審物：** 一張 **render 後的 PNG**（由 [`../_render/shot.mjs`](../_render/shot.mjs) 的 **`figures` 模式**逐 `<figure>` 截 2× PNG：`node shot.mjs <file-url> <out/prefix> figures` → `prefix-<data-fig>.png`；print-standalone 以 CSS @page 分頁、**無 `.sheet` div**，readiness 預設等 `#boot`「Preparing …」遮罩移除＝build 完成才截），對照語境讀該圖的繪圖原始碼：FIGS 圖讀 standalone 的 `const FIGS`、inline-SVG 圖讀 fragment 內 `<svg>`，並參照該節 `figcaption`。
> **枚舉（母體）：** 稽核母體 = 該章 fragment 內**全部 `<figure>` 元素**，含 inline-SVG（有 `id=` 無 `data-fig`、甚至無 figcaption 編號者）；**不可只取 `FIGS`／`data-fig` 定義的圖**。每章開審前以 `Grep '<figure'` 掃 fragment 對齊圖清單，漏的補進去並指派審查者。（shot.mjs 截整頁，inline-SVG 本就入鏡——漏的是「沒人被指派去看」，故枚舉須以 `<figure>` 為準。）
> **依據：** [`../../CONTENT_SPEC.md`](../../CONTENT_SPEC.md) §10（圖規則）＋本檔維度（從 ch01 圖稽核實證蒸餾，見 `../_dev-archive/ch01/ch01_figure-audit.md`）。
> **性質：** 唯讀、advisory＋blocking 分流、不改檔。審「**畫出來**對不對、讀不讀得懂」，不是 copyedit。
> **別跟「圖機會稽核」混為一談：** 本檔審「**已畫的圖對不對**」（correctness，render 後）；上游「**該不該加圖**」（opportunity，出圖前、Mode A／C）是另一道閘——`handout-figure-opportunity-audit` subagent ＋ [`FIGURE-OPPORTUNITY-RUBRIC.md`](FIGURE-OPPORTUNITY-RUBRIC.md)。兩者是同一張圖生命週期的兩端。

## 維度（D1–D8；每條標 Blocking / Advisory）

**可讀性（看得清嗎）**
- **D1 Label collision／overlap**：label 互撞、撞軸、撞曲線或出界。**蓋住資訊 → Blocking**；輕微偏移不蓋字 → advisory。
- **D2 Out-of-bounds／clipping**：關鍵元素（轉折、交點、漸近線、標記點）被裁出可視區。**→ Blocking**。
- **D3 Viewing-window readability**：x/y-range 過大或過小，使曲線貼線／爆框、定性行為（漸近線、截距、彎曲、方向）不可辨。**→ Blocking**（等同畫錯）。
- **D4 Tick labels present／legible**：承載教學值的軸（讀圖題、需讀值處）缺刻度文字（如 `tex` 欄缺失、fallback 不認整數）。**讀者無法讀值 → Blocking**；非承載軸缺刻度 → advisory。

**心智模型（傳達對的觀念嗎）**
- **D5 Figure ↔ caption／prose 一致**：圖與 figcaption／定義／範例陳述矛盾（如雙側極限題只畫單側、ε-strip 標「對稱」卻畫不對稱）。**→ Blocking**。
- **D6 Math correctness vs source**（需該圖繪圖原始碼：`data-fig` 圖讀 `const FIGS`；inline-SVG 圖讀 fragment 內 `<svg>` 的 `cx`/`cy`、`<path d>`、`viewBox`、`<text>` 字串）：座標／數值與課文不符 **→ Blocking**；純示意比例（標籤數學正確、形狀近似）**→ advisory**（沿用 ch01 A1 慣例，不修）。
- **D7 No-spoiler**：worked-example 圖洩露要學生算的量。**→ Blocking**。

**編碼穩健（§10）**
- **D8 Color-only／grayscale survival**：資訊只靠顏色區分、灰階印出後無法區辨（缺 redundant encoding：線型／標記／直接 label）。**→ Blocking**；palette 越界（非 blue／red／gray、無宣告）→ advisory。

## Non-findings（別當 finding）
- 刻意的示意近似比例（如直角三角形示意圖，標籤數學正確）。
- §10 允許的 callout、redundant curve label、宣告過的 palette exception。
- 純美學偏好（色深、字級），除非已影響可讀性。

## 複核紀律（verifier）

每條 raw finding 交回裁決前 **MUST** 經一輪對抗式複核（預設立場駁回、逐條比對上方 Non-findings）。針對 VLM 視覺誤讀，另有以下硬要求：

- **D5／D6 的「某行／某面板標錯」指控，verifier MUST 回繪圖原始碼逐字核對被指控的那一行**（`FIGS` 圖回 `const FIGS`、inline-SVG 圖回 fragment `<svg>`；核對座標、`<path d>` 控制點、`<text>` 字串、`viewBox`、note），不可只憑 render 後 PNG 的觀察就採信。inline-SVG 的小字級上標（如 `fig-map` 的 \(f^{-1}\)）同樣套此硬要求。
- **警覺 VLM 對小字級上標／下標的系統性誤讀**（如把 \(a^{+}\) 看成 \(a^{-}\)）：縮放後的 PNG 在此類細節不可靠，一律以原始碼為準。
- finding 的「建議修法」若會更動圖上某元素，**先確認該元素原本是否真的有誤**——勿據誤讀的指控把缺陷植入一張本來正確的圖。

Rationale：ch01 gate-1 曾對 Fig 1.15 報出一條假 blocking——auditor 誤讀小字級上標、又杜撰與檔案矛盾的行號，其建議修法反而會把缺陷植入正確的圖；對抗式複核（回原始碼逐字核對）擋下了它，gate-2 獨立盲審亦不復現。把這條紀律寫進契約，使「擋假陽性」不依賴操作者臨場記得。

## 輸出格式
1. `VERDICT` 行：視覺 blocking 數。
2. 逐條 finding：`圖 ID｜Figure #｜維度 D?｜Blocking|Advisory｜證據（座標/檔行/PNG 觀察）｜為何｜建議修法`（無 figcaption 編號的 inline-SVG 圖：`Figure #` 填 `N/A`、以其 `id` 當「圖 ID」）。
3. 各乾淨維度一行（「D? 乾淨」）。
4. 末行結論：本圖／本節「**視覺 blocking 是否歸零**」。

**不 over-report、乾淨圖是有效結果。** 你是提議、不是行動：findings 交回裁決，不改檔（本來也唯讀）。
