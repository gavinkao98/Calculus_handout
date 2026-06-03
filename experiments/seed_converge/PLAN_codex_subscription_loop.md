# 計畫：GPT（Codex CLI）↔ Claude（Code）訂閱制 review 迴圈

> 分支 `experiment/seed-converge`。日期：2026-06-03。換機接續用。
> 配套檔：`run.py`（重用其 prompt／JSON／loop 的「腦」）、`SYNTHESIS.md`（前一階段
> 的教訓）、`rules.md`（寫作契約）、`seed_s11.md`（§1.1 種子）。
> 本檔是「下一階段要做什麼、為什麼、怎麼驗收」，給回家換電腦後接續用。

---

## 0. 目標

讓 **GPT 給意見 → Claude 改 → 迭代收斂**，且**全走訂閱、不走 API（省錢）**。
使用者同時有 ChatGPT 與 Claude 訂閱，不想按 token 計費。

## 1. 為什麼是這個方向（關鍵轉向）

前一階段（`run.py`）走的是 **API↔API**：drafter／auditor 都打 OpenAI 相容
`/chat/completions`，用 `*_API_KEY`，**按 token 計費**——正是要避開的。

要用**訂閱**，正確形狀是 **CLI↔CLI**，不是 API↔API：

- **Claude Code**（這個 agent）跑在 **Claude 訂閱**上 → 當**改稿者**，$0 邊際成本。
- **Codex CLI** 可用 **ChatGPT 訂閱**登入 → 當**審查者**，$0 API。
- Claude Code 用 **Bash 直接叫 `codex exec`** 當子程序；它走訂閱、不碰 API 帳單。

## 2. 查證到的事實（2026-06-03）

1. **Codex CLI 支援 ChatGPT 訂閱登入**（Plus/Pro/Business/Edu/Enterprise）：
   `codex login` → 「Sign in with ChatGPT」，**不需要 API key、不按 token 計費**。
2. **`codex exec`（非互動、腳本化）也吃訂閱**：官方明寫「With your ChatGPT Plus
   plan… including scripted `codex exec` workflows」。← 這是命門：可從 Claude Code
   用 Bash 叫 `codex exec`，走訂閱。
3. **Windows 原生可跑**：Codex CLI 能在 PowerShell 用原生 sandbox 跑，**WSL 非必須**
   （仍有舊 issue 把 WSL 列為必要 → **待實機驗**，最差走 WSL）。

來源：
- https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan
- https://developers.openai.com/codex/cli
- https://developers.openai.com/codex/windows

## 3. 架構

```
Claude Code（Claude 訂閱，唯一寫手）
  編輯 §X.tex
     ↓
  Bash → codex exec "<auditor prompt>"   ← ChatGPT 訂閱，唯讀 reviewer，$0 API
     ↓
  讀 Codex 吐的 findings JSON → 改 .tex（帶 repo + linter + house rules）
     ↓
  再叫 codex exec 審 → blocking=0 → 人拍板採納（人在收斂閘）
```

**重用 `run.py` 的「腦」，只換「嘴」：**
- auditor system prompt（`run.py:auditor_prompt`）、blocking/advisory + 四級 triage
  契約、findings JSON schema、停在乾淨 audit 的紀律——**全部照用**。
- 只把 transport 從「API POST（`run.py:call`）」換成「subprocess `codex exec`」。
- 你花好幾輪調出來的護欄一條都不丟，成本從「每輪計費」變成「吃訂閱額度」。

## 4. 為何不選另外兩個

- **claude_codex_bridge（CCB）**：同一個 CLI↔CLI 點子的產品化版，但較重（tmux 面板
  + 手動 `/ask` 路由）、**Windows 要 WSL**（bridge 本身不支援原生 Windows）、不給
  blocking/advisory 收斂契約。直接 Bash 叫 `codex exec` 更簡、原生 Windows。CCB 只有
  「想看兩 agent 並排即時面板、手動分派」時才划算——那是 UX 偏好，非自動化需求。
- **GitHub PR + Codex**：Codex 雲端 review 也含在訂閱裡（不花 API 錢），但通用 PR
  review **不認 house rules／四級契約**（護欄繞過）、有 CI 來回延遲、要先 push。
  **留當一節「完稿後偶爾把關」，非每輪內迴圈。**

## 5. 風險 / caveats

- **訂閱用量上限**（per-5h／每週訊息數）是**真正的成本**（不是錢、是配額）。
  per-section 審幾次沒問題；無人狂跑會撞牆。
- **Codex 要鎖唯讀 reviewer**（read-only／suggest 模式），讓 Claude Code 當**唯一寫手**，
  避免兩邊同時改檔打架（single-writer 紀律）。
- **Windows 原生待實機驗**，最差走 WSL。
- 沿用 `SYNTHESIS.md` 的教訓：run-to-run 會飄 → 重要判斷多跑取聯集；格式交
  deterministic linter、不准擋收斂；**幻覺假說仍未壓測**（§1.1 太簡單）。

## 6. 下一步（可驗收步驟）

1. **環境檢查**：`codex --version`、登入狀態；確認走 ChatGPT 訂閱（非 API key）。
2. **一節手動試跑**（先驗做法、後落工具）：挑一節 → 用 `run.py:auditor_prompt`
   組 prompt → `codex exec`（唯讀）→ 檢查：
   - (a) 訂閱認證過不過；
   - (b) 肯不肯只吐 findings、不亂改檔；
   - (c) findings JSON 可不可解析（沿用 `run.py:_extract_json` 容錯）；
   - (d) Claude 改完 re-audit 收不收斂到 `blocking=0`。
3. **驗收門檻**：訂閱下穩定吐可解析 findings、且能 audit→fix→re-audit 到 `blocking=0`。
4. **過了再包工具**：作一個 `/audit-section` slash command 或 `run.py` 變體——把
   `call()` 的 API POST 換成 subprocess `codex exec`，其餘（prompt／JSON／loop）照用。
5. **真正的壓測**（SYNTHESIS 留下最關鍵 open question）：換**高風險節**（具名結果／
   微妙證明，如 Bolzano–Weierstrass、Cauchy 收斂）驗「兩模型會不會一起替同一個幻覺
   背書」。§1.1 幻覺面太低，壓不出來。

## 7. 換機接續備忘

- 分支 `experiment/seed-converge`，**隔離**；不碰 `chapters/*.tex` 與凍結的 `video/`。
- **新機要裝**：
  - Codex CLI（`codex login` → Sign in with ChatGPT，走 ChatGPT 訂閱）。
  - Claude Code（Claude 訂閱）。
- 配套檔（都在本資料夾）：`run.py`（重用 prompt/JSON/loop）、`SYNTHESIS.md`（教訓）、
  `rules.md`、`seed_s11.md`、本檔。
- ⚠️ 沿用 `SYNTHESIS.md` 的提醒：曾貼進對話的 API key 若還沒 rotate，先撤銷重發
  （本路線改走訂閱後，文字審不再需要 `DEEPSEEK_API_KEY`／`OPENAI_API_KEY`）。
