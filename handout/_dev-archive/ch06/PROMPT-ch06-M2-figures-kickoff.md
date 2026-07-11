# PROMPT — Ch6 M2 figure batch 接續（fresh session bootstrap）

> 整段貼進新 session。你要接續**微積分講義 Ch6（Integrals）的 M2 圖批次**：M1 全閘已完成、圖機會稽核（gate-1）已完成、`buildPlot` fill primitive 已加並驗證、**Figure 6.1 已繪成**。你的工作＝畫 **Figure 6.2–6.8**（7 張）＋跑視覺閘。

## 0. 先讀（依序）

1. `handout/_dev-archive/ch06/PLAN-ch06.md` — **首讀**；§「M2 figure batch」有 8 圖決定＋**逐圖 locus＋domain facts＋tier**（權威）；as-built 編號 ledger；各節 ⑤ 狀態。
2. `CLAUDE.md` ＋ `handout/CLAUDE.md` — 專案紀律（繁中對話；付費 API 先徵同意；Codex read-only 有 standing consent 逕行；改課文只改 `fragments/` 再 `build.py`；圖要改 fragment＋FIGS 兩處）。
3. `handout/PIPELINE.md` §「Canon 章 5-milestone」M2 列 ＋「gate-2 全跑」＋「render 自驗」。
4. `CONTENT_SPEC.md` §10（圖表與色彩：何時用圖、label economy、grayscale 冗餘編碼、placement、caption、worked-example 圖不洩答案）。
5. `handout/_audit/FIGURE-OPPORTUNITY-RUBRIC.md`（機會，已跑完）＋ `handout/_audit/FIGURE-AUDIT-RUBRIC.md`（**D1–D8 視覺正確性，你要跑**）。
6. **範本**：`handout/chapter6-print-standalone.html` 內 `const FIGS = { "riemann-lr-x2": …}`（Figure 6.1，抄它的寫法）＋其上方 `buildPlot`（含新加的 `rect`/`area` 分支）。ch05 更多 FIGS 範例在 `handout/chapter5-print-standalone.html`（`buildPlot` @1780、FIGS @1882）。

## 1. 現狀

- **branch**：`video/template-redesign-navy-spine`（使用者裁定續用；勿另開）。**尚未 commit**，全在工作樹。
- **M1**：§6.1–6.5 全數 Codex ⑤ 0 blocking＋sympy 29/29＋章層 review M1–M8 clean。as-built：Def 6.1–6.4／Thm 6.1–6.8／Strategy 6.1–6.2／Ex 6.1–6.16。
- **M2 gate-1**：圖機會稽核 done（4 subagent，§6.1–6.4）→ 8 圖 essential+strong 批次已決定（見 PLAN 表）。§6.5 無圖。
- **繪圖前置 done＋驗證**：`chapter6-print-standalone.html` 的 `buildPlot` 已加 **`rect`**（填色矩形：`{type:"rect",x1,x2,y1,y0,cls}`）＋**`area`**（曲線下填色：`{type:"area",fn,domain:[a,b],base,cls}`）item＋CSS fill classes（`.fill-area/.fill-pos/.fill-neg/.rect-lo/.rect-hi/.rect-sum`）。`build.py` 不動 `buildPlot`/CSS/FIGS（只換 content 區），故這些改動 persist。**Figure 6.1（`riemann-lr-x2`）已繪＋render 驗證正確**。

## 2. 任務：畫 Figure 6.2–6.8（reading order，連號不可跳號）

每張兩處同改：(a) `chapter6-print-standalone.html` 的 `FIGS` 物件加一個繪圖函數；(b) 對應 `handout/fragments/ch06/sec-6-N.html` 在該圖 locus 插 `<figure>` marker。

**繪圖 API**：`buildPlot(cfg)` → SVG 字串。cfg：`w,h,xmin,xmax,ymin,ymax,xlabel,ylabel,xticks:[{x,tex}],yticks:[{y,tex}],aria,items:[]`。item types：`curve{fn,domain:[a,b],samples,cls}`、`seg{x1,y1,x2,y2,cls}`、`vline{x}`、`hline{y,from,to}`、`dot{x,y,r,hollow}`、`arrow{x1,y1,x2,y2}`、`text{x,y,tex,anchor,vAnchor,dx,dy,cls,size}`、**`rect{x1,x2,y1,y0,cls}`**、**`area{fn,domain,base,cls}`**。**fill item 要放 items 陣列最前面**（先畫＝在曲線後方）。回傳 `{layout:"single"|"pair"|"triple", panels:[{svg,note}]}`；**note 用純文字**（MathJax 時序問題），數學 label 走 `text` item 的 `tex`。cls 常用：curve/tangent/refline/idline/bubble/dot/a-pt/a-ax＋新 fill classes。

**fragment marker 範式**（抄 Figure 6.1 的）：
```html
  <!-- expansion:figure [pass: enrichment] [source: figure-opportunity gate 2026-07-10 tier-<t> — <一句>; registered in chapter6 FIGS as "<id>"] -->
  <figure class="figure" data-fig="<id>">
    <figcaption><span class="fig-no">Figure 6.N</span> <說明，數學用 \(...\)>。</figcaption>
  </figure>
```

**硬約束**：① 圖只可視覺化**既有**內容（不新增數學）。② **D8 grayscale**：+/− 區、min/max 矩形要靠 **label＋色調/線型**區分，不可只靠顏色（正區 `fill-pos`＋"＋"標；負區 `fill-neg`＋"−"標＋虛線邊）。③ **label economy（§10）**：數值答案留在 Example／caption，不塞圖上。④ worked-example 圖不洩答案（但 Ex 全已解，低風險）。⑤ 只動 ch6 的 `buildPlot`（勿碰 ch1–5）。⑥ 連號：Figure 6.2 接在 6.1 後，依 reading order。

### 逐圖規格（權威在 PLAN；此處摘要 domain facts）

- **Fig 6.2 §6.1 refinement（`triple`）** — locus：Ex 6.1→Ex 6.2 之間（"The bracket will tighten as n grows"）。三 panel 右和 n=4,8,16 疊在 y=x² 上，gap 隨 n 縮；**勿標 "=1/3"**（那是 Ex 6.2 答案，no-spoiler）。panel note "n=4"/"n=8"/"n=16"。
- **Fig 6.3 §6.1 v–t 階梯（`single`）** — locus：Ex 6.3 或其後 unification 段。點 (0,0)(1,4)(2,7)(3,9)(4,10)(5,10)，Δt=1 階梯矩形（right sum 或 L&R）；**左和首格高 0、右和末兩格皆 10**；**離散資料——任何內插曲線畫虛線/soft，不可實線**（散文明說 modelling assumption）。訊息＝距離就是 v–t 圖下面積。
- **Fig 6.4 §6.2 號面積雙三角（`single`）** — locus：Ex 6.5。y=x−1 於 [0,2]，過軸於 x=1；[0,1] 在軸下（`fill-neg`＋"−"，三角面積 ½），[1,2] 在軸上（`fill-pos`＋"＋"，½）；net 0 vs total 1 進 caption。用 `area` fill（base=0，正負段分兩個 area item）或 seg 圍三角。
- **Fig 6.5 §6.2 min/max 夾擠（`single`）** — locus：Ex 6.6。√x 於 [1,4]（遞增、上凹）；m=1 於左端 (1,1)、M=2 於右端 (4,2)；inscribed 矩形 y=1（`rect-lo`）、circumscribed y=2（`rect-hi` 虛線邊）；只在端點碰曲線；面積 3、6 進 caption。
- **Fig 6.6 §6.3 累積 sliver（`single`，FTC-1 錨、最重要）** — locus："The accumulation function" 段。f>0；`area` 陰影 [a,x]=g(x)，另一 distinct 陰影薄片 [x,x+h]；**h 誇大、標 "not to scale"**；薄片高標 f(x)。軸標 a, x, x+h。
- **Fig 6.7 §6.3 證明夾擠（`single`）** — locus：FTC-1 Proof 的 trapping 步。[x,x+h] 上：inscribed 矩形高 m_h=min f（`rect-lo`）、circumscribed 高 M_h=max f（`rect-hi`）夾住真薄片；標 u_h,v_h（EVT 取到 min/max 處）；callout "as h→0, m_h,M_h→f(x)"；h>0、f>0。
- **Fig 6.8 §6.4 速度號面積（`single`）** — locus：Ex 6.12。v=t²−4 於 [0,3]（上開拋物線右半）：v(0)=−4、根 v(2)=0、v(3)=5；[0,2) 軸下（`fill-neg`＋"−"，面積 16/3=backward）、(2,3] 軸上（`fill-pos`＋"＋"，7/3=forward），兩區相接於 (2,0)；位移 −3 vs 路程 23/3 進 caption。

## 3. 閘序（每畫完一批或全部）

```bash
cd handout
python build.py ch06
node _render/linebreak-gate.mjs chapter6-print-standalone.html      # 自動斷 0
node _render/shot.mjs "file:///C:/Users/Kao/Downloads/Calculus_handout/handout/chapter6-print-standalone.html" <scratch>/ch6fig figures   # 每圖 2× PNG
# → 用 Read 工具逐一看 PNG 自檢（矩形有無碰對曲線、陰影區對不對、grayscale 可辨）
```
- 自檢修完 → **gate-1 D1–D8**：派 `handout-figure-audit` subagent（吃 render 後 PNG，依 FIGURE-AUDIT-RUBRIC 判 D1–D8 blocking/advisory）→ 修 blocking → 回歸。
- **gate-2（每章必跑，2026-07-10 全跑政策）**：Codex 視覺第二讀者餵 PNG。指令試 `codex exec -s read-only -C <repo> -i <png> - < <prompt>`（**先確認此版 codex 支援 `-i` 圖片輸入**；0.144.1 若不支援，改用 dedicated VLM 需先徵同意，或記錄降級）。收到 0 blocking。
- **產物**：`handout/_audit/REVIEW-ch06-figure-opportunity.html`（機會決定＋8 圖表）＋ `REVIEW-ch06-figure-audit.html`（render 圖＋D1–D8＋gate-2 結果）。findings 摘要轉錄 `handout/_dev-archive/ch06/ch06_figure-audit.md`（raw 不進版控）。
- **收尾**：更新 PLAN「M2 figure batch」狀態＋各 sec header 的 Figure ledger 註解＋PLAN 編號 ledger（Figure 6.1–6.8）；PIPELINE dashboard 的 Ch6 圖欄留待 M5。

## 4. 之後（M3–M5，不在本 prompt 範圍，但記著）

M3 散文 S·A·V＋難度 learner-sim（≥3 盲測）合一輪 → M4 Mode C gap-check → **三閘 gate-2 全跑**（數學/散文/圖，M4 後批次）→ M5 收尾（PIPELINE dashboard＋ROADMAP）。閘序權威＝`handout/PIPELINE.md`。

## 5. 紀律速記

- Codex／subagent read-only 有 standing consent，逕行、不逐次問（使用者 2026-07-06＋本輪重申）。真 TTS／高解析算圖／VLM 等**計費**才先徵同意。
- Karpathy：外科手術式改動、比照既有風格、每行改動可回溯到任務。圖畫錯就靠 D1–D8＋gate-2 抓、迭代到 0 blocking。
- commit 經授權才做；繁中、body 逐條記裁決、結尾 `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`。
- **起手**：讀 §0 檔 → 開 `chapter6-print-standalone.html` 找 `FIGS`（抄 `riemann-lr-x2` 樣式）→ 畫 Fig 6.2 → build+render+看 PNG → 逐張推進 → 全畫完跑 D1–D8＋gate-2。
