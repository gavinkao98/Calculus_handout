# §3.1 影片「最大詳細」全重做 — 設計規格（SPEC）

> **性質：** 這是經 brainstorming 設計閘核可的**規格**（what／why／決策／場景藍圖／收斂定義）。逐 task 的實作分解由後續 `writing-plans` 產出 `PLAN-ch03-s31-detail-redo.md`，不在本檔。
> **日期：** 2026-06-29 ／ **分支：** 續用 `video/template-redesign-navy-spine`（不另開）。
> **取代關係：** 本規格**取代** [`PLAN-ch03-s31-video.md`](PLAN-ch03-s31-video.md) 的內容密度假設（該檔走「壓縮塞一頁、邏輯骨架」；本檔回到方法論的「detail over compression」）。其餘工程節奏（指令、閘序、hook 機制）仍沿用該檔。

---

## 0. 緣起（翻案級的重新定性）

§3.1 影片第一版在 Stage-2 模板化時，把證明壓成單頁 2–3 行邏輯骨架（render 後實測填充僅 ~30–35%）。2026-06-29 密度稽核（[`REVIEW-ch03-s31-density-audit.html`](REVIEW-ch03-s31-density-audit.html)）證實：**無承載性缺口（旁白＋相鄰場景接住了推理），但場景確實稀、版面確實空。**

使用者裁決（2026-06-29）：**「影片裡的講解要越詳細越好、少省略；選材可以少，但講解要清楚。必要時重頭來過。」**

**關鍵定性：這不是改規則，是回去遵守本來就寫好的規則。**
- [`CONTENT_METHODOLOGY.md`](../../CONTENT_METHODOLOGY.md) §1 核心理念 #1：**「Detail over compression。寧可多開一個教學單元……做 4 分鐘精華片不是目標。」**
- 同檔 §3 環境對應表：**證明 >~4 步就拆「statement 單元＋proof 單元」**。
- [`DESIGN.md`](../../DESIGN.md) 多頁拆分：**「修復方法是 split，不是 squeeze」**，並已建好 `part: {current,total}` 機制。

第一版**違背了自己的方法論**；本次重做＝把 §3.1 補回合規。修法全靠現成機械，不動 pipeline。

---

## 1. 鎖定的決策（使用者 2026-06-29 逐項裁決）

| # | 決策 | 選定 |
|---|---|---|
| D1 | 重做範圍 | **全 §3.1 內容稿從頭重拆**（非只補幾場）。仍走兩階段，內容稿為 SSOT。 |
| D2 | 詳細度天花板 | **第1檔（忠實全展開）為全節基準 ＋ 核心證明加第2檔（直覺鷹架＋小圖）**。 |
| D3 | 選材 | **全保留**（companion limit／all-six／SHM 三個不同模式都留），只把講解加詳。 |
| D4 | 防漂移護欄 | **加**一條到 `DESIGN.md` authoring checklist（見 §6）。 |

「三檔密度」定義（決策當下的對照工具，以 continuity 證明示範）：
- **第0檔**＝現況骨架（界憑空出現、~35% 填充）。
- **第1檔**＝把課本完整證明每一步還原、每步有可見來源，超一頁拆場。**全節基準。**
- **第2檔**＝在第1檔之上加「為什麼這樣做」的直覺與小圖（**不加新數學**）。**只用在樞紐證明。**

---

## 2. 密度標準的落實機制（全為現成）

1. **長證明拆場**：`theorem_proof` 證明 >4 步 → 拆「statement 場」＋「proof 場」（方法論 §3）。
2. **超一頁走多頁**：單場填滿仍溢出 → `part: {current, total}`，每頁重貼 header、`{show}` 旁白逐場手寫（DESIGN.md「C 多頁機制」）。`sizecheck` 排版前預測式 warn「拆 ~N 頁」。
3. **一步一 beat**：每個承載性步驟在畫面上有自己的列與 `{show}` reveal，不再把推理藏進旁白。先前「憑空出現的界」「省掉的恆等式」一律顯示其來源。
4. **第2檔鷹架**（僅樞紐）：開場直覺 beat（白話講「這步在幹嘛」）＋必要的 mini-visual ＋收束回呼。硬護欄：**不增刪任何數學**（方法論 §1）。
5. **字級恆定**：詳細度靠「多開單元／拆頁」吸收，**永不靠縮字**（DESIGN.md 容量契約統御原則）。

**第2檔施用對象（樞紐 4 處）：** `difference_quotient_for_sine`、`sector_inequality→squeeze_to_the_bound`（幾何擠壓）、`fundamental_limit`、以及旗艦改造 `continuity_of_sin_cos`。其餘維持第1檔。

---

## 3. 場景藍圖（current 19 內容場 → 約 22–26）

> 仍是四階段結構（intro／4 divider／outro 不變）。下表是**內容場**的重做意向；正式逐場欄位於 Stage 1 內容稿撰寫時定稿。忠實對象：[`handout/fragments/ch03/sec-3-1.html`](../../../handout/fragments/ch03/sec-3-1.html)。

### Stage 1 — The Limit Behind the Slope
- **why_trig_is_different**（motivation）— 小改。保留「funnels to `lim sinθ/θ`（0/0）」的課本路線；加一個 beat 把 0/0 障礙講得更生動（不引入 angle-addition 新路線，維持課本 sum-to-product 進路）。
- **difference_quotient_for_sine**（derivation，**第2檔**）— 中改加料。sum-to-product → 分子 → 除以 h（顯示 `h=2·h/2` 技巧）→ 兩因子形 → 點名兩因子各需「連續」「基本極限」；加 `lim_{h→0}` framing ＋一句「整個導數現在掛在兩件事上」的直覺。容量允許則 1 場，溢出則拆。

### Stage 2 — A Geometric Squeeze
- **sector_inequality**（graph hook，**第2檔**）— 維持圖；偶函數論證獨立成 beat；三面積嵌套逐步 build。
- **(新) chord_le_arc**（visual，**第2檔 mini-visual**，可選）— 單位圓上「弦 ≤ 弧」把 `|sinθ| ≤ |θ|` 畫出來，餵給 continuity 與 fundamental limit。若併入 sector hook 則不獨立。
- **squeeze_to_the_bound**（derivation，**第2檔**）— 每步成 beat：×2 → `sinθ≤θ≤tanθ` → ÷sinθ＋`tan=sin/cos` → 取倒數翻向 → `cosθ≤sinθ/θ≤1`；附帶界 `0≤|sinθ|≤|θ|`。
- **continuity_of_sin_cos** — **旗艦改造，拆 2 場＋第2檔**：
  - **continuity_statement_sin_limit**（statement 場）— 陳述 sin、cos 處處連續 ＋ 由界＋squeeze 得 `lim_{θ→0} sinθ=0`；開場第2檔直覺「連續＝角度動一點、sin/cos 也只動一點」。
  - **continuity_argument**（proof 場）— **顯示**和差化積兩條恆等式（cos、sin）→「中間因子 ≤1」→ 界 `|Δcos|,|Δsin| ≤ 2|sin((x−x₀)/2)|` → `x→x₀ ⟹ RHS→0` → squeeze ⟹ 連續 ∎。（修掉第一版「界憑空出現」的唯一真缺口。）
- **fundamental_limit**（theorem_proof，**第2檔**）— statement ＋ `cosθ≤sinθ/θ≤1` ＋ `cosθ→1`（連續）＋ 偶 ⟹ 兩側；每步成 beat ＋ 直覺扣回擠壓圖。證明本身短，預設 1 場。
- **squeeze_graph**（graph）— 維持。
- **limit_not_identity**（callout）— 維持。
- **radians_essential**（callout）— 維持。

### Stage 3 — The Two Derivatives
- **derivative_of_sine**（theorem_proof）— **第1檔補回**：顯示 `lim_{h→0}`(差分商) = `lim cos(x+h/2)·sin(h/2)/(h/2)` → `cos x·1 = cos x`，兩個極限事實各自引用（連續、基本極限）。補上第一版省掉的 setup 行。
- **derivative_of_cosine**（theorem_proof）— **第1檔補回**：repeat-pattern 省 setup，但**顯示伴隨恆等式** `cos A−cos B = −2 sin((A+B)/2) sin((A−B)/2)`（這是唯一的新東西），再走鏡像論證。
- **slope_equals_height**（graph hook）— 維持。
- **derivative_cycle**（definition_math，Remark 3.1）— 小改：強化 `e^x` 一步自我複製 vs 四步循環的呼應 beat。

### Stage 4 — Consequences & Applications
- **companion_limit**（derivation，Ex 3.1）— 第1檔：每步成 beat（已忠實，確保逐步顯示）。
- **all_six_trig_derivatives**（derivation，Ex 3.2）— **第1檔補回**：顯示 sec′ 的商法則步驟（第一版只給結果）；視容量可拆 `tan′/sec′`（worked）與 `cot′/csc′`（stated）兩場。**全保留**（D3）。純機械操作，不加第2檔。
- **shm_compute**（derivation，Ex 3.3）— 維持（已乾淨）。
- **shm_stacked_graphs**（graph hook）— 維持。
- **toward_the_chain_rule**（forward_ref）— 維持（刻意輕；MUST NOT 報節號）。
- **recap**（recap_cards）— 小改：takeaway 對齊加詳後的證明四支柱。

**淨變化估計：** continuity 1→2、all-six 可能 1→2、新增 chord_le_arc（可選）、若干直覺 beat → 內容場 19 → **約 22–26**。

---

## 4. Stage 1 流程（內容稿，SSOT）

1. 讀現有 [`ch03_trig_derivatives.md`](../ch03_trig_derivatives.md) 為基線（不覆蓋重生，外科式重拆——方法論 §8）。
2. 依 §2–§3 重拆教學單元、重寫 narration（口語、一步一 beat、第2檔加直覺；數學忠實課本、不增刪）。
3. 重編 [`ch03_trig_derivatives_narration.html`](../ch03_trig_derivatives_narration.html) 審核稿。
4. **六鏡對抗式稽核**（SSOT `CONTENT-SIXLENS-RUBRIC.md`）：L1 忠實／L2 拆解／L3 語域／L4 不重複／**L5 數學正確（每個證明/例題隔離盲算）**／L6 完整；refute-by-default、四級分級、逐條複驗 → 修到 **blocking==0**。
5. **copyedit**（SSOT `NARRATION-COPYEDIT-RUBRIC.md`，鎖稿前唯一改措辭窗口）。
6. **交付 HTML、等使用者 sign-off → 標記 LOCKED、設 `CONTENT_APPROVED`**。

## 5. Stage 2 流程（工程）

1. 把新內容稿模板化進 [`ch03_trig_derivatives.yml`](../../storyboards/ch03_trig_derivatives.yml)：拆場、`part:`、新 `{show}` reveal 對齊新 narration。
2. 調整 3 個 hook（`sector_inequality`／`slope_equals_height`／`shm_stacked_graphs`）；若新增 `chord_le_arc` 則加第 4 個 hook 或併入 sector。
3. 三閘：`schema.py`／`lint.py`／`sizecheck.py` **0 error**（sizecheck 的「拆 ~N 頁」warn 逐筆判，作為拆場依據）。
4. 全片 mock render 1080p（`make.py --backend mock --quality high`）。
5. **視覺幀稽核**（`visual-frame-audit`，SSOT `VISUAL-FRAME-RUBRIC.md`）V1–V8 blocking → 修到 **blocking==0**。
6. HTML 報告（`REVIEW-ch03-s31-detail-redo-applied.html`）＋更新 `REBUILD_STATUS.md`。

## 6. 護欄（D4，順手加）

在 [`DESIGN.md`](../../DESIGN.md) §「Authoring checklist——反覆出現的錯誤」表加一行：

> **Don't：** 在低填充幀只放證明骨架／把 >4 步證明壓成 2–3 行。**Do：** proof >4 步拆 statement＋proof 場、超頁走 `part:`、一步一 beat。**原因：** detail over compression（CONTENT_METHODOLOGY §1）；ch03 §3.1 第一版壓縮漂移的學費（2026-06-29 密度稽核）。

## 7. 收斂定義（「做完」）

內容稿 LOCKED（六鏡＋copyedit blocking==0、使用者 sign-off）＋ storyboard 三閘 0 error ＋ 全片 mock render 成功 ＋ visual-frame-audit blocking==0 ＋ HTML 報告與 REBUILD_STATUS 就位 ＋ DESIGN.md 護欄行已加。

## 8. 計費紀律

全程**離線、免費**（mock TTS、本地 render、離線抽幀、免費 gate-1 subagent）。任何計費步驟（MiMo TTS 合成、Codex gate-2、VLM critic gate-2）**仍延後**，各自單獨報價、徵同意才跑——本規格不含任何計費步驟。

## 9. 參照

- 忠實來源：[`handout/fragments/ch03/sec-3-1.html`](../../../handout/fragments/ch03/sec-3-1.html)
- 方法論：[`CONTENT_METHODOLOGY.md`](../../CONTENT_METHODOLOGY.md)（§1 detail-over-compression、§3 proof split、§8 維護）
- 視覺/容量：[`DESIGN.md`](../../DESIGN.md)（容量契約、多頁 `part:`、template catalog）
- 前版計畫：[`PLAN-ch03-s31-video.md`](PLAN-ch03-s31-video.md)（工程節奏沿用、密度假設被本檔取代）
- 密度稽核：[`REVIEW-ch03-s31-density-audit.html`](REVIEW-ch03-s31-density-audit.html)
