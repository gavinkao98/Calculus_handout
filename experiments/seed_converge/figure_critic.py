#!/usr/bin/env python3
"""Multimodal figure QA for the calculus handout (mirrors video/pipeline/critic.py).

Rasterizes a figure-bearing PDF page with pymupdf -> sends the PNG to a MULTIMODAL
model -> gets a structured critique against the project's figure rules
(CONTENT_SPEC SS10): label/element collisions, clipped/off-bounds elements,
colour-only encoding, grayscale survival, axis/caption hygiene. The model is
ADVISORY -- a human triages; it judges the VISUAL layer only, not the maths.

This is the visual-layer sibling of the text cross-review in run.py: the same
critic.py conventions (urllib, OpenAI-compatible /chat/completions, env-var keys,
--dry-run/--confirm/--smoke gates, tolerant JSON, backoff retry), but the message
carries an image and the rubric is figure-specific.

BILLED with --confirm. Key from env (GEMINI_API_KEY / OPENAI_API_KEY) -- never a
flag, never a file, never logged.

    python figure_critic.py --pdf out/full1/preview.pdf --pages 2,6 --dry-run
    python figure_critic.py --pdf out/full1/preview.pdf --pages 2,6 --confirm --smoke
    python figure_critic.py --pdf out/full1/preview.pdf --pages 2,6 --confirm
"""
import argparse
import base64
import json
import os
import re
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

import fitz  # pymupdf -- in-process PDF rasterization

HERE = Path(__file__).resolve().parent
OUT_ROOT = HERE / "out" / "figure_critic"

# Multimodal providers speaking the OpenAI /chat/completions image_url shape.
PROVIDERS = {
    "gemini": {
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai",
        "env": "GEMINI_API_KEY",
        "token_param": "max_tokens",
    },
    "openai": {
        "base_url": "https://api.openai.com/v1",
        "env": "OPENAI_API_KEY",
        "token_param": "max_completion_tokens",
    },
}
DEFAULT_MODELS = {"gemini": "gemini-3.1-pro-preview", "openai": "gpt-5.1"}
PRICE = {"gemini": (1.25, 5.0), "openai": (1.25, 10.0)}  # USD / 1M tok, PLACEHOLDER
EST_IMAGE_TOKENS = 1200   # one 150-dpi A4 page, rough
EST_OUTPUT_TOKENS = 1500

_SYSTEM = (
    "You are an ADVISORY visual reviewer of a single FIGURE from a PRINTED calculus "
    "handout (it must survive a black-and-white photocopy). You are shown one "
    "rendered PDF page; judge ONLY the figure(s) on it. Surface defects for a human "
    "-- you do NOT redraw.\n"
    "Judge the VISUAL/LAYOUT layer ONLY (NOT the mathematics or prose) against these "
    "house rules:\n"
    "- NO label/element COLLISIONS: axis labels, curve labels, plotted points, point "
    "labels, and captions must not overlap each other or the axes/arrows.\n"
    "- nothing CLIPPED or running off the figure's bounding box.\n"
    "- REDUNDANT ENCODING: meaning must not rely on COLOUR ALONE -- distinct curves "
    "must also differ by line-style/label/marker, so the figure still reads in "
    "GRAYSCALE.\n"
    "- palette is three roles only (blue = primary, red = caution/counterexample, "
    "gray = auxiliary such as y=x).\n"
    "- axes labelled, tick/scale sane, a caption is present.\n"
    "Be EXHAUSTIVE about collisions/overlaps -- list EVERY label, point-label, curve, "
    "axis, arrow, or caption that overlaps another. Report CONCRETE defects (where / "
    "issue / suggestion); do not invent problems -- if the figure is genuinely clean, "
    "return an empty defects list. Return JSON only:\n"
    '{"defects":[{"severity":"low|med|high","where":str,"issue":str,'
    '"suggestion":str}],"overall":str}'
)

# Strict structured-output schema. Bare json_object made Gemini go rogue (returned
# a bounding box / an empty list), so we pin the exact shape via json_schema.
_SCHEMA = {
    "type": "object",
    "properties": {
        "defects": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "severity": {"type": "string", "enum": ["low", "med", "high"]},
                    "where": {"type": "string"},
                    "issue": {"type": "string"},
                    "suggestion": {"type": "string"},
                },
                "required": ["severity", "where", "issue", "suggestion"],
                "additionalProperties": False,
            },
        },
        "overall": {"type": "string"},
    },
    "required": ["defects", "overall"],
    "additionalProperties": False,
}


def _extract_json(text: str) -> dict:
    """Lenient parse: strip a ```json fence, take the outer {...}, repair illegal
    LaTeX backslashes inside strings (same fix as critic.py / run.py)."""
    s = (text or "").strip()
    if s.startswith("```"):
        s = s.split("```", 2)[1]
        if s.lstrip().startswith("json"):
            s = s.lstrip()[4:]
    i, j = s.find("{"), s.rfind("}")
    if 0 <= i < j:
        s = s[i:j + 1]
    try:
        return json.loads(s)
    except Exception:  # noqa: BLE001
        return json.loads(re.sub(r'\\(?![\\"/bfnrtu])', r"\\\\", s))


def rasterize(pdf_path: Path, page_num: int, out_png: Path, dpi: int = 150) -> Path:
    """1-based page_num -> PNG via pymupdf."""
    doc = fitz.open(pdf_path)
    try:
        doc.load_page(page_num - 1).get_pixmap(dpi=dpi).save(out_png)
    finally:
        doc.close()
    return out_png


def _image_data_url(png_path: Path) -> str:
    return "data:image/png;base64," + base64.b64encode(Path(png_path).read_bytes()).decode("ascii")


def call_vlm(provider: str, model: str, prompt: str, png_path: Path, *,
             api_key: str, max_tokens: int, timeout: int = 180, retries: int = 3):
    spec = PROVIDERS[provider]
    payload = {
        "model": model,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": _image_data_url(png_path)}},
            ],
        }],
        "response_format": {"type": "json_schema",  # pin exact shape (bare json_object went rogue)
                            "json_schema": {"name": "figure_critique", "strict": True, "schema": _SCHEMA}},
        spec["token_param"]: max_tokens,
    }
    req = urllib.request.Request(
        f"{spec['base_url'].rstrip('/')}/chat/completions",
        data=json.dumps(payload).encode("utf-8"), method="POST",
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
    )
    data = None
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            break
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and attempt < retries:
                time.sleep((2 ** attempt) * 2)
                continue
            raise
        except (urllib.error.URLError, TimeoutError):
            if attempt < retries:
                time.sleep((2 ** attempt) * 2)
                continue
            raise
    choice = data["choices"][0]
    return choice["message"]["content"], data.get("usage", {}), choice.get("finish_reason")


def _usage(used: dict, provider: str, model: str, finish=None) -> dict:
    pin, pout = int(used.get("prompt_tokens", 0)), int(used.get("completion_tokens", 0))
    cin, cout = PRICE[provider]
    return {"provider": provider, "model": model, "prompt_tokens": pin,
            "completion_tokens": pout, "finish_reason": finish,
            "usd": round(pin / 1e6 * cin + pout / 1e6 * cout, 4)}


def _prompt(page_num: int) -> str:
    return (f"This is page {page_num} of the rendered handout PDF. Critique the "
            f"figure(s) shown on this page per the rules.")


def run_critique(pdf, pages, *, provider, model, api_key, out_dir, max_tokens, smoke):
    out_dir.mkdir(parents=True, exist_ok=True)
    targets = pages[:1] if smoke else pages
    results, usage_log = [], []
    for pg in targets:
        png = out_dir / f"page_{pg:02d}.png"
        rasterize(pdf, pg, png)
        raw, used, fin = call_vlm(provider, model, _prompt(pg), png,
                                  api_key=api_key, max_tokens=max_tokens)
        try:
            crit = _extract_json(raw)
        except Exception as e:  # noqa: BLE001
            crit = {"scores": {}, "defects": [], "overall": f"PARSE_FAIL: {e}", "_raw": raw}
        (out_dir / f"page_{pg:02d}_critique.json").write_text(
            json.dumps(crit, ensure_ascii=False, indent=2), encoding="utf-8")
        usage_log.append({"page": pg, **_usage(used, provider, model, fin)})
        results.append({"page": pg, "png": str(png), "critique": crit})

    total = round(sum(c["usd"] for c in usage_log), 4)
    (out_dir / "usage.json").write_text(
        json.dumps({"calls": usage_log, "total_usd": total}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    _write_md(results, out_dir / "critique.md", provider, model)
    print(f"[figure-critic] {len(results)} page(s), est. ${total}. out={out_dir}", flush=True)
    return results


def _write_md(results, path, provider, model):
    lines = [f"# Figure critique ({provider}:{model})\n"]
    for r in results:
        c = r["critique"]
        if not isinstance(c, dict):
            c = {"scores": {}, "defects": [], "overall": f"non-object response: {c!r}"}
        lines.append(f"## Page {r['page']}\n")
        sc = c.get("scores", {})
        if sc:
            lines.append("scores: " + ", ".join(f"{k}={v}" for k, v in sc.items()) + "\n")
        for d in c.get("defects", []):
            lines.append(f"- **[{d.get('severity','?')}]** {d.get('where','')}: "
                         f"{d.get('issue','')}  \n  → {d.get('suggestion','')}")
        if not c.get("defects"):
            lines.append("- (no defects reported)")
        lines.append(f"\n_{c.get('overall','')}_\n")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def dry_run(pdf, pages, provider, model, out_dir, max_tokens):
    out_dir.mkdir(parents=True, exist_ok=True)
    for pg in pages:
        rasterize(pdf, pg, out_dir / f"page_{pg:02d}.png")
    cin, cout = PRICE[provider]
    n = len(pages)
    usd = n * ((EST_IMAGE_TOKENS + 300) / 1e6 * cin + EST_OUTPUT_TOKENS / 1e6 * cout)
    print("[figure-critic] DRY RUN -- no API calls.")
    print(f"  provider = {provider}:{model}   pages = {pages}   max_tokens = {max_tokens}")
    print(f"  rasterized {n} page PNG(s) to {out_dir}")
    print(f"  rough estimate: ${usd:.2f}   (PLACEHOLDER prices)")
    print(f"  to run billed: set {PROVIDERS[provider]['env']}, then --confirm (add --smoke first).")


def _role(spec: str):
    provider, _, model = spec.partition(":")
    if provider not in PROVIDERS:
        raise SystemExit(f"unknown provider {provider!r}; choose from {list(PROVIDERS)}")
    return provider, (model or DEFAULT_MODELS[provider])


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Multimodal figure QA (offline; billed call gated).")
    ap.add_argument("--pdf", required=True, type=Path)
    ap.add_argument("--pages", required=True, help="comma list of 1-based page numbers, e.g. 2,6")
    ap.add_argument("--provider", default="gemini", help="provider[:model], default gemini")
    ap.add_argument("--max-tokens", type=int, default=4000)
    ap.add_argument("--run-name", default=None)
    ap.add_argument("--dry-run", action="store_true",
                    help="rasterize pages + print estimate; never calls the API")
    ap.add_argument("--confirm", action="store_true",
                    help="actually call the VLM (BILLED). Key from env.")
    ap.add_argument("--smoke", action="store_true",
                    help="with --confirm, critique only the FIRST page")
    args = ap.parse_args()

    provider, model = _role(args.provider)
    pages = [int(x) for x in args.pages.split(",") if x.strip()]
    run_name = args.run_name or datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = OUT_ROOT / run_name

    if args.confirm:
        env = PROVIDERS[provider]["env"]
        key = os.environ.get(env)
        if not key:
            print(f"[figure-critic] --confirm needs the key in env {env} "
                  f"(never pass it as a flag, never write it to a file).", flush=True)
            return 2
        run_critique(args.pdf, pages, provider=provider, model=model, api_key=key,
                     out_dir=out_dir, max_tokens=args.max_tokens, smoke=args.smoke)
        return 0
    if args.dry_run:
        dry_run(args.pdf, pages, provider, model, out_dir, args.max_tokens)
        return 0
    print("[figure-critic] nothing ran. Re-run with --dry-run for the estimate, "
          "or --confirm for the billed critique.", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
