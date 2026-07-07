# House audio cue candidates

本資料夾放課程影片 house audio cue 候選。這組聲音用
[`generate_house_cues.py`](generate_house_cues.py) 由純 Python 標準函式庫合成，
沒有使用第三方 sample、素材庫音檔或外部 API。

使用者裁決稿：[`REVIEW-house-audio-candidates.html`](REVIEW-house-audio-candidates.html)（歷史紀錄）。

## 裁決結果（2026-07-02 定案；2026-07-07 清理落選檔）

**Candidate B（溫暖低調）獲採用**，接進 compose（政策表 `pipeline/house_audio.py`：intro/outro bed＋divider stinger gain 0.6；content 場全乾聲；**caution ping 不用**）。落選的 A（`calculus_*`）、C（`candidate_c_*`）全套與所有 `*_caution_ping.wav` 已於 2026-07-07 刪除（可從 git 歷史取回；裁決稿 HTML 內的 A/C 試聽連結因此失效）。現存檔案：

| 檔案 | 用途 |
|---|---|
| `candidate_b_intro_bed.wav` | intro 開場底樂（6–8 秒，淡入淡出） |
| `candidate_b_outro_bed.wav` | outro 結尾底樂 |
| `candidate_b_divider_stinger.wav` | divider 一次性 stinger（gain 0.6） |

## 預期使用決策

| 用途 | 套用模板 | 規則 |
|---|---|---|
| 開場底樂 | `intro` | 只在開場 6-8 秒使用，淡入淡出，不延伸到第一個 content scene。 |
| 結尾底樂 | `outro` | 只在結尾 slate 使用，音量維持低於旁白風格。 |
| act/stage 切換提示 | `divider` | 一次性 stinger，不作為連續背景音。 |
| caution 短提示 | `callout` with `type: caution` | 只在少數 notation trap / caution 場景使用，避免每個 callout 都響。 |

所有內容教學模板仍依 [`../../../../DESIGN.md`](../../../../DESIGN.md) 的 Audio policy
維持 narration-first：`definition_math`、`theorem_proof`、`procedure_steps`、
`derivation`、`value_table`、`sign_chart` 不放 BGM；`graph` 只在大型視覺轉換
需要時才可搭配極淡 whoosh。

## 授權與來源

- Source：本 repo 內的 `generate_house_cues.py`。
- Third-party assets：無。
- External API：無。
- Samples：無。
- Intended use：本專案 lesson videos 的預設非商用上網發布音訊。

若未來替換為 YouTube Audio Library、Pixabay 或其他第三方素材，必須另建素材清單，
記錄來源 URL、license、作者、下載日期與是否需署名；沒有素材清單，不進最終 mux。
