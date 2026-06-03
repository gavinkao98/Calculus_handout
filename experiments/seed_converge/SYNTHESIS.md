# 實驗總結：seed→雙模型自動收斂 ＋ 多模態圖檢查（經驗與教訓）

> 隔離實驗 `experiment/seed-converge` 分支跨數輪的綜合結論。日期：2026-06-03。
> 配套檔：`run.py`（文字收斂）、`figure_critic.py`（視覺挑錯）、`figure_fix.py`
> （視覺修圖閉環）、`RESULT.md`（§1.1 收斂評分）、`README.md`（跑法）。
> 本檔記的是「做完之後學到什麼」，給下一次對話／換機接續用。

---

## 0. 緣起

使用者要重構講義製作流程。構想：讓模型在手稿基礎上**自由大幅擴寫**（手稿只當種子，
不再是不可動的主軸），但這放大幻覺風險，故引入**第二個模型自動二次審核**。核心待驗
問題：

> **兩個模型無人介入地自動收斂，會「抓掉幻覺」，還是替一個雙方都同意的幻覺背書？**

定案配置：Gemini `gemini-3.1-pro-preview` 起草 ↔ DeepSeek `deepseek-v4-pro` 審核；
Claude 不進迴圈、當中立第三方評分。後續加 Gemini 多模態做視覺層。

---

## 1. 蓋棺結論（先講重點）

1. **內容（文字）層**：seed + 自由擴寫，在 §1.1 產出**數學零錯、忠於種子、8/8 覆蓋**的
   草稿。但 §1.1 幻覺面極低（初等、無歷史、無微妙證明），**核心幻覺假說其實還沒被真正
   壓測**。
2. **「自動收斂」一開始根本不收斂**：撞 4 輪上限、在格式 nit 上空轉（被審核誤升成
   level-1）。**修了護欄（blocking/advisory 分流）後 → 1 輪乾淨收斂、成本剩 1/8。**
3. **視覺層**：多模態看得到文字審原理上看不到的 render 缺陷（label 碰撞／灰階），**而且
   能自動把圖改好**（碰撞移除、紅線順手改虛線）——但**單跑不可靠**（視覺審三跑只一跑準）。
4. **貫穿教訓**：模型迴圈能加速，但都 run-to-run 飄、都需要人 triage、格式交 linter、
   計費要閘門。**「模型提案、人定奪」是唯一站得住的契約**，文字與視覺皆然——跟影片產線
   `critic.py` / `review_pack.py` 同源。

---

## 2. 逐輪實證（濃縮）

| 階段 | 做了什麼 | 結果 |
|---|---|---|
| full1 | §1.1 seed→converge（舊護欄） | 8/8 覆蓋、0 幻覺；但 **4 輪未收斂**、$0.17、空轉在格式 nit |
| 護欄修正 | blocking/advisory 分流、停在乾淨 audit、強制四級 | — |
| full2 | §1.1 重跑（新護欄） | **1 輪收斂**、$0.02、blocking=0、格式歸 advisory |
| figure_critic | 多模態挑圖（§1.1 preview） | 抓到 `h(x)` 撞 y 軸（**每跑必中**）＋灰階；次要缺陷飄 |
| figure_fix | 視覺修圖閉環（reflection 圖） | run2：碰撞**自動修掉**＋紅線改虛線；單跑不可靠 |

細節見 `RESULT.md`（full1 評分）與各 commit message。

---

## 3. 教訓 ／ 帶進新流程的契約

### 流程設計
- **模型審查一律 advisory ＋ 人定奪**；模型自我 triage 不可信（首跑 7 條 actionable，
  人過濾後只採 2；2 條過度 triage、1 條幻覺）。
- **blocking 只留「數學／忠實度／視覺真缺陷」**；格式 house-rule（`% expansion:`、
  `\index`、register）交 **deterministic linter**，**不准擋收斂**。否則迴圈在主觀格式上
  無限空轉。
- **收斂＝一次乾淨的 audit**；別停在「未經審核的 revise」（最終稿才不會 un-audited）。
- **run-to-run 會飄** → 重要判斷**多跑取聯集**，不信單跑（推理模型尤甚）。

### 工程細節（踩過的坑）
- **thinking model 要給足 token**：`max_tokens` 太低，可見輸出被隱藏推理吃掉而**截斷**
  （`finish_reason=length`／吐壞 LaTeX）。§1.1 起草 8000→16000 才完整；`figure_fix` 同病。
- **結構化輸出用 `json_schema`，別用裸 `json_object`**（Gemini 會脫稿成 bounding box／空
  list）；**VLM 的 numeric 1–5 scores 不可靠**（出現「全 1 卻說無缺陷」），改成純 defects。
- **JSON 要容錯**：模型在 JSON 字串裡塞 LaTeX，`\sqrt` 是非法 escape 會炸 `json.loads`，
  要用 regex 修補（沿用 `review_pack.py`/`critic.py`）。
- **API 會 timeout／503**：迴圈要 graceful 退出，別讓一次失敗丟掉整跑。
- **計費三閘**（`--dry-run`/`--confirm`/`--smoke`）＋ **key 只走 env**，絕不進旗標／檔案／
  對話記錄。

### 哲學
- 真正留得下的是**做法**（advisory ＋ 多跑聯集 ＋ blocking/四級分流 ＋ 人 triage ＋ 計費
  閘門），**不是 parser**。format 還會變，工具是消耗品（這也是當初決定「先驗做法、後落
  工具」的原因）。
- 文字層（`run.py`/DeepSeek）＋視覺層（`figure_critic`/`figure_fix`/Gemini）＝跟影片產線
  `critic.py`/`review_pack.py` 完全同源的「模型提案、人定奪」。

---

## 4. 還開著的問題

- **幻覺假說未壓測**（最關鍵）：§1.1 太簡單。要驗「兩模型會不會一起幻覺」，須換**高風險
  節**——有歷史／具名結果，或像 Ch4 的 Bolzano–Weierstrass、Cauchy 收斂那種微妙證明。
- **自動修圖可靠性**：視覺審三跑只一跑準，需多跑取聯集才堪用；目前單跑只能當 advisory。
  （使用者已決定圖形**改為人工審閱**，此線暫擱。）

---

## 5. 操作備忘（換機／下次接續）

- 全部在 `experiment/seed-converge` 分支，**隔離**；不碰 `chapters/*.tex` 與凍結的
  `video/`。工具 committed；run 產出（`out/`）gitignored、需重跑重生。
- 配置：Gemini `gemini-3.1-pro-preview`（起草／視覺）＋ DeepSeek `deepseek-v4-pro`
  （文字審）。會員訂閱不通用，**自動化一律走 API key（env）**。
- ⚠️ **兩把 API key 在本 session 曾貼進對話 → 請 rotate／撤銷重發。**
- 這條線是否併入正式講義流程：**待定**，看高風險節壓測結果再決定。
