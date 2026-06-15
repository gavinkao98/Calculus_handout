# 散文稽核閘 — 驗證報告

> **目的：** 記錄 gate 1（Claude prose-audit subagent）的驗證，作為「為何信任這道閘」的版控憑據。
> **日期：** 2026-06-14。
> **相關檔：** [`PROSE-AUDIT-RUBRIC.md`](PROSE-AUDIT-RUBRIC.md)（契約）、[`PROSE-AUDIT-PROMPT.template.md`](PROSE-AUDIT-PROMPT.template.md)（gate 2 Codex）、[`../../.claude/agents/handout-prose-audit.md`](../../.claude/agents/handout-prose-audit.md)（gate 1 subagent）、[`REVIEW-ch01-prose-audit-gate1.html`](REVIEW-ch01-prose-audit-gate1.html)／[`REVIEW-ch01-prose-audit-gate2.html`](REVIEW-ch01-prose-audit-gate2.html)（兩道閘各一份審核稿，可雙擊開、數學即渲染）。

## 驗證了兩條路徑

### 1. 乾淨路徑（不 over-report、不誤砍 §3 鋪陳）
對第一章 7 個 fragment 跑 gate 1 → **blocking=0，4 tighten，5 optional**（明細見 [`REVIEW-ch01-prose-audit-gate1.html`](REVIEW-ch01-prose-audit-gate1.html)）。
各節稽核員一致正確地保護 §3 鋪陳（鼓勵連接詞、動機段、*Informally* gloss、*we*、刻意教學重複、topic-term recurrence），未誤砍；整章僅吐極少 advisory，無 over-report。

### 2. Blocking 路徑（盲測：同一節 §1.6 真實散文，外科式各種一缺陷）
中性檔名、與正式閘**完全相同**的 prompt（不提示「種了缺陷」），5 變體並行：

| 變體 | 種的缺陷 | 預期 | 實際 |
|---|---|---|---|
| a | 重型 ε-δ 定義**前無動機** | U1 Blocking | **U1 Blocking**（且刻意不重複報 U2）✅ |
| b | 重型定義**後無任何拆解** | U2 Blocking | **U2 Blocking** ✅ |
| c | 證明**抽掉三角不等式橋** | U3 Blocking | **U3 Blocking**（精準指出缺了選共同 x ＋ 三角不等式）✅ |
| d | ∞／M **記號先用後定義** | U4 Blocking | **U4 Blocking**（＋連帶抓出變體含的 U1、U2）✅ |
| e | control（無缺陷） | 0 Blocking | **0 Blocking**（U2 僅 advisory、F2 optional）✅ |

**關鍵對照：** b 與 e 用**同一個 Def 1.13**，只切換「定義後的拆解」有無 → b 判 U2 **Blocking**、e 判 U2 **advisory**。證明閘是對「讀者到底會不會卡」判，而非機械地查「定義框內有沒有 gloss」。

## 由驗證促成的 rubric 微調（2026-06-14 採納）

兩個 near-miss（ch01 §1.6 / §1.4 與盲測 e）顯示 rubric 字面可能被更機械的審查員（含 gate 2 的 Codex）誤讀，故收緊：

1. **U2**：白話重述可在 inline gloss **或定義前後相鄰散文**任一處；**只有附近完全找不到任何白話重述、讀者被卡在純符號上**才 blocking。inline 缺但相鄰散文已解拆 → 至多 advisory。
2. **U4**：forward-dependency 的 blocking **限於「讀者被晾住、無法從使用處重建其義」**；若使用處當場以散文 gloss、可重建 → 降為 advisory。

閘**現行行為已符合**這兩條（驗證即為證）；改字是把行為鎖死，保護未來 / Codex 不誤判。

## 微調回歸驗證（2026-06-14）

微調後以**更新的 rubric** 盲測邊界案例，確認兩條微調**雙向正確**（該擋的擋、該降的降）：

| 案例 | 條件 | 期望 | 結果 |
|---|---|---|---|
| variant-b | 重型定義，附近**無**任何白話重述 | U2 Blocking | **U2 Blocking** ✅ |
| variant-e | 同一定義，附近**有**白話重述 | U2 advisory | U2 Optional、0 blocking ✅ |
| variant-g | 散文裡承載性術語**無定義、無法重建** | U4 Blocking | **U4 Blocking** ✅ |
| variant-d／f | worked example 順序錯置，但算式**自我示範**可重建 | advisory | 0 blocking、U4 Tighten ✅ |
| 真 §1.4 | ∞ 記號先用，但使用處**當場 gloss** | advisory | 0 blocking ✅ |

**U4 的重要校準心得：** U4-blocking 是一條**高、以實質為準**的線——花了三個 fixture（d→f→g）才造出「真正晾住」的條件，因為在微積分情境下，一個 worked example 的算式步驟、或一句當場 gloss，幾乎總能讓有心的讀者重建。這是**特性**：U4 擋的是「讀者真的無從得知這是什麼」（散文裡承載性術語零定義），**不擋**「記號只是排在定義前面但可重建」這種純順序問題。若日後希望「純順序違規」也一律擋，那是另一條更嚴、走機械路線的規則，需另外加（與目前 substance-over-mechanics 的哲學不同）。

## 結論

4 條 blocking 線皆會觸發、歸維正確、control 乾淨、不 over-report；兩條 rubric 微調（U2／U4）回歸驗證**雙向正確** → **gate 1 可信**。
gate 2（Codex 獨立複核）已於 2026-06-15 對 ch01 整章執行，**亦 0 blocking**（與 gate 1 收斂，未見任一閘漏抓的 blocking）；findings 見 [`REVIEW-ch01-prose-audit-gate2.html`](REVIEW-ch01-prose-audit-gate2.html)。

## 現況與下一步（2026-06-15，機器切換存檔）

- **第一章散文稽核：完成。** 兩道閘整章 0 blocking；gate-1（G1-1…G1-9 ＋ A）與 gate-2（G2-1…G2-4）所有 advisory 已逐條裁決、套用進 `fragments/ch01/sec-*.html`，並 `python build.py ch01` 重組進 `chapter1-print-standalone.html`。逐條紀錄（old→new）見 [`REVIEW-ch01-prose-audit-gate1.html`](REVIEW-ch01-prose-audit-gate1.html)／[`REVIEW-ch01-prose-audit-gate2.html`](REVIEW-ch01-prose-audit-gate2.html)。
- **閘的基建：完成並接進流程。** rubric（含 U2／U4 refinement、`G1-/G2-` 編號慣例、HTML 交付物規定）、gate-1 subagent（`.claude/agents/handout-prose-audit.md`，因 `.claude/` 被 gitignore 故以 `git add -f` 強制納入版控）、gate-2 Codex 模板（含 `-c service_tier=fast` 實測坑）；已接進 README Mode B、CONTENT_SPEC §15、CONTENT_SOURCING 2.4、audit-dimensions dimension F。
- **下一步：把閘推到 ch02／ch03。** gate 1（Claude subagent）免費、隨時可跑；gate 2（Codex）需 ChatGPT 訂閱配額、跑前先徵使用者同意。每章各產 gate-1／gate-2 兩份 `REVIEW-chNN-prose-audit-gate{1,2}.html`。

## Mode C 第一輪（ch01 軟深度充實，2026-06-15）

第一章主軸於 2026-06-15 凍結（見 [`../../CONTENT_ROADMAP.md`](../../CONTENT_ROADMAP.md) Ch 1 entry）後，執行首次 Mode C 充實回合，範圍限定軟深度（intuition／application／caution／strategy）。

- **偵察：** 7 節並行 gap-walk，產 38 條候選；裁決稿 [`REVIEW-ch01-modec-candidates.html`](REVIEW-ch01-modec-candidates.html)。使用者裁定「13 條 high-confidence 動手，其餘待研究」。
- **已寫入（13 條，皆帶 `[pass: enrichment]` 標記）：** §1.1 Caution 1.1（\(f^{-1}\)≠倒數）＋ role-swap intuition；§1.2 arccos \([0,\pi]\)／arctan \(\mathbb{R}\) 兩條 why-intuition ＋ Caution 1.4（arccos/arctan 域限）；§1.3 Caution 1.5（表格陷阱 \(\sin(\pi/x)\)）＋ velocity application（\(v(2)=-24\)）；§1.4 Caution 1.6（\(\lim=\infty\)≠存在）＋ Strategy 1.2（找垂直漸近線）；§1.5 limit-laws intuition ＋ Caution 1.7（商定律須分母非零）；§1.6 ε-δ tolerance application ＋ challenge-response intuition。
- **連號維護：** Caution 全章重排為 1.1–1.7、Strategy 新增 1.2（原 1.2／1.3 → 1.3／1.4）。build.py 不自動編號；grep 確認無散文以編號交叉引用這些環境，重排安全。
- **Mode B 收尾（gate-1，範圍限定新 `[pass: enrichment]`）：** 6 節並行盲審，**整輪 0 blocking** → Mode C 通過。advisory 裁決：§1.4「suspect factor」用詞不一致 → 改為「the denominator's zero … cancelled by the numerator」；§1.6 容差長句 → 拆兩句；其餘 optional（§1.2 principal-range 順序、§1.4 step-1 子句、§1.6 輕度回響）裁定保留。修正後 `python build.py ch01` 重組。
- **figure 閘（新基建，與 prose 閘對稱）：** [`FIGURE-AUDIT-RUBRIC.md`](FIGURE-AUDIT-RUBRIC.md)（維度 D1–D8）＋ gate-1 subagent `.claude/agents/handout-figure-audit.md`（看 render 後 PNG、唯讀，`git add -f` 納版控）＋ render harness [`../_render/shot.mjs`](../_render/shot.mjs)（Node CDP 截圖；本機已裝 Node v24）。gate-2＝Codex `-i` 看圖、定稿前複核（計費、徵同意）。視覺審 run-to-run drift 為先前誤判已撤（見 `authoring/seed_converge/SYNTHESIS.md`）。
- **下一步：** ① gate-2（Codex）對這 13 條新散文獨立複核（計費、需同意）；② 其餘 25 條候選（figure-notes、medium、history 待驗源等）待使用者研究後再議。
