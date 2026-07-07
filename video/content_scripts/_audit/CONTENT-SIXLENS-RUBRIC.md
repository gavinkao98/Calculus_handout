# 內容稿六鏡稽核 — 維度與收斂線（CONTENT-SIXLENS-RUBRIC）

> 本檔是「Stage-1 內容稿六鏡稽核（six-lens content audit）」的契約與**單一真相來源**。六鏡在**撰稿 DRAFT 階段**跑（內容稿成形、鎖稿前），是產線**最前面**的判斷閘。維度／收斂線**只在這裡改一次**。
>
> **被審物：** 一節的內容稿 [`content_scripts/<deck>.md`](.)（純內容中間產物：`id`／`source`／`learning_goal`／`kind`／`narration`／`visual_need`／`animation_cue`）＋ 其權威來源講義 fragment。**規範權威**見 [`../../CONTENT_METHODOLOGY.md`](../../CONTENT_METHODOLOGY.md)（§1 核心理念與硬規則、§2 scope、§3 拆解、§4 narration/register、§5 視覺、§7 品質檢核）；本檔只定「審哪六鏡、哪些擋稿、哪些不算 finding、怎麼回報、怎麼跑」，**不重述**方法論。
>
> **與另一套「lens」分清楚：** 本檔是**內容稿**的**六**鏡（layer 2）。`review_pack.py` 的**四**鏡（忠實／語域／拆解／**工程**）審的是 manim hook **code**（layer 5），是不同產物的不同閘，勿混。

## 性質與兩讀者

- 六鏡是**對抗式 multi-agent 稽核**：fan out 六鏡 → 每條 finding 由 Claude **refute-by-default 逐條複驗**（預設「先試圖駁回」，駁不掉才留）。**0-hallucination 為目標**：寧可漏報、不可幻覺出不存在的問題；回報前自查 over-triage。
- **無 Codex gate2。** 六鏡本身已是 multi-agent＋對抗複驗（已有獨立第二意見），**不再疊付費 gate2**（gate2 只保留給單讀者的 copyedit／NFA，見 [`NARRATION-FAITHFULNESS-RUBRIC.md`](NARRATION-FAITHFULNESS-RUBRIC.md)）。
- **唯讀、propose-not-act**：只回報、不改內容稿，findings 交回使用者裁決。

## 六鏡（L1–L6；每條標 Blocking / Advisory）

**L1 — 忠實 Faithful to handout.** 數學內容與範圍跟著講義這一節：不漏環境、不加入新的數學、不脫離、不牴觸；每個承載數學的單元 **MUST** 可回溯到講義某環境／手寫編號（`source` 欄）。**呈現**的重排與增補（場景順序為教學重排、加 intro/outro 與把散文幾何主張變視覺單元）是 §1/§3 允許的，**不算** finding。**L1 scaffold 例外：** 標記為 `scaffold` 的短文字若只把「已用到的目的／記號／慣例／定義域／前提」講白，**不算** L1「加入講義沒有的數學」；但須 cite locus、**不得**引入新定理／例題／結果、**不得**改條件。**Blocking：** 漏掉必納環境、加入講義沒有的數學、與講義牴觸、或數學單元無法回溯（§7：違反則 stage-2 前出局）。

**L2 — 拆解 Decomposition.** 環境→教學單元 `kind` 對應正確（§3 對應表）；**一單元一個教學重點**；環境之間的散文都歸類處理（Incorporative／Bridge／Forward-pointing）、**無 silent drop**。**Blocking：** 兩個教學重點塞進一個單元而拖累教學、或承載教學的散文被默默丟掉。輕微的 kind 選擇或順序偏好 → advisory。

**L3 — 語域 Register.** 對齊 [`../../CONTENT_METHODOLOGY.md`](../../CONTENT_METHODOLOGY.md) §4 的**口語標準**——影片刻意比講義口語（縮寫放行、引導語可用、守 lecture 底線：不俚俗、不用會讓數學失準的 hedge）。**審的是本節的口語標準、不是講義的正式度。** 多為 **Advisory**（polish）；只有當語域問題會誤導理解時才 blocking。

**L4 — 不重複 No-repeat.** 套 §4 repeat-pattern：兩個以上**同型**例子，第二個起省掉第一個已建立的 setup；跨單元不無謂重述同一鋪陳。**topic-term 自然反覆**（該節就在講那個概念）**不算** finding；刻意的教學 echo／recap 也不算。**Advisory。**

**L5 — 數學正確 Math correctness（HIGH PRIORITY）.** **獨立重算**每個 example 的每個數值、正負號、區間端點、象限、最終結果，確認與數學相符。**這一鏡必須隔離／盲算**（給底層數學、不先讀內容稿的結論，防 anchoring；同 [`NARRATION-FAITHFULNESS-RUBRIC.md`](NARRATION-FAITHFULNESS-RUBRIC.md) 的 D7 隔離 reader）。**Blocking：** 任何算錯（教錯數學）。**0-hallucination**：只報真能重算出的不符，不臆測。

**L6 — 完整 Completeness.** 套 §7 作者 checklist／§2 代表式涵蓋：每個 `definition`／`theorem`／`proposition` 有單元覆蓋；每個**不同模式**的 `example` 有代表單元，折疊掉的同型重複**就近註明**（MUST NOT silent drop）；**無 `exercise` 內容洩入**；intro／outro 齊備（intro 有定位＋tagline、recap 有 takeaway、outro 無 takeaways）；散文裡的幾何主張都有視覺單元（或就近註明刻意略過）；symbol-heavy 節套 §5 例外。**Blocking：** 漏掉必納的 def／thm／example 模式、習題外洩、缺 intro／outro（§7 是定稿前 blocking 閘）。

## 收斂線

- **收斂判準**：六鏡通過 ＝ **blocking findings（L1／L5／L6 的 blocking 類，及 L2 拖累教學者）== 0**。advisory（L3／L4 與輕微 L2）由使用者逐條裁決，**不強制歸零**。
- 六鏡在 DRAFT 階段收斂後，內容稿才進旁白 sign-off → lock（之後才是 LOCKED 階段的 NFA）。

## 不算 finding（別誤報）

- **呈現的重排與增補**（§1/§3 允許）：場景順序為教學重排、加 intro／outro、把散文幾何主張做成視覺單元——**是呈現、不是內容**，不算不忠實。
- **topic-term 自然反覆**、刻意的教學 echo／recap、§3 鼓勵的連接詞（*Notice that*、*Let us now*…）。
- **刻意折疊的同型第二例**（已就近註明者）。
- 語義等價的用詞差異；服務清晰度的「囉嗦」（§4 clarity > compactness）。
- **幻覺**：重算不出來、講義裡找不到依據的「問題」——**寧缺勿報**（0-hallucination）。

## 回報規格

四級，只報 tier 1–2（① 真錯／忠實破口／數學錯／完整性缺口 ② 轉換或拆解引入的真缺陷），tier 3（taste／register drift）至多一行，tier 4 略。**回報走 raw→actionable**（把原始觀察收斂成可執行建議）、**查過度 triage**、**不 over-report**；**乾淨的鏡是有效結果**。

**輸出格式（最終訊息；不寫任何檔案）：**

- 首行：`VERDICT: <X> blocking, <Y> advisory`
- 逐條：`- [Blocking|Advisory] [L#] unit-id — issue（引用原文／locus）→ 建議`
- 每個乾淨鏡一行（如 `L4 不重複: clean`）。
- 末行：對「**blocking 是否歸零**」給明確結論。

**交付給使用者裁決時**：依 [`../../../CLAUDE.md`](../../../CLAUDE.md) 交付規則產 standalone HTML 審核稿、finding 標穩定編號。純版控紀錄（如本 rubric、`REPORT-*.md`）不在 HTML 之限。
