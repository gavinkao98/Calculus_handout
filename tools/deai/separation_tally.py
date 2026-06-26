"""語意/聲音 critic 盲測分離度 tally（PLAN-deai-semantic-critic Task 4）。

吃一份盲測結果 JSON（每段 critic 的 S/A findings 數＋字數＋真實標籤），算
「S/A findings per 500 字」，比較 AI 段與真人段兩組平均，判是否「分得開」。

判準（spec §5）：mean(AI) > mean(human) 且分離倍數 ≥ THRESHOLD（預設 2×）。
分不開＝critic 是噪音 → 回 Task 2 改 rubric/錨，不可信它。

輸入 JSON 形狀（passage_id -> 紀錄）：
  { "p1": {"label": "human", "words": 105, "sa_findings": 0},
    "p2": {"label": "ai",    "words": 110, "sa_findings": 3}, ... }
label 僅 "ai" / "human"。sa_findings = Substance + Altitude findings 數（不含 Voice）。

跑：
  python tools/deai/separation_tally.py <results.json>                  # 真實 tally（ai vs human）
  python tools/deai/separation_tally.py <results.json> empty substantive  # 自訂兩組組名
  python tools/deai/separation_tally.py --selftest                      # 邏輯自測（假資料）
"""
import json
import sys
from statistics import mean

THRESHOLD = 2.0  # AI/human 平均分離倍數下限


def rate_per_500(sa_findings, words):
    """S/A findings 密度（每 500 字）。words<=0 視為 0 以防除零。"""
    if words <= 0:
        return 0.0
    return sa_findings / words * 500.0


def analyze(passages, threshold=THRESHOLD, pos_label="ai", neg_label="human"):
    """passages: {id: {label, words, sa_findings}} -> 分析結果 dict。

    pos_label = 「該被 flag」那組（預期 S/A 高）；neg_label = 「該乾淨」那組。
    預設 ai/human（spec 原框架）；本案實測用 empty/substantive（驗證軸＝空 vs 實）。
    """
    rows = []
    for pid, rec in passages.items():
        rows.append({
            "id": pid,
            "label": rec["label"],
            "words": rec["words"],
            "sa_findings": rec["sa_findings"],
            "rate": rate_per_500(rec["sa_findings"], rec["words"]),
        })
    pos = [r["rate"] for r in rows if r["label"] == pos_label]
    neg = [r["rate"] for r in rows if r["label"] == neg_label]
    if not pos or not neg:
        raise ValueError(f"需要 {pos_label} 與 {neg_label} 兩組各至少一段")

    mean_ai = mean(pos)
    mean_human = mean(neg)
    if mean_human > 0:
        ratio = mean_ai / mean_human
    else:
        ratio = float("inf") if mean_ai > 0 else 0.0

    passed = (mean_ai > mean_human) and (ratio >= threshold)
    return {
        "rows": sorted(rows, key=lambda r: (r["label"], r["id"])),
        "mean_ai": mean_ai,
        "mean_human": mean_human,
        "ratio": ratio,
        "threshold": threshold,
        "passed": passed,
        "pos_label": pos_label,
        "neg_label": neg_label,
    }


def format_report(res):
    lines = []
    lines.append(f"{'id':<6}{'label':<8}{'words':>6}{'S/A':>5}{'per500':>9}")
    lines.append("-" * 34)
    for r in res["rows"]:
        lines.append(f"{r['id']:<6}{r['label']:<8}{r['words']:>6}{r['sa_findings']:>5}{r['rate']:>9.2f}")
    lines.append("-" * 34)
    pos, neg = res["pos_label"], res["neg_label"]
    lines.append(f"mean({pos:<11}) = {res['mean_ai']:.2f}  S/A per 500")
    lines.append(f"mean({neg:<11}) = {res['mean_human']:.2f}  S/A per 500")
    ratio = res["ratio"]
    ratio_s = "inf" if ratio == float("inf") else f"{ratio:.2f}"
    lines.append(f"separation  = {ratio_s}x  (threshold {res['threshold']:.1f}x)")
    lines.append("")
    lines.append("VERDICT: " + (f"PASS — critic 分得開「{pos}」/「{neg}」，可信" if res["passed"]
                                 else "FAIL — 分不開，回 Task 2 改 rubric/錨"))
    return "\n".join(lines)


def selftest():
    """TDD：先寫期望斷言，確認 analyze 邏輯對。"""
    # 1) 明顯分得開：AI 高、真人全 0 → ratio=inf、pass
    sep = analyze({
        "p1": {"label": "human", "words": 100, "sa_findings": 0},
        "p2": {"label": "human", "words": 100, "sa_findings": 0},
        "p3": {"label": "ai", "words": 100, "sa_findings": 3},
        "p4": {"label": "ai", "words": 100, "sa_findings": 5},
    })
    assert sep["mean_human"] == 0.0, sep
    assert sep["mean_ai"] == 20.0, sep            # (15+25)/2 per 500
    assert sep["ratio"] == float("inf"), sep
    assert sep["passed"] is True, sep

    # 2) AI>human 但倍數 <2 → fail
    weak = analyze({
        "p1": {"label": "human", "words": 100, "sa_findings": 2},  # 10/500
        "p2": {"label": "ai", "words": 100, "sa_findings": 3},     # 15/500 → 1.5x
    })
    assert abs(weak["ratio"] - 1.5) < 1e-9, weak
    assert weak["passed"] is False, weak

    # 3) AI<human（critic 反向誤判）→ fail
    inv = analyze({
        "p1": {"label": "human", "words": 100, "sa_findings": 4},
        "p2": {"label": "ai", "words": 100, "sa_findings": 1},
    })
    assert inv["passed"] is False, inv

    # 4) 恰好 2× → pass（邊界含等號）
    edge = analyze({
        "p1": {"label": "human", "words": 100, "sa_findings": 1},  # 5/500
        "p2": {"label": "ai", "words": 100, "sa_findings": 2},     # 10/500 → 2.0x
    })
    assert abs(edge["ratio"] - 2.0) < 1e-9, edge
    assert edge["passed"] is True, edge

    # 5) 密度而非絕對數：字數正規化正確（長真人段多 1 個 finding 不該被當高密度）
    norm = analyze({
        "p1": {"label": "human", "words": 500, "sa_findings": 1},  # 1.0/500
        "p2": {"label": "ai", "words": 100, "sa_findings": 1},     # 5.0/500 → 5x
    })
    assert abs(norm["ratio"] - 5.0) < 1e-9, norm
    assert norm["passed"] is True, norm

    print("selftest OK（5 案全過）")


def main(argv):
    if len(argv) == 2 and argv[1] == "--selftest":
        selftest()
        return 0
    if len(argv) not in (2, 4):
        print(__doc__)
        return 2
    with open(argv[1], encoding="utf-8") as f:
        passages = json.load(f)
    if len(argv) == 4:
        res = analyze(passages, pos_label=argv[2], neg_label=argv[3])
    else:
        res = analyze(passages)
    print(format_report(res))
    return 0 if res["passed"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
