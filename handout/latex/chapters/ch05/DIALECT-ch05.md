# ch05 方言凍結表（LaTeX rollout）

> 比照 [`../ch04/DIALECT-ch04.md`](../ch04/DIALECT-ch04.md)：**這是 `convert.py` 的權威 mapping 表**，
> 轉換器只認這裡列的節點，其餘一律硬錯（[`../../KICKOFF-latex-pilot.md`](../../KICKOFF-latex-pilot.md) §4.2 fail-loud）。
> 盤點對象＝`../../../html/fragments/ch05/sec-5-{1..9}.html`。
> 盤點日：2026-07-26。重跑：`python handout/latex/dialect_inventory.py ch05`。

## 1. 摘要

- **35 種 tag＋class 組合，對 ch04 的差集為 0**——ch05 沒有帶進任何新的標記型別。
- **數學：inline `\(…\)` ×921、display `\[…\]` ×82**（合計 1003 段，與 math gate 的計數一致）。
- **圖：11 個 `<figure data-fig>` ／ 12 個 SVG panel**（`concavity-tangents` 為雙 panel，其餘單格）。
- 活散文的非 ASCII 4 種（`’ § — ô`），NCM／Inter 全數有字；字形閘 514 個嵌入字形 0 個輪廓不符。

## 2. ch05 的一項差集（本次 rollout 新凍結）

| # | 標記／現象 | 次數 | 處置 | 為什麼是 ch05 才遇到 |
|---|---|--:|---|---|
| D1 | **`span.env-kicker` 內含數學** | 2 段 | `convert.py` 的 Env emitter 把 kicker 從 `esc(...)` 改走 `restore(esc(...))`（與 inline 文字同一條路徑），並移到 `name` 之前算以保源順序 | ch05 §5.7 的證明標題是**自訂**的 <code>Proof of the \\(\\tfrac{0}{0}\\) case, \\(a\\) finite</code>——全書第一個把數學寫進 env-kicker 的地方。此前 kicker 一律是 `Theorem`／`Proof`／`Example` 這類純文字，`esc()` 夠用；帶數學時占位符不被還原＝那兩段數學被丟掉，由 pass-through 不變式擋下（實測報 `sec-5-7.html: 缺席 [65, 66]`）。**appD §D.3 是同型的第二處**（<code>Proof of Theorem 5.5 (\\(\\tfrac{\\ast}{\\infty}\\) case)</code>），該單元 rollout 時可直接受益。 |

`num` 維持純 `esc`：`env-num` 是編號（`5.5`），帶數學即屬體例錯誤，應由不變式擋下而非放行。

測試（[`../../test_convert.py`](../../test_convert.py)，90 tests）：
`test_env_kicker_math_is_restored`（kicker 數學須還原）＋
`test_env_kicker_math_ordering_before_env_name`（kicker → name → body 的還原順序）。

## 3. 本輪順帶抓到的一個內容缺陷（只有 LaTeX 線看得見）

三段 display 數學用了**排版右單引號 U+2019** 而非 ASCII prime `'`：

| 位置 | 原本 | 改成 |
|---|---|---|
| §5.5 Example 5.17 | `A’(x) &= 2\sqrt{...}` | `A'(x) &= 2\sqrt{...}` |
| §5.6 Example 5.18 | `&f’’(x) > 0 …`（3 處） | `&f''(x) > 0 …` |
| §5.8 Example 5.24 | `f’(x) &= \frac{...}` | `f'(x) &= \frac{...}` |

**為什麼 HTML 線看不出來**：MathJax 把 `A’(x)` 與 `A'(x)` 渲染成**完全相同**的輸出（實測兩者
都產生 U+2032 PRIME，`tex2chtml` 逐字元比對一致），所以螢幕與 print standalone 上都是正確的
撇號，既有的圖閘／散文閘也不會報。

**LaTeX 線才現形**：lualatex 把 U+2019 當成直立引號字元排出來，於是 §5.5 同一頁上，display 的
`A'(x)` 是直立撇號、正文 inline 的 `\(A'\)` 卻是正確的義大利體 `A′`——同一個符號兩種樣子。
編譯不會失敗（0 missing character），字形閘也 PASS（該引號字形本身嵌得好好的），**是排版
正確性問題，不是編譯問題**。修好後字形閘的嵌入字形數 515 → 514（直立引號那個字形不再需要）。

全書掃描確認：**此問題只出現在 ch05 這 8 個字元**，其餘單元的數學區段內零 U+2019。

## 4. 四閘結果（2026-07-26）

```
[dist] chapter5.tex（1003 段數學 pass-through）
[dist] chapter5.pdf：36 頁、error 0、missing char 0        ← 閘 1
[gate] 完整性閘 PASS：11 處 pdftotext 抽取假象，0 處真落差   ← 閘 3
[gate] 圖內文字閘 PASS：2 條 panel note 全數抵達 PDF
[gate] 字形閘 PASS：514 個嵌入字形的輪廓全數符合其 CID       ← 閘 4
```

確定性：重跑 `make_dist.py ch05` 的 `.tex` byte-identical。
回歸：`convert.py` 的 kicker 改動對既有單元**內容中性**——appB 與 ch03 重跑後 `.tex` 與
committed 版零內容差異（ch03 另跑完整四閘：612 段數學、22 頁、三閘全 PASS）。

## 5. 圖

11 張圖以 `node export_figs.mjs ../html/standalone/chapter5-print-standalone.html chapters/ch05/figs`
匯出成 12 個向量 PDF panel（`figs/` 是 gitignored 中間物，隨時可由 standalone 重生）。
面板寬度 64–85 mm，皆單欄內。`concavity-tangents` 是本章唯一的雙 panel 圖，兩條 panel note
的上畫面文字經圖內文字閘確認抵達 PDF。
