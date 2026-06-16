"""review_pack.py -- engineering packet assembler for the hook-code audit (offline, advisory).

Narrowed sibling of critic.py. critic.py extracts a rendered FRAME for the visual
gate; this assembles the GENERATED manim hook code -- with the animation_cue intent
and the math it must draw -- into ONE packet for the engineering audit:

  gate 1 = a free Claude subagent reading the packet against HOOK-ENGINEERING-RUBRIC.md
  gate 2 = Codex, a single run after convergence (like NFA / copyedit; CLAUDE.md consent)

It pairs with VISUAL-FRAME V8: the frame critic judges the VISIBLE math, this judges
the CODE that generated it (the coordinates / reflections / endpoints you cannot see
on a still frame).

Offline + zero-API by design: it WRITES the packet (rubric verbatim + payload) to
output/<ch>/<sec>/review/engineering-packet.md and stops. No model is called from
here; no key is read. (2026-06-16: the former DeepSeek second-opinion path is
retired; the content lenses faithfulness/register/decomposition moved to
CONTENT-SIXLENS, and the retired chapters/*.tex is no longer read -- the math
context comes from the content script.)

Run (offline, no key):
    python video/pipeline/review_pack.py --storyboard video/storyboards/<deck>.yml
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pipeline import _bootstrap  # noqa: E402

_bootstrap.bootstrap()

import yaml  # noqa: E402

# The engineering audit SSOT. Injected VERBATIM into the packet so the dimensions
# live in exactly one place (HOOK-ENGINEERING-RUBRIC.md) -- the same file gate 2 reads.
RUBRIC_PATH = (Path(__file__).resolve().parent.parent
               / "content_scripts" / "_audit" / "HOOK-ENGINEERING-RUBRIC.md")

# Four-level finding triage (CLAUDE.md), carried in the packet so the reviewer
# judges against this project's deliberate decisions, not generic priors.
_TRIAGE = (
    "Four-level triage (do NOT inflate): 1 real-conflict (violates a stated house "
    "rule) · 2 discoverability · 3 editorial-drift · 4 non-finding "
    "(semantically-equivalent / different-but-correct manim). Report only levels "
    "1-2; a clean read is a valid result. You are READ-ONLY -- propose findings, "
    "never edit the code. Follow the rubric's report format (VERDICT line + findings)."
)


# ---- inputs -------------------------------------------------------------

def load_storyboard(path: Path) -> dict:
    return yaml.safe_load(path.resolve().read_text(encoding="utf-8"))


def load_rubric() -> str:
    """Read the HOOK-ENGINEERING rubric body for verbatim injection. Falls back to
    a one-line pointer if the file is missing, so the assembler never crashes."""
    try:
        return RUBRIC_PATH.read_text(encoding="utf-8").strip()
    except OSError:
        return ("(HOOK-ENGINEERING-RUBRIC.md not found; judge E1 math fidelity "
                "[blocking] + E2 convention against the math context below.)")


_UNIT_HEADER = re.compile(r"^###\s+\d+\.\s+(\S+)")
_FIELD = re.compile(r"^-\s+\*\*([A-Za-z_]+):\*\*\s*(.*)$")


def parse_content_script(md_path: Path) -> dict:
    """Parse the §-content-script markdown into units. Each unit is a
    `### N. <id>` block with `- **field:** value` lines; `narration`/`visual_need`
    /`animation_cue` may continue on indented (or `>`-quoted) follow lines.
    Returns {header, units:[{id, source, learning_goal, kind, narration,
    visual_need, animation_cue}]}."""
    text = md_path.read_text(encoding="utf-8")
    lines = text.splitlines()

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


# ---- packet -------------------------------------------------------------

def packet_engineering(units: list[dict], hook_path: Path) -> dict | None:
    """Assemble the engineering packet: the generated hook code + the animated
    units' intent + the math they must draw. Math context comes from the content
    script (narration carries the math inline as LaTeX, `source` traces to the
    handout). Returns None if there is no hook code yet or no animated units (only
    storyboard '# HOOK' intent comments)."""
    if not hook_path.exists():
        return None
    animated = [u for u in units if u.get("animation_cue")]
    if not animated:
        return None
    cues = [{"id": u["id"], "animation_cue": u["animation_cue"],
             "source_ref": u.get("source", "")} for u in animated]
    math_ctx = "\n\n".join(
        f"[{u['id']}] ({u.get('source', '')})\n"
        f"narration: {u.get('narration', '')}\n"
        f"visual_need: {u.get('visual_need', '')}"
        for u in animated)
    return {"code": hook_path.read_text(encoding="utf-8"),
            "cues": cues, "math_ctx": math_ctx}


def build_packet_text(packet: dict, rubric: str) -> str:
    """The full self-contained packet a gate-1 Claude subagent (or gate-2 Codex)
    reads: the rubric verbatim, the triage rule, then the code + intent + math."""
    cues = "\n".join(f"- [{c['id']}] ({c['source_ref']}): {c['animation_cue']}"
                     for c in packet["cues"])
    return (
        "=== HOOK-ENGINEERING RUBRIC (verbatim) ===\n" + rubric +
        "\n=== END RUBRIC ===\n\n"
        + _TRIAGE + "\n\n"
        "--- animation_cue intent (natural language) ---\n" + cues + "\n\n"
        "--- math context (from content script) ---\n" + packet["math_ctx"] + "\n\n"
        "--- generated manim code ---\n" + packet["code"] + "\n"
    )


# ---- main ---------------------------------------------------------------

def main() -> int:
    # The injected rubric and the animation cues are UTF-8 (Chinese + LaTeX); a
    # Windows cp950 console would otherwise crash when printing them.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass

    ap = argparse.ArgumentParser(
        description="Assemble the engineering audit packet for generated hook code (offline; no API).")
    ap.add_argument("--storyboard", required=True, type=Path)
    args = ap.parse_args()

    repo = _bootstrap.REPO_ROOT
    stem = args.storyboard.stem
    script_path = repo / "video" / "content_scripts" / f"{stem}.md"
    hook_path = repo / "video" / "animations" / f"{stem}_hooks.py"
    if not script_path.exists():
        raise SystemExit(f"No content script at {script_path}")

    storyboard = load_storyboard(args.storyboard)
    meta = storyboard["meta"]
    out_dir = _bootstrap.section_output_dir(meta) / "review"

    units = parse_content_script(script_path)["units"]
    packet = packet_engineering(units, hook_path)
    if packet is None:
        print(f"[review] engineering audit skipped: no generated hook code at "
              f"{hook_path}, or no animated units (only storyboard '# HOOK' intent "
              f"comments). Build animations/{stem}_hooks.py first.", flush=True)
        return 0

    out_dir.mkdir(parents=True, exist_ok=True)
    packet_path = out_dir / "engineering-packet.md"
    packet_path.write_text(build_packet_text(packet, load_rubric()), encoding="utf-8")

    print(f"[review] {meta['id']}: engineering packet ({len(packet['cues'])} animated "
          f"unit(s)) -> {packet_path}", flush=True)
    print("[review] gate 1: hand this packet to a Claude subagent (free) -- it judges "
          "against content_scripts/_audit/HOOK-ENGINEERING-RUBRIC.md (injected above).",
          flush=True)
    print("[review] gate 2: Codex single run after convergence (CLAUDE.md consent).",
          flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
