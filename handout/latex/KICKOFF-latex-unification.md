# KICKOFF — LaTeX 統一（HTML 撰稿線退役・LaTeX 升格唯一源）

> **本檔是什麼**：2026-08-09 使用者拍板「**講義線＋影片線以後都走 LaTeX**」的權威拍板紀錄
> ＋遷移計畫。**supersede 2026-07-17 的兩線分工拍板**（「整體先做 HTML 講義、定稿再轉
> LaTeX」，見 [`../PIPELINE.md`](../PIPELINE.md) §出版排版線）。前代 pilot 的 D1–D10 拍板
> （[`KICKOFF-latex-pilot.md`](KICKOFF-latex-pilot.md)）**除 D2 的「HTML＝撰稿預覽載體」
> 定位與 D7 字面編號被本檔 U1／U3 取代外，其餘照舊有效**（D3 確定性轉換、D4 目標語言、
> D9 語意層分離等仍是本線的地基）。
>
> **給新 session 的開場**：接手遷移時——① 先讀本檔全文；② 再讀
> [`KICKOFF-latex-pilot.md`](KICKOFF-latex-pilot.md)（模板與轉換器沿革）、
> [`README.md`](README.md)（線導覽）、[`../../CLAUDE.md`](../../CLAUDE.md)（行為準則，尤其
> 「commit 需授權」「Codex 逐次徵詢」）；③ 查本檔 §4 的階段狀態表看推進到哪。
> **不要重新辯論 §2 已拍板決策**；發現本檔與 repo 現況矛盾時，停下來向使用者回報。

## 0. 沿革：為什麼統一（2026-08-09）

2026-07-17 拍板的分工是「HTML＝撰稿製作線（內容、QA 閘鏈、圖系統），LaTeX＝定稿出版線
（逐章確定性轉換）」。一個月實跑下來（appB＋ch01–07 共 8 單元 rollout 四閘全綠）：

- **rollout 稅逐章重複**：每定稿一章都要付「方言盤點→補 mapping→四閘→對照報告」；
  ch9–16 還有 8 章＋3 附錄要付。
- **LaTeX 人眼閘實證抓到 HTML 線看不出的缺陷**（ch07 3 條，含 figcaption 整句重複）——
  品質錨其實已在 LaTeX 側。
- **雙線維護面**：兩套排版契約（CONTRACT-html-writing＋DIALECT 方言表）、兩套 render
  驗證、CI 只驗 HTML 側。
- **手動編號 ledger 是全 repo 公認「最大錯誤來源」**（Ch8 M4 為閃 30 個 cascade 重編號
  特意把 example 轉不編號段）；HTML 源永遠享受不到 auto-counter。

使用者裁決：**HTML 撰稿線退役，LaTeX 升格為唯一內容源＋唯一工作線；影片線的講義輸入
一併改錨 LaTeX**。

## 1. 已查證事實（2026-08-09 盤點；新 session 不必重查）

1. **dist 的 `.tex` 已是可讀的語意層 LaTeX**（`\sechead`、環境家族、散文直書、圖
   `\includegraphics`）——升格為源是「接管」不是「重寫」。8/12 單元已有（appB＋ch01–07，
   四閘全綠）；**缺 ch08（方言未盤）＋appA/C/D**。
2. **圖＝105 張 `data-fig`**，由 standalone 內 JS `FIGS` 函數畫 SVG，
   [`export_figs.mjs`](export_figs.mjs)（Chrome printToPDF）匯向量 PDF 給 LaTeX 嵌。
   **2026-07-26 起圖匯出字體與 LaTeX 同源**（local HTTP 供 `template/fonts/inter/` 完整
   OTF＋本地 NewCM；`check_glyphs.py` 逐字形驗）——圖 PDF 嵌的字體＝正文字體檔本身。
   單張圖與 TikZ 重畫在讀者眼裡無可辨差異；混棧（存量 JS＋新圖 TikZ）反而是唯一
   讀者可見的不一致風險。
3. **影片線對講義的依賴＝「人讀課文寫內容稿」＋`source:` 引用錨**（如
   `chapter1-print-standalone.html §1.1 · Definition 1.1`），無程式 parse——切換成本
   ＝改權威輸入指向＋引用格式。Manim 數學本來就是 LaTeX，同棧更順。
4. **`check_prose.py`（散文子序列閘）的存在意義是驗證「轉換不丟內容」**——fragment 退役
   後無轉換可驗，此閘隨 convert.py 一同退役（首轉期間仍用）。
5. **CI（handout-checks.yml）**現驗：quote_lint（HTML 散文曲引號）＋doc_lint＋build.py
   同步。LaTeX 編譯閘現為本地跑（MiKTeX 26.2）。
6. **審核交付物 standalone HTML（`REVIEW-*.html`，MathJax CDN 雙擊即開）是給使用者的
   報告載體**，與講義產線無關——慣例保留（[`../../CLAUDE.md`](../../CLAUDE.md) 拍板）。

## 2. 拍板決策（U1–U7＝2026-08-09 使用者裁決。不再重議）

| # | 決策 | 內容與理由 |
|---|------|-----------|
| U1 | **LaTeX＝唯一內容源；HTML 撰稿線退役** | `latex/src/<ch>/<name>.tex` 升格為手改／LLM 改的源；fragment 樹、`build.py`、standalone、paginator **凍結歸檔**（不刪，git 歷史＋對照材料）。內容 QA 閘鏈（數學／散文／難度／Mode A–C）全部改讀 `.tex` 源。supersede 2026-07-17 拍板與 pilot D2 的 HTML 定位 |
| U2 | **圖系統＝JS kit 縮編為畫圖工具** | 憑據＝§1-2（字體已同源、單張無差、混棧才有風險）。`FIGS`＋`buildPlot`＋CSS 抽出到獨立 **figs harness 頁**（每章一份、無課文），`export_figs.mjs`（LaTeX 嵌圖）＋`shot.mjs`（圖閘 PNG）＋`check_glyphs.py` 照舊吃 harness。新圖（ch9–16）繼續用 kit 畫。repo 保留 Chrome/node 圖工具是已接受的代價 |
| U3 | **編號語意化：auto-counter＋`\label`/`\ref`**（supersede D7 字面編號） | 徹底消滅手動 ledger 錯誤源；插入不再 cascade。做法＝一次性確定性轉換腳本（字面 `Example 8.3` → 環境 auto-counter＋`\label{ex:8.3}`；本章內文引用 → `\ref`），驗收＝**編譯輸出編號與現行 as-built ledger 逐一相同**。**跨章引用維持字面文字**（單章獨立編譯，不引 xr/zref 跨檔機制）。獨立 Phase 做，不與源接管混批 |
| U4 | **Ch8 三閘 gate-2 債＝切換後在 LaTeX 源上還** | gate-2 是 Codex 讀文字，載體無差；兼作新閘鏈（rubric 改讀 .tex 後）的首個實戰驗證。輸入含既有 7 條內容發現（`ch08_modec-gapcheck-audit.md` §8，含 Ch6 Thm 6.5「applies verbatim」跨章矛盾） |
| U5 | **影片線講義輸入改錨 LaTeX** | golden path 首格改 `latex/src/<ch>/<name>.tex`（或其 dist PDF）；`source:` 引用錨改「`chapter3.tex §3.1 · Definition 3.1`」格式。內容稿／storyboard／Manim／TTS 流程全部不動；narration 審核 HTML 照舊（U7） |
| U6 | **推進節奏＝pilot 先行（ch03）再全面切** | Phase 0 用 ch03（最小完整章、有圖、v1 參照章）驗證「源升格編譯＋圖 harness」兩條技術路徑，過了才進 Phase 1 |
| U7 | **審核交付物 standalone HTML 慣例保留** | `REVIEW-*.html`／narration 審核稿是「打開就能讀」的報告載體（CLAUDE.md 拍板），不隨講義產線退役 |

**期望管理**：換 LaTeX 源後仍殘留的手工＝寬顯示式手動斷行（TeX 本質）、圖尺寸美學判斷。
新增責任＝撰稿契約從 CONTRACT-html-writing 換為 **CONTRACT-latex-writing**（語意指令
白名單＝`calcbook.sty` 語意層；Phase 3 立檔）。消失的稅＝方言盤點／轉換 mapping／
build 同步 CI／手動編號 ledger（U3 後）。

## 3. 目標架構（端狀態）

```
handout/
  latex/
    src/<ch>/<name>.tex     # ★ 唯一內容源（升格自 dist 自足 tex；手改／LLM 改）
    template/calcbook.sty   # 模板（照舊；U3 時加 counter／\label 語意層）
    dist/<ch>/<name>.pdf    # 成品（latexmk 編譯產物；tex 側成品＝src 本身）
    chapters/<ch>/          # 章工作資產：figs/（匯出圖＋figures.json）＋DIALECT-*.md（凍結存檔）
    build/                  # gitignored 編譯殘渣
  figkit/                   # ★ JS 畫圖 kit：figs-<ch>.html harness＋共用 css/js
                            #   （export_figs.mjs／shot.mjs 的輸入；自 standalone 抽出）
  _audit/、_dev-archive/    # 活資產（rubric、REVIEW 報告、章 PLAN ledger）自 html/ 遷出
  html/ → 凍結歸檔（legacy 化；fragment＋build.py＋standalone＋paginator）
video/                      # 流程不動；講義輸入錨改 latex/src（U5）
```

閘鏈對映：編譯閘（latexmk 0 error/0 missing char）＋版面閘（overfull）＋字形閘
（check_glyphs）＝既有四閘留三；check_prose 退役（§1-4）；linebreak-gate／quote_lint 的
職能由 TeX 原生斷行＋LaTeX 契約 lint（Phase 3 改造 quote_lint 掃 .tex 散文）接手；
內容閘（數學 M1–M8／散文 S·A·V／難度 sim／圖 D1–D8）rubric 改輸入為 .tex／harness PNG，
判準不變。

## 4. 遷移階段與狀態（推進時同步勾選）

| Phase | 內容 | DoD（驗收） | 狀態 |
|---|---|---|---|
| **P0 pilot** | ch03 源升格（`dist/ch03/chapter3.tex` → `src/ch03/`）＋編譯三閘＋`check_prose` 對現行 fragment 跑 PASS（證升格無損）；圖 harness 自 standalone 抽出→`export_figs` 重匯→與 `chapters/ch03/figs/` 現品比對一致 | 三閘綠＋子序列 PASS＋圖匯出一致 | ✅ 2026-08-09（commit `ceb92f9`；捎帶修 export_figs ERR_UNSAFE_PORT 隨機炸彈＋ch03 圖 Times 殘渣債） |
| **P1 源接管** | ch08＋appA/C/D 首轉（最後一批走 convert.py：方言盤點→mapping→四閘）；其餘 7 單元 tex 升格 `src/`；12 單元 figs harness 全建；`html/` 凍結、`make_dist.py` 退役、新 `build.py`＝日常編譯入口 | 12 單元 src 編譯全綠；fragment 凍結；convert.py／check_prose／make_dist.py 退役留檔 | ✅ 2026-08-09（方言差集：ch08/appA/appC/appD 皆 **0**，免補 mapping；ch05 圖 0 著陸債由 harness 重匯修；首轉 4 單元自動閘全綠、**人眼閘待使用者過目**；overfull 待裁決 6 條＝appA×3〔2.3pt 同型〕/appD×1〔14pt〕/ch04×1〔12.1pt〕/ch06×1〔4.2pt〕；`_audit`/`_dev-archive` 當日決定留在 html/ 原地——**2026-08-09 稍晚使用者要求佈局重構後推翻**：升層至 `handout/_audit`／`handout/_dev-archive`，html 凍結件與轉換工具移入 `legacy/html_handout/`＋`legacy/html2latex/`，`shot.mjs`→`figkit/`、`quote_lint.py`→`tools/`；引用以批量腳本＋doc_lint 迭代修至 clean） |
| **P2 編號語意化**（U3） | 轉換腳本＋模板 counter 層；逐單元轉＋驗證 | 12 單元輸出編號與 as-built ledger 逐一相同 | ✅ 2026-08-09（commit `3ebbcc8`；本表當時未回填，2026-09-14 依 git 補勾） |
| **P3 閘鏈＋契約＋CI＋文檔** | CONTRACT-latex-writing.md 立檔；6 個 handout subagent rubric 改輸入；quote_lint 改掃 .tex；CI 改（lint＋src 存在性；編譯閘維持本地）；README／PIPELINE／CONTENT_SPEC／WORKFLOW／CLAUDE.md 全面改寫 | doc_lint 綠；新 rubric 對任一章實跑一輪 | ✅ 2026-08-09（commit `827a508`；本表當時未回填，2026-09-14 依 git 補勾） |
| **P4 影片線**（U5） | video/README golden path＋CONTENT_METHODOLOGY `source:` 錨格式改 latex/src；各文檔權威輸入指向更新 | video 文檔 doc_lint 綠、引用格式範例更新 | ✅ 2026-08-09（commit `f6882de`；本表當時未回填，2026-09-14 依 git 補勾） |
| **P5 Ch8 gate-2**（U4） | 三閘 gate-2（數學／散文 S·A·V／圖視覺）在 LaTeX 源上跑到 0 blocking → Ch8 定版 | Ch8 定版；新閘鏈首戰紀錄回填本表 | ✅ 2026-08-09（新閘鏈首戰通過：`.tex` inline＋harness PNG 餵 Codex 全程順跑；數學 1B+1A／散文 0／圖 13 clean，9 處措辭修補〔含 ch06 EF1〕，回歸全綠，Ch8 定版。紀錄＝`html/_dev-archive/ch08/ch08_gate2-audit.md`） |

> P2 與 P3 可部分並行；P5 需 P1（ch08 有 src）＋P3（rubric 改完）。每 Phase 完成即回填
> 本表＋PIPELINE dashboard，commit 授權照 CLAUDE.md。

## 5. 風險與護欄

- **首轉仍走確定性轉換**（D3 精神）：ch08／appA/C/D 是 convert.py＋數學逐位元組
  pass-through 的最後一批任務；四閘（含 check_prose）照舊跑完才升格 src。之後 convert
  退役歸檔（不刪——未來若有 HTML 需求可逆向參照）。
- **fragment 凍結＝歸檔不刪**：git 歷史＋`legacy/` 索引；105 圖的 FIGS JS 抽出前
  standalone 不得刪。
- **U3 驗證是硬閘**：語意化若使任何編號偏離現行 as-built ledger（Def/Thm/Ex/Fig/
  Strategy/Caution 全型別），停下比對——偏離要嘛是腳本 bug、要嘛是 ledger 本來就有錯，
  都必須人裁後才續。
- **Ch8 帶債期間勿誤讀**：PIPELINE dashboard 的 Ch8「⚠️ 尚未定版」狀態持續有效，直到
  P5 收案。
- **中途狀態紀律**：每個 Phase 是可獨立 commit 的完整單位；不留「半接管」狀態過夜
  （例如 tex 已升格但 harness 未建就動 fragment）。
