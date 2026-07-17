# latex —— LaTeX 出版排版線

> **這條線做什麼**：定稿時把 HTML 線的 fragment（唯一內容源）**確定性轉換**成出版級 A4 PDF
> （2026-07-17 拍板：整體先做 HTML 講義、定稿再轉，見 [`../PIPELINE.md`](../PIPELINE.md) §出版排版線）。
> 沿革、D1–D10 拍板、rollout 計畫的權威文檔＝[`KICKOFF-latex-pilot.md`](KICKOFF-latex-pilot.md)。

## 哪個章節的講義在哪裡：看 `dist/`（成品夾）

**成品只看 [`dist/`](dist/)——每單元一夾、夾內乾乾淨淨兩個檔**：`<name>.pdf`（成品）＋
`<name>.tex`（自足成品源，對它直接編譯就重現 PDF）。中間物一律不在這裡（方言表、對照
報告、匯出圖住 `chapters/<ch>/`；編譯殘渣住 gitignored 的 `build/`）。

| 單元 | 狀態 | 成品夾 | 工作資產（中間物） |
|---|---|---|---|
| appB | ✅ **pilot GO**（14 頁，四閘全綠） | [`dist/appB/`](dist/appB/)：`appendixB.pdf`＋`appendixB.tex` | [`chapters/appB/`](chapters/appB/)：DIALECT、driver、對照報告 |
| ch03 | 🔶 v1 參照（轉換過、模板已換代，rollout 首發候選） | —（rollout 定版後產） | [`chapters/ch03/`](chapters/ch03/)：DIALECT、figs（7 張向量 PDF）、對照報告 |
| ch01–ch02、ch04–ch06、appA/C/D | ⬜ 未轉換（rollout 依定稿排程；建議順序見 KICKOFF §9） | 屆時 `dist/<ch>/` | 屆時 `chapters/<ch>/` |

**重編成品**（改了 fragment 之後）：

```powershell
cd handout/latex
python make_dist.py appB      # 轉換＋內嵌＋編譯＋log 驗收，成品夾維持兩檔
```

或不經工具、直接編譯成品 `.tex`（在 `dist/<ch>/` 下；aux 導去 build/、資料夾不留殘渣）：

```powershell
latexmk -lualatex -auxdir=../../build/aux-appB appendixB.tex
```

## 目錄結構

```
latex/
  README.md               # 本檔：線導覽＋章節狀態表
  KICKOFF-latex-pilot.md  # 沿革＋D1–D10 拍板＋rollout 計畫（權威）
  make_dist.py            # 產成品夾：轉換＋內嵌＋編譯＋三閘驗收（1/3/4）→ dist/<ch>/ 兩檔
  convert.py              # fragment → 語意層 LaTeX（數學逐位元組 pass-through、表外標記硬錯）
  test_convert.py         # golden tests＋數學逐位元組不變式
  dialect_inventory.py    # 方言盤點器（rollout 逐章：python dialect_inventory.py ch04）
  check_prose.py          # 完整性閘：散文子序列＋圖內文字（pdftotext）
  check_glyphs.py         # 字形閘：嵌入字形的輪廓是不是它宣稱的字（pdftotext 那層看不到）
  export_figs.mjs         # 圖匯出：standalone → 每 panel 一張向量 PDF
  print_html.mjs          # HTML 印 A4 PDF（對照報告的 HTML 側）
  dist/<ch>/              # ★ 成品夾：<name>.pdf＋<name>.tex（自足成品源），永遠只有兩檔
  template/               # 共用模板：calcbook.sty（語意＋樣式層）、sampler.tex（拍板樣張）、
                          # fonts/inter/（vendored）、M-B1-DECISIONS.md（模板拍板紀錄）
  chapters/<ch>/          # 章節工作資產：DIALECT-<ch>.md（方言凍結表）＋ driver .tex
                          # ＋ REVIEW 對照報告（含 img/）＋ figs/（匯出圖＋figures.json）
  build/                  # lualatex 工作目錄（gitignored；含 aux-<ch>/ 編譯殘渣）
  _dev-archive/           # v1 book-class shell 歸檔
```

## 開發／除錯用的分步建置（成品請一律走 `make_dist.py`）

```powershell
# 1. 轉換（在 latex/ 下；fragment 唯讀，輸出到 build/）
python convert.py appB --out build/appendixB-body.tex

# 2. 編譯 chapters/ 的 driver（CWD 在 template/——它 \input build/ 的 body，適合迭代模板）
cd template && latexmk -lualatex -output-directory=../build/appB ../chapters/appB/appendixB.tex

# 3. 完整性閘（散文子序列＋圖內文字；對 dist 或 build 的 PDF 皆可跑）
python check_prose.py appB dist/appB/appendixB.pdf
```

四閘驗收（編譯／版面／完整性／人眼）定義見 KICKOFF §4.5；golden tests＝`python test_convert.py`。

## rollout 每章的固定流程

1. `python dialect_inventory.py <ch>` 盤點 → 凍結 `chapters/<ch>/DIALECT-<ch>.md`（差集相對既有 mapping）。
2. 補 emitter mapping＋golden tests（`convert.py`／`test_convert.py`）。
3. 有圖章：`export_figs.mjs` 匯出到 `chapters/<ch>/figs/`（寬度 mm 由 figures.json 驅動；
   dist 的 \graphicspath 接線在 `make_dist.py`，首個有圖章時補——見檔頭註記）。
4. 建 driver `chapters/<ch>/<name>.tex` → 編譯 → 四閘 → 對照報告 → 使用者 GO。
5. GO 後 `make_dist.py <ch>`（先在 NAMES 表補檔名）→ `dist/<ch>/` 兩檔即成品。
