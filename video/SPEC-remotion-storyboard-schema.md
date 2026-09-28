# SPEC — Remotion 分鏡 yml 的 schema 與內容層閘（2026-09-28）

> **定位：** 本檔是 Remotion 分鏡（`<片>.yml`）欄位契約的 **SSOT**，也是內容層確定性檢查器接 Remotion 分鏡的接線說明。
> 執行器＝[`pipeline/check_storyboard.py`](pipeline/check_storyboard.py)（結構驗證＋串 provenance／source_rev／pedagogy／step_coverage／example_coverage；
> 零 Manim、零 render、零計費）。閘在審核地圖裡的位置見 [`REVIEW_GATES.md`](REVIEW_GATES.md) 層 6。
> **為何獨立成檔、不併進 `DESIGN.md`：** [`DESIGN.md`](DESIGN.md) 明定只承接「與渲染器無關」的四塊；分鏡 schema 是 Remotion 線的產物契約，
> 且各閘「讀哪些欄位」的對照表會隨 Remotion 場角色欄位的裁決繼續長，比照既有 `SPEC-motion-language.md`／`SPEC-pedagogy-firstlearner-*.md` 獨立成檔，
> `DESIGN.md` 的 `say`／`pauses:` 兩節只指過來。
> **事實來源：** 欄位以 `pipeline/tts.py` 讀得懂的為準（它是 Remotion 分鏡目前唯一的程式消費者；Remotion 本身只讀 tts 寫出的 manifest），
> 現行實例＝`remotion/{s31/s31,q7/q7,q7/q7.zh,act3/act3}.yml`；內容層閘讀的欄位以各檢查器的 selftest 為準。

---

## 1 · 頂層形狀

```yaml
meta:      # 一個 mapping（必填）
  id: q7_billiards        # 必填，非空字串。manifest 的 deck_id；`_mimo` 結尾會啟動 tts.py 的 derive_spoken freshness 閘（只給生成 deck 用）
  title: Square Billiards # 選填，字串
  language: en            # 選填，字串（tts.py 不讀；給人與 Remotion 看）
  voice: Dean             # 選填，字串；tts.py 的 MiMo builtin voice，缺＝Dean
  chapter: "Chapter 3"    # 選填；有它 provenance 的 `doc:` 錨池與 example_coverage 才武裝（見 §4）
  section: "3.1"          # 選填；example_coverage 以它找講義 `\sechead` 區間
scenes:    # 非空 list（必填）
  - …
```

- **Manim 時代必填的 `meta.section` 在 Remotion 降為選填**：解題片（Q7）沒有講義節；缺它只讓 example_coverage 不武裝，不算錯。
- **per-deck opt-in 旗標（沿用 Manim 慣例，預設全關，開了才把該閘的 warn 升 error）：** `meta.otf_enforce`（provenance）、`meta.pedagogy_enforce`、
  `meta.coverage_enforce`、`meta.example_coverage_enforce`。`source_rev` 恆 warn、沒有旗標。
- `meta.pedagogy_profile`（`first_time`｜`review`｜`expert`，預設 `first_time`）與 `meta.assumptions[]`（`id`／`text`／`first_use_unit`／`source`）＝pedagogy PD4 的 registry，選填。

## 2 · `scenes[]` 一場的欄位

| 欄位 | 必／選 | 適用 kind | 規則 | 誰讀 |
|---|---|---|---|---|
| `id` | 必填 | 全部 | 非空字串、全 deck 唯一；進 manifest `scene_id` 與音檔檔名 | tts.py、Remotion timing |
| `kind` | 必填 | 全部 | `intro`｜`content`｜`outro`｜`divider`。tts.py 缺值時預設 content，但本 SPEC 要求明寫 | tts.py、各閘 |
| `say` | 必填 | content | 被朗讀的口語文字，**不寫 LaTeX**（MiMo 照字面唸）；`{show <id>}` 切 beat（文法見 §3）。非 content 場寫了會被 tts.py 忽略（WARN） | tts.py |
| `duration` | 必填 | intro／outro／divider | 正數秒；silent 場的長度。content 場寫了會被忽略（長度來自 manifest） | tts.py → manifest `duration` |
| `bgm` | 選填 | 非 content | 原樣寫進 manifest（Remotion 目前不讀） | tts.py |
| `ref` | 選填（建議） | content／divider | `md:<unit_id>`（內容稿單元）或 `doc:<anchor>`（講義錨；`doc:sec:3.1`／`doc:thm:3.1`／`doc:fig:3.1`）。**這一場的出處**：Remotion 場的上畫面文字寫在 composition（`src/<片>/`）裡、不在 yml，所以場級 `ref:` 是這一場唯一的 provenance 把手（§4） | provenance、step_coverage |
| `refs` | 選填 | content／divider | `{欄位路徑: ref}` 逐欄覆寫；只對 yml 裡帶有上畫面教學文字欄位的場有意義（Remotion 場通常沒有） | provenance |
| `covers` | 選填 | content | `[step_id, …]`：這一場蓋到 `ref:` 所指 `md:` 單元 `screen_contract.required_steps` 的哪些步驟 | step_coverage |
| `scaffold` | 選填 | content／divider | `{motive, problem, flag}`：PD2／PD3／PD4 的宣告欄（Remotion 是否渲出 motive／problem 由設計輪定；閘只查存在與一致） | pedagogy、provenance（`scaffold.motive`／`scaffold.problem` 視為上畫面文字欄） |
| `pauses` | 選填 | content | `[{after: <show id>, seconds: >0}]`；`after` 必須是本場 `say` 裡揭示過的 id（否則 error）。**Remotion 目前不讀**（改在 composition 加 HOLD），但 `rewatch_pack` 折入它，宣告仍要合法 | pauses.py（rewatch_pack） |

**Manim gen-2 遺留、Remotion 分鏡不再接受（出現即 WARN「Manim gen-2 field, not read by the Remotion line」）：**
`template`、`focus`、`paced`、`carry`、`exit`、`accent`、`scene_role`、`hook`、`part`、`layout`、`aside`、`anim`，以及 `meta.video`、`meta.color_map`、
`meta.color_map_enforce`、`meta.fontfloor_enforce`、`meta.layout_enforce`、`meta.mathtype_enforce`。理由：這些欄位的消費者（`scene.py`／模板／`sizecheck`／`focus.py`／`pacing.py`）
全在 `legacy/manim_video/`，寫了沒人讀、只會讓人以為畫面會照做。從封存的正典 storyboard 抄 beat 切分到 Remotion 版時（§3.2 的預定做法），這條 WARN 就是防止把
`template:`／`carry:` 一起抄過來的護欄。WARN 不 error：它不會弄壞 tts／render，只是死欄位。

## 3 · `{show <id>}` 文法（與 `pipeline/narration.py` 同一份）

- 正則 `\{\s*show\s+([A-Za-z0-9_.\[\]]+)\s*\}`；`[`／`]` 會被正規化成 `.`。`{show}`、`{show a b}`、沒閉合的 `{show x` ＝ **malformed → error**（tts 會把它照字面唸出來）。
- 一個 beat＝從一個 marker（或場開頭）到下一個 marker 的文字段；場開頭那段是無 reveal 的首拍（manifest `reveal: null`，Remotion `buildShow` 記成 `"start"`）。
- **同一場內 id 必須唯一（duplicate → error）**：Remotion 的場元件以 id 查拍起訖，重複的 id 查不出「第幾次」。跨場可重用（`s31` 的 `limit`／`continuity` 都有 `paid`）。
- `--list` 列出每場的 reveal id，對照 `src/<片>/` 的元件查表。

## 4 · 內容層閘各讀哪些欄位（武裝前提）

> **原則（[`REVIEW_GATES.md`](REVIEW_GATES.md) §六 6.2）：「某閘 0 finding」不等於驗過——武裝前提要一起寫。** `check_storyboard.py` 對每道閘都印一行武裝狀態
> （掃了幾場、載了幾個錨／契約、內容稿在不在），乾淨與空轉分得開。

| 閘 | 讀 storyboard 的欄位 | 讀 repo 的什麼 | 武裝前提（缺了就是空轉，入口會說） | 嚴重度 |
|---|---|---|---|---|
| `[structure]` | §1／§2 全部 | — | 無（永遠武裝） | 結構錯＝error |
| `[provenance]`（OF2 確定性層） | 場級 `ref:`；`refs:`；上畫面教學文字欄（`statement`／`problem`／`body`／`reason`／`prompt`／`strategy`／`scaffold.motive`／`scaffold.problem`／`annotations[]`／`points[]`／`steps[].reason`／`notes[].text`…） | `content_scripts/<meta.id>.md` 的單元 id（`md:` 錨池）＋ `meta.chapter` 對應的 `handout/latex/src/chNN/*.tex` label key ∪ 凍結 legacy HTML 錨（`doc:` 錨池） | 內容稿存在 或 `meta.chapter` 有值（否則任何 `ref:` 都解不開）。**Remotion 場沒有上畫面文字欄**，所以逐欄檢查對它恆空；**場級檢查**（`provenance.scene_ref_issues`）補上：content／divider 場沒有任何文字欄時，缺 `ref:` 或 `ref:` 解不開＝一條 finding | warn；`meta.otf_enforce` → error |
| `[source_rev]` | 只讀 `meta.id`（找內容稿） | 內容稿標頭的 `source_rev` stamp vs 現檔 | 內容稿存在 | 恆 warn |
| `[pedagogy]`（PD2／PD3／PD4） | `meta.pedagogy_profile`、`meta.assumptions[]`、`scenes[].scaffold.{motive,problem,flag}`、`kind`、`template` | — | PD3（divider 要 `scaffold.problem`）與 PD4（registry 一致）永遠武裝；**PD2 以 `template ∈ {theorem_proof, derivation}` 為閘，Remotion 沒有 `template` ⇒ PD2 在 Remotion 分鏡上不武裝**（待 Remotion 場角色欄位裁決，§6） | warn；`meta.pedagogy_enforce` → error |
| `[coverage]`（SC1／SC2） | `ref:`（`md:`）＋ `covers[]`；`template`（只用在 enforce 下「單元必須有契約」） | 內容稿各單元的 `screen_contract`（`review_pack.parse_content_script`） | 內容稿存在且有 ≥1 份契約、且 ≥1 場帶 `md:` ref。契約解析失敗恆 error（不吃 enforce）。`_SCOPED_TEMPLATES` 的「無契約即 error」以 `template` 為閘 ⇒ Remotion 上不武裝 | warn；`meta.coverage_enforce` → error |
| `[example_coverage]`（EX1／EX2） | `meta.chapter`＋`meta.section`（**不讀 scenes**） | 講義該節 `\sechead` 區間的 `ex:` key vs 內容稿單元的 `examples:`／`folds:` | 內容稿存在（沒有就整個跳過，與 Manim 時代同）；`chapter`／`section` 解得到講義節 | EX1 warn（`meta.example_coverage_enforce` → error）；EX2 恆 warn；節解不開＝一條 EX1 嚴重度的 finding |

## 5 · 入口與 exit code

```bash
.venv\Scripts\python video\pipeline\check_storyboard.py <片>.yml [<片2>.yml …] [--list]
python tools\doctor.py --smoke      # 對 remotion/*/*.yml 全跑一遍（doctor 以 .venv python 呼叫本入口）
```

輸出比照封存的 `schema.py`：每道閘一行標頭 `[<閘>] <檔名>: …`，其下逐條 `  ERROR  …`／`  WARN   …`；最後一行 `[check_storyboard] <檔名>: N error(s), M warning(s)`。

| exit | 意思 |
|---|---|
| 0 | 沒有 error（可以有 warn） |
| 1 | ≥1 error：結構錯、malformed `{show}`、同場重複 id、silent 場缺 `duration`、`pauses.after` 指向未揭示 id、契約解析失敗、或 opt-in enforce 下的閘 finding |
| 2 | 檔案讀不到／不是合法 YAML（輸入層問題，與內容無關） |

多檔一次跑時 exit＝各檔最大值。

## 6 · 待裁決（本輪不定；列給使用者）

1. **場級 `ref:` 缺失對 Remotion 場是 WARN 還是 ERROR。** 本輪＝warn-default＋`meta.otf_enforce` 升 error（沿用 Manim 慣例：閘落地當下對既有 deck 零阻擋）。
   代價：解題片（Q7，本來就沒有講義出處）每跑一次都會列 13 條 WARN；若嫌吵，選項是加 `meta.provenance: none` 之類的宣告式 opt-out（本輪未加，避免沒被要求的旗標）。
2. **PD2／SC「單元必須有契約」在 Remotion 上如何重新武裝。** 兩者都以 Manim `template` 名為閘；Remotion 需要一個場角色欄（例如 `role: proof|derivation|example|…`）
   才能對應。`scene_role` 是 Manim 欄位（`DESIGN.md` 已明定不承接），本 SPEC 把它列進遺留清單而非重用，等設計輪決定 Remotion 的角色語彙後再接。
3. **`pauses:` 要不要讓 Remotion 讀**（[`DESIGN.md`](DESIGN.md) `pauses:` 節的懸案）。本 SPEC 只保證宣告合法，不決定誰消費它。
4. **要不要恢復「正典＋口語」雙軌**（`derive_spoken.py`）。現行 Remotion 分鏡直接寫口語；本 SPEC 以單軌為準，`_mimo` 後綴只保留給生成 deck。
