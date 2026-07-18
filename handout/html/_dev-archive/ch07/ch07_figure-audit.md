# Ch7 M2 — 圖正確性 D1–D8 gate-1 稽核紀錄（raw 不進版控；本檔為版控轉錄）

2026-07-18。23 張圖（Figure 7.1–7.23）繪製→`shot.mjs figures` 2× PNG→7 個 `handout-figure-audit`
subagent 平行審（依 FIGURE-AUDIT-RUBRIC；各 agent 均回 `const FIGS` 源碼逐座標覆算＝D6 verifier 紀律）。

## 繪製前置（記錄）

- **kit 擴充 ×1**：`buildPlot` 加 `areaBetween` primitive（兩曲線間填色；7.2/7.3/7.4/7.15/7.16 等多圖需要；
  比照 ch06 加 rect/area 的一次性擴充，註解已標明）。CSS 零新增（fill-neg/rect-sum/idline/bubble 既有）。
- **2.5D pattern**：依 `ch07_25d-pattern-codex-audit.md` 收斂契約繪製（axis-relative oblique、0.35 橢圓比、
  前實後虛、殼半徑徑向箭頭、#5 非旋轉體 cutaway、#8 2D fallback、#22 zone 2D profile）。
- **作者自查（落地前 checklist）**先抓 9 處並修：7.1 標籤擠壓、7.2 標籤歸屬、7.4 標籤互貼錯邊＋刻度撞頂點、
  7.5 Δx bracket 漂移、7.6 箭頭/標籤分家、7.9 刻度撞曲線＋直條太矮、7.10 Δx/x 標籤碰撞、7.13 標籤壓線、
  7.15 標籤碰撞、**7.17/7.18/7.21 曲線太平致教學點不可見（換拱形曲線重寫幾何）**、7.23 標籤壓線。

## Gate-1 裁決（首輪）

| 節 | 圖 | blocking | advisory | 摘要 |
|---|---|---|---|---|
| §7.1 | 7.1–7.4 | 0 | 0 | 四圖全乾淨（軸穿區、gap 標籤、交點、strip 端點 0.25/1.75 皆源碼驗證） |
| §7.2 | 7.5–7.8 | **3** | 0 | 7.6 D1（f(x) 標籤被 profile＋rim 夾殺、箭頭戳出輪廓）；7.8 D1（x 尺寸標籤貼 h 線＝歸屬錯亂）＋**D5（inset「正方形」因兩軸比例不等 render 成 1.27:1，與 caption 直接矛盾）**；7.5/7.7 乾淨 |
| §7.3 | 7.9–7.12 | 0 | 0 | 四圖全乾淨（含兩張 2.5D：雙壁/前實後虛/嵌套點線/√y 內圈騎拋物碗面全過） |
| §7.4 | 7.13–7.15 | 0 | 3 | 7.13 D1（F=kx 標籤被線尾穿過）；7.15 D1（y/2 撞錐壁）＋D6（半徑括線畫在 slab 下方、伸出錐壁 5.5px） |
| §7.5 | 7.16 | 0 | 0 | 乾淨（含 deficit/surplus 各 4/3 等積的忠實性覆算） |
| §7.6 | 7.17–7.19 | 0 | 1 | 7.18 D1（Δy_i 標籤與曲線尾端 0–2px 輕觸） |
| §7.7 | 7.20–7.23 | 0 | 2 | 7.20 D1（2πr̄ 錨點偏近外弧）；7.21 D1（左面板導線全高穿過刻度標籤） |
| **合計** | 23 | **3** | **6** | |

## 修復（blocking 3＋advisory 6 全數採納）

- **7.6**：半徑箭頭改畫在 disk 站位內（軸→disk 頂緣）；f(x) 標籤移到 disk 左側淨空帶（anchor end）。
- **7.8**：x 尺寸標籤 dy +14→−10（在自己線上方、與 h 一上一下配對）；inset 寬度依軸比補償
  （x2=0.209；0.9·34.14/43.36≈0.709 units → rendered 30.7×30.7px 真正方形）。
- **7.13**：標籤錨線終點上方（anchor end、dx −4、dy −14）。
- **7.15**：半徑括線移到 slab 中線 y=1.6（右端恰落錐壁）；y/2 移到 slab 上方開闊水域 (0.42,1.97)。
- **7.18**：曲線 domain 3.3→3.2。
- **7.20**：2πr̄ 的 y 偏移 +17→+11（明確掛在虛中線下）。
- **7.21**：左面板 vline 全高改 seg (x,0)→(x,f(x))。

修復後 rebuild＋重 render（figs4）：build ✔／linebreak 0／render math=986、katex-errors 0／23 圖全出。
六張修正圖逐一目視覆核到位。

## 回歸（§7.2 blocking 修復）— PASS：0 blocking／0 advisory

範圍限定 `handout-figure-audit` 複審 Figure 7.6／7.8（修復後 figs4 PNG，源碼逐行覆算）：
① 7.6 箭頭已收在 disk 內、頂在頂緣（尖端 cy−rs+1.5）；f(x) 標籤在左 rim 與 disk 之間的淨空帶、四向 ≥4px ✓。
② 7.8 x 標籤在自己尺寸線上方、與 h 一上一下配對、兩線間距 16px ✓。
③ inset 依軸比補償後 rendered ≈30.74×30.73px＝真正方形，caption 的 "square" 主張成立 ✓。
未引入新缺陷；兩圖其餘維度全乾淨。

## M2 gate-1 總結：23/23 圖視覺 blocking 歸零（2026-07-18）

首輪 3 blocking＋6 advisory → 全數修復＋回歸 clean。終值：build ✔／linebreak 0／render math=986、
katex-errors 0。報告（render 圖內嵌）：`_audit/REVIEW-ch07-figure-audit.html`。
**圖視覺 gate-2（Codex `-i` 第二讀者）依「三閘 gate-2 統一 M4 後批次」規則留待後續**——非 M2 範圍。

## 附註（稽核另提、未動）

- 7.14 源碼一條零長度 no-op `<line>`（render 無 artifact，僅記錄）。
- 7.21 右面板半徑比 62/46 較 f 值比誇大＝示意慣例（利於 r₁≠r₂ 可辨），non-finding。
