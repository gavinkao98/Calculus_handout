# Q7 配音工作流試驗

依 [2026-09-26 設計](../../_audit/REVIEW-tts-workflow-2026-09-26.html) 先準備聲音／時間來源小樣；同日使用者另指示「先用我們原本的 MIMO 跑一次全片」。兩個批次分開：**三家 × 三段的 9 次 pilot 仍只有離線計畫**；**MiMo 全片試聽另用 14 場完整 scene 的受控 runner**，不消耗或冒用前者的計畫與授權。尚未選出三家勝出者，也未改接正式產線。

## 下一候選：優先研究 Gemini 官方預設音色（2026-09-26）

使用者希望下一個優先研究／試聽 Gemini，並自述已有付費 API 餘額；本輪未核對帳務或可用額度。**目前配音試驗各家都先用官方預設音色**，暫不做 voice cloning／voice design。這是候選研究，尚未生成 Gemini 音訊，不代表新的合成批次已獲同意；原 MiMo 全片試聽與三家 × 三段離線 pilot 均保留，後者仍未執行。

今日核對[官方模型頁](https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash-tts)，現行研究型號為 `gemini-3.8-flash-tts`，模型層支援繁體及簡體中文。[官方 TTS 文件](https://ai.google.dev/gemini-api/docs/speech-generation#prebuilt-voices)列出 30 個 curated prebuilt voices，但不能把模型語言支援或一般音色描述當成特定 voice 的中文自然度證據。**中文候選尚未選定**：待查官方 prebuilt 的中文語言／地區標記後再凍結，之後以同稿試聽判斷自然度；目前未試聽新版，也不保證台灣口音。

按[官方 Standard 付費價](https://ai.google.dev/gemini-api/docs/pricing#gemini-3.8-flash-tts)（2026-09-26 查核、優惠至 2026-12-31），文字輸入 USD 0.50／百萬 tokens、音訊輸出 USD 9／百萬 tokens；音訊按 25 tokens／秒換算，約 **USD 0.0135／分鐘**。待選音色的估算方案為三個音色各一次、同一份約 45–60 秒試稿；若各次實際產出落在此範圍，共 3 次請求／135–180 秒，**音訊估 USD 0.030375–0.0405，文字另計**。這是時長假設下的估算，非固定報價或已支出；音色、試稿、文字 tokens、可用模型／帳號與完整批次快照確定後才另報量徵同意，不含重試、clone 或 voice design。

本機唯讀查核：repo `.env` 已有非空 `GEMINI_API_KEY`（不記值），全局／`.venv` 的 `google-genai` 分別為 2.7.0／2.8.0；尚未驗證新 3.8 schema 或帳號餘額／權限，未安裝或改接程式。[歷史紀錄](../../_archive/REBUILD_LOG-2026-05-to-07.md)曾採用 `gemini-3.1-flash-tts-preview`＋Charon 的 3 beat／41.4 秒試聽；**使用者於本輪更正：當時影片全英文，不能推論中文適用性**。2026-06-16 退場是使用者裁決統一 MiMo，亦非 Gemini 中文音質不佳的證據。既有中文 FA／Remotion 可沿用，生成請求、WAV 回應與 receipt 仍需適配：官方模型頁保留 GenerateContent 的 `part.speech_metadata` 入口，3.8 非串流預設回完整 WAV，不能只替換舊模型名稱。

同日用現有 key 做 4 次 metadata GET：`models/gemini-3.8-flash-tts` 與 voices endpoint 均 HTTP 200，但處理 camelCase／snake_case 欄位後，中文 tag 精確篩選仍未取得可確認的 prebuilt 中文候選；未篩語言的首頁有 1,000 筆及下一頁，未全遍歷，不能據此判定不支援中文；未驗生成權限／額度、未生成語音，模型文件支援繁中與特定 voice 中文自然度仍是不同證據。

## MiMo 全片試聽：14 場獨立批次

來源為 `../remotion_styles/paper/q7/q7.zh.yml`，14 個有旁白 scene、2,796 字元；每場一次 `mimo-v2.5-tts`／冰糖，無 style prompt。合成前報量約 8–13 分鐘、最多 14 次 HTTP 嘗試，2026-09-26 查核官網限時免費，使用者同意本批後執行。原有 beat 配音與原片保留。這是供人耳試看的 `trial`：`audio_locked=false`、`nfa_status=not_verified`，不代表稿鎖或正式音鎖驗收。

固定產物位置（相對儲存庫根）：

| 產物 | 路徑 |
|---|---|
| 不可覆寫 plan、ledger、原始 take | `video/output/tts_workflow/q7zh_mimo_scene_20260926/` |
| 中文對齊、cue 品質報告、schema 2 manifest | `video/experiments/remotion_styles/paper/public/audio/q7zh_scene_trial/` |
| 1080p 試片 | `video/experiments/remotion_styles/paper/out/q7zh_mimo_scene_trial_20260926.mp4` |

### 凍結計畫與受控合成

以下從儲存庫根目錄執行。`plan` 只做離線準備；既有批次已有 `plan.json` 時拒絕覆寫。新批次須用新目錄，並另行報量與取得同意。

```powershell
.venv/Scripts/python.exe video/pipeline/tts_scene_trial.py plan --storyboard video/experiments/remotion_styles/paper/q7/q7.zh.yml --output-dir video/output/tts_workflow/q7zh_mimo_scene_20260926
```

確認這份完整文字、模型、voice、上限已獲該批授權後，將工具印出的 `plan_snapshot_hash` 傳入執行入口。hash 用於綁定已獲同意的快照，本身不代替使用者同意：

```powershell
.venv/Scripts/python.exe video/pipeline/tts_scene_trial.py run --output-dir video/output/tts_workflow/q7zh_mimo_scene_20260926 --approve-plan <已獲同意的plan_snapshot_hash>
```

runner 只讀本機環境／repo `.env` 的 `MIMO_API_KEY`、`MIMO_BASE_URL`，不記錄金鑰；文字、模型與 voice 完全取自凍結 plan，不受 `MIMO_TTS_MODEL`／`MIMO_TTS_VOICE`／`MIMO_TTS_STYLE` 覆寫。逐完整 scene 合成，`{show}` 只作定位、不切成多次請求；plan 同時保存無旁白場景的順序及時長。

每次 HTTP 前將 `started` 寫進 `ledger.jsonl` 並 flush／fsync；不重試、不跟隨 redirect。收到完整回應立即存原始 `response.json`，然後保存未裁剪 `raw.wav`、`payload.json`、`receipt.json`。take 目錄以 UUID 命名，不覆寫。receipt 記錄供應商 response ID／usage、請求與檔案 hash、取樣數／取樣率／秒數，全部落盤後才記 `completed`、進下一場。

成功後再執行相同批次，只驗證並沿用既有音檔，零新增 API 呼叫；任一缺件或 hash 不符即停止。逾時、解碼或落盤失敗記 `error_unknown`；有 `started` 卻無完成事件也視為 unknown，整批禁止補送，須先人工核對 receipt／帳務。`run.lock` 防止並行執行；程序崩潰留下鎖時，先確認原程序已停止及帳本狀態，再人工處理鎖，不能把刪鎖當作重試授權。

### 中文對齊與影片接線

使用者已同意下載多語 Whisper `small`，本機 `small.pt` 已核對大小及 SHA256；使用已裝 stable-ts 的**全局 Python**，不是 repo `.venv`。環境與跨機重現見 [ENVIRONMENT.md](../../../ENVIRONMENT.md)。此工具只接受明確的本機權重檔，不下載模型、不呼叫 TTS：

```powershell
& 'C:/Users/Kao/AppData/Local/Programs/Python/Python312/python.exe' video/pipeline/tts_trial_align.py --trial-dir video/output/tts_workflow/q7zh_mimo_scene_20260926 --output-dir video/experiments/remotion_styles/paper/public/audio/q7zh_scene_trial --model-path C:/Users/Kao/.cache/whisper/small.pt
```

全批 take／receipt／WAV 驗證成功後，以 `language=zh`、CPU 8 threads 對原始音檔作限稿 FA，逐字映射既有 cue。詞內 cue 插值明標 `estimated`，低機率與零時長詞另記；不能把 FA 成功解讀為 cue 已人工驗到 ±0.1 秒。原始對齊與完整身分快取存 `_alignment/`，全部場景完成才發布 `manifest.json` 與 `cue-quality.json`。匯出的 WAV 與原始 take 位元完全相同；重跑對齊可以沿用已驗快取，永不重合成。

Remotion 使用既有 `Q7ZH` composition（1920×1080、30 fps），將 `manifest` prop 指向 `audio/q7zh_scene_trial/manifest.json`；既有預設配音不改。影片包含片頭、場間停頓及片尾，總長不等於 14 段 WAV 秒數直接相加。音檔／影片為本機生成資產，沒有因程式碼進 Git 就取得跨機備份；需要保留時複製整個原始批次與匯出目錄，不能靠再次 TTS 還原同一 take。

從 `video/experiments/remotion_styles/paper/` 建置；先將 `out/q7zh_mimo_scene_trial.props.json` 存成 `{"manifest":"audio/q7zh_scene_trial/manifest.json","lang":"zh"}`，再執行：

```powershell
npm.cmd run build
node_modules/.bin/remotion.cmd render build Q7ZH out/q7zh_mimo_scene_trial_raw_20260926.mp4 --codec=h264 --crf=20 --concurrency=8 --props=out/q7zh_mimo_scene_trial.props.json
```

原始渲染另經既有 `scripts/loudnorm.py` 作成片 −19 LUFS 處理，輸出上列 final 路徑；此為影片交付的音量處理，不覆寫 raw take 或 manifest WAV，也不改 cue 秒數。直接播放入口＝[MiMo 全片試聽頁](../../_audit/REVIEW-tts-mimo-full-trial-2026-09-26.html)。

2026-09-26 本批已完成 14／14 場合成，累計 **14 次 HTTP attempts、沿用 0、重試 0**；原始音訊共 **558.72 秒**。中文 FA 14／14 場成功，共 65 cue；6 個 cue 為 `estimated`（原生詞邊界零時長）、18 個低機率 cue（`probability < 0.35`，與 estimated 可重疊）。需人工核點的完整資料見匯出目錄 `cue-quality.json`；此數字不是錯讀判決。17,508 frames 渲染完成、零錯誤；ffprobe 確認影片 **583.600 秒、17,508 frames、1920×1080、30 fps**；容器長 583.658 秒，音訊為 AAC／48 kHz／stereo。成片音量實測 **−19.0 LUFS／−3.0 dBTP**，影片串流複製不重編碼。

試片可播放，尚未通過正式 12 秒停格門檻，兩處待看後裁決：`exam` 的 setup（beat 2，全片 20.767–35.067 秒）最長停格 14.2 秒；`foldback` 的 count（beat 5，全片 269.200–282.000 秒）最長停格 12.8 秒。其餘 12 場通過該 gate。QA 記錄＝`video/output/tts_workflow/preflight/q7zh_scene_trial_final_check/report.json`／`verdict.txt`；實際解碼讀出 17,508／17,508 frames，與預期完全相符。主審已看 14 場 contact sheet 與 Halfway／Angles 的 1920 全尺寸畫面，中文字、公式及版面正常；另確認 Halfway 235.5 秒定格的標籤、球路與三條奇偶說明完整。這是抽幀檢查，不冒充全片人耳／cue 驗收，亦未為避開門檻修改動畫。

### 工具回歸

`_selftest_tts_scene_trial.py` 21 項離線測試通過，包括 14 次假請求後重跑零次、hash 篡改、unknown 停止、缺音／換音拒絕補送、解碼失敗保留 response、執行鎖與禁止 redirect；direct／module 入口均覆蓋。對齊工具另有獨立離線自測。主線 `run_selftests.py` 全 81 組通過，`doctor.py --smoke` 全部必要項目通過。本節工具不提供多家 pilot 執行、take 比較、正式音鎖或自動重合成。

## 三家 × 三段 pilot：重建離線報量頁

從儲存庫根目錄執行（使用既有 Python／PyYAML 環境）：

```powershell
.venv/Scripts/python.exe video/pipeline/tts_pilot_plan.py --storyboard video/experiments/remotion_styles/paper/q7/q7.zh.yml --config video/experiments/tts_workflow/q7-pilot.config.json --output-json video/experiments/tts_workflow/q7-pilot.plan.json --output-html video/_audit/REVIEW-tts-pilot-plan-2026-09-26.html
```

打開 [批次報量頁](../../_audit/REVIEW-tts-pilot-plan-2026-09-26.html)。工具只讀稿件與設定、寫 JSON／HTML，不讀金鑰、不呼叫網路、不生成聲音。產生報表成功不代表可以執行合成；`blockers` 與 `approval` 仍要分別核對。

三個完整自然語段為 `mirror`、`halfway`、`recap`。每家每段一次，共 9 次初始請求；試音、重試、追加 take 另提計畫。`{show}` 依現有旁白文法移除，標點保留，既有空白壓成一個空白；不在原本沒有空白的 cue 處額外加空白。這是試驗用文字定位規則，尚非正式中文 timing／manifest adapter 契約。span 採 Unicode code point 的半開區間 `[start,end)`，不得直接當成 JavaScript UTF-16 索引。

## 候選與估價

查核日：2026-09-26。音色是初始候選，尚未以共同試稿比較聽感。

| 供應商／模型 | voice | 公開用量估價 |
|---|---|---|
| MiniMax `speech-2.8-hd` | `Chinese (Mandarin)_Gentleman` | [USD 100／百萬字符](https://platform.minimax.io/docs/guides/pricing-paygo)；保守計入 727 單位，USD 0.0727 |
| ElevenLabs `eleven_v3` | Adam Li，`hZTuv9Zqrq4yHYrEmF1r` | [USD 0.10／千字符](https://elevenlabs.io/pricing/api)；411 字符，USD 0.0411，帳號／音色加價待核 |
| MiMo `mimo-v2.5-tts` | 冰糖 | [官網限時免費](https://mimo.mi.com/docs/zh-CN/price/pay-as-you-go)，仍須外部呼叫同意 |

MiniMax 的漢字每字算 2、其他含空白標點算 1，是本計畫的保守預算假設，**不是已確認的供應商計字規則**；實際核對 `usage_characters` 與帳務。三家合計 USD 0.1138 為用量估算，未含購買方案、儲值、稅費或音色加價，不是帳單保證，也未授權訂閱／儲值。

MiniMax 音色出自[官方系統清單](https://platform.minimax.io/docs/faq/system-voice-id)；Adam Li 的 ID 核對自[官方中文頁](https://elevenlabs.io/text-to-speech/mandarin-chinese)已顯示的音色選項；冰糖沿用 Q7 現有配音。ElevenLabs 的 [Voice Library](https://elevenlabs.io/docs/eleven-creative/voices/voice-library) 有 API 方案限制，執行前需確認此帳號可用且無未列入計畫的加價。任何改 voice／參數／文字都重新產 plan 並同意該快照。

## 時間來源與驗收

既有冰糖音檔與這三段文字逐字相同，WAV 實測 `mirror` 20.320 秒、`halfway` 42.350 秒、`recap` 13.594 秒，合計 76.264 秒。取樣數、取樣率、檔案 hash 與相對路徑記於設定檔 `calibration`。這是 beat 串接基準，包含原本處理與停頓，不能冒充新整段 take；通用估時計算未套用校準係數。以此基準三家約 3.8 分鐘，實際時長仍以新音檔量測。

MiniMax 候選請求使用[詞級字幕時間](https://platform.minimax.io/docs/api-reference/speech-t2a-http)；ElevenLabs 擬使用[時間戳端點](https://elevenlabs.io/docs/api-reference/text-to-speech/convert-with-timestamps)，須實測 `eleven_v3`＋此 voice 的回應；MiMo 不先宣稱有可用字級時間。三家必要 cue 均須對最後交付音檔人工核點，目標誤差 ≤0.10 秒；未實測的時間保持 unresolved，插值只能標 estimated。對齊失敗保留原 take，不觸發重合成。

三家 pilot 的試聽規劃採 −19 LUFS、無 BGM、隱藏供應商標籤。先裁決錯讀／漏字，再記自然度、語句銜接、收尾、人工修改時間及 cue 誤差。三家 pilot 尚無新音訊，無品質評分；上方 MiMo 全片保留原始 WAV，不宣稱已套用三家盲聽處理。完整試聽一次是否成為所有正式影片的固定步驟，留待音鎖階段確認。

## 三家 pilot 的接續工作與停止點

1. 核對本地金鑰、帳號模型／音色權限與實價；金鑰只放本機環境，不寫進計畫或版控。
2. 完成三段口語稿的 NFA／稿鎖證據。工具目前固定標 pending；既有稿件審閱不能由工具自動升格為新批次的鎖稿。
3. 在實價及稿件確定後，取得綁定這份快照的 9 次初始請求同意。需要外部 NFA 時另行報量。
4. 合成前接上受控 pilot runner：每個 HTTP 嘗試先記帳、硬上限 9、無自動重試；成功立即保存原始 take／receipt／hash，逾時結果不明記 unknown 並停止。本離線工具不能執行這一步。
5. 完成盲聽與供應商時間驗證，依實測決定正式 plan／reuse／不可覆寫 take／累計帳本／lock，再補中文詞庫與相容匯出。沿用設計的三階段順序。

**勿把本計畫交給既有 `tts.py`／`mimo_preview.py` 當作已受新契約保護的執行器。** 本輪沒有改動其計費／fallback 行為；正式 live 接線前必須完成上述控制。既有 beat baseline 的 reuse 為 0，不能假裝是同自然語段請求的快取命中。

## 本輪驗收與回歸

2026-09-26：新增 20 項離線測試全過，包含標點／模型／voice／參數身分、cue 與詞庫版次不觸發新請求身分、Unicode span、重複／未知場景、非法標記、混合語言估時計數、缺 voice／價格阻擋、HTML escape、禁止網路／讀取環境變數，以及從不同路徑呼叫的快照一致性。直接執行自測與標準 `python -m pipeline._selftest_tts_pilot_plan` 入口均通過。

主審抽查修正：統一測試入口的 relative import、repo `.deps` 載入、來源路徑正規化，以及報表來源連結／長字串換行；上述項目已回歸。真 Q7 設定產出 9 筆計畫，三段文字 hash 與既有 baseline 證據一致；尚未進行 API／聽感／時間戳實測。HTML 已檢查資料與跳脫；內建瀏覽器禁止 `file:` 預覽，本輪未宣稱完成瀏覽器視覺驗收。

```powershell
.venv/Scripts/python.exe video/pipeline/run_selftests.py -k tts_pilot_plan
```
