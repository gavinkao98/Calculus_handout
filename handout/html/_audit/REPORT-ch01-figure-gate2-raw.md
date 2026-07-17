Reading prompt from stdin...
OpenAI Codex v0.140.0-alpha.2
--------
workdir: C:\Users\user\Desktop\Calculus_handout
model: gpt-5.5
provider: openai
approval: never
sandbox: read-only
reasoning effort: xhigh
reasoning summaries: none
session id: 019ecfab-c9fb-7f92-a9e3-cc62eb47966e
--------
user
你是本講義「圖稽核」的 **gate 2 —— 獨立第二位視覺審查者**（與 gate 1 各自獨立、互不參照）。對 Chapter 1 列印版的**全部 20 張教學圖**做**獨立**的視覺正確性／可讀性複核。

# 你拿到什麼
- 透過 `-i` 附上的 **19 張 PNG**：`chapter1-print-standalone.html` 經 headless Chrome 截的 A4 列印頁（2×）。每頁含 1–2 張圖與其周圍正文。檔名 `ch01-pNN.png` 的 `NN` 即頁碼。
- 你在 read-only sandbox 內可讀取 repo 檔案。

# 開審前先讀（權威依據，勿憑記憶）
1. `handout/_audit/FIGURE-AUDIT-RUBRIC.md` —— **本審契約**：維度 D1–D8、blocking／advisory 擋稿線、**Non-findings 清單**、輸出格式。務必逐條內化其 Non-findings 與「不 over-report」原則。
2. 每張圖的繪圖原始碼在 `handout/chapter1-print-standalone.html` 的 `const FIGS` 物件（搜尋 `"<figid>":`）—— D6（圖的數學正確性：座標、tick、對稱性）需據此**算數值**核對，不要只看變數名。
3. 圖所在小節在 `handout/fragments/ch01/sec-1-*.html` —— D5（圖↔caption／prose 一致）、D7（no-spoiler）的語境基準。

# 圖 → 頁 對照（共 20 圖；標「新」者為近期新增）
- Fig 1.1  `hlt` → p03
- Fig 1.3  `restrict-x2` → p06
- Fig 1.4  `sine-not-1to1` → p08
- Fig 1.5  `restricted-sine` → p09
- Fig 1.6  `arcsin-triangle` → p11
- Fig 1.7  `restricted-cosine` → p11（與 1.6 同頁）
- Fig 1.8  `restricted-tangent` → p13
- Fig 1.9  `arctan10-triangle` → p14（新）
- Fig 1.10 `arctan-general-triangle` → p15（新）
- Fig 1.11 `limit-same-near-a` → p17
- Fig 1.12 `read-limit-graph` → p18
- Fig 1.13 `one-sided-limits` → p21
- Fig 1.14 `piecewise-jump` → p22（新）
- Fig 1.15 `one-sided-infinite` → p24
- Fig 1.16 `vertical-asymptote` → p26
- Fig 1.17 `ln-asymptote` → p27（新）
- Fig 1.18 `floor-function` → p32（新）
- Fig 1.19 `squeeze-theorem` → p33（新）
- Fig 1.20 `squeeze-x2sin` → p34（新）
- Fig 1.21 `precise-limit` → p37

# 約束（務必遵守）
- **你是獨立審查者**：自行看圖＋自行核對 `FIGS` 座標／課文，**不要假設任何先前審查的結論**，也不要去找或參照任何其他審核報告（`REVIEW-*.html`、`REPORT-*` 等）。
- **嚴守 rubric 的 Non-findings**：刻意示意近似比例的直角三角形（標籤數學正確即可，如 arcsin／arctan triangle）、§10 允許的 callout／redundant curve label／宣告過的 palette exception、純美學偏好（色深/字級，除非已影響可讀性）、標準慣例（如 ε-δ 圖空心點＝極限值、實心點＝f(a)、非承載軸缺刻度僅 advisory）——這些是特性不是缺陷，絕不可當 finding。
- **寧缺勿濫、不 over-report**：乾淨的維度／圖是有效且常見的結果。把握不足 → 降為 advisory 或不報，不要升為 blocking。
- **唯讀**：只回報 findings，絕不修改任何檔案。

# 輸出（你的「最後一則訊息」＝完整報告，全程繁體中文；數學式、檔名、識別碼保留原樣）
逐圖（Fig 1.1 … Fig 1.21）給出：
- 該圖 `VERDICT: <B> blocking, <A> advisory`
- 逐條 finding（一行一筆）：`圖 ID｜Figure #｜維度 D?｜Blocking|Advisory｜證據（PNG 觀察＋FIGS 行/座標/數值）｜為何｜建議修法`
- 各**乾淨**維度一行帶過（如「D1–D8 乾淨」或逐條）。

最後給**全章彙總**：總 blocking 數、figure gate（gate 2）是否通過（blocking = 0）。乾淨圖就明說乾淨。

codex
我會先讀專案規則與 rubric，接著只讀 `FIGS` 原始座標和相關章節片段來核對 20 張圖；全程只做稽核、不改檔。
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "Get-Content -Raw handout\\_audit\\FIGURE-AUDIT-RUBRIC.md" in C:\Users\user\Desktop\Calculus_handout
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'Get-Content -Raw CLAUDE.md' in C:\Users\user\Desktop\Calculus_handout
 succeeded in 365ms:
# 雓儔?里????RUBRIC嚗igure audit嚗?
> **?砍祟憟?嚗銝?靘?嚗?* gate 1 = Claude `handout-figure-audit` subagent嚗?閬箏惜??Codex 蝚砌?霈???*摰阮??靽∪?銴**嚗?瘥憚敹?嚗?鞎駁???嚗?> **鋡怠祟?抬?** 銝撘?**render 敺? PNG**嚗 [`../_render/shot.mjs`](../_render/shot.mjs) 敺?standalone ?芸??Ｗ嚗??臬??扯府蝭 fragment ??`figcaption`嚗FIGS` ??蝣潛隤???> **靘?嚗?* [`../../CONTENT_SPEC.md`](../../CONTENT_SPEC.md) 禮10嚗?閬?嚗??祆?蝬剖漲嚗? ch01 ?里?詨祕霅擗橘?閬?`../_dev-archive/ch01/ch01_figure-audit.md`嚗?> **?扯釭嚗?* ?航??dvisory嚗locking ?????寞??祟??*?怠靘?*撠?撠?銝?敺???銝 copyedit??
## 蝬剖漲嚗1?8嚗?璇? Blocking / Advisory嚗?
**?航??改???皜?嚗?*
- **D1 Label collision嚗verlap**嚗abel 鈭???頠詻??脩????*??鞈? ??Blocking**嚗?敺桀?蝘颱??? ??advisory??- **D2 Out-of-bounds嚗lipping**嚗??萄?蝝?頧??漱暺撓餈???閮?嚗◤鋆?航????*??Blocking**??- **D3 Viewing-window readability**嚗/y-range ?之??撠?雿踵蝺票蝺??????扯??綽?瞍貉?蝺頝??脯??銝颲具?*??Blocking**嚗???荔???- **D4 Tick labels present嚗egible**嚗頛?摮詨潛?頠賂?霈????霈?潸?嚗撩?餃漲??嚗? `tex` 甈撩憭晞allback 銝??湔嚗?*霈?瘜?????Blocking**嚗??輯?頠貊撩?餃漲 ??advisory??
**敹璅∪?嚗????敹萄?嚗?*
- **D5 Figure ??caption嚗rose 銝??*嚗???figcaption嚗?蝢抬?蝭??唾膩?嚗??璆菟?憿?怠?氬?strip 璅?蝔晞?思?撠迂嚗?*??Blocking**??- **D6 Math correctness vs source**嚗? `FIGS` ??蝣潘?嚗漣璅??詨潸?隤脫?銝泵 **??Blocking**嚗?蝷箸?瘥?嚗?蝐斗摮豢迤蝣箝耦?餈撮嚗?*??advisory**嚗窒??ch01 A1 ???嚗?靽殷???- **D7 No-spoiler**嚗orked-example ?援?脰?摮貊?蝞???*??Blocking**??
**蝺函Ⅳ蝛拙嚗?0嚗?*
- **D8 Color-only嚗rayscale survival**嚗?閮???脣????箏??⊥??颲剁?蝻?redundant encoding嚗???璅?嚗??label嚗?*??Blocking**嚗alette 頞?嚗? blue嚗ed嚗ray?摰??嚗? advisory??
## Non-findings嚗??finding嚗?- ?餅??內??隡潭?靘?憒閫?閫耦蝷箸???璅惜?詨飛甇?Ⅱ嚗?- 禮10 ?迂??callout?edundant curve label?恐????palette exception??- 蝝?摮詨?憟踝??脫楛??蝝?嚗?歇敶梢?航??扼?
## 頛詨?澆?
1. `VERDICT` 銵?閬死 blocking ?詻?2. ?? finding嚗??ID嚚igure #嚚雁摨?D?嚚locking|Advisory嚚???摨扳?/瑼?/PNG 閫撖?嚚雿?撱箄降靽格?`??3. ?嗾瘛函雁摨虫?銵??? 銋暹楊????4. ?怨?蝯?嚗???祉???*閬死 blocking ?臬甇賊**??
**銝?over-report?嗾瘛典??舀?????* 雿?降???航???findings 鈭文?鋆捱嚗??寞?嚗靘??航?嚗?

 succeeded in 364ms:
# CLAUDE.md

?祆?獢?砍摮澈??蝯?AI 隞??嚗laude Code?odex 蝑???獢惜蝝?撘??舫遢????*甈??**嚗`AGENTS.md`](AGENTS.md) ????祆???璅??批捆銝?銴摮澈???渡?瑽?撱箇蔭閬?隞交?憡扳?隞?[`README.md`](README.md) ?箸?嚗摰寞撖怨??誑 [`CONTENT_SPEC.md`](CONTENT_SPEC.md) ?箸???

## ?辣?啣神隤?

- **README 銝敺誑蝜?銝剜??詨神??* ???急?桅???[`README.md`](README.md) 隞亙?摮??冗銝剖惇?潭撠???README嚗?憒?[`video/README.md`](video/README.md)嚗憓?靽格 README ?瘥颲衣???
- **敹?銋?靽???嚗?蝧餉陌嚗?* 蝔?蝣澆?憛?獢楝敺?????hell ?誘?憓??詻??亦Ⅳ嚗cene id?xport ?迂??雿?嚗誑????閰??銵?隤?Manim?aTeX?emini?TS?I?R?ode A/B/C 蝑???
- ?園??????憿”?潛?隤芣???銝敺蝙?函?擃葉??
- 蝚砌??嫣?鞈湛?`.deps/`?.deps_f5/`?.deps_voiceover/`嚗? git 撌乩?璅對?`.claude/worktrees/`嚗葉??README 銝甇方????嚗?閬??

## 敶梁?皜脫?閫??摨?

- **?日?雿輻??亥?瘙??血?銝敺誑 1080p 皜脫?**嚗make.py --quality high`嚗?閬銵蝙??`--quality low`嚗?80p嚗? `--quality 4k`??
- 4K 皜脫?嚗--quality 4k`嚗??其蝙?刻?蝣箸?摰?K???迤撘漱隞?雿輻??

## 隞祥 API 隤輻??蝬???

- **瘥活隤輻隞颱?閮祥????API嚗? Gemini TTS?emini ??嚗蔣????嚗????賢?????雿輻??蝣箏???銝?芾?隤輻??* ?寞活??嚗?憒蝭? TTS?蝡?頝?銝敺?隤芣?嚗活閬矽?其?暻潭芋??隡啁??beat ?賂??唾?蝘嚗??嚗???敺??瑁???
- 銝?鞎颯???雯?蝺楝敺??冽迨???舫??瑁???憒?`tts.py --backend mock`嚗神? WAV 撽?manifest嚗?摨????Manim render?fmpeg mux/concat??
- ??銝甈∪??隞?”閰脫活?Ⅱ隤芣??極雿????蝭?霈嚗?璅∪????湔??頝???敺萄?????

## 頝典?閰梯??嗅神?脩??扳?瑼?銝神?砍 memory嚗?

- **?蜇蝯?蝑???隞颱?頝典?閰梧?頝冽??函??亥???銝敺神?脫? git 銝??瑼?*嚗?*銝??芾??冽?啁? Claude memory**嚗~/.claude/.../memory/`嚗 `MEMORY.md`嚗?
- **??嚗?* 雿輻?虜??虫?璆哨??砍 memory 銝 repo 韏啜?璈停瘨仃嚗???扳?瑼?頝? git ?唳??唳??具?
- **撖怠鋆∴?** ?脣漲嚗??神?脰府?Ｙ???`REBUILD_STATUS.md`嚗??頝典?閰梢脣漲?剁?嚗極?瑞瘜??神?脣??? `README.md`嚗撘?鞈?瘚?蝝神??`DESIGN.md`嚗摰寞瘜?撖恍?`CONTENT_METHODOLOGY.md`?銝????瑼?嚗??蝙?刻??曉嚗?閬?暺閮脫??memory??

## ?啣神嚗祟?亦??Ｘ????嚗?摮?砍 memory嚗?銝?閬??祇脩??改?

- **?蝙?刻?閰曹?敺蝜?銝剜?**嚗aTeX嚗?撘Ⅳ??隞嗅?????銵?隤????璅????
- **??doc嚗ode review ??皜?蝝?銝?瘛瑞銝隢?** ????蝒????Ｗ?閬?嚗?靽殷???discoverability gap嚗??辣?喳嚗??嚗 editorial drift 憸券嚗??芸?嚗???finding嚗 ??finding嚗?蝷箔?閬??Ｗ榆?堆???*Framing嚗?* 敺?◤ review ?邦?瘜?潘?銝???session ?扳 commit嚗 merge ???渡?Ｘ?鈭祕嚗?蝢拍??寧??刻?撌桃銝? inconsistency?ver-reporting ????甇???芸???
- **銝?mode ?啣神瘚?嚗oot [`README.md`](README.md) 禮Mode B嚗?嚗ode B ?里?貉?瘙箄??潛撖恍脰府甈∩耨甇?commit ??message body**嚗ubject ??0 摮ody ??嚗??祆隞暻潦雿?憒乓鈭?暻潦??刻???嚗末霈靘?閰梁 `git log --grep="Mode B"` ??????commit嚗112aa5c`?0ef06ee`?? Mode A ??銵?bugfix 銝?具?
  - **commit-grep ??嚗?026-06-15嚗?** 銝膩 `Mode B` ??*雓儔**蝺?*video ???撖衣里?詨歇?孵? NFA**嚗??賢?撖衣里?賂???video?ode B??憟? [`video/content_scripts/_audit/NARRATION-FAITHFULNESS-RUBRIC.md`](video/content_scripts/_audit/NARRATION-FAITHFULNESS-RUBRIC.md)嚗??嗉?瘙箏?璅?神?脖耨甇?commit body嚗???`git log --grep="NFA"` ??嚗?雓儔 `Mode B` ??嚗??拇?蝺毽?典?銝 grep嚗?
- **隞乩??? preamble嚗tyle ?曄??臭蝙?刻?2026-04-21 撖拇敺????嚗??箸???嚗?* 銝? `showonlyrefs`?雁??`\raggedbottom`+`[H]`??蝯 `exercise` ?啣?嚗??衣? `problems` newlist嚗???`csquotes autostyle`嚗??? `style_lint.py`嚗?憓?霈???閰?銝行?雓??砌??豢?靽?嚗??曉 X??閮鳴?2026-06-12 韏瑁?蝢拇擃??嗥?憿exercise` ?啣???氯? `CONTENT_SPEC.md` 禮14嚗洵銝???甇瑕?儔?酉嚗?026-06-13 韏?LaTeX 雓儔?游??祇?`legacy/tex_handout/`?ive 雓儔?寧 `handout/` ??HTML ??MathJax/KaTeX嚗S paginator嚗??洵 1嚗?嚗? ?? LaTeX preamble 璈鈭虫???冽 live 雓儔??蝚?3 ??撅祆風?脫扯釭嚗???linter ??`legacy/tex_handout/tools/book_style_lint.py`嚗???HTML ?Ｙ?銝???
- **蝯虫蝙?刻祟?貊?鈭支??抵??具??停?質???敶Ｗ?嚗?026-06-12 雿輻??瘙?嚗?* ?急摮詨??祟?豢?隞?*銝?**鈭文?皛輻? LaTeX ??`.md`嚗?Ｗ standalone HTML嚗athJax/KaTeX CDN嚗???摮詨皜脫?嚗??嗡??舐?仿霈?耦撘??抒??扯釭??瑼??冽迨???～?雿輻???株?瘙箝??梯正銝敺甇方齒??
- **瘥???頛芣撖怠?銋???HTML ?勗?嚗?026-06-15 雿輻??瘙?嚗?* 銝??鋆捱???嚗indings 閬?HTML??*?∪???頛芸摰寞撖恬?Mode A嚗 蝑?嚗閬?撖阡?撖怠?摰孵?Ｖ?隞?standalone HTML ?勗?**嚗athJax/KaTeX CDN????摮詨皜脫?嚗?????撖急挾?踝?locus嚗[source:]`嚗府頛?Mode B 蝯?嚗?雿輻???殷?銝??芸撠店鋆∠策????????[`handout/_audit/REVIEW-ch01-modec-candidates.html`](handout/_audit/REVIEW-ch01-modec-candidates.html) ?耦撘?瑼???`REVIEW-??applied.html` 銋?嚗??嚗?瘙箇阮????
- **撖拇 finding 靽桀?敺???甇詨祟?賂?2026-06-12 雿輻??瘙?嚗?* 靽桀? blocking嚗dvisory finding 敺?銝?湔摰??摰?????靽格????頝?頛芸祟?賂?Codex ????撠??荔?嚗Ⅱ隤耨?寞頨急????交????甇詨祟?貊?蝯???里?豢?瑼葉閮???

## 蝔?嚗極蝔遙??銵皞?嚗arpathy guidelines嚗?

皞 [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills)嚗ndrej Karpathy 撠?LLM 撖怎?撘虜閬???閫撖???*?嚗?* ??雓寞??芸??潮漲嚗蝣遙?銵???*?拍蝭?隞?`video/` ?Ｙ??uild 撌亙??祉?蝔?嚗極蝔極雿??銝?冽雓儔?批捆?啣神**?ode A ???撖漲隞誑?refer richness?? `[source:]`???芣?撖拇?皞?閬?[`video/CONTENT_METHODOLOGY.md`](video/CONTENT_METHODOLOGY.md)嚗?銝蝚?2 璇???撠?撘Ⅳ?? code嚗??摰寧?撟?

- **1. ?單?璆???嚗hink Before Coding嚗?閬?皜研?閬?韏瑕????日?雓?*
  - ?Ⅱ隤芸?身嚗?蝣箏?撠勗?嚗?閬?暺???
  - ??蝔株圾霈??典??箔?嚗?閬?暺銝??
  - ?蝪∪??瘜停雓?敹??????准?
  - ?∩?撠勗?銝????芾ㄐ銝?璆??嗅???
- **2. 蝪∪?芸?嚗implicity First嚗?撠? code 閫?捱??嚗?撖急?璈抒??梯正??*嚗???撘Ⅳ嚗??批捆蝭?嚗?
  - 銝?瘝◤閬????踝?銝銝甈⊥?code 撱箸鞊∪惜??
  - 銝?瘝◤閬????改??航身摰扼?銝銝?賜???撖恍隤方???
  - 撖思? 200 銵? 50 銵停憭停?神?????瘛勗極蝔葦????摰?摨西?????
- **3. 憭???撘耨?對?Surgical Changes嚗?????舐??唳嚗皜撌梯ˊ???摮?*
  - 銝??????啁? code?酉閫????嚗?閬?瑽?憯??梯正??
  - 瘥?Ｘ?憸冽嚗雿蹂???亦?撖急???
  - ??⊿???dead code嚗??箔???閬??芸嚗蝘駁??雿??孵??????典??import嚗??賂??賢???
  - 瑼ａ?嚗?銝銵??賜?亥蕭皞臬?雿輻??閬?嚗?銝??? review?? over-report 銝?湛???
- **4. ?格?撽??瑁?嚗oal-Driven Execution嚗?摰儔??璅?嚗?餈游??圈?霅???*
  - ?遙???撽??璅???撽??????粹?瘜撓?亙神皜祈岫??摰????耨 bug????撖怨??葫閰血?霈?????瑽?X???Ⅱ靽?敺葫閰阡??
  - 憭郊撽遙??蝯虫??陛?剛??恬?甇仿? ??撽?暺?????皞?撘瑕停?質銵艘?????啗?車撘望?皞???琿?閬?皜?


codex
目前 PowerShell 預設編碼把中文輸出成亂碼；我會用 UTF-8 重新讀 rubric，避免誤解 blocking/advisory 邊界。
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "Get-Content -Raw -Encoding UTF8 handout\\_audit\\FIGURE-AUDIT-RUBRIC.md" in C:\Users\user\Desktop\Calculus_handout
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'Get-Content -Raw -Encoding UTF8 CLAUDE.md' in C:\Users\user\Desktop\Calculus_handout
 succeeded in 383ms:
# CLAUDE.md

本檔案為本儲存庫提供給 AI 代理（Claude Code、Codex 等）的專案層級指引，是這份指引的**權威版本**；[`AGENTS.md`](AGENTS.md) 僅為指向本檔的指標,內容不重複。儲存庫的完整結構與建置規則以權威性文件 [`README.md`](README.md) 為準；內容撰寫規則以 [`CONTENT_SPEC.md`](CONTENT_SPEC.md) 為準。

## 文件撰寫語言

- **README 一律以繁體中文書寫。** 這包含根目錄的 [`README.md`](README.md) 以及子資料夾中屬於本專案的 README（例如 [`video/README.md`](video/README.md)）。新增或修改 README 時都比照辦理。
- **必要之處保留原文，不翻譯：** 程式碼區塊、檔案路徑與連結、shell 指令、環境變數、識別碼（scene id、export 名稱、欄位名）、以及專有名詞與技術術語（Manim、LaTeX、Gemini、TTS、CI、PR、Mode A/B/C 等）。
- 其餘散文、標題、表格的說明文字一律使用繁體中文。
- 第三方依賴（`.deps/`、`.deps_f5/`、`.deps_voiceover/`）與 git 工作樹（`.claude/worktrees/`）中的 README 不在此規則範圍內，不要改動。

## 影片渲染解析度

- **除非使用者特別要求，否則一律以 1080p 渲染**（`make.py --quality high`）。不要自行使用 `--quality low`（480p）或 `--quality 4k`。
- 4K 渲染（`--quality 4k`）僅在使用者明確指定「4K」或「正式交付」時使用。

## 付費 API 調用須先經同意

- **每次調用任何計費的外部 API（如 Gemini TTS、Gemini 文字／影像生成等）之前，都必須先取得使用者明確同意，不可自行調用。** 批次合成（例如整節旁白 TTS、整章重跑）一律先說明：這次要調用什麼模型、預估用量（beat 數／音訊秒數）與成本，經同意後才執行。
- 不計費、不連網的離線路徑不在此限，可逕行執行——例如 `tts.py --backend mock`（寫靜音 WAV 驗 manifest／時序）、本地 Manim render、ffmpeg mux/concat。
- 取得一次同意即代表該次明確說明的工作範圍獲准；範圍變更（換模型、加場景、重跑）需重新徵得同意。

## 跨對話記憶寫進版控文檔（不寫本地 memory）

- **做總結、記筆記、留任何跨對話／跨機器的知識時，一律寫進會 git 上去的文檔**，**不要只記在本地的 Claude memory**（`~/.claude/.../memory/`，含 `MEMORY.md`）。
- **原因：** 使用者常換電腦作業；本地 memory 不隨 repo 走、換機就消失，只有版控文檔會跟著 git 到每台機器。
- **寫哪裡：** 進度／狀態寫進該產線的 `REBUILD_STATUS.md`（既有的跨對話進度錨）；工具用法／參考寫進對應的 `README.md`；格式／資料流契約寫進 `DESIGN.md`；內容方法論寫進 `CONTENT_METHODOLOGY.md`。找不到合適的既有文檔時，先問使用者要放哪，不要默默只記進本地 memory。

## 撰寫／審查的既有慣例（原存於本地 memory，依上節規則搬進版控）

- **與使用者對話一律用繁體中文**（LaTeX／程式碼、套件名、檔名、技術術語保持英文原樣）。
- **做 doc／code review 時分清四級，不要混為一談：** ① 真衝突／違反既定規則（要修）② discoverability gap（補文件即可，非矛盾）③ editorial drift 風險（低優先，不是 finding）④ 非 finding（如示例覆蓋面差異）。**Framing：** 從「目前被 review 的樹的現況」出發，不要把 session 內未 commit／未 merge 的變更當既成事實；語義等價的用詞差異不算 inconsistency。Over-reporting 會稀釋真正高優先項。
- **三-mode 撰寫流程（root [`README.md`](README.md) §Mode B）下，Mode B 的稽核裁決與發現寫進該次修正 commit 的 message body**（subject ≤70 字、body 逐條：原本是什麼、為何不妥、改了什麼、引用證據），好讓未來對話用 `git log --grep="Mode B"` 撈回。參考 commit：`112aa5c`、`0ef06ee`。純 Mode A 或例行 bugfix 不適用。
  - **commit-grep 分流（2026-06-15）：** 上述 `Mode B` 是**講義**線。**video 旁白的忠實稽核已改名 NFA**（旁白忠實稽核，原 video「Mode B」；契約 [`video/content_scripts/_audit/NARRATION-FAITHFULNESS-RUBRIC.md`](video/content_scripts/_audit/NARRATION-FAITHFULNESS-RUBRIC.md)），其裁決同樣寫進修正 commit body，但用 `git log --grep="NFA"` 撈回（與講義 `Mode B` 分流，免兩條線混在同一 grep）。
- **以下四項 preamble／style 現狀是使用者 2026-04-21 審查後刻意保留的，勿再當遺漏重提：** 不開 `showonlyrefs`、維持 `\raggedbottom`+`[H]`、題組用 `exercise` 環境（不另立 `problems` newlist）、不加 `csquotes autostyle`（引號靠 `style_lint.py`）。情境真變了再重評，並明講「原本你選擇保留，但現在 X」。（註：2026-06-12 起講義本體不收習題、`exercise` 環境退場——見 `CONTENT_SPEC.md` §14；第三項僅餘歷史意義。註：2026-06-13 起 LaTeX 講義整套搬進 `legacy/tex_handout/`、live 講義改為 `handout/` 的 HTML 版（MathJax/KaTeX＋JS paginator），故第 1／2／4 項的 LaTeX preamble 機制亦不再適用於 live 講義、與第 3 項同屬歷史性質；引號 linter 即 `legacy/tex_handout/tools/book_style_lint.py`，不在 HTML 產線上跑。）
- **給使用者審核的交付物要用「打開就能讀」的形式（2026-06-12 使用者要求）：** 含數學式的審核文件**不要**交塞滿生 LaTeX 的 `.md`，改產出 standalone HTML（MathJax/KaTeX CDN，雙擊即開、數學即渲染）或其他可直接閱讀的形式。版控紀錄性質的文檔不在此限；凡「等使用者過目裁決」的東西一律照此辦理。
- **每完成一輪撰寫後也要產 HTML 報告（2026-06-15 使用者要求）：** 不只「待裁決」的候選／findings 要 HTML——**凡完成一輪內容撰寫（Mode A／C 等），都要對實際寫入的內容另產一份 standalone HTML 報告**（MathJax/KaTeX CDN、雙擊即開、數學即渲染），逐條呈現所寫段落＋locus＋`[source:]`＋該輪 Mode B 結果，供使用者過目，不要只在對話裡給文字摘要。比照 [`handout/_audit/REVIEW-ch01-modec-candidates.html`](handout/_audit/REVIEW-ch01-modec-candidates.html) 的形式，檔名用 `REVIEW-…-applied.html` 之類，與「候選／裁決稿」分開。
- **審核 finding 修完後必須回歸審核（2026-06-12 使用者要求）：** 修完 blocking／advisory finding 後，不可直接宣告完成——必須對修改過的項目重新跑一輪審核（Codex 或手動比對均可），確認修改本身沒有引入新問題。回歸審核的結果附在原稽核文檔中記錄。

## 程式／工程任務的行為準則（Karpathy guidelines）

源自 [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills)（Andrej Karpathy 對 LLM 寫程式常見毛病的觀察）。**取捨：** 偏向謹慎優先於速度；瑣碎任務自行斟酌。**適用範圍以 `video/` 產線、build 工具、腳本等程式／工程工作為限；不適用於講義內容撰寫**——Mode A 散文密度仍以「prefer richness、標 `[source:]`、不自我審查」為準（見 [`video/CONTENT_METHODOLOGY.md`](video/CONTENT_METHODOLOGY.md)），下方第 2 條的「最少程式碼」指 code，不指內容篇幅。

- **1. 想清楚再動手（Think Before Coding）——不要臆測、不要藏起困惑、把取捨攤開講。**
  - 明確說出假設；不確定就問，不要默默猜。
  - 有多種解讀時全部列出來，不要默默選一個。
  - 有更簡單的做法就講，必要時據理力爭。
  - 卡住就停下，指名哪裡不清楚，然後問。
- **2. 簡單優先（Simplicity First）——用最少的 code 解決問題，不寫投機性的東西。**（僅限程式碼，非內容篇幅）
  - 不做沒被要求的功能；不為一次性 code 建抽象層。
  - 不加沒被要求的「彈性／可設定性」；不為不可能的情境寫錯誤處理。
  - 寫了 200 行但 50 行就夠就重寫。自問：「資深工程師會不會嫌它過度複雜？」
- **3. 外科手術式修改（Surgical Changes）——只動非動不可的地方，只清自己製造的爛攤子。**
  - 不要順手「改善」相鄰的 code、註解或排版；不要重構沒壞的東西。
  - 比照既有風格，即使你會用別的寫法。
  - 看到無關的 dead code，提出來、不要擅自刪；只移除「因你的改動」而變成沒用到的 import／變數／函式。
  - 檢驗：每一行改動都能直接追溯回使用者的要求（與上節四級 review、不 over-report 一致）。
- **4. 目標驅動執行（Goal-Driven Execution）——先定義成功標準，再迴圈到驗證通過。**
  - 把任務轉成可驗證的目標：「加驗證」→「先為非法輸入寫測試再讓它過」；「修 bug」→「先寫能重現的測試再讓它過」；「重構 X」→「確保前後測試都過」。
  - 多步驟任務先給一個簡短計畫（步驟 → 驗證點）。成功標準夠強就能自行迴圈；「弄到能動」這種弱標準只會不斷需要釐清。


 succeeded in 392ms:
# 講義圖稽核 — RUBRIC（figure audit）

> **本審契約（單一真相來源）。** gate 1 = Claude `handout-figure-audit` subagent；視覺層的 Codex 第二讀者退為**定稿前的信心複核**（非每輪必跑，計費需同意）。
> **被審物：** 一張 **render 後的 PNG**（由 [`../_render/shot.mjs`](../_render/shot.mjs) 從 standalone 截圖產出），可參照該節 fragment 的 `figcaption`／`FIGS` 原始碼當語境。
> **依據：** [`../../CONTENT_SPEC.md`](../../CONTENT_SPEC.md) §10（圖規則）＋本檔維度（從 ch01 圖稽核實證蒸餾，見 `../_dev-archive/ch01/ch01_figure-audit.md`）。
> **性質：** 唯讀、advisory＋blocking 分流、不改檔。審「**畫出來**對不對、讀不讀得懂」，不是 copyedit。

## 維度（D1–D8；每條標 Blocking / Advisory）

**可讀性（看得清嗎）**
- **D1 Label collision／overlap**：label 互撞、撞軸、撞曲線或出界。**蓋住資訊 → Blocking**；輕微偏移不蓋字 → advisory。
- **D2 Out-of-bounds／clipping**：關鍵元素（轉折、交點、漸近線、標記點）被裁出可視區。**→ Blocking**。
- **D3 Viewing-window readability**：x/y-range 過大或過小，使曲線貼線／爆框、定性行為（漸近線、截距、彎曲、方向）不可辨。**→ Blocking**（等同畫錯）。
- **D4 Tick labels present／legible**：承載教學值的軸（讀圖題、需讀值處）缺刻度文字（如 `tex` 欄缺失、fallback 不認整數）。**讀者無法讀值 → Blocking**；非承載軸缺刻度 → advisory。

**心智模型（傳達對的觀念嗎）**
- **D5 Figure ↔ caption／prose 一致**：圖與 figcaption／定義／範例陳述矛盾（如雙側極限題只畫單側、ε-strip 標「對稱」卻畫不對稱）。**→ Blocking**。
- **D6 Math correctness vs source**（需 `FIGS` 原始碼）：座標／數值與課文不符 **→ Blocking**；純示意比例（標籤數學正確、形狀近似）**→ advisory**（沿用 ch01 A1 慣例，不修）。
- **D7 No-spoiler**：worked-example 圖洩露要學生算的量。**→ Blocking**。

**編碼穩健（§10）**
- **D8 Color-only／grayscale survival**：資訊只靠顏色區分、灰階印出後無法區辨（缺 redundant encoding：線型／標記／直接 label）。**→ Blocking**；palette 越界（非 blue／red／gray、無宣告）→ advisory。

## Non-findings（別當 finding）
- 刻意的示意近似比例（如直角三角形示意圖，標籤數學正確）。
- §10 允許的 callout、redundant curve label、宣告過的 palette exception。
- 純美學偏好（色深、字級），除非已影響可讀性。

## 輸出格式
1. `VERDICT` 行：視覺 blocking 數。
2. 逐條 finding：`圖 ID｜Figure #｜維度 D?｜Blocking|Advisory｜證據（座標/檔行/PNG 觀察）｜為何｜建議修法`。
3. 各乾淨維度一行（「D? 乾淨」）。
4. 末行結論：本圖／本節「**視覺 blocking 是否歸零**」。

**不 over-report、乾淨圖是有效結果。** 你是提議、不是行動：findings 交回裁決，不改檔（本來也唯讀）。


codex
Rubric 已讀完：我會按 D1–D8 分流，只報實際影響正確性或可讀性的問題；直角三角形比例近似、允許的冗餘標籤與單純美學偏好不列 finding。接下來核對 `FIGS` 與正文語境。
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "rg -n \"Figure 1\\.(1|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18|19|20|21)|figcaption|data-fig|hlt|restrict-x2|sine-not-1to1|restricted-sine|arcsin-triangle|restricted-cosine|restricted-tangent|arctan10-triangle|arctan-general-triangle|limit-same-near-a|read-limit-graph|one-sided-limits|piecewise-jump|one-sided-infinite|vertical-asymptote|ln-asymptote|floor-function|squeeze-theorem|squeeze-x2sin|precise-limit\" handout\\fragments\\ch01\\sec-1-*.html" in C:\Users\user\Desktop\Calculus_handout
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "rg -n \"const FIGS|\\\"hlt\\\"|\\\"restrict-x2\\\"|\\\"sine-not-1to1\\\"|\\\"restricted-sine\\\"|\\\"arcsin-triangle\\\"|\\\"restricted-cosine\\\"|\\\"restricted-tangent\\\"|\\\"arctan10-triangle\\\"|\\\"arctan-general-triangle\\\"|\\\"limit-same-near-a\\\"|\\\"read-limit-graph\\\"|\\\"one-sided-limits\\\"|\\\"piecewise-jump\\\"|\\\"one-sided-infinite\\\"|\\\"vertical-asymptote\\\"|\\\"ln-asymptote\\\"|\\\"floor-function\\\"|\\\"squeeze-theorem\\\"|\\\"squeeze-x2sin\\\"|\\\"precise-limit\\\"\" handout\\chapter1-print-standalone.html" in C:\Users\user\Desktop\Calculus_handout
2026-06-16T09:04:50.403816Z ERROR codex_core::tools::router: error=Exit code: 1
Wall time: 0.6 seconds
Output:
rg : The term 'rg' is not recognized as the name of a cmdlet, function, script file, or operable program. Check the spe
lling of the name, or if a path was included, verify that the path is correct and try again.
At line:2 char:1
+ rg -n "Figure 1\.(1|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18|19|20|21 ...
+ ~~
    + CategoryInfo          : ObjectNotFound: (rg:String) [], CommandNotFoundException
    + FullyQualifiedErrorId : CommandNotFoundException
 

2026-06-16T09:04:50.403815Z ERROR codex_core::tools::router: error=Exit code: 1
Wall time: 0.6 seconds
Output:
rg : The term 'rg' is not recognized as the name of a cmdlet, function, script file, or operable program. Check the spe
lling of the name, or if a path was included, verify that the path is correct and try again.
At line:2 char:1
+ rg -n "const FIGS|\"hlt\"|\"restrict-x2\"|\"sine-not-1to1\"|\"restric ...
+ ~~
    + CategoryInfo          : ObjectNotFound: (rg:String) [], CommandNotFoundException
    + FullyQualifiedErrorId : CommandNotFoundException
 

 exited 1 in 551ms:
rg : The term 'rg' is not recognized as the name of a cmdlet, function, script file, or operable program. Check the spe
lling of the name, or if a path was included, verify that the path is correct and try again.
At line:2 char:1
+ rg -n "Figure 1\.(1|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18|19|20|21 ...
+ ~~
    + CategoryInfo          : ObjectNotFound: (rg:String) [], CommandNotFoundException
    + FullyQualifiedErrorId : CommandNotFoundException
 

 exited 1 in 552ms:
rg : The term 'rg' is not recognized as the name of a cmdlet, function, script file, or operable program. Check the spe
lling of the name, or if a path was included, verify that the path is correct and try again.
At line:2 char:1
+ rg -n "const FIGS|\"hlt\"|\"restrict-x2\"|\"sine-not-1to1\"|\"restric ...
+ ~~
    + CategoryInfo          : ObjectNotFound: (rg:String) [], CommandNotFoundException
    + FullyQualifiedErrorId : CommandNotFoundException
 

codex
`rg` 不在這個環境裡，我改用 PowerShell 的 `Select-String` 搜尋同一批圖 ID，仍然只讀檔案。
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "Select-String -Path handout\\fragments\\ch01\\sec-1-*.html -Pattern 'Figure 1\\.(1|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18|19|20|21)|data-fig|hlt|restrict-x2|sine-not-1to1|restricted-sine|arcsin-triangle|restricted-cosine|restricted-tangent|arctan10-triangle|arctan-general-triangle|limit-same-near-a|read-limit-graph|one-sided-limits|piecewise-jump|one-sided-infinite|vertical-asymptote|ln-asymptote|floor-function|squeeze-theorem|squeeze-x2sin|precise-limit' -Encoding UTF8 | ForEach-Object { \""'$($_.Path):$($_.LineNumber):$($_.Line)" }' in C:\Users\user\Desktop\Calculus_handout
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "Select-String -Path handout\\chapter1-print-standalone.html -Pattern 'const FIGS|\"hlt\"|\"restrict-x2\"|\"sine-not-1to1\"|\"restricted-sine\"|\"arcsin-triangle\"|\"restricted-cosine\"|\"restricted-tangent\"|\"arctan10-triangle\"|\"arctan-general-triangle\"|\"limit-same-near-a\"|\"read-limit-graph\"|\"one-sided-limits\"|\"piecewise-jump\"|\"one-sided-infinite\"|\"vertical-asymptote\"|\"ln-asymptote\"|\"floor-function\"|\"squeeze-theorem\"|\"squeeze-x2sin\"|\"precise-limit\"' -Encoding UTF8 | ForEach-Object { \""'$($_.LineNumber):$($_.Line)" }' in C:\Users\user\Desktop\Calculus_handout
 succeeded in 351ms:
490:  <figure class="figure" data-fig="hlt">
614:        <figure class="figure" data-fig="restrict-x2">
714:  <figure class="figure" data-fig="sine-not-1to1">
724:  <figure class="figure" data-fig="restricted-sine">
793:          <figure class="figure" data-fig="arcsin-triangle">
809:  <figure class="figure" data-fig="restricted-cosine">
876:  <figure class="figure" data-fig="restricted-tangent">
925:          <figure class="figure" data-fig="arctan10-triangle">
949:        <figure class="figure" data-fig="arctan-general-triangle">
1051:  <figure class="figure" data-fig="limit-same-near-a">
1066:        <figure class="figure" data-fig="read-limit-graph">
1203:  <figure class="figure" data-fig="one-sided-limits">
1257:        <figure class="figure" data-fig="piecewise-jump">
1334:  <figure class="figure" data-fig="one-sided-infinite">
1377:        <figure class="figure" data-fig="vertical-asymptote">
1413:        <figure class="figure" data-fig="ln-asymptote">
1638:        <figure class="figure" data-fig="floor-function">
1660:  <figure class="figure" data-fig="squeeze-theorem">
1681:        <figure class="figure" data-fig="squeeze-x2sin">
1814:  <figure class="figure" data-fig="precise-limit">
2138:  const FIGS = {
2140:    "hlt": () => ({
2178:    "restrict-x2": () => ({
2198:    "sine-not-1to1": () => ({
2217:    "restricted-sine": () => ({
2231:    "restricted-cosine": () => ({
2245:    "restricted-tangent": () => ({
2261:    "arcsin-triangle": () => ({
2281:    "arctan10-triangle": () => ({
2301:    "arctan-general-triangle": () => ({
2323:    "limit-same-near-a": () => {
2361:    "read-limit-graph": () => ({
2382:    "one-sided-limits": () => ({
2397:    "one-sided-infinite": () => {
2415:    "vertical-asymptote": () => ({
2430:    "piecewise-jump": () => ({
2450:    "ln-asymptote": () => ({
2467:    "floor-function": () => {
2490:    "squeeze-theorem": () => ({
2512:    "squeeze-x2sin": () => ({
2534:    "precise-limit": () => {

 succeeded in 369ms:
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-1.html:93:      <p>A horizontal line \(y = c\) meets the graph of \(f\) at a point \((x, c)\) exactly when \(f(x) = c\). Therefore, <em>a function is one-to-one if and only if no horizontal line intersects its graph more than once</em>. If the line \(y = c\) meets the graph at two distinct points \((x_{1}, c)\) and \((x_{2}, c)\), then \(f(x_{1}) = c = f(x_{2})\) with \(x_{1} \neq x_{2}\), so \(f\) fails to be one-to-one. Conversely, if every horizontal line meets the graph at most once, each output corresponds to at most one input. Figure 1.1 shows the two situations.</p>
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-1.html:97:  <figure class="figure" data-fig="hlt">
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-1.html:98:    <figcaption><span class="fig-no">Figure 1.1</span> Geometric interpretation of the horizontal line test.</figcaption>
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-1.html:220:        This is exactly why \(\sqrt{x}\) means the <em>positive</em> square root: the convention makes the square root the inverse of the restricted squaring function. Figure 1.3 shows the restricted parabola, its inverse, and the mirror line \(y = x\). The same idea — restrict first, then invert — is the key to the inverse trigonometric functions of the next section.</p>
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-1.html:221:        <figure class="figure" data-fig="restrict-x2">
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-1.html:222:          <figcaption><span class="fig-no">Figure 1.3</span> The squaring function restricted to \([0, \infty)\), its inverse \(\sqrt{x}\), and the mirror line \(y = x\).</figcaption>
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-2.html:12:  <p>Consider the sine function on \(\mathbb{R}\). As Figure 1.4 shows, a horizontal line can intersect the graph of \(y = \sin x\) more than once, so \(\sin\) is not one-to-one on \(\mathbb{R}\).</p>
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-2.html:14:  <figure class="figure" data-fig="sine-not-1to1">
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-2.html:15:    <figcaption><span class="fig-no">Figure 1.4</span> The sine function on \(\mathbb{R}\) is not one-to-one.</figcaption>
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-2.html:22:  On this interval, \(\sin x\) is one-to-one and its values cover the range \([-1, 1]\). The restricted branch is shown in Figure 1.5.</p>
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-2.html:24:  <figure class="figure" data-fig="restricted-sine">
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-2.html:25:    <figcaption><span class="fig-no">Figure 1.5</span> Restricted branch of the sine function used to define \(\arcsin x\).</figcaption>
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-2.html:93:          <figure class="figure" data-fig="arcsin-triangle">
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-2.html:94:            <figcaption><span class="fig-no">Figure 1.6</span> Right triangle with \(\sin\theta = \tfrac{1}{3}\).</figcaption>
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-2.html:107:  <p>The cosine function is one-to-one on the interval \(0 \le x \le \pi\), shown in Figure 1.7.</p>
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-2.html:109:  <figure class="figure" data-fig="restricted-cosine">
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-2.html:110:    <figcaption><span class="fig-no">Figure 1.7</span> Restricted branch of the cosine function used to define \(\arccos x\).</figcaption>
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-2.html:174:  <p>The tangent function is one-to-one on the interval \(-\tfrac{\pi}{2} < x < \tfrac{\pi}{2}\), shown in Figure 1.8.</p>
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-2.html:176:  <figure class="figure" data-fig="restricted-tangent">
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-2.html:177:    <figcaption><span class="fig-no">Figure 1.8</span> Restricted branch of the tangent function used to define \(\arctan x\).</figcaption>
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-2.html:225:          <figure class="figure" data-fig="arctan10-triangle">
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-2.html:226:            <figcaption><span class="fig-no">Figure 1.9</span> Right triangle with \(\tan\theta = 10\).</figcaption>
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-2.html:249:        <figure class="figure" data-fig="arctan-general-triangle">
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-2.html:250:          <figcaption><span class="fig-no">Figure 1.10</span> Right triangle with \(\tan y = x\).</figcaption>
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-3.html:3:     audit-approved. Figure 1.7 -> 1.8; new Fig 1.9 (read-from-graph). -->
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-3.html:29:  <p>When we consider \(\lim_{x \to a} f(x)\), we are concerned with the values of \(f(x)\) for \(x\) near \(a\), not with the value of \(f(a)\). In particular, \(f(a)\) need not be defined at all. Figure 1.11 shows three functions whose values at \(a\) are different (and one is undefined), yet which all share the same limit as \(x \to a\).</p>
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-3.html:31:  <figure class="figure" data-fig="limit-same-near-a">
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-3.html:32:    <figcaption><span class="fig-no">Figure 1.11</span> Three functions with the same limit as \(x \to a\).</figcaption>
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-3.html:40:        <p>The graph of a function \(f\) is shown in Figure 1.12. Evaluate the following, or state that the limit does not exist:</p>
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-3.html:46:        <figure class="figure" data-fig="read-limit-graph">
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-3.html:47:          <figcaption><span class="fig-no">Figure 1.12</span> A function whose limit at \(x = 2\) differs from its value there.</figcaption>
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-4.html:27:  <figure class="figure" data-fig="one-sided-limits">
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-4.html:28:    <figcaption><span class="fig-no">Figure 1.13</span> A function whose left-hand and right-hand limits at \(a\) are different.</figcaption>
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-4.html:81:        <figure class="figure" data-fig="piecewise-jump">
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-4.html:82:          <figcaption><span class="fig-no">Figure 1.14</span> Graph of the piecewise function of Example 1.20, showing a jump at \(x = 2\).</figcaption>
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-4.html:156:  are defined analogously. The four cases are illustrated in Figure 1.15.</p>
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-4.html:158:  <figure class="figure" data-fig="one-sided-infinite">
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-4.html:159:    <figcaption><span class="fig-no">Figure 1.15</span> The four typical one-sided infinite limits.</figcaption>
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-4.html:200:        At least one one-sided limit is infinite, so the line \(x = 3\) is a vertical asymptote, as shown in Figure 1.16.</p>
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-4.html:201:        <figure class="figure" data-fig="vertical-asymptote">
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-4.html:202:          <figcaption><span class="fig-no">Figure 1.16</span> The graph of \(y = \frac{2x}{x - 3}\) has a vertical asymptote at \(x = 3\).</figcaption>
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-4.html:237:        <figure class="figure" data-fig="ln-asymptote">
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-4.html:238:          <figcaption><span class="fig-no">Figure 1.17</span> The graph of \(y = \ln x\) has a vertical asymptote at \(x = 0\).</figcaption>
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-5.html:215:        <figure class="figure" data-fig="floor-function">
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-5.html:216:          <figcaption><span class="fig-no">Figure 1.18</span> The greatest integer function \([x]\) has a jump at every integer.</figcaption>
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-5.html:237:  <figure class="figure" data-fig="squeeze-theorem">
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-5.html:238:    <figcaption><span class="fig-no">Figure 1.19</span> The squeeze theorem: \(f\) is trapped between \(g\) and \(h\), which share the same limit \(L\).</figcaption>
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-5.html:258:        <figure class="figure" data-fig="squeeze-x2sin">
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-5.html:259:          <figcaption><span class="fig-no">Figure 1.20</span> The graph of \(y = x^{2}\sin(1/x)\) squeezed between \(y = -x^{2}\) and \(y = x^{2}\).</figcaption>
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-6.html:3:     (O1.6-d), 2026-06-12, audit-approved. Figure 1.11 -> 1.13. -->
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-6.html:59:  <p>Figure 1.21 gives a geometric reading of the definition. If \(x\) is restricted to the punctured interval \((a - \delta, a + \delta)\) with \(x \neq a\), then the corresponding values of \(f(x)\) lie in the target strip \((L - \varepsilon, L + \varepsilon)\). The value \(f(a)\) itself may be different from \(L\): the limit depends only on the behavior of \(f(x)\) when \(x\) is close to \(a\), not on what happens at \(x = a\).</p>
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-6.html:61:  <figure class="figure" data-fig="precise-limit">
C:\Users\user\Desktop\Calculus_handout\handout\fragments\ch01\sec-1-6.html:62:    <figcaption><span class="fig-no">Figure 1.21</span> Geometric interpretation of the \(\varepsilon\)-\(\delta\) definition; \(\delta\) depends on \(\varepsilon\).</figcaption>

codex
我已定位 20 個 `data-fig` 和 fragment caption。現在讀 `const FIGS` 的完整程式區塊，逐張用原始座標算是否與教學陳述一致。
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command '$lines = Get-Content -Encoding UTF8 handout'"\\chapter1-print-standalone.html; for ("'$i=2138; $i -le 2585; $i++) { if ($i -le $lines.Length) { '"'{0}:{1}' -f "'$i, $lines[$i-1] } }' in C:\Users\user\Desktop\Calculus_handout
 succeeded in 302ms:
2138:  const FIGS = {
2139:    /* ---------------- §1.1 ---------------- */
2140:    "hlt": () => ({
2141:      layout: "pair",
2142:      panels: [
2143:        {
2144:          svg: buildPlot({
2145:            w: 250, h: 200, xmin: -2.3, xmax: 2.2, ymin: -2.1, ymax: 2.3,
2146:            xlabel: "x", ylabel: "y", aria: "A one-to-one line crossed once by a horizontal line.",
2147:            items: [
2148:              { type: "curve", fn: (x) => x, domain: [-1.5, 1.45], cls: "curve" },
2149:              { type: "hline", y: 1, from: -2.1, to: 1.3, cls: "refline" },
2150:              { type: "dot", x: 1, y: 1 },
2151:              { type: "text", x: 1.55, y: 1.62, tex: "f", cls: "a-curve" },
2152:              { type: "text", x: 1.42, y: 1.0, tex: "y=c", cls: "a-ref", anchor: "start", vAnchor: "bottom", dy: -2 },
2153:              { type: "text", x: 1.06, y: 0.46, tex: "(x_1,\\,c)", cls: "a-pt", anchor: "start" },
2154:            ],
2155:          }),
2156:          note: "One-to-one \u2014 a line meets the graph at most once.",
2157:        },
2158:        {
2159:          svg: buildPlot({
2160:            w: 250, h: 200, xmin: -2.3, xmax: 2.2, ymin: -2.1, ymax: 2.3,
2161:            xlabel: "x", ylabel: "y", aria: "A parabola crossed twice by a horizontal line.",
2162:            items: [
2163:              { type: "curve", fn: (x) => 1.15 * x * x, domain: [-1.4, 1.4], cls: "curve" },
2164:              { type: "hline", y: 1.25, from: -1.85, to: 1.85, cls: "refline" },
2165:              { type: "dot", x: -1.043, y: 1.25 },
2166:              { type: "dot", x: 1.043, y: 1.25 },
2167:              { type: "text", x: 1.5, y: 2.18, tex: "f", cls: "a-curve" },
2168:              { type: "text", x: 1.9, y: 1.25, tex: "y=c", cls: "a-ref", anchor: "start", vAnchor: "bottom", dy: -1 },
2169:              { type: "text", x: -1.2, y: 0.98, tex: "(x_1,\\,c)", cls: "a-pt", anchor: "end" },
2170:              { type: "text", x: 1.2, y: 0.98, tex: "(x_2,\\,c)", cls: "a-pt", anchor: "start" },
2171:            ],
2172:          }),
2173:          note: "Not one-to-one \u2014 a line meets the graph more than once.",
2174:        },
2175:      ],
2176:    }),
2177:
2178:    "restrict-x2": () => ({
2179:      layout: "single",
2180:      panels: [{
2181:        svg: buildPlot({
2182:          w: 300, h: 300, xmin: -0.4, xmax: 2.7, ymin: -0.4, ymax: 2.7,
2183:          xlabel: "x", ylabel: "y",
2184:          aria: "The squaring function restricted to the nonnegative reals, its inverse square root, and the mirror line y equals x.",
2185:          items: [
2186:            { type: "curve", fn: (x) => x, domain: [0, 2.5], cls: "refline" },
2187:            { type: "curve", fn: (x) => x * x, domain: [0, 1.6], cls: "curve" },
2188:            { type: "curve", fn: (x) => Math.sqrt(x), domain: [0, 2.5], cls: "curve" },
2189:            { type: "text", x: 1.02, y: 2.25, tex: "f(x)=x^{2}", cls: "a-curve", anchor: "end" },
2190:            { type: "text", x: 2.5, y: 1.5, tex: "f^{-1}(x)=\\sqrt{x}", cls: "a-curve", anchor: "start" },
2191:            { type: "text", x: 2.32, y: 2.5, tex: "y=x", cls: "a-ref", anchor: "start" },
2192:          ],
2193:        }),
2194:      }],
2195:    }),
2196:
2197:    /* ---------------- §1.2 ---------------- */
2198:    "sine-not-1to1": () => ({
2199:      layout: "single",
2200:      panels: [{
2201:        svg: buildPlot({
2202:          w: 620, h: 220, xmin: -6.9, xmax: 7.4, ymin: -1.35, ymax: 1.35,
2203:          pad: { t: 16, r: 18, b: 26, l: 18 },
2204:          xlabel: "x", ylabel: "y", aria: "The sine function on the real line is not one-to-one.",
2205:          xticks: [{ x: -2 * P() }, { x: -P() }, { x: P() }, { x: 2 * P() }],
2206:          yticks: [{ y: -1, tex: "-1" }, { y: 1, tex: "1" }],
2207:          items: [
2208:            { type: "curve", fn: (x) => Math.sin(x), domain: [-6.8, 6.8], samples: 360, cls: "curve" },
2209:            { type: "hline", y: 0.5, from: -6.8, to: 6.8, cls: "refline" },
2210:            ...[0.5236, 2.618, 6.807, -3.6652, -5.7596].map((x) => ({ type: "dot", x, y: 0.5, r: 2.6 })),
2211:            { type: "text", x: 3.25, y: 1.0, tex: "\\sin x", cls: "a-curve", anchor: "start" },
2212:            { type: "text", x: 6.95, y: 0.5, tex: "y=c", cls: "a-ref", anchor: "start", vAnchor: "bottom", dy: -1 },
2213:          ],
2214:        }),
2215:      }],
2216:    }),
2217:    "restricted-sine": () => ({
2218:      layout: "single",
2219:      panels: [{
2220:        svg: buildPlot({
2221:          w: 380, h: 260, xmin: -1.95, xmax: 1.95, ymin: -1.25, ymax: 1.25,
2222:          xlabel: "x", ylabel: "y", aria: "Restricted branch of sine.",
2223:          xticks: [{ x: -P() / 2 }, { x: P() / 2 }], yticks: [{ y: -1, tex: "-1" }, { y: 1, tex: "1" }],
2224:          items: [
2225:            { type: "curve", fn: (x) => Math.sin(x), domain: [-P() / 2, P() / 2], cls: "curve" },
2226:            { type: "text", x: 1.02, y: 1.12, tex: "\\sin x", cls: "a-curve", anchor: "start" },
2227:          ],
2228:        }),
2229:      }],
2230:    }),
2231:    "restricted-cosine": () => ({
2232:      layout: "single",
2233:      panels: [{
2234:        svg: buildPlot({
2235:          w: 380, h: 200, xmin: -0.4, xmax: 3.6, ymin: -1.35, ymax: 1.75,
2236:          xlabel: "x", ylabel: "y", aria: "Restricted branch of cosine.",
2237:          xticks: [{ x: P() }], yticks: [{ y: -1, tex: "-1" }, { y: 1, tex: "1" }],
2238:          items: [
2239:            { type: "curve", fn: (x) => Math.cos(x), domain: [0, P()], cls: "curve" },
2240:            { type: "text", x: 1.25, y: 0.8, tex: "\\cos x", cls: "a-curve", anchor: "start" },
2241:          ],
2242:        }),
2243:      }],
2244:    }),
2245:    "restricted-tangent": () => ({
2246:      layout: "single",
2247:      panels: [{
2248:        svg: buildPlot({
2249:          w: 320, h: 320, xmin: -1.95, xmax: 1.95, ymin: -5, ymax: 5,
2250:          xlabel: "x", ylabel: "y", aria: "Restricted branch of tangent.",
2251:          xticks: [{ x: -P() / 2 }, { x: P() / 2 }],
2252:          items: [
2253:            { type: "vline", x: -P() / 2, cls: "refline" },
2254:            { type: "vline", x: P() / 2, cls: "refline" },
2255:            { type: "curve", fn: (x) => Math.tan(x), domain: [-1.37, 1.37], samples: 300, cls: "curve" },
2256:            { type: "text", x: 0.35, y: 2.8, tex: "\\tan x", cls: "a-curve", anchor: "start" },
2257:          ],
2258:        }),
2259:      }],
2260:    }),
2261:    "arcsin-triangle": () => ({
2262:      layout: "single",
2263:      panels: [{
2264:        svg: buildPlot({
2265:          w: 300, h: 130, xmin: -0.3, xmax: 3.5, ymin: -0.35, ymax: 1.45, axes: false,
2266:          aria: "Right triangle with angle theta, opposite 1, adjacent 2 root 2, hypotenuse 3.",
2267:          items: [
2268:            { type: "seg", x1: 0, y1: 0, x2: 3, y2: 0, cls: "curve" },
2269:            { type: "seg", x1: 3, y1: 0, x2: 3, y2: 1, cls: "curve" },
2270:            { type: "seg", x1: 3, y1: 1, x2: 0, y2: 0, cls: "curve" },
2271:            { type: "seg", x1: 2.78, y1: 0, x2: 2.78, y2: 0.22, cls: "axis" },
2272:            { type: "seg", x1: 2.78, y1: 0.22, x2: 3, y2: 0.22, cls: "axis" },
2273:            { type: "text", x: 0.66, y: 0.13, tex: "\\theta", cls: "a-pt", anchor: "start" },
2274:            { type: "text", x: 1.5, y: 0, tex: "2\\sqrt{2}", cls: "a-pt", anchor: "middle", vAnchor: "top", dy: 4 },
2275:            { type: "text", x: 3, y: 0.5, tex: "1", cls: "a-pt", anchor: "start", dx: 4 },
2276:            { type: "text", x: 1.25, y: 0.62, tex: "3", cls: "a-pt", anchor: "end" },
2277:          ],
2278:        }),
2279:      }],
2280:    }),
2281:    "arctan10-triangle": () => ({
2282:      layout: "single",
2283:      panels: [{
2284:        svg: buildPlot({
2285:          w: 240, h: 180, xmin: -0.3, xmax: 2.8, ymin: -0.35, ymax: 2.0, axes: false,
2286:          aria: "Right triangle with angle theta, adjacent 1, opposite 10, hypotenuse square root of 101.",
2287:          items: [
2288:            { type: "seg", x1: 0, y1: 0, x2: 2, y2: 0, cls: "curve" },
2289:            { type: "seg", x1: 2, y1: 0, x2: 2, y2: 1.5, cls: "curve" },
2290:            { type: "seg", x1: 2, y1: 1.5, x2: 0, y2: 0, cls: "curve" },
2291:            { type: "seg", x1: 1.78, y1: 0, x2: 1.78, y2: 0.22, cls: "axis" },
2292:            { type: "seg", x1: 1.78, y1: 0.22, x2: 2, y2: 0.22, cls: "axis" },
2293:            { type: "text", x: 0.46, y: 0.18, tex: "\\theta", cls: "a-pt", anchor: "start" },
2294:            { type: "text", x: 1, y: 0, tex: "1", cls: "a-pt", anchor: "middle", vAnchor: "top", dy: 4 },
2295:            { type: "text", x: 2, y: 0.75, tex: "10", cls: "a-pt", anchor: "start", dx: 4 },
2296:            { type: "text", x: 0.8, y: 0.9, tex: "\\sqrt{101}", cls: "a-pt", anchor: "end" },
2297:          ],
2298:        }),
2299:      }],
2300:    }),
2301:    "arctan-general-triangle": () => ({
2302:      layout: "single",
2303:      panels: [{
2304:        svg: buildPlot({
2305:          w: 240, h: 180, xmin: -0.3, xmax: 2.8, ymin: -0.35, ymax: 2.0, axes: false,
2306:          aria: "Right triangle with angle y, adjacent 1, opposite x, hypotenuse square root of 1 plus x squared.",
2307:          items: [
2308:            { type: "seg", x1: 0, y1: 0, x2: 2, y2: 0, cls: "curve" },
2309:            { type: "seg", x1: 2, y1: 0, x2: 2, y2: 1.5, cls: "curve" },
2310:            { type: "seg", x1: 2, y1: 1.5, x2: 0, y2: 0, cls: "curve" },
2311:            { type: "seg", x1: 1.78, y1: 0, x2: 1.78, y2: 0.22, cls: "axis" },
2312:            { type: "seg", x1: 1.78, y1: 0.22, x2: 2, y2: 0.22, cls: "axis" },
2313:            { type: "text", x: 0.46, y: 0.18, tex: "y", cls: "a-pt", anchor: "start" },
2314:            { type: "text", x: 1, y: 0, tex: "1", cls: "a-pt", anchor: "middle", vAnchor: "top", dy: 4 },
2315:            { type: "text", x: 2, y: 0.75, tex: "x", cls: "a-pt", anchor: "start", dx: 4 },
2316:            { type: "text", x: 0.8, y: 0.9, tex: "\\sqrt{1+x^{2}}", cls: "a-pt", anchor: "end" },
2317:          ],
2318:        }),
2319:      }],
2320:    }),
2321:
2322:    /* ---------------- §1.3 ---------------- */
2323:    "limit-same-near-a": () => {
2324:      const base = (extra) => buildPlot(Object.assign({
2325:        w: 250, h: 200, xmin: 0, xmax: 3.7, ymin: 0, ymax: 14,
2326:        pad: { t: 14, r: 16, b: 20, l: 18 }, xlabel: "x", ylabel: "y",
2327:        aria: "A function approaching L as x approaches a.",
2328:      }, extra));
2329:      const labels = [
2330:        { type: "hline", y: 8, from: 0, to: 3, cls: "refline" },
2331:        { type: "text", x: 3, y: 0, tex: "a", cls: "a-pt", anchor: "middle", vAnchor: "top", dy: 5 },
2332:        { type: "text", x: 0, y: 8, tex: "L", cls: "a-pt", anchor: "end", dx: -4 },
2333:      ];
2334:      return {
2335:        layout: "triple",
2336:        panels: [
2337:          {
2338:            svg: base({ items: [{ type: "curve", fn: pow2, domain: [0.45, 3.45], cls: "curve" }, ...labels, { type: "dot", x: 3, y: 8 }] }),
2339:            note: "\\(f(a) = L\\)",
2340:          },
2341:          {
2342:            svg: base({ items: [
2343:              { type: "curve", fn: pow2, domain: [0.45, 2.95], cls: "curve" },
2344:              { type: "curve", fn: pow2, domain: [3.05, 3.45], cls: "curve" },
2345:              ...labels, { type: "dot", x: 3, y: 8, hollow: true }, { type: "dot", x: 3, y: 5 },
2346:            ] }),
2347:            note: "\\(f(a) \\neq L\\)",
2348:          },
2349:          {
2350:            svg: base({ items: [
2351:              { type: "curve", fn: pow2, domain: [0.45, 2.95], cls: "curve" },
2352:              { type: "curve", fn: pow2, domain: [3.05, 3.45], cls: "curve" },
2353:              ...labels, { type: "dot", x: 3, y: 8, hollow: true },
2354:            ] }),
2355:            note: "\\(f(a)\\) is undefined",
2356:          },
2357:        ],
2358:      };
2359:    },
2360:
2361:    "read-limit-graph": () => ({
2362:      layout: "single",
2363:      panels: [{
2364:        svg: buildPlot({
2365:          w: 460, h: 280, xmin: -3.3, xmax: 2.9, ymin: -2.7, ymax: 2.8,
2366:          xlabel: "x", ylabel: "y",
2367:          aria: "A function with limit 1 at x = -2, limit 0 at x = 0, and limit 2 at x = 2, although f(2) = -2.",
2368:          xticks: [{ x: -2, tex: "-2" }, { x: 2, tex: "2" }],
2369:          yticks: [{ y: -2, tex: "-2" }, { y: 1, tex: "1" }, { y: 2, tex: "2" }],
2370:          items: [
2371:            { type: "curve", fn: (x) => -0.0375 * x * x * x + 0.375 * x * x + 0.4 * x, domain: [-2.8, 1.98], samples: 200, cls: "curve" },
2372:            { type: "curve", fn: (x) => -0.0375 * x * x * x + 0.375 * x * x + 0.4 * x, domain: [2.02, 2.7], samples: 50, cls: "curve" },
2373:            { type: "dot", x: 2, y: 2, hollow: true },
2374:            { type: "dot", x: 2, y: -2 },
2375:            { type: "text", x: -2.7, y: 1.55, tex: "y=f(x)", cls: "a-curve", anchor: "start" },
2376:          ],
2377:        }),
2378:      }],
2379:    }),
2380:
2381:    /* ---------------- §1.4 ---------------- */
2382:    "one-sided-limits": () => ({
2383:      layout: "single",
2384:      panels: [{
2385:        svg: buildPlot({
2386:          w: 420, h: 260, xmin: -0.5, xmax: 4.5, ymin: -0.5, ymax: 3.2,
2387:          xlabel: "x", ylabel: "y", aria: "Different left and right limits at a.",
2388:          xticks: [{ x: 2, tex: "a" }], yticks: [{ y: 1, tex: "L_1" }, { y: 2, tex: "L_2" }],
2389:          items: [
2390:            { type: "curve", fn: (x) => 1 + 0.25 * (x - 2) * (x - 2), domain: [0.2, 1.95], cls: "curve" },
2391:            { type: "curve", fn: (x) => 2 + 0.2 * (x - 2) * (x - 2), domain: [2.05, 4.2], cls: "curve" },
2392:            { type: "dot", x: 2, y: 1, hollow: true }, { type: "dot", x: 2, y: 2, hollow: true },
2393:          ],
2394:        }),
2395:      }],
2396:    }),
2397:    "one-sided-infinite": () => {
2398:      const mk = (fn, dom, ymin, ymax) => buildPlot({
2399:        w: 240, h: 210, xmin: -0.2, xmax: 3.2, ymin, ymax,
2400:        pad: { t: 14, r: 14, b: 20, l: 16 }, xlabel: "x", ylabel: "y",
2401:        aria: "A one-sided infinite limit.",
2402:        xticks: [{ x: 2, tex: "a" }],
2403:        items: [{ type: "vline", x: 2, cls: "refline" }, { type: "curve", fn, domain: dom, samples: 200, cls: "curve" }],
2404:      });
2405:      return {
2406:        layout: "grid",
2407:        panels: [
2408:          { svg: mk((x) => 1 / (2 - x), [0.25, 1.68], -0.55, 3.2), note: "\\(\\lim_{x\\to a^{-}} f(x)=\\infty\\)" },
2409:          { svg: mk((x) => 1 / (x - 2), [2.32, 3.0], -0.55, 3.2), note: "\\(\\lim_{x\\to a^{+}} f(x)=\\infty\\)" },
2410:          { svg: mk((x) => -1 / (2 - x), [0.25, 1.68], -3.0, 0.75), note: "\\(\\lim_{x\\to a^{-}} f(x)=-\\infty\\)" },
2411:          { svg: mk((x) => -1 / (x - 2), [2.32, 3.0], -3.0, 0.75), note: "\\(\\lim_{x\\to a^{+}} f(x)=-\\infty\\)" },
2412:        ],
2413:      };
2414:    },
2415:    "vertical-asymptote": () => ({
2416:      layout: "single",
2417:      panels: [{
2418:        svg: buildPlot({
2419:          w: 420, h: 260, xmin: -1, xmax: 7, ymin: -20, ymax: 20,
2420:          xlabel: "x", ylabel: "y", aria: "Graph with a vertical asymptote at x = 3.",
2421:          xticks: [{ x: 3, tex: "3" }], yticks: [{ y: 2, tex: "2" }],
2422:          items: [
2423:            { type: "vline", x: 3, cls: "refline" },
2424:            { type: "curve", fn: (x) => (2 * x) / (x - 3), domain: [-0.8, 2.9], samples: 200, cls: "curve" },
2425:            { type: "curve", fn: (x) => (2 * x) / (x - 3), domain: [3.1, 6.8], samples: 200, cls: "curve" },
2426:          ],
2427:        }),
2428:      }],
2429:    }),
2430:    "piecewise-jump": () => ({
2431:      layout: "single",
2432:      panels: [{
2433:        svg: buildPlot({
2434:          w: 360, h: 240, xmin: -0.5, xmax: 5, ymin: -0.5, ymax: 4.5,
2435:          xlabel: "x", ylabel: "y",
2436:          aria: "Piecewise function with jump at x equals 2: left limit is 3, right limit is 2.",
2437:          xticks: [{ x: 2, tex: "2" }],
2438:          yticks: [{ y: 2, tex: "2" }, { y: 3, tex: "3" }],
2439:          items: [
2440:            { type: "curve", fn: (x) => x + 1, domain: [-0.3, 1.97], cls: "curve" },
2441:            { type: "curve", fn: (x) => 4 - x, domain: [2.03, 4.5], cls: "curve" },
2442:            { type: "dot", x: 2, y: 3, hollow: true },
2443:            { type: "dot", x: 2, y: 2 },
2444:            { type: "text", x: 0.05, y: 2.3, tex: "y=x+1", cls: "a-curve", anchor: "start" },
2445:            { type: "text", x: 3.5, y: 1.0, tex: "y=4-x", cls: "a-curve", anchor: "start" },
2446:          ],
2447:        }),
2448:      }],
2449:    }),
2450:    "ln-asymptote": () => ({
2451:      layout: "single",
2452:      panels: [{
2453:        svg: buildPlot({
2454:          w: 340, h: 260, xmin: -0.8, xmax: 5.5, ymin: -2.8, ymax: 2.5,
2455:          xlabel: "x", ylabel: "y",
2456:          aria: "Graph of y equals natural log of x approaching negative infinity near x equals 0.",
2457:          xticks: [{ x: 1, tex: "1" }],
2458:          items: [
2459:            { type: "curve", fn: (x) => Math.log(x), domain: [0.09, 5.2], samples: 300, cls: "curve" },
2460:            { type: "text", x: 4.3, y: 2.0, tex: "y=\\ln x", cls: "a-curve", anchor: "start" },
2461:          ],
2462:        }),
2463:      }],
2464:    }),
2465:
2466:    /* ---------------- §1.5 ---------------- */
2467:    "floor-function": () => {
2468:      const steps = [];
2469:      for (var n = -1; n <= 4; n++) {
2470:        steps.push({ type: "seg", x1: n, y1: n, x2: n + 1, y2: n, cls: "curve" });
2471:        steps.push({ type: "dot", x: n, y: n });
2472:        steps.push({ type: "dot", x: n + 1, y: n, hollow: true });
2473:      }
2474:      return {
2475:        layout: "single",
2476:        panels: [{
2477:          svg: buildPlot({
2478:            w: 380, h: 320, xmin: -1.5, xmax: 5.5, ymin: -1.8, ymax: 4.8,
2479:            xlabel: "x", ylabel: "y",
2480:            aria: "The greatest integer function, a step function with jumps at each integer.",
2481:            xticks: [{ x: -1, tex: "-1" }, { x: 1, tex: "1" }, { x: 2, tex: "2" }, { x: 3, tex: "3" }, { x: 4, tex: "4" }],
2482:            yticks: [{ y: 1, tex: "1" }, { y: 2, tex: "2" }, { y: 3, tex: "3" }, { y: 4, tex: "4" }],
2483:            items: steps.concat([
2484:              { type: "text", x: 4.8, y: 4.5, tex: "y=[x]", cls: "a-curve", anchor: "start" },
2485:            ]),
2486:          }),
2487:        }],
2488:      };
2489:    },
2490:    "squeeze-theorem": () => ({
2491:      layout: "single",
2492:      panels: [{
2493:        svg: buildPlot({
2494:          w: 420, h: 280, xmin: -0.5, xmax: 5.5, ymin: -0.5, ymax: 4.2,
2495:          xlabel: "x", ylabel: "y",
2496:          aria: "Squeeze theorem: f is trapped between g and h, all converging to L at x equals a.",
2497:          xticks: [{ x: 2.5, tex: "a" }],
2498:          items: [
2499:            { type: "curve", fn: (x) => 2 + 0.4 * Math.pow(x - 2.5, 2), domain: [0.2, 4.9], cls: "refline" },
2500:            { type: "curve", fn: (x) => 2 - 0.4 * Math.pow(x - 2.5, 2), domain: [0.2, 4.9], cls: "refline" },
2501:            { type: "curve", fn: (x) => 2 + 0.3 * Math.pow(x - 2.5, 2) * Math.sin(5 * x), domain: [0.2, 4.9], samples: 400, cls: "curve" },
2502:            { type: "hline", y: 2, from: 0, to: 2.5, cls: "refline" },
2503:            { type: "dot", x: 2.5, y: 2 },
2504:            { type: "text", x: 0, y: 2, tex: "L", cls: "a-pt", anchor: "end", dx: -4 },
2505:            { type: "text", x: 5, y: 3.8, tex: "h", cls: "a-ref", anchor: "start" },
2506:            { type: "text", x: 5, y: 0.2, tex: "g", cls: "a-ref", anchor: "start" },
2507:            { type: "text", x: 4.5, y: 2.7, tex: "f", cls: "a-curve", anchor: "start" },
2508:          ],
2509:        }),
2510:      }],
2511:    }),
2512:    "squeeze-x2sin": () => ({
2513:      layout: "single",
2514:      panels: [{
2515:        svg: buildPlot({
2516:          w: 400, h: 280, xmin: -1.2, xmax: 1.2, ymin: -0.8, ymax: 1.2,
2517:          xlabel: "x", ylabel: "y",
2518:          aria: "x squared sin(1/x) squeezed between y equals x squared and y equals negative x squared.",
2519:          items: [
2520:            { type: "curve", fn: (x) => x * x, domain: [-1.1, 1.1], cls: "refline" },
2521:            { type: "curve", fn: (x) => -x * x, domain: [-1.1, 1.1], cls: "refline" },
2522:            { type: "curve", fn: (x) => x * x * Math.sin(1 / x), domain: [-1.1, -0.01], samples: 600, cls: "curve" },
2523:            { type: "curve", fn: (x) => x * x * Math.sin(1 / x), domain: [0.01, 1.1], samples: 600, cls: "curve" },
2524:            { type: "dot", x: 0, y: 0 },
2525:            { type: "text", x: 0.75, y: 0.85, tex: "x^{2}", cls: "a-ref", anchor: "end" },
2526:            { type: "text", x: 0.75, y: -0.55, tex: "-x^{2}", cls: "a-ref", anchor: "end" },
2527:            { type: "text", x: -0.35, y: 0.2, tex: "x^{2}\\!\\sin\\tfrac{1}{x}", cls: "a-curve", anchor: "end" },
2528:          ],
2529:        }),
2530:      }],
2531:    }),
2532:
2533:    /* ---------------- §1.6 ---------------- */
2534:    "precise-limit": () => {
2535:      const Lm = 6.150845, Lp = 9.849155;
2536:      return {
2537:        layout: "single",
2538:        panels: [{
2539:          svg: buildPlot({
2540:            w: 460, h: 300, xmin: 0, xmax: 3.8, ymin: 0, ymax: 14,
2541:            pad: { t: 16, r: 18, b: 24, l: 58 }, xlabel: "x", ylabel: "y",
2542:            aria: "Geometric interpretation of the epsilon-delta definition.",
2543:            items: [
2544:              { type: "curve", fn: pow2, domain: [0.45, 2.95], cls: "curve" },
2545:              { type: "curve", fn: pow2, domain: [3.05, 3.45], cls: "curve" },
2546:              { type: "hline", y: Lm, from: 0, to: 3.8, cls: "refline" },
2547:              { type: "hline", y: Lp, from: 0, to: 3.8, cls: "refline" },
2548:              { type: "vline", x: 2.7, cls: "refline" },
2549:              { type: "vline", x: 3.3, cls: "refline" },
2550:              { type: "dot", x: 3, y: 8, hollow: true },
2551:              { type: "dot", x: 3, y: 11.6 },
2552:              { type: "dot", x: 3.3, y: Lp, r: 1.8 },
2553:              { type: "text", x: 2.7, y: 0, tex: "a-\\delta", cls: "a-pt", anchor: "middle", vAnchor: "top", dy: 5 },
2554:              { type: "text", x: 3.02, y: 0, tex: "a", cls: "a-pt", anchor: "middle", vAnchor: "top", dy: 5 },
2555:              { type: "text", x: 3.32, y: 0, tex: "a+\\delta", cls: "a-pt", anchor: "middle", vAnchor: "top", dy: 5 },
2556:              { type: "text", x: 0, y: Lm, tex: "L-\\varepsilon", cls: "a-pt", anchor: "end", dx: -4 },
2557:              { type: "text", x: 0, y: 8, tex: "L", cls: "a-pt", anchor: "end", dx: -4 },
2558:              { type: "text", x: 0, y: Lp, tex: "L+\\varepsilon", cls: "a-pt", anchor: "end", dx: -4 },
2559:            ],
2560:          }),
2561:        }],
2562:      };
2563:    },
2564:  };
2565:
2566:  function hydrateFigures(root) {
2567:    (root || document).querySelectorAll("[data-fig]").forEach((el) => {
2568:      const def = FIGS[el.dataset.fig];
2569:      if (!def || el.dataset.figDone) return;
2570:      const { layout, panels } = def();
2571:      let html;
2572:      if (layout === "single" && panels.length === 1 && !panels[0].note) {
2573:        html = `<div class="figure-art">${panels[0].svg}</div>`;
2574:      } else {
2575:        const cls = { pair: "figure-art--pair", triple: "figure-art--triple", grid: "figure-art--grid" }[layout] || "";
2576:        html = `<div class="figure-art ${cls}">` +
2577:          panels.map((p) => `<div class="fig-panel">${p.svg}${p.note ? `<div class="fig-note">${p.note}</div>` : ""}</div>`).join("") +
2578:          `</div>`;
2579:      }
2580:      el.insertAdjacentHTML("afterbegin", html);
2581:
2582:      /* Connect per-figure CSS width variables (--fig-1-1 … --fig-1-13)
2583:         defined in :root to this figure's --fig-w so the control panel
2584:         actually takes effect. */
2585:      const figNo = el.querySelector(".fig-no");

exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "Select-String -Path handout\\chapter1-print-standalone.html -Pattern 'function buildPlot|const P|function pow2|xticks|yticks|tick|tex' -Encoding UTF8 | Select-Object -First 80 | ForEach-Object { \""'$($_.LineNumber):$($_.Line)" }' in C:\Users\user\Desktop\Calculus_handout
 succeeded in 304ms:
46:  tex: {
56:    mtextInheritFont: true,
70:<script defer src="https://cdn.jsdelivr.net/npm/mathjax@4/tex-chtml.js"></script>
103:  text-rendering: optimizeLegibility;
109:.skin-hs p, .skin-hs li { text-align: justify; text-justify: inter-word; }
110:.paper .ragged { text-align: left; }
111:.paper p { margin: 0 0 .85em; text-wrap: pretty; }
115:.paper li { margin: .35em 0; text-wrap: pretty; }
125:.paper .qed { display: block; text-align: right; margin: -1.62em 0 0; height: 1.62em; pointer-events: none; }
139:  text-transform: uppercase; color: var(--c-primary); font-weight: 700; margin-bottom: .55em;
148:.paper .figure { margin: 1.7em 0; text-align: center; }
155:  color: var(--ink-soft); margin-top: .7em; text-wrap: pretty;
156:  max-width: none; text-align: left; display: table; margin-inline: auto;
167:.paper .fig-svg text { font-family: var(--ui); font-size: 13px; }
172:.paper .setlab { fill: var(--ink); font-weight: 600; font-size: 14.5px; text-anchor: middle; }
189:  font-size: .62rem; letter-spacing: .07em; text-transform: uppercase; font-weight: 700;
256:  color: var(--ink-soft); margin-top: .55em; text-align: center; text-wrap: pretty;
263:  text-shadow: 0 0 2px var(--paper), 0 0 2px var(--paper), 0 0 1px var(--paper);
275:.paper table.tbl th, .paper table.tbl td { padding: .3em .8em; text-align: center; white-space: nowrap; }
277:.paper table.tbl .rowlab { text-align: right; padding-right: 1em; color: var(--ink-soft); }
282:.paper ul li { margin: .35em 0; text-align: justify; }
286:  font-family: var(--ui); font-size: .72rem; letter-spacing: .18em; text-transform: uppercase;
308:  text-align: center; font: 500 9pt "Inter", sans-serif; color: #82868f;
373:<!-- Chapter 1 opener — overview + learning outcomes. Content verbatim from ch01_foundations.tex. -->
394:<!-- §1.1 Inverse Functions. Content verbatim from ch01_foundations.tex;
420:      \[ f(x_{1}) \neq f(x_{2}) \qquad \text{whenever } x_{1} \neq x_{2}. \]
568:      \[ \begin{aligned} f^{-1}\!\bigl(f(x)\bigr) &= x \quad \text{for every } x \in A, \\ f\!\bigl(f^{-1}(y)\bigr) &= y \quad \text{for every } y \in B. \end{aligned} \]</p>
583:        <text x="72" y="22" class="setlab">A</text>
584:        <text x="288" y="22" class="setlab">B</text>
587:        <text x="52" y="96" class="ptlab">x</text>
588:        <text x="300" y="96" class="ptlab">f(x)</text>
591:        <text x="180" y="46" class="lab-curve">f</text>
592:        <text x="180" y="150" class="lab-ref-b">f⁻¹</text>
668:        \[ x - 5 = \frac{3}{y}, \quad\text{so}\quad x = 5 + \frac{3}{y}. \]
701:<!-- §1.2 Inverse Trigonometric Functions. Content verbatim from ch01_foundations.tex;
732:      \[ \arcsin x = y \quad \Longleftrightarrow \quad \sin y = x \ \text{ and } \ -\tfrac{\pi}{2} \le y \le \tfrac{\pi}{2}. \]
740:      <p>The notation \(\sin^{-1} x\) is also used for \(\arcsin x\). It does <em>not</em> mean the reciprocal \(\bigl(\sin x\bigr)^{-1} = 1 / \sin x\). When reading a source that uses \(\sin^{-1}\), check the context to decide which is meant.</p>
817:      \[ \arccos x = y \quad \Longleftrightarrow \quad \cos y = x \ \text{ and } \ 0 \le y \le \pi. \]
884:      \[ \arctan x = y \quad \Longleftrightarrow \quad \tan y = x \ \text{ and } \ -\tfrac{\pi}{2} < y < \tfrac{\pi}{2}. \]
964:      \[ \arccsc x = y \quad \Longleftrightarrow \quad \csc y = x \ \text{ and } \ y \in \left(0, \tfrac{\pi}{2}\right] \cup \left(\pi, \tfrac{3\pi}{2}\right]. \]</p>
972:      \[ \arcsec x = y \quad \Longleftrightarrow \quad \sec y = x \ \text{ and } \ y \in \left[0, \tfrac{\pi}{2}\right) \cup \left[\pi, \tfrac{3\pi}{2}\right). \]</p>
980:      \[ \arccot x = y \quad \Longleftrightarrow \quad \cot y = x \ \text{ and } \ y \in (0, \pi). \]</p>
989:      <p>For \(\arcsec x\), another common choice of principal range is \(y \in \left[0, \tfrac{\pi}{2}\right) \cup \left(\tfrac{\pi}{2}, \pi\right]\). In this text we use \(y \in \left[0, \tfrac{\pi}{2}\right) \cup \left[\pi, \tfrac{3\pi}{2}\right)\) because it makes the differentiation formulas for the inverse secant simpler. When consulting other sources or software, always check which convention is in use, since different branch choices can lead to different values.</p>
996:      <p>For \(\arccsc x\), another common choice of principal range is \(y \in \left[-\tfrac{\pi}{2}, 0\right) \cup \left(0, \tfrac{\pi}{2}\right]\). In this text we use \(y \in \left(0, \tfrac{\pi}{2}\right] \cup \left(\pi, \tfrac{3\pi}{2}\right]\) so that the chosen branch parallels the one selected for \(\arcsec x\). Once the principal range is fixed consistently, either convention gives a valid inverse function.</p>
1000:  <!-- expansion:example — domains of the remaining inverse trig functions + the branch convention has visible consequences [source: CLP-1 §2.12 #5, recomputed for this text's arccsc principal range] -->
1011:        <p>\(\arcsin\) requires \(|x| \le 1\) while \(\arccsc\) requires \(|x| \ge 1\), so the domain is just the two points \(x = \pm 1\). At \(x = 1\): \(\arcsin 1 = \tfrac{\pi}{2}\) and \(\arccsc 1 = \tfrac{\pi}{2}\) (the angle in \(\left(0, \tfrac{\pi}{2}\right]\) with cosecant \(1\)), so \(f(1) = \pi\). At \(x = -1\): \(\arcsin(-1) = -\tfrac{\pi}{2}\), and under this text's principal range for \(\arccsc\) the angle with cosecant \(-1\) is \(\arccsc(-1) = \tfrac{3\pi}{2}\), so \(f(-1) = -\tfrac{\pi}{2} + \tfrac{3\pi}{2} = \pi\). So \(f\) is the constant \(\pi\) on its two-point domain.</p>
1012:        <p>Under the alternative convention of Remark 1.4 (\(\arccsc(-1) = -\tfrac{\pi}{2}\)) one gets \(f(-1) = -\pi\) instead — a concrete instance of branch conventions changing answers, which is why this text fixes its conventions explicitly.</p>
1021:<!-- §1.3 The Limit of a Function. Content verbatim from ch01_foundations.tex;
1046:  \[ f(x) \to L \qquad \text{as } x \to a, \]
1168:  \[ v(4) = \lim_{t \to 4} \frac{s(4) - s(t)}{4 - t} = \lim_{t \to 4} \bigl[-5(t - 2)\bigr] = -10 \text{ m/s}. \]
1177:<!-- §1.4 One-Sided and Infinite Limits. Content verbatim from ch01_foundations.tex;
1212:      <p>\[ \lim_{x \to a} f(x) = L \quad \Longleftrightarrow \quad \lim_{x \to a^{-}} f(x) = L \ \text{ and } \ \lim_{x \to a^{+}} f(x) = L. \]</p>
1291:        \[ \lim_{x \to 0^{-}} \frac{1}{x}, \qquad \lim_{x \to 0^{+}} \frac{1}{x}, \qquad\text{and}\qquad \lim_{x \to 0} \frac{1}{x}, \]
1346:      \[ \lim_{x \to a^{-}} f(x) = \pm\infty \qquad \text{or} \qquad \lim_{x \to a^{+}} f(x) = \pm\infty. \]</p>
1356:        <li>At each candidate \(x = a\), examine the one-sided limits. When the expression has the form \(\frac{\text{nonzero}}{0}\), determine the sign of the small denominator on each side to decide between \(+\infty\) and \(-\infty\).</li>
1424:<!-- §1.5 Limit Laws and Computational Techniques. Content verbatim from ch01_foundations.tex;
1584:  <!-- expansion:example — combine fractions before taking the limit (Strategy step 2 in action) [source: CLP-1 §1.4 extra, prob_s1.4.tex:751] -->
1754:<!-- §1.6 The Precise Definition of a Limit. Content verbatim from ch01_foundations.tex;
1769:      <p>The drive to replace intuitive arguments with arithmetic precision is known as the <em>arithmetisation of analysis</em>. Bolzano anticipated a more rigorous, inequality-based treatment of continuity and convergence, while Cauchy gave limits and continuity a more systematic analytic form. Weierstrass, lecturing at Berlin from the 1860s onward, refined these ideas into the \(\varepsilon\text{-}\delta\) formulation that is essentially the one presented here.</p>
1807:      \[ |f(x) - L| < \varepsilon \qquad \text{whenever} \qquad 0 < |x - a| < \delta. \]</p>
1855:      \[ |f(x) - L| < \varepsilon \quad \text{whenever} \quad 0 < |x - a| < \delta_{1}, \]
1857:      \[ |f(x) - M| < \varepsilon \quad \text{whenever} \quad 0 < |x - a| < \delta_{2}. \]
1893:        \[ |(4x - 5) - 7| < \varepsilon \quad \text{whenever} \quad 0 < |x - 3| < \delta. \]
1914:        \[ |(x^{2} - 5x + 6) - 2| < \varepsilon \quad \text{whenever} \quad 0 < |x - 1| < \delta. \]
1932:      <p>The value of \(\delta\) is never unique. Once a valid \(\delta\) has been found, any smaller positive value also works, because shrinking the input neighborhood can only tighten the conclusion. The goal of an \(\varepsilon\text{-}\delta\) proof is to exhibit <em>one</em> working \(\delta\), not “the” \(\delta\). In Example 1.40, for instance, \(\delta = \varepsilon/5\) works just as well as \(\delta = \varepsilon/4\).</p>
1977:      \[ f(x) > M \qquad \text{whenever} \qquad 0 < |x - a| < \delta. \]
1981:      \[ f(x) < N \qquad \text{whenever} \qquad 0 < |x - a| < \delta. \]</p>
2020:  function piTex(v) {
2037:  function buildPlot(cfg) {
2055:      if (cfg.xlabel) pushLabel({ px: ax1 + 1, py: ayBase + 4, tex: cfg.xlabel, anchor: "start", vAnchor: "top", cls: "a-ax", size: 13 });
2056:      if (cfg.ylabel) pushLabel({ px: axBase - 5, py: ay1 + 1, tex: cfg.ylabel, anchor: "end", vAnchor: "top", cls: "a-ax", size: 13 });
2057:      (cfg.xticks || []).forEach(function(t) {
2060:        var tex = t.tex != null ? t.tex : (t.label != null ? null : piTex(t.x));
2061:        if (tex != null) pushLabel({ px: px, py: ayBase + 6, tex: tex, anchor: "middle", vAnchor: "top", cls: "a-pt", size: 12 });
2062:        else if (t.label != null) pushLabel({ px: px, py: ayBase + 6, text: t.label, anchor: "middle", vAnchor: "top", cls: "a-pt", size: 12 });
2064:      (cfg.yticks || []).forEach(function(t) {
2067:        var tex = t.tex != null ? t.tex : (t.label != null ? null : piTex(t.y));
2068:        if (tex != null) pushLabel({ px: axBase - 6, py: py, tex: tex, anchor: "end", vAnchor: "middle", cls: "a-pt", size: 12 });
2069:        else if (t.label != null) pushLabel({ px: axBase - 6, py: py, text: t.label, anchor: "end", vAnchor: "middle", cls: "a-pt", size: 12 });
2096:      } else if (it.type === "text") {

exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command '$lines = Get-Content -Encoding UTF8 handout'"\\chapter1-print-standalone.html; for ("'$i=2010; $i -le 2137; $i++) { '"'{0}:{1}' -f "'$i, $lines[$i-1] }' in C:\Users\user\Desktop\Calculus_handout
 succeeded in 287ms:
2010:  then \(f\) is said to be <em>continuous at \(a\)</em>. A systematic study of continuity belongs to a later chapter; we mention the term here because it is expressed directly in terms of limits.</p>
2011:
2012:</article>
2013:</template>
2014:<!-- END-CONTENT-FRAGMENTS -->
2015:<!-- plot.js — inlined -->
2016:<script>
2017:(function () {
2018:  var uid = 0;
2019:  var PI = Math.PI;
2020:  function piTex(v) {
2021:    var map = {};
2022:    map[(-2 * PI).toFixed(4)] = "-2\\pi";
2023:    map[(-PI).toFixed(4)] = "-\\pi";
2024:    map[(-PI / 2).toFixed(4)] = "-\\tfrac{\\pi}{2}";
2025:    map[(PI / 2).toFixed(4)] = "\\tfrac{\\pi}{2}";
2026:    map[PI.toFixed(4)] = "\\pi";
2027:    map[(2 * PI).toFixed(4)] = "2\\pi";
2028:    map[(0).toFixed(4)] = "0";
2029:    return map[v.toFixed(4)];
2030:  }
2031:  function esc(s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;"); }
2032:  function anchorTransform(anchor, vAnchor) {
2033:    var tx = anchor === "start" ? "0" : anchor === "end" ? "-100%" : "-50%";
2034:    var ty = vAnchor === "top" ? "0" : vAnchor === "bottom" ? "-100%" : "-50%";
2035:    return "translate(" + tx + "," + ty + ")";
2036:  }
2037:  function buildPlot(cfg) {
2038:    var w = cfg.w, h = cfg.h;
2039:    var pad = Object.assign({ t: 16, r: 18, b: 20, l: 22 }, cfg.pad || {});
2040:    var xmin = cfg.xmin, xmax = cfg.xmax, ymin = cfg.ymin, ymax = cfg.ymax;
2041:    var iw = w - pad.l - pad.r, ih = h - pad.t - pad.b;
2042:    var SX = function(x) { return pad.l + ((x - xmin) / (xmax - xmin)) * iw; };
2043:    var SY = function(y) { return h - pad.b - ((y - ymin) / (ymax - ymin)) * ih; };
2044:    var id = "pl" + (++uid);
2045:    var parts = [], labels = [];
2046:    function pushLabel(o) { labels.push(o); }
2047:    parts.push('<svg viewBox="0 0 ' + w + ' ' + h + '" style="width:' + w + 'px" class="fig-svg" role="img" aria-label="' + esc(cfg.aria || "graph") + '" preserveAspectRatio="xMidYMid meet">');
2048:    parts.push('<defs><marker id="' + id + 'a" markerWidth="8" markerHeight="8" refX="5.4" refY="2.8" orient="auto" markerUnits="userSpaceOnUse"><path d="M0,0 L5.4,2.8 L0,5.6" fill="none" stroke="var(--c-axis)" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>');
2049:    if (cfg.axes !== false) {
2050:      var x0 = Math.min(Math.max(0, xmin), xmax), y0 = Math.min(Math.max(0, ymin), ymax);
2051:      var ax0 = SX(xmin), ax1 = SX(xmax), ayBase = SY(y0);
2052:      parts.push('<path d="M' + ax0.toFixed(1) + ',' + ayBase.toFixed(1) + ' H' + (ax1 - 1).toFixed(1) + '" class="axis" marker-end="url(#' + id + 'a)"/>');
2053:      var ay0 = SY(ymin), ay1 = SY(ymax), axBase = SX(x0);
2054:      parts.push('<path d="M' + axBase.toFixed(1) + ',' + ay0.toFixed(1) + ' V' + (ay1 + 1).toFixed(1) + '" class="axis" marker-end="url(#' + id + 'a)"/>');
2055:      if (cfg.xlabel) pushLabel({ px: ax1 + 1, py: ayBase + 4, tex: cfg.xlabel, anchor: "start", vAnchor: "top", cls: "a-ax", size: 13 });
2056:      if (cfg.ylabel) pushLabel({ px: axBase - 5, py: ay1 + 1, tex: cfg.ylabel, anchor: "end", vAnchor: "top", cls: "a-ax", size: 13 });
2057:      (cfg.xticks || []).forEach(function(t) {
2058:        var px = SX(t.x);
2059:        parts.push('<line x1="' + px.toFixed(1) + '" y1="' + (ayBase - 3).toFixed(1) + '" x2="' + px.toFixed(1) + '" y2="' + (ayBase + 3).toFixed(1) + '" class="axis"/>');
2060:        var tex = t.tex != null ? t.tex : (t.label != null ? null : piTex(t.x));
2061:        if (tex != null) pushLabel({ px: px, py: ayBase + 6, tex: tex, anchor: "middle", vAnchor: "top", cls: "a-pt", size: 12 });
2062:        else if (t.label != null) pushLabel({ px: px, py: ayBase + 6, text: t.label, anchor: "middle", vAnchor: "top", cls: "a-pt", size: 12 });
2063:      });
2064:      (cfg.yticks || []).forEach(function(t) {
2065:        var py = SY(t.y);
2066:        parts.push('<line x1="' + (axBase - 3).toFixed(1) + '" y1="' + py.toFixed(1) + '" x2="' + (axBase + 3).toFixed(1) + '" y2="' + py.toFixed(1) + '" class="axis"/>');
2067:        var tex = t.tex != null ? t.tex : (t.label != null ? null : piTex(t.y));
2068:        if (tex != null) pushLabel({ px: axBase - 6, py: py, tex: tex, anchor: "end", vAnchor: "middle", cls: "a-pt", size: 12 });
2069:        else if (t.label != null) pushLabel({ px: axBase - 6, py: py, text: t.label, anchor: "end", vAnchor: "middle", cls: "a-pt", size: 12 });
2070:      });
2071:    }
2072:    (cfg.items || []).forEach(function(it) {
2073:      if (it.type === "curve") {
2074:        var cls = it.cls || "curve", n = it.samples || 240, a = it.domain[0], b = it.domain[1];
2075:        var d = "", pen = false;
2076:        for (var i = 0; i <= n; i++) {
2077:          var x = a + (b - a) * (i / n), y = it.fn(x);
2078:          if (!isFinite(y) || y < ymin - (ymax - ymin) * 0.04 || y > ymax + (ymax - ymin) * 0.04) { pen = false; continue; }
2079:          var px = SX(x).toFixed(2), py = SY(y).toFixed(2);
2080:          d += (pen ? "L" : "M") + px + "," + py + " "; pen = true;
2081:        }
2082:        if (d) parts.push('<path d="' + d.trim() + '" class="' + cls + '"/>');
2083:      } else if (it.type === "vline") {
2084:        parts.push('<line x1="' + SX(it.x).toFixed(1) + '" y1="' + SY(ymin).toFixed(1) + '" x2="' + SX(it.x).toFixed(1) + '" y2="' + SY(ymax).toFixed(1) + '" class="' + (it.cls || "refline") + '"/>');
2085:      } else if (it.type === "hline") {
2086:        var ha = it.from != null ? it.from : xmin, hb = it.to != null ? it.to : xmax;
2087:        parts.push('<line x1="' + SX(ha).toFixed(1) + '" y1="' + SY(it.y).toFixed(1) + '" x2="' + SX(hb).toFixed(1) + '" y2="' + SY(it.y).toFixed(1) + '" class="' + (it.cls || "refline") + '"/>');
2088:      } else if (it.type === "seg") {
2089:        parts.push('<line x1="' + SX(it.x1).toFixed(1) + '" y1="' + SY(it.y1).toFixed(1) + '" x2="' + SX(it.x2).toFixed(1) + '" y2="' + SY(it.y2).toFixed(1) + '" class="' + (it.cls || "curve") + '"/>');
2090:      } else if (it.type === "dot") {
2091:        var r = it.r || 3.0;
2092:        if (it.hollow) parts.push('<circle cx="' + SX(it.x).toFixed(1) + '" cy="' + SY(it.y).toFixed(1) + '" r="' + r + '" fill="var(--paper)" stroke="var(--ink)" stroke-width="1.5"/>');
2093:        else parts.push('<circle cx="' + SX(it.x).toFixed(1) + '" cy="' + SY(it.y).toFixed(1) + '" r="' + r + '" class="dot"/>');
2094:      } else if (it.type === "arrow") {
2095:        parts.push('<line x1="' + SX(it.x1).toFixed(1) + '" y1="' + SY(it.y1).toFixed(1) + '" x2="' + SX(it.x2).toFixed(1) + '" y2="' + SY(it.y2).toFixed(1) + '" class="axis" marker-end="url(#' + id + 'a)"/>');
2096:      } else if (it.type === "text") {
2097:        pushLabel({ px: SX(it.x), py: SY(it.y), tex: it.tex, text: it.tex == null ? it.text : null, anchor: it.anchor || "middle", vAnchor: it.vAnchor || "middle", dx: it.dx || 0, dy: it.dy || 0, cls: it.cls || "a-pt", size: it.size });
2098:      }
2099:    });
2100:    if (labels.length) {
2101:      var M = 52;
2102:      var spans = labels.map(function(L) {
2103:        var left = (L.px + (L.dx || 0) + M).toFixed(1);
2104:        var top = (L.py + (L.dy || 0) + M).toFixed(1);
2105:        var tf = anchorTransform(L.anchor, L.vAnchor);
2106:        var fs = L.size ? "font-size:" + L.size + "px;" : "";
2107:        var body = L.tex != null ? "\\(" + L.tex + "\\)" : esc(L.text == null ? "" : L.text);
2108:        return '<span class="fig-lbl ' + (L.cls || "") + '" style="left:' + left + 'px;top:' + top + 'px;transform:' + tf + ';' + fs + '">' + body + '</span>';
2109:      }).join("");
2110:      parts.push('<foreignObject x="' + (-M) + '" y="' + (-M) + '" width="' + (w + 2 * M) + '" height="' + (h + 2 * M) + '" class="fig-fo" requiredExtensions="http://www.w3.org/1999/xhtml"><div xmlns="http://www.w3.org/1999/xhtml" class="fig-lyr">' + spans + '</div></foreignObject>');
2111:    }
2112:    parts.push('</svg>');
2113:    return parts.join("");
2114:  }
2115:  window.buildPlot = buildPlot;
2116:  window.PIVAL = PI;
2117:})();
2118:</script>
2119:
2120:<!-- ============================================================
2121:     figures.js — inlined (Chapter 1 figure registry)
2122:     ============================================================ -->
2123:<script>
2124:/* ============================================================
2125:   figures.js — Chapter 1 figure registry.
2126:   Each entry returns { layout, panels:[{svg, note}] } (note may
2127:   carry \( \) math, rendered by the page's MathJax pass afterward).
2128:   In-figure labels also carry TeX via { type:"text", tex:"…" } and
2129:   are typeset by the same MathJax pass — so every glyph in the graphs
2130:   matches the body equations (Computer Modern).
2131:   hydrateFigures(root) fills every <figure data-fig="id"> before
2132:   its <figcaption>.
2133:   ============================================================ */
2134:(function () {
2135:  const P = () => window.PIVAL;
2136:  const pow2 = (x) => Math.pow(2, x);
2137:

codex
初步看起來大多數圖的座標與正文一致；我會特別放大幾張承載讀值的圖（如 floor、squeeze、ε-δ）確認 tick 與 label 沒有在列印 PNG 裡消失或互撞。
codex
在 p32 放大後，我注意到 `floor-function` 的正向整數 tick 標籤在 PNG 裡不像程式碼預期那樣明顯呈現；我會把它按 D4 的「是否承載讀值」標準審慎分級，不把純輔助刻度自動升成 blocking。
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command '$lines = Get-Content -Encoding UTF8 handout'"\\fragments\\ch01\\sec-1-5.html; for ("'$i=230; $i -le 270; $i++) { if ($i -le $lines.Length) { '"'{0}:{1}' -f "'$i, $lines[$i-1] } }' in C:\Users\user\Desktop\Calculus_handout
 succeeded in 422ms:
230:      \[ g(x) \le f(x) \le h(x) \]
231:      for all \(x\) near \(a\), except possibly at \(x = a\). If
232:      \[ \lim_{x \to a} g(x) = L, \qquad \lim_{x \to a} h(x) = L, \]
233:      then \(\lim_{x \to a} f(x) = L\).</p>
234:    </div>
235:  </section>
236:
237:  <figure class="figure" data-fig="squeeze-theorem">
238:    <figcaption><span class="fig-no">Figure 1.19</span> The squeeze theorem: \(f\) is trapped between \(g\) and \(h\), which share the same limit \(L\).</figcaption>
239:  </figure>
240:
241:  <div class="workedexample">
242:    <section class="env env-example">
243:      <p class="env-head"><span class="env-kicker">Example</span><span class="env-num">1.34</span></p>
244:      <div class="env-body">
245:        <p>Evaluate
246:        \[ \lim_{x \to 0} x^{2} \sin\!\left(\frac{1}{x}\right). \]</p>
247:      </div>
248:    </section>
249:    <section class="env env-solution">
250:      <p class="env-head"><span class="env-kicker">Solution</span></p>
251:      <div class="env-body">
252:        <p>We cannot apply the product law because \(\lim_{x \to 0} \sin(1/x)\) does not exist. Instead, we use the bound
253:        \[ -1 \le \sin\!\left(\frac{1}{x}\right) \le 1 \]
254:        valid for all \(x \neq 0\). Multiplying by \(x^{2} \ge 0\),
255:        \[ -x^{2} \le x^{2} \sin\!\left(\frac{1}{x}\right) \le x^{2}. \]
256:        Since \(\lim_{x \to 0}(-x^{2}) = 0 = \lim_{x \to 0} x^{2}\), the squeeze theorem yields
257:        \[ \lim_{x \to 0} x^{2} \sin\!\left(\frac{1}{x}\right) = 0. \]</p>
258:        <figure class="figure" data-fig="squeeze-x2sin">
259:          <figcaption><span class="fig-no">Figure 1.20</span> The graph of \(y = x^{2}\sin(1/x)\) squeezed between \(y = -x^{2}\) and \(y = x^{2}\).</figcaption>
260:        </figure>
261:      </div>
262:    </section>
263:  </div>
264:
265:  <div class="workedexample">
266:    <section class="env env-example">
267:      <p class="env-head"><span class="env-kicker">Example</span><span class="env-num">1.35</span></p>
268:      <div class="env-body">
269:        <p>Evaluate
270:        \[ \lim_{x \to 0} x \cos\!\left(\frac{1}{x}\right). \]</p>

codex
我確認 p34 的 `squeeze-x2sin` 有一個原始碼加入的實心點在 \(x=0\)，而該函數在 \(0\) 未定義；這會列為實質數學／語境問題。其餘疑點會繼續按圖逐一核對，不因樣式偏好擴大。
codex
我已完成主要頁面的視覺放大檢查；目前除 `squeeze-x2sin` 的實心原點與 `floor-function` 的輔助 tick 可讀性外，尚未看到會擋稿的標籤碰撞、裁切或視窗問題。最後會再跑一次座標一致性清單。
codex
審查完成，未修改檔案。依據 `FIGURE-AUDIT-RUBRIC.md`、`chapter1-print-standalone.html` 的 `FIGS` 座標，以及相關 `sec-1-*.html` 語境逐圖核對。

- Fig 1.1 `hlt`｜VERDICT: 0 blocking, 0 advisory｜D1–D8 乾淨。
- Fig 1.3 `restrict-x2`｜VERDICT: 0 blocking, 0 advisory｜D1–D8 乾淨。
- Fig 1.4 `sine-not-1to1`｜VERDICT: 0 blocking, 0 advisory｜D1–D8 乾淨。
- Fig 1.5 `restricted-sine`｜VERDICT: 0 blocking, 0 advisory｜D1–D8 乾淨。
- Fig 1.6 `arcsin-triangle`｜VERDICT: 0 blocking, 0 advisory｜D1–D8 乾淨；三角形比例示意不列 finding。
- Fig 1.7 `restricted-cosine`｜VERDICT: 0 blocking, 0 advisory｜D1–D8 乾淨。
- Fig 1.8 `restricted-tangent`｜VERDICT: 0 blocking, 0 advisory｜D1–D8 乾淨。
- Fig 1.9 `arctan10-triangle`｜VERDICT: 0 blocking, 0 advisory｜D1–D8 乾淨；三角形比例示意不列 finding。
- Fig 1.10 `arctan-general-triangle`｜VERDICT: 0 blocking, 0 advisory｜D1–D8 乾淨；三角形比例示意不列 finding。
- Fig 1.11 `limit-same-near-a`｜VERDICT: 0 blocking, 0 advisory｜D1–D8 乾淨。
- Fig 1.12 `read-limit-graph`｜VERDICT: 0 blocking, 0 advisory｜D1–D8 乾淨。
- Fig 1.13 `one-sided-limits`｜VERDICT: 0 blocking, 0 advisory｜D1–D8 乾淨。
- Fig 1.14 `piecewise-jump`｜VERDICT: 0 blocking, 0 advisory｜D1–D8 乾淨。
- Fig 1.15 `one-sided-infinite`｜VERDICT: 0 blocking, 0 advisory｜D1–D8 乾淨。
- Fig 1.16 `vertical-asymptote`｜VERDICT: 0 blocking, 0 advisory｜D1–D8 乾淨。
- Fig 1.17 `ln-asymptote`｜VERDICT: 0 blocking, 0 advisory｜D1–D8 乾淨。

- Fig 1.18 `floor-function`｜VERDICT: 0 blocking, 1 advisory  
  `floor-function`｜Figure 1.18｜D4｜Advisory｜PNG p32 中正向整數 tick marks 可見，但 `1,2,3,4` 標籤不易辨讀；`FIGS` 在 `chapter1-print-standalone.html:2481–2482` 明確設定 x/y 正整數 tick labels｜此圖輔助說明跳躍位置，非唯一讀值來源，故不升 blocking｜建議放大或重定位整數 tick labels，至少讓 `x=3` 清楚可讀。  
  D1–D3、D5–D8 乾淨。

- Fig 1.19 `squeeze-theorem`｜VERDICT: 0 blocking, 0 advisory｜D1–D8 乾淨。

- Fig 1.20 `squeeze-x2sin`｜VERDICT: 1 blocking, 0 advisory  
  `squeeze-x2sin`｜Figure 1.20｜D6｜Blocking｜PNG p34 在原點畫出實心點；`FIGS` 於 `chapter1-print-standalone.html:2522–2524` 將曲線分成 `[-1.1,-0.01]`、`[0.01,1.1]` 後又加入 `{ type: "dot", x: 0, y: 0 }`；fragment `sec-1-5.html:252–255` 說明 bound valid for all `x \neq 0`，caption 又稱此為 \(y=x^{2}\sin(1/x)\) 的 graph｜該函數在 \(x=0\) 未定義，實心點按圖例慣例會表示函數值存在且為 0，與數學對象矛盾｜建議移除該實心點；若要標示極限點，改空心點並在語境中避免暗示 \(f(0)\) 已定義。  
  D1–D4、D7–D8 乾淨；D5/D6 受同一原點實心點問題影響。

- Fig 1.21 `precise-limit`｜VERDICT: 0 blocking, 0 advisory｜D1–D8 乾淨；空心點／實心點用法符合本圖語境，不列 finding。

全章彙總：Blocking 1，Advisory 1。Figure gate 2 未通過，因 blocking 未歸零。
tokens used
465,316
審查完成，未修改檔案。依據 `FIGURE-AUDIT-RUBRIC.md`、`chapter1-print-standalone.html` 的 `FIGS` 座標，以及相關 `sec-1-*.html` 語境逐圖核對。

- Fig 1.1 `hlt`｜VERDICT: 0 blocking, 0 advisory｜D1–D8 乾淨。
- Fig 1.3 `restrict-x2`｜VERDICT: 0 blocking, 0 advisory｜D1–D8 乾淨。
- Fig 1.4 `sine-not-1to1`｜VERDICT: 0 blocking, 0 advisory｜D1–D8 乾淨。
- Fig 1.5 `restricted-sine`｜VERDICT: 0 blocking, 0 advisory｜D1–D8 乾淨。
- Fig 1.6 `arcsin-triangle`｜VERDICT: 0 blocking, 0 advisory｜D1–D8 乾淨；三角形比例示意不列 finding。
- Fig 1.7 `restricted-cosine`｜VERDICT: 0 blocking, 0 advisory｜D1–D8 乾淨。
- Fig 1.8 `restricted-tangent`｜VERDICT: 0 blocking, 0 advisory｜D1–D8 乾淨。
- Fig 1.9 `arctan10-triangle`｜VERDICT: 0 blocking, 0 advisory｜D1–D8 乾淨；三角形比例示意不列 finding。
- Fig 1.10 `arctan-general-triangle`｜VERDICT: 0 blocking, 0 advisory｜D1–D8 乾淨；三角形比例示意不列 finding。
- Fig 1.11 `limit-same-near-a`｜VERDICT: 0 blocking, 0 advisory｜D1–D8 乾淨。
- Fig 1.12 `read-limit-graph`｜VERDICT: 0 blocking, 0 advisory｜D1–D8 乾淨。
- Fig 1.13 `one-sided-limits`｜VERDICT: 0 blocking, 0 advisory｜D1–D8 乾淨。
- Fig 1.14 `piecewise-jump`｜VERDICT: 0 blocking, 0 advisory｜D1–D8 乾淨。
- Fig 1.15 `one-sided-infinite`｜VERDICT: 0 blocking, 0 advisory｜D1–D8 乾淨。
- Fig 1.16 `vertical-asymptote`｜VERDICT: 0 blocking, 0 advisory｜D1–D8 乾淨。
- Fig 1.17 `ln-asymptote`｜VERDICT: 0 blocking, 0 advisory｜D1–D8 乾淨。

- Fig 1.18 `floor-function`｜VERDICT: 0 blocking, 1 advisory  
  `floor-function`｜Figure 1.18｜D4｜Advisory｜PNG p32 中正向整數 tick marks 可見，但 `1,2,3,4` 標籤不易辨讀；`FIGS` 在 `chapter1-print-standalone.html:2481–2482` 明確設定 x/y 正整數 tick labels｜此圖輔助說明跳躍位置，非唯一讀值來源，故不升 blocking｜建議放大或重定位整數 tick labels，至少讓 `x=3` 清楚可讀。  
  D1–D3、D5–D8 乾淨。

- Fig 1.19 `squeeze-theorem`｜VERDICT: 0 blocking, 0 advisory｜D1–D8 乾淨。

- Fig 1.20 `squeeze-x2sin`｜VERDICT: 1 blocking, 0 advisory  
  `squeeze-x2sin`｜Figure 1.20｜D6｜Blocking｜PNG p34 在原點畫出實心點；`FIGS` 於 `chapter1-print-standalone.html:2522–2524` 將曲線分成 `[-1.1,-0.01]`、`[0.01,1.1]` 後又加入 `{ type: "dot", x: 0, y: 0 }`；fragment `sec-1-5.html:252–255` 說明 bound valid for all `x \neq 0`，caption 又稱此為 \(y=x^{2}\sin(1/x)\) 的 graph｜該函數在 \(x=0\) 未定義，實心點按圖例慣例會表示函數值存在且為 0，與數學對象矛盾｜建議移除該實心點；若要標示極限點，改空心點並在語境中避免暗示 \(f(0)\) 已定義。  
  D1–D4、D7–D8 乾淨；D5/D6 受同一原點實心點問題影響。

- Fig 1.21 `precise-limit`｜VERDICT: 0 blocking, 0 advisory｜D1–D8 乾淨；空心點／實心點用法符合本圖語境，不列 finding。

全章彙總：Blocking 1，Advisory 1。Figure gate 2 未通過，因 blocking 未歸零。
