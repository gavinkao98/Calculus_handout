# 講義 → 影片產線重建 — 進度與待辦

> 本檔是跨對話的進度錨。完整施工計畫在 `.claude/plans/`(gitignored,撈不回),故重點留存於此。

## ✅ 已完成

### 設計 brief 同步
- [`design_handoff/DESIGN_BRIEF.md`](design_handoff/DESIGN_BRIEF.md):從舊「Midnight Canvas（全暗）」同步成現行 **Direction B（雙 ground:暗底教學 / 淺底品牌）**,真實 tokens、8 模板對應、SummitBars/logo 規則。**標出兩個 token-vs-實作分歧待定案**(見待辦)。

### 第一階段:內容方法論
- [`CONTENT_METHODOLOGY.md`](CONTENT_METHODOLOGY.md):萃取 gen-1 `legacy/MANIM_STORYBOARD.md` 教學精神、剝離 gen-1 工程、適配 gen-2。決議:**內容/範圍緊跟講義,但場景順序為教學自由重排**;Gemini 直讀 LaTeX(無 spoken-math 表);動畫由使用者自畫、內容稿只給自然語言建議。含**內容稿格式**(`id/source/learning_goal/kind/narration/visual_need/animation_cue`)。
- [`content_scripts/ch01_inverse_functions.md`](content_scripts/ch01_inverse_functions.md):§1.1 內容稿(16 單元,校準樣本)。**16 段 narration 已認可。**
- 兩條校準細則已補進方法論(§3 規則+圖合拆;§5 視覺用具體函數示範)。

### 第二階段:重建工程 —— 里程碑「§1.1 mock 成片」**達成**
- [`make.py`](make.py):**單一 orchestrator**(`parse→synth→render→compose`),取代 gen-2 三 CLI 手動串。mock backend(靜音)。
- [`storyboards/ch01_inverse_functions.yml`](storyboards/ch01_inverse_functions.yml):§1.1 工程稿(16 場景,gen-2 格式 + `source` + `# HOOK` 動畫接入註記)。
- **mock 成片產出**:`output/ch01_inverse_functions.mp4`(16 場景,≈5'45",靜音、動畫模板頂著版)。`output/` 為 gitignored。
- **底層資產零重寫沿用**:`scene.py` 對齊核心、`theme`/`brand`、`audio`、`blocks`、`narration`、ffmpeg mux/concat。

## ⬜ 待辦

### 待你定案(視覺 / 內容)
- **看 mock 成片** `output/ch01_inverse_functions.mp4`:確認視覺/順序/版面。
- **字體分歧**:tokens 指定 sans(Space Grotesk/Hanken)vs 實作用 Computer Modern serif。
- **grid 分歧**:tokens 有 blueprint grid motif,但 `theme.py` `SHOW_GRID=False` 全停用。

### 重建後續(工程)
- **task #6 介面精煉**(唯一未完成的里程碑 task):templates 加 `reveal_targets()` 驗 `{show}`、正式 hook 機制、`scene.py` 去 class-attribute 副作用。
- **客製動畫接入**:5 個 `animation_cue`(motivation 兩進一出、why-x²-fails 水平線掃描、line-test 並排 sweep、composition 往返、reflection 翻摺)— 你畫好 manim 後,工程稿 `# HOOK` 處接入。
- **真旁白**:Gemini TTS(**計費**;依 CLAUDE.md 先報 beat 數/秒數/估算成本經同意才跑)。
- scaffold(內容稿→工程稿半自動)、schema/lint 獨立指令、增量快取(接 `text_hash`)。
- `output/_av/` 有舊測試殘留(21 vs 16 場景),可清。

### 內容擴展
- §1.2+ 內容稿(用方法論逐節)。
- (可選,暫跳過)§1.6 symbol-heavy 第二校準節 —— 壓力測試方法論的 symbol-heavy 例外。

## 🧊 凍結 / 棄用
- gen-2 舊上層 `pipeline/tts.py`、`build.py`、`mux.py`:被 `make.py` 取代,**暫留未刪**(底層 `scene/theme/brand/audio/blocks/narration` 仍沿用)。
- §1.1 舊 8-scene storyboard:已被 16-scene 工程稿覆寫。

## 💬 待討論
- 使用者尚有待討論的點(下次續)。
