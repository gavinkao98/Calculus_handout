"""Generator: §1.1 custom-animation (hook) sign-off report -> SELF-CONTAINED HTML.

Reads the sibling .digest.json (the 5 hooks' cue/anim/engineering metadata) and
emits a dark-themed, MathJax standalone report into video/content_scripts/_audit/.

PORTABILITY CONTRACT (see video/README.md §資料夾架構與版控策略):
  Every frame is embedded as a base64 data URI — the HTML carries its own
  images and renders on any machine after a fresh `git clone`, even though the
  render output under output/ is gitignored. NO external image refs.

Frame sources:
  - <nn>_<scene>/final.png : regenerable; read from the live render at
                             video/output/ch01/s1.1/critic/frames/ (re-run §1.1
                             mock to regenerate).
  - _mid_*.png             : animation mid-frames grabbed at scene-specific
                             timestamps (effectively irreproducible without the
                             exact ffmpeg recipe) -> preserved (tracked) under
                             ./frames_mid/.

This generator + its .digest.json + ./frames_mid/ live in a tracked location so
the report can be regenerated after the gitignored output/ is wiped.
"""
from __future__ import annotations
import base64
import html
import io
import json
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent               # .../video/content_scripts/_audit/_gen
REPO = HERE.parents[3]                                # repo root
DIGEST = HERE / "REVIEW-ch01_inverse_functions-hooks.digest.json"
OUT = HERE.parent / "REVIEW-ch01_inverse_functions-hooks.html"
FRAMES_LIVE = REPO / "video" / "output" / "ch01" / "s1.1" / "critic" / "frames"
FRAMES_MID = HERE / "frames_mid"
MAX_W = 1100

_URI_CACHE: dict[str, str] = {}
_MISSING: list[str] = []


def _resolve(rel: str) -> Path:
    """Map a frame subpath to a real file: _mid_*.png is tracked here, the rest
    are the live (regenerable) render frames."""
    name = rel.rsplit("/", 1)[-1]
    if name.startswith("_mid_"):
        return FRAMES_MID / name
    return FRAMES_LIVE / rel


def uri(rel: str) -> str:
    """base64 data URI for a frame subpath, downscaled to MAX_W; inline-SVG
    placeholder if the source is missing (e.g. final.png before a re-render)."""
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


def card(h):
    mid_html = ""
    if h.get("mid"):
        mid_html = (f'<div><div class="lbl mut">動畫中途幀</div>'
                    f'<img src="{uri(h["mid"])}" alt="{esc(h["scene_id"])} mid"></div>')
    return f'''
  <div class="card">
    <h3>{esc(h["nn"])} · {esc(h["scene_id"])} <span class="pill-ok">E-blocking 0</span></h3>
    <p class="lead"><b>{esc(h["title"])}</b></p>
    <p><span class="k">cue（意圖）</span>{esc(h["cue"])}</p>
    <p><span class="k">動畫</span>{esc(h["anim"])}</p>
    <div class="ba">
      <div><div class="lbl ok">端態（最末幀）</div><img src="{uri(h["final"])}" alt="{esc(h["scene_id"])}"></div>
      {mid_html}
    </div>
    <p class="eng"><span class="k">工程閘 E1/E2</span>{esc(h["eng"])}</p>
  </div>'''


def main():
    d = json.loads(DIGEST.read_text(encoding="utf-8"))
    summ = d["summary"]
    cards = "\n".join(card(h) for h in d["hooks"])

    doc = f'''<!DOCTYPE html>
<html lang="zh-Hant"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>§1.1 客製動畫 hook — sign-off 報告</title>
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
  .wrap{{max-width:1000px;margin:0 auto;padding:40px 24px 80px}}
  h1{{font-size:25px;margin:0 0 4px}} h2{{font-size:19px;margin:34px 0 12px;padding-bottom:6px;border-bottom:1px solid var(--line)}}
  h3{{font-size:15px;margin:0 0 6px;color:var(--accent)}}
  .sub{{color:var(--muted);font-size:14px;margin:0 0 4px}}
  .pill{{display:inline-block;padding:2px 10px;border-radius:999px;font-size:13px;font-weight:600;
    background:rgba(88,166,255,.15);color:var(--accent);border:1px solid rgba(88,166,255,.4)}}
  .pill-ok{{display:inline-block;padding:1px 9px;border-radius:999px;font-size:12px;font-weight:600;
    background:rgba(63,185,80,.15);color:var(--ok);border:1px solid rgba(63,185,80,.4)}}
  .tldr{{background:var(--panel);border:1px solid var(--line);border-left:3px solid var(--ok);border-radius:8px;padding:16px 18px;margin:18px 0}}
  .card{{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:16px 18px;margin:16px 0}}
  .lead{{font-size:15px;margin:2px 0 10px}}
  .k{{display:inline-block;min-width:104px;color:var(--muted);font-size:12px;text-transform:uppercase;letter-spacing:.4px;margin-right:8px}}
  .card p{{margin:5px 0;font-size:14px}}
  .eng{{margin-top:10px;padding-top:8px;border-top:1px solid var(--line);color:var(--ink)}}
  .ba{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:12px 0 4px}}
  .ba img{{width:100%;border-radius:6px;border:1px solid var(--line)}}
  .ba .lbl{{font-size:11px;text-transform:uppercase;letter-spacing:.5px;color:var(--muted);margin-bottom:4px}}
  code{{background:var(--code);color:var(--codeink);padding:1px 5px;border-radius:4px;font-size:13px;font-family:Consolas,monospace}}
  .ok{{color:var(--ok)}}.warn{{color:var(--warn)}}.bad{{color:var(--bad)}}.mut{{color:var(--muted)}}
  a{{color:var(--accent)}}
  .foot{{margin-top:36px;padding-top:14px;border-top:1px solid var(--line);color:var(--muted);font-size:13px}}
  @media(max-width:780px){{.ba{{grid-template-columns:1fr}}}}
</style></head><body><div class="wrap">

  <h1>§1.1 Inverse Functions — 客製動畫 hook · sign-off 報告</h1>
  <p class="sub">2026-06-17 · <span class="pill">Stage 2 第二輪動畫</span> · 5 個 <code># HOOK</code> 客製 manim 動畫</p>
  <p class="sub">生成動畫 code <b>視同 narration、需你 sign-off</b>（CONTENT_METHODOLOGY §5）。每個 hook 在模板既有 block 上替換 <code>anim</code> 為 callable，保留 reveal id／<code>{{show}}</code>／認可旁白不動；刪 <code>hook:</code> 行即回 stock 模板。</p>
  <p class="sub" style="font-size:12px">圖片均以 base64 內嵌（self-contained，換機 git clone 後仍可讀）。</p>

  <div class="tldr">
    <b>結論：</b>{summ["hooks"]} 個 hook 全 render 成功、最末幀端態正確、動畫都執行。<b>工程閘 E1/E2（5 agent＋E1 兩票複驗）：engineering blocking {summ["engineering_blocking"]}、confirmed {summ["confirmed_blocking"]}</b>——生成 code 數學保真（座標／反射建構／映射 pairs／弧方向，畫面看不到的部分全對）。Advisory 皆我自寫的 code、已就地清理（死 plumbing 清掉、<code>_mirror_xy</code> isotropic 加註、左臂出框手勢簡化）。<b>請逐一過目下方動畫、認可。</b>
  </div>

  <h2>5 個 hook</h2>
{cards}

  <div class="foot">
    工程閘 Workflow <code>{esc(summ["workflow"])}</code>（5 <code>hook-engineering-audit</code> agent＋E1 verify）· rubric <a href="HOOK-ENGINEERING-RUBRIC.md">HOOK-ENGINEERING-RUBRIC.md</a>（E1 數學保真 blocking＋E2 慣例）· 與 VISUAL-FRAME V8 分工（V8 看幀、本鏡看 code）·
    code <code>video/animations/ch01_inverse_functions_hooks.py</code>。
    <br>產生器：<code>_gen/REVIEW-ch01_inverse_functions-hooks.gen.py</code>（讀 .digest.json＋幀，圖 base64 內嵌、self-contained）。
  </div>

</div></body></html>'''
    OUT.write_text(doc, encoding="utf-8")
    size_mb = len(doc.encode("utf-8")) / 1e6
    print("wrote", OUT)
    print(f"hooks: {len(d['hooks'])} | embedded frames: {len(_URI_CACHE)} | "
          f"HTML size: {size_mb:.2f} MB | missing: {_MISSING or 'none'}")


if __name__ == "__main__":
    main()
