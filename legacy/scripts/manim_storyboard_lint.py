"""Lint a Manim storyboard against MANIM_STORYBOARD.md v1.6 mechanically verifiable rules.

This script enforces the SHOULD/MUST rules from the pre-render checklist that can be checked
without rendering -- specifically the ones the schema (`schemas/manim_storyboard.schema.json`)
and the runtime normaliser (`tools/manim_storyboard_workflow.py::normalize_storyboard`) do not
already enforce. Rules that require natural-language understanding (e.g., whether a voiceover
"verbally calls back" to an earlier math_line, the three-condition 9-sentence carve-out test)
are deliberately omitted; those remain manual audits.

Usage:
    python tools/manim_storyboard_lint.py --deck-id ch01_precise_limit
    python tools/manim_storyboard_lint.py --storyboard inputs/manim_storyboards/foo.yml
    python tools/manim_storyboard_lint.py --all

Exit code: 0 if no error-severity findings; 1 otherwise. Warnings do not fail the lint.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

from manim_storyboard_workflow import load_storyboard, resolve_storyboard_path
from shared_media_paths import DEFAULT_DECK_ID
from shared_runtime_bootstrap import REPO_ROOT
from shared_simple_yaml import load_yaml_path

try:
    from manim_templates.narration_compiler import compile_narration, list_bookmarks
    from manim_templates.reveal_strategy import (
        TEMPLATE_REVEAL_DEFAULTS,
        VALID_STRATEGIES,
        expand_patterns,
    )
    _STRATEGY_AVAILABLE = True
except ImportError:
    _STRATEGY_AVAILABLE = False

ERROR = "error"
WARNING = "warning"

RAW_LATEX_CMD = re.compile(r"\\[a-zA-Z]+")
SUBSCRIPT_PATTERN = re.compile(r"\b[A-Za-z]_[0-9A-Za-z]")
SCENE_ID_RE = re.compile(r"^[a-z][a-z0-9_]*$")
CBRT_VIOLATION = re.compile(r"\*\*\s*\(\s*1\s*/\s*3\s*\)")
META_OPENING = re.compile(r"^\s*(in\s+this\s+(scene|video)|today\s+we\s+will\s+see\s+a\s+scene)", re.IGNORECASE)
SENTENCE_BOUNDARY = re.compile(r"(?<=[.!?])\s+(?=[A-Z(])")

STANDARD_RANGE = (3, 7)  # v1.5: 3-6 target plus +1 boundary tolerance
TRANSITION_RANGE = (1, 5)  # 1-2 baseline, up to 5 for v1.4 concept transitions
EXAMPLE_RANGE = (3, 9)  # up to 9 for procedure+verification carve-out
THEOREM_PROOF_RANGE = (5, 9)  # v1.5 carve-out: statement + proof beats
RECAP_RANGE = (5, 8)  # v1.5 carve-out: one sentence per takeaway plus framing


def split_sentences(text: str) -> list[str]:
    cleaned = re.sub(r"\s+", " ", text.strip())
    if not cleaned:
        return []
    parts = SENTENCE_BOUNDARY.split(cleaned)
    return [p for p in parts if p.strip()]


def voiceover_range_for(template: str) -> tuple[int, int]:
    if template == "section_transition":
        return TRANSITION_RANGE
    if template == "example_walkthrough":
        return EXAMPLE_RANGE
    if template == "theorem_proof":
        return THEOREM_PROOF_RANGE
    if template == "recap_cards":
        return RECAP_RANGE
    return STANDARD_RANGE


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", str(text).strip())


def beat_voiceover_text(scene: dict[str, Any]) -> str:
    beats = scene.get("voiceover_beats") or []
    return normalize_text(" ".join(beat["text"] for beat in beats))


def reveal_ids_for_scene(scene: dict[str, Any]) -> set[str]:
    template = scene.get("template", "")
    data = scene.get("data", {}) if isinstance(scene.get("data"), dict) else {}
    ids = {"title", "header"}

    if template == "title_bullets":
        bullets = data.get("bullets", [])
        ids.update({"bullets"})
        ids.update(f"bullet_{i}" for i in range(len(bullets)))
    elif template == "definition_math":
        math_lines = data.get("math_lines", [])
        support = data.get("supporting_bullets", [])
        ids.update({"label", "rule", "statement", "math_lines", "supporting_bullets"})
        ids.update(f"math_line_{i}" for i in range(len(math_lines)))
        ids.update(f"support_{i}" for i in range(len(support)))
    elif template == "example_walkthrough":
        steps = data.get("steps", [])
        math_lines = data.get("math_lines", [])
        ids.update({"label", "rule", "steps", "math_lines", "takeaway"})
        ids.update(f"step_{i}" for i in range(len(steps)))
        ids.update(f"math_line_{i}" for i in range(len(math_lines)))
        ids.update(f"stage_{i}" for i in range(min(len(steps), len(math_lines))))
    elif template == "graph_focus":
        plots = data.get("plots", [])
        label_count = sum(1 for plot in plots if isinstance(plot, dict) and plot.get("label"))
        annotations = data.get("annotations", [])
        ids.update({"axes", "plots", "labels", "annotations"})
        ids.update(f"plot_{i}" for i in range(len(plots)))
        ids.update(f"label_{i}" for i in range(label_count))
        ids.update(f"annotation_{i}" for i in range(len(annotations)))
    elif template == "procedure_steps":
        steps = data.get("steps", [])
        equations = data.get("worked_equations", [])
        ids.update({"rule", "steps", "equations", "math_lines"})
        ids.update(f"step_{i}" for i in range(len(steps)))
        for i in range(len(equations)):
            ids.add(f"equation_{i}")
            ids.add(f"math_line_{i}")
    elif template == "recap_cards":
        points = data.get("points", [])
        identities = data.get("identities", [])
        ids.update({"rule", "points", "identities", "math_lines"})
        ids.update(f"point_{i}" for i in range(len(points)))
        for i in range(len(identities)):
            ids.add(f"identity_{i}")
            ids.add(f"math_line_{i}")
    elif template == "section_transition":
        upcoming = data.get("upcoming", [])
        ids.update({"rule", "subtitle", "upcoming"})
        ids.update(f"upcoming_{i}" for i in range(len(upcoming)))
    elif template == "theorem_proof":
        proof_steps = data.get("proof_steps", [])
        ids.update({"label", "rule", "statement", "proof_label", "proof_steps", "qed"})
        ids.update(f"proof_step_{i}" for i in range(len(proof_steps)))
    elif template == "comparison":
        left = data.get("left", {}) if isinstance(data.get("left"), dict) else {}
        right = data.get("right", {}) if isinstance(data.get("right"), dict) else {}
        left_count = 1 + len(left.get("items", [])) + (1 if left.get("math") else 0)
        right_count = 1 + len(right.get("items", [])) + (1 if right.get("math") else 0)
        ids.update({"rule", "divider", "left", "right"})
        ids.update(f"left_{i}" for i in range(left_count))
        ids.update(f"right_{i}" for i in range(right_count))
    return ids


def lint_storyboard(
    normalized: dict[str, Any], raw: dict[str, Any]
) -> list[tuple[str, str, str, str]]:
    """Return list of (scene_id, rule, severity, message)."""
    findings: list[tuple[str, str, str, str]] = []
    scenes = normalized.get("scenes", [])
    raw_scenes = raw.get("scenes", []) if isinstance(raw, dict) else []
    raw_by_id: dict[str, dict[str, Any]] = {}
    for raw_scene in raw_scenes:
        if isinstance(raw_scene, dict):
            sid = raw_scene.get("scene_id")
            if isinstance(sid, str):
                raw_by_id[sid] = raw_scene

    if scenes:
        first = scenes[0]
        if first.get("template") != "title_bullets":
            findings.append((
                first.get("scene_id", "<first>"),
                "opening-must-be-title-bullets",
                ERROR,
                f"first scene template is '{first.get('template')}'; opening hook MUST be title_bullets",
            ))
        last = scenes[-1]
        if last.get("template") != "recap_cards":
            findings.append((
                last.get("scene_id", "<last>"),
                "closing-must-be-recap-cards",
                ERROR,
                f"last scene template is '{last.get('template')}'; closing recap MUST be recap_cards",
            ))

    seen_counts: dict[str, int] = {}
    for scene in scenes:
        sid = scene.get("scene_id", "")
        seen_counts[sid] = seen_counts.get(sid, 0) + 1
    for sid, count in seen_counts.items():
        if count > 1:
            findings.append((sid, "duplicate-scene-id", ERROR, f"scene_id appears {count} times"))

    for scene in scenes:
        sid = scene.get("scene_id", "<unknown>")
        template = scene.get("template", "")
        beats = scene.get("voiceover_beats") or []
        voiceover = beat_voiceover_text(scene) if beats else scene.get("voiceover", "")
        scene_exit = scene.get("scene_exit", "fade")
        data = scene.get("data", {})
        raw_scene = raw_by_id.get(sid, {})

        if not SCENE_ID_RE.match(sid):
            findings.append((
                sid,
                "scene-id-snake-case",
                WARNING,
                "scene_id is not snake_case (lowercase letters, digits, underscore)",
            ))

        if template == "definition_math" and "content_type" not in raw_scene:
            findings.append((
                sid,
                "content-type-required-on-definition-math",
                ERROR,
                "definition_math scenes MUST set content_type explicitly (definition / theorem / proposition / lemma / warning)",
            ))

        if beats:
            raw_voiceover = raw_scene.get("voiceover")
            if isinstance(raw_voiceover, str) and normalize_text(raw_voiceover) != normalize_text(voiceover):
                findings.append((
                    sid,
                    "voiceover-beats-source-of-truth",
                    WARNING,
                    "voiceover_beats are present, so their joined text overrides the voiceover field",
                ))
            valid_reveals = reveal_ids_for_scene(scene)
            unknown_reveals = sorted(
                {
                    reveal_id
                    for beat in beats
                    for reveal_id in beat.get("reveal", [])
                    if reveal_id not in valid_reveals
                }
            )
            if unknown_reveals:
                findings.append((
                    sid,
                    "voiceover-beat-unknown-reveal",
                    ERROR,
                    f"voiceover_beats reference unknown reveal id(s): {unknown_reveals[:6]}",
                ))
            if scene.get("hook"):
                findings.append((
                    sid,
                    "voiceover-beats-with-hook",
                    WARNING,
                    "voiceover_beats pace the template renderer; custom hook animations still run after the template unless the hook handles beats itself",
                ))

        if _STRATEGY_AVAILABLE:
            findings.extend(_lint_reveal_strategy(scene, raw_scene, voiceover))

        if META_OPENING.match(voiceover):
            findings.append((
                sid,
                "voiceover-no-meta-opening",
                ERROR,
                "voiceover MUST NOT open with 'In this scene...' or 'In this video...'; start by teaching",
            ))

        latex_hits = sorted({m.group() for m in RAW_LATEX_CMD.finditer(voiceover)})
        if latex_hits:
            findings.append((
                sid,
                "voiceover-no-raw-latex",
                ERROR,
                f"voiceover contains raw LaTeX command(s) {latex_hits[:3]}; rewrite as spoken English",
            ))

        subscript_hits = sorted({m.group() for m in SUBSCRIPT_PATTERN.finditer(voiceover)})
        if subscript_hits:
            findings.append((
                sid,
                "voiceover-no-subscript",
                WARNING,
                f"voiceover contains subscript notation {subscript_hits[:3]}; use spoken form (e.g. 'x one' for x_1)",
            ))

        sentences = split_sentences(voiceover)
        n = len(sentences)
        lo, hi = voiceover_range_for(template)
        if n < lo or n > hi:
            findings.append((
                sid,
                "voiceover-sentence-count",
                WARNING,
                f"voiceover has {n} sentences; expected {lo}-{hi} for template '{template}'",
            ))

        if scene_exit == "fade" and template != "section_transition":
            findings.append((
                sid,
                "scene-exit-fade-non-transition",
                WARNING,
                f"scene_exit 'fade' is recommended only for section_transition; this is '{template}'",
            ))
        if scene_exit == "none" and "scene_exit" in raw_scene:
            findings.append((
                sid,
                "scene-exit-none-needs-comment",
                WARNING,
                "scene_exit 'none' SHOULD have a YAML comment recording the reason",
            ))

        if template == "graph_focus":
            plots = data.get("plots", []) if isinstance(data, dict) else []
            has_hook = bool(raw_scene.get("hook"))
            # Group function plots by expression so a multi-segment piecewise
            # function (same expression in two plot entries) only needs one
            # label between the segments, not one per segment.
            expr_groups: dict[str, dict[str, Any]] = {}
            for index, plot in enumerate(plots):
                if not isinstance(plot, dict):
                    continue
                expr = plot.get("expression", "")
                if isinstance(expr, str) and CBRT_VIOLATION.search(expr):
                    findings.append((
                        sid,
                        "graph-focus-cbrt-required",
                        ERROR,
                        f"plots[{index}] uses '**(1/3)' for cube root; MUST use cbrt(...) instead",
                    ))
                # Hook-rendered scenes draw their own labels and dots; skip checks
                # whose target lives inside the hook code, not the YAML plots.
                if has_hook:
                    continue
                kind = plot.get("kind")
                if kind == "function":
                    group = expr_groups.setdefault(
                        expr if isinstance(expr, str) else "",
                        {"indices": [], "labeled": False},
                    )
                    group["indices"].append(index)
                    if plot.get("label"):
                        group["labeled"] = True
                if kind == "point" and "hollow" not in plot:
                    findings.append((
                        sid,
                        "graph-focus-point-hollow-explicit",
                        WARNING,
                        f"plots[{index}] (kind=point) SHOULD set 'hollow: true' (function undefined / discontinuity) or 'hollow: false' (real point) explicitly; defaulting silently to solid has caused wrong renders",
                    ))
            if not has_hook:
                for expr, info in expr_groups.items():
                    if not info["labeled"]:
                        plot_ids = info["indices"]
                        findings.append((
                            sid,
                            "graph-focus-function-needs-label",
                            ERROR,
                            f"function expression '{expr}' (plots {plot_ids}) has no 'label'; at least one plot of each function MUST set 'label' (e.g. \"$f(x) = ...\") so viewers can identify it",
                        ))

            axes_data = data.get("axes", {}) if isinstance(data, dict) else {}
            if isinstance(axes_data, dict) and axes_data.get("equal_scale"):
                x_range = axes_data.get("x_range", [0, 1, 1])
                y_range = axes_data.get("y_range", [0, 1, 1])
                try:
                    x_span = float(x_range[1]) - float(x_range[0])
                    y_span = float(y_range[1]) - float(y_range[0])
                    x_len = float(axes_data.get("x_length", 8.5))
                    y_len = float(axes_data.get("y_length", 4.8))
                except (TypeError, IndexError, ValueError):
                    x_span = y_span = x_len = y_len = 0.0
                if x_span <= 0 or y_span <= 0:
                    findings.append((
                        sid,
                        "graph-focus-axes-degenerate-range",
                        ERROR,
                        f"axes range has non-positive span (x_span={x_span}, y_span={y_span})",
                    ))
                else:
                    x_unit = x_len / x_span
                    y_unit = y_len / y_span
                    if abs(x_unit - y_unit) / max(x_unit, y_unit) > 0.01:
                        findings.append((
                            sid,
                            "graph-focus-axes-equal-scale-mismatch",
                            ERROR,
                            f"axes.equal_scale=true but x_length/x_span ({x_unit:.4f}) != y_length/y_span ({y_unit:.4f}); adjust lengths so the ratios match",
                        ))

    return findings


def _lint_reveal_strategy(
    scene: dict[str, Any],
    raw_scene: dict[str, Any],
    voiceover: str,
) -> list[tuple[str, str, str, str]]:
    """Validate reveal_strategy / reveal_static / reveal_dynamic / bookmark
    references against the template's reveal contract.
    """
    findings: list[tuple[str, str, str, str]] = []
    sid = scene.get("scene_id", "<unknown>")
    template = scene.get("template", "")

    explicit_strategy = raw_scene.get("reveal_strategy")
    if explicit_strategy is not None:
        if explicit_strategy not in VALID_STRATEGIES:
            findings.append((
                sid,
                "reveal-strategy-invalid",
                ERROR,
                f"reveal_strategy '{explicit_strategy}' is not one of {list(VALID_STRATEGIES)}",
            ))

    valid_reveals = reveal_ids_for_scene(scene)

    static_patterns = raw_scene.get("reveal_static") or []
    if static_patterns:
        if not isinstance(static_patterns, list):
            findings.append((
                sid,
                "reveal-static-must-be-list",
                ERROR,
                "reveal_static must be a YAML list of element ids or wildcard patterns",
            ))
        else:
            resolved = expand_patterns(static_patterns, valid_reveals)
            if not resolved and any(not p.endswith("*") for p in static_patterns):
                # All patterns were exact ids and none matched.
                findings.append((
                    sid,
                    "reveal-static-no-match",
                    WARNING,
                    f"reveal_static {static_patterns} does not match any element produced by template '{template}'",
                ))

    dynamic_patterns = raw_scene.get("reveal_dynamic") or []
    if dynamic_patterns:
        if not isinstance(dynamic_patterns, list):
            findings.append((
                sid,
                "reveal-dynamic-must-be-list",
                ERROR,
                "reveal_dynamic must be a YAML list of element ids or wildcard patterns",
            ))

    # Bookmarks declared inline in voiceover must resolve to a dynamic id.
    narration = compile_narration(scene)
    inline_marks = set(list_bookmarks(narration))
    if inline_marks:
        defaults = TEMPLATE_REVEAL_DEFAULTS.get(template, {})
        candidate_dynamic = expand_patterns(
            raw_scene.get("reveal_dynamic") or defaults.get("dynamic", []),
            valid_reveals,
        )
        candidate_dynamic_set = set(candidate_dynamic) | set(valid_reveals)
        unknown = sorted(m for m in inline_marks if m not in candidate_dynamic_set)
        if unknown:
            findings.append((
                sid,
                "bookmark-unknown-reveal",
                ERROR,
                f"<bookmark mark=...> references id(s) the template will not produce: {unknown[:6]}",
            ))

    # hybrid_auto sanity: if the strategy is hybrid_auto AND voiceover has no
    # bookmarks AND the narration is non-trivial, warn that the renderer will
    # rely on anchor heuristics (whose hit rate the author should sanity-check
    # via evaluate_hybrid_auto.py).
    effective_strategy = explicit_strategy or TEMPLATE_REVEAL_DEFAULTS.get(template, {}).get("strategy")
    if (
        effective_strategy == "hybrid_auto"
        and not inline_marks
        and not scene.get("voiceover_beats")
        and len((voiceover or "").split()) > 12
    ):
        findings.append((
            sid,
            "hybrid-auto-no-bookmarks",
            WARNING,
            "reveal_strategy=hybrid_auto with no bookmarks: anchor heuristics will run; verify with evaluate_hybrid_auto.py",
        ))

    return findings


def collect_storyboard_paths(args: argparse.Namespace) -> list[Path]:
    if args.all:
        return sorted((REPO_ROOT / "inputs" / "manim_storyboards").glob("*.yml"))
    if args.storyboard:
        return [args.storyboard.resolve()]
    return [resolve_storyboard_path(args.deck_id, None)]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Lint Manim storyboard files against MANIM_STORYBOARD.md v1.6 rules."
    )
    parser.add_argument("--deck-id", default=DEFAULT_DECK_ID)
    parser.add_argument("--storyboard", type=Path)
    parser.add_argument(
        "--all",
        action="store_true",
        help="lint every storyboard under inputs/manim_storyboards/",
    )
    args = parser.parse_args()

    paths = collect_storyboard_paths(args)
    if not paths:
        print("No storyboard files to lint.")
        return 0

    has_error = False
    for path in paths:
        rel = path.relative_to(REPO_ROOT) if path.is_relative_to(REPO_ROOT) else path
        try:
            normalized = load_storyboard(path)
            raw = load_yaml_path(path)
        except Exception as exc:
            print(f"[FAIL] {rel}: {exc}")
            has_error = True
            continue

        findings = lint_storyboard(normalized, raw if isinstance(raw, dict) else {})
        if not findings:
            print(f"[OK] {rel}: no findings ({len(normalized.get('scenes', []))} scenes).")
            continue

        errors = sum(1 for f in findings if f[2] == ERROR)
        warnings = sum(1 for f in findings if f[2] == WARNING)
        print(f"[{errors} ERR / {warnings} WARN] {rel}")
        for sid, rule, sev, msg in findings:
            tag = "ERROR" if sev == ERROR else "warn "
            print(f"  {tag} {sid:<35s} {rule:<40s} {msg}")
        if errors:
            has_error = True

    return 1 if has_error else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FileNotFoundError, KeyError, RuntimeError, ValueError) as exc:
        raise SystemExit(str(exc))
