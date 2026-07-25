# Codex gate-2 raw：appB 平實化第二輪（句法黏接輪）回歸審核

- 調用：`codex exec -s read-only`（stdin 餵 UTF-8，材料 inline、未讓 Codex 讀檔），codex-cli 0.144.1，模型走 `~/.codex/config.toml` 預設。
- 日期：2026-07-25。授權：使用者本輪明示「跑 Codex 回歸審核」。
- 受審範圍：第二輪 20 個改點（A1–A15 拆句／B1–B3 分號回收／C1–C2 補修）＋未拆判斷（D 節）＋節奏成本＋升級後的規則措辭。
- 結果摘要：**15 PASS／5 FIX（A4、A8、A13、A15、B3）／0 REVERT**；Q2 確認「不拆」判斷全部正確；Q4 抓到「>25 詞占比 <10%」與「P90 32–35」的數學矛盾。
- 處置：5 個 FIX 全數採納；Q4 八條精修全數寫入 `CONTENT_SPEC.md` §3 與 `PROSE-AUDIT-RUBRIC.md` F4。整合紀錄見 `REVIEW-ch06-sec-6-2-plain-applied.html` §1–§2。
- 本檔為 **raw 輸出照登**（未刪改）。

---

## Q1　逐項裁決

- A1｜PASS（判斷正確：量詞是 `every`；hypothesis 藏在主語中 `integer divisible by 6` 的限制性描述，不是單獨藏在 `divisible`。）
- A2｜PASS（因果階梯完整，`So` 的銜接自然。）
- A3｜PASS（第二句明確展開何謂 advantage，沒有拆碎。）
- A4｜FIX: `Strategy B.1 requires the quantifiers to be explicit and in order. They are already explicit. But English often places a for all after the clause it governs, so the last of the three appears after the kernel rather than before it.`（現行的 `Explicit they already are` 倒裝，且 `asks for them explicit` 對 EFL 讀者偏生硬。）
- A5｜PASS（量詞相對次序仍是 ε → N → n；只有 kernel 後移，邏輯正確。）
- A6｜PASS（先引入 h，再說明二物件問題如何化為一物件問題，切點自然。）
- A7｜PASS（對稱性的前提、交換名稱的條件推論、claim 不變三者都保留且順序正確。）
- A8｜FIX: `The split into thirds gave each of the three pieces an allowance of ε/3. Since those allowances add to exactly ε, the sum of the three pieces is less than ε.`（`must come to less` 缺少明說的比較基準，對 EFL 讀者不夠清楚。）
- A9｜PASS（指令後接後果，簡潔而自然。）
- A10｜PASS（`Either … or, far more often, …` 是有意義的二分對照，不算黏接。）
- A11｜PASS（記號集合與 `x ∈ S` 的釋義是兩個真正不同的工作，指涉清楚。）
- A12｜PASS（`That` 明確指向 `let n = 2k`；三句有遞進，未過碎。）
- A13｜FIX: `The asymmetry here is worth carrying away. Over the integers, no number of confirming examples establishes a for all, because you can never check every object in its range. A single counterexample destroys one (§B.2).`（現行 `Short of …, and over the integers …` 的插入語失去破折號後句法鬆脫。）
- A14｜PASS（第一句保留量詞翻轉；第二句正確得到 `∃x ∈ S` 且 `P(x)` 成立、`Q(x)` 失敗，順序無誤。）
- A15｜FIX: `You can plan a proof before you can prove it, and you should. If you start at the top of the page without a plan, you may use at line one a fact that is established only at line ten.`（現行 44 詞冒號句仍同時承載勸告、替代行為與後果，值得拆。）
- B1｜PASS（斷開後更乾淨，沒有失去對比。）
- B2｜PASS（`None of that` 與前句的發現過程指涉清楚。）
- B3｜FIX: `Proof by contraposition is indirect only in what it establishes, not in how: you prove an equivalent sentence rather than the original claim, and §B.1 carries the result across.`（現行三個短宣告連續出現，略顯過碎；這個冒號仍是一個單一複雜想法。）
- C1｜PASS（`property` 準確指 rationality；新句語法與教學意義都正確。）
- C2｜PASS（術語首見加斜體恰當。）

## Q2　未拆項目

D 節的保留判斷都正確，沒有一項應再拆。

- §B.2 Strategy bullet 2 的冒號是「不是 contradiction，而是 direct proof」的必要釋義；既有 wording constraint 應保留。
- `And a split can sometimes be avoided altogether: …` 是 announce-then-deliver 的單一教學動作。
- lead、objectives、Definition B.1 與 B.4 的平行項目應以清單／平行結構閱讀，不應被當成普通散文黏句。
- §B.6 最後一句與 §B.3 最後一句都是定義性總結加展開；拆開會削弱收束力。

唯一執行條件是：正式 HTML 必須保留列表、display 式與標籤的視覺結構；若被壓成一段，應修版面，不應拆語句。

## Q3　節奏成本

`31 → 37` 是審核訊號，不是自動缺陷。真正讀起來像節拍器的是 §B.6 contraposition 段：

> `What you have written is a plain direct chain. The indirectness of a contraposition is in what it establishes, not in how. You never argued about the original claim itself. You proved an equivalent sentence, and §B.1 carried the result across.`

後三句加上前一句都很短、都是平直宣告；B3 的 FIX 可合回為一個較長但仍單一的說明句，正好解除這個節拍。

§B.5 Caution 尾端的 `Only a biconditional … / As you read … / A good share …` 約為同長三拍，但功能依序是規則、指令、後果，實際聽感尚可；不值得為了消除統計窗口而重黏。

## Q4　規則措辭

有一個明確的數值衝突：若 `>25 詞占比 <10%`，至少九成句子必為 `≤25` 詞，因此一般定義下 `P90` 應不高於 25，不可能同時把 `P90 32–35` 當同一母體的目標／正常區間。二者必須擇一調整：

- 保留 `<10%` 時，把長尾觀察改為例如 `P95 32–35`，並以已核准樣本校準。
- 保留 `P90 32–35` 時，`>25 詞占比 <10%` 必須放寬。

其餘漏洞與建議：

- 「一句一個完整想法」應定義為「一個論述動作」，不是一個子句。定義、條件＋結果、公式說明、平行列舉都可是一個動作。
- `≥30 詞＋黏接標點` 應明說是人工審核觸發器，不是拆句命令；否則正式定義、路線圖、引文、清單都會被誤傷。
- 應定義何謂「冒號接子句」：冒號後另起解釋／結果才計入；引出清單、引文、公式、標籤不計入。
- 也要補上漏網情形：多個推論可用 `and`、`while`、`which` 黏接，沒有冒號、分號或破折號也應由人工發現。
- 量詞與其範圍、條件與結論、代詞與先行詞不得因減少符號而被拆散。符號密集段落宜優先改 display、分行 skeleton、先立記號再使用，而非按詞數切句。
- 「連三句同長」應限定為連續散文，排除列表、proof skeleton、刻意平行與修辭三連；並以朗讀聽感判定，不只看 ±3 詞。
- 「AI 文風最典型」宜改為「常見的 AI-like 徵象之一」；它是讀感警訊，不是獨立的品質判準。
- 「不得反手用分號」太窄。應禁止的是為維持句數而重新黏回兩個獨立推論，不論使用分號、冒號、破折號或堆疊連接詞；單一對稱對比或正式定義仍可合法使用分號。

建議將 MUST 核心改為：

> 每句應服務一個可辨識的論述動作。30 詞以上且含潛在黏接訊號的連續散文句 MUST 人工判讀；這是審核觸發，不是拆句命令。只有當讀者必須在同一句完成兩個可獨立成立的推論或教學動作時，才拆開或改為列表。

## Q5　總裁決

總裁決：第二輪可採納，但應先納入 A4、A8、A13、A15、B3 的 FIX，並修正量化規則中 P90 與 `>25 詞占比` 的數學衝突。

- 以「論述動作」而非詞數或子句數判定是否拆句。
- 保護正式定義、平行列舉、量詞 scope 與符號密集段落的完整性。
- 只合回 §B.6 B3 那種真正節拍化的段落，不要為消除 `+6` 而機械重黏。

---

## 追加：2026-07-25 合併設計審查（同日第二次調用）

- 調用：`codex exec -s read-only`，材料＝合併提案（四份實測證據＋三層設計）＋ CONTENT_SPEC §3／§8 現行原文 inline。
- 總裁決：**有條件通過合併**——先鎖定共同分母與目標、把對稱插入語仲裁寫成決策序、把來源與 LaTeX 產物恢復為同一個原子發布單位。
- 關鍵改判（具約束力，已執行）：**A10 應 REVERT**——`— far more often —` 是同一主張的頻率修飾、無第二論述動作，改成逗號「沒有換來可理解性」；A13 維持整句 FIX（理由改為「不能逗號化，須依動作數重寫」）；`— only then —` 預設 KEEP，不得為一致性而動。
- 其餘裁決全數落實於 `CONTENT_SPEC.md` §3「成對破折號與標點負載」與 `PROSE-AUDIT-RUBRIC.md` F4：四步仲裁決策序、canonical prose stream 定義、兩指標共用分母、`T_can` 重新校準（不下修到 0.3–0.5）、不換 tic 護欄補「成對逗號」與顯著門檻（raw ≥+3 且密度 ≥+0.5/1000）、原因標籤、固定執行序、兩閘不可互相豁免、N<1000 報 raw、排序改以超額件數而非密度。
- 整合紀錄：`REVIEW-merge-dedash-plain-proposal.html`（提案）＋本輪 commit body。

### raw 輸出（照登）

結論：應合併，但要採「同一走查、兩個不可互相豁免的閘門」，不能把密度目標變成逐句改寫的裁決器。

### Q1

三層合併成立。較佳切法是：

- §3 放正式政策、仲裁決策序、量測定義與目標。
- §8 保留字元排印規則，em dash 僅一行指向 §3。
- 報告保留完整基準數字、例庫與 rollout 帳本；不要把會更新的實測表複製進 spec。

固定執行序應是：範圍／數學安全 → 論述動作判讀 → `CUT`／`KEEP` → 節級密度閘 → 不換 tic 檢查。

這樣不會稀釋紀律：逐例 `KEEP` 不能因為差幾個名額就被機械改成逗號；反過來，保留例也不能默默豁免密度。若仍超標，應找其他安全改點、重寫真正的多動作句，或明示節級例外，而非逐筆討價還價。兩份帳本可分開，但每個改點要共用 candidate ID 與原因標籤。

### Q2

擬議條文方向正確，但「多論述動作黏接句」未定義，還不夠可執行。建議改為：

> 成對 em dash 的節拍式插入語得保留，前提是移除插入語後主幹仍為一個教學動作，且插入語只修飾同一主張的程度、頻率、時點、必要條件或對比；它不得另行提出可獨立表述的定義、理由、例外、推論、指令或結論。必要條件加結論、公式說明、平行列舉仍可是一個動作。若讀者須分別處理兩個可獨立成立的教學動作，先重寫或分句；不得只把成對破折號換成逗號。

決策序：

1. 拿掉 `— Y —`，檢查 `X Z` 主幹是否仍文法完整、量詞與 scope 不變。
2. 問 `Y` 是否對脫離主幹後仍有獨立教學用途；有限動詞本身不是充分條件。
3. 若 `Y` 只是同一主張的修飾，保留成對 dash；若是另一步理由、域別結論、例外或指令，重寫整句。
4. 只有單破折號尾巴才進一般 `CUT` palette；不可用逗號作表面去 dash。

回裁：

- A10 應改判為 `REVERT`：`— far more often —` 是同一主張的頻率修飾，沒有可見的第二論述動作；改成逗號沒有換來可理解性。
- A13 維持 `FIX`，但理由是「不能逗號化，須依整句動作數重寫」，不是單純去 dash。`and over the integers you never can` 若構成另一個域別結論，就應拆開或重寫；若重寫後仍把兩步塞回一句，仍未結案。
- `— only then —` 不應為了一致性而動；預設 `KEEP`。只有宿主句確實是兩個獨立動作時才重寫。

### Q3

應建立唯一的 canonical prose stream，兩個 `/1000` 指標都只能用它的同一個 `N`。

| 範圍 | 主分母處置 |
|---|---|
| 正常段落、環境正文中的連續自然語言 | 納入 |
| 行內／display 數學，含 `\text{...}` | 全部排除 |
| 標題、`env-head`、導覽、目錄、註解、程式、隱藏文字 | 排除 |
| 清單、proof skeleton、表格、`figcaption` | 主分母排除，另列副表監測 |
| 連結可見文字 | 納入；URL／屬性不納入 |

以最終讀者可見產物為量測母體；來源端抽出的 stream 必須與產物端有相同雜湊。entity 依渲染器規則解碼一次：named、decimal、hex 中實際渲染為 `—` 的都計入；顯示為字面 `&mdash;` 的逸出文字不計。

tokenizer 也要版本固定，例如 Unicode 字母／數字串、內部 apostrophe／hyphen 視為同一 orthographic token。家族命中只能在同一 stream 內比對，不得跨被排除區塊。

`≤3/1000` 必須重新校準；不能用 ch07 的分母比例直接換算。重跑五本外部基準與已核准內部樣本後，才定 `T_can`。在此之前，舊的 3 只能是方向性遺留值，appB 的 2.0 也尚不是跨線可比的發布值。小於約 1,000 詞的單元應報 raw `n/N`，與鄰近單元合併後才作通過判定。

### Q4

不建議下修到 0.3–0.5。那是在模仿特定教材風格，不是品質底線；它會迫使合法的節拍插入語轉成冒號、括號或逗號 tic，正好重演 appB 的問題。

建議保留「約 CLP／人類上緣、但不超標」的目標意圖，待 canonical 重跑後定精確數字。appB 達 2.0 證明目前方向已足夠嚴格，並不構成再壓低目標的理由。

### Q5

最主要的風險與補件：

- 一輪多面向失去歸因：每筆須標示 `DASH-CUT`、`DASH-KEEP`、`PLAIN-SPLIT`、`TIC-REBALANCE` 等原因；報告同時列 raw count、`N`、密度與各標籤貢獻。
- `reverse-apply == HEAD` 仍可行，但只能證明已記錄 patch 可逆，不能證明量測正確、沒有漏項或 source／dist 同步。重疊改點必須先合成一個從 `HEAD` 到最終文字的 patch。
- appB 的產物脫鉤必須先補齊。每節應先完成來源交易式套用，再跑 `convert.py → make_dist.py` 三閘、做來源／產物 prose-stream parity，最後才量測與 commit。
- 不換 tic 護欄漏了逗號。總 comma rate 太吵，但應另報「成對逗號插入語」；並預先定義「顯著」，例如 raw 至少 `+3` 且密度至少 `+0.5/1000` 才強制填理由。
- appD 顯示不能只掃 literal `—`。測試 fixture 至少要含 named／decimal／hex entity、逸出 entity、`--`／`---`、LaTeX 等價表示、數學巢狀、導覽重複文字與屬性文字。
- 排序應先處理量測與同步 blocker；其餘以「超額 dash 的原始件數 `max(0, n - T_can·N/1000)`」加上加權 plain 未解項與讀者曝露量排序，不要只看密度。

ch07 適合作為量測鎖定後的首個整合 pilot：dash 數一致但分母衝突，正好驗證新抽取器；但在分母問題未解前，不應先動內容，也不能僅靠 17.2 的舊值證明它比 appA 更優先。Mode A 可納入，但 brief 與完稿自檢必須呼叫同一支 canonical script。

### Q6

總裁決：有條件通過合併——先鎖定共同分母與目標、把對稱插入語仲裁寫成決策序，並把來源與 LaTeX 產物恢復為同一個原子發布單位。

合併前必須先完成三件事：

1. 定版 canonical extractor、補 entity 回歸測試、重跑所有基準並解掉 ch07／appD 量測差異。  
2. 寫入仲裁決策序與先例：A10 `REVERT`、A13 維持整句 `FIX`、`— only then —` 預設 `KEEP`。  
3. 重出 appB `dist`，建立含 tic guard、prose-stream parity、全 patch reverse-apply 的交易式發布流程。
