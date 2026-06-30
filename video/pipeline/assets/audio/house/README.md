# House audio cue candidates

本資料夾放課程影片 house audio cue 候選。這組聲音用
[`generate_house_cues.py`](generate_house_cues.py) 由純 Python 標準函式庫合成，
沒有使用第三方 sample、素材庫音檔或外部 API。

使用者裁決稿：[`REVIEW-house-audio-candidates.html`](REVIEW-house-audio-candidates.html)。
回家後可直接雙擊 HTML 試聽 A/B/C 三套。

## 候選組

| 組別 | 風格 | 檔案 |
|---|---|---|
| A | 清亮品牌感 | `calculus_intro_bed.wav`、`calculus_outro_bed.wav`、`calculus_divider_stinger.wav`、`calculus_caution_ping.wav` |
| B | 溫暖低調（目前建議） | `candidate_b_intro_bed.wav`、`candidate_b_outro_bed.wav`、`candidate_b_divider_stinger.wav`、`candidate_b_caution_ping.wav` |
| C | 極簡自然 | `candidate_c_intro_bed.wav`、`candidate_c_outro_bed.wav`、`candidate_c_divider_stinger.wav`、`candidate_c_caution_ping.wav` |

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
