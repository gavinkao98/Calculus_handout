# legacy/ — 已封存的媒體產線（凍結，僅供參考）

本資料夾封存了「講義 → 影片」的**前兩代產線**及其間的一次橋接實驗。它們都已被
`../video/`（第二代，gen-2）取代並凍結；保留於此僅作為歷史與實作參考，**不再
維護、不保證可執行**。

目前活躍的影片產線請見 [`../video/README.md`](../video/README.md)。

封存日期：2026-05-31。

## 各世代

### gen-0 — 靜態投影片產線（最舊）

Beamer 投影片 → PDF → TTS 合成 → ffmpeg 合成 MP4。

- 方法論：[`LEGACY_SLIDE_PIPELINE.md`](LEGACY_SLIDE_PIPELINE.md)
- 腳本：`scripts/slides_*.py`、`scripts/voice_*.py`、`scripts/shared_*.py`
- 資料：`artifacts/slides/`、`artifacts/scripts/`、`inputs/media_plans/`、`schemas/slide_deck.schema.json`、`inputs/voice/`

### gen-1 — Manim 分鏡產線

`chapters/*.tex` → 手寫 `inputs/manim_storyboards/<deck>.yml` → preview／audio／render → `artifacts/manim/<deck>/` 與 `artifacts/video/<deck>_manim.mp4`。

- 方法論：[`MANIM_STORYBOARD.md`](MANIM_STORYBOARD.md)、[`MANIM_REFERENCE.md`](MANIM_REFERENCE.md)、[`MANIM_CHECKLIST.md`](MANIM_CHECKLIST.md)
- 腳本：`scripts/manim_*.py`、`scripts/manim_templates/`、`scripts/manim_hooks/`
- 資料：`inputs/manim_storyboards/`、`artifacts/manim/<deck>/`、`schemas/manim_storyboard.schema.json`
- 註：gen-1 的 `manim_storyboard_workflow.py` 會 import gen-0 的 `slides_script_workflow.py`，兩代相依，故一併封存於同一個 `scripts/`。

### 橋接實驗 — manim-voiceover spike

評估以 `manim-voiceover` 的 bookmark 驅動 reveal，取代 gen-1 的手動 timing 等待。
此實驗的結論（兩套 reveal 機制並存、spoken-math 改寫層過重）催生了 gen-2 的整套
重新設計。

- `artifacts/manim/manim_voiceover_experiment/`（含 `MANIM_VOICEOVER_MIGRATION_PLAN.md` 與各 spike）
- `scripts/manim_templates/{voiceover_service,voiceover_scene,reveal_strategy,narration_compiler,narration_markers,latex_speech,anchors}.py`

## 結構

```
legacy/
  README.md                                              你在這裡
  MANIM_STORYBOARD.md  MANIM_REFERENCE.md  MANIM_CHECKLIST.md   gen-1 方法論
  LEGACY_SLIDE_PIPELINE.md                                      gen-0 方法論
  scripts/        所有凍結的 .py（攤平同層，維持 bare-name import）+ manim_templates/、manim_hooks/
  schemas/        gen-0／gen-1 的 JSON schema
  inputs/         分鏡 yml、媒體計畫 json、語音參考與錄音樣本
  artifacts/      git 追蹤的 narration／final／tex + gitignored 的算繪輸出
```

## 為何不再保證可執行（重要）

這些腳本以 bare-name 互相 import（例如 `from manim_storyboard_workflow import ...`），
仰賴「執行時腳本所在目錄被加入 `sys.path`」。它們現在同層放在 `scripts/`，所以
**彼此的 import 仍可解析**；但 `scripts/shared_runtime_bootstrap.py` 的
`REPO_ROOT = Path(__file__).resolve().parents[1]` 在搬移後會指向 `legacy/` 而非
儲存庫根目錄，因此任何透過 `REPO_ROOT` 解析 `.deps*`／`.cache`／`chapters` 的路徑
都會失效。若日後真要重跑某支 gen-1 腳本，需手動修正 `REPO_ROOT`（或從歷史 commit
取出舊版於原位執行）。預設假設是：**這裡只讀不跑**。

## git 與磁碟

- 大型算繪輸出（`artifacts/audio`、`artifacts/video`、`artifacts/manim` 下的 render、
  以及 `inputs/voice/*.wav` 語音樣本，合計約 712 MB）實體存於本資料夾，但維持
  **gitignored**（規則見根目錄 [`../.gitignore`](../.gitignore)）。git 只追蹤文字
  原始碼與資料：腳本、schema、分鏡 yml、`narration.md`、`*_final.md`、slides `*.tex`。
- 本次封存以 `git mv`／rename 偵測完成，個別檔案歷史以 `git log --follow` 仍可追溯。
