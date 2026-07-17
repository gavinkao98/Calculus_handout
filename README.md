# 微積分講義專案

一份單面 A4 的**微積分講義**，供準備銜接大學微積分的高中生自學使用，並搭配輔助教學影片。講義本身自給自足；影片是強化補充。

本檔案是**儲存庫樞紐（repository hub）**。它對儲存庫結構與建置指令具有權威性——生產用講義是 `handout/` 下的 HTML 版（以 fragment 撰稿、`build.py` 組版），下方所載的 LaTeX／preamble／建置描述現為 legacy（已搬至 `legacy/tex_handout/`）。內容撰寫規則與媒體產線規則各自獨立成檔，連結列於下方。

---

## 從這裡開始

依你手上的任務，開啟對應的連結檔案。

- **撰寫或修訂章節。** 先看 [`CONTENT_QUICKSTART.md`](CONTENT_QUICKSTART.md)。當快速指南無法回答你的問題時，再回頭查 [`CONTENT_SPEC.md`](CONTENT_SPEC.md)。開始新的一章前，先看 [`CONTENT_ROADMAP.md`](CONTENT_ROADMAP.md)，並依 [`CONTENT_AUTHORING_WORKFLOW.md`](CONTENT_AUTHORING_WORKFLOW.md) 認清撰稿變體（Ch1–4 手稿變體／Ch5 起無手稿 canon 變體）與 Mode A／B／C 規則。每節內容的方向流程（方向 brief ＋ 六階方向層）見 [`CONTENT_DIRECTION.md`](CONTENT_DIRECTION.md)。
- **製作影片**（目前的主要路徑：第二代 Manim 產線）。先看 [`video/README.md`](video/README.md)，再看 [`video/DESIGN.md`](video/DESIGN.md) 了解分鏡契約與目前的模板決策。較舊的 `MANIM_*` 文件已封存於 [`legacy/`](legacy/)，保留作為第一代參考資料。
- **靜態投影片 MP4**（已凍結的舊路徑）。使用 [`legacy/LEGACY_SLIDE_PIPELINE.md`](legacy/LEGACY_SLIDE_PIPELINE.md)。此路徑不再有新開發——新工作請改用 Manim。
- **為課文補教學範例（從開放題庫選題）。** 見 [`CONTENT_SOURCING.md`](CONTENT_SOURCING.md)。講義本體不收習題——習題將以獨立習題本呈現（[`CONTENT_SPEC.md`](CONTENT_SPEC.md) §14，2026-06-12 定案）。
- **換電腦／環境出問題。** 見 [`ENVIRONMENT.md`](ENVIRONMENT.md)（每台機器要備什麼的權威清單）；跑 `python tools/doctor.py` 一行看出這台缺什麼、`tools/setup.ps1` 一鍵備妥 Python 端。

---

## 撰稿工作流程

內容撰寫的**權威流程檔已抽出為 [`CONTENT_AUTHORING_WORKFLOW.md`](CONTENT_AUTHORING_WORKFLOW.md)**（2026-07-07 自本檔遷出），涵蓋：

- **兩種撰稿變體**：Ch1–4 的**手稿變體**（手稿→教科書草擬，既成）與 Ch5 起的**無手稿 canon 變體**（canon-as-spine，預設）；
- **Mode A／B／C 狀態機**全文（草擬、審訂稽核、充實增補）、expansion 標記與類別、具名內容政策、密度校準、九項擴增稽核；
- 無手稿章節的 **provenance 規則**（`<!-- section-source: -->` header＋教學增添才標 `expansion:`）與反幻覺備援（hypothesis ledger、章末 sympy 重算）。

每節的方向層（方向 brief＋六階流程）見 [`CONTENT_DIRECTION.md`](CONTENT_DIRECTION.md)；完成一章的閘序見 [`handout/PIPELINE.md`](handout/PIPELINE.md)。

---

## Golden path（黃金路徑）

目前的影片工作位於 `video/` 下的第二代產線（權威流程與閘地圖見 [`video/README.md`](video/README.md)、[`video/REVIEW_GATES.md`](video/REVIEW_GATES.md)）：

```text
handout/chapterN-print-standalone.html（定稿講義的一節）
  --> video/content_scripts/<deck>.md（Stage-1 內容稿）＋ <deck>.spoken.yml（口語單一源）
  --> video/storyboards/<deck>.yml（Stage-2 工程稿；schema/lint/sizecheck render 前把關）
  --> python video/make.py --storyboard …（parse → synth → render → compose）
  --> video/output/ch<NN>/s<X.Y>/….mp4（真旁白走 MiMo：tts.py --backend mimo → make.py --reuse-audio）
```

先定稿章節內容，再寫內容稿與旁白（lock 後 derive 口語版、MiMo TTS），最後模板化 storyboard 與 render。第一代 Manim 產線與 gen-0 投影片產線已封存於 `legacy/`（索引與還原說明見 [`legacy/README.md`](legacy/README.md)），並非活躍開發路徑。

---

## 文件地圖

| 層級 | 檔案 | 用途 |
|---|---|---|
| 樞紐 | `README.md` | 儲存庫結構、HTML 講義建置規則（LaTeX preamble 對照現為 legacy） |
| 內容流程 | [`CONTENT_AUTHORING_WORKFLOW.md`](CONTENT_AUTHORING_WORKFLOW.md) | Mode A／B／C 與無手稿 canon 變體的權威撰寫流程 |
| 內容規格 | [`CONTENT_SPEC.md`](CONTENT_SPEC.md) | 權威性的教科書撰寫規則 |
| 內容日用 | [`CONTENT_QUICKSTART.md`](CONTENT_QUICKSTART.md) | 1–2 頁的作者速查表 |
| 內容脈絡 | [`CONTENT_ROADMAP.md`](CONTENT_ROADMAP.md) | 章節順序、先備知識、各章核心技能、Ch5–16 弧線骨架與 seam ledger |
| 內容題源 | [`CONTENT_SOURCING.md`](CONTENT_SOURCING.md) | 課文範例的題源與選題流程（題庫、provenance、授權） |
| 內容方向 | [`CONTENT_DIRECTION.md`](CONTENT_DIRECTION.md) | 每節擴寫的方向層：方向 brief、六階流程、人閘（驗證紀錄在 `authoring/direction_layer/`） |
| 講義閘序 | [`handout/PIPELINE.md`](handout/PIPELINE.md) | 完成一章的完整閘序與各章狀態 dashboard |
| HTML 契約 | [`handout/CONTRACT-html-writing.md`](handout/CONTRACT-html-writing.md) | 權威性 HTML 標記契約 |
| 影片產線 | [`video/README.md`](video/README.md) | 目前第二代 Manim 產線的狀態、指令、交接註記 |
| 影片設計 | [`video/DESIGN.md`](video/DESIGN.md) | 目前的分鏡契約、場景種類、模板決策 |
| 影片內容方法論 | [`video/CONTENT_METHODOLOGY.md`](video/CONTENT_METHODOLOGY.md) | Stage-1 內容稿撰寫方法論（拆解、narration、視覺決策） |
| 影片閘地圖 | [`video/REVIEW_GATES.md`](video/REVIEW_GATES.md) | 七產物層審核閘一覽（索引，home doc 為權威） |
| 影片進度錨 | [`video/REBUILD_STATUS.md`](video/REBUILD_STATUS.md) | 跨對話進度快照（歷史輪次在 `video/_archive/`） |
| manim v1 操作 | [`legacy/MANIM_CHECKLIST.md`](legacy/MANIM_CHECKLIST.md) | 第一代參考檢查表（已封存） |
| manim v1 參考 | [`legacy/MANIM_REFERENCE.md`](legacy/MANIM_REFERENCE.md) | 第一代欄位契約、模板、render 指令（已封存） |
| manim v1 方法論 | [`legacy/MANIM_STORYBOARD.md`](legacy/MANIM_STORYBOARD.md) | 第一代 LaTeX 轉 YAML 翻譯手冊（已封存） |
| 凍結舊版 | [`legacy/LEGACY_SLIDE_PIPELINE.md`](legacy/LEGACY_SLIDE_PIPELINE.md) | 靜態投影片／PDF + TTS + MP4（已封存，不再有新開發） |
| 封存總覽 | [`legacy/README.md`](legacy/README.md) | gen-0／gen-1 凍結產線的封存索引與還原說明 |

---

## 儲存庫結構

- `handout/` — **生產用講義（HTML 版）**。內容以 fragment 撰稿，`build.py` 組版。
  - `handout/fragments/chNN/sec-*.html` — 章節源檔，每節一個 fragment。
  - `handout/build.py` — 組版器：產出 `handout/chapterN-print-standalone.html`（僅列印版；螢幕版已移除）。
  - `handout/TYPESETTING_GUIDE.md` — HTML 排版指南；`handout/CONTRACT-html-writing.md` — 權威性 HTML 標記契約。
  - `handout/tex_export/` — **出版排版線（HTML→LaTeX；pilot GO 2026-07-17）**：`convert.py` 確定性轉換 fragment（數學逐位元組 pass-through、表外標記硬錯）→ `template/calcbook.sty`（memoir＋NewComputerModern＋vendored Inter）→ `latexmk -lualatex` 出 A4 PDF。權威文檔＝[`handout/KICKOFF-latex-pilot.md`](handout/KICKOFF-latex-pilot.md)（沿革＋rollout 計畫）、`tex_export/DIALECT-*.md`（方言凍結表）、`tex_export/template/M-B1-DECISIONS.md`（模板拍板紀錄）。
  - `handout/_audit/PROSE-AUDIT-RUBRIC.md` — 散文稽核 rubric（gate 1 契約）；`handout/_dev-archive/chNN/` — 各章編排檔（`PLAN-chNN.md`、`PROMPT-sNM-kickoff.md`、`brief_sNM.md`、`seed_chNN.md`）。
- `authoring/` — 撰稿方法論與機制 R&D。六階方向層流程已畢業為頂層 [`CONTENT_DIRECTION.md`](CONTENT_DIRECTION.md)；`authoring/direction_layer/` 保留其端到端驗證紀錄（`ch01/`、`test/`），`authoring/seed_converge/` 為機制 R&D（`SYNTHESIS.md`、`PLAN_codex_subscription_loop.md`、`run.py`、`figure_critic.py`、`figure_fix.py`、`rules.md`）。
- `problem_banks/` — 開放授權題庫的本地 clone 區（內容 gitignored，僅 README 進版控）。選題工作流程見 [`CONTENT_SOURCING.md`](CONTENT_SOURCING.md)。
- `legacy/tex_handout/` — 已凍結的 **LaTeX 講義樹**（`main.tex`、`preamble/`、`chapters/*.tex`、`refs/references.bib`，以及 `tools/book_style_lint.py`／`book_preamble_smoketest.py`／`book_docs_lint.py`）。此樹不再是生產路徑，僅供歷史參考；下方的 *Preamble 對照* 節描述的即是這棵 legacy 樹（*輸出格式*、*建置與 CI* 各節則以 HTML 講義為主、另附 legacy 註記）。（根目錄遺留的 `chapters/` 僅含 `.aux` 等建置殘留物。）
- `legacy/` — 已封存的凍結媒體產線（gen-0 投影片、gen-1 Manim 及其橋接實驗）：`legacy/scripts/`（腳本）、`legacy/MANIM_*.md` 與 `legacy/LEGACY_SLIDE_PIPELINE.md`（方法論文件）、`legacy/schemas/`、`legacy/inputs/`、`legacy/artifacts/`（gitignored 的大型算繪輸出仍存於磁碟，git 追蹤的例外為 narration／final／tex）。詳見 [`legacy/README.md`](legacy/README.md)。
- `.github/workflows/` — CI 檢查。

額外的活躍媒體工作區：

- `video/` — 目前第二代 Manim 課程影片產線，包含分鏡、可重用模板、設計註記，以及 gitignored 的預覽輸出。

---

## Preamble 對照（legacy LaTeX 講義）

> 生產用的 HTML 講義沒有 LaTeX preamble——它以 MathJax／KaTeX CDN 與 JS paginator 排版，設定見 [`handout/TYPESETTING_GUIDE.md`](handout/TYPESETTING_GUIDE.md)。已凍結 LaTeX 講義樹的 preamble 拆分說明（`packages`／`colors`／`layout`／`theorem_setup`／`numbering`／`bibliography` 六檔的職責）僅供歷史參考，檔案本身在 `legacy/tex_handout/preamble/`，封存索引見 [`legacy/README.md`](legacy/README.md)。

---

## 輸出格式

生產用講義的輸出是 `handout/chapterN-print-standalone.html`——由 `handout/build.py` 將各 fragment 組裝而成的列印用 standalone HTML，A4 分頁透過 JS paginator（`place()`）達成；數學以 MathJax／KaTeX CDN 渲染。設計為單張單頁列印、作為講義發送，而非裝訂成冊。版面與排版細節見 [`handout/TYPESETTING_GUIDE.md`](handout/TYPESETTING_GUIDE.md)。

**出版排版（2026-07-17 pilot GO）**：出版級輸出走 `handout/tex_export/` 的 LaTeX 線——fragment 仍是唯一內容源（一字不改），`convert.py` 轉為 `template/calcbook.sty` 的語意指令，`latexmk -lualatex` 產 A4 PDF（appB 實測：同內容 HTML 20 頁 → LaTeX 14 頁，四閘全綠）。HTML standalone 自此定位為**撰稿預覽＋圖閘 render 載體**（kickoff 決策 D2／D6）；逐章 rollout 順序見 [`handout/KICKOFF-latex-pilot.md`](handout/KICKOFF-latex-pilot.md) §9。

> **Legacy（LaTeX 講義）：** 已凍結的 LaTeX 版（`legacy/tex_handout/`）以 `\documentclass[a4paper,12pt,oneside]{book}` 產出單面 A4 PDF：`margin=3.3cm` 對稱、`\linespread{1.05}`、`\fancyhead`/`\fancyfoot` 單面 header／footer，並由 `main.tex` 以 `\ifprintbibliography` 與 `\ifincludescratchchapter` 開關控制參考書目與暫存章節。此路徑不再用於生產。

---

## 建置與 CI

本機建置：

```powershell
python handout/build.py
```

產出 `handout/chapterN-print-standalone.html`（列印用 standalone，A4 分頁由 JS paginator 達成）。每次 push 與 PR 由 [`.github/workflows/handout-checks.yml`](.github/workflows/handout-checks.yml) 自動執行此 build，並檢查 committed standalone 與 fragment 同步、散文引號合規（`handout/quote_lint.py`）、指引文檔相對連結無斷鏈（[`tools/doc_lint.py`](tools/doc_lint.py)，2026-07-07 加）。

內容閘採兩道：gate 1 為 Claude `handout-prose-audit` subagent（唯讀、免費，依 [`handout/_audit/PROSE-AUDIT-RUBRIC.md`](handout/_audit/PROSE-AUDIT-RUBRIC.md)）；gate 2 為 Codex 獨立複核（吃配額、先徵同意）。完整閘序見 [`handout/PIPELINE.md`](handout/PIPELINE.md)。HTML 標記與排版細節見 [`handout/CONTRACT-html-writing.md`](handout/CONTRACT-html-writing.md) 與 [`handout/TYPESETTING_GUIDE.md`](handout/TYPESETTING_GUIDE.md)。

> **Legacy（LaTeX 講義 CI）：** 舊的 LaTeX 路徑以 `latexmk -pdf … main.tex` 建置，並以 `tools/book_style_lint.py`、`book_preamble_smoketest.py`、`book_docs_lint.py` 三項檢查加 `latexmk` 建置經 `.github/workflows/latex-checks.yml` 把關。其中三項 `book_*.py` 工具已隨 LaTeX 樹搬至 `legacy/tex_handout/tools/`，原 `latex-checks.yml` 已移除（HTML 講義改由上述 `handout-checks.yml` 把關），皆不再是 HTML 講義的閘（其中 `book_docs_lint.py` 原用於掃描 markdown 中過時的 `tools/<name>.py` 指令引用與失效的相對連結）。第一代的 `manim_storyboard_lint.py` 則隨 Manim v1 產線封存至 `legacy/scripts/`。

權威性：當儲存庫結構或 HTML 講義建置規則變更時，**以本檔案**為權威；當撰寫或排版規則變更時，以 [`CONTENT_SPEC.md`](CONTENT_SPEC.md) 為權威。

---

## 媒體範圍說明

講義本體不收習題（[`CONTENT_SPEC.md`](CONTENT_SPEC.md) §14，2026-06-12 定案），故規劃各節媒體時無習題區塊需要排除；一律從定義、定理、範例與闡述散文來建構投影片 deck、旁白腳本、Manim 分鏡、合成音訊與 render 的影片。

## 備註

- **2026-06-15 結構遷移：** HTML 講義自 `experiments/handout_kit/` 升格為頂層 `handout/`（正式版）；撰稿方法論 `direction_layer`／`seed_converge` 移入 `authoring/`；`legacy_slide_deck` 移入 `legacy/`；`experiments/` 資料夾就此解散。LaTeX 講義樹早於 2026-06-13（commit `b0a89cf`）即移入 `legacy/tex_handout/`，本次同步更新所有指引文檔與路徑引用、並把 CI 由（已移除的）`latex-checks.yml` 改為 `handout-checks.yml`（建置 `handout/build.py`）。
- 本機快取、虛擬環境與內嵌依賴存於隱藏的儲存庫資料夾，例如 `.cache/`、`.venv/`、`.deps/` 與 `.deps_f5/`。
- 目前的影片開發在 `video/`，而非已封存的 `legacy/inputs/manim_storyboards`。逐節進度以 [`video/REBUILD_STATUS.md`](video/REBUILD_STATUS.md) 的現況快照為準（首個完整真旁白成片＝ch03 §3.1，MiMo Dean 路線）。
- 第一代凍結媒體範本（Sec. 1.1／Sec. 1.6 兩份對比分鏡與投影片計畫）與其校準脈絡見 [`legacy/README.md`](legacy/README.md)；新的 gen-2 分鏡放於 `video/storyboards/`。
