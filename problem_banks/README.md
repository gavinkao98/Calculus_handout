# problem_banks —— 開放授權題庫（本地 clone 區）

選題流程（manuscript first → bank fill → AI fallback）的搜題資料來源，
服務對象為**課文內的 worked examples**（講義本體不收習題——習題另出獨立習題本）。
工作流程契約見 [`CONTENT_SOURCING.md`](../CONTENT_SOURCING.md)。

**除本 README 外，整個資料夾 gitignored**——題庫是第三方 repo 的 shallow clone，
不進本專案版控。換機器後照下方指令重新抓取即可。

## 已接入的題庫

| 題庫 | 授權 | 本地路徑 | 題目所在 | 格式說明 |
|---|---|---|---|---|
| CLP-1 Differential Calculus（UBC） | CC BY-NC-SA 4.0 | `CLP1/` | `latex/problembook/problems/prob_sN.M.tex` | 每節一檔、共 418 題；每題 `question`（＋選用 `hint`）＋`answer`＋`solution` 同檔共存；節內以 `\Conceptual` / `\Procedural` / `\Application` 分組。**首選來源：唯一附完整詳解的題本。** |
| Mooculus / Ximera（OSU） | CC BY-NC-SA | `mooculus/` | 各主題資料夾的 `digIn*.tex`；`calculus{1,2,3}TextbookBySection/` 是按課程編排的索引 | Ximera LaTeX，題目為內嵌的 `\begin{question}`，多附答案欄位 |
| APEX Calculus v5 | CC BY-NC 4.0 | `APEXCalculusV5/` | `exercises/NN_MM_ex_KK.tex`（單題）、`NN_MM_exset_*.tex`（題組） | 單題兩括號格式 `{題目}{答案}`，約 3500 檔；只有最終答案、無詳解；`WebWork/` 另有 PG 題 |

## 重新抓取（換機／重建）

```powershell
git clone --depth 1 https://github.com/arechnitzer/CLP1 problem_banks/CLP1
git clone --depth 1 https://github.com/mooculus/calculus problem_banks/mooculus
git clone --depth 1 https://github.com/APEXCalculus/APEXCalculusV5 problem_banks/APEXCalculusV5
```

## 候選來源（尚未接入，需要時再加）

| 來源 | 授權 | 取得方式 | 何時接入 |
|---|---|---|---|
| CLP-2 Integral Calculus | CC BY-NC-SA 4.0 | `git clone --depth 1 https://github.com/arechnitzer/CLP2` | 進入積分章節時 |
| OpenStax Calculus Vol 1–2 | CC BY-NC-SA 4.0 | <https://openstax.org/details/books/calculus-volume-1>（源檔為 CNXML，抽取摩擦高，建議直接對照網頁版引用節號＋題號） | 需要大量分級 drill 時 |
| MIT OCW 18.01SC | CC BY-NC-SA 4.0 | <https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/>（problem sets＋考卷，全附詳解，PDF） | 需要綜合題／考試級題型時 |
| UBC Math Exam Resources | CC BY-NC-SA 3.0 | <https://wiki.ubc.ca/Science:Math_Exam_Resources>（MediaWiki，1000+ 題全解考古題） | 章末 mixed review |
| WeBWorK OPL | CC BY-NC-SA 3.0（預設；逐集合確認） | `git clone --depth 1 https://github.com/openwebwork/webwork-open-problem-library`（體積大；PG/Perl 模板需實例化） | 上列來源補完後仍有缺口、需要大量同型變式時 |
| Whitman / Community Calculus | CC BY-NC-SA | <https://www.whitman.edu/mathematics/calculus_late/>（TeX 源可下載） | 備援 |

## 授權紅線

- 以上全部屬 BY / BY-NC / BY-NC-SA 家族 → 可合法 remix 進**免費發布、整體掛 CC BY-NC-SA 4.0** 的講義（逐題 `[source: ...]` 標記＋credits 頁）。
- **不收**：CC BY-SA 來源（與 NC-SA remix 不相容，如 Active Calculus）、「免費瀏覽但保留版權」的來源（如 Paul's Online Math Notes）、College Board AP 歷屆題。
