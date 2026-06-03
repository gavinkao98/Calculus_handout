# Seed — §1.1 Inverse Functions（手稿轉錄）

> stage ① 產物。來源：老師掃描手稿 `chapter 1 manuscript`，p.1–5（§1.1 範圍，至第一條水平分隔線）。
> **已人核對轉錄忠實度（①-verify，2026-06-04：OK；唯一修正＝f₂ 圖軸標為 `a`、`b`）。** 忠於手稿，含手稿刻意的省略。

## §1.1 依賴（建立其上）
- 前置微積分函數觀念：函數 `f(x)` 在定義域每一點指派一個值；定義域、值域、圖形。
- 基本代數：解方程式、開立方根 `x^{1/3}`。

## 數學骨架（§1.1，照手稿順序）

- **[Recall] 函數**：`A function f(x) assigns a value at every point x.`
  - Ex①：`f(x)=x`, `x∈[0,1]`（`0≤x≤1`）；`f(0)=0, f(1/2)=1/2, f(1/8)=1/8`。
  - Ex②：`f(x)=x²`, `x∈[-1,1]`（`-1≤x≤1`）；`f(0)=0, f(1/2)=1/4, f(-1/2)=1/4`。
    （箭頭圖：`0↦0`、`1/2↦1/4`、`-1/2↦1/4`——兩個輸入到同一輸出。）

- **[動機] 反方向**：反函數＝把 `f` 的值域當定義域、看反方向。`f(x₁)=y₁` ⟹ `f⁻¹(y₁)=x₁`。
  （圖：`x₁ —f→ y₁`，`f⁻¹` 把 `y₁` 帶回 `x₁`。）

- **[障礙] 不是每個 f 都有反函數**：由上兩例——Ex① `f` 從不取同值兩次；Ex② `f(1/2)=f(-1/2)=1/4`，故**無法定義** `f⁻¹(1/4)=?`。

- **[Def] 一對一（one-to-one）**：`f(x₁)≠f(x₂) whenever x₁≠x₂` 的函數稱為 one to one function。
  （手稿邊註：`use example 身分證 number ⟹ student`——身分證號對學生為一對一的真實例。）

- **[幾何] 水平線檢驗（horizontal line test）**：看 `f` 的圖形。若一條水平線與圖形交於**多於一點**，則有 `x₁≠x₂` 使 `f(x₁)=f(x₂)`（可能更多）。
  （圖：`f₁` 單調——水平線交一次；`f₂` 起伏——水平線交多次，x 軸標 `a`、`b`。）

- **[判準] one-to-one ⟺ 無水平線交圖多於一次**：`A function is one to one if and only if no horizontal line intersects its graph more than once.`（手稿直接由幾何陳述，**未另證**。）

- **[Def] 反函數**：設 `f` 為一對一，定義域 `A`、值域 `B`。則反函數 `f⁻¹` 有定義域 `B`、值域 `A`，由下式定義：
  `f⁻¹(y)=x ⟺ f(x)=y`，for any `y∈B`。
  即 `f` 把 `x` 映到 `y`，則 `f⁻¹` 把 `y` 映回 `x`。
  - Ex①：`f(x)=x` ⟹ `f⁻¹(x)=x`。
  - Ex②：`f(x)=x³` ⟹ `f⁻¹(y)=y^{1/3}`，即 `f⁻¹(x)=x^{1/3}`；`⟺ f(x^{1/3})=(x^{1/3})³=x`。

- **[Rmk] 變數改名**：聚焦 `f⁻¹` 時，習慣用「`x`」當其變數，即 `f⁻¹(x)=y ⟺ f(y)=x`。

- **[性質] 互消（cancellation）**：
  - for every `x∈A`，`f⁻¹(f(x))=x`。（圖：`x —f→ f(x) —f⁻¹→ x`。）
  - for every `x∈B`，`f(f⁻¹(x))=x`。（圖：`y —f⁻¹→ x —f→ y`。）

- **[Strategy] 求反函數三步法**（手稿原話：一般而言 `f⁻¹` 很難直接寫出）：
  - step 1：寫 `y=f(x)`。
  - step 2：把此方程式**解出 `x`（用 `y` 表示）**。
  - step 3：要把 `f⁻¹` 表成 `x` 的函數，**對調 `x` 與 `y`**。

- **[Worked example] 求 `f(x)=x³+2` 的反函數**：
  - ① `y=x³+2` ⟹ `x³=y-2` ⟹ `x=(y-2)^{1/3}`。
  - ② 對調：`y=(x-2)^{1/3}`。
  - ③ `f⁻¹(x)=(x-2)^{1/3}`。
  - （check：`f(f⁻¹(x))=f((x-2)^{1/3})=((x-2)^{1/3})³+2=x-2+2=x`。）

## 手稿刻意省略／特徵（忠實記錄）
- 水平線檢驗判準：**只幾何陳述、未證**。
- **無「對 `y=x` 反射」圖**：手稿只有箭頭圖、反方向圖、兩張水平線檢驗圖、兩張互消圖；**沒有**反射圖（這點與既有 ch01／ROADMAP 的 key figure 不同——見下對照）。
- worked example：**1 個完整**（`x³+2`）＋ 內嵌小例（`x`、`x³`）。
- 動機散文：少；無 history、無 caution box、無 application（除身分證號邊註）。
- 互消性質 `f⁻¹(f(x))=x` 與三步法之間，手稿用「So, when we know f is one to one, we can try to use the following …」銜接。
- 記號：`f⁻¹`、定義域 `A`／值域 `B`。

## 對照 ground truth（評分用，非手稿）
既有 `chapters/ch01_foundations.tex` §1.1（L16–269）分三小節：One-to-one functions／Inverse functions／Finding the inverse of a function。含**對 `y=x` 反射圖**與 inverse-composition 圖（ROADMAP key figures）、strategy box「finding an inverse function」。本 seed 是手稿原貌；方向由 brief 決定。
