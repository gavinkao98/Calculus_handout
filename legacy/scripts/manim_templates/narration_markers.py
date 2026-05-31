"""Convert between ``<bookmark mark='X'/>`` (machine form) and the Chinese
inline markers used in ``narration.md`` for human proofreading.

Forward (export):  ``<bookmark mark='math_line_0'/>`` -> ``〔顯示式子〕``
Reverse (sync):    ``〔顯示式子〕`` -> ``<bookmark mark='math_line_0'/>``

Because ``〔顯示式子〕`` does not by itself identify the bookmark id, every
exported narration block carries a hidden HTML comment that records the
ordered list of (mark, kind) pairs:

    <!-- bookmark-marks: math_line_0=式子,math_line_1=式子,takeaway=總結 -->

The reverse step relies on this comment as ground truth: the Nth marker in
the prose body is mapped to the Nth entry in the comment. Authors are told
to leave both the markers and the comment alone — see MIGRATION_PLAN §6.

If a marker is missing from the prose body but the comment still lists it,
``parse_marked_narration`` raises a `MarkerCountMismatch` so the sync step
can prompt the human rather than silently dropping the bookmark.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable


# ─── Chinese marker labels by element kind ─────────────────────────────────

# The label the proofreader sees inside the marker bracket. Picked to be
# short, unambiguous Mandarin: 式子 = formula, 步驟 = step, 註記 = annotation,
# 總結 = takeaway, 結束 = QED, 元素 = generic fallback.
MARKER_LABELS: dict[str, str] = {
    "math_line": "式子",
    "identity": "式子",
    "equation": "式子",
    "step": "步驟",
    "proof_step": "步驟",
    "takeaway": "總結",
    "annotation": "註記",
    "qed": "結束",
    "support": "補充",
}
DEFAULT_LABEL = "元素"

MARKER_OPEN = "〔顯示"
MARKER_CLOSE = "〕"

_BOOKMARK_RE = re.compile(r"<bookmark\s*mark\s*=['\"](\w+)[\"\']\s*/>")
_MARKER_RE = re.compile(r"〔顯示([^〕]*)〕")
_HIDDEN_COMMENT_RE = re.compile(r"<!--\s*bookmark-marks:\s*([^>]*?)\s*-->")


# ─── Errors ────────────────────────────────────────────────────────────────


class MarkerCountMismatch(Exception):
    """Raised when proofread markers and the hidden comment disagree."""


# ─── Forward direction: export ─────────────────────────────────────────────


@dataclass
class _MarkerSpec:
    mark: str
    label: str

    def render(self) -> str:
        return f"{MARKER_OPEN}{self.label}{MARKER_CLOSE}"


def _kind_for_mark(mark: str) -> str:
    if mark in MARKER_LABELS:
        return MARKER_LABELS[mark]
    # Strip a trailing _<digits> for numbered ids (math_line_0 -> math_line).
    base = re.sub(r"_\d+$", "", mark)
    return MARKER_LABELS.get(base, DEFAULT_LABEL)


def render_marked_narration(narration: str) -> str:
    """Return narration with bookmarks replaced by Chinese markers and a
    hidden comment listing the original marks in order.
    """
    if not narration:
        return narration

    specs: list[_MarkerSpec] = []
    pieces: list[str] = []
    last = 0
    for m in _BOOKMARK_RE.finditer(narration):
        pieces.append(narration[last : m.start()])
        spec = _MarkerSpec(mark=m.group(1), label=_kind_for_mark(m.group(1)))
        pieces.append(spec.render())
        specs.append(spec)
        last = m.end()
    pieces.append(narration[last:])
    body = "".join(pieces).strip()

    if not specs:
        return body

    descriptor = ",".join(f"{s.mark}={s.label}" for s in specs)
    return f"{body}\n\n<!-- bookmark-marks: {descriptor} -->"


# ─── Reverse direction: sync ───────────────────────────────────────────────


def parse_marker_descriptor(comment_body: str) -> list[tuple[str, str]]:
    """Parse the hidden comment payload into [(mark, label), ...]."""
    parts = [p.strip() for p in comment_body.split(",") if p.strip()]
    out: list[tuple[str, str]] = []
    for part in parts:
        if "=" in part:
            mark, label = part.split("=", 1)
            out.append((mark.strip(), label.strip()))
        else:
            out.append((part.strip(), DEFAULT_LABEL))
    return out


def parse_marked_narration(text: str) -> str:
    """Return the narration with Chinese markers translated back to
    bookmarks, using the hidden comment as ground truth.

    Raises MarkerCountMismatch if the marker count and the comment list
    have different lengths, so the sync tool can refuse to write.
    """
    if not text:
        return ""

    comment_match = _HIDDEN_COMMENT_RE.search(text)
    if not comment_match:
        # No bookmarks were ever recorded — return cleaned narration.
        if _MARKER_RE.search(text):
            raise MarkerCountMismatch(
                "narration has 〔顯示...〕markers but no <!-- bookmark-marks: ... --> "
                "comment to identify them; cannot sync safely."
            )
        return text.strip()

    declared = parse_marker_descriptor(comment_match.group(1))
    body = text[: comment_match.start()] + text[comment_match.end() :]

    marker_positions = list(_MARKER_RE.finditer(body))
    if len(marker_positions) != len(declared):
        raise MarkerCountMismatch(
            f"found {len(marker_positions)} 〔顯示...〕 markers in narration "
            f"but bookmark-marks comment lists {len(declared)}; reconcile manually."
        )

    pieces: list[str] = []
    last = 0
    for spec, m in zip(declared, marker_positions):
        pieces.append(body[last : m.start()])
        pieces.append(f"<bookmark mark='{spec[0]}'/>")
        last = m.end()
    pieces.append(body[last:])
    return "".join(pieces).strip()


# ─── Convenience ───────────────────────────────────────────────────────────


def has_markers(text: str) -> bool:
    return bool(_MARKER_RE.search(text or ""))


def has_descriptor_comment(text: str) -> bool:
    return bool(_HIDDEN_COMMENT_RE.search(text or ""))


def list_declared_marks(text: str) -> list[str]:
    m = _HIDDEN_COMMENT_RE.search(text or "")
    if not m:
        return []
    return [mark for mark, _ in parse_marker_descriptor(m.group(1))]
