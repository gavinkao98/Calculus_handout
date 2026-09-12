# build_html.py — 把 <ID>/analysis.json（子代理拆解）＋ ours/（我方幀）＋ synthesis.html（主代理綜合判定）
# 合成單檔 standalone HTML（圖全內嵌 data URI）。用法：python build_html.py [out.html]
# 幀不進版控：缺圖時對應格子留空、不炸；重抓見 README.md。
import json, base64, os, io, sys, html, datetime
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'REVIEW-reference-videos.html')
W, Q = 880, 80


def b64(path, w=W, q=Q):
    im = Image.open(path).convert('RGB')
    if im.width > w:
        im = im.resize((w, round(w * im.height / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=q, optimize=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()


def esc(s):
    return html.escape(str(s if s is not None else ''))


def fmt_t(t):
    t = float(t or 0)
    m = int(t // 60)
    return f"{m}:{t - 60 * m:04.1f}"


DIM_ZH = {'motion-language': '動作語言', 'cross-scene-continuity': '跨場連續', 'visual-metaphor': '視覺隱喻',
          'layout-typography': '排版型階', 'sound-design': '音效'}
DIMS = list(DIM_ZH)
VIDS = [('A1', '3Blue1Brown・Essence of Calculus ch3・Sine 段'),
        ('A2', 'Think Twice・Derivative of sin(θ) is cos(θ)'),
        ('B1', 'Prof Ghrist・Calculus Lecture 10 Derivatives'),
        ('C1', 'Morphocular・Fractional Calculus')]
_full_dir = os.path.join(ROOT, 'ours', 'fullest')
_full_files = sorted(os.listdir(_full_dir)) if os.path.isdir(_full_dir) else []
FULLEST = {f.split('_', 1)[1].rsplit('.', 1)[0]: os.path.join(_full_dir, f) for f in _full_files}
FULLEST_ORDER = [f.split('_', 1)[1].rsplit('.', 1)[0] for f in _full_files]
_meta_path = os.path.join(ROOT, 'ours', 'meta.json')
ours_meta = json.load(open(_meta_path, encoding='utf-8')) if os.path.exists(_meta_path) else {}
SCENE_ZH = {'why_trig_is_different': '動機：代數為何不夠', 'difference_quotient_for_sine': '差商推導',
            'sector_inequality': '單位圓上的面積夾擠', 'squeeze_to_the_bound': '夾出上下界',
            'fundamental_limit': '基本極限定理', 'squeeze_graph': '夾擠，畫出來',
            'derivative_of_sine': 'sin 的導數（定理＋證明）', 'slope_equals_height': '斜率等於高度',
            'derivative_cycle': '導數循環', 'companion_limit': '伴隨極限', 'all_six_tan_sec': '六個導數（tan、sec）',
            'recap': '重點回顧', 'divider_limit': '章節分隔', 'continuity_statement_sin_limit': 'sin、cos 連續（陳述）'}
analyses = {}
for vid, _ in VIDS:
    p = os.path.join(ROOT, vid, 'analysis.json')
    if os.path.exists(p):
        analyses[vid] = json.load(open(p, encoding='utf-8'))
img_cache = {}


def img(path, w=W):
    key = (path, w)
    if key not in img_cache:
        img_cache[key] = b64(path, w)
    return img_cache[key]


def strip_html(files, base, cap=None, w=560):
    cells = ''.join(f'<img src="{img(os.path.join(base, f), w)}" alt="">' for f in files if os.path.exists(os.path.join(base, f)))
    if not cells:
        cells = '<span class="cap">（幀未抓；見 README 重抓）</span>'
    return f'<div class="strip">{cells}</div>' + (f'<div class="cap">{esc(cap)}</div>' if cap else '')


def ours_block(sid):
    if not sid or (sid not in FULLEST and sid not in ours_meta):
        return '<div class="ours none">（未對應我方場景）</div>'
    h = f'<div class="ours"><div class="ours-h">我方 §3.1・{esc(SCENE_ZH.get(sid, sid))} <code>{esc(sid)}</code></div>'
    if sid in FULLEST:
        h += f'<img class="full" src="{img(FULLEST[sid], 640)}" alt=""><div class="cap">2026-07-05 成片「最滿一幀」（六鏡看片的版本）</div>'
    if sid in ours_meta:
        s = ours_meta[sid]['strips'][1]
        base = os.path.join(ROOT, 'ours', sid)
        h += strip_html([os.path.relpath(f, base) for f in s['files']], base,
                        f'2026-09-12 單場重渲・t={fmt_t(s["t"])}（t−0.6／t／t+0.6）', 420)
    return h + '</div>'


CSS = """
:root{--ink:#1f2933;--mut:#5d646f;--line:#d9dee5;--bg:#fbfbfc;--card:#fff;--acc:#0068a7;--concept:#994a00;--practice:#04773b;--caution:#aa3333;--strategy:#6453a7}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.65 "Noto Sans TC","PingFang TC","Microsoft JhengHei",system-ui,sans-serif}
.wrap{max-width:1380px;margin:0 auto;padding:28px 32px 80px}h1{font-size:26px;margin:.2em 0}h2{font-size:21px;margin:2.2em 0 .6em;padding-bottom:.3em;border-bottom:2px solid var(--line)}h3{font-size:17px;margin:1.4em 0 .5em}
.meta{color:var(--mut);font-size:13.5px}code{font:13px/1 ui-monospace,Consolas,monospace;background:#eef1f5;padding:1px 5px;border-radius:4px}
table{border-collapse:collapse;width:100%;font-size:14px}th,td{border:1px solid var(--line);padding:8px 10px;vertical-align:top;text-align:left}th{background:#eef1f5}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px 18px;margin:14px 0;display:grid;grid-template-columns:1.25fr 1fr;gap:18px}
.card .txt{grid-column:1/-1}.strip{display:flex;gap:4px}.strip img{width:calc((100% - 8px)/3);height:auto;border-radius:4px;background:#000}
.cap{font-size:12.5px;color:var(--mut);margin-top:4px}.ours{background:#f4f6f9;border-radius:8px;padding:10px}.ours-h{font-weight:600;font-size:13.5px;margin-bottom:6px}.ours img.full{width:100%;border-radius:4px}.ours.none{color:var(--mut);font-size:13px}
.chip{display:inline-block;font-size:12px;padding:2px 8px;border-radius:999px;background:#e6eef7;color:var(--acc);margin-right:6px}.chip.vm{background:#f7ece3;color:var(--concept)}.chip.cc{background:#e6f3ea;color:var(--practice)}.chip.lt{background:#ece9f7;color:var(--strategy)}.chip.sd{background:#f7e6e6;color:var(--caution)}
.lbl{font-weight:700;font-size:16px}.t{color:var(--mut);font-size:13px;margin-left:8px}.k{font-weight:600;color:var(--mut);font-size:13px;margin-right:6px}
.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}.grid figure{margin:0}.grid img{width:100%;border-radius:4px}.grid figcaption{font-size:12px;color:var(--mut)}
.lesson{margin:.3em 0}.box{background:#fff8e6;border:1px solid #f0dca8;border-radius:8px;padding:12px 16px}
.syn{background:#eef6ff;border:1px solid #bcd6f0;border-radius:8px;padding:12px 16px}
@media(max-width:900px){.card{grid-template-columns:1fr}.grid{grid-template-columns:repeat(2,1fr)}}
"""
CHIP_CLS = {'motion-language': '', 'cross-scene-continuity': 'cc', 'visual-metaphor': 'vm', 'layout-typography': 'lt', 'sound-design': 'sd'}


def chips(dims):
    return ''.join(f'<span class="chip {CHIP_CLS.get(d, "")}">{esc(DIM_ZH.get(d, d))}</span>' for d in dims or [])


SYN_PATH = os.path.join(ROOT, 'synthesis.html')
synthesis = open(SYN_PATH, encoding='utf-8').read() if os.path.exists(SYN_PATH) else ''

parts = []
parts.append('<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8">'
             '<meta name="viewport" content="width=device-width,initial-scale=1">'
             '<title>參考影片視覺拆解對照表 A1／A2／B1／C1 vs §3.1</title>'
             f'<style>{CSS}</style></head><body><div class="wrap">')
parts.append('<h1>參考影片視覺拆解對照表：A1／A2／B1／C1 對照我方 §3.1</h1>'
             f'<div class="meta">產生日期 {datetime.date.today().isoformat()}・方法：headless Chrome 走 CDP 從 YouTube 播放器的 <code>&lt;video&gt;</code> 畫布抓幀（不下載影片）；'
             '每個時刻抓 t−0.6／t／t+0.6 三幀當「動作條」；四支影片由四個子代理各自挑時刻並寫分析，主代理核對合成。'
             '我方幀：2026-07-05 成片各場「最滿一幀」（六鏡看片的版本）＋ 2026-09-12 單場重渲的動作條（motion primitive 首輪進行中）。'
             '<b>音效維度無法從幀判斷，一律標「未評估」或只記來源已知事實。</b>第三方幀僅供內部對照審閱。</div>')

if synthesis:
    parts.append('<h2>0. 主代理綜合判定（先讀這段）</h2><div class="syn">' + synthesis + '</div>')

parts.append('<h2>1. 總覽：四支影片 × 五維度</h2><table><tr><th style="width:12%">影片</th><th style="width:14%">工具（來源／判斷）</th>'
             + ''.join(f'<th>{esc(DIM_ZH[d])}</th>' for d in DIMS) + '</tr>')
for vid, name in VIDS:
    a = analyses.get(vid)
    if not a:
        parts.append(f'<tr><td>{vid}</td><td colspan="7" class="meta">（無 analysis.json）</td></tr>')
        continue
    ov = a.get('overall', {})
    parts.append(f'<tr><td><b>{vid}</b><br><span class="meta">{esc(name)}</span><br><a href="{esc(a.get("url"))}">YouTube</a></td>'
                 f'<td>{esc(a.get("production_technique"))}</td>'
                 + ''.join(f'<td>{esc(ov.get(d, ""))}</td>' for d in DIMS) + '</tr>')
parts.append('</table>')

n = 1
for vid, name in VIDS:
    a = analyses.get(vid)
    n += 1
    parts.append(f'<h2>{n}. {vid}・{esc(name)}</h2>')
    if not a:
        parts.append('<p class="meta">（無 analysis.json）</p>')
        continue
    seg = a.get('segment') or [0, 0]
    parts.append(f'<div class="meta">{esc(a.get("title"))}・{esc(a.get("channel"))}・<a href="{esc(a.get("url"))}">{esc(a.get("url"))}</a>'
                 f'・片長 {fmt_t(a.get("duration_s") or 0)}・取樣段 {fmt_t(seg[0])}–{fmt_t(seg[1])}・工具：{esc(a.get("production_technique"))}</div>')
    base = os.path.join(ROOT, vid)
    for m in a.get('moments', []):
        t = float(m.get('t', 0))
        left = (f'<div><div><span class="lbl">{esc(m.get("label"))}</span><span class="t">t = {fmt_t(t)}・'
                f'<a href="{esc(a.get("url"))}&t={int(t)}s">在 YouTube 打開</a></span></div>'
                + strip_html(m.get('strip', []), base, '參考影片動作條（t−0.6／t／t+0.6）') + '</div>')
        right = ours_block(m.get('maps_to_ours'))
        txt = (f'<div class="txt"><div>{chips(m.get("dims"))}</div>'
               f'<p><span class="k">畫面</span>{esc(m.get("what"))}</p>'
               f'<p><span class="k">手法</span>{esc(m.get("technique"))}</p></div>')
        parts.append(f'<div class="card">{left}{right}{txt}</div>')

n += 1
parts.append(f'<h2>{n}. 給我們的教訓（子代理提案，待裁決）</h2><div class="box">')
for vid, name in VIDS:
    a = analyses.get(vid)
    if not a:
        continue
    parts.append(f'<h3>{vid}・{esc(name)}</h3><ul>' + ''.join(f'<li class="lesson">{esc(x)}</li>' for x in a.get('lessons_for_us', [])) + '</ul>')
parts.append('</div>')

if FULLEST_ORDER:
    n += 1
    parts.append(f'<h2>{n}. 我方 §3.1 基線全景（2026-07-05 成片「最滿一幀」）</h2><div class="grid">')
    for sid in FULLEST_ORDER:
        parts.append(f'<figure><img src="{img(FULLEST[sid], 480)}" alt=""><figcaption>{esc(SCENE_ZH.get(sid, sid))} <code>{esc(sid)}</code></figcaption></figure>')
    parts.append('</div>')

if ours_meta:
    n += 1
    parts.append(f'<h2>{n}. 我方 2026-09-12 單場重渲動作條（20%／50%／80% 片長各一組）</h2>')
    for sid, mm in ours_meta.items():
        parts.append(f'<h3>{esc(SCENE_ZH.get(sid, sid))} <code>{esc(sid)}</code>・{esc(mm["file"])}・{fmt_t(mm["duration"])}</h3>')
        base = os.path.join(ROOT, 'ours', sid)
        for s in mm['strips']:
            parts.append(strip_html([os.path.relpath(f, base) for f in s['files']], base, f't={fmt_t(s["t"])}', 420))
parts.append('</div></body></html>')
open(OUT, 'w', encoding='utf-8').write(''.join(parts))
print(OUT, round(os.path.getsize(OUT) / 1e6, 2), 'MB', 'videos:', list(analyses))
