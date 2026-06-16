# 生成動畫 code 工程稽核 — 維度與收斂線（HOOK-ENGINEERING-RUBRIC）

> 本檔是「生成 manim 動畫 hook code 工程稽核」的契約與**單一真相來源**。走兩讀者：
> - **gate 1 ＝ Claude subagent**（免費、做了客製動畫的節每輪跑）——讀 [`../../pipeline/review_pack.py`](../../pipeline/review_pack.py) 組好的 **engineering packet**（hook code＋animation_cue 意圖＋它該畫的數學），對照本檔判斷。
> - **gate 2 ＝ Codex**（計費、收斂後單次、需同意）——比照 NFA／copyedit 的 gate2，補 gate 1 的模型盲點。
>
> **被審物：** 生成的 `animations/<deck>_hooks.py`（Claude 依內容稿 `animation_cue` 生成的客製動畫 code）。**依據：** [`../../DESIGN.md`](../../DESIGN.md) authoring checklist ＋ [`../../CONTENT_METHODOLOGY.md`](../../CONTENT_METHODOLOGY.md) §5（動畫分工）。**性質：** 唯讀、propose-not-act、不改 code。
>
> **與 VISUAL-FRAME 的分工（V8 邊界）：** VISUAL-FRAME **V8** 查**幀上看得到的**數學；本鏡查**生成那個畫面的 code**——看不到的座標、取樣邏輯、反射建構、端點建構。兩邊各管一半，別重複報。

## 只審兩軸（DESIGN authoring checklist ＋ METHODOLOGY §5）

不評美學、不評「好不好看」（那是 render＋VISUAL-FRAME 的事，不是讀 code 的事）；不為品味提 refactor。只看：

- **E1 數學保真（blocking 軸）。** code 畫的東西與 **math context**（內容稿動畫單元的 `narration`＋`source`，數學為 inline LaTeX）和 `animation_cue` 意圖**完全一致**：函數式、座標、點、極限、漸近線、反射（鏡射軸／對應點）、端點開合、區間、方向。**畫錯／算錯／與源不符 → Blocking**（教錯）。
- **E2 慣例（多為 advisory；造成語義錯時升 Blocking）。**
  - theme primitive：用 `T.color(...)` 等具名 token，**不寫死 hex**。
  - 端點語義：**實心點＝值達到（閉）、空心點＝值不達（開）**；畫反 → **Blocking**（與 E1 同級，教錯）。
  - `muted` 只用於裝飾／已退場 scaffold，不承載教學值。
  - 尊重 `SAFE_MARGIN`、用既有 layout helper，不硬塞絕對座標出框。
  - 純風格／命名／可讀性偏好 → 至多 advisory，通常**非 finding**。

## 不算 finding（別誤報）

- **美學／構圖／顏色好不好看** —— 歸 VISUAL-FRAME（A 維），不在本鏡。
- **幀上可見的數學對錯** —— 歸 VISUAL-FRAME V8，不在本鏡（本鏡只看 code 邏輯）。
- **語義等價的寫法差異**（不同但正確的 manim 寫法、等價的建構順序）。
- **品味型 refactor**（「我會這樣寫」）。
- 刻意示意比例（標籤數學正確、形狀近似）—— 至多 advisory。

## 護欄

- 稽核員**唯讀**：只回報、不改 code（propose-not-act，findings 交回使用者裁決）。
- 遵守四級 finding 分級（①真衝突／違規 ②discoverability ③editorial-drift ④非 finding），**只報 1–2、不 over-report**；**乾淨的 code 是有效結果**。

## 收斂與回報

- **收斂判準：** 該節工程通過 ＝ **engineering Blocking（E1＋E2 致語義錯）== 0**；其餘 advisory 由使用者逐筆裁。
- **回報格式（機器可整理 JSON＋人讀報告）：**
  - 首行 `VERDICT: <n> engineering blocking`。
  - 每條：`- [Blocking|Advisory] [E1|E2] unit/位置 — 證據（code 片段／座標 vs 源）→ 為何 → 建議修法`。
  - 末行對「本節**工程 blocking 是否歸零**」給明確結論。

> **lineage：** 本鏡前身為 `review_pack.py` 四鏡之一的 `engineering` lens（原走 DeepSeek）。2026-06-16 DeepSeek 退場、收斂為本鏡並改兩讀者（gate1 Claude／gate2 Codex），與其餘判斷閘一致；忠實／語域／拆解三鏡已歸 [`CONTENT-SIXLENS-RUBRIC.md`](CONTENT-SIXLENS-RUBRIC.md)。
