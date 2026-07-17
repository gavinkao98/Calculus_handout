# 語意/聲音 critic 固定錨組（svc-exemplars）

> **用途：** 本檔是 [`PLAN-deai-semantic-critic.md`](../../../../authoring/_archive/deai/PLAN-deai-semantic-critic.md) §3 的「範本錨」，固定 **2 正 ＋ 1 負**。
> 兩用途：①掛在 prose-audit **Dimension C（S/A/V）** gate 的 prompt 末尾，當 few-shot 錨——critic 對著**正面 bar** 判稿、把**負面**當「該被 flag 長這樣」的示範；②2 段正例同時當 `CONTENT_SPEC.md` §3 的真人 **voice corpus** 替換（Task 6 消費，撤掉 Ch1 循環標靶）。
>
> **核心信念（spec §0）：** 中性 **≠** AI；**中性＋空**才是 AI。正例示範「中性但言之有物」，負例示範「中性但空」。
>
> **判準對照（spec §2）：** **S** Substance（S1 加新洞見／S2 針對這個物件／S3 刪了會損失）、**A** Altitude（A1 不嘮叨顯而易見／A2 不揮手帶過真正難的一步，self-relative）、**V** Voice（V1 §3 那點暖在不在——不灌人格）。
>
> **授權（spec §7 紅線）：** 兩段正例逐字取自 **OpenStax Calculus Volume 1**（CC BY-NC-SA 4.0），逐段標出處；負例為本案自撰示範段（非引用）。只用 BY／BY-NC／BY-NC-SA 家族。

---

## 正例 1 — Substance／Altitude／Voice 三維皆高（limit）

- **〔來源/授權〕** `[source: OpenStax Calculus Vol.1, CC BY-NC-SA 4.0, §2.2 "The Limit of a Function"]`
- **〔正/負〕** 正例。**這把尺主要的「言之有物」標靶**——三維 S/A/V 同時達標的代表段。
- **〔為何〕**
  - **S（substance）**：每句都掙得位置。不是把表格/圖翻成英文，而是**診斷它們的具體缺陷**（"rely too much on guesswork"），再用這個 gap 推出下一節的代數方法。payload＝「被命名的局限＋向前動機」，刪掉讀者真的少一塊（S1/S2/S3 全過）。
  - **A（altitude）**：對自學者高度剛好——不重講怎麼讀表（不犯 A1），也不揮手帶過為何需要更難的代數路徑（不犯 A2），誠實說直覺法不夠用並指向補救者。
  - **V（voice）**：§3 暖度到位但不話嘮——motivation-before-formalism、主代名詞 "we"、真正的 connective（"However"），對讀者誠實而非乾巴巴斷言。不灌人格、不加笑話，純粹「該暖處有暖」。
- **〔自足性〕** 全自足：無 figure/example/table 跨指涉，零 inline math。"the next section"／"two special limits" 為前指性**動機手勢**，非 load-bearing 跨指涉。字數 84（落在 80–150）。

> Looking at a table of functional values or looking at the graph of a function provides us with useful insight into the value of the limit of a function at a given point. However, these techniques rely too much on guesswork. We eventually need to develop alternative methods of evaluating limits. These new methods are more algebraic in nature and we explore them in the next section; however, at this point we introduce two special limits that are foundational to the techniques to come.

---

## 正例 2 — concrete-to-abstract 的 Substance／Voice 標靶（derivative）

- **〔來源/授權〕** `[source: OpenStax Calculus Vol.1, CC BY-NC-SA 4.0, §3.1 "Defining the Derivative"]`
- **〔正/負〕** 正例。**§3 招牌「具體→抽象、最後才命名」的標靶**（local linearity）。
- **〔為何〕**
  - **S（substance）**：object-specific 且層層推進——從可觸摸的物件（$\sqrt{x}$、點 $(1,1)$、收緊的區間）建起 local-linearity，每句推進 zoom 論證（圖與切線重合 → 切線值近似函數值 → 局部線性），不是重述同一句（S1）。
  - **V（voice）**：不機械陳述局部線性，而讓讀者先「看見」再命名；"In fact, … locally linear" 把直覺當成小小揭示而非平板定義——正是 §3 motivation-before-formalism 的暖。
  - **A（altitude）**：停在真正非顯然的一步（為何放大會讓曲線看起來直）而不糾纏瑣碎步驟。
- **〔自足性／caveat〕** 以 "In Figure 3.5 we show" 開頭、依賴該圖；但散文本身（收緊區間使 $\sqrt{x}$ 與其 $(1,1)$ 切線視覺重合，即局部線性）**完整承載核心意思，斷掉圖仍可讀懂**，依 spec 自足性約束可接受。inline math 輕且乾淨（$f(x)=\sqrt{x}$、$(1,1)$、$x=1$）。字數 81（落在 80–150）。

> In Figure 3.5 we show the graph of f(x)=√x and its tangent line at (1,1) in a series of tighter intervals about x=1. As the intervals become narrower, the graph of the function and its tangent line appear to coincide, making the values on the tangent line a good approximation to the values of the function for choices of x close to 1. In fact, the graph of f(x) itself appears to be locally linear in the immediate vicinity of x=1.

---

## 負例 — AI-default 空泛（該被 flag 長這樣）

- **〔來源/授權〕** 本案自撰示範段（非引用；刻意堆 tell 又空，當對比錨）。
- **〔正/負〕** 負例。
- **〔踩了哪些測試〕**
  - **S1（無新洞見）**：每句相對前句不加任何資訊、只堆形容詞（"fundamental"、"powerful"、"crucial"、"essential"）。
  - **S2（通用填充）**：整段貼到任何概念（積分、極限、向量）都成立，毫無對「導數**這個**物件」的針對性。
  - **A2（揮手帶過真正難的一步）**：承諾要 explore "how it works and why"，卻從不碰真正難的一步（差商、極限過程），全是 promise、無 delivery。
  - **V1（假暖、非該暖處有暖）**：'unlock a deeper appreciation'、'captures the essence of change itself' 是**灌人格／假親暱與空泛抒情**，不是 §3 要的那點暖——正是「中性＋空＝AI」的反面教材。

> The derivative is a fundamental and powerful concept that plays a crucial role in calculus. It is important to note that the derivative measures the rate of change of a function. In this section, we will explore how the derivative works and why it is so essential. By understanding the derivative, we unlock a deeper appreciation of how functions behave. Let us now delve into the details — at its core, the derivative captures the essence of change itself.

---

## 維護註記

- **錨總量** 約 250 字（2 正＝84＋81，1 負＝83），落在 spec §3「約 400 字」內偏精簡側，故意從嚴、寧少報。
- **盲測防洩漏（Task 4）：** 本錨組的兩段正例**不得**進盲測 benchmark 的真人負例池；benchmark 另取 OpenStax 其他節＋CLP-1（`.tmp/deai-corpus/clp-limit.md`），與此處不重複。
- **§3 共用（Task 6）：** 上述 2 段正例為 `CONTENT_SPEC.md` §3 真人 voice corpus 的指定替換素材。§3 既有 Markdown 慣例會把 verbatim 的純文字數學（如 `f(x)=√x`）正規化為 `$f(x)=\sqrt{x}$`；本錨檔保留 verbatim 原樣。
- **topic-matched 範本** 只在 Task 4／Task 5 驗證顯示某些難主題系統性判錯高度時才資料驅動局部補（spec §3），非一開始逐節換。
