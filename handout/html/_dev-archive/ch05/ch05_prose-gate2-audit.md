# Ch5 散文 S·A·V 閘 gate-2 稽核紀錄（Codex 跨模型，2026-07-10）

依 [`../../PIPELINE.md`](../../PIPELINE.md) 新政策「gate-2 全跑：三閘每章必跑到定版」（2026-07-10 使用者拍板，取代原風險分層），Ch5 散文 S·A·V 閘補跑跨模型 gate-2（原 2026-07-08 M3 checklist 記「依頻率矩陣＝非高風險章不跑」，該分層已取消）。執行：`codex exec -s read-only`（standing consent；gpt-5.6-terra／xhigh 依 `~/.codex/config.toml`）；契約＝[`../../_audit/PROSE-AUDIT-RUBRIC.md`](../../_audit/PROSE-AUDIT-RUBRIC.md)＋固定錨組 `_audit/anchors/svc-exemplars.md`；被審物＝ch05 全九節 fragment（sec-5-1…sec-5-9）散文，**乾淨 UTF-8 inline 進 prompt**（依 rubric §跨模型 first-read 硬紀律，避 Codex 自讀檔亂碼假陽性）。用量 64,287 tokens。raw 落 gitignored scratchpad（依 raw 政策不進版控），本檔為完整轉錄。

## VERDICT: 0 blocking, 1 tighten, 0 optional, 0 voice

**易懂性（A）＋ S/A blocking = 0 → prose gate 通過。**

### 唯一 finding（advisory，待使用者裁決）

- **[Tighten][F4 句長／認知負荷] §5.4 · Theorem 5.1 證明第二句**
  - 問題：一句包進區間前提＋兩種單調情形＋符號反轉，first-pass ESL 讀者要同時扛好幾個條件才讀到主結論。
  - 原文：「On each side, \(f\) is continuous on the closed piece — \([u, c]\) or \([c, v]\) — and differentiable on its interior, so the monotonicity corollary (Corollary 4.3) governs each: applied to \(f\) directly wherever \(f' > 0\), and to \(-f\) wherever \(f' < 0\), since a negative derivative for \(f\) is a positive one for \(-f\), making \(-f\) strictly increase and \(f\) strictly decrease.」
  - 建議（Codex 提案，語意不變、純 copyedit）：「On each side, \(f\) is continuous on the relevant closed interval and differentiable in its interior, so Corollary 4.3 applies. Where \(f' > 0\), \(f\) increases. Where \(f' < 0\), apply the corollary to \(-f\): then \(-f\) increases and \(f\) decreases.」
  - 證據：F4——一次線性讀需暫存多個區間條件與符號反轉論證才到主結論。
  - **裁決：** 使用者拍板**套用**（2026-07-10）。
  - **實際落地（與 Codex 草案的差異）：** 採其「拆成短句」的核心（F4 改善），但**保留 Codex 草案順手掉的兩處**——①`strictly`（原文 "strictly increase/decrease"；證明下方 bullet 要 \(f(u)<f(c)\) 嚴格不等式，strictness 承重不可丟）②區間名 `\([u,c]\)／\([c,v]\)`。落地文字：「…so Corollary 4.3 applies. Where \(f' > 0\), it governs \(f\) directly, so \(f\) strictly increases. Where \(f' < 0\), apply it to \(-f\): a negative derivative for \(f\) is a positive one for \(-f\), so \(-f\) strictly increases and \(f\) strictly decreases.」改 `fragments/ch05/sec-5-4.html`。
  - **scoped 回歸（CLAUDE.md 修完必回歸）：** `python build.py ch05` → render 自驗 **katex-errors=0**（math 1035→1036）＋ linebreak-gate 0 條；重讀該段：\(u,c,v\) 前句已定義、四 bullet 邏輯照舊接得上、`strictly`／`-f` 論證／區間名全保留，**未引入新 U/F/S/A/V 問題**。回歸通過。

### 乾淨維度
U1（動機缺位）／U2（重型形式無 gloss）／U3（未解釋跳躍）／U4（先用後定義）／U5（定義後未拆解）／F1（局部冗餘）／F2（贅字）／F3（句構可解析）／F5（語域）／S1–S3（Substance）／A1–A2（Altitude）／V1（Voice）——全 clean。

## 收斂

**散文 S·A·V gate-2 通過（blocking=0）。** 第二模型獨立盲審與 M3 gate-1（三組 0 blocking）一致：易懂性與 S/A 均無 blocking。唯一 advisory 為證明散文的句長收緊，屬選用潤稿。與 gate-1 相比無新 blocking，雙閘（Claude gate-1＋Codex gate-2）在散文軸收斂。
