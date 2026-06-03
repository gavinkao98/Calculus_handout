#!/usr/bin/env python3
"""Seed -> two-model auto-converge experiment (GPT drafts, Gemini audits).

Isolated experiment for the handout-refactor question: if one model free-expands
a sparse manuscript SEED and a SECOND model audits it, does an unattended
draft<->audit loop converge on correct content, or rubber-stamp a shared
hallucination? Claude stays OUT of the loop and grades the result separately.

Mirrors the API conventions of video/pipeline/review_pack.py and critic.py:
stdlib urllib, OpenAI-compatible /chat/completions, env-var keys, the
--dry-run/--confirm/--smoke cost gates, exponential-backoff retry, and a
tolerant JSON parser (LaTeX inside JSON breaks json.loads).

BILLED when run with --confirm. Keys are read from the environment
(OPENAI_API_KEY / GEMINI_API_KEY) -- never a flag, never a file, never logged.

Usage:
    python run.py --dry-run                       # free: write prompts + estimate
    python run.py --confirm --smoke               # ~2 billed calls, validate plumbing
    python run.py --confirm                        # full bounded loop (<= max-rounds)
    python run.py --drafter openai:gpt-5.1 --auditor gemini:gemini-2.5-pro --confirm
"""
import argparse
import json
import os
import re
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT_ROOT = HERE / "out"

# Providers speak the OpenAI /chat/completions shape. Gemini exposes an
# OpenAI-compatible endpoint, so one urllib path covers both -- only base_url,
# the token-cap field name, and the key env var differ.
PROVIDERS = {
    "openai": {
        "base_url": "https://api.openai.com/v1",
        "env": "OPENAI_API_KEY",
        "token_param": "max_completion_tokens",  # newer OpenAI models reject max_tokens
    },
    "gemini": {
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai",
        "env": "GEMINI_API_KEY",
        "token_param": "max_tokens",
    },
}
# Defaults are OVERRIDABLE via --drafter/--auditor and printed at --dry-run for
# confirmation; the exact current model ids may differ from these guesses.
DEFAULT_MODELS = {"openai": "gpt-5.1", "gemini": "gemini-2.5-pro"}

# PLACEHOLDER prices, USD per 1M tokens (input, output) -- estimate only.
PRICE = {"openai": (1.25, 10.0), "gemini": (1.25, 5.0)}
CHARS_PER_TOKEN = 3.2
EST_OUTPUT_TOKENS = 4000  # rough per-call output for the dry-run estimate


# --------------------------------------------------------------------------- #
# API call (mirrors review_pack.py:358-388)
# --------------------------------------------------------------------------- #
def _extract_json(text: str) -> dict:
    """Lenient: strip a ```json fence, take the outer {...}, repair illegal
    backslash escapes (the model writes LaTeX like $\\sqrt[3]{x}$ inside string
    values, and a lone backslash crashes json.loads). Same fix as review_pack.py."""
    s = (text or "").strip()
    if s.startswith("```"):
        s = s.split("```", 2)[1]
        if s.lstrip().startswith("json"):
            s = s.lstrip()[4:]
    i, j = s.find("{"), s.rfind("}")
    if 0 <= i < j:
        s = s[i:j + 1]
    try:
        return json.loads(s)
    except Exception:  # noqa: BLE001
        return json.loads(re.sub(r'\\(?![\\"/bfnrtu])', r"\\\\", s))


def call(provider: str, model: str, system: str, user: str, *,
         api_key: str, max_tokens: int, timeout: int = 180, retries: int = 3):
    """POST one chat completion. Returns (content_text, usage_dict)."""
    spec = PROVIDERS[provider]
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        spec["token_param"]: max_tokens,
    }
    req = urllib.request.Request(
        f"{spec['base_url'].rstrip('/')}/chat/completions",
        data=json.dumps(payload).encode("utf-8"), method="POST",
        headers={"Content-Type": "application/json",
                 "Authorization": f"Bearer {api_key}"},
    )
    data = None
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            break
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and attempt < retries:
                time.sleep((2 ** attempt) * 2)
                continue
            raise
        except (urllib.error.URLError, TimeoutError):
            if attempt < retries:
                time.sleep((2 ** attempt) * 2)
                continue
            raise
    content = data["choices"][0]["message"]["content"]
    return content, data.get("usage", {})


# --------------------------------------------------------------------------- #
# Prompts
# --------------------------------------------------------------------------- #
def drafter_prompt(seed: str, rules: str, prev_draft=None, findings=None):
    system = (
        "You expand a SPARSE seed of one section of a university calculus handout "
        "into a complete, self-contained textbook draft in LaTeX, in the "
        "Stewart/Rogawski self-study register. The seed is ONLY a seed: you MAY "
        "reorganize, rewrite, and add motivating prose, worked examples, TikZ "
        "figures, and strategy/caution boxes freely -- richness is wanted. But "
        "every mathematical claim MUST be correct and standard; do NOT invent "
        "theorems, identities, named results, or historical attributions. Follow "
        "the house rules. Output ONLY the LaTeX for the section body (no preamble, "
        "no \\documentclass)."
    )
    parts = [f"=== HOUSE RULES ===\n{rules}", f"=== SEED (section 1.1) ===\n{seed}"]
    if prev_draft is not None:
        parts.append("=== YOUR PREVIOUS DRAFT ===\n" + prev_draft)
        parts.append(
            "=== AUDITOR FINDINGS ===\n"
            + json.dumps(findings, ensure_ascii=False, indent=2)
            + "\n\nRevise to resolve the level-1 and level-2 findings. Do NOT "
            "blindly cut correct, useful richness. Return the FULL revised LaTeX.")
    else:
        parts.append("Write the full section draft now. Return ONLY LaTeX.")
    return system, "\n\n".join(parts)


def auditor_prompt(seed: str, rules: str, draft: str):
    system = (
        "You are an ADVISORY adversarial reviewer of a calculus handout section "
        "that was expanded from the SEED below. You do NOT rewrite; you surface "
        "findings for a human. Hunt especially for: (a) mathematical errors, "
        "fabricated theorems/identities, or over-generalized claims; (b) drift "
        "from the seed's mathematics; (c) house-rule / register violations.\n"
        "Classify EVERY finding into exactly one level (do not inflate):\n"
        "  1 real-conflict   -- wrong math or a stated-rule violation (must fix)\n"
        "  2 discoverability -- not wrong, under-specified / worth a note\n"
        "  3 editorial-drift -- low-priority style risk, not a defect\n"
        "  4 non-finding     -- e.g. wording differs but is mathematically equivalent\n"
        "Only levels 1-2 are actionable; over-reporting dilutes the real findings. "
        'Set "converged": true ONLY when there are zero level-1 AND zero level-2 '
        "findings. Return STRICT JSON only, no prose around it:\n"
        '{"converged":bool,"findings":[{"level":int,"severity":"low|med|high",'
        '"where":str,"issue":str,"evidence":str,"suggestion":str}],"summary":str}'
    )
    user = (f"=== HOUSE RULES ===\n{rules}\n\n"
            f"=== SEED (the intended mathematical scope, section 1.1) ===\n{seed}\n\n"
            f"=== DRAFT TO REVIEW ===\n{draft}")
    return system, user


# --------------------------------------------------------------------------- #
# Convergence loop
# --------------------------------------------------------------------------- #
def _usage(used: dict, provider: str, model: str) -> dict:
    pin, pout = int(used.get("prompt_tokens", 0)), int(used.get("completion_tokens", 0))
    cin, cout = PRICE[provider]
    return {"provider": provider, "model": model, "prompt_tokens": pin,
            "completion_tokens": pout, "usd": round(pin / 1e6 * cin + pout / 1e6 * cout, 4)}


def _actionable(findings):
    return [f for f in findings if int(f.get("level", 9)) in (1, 2)]


def run_loop(seed, rules, *, drafter, auditor, keys, out_dir, max_rounds, max_tokens, smoke):
    out_dir.mkdir(parents=True, exist_ok=True)
    (dp, dm), (ap, am) = drafter, auditor
    usage_log, trace = [], []

    s, u = drafter_prompt(seed, rules)
    draft, used = call(dp, dm, s, u, api_key=keys[dp], max_tokens=max_tokens)
    usage_log.append({"role": "drafter", "round": 0, **_usage(used, dp, dm)})
    (out_dir / "round_00_draft.tex").write_text(draft, encoding="utf-8")
    trace.append(f"Round 0: drafter ({dp}:{dm}) produced {len(draft)} chars.")

    converged, rounds_run = False, 0
    for k in range(1, max_rounds + 1):
        rounds_run = k
        s, u = auditor_prompt(seed, rules, draft)
        raw, used = call(ap, am, s, u, api_key=keys[ap], max_tokens=max_tokens)
        usage_log.append({"role": "auditor", "round": k, **_usage(used, ap, am)})
        try:
            verdict = _extract_json(raw)
        except Exception as e:  # noqa: BLE001
            verdict = {"converged": False, "findings": [],
                       "summary": f"PARSE_FAIL: {e}", "_raw": raw}
        (out_dir / f"round_{k:02d}_findings.json").write_text(
            json.dumps(verdict, ensure_ascii=False, indent=2), encoding="utf-8")
        acts = _actionable(verdict.get("findings", []))
        trace.append(
            f"Round {k}: auditor ({ap}:{am}) converged={verdict.get('converged')}, "
            f"{len(acts)} actionable / {len(verdict.get('findings', []))} total. "
            f"{verdict.get('summary', '')}")

        if verdict.get("converged") and not acts:
            converged = True
            break
        if not acts:
            converged = True
            trace.append(f"Round {k}: no actionable findings -> treat as converged.")
            break
        if smoke:
            trace.append("smoke: stopping after one audit round.")
            break

        s, u = drafter_prompt(seed, rules, prev_draft=draft, findings=verdict.get("findings", []))
        new_draft, used = call(dp, dm, s, u, api_key=keys[dp], max_tokens=max_tokens)
        usage_log.append({"role": "drafter", "round": k, **_usage(used, dp, dm)})
        (out_dir / f"round_{k:02d}_draft.tex").write_text(new_draft, encoding="utf-8")
        if new_draft.strip() == draft.strip():
            trace.append(f"Round {k}: draft unchanged -> stop.")
            draft = new_draft
            break
        draft = new_draft

    (out_dir / "final_draft.tex").write_text(draft, encoding="utf-8")
    total = round(sum(c["usd"] for c in usage_log), 4)
    (out_dir / "usage.json").write_text(
        json.dumps({"calls": usage_log, "total_usd": total}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    (out_dir / "trace.md").write_text(
        f"# Convergence trace\n\n"
        f"drafter={dp}:{dm}  auditor={ap}:{am}  max_rounds={max_rounds}  smoke={smoke}\n\n"
        f"**converged={converged}** after {rounds_run} audit round(s); "
        f"est. ${total} over {len(usage_log)} call(s)\n\n"
        + "\n".join(f"- {t}" for t in trace) + "\n", encoding="utf-8")
    print(f"[converge] total est. ${total} over {len(usage_log)} call(s)", flush=True)
    return converged, rounds_run, total


# --------------------------------------------------------------------------- #
# Dry run (free)
# --------------------------------------------------------------------------- #
def dry_run(seed, rules, drafter, auditor, out_dir, max_rounds, max_tokens):
    (dp, dm), (ap, am) = drafter, auditor
    pdir = out_dir / "prompts"
    pdir.mkdir(parents=True, exist_ok=True)
    ds, du = drafter_prompt(seed, rules)
    as_, au = auditor_prompt(seed, rules, "<<DRAFT GOES HERE>>")
    (pdir / "drafter_round0.txt").write_text(ds + "\n\n----\n\n" + du, encoding="utf-8")
    (pdir / "auditor_sample.txt").write_text(as_ + "\n\n----\n\n" + au, encoding="utf-8")

    draft_in = int(len(ds + du) / CHARS_PER_TOKEN)
    audit_in = int(len(as_ + au) / CHARS_PER_TOKEN) + EST_OUTPUT_TOKENS
    cin_d, cout_d = PRICE[dp]
    cin_a, cout_a = PRICE[ap]
    n_draft, n_audit = 1 + max_rounds, max_rounds  # worst case: revise every round
    usd = (n_draft * ((draft_in + EST_OUTPUT_TOKENS) / 1e6 * cin_d + EST_OUTPUT_TOKENS / 1e6 * cout_d)
           + n_audit * (audit_in / 1e6 * cin_a + EST_OUTPUT_TOKENS / 1e6 * cout_a))

    print("[converge] DRY RUN -- no API calls.")
    print(f"  drafter = {dp}:{dm}   auditor = {ap}:{am}   max_rounds = {max_rounds}   max_tokens = {max_tokens}")
    print(f"  round-0 drafter prompt ~ {draft_in} input tokens")
    print(f"  worst case: {n_draft} drafter + {n_audit} auditor calls")
    print(f"  rough estimate: ${usd:.2f}   (PLACEHOLDER prices; confirm the model ids above)")
    print(f"  prompts written to {pdir}")
    print("  to run billed: set OPENAI_API_KEY / GEMINI_API_KEY, then --confirm (add --smoke first).")


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def _role(spec: str):
    provider, _, model = spec.partition(":")
    if provider not in PROVIDERS:
        raise SystemExit(f"unknown provider {provider!r}; choose from {list(PROVIDERS)}")
    return provider, (model or DEFAULT_MODELS[provider])


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Seed -> two-model auto-converge experiment (offline; billed call gated).")
    ap.add_argument("--drafter", default="openai", help="provider[:model], default openai")
    ap.add_argument("--auditor", default="gemini", help="provider[:model], default gemini")
    ap.add_argument("--seed", type=Path, default=HERE / "seed_s11.md")
    ap.add_argument("--rules", type=Path, default=HERE / "rules.md")
    ap.add_argument("--max-rounds", type=int, default=4)
    ap.add_argument("--max-tokens", type=int, default=8000)
    ap.add_argument("--run-name", default=None, help="output subdir under out/ (default: timestamp)")
    ap.add_argument("--dry-run", action="store_true",
                    help="write prompts + print a cost estimate; never calls the API")
    ap.add_argument("--confirm", action="store_true",
                    help="actually call the APIs (BILLED). Keys from env OPENAI_API_KEY / GEMINI_API_KEY.")
    ap.add_argument("--smoke", action="store_true",
                    help="with --confirm, run ONE drafter + ONE auditor call only")
    args = ap.parse_args()

    drafter, auditor = _role(args.drafter), _role(args.auditor)
    seed = args.seed.read_text(encoding="utf-8")
    rules = args.rules.read_text(encoding="utf-8")
    run_name = args.run_name or datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = OUT_ROOT / run_name

    if args.confirm:
        keys = {}
        for provider, _model in (drafter, auditor):
            env = PROVIDERS[provider]["env"]
            key = os.environ.get(env)
            if not key:
                print(f"[converge] --confirm needs the key in env {env} "
                      f"(never pass it as a flag, never write it to a file).", flush=True)
                return 2
            keys[provider] = key
        conv, rounds, total = run_loop(
            seed, rules, drafter=drafter, auditor=auditor, keys=keys,
            out_dir=out_dir, max_rounds=args.max_rounds, max_tokens=args.max_tokens, smoke=args.smoke)
        print(f"[converge] done: converged={conv} after {rounds} round(s), est. ${total}. out={out_dir}",
              flush=True)
        return 0
    if args.dry_run:
        dry_run(seed, rules, drafter, auditor, out_dir, args.max_rounds, args.max_tokens)
        return 0
    print("[converge] nothing ran. Re-run with --dry-run for the plan + estimate, "
          "or --confirm for the billed loop (keys from env OPENAI_API_KEY / GEMINI_API_KEY).", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
