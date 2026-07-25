# Codex gate-2 raw：ch01 散文平實化回填（合併 sweep）逐條裁決

- **調用**：`codex exec -s read-only`（stdin 餵 UTF-8 prompt、`--output-last-message` 收檔；材料**全 inline**、未讓 Codex 讀檔——遵循 2026-06-28 編碼坑紀律），codex-cli 0.144.1，模型走 `~/.codex/config.toml` 預設 **gpt-5.6-terra**。
- **日期**：2026-07-25。**授權**：使用者本輪明示「跑 Codex Gate 2」（`CLAUDE.md` 2026-07-01 Codex 唯讀逐次徵詢條款）。
- **受審材料**（prompt 92.9 KB）：gate-1 走查的 42 條改點（前→後全句）＋ `CONTENT_SPEC.md` §3〈平實英文條款〉RC 條款節錄 ＋ `PROSE-AUDIT-RUBRIC.md` 四維度與擋稿線 ＋ ch01 provenance 背景（手稿 vs LLM）＋「刻意未改」清單 ＋ 本輪範圍五節的**完整散文**（逐段標手稿／LLM）＋ Q1–Q6。
- **走查稿**：[`REVIEW-ch01-plain-walk.html`](REVIEW-ch01-plain-walk.html)；**整合裁決與執行結果**：[`REVIEW-ch01-plain-applied.html`](REVIEW-ch01-plain-applied.html)。
- 本檔為 **raw 輸出照登**（未刪改一字）。折入時的逐條處置（含兩處我未完全照抄 Codex 措辭的理由）記在 applied 報告 §3 與該輪 commit body。

**摘要**：`VERDICT: ADOPT 34 / MODIFY 7 / REJECT 1`。最終執行 41 條（R3 依 REJECT 撤回；A4／D2／E6／E9／E12／E13 依 MODIFY 改稿，其中 A4／E6 我保留了 Codex 版本刪掉的承重內容，理由見 applied 報告）。Codex 另抓到一個**本輪範圍外的數學不精確**（S2 的 `arccos` 端點），已列為待裁決項。

---

VERDICT: ADOPT 34 / MODIFY 7 / REJECT 1

A2 ADOPT — 將插入釋義收回主幹，完整保留反向操作的意義。  
A3 ADOPT — 讓步子句改用逗號，語意與 scope 不變。  
A4 MODIFY — 方案仍用較不字面的 `reads as`；改為：For \(f\), the question is “given the input \(x\), what is the output?” For the inverse function, the question is “given that output, which input produced it?”  
A5 ADOPT — 對數函數的定義與其圖形是兩個可分開讀取的教學動作。  
A6 ADOPT — `why` 與 `how` 同為 `illustrates` 的受詞，逗號處理恰當。  
A7 ADOPT — 正根與 \(x \ge 0\) 的因果條件均完整保留。  
A8 ADOPT — 將操作順序直接字面化，橋接功能仍在。  
A9 ADOPT — 冒號引出名詞性結果，不拆散數學結論。  
B1 ADOPT — 前瞻的導數事實與 principal ranges 的作用可清楚分句。  
B2 ADOPT — `such as` 是例示同位語，逗號足夠。  
B3 ADOPT — 後段是鬆散的比較同位語，改逗號不損教學節奏。  
B4 ADOPT — principal value 與物理時間域是兩個獨立判讀。  
B5 ADOPT — 術語先就地釋義，再說明後續 domains，結構清楚。  
B6 ADOPT — 分支慣例造成差異與採用明示慣例的理由均保留。  
R8 ADOPT — `honest reciprocals` 是不必要的人格化，`really are` 較直白。  
R9 ADOPT — `puts to work` 是慣用語，`uses` 更可預測。  
P1 ADOPT — 前半建立倒數關係，後半推導恆等式；斷段合理且銜接完整。  
S1 ADOPT — 指令與 principal-value interval 的釋義分開後更易首次閱讀。  
S2 MODIFY — `negative inputs ... always do` 錯含 \(x=-1\) 的端點；改為：The principal value \(\arccos(-\tfrac{1}{2})\) lies in the <em>second</em> quadrant. More generally, \(\arccos x\) lies in that quadrant for \(-1 < x < 0\); \(\arccos(-1)=\pi\) is the endpoint of the principal range.  
C2 ADOPT — 選曲線與移動單點是連續但可獨立執行的作圖步驟。  
C3 ADOPT — 視覺描述後接字面的值域振盪理由，拆分有助理解。  
C4 ADOPT — 短對比改逗號自然，不改變全稱條件。  
C5 ADOPT — \(\tfrac00\) 的來源與約分後可處理的結論均仍明說。  
R1 ADOPT — `sidesteps` 的迴避隱喻改為直接說明定義不談 \(f(a)\)。  
R2 ADOPT — `close the loop` 改成可明確指涉的先前問題。  
D1 ADOPT — 重排後仍完整傳達「不決定極限」與「通常須代數化簡」。  
D2 MODIFY — 方案仍把 \(\tfrac00\) 形式本身說成可「equal anything」；改為：Thus, when direct substitution gives the indeterminate form \(\tfrac{0}{0}\), the limit may be any number, may be infinite, or may fail to exist, depending on the functions. This is why the form is called indeterminate and why we must simplify before deciding.  
E1 ADOPT — 具體的 chain-rule 前瞻資訊值得獨立成句。  
E4 ADOPT — 類比中的問題與 \(\delta\) 作為輸入容差的答案分開，清楚。  
R3 REJECT — `promise` 已由後面的字面條件立即解開；換成 `requirement` 沒有 R1/R2 證據，且把保證語氣改成約束語氣。  
E5 ADOPT — \(\varepsilon\) 的角色改為字面說明，挑戰—回應類比仍受明示保護。  
E6 MODIFY — 方案主要把 dash 換成括號，量詞順序的說明仍不夠字面；改為：First, the order of the tolerances is reversed. The definition must begin with “given any \(\varepsilon > 0\),” and then state that there is a corresponding \(\delta > 0\). The attempted version instead lets \(\varepsilon\) depend on \(\delta\).  
E7 ADOPT — 逗號引出否定對比，蘊含方向沒有改變。  
E8 ADOPT — \(\varepsilon=\tfrac{|L-M|}{2}\) 的理由被提升為完整句，未改其證明角色。  
E9 MODIFY — 方案刪掉尾巴，卻保留 `borrowed inequality did all the work` 的隱喻；改為：The given inequality already provides the necessary bound, so no factoring or separate auxiliary bound is needed.  
E10 ADOPT — 形式證明與先前非形式論證的對照清楚。  
E11 ADOPT — one-to-one 的字面定義與 horizontal line test 的圖形讀法應分開。  
R5 ADOPT — `could hardly look less alike` 是高風險否定式慣用語，改寫合理。  
R6 ADOPT — `pinned down` 改為 `described exactly`，語意精確。  
E12 MODIFY — 冒號後是完整的 `means that ...` 定義子句，不能視作純公式引出；改為：We began with the informal idea that \(\lim_{x \to a} f(x) = L\) means that \(f(x)\) is as close to \(L\) as we please once \(x\) is close enough to, but not equal to, \(a\). We estimated such limits from tables and graphs (§1.3).  
R7 ADOPT — `gaps ... yield to` 屬不透明擬人搭配，`is handled by` 較直白。  
E13 MODIFY — 前半冒號後是完整的 continuity 定義子句，應改用句號；改為：The chapter closed by naming continuity, the property that limits make precise. A function \(f\) is continuous at \(a\) when \(\lim_{x \to a} f(x) = f(a)\). Chapter 2 is built on this machinery: the derivative is itself a limit, the limit of secant slopes.

Q1. 唯一 REJECT 是 R3，理由不是拆句。其餘拆分沒有把單一推論機械切碎；A4、E6 是需改寫得更字面，而非保留原 dash 節拍。

Q2. A7、C5、D1、E8、E11、E12、E13 均未拆散量詞、條件—結論或先行詞；A7 的正根仍由 \(x\ge0\) 限定，E12 的「但不等於 \(a\)」仍留在同一句 scope 中。例外是 S2 與 D2：原／建議文字各自保留了邊界錯誤與非字面說法，故須依上述版本收緊。

Q3. 你的重數不對。A9、B5 的冒號後確為名詞／同位語短語，不算；但 E12 的 `… means that …` 與 E13 的 `\(f\) is continuous … when …` 都是冒號後另起的完整定義子句，不能因含公式而排除。因此現案實際是 +4（C5、E11、E12、E13），約 +0.69/1000，仍觸發 guard。採用我的 E12、E13 版本後才會降為 +2（C5、E11）。沒有任何一句形成雙冒號。

Q4. 11 個 LLM 成對 dash 沒有一個應原樣 KEEP；它們承載的是定義、例子、理由或操作，而非單純程度／頻率修飾。E6 是唯一接近「表面換標點」者，故改為完整量詞順序說明。其引文在 dash 外作釋義，不是引號內的對白式停頓例外。

Q5. 九條中只有 R3 屬無證據的同義詞美化，應砍；E9 則需比原建議更完整地去除 `borrowed`／`did all the work`。其餘皆有明確的慣用語、人格化或不透明否定式證據。完整散文中沒有其他值得另報的 R1 finding；已明示的直覺類比、`trap/trapped` 與作者既有用語不應為湊數而報。

Q6. 清單整體正確。§1.1 的 150 詞 lead 是章節路線圖，非 F4 問題；Example 1.5 與 §1.2 開場各是一條連續推線，不必拆段。四個手稿成對 dash 依使用者裁決保留站得住：它們不是唯一語意載體，且 §1.6 最後一例直接符合目的／時點修飾的 KEEP 類型。§1.4 凍結、作者用語、FLAG 句式、`trap/trapped`、正式定義與平行列舉也都不應另報。§1.6 的 \(\varepsilon\)-\(\delta\) 動機、例子與正式定義相鄰，沒有 U blocking；§1.2 亦先給受限區間與具體 range，再以 S1／B5 就地解釋 principal range，沒有阻斷線性閱讀的 U4。
