# 敘述放大機會稽核 — AMP（video 產線，expansion 層 M2）

> 本檔是「敘述放大（prose amplification）機會稽核」的契約與**單一真相來源（SSOT）**。gate ＝唯讀 Claude subagent `video-amplification-audit`（免費、唯讀）：掃某節 handout 的承重直覺標記、比對影片有沒有 surface、**提議**補漏掉的 → standalone HTML 裁決稿供使用者裁決。**propose-not-act：只提案、絕不改檔、絕不插稿。** 是講義線 `mode-c-gapwalk` 的影片側對應（見 [`../../../README.md`](../../../README.md) §撰稿工作流程、[`../../../CONTENT_DIRECTION.md`](../../../CONTENT_DIRECTION.md) 的「承重直覺／薄度剖析」）。
>
> 規範權威見 [`../../SPEC-pedagogy-firstlearner-expansion.md`](../../SPEC-pedagogy-firstlearner-expansion.md) §5（M2）。**與 M1（SC 步驟覆蓋）不同機制**：SC 是擋稿的確定性閘、管推導步驟；AMP 是唯讀機會稽核、管敘述直覺、**永不 blocking**。

## 錨與範圍

- **錨＝ handout 的 `expansion:*` 標記**（HTML 註解 `<!-- expansion:<cat> … -->`，權威定義見 [`../../../README.md`](../../../README.md) §撰稿工作流程）。系統性遍布 `handout/html/fragments/**`（`intuition`／`example`／`figure`／`caution`／`application`／`formula`／`strategy`／`summary`／`history`）。
- **本審只主管兩類承重敘述：**
  - **`intuition`（最高優先）**：白話直覺、動機、informal gloss——讓初學者先有畫面再看形式。
  - **`application`**：真實情境／應用例。
- **明確不主管（交別的 owner）：**
  - `expansion:caution` 中**影響公式真假的 correctness caution**（如 radians）→ 歸**假設機制**（storyboard `meta.assumptions` registry ／ `PD4`），**不當 intuition 提**（spec §5／D4）。純記號提醒型 caution 可低優先附帶。
  - `expansion:example` → 歸 `example-supplement`（講義線），本審**不提例題**。
  - `expansion:figure` → 歸 figure 閘，本審至多附一筆 figure-note（非重點）。

## AMP1（唯一 code，advisory）——四態分類、只提 `missing`

對該節每個 handout `expansion:intuition`／`application` 標記，判影片是否已 surface（**Codex R1：放寬定義，任一模態都算 surfaced**）：

| 態 | 判準 | 動作 |
|---|---|---|
| `screened` | 上畫面文字（`statement`／`annotations`／`scaffold`／…）承載該直覺 | 資訊性列出、**不提議** |
| `narration-only` | `say`／narration 承載、但畫面沒有 | 資訊性列出、**不計入 AMP1 提議**；若判斷顯然該落畫面，另記非提議的 `[consider-screen]` 註記供參考（不算候選、不計數） |
| `visual-only` | 圖／動畫承載 | 列出、預設不提議 |
| `missing` | 影片三模態（畫面／旁白／視覺）**都沒有** | **→ AMP1 提議**：補一句敘述／一個 beat |

- **只有 `missing`（三模態都沒有）的承重直覺成為 AMP1 提議。** 這是防過度觸發的核心——大量 handout 直覺本就該在旁白、不必上畫面；`narration-only`／`visual-only` 一律**不計入提議**（見上表）。
- **判 surfaced 的權威＝ storyboard**（上畫面文字／`say`／`# HOOK`·animation）。`.md` 的 `narration`／`visual_need` 只作**交叉佐證／詮釋**，**不單獨當「已 surface」的證據**——`visual_need` 是意圖、非 storyboard 已實作的證明（Codex R6）。
- 每筆提議帶 **provenance `doc:frag-sec-*`**，但 **anchor 是節級、非標記級**（同節多個 `expansion:` 共用同一 `frag-sec`）→ 故**必附該標記的短引文／行**以定位是哪一筆（Codex R6）。這讓補進來的敘述可過 OTF、**不違反忠實層**。

## 硬紀律

- **propose-not-act、advisory-only、永不 blocking。** 只提案，使用者逐條裁決，**不強制歸零**（同 `mode-c-gapwalk`、[`NARRATION-FAITHFULNESS-RUBRIC.md`](NARRATION-FAITHFULNESS-RUBRIC.md)）。
- **只增添、不重構**——不提議改寫既有 beat、不搬既有內容。每筆是「某 beat 前／後**新增**一段敘述」。主軸已凍結。
- **反幻覺**：提議的敘述必綁 handout 標記來源（`doc:`）；不捏造出處。
- **密度校準**：傾向多提（使用者可刪）；**under-propose 才是要避免的失敗模式**。但同一直覺不重複灌水；每筆標 confidence（high／medium／low）。
- **不 re-litigate** 已認可的旁白／教學法；乾淨節候選可為零，不硬湊。

## 邊界（不重疊）

| 議題 | 既有 owner | AMP 不重疊切片 |
|---|---|---|
| `.md` 內容忠實 handout | `L1` | AMP 不審 `.md` 忠實，只問「handout 直覺有沒有 surface 到影片」 |
| narration 衍生忠實 | `NFA` | AMP 提議補敘述，非審 narration 忠實 |
| 推導掉步驟／覆蓋誠實 | `SC1`／`SC-honesty` | AMP 管敘述直覺，非推導步驟 |
| correctness caution（radians） | 假設機制／`PD4` | **不進 AMP**（改建議進 registry） |
| 該補例題 | `example-supplement`（講義線） | 不進 AMP |
| **講義側**該不該加 intuition | `mode-c-gapwalk`（講義線） | AMP 是**影片側**「handout 既有直覺有沒有 surface 到片子」，**不改講義** |

## 輸出

standalone HTML 裁決稿（比照 `mode-c-gapwalk` 的卡片格式 + [`../../../CLAUDE.md`](../../../CLAUDE.md) 交付規則、MathJax CDN 雙擊即開），路徑 `video/content_scripts/_audit/REVIEW-<deck>-amplification.html`。逐 handout 標記列四態；`missing` 者為候選卡片（category／locus＝影片哪個 beat 前後／proposal／why／`doc:` source／confidence）；末附「建議進假設機制的 correctness caution」清單。回傳繁中摘要（掃幾節／標記數、各態幾筆、`missing` 提議幾筆、HTML 路徑）。**不改任何內容檔。**
