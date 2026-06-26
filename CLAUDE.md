# CLAUDE.md

本檔案為本儲存庫提供給 AI 代理（Claude Code、Codex 等）的專案層級指引，是這份指引的**權威版本**；[`AGENTS.md`](AGENTS.md) 僅為指向本檔的指標,內容不重複。儲存庫的完整結構與建置規則以權威性文件 [`README.md`](README.md) 為準；內容撰寫規則以 [`CONTENT_SPEC.md`](CONTENT_SPEC.md) 為準。

## 產線一覽

| 產線 | 路徑 | 說明 |
|------|------|------|
| HTML 講義 | `handout/` | MathJax/KaTeX＋JS paginator；fragment → print-standalone 組裝 |
| Manim 影片 | `video/` | 旁白＋動畫＋TTS；`make.py` 建置（詳見 [`video/README.md`](video/README.md)） |
| 舊 LaTeX 講義 | `legacy/tex_handout/` | 已凍結，僅供參照 |

> **講義「完成一章的完整閘序」**（Mode A 六階 → Mode B → Mode C ①補題目＋②軟深度 → 圖機會/正確性 → 數學 M1–M8 → S·A·V，含各閘 subagent／rubric／雙閘／Codex 調用紀律／「做完＝與 Ch1/Ch2 同級」定義）見權威總覽 [`handout/PIPELINE.md`](handout/PIPELINE.md)。

## 常用指令速查

```bash
python handout/build.py           # 建置全部講義章節（可接 ch01 只建一章）
python video/make.py --quality high  # 1080p 渲染影片（預設品質）
python tools/doctor.py            # 環境健康檢查
tts.py --backend mock             # 離線 TTS mock（不計費，可逕行）
```

## 文件撰寫語言

- **README 一律以繁體中文書寫。** 這包含根目錄的 [`README.md`](README.md) 以及子資料夾中屬於本專案的 README（例如 [`video/README.md`](video/README.md)）。新增或修改 README 時都比照辦理。
- **必要之處保留原文，不翻譯：** 程式碼區塊、檔案路徑與連結、shell 指令、環境變數、識別碼（scene id、export 名稱、欄位名）、以及專有名詞與技術術語（Manim、LaTeX、Gemini、TTS、CI、PR、Mode A/B/C 等）。
- 其餘散文、標題、表格的說明文字一律使用繁體中文。
- 第三方依賴（`.deps/`、`.deps_f5/`、`.deps_voiceover/`）與 git 工作樹（`.claude/worktrees/`）中的 README 不在此規則範圍內，不要改動。

## 影片渲染解析度

- **除非使用者特別要求，否則一律以 1080p 渲染**（`make.py --quality high`）。

## 付費 API 調用須先經同意

- **每次調用任何計費的外部 API（如 Gemini TTS、Gemini 文字／影像生成等）之前，都必須先取得使用者明確同意，不可自行調用。** 批次合成（例如整節旁白 TTS、整章重跑）一律先說明：這次要調用什麼模型、預估用量（beat 數／音訊秒數）與成本，經同意後才執行。
- 不計費、不連網的離線路徑不在此限，可逕行執行——例如 `tts.py --backend mock`（寫靜音 WAV 驗 manifest／時序）、本地 Manim render、ffmpeg mux/concat。
- 取得一次同意即代表該次明確說明的工作範圍獲准；範圍變更（換模型、加場景、重跑）需重新徵得同意。

## 安裝環境：缺套件／軟體先問、勿造輪子替代、裝完更新文檔

跨機環境的權威清單在 [`ENVIRONMENT.md`](ENVIRONMENT.md)，可執行版是 [`tools/doctor.py`](tools/doctor.py)（換機先跑它看缺什麼）。在此前提下：

- **缺套件／軟體先問，不要自行安裝。** 偵測到本機缺某個 pip 套件、系統 binary 或工具（如 `ffmpeg`、LaTeX、Node、Chrome、某個 pip 套件）時，**先說明要裝什麼、為什麼、怎麼裝（指令），經使用者同意才裝**，不可自行 `winget`／`pip install`。例外：照既有 [`requirements.lock`](requirements.lock)／`ENVIRONMENT.md` **重現「已議定」的環境**（例如跑 `tools/setup.ps1` 從 lock 裝）是重建、非新增，可逕行。
- **不要自行造輪子做替代。** 缺東西時**預設把正版裝起來**，不要為了繞過而手刻替代（hack 一條 code path 避開缺的 binary、自寫替代工具）。若你判斷某個替代做法確實更好，**講出來讓使用者定奪**，不要默默做（與下方 Karpathy §1「攤開取捨」、§2「不投機」一致）。前例：`ffmpeg`／`ffprobe` 選「裝真套件」而非「改 code 繞過 `ffprobe`」（策略 A，見 `video/REBUILD_STATUS.md`）。
- **裝完一定更新相關文檔，確保新電腦對得上。** 任何環境變更後同一輪內補齊：pinned 版本進 [`requirements.lock`](requirements.lock)／對應 `requirements.txt`、新需求寫進 [`ENVIRONMENT.md`](ENVIRONMENT.md)、檢查項加進 [`tools/doctor.py`](tools/doctor.py)（必要時連 `tools/setup.ps1`）。**驗收標準＝在新機 `python tools/doctor.py` 能據此把環境對齊到全綠。**

## 跨對話記憶寫進版控文檔（不寫本地 memory）

- **做總結、記筆記、留任何跨對話／跨機器的知識時，一律寫進會 git 上去的文檔**，**不要只記在本地的 Claude memory**（`~/.claude/.../memory/`，含 `MEMORY.md`）。
- **原因：** 使用者常換電腦作業；本地 memory 不隨 repo 走、換機就消失，只有版控文檔會跟著 git 到每台機器。
- **寫哪裡：** 進度／狀態寫進該產線的 `REBUILD_STATUS.md`（既有的跨對話進度錨）；工具用法／參考寫進對應的 `README.md`；格式／資料流契約寫進 `DESIGN.md`；內容方法論寫進 `CONTENT_METHODOLOGY.md`。找不到合適的既有文檔時，先問使用者要放哪，不要默默只記進本地 memory。

## 撰寫／審查的既有慣例（原存於本地 memory，依上節規則搬進版控）

- **與使用者對話一律用繁體中文**（LaTeX／程式碼、套件名、檔名、技術術語保持英文原樣）。
- **做 doc／code review 時分清四級，不要混為一談：** ① 真衝突／違反既定規則（要修）② discoverability gap（補文件即可，非矛盾）③ editorial drift 風險（低優先，不是 finding）④ 非 finding（如示例覆蓋面差異）。**Framing：** 從「目前被 review 的樹的現況」出發，不要把 session 內未 commit／未 merge 的變更當既成事實；語義等價的用詞差異不算 inconsistency。Over-reporting 會稀釋真正高優先項。
- **三-mode 撰寫流程（root [`README.md`](README.md) §Mode B）下，Mode B 的稽核裁決與發現寫進該次修正 commit 的 message body**（subject ≤70 字、body 逐條：原本是什麼、為何不妥、改了什麼、引用證據），好讓未來對話用 `git log --grep="Mode B"` 撈回。參考 commit：`112aa5c`、`0ef06ee`。純 Mode A 或例行 bugfix 不適用。
  - **commit-grep 分流（2026-06-15）：** 上述 `Mode B` 是**講義**線。**video 旁白的忠實稽核已改名 NFA**（旁白忠實稽核，原 video「Mode B」；契約 [`video/content_scripts/_audit/NARRATION-FAITHFULNESS-RUBRIC.md`](video/content_scripts/_audit/NARRATION-FAITHFULNESS-RUBRIC.md)），其裁決同樣寫進修正 commit body，但用 `git log --grep="NFA"` 撈回（與講義 `Mode B` 分流，免兩條線混在同一 grep）。
- **給使用者審核的交付物要用「打開就能讀」的形式（2026-06-12 使用者要求）：** 含數學式的審核文件**不要**交塞滿生 LaTeX 的 `.md`，改產出 standalone HTML（MathJax/KaTeX CDN，雙擊即開、數學即渲染）或其他可直接閱讀的形式。版控紀錄性質的文檔不在此限；凡「等使用者過目裁決」的東西一律照此辦理。
- **每完成一輪撰寫後也要產 HTML 報告（2026-06-15 使用者要求）：** 不只「待裁決」的候選／findings 要 HTML——**凡完成一輪內容撰寫（Mode A／C 等），都要對實際寫入的內容另產一份 standalone HTML 報告**（MathJax/KaTeX CDN、雙擊即開、數學即渲染），逐條呈現所寫段落＋locus＋`[source:]`＋該輪 Mode B 結果，供使用者過目，不要只在對話裡給文字摘要。比照 [`handout/_audit/REVIEW-ch01-modec-candidates.html`](handout/_audit/REVIEW-ch01-modec-candidates.html) 的形式，檔名用 `REVIEW-…-applied.html` 之類，與「候選／裁決稿」分開。
- **審核 finding 修完後必須回歸審核（2026-06-12 使用者要求）：** 修完 blocking／advisory finding 後，不可直接宣告完成——必須對修改過的項目重新跑一輪審核（Codex 或手動比對均可），確認修改本身沒有引入新問題。回歸審核的結果附在原稽核文檔中記錄。

## 程式／工程任務的行為準則（Karpathy guidelines）

源自 [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills)（Andrej Karpathy 對 LLM 寫程式常見毛病的觀察）。**取捨：** 偏向謹慎優先於速度；瑣碎任務自行斟酌。**適用範圍以 `video/` 產線、build 工具、腳本等程式／工程工作為限；不適用於講義內容撰寫**——Mode A 散文密度仍以「prefer richness、標 `[source:]`、不自我審查」為準（見 [`video/CONTENT_METHODOLOGY.md`](video/CONTENT_METHODOLOGY.md)），下方第 2 條的「最少程式碼」指 code，不指內容篇幅。

- **1. 想清楚再動手（Think Before Coding）——不要臆測、不要藏起困惑、把取捨攤開講。**
  - 明確說出假設；不確定就問，不要默默猜。
  - 有多種解讀時全部列出來，不要默默選一個。
  - 有更簡單的做法就講，必要時據理力爭。
  - 卡住就停下，指名哪裡不清楚，然後問。
- **2. 簡單優先（Simplicity First）——用最少的 code 解決問題，不寫投機性的東西。**（僅限程式碼，非內容篇幅）
  - 不做沒被要求的功能；不為一次性 code 建抽象層。
  - 不加沒被要求的「彈性／可設定性」；不為不可能的情境寫錯誤處理。
  - 寫了 200 行但 50 行就夠就重寫。自問：「資深工程師會不會嫌它過度複雜？」
- **3. 外科手術式修改（Surgical Changes）——只動非動不可的地方，只清自己製造的爛攤子。**
  - 不要順手「改善」相鄰的 code、註解或排版；不要重構沒壞的東西。
  - 比照既有風格，即使你會用別的寫法。
  - 看到無關的 dead code，提出來、不要擅自刪；只移除「因你的改動」而變成沒用到的 import／變數／函式。
  - 檢驗：每一行改動都能直接追溯回使用者的要求（與上節四級 review、不 over-report 一致）。
- **4. 目標驅動執行（Goal-Driven Execution）——先定義成功標準，再迴圈到驗證通過。**
  - 把任務轉成可驗證的目標：「加驗證」→「先為非法輸入寫測試再讓它過」；「修 bug」→「先寫能重現的測試再讓它過」；「重構 X」→「確保前後測試都過」。
  - 多步驟任務先給一個簡短計畫（步驟 → 驗證點）。成功標準夠強就能自行迴圈；「弄到能動」這種弱標準只會不斷需要釐清。
