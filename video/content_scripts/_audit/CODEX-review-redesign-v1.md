# Codex review — 影片模板重設計提案 v1（The Lectern）

> 來源：`codex exec -s read-only`（codex-cli 0.142.0），2026-06-24。讀兩份提案 HTML
> ＋ `DESIGN.md`／`_common.py`／`theme.py`／`brand.py`／`CLAUDE.md` 後產出。原稿存檔
> （%TEMP% 不隨 repo 走，故落版控）。被審物：
> [`REVIEW-template-redesign-v1.html`](REVIEW-template-redesign-v1.html)、
> [`REVIEW-prose-math-layout.html`](REVIEW-prose-math-layout.html)。
> 彙整與裁決原在 `TODO-template-redesign.md`（已退場，內容搬進 [`REBUILD_STATUS.md`](../../REBUILD_STATUS.md)「2026-06-24」節）；字體 Route A 實作計畫見 [`PLAN-routeA-plex-latex.md`](PLAN-routeA-plex-latex.md)。

---

## 結論

不建議整包核准 v1。可採納的核心是「固定 rail＋prose 保留完整 measure」；navy、spine、footer、Fraunces 應拆成獨立決策。

### 真 findings

1. **Gradient 違反既定 house style。**
   提案大量使用 background/panel gradients，但 SSOT 明定 dark flat、無 gradient。這是規則衝突，不是偏好。
   `REVIEW-template-redesign-v1.html:86` · `VISUAL-FRAME-RUBRIC.md:45`

2. **BEFORE 並非 current tree。**
   現行 `definition_math` 已是 statement→math 單欄、上偏配置，且已有可見 aside。提案仍將這些描述為新修復；另提議純 derivation 改左 flush，但現行刻意置中。
   `REVIEW-template-redesign-v1.html:262` · `definition_math.py:1` · `derivation.py:181`

3. **字體論證已過期且低估實作成本。**
   Live handout 已改為 New Computer Modern，不再是 Times。Fraunces 也不是只需 vendoring：含數學的 heading 目前經 `_compose()` 使用 `FONT_BODY`，會造成純標題 Fraunces、數學標題 Times；Space Mono 同樣不是現有系統字體。
   `handout/TYPESETTING_GUIDE.md:273` · `brand.py:279` · `theme.py:33`

4. **spine/footer 不是單純共用元件。**
   HTML 的可見 spine 在 5%，內容在 8.1%；現行 `SPINE_X` 本身就是內容左緣，直接畫線會壓字。Footer 又占用目前的 body zone、worked strip 與 motif 空間，而且 scene ordinal 尚未傳入 template context。必須改 layout/capacity/data flow。
   `REVIEW-template-redesign-v1.html:94` · `_common.py:38` · `scene.py:41`

### 文件漂移

`DESIGN.md` 目前至少有兩個真衝突：

- `definition_math` 同時寫「兩欄」與「已退兩欄」。 `DESIGN.md:236` · `DESIGN.md:295`
- 說 `body_text` 使用 Tex，但程式實際使用 Pango `Text`。 `DESIGN.md:488` · `brand.py:163`

### 左右 vs 上下

核心原則正確，但不要採用 `>45 字` lint：

- `derivation`：左右，因為式子↔理由逐列配對。
- `procedure_steps`：短指令可左右；長 prose 應拆 scene／改寫，不是靠固定字數。
- `recap_cards`：兩個獨立 gallery，可左右；目前 production points 已有 50–60 字，因此 45 字門檻會誤報。
- `definition_math`、`theorem_proof`：上下。
- figure：繼續置中，非 finding。

### 各提案裁決

- Flat navy `#0a1322`：**可試**，但保持純色並同步重調 panel/hairline。
- Visible spine：**做小範圍 prototype**；新增 `DECOR_SPINE_X`，不要挪用 `SPINE_X`。
- Footer：**v1 暫不採**。
- Fraunces：**延後單獨測試**。
- `HEADING_MATH_SCALE`：**不要依 CSS `.84em` 修改**；KaTeX 與 Manim/newtx 指標不可直接換算。

### 優先三步

1. 先修正兩份 review HTML 與 `DESIGN.md` 的 current-tree／字體／gradient 敘述。
2. 只做三張 1080p Manim A/B：definition、procedure＋worked、graph。
3. 第一輪僅測「flat navy＋克制的 spine」，保持現行字體、無 footer，隔離變因。
