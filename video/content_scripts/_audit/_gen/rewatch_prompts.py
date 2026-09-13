"""rewatch_prompts.py -- assemble the per-lens REWATCH prompts into an isolated workspace.

    python video/content_scripts/_audit/_gen/rewatch_prompts.py --ws <workspace dir> \
        [--pack video/output/ch03/s3.1/rewatch_pack] [--runs R1a,R1b,R2,R3,R4,R5] \
        [--tex handout/latex/src/ch03/chapter3.tex --section 3.1]

Builds <ws>/pack (a COPY of the viewer-facing pack: INDEX.md, sheets, per-scene md, frame
dirs -- no PRODUCTION.md, no pack.json), <ws>/handout_s<sec>.tex (only used by R3), and
<ws>/<run>/{PROMPT.md,schema.json} from PROMPT-rewatch.template.md + the rubric's common
rules + ONLY that lens's section (blind lenses must not see the other lenses' dimensions).
Run subagent lenses by pointing them at <ws>/<run>/PROMPT.md. Nothing here is committed.

--flat (REQUIRED for agy runs; 2026-09-13): agy does NOT confine its file tools to cwd --
when "PROMPT.md" is not found immediately it searches the workspace tree, finds all six lens
PROMPT.md files and picks one arbitrarily. The shared layout above therefore breaks blindness
for external runs: of three agy lenses, two reviewed a lens they were not assigned. With
--flat (exactly one --runs entry) the run IS the workspace: PROMPT.md, schema.json, pack/ and
the .tex land directly in <ws>, with no sibling run dirs to find. One --ws per agy lens; run
it with cwd=<ws> and --add-dir <ws>.
"""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent          # _gen
AUD = HERE.parent                                # content_scripts/_audit
REPO = AUD.parents[2]
RUN_LENS = {"R1a": "R1", "R1b": "R1", "R2": "R2", "R3": "R3", "R4": "R4", "R5": "R5"}


def section(text: str, start: str, ends: list[str]) -> str:
    a = text.index(start)
    stops = [text.find(e, a + len(start)) for e in ends]
    b = min((s for s in stops if s > 0), default=len(text))
    return text[a:b].strip()


def copy_pack(src: Path, dst: Path) -> None:
    dst.mkdir(parents=True, exist_ok=True)
    for p in src.iterdir():
        if p.name in ("PRODUCTION.md", "pack.json"):
            continue                                   # production info: not for blind lenses
        if p.is_dir():
            shutil.copytree(p, dst / p.name, dirs_exist_ok=True)
        else:
            shutil.copy2(p, dst / p.name)


def extract_section(tex: Path, sec: str) -> str:
    src = tex.read_text(encoding="utf-8")
    key = f"sechead{{{sec}}}"
    i0 = src.find(key)
    major, minor = sec.split(".")
    i1 = src.find(f"sechead{{{major}.{int(minor) + 1}}}")
    if i0 < 0:
        raise SystemExit(f"[rewatch_prompts] \\{key} not found in {tex}")
    return "\\" + (src[i0:i1] if i1 > 0 else src[i0:]).rstrip()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--ws", type=Path, required=True, help="workspace dir OUTSIDE the repo (scratchpad)")
    ap.add_argument("--pack", type=Path, default=REPO / "video" / "output" / "ch03" / "s3.1" / "rewatch_pack")
    ap.add_argument("--runs", default="R1a,R1b,R2,R3,R4,R5")
    ap.add_argument("--tex", type=Path, default=REPO / "handout" / "latex" / "src" / "ch03" / "chapter3.tex")
    ap.add_argument("--section", default="3.1")
    ap.add_argument("--scenes", default="", help="optional: restrict the review to these scene ids (comma list)")
    ap.add_argument("--flat", action="store_true",
                    help="single-run workspace: write PROMPT.md/schema.json into <ws> itself, no <run>/ subdir "
                         "(REQUIRED for agy, which would otherwise find the sibling lenses' prompts)")
    args = ap.parse_args()
    runs = args.runs.split(",")
    if args.flat and len(runs) != 1:
        raise SystemExit("[rewatch_prompts] --flat takes exactly one --runs entry (one workspace per agy lens)")

    rubric = (AUD / "REWATCH-REVIEW-RUBRIC.md").read_text(encoding="utf-8")
    template = (AUD / "PROMPT-rewatch.template.md").read_text(encoding="utf-8")
    schema = (AUD / "rewatch-findings.schema.json").read_text(encoding="utf-8")
    common = section(rubric, "## 共同規則", ["## 五鏡"]).split("\n", 1)[1].strip()
    lens_sections = {k: section(rubric, f"### {k} ", ["### R", "## 輸出格式"]) for k in ("R1", "R2", "R3", "R4", "R5")}
    rule_field = section(rubric, "### `rule`", ["## 編排"])

    ws = args.ws.resolve()
    copy_pack(args.pack.resolve(), ws / "pack")
    tex_out = ws / f"handout_s{args.section.replace('.', '')}.tex"
    tex_out.write_text(extract_section(args.tex, args.section), encoding="utf-8")
    extra = {
        "R1": "（無）", "R2": "（無）", "R5": "（無）",
        "R3": f"講義原節 LaTeX 源：`{tex_out.name if args.flat else tex_out}`（判弧線與該教的東西是否被安排；不重審忠實）",
        "R4": "（無）——本鏡**只讀** `INDEX.md` 與各場 `NN_<scene>.md` 的數字與時間軸，**不要開任何 .jpg**。",
    }
    scope = (f"\n\n**本次只審這些場**（其餘場在 JSON 裡仍要列出、verdict 填 `ok`、findings 留空）：`{args.scenes}`"
             if args.scenes else "")
    for run in runs:
        lens = RUN_LENS[run]
        body = (template.split("-->", 1)[1].strip()
                .replace("{{LENS_ID}}", lens)
                .replace("{{LENS_SECTION}}", lens_sections[lens])
                .replace("{{COMMON_RULES}}", common)
                .replace("{{PACK_DIR}}", str(ws / "pack"))
                .replace("{{EXTRA_INPUTS}}", extra[lens] + scope)
                .replace("{{OUTPUT_SCHEMA}}", schema.strip())
                .replace("{{RULE_FIELD}}", rule_field))
        if lens == "R4":
            body = body.replace("每場：先看 sheet（整張看過每一格與標籤），再讀 md（時間軸與數字），然後記下 verdict 與 findings。"
                                "看不清的格開原尺寸幀。",
                                "每場：只讀 md（時間軸與數字；本鏡不看圖），然後記下 verdict 與 findings。")
        d = ws if args.flat else ws / run
        d.mkdir(parents=True, exist_ok=True)
        (d / "PROMPT.md").write_text(body, encoding="utf-8")
        shutil.copy(AUD / "rewatch-findings.schema.json", d / "schema.json")
        print(f"{run} ({lens}) -> {d / 'PROMPT.md'}")
    print(f"pack copied to {ws / 'pack'}; tex -> {tex_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
