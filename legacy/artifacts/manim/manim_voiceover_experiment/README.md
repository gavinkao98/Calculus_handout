# Manim Voiceover 實驗

此資料夾是一個沙盒，用於將 `manim-voiceover` 與目前的
storyboard/TTS/ffmpeg 產線做比較。

它不會修改既有的課程 render 器。

## 安裝

目前環境有 Manim 與 gTTS，但沒有 `manim_voiceover`。

```powershell
python -m pip install --target .deps_voiceover "manim-voiceover[gtts]"
```

demo 預設使用 `gtts_linear`，一個位於 `voiceover_bookmark_demo.py` 的小型
fallback service。它正常使用 Manim Voiceover，但提供線性的詞界估計，使
bookmark 能在沒有 Whisper 的情況下運作。

## Python 3.12 的 Whisper 修正

在 Python 3.12 上請勿使用此指令：

```powershell
python -m pip install "manim-voiceover[transcribe]"
```

Manim Voiceover 0.3.7 為 `transcribe` extra 將 `openai-whisper` 釘在
`20230314`，而那個舊版本無法在此 Python 3.12 環境中順利建置。

請改為直接安裝目前相容的套件：

```powershell
python -m pip install --target .deps_voiceover --upgrade openai-whisper stable-ts
```

Manim Voiceover 只需要可匯入的 `whisper` 與 `stable_whisper` 模組。
以直接安裝，此環境解析為：

- `openai-whisper`：`20250625`
- `stable-ts`：`2.19.1`

## Render

從儲存庫根目錄：

```powershell
$root = (Get-Location).Path
$env:PYTHONPATH = (Join-Path $root ".deps_voiceover") + ";" + $env:PYTHONPATH
$env:HOME = $root
$env:MIKTEX_USERDATA = Join-Path $root ".cache\miktex-data"
$env:MIKTEX_USERCONFIG = Join-Path $root ".cache\miktex-config"
python -m manim -ql artifacts\manim\manim_voiceover_experiment\voiceover_bookmark_demo.py ManimVoiceoverExperiment --disable_caching --media_dir artifacts\manim\manim_voiceover_experiment\media
```

複製出來供快速檢視的輸出：

- `artifacts/manim/manim_voiceover_experiment/manim_voiceover_experiment.mp4`

## Service 切換

預設：

```powershell
$env:MANIM_VOICEOVER_SERVICE = "gtts_linear"
```

帶 Whisper 轉錄的官方 gTTS service：

```powershell
$env:MANIM_VOICEOVER_SERVICE = "gtts_transcribe"
$env:MANIM_VOICEOVER_TRANSCRIPTION_MODEL = "tiny.en"
python -m manim -ql artifacts\manim\manim_voiceover_experiment\voiceover_bookmark_demo.py ManimVoiceoverExperiment --disable_caching --media_dir artifacts\manim\manim_voiceover_experiment\media_whisper
```

複製出來供快速檢視的輸出：

- `artifacts/manim/manim_voiceover_experiment/manim_voiceover_experiment_whisper.mp4`

## 試用 Coqui Jenny

目前專案的音訊使用 Coqui 內建的 Jenny 模型：
`tts_models/en/jenny/jenny`。

在以 Coqui 支援安裝 Manim Voiceover 後，以此 render：

```powershell
python -m pip install "manim-voiceover[coqui]"
$env:MANIM_VOICEOVER_SERVICE = "coqui_jenny"
manim -pql artifacts\manim\manim_voiceover_experiment\voiceover_bookmark_demo.py ManimVoiceoverExperiment --disable_caching
```

若 bookmark 在使用非線性 service 時失敗，請改用 `gtts_linear` 或安裝
Whisper 支援。僅含時長的區塊仍會展現基本的自動同步行為。

## Precise Limit 旁白測試

`precise_limit_voiceover_demo.py` 是一個獨立測試，從
`ch01_precise_limit` 的二次 epsilon-delta 場景複製而來。它不使用製作用的
render 器。它讀取 `precise_limit_voiceovers/` 下複製來的音訊／manifest，並將
beat 起點作為 Manim Voiceover bookmark 揭露。

```powershell
$root = (Get-Location).Path
$env:PYTHONPATH = (Join-Path $root ".deps_voiceover") + ";" + $root + ";" + $env:PYTHONPATH
$env:HOME = $root
$env:MIKTEX_USERDATA = Join-Path $root ".cache\miktex-data"
$env:MIKTEX_USERCONFIG = Join-Path $root ".cache\miktex-config"
python -m manim -qm artifacts\manim\manim_voiceover_experiment\precise_limit_voiceover_demo.py PreciseLimitVoiceoverQuadratic --disable_caching --media_dir artifacts\manim\manim_voiceover_experiment\media_precise_limit
```

便利輸出：

- `artifacts/manim/manim_voiceover_experiment/precise_limit_voiceover_quadratic.mp4`

## 分鏡模板旁白測試

這是可重用的替換實驗。資料夾內含以下項目的本機複本：

- `voiceover_templates/`，自 `tools/manim_templates/` 複製
- `voiceover_hooks/`，自 `tools/manim_hooks/` 複製
- `ch01_precise_limit_voiceover_storyboard.yml`，自原始分鏡複製
- `precise_limit_voiceovers/`，自既有 render 出的 TTS WAV/manifest 複製

重要的改動在 `voiceover_templates/templates.py`：beat reveal 的時序改由
Manim Voiceover bookmark 驅動，而非手動的 duration 等待。

```powershell
$root = (Get-Location).Path
$env:PYTHONPATH = (Join-Path $root ".deps_voiceover") + ";" + $root + ";" + (Join-Path $root "tools") + ";" + (Join-Path $root "artifacts\manim\manim_voiceover_experiment") + ";" + $env:PYTHONPATH
$env:HOME = $root
$env:MIKTEX_USERDATA = Join-Path $root ".cache\miktex-data"
$env:MIKTEX_USERCONFIG = Join-Path $root ".cache\miktex-config"
python -m manim -qm artifacts\manim\manim_voiceover_experiment\precise_limit_voiceover_storyboard.py PreciseLimitVoiceoverQuadraticTemplate --disable_caching --media_dir artifacts\manim\manim_voiceover_experiment\media_storyboard_template
```

便利輸出：

- `artifacts/manim/manim_voiceover_experiment/precise_limit_voiceover_quadratic_template.mp4`

三場景樣本：

```powershell
python -m manim -qm artifacts\manim\manim_voiceover_experiment\precise_limit_voiceover_storyboard.py PreciseLimitVoiceoverStoryboardSample --disable_caching --media_dir artifacts\manim\manim_voiceover_experiment\media_storyboard_sample
```

便利輸出：

- `artifacts/manim/manim_voiceover_experiment/precise_limit_voiceover_storyboard_sample.mp4`

整節 render：

```powershell
python -m manim -qm artifacts\manim\manim_voiceover_experiment\precise_limit_voiceover_storyboard.py PreciseLimitVoiceoverFull --disable_caching --media_dir artifacts\manim\manim_voiceover_experiment\media_storyboard_full
```

便利輸出：

- `artifacts/manim/manim_voiceover_experiment/precise_limit_voiceover_full.mp4`

## 實驗用 CLI

當你在複製出的實驗分鏡中編輯旁白時使用此工具。`check` 指令會在分鏡旁白
不再與複製來的 `manifest.json`/WAV 檔相符時失敗。

```powershell
python artifacts\manim\manim_voiceover_experiment\voiceover_experiment_cli.py check
```

render 目標會先跑同一個 check，再把 Manim 的輸出複製到一個穩定的 MP4
路徑：

```powershell
python artifacts\manim\manim_voiceover_experiment\voiceover_experiment_cli.py render quadratic --quality medium
python artifacts\manim\manim_voiceover_experiment\voiceover_experiment_cli.py render sample --quality medium
python artifacts\manim\manim_voiceover_experiment\voiceover_experiment_cli.py render full --quality medium
```

若 check 在一次旁白編輯後失敗，請在 render 前重新產生或重新複製受影響的
音訊／manifest。僅在刻意測試純視覺變更時才使用 `--skip-check`。
