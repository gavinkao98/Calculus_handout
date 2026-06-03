# §1.2 方向 brief（stage ②→③，待核可）

> 來源 seed：[`seed_s12.md`](seed_s12.md)（手稿 p.5–9）。stage ② Claude 提案、**stage ③ 待人核可**。
> 輸入：seed＋薄度剖析＋ROADMAP Ch1 條目（引用不複述）。核可後＝④擴寫依據、⑤審查 direction-conformance 對照。
> 註：csc⁻¹/sec⁻¹ 慣例叉路 ①-verify 時已裁＝**照手稿非標準慣例**（下方叉路 A 記錄）。
> **③ 裁決（2026-06-04）：A＝加 convention caution；B＝三個反三角自身圖全補（arcsin/arccos/arctan，做成 forward-restricted＋inverse 反射的合併圖）；C＝補 principal-interval 陷阱例。小決定（sin⁻¹≠1/sin caution／arccos·arctan 各補一求值例／history·application skip）全照案。**

## 薄度剖析（{夠／薄／無}）
- 動機（trig 非一對一→域限）：**薄**（有 sin 波形圖，散文少）。
- arcsin 定義＋域/值域＋兩例：**夠**（手稿最 dense 處）。
- 互消 `sin⁻¹(sin x)=x`／`sin(sin⁻¹x)=x`：**夠**（但 principal-interval 限制值得升 caution）。
- arccos／arctan：**薄**（「定義方式類似／the same」一筆帶過，無例）。
- `cos(tan⁻¹x)` 化簡：**夠**（兩法：恆等式＋三角形）。
- 其餘 csc⁻¹/sec⁻¹/cot⁻¹：**薄**（列表、非標準值域、sec⁻¹ 給選擇理由）。
- **無**：`sin⁻¹x≠1/sin x` 記號 caution（ROADMAP pitfall，手稿沒寫）；反三角**自身**的圖（手稿只畫限制後正向函數）；principal interval 在圖上 shade。

## 範圍與深度
- 只吃手稿那叢：六個反三角的定義／principal interval／域值域＋三個化簡例。
- 微分公式（sec⁻¹ 選擇理由）**一行 forward-ref Ch3**，不展開（手稿本就只給理由）。
- arccos／arctan 雖手稿一筆帶過，**比照 arcsin 補對稱的定義段＋各補至多一個 evaluation 小例**（低風險、對齊「每技巧≥1 例」），但不堆同型例。

## ★方向叉路（③ 請裁）★

**叉路 A —— csc⁻¹/sec⁻¹ 值域慣例（①-verify 已裁＝照手稿）**
- 裁定：**照手稿非標準「微分友善」慣例** `csc⁻¹:(0,π/2]∪(π,3π/2]`、`sec⁻¹:[0,π/2)∪[π,3π/2)`。
- **配套（我的建議，請確認）**：加一個 `caution` 點明「此值域是 convention，別本課本可能用 `sec⁻¹:[0,π/2)∪(π/2,π]`；本書選此版因 Ch3 微分公式較簡」。忠實＋防學生對照他書困惑，對齊 ROADMAP notation-pitfall 線。手稿本就點了替代值域，caution 是把它顯題化。

**叉路 B —— 要不要補反三角「自身」的圖（arcsin/arccos/arctan）？**
- 現況：手稿只畫**限制後的正向函數**（restricted sin/cos/tan、sec）；不畫反函數圖。ROADMAP key figure＝「restricted-domain trig graphs with principal intervals shaded」＝**正向限制圖**（手稿這側）。
- **我的建議：主圖做 ROADMAP key figure（restricted sin/cos/tan，principal interval 上色）＝忠實＋達標；反三角自身圖「補 arcsin 一張」**當 §1.1 反射圖的回呼（沿 y=x 鏡射 restricted sin 得 arcsin），其餘 arccos/arctan 自身圖**不補**（避免圖過載）。→ 若你要全補或全不補，請裁。

**叉路 C —— 要不要補一個「principal-interval 陷阱」例？**
- 現況：手稿有 `sin⁻¹(sin x)=x`（限 `[-π/2,π/2]`）但**無**展示「超出主區間就不等」的例。
- **我的建議：補一個** `arcsin(sin(5π/6))=π/6 ≠ 5π/6` 之類的小例（`expansion:example`），把 ROADMAP pitfall「`arcsin(sin x)=x` 僅在主區間」落地。低風險、強化最常見誤解。→ 補或不補請裁。

## 承重直覺
- 領頭（一個）：**三角函數週期重複 → 必須先限到一個 principal interval 讓它一對一，才能反；反函數只回傳那個主值。**
- 打臉用手稿自帶碰撞：整條 sin 波形被水平線交無數次（§1.1 水平線檢驗的直接續用）→ 逼出 domain restriction。

## worked example 清單（手稿 3 個）
- 序：**求值 → 合成/診斷 → 化簡**。
  1. `sin⁻¹(1/2)=π/6`（手稿，求值錨）。
  2. `tan(arcsin 1/3)=1/(2√2)`（手稿，三角形技巧）。
  3. `cos(tan⁻¹x)=1/√(1+x²)`（手稿，恆等式＋三角形）。
  4.（叉路 C 若採納）`arcsin(sin(5π/6))=π/6`（principal-interval 陷阱）。
- arccos/arctan 各補至多一個 evaluation 小例（如 `cos⁻¹(1/2)=π/3`、`tan⁻¹(1)=π/4`），不堆同型。

## history／application
- **history：skip**（反三角無強起源故事）。
- **application：skip**（手稿無；放後章/不放）。留白勝過 padding。本節是定義＋技巧節。

## 強調／takeaway
- 樞紐：**principal interval（主區間）＝反三角一切定義的關鍵**；域/值域對調（§1.1 反函數的具體實例）。
- 可攜技能：用 `sin⁻¹x=y ⟺ sin y=x`（搭直角三角形/恆等式）化簡反三角合成式。
- 對齊 ROADMAP core skill：「work with inverse trig, principal-interval restrictions, and the identities that follow」。

## 刻意不寫（餵 ⑤ 反向檢查）
- **反三角的導數公式**（Ch3）——至多一行 forward-ref（手稿只給「微分較簡」當理由）。
- 不重證 §1.1 反函數一般理論（引用：域限→一對一→反函數）。
- 不漂進一般週期函數反演理論、複數 arg、雙曲反函數。
- 不堆同型求值例（每反三角≤1 evaluation 例）。

## 篇幅帶
- 軟帶 **≈ 200–250 .tex 行**（六個反三角＋3–4 例＋2–3 圖＋convention caution）；對照：既有 ch01 §1.2 ≈ 297 行（四小節）。明顯超出則回查是否圖過載或同型例過堆。

## 記號／figures
- 記號（ROADMAP）：`\arcsin \arccos \arctan \arccsc \arcsec \arccot`（house operators）；`sin⁻¹` 等並用；首用 `\index`。
- caution：`sin⁻¹x≠1/sin x`（ROADMAP pitfall）；csc⁻¹/sec⁻¹ convention（叉路 A 配套）；`arcsin(sin x)=x` 僅主區間（ROADMAP pitfall，搭叉路 C 例）。
- figures：restricted sin/cos/tan with principal interval shaded（ROADMAP key figure）；（叉路 B 若採納）arcsin 自身圖（反射回呼）；三角形圖 ×2（tan(arcsin)/cos(arctan)）。
