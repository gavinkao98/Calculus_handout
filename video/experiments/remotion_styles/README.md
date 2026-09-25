# Remotion 風格探索（2026-09-25 起）

**目的：** 用 Remotion 自由摸索新的影片視覺語言，不沿襲舊 Manim 片的外觀。使用者看過滿意後，再把選定的方向定為模板（token → 元件 → 模板的繼承結構）。前置評估與 §3.1 第三幕規劃稿見 [`../remotion_pilot/PLAN-act3-storyboard.html`](../remotion_pilot/PLAN-act3-storyboard.html)。

## 使用者的設計前提（2026-09-25 問卷）

- **唯一固定的元素：** 品牌 logo（`video/pipeline/assets/brand/*.svg`、`video/pipeline/assets/lockup-color-outlined.svg`）。其餘（節標題卡、大綱、分隔頁、內容場、片尾、配色、字型、轉場）全部開放。
- **視覺方向（三選，平行探索）：** 深色極簡發光（`dark_glow/`）、紙本編輯排版（`paper/`）、藍圖工程（`blueprint/`）。
- **動態手法：** 公式流暢變形、鏡頭推拉平移、筆畫描繪出現、彈性物理感（不要「俐落硬切」式的少動畫）。
- **節奏 3／5、密度 3／5**（中等）。
- **欣賞的頻道：** 3Blue1Brown、Khan Academy、Veritasium。
- **旁白：** 可以配合畫面改寫（內容不變、說法可改）；要重新配音時，付費 TTS 仍依 `CLAUDE.md` 先報量徵同意。
- **這一輪不跑任何稽核閘**（NFA、OF、pedagogy、visual audit 等全部跳過）。先專注設計；數學上暫時不嚴謹也可以接受。定為模板、進正式產線前再補回閘序。

## 流程

1. 三個方向各做：4 張風格幀（節標題卡、定理陳述、斜率＝高度的圖、導數循環），加上一段約 15 秒的共同分鏡動態測試，好讓使用者只比較風格、不比較內容。
2. 使用者挑選或混搭。
3. 依選定方向做完 §3.1 第三幕。
4. 使用者滿意後定為模板。

## 進度

- **2026-09-25：** 使用者比較三方向後選定**紙本編輯排版**（`paper/`）。`paper/act3/` 完成 §3.1 第三幕整幕：旁白改寫（`act3.yml`、`SCRIPT.md`），MiMo `mimo-v2.5-tts`／Dean 以 `--unit auto`（實際落到 beat）合成，共 35 次呼叫、0 次重試，約 2 分 44 秒音訊；成片約 2 分 56 秒，本機 render 約 2 分 45 秒。重現方式：在 `paper/` 下執行 `npm ci`，接著 `npx remotion bundle`，再執行 `npx remotion render build Act3 out/act3.mp4 --codec=h264 --crf=20 --props='{"manifest":"audio/act3_mimo/manifest.json"}'`。音訊在 `paper/public/audio/`，不進版控；換機要重跑 TTS，並先徵得使用者同意。
- **2026-09-25（續）：** 配音流程升級，三項都已驗證。
  - **整場合成：** `tts.py --unit scene`。`--unit auto` 只認舊產線的模板名稱，Remotion 稿一律會退回逐 beat，所以要明確指定 `scene`。
  - **逐字對時：** `paper/src/lib/words.ts`，動畫呼叫 `atWord()` 對到旁白的某個字。
  - **響度正規化：** `paper/scripts/loudnorm.py`，沿用 `make.py` 的兩段式 loudnorm，目標 −19 LUFS。
- **無指引生成實驗：** 主對話從講義提煉 [`OUTLINE-s31.md`](OUTLINE-s31.md)（只列要教的內容），子代理在不讀舊稿、舊片的隔離條件下，自己寫出整節 §3.1（`paper/s31/`、`paper/src/s31/`）。
  - **講法：** 「先猜（單位圓速度箭頭）→ 證明時記下欠款（OWED）→ 逐條還清（PAID IN FULL）」。
  - **配音：** MiMo `--unit scene` 共 29 次呼叫；14 場中 12 場整場對齊成功，areas、warnings 退回逐 beat。
  - **成片：** 約 8 分鐘，逐字對時版為 `out/s31_words_final.mp4`。
  - **重現：** `tts.py --storyboard video/experiments/remotion_styles/paper/s31/s31.yml --scene all --backend mimo --unit scene --output-dir video/experiments/remotion_styles/paper/public/audio/s31_scene`，接著 `npx remotion render build S31 … --props='{"manifest":"audio/s31_scene/manifest.json"}'`，最後跑 `python scripts/loudnorm.py`。
- **2026-09-26：解題影片 Q7（`paper/q7/`、`paper/src/q7/`）。** 2026 臺大北區科學人才培育計畫數學組入學考第 7 題（正方形撞球桌），英文旁白、依使用者核准的教學計畫製作：考卷卡 → 四發試射 → 反射＝鏡像 → 一拍一次反射地展開桌子（下一張桌子以牆為軸像書頁翻過來）→ 格點奇偶字典 → 中點測試證 (a) → 摺回真桌＋反彈計數 → tan θ = 2k 家族 → (b) 答案 0 → 回顧、考場寫法、√2 斜率填滿桌面的延伸。
  - **只做了 mock 時序**（14 場、12 個有旁白的場、51 個 beat，mock 全片約 6 分 12 秒）；MiMo 配音待使用者同意。
  - **重現：** 先跑 [`paper/q7/SCRIPT.md`](paper/q7/SCRIPT.md) 裡的 mock 指令，再在 `paper/` 下 `npm run q7`（`out/q7_mock.mp4`）、`npm run q7:stills`（`out/q7_stills/`）。
  - **新元件在 `src/q7/`，不動共用元件：** `geo.ts`（三角波摺疊、精確的反彈折線）、`kit.tsx`（`Table`、`Pocket`、`Rolling`、翻頁式 `Unfold`；計時、TeX 與標籤守門直接沿用 §3.1 的 `s31/kit.tsx`）。
- 尚未做：真實書頁捲曲的翻頁效果；鏡頭推近時裁到頁眉、旁註；定為模板。

各方向資料夾是獨立的 Remotion 專案：`npm ci` 還原依賴，`npx remotion studio` 預覽；`out/` 與 `node_modules/` 不進版控。
