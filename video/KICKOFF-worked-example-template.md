# KICKOFF — `worked_example` 影片模板（2026-09-13）

> **啟動提示（子代理直接讀）：** 本檔是契約；成功標準全在 §5／§6。依據＝[`_audit/design-template-system/WorkedExample.dc.html`](_audit/design-template-system/WorkedExample.dc.html)（mockup）、
> `LayoutRules.dc.html`（版面 4 條）、`MathRules.dc.html`（數學 5 條）、[`DESIGN.md`](DESIGN.md)「Template catalog」「Lectern 版面網格」「Worked-example 題目結構」「容量契約」「motion primitive」各節。
> 認領來源：[`KICKOFF-s31-amplify.md`](KICKOFF-s31-amplify.md) §0.5「未認領 ← 新對話接」；派工制度見根 `CLAUDE.md`「任務分派」。

## 0. 為什麼

全書 935 個語意塊裡 `workedexample`（例＋解）有 **220 個（24%）**，單一最大宗，影片產線沒有模板可放
（`Main.dc.html` 覆蓋矩陣）。§3.1 講義 16 個例題、影片 27 場一個例題場都沒有——現況只能借 `derivation`＋`prompt:`
（`_common.example_head`），沒有答案框、沒有策略 rail，結論不是畫面上最重的元素（版面規則 1）。

## 1. 拍板（主模型裁決；子代理照做、不重開）

| # | 裁決 | 理由 |
|---|---|---|
| D1 | **列文法與 `derivation` 逐字相同**：`steps[]`／`result`／`check` 的 `{math, anim, frame, cancel, seg_roles, color_role, mark}`；`anim: transform`／`cancel`／`{{…}}`／`seg_roles`／`meta.color_map`／`paced:` 直接**沿用 `derivation.py` 的既有函式**（`_eq_mob`／`_transform_anim`／`_cancel_anim`／`_eq_core`／`_DEFAULT_ANIM`／常數），不複製一份 | 一套變形機制、一套容量契約；derivation 改了這裡自動跟 |
| D2 | **列不收 `reason`（schema error）**、**不收 back-compat `lines[]`（schema error）** | 右 rail 給 `strategy`／`notes`（mockup），與 derivation 的 reason rail 是同一個欄位、不能兩者並存；理由進 `strategy:`／`notes:`／旁白。新模板沒有舊稿要相容 |
| D3 | **列一律左齊 `SPINE_X`，不做 mockup 的 `=` 對齊欄** | `=` 對齊要嘛動 `sizecheck._capacity_issues` 的 `round(left)` 分欄（影響既有 deck），要嘛塞看不見的幾何進列（`paced`／`_rail` 會把它當一段走）；正典 deck 的續行 `= …` 左齊已是 house look。**寫進 DESIGN 當「刻意偏離 mockup」** |
| D4 | **`prompt:` 必填（schema error）**；`result:`（答案框）**必填**，唯一例外＝`part.current < part.total` 的續頁 | 沒題目不是例題；沒答案不是例題；分頁的前幾頁答案還沒到 |
| D5 | **答案框＝畫面最重元素**：滿 `CONTENT_W`、**釘在下三分之一**（底邊＝底安全邊界）、答案數學 **62 px**（`MathRules` 規則 5 的 conclusion 階）、語意色 `accent_role`（預設 practice 綠）、右端 mono tag（`result.reason` 或預設 `answer`）；flat 填色（accent 低不透明）＋accent hairline 邊框、**不用漸層**（house style）、**不用 `accent_panel` 的左色條**（mockup 無） | 版面規則 1（結論最重）＋規則 2（下三分之一不空置）；規則 5 三階＝62／48／34 |
| D6 | **字級：步驟列 `math`（48）、答案 62、rail 數學 34、rail 文字 `prose_sm`**——62／34 用模板內常數（raw px），**不動 `theme._SCALE_PX`** | 取消 `math_sm 40` 是另案裁決；不在這裡動全域階 |
| D7 | **右 rail（`RAIL_X`，寬 `RAIL_W`）＝`strategy`＋`notes`**，兩者皆選填；rail 存在時步驟欄寬＝`PRIMARY_W − 間距`；**任一列寬過此值 → `build` 直接 `raise ValueError`（訊息點名該列與三條出路：拆列／縮題／拿掉 rail）**——sizecheck 會以「could not build scene」報 error | 版面規則 3（主內容佔寬 <58% 才展開右欄；`RAIL_COL=7` 正好 58.3%）；超量是 authoring 決策、不縮字、不靜默丟內容 |
| D8 | 沒有 rail 時步驟欄用 `CONTENT_W`、**左錨**在 SOLUTION 之下（同 derivation＋prompt 的既有行為），不置中 | 與既有 example 場一致 |
| D9 | **`accent` 未寫時預設 `example`（practice 綠）**：`build` 開頭 `spec.setdefault("accent", "example")`（比照 `callout` 設 `spec["accent"]`，讓 `scene_spine` 的 cap 同色） | 它就是講義的 `workedexample` 容器，講義裡永遠綠 |
| D10 | masthead 沿用 `example_head` 的 **block id**（`eyebrow`／`part`／`prompt`／`solrule`／`sollead`），但在模板檔內自建（**不改 `_common.example_head`**）：eyebrow 走 `resolve_chip`（`kicker` 可覆寫），有 `number:` 時字＝`[ example 3.1 ]`；`title` 渲成 chip 右側的**小字 tagline**（`caption` 30 px、role `text`、非大寫）——mockup 的「the companion limit」 | sizecheck 的 `HEADER` 集合與 `scene_spine` 找 `prompt` 都不用改；`title` 不再是被忽略的欄位 |
| D11 | **reveal id**：`step.N`／`result`／`check`／`strategy`／`note.N`；`strategy`／`note.N` 預設 static（開場就在），`say` 寫了 `{show …}` 才動態（`_common.reveals` 慣例，同 `statement`）；`result` 恆動態 | 揭示時序原語 1 |
| D12 | **容量契約**：`capacity_meta(spec)` 回兩個 `ColumnPlan`——步驟欄 `stack`（`min_pitch=derivation.MIN_PITCH`，`x_bucket=None`）＋rail 欄 `stack`（`min_pitch=RAIL_GAP`，`x_bucket=round(RAIL_X)`）；`extra_bottom`＝答案框高＋間距，**由模板自己的答案框 helper 量出來**（單一來源，放置與稽核同一個數） | L1／L2 比照 derivation；rail 與步驟欄是兩條獨立流 |
| D13 | `scaffold`（motive／problem／flag）比照 derivation 掛在 SOLUTION 之下；`statement` 不收（`prompt` 就是題目） | |
| D14 | **稽核模組**：`template_names.CONTENT_TEMPLATES` 加 `worked_example`（tts `--unit auto` allowlist 自動跟）；`schema._seg_roles_issues` 收 `worked_example`；`schema._derivation_issues` 的列迴圈抽成共用函式給兩個模板用（**derivation 輸出逐字不變**）；`step_coverage._SCOPED_TEMPLATES` 加 `worked_example`（純 allowlist、既有 deck 無此模板故零改變）；`provenance._present_text_fields` 加 `strategy`（scalar）與 `notes.i.text`（先 grep 確認既有 storyboard 沒有 `strategy:`／`notes:` 欄位——2026-09-13 已查：沒有）；`pedagogy._MOTIVE_TEMPLATES` **不加**（prompt 就是 motive）；`lint._example_missing_prompt` 不動（schema 已強制 prompt） | |

## 2. 契約（storyboard 欄位）

```yaml
- id: companion_limit_example
  kind: content
  template: worked_example
  accent: example                 # 省略＝example（D9）
  number: "3.1"                   # 選填 → eyebrow [ EXAMPLE 3.1 ]；省略 → [ EXAMPLE ]
  title: "the companion limit"    # chip 右側小字 tagline（D10）；critic 仍用它當場景標籤
  prompt: "Establish $\\displaystyle\\lim_{\\theta\\to 0}\\frac{1-\\cos\\theta}{\\theta}=0$."   # 必填
  part: { current: 1, total: 2 }  # 選填；續頁 SOLUTION (CONT.)、result 可省
  scaffold: { motive: "…" }       # 選填
  strategy: "Multiply by the conjugate: it turns the numerator into a square."   # 選填；rail 上段
  notes_label: "what each factor does"   # 選填；預設 notes
  notes:                          # 選填；rail 下段，每項一列
    - { math: "\\frac{\\sin\\theta}{\\theta}", text: "$\\to 1$", ref: "Prop 3.2" }
    - { math: "\\frac{\\sin\\theta}{1+\\cos\\theta}", text: "$\\to 0$", ref: "Prop 3.1" }
  paced: [step.0, result]
  say: |
    … {show strategy} … {show step.0} … {show step.1} … {show note.0} … {show note.1} … {show result} …
  steps:                          # 列文法＝derivation（D1）；不收 reason（D2）
    - { math: "\\frac{1-\\cos\\theta}{\\theta} = \\frac{(1-\\cos\\theta)(1+\\cos\\theta)}{\\theta\\,(1+\\cos\\theta)}" }
    - { math: "= \\frac{1-\\cos^{2}\\theta}{\\theta\\,(1+\\cos\\theta)}", anim: transform, frame: true }
    - { math: "= \\frac{\\sin^{2}\\theta}{\\theta\\,(1+\\cos\\theta)}", anim: transform }
    - { math: "= \\frac{\\sin\\theta}{\\theta}\\cdot\\frac{\\sin\\theta}{1+\\cos\\theta}", anim: transform }
  result: { math: "\\lim_{\\theta\\to 0}\\frac{1-\\cos\\theta}{\\theta} = 1\\cdot 0 = 0", reason: "answer" }   # 答案框；reason＝右端 tag 字，預設 answer
  check: { math: "…" }            # 選填；比照 derivation 的綠 ✓ 列，接在步驟鏈末
```

**版面（Lectern）：** masthead（eyebrow＋tagline → prompt → hairline → SOLUTION）→ body zone 上緣＝`sollead` 底 − `TITLE_GAP`；
下緣＝答案框頂 − `BAND_GAP`。步驟欄左齊 `SPINE_X`、`fill_gap` 彈性撐開（同 derivation），`_biased_y` 上偏；rail 頂齊 body zone 頂、
左緣 `RAIL_X`，rail 左側一條 `hairline` 直線（decoration 層），strategy 與 notes 之間一條 `hairline` 橫線；notes 每列＝
數學（34 px、primary）＋文字（`caption`、role `text`）＋`ref` mono tag（`tag` 30 px、`result_ink` 藍）靠右。
答案框：`RoundedRectangle`（`RADIUS_MD`）、寬 `CONTENT_W`、填 accent 色 opacity ≈0.10、邊 accent opacity ≈0.5 stroke 1.5；
內含答案數學（62 px、accent role）左齊＋tag 右齊；底邊釘 `-FRAME_H/2 + SAFE_MARGIN`。

## 3. 動作清單（子代理）

1. `pipeline/templates/worked_example.py`（新檔；docstring 寫契約與 D3／D7 偏離）。
2. `pipeline/templates/__init__.py` REGISTRY＋`pipeline/template_names.py`。
3. `pipeline/schema.py`：`_worked_example_issues`（D2／D4 的 error；`notes[]` 項缺 `math` 為 error；`strategy` 非字串 error）、
   列迴圈抽共用、`_seg_roles_issues` 收新模板、接進 `validate` 迴圈。
4. `pipeline/step_coverage.py`／`pipeline/provenance.py`（D14）。
5. `storyboards/_demo_worked_example.yml`：四場——`companion_limit_example`（§3.1 `ex:3.1`，照 mockup；`source:` 錨 `chapter3.tex §3.1 . Example 3.1`、
   `ref: doc:ex:3.1`；旁白可取材 `content_scripts/ch03_trig_derivatives.md` 的 `companion_limit` 單元，demo 不進正典、不 tts）、
   `no_rail`（無 strategy／notes，證 D8）、`capacity_over`（7 個分數列，證 L2 warn）、`multipage_p1`（`part 1/2`、無 result，證 D4 例外）。
   `meta.color_map: {"\\theta": concept}`。
6. `pipeline/_selftest_worked_example.py`（平鋪 assert、`_bootstrap` 風格；見 §5）。
7. `DESIGN.md`：Template catalog 加一列；新節「Worked-example 模板 `worked_example`」寫契約、id、容量、**D3／D7 偏離 mockup 與理由**；
   「Worked-example 題目結構」節末加一句指到新模板。`README.md`：模板清單加 bullet、`_demo_*` 清單加 `_demo_worked_example`。
8. 一個 commit（subject `feat(video): worked_example 模板——題目／SOLUTION／步驟鏈／答案框（依設計畫布 mockup）`；body 列 D1–D14 中有落地判斷的、測試數字、零行為改變證據）。

## 4. 不准動

`storyboards/ch03_trig_derivatives*.yml`、`ch03_chain_rule.yml`、`ch01_inverse_functions.yml`、任何既有 `_demo_*.yml`、
`_common.example_head`、`theme._SCALE_PX`、`derivation.py`（只 import 它，不改它）、`sizecheck.py`（若 D12 靠既有 `capacity_meta` 介面就夠，不改）、
`REBUILD_STATUS.md`／`KICKOFF-s31-amplify.md`（主模型收尾寫）。不跑任何計費 API；不 render 正典 deck。

## 5. 驗收（子代理回報必含）

1. `_selftest_worked_example.py` 綠，至少涵蓋：block id 集合；答案框底邊＝底安全邊界（±0.02u）、寬＝`CONTENT_W`（±0.02u）；
   答案字級 > 每個步驟列字級；步驟列左 ≈ `SPINE_X`、rail 左 ≈ `RAIL_X`、有 rail 時步驟列右緣 < `RAIL_X`；`strategy` 無 marker 為 static、有 marker 為動態；
   transform 列為 callable 且 `anim_seconds` 正確；未寫 `accent` 時 `accent_role(spec)=="practice"`；schema 五條 error（缺 prompt／列有 reason／`lines[]`／缺 result／
   `seg_roles` key 無段）＋`part 1/2` 缺 result 不報；rail 過寬 `build` raise；`capacity_over` 有 split warn、`companion_limit_example`／`no_rail` 無。
2. `_derivation_issues` 對 derivation fixture 的輸出**逐字不變**（selftest 內放一個 derivation dict 的 before/after 比對，或直接跑
   `schema.py` 對 `_demo_tex_parts.yml`／`ch03_trig_derivatives.yml` 比對基線）。
3. `python video/pipeline/run_selftests.py` 全綠（既有 40 + 新 1）；`_selftest_template_registry`／`_selftest_tts_unit` 綠。
4. 零行為改變：`schema.py`／`lint.py`／`sizecheck.py` 對全部既有 storyboard 的輸出逐字相同（主模型另有基線比對；子代理至少自查 `ch03_trig_derivatives.yml`、`_demo_derivation.yml`、`_demo_tex_parts.yml` 三個）。
5. `python video/scratch_frames.py --storyboard video/storyboards/_demo_worked_example.yml --out <scratch>/frames` 四場都出 PNG（1080p），
   回報時附路徑；主模型看幀。
6. 回報格式：改了哪些檔、測試數字、沒做到的條款（逐條對 D1–D14 與 §5）。

## 6. 完成定義（主模型收尾）

selftest 全綠、基線比對逐字相同、`doctor --smoke` 逐字相同、mock render 抽幀自檢、standalone HTML 報告
（`_audit/REVIEW-worked-example-template-applied.html`，幀 base64 內嵌）、`REBUILD_STATUS.md` 記一段、`KICKOFF-s31-amplify.md` §0.5 勾選。

## 7. 結果（2026-09-13）

- **落地 commit `c79372c`**（Opus 子代理、worktree、一個 commit）；契約 `b229973`；報告與收尾另一 commit。
- **D1–D14 全數做到**；子代理四個契約外判斷全部覆核接受（見報告「子代理判斷與覆核」）：① `sizecheck._capacity_issues` 加「完全落在 `extra_bottom` 保留帶內的 block 不計入堆疊」（否則答案框被算兩次）；② 有答案框不畫 motif；③ rail 分隔線收進 strategy group；④ 試點場收成 2 列（容量）。
- **驗收：** `run_selftests` 40→41 全綠；22 個既有 deck × schema／lint／sizecheck 66 份輸出逐字相同；`doctor --smoke` 逐字相同；試點 mock render `[sync]`／`[stillness]` clean、抽幀自檢；零計費、正典 deck 未動。
- **報告：** [`_audit/REVIEW-worked-example-template-applied.html`](_audit/REVIEW-worked-example-template-applied.html)（產生器 `_audit/_gen/worked_example_template.gen.py`＋digest）。
- **交裁決：** ① 單頁容量（48 px 步驟階下每頁約 2 個分數列，mockup 的 4 列放不進去——建議維持規則 5、用 `part:` 分頁）；② 正典 §3.1 三題要不要遷到新模板（另案）。
- **裁決結果（2026-09-13 主對話定案；asr-24 轉使用者過目，未推翻即生效）：**
  - **① 單頁容量＝維持規則 5**（步驟 48 px、答案 62 px），長解法一律用 `part:` 分頁、**答案框留在末頁**（D4 的續頁例外已支援）。**不**給 `worked_example` 另開 40 px 步驟階——那與規則 5「取消 `math_sm 40`」及容量契約「字級恆定不可協商」正面相撞。
  - **② 正典 §3.1 三題（`ex:3.1`–`ex:3.3`）＝不遷移。** 依據＝[`KICKOFF-shared-layer-v1.md`](KICKOFF-shared-layer-v1.md) §7「明確不做（本輪）」已列「`worked_example` 對既有 9 個 `derivation` + `prompt:` 場的遷移」；`derivation`＋`prompt:` 是合法的輕量形態，遷移另案再議（§8 backlog 有記）。
  - 附帶：D6 的 **62／34 raw px** 是本模板內的常數，**共用層 v1 的 T2 會把它升成 `theme._SCALE_PX` 的具名 token**（T4-5 回歸時模板改讀 token）。
- **未做：** `=` 對齊欄（D3）、填色 chip／外框 SOLUTION pill（全模板共用樣式）、`statement` 的 schema error、§7.1 其餘項目。
