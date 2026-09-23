# latex —— LaTeX 講義線（唯一內容源＋出版排版）

> **2026-08-09 LaTeX 統一（U1）**：本線＝**唯一內容源＋唯一工作線**。內容住
> `src/<ch>/<name>.tex`（手改／LLM 改；升格自原 dist 自足 tex），HTML 撰稿線已凍結
> （[`../../legacy/html_handout/README.md`](../../legacy/html_handout/README.md)）。權威計畫與拍板＝
> [`KICKOFF-latex-unification.md`](KICKOFF-latex-unification.md)；模板沿革（D1–D10）＝
> [`KICKOFF-latex-pilot.md`](KICKOFF-latex-pilot.md)。

## 日常工作流

```powershell
# 改課文：編輯 src/<ch>/<name>.tex（語意指令層＝template/calcbook.sty；勿手排樣式）
cd handout/latex
python build.py ch08        # 編譯＋log 閘＋字形閘＋成品 PDF 進 dist/ch08/
python build.py all         # 全部 12 單元
```

改圖：見 [`../figkit/README.md`](../figkit/README.md)（JS 圖 kit harness → `export_figs.mjs`
匯向量 PDF 到 `chapters/<ch>/figs/`；匯出品 gitignored、換機重匯）。**pull 進別台改過的
harness（`figkit/figs-<ch>.html`）後也要重匯**——`build.py` 不比對圖匯出品的新鮮度，本機的
舊圖會照樣編進有版控的 `dist/` PDF。

## 12 單元狀態（P1 源接管完成，2026-08-09）

| 單元 | 源 | 成品 | 備註 |
|---|---|---|---|
| ch01–ch08 | `src/ch{NN}/chapter{N}.tex` | `dist/ch{NN}/chapter{N}.pdf` | ch08 為 P1 首轉（方言差集 0、四自動閘綠、**人眼閘待過目**） |
| appA／appC／appD | `src/app{X}/appendix{X}.tex` | `dist/app{X}/appendix{X}.pdf` | P1 首轉（同上，人眼閘待過目；appA 3 條＋appD 1 條 overfull 待裁決） |
| appB | `src/appB/appendixB.tex` | `dist/appB/appendixB.pdf` | 原 pilot 章 |

內容閘家族狀態（Mode A／數學／圖／散文／難度）以 [`../PIPELINE.md`](../PIPELINE.md)
dashboard 為準；Ch8 三閘 gate-2 債在 P5 於本線源上償還。

## 目錄結構

```
latex/
  README.md               # 本檔：線導覽
  KICKOFF-latex-unification.md  # U1–U7 拍板＋P0–P5 遷移計畫（權威）
  KICKOFF-latex-pilot.md  # 模板時代沿革（D1–D10；D2/D7 已被 supersede）
  build.py                # ★ 日常編譯入口：src → 閘 → dist
  src/<ch>/<name>.tex     # ★ 唯一內容源（手改）
  template/               # calcbook.sty（語意＋樣式層）、fonts/、M-B1-DECISIONS.md
  dist/<ch>/<name>.pdf    # 成品 PDF（build.py 產）
  chapters/<ch>/          # 章工作資產：figs/（匯出圖，gitignored）＋DIALECT-*.md（凍結存檔）
  check_glyphs.py         # 字形閘（現役；build.py 內建呼叫）
  export_figs.mjs         # 圖匯出（現役；輸入＝../figkit/figs-<ch>.html）
  print_html.mjs          # HTML 印 A4（對照報告用，偶用）
  convert.py／test_convert.py／dialect_inventory.py／check_prose.py／make_dist.py
                          # 已退役（fragment→LaTeX 首轉產線；P1 完畢後留檔參照）
  build/                  # lualatex 工作目錄（gitignored）
  _dev-archive/           # v1 book-class shell 歸檔
```

## 驗收閘（源時代）

1. **編譯閘**：`latexmk -lualatex` 0 error／0 missing character／0 undefined reference／
   0 multiply-defined label（build.py 內建；命中即 FAIL 並列出 key）。
2. **版面閘**：overfull hbox 逐條列出待裁決（build.py 印出）。
3. **字形閘**：`check_glyphs.py`——嵌入字形輪廓＝其宣稱的字（build.py 內建）。
4. **人眼閘**：改版面級的變更後抽頁過目（首轉單元的首次人眼閘由使用者 GO）。

（原「完整性閘 check_prose」驗「轉換不丟內容」，隨轉換產線退役；內容正確性由
內容閘鏈把關——見 [`../PIPELINE.md`](../PIPELINE.md)。）
