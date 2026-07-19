# M-B1 模板設計拍板紀錄（LaTeX pilot v2）

> [`../KICKOFF-latex-pilot.md`](../KICKOFF-latex-pilot.md) M-B1 的裁決落檔（D10：模板設計必須互動拍板）。
> 訪談形式＝kickoff §4.2 議題清單逐項過（每題選項＋建議，使用者逐題點選）。
> 拍板日：2026-07-16。設計錨＝現行 HTML 視覺語彙（`html/standalone/appendixB-print-standalone.html` CSS 盤點），依 D9 錨定＋書籍化精緻。

## 1. 八議題拍板

| # | 議題 | 拍板 | 內容 |
|---|------|------|------|
| ① | class 選型 | **memoir** | 書籍設計工具單包內建（chapterstyle／pagestyle／caption／keep-together），不拼 titlesec／fancyhdr；lualatex＋fontspec 成熟 |
| ② | 章／附錄開場版式 | **緊湊對映** | kicker→標題→lead→objectives 連排、開場完直接接第一節（密度取向不變）；書籍化花在印刷細節（kicker 真字距、objectives 懸掛縮排） |
| ③ | 節標題書籍化 | **溫和書籍化** | 語彙照舊（淡灰上緣 rule＋藍色節號＋serif 粗體標題——HTML 的 600 由瀏覽器合成，NCM 無 semibold、以 Bold 落地），字級收斂：節 ≈20pt、章／附錄標題 ≈26pt（現行換算 24pt／30pt 偏網頁尺度） |
| ④ | env 家族框線語彙 | **忠實對映** | 左緣色線＋pill kicker（實心／outline 兩態）＋caution・strategy 染色卡片照搬；色彩家族 oklch→sRGB 精確換算進 xcolor |
| ⑤ | workedexample 分頁 | **可斷＋頭部保護** | 群組可跨頁（綠線兩頁續接），kicker＋首 2–3 行不孤懸頁尾（needspace 級保護） |
| ⑥ | steps／sol-list 清單 | **樸素＋懸掛對齊** | steps 數字粗體（NCM Bold，同上無 semibold）＋懸掛縮排；ul／sol-list 藍色 bullet 照現況；run-in 標籤→粗體；不加家族色系統 |
| ⑦ | UI sans 字體 | **vendored Inter** | rsms/inter 官方 release 下載（使用者同意），OFL 字體檔進 repo＋`fontspec Path=` 載入；換機零安裝；與圖內已嵌 Inter 一致 |
| ⑧ | 頁眉頁碼式樣 | **節級動態頁眉** | 頁眉隨當頁內容顯示「節號 · 節題」（LaTeX 原生能力，HTML 現況為章級靜態）；頁碼置中頁底、章首頁不印頁眉的慣例保留；twoside 留書級組裝再議。tie-break＝該頁新開節優先（LaTeX 書籍標準慣例，gate-2 B4） |
| ⑨ | 行距（2026-07-17 經典教科書對標訪談） | **16pt** | 12pt 本文、倍率 1.33＝數學教科書經典帶（近 10/12 傳統）；捨 HTML 的 18.6pt（1.55 網頁節奏），換每頁 39→45 行（＋15% 密度）。lead 段行距等比收斂 17pt |
| ⑩ | 上下邊距（同上訪談） | **上 17／下 23mm** | 總 40mm 不變（零密度成本）；書籍式下緣配重取代 HTML 均等 20/20。行寬 150mm 與字級 12pt 經對標討論後**維持既有拍板不動**（150mm 另為圖 px→mm 換算基準，有技術耦合） |

## 2. 語意指令詞彙表（D9 凍結——轉換器 emitter 的目標語言）

轉換器只射下列指令、不知道樣式；樣式全在 `calcbook.sty` 的樣式層。args 一律**字面照抄**（D7：無 counter）。

| fragment 標記 | 語意指令 |
|---|---|
| 開場（`header.chapter-head`＋kicker＋title） | `\appendixopener{Appendix B}{Reading and Writing Proofs}`；rollout 章＝`\chapteropener{Chapter 3}{…}` |
| `p.lead` | `\begin{lead}…\end{lead}` |
| `p.para-head` | `\parahead{…}` |
| `p.page-break-before` | `\pagebreakbefore`（**2026-07-17 擴充**，見下方註）——指令置於該段之前，語意＝**此段之前強制換頁**。樣式層＝`\par\ifdim\pagetotal>0pt\newpage\fi`，其中的 `\ifdim` 守衛刻意對映 HTML 分頁器的 `body.childElementCount > 0`（頁面已有內容才斷，不製造前導空白頁） |
| `header.sec-head`（`sec-no`＋title） | `\sechead{B.1}{Reading a Statement}` |
| `h3.subsec-head`（appB 未用） | `\subsechead{…}` |
| env 家族（10 類） | `\begin{envdefinition}{<kicker>}{<num>}{<name>}`…同構：`envdefinition`／`envtheorem`／`envproposition`／`envcorollary`／`envproof`／`envexample`／`envsolution`／`envremark`／`envcaution`／`envstrategy`。**三參數皆必填、可空 `{}`**（gate-2 B1：尾端 optional `[name]` 對機器 emitter 有歧義——body 首 token 是 `[` 會被吃掉；改 mandatory 後與 v1 emitter 輸出形一致）。kicker＝字面資料（`Pause` 照抄） |
| `div.workedexample` | `\begin{workedexample}…\end{workedexample}` |
| `ol.steps`／`ul.steps` | `\begin{steps}`／`\begin{bulletsteps}` |
| `ul.sol-list` | `\begin{sollist}`（env 內與散文位置同一環境） |
| 素 `ul`／`ol` | `itemize`／`enumerate` |
| 開場 objectives 清單 | `\begin{objectives}`（gate-2 B2：獨立語意槽，樣式現與 itemize 同貌、可單獨調而不動 emitter） |
| `figure[data-fig]`＋`figcaption`（appB 無、ch03 有） | `\begin{figureblock}`＋`\includegraphics[width=<mm>]`＋`\figcaption{<字面 fig-no>}{<caption>}`（gate-2 B3：D9 詞彙凍結須含 figure；non-float per D8，寬度由 emitter 依 `figures.json` 射 mm 值；視覺驗收仍留 rollout 首個有圖章） |
| `em` | `\emph{…}` |
| `strong` | `\runin{…}`（run-in 標籤語意；樣式層＝粗體） |
| `p[style="text-align:center;"]` | `\begin{centerstatement}…\end{centerstatement}`（內容可含 `\\`＝`<br>`） |
| `p.informal` | `\begin{informal}…\end{informal}` |
| `span.qed.qed-proof` | `\qedmark`（模板不自動補 □，記號驅動——DIALECT-appB §7） |
| reading-track 段（`p><em`，appB 未用） | `\readingtrack{…}` |
| `&ensp;`（U+2002） | `\enspace`（emitter 正規化，不賭字型） |

## 3. 版面常數（設計錨換算）

- A4；版心 150mm（`left=32mm, right=28mm`）；本文 12pt NCM（"Serif 10" optical→`NewComputerModern10` Regular，非 Book）；數學 `unicode-math`＋NewCM Math。
- Leading：HTML 12pt×1.55≈18.6pt ⇒ 起點 `\linespread{1.28}`（12×1.2×1.28≈18.4pt），樣張視覺微調——不照抄 CSS 數字（kickoff §4.2）。
- microtype 全開（protrusion＋expansion）。
- 頁眉：Inter ≈8.5pt 淡灰（#9AA0AC），對齊版心、baseline 距頁頂 ≈11mm；頁碼：Inter ≈9pt（#82868F）置中、距頁底 ≈8.5mm。
- 色彩（oklch→sRGB 換算值以 `calcbook.sty` 內註記為準；mix 值用 xcolor `!` 語法對映 CSS `color-mix(in srgb …)`）。

## 4. 待辦／待拍板

- [x] `sampler.tex` 樣張 → **使用者已拍板（2026-07-17，樣張 v4）**：判斷點 1–7 全數照樣張
      （段落模型＝書籍縮排式／標題 20·26pt／本文純黑／頁眉 incoming-section 慣例／qed 記號驅動
      ／行距 16pt／邊距 17·23mm）。使用者指示「進 M-B2」＝M-B1 收案；語意層詞彙（§2）就此凍結。
- [x] Codex gate-2 覆核模板設計案（standing consent，kickoff §8）——5B＋8A，逐條處置見 §6；
      五項 blocking 已於 sampler v3 全數關閉，修正後回歸覆核另跑（結果亦記 §6）。
- [x] Inter 下載（rsms/inter v4.1 release，六字重 OTF＋OFL 進 `fonts/inter/`，3.5MB）；
      同輪已更新 `ENVIRONMENT.md` §③b＋`doctor.py check_handout_latex`（跑過，區全綠）。

## 5. 樣張拍板紀錄（sampler 迭代時回填）

| 版 | 日期 | 變更 | 依據 |
|---|---|---|---|
| v1 | 2026-07-16 | 初版 9 頁；編譯閘全綠 | 八議題拍板落地 |
| v2 | 2026-07-16 | 開場 kicker 8.6pt→**11pt**（HTML 換算值印刷上過小） | 使用者看樣回饋 |
| v3 | 2026-07-17 | env 簽名改三 mandatory；補 `objectives`／`figureblock` 語意槽（＋ch03 真圖 demo）；補 `envcorollary` 樣例；補 **workedexample 跨頁 demo**（p9→10 綠線續接實證）；luacolor 修跨頁色彩；頁眉 tie-break 慣例記入 B.7；編譯閘全綠（10 頁） | Codex gate-2 五項 blocking（§6） |
| v4 | 2026-07-17 | **行距 18.6→16pt**（⑨）＋**上下邊距 20/20→17/23**（⑩）；lead 行距等比 17pt；B.7 判斷點清單同步改寫；跨頁 demo 重驗仍實斷（p8→9）；編譯閘全綠（**9 頁**——密度紅利實證） | 經典教科書對標訪談拍板 |
| v5 | 2026-07-17 | 開場 kicker 補 `\noindent`——kicker 段落誤吃全域 `\parindent` 1.5em、未與標題左齊（標題行的 `\raggedright` 會歸零縮排故看不出）；修後與 HTML 錨一致貼齊 | 使用者 GO 檢視時回報 |
| v6 | 2026-07-17 | **§2 詞彙表擴充一項：`p.page-break-before` → `\pagebreakbefore`**（appB §B.5 首用；語意＝此段之前強制換頁，守衛對映 HTML 分頁器的 `childElementCount>0`）。**`\cb@needspace` 修一個誤觸發**：頁面產生器是惰性的，`\pagetotal` 在前一段剛好撐爆頁面的時刻會**大於** `\pagegoal`（含下一頁材料），舊碼據此判「空間不足」而硬斷，留下只有一行的近空白頁；加溢出守衛後 appB 25→**24 頁**、近空白頁消失，且真·滿頁／真·不足的觸發不受影響 | appB §B.6 定稿時**人眼閘**抓到（版面閘的 overfull/underfull 抓不到分頁問題）；`\typeout` 逐次實測 17 次呼叫定位（#16 `pagetotal 739.87 > pagegoal 731.24`） |
| v7 | 2026-07-18 | **proof 內文改「塊狀段落」＋修行首殘留空白**（envproof 專屬 `\cb@proofparstyle`）——修 Prop B.4 歸納證明 *Base case*／*Inductive step* 兩**並列具名分部**的左緣不對齊。**兩件事一起落地：**（a）全域是 ② 的「書籍縮排式」（`\parindent` 1.5em、`\parskip` 0），proof 第二段（*Inductive step*）起會吃 1.5em 縮排、與貼左首段不對稱 → hook 內 `\parindent`→0、`\parskip`→`\medskipamount`，兩分部都貼左、以 `\medskip` 分隔（作用域由 `\begin/\end{envproof}` 群組界定、不外洩；段間設定只作用第二段起）。（b）(a) 使本 hook 由「空」變「非空」，**引爆一個既存潛在 bug**：`\cb@envhead` 尾端的 `\ignorespaces` 在 `\cb@mkenv` 裡排在 `#5` hook **之前**，hook 非空時 body 行首空白（`\begin{envproof}{…}` 後換行→空格）不再被吃掉、殘留成 **~4pt 行首縮排**（實測 pixel/vrule 定位：非側隙——italic B/I 側隙近乎相等、皆 ~0.8pt；純粹是這個 interword space；remark 因 `\small` 為 ~3.6pt）→ 在 hook 尾補一個 `\ignorespaces` 吃掉它。**(b) 採根治、全部 env 一起修**（使用者裁決）：把 `\ignorespaces` 從 `\cb@envhead` 尾端**移**到 `\cb@mkenv` 的 `#5` 後（`\cb@envhead` 自帶的那個保留不動——`envexample`／`envsolution` 直呼 `\cb@envhead`、不經建構器，靠它收行首空白）。於是 10 類 env 一律無殘留：空-hook env（definition／corollary／caution／strategy）由 `\cb@envhead` 收、輸出 **byte-identical**；非空-hook（theorem／proposition 的 `\itshape`、remark 的 `\small`、proof 的 `\cb@proofparstyle`）首段左移 ~4pt 貼齊。實測 page 7：Prop B.4 首行「For every positive integer *n*」849（貼左，原 ~+4pt）、Base case／Inductive step 皆 849。**四閘全綠（0/0 overfull/underfull）、25 頁不變、dist `.tex` 零變動**。(a) 的 `\cb@proofparstyle` 尾端 `\ignorespaces` 因根治而移除（改由 `\cb@mkenv` 統一處理）。性質＝② 全域縮排式的 **proof 內文 scoped 例外**（與 HTML 錨「垂直間距分段、貼左並列」一致）＋ env 首段 ~4pt 殘留空白的**根治**（所有 env 首行改與內文左緣齊）。**潛在 bug 溯源**：pixel/vrule 定位排除「側隙」假說——italic B/I 側隙近乎相等、皆 ~0.8pt；真兇是 `\begin{env}{…}` 後換行→空格，因 `\ignorespaces` 早於 `#5` 而殘留 | 使用者檢視 appB 排版：先問「*Inductive step* 為何被縮排」，(a) 落地後再回報「還是沒有對齊」→ 查出 (b) → 裁決根治全部 env |

**GO 裁決（2026-07-17）**：使用者檢視 appendixB 全篇對照報告後裁決 **GO（全面 rollout）** 並授權
commit 整條線；kicker 對齊為 GO 檢視時唯一回報項，已修。M-B1–M-B4 至此全部收案，
pilot 結果摘要見 [`../KICKOFF-latex-pilot.md`](../KICKOFF-latex-pilot.md) 頂部。

**頁數 waiver**：kickoff §3 寫 sampler「5–8 頁」；v3 為 **10 頁**——超出部分＝rollout 預覽頁（appB 未用槽位）、
跨頁行為 demo、判斷點清單頁，皆為拍板所需的展示面，非內容膨脹。記此為接受之偏離。

## 6. Codex gate-2 覆核紀錄（2026-07-17，read-only standing consent）

判定「5 blocking＋8 advisory、未關前不宜進 M-B2」。處置：

| # | Finding | 處置 |
|---|---|---|
| B1 | 尾端 optional `[name]` 簽名對 emitter 有歧義（body 首 `[` 被吃、name 含 `]` 提早閉合） | ✅ 已修：全家族改 `{kicker}{num}{name}` 三 mandatory（§2） |
| B2 | objectives 缺獨立語意槽（違 D9 分層） | ✅ 已修：`objectives` 環境（§2） |
| B3 | figure 語意 API 缺席（D9 凍結不完整） | ✅ 已修：`figureblock`＋`\figcaption`；sampler 以 ch03 真圖 demo |
| B4 | 動態頁眉行為與註解不符（`\rightmark`＝該頁第一個 mark→新開節優先） | ✅ 已修註解＋記入 B.7：此為 LaTeX 書籍標準慣例，採之 |
| B5 | 樣張沒展示 workedexample 跨頁（⑤ 無證據可拍板） | ✅ 已修：v3 p9→10 實斷（綠線續接＋頭部保護可見） |
| A1 | `parbox=false` 屬 tcolorbox experimental | 接受：sampler 即回歸樣例（清單／多段／跨頁全覆蓋）；rollout 遇異常再處理 |
| A2 | `\color` 跨 breakable 分頁在 LuaTeX 可能掉色 | ✅ 已修：載入 `luacolor`（attribute-based，根治） |
| A3 | `\pagetotal<1pt` 判頁首是 heuristic | 接受＋已註記；sampler 未見誤判，rollout 全章驗證 |
| A4 | Inter `Path=fonts/inter/` 綁編譯 CWD | 接受為技術債：M-B2 建置腳本固定從 `template/` 起跑；記於 sty 註解 |
| A5 | 拍板文字寫 semibold、落地是 NCM Bold | ✅ 已修文字（§1 ③⑥）：NCM 無 semibold，Bold 為正 |
| A6 | 「9 類」計數錯＋corollary 未展示 | ✅ 已修：10 類＋v3 補 corollary 樣例 |
| A7 | 頁數超出 kickoff 5–8 | ✅ 已記 waiver（§5） |
| A8 | gate-2 勾了卻沒記結果 | ✅ 本節即紀錄 |

**回歸覆核（2026-07-17，Codex read-only，對上表修正逐項驗證）**：

- **B2–B5＝closed**（逐項行號證據確認；p9→10 跨頁綠線續接、pill／綠線色值跨頁一致）。
- **B1＝not-closed**：功能歧義已關（sty／sampler 22 處呼叫／DECISIONS 三處一致），但 `calcbook.sty`
  一行註解殘留舊 `[name 選用]` 形式 → **已修**（該行改 `{name 可空}`）。
- **A5＝not-closed**：sty 清單註解仍寫 semibold → **已修**（改「粗體數字（NCM Bold）」）。
- **新 H1**：頁眉實高 14.5pt＞`headheight` 14pt，memoir warning ×2 → **已修**：`\setheadfoot{15pt}`，
  重編 warning＝0。
- **新 R1**：回歸紀錄未落檔 → 本段即補。
- 另確認：`luacolor`×tcolorbox×TikZ 無相容問題（`pdfcol` 停用訊息屬預期 Info）；`graphicspath`
  的 CWD 前提由既定建置契約涵蓋；79.90mm 的 manifest 來源鏈正確。
- 殘項修正後重編：**10 頁、0 error／0 missing character／0 overfull／0 underfull、0 headheight warning**
  （其餘 log Warning 僅 unicode-math 例行 info）。gate-2 至此**全數關閉**；sampler 進入待使用者拍板狀態。
