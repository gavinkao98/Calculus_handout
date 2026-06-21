"""Generator: §1.1 scene-by-scene visual polish round -> SELF-CONTAINED HTML.

A visual-tuning pass over every ch01_inverse_functions scene (2026-06-21): each
content scene was re-rendered (mock) and frame-checked, three template-level
fixes were distilled from the per-scene tweaks, and three storyboard titles were
reworded. This report shows the final state of all 17 content scenes with a note
on what was tuned, the three generalised template changes, and two concrete
before/after pairs (the cases _verify/ had a pre-round frame for).

PORTABILITY CONTRACT (see video/README.md §資料夾架構與版控策略):
  Every frame is base64-embedded (downscaled via Pillow) — zero external image
  refs, so the HTML renders after a fresh clone even though output/ is gitignored.
  This generator + its before-frame copies live under _gen/ (tracked).

Frame sources:
  - critic/frames/<nn>_<scene>/final.png : live mock render (re-run §1.1 to regen).
  - ./frames_before_polish/<scene>.png   : pre-round evidence copied from the
    _verify/ snapshot (irreproducible once output/ is wiped -> tracked here).
"""
from __future__ import annotations
import base64
import html
import io
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
OUT = HERE.parent / "REVIEW-ch01_inverse_functions-scene-polish.html"
FRAMES_LIVE = REPO / "video" / "output" / "ch01" / "s1.1" / "critic" / "frames"
FRAMES_BEFORE = HERE / "frames_before_polish"
MAX_W = 1100

_CACHE: dict[str, str] = {}


def _uri(p: Path) -> str | None:
    key = str(p)
    if key in _CACHE:
        return _CACHE[key]
    if not p.exists():
        return None
    im = Image.open(p).convert("RGB")
    if im.width > MAX_W:
        im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format="JPEG", quality=86)
    uri = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode("ascii")
    _CACHE[key] = uri
    return uri


def _img(p: Path, alt: str) -> str:
    u = _uri(p)
    if u is None:
        return f'<div class="missing">frame missing: {html.escape(alt)}</div>'
    return f'<img src="{u}" alt="{html.escape(alt)}" loading="lazy">'


# ---- the three generalised template changes -----------------------------
TEMPLATE_CHANGES = [
    ("A — Body placement: kill the dead band above content",
     "definition_math / derivation centred their content in the whole "
     "title→bottom zone, so short content drifted to ~y=−0.6 (below the frame "
     "centre) and read as detached from the title. New shared helper "
     "<code>_common.place_body()</code> centres the content BUT clamps the "
     "title→content gap to <code>theme.BODY_TOP_GAP_MAX</code> (~1.0u): short "
     "content settles near the frame centre (a touch high, to honour the title "
     "above), medium content centres, tall content still fills the full zone. "
     "Wired into definition_math + derivation — ~11 scenes. (The clamp was tuned "
     "from 0.71→1.0 after the gate-1 audit flagged several short scenes as "
     "top-heavy at 0.71.)"),
    ("B — Inline math in display headings no longer towers",
     "x-height-matched heading math sat 1.4–1.7× the bold cap height for simple "
     "f(x)=xⁿ and 3.1× for a \\dfrac — a title read as 'tiny words + huge "
     "formula'. <code>_compose(math_scale_mul=)</code> + "
     "<code>theme.HEADING_MATH_SCALE</code> (0.78) rein the math in for headings "
     "only (body prose keeps full x-height match). Plus three titles reworded to "
     "drop a formula that was redundant with the first body line or too tall to "
     "set inline (scenes 05, 15, 16)."),
    ("C — Verdict placement + reason-rail readability",
     "graph 2-up verdict ✓/✗ was <code>next_to(cap, RIGHT)</code>, so on a "
     "wrapped 2-line caption it floated at the vertical middle of the right "
     "margin. Now stacked centred ABOVE the caption, under its panel — it reads "
     "as that panel's punchline. And the derivation reason rail moved from "
     "<code>muted</code> (ink_3) to <code>text</code> (ink_2): the rail carries "
     "real reasoning and the project lint flagged muted as 'too faint for "
     "teaching content'; italic + the dotted leader keep it subordinate."),
]

# ---- per-scene final state + tuning note --------------------------------
# (scene_number, scene_id, template, note)
SCENES = [
    (2, "can_we_run_it_backwards", "definition_math + hook",
     "Fix A: the prose line + the two mapping diagrams sit in the upper-middle, "
     "anchored to the title (was floating). Hook diagrams unaffected."),
    (3, "one_to_one_definition", "definition_math",
     "Fix A: statement + math anchored below the title (was floating at dead "
     "centre with a large band between title and content). See before/after."),
    (4, "student_id_is_one_to_one", "definition_math",
     "Fix A: the 3 short lines now sit just under the title instead of floating "
     "low in the frame."),
    (5, "testing_x_and_x_squared", "derivation",
     "Title reworded 'Testing $f(x)=x$ and $g(x)=x^2$' → 'Testing $f$ and $g$' "
     "(the inline definitions towered and broke the baseline; the full defs live "
     "in the reason rail). Fix A + brighter rail."),
    (6, "shape_can_mislead", "derivation",
     "Fix A (content pulled up) + reason rail muted→text so the 'factor…', "
     "'h(0)=h(2)=0', 'one-to-one' reasoning is readable."),
    (7, "horizontal_line_test", "graph 2-up + hook",
     "Verdict ✓/✗ stacked above each caption, centred under its panel (was "
     "floating in the right margin of the wrapped caption). See before/after."),
    (8, "inverse_function_definition", "definition_math",
     "Fix A: prose + the two math lines anchored to the title."),
    (9, "inverse_iff_one_to_one", "theorem_proof",
     "No change — theorem_proof already top-anchors its statement card and "
     "cascades the proof; balanced. Included for a clean high-res check."),
    (10, "first_inverses", "derivation",
     "Fix A + brighter reason rail ('is its own inverse', 'set y=x³…', 'check by "
     "composing')."),
    (11, "composition_identities", "definition_math + hook",
     "Fix A pulled the prose up; the hook's A→B mapping diagram + the two "
     "identity lines are unaffected and balanced."),
    (12, "reflection_across_y_equals_x", "graph + hook",
     "Heading-math scale applies to the title '$y=x$' — sits as a balanced peer "
     "of the bold text. Graph unchanged."),
    (13, "repair_by_restricting", "graph + hook",
     "No layout change; the restrict→reflect graph and bottom caption read well."),
    (14, "finding_the_inverse_strategy", "procedure_steps",
     "Step 3 label shortened 'Interchange the names $x$ and $y$.' → 'Interchange "
     "$x$ and $y$.' so it sets on one line (was wrapping a lone 'y.' widow); "
     "'the names' is carried by the narration. Layout already balanced."),
    (15, "inverse_of_a_cubic", "derivation",
     "Title 'Inverse of $f(x)=x^3+2$' → 'Inverting a Cubic' (the formula is the "
     "first body line — redundant + towering in the heading). Fix A + brighter rail."),
    (16, "inverse_of_a_rational", "derivation",
     "Title 'Inverse of $f(x)=\\dfrac{3}{x-5}$' → 'Inverting a Rational Function' "
     "(the \\dfrac towered 3× over the text; the rational is the first body line). "
     "Fix A + brighter rail."),
    (17, "inverse_in_an_application", "derivation",
     "Fix A: the Fahrenheit↔Celsius chain anchored to the title (no reason rail "
     "in this scene)."),
    (18, "recap", "recap_cards",
     "No change — 4 numbered points + 3 REMEMBER formula cards, balanced."),
]

# scenes with a genuine pre-round frame in _verify/ -> before/after pair
BEFORE_AFTER = {"one_to_one_definition", "horizontal_line_test"}


def _scene_card(num: int, sid: str, template: str, note: str) -> str:
    after = FRAMES_LIVE / f"{num:02d}_{sid}" / "final.png"
    head = (f'<div class="scene"><h3>{num:02d} · {html.escape(sid)} '
            f'<span class="tpl">{html.escape(template)}</span></h3>'
            f'<p class="note">{note}</p>')
    if sid in BEFORE_AFTER:
        before = FRAMES_BEFORE / f"{sid}.png"
        body = ('<div class="ba">'
                f'<figure><figcaption>before</figcaption>{_img(before, sid + " before")}</figure>'
                f'<figure><figcaption>after</figcaption>{_img(after, sid + " after")}</figure>'
                '</div>')
    else:
        body = f'<div class="single">{_img(after, sid)}</div>'
    return head + body + "</div>"


def build_html() -> str:
    tpl = "\n".join(
        f'<div class="tc"><h3>{html.escape(t)}</h3><p>{d}</p></div>'
        for t, d in TEMPLATE_CHANGES)
    scenes = "\n".join(_scene_card(*s) for s in SCENES)
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>§1.1 Inverse Functions — scene-polish round (2026-06-21)</title>
<style>
  :root {{ color-scheme: dark; }}
  body {{ margin:0; background:#0a0d14; color:#dfe4ee;
    font-family:"Times New Roman",Georgia,serif; line-height:1.5; }}
  .wrap {{ max-width:1180px; margin:0 auto; padding:40px 26px 80px; }}
  h1 {{ font-size:30px; margin:0 0 6px; }}
  .sub {{ color:#8b93a6; font-size:15px; margin:0 0 18px; }}
  .verdict {{ background:#0e1a14; border:1px solid #1d3b2c; border-left:3px solid #57c08a;
    border-radius:8px; padding:12px 16px; margin:0 0 28px; font-size:14.5px; color:#bfe0cf; }}
  .verdict b {{ color:#7fe3ac; }}
  h2 {{ font-size:21px; border-bottom:1px solid #232838; padding-bottom:8px;
    margin:40px 0 18px; }}
  .tc {{ background:#10141d; border:1px solid #1d2433; border-left:3px solid #5cc8ec;
    border-radius:8px; padding:14px 18px; margin:0 0 14px; }}
  .tc h3 {{ margin:0 0 6px; font-size:17px; color:#eef2fb; }}
  .tc p {{ margin:0; font-size:14.5px; color:#b9c0d0; }}
  code {{ font-family:"Courier New",monospace; background:#1a2030; color:#9ad6f0;
    padding:1px 5px; border-radius:4px; font-size:13px; }}
  .scene {{ background:#0d111a; border:1px solid #1b2231; border-radius:9px;
    padding:16px 18px; margin:0 0 20px; }}
  .scene h3 {{ margin:0 0 4px; font-size:17px; color:#eef2fb; }}
  .scene h3 .tpl {{ font-family:"Courier New",monospace; font-size:11px; color:#6b748a;
    background:#141a26; padding:2px 7px; border-radius:10px; margin-left:8px;
    vertical-align:middle; letter-spacing:.04em; }}
  .note {{ margin:0 0 12px; font-size:14.5px; color:#aeb6c6; }}
  img {{ width:100%; border:1px solid #222a3a; border-radius:6px; display:block; }}
  .single img {{ max-width:760px; }}
  .ba {{ display:grid; grid-template-columns:1fr 1fr; gap:14px; }}
  figure {{ margin:0; }}
  figcaption {{ font-family:"Courier New",monospace; font-size:11px; letter-spacing:.06em;
    text-transform:uppercase; color:#6b748a; margin:0 0 5px; }}
  .ba figure:first-child figcaption {{ color:#e0884f; }}
  .ba figure:last-child figcaption {{ color:#57c08a; }}
  .missing {{ padding:30px; text-align:center; color:#e0884f; background:#15110d;
    border:1px dashed #4a3a2a; border-radius:6px; font-size:13px; }}
</style></head>
<body><div class="wrap">
  <h1>§1.1 Inverse Functions — scene-by-scene visual polish</h1>
  <p class="sub">2026-06-21 · mock render, no billed API · 17 content scenes
  re-rendered + frame-checked · 3 template fixes + 4 title/label rewords</p>

  <div class="verdict">✓ Independent gate-1 visual-frame audit (17 parallel
  agents, one per scene): <b>0 visual blocking deck-wide</b> — V1–V9 clean on
  every scene; remaining notes are Advisory aesthetics (A-scores 78–92). The
  recurring "top-heavy" note drove the BODY_TOP_GAP re-tune below.</div>

  <h2>Template changes (the generalised learnings)</h2>
  {tpl}

  <h2>Per-scene final state</h2>
  {scenes}
</div></body></html>"""


def main() -> None:
    OUT.write_text(build_html(), encoding="utf-8")
    ext = sum(1 for s in SCENES if (FRAMES_LIVE / f"{s[0]:02d}_{s[1]}" / "final.png").exists())
    print(f"wrote {OUT}  ({ext}/{len(SCENES)} after-frames embedded)")


if __name__ == "__main__":
    main()
