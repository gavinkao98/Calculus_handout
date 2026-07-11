# 講義 → 影片產線 — 進度錨（現況快照）

> 本檔只保留**現況快照＋open items**（目標 ≤50 行），是跨對話進度錨、每個新 session 第一個讀的檔。
> **歷史輪次全文在 [`_archive/REBUILD_LOG-2026-05-to-07.md`](_archive/REBUILD_LOG-2026-05-to-07.md)**（2026-05-30～07-06 逐輪詳錄，含所有決策原文與 durable 教訓）。
> **維護規則（2026-07-07 制）：** 每結一輪工作＝更新本快照，該輪詳錄（決策、教訓、成本帳）寫進 archive 檔頂部；本檔不再無限 append。

## 現役路線（2026-07-07）

- **TTS**：MiMo `mimo-v2.5-tts` builtin voice **Dean**（唯一真旁白路線；Gemini/Charon 2026-06-16 退場、voice-design／Calm Professor 2026-07-05 退役）。**scene-level TTS＋forced alignment 為正式路線**：計時源＝stable-ts transcript-constrained FA（whisper-timestamped 降級 QA 探針）；`tts.py --unit auto` 涵蓋全部 content template；fallback ladder＝arbiter(small.en)→resynth→sentence-chunk→beats（chunk 受 `--fallback-budget` 自檢）。
- **文字渲染**：Route A（全 LaTeX/pdflatex；內文/標題 IBM Plex Sans、eyebrow IBM Plex Mono、數學 Latin Modern）2026-06-25 落地，Pango 路徑已移除。
- **模板／版面**：Lectern grid＋navy spine；Step 0 型階 pass＋容量契約 v2（G1–G6，advisory lint）2026-07-05 落地。
- **House audio**：Candidate B（intro/outro bed＋divider stinger gain 0.6；content 場全乾聲；caution ping OFF）。
- **審核閘**：七層閘地圖見 [`REVIEW_GATES.md`](REVIEW_GATES.md)（含 2026-07-07 gate-2 頻率矩陣）；七份 SSOT rubric 在 `content_scripts/_audit/`。
- **分支**：`video/template-redesign-navy-spine`。

## 各節狀態

| 節 | deck | 狀態 |
|---|---|---|
| ch03 §3.1 | `ch03_trig_derivatives` | ✅ **全流程完成**：clean Dean 成片 `output/ch03/s3.1/ch03_trig_derivatives_mimo.mp4`（~16.2 分、1080p）；NFA 雙閘過（gate-2 抓 1 D3 已修）；§3.1 單景 backlog 8 項打磨完（V blocking=0）。3 場 FA 降級 beats（`continuity_argument`／`derivative_of_cosine`／`shm_stacked_graphs`）＝使用者裁決「先不用」修，**勿自行重試 scene-level**（燒 billed API）。真 4K final 另議。 |
| ch03 §3.2 | `ch03_chain_rule` | Stage-1 **LOCKED**（內容稿＋六鏡＋copyedit＋sign-off）；待 spoken／derive／NFA／storyboard render。 |
| ch01 §1.1 | `ch01_inverse_functions` | 版面回歸 deck（舊練習產物已刪；正式 ch01 影片屆時從講義重跑）。 |

## Open items

- **[進行中] 產線硬化**（kickoff [`KICKOFF-pipeline-hardening.md`](KICKOFF-pipeline-hardening.md)，分支 `video/pipeline-hardening`）：**Phase 0＋1 完成（2026-07-11）**。Phase 0：分支自 `84c2799`、綠基線 selftest 全綠。Phase 1（T1–T4，7 commits `0d6954e`→`320871f`）：T1 `_mimo.yml` freshness gate（`derived_check.py` 雙輸入 LF-norm stamp）；T2 tts.py 計費面（`--backend` 必填＋preflight fail-closed guard／dry-run planned-worst 報表／`--scene` 併回 prior／計費收據）；T3 `--unit auto` allowlist 單一源（`template_names.py`＋parity）；T4 ASR QA verdict 三態落 manifest。17 selftest 全綠、demo mock 整合驗收過。**Codex 對抗 review（Terra/max）usage-limited 中斷**，浮現 1 edge（null-char audio_file str 過 type check 但 `build_reuse_index` `Path()` crash）＝評估非 blocking（自產 manifest 不可能、fail-safe pre-synth、Karpathy §2；詳 scratch `codex-phase1-assessment.md`）。**§3.2 進真 TTS 前必做硬化＝達成**。Phase 2（T5 `{show}` cross-check）＋Phase 3 前段（T6 listening pack／T7 timeline+vtt+chapters／T8 單次編碼+bt709+faststart）已落地（commits 至 `39d697d`＋T7），**19 selftest 全綠**。**Codex 對抗 review 因 usage limit 反覆中斷（reset 10:55 local），改為 quota 回復後對 T1–T8 一次跑完整回歸**（詳 scratch `codex-*-assessment/raw`）。**剩：T9 場景轉場 A/B、T10 loudness A/B（皆裁決件——產 A/B 交付物後停等使用者裁決）、T11 文檔統一收尾。**
- §3.2 走完 MiMo 路線（spoken → NFA → render）＝下一個正典節。
- `{show}` target-vs-payload 交叉驗證（task #6，需 manim）；VISUAL-FRAME detection 面驗證（併入下一個重跑節）。
- 真 4K final render（§3.1）另議。
- spoken.yml 白名單 auto-prefill（V4 工程 backlog）——等下方成本量測顯示「手寫 spoken」是主要成本再啟動；產物仍過 parity＋NFA。
- 未消費產物（house audio A/C＋caution ping、孤兒 ch01_inverse_trig hooks、derive_spoken ch01 殘留）＝2026-07-07 清理（見該日 commit）。

## 每節成本量測（2026-07-07 起；量三節後檢視模板紅利，再定 per-scene 客製 hook 上限）

| 節 | audit/撰稿 tokens | render 次數 | 客製 hook 數 | 真 TTS calls | 回歸輪數 |
|---|---|---|---|---|---|
| §3.1（基線，事後估） | 單景打磨 8 項×80–216k | 多輪（Step 0／capacity v2 回歸含 48 場） | 8 | ~36（21 場＋fallback＋重合成） | 3+ |
| §3.2 | 待記 | 待記 | 待記 | 待記 | 待記 |
