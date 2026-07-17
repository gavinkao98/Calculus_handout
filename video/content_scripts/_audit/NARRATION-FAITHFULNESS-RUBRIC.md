# 旁白忠實稽核 — 維度與收斂線（NARRATION-FAITHFULNESS-RUBRIC / NFA）

> 本檔是「旁白忠實稽核（Narration Faithfulness Audit, **NFA**）」的契約與**單一真相來源（single source of truth）**。NFA 的兩道讀者——**gate 1（Claude subagent，免費）** 與 **gate 2（Codex 獨立第二讀者，計費）**——都讀本檔判斷；維度／收斂線**只在這裡改一次**，prompt 只「引用」不「複述」（防漂移）。
>
> **血統（lineage）：** NFA ＝ 原 video「Mode B」（審訂審查）。為解「與講義 Mode B 同名異義」的命名衝突而於 2026-06-15 改名；維度 D1–D7 **原封不動**沿用。舊 git 史用 `git log --grep="Mode B"`、本線改用 `git log --grep="NFA"`。**注意：** 講義的 Mode B（走 `<!-- expansion: -->` marker、Keep/Rewrite/**Move**/Cut、權威在 [`../../../CONTENT_AUTHORING_WORKFLOW.md`](../../../CONTENT_AUTHORING_WORKFLOW.md)，2026-07-07 自根 README 遷出）是**不同產物的不同閘**，與本檔無關。
>
> 方法論與資料流的**權威規範**見 [`../../CONTENT_METHODOLOGY.md`](../../CONTENT_METHODOLOGY.md)（§4 旁白為「說」而寫、§7 內容層品質檢核）、[`../../DESIGN.md`](../../DESIGN.md)（MiMo 口語軌、derive parity）。本檔只定「審哪些維度、哪些擋稿、哪些不算 finding、怎麼回報、開幾個 reader」，**不重述**方法論本身。

## 審查對象與邊界

NFA 在**鎖稿後**跑（旁白 source 已認可、已 derive）。從同一份 narration source 衍生的雙版本：

1. **Source narration（`<deck>.md` 的 `narration:` 欄）** — 英文＋inline LaTeX。是否已使用者認可 ＝ `CONTENT_APPROVED`（yes/no）。
2. **Version A — HTML 閱讀版（`<deck>_narration.html`）** — 經 MathJax 渲染數學。
3. **Version B — 口語版（`<deck>_narration_spoken.md`）** — 每個 LaTeX 攤成口語英文（無符號），供不能讀 LaTeX 的 TTS。

三件全讀。intro／outro 等**靜音單元無 narration，不審**。

- **審**：source → 兩個衍生版本的**忠實轉換**、口語數學念法的**等價與無歧義**、口語**順耳**、以及數學內容**正確**（D7，條件式）。
- **不審**：已認可 source 的教學內容／教學法（`CONTENT_APPROVED=yes` 時不得 re-litigate；但仍可在發現明顯數學錯時觸發 D7）。冗餘／贅字屬**鎖稿前** copyedit 的事（見 [`NARRATION-COPYEDIT-RUBRIC.md`](NARRATION-COPYEDIT-RUBRIC.md)）——NFA 鎖稿後**不動措辭**（去重會被當成 D2 違規）。

## 審查維度（D1–D7；每條標 Blocking / Advisory）

**D1 — Version A（HTML）忠實。** 每個單元 narration 與 source 逐字一致（markdown `*x*` → `<em>x</em>` 可）；無漏字／加字／改字；LaTeX 可渲染、無 malformed；kind 徽章正確；單元齊全、id／順序正確。

**D2 — Version B（口語）忠實。** 英文散文與 source **逐字等同**，只把數學記號攤成口語字；任何 paraphrase／漏／加／更動教學內容 → flag。

**D3 — 口語數學念法正確（HIGH PRIORITY）。** 每個口語化的數學是 (a) 與書寫數學**數學等價**、且 (b) 對「聽不到符號」的聽者**無歧義**。重點獵捕：根號／次方／分數的群組範圍；下標；反函數記號念「… inverse」而非倒數（除非課文刻意在討論 `^{-1}` 這個符號）；任何會被聽成另一個式子的念法。每筆引用 source LaTeX ＋口語形式。

**D4 — Version B 語域／順耳。** 念出來像沉穩的課堂語氣、自然；無 spell-out 造成的彆扭；「the quantity …」這類去歧義詞**只用在群組真的需要**處。範圍限「**念出來造成的**」彆扭——source 散文品質是鎖稿前 copyedit 的事，NFA 不回頭改。

**D5 — 念法慣例裁定（convention ledger，一次性、低量）。** 替口語稿標記的任何**開放念法抉擇**各推薦一個選項（附一句理由）。**性質：** 這是一次性的 setup 裁定——某節慣例（下標念法、座標念法、「the quantity」用法…）一旦定案即全節／跨節穩定，**穩態下幾乎恆「clean」**，不是逐單元必抓滿的常態維度。

**D6 — TTS 設定合理性（輕量，最弱維度）。** 文件化的合成設定（model／voice／format／sample rate／message shape）內部自洽、合理。**只 flag 明顯的內部矛盾。** 與 Tier 0 的 `derive_spoken --check`／manifest-freshness 對「實際合成」的檢查有重疊；本維只看「文件寫的設定」是否自洽，量低。

**D7 — 數學內容正確（條件式）。** `CONTENT_APPROVED=no` → **必跑**；`=yes` → 只 flag 明顯錯誤。**獨立重算**旁白裡的每個數值、正負號、區間端點、象限、最終結果，確認與數學相符（不只是 D3 的「口語 vs 書寫等價」）。引用任何不符處。**這是唯一需要 agent 隔離的維度**（見下「reader 拆法」）——重算必須對旁白自己的結論盲，否則只是覆述。

## 念法慣例（權威表；D3／D5 的裁定基準）

> 本表為 MiMo 口語數學念法的**單一權威**（2026-07-07 自 RUNBOOK／生成稿收斂至此）。[`../../RUNBOOK-mimo-narration-route.md`](../../RUNBOOK-mimo-narration-route.md) 步驟 1 與 `derive_spoken.py` 生成的 `_narration_spoken.md` §2 為其**摘錄**，衝突時以本表為準；D5 的新裁定定案後**回寫本表**。

- `f^{-1}` → “f inverse”（絕不 “f to the minus one”；例外：課文刻意對比 `\sin^{-1}` 與 `1/\sin` 這個記號時照字面念）
- 下標 `x_1, x_2` → “x sub one / x sub two”
- 和／差的根號 `\sqrt[3]{y-2}` → “the cube root of the quantity y minus two”（「the quantity」只在群組真的需要去歧義時用）
- 群組次方 `(\sqrt[3]{x-2})^3`／`(f^{-1}(x))^2` → “…, all cubed ／ all squared”
- 座標 `(a,b)` → “the point with coordinates a and b”；區間 `[a,b]` → “the interval from a to b”
- 反三角 `\arcsin` → “arcsine of …”；`\pi/2` → “pi over two”；常見分數念 “one half ／ nine-fifths” 等
- `x+\tfrac h2` → “x plus one half h”——**不可** “x plus h over two”（會被聽成 `(x+h)/2`；§3.1 gate-2 實證的 D3 blocking）

## 收斂線（blocking vs advisory）

- **收斂判準**：NFA 通過 ＝ **blocking findings = 0**。advisory 由使用者逐條裁決，**不強制歸零**（同講義 [`../../../handout/html/_audit/PROSE-AUDIT-RUBRIC.md`](../../../handout/html/_audit/PROSE-AUDIT-RUBRIC.md):40）。
- **不 governs Tier 0 腳本**：`derive_spoken --check` 等確定性閘以 exit code 收斂，不套 blocking/advisory。

## 兩道讀者與 reader 拆法（orchestration）

NFA 走**講義散文閘原形**：gate 1 迭代到收斂，gate 2 收斂後單次確認。

- **gate 1 ＝ Claude subagent（免費、迭代到 `blocking==0`）。** reader 拆法**按認知模式、不按維度數**：
  - **永遠 1 個「narration reader」agent**，吃 **D1–D6**（讀 source＋HTML＋口語三件，判忠實／念法／順耳／慣例／設定）——同一認知模式，一個 agent 一次讀完。先跑免費的 `derive_spoken --check` 把 id／`{show}` marker／`$`-漏出的**機械 parity** 吸走，reader 只判語義層。
  - **`CONTENT_APPROVED=no` 時 +1 個「independent recompute」agent**，吃 **D7**：只給它底層數學（source LaTeX／講義環境），**故意不給旁白的結論**，要它從零推導再與旁白宣稱的值對帳（盲、防 anchoring）。`=yes` 時 D7 退成輕量「只抓明顯錯」，由 reader agent 兼做，**不另開 agent**。
  - 穩態（內容已認可）下 NFA 即 **1 個 reader agent**。
- **gate 2 ＝ Codex（計費、收斂後單次、需同意）。** gate 1 已 `blocking==0` 且接近定稿時，跑**一次** Codex 當「另一個真實讀者」補 gate 1 的模型盲點；單讀者一次過 D1–D7，不 fan-out（依 [`../../../CLAUDE.md`](../../../CLAUDE.md) 付費 API 規則先 `--dry-run` 估值、徵同意再跑）。**兩道閘不合併**——各自獨立回報。

## 不算 finding（別誤報）

- `CONTENT_APPROVED=yes` 時已認可的教學內容／教學法（不得 re-litigate）。
- 語義等價的用詞差異、markdown→HTML 的等價轉換（`*x*`→`<em>`）。
- D3／D4：群組真的需要時用的去歧義詞（「the quantity …」），不是缺陷。
- topic-term 自然反覆（該節就在講那個概念）。

## 護欄

- 稽核員**唯讀**：只回報，不改任何檔案（propose-not-act，交回使用者裁決）。
- **不得改已認可 source**（鎖稿後忠實性閘的硬護欄）。
- 遵守四級 finding 分級、**不 over-report**；**乾淨的單元／維度是有效結果**。

## 回報規格

四級，只報 tier 1–2（① 真錯／忠實破口／不可渲染／數學錯 ② 轉換引入的真歧義或可讀性缺陷）；tier 3（純 style drift）至多一行；tier 4（語義等價）略。

**輸出格式（最終訊息；不寫任何檔案）：**

- 首行：`VERDICT: <X> blocking, <Y> advisory`
- 逐條（一行一筆）：
  `- [Blocking|Advisory] [D#] unit-id — issue（引用原文）→ Verdict: Keep|Rewrite|Cut → exact replacement if Rewrite`
- 接 `## Convention recommendations (D5)`、`## TTS sanity (D6)`、（若 D7 有跑）`## Math-content check (D7)`。
- 每個**乾淨**維度各一行（如 `D1 clean`）。
- 簡潔、引用 locus。

**交付給使用者裁決時**：依 [`../../../CLAUDE.md`](../../../CLAUDE.md) 交付規則，**每道閘各產一份** standalone HTML 審核稿（MathJax CDN、雙擊即開、數學即渲染），每筆 finding 標穩定編號（gate 1 用 `N1-…`、gate 2 用 `N2-…`）。NFA 裁決寫進該次修正 commit 的 message body（subject ≤70、body 逐條「原本／為何不妥／改了什麼／證據」），供 `git log --grep="NFA"` 撈回。純版控紀錄（如本 rubric、`REPORT-*.md`）不在 HTML 之限。
