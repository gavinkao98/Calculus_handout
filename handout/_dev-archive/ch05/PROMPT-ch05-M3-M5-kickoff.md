# PROMPT — Ch5 M3＋M5 kickoff（貼進新 session 用）

> 2026-07-07 產出。前情：Ch5 的 M1／M2／M4／數學 gate-2 已完成（commits `a5287b2`、`2436232`、`e7d4bf1`）；
> M3 六個 subagent 因 Claude session 額度中斷（未產出任何 findings），本 prompt 接續 M3→M5。

---

```
你負責 NTU 微積分講義 repo（Calculus_handout，分支 video/template-redesign-navy-spine）
Chapter 5 的 M3（散文＋難度合一輪）與 M5（收尾）。全程繁體中文溝通。

【先讀（依序，讀完再動手）】
1. handout/_dev-archive/ch05/PLAN-ch05.md —— 章狀態錨；「Gate-family checklist」記到哪、M3 重跑步驟。
2. handout/PIPELINE.md —— M3 定義、「難度閘」節、「易懂性單一錨」節、通用紀律。
3. handout/_audit/PROSE-AUDIT-RUBRIC.md —— 散文閘契約（維度 A/B/C、blocking 線、non-findings、輸出格式）。
4. CONTENT_SPEC.md §16 —— 難度預算與 §16.2 基線讀者／B 類先備清單。

【現況事實（勿重查）】
- Ch5 as-built：9 節、Def 5.1–5.7、Thm 5.1–5.5、Strategy 5.1–5.7、Ex 5.1–5.27（含 2026-07-07
  M4 新增 Ex 5.14/5.22 與 §5.3 Leibniz intuition、§5.8 asymptote caution）、Figure 5.1–5.11。
- 已過閘：M1（⑤＋sympy＋章層 review）、M2（D1–D8 gate-1 0/0）、M4（ADOPT 4）、數學 gate-2
  （1 blocking [M7] 已修＋回歸，紀錄在 _dev-archive/ch05/ch05_math-gate2-audit.md）。
- 內容已含彎引號合規修復（quote_lint ch05=0）；新寫散文一律用 ’ 與 “ ”，勿用 ASCII 引號。

【M3 執行】
A. 散文閘 gate-1：派 3 個 handout-prose-audit subagent（唯讀），各審三節：
   ① fragments/ch05/sec-5-1~5-3 ② sec-5-4~5-6 ③ sec-5-7~5-9，
   範圍含 figcaption 與 M4 新增段。照 rubric 輸出（VERDICT＋逐條＋乾淨維度）。
B. 難度閘：派 3 個 learner-sim subagent（盲測——prompt 只說「以 persona 第一次線性閱讀
   handout/chapter5-print-standalone.html 全章並依你的輸出格式回報」，不得預告任何難點、
   不得提及 M4 增補位置）。可先 grep B 類先備清單（SPEC §16.2）做機械預檢。
   ※ 上次六個 agent 同發撞額度牆；這次分兩批（先 A 三個，完成後再 B 三個）。
C. 合併裁決稿：彙整六份輸出成 handout/_audit/REVIEW-ch05-prose-difficulty.html
   （standalone、MathJax CDN、雙擊即開；頂部摘要表＝各節 blocking/slowdown/難度 1–5 三份 sim
   對照＋與基線比較【Ch1–3≈3/5、Ch4=4/5、尖峰 §4.2=4.5】；逐條 findings 卡片標穩定編號）。
D. 裁決與修復（易懂性單一錨）：
   - blocking＝sim 的 stuck、B 類先備違規、以及 prose gate 的 U1–U4 客觀缺陷（可即擋、不必等 sim）；
     S·A·V 維度 A 其餘 findings 作預篩 advisory。
   - 全章難度若 >4 或尖峰 >4.5 → 屬弧線層異常，回 ROADMAP 深度決策重議、不在散文層硬修（先回報）。
   - 修復一律改 fragments/ch05/，然後 python handout/build.py ch05；
     驗證：node handout/_render/linebreak-gate.mjs handout/chapter5-print-standalone.html（0/0）、
     PYTHONIOENCODING=utf-8 python handout/quote_lint.py（ch05=0）、python tools/doc_lint.py（clean）。
   - 回歸（不可省）：blocking 修完後，對修過的節重跑 scoped prose-audit＋一份新的盲測 sim，
     確認卡點消失且無新卡點；結果補進同一份 HTML。
   - S·A·V gate-2（Codex）依 PIPELINE 頻率矩陣＝高風險章或出版前抽樣——Ch5 非高風險章，
     本輪不跑、在報告記一行即可。決策點可依 2026-07-06 授權調用 codex（read-only standing
     consent）收斂，不必逐次問使用者；計費 API 仍須先報價徵同意。

【M5 收尾（M3 收斂後）】
1. PLAN-ch05.md：checklist M3→✅（記 blocking 數與修復摘要）、M5→✅。
2. handout/PIPELINE.md dashboard：Ch5 行改「全閘完成（canon 首例）」。
3. CONTENT_ROADMAP.md Ch5 entry：補一句 gates-complete（含 M3 難度曲線一行），
   有懸而未決的方向叉路就記進 Open questions，沒有就收掉。
4. Commit（經此 prompt 即授權）：繁中 subject ≤70、body 逐條記 M3 findings 裁決與回歸結果
   （raw 稽核輸出落 gitignored scratchpad，findings 轉錄進上述 HTML／PLAN，不 commit raw）；
   結尾 Co-Authored-By 依你 session 的指示。

【硬約束】
- 稽核 subagent 全部唯讀、propose-not-act；四級分級、不 over-report、乾淨節是有效結果。
- 不動 M4 已裁決內容的「教什麼」（re-litigate 禁止）；散文修復只改「怎麼說」，動到數學要說明並補 sympy。
- 不碰 video/、不碰其他章節（其他章的引號違規已有獨立背景任務卡，不在本輪）。

【完成後回報並停】
回報：M3 blocking/advisory 統計、難度曲線 vs 基線、修了什麼、回歸結果、M5 dashboard 狀態。
下一步選項（回報即止、不要自動開跑）：Ch6 M1 kickoff（抄 PLAN-ch05 範本）或 video §3.2 spoken 路線。
```
