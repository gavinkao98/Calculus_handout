"""Generator: §1.1 custom-animation SIGN-OFF report -> SELF-CONTAINED standalone HTML.

Presents the five §1.1 `# HOOK(第二輪)` custom animations (generated code, treated
like narration per CONTENT_METHODOLOGY §5) to the user for sign-off, after a fresh
1080p mock re-render + an independent adversarial visual audit of the rendered
animation frames.

PORTABILITY CONTRACT (video/README.md §資料夾架構與版控策略):
  Every frame is embedded as a base64 data URI — the HTML carries its own images,
  so it renders after a fresh `git clone` even though output/ is gitignored. No
  external image refs.

Frame sources (regenerable; re-create by re-rendering §1.1 then re-running the
ffmpeg extraction below):
  output/ch01/s1.1/_signoff_frames/
    sheet_<scene>.png            4s contact sheet (ffmpeg fps=1/4,tile=4x5)
    h{1..5}_a_*.png / *_b_end.png  before / end key stills (ffmpeg -ss)

Re-create frames after a fresh `make.py --backend mock` §1.1 render:
  for s in <5 hook scenes>: ffmpeg -ss <t> -i output/_av/<s>.mp4 -frames:v 1 <out>.png
  (timestamps in EXTRACT below; contact sheets via fps=1/4,scale=380:-1,tile=4x5)

The generator + its AUDIT digest live in a tracked location so the report can be
regenerated after the gitignored output/ is wiped.
"""
from __future__ import annotations
import base64
import html
import io
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent           # .../video/content_scripts/_audit/_gen
REPO = HERE.parents[3]                            # repo root
OUT = HERE.parent / "REVIEW-ch01_inverse_functions-animation-signoff.html"
FRAMES = REPO / "video" / "output" / "ch01" / "s1.1" / "_signoff_frames"
FILM = "output/ch01/s1.1/ch01_inverse_functions.mp4"
MAX_W = 1100

# ---- the five hooks (static content) ---------------------------------------
HOOKS = [
    {
        "key": "can_we_run_it_backwards", "nn": "01", "tmpl": "definition_math",
        "kicker": "motivation", "title": "Running a Function Backwards",
        "cue": ("兩進一出映射。<b>左</b> $f(x)=x$ on $[0,1]$：輸入 $0,\\tfrac12,\\tfrac18$ "
                "各以<span class='cy'>青箭頭</span>連到自己（$0\\to0$、$\\tfrac12\\to\\tfrac12$、"
                "$\\tfrac18\\to\\tfrac18$），乾淨一對一、箭頭逐一長出。<b>右</b> $g(x)=x^2$ on $[-1,1]$："
                "$\\tfrac12$ 與 $-\\tfrac12$ 兩條<span class='go'>金箭頭</span>匯到<b>唯一</b>的 $\\tfrac14$，"
                "第二箭頭落定瞬間 $\\tfrac14$ 紅色 <code>Indicate</code> 脈動一下（兩進一出＝回不去）。"),
        "say": ("…two quick examples show the difference. {show math.0} Take $f(x)=x$… every "
                "output traces back to exactly one input… {show math.1} Now take $f(x)=x^2$… a "
                "half squares to a quarter, but so does negative a half… That collision is the "
                "whole obstacle — when one output can be traced to two inputs, there is no honest "
                "way back."),
        "frames": [("左欄映射建立", "h1_a_left.png"), ("端態：兩欄並存", "h1_b_end.png")],
        "sheet": "sheet_can_we_run_it_backwards.png",
    },
    {
        "key": "horizontal_line_test", "nn": "06", "tmpl": "graph_compare",
        "kicker": "example", "title": "The Horizontal Line Test",
        "cue": ("水平虛線自上而下<b>掃入</b>兩格。<b>左</b>（$y=x$ 直線）：虛線恰交<b>一點</b>，交點以"
                "<span class='ok'>綠 Flash</span> 彈現、caption 配綠 ✓。<b>右</b>（$y=x^2$ 拋物線）："
                "虛線切過<b>兩點</b>、各以<span class='bad'>紅 Flash</span> 彈現、caption 配紅 ✗。"
                "底部 annotation：one-to-one $\\iff$ 沒有水平線交圖超過一次。"),
        "say": ("…a horizontal line $y=c$ meets the graph wherever $f(x)=c$… {show left.plot.1} A "
                "straight line like $y=x$ passes — {show left.plot.2} every horizontal line meets "
                "it just once. {show right.plot.1} A parabola fails — a horizontal line slices clean "
                "through both arms, {show right.plot.2}{show right.plot.3} and those two crossings "
                "are exactly the pair of inputs sharing an output."),
        "frames": [("左格：水平線＋一交點", "h2_a_leftline.png"), ("端態：兩格＋判定", "h2_b_end.png")],
        "sheet": "sheet_horizontal_line_test.png",
    },
    {
        "key": "composition_identities", "nn": "10", "tmpl": "definition_math",
        "kicker": "proposition", "title": "Composition Identities",
        "cue": ("$A\\leftrightarrow B$ 雙泡泡。<span class='cy'>青點</span> $x$ 由 $A$ 沿 $f$"
                "（<span class='cy'>上青弧</span>）到 $B$ 的 $f(x)$，再沿 $f^{-1}$"
                "（<span class='go'>下金弧</span>）回到<b>同一個</b> $x$，落點 Flash（往返回家）；"
                "第一恆等式 $f^{-1}(f(x))=x$ 浮現。第二趟由 $B$ 的 $y$ 沿 $f^{-1}$ 到 $A$、再沿 $f$ 回 $B$，"
                "第二恆等式 $f(f^{-1}(y))=y$ 浮現。"),
        "say": ("{show math.0} …applying $f$ and then $f$ inverse returns the original input… "
                "{show math.1} Going the other way works too… Picture an input $x$ in $A$; $f$ "
                "carries it across to its output in $B$, and $f$ inverse carries that output right "
                "back to the same $x$ — a round trip that lands home."),
        "frames": [("雙泡泡＋f／f⁻¹ 弧", "h3_a_diagram.png"), ("端態：兩恆等式", "h3_b_end.png")],
        "sheet": "sheet_composition_identities.png",
    },
    {
        "key": "reflection_across_y_equals_x", "nn": "11", "tmpl": "graph_focus",
        "kicker": "example", "title": "Reflection across $y=x$",
        "cue": ("$y=x^3$（<span class='cy'>青</span>）的 ghost 沿虛線 $y=x$ <b>翻摺</b>、精準落到立方根曲線上；"
                "較亮的 $y=\\sqrt[3]{x}$（<span class='go'>橙</span>）隨後淡入。鏡射點對 $(a,b)$／$(b,a)$ "
                "對稱於 $y=x$ 各 Flash 一下。<b>數學保真：</b>橙曲線確為青 $x^3$ 對 $y=x$ 的真鏡射（立方根＝立方的反函數）。"),
        "say": ("…the two graphs are mirror images across the line $y=x$. {show plot.2} a point "
                "$(a,b)$ sits on the graph of $f$ exactly when $(b,a)$ sits on the inverse, "
                "{show plot.3}{show plot.4} reflecting across $y=x$ trades a point's two "
                "coordinates… fold the graph of $x^3$ over $y=x$ and it lands right on the cube root."),
        "frames": [("翻摺前：僅 $x^3$", "h4_a_x3only.png"), ("端態：$x^3$／$\\sqrt[3]{x}$ 鏡射＋點對", "h4_b_end.png")],
        "sheet": "sheet_reflection_across_y_equals_x.png",
    },
    {
        "key": "repair_by_restricting", "nn": "12", "tmpl": "graph_focus",
        "kicker": "example", "title": "Restrict, then Invert",
        "cue": ("軸只顯示非負定義域（$x$ 自 $\\approx-0.4$ 起）。保留的 $f(x)=x^2$ 右臂"
                "（$x\\ge0$，<span class='cy'>青</span>）沿虛線 $y=x$ <b>鏡射</b>生成 "
                "$f^{-1}(x)=\\sqrt{x}$（<span class='go'>橙</span>）、淡入。<b>數學保真：</b>橙 $\\sqrt{x}$ "
                "確為青 $x^2$ 右臂對 $y=x$ 的真鏡射。<span class='mut'>（「丟棄左臂」手勢因左臂幾乎全出框而刻意省略，限定交由旁白承載。）</span>"),
        "say": ("…chop its domain down to the nonnegative numbers… it becomes one-to-one… "
                "{show plot.2} Now we can invert it — solving gives $f^{-1}(x)=\\sqrt{x}$… "
                "Restrict first, then invert — and that exact move is the key that unlocks the "
                "inverse trigonometric functions coming up."),
        "frames": [("鏡射前：僅 $x^2$ 右臂", "h5_a_x2only.png"), ("端態：$x^2$／$\\sqrt{x}$ 鏡射", "h5_b_end.png")],
        "sheet": "sheet_repair_by_restricting.png",
    },
]

# ---- AUDIT: filled from Workflow wf_d0d69df6-e46 (5 visual-frame-audit + verify) ----
# key -> {faithful: bool, blocking: int (confirmed), aesthetic: int, notes: str}
AUDIT: dict[str, dict] = {
    "can_we_run_it_backwards": {
        "faithful": True, "blocking": 0, "aesthetic": 88,
        "notes": ("稽核：映射對（½／−½ 同入 ¼）、reveal 順序對（左欄先、右欄後，無提前洩漏碰撞）、"
                  "青／金配色對。紅色 Indicate 為 0.6s transient，靜態幀不收、依 rubric 不扣忠實。"),
    },
    "horizontal_line_test": {
        "faithful": True, "blocking": 0, "aesthetic": 88,
        "notes": ("稽核：幾何對（左 1 交點／右 2 交點對稱於 y 軸）、$\\iff$ annotation 完整、verdict ✓／✗ 正確。"
                  "綠／紅交點 Flash 為 transient；A4 小註——兩格交點同為琥珀色，綠紅之分靠 caption ✓／✗ 標記（advisory，判定仍明確）。"),
    },
    "composition_identities": {
        "faithful": True, "blocking": 0, "aesthetic": 91,
        "notes": ("稽核：A／B 泡泡＋f（上青弧）／f⁻¹（下金弧）＋x、f(x) 點＋兩恆等式全對；"
                  "contact sheet 證 tracer 往返（青出金回）。本輪 aesthetic 最高（91）。"),
    },
    "reflection_across_y_equals_x": {
        "faithful": True, "blocking": 0, "aesthetic": 86,
        "notes": ("稽核：橙 $\\sqrt[3]{x}$ 確為青 $x^3$ 對 $y=x$ 的真鏡射、鏡射點對稱、function 標籤同色慣例、$y=x$ 標籤 muted。"
                  "翻摺為 transition 動態、靜態幀呈現端態。"),
    },
    "repair_by_restricting": {
        "faithful": True, "blocking": 0, "aesthetic": 87,
        "notes": ("稽核抓到 1 個 <b>A1 advisory（已修）</b>：橙標籤 $f^{-1}(x)=\\sqrt{x}$ 原 <code>label_point [2.0,1.4]</code> "
                  "幾乎落在自己曲線上（$\\sqrt2\\approx1.41$），曲線描邊穿過 $f^{-1}(x)=$ 前綴、降低該段可讀性"
                  "（複驗 refute 掉 blocking 等級——屬 crowding 非 info-loss，$\\sqrt{x}$ 段仍清晰）。"
                  "<b>已修：</b><code>label_point → [2.1,1.78]</code> 挪離曲線、進入橙曲線與 $y=x$ 虛線間的乾淨間隙，重渲複驗。"),
    },
}

SUMMARY = {
    "raw_blocking": 1, "confirmed_blocking": 0, "refuted": 1,
    "verdict": "視覺 blocking == 0 · choreography 忠實 5/5 · 1 advisory 已修",
}

_URI: dict[str, str] = {}
_MISSING: list[str] = []


def uri(name: str) -> str:
    if name in _URI:
        return _URI[name]
    p = FRAMES / name
    if not p.exists():
        _MISSING.append(name)
        ph = ("<svg xmlns='http://www.w3.org/2000/svg' width='640' height='360'>"
              "<rect width='100%' height='100%' fill='#1d2630'/>"
              "<text x='50%' y='50%' fill='#9aa7b4' font-family='sans-serif' font-size='18' "
              "text-anchor='middle'>frame missing — re-render §1.1 + re-extract</text></svg>")
        _URI[name] = "data:image/svg+xml;base64," + base64.b64encode(ph.encode()).decode()
        return _URI[name]
    im = Image.open(p).convert("RGB")
    if im.width > MAX_W:
        im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format="PNG", optimize=True)
    _URI[name] = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
    return _URI[name]


def esc(s):
    return html.escape(str(s), quote=False)


def ac(v):
    v = int(v)
    return "ok" if v >= 85 else ("warn" if v >= 72 else "bad")


def main():
    cards = []
    for h in HOOKS:
        a = AUDIT.get(h["key"], {})
        faithful = a.get("faithful")
        blocking = a.get("blocking", 0)
        aest = a.get("aesthetic")
        fa_pill = ('<span class="pill-ok">choreography 忠實 ✓</span>' if faithful
                   else '<span class="pill-bad">choreography 不符</span>' if faithful is False
                   else '<span class="tag">待稽核</span>')
        vb_pill = ('<span class="pill-ok">V clean</span>' if blocking == 0
                   else f'<span class="pill-bad">V-BLOCKING ×{blocking}</span>')
        aest_chip = (f'<span class="chip {ac(aest)}">aesthetic {aest}</span>' if aest is not None else "")
        ba = "".join(
            f'<div><div class="lbl">{esc(lbl)}</div><img src="{uri(fn)}"></div>'
            for (lbl, fn) in h["frames"])
        notes = a.get("notes", "")
        notes_html = f'<p class="mut" style="font-size:13px;margin:8px 0 0">{esc(notes)}</p>' if notes else ""
        cards.append(f'''
  <div class="card">
    <h3>{esc(h["nn"])} · {esc(h["key"])} <span class="tag">{esc(h["tmpl"])}</span>
        <span class="tag">{esc(h["kicker"])}</span> {fa_pill} {vb_pill} {aest_chip}</h3>
    <p class="cuelbl">動畫 cue</p><p class="cue">{h["cue"]}</p>
    <div class="ba2">{ba}</div>
    <details><summary>認可旁白逐字（節錄，動畫與此對齊）</summary>
      <p class="say">{h["say"]}</p></details>
    <details><summary>動態 contact sheet（每 4s 一格，時間 →／↓）</summary>
      <img class="thumb" src="{uri(h["sheet"])}"></details>
    {notes_html}
  </div>''')

    cardhtml = "\n".join(cards)
    s = SUMMARY
    if s["confirmed_blocking"] == 0:
        tldr_pill = '<span class="pill-ok">視覺 blocking == 0 · 動畫忠實全 ✓</span>'
    elif s["confirmed_blocking"] is None:
        tldr_pill = '<span class="tag">待稽核</span>'
    else:
        tldr_pill = f'<span class="pill-bad">confirmed blocking {s["confirmed_blocking"]}</span>'

    doc = f'''<!DOCTYPE html>
<html lang="zh-Hant"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>§1.1 客製動畫 sign-off 報告</title>
<script>
window.MathJax={{tex:{{inlineMath:[['$','$'],['\\\\(','\\\\)']]}},svg:{{fontCache:'global'}}}};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js" id="MathJax-script" async></script>
<style>
  :root{{--bg:#0f1419;--panel:#171e26;--panel2:#1d2630;--ink:#e6edf3;--muted:#9aa7b4;
    --line:#2a3742;--ok:#3fb950;--warn:#d29922;--accent:#58a6ff;--bad:#f85149;
    --cy:#4cc9f0;--go:#f0a93a;--code:#0b1118;--codeink:#c9d4df;}}
  *{{box-sizing:border-box}}
  body{{margin:0;background:var(--bg);color:var(--ink);
    font:16px/1.65 -apple-system,"Segoe UI",Roboto,"Noto Sans CJK TC","Microsoft JhengHei",sans-serif;}}
  .wrap{{max-width:1000px;margin:0 auto;padding:40px 24px 80px}}
  h1{{font-size:26px;margin:0 0 4px}} h2{{font-size:20px;margin:38px 0 12px;padding-bottom:6px;border-bottom:1px solid var(--line)}}
  h3{{font-size:15px;margin:0 0 10px;color:var(--accent);line-height:1.9}}
  .sub{{color:var(--muted);font-size:14px;margin:0 0 4px}}
  .pill{{display:inline-block;padding:2px 10px;border-radius:999px;font-size:13px;font-weight:600;
    background:rgba(88,166,255,.15);color:var(--accent);border:1px solid rgba(88,166,255,.4)}}
  .pill-ok{{display:inline-block;padding:1px 9px;border-radius:999px;font-size:12px;font-weight:600;
    background:rgba(63,185,80,.15);color:var(--ok);border:1px solid rgba(63,185,80,.4)}}
  .pill-bad{{display:inline-block;padding:1px 9px;border-radius:999px;font-size:12px;font-weight:600;
    background:rgba(248,81,73,.15);color:var(--bad);border:1px solid rgba(248,81,73,.4)}}
  code{{background:var(--code);color:var(--codeink);padding:1px 5px;border-radius:4px;font-size:13px;font-family:Consolas,monospace}}
  .tldr{{background:var(--panel);border:1px solid var(--line);border-left:3px solid var(--accent);border-radius:8px;padding:16px 18px;margin:18px 0}}
  .card{{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:16px 18px;margin:16px 0}}
  .cuelbl{{font-size:11px;text-transform:uppercase;letter-spacing:.5px;color:var(--muted);margin:4px 0 2px}}
  .cue{{font-size:14px;margin:0 0 12px}}
  .say{{font-size:13px;color:var(--muted);font-style:italic;background:var(--panel2);border-radius:6px;padding:10px 12px;margin:6px 0}}
  .ba2{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:10px 0}}
  .ba2 .lbl{{font-size:11px;color:var(--muted);margin-bottom:4px}}
  .ba2 img{{width:100%;border-radius:6px;border:1px solid var(--line);display:block}}
  .thumb{{width:100%;border:1px solid var(--line);border-radius:6px;display:block;margin:8px 0}}
  .chip{{font-size:11px;padding:1px 7px;border-radius:5px;border:1px solid var(--line);font-family:Consolas,monospace}}
  .chip.ok{{color:var(--ok);border-color:rgba(63,185,80,.4)}}
  .chip.warn{{color:var(--warn);border-color:rgba(210,153,34,.4)}}
  .chip.bad{{color:var(--bad);border-color:rgba(248,81,73,.5)}}
  .tag{{font-size:11px;padding:1px 7px;border-radius:5px;border:1px solid var(--line);background:var(--panel2);color:var(--muted)}}
  .ok{{color:var(--ok)}}.warn{{color:var(--warn)}}.bad{{color:var(--bad)}}.mut{{color:var(--muted)}}
  .cy{{color:var(--cy)}}.go{{color:var(--go)}}
  details{{margin:8px 0}} summary{{cursor:pointer;color:var(--muted);font-size:13px}}
  a{{color:var(--accent)}}
  .foot{{margin-top:40px;padding-top:14px;border-top:1px solid var(--line);color:var(--muted);font-size:13px}}
  @media(max-width:760px){{.ba2{{grid-template-columns:1fr}}}}
</style></head><body><div class="wrap">

  <h1>§1.1 Inverse Functions — 客製動畫 sign-off</h1>
  <p class="sub">2026-06-17 · <span class="pill">5 個 <code># HOOK(第二輪)</code> 客製動畫</span> · 重新渲染後待你過目認可</p>
  <p class="sub">生成動畫 code 視同 narration（<code>CONTENT_METHODOLOGY §5</code>）——render 結果經你認可才算定版。</p>
  <p class="sub" style="font-size:12px">圖片全 base64 內嵌（self-contained，換機 git clone 後仍可讀）。</p>

  <div class="tldr">
    <b>本輪：</b>本機產物過時 → <code>make.py --backend mock --quality high</code> 重渲 19 場景 1080p（三閘全過、19/19 成功、compose 成片）{tldr_pill}<br>
    <b>合併成片：</b><code>{FILM}</code>（~12:53、1080p h264＋aac、含 5 客製動畫＋全部視覺修正＋場景淡入淡出過場）。<br>
    <b>獨立稽核：</b>5 個 <code>visual-frame-audit</code> agent 對<b>實際 render 的動畫幀</b>各自對照 cue＋
    <a href="VISUAL-FRAME-RUBRIC.md">VISUAL-FRAME-RUBRIC</a>（V1–V8 blocking＋A1–A7），blocking 派 refute-by-default 複驗。
    <b>結果：raw blocking {s['raw_blocking']} → confirmed {s['confirmed_blocking']}</b>（refuted {s['refuted']}）；choreography 忠實 5/5。
  </div>

  <h2>① 怎麼審</h2>
  <p class="sub">最完整的審法是<b>直接看合併成片</b>裡的 5 段動畫（靜態幀看不到 flash／往返／翻摺的動態）：</p>
  <p class="sub">▸ 開 <code>{FILM}</code>，5 段動畫落在這些場景：
     <code>01 motivation</code>、<code>06 HLT</code>、<code>10 composition</code>、<code>11 reflection</code>、<code>12 restrict</code>。</p>
  <p class="sub">下面每張卡片給：動畫 cue（要演什麼）＋關鍵幀（before→端態）＋認可旁白逐字＋獨立稽核結果。靜態幀已足以判斷數學保真與端態正確；動態節奏請以成片為準。</p>

  <h2>② 五個動畫</h2>
{cardhtml}

  <div class="foot">
    重渲：<code>make.py --storyboard storyboards/ch01_inverse_functions.yml --backend mock --quality high</code>（19/19，exit 0）·
    稽核 Workflow <code>wf_d0d69df6-e46</code>（5 visual-frame-audit ＋ verify）· 抽幀 <code>ffmpeg -ss</code> 自 <code>output/_av/&lt;scene&gt;.mp4</code> ·
    收斂判準＝視覺 blocking==0 ＋ choreography 忠實。<br>
    產生器：<code>_gen/REVIEW-ch01_inverse_functions-animation-signoff.gen.py</code>（圖 base64 內嵌、self-contained）。
    動畫 code：<code>animations/ch01_inverse_functions_hooks.py</code>（工程閘 E1/E2 已收斂，blocking==0）。
  </div>

</div></body></html>'''
    OUT.write_text(doc, encoding="utf-8")
    size_mb = len(doc.encode("utf-8")) / 1e6
    print("wrote", OUT)
    print(f"hooks: {len(HOOKS)} | embedded frames: {len(_URI)} | HTML: {size_mb:.2f} MB | missing: {_MISSING or 'none'}")


if __name__ == "__main__":
    main()
