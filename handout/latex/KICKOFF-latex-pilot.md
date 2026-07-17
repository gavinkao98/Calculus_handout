# KICKOFF — HTML→LaTeX 出版排版 pilot v2（appB 端到端・模板先行）

> **📦 2026-07-17 資料夾重整註記**：pilot 收案同日，`handout/` 依兩線分工重整——本線原路徑
> `handout/tex_export/` 更名為 **`handout/latex/`**（本檔隨之遷入）；fragment／standalone／
> `_render`／`_audit` 等撰稿資產移至 **`handout/html/`**（standalone 集中進 `html/standalone/`）。
> 同日稍後本線再**依章整理**：DIALECT-*.md／章 driver .tex／對照報告（含 img）／figs 各歸
> `chapters/<ch>/`（線導覽與章節狀態表見 [`README.md`](README.md)）。
> 本檔內文路徑已同步改寫（原貌見 git 歷史）；歷史敘述中的「`latex/`」在當時名為 `tex_export/`。
> **⚠️ rollout 時點已被同日「兩線分工」拍板調整**（見 [`../PIPELINE.md`](../PIPELINE.md)
> §出版排版線）：整體先做 HTML 講義、逐章轉換跟定稿走——supersede 本檔 §9「GO 即全面
> rollout」的時點含義；§9 的建議順序與 D1–D10 決策本身不變。

> **✅ PILOT 結果（2026-07-17 收案）：GO，全面 rollout。** M-B0–M-B4 全部完成；使用者逐項拍板
> 模板（sampler v4，`template/M-B1-DECISIONS.md`）、檢視對照報告後裁決 GO。交付物：
> `build/appB/appendixB.pdf`（**14 頁 vs HTML 20 頁**，四閘全綠：0 error／0 missing char／
> 0 overfull／散文 0 真落差／數學 317/317 逐位元組）、`template/calcbook.sty`（語意層＋樣式層）、
> 重定向後 `convert.py`（tests 79/79，appB 差集 mapping 全入）、
> `chapters/appB/REVIEW-latex-pilot-appB.html`（對照報告，含三輪 Codex gate-2 紀錄與處置）。
>
> **⚠️ 上段是 pilot 收案當時（5 節 appB）的數字，已被內容變更取代。**
> **2026-07-17 稍晚**：appB 新增 §B.6「Writing a Proof」、附錄改名 **Reading and Writing Proofs**
> （內容側閘鏈見 [`../html/_audit/REVIEW-appendixB-b6-applied.html`](../html/_audit/REVIEW-appendixB-b6-applied.html)），
> 轉換線隨之重跑並**重新凍結**：**24 頁**、四閘仍全綠（0 error／0 missing char／0 overfull／
> 0 underfull／散文 0 真落差／數學 **545/545** 逐位元組、tests **81/81**）；
> 成品 `dist/appB/`（pdf＋自足 tex）已更新；方言凍結表見 `chapters/appB/DIALECT-appB.md`
> 的「2026-07-17 重新凍結」段（**35 種組合，＋1＝`p.page-break-before`**，M-B2 已補 mapping）。
> 模板連帶修一項：`\cb@needspace` 的誤觸發（人眼閘抓到；沿革見 `template/M-B1-DECISIONS.md` v6）。
> 工程要點（rollout 沿用）：needspace 套件的誘餌斷點病理改 `\cb@needspace` 硬檢查
> （calcbook.sty 註解有 `\tracingpages` 證據）；style 白名單收口 parser 層＋重複屬性硬錯；
> M-B0 對 §1 初步盤點的更正見 `chapters/appB/DIALECT-appB.md` §6。v1 `shell/` 已歸檔
> `_dev-archive/tex_export-v1-shell/`。後續＝§9 rollout（屆時另開計畫）。

> **給新 session 的開場**：本檔是 2026-07-15/16 兩輪討論的完整交接（v2）。接手流程——
> ① 先讀本檔全文；② 再讀 [`../html/CONTRACT-html-writing.md`](../html/CONTRACT-html-writing.md)（輸入方言契約）、
> [`../html/TYPESETTING_GUIDE.md`](../html/TYPESETTING_GUIDE.md) §9（版心／字體拍板）、[`../../CLAUDE.md`](../../CLAUDE.md)（行為準則，尤其「缺套件先問」「commit 需授權」）、
> `chapters/ch03/DIALECT-ch03.md`（v1 盤點格式範例）；③ 從 **M-B0** 開始按 §5 推進。
> **不要重新辯論已拍板決策（§2）**；發現本檔與 repo 現況矛盾時，停下來向使用者回報。
> 分支：**已在 `handout/latex-pilot`**（v1 執行 session 所開）；繼續用它。
> ⚠️ **M-B1 模板設計是互動milestone**：必須用 `grill-me`／`superpowers:brainstorming` 這類互動 skill 與使用者逐項討論、看樣張拍板（D10）——**不得自行定案然後直接往下做**。

---

## 0. 沿革：v1 → v2（為什麼改道）

- **v1（converter-first，ch03）**：2026-07-15 grilling 拍板、07-16 凌晨另一 session 執行，**已做到 review 階段**——產物全在 `latex/`：`convert.py`（IR＋emitter＋單趟數學 scanner）、`test_convert.py`（605 段數學逐位元組驗證）、`dialect_inventory.py`、`check_prose.py`（pdftotext 散文子序列閘）、`export_figs.mjs`＋`chapters/ch03/figs/`、`shell/`（book class preamble）、`build/chapter3.pdf`、`chapters/ch03/REVIEW-latex-pilot-ch03.html`（對照報告）。
- **2026-07-16 使用者裁決轉向 v2**：v1 的病根是把設計權威掛在「復刻 HTML 現況」（`\documentclass{book}`＋legacy 復活＝「強硬轉換」的味道）。使用者要的是——**LaTeX 模板自己是第一公民的書籍設計；HTML fragment 只是語意內容源，倒進模板**。同時 pilot 對象改 **appB**（無圖、無表＝最乾淨的模板設計畫布），且模板設計過程必須互動拍板（D10）。
- **v1 產物的地位**：保留、不刪、不重跑。轉換器機器（scanner／IR／測試／完整性閘）是 v2 的重用資產；`shell/` 的樣式層被 v2 模板取代；ch03 成品降為參照。

## 1. 背景與已查證事實

使用者原始訴求：不想再手動微調排版；**終極目標是出版級品質**。手動微調稅的根源＝瀏覽器天生缺印刷排版機能＋10 個 standalone 的 shell 已漂移。已查證事實（新 session 不必重查）：

- **Shell 漂移**：分頁器 3 變體（ch1＋appA–D／ch2／ch3–6）；`page-break-before` 只有 ch1＋附錄支援，ch2–ch6 寫了靜默失效；附錄複製了 ch1 的 28 個死 `--fig-1-*` 變數。
- **斷字規則全死**：`.skin-hs .page { hyphens:auto }` 構不到成品頁（`.page` 只在離屏量測區）；CDP 實測成品 `hyphens:"manual"`，10 檔全中。且 Chrome 斷字字典是 per-profile component（headless gate 環境沒有）→ 瀏覽器路線的分頁不可重現。此問題在 LaTeX 側原生消失。
- **手動微調稅 ↔ TeX 內建機能對映**：Knuth-Plass 全段斷行、Liang 斷字、分頁 penalty／glue、float placement、`\label`/`\ref`——瀏覽器全缺。
- **環境**：MiKTeX 26.2（latexmk 4.88、LuaHBTeX 1.24）在機且 doctor 有查；`pdftotext` 可用（v1 完整性閘已實跑）。legacy preamble 六件式在 `legacy/tex_handout/preamble/`（**v2 降為參照，不復活**）。
- **內容 QA 閘鏈與排版引擎無關**：數學／散文／難度閘讀 fragment 源；圖閘審圖不審頁。
- **appB 初步盤點（2026-07-16，M-B0 正式凍結）**：5 個 fragment（`sec-b-1` 含 3 個 article＝附錄開場變體）；env 家族＝definition／example／solution／**strategy**／caution／proof／proposition／remark＋`workedexample`×2；特有 class＝`steps`、`sol-list`、`env-name`；`style="text-align:center;"`×5（sec-b-3）；aligned×1；**0 圖、0 表**。與 DIALECT-ch03 的差集（strategy／steps／sol-list／env-name／inline center／附錄開場）即 M-B2 要補的 mapping。

## 2. 拍板決策紀錄（D1–D8＝2026-07-15；D5 改版＋D9／D10＝2026-07-16。不再重議）

| # | 決策 | 內容與理由 |
|---|------|-----------|
| D1 | 目標＝消滅手工排版稅，終點＝出版級品質 | 內容閘鏈是品質來源，排版外包給真正的排版引擎 |
| D2 | **排版的家＝LaTeX，現在就定**（不等內容凍結） | fragment 仍為唯一內容源；HTML 降級為撰稿預覽＋圖閘 render 載體 |
| D3 | 路徑＝**確定性轉換**，fragment 不改寫、禁止人工重打 | 數學 pass-through 零翻譯風險；人工轉寫＝雙源漂移＋每頁忠實稽核成本＋中途換創作棧，三重否決 |
| D4 | 目標語言＝**LaTeX（lualatex）**，不是 Typst | Typst 要翻譯數學＝風險押錯地方；出版社收 LaTeX；IR／emitter 分層留 Typst 退路 |
| D5′ | **pilot 對象＝appB**（取代 v1 的 ch03） | appB 無圖無表＝模板設計最乾淨畫布；5 節短、服務性附錄風險低；ch03 v1 產物保留為參照與回歸素材 |
| D6 | 原 HTML 排版強化計畫降級／取消 | 統一模板「做法 B」不做；`&shy;` 注入不做；HTML 已知缺陷留檔不修，維持「預覽夠用」 |
| D7 | 編號策略＝**照抄字面**，不開 auto-counter | fragment 手動 ledger 是編號唯一真實來源；`\label`/`\ref` 語意化是未來獨立 workstream |
| D8 | 圖的擺放＝就地不浮動（non-float） | 本 pilot 無圖，原則保留給 rollout；理由不變（作者刻意貼齊＋字面圖號） |
| **D9** | **模板先行、語意層分離**（v2 核心） | LaTeX 模板是第一公民的書籍設計：模板定義語意指令（`\begin{workedexample}`、strategy 環境、`\readingtrack{…}` 等），轉換器**只射語意指令、不知道樣式**。改設計只動模板、不碰轉換器；Typst 退路同受益。設計**錨定現行 HTML 視覺語言**（使用者 2026-07-16 表示大致滿意：150mm 版心／12pt NCM／密度取向／env 視覺家族），在此基礎上做「書籍化」精緻提案，不是砍掉重練 |
| **D10** | **模板設計必須互動拍板** | M-B1 全程用互動 skill（`grill-me`／`superpowers:brainstorming`；環境沒有就用等效的逐題訪談）與使用者討論：class 選型、chapter／section 樣式、env 框線語彙、頁眉頁碼、字級節奏——逐項給選項＋建議。**sampler 樣張未經使用者拍板，不得進入 M-B2** |

**期望管理（不變）**：換 LaTeX 後仍殘留的手工＝寬顯示式手動斷行（TeX 本質；既有 `aligned` 1:1 繼承）、圖尺寸美學判斷（rollout 起）、編號 ledger 手動（D7）。新增責任＝轉換器維護（契約新 markup 須同步 mapping；契約從此被機器強制）。

## 3. Pilot v2 目標與完成定義（DoD）

**交付物**：
1. **模板 sampler**（手寫 showcase，5–8 頁：附錄開場、節標題、appB 全部 env 家族、workedexample、steps／sol-list、aligned、reading-track）——M-B1 拍板用。
2. `appendixB.pdf`——appB 全篇出版樣式 A4 PDF（lualatex）。
3. 模板（語意指令層＋樣式層分離的 `.sty`/preamble）＋重定向後的轉換器。
4. 對照報告（HTML render vs PDF 抽樣並排，standalone HTML，照「打開就能讀」慣例；範本＝`chapters/ch03/REVIEW-latex-pilot-ch03.html`）。

**DoD**：
- **sampler 經使用者拍板**（前置閘，D10）。
- `latexmk -lualatex` 0 error、0 missing character；overfull hbox >2pt＝0（或逐條列出待裁決）。
- 轉換器對 appB 全節點 100% 交代（mapped 或白名單 skip，fail-loud）；`check_prose.py` appB 子序列閘通過；數學逐位元組測試綠（沿 v1 `test_convert.py` 機制擴 appB）。
- appB 全頁人眼過一遍；抽樣公式（含該 aligned）與 HTML render 並排無語義差異。
- 使用者過目 PDF 拍板：**GO（全面 rollout）／NO-GO（回兩階段案）**。

## 4. 技術設計

### 4.1 目錄佈局（2026-07-17 依章整理後的現況；pilot 當時樣貌見 git 歷史）

```
handout/latex/
  README.md             # 線導覽＋章節狀態表（哪章的 LaTeX 講義在哪、怎麼建置）
  convert.py            # v1 資產：IR＋emitter＋數學 scanner（M-B2 已重定向 emitter）
  test_convert.py       # v1 資產：golden tests＋數學逐位元組驗證（M-B2 已擴 appB）
  dialect_inventory.py  # v1 資產：方言盤點器（rollout 逐章跑）
  check_prose.py        # v1 資產：pdftotext 散文子序列閘
  export_figs.mjs       # v1 資產：圖匯出（rollout 首個有圖章驗收）
  template/             # 共用模板（樣式層＋語意指令層；sampler.tex＝拍板樣張）
  chapters/             # 章節資產各住一夾：DIALECT-<ch>.md＋driver .tex＋對照報告＋figs
    ch03/               #   v1 參照章（DIALECT、figs 匯出樣張、對照報告）
    appB/               #   pilot 章（DIALECT、appendixB.tex driver、對照報告）
  build/                # lualatex 工作目錄（gitignored；PDF 產物按章 build/<ch>/）
  _dev-archive/         # v1 book-class shell 歸檔
```

### 4.2 模板（第一公民；M-B1，互動）

- **兩層分離**：`語意層`（`\begin{workedexample}`、appB env 家族環境、`\readingtrack{…}`、附錄開場指令——**名稱與清單在 M-B1 與 mapping 表一起凍結**）＋`樣式層`（這些指令長什麼樣）。轉換器只認語意層。
- **class 選型**：起手建議 `memoir`（chapterstyle／pagestyle／caption 工具單包整合、書籍設計自由度最大）；`scrbook` 備選。**選型本身是 M-B1 第一個互動議題**，用 sampler 同一份內容雙排比較亦可。
- **設計錨（D9）**：A4、版心 150mm（`left=32mm, right=28mm`）、12pt NCM（`fontspec`＋NewComputerModern；optical size 對映 HTML "Serif 10" 微調）、**leading 換算**：HTML `12pt×1.55≈18.6pt` ⇒ 約 `\linespread{1.28}` 起點視覺微調（別照抄 CSS 數字）、密度取向（講義每頁多塞的拍板不變）、microtype 全開（protrusion＋expansion）、running header／頁碼對映現行 sheet-header／footer 語彙。
- **互動議題清單（M-B1 逐項過，附建議案）**：class 選型／chapter＋附錄開場樣式／sec-head 與 kicker 的書籍化處理／env 家族框線語彙（現行 HTML 的視覺家族 vs 書籍慣用的 rule-based 輕量化）／workedexample 與 solution 的視覺關係／steps・sol-list 清單樣式／UI sans 字體（裝 Inter 或用 NCM Sans——**裝字體先問**）／頁眉頁碼式樣。
- legacy `theorem_setup.tex` 等六件式＝**參照素材**，可抄想法、不整檔復活。

### 4.3 轉換器（M-B2；重用 v1，重定向）

- **不重寫**：單趟數學 scanner（已處理 `<`／`&`／`\\[2pt]`／巢狀分隔符／entity 反斜線等坑）、IR、fail-loud、coverage 統計、golden test 機制全部沿用。
- **兩件事**：① emitter 重定向——輸出 M-B1 凍結的語意指令（不再輸出 v1 book-class 標記）；② 補 appB 方言差集 mapping（strategy／steps／sol-list／env-name／inline center style／附錄開場變體），依 M-B0 的 DIALECT-appB.md 為權威。
- **鐵律不變**：數學 pass-through 逐位元組；fragment 唯讀；表外標記硬錯；編號照抄字面（D7）。

### 4.4 圖匯出（本 pilot 不動）

appB 無圖。`export_figs.mjs`＋`chapters/ch03/figs/` 保留原樣；正式驗收移至 rollout 首個有圖章（屆時沿 v1 的 Chrome print-to-pdf 路線，fallback 需新安裝先問）。

### 4.5 驗收 gates（pilot v2）

0. **sampler 拍板閘（前置，D10）**：使用者未拍板不進 M-B2。
1. **編譯閘**：`latexmk -lualatex` 0 error；0 missing character。
2. **版面閘**：overfull `\hbox` >2pt＝0；underfull 逐條目視。寬顯示式維持手動斷行政策。
3. **完整性閘**：coverage 100%＋`check_prose.py` appB 通過＋數學逐位元組測試綠。
4. **人眼閘**：appB 全頁看一遍；抽樣公式並排比對。
5. **交付**：PDF＋對照報告 → 使用者 **GO／NO-GO**（流程明定使用者裁決項）。

## 5. Milestones（v2；M-B* 以別於 v1 的 M-P*）

| M | 內容 | 驗證點 |
|---|------|--------|
| M-B0 | appB 方言盤點：`dialect_inventory.py` 跑 appB → `chapters/appB/DIALECT-appB.md`（含與 ch03 差集、語意指令需求清單） | 盤點落檔；差集清單凍結 |
| M-B1 | **模板設計（互動）**：class 選型＋設計議題逐項討論（D10 的 skill 互動）→ 手寫 `sampler.tex` → 使用者看樣張、逐項拍板；必要時迭代 | **使用者拍板紀錄在案**（哪版、改了什麼） |
| M-B2 | 轉換器重定向＋appB 差集 mapping；golden tests 更新＋數學逐位元組測試擴 appB | tests 全綠；appB 轉出 `.tex` 無硬錯、無表外標記 |
| M-B3 | 組裝編譯＋QA：編譯／版面／完整性／人眼四閘＋對照報告 | §4.5 閘 1–4 全過 |
| M-B4 | 交付 GO/NO-GO；文檔收尾：本檔補 pilot 結果、`README.md`／`PIPELINE.md` 補「LaTeX 排版線」一節、`ENVIRONMENT.md`／`doctor.py`（若有新件，含 pdftotext 查核項）、v1 `shell/` 歸檔 | 使用者裁決紀錄在案 |

## 6. 風險與對策

- **順序鐵律**：sampler 拍板前寫轉換器 emitter＝白工風險（v1 已示範）。M-B1 未關不開 M-B2。
- **模板完美主義蔓延**：M-B1 的目標是「拍板一版夠好的起點」，精修留給逐章 rollout 的實戰回饋；單輪互動議題以 §4.2 清單為界。
- **emitter 重定向弄壞既有正確性**：v1 測試資產是保護網——重定向前先跑綠、改完必須仍綠（數學逐位元組尤其）。
- **appB 太乾淨、代表性不足**（無圖表＝pilot 沒壓到圖表路徑）：接受——pilot 驗「模板＋轉換器核心＋流程」；圖表在 rollout 首個有圖章（建議 ch03，資產現成）補驗。
- **pilot 失敗退路**：回「HTML Tier-1 強化＋內容凍結後再轉」兩階段案；§1 調查結果屆時直接可用。

## 7. 範圍外（pilot v2 明確不做）

TOC／index／bibliography、`\label`/`\ref` 語意化、float 政策、prepress（CMYK／PDF/X／出血）、其他章 rollout、**ch03 全章重跑**（v1 產物保留參照即可）、圖匯出正式驗收（rollout）、HTML shell 修繕（D6）、Paged.js／Vivliostyle（已否決）、Typst emitter（僅留 IR 退路）。

## 8. 環境與同意事項

- 全程無計費 API：lualatex／headless Chrome／node／pdftotext 皆本地免費。Codex read-only review 有 standing consent（建議 M-B1 模板設計案＋M-B3 結果各跑一輪 gate-2 覆核）。
- **可能的新安裝（逐項先問再裝）**：Inter 桌面字體（M-B1 UI sans 議題）；其餘 v1 已打通、無新件。裝了同輪更新 `ENVIRONMENT.md`＋`doctor.py`。
- **commit 紀律**：經使用者授權才 commit；訊息繁中、body 記裁決。目前整個 `latex/`＋本檔均未 commit——**建議 M-B0 前先請使用者授權 commit 一次 v1＋v2 kickoff 快照**（換機保險）。

## 9. Pilot 通過後的 rollout 預告（屆時另開計畫）

逐章轉換（建議順序：ch03〔圖表補驗，資產現成〕→ ch01→ch06 → 其餘附錄；每章：方言差集→補 mapping→四閘）→ 書級組裝（`main.tex`、TOC、頁碼連續）→ HTML 線正式降級公告（PIPELINE.md 改記「排版閘＝LaTeX 側」、`linebreak-gate` 退役）→ 出版定版期再議：`\label`/`\ref` 語意化、float 政策、prepress 規格。

---

*v1：2026-07-15 grilling session 產出（converter-first，ch03）。v2：2026-07-16 使用者裁決改道（模板先行＋appB＋互動拍板），同日更新本檔。實測證據（CDP 探針、hyphen-data 對照、shell 漂移 diff）見 2026-07-15 對話；v1 執行產物見 `latex/`。*
