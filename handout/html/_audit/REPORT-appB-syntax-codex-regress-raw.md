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
