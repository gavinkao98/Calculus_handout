"""Atomic file writes: write to <name>.tmp then os.replace (atomic on the same
filesystem). Used for words/aligned/manifest JSON and promoting a verified scene WAV."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


def atomic_write_text(path: Path, text: str, *, encoding: str = "utf-8") -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text, encoding=encoding)
    os.replace(tmp, path)


def atomic_write_json(path: Path, obj: Any) -> None:
    atomic_write_text(path, json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def promote(tmp_path: Path, final_path: Path) -> None:
    """Move a verified temp artifact onto its canonical path (verify-before-overwrite):
    the canonical file is replaced only after validation passed."""
    Path(final_path).parent.mkdir(parents=True, exist_ok=True)
    os.replace(tmp_path, final_path)
