"""Freshness gate for GENERATED storyboards (the *_mimo.yml drift guard).

derive_spoken.py stamps BOTH generation inputs (the canonical storyboard AND the
<deck>.spoken.yml source) into the generated deck's meta.derived_from; make.py /
tts.py refuse to run a generated deck whose stamps no longer match the files on
disk. Kills the drift class found 2026-07-11: canonical gained Task 14 hooks
AFTER _mimo.yml generation, parity --check still passed, and the stale deck
rendered anyway.

Hashing is LF-normalized (this repo has core.autocrlf=true and no .gitattributes,
so the same file is CRLF in a Windows working tree but LF in the git blob -- a
raw byte hash would false-flag a freshly checked-out deck as stale on an LF
machine). check_derived_freshness stays layout-free: it resolves each stamped
path RELATIVE TO the generated deck's own directory, and never touches malformed
top-level/meta (schema.py owns those diagnostics)."""
from __future__ import annotations

import hashlib
import os
from pathlib import Path
from typing import Any


def text_sha256(path: Path) -> str:
    """sha256 of the file's content normalized to LF, so CRLF/LF working-tree
    differences never change the hash (this repo has core.autocrlf=true). Text
    only -- storyboards/spoken are always UTF-8; a decode error is a real problem
    we WANT to surface, not paper over with a byte hash."""
    normalized = path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def stamp_for(derived_path: Path, *input_paths: Path) -> dict[str, Any]:
    """Build a meta.derived_from stamp: each input's path RELATIVE TO the derived
    file's directory (forward slashes) + its LF-normalized sha256. Relative-to-
    derived keeps the checker free of repo-root detection. Used by BOTH
    derive_spoken.py (to stamp) and the selftest (to build fixtures)."""
    base = derived_path.parent
    return {"inputs": [
        {"path": os.path.relpath(p, base).replace(os.sep, "/"), "sha256": text_sha256(p)}
        for p in input_paths
    ]}


def check_derived_freshness(storyboard_path: Path, data: Any) -> str | None:
    """Error message if `data` (a loaded storyboard) is a stale or unstamped
    generated deck; None when fresh, not a generated deck, or malformed (malformed
    top-level/meta is left for schema_storyboard() to report -- do NOT raise)."""
    if not isinstance(data, dict):
        return None
    meta = data.get("meta")
    if not isinstance(meta, dict):
        return None
    if not str(meta.get("id", "")).endswith("_mimo"):
        return None
    deck = storyboard_path.stem[:-5] if storyboard_path.stem.endswith("_mimo") else storyboard_path.stem
    hint = f"re-run: python video/pipeline/derive_spoken.py --deck {deck}"
    derived = meta.get("derived_from")
    inputs = derived.get("inputs") if isinstance(derived, dict) else None
    if not isinstance(inputs, list) or not inputs:
        return f"{storyboard_path.name}: no derived_from stamp -- {hint}"
    for item in inputs:
        if not isinstance(item, dict) or "path" not in item or "sha256" not in item:
            return f"{storyboard_path.name}: malformed derived_from stamp -- {hint}"
    # Enforce the dual-input contract (B1): the stamp must be EXACTLY the canonical +
    # spoken pair, distinct. A degenerate stamp (single canonical, or canonical stamped
    # twice) otherwise hash-checks fine and silently bypasses the spoken-drift half of the
    # gate -- the gate must ENFORCE the contract, not trust the stamp's completeness.
    expected = {f"{deck}.yml", f"../content_scripts/{deck}.spoken.yml"}
    stamped = [str(item["path"]) for item in inputs]
    if len(stamped) != 2 or set(stamped) != expected:
        return (f"{storyboard_path.name}: derived_from must stamp exactly the canonical + spoken "
                f"pair {sorted(expected)}, got {stamped} -- {hint}")
    base = storyboard_path.parent
    for item in inputs:
        src = (base / str(item["path"])).resolve()
        if not src.exists():
            return f"{storyboard_path.name}: stamped source {item['path']} not found -- {hint}"
        if text_sha256(src) != str(item["sha256"]):
            return f"{storyboard_path.name}: STALE -- {src.name} changed since generation; {hint}"
    return None
