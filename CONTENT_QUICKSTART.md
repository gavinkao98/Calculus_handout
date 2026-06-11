# 作者速查手冊

本檔案是 [`CONTENT_SPEC.md`](CONTENT_SPEC.md) 的精簡日常參考伴侶。寫稿時查閱本檔即可；只有在本檔無法解答你的問題、或你打算偏離某條規則時，才需要翻閱完整 spec。

如果你是新加入的作者，另請瀏覽一次 [`CONTENT_ROADMAP.md`](CONTENT_ROADMAP.md)，了解你負責的章節在整體弧線中的位置。

---

## 語域一句話

Stewart / Rogawski 語調：讓一位自學的高中生能讀懂，完整句子、連接詞明確、直覺先於形式化、溫暖但不話嘮。不是 Spivak，不是課堂速記。

- 預設代名詞：**we**。**you** 僅用於溫和提醒或前方引用（*"you will see this again in §4.2"*）。
- 每個 formal statement（`definition`、`theorem`、`proposition`、`corollary`）**SHOULD** 在其前面有 1–2 段直覺散文，解釋為何值得引入這個概念以及它應該意味著什麼。
- `definition` 主體 **MAY** 在結尾額外附加一句口語化的解說，格式為 *"Informally, ..."*。這是 definition 專屬的選項，不是對所有 formal environment 的通用要求。該解說 **MUST NOT** 引入範例、圖表或新記號。

---

## Environment 速查表

選擇語義角色匹配的 environment。不要巢狀 formal environment。

| Env | 用途 |
|---|---|
| `definition` | 引入本章將使用的新術語。在首次出現時加上 `\index{...}`。 |
| `theorem` | 該節的主要結果。`\begin{theorem}[Name]` + 對應的 `\index{Name}`。 |
| `proposition` | 有用、可重用，但不是該節的主要結果。 |
| `corollary` | 教學上值得單獨點出的直接推論。 |
| `example` + `solution` | 總是成對出現，總是包裹在 `workedexample` 中。不能有單獨的 `example`。 |
| `workedexample` | 語義包裝器，恰好包裹一組 `example`+`solution`。不是分頁技巧。 |
| `proof` | 真正的證明。不用於計算推導。可選（見 spec §5）。 |
| `remark` | 旁註、記號說明、簡短歷史筆記、前方引用。**不是**主線知識。 |
| `caution` | 記號陷阱或容易忽略的限制條件，1–3 句。左側紅色裝飾條。 |
| `strategy` | 包含編號步驟的解題方法框（"given a problem of type X, do..."）。 |
| `exercise` | 位於 `\subsection*{Exercises}` 中。見 [`CONTENT_EXERCISES.md`](CONTENT_EXERCISES.md)。 |

每節教學目標（不是配額）：**2–3 個 remark**、在 worked example 共用同一方法時 **≥1 個 strategy**。自然沒有 remark 的節就保持零；為了湊數而硬加不可取。

**Remark 實用性測試。** 在保留一個 `remark` 之前，問自己：*如果移除這段，讀者會失去什麼？* 如果老實的答案是「什麼都不會失去，它只是在充數」，就刪掉。主線事實、definition 的換句話說、示意性的例子、以及瑣碎的套套邏輯都**不是** remark——把它們提升為散文、放進 `definition` 的 *"Informally, ..."* 句子中、包在 `workedexample` 裡、或用一句散文連接起來。詳見 SPEC §5 的好用 vs. 壞用範例。

---

## 章節開頭（MUST）

```latex
\chapter{Title In Title Case}

Overview paragraph (1-2 paragraphs). Establish the chapter's
motivation and how it connects to the previous chapter.

\paragraph{By the end of this chapter, you will be able to:}
\begin{itemize}
  \item skill 1 (verb-first: "compute", "verify", "recognize");
  \item skill 2;
  \item skill 3-5.
\end{itemize}

\section{First Section Title}
...
```

章節結尾 **MUST** 有 `\section*{Summary}`，包含 definitions / theorems / formulas 三個區塊。見 spec §4。

---

## 節的開頭

1–2 段動機說明。純計算的節可以用一句承接句開頭。不要用 definition 或 display math 開頭。

---

## 公式呈現：5 種模式

| 模式 | 何時使用 |
|---|---|
| inline `\(...\)` | 屬於句子一部分的短公式。 |
| display `\[...\]` | 視覺核心的公式或多步計算。 |
| `aligneddisplay` | 短小的上下對齊式或推導步驟。 |
| `conditiondisplay` | 公式帶有需要獨立間距的 trailing domain / range / branch condition。 |
| `\pairdisplay{A}{B}` | 恰好兩個短公式左右對比。過寬時自動堆疊。 |

經驗法則：
- 每個局部數學單元使用一種模式。不要在同一步驟中混用 centered、aligned 和 prose-condition。
- 在以 display math 結尾的 `solution` 的最後一行加上 `\qedhere`。
- 當 `solution` 主體以 block（list 或 display math）開頭時，在 `solution` body 開頭加上 `\solutionbreak`。
- **不用** `\iff`-helper macro。要表達 formal "A iff B"，使用 display math 搭配 `\Longleftrightarrow`。

---

## 圖表規則

- 色盤僅三種角色：blue = primary、red = caution/counterexample、gray = auxiliary。見 `preamble/colors.tex`。
- **不要僅靠顏色編碼意義。** 至少用以下一種方式做冗餘編碼：line style、label、marker。線型慣例：solid = 主要曲線；`dashed` = 漸近線與參考線（包括 `$y = x$`）；`dotted` = 輔助／鷹架。圖表 **must** 在灰階列印與影印後仍然可讀。詳見 SPEC §10 完整的冗餘編碼規則。
- 預設 placement `[H]`。若使用 `[htbp]`，須在註解中聲明例外。
- caption：sentence case，以句號結尾，描述數學目的。
- **worked-example 的圖**不可洩露例題要求讀者計算的量。
- 圖表密度目標：每個重要 definition / theorem 一張圖，計算型的節大約每 2–3 個 example 一張。

---

## Index 規則

`\index{...}` 放在以下項目的**首次出現**處：
- 每個被定義的術語；
- 每個具名定理；
- 每個記號（如 `\arcsin`、`\lim_{x \to a}`）；
- 每個讀者會想翻回去查的關鍵 example；
- 每個在本章引入的應用場景（physics、economics）；
- 每個記號陷阱（同時也會用 `caution` 標記）。

**查找測試**（當與上述列表衝突時，以此為準）：*讀者日後是否會想在不記得哪個章節引入的情況下找到這個項目？* 如果是，就加 index。純粹的局部符號、一次性的設定、以及僅用於增添趣味而只出現一次的應用場景都**不**需要 entry，即使它們名義上符合上述某個類別。

---

## Cross-reference 與 label

- 一律使用 `\cref{...}` / `\Cref{...}`。永遠不要手動加前綴如 `Theorem~\ref{...}`。
- 方程式引用使用 `\eqref{...}`。
- label 格式：`type:short-desc`，只用連字號。例：`def:one-to-one`、`thm:ivt`、`eq:limit-law-sum`、`fig:inverse-reflection`。
- 方程式編號僅用於後續會被引用或屬於 formal statement 的方程式。

---

## 散文排版

- 強調：僅用 `\emph{...}`，且僅用於新術語的首次出現或極少數承載關鍵意義的片語。**不用** `\textbf{...}` 或 `\textit{...}`（style lint 會強制執行）。
- 引號：TeX 風格 `` ``...'' ``。**不用** ASCII `"..."`（style lint 會強制執行）。
- 破折號：`--` 用於數值範圍（*pp. 12--18*），`---` 用於插入語。原始碼中不使用 unicode em-dash。
- 省略號：一律用 `\dots`（context-aware）。不要硬寫 `\ldots` 或三個句點。LaTeX 會在 display operator 內自動選擇 `\cdots`。

---

## 章節檔案中 **MUST NOT** 包含的內容

- `\newcommand`、`\renewcommand`、`\def`、`\newenvironment`、`\providecommand`（新 helper 放在 `preamble/` 中）。
- `\newpage`、`\pagebreak`、`\clearpage`（分頁由全域處理）。
- 手動 cross-reference 前綴（*Figure~\ref{...}*）。
- ASCII straight quotes。
- 散文中的 `\textbf` / `\textit`。
- `workedexample` body 內的 `\footnote`、`\marginpar` 或手動 `\hypertarget`。

---

## 提交前檢查

在本地執行：

```powershell
python tools/book_style_lint.py
python tools/book_preamble_smoketest.py
python tools/book_docs_lint.py
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error main.tex
```

四項 **MUST** 全部通過。它們也會在每次 push 和 PR 時透過 [`.github/workflows/latex-checks.yml`](.github/workflows/latex-checks.yml) 自動執行。`book_docs_lint` 會抓出過時的 `tools/<name>.py` 指令範例和壞掉的 markdown 連結——執行成本低，能省下重新命名後的 review 往返。

完整的一致性檢查清單（positioning、register、structure、environments、typography 等），見 [`CONTENT_SPEC.md`](CONTENT_SPEC.md) §15 結尾的 checklist。

---

## 何時離開速查手冊

以下情況請查閱完整 spec：
- **§3** — 完整的語域指引、風格 do/don't、語聲參考範文。
- **§5** — 完整的 environment 策略、每個 environment 的典型用途與原理。
- **§6** — 手動編號的邊界情況、不同精度層級的 paired definition。
- **§7** — 完整的 display 決策樹、cohesion 規則、delimiter sizing。
- **§9** — 記號表。
- **§13** — 例外協議（如何記錄規則偏離）。

如果你在嘗試遵守某條規則後仍覺得它不對，不要默默偏離。請提交一份 exception comment（§13）並提出規則修改建議。
