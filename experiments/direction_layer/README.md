# direction_layer —— 擴寫「方向層」設計（v0.1 draft）

> 隔離設計稿，`experiment/seed-converge` 分支。**未經實機測試。**
> 不碰 `chapters/*.tex`、pipeline、未 push 的 commit。

## 這資料夾是什麼

定義「**老師掃描手稿 → 完整講義一節**」之間缺的一層：**方向層**。

既有流程能查「對不對／完不完整／合不合規」，卻查不到「**這是不是我要的方向**」——一節可以數學全對、稽核 8/8，仍然是「往錯方向收斂得很精緻」。方向層補上這層，並用「**模型提案、人定奪**」（前置到擴寫之前）讓它**可檢核**。

權威設計稿：**[`RULE.md`](RULE.md)**。

## 為什麼跟 seed_converge 分開

| 資料夾 | 驗／定什麼 |
|---|---|
| [`../seed_converge/`](../seed_converge/) | **機制**：雙模型自動收斂、多模態圖 critic、訂閱制 review 迴圈。零件與壓測。 |
| `direction_layer/`（本資料夾） | **流程與規則**：方向 brief ＋ 人方向閘 ＋ 六階流程；把上述零件＋既有 Mode A/B/C 組成治理規則。 |

一句話：seed_converge 是「**能不能用**」，direction_layer 是「**怎麼用、往哪個方向用**」。

## 血統（站在哪些東西上）

- **起點問題**：有些手稿太簡略，撐不起教科書密度的例子。
- **改進、不打掉** [`../../README.md`](../../README.md) 的 Mode A/B/C —— 保留手稿主軸＋`% expansion:` 標記＋擴增稽核；新增方向層、機械化審查。
- **折入** seed_converge 的教訓（[`SYNTHESIS.md`](../seed_converge/SYNTHESIS.md)）與訂閱制 review 迴圈（[`PLAN_codex_subscription_loop.md`](../seed_converge/PLAN_codex_subscription_loop.md)）—— 後者即六階流程的 ⑤ 審查階段。

## 狀態與下一步

- **狀態**：v0.1 draft，流程已定、**未測**。
- **下一步**：挑 2–3 節真手稿跑完整六階流程（含**一個高風險節**正面壓測幻覺假說）→ 通過再把 `RULE.md` 畢業成頂層正式 doc（如 `CONTENT_DIRECTION.md`）並落工具（linter／`/audit-section`）。驗收門檻見 [`RULE.md`](RULE.md) §6。
