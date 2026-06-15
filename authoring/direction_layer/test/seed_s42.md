# Seed — §4.2 Continuity and the Exponent Law for e^x（手稿轉錄）

> stage ① 產物。來源：老師掃描手稿 `2023-11-4-ExponentialFunction`，p.3–10（§4.2 範圍）。
> **已人核對轉錄忠實度（①-verify，2026-06-03：沒問題）。** 忠於手稿，含手稿刻意的省略。

## §4.1 依賴（§4.2 建立其上）
- `e^x := Σ_{n≥0} x^n/n!`（先對 x>0 定義）；`0!:=1`。
- 完備性：單調有界數列收斂（遞增有上界／遞減有下界）。
- 尾界：`0<x<L, k>n0>2L` 時 `0 ≤ e^x − P_k(x) ≤ L^k/k! ≤ (L^{n0}/n0!)(1/2)^{k−n0}`，其中 `P_k(x)=Σ_{n=0}^k x^n/n!`。

## 數學骨架（§4.2）
- **[e2] e^x 在 x>0 連續**：`lim_{x→x0} e^x = e^{x0}`。證：同一 `P_k` 逼近 e^x 與 e^{x0}；`k>n0>2(x0+1)` 使尾項<ε；P_k 為多項式故連續 → ∃`δ<min{x0/2,1/2}`；三段拆 `e^x−e^{x0}=(e^x−P_k)+(P_k(x)−P_k(x0))+(P_k(x0)−e^{x0})` → `|e^x−e^{x0}|<3ε`。
- **[e3]** `0<e^y<∞` for y<0（陳述）。
- **(△) Property**：`Σ|a_n|<∞ ⟹ Σa_n 收斂`。（Σa_n 收斂＝`S_k=Σ_{n≤k}a_n` 收斂。）
- **[Def] Cauchy 序列**：∀ε>0 ∃N0，`|a_m−a_n|<ε ∀m,n≥N0`。
- **[Thm] 收斂 ⟺ Cauchy。** ★手稿原文：**"For the moment, we shall not prove this theorem."** —— 手稿刻意不證，只陳述後直接用。★
- **(△) 之證明（援用上 Thm）**：`S_n=Σ_{k≤n}a_k`；`Σ|a_k|<∞` → m>n>N0 時 `|S_m−S_n|≤Σ_{k>n}|a_k|<ε` → `{S_n}` Cauchy → 收斂。
- **延拓 x<0**：`|e^y|≤Σ|y|^n/n!≤e^{|y|}<∞`；`|e^y−P_k(y)|≤|y|^k/k!`（`k>n0>2|y|`）。配 (△) → e^x 定義於全 ℝ。
- **[Thm] 指數律 `e^x e^y=e^{x+y}`**（x,y∈[−L,L], `k>n0>8L`）：`P_k(x)P_k(y)=(I)+(II)`；二項式 `C^n_k:=n!/(k!(n−k)!)` → `(I)=P_k(x+y)`；`|(II)|≤Σ_{l=k+1}^{2k}(|x|+|y|)^l/l! ≤ (2L)^{n0}/n0!(1/2)^{k−n0}`；telescope `e^x e^y−e^{x+y}` 成四項、逐項以尾界+`|e^?|≤e^L` 控制 → →0（k→∞）；[−L,L] 後 L→∞ 推全 ℝ。
- **Summary**：`e^x:=Σx^n/n!`（x∈ℝ）連續且 `e^x e^y=e^{x+y} ∀x,y`。

## 手稿刻意省略／特徵（忠實記錄）
- **Cauchy⟺convergent 的證明：手稿明白 punt**（"we shall not prove"）。
- worked example：**0 個**。圖：**0**。動機散文：**極少**。caution／strategy／名結果索引：**無**。
- 記號：二項式 `C^n_k`；部分和 `P_k`。

## 對照 ground truth（評分用，非手稿）
已簽核 `chapters/ch04_exponential_logarithm.tex` §4.2（L167–453）走「**展開** Cauchy⟺convergent 成完整 Bolzano–Weierstrass＋單調子序列」路線（當初 user-directed）。本 seed 是手稿原貌；方向由 brief 決定。
