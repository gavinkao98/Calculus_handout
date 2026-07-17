# Ch 3 課文範例補充——選題稽核紀錄（Codex gate-2，version-controlled findings）

依 [`CONTENT_SOURCING.md`](../../../CONTENT_SOURCING.md) §流程 3.iii「裁決後過一輪選題稽核」建立。
契約沿用 [`CONTENT_DIRECTION.md`](../../../CONTENT_DIRECTION.md) ⑤：**math／faithfulness／aptness（對症性）＝blocking；source-license／format＝advisory**。
**findings 必須留版控**（Codex 原始輸出落在 gitignored `scratchpad/`、換機即失），故本檔保存 findings 原文＋triage 處置。

> **時序：** Mode C ①波 import（4 例，2026-06-26）→ 範圍限定 Mode B gate-1（Claude 三路，0 blocking／3 advisory，A2 已套）→ 本 **gate-2（Codex）跨模型獨立複核** → 採納 2 blocking 修正 → 手動回歸 PASS。

## 稽核設定

- **工具：** Codex CLI（`codex-cli 0.136.0`，PATH 上 npm 版；`codex exec -s read-only`，全程不改檔）。
  - 註：另一個絕對路徑 alpha 版（`%LOCALAPPDATA%\OpenAI\Codex\bin\codex.exe` 0.130.0-alpha.5）因 `config.toml` 的 `service_tier="default"` 與該版不相容而無法啟動；PATH 的 0.136.0 正常載入。PLAN-ch03 §6「本機無 node/codex」註記已過時（node v22＋codex 0.136 皆在 PATH）。
- **認證：** `codex login status` → 「Logged in using ChatGPT」——走 **ChatGPT 訂閱配額**，非 API key 計費（事前經使用者同意）。
- **模型／用量：** `gpt-5.5` @ `xhigh`（config 預設）；本次 **121,425 tokens**。
- **輸入：** prompt 以 bash `codex exec - < prompt.txt` 餵 raw UTF-8（避 PowerShell CJK 重編碼）；`--output-schema` 強制結構化（全欄 required、`additionalProperties:false`、`level`/`dimension`/`verdict` 用 enum）；`-o` 寫 last message。
- **ground truth：** Codex 自讀 `handout/fragments/ch03/sec-3-2.html`、`sec-3-3.html`、`PLAN-ch03.md`、`problem_banks/CLP1/.../prob_s2.9.tex`、`prob_s2.10.tex`——獨立於本 session 框架。
- **日期：** 2026-06-26。

## Findings（Codex 原始輸出，逐字）

```json
{
  "blocking_count": 2,
  "advisory_count": 0,
  "verdict": "needs_fixes",
  "summary": "I independently checked the four imports against the handout, PLAN D-boundaries, and CLP source. Source/license is correct: prob_s2.9.tex and prob_s2.10.tex both carry CC BY-NC-SA 4.0 headers, and prob_s2.10.tex:7 confirms CLP's log means natural log. Example 3.7 matches CLP prob_s2.9.tex:497-513 and re-derives correctly. Example 3.8 matches prob_s2.9.tex:12-52 and the sign reasoning is correct. Example 3.13's displayed derivative is correct on its stated positive domain and corresponds to the first three factors of prob_s2.10.tex:466-491 with log remapped to ln. Aptness and D-boundaries otherwise check out: the examples fill real gaps listed in the ledger/Mode C notes, stay within the allowed §3.2 derivative inventory, avoid product-rule reproving and implicit-diff framing, and are complete worked examples.",
  "findings": [
    {
      "example": "Example 3.6 (§3.2)",
      "dimension": "math",
      "level": "blocking",
      "issue": "The derivative is presented only on the x > 1 branch, but the stated function has another real differentiability interval.",
      "evidence": "The prompt asks to differentiate sqrt((x-1)/(x+2)) without restricting x. The solution gives 3/(2*sqrt(x-1)*(x+2)^(3/2)) with '(x>1)'. Re-derivation: q=(x-1)/(x+2), q'=3/(x+2)^2, so F'=3/(2*(x+2)^2*sqrt(q)) wherever q>0. The real derivative exists on (-inf,-2) union (1,inf). The simplification uses sqrt((x-1)/(x+2))=sqrt(x-1)/sqrt(x+2), only real-valid on x>1.",
      "fix": "Either restrict the problem to x>1 and disclose in the source marker, or give the unsplit derivative on (-inf,-2) union (1,inf), optionally followed by the x>1 simplification."
    },
    {
      "example": "Example 3.13 (§3.3)",
      "dimension": "faithfulness",
      "level": "blocking",
      "issue": "The adaptation adds a domain restriction that is not disclosed in the marker comment.",
      "evidence": "CLP prob_s2.10.tex:466 states the original 5-factor product with no stated domain. The handout changes the task to the truncated 3-factor product 'for x>0'. The marker discloses the 5->3 truncation and log->ln remap, but not the added x>0 restriction. That restriction matters because the solution splits ln y into ln(x+1)+2ln(x^2+1)+3ln(x^3+1), which needs positive factors as written.",
      "fix": "Amend the marker to disclose the added domain restriction, or adjust the statement to the intended domain and disclose that choice."
    }
  ]
}
```

## Triage（Claude 處置）

- **裁決：採納兩條 blocking（皆 Codex 自附 fix，成本極低、無爭議）。**
- **B1 — Example 3.6（math）→ 修。** 採 Codex option A（限定問題域）：題目由「Differentiate √((x-1)/(x+2))」改為「**…for \(x>1\)**」，使解末的 `(x>1)` 與題述域一致、不再 silently 丟 `x<-2` 支；marker 補揭露「stated for x>1 … the function is also differentiable on x<-2」。選 option A 而非 option B（給全域 unsplit 導數）是因本例教學焦點為 chain×quotient 機制，限定 x>1 較乾淨且與 CLP 官方答案形式（隱含 x>1）一致。
- **B2 — Example 3.13（faithfulness）→ 修。** marker 補揭露「**domain restricted to x>0 so all three log factors stay positive**」。CONTENT_SOURCING 要求所有改作（含本書自加的域限制）逐筆揭露；原 marker 只揭露 5→3 截斷與 log→ln，漏了 x>0。屬正當的 provenance 修補。
- **gate-1 vs gate-2 差異（雙模型閘的價值）：** 同樣兩處觀察，Claude gate-1 判 advisory（A1 域完整性、A3 x>0 保守）、Codex gate-2 判 blocking。採從嚴判定修正——兩條都讓內容更精確、零教學代價。**幻覺未穿過任一模型**（兩模型對 4 例的數學與來源結論一致，差別僅在 advisory↔blocking 的嚴格度）。
- **回歸審核（CLAUDE.md 2026-06-12）：** 修正屬外科手術級（一句題目限定＋兩處 marker，未動任何解法步驟），且正是 Codex 自附 fix → 手動比對確認兩 blocking 均解決、無新問題。build + render 自驗：Example 連續 3.1–3.16、0 KaTeX err、0 未渲染、7/7 圖 hydrate。依契約「Codex 或手動比對均可」，不另燒一次 Codex 複跑。

## 留證

- Codex 結構化輸出：上方 JSON（原 `scratchpad/codex_s3_out.json`＋`codex_s3_run.log`，gitignored scratch，已轉錄於此）。
- prompt／schema：`scratchpad/codex_s3_prompt.txt`／`codex_s3_schema.json`（gitignored scratch；要旨已記於本檔「稽核設定」）。
- gate-1（Claude 三路）原始裁決見套用報告 [`../../_audit/REVIEW-ch03-example-supplement-applied.html`](../../_audit/REVIEW-ch03-example-supplement-applied.html)。
