# Dean scene-level TTS + forced alignment 實驗總結

日期：2026-07-05  
用途：給 Claude 討論是否要把目前 beat-level TTS 流程升級成 hybrid / scene-level alignment 流程。

## TL;DR

這次實驗的結論是：**值得採 hybrid，但不建議直接全量取代舊 beat-level TTS。**

Scene-level Dean TTS + 本機 word timestamps 對「長旁白」與「密集 reveal」表現很好；真正危險的是「公式推導口語很長」的場景。推導場景中 Whisper 少抓 12 words，且漏掉的正是長數學片段。這代表新方法能改善聲線連貫與 API call 數量，但 production 化前必須加 guardrail 與 fallback。

推薦策略：

1. 保留 storyboard `{show ...}` / beat 作為正式 reveal 契約。
2. TTS 合成單位可從 beat 改成 scene，先限 prose / graph / 長旁白類場景。
3. forced alignment 失敗或不乾淨時，fallback 到 beat-level TTS，或對數學推導 scene 做更細 chunking。

## 背景

目前成熟流程是 beat-level：

- Storyboard `say` 內用 `{show ...}` 切 beat。
- `video/pipeline/tts.py` 針對每個 beat 合成一段 WAV。
- `video/make.py --reuse-audio` 用每段 beat WAV 的長度控制 Manim reveal 時序。
- 優點：畫面 reveal 與旁白契約直接，debug 容易，單一 beat 出問題只重做該 beat。
- 缺點：TTS call 多，且 voice-design 每 beat 獨立合成容易出現聲線/口音漂移。

本輪討論中，使用者觀察到有時聲音和影片內容對不上，也擔心自訂 voice-design 聲線會飄。於是改測 MiMo 內建 voice `Dean`，並建立一條不碰成熟流程的 forced-alignment 實驗線。

## 本輪已做的工程變更

實驗線：

- 新增 `video/experiments/forced_alignment_dean/`
- 所有實驗輸出放在 `video/output/experiments/forced_alignment_dean/`，屬 gitignored 成品區。
- 新增 wrapper：
  - `prepare_scene.py`
  - `synthesize_dean_scene.py`
  - `run_whisper_timestamped.py`
  - `map_alignment_to_beats.py`
  - `render_aligned_scene.py`

環境：

- 全局安裝 `whisper-timestamped 1.15.9`
- 同步安裝 `openai-whisper 20250625`
- 已下載 Whisper `base.en` model cache
- 更新 `ENVIRONMENT.md`、`video/README.md`
- `tools/doctor.py` 新增 `forced-alignment` 檢查，缺少 aligner 只 WARN，不擋核心產線
- `tools/doctor.py` 另修正 Windows subprocess 輸出 decoding，避免非 UTF-8/CP950 輸出造成背景 thread exception

旁白/TTS 相關前置修正：

- `video/pipeline/tts.py` 已加強 `--reuse-existing`：只有 prior manifest 的 backend/model/voice/style/text_hash 全部匹配才重用 WAV，避免改聲線或改文字卻偷用舊音檔。
- `video/make.py` 已避免 partial scene render 覆蓋 full deck mp4，scene subset 會輸出 `<deck>__<scene>.mp4`。
- 這些修正不是 forced-alignment 本身，但和「聲音/影片對不上」追查有關。

## 實驗資料流

單一 scene 的測試流程：

1. `prepare_scene.py`
   - 讀 storyboard
   - 去掉 `{show ...}` marker
   - 輸出整段 `transcript.txt`
   - 記錄每個 beat 對應的 `word_start` / `word_end`

2. `synthesize_dean_scene.py`
   - 使用 MiMo `mimo-v2.5-tts`
   - voice 使用內建 `Dean`
   - 一個 content scene 合成一段 WAV

3. `run_whisper_timestamped.py`
   - 本機執行 `whisper-timestamped`
   - model 使用 `base.en`
   - 產出 `words_whisper_timestamped.json`

4. `map_alignment_to_beats.py`
   - 讀 word timestamps
   - 依 plan 裡的 beat word indices 對回 beat durations
   - 若 ASR word count 與 plan 差距超過 5%，寫 warning

5. `render_aligned_scene.py`
   - 用 alignment 後的 beat durations render 單 scene
   - mux 單一 scene-level WAV

重要限制：目前使用的是 Whisper ASR + timestamps，嚴格來說不是「被 transcript 強制約束」的 forced alignment。它會受 ASR 誤聽/漏字影響，所以 production 化必須驗證 ASR words 是否和 plan words 對上。

## Pilot 測試

Scene：`why_trig_is_different`

- 類型：一般講解 / definition_math
- plan words：196
- ASR words：196
- avg confidence：約 0.852
- audio：72.087s
- mp4：約 74.0s
- 結論：乾淨通過，證明基本 plumbing 可用。

輸出：

- `video/output/experiments/forced_alignment_dean/why_trig_is_different/scene_dean.wav`
- `video/output/experiments/forced_alignment_dean/why_trig_is_different/words_whisper_timestamped.json`
- `video/output/experiments/forced_alignment_dean/why_trig_is_different/aligned_beats.json`
- `video/output/experiments/forced_alignment_dean/why_trig_is_different/why_trig_is_different_aligned_dean.mp4`

## 三類場景測試

使用者要求測三類：

1. 數學符號多的 derivation scene
2. 旁白很長的 scene
3. `{show}` 很密集、beat 很短的 scene

選用場景：

| 類型 | Scene | Template | Words | Beats |
|---|---|---:|---:|---:|
| 推導／符號多 | `difference_quotient_for_sine` | `derivation` | 197 | 5 |
| 長旁白 | `sector_inequality` | `graph` | 209 | 5 |
| 密集短 beat | `slope_equals_height` | `graph` | 99 | 7 |

三段 transcript 共 505 words，已依使用者明確同意送至 MiMo API 合成 Dean 測試音訊。

結果：

| 類型 | Scene | Plan words | ASR words | Delta | Avg confidence | Audio | MP4 | 判斷 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| 推導／符號多 | `difference_quotient_for_sine` | 197 | 185 | -12 | 0.776 | 81.930s | 83.733s | 有風險 |
| 長旁白 | `sector_inequality` | 209 | 209 | 0 | 0.833 | 81.189s | 82.999s | 通過 |
| 密集短 beat | `slope_equals_height` | 99 | 99 | 0 | 0.803 | 39.867s | 41.333s | 通過 |

測試影片：

- `video/output/experiments/forced_alignment_dean/difference_quotient_for_sine/difference_quotient_for_sine_aligned_dean.mp4`
- `video/output/experiments/forced_alignment_dean/sector_inequality/sector_inequality_aligned_dean.mp4`
- `video/output/experiments/forced_alignment_dean/slope_equals_height/slope_equals_height_aligned_dean.mp4`

## 主要發現

### 1. 長旁白不是問題本身

`sector_inequality` 有 209 words、81.189s audio，ASR word count 完全對上。這代表 scene-level audio 長度到 80 秒左右仍可接受。

### 2. 密集短 beat 也不是問題本身

`slope_equals_height` 有 7 beats / 99 words，ASR word count 也完全對上。Alignment 後的 beat durations 是：

```text
3.46s, 6.08s, 3.90s, 6.64s, 4.32s, 4.02s, 11.447s
```

這表示 `{show}` 密集不必然阻礙 scene-level TTS，只要 ASR word timestamps 對得上，短 reveal 仍可切出可用時間。

### 3. 公式推導的長口語片段是核心風險

`difference_quotient_for_sine` 少 12 words。Diff 顯示主要漏掉這段：

```text
of the quantity x plus one half h times sine of h over two
```

這類數學推導口語句子容易被 ASR 壓縮、漏聽或改寫。一旦漏字發生，後續用 word index 對 beat 的方法就可能整段偏移。

該 scene 的額外訊號：

- avg confidence：0.776，三者最低
- low-confidence words：32 個
- warning：`word count differs: transcript=197, alignment=185, delta=-12`

## 開銷比較

Beat-level 舊流程：

- TTS API call 多：每 beat 一段音訊，例如整節可能接近 100 calls。
- 本機後處理少：不需要 ASR/alignment。
- Debug 低成本：某 beat 壞了就重合成該 beat。
- 聲線風險較高：voice-design 每段獨立合成容易漂。

Scene-level + alignment 新流程：

- TTS API call 少：每 content scene 一段。
- 聲線較連貫：內建 Dean voice + scene-level 合成比 beat-by-beat 自然。
- 本機後處理增加：Whisper alignment 約數十秒一段，還需要 validation。
- Debug 較複雜：ASR 漏字、word count mismatch、math phrase 失真都要處理。
- 失敗 blast radius 較大：一個 scene 合成或 alignment 失敗，影響整個 scene。

整體判斷：新流程不是單純更便宜或更貴。它用較少 API calls 換取更多本機 alignment 與 validation 複雜度。對 voice stability 來說很有價值；對數學推導場景需要保守。

## 建議的 production 策略

採 hybrid：

1. **永遠保留 storyboard beat 契約**
   - `{show ...}` 仍是教學/reveal 的 source of truth。
   - 不建議把整節或整支影片合成成一條超長音訊後再控制全部畫面。

2. **TTS 合成單位可改成 scene**
   - 對 prose / graph / callout / recap 這類場景先啟用。
   - 用 alignment 回推 beat durations。

3. **Derivation / theorem_proof 場景加保守 guardrail**
   - 預設仍用 beat-level TTS，或 scene 內再切 chunk。
   - 若要用 scene-level，必須通過 validation。

4. **Validation gate**
   - `word_count_delta_ratio > 0.05`：fail / require fallback。
   - 平均 confidence 低於門檻：warning 或 retry。
   - low-confidence words 過多：warning。
   - 單 beat duration 過短或異常長：warning。
   - ASR text diff 若集中在 math phrase：fail。

5. **Fallback 順序**
   - 先用更大 Whisper model 重跑 alignment，例如 `small.en` 或 `medium.en`。
   - 若仍 mismatch，回退該 scene 到 beat-level TTS。
   - 若是公式口語太長，人工拆短 narration 或把 derivation scene 切成多個 audio chunks。

## 可能請 Claude 判斷的問題

1. 是否同意 hybrid 路線，而不是全量 scene-level？
2. 哪些 template 預設可以 scene-level？
   - 候選：`definition_math`、`graph`、`callout`、`recap_cards`
   - 保守：`derivation`、`theorem_proof`
3. 對 derivation 場景，應該：
   - 保留 beat-level TTS？
   - 還是改成「每 2 到 3 beats 一個 chunk」？
4. `whisper-timestamped` 是否足夠，還是應改用真正 transcript-constrained forced aligner？
5. Validation 門檻是否合理：
   - word count delta ratio：5%
   - avg confidence：是否要設 0.80 或更高？
   - low-confidence words：是否要用比例而非數量？
6. Production manifest 要如何設計？
   - 是否為每 scene 存 `scene_audio.wav`、`words.json`、`aligned_beats.json`
   - 是否保留每 beat fallback audio
   - `make.py --reuse-audio` 要如何驗證這些 artifacts freshness

## 目前不建議的方向

不建議「全節或全影片一次合成一條音訊」：

- 一句錯了就要重合成大段音訊。
- alignment 失敗難定位。
- intro/outro/house audio/cross-scene transition 會混在一起。
- `{show}` marker 是教學結構，不該完全交給 ASR 反推。

不建議「無 validation 直接相信 Whisper timestamps」：

- 本輪 derivation 場景已證明 ASR 可漏掉數學片段。
- 一旦 word index 偏移，beat timing 會系統性錯位。

## 可複製命令

Prepare：

```powershell
python video\experiments\forced_alignment_dean\prepare_scene.py `
  --storyboard video\storyboards\ch03_trig_derivatives_mimo.yml `
  --scene difference_quotient_for_sine
```

Dean TTS：

```powershell
python video\experiments\forced_alignment_dean\synthesize_dean_scene.py `
  --plan video\output\experiments\forced_alignment_dean\difference_quotient_for_sine\scene_plan.json `
  --backend mimo `
  --model mimo-v2.5-tts `
  --voice Dean
```

Local alignment：

```powershell
python video\experiments\forced_alignment_dean\run_whisper_timestamped.py `
  --plan video\output\experiments\forced_alignment_dean\difference_quotient_for_sine\scene_plan.json `
  --audio video\output\experiments\forced_alignment_dean\difference_quotient_for_sine\scene_dean.wav `
  --model base.en `
  --device cpu `
  --accurate
```

Map to beats：

```powershell
python video\experiments\forced_alignment_dean\map_alignment_to_beats.py `
  --plan video\output\experiments\forced_alignment_dean\difference_quotient_for_sine\scene_plan.json `
  --words video\output\experiments\forced_alignment_dean\difference_quotient_for_sine\words_whisper_timestamped.json `
  --audio video\output\experiments\forced_alignment_dean\difference_quotient_for_sine\scene_dean.wav
```

Render：

```powershell
python video\experiments\forced_alignment_dean\render_aligned_scene.py `
  --storyboard video\storyboards\ch03_trig_derivatives_mimo.yml `
  --scene difference_quotient_for_sine `
  --aligned video\output\experiments\forced_alignment_dean\difference_quotient_for_sine\aligned_beats.json `
  --audio video\output\experiments\forced_alignment_dean\difference_quotient_for_sine\scene_dean.wav `
  --quality low
```

## 狀態備註

- `video/output/experiments/forced_alignment_dean/` 是 gitignored，輸出影片與音訊不進版控。
- 實驗 source 與 summary 在 `video/experiments/forced_alignment_dean/`，可進版控。
- 本輪所有外部 MiMo TTS 呼叫都經使用者明確同意。
- `doctor.py --json` 目前 `forced-alignment` PASS；整體 doctor 仍有既有 MiKTeX font FAIL 與 Vale 權限 WARN，和 alignment 實驗本身無關。
