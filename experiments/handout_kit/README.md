# handout_kit —— 新排版規範（HTML kit）實驗

> 隔離實驗，`experiment/seed-converge` 分支。與 [`../seed_converge/`](../seed_converge/)、
> [`../direction_layer/`](../direction_layer/) 並列。**不碰** `chapters/*.tex`、正式 pipeline、
> 未 push 的 commit。

## 這資料夾是什麼

使用者第二次找人設計的**排版規範**——這次不是 LaTeX，而是一套 **HTML/CSS/JS handout kit**：
語意標記寫內容、`shared/` 引擎自動套樣式，同一份小節檔同時出**線上閱讀版**（可即時調樣式）與
**A4 列印版**（自動分頁、存 PDF）。本資料夾在隔離沙盒裡驗證它能不能用、好不好用。

## 哪些是 designer 的、哪些是實驗的

| | 檔 | 來源 |
|---|---|---|
| **designer 原樣** | `讀我-排版指南.md`、`template-screen.html`、`template-print.html`、`new-chapter-preview.html`、`shared/`、`new-chapter/`、`example-ch01/` | 解壓自 `latex.zip`，**未改動** |
| **本實驗新增** | `exp-ch04/sec-4-2.html`、`poc-screen.html`、`poc-print.html`、`CONTRACT-html-writing.md`、`RESULT-s42-html-poc.md`、`README.md`、`_render/` | 見下 |

## 跑到哪了（狀態）

1. **冒煙測試 ✅** — designer 附的 `example-ch01`（即現有 ch01 內容）螢幕＋列印兩版都正確渲染。
   證明引擎端到端可用。
2. **真內容壓測 ✅** — 把 §4.2（e^x 連續＋指數律，高風險證明節）**從 seed 直接生成** kit 的語意
   HTML（非轉 `.tex`），渲染兩版。**244 個 KaTeX、0 錯誤、8 頁 A4**。
   完整發現見 [`RESULT-s42-html-poc.md`](RESULT-s42-html-poc.md)。
   - 結論：標記詞彙對 proof-dense 內容夠用；唯一結構性代價是 LaTeX 的自動編號／交叉引用沒了
     （`\cref`→ 全手動）。

權威產物：
- **[`CONTRACT-html-writing.md`](CONTRACT-html-writing.md)** —— 讓模型「直接生 HTML」要遵的寫作契約
  （`../seed_converge/rules.md` 的 HTML 版）。是把生成步驟接到這套 kit 的那根槓桿。
- **[`RESULT-s42-html-poc.md`](RESULT-s42-html-poc.md)** —— POC 的完整 findings 與下一步。

## 怎麼渲染（零安裝）

螢幕版要 HTTP 伺服（template 用 `fetch()` 載片段）；兩版都要瀏覽器跑 JS（KaTeX／字體走 CDN、
列印版有 client-side 分頁器）。本機已有 Python 3.12 + 系統 Chrome，無需下載任何東西。

```powershell
# 1) 在本資料夾起 HTTP server
python -m http.server 8753 --bind 127.0.0.1
# 2) 螢幕版概覽（Chrome headless）
& "C:\Program Files\Google\Chrome\Application\chrome.exe" --headless=new --hide-scrollbars `
  --window-size=1000,6200 --virtual-time-budget=30000 --screenshot="_render\poc-screen-full.png" `
  "http://127.0.0.1:8753/poc-screen.html"
# 3) 列印版逐 A4 頁 2x 截圖（CDP，等分頁器跑完）
node _render\shot.mjs "http://127.0.0.1:8753/poc-print.html" "_render\poc-print" sheets `
  '(()=>{const b=document.getElementById("printBtn");return !!b && b.disabled===false;})()'
```

互動檢視：瀏覽器直接開 `http://127.0.0.1:8753/poc-screen.html`（右下角 Tweaks 可即時調樣式）或
`poc-print.html`（右上 Print / Save as PDF）。

> `_render/` 的 PNG 是可重生的截圖，已 `.gitignore`；`_render/shot.mjs` 工具有進版控。

## 下一步（待使用者定）

見 [`RESULT-s42-html-poc.md`](RESULT-s42-html-poc.md) 末節：補編號／交叉引用 linter、試一節**含圖**
的、為 ch02/ch03 備 seed、或把這份 HTML 草稿丟進既有的**訂閱制審查迴圈**（`codex exec` 唯讀
auditor，見 [`../seed_converge/PLAN_codex_subscription_loop.md`](../seed_converge/PLAN_codex_subscription_loop.md)）
閉環——寫手半邊（Claude Code）這次已示範，走訂閱非付費 API。
