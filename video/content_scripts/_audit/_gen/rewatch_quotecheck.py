"""rewatch_quotecheck.py -- mechanise the part of REWATCH's refute-by-default pass that a script can do:
does every finding's quoted narration actually exist in the film?

    python video/content_scripts/_audit/_gen/rewatch_quotecheck.py \
        --pack video/output/ch03/s3.1/rewatch_pack --digest _gen/rewatch_multilens.digest.json

REWATCH-REVIEW-RUBRIC.md 共同規則 2 要求每條 finding 的 evidence 附「一句旁白引文或畫面描述」，R1 鏡另有
「必須同時含旁白原句」的證據門檻。本工具抽出 evidence 裡被引號括起來的英文片段，正規化後在該場（其次全片）的
spoken text 裡找，判四種：

  VERBATIM   在該場的旁白裡找到 -- 引文成立
  ELSEWHERE  在別場找到 -- 跨場引用，合法，但 where 要標明是哪一場
  NO-QUOTE   沒有引英文旁白（引的是上畫面文字、或整條靠數字/畫面描述）-- 合規，人工判
  NOT-FOUND  全片都找不到 -- **引文是捏造的，合成時該條 evidence 一律駁回**

為什麼要有（2026-09-13，§3.1 里程碑審）：該輪 R5 鏡（Gemini 3.8 Flash high）5 條 finding 的引文
**全部 NOT-FOUND**（另有一條把 +44.3s 掛在只有 38.3 s 的場上，並描述了一個全片不存在的畫面），
而同輪四個 Opus 5 subagent 鏡是 77 條 VERBATIM／0 條 NOT-FOUND。肉眼讀起來兩者一樣通順，
差別只有逐句比對才看得出來 -- 所以這一步不能靠讀，要靠跑。

注意：NOT-FOUND 只否定那條 finding 的**證據**，不自動否定它的**主張**；主張若被別鏡以成立的證據獨立指出，
以那一鏡的條目為準（見 rubric「合成」）。
"""
from __future__ import annotations

import argparse
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]

QUOTE = re.compile(r"[「『\"'](.{25,400}?)[」』\"']", re.S)
MIN_LETTERS = 20          # below this a "quote" is too short to be a narration sentence
CORE_WORDS = 9            # match on the first N words: tolerates a truncated tail / ellipsis


def norm(s: str) -> str:
    """Fold to bare lowercase words. Punctuation -> space FIRST, then collapse runs: the pack's
    current-word markers (`[to]`) and the narration's commas must normalise to the same spacing."""
    s = unicodedata.normalize("NFKC", s).lower()
    for a, b in (("’", "'"), ("—", " "), ("–", " "), ("--", " ")):
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]+", " ", s)).strip()


def spoken_by_scene(pack: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    for md in sorted(pack.glob("[0-9][0-9]_*.md")):
        text = md.read_text(encoding="utf-8")
        if "## Beats" not in text:
            continue
        body = text.split("## Beats")[1].split("## Same beats")[0]
        said = " ".join(ln.split("|")[-2].strip() for ln in body.splitlines() if ln.startswith("| "))
        out[md.stem.split("_", 1)[1]] = norm(said)
    return out


def classify(evidence: str, scene_said: str, all_said: str) -> tuple[str, str]:
    quotes = [q for q in QUOTE.findall(evidence) if len(re.findall(r"[a-z]", q.lower())) > MIN_LETTERS]
    if not quotes:
        return "NO-QUOTE", ""
    verdict, detail = "NOT-FOUND", quotes[0][:70]
    for q in quotes:
        core = " ".join(norm(q).split()[:CORE_WORDS])
        if not core:
            continue
        if core in scene_said:
            return "VERBATIM", q[:60]
        if core in all_said:
            verdict, detail = "ELSEWHERE", q[:60]
    return verdict, detail


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--pack", type=Path, default=REPO / "video" / "output" / "ch03" / "s3.1" / "rewatch_pack")
    ap.add_argument("--digest", type=Path, default=HERE / "rewatch_multilens.digest.json")
    ap.add_argument("--quiet", action="store_true", help="only print the per-lens tally")
    args = ap.parse_args()

    said = spoken_by_scene(args.pack.resolve())
    if not said:
        raise SystemExit(f"[quotecheck] no per-scene .md found under {args.pack}")
    all_said = " || ".join(said.values())
    digest = json.loads(args.digest.read_text(encoding="utf-8"))

    rows = []
    for scene in digest["scenes"]:
        for f in scene["findings"]:
            if f.get("dim") == "note":
                continue
            verdict, detail = classify(f.get("evidence", ""), said.get(scene["id"], ""), all_said)
            rows.append((f["fid"], scene["id"], f.get("severity", ""), verdict, detail))

    if not args.quiet:
        for fid, sid, sev, verdict, detail in rows:
            if verdict in ("NOT-FOUND", "ELSEWHERE"):
                print(f"{verdict:10s} {fid:12s} {sev:6s} {sid:32s} {detail}")
        print()
    total = Counter(v for *_, v, _ in rows)
    print(f"{len(rows)} findings: " + ", ".join(f"{k} {n}" for k, n in sorted(total.items())))
    per: dict[str, Counter] = {}
    for fid, *_, verdict, _ in rows:
        per.setdefault(fid.split(".")[0], Counter())[verdict] += 1
    for run, c in sorted(per.items()):
        flag = "  <-- 引文全數落空，該鏡證據不可用" if c["NOT-FOUND"] and not c["VERBATIM"] else ""
        print(f"  {run:5s} " + ", ".join(f"{k} {n}" for k, n in sorted(c.items())) + flag)
    return 1 if any(c["NOT-FOUND"] and not c["VERBATIM"] for c in per.values()) else 0


if __name__ == "__main__":
    raise SystemExit(main())
