# KICKOFF — 工具線 backlog 第 2 輪（r1 §6 候選的四個 task）

> 2026-09-14 立檔，緊接 [`KICKOFF-toolline-backlog-r1.md`](KICKOFF-toolline-backlog-r1.md)（r1 六個 task 已全部併入 main `1dd7008`）。
> 本輪從 r1 §6 的 18 條候選裡挑**工具線能直接動、有明確驗收**的四個；其餘延後條列在 §5。
> 制度照 r1：每個 task 一個子代理、一個 worktree、一個 commit；主對話只寫契約、merge、審核。**全程離線零計費。**

---

## 0. 給子代理的啟動提示

> 你在 repo `Calculus_handout` 的 `video/` 子樹做工具線的一個 task。先讀
> [`KICKOFF-toolline-backlog-r1.md`](KICKOFF-toolline-backlog-r1.md) §1（全域護欄，全部適用）＋本檔 §1（r2 補充），
> 再讀你被指派的那一節（§2.G–§2.J）。**先寫會紅的測試，再讓它綠**；只改契約列的檔；一個 commit；回報照 r1 §4 格式。

---

## 1. r2 對 r1 §1 的補充（r1 教訓）

1. **scratchpad 各自子目錄**：所有產物放 `<scratchpad>/task<X>/`，不要放根目錄（r1 六個 task 共用根目錄互撞過檔名）。
2. **背景長工作寫成單一 Python 驅動器**，不要 `bash "<path>.sh"`（r1 實測那種形式偶發啟兩份 process tree）。
3. **證據條款的措辭**：「sizecheck error 仍 0」只對正典 deck（`ch01_inverse_functions`／`ch03_trig_derivatives{,_mimo}`／`ch03_chain_rule`）成立；
   `_demo_*` fixture 既有 30 條**刻意** error，驗收標準＝「fixture 的刻意 error 與基線逐字相同」。
4. **同一 worktree 不並行兩支會編 Tex 的東西**（`make.py` 內建 sizecheck preflight 也算一支）；跨 worktree 不受限。Task H 落地後這條由鎖接管。
5. 23 deck 三份報表的比對用 **finding 級**（只比 `WARN`／`ERROR`／`[schema|lint|sizecheck]` 行），manim 的 Tex cache log 是噪音。
6. 本輪起點＝main **`ca7276b`**（或更新）；開工先 `git merge main`。

---

## 2. Tasks

### 2.G — hung 列的底邊夾制（r1 §6 ⑫ ⭐；派 **opus**；tag `[hung-clamp]`）

**現況（已核）**：r1 Task E 的 `_rail_plan` 讓放不下的列把 reason 掛在等式下一行（`derivation.py` 的 `hung`／`HANG_GAP = 0.18`）。
`derivation.build` 最後用 `_common.place_body(content, body_ref, left_x)`（:526）放整條 chain；`_common._biased_y`（:113）對「太高」的內容
**刻意 top-anchor 讓它溢出下緣**（docstring：overflow flagged elsewhere），`fill_gap`（:476）只縮 spread 不縮 `_ROW_GAP`。
結果＝§3.1 場 04 `difference_quotient_for_sine` 的 hung reason 越下緣安全線 0.23u（≈28 px），貼近右下品牌波形
（sizecheck `block 'result' spills past the safe margin (… y[-3.68,-2.21] vs safe ±6.56/3.45)`；gate 1 advisory A1 78）。

**目標**：含 hung 列的 chain，**當「沒有 hung 時本來放得下」**，就不得越下緣安全線。做法由你在下列約束內擇定並寫進 `DESIGN.md` derivation 節：
- 不得新增字級、不得改 `_SCALE_PX`、不得動 `_ROW_GAP`／`MIN_PITCH`（容量契約）、不得破 r1 Task E 剛立的 `MIN_LEADER` 保證與 `RIGHT_SLACK`。
- 可動：`HANG_GAP`（含縮到 0）、hung reason 的落點（例如貼齊等式底線右對齊、或塞進該列與下一列之間的既有 gap）、chain 的 spread（`fill_gap` 的上限）、
  hung 列與其相鄰列的 gap 分配。
- 對 r1 E 實測「逐列不變」的 **25 個 derivation 場零改變**（用 r1 E 的方法：逐場 rail 幾何 dump 比對）。

**紅測試先行**：`pipeline/_selftest_derivation_hung.py`（新）：① 構造一條 4 列、其中一列 hung 的 chain，未 hung 版本放得下 → hung 版本所有 mobject 底緣 ≥ 下緣安全線；
② hung reason 仍不與其等式、與下一列重疊；③ 無 hung 的 chain 逐 mobject 座標與改前相同（把改前座標寫進 fixture）。

**改哪些檔**：`pipeline/templates/derivation.py`（必要時 `pipeline/templates/_common.py`，但 `place_body` 的其他呼叫者行為不得變——列出全部呼叫者並各附一句證據）、新 selftest、`DESIGN.md`。

**證明**：23 deck 報表：schema／lint 逐字相同；sizecheck 正典 deck error 0、**`ch03_trig_derivatives{,_mimo}` 那條 result spills warn 消失**、其餘 warn 逐字相同、fixture 刻意 error 逐字相同；
mock render 場 04、14、21、22 改前後幀（scratchpad/taskG），`visual-frame-audit` 四場 blocking 0；`run_selftests` 全綠記支數。

### 2.H — `sizecheck` TeX 建置段的 per-cwd 檔案鎖（r1 §6 ⑱ ⭐；派 **opus**；tag `[tex-lock]`）

**現況（已核）**：`sizecheck.check_scenes`（:979）逐場 `build_blocks` 會經 manim 編 Tex 到 `./media/Tex`（相對 cwd）；`make.py` 在 render 前**內建一次同樣的 preflight**（:1066–1078）。
同一 cwd 內兩支同時跑（背景 `sizecheck.py` ＋ 前景 `make.py`，或兩支報表）會撞出**假的** `ERROR … could not build scene (…dvi…)`（§3.2 session 2026-09-14 實測 3 條；r1 Task C 也撞到）。
文件叮嚀擋不住看不見的那一支。

**目標**：在 Tex 建置段加 **per-cwd 互斥鎖**，讓第二支**等待**而不是吐假 error：
1. 鎖檔＝`<media_dir>/Tex/.lock`（跟著 `config.media_dir`，所以跨 worktree 天然不互斥）；用 `os.open(O_CREAT|O_EXCL)` 原子建檔＋內寫 pid／時間；
   拿不到就每 0.5 s 重試；**逾時（預設 10 分鐘）或鎖檔過舊（mtime > 15 分鐘且 pid 不存在）視為 stale，覆蓋並印 `[texlock] stale lock from pid N removed`**。
2. **命中面補充（§3.2 session）：`critic.py`（`graph_label_geometry` 走 templates build）、`rewatch_pack.py`、`derived_check.py` 等獨立入口凡會建 TeX 都要包鎖；selftest 不包（runner 已序列化）。**
   鎖的範圍＝一整支程式的「會編 Tex 的段落」（`check_scenes` 全程；`make.py` 的 preflight 與 render 各自持鎖），不是每個 Tex 一次（那會讓兩支交錯、Tex cache 仍會互寫）。
   放在共用 helper `pipeline/texlock.py`：`with tex_lock(reason="sizecheck"):`。
3. 等待時每 10 s 印一行 `[texlock] waiting for pid N (sizecheck) … 20s`，讓使用者知道不是掛住。
4. 不依賴新套件（不裝 `filelock`）；Windows 與 POSIX 都要能跑（pid 存活檢查兩平台各一行）。

**紅測試先行**：`pipeline/_selftest_texlock.py`（新）：① 兩個 `subprocess` 同時對同一 cwd 跑一支只做「拿鎖→sleep 2 s→寫 marker→放鎖」的小腳本，marker 時間戳不重疊；
② stale 鎖（手寫一個假 pid、舊 mtime）被回收；③ 逾時回 `TimeoutError` 帶清楚訊息。**再一條整合測試**：兩個 `subprocess` 同時對 `_demo_derivation.yml` 跑 `sizecheck.py`，
兩邊輸出都**沒有** `could not build scene`（改前先確認這條會紅——若你的機器改前跑三次都撞不出來，記錄下來、以 ①③ 為準）。

**改哪些檔**：`pipeline/texlock.py`（新）、`pipeline/sizecheck.py`（`check_scenes` 包鎖）、`make.py`（preflight 與 render 包鎖）、新 selftest、
`REVIEW_GATES.md` §一層 6 加一句、`KICKOFF-shared-layer-v1.md` §8 ⑧ 補「已由 texlock 接管」、`DESIGN.md` 建置一節加一小段。

**證明**：23 deck 報表逐字相同（鎖不改輸出）；`run_selftests` 全綠；整合測試輸出貼上。

### 2.I — 閘覆蓋補洞：provenance 與 step_coverage 都看不見 `procedure_steps`（r1 §6 ①②；派 **opus**；tag `[gate-coverage]`）

**現況（已核）**：
- `provenance._present_text_fields`（:131）掃 `statement／problem／body／reason／prompt／strategy／scaffold.*／annotations／points／steps[].reason／lines[].reason／result.reason／check.reason／notes[].text`，
  **不掃 `procedure_steps` 的 `steps[]` 本文**（`templates/procedure_steps.py:62` 起把每個 step 以 `brand.prose` 上畫面）→ 確定性 OF2 對該模板等於空的
  （§3.2 `decomposition_strategy` 整場沒有 `ref:` 也沒被報，是手動補的）。
- `step_coverage._SCOPED_TEMPLATES`（:17）＝`{theorem_proof, derivation, worked_example}`，不含 `procedure_steps`／`definition_math` → Strategy 3.1 的五步不受 SC 閘保護（§3.2 因第 5 步沒上畫面吃過一條 PD1 blocking）。

**目標**：
1. `_present_text_fields` 加 `procedure_steps` 的 `steps.i`（字串或 dict 的 `text`／`prose` 欄——先看模板實際讀哪個 key，照模板）；`worked[]` 是數學不算。
2. `_SCOPED_TEMPLATES` 加 `procedure_steps`。**〔2026-09-14 主對話裁決，取代下文「由你判斷」：本輪不加 `definition_math`〕**——§3.2 session 實測納入會讓 `ch03_chain_rule`（已開 `meta.coverage_enforce`）多命中 7 個單元（`why_composition_is_missing`／`rates_multiply_intuition`／`leibniz_form`／`proof_strategy_bridge`／`remainder_form_definition`／`toward_section_3_3`／`decomposition_strategy_repeat`），需另一輪補契約；`procedure_steps` 只命中 `decomposition_strategy`，§3.2 會自補 `screen_contract`（Strategy 3.1 第 5 步曾因 SC 看不到 `procedure_steps` 而漏上畫面、吃過 PD1 blocking——此即 I 的驗收案例）。分析留當 r3 候選。原文：`definition_math` 要不要加由你判斷：讀 `_screen_contract.required_steps` 對 `definition_math` 單元會產出什麼；
   若 definition 單元根本沒有 required steps 就不加、寫明理由；若有且合理才加。
3. **對現有正典 deck 跑 `schema.py`（含 SC）看新增了什麼**：新 finding 逐條列出、判「真缺口」或「規則過寬」。**真缺口不准改 deck**（`ch03_chain_rule*` 是 §3.2 session 的檔；
   `ch03_trig_derivatives*` 是 §3.1 的）——記進回報給主對話轉交；規則過寬就縮規則。SC 的嚴重度維持現行 `enforce` 旗標邏輯，不升級。

**紅測試先行**：既有 `_selftest_provenance*`／`_selftest_step_coverage*`（找現有的那支）各加：① `procedure_steps` 場的 `steps.0` 出現在 present fields；
② `procedure_steps` 場的 required step 未被 `covers:` 蓋到 → `[SC1]`；③ 一個非 scoped 模板（如 `callout`）仍不受 SC。

**改哪些檔**：`pipeline/provenance.py`、`pipeline/step_coverage.py`、對應 selftest、`REVIEW_GATES.md` §一 provenance／SC 兩列、`CONTENT_METHODOLOGY.md` §5 OTF 段若列了模板清單就同步。

**證明**：23 deck 報表——lint／sizecheck 逐字相同；schema 差異逐條列（provenance／SC 新 finding）並分類；`run_selftests` 全綠。

### 2.J — sizecheck sibling 字級閘恆空＋`_demo_worked_example` 拆壓測場＋floorprobe 全 deck 首跑數據（r1 §6 ⑤⑪⑥；派 **sonnet**；tag `[sizecheck-siblings]`）

**現況（已核）**：
- `sizecheck.py:79–80` `carriers = [n for n in nodes if isinstance(n, Text) or (isinstance(n, Tex) and not isinstance(n, MathTex))]`——此版 manim **`Tex` 繼承 `MathTex`**
  （`tex_mobject.py:607`；同檔 `_effective_font_px` docstring 自己也這樣寫），第二個條件永遠 False，sibling 字級比較只收 `Text`，而 Route A 之後畫面上已無 `Text` → 閘等於空跑。
- `_demo_worked_example.yml` 含刻意超量的 `capacity_over` 場（2 條 SIZE error），所以這個 demo deck 永遠要 `--skip-sizecheck` 才 render 得動；`_selftest_worked_example.py:41` 的 `_FIXTURE` 指著它。
- r1 Task B 的 `[floorprobe]` 只在三場實跑過；`^`／`_` marker 是否會在全 deck 放大聲量（§6 ⑥）沒有數據。

**目標**：
1. 把 carriers 的條件改成真正的意圖（prose `Tex`，排除純 `MathTex`——注意 `Tex` ⊂ `MathTex` 的順序陷阱，比照 `floorprobe._effective_px` 的寫法），讓 sibling 閘活過來。
   **這是行為改變**：23 deck sizecheck 可能多出 sibling 字級 warn／error——逐條列出並判真偽；若出現**正典 deck 的新 error**，先降為 warn 並在回報說明（主對話裁決是否升回）。
2. `_demo_worked_example.yml` 拆成兩個 deck：`_demo_worked_example.yml`（乾淨、`make.py` 跑得完）＋`_demo_worked_example_over.yml`（只放 `capacity_over`，刻意 error）；
   `_selftest_worked_example.py` 的 fixture 指向依測試意圖分配；deck 數 23→24（`README.md`／`DESIGN.md` 若列 demo deck 清單就同步）。
3. **數據**：在你的 worktree 對 `ch03_trig_derivatives` 全 deck跑一次 `python video/make.py --storyboard video/storyboards/ch03_trig_derivatives.yml --backend mock --quality low`
   （27 場，約 15–25 分鐘；同一 worktree 不並行別的 Tex 工作），把 `[floorprobe]` 全部輸出存 `scratchpad/taskJ/floorprobe_s31.txt`，統計：DIRECT 幾條、INNER 幾條、INNER 裡由 `\tfrac`／`\frac`
   觸發幾條、只由 `^`／`_` 觸發幾條、hook 來源幾條。**不改 floorprobe 的 code**——數據交主對話裁決 §6 ⑥。

**紅測試先行**：在既有 sizecheck selftest（找 sibling／prose size 那支）加：① 一個 prose `Tex` 列被縮小 → sibling warn 出現（改前紅）；② 純 `MathTex` 列不被當 carrier。

**改哪些檔**：`pipeline/sizecheck.py`（只那一行＋註解）、兩個 demo deck、`_selftest_worked_example.py`、對應 sizecheck selftest、`README.md`／`DESIGN.md`（demo deck 清單，若有）。

**證明**：24 deck 報表——schema／lint 逐字相同（新 deck 除外）；sizecheck 差異逐條列（sibling 閘新 finding＋fixture 拆分）；`run_selftests` 全綠；`_demo_worked_example` 不帶 `--skip-sizecheck` 跑完 `make.py`。

---

## 3. 主對話的驗收與 merge 流程

同 r1 §3：逐一看 diff 限契約檔、測試數字、抽查幀；merge 順序 **J → I → H → G**（G 動 derivation.py 幾何，最後；H 動 sizecheck／make.py 的外殼，先於 G）；
每次 merge 後 `run_selftests`；全部併入後 main 對起點跑 23（24）deck finding 級 diff，逐條對六份回報；`REBUILD_STATUS.md` 記本輪。

## 4. 回報格式

同 r1 §4。多一項：**產物路徑一律在 `scratchpad/task<X>/` 下**。

## 5. 本輪不做（r1 §6 其餘）

- ③ `procedure_steps` 不吃 scaffold＋`worked[]` 與 row.3 重疊 57%：模板層 polish，等 §3.2 Phase B 或 §3.3 真的需要時再做（§3.2 已用 `part:` 繞過）。
- ④ derive_spoken 慣例表：已開 chip，使用者決定何時跑。
- ⑥ floorprobe `^`／`_` 噪音：等 J 的數據再裁。
- ⑦ `companion_limit` 不可逐像素重現：§3.1 hook 側，低優先。
- ⑨⑩ §3.1 場 22／23 與場 04 hung tag：**§3.1 側**，另開 chip（含 G 併入後的場 04 複驗）。
- ⑬ off-rail 列左緣分裂 22 px：需要別的設計，留。
- ⑮ reason 內嵌 `\tfrac` 低於 floor：J 的數據會涵蓋。
- ⑯⑰ text_metrics 短字串比例、`_WIDTH_K` bold：記錄性質，不做。
- motion-language-gaps §8 其餘（`{{}}` 段級 role、palette 撞色、graph sweep leave、scene_head 清點）：等有場需要或使用者看幀裁決。

---

## 6. 本輪進行中收到（r3 候選與驗收數據）

- **⭐ `_screen_contract.parse_block` fail-closed 靜默失效**（§3.2 session 2026-09-14 實踩）：`yaml.YAMLError`／非 dict／空一律回 `None`，一個 YAML 語法錯（雙引號 `tex:` 裡的 `\c`）
  就讓整份 `screen_contract` 從閘視野消失，enforce 下吐 `has no screen_contract` 把人導向「去寫一份」。解＝解析失敗印成獨立 `[SC] <unit>: screen_contract failed to parse -- <err>`
  ＋負向 selftest（含非法轉義的契約不得被當成「沒有契約」）。**已追加給 Task I**（若 I 已 commit 則為 r3 首項）。
- **Task I 的驗收數據（§3.2 session 提供）**：其分支 `30c5358` 補了 `decomposition_strategy` 的 `screen_contract`（7 條 required_steps，兩個 `part:` 場 covers 4＋3；契約 10→11、required 29→36）；
  模擬 `_SCOPED_TEMPLATES` 加 `procedure_steps` 後 `ch03_chain_rule{,_mimo}` 1 error → 0；全 repo 24 份 storyboard 零新增 error。
