# Runbook — MiMo 旁白雙版／影片路線（指派給單節 session 用）

> 這是「最新方法」的可貼提示詞。把下方 fenced 區塊整段貼給負責**某一節**的 session，
> 填入該節的 `DECK` / `SECTION`。權威細節：`video/README.md` §「MiMo 旁白／影片路線」、
> `video/DESIGN.md` §「MiMo 口語軌」、`video/REBUILD_STATUS.md` 2026-06-14 節。

**前提（重要）：** 此路線需要該節的**正典 storyboard** `video/storyboards/<deck>.yml`（含 `say` ＋ `{show}`）。
目前 `storyboards/` 僅存 `_demo_*.yml`（模板示範／回歸樣本），**無任何正典章節 storyboard**——
舊 ch01_* 練習已於 2026-06-16 全數廢棄、將從講義逐節重跑。故任一章節節在**該節 storyboard 落地前
先別跑本路線的影片步驟**；可先用下方「念法慣例」＋ NFA（旁白忠實稽核，原 Mode B）把口語版納入認可包，
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

步驟 3 — NFA 旁白忠實稽核（原 Mode B；read-only）：
  契約＝ content_scripts/_audit/NARRATION-FAITHFULNESS-RUBRIC.md（維度 D1–D7、收斂線、reader 拆法）。
  gate1（Claude subagent，免費）迭代到 blocking==0：1 個 narration reader 跑 D1–D6；CONTENT_APPROVED=no 時
  另開 1 個隔離盲 reader 跑 D7（獨立重算）。收斂後再跑 gate2（Codex，計費、需同意）單次確認。
- cp content_scripts/_audit/PROMPT-narration-faithfulness.template.md → _audit/PROMPT-<deck>-narration-faithfulness.md，填 {{...}}。
  該節旁白「尚未經使用者認可」就把 CONTENT_APPROVED 設為 no（會打開 D7 數學內容正確性維度）。
  gate2 範例：codex exec -s read-only < video/content_scripts/_audit/PROMPT-<deck>-narration-faithfulness.md \
      > video/content_scripts/_audit/REPORT-<deck>-narration-faithfulness.raw.txt 2>&1
- 收斂：依 Keep/Rewrite/Cut 改 <deck>.spoken.yml → 重跑 derive --check → 回歸審核 →
  寫乾淨的 REPORT-<deck>-narration-faithfulness.md。NFA 裁決寫進該次修正 commit 的 message body（CLAUDE.md，`git log --grep="NFA"`）。

步驟 4 —（須先徵得使用者同意：MiMo 雖免費仍屬外部 API）合成＋render：
- 確認 .env 有 MIMO_API_KEY。預設走 `mimo-v2.5-tts-voicedesign` 的 `Calm Professor`
  prompt（中速、穩重美式教授聲線，`optimize_text_preview=false`，不讓平台改稿）。先 smoke
  （mimo_preview.py --smoke）確認回應形狀，報用量、徵同意後：
  python video/pipeline/tts.py  --storyboard video/storyboards/<deck>_mimo.yml --backend mimo
  python video/make.py          --storyboard video/storyboards/<deck>_mimo.yml --reuse-audio --quality high
  → output/chNN/sX.Y/<deck>_mimo.mp4（1080p 預覽；正式交付才 --quality 4k）
- **合成單位 `--unit`（scene-level TTS＋forced alignment，2026-07-05；設計見 DESIGN.md「Manifest schema 2」）：**
  `tts.py` 預設 `--unit auto`——batch-1 template（`definition_math`／`graph`／`callout`／`recap_cards`）走
  scene-level（一場一次合成、`stable-ts` 回推 beat 時序、per-scene validation，過不了自動回退 beat），
  其餘（含 `derivation`／`theorem_proof`）暫走 beat。要全走舊路用 `--unit beat`；單一場強制 scene 用 `--unit scene`。
  **紀律：scene-level 真合成只在 narration lock＋NFA 之後**（「改一個字→整場重合成」的 blast radius 由 lock 吃掉）；
  lock 前一律 `make.py --backend mock`（beats、零計費、離線）迭代。scene-level 合成報價時**要把 §7 fallback retry 預算
  一併列入**（每場至多 2 次額外 call：resynth／chunk），核准即涵蓋、超出即停。
- `make.py --reuse-audio` 會先驗 manifest freshness（deck id、scene、beat count、`{show}`、
  `text_hash`、WAV 存在/時長；`scene_aligned` 另驗 scene WAV＋words/aligned 檔＋`validation.status`），再 render；
  若報 stale/incomplete，不要硬跳過，先重跑該 storyboard 的 `tts.py` 或確認是不是選錯 `<deck>_mimo.yml`。
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
（`--dry-run` 不呼叫 API；`--smoke` 只合首段）。要臨時回到內建音色試聽時，加
`--model mimo-v2.5-tts --voice Dean`（或 `Mia` / `Chloe` / `Milo`）。
