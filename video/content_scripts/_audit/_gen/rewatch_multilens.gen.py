"""rewatch_multilens.gen.py -- REWATCH multi-lens film review -> self-contained HTML.

    python video/content_scripts/_audit/_gen/rewatch_multilens.gen.py \
        [--digest _gen/rewatch_multilens.digest.json] [--out ../REVIEW-ch03_s31-rewatch-multilens.html]

Reads the digest (the six lens outputs merged + the orchestrator's per-finding checks and
per-scene synthesis; see REWATCH-REVIEW-RUBRIC.md "編排") and the rewatch pack (for the per-
scene contact sheets, embedded downscaled as base64 so the report opens anywhere). Pure
stdlib + PIL. Report text is Traditional Chinese; quotes / ids stay English (CLAUDE.md).
"""
from __future__ import annotations

import argparse
import base64
import html
import io
import json
from pathlib import Path

from rewatch_merge import rule_counts

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]

VERDICT_CLS = {"good": "v-good", "ok": "v-ok", "weak": "v-weak", "bad": "v-bad", "—": "v-none"}
CHECK = {"confirmed": ("✔ 核實", "c-ok"), "plausible": ("◐ 合理", "c-pl"), "refuted": ("✖ 駁回", "c-no"),
         "dup": ("≡ 重複", "c-dup"), None: ("· 未核", "c-none"), "": ("· 未核", "c-none")}
SEV_ORDER = {"must": 0, "should": 1, "nice": 2, "note": 3}
LENS_NAME = {"R1": "初學者", "R2": "動畫導演", "R3": "教學設計", "R4": "節奏剪輯", "R5": "講師"}
RULE_NAME = {"ML1": "一場一張畫布", "ML2": "畫出來，只動變的 token", "ML3": "框、放大鏡、調暗，不靠鏡頭",
             "ML4": "靜止是設計出來的", "ML5": "語意色貫穿圖與式", "unlabeled": "未標"}


def esc(s) -> str:
    return html.escape(str(s if s is not None else ""), quote=False)


def fmt(t: float) -> str:
    m, s = divmod(max(float(t), 0.0), 60)
    return f"{int(m)}:{s:04.1f}"


def sheet_b64(path: Path, width: int = 1100) -> str:
    from PIL import Image
    im = Image.open(path).convert("RGB")
    if im.width > width:
        im = im.resize((width, int(im.height * width / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=78, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode("ascii")


CSS = """
:root{--ink:#1a2233;--muted:#5a6b85;--line:#dce3ee;--bg:#f6f8fc;--navy:#0a1322;--card:#fff;--accent:#b0792a;
 --good:#1f7a4d;--goodbg:#e9f6ef;--ok:#20609b;--okbg:#e8f0fa;--weak:#9a6a12;--weakbg:#fdf4e3;--bad:#b3261e;--badbg:#fdecea}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.65 -apple-system,"Segoe UI",Roboto,"Noto Sans TC","PingFang TC","Microsoft JhengHei",sans-serif}
.wrap{max-width:1180px;margin:0 auto;padding:30px 22px 90px}
header.top{background:var(--navy);color:#fff;border-radius:14px;padding:24px 30px;margin-bottom:18px}
header .eyebrow{font:600 12px/1 ui-monospace,Consolas,monospace;letter-spacing:.14em;text-transform:uppercase;color:#8fb0e6}
header h1{margin:.35em 0 .2em;font-size:25px}
header .sub{color:#c4d2ec}
.meta{display:flex;flex-wrap:wrap;gap:6px 18px;margin-top:12px;font:13px/1.5 ui-monospace,Consolas,monospace;color:#c4d2ec}
.tldr{background:#12203a;border:1px solid #24406e;border-radius:10px;margin-top:16px;padding:14px 18px}
.tldr p{margin:.4em 0;color:#e6edf3}.tldr b{color:#7ee0a8}.tldr li{color:#e6edf3}
h2{font-size:18px;margin:34px 0 10px;padding-bottom:6px;border-bottom:2px solid var(--line)}
h3{font-size:16px;margin:26px 0 6px}
p{margin:.55em 0}
table{border-collapse:collapse;width:100%;background:var(--card);border:1px solid var(--line);border-radius:10px;overflow:hidden;font-size:13px;margin:10px 0}
th,td{text-align:left;vertical-align:top;padding:7px 9px;border-bottom:1px solid var(--line)}
th{background:#eef2f9;font:600 11.5px/1.3 ui-monospace,Consolas,monospace;color:#33415c;text-transform:uppercase;letter-spacing:.04em}
tr:last-child td{border-bottom:none}
code{font:12.5px/1.4 ui-monospace,Consolas,monospace;background:#eef1f7;padding:1px 4px;border-radius:3px;color:#33415c}
.note{font-size:13px;color:var(--muted);margin:14px 2px;padding:11px 15px;border-left:3px solid var(--accent);background:#fff8ec;border-radius:4px}
.chip{display:inline-block;font:600 11.5px/1.35 ui-monospace,Consolas,monospace;padding:2px 8px;border-radius:20px;white-space:nowrap;border:1px solid;margin:0 4px 2px 0;vertical-align:middle}
.v-good{color:var(--good);background:var(--goodbg);border-color:#bfe3cf}.v-ok{color:var(--ok);background:var(--okbg);border-color:#c3d8f0}
.v-weak{color:var(--weak);background:var(--weakbg);border-color:#ecd6a8}.v-bad{color:var(--bad);background:var(--badbg);border-color:#f1b8b3}
.v-none{color:#8a97ad;background:#f1f3f8;border-color:#d8dee9}
.c-ok{color:var(--good);border-color:#bfe3cf;background:var(--goodbg)}.c-pl{color:var(--ok);border-color:#c3d8f0;background:var(--okbg)}
.c-no{color:var(--bad);border-color:#f1b8b3;background:var(--badbg);text-decoration:line-through}.c-dup{color:#6b7280;border-color:#d8dee9;background:#f1f3f8}.c-none{color:#8a97ad;border-color:#d8dee9;background:#f8f9fb}
.lens{color:#33415c;background:#eef2f9;border-color:#d0d9e8}
.sev-must{color:var(--bad);border-color:#f1b8b3;background:var(--badbg)}.sev-should{color:var(--weak);border-color:#ecd6a8;background:var(--weakbg)}.sev-nice{color:var(--ok);border-color:#c3d8f0;background:var(--okbg)}.sev-note{color:#6b7280;border-color:#d8dee9;background:#f1f3f8}
.scene{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 20px;margin:18px 0}
.scene .stats{font:12.5px/1.6 ui-monospace,Consolas,monospace;color:var(--muted);margin:4px 0 8px}
.scene img{width:100%;height:auto;border-radius:8px;border:1px solid var(--line);margin:8px 0}
.syn{background:#f3f7fd;border-left:4px solid var(--ok);border-radius:6px;padding:10px 14px;margin:10px 0}
.syn.lv1{border-left-color:var(--bad)}.syn.lv2{border-left-color:var(--weak)}.syn.lv3{border-left-color:var(--ok)}.syn.lv4{border-left-color:var(--good)}
.finding{border:1px solid var(--line);border-radius:8px;padding:9px 12px;margin:7px 0;font-size:13.5px}
.finding.refuted{opacity:.55}
.finding .hd{display:flex;flex-wrap:wrap;gap:4px;align-items:center;margin-bottom:4px}
.finding .where{font:12px/1.4 ui-monospace,Consolas,monospace;color:var(--muted)}
.finding .ev{color:#33415c}.finding .pr{color:var(--ink)}.finding .pp{color:var(--good)}
.finding .ck{font-size:12.5px;color:var(--muted);margin-top:4px;border-top:1px dashed var(--line);padding-top:4px}
details{margin:8px 0}summary{cursor:pointer;font-weight:600}
.small{font-size:12.5px;color:var(--muted)}
.matrix td{text-align:center;padding:5px 6px}.matrix td.left{text-align:left}
.foot{margin-top:30px;font-size:12.5px;color:var(--muted);font-style:italic}
ul,ol{margin:6px 0;padding-left:22px}li{margin:4px 0}
"""


def chip(text: str, cls: str) -> str:
    return f'<span class="chip {cls}">{esc(text)}</span>'


def render(digest: dict, pack_dir: Path, embed: bool) -> str:
    lenses = digest["lenses"]
    scenes = digest["scenes"]
    film = digest.get("film", {})
    runs = list(lenses.keys())
    out: list[str] = []
    out.append(f"""<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>§3.1 成片 看片多鏡評審</title>
<script>window.MathJax={{tex:{{inlineMath:[['$','$']],displayMath:[['$$','$$']]}},svg:{{fontCache:'global'}}}};</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js" async></script>
<style>{CSS}</style></head><body><div class="wrap">
<header class="top"><div class="eyebrow">video · rewatch multi-lens review · advisory</div>
<h1>§3.1 成片 看片多鏡評審</h1>
<div class="sub">被審物：<code>{esc(Path(digest['film_path']).name)}</code>（{fmt(digest['total_seconds'])}，{len(scenes)} 場，2026-07-05 Dean 成片）。五鏡六份獨立盲審，orchestrator 逐條核實後合成。契約：<code>{esc(digest['rubric'])}</code>。</div>
<div class="meta"><span>日期：{esc(digest['date'])}</span><span>鏡頭：{'、'.join(f"{r}={lenses[r]['model']}" for r in runs)}</span><span>合成：Fable 5.1（refute-by-default）</span></div>
<div class="tldr"><p><b>一句話：</b>{esc(film.get('overall', ''))}</p>
<p><b>全片共同模式（多鏡同指）：</b></p><ul>{''.join(f'<li>{esc(p)}</li>' for p in film.get('patterns', []))}</ul>
<p><b>對「水位」決定的意義：</b>{esc(film.get('water_level', ''))}</p></div></header>
<div class="note"><b>怎麼讀：</b>每場一張卡：sheet（抽幀＋此刻旁白）→ 六份 verdict → 各鏡 findings（每條標 <span class="chip c-ok">✔ 核實</span>＝我對照 sheet／時間軸確認屬實、<span class="chip c-pl">◐ 合理</span>＝方向對但無法逐格核實或屬品味判斷、<span class="chip c-no">✖ 駁回</span>＝與 pack 證據不符、<span class="chip c-dup">≡ 重複</span>＝同一鏡或他鏡已提）→ 合成判定與「最該改的一件事」。分級沿用 CLAUDE.md 四級：① 真問題要修、② 補件即可、③ 結構性（重做時處理）、④ 非 finding。<b>本審不重審忠實／數學／聽感。</b></div>
""")
    # matrix
    out.append("<h2>一、逐場 verdict 矩陣</h2><table class=\"matrix\"><thead><tr><th class=\"left\">#</th><th class=\"left\">場</th><th>秒</th><th>靜止</th>"
               + "".join(f"<th>{esc(r)}<br><span class=\"small\">{esc(LENS_NAME[lenses[r]['lens']])}</span></th>" for r in runs)
               + "<th>合成</th><th class=\"left\">最該改的一件事</th></tr></thead><tbody>")
    for s in scenes:
        cells = "".join(f'<td>{chip(s["verdicts"].get(r, "—"), VERDICT_CLS.get(s["verdicts"].get(r, "—"), "v-none"))}</td>' for r in runs)
        out.append(f'<tr><td class="left">{s["n"]:02d}</td><td class="left"><a href="#s{s["n"]:02d}"><code>{esc(s["id"])}</code></a></td>'
                   f'<td>{s["duration"]:.0f}</td><td>{s["motion"]["static_ratio"] * 100:.0f}%</td>{cells}'
                   f'<td>{chip(s.get("level") or "—", "lens")}</td><td class="left">{esc(s.get("one_change", ""))}</td></tr>')
    out.append("</tbody></table>")
    # finding x motion-language rule (rubric `rule`; digest by_rule, recomputed for digests that predate it)
    total = digest.get("by_rule") or rule_counts([f for s in scenes for f in s["findings"]])
    per = {s["n"]: (s.get("by_rule") or rule_counts(s["findings"])) for s in scenes}
    out.append("<h3>finding × 畫面語法規則</h3><p class=\"small\"><code>rule</code> 欄位（SPEC-motion-language.md §0；R2 MUST、其他鏡 MAY）；不計 ✖ 駁回／≡ 重複與 note。</p>"
               "<table><thead><tr><th>代號</th><th>規則</th><th>合計</th><th>各場（場號 ×條數）</th></tr></thead><tbody>")
    for code, n in total.items():
        where = "、".join(f"{k:02d}×{c[code]}" for k, c in per.items() if c.get(code))
        out.append(f"<tr><td><code>{esc(code)}</code></td><td>{esc(RULE_NAME.get(code, code))}</td><td>{n}</td><td class=\"small\">{esc(where)}</td></tr>")
    out.append("</tbody></table>")
    # per-lens film verdicts
    out.append("<h2>二、各鏡總評（原文，未經合成）</h2>")
    for r in runs:
        L = lenses[r]
        f = L.get("film", {})
        u = L.get("usage") or {}
        out.append(f"<details><summary>{esc(r)} · {esc(LENS_NAME[L['lens']])} · {esc(L['model'])}"
                   f"{'  · tokens in/out ' + esc(u.get('input_tokens')) + '/' + esc(u.get('output_tokens')) if u else ''}</summary>"
                   f"<p><b>總評：</b>{esc(f.get('overall', ''))}</p><ul>{''.join(f'<li>{esc(p)}</li>' for p in f.get('patterns', []))}</ul>"
                   f"<p class=\"small\">最強：{esc('、'.join(f.get('strongest_scenes', [])))}　最弱：{esc('、'.join(f.get('weakest_scenes', [])))}</p></details>")
    if digest.get("missing_runs"):
        out.append(f"<p class=\"note\">未取得輸出的鏡：{esc('; '.join(digest['missing_runs']))}</p>")
    # scenes
    out.append("<h2>三、逐場</h2>")
    for s in scenes:
        m = s["motion"]
        sheet = pack_dir / s["sheet"]
        img = (f'<a href="{esc(sheet.as_posix())}" target="_blank"><img src="{sheet_b64(sheet) if embed else esc(sheet.as_posix())}" alt="{esc(s["id"])} sheet"></a>'
               if sheet.exists() else "<p class=\"small\">（sheet 不在本機）</p>")
        verd = " ".join(f'{esc(r)} {chip(s["verdicts"].get(r, "—"), VERDICT_CLS.get(s["verdicts"].get(r, "—"), "v-none"))}' for r in runs)
        lv = {"①": "lv1", "②": "lv2", "③": "lv3", "④": "lv4"}.get((s.get("level") or "")[:1], "")
        syn = (f'<div class="syn {lv}"><b>合成判定 {esc(s.get("level", ""))}</b>　{esc(s.get("synthesis", ""))}'
               f'<br><b>最該改的一件事：</b>{esc(s.get("one_change", ""))}</div>') if (s.get("synthesis") or s.get("one_change")) else ""
        fl = sorted(s["findings"], key=lambda f: (SEV_ORDER.get(f["severity"], 9), f["run"]))
        items = []
        for f in fl:
            ck_label, ck_cls = CHECK.get(f.get("check"), CHECK[None])
            cls = "finding refuted" if f.get("check") in ("refuted", "dup") else "finding"
            hd = (chip(f["run"] + " " + LENS_NAME[f["lens"]], "lens") + chip(f["severity"], "sev-" + f["severity"])
                  + (chip(f["dim"], "lens") if f["dim"] else "") + (chip(f["rule"], "lens") if f.get("rule") else "") + chip(ck_label, ck_cls)
                  + f'<span class="where">{esc(f["fid"])} · {esc(f["where"])}</span>')
            body = ""
            if f["evidence"]:
                body += f'<div class="ev"><b>證據：</b>{esc(f["evidence"])}</div>'
            body += f'<div class="pr"><b>問題：</b>{esc(f["problem"])}</div>' if f["problem"] else ""
            if f["proposal"]:
                body += f'<div class="pp"><b>提議：</b>{esc(f["proposal"])}</div>'
            if f.get("check_note"):
                body += f'<div class="ck">核實：{esc(f["check_note"])}</div>'
            items.append(f'<div class="{cls}"><div class="hd">{hd}</div>{body}</div>')
        out.append(f"""<div class="scene" id="s{s['n']:02d}"><h3>{s['n']:02d} · {esc(s['title'])} <code>{esc(s['id'])}</code></h3>
<div class="stats">全片 {fmt(s['global_start'])} → {fmt(s['global_start'] + s['duration'])} · {s['duration']:.1f}s · {esc(s['kind'])}{(' / ' + esc(s['template'])) if s.get('template') else ''}{' · hook' if s.get('hook') else ''} · reveals {s['reveals']} · 靜止 {m['static_ratio'] * 100:.0f}% · 最長不動 {m['longest_still_seconds']}s · 非 reveal 變化 {len(m['non_reveal_events'])} 次</div>
{img}<div>{verd}</div>{syn}{''.join(items) or '<p class="small">六鏡皆無 finding。</p>'}</div>""")
    out.append(f"""<h2>附錄 · 方法與重現</h2>
<p class="small">pack：<code>python video/pipeline/rewatch_pack.py --deck {esc(digest['deck'])}</code>（離線）。六份盲審依 <code>PROMPT-rewatch.template.md</code> 組裝（每鏡只拿自己的段落與共同規則；R1 兩份在 repo 外隔離工作區、只給觀眾面 pack；R3 另拿 §3.1 的 .tex；R4 不看圖）。agy 三次（唯讀 <code>--mode plan</code>、<code>--json-schema</code>）＋ subagent 三次。原始輸出＝<code>_gen/rewatch_lenses/*.json</code>；合成資料＝<code>_gen/rewatch_multilens.digest.json</code>；本檔由 <code>_gen/rewatch_multilens.gen.py</code> 產生。</p>
<p class="foot">advisory、propose-not-act：本報告不改任何產線檔案；裁決權在使用者。</p></div></body></html>""")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--digest", type=Path, default=HERE / "rewatch_multilens.digest.json")
    ap.add_argument("--out", type=Path, default=HERE.parent / "REVIEW-ch03_s31-rewatch-multilens.html")
    ap.add_argument("--no-embed", action="store_true", help="link sheets instead of embedding base64")
    args = ap.parse_args()
    digest = json.loads(args.digest.read_text(encoding="utf-8"))
    pack_dir = Path(digest["film_path"]).parent / "rewatch_pack"
    args.out.write_text(render(digest, pack_dir, embed=not args.no_embed), encoding="utf-8")
    print(f"wrote {args.out} ({args.out.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
