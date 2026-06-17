"""Generator: VISUAL-FRAME gate1 §1.1 report -> SELF-CONTAINED standalone HTML.

Reads the workflow digest (sibling .digest.json) and emits a dark-themed,
MathJax standalone report into video/content_scripts/_audit/.

PORTABILITY CONTRACT (see video/README.md §資料夾架構與版控策略):
  Every frame is embedded as a base64 data URI — the HTML carries its own
  images, so it renders on any machine after a fresh `git clone`, even though
  the render output under output/ is gitignored. NO external image refs.

Frame sources:
  - <nn>_<scene>/final.png      : regenerable; read from the live render at
                                  video/output/ch01/s1.1/critic/frames/ when
                                  present (re-run §1.1 mock to regenerate).
  - <nn>_<scene>/final_before.png : irreproducible pre-fix evidence; preserved
                                  (tracked) under ./frames_before/.

This generator + its .digest.json + ./frames_before/ all live in a tracked
location so the report can be regenerated after the gitignored output/ is wiped.
"""
from __future__ import annotations
import base64
import html
import io
import json
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent           # .../video/content_scripts/_audit/_gen
REPO = HERE.parents[3]                            # repo root (video/content_scripts/_audit/_gen -> 3 up)
DIGEST = HERE / "REVIEW-ch01_inverse_functions-visualframe.digest.json"
OUT = HERE.parent / "REVIEW-ch01_inverse_functions-visualframe.html"
FRAMES_LIVE = REPO / "video" / "output" / "ch01" / "s1.1" / "critic" / "frames"
FRAMES_BEFORE = HERE / "frames_before"
MAX_W = 1100                                      # downscale width for embedded frames

# ---- regression / blocking resolution (filled after the recap re-verify) ----
REGRESSION = {
    "fixed": True,
    "verdict": "0 visual blocking",
    "note": ("獨立 visual-frame-audit agent 重判新 recap 幀：VERDICT 0 visual blocking。"
             "point 04「first).」完整落在底部安全邊界內（baseline ~478/540px、底下約 60px 間距）；"
             "全 4 點＋3 公式卡在框、無相撞；縮短 point.0／point.2 為 2 行未引入新 wrap／失衡／overlap，"
             "僅餘 low-severity A1／A4／A7 美學註記（右欄略偏下、卡片內距微差、recap 諸點刻意等重無單一焦點）。"),
}

_URI_CACHE: dict[str, str] = {}
_MISSING: list[str] = []


def _resolve(rel: str) -> Path:
    """Map a frame subpath (e.g. '17_recap/final.png') to a real file."""
    if rel.endswith("final_before.png"):
        return FRAMES_BEFORE / rel
    return FRAMES_LIVE / rel


def uri(rel: str) -> str:
    """Return a base64 data URI for a frame subpath, downscaled to MAX_W.

    Falls back to an inline SVG placeholder if the source frame is missing
    (e.g. final.png before §1.1 is re-rendered)."""
    if rel in _URI_CACHE:
        return _URI_CACHE[rel]
    p = _resolve(rel)
    if not p.exists():
        _MISSING.append(rel)
        ph = ("<svg xmlns='http://www.w3.org/2000/svg' width='640' height='360'>"
              "<rect width='100%' height='100%' fill='#1d2630'/>"
              "<text x='50%' y='50%' fill='#9aa7b4' font-family='sans-serif' "
              "font-size='18' text-anchor='middle'>frame missing — re-render §1.1</text></svg>")
        data = "data:image/svg+xml;base64," + base64.b64encode(ph.encode()).decode()
        _URI_CACHE[rel] = data
        return data
    im = Image.open(p).convert("RGB")
    if im.width > MAX_W:
        im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format="PNG", optimize=True)
    data = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
    _URI_CACHE[rel] = data
    return data


def esc(s):
    return html.escape(str(s), quote=False)


def ac(v):
    v = int(v)
    if v >= 85:
        return "ok"
    if v >= 72:
        return "warn"
    return "bad"


def main():
    d = json.loads(DIGEST.read_text(encoding="utf-8"))
    scenes = d["scenes"]
    summ = d["summary"]

    # split advisory v_findings into "real defect" vs "clean-check noise"
    def real_v(f):
        fix = (f.get("fix", "") + f.get("why", "")).lower()
        return not ("none needed" in fix or "clean check" in fix or "no defect" in fix)

    rows = []
    cards = []
    for r in scenes:
        s, a = r["scene"], r["audit"]
        asc = a["a_scores"]
        amin = min(asc.values())
        vb = a.get("visual_blocking_count", 0)
        vadv = [f for f in a.get("v_findings", []) if f["severity"] == "Advisory" and real_v(f)]
        vbcell = (f'<span class="bad">●{vb}</span>' if vb else '<span class="ok">0</span>')
        rows.append(
            f'<tr><td><code>{s["nn"]}</code></td><td>{esc(s["scene_id"])}'
            f'<div class="mut" style="font-size:12px">{esc(a.get("verdict_line","")[:0])}</div></td>'
            f'<td><span class="tag">{esc(s["template"])}</span></td>'
            f'<td style="text-align:center">{vbcell}</td>'
            f'<td><span class="chip {ac(amin)}">min {amin}</span></td></tr>')

        # per-scene card
        defs = a.get("defects", [])
        med = [x for x in defs if x["severity"] == "med"]
        low = [x for x in defs if x["severity"] == "low"]
        det = []
        for f in vadv:
            det.append(
                f'<li><b class="warn">[{esc(f["dimension"])} Advisory]</b> '
                f'{esc(f["evidence"])}<br><span class="mut">→ {esc(f["fix"])}</span></li>')
        for x in med:
            det.append(
                f'<li><b class="warn">[{esc(x["dimension"])} · med]</b> {esc(x["issue"])}'
                f'<br><span class="mut">→ {esc(x["suggestion"])}</span></li>')
        for x in low:
            det.append(
                f'<li><b class="mut">[{esc(x["dimension"])} · low]</b> {esc(x["issue"])}</li>')
        det_html = ("<ul>" + "".join(det) + "</ul>") if det else '<p class="mut">無 advisory／polish defect。</p>'
        chips_full = "".join(
            f'<span class="chip {ac(asc[k])}">{k} {asc[k]}</span>' for k in
            ["A1", "A2", "A3", "A4", "A5", "A6", "A7"])
        frame = f'{s["nn"]}_{s["scene_id"]}/final.png'
        cards.append(f'''
  <div class="card">
    <h3>{esc(s["nn"])} · {esc(s["scene_id"])} <span class="tag">{esc(s["template"])}</span>
        {'<span class="pill-bad">V-BLOCKING</span>' if vb else '<span class="pill-ok">V clean</span>'}</h3>
    <img class="thumb" src="{uri(frame)}" alt="{esc(s["scene_id"])}">
    <div class="chips">{chips_full}</div>
    <details><summary>{len(det)} advisory／polish note(s)</summary>{det_html}</details>
  </div>''')

    table = "\n".join(rows)
    cardhtml = "\n".join(cards)

    reg = REGRESSION
    reg_pill = (f'<span class="pill-ok">已修 · 回歸 {esc(reg["verdict"])}</span>'
                if reg["fixed"] and reg["verdict"] != "PENDING"
                else '<span class="pill-bad">待回歸驗證</span>')

    doc = f'''<!DOCTYPE html>
<html lang="zh-Hant"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>§1.1 VISUAL-FRAME gate1 視覺稽核報告</title>
<script>
window.MathJax={{tex:{{inlineMath:[['$','$'],['\\\\(','\\\\)']]}},svg:{{fontCache:'global'}}}};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js" id="MathJax-script" async></script>
<style>
  :root{{--bg:#0f1419;--panel:#171e26;--panel2:#1d2630;--ink:#e6edf3;--muted:#9aa7b4;
    --line:#2a3742;--ok:#3fb950;--warn:#d29922;--accent:#58a6ff;--bad:#f85149;--code:#0b1118;--codeink:#c9d4df;}}
  *{{box-sizing:border-box}}
  body{{margin:0;background:var(--bg);color:var(--ink);
    font:16px/1.65 -apple-system,"Segoe UI",Roboto,"Noto Sans CJK TC","Microsoft JhengHei",sans-serif;}}
  .wrap{{max-width:1080px;margin:0 auto;padding:40px 24px 80px}}
  h1{{font-size:26px;margin:0 0 4px}} h2{{font-size:20px;margin:38px 0 12px;padding-bottom:6px;border-bottom:1px solid var(--line)}}
  h3{{font-size:15px;margin:0 0 8px;color:var(--accent)}}
  .sub{{color:var(--muted);font-size:14px;margin:0 0 4px}}
  .pill{{display:inline-block;padding:2px 10px;border-radius:999px;font-size:13px;font-weight:600;
    background:rgba(88,166,255,.15);color:var(--accent);border:1px solid rgba(88,166,255,.4)}}
  .pill-ok{{display:inline-block;padding:1px 9px;border-radius:999px;font-size:12px;font-weight:600;
    background:rgba(63,185,80,.15);color:var(--ok);border:1px solid rgba(63,185,80,.4)}}
  .pill-bad{{display:inline-block;padding:1px 9px;border-radius:999px;font-size:12px;font-weight:600;
    background:rgba(248,81,73,.15);color:var(--bad);border:1px solid rgba(248,81,73,.4)}}
  table{{border-collapse:collapse;width:100%;margin:12px 0;font-size:14px}}
  th,td{{border:1px solid var(--line);padding:7px 9px;text-align:left;vertical-align:top}}
  th{{background:var(--panel2);color:var(--muted);font-weight:600}}
  code{{background:var(--code);color:var(--codeink);padding:1px 5px;border-radius:4px;font-size:13px;font-family:Consolas,monospace}}
  .tldr{{background:var(--panel);border:1px solid var(--line);border-left:3px solid var(--accent);border-radius:8px;padding:16px 18px;margin:18px 0}}
  .grid{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:12px 0}}
  .card{{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:14px 16px}}
  .thumb{{width:100%;border:1px solid var(--line);border-radius:6px;display:block;margin:8px 0}}
  .chips{{display:flex;flex-wrap:wrap;gap:5px;margin:6px 0}}
  .chip{{font-size:11px;padding:1px 7px;border-radius:5px;border:1px solid var(--line);font-family:Consolas,monospace}}
  .chip.ok{{color:var(--ok);border-color:rgba(63,185,80,.4)}}
  .chip.warn{{color:var(--warn);border-color:rgba(210,153,34,.4)}}
  .chip.bad{{color:var(--bad);border-color:rgba(248,81,73,.5)}}
  .tag{{font-size:11px;padding:1px 7px;border-radius:5px;border:1px solid var(--line);background:var(--panel2);color:var(--muted)}}
  .ok{{color:var(--ok)}}.warn{{color:var(--warn)}}.bad{{color:var(--bad)}}.mut{{color:var(--muted)}}
  .ba{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:10px 0}}
  .ba .lbl{{font-size:11px;text-transform:uppercase;letter-spacing:.5px;color:var(--muted);margin-bottom:4px}}
  .ba img{{width:100%;border-radius:6px;border:1px solid var(--line)}}
  details{{margin:6px 0}} summary{{cursor:pointer;color:var(--muted);font-size:13px}}
  ul{{margin:8px 0;padding-left:20px}} li{{margin:6px 0;font-size:13px}}
  a{{color:var(--accent)}}
  .foot{{margin-top:40px;padding-top:14px;border-top:1px solid var(--line);color:var(--muted);font-size:13px}}
  @media(max-width:820px){{.grid,.ba{{grid-template-columns:1fr}}}}
</style></head><body><div class="wrap">

  <h1>§1.1 Inverse Functions — VISUAL-FRAME gate1 視覺稽核</h1>
  <p class="sub">2026-06-17 · <span class="pill">Stage 2 工程稿視覺驗收</span> · 19 場景 1080p mock，17 內容幀逐幀稽核</p>
  <p class="sub">流程：<code>make.py --backend mock</code> 19 場景 1080p → <code>ffmpeg -sseof</code> 抽每場景最末（最滿）幀 →
     Workflow fan-out（17 幀 × <code>visual-frame-audit</code> agent，對照 <a href="VISUAL-FRAME-RUBRIC.md">VISUAL-FRAME-RUBRIC</a>
     V1–V8 blocking＋A1–A7 magnitude）→ 每個 blocking finding 派 3 個 refute-by-default skeptic 對抗式複驗（多數決）。</p>
  <p class="sub" style="font-size:12px">圖片均以 base64 內嵌（self-contained，換機 git clone 後仍可讀）。</p>

  <div class="tldr">
    <b>結論：</b>17 內容幀全審。<b>raw V-blocking {summ['raw_blockings']}</b>（三票複驗：confirmed {summ['confirmed_blockings']}、refuted {summ['refuted_blockings']}）。
    唯一 blocking＝<b>recap point 04 caveat 出框</b>（V1，3/3 票確認）{reg_pill}。其餘 16 場景 V1–V8 全 clean，A 分均值 80–90。
    使用者裁決後處理的 3 個 advisory：<b>align_on＝false positive（不改）</b>、<b>label 顏色＝已修（template）</b>、<b>y=x label 壓線＝已修（per-deck）</b>，皆回歸 confirmed（見 §②）。其餘 A 面 polish nit 留待專門 pass。
  </div>

  <h2>① Blocking（V1，已修 → 回歸）</h2>
  <p class="sub"><b>17 recap · V1 出框／裁切 · 3/3 skeptic 確認</b></p>
  <div class="ba">
    <div><div class="lbl bad">修改前（caveat 被切）</div><img src="{uri('17_recap/final_before.png')}"></div>
    <div><div class="lbl ok">修改後（重渲）</div><img src="{uri('17_recap/final.png')}"></div>
  </div>
  <ul>
    <li><b>證據：</b>左欄 point 04「Find it: solve $y=f(x)$ for $x$, then swap $x$ and $y$ (check one-to-one <b>first).</b>」最後一行被切在畫面底部安全邊界外，丟失旁白強調的「先驗一對一」caveat（say:「…after checking one-to-one…」）。</li>
    <li><b>為何 Blocking：</b>這是 recap 最末／最滿幀，所有 reveal 本應在場；關鍵教學資訊被裁出框＝V1 Blocking（非單純擁擠）。sizecheck 對 recap wrap 高度有已知盲區，故三閘未擋。</li>
    <li><b>修法（this-deck-only，與既有「recap 點縮短」慣例一致、不動共用模板）：</b>把兩個 3 行長點縮成 2 行騰出垂直空間——point.0「different inputs give different outputs (horizontal line test)」→「distinct inputs give distinct outputs」；point.2「The inverse swaps…its graph reflects」→「Inverse swaps…graph reflects」。<b>帶 caveat 的 point.3 逐字保留</b>。</li>
    <li><b>回歸：</b>{esc(reg["note"]) or "重渲 recap、重抽最末幀、視覺複驗 point 04「first).」是否完整落在安全邊界內（見右圖）。"}</li>
  </ul>

  <h2>② Advisory 處置（使用者裁決「先修 template bug」後）</h2>
  <p class="sub">gate1 的 A 面 advisory <b>未經三票對抗式複驗</b>（只有 V-blocking 走複驗）。逐項調查後處置如下——其中 align_on 經查為 <b>false positive</b>，印證「未複驗的 A 面 advisory 不可盡信」。</p>

  <div class="card" style="border-left:3px solid var(--ok);margin-bottom:14px">
    <h3 class="ok">①·a　derivation <code>align_on:"="</code> — 調查後＝FALSE POSITIVE（不改）</h3>
    <p>audit 對 scene 14／16 報「<code>align_on</code> 宣告了卻渲成置中、<code>=</code> 沒對成一欄」。實測推翻：</p>
    <ul>
      <li><b>幾何量測</b>（複現模板的實際 MathTex）：定位後每行 <code>=</code> 的 left-x 全等（+0.291），<code>arrange+center</code> 後仍全等（−0.593）＝完美一欄。</li>
      <li><b>放大裁切</b> scene 14 方程式區：5 行的第一個 <code>=</code> 確實對齊同一 x，各行左緣刻意錯開正是為了對齊 <code>=</code>。</li>
      <li><b>結論：</b>VLM 把模板刻意的「整塊置中」誤讀成「<code>=</code> 沒對齊」。模板正常，<b>不動</b>（改它反而會弄壞正常對齊）。</li>
    </ul>
  </div>

  <div class="card" style="border-left:3px solid var(--accent)">
    <h3 class="ok">①·b　graph_focus line label 顏色 ＋ ①·c　y=x label 壓線 — 已修＋回歸 confirmed</h3>
    <ul>
      <li><b>顏色（template 根因）：</b><code>graph_focus.py</code> 的 <code>line</code> label 預設 <code>role="warning"</code>（紅）——故 <code>color_role: muted</code> 的 y=x 線、未設 <code>label_role</code> 時 label 掉成紅色。改為<b>繼承該線的 <code>color_role</code></b>（與 function label 繼承曲線色一致）。blast radius 安全：唯二受影響的就是這兩條 y=x 線；demo 皆設顯式 <code>label_role</code>、不受影響。</li>
      <li><b>壓線（per-deck）：</b>y=x label 的 <code>label_point</code> 挪離虛線（11 順手把與 cyan 曲線相疊的 y=x³ label 一起清開）。</li>
      <li><b>回歸：</b>2 個獨立 <code>visual-frame-audit</code> agent 重判 scene 11／12＝<b>各 0 visual blocking</b>，兩修法 confirmed、無新碰撞。</li>
    </ul>
    <div class="ba">
      <div><div class="lbl bad">11 修前（紅 label·壓線）</div><img src="{uri('11_reflection_across_y_equals_x/final_before.png')}"></div>
      <div><div class="lbl ok">11 修後（muted·離線）</div><img src="{uri('11_reflection_across_y_equals_x/final.png')}"></div>
    </div>
    <div class="ba">
      <div><div class="lbl bad">12 修前（紅 label·壓線）</div><img src="{uri('12_repair_by_restricting/final_before.png')}"></div>
      <div><div class="lbl ok">12 修後（muted·離線）</div><img src="{uri('12_repair_by_restricting/final.png')}"></div>
    </div>
  </div>

  <h2>③ 每場景視覺計分卡（17 內容幀）</h2>
  <table><thead><tr><th>#</th><th>scene</th><th>template</th><th>V-blk</th><th>A 最低</th></tr></thead>
  <tbody>
{table}
  </tbody></table>

  <h2>④ 各場景幀＋findings</h2>
  <div class="grid">
{cardhtml}
  </div>

  <div class="foot">
    Workflow <code>wf_c6310a21-e22</code>（20 agents：17 audit ＋ 3 verify）· 抽幀 <code>.venv/ffmpeg_shim/ffmpeg.exe -sseof -0.4</code>（本機無 ffprobe，繞過 critic.py per=scene）·
    rubric <a href="VISUAL-FRAME-RUBRIC.md">VISUAL-FRAME-RUBRIC.md</a> · 收斂判準＝視覺 blocking==0 · 唯讀稽核、propose-not-act、四級分流不 over-report。
    <br>產生器：<code>_gen/REVIEW-ch01_inverse_functions-visualframe.gen.py</code>（圖 base64 內嵌、self-contained）。
  </div>

</div></body></html>'''
    OUT.write_text(doc, encoding="utf-8")
    size_mb = len(doc.encode("utf-8")) / 1e6
    print("wrote", OUT)
    print(f"scenes: {len(scenes)} | raw blockings: {summ['raw_blockings']} | confirmed: {summ['confirmed_blockings']}")
    print(f"embedded frames: {len(_URI_CACHE)} | HTML size: {size_mb:.2f} MB | missing: {_MISSING or 'none'}")


if __name__ == "__main__":
    main()
