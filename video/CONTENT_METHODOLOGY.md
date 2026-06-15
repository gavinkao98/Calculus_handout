# 教學影片內容方法論（Content Methodology）

> **這份文件回答一個問題：給定講義中已定稿的**一節**，我們要做出怎樣一支教學影片的**內容**？**
>
> 它只管**內容**（教什麼、怎麼教、怎麼說、哪裡要視覺／動畫），**完全不碰工程**（template、`{show}` reveal marker、accent、視覺 payload、render）——工程是**第二階段**把內容稿「模板化」時才處理。
>
> **血統與定位：** 萃取自 [`legacy/MANIM_STORYBOARD.md`](../legacy/MANIM_STORYBOARD.md)（gen-1, v1.6）的教學精神，**剝離**其 gen-1 工程約束（spoken-math 改寫大表、reveal 策略、9-template catalog、lint／schema），**適配** gen-2（Gemini TTS 直讀 LaTeX、intro／outro first-class）。它是 gen-1 方法論在 gen-2 的繼任者。
>
> **相關文件：** 視覺系統見 [`design_handoff/`](design_handoff/)（Direction B）；講義（HTML handout kit）的撰寫契約與環境詞彙見 [`../handout/_dev-archive/general/CONTRACT-html-writing.md`](../handout/_dev-archive/general/CONTRACT-html-writing.md)；本產線總覽見 [`README.md`](README.md) 與 [`DESIGN.md`](DESIGN.md)。
>
> **交付物：** 每節一份**內容稿**（格式見 §6）——`.md` 為 source of truth，且**一律附上編譯後的 standalone HTML 審核稿**供使用者閱讀（見 §6「交付形式」，2026-06-14 使用者指示）。

## 一致性關鍵字

沿用 RFC 2119 風格，讓吃重的規則無歧義：

- **MUST／MUST NOT** — 硬性要求，違反者不合格、應在進入第二階段前修正。
- **SHOULD／SHOULD NOT** — 強建議；偏離需有具體理由，並在內容稿就近註記，供日後判斷。
- **MAY** — 選用。

---

## 1. 核心理念

**影片是一堂課，不是把課本念出來。** 三個承諾：

1. **Detail over compression（細節優先）。** 寧可多開一個教學單元，也不要把兩個重點塞進一個。一節 HTML fragment 開成十幾、二十個單元是正常的；做 4 分鐘精華片**不是**目標。
2. **Conversational（口語優先）。** narration 是**說出來**的英文，為耳朵寫，不是印在紙上的句子。書本說「Determine which of these functions are one-to-one」；影片說「Now let us test two functions」。
3. **Visual／animation over textual（視覺、動畫優先）。** 能在圖上展示的概念就給它視覺；會「動」的概念（過程／變化／對應／掃描）就給它動畫。**例外**見 §5 的 symbol-heavy 規則。

兩條貫穿全篇的硬規則：

- **一個單元一個教學重點（one teaching idea per unit）。** 一段 narration 若需要兩個主題句，就拆成兩個單元。
- **內容忠實於講義（faithful to the handout）。** 數學內容與範圍跟著講義 HTML（handout kit；各章權威檔見 [`README.md`](README.md)「輸入」）這一節走——不漏環境、不加入新的數學、不脫離；每個承載數學的單元 MUST 可回溯到講義的某個環境／手寫編號。**但呈現為教學服務**：場景**順序可為教學自由重排**（見 §3），且 MAY 增補書本沒有的單元（intro／outro、把散文裡的幾何主張變成視覺／動畫單元）。重排與增補的是**呈現**，不是內容——不因重排而增刪任何數學。

---

## 2. 影片的單位與範圍（Scope）

- **一節 = 一支影片。**（gen-2：一節一片；小節之間不另做過場片。）
- **每支必有 intro 與 outro**（gen-2 first-class，純動畫、**無 narration**）：
  - **intro** — Section Gate 開場（章節地圖 → 聚焦本節 → 標題字卡）。內容稿只需提供本節在章內的定位：章、章名、節、節標題，以及一句引導問題 `tagline`。
  - **outro** — 收尾的品牌字卡（暗轉亮橋接 → 最終 logo 字卡，**無 takeaways**）。Key Takeaways 是獨立的 recap 單元（→ `recap_cards` 場景，有旁白），不在 outro。
- **一定納入（MUST）：** 每個 `definition` / `theorem` / `proposition`；書本明確編號的 procedure／strategy；承載教學的圖。
- **例題：代表式涵蓋（MUST cover every distinct pattern; MAY fold repeats）。** 每個**不同教學模式**的 `example`（+`solution`）——帶來新技巧、新陷阱、或新情形的——MUST 有代表單元；**同型重複**的例題（同一手法的第二、三個 drill）MAY 折疊成一個代表＋一句「同手法，留給你在講義練」，並在內容稿就近**註明折疊了哪個、為何**（MUST NOT silently drop）。判準是「這個例題有沒有帶來新東西」，不是固定數量——影片是線性計時的一堂課、講義是隨機存取的參考書，忠實靠「涵蓋每個概念／技巧且不牴觸」達成，不必把每個 drill 重演。保留的同型第二例仍套 §4 repeat-pattern 省 setup。（2026-06-13 使用者拍板，取代原「每個 example 一律 MUST 納入」。）
- **一定略過（MUST NOT 進影片）：** `env-exercise`（習題只屬書本）、指向本節**外**的交叉引用（kit 為手寫編號的 prose 引用，如 “by Theorem 4.2”——改用白話轉述，觀眾沒有頁可翻）、純裝飾的圖。
- **視情況納入：** `proof`（短、有啟發、或書本已寫就收；冗長或純技術就略）、`remark`（升格為**具名規則**如「水平線測試」才獨立成單元，否則併入鄰段 narration）。

---

## 3. 從講義拆成教學單元（Decomposition）

### 環境 → 教學單元對應

第一刀照下表切；邊角看註解。（講義環境詞彙定義在 [`../handout/_dev-archive/general/CONTRACT-html-writing.md`](../handout/_dev-archive/general/CONTRACT-html-writing.md)。）**注意：下表給的是教學單元的 `kind`（教學角色），不是工程 template——template 是第二階段的事。**

| 講義環境（kit class） | 單元 `kind` | 處理 |
|---|---|---|
| `env-definition` | `definition` | 一個定義一個單元。螢幕上的 statement 收斂成一句宣告句，符號內容照搬；`informal` gloss 是現成的白話句。 |
| `env-theorem` + `env-proof` | `theorem`（+`proof`） | statement + 證明邏輯鏈。證明若超過 ~4 步，拆成「statement 單元」+「proof 單元」，讓學生能在陳述後暫停。 |
| `env-theorem`／`env-proposition`／`env-corollary`（無證明） | `theorem`／`proposition` | 同定義的處理，教學角色不同而已。 |
| `env-example` + `env-solution`（`workedexample` 配對） | `example` | 每個邏輯動作一個 step。**同型的第二個例子 MUST 跳過第一個已建立的 setup**，直接進新內容。 |
| `env-strategy`（`ol.steps`） | `procedure` | 步驟用祈使句。判斷型 strategy（含條件分支）**MUST NOT** 因分支而拆成多個單元——讓 narration 承載條件邏輯。 |
| `env-remark`（具 `env-name` 的具名規則） | `proposition`／`definition` | 當輕量命題處理。 |
| `env-remark`（短附註） | —（併入鄰段 narration） | 2 句的提醒不需要自己的單元。 |
| `env-caution`（1–3 句陷阱警示） | —（併入其警示對象的單元） | 用警示語氣融進該單元 narration；自成教學點（如標準反例）才獨立，多為 `counterexample`。 |
| `figure`（`data-fig` 註冊於 figures.js，或 inline SVG） | `visual` | **Redraw, don't reproduce**（見 §5）；多半值得做成動畫。 |
| 散文裡的幾何主張 | `visual`（補充） | 講義只用散文講鏡射／相交／形狀時，**SHOULD** 加一個視覺單元（symbol-heavy 例外見 §5）。 |

### 邊角：具名規則 + 其演示圖

一個具名規則（如水平線測試）與「讀它的那張圖」往往是**同一個教學重點**——此時 **SHOULD** 合為**一個**單元（規則寫進 `narration`，圖寫進 `visual_need`／`animation_cue`），不必拆成「規則單元 + 圖單元」。只有當 narration 過載、或那張圖另有獨立的教學點時才拆。（校準來源：§1.1 內容稿的水平線測試單元。）

### 環境之間的散文（prose-only）

一節常有承載教學的散文夾在環境**之間**（鋪陳、過渡、圖後小結、向前預告）。每一段 MUST 歸類並處理，**MUST NOT silently drop**：

- **Incorporative（鋪陳）** — 為下個環境鋪路（定義要研究的函數、引出即將到來的定義）。併入下個單元 narration 的 **lead-in**。
- **Bridge（過渡）** — 連接兩個概念塊。1–2 句：併入前一單元的收尾或後一單元的 lead-in。3 句以上且有真正的概念跳躍：**promote** 成獨立單元。
- **Forward-pointing（向前預告）** — 引入後章才系統處理的概念（「我們會在後面細談」）。**永遠獨立成單元**，放在本節主內容與 recap **之間**。**MUST NOT** 報出章號（影片的生命週期與書本章序無關）。

### 順序：為教學自由重排

場景順序**不必**是書本出現的順序——為教學重排。單節的偏好流程：

1. **intro** 開場。
2. **motivation／第一個概念**：開節的定義，先白話講清楚再形式化。
3. **該概念的具體例子**：書本若有真實世界或數值例子，放在代數例子**之前**——學生先把定義扣在具體個案上。
4. **代數例子**：同一概念的符號處理。
5. **幾何視覺**：若散文做了幾何主張。
6. **支撐命題／引理**：若書本有述。
7. **（下一個概念，重複 2–6）。**
8. **procedure**：若本節把一個演算法定型。
9. **套用 procedure 的 worked example**。
10. **反思／對稱／圖像視覺**：worked example 的幾何面。
11. **定義域限制／邊界例子**：若書本有。
12. **recap**，接 **outro**。

把書本沒有的視覺／動畫單元就近插在它所支持的內容旁。**重排的是呈現順序，內容仍忠實**——每個承載數學的單元仍可回溯到講義（見 §1），不因重排而增刪數學。

### 單元數不是預算

不要刻意壓低單元數。一節該幾個單元，是好拆解的**結果**，不是限制。

---

## 4. narration：為「說」而寫

這是最容易出錯的一層。書本散文印在紙上好讀，念出來生硬。每一句都為耳朵改寫。

### Register（語域）

- **「we／let us」帶全班，祈使句做 setup，「you」少用且只用於直接呼喚。** 避免「the reader」「I」。
- 縮寫多半攤開：「let us」「that is」「do not」優先於「let's」「i.e.」「don't」（流暢時 MAY 破例）。
- 課堂引導語小量使用：「Here is the idea」「Notice that」「Watch what happens」——拉著學生走，別濫用。

### 三段結構

一段 narration **SHOULD** 依序有三部分（不必全到）：

1. **Hook／transition**（1 句）— 接上文或點出本單元主題。
2. **Body**（2–4 句）— 承載內容，把數學說出來、把邏輯走一遍。
3. **Takeaway／bridge**（1 句）— 學生該記住的一句，或指向下一單元。

標準單元 **3–7 句**為目標；不同 `kind` 自然句數不同（證明、recap 偏長）。抓的是「**一個教學重點的凝聚**」，不是死守句數——明顯超長就拆，明顯過短代表視覺在做 narration 該做的事。

### 數學口語化（輕量原則，取代 gen-1 的 spoken-math 大表）

gen-2 用 **Gemini TTS 直讀 LaTeX**，所以 narration 裡可以**直接內嵌 LaTeX 數學**讓它讀——**不必**再手動把 `f(x_1)` 改寫成「f of x one」。原則：

- narration 寫成「**老師會怎麼把這個式子講出來**」。簡單式子直接內嵌（`$f(x_1)=f(x_2)$`）；當念出來會卡或冗長時，改寫成白話敘述。
- **對齊推導鏈**（aligned on `=`／`\le`／`<`）：首行念全式（含 LHS），中段只念「連接詞 + RHS」（省掉對齊在維持的 LHS），末行若回到原 LHS（矛盾收尾）則明白點出。不要每行重念 LHS——對齊已經替你做視覺重複了。
- **直讀已驗證**：Gemini 直讀 LaTeX 已實測沒問題（下標、分數、根號、`\varepsilon`-`\delta`、量詞都可），所以 narration 裡放心直接內嵌數學讓它讀，**無需**任何 spoken-math 改寫層。改寫成白話純粹是**教學選擇**（某些式子講白話更好懂），不是 TTS 的限制。

### repeat-pattern：第二次省掉 setup

一節若有兩個以上**同型**的例子（兩個 `\varepsilon`-`\delta` 驗證、兩個分部積分），第二個起 **MUST NOT** 重述第一個已建立的 setup；用一句轉場（「Same goal, but the algebra is more delicate…」）直接進新內容。

### narration 的禁則（MUST NOT）

- 念出螢幕標題。
- 逐字念螢幕上的條列（改用轉述或延伸）。
- 報節號／圖號／式號，或書本手寫編號的 prose 交叉引用目標（如「by Theorem 4.2」）。
- 用「see」「as shown」「in the diagram above／below」。
- 用「In this scene we will…」開頭——直接開始教。

---

## 5. 視覺與動畫：內容層的決策

本節只做**內容層決策**（要不要視覺、要什麼、演示哪個教學點），**不做工程實作**（座標、plot、manim code 都屬第二階段——含 Claude 依 `animation_cue` 生成的客製動畫）。

- **Redraw, don't reproduce。** 書本圖是「**要顯示什麼**」的權威，不是「**怎麼顯示**」。內容稿描述要顯示的數學物件與教學目的即可。
- **Animate, not just display。** 書本圖是靜態一頁；影片能讓曲線 trace 出來、測試線 sweep 進來、交點 flash、圖形對 `y=x` 翻摺、極限逐步逼近。**會動的概念就讓它動，讓動態承載一個教學點。**
- **散文的一般主張 MAY 用具體函數示範。** 當講義只用散文陳述一個**一般**的幾何主張（如「$f$ 與 $f^{-1}$ 的圖對 $y=x$ 鏡射」），視覺單元 **MAY** 挑一個**具體函數**把它畫出來（如用 $x^3/\sqrt[3]{x}$ 示範鏡射），最好呼應本節已出現的例子。這是**增補呈現、不增刪內容**——畫的是已述主張的一個實例，不是新的數學。（校準來源：§1.1 內容稿的 reflection 視覺單元。）

### 靜態視覺 vs 動畫（內容稿的兩個欄位）

- **`visual_need`** — 靜態視覺需求：要畫什麼圖、標什麼點、放哪句數學。
- **`animation_cue`** — 當概念適合**動態演示**時，用**自然語言**描述建議動畫：**演什麼、怎麼動、強調哪個教學點**。

### 動畫的分工（重要）

內容稿**只提動畫建議（自然語言）**，**MUST NOT 寫 manim code**——內容層與工程層的分離不變。但**客製動畫的 manim code 由 Claude 依 `animation_cue` 的自然語言生成**（不再由使用者手畫），生成後接入工程層的 hook 接入點（工程稿的 `# HOOK` 處）。這對應 gen-1 的 `hook`（客製動畫 escape hatch）——模板畫不出來的、需要手控時序的動畫，現由 Claude 從自然語言規格生成。生成的動畫 code 視同 narration：**SHOULD 經使用者過目認可**再定版。

於是 `animation_cue` 是使用者／內容稿作者交給 Claude 的**動畫規格**，也是 Claude 生成 code 的依據；它的寫法 **SHOULD** 聚焦**教學意圖**而非實作細節（實作細節由 Claude 在生成時決定）：

- 好：「水平線從畫面上方緩緩下移、掃過 parabola；落到 $y=\tfrac14$ 時停住，同時閃示兩個交點 $x=\pm\tfrac12$，凸顯『一個輸出對應兩個輸入』。」
- 不好：寫座標數值、寫 manim 物件名、寫 `run_time`。

### 生成 code 的修補紀律（render 失敗時）

Claude 依 `animation_cue` 生成的客製動畫 code 偶爾 render 失敗。此時 **SHOULD 由小到大逐層修補**，**MUST NOT** 一失敗就整支重生——重生會丟掉已被使用者認可的部分，還得從頭重審。修補階梯：

1. 讀 manim traceback，定位失敗落在生成 code 的哪一行。
2. **局部修**：只動失敗行與其緊鄰上下文，重跑。
3. 連續數次局部修仍失敗 → **放大到整個 hook 函式**重寫。
4. 仍失敗 → **才**從 `animation_cue` 整支重生（回到自然語言規格重新生成）。
5. 每次修補 **SHOULD** 小到能被使用者**重新過目**——維持「生成 code 視同 narration、經認可才定版」的不變量（見上「動畫的分工」）。

緊迴路用既有的 per-scene mock render（離線、不計費；`make.py` 的 `render()` 已逐場景捕捉例外並印 traceback）：

```powershell
python video\make.py --storyboard <yml> --scene <hook場景id> --backend mock --quality low
```

（這條是**工程層**的修補節奏，render 機制本身屬第二階段，見 [`DESIGN.md`](DESIGN.md)；§5 在此只定「先局部、保認可、小步可審」這條紀律。借鏡 Code2Video 的 ScopeRefine 分層除錯，細節見 [`CODE2VIDEO_STUDY.md`](CODE2VIDEO_STUDY.md) P2。）

### symbol-heavy 例外

若一節的教學重量 **≥ 70%** 是符號／邏輯／量詞（`\varepsilon`-`\delta`、收斂判別、Riemann sum、形式連續性、歸納證明），視覺**條件化**而非放棄：

- **一個 anchor 視覺**，抓住該節核心的幾何直覺。
- **至多一個對比視覺**，且只在「對比本身就是這課」時（反例、破壞假設、發散情形）。
- **不**為每個代數例子都加圖——那會稀釋掉真正的內容（不等式操作）。符號本身就是該節的 beat。

操作判準：下筆前估這一節的教學重量裡，符號／邏輯佔多少 vs 幾何佔多少。≥70% 符號 → 套條件化規則。（gen-1 校準：§1.1 約 40% 符號，七個視覺單元各司其職；§1.6 約 90% 符號，只有 anchor + 一個動機圖。）

---

## 6. 內容稿格式（純內容中間產物）

延續 [`legacy/.../ch01_inverse_functions_final.md`](../legacy/artifacts/scripts/ch01_inverse_functions_final.md) 的乾淨結構，補上來源與視覺／動畫需求，**剝除一切工程欄位**。每個教學單元：

| 欄位 | 內容 |
|---|---|
| `id` | 單元識別碼。snake_case、描述**教學重點**而非書本結構（好：`why_square_fails`；壞：`scene_3`）。本節內唯一。 |
| `source` | 對應講義環境＋手寫編號（如 `chapter1-print-standalone.html §1.1 · Definition 1.1`；prose 段落用就近環境錨點描述、圖用 `data-fig` id 或 `Figure N.M`）。 |
| `learning_goal` | 一句話：學生看完此單元學會什麼。 |
| `kind` | 教學角色：`motivation` / `definition` / `theorem` / `proof` / `proposition` / `example` / `counterexample` / `procedure` / `visual` / `recap` / `forward_ref` … |
| `narration` | 口語完整稿（英文；數學依 §4 口語化原則；intro／outro 無此欄）。 |
| `visual_need` | 此單元需要的**靜態視覺**（內容層描述，不指定 template／payload）。 |
| `animation_cue` | （選用）概念適合**動態演示**時的自然語言動畫建議（＝交給 Claude 的教學意圖規格）→ **Claude 依此生成客製 manim code**，認可後接入工程稿 `# HOOK`。 |

> 刻意**不含** `template` / `{show}` marker / `accent` / 視覺 payload——那些是第二階段把內容稿「模板化」時才填。

### 交付形式：`.md` 為源、編譯 HTML 為審核稿（2026-06-14 使用者指示）

內容稿以**兩種形式並存**交付，缺一不可：

- **`content_scripts/<deck-id>.md`——source of truth。** 純內容中間產物、可 diff／版控；上表欄位的權威版本。後續維護（§8）一律改這裡。
- **`content_scripts/<deck-id>_narration.html`——給使用者審核的可讀稿（一律附上）。** standalone HTML（MathJax/KaTeX CDN，雙擊即開、數學即渲染），逐單元列 `narration`，並把 `learning_goal`／`visual_need`／`animation_cue` 收進可展開區。**每次交付內容稿（新撰或修訂）都 MUST 同時編譯出這份 HTML**——生 `.md` 裡的 inline LaTeX 不好讀，渲染後才方便逐段審旁白。

**規則：** 旁白認可在 HTML 上進行，但 `.md` 仍是 source of truth；兩者 narration 內容 MUST 一致（改 `.md` 就重編 HTML，不可只改一邊）。這是根目錄 [`../CLAUDE.md`](../CLAUDE.md)「給使用者審核的交付物要用『打開就能讀』的形式」對內容稿的具體落實。**範本**（head／CSS 可直接沿用）：[`content_scripts/ch01_inverse_trig_narration.html`](content_scripts/ch01_inverse_trig_narration.html)（§1.2）、[`content_scripts/ch01_limit_of_function_narration.html`](content_scripts/ch01_limit_of_function_narration.html)（§1.3）。

### 範例 A：一個 `definition` 單元（靜態即可）

```
id: one_to_one_definition
source: chapter1-print-standalone.html §1.1 · Definition 1.1（one-to-one）
learning_goal: 認得讓函數可逆的形式條件——one-to-one。
kind: definition
narration: |
  The property we need is called one-to-one. A function is one-to-one
  when different inputs always give different outputs — no two distinct
  inputs ever land on the same output. Equivalently, if $f(x_1)=f(x_2)$
  then $x_1=x_2$; that second form is the one you actually use in a proof.
visual_need: 一句白話定義 + 兩條等價數學式
  ($f(x_1)\ne f(x_2)$ whenever $x_1\ne x_2$；$f(x_1)=f(x_2)\implies x_1=x_2$)。
animation_cue: （無——靜態即可）
```

### 範例 B：一個帶動畫建議的 `counterexample` 單元

```
id: why_square_fails
source: chapter1-print-standalone.html §1.1 · Remark 1.1（Horizontal line test）+ Figure 1.1（data-fig: hlt）
learning_goal: 看見「重複的輸出」如何讓反函數無法定義。
kind: counterexample
narration: |
  Watch what goes wrong for $g(x)=x^2$ on $[-1,1]$. The output one quarter
  comes from two different inputs, a half and minus a half. One output
  forced to choose two inputs — that is exactly what an inverse cannot do,
  so $g$ has no inverse on this interval.
visual_need: parabola $y=x^2$ 於 $[-1,1]$；水平線 $y=\tfrac14$；兩交點 $x=\pm\tfrac12$。
animation_cue: |
  建議動畫：水平線從畫面上方緩緩下移、掃過 parabola；落到
  $y=\tfrac14$ 時停住，同時在 $x=-\tfrac12$、$x=\tfrac12$ 閃示兩個實心點，
  各拉一條虛線回 x 軸，凸顯「同一個輸出 → 兩個不同輸入」。
```

---

## 7. 內容層品質檢核

定稿一節內容稿前，逐項過（**只列內容層；工程檢核屬第二階段**）：

- [ ] 每個 `definition` / `theorem` / `proposition` 都有單元覆蓋；每個**不同模式**的 `example` 有代表單元，折疊掉的同型重複都就近註明（§2 代表式涵蓋）。
- [ ] 沒有 `exercise` 內容洩入。
- [ ] intro 與 outro 齊備（intro 有定位資訊 + tagline；recap 單元有 takeaway 清單；outro 無 takeaways）。
- [ ] 每個散文裡的幾何主張都有視覺單元（或就近註明刻意略過）；symbol-heavy 節套 §5 例外。
- [ ] 每段環境之間的散文都歸類過（Incorporative／Bridge／Forward-pointing），fold 或 promote，無 silently drop。
- [ ] 每段 narration：3–7 句（依 `kind` 調整）、開頭是 hook、結尾是 takeaway、未犯 §4 禁則、同型第二例不重述 setup。
- [ ] 數學在 narration 裡讀得順（直讀 LaTeX 或白話；對齊鏈不重念 LHS）。
- [ ] 動畫建議用自然語言、聚焦教學意圖（manim code 由 Claude 依此生成、經認可定版，見 §5）。
- [ ] 每個 `id` 唯一、snake_case、描述教學重點。
- [ ] **通讀整份 narration**，任何一段聽起來像教科書就重寫。
- [ ] **散文潤稿 pass**：鎖稿前跑過 redundancy／贅字／讀順度 rubric（[`content_scripts/_audit/PROMPT-narration-copyedit.template.md`](content_scripts/_audit/PROMPT-narration-copyedit.template.md)），冗餘與贅字在 derive 前處理掉（鎖稿後忠實性 Mode B 不再動措辭）。
- [ ] **已編譯出 `<deck-id>_narration.html` 審核稿**（§6「交付形式」）：數學渲染正確、與 `.md` narration 一致——交付給使用者審核的是這份 HTML。

### 散文潤稿 pass（鎖稿前；與忠實性 Mode B 的分工）

narration 草稿成形、**鎖稿並 derive 成 HTML／口語版之前**，跑一輪**散文潤稿**（[`content_scripts/_audit/PROMPT-narration-copyedit.template.md`](content_scripts/_audit/PROMPT-narration-copyedit.template.md)）：抓 local redundancy（同詞在一兩句內重述，如「has a name: one-to-one. A function $f$ is one-to-one if…」）、贅字、讀順度、句長、跨單元 echo。它**可以動源稿措辭**，但只改「怎麼說」、不改「教什麼」與任何數學。

**為何在這裡、而非 Mode B：** 忠實性 Mode B（[`content_scripts/_audit/PROMPT-narration-modeB.template.md`](content_scripts/_audit/PROMPT-narration-modeB.template.md)）在鎖稿**之後**跑，且其 framing 明令「不 re-litigate 已認可內容」、忠實維度（D2）更要求口語版逐字照源稿——所以冗餘／贅字一旦進了認可源稿就改不動了（去重會被當成 D2 違規）。**冗餘與贅字只能在鎖稿前的這個 pass 攔下。** 分工：潤稿管 *how*（鎖稿前、可改源稿），Mode B 管 *faithful + 數學正確*（鎖稿後、不改源稿）。

**已鎖稿的節要補潤稿**屬例外：使用者明確授權為一次 Mode A 編修；若改到已合成的 beat，要重新 derive ＋ 重新 TTS（計費）。

---

## 8. 講義變動時的維護

當講義 HTML 改動已寫過內容稿的一節：

1. **Diff 這一節**，認出哪些環境被加／刪／改寫。
2. **外科式修改**受影響的單元，不要整份重寫。
3. **重念受影響的 narration**：若記號改了，引用該記號的 narration 也要跟著改。
4. **內容稿是 source of truth**，MUST NOT 從別處（舊 storyboard、deck）重生覆蓋——重生會丟掉所有人工撰寫。
