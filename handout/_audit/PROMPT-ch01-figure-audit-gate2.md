你是本講義「圖稽核」的 **gate 2 —— 獨立第二位視覺審查者**（與 gate 1 各自獨立、互不參照）。對 Chapter 1 列印版的**全部 21 張教學圖（20 張 FIGS ＋ 1 張 inline-SVG）**做**獨立**的視覺正確性／可讀性複核。

# 你拿到什麼
- 透過 `-i` 附上的 **19 張 PNG**：`chapter1-print-standalone.html` 經 headless Chrome 截的 A4 列印頁（2×）。每頁含 1–2 張圖與其周圍正文。檔名 `ch01-pNN.png` 的 `NN` 即頁碼。
- 你在 read-only sandbox 內可讀取 repo 檔案。

# 開審前先讀（權威依據，勿憑記憶）
1. `handout/_audit/FIGURE-AUDIT-RUBRIC.md` —— **本審契約**：維度 D1–D8、blocking／advisory 擋稿線、**Non-findings 清單**、輸出格式。務必逐條內化其 Non-findings 與「不 over-report」原則。
2. 每張圖的繪圖原始碼：**FIGS 圖**在 `handout/chapter1-print-standalone.html` 的 `const FIGS` 物件（搜尋 `"<figid>":`）；**inline-SVG 圖**（無 `data-fig`，如 Fig 1.2 `fig-map`）在 `handout/fragments/ch01/sec-1-1.html` 的 `<svg>` 內（讀 `cx`/`cy`、`<path d>`、`<text>` 字串）。D6（座標、tick、對稱性）需據此**算數值**核對，不要只看變數名。
3. 圖所在小節在 `handout/fragments/ch01/sec-1-*.html` —— D5（圖↔caption／prose 一致）、D7（no-spoiler）的語境基準。

# 圖 → 頁 對照（共 21 圖；標「新」者為近期新增；標「inline」者為 inline-SVG、原始碼在 fragment）
- Fig 1.1  `hlt` → p03
- Fig 1.2  `fig-map`（inline）→ p04–05（介於 1.1 與 1.3，render 後依實際頁碼填）
- Fig 1.3  `restrict-x2` → p06
- Fig 1.4  `sine-not-1to1` → p08
- Fig 1.5  `restricted-sine` → p09
- Fig 1.6  `arcsin-triangle` → p11
- Fig 1.7  `restricted-cosine` → p11（與 1.6 同頁）
- Fig 1.8  `restricted-tangent` → p13
- Fig 1.9  `arctan10-triangle` → p14（新）
- Fig 1.10 `arctan-general-triangle` → p15（新）
- Fig 1.11 `limit-same-near-a` → p17
- Fig 1.12 `read-limit-graph` → p18
- Fig 1.13 `one-sided-limits` → p21
- Fig 1.14 `piecewise-jump` → p22（新）
- Fig 1.15 `one-sided-infinite` → p24
- Fig 1.16 `vertical-asymptote` → p26
- Fig 1.17 `ln-asymptote` → p27（新）
- Fig 1.18 `floor-function` → p32（新）
- Fig 1.19 `squeeze-theorem` → p33（新）
- Fig 1.20 `squeeze-x2sin` → p34（新）
- Fig 1.21 `precise-limit` → p37

# 約束（務必遵守）
- **你是獨立審查者**：自行看圖＋自行核對繪圖原始碼（FIGS 圖讀 `const FIGS`、inline-SVG 圖讀 fragment `<svg>`）／課文，**不要假設任何先前審查的結論**，也不要去找或參照任何其他審核報告（`REVIEW-*.html`、`REPORT-*` 等）。
- **嚴守 rubric 的 Non-findings**：刻意示意近似比例的直角三角形（標籤數學正確即可，如 arcsin／arctan triangle）、§10 允許的 callout／redundant curve label／宣告過的 palette exception、純美學偏好（色深/字級，除非已影響可讀性）、標準慣例（如 ε-δ 圖空心點＝極限值、實心點＝f(a)、非承載軸缺刻度僅 advisory）——這些是特性不是缺陷，絕不可當 finding。
- **寧缺勿濫、不 over-report**：乾淨的維度／圖是有效且常見的結果。把握不足 → 降為 advisory 或不報，不要升為 blocking。
- **唯讀**：只回報 findings，絕不修改任何檔案。

# 輸出（你的「最後一則訊息」＝完整報告，全程繁體中文；數學式、檔名、識別碼保留原樣）
逐圖（Fig 1.1 … Fig 1.21）給出：
- 該圖 `VERDICT: <B> blocking, <A> advisory`
- 逐條 finding（一行一筆）：`圖 ID｜Figure #｜維度 D?｜Blocking|Advisory｜證據（PNG 觀察＋繪圖原始碼 FIGS／inline-SVG 行/座標/數值）｜為何｜建議修法`
- 各**乾淨**維度一行帶過（如「D1–D8 乾淨」或逐條）。

最後給**全章彙總**：總 blocking 數、figure gate（gate 2）是否通過（blocking = 0）。乾淨圖就明說乾淨。
