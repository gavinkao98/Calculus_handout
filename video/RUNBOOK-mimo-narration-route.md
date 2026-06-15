# Runbook — MiMo 旁白雙版／影片路線（指派給單節 session 用）

> 這是「最新方法」的可貼提示詞。把下方 fenced 區塊整段貼給負責**某一節**的 session，
> 填入該節的 `DECK` / `SECTION`。權威細節：`video/README.md` §「MiMo 旁白／影片路線」、
> `video/DESIGN.md` §「MiMo 口語軌」、`video/REBUILD_STATUS.md` 2026-06-14 節。

**前提（重要）：** 此路線需要該節的**正典 storyboard** `video/storyboards/<deck>.yml`（含 `say` ＋ `{show}`）。
目前只有 §1.1（`ch01_inverse_functions`）、§1.6（`ch01_precise_limit`）有 storyboard；
§1.2/1.3/1.4/1.5 仍在「內容稿＋narration HTML、待認可、**尚無 storyboard**」階段——
那些節**先別跑本路線的影片步驟**，可先用下方「念法慣例」＋ Mode B 把口語版納入認可包，
storyboard 落地後再走完整流程。

---

```
你負責 NTU 微積分影片產線（repo Calculus_handout，video/ 子樹）某一節的「MiMo 旁白雙版／影片」產出。
全程用繁體中文溝通；動手前先讀 video/README.md §「MiMo 旁白／影片路線」、video/DESIGN.md §「MiMo 口語軌」、
該節 content_scripts/<deck>.md 與 storyboards/<deck>.yml。

DECK: <填，如 ch01_precise_limit>      SECTION: <填，如 §1.6>

步驟 0（前提檢查，先做）：
- 確認 storyboards/<deck>.yml 存在（含 say + {show}）。不存在就停手回報——本路線在 storyboard 落地後才跑
  （旁白須先認可 → 出 storyboard）。

步驟 1 — 寫口語單一源 content_scripts/<deck>.spoken.yml：
- 每個 content scene 一筆 `scene_id: | <口語旁白>`；把該 scene 已認可 narration 的英文散文「逐字保留」，
  只把每個 LaTeX 數學式攤成口語，並把 {show ...} 標記留在與正典 say 相同的位置（順序/目標一致）。
- 念法慣例（務必遵守）：
  · f^{-1} → "f inverse"（絕不 "f to the minus one"；例外：課文刻意對比 sin^{-1} 與 1/sin 時，該處照字面念）
  · 下標 x_1,x_2 → "x sub one / x sub two"
  · 和/差根號 √(y-2) → "the cube root of the quantity y minus two"
  · 群組次方 (∛(x-2))^3 / (f^{-1}(x))^2 → "…, all cubed / all squared"
  · 座標 (a,b) → "the point with coordinates a and b"；區間 [a,b] → "the interval from a to b"
  · 反三角 arcsin → "arcsine of …"；π/2 → "pi over two"；分數念 "one half / nine-fifths" 等
- 只改數學念法，不動英文散文用詞。

步驟 2 — 生成＋parity 檢查（不呼叫任何 API）：
  python video/pipeline/derive_spoken.py --deck <deck> --check   # 必須印 "parity OK"
  python video/pipeline/derive_spoken.py --deck <deck>           # 生成 _mimo.yml + _narration_spoken.md
  （這兩個生成檔標 DO NOT EDIT；要改旁白改 .spoken.yml 後重生。）

步驟 3 — Mode B（codex 稽核，read-only）：
- cp content_scripts/_audit/PROMPT-narration-modeB.template.md → _audit/PROMPT-<deck>-narration-modeB.md，填 {{...}}。
  該節旁白「尚未經使用者認可」就把 CONTENT_APPROVED 設為 no（會打開 D7 數學內容正確性維度）。
  codex exec -s read-only < video/content_scripts/_audit/PROMPT-<deck>-narration-modeB.md \
      > video/content_scripts/_audit/REPORT-<deck>-narration-modeB.raw.txt 2>&1
- 收斂：依 Keep/Rewrite/Cut 改 <deck>.spoken.yml → 重跑 derive --check → 回歸審核 →
  寫乾淨的 REPORT-<deck>-narration-modeB.md。Mode B 裁決寫進該次修正 commit 的 message body（CLAUDE.md）。

步驟 4 —（須先徵得使用者同意：MiMo 雖免費仍屬外部 API）合成＋render：
- 確認 .env 有 MIMO_API_KEY。先 smoke（mimo_preview.py --smoke）確認回應形狀，報用量、徵同意後：
  python video/pipeline/tts.py  --storyboard video/storyboards/<deck>_mimo.yml --backend mimo --voice Mia
  python video/make.py          --storyboard video/storyboards/<deck>_mimo.yml --reuse-audio --quality high
  → output/chNN/sX.Y/<deck>_mimo.mp4（1080p 預覽；正式交付才 --quality 4k）
- `make.py --reuse-audio` 會先驗 manifest freshness（deck id、scene、beat count、`{show}`、
  `text_hash`、WAV 存在/時長），再 render；若報 stale/incomplete，不要硬跳過，先重跑該 storyboard
  的 `tts.py` 或確認是不是選錯 `<deck>_mimo.yml`。
- 若出現 `[sync] short/reveal-only beat warning`，通常是連續 `{show a} {show b}` 或短空 beat；
  優先把其中一個 reveal 合併到有旁白的 beat，或接受它作為 deliberate visual pause。
- render 後 `[sync] render/audio lengths clean` 最好要出現；fatal mismatch 代表 narration 可能超過
  video，先不要 compose/交片。
- 驗收：在幾個 reveal beat 的時間點抽幀，確認 reveal 準時出現＋LaTeX 無亂碼（光看 exit code 不夠）。

規則：
- MiMo 非決定性——同文字每次合成是不同 take（±~10% 長度）；滿意的 take 不要重合成。
- 不要編輯生成檔（_mimo.yml、_narration_spoken.md）；改 .spoken.yml 重生。
- 未經要求不要 commit。任何計費/外部 API 呼叫前先報用量徵同意（CLAUDE.md）。
```

---

**只想聽聲音（不出影片）：** `python video/pipeline/mimo_preview.py --spoken content_scripts/<deck>_narration_spoken.md`
（`--dry-run` 不呼叫 API；`--smoke` 只合首段）。
