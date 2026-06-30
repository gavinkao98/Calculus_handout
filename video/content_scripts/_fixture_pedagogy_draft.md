# _fixture_pedagogy_draft — pedagogy-firstlearner calibration content script (DRAFT, test-only)

> **階段：** DRAFT（fixture；`CONTENT_APPROVED=no`）。本檔是 `pedagogy-firstlearner` 閘**生命週期**校準的「未核准源」(draft deck `pedagogy_audit_draft.yml` 的 `md:<unit>` ref 解析於此)。因 deck 級 `CONTENT_APPROVED=no`，凡 OF finding 一律 dry-run／advisory、永不 blocking（見 rubric §生命週期）。唯一單元 `unit_draft` 的 prose 刻意造得窄，好讓 draft storyboard 的上畫面文字「超出源」。

### unit: unit_draft
```
id: unit_draft
source: fixture (narrow draft claim — single limit, not yet approved)
learning_goal: 草稿階段只先陳述 lim_{θ→0} (sin θ)/θ = 1 這一個極限
kind: content
narration: |
  草稿：(sin θ)/θ 在 θ → 0 的極限等於 1。這一版只先放這個極限值本身，
  尚未補上餘弦那條 (1 − cos θ)/θ → 0，也還沒寫導數結論。內容未定、待核。
visual_need: 單一極限式
animation_cue: 淡入極限式
```
