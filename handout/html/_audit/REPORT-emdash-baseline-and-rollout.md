# em-dash 真實教材基準 · 全書 de-dash rollout（REPORT-emdash-baseline-and-rollout）

> **一句話：** 本書散文的 em-dash（`—`）密度遠高於真實數學課本與人類寫作基準，是可量測的 LLM 撰稿指紋。本檔記錄 2026-07-20 的**實測基準**、**全書現況**、**de-dash 方法**與**逐單元 rollout 待辦**。appB 已完成（16.0 → 2.2/1000）、ch01 已完成（9.3 → 2.1/1000，2026-07-25 合併 sweep）；其餘章節待套用。
>
> 關聯：量測與 C6 門檻的既有依據見 [`REPORT-deai-ch1-calibration.md`](REPORT-deai-ch1-calibration.md)（Ch1 校準）。

---

## ⚠ 2026-07-25 重大更新：本線已併入平實英文條款；量尺已定版

三件事同日發生，讀本檔前必知：

1. **政策搬家。** cut/keep palette、密度目標、成對插入語仲裁、不換 tic 護欄**已全部併入 [`CONTENT_SPEC.md`](../../../CONTENT_SPEC.md) §3〈平實英文條款〉的「成對破折號與標點負載」小節**；§8「破折號」只留字元排印區辨並指向 §3。**本檔自此只是基準與 rollout 帳本，不是政策來源。** 合併理由（含「兩線互相抵銷」的實測證據）見 [`REVIEW-merge-dedash-plain-proposal.html`](REVIEW-merge-dedash-plain-proposal.html)，經 Codex 設計審查（有條件通過）。
2. **量尺定版。** 唯一真實來源為 [`tools/prose_metrics.py`](../../../tools/prose_metrics.py)（canonical prose stream；22 項 entity／格式 fixture 全綠）。舊腳本有兩個缺陷：**(a) 只數字面 `—`，漏掉 entity**；**(b) 散文詞分母定義與平實線不同**（同一單元 ch07 的 dash 數相同、分母差 3172 詞）。下方 §1／§2 的表已改用 canonical 重測值，舊值以刪節線保留供追溯。
3. **一個結論被推翻：`appD` 不是「無需處理」。** 舊表記 0.9／「本就低」，實為量測 bug——appD 是全書唯一用 `&mdash;` entity 寫破折號的單元（20 entity ＋ 4 字面），canonical 實測 **13.2/1000**，與其他待做單元同級。

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

**canonical 重測（2026-07-25，`python tools/prose_metrics.py --external`）**——本機語料三本，與上表同一批文本但改用定版量尺：

| 教材 | canonical N | em-dash | **/1000** | 舊尺 /1000 |
|---|--:|--:|--:|--:|
| mooculus | 613,813 | 21 | **0.0** | 0.09 |
| APEX Calculus V5 | 60,805 | 30 | **0.5** | 0.30 |
| CLP1 | 111,032 | 348 | **3.1** | 3.40 |

（OpenStax 與 Active Calculus 為當時線上抓取、本機無語料，沿用舊值 0.38／0.12。）**兩把尺的密度落在同一區間**——這是量尺換手後仍可沿用 `T_can ≤ 3.0` 的依據。

已發表基準（對照）：

- **人類寫作平均 ≈ 3.23/1000**（median 3.83、range 0.33–17.12），來源 arXiv **2603.27006**《The Last Fingerprint: How Markdown Training Shapes LLM Prose》，語料＝8 篇散文（文學評論／新聞／技術寫作，57,232 詞）。
- 同論文 **LLM 未受限**：GPT-4.1 10.62、Claude Opus 4.6 9.09、Claude Sonnet 4 8.29、GPT-4o 4.12、Llama 0.00。
- LLM 時代 em-dash 頻率群體性上升另見 arXiv **2606.29540**《Em-ergence of the em-dash》（medRxiv preprints）。

**結論：** 五本真實課本落在 **0.09–3.40/1000**；數學書尤其貼近人類寫作的**地板**（改用括號／冒號／分號／短句——實測 APEX 248k 詞裡有 66,419 個 `(`、破折號幾乎為零）。**本書任何一章的 em-dash 密度都超過其中四本、多數超過全部五本**（見 §2）。這不是「差一點」，是差一到兩個數量級的 AI 指紋。

## 2. 全書現況（canonical 重測；2026-07-26 合併回收後）

`python tools/prose_metrics.py`。tic guard 四項（冒號接子句／分號／左括號／成對逗號）一併記為基線，供每輪比對。

| 單元 | em-dash | canonical N | **/1000** | 冒號 | 分號 | 括號 | 雙逗號 | 狀態 |
|---|--:|--:|--:|--:|--:|--:|--:|---|
| **ch05** | 6 | 7,667 | **0.8** | 79 | 42 | 44 | 29 | ✅ 已達標（原 14.4；執行 115 條）——[`REVIEW-ch05-plain-applied.html`](REVIEW-ch05-plain-applied.html) |
| **ch02** | 6 | 6,992 | **0.9** | 58 | 39 | 68 | 24 | ✅ 已達標（原 16.7；執行 109 條，Codex ADOPT 74／MODIFY 25／REJECT 1）——剩 3 對 KEEP；**LaTeX 線四閘全綠、`dist/ch02/` 已產出**。[`REVIEW-ch02-plain-applied.html`](REVIEW-ch02-plain-applied.html)、[`DIALECT-ch02.md`](../../latex/chapters/ch02/DIALECT-ch02.md) |
| **ch03** | 6 | 3,855 | **1.6** | 33 | 18 | 59 | 34 | ✅ 已達標（原 14.0；執行 66 條）——[`REVIEW-ch03-plain-applied.html`](REVIEW-ch03-plain-applied.html) |
| **ch07** | 14 | 8,937 | **1.6** | 92 | 36 | 56 | 43 | ✅ 已達標（原 17.5，全書超額最多的單元；執行 146 條）——[`REVIEW-ch07-plain-applied.html`](REVIEW-ch07-plain-applied.html) |
| **ch01** | 12 | 5,810 | **2.1** | 42 | 20 | 37 | 41 | ✅ 已達標（原 9.3；執行 41 條）——剩下 12 個＝**手稿逐字 8**（4 對成對插入語，使用者裁決比照 §1.4 保留）＋**§1.4 凍結 4**；[`REVIEW-ch01-plain-applied.html`](REVIEW-ch01-plain-applied.html) |
| **appB** | 17 | 7,793 | **2.2** | 99 | 32 | 48 | 25 | ✅ 已達標（原 17.1；~~舊尺 2.2~~） |
| **ch04** | 16 | 6,939 | **2.3** | 68 | 43 | 82 | 27 | ✅ 已達標（原 13.3；執行 97 條）——[`REVIEW-ch04-plain-applied.html`](REVIEW-ch04-plain-applied.html) |
| ch06 | 72 | 5,770 | 12.5 | 41 | 37 | 52 | 32 | ⏳ **進行中**（走查與 Codex gate-2 已產出、尚未提交）；§6.2／§6.3 早先已平實化但 dash 未做 |
| **appD** | 18 | 1,363 | **13.2** | 18 | 13 | 17 | 6 | ⏳ 待做——~~舊表誤標「0.9 無需處理」~~（entity bug） |
| appC | 24 | 1,347 | 17.8 | 8 | 15 | 7 | 3 | ⏳ 待做；**N<1000 附近，報 raw 24/1347**（~~舊尺 11.4~~） |
| appA | 58 | 3,081 | 18.8 | 32 | 24 | 18 | 8 | ⏳ 待做，全書最高（~~舊尺 12.8~~） |

**進度：11 個單元中 7 個達標**（appB／ch01–ch05／ch07），剩 ch06（進行中）＋appA／appC／appD 三個附錄。
2026-07-26 的合併回收一次併回六輪成果（ch02／ch03／ch04／ch05／ch07 五條分支，無衝突），**全書複測無任何單元回退**。

**目標值 `T_can` ≤ 3.0/1000（canonical stream）。** 依據＝canonical 重測的真實教材基準（§1）：mooculus 0.0、APEX V5 0.5、CLP1 3.1。目標貼 CLP1（五本中最口語者）的上緣；已達標的七個單元落在 **0.8–2.3**，全數在 APEX（0.5）與 CLP1（3.1）之間。

**ch01 順帶量到的手稿基線（2026-07-25，本線第一份真人對照）：** 手稿 [`legacy/tex_handout/chapters/ch01_foundations.tex`](../../../legacy/tex_handout/chapters/ch01_foundations.tex) 的**散文**（排除 itemize，與 canonical 同分母）em-dash **11／4,541 詞＝2.42/1000**，本來就在 `T_can` 之內；fragment 的 9.3 幾乎全來自 LLM 增補段落（54 處中手稿逐字僅 9，且**20 個單破折號尾巴全部是 LLM 寫的**）。這推翻了「ch01 的破折號節奏是作者招牌」的舊說法，也是「改用真實教材基準」政策轉向最強的一次驗證（詳見 [`REVIEW-ch01-plain-walk.html`](REVIEW-ch01-plain-walk.html) Gate 0）。

**不下修到 0.3–0.5**（2026-07-25 Codex 裁決）：那是模仿特定教材風格而非品質底線，且會迫使合法的節拍插入語轉成冒號／括號／逗號 tic——正是本線在 appB 已犯過一次的錯（見上方 ⚠ 第 1 點）。

**注意（歷史）：** 去 AI 味報告當初刻意保留 Ch1 的破折號節奏（視為合法招牌），並把 C6 天花板設在 4.0/500（＝8.0/1000）——那條線本身**高於**真實課本；本研究把目標從「本書 Ch1 基準」改為「真實教材基準」。

## 3. 方法：cut / keep palette

> **2026-07-25：本節內容已升格為政策，權威版在 [`CONTENT_SPEC.md`](../../../CONTENT_SPEC.md) §3「成對破折號與標點負載」**（含四步仲裁決策序與具約束力的先例：`— far more often —` KEEP、`— and over the integers you never can —` 整句重寫、`— only then —` 預設 KEEP）。下方保留原始 palette 供追溯；**兩者衝突時以 §3 為準**——特別是「KEEP 成對插入語」現在有明文前提（移除插入語後主幹仍是一個教學動作），且 **MUST NOT 只把成對破折號換成逗號**。

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

## 5. Rollout 待辦（2026-07-25 合併後重排）

**每單元跑的是「合併 sweep」，不再是單獨的 de-dash 輪**——固定執行序（CONTENT_SPEC §3）：① 範圍／數學安全 → ② 論述動作判讀 → ③ CUT／KEEP → ④ 節級密度閘 → ⑤ 不換 tic 檢查。一份走查稿、一份 applied、一個 commit；每個改點標原因標籤（`DASH-CUT`／`DASH-KEEP`／`PLAIN-SPLIT`／`TIC-REBALANCE`／`R1-LEXICAL`）。

**排序原則（Codex 2026-07-25）：不要只看密度**，以「超額 dash 的原始件數 `max(0, n − T_can·N/1000)`」＋加權的平實未解項＋讀者曝露量排序。依此計算的超額件數：

| 批次 | 單元 | 超額件數 `n − 3N/1000` | 備註 |
|---|---|--:|---|
| **blocker** | appB dist 重出 | — | 產物脫鉤：`dist/appB/` 停在 de-dash commit，fragment 已被平實兩輪改過（appB 是 LaTeX pilot GO 單元） |
| 1 | ch07 | 128 | 最新章，改完可當「新章標準流程」樣板 |
| 2 | ch02 | 95 | |
| 3 | ch05 | 86 | |
| 4 | ch04 | 71 | |
| 5 | ch06（§6.1／§6.4／§6.5） | 55 | §6.2／§6.3 已平實化但 dash 未做；**§6.1 另有兩段 ≥150 詞的段落離群** |
| 6 | appA | 49 | |
| ~~7~~ | **ch03** | ~~42~~ | ✅ **2026-07-25 完成**。執行 66 條（走查 50＋Codex Q6 第二波 16）、14.0→1.6/1000、既有數學片段零改動、分頁 27 頁不變；Codex gate-2 ADOPT 38／MODIFY 12／REJECT 0（抓到一處既有課文錯誤：continuity 只管差商的第一個因子）。**Gate 7（LaTeX）四閘全綠、`dist/ch03/` 成品已產出**（完整性閘的假紅修法＝`check_prose.py` 改用 `pdftotext -raw`；字形閘的 Times 後備修法＝圖匯出改用 repo 內附的完整 Inter，Google Fonts 的子集不含 U+2080）。紀錄 [`REVIEW-ch03-plain-applied.html`](REVIEW-ch03-plain-applied.html) |
| ~~8~~ | **ch01** | ~~37~~ | ✅ **2026-07-25 完成**（提前做：RC 後第一個回填單元，用它驗證條款在手稿章不誤傷）。執行 41 條、9.3→2.1/1000、數學片段零差異、分頁 53 頁不變、§1.4 對照組零改動；Codex gate-2 ADOPT 34／MODIFY 7／REJECT 1。**Gate 7（LaTeX）四閘全綠、成品已產出**：`NAMES` 補 ch01、九條方言 mapping、33 panel 圖匯出；閘 1 編譯（44 頁／0 error／0 missing char／0 overfull）、閘 3 完整性（0 真落差）、閘 3b 表格（新增，18 格）、閘 3c 圖內文字（13 條 note）、閘 4 字形（489 字形輪廓）全 PASS。`dist/ch01/` ＝ chapter1.tex ＋ chapter1.pdf。多 panel 圖的 grid 版面 2026-07-26 補上（Figure 1.1 併成一列、Figure 1.17 排 2×2，圖說不再孤立）。紀錄 [`../../latex/chapters/ch01/DIALECT-ch01.md`](../../latex/chapters/ch01/DIALECT-ch01.md) |
| 9 | appC | 20 | N<1000 附近，報 raw 並與鄰近單元合併判定 |
| 10 | appD | 14 | 舊表誤標「免」，實需處理 |

- **新增章節不進本清單**：合併後 em-dash 目標與 palette 已在 §3，Mode A 的 brief 與完稿自檢直接呼叫 `tools/prose_metrics.py`＝**生成端就受約束**。下一個新節同時作為「生成端兩臂對照」的場地（一臂只給範文、一臂掛完整條款），用以驗證新章是否還需要回填輪。
- 每輪完成後於 §2 表更新密度與 tic guard 四項並打勾。

---
*Record（本輪 appB）：裁決稿 [`REVIEW-appendixB-dedash-candidates.html`](REVIEW-appendixB-dedash-candidates.html)（含 Codex 覆核與回歸結果）。*
