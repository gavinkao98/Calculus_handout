# 擴寫方向準則（Expansion Direction Rule）—— 從手稿到一節的「方向層」

> **狀態：v0.1 draft，2026-06-03，分支 `experiment/seed-converge`。設計稿，未經實機測試。**
> 一句話定位：在「老師掃描手稿 → 完整講義一節」之間補上**方向層**，讓「**這是不是我要的方向**」從不可檢核變可檢核。
>
> **適用範圍：** 每節、每章同一套，治理講義內容的擴寫。**不碰** `chapters/*.tex`、**不碰** pipeline、未測前**不進**正式流程。
>
> **與既有文件的關係（引用、不複述）：**
> - [`../../README.md`](../../README.md) §撰稿工作流程 —— Mode A/B/C、`% expansion:` 標記與類別、具名內容政策、密度校準、擴增稽核。本準則**保留**這些零件，只在頂層改寫流程敘事（見 §4）。
> - [`../../CONTENT_SPEC.md`](../../CONTENT_SPEC.md) —— 排版、環境集、顯示模式、記號（HOW to write，權威）。
> - [`../../CONTENT_ROADMAP.md`](../../CONTENT_ROADMAP.md) —— 章節弧、每章 core skills、key figures。**本流程的 macro 北極星**：每節 brief 以對應章條目為輸入並保持一致、方向叉路回填其「Open questions」（見 §3.5）。
> - [`../seed_converge/SYNTHESIS.md`](../seed_converge/SYNTHESIS.md) —— 實驗教訓（advisory 迴圈、blocking/advisory 分流、訂閱、圖 critic），本準則**折入**。
> - [`../seed_converge/PLAN_codex_subscription_loop.md`](../seed_converge/PLAN_codex_subscription_loop.md) —— **流程 ⑤「advisory 審查迴圈」的具體實作**：Codex CLI 走訂閱、唯讀 reviewer、`codex exec`／`--output-schema`、single-writer 紀律、配額 caveat。本準則的 ⑤ **即此 PLAN**，外加 `direction-conformance` 檢查。

---

## 0. 它解決什麼問題

**起點：** 有些老師的手稿太簡略，撐不起教科書密度的例子——想補例題、補有趣的應用。

**為什麼不直接用舊 Mode A：** Mode A **本來就能補**（`% expansion:example`／`application`、密度校準「拿不準時傾向更多擴充」、擴增稽核第 3 項「每技巧 ≥1 補充 workedexample」）。但 Mode A 的稽核只查**完整度／密度／合規**，**不查方向**。一節可以拿稽核 8/8、數學全對，**仍然是「往錯方向收斂得很精緻」**。`seed_converge` 的實證正是如此：迴圈 8/8 覆蓋、0 幻覺，卻和人寫版做了**相反的圖選擇**、漏掉證明與例子——這些都不是 error，是**方向**，沒有任何 auditor 抓得到。

**兩軸拆解（避免把兩件獨立的事綁成一個「新 vs 舊」選擇）：**

| 軸 | 選項 | 本準則採用 |
|---|---|---|
| **軸一 擴寫自由度** | 手稿當「數學主軸」(wrap-around) ↔ 當「可自由改寫的種子」 | **hybrid：手稿是數學主軸，加法旋鈕轉大。** 新的具名結果／歷史／微妙證明一律人工查核。 |
| **軸二 審查自動化** | 人單獨審 ↔ 模型 advisory 迴圈 | **advisory 迴圈 ＋ 人在閘**（折入實驗驗過的契約）。 |

> 把手稿降為「可自由改寫的種子」是比「補例題」更大、也更危險的改動（放大幻覺風險，且核心幻覺假說尚未壓測）。而你要補的例題／應用是**低幻覺的加法**——不管手稿是主軸或種子都一樣安全。所以**種子化沒換到對應好處，卻付了風險**；本準則不採用。

**核心機制：** 把實驗已驗過的「**模型提案、人定奪**」契約，套到「**方向**」層，而且**前置到擴寫之前**——
Claude 先從手稿提一份**方向 brief** → **你核可**（方向在此由人定死）→ 才擴寫 → 審查時對照 brief 查「**方向符合度**」。
這就是讓「是不是我要的方向」可檢核的全部機關。

---

## 1. 六階 per-section 流程

每節都跑同一套。`★` 是相對實驗版新增的兩處關鍵。

```
① intake 盤點
   掃描手稿 →〔轉錄成文字 seed〕→ 人核對轉錄忠實度（①-verify）→ Claude 出「盤點 ＋ 薄度剖析」
   ↓
② direction proposal 方向提案                         [Claude 提案]
   Claude 依手稿＋薄度＋**該章 ROADMAP 條目**，填「方向 brief」（§2 模板）；薄處提案「補什麼」
   ↓
③ direction gate 方向閘  ★新★                         [人定奪]
   你改／核可 brief ← 方向在此由人定死，先於任何擴寫
   ↓
④ expansion 擴寫
   Claude 朝「已核可方向」寫 §X.tex；手稿數學＝主軸、加法全標 % expansion:
   ↓
⑤ advisory review loop 審查迴圈                        [Codex advisory + Claude 改]
   Codex（訂閱·唯讀）審 → blocking = ｛數學／忠實度／★方向符合度★｝
   格式 house-rule → deterministic linter（advisory、不擋收斂）
   Claude 改 → 再審 → blocking=0（停在一次乾淨 audit）
   ↓
⑥ convergence gate 收斂閘                              [人定奪]
   你最終拍板；格式 nit 交 linter；**resolved 方向叉路回填該章 ROADMAP「Open questions」**
```

**逐階說明：**

- **① intake：** 掃描手稿**先轉錄成文字 seed**〔流程選擇甲〕——這樣「手稿＝數學主軸」就有一份**可 diff 的白紙黑字**，忠實度才查得動。Claude 接著產出盤點與薄度剖析（見 §2 前兩欄）。**產出後先過一道人核對（`①-verify`）：使用者對掃描核對 seed 的數學忠實度，確認才進 ②**——整套「手稿＝數學主軸」的保險，地基就是這份轉錄，轉錯則後面全錯。（校準來源：§4.2 首跑。）
- **② 方向提案：** Claude 把 §2 的 brief 填好，薄的地方提案要補哪些例子／應用。**輸入除了手稿＋薄度，還有該章的 `CONTENT_ROADMAP` 條目**（core skills／key figures／pitfalls／open questions）——讓節層 brief 與章層弧一致，且 brief **引用不複述** ROADMAP（見 §3.5）。
- **③ 方向閘（新）：** 使用者改或核可。**實驗版沒有這一環**——seed→擴寫→審，中間沒有人定方向的關卡，所以迴圈只能查「對不對」、永遠查不到「是不是你要的」。插入 ③ 即補上此缺口。brief 維持**輕量**〔流程選擇丙〕，讓這道人閘快到你願意每節都過。
- **④ 擴寫：** Claude 是**唯一寫手**，朝已核可方向擴寫；手稿數學為主軸，每一處非翻譯的增添都加 `% expansion:` 標記（沿用 README 的類別與政策）。
- **⑤ advisory 審查迴圈：** Codex CLI（走訂閱、唯讀 reviewer）出 findings。**blocking 只留數學／忠實度／方向符合度**〔方向符合度＝blocking，流程選擇乙〕；格式（`% expansion:`／`\index`／register）一律 advisory、交 deterministic linter、**不准擋收斂**。停在**一次乾淨 audit**（別停在未經審核的 revise）。reasoning 模型 run-to-run 會飄 → 重要判斷**多跑取聯集**。（Codex 接法、訂閱認證、`codex exec`／schema、配額 caveat 的**具體實作**見 [`../seed_converge/PLAN_codex_subscription_loop.md`](../seed_converge/PLAN_codex_subscription_loop.md)。）
- **⑥ 收斂閘：** 使用者最終裁決；格式 nit 交 linter。

---

## 2. 方向 brief 模板（每節填、人在 ③ 核可）

輕量、bullet 級、約半頁。每欄：**捕捉什麼** ＋ **決策程序（泛用，怎麼從任一手稿決定它）**。

| 欄位 | 捕捉什麼 | 決策程序（泛用） |
|---|---|---|
| **手稿盤點** | 本節手稿實際有什麼 | 照原順序列出手稿的主題、定義、定理（含證明與否）、worked example、圖、具名結果（人物／日期／命名定理）。 |
| **薄度剖析** | 哪裡撐不起教科書密度 | 對每塊標 **{夠／薄／無}**：「夠」＝已達 Stewart 密度；「薄」＝有骨架但缺動機／例子／圖；「無」＝該有卻完全沒有。可疑／非標準數學標「**請查核**」丟使用者（手稿＝數學主軸，**不靜默改**）。輸出指向「加法該往哪去」。 |
| **範圍與深度** | 本節邊界與嚴謹度 | 只吃手稿那一叢主題、不外擴；後面章節才系統處理的概念用**一行 forward-ref** fence 掉（不 preview-creep）。結構結果決定「**證或只陳述**」：證明**短、標準、具啟發**就補（`expansion:formula`／`example`）；多頁或需未引入材料的證明，標記**待使用者授權**。 |
| **承重直覺** | 最該先講通的那一個直覺 | 找出「**為何天真／直接做法會壞**」的關鍵，用一個**具體碰撞／失敗例**先打臉、再形式化；其次才是「這概念在做什麼」的心像。**一節只挑一個承重直覺領頭**，其餘為它服務。 |
| **worked example 清單** | 例子的選取與順序 | 每技巧 ≥1 例。預設序：**真實情境/具體錨 → 判別/診斷 → 建構/計算 → 驗證/反思**。手稿薄的技巧**慷慨新增**（低風險、`expansion:example`、可刪），清單標出哪些是新增。同型第二例**跳過**已建立 setup。手稿自帶足量例子者不硬加。 |
| **history／application** | 要不要放史／應用、放什麼 | `application` 只在有**忠實的真實實例**時放（非裝飾）；薄手稿寧可開節放**一個強錨**，不散落弱錨。`history` 只在概念有**可考起源／記號故事**時放，且**標來源**（特定來源或 `[source: standard calculus-textbook historical note]`；直接引文必須特定來源，否則改釋義）。兩者皆不自然 → **留白勝過 padding**。 |
| **強調／takeaway** | 讀者該帶走什麼 | 點名**一個概念樞紐**（邏輯支點）＋**一個可攜技能**（學生能帶去別處的操作）。寫進 brief，讓 ④ 朝它寫、⑤ 查它有沒有真的落地。 |
| **刻意不寫** | 本節的「反方向」 | 列出模型在此**會自然手癢多加、但不該加**的東西（forward 主題、岔題、過度推廣、本可省的形式證明），各附一行理由＋它該去哪。**此清單餵給 auditor 當方向符合度的反向檢查**（多寫了不該寫的＝違反方向）。 |
| **篇幅帶** | 體量護欄 | 由主題份量＋簽核深度推一個**軟帶**（行數／頁數區間），**當護欄不當預算**——篇幅是好拆解的結果。明顯超出 → 回頭查是否某塊過度擴寫或漏 fence 的 forward 主題。 |

---

## 3. brief 下游怎麼用

方向 brief 在 ③ 被核可後，是 ④ 與 ⑤ 的契約：

- **④ 朝它寫（drafted-toward）：** Claude 擴寫時以 brief 為方向依據——範圍照「範圍與深度」與「刻意不寫」、例子照「worked example 清單」、史／應用照其觸發決定、敘事重心朝「強調／takeaway」。
- **⑤ 對它審（audited-against）：** 把 brief 連同草稿一起餵給 Codex auditor，新增一個 **blocking 類別 `direction-conformance`**——問：
  - 稿子有沒有覆蓋 brief 指定的例子／直覺／強調？（漏了＝違反方向）
  - 稿子有沒有寫進「刻意不寫」清單裡的東西？（多了＝違反方向）
  - 範圍／深度／篇幅有沒有偏離 brief？

  數學／忠實度仍是 blocking；格式仍 advisory 交 linter。**方向符合度的判準就是 brief 本身**——這正是「是不是我要的方向」變可檢核的所在。

---

## 3.5 ROADMAP ↔ brief：章層大綱與節層方向的接法

`CONTENT_ROADMAP.md` 是方向層的**前身**：它每章條目末尾的 **Open questions** 一直在記 user-directed 的方向裁決（如 Ch4 的「Cauchy⟺convergent 證明＝展開成 Bolzano–Weierstrass」——正是 §4.2 brief 的同一個叉路，只是 brief 這次選了相反的折衷）。方向層不取代它，而是把它在 Open questions 裡做的事**系統化、前置化、每節一份、機器可檢核**。

兩者是同一條「素材 → 結構化計畫 → 實作」鏈上的**粗細兩格**，互補不重疊：

| | 層級 | 內容 |
|---|---|---|
| **ROADMAP 條目** | 章／弧（macro） | 章序、跨章前置、跨章記號線、handout-vs-video、整章 core skills／key figures／pitfalls／**Open questions** |
| **方向 brief** | 節（micro） | 這節從這份手稿往哪長（§2 九欄）＋人閘＋審查契約 |

雙向接法：
- **下行（ROADMAP → brief）：** ② 提 brief 時讀該章條目，節層的承重直覺／強調／圖／caution **對齊**章層 core skills／key figures／pitfalls；brief **引用、不複述**（沿用反炒冷飯原則）。
- **上行（brief → ROADMAP）：** ③ 拍板、⑥ 後，把 resolved 的方向叉路**回填**該章「Open questions」——這本就是 ROADMAP 記決定的用法。

欄位對應（節 brief 的決定，多半是章 ROADMAP 某欄的節層落地）：core skills→強調／takeaway；key figures→圖決定；common pitfalls→caution；notation→記號；prerequisites→範圍／fence；**Open questions→方向叉路**。

## 4. 承接 A/B/C：keep / add / fold

本準則**改進、不打掉** README 的 Mode A/B/C。被取代的只有**頂層的 A/B/C 狀態機敘事**（升級成 §1 的六階流程）；其餘零件全用 reference 沿用、不重寫 README／CONTENT_SPEC。

| 原件 | 處置 |
|---|---|
| **Mode A**（手稿主軸＋`% expansion:` 標記與類別＋密度校準＋擴增稽核） | **保留**；加法旋鈕轉大；由「Claude 決定方向、人事後稽核」改為「**朝已核可方向寫**」。 |
| **Mode B**（四級 triage／committed=authorized／ask-don't-delete／記號飄移當問題不當幻覺） | **保留邏輯**；transport 從「人單獨審」換成 **Codex advisory 迴圈**；新增 `direction-conformance` 檢查。 |
| **Mode C**（簽核後充實、propose-only） | **原樣保留**。 |
| **方向層**（brief ＋ 人方向閘） | **新增**，插在 Mode A 之前（②③）。 |
| 實驗的 **advisory 迴圈／訂閱省錢／圖 critic** | **折入** Mode B 那格（⑤），不丟。 |
| **CONTENT_ROADMAP（章層大綱）** | **保留並升格**為 brief 的 macro 北極星：②的第二輸入＋方向叉路回填其 Open questions（見 §3.5）。 |

**關鍵洞察：** 新方向層其實只是把 Mode A 本來就有的「擴充／重排決定」，從「**Claude 決定、人事後稽核**」改成「**Claude 提案、人事前核可**」——同一批決定，把人的方向決定**往前挪**。這是流程人因的改良，不是規則翻新。

---

## 5. 已知取捨與開放問題

- **核心幻覺假說未壓測（最關鍵）：** §1.1 太簡單（初等、無歷史、無微妙證明），驗不出「兩模型會不會一起替同一個幻覺背書」。要驗須換**高風險節**（具名結果／微妙證明，如 Bolzano–Weierstrass、Cauchy 收斂）。見 `seed_converge/SYNTHESIS.md §4`。
- **丟了「中立第三方評分」那層：** 實驗原讓 Claude 在迴圈外當中立評分；新流程把 Claude 拉進當寫手後，外部裁判只剩「人」。不致命（人本在閘），但可考慮**偶爾請第三模型（如 Gemini）對成稿抽查**，補回外部視角。
- **配額管理：** 訂閱用量上限（per-5h／每週）是硬牆，且 CLI 撞牆後回退 API key 不可靠。per-section 限次、人在收斂閘是唯一可靠防線。別把架構建立在「撞牆無縫切 API」上。
- **首跑已驗（§4.2，詳見 [`test/RESULT_s42.md`](test/RESULT_s42.md)）：** 流程在一個高風險節端到端跑通、收斂到 `blocking=0`，且第二模型抓到一處擴寫引入的過度推廣（正面數據點，**一個樣本**）。仍需**低風險對照節**與**更多高風險節**驗證，通過再把本檔「**畢業**」成頂層正式 doc（如 `CONTENT_DIRECTION.md`）並接上 linter／slash command。
- **工程坑（§4.2 首跑實證）：** 組 ⑤ 的 prompt 時，非 ASCII（中文／Unicode 數學符號）會被 `Get-Content`（ANSI 預設）＋ PowerShell pipe 重編碼成亂碼，auditor 收到糊掉的 seed/brief。修法：`[IO.File]::ReadAllText` 讀 UTF-8 ＋ `cmd /c "codex exec - … < prompt"` 餵原始 bytes ＋ 一道 CJK 護欄。

---

## 6. 下一步（驗收）

1. 挑 2–3 節真手稿，跑完整六階流程（含 ③ 人方向閘、⑤ Codex advisory）。
2. 至少含**一個高風險節**，正面壓測幻覺假說。
3. 驗收門檻：方向 brief 輕到願意每節過；④ 擴寫朝向 brief；⑤ 能 audit→fix→re-audit 到 `blocking=0`、且 `direction-conformance` 真能擋住「漏寫／多寫」。
4. 過了再把本檔畢業成頂層 doc、落工具。
