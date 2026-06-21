#!/usr/bin/env python3
"""Generator for the §1.1 Codex aesthetic-polish sign-off report (2026-06-21).

Self-contained HTML (base64-embedded before/after frames + the verbatim Codex
gpt-5.5 verdicts), per CLAUDE.md "打開就能讀" + "凡完成一輪內容撰寫都要產 HTML 報告".

Inputs (all tracked under this _gen dir, so the HTML reproduces from git alone):
  frames_before_codex/<sid>.png   -- frame at the start of this round
  frames_after_codex/<sid>.png    -- frame after the Codex-driven changes
  codex_reviews/before/<sid>.raw.txt , codex_reviews/after/<sid>.raw.txt

Run:  python REVIEW-ch01-codex-polish.gen.py
Out:  ../REVIEW-ch01_inverse_functions-codex-polish.html
"""
from __future__ import annotations
import base64, html, re
from pathlib import Path

HERE = Path(__file__).resolve().parent
BEFORE_DIR = HERE / "frames_before_codex"
AFTER_DIR = HERE / "frames_after_codex"
REV_BEFORE = HERE / "codex_reviews" / "before"
REV_AFTER = HERE / "codex_reviews" / "after"
OUT = HERE.parent / "REVIEW-ch01_inverse_functions-codex-polish.html"

# scene order + display titles (content scenes; intro/outro appended)
SCENES = [
    ("can_we_run_it_backwards", "Running a Function Backwards", "definition_math + hook"),
    ("one_to_one_definition", "One-to-One", "definition_math"),
    ("student_id_is_one_to_one", "A One-to-One Function in Words", "definition_math"),
    ("testing_x_and_x_squared", "Testing f and g", "derivation (2-col)"),
    ("shape_can_mislead", "Same Shape, Opposite Verdicts", "derivation (2-col)"),
    ("horizontal_line_test", "The Horizontal Line Test", "graph (2up)"),
    ("inverse_function_definition", "The Inverse Function", "definition_math"),
    ("inverse_iff_one_to_one", "An Inverse Exists Exactly When One-to-One", "theorem_proof"),
    ("first_inverses", "Computing a Couple of Inverses", "derivation (2-col)"),
    ("composition_identities", "Composition Identities", "graph + hook"),
    ("reflection_across_y_equals_x", "Reflection across y=x", "graph (single) + hook"),
    ("repair_by_restricting", "Restrict, then Invert", "graph (single) + hook"),
    ("finding_the_inverse_strategy", "Finding the Inverse", "procedure_steps"),
    ("inverse_of_a_cubic", "Inverting a Cubic", "derivation (reason-less)"),
    ("inverse_of_a_rational", "Inverting a Rational Function", "derivation (reason-less)"),
    ("inverse_in_an_application", "An Inverse That Answers a Question", "derivation (reason-less)"),
    ("recap", "Section 1.1 — Recap", "recap_cards"),
    ("intro", "Intro", "intro brand frame"),
    ("outro", "Outro", "outro brand frame"),
]

TEMPLATE_CHANGES = [
    ("Center reason-less equation chains", "derivation.py",
     "A pure equation chain (no reason rail, no statement) was left-flush and hugged the "
     "left third, leaving the right ~60% empty. Now centred horizontally (rows still "
     "mutually left-aligned). Fixes the worst left-heavy offenders: cubic / rational / application."),
    ("Spread short content to fill the body zone", "_common.py (fill_gap) + theme.BODY_FILL_FRAC=0.72",
     "Short chains stranded a dead band under the title AND an empty lower third. fill_gap() "
     "opens the inter-row spacing so a short chain occupies ~72% of the zone before placement "
     "(capped so tall chains keep their pitch)."),
    ("Tighten the title->body gap", "theme.BODY_TOP_GAP_MAX 1.0 -> 0.62",
     "With rows now filling the lower zone, a tighter top clamp closes the dead band Codex "
     "flagged on ~12 scenes without stranding content up top. (History: 0.71->1.0 was a "
     "pre-spread gate-1 tune; 0.62 is the post-spread value.)"),
    ("Crisper amber key glow", "brand.text_glow default 2.6/0.5 -> 2.0/0.42; derivation result 3.0/0.45 -> 2.2/0.38",
     "Codex read the amber takeaway glow as fuzzy / embossed on ~6 scenes. Thinner, lower-opacity "
     "halo keeps the gold salient but sharp."),
    ("Brighter reason-rail leaders", "derivation.py leader opacity 0.55 -> 0.7 (result 0.5 -> 0.6)",
     "The dotted leaders binding each step to its rail note read as too faint."),
    ("Lift graph captions off the bottom edge", "graph.py single +0.25->+0.55, 2up +0.3->+0.6",
     "Captions sat ~5px above the safe margin, reading as a footer parked on the edge."),
    ("Softer procedure numerals + pulled-in result column", "procedure_steps.py glow 3.0/0.4 -> 2.4/0.34; RHS pulled in 1.3u",
     "Numerals over-glowed; the result column floated at the far gutter, detached from each step."),
    ("Modest title size reduction", "theme h1 82 -> 78 px",
     "Titles read as over-dominant on several scenes across both review rounds. A ~5% trim "
     "(easily reverted -- one constant). NOTE: affects all decks; flag for review."),
]

PER_SCENE = {
    "horizontal_line_test": "Short parallel captions ('Every height: one crossing.' / 'One height: two crossings.') replacing awkward two-line wraps; caption band lifted.",
    "reflection_across_y_equals_x": "Dim y=x reference label brightened (label_role: text); caption lifted.",
    "repair_by_restricting": "Dim y=x reference label brightened; caption lifted.",
    "inverse_of_a_cubic": "Equation chain now centred horizontally (was left-heavy).",
    "inverse_of_a_rational": "Equation chain now centred horizontally (was left-heavy).",
    "inverse_in_an_application": "Equation chain now centred horizontally (was left-heavy).",
    "inverse_function_definition": "Block lifted toward the title (dead band closed, amber key raised).",
    "one_to_one_definition": "Block lifted toward the title.",
    "student_id_is_one_to_one": "Block lifted toward the title; amber glow crisper.",
    "testing_x_and_x_squared": "Rows spread to fill; rail leaders brighter; block lifted.",
    "shape_can_mislead": "Rows spread to fill; rail leaders brighter; block lifted.",
    "first_inverses": "Rows spread to fill; rail leaders brighter; block lifted.",
    "finding_the_inverse_strategy": "Result column pulled in toward the steps; numeral glow softened.",
    "can_we_run_it_backwards": "Amber glow crisper; title slightly smaller (hook diagram unchanged).",
    "composition_identities": "Amber glow crisper; title slightly smaller.",
    "inverse_iff_one_to_one": "Title slightly smaller (h1 82->78).",
    "recap": "Title slightly smaller (h1 82->78).",
    "intro": "Added the bottom-right watermark to the course-map stage (this thumbnail is the final dark end-slate, so the course-map mark is not visible here).",
    "outro": "Unchanged (light end-slate is a deliberate house treatment).",
}

NON_FINDINGS = [
    ("Outro light 'paper' background", "Codex read it as off-house-style, but the cream end-slate "
     "is a deliberate section-close treatment (REBUILD_STATUS 2026-06-20). Kept."),
    ("Bottom-right summit-bars motif", "Flagged as 'accidental UI residue' on most scenes, but it is "
     "the brand watermark. A dimmed version was trialled; the user reviewed it and chose to keep the "
     "motif at its original prominence (opacity 0.40)."),
    ("'many-to-one' label in red (can_we_run_it_backwards)", "Codex suggested amber; red is correct here "
     "(it marks the collision / failure, not the key takeaway). Kept red."),
]

# Independent gate-1 visual-frame-audit (rubric-based, refute-by-default), run on the
# FINAL frames as a cross-check to the external Codex gate-2 review.
GATE1 = {
    "audited": 17, "confirmed_blocking": 0, "raised_then_refuted": 0,
    "scores": {
        "can_we_run_it_backwards": 84, "composition_identities": 86,
        "finding_the_inverse_strategy": 86, "first_inverses": 86,
        "horizontal_line_test": 86, "inverse_function_definition": 87,
        "inverse_iff_one_to_one": 86, "inverse_in_an_application": 86,
        "inverse_of_a_cubic": 82, "inverse_of_a_rational": 86,
        "one_to_one_definition": 86, "recap": 84,
        "reflection_across_y_equals_x": 85, "repair_by_restricting": 82,
        "shape_can_mislead": 85, "student_id_is_one_to_one": 86,
        "testing_x_and_x_squared": 82,
    },
}

RESIDUAL = [
    "testing / shape reason rail: the roman words inside a rail note (\"on\", \"test\") render slightly "
    "LARGER than the adjacent inline math, a mixed text/inline-math sizing quirk of brand._compose's "
    "x-height alignment (gate-1 A6 ~72, legible/advisory). Template-wide; flagged for a future typography pass.",
    "Definitions now read slightly top-heavy (whitespace pools below). This is the inherent tension of "
    "short 2-block content in a tall frame: round-1 Codex wanted the block UP, round-2 wanted it DOWN. "
    "The current 'title + lede + formula' layout is a clean compromise; not chased further.",
    "Reason-rail TEXT (testing / shape) still reads a touch dim. It is ink_2 on purpose (subordinate to the "
    "bright equations); pushing it brighter would make it compete. Leaders were brightened instead.",
    "Amber salience on testing / shape: their conclusion is a +/- verdict (red cross / green check), not an "
    "amber 'result' row. Amber on a negative verdict would misread, so the verdict glyphs carry salience.",
    "Procedure result column pulled in but still a distinct right column (deliberate 'result at a glance' layout).",
]


def b64(p: Path) -> str | None:
    if not p.exists():
        return None
    return base64.b64encode(p.read_bytes()).decode("ascii")


def clean_review(path: Path) -> str:
    """Final clean answer = from the last 'OVERALL:' to EOF (Codex echoes it twice)."""
    if not path.exists():
        return ""
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    last = max((i for i, ln in enumerate(lines) if ln.startswith("OVERALL:")), default=0)
    return "\n".join(lines[last:]).strip()


def score_of(text: str) -> str:
    m = re.search(r"(\d{2,3})\s*/\s*100", text) or re.search(r"[Ss]core:?\s*(\d{2,3})", text)
    return m.group(1) if m else "—"


def img_tag(data: str | None, alt: str) -> str:
    if data is None:
        return f'<div class="noimg">no frame: {html.escape(alt)}</div>'
    return f'<img loading="lazy" alt="{html.escape(alt)}" src="data:image/png;base64,{data}">'


def main() -> None:
    cards = []
    for sid, title, tmpl in SCENES:
        before = b64(BEFORE_DIR / f"{sid}.png")
        after = b64(AFTER_DIR / f"{sid}.png")
        rb = clean_review(REV_BEFORE / f"{sid}.raw.txt")
        ra = clean_review(REV_AFTER / f"{sid}.raw.txt")
        sb, sa = score_of(rb), (score_of(ra) if ra else "—")
        change = PER_SCENE.get(sid, "")
        rev_after_html = (f'<details><summary>Codex re-review (after) — score {sa}</summary>'
                          f'<pre>{html.escape(ra)}</pre></details>') if ra else \
                         '<p class="muted">Not re-reviewed this round (only the corner motif changed).</p>'
        cards.append(f"""
        <section class="card">
          <h3>{html.escape(title)} <span class="sid">{html.escape(sid)}</span></h3>
          <div class="meta"><span class="tmpl">{html.escape(tmpl)}</span>
            <span class="score">score {sb} &rarr; {sa}</span></div>
          {f'<p class="change"><b>Changed:</b> {html.escape(change)}</p>' if change else ''}
          <div class="ba">
            <figure>{img_tag(before, sid+' before')}<figcaption>before</figcaption></figure>
            <figure>{img_tag(after, sid+' after')}<figcaption>after</figcaption></figure>
          </div>
          <details><summary>Codex review (before) — score {sb}</summary><pre>{html.escape(rb)}</pre></details>
          {rev_after_html}
        </section>""")

    tmpl_html = "\n".join(
        f'<li><b>{html.escape(t)}</b> <code>{html.escape(loc)}</code><br>{html.escape(d)}</li>'
        for t, loc, d in TEMPLATE_CHANGES)
    nonf_html = "\n".join(f'<li><b>{html.escape(t)}</b> — {html.escape(d)}</li>' for t, d in NON_FINDINGS)
    resid_html = "\n".join(f'<li>{html.escape(r)}</li>' for r in RESIDUAL)
    gate1_audited = GATE1["audited"]
    gate1_blocking = GATE1["confirmed_blocking"]
    gate1_refuted = GATE1["raised_then_refuted"]
    gate1_scores = " ".join(
        f'<span class="g1s">{html.escape(s)} <b>{v}</b></span>' for s, v in GATE1["scores"].items())

    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>§1.1 Codex aesthetic polish — sign-off</title>
<style>
 :root{{color-scheme:dark}}
 body{{margin:0;background:#0b0f17;color:#e7ecf3;font:16px/1.6 -apple-system,Segoe UI,Roboto,sans-serif}}
 .wrap{{max-width:1180px;margin:0 auto;padding:32px 22px 80px}}
 h1{{font-size:30px;margin:0 0 4px}} h2{{font-size:21px;margin:38px 0 12px;border-bottom:1px solid #243044;padding-bottom:6px}}
 h3{{font-size:18px;margin:0 0 6px}} .sid{{font:12px ui-monospace,monospace;color:#7da7d9;font-weight:400}}
 .lede{{color:#a9b6c8}}
 .summary{{background:#121a27;border:1px solid #243044;border-radius:10px;padding:14px 18px;margin:14px 0}}
 ul{{margin:8px 0 8px 0;padding-left:20px}} li{{margin:6px 0}}
 code{{background:#1a2333;color:#9fd0ff;padding:1px 6px;border-radius:5px;font-size:12.5px}}
 .card{{background:#0f1622;border:1px solid #223044;border-radius:12px;padding:16px 18px;margin:16px 0}}
 .meta{{display:flex;gap:14px;align-items:center;margin:0 0 8px}}
 .tmpl{{font:12px ui-monospace,monospace;color:#9bb0c9;background:#16202e;padding:2px 8px;border-radius:6px}}
 .score{{font-weight:600;color:#ffd479}}
 .change{{color:#cfe0d4;background:#10211a;border-left:3px solid #3ea66a;padding:6px 12px;border-radius:4px;margin:6px 0}}
 .ba{{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:10px 0}}
 figure{{margin:0}} img{{width:100%;border:1px solid #2a3a52;border-radius:8px;display:block}}
 figcaption{{text-align:center;color:#8aa;font-size:12px;margin-top:4px;text-transform:uppercase;letter-spacing:.08em}}
 .noimg{{padding:40px;text-align:center;color:#667;border:1px dashed #334;border-radius:8px}}
 details{{margin:8px 0;background:#0c131d;border:1px solid #1d2838;border-radius:8px;padding:6px 12px}}
 summary{{cursor:pointer;color:#bcd;font-size:13px}}
 pre{{white-space:pre-wrap;font:12.5px/1.5 ui-monospace,monospace;color:#cdd8e6;margin:8px 0 2px}}
 .muted{{color:#7e8aaa;font-size:13px}}
 .g1{{margin-top:10px;display:flex;flex-wrap:wrap;gap:6px}}
 .g1s{{font:11.5px ui-monospace,monospace;color:#9bb0c9;background:#101a14;border:1px solid #24402e;padding:2px 7px;border-radius:5px}}
 .g1s b{{color:#7fd49a}}
</style></head><body><div class="wrap">
<h1>§1.1 Inverse Functions — Codex aesthetic / layout polish</h1>
<p class="lede">Per-scene review by <b>Codex (gpt-5.5, xhigh)</b> on rendered frames &rarr; fixes applied &rarr;
regression re-review. 2026-06-21. All offline / mock render; the only billed calls are the Codex reviews
(explicitly requested).</p>
<div class="summary">
 <b>Outcome:</b> 0 blocking issues across all 19 scenes in both rounds (pure aesthetic polish).
 Recurring findings were promoted to <b>template fixes</b>; per-scene items handled in the storyboard.
 Regression scores mostly rose or held (rational 78&rarr;84, application 78&rarr;86, one-to-one 82&rarr;86,
 reflection 84&rarr;86, can-we 82&rarr;86, first-inverses 78&rarr;82); none regressed below baseline on a
 real issue. Independent gate-1 visual-frame-audit cross-check (below) agrees: 0 blocking.
</div>

<div class="summary" style="border-color:#2c4a36">
 <b>Dual-gate verdict.</b> <b>Gate-2 (Codex gpt-5.5, external):</b> 0 blocking across 19 scenes, both rounds.
 <b>Gate-1 (visual-frame-audit, internal rubric, refute-by-default):</b> {gate1_audited} content scenes,
 <b>{gate1_blocking} confirmed blocking</b>, {gate1_refuted} raised-then-refuted; aesthetic 82&ndash;87.
 Two independent reviewers, zero blocking issues &mdash; the polish is purely additive.
 <div class="g1">{gate1_scores}</div>
</div>

<h2>Template changes (recurring findings &rarr; templates)</h2>
<ul>{tmpl_html}</ul>

<h2>Per-scene before &rarr; after</h2>
{''.join(cards)}

<h2>Treated as non-findings (deliberate design)</h2>
<ul>{nonf_html}</ul>

<h2>Residual advisories (left as-is, with rationale)</h2>
<ul>{resid_html}</ul>
</div></body></html>"""
    OUT.write_text(doc, encoding="utf-8")
    print(f"wrote {OUT}  ({OUT.stat().st_size//1024} KB)")


if __name__ == "__main__":
    main()
