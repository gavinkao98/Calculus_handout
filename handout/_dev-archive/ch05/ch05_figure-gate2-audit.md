# Ch5 圖視覺閘 gate-2 稽核紀錄（Codex 第二讀者，2026-07-10）

依 [`../../PIPELINE.md`](../../PIPELINE.md) 新政策「gate-2 全跑：三閘每章必跑到定版」（2026-07-10 使用者拍板，取代原風險分層），Ch5 圖視覺閘補跑跨模型 gate-2（原 2026-07-07 M2 checklist 記「視覺 gate-2 依頻率矩陣＝出版前抽樣」，該分層已取消）。執行：`codex exec -s read-only`（standing consent；gpt-5.6-terra／xhigh）；契約＝[`../../_audit/FIGURE-AUDIT-RUBRIC.md`](../../_audit/FIGURE-AUDIT-RUBRIC.md)；被審物＝該章 **11 張 render 後 2× PNG**（`shot.mjs … figures` 模式截）＋對照 `const FIGS` 繪圖原始碼（standalone L1882–2183）＋11 條 figcaption，全 inline／`-i` 附件。用量 39,787 tokens。raw 落 gitignored scratchpad，本檔為完整轉錄。

## 母體（11 張，全數複核）

枚舉以 fragment 內全部 `<figure>` 為準（`Grep '<figure'` 對齊，11 個皆 `data-fig`、無漏網 inline-SVG）：
Figure 5.1 tangent-radius-circle（§5.1）· 5.2 ladder-triangle（§5.2）· 5.3 streetlight-similar（§5.2）· 5.4 sqrt-linearization（§5.3）· 5.5 dy-vs-deltay（§5.3）· 5.6 fence-river（§5.5）· 5.7 semicircle-rectangle（§5.5）· 5.8 concavity-tangents（§5.6）· 5.9 rational-asymptotes（§5.8）· 5.10 slant-asymptote（§5.8）· 5.11 newton-step（§5.9）。

## VERDICT: 0 visual blocking（0 findings, 0 advisory）

D1（label collision）／D2（out-of-bounds）／D3（viewing-window）／D4（tick labels）／D5（figure↔caption 一致）／D6（math correctness vs 原始碼）／D7（no-spoiler）／D8（grayscale 存活）——**D1–D8 全 clean**。

對抗式複核硬要求已在 prompt 內生效（D5/D6 指控須回 `const FIGS` 逐字核對座標／`<path d>`／`<text>`；警覺 VLM 對小字級上／下標的系統性誤讀）——本輪無任何 D5/D6 指控成立，亦無假陽性需擋。

## 收斂

**圖視覺 gate-2 通過（blocking=0）。** 第二模型獨立盲審與 gate-1（Claude `handout-figure-audit`，自檢修 7 缺陷後 blocking=0／advisory=0）一致：11 張圖視覺無 blocking。雙閘在圖視覺軸收斂。
