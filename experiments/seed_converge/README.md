# 實驗：手稿當種子 → 兩模型自動收斂

隔離的一次性實驗，回答講義重構的一個問題：**若一個模型在稀疏手稿種子上自由
大幅擴寫，另一個模型自動二次審核、兩者無人介入地來回收斂，結果是抓掉幻覺、
還是替一個雙方都同意的幻覺背書？**

陣容可切換（`--drafter`/`--auditor`）。**§1.1 首跑用 Gemini 起草 ↔ DeepSeek 審核**，
結果見 [`RESULT.md`](RESULT.md)。Claude **不進迴圈**，跑完後當中立第三方，對照已簽核的
§1.1（[`chapters/ch01_foundations.tex`](../../chapters/ch01_foundations.tex) 第 16–268 行）評分。

## 檔案

| 檔 | 用途 |
|---|---|
| `run.py` | harness：起草↔審核自動收斂迴圈、計費三閘、容錯 JSON、落檔 |
| `seed_s11.md` | §1.1 的 8 條稀疏種子（只有數學骨幹） |
| `rules.md` | 蒸餾版寫作契約（register／環境集／顯示／`% expansion:` 標記／correctness） |
| `out/<run>/` | 每次 run 的產出（**gitignored**） |
| `RESULT.md` | Claude 跑完後的對照評分（進 git） |

工程慣例完全比照 [`video/pipeline/review_pack.py`](../../video/pipeline/review_pack.py)：stdlib `urllib`、OpenAI 相容
`/chat/completions`、env-var key、`--dry-run`/`--confirm`/`--smoke` 計費閘。

## 跑法

```powershell
# 1) 免費：寫出 prompts + 印 token/成本估算，不打 API
python experiments/seed_converge/run.py --dry-run

# 2) 設好金鑰（會員訂閱不通用，需 API key；Gemini 可用 AI Studio 免費 tier）
$env:OPENAI_API_KEY = "sk-..."
$env:GEMINI_API_KEY = "..."

# 3) 驗管路：只跑一輪（1 起草 + 1 審核，幾分錢）
python experiments/seed_converge/run.py --confirm --smoke

# 4) 跑完整 bounded 迴圈（預設 ≤4 輪）
python experiments/seed_converge/run.py --confirm
```

模型 id 走旗標、`--dry-run` 會印出來確認（預設值未必是當下的確切 id）：

```powershell
python experiments/seed_converge/run.py --drafter openai:gpt-5.1 --auditor gemini:gemini-2.5-pro --confirm
```

## 收斂與終止

每輪：審核模型對草稿出 strict-JSON findings（四級分類 + `converged` 旗標）。
無 level-1/2 actionable（或 auditor 自宣 `converged`、或達 `--max-rounds`、或
草稿不再變動）即停。每輪的 `round_NN_draft.tex` 與 `round_NN_findings.json`
全部落檔；`trace.md` 是人讀的收斂敘事，`usage.json` 記 token 與估算成本。

## 計費（CLAUDE.md）

`--confirm` 會計費。金鑰只從環境變數讀，絕不進旗標、不寫檔、不 log。一節估
約 $0.10–0.60（placeholder 價）。先 `--dry-run` 看精確估算、再 `--smoke`
驗一發、最後才整迴圈。

## 範圍外（刻意不做）

不碰正式講義流程、不碰 `chapters/*.tex`、不碰凍結中的 `video/`。不寫 parser／
schema 進正式產線（format 未定）。只跑 §1.1 一節，驗證有價值再談擴大。
