# Ch5 example import record（M4 gap-check，2026-07-07）

依 [`../../../CONTENT_SOURCING.md`](../../../CONTENT_SOURCING.md) Provenance 規則記錄本輪匯入。選題稽核＝M4 Codex 裁決（read-only，standing consent；raw 落 session scratchpad，裁決全文轉錄於 [`../../_audit/REVIEW-ch05-modec-gapcheck.html`](../../_audit/REVIEW-ch05-modec-gapcheck.html)）。

## Example 5.22 — \(\lim_{x\to0^+}\ln x / x\)（題庫匯入）

- **來源**：CLP-1 §3.7 problem "2010H"（`problem_banks/CLP1/latex/problembook/problems/prob_s3.7.tex` L97–115），官方完整解含「誤用 L'Hôpital 得錯號」remark。
- **授權**：CC BY-NC-SA 4.0 ✓（與本書 BY-NC-SA 相容）。
- **官方解摘要**：form check → num→−∞、den→0⁺ → 非不定形 → −∞；remark 演示盲套 L'Hôpital 得 (1/x)/1→+∞ 之誤。
- **改作差異**：log→ln 記號；語域改本書 Stewart/Rogawski 課文體；補一句與 Example 5.21（x→∞ 同式合法情形）的對照與「property of the point」收束。**數學實質零更動**。
- **驗證**：sympy `limit(log(x)/x, x, 0, '+') = -oo`、`limit(1/x, x, 0, '+') = +oo`、`limit(log(x)/x, x, oo) = 0`（2026-07-07）。
- **落點**：`sec-5-7.html`，Ex 5.21（growth comparison）之後；編號 cascade 見下。

## Example 5.14 — 分類 \(x^{3/5}(4-x)\) 的臨界點（AI 自撰，audit-approved）

- **來源**：AI 自撰——緊扣 running example（Ex 5.11）的延伸，兌現其明文承諾 “settled below”；CONTENT_SOURCING「AI 備援」正當情形（題庫無對症：CLP-1 §3.5.1 的 singular-point 題分類法與本書 Def 5.4 相衝、且無法兌現對該函數的承諾）。
- **稽核**：M4 Codex 裁決 ADOPT（理由：讀者可見的契約破口＋Thm 5.1 兩個未演假設——f′ DNE 情形與第三 bullet「neither」）。
- **驗證**：sympy 數值恆等 f′≡4(3−2x)/(5x^{2/5})（max err 9e-16）、f(3/2)≈3.1886、f′(3/2)=0、符號型態 ＋/＋（x=0 neither）與 ＋→−（x=3/2 local max）（2026-07-07）。
- **落點**：`sec-5-4.html`，Ex 5.13 之後。

## 編號 cascade（一次到位；Codex 終表）

新 5.14（§5.4）→ 舊 5.14–5.20 → **5.15–5.21**；新 5.22（§5.7）→ 舊 5.21–5.25 → **5.23–5.27**。全章 as-built＝**Ex 5.1–5.27**。受影響引用（figcaption ×4、各節 header ledger、FIGS 程式註解）已同步；`grep env-num` 連續性驗證通過（27 例無跳號）。
