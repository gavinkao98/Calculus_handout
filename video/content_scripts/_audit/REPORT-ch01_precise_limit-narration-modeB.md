# §1.6 (The Precise Definition of a Limit) — MiMo spoken narration · Mode B 稽核紀錄

> 路線：MiMo 旁白雙版（口語 single-source）。被審物：`content_scripts/ch01_precise_limit_narration_spoken.md`（版本 B，由 `ch01_precise_limit.spoken.yml` 經 `derive_spoken.py` 生成），對照基準＝正典 `storyboards/ch01_precise_limit.yml` 的 `say`。
> 稽核器：`codex exec -s read-only`（model gpt-5.5、reasoning xhigh）。prompt＝`PROMPT-ch01_precise_limit-narration-modeB.md`；原始輸出＝`REPORT-ch01_precise_limit-narration-modeB.raw.txt`。
> CONTENT_APPROVED = yes（§1.6 narration 內容先前已認可）；D1 跳過（本節無 Version A HTML）；D3／D7 全跑。

## 裁決總結

**VERDICT: 0 blocking, 2 advisory** → 兩條 advisory **皆採納**（均為 spell-out 引入的 tier-2 清晰度修正，外科式、忠實、未動 `{show}` 或內容）。

| # | 維度 | 單元 | 發現 | 裁決 | 動作 |
|---|---|---|---|---|---|
| 1 | D3 | `uniqueness_proof_triangle` | `\|L-f(x)+f(x)-M\|` 念成「the absolute value of L minus f of x, plus f of x, minus M」，絕對值範圍可能被聽成提早結束 | **Rewrite（採納）** | 整個四項群組改用「the absolute value of **the quantity** L minus f of x plus f of x minus M」綁定範圍 |
| 2 | D4 | `epsilon_delta_recipe` | 「Take the quantity the absolute value of f of x minus L」雖忠實但唸起來卡 | **Rewrite（採納）** | 同位語以逗號隔開：「Take the quantity**,** the absolute value of f of x minus L**,** and bound it above …」（僅加標點＝停頓，無改字） |

> 兩處同型的 `|L-f(x)|+|f(x)-M|`＝兩個獨立絕對值相加，維持「the absolute value of … , plus the absolute value of …」不動（正確且不混淆）。

## 其他維度

- **D2（忠實度）：** clean。英文散文逐字忠於正典 `say`（含正典刻意的「vertical / horizontal axis」用語）。
- **D5（念法慣例）：** 稽核建議維持現用慣例——`|x-a|`→「the absolute value of x minus a」（保留證明所需的代數形式）、複合不等式「zero is less than …, which is less than delta」、小數「zero point zero five」。已採納為本節定案，記於 `ch01_precise_limit.spoken.yml` 檔頭。
- **D6（MiMo 設定 sanity）：** clean。`mimo-v2.5-tts`、OpenAI 相容、voice `Mia`、`wav` 24kHz/mono/PCM16 內部一致。
- **D7（數學內容正確性，全跑）：** clean。獨立重推全部數值／代數皆通過：`|(2x-1)-5|=2|x-3|`、`0.1/2=0.05`、`0.01/2=0.005`、`|(4x-5)-7|=4|x-3|`、`4·(ε/4)=ε`、`|x-1|<1 ⟹ 0<x<2 ⟹ |x-4|<4`、`δ=min{1,ε/4}`、唯一性 `2ε=|L-M|` 與矛盾 `|L-M|<|L-M|`。

## 回歸審核（CLAUDE.md 要求）

兩處 Rewrite 已改入 source `ch01_precise_limit.spoken.yml` → 重跑 `derive_spoken.py --check` **parity OK**（`{show}` 結構、無 `$` 洩漏均維持）→ 重新生成 `_mimo.yml` 與 `_narration_spoken.md`。兩處修改僅動目標措辭／標點，未觸及 `{show}` 標記或數學內容，無引入新問題。
