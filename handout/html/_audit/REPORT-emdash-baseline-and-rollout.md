# em-dash 真實教材基準 · 全書 de-dash rollout（REPORT-emdash-baseline-and-rollout）

> **一句話：** 本書散文的 em-dash（`—`）密度遠高於真實數學課本與人類寫作基準，是可量測的 LLM 撰稿指紋。本檔記錄 2026-07-20 的**實測基準**、**全書現況**、**de-dash 方法**與**逐單元 rollout 待辦**。appB 已完成（16.0 → 2.2/1000）；其餘章節（含 ch01）待套用。
>
> 關聯：量測與 C6 門檻的既有依據見 [`REPORT-deai-ch1-calibration.md`](REPORT-deai-ch1-calibration.md)（Ch1 校準）；排版規則見 [`../../../CONTENT_SPEC.md`](../../../CONTENT_SPEC.md) §8「破折號」。

## 度量單位（一律用這把尺）

**散文 em-dash / 1000 詞**：剝除 HTML 註解與 `<!-- -->`、剝除數學 `\(…\)`／`\[…\]`、剝除標籤、解 entity，再數英文詞元（`[A-Za-z][A-Za-z'’-]*`）。**只算散文用的 `—`（U+2014）**，不含連字號 `-`、en dash `–`、數學內的任何字元。這與去 AI 味報告的「散文 em-dash/500 字」同源（×2 換算）。

## 1. 研究結果：真實教材基準

以**同一把尺**實測本機 `problem_banks/` 與線上抓取的真實開源微積分課本說明散文（非習題）：

| 教材（實測） | 格式 | em-dash | 散文詞 | **/1000** |
|---|---|--:|--:|--:|
| mooculus | LaTeX (`digIn*.tex`) | 18 | 199,472 | **0.09** |
| Active Calculus（Boelkins） | PreTeXt | 27 | 234,097 | **0.12** |
| APEX Calculus V5 | PreTeXt (`<mdash/>`) | 74 | 248,352 | **0.30** |
| **OpenStax Calculus**（全美最主流） | CNXML（字面 `—`） | 152 | 399,160 | **0.38**（Vol 1：0.37） |
| CLP1（Feldman；六本中最口語） | PreTeXt (`<mdash/>`) | 495 | 145,708 | **3.40** |

已發表基準（對照）：

- **人類寫作平均 ≈ 3.23/1000**（median 3.83、range 0.33–17.12），來源 arXiv **2603.27006**《The Last Fingerprint: How Markdown Training Shapes LLM Prose》，語料＝8 篇散文（文學評論／新聞／技術寫作，57,232 詞）。
- 同論文 **LLM 未受限**：GPT-4.1 10.62、Claude Opus 4.6 9.09、Claude Sonnet 4 8.29、GPT-4o 4.12、Llama 0.00。
- LLM 時代 em-dash 頻率群體性上升另見 arXiv **2606.29540**《Em-ergence of the em-dash》（medRxiv preprints）。

**結論：** 五本真實課本落在 **0.09–3.40/1000**；數學書尤其貼近人類寫作的**地板**（改用括號／冒號／分號／短句——實測 APEX 248k 詞裡有 66,419 個 `(`、破折號幾乎為零）。**本書任何一章的 em-dash 密度都超過其中四本、多數超過全部五本**（見 §2）。這不是「差一點」，是差一到兩個數量級的 AI 指紋。

## 2. 全書現況（per-unit，2026-07-20，散文詞法）

| 單元 | em-dash | 散文詞 | **/1000** | 狀態 |
|---|--:|--:|--:|---|
| **appB** | 24 | 10,873 | **2.2** | ✅ 已 de-dash（本輪；原 16.0） |
| appD | 2 | 2,342 | 0.9 | 本就低，無需處理 |
| ch01 | 54 | 9,860 | 5.5 | ⏳ 待做（去 AI 味簽核基準，最低的一章，但仍 >真實課本） |
| ch03 | 55 | 6,849 | 8.0 | ⏳ 待做 |
| ch04 | 87 | 10,791 | 8.1 | ⏳ 待做 |
| ch06 | 87 | 9,073 | 9.6 | ⏳ 待做 |
| ch05 | 120 | 11,165 | 10.7 | ⏳ 待做 |
| ch02 | 120 | 10,839 | 11.1 | ⏳ 待做 |
| appA | 64 | 5,008 | 12.8 | ⏳ 待做 |
| appC | 21 | 1,835 | 11.4 | ⏳ 待做 |
| ch07 | 180 | 13,656 | 13.2 | ⏳ 待做（全書最高） |

**目標值：** 收到 **≤ ~3/1000**（CLP／人類平均檔位）即脫離指紋區；理想往 OpenStax／APEX 的 ~0.3–0.5 但那是大幅重寫。appB 落在 2.2。**注意：** 去 AI 味報告當初刻意保留 Ch1 的破折號節奏（視為合法招牌），並把 C6 天花板設在 4.0/500（＝8.0/1000）——那條線本身**高於**真實課本；本研究把目標從「本書 Ch1 基準」下修到「真實教材基準」。

## 3. 方法：cut / keep palette（appB 已驗證，Codex 覆核通過）

**硬護欄：語義一律不變；只動標點與必要連接詞，數學逐位元組不碰。**

- **CUT（AI tell 主力）**
  - 單破折號「子句 — 補述／改寫」尾巴 → **冒號**（交付 payload）／**逗號**（鬆散同位語）／**分句**（後段是獨立子句）。
  - 可用括號的插入語 → **括號 `( )`**（尤其插入語本身含逗號或清單）。
- **KEEP（真正承重）**
  - **句中對稱插入語**（刻意打斷主句的強調節拍）：如 `— far more often —`、`— only then —`、`— and over the integers you never can —`。
  - 引號內**對白式**停頓：`"ah, that one again — what is it buying here?"`。
  - CONSTRAINT 註解標明「多處須平行」的措辭：如 appB §B.6 的 `— and the one to try first —`（動一處會使三處失步）。
  - worked-solution 的電報式 gloss、無動詞短句尾（分句會變殘句）——保留破折號。
- **Codex 覆核要點（避免用一個 tic 換另一個）**
  - **不要**在同一句造出**雙冒號**（前一個冒號還在時，後段改分句）。
  - **不要**把括號堆在既有括號旁（尤其鄰近 `\(…\)` 數學）；該處改逗號／分句。
  - `→ 冒號` 用太多會變**新的冒號 tic**；命題轉命題處改**分句**，冒號只留給真正的清單／定義。
  - **不要**把承重的外層量詞（`for all rational r and s`）用括號降級。

## 4. 驗證 recipe（可重用；appB 實跑）

1. **列舉**：程式掃出每個 `—` 的**原始位元組**上下文（排除 `<!-- -->` 註解、只在 `<article>` 內），得權威工作清單（勿手工轉抄 entity）。
2. **裁決稿**：逐處「原句 → 建議改法 → 理由」，產 standalone HTML（MathJax、雙擊即開），供使用者過目。
3. **Codex 覆核**：`codex exec -s read-only`（唯讀，逐次徵得同意）對抗式 review；findings 分 BLOCKING／ADVISORY，逐條查證後折入。
4. **交易式套用**：每筆 `(old→new)` `assert` 只命中一次、逐檔全對才寫；套用後逐檔 em-dash 數命中保留目標。
5. **硬護欄證明**：**reverse-apply == HEAD**——把改動逆轉後 byte-for-byte 等於 HEAD，即「HEAD＋恰好這些標點改動、其餘一字未動」；連帶證明數學與 tag skeleton 不變、括號成對平衡。
6. **build ＋回歸**：`python handout/html/build.py <unit>` 重組；重數密度、抽查渲染。
7. **定稿進 LaTeX 線**：`python convert.py <unit> --out …`（0 skipped、數學 pass-through）→ `python make_dist.py <unit>`（三閘全綠）。

**工具硬化（本輪）：** `check_prose.py` 的完整性閘原只接合**同頁**行末連字（`-\n`），跨頁斷字時 running header／folio 會插進兩截之間（實測 appB `conditions` 抽成 `con` + `10 B.4 Steps…` + `ditions`），被誤報「真落差」。已補 `_page_split()`：PDF span 以詞的 prefix 開頭、又以其餘 suffix 結尾即判為抽取假象（護欄 len≥5，短詞不走此路）。這是**通用**修正，之後每章 rollout 都受用。

## 5. Rollout 待辦

- **ch01 也還沒做**（回答使用者提問）：ch01 是去 AI 味簽核基準、全書最低（5.5/1000），但仍是人類平均的 ~1.7×、OpenStax 的 ~14×——若目標是「讀起來像真數學課本」，ch01 一樣要收。它最不急、幅度最小。
- 建議優先序（由重到輕）：ch07 (13.2) → appA (12.8) → appC (11.4) → ch02 (11.1) → ch05 (10.7) → ch06 (9.6) → ch04 (8.1) → ch03 (8.0) → ch01 (5.5)。appD (0.9) 免。
- 每章照 §3 palette、§4 recipe 各跑一輪；章內若有 CONSTRAINT 平行措辭需逐檔查（如 appB §B.6）。
- 完成後於 §2 表更新密度並打勾。

---
*Record（本輪 appB）：裁決稿 [`REVIEW-appendixB-dedash-candidates.html`](REVIEW-appendixB-dedash-candidates.html)（含 Codex 覆核與回歸結果）。*
