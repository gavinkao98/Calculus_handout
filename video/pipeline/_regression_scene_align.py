"""Real-data regression: production scene_align must reproduce the forced_alignment_dean
experiment's stable-ts output. Zero-cost (local CPU, WAVs already on disk; no API).

Run: python video/pipeline/_regression_scene_align.py

Skips cleanly (exit 0) when stable-ts or the experiment WAVs are absent, so it stays
green on a machine without the aligner/artifacts. Compares against the *_stable
artifacts (aligned_beats_stable.json / words_stable_ts.json), NOT aligned_beats.json
(that is the free-ASR/whisper-timestamped timeline -- 185 words for the derivation
scene, not the 197-word stable-ts one).
"""
import json
import sys
from pathlib import Path

# Drop THIS script's own dir (video/pipeline/, auto-prepended by Python) from
# sys.path: it holds pipeline/coverage.py, whose bare name would shadow the
# 'coverage' package that numba (pulled in by stable-ts -> whisper at align time)
# optionally `import coverage`s -- the shadow lacks `.types` and crashes the aligner.
# We only need video/ so `from pipeline import ...` resolves. (Qualified
# `from pipeline import coverage` elsewhere is unaffected.)
_HERE = str(Path(__file__).resolve().parent)
sys.path[:] = [p for p in sys.path if p not in ("", _HERE)]
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline import scene_align as SA  # noqa: E402
from pipeline.audio import wav_duration  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
STORYBOARD = REPO / "video" / "storyboards" / "ch03_trig_derivatives_mimo.yml"
EXP = REPO / "video" / "output" / "experiments" / "forced_alignment_dean"
SCENES = ["difference_quotient_for_sine", "sector_inequality", "slope_equals_height"]

TOL = 1e-6      # words: start/end/probability are deterministic for the same model+wav
BEAT_TOL = 1e-3  # mapped beat boundaries compared to 3 dp


def _load_scene(scene_id):
    import yaml
    data = yaml.safe_load(STORYBOARD.read_text(encoding="utf-8"))
    by_id = {s["id"]: s for s in data["scenes"]}
    return by_id[scene_id]


def _cmp_words(got, want):
    if len(got) != len(want):
        return f"word count {len(got)} != {len(want)}"
    for i, (g, w) in enumerate(zip(got, want)):
        if g["word"] != w["word"]:
            return f"token {i}: {g['word']!r} != {w['word']!r}"
        for k in ("start", "end", "probability"):
            gv, wv = g.get(k), w.get(k)
            if gv is None and wv is None:
                continue
            if gv is None or wv is None or abs(float(gv) - float(wv)) > TOL:
                return f"token {i} {k}: {gv} != {wv}"
    return None


def _cmp_summary(got, want):
    for k in ("word_count", "low_prob_words"):
        if got.get(k) != want.get(k):
            return f"summary.{k}: {got.get(k)} != {want.get(k)}"
    for k in ("prob_min", "prob_mean"):
        gv, wv = got.get(k), want.get(k)
        if gv is None and wv is None:
            continue
        if gv is None or wv is None or abs(float(gv) - float(wv)) > 1e-3:
            return f"summary.{k}: {gv} != {wv}"
    if len(got.get("low_prob_runs", [])) != len(want.get("low_prob_runs", [])):
        return "summary.low_prob_runs count differs"
    if len(got.get("beat_boundary_in_multi_token_word", [])) != \
       len(want.get("beat_boundary_in_multi_token_word", [])):
        return "summary.beat_boundary_in_multi_token_word count differs"
    return None


def _cmp_beats(got, want):
    if len(got) != len(want):
        return f"beat count {len(got)} != {len(want)}"
    for i, (g, w) in enumerate(zip(got, want)):
        for k in ("start_seconds", "end_seconds"):
            if abs(float(g[k]) - float(w[k])) > BEAT_TOL:
                return f"beat {i} {k}: {g[k]} != {w[k]}"
    return None


def main():
    try:
        import stable_whisper  # noqa: F401
    except ImportError:
        print("SKIP: stable-ts not installed")
        return 0
    if not all((EXP / s / "scene_dean.wav").exists() for s in SCENES):
        print("SKIP: experiment WAVs not on disk")
        return 0

    passed = 0
    for sid in SCENES:
        d = EXP / sid
        wav = d / "scene_dean.wav"
        stored = json.loads((d / "words_stable_ts.json").read_text(encoding="utf-8"))
        stored_beats = json.loads((d / "aligned_beats_stable.json").read_text(encoding="utf-8"))
        plan = SA.build_scene_plan(_load_scene(sid))
        res = SA.align_scene(wav, plan)
        err = (_cmp_words(res["words"], stored["words"])
               or _cmp_summary(res["summary"], stored["summary"]))
        if not err:
            beats = SA.map_to_beats(plan, res["words"], wav_duration(wav), multi=res["multi"])
            err = _cmp_beats(beats, stored_beats["beats"])
        if err:
            print(f"  FAIL {sid}: {err}")
        else:
            print(f"  OK   {sid}: {len(res['words'])} words, {len(stored_beats['beats'])} beats match")
            passed += 1

    if passed == len(SCENES):
        print(f"OK regression: {passed}/{len(SCENES)} scenes match stable-ts output")
        return 0
    print(f"REGRESSION FAILED: {passed}/{len(SCENES)} scenes matched")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
