# CLAUDE.md

本檔案為本儲存庫提供給 AI 代理（Claude Code、Codex 等）的專案層級指引，是這份指引的**權威版本**；[`AGENTS.md`](AGENTS.md) 僅為指向本檔的指標,內容不重複。儲存庫的完整結構、preamble 與建置規則以權威性文件 [`README.md`](README.md) 為準；內容撰寫規則以 [`CONTENT_SPEC.md`](CONTENT_SPEC.md) 為準。

## 文件撰寫語言

- **README 一律以繁體中文書寫。** 這包含根目錄的 [`README.md`](README.md) 以及子資料夾中屬於本專案的 README（例如 [`video/README.md`](video/README.md)）。新增或修改 README 時都比照辦理。
- **必要之處保留原文，不翻譯：** 程式碼區塊、檔案路徑與連結、shell 指令、環境變數、識別碼（scene id、export 名稱、欄位名）、以及專有名詞與技術術語（Manim、LaTeX、Gemini、TTS、CI、PR、Mode A/B/C 等）。
- 其餘散文、標題、表格的說明文字一律使用繁體中文。
- 第三方依賴（`.deps/`、`.deps_f5/`、`.deps_voiceover/`）與 git 工作樹（`.claude/worktrees/`）中的 README 不在此規則範圍內，不要改動。

## 付費 API 調用須先經同意

- **每次調用任何計費的外部 API（如 Gemini TTS、Gemini 文字／影像生成等）之前，都必須先取得使用者明確同意，不可自行調用。** 批次合成（例如整節旁白 TTS、整章重跑）一律先說明：這次要調用什麼模型、預估用量（beat 數／音訊秒數）與成本，經同意後才執行。
- 不計費、不連網的離線路徑不在此限，可逕行執行——例如 `tts.py --backend mock`（寫靜音 WAV 驗 manifest／時序）、本地 Manim render、ffmpeg mux/concat。
- 取得一次同意即代表該次明確說明的工作範圍獲准；範圍變更（換模型、加場景、重跑）需重新徵得同意。

## 跨對話記憶寫進版控文檔（不寫本地 memory）

- **做總結、記筆記、留任何跨對話／跨機器的知識時，一律寫進會 git 上去的文檔**，**不要只記在本地的 Claude memory**（`~/.claude/.../memory/`，含 `MEMORY.md`）。
- **原因：** 使用者常換電腦作業；本地 memory 不隨 repo 走、換機就消失，只有版控文檔會跟著 git 到每台機器。
- **寫哪裡：** 進度／狀態寫進該產線的 `REBUILD_STATUS.md`（既有的跨對話進度錨）；工具用法／參考寫進對應的 `README.md`；格式／資料流契約寫進 `DESIGN.md`；內容方法論寫進 `CONTENT_METHODOLOGY.md`。找不到合適的既有文檔時，先問使用者要放哪，不要默默只記進本地 memory。

## 撰寫／審查的既有慣例（原存於本地 memory，依上節規則搬進版控）

- **與使用者對話一律用繁體中文**（LaTeX／程式碼、套件名、檔名、技術術語保持英文原樣）。
- **做 doc／code review 時分清四級，不要混為一談：** ① 真衝突／違反既定規則（要修）② discoverability gap（補文件即可，非矛盾）③ editorial drift 風險（低優先，不是 finding）④ 非 finding（如示例覆蓋面差異）。**Framing：** 從「目前被 review 的樹的現況」出發，不要把 session 內未 commit／未 merge 的變更當既成事實；語義等價的用詞差異不算 inconsistency。Over-reporting 會稀釋真正高優先項。
- **三-mode 撰寫流程（root [`README.md`](README.md) §Mode B）下，Mode B 的稽核裁決與發現寫進該次修正 commit 的 message body**（subject ≤70 字、body 逐條：原本是什麼、為何不妥、改了什麼、引用證據），好讓未來對話用 `git log --grep="Mode B"` 撈回。參考 commit：`112aa5c`、`0ef06ee`。純 Mode A 或例行 bugfix 不適用。
- **以下四項 preamble／style 現狀是使用者 2026-04-21 審查後刻意保留的，勿再當遺漏重提：** 不開 `showonlyrefs`、維持 `\raggedbottom`+`[H]`、題組用 `exercise` 環境（不另立 `problems` newlist）、不加 `csquotes autostyle`（引號靠 `style_lint.py`）。情境真變了再重評，並明講「原本你選擇保留，但現在 X」。
