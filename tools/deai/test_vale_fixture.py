"""跑 Vale 對 fixture，斷言 flag 命中且不誤砍。跑：python tools/deai/test_vale_fixture.py"""
import subprocess, sys, json

def vale_json(path):
    # encoding="utf-8" 強制以 UTF-8 解 Vale 輸出——否則 Windows cp950 主控台會 UnicodeDecodeError
    # 噎在規則訊息的繁中字（同 doctor.py 對主控台做的 reconfigure）。
    out = subprocess.run(["vale", "--output=JSON", path], capture_output=True,
                         text=True, encoding="utf-8", errors="replace")
    return json.loads(out.stdout or "{}")

tell = vale_json("handout/html/_audit/fixtures/ai-tell-fixture.html")
ctrl = vale_json("handout/html/_audit/fixtures/clean-control.html")

tell_hits = [m["Match"].lower() for alerts in tell.values() for m in alerts]
ctrl_hits = [m["Match"] for alerts in ctrl.values() for m in alerts]

errors = []
# 必須抓到的 tell（含 copula-avoidance、negative parallelism）
for needle in ["it is worth noting", "serves as", "delve", "not only"]:
    if not any(needle in h for h in tell_hits):
        errors.append(f"漏抓 tell：{needle}")
# 不可誤砍：數學詞 robust（在 accept）、$...$ 內任何符號
if any("robust" in h for h in tell_hits):
    errors.append("誤砍受保護數學詞 robust")
if any(sym in " ".join(tell_hits) for sym in ["sqrt", "x^2", "f^{-1}", "infty"]):
    errors.append("誤砍 $...$ 內數學符號")
# 對照組應乾淨（'Notice that' 是 §3 鼓勵連接詞，單次不該 flag）
if ctrl_hits:
    errors.append(f"對照組誤報：{ctrl_hits}")

if errors:
    print("FAIL:\n" + "\n".join(errors)); sys.exit(1)
print("OK: Vale fixture 通過"); sys.exit(0)
