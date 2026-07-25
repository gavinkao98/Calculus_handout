# Kickoff prompts：ch02–ch07 散文平實化回填（合併 sweep）

> 每章一段，各自貼進**不同的新對話**。ch01 見 [`PROMPT-plain-backfill-ch01.md`](PROMPT-plain-backfill-ch01.md)。
> 流程權威＝[`KICKOFF-plain-backfill.md`](KICKOFF-plain-backfill.md)；判準權威＝[`CONTENT_SPEC.md`](../../../CONTENT_SPEC.md) §3〈平實英文條款〉（RC，2026-07-25 凍結）。本檔只給**各章的 delta**：專屬前提＋起跑基線。

## 平行執行的三條紀律（每個 session 都必須遵守）

1. **一章一分支**：`handout/plain-chNN`。不要 commit 到 `main`，也不要跟別章共用分支。
2. **不動共用檔**：**MUST NOT** 編輯 `handout/html/_audit/REPORT-emdash-baseline-and-rollout.md`（rollout 帳本）與 `handout/latex/make_dist.py` 的 `NAMES` 表——這兩處平行寫必衝突。把新的密度與 tic guard 數字**寫進自己的 applied 報告**，並在報告末尾留一行「待併：rollout 帳本 §2 的 chNN 列」。
3. **build 一定帶參數**：`python handout/html/build.py chNN`。無參數版會重建全部 standalone、蓋掉別章成果。

`tools/prose_metrics.py`／`tools/verify_edits.py` 是唯讀工具，平行呼叫安全。

## 共同的起跑基線（2026-07-25 canonical，`T_can` ≤3.0/1000）

| 章 | N | em-dash | /1000 | 超額件數 | 冒號 | 分號 | 括號 | 雙逗號 | 變體 |
|---|--:|--:|--:|--:|--:|--:|--:|--:|---|
| ch02 | 6942 | 116 | 16.7 | 95 | 58 | 43 | 66 | 21 | 手稿章 |
| ch03 | 3855 | 54 | 14.0 | 42 | 36 | 20 | 60 | 28 | 手稿章 |
| ch04 | 6895 | 92 | 13.3 | 71 | 68 | 45 | 82 | 26 | 手稿章 |
| ch05 | 7502 | 108 | 14.4 | 85 | 77 | 47 | 43 | 28 | canon（無手稿） |
| ch06 | 5770 | 72 | 12.5 | 55 | 41 | 37 | 52 | 32 | canon |
| ch07 | 8795 | 154 | 17.5 | 128 | 102 | 37 | 56 | 32 | canon |

**手稿章 vs canon 章的預期差異**：Ch1–4 內容逐字取自手稿（真人作者），實測 ch01 §1.4 的家族命中密度 ≈0；canon 章（Ch5 起無手稿、LLM 自產）實測 ch06 §6.2 為 14.7／千詞。**手稿章的詞彙層 findings 會少很多，這是正常結果，不得為湊數 over-report**；canon 章反之要預期較多。em-dash 密度兩者都超標，與變體無關。

## ch01 輪（2026-07-25，RC 後第一個回填單元）建立的先例——**手稿章必讀**

ch01 已完成：em-dash 9.3 → **2.1**/1000、執行 41 條（走查 42 − Codex REJECT 1）、數學片段零差異、分頁 53 頁不變、§1.4 對照組零改動；Codex gate-2 ADOPT 34／MODIFY 7／REJECT 1。紀錄：[`REVIEW-ch01-plain-walk.html`](REVIEW-ch01-plain-walk.html)、[`REVIEW-ch01-plain-applied.html`](REVIEW-ch01-plain-applied.html)、[`REPORT-ch01-plain-codex-raw.md`](REPORT-ch01-plain-codex-raw.md)。以下三點對 **ch02／ch03／ch04**（同為手稿章）有約束力：

1. **Gate 0 要比對手稿，把每個 dash 分類為「手稿逐字」或「LLM 增補」。** ch01 這樣做之後發現：手稿本身的散文 em-dash 密度只有 **2.42/1000**（本來就在 `T_can` 內），fragment 的 9.3 幾乎全來自 LLM 增補段落——**20 個單破折號尾巴全部是 LLM 寫的**。手稿檔：ch02→`legacy/tex_handout/chapters/ch02_derivatives.tex`、ch03→`ch03_chain_rule.tex`、ch04→`ch04_exponential_logarithm.tex`。
2. **手稿逐字的成對插入語保留**（使用者裁決，比照 §1.4 對照組）。ch01 最後留下的 12 個 dash ＝ 手稿逐字 8 ＋ §1.4 凍結 4。**改 LLM 增補的、不改真人寫的**——這也讓「達標」與「保住作者聲音」不再衝突。
3. **沿用 ch06／ch01 已裁的詞彙先例**，不要重新發明：擬人（式子「屈服」`yield to`→`is handled by`）、品格詞配數學物件（`honest reciprocals`→`really are reciprocals`）、片語動詞（`puts to work`→`uses`）。同型出現時直接引用先例編號，別再開新裁決。

---

## ch02

```text
你在一個 fresh session。任務：對 ch02 執行一輪「散文平實化回填（合併 sweep）」。

先讀（依序）：CLAUDE.md（根）＋handout/CLAUDE.md → handout/html/_audit/KICKOFF-plain-backfill.md
（本輪流程權威，Gate 0–9，照它跑）→ CONTENT_SPEC.md §3〈平實英文條款〉（判準，狀態 RC）
→ handout/html/_audit/PROSE-AUDIT-RUBRIC.md → 前例形狀 REVIEW-ch06-sec-6-2-plain-applied.html。

ch02 專屬前提：
- ch02／ch03／ch04 是手稿章：**Gate 0 必須比對手稿把每個 dash 分類為「手稿逐字」或「LLM 增補」**
  （ch01 先例：手稿本身只有 2.42/1000、本來就達標，超標幾乎全來自 LLM 增補段落）。
  **手稿逐字的成對插入語保留**（比照 §1.4 對照組的使用者裁決）；改 LLM 增補的即可達標。
  手稿檔＝legacy/tex_handout/chapters/ch02_derivatives.tex。
  沿用 ch06／ch01 已裁的詞彙先例（yield to→is handled by、honest→really are、puts to work→uses），
  同型直接引用、不要重開裁決。
- ch02 是手稿章（內容逐字取自手稿），非 LLM 自產。預期詞彙層 findings 遠少於 canon 章
  （ch01 §1.4 實測家族密度 ≈0 vs ch06 §6.2 的 14.7/千詞）。乾淨的節是有效結果，不得湊數。
- §2.4 有 e^x 的 on-credit fence（「Everything about e^x in this section is on credit —
  borrowed now, to be repaid in Chapter 4.」）。on credit 是全書機制用語（SPEC §16.1）、
  首見處已 gloss，一律保留；只在周邊贅飾動手。那個 dash 屬「首見 gloss 的交付」，
  走四步仲裁決策序判、不要反射式砍掉。
- Gate 7（LaTeX）：make_dist.py 的 NAMES 表沒有 ch02 → 記 pending，不可默默跳過，
  也不要為此改 NAMES（平行輪會衝突）。

起跑基線（canonical）：N=6942、em-dash 116、16.7/1000、超額約 95 件；
tic guard 冒號 58／分號 43／括號 66／雙逗號 21。
逐節（dash 多到少）：§2.4 32 個（18.4）、§2.2 26（19.0）、§2.5 23（14.1）、§2.3 21（18.4）、
§2.1 14（13.1）。段落離群：§2.1 有一段 175 詞。

平行紀律：commit 到新分支 handout/plain-ch02；MUST NOT 編輯 rollout 帳本
（REPORT-emdash-baseline-and-rollout.md）與 make_dist.py 的 NAMES；build 一定帶參數
（python handout/html/build.py ch02）。

先做 Gate 0（基線＋grep fragment 註解裡的 CONSTRAINT／WORDING CONSTRAINT），
再進 Gate 1 走查；走查產出後停下來給我過目。
```

## ch03

```text
你在一個 fresh session。任務：對 ch03 執行一輪「散文平實化回填（合併 sweep）」。

先讀（依序）：CLAUDE.md（根）＋handout/CLAUDE.md → handout/html/_audit/KICKOFF-plain-backfill.md
（本輪流程權威，Gate 0–9，照它跑）→ CONTENT_SPEC.md §3〈平實英文條款〉（判準，狀態 RC）
→ handout/html/_audit/PROSE-AUDIT-RUBRIC.md → 前例形狀 REVIEW-ch06-sec-6-2-plain-applied.html。

ch03 專屬前提：
- ch02／ch03／ch04 是手稿章：**Gate 0 必須比對手稿把每個 dash 分類為「手稿逐字」或「LLM 增補」**
  （ch01 先例：手稿本身只有 2.42/1000、本來就達標，超標幾乎全來自 LLM 增補段落）。
  **手稿逐字的成對插入語保留**（比照 §1.4 對照組的使用者裁決）；改 LLM 增補的即可達標。
  手稿檔＝legacy/tex_handout/chapters/ch03_chain_rule.tex。
  沿用 ch06／ch01 已裁的詞彙先例（yield to→is handled by、honest→really are、puts to work→uses），
  同型直接引用、不要重開裁決。
- ch03 是手稿章，非 LLM 自產 → 預期詞彙層 findings 遠少於 canon 章；乾淨的節是有效結果。
- **Gate 7 這章要真的跑**：ch03 已在 make_dist.py 的 NAMES 表內（appB、ch03），
  改完後 cd handout/latex && python make_dist.py ch03，三閘（log／完整性 check_prose／
  字形 check_glyphs）須全綠、完整性閘 0 處真落差。這是全書第二個有 LaTeX 產物的單元，
  來源與產物必須同一個原子發布單位（appB 曾脫鉤兩輪，別重演）。
- §3.1 有和差化積的就地推導（SPEC §16.2 B 類就地建立），數學與推導步驟一律不碰。

起跑基線（canonical）：N=3855、em-dash 54、14.0/1000、超額約 42 件；
tic guard 冒號 36／分號 20／括號 60／雙逗號 28。
逐節：§3.2 22 個（16.4）、§3.3 16（12.6）、§3.1 16（12.9）。無段落離群。
注意括號 60／N 3855＝全書相對最高，去 dash 時 MUST NOT 再往括號堆（會踩不換 tic 護欄）。

平行紀律：commit 到新分支 handout/plain-ch03；MUST NOT 編輯 rollout 帳本；
build 一定帶參數（python handout/html/build.py ch03）。NAMES 表已有 ch03，不需改。

先做 Gate 0，再進 Gate 1 走查；走查產出後停下來給我過目。
```

## ch04

```text
你在一個 fresh session。任務：對 ch04 執行一輪「散文平實化回填（合併 sweep）」。

先讀（依序）：CLAUDE.md（根）＋handout/CLAUDE.md → handout/html/_audit/KICKOFF-plain-backfill.md
（本輪流程權威，Gate 0–9，照它跑）→ CONTENT_SPEC.md §3〈平實英文條款〉（判準，狀態 RC）
→ handout/html/_audit/PROSE-AUDIT-RUBRIC.md → 前例形狀 REVIEW-ch06-sec-6-3-plain-applied.html
（ch04 是證明重的章，§6.3 那份的處置方式最接近）。

ch04 專屬前提：
- ch02／ch03／ch04 是手稿章：**Gate 0 必須比對手稿把每個 dash 分類為「手稿逐字」或「LLM 增補」**
  （ch01 先例：手稿本身只有 2.42/1000、本來就達標，超標幾乎全來自 LLM 增補段落）。
  **手稿逐字的成對插入語保留**（比照 §1.4 對照組的使用者裁決）；改 LLM 增補的即可達標。
  手稿檔＝legacy/tex_handout/chapters/ch04_exponential_logarithm.tex。
  沿用 ch06／ch01 已裁的詞彙先例（yield to→is handled by、honest→really are、puts to work→uses），
  同型直接引用、不要重開裁決。
- ch04 是手稿章，但也是**全書 foundation 章**（e^x 冪級數構造、Bolzano–Weierstrass、MVT），
  深度上限、proof 比計算多。**符號密集段落另立標準**：優先改 display／分行 skeleton／
  先立記號，MUST NOT 為降詞數按詞切句、MUST NOT 拆散量詞 scope 與條件—結論。
- §4.1 開場有「All of that was on credit. This chapter goes back and pays the debt」——
  credit／debt／repay 是全書刻意貫穿、首見已 gloss 的機制隱喻，**一律保留**，
  只動周邊贅飾（參考 ch06 §6.2 的 W-13(a) 處置）。
- 段落離群四處要處理：§4.1 158詞/9式、§4.4 157詞/4式、§4.5 164詞/10式、
  §4.5 126詞/25式（**25 個行內式 > 20 的 SHOULD 上限，是全書目前唯一的記號離群**）。
  依 SPEC §3 段落層：≥150 詞或 >20 式或一段多論證 → 人工判定；拆段而非拆句。
- Gate 7（LaTeX）：NAMES 表沒有 ch04 → 記 pending，不要改 NAMES。

起跑基線（canonical）：N=6895、em-dash 92、13.3/1000、超額約 71 件；
tic guard 冒號 68／分號 45／括號 82／雙逗號 26（**括號 82 為全書最高，去 dash 時不得再往括號堆**）。
逐節：§4.2 23 個（12.3）、§4.4 21（11.7）、§4.5 19（15.2）、§4.1 17（12.1）、§4.3 12（21.1，密度最高）。

平行紀律：commit 到新分支 handout/plain-ch04；MUST NOT 編輯 rollout 帳本與 NAMES；
build 一定帶參數（python handout/html/build.py ch04）。

先做 Gate 0，再進 Gate 1 走查；走查產出後停下來給我過目。
```

## ch05

```text
你在一個 fresh session。任務：對 ch05 執行一輪「散文平實化回填（合併 sweep）」。

先讀（依序）：CLAUDE.md（根）＋handout/CLAUDE.md → handout/html/_audit/KICKOFF-plain-backfill.md
（本輪流程權威，Gate 0–9，照它跑）→ CONTENT_SPEC.md §3〈平實英文條款〉（判準，狀態 RC）
→ handout/html/_audit/PROSE-AUDIT-RUBRIC.md → 前例形狀 REVIEW-ch06-sec-6-2-plain-applied.html。

ch05 專屬前提：
- ch05 是**第一個 canon 章**（無手稿、100% LLM 自產，Ch5 起皆為此變體）。實測 canon 章的
  詞彙層家族密度遠高於手稿章（ch06 §6.2 為 14.7/千詞、§6.3 為 10.6，手稿章 ≈0）
  → **預期 findings 較多**：擬人（數學物件作主語＋情緒／意志動詞）、交易隱喻
  （earn／owe／grant／buy）、不透明慣用語、cleft、警句式收尾、低頻文學詞。
- 節數最多（九節），逐節密度平均但都超標；建議依 dash 數分兩批走查，避免一份報告過長。
- Gate 7（LaTeX）：NAMES 表沒有 ch05 → 記 pending，不要改 NAMES。

起跑基線（canonical）：N=7502、em-dash 108、14.4/1000、超額約 85 件；
tic guard 冒號 77／分號 47／括號 43／雙逗號 28。
逐節：§5.4 19 個（17.2）、§5.7 15（16.6）、§5.6 13（15.5）、§5.3 12（14.6）、§5.1 12（12.3）、
§5.8 11（13.3）、§5.9 10（16.9）、§5.5 10（13.7）、§5.2 6（8.5）。無段落離群。

平行紀律：commit 到新分支 handout/plain-ch05；MUST NOT 編輯 rollout 帳本與 NAMES；
build 一定帶參數（python handout/html/build.py ch05）。

先做 Gate 0，再進 Gate 1 走查；走查產出後停下來給我過目。
```

## ch06（剩餘節）

```text
你在一個 fresh session。任務：對 ch06 執行一輪「散文平實化回填（合併 sweep）」。
注意：ch06 有兩節已做過平實化，本輪範圍與其他章不同，先讀清楚。

先讀（依序）：CLAUDE.md（根）＋handout/CLAUDE.md → handout/html/_audit/KICKOFF-plain-backfill.md
（本輪流程權威，Gate 0–9）→ CONTENT_SPEC.md §3〈平實英文條款〉（判準，狀態 RC）
→ handout/html/_audit/PROSE-AUDIT-RUBRIC.md
→ **必讀既有成果**：REVIEW-ch06-sec-6-2-plain-applied.html 與
  REVIEW-ch06-sec-6-3-plain-applied.html（§6.2／§6.3 的完整處置紀錄與保留清單）。

ch06 專屬前提（範圍不同，務必看）：
- **§6.2 與 §6.3 的「詞彙層＋句法層＋段落層」已於 2026-07-25 完成**（§6.2 14 條、
  §6.3 11 條，含段落標準定值）。這兩節**不要重跑平實化**——但它們的 **em-dash 尚未處理**
  （§6.2 現 10 個/7.3、§6.3 現 10 個/9.1），本輪要一併收到 T_can ≤3.0。
  → 對 §6.2／§6.3 只做 dash 與標點負載；**已裁決的保留清單一律尊重**
  （on credit 機制用語、dominoes、ε-δ contest、one-way street 等）。
- **§6.1、§6.4、§6.5 是完整一輪**（詞彙＋句法＋段落＋dash）。
- **§6.1 有兩段段落離群**（156 詞、166 詞）＋**§6.5 一段 188 詞**——這是段落標準上線後
  第一批該處理的離群，依 SPEC §3 段落層判定（拆段、run-in 標籤，不拆句、不動數學）。
  §6.2 的 W-14 是可直接參照的前例（294 詞/34 式 → 五段）。
- **ch06 的 print 版分頁一直沒目視檢查過**（前輪瀏覽器打不開該檔）。Gate 8 這章請確實做，
  順便補檢 §6.2／§6.3 的分頁。
- Gate 7（LaTeX）：NAMES 表沒有 ch06 → 記 pending，不要改 NAMES。

起跑基線（canonical）：N=5770、em-dash 72、12.5/1000、超額約 55 件；
tic guard 冒號 41／分號 37／括號 52／雙逗號 32。
逐節：§6.1 24 個（16.7）、§6.4 15（17.9）、§6.5 13（12.6）、§6.3 10（9.1）、§6.2 10（7.3）。

平行紀律：commit 到新分支 handout/plain-ch06；MUST NOT 編輯 rollout 帳本與 NAMES；
build 一定帶參數（python handout/html/build.py ch06）。

先做 Gate 0，再進 Gate 1 走查；走查產出後停下來給我過目。
```

## ch07

```text
你在一個 fresh session。任務：對 ch07 執行一輪「散文平實化回填（合併 sweep）」。
ch07 是全書超額件數最多的單元（128 件），也是最新章——改完可當「新章標準流程」的樣板。

先讀（依序）：CLAUDE.md（根）＋handout/CLAUDE.md → handout/html/_audit/KICKOFF-plain-backfill.md
（本輪流程權威，Gate 0–9，照它跑）→ CONTENT_SPEC.md §3〈平實英文條款〉（判準，狀態 RC）
→ handout/html/_audit/PROSE-AUDIT-RUBRIC.md → 前例形狀 REVIEW-ch06-sec-6-2-plain-applied.html
＋ REVIEW-ch06-sec-6-3-plain-applied.html。

ch07 專屬前提：
- ch07 是 canon 章（無手稿、100% LLM 自產）→ **預期詞彙層 findings 最多**：擬人（數學物件
  作主語＋情緒／意志動詞）、交易隱喻（earn／owe／grant／buy）、不透明慣用語、cleft、
  警句式收尾、低頻文學詞。同時 em-dash 密度全書最高（17.5/1000）。
- **五處段落離群**：§7.1 204詞、§7.3 174詞/10式、§7.4 173詞、§7.7 247詞/10式、§7.7 190詞。
  §7.7 的 247 詞是全書第二大段落（僅次於已修的 §6.2 294 詞）。依 SPEC §3 段落層判定，
  拆段（run-in 標籤）而非拆句；參照 §6.2 的 W-14 前例。
- tic guard 的冒號接子句 102 為全書最高 → **去 dash 時 MUST NOT 再往冒號推**
  （appB 首輪就是這樣把負載從 dash 搬到冒號，事後得再清一次）。命題轉命題處改分句。
- Gate 7（LaTeX）：NAMES 表沒有 ch07 → 記 pending，不要改 NAMES。

起跑基線（canonical）：N=8795、em-dash 154、17.5/1000、超額約 128 件；
tic guard 冒號 102／分號 37／括號 56／雙逗號 32。
逐節：§7.2 30 個（23.8，密度最高）、§7.7 28（17.0）、§7.1 24（17.6）、§7.6 22（17.0）、
§7.4 18（14.6）、§7.5 16（17.5）、§7.3 16（15.0）。

平行紀律：commit 到新分支 handout/plain-ch07；MUST NOT 編輯 rollout 帳本與 NAMES；
build 一定帶參數（python handout/html/build.py ch07）。

先做 Gate 0，再進 Gate 1 走查；走查產出後停下來給我過目。
```

---

## 合併回收（各章跑完後由一個 session 統一做）

平行輪刻意讓各 session **不動** rollout 帳本與 `NAMES` 表，因此收尾要有人一次補齊：

1. 依序把 `handout/plain-chNN` 各分支併回 `main`（衝突只可能出現在 standalone，各章不同檔，實際應為 ff 或無衝突）。
2. 用各章 applied 報告末尾的「待併」數字，一次更新 `REPORT-emdash-baseline-and-rollout.md` §2 的密度與 tic guard 四項並打勾。
3. 若要讓 ch02／ch04–ch07 進 LaTeX 線，補 `make_dist.py` 的 `NAMES` 表（一次補完，之後逐章跑三閘）。
4. 全書複測：`python tools/prose_metrics.py`，確認每章 ≤3.0/1000、無單元回退。

---
*本檔 2026-07-25 建立。判準變更一律改 `CONTENT_SPEC.md` §3（RC 凍結，需「同一規則在三節以上反覆誤判」才夠格），不在本檔另立規則。*
