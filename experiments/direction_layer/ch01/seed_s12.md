# Seed — §1.2 Inverse Trigonometric Functions（手稿轉錄）

> stage ① 產物。來源：老師掃描手稿 `chapter 1 manuscript`，p.5（第一條水平線後）–9（第二條水平線前）。
> **已人核對轉錄忠實度（①-verify，2026-06-04：OK）。** csc⁻¹／sec⁻¹ 的「微分友善」非標準值域已確認為手稿原意（使用者並裁定 ②③ 方向＝**照手稿非標準慣例**）；三角形 `tan(arcsin 1/3)=1/(2√2)` 與 sec⁻¹ 替代值域那行皆確認。忠於手稿，含刻意省略。

## §1.2 依賴（建立其上）
- §1.1 反函數：一對一、反函數定義、互消 `f⁻¹(f(x))=x`／`f(f⁻¹(x))=x`、域限使函數變一對一（§1.1 叉路 B 的 forward-ref 在此兌現）。
- 三角函數 `sin, cos, tan, csc, sec, cot` 及其圖形、`1+tan²=sec²`。

## 數學骨架（§1.2，照手稿順序）

- **[動機] 困難**：求反三角函數有「slight difficulty」——它們**不是一對一**（Ex：sin 波形＋水平線交多次圖）。**克服法：restrict the domain 使其變一對一。**

- **[arcsin] 反正弦**：
  - 對 `sin x`、`-π/2 ≤ x ≤ π/2`（圖：限制後的 sin 單調遞增）→ 此域上反函數存在，記 `sin⁻¹` 或 `arcsin x`，稱 inverse sine／arcsine function。
  - `sin⁻¹x=y ⟺ sin y=x`，`y∈[-π/2,π/2]`（即 `-π/2≤y≤π/2`）。
  - 當 `-π/2≤y≤π/2`，`sin y=x` 落在 `-1≤x≤1`。
  - **故 `sin⁻¹` 定義域 `-1≤x≤1`、值域 `-π/2≤y≤π/2`**。
  - **Ex①**：Evaluate `sin⁻¹(1/2)`。Sol：`sin⁻¹(1/2)=y ⟺ sin y=1/2 ⟺ y=π/6`，∴ `sin⁻¹(1/2)=π/6`。
  - **Ex②**：`tan(arcsin(1/3))`。令 `arcsin(1/3)=θ`（即 `sin θ=1/3`）→（直角三角形：對邊 1、斜邊 3、鄰邊 `2√2`）→ `tan θ = 1/(2√2)`。

- **[互消 Recall again]**：① `sin⁻¹(sin x)=x`，`-π/2≤x≤π/2`。② `sin(sin⁻¹x)=x`，`-1≤x≤1`。

- **[arccos] 反餘弦（定義方式類似）**：
  - `cos x`、`0≤x≤π` 時一對一（圖：限制後的 cos 單調遞減）→ 反函數記 `cos⁻¹` 或 `arccos`。
  - `cos⁻¹x=y ⟺ cos y=x`，`0≤y≤π`，且 `-1≤x≤1`。

- **[arctan] 反正切（the same）**：
  - `f(x)=tan x`、`-π/2<x<π/2`（圖：該域上的 tan）。
  - `tan⁻¹x=y ⟺ tan y=x`，`-π/2<y<π/2`，`-∞<x<∞`。

- **[Worked example] 化簡 `cos(tan⁻¹x)`**：
  - `y=tan⁻¹x`、`-π/2<y<π/2`，即 `tan y=x`，要求 `cos y`。
  - 用 `1+tan²y=sec²y` → `sec²y=1+x²` → `sec y=√(1+x²)`（或 `-√(1+x²)`，但 `-π/2<y<π/2` 時 `sec y>0`）。
  - → `cos y = 1/sec y = 1/√(1+x²)`。
  - （或：`tan y=x` →（三角形：斜邊 `√(1+x²)`、對邊 `x`、鄰邊 1）→ `cos y = 1/√(1+x²)`。）

- **[其餘反三角，列出，不常用]**：
  - ① `y=csc⁻¹x`（`|x|≥1`）`⟺ csc y=x`，★`y∈(0,π/2]∪(π,3π/2]`【請查核：非標準值域】。
  - ② `y=sec⁻¹x`（`|x|≥1`）`⟺ sec y=x`，★`y∈[0,π/2)∪[π,3π/2)`【請查核：非標準值域】。
  - ③ `y=cot⁻¹x`，`x∈ℝ`，`cot y=x`，`y∈(0,π)`。

- **[sec⁻¹ 值域選擇的理由]**：圖 `y=sec x`（含漸近線、分支）。
  - 手稿註：「(so for `sec⁻¹`, we also can choose `y∈[0,π/2)∪(π/2,π]`)」——即另有一個（較標準的）替代值域。
  - **選 `[0,π/2)∪[π,3π/2)` 的理由：differentiation formulas are simpler（微分公式較簡）。** ★（微分公式屬 Ch3，此處只給理由、不展開。）

## 手稿刻意省略／特徵（忠實記錄）
- **csc⁻¹／sec⁻¹ 值域為「微分友善」非主流慣例**（`[0,π/2)∪[π,3π/2)` 型），手稿自己也點出 sec⁻¹ 有替代值域 `[0,π/2)∪(π/2,π]`。★這是本節最該核的非標準點。
- 手稿**只畫「限制後的正向函數」圖**（restricted sin／cos／tan、sec），**不畫 arcsin／arccos／arctan 本身的圖**。
- worked example：**3 個**（`sin⁻¹(1/2)`、`tan(arcsin 1/3)`、`cos(tan⁻¹x)`）；兩個用直角三角形技巧。
- **不給反三角的導數公式**（只用「微分較簡」當 sec⁻¹ 選擇理由，forward 到 Ch3）。
- 記號：`sin⁻¹/cos⁻¹/tan⁻¹` 與 `arcsin/arccos/arctan` 並用；`csc⁻¹/sec⁻¹/cot⁻¹`。
- 無 history、無一般「反函數圖＝對 y=x 反射」回呼（雖 §1.1 已建立）。

## 對照 ground truth（評分用，非手稿）
既有 `chapters/ch01_foundations.tex` §1.2（L270–566）分四小節：inverse sine／inverse cosine／inverse tangent／remaining。ROADMAP key figure＝「restricted-domain trig graphs with principal intervals shaded」；common pitfalls＝「`sin⁻¹x` 非 `1/sin x`」「`arcsin(sin x)=x` 僅在 `[-π/2,π/2]`」；notation＝`\arcsin…\arccot`。本 seed 是手稿原貌；方向由 brief 決定。
