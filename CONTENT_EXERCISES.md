# 習題：最低骨架

完整的習題系統設計延後至本書主要內容大致完成後進行（見 [`CONTENT_SPEC.md`](CONTENT_SPEC.md) §14）。本檔案是**最低骨架**——在各章開始累積正式習題之前就應鎖定的決策，以免日後每一節都得回頭改造。

本檔案中標記為 *(TBD)* 的項目是明確開放的。未標記 *(TBD)* 的項目是 working decision，作者應遵循直到本檔修訂為止。

> **適用範圍修正（2026-06-12，使用者定案）：講義本體不收節末習題。** 習題改由日後**獨立的
> 習題本**處理（屆時的設計輪次沿用本檔的預算、題型分類與答案／提示決策）。本檔的「選題流程」
> 一節是格式無關的共用工作流程，**當前的應用對象是課文內的 worked examples**（`example`＋
> `solution`，見 [`CONTENT_SPEC.md`](CONTENT_SPEC.md) §5；HTML 線為 `env-example`＋
> `env-solution`）——矩陣的欄判準從「四類題型覆蓋」改讀為「每個教學點有無示範」，且官方
> solution 為硬性條件（worked example 必須附完整解）。[`CONTENT_SPEC.md`](CONTENT_SPEC.md)
> §14「每節結尾 MUST 有 Exercises 區塊或 TODO placeholder」與本定案衝突，**待依 spec 的
> 修訂協議提案處理**；在那之前 placeholder 留在原處不動。

---

## Spec 與本檔的分工

[`CONTENT_SPEC.md`](CONTENT_SPEC.md) §5（`exercise` environment）+ §14（延後設計）已確立：

- 每節結尾 **MUST** 有一個正式的 `\subsection*{Exercises}` 區塊，或者 TODO placeholder 註解 `% TODO: add \subsection*{Exercises} block with end-of-section problems for Section N.M.`
- 習題為 **book-only**——它們不會進入投影片、旁白或 Manim storyboard（見 [`README.md`](README.md) *Media scope*）。
- 完整的習題系統（difficulty marker、answer appendix、inline self-check variant、hint format）是**延後的**。

本檔案處於 placeholder 規則和完整延後設計之間。它釘住最低限度，使得未來正式設計開啟時，是在精煉既有結構，而非從零發明。

---

## 每節預算 *（working decision——預設區間，coverage 為權威）*

- **預設區間：每節 8–12 題。** 短小的單一技能節自然會偏低（5–6 題）；計算密集的節可高達 15 題。
- 此區間是校準用的預設值，**不是配額**。權威判準是該節的**覆蓋矩陣**（見下方*選題流程*）：該節教授的每個 definition、theorem 和 strategy 都必須以其學習目標所要求的深度被練習到。
- **合規判定以矩陣為準，不以數量為準。** 一節不合規的情況是：某個教學項目沒有對應習題，或者用近乎重複的題目灌數以達到區間——而不是一個已充分覆蓋的節只有 6 題，也不是一個五技能的節需要 16 題。
- 在骨架階段，落在區間外的節不需要另寫 exception comment；其覆蓋矩陣即為理由。

原理：各節內容差異太大，無法用同一個固定數字——一技能的節和五技能的節不該共用同一個配額。區間之所以保留為預設值，是因為多數節確實落在此範圍內，而且在 gap-fill 階段它仍是合理的 sanity check（自學讀者需要足夠的反覆練習，但做完全部習題不該耗掉一整個週末）。矩陣在數量會導致錯誤決策時具有權威性，呼應 [`CONTENT_SPEC.md`](CONTENT_SPEC.md) §5 中 remark-target 的慣用語（"a target, not a production quota"）。

---

## 題型分類與組合 *（working decision——分類固定，每節組合由內容決定）*

四種題型的分類是固定的；每道習題歸屬其中之一：

| 類型 | 目的 |
|---|---|
| `conceptual` | "why" 或 "what fails if"——迫使讀者陳述一個 definition 或判斷某個條件是否成立。 |
| `computational` | 直接將方法應用於乾淨的輸入。 |
| `reasoning` | 短證明、反例構造、"for which inputs does this identity hold?" |
| `applied` *（選用）* | physics / economics / geometry 的應用情境（適用時才加）。 |

**每節組合由內容驅動，不由配額驅動。** 覆蓋矩陣決定一切：ε-δ 的節合理地偏重 reasoning，技巧型的節合理地偏重 computational，早期章節自然偏向 conceptual + computational。一個類型只有在該節的內容確實賦予它有意義的工作時才會出現。

**全書預設先驗分布**——gap-fill 步驟的目標分布，也是章節層級的 sanity check：

> `conceptual` ≥ 20% · `computational` 40–60% · `reasoning` ≥ 10% · `applied` 0–20%

以**每章**為單位審計這些比例，而非每節：章級總計應接近先驗值，即使個別節有所偏斜。整章未達先驗值通常意味著 conceptual / reasoning 的供給不足（這是反覆出現的失敗模式），而非由內容驅動的偏斜。

`exercise` environment 內部的 type marker 本身是 *(TBD)*——可能的選項包括 `type=` key-value argument、`\begin{exercise}[conceptual]` optional label、或不在原始碼中做標記（type 僅由作者判斷執行）。在完整設計輪次中擇一。

---

## 選題流程 *（working decision——manuscript 優先、bank 填補、AI fallback）*

習題從三個來源進入一節，按優先順序，每題追蹤 provenance。

1. **Manuscript 習題——必要核心。** 教師手稿中的每一道題目都出貨。它們為覆蓋矩陣播種。
2. **開放題庫——gap fill。** 當該節的主要內容寫好之後：
   1. 建立**覆蓋矩陣**：列 = 該節教授的每一個 definition / theorem / strategy；欄 = 四種題型。標記 manuscript 習題已覆蓋的格子。
   2. 在本地題庫（[`problem_banks/README.md`](problem_banks/README.md)）中搜尋填補空格的候選題；產生候選清單供人工篩選。題庫的分類法是**搜索索引**——gap 由該節自身的內容定義，不由題庫碰巧包含什麼來定義。
   3. 將被接受的題目適配為本書的語域與記號（[`CONTENT_SPEC.md`](CONTENT_SPEC.md) §3、§9）。
3. **AI 出題——fallback。** 僅用於沒有題庫能填補的格子（通常是與 manuscript running example 緊密耦合的擴展題）。需人工審核，同前。

### Provenance 與授權

- 每道非 manuscript 習題在匯入時帶有來源標記：`[source: CLP-1 §1.3 #2]`、`[source: APEX §6.1 #14]`、`[source: AI]`。在完整設計輪次決定標記是否、以何種方式出現在出貨產出之前，先以註解形式保留在原始碼中習題旁邊。
- `problem_banks/` 中的題庫全為 CC BY / CC BY-NC / CC BY-NC-SA——合法地組合為一份**以 CC BY-NC-SA 4.0 免費發行的講義**，附 credits page。不要從 share-alike-only 來源（CC BY-SA，如 Active Calculus）或「free to view but not openly licensed」來源（如 Paul's Online Math Notes）匯入。
- **在匯入時擷取題庫的官方 hint / answer / solution**，存入章節的 import record（`exercise-imports.md`，放在章節原始碼旁邊）。這是未來 answer appendix 的原始素材，不是 appendix 本身——匯入時遺失就得日後重新推導每個 solution。

---

## 答案與提示 *（working decision）*

兩個承重決策：

- **習題是否附帶答案？**
  Working default：**精選的 computational 習題附一個最終的數值或符號答案**，放在書末，讓自學讀者能檢查自己的結果而不必看完整 solution。Conceptual 和 reasoning 習題預設不附答案。
- **習題是否附帶提示？**
  Working default：**習題不附 inline hint。** 如果一道題需要提示才能入手，那它可能設計有問題，前方的 worked example 應該承載那個想法。

Answer-appendix 的格式（章末 vs. 書末、選取準則、在原始碼中的編碼方式）是 *(TBD)*。

---

## Difficulty marker *（延後）*

刻意尚未決定。完整設計輪次將從以下選項中擇一：

- 完全不標記（最簡單——節內順序即難度）。
- ⭐ / ⭐⭐ / ⭐⭐⭐ inline marker。
- 字母代碼（`A`、`B`、`C`）。
- 分為 `\subsection*{Exercises}` 和 `\subsection*{Challenge Problems}` 兩個區塊。

在該決策落地之前，**不要**在習題原始碼中編碼難度。區塊內的排列順序是唯一允許的難度信號。

---

## 編號與 label *（working decision）*

- 習題按節編號：`1`、`2`、...，每進入新的節重新開始。
- label 遵循 [`CONTENT_QUICKSTART.md`](CONTENT_QUICKSTART.md) 中的專案 label 慣例：`ex:sectionslug-descriptor`。例：`ex:limits-squeeze-1`。
- label **SHOULD** 出現在後續章節會引用的習題上。大多數習題不需要 label。

---

## `\subsection*{Exercises}` 內的格式 *（working decision）*

```latex
\subsection*{Exercises}

\begin{exercise}
  Prompt text.
\end{exercise}

\begin{exercise}
  Another prompt. May contain display math, inline math, and short
  multi-part structure using \texttt{enumerate}.
\end{exercise}
```

多部分的習題在 `exercise` body 內使用 `enumerate`。在完整設計輪次之前不要為 sub-part 發明新的 environment。

---

## 完整設計輪次之前 NOT to do 的事

以下是我們想避免在習題系統正式設計之前累積的陷阱：

- **不要**發明 per-chapter exercise macro。如果某個捷徑看起來有用，記錄在 [`CONTENT_ROADMAP.md`](CONTENT_ROADMAP.md) 中該章的 open-questions 清單，而不是加一個 `\newcommand`。
- **不要**把投影片或旁白內容混進 exercise prompt——習題是 book-only。
- **不要**在選取準則和格式鎖定之前開始建 answer appendix。（將題庫提供的 solution 擷取到章節的 `exercise-imports.md` 是可以的——那是匯入原始素材，不是 appendix。）
- **不要**在原始碼中標記難度。
- **不要**加 inline hint。

---

## 本檔案何時升級

觸發條件：**大多數章節的主要內容已完成**（依 spec §14）。

屆時，專門的習題設計輪次將：

1. 審計現有 TODO placeholder 和已累積的正式 exercise 區塊。
2. 決定延後的項目：difficulty marker、answer appendix 格式、hint 策略、原始碼內 type taxonomy、environment variant（self-check、challenge）。
3. 以完整 spec 取代本骨架檔案，並增加版本號。
4. 逐章改造既有的 exercise 區塊以符合新 spec。

在此之前，本檔案未涵蓋的事項應偏向**簡單且可逆**——將習題視為「帶框的散文」而非一個 domain-specific 子系統。
