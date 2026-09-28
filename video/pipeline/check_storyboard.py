"""check_storyboard.py -- the Remotion storyboard entry: structure validation + the
content-layer deterministic checkers, in one run, with each gate's ARMING state said aloud.

Contract: SPEC-remotion-storyboard-schema.md (fields, severities, exit codes). Successor to
the archived Manim gate legacy/manim_video/pipeline/schema.py for the part of it that was
never about templates: required keys, scene kinds, unique ids, well-formed {show} markers,
`pauses:` targets, and the wiring of provenance / source_rev / pedagogy / step_coverage /
example_coverage. No manim, no render, no network.

    python video/pipeline/check_storyboard.py <deck>.yml [<deck2>.yml ...] [--list]

Per gate one header line `[<gate>] <deck>: ...` then `  ERROR  ...` / `  WARN   ...` lines.
Every header also states what the gate could check against (units / anchors / contracts
loaded, scenes scanned) -- "clean" and "nothing was armed" must read differently
(REVIEW_GATES.md section 6.2). Exit 0 = no error; 1 = >=1 error; 2 = a deck could not be
read or parsed. warn-default: a gate's findings become errors only under its per-deck
opt-in flag (meta.otf_enforce / pedagogy_enforce / coverage_enforce /
example_coverage_enforce); source_rev is always warn.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline import example_coverage, pedagogy, provenance, review_pack, source_rev, step_coverage  # noqa: E402
from pipeline.narration import list_reveal_targets, malformed_show_markers  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
SCENE_KINDS = ("intro", "content", "outro", "divider")
SILENT_KINDS = ("intro", "outro", "divider")

# Manim gen-2 fields with no consumer left in video/ (their readers -- scene.py, templates,
# sizecheck, focus.py, pacing.py -- are all in legacy/manim_video/). Written on a Remotion
# deck they are dead weight that LOOKS like it will do something; said, not blocked.
LEGACY_META_FIELDS = ("video", "color_map", "color_map_enforce", "fontfloor_enforce",
                      "layout_enforce", "mathtype_enforce")
LEGACY_SCENE_FIELDS = ("template", "focus", "paced", "carry", "exit", "accent", "scene_role",
                       "hook", "part", "layout", "aside", "anim")

Issue = "tuple[str, str]"


def _pause_issues(sid: str, scene: dict, revealed: "set[str]") -> "list[Issue]":
    """`pauses:` (DESIGN.md): `after` must be a reveal THIS scene makes, `seconds` > 0.
    Errors: a hold that points nowhere has no other symptom."""
    entries = scene.get("pauses")
    if not isinstance(entries, list):
        return [("error", f"{sid}.pauses: must be a list of {{after, seconds}}")]
    issues: list[Issue] = []
    for j, item in enumerate(entries):
        where = f"{sid}.pauses[{j}]"
        if not isinstance(item, dict):
            issues.append(("error", f"{where}: not a mapping (expected {{after, seconds}})"))
            continue
        after, seconds = item.get("after"), item.get("seconds")
        if not isinstance(after, str) or not after:
            issues.append(("error", f"{where}.after: required non-empty reveal id"))
        elif after not in revealed:
            issues.append(("error", f"{where}.after {after!r}: `say` never does {{show {after}}} "
                                    f"(revealed here: {sorted(revealed)})"))
        if not isinstance(seconds, (int, float)) or isinstance(seconds, bool) or seconds <= 0:
            issues.append(("error", f"{where}.seconds: required positive number"))
    return issues


def structure_issues(data) -> "list[Issue]":
    """(severity, message) for the SPEC section 1-3 rules. 'error' = tts.py / the composition
    would misread or crash on it; 'warn' = ignored or dead field."""
    if not isinstance(data, dict):
        return [("error", "top level is not a mapping (expected `meta` + `scenes`)")]
    issues: list[Issue] = []
    meta = data.get("meta")
    if not isinstance(meta, dict):
        issues.append(("error", "meta: missing or not a mapping"))
        meta = {}
    if not isinstance(meta.get("id"), str) or not meta["id"]:
        issues.append(("error", "meta.id: required non-empty string (manifest deck_id)"))
    for key in ("title", "voice", "language", "section", "chapter"):
        if key in meta and not isinstance(meta[key], str):
            issues.append(("warn", f"meta.{key}: present but not a string"))
    for key in LEGACY_META_FIELDS:
        if key in meta:
            issues.append(("warn", f"meta.{key}: Manim gen-2 field, not read by the Remotion line"))

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
        elif sid in seen:
            issues.append(("error", f"{where}.id '{sid}': duplicate (also scenes[{seen[sid]}])"))
        else:
            seen[sid] = i
        kind = scene.get("kind")
        if kind not in SCENE_KINDS:
            issues.append(("error", f"{sid}.kind: {kind!r} not one of {list(SCENE_KINDS)} "
                                    f"(write it: tts.py silently defaults a missing kind to content)"))
        say = scene.get("say")
        if kind == "content":
            revealed: set[str] = set()
            if not isinstance(say, str) or not say.strip():
                issues.append(("error", f"{sid}: content scene needs a non-empty 'say'"))
            else:
                for bad in malformed_show_markers(say):
                    issues.append(("error", f"{sid}: malformed {{show}} marker {bad!r} -- cuts no "
                                            f"beat and TTS would speak it; write {{show <id>}}"))
                targets = list_reveal_targets(say)
                for dup in sorted({t for t in targets if targets.count(t) > 1}):
                    issues.append(("error", f"{sid}: duplicate reveal id {dup!r} in one scene -- the "
                                            f"composition looks beats up by id, so it must be unique "
                                            f"within the scene"))
                revealed = set(targets)
            if "pauses" in scene:
                issues += _pause_issues(sid, scene, revealed)
        elif kind in SILENT_KINDS:
            dur = scene.get("duration")
            if not isinstance(dur, (int, float)) or isinstance(dur, bool) or dur <= 0:
                issues.append(("error", f"{sid}.duration: {kind} scene needs a positive number of "
                                        f"seconds (tts.py would record 0.0)"))
            if isinstance(say, str) and say.strip():
                issues.append(("warn", f"{sid}: {kind} scene has 'say' but {kind} is silent -- ignored"))
            if "pauses" in scene:
                issues.append(("error", f"{sid}: 'pauses' is a content-scene field (this scene is "
                                        f"kind={kind!r})"))
        for key in LEGACY_SCENE_FIELDS:
            if key in scene:
                issues.append(("warn", f"{sid}.{key}: Manim gen-2 field, not read by the Remotion line"))
    return issues


def _print_block(gate: str, name: str, issues: "list[Issue]", note: str,
                 flag: "str | None" = None, enforce: bool = False) -> "tuple[int, int]":
    """One gate's header + findings -> (errors, warnings)."""
    if flag is None:
        mode = "warn-only"
    else:
        mode = "ENFORCED" if enforce else f"warn-only; set meta.{flag} to gate"
    summary = f"{len(issues)} finding(s) ({mode})" if issues else f"clean ({mode})"
    print(f"[{gate}] {name}: {summary} -- {note}")
    for sev, msg in issues:
        print(f"  {'ERROR' if sev == 'error' else 'WARN '}  {msg}")
    n_err = sum(1 for s, _ in issues if s == "error")
    return n_err, len(issues) - n_err


def check_deck(path: Path, data, list_reveals: bool) -> "tuple[int, int]":
    """Run every gate over one loaded deck, print, return (errors, warnings)."""
    name = path.name
    errors = warnings = 0

    issues = structure_issues(data)
    if issues:
        n_err = sum(1 for s, _ in issues if s == "error")
        print(f"[structure] {name}: {n_err} error(s), {len(issues) - n_err} warning(s)")
        for sev, msg in issues:
            print(f"  {'ERROR' if sev == 'error' else 'WARN '}  {msg}")
        errors, warnings = n_err, len(issues) - n_err
    else:
        print(f"[structure] {name}: structure OK")

    meta = data.get("meta") if isinstance(data, dict) else None
    meta = meta if isinstance(meta, dict) else {}
    scenes = [s for s in (data.get("scenes") or []) if isinstance(s, dict)] if isinstance(data, dict) else []
    deck_md = provenance.content_script_for(meta, REPO_ROOT)
    md_rel = deck_md.relative_to(REPO_ROOT).as_posix()

    def add(counts: "tuple[int, int]") -> None:
        nonlocal errors, warnings
        errors, warnings = errors + counts[0], warnings + counts[1]

    # -- provenance (OF2 deterministic layer): per-field for scenes that carry text fields,
    # scene-level `ref:` for the Remotion shape (no text field in the yml).
    enforce = bool(meta.get("otf_enforce"))
    loci = provenance.Loci.from_deck(meta, REPO_ROOT)
    prov = provenance.provenance_issues(data, loci, enforce=enforce) \
        + provenance.scene_ref_issues(data, loci, enforce=enforce)
    scanned = sum(1 for s in scenes if s.get("kind") in provenance.OTF_KINDS)
    md_note = (f"md: {len(loci.md_unit_ids)} unit(s) from {md_rel}" if deck_md.exists()
               else f"md: 0 unit(s) ({md_rel} absent)")
    doc_note = (f"doc: {len(loci.handout_anchors)} anchor(s) from {meta.get('chapter')!r}"
                if meta.get("chapter") else "doc: 0 anchor(s) (no meta.chapter)")
    armed = "" if (loci.md_unit_ids or loci.handout_anchors) else "not armed (no ref: can resolve); "
    add(_print_block("provenance", name, prov,
                     f"{armed}{md_note}; {doc_note}; {scanned} content/divider scene(s) scanned",
                     "otf_enforce", enforce))

    # -- source_rev (always warn): the LOCKED content script vs the handout it was stamped against.
    if not deck_md.exists():
        print(f"[source_rev] {name}: skipped -- {md_rel} absent")
    elif deck_md.name.startswith("_"):
        print(f"[source_rev] {name}: skipped -- {md_rel} is a fixture (`_` prefix)")
    else:
        add(_print_block("source_rev", name, source_rev.check_source_rev(deck_md, REPO_ROOT),
                         f"stamp in {md_rel} vs the current handout source"))

    # -- pedagogy (PD2 / PD3 / PD4): PD2 is keyed on the Manim `template` name, so on a
    # Remotion deck it cannot fire; say so instead of printing a clean line.
    enforce = bool(meta.get("pedagogy_enforce"))
    pd2 = any(s.get("template") in pedagogy._MOTIVE_TEMPLATES for s in scenes)
    dividers = sum(1 for s in scenes if s.get("kind") == "divider")
    registry = meta.get("assumptions")
    add(_print_block("pedagogy", name, pedagogy.pedagogy_issues(data, enforce=enforce),
                     f"PD3 over {dividers} divider(s); PD4 over "
                     f"{len(registry) if isinstance(registry, list) else 0} assumption(s); "
                     f"PD2 {'armed' if pd2 else 'not armed (no scene has template: theorem_proof|derivation)'}",
                     "pedagogy_enforce", enforce))

    # -- SC step-coverage + EX example-coverage: both need the content script.
    md_units = None
    if not deck_md.exists():
        print(f"[coverage] {name}: skipped -- {md_rel} absent")
        print(f"[example_coverage] {name}: skipped -- {md_rel} absent")
    else:
        try:
            md_units = review_pack.parse_content_script(deck_md).get("units", [])
        except Exception as exc:      # fail-closed like schema.py did, but say so instead of staying quiet
            print(f"[coverage] {name}: skipped -- {md_rel} unreadable ({exc})")
            print(f"[example_coverage] {name}: skipped -- {md_rel} unreadable")
    if md_units is not None:
        contracts = {u["id"]: u["screen_contract"] for u in md_units
                     if u.get("id") and u.get("screen_contract")}
        enforce = bool(meta.get("coverage_enforce"))
        reffed = sum(1 for s in scenes if (provenance.parse_ref(s.get("ref")) or ("",))[0] == "md")
        add(_print_block("coverage", name, step_coverage.coverage_issues(data, contracts, enforce=enforce),
                         f"{len(contracts)} contract(s) from {md_rel}; {reffed} scene(s) with md: ref",
                         "coverage_enforce", enforce))
        enforce = bool(meta.get("example_coverage_enforce"))
        section = str(meta.get("section", "")).strip()
        keys = example_coverage.examples_for_deck(meta, REPO_ROOT)
        note = (f"section §{section}: {len(keys)} handout example(s); {len(md_units)} unit(s) declare"
                if keys is not None else
                f"handout section unresolved (meta.chapter={meta.get('chapter')!r}, meta.section={meta.get('section')!r})")
        add(_print_block("example_coverage", name,
                         example_coverage.example_issues(section, keys, md_units, enforce=enforce),
                         note, "example_coverage_enforce", enforce))

    if list_reveals:
        print(f"[list] {name}: reveal ids per content scene (the composition's lookup keys)")
        for s in scenes:
            if s.get("kind") == "content":
                say = s.get("say")
                shown = ", ".join(list_reveal_targets(say) if isinstance(say, str) else [])
                print(f"  {s.get('id')}: {shown or '(none -- all at scene start)'}")
    return errors, warnings


def main(argv: "list[str] | None" = None) -> int:
    import argparse
    for stream in (sys.stdout, sys.stderr):    # findings carry CJK; keep a cp950 console alive
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(description="Validate Remotion storyboard structure and run the "
                                             "content-layer checkers (SPEC-remotion-storyboard-schema.md).")
    ap.add_argument("storyboard", nargs="+", type=Path)
    ap.add_argument("--list", action="store_true", help="also list each content scene's {show} ids")
    args = ap.parse_args(argv)
    import yaml

    rc = 0
    for path in args.storyboard:
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError) as exc:
            print(f"[check_storyboard] {path.name}: cannot read/parse -- {exc}")
            rc = max(rc, 2)
            continue
        n_err, n_warn = check_deck(path, data, args.list)
        print(f"[check_storyboard] {path.name}: {n_err} error(s), {n_warn} warning(s)"
              f"{' -> exit 1' if n_err else ''}")
        rc = max(rc, 1 if n_err else 0)
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
