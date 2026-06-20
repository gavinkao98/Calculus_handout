# 影片視覺幀稽核 — 維度與收斂線（VISUAL-FRAME-RUBRIC）

> 本檔是「影片視覺幀稽核」的契約與**單一真相來源**。視覺層走**講義 figure-audit 的鏡像**（見 [`../../../handout/_audit/FIGURE-AUDIT-RUBRIC.md`](../../../handout/_audit/FIGURE-AUDIT-RUBRIC.md)）：
> - **gate 1 ＝ Claude 抽幀 subagent**（免費、每次 render 跑）——讀 [`../../pipeline/critic.py`](../../pipeline/critic.py) `--dry-run` 抽出的幀（一個 content scene 一張 fullest 幀），對照本檔判斷。
> - **gate 2 ＝ 外部 VLM 信心複核**（MiMo-V2.5 via `critic.py --confirm`，間歇、計費、需同意）——定稿前非每輪必跑，補 gate 1 的模型盲點。
>
> **被審物：** 已 render 的 scene 幀 PNG（additive reveal 的最末/最滿幀）。**依據：** `critic.py` 既有的 5 維 AES rubric（蒸餾自 DESIGN.md Visual QA）＋ figure-audit 維度 ＋ [`../../REVIEW_GATES.md`](../../REVIEW_GATES.md) 層 7「抽幀目視」清單，並補影片特有的 reveal／manim-Tex 失效模式。**性質：** 唯讀、propose-not-act、不改檔。

## 兩層結構

幀稽核分兩層，各司其職：

- **Layer 1 — Blocking gate（V1–V9）：對錯／可讀性**，二元 Blocking/Advisory；**收斂判準＝視覺 blocking==0**。
- **Layer 2 — AES magnitude（A1–A7）：美學 polish**，每維 0–100＋具體缺陷（severity low/med/high）；**驅動「判→採→重 render→複驗」迴圈的優先序**，本身不 gate 收斂（低分＝advisory，不單獨擋稿）。

**兩層重疊怎麼判（escalation rule，比照 figure-audit「蓋住資訊→Blocking／輕微→advisory」）：** 同一個觀察——**會丟資訊／矛盾／亂碼 → 升 Layer 1 的 V-blocking；只是擠／不夠清楚／不夠美 → 扣 Layer 2 的 A 分。**

## Layer 1 — Blocking 維（每條標 Blocking / Advisory）

- **V1 出框／裁切。** 關鍵元素（轉折、交點、漸近線、標記點、軸標、關鍵式）被裁出框或越安全邊界而**丟資訊**。丟資訊 → **Blocking**；不丟的輕微越界 → advisory。
- **V2 標籤／元素相撞蓋字。** label 壓在曲線／點／空心點／導引線／marker／另一 label 上而**蓋住資訊**。蓋住 → **Blocking**；不蓋字的輕微偏移 → advisory。
- **V3 視窗可讀性。** x/y range 過大或過小，使定性行為（漸近線、截距、彎曲、方向、交點）不可辨、曲線貼框／爆框。→ **Blocking**（等同畫錯）。
- **V4 數學渲染完整／可讀。** 螢幕上每個 Tex 完整渲染——**無亂碼、無生 `$`／反斜線漏出、無缺字／溢字**（manim Tex 特有失效）；承載教學值的字大到讀得到。亂碼／缺字／小到讀不到值 → **Blocking**。
- **V5 端點／記號語義。** 實心／空心端點對該值正確（閉/開）、✓／✗ 正確、箭頭／漸近線虛線正確。畫反 → **Blocking**（教錯）。
- **V6 幀 ↔ 旁白 beat 一致。** 螢幕所示與**這個 beat 正在講的**相符（交點數、哪個函數、宣稱的特徵、象限）。矛盾 → **Blocking**。
- **V7 reveal 同步（影片特有）。** 每個元素**跟著它的 narration beat 出現**——不早（劇透學生要算的答案）、不晚（旁白提到還沒出現的東西）。破壞教學 → **Blocking**；輕微時序 → advisory。
- **V8 視覺數學正確 vs 源（限「幀上可見」）。** 畫出來且**看得到的**座標／數值／形狀與底層數學相符。可見量值不符 → **Blocking**；**刻意示意比例（標籤數學正確、形狀近似）→ advisory**（沿用 figure A1/D6 慣例）。
  - **邊界：** V8 只查**幀上看得到的**；hook code 的數學保真（看不到的座標、生成邏輯）歸**工程鏡**（`review_pack.py`，待修），兩邊各管一半。
- **V9 量化讀值的尺度（gap A）。** 當旁白／標題要觀眾從圖上**讀出某個具體座標或數值**（「在 $x=a$」「值為 $L$」「從 $1$ 降到 $-1$」），那個值必須**讀得到**——靠軸刻度（teaching-tick）／標在點線上的數值標籤／軸數字其一。**完全無從讀到**（無刻度、無數值標籤、無標記）→ **Blocking**（丟資訊，等同沒給數據）。值由標記點／標籤**間接**傳達但缺軸尺度 → **Advisory**（改扣 A1）。**純定性圖**（只談形狀／趨勢／對稱／單調，不要求讀任何具體值）維持無刻度 → **不是 finding**。判準依 DESIGN.md graph「座標軸刻度／級距：何時該標」的 qualitative／quantitative 兩分。

## Layer 2 — AES magnitude 維（每維 0–100；驅動重 render 優先序）

沿用 `critic.py` 既有 5 維、並補 2 維（A6/A7）：

- **A1 Element Layout。** overlap、crowding、越安全邊界、平衡；**留白舒服、元素對齊一致的視覺 grid**；graph label 不壓在曲線／點／空心點／導引線／marker 上。
- **A2 Attractiveness。** 清楚、有目的，不是一張扁平的文字投影片。
- **A3 Logic Flow。** 螢幕所示是否服務這個 narration beat 的重點。
- **A4 Visual Consistency。** accent 色、字級、間距一致。
- **A5 Accuracy & Depth。** 視覺是否傳達到該點；任何可見的標註品質問題。
- **A6 Typography & wrapping（新）。** wrap 斷在合理處；**多行對齊一致——句子級教學散文左對齊、不要置中孤行**（短 callout／title card 才置中）；無 orphan／widow；math 與相鄰文字 baseline 對齊；行距舒服。
- **A7 Visual hierarchy／focus（新）。** 眼睛被帶到**這個 beat 正在講的東西**（用 accent／大小／位置凸顯）；已講完的 scaffold 退到背景；不是所有元素一樣搶眼。

## 不算 finding（house style／影片特性；別誤報）

- **dark flat 極簡背景**（純深色、**無 gradient／noise／grid**）是 house style（3Blue1Brown 風），**不是缺陷**——別建議加。
- **progressive reveal：** final/最滿幀「所有元素同時可見」是預期、**不扣分**；mid-reveal 幀的空白不是缺陷；**靜幀無動態是預期**（別期待動作）。
- **刻意示意比例**（標籤數學正確、形狀近似）至多 advisory。
- **無刻度的乾淨軸本身不是缺陷**（house style）——**但僅限定性圖**；若旁白要求讀某具體值卻無從讀到，那屬 **V9**（見上），不在本豁免內。
- 宣告過的 palette／accent 例外（深色主題內）。
- 影片是彩色螢幕——**不查灰階存活**（figure-audit D8 不適用於本線）。

## 護欄

- 稽核員**唯讀**：只回報、不改檔（propose-not-act，findings 交回使用者裁決）。
- 遵守四級 finding 分級、**不 over-report**；**乾淨的幀／維度是有效結果**。

## 收斂與回報

- **收斂判準：** 該節視覺通過 ＝ **視覺 blocking（V1–V9）== 0**。A 分（A1–A7）驅動「先重 render 哪個／夠不夠 polished」但**不 gate 收斂**；advisory 由使用者逐筆裁。
- **回報格式（沿用 `critic.py` 的機器可整理 JSON＋人讀報告）：**
  - 首行 `VERDICT: <X> visual blocking`（V 維）。
  - **V 維 findings：** `- [Blocking|Advisory] [V#] scene/frame — 證據（座標/觀察/位置）→ 為何 → 建議修法`。
  - **A 維：** 每維 0–100 分 ＋ `defects`（`{dimension, severity low|med|high, where, issue, suggestion}`）。
  - 各乾淨維度一行；末行對「本節**視覺 blocking 是否歸零**」給明確結論。

> **wiring 註（2026-06-16 已接線）：** gate 1（Claude subagent）直接讀本檔、即時涵蓋 V1–V9＋A1–A7。外部 gate 2（[`../../pipeline/critic.py`](../../pipeline/critic.py)／MiMo）**已接上本檔**：runtime verbatim-inject 整份 rubric body（取代原 hardcoded 5 維），JSON schema／`_write_md` 改輸出 `visual_blocking_count`＋`v_findings`（V1–V9、Blocking/Advisory、`VERDICT` 行）＋A1–A7 0–100 scores＋`defects`。§1.1 真 `--dry-run` 驗過。落地紀錄見 [`../../REVIEW_MODEL_DECISIONS.md`](../../REVIEW_MODEL_DECISIONS.md) §八。
