#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the §1.2 animation sign-off HTML report (self-contained, base64 frames).

Per hook: the animation cue (intended motion), before -> end-state frames, the
approved spoken narration, and the gate verdicts (VISUAL-FRAME + HOOK-ENGINEERING,
both 0 blocking this round). Mirrors §1.1's REVIEW-…-animation-signoff.html so the
user can do the animation sign-off gate (生成 code 視同 narration, CONTENT_METHODOLOGY §5).

Frames read from gitignored output/.../critic/frames/_signoff/<id>_{before,end}.png
(re-extractable: re-render the hooked scenes + ffmpeg -ss/-sseof). Run with .venv
python (needs Pillow). Output: _audit/REVIEW-ch01_inverse_trig_functions-animation-signoff.html
"""
import base64, io
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
FRAMES = AUDIT.parent.parent / "output" / "ch01" / "s1.2" / "critic" / "frames" / "_signoff"
OUT = AUDIT / "REVIEW-ch01_inverse_trig_functions-animation-signoff.html"

# Per-hook: (scene id, display title, cue [intended motion], spoken narration excerpt,
#            visual verdict, engineering verdict)
HOOKS = [
    ("sine_is_not_one_to_one", "Sine is not one-to-one — sweep line",
     "一條水平虛線從畫面上方滑入、停在 y = 1/2，沿 sine 波閃示它命中的多個同高交點"
     "（往兩側無窮多個），凸顯「同一個輸出 → 無窮多個角度」。",
     "Slide a horizontal line across the graph of y equals sine x: at almost every "
     "height it crosses not once but over and over… a single value of sine comes from "
     "infinitely many angles.",
     "V 0 blocking（A 88–92）；4 交點皆為真 sin = 0.5 解、落位準。",
     "clean — plot.1（line）`_slide_line_down`、plot.2–5（points）`_pop_crossing`，bare-Line/Dot 結構假設正確。"),
    ("restrict_sine_branch", "Keep the middle branch — isolate + sweep",
     "把 [-π/2, π/2] 以外的 sine 淡化，中央分支高亮（橙、加粗）Create 點亮；"
     "一個點沿分支從 (-π/2,-1) 滑到 (π/2,1)，凸顯單調掃過 [-1,1]。",
     "Keep only the middle piece… On that one interval sine climbs steadily from "
     "negative one up to one, never repeating a value.",
     "V 0 blocking（A1 86；分支 label 已移離曲線）。",
     "clean — plot.1 Create + Dot `MoveAlongPath`（sin 無 y_clip = 單段曲線，路徑合法）。"),
    ("evaluating_arcsin", "Reference triangle — Pythagoras fills the adjacent",
     "由 sin θ = 1/3 逐步建構直角三角形：對邊 1、斜邊 3、角 θ 先給，鄰邊 2√2 由 "
     "Pythagoras「填入」（Create 畫出 + Flash 強調是算出來的）。",
     "Set theta equals arcsine of one third… Draw a right triangle with opposite "
     "side one and hypotenuse three; the adjacent side is the square root of nine "
     "minus one, which is two root two.",
     "V 0 blocking（三角形已抬離 x 軸、鄰邊讀為一邊；構圖略右偏 advisory）。",
     "clean — plot.2（adjacent）Create + Flash，line-reveal 的 mob[0] = line 正確。"),
    ("principal_value_trap", "Bobbing particle — one principal value",
     "小球沿 h = cos t 上下 bob（MoveAlongPath）；高度反覆達 1，真正達 1 的時刻 "
     "t = 2πn（橙點）Flash；arccos(1) = 0 單獨標在 t = 0（紅點、粒子尚未啟動）。",
     "A particle… bobs up and down, its height equal to cosine t… arccosine returns "
     "only its one principal value, t equals zero… reaches height one at the times "
     "t equals two pi n.",
     "V 0 blocking（label 重疊已修：4 label 兩兩分離、紅/橙點清楚對比）。",
     "clean — plot.0 Create + ball `MoveAlongPath`（cos 無 y_clip = 單段），plot.2 `_pop_crossing`。"),
    ("restrict_tangent_branch", "Tangent climbs −∞ → +∞",
     "tangent 分支以 Create 由左下（趨 -∞）畫到右上（趨 +∞）＝攀升本身；夾在兩條 "
     "垂直漸近線 x = ±π/2 之間，凸顯「每個實數取一次 → arctan 接受全體 ℝ」。",
     "On the open interval from negative pi over two to pi over two, tangent climbs "
     "without bound… it passes through every real number, and through each one "
     "exactly once.",
     "V 0 blocking（V4 漸近線 label `±π/2` 已修：去 `\\tfrac` 疊層＋放大＋移 outer band）。",
     "clean — plot.2 `Create`（tan 經 y_clip = 多段 VGroup，正確避開 `MoveAlongPath` 陷阱）。"),
]


def b64(path: Path, max_w: int = 1100) -> str:
    if not path.exists():
        return ""
    im = Image.open(path).convert("RGB")
    if im.width > max_w:
        im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format="PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def img(path: Path, alt: str) -> str:
    d = b64(path)
    if not d:
        return ('<div class="ph">（幀缺；重渲 hook 場景＋ffmpeg -ss/-sseof 重生）<br>%s</div>'
                % alt)
    return '<img src="%s" alt="%s">' % (d, alt)


def build():
    cards = []
    for i, (sid, title, cue, narr, vv, ev) in enumerate(HOOKS, 1):
        before = img(FRAMES / f"{sid}_before.png", f"{sid} before")
        end = img(FRAMES / f"{sid}_end.png", f"{sid} end-state")
        cards.append(f"""
  <section class="hook">
    <div class="hh"><span class="hn">HOOK {i}</span><h3>{title}</h3><code class="sid">{sid}</code></div>
    <p class="cue"><b>動畫 cue（教學意圖）.</b> {cue}</p>
    <div class="frames">
      <figure>{before}<figcaption>before（動畫前的靜態底）</figcaption></figure>
      <figure>{end}<figcaption>end-state（動畫完成的最末幀）</figcaption></figure>
    </div>
    <p class="narr"><b>認可旁白（口語版）.</b> <i>{narr}</i></p>
    <div class="verdicts">
      <div class="v vv"><b>視覺稽核（VISUAL-FRAME gate1）</b><br>{vv}</div>
      <div class="v ev"><b>工程稽核（HOOK-ENGINEERING gate1）</b><br>{ev}</div>
    </div>
  </section>""")
    body = "\n".join(cards)
    html = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>§1.2 Inverse Trig — 動畫 sign-off 報告</title>
<style>
  :root{{--bg:#0f1419;--panel:#171e26;--panel2:#1d2630;--ink:#e6edf3;--muted:#9aa7b4;
    --line:#2a3742;--ok:#3fb950;--warn:#d29922;--accent:#58a6ff;--code:#0b1118;--codeink:#c9d4df;}}
  *{{box-sizing:border-box}}
  body{{margin:0;background:var(--bg);color:var(--ink);
    font:16px/1.65 -apple-system,"Segoe UI",Roboto,"Noto Sans CJK TC","Microsoft JhengHei",sans-serif;}}
  .wrap{{max-width:1040px;margin:0 auto;padding:40px 24px 80px}}
  h1{{font-size:25px;margin:0 0 4px}} h3{{font-size:17px;margin:0;color:var(--ink)}}
  .sub{{color:var(--muted);font-size:14px;margin:0 0 4px}}
  .pill{{display:inline-block;padding:2px 10px;border-radius:999px;font-size:13px;font-weight:600;
    background:rgba(63,185,80,.15);color:var(--ok);border:1px solid rgba(63,185,80,.4)}}
  .pill.warn{{background:rgba(210,153,34,.15);color:var(--warn);border-color:rgba(210,153,34,.4)}}
  .tldr{{background:var(--panel);border:1px solid var(--line);border-left:3px solid var(--ok);
    border-radius:8px;padding:16px 18px;margin:18px 0}}
  .hook{{background:var(--panel);border:1px solid var(--line);border-radius:11px;padding:18px 20px;margin:20px 0}}
  .hh{{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:8px}}
  .hn{{font-size:12px;font-weight:700;letter-spacing:.5px;color:#fff;background:var(--accent);
    padding:2px 9px;border-radius:6px}}
  .sid{{font-family:"Cascadia Code",Consolas,monospace;font-size:12.5px;color:var(--muted);
    background:var(--code);padding:1px 6px;border-radius:4px;margin-left:auto}}
  .cue{{font-size:14.5px;color:var(--ink);margin:8px 0}}
  .cue b,.narr b{{color:var(--accent)}}
  .frames{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:12px 0}}
  .frames img{{width:100%;border:1px solid var(--line);border-radius:7px;display:block}}
  .frames figcaption{{color:var(--muted);font-size:12.5px;margin-top:5px;text-align:center}}
  .ph{{background:var(--panel2);border:1px dashed var(--line);border-radius:7px;padding:40px 12px;
    color:var(--muted);text-align:center;font-size:13px}}
  .narr{{font-size:14px;color:var(--muted);margin:10px 0}} .narr i{{color:var(--ink)}}
  .verdicts{{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:10px}}
  .v{{background:var(--panel2);border:1px solid var(--line);border-radius:8px;padding:10px 13px;font-size:13px}}
  .v.vv{{border-left:3px solid var(--ok)}} .v.ev{{border-left:3px solid var(--ok)}}
  .v b{{color:var(--ink)}} code{{font-family:"Cascadia Code",Consolas,monospace;font-size:.92em}}
  .foot{{margin-top:40px;padding-top:14px;border-top:1px solid var(--line);color:var(--muted);font-size:13px}}
  a{{color:var(--accent)}}
  @media(max-width:720px){{.frames,.verdicts{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
<div class="wrap">
  <h1>§1.2 Inverse Trigonometric Functions — 動畫 sign-off 報告</h1>
  <p class="sub">2026-06-18 · deck <code>ch01_inverse_trig_functions</code> · 5 客製動畫 hook · <span class="pill">視覺 0 blocking</span> <span class="pill">工程 0 blocking</span> <span class="pill warn">待動畫 sign-off</span></p>
  <p class="sub">生成動畫 code 視同 narration（CONTENT_METHODOLOGY §5），經你過目認可才定版。動畫源：<code>animations/ch01_inverse_trig_functions_hooks.py</code>。</p>
  <div class="tldr">
    <b>TL;DR.</b> §1.2 的 5 個 <code># HOOK</code> 客製動畫已接入＋render 無誤。每個 hook 下方列：<b>動畫 cue（教學意圖）</b>、<b>before → end-state 幀</b>、<b>認可旁白</b>、以及兩道 gate1 稽核裁決（<b>VISUAL-FRAME 視覺 0 blocking</b>、<b>HOOK-ENGINEERING 工程 0 blocking</b>，皆對抗式複驗）。
    <b>動畫的「動態」本身請看 mock 成片</b> <code>output/ch01/s1.2/ch01_inverse_trig_functions.mp4</code>（靜態幀只示端態構圖）；本報告供逐 hook 對照 cue＋裁決做 sign-off。<b>未動任何計費 API。</b>
  </div>
{body}
  <p class="foot">本報告由 <code>_audit/_gen/REVIEW-ch01_inverse_trig_functions-animation-signoff.gen.py</code> 生成（幀 base64 內嵌、self-contained、雙擊即開）。幀讀自 gitignored <code>output/…/critic/frames/_signoff/</code>（重渲 hook 場景＋<code>ffmpeg -ss/-sseof</code> 可重生）。裁決內嵌於產生器。</p>
</div>
</body>
</html>
"""
    OUT.write_text(html, encoding="utf-8")
    print("wrote", OUT)


if __name__ == "__main__":
    build()
