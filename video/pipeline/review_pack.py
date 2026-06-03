"""review_pack.py -- content/engineering cross-review scaffold (advisory only).

The TEXT-review sibling of critic.py. Where critic.py sends a RENDERED FRAME to a
vision model to catch visual defects, this assembles the AUTHORING context --
.tex source, narration, the unit breakdown, generated hook code -- and sends it
to a second text model (DeepSeek) to catch what the deterministic guards and the
VLM structurally cannot: faithfulness drift, textbook-stiff narration,
decomposition problems, and math/convention bugs in generated animation code.

Four lenses (CODE2VIDEO_STUDY P1 philosophy, extended from visual to content):
  faithfulness   per unit:  .tex source slice  <->  narration   (METHODOLOGY 1,3)
  register       per unit:  narration                           (METHODOLOGY 4)
  decomposition  whole section:  unit kind/goal list            (METHODOLOGY 3,5)
  engineering    generated hook code  <->  cue + .tex math      (DESIGN checklist)

Same gate as critic.py: free assembly + --dry-run (writes packets, prints a token
estimate, NO network). The billed DeepSeek call is behind --confirm and reads the
key from env DEEPSEEK_API_KEY -- never a flag, never a file, never committed
(CLAUDE.md). Advisory only: writes output/review/<id>/review.{json,md}; it never
edits the content script or storyboard. The human stays the authority.

The prompt feeds the model the HOUSE RULES (the methodology rubric per lens) plus
the CLAUDE.md four-level finding triage, so a fresh model judges against this
project's deliberate decisions rather than flooding generic-prior nitpicks.

Run (offline, no key):
    python video/pipeline/review_pack.py --storyboard video/storyboards/ch01_inverse_functions.yml --dry-run
"""
from __future__ import annotations

import argparse
import json
import os
import re
import time
import urllib.error
import urllib.request
from pathlib import Path

sys_path_anchor = Path(__file__).resolve().parent.parent
import sys  # noqa: E402

sys.path.insert(0, str(sys_path_anchor))

from pipeline import _bootstrap  # noqa: E402

_bootstrap.bootstrap()

import yaml  # noqa: E402

# DeepSeek platform: OpenAI-compatible /chat/completions, Bearer auth. Model id
# `deepseek-v4-pro` confirmed available on this key (also deepseek-v4-flash). Key
# is read from env DEEPSEEK_API_KEY -- never a flag, never a file, never logged.
DEFAULT_BASE_URL = "https://api.deepseek.com"
DEFAULT_MODEL = "deepseek-v4-pro"

# Placeholder pricing for the cost estimate, clearly labelled. DeepSeek text rates
# are an order cheaper than the MiMo vision call; refine from the smoke test's
# real usage before trusting the dollar figure.
PRICE_IN_PER_MTOK = 0.28    # USD per 1M input tokens  (PLACEHOLDER)
PRICE_OUT_PER_MTOK = 1.10   # USD per 1M output tokens (PLACEHOLDER)
CHARS_PER_TOKEN = 3.2       # rough: mixed English + CJK + LaTeX (estimate only)
EST_OUTPUT_TOKENS = 2700    # per call: deepseek-v4-pro is a REASONING model -- most
                            # completion tokens are hidden reasoning (~2.5k measured
                            # in the smoke run), so out >> in. max_tokens stays 8000.


# ---- inputs -------------------------------------------------------------

def load_storyboard(path: Path) -> dict:
    return yaml.safe_load(path.resolve().read_text(encoding="utf-8"))


_UNIT_HEADER = re.compile(r"^###\s+\d+\.\s+(\S+)")
_FIELD = re.compile(r"^-\s+\*\*([A-Za-z_]+):\*\*\s*(.*)$")
_LINE_RANGE = re.compile(r"L\s*(\d+)\s*[-–—]\s*(\d+)")
_LINE_ONE = re.compile(r"L\s*(\d+)\b")


def parse_content_script(md_path: Path) -> dict:
    """Parse the §-content-script markdown into units. Each unit is a
    `### N. <id>` block with `- **field:** value` lines; `narration`/`visual_need`
    /`animation_cue` may continue on indented (or `>`-quoted) follow lines.
    Returns {header, units:[{id, source, learning_goal, kind, narration,
    visual_need, animation_cue}]}."""
    text = md_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    # header blurb = everything before the first unit header (has the .tex name)
    header_lines: list[str] = []
    for ln in lines:
        if _UNIT_HEADER.match(ln):
            break
        header_lines.append(ln)
    header = "\n".join(header_lines)

    units: list[dict] = []
    cur: dict | None = None
    field: str | None = None

    def _commit_field() -> None:
        if cur is not None and field is not None:
            cur[field] = " ".join(cur[field]).strip() if isinstance(cur[field], list) else cur[field]

    for ln in lines:
        m = _UNIT_HEADER.match(ln)
        if m:
            _commit_field()
            if cur is not None:
                units.append(cur)
            cur = {"id": m.group(1), "source": "", "learning_goal": "", "kind": "",
                   "narration": "", "visual_need": "", "animation_cue": ""}
            field = None
            continue
        if cur is None:
            continue
        mf = _FIELD.match(ln)
        if mf:
            _commit_field()
            field = mf.group(1).lower()
            val = mf.group(2).strip().strip("`").strip()
            cur[field] = [val] if val else []
            continue
        # continuation of the current field?
        if field is not None and ln.strip():
            piece = ln.strip()
            if piece.startswith(">"):
                piece = piece[1:].strip()
            if not isinstance(cur[field], list):
                cur[field] = [cur[field]]
            cur[field].append(piece)
            continue
        if not ln.strip():
            _commit_field()
            field = None
    _commit_field()
    if cur is not None:
        units.append(cur)

    # normalise the em-dash "not applicable" placeholders to empty
    for u in units:
        for k in ("narration", "visual_need", "animation_cue", "learning_goal"):
            v = u.get(k, "")
            if v.lstrip().startswith("—") or v.strip() == "-":
                u[k] = ""
    return {"header": header, "units": units}


def source_tex_name(header: str, override: str | None) -> str | None:
    if override:
        return override
    m = re.search(r"([A-Za-z0-9_]+\.tex)", header)
    return m.group(1) if m else None


def tex_slice(tex_lines: list[str], source: str, pad: int = 0, cap: int = 80) -> str:
    """Pull the .tex lines named by a unit's `source` field (e.g. '(L33-45)').
    Multiple ranges are concatenated; total capped so a packet stays small."""
    spans: list[tuple[int, int]] = []
    for a, b in _LINE_RANGE.findall(source):
        spans.append((int(a), int(b)))
    if not spans:
        singles = [int(x) for x in _LINE_ONE.findall(source)]
        spans = [(s, s) for s in singles]
    if not spans:
        return ""
    out: list[str] = []
    for a, b in spans:
        lo = max(1, a - pad)
        hi = min(len(tex_lines), b + pad)
        chunk = tex_lines[lo - 1:hi]
        out.append(f"% --- {tex_name_label(source)} L{lo}-{hi} ---")
        out.extend(chunk)
        if sum(len(x) for x in out) > cap * 90:
            break
    return "\n".join(out[: cap + len(spans)])


def tex_name_label(source: str) -> str:
    m = re.search(r"(§[\d.]+[^\(]*)", source)
    return (m.group(1).strip() if m else source).strip()


# ---- packet builders (one dict per review call) -------------------------

def _is_silent(unit: dict) -> bool:
    return unit.get("kind", "").lower() in ("intro", "outro")


def packets_faithfulness(units: list[dict], tex_lines: list[str]) -> list[dict]:
    out = []
    for u in units:
        if _is_silent(u) or not u.get("narration"):
            continue
        src = tex_slice(tex_lines, u.get("source", ""))
        if not src:
            continue
        out.append({"layer": "faithfulness", "unit_id": u["id"], "kind": u.get("kind", ""),
                    "source_ref": u.get("source", ""), "tex": src,
                    "narration": u["narration"], "visual_need": u.get("visual_need", "")})
    return out


def packets_register(units: list[dict]) -> list[dict]:
    out = []
    for u in units:
        if _is_silent(u) or not u.get("narration"):
            continue
        out.append({"layer": "register", "unit_id": u["id"], "kind": u.get("kind", ""),
                    "narration": u["narration"]})
    return out


def packet_decomposition(units: list[dict]) -> dict:
    rows = []
    for i, u in enumerate(units, 1):
        rows.append({"n": i, "id": u["id"], "kind": u.get("kind", ""),
                     "learning_goal": u.get("learning_goal", ""),
                     "has_animation": bool(u.get("animation_cue"))})
    return {"layer": "decomposition", "unit_id": None, "units": rows}


def packet_engineering(units: list[dict], hook_path: Path, tex_lines: list[str]) -> dict | None:
    if not hook_path.exists():
        return None
    cues = [{"id": u["id"], "animation_cue": u["animation_cue"],
             "source_ref": u.get("source", "")}
            for u in units if u.get("animation_cue")]
    # math context: the source slices of the animated units, so the reviewer can
    # check the code's numbers against the handout
    math_ctx = "\n".join(
        tex_slice(tex_lines, u.get("source", ""))
        for u in units if u.get("animation_cue") and tex_slice(tex_lines, u.get("source", "")))
    return {"layer": "engineering", "unit_id": None,
            "code": hook_path.read_text(encoding="utf-8"),
            "cues": cues, "math_ctx": math_ctx}


# ---- prompts ------------------------------------------------------------

_SYSTEM = (
    "You are a second-opinion reviewer for a HAND-CRAFTED university calculus "
    "lesson video. You are ADVISORY: you surface findings for a human to weigh; "
    "you NEVER rewrite the content. This project has DELIBERATE house rules -- "
    "judge against THEM, stated below, not against generic priors.\n\n"
    "Classify EVERY finding into exactly one level (do not inflate):\n"
    "  1 real-conflict   -- violates a stated house rule (worth fixing)\n"
    "  2 discoverability -- not wrong, just under-specified / worth a note\n"
    "  3 editorial-drift -- low-priority style risk, not a defect\n"
    "  4 non-finding     -- e.g. wording differs but is semantically equivalent\n"
    "Semantically-equivalent paraphrase is NOT an inconsistency. Math written "
    "inline as LaTeX is intended (the TTS reads it). Over-reporting dilutes the "
    "real findings -- only levels 1-2 should drive action. If nothing is wrong, "
    "return an empty findings list. Return STRICT JSON only, no prose around it:\n"
    '{"layer":str,"unit_id":str|null,"findings":[{"level":1,"severity":'
    '"low|med|high","where":str,"issue":str,"evidence":str,"suggestion":str}],'
    '"summary":str}'
)

_RUBRIC = {
    "faithfulness": (
        "LENS: faithfulness (CONTENT_METHODOLOGY 1,3). The narration's MATH "
        "CONTENT and SCOPE must stay faithful to the .tex source: no environment "
        "dropped, no NEW mathematics added, no distortion. Presentation may be "
        "re-ordered and prose folded, but every math-bearing claim must trace to "
        "the source, and prose between environments must not be silently dropped. "
        "CHECK: does this unit's narration faithfully and completely carry the "
        "math of its .tex slice? Flag dropped / added / distorted math, a source "
        "claim with no narration, or a narration claim with no source."
    ),
    "register": (
        "LENS: register (CONTENT_METHODOLOGY 4). Narration is SPOKEN English, "
        "written for the ear. MUST NOT: read the on-screen title aloud; read a "
        "bullet list verbatim; say section / figure / equation numbers; use "
        "'see' / 'as shown' / 'in the diagram above|below'; open with 'In this "
        "scene we will'. SHOULD: hook -> body -> takeaway; ~3-7 sentences; expand "
        "contractions; an aligned derivation should not re-read the left-hand side "
        "every line. CHECK: does it read like a teacher talking, not a textbook? "
        "Flag concrete stiff / textbook phrasings and any MUST-NOT violation."
    ),
    "decomposition": (
        "LENS: decomposition (CONTENT_METHODOLOGY 3,5). ONE teaching idea per "
        "unit -- a narration needing two topic sentences should split. Unit count "
        "is an OUTCOME, not a budget (detail over compression); do not suggest "
        "merging just to shorten. Ordering may be re-arranged for teaching. "
        "Animation density: only things that MOVE (process / correspondence / "
        "sweep / reflection) get an animation; definitions, calculations, recap "
        "stay static. CHECK the whole unit list: a unit carrying two ideas (split), "
        "two that are really one teaching beat (merge), an ordering that hurts "
        "teaching, or animation over/under-use."
    ),
    "engineering": (
        "LENS: engineering (DESIGN authoring checklist + METHODOLOGY 5). Review "
        "the GENERATED manim animation code on TWO axes only. (1) MATHEMATICAL "
        "FIDELITY: does the code draw EXACTLY the math in the .tex source and the "
        "animation_cue's intent -- correct functions, points, coordinates, limits, "
        "reflections, endpoints? (2) CONVENTION: theme primitives (T.color(...), "
        "not hardcoded hex); solid dot = value attained, hollow = value absent; "
        "muted = decoration only; respects SAFE_MARGIN. DO NOT judge aesthetics "
        "or 'does it look good' -- that is the render+VLM's job, not a code read. "
        "DO NOT propose refactors for taste. Correctness + convention ONLY."
    ),
}


def build_user(packet: dict) -> str:
    layer = packet["layer"]
    head = _RUBRIC[layer] + "\n\n"
    if layer == "faithfulness":
        return (head +
                f"UNIT: {packet['unit_id']}  (kind: {packet['kind']})\n"
                f"SOURCE REF: {packet['source_ref']}\n\n"
                f"--- .tex source ---\n{packet['tex']}\n\n"
                f"--- narration (spoken) ---\n{packet['narration']}\n\n"
                f"--- visual_need ---\n{packet['visual_need']}\n")
    if layer == "register":
        return (head +
                f"UNIT: {packet['unit_id']}  (kind: {packet['kind']})\n\n"
                f"--- narration (spoken) ---\n{packet['narration']}\n")
    if layer == "decomposition":
        rows = "\n".join(
            f"{r['n']:2d}. {r['id']}  [{r['kind']}]  anim={'Y' if r['has_animation'] else 'n'}\n"
            f"     goal: {r['learning_goal']}"
            for r in packet["units"])
        return head + "WHOLE-SECTION UNIT LIST:\n\n" + rows + "\n"
    if layer == "engineering":
        cues = "\n".join(f"- [{c['id']}] ({c['source_ref']}): {c['animation_cue']}"
                         for c in packet["cues"])
        return (head +
                f"--- animation_cue intent (natural language) ---\n{cues}\n\n"
                f"--- .tex math context ---\n{packet['math_ctx']}\n\n"
                f"--- generated manim code ---\n{packet['code']}\n")
    raise ValueError(layer)


# ---- billed call (gated behind --confirm) -------------------------------

def _extract_json(text: str) -> dict:
    """Lenient: strip a ```json fence, take the outer {...}, and repair illegal
    backslash escapes -- the model writes LaTeX ($\\sqrt[3]{x}$) inside string
    values, and a lone backslash crashes json.loads (same fix as critic.py)."""
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
        return json.loads(re.sub(r'\\(?![\\"/bfnrtu])', r'\\\\', s))


def review_one(packet: dict, *, base_url: str, api_key: str, model: str,
               max_tokens: int = 8000, timeout: int = 180, retries: int = 3) -> dict:
    body = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": _SYSTEM},
            {"role": "user", "content": build_user(packet)},
        ],
        "max_tokens": max_tokens,
        "temperature": 0.2,
        "stream": False,
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{base_url.rstrip('/')}/chat/completions", data=body, method="POST",
        headers={"Content-Type": "application/json",
                 "Authorization": f"Bearer {api_key}"},
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
    msg = data["choices"][0]["message"]
    content = msg.get("content") or ""
    try:
        review = _extract_json(content)
    except Exception:  # noqa: BLE001
        review = None
    return {"raw": content, "review": review, "usage": data.get("usage", {})}


def _write_md(results: list[dict], path: Path) -> None:
    order = {"faithfulness": 0, "register": 1, "decomposition": 2, "engineering": 3}
    results = sorted(results, key=lambda r: (order.get(r["layer"], 9), r.get("unit_id") or ""))
    out = ["# Content cross-review (DeepSeek) -- advisory report\n",
           "> Levels: **1** real-conflict (fix) · **2** discoverability · "
           "**3** editorial-drift · **4** non-finding. Only 1-2 should drive action.\n"]
    cur_layer = None
    for r in results:
        if r["layer"] != cur_layer:
            cur_layer = r["layer"]
            out.append(f"\n## Lens: {cur_layer}\n")
        tag = r.get("unit_id") or "(whole section)"
        rev = r.get("review")
        if not rev:
            out.append(f"### {tag}\n> could not parse JSON; raw:\n```\n"
                       + (r.get("raw") or "")[:1200] + "\n```\n")
            continue
        findings = [f for f in rev.get("findings", []) or []]
        actionable = [f for f in findings if int(f.get("level", 9)) <= 2]
        out.append(f"### {tag}  ({len(actionable)} actionable / {len(findings)} total)")
        if rev.get("summary"):
            out.append(f"_{rev['summary']}_\n")
        for f in sorted(findings, key=lambda x: int(x.get("level", 9))):
            out.append(f"- **L{f.get('level','?')} [{f.get('severity','?')}]** "
                       f"({f.get('where','?')}): {f.get('issue','?')}")
            if f.get("evidence"):
                out.append(f"    - evidence: {f['evidence']}")
            if f.get("suggestion"):
                out.append(f"    - suggest: {f['suggestion']}")
        out.append("")
    path.write_text("\n".join(out) + "\n", encoding="utf-8")


def run_review(packets: list[dict], *, base_url: str, api_key: str, model: str,
               out_dir: Path, smoke: bool = False, delay: float = 0.5) -> "list[dict] | None":
    todo = packets[:1] if smoke else packets
    if not todo:
        print("[review] nothing to review.", flush=True)
        return None
    print(f"[review] reviewing {len(todo)} packet(s) via {model} ...", flush=True)
    results, tin, tout, fails = [], 0, 0, 0
    for n, pk in enumerate(todo):
        label = f"{pk['layer']}:{pk.get('unit_id') or 'section'}"
        print(f"[review] -> {label} ({n + 1}/{len(todo)})", flush=True)
        meta = {"layer": pk["layer"], "unit_id": pk.get("unit_id")}
        try:
            r = review_one(pk, base_url=base_url, api_key=api_key, model=model)
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace")[:300]
            print(f"           HTTP {e.code}: {body}  -- skipped", flush=True)
            fails += 1
            results.append(meta | {"usage": {}, "review": None, "raw": None,
                                   "error": f"HTTP {e.code}: {body}"})
            continue
        except Exception as e:  # noqa: BLE001
            print(f"           error: {e!r}  -- skipped", flush=True)
            fails += 1
            results.append(meta | {"usage": {}, "review": None, "raw": None, "error": repr(e)})
            continue
        u = r["usage"]
        tin += int(u.get("prompt_tokens", 0))
        tout += int(u.get("completion_tokens", 0))
        rev = r["review"]
        if rev is not None:
            acts = [f for f in rev.get("findings", []) or [] if int(f.get("level", 9)) <= 2]
            print(f"           {len(acts)} actionable finding(s)", flush=True)
        else:
            print("           (response not parseable JSON -- kept raw)", flush=True)
        results.append(meta | {"usage": u, "review": rev, "raw": r["raw"]})
        if delay and n < len(todo) - 1:
            time.sleep(delay)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "review.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    _write_md(results, out_dir / "review.md")
    usd = tin / 1e6 * PRICE_IN_PER_MTOK + tout / 1e6 * PRICE_OUT_PER_MTOK
    ok = len(results) - fails
    print(f"\n[review] done: {ok}/{len(results)} ok"
          f"{f', {fails} failed' if fails else ''}; tokens {tin:,} in + {tout:,} out "
          f"-> ~${usd:.4f} (placeholder rates). report -> {out_dir / 'review.md'}", flush=True)
    return results


# ---- dry-run / estimate -------------------------------------------------

def _est_tokens(packet: dict) -> int:
    body = _SYSTEM + build_user(packet)
    return int(len(body) / CHARS_PER_TOKEN)


def dry_run(packets: list[dict], out_dir: Path) -> None:
    pkt_dir = out_dir / "packets"
    pkt_dir.mkdir(parents=True, exist_ok=True)
    in_tok = 0
    print(f"\n[dry-run] {len(packets)} packet(s) assembled; NO API call. "
          f"This is what WOULD be sent to the model:\n", flush=True)
    by_layer: dict[str, int] = {}
    for pk in packets:
        et = _est_tokens(pk)
        in_tok += et
        by_layer[pk["layer"]] = by_layer.get(pk["layer"], 0) + 1
        tag = pk.get("unit_id") or "(section)"
        (pkt_dir / f"{pk['layer']}__{(pk.get('unit_id') or 'section')}.txt").write_text(
            "=== SYSTEM ===\n" + _SYSTEM + "\n\n=== USER ===\n" + build_user(pk),
            encoding="utf-8")
        print(f"  {pk['layer']:14s} {tag:34s} ~{et:5d} in-tok", flush=True)
    out_tok = len(packets) * EST_OUTPUT_TOKENS
    usd = in_tok / 1e6 * PRICE_IN_PER_MTOK + out_tok / 1e6 * PRICE_OUT_PER_MTOK
    print("\n  by lens:", ", ".join(f"{k}={v}" for k, v in by_layer.items()), flush=True)
    print(f"  packets written -> {pkt_dir}", flush=True)
    print(f"\n[estimate] {len(packets)} calls -> ~{in_tok:,} in + ~{out_tok:,} out "
          f"tokens -> ~${usd:.4f} (PLACEHOLDER DeepSeek rates; confirm from the "
          f"smoke run's real usage).", flush=True)
    print("[note] no key was used and no request was sent.", flush=True)


# ---- main ---------------------------------------------------------------

def build_packets(storyboard_path: Path, layers: list[str], tex_override: str | None):
    stem = storyboard_path.stem
    repo = _bootstrap.REPO_ROOT
    script_path = repo / "video" / "content_scripts" / f"{stem}.md"
    hook_path = repo / "video" / "animations" / f"{stem}_hooks.py"
    if not script_path.exists():
        raise SystemExit(f"No content script at {script_path}")

    cs = parse_content_script(script_path)
    units = cs["units"]
    tex_name = source_tex_name(cs["header"], tex_override)
    tex_lines: list[str] = []
    if tex_name:
        tp = (repo / "chapters" / tex_name) if not Path(tex_name).is_absolute() else Path(tex_name)
        if tp.exists():
            tex_lines = tp.read_text(encoding="utf-8").splitlines()
        else:
            print(f"[review] WARN: tex source {tp} not found; faithfulness/engineering "
                  f"will lack source context.", flush=True)

    packets: list[dict] = []
    if "faithfulness" in layers:
        packets += packets_faithfulness(units, tex_lines)
    if "register" in layers:
        packets += packets_register(units)
    if "decomposition" in layers:
        packets.append(packet_decomposition(units))
    if "engineering" in layers:
        eng = packet_engineering(units, hook_path, tex_lines)
        if eng is None:
            print(f"[review] engineering lens skipped: no generated hook code at "
                  f"{hook_path} (only storyboard '# HOOK' intent comments exist).", flush=True)
        else:
            packets.append(eng)
    return units, packets


def main() -> int:
    ap = argparse.ArgumentParser(description="Content cross-review scaffold (offline; billed call gated).")
    ap.add_argument("--storyboard", required=True, type=Path)
    ap.add_argument("--layers", default="faithfulness,register,decomposition,engineering",
                    help="comma list: faithfulness,register,decomposition,engineering")
    ap.add_argument("--tex", default=None, help="override .tex source path (default: parsed from script header)")
    ap.add_argument("--dry-run", action="store_true",
                    help="assemble packets + write them + print estimate; never calls the API")
    ap.add_argument("--confirm", action="store_true",
                    help="actually call DeepSeek (BILLED). Reads key from env DEEPSEEK_API_KEY.")
    ap.add_argument("--smoke", action="store_true", help="with --confirm, review only the FIRST packet")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--base-url", default=DEFAULT_BASE_URL)
    args = ap.parse_args()

    layers = [x.strip() for x in args.layers.split(",") if x.strip()]
    bad = [l for l in layers if l not in _RUBRIC]
    if bad:
        raise SystemExit(f"Unknown layer(s) {bad}. Choose from {list(_RUBRIC)}.")

    storyboard = load_storyboard(args.storyboard)
    deck_id = storyboard["meta"]["id"]
    out_dir = _bootstrap.REPO_ROOT / "video" / "output" / "review" / deck_id

    _, packets = build_packets(args.storyboard, layers, args.tex)
    if not packets:
        print("[review] no packets assembled (check --layers and inputs).", flush=True)
        return 0
    print(f"[review] {deck_id}: {len(packets)} packet(s) across {layers}", flush=True)

    if args.confirm:
        api_key = os.environ.get("DEEPSEEK_API_KEY")
        if not api_key:
            print("[review] --confirm needs the key in env DEEPSEEK_API_KEY "
                  "(never pass it as a flag, never write it to a file).", flush=True)
            return 2
        res = run_review(packets, base_url=args.base_url, api_key=api_key,
                         model=args.model, out_dir=out_dir, smoke=args.smoke)
        return 0 if res else 1
    if args.dry_run:
        dry_run(packets, out_dir)
    else:
        print("[review] packets assembled. Re-run with --dry-run for the send plan + "
              "estimate, or --confirm for the billed review (env DEEPSEEK_API_KEY).", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
