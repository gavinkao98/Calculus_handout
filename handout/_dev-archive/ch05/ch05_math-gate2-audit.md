# Ch5 數學正確性閘 M1–M8 gate-2 稽核紀錄（Codex 跨模型，2026-07-07）

依 [`../../PIPELINE.md`](../../PIPELINE.md) M gate-2 風險判準，Ch5（標準嚴謹章）作為**抽樣層樣本章**執行跨模型全章複核。執行：`codex exec -s read-only`（standing consent；gpt-5.5 依 `~/.codex/config.toml`）；契約＝[`../../_audit/MATH-CORRECTNESS-RUBRIC.md`](../../_audit/MATH-CORRECTNESS-RUBRIC.md)；被審物＝ch05 全 9 節 as-built（Def 5.1–5.7、Thm 5.1–5.5、Strategy 5.1–5.7、Ex 5.1–5.27 含 M4 新增、Figure 5.1–5.11、appD §D.3 對照）。raw 落 gitignored scratchpad（依 raw 政策不進版控），本檔為完整轉錄。

## 首輪 VERDICT: 1 blocking, 0 advisory

- **[Blocking] [M7] `sec-5-8.html` asymptote caution（M4 2026-07-07 新增段）**
  - 原文：「Only a vertical asymptote is uncrossable at the point itself, because the function has no value there.」
  - 為何錯：垂直漸近線的定義只要求至少一側 \(f(x)\to\pm\infty\)（本書 Def 5.7、Ch1 Def 1.12），**不要求 \(f(a)\) 未定義**——可令 \(f(x)=1/x\)（\(x\ne0\)）並另行定義 \(f(0)=0\)：\(x=0\) 仍是 VA，但函數在該點有值。絕對化陳述與定義不一致。
  - 修法（已套用）：改為「Vertical asymptotes are different in kind: they mark places where the nearby values blow up, not lines the graph runs alongside — usually the function is not even defined there, and an isolated value assigned at that point changes nothing about the blow-up.」

清潔維度：M1 定義／M2 定理陳述／M3 量詞邏輯／M4 推導計算（含新增 Ex 5.14、5.22）／M5 邊界與定義域／M6 記號一致／M8 隱性假設——**全 clean**。

## 回歸複核（scoped，修復後）

VERDICT：**解除；未引入新的數學／定義一致性問題。** 「新文改成 usually 且明說 isolated value 不影響 blow-up，已符合 Def 5.7／Def 1.12 的 one-sided infinite limit 判準。」附一條 non-blocking 措辭註記（末句 “far end” 對 VA 略可誤讀，前句已區分——不動）。

## 收斂

**M gate-2 通過（blocking=0）。** 註記：本條 blocking 出自當日 M4 新增內容且已過 gate-1 層（sympy 驗數字、scoped Mode B 驗合規）——「sympy 只驗數不驗定理衛生」的既知缺口正由跨模型 gate-2 補上，雙閘價值的具體實證；一併作為抽樣層「被抽中章」的品質基線（1 blocking／章，源自增補非原稿）。
