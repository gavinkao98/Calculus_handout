# 講義數學正確性稽核 — RUBRIC（math-correctness audit）

> **本審契約（單一真相來源）。** 審「**教什麼、對不對**」——課文散文／定義／定理／推導裡的數學是否成立。這正是散文稽核（怎麼寫、讀者跟不跟得上）與圖稽核（畫得對不對）都**明文排除**的那一塊。
>
> **目前的消費者：** Mode B 主審（Claude 主流程直接走查，見 [`../../../CONTENT_AUTHORING_WORKFLOW.md`](../../../CONTENT_AUTHORING_WORKFLOW.md) §Mode B「其他 Mode B 發現 §數學正確性」）＋ 定稿前的 **Codex 獨立複核**（吃配額、先徵同意）。**本檔刻意先於 subagent 落地**：維度／擋稿線在這裡定一次，未來若要把 gate 1 包成 `handout-math-audit` 唯讀 subagent，直接引本檔即可，不必另立規則（比照 `handout-prose-audit`／`handout-figure-audit` 與其 rubric 的關係）。
>
> **被審物：** 講義單節 fragment（`handout/html/fragments/ch{NN}/sec-*.html`）的數學內容，並對照該節的**手稿**。
>
> **依據：** [`../../../CONTENT_AUTHORING_WORKFLOW.md`](../../../CONTENT_AUTHORING_WORKFLOW.md) §Mode B（「數學正確性」發現用 *「請查核 X」* 框架；§238 數學內容**以手稿為準**）＋ [`../../../CONTENT_SPEC.md`](../../../CONTENT_SPEC.md) §5（proof 為選用、預設省略）／§7（公式呈現）／§9（記號）／§15（最終一致性檢查）。本檔只定「審哪些維度、哪些擋稿、哪些不算 finding、怎麼回報」，**不重述**那些規範本身。
>
> **性質：** 唯讀、blocking＋advisory 分流、**一律提議不行動**——findings 用 *「請查核 X」* 框架交使用者裁決，**不自行改、不自行刪**。

## 審查對象與邊界

- **審**：`definition`／`theorem`／命題陳述、`workedexample` 的 `solution` 推導步驟、以及散文中的數學主張——其**數學是否成立**。math 公式既是被審物，也對照手稿判定。
- **不審**（各有其 audit，避免雙審）：
  - 散文「怎麼寫、讀者跟不跟得上」→ [`PROSE-AUDIT-RUBRIC.md`](PROSE-AUDIT-RUBRIC.md)（U／F 維度）。本審只問「對不對」，**不評措辭**。
  - **圖內**座標／數值正確性 → [`FIGURE-AUDIT-RUBRIC.md`](FIGURE-AUDIT-RUBRIC.md) 的 **D6**。本審不重看圖裡的數；但若某數學**陳述**寫在 `figcaption`／散文（如 caption 宣稱的定理對不對），仍屬本審。
  - 編號／cross-reference／排版／index → §15 lint 與其他 audit。

## 維度（M1–M8；每條標 Blocking / Advisory）

**A. 陳述正確（定義／定理本身對不對）**

- **M1 定義正確性** — definition 在數學上正確且**完整**：量詞與條件齊備、無遺漏前提或定義域限制。例：continuity at $a$ 需 $a$ 在定義域內且 $\lim_{x\to a} f = f(a)$；極限的 ε-δ 定義需 $0<|x-a|<\delta$（漏掉 $0<$ 會把 $a$ 點本身也算進去）；可微定義需差商極限存在。**遺漏條件使定義變寬／變窄 → Blocking**。
- **M2 定理／命題陳述正確性** — 假設充分且如實、結論正確、無漏掉或多餘的 hypothesis。例：MVT 需 $[a,b]$ 上連續**且** $(a,b)$ 上可微；極限四則運算律需各分項極限**存在**；「可微 ⇒ 連續」非其逆。**漏假設使定理變偽，或多餘假設弱化到與課文用法不符 → Blocking**。
- **M3 量詞與邏輯結構** — $\forall$／$\exists$ 的順序與作用域、必要 vs 充分、`iff` 是否真雙向、逆命題／逆否命題未混用。例：「for all $\varepsilon>0$ there exists $\delta>0$」不可倒序；把「若 $A$ 則 $B$」當「若 $B$ 則 $A$」用。**邏輯結構錯 → Blocking**。

**B. 推演正確（算出來對不對）**

- **M4 推導／計算步驟** — 每一代數／微積分步驟成立：無正負號錯、無非法約分、無對可能為零的量除、規則套用正確（chain rule、換元、極限律），且 worked example 的**最終答案正確**。**步驟或答案錯 → Blocking**。
- **M5 邊界條件／定義域／特例** — 定義域限制（$\tan$ 的定義域、$\ln x$ 需 $x>0$、分母 $\neq 0$）、端點與單／雙側、可去 vs 本質、$x\to 0$ 等特例是否處理。把僅在「幾乎所有 $x$」成立的式子寫成「for all $x$」。**遺漏使陳述變偽 → Blocking；未明說但在該節語境下為真的限制 → Advisory**（建議補一句，不擋稿）。

**C. 一致與完備（跟自己、跟手稿、跟全書一致嗎）**

- **M6 記號一致性（§9／手稿）** — 同一物件在節內與跨節記號一致、符合 §9 canonical list；某符號定義後不被悄悄改義。**與手稿的記號差異一律當 *「請查核：是有意升級還是該對齊回手稿」* 的問題提出，不自行判錯**（README §203／§238）。**造成真歧義／誤讀 → Blocking；單純風格 drift、不致誤解 → Advisory**。
- **M7 跨陳述／跨節一致** — 同一結果在兩處陳述是否相符、後節引用前節結果是否落在其陳述的假設內、同一數值／公式兩處是否一致。**真矛盾 → Blocking**。
- **M8 隱性假設未揭示** — 某主張倚賴一個**未陳明、且在書中此處尚不可用**的前提（如尚未引入連續性就拿來用、默默假設可微）。與 prose `U4`（術語先用後定義，**讀者**跟不上）區別：M8 是**數學健全性**——前提缺位使主張不成立，而非可讀性。**使主張不健全 → Blocking；前提為真但該明說 → Advisory**。（純排序／可讀性版歸 prose `U4`；若其修法是**搬動定義／介紹段**的結構性 reorder，最便宜在 Mode A 方向層攔、別等晚期 cascade 編號——見 [`../../CONTENT_DIRECTION.md`](../../../CONTENT_DIRECTION.md) §2。）

## 擋稿線（blocking vs advisory）

- **BLOCKING（造成偽陳述、不健全推理或錯答案）**：`M1`、`M2`、`M3`、`M4`；`M5`／`M6`／`M7`／`M8` 中「使陳述變偽或自相矛盾」者。
- **ADVISORY（為真但可改善／一致性 polish／該補的提醒）**：`M5` 未明說但為真的限制、`M6` 不致誤解的 drift、`M8` 前提為真但該明說、以及任何「建議補一句使其更嚴謹」。
- **收斂判準**：該節 math gate 通過 = **blocking math findings = 0**。advisory 由使用者逐條裁決，**不強制歸零**。

## 不算 finding（math-content-protected；別誤砍）

數學稽核**最易誤報**——下列是**特性或編輯選擇**，不是缺陷，絕不可當 finding：

- **手稿刻意的證明方法／定義形式**（README §238：數學內容手稿勝出）——用 squeeze 而非 L'Hôpital、採某種等價定義式，是編輯選擇，不是錯。
- **預設省略的證明**（§5：proof 選用、預設省略）——「沒給證明」不是數學錯。
- **刻意的記號升級**（§9／README §203）——手稿 `[x]`、HTML 用 `\lfloor x\rfloor` 等有意升級；提問即可（走 M6），不當錯砍。
- **明標 *Informally* 的非正式陳述**——啟發式 gloss 不必扛完整嚴謹度；別拿 full rigor 挑剔已標 informal 的句子。
- **節層級一次宣告、其後沿用的範圍假設**（如 "throughout this section, $f$ is continuous"）——別在每次使用處重覆標 M8。
- **明標近似的示意**（"approximately"、"roughly"、示意比例）——刻意近似不算 M4／M5。
- **語意等價的表述差異**——$\lim f = L$ vs $f(x)\to L$、區間寫法的等價變體；等價 ≠ inconsistency。
- **§7 允許的公式呈現變體**——只要數學等價，display 模式的選擇不是數學錯。

## 護欄

- **一律 *「請查核 X」* 框架**（README §204）：每條 finding 都附「為何存疑＋依據」，措辭是「這個陳述／步驟看似有誤，**請查核**」，**不是**「我移除／改了 X」。稽核員的數學把握度天生較低——可能誤讀，或手稿有意如此。
- **數學內容手稿勝出**（README §238）：凡與手稿的數學差異，當作「請確認是有意升級還是該對齊回手稿」的問題提出，**不自行判錯、不自行改**。
- **不確定時降級，不升級**：把握不足 → 提 Advisory「請查核」而非 Blocking。**寧缺勿濫——over-report 會稀釋真正的 blocking。**
- **唯讀**：只回報，不改任何檔案；Blocking 的修法也只**提議**，交使用者落地。

## 回報規格

四級，只報 tier 1–2、tier 3 至多一行、tier 4 略（專案 review 慣例，**不 over-report**；**乾淨的章節是有效結果**）：

1. 明確的數學缺陷（blocking：偽陳述／錯答案／不健全推理）→ 報；
2. 值得提的 advisory（未明說的限制、該補的嚴謹度、不致誤解的記號 drift）→ 報；
3. 純風格／品味層級的數學表述偏好 → ≤1 行，低優先；
4. non-finding（見上節）→ 略。

**輸出格式：**

- 首行：`VERDICT: <B> blocking, <A> advisory`（math gate 收斂 ⇔ `B = 0`）。
- 逐條（一行一筆）：
  `- [Blocking|Advisory] [M#] <sec>:<locus> — <宣稱／步驟>（原文：「…」）｜為何存疑：<…>｜依據：<手稿／SPEC §／數學理由> → 請查核／建議：「…」`
- 每個**乾淨**的維度各一行（如 `M4 推導步驟: clean`）。
- 末行：對「**數學 blocking 是否歸零**」給一句明確結論（math gate 收斂判準）。

**交付給使用者裁決時**：產 standalone HTML 審核稿（MathJax/KaTeX CDN、雙擊即開、數學即渲染、頂部摘要表、逐條卡片含原文與「請查核」理由），比照散文兩閘的 `REVIEW-…-gate*.html`／本輪落地的 `REVIEW-…-applied.html`。每條 finding 標**穩定編號**（如 `M-1…`；subagent 化後可比照 gate 用 `G1-`／`G2-`），方便逐條報編號討論與回覆裁決。**不要**交塞滿生 LaTeX 的 `.md`（CLAUDE.md 規則）；純版控紀錄（如本 rubric）不在此限。

---

> **狀態（v0.1，經 ch01 首輪 dry-run 校準）**：維度自 README §Mode B「數學正確性」＋ CONTENT_SPEC §5／§7／§9／§15 蒸餾。2026-06-16 對 ch01 §1.1–§1.6 跑首輪稽核＋對抗式複核（報告 [`REVIEW-ch01-math-audit-gate1.html`](REVIEW-ch01-math-audit-gate1.html)）：auditor 提 3 條 advisory（2×M5 啟發式／特例、1×M6 手稿飄移），對抗式複核一致判為 rubric-protected non-finding 全數撤回，**0 confirmed defect**。校準結論：non-findings 護欄＋「不確定降級」護欄運作正常、成功攔下 over-report，**擋稿線與 non-findings 暫不鬆動**。CONTENT_SPEC §15「Build 與過閘」已加 math gate 檢核項（與 prose gate 1／gate 2 並列）。待累積更多章節實證後再評是否需 `handout-math-audit` subagent 外殼。
