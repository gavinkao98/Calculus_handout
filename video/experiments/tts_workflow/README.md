# Q7 配音工作流試驗

依 [2026-09-26 設計](../../_audit/REVIEW-tts-workflow-2026-09-26.html) 的落地順序，先完成聲音／時間來源小樣的準備。本目錄保存候選設定與報量快照；目前只有**離線計畫工具**，尚未執行三家合成、選出勝出者或改接正式產線。

## 重建報量頁

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

試聽採 −19 LUFS、無 BGM、隱藏供應商標籤。先裁決錯讀／漏字，再記自然度、語句銜接、收尾、人工修改時間及 cue 誤差。本輪沒有新音訊，無品質評分。完整試聽一次是否成為所有正式影片的固定步驟，留待音鎖階段確認。

## 接續工作與停止點

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
