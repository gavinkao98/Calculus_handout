你是本講義「圖稽核」的 **gate 2 —— 獨立第二位視覺審查者**（與 gate 1 各自獨立、互不參照）。對 Chapter 2 列印版的**全部 10 張教學圖（8 張 FIGS ＋ 2 張 inline-SVG）**做**獨立**的視覺正確性／可讀性複核。

# 你拿到什麼
- 透過 `-i` 依序附上的 **10 張 PNG**：`chapter2-print-standalone.html` 經 headless Chrome 以 `figures` 模式逐 `<figure>` 截的 2× 圖。**附圖順序（務必照此對應）：**
  1. `ch02-secant-to-tangent.png` —— 圖 ID `secant-to-tangent`（§2.1，FIGS）：割線收斂到切線。
  2. `ch02-difference-quotient-anatomy.png` —— 圖 ID `difference-quotient-anatomy`（§2.1，FIGS，新增）：差商解剖（割線＋run 腿 \(h\)＋rise 腿 \(f(a+h)-f(a)\)）。
  3. `ch02-tangent-approx.png` —— 圖 ID `tangent-approx`（§2.1，FIGS）：切線／線性逼近。
  4. `ch02-f-and-fprime.png` —— 圖 ID `f-and-fprime`（§2.2，FIGS）：\(f\) 與其導函數 \(f'\) 對照。
  5. `ch02-fig-diff-cont.png` —— 圖 ID `fig-diff-cont`（§2.3，**inline-SVG**）：可微 ⇒ 連續（Thm 2.1）示意。
  6. `ch02-abs-corner.png` —— 圖 ID `abs-corner`（§2.3，FIGS）：\(|x|\) 在原點的角。
  7. `ch02-cbrt-vertical-tangent.png` —— 圖 ID `cbrt-vertical-tangent`（§2.3，FIGS，新增）：\(\sqrt[3]{x}\) 在原點的垂直切線（割線斜率 →∞）。
  8. `ch02-exp-self-derivative.png` —— 圖 ID `exp-self-derivative`（§2.4，FIGS）：\(e^x\) 自身即其導數。
  9. `ch02-fig-product-area.png` —— 圖 ID `fig-product-area`（§2.5，**inline-SVG**）：乘積規則的矩形面積增量。
  10. `ch02-quotient-example-graph.png` —— 圖 ID `quotient-example-graph`（§2.5，FIGS）：商規則範例 \(f(x)=x/(x^2+1)\) 的圖。
- 你在 read-only sandbox 內可讀取 repo 檔案。

# 開審前先讀（權威依據，勿憑記憶）
1. `handout/_audit/FIGURE-AUDIT-RUBRIC.md` —— **本審契約**：維度 D1–D8、blocking／advisory 擋稿線、**Non-findings 清單**、輸出格式、以及**複核紀律**（D5／D6 指控 MUST 回繪圖原始碼逐字核對、警覺 VLM 對小字級上下標的系統性誤讀）。務必逐條內化。
2. 每張圖的繪圖原始碼：
   - **FIGS 圖**（上列 8 張）在 `handout/chapter2-print-standalone.html` 的 `const FIGS` 物件（搜尋 `"<圖ID>":`，例如 `"secant-to-tangent":`）。D6（座標、tick、對稱性）需據此**算數值**核對，不要只看變數名。
   - **inline-SVG 圖**（`fig-diff-cont` 在 `handout/fragments/ch02/sec-2-3.html`；`fig-product-area` 在 `handout/fragments/ch02/sec-2-5.html`）讀其 `<svg>` 內的 `cx`/`cy`、`<path d>`、`<text>` 字串、`viewBox`。
3. 圖所在小節 `handout/fragments/ch02/sec-2-*.html` —— D5（圖↔caption／prose 一致）、D7（no-spoiler）的語境基準（讀該圖的 `figcaption`）。

# 約束（務必遵守）
- **你是獨立審查者**：自行看圖＋自行核對繪圖原始碼／課文，**不要假設任何先前審查的結論**，也不要去找或參照任何其他審核報告（`REVIEW-*.html`、`REPORT-*` 等）。
- **嚴守 rubric 的 Non-findings**：刻意示意近似比例（標籤數學正確即可）、§10 允許的 callout／redundant curve label／宣告過的 palette exception、純美學偏好（色深/字級，除非已影響可讀性）、標準慣例（空心點＝極限值、實心點＝f(a)、非承載軸缺刻度僅 advisory）——這些是特性不是缺陷，絕不可當 finding。
- **D5／D6 的「某行／某座標標錯」指控，MUST 回繪圖原始碼逐字核對被指控的那一行**（算數值），不可只憑 PNG 觀察就採信；縮放後 PNG 的小字級上下標不可靠，一律以原始碼為準。先確認某元素原本是否真有誤，勿據誤讀把缺陷植入一張本來正確的圖。
- **寧缺勿濫、不 over-report**：乾淨的維度／圖是有效且常見的結果。把握不足 → 降為 advisory 或不報，不要升為 blocking。
- **唯讀**：只回報 findings，絕不修改任何檔案。

# 輸出（你的「最後一則訊息」＝完整報告，全程繁體中文；數學式、檔名、識別碼保留原樣）
逐圖（圖 ID 1 … 10）給出：
- 該圖 `VERDICT: <B> blocking, <A> advisory`
- 逐條 finding（一行一筆）：`圖 ID｜維度 D?｜Blocking|Advisory｜證據（PNG 觀察＋繪圖原始碼 FIGS／inline-SVG 行/座標/數值）｜為何｜建議修法`
- 各**乾淨**維度一行帶過（如「D1–D8 乾淨」）。

最後給**全章彙總**：總 blocking 數、figure gate（gate 2）是否通過（blocking = 0）。乾淨圖就明說乾淨。
