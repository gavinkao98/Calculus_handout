# 微積分講義：排版總規範

**Version 3.2**——單點修訂：習題整體移出講義本體（使用者 2026-06-12 定案，習題將以**獨立習題本**呈現）。`exercise` environment、per-section Exercises placeholder 義務與相關規則退場（§5、§6、§14、§15）；課文範例的題源工作流程移至 [`CONTENT_SOURCING.md`](CONTENT_SOURCING.md)。其餘內容承襲 v3.1——在 v3.0 之後的精煉 pass，發生在文件框架拆分為 spec + quickstart + roadmap + exercises skeleton、且 preamble/template 實作落地之後。v3.0 是從零重寫取代 v1.x 和 v2.x，圍繞一個明確的產品定義重新組織規則書：一份 single-sided A4 英文講義，對象為準備自修大學微積分的高中生，搭配影片，以 Stewart / Rogawski 語域撰寫。v3.1 在此基礎上新增 content-level 的精煉（remark usefulness test 附好壞範例、figure redundant-encoding rule for grayscale and accessibility、index lookup test、per-section exercise numbering）。Changelog（§16）列出具體差異。

---

## 1. 目的與受眾

本專案產出一份給高中生的**微積分講義**，對象為想準備或自修大學微積分的學生。

- **Format**：canonical 列印格式為 print-standalone HTML（由 [`handout/build.py`](handout/build.py) 組裝出 `handout/chapterN-print-standalone.html`），印刷並作為講義發放（不裝訂成書）。Layout 比照 single-sided A4，12 pt Times、3.3 cm symmetric margins；A4 分頁由 JS paginator（`place()`）處理。排版細節見 [`handout/TYPESETTING_GUIDE.md`](handout/TYPESETTING_GUIDE.md)。
- **受眾**：有動機的高中生。他們有紮實的 precalculus 基礎、一些數學推理經驗、且有足夠的成熟度在遇到困惑段落時停下來試著自行釐清，但尚未達到大學數學主修的程度。
- **Companion medium**：強化講義的影片課程。
- **讀者與文本的關係**：**講義是自足的**。一個從未看過影片的學生仍應能端到端閱讀講義並吸收材料。影片是 reinforcement，不是主要管道。這是最重要的定位決策，驅動了以下大部分規則。

本文件中的每條規則服務於三個目標之一：

1. **Clarity over compactness.** 自學讀者不能卡住。如果一條規則使書更厚但閱讀體驗更清晰，該規則就是對的。
2. **Consistency across multiple authors.** 本書取材自多位教師的手稿；規則的存在是為了讓一個從 Chapter 3 讀到 Chapter 7 的讀者不會感受到語聲的變化。
3. **Lookup-friendliness.** 自學讀者會翻回去查。Index entry、per-type counter、有 label 的 formal statement、以及 chapter-end Summary 都支持此目標。

---

## 2. 如何閱讀這些規則

### Conformance keyword

本文件使用三個義務層級：

- **MUST**——規則具有約束力。違反即缺陷。
- **SHOULD**——規則為預設值。在特定情況下 rationale 轉移時可偏離，但作者必須能向 reviewer 解釋偏離的原因。
- **MAY**——該選項被允許。不使用不算缺陷。

沒有 keyword 的規則等同 SHOULD。

### Rationale

多數規則後面附有 **Rationale** 段落，解釋該規則為何存在。規則是 normative layer（「做什麼」）；rationale 是 interpretive layer（「為何是這條規則而非其反面」）。當新情況落在規則的字面文字之外時，Rationale 是解決邊界情況的首要指引——從目的推衍，而非機械套用。

### 與其他文件的關係

- [`README.md`](README.md)——repo layout、preamble structure、build instructions。
- [`video/README.md`](video/README.md)——當前（第二代）影片產線（主要 media path）。
- [`legacy/MANIM_REFERENCE.md`](legacy/MANIM_REFERENCE.md)、[`legacy/MANIM_STORYBOARD.md`](legacy/MANIM_STORYBOARD.md)、[`legacy/MANIM_CHECKLIST.md`](legacy/MANIM_CHECKLIST.md)——第一代 Manim animation pipeline（凍結；歸檔在 `legacy/` 下）。
- [`legacy/LEGACY_SLIDE_PIPELINE.md`](legacy/LEGACY_SLIDE_PIPELINE.md)——凍結的 static-slide/PDF path（僅供參考）。
- [`CONTENT_QUICKSTART.md`](CONTENT_QUICKSTART.md)——本檔的精簡日常參考伴侶。
- [`CONTENT_ROADMAP.md`](CONTENT_ROADMAP.md)——課程弧線、章節順序、prerequisites、per-chapter core skills。
- [`CONTENT_SOURCING.md`](CONTENT_SOURCING.md)——課文範例的題源與選題流程（開放題庫、provenance、授權）。
- [`handout/_dev-archive/general/CONTRACT-html-writing.md`](handout/_dev-archive/general/CONTRACT-html-writing.md)——HTML section fragment 的撰寫契約（authoritative HTML markup），編碼了本檔的規則。新章節以 HTML fragment 撰寫於 `handout/fragments/chNN/sec-*.html`。（legacy LaTeX 起始骨架 `_chapter_template.tex` 已移至 `legacy/tex_handout/chapters/`。）

當 repository layout 或 preamble 決策變更時，`README.md` 為權威。當撰寫或排版規則變更時，**本檔**為權威。

---

## 3. 語域與語聲

### 目標語域

講義以 **Stewart / Rogawski** 的語域撰寫：讓自學的高中讀者能讀懂、溫暖但不話嘮、對數學嚴謹但對讀者不冷淡。

校準用：

- **太 formal**：Spivak、Apostol、Rudin。短的陳述句、只用 "we"、直覺住在 formal environment 之外、歷史和應用筆記罕見。有動機的大學生能讀；自學的高中生往往不行。
- **太 informal**：某些課堂筆記 PDF、通俗數學書。不完整的句子、大量俚語、ad-hoc 結構。
- **目標**：Stewart。完整句子帶明確 connective、直覺穿插在散文中偶爾進入 definition environment、chapter 和 section opening 有動機段落、大量 worked example、頻繁的圖表。

語域**不是**非正式數學的藉口。Definition 仍精確；proof 仍完整；limit law 仍是 limit law。放鬆的是圍繞數學的散文，不是數學本身。

### Pronoun 策略

主要代名詞為 **"we"**，將讀者納入論證中。這是 Stewart / Apostol 傳統。

**"You"** 在兩個特定情境中允許：

1. **溫和提醒或驗證**，短暫轉向讀者：*"You should verify that $f^{-1}(f(x)) = x$ in this example."*
2. **前方引用**，針對讀者的未來工作：*"You will use this idea again when we study derivatives in Chapter 3."*

**"I" / "the author"**——永遠不用。這是多作者文本；第一人稱單數不適用。

祈使語氣是 setup 和 observation 的標準用法：*"Let $f$ be a one-to-one function."*、*"Consider the behavior near $x = 0$."*、*"Observe that both sides vanish at $x = 0$."*

### 銜接用語

以下用語受到鼓勵，能幫助自學讀者追蹤論證。它們不是 MUST——過度使用任何一句都比隱含的轉折更糟——但零銜接用語的草稿對目標語域而言幾乎總是太緊。

- *Notice that...* / *Observe that...*——引起對剛展示的特徵的注意。
- *Let us now...*——宣布新的步驟。
- *In other words...*——用更平易的語言複述剛給出的形式主義。
- *To see why this matters...*——引入一段動機。
- *We are ready to state...*——從鋪墊轉到 formal statement。
- *Before we proceed...*——為旁註或提醒暫停。

避免填充語（*basically*、*actually*、*essentially* 作為 hedge）、過度親暱（*you guys*、*super easy*）、以及黑板速記（在 running prose 中的 *iff*、*w.r.t.*、*s.t.*——展開它們）。

### 直覺先於形式

Formal statement（definition、theorem、proposition、corollary）**SHOULD** 在其前面有一或兩段散文，解釋為何值得引入這個概念以及它在直覺上應該意味著什麼。

`definition` body **MAY** 以一句 *"Informally, this means..."* 的口語化 restatement 結尾，**當 formal statement 在語法上很重**時——即它使用了巢狀 quantifier（如 $\varepsilon$-$\delta$）、多個邏輯子句、或初讀時難以解析的 symbol-dense notation。**當 formal statement 已接近英語且只有一兩個符號**時（如 $f^{-1}(y) = x \Longleftrightarrow f(x) = y$），跳過 inline gloss；此時動機屬於 definition **之前**的散文或後面的 remark。

Informal 句子 **MUST NOT** 引入 example、figure 或新 notation——如果 restatement 需要這些，提升為 definition 之後的獨立 remark 或散文段落。

Rationale：Stewart 語域加上自足的 handout 意味著讀者無法依賴老師即時「翻譯」formal statement。講義本身必須做這個翻譯，通常做兩次——一次在 formal statement 之前的動機散文中，一次（當語法上很重的形式主義有必要時，如 $\varepsilon$-$\delta$）作為 definition 內部的 inline gloss。「接近英語時跳過」的條款存在是為了防止 inline gloss 變成反射動作：一個 symbolic body 本身就是口語化的 definition 從 paraphrase 中得不到任何好處。

### 風格 do / don't

**偏好：**
- 簡潔的數學散文、完整句子、直接陳述、清晰的轉折；
- guided worked example（見 §5）；
- 明確的邏輯 connective（*therefore*、*because*、*in other words*）；
- 繁重形式主義之前的動機段落。

**避免：**
- lecture-note fragmentation；
- casual spoken filler 或 slang；
- 未解釋的邏輯跳躍；
- 多句 "meta" commentary 談本章在做什麼（信任結構和 chapter opening 的 bullet list 來做這件事）；
- prose 中的 inline abbreviation 如 *iff*、*w.r.t.*、*s.t.*——寫出來。

### 語聲參考範文

以下段落示範目標語聲。對語域有疑問時，將你的草稿與此範文對照。

> Not every function can be reversed. If two different inputs produce the same output, we cannot recover the input from the output uniquely. To build a rigorous version of this idea, we first need a name for the functions that avoid this problem.
>
> **Definition.** A function $f$ with domain $A$ is *one-to-one* if $f(x_1) \ne f(x_2)$ whenever $x_1 \ne x_2$. *Informally, a function is one-to-one when different inputs always give different outputs.*
>
> Notice how this condition rules out exactly the problem described above. If two different inputs $x_1$ and $x_2$ gave the same output, there would be no way to decide which one was "the" input corresponding to that output, and the reverse direction would be ambiguous.
>
> To check whether a specific function is one-to-one, we can use a graphical test that you have likely seen before in precalculus...

此語聲的關鍵特徵：

- 動機段落先於 definition（"Not every function can be reversed..."）。
- 直覺出現在 definition body 內（斜體 *"Informally, ..."* 句子）。
- Definition 之後的散文解拆該條件（*"Notice how this condition rules out..."*）。
- 明確的 bridge（*Notice how*、*To check...*）引導讀者經過每個轉折。
- "We" 是預設；"you" 出現為溫和的 forward-reference（"you have likely seen..."）。

---

## 4. 文件結構

### 標題層級

使用四個層級：

1. 章標題（`.chapter-head` 的 `<h1 class="ch-title">`）——Title Case。
2. 節標題（`<h2 class="sec-title">`）——Title Case。
3. 小節標題（`<h3 class="subsec-head">`）——sentence case。
4. 段落小標（`<p class="para-head">`）——sentence case，不編號，不進目錄。

**MUST NOT** 使用第三層以下的編號標題（即沒有 LaTeX `\subsubsection` 的對應物）。當小節需要拆成多於約四個子題時，要麼拆成兩個小節（優先），要麼使用 `para-head` 段落小標。

Rationale：將編號深度限制在三層保持目錄的可讀性。`para-head` 為短的平行子題提供輕量的第四層，不膨脹 ToC。

### 標題大小寫

- 章標題（`ch-title`）和節標題（`sec-title`）：**Title Case**（如 *Inverse Functions and Limits*、*The Precise Definition of a Limit*）。
- 小節標題（`subsec-head`）和段落小標（`para-head`）：**sentence case**（如 *Computing limits algebraically*、*Restricted sine and arcsine*）。
- Proper noun 無論大小寫風格一律大寫（如 *Newton's method*、*Stewart's notation*）。

Rationale：大小寫對比在視覺上標示層級。Title-case section 讀起來像學生在 ToC 中查找的具名 landmark；sentence-case subsection 讀起來像 running argument 的延續。

### Section title 內容

Section title **MUST NOT** 實質重複 chapter title。命名該 section 發展的具體主題，而非 chapter 的整體主題。

*例。* 一個標題為 *Inverse Functions and One-to-One Functions* 的 chapter 應有如 *Inverse Functions* 和 *One-to-One Functions* 的 section，而非另一個 *Inverse Functions and One-to-One Functions*。

Subsection title **SHOULD** 命名其內容的統一主題，而非僅列舉其中的對象。偏好 *Limits of piecewise-defined functions* 而非 *The absolute value function and the greatest integer function*。

### 章節開頭

每章 **MUST** 以以下兩個元素開頭，按順序，放在章標題（`chapter-head`）之後、第一個節標題（`sec-title`）之前：

1. **概述**：1–2 段散文，內容：
   - 點名本章涵蓋的數學領域；
   - 將本章與先前章節連結（如有）；
   - 預覽讀者將看到的核心結果。
2. **學習成果 bullet list**：以 *"By the end of this chapter, you will be able to:"*（或等價語句）為標題，包含 3–5 個具體成果，最多佔半頁。

概述是散文，不是 definition、theorem 或 remark。它 **MUST NOT** 引入新 notation 或陳述 formal result。

Bullet list 使用描述讀者將能*做什麼*的動詞（*solve*、*compute*、*recognise*、*prove*），而非章節將「涵蓋」或「討論」什麼。

*例。*

```html
<header class="chapter-head">
  <p class="ch-kicker">Chapter 1</p>
  <h1 class="ch-title">Inverse Functions and Limits</h1>
</header>

<p class="lead">This chapter develops two themes that together form the starting point of
calculus. The first is ... (1-2 paragraphs of prose)</p>

<p class="para-head">By the end of this chapter, you will be able to:</p>
<ul>
  <li>determine when a function has an inverse, and construct the inverse when it exists;</li>
  <li>work with the inverse trigonometric functions and their principal ranges;</li>
  <li>estimate limits from tables and graphs, and compute them using the limit laws;</li>
  <li>state and apply the precise \(\varepsilon\)-\(\delta\) definition of a limit.</li>
</ul>

<!-- 第一節 fragment 接於 handout/fragments/ch01/sec-1-1.html，header 為 <h2 class="sec-title"> -->
```

Rationale：自學讀者打開一章時會問*「我將學到什麼？」* Bullet list 在五秒內回答這個問題。概述在半分鐘內回答*「這和我已知的東西如何連結？」* 兩者都必須存在。

### 節的開頭

每節 **SHOULD** 在第一個 formal environment 之前以 1–2 段動機、直覺或應用背景開頭。

例外：一個內容純粹是計算的短節（如 *Direct substitution*、*Algebraic simplification of limits*）**MAY** 以一句連接到前一節的承接句開頭，跳過動機段落。

Rationale：自學讀者在投入閱讀精力之前需要一個在乎的理由。一個以 *"Definition 1.1."* 作為第一行開頭的節要求讀者先憑信念接受回報。

### 章節結尾

每章 **MUST** 以一個不編號的 Summary 區塊（`<section class="env">` 風格、標題為 Summary）結尾，半頁到一頁長，按順序包含三部分：

1. **Key definitions**——本章引入的 definition 術語 bullet list，按出現順序，每項一行引用 definition 名稱（不重述完整的 formal body）。
2. **Key theorems, propositions, and corollaries**——具名 formal result 的 bullet list，每項附一句 plain-English restatement。
3. **Key formulas and identities**——讀者應記住的 3–8 個最重要公式，緊湊呈現。

Summary 不引入新內容。它不出現在編號 section 序列中（不編號）。

Rationale：這是讀者的永久參考頁。一個月前讀過本章的學生想要複習時，應能在五分鐘內只用 Summary 重新吸收骨架。

### Build toggle（legacy）

HTML build（[`handout/build.py`](handout/build.py)）只組裝 print-standalone 變體（screen 變體已移除），沒有 chapter-level toggle：要納入哪些 section fragment 由 `build.py` 的章節清單決定，work-in-progress fragment 不列入清單即不會出貨。

（legacy 註記：凍結的 LaTeX book 在 `legacy/tex_handout/main.tex` 中有 `\ifprintbibliography`／`\ifincludescratchchapter` 兩個 top-level toggle，控制 bibliography 輸出與是否 include `_scratch.tex`；這些已不適用於 HTML handout。）

---

## 5. Environment 集

本專案使用恰好 **11 個 semantic block（HTML `<section class="env env-…">` 元件；在 legacy LaTeX 中為 environment）**。新的章節內容 **MUST** 使用其中之一；**MUST NOT** 引入新的 semantic block 而不更新本文件。下文沿用「environment」一詞指稱這些語義角色，HTML 中對應到 `env-*` class（見 [`handout/_dev-archive/general/CONTRACT-html-writing.md`](handout/_dev-archive/general/CONTRACT-html-writing.md)）。

### 11 個 environment

**Formal statement**（各有自己的 counter，chapter-scoped；見 §6）：

| Environment | 角色 |
|---|---|
| `definition` | 引入新的數學術語。 |
| `theorem` | 主要／重要的 formal result。 |
| `proposition` | 有用但不是該節 headline result 的 formal result。 |
| `corollary` | 值得為了教學而命名的附近 theorem 或 proposition 的直接推論。 |

**Worked material**：

| Environment | 角色 |
|---|---|
| `example` | Example prompt。總是包在 `workedexample` 中，總是與 `solution` 配對。 |
| `solution` | `example` 的 worked solution。 |
| `proof` | Theorem、proposition 或 corollary 的 proof。 |

**Aside and scaffolding**（各有自己的 counter）：

| Environment | 角色 |
|---|---|
| `remark` | 真正的旁註、notation 說明、歷史筆記、forward reference。 |
| `caution` | 關於常見錯誤或 notation 陷阱的警告。視覺上區別於 `remark`（見 §8、§10）。 |
| `strategy` | 解題策略或方法框。 |

**Semantic wrapper**（無 counter，本身無輸出）：

| Environment | 角色 |
|---|---|
| `workedexample` | 包裹恰好一組 `example` + `solution` 作為單一 pagination unit。 |

### 翻譯手稿標籤

來源手稿使用多種標籤。依數學角色翻譯，而非表面措詞：

| 手稿標籤 | 目標 environment |
|---|---|
| Def / Definition | `definition` |
| Property / Thm / Theorem | `theorem` 或 `proposition`（依角色） |
| Note / 註記 | `remark` |
| Warning / ⚠ / 注意 | `caution` |
| Method / Procedure / 解題技巧 | `strategy` |
| Homework / Practice | 不進講義本體——保留給獨立習題本（見 §14） |
| Worked calculation | `example` + `solution`，包在 `workedexample` 中 |

### 刻意排除

本專案**不**使用：

- `exercise`——v3.2 移除：講義本體不收習題（見 §14）；手稿的 Homework / Practice 材料歸入獨立習題本。
- `lemma`——對高中受眾而言，區分 lemma 和 theorem 的認知成本超過收益。在 graduate-level 書中會是 lemma 的結果，要麼吸收進 proof，要麼提升為 `proposition`。
- `subsubsection`——見 §4。
- 任何 `boxed`、`tip` 或 `note` environment——角色由 `remark`、`caution` 或 `strategy` 涵蓋。

### 各 environment 規則

#### `definition`

僅在首次引入新數學術語時使用。

Definition **MUST** 精確、形式化且簡潔。

Definition body **MAY** 以一句 *"Informally, this means..."* 的口語化 restatement 結尾。Informal 句子 **MUST NOT** 引入 example、figure 或新 notation。

**MUST NOT** 為本章不會再使用或發展的術語開一個 `definition`。對將來才會定義的術語的前瞻預覽放在散文中，可選地標為 index target（見 §11），不放在 formal environment 中。

Rationale：formal definition 是一個承諾——該術語現在可供重用。為本章從不引用的術語使用 `definition` 會稀釋這個承諾並弄亂 cross-reference graph。

#### `theorem`

保留給學生預期記住和重用的主要／重要結果。

Named theorem（Mean Value Theorem、Intermediate Value Theorem、Rolle's Theorem、Fundamental Theorem of Calculus、Squeeze Theorem 等）**MUST**：

1. 使用 `<section class="env env-theorem">`，並在 `env-head` 的 `<span class="env-name">` 放 Name，Name 為 Title Case 且完整拼寫（*Mean Value Theorem*，不是 *MVT*）；
2. （book-level index 在 HTML kit 中不存在；若日後要做整書索引，在此標記該 named theorem 為索引目標。詳見 §11。）

Rationale：named theorem 是僅次於 definition 的最常見查找目標。descriptive title 和 matching index entry 的組合是讀者進入本書的主要路徑。

#### `proposition`

有用且常可重用，但不是該節 headline result 的 formal result。典型用途：inverse function 的代數性質、inverse trigonometric function 的 composition identity、limit 的唯一性、one-sided limit 的 two-sided-limit 判準。

#### `corollary`

Theorem 或 proposition 的直接推論，因教學上值得點出而命名。典型用途：increasing-function test 作為 Mean Value Theorem 的 corollary；$n$-th root 的存在性作為 Intermediate Value Theorem 的 corollary。

不要機械地加 corollary。

#### `example` 和 `solution`

每個 `example` **MUST** 與恰好一個 `solution` 配對，兩者 **MUST** 包在一個 `<div class="workedexample">` 中（`env-example` + `env-solution`）。

`solution`（`env-solution`）在視覺上區別於 `proof`：粗體 "Solution." label（非斜體）、upright body text、trailing QED box（`<span class="qed"></span>`）。

- 當 solution body 以散文開頭時，保持 "Solution." inline。
- 如果 solution 的第一個 real content 是 block（`<ol>`、`<ul>`、display math），讓 "Solution." label 獨立成行（HTML 中由 skin CSS 處理）。
- solution 的結尾以 `<span class="qed"></span>` 標記 QED box；當最後一行是 display math 時，將該 QED span 緊接在 display 之後，使 box 視覺上附著於公式。

#### `proof`

僅用於數學 statement 的真正 proof。不要把 worked calculation 標記為 `proof`。

Theorem、proposition 或 corollary **MAY** 不附 proof。在以下至少一項成立時 include proof：

- 手稿包含一個；
- proof 對本章在邏輯上重要；
- proof 對學生理解在教學上重要。

不要機械地加 proof。

#### `remark`

真正的旁註、notation 說明、關於微妙限制的警告（當警告是 prose-shaped 而非 trap-shaped 時；trap-shaped 的警告見 `caution`）、短歷史筆記（2–5 句）、或 forward reference 到後面的章節。

Per-chapter **教學目標**：大約**每節 2–3 個 remark**（6 節的章約 12–18 個）。這是目標，不是生產配額。一個沒有自然 remark 的節應保持零而非為了湊數而加 padding；一個有五個真正有用 remark 的節應全部保留而非砍掉兩個以落在範圍內。下方的 usefulness test 在數量會導致錯誤決策時具有權威性。

`remark` **MUST NOT** 承載每個學生都必須閱讀的主線知識。如果內容是該節邏輯流的一部分，寫成散文。

**Usefulness test。** 在加一個 `remark` 之前，問：*如果這段被悄悄移除，讀者會失去什麼？* 如果老實的答案是「什麼都不會失去，它只是在充數」，就刪掉。如果答案是「一些背景、動機、歷史色彩或 future connection 會被錯過」，就保留。

**好用法**——這些屬於 `remark`：

- *歷史筆記*：*"Euler introduced this notation in 1748 in his* Introductio in Analysin Infinitorum*, where he also first treated $e$ as a limit rather than as the base of the natural logarithm."*
- *應用動機*：*"Exponential functions model radioactive decay, continuously compounded interest, and population growth under constant per-capita rates. We will return to each in §3.6."*
- *Forward reference*：*"The composition $f \circ f^{-1}$ we just computed will reappear as the setup for the inverse-function derivative in §4.3."*
- *Prose-shaped subtle restriction*：*"The identity holds for real $a > 0$; extending to complex or negative $a$ requires choosing a branch of the logarithm, which is outside this book's scope."*

**壞用法**——這些不屬於 `remark`；按指示改寫：

- *偽裝的主線事實*：*"Note that the limit laws we just proved also apply when both limits are infinite."* → 讀者需要這個；提升為散文、`proposition` 或 `corollary`。
- *Definition restatement 作為 padding*：*"In other words, a one-to-one function never sends two different inputs to the same output."* → 如果 definition 需要口語 gloss，把 *"Informally, ..."* 句子放在 `definition` body 內，不是獨立的 `remark`。
- *偽裝的 example*：*"For instance, when $x = 2$ we have $f(2) = 5$, which illustrates..."* → 如果它在 illustrate，它是 `workedexample` 內的 `example` + `solution`，不是 `remark`。
- *瑣碎的套套邏輯*：*"This follows from the theorem above."* → 如果讀者應注意到這點，寫一句連接兩者的散文；只說這個的獨立 `remark` 是 padding。

在 chapter 或 section 開頭、或關鍵概念緊前方的短歷史或應用動機筆記（2–5 句）是 `remark` 的好用法，直接支持目標語域。

#### `caution`

關於常見錯誤、notation 陷阱或容易忽略的限制條件的警告。視覺上區別於 `remark`（彩色 solid box 加 "Caution." label；見 §8）。

典型用途：

- Notation 陷阱：*"$\sin^{-1} x$ denotes the inverse sine; it does not mean the reciprocal $1/\sin x$."*
- 容易忘記的 domain restriction：*"The identity $\arcsin(\sin x) = x$ holds only when $x \in [-\pi/2, \pi/2]$."*
- 計算中的 sign-error 或 branch-choice pitfall。

`caution` 通常 1–3 句。如果更長，它可能是偽裝的 `remark`。

#### `strategy`

明確的解題策略或方法框。這是本專案提供的最高槓桿自學輔助工具；當一節的 worked example 會讓讀者問*「一般來說，我該如何處理這類問題？」*時使用它。

典型用途：

- *"Strategy for computing limits: (1) Try direct substitution. (2) If the result is an indeterminate form such as $0/0$, simplify by factoring or rationalising. (3) If neither works, try the squeeze theorem or rewrite using a known limit."*
- *"Strategy for finding an inverse: (1) Verify the function is one-to-one (optionally by the horizontal line test). (2) Solve $y = f(x)$ for $x$. (3) Swap $x$ and $y$."*

`strategy` 通常是一個短的編號列表，偶爾是一段散文。

Rationale：Stewart-style 的解題策略框是自學讀者最明顯受益的功能之一。此 environment 使策略可透過掃視而非重讀 worked example 並逆向工程模式來發現。

#### `workedexample`

語義 wrapper，測量合併的 `example` + `solution` body（上限 16 baselines）並預留等量的垂直空間，使短 example 不會擱淺在頁底而其 solution 滑到下一頁。

**MUST** 恰好包含一個 `example` 後接一個 `solution`。不巢狀；不將多組 example-solution 對打包在一個 wrapper 中。

**MUST NOT** 在 `workedexample` body 中包含 `\footnote`、`\marginpar` 或手動 `\hypertarget`：body 在最終 placement 前在 box 中測量，因此 page-anchored material 可能無法正確重定位。

Maintainer note：`workedexample` 依賴對其 body 的 one-shot capture。不要將它替換為重新展開 example/solution body 的 wrapper，否則 counter 和 pagination 假設會失準。

---

## 6. 編號與 Cross-Reference

### Counter

每個 formal-statement environment 有其**自身的 counter**，chapter-scoped：

- `definition` → Definition 1.1, 1.2, 1.3, ...
- `theorem` → Theorem 1.1, 1.2, ...
- `proposition` → Proposition 1.1, 1.2, ...
- `corollary` → Corollary 1.1, 1.2, ...

Aside environment 也有自身的 chapter-scoped counter：

- `example` → Example 1.1, 1.2, ...
- `remark` → Remark 1.1, 1.2, ...
- `caution` → Caution 1.1, 1.2, ...
- `strategy` → Strategy 1.1, 1.2, ...

Figure、table 和 numbered equation 也 per chapter reset：Figure 1.1、(1.1)。

Rationale：高中自學讀者翻回去查時會問*「Definition 1.3 在哪裡？」*，期望 "Definition 1.3" 是 Chapter 1 中的**第三個 definition**。Shared counter（本專案早期版本使用）會打破這個期望——"Definition 1.3" 可能前面穿插了 theorem 和 proposition，使編號在查找時 less informative。Per-env chapter-scoped counter 匹配讀者對 formal statement 和 aside environment 的心智模型。

Implementation note：HTML kit 沒有 auto-counter——所有編號都是 `env-num` 的**手寫文字**，per-type、chapter-scoped，由作者指派並手動維持一致（見 [`handout/_dev-archive/general/CONTRACT-html-writing.md`](handout/_dev-archive/general/CONTRACT-html-writing.md) 的 "Numbering and cross-references"）。（legacy 註記：凍結的 LaTeX book 以 `legacy/tex_handout/preamble/theorem_setup.tex` 中個別的 `\newtheorem{...}{Label}[chapter]` 宣告每個 environment；先前基於 `aliascnt` 的 shared-counter pattern 在 v3.0 中移除。）

### 手動編號

**MUST NOT** 手動編號 environment、figure、equation 或 section heading。讓 project template 處理編號。

### 方程式編號

只在以下至少一項成立時為 display equation 編號：

- 該方程式在同一章中被後續以散文引用（如 "(\*)"，透過 `\tag{*}` render 出 tag）；
- 該方程式被後續章節引用；
- 該方程式是 theorem、proposition 或 corollary 的 formal statement。

否則使用 unnumbered display math `\[...\]`（不加 `\tag`）。

Rationale：方程式編號是一個承諾——該方程式將在後面被命名。沒人引用的編號弄亂頁面並削弱有引用的編號的信號價值。

### Label 和 cross-reference

HTML kit 沒有 `\label`／`\cref`／`\eqref` auto-reference 機制。所有 cross-reference **MUST** 是引用手寫編號的散文：

- in-prose reference 直接寫出 type 前綴加手寫編號，如 *by Theorem 4.2*、*as in §1.3*、*Proposition 4.1*；
- 句首比照（*Theorem 4.2 shows that …*）；
- 方程式引用：以 `\tag{*}` render 出 tag，在散文中以 plain "(\*)" 引用。

**MUST NOT** 仰賴任何 auto-prefix／hyperlink 機制；編號的指派與引用一致性由作者手動維持（見 [`handout/_dev-archive/general/CONTRACT-html-writing.md`](handout/_dev-archive/general/CONTRACT-html-writing.md)）。

**手寫編號慣例**：per-type counter，在同一章跨節連續（Theorem 4.1, 4.2, …；Proposition 4.1, …；Definition 4.1, …），寫在 `env-num`、`fig-no`、`sec-no` 中。當在草稿中以助記 key 標示某項目以便日後對齊引用時，沿用 `type:short-description`（連字號）形式的描述性 key——`type` 前綴來自：

`def`、`thm`、`prop`、`cor`、`ex`、`sol`、`rem`、`caut`、`strat`、`fig`、`eq`、`sec`、`subsec`。

- 好：`fig:horizontal-line-test`、`thm:squeeze`、`def:limit-precise`、`caut:sin-inverse-vs-reciprocal`。
- 壞：`fig1`、`eq2`、`thm-important`、`horizontal_line`。

Rationale：手寫編號加散文引用是 HTML kit 的既定取捨（the main authoring tax）。一致的 type 前綴與 per-type counter 讓讀者的心智模型（「Theorem 4.2 是第 4 章第 2 個 theorem」）成立；downstream lint 應驗證每個 "Theorem N.M" 式引用都對應到存在的 `env-num`。

### 不同精度層級的 paired definition

當一個概念同時有 informal 和 precise（如 $\varepsilon$-$\delta$）definition 時：

1. **MUST** 使用指明精度層級的不同 label key，如 `def:limit-informal` 和 `def:limit-precise`。
2. Precise definition **MUST** 明確 cross-reference informal definition，如 *"This formalises the informal notion introduced in Definition 1.2."*（以散文引用 informal definition 的手寫編號）
3. Informal definition **MUST** forward-reference precise definition，如 *"A precise formulation is given in Definition 1.5."*（以散文引用 precise definition 的手寫編號）
4. 兩者都算獨立的 `definition` environment，各自 increment `definition` counter。

Rationale：回來查 *limit* 的學生應同時找到兩個版本並立即看到它們之間的關係。沒有 cross-link 的 silent duplication 是多作者微積分教科書中常見的困惑來源。

---

## 7. 公式呈現

本專案使用 **五種** formula display 模式（math 透過 KaTeX render）。所有其他變體（散文裡用 `<br>` 加垂直間距硬排公式等 ad-hoc vertical spacing）在 fragment source 中禁止，除非依 Exception Protocol 宣告。

### 五種模式

1. **Inline math** `\(...\)`——讀起來是句子一部分的公式。
2. **Display math** `\[...\]`——段落的視覺焦點的公式。
3. **Aligned display**——stacked aligned chain（共享 `=` anchor 的一系列相關方程式）；以 `\[ \begin{aligned} a &= b \\ &= c. \end{aligned} \]` 寫出。
4. **Condition display**——公式後接 domain / range / branch condition；在 HTML 中以 trailing 散文或 KaTeX 內的 `\text{...}` condition 呈現（kit 無 LaTeX 的 `conditiondisplay` 巨集）。
5. **Pair display**——恰好兩個短的可比較公式 side-by-side 顯示（任一側過寬時改為堆疊）；在 HTML 中以並排的兩個 display 或對應的 fragment 結構呈現（kit 無 LaTeX 的 `\pairdisplay` 巨集）。

早期 LaTeX 版本的 equivalence helper `\iffstackeddisplay` 和 `\iffwithconditions` 在 v3.0 中**移除**。改用 ordinary display math 搭配 `\Longleftrightarrow` 加 inline 或散文 condition。（aligneddisplay／conditiondisplay／`\pairdisplay` 原為 preamble 定義的 LaTeX 巨集，現 preamble 已移至 `legacy/tex_handout/`；上述為其 HTML 對應寫法。）

### 何時使用

**Inline math** 用於：

- 單一符號、短表達式、短區間；
- 散文中的短結論（*"...and hence $f'(0) = 0$."*）；
- example prompt 中適合放在句子裡的短目標表達式。

**Display math** 用於：

- definition、theorem、proposition 或 corollary 中的核心公式；
- 讀者應垂直掃視的多步計算；
- 使用 `cases`、`aligned` 或類似高結構的公式；
- 段落的視覺焦點而非句子流一部分的公式。

**Aligned display**（`\begin{aligned}`）——兩個以上公式形成 list、progression、hypothesis set 或共享 vertical anchor 的 chain of equality 時。

**Condition display**——公式帶有 trailing domain、range 或 branch condition，受益於專用呈現而非塞入公式或丟進散文中時。

**Pair display**——僅在恰好兩個短公式被 left-to-right 比較（不是 top-to-bottom）時。如果任一側過寬（約超過半行寬），改為上下堆疊；不要依賴 stacking fallback 來救長內容。

Rationale：五種模式是語義區分停止幫助作者並開始造成決策成本的臨界點。早期版本有七種模式；v3.0 中移除的兩個（`\iffstackeddisplay`、`\iffwithconditions`）所處理的 use case 用 ordinary display math 搭配 `\Longleftrightarrow` 加 inline condition 就能乾淨處理。

### Display block cohesion

在一個局部數學單元內（單一 derivation、單一 theorem statement、單一 solution step），作者 **SHOULD** 一致地使用一種 display grammar。

此規則是 SHOULD，不是 MUST：當一個*真正的新想法*接在 derivation 之後時混用 grammar——例如 aligned display chain 後接一個 final inline conclusion——是自然且可接受的。規則禁止的是在同一三句話範圍內一個 centred display、一個 aligned display、一個 prose-embedded formula 和一個 condition display 混雜做代數工作。

具體指引：

- 如果幾個公式是一個 derivation 中的 peer，將它們組合在一個 aligned display（`\begin{aligned}`）中；不要分散在多個 `\[...\]` block 中。
- 如果短的 follow-up formula 在散文後自然地讀出，保持 inline。
- 不要把 *"provided that $x \ne 1$"* 這類 condition 作為 extra alignment column 附加到 aligned row 上——如果該 condition 只適用於其中一行；把它移入 display block 前後的散文中。

### Inline fraction：`\frac` vs `\dfrac`

Inline math 中預設用 `\frac`。只在 inline fraction 在縮小尺寸下確實難以閱讀、或與鄰近的 display formula 匹配時才用 `\dfrac`。

將 `\dfrac` 保留給：

- 分子或分母結構實質的 fraction：$\dfrac{f(x+h) - f(x)}{h}$；
- 追蹤特定 $\varepsilon$-$\delta$ bound 的 fraction：$\dfrac{\varepsilon}{4}$（當 fraction 本身是討論對象時）；
- 與相鄰 display equation 使用同一表達式視覺配對的 inline fraction。

Running-prose fraction（$\frac{1}{x}$、$\frac{1}{x^2}$、$\frac{\pi}{2}$）保持 `\frac`。

在 table 中，偏好 `\tfrac` 或 plain-text 形式以保持 row 緊湊。

Display math 中的所有 `\frac` 自動以 full size render；display math 中的 `\dfrac` 是多餘的。

### Inline `\displaystyle`

**謹慎地**使用 `\(\displaystyle ...\)`，僅在以下兩項同時成立時：

- 公式必須留在句子中，且
- 它包含在 inline size 下難以閱讀的 large fraction、integral、sum 或 limit。

*允許的例子*：*"the difference quotient $\displaystyle \frac{f(x+h) - f(x)}{h}$"*。

不要將 `\displaystyle` 作為讓公式看起來「重要」的預設方式。如果一個公式重要到需要突出，把它移到 display math。

### Delimiter sizing

- 當被包圍的表達式包含 tall object（full-size fraction、nested radical、large operator）時使用 `\left...\right`。
- 對短表達式使用 fixed-size delimiter：偏好 `(x+1)` 而非 `\left(x+1\right)`。
- 對帶 displayed fraction 的 interval notation，`\left[-\tfrac{\pi}{2}, \tfrac{\pi}{2}\right]` 是合適的，因為 `\tfrac` 使 fraction 保持在縮小的高度。

### 規則速查表

| 情境 | Helper |
|---|---|
| 句子中的短公式 | inline math |
| 主要公式或視覺核心表達式 | display math |
| 對齊的方程式 chain | aligned display（`\begin{aligned}`） |
| 帶 trailing domain/range/branch condition 的公式 | condition display |
| 恰好兩個短的可比較公式，side by side | pair display（兩個並排 display） |
| 兩個 statement 的 formal equivalence | display math 搭配 `\Longleftrightarrow` |
| 帶 large operator 的 inline formula，句子不能斷 | `\(\displaystyle ...\)` |

---

## 8. 排版

### 破折號

- Hyphen（`-`）：連字詞如 *one-to-one*、*left-hand*、*real-valued*。
- En dash（Unicode `–`）：數值和頁碼範圍如 *pages 12–15*。
- Em dash（Unicode `—`）：散文中的插入語。謹慎使用；comma 或一對括號通常更好。

### 省略號

散文中使用 Unicode 省略號字元 `…`（U+2026），不要硬寫三個 literal period。數學式中使用 KaTeX 的 `\dots`（context-aware）：

- 在數學文字中：*the sequence \(a_1, a_2, \dots, a_n\)*。
- 在帶 operator 的 display 中：*\(a_1 + a_2 + \dots + a_n\)*——KaTeX 自動選擇 `\cdots`。

### 引號

- 散文中的雙引號：直接用 Unicode curly quotes `“…”`（檔案為 UTF-8）。
- 單引號：`‘…’`。
- **MUST NOT** 在 fragment 中使用 straight ASCII `"..."`。（HTML kit 中改用真正的 Unicode 標點；引號／省略號的一致性靠手動與下游 lint 檢查。）

### 強調

`<em>...</em>` 是 running prose 中唯一允許的強調機制。

- `<em>term</em>` **MUST** 標記 `definition` body 中新術語的引入。
- `<em>term</em>` **MAY** 標記 formal definition 之前的動機散文中術語的首次出現。每個術語最多一次。
- `<em>word</em>` **MAY** 用於關鍵字語氣強調——突顯讀者容易漏看的限定詞或轉折，如 *not*、*all*、*at*、*every*、*always*。限於真正改變句意的字；不濫用。
- `<em>lead sentence</em>` **MAY** 用於 strategy 清單各條的領句（opening phrase），作為視覺分隔，讓讀者快速掃描。
- **MUST NOT** 在 running prose 中使用 `<b>...</b>` 或 `<strong>...</strong>` 做強調。Bold 保留給 environment label（`env-kicker`）和 theorem heading，由 skin CSS 自動處理。
- **MUST NOT** 對同一術語強調兩次。
- **MUST NOT** 用 `<em>` 標記數學符號——數學斜體由 MathJax 處理。

Rationale：單一強調機制意味著讀者學一個 visual cue。Running prose 中多種強調機制稀釋信號並迫使作者做出應被預先決定的 style 選擇。

### 新 environment 的視覺 label

`caution` 和 `strategy` environment 使用**彩色 solid box 加文字 label**，色彩由 `shared/skin-hs.css` 依角色自動套用（在 HTML kit 中 `caution`、`strategy` 是 solid box，非左側裝飾條）。

- `caution`（`env-caution`）——red box，"Caution." label。
- `strategy`（`env-strategy`）——violet box，"Strategy." label。

Rationale：色彩編碼承載教學意義，文字 label 確保語義不只靠色彩傳達（與 §10 的冗餘編碼一致）。色彩在 `shared/skin-hs.css` 集中定義一次，作者不在 fragment 內寫 inline `style=`。

### 數學間距

- Binary relation 和 operator：依賴 LaTeX 的 built-in spacing（`\ne`、`\le`、`\ge`、`+`、`-`）。
- 積分中的微分符號：differential 前加 thin space（`\int_a^b f(x)\,dx`）。
- 函數應用：不加空格（`f(g(x))`，不是 `f( g(x) )`）。
- 只在 alignment 或 readability 確實需要時使用 `\,`、`\;` 或 `\quad`。

---

## 9. 記號

記號 **MUST** 在所有章節間保持一致。使用以下標準形式，除非保留特定手稿慣例（此時 **SHOULD** 以 `caution` 或 `remark` 在首次使用時標註該慣例選擇）。

| 概念 | 偏好的記號 |
|---|---|
| Inverse trigonometric function | `\arcsin x`、`\arccos x`、`\arctan x`、`\arccsc x`、`\arcsec x`、`\arccot x` |
| Logarithm 和 exponential | `\ln`（natural log）、`\exp` 或 `e^x` |
| Trigonometric function | `\sin`、`\cos`、`\tan` 等（皆透過 `\operatorname`-style macro，非斜體字母） |
| Derivative | `f'(x)` 表示一般的 derivative；`\dfrac{d}{dx}` 表示 explicit differential operator |
| Two-sided limit | `\lim_{x\to a} f(x) = L` |
| One-sided limit | `\lim_{x\to a^-}`、`\lim_{x\to a^+}` |
| Infinite limit | `\lim_{x\to a} f(x) = \infty`、`\lim_{x\to a} f(x) = -\infty` |
| 實數線 | `\mathbb{R}` |
| Interval notation | `(a,b)`、`[a,b]`、`[a,b)`、`(a,b]`；unbounded endpoint 用 `(-\infty, a)`、`[a, \infty)` |

不要在章節間切換記號風格而沒有充分理由。如果手稿採用了一個不太常見但數學上合理的慣例（例如 inverse trigonometric function 的非標準 principal range），保留它，並在首次使用時以 `caution` 標註常見的替代方案。

`\sin^{-1}` 作為 inverse sine **不是**本書的記號。如果必須提及它（例如讀者可能在其他地方遇到），在 `caution` 中引入並區分它與 reciprocal $1/\sin x$。

Rationale：notation drift 是多作者教科書中最顯眼的 inconsistency 之一。在規則層級固定一個小型 canonical list 消除了一整類 editorial decision 並使 index 更乾淨。

---

## 10. 圖表與色彩

### 何時使用圖表

圖表是教學，不是裝飾。只在確實有幫助時才加。

**SHOULD** 在以下位置或附近加圖表：

- 每個重要 definition，尤其是 geometric 或 graphical 概念；
- 每個有可視覺化 statement 的重要 theorem；
- 計算型 section 中大約每 2–3 個 example；
- solution 內部：當解題步驟涉及幾何設定、積分區域、截面形狀、向量分解等空間或圖形推理時，在該步驟處加圖——這類圖是解題論證的一部分，不只是題目的配圖。

不要加裝飾性圖表。不要加一張目的是填充半空頁面的圖。

Rationale：自學讀者嚴重依賴視覺直覺。一章每五頁一張圖對高中讀者而言太稀疏；Stewart 密度（視覺豐富主題中接近每頁一張圖）是正確的鄰域。

### 主動標記圖機會

撰寫內容時（Mode A），**MUST** 在每個符合上述「SHOULD 加圖」條件的位置插入佔位符，即使當下不立即繪圖：

```html
<!-- [FIGURE-OPPORTUNITY] 描述：這張圖的教學功能
     類型：graph | diagram | multi-panel
     理由：為何此處用圖比純文字更有效 -->
```

佔位符規則：

- **描述**欄寫圖的教學目的（如「幾何直觀：\(\epsilon\)-\(\delta\) 鄰域與函數值的帶狀關係」），不是「畫個圖」。
- 當散文宣告了**定義域限制、間斷、或 \(f(a)\) 未定義／不等於極限值**時，**描述**欄 **MUST** 一併記下這些事實與其圖示後果（如「\(x = 0\) 未定義 → 不放點或用空心點」「\(x = 2\) 跳點 → 實心＝取到的值、空心＝另一支極限」），使日後繪圖階段不與散文的定義域矛盾。Rationale：繪圖常是寫稿之後的另一道工序，屆時已離開散文語境；把定義域事實寫進佔位符，繪圖者才不會在未定義處誤畫實心點（對應稽核 D5／D6——此類曾為 ch01 圖稽核 blocking）。
- **類型**欄對應 §10.2 工具選擇：`graph`（座標圖）、`diagram`（schematic／概念圖）、`multi-panel`（§10.3）。
- 佔位符是 HTML 註解（`<!-- ... -->`），在頁面中 inert、不影響 render；後續 Mode B 稽核時逐條裁決是否繪圖。
- 已有手稿圖或已繪好的圖**不需要**再標佔位符——只標「應有圖但目前沒有」的位置。
- 如果某段散文的概念純代數操作、無幾何或圖形直觀可言，不需要硬標。

Rationale：教師手稿通常不含圖，AI 生成內容時亦不會主動產圖。佔位符讓「應該有圖但沒有」的缺口在寫作階段就被捕捉，而非等到排版或學生回饋後才發現。

### 繪圖落地前自檢（write-time figure checklist）

上一節「主動標記圖機會」確保 Mode A 在寫稿時捕捉「該有圖」的位置；本節是其對稱物——當圖**真正落到** `buildPlot(cfg)` 繪圖函數（fragment 的 `<figure data-fig>` 對應的繪圖實作，機制見 [`handout/CLAUDE.md`](handout/CLAUDE.md) 的「圖表系統」）時，作者 **MUST** 在宣告該圖完成前逐項自檢下列各點。每項標注其對應的事後稽核維度（見 [`handout/_audit/FIGURE-AUDIT-RUBRIC.md`](handout/_audit/FIGURE-AUDIT-RUBRIC.md) 的 D1–D8），使「寫稿預防」與「事後稽核」共用同一錨點。

- **承載軸刻度可讀（D4）**：讀圖題或任何需讀出座標的軸，凡刻度值**非整數且非 \(\pi\) 倍數**（如 \(\tfrac{1}{2}\)、具名刻度 \(a\)）**MUST** 在 tick 物件顯式給 `tex`。整數與 \(0,\pm\tfrac{\pi}{2},\pm\pi,\pm 2\pi\) 由 `buildPlot` 的 `piTex` 自動補；**不要**假設它會自動補非整數小數——那會靜默地只畫刻度線、不出數字。
- **點記號對齊定義域（D6／D5）**：每顆 `dot` 都 **MUST** 對照散文宣告的定義域與 \(f(a)\) 是否定義——有定義且值即此點 → 實心（預設）；未定義／開區間端點／僅為某一支的極限值（非 \(f(a)\)）→ **MUST** 設 `hollow:true`；函數在該點根本不存在 → **不放** `dot`。`dot` 預設實心，未定義處漏設 `hollow` 會誤暗示該點有定義（ch01 squeeze \(x^{2}\sin(1/x)\) 圖即因在 \(x = 0\) 放實心點被判 blocking）。
- **姊妹圖一致（D4／D5）**：新增或修改一張圖前，先看同節講同一概念的姊妹圖，照抄其 `xlabel`／`ylabel` 與刻度標法（同一個軸給同樣的 `tex`）。多面板／多連圖 **SHOULD** 用共用工廠函數集中設定 `xlabel`／`ylabel`／`xticks`／`yticks`，只讓 `items` 逐面板變動，避免跨面板漂移。
- **刻度節制（D1）**：只標「承載教學值」或「錨定尺度必需」的刻度；刪掉非讀值所需、又落在曲線／端點／軸密集區的多餘刻度。
- **in-figure label 不蓋資訊（D1）**：每個圖內文字放在空白處，不撞軸、不撞曲線、不撞其他 label、不出界（亦見本節「Label economy」）。
- **viewing-window 可辨（D2／D3）**：x／y-range **MUST** 使承載教學點（漸近線、截距、彎曲、轉折、交點、標記點）落在可視區內，不貼線、不爆框、不被裁；非承載元素被壓縮可接受。此項最終以 render 後的 PNG 為準，寫稿時憑 range 預估自查。
- **圖↔caption／prose 一致（D5）**：圖實際畫的（單側 vs 雙側、對稱性、定義域、漸近線）與 figcaption、定義、範例陳述相符。
- **不洩答案（D7）**與**灰階存活（D8）**：已分別由本節「Worked-example 圖不可洩露答案」與「Grayscale 和 accessibility 的冗餘編碼」規範，落地時一併套用。

Rationale：D7（no-spoiler）與 D8（冗餘編碼）原已有寫稿規範，但 render-geometry（D1–D4）與圖↔prose 一致性（D5）過去整片空白、全靠事後 PNG 稽核補抓；ch01 圖稽核（gate-1／gate-2）即在這些類別連續抓到**可預防**的 blocking（承載軸缺 `tex`、未定義點誤畫實心）。把它們轉成落地前自檢，可在繪圖當下攔下，而非每輪靠稽核回補。（其中「承載軸整數刻度缺 `tex`」一類已另從工具根治——`piTex` 現會自動補整數；本檢核項僅餘非整數小數需顯式 `tex`。）

### 工具選擇

HTML kit 的圖以 standalone HTML 的 `FIGS` 物件中註冊的繪圖函數（`buildPlot(cfg)` 產出 SVG，由 `hydrateFigures()` 依 fragment 的 `<figure data-fig>` 注入；機制見 [`handout/CLAUDE.md`](handout/CLAUDE.md) 的「圖表系統」）呈現，schematic diagram 也可用 inline SVG（見 [`handout/_dev-archive/general/CONTRACT-html-writing.md`](handout/_dev-archive/general/CONTRACT-html-writing.md) 的 "Figures"）。依教學功能選擇圖型：

- **graph**——coordinate graph、plotted function、asymptote、analytic behavior（`FIGS` 的 `buildPlot` 繪圖 helper）。
- **diagram**——conceptual diagram、mapping diagram、interval、arrow、geometric sketch（inline SVG 或繪圖 helper）。

### 多面板比較圖

當兩到三張相關圖片屬於一起時（如 restricted sine / cosine / tangent branch；left-hand / right-hand / two-sided limit graph），將它們排在單一 `<figure>` 中，由 `FIGS` 的繪圖函數回傳 multi-panel layout（side-by-side panel）。

規則：

- 2 或 3 個 panel 的水平 layout。超過 3 個太擠；改為垂直堆疊。
- 一個共享 caption 描述比較說明了什麼。
- 每個 panel 下方有一個小的 in-panel label 命名該 panel（如 *Restricted sine*、*Restricted cosine*）。

### Callout 與 annotation

圖表 **MAY** 包含指向特定特徵的帶短文字 label 的箭頭（"callout"）（*"Here the function is not defined."*、*"Inflection point."*、*"Asymptote."*）。

Callout 文字 **SHOULD** 是完整句子或完整名詞片語；句子以句號結尾，名詞片語不加。

Rationale：自學讀者從有 annotation 的圖表中吸收資訊的速度顯著快於無 annotation 的。Stewart-style callout 是目標語域中最高槓桿的視覺元素。

### Label economy

圖表只承載*閱讀*它所需的 label：axis name、讀者必須辨識的尺寸或 point、curve label（見下方 "Redundant encoding"）、以及短 callout。其他一切——命名每個 region 或 area、重述公式、拼出 construction——屬於 **caption 和 body prose**，不要塞進圖畫上。

- **SHOULD** 保持 in-figure text 在使圖片可讀的最低限度。當一個 label 會承載一個子句份量的解釋時，把那個解釋移入周圍的文字，只在圖上留一個短 anchor。
- 一張內部讀起來像一段話的 diagram 是 over-labelled。偏好乾淨的圖畫加一句散文，而非密布公式的圖畫。

Rationale：不雜亂的圖表掃描更快，而 body prose 是自學讀者期望推理所在之處。（實例：product-rule area rectangle 只以其邊長和一個原始面積 anchor 標記；strip 和 corner area 在文字中命名，不在圖上。）

### 色彩慣例

本專案使用三色 palette，在 `shared/skin-hs.css` 中集中定義一次，全程以 CSS 變數／class 引用（不在 fragment 內寫 inline 色彩）：

| 色彩 | 角色 | 典型用途 |
|---|---|---|
| Blue | primary / main object | 主要函數、主要曲線、圖的焦點 |
| Red | warning / asymptote | 漸近線、dashed reference line、visual warning；`caution` box |
| Gray | auxiliary / structural | 軸元素、guide line、reference construction |

Working-draft hex 值：blue `#1f4e79`、red `#c0392b`、gray `#7f7f7f`。確切值可在 implementation 時微調；上方的語義指派是固定的。

額外的色彩 **MUST** 透過 Exception Protocol（見 §13）引入並在 chapter 層級記錄。

### Grayscale 和 accessibility 的冗餘編碼

色彩承載教學意義但 **MUST NOT 是唯一承載它的管道**。每張使用色彩區分 curve、line、region 或 point 的圖表 **MUST** 也用以下至少一種方式區分：

- **Line style**——solid 用於 primary curve、`dashed` 用於 reference line 和 asymptote、`dotted` 用於 auxiliary / scaffolding construction；
- **Label**——每條 curve 或 line 在其本體附近有 label（*$f$*、*$f^{-1}$*、*$y = x$*），不僅靠 colour legend；
- **Marker**——key point 使用 `$\bullet$` / `$\circ$` / `$\square$`，使 labelled point 在色彩消失時仍可區分。

本書慣例：

- primary curve：blue、solid、有 label；
- inverse 或 paired curve：solid 或 dashed（依其在 pair 中的角色）、有 label；
- asymptote 或 reference line（包括 \(y = x\)）：dashed，red 如果是 warning/asymptote，gray 如果是 scaffolding；在空間允許處以其方程式 label；
- auxiliary construction（guide line、midpoint、reference rectangle）：gray、dotted；
- key point：`$\bullet$` 表示 filled、`$\circ$` 表示 open，以 coordinate 或 name label。

圖表 **MUST** 在 grayscale 下保持可讀——色彩是語義的，疊加在 line-style 和 marker 資訊之上，而非取代之。

Rationale：學生在 single-sided 黑白印表機上列印、影印章節、或在沖淡色彩的顯示條件下閱讀。一張說「紅色曲線 vs. 藍色曲線」的圖在色彩消失時會退化為兩條相同的灰色曲線。既有的 grayscale-readability 目標是一個承諾，不是抽查；冗餘編碼是信守承諾的方式。冗餘編碼同時也支持色覺異常讀者，無需獨立的 accessibility pass。

### Placement

- 預設將圖放在 source 中介紹它的散文旁，由 JS paginator（`place()`）就地分頁，使圖精確停在放置位置附近。
- 如果該位置會在頁面上產生過多空白，先嘗試調整周圍的散文（改寫、精簡或重排附近段落）。
- 如果散文調整無法解決問題，強制在圖前分頁是允許的，作為 Exception Protocol 下的**記錄例外**。
- 保持圖表的尺寸使其與介紹它的散文能放在同一頁。

Rationale：對教學導向的 handout，圖與散文的鄰近性在教學上很重要。HTML kit 的 paginator 就地排版、讓圖貼著其散文；多餘的垂直空間由分頁邏輯吸收。當這個 trade-off 在局部失敗時，exception 是可以的，但必須記錄。

### Caption

- Sentence case。
- 簡潔且數學化。
- 以句號結尾。
- 描述圖的數學目的，而非僅描述其內容。

好：*Geometric interpretation of the horizontal line test.*、*The sine function on $\mathbb{R}$ is not one-to-one.*

壞：*Graph.*、*Diagram of sine function.*

### Worked-example 圖不可洩露答案

如果一個 `example` 要求讀者計算邊長、角度或 coordinate，伴隨的圖 **MUST NOT** 在其 label 中顯示計算出的值。以變數（$a$、$\theta$）標記未知量，讓散文推導出值。

Rationale：一張在學生被要求計算的邊旁邊已顯示「$3$」的 diagram 會把 example 變成照抄圖片而非實際計算的過程。

### 手稿優先

如果手稿已包含 figure idea，保留其數學目的。以上方指定的乾淨教科書 style 重繪；不保留手寫或黑板 styling。

---

## 11. Index 策略

HTML handout 目前**沒有** back-of-book index——kit 沒有 `\index` 巨集，也不做 per-section 索引。本節記錄的 index 策略（lookup test、該索引什麼、sub-entry）保留為 book-level 索引的內容判準：若日後決定產出整書索引，依此標記索引目標。（legacy 註記：凍結的 LaTeX book 以 `imakeidx` 在 `latexmk -pdf main.tex` 的 three-pass compile 下產生 index，已不適用於 HTML handout。）

> 機制註記：HTML kit 沒有 `\index` 巨集，目前不產出 index。以下規則是 book-level 索引的**內容判準**——標示哪些項目「屬於索引」；待整書索引落地時據此產生。下文以 `index-target` 表示「應被索引的項目」，原 LaTeX 的 `\index{key}` 對應為「以 key 標記的 index target」。

### Lookup test

在把任何項目標記為 **index target**——無論 mandatory 或 optional——之前，都套用 **lookup test**：*讀者日後是否會想在不記得哪個章節引入的情況下找到這個項目？* 如果是，它屬於 index。

未通過 lookup test 的項目**不**屬於 index，即使作者碰巧給它們了名字：單一 proof 中的一次性 substitution variable、僅在自身段落中使用的 throwaway example label、proof 從不再引用的 intermediate lemma-style claim、只在 context 中有意義的 mnemonic。加入這些會弄亂 index 並降低讀者真正需要找到的項目的品質。

下方的 mandatory 和 optional 列表是其類別的 lookup test 的預設答案。當 mandatory 類別中的特定項目在其 context 中確實未通過測試時（例如僅用於增添趣味的一次性 applied setting），lookup test 優先：不加，並在 exception comment 中標註省略。

### Mandatory entry

以下項目 **MUST** 在其首次出現處標記為 **index target**（key 形式列於下方，供整書索引落地時使用）：

1. **每個由 `definition` 引入的術語**——primary term 和在其他地方使用的 synonym。
2. **每個 named theorem**——*Squeeze Theorem*、*Intermediate Value Theorem*、*Mean Value Theorem*、*Fundamental Theorem of Calculus* 等。
3. **每個本書引入的 notation**——`\arcsin`、`\lim`、`\int` 等，使用 sort-key-plus-display 形式（拼寫 key `@` 顯示 glyph）：`arcsine@$\arcsin$`、`limit@$\lim$`、`integral@$\int$`。
4. **每個本書期望讀者記住名稱的 key example**——$1/x$-near-$0$ example、$x^{2}\sin(1/x)$ squeeze example 等。Key 形式：`1/x near 0@$1/x$ near $0$`、`x^2 sin(1/x) example@$x^{2}\sin(1/x)$ example`。「期望讀者記住名稱」就是 lookup test：如果 example 在書中後面被引用或是 field 本身命名的 canonical counterexample，就標為 index target。純粹是方法 local illustration 的不需要。
5. **每個可能困惑讀者的 notation trap**——*sine inverse vs reciprocal*、*absolute value vs interval brackets* 等。Key 形式：`sine inverse vs reciprocal@$\sin^{-1}$ vs $1/\sin$`。
6. **每個引入新術語或將被重用的 applied setting**——*instantaneous velocity*、*tangent line*、*rate of change*、*slope*、*area under a curve*。僅用於增添趣味而只出現一次的 incidental application（introduction 中的一杯水、圍繞掉落的球的 numerical example 且從不重訪）不需要。

### Optional entry

- 首次在歷史筆記中提及的 named mathematician。
- 超出 (4) 的額外 example keyword。

### 規則

1. 將 index target 標在術語的**首次出現**處，不是每次後續提及。
2. 使用 **sentence-case** key：`one-to-one function`，不是 `One-to-One Function`。
3. 使用 **sub-entry**（透過 `!`）：`limit!one-sided`、`limit!infinite`、`asymptote!vertical`。
4. 對 notation，總是使用 sort-key-plus-display 形式 `key@$\text{symbol}$`，使 index 依拼寫 key 字母排序同時顯示 glyph。

Rationale：index 是自學讀者在休息後回到書本時的主要導航工具。稀疏的 index 迫使讀者翻閱章節尋找概念被引入的位置；密集、well-cross-linked 的 index 將每個後續概念變成兩秒的查找。寫作時加 index entry 的成本很小；事後重建 index 的成本很大，且重建永遠不如即時準確。

---

## 12. 原始碼衛生與 CI

### Fragment 中 MAY 包含的內容

- 標題結構：`chapter-head`／`sec-title`／`subsec-head`／`para-head`（見 §4）。
- §5 中核准的 11 個 environment（`env-*` semantic block）。
- §7 中核准的 5 個 formula-display 模式（KaTeX）。
- 引用手寫編號的散文 cross-reference 與 index target 標記（見 §6、§11）。
- 散文，包括依 §8 使用的 `<em>...</em>`。

### Fragment 中 MUST NOT 包含的內容

- inline `style=` 或 fragment 內的 `<style>`／`<script>`（render 由 chapter template 與 `shared/` 供給；色彩等樣式集中在 skin CSS）。
- per-section 自訂的數學巨集（section-specific operator 放在 chapter template 的 `macros: {}` block，不在 fragment 內 per-section 定義）。
- 為 JS paginator 而手動硬塞的分頁／空白（不要用 `<br>` 堆疊撐版面；分頁交給 `place()`）。
- 仰賴 auto-prefix／hyperlink 的 cross-reference（一律以散文引用手寫編號，見 §6）。
- ASCII straight quotes（`"..."`）；散文用 Unicode curly quotes（見 §8）。
- 散文中用於強調的 `<b>...</b>` 或 `<strong>...</strong>`（強調只用 `<em>`）。
- `workedexample` body 中的 page-anchored material（在 HTML kit 中不適用 LaTeX 的 `\footnote`／`\marginpar`／`\hypertarget`）。

No-custom-macro 規則的 rationale：這是多作者專案。Per-section 自訂巨集產生 notational inconsistency（同一概念在不同節以不同方式書寫）並使個別 fragment 更難 cold read。chapter template／`shared/` 中的 shared helper 已涵蓋常見情況；如果出現新情況，正確的做法是把 helper 加入 chapter template／skin（並在此記錄），而非 per-section 定義。

### Shared 元件職責

新 environment（`env-*` semantic block）、新 display 結構和新色彩定義屬於 chapter template 與 `shared/`（skin CSS／模板），不在 fragment 內逐節定義。新增共用元件時改 build／CSS 資產並在此記錄，使各 fragment 保持可 cold read。（legacy 註記：凍結的 LaTeX book 在 `legacy/tex_handout/preamble/` 中以 `\newdisplayenv{...}` 等 helper 宣告 display environment；已不適用於 HTML handout。）

### Build 與內容過閘

HTML handout 的 live 驗證路徑：

1. **Build**——`python handout/build.py` 把 fragment 組裝成 `handout/chapterN-print-standalone.html`，並驗證 KaTeX render 無誤（KaTeX 以 `throwOnError:false` 跑，malformed 表達式會 render 成紅色原始碼，即為要修的信號）。
2. **散文內容過閘**——章節由 `handout-prose-audit` subagent（gate 1）稽核易懂性，契約見 [`handout/_audit/PROSE-AUDIT-RUBRIC.md`](handout/_audit/PROSE-AUDIT-RUBRIC.md)；定稿前再經 Codex 獨立複核（gate 2）。
3. **手寫編號／引用一致性**——downstream lint 應驗證每個 "Theorem N.M" 式散文引用都對應到存在的 `env-num`（手寫編號的 authoring tax，見 §6）。

通過 build（KaTeX 無誤）並過 gate 1／gate 2 後，章節才被視為 ready for review。

（legacy 註記：凍結的 LaTeX book 曾由 `.github/workflows/latex-checks.yml` 跑 `tools/book_style_lint.py`／`book_preamble_smoketest.py`／`book_docs_lint.py` 與 `latexmk -pdf … main.tex` 四項檢查；`book_*.py` 工具已移至 `legacy/tex_handout/tools/`，原 `latex-checks.yml` 已移除、HTML handout 改由 `.github/workflows/handout-checks.yml` 建置，皆不再 gate 內容規則。）

---

## 13. Exception Protocol

個別章節偶爾需要偏離本文件中的規則。當此情況發生時，偏離 **MUST** 被記錄，不被隱藏。

### 宣告 exception

在 section fragment 頂部、`<article class="sec">` 開頭（或章 opener 的 `chapter-head` 之後）緊接著放一則 HTML 註解，格式為：

```html
<!-- Exception: Figure 3.9 forces a page break before it to avoid a near-blank page.
     Rule: Figure Placement (§10, figure stays near its prose).
     Reason: the four-panel figure is taller than the surrounding budget,
             and letting the paginator place it inline produces a near-blank page. -->
```

### 升級

如果一個 exception 跨章反覆出現（三個以上相同偏離的 instance），提出規則修訂而非累積 local exception。規則修訂透過：

1. 在修改本檔並 bump version number 的 pull request 中提出變更；
2. 與 project owner 討論變更；
3. 在 Changelog（§16）中記錄修訂。

### Silent deviation

沒有 exception comment 的 chapter 被推定遵循本文件中的每條規則。Silent deviation 是缺陷。

Rationale：規則會演進。明確的 exception record 將偏離從 noise 變成 data，使規則書能基於規則實際失敗之處進行修訂。一致性宣稱（「本書遵循自己的規則」）只有在 exception 被宣告時才可驗證。

---

## 14. 習題——獨立習題本（不在講義本體）

**2026-06-12 定案：講義本體不收習題。** 習題將以**獨立的習題本**呈現，屆時以專門的設計輪次另立規格；與課文範例共用的題源工作流程（開放題庫、provenance、授權）見 [`CONTENT_SOURCING.md`](CONTENT_SOURCING.md)。

對本 spec 的影響：

- `exercise` environment 自 §5 移除（12 → 11 個 environment）。
- 章節源檔**不需要**（也不應再有）`\subsection*{Exercises}` 區塊或 `% TODO: add \subsection*{Exercises}` placeholder。
- 手稿中的 Homework / Practice 材料不進講義，保留給習題本輪次（§5 翻譯表）。

歷史紀錄：v3.1 以前的習題規則（per-section placeholder 義務、最低習題骨架 `CONTENT_EXERCISES.md`、Ch 1 習題候選文件）可從 git 歷史取回（commit `7d6fde9` 前的樹）。

---

## 15. 最終輸出前的一致性檢查

提交章節或宣告其 ready for review 之前，驗證：

**定位與語域**
- [ ] 本章讀起來是自足的——沒有影片的學生也能完成。
- [ ] Pronoun 遵循 §3："we" 為預設；"you" 僅用於溫和提醒或 forward reference。
- [ ] 直覺段落先於 formal environment；*"Informally, ..."* gloss 在有幫助處使用。
- [ ] **散文易懂性過閘（HTML 線）**：本章已過散文稽核 gate 1（`handout-prose-audit` subagent），**易懂性 blocking = 0**；契約見 [`handout/_audit/PROSE-AUDIT-RUBRIC.md`](handout/_audit/PROSE-AUDIT-RUBRIC.md)。定稿前再經 gate 2（Codex 獨立複核）。

**結構**
- [ ] 章節以 1–2 段概述和 *"By the end of this chapter, you will be able to:"* bullet list（3–5 項）開頭。
- [ ] 每節以 1–2 段動機開頭，或純計算節以一句承接句開頭。
- [ ] 章節以 unnumbered Summary（`<section class="env">` 風格的 Summary block）結尾，包含三個必要區塊（definitions、theorems、formulas）。
- [ ] Section title 使用 Title Case；subsection title 使用 sentence case。
- [ ] 無第三層以下的編號標題（無 `subsubsection` 對應物）。

**Environment**
- [ ] 每個 `definition` 引入本章實際使用的術語。
- [ ] 每個 named theorem 使用 `env-theorem` 並在 `env-name` 放完整名稱（並標為 index target，見 §11）。
- [ ] `example` + `solution` 對包在 `workedexample` 中。
- [ ] `remark` 是 aside material，不是主線知識。
- [ ] `caution` 用於 notation trap 和容易忽略的限制條件；`strategy` 用於方法框。
- [ ] 無 `lemma`（v3.0 從 environment set 中移除）。

**公式呈現**
- [ ] 每個 display 情境使用五種核准模式中的恰好一種。
- [ ] 每個局部數學單元內維持 display block cohesion。
- [ ] 以 display math 結尾的 `solution`，其 QED box（`<span class="qed"></span>`）緊接在最後一行 display 之後。
- [ ] 方程式編號僅在被後續引用或為 formal statement 時出現。

**排版**
- [ ] 散文中無 `<b>...</b>` 或 `<strong>...</strong>`。
- [ ] `<em>...</em>` 用於新術語（每個一次），且僅在 §8 允許的 context 中。
- [ ] 散文用 Unicode curly quotes `“…”`；無 ASCII straight quotes。
- [ ] 破折號和省略號遵循 §8。

**記號**
- [ ] 符號和 macro 遵循 §9 的 canonical list。
- [ ] 保留的任何 manuscript-specific 慣例在首次使用時以 `caution` 或 `remark` 標記。

**圖表**
- [ ] 圖表密度足夠——大約每個重要 definition / theorem 一張，計算型 section 每 2–3 個 example 一張。
- [ ] Caption 為 sentence case、以句號結尾、描述數學目的。
- [ ] 色彩 palette 保持在 blue / red / gray 內（或有宣告的 exception）。
- [ ] 圖貼著介紹它的散文（由 paginator 就地排版），或有宣告的 exception。
- [ ] Worked-example 圖不洩露 example 要求讀者計算的量。
- [ ] 所有符合 §10.1 條件但尚無圖的位置已標記 `<!-- [FIGURE-OPPORTUNITY] -->` 佔位符。

**Index**
- [ ] 每個 defined term、named theorem、notation、key example、notation trap 和首次提及的 applied setting 在其首次出現處已標為 index target（見 §11；整書索引落地時據此產生）。

**Cross-reference**
- [ ] 所有 in-prose reference 以散文引用手寫編號（如 *by Theorem 4.2*、*§1.3*）；無 auto-prefix／hyperlink。
- [ ] 方程式以 `\tag{*}` render，散文中以 "(\*)" 引用。
- [ ] 每個 "Theorem N.M" 式引用都對應到存在的 `env-num`（手動維持一致）。

**Fragment 衛生**
- [ ] Fragment 中無 inline `style=`／`<style>`／`<script>`、無 per-section 自訂數學巨集。
- [ ] 無為 paginator 而手塞的分頁／空白。
- [ ] 如果偏離本文件中的任何規則，fragment 頂部有 exception comment。

**Build 與過閘**
- [ ] `python handout/build.py` 組裝 print-standalone 且 KaTeX 無 render 錯誤。
- [ ] 已過散文稽核 gate 1（`handout-prose-audit`，易懂性 blocking = 0）與 gate 2（Codex 複核）。
- [ ] **已過數學稽核（math gate），數學 blocking = 0**；契約見 [`handout/_audit/MATH-CORRECTNESS-RUBRIC.md`](handout/_audit/MATH-CORRECTNESS-RUBRIC.md)。目前由 Mode B 主審走查＋定稿前 Codex 獨立複核（`handout-math-audit` subagent 化規劃中）。

---

## 16. Changelog

- **v3.2**——習題退出講義本體（使用者 2026-06-12 定案：講義不收習題，習題以獨立習題本呈現）。`exercise` environment 自 §5 移除（12 → 11 個），手稿 Homework / Practice 標籤改歸習題本，§6 的 exercise 編號例外移除，§14 改寫為定案紀錄，§15 移除習題檢查項，各章源檔的 Exercises placeholder 與佔位句移除。文件家族中 `CONTENT_EXERCISES.md`（最低習題骨架）刪除；課文範例的題源工作流程（開放題庫、provenance、授權——2026-06-11／12 兩日定案）移至新檔 `CONTENT_SOURCING.md`。

- **v3.1**——framework split 和 implementation 落地。v3.0 文件被拆分為四個以作者實際使用方式為 key 的 author-facing 檔案：本檔（authoritative spec）、[`CONTENT_QUICKSTART.md`](CONTENT_QUICKSTART.md)（1–2 頁日常參考）、[`CONTENT_ROADMAP.md`](CONTENT_ROADMAP.md)（course arc、chapter order、prerequisite、per-chapter core skills）、以及 `CONTENT_EXERCISES.md`（完整延後設計前的最低習題骨架；v3.2 已刪除）。v3.0 下標記為 pending 的 preamble 和 template implementation 現已落地：per-env chapter-scoped counter（透過個別 `\newtheorem`）、`caution` 和 `strategy` environment（透過 `\newmdtheoremenv`）、`preamble/colors.tex` 中的 three-role semantic palette、擴展的 `tools/book_style_lint.py` 規則、以及更新的 `_chapter_template.tex`。本次 pass 中新增的 content-level 精煉：remark policy 擴展為 usefulness test 附明確的好壞範例；figure 在 §10 新增 "Redundant encoding for grayscale and accessibility" subsection，要求 line-style / label / marker 與色彩並行；index policy 在 §11 新增覆蓋性的 "lookup test" 判斷準則。§5 中的 `example` + `solution` pairing rule 現在在本文件和 `chapters/_chapter_template.tex` 之間已對齊（每個 `example` MUST 包在 `workedexample` 中；standalone `example` 不再允許）。Exercise 編號現為 per-section（Exercise 1, 2, ...，每 `\section` reset）而非 chapter-scoped，反映 end-of-section exercise block 是 locally consume 的。

- **v3.0**——從零重寫。目標語域從 Spivak / Apostol（shared formal-statement counter、austere pronoun、strict definition purity、sparse figure 和 remark）轉為 Stewart / Rogawski（per-type counter、特定 context 中允許 "you"、`definition` 中允許 *"Informally, ..."* gloss、denser figure 和更大方的 remark）。新增 `caution` 和 `strategy` environment 以支持 notation-trap warning 和解題策略框；`lemma` 移除。Display-helper set 從 7 減為 5（移除 `\iffstackeddisplay` 和 `\iffwithconditions`）。Display Block Cohesion 從 MUST 降為 SHOULD。Index policy 擴展以涵蓋 key example、notation trap 和首次提及的 applied setting。Chapter opening 新增 mandatory learning-outcomes bullet list；chapter closing 新增 mandatory `\section*{Summary}` block。動機散文中允許 `\emph{...}` 用於術語首次出現。Exercise-system design 延後至主要內容完成。CI 檢查擴展以涵蓋新規則。Notation policy 整合為獨立的 section（§9）。語聲參考範文以 Stewart tone 重寫。

  （v3.0 是 positioning-level rewrite；其標記為 pending 的具體 preamble 和 template implementation 已落地——見上方 v3.1。）

- **v2.x**——早期版本（v2.0 到 v2.0.11）透過 per-chapter review 累積規則新增；所得文件以新增日期而非主題組織。v2.x 中原封保留至 v3.0 的重要決策包括：cleveref-only cross-reference、`[H]` 預設 figure placement 附 Exception Protocol、shared formula-display helper `aligneddisplay` / `conditiondisplay` / `\pairdisplay`、chapter-scoped counter、paired-definition cross-reference rule、`workedexample` wrapper semantics、`solution` 最後 display 行的 `\qedhere`、以及 three-layer CI（style lint + preamble smoketest + latexmk）。

- **v1.0**——初始版本。
