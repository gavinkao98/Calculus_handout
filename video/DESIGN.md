# 影片產線——設計（第二代）

這是重新設計的 handout → lesson-video 產線。輸入為 HTML handout
kit（`../experiments/handout_kit/`；per-chapter authoritative file 列於
[README.md](README.md)——2026-06-10 從 `chapters/*.tex` 切換）。它取代第一代系統
（`tools/manim_*`、`MANIM_STORYBOARD.md`、`MANIM_REFERENCE.md`、
`MANIM_CHECKLIST.md`），第一代被凍結、不刪除。

狀態：**partially implemented**。storyboard → TTS → audio-driven render → mux
的路徑現在已端到端可運作（在 §1.1 上驗證）；標記為 (TODO) 的其餘部分尚未實作。

---

## 為何重新設計

第一代可以運作，但累積了三個摩擦源：

1. **兩套 reveal mechanism 並存。** 一個 timing-based path（`_run_voiceover_beats`，
   手動估計秒數）和一個 bookmark path（`reveal_strategy` + manim-voiceover）
   並行運作，在 render time 切換。作者必須兩套都懂。
2. **繁重的 spoken-math rewrite layer。** 每個 `f(x_1)` 都得手動改寫為
   "f of x one"，放在獨立的 `voiceover` 欄位中，受一張大規則表管制——因為舊
   TTS 無法直讀 LaTeX。
3. **三個重疊的 narration 欄位。** `voiceover` + `voiceover_beats` +
   `bookmark`/`reveal_groups` 同時編碼「說什麼」和「何時顯示」，靠手動保持同步。

兩個決策解消了全部三個問題：

- **Gemini TTS 直讀 LaTeX**，使用模型的 preset voice name
  （`meta.voice` / `--voice`）。不使用 voice cloning 或 reference audio。
  spoken-math rewrite layer 刪除。Narration 只寫一次，LaTeX 直接 inline。
- **一個 narration 欄位搭配 inline reveal marker。** `say` 同時承載文字和
  timing cue。不再有獨立的 beats/bookmark/reveal array。

另加一個新的 product requirement：**每節都有 intro 和 outro animation**，因此
scene `kind` 是 first-class 的，且支援 silent（no-narration）scene。

---

## 沿用 vs 重寫

| 原封沿用（已驗證，重寫無收益） | 從零重寫 |
|---|---|
| `visuals/theme.py`（Midnight Canvas palette + Times typography + layout metrics） | storyboard schema + format |
| `visuals/graph_utils.py`（safe expr eval + sampling） | narration → beats compiler |
| `visuals/layout.py`（16:9 zone layout） | scene templates |
| ffmpeg mux/concat logic *（以 `pipeline/mux.py` 重新實作）* | TTS backend（Gemini） |
| Midnight Canvas visual philosophy + animation language | CLI / orchestration |

沿用的資產是逐 key 從真正的 source dict 複製的
（`DEFAULT_THEME` in `legacy/scripts/manim_render_lesson.py`、`SceneLayout` in
`legacy/scripts/manim_templates/layout.py`、`safe_eval_expression` in
`legacy/scripts/manim_templates/graph_utils.py`），不是從文件重建的。

`MANIM_STORYBOARD.md` 的方法論*精神*沿用（每場景一個教學概念、detail over
compression、conversational narration、visual over textual、symbol-heavy
exception）。其機械規則（spoken-math table、sentence-count carve-out、bookmark
syntax）不沿用——它們是舊約束的產物。

---

## Storyboard 格式

每節一個 YAML 檔。Top-level：`meta` + `scenes`。

```yaml
meta:
  id: ch01_inverse_functions      # deck id，也是 output dir name
  section: "1.1"                  # intro/outro template 顯示
  title: "Inverse Functions"
  language: en
  theme: midnight
  voice: Charon                   # Gemini preset voice name (fixed default)
  video: { w: 3840, h: 2160, fps: 60 }   # 交付標準：4K60（manim fourk_quality）

scenes:
  - id: <unique snake_case>
    kind: intro | content | outro
    ...
```

**解析度慣例。** 測試和預覽 render 使用 **1080p**
（`make.py --quality high`，預設值）——足以做 visual QA 和 VLM frame
critique，不需要 4K 的 render 成本。**只有最終交付使用 4K**
（`--quality 4k`）：專案標準 `3840×2160@60`（manim `fourk_quality`），
在 `meta.video` 中 per section 宣告，省略時使用預設值。`--quality low` /
`medium`（480p/720p）是快速 scratch preview。Layout 是 resolution-independent 的
（manim frame 為固定的 14.222×8 units），因此 1080p 測試和 4K master 是
pixel-for-pixel 相同的 composition——只有 sampling density 和 render time 不同。

### Scene kind

- **`content`**——教學場景。有 `template`、`say` 和 visual data。這是
  workhorse；以下關於 `say`/reveal 的一切都適用於它。
- **`intro`**——section opener。**沒有 `say`**（純 animation）。讀取
  `meta.chapter`、`meta.chapter_title`、`meta.sections`、`meta.section`、
  `meta.title`，以及 optional `tagline`、optional `bgm`、`duration`。可重用的
  template 是 Section Gate：先顯示 chapter map，focus 當前 section，resolve 成
  logo / section / title / tagline slate，然後加一段短暫的 dark handoff，使第一個
  教學場景不會感覺像突然的色彩切換。
- **`outro`**——section closer。**沒有 `say`**。讀取 optional `bgm`、`duration`
  和 optional `end_slate` override。Template 為兩階段：從 teaching ground 到
  light 的 short dark-to-light bridge，然後是最終的 centered logo slate，讓觀眾
  清楚感到影片已結束。**Key Takeaways 不在 outro 中**——它們在前面的
  `recap_cards` content scene 中，該場景帶有 narration（一個 silent 的
  takeaways slate 讀起來比 narrated recap 弱）。end slate 預設為
  `meta.section` + `meta.title`；僅在某節覆蓋標準結尾時才使用 optional
  `end_slate.label`、`end_slate.title` 或 `end_slate.logo_height`。（outro 上的
  任何 `recap`/`next` key 都是 vestigial——template 會忽略它們。）

`intro`/`outro` 作為參數化 template **只定義一次**，每節重用——作者永遠不需要
per section 手建它們。

最小可重用 outro：

```yaml
- id: outro
  kind: outro
  duration: 8.0
  # optional: bgm, and an end_slate override (label / title / logo_height)
  # Key Takeaways 是獨立的 recap_cards scene，不是 outro。
```

最小可重用 intro：

```yaml
meta:
  chapter: "Chapter 1"
  chapter_title: "Inverse Functions and Limits"
  section: "1.1"
  title: "Inverse Functions"
  sections:
    - { id: "1.1", title: "Inverse Functions" }
    - { id: "1.2", title: "Inverse Trigonometric Functions" }

scenes:
  - id: intro
    kind: intro
    tagline: "When can a function be run backwards?"
    duration: 6.0
```

### `content` scene 欄位

| 欄位 | 必填 | 意義 |
|---|---|---|
| `template` | yes | 使用哪個 scene template（見下方 "Template catalog"） |
| `accent` | definition-family 必填 | 色彩角色：`definition` / `theorem` / `proposition` / `example` / `warning` / `procedure` / `recap`。取代舊的 `content_type`。 |
| `title` | yes | 螢幕上的 scene title；可使用 `$...$` 表示數學 |
| `say` | yes | 單一 narration 欄位（見下方） |
| `statement`、`math`、`steps`、`plots`、… | per template | 螢幕上的 visual payload |
| `hook` | no | `"<module>:<fn>"` custom-animation factory，可從 `video/` import（例如 `"animations.ch01_inverse_functions_hooks:can_we_go_backwards"`）。Factory 接收 `(spec, ctx, template_blocks)` 並回傳最終的 block list：替換 block 的 mobject **但保留其 reveal id**（使 `{show ...}` marker 和已核准的 narration 不受影響）、將 static element defer 到一個 beat、或附加一個 callable anim `(scene, mobject, ground) -> seconds spent`（`pipeline/blocks.py`）。Storyboard 中的 template payload 保留為 no-hook fallback——刪掉 `hook:` 行即恢復 stock scene。在 `pipeline/templates/__init__.py:_apply_hook` 中接線。 |

### Template catalog（content scene）

每個 template 一行——教學形狀、payload 和 `{show ...}` 可指向的目標。
Demo storyboard 在 `storyboards/_demo_*.yml`。

| template | 教學形狀 | payload 欄位 | reveal target |
|---|---|---|---|
| `definition_math` | definition / theorem statement / note / motivation：statement + math lines | `statement`、`math[]`、`kicker` | `math.N` |
| `theorem_proof` | statement card + dot-led proof steps + QED | `statement`、`proof[]`、`qed` | `proof.N`、`qed` |
| `example_walkthrough` | 離散的 worked steps，reasoning 在 math 旁邊，✓/✗ mark | `steps[{text,math,mark,hot}]`、`takeaway`、`takeaway_tone` | `math.N`、`takeaway` |
| `procedure_steps` | 編號步驟 + 底部 worked strip | `steps[{text,math}]`、`worked[]` | `math.N`、`worked` |
| `derivation` | 全寬連續推導鏈 | `statement`、`lines[]`、`align_on` | `line.N` |
| `graph_focus` | 一張全幅 plot | `axes`、`plots[]`、`annotations[]` | `annotation.N`；opt-in `plot.N`（`reveal: true`） |
| `graph_compare` | 兩張並排的圖表——比較本身即是課程（HLT、f vs f′、converges vs diverges） | `left`/`right` `{axes, plots, caption, verdict}`、`annotations[]` | `caption.left/right`、`left.plot.N`/`right.plot.N`（`reveal: true`）、`annotation.N` |
| `value_table` | 數值 limit 表 / formula grid / property comparison | `header[]`、`rows[][]`、`reveal: rows\|cols`、`accent_col`/`accent_row`、`statement` | `row.N` 或 `col.N` |
| `sign_chart` | number line + signed interval rows（monotonicity、curve sketching） | `points[]`（`excluded: true` 表示 break）、`rows[{label, marks}]`、`statement` | `mark.R.I`（row R, interval I） |
| `recap_cards` | key point + remember-formula card | `points[]`、`formulas[]` | `point.N`、`formula.N` |

### Template 選擇：離散步驟 vs 推導鏈

計算場景有兩種形狀，選錯 template 就是長公式跑出空間的原因——兩欄 template
的 math column 上限約 ~5 manim units，而真正的 chain line（ch02 的
slope-from-definition computation）需要 7–9：

- **`example_walkthrough` / `procedure_steps`**——離散步驟：每步是一條短公式，
  其 reasoning text 值得*在旁邊閱讀*。容量：3–4 行，math column ~5 units。
- **`derivation`**——連續推導鏈（derivative from the definition、limit-law
  rewrite、identity proof）：一條 aligned 全寬 chain（~11 units），透過
  `{show line.N}` 逐行揭示；per-step 的 "why" 在 narration 中，不在螢幕上。
  Line 0 帶 LHS；後續行以 "= ..." continuation style 將其 relation symbol
  x-align 到 line 0 的下方（`align_on`，預設 `=`）。`anim: highlight` 標記
  result line（accent colour）。Optional 的 centred `statement` 陳述問題——但
  滿容量的 chain 應將該工作交給 narration 的第一個 beat（實測：statement + 四行
  fraction-height lines + result line 超出 zone ~0.5）。
- **分割場景前的容量**（content-layer 決策，與 methodology §3 的 proof split
  精神相同）：沒有 statement 時 ~5 行 fraction-height lines，有 statement 時
  ~4 行；~7 行 single-height lines。`sizecheck` 標記 overflow；修復方法是
  split，不是 squeeze。Demo / reference storyboard：
  `storyboards/_demo_derivation.yml`（真正的 ch02 chain + 6 行探針）。
- **Step template 中的 row pitch 是最小值，不是常數。**
  `example_walkthrough` / `procedure_steps` / `theorem_proof` 以其設計的
  rhythm（1.25 / 1.4 / 0.95）放置 row，但當相鄰 row 較高（wrapped step text、
  fraction math）時會擴大 pitch，保持 ≥0.35 的空氣——因此 row 永遠不會碰撞
  （recap_cards fused-rows class，2026-06-11 在 template layer 修正）。較高的
  first row / statement 也會向下*推離* title 而非長入其中。對 authoring 的影響：
  高內容吃 row——3–4 step 的容量假設 single-line step；有 stacked fraction 時
  預期 ~3 行。Overflow 現在從底部溢出（sizecheck 會抓）；修復仍是 split。
  Stress demo：`storyboards/_demo_tall_rows.yml`。

### `say`：narration + inline reveal（核心變更）

`say` 是**被朗讀的內容**，**LaTeX inline 書寫**（`$f(x_1)$`），以及**reveal
marker** `{show <target>}` 穿插其中。

```yaml
say: |
  The property we need is called one-to-one. A function is one-to-one
  when different inputs always give different outputs.
  {show math.0} No two distinct inputs ever land on the same output.
  {show math.1} Equivalently, if $f(x_1) = f(x_2)$ then $x_1 = x_2$.
```

規則：

- **`{show <target>}`** 標記「現在揭示此元素」。Target 命名場景 visual payload
  中的一個元素：`math.0`、`math.1`、`step.0`、`bullet.0`、`plot.0`、
  `statement`、`takeaway`、…（index 指向對應 list）。
- 一個 **beat** 是從一個 marker（或 scene 開始）到下一個 marker 之間的文字段。
- Static element（title、axes、statement）預設在 scene 開始時出現；只有被
  `{show ...}` 命名的元素才會等待其 beat。（這是舊的 static/dynamic 分類，現在
  以 inline 方式表達，而非 per-template table。）
- **`graph_focus` 的 plot 預設是 static 的**（整張圖從 frame 1 就在螢幕上）。
  將 plot entry 標記 `reveal: true` 使其等待 `{show plot.N}`——教學順序
  （curve first、*然後* ε-band、*然後* δ-band）變成 `say` 中的 beat 決策，
  不需要 hook。Revealed plot 的 `label` 折入同一個 block，因此一個 marker 同時
  帶出元素和它的名稱。Demo：`storyboards/_demo_graph_reveal.yml`。
- `say` 中的 LaTeX 原樣傳給 Gemini TTS。**不做 spoken-math rewrite。** 如果某個
  特定短語以特定方式朗讀更好，直接在 `say` 中如此撰寫即可。

### `math` 和其他 visual payload

```yaml
math:
  - "$f(x_1) \\ne f(x_2)$ whenever $x_1 \\ne x_2$"     # 純字串
  - { tex: "$f(x_1)=f(x_2)\\implies x_1=x_2$", anim: highlight }   # 帶 animation
```

`anim` 選項（沿用）：`write`（預設）、`highlight`、`transform_from_previous`。
*何時*（reveal timing）在 `say` 中透過 `{show math.N}`；*如何*（animation
style）在此。乾淨分離。

### Text rendering：prose vs math（no garble）

螢幕文字走兩條 render path 之一。兩者都是 Times（匹配 LaTeX handout 的
newtxtext/newtxmath），但 manim 在相同 `font_size` 下 size 不同，且只有一條
理解 LaTeX：

| Path | Engine | 理解 `$math$` / `\\`？ | 使用者 |
|---|---|---|---|
| `Text` | Pango（Times New Roman） | **否**——markup 會 literally 印出（garble） | `brand.heading`、`brand.eyebrow` |
| `Tex` / `MathTex` | LaTeX（newtxtext + newtxmath） | 是 | `brand.body_text`、`brand.prose`、`brand.heading_rich`、`brand.math_line` |

`brand.body_text` 透過 `Tex(r'\text{...}')` render（不是 Pango `Text`），讓
body prose 取得 LaTeX-quality kerning——匹配 handout。Heading 仍使用 Pango
`Text`（SEMIBOLD weight，Tex 無法表達）；在 display size 和 bold weight 下
Pango kerning 差異不可感知。

`Text` 在相同 `font_size` 下比 `Tex` 高 ~1.36×，因此透過 Tex render 的 prose
以 `theme.TEX_TEXT_SCALE` 放大，使其與旁邊的 heading 相同大小。Math
（`math_line`）保持其自身的 size role，不放大。

**規則（template 必須遵循）：** 作者可能放入 `$` 或 `\` 的任何欄位——`title`、
`statement`、step `text`、`takeaway`、recap `points`——透過 **`brand.prose`**
（body prose）或 **`brand.heading_rich`**（title）render。這是 markup routing
的唯一決策點：有 markup → Tex text-mode，否則 → `body_text`（也是 Tex，為了
kerning）。永遠不要在 author prose 欄位上直接呼叫 `heading`。純 math 欄位
（`math`、`formulas`、`proof`、`worked`）走 `brand.math_line`。

Plain-Text-only 欄位是 intro/outro brand label（`meta.chapter`、
`meta.chapter_title`、`meta.section`、`meta.title`、`meta.tagline`、
`meta.sections[].title`）——不要在這些中放 markup。`pipeline/lint.py` 靜態地
強制執行以上全部（見 Data flow），在每次 render 前執行。

**Sizing 規則——wrap, don't shrink（針對 stacked prose）。** 當一行 prose
太寬時，`brand.prose` 在 full size 下*換行*到更多行；它永遠不
`scale_to_fit_width` 單行縮小。這對 **stacked siblings** 很重要（recap point、
proof step、graph annotation、example step）：如果一行長的被縮小而旁邊的短行
沒有，它們會以明顯不同的大小 render（這是一個真實的 bug）。因此任何一組並排的
prose line 必須走 `brand.prose` 帶 `max_width`——不是 `math_line` +
`scale_to_fit_width`。`$...$` span 對 wrapper 是 atomic 的，所以換行永遠不會
拆斷 math。唯一允許 `scale_to_fit_width` 的地方是**沒有 sibling 需要匹配的
standalone display line**——`heading`/`heading_rich` title——即使在那裡，換行
讀起來好時也優先。Math grid（`math`、`formulas`、`worked`）是自己的 size role，
免除此規則。

自動強制：`pipeline/sizecheck.py` build 每個 scene（不 render），在每個
stacked-sibling group（`point`、`proof`、`step`、`annotation`、`row`）中找到
`brand.prose`-tagged lines，並標記一組 lines 在 scale-aware font size 上不同的
group。`make.py` 在 render 所選 scene 之前執行它（`--skip-sizecheck` 可略過），
與 garble `lint.py` 並行。

**色彩／可讀性。** 承載教學內容的文字使用 `text`/`primary` 或 semantic
accent——永遠不用 `muted`。這涵蓋 prose（statement、step text、graph
annotation、recap point）**以及直接的 `MathTex`/`Text` value label**——例如
mapping diagram 上的數字（`½`、`−½`、`¼`）或 point coordinate 是 content，
因此用 `text`，不用 `muted`（兩者都是真實的 miss，在影片觀看距離下太淡）。
`muted`（`#7e8497`）**僅用於裝飾和 de-emphasis**：summit-bars motif、non-current
section-map entry、retired content、以及純 reference label（`y=x` guide line、
set `A`/`B` tag）。

> Guard blind spot：`sizecheck` 只在 `brand.prose` text 上標記 `muted`。**直接
> 構造的 `MathTex`/`Text` label 使用 `muted` 不會被抓到**——因為某些這樣的
> label（上述的 reference/decoration 類）確實合理地使用 muted，blanket rule 會
> false-positive。對直接 label 這是 convention + review，不是 automated guard。

**Prose 中不使用手動換行。** 將 step/point/annotation/statement 撰寫為
plain sentence——**不要**插入 LaTeX `\\` 強制換行。`brand.prose` 在 column
`max_width` 處自動換行：短行留在一行，長行在 word boundary 換行。手動 `\\`
強制一個 arbitrary break（例如 "Solve $y=x^3$\\ for $x$." 把一個單行短語
斷成兩行）——那是 authoring artifact，不是 layout。將 `\\` 保留給*刻意的*
stylistic break，在此處極少見。

---

### Authoring checklist——反覆出現的錯誤，不要重蹈覆轍

以下每一項都曾作為真實 bug 出貨，本專案已為此付出代價。撰寫 storyboard 或
template 時請遵守。嚴重度：**error** 中止 render（確定壞了）；**warn** 印出但
不阻擋（有罕見的合理例外）。兩者都在 `make.py` render 前執行。

| Don't | Do | 原因／guard |
|---|---|---|
| 在 plain-Text 欄位（`title`、`meta.*` label）中使用 `$math$` 或 `\` | 只在 markup-capable 欄位放 math | 會 literally 印出；**lint error** |
| 奇數個 `$` | 平衡每個 `$…$` | LaTeX crash；**lint error** |
| 在可能包含 `$`/`\` 的欄位上用 `heading` | `brand.prose` / `brand.heading_rich` | garble；routing 集中在那裡 |
| 在 stacked prose 上用 `math_line` + `scale_to_fit_width` | `brand.prose(..., max_width=…)`（wrap） | size mismatch；**sizecheck error** |
| prose 中的手動 `\\` break | plain sentence，讓 prose wrap | arbitrary break；**lint warn** |
| 教學內容使用 `muted`（prose **或**直接 `MathTex`/`Text` value label） | `text`/`primary` 或 semantic accent | 太淡；prose 上 **sizecheck warn**——直接 label 靠 convention |
| 用空心 `○` dot 表示 attained value（curve 上的點／交點） | 實心 `●`（`hollow: false`）；刻意 excluded 的值加 `hollow_reason: <why>` | `○` 意味著*值不存在*；**lint warn**（interior curve point 上的 hollow），有 `hollow_reason` 時抑制 |
| 元素寬於/高於 frame（formula/recap card、長 statement、unclamped headline） | 縮短、clamp width、或 split | 被 silently clip 出 frame；**sizecheck error**（off-frame）/ **warn**（spill past safe margin） |
| 在非判定的推導／setup 步驟標 `mark: ok`/`bad`（✓/✗） | ✓/✗ 只標真正的判定或檢查（one-to-one 測試、compose 驗證；求逆的推導步驟不標，驗證交給 takeaway） | ✓ 全片應只表「通過／驗證」；裝飾性勾號會誤導觀眾（2026-06-13 §1.1 review 學費） |

---

### Visual QA——全影片驗收通過

上方的 authoring checklist 靜態地抓*已知的 per-element 錯誤*。以下是其補充：
一個**五維度的成品影片通過**（或其 key frame），在一節出貨前端到端觀看。維度
改編自 Code2Video 的 AES rubric；在該研究中 aesthetic score 與測量的 learning
gain 相關 **r ≈ 0.97**，因此 visual clarity 就是 teaching efficacy，不是 polish。
同一張表也兼作未來 VLM critic 的 rubric（見
[`CODE2VIDEO_STUDY.md`](CODE2VIDEO_STUDY.md) P1/P3）。

| 維度 | 本產線的具體檢查 |
|---|---|
| **Element Layout** | 沒有兩個 content block 重疊（現由 `sizecheck._overlap_issues` 自動抓到）；一切都在 `SAFE_MARGIN` 內；graph label 不可壓在線、點、空心點或其他圖形標記上（例如 `$y=f(x)$` 貼在線段上即為 finding）；frame 讀起來平衡、不歪斜。 |
| **Attractiveness** | 每個 animation 都值得存在——它*animate*一個概念（sweep、trace、reflection across `y=x`），不只是 static slide reveal（methodology §5, "Animate, not just display"）。 |
| **Logic Flow** | Reveal 順序追蹤 narration beat；每場景一個教學概念；narration 說到之前，螢幕上什麼都不該出現。 |
| **Visual Consistency** | Accent role 一致（definition = cyan、theorem = gold、example = electric blue、…）；全片一套 font 和 size scale；intro 和 outro 匹配 brand bookend。 |
| **Accuracy & Depth** | 忠實於 handout，數學正確，且每場景的 `learning_goal`（content script，methodology §6）確實被 deliver——在螢幕上*且*在 narration 中。 |

此通過由 **VLM critic**（`pipeline/critic.py`，Code2Video P1 adoption）執行：
它提取每場景的 fullest frame，讓 vision model（MiMo-V2.5）對照這五個維度打分並
列出具體缺陷。它是 **advisory**——它寫 report
（`output/<chNN>/<sX.Y>/critic/critique.{json,md}`），永遠不編輯 storyboard；human
仍是 layout 的 authority。指令和 cost gate 在 [`README.md`](README.md)
（§ VLM 視覺批改）。

**Review loop。** 一個 finding 是一個要衡量的意見，不是命令。以迭代方式而非
one-shot 運行：

1. **Critique**——在 scene/section 上跑 critic；讀取其 score、defect 和
   suggestion。
2. **Judge & adopt**——決定哪些要採納。採納任何*依你的判斷能讓影片更好*的——
   **不僅限於明顯的 bug**。一個改善 clarity、pacing 或 teaching 的 suggestion
   即使沒有什麼「錯」也值得採納。只在 suggestion 會*傷害*（例如破壞跨場景
   consistency）或與刻意的 house decision 衝突（flat, no-grid aesthetic；一個被
   declined 的 typesetting choice）時才拒絕。當一個 suggestion 真正**有爭議**——
   兩面都說得通，或是作者該做的 design call——提交給 human 決定而非自行定奪。
   VLM 提議；你決定，對 close call 上報。
3. **Modify**——套用已採納的變更（storyboard / template），重新 render 受影響的
   scene。
4. **Re-verify**——在變更後的 frame 上再次跑 critic：確認 defect 已消失且沒有
   新的出現。提出它的 judge 確認修復——你自己的肉眼不夠（此規則是在一個修復被
   目測但未複驗後設立的）。
5. **Final check**——你自己讀一遍結果。
6. **Iterate**——重複直到 critic 不再提出值得採納的東西。

審查每個 suggestion：critic 曾提議過 off-screen coordinate，以及違反 house style
的 gradient/grid。運用判斷力，永遠不要盲從——prompt 已告訴 model style 是
deliberately flat 以抑制該偏差。

---

## Data flow（目標）

```
handout-kit HTML  (per-chapter authoritative file, see README「輸入」)
   │  (作者閱讀該節，手動撰寫 storyboard——非自動生成)
   ▼
video/storyboards/<id>.yml
   │
   ├─ lint.py              error: plain-Text 欄位中有 markup、unbalanced $；    (DONE)
   │                       warn: prose 中的手動 \\、curve 上的 hollow point
   │                       （帶 hollow_reason: <why> 的 point 免除）
   ├─ sizecheck.py         build scene（不 render）。error: stacked sibling     (DONE)
   │                       size 不同、或元素被 clip 出 frame；
   │                       warn: 教學 prose 使用 muted、spill past safe
   │                       margin、或兩個 content block 重疊
   ├─ schema.py            validate format, list reveal target                   (TODO)
   │
   ▼
narration.parse_say        將每個 `say` 在 {show} marker 處拆成 beat              (DONE)
   │                        → 每場景的 ordered (beat_text, reveal_target) list
   ▼
synth                      每個 beat 一個 clip；mock = 依 word count 的靜音        (DONE)
   │                        （billed Gemini = pipeline/tts.py）；測量
   │                        duration → audio/<id>/… + manifest.json
   ▼
render (scene.py)          Manim render 每場景（silent）；reveal 在其 beat        (DONE)
   │                        開始時觸發；audio duration 驅動 hold（讀
   │                        manifest.json）。每場景一個 silent MP4。
   ▼
sync guard                 reuse manifest freshness、短/reveal-only beat warning、(DONE)
   │                        render 後 video duration vs lead+audio(+tail) audit
   ▼
compose (ffmpeg)           將每場景的 narration 鋪在其 video 下（delayed to       (DONE)
   │                        第一個 reveal），每個場景邊界淡出黑場再淡入
   │                        （fade-through-black，--transition 預設每側 0.2s），
   │                        intro/outro 為 silent track，concat。
   ▼
video/output/<chNN>/<sX.Y>/<id>.mp4
```

**Orchestrator：** `make.py` 是唯一入口點——一條指令跑完 parse → synth →
render → compose（`make.py --storyboard <yml> --backend mock`），包含
pre-render 的 `lint.py` / `sizecheck.py` guard。它是 **offline only**：mock
synthesis（依 word count 的 silent clip），不計費。Real Gemini TTS 是計費的，
刻意**不**接入 make.py（見 CLAUDE.md），因此 narrated master 仍走保留的
lower-level chain `pipeline/tts.py` → `build.py` → `mux.py`——被 make.py
取代用於 offline 工作但保留、不刪除。以 visual payload 為 key 的 per-stage
caching（使得編輯 `say` 會重新 synthesize audio 但不重新 render Manim）仍為
(TODO)。

### Alignment，重述（避免在重寫中遺失）

第一代的洞見沿用：alignment **不依賴** TTS 回傳 word-level timestamp。我們
**每個 beat 合成一個 clip**，測量其真實 duration，該 duration *就是* reveal
hold。Gemini 換了 synthesizer，不換 alignment model。（已確認：Gemini 回傳
24 kHz mono 16-bit raw PCM，wrap 成 WAV 後 locally 測量；在 §1.1 上 end-to-end
驗證——每個 reveal 落在其 narration beat 的 ~1 frame 之內。）

同步相關常數集中在 `pipeline/timing.py`：`SCENE_LEAD_SECONDS` 是 scene 開頭
等待與 mux/critic offset 的單一來源，`SCENE_TAIL_SECONDS` 是 content scene
收尾等待。`make.py --reuse-audio` 會在 render 前驗 manifest freshness（deck id、
scene、beat count、`{show}` target、`text_hash`、WAV 存在與時長），避免 MiMo/Gemini
舊 take 被靜默沿用；render 前會警告短 beat / reveal-only beat，render 後用 ffprobe
檢查 content scene video duration 至少覆蓋 `lead + narration`，並回報相對
`lead + narration + tail` 的偏差。

### MiMo 口語軌（single-source）＋非決定性（2026-06-14）

Gemini 直讀 inline LaTeX；MiMo（`mimo-v2.5-tts`）不行，需「數學攤成口語」的旁白。
唯一源＝`content_scripts/<deck>.spoken.yml`（口語＋`{show}`）；`pipeline/derive_spoken.py`
由它＋正典 storyboard 生成 `storyboards/<deck>_mimo.yml`（`say` := spoken、`meta.id` 加
`_mimo`、`voice` Mia）＋`content_scripts/<deck>_narration_spoken.md`（閱讀視圖，`{show}` 移除），
且 `--check` 守 parity（scene/`{show}` 結構與正典一致、口語無 `$`）杜絕兩軌 drift。

對齊模型同上（每 beat 一 clip、量 duration 驅動 reveal）；`MimoTTSBackend`（`tts.py`，OpenAI
相容、urllib、雙 header、比照 `critic.py`）預設**裁 beat 頭尾靜音**（`audio.trim_silence`，留 0.08s），
並在 manifest 記錄 raw/trimmed/cut 秒數，方便 debug padding。真音訊 render 走
`make.py --reuse-audio`（讀 `tts.py` 的 manifest、不重 synth；非 reuse 但偵測到
真 manifest 會拒絕用 mock 覆蓋；reuse 會做 stale manifest 檢查）。**MiMo 非決定性**：同文字重合成＝不同 take、長度 ±~10%，
影片長度不可重現；要定版就別重合成。Mode B（codex）稽核兩版＋收斂，模板見
`content_scripts/_audit/PROMPT-narration-modeB.template.md`（含「數學內容正確性」維度，未認可章節必跑）。

---

## Open question／尚未決定

- ~~Template catalog for gen-2~~——resolved 2026-06-11：即上方的 catalog。沿用的
  content template 全部保留；gen-2 新增 `derivation`（2026-06-11），接著
  `value_table` / `graph_compare` / `sign_chart`（依使用者指示提前為 §1.3 /
  ch02 / §4.5 建構——先做 static template，hook 仍為 animation layer）。
- BGM：source、ducking、licensing。
- `{show ...}` target grammar：dotted（`math.0`）vs bracketed（`math[0]`）。目前為 dotted。
- Gemini specifics（resolved）：model id `gemini-3.1-flash-tts-preview`（CLI-configurable）；
  voice `meta.voice` / `Charon` 作為 prebuilt voice name；output 為 24 kHz mono 16-bit raw
  PCM，wrap 成 WAV 後 locally 測量。Paid tier 確認可運作；free tier 對此 model
  限制 ~10 requests/day，因此 batch synthesis 需 paid billing。`tts.py`
  遵循 per-minute 429 `retryDelay` 並在 per-day cap 時 fail fast。
