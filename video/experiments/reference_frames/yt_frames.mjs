// yt_frames.mjs — headless-Chrome CDP frame grabber for YouTube (no file download).
// Adapted from handout/figkit/shot.mjs (Node >=21, dependency-free).
//   node yt_frames.mjs <videoId> <outDir> sample <start> <end> <step> [width]
//   node yt_frames.mjs <videoId> <outDir> at <t1,t2,...> [width] [strip 0|1] [dt]
import { spawn } from "node:child_process";
import { writeFileSync, mkdirSync, existsSync } from "node:fs";
const CHROME = process.env.CHROME ?? [
  "C:\Program Files\Google\Chrome\Application\chrome.exe",
  "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
  (process.env.LOCALAPPDATA ?? "") + "\Google\Chrome\Application\chrome.exe",
].find(existsSync);
if (!CHROME) { console.error("Chrome not found"); process.exit(1); }
const [, , VID, OUT, MODE, ...REST] = process.argv;
mkdirSync(OUT, { recursive: true });
const PORT = 9300 + (process.pid % 400);
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const proc = spawn(CHROME, [
  "--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check", "--hide-scrollbars",
  "--autoplay-policy=no-user-gesture-required", "--mute-audio", "--lang=en-US",
  `--remote-debugging-port=${PORT}`, "--user-data-dir=" + process.env.TEMP + "\yt-cdp-" + process.pid,
  "--window-size=1920,1080", `https://www.youtube.com/watch?v=${VID}`,
], { stdio: "ignore" });
async function getWs() {
  for (let i = 0; i < 100; i++) {
    try { const list = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
      const page = list.find((t) => t.type === "page" && t.webSocketDebuggerUrl); if (page) return page.webSocketDebuggerUrl; } catch {}
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
await cmd("Page.enable"); await cmd("Runtime.enable");
const V = `document.querySelector('video.html5-main-video')`;
let info = null;
async function initPlayer() {
  let ready = false;
  for (let i = 0; i < 240; i++) { if (await evalJs(`(()=>{const v=${V}; return !!(v && v.duration>0)})()`)) { ready = true; break; } await sleep(250); }
  if (!ready) { console.error("no video element; title=", await evalJs("document.title")); return false; }
  await evalJs(`(async()=>{const v=${V}; v.muted=true; try{await v.play()}catch(e){} return 1})()`);
  for (let i = 0; i < 160; i++) {
    const st = JSON.parse(await evalJs(`(()=>{const ad=!!document.querySelector('.ad-showing, .ad-interrupting'); const b=document.querySelector('.ytp-skip-ad-button, .ytp-ad-skip-button, .ytp-ad-skip-button-modern, button.ytp-ad-skip-button-container'); if(b){try{b.click()}catch(e){}} const v=${V}; return JSON.stringify({ad, dur:v.duration, t:v.currentTime})})()`));
    if (!st.ad && st.dur > 30) break; await sleep(500);
  }
  await evalJs(`(()=>{const p=document.getElementById('movie_player'); try{p.setPlaybackQualityRange('hd1080','hd1080'); p.setPlaybackQuality('hd1080')}catch(e){} return 1})()`);
  await sleep(2000);
  await evalJs(`(()=>{const p=document.getElementById('movie_player'); try{p.pauseVideo()}catch(e){} ${V}.pause(); return 1})()`);
  info = JSON.parse(await evalJs(`(()=>{const v=${V}; const p=document.getElementById('movie_player'); return JSON.stringify({dur:v.duration, w:v.videoWidth, h:v.videoHeight, q:(p&&p.getPlaybackQuality&&p.getPlaybackQuality()), title:document.title})})()`));
  console.log(JSON.stringify(info));
  return true;
}
if (!(await initPlayer())) { proc.kill(); process.exit(2); }
writeFileSync(OUT + "/info.json", JSON.stringify(info));
async function reinit(t) {
  await cmd("Page.navigate", { url: `https://www.youtube.com/watch?v=${VID}&t=${Math.max(0, Math.floor(t))}s` });
  await sleep(1500);
  return initPlayer();
}
const pad = (t) => String(Math.round(t * 10) / 10).padStart(7, "0");
async function grab(t, path, width) {
  for (let attempt = 0; attempt < 3; attempt++) {
    const data = await evalJs(`(async()=>{const p=document.getElementById('movie_player');
      const b=document.querySelector('.ytp-skip-ad-button, .ytp-ad-skip-button, .ytp-ad-skip-button-modern'); if(b){try{b.click()}catch(e){}}
      try{p.playVideo()}catch(e){}
      try{p.seekTo(${t}, true)}catch(e){ const v=${V}; if(v) v.currentTime=${t}; }
      let ok=false;
      for(let i=0;i<80;i++){ const vv=${V}; if(vv && Math.abs(vv.currentTime-${t})<0.6 && vv.readyState>=2 && vv.videoWidth>0 && !document.querySelector('.ad-showing')){ok=true;break;} await new Promise(r=>setTimeout(r,100)); }
      const vv=${V}; try{p.pauseVideo()}catch(e){} if(vv) vv.pause(); await new Promise(r=>setTimeout(r,200));
      const st={ok, ct:vv?vv.currentTime:-1, rs:vv?vv.readyState:-1, vw:vv?vv.videoWidth:-1, ps:(p&&p.getPlayerState)?p.getPlayerState():null, ad:!!document.querySelector('.ad-showing'), err:(vv&&vv.error&&vv.error.code)||null, perr:!!document.querySelector('.ytp-error')};
      if(!ok) return JSON.stringify(st);
      const W=${width}||vv.videoWidth; const H=Math.round(W*vv.videoHeight/vv.videoWidth); const c=document.createElement('canvas'); c.width=W; c.height=H; c.getContext('2d').drawImage(vv,0,0,W,H);
      st.d=c.toDataURL('image/jpeg',0.85); return JSON.stringify(st)})()`);
    let o; try { o = JSON.parse(data); } catch { console.error("[bad]", String(data).slice(0, 120)); o = null; }
    if (o && o.ok && o.d && o.d.length > 1000) { writeFileSync(path, Buffer.from(o.d.split(",")[1], "base64")); return o.ct; }
    if (o) { delete o.d; console.error(`[retry ${attempt}] t=${t}`, JSON.stringify(o)); }
    if (attempt === 0) { const shot = await cmd("Page.captureScreenshot", { format: "jpeg", quality: 55 }); if (shot.result?.data) writeFileSync(`${OUT}/_debug_${pad(t)}.jpg`, Buffer.from(shot.result.data, "base64")); }
    if (attempt >= 1) { await reinit(t); } else { await sleep(1500); }
  }
  return false;
}
if (MODE === "sample") {
  const [s, e, step, w] = REST.map(Number);
  for (let t = s; t <= Math.min(e, info.dur - 0.5); t += step) { const ct = await grab(t, `${OUT}/t_${pad(t)}.jpg`, w || 640); process.stdout.write(`${t}->${ct === false ? "FAIL" : ct.toFixed(1)} `); }
} else if (MODE === "at") {
  const ts = REST[0].split(",").map(Number); const w = Number(REST[1] || 1280); const strip = Number(REST[2] || 0); const dt = Number(REST[3] || 0.6);
  for (const t of ts) {
    const offs = strip ? [-dt, 0, dt] : [0];
    for (const [k, o] of offs.entries()) { const tt = Math.max(0, t + o); const ct = await grab(tt, `${OUT}/at_${pad(t)}_${"abc"[k]}.jpg`, w); process.stdout.write(`${tt.toFixed(1)}->${ct === false ? "FAIL" : ct.toFixed(1)} `); }
  }
}
console.log("\ndone"); ws.close(); proc.kill(); process.exit(0);
