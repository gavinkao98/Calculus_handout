# 影片產線——設計（第二代）

這是重新設計的 handout → lesson-video 產線。輸入為 HTML handout
kit（`../handout/`；per-chapter authoritative file 列於
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

- **TTS 攤平 LaTeX、刪掉 gen-1 的 spoken-math 大表。** 原 gen-2 用 Gemini 直讀
  inline LaTeX；**2026-06-16 起 TTS 收斂為 MiMo**（不讀 LaTeX），故每節多一個輕量
  `<deck>.spoken.yml`（單一源、`derive_spoken.py` 派生、`--check` 守 parity）把數學
  攤成口語——但這仍**不是** gen-1 那張大規則表：正典 narration 依舊只寫一次、LaTeX
  直接 inline（供閱讀版與 storyboard `say`），攤平只發生在 MiMo 軌。
- **一個 narration 欄位搭配 inline reveal marker。** `say` 同時承載文字和
  timing cue。不再有獨立的 beats/bookmark/reveal array。

另加一個新的 product requirement：**每節都有 intro 和 outro animation**，因此
scene `kind` 是 first-class 的，且支援 silent（no-narration）scene。

---

## 沿用 vs 重寫

| 原封沿用（已驗證，重寫無收益） | 從零重寫 |
|---|---|
| `visuals/theme.py`（Midnight Canvas palette + Plex/LaTeX type scale + layout metrics） | storyboard schema + format |
| `visuals/graph_utils.py`（safe expr eval + sampling） | narration → beats compiler |
| `visuals/layout.py`（16:9 zone layout） | scene templates |
| ffmpeg mux/concat logic *（現於 `make.py` compose；gen-2 的 `mux.py` 已刪）* | TTS backend（MiMo；Gemini 已退場） |
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
  voice: Dean                     # MiMo built-in voice (default; voice-design/Calm Professor retired 2026-07-05)
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
| `accent` | definition-family 必填 | 色彩角色：`definition` / `theorem` / `proposition` / `example` / `warning` / `procedure` / `recap`。取代舊的 `content_type`。**只管顏色**，不管 eyebrow 字卡（見下 §Eyebrow 字卡 resolver）。 |
| `scene_role` | no | eyebrow 字卡的**教學 beat 軸**（與 `accent` 顏色軸正交）。exposition beat（`motivation`/`intuition`/`bridge`/`forward-ref`/`setup`/`roadmap`）→ **無字卡**；形式物件（`definition`/`theorem`/`remark`/…）→ 對應字卡。省略＝沿用模板/`accent` 預設字卡（見下 §Eyebrow 字卡 resolver）。 |
| `title` | yes | 螢幕上的 scene title；可使用 `$...$` 表示數學 |
| `say` | yes | 單一 narration 欄位（見下方） |
| `statement`、`math`、`steps`、`plots`、… | per template | 螢幕上的 visual payload |
| `hook` | no | `"<module>:<fn>"` custom-animation factory，可從 `video/` import（例如 `"animations.ch01_inverse_functions_hooks:can_we_go_backwards"`）。Factory 接收 `(spec, ctx, template_blocks)` 並回傳最終的 block list：替換 block 的 mobject **但保留其 reveal id**（使 `{show ...}` marker 和已核准的 narration 不受影響）、將 static element defer 到一個 beat、或附加一個 callable anim `(scene, mobject, ground) -> seconds spent`（`pipeline/blocks.py`）。Storyboard 中的 template payload 保留為 no-hook fallback——刪掉 `hook:` 行即恢復 stock scene。在 `pipeline/templates/__init__.py:_apply_hook` 中接線。 |

### Template catalog（content scene）

每個 template 一行——教學形狀、payload 和 `{show ...}` 可指向的目標。
Demo storyboard 在 `storyboards/_demo_*.yml`。

> **Direction D（2026-06-20 視覺重設計）後的目錄。** 標 ★ 者 schema 有變或全新。
> `definition_math` / `theorem_proof` / `procedure_steps` / `value_table` / `sign_chart`
> / `recap_cards` 的 payload 欄位**不變**（只是視覺重皮）。落地時的暫存驗證稿
> `_demo_redesign.yml` 已清（git 歷史可取回）；活的回歸樣本＝上述 `storyboards/_demo_*.yml`。

| template | 教學形狀 | payload 欄位 | reveal target |
|---|---|---|---|
| `definition_math` | definition / statement / note / motivation：statement + math lines（key line 用 `anim: highlight` → amber + glow） | `statement`、`math[]`、`kicker`、`math_align: center`(opt) | `math.N` |
| `theorem_proof` | gold-bar 面板 statement + 藍點 proof steps + 綠 QED | `statement`、`proof[]`、`qed` | `proof.N`、`qed` |
| `procedure_steps` | 01/02 藍數字步驟 + 底部圓角 worked strip | `steps[{text,math}]`、`worked[]` | `math.N`、`worked` |
| `derivation` ★ | **統一數學系統**：式子左欄 + reason rail（dotted leader）+ amber ∴ result + 綠 ✓ check | `steps[{math, reason?}]`、`result:{math, reason?}`、`check:{math, reason?}`；**或** back-compat `lines[]`（`anim: highlight` → result）、`statement` | `step.N`/`result`/`check`（或 `line.N`） |
| `callout` ★ | Remark / Caution / Note：eyebrow `[ TYPE n.n ]`＋title masthead，body 文字置於標題下方（色隨 type：remark 藍／caution 紅／note 琥珀）；`body` 字串→散文、list→條列（同色圓點）。同 `definition_math` 走 `scene_head`＋`place_body`（2026-06-29 改版，見下） | `type: remark\|caution\|note`、`number`(opt)、`title`、`body`(字串或 list) | `body` |
| `graph` ★ | **統一 graph 引擎**：`mode: single`（一張全幅 plot）或 `mode: 2up`（兩張並排比較） | single：`axes`、`plots[]`、`annotations[]`；2up：`left`/`right` `{axes, plots, caption, verdict}`、`annotations[]` | single：`annotation.N`、`plot.N`(`reveal:true`)；2up：`caption.left/right`、`left.plot.N`/`right.plot.N`、`annotation.N` |
| `value_table` | 數值 limit 表 / formula grid（punchline 欄／列鋪 scene accent 同色 tint + 抬升 ink） | `header[]`、`rows[][]`、`reveal: rows\|cols`、`accent_col`/`accent_row`、`statement` | `row.N` 或 `col.N` |
| `sign_chart` | number line + signed interval rows（+綠/−紅 glow、↗/↘） | `points[]`（`excluded: true` 表示 break）、`rows[{label, marks}]`、`statement` | `mark.R.I`（row R, interval I） |
| `recap_cards` | key point（amber 發光編號當 marker）+ blue-bar remember-formula cards | `points[]`、`formulas[]` | `point.N`、`formula.N` |
| ~~`example_walkthrough`~~ | **deprecated → 用 `derivation`**（其 reason rail 取代並列推理欄；舊 scene 仍可渲） | — | — |
| ~~`graph_focus` / `graph_compare`~~ | **deprecated alias → `graph` + `mode: single`/`2up`**（payload 不變；舊 scene 仍可渲） | — | — |

**全 content 模板共用的選用欄位（上表各列不再重複）：** `scene_role`（eyebrow 字卡的 beat 軸，含「無字卡」；見下 §Eyebrow 字卡 resolver）、`kicker`（覆寫 eyebrow 標籤字、保留 accent 配色）、`part: {current, total}`（多頁分頁指示器，右上角）、`hook`（custom-animation factory，見上 §`content` scene 欄位）。`definition_math`／`theorem_proof` 另支援 `aside`（L3 右 rail enrichment 卡：主內容夠稀疏才展開成雙欄、過密自動收掉）。

### Eyebrow 字卡 resolver（`scene_role`；2026-07-01）

**兩條正交的軸。** eyebrow 字卡（`[ DEFINITION ]` 等）與顏色是**兩件事**：`accent` 決定**顏色**（`blocks.ACCENT_ROLE`），`scene_role` 決定**字卡**。字卡標的是「這格是什麼**教學 beat**」，不是「什麼數學物件」——對定理格兩者重合，但對開場／動機／直覺這類 exposition beat 兩者分岔，字卡不該硬套形式標籤。

**單一 resolver。** 字卡在**一處**決定——`pipeline/scene_roles.py:resolve_chip(spec, default_label)`，由 `templates/_common.py:scene_head` 呼叫。優先序（高→低）：

1. `kicker` — 顯式覆寫字（既有行為）
2. `label` — 顯式字卡字（如 `theorem_proof` 的 `[ proof of the chain rule ]`）；**贏過 `scene_role`**，使後加的 `scene_role` 絕不會抹掉作者寫死的 label
3. `scene_role` — beat → 對應字卡（`SCENE_ROLE_CHIP`；可為 `None` = 無字卡）
4. `default_label` — 模板預設（`definition_math` 的 `LABEL[accent]` / 各模板固定字串）

未知 `scene_role` → `raise`（typo guard；lint 亦攔）。

**字彙（`SCENE_ROLE_CHIP`）。** exposition／修辭 beat → **`None`（無字卡）**：`motivation`、`intuition`、`bridge`、`forward-ref`、`setup`、`roadmap`。形式／半形式物件 → 對應字卡：`definition`/`theorem`/`proposition`/`example`/`remark`/`caution`/`note`/`procedure`/`recap`/`derivation`（形式值先備齊，使 `scene_role` 可逐步成為完整字卡軸；本波只實際用到 exposition + `remark`）。

**視覺規則是單向的。** exposition ⟹ 無字卡；但**無字卡 ⇏ exposition**——`graph`／figure 場景本來就無字卡（走 `_build_single`，不經 `scene_head`），是另一條路徑。所以不要反推。

**無字卡的機制＝隱形 placeholder。** `scene_head` 仍以預設字建出 eyebrow mobject 並定位（量測其高度），再 `set_opacity(0)` 隱形、且**照樣放進 index-0 的 block**。如此：(i) title 錨在與有字卡場景**完全相同**的 y（`title.next_to(eyebrow, DOWN)`）→ 無跨場飄移（`MASTHEAD_TOP` 不變式，下游 `body_zone`/`place_body` 也不動）；(ii) 保住 `head[1]`/`blocks[1]` 取 title 的既有契約，六個 index-based 模板零改動。static block 走 `scene.py` 的 `self.add()`（不 FadeIn、不強設 opacity），隱形得以保持。**Lectern spine 的 accent cap** 對 chipless 場景改從 **title 頂端**起算（`_spine_cap_top`），不照亮字卡列的空白帶——否則藍 cap 會懸在標題上方的空白處（2026-07-01 修）。

**lint（`lint.py:_scene_role_issues`）。** 未知 `scene_role` → error；`scene_role` 與 `label`/`kicker` 併存 → warn（`scene_role` 被 outrank、形同失效）。**刻意不做**「`accent: definition` 無 `scene_role` 就報」的全域 lint（會誤傷真定義）。

**本波邊界（Codex 標的「第二次遷移」）。** resolver 這次**只接 `scene_head`**。仍散在外面、未上 resolver 的：`graph`（不經 `scene_head`）、`example_head` 自建的 `[ example ]`、各模板傳給 `scene_head` 的固定 `default_label`。若未來要讓 `scene_role` 全面控管字卡（含 graph 加/去字卡），需再一次 header 重構。**待清理（本波刻意延後）：** ch01 四格用 `derivation` 描述 handout Example 但缺 `prompt:` → 現渲 `[ derivation ]`（`_example_missing_prompt` 已 warn，補 `prompt:` 即成 `[ example ]`）；ch01 兩格 motivation/Example 走 `value_table` → `[ table ]`（低風險）。

測試：`_selftest_scene_roles.py`（resolver 6 例 + lint 4 例 + scene_head chipless build 1 例）。

**Brand frames（`kind` 鍵，非 content template）：** `intro`（paper course-map）、
`outro`（paper end-slate；opt `next_section`/`next_title` → 自畫品牌紅三角 caret＋「Next §x.x」hint）、
`divider` ★（新，dark 章節 opener：發光 hero curve + ghost numeral + eyebrow/title/
subtitle + progress dots；欄位 `eyebrow`（別名 `kicker`；省略→`Section {section}`）/`title`（省略→`meta.title`）/`subtitle`（別名 `sub`/`tagline`）/`ghost`（省略→`meta.section` 章號）/`progress:{current,total}`（省略→由 `meta.sections` 推導）/`accent`）。三者皆 silent（不吃 `say`），文案多讀自 `meta`（`chapter`/`chapter_title`/`section`/`title`/`sections[]`）；intro 另吃 scene 層 `tagline` 與 `duration`，詳見上 §Scene kind 與下方最小範例。

### Audio policy（全章節統一）

本產線的預設聲音設計是 **narration-first**：數學教學內容已同時承載旁白、公式、
圖形與 reveal timing，連續背景音容易和工作記憶競爭。所有章節、所有 section
統一依 template 決定音樂／音效，不依單節喜好臨場加配樂。

**House cue candidates（待使用者裁決）。** 預設不用外部素材庫音樂，改用 repo 內自有 cues：
[`pipeline/assets/audio/house/`](pipeline/assets/audio/house/)。這些 WAV 由
`generate_house_cues.py` 程序合成，無第三方 sample、無素材庫來源、無外部 API。
音樂底色固定為無人聲、無鼓點、無明顯旋律 hook 的 soft pad / bell texture。
剪輯音量以旁白為中心：BGM 約比旁白低 20-30 dB，所有 stinger / whoosh 都短、淡、
一次性。候選試聽裁決稿為
[`pipeline/assets/audio/house/REVIEW-house-audio-candidates.html`](pipeline/assets/audio/house/REVIEW-house-audio-candidates.html)。

| candidate | 風格 | cue set |
|---|---|---|
| A | 清亮品牌感 | `calculus_*` |
| B | 溫暖低調（目前建議） | `candidate_b_*` |
| C | 極簡自然 | `candidate_c_*` |

**Template-level 規則。**

| kind / template | 音樂規則 | 音效規則 |
|---|---|---|
| `intro` | **使用裁決出的 intro bed**。6-8 秒淡入淡出；不接到第一個教學場景。 | 不需要額外音效。 |
| `divider` | **使用裁決出的 divider stinger**。只標示 act/stage 切換，不鋪滿前後內容。 | 不另加音效。 |
| `outro` | **使用裁決出的 outro bed**。用於結尾呼吸與品牌收束。 | 不需要額外音效。 |
| `definition_math` | **不放 BGM**。定義與符號需要乾淨旁白。 | 通常不放；key line 的 visual highlight 已足夠。 |
| `theorem_proof` | **不放 BGM**。證明步驟不可被音樂稀釋。 | 不放逐步音效；`qed` 也不加 ding。 |
| `procedure_steps` | **不放 BGM**。程序要靠旁白節奏和畫面步驟讀清楚。 | 不放每步提示音。 |
| `derivation` | **不放 BGM**。任何代數、極限、導數連續推導一律乾聲。 | 不放每行 reveal 音效。 |
| `value_table` | **不放 BGM**。表格讀值時保持安靜。 | 不放每列／每欄音效。 |
| `sign_chart` | **不放 BGM**。符號區間判讀需要低干擾。 | 不放每個 mark 音效。 |
| `graph` | **不放 BGM**。圖形講解以旁白和動畫承擔節奏。 | 只有大型視覺轉換（例如整張圖切入、反射、domain restriction）可用極淡 whoosh；單一曲線、點、標籤 reveal 不加。 |
| `callout` | **不放 BGM**。Remark/Caution/Note 是教學語氣的轉折，不是音樂段落。 | `type: caution` 可用裁決出的 caution ping；`remark` 預設不加。 |
| `recap_cards` | **不放 BGM**。Key Takeaways 仍是 narrated content；音樂留給後面的 `outro`。 | 可在第一張 recap 卡出現時用一次短 chime；不要每點都加。 |

**授權與來源規則。**

- 優先使用 YouTube Audio Library 中「不需署名」的 music/SFX，尤其是 `intro`、`divider`、
  `outro` 這種品牌場景。
- 可接受 Pixabay Content License 的 music/SFX，但下載當日必須保存來源 URL、授權頁、
  作者、下載日期；若素材頁標示 Content ID registered，除非沒有等價替代，否則避開。
- 可接受 CC0 SFX。CC BY 只在確定會於影片描述署名時使用。**不用** CC BY-NC、CC BY-ND、
  來路不明的 "no copyright" YouTube 轉載音樂或無法保留授權證據的素材。
- 真正加入音檔時，第三方素材清單必須進版控，記錄檔名、用途、來源、license、是否需署名；
  沒有這份清單，不進最終 mux。

#### Plot label 顏色慣例（graph，2026-06-17 拍板）

**plot 的標籤預設繼承該 plot 的 `color_role`——標示函數／線的標籤，顏色跟它標示的函數／線一致。** cyan 的 `$y=x^3$` 配 cyan 標籤、orange 的 `$\sqrt[3]{x}$` 配 orange 標籤、`muted` 的 `$y=x$` guide line 配 muted 灰標籤。逐項可用 `label_role` 覆寫。

- **緣由：** 原本 `function` label 預設 `primary`（白）、`line` label 預設 `warning`（紅），標籤與其曲線／線**不同色**——尤其 `muted` 的 `$y=x$` 參考線配到刺眼紅標（VISUAL-FRAME gate1 在 §1.1 scene 11／12 抓到）。改為繼承 `color_role` 後，曲線↔標籤的顏色關聯一眼可辨（使用者 2026-06-17 明確要求「標示函數的標籤顏色跟函數的顏色一致」）。
- **`point` label** 仍預設 `text`（中性，給座標／標記註解用），可用 `label_role` 覆寫。
- 實作：[`pipeline/templates/graph.py`](pipeline/templates/graph.py) function／line 分支的 `role=plot.get("label_role", str(plot.get("color_role", "secondary")))`。compare（2up）模式共用 `_plot_blocks` 故一併適用。

#### Plot label 重疊偵測（graph，2026-06-19）

**兩個曲線／線／點的方程式標籤互疊由 `sizecheck._graph_label_overlap_issues` 自動抓（advisory warn，門檻 `LABEL_OVERLAP_FRAC=0.30`）。** 這是 graph 層豁免（`Block.layer="graph"`，把「點落在曲線上」「標籤緊貼曲線」等刻意重合放過）唯一刻意開的口——label-vs-label 互疊是 heuristic／手填 `label_point` 無碰撞避讓造成的真缺陷。修法是給標籤一個顯式 `label_point` 分開。

- **不是 error，是 warn：** label 擺位偏 heuristic，render-blocking 太兇；嚴重時印 warn 讓人裁決。曲線／點本身的重合仍豁免（不誤報）。
- **餵進 critic（B.1b）：** `sizecheck.graph_label_geometry(meta, scene)` 算出每個標籤的 frame-fraction box＋region＋重疊，由 [`pipeline/critic.py`](pipeline/critic.py) `build_prompt` 注入 VLM context，讓視覺幀稽核（gate2）對 `V2`（蓋字）/`A1`（壓線）有確定性依據、能指名往哪移，且未偵測到重疊時明告「勿幻覺出碰撞」。
- **不做自動擺位：** 連 Code2Video 自己都沒有標籤自動重擺演算法（其「重擺位」是 VLM 整段重生，見 [`CODE2VIDEO_STUDY.md`](CODE2VIDEO_STUDY.md) 2026-06-19 addendum）；故走「偵測＋餵 VLM 建議」，不寫投機性搜尋。
- 實作：`sizecheck.py` `_graph_label_overlap_issues`／`graph_label_geometry`；標記在 `graph._label`（`_graph_label`／`_graph_label_text`）。fixture：[`storyboards/_demo_label_overlap.yml`](storyboards/_demo_label_overlap.yml)。

#### 座標軸刻度／級距：何時該標（graph，2026-06-19）

**預設無刻度數字是刻意的 house style，不是遺漏。** `Axes` 一律畫軸線＋箭尖＋軸尖的 `x`／`y` 字母，但 `include_ticks`／`include_numbers` 預設 `False`（深藍工程底 + 乾淨軸的 3b1b 風格）。是否補刻度，**依該圖在教什麼分兩類**：

| 圖的類型 | 判準 | 刻度規則 | 例 |
|---|---|---|---|
| **qualitative（形狀）** | 旁白只談形狀／趨勢／對稱／單調，不指名具體座標 | 維持無刻度（預設） | 反函數對 `$y=x$` 對稱、漸近線行為 |
| **quantitative（讀值）** | 旁白指名某座標或要讀值（「在 `$x=a$`」「值為 `$L$`」「`$\arccos 1=0$`」） | **必須**在那些座標放 teaching-tick | `$\sin\theta=\tfrac13$` 求 `$\tan\theta$`、極限讀值 |

- **teaching-tick 機制（已存在、opt-in）：** axes 區塊寫 `x_ticks: [{at, label}]`／`y_ticks: […]`，在指定座標畫**幾個關鍵刻度**（例如在 `$x=a$` 標 `a`、在 `$y$` 軸標 `L`），而非整條數線——保住乾淨軸又給尺度錨點。實作 `graph._axis_ticks`；數字渲成 math，故 `a`／`L` 會是斜體。
- **軸字母：** `_add_axis_labels` 預設在軸尖標 `x`／`y`；該圖確實不需要時用 `axis_labels: false` 關掉（勿濫用）。
- **enforcement：** 此為**撰稿慣例**，目前靠人／VISUAL-FRAME gate 判讀，**未加 lint**（曾評估「旁白座標引用 ↔ teaching-tick」的 A-2 lint，因正則偵測旁白偽陽／偽陰風險，暫不採；情境變了再評）。緣由與取捨見 [`content_scripts/_audit/REVIEW-graph-axis-label-convention-proposal.html`](content_scripts/_audit/REVIEW-graph-axis-label-convention-proposal.html)。

## Lectern 版面網格（2026-06-21 版面重設計）

**問題（2026-06-21 設計盤點 #1，最高槓桿）：** 各模板各選左軸（`scene_head` 的
gutter、`derivation` 的式子右緣、`callout` 的置中…），任何「第二內容流」
（`derivation` 理由、`procedure` 結果、`recap` 公式卡）跟著 primary 欄寬**浮動**，
導致沒有兩種場景對齊、16:9 右半結構性閒置；`graph` 標題用 `SAFE_MARGIN`、比別人更左，
切到 graph 場景時標題往左跳（使用者回報的「標題飄來飄去」）。

**解法——一條全模板共用的網格**（`pipeline/templates/_common.py`，全由 `theme` 度量
推導、無新魔術數字）：

| token | 意義 |
|---|---|
| `SPINE_X` | 唯一左對齊軸（masthead ＋ 每個 primary 欄）。 |
| `RAIL_X` / `col_x(n)` / `RAIL_COL=7` | 固定右 rail 欄；第二內容流一律 snap 到此。`RAIL_COL` 是唯一旋鈕，一改全模板一起平衡。 |
| `PRIMARY_W` / `RAIL_W` | primary（spine→rail）與 rail（rail→右緣）欄寬。 |
| `MASTHEAD_TOP` | eyebrow 頂的固定 y；title 釘在其下固定間距，故標題 top 永不飄。修法＝讓 `scene_head` 成為**唯一** masthead（自刻/略過它的模板才會飄）。 |

**各模板採用：**

- `definition_math`：**單欄**（退兩欄，2026-06-21；見下「definition 單欄」節）——散文
  `statement` 滿寬 ＋ 符號式堆其下 ＋ `place_body` 上偏置中。內容稀疏時可選 L3 `aside`
  卡 snap `RAIL_X`（會 graceful 收合，不與內容競爭）。
- `derivation`：理由 snap `RAIL_X`；dotted leader 改為**目錄式可變長 connector**
  （短式配長 leader，連接永遠成立）。無理由的純鏈仍置中（不變）。
- `procedure_steps`：result 欄左對齊 `RAIL_X`（原右對齊 far gutter、Codex 兩輪嫌 detached）。
- `recap_cards`：**不用 rail**——改為單一全幅編號點欄（`points[]` 以 `01/02/03` ＋ 全寬 prose
  左堆疊、`center_in_zone` 上偏置中）；舊「公式卡 snap `RAIL_X`」雙欄版已退場。
- `theorem_proof`：左軸用 `SPINE_X`（proof 仍刻意 `+0.4` 縮排階層）。**statement 字卡採容量感知的
  measure-driven regime（2026-07-05）**：**只有「不換行」才留 rail**（`RAIL_MAX_LINES=1`：單行散文 /
  rail-fit 公式）→ 右上 rail、**shrink-wrap、右緣貼 gutter**；**一換行就想升 title 下全寬 band**（左緣
  `SPINE_X`、與 proof 同 `round(left)` 欄 stack）——**但 band 把 statement 疊到 proof 上方、較耗縱向；若
  band＋proof 超出 body zone，自動退回兩欄 rail**（statement 右欄、proof 左欄用滿縱向），讓長證明仍單頁
  塞得下（§3.1 實例：`continuity_statement`→band、`continuity_argument`→rail fallback）。判定：
  `statement_regime()` 給「換行→想 band」的**美學偏好**（讀**真實 `brand.prose` 行數** `len(submobjects)`，
  對 `body_text`／`_prose_lines` 皆精準）；`build()` **先建 proof 量高度**、加**容量 fallback** 定案；
  sizecheck 的升-band advisory **改讀實際 build 出的卡片幾何**（band＝貼脊全寬、rail＝貼右緣窄卡）→ 反映
  真實結果、零 drift。過寬公式**不縮小**（band 走 `prose(max_width=None)`），逾 band 寬交 `_overflow_issues`。
  `RAIL_COL` 不動——rail 仍留給次要短卡（`build_aside`），只有主角 statement 依量體＋容量改欄。
- `graph`：title 左軸 `SAFE_MARGIN`→`SIDE_GUTTER`（=`SPINE_X`），與其他模板水平對齊。

**figure 置中是刻意、非 drift（decline 的 finding）：** `graph`／`value_table`／
`sign_chart` 是 figure——masthead 左錨、figure 本體置中，是一致的 house rule，**不要**
硬改成左 flush（盤點的「左 stub」屬 editorial-drift 級）。`sign_chart` 數軸維持 `muted`
也正確（參考骨架，非內容）。

**四色貫穿內文（增量 6）：** `value_table` punchline 的 tint＋accent cell 改跟
`accent_role`（原寫死藍，連 theorem-accent 表也藍）；映射 `_ACCENT_INK`。**註：
`play_block` 的 `Flash` 維持 amber 是對的**——它閃的是依「強調=amber」固定語意本就琥珀的
result/key 元素，改了反而錯（先前盤點誤列為 bug，已更正）。

> **更新（2026-06-29，使用者要求「拿掉爆炸特效」）：** 上述 `Flash` 爆閃已**全片移除**——
> `play_block` 中 `write_glow`／`flash_in`／`slide_pop` 三個揭示動畫的 `Flash` 拿掉，只留
> `Write`／`FadeIn` 浮現（模板的 `anim` 字串不變）。重點／result/key 行的強調改由既有
> 「amber 顏色＋持久 `text_glow` 光暈」（靜態，留在最終幀）承載；本段「Flash 維持 amber」之
> 結論隨之作廢（歷史紀錄保留不回改）。

**短內容的下半留白（2026-06-21 解決）**：`place_body`／`center_in_zone` 以
`UPPER_BIAS_FRAC`（≈0.55）把短內容偏 body zone 的**上中段、貼標題**，剩餘留白集中底部、
由角落 motif 平衡——取代原本的死正中對齊（短內容會在標題下與底部**都**留大洞、與標題脫節，
最顯著於單欄 definition）。高內容仍 top-anchor。詳見下「內容分量自適應」與「模板視覺修正」。

**驗證：** §1.1 全 19 場景重渲、逐幀檢視無回歸（rail-derivation `first_inverses`／
`testing_x_and_x_squared`／`shape_can_mislead` 理由欄一致對齊、masthead 跨模板對齊）；
gate-1 visual-frame 稽核 0 blocking。盤點全文與三方向 mockup 見對話紀錄（2026-06-21）。

## Scaffold 承載與視覺契約（first-learner 框架；SPEC §6）

讓「為什麼做這個」「正在解什麼」「默默用到什麼前提」上畫面、可確定性檢查、可回溯核准源的承載層。
權威 spec＝[`SPEC-pedagogy-firstlearner-framework.md`](SPEC-pedagogy-firstlearner-framework.md) §6（承載設計 a–d）。
**收斂原則：不為三個欄位各立新機制**（不與既有 `kicker`／`aside`／`statement`／`subtitle` 疊床），改由一個共用
helper ＋ deck-level registry ＋ 既有 provenance 慣例承載。落地當下**零行為改變**——缺 `scaffold` 一律 no-op。

**共用渲染（[`_common.render_scaffold`](pipeline/templates/_common.py)，掛 Lectern）：** content 場
（`definition_math`／`theorem_proof`／`derivation`）的 `scaffold.motive` → 標題下一行**較小的 `text` role**「為什麼」
（`prose_sm`、滿 `CONTENT_W` 不早 wrap）；**不可 `muted`**——違反上「教學內容用 `text`/`primary` 非 `muted`」並觸發
`sizecheck` muted-prose 警告，de-emphasis 靠字級／位置、非調暗。`divider` 的 `scaffold.problem` → 標題下用
**`brand.prose`（`prose` 字級、`text` role）**；純 `$…$` 問題式由 `brand.prose` 自動走 `math_line` 渲為**顯示
公式行**、純文字則 wrap（無專用 formula-block compositor），字級比會 wrap 成小字的 `subtitle` 大。首用場的 `scaffold.flag: <assumption_id>`
→ 小 badge／aside（`assumes` 標籤＋該 assumption 文字，走 `build_aside` snap primary 欄）。**缺 `scaffold` 一律
no-op**（`render_scaffold` 回傳 `[]`，render 不變、零行為改變）。

**`meta.assumptions` registry（deck-level，置於 `meta:` 之下）：** 讓「前提首用才標」可確定性檢查——

```yaml
meta:
  assumptions:
    - id: radians
      text: "$\\theta$ in radians (arc length $=\\theta$)"
      first_use_unit: sector_inequality
      source: "chapter3-print-standalone.html §3.1 · radians 預告句"
```

每筆 `{id, text, first_use_unit, source}` 必須在 `first_use_unit` 渲出對應 `scaffold.flag: <id>`；「是否用到／何處
首用」由作者**顯式宣告**，閘不推斷（[`pipeline/pedagogy.py`](pipeline/pedagogy.py) 讀 `meta.assumptions`）。

**`meta.pedagogy_profile`（預設 `first_time`，可覆寫）：** PD1 拆步粒度與 PD2 motive 要求讀此值；SP1 只定義
`first_time` 行為，覆寫語義（如 `review`／`expert`）留 YAGNI 日後。

**scaffold provenance 走 OTF 的 `ref:`／`refs:`：** 場景的 `ref:` 由所有上畫面文字欄位**繼承**；欄級覆寫用 `refs:`
**flat map**——key 是欄位路徑字串（**非巢狀物件**），如 `refs: { scaffold.motive: 'md:…' }`（[`pipeline/provenance.py`](pipeline/provenance.py)
讀 `scene.refs.get("scaffold.motive")`，巢狀 `refs: { scaffold: { motive: … } }` 會被 silently 漏掉）。**`source:` 是
freeform 人讀標籤、不被解析為 provenance**（provenance 只認 `ref:`／`refs:`）。OTF 規則（繼承／覆寫時機／可解析路徑）
的權威落點是 [`CONTENT_METHODOLOGY.md`](CONTENT_METHODOLOGY.md)；本節只記 scaffold 在視覺層的承載。

## Worked-example 題目結構（2026-06-21）

課堂式 worked example **顯示題目**、不用模糊描述標題。有 `prompt:` 的 content scene 走
`_common.example_head`：`[ EXAMPLE ]` eyebrow ＋ **題目當 headline**（statement-weight prose，
不是 towering 的 bold title）＋ 細線 ＋ `SOLUTION` lead，解題本體接在其下。對映 handout 的
`example`＋`solution`。純 `[ EXAMPLE ]`（不編課本題號）；illustrative 探索型（非單一題目）不放
`prompt`。`title` 仍保留供 schema（並作 `critic.py` 的場景標籤），example_head 忽略它。

**`prompt:` 是 worked example 的必填、`derivation` 無 `prompt` 時 eyebrow 預設改 `[ DERIVATION ]`（2026-06-29）：**
`derivation` 模板「無 `prompt:`」的 eyebrow 預設由 `[ EXAMPLE ]` 改為 **`[ DERIVATION ]`**（模板同名）——
舊預設把每條證明推導鏈都誤標成 example（ch03 §3.1 的 scene 3/6 即此）。據此：
- **是課本 Example** → **必填 `prompt:`**（題目；太長放簡略版），走 `example_head` 顯示 `[ EXAMPLE ]`＋原題＋細線＋`SOLUTION`。
- **是純推導**（非單一題目的證明步驟）→ 不寫 `prompt:`，eyebrow 預設 `[ DERIVATION ]`；要別的字用 `kicker:` 覆寫。

把關：[`lint._example_missing_prompt`](pipeline/lint.py) 對「`derivation` 場的 `source` 指到 handout『Example N.N』卻無 `prompt:`」**warn**（advisory，不擋 build；待全章補齊後可升為 error）。

## 內容分量自適應 ＋ 多頁拆分（2026-06-21）

固定 body zone（≈5u）要容納 1–7 列的內容。原則：**字型保持統一，用「間距帶＋拆分」吸收差異**，
不靠縮字。

- **`place_body` 上偏（Lectern bias，2026-06-21）**：短內容落在 body zone 的**上中段**
  （`_biased_y`，`UPPER_BIAS_FRAC≈0.55`，貼標題），剩餘留白集中底部、由角落 motif 平衡——取代
  原本的死正中對齊（短內容兩端都留大洞、與標題脫節，最顯著於單欄 definition）。高內容仍 top-anchor。
- **`stack_layout`（舒適間距帶）**：`[min_pitch, min_pitch+COMFORT_SPREAD]`，`COMFORT_SPREAD=0.5`
  是 stretch 的**絕對上限**。輕→用 max pitch 置中；中→撐到填滿 zone；重→min pitch 頂錨（交給拆分）。
- **`center_in_zone`**：把 procedure/theorem/recap 那種「固定高錨點擺」的內容群組 shift 到 zone
  上中段（同 `_biased_y` 的 Lectern bias；procedure 用 `extra_bottom` 預留底部 worked strip；
  theorem 卡片留頂、只置中 proof）。
- **B 拆分偵測（`sizecheck._capacity_issues`）**：對**同質鏈**模板（derivation/definition，宣告
  `MIN_PITCH`）算 `Σ列高+(n−1)·MIN_PITCH > zone_h` → warn「拆 N 頁」。predictive（排版前），補上
  derivation 的 place_body clamp 會藏溢出、反應式 off-frame 抓不到的盲點。異質模板（theorem/
  procedure/recap，gap 不一）不宣告 `MIN_PITCH`，靠反應式 off-frame。
- **C 多頁機制**：偵測自動、**切點手動**（作者把長場景拆成數個 scene、每頁重貼 header、設
  `part: {current, total}`）。`part` 指示（accent 色、右上）通用化到 `scene_head`／`example_head`；
  續頁 example 標 `SOLUTION (CONT.)`。不全自動切——`{show}` 旁白逐場景手寫，自動切會破壞音畫對齊。
  fixture：[`storyboards/_demo_multipage.yml`](storyboards/_demo_multipage.yml)。

**definition 單欄（退兩欄，2026-06-21）**：definition 的散文與符號**非逐列配對**，兩欄只會把一行
寫得下的句子硬拆兩行 → 改回單欄滿寬 prose ＋ 符號式 ＋ place_body 上偏置放。兩欄/rail 保留給有真逐列
配對的 derivation/procedure/recap（見上節 Lectern「版面 = 內容結構」）。

## 模板視覺修正（2026-06-21 第二輪：上偏／對比／序號／rail）

承上版面與單欄修正，對 render 後逐幀盤點出的視覺缺陷做外科手術式修正——每項改前後逐幀比對、
全 19 場景回歸無誤、schema/lint/sizecheck 0 error（離線 `save_last_frame` 抽幀驗證，不計費）：

- **A1 版面上偏**：見上「短內容的下半留白」與「內容分量自適應」的 `UPPER_BIAS_FRAC`／`_biased_y`。
  最顯著受益者是單欄 definition（短內容原本死正中浮空、與標題脫節）。
- **A2 derivation 對比**（[`pipeline/templates/derivation.py`](pipeline/templates/derivation.py)）：
  ① check 列的式子由 `role="muted"`→`"primary"`——驗證列是「通過」不是「被劃掉」，原 ink_3 讀起來像停用。
  ② check 的綠 ✓ 取消 `scale(0.8)`、改全 math size＋綠 `text_glow`，當明確判定標記（標 `mark: ok/bad`
  的步驟同步放大）。③ reason 欄統一**正體**——含 `$` 的 reason 走 `prose()` 本就正體，純文字 reason
  原寫死 `slant=ITALIC`，同欄正/斜體混用不一致。
- **A3 序號語彙一致**（[`pipeline/templates/recap_cards.py`](pipeline/templates/recap_cards.py)）：recap 點序號
  由「小 mono eyebrow amber＋多餘圓點」改為 **display serif＋accent＋soft glow**，與 procedure 的發光序號
  同語彙，僅尺寸隨結構角色縮小（列表標記 `h3` vs 步驟錨點 `numeral`）；序號取代圓點（一個標記，不重複）。
  `pt_gap` 維持 0.42——4 列點欄距放大會讓末列溢出底部 safe margin（sizecheck 抓到、已收回）。
- **B2 procedure rail leader**（[`pipeline/templates/procedure_steps.py`](pipeline/templates/procedure_steps.py)）：
  每個步驟↔右側結果式之間加細點 dotted leader（同 derivation reason rail），消除「右式脫節浮在右邊」感；
  步驟文字逼近 rail 時跳過。
- **B3 recap 卡片加重**（`recap_cards.py`）：REMEMBER 公式卡 pad 0.36→0.46、pad_x 0.5→0.62、bar 5→6px、
  fill `bg_soft`→`panel`，與左欄等重（原本偏小偏弱）。

**B1（definition 退單欄）早於本輪已在程式碼完成**，本輪僅重渲驗證（`output/_lectern/full` 那張兩欄是
比程式碼舊的 stale render，勿據以重提）。

## P5 圖凸顯／P6 次要文字可讀（first-learner 框架；SPEC §8，現已 ENFORCED）

兩條 first-learner 視覺原則經 Plan 4 落地，**現由視覺閘量測／工程層 clamp 強制**（非僅 authoring 建議）。
權威 spec＝[`SPEC-pedagogy-firstlearner-framework.md`](SPEC-pedagogy-firstlearner-framework.md) §8；判斷層 rubric＝
[`content_scripts/_audit/VISUAL-FRAME-RUBRIC.md`](content_scripts/_audit/VISUAL-FRAME-RUBRIC.md)。原則：**sharpen 既有 V/A 維，不立新
V/A code**。

- **P5 圖凸顯（figure-prominence）：** 核心是幾何直覺的場（hook／graph），圖應**主導畫面**。凸顯維持靠
  `x_length`／`y_length` 放大圖、**不引入 magic boolean**（不加 `figure_focus: true`）；由視覺閘 `A7`
  （hierarchy／focus）**量測**圖佔幀比例判定，低於門檻扣分（advisory magnitude，非 blocking）。
- **P6 次要文字可讀（min-size floor ＋ mobile）：** reason-rail／註解有最小可讀字級
  **`MIN_FONT_FLOOR = 26px`**（[`pipeline/visuals/theme.py`](pipeline/visuals/theme.py)，校在最小**刻意**命名尺寸
  eyebrow=26）。render-time **clamp**（[`brand._clamp_shrink`](pipeline/brand.py)）把單行縮到合寬、但**永不低於
  floor**——到 floor 就停、改 wrap／overflow（封住既有 single-line `scale_to_fit_width` 縮穿 floor 的盲點）。
  build 前另有 **warn-default check**（[`pipeline/sizecheck.py`](pipeline/sizecheck.py) `_floor_issues`，opt-in
  `meta.fontfloor_enforce` 才升 error）浮現過小文字。判斷層：承載值小到不可讀 → `V4`（blocking）；小但可辨
  → `A6` 扣分，並補一條「以手機寬度檢核次要文字」的尺標。

## 內容分量變異：容量契約三層架構（2026-06-21 設計拍板）

**這是讓「同一套模板套用到之後所有章節」成立的權威契約。** 問題：同一個模板在不同章節被餵進來的
文字量／數學量天差地別（同模板實測 2–3.4× 變異是常規），模板必須優雅吸收而不爆版、不留死洞、
不犧牲跨場景一致。經一輪設計探索（並行盤點現有機制＋逐模板壓測＋五策略評審團＋收斂）拍板如下。

**統御原則：** 字級恆定不可協商；分量變異由**「一條容量公式同時驅動『放置』與『稽核』」**吸收——
輕則上偏、中則撐滿、密則拆頁、稀疏則投放可選 enrichment。放置端（`stack_layout`）與稽核端
（`sizecheck._capacity_issues`）今天**各寫一份高度公式**會漂移；統一到單一 `capacity_meta` +
`classify_regime` 是骨幹。**明確否決 auto-fit 縮字**——它把字級不一致從「場景內」（被 sizecheck sibling
檢查抓）搬到「無人看守的場景間」；`brand.py` 既有的單行 width-fit（title/equation over-width
`scale_to_fit_width`）保留，body height-fit 路徑不落地。

**六條正交變異軸**（前四＝縱向溢出側、第五＝橫向、第六＝稀疏側）：V1 列數、V2 列高、V3 行寬→換行
行數、V4 雙流不平衡、V5 橫向過寬、V6 稀疏死區。現況守門幾乎只覆蓋 V1–V4 的**同質鏈**（宣告
`MIN_PITCH` 的 derivation/definition）；異質模板（procedure/theorem/recap/callout）退反應式 off-frame。

**三層方案（多為既有機制小擴充）：**

| 層 | 做什麼 | 軸 | 性質 |
|---|---|---|---|
| **L1 容量契約** | 每縱向模板宣告 `capacity_meta(spec)→list[ColumnPlan]`（`row_heights, min_pitch, extra_bottom, x_bucket`）；`stack_layout` 的 LIGHT/FIT/OVERFLOW 三分支抽成共用 `classify_regime()` | V1/V2/V4 | 骨幹，多為重構 |
| **L2 預測式拆分守門** | `sizecheck._capacity_issues` 把 `getattr(mod,"MIN_PITCH")` 換成先讀 `capacity_meta`（保留舊分支相容），**自動覆蓋 theorem/procedure/recap/callout** | V1 溢出 | 小擴充、關掉最大缺口 |
| **L3 稀疏出口** | 可選 `aside` 欄（key-idea 卡/mini-example），snap 既有 `RAIL_X`、用 `accent_panel`、`layer="decoration"` 豁免檢查；primary 密集時 silently 收合 | V6 | 純加法 opt-in |
| ~~auto-fit~~ | **否決**（理由見統御原則） | — | 不落地 |

**四 regime 是一條連續決策**（由 `r = natural_min/zone_h` 驅動），不是離散斷點——regime 內仍跑既有
連續吸收（`_biased_y` 上偏、`stack_layout` 三分支），只有「投不投 aside／警不警告拆頁」是離散開關。

**三項拍板決策（2026-06-21，使用者裁決）：**
1. **L2 異質列高＝估算＋保守 buffer**（不二次 build）：用 `brand.estimate_text_width` 估換行行數×列高，
   ±2–5% 誤差靠保守 buffer 吸收。因 L2 是 **warn** 不是 error，估偏只讓拆頁建議稍鬆/緊、不誤殺；
   避免「稽核期 double-build」的第三種狀態維護風險。
2. **超量＝warn 不 hard error**：同模板 2–3.4× 變異是常規真實壓力，硬 error 會誤殺合法稿、且與
   Mode A「prefer richness、不自我審查」衝突。warn 給作者判斷權（拆 `part:` 或精簡），不替他決定內容。
3. **regime＝連續內插**：沿用 `stack_layout` 既有連續三分支，無跨場景 cliff、無斷點抖動。

**逐 family 套用：** definition＝L1（零行為改變）＋**L3 主受益**；derivation＝L1＋L2（純鏈置中例外保留、
不開 L3，RAIL 被 reason 佔）；procedure/recap＝**L1＋L2 核心受益**（反應式→預測式）；theorem＝L1＋L2＋
**L3（僅 statement-only 命題：無 proof 時 card 收窄＋rail aside 兩欄；有 proof 則 aside 收合）**；
value_table＝**L2 `model="group"`**（置中 figure，量合併群組高，2026-06-21 擴充）；sign_chart／graph＝
**維持反應式**（sign_chart 數線在 `layer="graph"`、group 跨度量不到頂；graph 真非線性；靠 `_overflow_issues`／
`_graph_label_overlap_issues`）；callout＝反應式（置中單面板、無 masthead zone）。

**作者契約：** payload 陣列長度＋prose 換行行數共同決定容量；超量是 authoring 決策（拆/精簡），
永不靠縮字救；sizecheck 在排版前（純預測、不需 render）對所有縱向模板給「拆 ~N 頁」warn。

**分期落地（每步有驗證閘）：** ① `classify_regime` 抽函式＋同質模板 `capacity_meta`（**零行為改變**，
驗收＝既有 storyboard render **pixel 等價**）**【已完成 2026-06-21：`_common.ColumnPlan`/`classify_regime`、
derivation/definition `capacity_meta`、`sizecheck._capacity_issues` 優先讀 `capacity_meta`（回退 `MIN_PITCH`）；
§1.1 全 19 場景 render MD5 逐檔相同、sizecheck 行為保持（`_demo_multipage` 溢出仍報「拆 ~2 頁」）】**
→ ② `sizecheck` 換源＋異質模板 `capacity_meta`
**【已完成 2026-06-21：procedure/theorem/recap 各加 `capacity_meta`（`model="span"`）；§1.1 render 19/19 MD5 相同、
合法內容零誤報、derivation/definition 不變、超量異質場景正確 warn（recap 7 點 ~17u、procedure 6 步 ~8u、
theorem 5 步 ~7.6u），`_demo_tall_rows::proof_tall` 邊界 warn 與反應式 spill 互相佐證】**
→ ③ 容量回歸網 **【已完成 2026-06-21：[`storyboards/_demo_capacity.yml`](storyboards/_demo_capacity.yml)
每模板 fit+over 各一場景（含 value_table）＋ [`video/capacity_selftest.py`](capacity_selftest.py) 斷言 EXPECT 表，
12/12 通過；本地跑（需 manim、非 handout CI），改模板若破壞容量預測即紅】**
→ ④ L3 enrichment slot **【已完成 2026-06-21：`_common.build_aside`（rail 卡片）＋ `definition_math` 的可選
`aside` 欄（稀疏→兩欄 primary＋rail key-idea 卡、密集→自動收合回滿寬單欄）；§1.1 render 19/19 MD5 相同、
無 aside 路徑逐位元保持；fixture [`storyboards/_demo_aside.yml`](storyboards/_demo_aside.yml)】**。
figure 三模板與 **callout（置中單面板、無 masthead zone）不加 `capacity_meta`**。grounding 與五策略全文見
2026-06-21 workflow 紀錄（task wgpvk07nd）。

**`aside` 欄位契約（L3）：** 可選 `aside`：`{label?, body, accent?}`（或裸 body 字串），`build_aside` 走
`accent_panel`、`layer="decoration"` 豁免容量/overlap 檢查。**`definition_math`**：有 `aside` 時 primary 收窄
到 `PRIMARY_W`、卡片 snap `RAIL_X`；primary 收窄後若會溢出 zone 或某 math 列寬過 `PRIMARY_W` 則**自動收合**
（丟 aside、回滿寬單欄）。**`theorem_proof`（2026-06-21 擴充）**：僅 statement-only 命題（無 `proof`／`qed`）吃
aside——card 收窄＋rail aside、兩者置中（Lectern bias）；有 proof 時 aside 收合（proof 即內容）。**`callout`
不開 aside**——它本身就是置中單一 boxed aside、無 masthead/rail，再塞 rail aside 自相矛盾。**author-authored、
純可選——框架絕不自動生成內容填空**（否則退化成被否決的 auto-fit 投機）。

**callout 改版（2026-06-29，使用者要求「不要卡片式、改成文字在下方敘述、可條列」）：** `callout` 從
「置中卡片＋glyph box（accent_panel）」改為與 `definition_math` 同型的 masthead 教學幀——`scene_head`
（eyebrow `[ TYPE n.n ]`＋title）＋body 左齊置於標題下方（`place_body` 上偏置中）。type 訊號改由顏色
（eyebrow／spine cap／條列圓點）＋eyebrow 字承載，不再用 box；於 `build` 開頭設 `spec["accent"]=type`
（`ACCENT_ROLE` 已有 caution→warning／remark→secondary／note→accent），讓本模板 `scene_head` 與
**中央 `scene_spine`**（`templates.build_blocks` 後加）同時上正確顏色（修掉先前 caution spine cap 誤為藍的
bug）。`body` 為 list 時逐項以「同色小圓點＋散文」條列（單一 `Block("body")`，`{show body}` 旁白 cue 不變）。
新增 `capacity_meta`（`model="span"`，同 definition）納入 L2 預測式拆分守門；仍不開 aside（body 即內容）。
**本次取代上文 2026-06-21 段落中所有「callout＝反應式／置中單面板／無 masthead zone／不加 `capacity_meta`」
之敘述**（該段保留為歷史決策紀錄，不回改）。

**取捨 A 的正向偏離（2026-06-21，實作時發現）：** 拍板時假設 L2 異質列高要「估算+保守 buffer」（V3 風險）。
但因 L2 是**擴展既有 build-based 的 `_capacity_issues`**（它本就 build 完量測，非 YAML-only 估算），且
固定節奏模板改用 **span 模型直接量實際 render 跨度**（`ColumnPlan.model="span"`：`max(top)−min(bottom)`，
非 `Σh+(n-1)·pitch`），**列高是「量到的」不是「估的」——V3 估算根本不發生**，比拍板假設更準。緣由：固定
節奏模板的 `Σh+pitch` 會誤模其 center-to-center 節奏（重複計入中間列高），span 量測才正確。

**模型分類（哪些 span、哪些 stack）：** 只有**真彈性**（用 `fill_gap` 撐開填滿、build 後位置不反映最緊排法）
的模板用 `stack`（tightest-pitch 估算）——目前**僅 `derivation`**。**固定節奏**（fixed buff＋`place_body`/
`center_in_zone` 只定位、不撐開）的全用 `span`：procedure/theorem/recap **以及 `definition_math`**。
（`definition_math` 原在 Step ① 暫歸 stack，Step ④ 的 `aside_collapse` 測試揭示它其實固定節奏——stack 用
`MIN_PITCH` 估那個 0.71 的 statement→math gap 會低估 ~0.35u、漏抓密集 definition 的溢出——已改 span。）

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

### Authoring Playbook：內容形狀 → 模板 → 單頁容量預算 → 超量／稀疏動作（2026-07-05 拍板）

寫 storyboard 時對照選模板、預估分頁；寫完跑 schema→lint→sizecheck→mock render→visual gate 即收斂。
預算與 `_demo_capacity.yml`／`capacity_selftest.py` 的 fit/over EXPECT 對齊，fixture 調整需同步本表。

| 內容形狀 | 模板 | 單頁容量預算 | 超量動作（DENSE） | 稀疏動作（SPARSE） |
|---|---|---|---|---|
| 連續推導鏈 | `derivation` | fraction 列：無 statement ~5、有 statement ~4；single 列 ~7 | 按邏輯階段切 `part:`，不硬切等號 | fill_gap 自動；勿加廢列 |
| 陳述＋符號式 | `definition_math` | statement ≤3 行＋math ≤4 列 | 拆 part 或把長鏈改 derivation 景 | 掛 `aside` 卡（L3） |
| 命題＋證明 | `theorem_proof` | proof ≤4 步＋qed（一般步 2–3；fraction 步更保守） | >4 步拆 statement＋proof 兩場、超頁 `part:` | statement-only 走 card＋aside 兩欄 |
| 離散步驟 | `procedure_steps` | 3–4 步、math ≤5u 寬 | 拆 part；長式改 derivation | ——（步驟自然 ≥3） |
| 單句警示／評註 | `callout` | 條列 2–4 點或段落 ≥3 行 | 條列砍到 ≤4 點 | G3 三出口：條列化／併景／`sparse_ok` |
| 函數圖／幾何圖 | `graph` | 圖主導：x 以 8.0u 起手、y 交 `_fit_graph_to_safe_zone` 封頂；有 caption band 時被自動縮回是預期行為；A7 量測為最終裁判；標籤走 carrier≥刻度＋亮度地板 | 拆 reveal beats（`{show plot.N}`） | 放大圖填版（P5 正向） |
| 數值對照 | `value_table` | ~5×3 格 | 砍列（教學點優先） | —— |
| 正負號分析 | `sign_chart` | 1 軸＋≤4 區 | —— | —— |
| 總結要點 | `recap_cards` | 4–5 點 | 砍點（recap 不拆頁） | —— |
| 章節轉場 | `divider` | title＋hook 式（56px）＋一句 subtitle | —— | —— |

**G3 稀疏出口（單塊 prose 場景）：** callout（字串 body）／definition_math（statement-only）實測佔 body zone
<35% 時 sizecheck advisory 提示三出口——① 條列化（callout body 用 list 形式）；② 併景（掛相鄰場景
`scaffold.flag`／`aside`）；③ `sparse_ok: true` 接受留白（pull-quote 式刻意孤句合法；render 不讀此欄位，
僅 sizecheck 讀＝advisory ack，非 magic boolean）。

**G4 卡片孤字：** aside／rail statement 的 prose 尾端孤 math token（frame 07 的孤 `$x_0$`）由 lint advisory
提示，修法＝改寫文案（如 `at every point $x_0$.`）。**不用 `~`**——`brand._escape_tex` 會把它印成可見波浪號。

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
- **`graph` 的 plot 預設是 static 的**（整張圖從 frame 1 就在螢幕上）。
  將 plot entry 標記 `reveal: true` 使其等待 `{show plot.N}`——教學順序
  （curve first、*然後* ε-band、*然後* δ-band）變成 `say` 中的 beat 決策，
  不需要 hook。Revealed plot 的 `label` 折入同一個 block，因此一個 marker 同時
  帶出元素和它的名稱。Demo：`storyboards/_demo_graph_reveal.yml`。
- `say` 中的 LaTeX 是正典寫法（mock 與閱讀版直接用）。**真旁白走 MiMo**，由
  `<deck>.spoken.yml` 把數學攤成口語（見下方「MiMo 口語軌」）；若某短語以特定
  方式朗讀更好，就在 `.spoken.yml` 中如此撰寫。

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

**Route A（2026-06-24 落地）：所有螢幕文字都走 LaTeX/pdflatex** 以拿到正確 kerning——內文/標題 **IBM Plex Sans**、eyebrow **IBM Plex Mono**、數學 **Latin Modern**。根因：實測 manim `Text`/`MarkupText`（Pango）完全不套 kerning（`W("AVAVAV")`≈各字寬相加），sans 尤其鬆；LaTeX 會 kerning。字體在 TeX preamble 設定（`_bootstrap.apply_tex_template`：`plex-sans`＋`plex-mono`＋`lmodern`＋`microtype`，`familydefault=\sfdefault`，`\everymath{\displaystyle}`），所以本模組不再出現任何 Pango family 名。硬約束：只能 pdflatex（lualatex/xelatex 會破壞 manim 的 `\special{dvisvgm:raw}` 數學子部件定址）。計畫見 [`content_scripts/_audit/PLAN-routeA-plex-latex.md`](content_scripts/_audit/PLAN-routeA-plex-latex.md)。

> **每景重套 template（坑）：** manim 的 `tempconfig`（`make.py`／`scratch_frames` 每景 `with tempconfig(cfg): LessonScene().render()`）退出時會把 `config.tex_template` 重設回預設（serif CM、缺 `\sfdefault` 與 `\arccsc` 等），所以 `LessonScene.construct()` 在 build 前都呼叫 `_bootstrap.apply_tex_template()` 重套，否則一個 batch 只有第一景拿到 Plex。

螢幕文字現在全走 LaTeX（`Tex`／`MathTex`），按角色分：

| 角色 | 函式 | 字體 | LaTeX |
|---|---|---|---|
| 標題 | `brand.heading` / `brand.heading_rich` | Plex Sans Bold | `\textbf{…}` |
| 內文 prose | `brand.body_text` / `brand.prose` | Plex Sans | text-mode（含 `$math$`） |
| eyebrow / label | `brand.eyebrow` | Plex Mono | `\texttt{…}` |
| 數學 | `brand.math_line` / `MathTex` | Latin Modern | math-mode |

`Tex` 在 text mode 原生排「文字＋內聯 `$math$` 同行」、baseline 正確、kerned，所以**舊的 Pango↔Tex 拼接機制已全部移除**：`theme.TEX_TEXT_SCALE`（Pango↔Tex 尺寸對齊，今 = 1.0 no-op）、`brand._pango_dashes`、`brand._compose`／`_prose_mixed`（手動 baseline 拼接）。換行寬度估計 `_WIDTH_K`／`estimate_text_width` 與 kerning 無關，保留並已重校為 Plex-LaTeX。

**規則（template 必須遵循）：** 作者可能放入 `$` 或 `\` 的任何欄位——`title`、
`statement`、step `text`、`takeaway`、recap `points`——透過 **`brand.prose`**
（body prose）或 **`brand.heading_rich`**（title）render。這是 markup routing
的唯一決策點：有 markup → Tex text-mode，否則 → `body_text`（也是 Tex，為了
kerning）。永遠不要在 author prose 欄位上直接呼叫 `heading`。純 math 欄位
（`math`、`formulas`、`proof`、`worked`）走 `brand.math_line`。

**Display-style 慣例（2026-06-29）。** Preamble 設定 `\everymath{\displaystyle}`，
使所有 `$...$` inline math 自動以 display style 渲染（大分數、`\lim` 下標在
正下方）。此外 `brand.math_line` 與 `brand.prose` 在偵測到「整串只有一組
`$...$` 包裹的純數學」時，會剝掉 `$` 改走 `MathTex`（display mode）。搭配的
**storyboard 分數慣例**：

| 位置 | 用 | 效果 |
|---|---|---|
| display 欄位（`statement` / `math` / `proof` / `formulas`） | `\frac` | display-size 大分數 |
| inline 位置（`title`・`prompt`・`body`（callout）・`points[]`（recap）・`scaffold.motive`・`reason`（含 `steps[].reason`）・`say`・table cell・axis label） | `\tfrac`／slash form／inline `\lim` | 顯式覆蓋回 text-size；display 級分數與堆疊上下標只進 display 欄位 |

`\tfrac` 不受 `\everymath{\displaystyle}` 影響（它顯式指定 text style），所以
兩者能共存：display 位置自動大，inline 位置顯式小。

**G1 執法（2026-07-05）：** 上表由 `pipeline/lint.py` 的 `_display_math_in_inline` advisory 靜態執法
（掃 inline 欄位 `$...$` 內的 `\frac`/`\dfrac`/`\lim_`/`\sum_`/`\int_`）。display 欄位
（`statement`/`math`/`proof`/`formulas`/`scaffold.problem`）**不掃**。罕例真要 display 可無視 warn。

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

### 型階與量測表（2026-07-05 體檢存檔）

**型階承載表**（`theme._SCALE_PX`，px＠1920×1080；由大到小）：

| 型階 | px | 用途 |
|---|---|---|
| hero | 112 | 無 call site 保留 |
| divider | 92 | divider title（`heading_rich size="intro_headline"`；2026-07-05 由 raw 92 掛回 token。outro title 亦由 raw 72 → `outro_headline`=78） |
| h1 | 78 | 一級標題 |
| h2 | 58 | 二級標題 |
| result | 54 | derivation result line |
| math | 48 | display 數學 |
| h3 | 44 | 三級標題（example prompt） |
| statement | 44 | **命題/定義/value_table/sign_chart 的 `statement`**（2026-07-05 統一 raw-px 落單；原散落 h3=44／prose=42／raw 40） |
| prose / step | 42 | 內文、離散步驟文字、value_table 內文 cell |
| math_sm | 40 | 刻度／軸名（graph carrier label 現已升為 math_sm） |
| prose_sm | 35 | reason rail／aside／divider 副標／value_table 表頭（2026-07-05 收 raw 40／38 落單） |
| tag | 30 | derivation result-reason、part pager |
| eyebrow | 26 | floor（`MIN_FONT_FLOOR`） |

**數學三路徑表**：

| 路徑 | 公式 | 說明 |
|---|---|---|
| `MathTex`（display） | `px × PX_TO_FS(0.698)` | 基準：math-anchored 換算 |
| inline-in-prose | 同基準 `× TEXT_SCALE(1.3102)` ＝ **+31%** | `brand.prose` 中的 inline `$...$` |
| inline-in-heading | 同基準 `× HEADING_MATH_SCALE(1.0)` | 標題中的 inline `$...$`，無額外放大 |

Divider hook 案例：`divider` 的 **title 走 92px**（heading 路徑）；其 optional `scaffold.problem`（hook 式問句，P-A3）走 **56px raw px**——純 `$math$` 因此走 `MathTex` display 路徑（不吃 `TEXT_SCALE`），讀來高於 subtitle 而非其 ~80%（見上方 Authoring Playbook「章節轉場」列）。

**縱向節奏 token 表**（有壓測紀錄、不重構）：

| Token | 值 | 用途 |
|---|---|---|
| `EYEBROW_GAP` | 22 | eyebrow → title 間距 |
| `TITLE_GAP` | 56 | title → body 間距 |
| `LINE_GAP` | 28 | 同段內行距 |
| `ROW_GAP` | 44 | 跨列間距 |
| derivation pitch | 54 | chain line 節奏 |
| definition pitch | 48.6 ／ 95.9 | statement／math 節奏 |
| theorem pitch | 67.5 | proof step 節奏 |
| procedure pitch | row_gap 1.4 / min_clear 0.35 / title_clear 0.2u | `procedure_steps.py` 設計 rhythm |
| recap pitch | 47 | recap card 節奏 |

**行長量測法：** 權威＝`brand._WIDTH_K = 0.00507`（＋CJK 字元 ×2 加權）；
`CONTENT_W ≈ 65` 加權字元＝可讀上緣。**勿再用 0.5em 粗估**——`_WIDTH_K` 已為
Plex-LaTeX kerning 重新校正，粗估法未計入 kerning 與 CJK 加權，會系統性低估
真實跨度。

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
| 在低填充幀只放證明骨架；把 >4 步證明壓成 2–3 行 | proof >4 步拆 statement＋proof 場、超頁走 `part:`、一步一 beat（每承載步驟一個 `{show}`） | detail over compression（[`CONTENT_METHODOLOGY.md`](CONTENT_METHODOLOGY.md) §1）；ch03 §3.1 第一版壓縮漂移學費（2026-06-29 密度稽核 `content_scripts/_audit/REVIEW-ch03-s31-density-audit.html`） |
| 在 `derivation` 的 `result`/`check` 的 `reason` 放 `$math$` | result/check 的 reason 用純文字（要顯示的 math 放進 `result.math`／`check.math` 本體） | result/check reason 走 `texttt`（大寫 mono、不處理 `$…$`）→ 印出 raw LaTeX garble；只有 step 的 `reason` 吃 math（2026-06-29 ch03 §3.1 detail-redo 學費，visual-frame V4） |
| scaffold 的 `motive`／`problem`／`flag` 用 `muted` role | `text`／`primary` role（de-emphasis 靠字級／位置，非調暗） | 太淡＋違反「教學內容非 muted」；prose 上 **sizecheck warn**（first-learner scaffold 承載） |
| `theorem_proof`／`derivation` 場缺 `scaffold.motive`（PD2「為什麼做這個」上畫面） | 加一句 `scaffold.motive` | **pedagogy warn**（opt-in `meta.pedagogy_enforce` 才升 error）；definition_math 必填與否＝gate-1 advisory |
| `kind: divider` 場缺 `scaffold.problem`（PD3 講具體式、非概念標題） | 加 `scaffold.problem` 公式塊 | **pedagogy warn**（opt-in 才 error）；intro／recap 依 kind／template 本就排除 |
| `meta.assumptions[]` 有 entry 卻在 `first_use_unit` 沒對應 `scaffold.flag`，或有孤兒 `scaffold.flag`（PD4 前提首用即標） | 每筆 assumption ⇄ 其 `first_use_unit` 的 `flag` 一一對應，無孤兒 | **pedagogy warn**（registry 一致性，opt-in 才 error） |
| 上畫面教學文字（含 scaffold）無 provenance ref（OTF 可回溯） | 帶場級 `ref:`，例外欄位用 `refs:` flat-map 覆寫（key＝欄位路徑字串） | **provenance warn**（opt-in `meta.otf_enforce` 才 error）；規則見 [`CONTENT_METHODOLOGY.md`](CONTENT_METHODOLOGY.md) |
| proof／derivation 場的 storyboard 漏掉 `.md screen_contract.required_steps` 宣告的承重步驟（SC1，**可合併不可掉**）；或場級 `covers:` 宣告了畫面 payload 沒有的步驟（SC-honesty） | 場級 `covers: [id…]` 聯集蓋滿該單元承重步驟（一 reveal 可蓋多 id＝合併／重排）；掉步驟就補上畫面，`recap_required` 的 cash-in 步驟要在地重述（SC2） | **coverage warn**（opt-in `meta.coverage_enforce` 才 error）；把上方「>4 步壓成 2–3 行」從人工 checklist 升級為確定性閘；細節 [`CONTENT_METHODOLOGY.md`](CONTENT_METHODOLOGY.md) `screen_contract` 節 |
| exposition beat（`motivation`／`intuition`／`bridge`／`forward-ref`）用 `definition_math`／`value_table` 卻不設 `scene_role` | 設 `scene_role: <beat>`（→ 無字卡）；只有真形式物件（definition/theorem/…）才戴字卡 | 否則靜默沿用 `accent` 的預設字卡（如 `[ DEFINITION ]`）＝把形式標籤套在講解 beat（2026-07-01 字卡 resolver 學費，見 §Eyebrow 字卡 resolver）。**注意：lint 抓不到「漏設」**（無法偵測 beat role）→ 純靠此 checklist；完全強制須待 L3 把 `scene_role` 設必填 |

---

### Visual QA——全影片驗收通過

上方的 authoring checklist 靜態地抓*已知的 per-element 錯誤*。以下是其補充：
一個**成品影片通過**（或其 key frame），在一節出貨前端到端觀看。維度
改編自 Code2Video 的 AES rubric；在該研究中 aesthetic score 與測量的 learning
gain 相關 **r ≈ 0.97**，因此 visual clarity 就是 teaching efficacy，不是 polish。

> **權威更新（2026-06-16）：** 視覺稽核的 SSOT 已收斂到
> [`content_scripts/_audit/VISUAL-FRAME-RUBRIC.md`](content_scripts/_audit/VISUAL-FRAME-RUBRIC.md)——兩層
> **V1–V9 blocking（收斂＝視覺 blocking==0）＋A1–A7 magnitude（0–100，驅動重 render 優先序）**。
> 下表這五維即 **A1–A5 的來源**（A6 typography/wrapping、A7 hierarchy/focus 為增補）。gate 1（Claude 抽幀
> subagent）與 gate 2（`critic.py`／MiMo，已 runtime verbatim-inject 該 rubric）共讀它；本表保留作 A 維出處與 authoring 參考。

| 維度 | 本產線的具體檢查 |
|---|---|
| **Element Layout** | 沒有兩個 content block 重疊（現由 `sizecheck._overlap_issues` 自動抓到）；一切都在 `SAFE_MARGIN` 內；graph label 不可壓在線、點、空心點或其他圖形標記上（例如 `$y=f(x)$` 貼在線段上即為 finding）；frame 讀起來平衡、不歪斜。 |
| **Attractiveness** | 每個 animation 都值得存在——它*animate*一個概念（sweep、trace、reflection across `y=x`），不只是 static slide reveal（methodology §5, "Animate, not just display"）。 |
| **Logic Flow** | Reveal 順序追蹤 narration beat；每場景一個教學概念；narration 說到之前，螢幕上什麼都不該出現。 |
| **Visual Consistency** | Accent role 一致（definition = cyan、theorem = gold、example = electric blue、…）；全片一套 font 和 size scale；intro 和 outro 匹配 brand bookend。 |
| **Accuracy & Depth** | 忠實於 handout，數學正確，且每場景的 `learning_goal`（content script，methodology §6）確實被 deliver——在螢幕上*且*在 narration 中。 |

此通過由 **VLM critic（視覺 gate 2）**（`pipeline/critic.py`）執行：
它提取每場景的 fullest frame，讓 vision model（MiMo-V2.5）對照 **VISUAL-FRAME-RUBRIC（V1–V9 blocking＋A1–A7）**
判定並列出具體缺陷。它是 **advisory**——它寫 report
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
   ├─ schema.py            結構驗證（meta/scene kind/id 唯一/{show} 不閉合）       (DONE)
   │                       ＋列舉 reveal 目標；make.py 中最先跑（schema→lint→sizecheck）
   ▼
narration.parse_say        將每個 `say` 在 {show} marker 處拆成 beat              (DONE)
   │                        → 每場景的 ordered (beat_text, reveal_target) list
   ▼
synth                      每個 beat 一個 clip；mock = 依 word count 的靜音        (DONE)
   │                        （billed MiMo = pipeline/tts.py --backend mimo）；測量
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
pre-render 的 `schema.py` / `lint.py` / `sizecheck.py` guard。它是 **offline only**：
mock synthesis（依 word count 的 silent clip），不計費。Real MiMo TTS 是外部 API、
需逐次同意（見 CLAUDE.md），刻意**不**接入 make.py 的 synth；narrated master 走
`pipeline/tts.py --backend mimo` → `make.py --reuse-audio`（後者直接讀 tts.py 的真
manifest render）。（gen-2 的 Gemini 直鏈 `build.py`／`mux.py` 已於 2026-06-16 刪除、
Gemini 路線退場。）以 visual payload 為 key 的 per-stage caching（編輯 `say` 重新
synthesize audio 但不重新 render Manim）仍為 (TODO)。

### Alignment，重述（避免在重寫中遺失）

第一代的洞見沿用：alignment **不依賴** TTS 回傳 word-level timestamp。我們
**每個 beat 合成一個 clip**，測量其真實 duration，該 duration *就是* reveal
hold。換 synthesizer 不換 alignment model（mock→MiMo 只是換了把尺）。（MiMo 回傳
WAV，locally 測量；§1.1 曾 end-to-end 驗證——每個 reveal 落在其 narration beat
的 ~1 frame 之內。）

同步相關常數集中在 `pipeline/timing.py`：`SCENE_LEAD_SECONDS` 是 scene 開頭
等待與 mux/critic offset 的單一來源，`SCENE_TAIL_SECONDS` 是 content scene
收尾等待。`make.py --reuse-audio` 會在 render 前驗 manifest freshness（deck id、
scene、beat count、`{show}` target、`text_hash`、WAV 存在與時長），避免 MiMo
舊 take 被靜默沿用；render 前會警告短 beat / reveal-only beat，render 後用 ffprobe
檢查 content scene video duration 至少覆蓋 `lead + narration`，並回報相對
`lead + narration + tail` 的偏差。

### MiMo 口語軌（single-source）＋非決定性（2026-06-14）

MiMo（`mimo-v2.5-tts`，唯一 TTS 路線）不讀 inline LaTeX，需「數學攤成口語」的旁白。
唯一源＝`content_scripts/<deck>.spoken.yml`（口語＋`{show}`）；`pipeline/derive_spoken.py`
由它＋正典 storyboard 生成 `storyboards/<deck>_mimo.yml`（`say` := spoken、`meta.id` 加
`_mimo`、`voice` Dean）＋`content_scripts/<deck>_narration_spoken.md`（閱讀視圖，`{show}` 移除），
且 `--check` 守 parity（scene/`{show}` 結構與正典一致、口語無 `$`）杜絕兩軌 drift。

對齊模型同上（每 beat 一 clip、量 duration 驅動 reveal）；`MimoTTSBackend`（`tts.py`，OpenAI
相容、urllib、雙 header、比照 `critic.py`）預設**裁 beat 頭尾靜音**（`audio.trim_silence`，留 0.08s），
並在 manifest 記錄 raw/trimmed/cut 秒數，方便 debug padding。真音訊 render 走
`make.py --reuse-audio`（讀 `tts.py` 的 manifest、不重 synth；非 reuse 但偵測到
真 manifest 會拒絕用 mock 覆蓋；reuse 會做 stale manifest 檢查）。**MiMo 非決定性**：同文字重合成＝不同 take、長度 ±~10%，
影片長度不可重現；要定版就別重合成。**NFA（旁白忠實稽核，原 Mode B）** 稽核兩版＋收斂（gate1 Claude→gate2 Codex），契約見 SSOT
`content_scripts/_audit/NARRATION-FAITHFULNESS-RUBRIC.md`、thin prompt `content_scripts/_audit/PROMPT-narration-faithfulness.template.md`（D7「數學內容正確性」維度，未認可章節必跑、開隔離重算 reader）。

### Manifest schema 2：scene-level TTS＋forced alignment（2026-07-05）

設計權威＝`experiments/forced_alignment_dean/REVIEW-scene-tts-production-design.html`；落地紀錄見 `REBUILD_STATUS.md` 同日節。核心：TTS 合成單位可由 beat 升到 content scene，一個 scene 一次合成、用 `stable-ts` transcript-constrained forced alignment 回推每 beat reveal 時序；per-scene validation 決定該 scene 走 scene-level 或回退 beat-level，**永遠有可出片的路**。

- **頂層 `"schema": 2`。** 無 `schema` 欄位的舊 manifest 視為 schema 1（全 beats），照舊可用，**不需遷移**；`make.py` 入口 `_check_manifest_schema` 對 `schema>2` 明確報錯（拒絕靜默誤讀）。
- **`narration_mode` 三值：** `"silent"`（intro/outro/divider）｜`"beats"`（既有，每 beat 一 WAV）｜**`"scene_aligned"`（新）**。同一 manifest 允許混用（per-scene 決定）。
- **`scene_aligned` 條目與 `beats` 模式共用 `beats[]` 形狀**（`index`／`id`／`reveal`／`text`／`text_hash`／`audio_seconds`／`start_seconds`／`end_seconds`），另加 per-beat `word_start`／`word_end`／`boundary{prob,interpolated}`，以及 scene 級 `audio_file`（唯一音檔，無 per-beat WAV）、`scene_text_hash`、`alignment{words_file,aligned_file,aligner{tool,version,model,…},chunks}`、`validation{status,warnings,metrics}`（`status ∈ {pass, pass_with_warnings}`；fail 即回退，不會落進 manifest）、`fallback_history[]`。這使 7 個消費端中 6 處只需把 `narration_mode=="beats"` 放寬為「兩模式皆可」，只有 `make.py._validate_reuse_manifest` 需真正的 `scene_aligned` freshness 分支。
- **兩層獨立 freshness（scene-level 紅利）：** 文字改＝重合成（計費）＋重對位；reveal／beat 數改（文字沒改）＝沿用 WAV、只重跑映射＋驗證（免費）；aligner 換 model／調參＝沿用 WAV、只重對位（免費）；backend／model／voice／style 改＝重合成。判定依 `scene_text_hash`＋per-beat `text_hash`＋top-level 四欄＋WAV 實際時長。`make.py` render 時**不檢查 aligner model**（它沒有 aligner 設定可比；aligner freshness 是 `tts.py` 的職責）。
- **原子寫入＋verify-before-overwrite：** words／aligned／manifest 一律 `.tmp`＋rename（`pipeline/atomicio.py`）；scene WAV 先寫 temp、gates 過才 promote 到正檔，杜絕「舊 words.json 配新 WAV」與「壞 re-synth 蓋掉好 WAV」。
- **模組：** 核心 `pipeline/scene_align.py`（純函式＋單一 aligner seam `align_scene`，換 aligner 只改這函式；另含 `split_sentence_chunks`／`merge_chunk_alignments` 供 rung 3）；fallback ladder `pipeline/scene_fallback.py`；`tts.py --unit beat|scene|auto`（auto 依 template allowlist；**batch-2（2026-07-06）已含全部 content template**）。**ladder＝arbiter(small.en 免費)→resynth(計費 1 call)→chunk(sentence-chunk，N 個 billed sub-synth)→beats(免費終點)**——rung 3 sentence-chunk 於 2026-07-06 batch-2 落地：切句、逐句合成＋對位、concat＋merge 回同一時間軸（`verify_plan_index` 自檢 token tiling）。**計費紀律：chunk fan-out＝N call，故對 `run_ladder` 宣告 `billed=False`、自檢 `RetryBudget`——reserve N、`need > 剩餘 budget` 即 decline 退 beats**；預設 `--fallback-budget 2` 只夠 resynth，chunk 要靠調高 budget（併入報價）才啟用。

---

## Open question／尚未決定

- ~~Template catalog for gen-2~~——resolved 2026-06-11：即上方的 catalog。沿用的
  content template 全部保留；gen-2 新增 `derivation`（2026-06-11），接著
  `value_table` / `graph` / `sign_chart`（依使用者指示提前為 §1.3 /
  ch02 / §4.5 建構——先做 static template，hook 仍為 animation layer）。
- BGM：source、ducking、licensing。
- `{show ...}` target grammar：dotted（`math.0`）vs bracketed（`math[0]`）。目前為 dotted。
- MiMo specifics（唯一 TTS 路線，2026-06-16）：model `mimo-v2.5-tts`（builtin）、voice
  `meta.voice` / `Dean`（voice-design/Calm Professor 已 2026-07-05 退役）、OpenAI 相容 `/chat/completions`（與 `critic.py` 共用
  `MIMO_API_KEY`）；待唸文字放 `assistant`、voice 經 `audio.voice` 選定（builtin 不送 style prompt）；回 WAV，`MimoTTSBackend`
  預設裁 beat 頭尾靜音（留 0.08s）。公測免費、仍屬外部 API（批次前依 CLAUDE.md 徵
  同意）。**非決定性**：同文字每 take ±~10% 長度，定版後勿重合成。（Gemini 路線及
  其 `build.py`／`mux.py` 已於 2026-06-16 退場。）
