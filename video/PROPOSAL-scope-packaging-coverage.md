# PROPOSAL — 影片內容取捨的三件事：分工、封裝、例題涵蓋（定稿）

> 2026-09-12 立檔；同日四鏡（教學設計／產線工程／契約一致性／反對）獨立裁決，終審依親驗證據收斂成本定稿。
> **狀態：已執行（2026-09-12）。** §6 步驟 1–7 全部完成、§7 驗收全過、回歸審核 0 blocking。
> 執行紀錄與實測數字見 [`REBUILD_STATUS.md`](REBUILD_STATUS.md) 品質補強輪 ⑩；
> 交付物 [`content_scripts/_audit/REVIEW-example-coverage-applied.html`](content_scripts/_audit/REVIEW-example-coverage-applied.html)。
> 執行中修掉三個本檔未預見的問題（無 `.md` 的 deck 誤咬、`folds:` 多行被 join、裸 key 的診斷），詳見 ⑩。
> 起因＝使用者問「影片內容取捨是不是也要重新設計」「要不要讓講義指導影片，還是把講義當大綱、兩條線分開」。

---

## 0. 一頁摘要

| # | 提案 | 裁決 | 改動面 |
|---|---|---|---|
| ① | **分工升格成通則**：講義治「涵蓋什麼、什麼是對的」，影片治「什麼順序、切幾支、多長、畫面放什麼」 | **做**（§1 論證重寫；U1-a 不加閘） | 文檔：`CONTENT_METHODOLOGY.md` §1／§7 |
| ② | **一支影片的單位從「節」改成「幕」**（`make.py --act`） | **不做**。節內導航＝既有 sidecar `<stem>.chapters.txt`（T7）；「一節＝一支影片」規則不改 | 零 code；`CONTENT_METHODOLOGY.md` §2 加一句指標 |
| ③ | **例題涵蓋閘** → 改名**例題折疊宣告閘** | **做**，但技術設計依親驗重寫（宣告進 `.md`、閘純 `.md`↔`.tex` 比對、按 `\sechead` 區間歸節） | 新 `pipeline/example_coverage.py`＋`review_pack._FIELD_KEYS`＋`schema.py` 接線＋selftest＋兩份 `.md` 回填＋文檔 |

**對使用者兩個問題的直接回答：**

- **「內容取捨要不要重新設計」——不要。** 取捨規則已經在：§1 忠實於講義、§2 代表式涵蓋（同型例題可折疊但 MUST 註明）、§3 順序為教學自由重排。缺的是 (a) §1 開宗明義的分工宣告 (b) 折疊宣告的確定性閘 (c) 順序規則的鎖稿前自檢。使用者記憶中的「只放重點」在**例題層**是合法的（§2 折疊），在**證明步驟層**不合法（`DESIGN.md` 反模式「>4 步壓成 2–3 行」、§3.1 第一版壓縮學費）——兩層不要混。
- **「講義指導影片 vs 兩條線分開」——不拆。** 講義治涵蓋／正確性／可回溯，影片治順序／切分／節奏／畫面。這條線本來就在（§1:34、§3:82），本案把它寫成通則。

---

## 1. 依據（親驗＋四鏡核實）

**1.1 §3.1 成片＝973.2 s＝16.2 分、27 場、四幕**（digest `total_seconds`；反對鏡 A4 逐幕加總核對）：

| 幕（divider） | 場數 | 長度 |
|---|---|---|
| `divider_limit` 極限是什麼 | 3（＋intro） | 2.4 分 |
| `divider_squeeze` 幾何夾擠 | 9 | 6.5 分 |
| `divider_derivatives` 兩個導函數 | 5 | 2.6 分 |
| `divider_apply` 應用與延伸 | 9（＋outro） | 4.5 分 |

全書推算：§3.1 佔全書 935 個語意塊中的 18 個（1.9%）→ 全書約 840 分＝14 小時、66 節平均 12–13 分／節（語意塊盤點見 `REBUILD_STATUS.md` 品質補強輪 ⑨）。

**1.2 順序自由早就是通則——原提案 §2「現況」寫錯了。** `CONTENT_METHODOLOGY.md:34`（§1 硬規則）：「場景**順序可為教學自由重排**（見 §3）」；`:82` §3 整節標題「### 順序：為教學自由重排」，附 12 步非書序偏好流程。`git log -S"順序：為教學自由重排"` 只有 `10acfd5`（2026-06-01），比 §3.1 內容稿 LOCKED（2026-06-29，`5f3e7ea`）早近一個月。**真正的現況＝「規則在、撰稿時沒遵守、鎖稿前沒自檢」**，藥方是「升格＋自檢」，不是「補真空」。

**1.3 沒有任何一道閘在管順序（正確）。** `step_coverage.py` docstring：*"Merging/re-layout is free (one reveal may cover many ids); only dropping a must-show step is a finding."*；`provenance.py` 只管可回溯、`pedagogy.py` PD1–PD4 只管粒度／動機／divider problem／前提 flag、NFA 對的是我們自己的內容稿。

**1.4 順序失誤案例只有兩個，且修復已定案。** 場 06（對稱論證擋在單位圓圖前 38 s；`chapter3.tex:43` 就是這個順序；四鏡同指）、場 13（度數導數公式在 sin′=cos 推出前印出；`chapter3.tex:96-99` 的 `envcaution` 位置一一對應——且 §3「env-caution 併入其警示對象的單元」照做本可避免）。**場 20 不是順序問題**：digest `scenes[19].synthesis` 判「動機與後續用途都沒有交代——內容稿層的問題」，`yml:548` 的 `scaffold.motive` 本身就沒交代用途，挪到哪都一樣；歸 PD2／`scaffold.motive`。三處修復＝品質補強輪 ⑤④ R6（`REBUILD_STATUS.md:26`；`KICKOFF-motion-primitives.md:15`「不在本輪，放大階段做」）。**① 因此是面向下一節的預防性通則，不是修 §3.1。**

**1.5 「16 分鐘太長」查無稽核證據。** digest `film.overall`：「內容與骨架是好的……問題幾乎全在『畫面怎麼教』這一層」；六鏡 96 條 finding 與品質補強輪 ①–⑨ 沒有一條講片長；五鏡抱怨的是畫面不動（content 場靜止 92–97%）。片長是**使用者本輪的新偏好**，不是被稽核出的問題——這決定了 ② 的處置（§3）。

---

## 2. 提案 ① — 分工升格成通則：做

### 2.1 寫進 `CONTENT_METHODOLOGY.md` §1 的內容（緊接兩條硬規則之後）

**分工（2026-09-12 拍板）——講義治「什麼」，影片治「怎麼呈現」。**

| 誰治 | 治什麼 | 由什麼守 |
|---|---|---|
| **講義** | **涵蓋**（每個 definition／theorem／proposition；每個不同教學模式的 example）、**正確性**（定義與定理陳述、數學事實）、**可回溯**（每段上畫面文字有來源） | `provenance` OF1/OF2、`step_coverage` SC1/SC2、`example_coverage` EX1/EX2（本案 ③）、NFA、`source_rev` |
| **影片** | **順序**、**切分**、**節奏**、**畫面構成**、**視覺發明** | **無確定性閘**（創作決定）。owner 指名：鎖稿前 §7「順序自檢」（免費）→ gate-1 `pedagogy-firstlearner-audit`（PD1／L2 脈絡）→ render 後 REWATCH R3 `A-bridge`（advisory；是否常設另議） |

兩條操作規則：

- **重排不需要理由，漏掉才需要。**（`step_coverage` 既有語義的升格。）
- **重排不得違反數學依賴序**——不得在證明／建立之前使用某結果。

範圍註記：本規則管**新稿的場級順序**。§3.1 已鎖稿的 06／13 是 beat 級（鎖在 LOCKED 旁白內，動它＝重 TTS），走 R6，不在此。

### 2.2 U1-a 數學依賴序：不加閘（四鏡收斂）

理由（寫進 §1，取代原提案的「作者不會犯」）：(1) 每場開頭的回指句（"that little bound"／"we already did the hard algebra"）已把依賴**表面化**，違反依賴序會直接產生無先行詞的句子，gate-1 與 R3 `A-bridge` 看得見；(2) 步驟級依賴已有 `screen_contract.required_steps[].depends_on`＋`recap_required`（`SPEC-pedagogy-firstlearner-expansion.md:66-70`），場級再加是第二套真相；(3) PD4／`scaffold.assumes`／SC2 三個代理已在；(4) 零實際案例；(5) 成本不只一個欄位（`review_pack._FIELD_KEYS` 白名單要動＋新檢查＋全 deck 回填）。**若日後真做，欄位名用 `order_depends_on`**（`depends_on` 已被 `required_steps[]` 佔用）。

**與 ③ 的不對稱（反對鏡 S3，要寫明）：** 順序是語意判斷，機器做不了，所以交給人與 agent；例題折疊是純書記，閘便宜、比照現成 pattern——③ 是**低成本預防性閘，不是因為出過事**（§3.1 跑起來預期 0 EX1）。

### 2.3 U1-b `source_rev`：對得上，理由更正

`source_rev.py:39` 的 `_STAMP` 只在 `.md` **標頭**抓**一行**：repo 相對路徑＋整檔 LF 正規化 sha256——**整個 deck 一個 stamp，hash 的是整份講義源檔**，不是逐單元。順序脫鉤仍安全的真正理由：storyboard 場序位於 `.md` 下游，從不進 stamp 計算。副作用（非 blocking，記錄即可）：整檔粒度只能說「講義變了」，說不出哪個單元變了；§8 定位仍靠 `.md` 的 `source:` 自由文字。

### 2.4 文檔改動

- `CONTENT_METHODOLOGY.md` §1：上表＋兩規則＋範圍註記＋U1-a 理由（2.1–2.2）。
- `CONTENT_METHODOLOGY.md` §7 檢核表新增一條（教學鏡 F4，零成本自檢）：
  - [ ] **順序自檢**：本節有沒有在推導之前就把結論式放上畫面？是刻意的 advance organizer，還是洩題？（§3.1 場 13 學費）有沒有把「為什麼現在做這個」的先行條件放在它的圖／式**之後**？（場 06 學費：對稱論證在單位圓圖前 38 s）
- 原提案 §0 的「壓縮失敗史」類比改寫為 §0 第二段的兩層說法（例題層可折疊、證明步驟層不可壓）。

---

## 3. 提案 ② — 幕為單位：不做

**裁決：不新增 `make.py --act`、不做幕級 intro/outro、不改 `CONTENT_METHODOLOGY.md:40`「一節 = 一支影片（小節之間不另做過場片）」。** 理由，按重量排：

1. **與現行 MUST 級規則正面對撞而原提案未提。** `:40` 原文如上；§3.1 的四個 divider 正是這節的小節層級（`chapter3.tex` §3.1 內 5 個 `\subsechead`），`--act` 做的正是規則禁止的事。要做就得先改規則，那是使用者要另外裁的事，不是 15 行 code。
2. **前提查無實據**（§1.5）。
3. **四幕不是獨立單元。** 三個幕首的先行詞都在幕外：幕 2「Here is that new tool」（→ 場 03）、幕 3「we already did the hard algebra: that quotient is cos(x+h/2)·sin(h/2)/(h/2)」（→ 場 04，第 1 幕）、幕 4「The fundamental limit has a companion」（→ 場 10）。第 3 幕六鏡零 weak 零 bad 不是因為它 2.6 分，是因為前兩幕已把帳付完——**這正是幕不能單賣的證據**。獨立播放要嘛斷（U2-a）、要嘛改 LOCKED 旁白重 TTS（與「不動內容」自相矛盾）。
4. **切了之後第 4 幕第一分鐘就是門面缺陷**（divider 問「tan′ sec′ cot′ csc′＝?」，下一場開口卻是伴隨極限），前置條件＝先裁場 20 的位置（R6 未做）。
5. 工程面：逐幕 loudnorm 各自 normalize 造成幕間響度級差（`make.py:630` two-pass 對 concat 成品量測）、同場 encode 5×、全書 66 節×4 幕≈264 支檔的導航問題、intro/outro 模板讀 `meta.sections` 不能直接當幕級用。

**取而代之（零 code、已存在）：** `make.py` compose 每次都寫 `<stem>.chapters.txt`（`make.py:771-773`、`captions.to_chapters`：intro 的 tagline 在 0:00＋每個 divider 的 `title`，YouTube 章節格式；T7，2026-07-11 落地、`DESIGN.md:1061` 有記）。§3.1 全片 compose 即得 5 個跳轉點（0:00 intro＋四幕）。**一支 16 分、四個可跳轉點：敘述零斷裂、零重複 branding、零 TTS、零 schema。** 教學鏡的 N1 就是它，只是沒人注意到已經做完。文檔上只在 `:40` 括號內加一句：「節內導航靠成片 sidecar `<stem>.chapters.txt`（divider／intro 時間點）；2026-09-12 裁決不做分幕獨立檔。」

**唯一重開條件：** 使用者看過帶章節標記的成片後**仍**要獨立檔案（排課／連結需求）。屆時另立提案，前置＝改 `:40` 規則＋先裁場 20 位置；技術降規可直接沿用工程鏡的結論（divider 當分界非起點、`--act` 算出 id 清單後走 `select_scenes()`、與 `--scene` 互斥、不做幕級 intro/outro、loudnorm 四幕共用整片一次 pass-1 量測）。

---

## 4. 提案 ③ — 例題折疊宣告閘：做（技術設計重寫）

### 4.1 親驗更正原提案三個技術前提

| 原提案 | 親驗結果 | 後果 |
|---|---|---|
| 「`provenance.py` 目前解析 `doc:sec:`／`thm:`／`def:`／`fig:`——加 `doc:ex:`」 | `provenance.py:53` `_TEX_ENV_KEY = \\begin\{env[a-z]+\}\{[^}]*\}\{([a-z]+:[^}\s]+)\}` 是泛型，docstring `:10-12` 明列 `ex:...`；`ex:3.1`–`ex:3.16` 今天就解得出來 | 步驟 1 成本 0 行；真正要寫的是下一列 |
| 隱含「`ex:3.x` 屬 §3.x」 | **`ex:` 是章序不是節序**：`chapter3.tex` `\sechead{3.1}`(L30)→`ex:3.1–3.3`(L136–183)、`\sechead{3.2}`(L208)→`ex:3.4–3.8`、`\sechead{3.3}`(L417)→`ex:3.9–3.16`；ch01 六節 `ex:1.1–1.43` 連號跨節（§1.1→`1.1–1.8`、§1.5→`1.26–1.36`）；`calcbook.sty:271-276`：counter「章內連續」、label key「沿用歷史號、不承諾等於印值」 | **必須按 `\sechead` 區間掃描歸節；用節號前綴 match 會災難性錯判；集合比對、不假設連號** |
| 涵蓋判定 (a)「被某個 storyboard 場的 `ref:`／`refs:` 指到」 | 全 18 個 storyboard **零**個 `doc:<kind>:` 形式 ref；ch03 教學場的 `ref:` 全是單值 `md:<unit>`（`yml:79/111/196/…`），divider 是 `doc:frag-sec-3-1`；`refs:` 是 per-field 的 OF1/OF2 覆寫（`provenance.scene_text_refs`），語義是「這個欄位的文字可回溯到這裡」，借來掛例題錨會污染 provenance 閘 | **(a) 做不到**；照原稿實作 §3.1 三個 `ex:` 一個都不命中 → 3 EX1，§6.3 驗收自我否定。宣告只能進 `.md` |

### 4.2 設計（比照 `step_coverage.py`：契約在 `.md`、確定性層純比對、warn-default）

**(1) 錨與歸節。** 新模組 `pipeline/example_coverage.py`（pure stdlib）提供 `tex_examples_by_section(text) -> dict[str, list[str]]`：對章 `.tex` 用 `finditer` 順序掃 `\sechead{n.m}`（沿用 `provenance._TEX_SECHEAD`）與 `\begin{envexample}{…}{ex:…}{}`（沿用 `provenance._TEX_ENV_KEY`、只收 `ex:` 前綴），每個 `ex:` 歸入它前面最近的 `\sechead`。deck 的章／節取 `meta.chapter`（"Chapter 3"→3）與 `meta.section`（"3.1"），`.tex` 路徑用 `Loci._handout_anchors` 同一個 glob（`handout/latex/src/ch{NN}/*.tex`）。`provenance.py` 本身不改。

**(2) 宣告——只在 `.md`，正反兩面都在代表單元上。** `CONTENT_METHODOLOGY.md` §6 欄位表新增兩欄（選用）：

```
### unit: all_six_trig_derivatives
examples: ex:3.2                 # 本單元教到的講義例題 label key；多個以逗號分隔
folds: |                         # 折疊進本單元的同型例題；一筆一行；理由必填
  ex:3.6 — 同 quotient rule 手法（cot′／csc′ 與 tan′／sec′ 同型），留給講義練
```

`review_pack._FIELD_KEYS`（`:75`）加 `examples`、`folds`——**不加就被 `:147` 的 `if key not in cur: continue` 靜默吞掉、閘看到零宣告、全部 EX1**（工程鏡 D1；selftest 專門守）。宣告放代表單元上＝「就近註明」本身；原提案的 `folded_into: <unit>` 跨檔 join 與「dangling fold」finding 因此消失。閘不讀 storyboard（③ 與 ① 互不干擾：重排 storyboard 不影響宣告）。

**(3) 判定與 finding。** 對一個 deck：`E` ＝ `.tex` 該節的 `ex:` 集合；`T` ＝ 全部單元 `examples:` 聯集；`F` ＝ 全部單元 `folds:` 的 key→reason。
- **EX1（silent drop）**：`e ∈ E`，`e ∉ T ∪ F`。訊息：`[EX1] ex:3.2: handout example in §3.1 neither taught (examples:) nor folded (folds:) by any unit`。
- **EX2（宣告不成立）**：宣告的 key `∉ E`（打錯字或別節）；fold 理由空；同一 key 同時在 `T` 與 `F`。
- 嚴重度：EX1 ＝ `error` if `meta.example_coverage_enforce` else `warn`；EX2 恆 `warn`（比照 SC 的 orphan `covers`）。
- **乾淨時不印**；有 finding 才印 `[example_coverage] <deck>: N finding(s) (ENFORCED | warn-only; set meta.example_coverage_enforce to gate)`，格式與 `[coverage]` 區塊逐字同型。
- 跳過條件：deck 無 `.md`（`provenance.content_script_for` 不存在→skip，同 SC）；`_mimo` deck 經 `content_script_for` 剝後綴共用基底 `.md`；`_fixture*` 的 `section: "0.0"` 在 `.tex` 找不到區間→`E=∅`→零輸出；`_demo_*` 無 `.md`→skip。

**(4) 接線只接 `schema.py:main()`**（緊接 `[coverage]` 區塊之後，`:243-265` 同型），**不接 `make.py`**——SC 就只在 `schema.py`（`make.py` 只重複了 provenance／source_rev／pedagogy 三閘，`coverage` 本來就不在），`doctor.py --smoke` 走的也是 `schema.py`；例題選材是撰稿期決定，不該擋 render preflight。`make.py`／`schema.py` 三閘重複接線是既有技術債，本輪不順手重構（Karpathy §3）。

**(5) selftest** `pipeline/_selftest_example_coverage.py`（`run_selftests.py` 自動發現）：hermetic，in-memory `.tex` 字串含 `\sechead{3.1}`＋`ex:3.1–3.3`、`\sechead{3.2}`＋`ex:3.4`。斷言：(i) **章序陷阱**：`ex:3.2 ∈ §3.1`、`∉ §3.2`；(ii) §3.1 漏宣告一個 → 恰一個 EX1；(iii) 全宣告 → 0 finding；(iv) 打錯 key／空理由／同 key 既教又折 → EX2；(v) 用 tempfile 寫一份含 `examples:`／`folds:` 的 `.md`，經 `review_pack.parse_content_script` 後兩欄是非空字串（守 D1）；(vi) `enforce=True` 時 EX1 為 `error`、EX2 仍 `warn`。

**(6) 回填（純書記，兩份正典 `.md`，各單元 `source:` 已寫明 Example 編號）：**
- `ch03_trig_derivatives.md`：`companion_limit`→`examples: ex:3.1`；`all_six_trig_derivatives`→`ex:3.2`；`shm_compute`→`ex:3.3`。
- `ch03_chain_rule.md`：`example_single_composition`→`ex:3.4`；`example_nested_three_layers`→`ex:3.5`；`example_chain_times_quotient`→`ex:3.6`；`example_chain_times_product`→`ex:3.7`；`example_leibniz_rates`→`ex:3.8`。
- 兩節都不需要 `folds:`（例題全部有單元）。`ch01_inverse_functions` **沒有 `.md`**（gen-1 遺留），閘 skip、不回填。
- 兩份 `.md` 都是 LOCKED：只加 metadata 行、narration 零改動；`derived_check` 只 stamp `<deck>.yml`＋`.spoken.yml`（`derived_check.py:69`）、`source_rev` hash 的是講義源、NFA 對的是 narration——三者皆不受影響；`_narration.html` 不需重編（narration 未變）。
- **本輪不開 `meta.example_coverage_enforce`**（warn-default 是所有閘的落地慣例；開 enforce 要動正典 yml meta→`_mimo` 需重 derive，留給 §3.1 整節重做輪順做）。

### 4.3 名字與免責（教學鏡 F5／U3-b）

模組名沿用 `example_coverage.py`，但文檔與模組 docstring 一律稱**「例題折疊宣告閘」**並印一句：「本閘只擋 silent drop 與空宣告；**不判折疊得對不對、不判教得好不好**。」現成反例：`ex:3.1`（伴隨極限）有場 20 對應、閘判 covered，但四鏡同指它是孤兒（後段與 recap 都沒回用）——那是 gate-1／R5 的事。為此 `PEDAGOGY-FIRSTLEARNER-RUBRIC.md` 加一行 advisory **EX-adv**：「`folds:` 的理由是否成立（同型判斷＝語意，agent 判；閘只查宣告存在）」，inputs 清單（`:13`）加「cited `.md` 的 `examples:`／`folds:`」。

### 4.4 文檔改動

- `CONTENT_METHODOLOGY.md` §2 `:45` 例題規則末尾加：宣告語法指向 §6、閘只擋 EX1/EX2 的免責句；§6 欄位表加 `examples`／`folds` 兩列＋parser 註記（`_FIELD_KEYS` 同步）；§7 第一條加「`examples:`／`folds:` 已宣告；`schema.py` `[example_coverage]` 0 EX1」。
- `DESIGN.md` 反模式／閘表（`:937` SC 列之後）加一列：「講義該節有 `ex:` 既未 `examples:` 也未 `folds:`（EX1）→ 在代表單元宣告 → **example_coverage warn**（opt-in `meta.example_coverage_enforce` 才 error）」。
- `REVIEW_GATES.md:67` `schema.py` 列加「2026-09-12 增掛 `example_coverage`（EX1/EX2，宣告在 `.md`）」；`README.md:34`／`:174` 的 schema.py 並跑清單加 `example_coverage`。
- 本輪 HTML 報告：`video/content_scripts/_audit/REVIEW-example-coverage-applied.html`（繁體中文框架；逐 deck 列 N 個例題／M 個 `examples:`／K 個 `folds:`、每一行新增的宣告、回填**前**的閘輸出（3／3／5 個 EX1＝閘有效性證據）與回填**後**的零輸出、回歸審核結果）。

---

## 5. 明確不做

- **不壓縮內容。** 證據：六鏡無一說「講太多」，五鏡抱怨畫面不動；正在跑的 motion-primitives 輪治的就是那個。
- **不拆講義與影片的內容權威**：`provenance`／`step_coverage`／NFA／`source_rev` 全保留。那層耦合擋的是講錯、講漏；使用者要的自由（順序、節奏、畫面）本來就沒被任何閘綁住（§1.3）。
- **不做 `--act`、不做幕級 intro/outro、不改「一節＝一支影片」**（§3）。
- **不加場級依賴序閘 `order_depends_on`**（§2.2）。
- **不動 `provenance.py`**（`ex:` 已解析）、**不接 `make.py`**、**不重構 `make.py`／`schema.py` 的重複接線**。
- **不動字體、版面構成與數學排版規範**（品質補強輪 ⑨ 未竟項，另案）。
- **不動 §3.1 的 06／13／20**（R6，另輪）。

---

## 6. 執行順序

| 步 | 做什麼 | 完成判準 |
|---|---|---|
| 0 | 使用者裁決本定稿；本檔頂部「待裁決」改「已裁決（日期）」 | — |
| 1 | ③ code：`pipeline/example_coverage.py`＋`review_pack._FIELD_KEYS` 加兩欄＋`_selftest_example_coverage.py` | `python video/pipeline/run_selftests.py` 全綠、數量 +1 |
| 2 | ③ 接線 `schema.py:main()`；對 `ch03_trig_derivatives.yml`／`_mimo.yml`／`ch03_chain_rule.yml` 各跑一次 `schema.py` | 預期 3／3／5 個 EX1（**閘會咬**）；把輸出存進 HTML 報告 |
| 3 | ③ 回填兩份 `.md` 共 8 行 `examples:`；重跑步 2 | 0 EX1／0 EX2、`[example_coverage]` 區塊不印；`derive_spoken.py --deck ch03_trig_derivatives --check` parity 仍過 |
| 4 | ①＋②＋③ 文檔（§2.4、§3 末段、§4.4 清單）一次 commit；Mode B 式 commit body 逐條寫「原本是什麼、為何不妥、改了什麼、證據」 | `git grep -n example_coverage` 命中 §7.6 列的檔案 |
| 5 | HTML 報告 `REVIEW-example-coverage-applied.html` | 雙擊即開、含 before/after 閘輸出 |
| 6 | 回歸審核（依 `CLAUDE.md`「修完後必須回歸審核」）：對步 1–4 的改動跑一輪覆核——Codex `exec -s read-only`（**逐次徵詢**）或手動比對；結果附進 HTML 報告末節 | 0 新 blocking |
| 7 | `REBUILD_STATUS.md` 加本輪一條（含「② 不做＋重開條件」「① 升格」「③ 落地＋回填」）；本檔標「已執行」 | — |

步 1–3 無外部 API、無計費；步 6 若用 Codex 需先徵同意。

---

## 7. 驗收標準

1. `python video/pipeline/run_selftests.py` 全綠，且含 `_selftest_example_coverage`（內含章序陷阱斷言 `ex:3.2 ∈ §3.1`）。
2. `schema.py` 對三個正典 deck：`[example_coverage]` 0 finding（乾淨不印）；HTML 報告內留有回填前 3／3／5 個 EX1 的輸出。
3. `python tools/doctor.py --smoke` 輸出與改前**逐字相同**（含各 deck 的 WARN 計數）；`_demo_*`／`_fixture*` 零新輸出。
4. 預設全片建置的 schema／lint／sizecheck 報表逐字相同（純新增路徑、乾淨不印）。
5. `git diff` 兩份 `.md`：只有 `examples:` 行（3＋5），narration／`source_rev` 標頭零改動。
6. 文檔七處改齊：`CONTENT_METHODOLOGY.md`（§1 分工表＋兩規則＋範圍；§2 `:40` 括號指標＋`:45` 免責；§6 兩列；§7 兩條）、`DESIGN.md` 閘表一列、`REVIEW_GATES.md:67`、`README.md:34/:174`、`PEDAGOGY-FIRSTLEARNER-RUBRIC.md` EX-adv、`REBUILD_STATUS.md`、本檔狀態行。`:40` 原句「一節 = 一支影片。（gen-2：一節一片；小節之間不另做過場片。）」**逐字未改**，只加括號指標。
7. 下一次 §3.1 全片 compose（motion-primitives 輪順帶）產出的 `<stem>.chapters.txt` 恰 5 行：`0:00` intro tagline＋四個 divider 標題——這是 ② 替代方案的驗收，不在本輪 render。
8. HTML 報告存在、框架繁體中文、含回歸審核結果。

---

## 8. 已知風險

- **假保證（U3-b）。** 閘只查宣告存在。作者可以宣告 `folds:` 理由亂寫而閘全綠；防線＝rubric EX-adv（gate-1 語意審）。文檔與 docstring 的免責句就是為了不讓人以為「有閘就安全」。
- **`_FIELD_KEYS` 漏註冊 ⇒ 全 EX1。** selftest (v) 守；文檔 §6 parser 註記提醒改格式要同步 parser。
- **`folds:` 理由內含 `ex:` 字樣會被當成下一筆。** 文檔註明「理由裡不要寫 `ex:` token」。
- **`\sechead` 形狀。** `_TEX_SECHEAD` 只認 `\d+\.\d+`；附錄（`\cbchapter{A}`）不在影片線範圍；章 `.tex` 目前每章一檔，若日後拆檔、節不得跨檔（現況不存在，出現時再處理）。
- **LOCKED `.md` 加 metadata 行。** 親驗不動 narration、不動任何 stamp；若使用者認定 §3.2「凍結」含 metadata，則步 3 只回填 §3.1，§3.2 的 5 個 EX1 WARN 列為已知（與現行 `[source_rev]` WARN 同性質），驗收 3 改為「WARN 變動僅來自 `[example_coverage]` 且僅在 `ch03_chain_rule`」。
- **② 不做的風險。** 使用者若確有短檔需求（排課／連結），現況只有章節標記；重開條件與技術降規已列在 §3，不必重新調查。
- **① 無閘的風險。** 順序失誤只能在鎖稿前自檢、gate-1 與 REWATCH 攔；REWATCH 是否常設為閘另議（品質補強輪 ①）。
