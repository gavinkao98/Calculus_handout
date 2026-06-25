"""種子清單 curation 守門：跑 `python tools/deai/check_seed.py`。"""
import sys, pathlib

VOCAB = pathlib.Path("styles/config/vocabularies/AItexture")
reject = (VOCAB / "reject.txt").read_text(encoding="utf-8").lower().splitlines()
accept = (VOCAB / "accept.txt").read_text(encoding="utf-8").lower().splitlines()

# 合法數學詞絕不可出現在 reject（否則誤砍課文）
MATH_WORDS = ["leverage", "robust", "comprehensive", "integral",
              "intrinsic", "examine", "demonstrate", "derive", "bound"]
# 已知 AI-tell 必須在 reject
MUST_FLAG = ["delve into", "it is worth noting that", "serves as a",
             "plays a crucial role in", "rich tapestry"]

errors = []
for w in MATH_WORDS:
    if any(w == line.strip() for line in reject):
        errors.append(f"數學詞誤入 reject：{w}")
    if not any(w == line.strip() for line in accept):
        errors.append(f"數學詞未受 accept 保護：{w}")
for p in MUST_FLAG:
    if not any(p == line.strip() for line in reject):
        errors.append(f"已知 tell 不在 reject：{p}")

if errors:
    print("FAIL:\n" + "\n".join(errors)); sys.exit(1)
print(f"OK: reject={len(reject)} accept={len(accept)}"); sys.exit(0)
