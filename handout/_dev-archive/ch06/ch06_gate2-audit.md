# ch06 三閘 gate-2 — raw record（數學／散文／圖，定版前跨模型複核）

> Raw working record（`_dev-archive` 不進版控）。durable：`handout/_audit/REVIEW-ch06-gate2.html` ＋ `PLAN-ch06.md` 三閘 gate-2 列。
> 2026-07-11 · Codex **`gpt-5.6-sol` / `model_reasoning_effort=max`** · 三獨立 `codex exec -s read-only`（standing consent）· **三閘 = 0 blocking（fixes 套用＋回歸畢）→ Ch6 定版**。

## 調用
- 數學：`--output-schema gate2-schema.json -o gate2-math-out.json - < gate2-math-prompt.txt`（rubric＝MATH-CORRECTNESS-RUBRIC，讀 5 fragments）
- 散文：同 schema，`gate2-prose-*`（rubric＝PROSE-AUDIT-RUBRIC）
- 圖：`-i g-riemann… g-velocity-signed-area`（9 PNG，Fig 6.1–6.9 順序），free-text per-figure

## 數學 M1–M8：1 blocking + 1 advisory（皆修）
- **[M4 blocking] Fig 6.2 caption**（sec-6-1）：原「overshoot above the curve — a single end strip of width 1/n」把 R−A（曲線上方 overshoot，分布在每子區間，=1/(2n)+1/(6n²)）與 R−L gap（=1/n，單一末端長條）混為一談。**確認為真**。→ 改 qualitatively 正確、不 forward-ref Ex 6.2、不洩 A：「the rectangles overshoot the curve on every strip, but by less and less as n grows…」。
- **[M7 advisory] §6.1 Σi² cross-ref**：「proved by **induction**」，但 App A §A.3 Prop A.6 實以 **telescoping** 證（Σ[(k+1)²−k²]=(n+1)²−1）。**確認為真**。→「proved by **telescoping**」。
- **PASS（無 finding）**：5 M4 authored 例（6.6/6.7/6.10/6.15/6.19）獨立複核、FTC-1/FTC-2 兩證（h<0 分支、EVT/Squeeze/Cor 4.4）、換元三證、全章數值＋圖說值、編號一致性。

## 散文 S·A·V：0 blocking + 4 advisory（3 套用／1 held）
- [A] §6.3「Two chapters of work」→「Two **sections**」（事實：定積分建於 §6.1–6.2）。**套用**。
- [U4] §6.3「the constant of integration」→「any added constant」（此名詞 §6.4 Def 6.4 才定義，forward-term）。**套用**。
- [A] §6.5 對稱幾何直覺（M4 段）：「equal areas on the same side of the axis」對會過軸的偶函數過度斷言 → 改「對應薄片同高同號相加／反號相消」。**套用（精確化）**。
- [F4] §6.2 additivity 括號密度：結構性重排（M3 已動此段）→ **held**，advisory 交裁決。

## 圖視覺：8 clean + 1 false-positive
- **Fig 6.9（velocity）「ylabel 應為 v」＝false-positive**：source 本就 `ylabel:"v"`（＋曲線標 v=t²−4、aria、caption 皆 v），VLM 把斜體 v 誤讀為 y（rubric 明列 VLM 小字誤讀）。**未依誤讀改標**。但根因＝該 label 緊貼「5」刻度而易誤讀 → 加頂 headroom（ymax 5.7→6.5），zoom 複驗 v 清晰。Fig 6.1–6.8 clean。

## 雙閘價值實證
sol/max 抓到的 Fig 6.2 caption 數學錯，M2 圖 gate-1＋gate-2（看 PNG，判畫得對不對）與 M3 §6.1 散文 gate-1 都**漏掉**——caption 的 prose-math 概念錯需數學讀者解析文字才抓得到。幻覺/失誤穿過兩個獨立模型（不同鏡頭）才會漏，正是三閘 gate-2 全跑的價值。同時 4 條被標中 2 條經回 source 複核駁回/重構，示範 over-report 需對抗式複核擋下。

## 定版
三閘 0 blocking → Ch6 as-built 凍結：Def 6.1–6.4／Thm 6.1–6.8／Strategy 6.1–6.2／Example 6.1–6.21／Figure 6.1–6.9／Cautions unnumbered。rebuild＋linebreak 0＋katex 0＋env-num 連續。**首個全程 5-milestone 試點章 M1–M5 端到端完成。**
