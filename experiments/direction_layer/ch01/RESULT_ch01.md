# 測試結果：方向層流程跑完整第一章（Ch1，逐節六階）

> 中立記錄。direction_layer 流程（[`../RULE.md`](../RULE.md)）在**整章 6 節**上的逐節端到端跑。
> 目的：測新流程在一整章上的成效，**非取代既有 `chapters/ch01_foundations.tex`**。
> 分支 `experiment/seed-converge`。產物隔離在本資料夾，未經同意不 commit。

## Run metadata
- **章**：Ch1「Inverse Functions and Limits」，手稿 `chapter 1 manuscript.pdf`（23 頁，手寫掃描）。
- **角色**：Claude＝唯一寫手（drafter）；Codex CLI `gpt-5.5`（reasoning xhigh、`--sandbox read-only`、走 ChatGPT 訂閱）＝advisory auditor。
- **節對應**（手稿與既有 ch01 §1.1–§1.6 乾淨對齊，6 節）：
  §1.1 反函數／§1.2 反三角／§1.3 函數極限／§1.4 單側與無窮／§1.5 極限定律／§1.6 ε-δ 精確定義。
- **Codex 授權**：§1.1 個別同意；**§1.2–§1.6 使用者一次性預授權整章**（仍逐節跑、仍保留 ⑥ 人收斂閘）。每節 audit read-only、~30k 訂閱 token/次（不計費）。
- **人閘**：每節 ①-verify／③ 方向閘／⑥ 收斂閘逐節保留。

## 逐節狀態
| 節 | ①seed | ②③brief（叉路決定） | ④draft | ⑤audit | ⑥ |
|---|---|---|---|---|---|
| §1.1 反函數 | ✅ 核可 | ✅ A=補反射圖；B=√x 點到為止+fref | ✅ 204 行 | ✅ v2 blocking=0 | ✅ 接受（保留 proof） |
| §1.2 反三角 | ✅ 核可 | ✅ A=非標準慣例+caution；B=三反函數圖全補；C=陷阱例 | ✅ 253 行 | ✅ v2 blocking=0 | ✅ 接受 |
| §1.3 函數極限 | ⏳ | | | | |
| §1.4 單側無窮 | ⏳ | | | | |
| §1.5 極限定律 | ⏳ | | | | |
| §1.6 ε-δ | ⏳ | | | | |

---

## §1.1 Inverse Functions

**配套**：`seed_s11.md`／`brief_s11.md`／`draft_s11.tex`／`audit_findings_s11_v1.txt`（v1）／`audit_findings_s11.txt`（v2）／`audit_prompt_s11.txt`。

**① intake**：手稿 p.1–5（至第一條水平分隔線）轉錄。①-verify 一處修正＝f₂ 圖軸標為 `a`、`b`（非 `a … n`）；其餘忠實 OK。關鍵特徵：水平線判準只幾何陳述未證；**手稿無「對 y=x 反射」圖**（標準教科書反函數的幾何核心，手稿漏）。

**②③ 方向**：兩個叉路，③ 人裁：
- **叉路 A（反射圖）＝補**。低風險加法（一張 TikZ 鏡射圖，非具名結果／微妙證明），對齊 ROADMAP key figure 與 Stewart 慣例。與 §4.2「證不證 B-W」不同——那是難證明取捨，這只是補手稿漏的標準圖。
- **叉路 B（x² 域限→√x）＝點到為止+forward-ref**。x² 碰撞後加 1–2 句 √x、一行指向 §1.2 系統處理；不展開成小節（不偷 §1.2 主力裝置）。
- 小決定：補診斷型 worked example、ID 號一對一錨（application）、水平線判準陳述＋一句幾何說明（非形式證明）、history skip。

**④ 擴寫**：`draft_s11.tex`（204 行；14 個 `% expansion:`；4 workedexample＝2 brief 要求＋2 手稿忠實；2 圖＝水平線＋反射；strategy「找反函數三步法」）。手稿數學為主軸。

**⑤ 審查**：
- **v1**：blocking=0（首審即乾淨）；3 advisory（① 水平線判準用 proof 環境→應折散文；② 圖 a,b 落極值非交點；③「wildly non-one-to-one」口語）。
- **fix**：水平線判準 proof→散文一句；重畫圖讓 a,b 在水平線兩交點下（加虛線垂足）；「wildly」→「far from one-to-one」。
- **v2**：blocking=0、乾淨。1 advisory（cancellation 的 proposition 仍用 proof 環境）——**run-to-run 飄**（v1 沒提這條）。判定：`proof` 真實專案合法（§4.2 用過、審查照過），distilled `rules.md` 短清單漏列而已；保留。

**⑥ 收斂**：使用者接受為收斂稿；保留 cancellation proof。ROADMAP 不動（反射圖已在 key figures；域限 scoping 可選記，未改）。

**takeaway（§1.1）**：低風險對照節，direction-conformance 機制運作正常（auditor 不把「補反射圖／略 history／不展開域限」誤判成缺陷，且確認照走核可方向）。一輪 advisory 修正即落乾淨 v2。核心幻覺面低（初等、無具名結果），符合「低風險對照節」定位。

**工程坑（本章新踩）**：PowerShell 跑 `codex exec` 時，**inline `cmd /c "…"` 緊鄰 `Remove-Item` 會被 harness sandbox 誤判**為「Remove-Item on '/c'」而擋下。修法：把 cmd 字串放進 `$cmd` 變數再 `cmd /c $cmd`（v1 證實可行），並移除多餘的 Remove-Item（codex `--output-last-message` 自會覆寫）。

---

## §1.2 Inverse Trigonometric Functions

**配套**：`seed_s12.md`／`brief_s12.md`／`draft_s12.tex`／`audit_findings_s12_v1.txt`（v1）／`audit_findings_s12.txt`（v2）。

**① intake**：手稿 p.5–9。①-verify OK。**關鍵核對點＝csc⁻¹/sec⁻¹ 的「微分友善」非標準值域**（`csc⁻¹:(0,π/2]∪(π,3π/2]`、`sec⁻¹:[0,π/2)∪[π,3π/2)`）——使用者確認手稿原意，並順帶裁定方向＝照手稿非標準慣例。手稿只畫限制後正向函數圖、不畫反函數自身圖；不給反三角導數（只用「微分較簡」當 sec⁻¹ 選擇理由）。

**②③ 方向**（③ 人裁）：
- **叉路 A（csc⁻¹/sec⁻¹ 慣例）＝照手稿非標準 ＋ 加 convention caution**（點明別書可能用 `sec⁻¹:[0,π/2)∪(π/2,π]`、本書選此版因 Ch3 微分較簡）。
- **叉路 B（反函數自身圖）＝三個全補**（arcsin/arccos/arctan，做成 restricted-forward＋inverse 沿 y=x 反射的合併圖；§1.1 反射圖的回呼）。
- **叉路 C（principal-interval 陷阱例）＝補**（`arcsin(sin 5π/6)=π/6≠5π/6`）。
- 小決定：`sin⁻¹x≠1/sin x` caution、arccos/arctan 各補一求值例、history/application skip。

**④ 擴寫**：`draft_s12.tex`（253 行；12 `% expansion:`；6 workedexample；5 視覺＝3 反函數合併圖＋2 三角形；def×3 arcsin/arccos/arctan；prop×1 cancellation；caution×3）。

**⑤ 審查**：
- **v1**：`converged=false`、**1 blocking（direction）**＝brief 定 2 張三角形但只畫 1（`cos(tan⁻¹x)` 那張漏）；3 advisory（三角形 x<0 邊長標示、Ch3 forward-ref 用錯 cref、其餘反三角未用 house operators+index）。auditor 確認 **csc⁻¹/sec⁻¹ 值域內部一致、符合核可慣例**（非標準沒被誤判）。
- **fix**：補第二張三角形（框成 x≥0 參考三角形、解 x<0 標示問題）；Ch3 forward-ref 改純文字「Chapter 3」；其餘反三角改 `\arccsc/\arcsec/\arccot`＋index。
- **v2**：`converged=true`、blocking=0。3 advisory 全 house_rule/L3 linter 級（個別 expansion 標記、index 覆蓋、手動 Ch3 ref——後者在 experiment artifact 本就只能手動）。→ 交 linter，不再迭代。

**⑥ 收斂**：使用者接受為收斂稿（2026-06-04）。3 條 linter 級 advisory 交 linter（不再迭代）。接著使用者要求先看 §1.1+§1.2 的 PDF 效果（見下 Preview build）。

**takeaway（§1.2）**：中風險節。**direction-conformance 抓到一個真 blocking**（漏畫 brief 要求的第二張圖）——比 §1.1 更實證了「方向符合度＝blocking」能擋住「漏寫 brief 指定項」。非標準 csc⁻¹/sec⁻¹ 慣例經 ①-verify 標「請查核」→ 人定方向 → auditor 驗內部一致但不誤判，整條「手稿主軸＋人定方向＋模型查一致性」鏈走通。一輪修正即收斂。

---

## Preview build（§1.1–§1.2，視覺複驗）

使用者於 §1.2 ⑥ 後要求先看 §1.1+§1.2 的 PDF 效果。做法與教訓（對後續節通用）：

- **編法**：`cmp_s11_s12.tex` wrapper（`book` class＋`\input{preamble/{packages,colors,layout,theorem_setup,numbering}}`，**跳過 bibliography 避 biber**，`\chapter`＋`\input` 兩 draft）。從 **repo root** 跑 `pdflatex -output-directory=experiments/direction_layer/ch01 …/cmp_s11_s12.tex` ×2（解 `\cref`）。結果：**9 頁、exit=0、0 undefined refs**。產物 `cmp_s11_s12.pdf`＋`preview_pg-*.png`。
- **★工程坑（色盤）**：色盤（`preamble/colors.tex`）**只有三色** `colorprimary`(藍)／`colorcaution`(紅)／`colorauxiliary`(灰)，**沒有 `colorsecondary`／`coloraccent`**。我 draft 初版用了後兩者→未定義會炸。**修法＝主曲線 `colorprimary`、反曲線/參考線 `colorcaution`**（正好對齊 ch01 既有 figure 慣例：raw `blue`/`red`、`red,dashed` 參考線、黑軸）。**後續各節 TikZ 一律只用這三色 macro。**
- **VLM 複驗**：逐頁查圖——反射圖（f 藍/f⁻¹ 紅/y=x 虛線/標點）、HLT 圖（a、b 在紅線兩交點正下方，v1 修正生效）、三反三角合併圖（principal interval 上色＋反射）、兩三角形、Strategy/caution 方塊、非標準 csc⁻¹/sec⁻¹ 值域顯示——**全部正確**。numbering：Definition/Example/Caution/Strategy/Figure 皆 1.x 正常。

---

## §1.3–§1.6
⏳ 待跑（六階照 RULE.md，人閘 ①-verify／③／⑥ 逐節保留）。
- §1.3 函數的極限（手稿 p.9–11）／§1.4 單側與無窮（p.11–14）／§1.5 極限定律（p.14–17）／§1.6 ε-δ（p.18–23）。
- Codex 審查 §1.2–§1.6 **已整章預授權**（read-only、每節 ~30k 訂閱 token），仍逐節跑、仍保留 ⑥ 人收斂閘。

---

## 本次 session 停點（2026-06-04）
- **完成**：§1.1、§1.2 全六階收斂並經使用者收斂閘接受；§1.1+§1.2 PDF preview 編譯乾淨（9 頁）並 VLM 複驗。
- **下一步（換機接續）**：從 **§1.3 函數的極限** 的 ① intake 開始（讀手稿 p.9–11 → seed_s13.md → ①-verify）。流程權威見 [`../RULE.md`](../RULE.md)、契約見本檔上方各節記錄。
- **已 commit**：本資料夾 source＋results（`.gitignore` 忽略可重生的 PDF/PNG/audit_prompt/LaTeX 中間檔；PDF 用 `cmp_s11_s12.tex` 從 repo root `pdflatex -output-directory=…` ×2 重生）。
- **工程備忘（後續節沿用）**：⑤ 組 prompt 走 `[IO.File]::ReadAllText` UTF-8 ＋ `cmd /c "codex exec … < prompt"`（用 `$cmd` 變數形式，避開 sandbox 對 inline `cmd /c`+`Remove-Item` 的誤判）＋ CJK 護欄；TikZ 只用 `colorprimary/colorcaution/colorauxiliary` 三色。

---

## 跨節 takeaway / 對照既有 ch01 / 踩到的坑（收尾彙整）
⏳ 全章跑完填：逐節 seed→brief→draft→audit 收斂彙整、對照既有 `ch01_foundations.tex` 的差異、跨節教訓、工程坑總結。
