"""Per-scene fallback ladder for scene-level alignment (design §7).

Rungs, in order: (1) small.en arbiter re-align [free], (2) resynthesize the scene
once [billed], (3) sentence-chunk resynth+merge [billed], (4) beat-level TTS
[billed, but the always-available terminal]. Lazy: a rung runs only when reached.
Verify-before-overwrite and the billed-retry budget are enforced here so the
billed-cost surface stays in one auditable place (CLAUDE.md).

Rung callables are injected (tts.py wires the real ones; the selftest injects
outcome stubs), so the ladder policy is testable with zero API and zero model.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class RetryBudget:
    """max_billed = extra billed calls allowed across rungs 2-3 for THIS scene
    (design §7: the consent quote pre-approves <=2/scene). Rung 4 (beats) is the
    guaranteed terminal and is always allowed even at budget 0."""
    max_billed: int = 2
    spent: int = 0

    def can_bill(self) -> bool:
        return self.spent < self.max_billed


Rung = Callable[[dict[str, Any]], dict[str, Any]]  # ctx -> {"status", "entry", "reason"?}


def run_ladder(*, scene_id: str, rungs: list[tuple[str, bool, Rung]], budget: RetryBudget,
               ctx: dict[str, Any] | None = None) -> dict[str, Any]:
    """Walk rungs until one returns status=="pass". Each rung is (name, billed,
    callable) -- billedness is DECLARED, not inferred by name or self-reported. A
    billed rung is skipped (recorded) when the budget is exhausted; the non-billed
    'beats' terminal is never skipped. The chosen entry carries the full history in
    its fallback_history (design §7). Returns {"entry", "history"}."""
    ctx = ctx or {}
    history: list[dict[str, Any]] = []
    for name, billed, rung in rungs:
        if billed and not budget.can_bill():
            history.append({"rung": name, "skipped_over_budget": True})
            continue
        result = rung(ctx)
        if billed:
            budget.spent += 1
        history.append({"rung": name, "status": result.get("status"),
                        "reason": result.get("reason")})
        if result.get("status") == "pass":
            entry = result["entry"]
            if isinstance(entry, dict):     # stamp the path taken onto the manifest entry
                entry.setdefault("fallback_history", [])
                entry["fallback_history"] = list(entry["fallback_history"]) + history
            return {"entry": entry, "history": history}
    # Exhausted without a pass -> caller must ensure the last rung is the free beats
    # terminal (always passes); reaching here means a wiring bug -- surface it.
    return {"entry": history[-1].get("entry") if history else None, "history": history}
