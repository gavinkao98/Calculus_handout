"""rewatch_merge.py -- merge the REWATCH lens outputs (+ the orchestrator's verification) into
the digest that rewatch_multilens.gen.py renders.

    python video/content_scripts/_audit/_gen/rewatch_merge.py --ws <workspace> \
        [--pack-json video/output/ch03/s3.1/rewatch_pack/pack.json] \
        [--models R1a=gemini-3.1-pro-high:agy,R1b=claude-sonnet-4-6:agy,R2=opus:sub,...] \
        [--verify verify.json] --out _gen/rewatch_multilens.digest.json

Lens outputs: <ws>/<run>/result.json (subagents write it directly) or <ws>/<run>/run.out
(agy --output-format json envelope; its structured_output is extracted and also saved as
result.json). Finding ids are stable: <run>.<scene NN>.<k>, so a verify file written against
a partial merge stays valid when more lenses land.

verify.json shape (the orchestrator's refute-by-default pass):
  {"checks": {"R2.06.1": {"check": "confirmed|plausible|refuted|dup", "note": "..."}, ...},
   "scenes": {"<scene_id>": {"level": "①..④", "synthesis": "...", "one_change": "..."}},
   "film": {"overall": "...", "patterns": [...], "water_level": "...", "agreement": "...", "lens_quality": "..."}}
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
RUN_LENS = {"R1a": "R1", "R1b": "R1", "R2": "R2", "R3": "R3", "R4": "R4", "R5": "R5"}
RULES = ("ML1", "ML2", "ML3", "ML4", "ML5")   # motion-language rule codes (rubric `rule`; SPEC-motion-language.md §0)
DEFAULT_MODELS = ("R1a=Gemini 3.1 Pro (high) · agy:agy,R1b=Claude Sonnet 4.6 · agy:agy,R2=Claude Opus 5 · subagent:sub,"
                  "R3=Claude Sonnet 5 · subagent:sub,R4=Claude Haiku 4.5 · subagent:sub,R5=Gemini 3.8 Flash (high) · agy:agy")


def load_run(d: Path, source: str):
    usage = None
    if source == "agy":
        env = json.loads((d / "run.out").read_text(encoding="utf-8", errors="replace").strip())
        usage = env.get("usage")
        data = env.get("structured_output")
        if not data:
            txt = env.get("response", "")
            data = json.loads(txt[txt.index("{"): txt.rindex("}") + 1])
        (d / "result.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
        return data, usage
    return json.loads((d / "result.json").read_text(encoding="utf-8")), usage


def rule_counts(findings: list[dict]) -> dict[str, int]:
    """finding x rule: count per ML code + "unlabeled"; notes and refuted/dup findings are not counted."""
    counts = {r: 0 for r in (*RULES, "unlabeled")}
    for f in findings:
        if f.get("dim") != "note" and f.get("check") not in ("refuted", "dup"):
            key = f.get("rule") or "unlabeled"
            counts[key] = counts.get(key, 0) + 1
    return counts


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--ws", type=Path, required=True)
    ap.add_argument("--pack-json", type=Path, default=REPO / "video" / "output" / "ch03" / "s3.1" / "rewatch_pack" / "pack.json")
    ap.add_argument("--models", default=DEFAULT_MODELS, help="run=label:source(agy|sub),...")
    ap.add_argument("--verify", type=Path, default=None)
    ap.add_argument("--out", type=Path, default=HERE / "rewatch_multilens.digest.json")
    ap.add_argument("--date", default="")
    args = ap.parse_args()

    models = {}
    for item in args.models.split(","):
        run, rest = item.split("=", 1)
        label, source = rest.rsplit(":", 1)
        models[run] = (label, source)
    verify = json.loads(args.verify.read_text(encoding="utf-8")) if args.verify else None
    pack = json.loads(args.pack_json.read_text(encoding="utf-8"))
    order = [s["id"] for s in pack["scenes"]]

    lenses, missing = {}, []
    for run, (label, source) in models.items():
        try:
            data, usage = load_run(args.ws / run, source)
        except Exception as exc:  # noqa: BLE001
            missing.append(f"{run}: {type(exc).__name__}: {exc}")
            continue
        by_id = {re.sub(r"^\d{2}_", "", str(s.get("id", ""))).strip(): s for s in data.get("scenes", [])}
        lenses[run] = {"lens": RUN_LENS[run], "model": label, "film": data.get("film", {}), "usage": usage,
                       "scenes_reported": len(by_id), "by_id": by_id}

    scenes = []
    for n, sid in enumerate(order, 1):
        meta = pack["scenes"][n - 1]
        verdicts, findings = {}, []
        for run, L in lenses.items():
            sc = L["by_id"].get(sid)
            if not sc:
                verdicts[run] = "—"
                continue
            verdicts[run] = sc.get("verdict", "—")
            for k, f in enumerate(sc.get("findings", []), 1):
                findings.append({"fid": f"{run}.{n:02d}.{k}", "run": run, "lens": L["lens"],
                                 **{key: f.get(key, "") for key in ("dim", "severity", "rule", "where", "evidence", "problem", "proposal")},
                                 "check": None, "check_note": ""})
            if sc.get("note"):
                findings.append({"fid": f"{run}.{n:02d}.note", "run": run, "lens": L["lens"], "dim": "note", "severity": "note",
                                 "where": "", "evidence": "", "problem": sc["note"], "proposal": "", "check": None, "check_note": ""})
        rec = {"n": n, "id": sid, "title": meta["title"], "kind": meta["kind"], "template": meta.get("template"),
               "hook": bool(meta.get("hook")), "global_start": meta["global_start"], "duration": meta["duration"],
               "reveals": meta["reveals"], "motion": meta["motion"], "sheet": meta["sheet"],
               "verdicts": verdicts, "findings": findings, "synthesis": "", "one_change": "", "level": ""}
        if verify:
            v = verify.get("scenes", {}).get(sid, {})
            rec["synthesis"], rec["one_change"], rec["level"] = v.get("synthesis", ""), v.get("one_change", ""), v.get("level", "")
            for f in rec["findings"]:
                c = verify.get("checks", {}).get(f["fid"])
                if c:
                    f["check"], f["check_note"] = c.get("check"), c.get("note", "")
        rec["by_rule"] = rule_counts(rec["findings"])
        scenes.append(rec)

    digest = {"deck": pack["deck"], "film_path": pack["film"], "total_seconds": pack["total_seconds"],
              "date": args.date, "rubric": "video/content_scripts/_audit/REWATCH-REVIEW-RUBRIC.md",
              "lenses": {run: {k: v for k, v in L.items() if k != "by_id"} for run, L in lenses.items()},
              "missing_runs": missing, "scenes": scenes, "film": (verify or {}).get("film", {}),
              "by_rule": rule_counts([f for s in scenes for f in s["findings"]])}
    args.out.write_text(json.dumps(digest, ensure_ascii=False, indent=1), encoding="utf-8")
    nf = sum(1 for s in scenes for f in s["findings"] if f["dim"] != "note")
    unchecked = [f["fid"] for s in scenes for f in s["findings"] if f["dim"] != "note" and not f["check"]]
    print(f"wrote {args.out}: {len(lenses)} lenses, {nf} findings, unchecked {len(unchecked)}; missing: {missing or 'none'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
