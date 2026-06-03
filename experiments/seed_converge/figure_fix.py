#!/usr/bin/env python3
"""Visual auto-fix loop for ONE handout figure -- closes the loop figure_critic opens.

render (latexmk) -> rasterize (pymupdf) -> critique (figure_critic rubric) -> if
defects, ask a MULTIMODAL model to REWRITE the TikZ (it sees the image + the current
code + the defects, with the maths held fixed) -> re-render -> re-critique. Repeat
until clean or --max-rounds. This is the figure analog of run.py's converge loop,
but the auditor is VISUAL.

Reuses figure_critic.py for rasterization, the VLM call, the figure rubric, and the
tolerant JSON parse. BILLED with --confirm. Key from env (GEMINI_API_KEY). Needs
latexmk on PATH + pymupdf.

    python figure_fix.py --fig out/reflection_fig.tex --confirm
"""
import argparse
import json
import os
import subprocess
from datetime import datetime
from pathlib import Path

import figure_critic as fc  # same dir; reuse rasterize / call_vlm / rubric / parse

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
OUT_ROOT = HERE / "out" / "figure_fix"

_PREAMBLE = "\n".join(
    rf"\input{{{(REPO / 'preamble' / p).as_posix()}}}"
    for p in ("packages", "colors", "layout", "theorem_setup", "numbering"))
_DOC = (
    r"\documentclass[a4paper,12pt,oneside]{book}" + "\n" + _PREAMBLE + "\n"
    + r"\makeindex[columns=2,title=Index,intoc]" + "\n"
    + r"\newif\ifprintbibliography \printbibliographyfalse" + "\n"
    + r"\newif\ifincludescratchchapter \includescratchchapterfalse" + "\n"
    + r"\begin{document}" + "\n%s\n" + r"\end{document}" + "\n")

_FIX_SYS = (
    "You FIX the LaTeX/TikZ source of ONE calculus-handout figure. You are given the "
    "RENDERED image, the current TikZ code, and a list of VISUAL defects (label "
    "collisions, clipping, colour-only encoding, etc.). Rewrite the TikZ to resolve "
    "EVERY listed defect while keeping the MATHEMATICS IDENTICAL (same functions, "
    "points, domains, and the meaning of every label) and honouring the house palette "
    "(blue = primary, red = secondary/counterexample, gray = auxiliary such as y=x) "
    "and REDUNDANT ENCODING (distinguish curves by line-style/marker too, not colour "
    "alone). Output ONLY the corrected figure LaTeX (\\begin{figure}...\\end{figure}); "
    "no prose, no code fence.")


def _render(fragment: str, work_dir: Path, name: str) -> Path:
    doc = work_dir / f"{name}.tex"
    doc.write_text(_DOC % fragment, encoding="utf-8")
    subprocess.run(
        ["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error",
         f"-output-directory={work_dir.as_posix()}", doc.as_posix()],
        cwd=str(REPO), capture_output=True, text=True)
    pdf = work_dir / f"{name}.pdf"
    if not pdf.exists():
        raise RuntimeError(f"latexmk produced no PDF for {name}")
    return pdf


def _strip_fence(s: str) -> str:
    s = s.strip()
    if s.startswith("```"):
        s = s.split("```", 2)[1]
        for tag in ("latex", "tex"):
            if s.lstrip().startswith(tag):
                s = s.lstrip()[len(tag):]
    return s.strip()


def run(fig_path, *, provider, model, api_key, out_dir, max_rounds, max_tokens):
    out_dir.mkdir(parents=True, exist_ok=True)
    tikz = Path(fig_path).read_text(encoding="utf-8")
    trace, usage = [], []
    for k in range(max_rounds + 1):
        (out_dir / f"round_{k:02d}.tex").write_text(tikz, encoding="utf-8")
        try:
            pdf = _render(tikz, out_dir, f"round_{k:02d}")
        except RuntimeError as e:
            trace.append(f"Round {k}: render FAILED ({e}); keeping previous figure.")
            break
        png = out_dir / f"round_{k:02d}.png"
        fc.rasterize(pdf, 1, png)
        try:
            raw, used, _f = fc.call_vlm(provider, model, fc._prompt(1), png,
                                        api_key=api_key, max_tokens=4000)
        except Exception as e:  # noqa: BLE001 -- transient API error shouldn't lose the run
            trace.append(f"Round {k}: critique call FAILED ({type(e).__name__}); stopping.")
            break
        usage.append({"round": k, "step": "critique", **fc._usage(used, provider, model)})
        try:
            crit = fc._extract_json(raw)
        except Exception as e:  # noqa: BLE001
            crit = {"defects": [], "overall": f"PARSE_FAIL: {e}", "_raw": raw}
        (out_dir / f"round_{k:02d}_critique.json").write_text(
            json.dumps(crit, ensure_ascii=False, indent=2), encoding="utf-8")
        defects = crit.get("defects", []) if isinstance(crit, dict) else []
        trace.append(f"Round {k}: {len(defects)} defect(s)"
                     + ((": " + "; ".join(d.get("issue", "") for d in defects)) if defects else " -- CLEAN."))
        if not defects or k == max_rounds:
            break
        prompt = (_FIX_SYS + "\n\n--- current TikZ ---\n" + tikz
                  + "\n\n--- visual defects ---\n" + json.dumps(defects, ensure_ascii=False, indent=2)
                  + "\n\nRewrite the figure to fix these. Output ONLY the corrected figure LaTeX.")
        try:
            fixed, used, _f = fc.call_vlm(provider, model, prompt, png, api_key=api_key,
                                          max_tokens=max_tokens, response_format=None)
        except Exception as e:  # noqa: BLE001 -- transient API error shouldn't lose the run
            trace.append(f"Round {k}: fix call FAILED ({type(e).__name__}); keeping round {k} figure.")
            break
        usage.append({"round": k, "step": "fix", **fc._usage(used, provider, model)})
        tikz = _strip_fence(fixed)

    (out_dir / "final.tex").write_text(tikz, encoding="utf-8")
    total = round(sum(u["usd"] for u in usage), 4)
    (out_dir / "usage.json").write_text(
        json.dumps({"calls": usage, "total_usd": total}, ensure_ascii=False, indent=2), encoding="utf-8")
    (out_dir / "trace.md").write_text(
        f"# figure_fix trace ({provider}:{model})\n\nest. ${total} over {len(usage)} call(s)\n\n"
        + "\n".join("- " + t for t in trace) + "\n", encoding="utf-8")
    print(f"[figure-fix] done, est. ${total}. out={out_dir}", flush=True)
    for t in trace:
        print("  " + t, flush=True)


def main() -> int:
    ap = argparse.ArgumentParser(description="Visual auto-fix loop for one figure (billed).")
    ap.add_argument("--fig", required=True, type=Path, help="a .tex file with ONE figure block")
    ap.add_argument("--provider", default="gemini", help="provider[:model], default gemini")
    ap.add_argument("--max-rounds", type=int, default=3)
    ap.add_argument("--max-tokens", type=int, default=16000)  # thinking model: headroom so the fix isn't truncated
    ap.add_argument("--run-name", default=None)
    ap.add_argument("--confirm", action="store_true",
                    help="BILLED: renders + multimodal critique/fix. Key from env.")
    args = ap.parse_args()

    provider, model = fc._role(args.provider)
    if not args.confirm:
        print("[figure-fix] re-run with --confirm (BILLED: latexmk renders + multimodal "
              "critique & fix). Key from env.", flush=True)
        return 0
    env = fc.PROVIDERS[provider]["env"]
    key = os.environ.get(env)
    if not key:
        print(f"[figure-fix] needs the key in env {env} (never a flag, never logged).", flush=True)
        return 2
    run_name = args.run_name or datetime.now().strftime("%Y%m%d_%H%M%S")
    run(args.fig, provider=provider, model=model, api_key=key,
        out_dir=OUT_ROOT / run_name, max_rounds=args.max_rounds, max_tokens=args.max_tokens)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
