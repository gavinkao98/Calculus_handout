// page_shots.mjs <fileUrl> <outDir> <nShots>  — headless-Chrome viewport screenshots at spread scroll positions
import { spawn } from "node:child_process";
import { writeFileSync, mkdirSync } from "node:fs";
const CHROME = process.env.CHROME;
const [, , URL_, OUT, N = "8"] = process.argv; mkdirSync(OUT, { recursive: true });
const PORT = 9300 + (process.pid % 400); const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const proc = spawn(CHROME, ["--headless=new", "--disable-gpu", "--no-first-run", "--hide-scrollbars", `--remote-debugging-port=${PORT}`, "--user-data-dir=" + process.env.TEMP + "\pg-cdp-" + process.pid, "--window-size=1400,1000", URL_], { stdio: "ignore" });
async function getWs() { for (let i = 0; i < 100; i++) { try { const l = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json(); const p = l.find((t) => t.type === "page" && t.webSocketDebuggerUrl); if (p) return p.webSocketDebuggerUrl; } catch {} await sleep(150); } throw new Error("no target"); }
const ws = new WebSocket(await getWs()); await new Promise((r) => (ws.onopen = r));
let _id = 0; const pending = new Map(); ws.onmessage = (ev) => { const m = JSON.parse(ev.data); if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); } };
const cmd = (method, params = {}) => new Promise((res) => { const id = ++_id; pending.set(id, res); ws.send(JSON.stringify({ id, method, params })); });
const ev = async (e) => (await cmd("Runtime.evaluate", { expression: e, returnByValue: true, awaitPromise: true })).result?.result?.value;
await cmd("Page.enable"); await cmd("Runtime.enable"); await sleep(2500);
const H = await ev("document.documentElement.scrollHeight"); console.log("scrollHeight", H);
const n = Number(N);
for (let i = 0; i < n; i++) { const y = Math.round((H - 1000) * i / (n - 1)); await ev(`window.scrollTo(0, ${y}); 1`); await sleep(400); const s = await cmd("Page.captureScreenshot", { format: "jpeg", quality: 70 }); writeFileSync(`${OUT}/shot_${String(i).padStart(2, "0")}.jpg`, Buffer.from(s.result.data, "base64")); }
ws.close(); proc.kill(); console.log("done"); process.exit(0);
