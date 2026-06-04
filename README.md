# 微積分講義專案

一份單面 A4 的**微積分講義**，供準備銜接大學微積分的高中生自學使用，並搭配輔助教學影片。講義本身自給自足；影片是強化補充。

本檔案是**儲存庫樞紐（repository hub）**。它對儲存庫結構、preamble 結構與建置指令具有權威性。內容撰寫規則與媒體產線規則各自獨立成檔，連結列於下方。

---

## 從這裡開始

依你手上的任務，開啟對應的連結檔案。

- **撰寫或修訂章節。** 先看 [`CONTENT_QUICKSTART.md`](CONTENT_QUICKSTART.md)。當快速指南無法回答你的問題時，再回頭查 [`CONTENT_SPEC.md`](CONTENT_SPEC.md)。開始新的一章前，先看 [`CONTENT_ROADMAP.md`](CONTENT_ROADMAP.md)。
- **製作影片**（目前的主要路徑：第二代 Manim 產線）。先看 [`video/README.md`](video/README.md)，再看 [`video/DESIGN.md`](video/DESIGN.md) 了解分鏡契約與目前的模板決策。較舊的 `MANIM_*` 文件已封存於 [`legacy/`](legacy/)，保留作為第一代參考資料。
- **靜態投影片 MP4**（已凍結的舊路徑）。使用 [`legacy/LEGACY_SLIDE_PIPELINE.md`](legacy/LEGACY_SLIDE_PIPELINE.md)。此路徑不再有新開發——新工作請改用 Manim。
- **設計章末習題。** [`CONTENT_EXERCISES.md`](CONTENT_EXERCISES.md)（在完整設計回合開始前，僅為最小骨架）。

---

## 撰稿工作流程

各章源自**由不同老師撰寫的手稿**，他們彼此分工分攤了整本書。Claude 以三種不同的模式與這些手稿互動；規則因模式而異。動手前先確認模式正確。

這些模式構成一個小型狀態機，而非固定管線：

- **新手稿送達。** 執行 **Mode A**（草擬）。Mode A 從手稿產出一份教科書草稿，並以一次擴增稽核（amplification audit）作結。
- **Mode A 草稿，使用者簽核前。** **Mode B**（審訂審查）可作為一次「待審」稽核在草稿上執行。
- **簽核完成；章節提交至 `main`。** 在沒有使用者明確呼叫的情況下，不再執行任何模式。
- **一個已簽核的章節需要更多深度。** 執行 **Mode C**（充實增補回合）。Mode C 只增添，絕不重構。
- **Mode C 之後。** **Mode B 必須執行**，範圍限定於 Mode C 所產生的新 `[pass: enrichment]` 標記。

簡言之：A 草擬，C 對既有草稿做充實，B 稽核——B 是唯一作為另一模式後續而執行的模式。有效的轉移路徑為 A →（可選 B）→ 簽核 →（可選 C → 必要 B）→ ……。

### Mode A — 手稿轉教科書草擬（Claude 將新手稿轉成 LaTeX）

當使用者轉來一份手稿並要求 Claude 產出章節檔時，使用此模式。Claude 的職責：

1. 自使用者處接收手稿。
2. 依 [`CONTENT_SPEC.md`](CONTENT_SPEC.md) 與 [`CONTENT_QUICKSTART.md`](CONTENT_QUICKSTART.md)，將其轉成符合專案規範的 LaTeX，置於 `chapters/chNN_<slug>.tex`。
3. 在完整性或 Stewart／Rogawski 自學語域有助益之處，圍繞手稿加以擴充。下方的擴充政策說明哪些增添屬於政策範圍內，以及必須如何標記。
4. 更新 [`CONTENT_ROADMAP.md`](CONTENT_ROADMAP.md) 以反映手稿實際的決定，取代任何手稿到達前的暫定工作假設條目。

#### 手稿是主軸

每一個手稿主題、範例、註解、證明與圖示構想，都依手稿呈現的順序出現在章節中，並改寫為符合專案規範的 LaTeX。Claude **不**跳過手稿內容，**不**無故重排其順序，也**不**改寫其數學實質。擴充內容包裹在手稿內容之外；絕不取代手稿內容。

若某個重排或結構重組確實有用，請記錄在該章 roadmap 條目的 *Open questions* 之下，讓使用者可於審查時簽核。

#### 擴充政策——範圍寬鬆，但以標記呈現

Claude 可在未事先授權的情況下圍繞手稿擴充，條件是 LaTeX 原始碼中**每一處擴充都加上標記**，使事後審查可行。標記的形式為

```latex
% expansion:<category> [pass: <pass-id>] [source: <brief source>] — <one-line description>
```

置於擴充內容緊接的前一行。方括號提示各自為選用，但出現時須遵守嚴格規則：

- `<category>` 為必填，且須取自下方表格。
- `[pass: <pass-id>]` 標示是哪一個模式回合引入了該擴充。在 Mode A 中省略它——沒有 `[pass: ...]` 提示的 `% expansion:` 標記，視為 Mode A 原始草擬（標記本身仍為必要，只有 `[pass: ...]` 提示是選用）。在 Mode C 中**必填**，值固定為 `[pass: enrichment]`，使事後審查能區分原始草擬與後續充實。
- `[source: <brief source>]` 註明擴充所依據的參考來源。一般情況下選用；依下方「具名內容」規則，`history` 類具名內容**必填**，且任何正確性取決於特定參考的擴充均建議填寫。
- 當兩個提示同時存在時，**`[pass: ...]` 在 `[source: ...]` 之前**。順序固定，使 `book_style_lint` 能偵測格式錯誤的標記；順序錯誤的標記為 lint 錯誤。
- 未知的方括號鍵為 lint 錯誤——僅 `pass` 與 `source` 被承認。像 `[soure: …]` 這樣的錯字，否則會悄悄使該提示在審查中被剝除。

承認的類別（`book_style_lint` 檢查會強制此清單）：

| 類別 | 用途 |
|---|---|
| `history` | 數學史脈絡：概念如何發展、為何選用該記號 |
| `application` | 真實世界連結：物理、經濟、幾何、工程的關聯 |
| `formula` | 由手稿已證明或定義者推得的衍生恆等式／系理 |
| `summary` | 將一組範例或一個證明收束在一起的綜合段落 |
| `figure` | 手稿以文字暗示但未繪出的圖示構想 |
| `example` | 闡明手稿所引入技巧的補充 `workedexample` |
| `intuition` | 形式陳述前的動機段落，或一段 *Informally, ...* 的白話注解 |
| `strategy` | 提煉多個手稿範例共用方法的 `strategy` 方塊 |
| `caution` | 針對微妙限制、記號陷阱或常見錯誤的 `caution` 方塊 |

此類別清單刻意精簡；當出現一個值得長存的新類型時，在引入該新類別第一個標記的同一次提交中擴充此表，lint 便會自此接受它。

事後審查於是變成

```powershell
grep "^% expansion:" chapters/chNN_*.tex
```

——使用者一眼看盡每一處非手稿的增添，逐一標記決定*保留*、*改寫*或*移除*，無須將整章與手稿全文比對。

#### 具名內容：標上來源，不要自我審查

具名內容——特定歷史人物、日期、世紀、專名歸屬、具名結果——在草擬模式中是**允許的**。使用者已表明會在事後審查時手動查核姓名與日期，因此 Claude 的工作是在內容契合 Stewart／Rogawski 語域時納入它，並標上來源（或最接近的標準參考），使審查有效率。

格式：

```latex
% expansion:history [source: <specific source OR "standard calculus-textbook historical note">] — <description>
```

- 若 Claude 能指出特定來源（例如 *Stewart 8e §2.4 historical note*、*Rogawski 4e Ch 2*、*Wikipedia "History of calculus"*），就在標記中引用它。這讓使用者能對照單一處查核，而非猜測。
- 若內容是多數微積分書共有的常見教科書語域段落——牛頓／萊布尼茲的起源、十九世紀 ε-δ 的釐清、阿基米德與窮竭法——使用 `[source: standard calculus-textbook historical note]`，並簡述 Claude 所依據的內容。使用者會將此視為*「我會確認該主張並無爭議」*，而非*「我會去查某一特定頁面」*。
- **直接引文**仍需特定來源。逐字引用一位數學家是風險最高的子類；若無特定來源可用，請改用釋義而非引文。

精神：Claude 應傾向**納入**對教學有益的具名內容，而非為求保險而自我審查。標記使內容可被審查；來源標籤使審查有效率。自我審查產出單薄的章節；過度納入產出使用者在審查時能快速修剪的章節。前者的代價遠高於後者。

#### 擴充密度的校準

正確的密度目標是 **Stewart／Rogawski 自學教科書**，而非極簡的手稿翻譯。具體而言：

- 當多個 `example` 擴充能從不同角度闡明同一主要技巧時，是受歡迎的；
- 綜合性的散文（連接段落、總結結論、收束各條線索）應慷慨而非稀疏；
- 每一節開頭的歷史開場、應用關聯與直覺鋪陳是預設，而非例外；
- 針對標準陷阱的 `strategy` 與 `caution` 方塊是本書語氣的一部分。

在這次全新 Mode A 回合之前所提交的第一章（提交 `f701c02`）是有用的密度參考——那份由使用者撰寫的草稿，展現了所欲達到的豐富度。拿不準時，Claude 應傾向更多擴充（帶標記）而非更少。擴充不足比擴充過度更難事後補救，因為使用者在審查時隨時能刪除一處帶標記的擴充，卻鮮少在審查時親自補寫擴充。

#### 體量合理性檢查（軟性，不強制）

擴充對手稿的比例沒有硬性規定，只做一次自我檢查：若某一節的 `% expansion:` 標記多到使手稿內容淹沒在擴充之中、難以辨識，那就是某處飄移了。在該章 roadmap 的 *Open questions* 中標註，以便於簽核時檢視比例。否則，自由擴充。

#### 不重複規則：不同深度、不同切入

教學性的重複（一個關鍵概念在章首、節首與總結再度出現）是無妨的、且常有助益——但**唯有當每次再現都處於不同深度或以不同切入呈現時**。同深度的炒冷飯才是製造「我們剛剛不是讀過這個？」感受的元兇。四個具體機制可避免擴充彼此踩線：

1. **各類別的角色條款。** 每個擴充類別都有狹窄的職責，並明確迴避鄰近類別的職責：
   - **章節總覽**（`intuition`）：描述本章的脈絡——它發展哪兩三個主題、它們如何連結。**不**預告每一節將教什麼；那是學習成果清單與每節自己開場的職責。
   - **學習成果**（`summary`）：以動詞起首的可操作技能項目清單（*判斷*、*計算*、*應用*）。**不**解釋概念或給出其動機；那是內文的職責。
   - **節首開場**（`intuition` 或 `application`）：專為*這一*節做動機鋪陳，包括它如何承接上一節。**不**重述章節總覽，也**不**列出下一節將涵蓋什麼。
   - **Informally 白話注解**（`intuition`，置於 `definition` 內）：一句白話。**不**膨脹成動機段落、範例，或周圍定理的預告。
   - **Strategy 方塊**（`strategy`）：提煉同一節中已由兩個以上 worked example 示範過的方法。**不**重述 worked example 的散文；它只點出步驟。
   - **Caution**（`caution`）：一個特定陷阱或微妙限制。**不**重述它所附著的定義或定理；讀者就近仍有那些內容。
   - **總結**（`summary`，章末）：每個項目一行提醒（定義以其一句精要、定理以其條件與結論、公式以其裸恆等式）。**不**重新證明、重新推導或重新鋪陳動機。

2. **指向，不重述。** 當較早引入的概念再度出現時，使用明確的交叉參照（`\cref{sec:foo}`、*「如 §1.3 所介紹，……的極限」*）而非重述內容。交叉參照是誠實的：它表明「我們有這個，它在這裡」。重述是不誠實的：它假裝該概念是新的。

3. **深度分層的再現。** 同一概念可出現三次（章首、節首、總結），條件是每次出現處於不同深度：
   - 章首：一句話將概念安置於脈絡之中；
   - 節首：一段說明本節為何使概念更加精確；
   - 總結：一行提醒。
   同深度出現三次＝重複；不同深度出現三次＝螺旋複習。

4. **草擬收尾的自我檢查。** 章節草擬完成後，依序掃描每一個 `% expansion:` 標記後的第一句。若任兩個連續擴充以相同的主張或概念開頭，將其一收束為交叉參照。特別要掃描章節總覽對 §1 開場、各節開場對前一節結尾、總結項目對學習成果——那是三處最常溜進同深度炒冷飯的地方。

若一處擴充並沒有其他擴充尚未在做的職責，它就應該被改寫以劃出獨特角色，或被刪除。

#### Mode A 以一次擴增稽核作結

Mode A 回合並非在手稿轉成 LaTeX 後就算完成。在把章節交回之前，Claude 依下方的逐節檢查表逐節走查，並對每一個未滿足的項目，**要不補上缺口，要不在該章 roadmap 條目的 *Open questions* 中記錄這個刻意的省略**。這次稽核正是把一份排版好的手稿變成一份教科書草稿的關鍵；少了它，上述密度校準目標只是理想而非有效規範。

逐節檢查表（每一項都是*補上或記錄*——悄悄略過正是此規則存在要防止的事）：

1. **節首開場。** 該節是否以一段承接上一節或章節脈絡的動機段落開場？（`intuition` 或 `application`）
2. **定義注解。** 每個新定義在形式陳述之前，是否至少有一次白話注解或直覺鋪陳？（`intuition`）
3. **worked-example 密度。** 每個新技巧是否至少有一個超出手稿所提供的補充 `workedexample`？（`example`）——*當手稿本身已為每個技巧提供多個 worked example 時為例外；若適用，請在 roadmap 中記錄。*
4. **邊界情況或反例。** 該節是否包含至少一個邊界情況、反例，或顯示技巧何時失效的非範例？（`example` 或 `caution`）
5. **Caution 方塊。** 常見錯誤、正負號陷阱或記號陷阱是否被捕捉為 `caution` 方塊？（`caution`）
6. **Strategy 提煉。** 當該節有兩個以上範例共用一個方法時，該方法是否被提煉為 `strategy` 方塊？（`strategy`）
7. **視覺推理。** 受益於圖像的概念，是否至少由一個 `figure` 構想承載（素材本身可延後至媒體工作再做）？（`figure`）
8. **收尾綜合。** 該節是否以綜合性散文作結，將範例與定理收束回該節的標題結果？（`summary`）

任何一項給出*否*都是可接受的，前提是該刻意省略有被記錄——規則是**補上或記錄**，而非「每一節都必須拿 8/8」。在 roadmap 的 *Open questions* 中記錄省略，讓使用者能於簽核時同意、反駁，或補上缺失的部分；悄悄略過該項則會產生教科書密度目標所要防止的「翻譯講義」感。

#### 草擬模式中仍然禁止的事

- 跳過手稿內容（手稿是主軸）；
- 改寫手稿主張的數學實質（證明方法、變數選擇、定義形式）；
- 自創習題——習題庫來自手稿（見 [`CONTENT_EXERCISES.md`](CONTENT_EXERCISES.md)）；
- 未標記的擴充——每一處非翻譯的增添都要加上 `% expansion:` 標記；
- 違反上述「具名內容」防護欄的具名內容。

補上手稿省略的證明是個邊界案例：依 [`CONTENT_SPEC.md`](CONTENT_SPEC.md) §5，證明為選用且預設省略。當證明簡短、標準且具闡明性時，Claude **可**將其作為 `expansion:formula`（簡短推導）或 `expansion:example`（worked case）加入；多頁的證明，或需要章節尚未引入之材料的證明，則需使用者明確授權。

### Mode B — 審訂審查（Claude 稽核既有內容）

當 Claude 被要求對照手稿、規格或目前草稿狀態來稽核既有章節內容時，使用此模式。依上方的工作流程狀態機，Mode B 有三個有效的進入點：

- 一份 Mode A 草稿，使用者簽核前（待審稽核）；
- 一個已提交至 `main` 的章節（週期性的規格合規或正確性審查）；
- 一次 Mode C 充實回合的產出（**必要**的後續，範圍限定於新的 `[pass: enrichment]` 標記）。

**已提交的內容即已授權的內容。** 使用者已對落入 `main` 的內容簽核；Claude **不得**僅因某些超出手稿的既有擴充未逐字見於手稿，就將其視為「幻覺」——使用者很可能是在原始草擬回合中自己撰寫了該擴充。

#### 逐標記裁決（Keep／Rewrite／Move／Cut）

對帶有 `% expansion:` 標記的章節，Mode B 走查檔案中每一個標記，並指派四種裁決之一。裁決**逐標記回報給使用者**；Claude 不會擅自據以行動。

| 裁決 | 含義 | Claude 的作為 |
|---|---|---|
| **Keep** | 正確、位置適當、語域契合 Stewart／Rogawski、未與鄰近擴充重複。 | 記為 Keep；不做變更。 |
| **Rewrite** | 方向正確但執行需要改善——語域滑落、與鄰近者冗餘、措辭笨拙、正確性的小瑕疵。 | 就地提出改寫，讓使用者能接受或再修。 |
| **Move** | 內容有價值但該放別處——較前的節、章末總結、改用 `strategy` 方塊而非 `example`，甚至放到一個能有適當鋪陳的後續章節。 | **僅提議。** 描述該搬移，不要執行它。 |
| **Cut** | 正確但在此處不承載教學重量——與鄰近者同深度重複，或重述內文已清楚說明的內容。 | 提議刪除，附一句說明理由。 |

**`Move` 是僅提議。** 這是最容易被誤用的裁決。一次 Mode B 回合若以「搬移」為名悄悄跨節重置擴充，便破壞了稽核的目的：每一次跨節重構都是使用者必須親自落實的結構決定。即使在單一節之內，改變順序或環境類型（例如 `example` → `strategy`）的搬移也是提議，而非行動。

當 Mode B 作為 Mode C 的必要後續而執行時，將裁決回合的範圍限定於新的 `[pass: enrichment]` 標記——原本的 Mode A 標記已在簽核時稽核過，再次稽核它們只會招致無謂的變動。

#### 其他 Mode B 發現（與裁決並行）

獨立於逐標記裁決之外，Claude 另行標示：

- **規格合規**——對照 [`CONTENT_SPEC.md`](CONTENT_SPEC.md) 的規則違反：不允許的顯示輔助巨集、散文中的 `\textbf`／`\textit`、ASCII 引號、手動交叉參照前綴、章節檔中的 `\newcommand`、缺少章節開頭結構等。這些是明確的缺陷；提出修正。規格合規也包含**需要章內交叉比對的模式層級規則**——例如，章內所有定義是否一致遵循 §3 的注解決策規則、所有圖是否遵循 §10 的擺放規則、平行結構（份量相近的定義、形式相近的命題）是否格式一致。單行 lint 掃描是必要但不充分的；模式層級的稽核需要明確走查每一條帶有決策準則的 SPEC 規則，並就整章加以檢查。
- 相對於手稿的**記號飄移**——例如手稿用 `[x]` 而 `.tex` 悄悄用了 `\lfloor x \rfloor`。將此作為一個問題提給使用者，而非作為幻覺。使用者可能是有意升級了記號，或可能想重新對齊回手稿。
- **數學正確性**——若某陳述看似有誤，將其作為*「請查核 X」*提出，而非*「我因為 X 不在手稿中而移除它」*。
- **手稿中缺漏的內容**——若手稿涵蓋了某主題而 `.tex` 跳過了，標示這個缺口，讓使用者能決定該省略是否為有意。
- **結構決定**——分節、定理命名及類似的編輯抉擇。作為問題提出；不要擅自變更。

#### Claude 在 Mode B 中不得做的事

- 預設將 `.tex` 中手稿沒有的內容視為幻覺；
- 以缺乏手稿依據為由，悄悄移除或改寫使用者撰寫的擴充；
- 對 `Move` 裁決據以行動——`Move` 永遠僅提議，單一節之內亦然；
- 在未先詢問歷史註解、額外 worked example 或額外註解是使用者撰寫的擴充還是草擬模式的幻覺之前，就提議刪除它們；
- 當進入點為 Mode C 後續時，去稽核沒有 `[pass: enrichment]` 的 `% expansion:` 標記——那些不在該回合的範圍內。

Mode B 中的關鍵問題是*「這段內容是否正確、合規、位置適當？」*——而非*「這段內容是否在手稿中？」*。唯有在 Mode A 中，第二個問題才承載重量。

### Mode C — 充實增補回合（Claude 為已簽核的章節增添深度）

當一個已簽核的章節將受益於額外的教科書深度，且使用者明確要求 Claude 充實它時，使用此模式。Mode C 之所以存在，是因為「放大一個章節」的自然時機是*在*手稿主軸於簽核時定下*之後*，而非重新進入 Mode A 並冒著改動主軸本身的風險。

#### Mode C 可以做的事

- 加入 `intuition`、`example`、`figure`、`caution`、`strategy`、`application`、`formula`、`history` 或 `summary` 擴充，每一處的標記方式與 Mode A 完全相同（`% expansion:<category> …`），**但帶有必要的 `[pass: enrichment]` 提示**，使事後審查能區分原始草擬與充實；
- 以 Mode A 所用的同一份逐節擴增稽核作結——依檢查表逐節走查，補上現在可見的任何缺口，或在 roadmap 的 *Open questions* 中記錄缺口。這次稽核正是使 Mode C 成為一次充實回合、而非零散補強的關鍵。

#### Mode C 不得做的事

- 改動手稿的主軸：不重排各節、不改寫定義或定理陳述、不取代或刪除既有擴充（那些是 Mode B 的 `Move` 與 `Cut` 裁決，且維持僅提議）；
- 加入沒有 `[pass: enrichment]` 的 `% expansion:` 行——那假裝該增添是原始草擬，並污染稽核軌跡；
- 作為最後一個步驟而執行。每一次 Mode C 回合**都必須接著一次範圍限定於新 `[pass: enrichment]` 標記的 Mode B 稽核**。上方的狀態機在這一點上不容妥協：一次未接 Mode B 後續就出貨的 Mode C 回合是不完整的。

不重複規則、具名內容規則與密度校準目標，皆與 Mode A 一樣適用於 Mode C——Mode C 唯一改變的是標記提示，以及禁止觸碰既有主軸。

### 當手稿與規格相牴觸時（適用於任何模式）

- **格式**：[`CONTENT_SPEC.md`](CONTENT_SPEC.md) 勝出。改寫手稿的措辭以求合規（例如散文中 `\textbf{...}` → `\emph{...}`、ASCII 引號 → TeX 引號、手動交叉參照前綴 → `\cref{}`）。數學內容不變。
- **數學內容**：手稿勝出。若手稿以特定方式證明一個定理，保留該方法；若手稿以特定形式定義一個詞，保留該形式。與規格 §9 的記號差異，以 `caution` 註解（若調和並非無關緊要時）調和為本書慣例。
- **真正的衝突**（手稿堅持一條規格基於編輯理由而非數學理由所禁止的規則）：詢問使用者。將決定記錄在該章 roadmap 條目的 *Open questions* 之下。

逐章手稿追蹤——誰寫的、何時收到、轉換狀態,以及任何使用者撰寫的擴充註記——存於 [`CONTENT_ROADMAP.md`](CONTENT_ROADMAP.md) 中每一章條目的 **Manuscript source** 之下。

---

## Golden path（黃金路徑）

目前的影片工作位於 `video/` 下的第二代產線：

```text
chapters/*.tex  -->  video/storyboards/<section_id>.yml
                  -->  video/pipeline/build.py silent previews
                  -->  video/output/...
```

下方較舊的 `legacy/inputs/manim_storyboards` / `legacy/artifacts/video` 路徑（已封存於 `legacy/`）保留作為第一代參考資料，並非目前的活躍開發路徑。

```
  chapters/*.tex  ──▶  inputs/manim_storyboards/<deck_id>.yml
  (CONTENT_SPEC)      (MANIM_STORYBOARD + MANIM_REFERENCE)
                                   │
                                   ▼
                         preview → audio → render
                         (MANIM_CHECKLIST)
                                   │
                                   ▼
                       artifacts/video/<deck_id>_manim.mp4
```

先定稿章節內容。再從定稿的 LaTeX 手寫分鏡。逐一預覽場景。待場景感覺對了，再產出音訊與最終 MP4。

---

## 文件地圖

| 層級 | 檔案 | 用途 |
|---|---|---|
| 樞紐 | `README.md` | 儲存庫結構、preamble 對照、建置規則 |
| 內容規格 | [`CONTENT_SPEC.md`](CONTENT_SPEC.md) | 權威性的教科書撰寫規則 |
| 內容日用 | [`CONTENT_QUICKSTART.md`](CONTENT_QUICKSTART.md) | 1–2 頁的作者速查表 |
| 內容脈絡 | [`CONTENT_ROADMAP.md`](CONTENT_ROADMAP.md) | 章節順序、先備知識、各章核心技能 |
| 內容習題 | [`CONTENT_EXERCISES.md`](CONTENT_EXERCISES.md) | 最小習題骨架 |
| 影片產線 | [`video/README.md`](video/README.md) | 目前第二代 Manim 產線的狀態、指令、交接註記 |
| 影片設計 | [`video/DESIGN.md`](video/DESIGN.md) | 目前的分鏡契約、場景種類、模板決策 |
| manim v1 操作 | [`legacy/MANIM_CHECKLIST.md`](legacy/MANIM_CHECKLIST.md) | 第一代參考檢查表（已封存） |
| manim v1 參考 | [`legacy/MANIM_REFERENCE.md`](legacy/MANIM_REFERENCE.md) | 第一代欄位契約、模板、render 指令（已封存） |
| manim v1 方法論 | [`legacy/MANIM_STORYBOARD.md`](legacy/MANIM_STORYBOARD.md) | 第一代 LaTeX 轉 YAML 翻譯手冊（已封存） |
| 凍結舊版 | [`legacy/LEGACY_SLIDE_PIPELINE.md`](legacy/LEGACY_SLIDE_PIPELINE.md) | 靜態投影片／PDF + TTS + MP4（已封存，不再有新開發） |
| 封存總覽 | [`legacy/README.md`](legacy/README.md) | gen-0／gen-1 凍結產線的封存索引與還原說明 |

---

## 儲存庫結構

- `main.tex` — 全書的 LaTeX 進入點。
- `chapters/` — 章節源檔。
  - `chapters/_chapter_template.tex` — 新章節的起始骨架。
  - `chapters/_scratch.tex` — 選用的本機暫存章節，由 `\ifincludescratchchapter` 控制。
- `preamble/` — 共用的 LaTeX 設定（見下方 *Preamble 對照*）。
- `preamble_smoketest.tex` — 僅供 preamble 版面檢查的最小回歸文件。
- `refs/` — 參考書目資料。
- `tools/` — 書籍源碼工具（`book_style_lint.py`、`book_preamble_smoketest.py`、`book_docs_lint.py`）。第一代媒體產生腳本已封存至 `legacy/scripts/`。
- `legacy/` — 已封存的凍結媒體產線（gen-0 投影片、gen-1 Manim 及其橋接實驗）：`legacy/scripts/`（腳本）、`legacy/MANIM_*.md` 與 `legacy/LEGACY_SLIDE_PIPELINE.md`（方法論文件）、`legacy/schemas/`、`legacy/inputs/`、`legacy/artifacts/`（gitignored 的大型算繪輸出仍存於磁碟，git 追蹤的例外為 narration／final／tex）。詳見 [`legacy/README.md`](legacy/README.md)。
- `.github/workflows/` — CI 檢查。

額外的活躍媒體工作區：

- `video/` — 目前第二代 Manim 課程影片產線，包含分鏡、可重用模板、設計註記，以及 gitignored 的預覽輸出。

---

## Preamble 對照

`preamble/` 依職責拆分，使版面與模板行為可被快速找到：

- `preamble/packages.tex` — 套件載入：Times 內文／數學字型（`newtxtext` + `newtxmath`）、`microtype`、`amsmath` / `amsthm` / `mathtools`、`graphicx` / `tikz` / `pgfplots`、`float` / `flafter`、`needspace`、`enumitem`、頁面幾何（3.3 cm 邊界）、headers、`hyperref` / `cleveref`、為 `caution` / `strategy` 而設的 `mdframed`（`framemethod=TikZ`）、`xcolor`，以及本書的反三角運算子（`\arccsc`、`\arcsec`、`\arccot`）。
- `preamble/colors.tex` — 三角色語意調色盤（`colorprimary` 藍、`colorcaution` 紅、`colorauxiliary` 灰），驅動圖示以及 `caution` / `strategy` 上的強調色條與其同色淺底（`colorcautionbg`／`colorprimarybg`，各為 7% 淡化）。
- `preamble/layout.tex` — 段落縮排與間距、清單間距、全域 `\linespread{1.05}`、浮動體擺放、running headers 與 footers、`\Needspace` 掛勾、共用的短公式輔助巨集（`aligneddisplay`、`conditiondisplay`、`\pairdisplay`），以及供任何 `\[...\]` 包裝器使用的 `\newdisplayenv{name}{begin}{end}`（透過 `\AfterEndEnvironment` 安裝核心 `\@doendpe` 掛勾，以抑制環境後的多餘縮排）。
- `preamble/theorem_setup.tex` — `definition` / `theorem` / `proposition` / `corollary` 的逐環境、章內計數器；`solution` 環境；`caution` 與 `strategy`（左側色條的 `\newmdtheoremenv`）；頁面流保護掛勾；以及將 `example` + `solution` 一對作為單一單元保留空間的 `workedexample` 語意包裝器。
- `preamble/numbering.tex` — 依章編列方程式編號。
- `preamble/bibliography.tex` — 參考書目後端與來源檔案。

---

## 輸出格式

單面 A4 PDF，設計為單張單頁列印、作為講義發送，而非裝訂成冊。

- `\documentclass[a4paper,12pt,oneside]{book}` — 每一頁採同一邊界規則。
- `margin=3.3cm` 對稱；文字區塊接近 12 pt Times 每行 66–72 字元的舒適範圍。
- `\linespread{1.05}` — 為數學密集的散文提供適度的額外行距，又不致頁面稀疏。
- `\fancyhead[L]` / `\fancyhead[R]` / `\fancyfoot[R]`（非 twoside 的 `[LE]`/`[RO]` 模式）。
- `main.tex` 將 `\maketitle` 包在 `\begingroup\hypersetup{pageanchor=false}...\endgroup` 中，以避免標題頁出現重複目的地的警告。
- `main.tex` 在檔首附近保留 `\ifprintbibliography` 與 `\ifincludescratchchapter` 開關，使參考書目與暫存章節維持選用。

若專案日後需要裝訂書版本，最小變更為：改用 `\documentclass[a4paper,12pt,twoside,openright]{book}`、將 `\fancyhead`/`\fancyfoot` 改用 `[LE]`/`[RO]` 配對，並考慮使用帶 `bindingoffset` 的非對稱 `inner`/`outer` 邊界。

---

## 建置與 CI

本機建置：

```powershell
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error main.tex
```

提交一個章節之前，另須執行：

```powershell
python tools/book_style_lint.py
python tools/book_preamble_smoketest.py
python tools/book_docs_lint.py
```

全部四項檢查（上述三項加上 `latexmk` 建置）會在每一次 push 與 PR 時透過 [`.github/workflows/latex-checks.yml`](.github/workflows/latex-checks.yml) 執行。`book_docs_lint.py` 掃描 markdown 中過時的 `tools/<name>.py` 指令引用與失效的相對連結，使文件改名造成的飄移無法在審查時悄悄溜過。（第一代的 `manim_storyboard_lint.py` 已隨 Manim v1 產線封存至 `legacy/scripts/`，不再納入 CI；其方法論文件見 `legacy/`。）

權威性：當儲存庫結構或 preamble 決策變更時，**以本檔案**為權威；當撰寫或排版規則變更時，以 [`CONTENT_SPEC.md`](CONTENT_SPEC.md) 為權威。

---

## 媒體範圍說明

章末的 `\subsection*{Exercises}` 區塊僅供列印講義之用。它們**不**納入投影片 deck、旁白腳本、Manim 分鏡、合成音訊或 render 的影片。規劃各節媒體時，忽略來源節的習題區塊，從定義、定理、範例與闡述散文來建構。

## 備註

- 本機快取、虛擬環境與內嵌依賴存於隱藏的儲存庫資料夾，例如 `.cache/`、`.venv/`、`.deps/` 與 `.deps_f5/`。
- 目前的影片開發在 `video/`，而非已封存的 `legacy/inputs/manim_storyboards`。目前的檢查點是 Section 1.1
  [`video/storyboards/ch01_inverse_functions.yml`](video/storyboards/ch01_inverse_functions.yml)，
  附有可重用的 intro/outro 模板、`graph_focus`，以及 `video/output/` 下的低畫質無聲預覽。
- 已封存的第一代媒體範本是兩份刻意對比的 Manim 分鏡，曾用於校準 [`legacy/MANIM_STORYBOARD.md`](legacy/MANIM_STORYBOARD.md)：Section 1.1 *Inverse Functions*（[`legacy/inputs/manim_storyboards/ch01_inverse_functions.yml`](legacy/inputs/manim_storyboards/ch01_inverse_functions.yml)），圖形為主、符號內容輕量；以及 Section 1.6 *The Precise Definition of a Limit*（[`legacy/inputs/manim_storyboards/ch01_precise_limit.yml`](legacy/inputs/manim_storyboards/ch01_precise_limit.yml)），符號為主、帶兩個錨定圖形。Sec. 1.1 是原本的 v1.0–v1.3 參考；Sec. 1.6 作為 v1.4 壓力測試範本加入。Sec. 1.1 的凍結投影片計畫位於 [`legacy/inputs/media_plans/ch01_inverse_functions.json`](legacy/inputs/media_plans/ch01_inverse_functions.json)；以上皆為第一代凍結資料，新的 gen-2 分鏡改放於 `video/storyboards/`。
