"""code_review_2026_09_23.gen.py -- 2026-09-23 程式碼審查報告 -> self-contained HTML.

    python video/_audit/_gen/code_review_2026_09_23.gen.py [--out <html>]

讀三份資料：
  * code_review_2026_09_23.findings.json -- 7 片審查員的原始回傳（Workflow 結構化輸出，照登不改字）
  * code_review_2026_09_23.digest.json   -- 主模型的稽核結論（裁決、批次、活動紀錄、限制）
  * code_review_2026_09_23.outcome.json  -- 修正輪的結果（輪次、驗收、每條 finding 的修正與回歸判定；沒有時只呈現審查）
預設輸出 video/_audit/REVIEW-code-review-2026-09-23.html。純 stdlib；報告不含數學式，所以不載 MathJax
（finding 原文裡的 `$...$` 是被審的字串，要照字面顯示）。本產生器不下判斷——所有評語取自這三份 JSON。
"""
from __future__ import annotations

import argparse
import html
import json
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
FINDINGS = HERE / "code_review_2026_09_23.findings.json"
DIGEST = HERE / "code_review_2026_09_23.digest.json"
OUTCOME = HERE / "code_review_2026_09_23.outcome.json"   # 修正輪的結果；不存在時報告只呈現審查
OUT = HERE.parent / "REVIEW-code-review-2026-09-23.html"

DECISION = {"fix": "修", "doc": "補文件", "dup": "重複", "record": "只記錄"}
AUDIT = {"reran": "主模型重跑重現", "code": "主模型讀 code 核對", "reviewer": "審查員證據"}
LEVEL = {1: "L1 真 bug", 2: "L2 缺文件", 3: "L3 drift"}

CSS = """
:root{--ink:#1a2233;--muted:#5a6b85;--line:#dce3ee;--bg:#f6f8fc;--navy:#0a1322;--card:#fff;
 --t1:#b3261e;--t1bg:#fdecea;--t2:#9a6a12;--t2bg:#fdf4e3;--t3:#20609b;--t3bg:#e8f0fa;--t4:#1f7a4d;--t4bg:#e9f6ef}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.65 -apple-system,"Segoe UI",Roboto,"Noto Sans TC","PingFang TC","Microsoft JhengHei",sans-serif}
.wrap{max-width:1080px;margin:0 auto;padding:34px 22px 90px}
header.top{background:var(--navy);color:#fff;border-radius:14px;padding:26px 30px;margin-bottom:18px}
header .eyebrow{font:600 12px/1 ui-monospace,Consolas,monospace;letter-spacing:.14em;text-transform:uppercase;color:#8fb0e6}
header h1{margin:.35em 0 .2em;font-size:25px}
.meta{display:flex;flex-wrap:wrap;gap:6px 18px;margin-top:12px;font:13px/1.5 ui-monospace,Consolas,monospace;color:#c4d2ec}
.tldr{background:#12203a;border:1px solid #24406e;border-radius:10px;margin-top:16px;padding:14px 18px}
.tldr li{margin:.35em 0;color:#e6edf3}
.tldr code{background:#1d3157;color:#e6edf3}
h2{font-size:18px;margin:34px 0 10px;padding-bottom:6px;border-bottom:2px solid var(--line)}
h3{font-size:15.5px;margin:22px 0 8px}
p{margin:.55em 0}
table{border-collapse:collapse;width:100%;background:var(--card);border:1px solid var(--line);border-radius:10px;overflow:hidden;font-size:13.5px;margin:10px 0}
th,td{text-align:left;vertical-align:top;padding:8px 10px;border-bottom:1px solid var(--line)}
th{background:#eef2f9;font:600 12px/1.3 ui-monospace,Consolas,monospace;color:#33415c;letter-spacing:.03em}
tr:last-child td{border-bottom:none}
td.num{text-align:right;font-variant-numeric:tabular-nums}
code{font:12.5px/1.4 ui-monospace,Consolas,monospace;background:#eef1f7;padding:1px 4px;border-radius:3px;color:#33415c;word-break:break-word}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 18px;margin:12px 0}
.card.l1{border-left:5px solid var(--t1)}.card.l2{border-left:5px solid var(--t3)}.card.l3{border-left:5px solid var(--t2)}
.card h4{margin:0 0 6px;font-size:15px}
.card dl{margin:8px 0 0;display:grid;grid-template-columns:7.5em 1fr;gap:6px 12px}
.card dt{color:var(--muted);font-size:13px}
.card dd{margin:0;font-size:14px;min-width:0}
.pill{display:inline-block;font:600 11.5px/1.6 ui-monospace,Consolas,monospace;padding:0 7px;border-radius:999px;margin-right:4px;white-space:nowrap}
.p-l1{background:var(--t1bg);color:var(--t1)}.p-l2{background:var(--t3bg);color:var(--t3)}.p-l3{background:var(--t2bg);color:var(--t2)}
.p-high{background:var(--t1);color:#fff}.p-medium{background:var(--t2bg);color:var(--t2)}.p-low{background:#eef1f7;color:#33415c}
.p-fix{background:var(--t4bg);color:var(--t4)}.p-doc{background:var(--t3bg);color:var(--t3)}.p-dup{background:#eef1f7;color:var(--muted)}.p-record{background:var(--t2bg);color:var(--t2)}
.muted{color:var(--muted)}
.note{background:#fffbea;border:1px solid #f0e2a8;border-radius:8px;padding:10px 14px;margin:10px 0;font-size:14px}
details{margin:8px 0}
summary{cursor:pointer;color:var(--muted);font-size:13.5px}
.scroll{overflow-x:auto}
@media (max-width:640px){.wrap{padding:18px 16px 60px}.card dl{grid-template-columns:1fr}header.top{padding:20px}}
"""


def t(s: object) -> str:
    """Escape, then render `code` spans and line breaks."""
    s = html.escape(str(s))
    s = re.sub(r"`([^`\n]+)`", r"<code>\1</code>", s)
    return s.replace("\n", "<br>")


def pill(cls: str, text: str) -> str:
    return f'<span class="pill p-{cls}">{html.escape(text)}</span>'


def slice_key(name: str) -> str:
    return name.split()[0]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=OUT)
    args = ap.parse_args()

    slices = json.loads(FINDINGS.read_text(encoding="utf-8"))
    dg = json.loads(DIGEST.read_text(encoding="utf-8"))
    oc = json.loads(OUTCOME.read_text(encoding="utf-8")) if OUTCOME.exists() else None
    dec = dg["decisions"]
    order = ["A", "B", "C", "D1", "D2", "E", "F"]
    slices.sort(key=lambda s: order.index(slice_key(s["slice"])))
    allf = [f for s in slices for f in s["findings"]]
    missing = {f["id"] for f in allf} ^ set(dec)
    if missing:
        raise SystemExit(f"decisions and findings disagree on: {sorted(missing)}")
    uniq = [f for f in allf if dec[f["id"]][0] != "dup"]
    dcount = Counter(dec[f["id"]][0] for f in allf)

    def result_cell(fid: str) -> str:
        """One finding's fix outcome: status pill + commits (+ the regression closure verdict)."""
        r = (oc or {}).get("findings", {}).get(fid)
        if r is None:
            return '<span class="muted">—</span>'
        cls = {"fixed": "fix", "partial": "record", "not_fixed": "record", "no_change_needed": "dup",
               "recorded": "record"}.get(r["status"], "dup")
        label = {"fixed": "已修", "partial": "部分", "not_fixed": "未修", "no_change_needed": "免修",
                 "recorded": "只記錄"}.get(r["status"], r["status"])
        commits = " ".join(f"<code>{html.escape(c)}</code>" for c in r.get("commits", []))
        verdict = r.get("closure")
        tail = f' <span class="muted">回歸：{html.escape(verdict)}</span>' if verdict else ""
        return pill(cls, label) + commits + tail

    out: list[str] = []
    w = out.append
    w('<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="utf-8">')
    w('<meta name="viewport" content="width=device-width, initial-scale=1">')
    w(f"<title>{html.escape(dg['title'])}</title><style>{CSS}</style></head><body><div class=\"wrap\">")

    # ---- header ----
    w('<header class="top"><div class="eyebrow">Code review · video pipeline ＋ handout LaTeX build</div>')
    w(f"<h1>{html.escape(dg['title'])}</h1>")
    w(f'<div class="meta"><span>快照 {dg["snapshot"]}</span><span>跨模組 diff {dg["diff_base"]}..{dg["snapshot"]}</span>'
      f'<span>{len(allf)} 條 finding／去重 {len(uniq)} 條</span><span>{html.escape(dg["reviewers"])}</span></div>')
    w(f'<div class="meta"><span>狀態：{html.escape(dg["status"])}</span></div>')
    w('<div class="tldr"><ul>' + "".join(f"<li>{t(x)}</li>" for x in dg["tldr"]) + "</ul></div></header>")

    # ---- fix outcome (only once the fixes landed) ----
    if oc:
        w(f"<h2>〇、修正結果（{html.escape(oc['date'])}）</h2>")
        w("<ul>" + "".join(f"<li>{t(x)}</li>" for x in oc["summary"]) + "</ul>")
        w("<h3>修正輪次</h3><div class=\"scroll\"><table><tr><th>輪</th><th>內容</th><th>merge</th><th>審核</th></tr>")
        for rnd, body, merge, review in oc["rounds"]:
            w(f"<tr><td style=\"white-space:nowrap\"><b>{t(rnd)}</b></td><td>{t(body)}</td><td>{t(merge)}</td><td>{t(review)}</td></tr>")
        w("</table></div><h3>驗收</h3><div class=\"scroll\"><table><tr><th>項目</th><th>結果</th></tr>")
        for item, result in oc["verification"]:
            w(f"<tr><td style=\"white-space:nowrap\">{t(item)}</td><td>{t(result)}</td></tr>")
        w("</table></div><h3>有意的畫面改變（修正前後末幀已逐張目視）</h3><ul>"
          + "".join(f"<li>{t(x)}</li>" for x in oc["visual_changes"]) + "</ul>")
        w("<h3>仍未處理（已記錄）</h3><ul>" + "".join(f"<li>{t(x)}</li>" for x in oc["remaining"]) + "</ul>")

    # ---- activities ----
    w("<h2>一、本次做了哪些事</h2><table><tr><th>步驟</th><th>內容</th></tr>")
    for step, body in dg["activities"]:
        w(f"<tr><td style=\"white-space:nowrap\"><b>{t(step)}</b></td><td>{t(body)}</td></tr>")
    w("</table>")

    # ---- numbers ----
    w("<h2>二、數字總覽</h2><div class=\"scroll\"><table><tr><th>片</th><th>讀過檔案</th><th>finding</th>"
      "<th>L1</th><th>L2</th><th>L3</th><th>high</th><th>medium</th><th>low</th></tr>")
    for s in slices:
        fs = s["findings"]
        lv = Counter(f["level"] for f in fs)
        sv = Counter(f["severity"] for f in fs)
        w(f"<tr><td>{t(s['slice'])}</td><td class=\"num\">{len(s['files_reviewed'])}</td><td class=\"num\">{len(fs)}</td>"
          + "".join(f'<td class="num">{lv.get(k, 0)}</td>' for k in (1, 2, 3))
          + "".join(f'<td class="num">{sv.get(k, 0)}</td>' for k in ("high", "medium", "low")) + "</tr>")
    lv = Counter(f["level"] for f in allf)
    sv = Counter(f["severity"] for f in allf)
    w(f"<tr><td><b>合計</b></td><td></td><td class=\"num\"><b>{len(allf)}</b></td>"
      + "".join(f'<td class="num"><b>{lv.get(k, 0)}</b></td>' for k in (1, 2, 3))
      + "".join(f'<td class="num"><b>{sv.get(k, 0)}</b></td>' for k in ("high", "medium", "low")) + "</tr></table></div>")
    w(f"<p class=\"muted\">裁決分布：修 {dcount['fix']}、補文件 {dcount['doc']}、只記錄 {dcount['record']}、"
      f"跨片重複 {dcount['dup']}（併入主條）。稽核方式：主模型重跑重現 "
      f"{sum(dec[f['id']][2] == 'reran' for f in allf)} 條、主模型讀 code 核對 "
      f"{sum(dec[f['id']][2] == 'code' for f in allf)} 條，其餘採審查員附的證據與重現。</p>")

    # ---- decision table ----
    w("<h2>三、裁決總表</h2><p class=\"muted\">點 ID 跳到該條詳情。重複條標出它併入的主條；批次代號見第四節。</p>")
    w("<div class=\"scroll\"><table><tr><th>ID</th><th>等級</th><th>嚴重度</th><th>把握</th><th>標題</th><th>裁決</th><th>批次</th><th>稽核</th>"
      + ("<th>結果</th>" if oc else "") + "</tr>")
    sev_rank = {"high": 0, "medium": 1, "low": 2}
    for f in sorted(allf, key=lambda f: (dec[f["id"]][0] == "dup", f["level"], sev_rank[f["severity"]])):
        d, batch, audit, _ = dec[f["id"]]
        w(f"<tr><td><a href=\"#{f['id']}\"><code>{f['id']}</code></a></td><td>{pill('l%d' % f['level'], LEVEL[f['level']])}</td>"
          f"<td>{pill(f['severity'], f['severity'])}</td><td class=\"muted\">{f['confidence']}</td><td>{t(f['title'])}</td>"
          f"<td>{pill(d, DECISION[d])}</td><td><code>{batch or '—'}</code></td><td class=\"muted\">{AUDIT[audit]}</td>"
          + (f"<td>{result_cell(f['id'])}</td>" if oc else "") + "</tr>")
    w("</table></div>")

    # ---- batches ----
    w("<h2>四、修正批次</h2>")
    w("<div class=\"scroll\"><table><tr><th>批</th><th>主題</th><th>檔案所有權</th><th>findings</th><th>做法重點</th></tr>")
    for key, theme, files, items, how in dg["batches"]:
        w(f"<tr><td><code>{key}</code></td><td>{t(theme)}</td><td>{t(files)}</td><td>{t(items)}</td><td>{t(how)}</td></tr>")
    w("</table></div><h3>派工規則</h3><ul>" + "".join(f"<li>{t(x)}</li>" for x in dg["batch_rules"]) + "</ul>")

    # ---- not fixing / s32 ----
    w("<h2>五、不修／只記錄</h2><table><tr><th>項目</th><th>理由</th></tr>")
    for k, why in dg["not_fixing"]:
        w(f"<tr><td><code>{t(k)}</code></td><td>{t(why)}</td></tr>")
    w("</table>")
    w("<h2>六、§3.2 線待辦（未合併分支擁有的檔，本次不碰）</h2>")
    w("<p class=\"muted\">這些檔在 <code>claude/reverent-lovelace-e56072</code> 上有未合併的改動；由 §3.2 那條線合併時一起改，避免衝突。</p>")
    w("<table><tr><th>來源</th><th>位置</th><th>要改什麼</th></tr>")
    for fid, loc, what in dg["s32_pending"]:
        w(f"<tr><td><a href=\"#{fid}\"><code>{fid}</code></a></td><td>{t(loc)}</td><td>{t(what)}</td></tr>")
    w("</table>")

    # ---- per-slice detail ----
    w("<h2>七、各片詳情</h2>")
    for s in slices:
        w(f"<h3>{t(s['slice'])}</h3>")
        w(f"<p>{t(s['health_summary'])}</p>")
        w(f"<details><summary>未涵蓋的部分與讀過的檔案（{len(s['files_reviewed'])}）</summary>"
          f"<p>{t(s['not_covered'])}</p><p class=\"muted\">"
          + "、".join(f"<code>{html.escape(x['path'])}</code>{'' if x['depth'] == 'full' else '（skim）'}" for x in s["files_reviewed"])
          + "</p></details>")
        for f in s["findings"]:
            d, batch, audit, note = dec[f["id"]]
            w(f"<div class=\"card l{f['level']}\" id=\"{f['id']}\"><h4><code>{f['id']}</code> {t(f['title'])}</h4>")
            w(pill("l%d" % f["level"], LEVEL[f["level"]]) + pill(f["severity"], f["severity"])
              + pill(d, DECISION[d] + (f" · {batch}" if batch else "")) + f"<span class=\"muted\">{f['confidence']} · {html.escape(f['category'])}</span>")
            w("<dl>")
            w(f"<dt>位置</dt><dd><code>{html.escape(f['file'])}:{f['line']}</code></dd>")
            for label, key in (("說明", "description"), ("失敗情境", "failure_scenario"), ("證據", "evidence"),
                               ("重現", "repro"), ("建議修法", "suggested_fix")):
                w(f"<dt>{label}</dt><dd>{t(f[key])}</dd>")
            if f["known_ref"]:
                w(f"<dt>既有記載</dt><dd>{t(f['known_ref'])}</dd>")
            w(f"<dt>稽核</dt><dd><b>{AUDIT[audit]}</b>{'：' + t(note) if note else ''}</dd>")
            r = (oc or {}).get("findings", {}).get(f["id"])
            if r:
                tests = "、".join(f"<code>{html.escape(x)}</code>" for x in r.get("tests", []))
                w(f"<dt>修正結果</dt><dd>{result_cell(f['id'])}<br>{t(r.get('summary', ''))}"
                  + (f"<br><span class=\"muted\">紅→綠測試：</span>{tests}" if tests else "")
                  + (f"<br><span class=\"muted\">回歸審核：</span>{t(r['closure_evidence'])}" if r.get("closure_evidence") else "")
                  + "</dd>")
            w("</dl></div>")

    # ---- limits / regression ----
    w("<h2>八、稽核限制</h2><ul>" + "".join(f"<li>{t(x)}</li>" for x in dg["limits"]) + "</ul>")
    if not oc:
        w("<h2>九、回歸審核</h2><div class=\"note\">本次只審查、未修改任何程式碼，因此沒有回歸審核。"
          "照第四節修正後，回歸審核結果補在這一節（CLAUDE.md：審核 finding 修完後必須回歸審核）。</div>")
    else:
        rg = oc["regression"]
        w("<h2>九、回歸審核</h2>")
        w(f"<p>{t(rg['method'])}</p>")
        w("<table><tr><th>鏡頭</th><th>總評</th></tr>"
          + "".join(f"<tr><td style=\"white-space:nowrap\">{t(k)}</td><td>{t(v)}</td></tr>" for k, v in rg["lenses"])
          + "</table>")
        w("<h3>修正本身帶進的新問題與處理</h3><div class=\"scroll\"><table><tr><th>ID</th><th>等級</th><th>問題</th><th>處理</th></tr>")
        for rid, lvl, title, handling in rg["new_issues"]:
            w(f"<tr><td><code>{html.escape(rid)}</code></td><td>{pill('l%d' % lvl, LEVEL[lvl])}</td><td>{t(title)}</td><td>{t(handling)}</td></tr>")
        w("</table></div>")
    w(f"<p class=\"muted\">由 <code>video/_audit/_gen/{Path(__file__).name}</code> 產生；資料："
      f"<code>{FINDINGS.name}</code>（審查員原始回傳）＋<code>{DIGEST.name}</code>（主模型稽核結論）。</p>")
    w("</div></body></html>")

    args.out.write_text("\n".join(out), encoding="utf-8")
    print(f"wrote {args.out} ({len(allf)} findings, {len(uniq)} unique)")


if __name__ == "__main__":
    main()
