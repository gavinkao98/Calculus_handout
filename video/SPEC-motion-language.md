# SPEC — 畫面語法五條規則（motion language）

> **2026-09-13 立檔。依據**＝四支參考影片的逐幀拆解 [`content_scripts/_audit/REVIEW-reference-videos-A1A2B1C1.html`](content_scripts/_audit/REVIEW-reference-videos-A1A2B1C1.html)（32 張對照卡，每卡左＝參考影片三幀動作條、右＝我方 §3.1 同概念的幀）與六鏡看片 [`REVIEW-ch03_s31-rewatch-multilens.html`](content_scripts/_audit/REVIEW-ch03_s31-rewatch-multilens.html)。**裁決**＝使用者 2026-09-13「五條規則都進規格」。研究過程與替代方案見附錄 A，參考影片清單見附錄 B，工具見附錄 C。
>
> **定位。** 本檔是 motion primitive 的**設計語言層**：規定畫面「該怎麼動」與「為什麼」。[`DESIGN.md`](DESIGN.md)「motion primitive」各節是**實作契約層**（storyboard 欄位、Block、anim、零行為改變）。驗收歸 [`REVIEW_GATES.md`](REVIEW_GATES.md) 與 [`REWATCH-REVIEW-RUBRIC.md`](content_scripts/_audit/REWATCH-REVIEW-RUBRIC.md)。衝突時**本檔定原則、DESIGN.md 定欄位**：欄位做不到原則就回來改欄位，不反過來降原則。
>
> **不改的既有裁決。** 水位「模板層普遍有動」（品質補強輪 ⑦）、原語清單 1–7（③＋⑬；本檔把參考影片裡的新手法**歸進既有原語**，不新增編號）、驗收線「每個 content 場 `longest_still_seconds` ≤ 12 s」（⑧）、「模板不是病灶」的證據（⑧）。
>
> **適用範圍。** 新稿 **MUST** 遵守；既有 deck 依 DESIGN.md 的 opt-in 欄位逐場採用、預設路徑零行為改變；§3.1 放大階段以本檔為驗收依據。RFC 2119 用語同 [`CONTENT_METHODOLOGY.md`](CONTENT_METHODOLOGY.md)。

## 0. 一頁摘要

| # | 規則 | 一句話 | 已有機制（DESIGN.md） | 缺口（待建） | 驗收信號 |
|---|---|---|---|---|---|
| 1 | **一場一張畫布** | 承重物件在一幕裡只建一次，換步驟用位移／縮放／複製搬去新佈局；臨時標註縮小加淡出退場 | `color_role`（顏色延續）、`{show scaffold.*}`（版面不變、晚到） | 物件跨場攜帶、複本飛去角落當 inset、收尾歸位 | 每幕至少一個承重物件跨場延續；R2「一場一張卡」finding＝0 |
| 2 | **畫出來，只動變的 token** | 曲線由點走出、文字逐字寫、式子只動變的 token；整行 FadeOut 再 FadeIn 是反模式 | `anim: transform`、`paced:`（隨旁白書寫）、`seconds: beat` | token 級插入（鄰居讓位）、兩段式消去、graph 物件 Create 而非 Fade | 新稿 derivation 場整塊淡入 ≤ 1 次（首列） |
| 3 | **框、放大鏡、調暗，不靠鏡頭** | 注意力用框選預備、inset 放大（主圖不縮放）、主圖降亮；2D 場不以 zoom 為第一選擇 | `focus:`（壓暗與還原）、transform 自動把來源列退為 muted | inset 放大鏡、變動前框選、強調閃爍（Indicate） | 每個 derivation 結果拍與 graph 關鍵拍有 focus 宣告；R2「找不到重點」finding＝0 |
| 4 | **靜止是設計出來的** | 每段超過 6 s 的靜止 MUST 是宣告的（`pauses:`）或被 paced／sweep 填滿；動作只在步驟切換時發生 | `pauses:`、`paced:`、`seconds: beat`、⑧ 的 12 s 線、**`[stillness]` advisory（`make.py`＋`pipeline/stillness.py`，2026-09-13 接線）** | R4 rubric 門檻對齊（kickoff T5） | `longest_still_seconds` ≤ 12 s（沿用）＋未宣告靜止 > 6 s＝0 |
| 5 | **語意色貫穿圖與式** | 同一變數在圖、括號、軸標、填色、式子 token 用同色；卡類型色與箭頭色本身就是語意 | `color_role`（derivation 列、graph plot）、Direction B 色軸（accent）、**VISUAL-FRAME V10（2026-09-13 接線）** | deck 級變數色表、MathTex token 上色、箭頭色＝目標色（kickoff T1） | 同一節內同一變數不得出現兩種色；V10 blocking＝0 |

## 1. 依據（一段講完）

四支影片、三種引擎、同一套語法。A1（3Blue1Brown，Manim）與 C1（Morphocular，Manim）做到全部五條；A2（Think Twice，PowerPoint 或 After Effects，幀上分不出）做到前三條；B1（Ghrist，PowerPoint 加 Illustrator，一人一暑假 60 支）放棄一到三、守住四與五。**所以瓶頸不在引擎**，在「規格有沒有寫下來、模板有沒有落實」。我方 §3.1 六鏡看片的判定（內容好、畫面語法是「卡片加整塊淡入」、content 場靜止 92 到 97%）正是五條都沒守的樣子；hook 場靜止比例與非 hook 場無異，說明沒有規格時，人寫或 agent 寫都會回到「揭示然後停住」。

## 2. 五條規則

每條四段：規則（MUST／SHOULD）、證據（影片與時間點，可在對照表用「在 YouTube 打開」直接跳到）、落地（已有機制怎麼用、缺什麼）、驗收。

### 規則 1　一場一張畫布

**規則。**
- 一幕（divider 之間的場群）裡的**承重物件**（定理裡的圖、被推導的式子、單位圓、坐標系）**MUST 只建一次**；後續場要用同一物件時 MUST 以位移、縮放、複製把它帶到新佈局，MUST NOT 淡出後在下一場重生一份長得一樣的。
- **臨時標註**（callout、引線、說明字）退場 SHOULD 用縮小加淡出；**結論物件** SHOULD 複製一份連同標籤飛到角落縮成 inset，當後續步驟的常駐提醒。
- 一幕的**最後一場 SHOULD 與第一場同構**（物件歸位、結論獨立成句），形成閉環。
- 場與場之間 SHOULD 用交叉溶接（新場先以低透明度鋪在下層），同一坐標系與釘住的標題 MUST NOT 換位置。

**證據。** A2 從 12 s 到 144 s 是同一張畫布：65 s 小三角形複本飛去右上角當 inset、74 s 放大鏡、97 s 圓退場三角形滑成並排、129 s 三角形滑回圓上、末幀與開場同構。A1 只有兩個舞台（單位圓加 inset、正弦圖）來回三次，989 s 交叉溶接時左上 `f(θ)=sin(θ)` 不動，995 s 重播 851 s 的畫面與逐字動作做回扣。C1 定義式 675 到 750 s 停在頂端、下方工作行才變；雙圖物件 1277 s 與 1505 s 兩度回歸，只換頂端式子。B1 不做物件飛行，靠一個機器盒圖示（徽章→動機卡→定義卡縮小召回）與固定版面（①②③ 側欄、便條紙色塊換色）撐連續感。

**落地。**
- 已有：`color_role` 讓推導列沿用圖的顏色（DESIGN.md「次輪」節，那裡稱它跨場延續的顏色面）；`{show scaffold.*}` 讓版面不變、物件晚到。
- 缺（原語 5 的物件面）：(a) 場級「攜帶」宣告——上一場的某個 block 在本場開場就在、位置由本場模板決定；(b) 「複本飛去角落」與「歸位」兩個 stock 動作；(c) 交叉溶接當場間預設轉場（現為淡黑 0.4 s，`timing`／`make.py compose`）。契約與欄位名由 DESIGN.md 定，本檔只要求語意。
- 便宜替代（B1 式）：每幕一個具象錨圖示，在動機卡、定義卡、recap 三處縮放召回；成本一張圖。

**驗收。** storyboard 可查：每幕至少一個承重物件跨場延續（攜帶宣告或錨圖示）。R2 導演鏡的「一場一張卡」類 finding＝0。同一幕內同一物件重生（連續兩場各自 FadeIn 同一張圖）＝finding。

### 規則 2　畫出來，只動變的 token

**規則。**
- 曲線 MUST 被畫出來（Create、由點走出、隨參數長），不是整條淡入；文字標題 SHOULD 逐字寫入（Write）。
- 式子從一列到下一列 MUST 只動變的 token：替換在原位 morph、插入時新 token 淡入且鄰居平移讓位、消去分兩段（被消項原地淡出讓讀者確認是哪兩項，存活項再平移合攏）。**整行 FadeOut 再 FadeIn 是反模式**。
- 填色 SHOULD 有方向（從角的頂點往外掃），與意義一致；引線 SHOULD 從對象本身畫出。
- 每步一行、舊行不清除，整題留在同一張畫布到最後加框（B1 419 s）。

**證據。** A1 810 s 正弦曲線由圓上的點走出、851 s 文字逐字寫入、943 s 小三角形飛出邊轉邊放大貼合成大三角形。C1 335 s 只有 n 在原位 morph 成 ½、其餘 token 不動；700 s 新 token 淡入、鄰居讓位；740 s 下一行從上一行 transform（中間幀字形重疊）。A2 21 s 三角形填色從頂點往右 wipe、31.8 s 引線從弧段彎出。B1 419 s 兩段式消去。

**落地。**
- 已有：`anim: transform`（`TransformMatchingShapes`，來源列退 muted）；`paced:` 的「隨旁白書寫」（`Write` 跨整拍、速率有上限）；graph 的 `create`／`grow` anim；`seconds: beat`。
- 缺：(a) token 級插入與兩段式消去（`transform` 現為整列字形配對，做不出「鄰居讓位」與「先淡出再合攏」的時序）；(b) graph 的 function plot 預設 `create` 而非 `fade`；(c) 引線與 wipe 填色是 hook 級，等 annotation 契約。
- **新稿 SHOULD 把 derivation 的 `anim: transform` 當預設**；既有 deck 維持 opt-in。

**驗收。** 新稿 derivation 場整塊淡入 ≤ 1 次（首列）。graph 場的曲線 anim 為 `create`／sweep／隨旁白長之一。

### 規則 3　框、放大鏡、調暗，不靠鏡頭

**規則。**
- 要看細節，第一選擇 MUST 是：主圖標一個小框、另開 inset 顯示同一區域的放大（主圖不縮放、不移動）；或主圖降到四到五成亮度、要看的位置套取景框、虛線導引到旁邊的鏡片。
- 即將變動的部位 SHOULD 先用框圈出當預備動作，再做代入或變形。
- 強調 SHOULD 用「物件短暫換高亮色並微放大再回復」（約 1 s），不加框、不加字、不動其他物件。
- 2D 場 MUST NOT 以鏡頭 zoom／pan 為第一選擇；用 zoom 時 MUST 同時把大尺度標籤淡出（label LOD），講完 MUST zoom 回主圖。

**證據。** C1 的 2D 場 61 幀零 zoom 零 pan；335 s 先藍框圈出係數再代入。A1 903 s 主圖小方框加右上白框放大鏡，inset 是活鏡頭（943 s 大三角形的頂角自動出現在 inset 裡）；928 s 三角形閃黃再回綠。A2 74 s 主圖調暗、小圓取景框、右側鏡片先鬼影再實體；50 s 是唯一用 zoom 的，且同時淡出大尺度標籤、65 s zoom 回來。

**落地。**
- 已有：`focus:`（每拍取代壓暗集合、場末還原、`save_state`／`restore`）；`anim: transform` 自動把來源列退 muted。
- 缺：(a) inset 放大鏡（graph 模板：指定資料座標矩形，右上開第二組 axes 顯示同內容並跟隨主圖更新）；(b) 「變動前框選」stock 動作（transform 前 0.4 s 畫框）；(c) 強調閃爍（`Indicate`）當 `focus:` 的一個變體。
- 原語 4 現有的壓暗方向正確；本檔把「inset」與「框選」也歸原語 4。

**驗收。** 每個 derivation 的結果拍與 graph 的關鍵拍有 `focus:` 或 transform 壓暗；R2 導演鏡「找不到重點／視線不知道看哪」類 finding＝0。2D 場出現 camera zoom 而無 label LOD＝finding。

### 規則 4　靜止是設計出來的

**規則。**
- 每段超過 **6 s** 的靜止 MUST 是有意的：要嘛是 `pauses:` 宣告的停頓（動作後留給旁白），要嘛那一拍被 `paced:`、sweep、`seconds: beat` 填滿。未宣告的長靜止＝缺陷。
- 動作 SHOULD 只在步驟切換時發生（A2 式：動完停 3 到 6 s 給旁白）；或圖跟旁白長（A1 式：每 8 s 都有東西在動）。兩種節奏都可，但每場 MUST 選一種並一致。
- 沿用 ⑧：每個 content 場 `longest_still_seconds` ≤ 12 s（0.05% 門檻量測，引用時兩個門檻都列）。

**證據。** A2 每步動作後有 3 到 6 s 完全靜止（3 s 抽樣中 54 到 63 s、108 到 126 s 幾乎無變化），動作只在步驟切換。A1 從 8 s 抽樣看每 8 s 內至少一個物件在動。C1 參數讀數會折返（220 s 的 0.10→0.03→0.48），推測是讓觀眾多看幾次。B1 一次動一個元素、動完就停。

**落地。**
- 已有：`pauses:`（純旁白變換，插靜音）、`paced:`（逐段攤在整拍）、`seconds: beat`、`rewatch_pack` 的 `longest_still_seconds`。
- 已接線（2026-09-13）：`make.py` 的 `[stillness]` advisory——「本場有 > 6 s 的拍既無 paced／sweep／`seconds: beat`、也無 `pauses:`」在 render 前就印出來；callable 動畫一律視為畫面自己在動（含 `anim: transform`，此為已知盲點）。

**驗收。** `longest_still_seconds` ≤ 12 s（沿用）；未宣告靜止 > 6 s 的拍＝0。

### 規則 5　語意色貫穿圖與式

**規則。**
- 同一節內，同一個變數或幾何量在圖、括號、軸標、填色、讀數框、式子 token 裡 MUST 用同一色；結論式的分子分母色 MUST 等於它們在圖上的括號色。
- 卡類型色（definition、theorem、example、caution 等）沿 Direction B 色軸；箭頭色 SHOULD 等於它指向的分類色，讓箭頭不必再加文字。
- 填色 SHOULD 少而固定：兩到三種填色全片對應固定物件，靠填色而非標籤分辨。

**證據。** A1 的 dθ 粉紅、d(sin θ) 綠、θ 黃，從 inset 的括號一路到 989 s 的結論式 `d(sin θ)/dθ = Adj./Hyp. = cos θ` 分子分母同色。C1 的 f 紅、x 綠、t 紫從式子到軸標到填色到讀數框全片一致。A2 只有兩種填色（深藍＝基準三角、深綠＝Δ 三角）。B1 箭頭色＝目標欄色（綠箭→BEST、黃箭→OK）。

**落地。**
- 已有：`color_role`（graph plot 一直有；derivation 列 2026-09-12 起可寫同一 role）；Direction B 色軸對位講義 `calcbook.sty`（⑨）。
- 缺：(a) deck 級變數色表（`meta` 下宣告「θ＝黃、dθ＝粉、…」）；(b) MathTex token 上色讀同一張表（`brand.math_line` 加 token→role 映射）；(c) graph 的軸標、填色、annotation 讀同一張表；(d) 箭頭色＝目標色的慣例寫進 annotation 契約。

**驗收。** 同一節內同一變數不得出現兩種色；`visual-frame-audit` 增一條（V 類，blocking）：結論式 token 色與圖上對應物件色不一致。

## 3. 產能與兩級製作

B1 證明只用四種動作（cross-dissolve、appear、箭頭 wipe、單段平移）就能撐起一致的 60 支，代價是放棄規則一到三。這給「模板層普遍有動」定了下限：**規則四與五是每場零成本的模板行為，MUST 全書一致；規則一到三每場至少做一處，其餘比照分段揭示**（B1 子代理的建議）。要往 A1／C1 靠的招牌場，再把規則一到三做滿。R7 兩級製作的裁決屆時以此為分界。

## 4. 驗收接線（2026-09-13 狀態）

- ✅ REWATCH rubric：finding 可標規則代號 **`rule: ML1`–`ML5`**（motion language；`R1–R5` 是鏡頭編號、`G1–G6` 是容量契約，故另取前綴；選填，R2 導演鏡 MUST 標、其他鏡 MAY），定義表在 [`REWATCH-REVIEW-RUBRIC.md`](content_scripts/_audit/REWATCH-REVIEW-RUBRIC.md)「輸出格式」的 `rule` 小節並逐字注入每鏡 prompt；`rewatch-findings.schema.json`／`rewatch_merge.py`（`by_rule`，不計 refuted／dup）／`rewatch_multilens.gen.py`（finding × 規則小表＋chip）同步。
- ✅ `visual-frame-audit`：規則 5 的色一致性＝VISUAL-FRAME **V10**（結論式 token 色對不上圖上物件＝blocking）；agent 提示、REVIEW_GATES、`critic.py` 的 V 範圍同步到 V1–V10。
- ✅ 規則 4 的未宣告靜止 advisory＝`make.py` `[stillness]`（`pipeline/stillness.py`，6 s，warn-only；DESIGN.md「motion primitive：`pauses:`」節）。
- ⏳ 規則 1 的攜帶宣告存在性：依附於尚未建的 `carry:` 欄位，併入 [`KICKOFF-motion-language-gaps.md`](KICKOFF-motion-language-gaps.md) T4-4。
- `rewatch_pack`：兩個門檻（0.2%／0.05%）並列輸出，已在 ⑬ 註明。
- **code 缺口（規則 1 到 3、規則 5 的變數色表）＝[`KICKOFF-motion-language-gaps.md`](KICKOFF-motion-language-gaps.md)**（T1 色表、T2 inset／框選／閃爍、T3 token 級變形與兩段式消去、T4 跨場攜帶、T5 三門檻對齊）。

## 附錄 A　替代方案研究摘要（2026-09-12）

起因＝使用者問「現有架構之外還有什麼方案」，動機收斂為「視覺精緻度想跟 YouTube 頻道看齊」。現行產線三層：內容層（內容稿、旁白、NFA）與音訊／計時層（MiMo TTS 加 stable-ts 強制對齊）**後端無關、值得保留**；只有視覺渲染層是 Manim 專屬。五個家族：

| 家族 | 代表 | 對視覺層的意義 | 裁決 |
|---|---|---|---|
| A 換引擎 | Motion Canvas／Revideo（TypeScript、即時編輯器、tex 分段 morph）、Remotion（React、授權待查） | 買到迭代速度與鏡頭；代價是視覺層重寫、MathJax 取代 pdflatex | 保留為選項 |
| B narrated slides | Beamer／Touying 直接吃 `.tex`，TTS 時間戳驅動 highlight（arXiv 2505.02966） | 最忠實最便宜，但正是六鏡批評的靜態語法 | 否決（不夠精緻） |
| C agent 起草 | TheoremExplainAgent、Code2Video、ManimAgent（2026-06） | 買到每小時嘗試次數；沒有規格時只會更快產出靜止畫面 | 保留為選項 |
| D 生成式影片／虛擬講者 | NotebookLM Cinematic Video Overviews、Veo 3.1／Sora 2、HeyGen／Synthesia | 式子渲染不可靠，只適合 B-roll | 否決（成本） |
| E 真人 | 講師錄旁白、手寫板、講課錄影 | 對齊產線不挑聲源，可直接換聲源；但不可版控 | 否決（成本） |

**引擎相關事實。** Manim Community 2026-08 起大重構、暫不收新功能（README）；四支參考影片顯示規則在 Manim 裡都有現成原語。**若日後證明瓶頸是迭代慢**（render 才看得到），先試 A′：留在 Manim、把 `scratch_frames.py` 做成場級秒回預覽或用 manimgl 互動模式；A′ 不夠再考慮 Motion Canvas。**A 與 C 正交**：A 管引擎與迭代迴圈，C 管誰來寫；兩者都需要本檔這份規格。

頂級頻道的工具：3Blue1Brown＝Manim（互動迭代）；Mathologer＝Keynote 加 Illustrator；Kurzgesagt＝Illustrator 加 After Effects（一支 10 分鐘約 1200 小時）；Primer＝Blender 加 Unity；Mathemaniac＝PowerPoint、GeoGebra、Mathematica（頻道自述）；Ghrist＝PowerPoint 加 Illustrator。共同點是即時預覽下的大量迭代、一雙設計師的眼睛、每分鐘投入的小時數，不是引擎。

## 附錄 B　參考影片清單（2026-09-12 核過連結）

使用者選定並已拆解：
- **A1** [3Blue1Brown, Derivative formulas through geometry（Essence of Calculus ch3）](https://www.youtube.com/watch?v=S0_qX4VJhMQ)，Sine 段 12:36–16:56，Manim。
- **A2** [Think Twice, Visual Calculus: Derivative of sin(θ) is cos(θ)](https://www.youtube.com/watch?v=R4o7sraVMZg)，3B1B 在 A1 說明欄推薦，工具推測 PowerPoint 或 AE。
- **B1** [Prof Ghrist Math, Calculus Chapter 2 Lecture 10 Derivatives](https://www.youtube.com/watch?v=TUV6dOJzpkA)，PowerPoint 加 Illustrator；整門課 [播放清單](https://www.youtube.com/playlist?list=PLKc2XOQp0dMwj9zAXD5LlWpriIXIrGaNb)。
- **C1** [Morphocular, What Lies Between a Function and Its Derivative?](https://www.youtube.com/watch?v=2dwQUUDt5Is)，Manim（信心約 85%）。

其他候選（未拆解）：3B1B [ch4 chain rule](https://www.youtube.com/watch?v=YG15m2VwSjA)、[ch7 limits／ε-δ](https://www.youtube.com/watch?v=kfF40MiS7zA)、[Essence of Calculus 全系列](https://www.youtube.com/watch?v=WUvTyaaNkzM)；[Dr. Trefor Bazett Calculus I 62 堂](https://www.youtube.com/playlist?list=PLHXZ9OQGMqxfT9RMcReZ4WcoVILP4k6-m)；[Mathemaniac](https://www.youtube.com/@mathemaniac)（PowerPoint 上限）；[Mathematical Visual Proofs](https://www.youtube.com/@MathVisualProofs)（manimgl、無旁白）；[Mathologer](https://www.youtube.com/channel/UC1_uAIS3r8Vu6JjXWvastJg)（Keynote）；中文：[漫士沉思录 火柴人解析(下) 導數與泰勒展開](https://www.youtube.com/watch?v=m14GE_wpHko)、[马同学图解数学 微积分基本定理](https://www.youtube.com/watch?v=p9KkjRdvhQw)、[數學老師張旭 夾擠定理](https://www.youtube.com/watch?v=sTvtt4K85s0)（台灣現況對照組）。

## 附錄 C　工具與重現

[`experiments/reference_frames/`](experiments/reference_frames/)：`yt_frames.mjs`（headless Chrome 走 CDP 從播放器 `<video>` 畫布抓幀，**不下載影片**）、`sheet.py`（contact sheet）、`build_html.py`（合成對照表）、四份 `analysis.json`（子代理的時刻與判斷，含每個時刻的秒數，可重抓）、`synthesis.html`（主代理綜合判定）。幀不進版控；用法與已知行為見該資料夾 README。子代理 prompt 的要點：只寫幀上看得到的證據、五個維度只用固定詞彙、`maps_to_ours` 只能選我方場景 id、不確定標「推測」。
