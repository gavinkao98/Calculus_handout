// One-off DOM audit via CDP (uses bundled node). Mirrors shot.mjs plumbing.
import { spawn } from "node:child_process";
const CHROME = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const URL_ = process.argv[2];
const PORT = 9334;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const proc = spawn(CHROME, [
  "--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
  `--remote-debugging-port=${PORT}`, "--user-data-dir=" + process.env.TEMP + "\\hk-chrome-chk",
  "--window-size=1120,1500", URL_,
], { stdio: "ignore" });
async function getWs() {
  for (let i = 0; i < 100; i++) {
    try { const list = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
      const page = list.find((t) => t.type === "page" && t.webSocketDebuggerUrl);
      if (page) return page.webSocketDebuggerUrl; } catch {}
    await sleep(150);
  }
  throw new Error("no CDP page target");
}
const ws = new WebSocket(await getWs());
await new Promise((res) => (ws.onopen = res));
let _id = 0; const pending = new Map();
ws.onmessage = (ev) => { const m = JSON.parse(ev.data); if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); } };
const cmd = (method, params = {}) => new Promise((res) => { const id = ++_id; pending.set(id, res); ws.send(JSON.stringify({ id, method, params })); });
const evalJs = async (expression) => (await cmd("Runtime.evaluate", { expression, returnByValue: true, awaitPromise: true })).result?.result?.value;
await cmd("Runtime.enable");
for (let i = 0; i < 240; i++) { if (await evalJs("document.querySelectorAll('.katex').length>3 && document.fonts.status==='loaded'")) break; await sleep(200); }
await sleep(400);
const report = await evalJs(`(function(){
  const paper = document.querySelector('.paper');
  const envs = [...paper.querySelectorAll('.env-head')].map(h => {
    const k = h.querySelector('.env-kicker'); const n = h.querySelector('.env-num');
    return (k?k.textContent.trim():'?') + (n?(' '+n.textContent.trim()):'');
  });
  const figs = [...paper.querySelectorAll('.fig-no')].map(f=>f.textContent.trim());
  const secNos = [...paper.querySelectorAll('.sec-no')].map(s=>s.textContent.trim());
  const txt = paper.textContent;
  // dangling-reference scan: every "Theorem/Proposition/Example/Figure N.M" mentioned in prose must exist as a label
  const labels = new Set([...envs, ...figs]);
  const refRe = /(Theorem|Proposition|Example|Figure|Corollary|Definition|Remark)\\s+(\\d+\\.\\d+)/g;
  const refs = {}; let m;
  while ((m = refRe.exec(txt))) { const key = m[1]+' '+m[2]; refs[key]=(refs[key]||0)+1; }
  const dangling = Object.keys(refs).filter(r => !labels.has(r));
  const ps = [...paper.querySelectorAll(':scope > .sec > p')];
  const lastP = ps.length ? ps[ps.length-1].textContent.slice(0,120) : '(none)';
  return JSON.stringify({
    katexErrors: document.querySelectorAll('.katex-error').length,
    secNos, envs, figs,
    labels: [...labels],
    refsFound: Object.keys(refs),
    dangling,
    lastParagraph: lastP,
    redSourceLeak: (paper.innerHTML.match(/color:\\s*#cc0000|katex-error/g)||[]).length
  }, null, 2);
})()`);
console.log(report);
ws.close(); proc.kill(); process.exit(0);
