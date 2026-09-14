"""Self-test: the per-cwd TeX build lock (`pipeline/texlock.py`). Run from video/:
    python -m pipeline._selftest_texlock

Pins the four contract clauses of r2 kickoff §2.H:
  (1) two processes sharing a cwd take the lock one after the other, never at once
  (2) a lock left behind by a dead process (old mtime + vanished pid) is reclaimed
  (3) a lock held by a LIVE process raises TimeoutError with an actionable message
      -- and is not mistaken for stale just because it is old
  (4) integration: two concurrent `sizecheck.py _demo_derivation.yml` in one cwd no
      longer produce the false `could not build scene`. Without the lock this failed
      in 3 of 3 measured rounds on a cold Tex cache (see texlock.py's docstring);
      it is the defect the lock exists for, so the deck really is built twice here.
      It needs a quiet MiKTeX: another LaTeX run anywhere on the machine can fail a
      build through the global fndb lock, which is a different defect texlock does not
      address (KICKOFF-shared-layer-v1 §8 (8)). The assertion says which one it hit.

(1) and (4) spawn subprocesses in a fresh temp cwd, which is also where their
`media/Tex` lands -- so the Tex cache is cold (the race needs actual compilation)
and the worktree's own cache is left alone. (2) and (3) chdir into a temp dir for
the same isolation.
"""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from pipeline import _bootstrap

_bootstrap.bootstrap()

from pipeline.texlock import PROGRESS_SECONDS, STALE_SECONDS, lock_path, tex_lock  # noqa: E402

VIDEO = Path(__file__).resolve().parent.parent
DECK = VIDEO / "storyboards" / "_demo_derivation.yml"

# One holder: take the lock, sit in it, then record the interval it owned.
_HOLDER = '''
import os, sys, time
sys.path.insert(0, sys.argv[1])
from pipeline import _bootstrap
_bootstrap.bootstrap()
from pipeline.texlock import tex_lock

with tex_lock(reason="selftest"):
    start = time.time()
    time.sleep(2.0)
    end = time.time()
    with open(sys.argv[2], "a", encoding="utf-8") as fh:
        fh.write(f"{os.getpid()} {start!r} {end!r}\\n")
'''


def _chdir(tmp):
    """chdir into `tmp` and return the previous cwd (the lock path is cwd-relative)."""
    old = os.getcwd()
    os.chdir(tmp)
    return old


def _dead_pid() -> int:
    """A pid that has certainly exited."""
    proc = subprocess.Popen([sys.executable, "-c", "pass"])
    proc.wait()
    return proc.pid


# -- (1) mutual exclusion ------------------------------------------------------

def test_two_processes_never_hold_the_lock_at_the_same_time():
    with tempfile.TemporaryDirectory() as tmp:
        script = Path(tmp) / "holder.py"
        script.write_text(_HOLDER, encoding="utf-8")
        marker = Path(tmp) / "marker.txt"
        procs = [subprocess.Popen([sys.executable, str(script), str(VIDEO), str(marker)],
                                  cwd=tmp, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                  text=True, encoding="utf-8", errors="replace")
                 for _ in range(2)]
        outs = [p.communicate()[0] for p in procs]
        assert all(p.returncode == 0 for p in procs), outs

        spans = []
        for line in marker.read_text(encoding="utf-8").splitlines():
            _pid, start, end = line.split()
            spans.append((float(start), float(end)))
        assert len(spans) == 2, spans
        spans.sort()
        assert spans[0][1] <= spans[1][0], f"overlapping holds: {spans}"
        # and the second one really waited rather than erroring out early
        assert spans[1][1] - spans[0][0] >= 4.0, spans


def test_the_waiter_says_who_it_is_waiting_for():
    """The 10 s progress line: a wait must never look like a hang."""
    with tempfile.TemporaryDirectory() as tmp:
        script = Path(tmp) / "holder.py"
        # The waiter must still be waiting when it crosses a PROGRESS_SECONDS mark, and its
        # own clock only starts after interpreter startup + bootstrap, so hold well past it.
        hold = 2 * PROGRESS_SECONDS
        script.write_text(_HOLDER.replace("time.sleep(2.0)", f"time.sleep({hold})"), encoding="utf-8")
        marker = Path(tmp) / "marker.txt"
        first = subprocess.Popen([sys.executable, str(script), str(VIDEO), str(marker)], cwd=tmp,
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                                 encoding="utf-8", errors="replace")
        time.sleep(3.0)     # let it get the lock first
        second = subprocess.Popen([sys.executable, str(script), str(VIDEO), str(marker)], cwd=tmp,
                                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                                  encoding="utf-8", errors="replace")
        out = second.communicate()[0]
        first.communicate()
        assert "[texlock] waiting for pid" in out, out
        assert "(selftest)" in out, out


# -- the lock must outlive manim's own housekeeping ----------------------------

def test_the_lock_survives_manims_tex_directory_sweep():
    """manim runs `delete_nonsvg_files()` after every Tex->SVG conversion, and it
    unlinks EVERY file in media/Tex that is not .svg/.tex. A lock kept in there is
    deleted by the builds it guards -- measured: the second process then took the
    "free" lock ~1 s in and both raced as before. Hence <media_dir>/Tex.lock."""
    from manim import config
    from manim.utils.tex_file_writing import delete_nonsvg_files

    with tempfile.TemporaryDirectory() as tmp:
        old = _chdir(tmp)
        try:
            Path(config.get_dir("tex_dir")).mkdir(parents=True, exist_ok=True)
            with tex_lock(reason="holder", timeout=10):
                delete_nonsvg_files()
                assert lock_path().exists(), \
                    f"manim's Tex sweep deleted the lock at {lock_path()}"
        finally:
            os.chdir(old)


# -- (2) stale reclaim ---------------------------------------------------------

def test_a_lock_from_a_dead_process_is_reclaimed():
    with tempfile.TemporaryDirectory() as tmp:
        old = _chdir(tmp)
        try:
            path = lock_path()
            path.parent.mkdir(parents=True, exist_ok=True)
            gone = _dead_pid()
            path.write_text(f"{gone}\nstale-holder\n0\n", encoding="utf-8")
            aged = time.time() - (STALE_SECONDS + 60)
            os.utime(path, (aged, aged))
            with tex_lock(reason="reclaimer", timeout=10):
                assert path.read_text(encoding="utf-8").splitlines()[0] == str(os.getpid())
            assert not path.exists()
        finally:
            os.chdir(old)


# -- (3) timeout on a live holder ----------------------------------------------

def test_a_live_holder_times_out_with_an_actionable_message():
    with tempfile.TemporaryDirectory() as tmp:
        old = _chdir(tmp)
        try:
            path = lock_path()
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"{os.getpid()}\nrender\n0\n", encoding="utf-8")
            t0 = time.monotonic()
            try:
                with tex_lock(reason="second", timeout=1.5):
                    raise AssertionError("acquired a lock that a live process holds")
            except TimeoutError as exc:
                waited = time.monotonic() - t0
                assert 1.0 <= waited < 8.0, waited
                assert "[texlock]" in str(exc) and str(os.getpid()) in str(exc), str(exc)
                assert "render" in str(exc), str(exc)
            assert path.exists(), "a timed-out waiter must not delete the holder's lock"
        finally:
            os.chdir(old)


def test_an_old_lock_whose_owner_is_alive_is_not_stale():
    """A full-deck render outlives the staleness window; both conditions must hold."""
    with tempfile.TemporaryDirectory() as tmp:
        old = _chdir(tmp)
        try:
            path = lock_path()
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"{os.getpid()}\nlong-render\n0\n", encoding="utf-8")
            aged = time.time() - (STALE_SECONDS + 60)
            os.utime(path, (aged, aged))
            try:
                with tex_lock(reason="second", timeout=1.5):
                    raise AssertionError("reclaimed a lock whose owner is still running")
            except TimeoutError:
                pass
        finally:
            os.chdir(old)


# -- re-entrancy: make.py holds the lock across a check_scenes that takes it too --

def test_nesting_in_one_process_does_not_deadlock():
    with tempfile.TemporaryDirectory() as tmp:
        old = _chdir(tmp)
        try:
            path = lock_path()
            with tex_lock(reason="make preflight", timeout=5):
                with tex_lock(reason="sizecheck", timeout=5):
                    assert path.exists()
                assert path.exists(), "the inner block must not release the outer lock"
            assert not path.exists()
        finally:
            os.chdir(old)


# -- (4) the defect itself -----------------------------------------------------

def test_two_concurrent_sizechecks_do_not_fake_a_build_failure():
    with tempfile.TemporaryDirectory() as tmp:
        procs = [subprocess.Popen([sys.executable, str(VIDEO / "pipeline" / "sizecheck.py"), str(DECK)],
                                  cwd=tmp, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                  text=True, encoding="utf-8", errors="replace")
                 for _ in range(2)]
        outs = [p.communicate()[0] for p in procs]
        for n, out in enumerate(outs):
            hits = [ln.strip() for ln in out.splitlines() if "could not build scene" in ln]
            # A hit is either the race this lock fixes (the two processes stepping on each
            # other's media/Tex files) or the machine-wide MiKTeX fndb flake, which texlock
            # does NOT address (KICKOFF-shared-layer-v1 §8 (8)) -- say which, so a red here
            # is not misread as the lock having failed.
            kind = ("the per-cwd Tex race (the lock did not hold)"
                    if any("PermissionError" in h or "FileNotFoundError" in h for h in hits)
                    else "the machine-wide MiKTeX flake, NOT the lock -- rerun with no other "
                         "LaTeX running on this machine")
            assert not hits, f"process {n} -- {kind}:\n" + "\n".join(hits)


if __name__ == "__main__":
    import traceback

    fails = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn(); print(f"PASS {name}", flush=True)
            except Exception:
                fails += 1; print(f"FAIL {name}", flush=True); traceback.print_exc()
    sys.exit(1 if fails else 0)
