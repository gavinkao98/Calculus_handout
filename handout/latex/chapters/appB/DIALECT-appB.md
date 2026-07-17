# M-B0 盤點：appB 方言凍結表

> LaTeX pilot v2（[`../../KICKOFF-latex-pilot.md`](../../KICKOFF-latex-pilot.md)）M-B0 的落檔產物。
> **與 [`../ch03/DIALECT-ch03.md`](../ch03/DIALECT-ch03.md) 並讀**：ch03 表已凍結的 mapping 不重列細節，本檔權威範圍＝appB 實況＋與 ch03 的差集。
> M-B2 補 mapping 以本檔 §3 差集為準；語意指令的**正式名稱在 M-B1 與模板一起凍結**（D9），本檔 §4 只列需求＋暫名提案。
> 盤點對象＝`../../../html/fragments/appB/sec-b-{1,2,3,4,5}.html`（415 行）。**0 圖、0 表**（D5′ 的「最乾淨模板畫布」前提成立，無 FIGS、無 `export_figs` 需求）。
> 盤點日：2026-07-16。重跑：`python handout/latex/dialect_inventory.py appB`。

> ## 2026-07-17 重新凍結（§B.6 新增後，pilot 四閘已重跑全綠）
>
> **變更**：appB 新增 §B.6「Writing a Proof」（`sec-b-6.html`）並改動 sec-b-1..5；附錄改名
> 「Reading Theorems and Proofs」→「**Reading and Writing Proofs**」。撰稿側閘鏈紀錄見
> [`../../../html/_audit/REVIEW-appendixB-b6-applied.html`](../../../html/_audit/REVIEW-appendixB-b6-applied.html)。
> **同日稍晚（r3，附錄定案）**：第三份第三方意見逐條裁決後落地兩項——① §B.2 的 contraposition
> 歸類對齊 §B.6（純散文改寫：Strategy B.2 條目 2 的親緣子句改為 look-alike 消歧、Prop B.1 後的
> 過渡句改口；**roster 仍 5 形狀、回馬槍不動**）② §B.6 新增 **Example B.11**（歸納法斷鏈：步驟有效、
> 無 base case）＋其框架段落由「two／both … perfectly true」改為三分流。裁決稿見
> [`../../../html/_audit/REVIEW-appendixB-r3-adjudication.html`](../../../html/_audit/REVIEW-appendixB-r3-adjudication.html)。
> **r3 第二輪（同日，使用者裁決「四件事你自己判斷全部做完，一頁式總表就不做了」）**再落地三項純散文改動：
> ③ **§B.3 Strategy B.3 步驟 2 加指路子句**（只指路、不搬規則——`sec-b-6.html` 的 implication-kernel
> 分工 CONSTRAINT 未動）④ §B.2 分案段「a **shrewd** split…」修飾語誤掛（改用刪除而非搬移）
> ⑤ §B.2 歸納段骨牌句重寫（懸垂修飾＋「the first fall」名詞/動詞 garden-path）。
> **一頁式總表經使用者裁決不做**——動機成立但成本被低估（全書 fragment `<table>` 命中數＝**0**，
> 將是全書第一個表，須進 CONTRACT＋mapping＋模板＋四閘；且與 Strategy B.2＋§B.6 骨架重疊約八成）。
> **r3 對本表的影響＝方言零成長**（五項都刻意只用既有詞彙），僅計數與頁數變動。
> **本表下方 §2 的逐項「次數」欄仍是 M-B0（5 節）的歷史凍結值；下表為現況權威。**
>
> | | M-B0 凍結（5 節、415 行） | §B.6 定版（6 節、925 行） | **r3 現況凍結（6 節、1089 行）** |
> |---|---|---|---|
> | **tag＋class 組合** | 34 種 | 35 種——＋1（見下） | **35 種——r3 ＋0** |
> | 數學 inline `\(…\)` | 308 | 532 | **550** |
> | 數學 display `\[…\]` | 9 | 13 | **16**（`aligned` 仍僅 1，在 sec-b-2；r3 ＋3＝Ex B.11 的宣稱／歸納步驟／Prop B.4 對照式） |
> | inline `style=` | 5（僅 sec-b-3） | 5 | **5**（仍僅 sec-b-3，未新增） |
> | 圖／表 | 0／0 | 0／0 | **0／0** |
> | 活散文非 ASCII（**raw**） | `—`×98 `§`×14 `’`×4 | `—`×171 `§`×31 `’`×17 `–`×1 | **`—`×174 `§`×34 `’`×17 `–`×1** |
> | PDF 頁數 | 14（HTML 20） | 24 | **25** |
> | `span.env-num` 編號帳 | — | 23 | **24**＝Definition 1＋Strategy 7＋Example **11**＋Proposition 5 |
>
> **§3 差集新增一項（M-B2 已補 mapping、已凍結正式名稱）：**
>
> | 差集項 | 次數 | 收編方式（M-B2 定案 2026-07-17） |
> |---|---|---|
> | `p.page-break-before` | 1 | `sec-b-5.html`，§B.5 Pause 框後的走查段。語意＝**此段之前強制換頁**（讓 Pause 的「先自試」在單面 A4 上真的做得到——答案不與題目同頁；未加之前盲測實證該教具「靜靜失效」）。語意指令＝**`\pagebreakbefore`**（M-B1 §2 詞彙表 2026-07-17 擴充）；樣式層＝`\par\ifdim\pagetotal>0pt\newpage\fi`，`\ifdim` 守衛刻意對映 HTML 分頁器的 `body.childElementCount > 0`（頁面已有內容才斷，不製造前導空白頁）。轉換器：`convert.py` 的 `<p>` 分支加此 variant，複合 class 仍硬錯（`test_convert.py::test_p_page_break_before*` 兩條鎖住）。**`ch01/sec-1-1.html` 已用同一 class 兩次**（`h3.subsec-head` 與 `section.env.env-theorem`）——那兩個組合**不在本表**，ch01 rollout 時須各自補 mapping（語意指令可沿用）。 |
>
> **其餘一切照舊**：§B.6 與 §B.4 新增的 Example B.6 都是刻意只用本表既有詞彙寫成的
> （`ol.steps`／`strong` run-in／`div.workedexample`／`ul.sol-list`／`p.informal`／
> `env-strategy`／`env-caution`／`env-remark`）。除上表那一項外，M-B2 的 mapping 工作量不受影響。
>
> **另一個新事實（不是新組合，但語意指令要容得下）：`ol.steps` 多了父元素 `article.sec`**
> （原僅 `div.env-body`）——§B.6 的 proof skeleton 直接住在散文裡、不在 env 盒內。已有先例
> （§2 #15 的 `ul.sol-list` 早有「×1 直接在 article.sec」），但語意指令若假設 `steps` 必在 env 內就會踩到。
>
> **四閘（2026-07-17 §B.6 定版時重跑，全綠）**：編譯 0 error／0 missing char｜版面 0 overfull／0 underfull｜
> 完整性 coverage 100%（695 mapped／0 skipped）＋`check_prose.py` PASS（4 處 pdftotext 抽取假象、
> 0 真落差）＋數學逐位元組 81 測試全過｜人眼 24 頁逐頁。成品 `../../dist/appB/`（pdf＋自足 tex）已更新。
> **模板連帶**：人眼閘抓到 `\cb@needspace` 的誤觸發（詳見 `../../template/calcbook.sty` 該處註解
> 與 `../../template/M-B1-DECISIONS.md` 沿革），已修並回歸——25 頁→24 頁、近空白頁消失。
>
> **四閘（r3 重跑，全綠；下列為第二輪收案值）**：編譯 0 error／0 missing char｜版面 0 overfull／0 underfull｜
> 完整性 coverage 100%（**717** mapped／0 skipped）＋`check_prose.py` PASS（**14** 處 pdftotext
> 抽取假象、**0 真落差**）＋數學逐位元組 **81 測試全過**｜人眼見下。`make_dist.py appB` 一把跑完，
> 成品 `../../dist/appB/` 已更新（25 頁）。
> **`test_convert.py` 的鎖實值同步**（ledger lock，非 bug）：`mapped` 695→716→**717**（716→717＝
> §B.3 指路子句新增的 `<em>if–then</em>` 節點，精確可解釋）、`math` 545→**566**＝inline 550＋
> display 16。改動前這幾條會硬錯，正是它們該有的行為。
> **HTML 線交叉驗證**：standalone 實測 **566 個 MathJax 容器／0 error**，與 LaTeX 線的 566 段數學
> pass-through **完全一致**；`.env-num` ×24，展開逐節對得上文件順序，**Example B.1–B.11 連續、零 cascade**。
> **人眼閘（r3 範圍說明，據實記載）**：FIX-1 使 p4 的 Strategy B.2 條目 2 長約 4 行，故 **p4 以後
> 全篇位移**，不能宣稱「其餘頁未動」。實際做法＝① 改動落點逐頁看（**p4–5** FIX-1；**p20–23** FIX-2，
> 含 Ex B.11 跨 p22–23 的 workedexample keep-together）② 全 25 頁做低密度掃描以攔上一輪那個
> `\cb@needspace` 級失效（字元中位數 2125；唯一低密度頁＝**p25** 收束段 587 字元＝正常尾頁，
> **中間無近空白頁**）。未逐頁重看全 25 頁。

## 1. 摘要

- **34 種 tag＋class 組合**。其中 29 種與 ch03 共用或屬 CONTRACT 既有詞彙；**5 種為 appB 新組合**（`strong`、`br`、`ul.steps`、`ul.sol-list`、`span.qed.qed-proof`），另有 **inline `style="text-align:center;"` ×5**（僅 sec-b-3）。後兩類含 CONTRACT 明文不允許的寫法（見 §7）——皆為樹上既成內容，依 D3（fragment 不改寫）由轉換器收編。
- **數學：inline `\(…\)` ×308、display `\[…\]` ×9**（`aligned` ×1，在 sec-b-2 歸納證明，內含對齊符 `&` 與換列 `\\`——v1 scanner 已處理的型）。**數學區段內零非 ASCII、零 entity** → 逐位元組 pass-through 無字元風險、無 HTML/LaTeX 語義分岔點。
- **活散文非 ASCII（raw）3 個字元**：`—` U+2014 ×98、`§` U+00A7 ×14、`’` U+2019 ×4（2026-07-17 quote_lint 修正後新增，見 §5）。另用 **5 種 character entity**（ch03 全用 raw Unicode、appB 部分用 entity——來源方言差異，見 §5）。
- **HTML 註解含 CJK 與 `¬`**（撰稿溯源筆記）——轉換器丟棄註解後不進 LaTeX，同 ch03 結論：不需要 CJK 字體。

## 2. 凍結盤點表（34 組合）

「次數」為 appB 五個 fragment 的實際出現數；「ch03」欄＝該組合是否已在 DIALECT-ch03 凍結表（Y＝mapping 沿用、**N＝差集**）。

| # | Fragment 標記 | 次數 | ch03 | 備註（父元素／語意） |
|---|---|---|---|---|
| 1 | `article.sec` | 6 | Y | root 直下；sec-b-1 含 **2** 個（開場＋§B.1），其餘各 1 |
| 2 | `header.chapter-head`＋`div.ch-kicker`＋`h1.ch-title` | 各 1 | Y* | **附錄開場變體**：結構與 ch03 章開場全同，kicker 字面＝`Appendix B`（非 `Chapter N`）→ 語意指令須有 appendix 變體或以 kicker 字面驅動 |
| 3 | `p.lead` | 1 | Y | 開場 lead |
| 4 | `p.para-head` | 1 | Y | 開場「By the end of this appendix…」引言行 |
| 5 | `header.sec-head`＋`h2.sec-title`＋`span.sec-no` | 各 5 | Y | `sec-no` 照抄字面 `B.1`–`B.5`（D7） |
| 6 | `p` | 70 | Y | article.sec 與 div.env-body 兩處 |
| 7 | `p[style="text-align:center;"]` | 5 | **N** | 全在 sec-b-3：置中陳述（量詞句 (i)/(ii)、待否定句、否定結果句、ε–δ 模式句）；兩句帶 `(i)&ensp;&ensp;` 式編號；1 句內含 `<br>` |
| 8 | `br` | 1 | **N** | sec-b-3:69，置中陳述內的手動斷行 → `\\` |
| 9 | `p.informal` | 2 | Y | 皆在 strategy 的 env-body 內（ch03 在 definition 內；mapping 同） |
| 10 | `em` | 101 | Y | `\emph` |
| 11 | `strong` | 30 | **N** | ch03 明文「未使用」；appB 用作 **run-in 粗體標籤**：li 首（×25，如 `<strong>Direct.</strong>`）＋ p 首（×5，sec-b-2 五個證明形狀段落的 lead-in） |
| 12 | `ul` | 2 | Y | 開場 objectives（article.sec 下）＋ Definition B.1 內文 |
| 13 | `ol.steps` | 4 | Y | Strategy B.1／B.3／B.5 ＋ **env-remark（Pause）內 ×1** |
| 14 | `ul.steps` | 2 | **N** | Strategy B.2／B.4：**無序** steps 變體（CONTRACT 只定義 `ol.steps`） |
| 15 | `ul.sol-list` | 3 | **N** | ch03 無 sol-list。×2 在 solution 的 env-body；**×1 直接在 article.sec**（sec-b-5:69，散文位置的五習慣走查清單，不在任何 env 內） |
| 16 | `li` | 47 | Y | ol.steps／ul.steps／ul.sol-list／ul 四處 |
| 17 | `section.env.env-definition` | 1 | Y | Definition B.1 |
| 18 | `section.env.env-proposition` | 5 | Y | Proposition B.1–B.5 |
| 19 | `section.env.env-proof` | 5 | Y | 每個 proposition 各配一個 |
| 20 | `section.env.env-example` | 5 | Y | Example B.1–B.5 |
| 21 | `section.env.env-solution` | 5 | Y | 不編號 |
| 22 | `section.env.env-remark` | 1 | Y* | **kicker 字面＝`Pause`**（非 `Remark`）→ kicker 是資料不是樣式常數 |
| 23 | `section.env.env-caution` | 3 | Y | 皆不編號 |
| 24 | `section.env.env-strategy` | 5 | Y | Strategy B.1–B.5，每節一個 |
| 25 | `p.env-head` | 30 | Y | |
| 26 | `span.env-kicker` | 30 | Y | 字面集合＝Definition／Proposition／Proof／Example／Solution／Caution／Strategy／**Pause** |
| 27 | `span.env-num` | 16 | Y | 照抄字面（D7）：Definition B.1＋Strategy B.1–5＋Example B.1–5＋Proposition B.1–5；solution／proof／caution／remark 不編號 |
| 28 | `span.env-name` | 6 | Y | Strategy B.1–B.5 的方法名＋Proposition B.5 `The pigeonhole principle` |
| 29 | `div.env-body` | 30 | Y | |
| 30 | `div.workedexample` | 5 | Y | 恰 1 example＋1 solution（B.1–B.5；sec-b-4 有 2 個，sec-b-5 為 0） |
| 31 | `span.qed.qed-proof` | 5 | **N** | ch03 零 qed；appB **5 個 proof 全部**照 CONTRACT 以之收尾，位置＝proof 最後一個 `<p>` 的段尾 |

補充規則（沿 ch03）：HTML 註解全丟棄（appB 溯源筆記含 CJK）；`article` 的 `lang="en"` 忽略；屬性面盤點＝`class`（全部）＋`lang`（article ×6）＋`style`（p ×5，即 #7），**無其他屬性**。

## 3. 與 ch03 的差集（M-B2 要補的 mapping，凍結）

**appB − ch03（6 項標記＋2 項來源方言）**：

| 差集項 | 次數 | 收編方式提案（M-B1／M-B2 定案） |
|---|---|---|
| `strong` | 30 | run-in 粗體標籤（`\textbf` 或語意 `\runin{…}`——樣式層決定字體與後綴間距） |
| `br` | 1 | 僅允許出現在置中陳述內 → `\\`；其他位置照 fail-loud 硬錯 |
| `ul.steps` | 2 | steps 的無序變體（bullet 版 method list） |
| `ul.sol-list` | 3 | sol-list 環境；**父元素允許 env-body 與 article.sec 兩種**（後者＝散文位置） |
| `p[style="text-align:center;"]` | 5 | 置中陳述語意指令（唯一允許的 inline style 字面值，白名單精確比對；其他 style 硬錯） |
| `span.qed.qed-proof` | 5 | proof 收尾記號（樣式層決定 □ 的長相；另見 §7 qed 條） |
| 附錄開場（kicker=`Appendix B`） | 1 | 開場指令的 appendix 變體（字面驅動，不開 counter） |
| entity 寫法（§5 的 5 種） | — | `convert_charrefs=True` 已自動解碼為 Unicode，emitter 端只需處理 **U+2002**（見 §5） |

**ch03 − appB（模板仍須支援、本 pilot 不驗）**：`h3.subsec-head`、`section.env.env-theorem`、`figure.figure[data-fig]`＋`figcaption`＋`span.fig-no`。theorem 樣式與 example 級 keep-together 已由 ch03 表凍結；圖路徑依 kickoff §4.4 留 rollout 首個有圖章補驗。另 reading-track 句型（`p em` 的 `First reading:`／`Proof track:`）兩邊都沒有（只在 ch01），但 kickoff §3 sampler 清單點名要展示 → M-B1 需求照列。

**修正 kickoff §1 的初步差集清單**：`strategy`／`steps`（ol 版）／`env-name` **不在差集**——DIALECT-ch03 凍結表第 22／12／26 列已有（ch03 有 Strategy ×2、ol.steps ×2、env-name ×13）。真差集如上表；初步清單漏列 `strong`／`br`／`qed`／`ul` 兩變體／entity。

## 4. 語意指令需求清單（M-B1 拍板正式名稱＋樣式；暫名僅供討論）

模板語意層（D9）至少須涵蓋下列槽位。「appB」欄＝pilot 實際壓到；未壓到者進 sampler 展示（per kickoff §3 DoD）或留 rollout。

| 需求 | appB | 暫名提案 | 設計備註（M-B1 議題） |
|---|---|---|---|
| 章／附錄開場（kicker＋title＋lead＋objectives） | ✓ | `\chapteropener`／`appendixopener` | kicker 字面照抄；objectives＝開場專用清單樣式 |
| 節標題（字面 sec-no） | ✓ | `\sechead{B.1}{…}` | 與 kicker 的書籍化處理＝§4.2 互動議題 |
| env 家族：definition／proposition／proof／example／solution／remark／caution／strategy | ✓ | 同名環境 | kicker、num、name 皆為**環境參數**（字面資料）；theorem／corollary 同族預留 |
| workedexample 群組 | ✓ | `workedexample` 環境 | keep-together（needspace 級）＝ch03 表既定 |
| steps（有序／無序） | ✓ | `steps`／`steps*` | 無序變體＝appB 新增 |
| sol-list（solution 內／散文位置） | ✓ | `sollist` | 兩種父位置同一樣式 |
| run-in 粗體標籤 | ✓ | `\runin{…}`（或直接 `\textbf`） | li 首與 p 首兩位置 |
| 置中陳述（±手動 `\\` 斷行） | ✓ | `centerstatement` | 承載量詞句；(i)/(ii) 字面＋`\enspace` 對齊 |
| informal gloss | ✓ | `\informal{…}` 或環境 | 斜體 softer，ch03 既定 |
| qed 記號 | ✓ | `\qedmark` | 手動、不用 amsthm 自動 □（見 §7） |
| `em` 強調 | ✓ | `\emph` | |
| 一般 `ul`／`li` | ✓ | `itemize` | |
| lead／para-head | ✓ | `\lead`／`\parahead` | |
| subsec-head | — | `\subsechead` | ch03 有、appB 無；模板須備 |
| figure（non-float）＋字面 fig-no | — | ch03 表既定 | rollout 首個有圖章驗收 |
| reading-track 標示 | — | `\readingtrack{…}` | 僅 ch01 用到；sampler 展示（kickoff §3） |

## 5. 字元盤點（「0 missing character」DoD 依據）

**活散文（註解外、數學外）**，raw ＋ entity 解碼後合併視角：

| 字元 | 來源 | 次數 | NCM 風險 |
|---|---|---|---|
| `—` U+2014 | raw | 98 | 無（ch03 已驗） |
| `§` U+00A7 | raw | 14 | 無（ch03 已驗） |
| `“` `”` U+201C/201D | entity `&ldquo;`/`&rdquo;` | 58＋58 | 無（ch03 raw 已驗） |
| `…` U+2026 | entity `&hellip;` ×4 | 4 | 無（NCM 有字）；或 emitter 正規化為 `\ldots` |
| en space U+2002 | entity `&ensp;` ×4 | 4 | **不賭字型**：emitter 一律映射 `\enspace`（間距指令，非字形） |
| `–` U+2013 | entity `&ndash;` ×2 | 2 | 無（ch03 raw 已驗） |
| `’` U+2019 | raw | 4 | 無（ch03 已驗）；2026-07-17 新增，見下方撇號條目 |

- **來源方言差異（凍結為事實）**：ch03 全用 raw Unicode；appB 印刷字元多走 entity。`convert.py` 的 `FragmentParser(convert_charrefs=True)` 已自動解碼，兩種寫法進 IR 後無差異；數學 scanner 掃 raw 源、appB **數學內零 entity**（已逐一驗過，唯一的 `&` 是 aligned 對齊符），故 v1 的 `&#92;` 級 entity-delimiter 硬錯防線不會觸發。
- 撇號：凍結時（2026-07-16）appB 用 ASCII `'`（ch03 用 `’`）；**2026-07-17 已依 CONTENT_SPEC §8 以 `quote_lint.py --fix` 改為 `’` U+2019 ×4**（sec-b-{1,2,3,5} 各 1，CI quote-lint gate 要求）。LaTeX 輸出兩者同形（`'` 亦排成右引號），轉換無風險；本表其餘凍結值不受影響（`dialect_inventory.py appB` 2026-07-17 重跑僅此字元項變動）。
- **數學區段內零非 ASCII**（同 ch03）。
- 註解內：CJK ×17 字＋`¬` ×2＋`§` ×25 等——全部隨註解丟棄。

## 6. 與 kickoff §1 初步盤點的出入（M-B0 正式凍結值）

kickoff §1 那段是 2026-07-16 討論時的**初步**盤點，本節為正式凍結後的更正；kickoff 本文不回改（M-B4 文檔收尾時補記指向本檔）。

| kickoff §1 說 | 實測凍結值 |
|---|---|
| 「sec-b-1 含 3 個 article」 | **2 個**（開場＋§B.1）；全 appB `article.sec` ×6 |
| 「workedexample ×2」 | **×5**（B.1–B.5 各一；sec-b-4 佔 2、sec-b-5 為 0） |
| 差集＝「strategy／steps／sol-list／env-name／inline center／附錄開場」 | strategy／ol.steps／env-name **ch03 已有，不是差集**；真差集見 §3（含初步清單漏列的 `strong` ×30、`br`、`qed` ×5、`ul.steps`／`ul.sol-list` 變體、entity 方言） |
| 「env 家族＝definition／example／solution／strategy／caution／proof／proposition／remark」 | ✓ 相符（無 theorem／corollary） |
| 「特有 class＝steps、sol-list、env-name」 | steps／env-name ch03 已有；appB 特有＝**ul.steps／ul.sol-list 變體**與 sol-list 本身 |
| 「`style="text-align:center;"` ×5（sec-b-3）」 | ✓ 相符（含 1 個內嵌 `<br>`） |
| 「aligned ×1」 | ✓ 相符（sec-b-2 歸納證明） |
| 「0 圖、0 表」 | ✓ 相符 |

## 7. CONTRACT 對照（既存偏差，凍結為現況；依 D3 收編、不改 fragment）

[`../../../html/CONTRACT-html-writing.md`](../../../html/CONTRACT-html-writing.md) 與 appB 樹上實況的出入。**pilot 立場＝轉換器收編現況**；fragment 端要不要回頭整併是內容線的事，不在 pilot 範圍（記錄於此供未來裁決）：

1. **`strong` ×30** — CONTRACT「Emphasis: `<em>` only — no `<b>`/`<strong>` in prose」。appB 系統性用作 run-in 標籤（清單項首、段首 lead-in），非散文強調——語意上自成一格，收編為 run-in 槽位。
2. **inline `style` ×5** — CONTRACT「never write inline `style=`」。收編為置中陳述指令；白名單只認 `text-align:center;` 這個字面值。
3. **`ul.steps`／`ul.sol-list`** — CONTRACT 定義 `<ol class="steps">`／`<ol class="sol-list">`。appB 的 ul 變體語意合理（無順序的方法目錄），收編。
4. **`ul.sol-list` 出現在散文位置**（article.sec 直下，sec-b-5）— CONTRACT 說 sol-list 是「solution parts」。收編為兩父位置皆可。
5. **entity 寫法** — CONTRACT「Use real Unicode directly」。appB 用 entity；解碼後等價，無行為差異。
6. **qed** — appB 的 5 個 proof 全部照 CONTRACT 以 `<span class="qed qed-proof">` 收尾（**ch03 反而全沒有**）。DIALECT-ch03 §7 的 F2（LaTeX proof 環境自動補 □ 與否）在 appB 有了答案：**qed 由 fragment 記號驅動、模板不自動補**——這樣 ch03（無記號）與 appB（有記號）rollout 時行為都與 HTML 一致。樣式層長相 M-B1 定。

## 8. M-B0 驗證點狀態

- ✅ 盤點落檔（本檔）；`dialect_inventory.py appB` 可重跑覆核。
- ✅ 差集清單凍結（§3）；語意指令需求清單凍結（§4，名稱待 M-B1）。
- ✅ 附帶驗證：數學 pass-through 無 entity 分岔點；0 圖 0 表前提成立。

---

*M-B0 完成（2026-07-16）。下一步 M-B1＝模板設計（互動，D10）：class 選型起手，逐項過 kickoff §4.2 議題清單 → `template/sampler.tex` → 使用者拍板。*
