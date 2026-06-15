# 內容方向準則（Content Direction）—— 從手稿到一節的「方向層」

> **本檔是 HTML 講義「每節內容方向」的權威流程文件。** 它在「老師掃描手稿 → 完整講義一節」之間補上一道**方向層**，讓「**這是不是我要的方向**」從不可檢核變可檢核。已在 ch01 §1.1–§1.2、§4.2、ch02 §2.1–§2.5、ch03 端到端跑過六階並收斂（committed）；逐節驗證紀錄存於 [`authoring/direction_layer/`](authoring/direction_layer/)（`ch01/`、`test/`）。
>
> 一句話定位：六階流程把「**模型提案、人定奪**」的契約，從「對不對」延伸到「**是不是我要的方向**」，並**前置到擴寫之前**。
>
> **適用範圍：** 每節、每章同一套，治理講義內容的擴寫。**不碰** video/ pipeline、**不碰**已凍結的 legacy LaTeX 書（`legacy/tex_handout/chapters/*.tex`）。
>
> **與既有文件的關係（引用、不複述）：**
> - [`README.md`](README.md) §撰稿工作流程 —— Mode A/B/C、expansion 標記與類別、具名內容政策、密度校準、擴增稽核。本準則**保留**這些零件，只在頂層改寫流程敘事（見 §4）。
> - [`CONTENT_SPEC.md`](CONTENT_SPEC.md) —— 排版、環境集、顯示模式、記號（HOW to write，權威）。
> - [`CONTENT_ROADMAP.md`](CONTENT_ROADMAP.md) —— 章節弧、每章 core skills、key figures。**本流程的 macro 北極星**：每節 brief 以對應章條目為輸入並保持一致、方向叉路回填其「Open questions」（見 §3.5）。
> - [`authoring/seed_converge/SYNTHESIS.md`](authoring/seed_converge/SYNTHESIS.md) —— 機制實驗教訓（advisory 迴圈、blocking/advisory 分流、訂閱、圖 critic），本準則**折入**。
> - [`authoring/seed_converge/PLAN_codex_subscription_loop.md`](authoring/seed_converge/PLAN_codex_subscription_loop.md) —— **流程 ⑤「advisory 審查迴圈」的具體實作**：Codex CLI 走訂閱、唯讀 reviewer、`codex exec`／`--output-schema`、single-writer 紀律、配額 caveat。本準則的 ⑤ **即此 PLAN**，外加 `direction-conformance` 檢查。

---

## 0. 它解決什麼問題

**起點：** 有些老師的手稿太簡略，撐不起教科書密度的例子——想補例題、補有趣的應用。

**為什麼不直接用舊 Mode A：** Mode A **本來就能補**（`expansion:example`／`application`、密度校準「拿不準時傾向更多擴充」、擴增稽核第 3 項「每技巧 ≥1 補充 workedexample」）。但 Mode A 的稽核只查**完整度／密度／合規**，**不查方向**。一節可以拿稽核 8/8、數學全對，**仍然是「往錯方向收斂得很精緻」**。`seed_converge` 的實證正是如此：迴圈 8/8 覆蓋、0 幻覺，卻和人寫版做了**相反的圖選擇**、漏掉證明與例子——這些都不是 error，是**方向**，沒有任何 auditor 抓得到。

**兩軸拆解（避免把兩件獨立的事綁成一個「新 vs 舊」選擇）：**

| 軸 | 選項 | 本準則採用 |
|---|---|---|
| **軸一 擴寫自由度** | 手稿當「數學主軸」(wrap-around) ↔ 當「可自由改寫的種子」 | **hybrid：手稿是數學主軸，加法旋鈕轉大。** 新的具名結果／歷史／微妙證明一律人工查核。 |
| **軸二 審查自動化** | 人單獨審 ↔ 模型 advisory 迴圈 | **advisory 迴圈 ＋ 人在閘**（折入實驗驗過的契約）。 |

> 把手稿降為「可自由改寫的種子」是比「補例題」更大、也更危險的改動（放大幻覺風險，且核心幻覺假說壓測樣本仍有限，見 §5）。而你要補的例題／應用是**低幻覺的加法**——不管手稿是主軸或種子都一樣安全。所以**種子化沒換到對應好處，卻付了風險**；本準則不採用。

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
   Claude 朝「已核可方向」寫該節草稿（目前 handout sec-N-M.html）；手稿數學＝主軸、加法全標 expansion: 標記
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
  - **seed 轉錄語法（輕量可讀，2026-06-07 定）：** seed 是給人讀的轉錄（`①-verify` 拿它逐字對掃描），**純文字好讀為第一優先**。數學一律**反引號行內＋Unicode**（`≤ ≥ ≠ ⟺ ⟹ → ∞ √ ± · π θ ε Σ`、上標 `x² xⁿ x⁻¹`、複合次方用 `x^(n−1)`、分數 `a/b`、`lim_{h→0} (…)`），**不要 `$$…$$`／`\[…\]` 顯示區塊、不要 `\frac`／`\quad`／`\text` 等巨集**；複雜到 Unicode 會歧義時才退回**短**的行內 `\(…\)`（用 kit delimiter，絕不用 `$$`）。seed 為**稀疏骨架**：記手稿有的（含其 worked example）但別展開成多步排版——漂亮 KaTeX 留給 ④ 輸出。可疑／非標準數學標 **[請查核]**。風格範本：[`authoring/direction_layer/ch01/seed_s12.md`](authoring/direction_layer/ch01/seed_s12.md)、[`authoring/direction_layer/test/seed_s42.md`](authoring/direction_layer/test/seed_s42.md)。
- **② 方向提案：** Claude 把 §2 的 brief 填好，薄的地方提案要補哪些例子／應用。**輸入除了手稿＋薄度，還有該章的 `CONTENT_ROADMAP` 條目**（core skills／key figures／pitfalls／open questions）——讓節層 brief 與章層弧一致，且 brief **引用不複述** ROADMAP（見 §3.5）。
- **③ 方向閘（新）：** 使用者改或核可。**實驗版沒有這一環**——seed→擴寫→審，中間沒有人定方向的關卡，所以迴圈只能查「對不對」、永遠查不到「是不是你要的」。插入 ③ 即補上此缺口。brief 維持**輕量**〔流程選擇丙〕，讓這道人閘快到你願意每節都過。
- **④ 擴寫：** Claude 是**唯一寫手**，朝已核可方向擴寫；手稿數學為主軸，每一處非翻譯的增添都加 expansion 標記（沿用 README 的類別與政策）。HTML 講義的標記語法是 HTML 註解 `<!-- expansion:<cat> … -->`（LaTeX 的 `% expansion:` 只存在於 legacy），類別與 `[pass:]`／`[source:]` 規則不變。
- **⑤ advisory 審查迴圈：** Codex CLI（走訂閱、唯讀 reviewer）出 findings。**blocking 只留數學／忠實度／方向符合度**〔方向符合度＝blocking，流程選擇乙〕；格式（`<!-- expansion: -->`／register 等 HTML house rule）一律 advisory、交 deterministic linter、**不准擋收斂**。停在**一次乾淨 audit**（別停在未經審核的 revise）。reasoning 模型 run-to-run 會飄 → 重要判斷**多跑取聯集**。（Codex 接法、訂閱認證、`codex exec`／schema、配額 caveat 的**具體實作**見 [`authoring/seed_converge/PLAN_codex_subscription_loop.md`](authoring/seed_converge/PLAN_codex_subscription_loop.md)。）
- **⑥ 收斂閘：** 使用者最終裁決；格式 nit 交 linter。

---

## 1.5 跨 session 操作：per-chapter 編排檔（PLAN ＋ kickoff）

§1 講「**一節**怎麼跑」；本節講「**一整章、跨多個 session 怎麼編排著跑**」。實證沿用：ch01 §1.1–§1.2、ch02 §2.1–§2.5、ch03（全套範本）。

**工作模型：** 每節各開一個**新 session**（fresh context、無前對話記憶）。Claude 是**唯一寫手**（single-writer）；使用者只在三道人閘介入：`①-verify`（seed 忠實度）、`③`（方向閘）、`⑥`（收斂閘）。新 session 靠下列**版控編排檔**自帶脈絡、不靠對話記憶——這正是 root [`CLAUDE.md`](CLAUDE.md)「跨對話知識寫進會 git 的文檔、不寫本地 memory」的落地。

**每章兩類編排檔**（住在 [`handout/_dev-archive/`](handout/_dev-archive/) 的 `chNN/`；輸出目前走 handout HTML，但本編排與輸出格式無關）：

| 檔 | 是什麼 | 誰讀 |
|---|---|---|
| `PLAN-chNN.md` | **章層方向錨＋跨 session 狀態**：手稿↔ROADMAP 對應、逐節範圍、章層方向決策（提案、待各節 ③）、**編號 ledger**、章基礎建設、工程坑、逐節狀態表 | 每個新 session **第一個讀** |
| `PROMPT-sNM-kickoff.md` | **每節一份的 bootstrap 提示詞**，整段貼進新 session 即自帶脈絡：讀檔清單（首為 PLAN）、該節從第幾階起、編號接續、內容範圍、章層決策提醒、題目政策、渲染、⑤ Codex、硬約束、起手 | 該節的新 session（使用者貼上） |

**章層 intake（一次性、先於逐節）：** 手稿的**自有分節未必 = ROADMAP 分節**。開章先做一次「**手稿 → ROADMAP §X.M 對應**」寫進 PLAN：哪段去哪節、哪段已在別章（只 cross-ref、不重寫）、哪段在 Homework（待升格 worked example）。（ch03 即典型：手稿把 product rule 重證了一遍（已是 Ch2 §2.5）、tan′ 藏在 Homework、應用置於證明之前——照手稿頁序直切就會重複／漏接。）

**該節從第幾階起：** seed 已轉錄（如 ch03 §3.1）→ kickoff 從 `②` 起；seed 未轉錄 → 從 `①` intake 起（kickoff 內含「讀手稿 pp.X–Y → seed → `①-verify`」）。

**編號跨 session 交接（kit 無 auto-counter，最大風險點）：** 章內每型獨立 counter、跨節連續（Theorem 3.1, 3.2…）。後節 session **讀前節成品 HTML 末尾**確認各型 counter 用到哪、再續編；實際號回填 PLAN 的 ledger 表。交叉引用一律純文字，寫完**自查每個引用都對得到一個存在的 `env-num`**。

**新章怎麼起：** 抄 ch02／ch03 範本，改章號／節號／ROADMAP 行號／手稿頁範圍即可——
- master kickoff 範本：[`handout/_dev-archive/ch02/PROMPT-ch02-kickoff.md`](handout/_dev-archive/ch02/PROMPT-ch02-kickoff.md)（明示「ch03/ch04 換章號即可重用」）；
- per-section 範本：`handout/_dev-archive/ch02/PROMPT-s2*-kickoff.md`；含 PLAN 的全套範本：`handout/_dev-archive/ch03/PLAN-ch03.md` ＋ `PROMPT-s3*-kickoff.md`。
> 註：上述 `_dev-archive/` 編排檔為歷史開發紀錄，內含的相對路徑可能過時（見該資料夾的 README）；以本檔的六階流程敘事為準。

---

## 2. 方向 brief 模板（每節填、人在 ③ 核可）

輕量、bullet 級、約半頁。每欄：**捕捉什麼** ＋ **決策程序（泛用，怎麼從任一手稿決定它）**。

| 欄位 | 捕捉什麼 | 決策程序（泛用） |
|---|---|---|
| **手稿盤點** | 本節手稿實際有什麼 | 照原順序列出手稿的主題、定義、定理（含證明與否）、worked example、圖、具名結果（人物／日期／命名定理）。 |
| **薄度剖析** | 哪裡撐不起教科書密度 | 對每塊標 **{夠／薄／無}**：「夠」＝已達 Stewart 密度；「薄」＝有骨架但缺動機／例子／圖；「無」＝該有卻完全沒有。可疑／非標準數學標「**請查核**」丟使用者（手稿＝數學主軸，**不靜默改**）。輸出指向「加法該往哪去」。 |
| **範圍與深度** | 本節邊界與嚴謹度 | 只吃手稿那一叢主題、不外擴；後面章節才系統處理的概念用**一行 forward-ref** fence 掉（不 preview-creep）。結構結果決定「**證或只陳述**」：證明**短、標準、具啟發**就補（`expansion:formula`／`example`）；多頁或需未引入材料的證明，標記**待使用者授權**。 |
| **承重直覺** | 最該先講通的那一個直覺 | 找出「**為何天真／直接做法會壞**」的關鍵，用一個**具體碰撞／失敗例**先打臉、再形式化；其次才是「這概念在做什麼」的心像。**一節只挑一個承重直覺領頭**，其餘為它服務。 |
| **worked example 清單** | 例子的選取與順序 | 每技巧 ≥1 例。預設序：**真實情境/具體錨 → 判別/診斷 → 建構/計算 → 驗證/反思**。手稿薄的技巧**慷慨新增**（低風險、`expansion:example`、可刪），清單標出哪些是新增。同型第二例**跳過**已建立 setup。手稿自帶足量例子者不硬加。<br>**自創題政策（使用者 2026-06-07 定）：** 可自創新題，但 (1) 須經**使用者批准**、(2) 題型須與既有 example **不同**（非換數字／係數的同型題）、(3) 一律寫成 **worked example**（含 solution＋講解），不產 bare your-turn exercise。理由：bare 自創習題受 root [`README.md`](README.md) §防護欄「自創習題——習題庫來自手稿」所禁、設計 deferred（[`CONTENT_SPEC.md`](CONTENT_SPEC.md) §14）；但含解的 worked example 屬闡述（Mode A），不在此限。 |
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
| **Mode A**（手稿主軸＋expansion 標記與類別＋密度校準＋擴增稽核） | **保留**；加法旋鈕轉大；由「Claude 決定方向、人事後稽核」改為「**朝已核可方向寫**」。 |
| **Mode B**（四級 triage／committed=authorized／ask-don't-delete／記號飄移當問題不當幻覺） | **保留邏輯**；transport 從「人單獨審」換成 **Codex advisory 迴圈**；新增 `direction-conformance` 檢查。 |
| **Mode C**（簽核後充實、propose-only） | **原樣保留**。 |
| **方向層**（brief ＋ 人方向閘） | **新增**，插在 Mode A 之前（②③）。 |
| 實驗的 **advisory 迴圈／訂閱省錢／圖 critic** | **折入** Mode B 那格（⑤），不丟。 |
| **CONTENT_ROADMAP（章層大綱）** | **保留並升格**為 brief 的 macro 北極星：②的第二輸入＋方向叉路回填其 Open questions（見 §3.5）。 |

**關鍵洞察：** 新方向層其實只是把 Mode A 本來就有的「擴充／重排決定」，從「**Claude 決定、人事後稽核**」改成「**Claude 提案、人事前核可**」——同一批決定，把人的方向決定**往前挪**。這是流程人因的改良，不是規則翻新。

---

## 5. 已知取捨與開放問題

- **核心幻覺假說：樣本仍少（最關鍵 open question）：** 「兩模型會不會一起替同一個幻覺背書」尚未在最硬的具名結果上窮盡。已跑的高風險節（§4.2 eˣ 連續＋指數律、ch02 §2.3 首個定理＋證明）中 auditor 都抓到真問題、**未見幻覺穿過**——正面但**樣本有限**的證據。仍待更多高風險節（如 Ch4 Bolzano–Weierstrass、Cauchy 收斂）持續壓測。見 [`authoring/seed_converge/SYNTHESIS.md`](authoring/seed_converge/SYNTHESIS.md) §4。
- **丟了「中立第三方評分」那層：** 實驗原讓 Claude 在迴圈外當中立評分；本流程把 Claude 拉進當寫手後，外部裁判只剩「人」。不致命（人本在閘），但可考慮**偶爾請第三模型（如 Gemini）對成稿抽查**，補回外部視角。
- **配額管理：** 訂閱用量上限（per-5h／每週）是硬牆，且 CLI 撞牆後回退 API key 不可靠。per-section 限次、人在收斂閘是唯一可靠防線。別把架構建立在「撞牆無縫切 API」上。
- **多節端到端驗證紀錄（詳見 [`authoring/direction_layer/ch01/RESULT_ch01.md`](authoring/direction_layer/ch01/RESULT_ch01.md)、[`authoring/direction_layer/test/RESULT_s42.md`](authoring/direction_layer/test/RESULT_s42.md)、[`handout/_dev-archive/ch02/`](handout/_dev-archive/ch02/)）：** ch01 §1.1（低風險對照節）、§1.2（中風險，direction-conformance 抓到一個真 blocking＝漏畫 brief 指定的圖）、§4.2（高風險，第二模型抓到一處擴寫引入的過度推廣）、ch02 §2.1–§2.5（全數收斂 `blocking=0`）皆跑完六階。
- **工程坑（§4.2 首跑實證）：** 組 ⑤ 的 prompt 時，非 ASCII（中文／Unicode 數學符號）會被 `Get-Content`（ANSI 預設）＋ PowerShell pipe 重編碼成亂碼，auditor 收到糊掉的 seed/brief。修法：`[IO.File]::ReadAllText` 讀 UTF-8 ＋ `cmd /c "codex exec - … < prompt"` 餵原始 bytes ＋ 一道 CJK 護欄。

---

## 6. 狀態與可選後續

本準則**已畢業為頂層正式文件（即本檔）**，是 HTML 講義每節內容方向的權威流程。驗收門檻 1–3 已達，憑 ch01 §1.1–§1.2、§4.2、ch02 §2.1–§2.5 的端到端跑（committed）：

1. ✅ 已跑 7 節真手稿的完整六階（含 ③ 人方向閘、⑤ Codex advisory）。
2. ✅ 含高風險節（§4.2、ch02 §2.3 首個定理＋證明）正面壓測幻覺假說——auditor 抓到真問題、未見幻覺穿過（樣本仍少，見 §5）。
3. ✅ 方向 brief 輕到每節都過；④ 擴寫朝向 brief；⑤ audit→fix→re-audit 收斂到 `blocking=0`；`direction-conformance` 擋下過真 blocking（§1.2 漏圖）。

**可選後續（尚未做、非阻塞）：** 把 ⑤ 的格式 house-rule 落成 deterministic linter，以及把整套流程包成 `/audit-section` 之類的 slash-command，讓每節跑得更省手。在那之前，本流程以本檔為準、人工照六階執行。
