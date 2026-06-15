# 選題稽核——通用維度與 Findings 契約（模板）

> **本檔是所有章別稽核 prompt 的 single source of truth。**
> 新增章別 prompt 時，把下方維度 A–F 與 Findings 契約整段複製進去，
> 只替換 `[章別特定: …]` 標記處。更新維度定義時改本檔，再同步到已有的章別 prompt。
>
> 對應 [`CONTENT_SOURCING.md`](../../CONTENT_SOURCING.md) 流程 2.4「裁決前選題稽核」；
> 契約沿用 [`../direction_layer/RULE.md`](../direction_layer/RULE.md) ⑤。

---

## 角色與語言（每份 prompt 開頭照貼）

```
你是唯讀的審查者（auditor），不是寫手：**不要改任何檔案**，只輸出 findings。
全程用繁體中文回報（數學式、檔名、識別碼保留原樣）。
```

---

## 稽核維度（A–F，依優先序）

```
A. **缺口判定**：對照課文片段裡既有的 worked examples，被審物聲稱的每個缺口
   是否成立（該教學點確實沒有示範）？有沒有它漏掉、且比已列缺口更要緊的缺口？

B. **對症與程度**：每筆 E／O 候選是否真的示範了它聲稱的缺口？難度是否貼齊高中自學
   受眾？插入點（meta 行）在教學順序上是否正確？

C. **數學正確性（重點）**：
   [章別特定: 列出本章「解為本次撰寫」的筆、「改算」的筆、以及需要對照哪個
    definition/convention 獨立驗證的細節。其餘有官方解的筆一律抽驗。]
   - 解為本次撰寫的筆——逐步驗算。
   - 改算筆（因本講義約定而重算者）——對照課文 definition 獨立驗證。
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

F. **不要做**：本選題稽核**不評散文**——語域用詞品味最多 advisory。散文的
   **易懂性／可讀性另有獨立一道審**（gate 1 Claude subagent ＋ gate 2 Codex；
   契約見 ../../_audit/PROSE-AUDIT-RUBRIC.md，其易懂性 U 維度可 blocking），
   與本選題稽核平行、互不重疊。其餘不做：不建議「多加題目」（數量克制是刻意
   設計）；不審尚未發生的插入／編號（那是 import 後另一輪的事）；不改寫任何內容。
```

---

## Findings 契約（與 RULE.md ⑤ 一致）

```
- **blocking**＝｛數學錯誤（含圖的數學錯誤與 viewing window 導致教學特徵不可讀）｜對症性不成立（缺口誤判或候選不對題）｜來源/授權標示不實｝
- **advisory**＝格式、語域、可讀性建議
- 每條 finding：級別（blocking/advisory）＋一句結論＋證據（檔案＋行號或題號）＋建議修法。
- 分清四級：① 真錯誤（要修）② 文件補充即可 ③ 低優先風格 ④ 非 finding。
  不要 over-report：語義等價的措詞差異不是 inconsistency。
- 結尾給一行總結：blocking 共幾條；若為 0，明說「選題稽核通過，可交使用者裁決」。
```

---

## 章別 prompt 的組裝方式

1. 從本檔複製「角色與語言」、維度 A–F、Findings 契約。
2. 加上章別特定的：
   - **背景段**（本章有幾個候選、來自哪些題庫、插入哪些 HTML 片段）。
   - **依序讀**（課文檔案清單、被審物路徑、figures.js 路徑）。
   - **dimension C 的章別細節**（哪些筆是自撰解、哪些是改算、對照哪個 definition）。
   - **dimension F 的補充**（本章的候選總量，如「15+6」）。
3. 存為 `PROMPT-chNN-example-selection-audit.md`。
4. 餵 Codex 時整段餵——prompt 必須自含（Codex 看不到 include）。

---

## 變更紀錄

| 日期 | 變更 |
|------|------|
| 2026-06-12 | 初版：從 Ch1 prompt 抽取通用維度；新增 dimension E（圖的數學正確性），含 viewing window 與關鍵刻度檢查。 |
| 2026-06-15 | dimension F 澄清：散文易懂性／可讀性改由獨立的 prose audit（`_audit/PROSE-AUDIT-RUBRIC.md`）負責，本選題稽核僅避免語域品味；兩審平行、互不重疊。 |
