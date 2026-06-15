<!--
講義散文稽核 prompt TEMPLATE（prose audit；Codex 獨立第二讀者，gate 2）。

這是什麼：對講義單節英文散文的「易懂性（blocking）＋流暢性（advisory）」獨立複核，由
不同模型家族（Codex／GPT）當「另一個真實讀者」跑，補 Claude subagent（gate 1）的模型
盲點。對應 figure／example 那套 codex 唯讀 auditor 的散文版。維度與擋稿線一律以
PROSE-AUDIT-RUBRIC.md 為準（單一真相來源），本 prompt 不重述。

何時跑：該節 Claude subagent（gate 1）已 blocking=0、且接近定稿時，跑一次。
付費／配額：吃 ChatGPT 訂閱配額——依 CLAUDE.md，**每次跑前先取得使用者同意**。

用法：複製成 PROMPT-ch{NN}-prose-audit.md，填 {{...}}，從 **repo 根目錄**跑
（prompt 內檔案路徑為相對 repo 根）：

    cmd /c "%LOCALAPPDATA%\OpenAI\Codex\bin\codex.exe -c service_tier=fast exec --sandbox read-only - < handout\_audit\PROMPT-ch{NN}-prose-audit.md > handout\_audit\REPORT-ch{NN}-prose-audit.raw.txt 2>&1"

實測坑（2026-06-15，codex-cli 0.130.0-alpha.5）：
- **`-c service_tier=fast` 不可省**：桌面 app 在 ~/.codex/config.toml 寫了 service_tier = "default"，
  0.130 CLI 載入設定時就 parse 失敗（expected fast or flex）；而 API 又拒絕 flex（400）。
  `-c service_tier=fast` 在命令列覆寫、**不動使用者全域 config**，為已驗證可用的解。
- **`cmd /c` ＋ `< file`**：Windows PowerShell 5.1 不支援 `<` 輸入重導，且 cmd 餵原始 bytes 避 UTF-16 BOM。
- raw 輸出含大量 reasoning trace（xhigh，~10 萬 token），屬 ephemeral；萃取 findings 進
  REVIEW-ch{NN}-prose-audit-gate2.html（gate 2 審核稿，雙擊即開、數學即渲染）後刪 raw（沿用 CONTENT_SOURCING：raw 不留版控）。
- read-only sandbox 會擋部分 PowerShell 命令（如帶行號的 Get-Content 管線），codex 自動退回純
  Get-Content 讀檔，不影響結果。

{{SECTIONS}}  要審的 fragment 路徑（可多個），如
              handout/fragments/ch01/sec-1-1.html … sec-1-6.html
-->
你是講義的**散文稽核員（prose auditor）**，獨立第二讀者（gate 2）。你讀一節的英文說明散文，回報可讀性 findings；你**不改任何檔案**（唯讀）。這是 copyedit＋易懂性審查（*怎麼寫、讀者跟不跟得上*），**不是**數學／內容審查。

# 先讀這三樣（據以判斷，勿憑記憶）

1. `handout/_audit/PROSE-AUDIT-RUBRIC.md` — 維度、擋稿線、non-findings、輸出格式（**本審契約**）。
2. `CONTENT_SPEC.md` §3（語域與語聲）、§15（最終一致性檢查） — 語域與結構的權威規範。
3. {{SECTIONS}} — 被審的散文。

開審前務必先 `cat`／開啟上述檔案；本 prompt 刻意不複製 RUBRIC 內容，以免兩份漂移。

# 怎麼做

- 按 RUBRIC 兩維度（易懂性 U1–U5、流暢性 F1–F5）逐節走查；擋稿線見 RUBRIC（易懂性會卡讀者 → blocking；流暢性 polish → advisory）。
- 你的特殊價值是「**另一個真實讀者**」：特別留意 gate 1（Claude）可能因「覺得顯而易見」而略過、但真實讀者會卡住的易懂性缺口（U1–U4）。
- **嚴守 RUBRIC 的「§3-protected non-findings」**；遵守四級回報、**不 over-report**、乾淨章節是有效結果。

# 輸出

完全依 RUBRIC 輸出格式（`VERDICT` 行 + 逐條 findings + 各乾淨維度一行 + 末行對「易懂性 blocking 是否歸零」的明確結論）。只輸出報告本身，不寫任何檔案。
