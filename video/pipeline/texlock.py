"""Per-cwd mutual exclusion for the pipeline's TeX-building segments.

Every gate that builds blocks (`sizecheck.check_scenes`, `critic.plan_frames`'s
`graph_label_geometry`, `make.py`'s pre-render sizecheck and its render loop,
`scratch_frames.py`) compiles LaTeX through manim into ``config.media_dir``/Tex.
manim writes each snippet as ``<hash>.tex`` -> ``.dvi`` -> ``.svg`` in that one
directory with no locking of its own, so two programs sharing a cwd interleave on
the same files and one of them loses the race:

    SIZE   slope_chain: could not build scene (PermissionError(13, ...))
    SIZE   capacity_probe: could not build scene (FileNotFoundError(2, ...))

Those errors are **false** -- the scene is fine, the file was simply deleted or
still open when the other process reached for it. Measured 2026-09-14 on a cold
Tex cache: two concurrent `sizecheck.py _demo_derivation.yml` in one cwd produced
a bogus `could not build scene` in 3 of 3 rounds. The standing mitigation was a
line of documentation ("never run two report passes in one worktree",
KICKOFF-shared-layer-v1 §8 (8)) which cannot see the background process the user
forgot about, and which cost r1 Task C and the §3.2 session real debugging time.

So the TeX segments take a lock file instead. Scope notes:

* **Granularity is the whole segment, not one Tex build.** Locking per snippet
  would let the two programs interleave anyway and keep writing over each
  other's cache entries; the point is that one program owns the Tex directory
  from its first build to its last.
* **Per cwd, by construction.** The lock lives at ``<media_dir>/Tex.lock``, i.e.
  ``./media/Tex.lock`` under manim's default `media_dir`, so two worktrees (or any
  two different working directories) never block each other -- which matches where
  the race actually is (§8 (8): the `media/Tex` contention is per-cwd; MiKTeX's
  global fndb lock is a different, hang-shaped failure this does not address).
  Beside the Tex directory, not inside it -- see `lock_path`.
* **Re-entrant within one process.** `make.py` holds the lock across its
  pre-render sizecheck, and `check_scenes` takes it again from the inside; the
  depth counter makes the inner `with` a no-op instead of a ten-minute
  self-deadlock.
* **No new dependency.** `os.open(O_CREAT | O_EXCL)` is atomic on both Windows
  and POSIX, which is all a mutex between cooperating processes needs; `filelock`
  would buy nothing here and every dependency has to be installed on every
  machine (CLAUDE.md).

A holder that dies without cleaning up (Ctrl-C on a render, a killed
`latex.exe`) leaves the file behind, so a lock is reclaimed as stale once it is
both older than `STALE_SECONDS` **and** owned by a pid that no longer exists --
both conditions, because a legitimate full-deck render holds the lock far longer
than the staleness window while very much alive.

`DEFAULT_TIMEOUT` is 30 min (raised from 10 at the r2 merge, 2026-09-14): a full-deck
render holds the lock for 15-25 min, and a gate started in the same cwd DURING such a
render should wait it out rather than raise -- the every-10-s progress line is what keeps
that wait from looking like a hang. It stays finite so a wedged holder that is somehow
alive but stuck cannot block a cwd forever; pass `timeout=` to tighten it for a gate.
"""
from __future__ import annotations

import contextlib
import os
import time
from pathlib import Path

RETRY_SECONDS = 0.5         # poll interval while another process holds the lock
DEFAULT_TIMEOUT = 1800.0    # 30 min: outlasts a full-deck render (15-25 min) so a waiter waits it out;
                            # still finite so a wedged holder cannot block forever (r2 merge ruling)
STALE_SECONDS = 900.0       # 15 min untouched AND a dead pid -> reclaim
PROGRESS_SECONDS = 10.0     # say something every 10 s so a wait never looks like a hang

_depth = 0                  # >0 = this process already holds the lock (re-entrancy)


def lock_path() -> Path:
    """`<media_dir>/Tex.lock` -- beside the Tex directory, deliberately NOT inside it.

    manim calls `tex_file_writing.delete_nonsvg_files()` after every Tex->SVG
    conversion, and it unlinks EVERY file in `media/Tex` whose suffix is not `.svg`
    or `.tex`. A lock file kept in there is therefore swept away by the very builds
    it is guarding: measured 2026-09-14, the second process took the "free" lock
    ~1 s in while the first still held it, and both then raced as before. (That same
    sweep is half of why the race is destructive at all -- it deletes the OTHER
    process's `.dvi`/`.log` mid-build, which is the `FileNotFoundError` half of the
    false errors.) So the lock sits one level up, where nothing housekeeps it.

    Resolved at acquisition time rather than cached at import: `make.py` changes
    `media_dir` per scene inside `tempconfig`, and the lock must key off the cwd-level
    directory the report gates share, not off whatever a scene is set to."""
    from manim import config

    return Path(config.get_dir("media_dir")) / "Tex.lock"


def _pid_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    if os.name == "nt":
        import subprocess

        out = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"],
                             capture_output=True, text=True).stdout
        return any(field == str(pid) for line in out.splitlines() for field in line.split())
    try:
        os.kill(pid, 0)         # signal 0 = existence check, no signal delivered
    except ProcessLookupError:
        return False
    except PermissionError:
        return True             # someone else's process -- alive, just not ours
    return True


def _holder(path: Path) -> "tuple[int, str]":
    """(pid, reason) written by the current holder; (0, '?') if unreadable.

    Unreadable covers two normal cases, not just corruption: the holder released the
    lock between our failed create and this read, and the holder created the file but
    has not written its payload yet."""
    try:
        parts = path.read_text(encoding="utf-8").splitlines()
        return int(parts[0]), (parts[1] if len(parts) > 1 else "?")
    except (OSError, ValueError, IndexError):
        return 0, "?"


def _is_stale(path: Path, pid: int) -> bool:
    try:
        age = time.time() - path.stat().st_mtime
    except OSError:
        return False
    return age > STALE_SECONDS and not _pid_alive(pid)


@contextlib.contextmanager
def tex_lock(*, reason: str, timeout: float = DEFAULT_TIMEOUT):
    """Hold the per-cwd TeX build lock for the duration of the block.

    `reason` names the segment ("sizecheck", "make preflight", ...) and is what a
    waiting process prints, so whoever is watching knows what they are queued behind.
    Raises `TimeoutError` after `timeout` seconds rather than waiting forever."""
    global _depth
    if _depth:
        _depth += 1
        try:
            yield
        finally:
            _depth -= 1
        return

    path = lock_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = f"{os.getpid()}\n{reason}\n{time.time()}\n".encode("utf-8")
    started = time.monotonic()
    next_note = PROGRESS_SECONDS
    while True:
        try:
            fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            pass
        else:
            os.write(fd, payload)
            os.close(fd)
            break

        pid, held_for = _holder(path)
        if _is_stale(path, pid):
            print(f"[texlock] stale lock from pid {pid} removed", flush=True)
            with contextlib.suppress(OSError):
                path.unlink()
            continue
        waited = time.monotonic() - started
        if waited >= next_note:
            print(f"[texlock] waiting for pid {pid} ({held_for}) ... {int(waited)}s", flush=True)
            next_note += PROGRESS_SECONDS
        if waited >= timeout:
            raise TimeoutError(
                f"[texlock] gave up after {int(waited)}s waiting for {path}: pid {pid} "
                f"({held_for}) is still building Tex in this directory. Wait for it to "
                f"finish, or -- if that process is gone -- delete the lock file."
            )
        time.sleep(RETRY_SECONDS)

    _depth = 1
    try:
        yield
    finally:
        _depth = 0
        with contextlib.suppress(OSError):
            path.unlink()
