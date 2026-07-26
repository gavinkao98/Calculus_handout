# Kickoff：散文平實化回填（合併 sweep）——每單元的關卡序

> **新對話直接用：** 對新對話說「讀 `handout/html/_audit/KICKOFF-plain-backfill.md` 並對 ch07 執行」即可開跑。本檔是**流程權威**（跑哪些關卡、擋稿線、要不要徵同意、產物命名）；**判準權威**在 [`CONTENT_SPEC.md`](../../../CONTENT_SPEC.md) §3〈平實英文條款〉（狀態：RC，2026-07-25 凍結）。

## 這條線在做什麼（一段背景）

使用者反映 LLM 撰寫的課文英文「艱澀、太文學，不適合非母語讀者」。診斷結論：病灶不是句長或音節（Flesch 類公式對病句全部放行），而是**對 EFL 讀者不透明**——不透明慣用語與搭配、擬人與隱喻承載數學內容、一句塞兩個獨立論述動作、段落塞多個論證、以及過量 em-dash（可量測的 LLM 指紋）。原本是兩條規則線（平實化、去 em-dash），2026-07-25 因實測「互相抵銷」而**合併為一輪 sweep**。

已完成（2026-07-26 合併回收後，11 個單元中 **8 個達標**）：appB 2.2、ch01 2.1、ch02 0.9、ch03 1.6、ch04 2.3、ch05 0.8、ch06 1.4、ch07 1.6——全部落在 APEX（0.5）與 CLP1（3.1）之間，逐輪紀錄見各章 `REVIEW-ch<NN>-plain-applied.html`。ch01 §1.4 **刻意不動**，作為手稿章（真人逐字）的假陽性基準。

**剩餘：** appA 18.8／appC 17.8／appD 13.2 三個附錄——**2026-07-26 使用者裁決：暫緩執行**（先開新章驗證生成端條款，附錄另擇時機再啟）。（ch06 已於 2026-07-26 完成合併 sweep 併回 `main`：62 筆、12.5→1.4/1000，紀錄 [`REVIEW-ch06-plain-applied.html`](REVIEW-ch06-plain-applied.html)。）

## 開跑前必讀（權威來源，依序）

1. `CLAUDE.md`（根）＋ `handout/CLAUDE.md` — 專案紀律：Codex 唯讀調用**逐次徵同意**、繁中對話、commit body 逐條記 Mode B、fragment 是唯一內容源。
2. `CONTENT_SPEC.md` §3〈平實英文條款〉— **判準**：MUST／SHOULD／FLAG 三層、暖句四條件、**成對破折號與標點負載**（量測、`T_can`、CUT palette、四步仲裁決策序、先例、不換 tic 護欄、原因標籤、固定執行序、兩閘不可互相豁免）、段落層數值。
3. `handout/html/_audit/PROSE-AUDIT-RUBRIC.md` — 四維度（U 易懂／F 流暢＋黏接判準／S·A·V 語意聲音／**R 語域平實**）、擋稿線、non-findings。
4. `handout/html/_audit/REPORT-emdash-baseline-and-rollout.md` — 基準與 rollout 帳本（canonical 現況表、超額件數排序、每輪完成後回來打勾）。
5. 前例報告（照這個形狀產出）：`REVIEW-mainline-plain-walk.html`（走查）、`REVIEW-ch06-sec-6-2-plain-applied.html`（執行＋math gate）、`REVIEW-ch06-sec-6-3-plain-applied.html`（含段落標準）、`REVIEW-merge-dedash-plain-proposal.html`（合併設計）。

## 關卡序（每單元一輪；⛳＝停下來交付／徵詢）

### Gate 0 — 基線與地雷勘查（唯讀）

- `python tools/prose_metrics.py --unit <unit>` → 記下 canonical `N`、em-dash 數與密度、**tic guard 四項**（冒號接子句／分號／左括號／成對逗號）作為前值。
- 段落層量測：最長段詞數、每段最多行內式、≥150 詞段數（觸發器見 SPEC §3）。
- **讀 fragment 開頭的 HTML 註解**：專案慣例把「不得動的措辭」寫成 `CONSTRAINT`／`WORDING CONSTRAINT`（appB §B.2 有兩處、§B.6 有多處）。**動到它們＝破壞已裁決的設計**。
- 確認該單元既有閘的狀態（數學／圖／example／learner-sim 是否已過），據此決定 Gate 5–6 的範圍。

### Gate 1 — 走查（Claude gate-1，propose-only）⛳

依 SPEC §3 的**固定執行序**：① 範圍／數學安全 → ② 論述動作判讀 → ③ CUT／KEEP → ④ 節級密度閘 → ⑤ 不換 tic 檢查。

- 每條 finding 附：**candidate ID**、原因標籤（`DASH-CUT`／`DASH-KEEP`／`PLAIN-SPLIT`／`TIC-REBALANCE`／`R1-LEXICAL`）、踩哪個測試（R1–R3／F4／段落觸發器）、一行為什麼、改寫或【刪】。
- **成對破折號一律走四步仲裁決策序**（SPEC §3），不得只換成逗號；**先例具約束力**：`— far more often —` KEEP、`— only then —` 預設 KEEP、`— and over the integers you never can —` 整句重寫。
- 產 `REVIEW-<unit>-plain-walk.html`（standalone、MathJax CDN、雙擊即開、頂部摘要表、逐條卡片、含 `<del>`／`<ins>`）。**裁決前不改任何 fragment。**

### Gate 2 — Codex gate-2（跨模型獨立裁決）⛳ 需徵同意

- `codex exec -s read-only`，**材料一律 inline 進 prompt**（本機讓 Codex 自讀 fragment 會把 UTF-8 解成亂碼，整批假陽性——2026-06-28 實證）。
- 大 prompt（>70KB）會跑 10–15 分鐘：**用背景執行**，不要卡前景 timeout。
- 逐項要 `ADOPT／MODIFY／REJECT`；並問「未拆／未改的判斷是否正確」（Codex 三度抓到真問題：撤回一條不該改的、指出我拆過頭、抓到 spec 的數值矛盾）。
- 產 `REPORT-<unit>-codex-<round>-raw.md`（raw 照登）＋整合進 applied 報告。

### Gate 3 — 裁決與交易式套用

- 政策題（會牽動全書機制用語者，如 `on credit`）⛳ **交使用者裁決**；逐條 finding 可依使用者授權整批執行。
- 套用後 `python tools/verify_edits.py <file> <edits.txt>` → 必須 **PASS：工作樹 == HEAD ＋ 恰好這些替換**（reverse-apply byte-for-byte，未涵蓋差異 0 處）。

### Gate 4 — build ＋ 量測回歸（blocking）

- `python handout/html/build.py <unit>`。
- `python tools/prose_metrics.py --unit <unit>` → 對照 Gate 0 前值：
  - em-dash 密度須達 **`T_can` ≤ 3.0/1000**（canonical）；`N < 1000` 的單元報 raw `n/N`、與鄰近單元合併判定。
  - **不換 tic**：四項標點任一「raw ≥ +3 **且** 密度 ≥ +0.5/1000」→ MUST 填理由。
  - 句長：平均 18–22 為監測值（非門檻）、P90 32–35 審查區；**不設硬性上限、不機械拆句**。
  - 段落層：≤120 詞／≤20 式為 SHOULD；≥150 詞或 >20 式或一段多論證 → 人工判定。

### Gate 5 — Math gate（範圍限定，blocking）

- **數學片段程式化比對**：`git show HEAD:<file>` vs 現在，逐片段 diff；理想是 **零差異**（§6.3 達成 189→189），有差異須逐條說明。
- 對改動句走 M1–M8（定義／定理陳述／量詞邏輯／推導／邊界條件／記號一致／跨節一致）；契約見 `MATH-CORRECTNESS-RUBRIC.md`。
- 結構健檢：標籤配對（`<p>`／`<section>`／`<div>`）、inline 數學分隔符配對、**cross-ref 清單全數在位**。
- **重複片語掃描**：`python tools/dup_scan.py <unit>`。`verify_edits.py` 只證明「替換恰好套用一次」，**證不出替換字串的尾端與後文語意重複**；`figcaption` 又屬副表、不入 canonical 主分母，散文閘與密度閘都不看。ch07 的 `E-08` 就是這樣把一整句貼成兩次、一路過關到排版才被 LaTeX 人眼閘抓到（2026-07-26）。真 bug 的特徵是**間隔 ≈ 片語長度的密集叢集**（多個重疊 n-gram）；間隔 40–70 詞的多是定義↔重述、定理↔證明呼應或刻意的平行句，屬 rubric 的「刻意的教學重複」，不是 finding。

### Gate 6 — Mode B 語意等價（範圍限定）

只審**本輪改動句**的四維度（U／F／S·A·V／R），確認改寫保語意、未拆散量詞 scope 與條件—結論、未造出連續三句長度相近。**不重跑該單元其他既有閘**（圖閘、example 選題、learner-sim 已過者不重跑；除非改到 figcaption 語義）。

### Gate 7 — LaTeX 線同步（若該單元在 LaTeX rollout 內）

- `cd handout/latex && python make_dist.py <unit>` → 三閘全綠：log（0 error／0 missing char）＋完整性閘（`check_prose.py`，**0 處真落差**）＋字形閘（`check_glyphs.py`）。
- **另外要手動跑 `python handout/latex/test_convert.py`**（2026-07-26 補；`make_dist.py` **不會**跑它）。
  原因：golden tests 裡有**逐章的數學段數普查錨**（目前 ch03 612、appB 571），本輪只要淨增減行內式就會紅。
  它已經連續踩中兩次——appB 一次（`942ccea`，566→571）、ch03 一次（`c849bca`，605→612），
  而且兩次都因為 Gate 7 卡在前面的閘就中止、golden tests 又不在三閘定義內，所以**當下沒被發現**。
  錨的用途是防止「依序、恰好一次」的不變式被縮水的集合空洗，**內容合法增減時它就該跟著更新**，
  並在原地寫下沿革（數字為何變）。
- 目前 `NAMES` 表有 appB、ch01、ch02、ch03；**其他單元先補表**。不在表內者記為 pending，不可默默跳過（appB 曾因此脫鉤兩輪）。

### Gate 8 — 版面目檢

開 `handout/html/standalone/<unit>-print-standalone.html`，看分頁：孤行、溢頁、圖文相鄰。**拆句與拆段會增加行數**，這關不能省。

### Gate 9 — 紀錄與提交

- 產 `REVIEW-<unit>-plain-applied.html`：前後全句對照（依原因標籤分組）＋驗收表（Gate 4–8 逐項）＋保留清單（示範規則不誤傷）＋誠實記錄未完成項。
- 回 `REPORT-emdash-baseline-and-rollout.md` §2 更新密度與 tic guard 四項並打勾。
- commit：subject ≤70 字、body 逐條記 Mode B 裁決（原本是什麼／為何不妥／改了什麼／證據），末行 `Co-Authored-By`。

## 硬護欄（違反即缺陷）

- **裁決前 propose-only**：Gate 1–2 不改任何 fragment。
- **不動數學**：公式、編號、cross-ref 一律不碰；math gate 以程式化比對證明。
- **不機械拆句／不設硬性句長上限**；不得為維持句數用任何標點把兩個獨立推論黏回一句。
- **不得只把成對破折號換成逗號**（表面去 dash）；KEEP 先例具約束力。
- **兩閘不可互相豁免**：逐例 KEEP 不因密度差幾個名額被機械改掉；KEEP 的存在也不豁免節級密度——仍超標時另找安全改點、重寫真正的多動作句，或**明示節級例外**。
- **不重跑已過的其他閘**（避免白工）；但**改過的段落不能沿用舊 pass**。
- Codex 調用**逐次徵同意**；付費／外部 API 同。

## 回填順序（依超額件數 `n − 3N/1000`，2026-07-25）

~~ch07 (128) → ch02 (95) → ch05 (86) → ch04 (71) → ch06 剩餘節 (55) →~~ **appA (49)** → ~~ch03 (42) → ch01 (37) →~~ **appC (20)** → **appD (14)**（三附錄 2026-07-26 使用者裁決**暫緩執行**）。

**2026-07-26 合併回收**：ch02／ch03／ch04／ch05／ch07 五條分支已無衝突併回 `main`，全書複測無單元回退（rollout 帳本 §2 已更新）。**Gate 0 的 provenance 前提修正見 [`PROMPT-plain-backfill-ch02-ch07.md`](PROMPT-plain-backfill-ch02-ch07.md) 檔頭**——手稿章的「逐字保留」先例要先量重疊率才成立，別直接假設。

## 新增章節不走本流程

合併後 em-dash 與平實條款都在 SPEC §3，**Mode A 的 brief 與完稿自檢直接呼叫 `tools/prose_metrics.py`＝生成端就受約束**。下一個新節同時作為「生成端兩臂對照」的場地（一臂只給範文、一臂掛完整條款），用以驗證新章是否還需要回填輪——這也是條款升 v1.0 的最後一塊。

---
*本檔 2026-07-25 建立，作為 RC 凍結後的回填流程權威。判準變更一律改 `CONTENT_SPEC.md` §3，不在本檔另立規則。*
