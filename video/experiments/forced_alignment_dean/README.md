# Dean forced-alignment 實驗線

本資料夾是獨立實驗，不改 `video/make.py`、`video/pipeline/tts.py` 的成熟 beat 級主流程。

目標是測試下一代資料流：

1. 保留 storyboard 裡的 `{show ...}` beat，作為教學與 reveal 契約。
2. TTS 改成一個 content scene 一段音訊，先用 MiMo 內建 voice `Dean`，降低 voice drift。
3. 用 forced alignment 取得 word timestamps。
4. 把每個 `{show}` 映回 word timestamp，產出 beat durations。
5. 單場 render/mux，觀察同步品質。

本機 aligner 有兩個、角色不同（2026-07-05 三場景實測拍板，詳見 [`RESULTS-2026-07-05.md`](RESULTS-2026-07-05.md)）：

- **`stable-ts`（計時來源）**：`run_stable_ts_align.py`，transcript-constrained forced alignment——被 plan transcript 約束、結構上不可能漏字，每字附 timestamp＋機率。beat durations 一律用它。
- **`whisper_timestamped`（QA 探針）**：`run_whisper_timestamped.py`，自由 ASR＋DTW。ASR decoder 對重複的數學公式片語會跳字（實測 derivation 場景漏 12 字、後續 beat 邊界整體錯位 4.6–7.0s），**不可當計時來源**；用途是拿 ASR 文字 diff transcript，抓「TTS 沒唸／唸錯」這類 FA 看不到的錯。

`map_alignment_to_beats.py` 仍採「aligner 可插拔」格式：任何工具只要能輸出 word-level JSON，就能接進來——但**用 word index 對 beat 的前提是 words 與 plan tokens 逐字對齊**，自由 ASR 給不了這個保證。

## 輸出位置

所有實驗產物預設放在：

```powershell
video\output\experiments\forced_alignment_dean\
```

這在 `video/output/` 底下，屬 gitignored 成品區，不污染版控。

## 建議第一輪

先挑一個短 scene，例如：

```powershell
python video\experiments\forced_alignment_dean\prepare_scene.py `
  --storyboard video\storyboards\ch03_trig_derivatives_mimo.yml `
  --scene why_trig_is_different
```

這會產出：

- `transcript.txt`：移除 `{show}` 後的一整段旁白文字。
- `scene_plan.json`：每個 beat 對應的 word index、reveal id、文字。

Dean 整場景 TTS（外部 API；執行前仍需依 `CLAUDE.md` 徵得同意）：

```powershell
python video\experiments\forced_alignment_dean\synthesize_dean_scene.py `
  --plan video\output\experiments\forced_alignment_dean\why_trig_is_different\scene_plan.json `
  --backend mimo
```

若只是測管線，不呼叫 API：

```powershell
python video\experiments\forced_alignment_dean\synthesize_dean_scene.py `
  --plan video\output\experiments\forced_alignment_dean\why_trig_is_different\scene_plan.json `
  --backend mock
```

本機 forced alignment（計時來源；第一次跑 `base.en` 會下載 Whisper model cache）：

```powershell
python video\experiments\forced_alignment_dean\run_stable_ts_align.py `
  --plan video\output\experiments\forced_alignment_dean\why_trig_is_different\scene_plan.json `
  --audio video\output\experiments\forced_alignment_dean\why_trig_is_different\scene_dean.wav `
  --model base.en `
  --device cpu
```

這會產出 `words_stable_ts.json`：頂層 `words[]` 已 explode 成 plan 的 WORD_RE tokenization（逐字驗證與 plan tokens 對齊、對不上會報錯退出），`summary` 帶 aligner 版本／參數、低機率 run、beat 邊界落在多 token 字內的警告；`segments[]` 保留 stable-ts 原始輸出。對不上 transcript 超過 `--failure-threshold`（預設 20%）會直接 abort，不會產出錯的時間軸。

ASR QA 探針（選跑；抓「TTS 沒唸／唸錯」，不當計時來源）：

```powershell
python video\experiments\forced_alignment_dean\run_whisper_timestamped.py `
  --plan video\output\experiments\forced_alignment_dean\why_trig_is_different\scene_plan.json `
  --audio video\output\experiments\forced_alignment_dean\why_trig_is_different\scene_dean.wav `
  --model base.en `
  --device cpu `
  --accurate
```

這會產出 `words_whisper_timestamped.json`，形狀是 `segments[].words[]`。

## Word timestamps 格式

`map_alignment_to_beats.py` 接受這種簡單格式：

```json
{
  "words": [
    {"word": "Every", "start": 0.12, "end": 0.34},
    {"word": "derivative", "start": 0.35, "end": 0.81}
  ]
}
```

也支援 WhisperX / stable-ts 常見的 `segments[].words[]` 形狀。

把 forced alignment 結果映回 beat（計時來源用 `words_stable_ts.json`）：

```powershell
python video\experiments\forced_alignment_dean\map_alignment_to_beats.py `
  --plan video\output\experiments\forced_alignment_dean\why_trig_is_different\scene_plan.json `
  --words video\output\experiments\forced_alignment_dean\why_trig_is_different\words_stable_ts.json `
  --audio video\output\experiments\forced_alignment_dean\why_trig_is_different\scene_dean.wav
```

若要在沒有 aligner 的機器上測 plumbing，可用線性假 timestamps（不是 forced alignment，只是確認資料流）：

```powershell
python video\experiments\forced_alignment_dean\map_alignment_to_beats.py `
  --plan video\output\experiments\forced_alignment_dean\why_trig_is_different\scene_plan.json `
  --audio video\output\experiments\forced_alignment_dean\why_trig_is_different\scene_dean.wav `
  --linear-from-audio
```

單場 render/mux：

```powershell
python video\experiments\forced_alignment_dean\render_aligned_scene.py `
  --storyboard video\storyboards\ch03_trig_derivatives_mimo.yml `
  --scene why_trig_is_different `
  --aligned video\output\experiments\forced_alignment_dean\why_trig_is_different\aligned_beats.json `
  --audio video\output\experiments\forced_alignment_dean\why_trig_is_different\scene_dean.wav
```

## 實驗原則

- 不覆蓋 `audio_mimo/manifest.json`。
- 不改正式 storyboard。
- 不把實驗音訊當正式成片。
- 真 MiMo TTS 前先報：model、voice、scene、字數／預估秒數、估值成本。
- forced-alignment 依賴與版本記在 repo 根 [`ENVIRONMENT.md`](../../../ENVIRONMENT.md)，`tools/doctor.py` 只把缺少 aligner 判為 WARN。
