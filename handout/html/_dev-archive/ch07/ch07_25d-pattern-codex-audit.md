# Ch7 M2 — 2.5D solid-of-revolution schematic pattern：Codex 收斂紀錄（raw JSON gitignored）

2026-07-18。本書首批旋轉固體 schematic 的 pattern 設計對抗收斂（gpt-5.6-terra／xhigh、read-only）。
提案（Claude P1–P7）→ Codex 4 blocking 修正＋1 advisory＋Q(a)–Q(f) 裁答 → **全數採納後 PASS、逕入繪製批次**。

## 收斂後的 pattern（繪製契約——後續章節旋轉固體圖沿用）

- **投影＝axis-relative parallel-oblique glyph**（不是實體 camera）：圓截面畫成橢圓，**minor:major 固定 0.35**，major 半軸 ⊥ 旋轉軸＝真實半徑。**x 軸旋轉場景橫放**（profile 在軸上方）；**y 軸旋轉場景直立**（profile 在右側）——統一的是投影規則與筆畫階層，不是頁面上的軸方向（QAC-01；Q(c)：直立殼比橫躺更忠實於 strip 方向與半徑讀法）。
- **筆畫階層**：profile 2.2px（primary）／掃出 silhouette 1.5px／rim 1.25px／被遮蔽 rim 弧＝灰虛線／旋轉軸＝灰 dash-dot／輔助＝灰點線；**紅色永不作深度暗示**；highlight＝primary ~0.14 opacity 填色＋實線輪廓＋尺寸線，絕不只靠填色（QF-02）。
- **前後慣例**：直立場景前（下）弧實線、後（上）弧虛線；橫放場景同一 glyph 轉 90°。**exposed cut face（如 disk 切面）＝完整實線輪廓＋填色，不虛線**（QF-01）。
- **無座標鷹架為預設**（無 grid、無完整第二座標軸、無非承載刻度；Q(b)：D4 不要求無讀值任務的數字刻度），但**准許數學必要的 datum**：沿軸 station 只刻在旋轉軸上（僅限沿軸堆疊的 disk/washer）；**殼的 x＝從軸到殼中面的徑向箭頭**（刻在 y 軸上會畫錯數學——QB-01）；Δx 標在兩徑向壁之間；#5 用圖下方的 dimension line（不得冒充旋轉軸）。
- **物件各自的 geometry contract**（QF-01）：disk＝軸心在軸上的完整填色橢圓、固體延伸到軸下；shell＝雙壁（徑向 Δx）＋嵌套小殼灰點線直接可辨；同體對照圖兩面板共用同一份底座幾何、只換 overlay；frustum band＝只填側面、rim 開口不封蓋、近側母線＝傾斜弦（r₁≠r₂）。
- **#5 generic solid＝非旋轉體 cutaway**（QD-01）：不對稱 oblique loaf、kidney／rounded-scalene 不規則截面（**絕不用橢圓**）、無鏡射輪廓、無旋轉軸/箭頭；端平面＝灰斜平行四邊形；slab 前面不規則面＝淡填＋少量 hatch＋外置 Δx bracket；caption 註明厚度誇大。
- **個別定案**：#22（unrolled band）＝純 2D 環扇形；#23（sphere zone）＝**2D profile**（圓＋橫軸＋兩組等寬縱切、上弧強調＋半徑導線；Q(e)：比透視球更直接呈現「小半徑長斜」對「大半徑短斜」）；#8（pyramid）＝**2D 過軸剖面 fallback 優先**（若 2.5D 須 polyhedral 語法非橢圓）。
- **D5/D6 附鎖**：橢圓 major 半徑必須精確接到 profile；#6/#9 用 generic x 語域；#11 washer R=1、r=√y、shell 高 x²、不印 π/2；#20 caption 對映 r₁=f(x_{i−1})、r₂=f(x_i)、ℓ=|P_{i−1}P_i|；誇大的 Δx／band 厚度說在 caption 不塞圖內。
- **實作**：chapter-local FIGS IIFE 內手寫 raw SVG＋共用 helper，沿用 .fig-svg／既有 CSS vars，不動 global kit（P6 通過）。驗收＝實際 220–300px panel 寬 2× PNG＋灰階檢查（→ D1–D8 gate-1）。

## 原提案被駁回的要點（記錄免重蹈）

- P1/P5 的「相機」敘事自相矛盾（軸一律水平 vs 直立場景）→ 改 axis-relative glyph 敘事。
- P3 的「station 一律刻在旋轉軸」對 y 軸殼是**數學錯誤**（x 是徑向距離不是軸上位置）。
- P2 的單一 anatomy 會混淆 disk／shell／band 三種物件；「rim 固定半實半虛」會把 exposed cut face 誤畫成隱藏邊。
- #5 若用鏡射 profile＋橢圓 rim 會直接違反「非旋轉體」的 marker 要求。

**落地**：wave-2 七張（7.5/7.6/7.8/7.10/7.12/7.21/7.22）依本契約繪製；連同 wave-1 十六張共 23 張進 D1–D8 gate-1（`ch07_figure-audit.md`／`REVIEW-ch07-figure-audit.html` 收殘局）。
