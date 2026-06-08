# Direction Brief — §3.3 Applications of the Chain Rule

> ② 方向提案（RULE.md §2 九欄）。輸入：[`seed_ch03_s3.md`](seed_ch03_s3.md)（手稿 pp.12–14 應用①②③＋pp.21–22 Homework，**①-verify ✅ 2026-06-08**）
> ＋ [`PLAN-ch03.md`](PLAN-ch03.md) 章層決策 D8/D9/D10＋§5 編號 ledger ＋ ROADMAP「Chapter 3」條目。
> 設計經 **3-lens design panel**（pedagogy／faithfulness+numbering／ROADMAP-alignment）壓測、本檔為綜合稿。
> **✅ ③ 方向閘已核可（2026-06-08）**：補 arctan′（Ex 3.12）、omit Figure 3.3、D9 三項全收（arccos′ Ex 3.11／2ˣ′ Ex 3.8／(x ln x−x)′ Ex 3.9）、results framing＝worked example。本檔為 ④/⑤ 契約。
> §3.3 是 ch03 **末節**：另負責**章末 chapter summary**（tie §3.1–§3.3＋forward Ch4）。§3.1/§3.2 已過六階，為風格／密度／編號基準。

---

## 手稿盤點（照原順序）
- **應用①**（p.12）：`d/dx ln x = 1/x` (x>0)。經 `x = ln eˣ = e^(ln x)`，設 `g=ln x`、`f=eʸ`，chain rule 取 `1 = g'(x)·e^(ln x) = x·g'(x)` ⟹ `g'(x)=1/x`。用 `(eˣ)'=eˣ`。
- **應用②**（pp.12–13）：`d/dx xˣ = (1+ln x)xˣ` (x>0)。log differentiation：`g = ln W = x ln x` 兩邊取導，`W'/W = ln x + 1`。
- **應用③**（pp.13–14）：`d/dy arcsin y = 1/√(1−y²)` (y∈(−1,1))。經 composition identity `sin⁻¹(sin x)=x`（`f=sin`、`g=arcsin`）取導，`1 = cos x·g'(sin x)` ⟹ `1/cos x = 1/√(1−sin²x) = 1/√(1−y²)`；關鍵 `cos x ≥ 0` on `[−π/2,π/2]`。
- **Homework**（pp.21–22）：(1) arccos 定義（branch `[0,π]`）＋求 `d/dy arccos y`；(2)(i) `tan'`（x∈[0,π/2)）(ii) `sec'`（同）(iii) `(x ln x − x)'`（x>0）(iv) `2ˣ'`（x∈ℝ）；(3) `f=x³−3x²+2` 求 `f'` 根；(4) `f=(x−1)⁴` 求 `f=0`、`f'=0` 根。
- 具名人物／史實：**無**。手稿置應用於 chain rule 證明**之前**；handout 依 **D7** 已將應用排到 §3.2 證明**之後**（即本節）。

## 薄度剖析
| 區塊 | 狀態 |
|---|---|
| ln′／xˣ／arcsin′ 三推導 | **夠**（手稿全做、composition-identity 標準且具啟發） |
| 承重直覺（為何 ln/xˣ/arcsin 無從直接微分、chain rule 如何「反向」破局） | **薄**（手稿直接進每個 identity，沒點破「三者是同一個 lever」） |
| 統合敘事（六個導數讀成「一個方法用六次」而非散列） | **無→薄**（手稿是三段獨立計算）→ 承重直覺＋skip-setup 排序補 |
| logarithmic differentiation strategy | **無**（ROADMAP 指派）→ Strategy 3.2 expansion |
| arccos′／2ˣ′／(x ln x−x)′ | **薄**（手稿 HW 骨架）→ D9 升格 worked example（per-item ③） |
| arctan′ | **無**（手稿全無）→ 但 **opener line 42＋§3.2 close line 208 已 shipped 承諾**＋ROADMAP core skill ⟹ expansion 候選（§B1） |
| arcsin/arccos 域陷阱 | **無**（手稿只在 arcsin 標 y∈(−1,1)）→ Caution（ROADMAP pitfall） |
| ln 非正式依賴 | **無顯標**（手稿默用 `(eˣ)'=eˣ`）→ D8 forward fence |

## 範圍與深度
- **吃手稿這一叢**：chain rule 的應用——ln′、xˣ（log diff）、arcsin′，外加 D9 升格的 arccos′／2ˣ′／(x ln x−x)′、與 expansion 的 arctan′。深度＝手稿的**直覺-嚴謹層**（套用 §3.2 已證的 chain rule，不在本節重證；不額外 ε-δ 化）。
- **cross-ref 不重做／不重定義**：tan′/sec′ 已 **§3.1 Example 3.2(a)(b)**（D1＋③），本節**不重做**（僅引用 `sec²=1+tan²` 供 arctan′）；arcsin/arccos/arctan 的定義已 **Ch1 §1.2**，本節 **prose recall branch、不 mint Definition**（泛指「Chapter 1」，Ch1 HTML 未落地）。chain rule＝§3.2 Theorem 3.3；`(eˣ)'=eˣ`＝Ch2 §2.4 Theorem 2.5；product rule＝Ch2 §2.5 Theorem 2.6；sin′/cos′＝§3.1 Theorem 3.1/3.2。
- **forward-fence（一行，D8）**：ln x 在此**非正式當 eˣ 反函數**（`e^(ln x)=x`），嚴謹建構延 **Ch4 §4.5**。
- **D10 邊界**：照 manuscript composition-identity，**不引入 implicit-diff 框架／詞彙**（連 forward-fence 都不提——提了就引入詞彙）。
- **加法（待 ③）**：Strategy 3.2（log diff）、arctan′（§B1）、D9 三項（§B4）、（選配）Figure 3.3（§B3）、章末 chapter summary＋results recap。

## 承重直覺（一節一個，領頭）
**要微分一個無從正面下手的函數，就去微分它滿足的一個「關係」，再解出你要的導數。** 具體 failure hook（領頭打臉）：`ln x` 沒有可微的公式（它只被定義成「eˣ 的反函數」）、`xˣ` 變數同時在底與冪（power rule 與 eˣ 規則都不適用）、`arcsin y` 沒有初等閉式——三者都**無法直接微分**。破局的 lever 每次都一樣：寫下一個它滿足、且**你已會微分**的關係（`e^(ln x)=x`；`ln(xˣ)=x ln x`；`sin(arcsin y)=y`），對兩邊用 **chain rule**，再把唯一未知的導數**解出來**。這單一心像貫穿全節六個導數，也正是手稿走的路（D10：composition-identity，非 implicit-diff 詞彙）。§3.3 因此是全章的 **payoff**：chain rule 的威力不只在「正向算合成的導數」，更在「從已知關係**反向萃取**搆不到的導數」。logarithmic differentiation 是同一 lever 的 manufacture-your-own-identity 版本。

## worked example 清單（**待 ③ 批准**；含解；數學已核）
> 排序＝technique-grouped（先 log/exponential family、後 inverse-trig family），各 family 第二例起 **skip 已建立 setup**（控篇幅＋聚焦真正新的一步）。標記：**core**＝手稿主軸（無須 D9）；**D9**＝手稿 HW 升格（per-item ③）；**exp**＝自創（§B1，③）。

| # | 內容 | 技巧 | 來源／深度 | 用到（cross-ref） |
|---|---|---|---|---|
| **Ex 3.6** | `d/dx ln x = 1/x` (x>0) | 微分已知關係 `e^(ln x)=x`、解出導數（**lever 在此 full 引入**） | **core**①／full | `(eˣ)'=eˣ`〔Ch2 §2.4 Thm 2.5〕、chain rule〔§3.2 Thm 3.3〕；**D8 fence 掛此** |
| **Strategy 3.2** | logarithmic differentiation | 取 `ln` 於兩邊→微分→解 `y'`；一般式含 `f(x)^{g(x)}` | ROADMAP 指派／minted at Ex 3.7 | — |
| **Ex 3.7** | `d/dx xˣ = (1+ln x)xˣ` (x>0) | log diff：`ln W = x ln x`，`W'/W = ln x + 1` | **core**②／full（log-diff archetype） | ln′〔Ex 3.6〕、product rule〔Ch2 §2.5 Thm 2.6〕、chain rule |
| **Ex 3.8** | `d/dx 2ˣ = 2ˣ ln 2` (x∈ℝ) | `2ˣ = e^(x ln 2)`、chain rule（一句 general `aˣ=aˣ ln a`、e 為何「natural」） | **D9**(HW2iv)／short skip-setup | `(eˣ)'=eˣ`〔Ch2 §2.4〕 |
| **Ex 3.9** | `d/dx(x ln x − x) = ln x` (x>0) | product rule＋ln′：`(x ln x)'=ln x+1`，減 1 | **D9**(HW2iii)／short；**最易砍** | ln′〔Ex 3.6〕、product rule〔Ch2 §2.5〕；一句 antiderivative foreshadow |
| **Ex 3.10** | `d/dy arcsin y = 1/√(1−y²)` (y∈(−1,1)) | 微分 composition identity `sin⁻¹(sin x)=x`、解；`cos x≥0` on `[−π/2,π/2]` 定符號 | **core**③／full | sin′=cos〔§3.1 Thm 3.1〕；**Caution 掛此**〔＋選配 Fig 3.3〕 |
| **Ex 3.11** | `d/dy arccos y = −1/√(1−y²)` (y∈(−1,1)) | 同 Ex 3.10 route；`(cos)'=−sin` 致負號；`sin x≥0` on `[0,π]` | **D9**(HW1)／short skip-setup | cos′=−sin〔§3.1 Thm 3.2〕；**用正確 identity `cos(arccos y)=y`**（非手稿 loose 形，見 seed [請查核]） |
| **Ex 3.12** | `d/dy arctan y = 1/(1+y²)` (y∈ℝ) | 同 route；`sec²=1+tan²` ⟹ `1/sec² = 1/(1+y²)`；**domain 全 ℝ**（域對比） | **exp**（§B1，③）／short skip-setup | tan′=sec²〔§3.1 Ex 3.2a〕、Pythagorean `1+tan²=sec²` |

- **序與理由**：ln′（lever full 引入＋供後續 ln′）→ Strategy 3.2 → xˣ（log-diff archetype）→ 2ˣ（短，延伸「任意底經 e」）→ (x ln x−x)（短，ln′ 應用＋antiderivative 伏筆）→〔bridge 轉 inverse-trig〕→ arcsin′（full＋Caution）→ arccos′（短，符號翻轉）→ arctan′（短，域對比、honors 承諾）。手稿三 app 的相對序（ln→xˣ→arcsin）保留為骨幹；D9/exp 升格項各**緊貼同型 core 例**以「skip setup」呈現——這是全節**不淪為六個散列導數**的主要 lever。
- **自創題政策（2026-06-07）**：須 ③ 批准、題型與既有 example 不同（非換數字同型）、寫成含解 worked example、**不產 bare exercise**。arctan′（exp）為唯一自創，§B1 詳論；arccos/2ˣ/(x ln x−x) 為手稿 HW 升格（D9）。
- **正確性自核**：ln′=1/x、xˣ′=(1+ln x)xˣ、2ˣ′=2ˣln2、(x ln x−x)′=ln x、arcsin′=1/√(1−y²)、arccos′=−1/√(1−y²)、arctan′=1/(1+y²)——皆標準、已驗。

## history / application
- **history**：無可考起源／記號故事可放 → **留白**（不為 padding 硬塞）。
- **application**：六個 worked example **即** chain rule 的應用，本身就是本節的 application 錨；`(x ln x−x)'=ln x` 順帶一句伏筆「x ln x−x 是 ln x 的反導數」（指向積分），不另設真實情境錨。**留白勝過 padding**（同 §3.1/§3.2）。

## 強調 / takeaway
- **概念樞紐**：chain rule 套在一個**已知關係**上，能萃取出任何直接規則搆不到的導數——反函數（ln, arcsin, arccos, arctan）與彆扭的指數（xˣ, 2ˣ）。logarithmic differentiation 是「自己造關係」的特例。
- **可攜技能**：遇反函數或隱式關聯的函數，寫下其定義關係、用 chain rule 微分、解出導數；遇變數冪（底或冪含 x），先取 `ln` 再微分（log diff）。**認得野生的此類函數、知道該 reach for 哪個 identity。**

## 刻意不寫（餵 auditor 作 direction-conformance 反向檢查）
| 不寫什麼 | 理由 | 它該去哪 |
|---|---|---|
| ln 的嚴謹建構（積分定義／反函數存在性／連續性證明） | D8 延 Ch4 §4.5；此處只用 `e^(ln x)=x` 非正式 | Ch4 §4.5 |
| **implicit-differentiation 框架／詞彙**（連 forward-fence 都不提——提了就引入詞彙） | D10；走 composition-identity。**注意 opener line 35「inverse and implicitly defined functions」是寬鬆措辭**，xˣ via log-diff 已寬鬆滿足，**勿被它拉進 implicit-diff 小節** | 未來專章 |
| 重做 tan′／sec′ | 已 §3.1 Example 3.2(a)(b)（D1／③）；本節僅引用 `sec²=1+tan²` 供 arctan′ | §3.1 |
| 重新編號／重新定義 arcsin／arccos／arctan | 已 Ch1 §1.2；prose recall branch、不 mint Definition（同 §3.1 D3／§3.2 Option B 反炒冷飯） | Ch1 §1.2 |
| 第二個 strategy box（"inverse-function differentiation"） | ROADMAP 只派 log-diff 一個；boxed 通用反函數 recipe 有 **D10 風險**（讀如 implicit-diff 框架）；method 走 prose＋既有 Strategy 3.1（「對一個關係套 Strategy 3.1 再解」） | prose／Strategy 3.1 |
| 把導數結果升格 Theorem／Proposition | 手稿框為 application、PLAN ledger 配 Example 計數、§3.1 tan′/sec′＝Example 先例；citability 由章末 results recap 收 | —（recap） |
| §3.3 figure（除非 ③ override，§B3） | ROADMAP 未派 §3.3 圖；sin↔arcsin 反射圖屬 Ch1 §1.2 反函數**定義**、非導數技巧 | Ch1 §1.2（若要） |
| bare your-turn exercise／HW3-HW4 多項式求根升格 | README §防護欄禁自創 bare exercise；多項式屬 power-rule 代數、**非 chain-rule 技巧、離題** | manuscript exercise bank（若有）／deferred |
| 通用 `aˣ=aˣln a`／`f(x)^{g(x)}` 升格定理 | 具體 2ˣ（Ex 3.8）＋Strategy 3.2 prose 一般式已足 | — |
| 額外 ε-δ（重證 chain rule、從頭證 `cos≥0`） | §3.2 已證 chain rule；本節只在手稿層次套用 | §3.2／Ch1 |

## 篇幅帶（護欄非預算）
**5–7 A4 print 頁**（無章 opener；7 worked example——但其中 4 個 short skip-setup＋1 Strategy＋1 Caution＋章末 summary）。密度風險＝example 多。**length cut 順序：先砍 Ex 3.9 (x ln x−x)，再砍 Ex 3.8 (2ˣ)（可 fold 進 Strategy 3.2 prose）；arctan′（§B1）與 arccos′（手稿 HW）優先保留。** 明顯超出 → 回查 short examples 是否真短、有無重複 setup。

---

## A. 編號 ledger 提案（§3.3；④ 落定後回填 PLAN §5）
> 續編自 §3.2 末尾（已讀 `sec-3-2.html` header／footer ledger 確認）。**Example／Strategy 連續編；Theorem／Proposition／Definition／Figure 本節提案不 mint（留空給後續）。**

| 型別 | §3.3 提案 | 說明 |
|---|---|---|
| **Example** | `3.6` ln′、`3.7` xˣ、`3.8` 2ˣ、`3.9` (x ln x−x)′、`3.10` arcsin′、`3.11` arccos′、`3.12` arctan′ | 接 §3.2 Example 3.5；**contiguous**——若 ③ 砍某 D9/exp 項，其後順延、**無 gap** |
| **Strategy** | `3.2` = logarithmic differentiation | 接 §3.2 Strategy 3.1（chain-rule decomposition）；ROADMAP 指派 |
| **Caution** | 無編號 = arcsin／arccos 域 `(−1,1)`（端點 ±1 垂直切線、導數不存在） | ROADMAP pitfall；arccos 共用同一 box、不重貼 |
| **Remark** | `3.3` =（選配）章末 takeaway／forward，或 fold 進 plain prose | 接 §3.2 Remark 3.2 |
| **Theorem** | **不 mint**（`3.4` 留空） | §3.3 是 applications、無新定理；皆由既有 chain rule（Thm 3.3）推出 |
| **Proposition** | **不 mint**（`3.4` 留空） | results-framing：導數結果走 Example（§B2） |
| **Definition** | **不 mint**（`3.2` 留空） | arcsin/arccos/arctan 已 Ch1 §1.2；prose recall、cross-ref 泛指 |
| **Figure** | **不 mint**（`3.3` 留空；除非 ③ override，§B3） | ROADMAP 未派 §3.3 圖 |

- 交叉引用一律純文字（"by the chain rule (Theorem 3.3)"、"§3.1 的 sin′"、"Ch2 §2.4 Theorem 2.5 的 `(eˣ)'`"、"Ch4 §4.5 will construct ln rigorously"）；④ 寫完**自查每個引用都對得到存在 `env-num`**。
- **⚠ 唯一無法 DOM-audit 的 cross-ref**：arcsin/arccos/arctan 定義指向 **Ch1 §1.2**——Ch1 HTML 未落地、無 existing `env-num`。④/⑤ 自查時**標明此為 generic prose cross-ref（"Chapter 1"），非 dangling defect**，勿誤報。

## B. ③ 裁示（design panel 三視角綜合；附建議）
> **✅ ③ 已裁示（2026-06-08）：1 = 補 arctan′；2 = worked example（確認）；3 = omit Figure 3.3；4 = D9 三項全收。** 以下保留提案脈絡。

1. **【最重要】arctan′ 補不補（Ex 3.12，自創 expansion）**：**三 lens 一致建議補。** 依據：(i) **兩處已 shipped 承諾**白紙黑字點名 arctan——opener [sec-3-1.html:42](sec-3-1.html) 「derive the derivatives of arcsin x, **arctan x**, and ln x」＋§3.2 收尾 [sec-3-2.html:208](sec-3-2.html) 「the inverse functions ln x, arcsin x, and **arctan x**」；(ii) ROADMAP core skill 明列 `d/dx arctan x`；(iii) **零新機械**——同 arcsin/arccos composition-identity 技巧（D10-compliant），只用 §3.1 `tan'=sec²`＋Pythagorean；(iv) `1/(1+y²)` domain 全 ℝ，正好與 arcsin/arccos 的開區間域形成**對比**收尾。**若你否決 arctan′**：須**同步修兩處 shipped 承諾**（移除 sec-3-1:42、sec-3-2:208 的 "arctan"），否則 dangling promise。→ **請裁示：① 補 arctan′（建議）／② 否決並改兩處承諾。**
2. **results framing**：導數結果全寫 **worked example**（非 Proposition/Theorem）。三 lens 一致：手稿框為 application、PLAN ledger 配 Example、§3.1 tan′/sec′ 即 Example 先例；citability 由**章末 results recap 清單**收（不 mint 六個定理號）。→ **請確認採此（建議）。**
3. **Figure 3.3（sin↔arcsin 反射圖）**：**建議 omit（2:1 lens）**——ROADMAP 未派 §3.3 圖、反射圖屬 Ch1 §1.2 反函數**定義**而非導數技巧、且本節已 example-dense。pedagogy lens 異見：arcsin 反射圖可釘住 branch 限制與 `cos x≥0` 定符號這一**全節唯一微妙步**。→ **請裁示：① omit（建議，純散文 recall）／② 收 sin↔arcsin Figure 3.3（掛 Ex 3.10，label-light，inline SVG）。**
4. **D9 逐一批准**（手稿 HW 升格 worked example，per-item）：
   - **Ex 3.11 arccos′**（HW1）——手稿明列、同 arcsin 技巧、short skip-setup。**建議收。**
   - **Ex 3.8 2ˣ′**（HW2iv）——手稿明列、`e^(x ln 2)`、short。**建議收**（兼顧 ROADMAP `aˣ`）。
   - **Ex 3.9 (x ln x−x)′**（HW2iii）——手稿明列、用 ln′＋product rule、short、antiderivative 伏筆。**建議收**（但 length cut 第一順位）。
   - → **請逐一批准／取捨**（題型彼此不同，非換數字同型）。
5. **低風險預設（如不另指，④ 照此走）**：ln′／xˣ／arcsin′ 為手稿核心（無須 D9）；arccos′ 用**正確 identity** `cos(arccos y)=y`（非 seed 標記的手稿 loose 形 `cos⁻¹(cos y)`）；Strategy 3.2 含 `f(x)^{g(x)}` 一般式一句；章末**一段 chapter summary**（每節一句貢獻＋一句 forward Ch4）＋**results recap**（六個導數公式收成可引用清單）。

## C. 章層決策 D8/D9/D10 落地（確認）
- **D8 — ln 非正式。** `e^(ln x)=x` 取 ln′；一句 forward fence（`.informal`）掛 **Ex 3.6**，rigorous → **Ch4 §4.5**（呼應 ROADMAP ch04 line 275/284 的 loop-closure）。→ ROADMAP pitfall「ln informal」於此 realized。
- **D9 — HW 升格 worked example。** arccos′／2ˣ′／(x ln x−x)′ per-item ③（§B4）；tan′/sec′ **已 §3.1、不重做**；多項式 HW3/HW4 **不升格**（power-rule 代數、離題，至多 deferred 提一句）。**arctan′ 非 HW、為 expansion，另由 §B1 議。**
- **D10 — 不引入 implicit-diff。** 照 manuscript composition-identity；**連 forward-fence 都不提** implicit-diff（提了就引入詞彙）。opener line 35「implicitly defined functions」寬鬆措辭——xˣ via log-diff 寬鬆滿足，勿被拉進 implicit-diff 小節。
- **ROADMAP open questions**：本節無新 open question 需 resolve（D5 Def placement／D4 squeeze 已 §3.2/§3.1 resolved）；D10「implicit differentiation」維持 deferred（⑥ 後於 ROADMAP ch03 註記「§3.3 照 composition-identity、未開 implicit-diff」）。**三節全收斂後**經你確認可將 ch03 status 標「manuscript coverage complete」。

---

## 結構草圖（④ 照此寫；待 ③ 定案；intuition-first、technique-grouped）
opener（§3.3 ＝ chain rule 的 **payoff**；承重直覺「differentiate the relation, then solve」＋具體 failure hook：ln/xˣ/arcsin 無從直接微分；一句 D8 forward §Ch4、一句 §3.2 chain rule 回指）
→ **Ex 3.6 ln′**（core①；full；lever 在此引入；**D8 fence**）
→ **Strategy 3.2** logarithmic differentiation（minted；含 `f(x)^{g(x)}` 一般式一句）
→ **Ex 3.7 xˣ**（core②；full；log-diff archetype）
→ **Ex 3.8 2ˣ**（D9；short；`e^(x ln 2)`；一句 general `aˣ`／e natural）
→ **Ex 3.9 (x ln x−x)′ = ln x**（D9；short；ln′ 應用；antiderivative 伏筆）〔length cut 第一順位〕
→ bridge（從 log/exponential family 轉 inverse-trig family；同一 lever、改套 trig identity）
→ **Ex 3.10 arcsin′**（core③；full；`sin⁻¹(sin x)=x` 取導；`cos x≥0` 定符號）＋ **Caution**（域 `(−1,1)`、端點垂直切線）〔＋選配 **Figure 3.3** §B3〕
→ **Ex 3.11 arccos′**（D9；short skip-setup；負號＋`sin x≥0` on `[0,π]`；用正確 identity）
→ **Ex 3.12 arctan′**（exp §B1；short skip-setup；domain 全 ℝ 對比；honors 承諾）
→ **章末 chapter summary**：results recap（`ln'=1/x`, `(xˣ)'=(1+ln x)xˣ`, `(2ˣ)'=2ˣln2`, `arcsin'=1/√(1−y²)`, `arccos'=−1/√(1−y²)`, `arctan'=1/(1+y²)`）＋ tie §3.1（trig 導數）＋§3.2（chain rule）＋§3.3（applications）＋ forward Ch4 §4.3/§4.5（rigorous eˣ/ln）＋ MVT〔選配收 **Remark 3.3**，否則 plain prose；勿 preview MVT 機制〕。
