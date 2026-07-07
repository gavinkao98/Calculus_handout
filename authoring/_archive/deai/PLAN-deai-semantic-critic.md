> **Status: archived / completed（2026-07-07 歸檔）** — 本計畫已落地：Vale lane＝advisory 預標（`ENVIRONMENT.md` §⑤b）、語意/聲音 S·A·V critic＝`handout/_audit/PROSE-AUDIT-RUBRIC.md` Dimension C。本檔為歷史施工紀錄，勿當現行流程；內含相對路徑可能已過時。

# PLAN-deai-semantic-critic — 語意/聲音 critic（取代 metric Dimension C）

> **本檔是什麼：** 「去 AI 味」方案的**偵測設計第二版**。取代 [`PLAN-deai-flavor.md`](PLAN-deai-flavor.md) 與 [`PLAN-deai-flavor-implementation.md`](PLAN-deai-flavor-implementation.md) 中「靠 Vale 清單＋Dimension C 數 tell／密度」的偵測層；其餘（三層架構的「預防」框架、不用 AI-detector、授權政策、§3 語域權威）不變。
>
> **為什麼有這份：** 真人語料校準（2026-06-26）證明舊偵測層在「數學教科書」這個窄語域天花板很低——見 §0。
>
> **語言：** 繁體中文；LaTeX／程式碼、套件名、檔名、技術術語（Vale、Dimension C、S/A/V、gate、propose-only…）保留英文。
>
> **狀態：** 設計已與使用者逐段拍板（2026-06-26，Q1–Q4＋§1–§4＋錨定）。本檔為權威設計錨；逐 task 實作展開另出 implementation plan。

---

## 0. 為什麼改（pivot 緣由，2026-06-26）

用 open-licensed 真人微積分教材當 ground truth 校準後，三件事推翻了舊偵測層的前提：

1. **可量測的結構指標分不出人/AI。** 同一把尺量 em-dash 密度（/500 字）：真人 **OpenStax 0.63、CLP-1 7.32**（跨度 10×，純家規差異）；**Ch1 4.12、Ch2 8.22** 都落在真人區間內。先前「Ch1 是 AI 灌水」是單一出版社（OpenStax 特別不愛 em-dash）的假象。其他維度（句長、burstiness）講義反而比真人**更短、更參差**（反 AI 方向）。
2. **數學說明文是高度約定俗成的窄語域。** 可用的搭配詞與句型就那一小撮（`Let f be`／`Notice that`／`approaches`／`It follows that`…），真人作者和 AI 都從同一個 pool 抽 → style/tell-based 偵測**天生**天花板低。Vale 的 14 條 banned 清單對真人**和**講義都 0 命中，因為那份清單源自一般散文的 AI-slop，根本不屬於數學教科書語域。
3. **殘留的 AI 味在語意層，不在指標。** 中性 **≠** AI（OpenStax 純中性卻讀來全然像人）；**中性＋空**才是 AI。真正分得出的是：每句有沒有言之有物、高度對不對、§3 那點暖在不在。這些只有「讀意思」抓得到，lint／密度抓不到。

**目標（使用者拍板）：積極 — 讓講義跟好的人類教科書難以分辨。** 但循上述，路徑不是收緊指標門檻，而是**語意層的逐句編輯**，瞄準 §3 既定語域。

---

## 1. 已拍板決策（Q1–Q4，勿 re-litigate）

- **Q1 形態：** critic 同時**偵測→改寫**，propose-only（讀出哪句空/平/高度不對，再提改寫，使用者裁決）。
- **Q2 聲音目標：** **沿用 §3 既定調**（Stewart/Rogawski、warm-not-chatty、clarity-first）。critic 火力 **約 80% 實質/高度、20% §3 那點暖**，**不灌人格**（多作者一致性＋自學者查閱性的考量；中性但言之有物即達標）。voice corpus 換真人範本。
- **Q3 機制：** **LLM-critic gate**（Claude gate-1 ±（可選）Codex gate-2），使用者裁決，**真人範本當 few-shot 錨**以降「LLM 判 AI-ness 的自我參照」風險。
- **Q4 與舊機制：** **取代並收編**——新 critic 取代 metric/tell 的 Dimension C；**Vale 降為免費低優先護欄**（本來就 0 誤砍）。

---

## 2. 判準：Dimension C 改鑄為 S/A/V

沿用現有 prose-audit 的 A（易懂）/B（流暢）/**C** 第三槽，**C 的內容整個換掉**。對每個候選句/段跑三組診斷，**每條 finding 強制附證據**：

**S — Substance（這句掙得它的位置嗎？）**
- **S1 資訊** — 相對前句、相對數學式本身，有沒有加**新洞見**？（只把算式翻成英文卻沒加東西＝空）
- **S2 具體性** — 斷言針對**這個**物件/問題，還是「貼到任何節都成立」的通用填充？
- **S3 刪除測試** — 刪掉讀者有損失嗎？**沒有→建議刪，不是改寫。**

**A — Altitude（對自學者高度對嗎？）**
- **A1 嘮叨** — 顯而易見的步驟被長篇解釋？（過高）
- **A2 跳步** — 真正難的一步被略過/揮手帶過？（過低）
- **高度 self-relative：** A1/A2 對著「**這節在教什麼、這一步本身多難**」判，**不**對著範本判（避免引進別人的教法）。範本只示範「好高度的形狀」。

**V — Voice（§3 那點暖到位嗎？）**
- **V1 平** — 某處只機械陳述、缺了 §3 要的動機/直覺鋪陳？（**不是**叫它灌人格/加笑話——只問「§3 本來就要的那點暖在不在」）

**兩個防呆（避免重蹈 metric/tell 覆轍）：**
1. **真人範本當錨 ＋ 強制附證據** — critic prompt 內掛範本（見 §3）標為「言之有物的真人數學散文」，要它對著這個 bar 判。每條 finding **必附**：問題句＋踩哪個測試（S1/S2/S3/A1/A2/V1）＋一行為什麼＋改寫（或「刪」）。→ 可稽核，不是憑感覺。
2. **中性不扣分** — 純粹平實、中性但言之有物的句子**不准 flag**（那正是目標）。只抓空/錯高度/該暖沒暖。

唯讀、propose-only、**保語意、不動數學、不碰教學順序與選題**（copyedit 級硬護欄，同 A/B 維度）。

---

## 3. 範本錨（exemplars）

- **組成：固定 2 正 ＋ 1 負，錨總量約 400 字（每段 ~1 paragraph）。**
  - **2 正** — register 貼 §3、確定真人、**NOT Ch1**（破循環）。起手建議：OpenStax 極限段＋OpenStax 導數段（最接近 §3「中性但暖、言之有物」）。
  - **1 負** — 刻意空/AI-default 的數學段，標「這種要 flag，這是為什麼」。對「抓壞句」任務，正＋負對比錨比純正面有效；且兼作 §4 盲測素材。
- **固定一組、全節通用**（S/A/V 大多 topic-independent；A 靠 self-relative 判）。**topic-matched 範本只在驗證顯示某些難主題系統性判錯高度時，才針對那些主題局部補**（資料驅動，非一開始逐節換）。
- **正面那 2 段直接當 §3 voice corpus 的真人替換**（撤掉 Task 2.4 放的 Ch1 四段）。一套素材、兩用途。
- **錨組存成 rubric 附錄檔、版控。** 授權 BY-NC-SA，逐段標示來源。
- **⛳ 最終選由使用者 bless**（範本＝那把尺，也是 §3 語聲標靶）。

---

## 4. 機制/流程

- **收編進現有 gate（不另起爐灶）：** 把 `handout-prose-audit` subagent 的 **Dimension C 內容換成 S/A/V**；同一 agent 一次跑 A＋B＋C-recast，prompt 末尾掛固定錨組。契約改在 [`handout/_audit/PROSE-AUDIT-RUBRIC.md`](handout/_audit/PROSE-AUDIT-RUBRIC.md)（單一真相來源，gate-2 Codex 自動繼承）。
- **流程：** gate-1 Claude →（可選）gate-2 Codex → **使用者逐條裁決**（propose-only）→ 套用獲准改寫（保語意/不動數學）→ 回歸審核（CLAUDE.md 2026-06-12）。
- **產出：** standalone HTML 審核稿，比照 [`handout/_audit/REVIEW-ch01-prose-audit-gate1.html`](handout/_audit/REVIEW-ch01-prose-audit-gate1.html)：摘要表＋逐條卡片（踩哪測試＋為什麼＋`<del>/<ins>` 改寫或「刪」）＋穩定編號。
- **Vale 降級：** 留作零成本 pre-flag（預期 ~0），不再是 gate、不進收斂判準。
- **範圍：** 本設計只動 **handout**；video 線（`NARRATION-COPYEDIT-RUBRIC.md`）日後比照，本輪不碰。

---

## 5. 驗證（取代「校準 Ch1」）

舊法錨 Ch1 已廢。新法 = **盲測分離 ＋ 過度-flag 防護 ＋ 使用者抽查 ＋ pilot**：

1. **盲測分離（核心信任檢查）：** 小 benchmark——正例＝vanilla prompt 生的 AI-default 數學段（該被 flag）；負例＝**另一批**真人段（OpenStax/CLP，**與錨組不重複**，防洩漏）。遮標籤跑 critic，看它對 AI 段的 S/A findings 是否明顯多於真人段。**分不開＝critic 是噪音 → 先改 rubric/錨再信它。**
2. **過度-flag 防護：** 量真人負例上的誤報率；若把一堆真人句也 flag → 太兇，收緊「中性不扣分」。
3. **使用者抽查：** 挑 1–2 節真實講義，比對 critic findings 與使用者讀感；常不同步就重調。
4. **pilot 再鋪：** 驗證過的 critic 先跑**一節**，看順了再鋪 Ch1–4。

**驗證結果（2026-06-26，已執行）：**
- **盲測分離 PASS：** empty vs substantive **29.7× 分離**、blocking-only **完美分離**（11 段實質散文——真人＋好 AI＋bare vanilla——零 blocking；3 段刻意空泛全被 blocking 重咬、踩對 S1/S3/A2/V1）。過度-flag 防護成立。
- **軸的修正：** §5.1 原框「正例＝AI 段、負例＝真人段」假設「AI＝該 flag」。實測推翻：vanilla LLM 在 limit/derivative 這類好走主題上**本身言之有物、與真人不可分**（實證 §0「中性≠AI」）。故可驗證、critic 真能分的軸是 **「空 vs 實」**，不是「AI vs 人」——本 critic 驗的是**空泛偵測＋過度-flag 防護**（正是 §6 Task 8 的職責），不是「AI 偵測」。
- **pilot＋Ch1：** §1.4 pilot 通過；Ch1 六節經 **gate-1（Claude）＋gate-2（Codex）雙審皆 0 blocking**，推翻舊 metric「Ch1 是 AI 灌水」。實作細節與逐節結果見 [`PLAN-deai-semantic-critic-implementation.md`](PLAN-deai-semantic-critic-implementation.md)「實作進度與結果」。

---

## 6. Scope／退役／連帶

- **退役：** C6 em-dash 密度、≥3/500 高密度叢集機制、Ch1 校準門檻（⛳#1 的 em-dash 線作廢）。
- **替換：** Task 2.4 §3 那四段 Ch1 範文 → 2 段真人正面範本。
- **保留：** Vale（降級）、§3 語域規範、propose-only/HTML/回歸那套機器、授權框架。
- **Ch1 入清掃範圍**（⛳#1「Ch1 不動」由使用者主動重開）。
- **video** 線日後比照，本輪不碰。

---

## 7. 護欄（不變的硬約束）

- **絕不**用 AI-detector 機率分數當 gate（非母語偽陽、可 paraphrase 規避）。
- 自動 lint（Vale）**永遠** flag-only；決定性「擋」只在人審 ＋ 使用者裁決。
- critic **保語意、不動數學、不碰教學順序與選題**（copyedit 級）。
- 語料只用 **BY／BY-NC／BY-NC-SA** 家族，逐段標示（同 `problem_banks` 授權紅線；排除 BY-SA 如 Active Calculus）。

---

## 8. 落地步驟（高層；逐 task 細節留給 implementation plan）

1. **定錨組**（2 正 1 負）→ ⛳ 使用者 bless。
2. **改鑄** `PROSE-AUDIT-RUBRIC.md` 的 Dimension C 為 S/A/V（＋錨附錄檔）。
3. **建盲測 benchmark ＋ 跑分離測試**（驗 critic 真能分人/AI；不過關先迭代）。
4. **pilot 一節**（使用者看順）。
5. **鋪 Ch1–4**（逐節 propose-only，逐 ⛳ 裁決，回歸審核）。
6. **退役舊機制 ＋ 換 §3 voice corpus 為真人**。
7. **更新 `PLAN-deai-flavor*`**（標 superseded，指向本檔）。

---

## 附：本 pivot 取代/影響的既有文檔（待使用者裁決刪/標 superseded）

| 文檔 | 處置建議 |
|---|---|
| `PLAN-deai-flavor.md`／`-implementation.md` | **標 superseded**、指向本檔（保留決策史，勿刪） |
| `REPORT-deai-ch1-calibration.md`＋對應 HTML | **標 superseded**（它是「為什麼 pivot」的證據，建議留） |
| `REVIEW-deai-voicecorpus-candidates/applied.html` | 真正過時（Ch1 voice corpus）→ 可刪或標 superseded |
| `REVIEW-ch02-deai-gate1.html`（本輪、未 commit） | 用舊 metric C；A/B findings 仍有效 → 留 A/B、退 C 部分 |
| `CONTENT_SPEC.md §3`（未 commit）/`CONTENT_DIRECTION.md ⑤`（未 commit） | §3 改真人範本；⑤ Vale 改標「降級護欄」 |
