"""Generator for the §1.1 render + overflow sign-off report (2026-06-20 續).

Self-contained standalone HTML (base64-embedded end-state frames + MathJax CDN),
per CLAUDE.md "含圖 HTML 報告一律 base64 self-contained". Frames live in the
gitignored output/ tree; re-render (make.py --scene all --backend mock) + re-extract
(critic.py --dry-run), then re-run this generator to regenerate the report.

    python video/content_scripts/_audit/_gen/REVIEW-ch01_inverse_functions-s11-render-overflow.gen.py
"""
from __future__ import annotations

import base64
import io
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[4]
FRAMES = ROOT / "video" / "output" / "ch01" / "s1.1" / "critic" / "frames"
OUT = ROOT / "video" / "content_scripts" / "_audit" / "REVIEW-ch01_inverse_functions-s11-render-overflow.html"

# (frame_dir, heading, caption-with-$math$)
FIXED = [
    ("09_inverse_iff_one_to_one", "Overflow fix · QED (theorem_proof)",
     "Two proof steps tightened to single lines; the green QED line "
     "rose from bottom-y $-3.92$ to $-3.08$ (safe margin $-3.45$) — comfortably in-frame."),
    ("18_recap", "Overflow fix · recap point 4 (+ Pango-crash reword)",
     "Point 4 dropped \"then\" (bottom-y $-3.81\\to-3.27$) and swapped the "
     "\"(check …)\" parenthetical for an em-dash to dodge the Inter-Tight $\\texttt{(check}$ "
     "empty-SVG crash. Renders clean, in-margin."),
]
HOOKS = [
    ("02_can_we_run_it_backwards", "Hook 1 · two-in/one-out mapping",
     "$f(x)=x$ maps each input to itself (cyan, one-to-one); $g(x)=x^2$ sends "
     "$\\tfrac12$ and $-\\tfrac12$ both to $\\tfrac14$ (orange) — labelled \"many-to-one\"."),
    ("07_horizontal_line_test", "Hook 2 · HLT sweep (graph mode:2up)",
     "Left $y=x$: one crossing (green check). Right $y=x^2$: two crossings (red cross). "
     "The $\\texttt{graph\\ mode:2up}$ conversion preserved $\\texttt{left/right.plot.N}$."),
    ("11_composition_identities", "Hook 3 · A↔B round trip",
     "$x$ rides arc $f$ (cyan) to $f(x)$ in $B$, returns via arc $f^{-1}$ (orange) to "
     "the same $x$ in $A$; both identities $f^{-1}(f(x))=x$, $f(f^{-1}(y))=y$ shown."),
    ("12_reflection_across_y_equals_x", "Hook 4 · fold x³ over y=x (graph mode:single)",
     "$y=x^3$ (cyan) folds across $y=x$ onto $y=\\sqrt[3]{x}$ (orange); the "
     "$(a,b)\\leftrightarrow(b,a)$ mirror point pair is marked."),
    ("13_repair_by_restricting", "Hook 5 · reflect right arm → √x (graph mode:single)",
     "The restricted right arm of $f(x)=x^2$ reflects across $y=x$ onto "
     "$f^{-1}(x)=\\sqrt{x}$ (positive root)."),
]

# VLM gate1 verdict (Workflow wf_b83ff82d-d59): all 17 content scenes in-frame-and-safe.
SCENES_17 = [
    "can_we_run_it_backwards", "one_to_one_definition", "student_id_is_one_to_one",
    "testing_x_and_x_squared", "shape_can_mislead", "horizontal_line_test",
    "inverse_function_definition", "inverse_iff_one_to_one", "first_inverses",
    "composition_identities", "reflection_across_y_equals_x", "repair_by_restricting",
    "finding_the_inverse_strategy", "inverse_of_a_cubic", "inverse_of_a_rational",
    "inverse_in_an_application", "recap",
]


def b64_frame(frame_dir: str, max_w: int = 1040) -> str:
    p = FRAMES / frame_dir / "final.png"
    if not p.exists():
        return ""
    img = Image.open(p).convert("RGB")
    if img.width > max_w:
        img = img.resize((max_w, round(img.height * max_w / img.width)), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def card(frame_dir, heading, caption) -> str:
    src = b64_frame(frame_dir)
    img = f'<img src="{src}" alt="{frame_dir}">' if src else \
        f'<div class="missing">frame {frame_dir} not found — re-render + critic --dry-run</div>'
    return (f'<div class="card"><h3>{heading}</h3>{img}'
            f'<p class="cap">{caption}</p><p class="fid">{frame_dir}/final.png</p></div>')


def build() -> str:
    fixed = "\n".join(card(*c) for c in FIXED)
    hooks = "\n".join(card(*c) for c in HOOKS)
    rows = "\n".join(
        f'<tr><td>{i+2:02d}</td><td>{s}</td><td class="ok">in-frame-and-safe</td></tr>'
        for i, s in enumerate(SCENES_17))
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>§1.1 Render + Overflow Sign-off (2026-06-20)</title>
<script>MathJax={{tex:{{inlineMath:[['$','$']]}}}};</script>
<script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<style>
  :root{{--bg:#0d1117;--panel:#161b22;--ink:#e6edf3;--dim:#8b949e;--ok:#3fb950;
        --warn:#d29922;--accent:#58a6ff;--line:#30363d;}}
  *{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--ink);
    font:15px/1.65 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;padding:34px}}
  .wrap{{max-width:1080px;margin:0 auto}}
  h1{{font-size:25px;margin:0 0 4px}} .sub{{color:var(--dim);margin:0 0 22px}}
  h2{{font-size:18px;border-bottom:1px solid var(--line);padding-bottom:6px;margin:34px 0 14px}}
  h3{{font-size:14px;color:var(--accent);margin:0 0 8px;font-weight:600}}
  .verdict{{background:var(--panel);border:1px solid var(--line);border-left:4px solid var(--ok);
    border-radius:8px;padding:14px 18px;margin:0 0 8px}}
  .verdict b{{color:var(--ok)}}
  ul{{margin:8px 0}} li{{margin:3px 0}}
  .card{{background:var(--panel);border:1px solid var(--line);border-radius:10px;
    padding:14px;margin:0 0 18px}}
  .card img{{width:100%;border-radius:6px;display:block;border:1px solid var(--line)}}
  .cap{{color:var(--ink);margin:10px 2px 2px}} .fid{{color:var(--dim);font:12px monospace;margin:2px}}
  .missing{{color:var(--warn);padding:30px;text-align:center;border:1px dashed var(--warn);border-radius:6px}}
  table{{width:100%;border-collapse:collapse;margin:6px 0;font-size:13px}}
  td,th{{border:1px solid var(--line);padding:5px 9px;text-align:left}}
  th{{background:var(--panel)}} td.ok{{color:var(--ok)}}
  code{{background:#1f2630;padding:1px 5px;border-radius:4px;font-size:12px}}
  .warn{{color:var(--warn)}} .grid{{}}
</style></head><body><div class="wrap">
<h1>§1.1 Inverse Functions — Render + Overflow Sign-off</h1>
<p class="sub">2026-06-20 · Direction D 收尾 · mock render (offline, no billed API) · gate1 VLM audit <code>wf_b83ff82d-d59</code></p>

<div class="verdict"><b>VERDICT: 0 confirmed visual blockings · 17/17 content scenes in-frame-and-safe.</b>
Full §1.1 mock 成片 rendered end-to-end (make.py EXIT 0): h264 1920×1080, 30fps, 769s ≈ 12:49,
19 scenes + 5 custom hooks composed. Tasks ①②③ complete.</div>

<h2>Tasks</h2>
<ul>
<li><b>① Full mock 成片 — hooks end-to-end:</b> 19 scenes + 5 hooks rendered &amp; composed; all hook
  reveal-id contracts survived the <code>graph_focus/compare → graph</code> conversion (graph.py is a thin dispatcher). ✓</li>
<li><b>② Regenerate <code>_mimo</code>:</b> spoken.yml markers synced (<code>math.N→step.N/check</code>, <code>takeaway</code> removed),
  <code>derive_spoken --deck</code> parity OK, <code>_mimo.yml</code> + <code>_narration_spoken.md</code> regenerated. MiMo TTS synthesis still deferred. ✓</li>
<li><b>③ Per-scene overflow:</b> QED + recap overflows fixed; all 17 scenes confirmed in-frame-and-safe. ✓</li>
</ul>

<h2>Overflow fixes (task ③)</h2>
{fixed}

<h2>Hook end-states (task ① — graph conversion did not break the animations)</h2>
{hooks}

<h2>3 regressions the full render surfaced (the representative-scene render missed; all fixed)</h2>
<ul>
<li><b>recap <code>(check</code> → manimpango empty-SVG crash (deterministic):</b> in Inter Tight, the isolated
  token <code>Text("(check")</code> shapes to an empty SVG → <code>ParseError</code> → recap fails to build → blocks the whole render.
  Astonishingly narrow (<code>"(chec"</code>, <code>"(check)"</code>, default font all fine; the TTF <em>has</em> the <code>(</code> glyph).
  Fixed by rewording the on-screen recap payload (em-dash). <span class="warn">⚠ Latent landmine: any isolated <code>(word</code>
  token in Inter-Tight prose could crash a render; a robust fix (defensive <code>_compose</code> guard / font re-instance) is
  shared-infra and is surfaced for your decision, not done this round.</span></li>
<li><b>sizecheck mixed-prose sibling-size false positive (Direction-D <code>_compose</code>):</b> inline <code>$math$</code> is
  x-height-matched (CM font_size ≈ 1.61× text) but <code>_norm_size</code> normalised by <code>TEX_TEXT_SCALE</code> (1.42),
  so math-bearing prose lines over-measured → mixed sibling groups (<code>point</code>/<code>step</code>) falsely flagged → aborts render.
  Fixed <code>sizecheck._block_prose_size</code> to compare only Text / prose_tex carriers (skip pure inline-math lines; a real shrink still shrinks the Text).</li>
<li><b>QED + recap overflow:</b> the geometry/font enlargement pushed both past the bottom safe margin (see fixes above).</li>
</ul>

<h2>Advisory (surfaced, not fixed — outside the 3 tasks)</h2>
<ul>
<li><b>derivation reason-rail text↔math spacing</b> (<code>testing_x_and_x_squared</code>, <code>shape_can_mislead</code>): the
  roman word abuts inline math with a tight gap (e.g. "factor h(x)", "+4 one-to-one"), more visible after the enlargement.
  Readable but cramped; a <code>_compose</code> text/math boundary-spacing item at the <b>template level</b> (affects all derivation
  reason rails incl. §1.2). Other advisories are cosmetic (A1 upper whitespace, A7 dim labels).</li>
</ul>

<h2>VLM gate1 verdict — per scene (overflow)</h2>
<table><tr><th>#</th><th>scene</th><th>overflow</th></tr>
{rows}
</table>
<p class="sub">17 <code>visual-frame-audit</code> agents + refute-by-default verification · 0 confirmed blockings ·
50 advisories (mostly clean-confirmations / cosmetic). Frames: <code>output/ch01/s1.1/critic/frames/NN_&lt;id&gt;/final.png</code> (gitignored).</p>
</div></body></html>"""


def main() -> int:
    OUT.write_text(build(), encoding="utf-8")
    n = sum(1 for c in FIXED + HOOKS if (FRAMES / c[0] / "final.png").exists())
    print(f"[gen] wrote {OUT}  ({n}/{len(FIXED)+len(HOOKS)} frames embedded)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
