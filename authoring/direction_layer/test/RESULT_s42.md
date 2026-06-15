# 測試結果：方向層流程首跑（§4.2，高風險節）

> 中立記錄。direction_layer 流程（[`../../../CONTENT_DIRECTION.md`](../../../CONTENT_DIRECTION.md)）在一個高風險節上的端到端首跑。
> 日期：2026-06-04，分支 `experiment/seed-converge`。
> 配套：`seed_s42.md`／`brief_s42.md`／`draft_s42.tex`／`audit_findings_s42.txt`（v1）／`audit_findings_s42_v2.txt`（v2）。

## Run metadata
- **節**：§4.2 Continuity and the Exponent Law for e^x（手稿 `2023-11-4-ExponentialFunction` p.3–10）。
- **角色**：Claude＝唯一寫手（drafter）；Codex CLI `gpt-5.5`（reasoning xhigh, `--sandbox read-only`，走 ChatGPT 訂閱）＝advisory auditor。
- **流程**：① 轉錄＋①-verify → ②③ 方向 brief（折衷）→ ④ 擴寫 → ⑤ audit→fix→re-audit。
- **結果**：v2 `converged=true`、`blocking=0`。每跑 ~30k 訂閱 token（不計費）。

## 流程走過
1. **① intake**：掃描 → 轉錄成 `seed_s42` → 人核對忠實度（沒問題）。**關鍵發現**：手稿在 Cauchy⟺convergent 明白 punt（“we shall not prove this theorem”）。
2. **②③ 方向**：最大叉路＝Cauchy⟺convergent 證或不證。③ 人裁＝**折衷**（陳述＋trivial 方向＋completeness remark，不證 B-W）。刻意偏離已簽核書（全展開 B-W）。
3. **④ 擴寫**：朝 brief 寫 `draft_s42`（~165 行）；手稿數學為主軸、加法標 `% expansion:`。
4. **⑤ 審查**：
   - **v1**：1 blocking（math）＋2 advisory。blocking＝我擴寫時加的一句**過度推廣**（「Cauchy 準則在 complete ordered field 等價且反之」——一般序體缺 Archimedean 時反向不成立）。順帶**暴露編碼 bug**（見下）。
   - **fix**：F1（收斂回 ℝ）＋F2（continuity theorem 提前＋proof sketch）＋F3（caution 拿掉「source manuscript」字樣）＋修編碼。
   - **v2**：`converged=true`、`blocking=0`，3 條 advisory（continuity sketch 可選展開；2 條 house-rule → linter）。seed/brief 完整 UTF-8 進 Codex，**direction-conformance 實覆蓋且通過**（auditor 自述：遵守折衷、含必要 examples、略過 history/application、沒證 B-W）。

## Takeaways
1. **核心幻覺假說首次真壓測 → 正面（一個樣本）。** 獨立第二模型抓到我擴寫引入的微妙過度推廣，未背書。**風險出在「模型加的 flourish」、非手稿骨架**——印證「手稿當數學主軸＋auditor 盯擴充」的設計。
2. **方向層可檢核。** 折衷寫進 brief 後，auditor 據此確認「照走、沒過度展開 B-W」，也沒把刻意省略當缺陷。四級紀律守住、無 L1 灌水（比 `seed_converge` full1 乾淨）。
3. **loop 一輪修正即收斂**（audit→fix→re-audit→blocking=0），合「停在乾淨 audit」紀律。

## 工程坑（修法已落地、v2 驗證）
- **非 ASCII 被重編碼成亂碼**：組 prompt 時 `Get-Content`（ANSI 預設）＋ PowerShell pipe 把中文／Unicode 數學符號糊掉 → auditor 收到糊掉的 seed/brief（v1 的 faithfulness/direction 覆蓋因此打折）。
- **修法**：`[System.IO.File]::ReadAllText`（UTF-8 讀）＋ `cmd /c "codex exec - … < prompt"`（cmd 的 `<` 餵原始 bytes，繞過 PS pipe 重編碼）＋ 一道 CJK regex 護欄（`[一-鿿]`）擋下萬一仍亂碼。v2 已驗證中文完整進 Codex。

## 對照已簽核 §4.2（ground truth）
- **Cauchy⟺convergent**：簽核版全展開（Cauchy-bounded＋單調子序列＋Bolzano–Weierstrass＋雙向）；實驗版折衷（陳述＋forward＋remark）。實驗版**更貼手稿原意**（手稿本就 punt）、更貼 HS 自學語域；簽核版更自足。
- **worked example**：實驗版 2（指數律數值＋`Σ(−1)^n/n!`）；簽核版 1。
- **篇幅**：實驗版 ~165 行；簽核版 ~287 行。
- **correctness**：兩版最終皆正確；但實驗版**出廠時有一處過度推廣**（人寫版沒有），靠 adversarial audit 抓回。

## 限制
- 單節、單樣本、低風險對照節未跑；核心假說只得一個正面數據點，**勿外推**。
- auditor run-to-run 會飄；重要判斷宜多跑取聯集（本次僅單跑）。
- 流程本身仍 v0.1，未畢業成正式 doc。
