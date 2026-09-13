"""worked_example_template.gen.py -- worked_example 模板落地驗收報告 -> self-contained HTML.

    python video/_audit/_gen/worked_example_template.gen.py \
        [--digest _gen/worked_example_template.digest.json] \
        [--frames <repo>/video/output/_qa/worked_example] \
        [--gates <dir with _demo_worked_example.{schema,lint,sizecheck}.txt>] \
        [--out ../REVIEW-worked-example-template-applied.html]

讀 digest（全部資料；繁體中文，照登不改字）＋試點場 storyboard（逐拍旁白，由 `say:` 依
`{show X}` marker 切段）＋四場末幀／mockup／逐拍幀（PNG，base64 內嵌）＋（可選）demo deck
三份閘輸出原文。純 stdlib + PIL + PyYAML。報告文字繁體中文；引文／識別碼／檔名保留原文
（CLAUDE.md）。本產生器不下判斷、不改寫 digest 的結論——所有評語逐字取自 digest。
"""
from __future__ import annotations

import argparse
import base64
import html
import io
import re
import subprocess
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
STORYBOARD = REPO / "video/storyboards/_demo_worked_example.yml"
PILOT_SCENE_ID = "companion_limit_example"

# 四場末幀：檔名 -> (場 id 顯示, 它驗的條款；照 _demo_worked_example.yml 檔頭註解)
FINAL_FRAMES = [
    ("companion_limit_example.png", "companion_limit_example",
     "完整形狀（照 mockup：題目＋策略 rail＋notes＋答案框；取材 §3.1 Example 3.1 伴隨極限）"),
    ("no_rail.png", "no_rail",
     "無 rail（D8：無 strategy／notes → 步驟欄吃滿 CONTENT_W）"),
    ("capacity_over.png", "capacity_over",
     "容量超量（L2 預測式拆頁 warn；刻意的壓測 fixture，畫面溢出是預期）"),
    ("multipage_p1.png", "multipage_p1",
     "分頁續頁（D4 例外：part 1/2 且無 result，續頁答案還沒到）"),
]

# 試點場逐拍幀：檔名 -> reveal id（None 表開場拍，之前無 {show} marker）
PILOT_BEATS = [
    ("00_open.png", None),
    ("01_strategy.png", "strategy"),
    ("02_step.0.png", "step.0"),
    ("03_step.1.png", "step.1"),
    ("04_note.0.png", "note.0"),
    ("05_note.1.png", "note.1"),
    ("06_result.png", "result"),
]

GATE_FILES = [
    ("schema", "_demo_worked_example.schema.txt"),
    ("lint", "_demo_worked_example.lint.txt"),
    ("sizecheck", "_demo_worked_example.sizecheck.txt"),
]


def esc(s) -> str:
    return html.escape(str(s if s is not None else ""), quote=False)


def git_short_head() -> str:
    try:
        out = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=REPO,
                              capture_output=True, text=True, check=True, timeout=10)
        return out.stdout.strip() or "（未知）"
    except Exception:
        return "（未知）"


def img_b64(path: Path, width: int = 1100) -> str | None:
    if not path.exists():
        return None
    from PIL import Image
    im = Image.open(path).convert("RGB")
    if im.width > width:
        im = im.resize((width, int(im.height * width / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=78, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode("ascii")


def placeholder_svg(label: str) -> str:
    return (f'<svg viewBox="0 0 1100 619" xmlns="http://www.w3.org/2000/svg" role="img" '
            f'aria-label="missing: {esc(label)}">'
            f'<rect width="1100" height="619" fill="#d8dee9"/>'
            f'<text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" '
            f'font-family="ui-monospace,Consolas,monospace" font-size="20" fill="#5a6b85">'
            f'（缺圖：{esc(label)}）</text></svg>')


def img_tag(path: Path, alt: str, width: int = 1100) -> str:
    b64 = img_b64(path, width)
    if b64 is None:
        return placeholder_svg(str(path.name))
    return f'<img src="{b64}" alt="{esc(alt)}">'


def read_gate(gates_dir: Path | None, fname: str) -> str | None:
    if gates_dir is None:
        return None
    p = gates_dir / fname
    if not p.exists():
        return None
    text = p.read_text(encoding="utf-8", errors="replace")
    if "sizecheck" in fname:
        keep = []
        for line in text.splitlines():
            if line.startswith("[sizecheck]") or line.startswith("  SIZE") or \
               line.startswith("  WARN") or line.startswith("exit="):
                keep.append(line)
        text = "\n".join(keep)
    return text


def load_pilot_say() -> str:
    doc = yaml.safe_load(STORYBOARD.read_text(encoding="utf-8"))
    for scene in doc["scenes"]:
        if scene["id"] == PILOT_SCENE_ID:
            return scene["say"]
    raise SystemExit(f"scene {PILOT_SCENE_ID} not found in {STORYBOARD}")


def split_beats(say: str) -> dict[str, str]:
    """{marker id (None = 開場): narration text}, split on `{show X}` markers."""
    parts = re.split(r"\{show ([^}]+)\}", say)
    out: dict[str, str] = {None: " ".join(parts[0].split())}
    for i in range(1, len(parts), 2):
        marker, text = parts[i], parts[i + 1]
        out[marker] = " ".join(text.split())
    return out


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
.tldr p{margin:.4em 0;color:#e6edf3}.tldr b{color:#7ee0a8}
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
.chip.ok{color:var(--good);background:var(--goodbg);border-color:#bfe3cf}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 18px;margin:12px 0}
.card b.rec{color:var(--ok)}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.grid2 figure{margin:0;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px}
.grid2 figure img,.grid2 figure svg{width:100%;height:auto;border-radius:6px;border:1px solid var(--line)}
.grid2 figcaption{font-size:12.5px;color:var(--muted);margin-top:6px}
.beats{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px}
.beats figure{margin:0;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px}
.beats figure img,.beats figure svg{width:100%;height:auto;border-radius:6px;border:1px solid var(--line)}
.beats figcaption{font-size:12.5px;margin-top:6px}
.beats figcaption .say{color:var(--ink);display:block;margin-top:3px}
.finalframes{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:16px}
.finalframes figure{margin:0;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px}
.finalframes figure img,.finalframes figure svg{width:100%;height:auto;border-radius:6px;border:1px solid var(--line)}
.finalframes figcaption{font-size:12.5px;color:var(--muted);margin-top:6px}
details{margin:8px 0}summary{cursor:pointer;font-weight:600}
pre{background:#0f1830;color:#d7e2f5;border-radius:8px;padding:12px 14px;overflow-x:auto;font:12.5px/1.55 ui-monospace,Consolas,monospace;white-space:pre-wrap}
.small{font-size:12.5px;color:var(--muted)}
ul,ol{margin:6px 0;padding-left:22px}li{margin:4px 0}
.foot{margin-top:30px;font-size:12.5px;color:var(--muted);font-style:italic}
"""


def render_decisions(decisions: list[dict]) -> str:
    out = ["<h2>一、交裁決</h2>"]
    for d in decisions:
        out.append(f'<div class="card"><h3>{esc(d["id"])} {esc(d["title"])}</h3>'
                    f'<p>{esc(d["body"])}</p>'
                    f'<p><b class="rec">建議：</b>{esc(d["recommendation"])}</p></div>')
    return "\n".join(out)


def render_mockup_vs_final(frames_dir: Path, decisions: list[dict], judgments: list[dict]) -> str:
    mockup = frames_dir / "mockup_1080.png"
    final = frames_dir / "companion_limit_example.png"
    dev3 = decisions[2]  # id ③：兩處刻意偏離 + masthead 樣式
    j4 = next(j for j in judgments if j["n"] == 4)
    out = ["<h2>二、mockup vs 成品</h2>",
           '<div class="grid2">',
           f'<figure>{img_tag(mockup, "mockup_1080.png")}'
           f'<figcaption><b>mockup</b>（{esc(mockup.name)}；字型為 Chrome fallback，非最終字型）</figcaption></figure>',
           f'<figure id="mockup-compare-final">{img_tag(final, "companion_limit_example.png")}'
           f'<figcaption><b>成品</b>（{esc(final.name)}；IBM Plex Sans＋Latin Modern，1080p）</figcaption></figure>',
           "</div>",
           "<h3>對照要點</h3><ul>",
           f'<li><b>{esc(dev3["title"])}：</b>{esc(dev3["body"])}</li>',
           f'<li><b>{esc(j4["what"])}：</b>{esc(j4["why"])}</li>',
           "</ul>"]
    return "\n".join(out)


def render_pilot_beats(frames_dir: Path) -> str:
    say = load_pilot_say()
    narration = split_beats(say)
    out = ["<h2>三、試點場逐拍幀（<code>companion_limit_example</code>）</h2>",
           '<p class="small">§3.1 Example 3.1（伴隨極限），mock render 480p 抽幀；旁白依 <code>{show X}</code> '
           f'marker 切段，取自 <code>{esc(STORYBOARD.relative_to(REPO).as_posix())}</code> 的 <code>say:</code>。</p>',
           '<div class="beats">']
    beats_dir = frames_dir / "beats"
    for i, (fname, marker) in enumerate(PILOT_BEATS):
        text = narration.get(marker, "")
        label = f"beat {i:02d} · 開場（無 {{show}} marker）" if marker is None else f"beat {i:02d} · {{show {marker}}}"
        out.append(f'<figure>{img_tag(beats_dir / fname, fname)}'
                    f'<figcaption><b>{esc(label)}</b><span class="say">{esc(text)}</span></figcaption></figure>')
    out.append("</div>")
    return "\n".join(out)


def render_final_frames(frames_dir: Path) -> str:
    out = ["<h2>四、四場末幀</h2>", '<div class="finalframes">']
    for fname, scene_id, note in FINAL_FRAMES:
        if scene_id == PILOT_SCENE_ID:
            # 已在「二、mockup vs 成品」嵌過同一張圖（避免重複內嵌 base64），此處連結回去。
            body = ('<div class="small" style="padding:20px 0">'
                    '（同一張圖，見上方「二、mockup vs 成品」的「成品」欄'
                    '　<a href="#mockup-compare-final">跳至該圖</a>）</div>')
        else:
            body = img_tag(frames_dir / fname, fname)
        out.append(f'<figure>{body}<figcaption><code>{esc(scene_id)}</code><br>{esc(note)}</figcaption></figure>')
    out.append("</div>")
    return "\n".join(out)


def render_contract(rows: list[list[str]]) -> str:
    out = ["<h2>五、契約 D1–D14 逐條</h2>",
           "<table><thead><tr><th>條款</th><th>內容</th><th>狀態</th></tr></thead><tbody>"]
    for cid, desc, status in rows:
        out.append(f"<tr><td><code>{esc(cid)}</code></td><td>{esc(desc)}</td><td>{esc(status)}</td></tr>")
    out.append("</tbody></table>")
    return "\n".join(out)


VERIFICATION_LABELS = [
    ("selftests", "selftest"),
    ("gates_identical", "既有 22 個 deck 的 gate 輸出"),
    ("smoke_identical", "doctor --smoke"),
    ("demo_gates", "demo deck 本身的 gate"),
    ("mock_render", "mock render 抽幀自檢"),
    ("billing", "計費／連網"),
]


def render_verification(verification: dict, gates_dir: Path | None) -> str:
    out = ["<h2>六、閘與零行為改變證據</h2>", "<table><thead><tr><th>項目</th><th>結果</th></tr></thead><tbody>"]
    for key, label in VERIFICATION_LABELS:
        if key in verification:
            out.append(f"<tr><td>{esc(label)}</td><td>{esc(verification[key])}</td></tr>")
    out.append("</tbody></table>")
    if gates_dir is None:
        out.append('<p class="note">未提供 <code>--gates</code>，略過 demo deck 三份閘輸出原文。</p>')
        print("[warn] --gates not given, skipping demo deck gate output verbatim section")
    else:
        out.append("<h3>demo deck（<code>_demo_worked_example.yml</code>）三份閘輸出原文</h3>")
        for kind, fname in GATE_FILES:
            text = read_gate(gates_dir, fname)
            if text is None:
                out.append(f'<p class="note">找不到 <code>{esc(fname)}</code>（於 <code>{esc(str(gates_dir))}</code>）。</p>')
                print(f"[warn] gate file missing: {gates_dir / fname}")
            else:
                out.append(f"<details open><summary>{esc(kind)}</summary><pre>{esc(text)}</pre></details>")
    return "\n".join(out)


def render_judgments(judgments: list[dict]) -> str:
    out = ["<h2>七、子代理判斷與主模型覆核</h2>"]
    for j in judgments:
        out.append(f'<div class="card"><h3>判斷 {j["n"]}</h3>'
                    f'<p><b>做了什麼：</b>{esc(j["what"])}</p>'
                    f'<p><b>為什麼：</b>{esc(j["why"])}</p>'
                    f'<p><b>覆核：</b>{esc(j["verdict"])}</p></div>')
    return "\n".join(out)


def render_tail(advisories: list[str], files: list[list[str]], not_done: list[str]) -> str:
    out = ["<h2>八、advisory</h2><ul>"]
    out += [f"<li>{esc(a)}</li>" for a in advisories]
    out.append("</ul>")
    out.append("<h2>九、改動檔案</h2><table><thead><tr><th>檔案</th><th>說明</th></tr></thead><tbody>")
    for path, desc in files:
        out.append(f"<tr><td><code>{esc(path)}</code></td><td>{esc(desc)}</td></tr>")
    out.append("</tbody></table>")
    out.append("<h2>十、未做／另案</h2><ul>")
    out += [f"<li>{esc(n)}</li>" for n in not_done]
    out.append("</ul>")
    return "\n".join(out)


def render(digest: dict, frames_dir: Path, gates_dir: Path | None) -> str:
    commits = dict(digest["commits"])
    commits["closing"] = git_short_head()
    parts = [f"""<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>{esc(digest['title'])}</title>
<script>window.MathJax={{tex:{{inlineMath:[['$','$']],displayMath:[['$$','$$']]}},svg:{{fontCache:'global'}}}};</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js" async></script>
<style>{CSS}</style></head><body><div class="wrap">
<header class="top"><div class="eyebrow">video · worked_example template · acceptance</div>
<h1>{esc(digest['title'])}</h1>
<div class="sub">kickoff：<code>{esc(digest['kickoff'])}</code>　mockup：<code>{esc(digest['mockup'])}</code></div>
<div class="meta"><span>日期：{esc(digest['date'])}</span>
<span>commit kickoff <code>{esc(commits['kickoff'])}</code></span>
<span>template <code>{esc(commits['template'])}</code></span>
<span>closing <code>{esc(commits['closing'])}</code></span></div>
<div class="tldr"><p><b>一句話：</b>{esc(digest['one_line'])}</p></div></header>
"""]
    parts.append(render_decisions(digest["decisions_for_user"]))
    parts.append(render_mockup_vs_final(frames_dir, digest["decisions_for_user"], digest["agent_judgments"]))
    parts.append(render_pilot_beats(frames_dir))
    parts.append(render_final_frames(frames_dir))
    parts.append(render_contract(digest["contract_rows"]))
    parts.append(render_verification(digest["verification"], gates_dir))
    parts.append(render_judgments(digest["agent_judgments"]))
    parts.append(render_tail(digest["advisories"], digest["files"], digest["not_done"]))
    parts.append('<p class="foot">本報告由 <code>video/_audit/_gen/worked_example_template.gen.py</code> '
                  "從 <code>worked_example_template.digest.json</code> 產生；文字逐字取自 digest，不另加評語。"
                  "</p></div></body></html>")
    return "\n".join(parts)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--digest", type=Path, default=HERE / "worked_example_template.digest.json")
    ap.add_argument("--frames", type=Path, default=REPO / "video/output/_qa/worked_example")
    ap.add_argument("--gates", type=Path, default=None)
    ap.add_argument("--out", type=Path, default=REPO / "video/_audit/REVIEW-worked-example-template-applied.html")
    args = ap.parse_args()

    import json
    digest = json.loads(args.digest.read_text(encoding="utf-8"))
    html_out = render(digest, args.frames, args.gates)
    args.out.write_text(html_out, encoding="utf-8")
    print(f"wrote {args.out} ({args.out.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
