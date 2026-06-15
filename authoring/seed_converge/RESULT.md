# 評分：seed→雙模型自動收斂（§1.1 首跑）

> 中立第三方評分（Claude 不在收斂迴圈內）。對照已簽核的 §1.1
> （[`chapters/ch01_foundations.tex`](../../legacy/tex_handout/chapters/ch01_foundations.tex) 第 16–268 行）。
> 日期：2026-06-03。

## Run metadata

- **陣容**：起草 `gemini-3.1-pro-preview` ↔ 審核 `deepseek-v4-pro`
- **回合**：4 輪（撞 `--max-rounds` 上限）、`--max-tokens 16000`
- **結果**：`converged=False`、9 calls、~**$0.17**（placeholder 價）
- **產物**：`out/full1/`（gitignored）；最終稿 `final_draft.tex`，237 行 LaTeX

---

## 裁決（先講結論）

**兩件事同時為真，且都跟我們原本的爭論不完全一樣：**

1. **這一節沒有幻覺。** seed 只當種子、模型大幅自由擴寫，產出的數學**從頭到尾正確、忠於種子、無捏造、無過度推廣**。我先前警告的「兩模型收斂到一個共同幻覺」**在 §1.1 沒有發生**——但這多半是因為 **§1.1 本身幻覺面極低**（初等、標準、無歷史／具名結果、無微妙證明）。**這個結果不能外推到高風險章節**（例如 Ch4 的 Bolzano–Weierstrass、Cauchy 收斂那種）。本跑驗證了**機制可行且在簡單素材上乾淨**，但「第二個模型抓不抓得到幻覺」這個核心假說**其實還沒被真正壓測**。

2. **「自動收斂」沒有收斂。** 迴圈跑滿 4 輪、始終 ≥1 個 actionable，最後是**撞上限**而停，不是達成共識。卡住的原因**不是數學**（R2、R3 審核都明說「mathematically sound / no mathematical errors」），而是 `% expansion:` 註記、`\index` 這類 **house-rule 小事被審核升級成 level-1「必修」**，加上 reasoning 模型的 **run-to-run 飄移**（每輪冒不同的新 nit）。**我預測的失敗模式沒出現，但「無人介入自動收斂直接能用」也沒成立**——出現的是第三種失敗：**在主觀規則合規上空轉、不終止。**

---

## 1. 覆蓋率：8 條種子 → **8/8 全到**

| 種子骨幹 | 最終稿 |
|---|---|
| one-to-one 定義 | ✅ `def:one_to_one`（含 informal gloss） |
| Horizontal Line Test | ✅ `thm:hlt` + TikZ 圖 |
| inverse 定義（domain/range 互換） | ✅ `def:inverse` + 散文說明 |
| 存在性：has inverse iff one-to-one | ✅ `thm:existence_inverse` |
| composition identities | ✅ `prop:composition_identities` |
| reflection across y=x | ✅ `prop:reflection` + TikZ 圖（含 (1,3)↔(3,1) 對應點） |
| 求反函數三步驟 | ✅ `strat:finding_inverses` |
| 三個 worked examples（x, x³, x³+2） | ✅ 三個齊全，x³+2 還附雙向組合驗證 |

**自加擴充（皆正確、皆有標記）**：開場「車子位置」類比、`f^{-1}` 非倒數的 `caution`、reflection 圖、組合驗證 example。

**比已簽核 §1.1 少的東西**（非錯誤，是豐富度差）：student-ID 例、限定定義域 [0,1]/[-1,1] 的數值暖身、**存在性定理的證明**（committed 版有證、本稿只陳述）、mapping-diagram 圖。→ 自動擴寫**覆蓋全部骨幹，但豐富度略遜**人寫版（少了一個證明與幾個例子）。

---

## 2. 幻覺帳本：**0 筆**

逐句掃過最終稿，§1.1 沒有的主張全部歸類：

| 主張 | 類別 |
|---|---|
| 車子位置／往返同位置 → 非單射 | valid-standard（動機類比，正確） |
| x² 非 1-1、x³ 是 1-1 | valid-standard |
| `f^{-1}` 的 −1 非指數、非倒數 | valid-standard（標準 caution） |
| reflection (a,b)↔(b,a) across y=x | valid-standard |
| x³+2 的雙向組合驗證 | valid-standard（算式正確） |

**fabrication / math-error / over-generalization：各 0 筆。**

---

## 3. 數學驗算（sympy + 數值）

三個 worked example 的反函數，`f(f⁻¹(x))=x` 與 `f⁻¹(f(x))=x` 皆成立：

- `f(f⁻¹(x))=x`：sympy 符號化簡三個全 `True`。
- `f⁻¹(f(x))=x`：sympy 對 `real_root(x³)` 不自動化簡（CAS 假象），改**數值驗證** x∈{−2,−1,0,1,2}（含負值）全部 `True`。

→ 全部正確。

---

## 4. 收斂行為分析（這次最有價值的發現）

逐輪 actionable 數：**2 → 4 → 1 → 1**（從未到 0）。

- **非單調、不收斂**：R2 在一次改稿後 findings 不減反增（2→4），代表**改稿動作本身引入了新的可挑剔點**，或審核模型注意力飄移。
- **L1 灌水**：R2 那 4 條全是「缺 `% expansion:` 註記 / 缺 `\index`」——auditor 自己標 `severity: low` 卻判 `level: 1`（必修）。**把格式合規升級成 blocking**，正是 over-report 稀釋的反面教材。
- **審核會 drift / 偶有不精準**：R4 說「reflection 段落缺 expansion 註記」，但下一步起草補上後，最終稿第 199 行其實已有 `% expansion:intuition — geometric explanation of the reflection property`。
- **最終稿是「未經審核」的一版**：迴圈是 `audit → revise`，跑滿 4 輪後**停在一次 revise**，所以 `final_draft.tex` 是回應 R4 的修訂、**沒有第 5 輪審核確認**。`converged=False` 反映的是 round-3 稿的狀態，不等於最終稿仍有問題。

---

## 5. 「收斂迴圈」到底做了什麼

- round 0 起草**已經數學正確且大致完整**（R1 審核即認證 mathematically correct）。
- 4 輪迭代的實質增值：補 `% expansion:` 註記、補一個 `\index`、加入組合驗證 example——**全是格式合規與小幅充實，沒有任何數學修正**（因為一開始就沒有錯）。
- 代價：多 8 次 call、never converge。**人若在迴圈內用四級紀律過濾，round 0 大概就「2 個小修、收下」**，不會空轉 4 輪。

---

## 6. 對「講義重構」的意涵

1. **「第二模型抓幻覺」假說尚未驗證**：§1.1 無幻覺可抓。要回答這題，**下一跑必須換高風險節**（有歷史／具名結果，或像 Ch4 的微妙證明）——那才是兩模型會不會一起錯、或第二模型救不救得了的真正戰場。
2. **無人介入的自動收斂有真實失敗模式**：不是（我猜的）收斂到共同幻覺，而是**在主觀規則合規上不終止 + reasoning drift**。若要走這條，需要護欄：
   - auditor 把 **blocking（數學／忠實度）** 與 **advisory（格式）** 分流，只在前者擋收斂；
   - **終止條件改成「一次乾淨的 audit」**，而非停在 revise；
   - 對 **auditor 強制四級紀律**（目前它把 L1 灌水）；
   - 仍保留**人做最終裁決**（這跟我們先前的結論一致）。
3. **品質本身可用**：Gemini 起草的 LaTeX 合規、可讀、數學正確，覆蓋全部骨幹——當「草稿產生器」是堪用的；問題在「自動收斂」這層，不在「自由擴寫」這層。

---

## 7. 成本 / token

9 calls、$0.17。auditor（DeepSeek reasoning）output 最重（單輪最高 13997 completion tok），但因 Gemini 單價較高，**drafter 每次反而較貴**。完整逐 call 數字見 `out/full1/usage.json`。

---

## 限制

- **單節、低風險、單跑**。reasoning 模型 run-to-run 會飄，重跑結果會不同。
- 只測「文字／數學」幻覺面；render 後才看得到的視覺層錯誤不在範圍。
- 結論「無幻覺」**僅就 §1.1**；切勿外推到歷史或進階分析章節。
