# ch07 三閘 gate-2 — record（數學／散文／圖，定版前跨模型複核）

> Raw working record（`_dev-archive`；Codex raw JSON 屬 ephemeral scratchpad、不進版控）。durable：`handout/html/_audit/REVIEW-ch07-gate2.html` ＋ `PLAN-ch07.md` 三閘 gate-2 列。
> 2026-07-18 · Codex **`gpt-5.6-sol` / `model_reasoning_effort=max`** · 三獨立 `codex exec -s read-only -C repo`（本對話 standing consent）· 涵蓋 M1–M4 全部 as-built（含 M3 散文/難度＋M4 Mode C 新內容）。
> **結果：數學 0 blocking／散文 0 blocking／圖 1 D7（使用者裁 B 輕修）→ 6 fixes 全落地＋回歸 → Ch7 三閘收斂。**

## 調用
- 數學：`--output-schema gate2-schema.json -o gate2-math-out.json - < gate2-math-prompt.txt`（rubric＝MATH-CORRECTNESS-RUBRIC M1–M8，讀 7 fragments；canon 章＝對數學真值/canon/內部一致判，非手稿）
- 散文：`gate2-prose-schema.json` / `gate2-prose-*`（rubric＝PROSE-AUDIT-RUBRIC U/F/S/A/V）
- 圖：`-i` 餵 23 PNG（Fig 7.1–7.23 順序，shot.mjs figures 2×）＋讀 fragment caption；rubric＝FIGURE-AUDIT-RUBRIC D1–D8/A1–A7

## 數學 M1–M8：0 blocking + 1 advisory（套用）
- **PASS**：M1/M2/M3/M4/M6/M7/M8 全乾淨。23 例最終答案＋Thm 7.1（shell）/7.2（積分均值 proved）/7.3（弧長 proved）/7.4（表面積 proved）四證皆判正確。特別複核的 M3/M4 新內容——§7.7 Thm 7.4 的 MVT→f'(ζ) Lipschitz＋averaging bridge、frustum 消元、§7.5 α/β「為何 [α,β]」、新 Ex 7.8 V=8π/15、avg-velocity 橋、Strategy 7.4——均無異議。
- **[G2M-1 M5 advisory → 套用]** Ex 7.15（圓錐水槽）：`r(y)/y = 2/4` 端點 y=0 除以零退化（答案不受影響，r(0)=0，被積式為 0）。→ 改 `r(y)/2 = y/4`（等價、無退化、對齊 Ex 7.9 體例）。sympy 複驗 W=77175π/2 不變。

## 散文 S·A·V：0 blocking + 4 advisory（全套用）
第二模型確認「M3/M4 承重橋接均成立」。U1–U5/F1–F2/F5/S/A/V 全乾淨；4 條皆 F3/F4 copyedit：
- **[G2P-1 F3]** §7.4 gravity 括號「opposite, negative, work」逗號串 → 重寫為「pulls against the motion and therefore does negative work; overcoming it…」。
- **[G2P-2 F3]** §7.6 Def 7.5 後（M3 時態句）「…7.2 and 7.6 — one already made, one still to come — it declares…」run-on → 斷兩句「…as Definition 7.2 and the forthcoming Definition 7.6. It declares…」。
- **[G2P-3 F3]** §7.7 開場「what sweeps out」缺 it → 「what it sweeps out」＋補逗號。
- **[G2P-4 F4]** §7.7 frustum 推導句（M4）過密 → 拆三句。**調和 M3 sim「show 消元」× prose「別擠」**。

## 圖視覺：1 D7 blocking（使用者裁 B）+ 22 clean
- **[G2F-1 D7]** **Fig 7.16 levelling-rectangle**：圖在 Ex 7.16 前，y=2 tick＋f_ave 標籤示 f_ave=2、caption 明寫「crosses at x=±1」→ 提前揭露 Ex 7.16（f_ave=2）＋Ex 7.18（c=±1）答案。source 確認（非小字誤讀）。
  - **對抗式裁定：邊界／偏軟**——D7 字面＝worked-example 圖，此為**定義示意圖**（Def 7.4 後）；後續 Ex 為示範非挑戰題；**canon 標準**（Stewart §6.5 同法）；M2 gate-1 曾複核（聚焦 D6 等積、未聚焦 D7）。
  - **使用者裁決 (B) 輕修 caption**：去掉明寫的「crosses at x=±1…left endpoint」句，改「…so the levelling rectangle and the region hold the same area.」（擋掉最強的 Ex 7.18 spoiler；f_ave 保符號；圖上 y=2 視覺按 (B) 接受＝canon 定義示意）。22 圖（7.1–7.15,7.17–7.23）clean。

## 雙閘價值（本輪）
gate-1（Claude，免費）三閘已 0 blocking；gate-2（Codex sol/max，第二模型）**確認**數學/散文 0 blocking（含 M3/M4 全部新內容），並在圖層提出一個 gate-1 未聚焦的 D7 角度（定義圖 spoiler）——經對抗式裁定為邊界、使用者取輕修。無 confirmed 數學/散文 blocking＝強結果；幻覺須穿過兩獨立模型。

## 落地驗證
6 fixes 全落地。rebuild ✔／linebreak 0／quote_lint clean ×7／render **math=1028、katex 0**／sympy 水槽 W 不變。皆 copyedit/notation（無難度變化）→ 無需 scoped 難度回歸。**三閘 gate-2 收斂 → Ch7 進 M5 收尾。**
