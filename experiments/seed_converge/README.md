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

每輪：審核模型對草稿出 strict-JSON findings，每條標 `category` + `blocking`
（**只有 math／faithfulness 錯誤 blocking=true**；`% expansion:`／`\index`／register
等格式 house-rule 屬 advisory、交給下游 linter，不擋收斂）＋ `level`（四級供人 triage）。
**無 blocking finding 即視為收斂**（數學正確、忠於種子，縱有格式 nit 仍收斂）。
迴圈**停在一次 audit**（達 `--max-rounds` 時不再多做一版未經審核的 revise），
或草稿不再變動。每輪 `round_NN_draft.tex` 與 `round_NN_findings.json` 全落檔；
`trace.md` 人讀敘事，`usage.json` 記 token／成本。

## 計費（CLAUDE.md）

`--confirm` 會計費。金鑰只從環境變數讀，絕不進旗標、不寫檔、不 log。一節估
約 $0.10–0.60（placeholder 價）。先 `--dry-run` 看精確估算、再 `--smoke`
驗一發、最後才整迴圈。

## 視覺層：figure_critic.py（多模態圖檢查）

文字審（run.py 的 DeepSeek）看不到 render 後的視覺缺陷。`figure_critic.py` 是
[`critic.py`](../../video/pipeline/critic.py) 的講義版：pymupdf 把含圖的 PDF 頁轉
PNG → 多模態模型（Gemini，`image_url`）→ 依 CONTENT_SPEC §10 圖規則出 defects（label
碰撞／出界／只靠顏色編碼／灰階存活）→ 人 triage。閘門同 run.py。

```powershell
python experiments/seed_converge/figure_critic.py --pdf <pdf> --pages 2,6 --dry-run
python experiments/seed_converge/figure_critic.py --pdf <pdf> --pages 2,6 --confirm
```

§1.1 preview 實跑（pages 2,6、~$0.005/run）：**穩定抓到 `h(x)` 標籤撞 y 軸（每跑
必中）** 與灰階只靠顏色編碼等真缺陷，但次要缺陷（子圖未對齊、紅標壓點、缺刻度）
**run-to-run 飄移**——跟文字審同病，需**多跑取聯集＋人 triage**；單跑為 advisory、
非窮舉。用 `json_schema` 強制結構化（裸 `json_object` 會讓模型脫稿成 bbox／空 list；
numeric scores 不可靠、已移除）。

### figure_fix.py：視覺自動修圖（閉環實驗）

`figure_critic` 只挑錯不動手；[`figure_fix.py`](figure_fix.py) 把它閉環：render →
視覺 critique → 多模態模型重寫 TikZ（看著圖＋舊 code＋defects、數學不動）→ 再 render
→ 再 critique，直到無缺陷或 `--max-rounds`。是 run.py 收斂迴圈的視覺版。

```powershell
python experiments/seed_converge/figure_fix.py --fig <one-figure.tex> --confirm
```

reflection 圖實跑：**真碰撞（`y=x³` 標籤撞 y 軸）被自動修掉、紅曲線還順手改虛線
（灰階加分）**——證明圖能自動改好。但**不可靠**：三跑三樣——視覺審 run-to-run 飄
（1/3 跑準、其餘漏真缺陷或把彩色曲線幻覺成黑）、thinking model 不給足 `--max-tokens`
會截斷出壞 LaTeX、API 偶發 timeout／503（已加 graceful 處理、不再讓整跑崩掉）。
結論同文字審：**能用，但要多跑取聯集＋人 triage，不能盲目無人迴圈。**

## 範圍外（刻意不做）

不碰正式講義流程、不碰 `chapters/*.tex`、不碰凍結中的 `video/`。不寫 parser／
schema 進正式產線（format 未定）。只跑 §1.1 一節，驗證有價值再談擴大。
