# 看片多鏡評審 — REWATCH（成片品質評審，五鏡並審）

> 本檔是「看片多鏡評審（rewatch multi-lens review）」的契約與**單一真相來源（SSOT）**。被審物是**已 render 的成片**，以觀眾的方式看：時間、停留、畫面有沒有動、跟不跟得上。它補的是評估報告（[`../../_audit/REVIEW-pipeline-assessment-2026-09-07.html`](../../_audit/REVIEW-pipeline-assessment-2026-09-07.html) F8）點出的缺口：既有視覺閘審靜幀、教學閘審 storyboard 結構，**沒有任何一閘看過影片本身**。
>
> **性質：品質評審、advisory、propose-not-act、永不 blocking。** 忠實（NFA）、數學正確（L5／D7）、上畫面文字回溯（OF）各有 owner，本審**不重審**。輸出是給使用者裁決「重做水位」的證據，不是擋稿。
>
> **2026-09-12 立檔（首用＝ch03 §3.1 成片）。是否常設為閘，另議。**

## 被審物：rewatch pack

模型評審員讀得了圖與字、聽不到聲音、也不能播放影片，所以先由 [`../../pipeline/rewatch_pack.py`](../../pipeline/rewatch_pack.py) 把成片翻譯成 pack（`output/<ch>/<sec>/rewatch_pack/`，gitignored、可重生）：

- `INDEX.md`：全片 27 場總表——每場的全片起點、秒數、reveal 數、畫面靜止比例、最長不動秒數、「與 reveal 無關的畫面變化」次數，以及讀法說明。
- `NN_<scene>.sheet.jpg`：每場一張 contact sheet，8–12 格抽幀。**每格的標籤＝場內第幾秒、全片時間、為何抽這格（場首／某 beat 的 reveal 之後／長 beat 中段／場末最滿幀）、此刻旁白正念到哪幾個字（方括號＝當下那個字；`~`＝在該 beat 內線性內插的近似）**。右上角小長條圖＝該場每 2 秒的畫面變化量。
- `NN_<scene>.md`：該場的時間軸——逐 beat 的 reveal 目標、起訖秒、每秒字數、口語全文；同一段的書寫版（LaTeX）；靜止統計；每格抽幀的對照表。
- `NN_<scene>/f_XX_+<t>s.jpg`：抽幀原尺寸（1920×1080），看不清時開這個。

**時間模型**：content 場＝1 秒 lead → 每個 beat 各念各的秒數（reveal 動畫在 beat 起點播）→ 1 秒 tail。畫面靜止比例的定義：每秒取樣 4 次、低解析度，超過 0.2% 像素變動算「有動」。

## 共同規則（每一鏡都適用）

1. **只憑 pack 判斷。** 看得到的、時間軸寫的、數字算出的才算證據；沒看到的不要推論。無法判斷就寫「無法從 pack 判斷」，不要補腦。
2. **每條 finding 必附證據**：場 id ＋ 格號（`tile 04`）或秒數（`+39.3s`）＋ 一句旁白引文或畫面描述。沒有證據的 finding 會在合成時被駁回。
3. **嚴重度三級**：`must`＝會讓初學者跟丟或形成錯誤印象；`should`＝明顯提升教學效果；`nice`＝錦上添花。
4. **每場給 verdict**：`good`／`ok`／`weak`／`bad`（初學者鏡的對應：輕鬆跟上／跟得上但費力／部分跟丟／卡住或誤解）。乾淨的場就寫 `good` 或 `ok` 並留空 findings——**乾淨是有效結果，不要硬湊**。
5. **每條 finding 要有 proposal**：不只說「哪裡不對」，要說「你想變成怎樣」，具體到能動手（例：「beat 3 念到 sector 時，讓扇形從 O 掃出來 1.5 秒，而不是整塊淡入」）。
6. **不審**：數學對錯、旁白是否忠於講義、發音／語氣（聽不到）、品牌／解析度。看到疑似數學錯可以在 `note` 提一句，但不算 finding。
7. **語言**：繁體中文；旁白引文、識別碼（scene id、tile、reveal 名）保留英文原樣。
8. **獨立**：不跟其他鏡商量、不猜其他鏡會說什麼；你只代表你這一鏡。

## 五鏡

### R1 初學者（Learner；盲測、派兩份獨立實例）

- **你是誰**：第一次學這一節的學生（先備＝ CONTENT_SPEC §16.2 基線讀者：會三角函數基本定義與恆等式、會極限與導數定義、剛學完多項式與 e^x 的導數；**還不知道** sin′＝cos）。
- **怎麼看**：從 `01` 到 `27` **線性**看，一場看完才看下一場；每場先讀 sheet 再讀 md。不要回頭修改前面的判斷（第一次看就是第一次看）。
- **維度**：
  - `L-follow` 跟不跟得上：這場結束時你知道它證了什麼、算了什麼嗎？
  - `L-why` 你知道為什麼要做這一步嗎？（動機有沒有被說出來）
  - `L-attention` 走神點：哪裡讓你想快轉（畫面很久沒變、字太多、一直在念）
  - `L-picture` 畫面有沒有幫到你，還是「只是字」？哪一格讓你恍然大悟、哪一格看了沒感覺？
  - `L-recall` 全片看完，你記得的三件事是什麼？記錯的算 finding。
- **輸出重點**：每場的 verdict（用共同規則的四級）＋卡點；`film.patterns` 寫你整體的感受（三到五句）。

### R2 動畫導演（Director）

- **你是誰**：做數學解說影片的導演，在意「畫面有沒有在教」。
- **維度**：
  - `D-motion` 畫面是否**隨數學演化**（該變形的變形、該掃過的掃過、該對齊的對齊），還是只是「東西出現、停住」？
  - `D-focus` 此刻該看哪裡，畫面有沒有引導（高亮、聚焦、退淡）？
  - `D-carry` 動畫承載教學點，還是裝飾？哪些教學點**本該**用動作表達卻用文字帶過？
  - `D-composition` 版面：留白、層次、字量、圖與字的關係。
  - `D-continuity` 場與場之間的視覺連貫（同一個圖形換場後有沒有延續）。
  - `D-dwell` reveal 之後的停留：夠看完嗎、還是停太久變成投影片？
- **輸出重點**：每場 verdict ＋ findings；`film.patterns` 寫全片的視覺語言診斷；對每一場給**一個最值得做的動作**（proposal 要具體到「什麼東西怎麼動、幾秒」）。finding 對得上畫面語法規則就標 `rule`（`ML1`–`ML5`，定義見「輸出格式」的 `rule` 小節）。

### R3 教學設計（Lesson-arc designer）

- **你是誰**：課程設計者，在意這一節「作為一堂課」的形狀。你**可以**讀講義原節（`.tex`）判斷該教的東西有沒有被安排進弧線裡，但不重審忠實。
- **維度**：
  - `A-arc` 弧線：引導問題 → 探索／直覺 → 形式化 → 鞏固／回顧。引導問題是什麼、在哪裡被回答？
  - `A-order` 順序是教學順序，還是課本環境的順序？哪裡調換會更好教？
  - `A-motive` 每場開頭有沒有「為什麼現在做這個」？
  - `A-load` 認知負荷：一場塞了幾個新想法？哪裡該拆、哪裡該併？
  - `A-bridge` 場與場的銜接：上一場的結論有沒有被下一場接住？
  - `A-recap` 回顧場有沒有回到引導問題？
- **輸出重點**：`film.patterns` 先寫你眼中這堂課的弧線（或它沒有弧線的證據）；每場 verdict ＋ findings。

### R4 節奏剪輯（Rhythm editor；只看數字與時間軸，不看圖）

- **你是誰**：剪接師，用秒數說話。
- **維度**：
  - `T-rate` 每秒字數與 reveal 密度：念得快又長時間沒新東西上畫面的段落。
  - `T-dwell` 承重步驟（證明的關鍵一步、結論式）之後有沒有停留？停多久？
  - `T-still` 最長不動秒數；超過 15 秒的靜止段落逐一列出並說明此時旁白在講什麼。
  - `T-beat` 超過 25 秒沒有 reveal 的 beat。
  - `T-balance` 場長分布：哪幾場相對其內容過長／過短？
- **輸出重點**：每條 finding 都帶數字（現況幾秒、建議幾秒）；`film.patterns` 給全片的節奏診斷（例如「平均每 X 秒一個 reveal，難步驟後平均停留 Y 秒」）。

### R5 資深講師（Instructor）

- **你是誰**：教過這一節十次以上的微積分老師。
- **維度**：
  - `I-emphasis` 專家會特別強調、而影片輕輕帶過的點。
  - `I-misconception` 常見誤解（例如「極限等於恆等式」「度數也行」「sin′＝cos 是定義」）有沒有被預先擋住？擋的時機對嗎？
  - `I-timing` 對的東西有沒有在對的時刻出現（太早、太晚、該回顧時沒回顧）？
  - `I-example` 例子選得好不好、順序對不對？
  - `I-language` 口頭說法會不會誤導（引旁白原句）。
- **輸出重點**：每場 verdict ＋ findings；`film.patterns` 寫「如果是我來講，我會改的三件事」。

## 輸出格式（機器可讀；合成靠它）

**只輸出一個 JSON 物件**（schema 見 [`rewatch-findings.schema.json`](rewatch-findings.schema.json)），不要前後加說明文字：

```json
{
  "lens": "R2",
  "film": {
    "overall": "一段話總評",
    "patterns": ["全片共同模式 1", "…"],
    "strongest_scenes": ["scene_id", "…"],
    "weakest_scenes": ["scene_id", "…"]
  },
  "scenes": [
    {
      "id": "<scene_id>",
      "verdict": "weak",
      "note": "（選填）一句話",
      "findings": [
        {
          "dim": "<本鏡的維度代碼>",
          "severity": "should",
          "rule": "ML2",
          "where": "tile 05 (+46.1s)",
          "evidence": "旁白念「…引文…」時，畫面上…（描述你實際看到的）",
          "problem": "為什麼這對觀眾是問題",
          "proposal": "你想變成怎樣，具體到能動手（什麼東西、怎麼變、幾秒）"
        }
      ]
    }
  ]
}
```

- `scenes` 必須 27 場齊全（順序同 INDEX），乾淨場 `findings: []`。
- `where` 一律含格號或秒數；`evidence` 一律含引文或畫面描述。
- `rule`（選填）＝這條 finding 違反的畫面語法規則代號，見下節；未標的在 digest 歸「未標」。

### `rule`：畫面語法規則代號（選填；R2 MUST、其他鏡 MAY）

值域＝[`../../SPEC-motion-language.md`](../../SPEC-motion-language.md) §0 的五條規則，代號 `ML1`–`ML5`（ML＝motion language；不用 R1–R5，免與鏡頭編號撞名）。**R2 動畫導演鏡 MUST 標**——finding 對得上規則就標，對不上留空；**其他鏡 MAY 標**。合成後 digest 按它計數（`by_rule`：總計＋每場），HTML 出「finding × 規則」小表。

| 代號 | 規則 | 一句話（SPEC §0） | 對位機制（DESIGN.md） |
|---|---|---|---|
| `ML1` | 一場一張畫布 | 承重物件在一幕裡只建一次，換步驟用位移／縮放／複製搬去新佈局；臨時標註縮小加淡出退場 | 原語 5（跨場延續） |
| `ML2` | 畫出來，只動變的 token | 曲線由點走出、文字逐字寫、式子只動變的 token；整行 FadeOut 再 FadeIn 是反模式 | `anim: transform`、`paced:` |
| `ML3` | 框、放大鏡、調暗，不靠鏡頭 | 注意力用框選預備、inset 放大（主圖不縮放）、主圖降亮；2D 場不以 zoom 為第一選擇 | `focus:` |
| `ML4` | 靜止是設計出來的 | 每段超過 6 s 的靜止 MUST 是宣告的（`pauses:`）或被 paced／sweep 填滿；動作只在步驟切換時發生 | `pauses:`、`paced:`、`seconds: beat`、12 s 驗收線 |
| `ML5` | 語意色貫穿圖與式 | 同一變數在圖、括號、軸標、填色、式子 token 用同色；卡類型色與箭頭色本身就是語意 | `color_role` |

## 編排（orchestrator 的事，評審員不必讀）

- **盲的層級**：R1 兩份實例只拿 pack 的觀眾面（sheet／md／INDEX／幀），**不給** `PRODUCTION.md`、`pack.json`、storyboard、任何既有評估或裁決；在 repo 外的隔離工作區跑。R2／R5 拿 pack ＋ 本鏡段落；R3 另拿講義原節 `.tex`；R4 只拿 md／INDEX（不看圖）。**任何一鏡都不給** 7 月 grilling 結論、產線評估報告、其他鏡的輸出。
- **模型分派（首用 2026-09-12）**：R1a Gemini 3.1 Pro（agy）、R1b Claude Sonnet 4.6（agy）、R2 Claude Opus 5（subagent）、R3 Claude Sonnet 5（subagent）、R4 Claude Haiku 4.5（subagent）、R5 Gemini 3.8 Flash（agy）；合成＝Fable。三個模型家族、單一模型不重複同鏡。
- **合成（refute-by-default）**：逐條對 pack 核實——找得到的 evidence 才留；多鏡同指一場加權；套 CLAUDE.md 四級分類；產 standalone HTML（`REVIEW-<deck>-rewatch-multilens.html`，逐場並列五鏡＋ sheet ＋數字＋合成判定＋「每場最該改的一件事」），餵 Step ② 水位決定。
- **工具**：`_gen/rewatch_prompts.py --ws <repo 外目錄> --runs … [--scenes …]`（組隔離工作區與每鏡 prompt）→ 跑鏡 → `_gen/rewatch_merge.py --ws … --verify verify.json --out …`（合併＋核實 → digest）→ `_gen/rewatch_multilens.gen.py`（digest → HTML）。
- **agy 呼叫**：見根 [`../../../CLAUDE.md`](../../../CLAUDE.md)「付費 API」節（唯讀 `--mode plan`、`--add-dir` 圈定工作區、`--json-schema` 強制輸出）。
- **首用教訓（2026-09-12，§3.1）**：① 鏡頭品質差很多——R2 Opus 5 45 條逐格引證全數核實；R1b Claude Sonnet 4.6（agy）18 條 16 條成立；R4 Haiku 15 條數字主張 11 條成立；R3／R5 各 3 條全成立；**R1a Gemini 3.1 Pro 12 條全是同一句模板、只套 INDEX 的靜止門檻**——下次初學者鏡不用它，且 prompt 要求「每條 finding 必引旁白原句＋描述 tile 畫面，否則不算」。② 「與 reveal 無關的畫面變化」曾因 pack 取樣容差誤報（reveal 淡入落在前一個 1/4 秒），R4 據此推出的 4 條全駁；已修（`rewatch_pack.py` 容差 −0.3 s）。③ 差分偵測抓不到細線／小標籤的 reveal（24 的 mirror），「靜止秒數」對這類 reveal 會高估——核實時以 manifest 的 reveal 時間為準。④ 合成時把 must／should 重新校準：單鏡的 must 若無他鏡印證且屬品味，降為 should。
