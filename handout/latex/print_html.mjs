// Print a built print-standalone to one A4 PDF (the對照報告's HTML side).
//
//   node print_html.mjs <standalone.html> <out.pdf>
//
// Chrome launch / CDP scaffolding and the #boot readiness signal are lifted from
// export_figs.mjs (proven on this machine); the only difference is a whole-document
// Page.printToPDF with preferCSSPageSize (the standalone carries @page{size:A4;margin:0}).
import { spawn } from "node:child_process";
import { writeFileSync, existsSync } from "node:fs";
import { resolve } from "node:path";
import { pathToFileURL } from "node:url";

const CHROME = process.env.CHROME ?? [
  "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
  (process.env.LOCALAPPDATA ?? "") + "\\Google\\Chrome\\Application\\chrome.exe",
].find(existsSync);
if (!CHROME) {
  console.error("Chrome not found — install it or set the CHROME env var to chrome.exe");
  process.exit(1);
}

const [, , SRC, OUT] = process.argv;
if (!SRC || !OUT) {
  console.error("usage: node print_html.mjs <standalone.html> <out.pdf>");
  process.exit(1);
}

const PORT = 9700 + (process.pid % 250);
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const proc = spawn(CHROME, [
  "--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
  "--hide-scrollbars", `--remote-debugging-port=${PORT}`,
  "--user-data-dir=" + process.env.TEMP + "\\hk-htmlprint-" + process.pid,
  "--window-size=1120,1600", pathToFileURL(resolve(SRC)).href,
], { stdio: "ignore" });

async function getWs() {
  for (let i = 0; i < 100; i++) {
    try {
      const list = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
      const page = list.find((t) => t.type === "page" && t.webSocketDebuggerUrl);
      if (page) return page.webSocketDebuggerUrl;
    } catch {}
    await sleep(150);
  }
  throw new Error("no CDP page target");
}

const ws = new WebSocket(await getWs());
await new Promise((res) => (ws.onopen = res));
let _id = 0;
const pending = new Map();
ws.onmessage = (ev) => {
  const m = JSON.parse(ev.data);
  if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); }
};
const cmd = (method, params = {}) =>
  new Promise((res) => { const id = ++_id; pending.set(id, res); ws.send(JSON.stringify({ id, method, params })); });
const evalJs = async (expression) =>
  (await cmd("Runtime.evaluate", { expression, returnByValue: true, awaitPromise: true })).result?.result?.value;

await cmd("Page.enable");
await cmd("Runtime.enable");

// #boot 只在 fragments 組裝、MathJax 排版、圖 hydrate、分頁全部完成後才移除（同 shot.mjs）
const readyExpr = "document.readyState!=='loading' && !document.getElementById('boot')";
let ok = false;
for (let i = 0; i < 240; i++) { if (await evalJs(readyExpr)) { ok = true; break; } await sleep(200); }
if (!ok) { console.error("page never became ready"); proc.kill(); process.exit(1); }
await evalJs("document.fonts.ready");
await sleep(400);

const nSheets = await evalJs("document.querySelectorAll('.sheet').length");
const res = await cmd("Page.printToPDF", { preferCSSPageSize: true, printBackground: true });
writeFileSync(resolve(OUT), Buffer.from(res.result.data, "base64"));
console.log(`wrote ${OUT} (${nSheets} sheets)`);
proc.kill();
process.exit(0);
