# 微積分教學影片 — 視覺設計 Brief（Direction B · 現行系統）

> 這份文件給設計師 / 設計工具（如 claude.ai Artifacts）閱讀。
>
> **現況**：視覺系統已從零定案過一輪——目前採用的是設計師交付的 **Direction B（Blueprint Grid）**，
> 已移植進 Manim 產線並用於實際成片。所以這份 brief 的用途**不再是「從零設計」，而是
> 「理解現行系統，並針對它精修 / 迭代」**。
> - 現行設計系統的真實數值來源：[`from_designer/handoff/tokens.json`](from_designer/handoff/tokens.json)（請從這裡量測，而非從 PNG）。
> - 現行視覺參考：[`from_designer/handoff/screenshots/`](from_designer/handoff/screenshots/)（8 個場景模板各一張）。
> - 根目錄 [`screenshots/`](screenshots/) 是**上一代** Midnight Canvas 的舊參考，已被 Direction B 取代，僅供對照。
> - 文件最後有「可迭代的清單」。

---

## 1. 這是什麼專案

把一本大學微積分教科書（LaTeX 講義）做成一系列**教學影片**，一節課一支，帶英文旁白語音。
影片本質是「**一堂課**」，不是課本朗讀——細節優先、口語、視覺帶著教。

- **觀眾**：大學微積分學生（台灣 NTU MATH 等級）。
- **語言**：旁白英文，數學符號標準 LaTeX。
- **目前範例章節**：Section 1.1 反函數（Inverse Functions）。
- **產出**：每節一支 1080p、16:9 的 MP4。
- **現狀**：產線已端到端打通——storyboard → TTS（MiMo）→ 音訊驅動 render → compose，旁白與揭示動畫對齊。視覺即採用本文件描述的 Direction B。（舊 §1.1 練習成片已廢棄，正式版從講義重跑。）

---

## 2. 重要技術約束（設計前必讀）

影片是用 **Manim**（Python 數學動畫引擎）算圖渲染的，不是網頁。這決定了什麼能設計、什麼不能：

| 你設計的東西 | 我們能不能用 | 說明 |
|---|---|---|
| **配色、字體比例、間距、版面、視覺層次** | ✅ 完全可用 | 這是最有價值的產出，會直接編進渲染主題（`pipeline/visuals/theme.py`）。 |
| **靜態場景 mockup（一張圖說明某場景長怎樣）** | ✅ 當藍圖照做 | 請盡量提供。Direction B 即是這樣交付的。 |
| **設計 token（`tokens.json` 式的色票 / 字級 / 間距數值）** | ✅ 最理想 | 工程端逐值移植，是真實來源。 |
| **SVG 圖示 / 裝飾元素** | ⚠️ 部分可用 | Manim 能載入**純幾何** SVG（`<rect>`/`<path>`）；含 `<text>` 的 SVG 其文字會被丟棄（logo 因此是用 Manim primitives 重建的）。漸層、陰影、網頁字體不保證。 |
| **CSS / JS / React 動畫、互動** | ❌ 無法轉換 | 動畫一律在 Manim 重寫，這是工程端的工作，不是設計端。 |

**請這樣分工**：
- **設計端負責「長什麼樣」**（靜態風格：色、字、版面、片頭樣貌、卡片/強調樣式）。
- **工程端負責「怎麼動」**（所有動畫：淡入、寫字、曲線描繪、強調閃光等，我們在 Manim 實作）。

**三條鐵則**：
1. **數學一律走 LaTeX**，不要在設計工具裡排版數學式（`f(x)`、分數、根號…）。你可以畫「這裡放一條數學式」的佔位框，實際數學由 Manim 的 LaTeX 算（Computer Modern）。
2. **畫布固定 16:9，1920×1080**。所有版面請以這個比例設計。
3. **雙 ground 系統**（見下）：品牌時刻（intro/outro）走**淺底**，教學主體走**暗底**。若要動基調，請整套一起重新定義（兩種底色 + 各強調色對比都要重算）。

提供格式偏好：**設計 token（hex + px 數值）**最理想（可直接擷取為真實來源）；**截圖 / mockup 圖片**最直接（我們看得到圖）；**純幾何 SVG** 可用於圖示。

---

## 3. 目前的設計系統：Direction B（Blueprint Grid）

取代上一代的「Midnight Canvas」（全程暗底）。**你可以沿用並精修它，也可以提案調整**——但若要大改基調，請整套重新定義。

### 設計理念
- **藍圖格、發光的數學、克制的品牌時刻**。教學主體是沉穩的深藍黑「工程藍圖」底；開場與收尾切到淺色「紙張」底，露出 NTU 數學組品牌。
- 「內容本身就是設計」：不堆砌卡片、邊框、徽章。唯一恆定的裝飾是標題下的一條細線。
- 每一刻畫面只有一個焦點；舊內容淡退、新內容寫上。

### 雙 ground 流程（每支影片的骨架）
```
intro（淺底·品牌）→ teaching frames（暗底·教學）→ outro（淺底·品牌）
```
- **淺＝品牌時刻**（開場／收尾），露出官方校徽 lockup。
- **暗＝教學主體**（定義／例題／流程／定理／回顧／圖表）。
- 明暗切換**每支影片只各發生一次**；在這兩個切點做 0.3–0.5 秒 cross-fade，讓亮度變化不突兀。
- 因為一節即一支影片，小節間的 `section_transition` 過場卡**已棄用**（原始碼僅保留參考）。

### 配色（hex，來源：`tokens.json`）

**暗底 · 教學畫布**
| 角色 | 色碼 | 用途 |
|---|---|---|
| 背景 bg | `#0a0e1a` | 深藍黑藍圖底 |
| 面板 bg_soft | `#121a2e` | 抬升的側欄／面板塊 |
| 主色 primary | `#eef0f7` | 標題、中性文字（冷米白） |
| 次色 secondary | `#4cc9f0` | 定義、命題（冷青） |
| 強調 accent | `#f4b13a` | 定理、重點（暖金） |
| 數學 math | `#7df9ff` | 數學式（電光藍） |
| 警告 warning | `#ff6b6b` | 反例、陷阱（珊瑚紅） |
| 成功 success | `#06d6a0` | 驗證、QED（翡翠綠） |
| 內文 text | `#c8ccdb` | 一般敘述（淺石板） |
| 淡化 muted | `#7e8497` | 已退場的舊內容 |
| 細線 hairline | `#243049` | 細規線、刻度、邊框 |

**淺底 · 品牌畫布**
| 角色 | 色碼 | 用途 |
|---|---|---|
| 紙張 paper_bg | `#eef1f6` | intro/outro 淺底 |
| 標題 heading | `#16294E` | 藏青標題／wordmark |
| 副題 subtitle | `#5a6478` | 淺底上的副標 |
| 內文 list_body | `#2b3242` | 淺底上的清單／內文 |
| 強調 accent | `#BA0C2F` | eyebrow、編號、圓點、細線（校門紅） |

**品牌色（雙 ground 共用）**：校門紅 `#BA0C2F`（暗底文字用較亮的 `#e23a57`）、藏青 `#16294E`、點綴金 `#B6892B`。

### 字體與比例

> ✅ **字體已定案：全 Times New Roman / newtx**（與設計師 `tokens.json` 原案刻意不同，紀錄如下）：
> - **設計師 `tokens.json` 原案**：display = `Space Grotesk`、body = `Hanken Grotesk`、mono = `JetBrains Mono`（現代 sans）。
> - **最終實作（成片實際使用）**：body text 走 LaTeX `\text{}` **newtxtext**（非 Pango）以獲得正確 kerning；heading 走 Pango **Times New Roman** SEMIBOLD；mono **Courier New**；數學走 LaTeX **newtxmath**。全鏈與 LaTeX 講義字體一致。
> - **定案理由**：影片與講義字體統一（講義用 `newtxtext` + `newtxmath`）；Times New Roman 為系統內建字體，無需額外安裝。
> - **給設計師**：請在「全 Times」前提下精修（字級、間距、層次）；sans 提案已不採用。

- 字級（px @ 1920×1080，渲染等比縮放）：display 104 / h1 62 / h2 46 / math 46 / math_sm 36 / body 38 / step 32 / eyebrow 24 / label 28。片頭片尾另有覆寫：intro 標題 88、intro 副題 34、outro 標題 78。
- eyebrow 樣式：大寫、寬字距（letter-spacing 0.32em）、mono。
- 版面：安全邊距 96px、左右 gutter 220px、內容寬約佔畫面 **77%**，呼吸感重要；標題細線寬 3px。

### Motif（品牌元素，可動畫化）
- **SummitBars**：7 根上升的圓角長條（中央最高）＋ 選用的金色四角星。這是品牌 **DNA，不是 logo**，可安全重繪／動畫化。
- **PlotDot**：小實心圓點（座標點 motif），用作項目符號。
- **glow 強調**：被強調的那一條「key line」打金色 glow（`glow_accent`），作為 Manim flash/indicate 的靜態替身。

### Logo（NTU 數學組 lockup · 不可變形）
- 官方校徽 lockup（SummitBars 標記 + 分隔線 + 中文 wordmark + 「數學組」紅色 pill）。墨色為藏青／紅／金。
- **淺底（intro/outro）**：用彩色 lockup，直接置於紙張底，不加白框。
- **暗底（教學框）**：用反白 icon，置右下角、低不透明度。
- **鐵則**：彩色 lockup **僅**供淺底；絕不在沒有淺色襯底時放上暗底。logo SVG 不得重新上色或變形（SummitBars motif 才可以）。

### 動畫語言（目前；供你理解節奏，動畫由工程端做）
- 數學式：像粉筆一樣「寫」出來（逐字描繪）。
- 曲線：由左到右「描繪」。
- 重點：閃一下金光強調。
- 舊步驟：淡退成 muted 灰，不刪除。
- 片頭/片尾（淺底）：花俏一點（標題寫出+爆光、lockup 浮現）。教學場景（暗底）：克制、專注。

### 座標格線（已定案：不露出）
`tokens.json` 把 80px 的 blueprint 座標格列為背景 motif，但**最終決定所有模板都不露出格線**（`theme.py` `SHOW_GRID = False`，要乾淨的深藍底）；`grid_line` 色保留為潛在 motif（日後若要可重啟）。「Blueprint Grid」這名字保留——指的是深藍工程藍圖的整體調性，而非字面上的格線。

---

## 4. 目前成品（場景模板一覽）

現已實作 **8 個場景模板**（含 intro/outro），均為 Direction B。設計師 mockup 見
`from_designer/handoff/screenshots/`；同一批已移植為 `pipeline/templates/*.py` 並用 Manim render。

| 截圖 | 模板 | kind / accent | 工程端模板 |
|---|---|---|---|
| `01-intro` | intro（淺·彩色 lockup） | intro | `templates/intro.py` |
| `02-definition_math` | 定義 / 命題（敘述 + 數學式） | content · definition | `templates/definition_math.py` |
| `03-example_walkthrough` | 例題逐步（步驟列 + 演算 + 結論） | content · example | `templates/example_walkthrough.py` |
| `04-procedure_steps` | 流程（大編號 + 步驟 + 公式） | content · procedure | `templates/procedure_steps.py` |
| `05-theorem_proof` | 定理 + 證明（敘述 + 步驟 + QED） | content · theorem | `templates/theorem_proof.py` |
| `06-recap_cards` | 節末回顧（重點 + 要記公式） | content · recap | `templates/recap_cards.py` |
| `07-graph_focus` | 滿框函數圖（軸 + 曲線 + 標點 + 註解） | content · example | `templates/graph_focus.py` |
| `08-outro` | outro（淺·彩色 lockup + 結尾字卡；無 takeaways） | outro | `templates/outro.py` |

> ⚠️ 截圖是靜態的，看不出動畫。重點請看**版面、配色、層次、字體**。
> 精確像素位置請用 `tokens.json` + 原始碼（`from_designer/handoff/source/`），別從 PNG 量。

此外，工程端後續以同一套 Direction B token／primitive **新增了四個無設計師 mockup 的模板**
（2026-06-11）：`derivation`（全寬推導鏈）、`value_table`（數值表／公式總表）、
`graph_compare`（雙圖並排對照）、`sign_chart`（數線符號表）。它們不對應任何截圖；
版面權威是 [`../DESIGN.md`](../DESIGN.md)「Template catalog」與各自的
`storyboards/_demo_*.yml` demo 稿。

---

## 5. 可迭代的清單（現有系統的精修方向，不是從零設計）

8 個模板都已存在。請針對下列各項提供**精修建議**（版面微調 + 任何配色/字體調整），而非重畫。

### A. 全域視覺語言（地基，優先校準）
- [x] **字體定案**：已決定**全 Computer Modern**（放棄 tokens 的 sans 提案，理由見 §3）。
- [ ] **配色微調**：確認雙 palette 在各自底色上對比足夠（尤其暗底 secondary/math 與淺底 accent）。
- [ ] **明暗交接**：兩個 cross-fade 切點的節奏與亮度橋接。
- [x] **格線決策**：已決定**不露出格線**（`SHOW_GRID=False`，見 §3 末）。

### B. 片頭 / 片尾（視覺最重，淺底品牌時刻）
- [ ] **intro**：Section Gate 開場（章節地圖 → 聚焦當前節 → logo/節/標題/slogan 字卡 → 暗場交接）。
- [ ] **outro**：兩段式（暗轉亮橋接 → 最終 logo 字卡）；Key Takeaways 在前一個 `recap_cards` 場景（有旁白），不在 outro。

### C. 內容場景模板（暗底，數學走 LaTeX）
- [ ] **definition_math**、**example_walkthrough**、**procedure_steps**、**theorem_proof**、**recap_cards**：皆已實作，可逐一美化。
- [ ] ~~section_transition~~：**已棄用**（一節一片）。

### D. 圖表場景（最特殊）
- [ ] **graph_focus**：滿框函數圖。曲線由 Manim 算，但**軸的粗細顏色、標記點（實心 vs 空心的數學語意）、註解框樣式、配色搭配**需要你定。

### E.（可選）品牌與聲音
- [ ] 角落浮水印 / 統一標記。
- [ ] **BGM**：片頭/片尾的背景音樂風格、來源、授權與 ducking（尚未接）。

---

## 6. 建議的討論順序

1. 先校準 **A 全域視覺語言**（字體與格線已定案，剩配色對比與明暗交接）。
2. 再看 **B 片頭/片尾**（淺底品牌時刻，回饋最快）。
3. 然後 **C 內容模板**（一個一個精修）。
4. 最後 **D graph_focus**（最特殊，單獨深談）。

---

## 7. 給設計工具的一句話總結

> 精修一套**已定案**的 16:9 數學教學影片視覺系統 **Direction B（Blueprint Grid）**：**雙 ground**——
> 暗底教學 + 淺底品牌（intro/outro），真實數值在 `from_designer/handoff/tokens.json`。字體與格線已定案
> （**全 Computer Modern**、**不露出格線**，刻意偏離 token，理由見 §3）。重點待辦：雙 palette 對比校準、
> 各模板版面微調。數學式一律 LaTeX（Computer Modern），所有動畫由工程端 Manim 實作（別做 CSS/JS 動畫）。
> 現行截圖見 `from_designer/handoff/screenshots/`。
