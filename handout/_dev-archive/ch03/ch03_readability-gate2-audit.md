# Ch3 可讀性回填 — gate-2（Codex）原始輸出轉錄 ＋ triage

> 版控紀錄（scratchpad gitignored、換機即失，故轉錄於此，比照 `ch01_readability-gate2-audit.md`／`ch03_example-supplement-audit.md`）。
> gate-2 = Codex `codex-cli 0.136.0`（PATH，ChatGPT 訂閱；model `gpt-5.5`、reasoning effort `xhigh`、sandbox `read-only`）獨立跨模型複核同兩條檢查（① reader-persona、② introduce-before-use）。
> 對**現行** Ch3（gate-1 0 survivors，未套用任何改動）跑；clean inline UTF-8 餵入（HTML 註解已剝除、**非 -C 自讀**）；schema-constrained 輸出。2026-06-28。

## 執行參數

- builder：`scratchpad/gate2/build_prompts.py`（Python UTF-8 read+write；剝 `<!-- -->`；每節 prompt = 指令 ①② ＋ **本章先前已介紹之記號/術語 ledger（③）** ＋ 該節清乾淨全文 inline）。三節 prompt 各 ~26k 字元、0 個 U+FFFD。
- 指令：`codex exec -s read-only -C <repo> --output-schema schema.json -o out-<sec>.json - < prompt-<sec>.txt`（Bash 工具、prompt 經 stdin 餵 raw UTF-8）。
- schema：全欄 required、`additionalProperties:false`、enum、無 min/max（`section`／`findings[]`（check·dimension·severity·tier·fix_type·locus·quote·what_stalls·minimal_unstick）／`notes`）。
- smoke test：先跑 sec-3-1 → schema 解析 OK、輸出 JSON 0 個 U+FFFD、編碼正常（`—`／`θ`／`π`／`≤`／`∘` 皆無亂碼）→ 再循序（非並發）跑 sec-3-2、sec-3-3。
- 用量：sec-3-1 **20,422**｜sec-3-2 **20,977**｜sec-3-3 **19,544** ≈ **60,943 token**（訂閱配額；遠低於 ~8–11 萬估值，亦低於 Ch1 全章 172,715）。
- raw findings：**0（0+0+0）**。

## Triage 結論（要點）

- **gate-2 全章 0 raw findings**——三節 Codex 皆回 `findings:[]`、10 維度（U1–U5／F1–F5）全 clean。
- **與 gate-1 取交集：兩閘交集為空集**。gate-1（Claude Opus；reader pass 2 raw → 對抗 verifier 全砍、completeness pass 0 new）＋ gate-2（Codex gpt-5.5 獨立）**各自獨立**判 ch03 在 ① reader-persona、② introduce-before-use 兩條檢查上乾淨。交集＝最低後悔＝最高信心 clean。
- **無迴歸可抓**：本章 gate-1 0 survivors → 未套用任何 fragment 改動 → gate-2 的「抓套用迴歸」用途不適用（與 Ch1 不同：Ch1 靠 gate-2 抓到套用 G1-5 時掉 `integers`）。gate-2 在此純扮演**跨模型獨立 clean 確認**。
- **為何 ch03 比 Ch1 乾淨**：ch03 在「introduce-before-use 已寫入 `CONTENT_DIRECTION` §2 方向層」之後撰寫（排序問題在編號未鎖前已上游攔掉），且已過完整 S·A·V 散文閘（含 U／F 維度）；本兩條檢查多被既有閘涵蓋。乾淨是預期且有效的結果。
- **③ ledger 有效**：餵入「Ch1/Ch2/§3 前節已介紹之記號術語」ledger 後，Codex 未把任何 Ch1/Ch2 cross-ref（squeeze §1.5、quotient §2.5、`e^x` §2.4、Theorem 3.1 等）誤報為先用後定義——避免了 Ch3 對 Ch1（gate-2 對首章）才會有的「每個 cross-ref 都當 U4」假陽性叢集。

## sec-3-1 — 3.1 Derivatives of the Sine and Cosine Functions（含章開場）  (20,422 tok, 0 findings)

- **findings:** （無）
- **Codex notes（原文轉錄）:** “No tier 1-3 findings. For introduce-before-use, I checked symbols/terms including composition, chain rule, logarithmic differentiation, inverse/implicitly defined functions, radians, theta/h substitution, even function, unit circle/tangent/sector/chord/arc, inequality (1), continuity, squeeze theorem, proposition/theorem references, quotient rule, sec/csc/cot, simple harmonic motion, and derivative-cycle notation. Items were either already in the ledger, standard precalculus notation, glossed in place, or clearly previewed as later chapter business. Clean dimensions: U1, U2, U3, U4, U5, F1, F2, F3, F4, F5.”

## sec-3-2 — 3.2 The Chain Rule  (20,977 tok, 0 findings)

- **findings:** （無）
- **Codex notes（原文轉錄）:** “Ran exactly the two requested independent sweeps: reader-persona first-read friction and introduce-before-use. For introduce-before-use, I checked symbols/terms/notations including composition/composite, P=f∘g, h increments, u0/y0, Leibniz dy/dx form, inner/outer function language, differentiability/remainder form, R, R1/R2/R3, m1/m2, epsilon-delta symbols, α/α1, quotient/product/power-rule references, sin^2 x/cos^2 x notation, and inverse-function names in the closing paragraph against the ledger and local glosses. No tier 1-3 findings. Clean dimensions: U1, U2, U3, U4, U5, F1, F2, F3, F4, F5.”

## sec-3-3 — 3.3 Applications of the Chain Rule（含 Chapter summary）  (19,544 tok, 0 findings)

- **findings:** （無）
- **Codex notes（原文轉錄）:** “Clean: no tier 1-3 findings. introduce-before-use checked symbols/terms including ln, logarithmic differentiation, W, y as a function of x, d/dx ln y = y'/y, d/dx ln u = u'/u, antiderivative, inverse-trig branch/interior language, vertical tangent, open interval restrictions, and summary domain conditions; all are either ledger-known, standard notation, introduced/glossed in place, or immediately recoverable from adjacent prose. Clean dimensions: U1, U2, U3, U4, U5, F1, F2, F3, F4, F5.”

## 收斂

- **ch03 可讀性回填（① reader-persona ＋ ② introduce-before-use）雙閘收斂：gate-1 0 survivors ＋ gate-2 0 findings ＝整章乾淨、0 課文改動。**
- 無套用 → 無 build、無範圍限定 Mode B、無 render 自驗需求（未碰任何 `fragments/` 或 `chapter3-print-standalone.html`）。
- 產物：`REVIEW-ch03-readability-{gate1,gate2,applied}.html` ＋ 本檔。
