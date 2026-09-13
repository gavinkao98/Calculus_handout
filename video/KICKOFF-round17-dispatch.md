# KICKOFF — 品質補強輪 ⑱（檔名沿用 round17）：色軸統一＋鋪滿輪 backlog 派工（2026-09-13）

> **啟動提示（新對話直接貼）：** 讀本檔＋[`KICKOFF-motion-language-rollout.md`](KICKOFF-motion-language-rollout.md) §5／§7＋根目錄 `CLAUDE.md`「任務分派」一節。
> 本輪是第一輪照「主模型只做拍板／審核／難題，簡單任務派 sonnet／haiku、獨立項目開新對話」做的：四個 task 各一個 sonnet 子代理在 worktree 做，主模型只 merge＋審核；worked_example 模板開成新對話的 chip。

## 0. 裁決（使用者，2026-09-13）

1. **色軸照 11／18／24 的定：** 藍 `secondary`＝cos、琥珀 `accent`＝sin、綠 `success`＝斜率／加速度／tan；θ 物件（弧、扇形）維持色表 `concept` 赭。**08 改掉**（06／07 跟著對齊）。已知取捨：accent 與 concept 色相相近，θ 弧旁的 sin 半弦要靠明度分辨；若要拉開只能換 θ 的色（下一個裁決點，本輪不動）。**→ 同日第二次裁決：θ 物件與 token 全改 `strategy` 紫**（幀證實琥珀／赭疊在一起分不出來），Sonnet 子代理 `5fd41c8`。
2. **派工制度：** Fable 5.1 只做拍板、決策、審核、困難任務；簡單任務派適合的模型（sonnet 做 code／hook／文件，haiku 做純文字整理）；獨立項目開新對話（`spawn_task` chip），避免單一對話把上下文撐滿。已寫進 `CLAUDE.md`。

## 1. 派工表

| # | 任務 | 模型 | 隔離 | 動的檔 | 驗收 |
|---|---|---|---|---|---|
| A | 色軸統一：08 sin 半弦／長條→accent、cos 腿→secondary、弧／`|θ|`→concept；06 內三角→accent、扇形→concept、外三角 success 不變、evenness 半弦 +θ accent／−θ muted；07 三列 `seg_roles` 對應；DESIGN 色軸節加影片層物件色慣例 | sonnet | worktree | hooks（06／08 兩函式）、storyboard 場 07、`_mimo`、DESIGN | selftest 全綠；schema／sizecheck 逐字相同；三場 mock render 抽幀核色 |
| B | prose 行內 θ 吃色表：`Tex` 混排路徑（`math_line` 混排分支／`_prose_lines`／`heading_rich`）對 `$…$` 內命中 token 注入 dvisvgm `\special{color push/pop}`，建物件不傳 `color=`、建好後保留注入色、其餘補行色；fallback 單色 | sonnet | worktree | brand.py、`_selftest_color_map.py`、DESIGN、README | 新測試 4 條；sizecheck 幾何逐字相同；12 場 mock 抽幀 body 四個 θ 赭 |
| C | theorem_proof 的 proof dict 列 `seg_roles` 傳遞（`prose(..., seg_roles=)`）＋`schema._seg_roles_issues` 擴 theorem_proof | sonnet | worktree | theorem_proof.py、brand.py（只加參數）、schema.py、`_selftest_proof_transform.py`、DESIGN | 新測試；零行為改變 |
| D | 場 23 `shm_device` hook（R2 must：彈簧與重物沒畫）：裝置在列右側，重物隨 `s=sin t` 擺、step.1 加速度箭頭藍、step.2 加速度箭頭綠永遠指向平衡線、result 位移琥珀，場尾淡出；旁白零字不改、不加 marker | sonnet | worktree | hooks（新函式）、storyboard 場 23 `hook:`／`exit:`、`_mimo` | schema／lint／sizecheck 0 error；mock render 四幀自檢；selftest 全綠 |
| chip | `worked_example` 影片模板（另一 session 交接檔「未認領」第一優先；設計畫布在 `_audit/design-template-system/`） | 新對話 | 新 worktree | 新模板檔、registry、demo、selftest | 見 chip prompt |

主模型（本對話）：審 A–D 的回報與幀、merge、解衝突、跑 main 的 selftest／smoke 對照、記 REBUILD_STATUS ⑱（另一 session 的 Task D 已用 ⑰）。另一 session（`calculus-handout-a7`）正在 main 做 Task D（計費改稿＋重 render），hooks 檔有它的 dirty hunk：A／D 的 merge 等它 commit 後做。

## 2. 不做（本輪）

- θ 換色（第二個裁決點）；09 hook（另一 session 已做，`eb0d203`）；06 主圖放大；`[stillness]` 對 theorem_proof transform 列的補法（等 B／C 落地後看 R2）；carry 角落複本「只帶 eq」選項（等使用者看片）。

## 3. 驗收與 DoD

A–D 各自 commit 合進 main、`run_selftests` 全綠、`doctor --smoke` 與 ⑯ 收尾逐字相同、正典 deck schema／sizecheck 0 error；A／B／D 的幀由主模型抽查；全片重 render 由另一 session 的 Task D 收尾一起做（避免兩份成片互相覆寫），之後六鏡再審。`REBUILD_STATUS.md` 記 ⑱。

## 4. 結果

（執行中，2026-09-13）A 色軸 ✅ `c5dd432`→再裁 θ 紫 ✅ `5fd41c8`；B prose θ ✅ `24536f9`；C seg_roles proof ✅ `44ed099`；D 23 彈簧 ✅ `ff8c3d1`（＋拿掉 23 的 indicate，`54e2008`）；另一 session：09 ✅ `3621597`、pack fine 定位 ✅ `e2a29de`；**04 覆蓋層（Opus）進行中**。main 閘：selftest 40/40、schema OK、sizecheck 0 error。合併版 render 待 04 合併後由另一 session 跑。
