# Ch 4 數學正確性閘——gate-2 稽核紀錄（Codex 跨模型獨立複核，version-controlled findings）

依 [`../../_audit/MATH-CORRECTNESS-RUBRIC.md`](../../_audit/MATH-CORRECTNESS-RUBRIC.md)（M1–M8，「請查核 X」propose-only、手稿勝出、不確定降級）。
**findings 必須留版控**（Codex 原始輸出落在 gitignored `scratchpad/`、換機即失），故本檔保存 findings 原文＋triage 處置。範本沿用同目錄 [`ch04_figure-audit-gate2.md`](ch04_figure-audit-gate2.md)／ch03 的 [`ch03_math-audit-gate2.md`](../ch03/ch03_math-audit-gate2.md)。

> **時序：** 主流程 sympy／python 獨立重算（worked-example 數值＋尾界 (∗)）全 PASS → gate-1（Claude ×7：5 per-section 全 M1–M8＋1 worked-example 重算專員＋1 跨章 M6/M7/M8 一致性，每候選對抗式雙鏡頭 verify，**raw 候選 = 0**，**0 blocking/0 advisory**，裁決稿 [`../../_audit/REVIEW-ch04-math-audit.html`](../../_audit/REVIEW-ch04-math-audit.html)）→ 使用者授權（2026-06-27）→ 本 **gate-2（Codex）跨模型獨立複核** → **0 blocking/0 advisory，雙閘收斂**。

## 稽核設定

- **工具：** Codex CLI（`codex-cli 0.136.0`，PATH 上 npm 版 `/c/Users/Kao/AppData/Roaming/npm/codex`；`codex exec -s read-only -C <repo>`，全程不改檔）。
- **認證：** Logged in using ChatGPT——走 **ChatGPT 訂閱配額**（事前經使用者明確同意，2026-06-27）。
- **模型／用量：** `gpt-5.5`（config 預設 `model_reasoning_effort=xhigh`）；本次 **173,720 tokens**、單輪收斂（run1）。
- **輸入：** prompt 以 bash `codex exec - < prompt.txt` 餵 raw UTF-8（避 PowerShell CJK 重編碼）；`--output-schema schema_ch04_math.json` 強制結構化（全欄 required、`additionalProperties:false`、`verdict`/`status`/`severity`/`dimension` 用 enum、無 min/max）；`-o` 寫 last message。
- **ground truth：** Codex 自讀 `handout/_audit/MATH-CORRECTNESS-RUBRIC.md`、`CLAUDE.md`、`handout/_dev-archive/ch04/PLAN-ch04.md`（§3 D1–D9 邊界、§5 ledger）、`handout/fragments/ch04/sec-4-{1,2,3,4,5}.html`、手稿轉錄 `seed_ch04_s{1..5}.md`、signed legacy `legacy/tex_handout/chapters/ch04_exponential_logarithm.tex`——獨立於本 session 框架與 gate-1 裁決。被要求 INDEPENDENTLY RECOMPUTE 全部 Example 4.1–4.7 ＋尾界 (∗)＋指數律 6 步二項式重組＋(e^h−1)/h index-shift bound＋積律／反函數導數證明。
- **日期：** 2026-06-27。

## Findings（Codex 原始輸出，逐字）

```json
{
  "verdict": "converged",
  "blocking_count": 0,
  "advisory_count": 0,
  "per_dimension": [
    {"dimension":"M1","status":"clean","note":"Checked definitions of e^x, Cauchy sequence, extrema, ln x, and general powers; no incorrect definition found."},
    {"dimension":"M2","status":"clean","note":"Checked theorem/proposition hypotheses and conclusions, including completeness, continuity, Cauchy criterion, EVT/Rolle/MVT, derivatives, and log laws."},
    {"dimension":"M3","status":"clean","note":"Checked quantifiers, iff directions, existence statements, and limiting arguments; no reversal or quantifier defect found."},
    {"dimension":"M4","status":"clean","note":"Recomputed algebraic and analytic steps, including tail bounds, binomial reorganization, derivative bound, product law, and inverse derivative."},
    {"dimension":"M5","status":"clean","note":"Checked domains and side conditions: x>0 versus all real x, h nonzero and small, ln domain x>0, interval interiors, and a,b>0."},
    {"dimension":"M6","status":"clean","note":"Checked against manuscript seeds, PLAN boundaries, and signed legacy version; expansions are intentional or manuscript-faithful."},
    {"dimension":"M7","status":"clean","note":"Checked proof dependencies for circularity: exponent law before exp derivative, MVT before monotonicity, ln continuity before ln derivative."},
    {"dimension":"M8","status":"clean","note":"Checked worked-example answers and chapter summary claims; no erroneous computation or conclusion found."}
  ],
  "findings": [],
  "worked_example_recompute": [
    {"example":"Example 4.1","claim":"Partial sums P_k(1) for k=0..5 are 1.0000, 2.0000, 2.5000, 2.6667, 2.7083, 2.7167; P_10(1) is about 2.7182818 and e is about 2.7183.","recomputed":"P0=1, P1=2, P2=5/2=2.5, P3=8/3=2.6667, P4=65/24=2.7083, P5=163/60=2.7167; P10=2.718281801..., below e=2.718281828....","agrees":true},
    {"example":"Example 4.2","claim":"For f(x)=x^2 on [0,2], the MVT point is c=1.","recomputed":"Average slope is (4-0)/(2-0)=2; f'(x)=2x, so 2c=2 and c=1 in (0,2).","agrees":true},
    {"example":"Example 4.3","claim":"|sin a - sin b| <= |a - b| for all real a,b by the MVT.","recomputed":"If a!=b, apply MVT to sin on the interval between a and b: sin a - sin b = cos(c)(a-b), so absolute value is <= |a-b| since |cos c|<=1; a=b is trivial.","agrees":true},
    {"example":"Example 4.4","claim":"f(x)=3x-sin x has exactly one real root, x=0, and f'(x)=3-cos x.","recomputed":"f(0)=0. If another root existed, Rolle would give f'(c)=0, but f'(x)=3-cos x>=2>0 for all x. Hence exactly one root.","agrees":true},
    {"example":"Example 4.5","claim":"sin x is strictly increasing on [0, pi/4].","recomputed":"On (0,pi/4), (sin x)'=cos x>0; the strict MVT monotonicity corollary gives strict increase on [0,pi/4].","agrees":true},
    {"example":"Example 4.6","claim":"e^x is strictly increasing on all real numbers.","recomputed":"(e^x)'=e^x and e^x>0 for all real x; applying strict monotonicity on any closed interval [x1,x2] gives e^x1<e^x2 for x1<x2.","agrees":true},
    {"example":"Example 4.7","claim":"With a^x:=e^(x ln a), the laws a^x b^x=(ab)^x and (a^x)^y=a^(xy)=(a^y)^x hold for a,b>0.","recomputed":"a^x b^x=e^(x ln a)e^(x ln b)=e^(x(ln a+ln b))=e^(x ln(ab))=(ab)^x. Also ln(a^x)=ln(e^(x ln a))=x ln a, so (a^x)^y=e^(y x ln a)=a^(xy), symmetrically equal to (a^y)^x.","agrees":true}
  ],
  "overall_conclusion": "Gate-2 converges with gate-1: I found 0 blocking and 0 advisory mathematics-correctness findings. The manuscript/PLAN-protected omissions were not treated as defects, and the key computations requested all recompute correctly."
}
```

## Triage（Claude 處置）

- **裁決：converged，無 finding 可採納或駁回——不需任何內容修改。** Codex 獨立複核與 gate-1（Claude ×7）＋主流程 sympy／python 三方一致：§4.1–§4.5 的全部陳述、計算、假設、定義域限制、跨節／跨章引用在 rubric 下皆健全。
- **worked-example 重算逐項對齊：** Codex 自行重算 Example 4.1–4.7 七題、`agrees=true` 全數通過，且與 gate-1 重算專員＋主流程 sympy 數值完全一致（含 `P_10(1)=2.718281801 < e=2.718281828` 的下逼近、`min(3−cos x)=2`、指數律歸 0）。
- **雙閘收斂（雙模型閘的價值）：** 幻覺要穿過兩個獨立模型才會漏。本章 gate-1（Claude opus-4-8 ×7）與 gate-2（Codex gpt-5.5 xhigh）對 M1–M8 結論完全一致、皆 0 blocking 0 advisory；Codex 特別點名複核了依賴鏈無循環（指數律先於 exp 導數、MVT 先於單調性、ln 連續先於 ln 導數）與 manuscript/PLAN-protected 的刻意省略（a^r fence、EVT 不證、range (0,∞) 斷言）皆未誤判為缺陷。**收斂判準（blocking = 0）達成。**
- **無回歸審核需求：** 兩閘皆 clean、未套用任何修正，故無「修完回歸」一步（CLAUDE.md 2026-06-12 回歸規則僅適用於有 finding 被修的情形）。

## 留證

- Codex 結構化輸出：上方 JSON（原 `scratchpad/result_ch04_math.json`＋`codex_ch04_math.log`，gitignored scratch，已逐字轉錄於此）。
- prompt／schema：`scratchpad/prompt_ch04_math.txt`／`schema_ch04_math.json`（gitignored scratch；要旨已記於本檔「稽核設定」）。
- gate-1（Claude ×7）原始裁決＋ sympy 重算清單見裁決稿 [`../../_audit/REVIEW-ch04-math-audit.html`](../../_audit/REVIEW-ch04-math-audit.html)（gate-2 欄已回填 converged）。workflow run id `wf_ea8a0ceb-39a`。
