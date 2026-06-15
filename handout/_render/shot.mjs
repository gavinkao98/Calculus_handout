// Minimal dependency-free CDP screenshotter (Node >=21 for global WebSocket/fetch).
// Launches headless Chrome, waits for a readiness expression, then captures either
// every element matching a selector (default ".sheet" = one A4 print page) or the
// full page, at 2x device scale. Used to verify the handout render fidelity and to
// feed rendered figure PNGs to the handout-figure-audit subagent (gate 1, visual).
//
//   node shot.mjs <url> <outDir/prefix> <mode> [readyExpr]
//     mode = "sheets" (each .sheet -> prefix-pNN.png) | "full" (prefix.png)
//
import { spawn } from "node:child_process";
import { writeFileSync } from "node:fs";

const CHROME = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const [, , URL_, PREFIX, MODE = "sheets", READY] = process.argv;
const PORT = 9333;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const proc = spawn(CHROME, [
  "--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
  "--hide-scrollbars", `--remote-debugging-port=${PORT}`,
  "--user-data-dir=" + process.env.TEMP + "\\hk-chrome-cdp",
  "--window-size=1120,1500", URL_,
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

// wait for readiness
const readyExpr = READY || "document.querySelectorAll('.katex').length>3 && document.fonts.status==='loaded'";
let ok = false;
for (let i = 0; i < 240; i++) { if (await evalJs(readyExpr)) { ok = true; break; } await sleep(200); }
await sleep(500); // settle
const errs = await evalJs("document.querySelectorAll('.katex-error').length");
const katexN = await evalJs("document.querySelectorAll('.katex').length");
console.log(`ready=${ok}  katex=${katexN}  katex-errors=${errs}`);

const shoot = async (clip, file) => {
  const { data } = (await cmd("Page.captureScreenshot", {
    format: "png", captureBeyondViewport: true,
    clip: { ...clip, scale: 2 },
  })).result;
  writeFileSync(file, Buffer.from(data, "base64"));
  console.log("  wrote", file, `(${clip.width}x${clip.height})`);
};

if (MODE === "full") {
  const dims = JSON.parse(await evalJs(
    "JSON.stringify({w:document.documentElement.scrollWidth,h:document.documentElement.scrollHeight})"));
  await shoot({ x: 0, y: 0, width: dims.w, height: dims.h }, `${PREFIX}.png`);
} else {
  const rects = JSON.parse(await evalJs(
    "JSON.stringify([...document.querySelectorAll('.sheet')].map(el=>{const r=el.getBoundingClientRect();" +
    "return {x:r.left+scrollX,y:r.top+scrollY,w:r.width,h:r.height};}))"));
  console.log(`  ${rects.length} sheet(s)`);
  for (let i = 0; i < rects.length; i++) {
    const r = rects[i];
    await shoot({ x: Math.round(r.x), y: Math.round(r.y), width: Math.round(r.w), height: Math.round(r.h) },
      `${PREFIX}-p${String(i + 1).padStart(2, "0")}.png`);
  }
}

ws.close();
proc.kill();
process.exit(0);
