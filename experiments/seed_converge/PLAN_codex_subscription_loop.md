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

> ✅ **已於 2026-06-03 上網覆核**（OpenAI 官方文件 + GitHub），結論與修訂見 [§8](#8-查證與修訂2026-06-03-claude-code-上網覆核)：地基成立、Windows 可放寬、另有實作改善與一條新 caveat。

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

## 8. 查證與修訂（2026-06-03，Claude Code 上網覆核）

針對 §2 的命門事實做了線上覆核（OpenAI 官方 developers／help 文件 + `openai/codex`
GitHub issues，2026-06）。**結論：地基成立，且 Windows 比原本設想的好；另發現幾個直接
改善實作路徑的事實，與一條新 caveat。**

**§2 事實覆核：**

- ✅ **`codex exec` 走訂閱**：CLI 登入可選「Sign in with ChatGPT account or API key」
  （Plus/Pro/Business/Edu/Enterprise）；官方有 `exec` 腳本化與 non-interactive 專頁；
  用量計入 plan 的 agentic usage limit（不另計 token 費）。
- ✅ **Windows 原生（比原設想好）**：官方明文「Use Codex on Windows with the native …
  CLI」，原生兩種 sandbox（elevated 優先／unelevated fallback，`config.toml` 設）；
  **WSL2 改列「可選 fallback」非必須**。→ §2.3 與 §5 的「Windows 要 WSL／最差走 WSL」
  hedge 可放寬：原生為預設路徑，WSL 只在原生 sandbox 不合用時才需要。

**實作路徑因此更穩（直接解掉先前疑慮）：**

- **唯讀是預設**：「By default, `codex exec` runs in a read-only sandbox」，並可
  `--sandbox read-only` 明示；要寫檔才需 `--sandbox workspace-write`。→ §5 的
  single-writer 紀律幾乎零成本，預設就成立。
- **prompt 走 stdin／檔案**：`cat prompt.txt | codex exec -`（或 `codex exec -` 讀
  stdin）。→ 解掉「幾千字含 LaTeX 的 auditor prompt 不能當 shell argv 傳」的脆弱點，
  不必硬塞參數。
- **findings JSON 可強制結構化**：`codex exec --output-schema ./schema.json` 依 JSON
  Schema 約束輸出；`-o`／`--output-last-message <path>` 把最終訊息落檔。→ 比靠
  `run.py:_extract_json` 從聒噪 stdout 刮 JSON 更可靠；步驟 6.2(c) 的解析風險大幅
  降低（`_extract_json` 留作保險）。

**新增 caveat（補進 §5）：**

- **撞配額後，CLI 內回退 API key 不可靠**（`openai/codex` issue #5823）：ChatGPT Plus
  用量上限是硬牆，且 CLI 在撞牆後切換到 API key 有 bug。→ 別把架構建立在「撞牆就無縫切
  API」的假設上；配額管理（per-section 限次、人在收斂閘）是唯一可靠防線。

**方法論修訂（原計畫未提，補記）：**

- **「只換嘴」低估了改動範圍**：舊 `run.py` 是一支 Python `run_loop` 同時驅動 drafter
  （API）與 auditor（API）。新形狀中 **drafter＝Claude 這個 agent 本身**，`run_loop`
  的「drafter 半邊＋無人迴圈」是被 Claude 取代、非照用。真正沿用的是 `auditor_prompt`
  ＋ `_extract_json` ＋ blocking/advisory 四級契約。換的是整個 orchestration 模型，不是
  一行 transport swap（§3「只換嘴」、§6.4「其餘照用」據此修正理解）。
- **丟了「中立第三方評分」這層**：`SYNTHESIS.md` 原設計讓 Claude 在迴圈外當中立評分者
  （"Claude 不進迴圈"）。新計畫把 Claude 拉進迴圈當寫手後，迴圈產出的中立裁判只剩
  「人」。原設計多一層外部裁判的安全網沒了——不致命（人本在收斂閘），但需明列為已知
  取捨。可考慮偶爾請第三模型（如 Gemini）對成稿抽查，補回外部視角。

**注意：本次轉向與「核心幻覺假說」正交。** 換訂閱 transport 只省了錢／配額，沒讓你更接近
`SYNTHESIS.md §4` 的關鍵 open question（兩模型會不會一起替幻覺背書）。步驟 6.5（高風險節
壓測）才是決定「這條線要不要併進正式講義流程」的真正關卡。

**來源：** `developers.openai.com/codex/cli`、`/codex/windows`、`/codex/noninteractive`；
`help.openai.com` article 11369540；`github.com/openai/codex` issue #5823。

## 9. 實機煙霧測試（2026-06-04，Claude Code）

在本機（Windows）實際裝好 Codex CLI 並打通最小 `codex exec` 呼叫，驗證 §6.1–§6.2 的
(a)(c) 管路。**環境：** `codex-cli 0.136.0`（npm `@openai/codex` 全域安裝）、
`codex login status` → 「Logged in using ChatGPT」（訂閱認證，非 API key）。最小呼叫成功
回 schema-conforming JSON、`-o` 落檔可讀、`--sandbox read-only` 全程不改檔。**踩到三條會
反覆中招的坑，記下來避免重犯：**

1. **`codex exec` 的 stdin 一定要收到 EOF，否則永久卡死。** prompt 必須用管線餵入並以
   `-` 收尾——`Get-Content prompt.txt -Raw | codex exec … -`（或 `… | codex exec -`）。
   **不要**在非 TTY／背景環境把 prompt 當裸參數傳：codex 偵測到 stdin 是 pipe 就會額外讀
   stdin 當 `<stdin>` 區塊，等一個永不來的 EOF（背景執行器不關 stdin）→ hang。症狀：輸出
   停在 `Reading additional input from stdin...`。這也是 §6.2 走 stdin（而非 argv）的硬
   理由，強化 §8「prompt 走 stdin／檔案」。

2. **`--output-schema` 必須符合 OpenAI 嚴格結構化輸出規則，否則 400 `invalid_json_schema`。**
   兩條硬規則：(a) `properties` 裡**每一個 key 都要列進 `required`**（不允許選填欄位）；
   (b) **不吃 `minimum`／`maximum`** 這類數值約束關鍵字（用 `enum` 取代，或交散文約束）。
   → findings schema 的 `level` 改用 `"enum":[1,2,3,4]`、`additionalProperties:false`
   且全欄位 required；`run.py:auditor_prompt` 的 JSON 契約照搬時要先這樣改寫過 schema。

3. **預設模型 `gpt-5.5` 跑 `reasoning effort: xhigh`，配額成本不低。** 連「回一個
   `{ok:true}`」的瑣碎呼叫都用掉 **~11,052 tokens**。真正的 auditor 呼叫（house rules＋
   seed＋整段草稿）一次數萬 token 跑不掉——這把 §5「配額是真正成本」從抽象變具體：xhigh
   會放大配額消耗。需要省時可用 `-m`／`-c` 調模型或 reasoning effort，但 auditor 要抓微妙
   數學錯，高 reasoning 通常值得，取捨自行斟酌。

**接續狀態：** 管路（§6.1 ＋ §6.2 的 (a) 認證、(c) 可解析結構化輸出）已驗通；真正的
「草擬 §1.1 → auditor 審 → 收斂」內容試跑**刻意暫停**，等先把講義「擴寫方向／brief」討論
定案再跑——auditor 只驗正確／忠實／格式，無法驗方向，方向需人先定（見換機接續時的內容
方向討論）。
