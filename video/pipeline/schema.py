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


def _focus_issues(sid: str, scene: dict, say) -> "list[tuple[str, str]]":
    """`focus:` dims everything the narration is not on right now (pipeline/focus.py).
    `at` must name a reveal this scene makes -- same reasoning as `pauses.after`: a focus
    keyed to a beat that never happens is invisible with no other symptom. The `dim` ids
    are NOT checked here (block ids only exist once the template has built; sizecheck
    catches a typo'd one, exactly as it does for `{show}` targets)."""
    if "focus" not in scene:
        return []
    entries = scene.get("focus")
    if not isinstance(entries, list):
        return [("error", f"{sid}.focus: must be a list of {{at, dim}}")]
    revealed = set(reveal_targets(say) if isinstance(say, str) else [])
    issues: list[tuple[str, str]] = []
    seen: set[str] = set()
    for j, item in enumerate(entries):
        where = f"{sid}.focus[{j}]"
        if not isinstance(item, dict):
            issues.append(("error", f"{where}: not a mapping (expected {{at, dim}})"))
            continue
        at = item.get("at")
        dim = item.get("dim")
        if not isinstance(at, str) or not at:
            issues.append(("error", f"{where}.at: required non-empty reveal id"))
        elif at not in revealed:
            issues.append(("error", f"{where}.at {at!r}: `say` never does "
                                    f"{{show {at}}} (revealed here: {sorted(revealed)})"))
        elif at in seen:
            issues.append(("error", f"{where}.at {at!r}: already focused by an earlier "
                                    f"entry (one focus per beat; later one would win)"))
        else:
            seen.add(at)
        if not isinstance(dim, list):
            issues.append(("error", f"{where}.dim: required list of block ids "
                                    f"(use [] to restore everything)"))
        elif any(not isinstance(d, str) or not d for d in dim):
            issues.append(("error", f"{where}.dim: every entry must be a non-empty block id"))
        # `indicate` (the rule-3 flash variant, focus.py): optional; ids exist only once
        # the template has built, so like `dim` they are cross-checked in sizecheck.
        if "indicate" in item:
            ind = item.get("indicate")
            if not isinstance(ind, list) or any(not isinstance(i, str) or not i for i in ind):
                issues.append(("error", f"{where}.indicate: must be a list of non-empty "
                                        f"block ids"))
            elif isinstance(dim, list):
                for both in [i for i in ind if i in dim]:
                    issues.append(("error", f"{where}.indicate {both!r}: also in this entry's "
                                            f"dim (cannot flash and dim one block in one beat)"))
    return issues


def _paced_issues(sid: str, scene: dict, say) -> "list[tuple[str, str]]":
    """`paced:` walks a block's parts across its whole beat (pipeline/pacing.py). Same
    reasoning as `focus.at` / `pauses.after`: a paced id the narration never reveals is
    silently inert, so require it to name a reveal this scene makes."""
    if "paced" not in scene:
        return []
    entries = scene.get("paced")
    if not isinstance(entries, list) or any(not isinstance(e, str) or not e for e in entries):
        return [("error", f"{sid}.paced: must be a list of reveal ids")]
    revealed = set(reveal_targets(say) if isinstance(say, str) else [])
    issues: list[tuple[str, str]] = []
    for bid in entries:
        if bid not in revealed:
            issues.append(("error", f"{sid}.paced {bid!r}: `say` never does {{show {bid}}} "
                                    f"(revealed here: {sorted(revealed)})"))
    if len(set(entries)) != len(entries):
        issues.append(("error", f"{sid}.paced: duplicate id"))
    return issues


def _pause_issues(sid: str, scene: dict, say) -> "list[tuple[str, str]]":
    """`pauses:` is an authored silent hold after a reveal (pipeline/pauses.py). Its
    `after` must name a reveal this scene actually makes -- a typo'd one would otherwise
    be a hold nobody ever sees, with no other symptom. Errors, not warnings: a pause that
    points nowhere is always a mistake."""
    if "pauses" not in scene:
        return []
    entries = scene.get("pauses")
    if not isinstance(entries, list):
        return [("error", f"{sid}.pauses: must be a list of {{after, seconds}}")]
    revealed = set(reveal_targets(say) if isinstance(say, str) else [])
    issues: list[tuple[str, str]] = []
    for j, item in enumerate(entries):
        where = f"{sid}.pauses[{j}]"
        if not isinstance(item, dict):
            issues.append(("error", f"{where}: not a mapping (expected {{after, seconds}})"))
            continue
        after = item.get("after")
        seconds = item.get("seconds")
        if not isinstance(after, str) or not after:
            issues.append(("error", f"{where}.after: required non-empty reveal id"))
        elif after not in revealed:
            issues.append(("error", f"{where}.after {after!r}: `say` never does "
                                    f"{{show {after}}} (revealed here: {sorted(revealed)})"))
        if not isinstance(seconds, (int, float)) or isinstance(seconds, bool) or seconds <= 0:
            issues.append(("error", f"{where}.seconds: required positive number"))
    return issues


_CARRY_CORNERS = ("top_left", "top_right", "bottom_left", "bottom_right")


def _prev_content_in_act(scenes: list, index: int) -> "str | None":
    """Id of the content scene right before scenes[index] inside the same act, or None
    when this scene opens its act. An act is what lies between two brand frames, so the
    first scene met walking back is either that content scene or a boundary."""
    for s in reversed(scenes[:index]):
        if isinstance(s, dict):
            return s.get("id") if s.get("kind") == "content" else None
    return None


def _carry_issues(sid: str, scene: dict, say, scenes: list, index: int) -> "list[tuple[str, str]]":
    """`carry:` brings a block the PREVIOUS content scene built into this one
    (templates._apply_carry; SPEC-motion-language rule 1). `from` must be exactly that
    scene -- the one right before this inside the same act -- because a carried object only
    reads as "the same object" across the cut make.py hard-cuts for it (_segment_fades),
    and a divider between them is a new canvas by definition. `block` existence needs the
    built blocks, so sizecheck owns it (as for {show} targets and focus.dim); `as` is
    checked against the scene's own blocks there too."""
    if "carry" not in scene:
        return []
    entries = scene.get("carry")
    if not isinstance(entries, list):
        return [("error", f"{sid}.carry: must be a list of {{from, block, as, to}}")]
    prev = _prev_content_in_act(scenes, index)
    revealed = set(reveal_targets(say) if isinstance(say, str) else [])
    issues: list[tuple[str, str]] = []
    seen_as: set[str] = set()
    for j, item in enumerate(entries):
        where = f"{sid}.carry[{j}]"
        if not isinstance(item, dict):
            issues.append(("error", f"{where}: not a mapping (expected {{from, block, as, to}})"))
            continue
        src = item.get("from")
        if not isinstance(src, str) or not src:
            issues.append(("error", f"{where}.from: required non-empty scene id"))
        elif prev is None:
            issues.append(("error", f"{where}.from {src!r}: this scene opens its act (no content "
                                    f"scene since the last divider) -- nothing to carry from"))
        elif src != prev:
            issues.append(("error", f"{where}.from {src!r}: must be the content scene right "
                                    f"before this one in the same act ({prev!r})"))
        blk = item.get("block")
        if isinstance(blk, list):
            if not blk or any(not isinstance(b, str) or not b for b in blk):
                issues.append(("error", f"{where}.block: a list must hold non-empty block ids"))
        elif not isinstance(blk, str) or not blk:
            issues.append(("error", f"{where}.block: required non-empty block id (or a list of ids "
                                    f"carried as one group)"))
        as_id = item.get("as")
        if not isinstance(as_id, str) or not as_id:
            issues.append(("error", f"{where}.as: required non-empty block id"))
            as_id = None
        elif as_id in seen_as:
            issues.append(("error", f"{where}.as {as_id!r}: duplicate (another entry already "
                                    f"carries under that id)"))
        else:
            seen_as.add(as_id)
        to = item.get("to", "keep")
        if to == "keep":
            if as_id in revealed:
                issues.append(("error", f"{where}: `to: keep` puts {as_id!r} on screen from t=0, "
                                        f"but `say` does {{show {as_id}}} -- drop the marker or "
                                        f"use `to: {{corner, scale}}`"))
        elif isinstance(to, dict):
            if to.get("corner") not in _CARRY_CORNERS:
                issues.append(("error", f"{where}.to.corner: required one of {list(_CARRY_CORNERS)}"))
            scale = to.get("scale", 1.0)
            if not isinstance(scale, (int, float)) or isinstance(scale, bool) or scale <= 0:
                issues.append(("error", f"{where}.to.scale: must be a positive number"))
            if as_id is not None and as_id not in revealed:
                issues.append(("warn", f"{where}: `say` never does {{show {as_id}}}, so the flight "
                                       f"to the corner runs at scene end (after the last beat)"))
        else:
            issues.append(("error", f"{where}.to: 'keep' or a mapping {{corner, scale}}"))
    return issues


def _exit_issues(sid: str, scene: dict) -> "list[tuple[str, str]]":
    """`exit:` fades the named blocks out in the scene's tail (scene.py _tail). Shape only;
    the ids need the built blocks, so sizecheck cross-checks them (as for focus.dim)."""
    if "exit" not in scene:
        return []
    entries = scene.get("exit")
    if not isinstance(entries, list) or any(not isinstance(e, str) or not e for e in entries):
        return [("error", f"{sid}.exit: must be a list of block ids")]
    if len(set(entries)) != len(entries):
        return [("error", f"{sid}.exit: duplicate id")]
    return []
def _color_map_issues(meta: dict) -> "list[tuple[str, str]]":
    """`meta.color_map` (SPEC-motion-language rule 5; kickoff T1-1): tex token -> palette role,
    read by brand.math_line for every math line in the deck. theme.color() falls back to
    `primary` on a role it does not know -- silently -- so a typo'd role would render as plain
    ink with no other symptom; this is where it gets said. warn-default, error under
    meta.color_map_enforce (the pedagogy.assumptions_registry_issues shape)."""
    if "color_map" not in meta:
        return []
    sev = "error" if meta.get("color_map_enforce") else "warn"
    cmap = meta.get("color_map")
    if not isinstance(cmap, dict):
        return [(sev, "meta.color_map: must be a mapping {tex token: palette role}")]
    from pipeline.visuals import theme
    roles = theme.palette("dark")
    issues: list[tuple[str, str]] = []
    for key, role in cmap.items():
        if not isinstance(key, str) or not key.strip():
            issues.append((sev, f"meta.color_map[{key!r}]: key must be a non-empty tex token "
                                f"(e.g. '\\\\theta', 'h')"))
        elif not isinstance(role, str) or role not in roles:
            issues.append((sev, f"meta.color_map[{key!r}]: {role!r} is not a palette role "
                                f"(theme.color would silently fall back to primary); "
                                f"use a key of theme.DARK, e.g. concept / result / caution"))
    return issues


def _proof_row_issues(sid: str, scene: dict) -> "list[tuple[str, str]]":
    """theorem_proof `proof[]` dict rows (rollout T1-3): `{tex, anim: transform, frame}`. `tex`
    is required; `frame` needs `anim: transform` as in derivation; `cancel` is derivation-only
    (a proof row has no `{{...}}` segment contract to index into). String rows are untouched."""
    issues: list[tuple[str, str]] = []
    for j, row in enumerate(scene.get("proof") or []):
        if not isinstance(row, dict):
            continue
        where = f"{sid}.proof[{j}]"
        anim = row.get("anim")
        if not isinstance(row.get("tex"), str) or not row["tex"].strip():
            issues.append(("error", f"{where}.tex: required non-empty string"))
        if anim == "cancel" or row.get("cancel") is not None:
            issues.append(("error", f"{where}: anim: cancel is derivation-only "
                                    f"(a proof row takes anim: transform)"))
        elif row.get("frame") and anim != "transform":
            issues.append(("error", f"{where}.frame: only applies with anim: transform "
                                    f"(this row: {anim!r})"))
    return issues


def _derivation_issues(sid: str, scene: dict) -> "list[tuple[str, str]]":
    """derivation rows' `anim: cancel` + `cancel: [i, ...]` and `frame: true` (kickoff T3-3 /
    T2-2). A cancel index points into the PREVIOUS row's `{{...}}` segments, so it needs a
    previous row, that row needs segments, and every index must fall inside them -- an index
    that misses is an IndexError mid-render, a `cancel:` without `anim: cancel` (or a `frame`
    on a plain reveal) is silently inert. Errors: each is always a mistake. theorem_proof's
    `proof[]` dict rows get the same treatment via _proof_row_issues (rollout T1-3)."""
    if scene.get("template") == "theorem_proof":
        return _proof_row_issues(sid, scene)
    if scene.get("template") != "derivation":
        return []
    from pipeline import texparts
    rows: list[tuple[str, dict]] = []      # (where, row) in the template's order; check has a fixed reveal
    if scene.get("steps") is not None or scene.get("result") is not None:
        for j, st in enumerate(scene.get("steps") or []):
            rows.append((f"{sid}.steps[{j}]", st if isinstance(st, dict) else {"math": st}))
        if scene.get("result") is not None:
            r = scene["result"]
            rows.append((f"{sid}.result", r if isinstance(r, dict) else {"math": r}))
    else:
        for j, ln in enumerate(scene.get("lines") or []):
            ln = ln if isinstance(ln, dict) else {"tex": ln}
            rows.append((f"{sid}.lines[{j}]", {**ln, "math": ln.get("tex", "")}))
    issues: list[tuple[str, str]] = []
    for j, (where, row) in enumerate(rows):
        anim = row.get("anim")
        cancel = row.get("cancel")
        if row.get("frame") and anim not in ("transform", "cancel"):
            issues.append(("error", f"{where}.frame: only applies with anim: transform | cancel "
                                    f"(this row: {anim!r})"))
        if cancel is not None and anim != "cancel":
            issues.append(("error", f"{where}.cancel: needs anim: cancel (this row: {anim!r})"))
        if anim != "cancel":
            continue
        if j == 0:
            issues.append(("error", f"{where}: anim: cancel has no previous row to cancel from"))
            continue
        prev = str(rows[j - 1][1].get("math", ""))
        if not texparts.has_segments(prev):
            issues.append(("error", f"{where}: anim: cancel needs the previous row cut into "
                                    f"{{{{...}}}} segments to point at"))
            continue
        n = len(texparts.split_segments(prev))
        if (not isinstance(cancel, list) or not cancel
                or any(isinstance(c, bool) or not isinstance(c, int) for c in cancel)):
            issues.append(("error", f"{where}.cancel: required list of segment indexes into the "
                                    f"previous row (0..{n - 1})"))
            continue
        for c in cancel:
            if not 0 <= c < n:
                issues.append(("error", f"{where}.cancel[{c}]: previous row has {n} segment(s) "
                                        f"(0..{n - 1})"))
    return issues


def _seg_roles_issues(sid: str, scene: dict) -> "list[tuple[str, str]]":
    """derivation rows' `seg_roles: {segment tex: palette role}` (kickoff rollout T2-1): a
    whole `{{...}}` segment in one role colour. Each key must be one of the row's segments
    (the tex inside `{{...}}`, stripped) and each role a palette key -- a miss is silent at
    render (brand skips a row without segments or a key that matches nothing; theme.color
    falls back to primary on an unknown role), so it is said here. Errors: each is always a
    mistake. steps[i] / result / check / lines[] dict rows; theorem_proof's `proof[]` dict
    rows get the same three checks (rollout T2-3), their `tex` field standing in for
    derivation's `math`."""
    template = scene.get("template")
    if template not in ("derivation", "theorem_proof"):
        return []
    from pipeline import texparts
    from pipeline.visuals import theme
    rows: list[tuple[str, dict]] = []
    if template == "theorem_proof":
        for j, row in enumerate(scene.get("proof") or []):
            if isinstance(row, dict):
                rows.append((f"{sid}.proof[{j}]", {**row, "math": row.get("tex", "")}))
    elif scene.get("steps") is not None or scene.get("result") is not None:
        for j, st in enumerate(scene.get("steps") or []):
            if isinstance(st, dict):
                rows.append((f"{sid}.steps[{j}]", st))
        for key in ("result", "check"):
            if isinstance(scene.get(key), dict):
                rows.append((f"{sid}.{key}", scene[key]))
    else:
        for j, ln in enumerate(scene.get("lines") or []):
            if isinstance(ln, dict):
                rows.append((f"{sid}.lines[{j}]", {**ln, "math": ln.get("tex", "")}))
    roles = theme.palette("dark")
    issues: list[tuple[str, str]] = []
    for where, row in rows:
        if "seg_roles" not in row:
            continue
        seg_roles = row["seg_roles"]
        if not isinstance(seg_roles, dict):
            issues.append(("error", f"{where}.seg_roles: must be a mapping "
                                    f"{{segment tex: palette role}}"))
            continue
        math = str(row.get("math", ""))
        if not texparts.has_segments(math):
            issues.append(("error", f"{where}.seg_roles: the row has no {{{{...}}}} segments "
                                    f"to colour"))
            continue
        segs = texparts.split_segments(math)
        for key, role in seg_roles.items():
            if str(key).strip() not in segs:
                issues.append(("error", f"{where}.seg_roles[{key!r}]: matches no segment of "
                                        f"the row (segments: {segs})"))
            if not isinstance(role, str) or role not in roles:
                issues.append(("error", f"{where}.seg_roles[{key!r}]: {role!r} is not a palette "
                                        f"role (theme.color would silently fall back to "
                                        f"primary); use a key of theme.DARK, e.g. secondary / "
                                        f"accent / success"))
    return issues


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
    issues += _color_map_issues(meta)

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
            issues += _pause_issues(sid, scene, scene.get("say"))
            issues += _focus_issues(sid, scene, scene.get("say"))
            issues += _paced_issues(sid, scene, scene.get("say"))
            issues += _carry_issues(sid, scene, scene.get("say"), scenes, i)
            issues += _exit_issues(sid, scene)
            issues += _derivation_issues(sid, scene)
            issues += _seg_roles_issues(sid, scene)
        elif "pauses" in scene:
            issues.append(("error", f"{sid}: 'pauses' is a content-scene field "
                                    f"(this scene is kind={kind!r})"))
        elif "focus" in scene:
            issues.append(("error", f"{sid}: 'focus' is a content-scene field "
                                    f"(this scene is kind={kind!r})"))
        elif "carry" in scene:
            issues.append(("error", f"{sid}: 'carry' is a content-scene field "
                                    f"(this scene is kind={kind!r})"))
        elif "exit" in scene:
            issues.append(("error", f"{sid}: 'exit' is a content-scene field "
                                    f"(this scene is kind={kind!r})"))

        if kind in ("intro", "outro"):
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
    meta = data.get("meta") if isinstance(data, dict) else None
    meta = meta if isinstance(meta, dict) else {}
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

    # source_rev freshness (warn-only, never gates): the LOCKED content script vs the handout
    # source it was stamped against. Drift is the CONTENT_METHODOLOGY.md §8 trigger (assessment
    # F2, 2026-09-07: §3.1/§3.2 sources were edited three times after lock and nothing said so).
    from pipeline import source_rev as _srev
    srev = _srev.check_source_rev(_srev.md_for_deck(meta, repo_root), repo_root)
    if srev:
        print(f"[source_rev] {args.storyboard.name}: {len(srev)} finding(s) (warn-only)")
        for _sev, msg in srev:
            print(f"  WARN   {msg}")

    # Pedagogy structural checks (warn-default; gates only when meta.pedagogy_enforce is True)
    from pipeline import pedagogy as _ped
    ped_enforce = bool(meta.get("pedagogy_enforce"))
    ped = _ped.pedagogy_issues(data, enforce=ped_enforce)
    if ped:
        ped_err = sum(1 for s, _ in ped if s == "error")
        print(f"[pedagogy] {args.storyboard.name}: {len(ped)} finding(s)"
              f"{' (ENFORCED)' if ped_enforce else ' (warn-only; set meta.pedagogy_enforce to gate)'}")
        for sev, msg in ped:
            print(f"  {'ERROR' if sev == 'error' else 'WARN '}  {msg}")
        if ped_err:
            errors = errors + [m for s, m in ped if s == "error"]

    # SC step-coverage (warn-default; gates only when meta.coverage_enforce is True)
    from pipeline import step_coverage as _cov
    from pipeline import review_pack as _rp
    cov_enforce = bool(meta.get("coverage_enforce"))
    # "<deck>_mimo" shares the base deck's .md (and thus its screen_contracts) -- the
    # un-stripped lookup here made the generated canonical deck fail SC on every proof
    # unit ('no screen_contract'); found by doctor --smoke 2026-09-12.
    deck_md = _prov.content_script_for(meta, repo_root)
    contracts = {}
    md_units: list = []
    if deck_md.exists():
        try:
            md_units = _rp.parse_content_script(deck_md).get("units", [])
            for u in md_units:
                if u.get("id") and u.get("screen_contract"):
                    contracts[u["id"]] = u["screen_contract"]
        except Exception:
            contracts = {}     # fail-closed: unreadable .md -> no contracts -> no SC noise
            md_units = []
    cov_issues = _cov.coverage_issues(data, contracts, enforce=cov_enforce)
    if cov_issues:
        cov_err = sum(1 for s, _ in cov_issues if s == "error")
        print(f"[coverage] {args.storyboard.name}: {len(cov_issues)} finding(s)"
              f"{' (ENFORCED)' if cov_enforce else ' (warn-only; set meta.coverage_enforce to gate)'}")
        for sev, msg in cov_issues:
            print(f"  {'ERROR' if sev == 'error' else 'WARN '}  {msg}")
        if cov_err:
            errors = errors + [m for s, m in cov_issues if s == "error"]

    # -- EX: 例題折疊宣告閘 (example_coverage.py). Declarations live in the .md next to
    # the screen_contracts above; the storyboard is deliberately NOT read (scene order and
    # splitting are the video's business -- CONTENT_METHODOLOGY.md §1 分工). Wired HERE
    # only, not in make.py: SC is the precedent (make.py repeats provenance/source_rev/
    # pedagogy but never coverage), and which examples to teach is an authoring-time
    # decision that should not block a render. Clean -> prints nothing.
    # A deck with NO .md is skipped entirely (same as SC): ch01_inverse_functions is a
    # gen-1 layout-regression deck with no content script, so "zero declarations" there
    # means "nobody has written one yet", not "8 examples were dropped" -- running the
    # gate on it would fire one EX1 per handout example and say nothing true.
    from pipeline import example_coverage as _ex
    ex_enforce = bool(meta.get("example_coverage_enforce"))
    ex_issues = [] if not deck_md.exists() else _ex.example_issues(
        str(meta.get("section", "")).strip(),
        _ex.examples_for_deck(meta, repo_root),
        md_units, enforce=ex_enforce)
    if ex_issues:
        ex_err = sum(1 for s, _ in ex_issues if s == "error")
        print(f"[example_coverage] {args.storyboard.name}: {len(ex_issues)} finding(s)"
              f"{' (ENFORCED)' if ex_enforce else ' (warn-only; set meta.example_coverage_enforce to gate)'}")
        for sev, msg in ex_issues:
            print(f"  {'ERROR' if sev == 'error' else 'WARN '}  {msg}")
        if ex_err:
            errors = errors + [m for s, m in ex_issues if s == "error"]

    if args.list and not errors:
        print(f"[schema] {args.storyboard.name}: reveal targets per content scene")
        for sid, targets in enumerate_reveals(data):
            shown = ", ".join(t or "(empty)" for t in targets) or "(none -- all at scene start)"
            print(f"  {sid}: {shown}")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
