# Ch1 去 AI 味校準報告（REPORT-deai-ch1-calibration）

> **本檔是什麼：** 去 AI 味方案（[`../../PLAN-deai-flavor.md`](../../PLAN-deai-flavor.md)）Phase 1 / Task 1.2 的校準掃描交付物。對全書唯一已簽核、已過 prose audit 的 **Ch1** 做唯讀掃描，量測兩層（Vale 決定性 lint + 人審 Dimension C）的命中與**誤砍率**，據此提出「高密度叢集」**門檻建議值**供使用者拍板（PLAN §6-2/§6-3）。
>
> **唯讀：** 本輪不改任何 fragment、不改 `reject.txt`/`accept.txt`。所有改動建議列在 §6，等使用者 ⛳ 拍板後才動。
>
> **方法：** ① Vale `--output=JSON` 掃 7 節 fragment，逐節算 distinct 命中與每 500 字密度；② 對 7 節各派一個 `handout-prose-audit` subagent（含新增的 Dimension C，階段一 advisory），收 C1–C6 findings、distinct-tell 數、密度、疑似誤砍、A/B blocking 數。

---

## 1. 結果總表

| 節 | 字數 | Vale distinct flags | 人審 distinct 真 tell | 人審密度/500 | **散文 em-dash/500** | A/B blocking |
|----|------|--------------------|----------------------|-------------|---------------------|--------------|
| §1.1 Inverse Functions | 1706 | **0** | 1（C6 em-dash） | 0.29 | ~1.7 | 0 |
| §1.2 Inverse Trig | 1865 | **0** | 1（C6 em-dash） | 0.27 | ~1.9 | 0 |
| §1.3 Limit of a Function | 905 | **0** | 2（C6＋邊緣 C3） | 1.1 | **~4.0** | 0 |
| §1.4 One-Sided/Infinite | 1376 | **0** | 1（C6 em-dash） | 0.36 | ~2.2 | 0 |
| §1.5 Limit Laws | 1772 | **0** | 3（皆邊緣，0 真 tell） | 0.85 | ~0.85 | 0 |
| §1.6 Precise Definition | 1454 | **0** | 1（C6 em-dash） | 0.34 | **~3.8** | 0 |
| sec-intro（章首） | 246 | **0** | 4（皆 content-bearing 邊緣） | **8.1** ⚠ | 低（單對） | 0 |
| **全章** | **9324** | **0** | — | — | 峰值 ~4.0 | **0** |

⚠ sec-intro 的 8.1/500 是**小樣本假象**：4 個 content-bearing 邊緣項 ÷ 246 字 × 500。見 §4。

---

## 2. 第一層（Vale 決定性 lint）：0 誤砍

- **9324 字、7 節，Vale 命中數 = 0。誤砍率 = 0%。**
- 保守起步的 14 條 `reject.txt` 種子（§4.2「寧缺勿濫」）在已簽核好散文上**完全不開火**——這正是設計目標：高 signal、低誤砍，決定性層不誤觸合法數學散文。
- **結論：`reject.txt`/`accept.txt` 本輪無需調整**。`accept.txt` 的 9 個數學詞白名單未被任何節觸及（Ch1 不含 banned 片語），但保留它們仍是正確的防禦（fixture 已證 `robust` 受保護）。

---

## 3. 第二層（人審 Dimension C）：真 tell 趨近於零，唯一訊號是 em-dash

逐節 subagent 的判讀高度一致：

- **非 em-dash 的 C-tell（C1 空心 signposting／C2 copula-avoidance／C3 裝飾性 negative parallelism／C4 強迫 rule-of-three／C5 puffery）：全章 0 個「清關」真 tell。** 每一個候選都被明確判為「邊緣、由內容掙得、§3 受保護、未過 tell bar」。例：
  - C2：§1.2「全節零命中」，definition 一律用直白 `is defined by`／`is one-to-one`；§1.5「plays a central role」是唯一邊緣，且同段下句即自然用 `is the standard tool`。
  - C3：所有 `not X but Y` 都是**承載真實數學對比**（如「±√y — two values, **not** a function」、「depend **not** on the value… **but** on its behavior」），非裝飾節奏。
  - C4：所有三元組都是**真有三項**（三階段教學進路、三個 motivating instance、推理鏈三步），非為 cadence 湊數。
  - C5：無一處 `powerful/elegant/profound/rich tapestry/fundamental building block` 空心斷言；無 `In summary, we have seen…` 式空心收束。
- **唯一可量化的密度型語聲訊號 = em-dash 作插入語（C6）。** 這是 Ch1 散文的招牌節奏，也正是 Vale 難數、要靠人審的那種 tell。每處個別都合法（§8 容許謹慎使用），但全章節奏一致依賴「主句 — 補述」同型句尾。

---

## 4. 誤砍盤點：保護條款全部生效

7 節合計回報數十條 `suspected_false_positives`，**全數**落在 rubric 既有的「不算 finding（§3-protected）」保護傘內，無一是 rubric 漏保護的真誤砍：

- **§3 鼓勵連接詞**（`Notice that`／`Recall that`〔有可回查對象〕／`Let us now`／`In particular`／`More generally`／`In words`）——皆導向實質內容，distinct 種類分散、無單一套語超量。
- **Informally gloss**、**章末回查重述**（lookup-friendliness）、**topic-term recurrence**（`one-to-one`／`limit`／`epsilon-delta` 等主題詞自然反覆）——rubric 明文保護，subagent 正確未砍。
- **合法數學詞**（`fundamental trigonometric limit`、`indeterminate form`、`principal range`、`rigorous footing`）——領域標準用語，非 puffery。

**校準啟示（重要）：** sec-intro 在 246 字內有 4 個 content-bearing 邊緣項，外插成 8.1/500。若門檻只看「外插密度」而不分「真 tell vs content-bearing 邊緣」，**短節會被假觸發**。這直接決定 §6 的兩個 refinement。

---

## 5. em-dash 密度分布（C6 天花板的主要依據）

已簽核 Ch1 的散文 em-dash-as-parenthetical 密度（每 500 字）：

```
§1.5  ▌ 0.85
§1.1  ▌▌ 1.7
§1.2  ▌▌ 1.9
§1.4  ▌▌▌ 2.2
§1.6  ▌▌▌▌ 3.8   ← 次高（line 89 單句 3 個 em-dash）
§1.3  ▌▌▌▌ 4.0   ← 最高
```

**上界 ≈ 4.0/500。** 任何 C6 密度天花板若設在 4.0/500 或以下，會把已簽核基準判成違規——故天花板**必須設在 4.0/500 之上**。唯一的局部熱點是 **§1.6 line 89**（單句 3 個 em-dash），是全章最該考慮收緊的一處（仍 Optional）。

---

## 6. 門檻建議（待 ⛳ 拍板 — PLAN §6-2/§6-3）

> 以下為**提案＋推薦值**，依 CLAUDE.md「一律提案、不自己定死」。Ch1 資料支撐見上。

### 6.1 「高密度叢集」blocking 門檻 N（PLAN §6-2）

- **推薦：維持 `N = 3`（≥3 distinct 真 tell / ~500 字 = BLOCKING）**，但加**兩個 refinement**（校準資料要求）：
  - **(a) 只數「真 tell」**：content-bearing／§3-protected 的邊緣候選**不計入**密度。Ch1 全節據此真 tell ≤2/500，N=3 讓整章安全落在線下（符合「Ch1 該過」的校準目標）。
  - **(b) 短節絕對下限**：density-per-500 外插在約 <400 字時不可靠（sec-intro 假象）。建議 blocking 需**同時**滿足「該節 ≥3 個 distinct 真 tell（絕對數）」**且**「≥3/500（密度）」，使短開場節不會以 1–2 項觸線。
- 備選：若想更寬鬆可設 `N = 4`；但資料顯示 N=3 + refinement 已不誤判 Ch1，無需放寬。

### 6.2 C6 em-dash 密度線

- **推薦：advisory 線 = 每 500 字 ≥4 個散文 em-dash**（在 Ch1 上界之上，故基準不被判違規）；**單句 ≥3 個 em-dash** 為 local advisory trigger（命中 §1.6 line 89 那種）。
- em-dash 僅在「**與其他 C-tell 合計**達高密度叢集」時才貢獻 blocking；單純 em-dash 偏多維持 advisory（它是合法插入語、Ch1 招牌節奏）。

### 6.3 C1–C6 措辭（PLAN §6-3）

- **驗證通過：** 7 節掃描中每個 C 維度都「該開火就開火、該保護就保護」，措辭無誤導。**建議維持現措辭**，僅一處**可選**微調：
  - C6 補一句具體 local trigger：「**單句內 ≥3 個 em-dash 作插入語**即為 advisory 熱點（即使全節密度未超線）」——把 §1.6 line 89 這種點明確化。

### 6.4 Ch1 hotspots：是否選擇性小修

- **推薦：Ch1 維持不動**（它是已簽核校準基準；em-dash 是合法招牌節奏，非缺陷）。
- 若使用者仍想降低 em-dash 指紋，**唯一推薦候選 = §1.6 line 89**（單句 3 個 em-dash，可把其中 1–2 個改成逗號/括號/冒號）；次選 §1.3 收尾 velocity 段。其餘一律不建議動。

---

## 7. 驗收結論

- **誤砍率可接受：** Vale 0%（決定性層）；人審層的 suspected-FP 全在既有保護傘內、無漏保護。**門檻有 Ch1 實測資料支撐，非憑感覺。**
- **回 Task 0.2/0.3 調整：不需要**（reject/accept/TokenIgnores 在 Ch1 上零誤砍）。
- **下一步：** 等 ⛳ 拍板 §6.1–6.4 後，進 Phase 2 Task 2.1（升 blocking + §3 保護清單加密度天花板），把拍板的 N 與 refinement 寫進 rubric。
