# §1.1 旁白雙版本 — Mode B 稽核＋收斂紀錄

> **稽核者：** codex `gpt-5.5`（reasoning xhigh，sandbox read-only）。原始逐字 transcript：[`REPORT-ch01-narration-modeB.raw.txt`](REPORT-ch01-narration-modeB.raw.txt)。稽核 prompt：[`PROMPT-ch01-narration-modeB.md`](PROMPT-ch01-narration-modeB.md)。
> **受審物：** 源稿 `ch01_inverse_functions.md`（已認可 narration）＋ 版本 A `ch01_inverse_functions_narration.html`（HTML 閱讀版）＋ 版本 B `ch01_inverse_functions_narration_spoken.md`（MiMo 口語版）。
> **日期：** 2026-06-14。

## 1. codex 裁決

**VERDICT: 1 blocking, 0 advisory**

| # | 維度 | 單元 | 問題 | 裁決 |
|---|------|------|------|------|
| F1 | D2／D4 | u10／u12／u17 | 口語稿正文內嵌字面 `⟨breath⟩` 標記＝非源文字／符號，會被 TTS 唸出（且與 §1「口語稿維持純文字」自相矛盾）。引用：`one-to-one. ⟨breath⟩ Now the converse.`、`for every y in B. ⟨breath⟩ In words:`、`t minus thirty-two. ⟨breath⟩ And the check is reassuring` | **Cut** |

**乾淨維度：**
- **D1（版本 A 忠實）：** 19 單元齊、順序對、kind 徽章對、narration 文字與源稿一致、LaTeX 可渲染。
- **D2／D3（版本 B 忠實＋數學口語化）：** 除 F1 外，散文逐字忠實；數學口語化正確；`f^{-1}` 全程念 "f inverse"、無 reciprocal 誤讀。
- **D6（MiMo 設定）：** 無內部矛盾——OpenAI 相容 `chat/completions`、style 放 `user`／文字放 `assistant`、`audio.format`/`audio.voice`、24kHz mono PCM16、Dean/Milo/Mia/Chloe 音色，皆合理一致。

## 2. D5 念法抉擇裁定（codex 建議 → 採納）

| 項 | codex 裁定 | 採納後動作 |
|----|-----------|-----------|
| a. 下標 | 用 **"x sub one / x sub two"**（正式定義／證明語境最無歧義） | 取代初稿 "x-one/x-two"，套用 u3／u10／u14 |
| b. 座標點 | 用 **"the point with coordinates a and b"**（無視覺符號時最清楚） | 取代初稿 "the point a, b"，套用 u13 |
| c. "the quantity …" | **只用在真群組**（和／差的根號、群組因式、括號次方）；現況大致正確 | 維持現況，不動 |
| d. audio tag | **維持預設關閉**；把 `⟨breath⟩` 移出正文、停頓點改記為 metadata，待真 MiMo 實測證明 tag 安全再用 | 同 F1；停頓點清單移入 §1 metadata |

## 3. 收斂動作（套用於版本 B）

1. **F1（blocking）：** 移除 u10／u12／u17 正文的 `⟨breath⟩`；同步移除 u18 風格註記中的 `⟨breath⟩` 字樣。
2. **D5-a：** `x-one/x-two` → `x sub one / x sub two`（u3／u10／u14）。
3. **D5-b：** `the point a, b` / `the point b, a` → `the point with coordinates a and b` / `… b and a`（u13）。
4. **§1 audio-tag 政策：** 改寫為「口語稿一律純文字、不內嵌任何 tag 或停頓標記」；候選換氣點（u10／u12／u17／u18）改列為 metadata。
5. **§2 念法慣例表：** a／b 兩列由「候選、待 codex 裁決」更新為「Mode B 裁定」定案。
6. **版本 A（HTML）：** D1 乾淨，**未改**。

## 4. 回歸審核（修改後複驗，2026-06-14）

| 檢查 | 預期 | 結果 |
|------|------|------|
| 正文殘留 `⟨breath⟩` | 0 | ✅ 0（僅本紀錄與狀態行的反引號引用，非正文） |
| 殘留 `x-one/x-two` | 0 | ✅ 0 |
| `x sub one/two` 出現於 u3／u10／u14 | 是 | ✅ 三單元齊（＋表格／狀態行） |
| `the point with coordinates` | u13 ×2 | ✅ 2 |
| 殘留 reciprocal 念法（"to the minus one"） | 0 | ✅ 0；`f inverse` ×29 |
| 移除標記後句子接合（雙空格／斷句） | 乾淨 | ✅ 三處接合單空格、無斷句 |

**結論：收斂未引入新問題。版本 B 收斂完成、待使用者拍板。**
