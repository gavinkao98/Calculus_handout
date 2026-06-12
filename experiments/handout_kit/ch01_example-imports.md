# Ch 1 課文範例補充——import 紀錄（provenance／改作審計軌跡）

依 [`CONTENT_SOURCING.md`](../../CONTENT_SOURCING.md) §Provenance 與標記建立。
記錄 2026-06-12 import 的 21 筆 worked examples 之來源、授權、解材出處與改作差異，
供日後覆核。裁決＝核心 15＋選收 6 全收（使用者 2026-06-12）；選題稽核見
[`ch01_example-supplement-audit.md`](ch01_example-supplement-audit.md)。

**解材出處三型：**
- **official**：題庫附完整官方 solution，本書版為其改寫（換語域／記號／合併）。
- **authored**：題庫只附最終答案或指示，solution 為本次撰寫。
- **recomputed**：依本書約定重算，結論與題庫官方解不同（需重點覆核）。

授權：CLP-1＝CC BY-NC-SA 4.0（逐檔檔頭）；APEX＝CC BY-NC 4.0；Mooculus repo＝
CC BY-NC-SA 4.0（`mooculus/license.md`）；Stitz-Zeager（經 Mooculus 轉收）＝
CC BY-NC-SA（`10_06_ex_131-154.tex` 檔頭）。全 NC 家族，可 remix 進掛 CC BY-NC-SA 4.0
的免費講義。

---

## §1.1（sec-1-1.html）

| 例號 | 來源 | 解材 | 改作差異 |
|---|---|---|---|
| Example 1.3 | `[source: Mooculus digInInversesOfFunctions L293]` | authored | 原為 selectAll 互動題（x, x², x³−4x, x³+4 選一對一）；改為求證 h=x³−4x 非一對一（給 h(0)=h(2)=0 反例）、k=x³+4 一對一（cube-root 論證），並加教學收尾句。 |
| Example 1.5 | `[source: Mooculus digInInversesOfFunctions L407–453]` | official | 原為 worked example（x² 限制 [0,∞) 求 √x）；保留數學，換 Stewart 語域，加 forward reference 到 §1.2，配新 Figure 1.3。 |
| Example 1.7 | `[source: APEX §2.7 #7]` `APEXCalculusV5/exercises/02_07_ex_07.tex` | authored | APEX 僅給函數對與「compose 雙向驗證」指示；solution（求 f⁻¹=（5x+3)/x、雙向組合、定義域配對說明）為本次撰寫。 |
| Example 1.8 | `[source: Mooculus digInInversesOfFunctions L181–227]` | official | 原為攝氏↔華氏 worked example；保留，換語域，補 f⁻¹(f(t))=t 驗證步驟。 |

## §1.2（sec-1-2.html）

| 例號 | 來源 | 解材 | 改作差異 |
|---|---|---|---|
| Example 1.10 | `[source: CLP-1 §2.12 #1 (a)(c)]` `CLP1/latex/problembook/problems/prob_s2.12.tex:14` | official | 取原題 (a) arcsin(cos x)、(c) sin(arccos x)（捨 (b) arccsc(cos x)）；官方詳解改寫，加「inner/outer」模式收尾句。 |
| Example 1.11 | `[source: CLP-1 §2.12 #2]` `prob_s2.12.tex:38` | official | 粒子高度 cos t、arccos(1) 主值陷阱；官方詳解改寫，保留變數與時點。 |
| Example 1.12 | `[source: Stitz-Zeager via Mooculus 10_06_ex_131-154.tex]` | authored | 原為 14 小題精確值清單（僅附答案）；選 3 題（sin(arccos(−½))、sec(arctan 10)、tan(arcsin(−2√5/5))），solution 的象限／三角形論證為本次撰寫。 |
| Example 1.14 | `[source: CLP-1 §2.12 #5]` `prob_s2.12.tex:155` | **recomputed** | **重點覆核**：原題 arcsin x + arccsc x domain；CLP 官方解用標準 arccsc 主值得 f(−1)=−π。本書依 Definition 1.6 的非標準主值 y∈(0,π/2]∪(π,3π/2] 重算 arccsc(−1)=3π/2，故 f(−1)=π。差異本身轉為 Remark 1.4 的教學點。Codex 稽核已獨立驗算 f(−1)=π 正確。捨原題 differentiability 部分。 |

## §1.3（sec-1-3.html）

| 例號 | 來源 | 解材 | 改作差異 |
|---|---|---|---|
| Example 1.15 | `[source: CLP-1 §1.3 #1]` `prob_s1.3.tex:12` | official | 讀圖求三極限（含 lim≠f(a)）；官方詳解改寫。原 TikZ 圖重畫為 Figure 1.9（`figures.js` `read-limit-graph`：三次曲線過 (−2,1)、(0,0)、趨 (2,2) 空心，(2,−2) 實心）。 |
| Example 1.16 | `[source: CLP-1 §1.3 #5]` `prob_s1.3.tex:147` | official | 構造 lim=10、f(3)=0 的曲線；官方「many answers」解改寫為文字描述（學生自繪，無附圖）。 |

## §1.4（sec-1-4.html）

| 例號 | 來源 | 解材 | 改作差異 |
|---|---|---|---|
| Example 1.19 | `[source: CLP-1 §1.3 #8, #9]` `prob_s1.3.tex:209,222` | official | 兩題合一：已知雙側推單側／已知單側資訊不足；官方詳解改寫。 |
| Example 1.22 | `[source: CLP-1 §1.3 #13, #14, #15]` `prob_s1.3.tex:275,285,299` | official | 1/x 單側＋雙側 DNE，對照 1/x²＝∞；官方三題詳解合併改寫，`log` 改 `ln` 未涉及（原為 1/x 不含 log）。 |
| Example 1.24 | `[source: CLP-1 §3.6.1 #1]` `prob_s3.6.1.tex:11` | official | 分母為零不保證鉛直漸近線（g=1 vs g=x²−9 兩反例）；官方詳解改寫。 |

## §1.5（sec-1-5.html）

| 例號 | 來源 | 解材 | 改作差異 |
|---|---|---|---|
| Example 1.26 | `[source: CLP-1 §1.4 #42]` `prob_s1.4.tex:884` | official | 抽象用 limit laws（已知 lim f=−1 求複合極限＝−4）；官方詳解改寫。 |
| Example 1.28 | `[source: CLP-1 §1.4 #2, #5]` `prob_s1.4.tex:28,66` | official | 兩題合一：構造 0/0→10、列舉所有可能值；官方詳解改寫，加「indeterminate」收尾句。 |
| Example 1.31 | `[source: CLP-1 §1.4 extra]` `prob_s1.4.tex:751` | official | 通分化簡 t→½，答 −32/9；官方詳解改寫。 |
| Example 1.36 | `[source: CLP-1 §1.4 #43]` `prob_s1.4.tex:898` | official | 反推常數 a=7/2 使極限存在再求值 1/6；官方詳解改寫，加「existence forced a」收尾句。 |

## §1.6（sec-1-6.html）

| 例號 | 來源 | 解材 | 改作差異 |
|---|---|---|---|
| Example 1.38 | `[source: APEX §1.2 #1, #2]` `01_02_ex_01.tex`,`02.tex` | official | 診斷寫錯的 ε-δ 定義（量詞順序＋蘊含方向）；APEX 答案（兩句）擴寫為完整說理。 |
| Example 1.39 | `[source: APEX §1.2 #3]` `01_02_ex_03.tex` | official | 常數函數 lim 5＝5，任何 δ 皆可；官方證明改寫。 |
| Example 1.42 | `[source: APEX §1.2 #8]` `01_02_ex_08.tex` | official | 借 \|sin x\|≤\|x\| 證 lim sin x＝0；官方證明改寫，加連到 squeeze 的收尾句。 |
| Example 1.43 | `[source: AI]` | **authored (AI)** | 題庫無乾淨候選；M-δ 證 lim 1/x²＝∞（取 δ=1/√M），與 Example 1.21 首尾呼應。使用者 2026-06-12 授權 AI 出題，Codex 稽核驗算通過。 |

---

## 編號位移總表（kit 無自動編號，手動稅）

- **Examples**：原 22 個（1.1–1.22）＋新 21 個＝43 個（1.1–1.43）。位移對照見各 `sec-*.html`
  檔頭註解與 git diff。prose 內無 example 編號交叉引用（已 grep 確認），故無連帶 prose 改動。
- **Figures**：原 11 個＋新 2 個（Fig 1.3 restrict-x2、Fig 1.9 read-limit-graph）＝13 個。
  位移：§1.2 全部 +1、§1.3 的 1.7→1.8、§1.4 全部 +2、§1.6 的 1.11→1.13。prose 圖引用
  8 處＋figcaption 已全部同步（grep 核對 1.1–1.13 連續、交叉引用全解析）。
- **不位移**：所有 definition/theorem/proposition/remark/caution/strategy 編號（未插入此類環境）。
  `Definition 1.11` 等 prose 引用維持正確。

## 渲染驗證（2026-06-12，print standalone，Preview MCP）

43 examples、13 figures 全 hydrate、0 MathJax 錯誤、0 未渲染數學式、分頁 35 頁 A4。
兩幅新圖目視確認（Fig 1.3 兩曲線為 y=x 鏡射＋虛線；Fig 1.9 空心/實心點正確）。
