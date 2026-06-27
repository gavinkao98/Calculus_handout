# Ch 4 課文範例補充——選題稽核紀錄（Codex gate-2，version-controlled findings）

依 [`CONTENT_SOURCING.md`](../../../CONTENT_SOURCING.md) §流程 3.iii「裁決後過一輪選題稽核」建立。
契約沿用 [`CONTENT_DIRECTION.md`](../../../CONTENT_DIRECTION.md) ⑤：**math／faithfulness／aptness（對症性）＝blocking；source-license／format＝advisory**。
**findings 必須留版控**（Codex 原始輸出落在 gitignored `scratchpad/`、換機即失），故本檔保存 findings 原文＋triage 處置。

> **時序：** Mode C ①波 gate-1（五節 `example-supplement` 並行＋章層 completeness critic，皆 Claude、免費；`wf_a9a30cfa-c0e`）→ §4.1/§4.2/§4.3/§4.5 判 clean、§4.4 浮 2 候選（E1 Lipschitz 估計／E2 Rolle 反向根計數，皆 high）→ 使用者裁決**兩條都收** → 本 **gate-2（Codex）跨模型獨立複核** → **run1 直接收斂（0 blocking）** → import pass。

## 稽核設定

- **工具：** Codex CLI（`codex-cli 0.136.0`，PATH 上 npm 版；`codex exec -s read-only`，全程不改檔）。
- **認證：** `codex login status` → 「Logged in using ChatGPT」——走 **ChatGPT 訂閱配額**（事前經使用者同意計費）。
- **模型／用量：** `gpt-5.5` @ `xhigh`（config 預設）；本次 **74,207 tokens**（一輪）。
- **輸入：** prompt 以 bash `codex exec - < prompt.txt` 餵 raw UTF-8（避 PowerShell CJK 重編碼）；`--output-schema` 強制結構化（全欄 required、`additionalProperties:false`、`example`/`dimension`/`level`/`verdict` 用 enum）；`-o` 寫 last message。
- **ground truth：** Codex 自讀 `CLAUDE.md`、`handout/fragments/ch04/sec-4-4.html`、`sec-4-5.html`、`handout/_dev-archive/ch04/PLAN-ch04.md`、`problem_banks/CLP1/.../prob_s2.13.tex`——獨立於本 session 框架，逐行 `rg` 引證行號。
- **日期：** 2026-06-27。

## 審核對象（兩候選，gate-1 已過、使用者已裁決收）

- **4.4-E1**（Layer-2，high）：`Use the Mean Value Theorem to show that |sin a − sin b| ≤ |a − b|`。locus＝緊跟 Strategy 4.2／Example 4.2、Corollary 4.3 之前。source＝`[source: CLP-1 §2.13 (MVT) — bounded-derivative application variant]`，**解為本次撰寫**（CLP 原 `f(100)<100` 自參照 ODE 題超綱，改用 sin）。
- **4.4-E2**（Layer-2，high）：`How many real roots does f(x)=3x−sin x have?`。locus＝緊跟 E1。source＝`[source: CLP-1 §2.13 Procedural — “3x−sin x”]`（`prob_s2.13.tex:348`），輕改照搬論證骨架＋補一行 `f'(x)=3−cos x≥2>0`。

## Findings（Codex 原始輸出，逐字）

```json
{
  "blocking_count": 0,
  "advisory_count": 0,
  "verdict": "pass",
  "summary": "Both candidates are clean. E1’s MVT proof and bounded-derivative note are mathematically correct, use only Theorem 4.12 plus |cos c|<=1 at the proposed insertion point, and fill a different action than existing Examples 4.2-4.4. Its provenance is acceptable as a clearly disclosed CLP bounded-derivative application variant with authored solution, not a light rewrite. E2 matches the CLP source argument at prob_s2.13.tex lines 348-357, with a correct added bound f'(x)=3-cos x>=2>0; the CC BY-NC-SA 4.0 header is at lines 1-4. E2’s Rolle-based root-count pattern is distinct from §4.5 Corollary 4.4, which proves f'=0 implies constant.",
  "findings": []
}
```

## Triage（Claude 處置）

- **裁決：gate-2 run1 直接收斂（0 blocking／0 advisory／0 findings）——兩例皆清，無修正需採納。** 本章繼 §4.3 之後第二個 run1 全清的閘。
- **雙閘一致（雙模型閘的價值）：** gate-1（Claude 五節 example-supplement ＋ 章層 critic）與 gate-2（Codex gpt-5.5 xhigh）兩個獨立模型對兩例的數學、對症性、provenance、D-邊界結論完全一致——**幻覺未穿過任一模型**。Codex 額外獨立引證：E2 源在 `prob_s2.13.tex:348-357`、CC BY-NC-SA 4.0 header 在 `:1-4`、E2 與 §4.5 Cor 4.4 邏輯相異（`f'` 恆非零排第二根 vs `f'≡0` 得常數，方向相反）；E1 只用 Theorem 4.12＋`|cos c|≤1`、provenance 標「disclosed variant＋authored solution」恰當（非 light rewrite）。
- **provenance 微調（採 Codex 措辭，非 finding）：** Codex 明指 E1 應記為「disclosed variant with authored solution, **not a light rewrite**」。E1 的 review marker 本就標 `rewrite: 重寫（解為本次撰寫）`，與 Codex 判定一致；import pass 落地 marker 時沿用「authored solution / variant of CLP §2.13 bounded-derivative application」措辭。
- **回歸審核（CLAUDE.md 2026-06-12）：** 0 findings 無修正，回歸對象＝import pass 後的 render 自驗（編號連續、cross-ref 解析、0 KaTeX err）。依契約不另燒 Codex 複跑。

## 留證

- Codex 結構化輸出：上方 JSON（原 `scratchpad/codex_s44_out.json`＋`codex_s44_run.log`，gitignored scratch，已轉錄於此）。
- prompt／schema：`scratchpad/codex_s44_prompt.txt`／`codex_s44_schema.json`（gitignored scratch；要旨已記於本檔「稽核設定」與「審核對象」）。
- gate-1（五節 example-supplement ＋ critic）候選全文＋裁決見 [`ch04_example-supplement-review.html`](ch04_example-supplement-review.html)。
