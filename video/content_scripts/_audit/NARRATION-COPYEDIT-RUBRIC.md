# 旁白散文潤稿 — 維度與分工（NARRATION-COPYEDIT-RUBRIC）

> 本檔是「旁白散文潤稿（copyedit pass）」的契約與**單一真相來源**。潤稿的讀者——**gate 1（Claude subagent，免費）** 與 **gate 2（Codex 獨立第二讀者，計費）**——都讀本檔判斷；維度／護欄**只在這裡改一次**，prompt 只「引用」不「複述」。
>
> 方法論權威見 [`../../CONTENT_METHODOLOGY.md`](../../CONTENT_METHODOLOGY.md) §4（旁白為「說」而寫）、§7「散文潤稿 pass（鎖稿前；與忠實性 NFA 的分工）」。本檔只定維度／護欄／回報，**不重述**方法論。

## 審查對象與邊界（與 NFA 的分工）

潤稿是 **Stage-1（DRAFT）側**對 narration **source** 的散文品質 pass，在 source **鎖稿並 derive 成 HTML／口語版之前**跑。**這是 copyedit（*怎麼說*），不是內容審查（*教什麼*），也不是忠實稽核。**

- **可以**提議改 source 措辭（收緊、去重、順耳）。
- **時機關鍵：** 冗餘／贅字一旦進了認可 source 就改不動了——鎖稿後的忠實性 NFA（[`NARRATION-FAITHFULNESS-RUBRIC.md`](NARRATION-FAITHFULNESS-RUBRIC.md)）明令不 re-litigate 已認可內容、且 D2 要求口語版逐字照 source，去重會被當成 D2 違規。**所以冗餘只能在這個鎖稿前的 pass 攔下。** 分工：潤稿管 *how*（鎖稿前、可改 source），NFA 管 *faithful＋數學正確*（鎖稿後、不改 source）。
- **不要**拿本 pass 去重開已鎖稿、已認可的 source；那正是 NFA 禁止的。（已鎖稿 source 若仍須動，由使用者明確授權為一次 Stage-1 源稿編修，不走本 pass；若改到已合成 beat 要重 derive ＋重 TTS，計費。）

## 唯一硬護欄（先讀這條）

潤稿**精確保留語意。** 可收緊措辭、去重、順耳——**不可**改教學內容、增刪步驟、更動任何數學陳述／數值／區間、或改教學順序。每個提議改寫都必須與原文語義完全相同、只是說得更好。若一個收緊會碰到數學或教學法，**出界——留著別動。**

## 維度（C1–C5；全 Advisory）

**C1 — 局部冗餘。** 一個詞／概念在 ~1–2 句內無新意地重述（「say it, then say it again」老毛病）。典型：命名一個詞後緊接在下一子句又用它，而一次提及就承載兩者（如 *"…has a name: one-to-one. A function $f$ is one-to-one if…"* → 折成只說一次）。只 flag 鄰近碰撞，**絕不** flag 跨單元的 topic 反覆。

**C2 — 贅字。** filler／疊字（*the fact that*、*in order to*、*it is the case that*、*actually*、*basically*、多餘的 *both … as well*…），刪了零語意損失。引用它、給收緊後的措辭。

**C3 — 讀順度（read-aloud fluency）。** 念出來會卡：子句堆疊、garden-path 開頭、動詞前鋪陳過長、繞口的相鄰。旁白為耳朵寫——偏好較短的主句。

**C4 — 句長／可聽度。** 一句太長、聽者一口氣的意義扛不住（方法論 §4：口語、一單元一概念）。給切點。

**C5 — 跨單元 echo。** 一句 setup／framing 在後面單元近乎逐字重複、而聽者已有（方法論 §"repeat-pattern：第二次省掉 setup"）。flag 後出現的那次以收緊。

## 收斂線

潤稿**結構上沒有 blocking 級**——所有 finding 都是 advisory（Tighten／Optional）。因此**blocking 恆 0、收斂在 blocking 軸上自動成立**；潤稿不靠收斂線把關，而是**逐筆交使用者裁決**收哪些。兩道讀者的角色：gate 1（Claude，免費）先抓；接近定稿時 gate 2（Codex，計費、需同意）當「另一個真實讀者」補盲點，兩份各自獨立、不合併。

## 不算 finding（別誤砍）

- **topic-term 反覆** — 該節就是在講那個詞（如 "one-to-one"、"limit"、"continuous"），跨單元自然反覆，**絕不** flag。
- **刻意教學法** — 為強調的 echo、recap 重述、「同型第二例跳過 setup」（方法論 §repeat-pattern），是設計、保留。**Caveat：** name-then-define 在「名稱與定義跨句／跨 reveal」時是好教學法；但**同一詞在緊鄰子句連說兩次**（"…has a name: one-to-one. A function $f$ is one-to-one if…"）就是 C1 tic，不是受保護教學法，折成只說一次。
- 語義等價的用詞差異。

## 回報規格

四級，只報 tier 1–2（① careful editor 會修的真冗餘／贅字／讀順卡頓 ② 值得提的收緊），tier 3（taste／voice drift）至多一行，tier 4 略。**不 over-report；乾淨章節是有效結果。**

**輸出格式（最終訊息；不寫任何檔案）：**

- 首行：`VERDICT: <N> tighten, <M> optional`
- 逐條：`- [Tighten|Optional] [C#] unit-id — issue（引用原文）→ proposed: "<收緊後措辭>"`
- 每個乾淨維度一行（如 `C2 wordiness: clean`）。
- 末行提醒：對**已合成** beat 採用某改寫＝要重 derive ＋ 重 TTS（**計費**）——故由使用者逐筆決定收哪個。

**交付給使用者裁決時**：依 [`../../../CLAUDE.md`](../../../CLAUDE.md) 交付規則產 standalone HTML 審核稿（MathJax/KaTeX CDN、雙擊即開）、finding 標穩定編號。純版控紀錄不在此限。
