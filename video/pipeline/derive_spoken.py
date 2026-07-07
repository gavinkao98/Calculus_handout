"""Single-source derivation of the spoken-narration artifacts (any section).

`content_scripts/<deck>.spoken.yml` is the ONE place the spoken narration lives
(math read aloud, with {show} markers). From it + the canonical storyboard this
generates, deterministically:

  - storyboards/<deck>_mimo.yml                  MiMo storyboard (say := spoken, meta._mimo, voice Dean)
  - content_scripts/<deck>_narration_spoken.md   the human reading view ({show} stripped)

and `--check` validates parity against the canonical storyboard so the two
narration tracks can't silently drift:

  - every canonical content scene with a `say` has a spoken entry (and vice-versa);
  - the {show ...} markers in each spoken `say` match the canonical `say` exactly;
  - no `$` (LaTeX) leaks into the spoken text.

    python video/pipeline/derive_spoken.py --deck ch03_trig_derivatives          # regenerate (runs --check first)
    python video/pipeline/derive_spoken.py --deck ch03_trig_derivatives --check   # validate only, write nothing
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from pipeline import _bootstrap  # noqa: E402

_bootstrap.bootstrap()
import yaml  # noqa: E402

STORY = _bootstrap.REPO_ROOT / "video" / "storyboards"
CONTENT = _bootstrap.REPO_ROOT / "video" / "content_scripts"

_SHOW = re.compile(r"\{show\s+([^}]+)\}")

# Optional advisory per-unit MiMo styling notes (NOT spoken text), keyed by deck
# then scene id. New sections may omit; they simply get no notes in the md view.
# (ch01 practice-era notes removed 2026-07-07 — that deck's spoken route was
#  discarded with the practice artifacts; see git history if ever needed.)
STYLE_NOTES: dict[str, dict[str, str]] = {}

# §1 (MiMo config) and §2 (reading conventions) are UNIVERSAL across sections.
MD_CONFIG_AND_CONVENTIONS = """## 一、MiMo 合成設定（現用）

| 項目 | 值 |
|------|----|
| `model` | `mimo-v2.5-tts`（builtin voice 模型；唯一模型） |
| `voice` | `Dean`（builtin；經 `audio.voice` 選定） |
| `audio.format` | `wav`（24kHz/mono/PCM16，與產線 `write_pcm_wav` 相容；beat WAV 自動裁頭尾靜音） |

**風格提示：** 無——builtin Dean 路線**不送 persona/style prompt**（2026-07-05 起，voice-design 模型與「Calm Professor」persona 已退役）。節奏靠口語稿標點與句構。

**Audio tag：** 維持預設**不啟用**（口語稿純文字）。

## 二、數學念法慣例（全節通用；NFA 裁定）

| 數學 | 口語念法 | 備註 |
|------|---------|------|
| $f^{-1}$（反函數記號） | **“f inverse”** | 絕不念 “f to the minus one”。例外：若課文**刻意對比** $\\sin^{-1}$ 記號與 $1/\\sin$，該處照字面念 “sine to the minus one” 並講清不是倒數。 |
| $x_1,\\ x_2$（下標） | **“x sub one”, “x sub two”** | 正式定義／證明語境最無歧義。 |
| $x^2,\\ x^3$ | “x squared”, “x cubed” | |
| $\\sqrt[3]{x}$ / $\\sqrt[3]{y-2}$ | “the cube root of x” / “…of **the quantity** y minus two” | 和/差根號加 “the quantity” 消歧義。 |
| $(\\sqrt[3]{x-2})^3$ / $(f^{-1}(x))^2$ | “…, **all cubed**” / “…, **all squared**” | 外層次方蓋整體。 |
| 分數 $\\tfrac{a}{b}$ | “a over b”（簡單分數念 “one half / one quarter / nine-fifths”…） | |
| 複雜分數（分子或分母含乘積／根號） | “…, all over …” 或 “… divided by the quantity …” | 例：$\\tfrac{1}{2\\sqrt2}$→“one over the quantity two root two”（“the quantity” 群組分母、防 (1/2)√2 誤聽）；$-\\tfrac{2\\sqrt5}{5}$→“negative two root five over five”（兩種群組同值、免 quantity）（NFA §1.2 D5）。 |
| 區間 $[a,b]$ / $(a,b)$ | “the (open) interval from a to b” | |
| 座標點 $(a,b)$ | **“the point with coordinates a and b”** | 無視覺符號時最清楚。 |
| $\\pi/2$、$\\arcsin$… | “pi over two”、“arcsine of …” | 反三角直接念 arc-名。 |
| domain $A$ / range $B$ | “domain A / range B” | |
"""


def load(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def show_markers(say: str) -> list[str]:
    return _SHOW.findall(say or "")


def check(canon: dict, spoken: dict) -> list[str]:
    """Return a list of parity problems (empty == clean)."""
    problems: list[str] = []
    content = {s["id"]: s for s in canon["scenes"]
               if s.get("kind", "content") == "content" and "say" in s}
    miss = set(content) - set(spoken)
    extra = set(spoken) - set(content)
    if miss:
        problems.append(f"canonical content scenes missing a spoken entry: {sorted(miss)}")
    if extra:
        problems.append(f"spoken entries with no matching canonical scene: {sorted(extra)}")
    for sid in sorted(set(content) & set(spoken)):
        if "$" in spoken[sid]:
            problems.append(f"{sid}: spoken text still contains '$' (LaTeX not spelled out)")
        cm, sm = show_markers(content[sid]["say"]), show_markers(spoken[sid])
        if cm != sm:
            problems.append(f"{sid}: {{show}} markers differ\n    canonical: {cm}\n    spoken:    {sm}")
    return problems


def gen_mimo(canon: dict, spoken: dict, deck: str) -> dict:
    canon["meta"]["id"] = f"{deck}_mimo"
    canon["meta"]["voice"] = "Dean"
    for scene in canon["scenes"]:
        if scene["id"] in spoken:
            scene["say"] = spoken[scene["id"]]
    return canon


def gen_md(canon: dict, spoken: dict, deck: str) -> str:
    meta = canon["meta"]
    title = f"§{meta.get('section','')} {meta.get('title','')}".strip()
    header = (
        f"# {title} — 旁白口語版（版本 B · MiMo-V2.5-TTS 客製）\n\n"
        f"> **此檔為生成檔（DO NOT EDIT）。** 由 `content_scripts/{deck}.spoken.yml`（口語單一源）"
        f" 經 `pipeline/derive_spoken.py` 生成。要改旁白請改 `.spoken.yml` 後重生。\n"
        f"> **性質：版本 B（口語 TTS 版）。** 英文散文逐字忠於內容稿 `narration`，**只把數學攤成口語**（無 LaTeX），"
        f"供不能直讀 LaTeX 的 TTS（MiMo）照念。對照閱讀版（版本 A，數學渲染）＝ `{deck}_narration.html`。\n"
        f"> **NFA 稽核狀態：** 見 `content_scripts/_audit/`（每節各自記錄）。\n\n---\n\n"
        + MD_CONFIG_AND_CONVENTIONS
        + "\n## 三、逐段口語稿\n\n"
        "> 每段 `uNN · id` 即該單元 `assistant` 訊息內容（`{show}` 已移除）。intro/outro 無旁白，不列。\n\n"
    )
    notes = STYLE_NOTES.get(deck, {})
    numbers = {s["id"]: i for i, s in enumerate(canon["scenes"], start=1)}
    units = []
    for sid, say in spoken.items():
        text = " ".join(_SHOW.sub("", say).split())
        units.append(f"### u{numbers[sid]} · {sid}\n{text}")
        if sid in notes:
            units.append(f"\n> _per-unit 風格：_ {notes[sid]}")
        units.append("")
    footer = (
        "\n---\n\n## 四、備忘\n\n"
        f"- 口語文字單一源＝ `content_scripts/{deck}.spoken.yml`；本檔與 `storyboards/{deck}_mimo.yml` 皆由 `derive_spoken.py` 生成。\n"
        "- `{show}` beat 切分與正典 storyboard 對齊（`derive_spoken.py --check` 守門）。\n"
        "- 計費：MiMo 公測限免但屬外部 API；批次合成前依 `CLAUDE.md` 報用量、徵同意。\n"
    )
    return header + "\n".join(units) + footer


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--deck", required=True, help="deck id, e.g. ch01_inverse_functions")
    ap.add_argument("--check", action="store_true", help="validate parity only; write nothing")
    args = ap.parse_args()

    canon_path = STORY / f"{args.deck}.yml"
    spoken_path = CONTENT / f"{args.deck}.spoken.yml"
    for p in (canon_path, spoken_path):
        if not p.exists():
            raise SystemExit(f"[derive_spoken] missing {p}")
    canon = load(canon_path)
    spoken = load(spoken_path)

    problems = check(canon, spoken)
    if problems:
        print("[derive_spoken] PARITY ERRORS:", flush=True)
        for p in problems:
            print(f"  - {p}", flush=True)
        return 1
    print("[derive_spoken] parity OK", flush=True)
    if args.check:
        return 0

    mimo_yml = STORY / f"{args.deck}_mimo.yml"
    md = CONTENT / f"{args.deck}_narration_spoken.md"
    mimo_yml.write_text(
        f"# GENERATED by pipeline/derive_spoken.py from {args.deck}.spoken.yml + the canonical\n"
        "# storyboard. DO NOT EDIT -- change the .spoken.yml source and regenerate.\n\n"
        + yaml.safe_dump(gen_mimo(load(canon_path), spoken, args.deck),
                         allow_unicode=True, sort_keys=False, width=4096),
        encoding="utf-8",
    )
    md.write_text(gen_md(canon, spoken, args.deck), encoding="utf-8")
    print(f"[derive_spoken] wrote {mimo_yml}", flush=True)
    print(f"[derive_spoken] wrote {md}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
