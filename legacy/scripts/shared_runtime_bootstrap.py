from __future__ import annotations

import os
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEPS_DIR = REPO_ROOT / ".deps"
F5_DEPS_DIR = REPO_ROOT / ".deps_f5"
CACHE_DIR = REPO_ROOT / ".cache"
HF_CACHE_DIR = CACHE_DIR / "huggingface"
TTS_CACHE_DIR = CACHE_DIR / "tts"
TORCH_CACHE_DIR = CACHE_DIR / "torch"


def bootstrap_repo_deps(*extra_dirs: Path) -> None:
    for dep_dir in [*extra_dirs, DEPS_DIR]:
        deps_path = str(dep_dir)
        if dep_dir.exists() and deps_path not in sys.path:
            sys.path.insert(0, deps_path)
    ensure_repo_cache_env()


def ensure_repo_cache_env() -> None:
    ensure_directory(CACHE_DIR)
    ensure_directory(HF_CACHE_DIR)
    ensure_directory(TTS_CACHE_DIR)
    ensure_directory(TORCH_CACHE_DIR)
    os.environ.setdefault("HF_HOME", str(HF_CACHE_DIR))
    os.environ.setdefault("TTS_HOME", str(TTS_CACHE_DIR))
    os.environ.setdefault("TORCH_HOME", str(TORCH_CACHE_DIR))


def require_path(path: Path, description: str) -> Path:
    if not path.exists():
        raise FileNotFoundError(f"Missing {description}: {path}")
    return path


def ensure_directory(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path
