# 作者速查手冊

本檔案是 [`CONTENT_SPEC.md`](CONTENT_SPEC.md) 的精簡日常參考伴侶。寫稿時查閱本檔即可；只有在本檔無法解答你的問題、或你打算偏離某條規則時，才需要翻閱完整 spec。

如果你是新加入的作者，另請瀏覽一次 [`CONTENT_ROADMAP.md`](CONTENT_ROADMAP.md)，了解你負責的章節在整體弧線中的位置。

**內容寫在哪裡。** 正式講義是 HTML：內容以每節一個片段撰寫於 `handout/fragments/chNN/sec-*.html`，由 `python handout/build.py` 組成 `handout/chapterN-print-standalone.html`（print standalone，A4 分頁由 JS paginator 處理）。HTML 標記契約見 [`handout/_dev-archive/general/CONTRACT-html-writing.md`](handout/_dev-archive/general/CONTRACT-html-writing.md)，排版規範見 [`handout/TYPESETTING_GUIDE.md`](handout/TYPESETTING_GUIDE.md)。（舊的 LaTeX 講義已移入 `legacy/tex_handout/`。）

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
| `definition` | 引入本章將使用的新術語。 |
| `theorem` | 該節的主要結果；具名定理在標題帶上名稱。 |
| `proposition` | 有用、可重用，但不是該節的主要結果。 |
| `corollary` | 教學上值得單獨點出的直接推論。 |
| `example` + `solution` | 總是成對出現，總是包裹在 `workedexample` 中。不能有單獨的 `example`。 |
| `workedexample` | 語義包裝器，恰好包裹一組 `example`+`solution`。不是分頁技巧。 |
| `proof` | 真正的證明。不用於計算推導。可選（見 spec §5）。 |
| `remark` | 旁註、記號說明、簡短歷史筆記、前方引用。**不是**主線知識。 |
| `caution` | 記號陷阱或容易忽略的限制條件，1–3 句。左側紅色裝飾條。 |
| `strategy` | 包含編號步驟的解題方法框（"given a problem of type X, do..."）。 |

（無 `exercise`——講義本體不收習題，見 [`CONTENT_SPEC.md`](CONTENT_SPEC.md) §14；習題另出獨立習題本。）

每節教學目標（不是配額）：**2–3 個 remark**、在 worked example 共用同一方法時 **≥1 個 strategy**。自然沒有 remark 的節就保持零；為了湊數而硬加不可取。

**Remark 實用性測試。** 在保留一個 `remark` 之前，問自己：*如果移除這段，讀者會失去什麼？* 如果老實的答案是「什麼都不會失去，它只是在充數」，就刪掉。主線事實、definition 的換句話說、示意性的例子、以及瑣碎的套套邏輯都**不是** remark——把它們提升為散文、放進 `definition` 的 *"Informally, ..."* 句子中、包在 `workedexample` 裡、或用一句散文連接起來。詳見 SPEC §5 的好用 vs. 壞用範例。

---

## 章節開頭（MUST）

章開場**併入該章第一節的片段**（`handout/fragments/chNN/sec-N-1.html`），作為該檔內第一個 `<article>`（在節標題那個 `<article>` 之前）——**不另設獨立的 `sec-intro` 片段**。開場必須有：

1. **概覽散文（1–2 段）**：建立本章動機，並說明它如何承接前一章。
2. **「By the end of this chapter, you will be able to:」技能清單**：每項以動詞開頭（"compute"、"verify"、"recognize"），約 3–5 項。
3. 緊接著就是第一節本身（同一片段內的第二個 `<article>`，標題為 `sec-title`）。

實際 HTML 標記（雙 `<article>` 開場結構、標題層級、清單、技能區塊）見任一章的第一節片段範例 [`handout/fragments/ch04/sec-4-1.html`](handout/fragments/ch04/sec-4-1.html) 與 [`handout/TYPESETTING_GUIDE.md`](handout/TYPESETTING_GUIDE.md)。

章節結尾 **MUST** 有一個不編號的 *Chapter summary* 區段：以連續散文重述本章的論證弧線（點名核心結果＋§號回指、串起主線、收 forward/backward fence），而非三桶條列。見 spec §4。

---

## 節的開頭

1–2 段動機說明。純計算的節可以用一句承接句開頭。不要用 definition 或 display math 開頭。

---

## 公式呈現：5 種模式

數學以 MathJax/KaTeX 渲染，五種模式的具體 HTML/MathJax 標記見 [`handout/TYPESETTING_GUIDE.md`](handout/TYPESETTING_GUIDE.md)。

| 模式 | 何時使用 |
|---|---|
| inline `\(...\)` | 屬於句子一部分的短公式。 |
| display `\[...\]` | 視覺核心的公式或多步計算。 |
| aligned display | 短小的上下對齊式或推導步驟。 |
| condition display | 公式帶有需要獨立間距的 trailing domain / range / branch condition。 |
| pair display | 恰好兩個短公式左右對比。過寬時自動堆疊。 |

經驗法則：
- 每個局部數學單元使用一種模式。不要在同一步驟中混用 centered、aligned 和 prose-condition。
- 要表達 formal "A iff B"，使用 display math 搭配 `\Longleftrightarrow`。

---

## 圖表規則

- 色盤僅三種角色：blue = primary、red = caution/counterexample、gray = auxiliary。色彩定義見 HTML 講義的 CSS／typesetting 規範（[`handout/TYPESETTING_GUIDE.md`](handout/TYPESETTING_GUIDE.md)）。
- **不要僅靠顏色編碼意義。** 至少用以下一種方式做冗餘編碼：line style、label、marker。線型慣例：solid = 主要曲線；`dashed` = 漸近線與參考線（包括 `$y = x$`）；`dotted` = 輔助／鷹架。圖表 **must** 在灰階列印與影印後仍然可讀。詳見 SPEC §10 完整的冗餘編碼規則。
- 圖片在 fragment 中以 `<figure>` 就地放置；分頁由 JS paginator（`place()`）處理，無 LaTeX 浮動體 placement。
- caption：sentence case，以句號結尾，描述數學目的。
- **worked-example 的圖**不可洩露例題要求讀者計算的量。
- 圖表密度目標：每個重要 definition / theorem 一張圖，計算型的節大約每 2–3 個 example 一張。

---

## Index 規則

HTML 講義目前沒有自動 back-of-book index 機制（原 LaTeX `\index{...}` 工具鏈已隨講義移入 `legacy/tex_handout/`）。以下「值得日後可被查找」的判準仍保留，作為撰寫時對重點項目的辨識依據；待 HTML 講義具備索引／查找機制後再落實。

可被查找的項目（**首次出現**處標示）：
- 每個被定義的術語；
- 每個具名定理；
- 每個記號（如 `\arcsin`、`\lim_{x \to a}`）；
- 每個讀者會想翻回去查的關鍵 example；
- 每個在本章引入的應用場景（physics、economics）；
- 每個記號陷阱（同時也會用 `caution` 標記）。

**查找測試**（當與上述列表衝突時，以此為準）：*讀者日後是否會想在不記得哪個章節引入的情況下找到這個項目？* 如果是，就值得標示。純粹的局部符號、一次性的設定、以及僅用於增添趣味而只出現一次的應用場景都**不**需要，即使它們名義上符合上述某個類別。

---

## Cross-reference 與編號

HTML 講義沒有 `\cref`/`\label`/`\eqref` 自動交叉參照機制；改用散文直接引用手寫編號（例：*"by Theorem 4.2"*、*"as in §1.3"*）。標記方式見 [`handout/_dev-archive/general/CONTRACT-html-writing.md`](handout/_dev-archive/general/CONTRACT-html-writing.md)。

- 引用定理／圖／節時，直接寫出手寫編號（*"by Theorem 4.2"*、*"see Figure 2.5"*），不要重述其內容。
- 方程式編號僅用於後續會被引用或屬於 formal statement 的方程式。

---

## 散文排版

HTML 標點與強調的具體寫法見 [`handout/TYPESETTING_GUIDE.md`](handout/TYPESETTING_GUIDE.md)；以下為原則。

- 強調：散文中僅用 `<em>`，且僅用於新術語的首次出現或極少數承載關鍵意義的片語。**不用** `<b>` / `<strong>` 做強調。
- 引號：使用 Unicode 彎引號（“…”）。**不用** ASCII `"..."`。
- 破折號：用 Unicode en dash（–）表數值範圍（*pp. 12–18*），em dash（—）表插入語。
- 省略號：使用 Unicode 省略號字元（…）。不要硬寫三個句點。

---

## HTML 片段中 **MUST NOT** 包含的內容

- 自訂共用樣式／元件就地內嵌（新的共用結構、樣式或色彩屬於 HTML 講義的 build／CSS，不要在單一片段裡硬塞 inline style 或 `<script>`）。
- 對抗 JS paginator 的手動分頁 hack（分頁由 paginator `place()` 全域處理）。
- ASCII straight quotes（改用 Unicode 彎引號）。
- 散文中的 `<b>` / `<strong>` 做強調（改用 `<em>`）。
- `env-solution`／worked example body 內的腳註、邊註等版面破壞性插入。

---

## 提交前檢查

在本地執行：

```powershell
python handout/build.py
```

build 成功（產出 `handout/chapterN-print-standalone.html`，print standalone、A4 分頁由 JS paginator 處理）後，內容把關不靠 LaTeX CI，而是 handout-prose-audit subagent（gate 1）＋ Codex（gate 2）。
（HTML 講義建置由 `.github/workflows/handout-checks.yml` 在 push／PR 把關；舊的 LaTeX 工具鏈——`tools/book_*.py`、`latexmk … main.tex`——已隨 LaTeX 講義移入 `legacy/tex_handout/`，原 `latex-checks.yml` 已移除，皆不再把關 HTML 講義。）

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
