# legacy/ — 已封存的產線（凍結，僅供參考）

本資料夾封存了**三代媒體產線**——gen-0／gen-1（被 `../video/` gen-2 取代；封存
2026-05-31）與 **gen-2 的 Manim 渲染引擎**（`manim_video/`，2026-09-28 影片線統一走
Remotion 後封存）——以及**舊 LaTeX 講義樹**（`tex_handout/`，2026-06-13 凍結）、**HTML 講義
時代的兩件套**（2026-08-09 LaTeX 統一後移入）：

- [`manim_video/`](manim_video/README.md) — gen-2 Manim 講義影片產線（`make.py`＋渲染側
  `pipeline/`＋模板＋storyboard＋hook 動畫；回退 tag `archive/2026-09-28-manim-gen2-final`）。
- [`html_handout/`](html_handout/README.md) — HTML 撰稿線快照（fragments／standalone／
  `build.py`／舊契約；**存量 provenance 的 grep 地**）。
- [`html2latex/`](html2latex/README.md) — HTML→LaTeX 轉換產線工具（12 單元首轉完畢後退役）。

一律**不再維護、不保證可執行**。活躍產線：講義＝[`../handout/latex/`](../handout/latex/README.md)、
影片＝[`../video/README.md`](../video/README.md)。

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

### gen-2 — Manim 講義影片產線（2026-09-28 封存）

講義內容稿 → storyboard YAML → `make.py`（parse → synth → render → compose）→ Manim 逐場
渲染＋MiMo 旁白 → ffmpeg 成片。2026-09-28 使用者拍板影片線統一走 Remotion，渲染引擎整包
以 `git mv` 移入 [`manim_video/`](manim_video/README.md)（相對路徑不變）；與渲染器無關的
共用層（TTS／對齊／音訊）與內容層留在 [`../video/`](../video/README.md)。

- 說明、逐項「從 → 到」對照表、留在 `video/` 的部分與原因：[`manim_video/README.md`](manim_video/README.md)
- 契約：[`../video/KICKOFF-remotion-unification.md`](../video/KICKOFF-remotion-unification.md)
- 回退錨點：annotated tag `archive/2026-09-28-manim-gen2-final`（要跑請 checkout 此 tag）

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
