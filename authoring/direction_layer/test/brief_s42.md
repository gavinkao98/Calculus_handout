# §4.2 方向 brief（stage ②→③，已核可）

> 來源 seed：[`seed_s42.md`](seed_s42.md)（手稿 p.3–10）。stage ② Claude 提案、**stage ③ 人核可 2026-06-04**。
> 此 brief 是 **④ 擴寫的方向依據**、**⑤ 審查的 `direction-conformance` 對照**。

## 範圍與深度
- 擁有：e^x 在 ℝ 上連續、絕對收斂（工具）、指數律。
- e2 連續性、指數律：**照手稿全證**（手稿主軸、已 dense）。
- ★**Cauchy⟺convergent（③ 決定＝折衷）**★：陳述定理 ＋ 證 **trivial 方向**（convergent ⟹ Cauchy，三角不等式）＋ 一個 `remark` 點出「反向 ⟸ 等價於完備性、靠 Bolzano–Weierstrass」**但不細證 B-W／單調子序列**。→ **刻意偏離已簽核 §4.2（全展開）**。
- 依據：合 Stewart/Rogawski 高中自學語域；合「多頁證明需明確授權」規則（B-W 多頁、未授權）。

## 承重直覺
- 領頭：「**無窮級數用有限多項式 `P_k` 逼近、再控尾項**」——本節與 §4.3 的 workhorse，升格成具名 `remark`。
- 絕對收斂：絕對級數單調 → 完備性給極限；`|S_m−S_n|≤|尾|` 轉移控制。

## worked example（手稿 0 個 → 補）
1. 指數律數值檢核 `e·e vs e²`（低風險錨）。
2. 一個絕對收斂具體例（如 `Σ(−1)^n/n!` 絕對收斂）。
- 序：動機 → 技巧 → 指數律 → 數值檢核。同型第二例跳過已建立 setup。

## history／application
- **都 skip**（留白勝過 padding）。history（Euler／e 起源）屬 §4.1 定義 e 之處；application（成長衰變）屬後章。§4.2 是 rigor 節。

## 強調／takeaway
- 樞紐：指數律 `e^x e^y=e^{x+y}` 現在是**定理**（非假設），靠多項式逼近＋絕對收斂掙來。
- 技能：尾界／多項式逼近技巧。

## 刻意不寫
- **完整 Bolzano–Weierstrass＋單調子序列證明**（③ 決定不寫；若 ④ 寫了＝direction 違規，⑤ 應擋）。
- 不重證 §4.1 收斂（引用）。
- 不漂進一般實分析（limsup、一般級數判別法）。

## 篇幅帶
- ≈ **150–180 .tex 行**（折衷路線）；對照：簽核版全展開 287 行。

## 記號
- 手稿用 `C^n_k`／`P_k`；本書慣例 `\binom{n}{k}` —— 首用 `caution` 雙記號（per ROADMAP 記號線）。
