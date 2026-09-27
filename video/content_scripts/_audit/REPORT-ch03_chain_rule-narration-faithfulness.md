# NFA 旁白忠實稽核 — 結案報告（§3.2 `ch03_chain_rule`）

> **這份檔是什麼：** §3.2 旁白忠實稽核（NFA）兩道閘的**版控結案紀錄**，是 A4「旁白雙版落地」
> 的最後一項完成判準。稽核契約見 [`NARRATION-FAITHFULNESS-RUBRIC.md`](NARRATION-FAITHFULNESS-RUBRIC.md)，
> 本節的派工 prompt 見 [`PROMPT-ch03_chain_rule-narration-faithfulness.md`](PROMPT-ch03_chain_rule-narration-faithfulness.md)。
> 依 rubric §回報規格，`REPORT-*.md` 屬純版控紀錄，不在「交付物須產 HTML」之限；
> 逐筆 finding 的可讀版在各閘自己的 HTML 審核稿。
>
> **收斂判定：`blocking == 0`（兩道閘皆已關閉）。** 詳下 §6。

---

## 1. 稽核對象與工件

| 角色 | 檔案 | 說明 |
|---|---|---|
| **忠實度判準源（source of truth）** | [`../../storyboards/ch03_chain_rule.yml`](../../storyboards/ch03_chain_rule.yml) | 23 個 content 場的 `say:`。**這就是會被合成、會出片的旁白。** 28 場＝intro 1／divider 3／content 23／outro 1 |
| **受審工件（Version B，口語單一源）** | [`../ch03_chain_rule.spoken.yml`](../ch03_chain_rule.spoken.yml) | 手寫口語稿；D2／D3／D4 對它判 |
| 受審工件（Version B 投影） | [`../ch03_chain_rule_narration_spoken.md`](../ch03_chain_rule_narration_spoken.md) | 由 `derive_spoken.py` 機械生成的人讀版 |
| 受審工件（Version A） | [`../ch03_chain_rule_narration.html`](../ch03_chain_rule_narration.html) | 內容稿 `narration:` 的 MathJax 渲染版 |
| 交叉參照（非判準） | [`../ch03_chain_rule.md`](../ch03_chain_rule.md) | 內容稿 24 單元的 `narration:`（LOCKED，2026-06-29 sign-off） |
| 機械投影（context） | [`../../storyboards/ch03_chain_rule_mimo.yml`](../../storyboards/ch03_chain_rule_mimo.yml) | `say := spoken`，送 TTS 的 deck |

**Tier 0 前提（兩閘開跑前即綠）：** `python video/pipeline/derive_spoken.py --deck ch03_chain_rule --check`
→ `parity OK`（每個 content `say` 都有 spoken 對應、`{show}` marker 逐一對齊、口語端無 `$` LaTeX 外洩）。
NFA 只判語意層。

**判準紀律（本節與 §3.1 同案）：** 內容稿 `narration:` 與出片 `say:` 措辭有差，是 Stage 2
「依鎖定內容稿為口說再撰寫」的**設計結果**，屬已知 doc-sync 落差，**非 blocking**；
忠實度**對 `say:` 判**，不對 `narration:` 判（見 [`../ch03_chain_rule.md`](../ch03_chain_rule.md):8 的檔頭裁決行）。

---

## 2. gate-1 — `narration-faithfulness-audit` subagent（Claude Opus 5，免費）

**VERDICT: 0 blocking, 3 advisory**

### N1-01 [D1/D2] 內容稿 `narration:` 與出片 `say:` 全節措辭不同

- **裁決＝Keep 兩個產物都不動 ＋ doc-sync 標註。**
- 理由：這是 Stage 2 為口說收緊的既定設計，不是忠實破口；§3.1 先例已裁定為
  **known pre-existing、非 blocking**。
- 落地證據：已在 [`../ch03_chain_rule.md`](../ch03_chain_rule.md):8 檔頭加一行說明
  （「**出片旁白的權威（doc-sync）**」），寫明出片旁白以 storyboard `say:` 為準、
  `narration:` 已 LOCKED 一字不改、NFA 對 `say:` 判。
- 兩個產物本身**零改動**。

### N1-02 [D4] `proof_delicate_bound` 主詞與動詞相距 23 字

- **裁決＝採納。**
- 口語端把 `$|R_1(h)|/|h|<1$` 的唸法改為 $\lvert R_1(h)/h\rvert$ 的形（數學等價，省 4 字），
  縮短主詞—動詞距離。
- 現行口語（[`../ch03_chain_rule.spoken.yml`](../ch03_chain_rule.spoken.yml):290）：
  “…shrinking the window once more so **the absolute value of the ratio of R sub one of h
  to h** is less than one puts the whole piece below…”
- **散文一字不動**——只換數學的唸法，D2 逐字條件不受影響。

### N1-03 [D3] `(x+2)^2` 的 “squared” 右界未關

- **裁決＝採納。**
- 舊唸法 “…, the quantity x plus two, squared” 的 “squared” 掛在哪一層沒有標記，
  聽者可能聽成 $\bigl(\tfrac{3}{x+2}\bigr)^2$。
- 改為 “**the square of the quantity x plus two**”
  （[`../ch03_chain_rule.spoken.yml`](../ch03_chain_rule.spoken.yml):334）。

### 連帶：D5 新慣例入 rubric

[`NARRATION-FAITHFULNESS-RUBRIC.md`](NARRATION-FAITHFULNESS-RUBRIC.md):51 新增一列——

> 分母整體被平方的分數 $\tfrac{A}{(X+Y)^2}$ → “A over **the square of the quantity** X plus Y”

**適用範圍限「分母整個被平方」**；獨立群組的次方（`(\sqrt[3]{x-2})^3`、`(f^{-1}(x))^2`、
§3.1 的 “expanded the quantity x plus h, to the n”）仍走既有的「群組次方 → all squared」列，
本列**不推翻 §3.1 的先例**。

落地 commit：`ae840f3`。

### gate-1 回歸輪

三條 advisory 修完後重跑 gate-1：**3 advisory → 1 advisory**（唯一殘留＝下節的 R2-01）。

---

## 3. R2-01 — gate-1 回歸輪發現的契約自相矛盾

- **現象：** gate-2 的 prompt 檔與 [`../ch03_chain_rule.md`](../ch03_chain_rule.md) 檔頭的判準**相反**
  ——一邊說忠實度對內容稿 `narration:` 判，一邊說對 storyboard `say:` 判。
- **成因：** **主對話派工契約寫錯**——事實表把「核准源」欄填成 `.md`，於是 prompt 承繼了錯的判準。
  不是子代理的問題，是派工端的問題。
- **處置：** 主對話修正 prompt，使其與 §3.1 同案裁決及 `.md` 檔頭一致（忠實度對 `say:` 判）。
- **commit：** `52962e0`。

---

## 4. gate-2 — agy `gemini-3.1-pro-high`（計費，使用者 2026-09-14 核准）

**VERDICT: 1 blocking, 0 advisory**

### 4.1 執行條件

- **模型／通道：** Antigravity CLI（`agy`）`gemini-3.1-pro-high`。外部生成式 API，
  **使用者 2026-09-14 逐次核准後才調用**（CLAUDE.md「付費 API 調用須先經同意」）。
- **盲審隔離：** cwd 與 `--add-dir` **都設在 repo 外的工作資料夾**，資料夾內只放 9 個受審檔。
  它看不到 repo 其餘內容，也無法回頭讀 gate-1 的結論。
- **usage：** input 127,089／output 40,411（其中 thinking 31,243）／cache_read 1,783,091／
  total 167,500；`status` 回 **SUCCESS**。

### 4.2 高風險唸法逐條查核 — **13 條全部 PASS**

prompt 表列 11 條，加上 gate-1 這一輪新改動的 2 條（`3/(x+2)^2`、`|R_1(h)/h|<1`），共 13 條：

| # | 數學 | 查核點 | 判定 |
|---|---|---|---|
| 1 | `f'(g(x_0)) g'(x_0)` | at／of 分工（`f prime at g of…` vs `g prime of x sub zero`）關住引數、不讓後續 “times” 被聽進括號內 | PASS |
| 2 | `R_1(h)/h`、`R_2(y)/y`、`R_3(h)/h` | 一律 “the ratio of A **to** B”，全 deck 不用 “over” | PASS |
| 3 | `m+R(h)/h` | “m plus the ratio of R of h to h”，外層和不被吞 | PASS |
| 4 | `\sqrt{1+x^2}`、`\sqrt{1+\sin^2 x}` | 根號範圍以 “the quantity” 開群 | PASS |
| 5 | `(\|m_1\|+1)\varepsilon` | 三重邊界正確，非 $\lvert m_1+1\rvert\varepsilon$、非 $\lvert m_1\rvert+(1\cdot\varepsilon)$ | PASS |
| 6 | `m_1 h+R_1(h)` | 積／和邊界以顯式 “times” ＋停頓標出 | PASS |
| 7 | `\cos^2 x` vs `(\cos x)^2` | “cosine squared x” vs “cosine x, all squared”，同拍出現時可辨 | PASS |
| 8 | `3/(x+2)^2` | D5 新慣例 “the square of the quantity x plus two”（gate-1 N1-03 改動） | PASS |
| 9 | `\|R_1(h)/h\|<1` | “the absolute value of the ratio of R sub one of h to h is less than one”（gate-1 N1-02 改動） | PASS |
| 10 | `dK/dU`、`dU/dO`、`dK/dO` | Leibniz 讀法（kelp／urchin／otter 食物鏈例） | PASS |
| 11 | `\varepsilon`、`\delta`、`\alpha` | 希臘字母一律拼英文名，全 deck 一致 | PASS |
| 12 | `x_0`、`u_0`、`m_1`、`m_2`、`R_1`–`R_3` | 下標 “sub” 讀法，全 deck 一致 | PASS |
| 13 | `f^{-1}` | **查證「本 deck 未使用」的主張為真**（自行 grep `.spoken.yml` 與 `narration:`），非採信 | PASS（確認未出現） |

### 4.3 維度判定

| 維度 | 判定 | 說明 |
|---|---|---|
| D1 Version A 忠實 | `skipped_by_premise` | 依 prompt 判準，忠實度對 `say:` 判；Version A 對 `narration:` 的逐字性另案已驗 |
| D2 Version B 忠實 | **`has_findings`** | 見 N2-01 |
| D3 口語數學唸法 | `clean_verified` | 13 條高風險逐條走過（§4.2） |
| D4 口語語域／順耳 | `clean_verified` | |
| D5 唸法慣例裁定 | `clean_verified` | |
| D6 TTS 設定合理性 | `clean_verified` | |
| D7 數學內容正確 | `clean_verified` | |

> D1 的 `skipped_by_premise` 是**因既定前提而未走**，與 D3–D7 的 `clean_verified`
> （實際走過且判乾淨）性質不同，依 prompt 要求分開記。

### 4.4 N2-01 [D2] **blocking** — `example_chain_times_quotient` 的散文被改寫

**原本是什麼**（canonical `say:`，修前）：

    it comes out to three over $(x+2)$ squared.

對應口語稿：

    it comes out to three over the square of the quantity x plus two.

**為何是 blocking：** D2 的硬條件是「英文散文**逐字**相同，只有 `$...$` 裡的 LaTeX 可以被拼成口語」。
上式的 `squared` 是寫在 `$...$` **外面**的英文散文字，卻在口語端被改寫成 “the square of” 並**搬到前面**
——散文被改寫、被搬位，不是「LaTeX 被拼成口語」，因此構成 D2 parity break。

**裁決＝採納 gate-2 的最小修法（修根因）。** 把指數搬進 LaTeX：

    - over $(x+2)$ squared.
    + over $(x+2)^2$.

`squared` 於是不再是散文字，**口語文字一字不改**，兩邊散文回到逐字相同。
現況見 [`../../storyboards/ch03_chain_rule.yml`](../../storyboards/ch03_chain_rule.yml):584。
commit `201281d`。

**這一條 gate-1 沒抓到。** 而且成因正是 gate-1 自己的 N1-03 修法——為了關 D3 的右界，
在 `squared` 還是散文字的狀態下改寫了口語端；**主對話當時看過這個落差，判為灰區、放過**。
兩道判斷同時漏接，由獨立第二讀者補上。**這就是 gate-2 存在的理由**，如實記錄於此。

### 4.5 修後回歸

- 對 N2-01 修正重跑：**0 blocking / 0 advisory**。
- **全 deck 掃同型破口（`$...$` 外的散文數學字在口語端被改寫）：0 處。**
  修掉的那一句是全 deck 唯一例外。
- **23 場 `scene_text_hash` 零變動 ⇒ 零 TTS 成本。**（`say:` 的英文散文 token 序列不變，
  `tts.scene_reuse_ok` 全數命中快取。）

---

## 5. gate-2 的框架層反對（`disagreements_with_premise`）

gate-2 在 `disagreements_with_premise` 欄提出一條**對前提本身**的反對，不是 finding：

> 反對「storyboard `say:` 而非內容稿是 source of truth」——理由是這讓**下游工程產物**
> 變成事實上的 SSOT，架空了使用者對內容稿的簽核：使用者簽的是內容稿，
> 真正被合成、被聽見的卻是從未以「旁白」身分送簽的 `say:`。

**使用者裁決＝選 B：合成前補一個 storyboard `say:` 的簽核點。**
不動既有判準（忠實度仍對 `say:` 判、`narration:` 仍 LOCKED），而是在**花錢合成之前**
補一道人閘，把 23 場的 `say:` 以「旁白」身分送到使用者面前簽核。

落地產物：

- 產生器 [`_gen/build_s32_narration_signoff_html.py`](_gen/build_s32_narration_signoff_html.py)
- 簽核稿 [`REVIEW-ch03_chain_rule-s32-narration-signoff.html`](REVIEW-ch03_chain_rule-s32-narration-signoff.html)

---

## 6. 收斂判定

| 閘 | 讀者 | blocking | advisory | 狀態 |
|---|---|---|---|---|
| Tier 0 | `derive_spoken --check` | — | — | `parity OK` |
| gate-1 | `narration-faithfulness-audit` subagent（Claude Opus 5，免費） | 0 | 3 → 回歸後 1（R2-01） | 已關閉 |
| gate-1 回歸 | 同上 | 0 | R2-01 由主對話修正（`52962e0`） | 已關閉 |
| gate-2 | agy `gemini-3.1-pro-high`（計費，2026-09-14 核准） | **1（N2-01）** | 0 | 修後回歸 0/0，已關閉 |

**依 rubric §收斂線（`blocking == 0`）＝ NFA 通過。**

**commit 索引（`git log --grep="NFA"` 可撈回）：**

| commit | 內容 |
|---|---|
| `ae840f3` | gate-1 三條 advisory 落地 ＋ D5 新慣例入契約 |
| `52962e0` | R2-01：gate-2 prompt 的判準對齊 §3.1（對 `say:` 判） |
| `201281d` | N2-01：指數搬進 LaTeX，D2 parity 恢復 |

---

## 7. 已知未處理（backlog）

- **`derive_spoken.py` 的 `MD_CONFIG_AND_CONVENTIONS` §二 慣例摘錄表未收 D5 新列。**
  該表是 `_narration_spoken.md` 的檔頭樣板，屬 **pipeline 共用 code**；改它會讓 §3.1
  `ch03_trig_derivatives` 的生成檔一併漂移，而本輪的工作範圍**不得碰 §3.1**。
  權威表（[`NARRATION-FAITHFULNESS-RUBRIC.md`](NARRATION-FAITHFULNESS-RUBRIC.md):51）已收，
  摘錄表落後一列；下次動到共用層時一併補，並同輪重生兩節的衍生檔。

---

*本報告為 §3.2 A4「旁白雙版落地」的完成判準文件。*
