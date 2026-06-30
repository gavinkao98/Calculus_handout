"""schema.py -- storyboard structure validation + {show} target enumeration.

The third pre-render gate (after lint.py + sizecheck.py). lint guards text that
would render as garble; sizecheck guards layout overflow; this guards the
STRUCTURE: required keys, scene kinds, unique ids, well-formed {show} markers --
the malformed-YAML / typo'd-kind class of bug that otherwise surfaces as an opaque
KeyError or a silent skip mid-render. It also ENUMERATES every {show <target>}
reveal marker per scene, so an author can eyeball what each scene reveals and when.

NOTE: this validates marker SYNTAX, not whether a target exists in its template's
payload (e.g. that ``{show math.0}`` has a math block index 0). That cross-check
needs per-template ``reveal_targets()`` introspection (task #6) and the manim
layer, so it is deliberately out of scope here -- this gate stays a fast, manim-free
static check on the YAML.

Run standalone:

    python video/pipeline/schema.py video/storyboards/_demo_derivation.yml

``make.py`` runs it automatically before rendering and aborts on any error
(pass ``--skip-schema`` to bypass).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

SCENE_KINDS = ("intro", "content", "outro", "divider")

# A reveal marker: {show <target>} embedded in a content scene's `say`. The target
# is dotted (e.g. math.0, step.2, plot.0, takeaway). `_SHOW_OPEN` finds every
# opener so an unclosed `{show` (missing `}`) can be caught.
_SHOW = re.compile(r"\{show\b([^}]*)\}")
_SHOW_OPEN = re.compile(r"\{show\b")


def reveal_targets(say: str) -> list[str]:
    """Every {show <target>} target in order (stripped); empty string for {show}."""
    return [m.group(1).strip().replace("[", ".").replace("]", "") for m in _SHOW.finditer(say)]


def schema_storyboard(data) -> "list[tuple[str, str]]":
    """Return a list of (severity, message); severity is 'error' or 'warn'.
    'error' aborts the render (broken / unparseable structure); 'warn' is advisory."""
    issues: list[tuple[str, str]] = []

    if not isinstance(data, dict):
        return [("error", "top level is not a mapping (expected `meta` + `scenes`)")]

    meta = data.get("meta")
    if not isinstance(meta, dict):
        issues.append(("error", "meta: missing or not a mapping"))
        meta = {}
    for key in ("id", "section"):
        if not isinstance(meta.get(key), str) or not meta.get(key):
            issues.append(("error", f"meta.{key}: required non-empty string"))
    if "title" in meta and not isinstance(meta.get("title"), str):
        issues.append(("warn", "meta.title: present but not a string"))
    video = meta.get("video")
    if video is not None:
        if not isinstance(video, dict):
            issues.append(("error", "meta.video: must be a mapping {w, h, fps}"))
        else:
            for key in ("w", "h", "fps"):
                if not isinstance(video.get(key), (int, float)) or isinstance(video.get(key), bool):
                    issues.append(("error", f"meta.video.{key}: required number"))

    scenes = data.get("scenes")
    if not isinstance(scenes, list) or not scenes:
        issues.append(("error", "scenes: missing or empty list"))
        scenes = []

    seen: dict[str, int] = {}
    for i, scene in enumerate(scenes):
        where = f"scenes[{i}]"
        if not isinstance(scene, dict):
            issues.append(("error", f"{where}: not a mapping"))
            continue
        sid = scene.get("id")
        if not isinstance(sid, str) or not sid:
            issues.append(("error", f"{where}.id: required non-empty string"))
            sid = where
        else:
            if sid in seen:
                issues.append(("error", f"{where}.id '{sid}': duplicate (also scenes[{seen[sid]}])"))
            seen[sid] = i

        kind = scene.get("kind")
        if kind not in SCENE_KINDS:
            issues.append(("error", f"{sid}.kind: {kind!r} not one of {list(SCENE_KINDS)}"))

        if kind == "content":
            tmpl = scene.get("template")
            if not isinstance(tmpl, str) or not tmpl:
                issues.append(("error", f"{sid}: content scene needs a 'template'"))
            say = scene.get("say")
            if not isinstance(say, str) or not say.strip():
                issues.append(("error", f"{sid}: content scene needs a non-empty 'say'"))
            else:
                if len(_SHOW_OPEN.findall(say)) != len(_SHOW.findall(say)):
                    issues.append(("error", f"{sid}: malformed {{show}} marker (unclosed '}}')"))
                for t in reveal_targets(say):
                    if not t:
                        issues.append(("warn", f"{sid}: empty {{show}} target (reveals nothing)"))
        elif kind in ("intro", "outro"):
            say = scene.get("say")
            if isinstance(say, str) and say.strip():
                issues.append(("warn",
                    f"{sid}: {kind} scene has 'say' but intro/outro are silent -- it is ignored"))

    return issues


def enumerate_reveals(data) -> "list[tuple[str, list[str]]]":
    """(scene_id, [reveal targets]) for every content scene, in order."""
    out: list[tuple[str, list[str]]] = []
    if not isinstance(data, dict):
        return out
    for i, scene in enumerate(data.get("scenes", []) or []):
        if not isinstance(scene, dict) or scene.get("kind") != "content":
            continue
        sid = scene.get("id", f"scenes[{i}]")
        say = scene.get("say")
        out.append((sid, reveal_targets(say) if isinstance(say, str) else []))
    return out


def load_file(path: Path):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from pipeline import _bootstrap

    _bootstrap.bootstrap()
    import yaml

    return yaml.safe_load(path.read_text(encoding="utf-8"))


def main(argv: "list[str] | None" = None) -> int:
    import argparse

    # rubric/markers can be UTF-8; keep a Windows cp950 console from crashing.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass

    parser = argparse.ArgumentParser(
        description="Validate storyboard structure + list {show} reveal targets.")
    parser.add_argument("storyboard", type=Path)
    parser.add_argument("--list", action="store_true",
                        help="also print the per-scene {show} reveal-target enumeration")
    args = parser.parse_args(argv)

    data = load_file(args.storyboard)
    issues = schema_storyboard(data)
    errors = [m for s, m in issues if s == "error"]
    warns = [m for s, m in issues if s == "warn"]

    if issues:
        print(f"[schema] {args.storyboard.name}: {len(errors)} error(s), {len(warns)} warning(s)")
        for sev, msg in issues:
            print(f"  {'ERROR' if sev == 'error' else 'WARN '}  {msg}")
    else:
        print(f"[schema] {args.storyboard.name}: structure OK")

    # OTF provenance (warn-default; gates only when meta.otf_enforce is True)
    from pathlib import Path as _Path
    from pipeline import provenance as _prov
    repo_root = _Path(__file__).resolve().parent.parent.parent
    meta = data.get("meta", {}) if isinstance(data, dict) else {}
    enforce = bool(meta.get("otf_enforce"))
    loci = _prov.Loci.from_deck(meta, repo_root)
    prov = _prov.provenance_issues(data, loci, enforce=enforce)
    if prov:
        p_err = sum(1 for s, _ in prov if s == "error")
        print(f"[provenance] {args.storyboard.name}: {len(prov)} finding(s)"
              f"{' (ENFORCED)' if enforce else ' (warn-only; set meta.otf_enforce to gate)'}")
        for sev, msg in prov:
            print(f"  {'ERROR' if sev == 'error' else 'WARN '}  {msg}")
        if p_err:
            errors = errors + [m for s, m in prov if s == "error"]

    if args.list and not errors:
        print(f"[schema] {args.storyboard.name}: reveal targets per content scene")
        for sid, targets in enumerate_reveals(data):
            shown = ", ".join(t or "(empty)" for t in targets) or "(none -- all at scene start)"
            print(f"  {sid}: {shown}")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
