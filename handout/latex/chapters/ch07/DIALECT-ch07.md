# ch07 方言凍結表（LaTeX rollout）

> 比照 [`../ch06/DIALECT-ch06.md`](../ch06/DIALECT-ch06.md)：**這是 `convert.py` 的權威 mapping 表**，
> 轉換器只認這裡列的節點，其餘一律硬錯（[`../../KICKOFF-latex-pilot.md`](../../KICKOFF-latex-pilot.md) §4.2 fail-loud）。
> 盤點對象＝`../../../html/fragments/ch07/sec-7-{1..7}.html`。
> 盤點日：2026-07-26。重跑：`python handout/latex/dialect_inventory.py ch07`。

## 1. 摘要

- **33 種 tag＋class 組合，對既有 mapping 的差集為 0**——ch07 是 ch05 的**嚴格子集**
  （ch05 另有 `p.informal` 與 `strong`，ch07 沒用到）。`convert.py` 一個字沒改。
- **數學：inline `\(…\)` ×883、display `\[…\]` ×67**（合計 950 段，與 `make_dist.py`
  回報的 pass-through 段數一致）。
- **圖：23 個 `<figure data-fig>` ／ 27 個 SVG panel**（`strip-to-disk`、`washer-vs-shell`、
  `polygon-refinement`、`chord-to-band` 四張是雙 panel，其餘單格）——**全書圖最多的一章**。
- 活散文的非 ASCII 9 種（`’ § — “ ” – é ³ ²`），NCM／Inter 全數有字；
  字形閘 570 個嵌入字形 0 個輪廓不符。
- **數學區段內零 U+2019**——ch05 那個「排版右單引號被當成 prime」的內容缺陷，本章沒有。

## 2. 差集：無

ch07 沒有帶進任何新的標記型別。這是 rollout 至今第二個差集為 0 的單元（前一個是 ch06）。

## 3. 本輪修掉的一個**共用工具** bug：字形閘在合法的 TrueType 構造上崩掉

**症狀。** `make_dist.py ch07` 的前三閘全過，第四閘（字形）直接 traceback：

```
File "check_glyphs.py", line 164, in _glyf_outline
    return tuple((op, tuple(round(c, 1) for pt in args for c in pt)) for op, args in pen.value)
TypeError: 'NoneType' object is not iterable
```

**根因。** `_glyf_outline` 假設 fontTools 的 pen 吐出的每個點都是座標對。但 TrueType 允許
**一整條輪廓全是 off-curve 點**（相鄰兩點的中點即為隱含的 on-curve 點），pen protocol 用
結尾的 `None` 表示這種閉合輪廓——`qCurveTo(p1…pn, None)`。

**為什麼是 ch07 才踩到。** 觸發者是 web 版 New Computer Modern 的 **`question`（`?`，GID 34）**：
它的那個圓點正是全 off-curve 畫的。原字型有 **68 個**同型字形（`! . : ; ? ¡ · ¿` 等圓點類），
但**子集只帶進實際用到的字元**——ch07 是全書第一個把 `?` 排進圖面板文字的單元
（§7.3 的 “Washer or shell?” 一線），此前各章的面板文字剛好都避開了這幾個字元。
實測：ch07 的五個 WebCM 子集中，只有一個含 `question`，其餘四個 0 個。

**處置。** `_glyf_outline` 改成保留 `None` 為**可區分**的值（不是過濾掉）：

```python
return tuple(
    (op, tuple(None if pt is None else tuple(round(c, 1) for c in pt) for pt in args))
    for op, args in pen.value)
```

過濾掉 `None` 會讓「最後一點是隱含 on-curve」與「最後一點是實際 on-curve」的兩條輪廓
比成相等，等於在本閘上開一個洞——所以是保留而非丟棄。

**回歸測試。** 新增 [`../../test_check_glyphs.py`](../../test_check_glyphs.py)（4 tests，純 stdlib
unittest）：不得崩、`None` 須可區分、正常路徑仍相等、取整仍生效。已實測舊實作在同一輸入下
確實 `TypeError`，測試守得住這個回歸。

**對既有單元中性。** 修的是比對器的內部表示，兩側同時套用，只可能把 crash 變成正常比對。
七個既有 dist PDF 重跑字形閘全數 PASS，且數字與各章當初記錄的一致
（appB 362／ch01 489／ch02 512＋1 白名單／ch03 438／ch04 549／**ch05 514**（與其 commit 所記相同）／ch06 507）。

## 4. 四閘結果（2026-07-26）

```
[dist] chapter7.tex（950 段數學 pass-through）
[dist] chapter7.pdf：39 頁、error 0、missing char 0        ← 閘 1
[gate] 完整性閘 PASS：48 處 pdftotext 抽取假象，0 處真落差   ← 閘 3
[gate] 表格閘：本章無 table.tbl，略過
[gate] 圖內文字閘 PASS：8 條 panel note 全數抵達 PDF
[gate] 字形閘 PASS：570 個嵌入字形的輪廓全數符合其 CID       ← 閘 4
```

確定性：重跑 `make_dist.py ch07` 的 `.tex` byte-identical。

**48 處抽取假象**（全書至今最多）幾乎全是同一型：`\(i\)th`／`\(x\)-axis` 這類
「行內數學緊接純字母」被 `pdftotext` 抽成 `𝑖th`／`𝑥axis`，逐條確認內容都在。
本章大量使用 `\(x\)-axis`／`\(y\)-axis`（旋轉軸紀律是全章主題）是件數偏高的原因。

## 5. 圖

23 張圖以

```
node export_figs.mjs ../html/standalone/chapter7-print-standalone.html chapters/ch07/figs
```

匯出成 27 個向量 PDF panel（`figs/` 是 gitignored 中間物，隨時可由 standalone 重生）。
面板寬度 42.4–79.9 mm，皆單欄內。四張雙 panel 圖的 8 條 panel note
（Strip／Disk、Washers／Shells、\(n=4\)／\(n=8\)、Chord／Frustum band）
經圖內文字閘確認全數抵達 PDF。
