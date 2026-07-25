# Kickoff prompt：ch01 散文平實化回填（合併 sweep）

> 整段貼進**新對話**即可開跑。本檔同時是該輪的版控紀錄。
> 流程權威＝[`KICKOFF-plain-backfill.md`](KICKOFF-plain-backfill.md)；判準權威＝[`CONTENT_SPEC.md`](../../../CONTENT_SPEC.md) §3〈平實英文條款〉（RC，2026-07-25 凍結）。

---

## 貼這段（以下為 prompt 本體）

你在一個 fresh session（無前對話記憶）。任務：對 **ch01** 執行一輪**散文平實化回填（合併 sweep）**。

### 先讀（權威來源，依序）

1. `CLAUDE.md`（根）＋ `handout/CLAUDE.md` — 專案紀律：**Codex 唯讀調用需逐次徵得使用者同意**、與使用者一律繁體中文、commit body 逐條記 Mode B 裁決、fragment 是唯一內容源（改完跑 `python handout/html/build.py ch01`）。
2. `handout/html/_audit/KICKOFF-plain-backfill.md` — **本輪的流程權威**：Gate 0–9 關卡序、擋稿線、硬護欄、產物命名。照它跑，不要自創流程。
3. `CONTENT_SPEC.md` §3〈平實英文條款〉— **判準**（狀態 RC，凍結）：MUST／SHOULD／FLAG 三層、暖句四條件、**成對破折號與標點負載**（canonical 量測、目標 `T_can` ≤3.0/1000、CUT palette、四步仲裁決策序、具約束力先例、不換 tic 護欄、原因標籤、固定執行序、兩閘不可互相豁免）、段落層數值（≤120 詞／≤20 式為 SHOULD；≥150 詞或 >20 式或一段多論證 → 人工判定）。
4. `handout/html/_audit/PROSE-AUDIT-RUBRIC.md` — 四維度（U 易懂／F 流暢＋黏接判準／S·A·V／**R 語域平實**）、擋稿線、**§3-protected non-findings**（別誤砍連接詞、動機段、*Informally* gloss、教學重複）。
5. 前例（照這個形狀產出報告）：`REVIEW-ch06-sec-6-2-plain-applied.html`、`REVIEW-ch06-sec-6-3-plain-applied.html`、`REVIEW-mainline-plain-walk.html`。

### ch01 的三個專屬前提（**先看再動手**）

1. **§1.4 排除，不要動。** `sec-1-4.html` 是全專案唯一的**假陽性對照基準**——它是手稿章逐字內容，前三輪刻意保留，用來證明規則不誤傷真人寫的散文（家族命中 2 處、皆假陽性）。**本輪範圍＝§1.1、§1.2、§1.3、§1.5、§1.6 五節；§1.4 只量測、不改寫。**
2. **ch01 的破折號節奏曾被「刻意保留」，RC 已覆蓋該決定。** 早期去 AI 味報告把 ch01 的破折號視為合法招牌、把天花板設在 8.0/1000（ch01 現為 9.3）。2026-07-25 起目標改為**真實教材基準** `T_can` ≤3.0（canonical 重測：mooculus 0.0／APEX 0.5／CLP1 3.1）。**這是已定的政策轉向，不需重新討論**；但成對破折號仍須走四步仲裁決策序，**不得只換成逗號**（先例：`— far more often —` KEEP、`— only then —` 預設 KEEP）。
3. **ch01 是手稿章**（內容逐字取自 `ch01_foundations.tex`），不是 LLM 自產章。已量測的 §1.4 家族命中密度 ≈0，遠低於 canon 章（ch06 §6.2 為 14.7／千詞）。**預期詞彙層 findings 會少很多——這是正常結果，不要為了湊數而 over-report。**（rubric 明訂「乾淨的節是有效結果」。）

### 起跑基線（Gate 0 前值，2026-07-25 `python tools/prose_metrics.py --unit ch01`）

全章：canonical `N` = 5792、em-dash 54、密度 **9.3/1000**；tic guard 冒號接子句 39／分號 22／左括號 38／成對逗號 38。超額件數 `54 − 3×5792/1000` ≈ **37**。

| 節 | N | em-dash | /1000 | 冒號 | 分號 |
|---|--:|--:|--:|--:|--:|
| §1.1 | 1226 | 13 | 10.6 | 11 | 3 |
| §1.2 | 994 | 6 | 6.0 | 8 | 5 |
| §1.3 | 583 | 8 | 13.7 | 1 | 2 |
| §1.4 | 733 | 4 | 5.5 | 2 | 3 | ← **對照組，不改** |
| §1.5 | 731 | 3 | 4.1 | 1 | 3 |
| §1.6 | 1525 | 20 | 13.1 | 16 | 6 |

重點目標：**§1.6（20 個 dash，全章最多）與 §1.3（密度最高）**。

### 工具

- 量測：`python tools/prose_metrics.py --unit ch01`（canonical prose stream；兩個 `/1000` 指標共用同一分母）。
- 改動驗證：`python tools/verify_edits.py <file> <edits.txt>` — 套用後必須 **PASS**（工作樹 == HEAD ＋恰好這些替換、reverse-apply byte-for-byte、未涵蓋差異 0 處）。
- build：`python handout/html/build.py ch01`（**一定帶 `ch01` 參數**；無參數會重建全部 standalone）。

### 硬護欄

- **裁決前 propose-only**：Gate 1–2 不改任何 fragment。
- **不動數學**：公式、編號、cross-ref 一律不碰；Gate 5 以「數學片段程式化 diff」證明（理想零差異）。
- **不機械拆句、不設硬性句長上限**；不得為維持句數用任何標點把兩個獨立推論黏回一句。
- **讀 fragment 開頭的 HTML 註解**：`CONSTRAINT`／`WORDING CONSTRAINT` 標的措辭是已裁決過的設計，動到就是破壞它（ch01 §1.4 有 ln gloss 的紀錄；其他節逐檔看）。
- **不重跑已過的其他閘**（圖閘、example 選題、learner-sim）；但**改過的段落不能沿用舊 pass**，Gate 5（math）與 Gate 6（Mode B 語意等價）必跑。
- **LaTeX 線**：`make_dist.py` 的 `NAMES` 表目前只有 appB、ch03，**ch01 不在表內** → Gate 7 記為 pending（要補表才能跑），**不可默默跳過**。
- **Codex（Gate 2）調用前先說模型／用量／成本徵同意**；大 prompt 要背景執行（>70KB 約 10–15 分鐘），材料一律 inline 進 prompt（讓 Codex 自讀 fragment 會 UTF-8 亂碼、產生整批假陽性）。

### 產物

- `handout/html/_audit/REVIEW-ch01-plain-walk.html`（Gate 1 走查，逐條含 candidate ID ＋原因標籤 `DASH-CUT`／`DASH-KEEP`／`PLAIN-SPLIT`／`TIC-REBALANCE`／`R1-LEXICAL`）
- `handout/html/_audit/REPORT-ch01-plain-codex-raw.md`（Gate 2 raw 照登）
- `handout/html/_audit/REVIEW-ch01-plain-applied.html`（前後全句對照＋Gate 4–8 驗收表＋保留清單＋未完成項）
- 回 `handout/html/_audit/REPORT-emdash-baseline-and-rollout.md` §2 更新 ch01 的密度與 tic guard 四項並打勾。
- commit：在**新分支**（如 `handout/plain-ch01`），subject ≤70 字，body 逐條記 Mode B。

### 完成定義

密度達 `T_can` ≤3.0/1000、tic guard 四項無顯著上升（raw ≥+3 **且** 密度 ≥+0.5/1000 才算顯著、須填理由）、Gate 5 數學零差異（或逐條說明）、Gate 6 語意等價、Gate 8 分頁目檢過、§1.4 未被改動（`git diff` 確認）、四份產物齊備。

---

*本檔 2026-07-25 建立。ch01 是 RC 凍結後第一個回填單元；本輪的裁決若顯示「同一條規則在三節以上反覆誤判」，才依 RC 條款回頭修 `CONTENT_SPEC.md` §3，否則一律走 finding 層逐條裁決。*
