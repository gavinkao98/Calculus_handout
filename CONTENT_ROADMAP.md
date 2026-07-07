# 內容路線圖

本檔案承載講義的**課程弧線**：有哪些章節、順序為何、每章負責什麼、以及概念如何跨章串聯。它是 [`CONTENT_SPEC.md`](CONTENT_SPEC.md)（規範*如何*寫）和 [`CONTENT_QUICKSTART.md`](CONTENT_QUICKSTART.md)（日常作者規則）的課程面伴侶。

開始寫新章節時，先更新下方的 entry，**然後**才動筆。當你結束一章時，標記為 done 並回頭檢視下游章節的 prereq 敘述。

本書由**不同教師撰寫的手稿**組裝而成。每章 entry 在 **Manuscript source** 欄位記錄其手稿來源，使草稿的起源與轉換狀態一目了然。手稿轉 HTML 片段的工作流程以及規範 Claude 擴展手稿的 anti-hallucination 規則都在 [`README.md`](README.md) §*Authoring workflow* 中；本檔案是各章手稿追蹤的落點。

---

## 受眾與定位

重複自 [`CONTENT_SPEC.md`](CONTENT_SPEC.md) §1，讓任何一章的作者能快速校準：

- 有志自修大學微積分的高中生。
- 具備紮實的 precalculus 基礎；有一些數學推理經驗；尚未達到大學數學主修的程度。
- 將講義視為主要學習管道。**講義是自足的**；影片是強化而非前提。

兩個跨章的目標凌駕於任何章節特定的內容之上：

- **self-sufficiency**——從未看過影片的學生仍然能從講義中學到東西。
- **lookup-friendliness**——在第五章忘了某個 definition 的學生可以透過 index、章節開頭或 summary 找回來。

---

## 章節列表

> **狀態圖例**：`draft` = 正在撰寫中。`skeleton` = 結構已規劃但內容未草擬。`planned` = 在路線圖上，尚未開始。`done` = 通過 §15 一致性檢查清單。

| # | 標題 | 狀態 | 各節 |
|---|---|---|---|
| 1 | Inverse Functions and Limits | draft | 1.1 Inverse Functions and One-to-One Functions; 1.2 Inverse Trigonometric Functions; 1.3 Limits; 1.4 One-Sided and Infinite Limits; 1.5 Limit Laws; 1.6 The Precise Definition of a Limit |
| 2 | Derivatives | draft | 2.1 The Tangent Line and the Derivative at a Point; 2.2 The Derivative as a Function; 2.3 Differentiability, Continuity, and Higher Derivatives; 2.4 Derivatives of Polynomials and the Exponential Function; 2.5 The Product and Quotient Rules |
| 3 | Chain Rule and Trigonometric Derivatives | draft | 3.1 Derivatives of the Sine and Cosine Functions; 3.2 The Chain Rule; 3.3 Applications of the Chain Rule |
| 4 | The Exponential and Logarithmic Functions | draft | 4.1 Construction of the Exponential Function; 4.2 Continuity and the Exponent Law for $e^x$; 4.3 The Derivative of $e^x$; 4.4 Rolle's Theorem and the Mean Value Theorem; 4.5 Monotonicity and the Logarithmic Function |
| 5 | Applications of Differentiation | draft | 5.1 Implicit Differentiation; 5.2 Related Rates; 5.3 Linear Approximation and Differentials; 5.4 Maximum and Minimum Values; 5.5 Optimization Problems; 5.6 Derivatives and the Shape of a Graph; 5.7 L'Hôpital's Rule; 5.8 Curve Sketching; 5.9 Newton's Method |
| 6 | Integrals | planned | *脊椎；深度：深理論核心（FTC 當場證）* |
| 7 | Applications of Integration | planned | *脊椎；深度：標準（含 further applications，選材節制）* |
| 8 | Techniques of Integration | planned | *脊椎；深度：標準/計算* |
| 9 | Differential Equations | planned | *脊椎；first-order intro（章名框住範圍）；深度：標準* |
| 10 | Parametric Equations and Polar Coordinates | planned | *脊椎；含 conics（銜接 A.5）；深度：標準* |
| 11 | Infinite Sequences and Series | planned | *脊椎；**建議拆 11a/11b**；深度：深理論核心* |
| 12 | Vectors and the Geometry of Space | planned | *脊椎；深度：標準* |
| 13 | Vector Functions | planned | *脊椎；深度：標準* |
| 14 | Partial Derivatives | planned | *脊椎；**可能需拆（sleeper）**；深度：深理論核心（多變數可微性）* |
| 15 | Multiple Integrals | planned | *脊椎；深度：標準設定＋變數變換/Jacobian 最重 fence* |
| 16 | Vector Calculus | planned | *脊椎；**建議拆 16a/16b**；深度：嚴謹陳述＋一般定理 fence* |

目標範圍：Calc I + II + III（單變數到多變數向量微積分），對標 **NTU 微積分甲**（理工嚴謹軌；其甲上章節即 Stewart Ch1–10）。**2026-07-04 使用者裁定章脊椎**（研究 Stewart ET 9e／Thomas 14e／Rogawski 4e／NTU 微積分甲＋Codex 覆核，見 [`handout/_audit/REVIEW-chapter-arc-proposal.html`](handout/_audit/REVIEW-chapter-arc-proposal.html)）：**16 主題脊椎**，其中 **Ch11 與 Ch16 各拆 2 章 → 實務約 18 章**（Ch14 待觀察）。本書切得比 Stewart 細（Ch1–4 已用 4 章走完 Stewart 約 2.5 章）＋深度向分析靠攏，故章數多於參考弧線的 14。分組（本書實際弧線，非參考弧線）：

- **Calc I**（Ch 1–6）：反函數與極限 → 導數 → 鏈式法則與三角導數 → 指對數（含 MVT）→ 微分應用 → 積分。（**Early Transcendentals**：指對數已於 Ch4 早鋪並以級數嚴格構造，中段不再設 transcendentals 章。）
- **Calc II**（Ch 7–11）：積分應用 → 積分技巧 → 微分方程（first-order intro）→ 參數式與極座標 → 無窮級數（11a/11b）。
- **Calc III**（Ch 12–16）：向量與空間幾何 → 向量函數 → 偏導數 → 重積分 → 向量微積分（16a/16b）。

**章脊椎與深度基調已於 2026-07-04 定案**（使用者裁決）：上表 Ch5–16 的標題、role、對應標準、深度基調固定（骨架見下方「Ch5–16 弧線骨架」）。但**節層細節仍不承諾**：各章的完整 entry（core skills、key figures、notation、cautions、open questions，以及確切各節與 Ch11/Ch16 拆章的最終編號）仍在該章的直接前驅到達 `draft` 狀態時才填——因為前驅章節的上游決策會影響後繼章節的節層安排。原則＝**「脊椎＋深度基調現在鎖、節層跟章走」**。**〔2026-07-06 精修——Ch5–16 已無老師手稿〕** 純 JIT 的「等手稿逐份到、上游 cascade」理由消失（canon 現在就定範圍）→ 升級為 **「脊椎＋全局 seam ledger 現在鎖、完整節層 brief 跟章走」**：現在全局鎖 provisional 節 roster＋**跨章 export/import 定理號契約**＋記號串接＋fence/hook 觸發（除定理號與跨章依賴外全 provisional）；完整節層 brief／worked example／圖／證明長度／最終編號仍跟章 JIT。詳見下方「全局 seam ledger」。（「脊椎＋深度基調現在鎖」段取代原「Ch3 以後標題不承諾」政策——該政策防的是節層細節，非章脊椎；脊椎現已在主題收斂＋NTU 對標＋Ch1–4 深度確立下安全定案。）

**Appendix A — Precalculus Toolbox（2026-07-03 立項，status: draft）**：`CONTENT_SPEC.md` §16.2 的 B 類先備中「值得完整鋪開」者的家（使用者 2026-07-03 裁示立項）。**收錄**：A.1 The Reciprocal Trigonometric Functions（Definition A.1、Proposition A.1、Example A.1）；A.2 The Product-to-Sum and Sum-to-Product Identities（Proposition A.2/A.3、Strategy A.1、Example A.2）；A.3 The Infinite Geometric Series（Proposition A.4/A.5、Example A.3）。**機制**：獨立編號 namespace「A」（per-type counter 跨三節連續）、`handout/fragments/appA/`、`build.py` registry `appA` → `appendixA-print-standalone.html`（shell 複製自 ch01，title/brand/runningHead 已改；FIGS registry 沿用 ch01 副本、惰性未用）。**被引用**：§1.2（倒數三角 bridge）、§3.1（和差化積 bridge）、§4.1（無窮等比 bridge）——三處主線 bridge 均保留並 cross-ref 附錄（spec §16.2 處置慣例）。**刻意偏離章規格**：無 chapter summary（工具箱非敘事章）；批次一（A.1–A.3）無圖（§A.5 於第二批補 4 張圓錐曲線圖，見下）。**閘計畫**（support 材料、縮閘）：prose audit gate-1＋Codex 數學/語域 gate-2＋難度閘 sim＋render 自驗；六閘全套不適用。**Open questions**：(i) 要不要為 A.1 補倒數函數圖形（與 §1.2 arccsc/arcsec 分支無圖的 figure-opportunity 候選同批裁決）；(ii) 未來章節出現新的 B 類「值得鋪開」項時擴充。
**2026-07-04 第二批（使用者裁決 roster）— 已撰寫並過縮閘**（as-built 與 gate 結果見 [`handout/_audit/REVIEW-appendixA-applied.html`](handout/_audit/REVIEW-appendixA-applied.html) 七～十節）：§A.2 內擴充降冪（不編號）；**Σ 記號/index 操作經使用者裁決併入 §A.3**（retitle「Sigma Notation and the Geometric Series」，非獨立節——避「§A.3 已用 Σ_∞、下一節才介紹」的順序倒錯＋重編號）；新增 **§A.4 部分分式**（Prop A.6 三型＋Strategy A.2＋Ex A.4/A.5，並補進 SPEC §16.2 B 類）、**§A.5 圓錐曲線**（標準式＋Ex A.6＋Figure A.1–A.4；FIGS 進 standalone、過圖正確性閘；analytic geometry，**不列** B 類）；**絕對值不等式使用者未選＝未寫**。**節連號 §A.1–§A.5**（Σ 併入故無 §A.4 空缺）。三閘（prose/sim/Codex）＋圖正確性閘＋render/linebreak-gate 全綠，blocking（§A.4 opener 過時）皆已修並回歸。**Appendix B — Reading Theorems and Proofs（2026-07-04 撰寫並過縮閘，status: draft）**：`CONTENT_SPEC.md` §16.2 B 類先備「量詞操作與以反證法為主的證明寫作」的完整鋪開——一份**自足的「怎麼讀證明」primer**（後設閱讀指南，非新定理章）。**使用者 2026-07-04 裁決**：獨立 build 單元 appB、namespace B（編號從 B.1 起）；**自足、用通用經典例子**（整數／質數／√2／鴿籠／通用 ε 估計），**不錨 Ch1–4**（比照對 Appendix A 做的去章節連結；內部 §B.x 互引保留）。**收錄（5 節）**：B.1 Reading a Statement（Definition B.1 converse/contrapositive＋Strategy B.1＋Example B.1）／B.2 The Main Proof Shapes（Strategy B.2＋Prop B.1–B.4＋Example B.2：直證／反證(√2)／反例否證／分案／歸納）／B.3 A Quantifier Toolbox（∀∃順序＋Strategy B.3 否定＋Example B.3＋∀ε∃δ 挑戰–回應）／B.4 Steps That Come From Nowhere（Strategy B.4：add-subtract／3ε／min／輔助函數／WLOG＋Example B.4/B.5）／B.5 Reading Actively（Strategy B.5 五習慣＋Prop B.5 鴿籠＋Caution ⇒≠⇔）。**機制**：shell 複製自 `appendixA-print-standalone.html`（改 title/brand/runningHead/CHAPTER.fragments）、`build.py` registry 加 `appB` → `appendixB-print-standalone.html`；無圖（沿用 appA FIGS 惰性未用）。**刻意偏離章規格**：無 chapter summary（primer 非敘事章）、formal Definition 用得少（僅 B.1）。**縮閘全綠**（as-built 與 gate 結果見 [`handout/_audit/REVIEW-appendixB-applied.html`](handout/_audit/REVIEW-appendixB-applied.html)）：prose gate-1（5 節全 0 blocking）＋難度 learner-sim ×3（全 0 stuck、0 B 類違規、自足通過）＋Codex 邏輯/證明正確性 gate-2（1 blocking＋4 advisory，MATH/CROSS-REF/REGISTER 全 CHECKED-CLEAN）＋`build.py appB`／`linebreak-gate`／render 自驗；共 **9 筆修**（1 blocking＝Example B.5 δ 正性＋8 收斂/教學缺口 advisory，全句子級澄清補述、不動數學/結構/編號、不增刪招式）皆已修並 **scoped 盲測回歸 PASS**。撰寫階段另修一 MathJax v4 `\text{}` 邊界吞空格排版缺陷（3 處句子型顯示式改 HTML inline-math）。**未 commit**（沿用「先不 commit」，與 Appendix A 那批一同留工作樹 `video/template-redesign-navy-spine`）。**紀律（使用者 2026-07-04 兩度強調）：附錄收錄條目一律先與使用者討論裁決，不得自行決定。**（本次 B.1–B.5 結構與「自足/通用例子」為使用者裁定範圍內，未增刪招式。） **2026-07-04 外部 review（~8.5/10）處置**（見 REVIEW HTML 第八節）：修 2 精確度缺陷（B.1 量詞/前提措辭、B.2 反證「assume the claim is false」）；經 AskUserQuestion 採納 3 增補——proof by contraposition 輕量標註（Prop B.1＋Strategy B.2 選單，roster 仍 5 形狀）、B.3 量詞否定 warm-up（單→雙→三重）、B.5「Pause」自試框；3 項與既定決策衝突不採納（加習題↔§14、list 左對齊↔全域 shell、清 FIGS↔brief「B 不必碰 FIGS」）；英文語域經裁「維持現狀」。三增補過 Codex(0/0)＋難度 sim(PASS)＋prose(0 blocking) 閘。

**全 arc 先備掃描（2026-07-04，唯讀）**：[`handout/_audit/REVIEW-appendix-fullarc-prereq-sweep.html`](handout/_audit/REVIEW-appendix-fullarc-prereq-sweep.html)（＋缺口分析 [`REVIEW-appendix-gap-analysis.html`](handout/_audit/REVIEW-appendix-gap-analysis.html)）——掃 Ch5–16 先備，淨新附錄候選 roster：**GAP-A** 冪次和 \(\sum k^2,\sum k^3\)→ Ch6 黎曼和／擴充 §A.3；**GAP-B** 複數 primer → Ch9/Ch11；**GAP-C** 行列式 2×2/3×3 → Ch12/15/16；**GAP-D** 補證處/Proof-track → Ch14 起（首個 on-credit fence 出現時立）；**GAP-E** 絕對值不等式（收斂半徑承重）→ Ch11 重估；**GAP-F** 完全平方 → Ch8／併 A.4/A.5。另建議 §16.2 補 3 分類（複數/行列式/冪次和，Codex 覆核建議均為 B）。**均待使用者逐項裁決**（附錄收錄紀律，2026-07-04 使用者兩度強調）；下方各章骨架已就地標註掛鉤。

**全 arc 附錄 clean-slate 重設計（2026-07-04，使用者裁定；設計＋Codex 獨立覆核見 [`handout/_audit/REVIEW-appendix-clean-slate-design.html`](handout/_audit/REVIEW-appendix-clean-slate-design.html)）**：不被現有附錄綁住、從 16 章全 arc 按「附錄功能」重推，結論＝現有 A.1–A.5／B.1–B.5 **全 validated**（無廢料/放錯），理想體系＝4 功能：**A precalc 工具箱**（現 5 節＋收尾 roster）／**B 讀證明**（現 5 節）／**線性代數**（新，見下）／**補證處 Proof-track**（新，見下）。跳過：函數圖形 review（A 類＋主線）、反函數/反三角（**刻意主線** §1.1/§1.2）、完整積分表（教學型非參考型）。實數完備性/分析基礎經裁**不設獨立附錄**（承重留 Ch4 主線、fence 的收補證處）。**Appendix A 收尾 roster 執行中**：GAP-A 冪次和（**建置中**，擴 §A.3）→ 完全平方 → 絕對值不等式（＋複數條件）。

**Appendix C — Linear Algebra for Calculus（2026-07-04 撰寫並過縮閘，status: draft）**：Calc III 的線性代數工具箱——§16.2 B 類「行列式」＋承重的向量/方向工具的完整鋪開（Codex 獨立設計補抓 Hessian/orientation）。**as-built（4 節；namespace「C」；build unit `appC` → `appendixC-print-standalone.html`，shell 複製自 appB、title/brand/runningHead 已改、無殘留 appB 身份）**：§C.1 Matrices and Determinants（Def C.1 2×2/3×3 餘因子＋Ex C.1＝算 3×3=6）／§C.2 The Determinant as Signed Area and Volume（Prop C.1＋Ex C.2＝三角形面積 11/2）／§C.3 Orientation and the Cross Product（Def C.2 叉積=行列式、Prop C.2 |a×b|=面積・三重積=有向體積＋Ex C.3）／§C.4 Quadratic Forms and Definiteness（Def C.3、Prop C.3 \(D=ac-b^2\) 判別＋配方證明＋Ex C.4）。**設計精修（撰寫時定，使用者已知會）**：收斂為**純線性代數先備**——Jacobian 矩陣與 Hessian 這兩個「由偏導 built 的微積分物件」**移出附錄、留 Ch14/Ch15**（附錄只給它們用的線代事實＋forward-motivation），避免「先備附錄要求先懂偏導」的循環。**被引用（規劃）**：Ch12（叉積/法向量）、Ch14（Hessian 判別借 §C.4）、Ch15（Jacobian 行列式借 §C.2）、Ch16（旋度行列式）。**刻意偏離章規格**：無 chapter summary（工具箱）；無圖（signed-area 平行四邊形／右手定則／parallelepiped 為 figure-opportunity 候選，deferred，比照 appA 批一）。**縮閘全綠**：quote-lint clean（4 檔）＋`build.py appC`＋MathJax render（95→106 容器、0 error、0 欄寬溢出，3×3 行列式/矩陣最寬亦不溢）＋Codex gate-2（gpt-5.5/xhigh）**1 blocking＋1 advisory 皆修並回歸**（blocking＝Prop C.3 證明漏 \(a=0\wedge D<0\) 情形→補該 case；advisory＝Prop C.2「右手定則」限定非零非平行 \(\mathbf a,\mathbf b\)）。**未 commit**（沿用附錄批次「先不 commit」，同留工作樹 `video/template-redesign-navy-spine`）。

**Appendix D — Deferred Proofs / The Proof Track（2026-07-04 立項；appD as-built 2026-07-06，status: draft）**：§16.1 深度政策 (B) 的必然配套——主文 on-credit fence 掉的重證明的家（clean-slate 判為結構級必需）。**收錄（隨各章 fence 陸續填）**：Ch6 連續⇒可積（Riemann/Darboux 可積性）、Ch11 重排定理/一致收斂、Ch14 Clairaut 混合偏導對稱、Ch15 一般變數變換/Jacobian 定理、Ch16 一般 Green/Stokes/散度定理（Ch9 若用唯一性語言則 Picard–Lindelöf）。**另含定理假設表**（每定理吃哪些假設：continuity／\(C^1\)／simple region／orientation——與「不假證」定位相配）＋補證處使用說明（陳述/依賴/簡單情形/一般證明邊界/章節用途）。**不收**：Ch4 e^x 級數構造、MVT、FTC、級數主定理、多變數可微性基本理論（＝指定核心章的當場嚴格內容）。**觸發**：第一個 fence 隨 Ch6 到來時開建；現先立項讓 Ch6+ 的 fence 有指向。 **〔2026-07-06 提前啟用〕** 全書 seam pass 撈出 Ch4 已有兩個未 discharge 的存在定理 fence——**EVT（Thm 4.9）陳述未證**、且 **IVT 從未陳述卻在 §4.5 默借**（撐 $e^x$ 值域 $(0,\infty)$／ln 定義）。使用者 2026-07-06 裁決：IVT＋EVT 一併陳述於 **Ch4 §4.4**，兩證 fence 至本附錄為**首批收錄**（皆由完備性 Thm 4.1 可證）→ 本附錄首建觸發點由 Ch6 提前到 IVT/EVT 補寫。**已建（2026-07-06）**：build unit `appD` → `appendixD-print-standalone.html`，§D.1 Using the Proof Track（how-to＋「Fenced so far」定理假設 summary）＋§D.2 The Existence Theorems（**Lemma D.1** LUB from Thm 4.1＋EVT proof＋IVT proof），閘全綠。後續 fence（Ch6 連續⇒可積…）隨各章加入。裁決稿 [`handout/_audit/REVIEW-fullarc-seam-skeleton.html`](handout/_audit/REVIEW-fullarc-seam-skeleton.html)。

---

## 每章 entry 範本

開始新章節時，將此區塊複製到章節列表區域。

```
### Chapter N: Title

**Status**: draft | skeleton | planned | done
**Source file**: handout/fragments/chNN/sec-*.html（每節一個片段）
**Estimated length**: N pages printed（以 handout/build.py 產出的列印 standalone 為準）
**Manuscript source**: <teacher name | "pre-manuscript working hypothesis" | "pre-existing LaTeX — entry reverse-engineered">
 — <pending | received YYYY-MM-DD | converted YYYY-MM-DD>. <optional note on coverage, gaps, or register hints from the teacher>.

**Role in the arc**
- 一段說明本章對讀者的作用。
- 為什麼它在位置 N 而不是更前或更後。

**Prerequisites**
- 本章依賴的章節（按節列出）。
- 讀者預期帶來的 precalculus 知識。
- 先前引入的、本章會重用的記號或 environment。

**Core skills**
每項 MUST 對應章節開頭 "By the end of this chapter, you will be able to:" 列表中的一個子彈。
- skill 1
- skill 2
- skill 3-5

**Key figures**
- 每個節開頭動機依賴的圖（各一個子彈）。

**Handout self-sufficiency vs. video reinforcement**
- 講義獨立教授的內容。
- 影片在此基礎上增加的內容（直覺視覺化、替代的 worked example、節奏）。
  影片永遠不會承載講義中未陳述的事實。

**Strategy boxes expected**
- 題型 → strategy 名稱。例："computing a limit → §1.5 Limit-computation strategy."

**Notation introduced**
- 新符號、macro 或記號慣例。每一個在首次使用時都以清楚散文標記以利查找（lookup-friendliness）；HTML 講義無自動索引，交叉引用為手寫散文。

**Common pitfalls (caution boxes)**
- 記號陷阱。
- Branch-choice 或 domain-restriction pitfall。
- 只在 subdomain 上成立的恆等式。

**Open questions**
- 尚未做出的決策。在宣告該章 `done` 之前關閉。
```

---

## Chapter 1（已填範例）

### Chapter 1: Inverse Functions and Limits

**Status**: Mode C 充實中 — 散文雙閘已過（gate-1 Claude＋gate-2 Codex，0 blocking）；**主軸於 2026-06-15 凍結，作為 Mode C 起點**（Mode C 只增添、不動主軸；新增擴充以 `[pass: enrichment]` 標記，完成後跑範圍限定於新標記的 Mode B）。
**Source file**: [`handout/fragments/ch01/`](handout/fragments/ch01/)（`sec-*.html`）——slug `foundations` 是弧線層級的標籤（Chapter 1 是弧線的 *foundations* 階段），不是印刷的章節標題的一部分。（原 LaTeX 稿現置於 [`legacy/tex_handout/chapters/ch01_foundations.tex`](legacy/tex_handout/chapters/ch01_foundations.tex)。）
**Estimated length**: *（完成首次完整編譯後填入）*
**Manuscript source**: pre-existing LaTeX——entry 從已提交的 LaTeX 稿反推而來。現以 HTML 片段為準；本 entry 是對現有內容的描述，不是未來草擬的計畫。當 Chapter 1 進行進一步編輯時，同時更新 HTML 片段和本 entry。

**Role in the arc**
Chapter 1 是課程弧線的 **foundations** 階段。它建立微積分的兩部基礎機器：inverse function（將規則「反向運行」的代數機器）和 limit（「逼近但不等於」的分析機器）。本章刻意將兩者配對，因為兩者都迫使讀者從對應關係和近似的角度思考，而非僅盯著公式。

**Prerequisites**
- Precalculus 函數：domain、range、composition、graphs。
- 三角函數及其在標準區間上的圖形。
- 基本代數運算（factoring、rationalising、completing the square）。

**Core skills**（對應章節開頭的 bullet list）
- 判定一個函數是否 one-to-one，如果是則求出其 inverse；
- 使用 inverse trigonometric function，包括它們的 principal-interval restriction 和由此產生的 identity；
- 用 substitution、factoring、rationalising 和 one-sided analysis 計算 Ch. 1 和 Ch. 2 中遇到的各類 limit；
- 判定一個 limit 何時不存在；
- 使用 $\varepsilon$–$\delta$ definition 陳述並（在需要時）驗證一個 limit。

**Key figures**
- inverse-composition diagram（§1.1）。
- 可逆函數圖形沿 $y = x$ 的反射（§1.1）。
- 帶有 principal interval 著色的 restricted-domain trig graphs（§1.2）。
- one-sided-limit 不一致的範例（§1.4）。
- $\varepsilon$–$\delta$ tube-and-interval diagram（§1.6）。

**Handout self-sufficiency vs. video reinforcement**
- 講義獨立承載每個 definition、每個 theorem statement、每個 worked example 和每個 strategy box。
- 影片（每節一支，目前以 §1.1 為範例）增加了動態的沿 $y=x$ 反射展示、動態的 $\varepsilon$–$\delta$ tube（靜態頁面無法傳達的效果）、以及對記號陷阱的較慢口頭講解。
- 影片中沒有任何內容取代閱讀講義——影片場景在 [`legacy/MANIM_STORYBOARD.md`](legacy/MANIM_STORYBOARD.md) 中標記為 reinforcement。

**Strategy boxes present**
- 求 inverse function（§1.1）。
- 計算 limit（§1.5）。
- 驗證 $\varepsilon$–$\delta$ limit（§1.6）。

**Notation introduced**
- `\arcsin`、`\arccos`、`\arctan`、`\arccsc`、`\arcsec`、`\arccot`（本書的 inverse-trig operator）。
- `\lim_{x \to a} f(x)`、`\lim_{x \to a^-} f(x)`、`\lim_{x \to a^+} f(x)`、`\lim_{x \to \infty} f(x)`。
- $\varepsilon$、$\delta$。

**Common pitfalls (caution boxes present)**
- $\sin^{-1} x$ 表示 inverse sine，不是 $1/\sin x$。
- $\arcsin(\sin x) = x$ 僅在 principal interval $[-\pi/2, \pi/2]$ 上成立。

**Open questions**
- 本區塊為 ch01 **Mode C 充實**的延後／刻意省略決定錨點（依 [`README.md`](README.md) Mode A/C 擴增稽核；2026-06-15 起）。
- （習題項已結案：講義本體不收習題，placeholder 已全數移除——[`CONTENT_SPEC.md`](CONTENT_SPEC.md) §14，2026-06-12 定案。課文範例補充另行進行，見 [`CONTENT_SOURCING.md`](CONTENT_SOURCING.md)。）
- *§1.2（inverse trig）後移*——**deferred 2026-07-03**：作者提議把 inverse trig 詳細計算移到 inverse-trig derivatives（現 §3.3）之前再教。兩輪 Codex 仲裁結論：教學論點成立但非 hotfix——Stewart／Thomas ET 同樣把 inverse trig 放 Ch1、導數放 Ch3（現行＝主流做法）；模擬閱讀判 §1.2 修補後可自學通過；搬動觸發 Ch1＋Ch3 全面重編號與雙章審核閘重跑。留待未來 arc 修訂（依本檔「roadmap-first」程序）一併重估。過渡措施已上：§1.2 lead 的 Chapter 3 forward fence（2026-07-03）。仲裁紀錄：`handout/_audit/REVIEW-ch01-ch04-difficulty-mitigation-applied.html`。

---

## Chapter 2（已填 entry）

### Chapter 2: Derivatives

**Status**: draft，**Mode C 充實中**。手稿覆蓋在 HTML handout 中已**完成**（`handout/fragments/ch02/`）：§2.1–§2.5 透過六階方向層流程（[`CONTENT_DIRECTION.md`](CONTENT_DIRECTION.md)）撰寫，每節經 Codex audit 至 blocking=0（2026-06）。Mode C 充實分兩波：① 課文範例補充已套用（6 例，2026-06-22，重編號至 Examples 2.1–2.23，見 [`handout/_audit/REVIEW-ch02-example-supplement-applied.html`](handout/_audit/REVIEW-ch02-example-supplement-applied.html)）；② 軟深度充實（intuition／caution／application／history）已套用 15 塊（2026-06-26，皆標 `[pass: enrichment]`，範圍限定 Mode B/S·A·V gate-1 全 0 blocking，見 [`handout/_audit/REVIEW-ch02-modec-applied.html`](handout/_audit/REVIEW-ch02-modec-applied.html)；裁決稿 `REVIEW-ch02-modec-adjudication.html`，候選 `REVIEW-ch02-modec-enrichment.html`）。gate-2 Codex（gpt-5.5, read-only）跨模型複審亦過：14 塊 clean、1 blocking on §2.3 的 \(d^2y/dx^2\) 記號（reify `dx`，與 §2.2「`dy/dx` 非分數」衝突）→ 改 operator 讀法 → re-audit pass（見 [`handout/_audit/REVIEW-ch02-modec-gate2.html`](handout/_audit/REVIEW-ch02-modec-gate2.html)）。圖機會閘＋圖正確性閘已跑（2026-06-26）：圖正確性 8 圖（6 buildPlot＋2 inline SVG）視覺 blocking 全 0——quotient-example-graph 上面板 f(x) 標籤與藍曲線同色糊字 1 blocking 已修（標籤移右下空白區）＋重渲確認，見 [`handout/_audit/REVIEW-ch02-figure-audit.html`](handout/_audit/REVIEW-ch02-figure-audit.html)；圖機會閘提 5 候選、裁決畫 2（F-2.3-A＝§2.3 Example 2.12 ∛x 垂直切線、F-2.1-A＝§2.1 差商解剖），兩新圖 D1–D8 複審 0 blocking，其餘 3 候選不畫（近重複），見 [`handout/_audit/REVIEW-ch02-figure-opportunity.html`](handout/_audit/REVIEW-ch02-figure-opportunity.html)。圖總數 8→10。獨立數學正確性閘已跑（2026-06-26，gate-1 Claude ×5＋gate-2 Codex）：M1–M8 雙閘 blocking 全 0（gate-1 1 條 borderline advisory＝§2.4 Ex 2.16 定義域 polish、gate-2 未復現），worked-example 答案多處 sympy 重算核對，見 [`handout/_audit/REVIEW-ch02-math-audit.html`](handout/_audit/REVIEW-ch02-math-audit.html)。新版 S·A·V 散文閘（Task 8）已跑（2026-06-26，gate-1 Claude ×5）：5 節 blocking 全 0、10 條 advisory（皆 propose-only 軟潤稿），裁決套用 2 條 F4 拆句（§2.4 eˣ setup、§2.5 rectangle-area），逐節回歸 PASS、其餘 8 條保留，見 [`handout/_audit/REVIEW-ch02-svc-gate1.html`](handout/_audit/REVIEW-ch02-svc-gate1.html)。**S·A·V 與圖正確性兩閘的 gate-2 Codex 獨立複核亦已跑（2026-06-26）：** ① 散文 gate-2（`codex exec` read-only，依同一 PROSE rubric＋svc 錨組獨立審 5 節）blocking 全 0（兩 critic 一致）、4 條新 advisory，裁決採納 C2-3／C2-4＝改掉 §2.4／§2.5 共 5 處 student-facing 散文露出「the manuscript」為內容層語氣（HTML 註解 provenance 保留、數學不動），逐節回歸 re-audit PASS、其餘 2 條 F4 密度保留，見 [`handout/_audit/REVIEW-ch02-svc-gate2.html`](handout/_audit/REVIEW-ch02-svc-gate2.html)；② 圖正確性 gate-2（Codex 收 10 張重渲 2× PNG via `-i`，回 `const FIGS`／inline-SVG 算數值核對 D1–D8）全 10 圖 blocking 0、advisory 0（含兩新圖與 gate-1 修過的 quotient-example-graph），見 [`handout/_audit/REVIEW-ch02-figure-audit-gate2.html`](handout/_audit/REVIEW-ch02-figure-audit-gate2.html)。**Ch2 至此與 Ch1 完全同級全跑（含各閘 gate-2 跨模型複核）**：手稿六階＋Mode C（例題＋軟深度）＋去 AI 味 S·A·V（gate-1+gate-2）＋圖機會/正確性兩閘（圖正確性 gate-1+gate-2）＋數學正確性雙閘。
**Source file**: `handout/fragments/ch02/sec-2-*.html`
**Estimated length**: *（完成首次完整編譯後填入）*
**Manuscript source**: received 2026-04-27（13 頁手寫手稿，由該章作者提供）。手稿涵蓋微分章的基礎部分：tangent-line motivation、the derivative at a point、the derivative as a function、differentiability vs continuity、higher derivatives、constants / power function / exponential 的微分、以及 product / quotient rules。**不包含**原始 working hypothesis 中列為 §2.4–§2.8 的 trigonometric、chain-rule、implicit、inverse-function 或 logarithmic-derivative 材料。這些主題是否會作為後續手稿到達（擴展 Ch 2）或移至後面的章節，見下方 Open questions。

**Role in the arc**
Chapter 2 是 Calc I 的**展開**階段。它將 Chapter 1 的 limit 機器轉化為一個可運作的算子：給定一個函數，產生另一個描述其瞬時變化率的函數。Ch 1 完成了繁重的概念鋪墊（「逼近但不等於」意味著什麼？）；Ch 2 將其在演算法上兌現。以目前手稿的範圍，Ch 2 涵蓋 derivative 的 definition 以及對 polynomial、natural exponential 和任何可微函數的 product 或 quotient 進行微分所需的規則。Trigonometric、chain-rule、implicit、inverse 和 logarithmic differentiation 是延後的（見 Open questions）。

**Prerequisites**
- **來自 Chapter 1**：全部六節，尤其 §1.3（limits）、§1.4（one-sided and infinite limits）和 §1.5（limit laws）。Derivative 是以 limit 定義的；對 limit 運算不熟練的學生無法撐過 §2.1 的定義。§1.6（ε-δ）並非嚴格前提——derivative 是用 algebraic limit 而非 ε-δ 形式表述的——但看過 §1.6 的學生會覺得 §2.1 的嚴謹性不那麼突兀。
- **Precalculus**：polynomial 和 rational 運算；binomial theorem（用於 §2.4 power-rule proof）。
- **不需要先前接觸 derivative**——本章假設 derivative 是新概念。

**Core skills**（將對應章節開頭的 bullet list）
- 陳述 derivative 的 limit definition $f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}$ 並應用之從 first principle 計算 polynomial 和 root function 的 derivative；
- 使用 power、constant-multiple、sum、product 和 quotient rule 微分代數和指數的組合；
- 用 series definition 微分 natural exponential function $e^x$；
- 識別函數不可微的位置（如 corner）並將 differentiability 與 continuity 連結；
- 計算 higher-order derivative。

**Key figures**
- secant-to-tangent limit diagram（§2.1）：一條曲線上，一系列 secant line 隨第二個點趨近第一個點而收斂為 tangent line。
- derivative as a function（§2.2）：一對圖，$f$ 在上、$f'$ 在下，以 $x$-axis 對齊，使零點、極值和正負號變化在視覺上對齊。
- 在 corner 不可微（§2.3）：$|x|$ 在 $0$ 附近的圖形，左右 secant slope 有標記，顯示 one-sided limit 不一致。

**Handout self-sufficiency vs. video reinforcement**
- 講義獨立承載 limit definition、每條微分規則及其 proof、每個 worked example 和每個 strategy box。
- 影片增加：(a) 動態 secant-to-tangent 收斂動畫（靜態頁面難以傳達）；(b) 動態 slope-of-tangent-line demo，其中 tangent point 沿曲線掃過，slope 即時繪在下方，展示 $f'$ 作為函數的浮現。
- 影片中沒有任何內容取代閱讀講義；推廣方向始終是 *video → handout*，永遠不是反向。

**Strategy boxes expected**
- *Computing a derivative from the limit definition*（§2.2）：3 步流程——(1) 寫出 difference quotient $(f(x+h) - f(x))/h$；(2) 代數化簡直到 $h$ 從分母中消去；(3) 取 $h \to 0$。
- *Selecting among the basic rules*（§2.5）：何時使用 power rule vs product vs quotient；測試標準是表達式的語法形狀。

**Notation introduced**
- $f'(x)$、$\dfrac{dy}{dx}$、$\dfrac{df}{dx}$、$\dfrac{d}{dx}[f(x)]$、$f''(x)$、$f^{(n)}(x)$——常見的 derivative notation，引入時明確指引何時各自最自然。在首次使用時為 prime notation 和 Leibniz notation 各加 index entry。
- $\Delta x$、$h$——increment notation；手稿在引入代換 $x = a + h$ 之後專用 $h$。在 caution 中標記 $\Delta x$ 和 $h$ 在 derivative context 中是同義的。

**Common pitfalls (caution boxes)**
- *Power rule domain*：$\frac{d}{dx}[x^n] = n x^{n-1}$ 在 §2.4 中對正整數 $n$ 證明；負整數情形留為 manuscript exercise。Caution 標記此點並將 full real-exponent 的陳述延後至後面的章節。
- *Quotient rule asymmetry*：$\frac{d}{dx}\left[\frac{f}{g}\right] = \frac{f'g - fg'}{g^2}$ 對 $f$ 和 $g$ 不對稱；分子中項的順序很重要。
- *Differentiable implies continuous, but not conversely*：§2.3 的定理是單方向的。$|x|$ 在 $0$ 處是標準反例；手稿和本章都明確指出。
- *(fg)' is not f'g'*：手稿用 product rule 的開場反例（`f = x`、`g = x^2`、`fg = x^3`）；caution 將其保留為主要陷阱。

**Open questions**
- ~~*Manuscript scope vs original 9-section hypothesis*~~——**resolved 2026-04-27**：兩份後續手稿（`2023-10-28-chainRule` 和 `2023-11-4-ExponentialFunction`）涵蓋了缺失的主題（trig derivatives、chain rule、ln/arcsin/x^x via chain rule、rigorous $e^x$、MVT、ln）。這 4 個缺失主題沒有擴展 Ch 2；它們成為 Ch 3（*Chain Rule and Trigonometric Derivatives*）和 Ch 4（*The Exponential and Logarithmic Functions*）。Implicit differentiation 不在任何一份手稿中，仍延後至後面的章節。
- ~~*Treatment of $e^x$ derivative*~~——**resolved 2026-06-08**：在 §2.4 ⑥ convergence gate 確認。本章遵循手稿的 series-based derivation（提出 $e^x$，然後 $(e^h-1)/h = 1 + h/2! + h^2/3! + \dots \to 1$），保持手稿的直覺層次而非 Stewart 的「$\lim_{h \to 0}(e^h-1)/h = 1$ as the defining property」路線。嚴格的 convergence 和 $e^x$ 的 construction 延後至 Ch 4 §4.3，該節會重新推導 derivative 並 cross-reference 回來。在 §2.4 實作為 Theorem 2.5 + series proof，附一行 forward fence 到 Ch 4，以及 Codex audit（4 runs, blocking=0）。
- ~~*Higher derivatives placement*~~——**resolved 2026-06-08**：higher derivative（$f''$、$f'''$、$f^{(n)}$）保持為 §2.3 的 subsection（遵循手稿）。在 §2.3 ⑥ convergence gate 確認；brief 和 HTML 均將其實作為 `<h3>` subsection 而非獨立的 `<article class="sec">`。
- ~~*§2.5 product/quotient rules——figure choice & section completion*~~——**resolved 2026-06-08** 於 §2.5 ⑥ convergence gate（最後一個 manuscript section，因此完成了 Ch 2 的 manuscript coverage）。實作為 Theorem 2.6（product rule）和 Theorem 2.7（quotient rule），使用手稿的 add-and-subtract proof——domain hypotheses 明確化（$g$ continuous via §2.3 Theorem 2.1；$g(x)\neq 0$ for the quotient）——加上 Strategy 2.2（*selecting among the basic rules*，by syntactic shape + "simplify first"）、三個 pitfall caution（$(fg)'\neq f'g'$ 用手稿的反例、$\Delta x \equiv h$、quotient-rule asymmetry）、以及 Examples 2.15–2.17。**Figure decision**：使用者加入了 **Figure 2.4**，一張 product-rule rectangle-area diagram（面積增量 = 長條 $f\,\Delta g$、$g\,\Delta f$ + 二階 corner $\Delta f\,\Delta g$），覆蓋了 brief 的預設「rules section 不附圖」；以 inline schematic SVG 呈現（無 `figures.js` entry——`buildPlot` 沒有 fill primitive）。保持 label-light 衍生出一條新的權威規則：[`CONTENT_SPEC.md`](CONTENT_SPEC.md) §10 "Label economy"（在 kit 的 `CONTRACT-html-writing.md` §Figures 中 mirror），後續章節遵循。Codex audit converged（2 runs；run 1 抓到一個在新增的 $1/x$ inline check 中的 notation conflict，修正後 → run 2 blocking=0）。

---

## Chapter 3（已填 entry）

### Chapter 3: Chain Rule and Trigonometric Derivatives

**Status**: **與 Ch1/Ch2 同級全跑**（2026-06-27）。手稿覆蓋於 2026-06-08 完成（§3.1–§3.3，三節皆過 six-stage convergence gate，含 two-model adversarial audit：Claude multi-lens + Codex gpt-5.5 xhigh）。其後各獨立閘已補齊全跑：**Mode C** ①課文範例補充（+4 CLP-1 worked example、全章重編號 Examples 3.1–3.16、雙閘收斂，見 [`handout/_dev-archive/ch03/ch03_example-supplement-review.html`](handout/_dev-archive/ch03/ch03_example-supplement-review.html)）＋②軟深度（§3.1 +1 Caution「極限非恆等式」，見 [`handout/_audit/REVIEW-ch03-modec-enrichment.html`](handout/_audit/REVIEW-ch03-modec-enrichment.html)）；**圖機會閘＋圖正確性兩閘**（7 圖 Figure 3.1–3.7：圖機會閘核可新增 5 圖、視覺正確性 gate-1 D1–D8 全 0 blocking［Fig 3.7 等比座標修正後回歸，2026-06-21，見 [`handout/_audit/REVIEW-ch03-figure-opportunity.html`](handout/_audit/REVIEW-ch03-figure-opportunity.html)］；gate-2 Codex 視覺第二讀者［120,683 tokens］提 1 blocking——Fig 3.6 caption「Halving $h$」vs FIGS source $0.5/1.35\approx0.37$（D5）→裁決修圖 `panel(0.5)→panel(0.675)` 真減半→手動回歸 PASS，見 [`handout/_audit/REVIEW-ch03-figure-audit-gate2.html`](handout/_audit/REVIEW-ch03-figure-audit-gate2.html)）；**數學正確性 M1–M8 雙閘**（sympy 獨立重算 31/31 PASS＋gate-1 Claude ×5［per-section×3＋cross-ref＋proof-rigor，對抗式 verify 0 候選］＋gate-2 Codex［100,807 tokens］，皆 0 blocking 0 advisory，見 [`handout/_audit/REVIEW-ch03-math-audit.html`](handout/_audit/REVIEW-ch03-math-audit.html)）；**去 AI 味 S·A·V 散文雙閘**（Vale 0/0/0＋gate-1 Claude ×3 0 blocking［採 5 條 copyedit tighten］＋gate-2 Codex［81,096 tokens］0 blocking［採 2 條 F5「the manuscript」student-facing 露出改寫］，見 [`handout/_audit/REVIEW-ch03-svc-gate1.html`](handout/_audit/REVIEW-ch03-svc-gate1.html)／[`REVIEW-ch03-svc-gate2.html`](handout/_audit/REVIEW-ch03-svc-gate2.html)）。**Ch3 至此與 Ch1/Ch2 完全同級全跑**：手稿六階＋Mode C（①例題＋②軟深度）＋去 AI 味 S·A·V（gate-1+gate-2）＋圖機會/正確性兩閘（圖正確性 gate-1+gate-2）＋數學正確性雙閘。
**Source file**: `handout/fragments/ch03/sec-3-*.html`
**Estimated length**: *（完成首次完整編譯後填入）*
**Manuscript source**: `2023-10-28-chainRule`（2023-10-28 的手寫手稿，2026-04-27 收到）。手稿涵蓋 (i) 透過 squeezing lemma + sector geometry 推導 $\sin x$ 和 $\cos x$ 的 derivative，(ii) 使用 differentiability 的 remainder-form definition（$f(x_0 + h) = f(x_0) + mh + R(h)$，$R(h)/h \to 0$）證明 chain rule，以及 (iii) chain-rule 應用，包括 $d/dx \ln x$、$d/dx x^x$ 和 $d/dx \arcsin y$。手稿也重述了 product rule 和 differentiable-implies-continuous lemma；兩者在 Ch 3 中以 cross-reference 回 Ch 2 處理，而非重新推導。

**Role in the arc**
Chapter 3 是 Calc I 的**規則延續**。Chapter 2 建立了 derivative 的 limit definition 和基本代數規則（constant、power、sum、product、quotient、$e^x$）；Chapter 3 加入 composition 的規則（chain rule）並將其應用於引入 trigonometric derivative 以及提取 inverse function 和 implicitly-defined function 的 derivative。連同 Ch 4 對 $e^x$ 和 $\ln x$ 的嚴格處理，Ch 3 收尾了微分工具箱。

**Prerequisites**
- **來自 Chapter 1**：§1.5（特別是 squeeze theorem——直接用於 $\lim_{\theta \to 0} \sin \theta / \theta = 1$）。§1.2（inverse trig——$\arcsin$ 是 chain-rule example 的目標之一）。
- **來自 Chapter 2**：全部五節，尤其 §2.5 product rule（chain-rule 手稿重新推導了它；我們改為 cross-ref）和 §2.3 differentiable $\Rightarrow$ continuous（用於 chain-rule proof 和 trigonometric continuity proof 中）。
- **Trigonometric identity**：和差化積 identity $\sin(x + h) - \sin(x) = 2 \sin(h/2) \cos(x + h/2)$ 是本章的主要代數工具。Pythagorean identity $1 + \tan^2 = \sec^2$ 也出現在 worked example 中。

**Core skills**
- 計算 $d/dx \sin x$、$d/dx \cos x$、$d/dx \tan x$，以及（透過 chain rule）$d/dx \sin(g(x))$、$d/dx \cos(g(x))$ 等；
- 應用 chain rule 微分兩層或多層函數的 composition，包括 $f(g(h(x)))$ 型的巢狀；
- 使用 chain rule + log differentiation 微分 $x^x$、$f(x)^{g(x)}$ 和類似的非標準指數表達式；
- 從 inverse-function relation $\sin(\arcsin y) = y$ 等出發，應用 chain rule 推導 $d/dx \arcsin x$、$d/dx \arctan x$ 和 $d/dx \ln x$。

**Key figures**
- secant inequality figure（§3.1）：unit circle 上的 sector $OAB$ 和三角形 $\triangle OAB$、$\triangle ABC$，用以建立 $\cos \theta \le \sin \theta / \theta \le 1$ 的邊界。
- chain rule as composed mapping（§3.2）：堆疊的 input–intermediate–output 軸，展示微小的 $h$ 在 input 端如何傳播到 output 端的變化，以 intermediate slope 的乘積為比例。

**Strategy boxes expected**
- *Chain-rule decomposition*（§3.2）：給定一個複雜表達式，辨識最外層操作；將表達式寫為 $f(g(x))$；微分為 $f'(g(x)) \cdot g'(x)$。對巢狀 composition 迭代此步驟。
- *Logarithmic differentiation*（§3.3）：當表達式具有 $f(x)^{g(x)}$ 的形式或具有多因子的 product/quotient 時，對兩邊取 $\ln$，應用 chain rule 和 product rule，然後解出 $y'$。

**Notation introduced**
- differentiability 的 remainder-form definition $f(x_0 + h) = f(x_0) + m h + R(h)$，$R(h)/h \to 0$。這是手稿中的 Def 2；等價於標準的 limit definition，但對 chain-rule proof 更方便。
- $\arcsin'$、$\arccos'$、$\arctan'$ 在 §3.3 中透過對 $\sin(\arcsin y) = y$ 等應用 chain-rule 技巧而引入。

**Common pitfalls (caution boxes)**
- *Chain rule is one identity, not two fractions*：$\frac{dy}{dx} = \frac{dy}{du} \cdot \frac{du}{dx}$ 是 chain rule，不是 $du / du = 1$ 的消去。Leibniz 形式的表觀分數消去是有用的助記法，但不是 proof。
- *Forgetting the inner derivative*：最常見的 chain-rule 錯誤是 $\frac{d}{dx}[\sin(g(x))] = \cos(g(x))$ 而非 $\cos(g(x)) \cdot g'(x)$。一個 worked example 標記此錯誤。
- *Domain issues for $\arcsin$ derivative*：公式 $1/\sqrt{1 - y^2}$ 僅在 $y \in (-1, 1)$（open interval——endpoints 具有 vertical tangent）上有效。Caution 標記此點。
- *$\ln$ used informally before rigorous construction*：§3.3 將 $\ln$ 視為「$e^x$ 的 inverse」，使用 $e^{\ln x} = x$ 提取 $d/dx \ln x = 1/x$。嚴格的 construction 延後至 Ch 4。一則 note 標記此依賴關係。

**Open questions**
- ~~*Trig derivatives placement vs squeeze-theorem location*~~——**resolved 2026-06-08** 於 §3.1 ⑥ convergence gate：Ch 3 草稿**在散文中 cross-reference §1.5 squeeze theorem，不重述它**（D4）。$\lim_{\theta \to 0} \sin \theta / \theta = 1$ 作為 **Proposition 3.2** 證明，$\sin$ 和 $\cos$ 的 continuity 作為 **Proposition 3.1** 證明，各自在 $\theta \to 0$ 形式上引用「the squeeze theorem (§1.5)」；手稿的額外 $x \to \infty$ 形式不需要且省略，因此無重複。$(1 - \cos\theta)/\theta \to 0$ 作為 **Example 3.1** 加入（D2）。Two-model adversarial audit（Claude 4-lens + Codex gpt-5.5 ×2 runs）converged with 0 blocking。
- ~~*Two equivalent definitions of differentiability*~~——**resolved 2026-06-08** 於 §3.2 ⑥ convergence gate：Def 2（remainder form）在 §3.2 作為 **Definition 3.1** 引入，因為 chain-rule proof 使用它。Def 1（limit form）在 §2.2 建立，**在散文中 cross-reference，不重新編號**（Option B，§3.2 ③ 核准）。等價性作為 **Proposition 3.3** 證明——忠實的短雙向論證，補充了手稿中 bare "easy to see" 的部分——然後 Def 2 僅用於 chain-rule proof（Theorem 3.3）。Two-model adversarial audit（Claude 4-lens + Codex gpt-5.5 ×2 runs）converged with 0 blocking。
- ~~*Implicit differentiation*~~——**resolved 2026-06-08** 於 §3.3 ⑥ convergence gate（D10）：§3.3 遵循手稿的 **composition-identity route**——$\ln x$（Example 3.6）、$\arcsin$（3.10）、$\arccos$（3.11）和 $\arctan$（3.12）的 derivative 透過微分各函數滿足的 identity（$e^{\ln x}=x$；$\arcsin(\sin x)=x$ on $[-\pi/2,\pi/2]$；etc.）並解出未知 derivative 而得到，$x^x$（3.7）透過 logarithmic differentiation（Strategy 3.2）——**未引入 implicit-differentiation framework 或 vocabulary**。未來的專門 implicit-differentiation 章節可能重新審視這些作為 canonical motivating example。Two-model adversarial audit（Claude 5-lens + Codex gpt-5.5 ×4 runs, xhigh）converged with 0 blocking；唯一的 blocking finding（unqualified $\arcsin(\sin x)=x$）被 Codex 抓到並修正。
- ~~*$\ln x$ informal before rigorous construction; $\arcsin$-derivative domain*~~——**resolved 2026-06-08** 於 §3.3 ⑥ gate（D8 + pitfalls）：$\ln x$ 以非正式方式作為 $e^x$ 的 inverse（僅用 $e^{\ln x}=x$）來提取 $d/dx\,\ln x = 1/x$（Example 3.6），附一行 forward fence 將嚴格 construction 延後至 Ch 4 §4.5（該節會重新推導）。$\arcsin/\arccos$ 的 derivative $1/\sqrt{1-y^2}$ 在 unnumbered Caution 中標記為僅在 **open** interval $(-1,1)$ 上有效；$\arctan$（Example 3.12）與之對比——在全 $\mathbb{R}$ 上可微。

---

## Chapter 4（已填 entry）

### Chapter 4: The Exponential and Logarithmic Functions

**Status**: **與 Ch1/Ch2/Ch3 同級全跑**（2026-06-27）。手稿覆蓋於 2026-06-21 完成（§4.1–§4.5，五節皆過 six-stage convergence gate，含 two-model adversarial audit：Claude multi-lens + Codex gpt-5.5 xhigh、章層 Mode B）。其後各獨立閘已補齊全跑：**Mode C** ①課文範例補充（§4.4 +2 CLP-1 worked example＝Example 4.3 Lipschitz／4.4 根計數，Example 封頂重編號 4.1–4.7，雙閘收斂，見 [`handout/_audit/REVIEW-ch04-example-supplement-applied.html`](handout/_audit/REVIEW-ch04-example-supplement-applied.html)）＋②軟深度（§4.4／§4.5 各 +1 Caution＝假逆命題 $x^3$／對數誤推廣 $\ln(a+b)$，見 [`handout/_audit/REVIEW-ch04-modec-enrichment-applied.html`](handout/_audit/REVIEW-ch04-modec-enrichment-applied.html)）；**圖機會閘＋圖正確性兩閘**（6 圖 Figure 4.1–4.6：圖機會閘核可新增 3 圖＝完備性/夾擠/倒數斜率；視覺正確性 D1–D8 gate-1+gate-2 Codex［77,984 tokens，6 PNG via `-i`］兩模型一致 0 blocking／1 非 blocking advisory［Fig 4.2 -2 刻度負號被壓、簽核圖不動］，見 [`handout/_dev-archive/ch04/ch04_figure-audit-gate2.md`](handout/_dev-archive/ch04/ch04_figure-audit-gate2.md)）；**數學正確性 M1–M8 雙閘**（gate-1 Claude ×7［5 per-section＋worked-example 重算＋跨章一致性，對抗式雙鏡頭 verify 0 候選］＋主流程 sympy 全 PASS＋gate-2 Codex［173,720 tokens］，皆 0 blocking 0 advisory，見 [`handout/_audit/REVIEW-ch04-math-audit.html`](handout/_audit/REVIEW-ch04-math-audit.html)）；**去 AI 味 S·A·V 散文雙閘**（Vale 0/0/0＋gate-1 Claude ×5 0 blocking［採 4 條 copyedit tighten］＋gate-2 Codex［154,714 tokens］0 blocking＋Claude 完整性掃描補抓 3 處 F5「the manuscript」student-facing 露出全採去露出＋回歸 PASS，見 [`handout/_audit/REVIEW-ch04-svc-gate1.html`](handout/_audit/REVIEW-ch04-svc-gate1.html)／[`REVIEW-ch04-svc-gate2.html`](handout/_audit/REVIEW-ch04-svc-gate2.html)）。**Ch4 至此與 Ch1/Ch2/Ch3 完全同級全跑**：手稿六階＋Mode C（①例題＋②軟深度）＋去 AI 味 S·A·V（gate-1+gate-2）＋圖機會/正確性兩閘（圖正確性 gate-1+gate-2）＋數學正確性雙閘。
**Source file**: `handout/fragments/ch04/sec-4-*.html`
**Estimated length**: *（完成首次完整編譯後填入）*
**Manuscript source**: `2023-11-4-ExponentialFunction`（2023-11-04 的手寫手稿，2026-04-27 收到）。手稿涵蓋 (i) 透過 power series $\sum x^n / n!$ 嚴格構造 $e^x$，使用 $\mathbb{R}$ 的完備性證明 convergence；(ii) $e^x$ 的 continuity 和 exponent law $e^x e^y = e^{x+y}$，透過仔細的 series-multiplication 論證和 Cauchy convergence；(iii) derivative $d/dx \, e^x = e^x$（比 Ch 2 §2.4 更嚴格的重新推導，附有對 $(e^h - 1)/h - 1$ 的 explicit bound）；(iv) Rolle's theorem 和 Mean Value Theorem；(v) 推論 $f' \ge 0 \Rightarrow f$ increasing；(vi) logarithm $\ln x$ 作為 $e^x$ 的 inverse，其 continuity，以及 $d/dx \ln x = 1/x$（透過 inverse-function technique）。

**Role in the arc**
Chapter 4 為 Calc I 的微分章節收尾嚴謹基礎。Ch 2 非正式地引入了 $e^x$ 並從一個隨意的逐項論證證明 $(e^x)' = e^x$；Ch 4 從零開始以 power series 建構 $e^x$，證明 Ch 2 視為理所當然的 convergence 和 continuity，並以完全嚴謹的方式重新推導 derivative。本章接著引入 Mean Value Theorem——驅動 derivative-to-monotonicity 論證的核心存在定理，用以將 strictly increasing 的 $e^x$ 反轉而構造 $\ln x$。Chapter 5 以後（applications of differentiation：extrema、optimisation、related rates、L'Hôpital）將重用本章引入的 MVT 機器。

**Prerequisites**
- **來自 Chapter 1**：§1.5（limit law 和基本 continuity 論證）、§1.6（precise $\varepsilon$-$\delta$ definition——§4.2 對 $e^x$ 的 continuity proof 本質上是 $\varepsilon$-$\delta$ 精神的，看過 §1.6 的學生會覺得熟悉）。
- **來自 Chapter 2**：§2.4（informal 的 $(e^x)' = e^x$ derivation；§4.3 嚴格重做並 cross-reference 回來）、§2.3（differentiable $\Rightarrow$ continuous，用於 MVT setup）。
- **來自 Chapter 3**：§3.3 非正式地使用 $\ln x$ 並 forward reference 到本章的嚴格 construction；§4.5 關閉此迴路。
- **Real analysis prerequisites**：reals 的 completeness（monotone bounded sequence converge）；Bolzano–Weierstrass（在 §4.2 中從 completeness 經由 monotone-subsequence lemma 證明）；binomial theorem（已在 Ch 2 §2.4 power-rule proof 中使用）。Cauchy sequence 及 convergent $\Leftrightarrow$ Cauchy 的等價在 §4.2 中引入並**證明**。

**Core skills**
- 陳述 $e^x$ 的 power-series definition 並 bound 其 tail 以建立在 $\mathbb{R}$ 上的 convergence；
- 證明 $e^x$ 在 $\mathbb{R}$ 上 continuous 且滿足 $e^x e^y = e^{x+y}$（透過 series-multiplication 論證）；
- 嚴格地用 bound $\lvert (e^h - 1)/h - 1 \rvert \le \lvert h \rvert$（在小區間上）計算 $d/dx \, e^x = e^x$；
- 陳述並證明 Rolle's theorem 和 Mean Value Theorem；
- 使用 MVT 證明 $f' \ge 0$ on $(a, b)$ implies $f$ is increasing on $[a, b]$；
- 定義 $\ln x$ 為 $e^x$ 的 inverse，證明其 continuity，並推導 $d/dx \ln x = 1/x$。

**Key figures**
- partial-sum convergence figure（§4.1）：在 $[-2, 2]$ 上繪製 $\sum_{n=0}^{k} x^n / n!$（$k = 1, 2, 3, 4$），展示收斂到光滑的 $e^x$ 曲線。
- MVT 的 secant–tangent figure（§4.4）：一條曲線，從 $(a, f(a))$ 到 $(b, f(b))$ 的 secant 畫為 dashed，內部點 $c$ 處的平行 tangent 畫為 solid。
- $e^x$ 和 $\ln x$ 的反射（§4.5）：重用 Ch 1 的 reflection-across-$y = x$ setup，$e^x$ 為 blue、$\ln x$ 為 red。

**Strategy boxes expected**
- *Tail-bound argument*（§4.1、§4.2）：當 $n_0 > 2x$ 時，用 geometric series bound $\sum_{n = n_0 + 1}^{\infty} x^n/n!$。此模板在本章中多次重用，值得提煉。
- *Verifying the MVT hypotheses before applying*（§4.4）：分別檢查 $[a, b]$ 上的 continuity 和 $(a, b)$ 上的 differentiability。常見錯誤是在函數於 endpoint 實際不可微的 closed interval 上應用 MVT。

**Notation introduced**
- $e^x$ 作為 power-series definition（手稿的選擇）。$\ln x$ 在 §4.5 首次使用時加 index entry；$e$（常數）和 $e^x$（函數）在 §4.1 首次使用時加 index entry。
- $C_k^n$ 表示 binomial coefficient（手稿的記號）。本書全程使用 $\binom{n}{k}$；當手稿的記號出現時 cross-reference 兩種記號。
- $P_k(x) = \sum_{n=0}^{k} x^n / n!$ 表示 partial sum（手稿的記號，在 §4.1–§4.2 中保留）。

**Common pitfalls (caution boxes)**
- *Series defines, doesn't derive*：series $e^x = \sum x^n / n!$ 在本章是 $e^x$ 的 **definition**。熟悉的 exponent law、continuity 和 derivative 接著是需要證明的 theorem。在 Ch 2 非正式接觸過 $e^x$ 的學生可能會在這些性質重新建立之前就嘗試使用；標記此點。
- *Bolzano–Weierstrass dependency*：§4.2 中 convergent $\Leftrightarrow$ Cauchy 的 proof 經由 Bolzano–Weierstrass（從 completeness 經 monotone-subsequence peak argument 證明）。章節 note 中的 caution 標註依賴鏈，讓學生看到 Cauchy $\Leftrightarrow$ convergent 在邏輯上等價於 completeness。
- *MVT continuity vs differentiability*：函數必須在 **closed** interval $[a, b]$ 上 continuous 且在 **open** interval $(a, b)$ 上 differentiable；endpoint 處的 differentiability 不要求。Caution 標記此不對稱。
- *$\ln$ defined only for $x > 0$*：每個涉及 $\ln x$ 的公式都隱含 $x > 0$。在 §4.5 標記；與 Ch 3 §3.3 相同慣例。

**Open questions**
- ~~*Cauchy / convergent equivalence proof*~~——**resolved 2026-04-27（user-directed）**：proof 在 §4.2 中透過 Bolzano–Weierstrass theorem 和 monotone-subsequence lemma 供給，超越了手稿本身供給的範圍。本章現在完整證明兩個方向。
- ~~*Exponent law proof level of detail*~~——**resolved 2026-04-27（user-directed）**：§4.2 的 exponent-law proof 原本草擬為 4 步 outline；在使用者指示下改寫為完整的 6 步 proof，匹配手稿的 detail level（完整 binomial-theorem reorganisation、explicit (II)-piece tail-bound estimate、step 5 中 telescoped error）。
- ~~*MVT placement*~~——**resolved 2026-07-06**（全書 seam pass＋Codex 覆核）：MVT **留 Ch 4 不搬**。§4.5 的 $\ln$ 構造需 monotonicity corollary（Cor 4.3，源自 MVT Thm 4.12）；搬走會拆散 Ch4 邏輯鏈並觸發 Ch4＋Ch5 全重編號。Ch5 §5.4–§5.7 改以 cross-ref 引用 MVT（Thm 4.12）。
- ~~*IVT/EVT 補嚴謹（Ch4 定稿後結構補寫）*~~——**done 2026-07-06**（全書 seam pass 撈出；Codex 設計＋數學閘雙審收斂，0 blocking）：**Theorem 4.9 改為 EVT (a)＋IVT (b) 兩部**（Codex option c 綁併＝**零重編號**：EVT 仍 4.9、MVT 仍 4.12、§4.5 號全不動、export ledger 不變）；EVT 舊「陳述不證」黑箱 note 改 fence 至新建 **Appendix D（The Proof Track）**。§4.5 值域 $(0,\infty)$ 由默借改 **IVT 全證**（bracket＋IVT 4.9(b)，用 Cor 4.1／Thm 4.6／4.7）。閘：`build.py appD/ch04`＋linebreak-gate 0/0＋render katex-errors=0＋Codex 對抗式數學閘 **0 blocking**（2 微 advisory 未改）。loci：`fragments/ch04/sec-4-4.html`、`sec-4-5.html`、`fragments/appD/sec-d-1.html`、`sec-d-2.html`；applied 報告 [`handout/_audit/REVIEW-ch04-ivt-evt-applied.html`](handout/_audit/REVIEW-ch04-ivt-evt-applied.html)。
- *§4.3 redundancy with §2.4*：Ch 2 的 informal derivation of $(e^x)' = e^x$ 和 §4.3 的 rigorous re-derivation 主要差異在對 $(e^h - 1)/h - 1$ 的 explicit bound。可能的重構：將 Ch 2 的 casual version 替換為 forward-reference 到 §4.3，消除重複。決策延後至兩章都簽核後。
- *Applications 擴充（複利等）*——**recorded 2026-07-03**：作者希望補 exponential 建模應用。§4.5 已有 growth/decay/half-life capstone（§C-10 add-on）、§2.4 已有 $y' = ky$ 直覺段；缺的（複利、更完整的建模）留待 arc 內既定的 applications of differentiation 章草擬時以 example-supplement 流程補充，**不在 Ch4 內擴充**。仲裁紀錄：`handout/_audit/REVIEW-ch01-ch04-difficulty-mitigation-applied.html`。

---

## Ch5–16 弧線骨架（2026-07-04 使用者裁定脊椎＋深度基調；節層待前驅 draft）

> 研究（Stewart ET 9e／Thomas 14e／Rogawski 4e／NTU 微積分甲）＋Codex 覆核見 [`handout/_audit/REVIEW-chapter-arc-proposal.html`](handout/_audit/REVIEW-chapter-arc-proposal.html)。深度政策＝[`CONTENT_SPEC.md`](CONTENT_SPEC.md) §16.1 雙軸＋§16.3 逐章深度決策；使用者裁定 **(B) 分章校準**——「不假證」全程守住，主線嚴謹交付到 §16.2 難度預算為止，最重的定理 on-credit fence（Ch4 為既有深度上限）。深度基調三層：**深理論核心（Ch4 級）**／**標準嚴謹（rigorous-Stewart）**／**嚴謹陳述＋最重的 fence**。以下為脊椎骨架，非完整 entry；core skills／key figures／notation／確切各節與 Ch11/Ch16 拆章的最終編號待該章前驅到 `draft` 才填。

**Ch5 Applications of Differentiation** — *Role*：把 Ch2–4 的導數機器轉成分析工具。含極值/最佳化/相關變率/L'Hôpital/曲線描繪/Newton 法、隱微分、線性近似 differentials。*Prereq*：Ch2–4（尤 Ch4 MVT／單調性；反三角導數已在 Ch3）。*對應*：Stewart 4。*深度*：**標準嚴謹**（L'Hôpital 靠 §5.7 就地引入的 **Generalized MVT（Cauchy's form）** 可全證——Ch4 只有普通 MVT Thm 4.12、無 Cauchy 形；其餘應用計算為主）。節 roster（Codex 重排 9 節）見下方「全局 seam ledger」。 **〔2026-07-06 起 as-built〕** 首個無手稿章（canon-as-spine），Mode A（M1）完成；L'Hôpital ∞/∞ 補證入 **Appendix D §D.3**（Proof Track 第二 customer）。**閘狀態唯一表＝[`handout/PIPELINE.md`](handout/PIPELINE.md) dashboard；as-built 編號與逐節 ledger＝[`handout/_dev-archive/ch05/PLAN-ch05.md`](handout/_dev-archive/ch05/PLAN-ch05.md)**（2026-07-07 三檔分工制：本 entry 只留弧線／契約／open questions）；applied 報告 [`handout/_audit/REVIEW-ch05-applied.html`](handout/_audit/REVIEW-ch05-applied.html)。

**Ch6 Integrals** — *Role*：定積分與 FTC，接起微分與積分。含原函數/黎曼和/定積分/FTC/代換。*Prereq*：Ch5、Ch1 極限；附錄 GAP-A 冪次和（黎曼和從定義）。*對應*：Stewart 5。*深度*：**深理論核心**（FTC 當場證；最重的可積性刻畫 fence）。

**Ch7 Applications of Integration** — *Role*：積分的幾何/物理應用。含面積/體積/弧長/表面積/平均值/功（併入 further applications，選材節制以免比 Ch5 腫）。*Prereq*：Ch6。*對應*：Stewart 6(+8)。*深度*：**標準嚴謹**。

**Ch8 Techniques of Integration** — *Role*：符號積分工具箱。含分部/三角積分/三角代換/部分分式/瑕積分/數值積分；inverse hyperbolic 可放此。*Prereq*：Ch6；附錄 A.2（積化和差/降冪）、A.4（部分分式）、GAP-F（完全平方，三角代換）。*對應*：Stewart 7。*深度*：**標準/計算**。

**Ch9 Differential Equations** — *Role*：一階 DE 入門。含可分離/一階線性/成長衰變建模（銜接 Ch4 \(y'=ky\)）。**章名/開場明示 first-order intro**，排除二階線性/冪級數解。*Prereq*：Ch6–8。*對應*：Stewart 9。*深度*：**標準嚴謹**（存在唯一性 fence）。

**Ch10 Parametric Equations and Polar Coordinates** — *Role*：非直角座標下的微積分。含參數微積分/極座標/極座標面積/極座標圓錐。*Prereq*：Ch6–7；附錄 A.5（圓錐曲線）。*對應*：Stewart 10。*深度*：**標準嚴謹**。

**Ch11 Infinite Sequences and Series** —（**建議拆**：11a *Sequences & Numerical Series*／11b *Power Series & Taylor's Theorem*）*Role*：收斂理論與函數的級數表示。含數列/數項級數/斂散測試/冪級數/收斂半徑/Taylor 帶餘項。**須回收並一般化 Ch4 提前借用的級數機器**。*Prereq*：Ch1 極限、Ch4 收斂理論；附錄 A.3（幾何級數）、GAP-A（冪次和）、GAP-E（絕對值不等式，收斂半徑）。*對應*：Stewart 11。*深度*：**深理論核心**（測試與 Taylor 餘項當場證；重排/一致收斂等 fence）。

**Ch12 Vectors and the Geometry of Space** — *Role*：進入 3D／多變數的幾何語言。含 3D 座標/向量/點積/叉積/線與平面/二次曲面。*Prereq*：Ch10（座標經驗）；附錄 A.5（二次曲面建於圓錐）、GAP-C（叉積行列式）。*對應*：Stewart 12。*深度*：**標準嚴謹**。

**Ch13 Vector Functions** — *Role*：空間曲線的微積分。含向量函數微積分/弧長/曲率/運動。*Prereq*：Ch12、Ch6。*對應*：Stewart 13。*深度*：**標準嚴謹**。

**Ch14 Partial Derivatives** —（**可能需拆，sleeper**）*Role*：多變數微分。含多變數極限/連續/**可微性（嚴謹定義）**/偏導/多變數 chain rule/方向導數/梯度/Lagrange 乘子。*Prereq*：Ch12–13。*對應*：Stewart 14。*深度*：**深理論核心**（可微性定義當場嚴格；Clairaut 混合偏導對稱 fence 到補證處 GAP-D）。

**Ch15 Multiple Integrals** — *Role*：多變數積分。含二重/三重積分/極座標二重積分/柱球座標/變數變換 Jacobian。*Prereq*：Ch14、Ch6；GAP-C（Jacobian 行列式）。*對應*：Stewart 15。*深度*：**嚴謹設定＋最重的 fence**（一般變數變換定理給嚴謹陳述＋簡單情形，一般證明 fence）。

**Ch16 Vector Calculus** —（**建議拆**：16a *線積分/保守場/Green*／16b *面積分/Stokes/散度定理*）*Role*：向量場的積分定理，收尾多變數。含向量場/線積分/保守場/路徑無關/線積分基本定理/Green/面積分/Stokes/散度定理。*Prereq*：Ch13–15；GAP-C（旋度行列式）。*對應*：Stewart 16。*深度*：**嚴謹陳述＋一般定理 fence**（三大定理給嚴謹陳述＋簡單情形證明，一般證明 fence——嚴謹課程大一慣例）。

---

## 全局 seam ledger（2026-07-06 定案；hybrid front-load，因 Ch5–16 無手稿）

> **由來：** Ch5 起「無老師手稿」→ 產線改 **canon 為軸＋全閘**（比照附錄 A/B/C 無手稿先例、放大到 mainline 全閘）。使用者提「先定全書大綱再逐章寫」＋「Ch1–4 亦可動」。經 **Codex**（gpt-5.5／xhigh，唯讀，92.5k tok）第二意見＋兩支唯讀 subagent 撈底（Ch1–4 精確 export ledger／既有 arc 決策 digest）三方收斂 **front-load 薄骨架、細節 JIT**。完整裁決稿＋Codex 意見＋rationale：[`handout/_audit/REVIEW-fullarc-seam-skeleton.html`](handout/_audit/REVIEW-fullarc-seam-skeleton.html)。**除本節「export/import 契約」與跨章依賴外，一律 provisional。**

### 各章 provisional 節 roster（暫定、跟章可改）

- **Ch5**（Codex 重排：optimization 緊接 max/min、curve sketching 殿後綜合）：5.1 Implicit Differentiation｜5.2 Related Rates｜5.3 Linear Approximation &amp; Differentials｜5.4 Maximum and Minimum Values｜5.5 Optimization Problems｜5.6 Derivatives and the Shape of a Graph（凹性/拐點/二階判別法＝NEW）｜5.7 L'Hôpital's Rule（**export：Generalized MVT / Cauchy's form** lemma）｜5.8 Curve Sketching｜5.9 Newton's Method。排除原函數（→Ch6）；fold 候選＝5.3+5.9。§5.1 地雷：不寫一般 $F_x/F_y$（需 Ch14 偏導），operational/branch-based。
- **Ch6**：6.1 Areas &amp; Distances（import GAP-A）｜6.2 The Definite Integral｜6.3 FTC（當場證，**export FTC**）｜6.4 Indefinite Integrals &amp; Net Change｜6.5 Substitution。fence：連續⇒可積。
- **Ch7**：7.1 Areas Between Curves｜7.2 Volumes｜7.3 Shells｜7.4 Work｜7.5 Average Value｜7.6 Arc Length｜7.7 Surface Area。選材節制（7.4/7.5 或 7.6/7.7 可縮）。
- **Ch8**：8.1 by Parts｜8.2 Trig Integrals（A.2）｜8.3 Trig Substitution（GAP-F）｜8.4 Partial Fractions（A.4）｜8.5 Strategy｜8.6 Improper｜8.7 Approximate。inverse hyperbolic 可置此。
- **Ch9**：9.1 Modeling+direction fields｜9.2 Separable｜9.3 First-Order Linear｜9.4 Growth &amp; Decay（import Ch4 $y'=ky$）。first-order intro；fence 存在唯一性。
- **Ch10**：10.1 Parametric Curves｜10.2 Calculus w/ Parametric｜10.3 Polar｜10.4 Areas &amp; Lengths in Polar｜10.5 Conics in Polar（A.5）。
- **Ch11**（拆 11a/11b）：**11a** 11.1 Sequences（回收 Ch4 收斂機器）｜11.2 Series（A.3）｜11.3 Integral Test｜11.4 Comparison｜11.5 Alternating &amp; Absolute｜11.6 Ratio &amp; Root；**11b** 11.7 Power Series（GAP-E）｜11.8 Function Representations｜11.9 Taylor &amp; Maclaurin（餘項；import Ch5 Generalized MVT）｜11.10 Applications。fence：重排/一致收斂。
- **Ch12**：12.1 3D Coordinates｜12.2 Vectors｜12.3 Dot Product｜12.4 Cross Product（附錄 C）｜12.5 Lines &amp; Planes｜12.6 Quadric Surfaces（A.5）。
- **Ch13**：13.1 Vector Functions &amp; Space Curves｜13.2 Derivatives &amp; Integrals｜13.3 Arc Length &amp; Curvature｜13.4 Motion in Space。
- **Ch14**（sleeper，可能拆）：14.1 Functions of Several Variables｜14.2 Limits &amp; Continuity｜14.3 Partial Derivatives｜14.4 Differentiability &amp; Tangent Planes｜14.5 Chain Rule｜14.6 Directional Derivatives &amp; Gradient｜14.7 Max/Min（附錄 C.4；import Ch5 §5.6 二階判別法）｜14.8 Lagrange。fence：Clairaut→GAP-D。
- **Ch15**：15.1 Double over Rectangles｜15.2 over General Regions｜15.3 in Polar｜15.4 Applications｜15.5 Triple｜15.6 Cylindrical &amp; Spherical｜15.7 Change of Variables（Jacobian；附錄 C）。fence：一般變數變換。
- **Ch16**（拆 16a/16b）：**16a** 16.1 Vector Fields｜16.2 Line Integrals｜16.3 FTC for Line Integrals｜16.4 Green；**16b** 16.5 Curl &amp; Divergence（GAP-C）｜16.6 Parametric Surfaces｜16.7 Surface Integrals｜16.8 Stokes｜16.9 Divergence。fence：一般 Green/Stokes/散度。

### 跨章 export/import 契約（**非 provisional**；Ch1–4 號經撈底核對 built standalone、無 discrepancy）

**Ch1–4 提供、Ch5+ import 的關鍵 export（精確號）：** Limit laws **Thm 1.2**／Squeeze **Thm 1.3**／無窮極限 **Def 1.11**／ε-δ **Def 1.13**（Ch1）；可微⇒連續 **Thm 2.1**／power·product·quotient **Thm 2.3·2.6·2.7**／limit-form 可微性 **Def 2.3**（Ch2）；chain rule **Thm 3.3**／remainder-form 可微性 **Def 3.1**／arcsin·arccos·arctan 導數 **Ex 3.14·3.15·3.16**（Ch3）；完備性 **Thm 4.1**／Bolzano–Weierstrass **Thm 4.4**／Cauchy criterion **Thm 4.5**／EVT **Thm 4.9**〔陳述未證，見 §4.4 補寫〕／Fermat **Thm 4.10**／Rolle·MVT **Thm 4.11·4.12**／單調性·常數性 **Cor 4.3·4.4**／$(e^x)'$ **Thm 4.8**／$(\ln x)'$ **Thm 4.14**（Ch4）。**IVT ＝ 目前缺**（見 Ch4 Open questions「IVT/EVT 補嚴謹」決定；補後入 §4.4）。

**Ch5+ 新 export（forward 契約）：** Generalized MVT（Cauchy's form）§5.7 → Ch11 Taylor 餘項；linear approx／differentials §5.3 → Ch6 $du$·Ch11·Ch14 切平面；concavity／二階判別法 §5.6 → Ch14 Hessian（§C.4）；FTC §6.3 → Ch7–8·11·13·15–16；power-series/收斂機器 Ch4 提前借、Ch11 回收一般化；行列式/叉積/orientation 附錄 C → Ch12/14/15/16。

### 記號串接（Ch5–16 前瞻；權威落點仍為下節「跨章記號串聯」）

$dy,\ \Delta y$（微分 vs 增量，Ch5 §5.3 新）｜$dy/dt$（對時間，Ch5 §5.2 新）｜$\int,\ \int_a^b,\ \sum$（Ch6，Σ 先備 A.3）｜數列 $\{a_n\}$／Cauchy（Ch4→Ch11 回收）｜向量 $\mathbf v,\ \cdot,\ \times,\ \det$（Ch12／附錄 C）｜偏導 $\partial,\ \nabla$／Jacobian／orientation（Ch14–15／附錄 C）。

### fence / 附錄 hook 觸發 ＋ 跨 arc 待裁決（記觸發點，非現在阻塞）

| Hook / 決策 | 觸發章 | 現況 |
|---|---|---|
| GAP-A 冪次和 | Ch6 | **已建**（§A.3 retitle「Sigma Notation, Power Sums, and the Geometric Series」、Prop A.6） |
| GAP-B 複數 primer（A/B 類？收多深） | **Ch11**（Euler/複數應用；Ch9 first-order 不觸發） | **待裁**（§16.2 undefined；**唯一未建 GAP**） |
| GAP-C 行列式 | Ch12/15/16 | 已成 附錄 C |
| GAP-D Proof Track | Ch4 IVT/EVT 提前啟用；Ch6+ | 首批＝**EVT＋IVT＋連續⇒可積/uniform continuity**（Codex：同 compactness 群）；見上「Deferred Proofs」entry |
| GAP-E 絕對值不等式 | Ch11 | **已建**（新 §A.6「Absolute Value and Inequalities」、Prop A.8 三角不等式，2026-07-04） |
| GAP-F 完全平方 | Ch8/10/15 | **已建**（併入 §A.5 收尾段，2026-07-04） |
| 部分分式重編號 | Ch8 cite | §A.4 部分分式現為 **Prop A.7**（A.3 插入 Power sums Prop A.6 後移；本檔上文批二段的「Prop A.6」已 stale，Ch8 引用前以 as-built 為準） |
| Ch7 further-app 選材／折 | Ch7 | Codex：surface area 最易折 |
| Ch9 章名框 first-order | Ch9 | 建議採；Codex：勿混入二階/複數 |
| Ch14 是否拆（sleeper） | Ch14 draft 後 | Codex 強化傾向**拆 14a 微分／14b 最佳化與約束**；最終拆否仍 JIT |
| §1.2 反三角後移 | — | **維持現狀**（reconfirm keep 2026-07-06；兩輪仲裁已判主流放 Ch1） |

> **各章 blocking 前提/fence（Codex 全弧 seam-hunt，2026-07-06）：** Ch6 連續⇒可積(uniform continuity)＋`ln|x|`原函數；Ch7 積分均值(EVT+IVT)＋C¹弧長定理；Ch8 實多項式因式分解(FTA fact)＋§8.7誤差界需Taylor(Ch11)；Ch10 參數dy/dx局部可逆假設＋參數弧長定理(Ch13前)；Ch11 冪級數半徑LUB＋逐項微分/積分(uniform conv, proof-track)；Ch12 §12.3 export Cauchy–Schwarz；Ch14 多變數EVT＋二階Taylor(Hessian)＋Jacobian matrix/matrix chain rule＋Lagrange需IFT；Ch15 多變數可積性＋Fubini(與變數變換分開fence)；Ch16 reparametrization invariance＋curl-free⇒conservative需單連通＋正則參數曲面。**新增 forward export：** `ln|x|`(§6.4)、Cauchy–Schwarz(§12.3)、Jacobian matrix/matrix chain rule(§14)、Fubini/多變數可積(§15)。這些為各章 draft 時的 build/fence 清單，非現在阻塞。

---

## 跨章記號串聯

一份學生會翻回去查的微積分講義，需要記號一旦引入就保持穩定。首次做出決定時記錄在此；後續章節引用本節而非重新決定。

- `\arcsin` / `\arccos` / `\arctan` 是本書使用的 operator。`\sin^{-1}`、`\cos^{-1}`、`\tan^{-1}` 僅在首次警告 reciprocal 誤讀時出現在 caution box 中。
- Domain restriction 在適用於單一公式時以 inline 方式寫在 condition 區塊中；容易忘記時則移入 caution 區塊。HTML 對應的 markup 見 [`handout/CONTRACT-html-writing.md`](handout/CONTRACT-html-writing.md)。
- 方程式編號為 per-chapter（`(1.3)`、`(2.7)`），且僅在方程式被後續引用或為 formal statement 時出現（見 spec §6）。

*（後續章節引入新的慣例決策時擴展此列表。）*

---

## 講義–影片邊界（重複規則）

每一章的作者 **MUST** 驗證：

- 講義獨立成立。沒有影片的學生仍能完成本章。
- 影片不引入講義中不存在的 fact、definition 或 theorem。
- 影片可自由加入視覺直覺、節奏變化或替代的 worked example；這些是 reinforcement，不是 prerequisite。

存疑時，將事實從影片提升至講義，而非反向。

---

## 檢視路線圖

每當一章到達 `done` 後，回頭檢視本檔。典型的更新：

- 關閉該章的 `Open questions` 區塊，或將剩餘項目移入後續 issue。
- 更新從較早章節 forward-reference 到本章的 cross-reference。
- 檢查後續章節的 `Prerequisites` 區塊在任何結構調整後是否仍列出正確的先前章節。

如果整體弧線變更——例如兩章應合併、或某章應提前——在修改章節原始碼**之前**先更新本檔。路線圖是計畫；章節原始碼是實作。
