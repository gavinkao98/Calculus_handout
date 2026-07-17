// linebreak-gate.mjs — 版面閘：抓出被 MathJax 4 自動硬斷（ugly auto-linebreak）的顯示式。
//
// 背景：print-standalone 的 MathJax 設了 output.displayOverflow:'linebreak'
// （見各 chapter standalone 的 window.MathJax 設定），顯示式超過欄寬時會被自動斷行，
// 斷點常很醜（甚至把左式劈成兩段）。撰寫規則是「寬式一律手動斷行、不靠自動斷」
// （CONTENT_SPEC.md §數學排版「寬顯示式的斷行」）。本閘是該規則的可執行驗收：
// 重建後跑一次，列出還有哪些式子被自動斷，理想結果是 0。
//
//   node handout/html/_render/linebreak-gate.mjs                 # 檢查 standalone/ 全部檔案
//   node handout/html/_render/linebreak-gate.mjs <file.html> ... # 只檢查指定檔
//
// 退出碼：完全沒有自動斷行＝0；偵測到任何一條＝1（可接進 CI／pre-build 檢查）。
//
// 偵測原理：MathJax 4 CHTML 自動斷行時，會把該顯示式包進 <mjx-linestack>
// （每行一個 <mjx-linebox>）。作者用 \\ 寫的 aligned 換行是 mtable／mtr，不是 linestack，
// 所以這個訊號只命中「非作者本意的自動斷」。再透過 MathJax.startup.document.math
// 把命中的容器對回原始 TeX，方便定位到 fragment。
//
import { spawn } from "node:child_process";
import { existsSync, readdirSync } from "node:fs";
import { fileURLToPath, pathToFileURL } from "node:url";
import { dirname, resolve } from "node:path";

const CHROME = process.env.CHROME ?? [
  "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
  (process.env.LOCALAPPDATA ?? "") + "\\Google\\Chrome\\Application\\chrome.exe",
].find(existsSync);
if (!CHROME) {
  console.error("Chrome not found — install it or set the CHROME env var to chrome.exe");
  process.exit(2);
}

// 預設目標：html/standalone/ 下全部 print-standalone（本檔在 html/_render/，故往上一層）。
const HERE = dirname(fileURLToPath(import.meta.url));
const STANDALONE_DIR = resolve(HERE, "..", "standalone");
const args = process.argv.slice(2);
const targets = args.length
  ? args.map((p) => resolve(process.cwd(), p))
  : readdirSync(STANDALONE_DIR).filter((f) => f.endsWith("-print-standalone.html")).sort()
      .map((f) => resolve(STANDALONE_DIR, f));

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function check(file, idx) {
  if (!existsSync(file)) { console.error(`  ! 找不到檔案：${file}`); return { file, missing: true, hits: [] }; }
  // port／profile 每個目標都唯一：序列執行時避免重用 profile 被前一個 lingering Chrome 鎖住。
  const PORT = 9300 + ((process.pid + idx) % 600);
  const proc = spawn(CHROME, ["--headless=new","--disable-gpu","--no-first-run","--no-default-browser-check",
    "--hide-scrollbars",`--remote-debugging-port=${PORT}`,
    "--user-data-dir="+process.env.TEMP+"\\hk-lbgate-"+process.pid+"-"+idx,"--window-size=1120,1600",
    pathToFileURL(file).href], { stdio: "ignore" });
  try {
    let wsUrl;
    for (let i = 0; i < 100 && !wsUrl; i++) {
      try {
        const list = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
        const page = list.find((t) => t.type === "page" && t.webSocketDebuggerUrl);
        if (page) wsUrl = page.webSocketDebuggerUrl;
      } catch {}
      if (!wsUrl) await sleep(150);
    }
    if (!wsUrl) throw new Error("no CDP page target");
    const ws = new WebSocket(wsUrl);
    await new Promise((res) => (ws.onopen = res));
    let _id = 0; const pend = new Map();
    ws.onmessage = (e) => { const m = JSON.parse(e.data); if (m.id && pend.has(m.id)) { pend.get(m.id)(m); pend.delete(m.id); } };
    const cmd = (method, params = {}) => new Promise((res) => { const id = ++_id; pend.set(id, res); ws.send(JSON.stringify({ id, method, params })); });
    const evalJs = async (expr) => (await cmd("Runtime.evaluate", { expression: expr, returnByValue: true, awaitPromise: true })).result?.result?.value;
    await cmd("Runtime.enable");
    // 等 build 完成（#boot curtain 移除＝fragment 組好、MathJax typeset 完、分頁跑完）
    const ready = "document.readyState!=='loading' && !document.getElementById('boot')";
    let ok = false;
    for (let i = 0; i < 240; i++) { if (await evalJs(ready)) { ok = true; break; } await sleep(200); }
    await sleep(500);
    if (!ok) throw new Error("page never became ready (#boot still present)");
    const merr = await evalJs("document.querySelectorAll('mjx-merror, .katex-error').length");
    const probe = `(function(){
      const doc = MathJax.startup.document; const out = [];
      for (const item of doc.math) {
        const node = item.typesetRoot; if (!node || !item.display) continue;
        if (node.querySelectorAll('mjx-linestack').length > 0) {
          out.push({ lines: node.querySelectorAll('mjx-linebox').length, tex: item.math.replace(/\\s+/g,' ').trim() });
        }
      }
      return JSON.stringify(out);
    })()`;
    const hits = JSON.parse(await evalJs(probe) || "[]");
    ws.close();
    return { file, hits, merr };
  } finally {
    proc.kill();
  }
}

let totalBroken = 0, totalErr = 0;
for (let idx = 0; idx < targets.length; idx++) {
  const file = targets[idx];
  const { hits = [], merr = 0, missing } = await check(file, idx);
  if (missing) { totalBroken++; continue; }
  const name = file.split(/[\\/]/).pop();
  totalErr += merr;
  if (hits.length === 0 && merr === 0) { console.log(`[OK]   ${name} — 無自動斷行、無渲染錯誤`); continue; }
  console.log(`[FAIL] ${name} — 自動斷行 ${hits.length} 條${merr ? `、渲染錯誤 ${merr}` : ""}`);
  hits.forEach((h, i) => console.log(`   ${i + 1}. (${h.lines} 行) ${h.tex.slice(0, 140)}`));
  totalBroken += hits.length;
}
console.log(`\n合計：自動斷行 ${totalBroken} 條、渲染錯誤 ${totalErr}`);
process.exit(totalBroken > 0 || totalErr > 0 ? 1 : 0);
