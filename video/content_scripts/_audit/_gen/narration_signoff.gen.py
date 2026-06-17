#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the standalone narration sign-off HTML from a content-script .md.

The content script (`content_scripts/<deck>.md`) is the source of truth; this
emits `content_scripts/<deck>_narration.html` — a light-theme, MathJax-rendered,
double-click-to-open review doc (CONTENT_METHODOLOGY §6「交付形式」). Reusable
across sections: parses the meta bullet list + the `### unit:` / fenced-field
blocks, so re-running after any .md edit keeps the HTML in sync.

Usage:  python narration_signoff.gen.py <deck-id>
        (defaults to ch01_inverse_trig_functions)

Per-deck banner status lives in STATUS below (add an entry when running a new
deck). Body is pure stdlib — no external deps.
"""
import re, sys, html
from pathlib import Path

HERE = Path(__file__).resolve().parent
CS = HERE.parent.parent                      # content_scripts/

# Per-deck sign-off banner (pill + the two gate cards). Add an entry per deck.
STATUS = {
    "ch01_inverse_trig_functions": {
        "pill": '<span class="pill warn">DRAFT · 待 sign-off</span>',
        "gates": [
            ("六鏡內容稽核 ✓ 收斂",
             "0 blocking · 6 advisory（皆非阻斷）— L1 忠實／L2 拆解／L3 語域／L4 不重複／"
             "<b>L5 數學隔離盲算（10 項全 match）</b>／L6 完整，blocking 全歸零"),
            ("散文潤稿 ✓ gate1",
             "narration-copyedit：3 tighten＋6 optional 全 advisory；採 3 條純 wording "
             "（語義／數學未動）· gate2 Codex 可選收尾（計費，徵同意）"),
        ],
        "date": "2026-06-17",
    },
}

KIND_LABEL = {  # kinds that aren't their own literal label get a display tweak
}

def parse_meta(md):
    def grab(key):
        m = re.search(r'^- `%s`[^:：]*[:：]\s*(.+)$' % re.escape(key), md, re.M)
        return m.group(1).strip() if m else ""
    return {
        "id": grab("id"), "section": grab("section"), "title": grab("title"),
        "chapter": grab("chapter"), "chapter_title": grab("chapter_title"),
        "tagline": grab("tagline"),
    }

def parse_units(md):
    """Return [(uid, {field: value})] in document order."""
    blocks = re.findall(r'^### unit:\s*(\S+)\s*\n+```\n(.*?)\n```', md, re.M | re.S)
    out = []
    keyre = re.compile(r'^([a-z_]+):\s?(.*)$')
    for uid, body in blocks:
        fields, lines, i = {}, body.split('\n'), 0
        while i < len(lines):
            km = keyre.match(lines[i])
            if km:
                key, val = km.group(1), km.group(2)
                if val.strip() == '|':                      # block scalar
                    buf, i = [], i + 1
                    while i < len(lines) and (lines[i].startswith('  ') or not lines[i].strip()):
                        if lines[i].strip():
                            buf.append(lines[i][2:].rstrip() if lines[i].startswith('  ') else lines[i].strip())
                        i += 1
                    fields[key] = ' '.join(buf)
                    continue
                fields[key] = val.strip()
            i += 1
        out.append((uid, fields))
    return out

def esc(s):
    # Escape only &,<,> so inline $…$ LaTeX survives to MathJax (browser decodes
    # &lt; back to < in the DOM text before MathJax reads it).
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def is_silent(v):
    return v.strip().startswith('（無')

def card(idx, uid, f):
    kind = f.get('kind', 'motivation')
    narr = f.get('narration', '')
    head = ('<div class="uhead"><span class="unum">%02d</span>'
            '<span class="badge k-%s">%s</span><span class="uid">%s</span></div>'
            % (idx, kind, kind, esc(uid)))
    if is_silent(narr) or not narr:
        vn = f.get('visual_need', '').strip()
        sil = '純動畫（無旁白）— %s' % esc(vn) if vn else '純動畫（無旁白）。'
        return '  <section class="unit">\n    %s\n    <p class="narr silent">%s</p>\n  </section>\n' % (head, sil)
    rows = []
    if f.get('learning_goal') and not is_silent(f['learning_goal']):
        rows.append('<p class="meta-row"><b>Learning goal.</b> %s</p>' % esc(f['learning_goal']))
    if f.get('visual_need') and not is_silent(f['visual_need']):
        rows.append('<p class="meta-row"><b>視覺.</b> %s</p>' % esc(f['visual_need']))
    if f.get('animation_cue') and not is_silent(f['animation_cue']):
        rows.append('<p class="meta-row"><b>建議動畫.</b> %s</p>' % esc(f['animation_cue']))
    if f.get('source'):
        rows.append('<p class="meta-row"><b>來源.</b> %s</p>' % esc(f['source']))
    summ = 'learning goal · 視覺' + (' · 動畫' if (f.get('animation_cue') and not is_silent(f['animation_cue'])) else '')
    det = '    <details>\n      <summary>%s</summary>\n      %s\n    </details>\n' % (summ, '\n      '.join(rows))
    return '  <section class="unit">\n    %s\n    <p class="narr">%s</p>\n%s  </section>\n' % (head, esc(narr), det)

def build(deck):
    md = (CS / (deck + '.md')).read_text(encoding='utf-8')
    meta = parse_meta(md)
    units = parse_units(md)
    st = STATUS.get(deck, {"pill": '<span class="pill warn">DRAFT</span>', "gates": [], "date": ""})
    gates = '\n'.join(
        '    <div class="gate"><b>%s</b><div class="g-sub">%s</div></div>' % (t, s)
        for t, s in st["gates"])
    cards = ''.join(card(i, uid, f) for i, (uid, f) in enumerate(units))
    title = '§%s %s' % (meta['section'], meta['title'])
    H = []
    H.append('<!DOCTYPE html>\n<html lang="zh-Hant">\n<head>\n<meta charset="utf-8">')
    H.append('<meta name="viewport" content="width=device-width, initial-scale=1">')
    H.append('<title>%s — 旁白審核稿</title>' % esc(title))
    H.append('''<script>
  window.MathJax = {
    tex: { inlineMath: [['$','$'], ['\\\\(','\\\\)']], displayMath: [['$$','$$'], ['\\\\[','\\\\]']] },
    svg: { fontCache: 'global' }
  };
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js" id="MathJax-script" async></script>''')
    H.append('''<style>
  :root{
    --bg:#f7f8fa; --paper:#ffffff; --ink:#1c2330; --soft:#5b6675; --line:#e3e7ee;
    --accent:#2f6df0; --accentsoft:#eaf1ff;
    --def:#0a8f6e; --thm:#b8860b; --ex:#2f6df0; --prop:#7a3ff0; --proc:#c2410c;
    --vis:#0e7490; --motiv:#475569; --recap:#be185d; --cex:#dc2626;
    --ok:#0a8f6e; --warnbg:#fff7e6; --warnline:#e0b341;
  }
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);
    font:17px/1.7 -apple-system,"Segoe UI",Roboto,"Noto Sans CJK TC","Microsoft JhengHei",Georgia,serif;}
  .wrap{max-width:860px;margin:0 auto;padding:40px 22px 90px}
  h1{font-size:27px;margin:0 0 6px;letter-spacing:.2px}
  .sub{color:var(--soft);font-size:14.5px;margin:2px 0}
  .pill{display:inline-block;padding:2px 11px;border-radius:999px;font-size:12.5px;font-weight:700;
    background:var(--accentsoft);color:var(--accent);border:1px solid #bcd2fb;vertical-align:middle}
  .pill.warn{background:var(--warnbg);color:#9a6a00;border-color:var(--warnline)}
  .gates{display:flex;gap:10px;flex-wrap:wrap;margin:16px 0 4px}
  .gate{flex:1;min-width:210px;background:var(--paper);border:1px solid var(--line);
    border-left:3px solid var(--ok);border-radius:9px;padding:11px 14px;font-size:13.5px}
  .gate b{color:var(--ink)} .gate .g-sub{color:var(--soft)}
  .howto{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:14px 18px;margin:18px 0 6px;font-size:14.5px;color:var(--soft)}
  .howto b{color:var(--ink)}
  .unit{background:var(--paper);border:1px solid var(--line);border-radius:12px;
    padding:18px 22px 14px;margin:18px 0;box-shadow:0 1px 2px rgba(20,30,50,.03)}
  .uhead{display:flex;align-items:center;gap:11px;margin-bottom:8px;flex-wrap:wrap}
  .unum{font-variant-numeric:tabular-nums;font-weight:700;color:var(--soft);font-size:14px;
    border:1px solid var(--line);border-radius:7px;padding:1px 8px;background:var(--bg)}
  .badge{font-size:11.5px;font-weight:700;letter-spacing:.4px;text-transform:uppercase;
    padding:2px 9px;border-radius:6px;color:#fff}
  .uid{font-family:"Cascadia Code",Consolas,monospace;font-size:12.5px;color:var(--soft)}
  .k-motivation{background:var(--motiv)} .k-definition{background:var(--def)}
  .k-example{background:var(--ex)} .k-proposition{background:var(--prop)}
  .k-theorem{background:var(--thm)} .k-procedure{background:var(--proc)}
  .k-visual{background:var(--vis)} .k-recap{background:var(--recap)}
  .k-counterexample{background:var(--cex)}
  .narr{font-size:18px;line-height:1.78;margin:6px 0 10px}
  .silent{color:var(--soft);font-style:italic}
  details{margin-top:8px;border-top:1px dashed var(--line);padding-top:8px}
  summary{cursor:pointer;color:var(--accent);font-size:13.5px;font-weight:600;list-style:none}
  summary::-webkit-details-marker{display:none}
  summary::before{content:"\\25B8 ";color:var(--soft)}
  details[open] summary::before{content:"\\25BE "}
  .meta-row{font-size:14px;color:var(--soft);margin:7px 0}
  .meta-row b{color:var(--ink)}
  .foot{margin-top:42px;padding-top:14px;border-top:1px solid var(--line);color:var(--soft);font-size:13px}
  a{color:var(--accent)}
  code{font-family:"Cascadia Code",Consolas,monospace;font-size:.92em}
</style>
</head>
<body>
<div class="wrap">''')
    H.append('  <h1>%s — 旁白審核稿</h1>' % esc(title))
    H.append('  <p class="sub">deck <code>%s</code> · %s「%s」· %s</p>'
             % (esc(meta['id']), esc(meta['chapter']), esc(meta['chapter_title']), st['pill']))
    H.append('  <p class="sub">權威來源：<code>handout/chapter1-print-standalone.html</code> §%s'
             '（編輯源 <code>fragments/ch01/sec-%s.html</code>）· source of truth：'
             '<code>video/content_scripts/%s.md</code> · %s</p>'
             % (esc(meta['section']), esc(meta['section'].replace('.', '-')), esc(meta['id']), st['date']))
    H.append('  <p class="sub">引導問題（intro tagline）：<i>“%s”</i></p>' % esc(meta['tagline']))
    H.append('  <div class="gates">\n%s\n  </div>' % gates)
    H.append('''  <div class="howto">
    <b>怎麼審：</b>下面每張卡是一個教學單元的「旁白原文」（為「說」而寫，數學已渲染）。請把 narration 當成老師會<b>唸出來</b>的話來審——順不順、清不清楚、教學對不對位。每張卡可展開看 learning goal／靜態視覺需求／建議動畫（這些是工程第二階段的依據，<b>非</b>本次 sign-off 的對象）。認可後才 lock → 進工程稿（storyboard）。intro／outro 為純動畫、無旁白。
  </div>''')
    H.append(cards)
    H.append('  <p class="foot">本檔由 <code>_audit/_gen/narration_signoff.gen.py</code> 從 '
             '<code>%s.md</code> 編譯產生；<code>.md</code> 為權威，改稿後重跑即同步。'
             '單元數：%d（含 intro／outro）。</p>' % (esc(meta['id']), len(units)))
    H.append('</div>\n</body>\n</html>\n')
    out = CS / (deck + '_narration.html')
    out.write_text('\n'.join(H), encoding='utf-8')
    print('wrote', out, '(%d units)' % len(units))

if __name__ == '__main__':
    build(sys.argv[1] if len(sys.argv) > 1 else 'ch01_inverse_trig_functions')
