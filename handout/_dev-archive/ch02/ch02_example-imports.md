# Ch 2 課文範例補充——import 紀錄（provenance／改作審計軌跡）

依 [`CONTENT_SOURCING.md`](../../CONTENT_SOURCING.md) §Provenance 與標記建立。
記錄 2026-06-22 import 的 6 筆 worked examples 之來源、授權、解材出處與改作差異，供日後覆核。
裁決＝核心 4＋選收 2 全收（使用者 2026-06-22「六題全部補上」）；候選稿見
[`ch02_example-supplement-review.html`](ch02_example-supplement-review.html)。

**解材出處三型：**
- **official**：題庫附完整官方 solution，本書版為其改寫（換語域／記號／合併）。
- **authored**：題庫只附最終答案或指示，solution 為本次撰寫。
- **recomputed**：依本書約定重算，結論與題庫官方解不同（需重點覆核）。

授權：CLP-1＝CC BY-NC-SA 4.0（逐檔檔頭）。全 NC 家族，可 remix 進掛 CC BY-NC-SA 4.0
的免費講義。六筆全部出自 CLP-1（首選來源）。

---

## §2.3（sec-2-3.html）—— 補 2（differentiability 失敗模式 ＋ 反向應用）

| 例號 | 來源 | 解材 | 改作差異 |
|---|---|---|---|
| Example 2.12 | `[source: CLP-1 §2.2 prob_s2.2 vertical-tangent remark + standard textbook example]` | **authored** | 填 L1-1：Definition 2.3 提「no vertical spike」但原僅 Example 2.11 示範 corner。本例以 \(f(x)=\sqrt[3]{x}\) at \(x=0\) 示範差商 \(1/h^{2/3}\to+\infty\) 的 vertical tangent（左右極限一致但無界，與 corner 的左右不等對比）。CLP-1 §2.2 有 \(\sqrt{1+x}\) 的 vertical-tangent domain remark 但無 cube-root 的完整 worked example；solution 為本次撰寫。**置位微調**：審核稿建議「Example 2.11 之後、Figure 2.3 之前」；改置於 corner 圖（Figure 2.3）＋V-shape 散文之後，使「corner 例＋其圖＋說明」維持為一個完整單元，再以本例作第二個失敗模式收尾（教學序更順、編號不變）。 |
| Example 2.13 | `[source: CLP-1 §2.2 prob_s2.2 "2006H piecewise x^2 / ax+b"]` | official | 填 L2-1（選收）：把 differentiability 定義反過來用——求常數 \(a,b\) 使 piecewise（\(x^2\) for \(x\le2\)、\(ax+b\) for \(x>2\)）處處可微。Step 1 用 Theorem 2.1（可微⇒連續）得 \(2a+b=4\)，Step 2 用左右導數相等得 \(a=4\)，故 \(b=-4\)。**改作**：CLP-1 官方解直接引已知 \((x^2)'=2x\)；本書 §2.3 尚未正式介紹 differentiation rules（§2.4 才有），故 solution 改以「difference quotient 一行得出 \(2x\)（the same technique used in §2.2 Example 2.6）」＋引用 Theorem 2.1，而非 CLP-1 的 Lemma 引用。**回歸審核 advisory 修正**：初稿曾寫「by the limit definition of §2.2 is \(2x\)」，稽核指出 §2.2 僅從定義算過 \(x^2+4x-2\)、\(\sqrt{x}\)、\(1/x\)，未算過 bare \((x^2)'=2x\)；改為「follows in one line from the difference quotient（the same technique used in §2.2 Example 2.6）」，不再 overstate §2.2 字面所立。置於 Theorem 2.1 的 Caution 之後（此例正是 Theorem 2.1 的應用），先於 Higher derivatives 小節。 |

## §2.4（sec-2-4.html）—— 補 2（power rule 的負／分數指數）

| 例號 | 來源 | 解材 | 改作差異 |
|---|---|---|---|
| Example 2.16 | `[source: CLP-1 §2.6 prob_s2.6 "s(t)=3t^4+5t^3-1/t"]` | official | 填 L1-2：Caution 說 power rule 對負整數指數亦成立，但原 Example 2.15（多項式）只用正整數次方。本例把 \(1/t\) 改寫為 \(t^{-1}\) 再套 power rule，得 \(s'(t)=12t^3+15t^2+1/t^2\)，並回扣 §2.2 Example 2.8 的 \((1/x)'=-1/x^2\)。官方詳解改寫。置於 Example 2.15 之後、exponential 小節之前。 |
| Example 2.17 | `[source: CLP-1 §2.4 prob_s2.4 "f(x)=3x^2+4x^(1/2)"]` | official（tangent-line 部分為本書新增） | 填 L1-2（延續）：補分數指數 \(4\sqrt{x}=4x^{1/2}\)，得 \(f'(x)=6x+2/\sqrt{x}\)，回扣 §2.2 Example 2.7 從定義得的 \((x^{1/2})'=1/(2\sqrt{x})\)。**改作**：原題僅要求 differentiate；本書加上 \(x=1\) 處切線（\(y=8x-1\)）以回扣 §2.1 的核心技能，使一例服務兩個教學目的。原 \(f'\) 不變。**回歸審核 advisory 修正**：初稿對 \(x^{1/2}\) 直接「apply the power rule」未加保留，但同節 Caution 已將「一般實指數 power rule」延後至後章（需 chain rule）；稽核指此與該節自身 Caution 內部矛盾（對照 Example 2.16 對負整數例有引 Caution）。改為明點「\(\tfrac12\) 非整數＝Caution 所延後者，但此特例已由 §2.2 Example 2.7 從定義立得」，再以 power-rule bookkeeping 作呼應，化解矛盾且仍示範分數指數的 power-rule 形式。 |

## §2.5（sec-2-5.html）—— 補 2（quotient rule 辨錯 ＋ 指數型）

| 例號 | 來源 | 解材 | 改作差異 |
|---|---|---|---|
| Example 2.21 | `[source: CLP-1 §2.6 prob_s2.6 Conceptual Q1 "spot the error: 2x/(x+1)"]` | official | 填 L2-3：§2.5 第三個 Caution 點名「swapping the order flips the sign」是最常見的 quotient-rule 錯誤，但無以辨錯為核心任務的 example。本例給一份含 sign 錯誤＋化簡錯誤的學生計算，要求找出並糾正，正解 \(2/(x+1)^2\)。官方詳解改寫。**改作**：審核稿用 \(\color{red}{-}\) 標紅減號；改以散文「carries a <em>minus</em> sign … but the student wrote a plus」陳述（避免在列印數學式內用 `\color`，與既有 fragment 風格一致），數學完全相同。置於 Example 2.20（首個 full quotient 例）＋其圖之後。 |
| Example 2.23 | `[source: CLP-1 §2.7 prob_s2.7 Procedural "f(x)=e^x/(2x)"]` | official | 填 L2-3（延續，選收）：把 \(e^x\) 放在分子、多項式放在分母（與 Example 2.22(c) 的 \(x^2/e^x\) 相反方向），得 \((x-1)e^x/(2x^2)\)，並讀 \(f'\) 的正負定增減（\(x=1\) 變號）。官方詳解改寫。置於 Example 2.22 之後、§2.5 收尾散文之前。 |

---

## 編號位移總表（kit 無自動編號，手動稅）

- **Examples**：原 17 個（2.1–2.17）＋新 6 個＝23 個（2.1–2.23）。位移對照：
  - §2.3：插 2.12（vertical tangent）、2.13（piecewise）；舊 2.12（higher deriv）→ 2.14。
  - §2.4：舊 2.13 → 2.15；插 2.16（neg exp）、2.17（frac exp）；舊 2.14 → 2.18。
  - §2.5：舊 2.15 → 2.19、舊 2.16 → 2.20；插 2.21（error-spotting）；舊 2.17 → 2.22；插 2.23（quot×exp）。
  - 各 `sec-*.html` 檔頭註解已同步更新編號 ledger。
- **prose 交叉引用**：grep 確認所有既有 example 引用均指向 2.1–2.11（未位移之 §2.1／§2.2 例題），
  無任一引用指向被位移的例題，故**無連帶 prose 改動**。新例的引用（2.12→Example 2.11；
  2.16→§2.2 Example 2.8；2.17→§2.2 Example 2.7）均解析正確。
- **不位移**：所有 definition/theorem/corollary/remark/caution/strategy 編號（未插入此類環境）。
  Theorem 2.1–2.7、Corollary 2.1、Remark 2.5–2.6、Strategy 2.2、Figure 2.3–2.4 等 prose 引用維持正確。
- **不新增圖**：六筆均無附圖（不增 `data-fig`／FIGS）。

## 渲染驗證（2026-06-22，print standalone，Preview MCP）

`python build.py ch02` 重生 `chapter2-print-standalone.html` 後：23 examples 全渲染、
6 個 `data-fig` 圖全 hydrate（含 SVG）、**0 MathJax 錯誤**、0 未渲染 \(\backslash(\)／\(\backslash[\)、
0 console error。新增六例之散文內容逐一目視確認在位；被位移之六例內容保持原樣（僅編號更動）。

## 回歸審核（regression audit，2026-06-22，唯讀對抗式覆核）

import 後跑一輪 read-only 對抗式稽核（6 個數學覆核 agent 各獨立重推一例＋1 個編號／交叉引用完整性 agent）：

- **數學：6/6 全部 `final_answer_correct` ＋ `all_steps_valid`**——無計算錯誤。
- **完整性：clean**——編號 2.1–2.23 連續、無重複、無 dangling 交叉引用、被位移六例內容一致。
- **兩條 advisory（內部一致性，非數學錯）已修並回歸覆核 RESOLVED：**
  1. Example 2.13：左導數歸因 overstate §2.2（見上表）→ 改 difference-quotient 歸因。
  2. Example 2.17：分數指數套 power rule 與同節 Caution 內部矛盾 → 加延後保留＋§2.2 Example 2.7 立論。
  兩例修正後各重跑一輪稽核，確認「finding 已解、未引入新缺陷、數學仍正確」。
- **外部 Codex 選題稽核（2026-06-22，補跑）：`clean`（0 blocking／0 advisory）。** `codex exec`
  唯讀、走 ChatGPT 訂閱、`gpt-5.5 @ xhigh`、自讀 5 個 fragment 獨立審四維（math／faithfulness／
  aptness／source-license）。內部 agents 與外部 Codex 兩條獨立路徑一致 clean。詳見
  [`ch02_example-supplement-audit.md`](ch02_example-supplement-audit.md)。
