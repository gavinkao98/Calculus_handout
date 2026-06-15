# Audit prompt — Ch 1 課文範例補充的「選題稽核」（codex exec 用）

> 用法：把 `=== 提示詞 ===` 之間整段餵給 `codex exec`（唯讀 auditor，走 ChatGPT 訂閱配額）。
> 對應 [`CONTENT_SOURCING.md`](../../CONTENT_SOURCING.md) 流程 2.4「裁決前選題稽核」；
> 契約沿用 [`../direction_layer/RULE.md`](../direction_layer/RULE.md) ⑤。
> ⚠ 餵 prompt 的編碼坑（RULE.md 已實證）：PowerShell 直接 pipe 會把中文重編碼成亂碼——
> 用 `cmd /c "codex exec - ... < PROMPT-ch01-example-selection-audit.md"` 餵原始 bytes。
>
> **維度定義的 single source of truth：[`PROMPT-audit-dimensions.md`](PROMPT-audit-dimensions.md)**。
> 下方 prompt 已從該模板組裝；若模板更新，須同步此處。

```
=== 提示詞 ===
# 角色：唯讀 auditor——稽核「Ch 1 課文範例補充」的選題與改寫

你是唯讀的審查者（auditor），不是寫手：**不要改任何檔案**，只輸出 findings。
全程用繁體中文回報（數學式、檔名、識別碼保留原樣）。

## 背景（一段講完）
本專案是一份免費公開的英文微積分講義（高中自學受眾、Stewart 語域）。講義不收習題
（習題另出獨立習題本）；為了補「課文範例太少」，我們從開放授權題庫（CLP-1／APEX／
Mooculus／Stitz-Zeager，全為 CC BY-NC 家族）選了 15 個核心＋6 個選收的候選，改寫成
worked examples（example＋solution），準備插入 Ch 1 的六個 HTML 課文片段。
**插入前**需要你獨立覆核這份選題與改寫。

## 依序讀（建立脈絡）
1. CONTENT_SOURCING.md                                  ← 選題流程與選題標準（你的稽核基準）
2. handout/ch01_example-supplement-review.html  ← 被審物：候選清單＋擬改寫全文
   （HTML 內數學是 MathJax 原始 TeX，直接讀 \( \) 與 \[ \] 即可）
3. handout/example-ch01/sec-1-1.html … sec-1-6.html  ← 課文現況（缺口分析的基準）
   handout/example-ch01/figures.js  ← 圖的程式定義（JS 函式、domain、標記文字）
4. problem_banks/ 下被審物 meta 行引用的原始題檔（逐筆給了路徑與行號）
   ← 若 problem_banks/ 不存在，先照 problem_banks/README.md 的三行 git clone 抓取
5.（語域／記號參考，僅 advisory 用）CONTENT_SPEC.md §3、§9

## 稽核問題（依優先序）
A. **缺口判定**：對照六個片段裡既有的 22 個 worked examples，被審物聲稱的每個缺口
   是否成立（該教學點確實沒有示範）？有沒有它漏掉、且比已列缺口更要緊的缺口？

B. **對症與程度**：每筆 E／O 候選是否真的示範了它聲稱的缺口？難度是否貼齊高中自學
   受眾？插入點（meta 行）在教學順序上是否正確？

C. **數學正確性（重點）**：
   - 解為本次撰寫的筆（被審物已標明）：E1.1-a、E1.1-c、E1.2-a、E1.6-a 擴寫、O1.6-d
     ——逐步驗算。
   - **E1.2-c 是唯一的「改算」筆**：CLP 原解用標準 arccsc 主值得 f(-1)=-π；本講義
     Definition 1.6 用非標準主值 y ∈ (0, π/2] ∪ (π, 3π/2]，被審物重算為 f(-1)=π。
     請對照 sec-1-2.html 的 Definition 1.6 獨立驗證這個重算。
   - 其餘有官方解的筆：抽驗改寫是否偏離原解的數學實質。

D. **來源與授權**：逐筆 [source:] 能否在 problem_banks 對上原題？授權標示
   （CLP=CC BY-NC-SA 4.0、APEX=CC BY-NC 4.0、Mooculus 逐題=CC BY-NC 3.0、
   Stitz-Zeager=CC BY-NC-SA）是否與題檔檔頭一致？

E. **圖的數學正確性與視覺可讀性（figures.js vs 課文）**：
   - 每幅圖的 JS 函式（`fn:`）是否與課文描述的數學函式一致？
   - `domain` 截斷是否合理——有沒有截掉教學上重要的行為（例如應從雙側趨近的
     曲線只畫了一側、漸近線附近過早截斷）？
   - 特殊點（`dot` 的 `hollow`/solid、`hline`/`vline` 的座標）是否數學正確？
     需要對稱的標記（如 ε-strip 的 L±ε）是否真的等距於 L？
   - 標記文字（`tex:` 欄位）是否與對應曲線吻合？
   - figcaption 與周圍散文的描述是否與圖的實際內容一致？
   - **viewing window（`xmin`/`xmax`/`ymin`/`ymax`）是否讓教學重點可讀？**
     range 過大會讓曲線形狀、漸近線、截距等特徵壓縮到不可辨識——等同圖畫錯。
     逐圖檢查：函式在 domain 內的值域佔 y-range 的比例是否合理（<10% 即為紅旗）；
     課文提及的特徵（漸近線、極值、截距）在 viewing window 內是否可視覺區分。
   - `xticks`/`yticks` 是否標出教學上關鍵的刻度（例如水平漸近線的 y 值、
     特殊點的座標）？缺少關鍵刻度時讀者無參照，列為 blocking。

F. **不要做**：不評語域用詞品味（最多 advisory）；不建議「多加題目」（數量克制
   是刻意設計：每節 1–3、總量 15+6）；不審尚未發生的插入／編號（那是 import 後
   另一輪的事）；不改寫任何內容。

## Findings 契約（與 RULE.md ⑤ 一致）
- **blocking**＝｛數學錯誤（含圖的數學錯誤與 viewing window 導致教學特徵不可讀）｜對症性不成立（缺口誤判或候選不對題）｜來源/授權標示不實｝
- **advisory**＝格式、語域、可讀性建議
- 每條 finding：級別（blocking/advisory）＋一句結論＋證據（檔案＋行號或題號）＋建議修法。
- 分清四級：① 真錯誤（要修）② 文件補充即可 ③ 低優先風格 ④ 非 finding。
  不要 over-report：語義等價的措詞差異不是 inconsistency。
- 結尾給一行總結：blocking 共幾條；若為 0，明說「選題稽核通過，可交使用者裁決」。
=== 提示詞結束 ===
```

## 給使用者的備忘（不用餵給 codex）
- 跑這個會吃 ChatGPT 訂閱配額；你自己發動即視為同意。
- **本機調用實務（2026-06-12 實測，公司機）**：
  - PATH 上沒有 codex；能用的是桌面 app 捆的
    `%LOCALAPPDATA%\OpenAI\Codex\bin\codex.exe`（0.130.0-alpha.5）。
    `~\.codex\.sandbox-bin\codex.exe`（0.119）太舊，後端拒絕 gpt-5.5，勿用。
  - `~\.codex\config.toml` 的 `service_tier = "priority"`（app 寫的）兩顆 CLI 都不認，
    會在 config 解析就炸——跑前備份並暫時註解該行，**跑完立刻還原**。
  - 完整調用：`cmd /c "<codex.exe 路徑> exec --sandbox read-only - < 提示詞.txt > 輸出.txt 2>&1"`。
  - 首輪全量稽核實測 ~161k tokens、範圍限定複審 ~60k。
- Codex 跑完把 findings 原文丟回給 Claude：blocking>0 → Claude 修訂候選（改 HTML 審核
  文件）→ 重審到 blocking=0；之後才輪到你填裁決表。
- import 完成後還有一輪**輕量整合稽核**（編號位移、prose 引用、渲染）——那輪的 prompt
  屆時另備，不在本檔範圍。
