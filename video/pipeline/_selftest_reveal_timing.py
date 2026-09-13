"""Self-test: {show statement} makes the statement card enter on that beat. Run from video/:
    python -m pipeline._selftest_reveal_timing

Before this primitive the `statement` Block was unconditionally static, so a scene whose
`say` named `{show statement}` put the card on screen at t=0 AND re-played a FadeIn on the
already-visible mobject at the marker -- the "reveal前後兩幀無差" finding on
ch03 continuity_statement_sin_limit (rewatch R2, 2026-09-12). The marker is the opt-in:
a scene that does NOT name it keeps the card in the opening frame exactly as before.

Also locks P1-2: the PROOF eyebrow rides with proof.0 instead of standing alone in the
opening frame when the proof is narration-revealed. HOW it rides -- its own Block carrying
`reveal_with`, proof against a hook that replaces proof.0's anim -- is
`_selftest_theorem_proof_label`; this file only locks the timing switch itself.
"""
import pathlib

import yaml

from pipeline import _bootstrap

_bootstrap.bootstrap()   # templates import manim at module level -- bootstrap FIRST (repo rule)

from pipeline.templates import build_blocks

_META = {"id": "_t", "chapter": "Chapter 9", "section": "9.9", "title": "T", "theme": "midnight"}

_THM_BASE = {
    "id": "thm", "kind": "content", "template": "theorem_proof", "accent": "theorem",
    "title": "A Theorem",
    "statement": "Every $f$ is nice.",
    "proof": ["$a = b$", "$b = c$"],
    "qed": "$a = c$",
}
_DER_BASE = {
    "id": "der", "kind": "content", "template": "derivation", "accent": "definition",
    "title": "A Derivation",
    "statement": "We chase the quotient.",
    "steps": [{"math": "a = b", "reason": "given"}],
    "result": {"math": "a = c", "reason": "so"},
}
_DEF_BASE = {
    "id": "def", "kind": "content", "template": "definition_math", "accent": "definition",
    "title": "A Definition",
    "statement": "A thing is nice when it behaves.",
    "math": ["$a = b$"],
}


def _build(base: dict, say: str):
    spec = {**base, "say": say}
    return build_blocks(spec, {"ground": "dark", "meta": _META})


def _block(blocks, bid: str):
    return next(b for b in blocks if b.id == bid)


def _ids(blocks):
    return {b.id for b in blocks}


# -- theorem_proof ----------------------------------------------------------

def test_theorem_statement_static_without_marker():
    b = _block(_build(_THM_BASE, "Words. {show proof.0} More."), "statement")
    assert b.static is True and b.anim == "fade"


def test_theorem_statement_dynamic_with_marker():
    b = _block(_build(_THM_BASE, "Words. {show statement} The claim. {show proof.0} More."),
               "statement")
    assert b.static is False, "{show statement} must make the card enter on that beat"
    assert b.anim == "slide"


def test_theorem_aside_path_follows_the_marker_too():
    aside_spec = {"id": "prop", "kind": "content", "template": "theorem_proof",
                  "accent": "proposition", "title": "A Proposition",
                  "statement": "Every $f$ is nice.",
                  "aside": {"title": "Note", "body": "Only for nice $f$."}}
    off = _block(_build(aside_spec, "Words only."), "statement")
    on = _block(_build(aside_spec, "Words. {show statement} The claim."), "statement")
    assert off.static is True and off.anim == "fade"
    assert on.static is False and on.anim == "slide"


# -- derivation -------------------------------------------------------------

def test_derivation_statement_static_without_marker():
    b = _block(_build(_DER_BASE, "Words. {show step.0} More."), "statement")
    assert b.static is True and b.anim == "fade"


def test_derivation_statement_dynamic_with_marker():
    b = _block(_build(_DER_BASE, "Words. {show statement} The setup. {show step.0} More."),
               "statement")
    assert b.static is False and b.anim == "slide"


# -- definition_math --------------------------------------------------------
# This template was missed when ⑦ wired the primitive into theorem_proof/derivation, so
# the 13 scenes across three decks that DO write {show statement} were re-fading a card
# already on screen (ch03 §3.1: why_trig_is_different / derivative_cycle /
# toward_the_chain_rule -- 17.3 s, 6.8 s and 9.6 s of narration with no frame change).

def test_definition_statement_static_without_marker():
    b = _block(_build(_DEF_BASE, "Words. {show math.0} More."), "statement")
    assert b.static is True and b.anim == "fade"


def test_definition_statement_dynamic_with_marker():
    b = _block(_build(_DEF_BASE, "Words. {show statement} The claim. {show math.0} More."),
               "statement")
    assert b.static is False and b.anim == "slide"


# -- P1-2: the PROOF eyebrow rides with proof.0 -----------------------------

def test_proof_label_static_when_proof_not_revealed():
    blocks = _build(_THM_BASE, "Words only, no markers.")
    assert "proof_label" in _ids(blocks), "label stands alone when nothing reveals proof.0"
    assert _block(blocks, "proof_label").static is True


def test_proof_label_rides_with_proof0_when_revealed():
    blocks = _build(_THM_BASE, "Words. {show proof.0} The first step.")
    label = _block(blocks, "proof_label")
    assert label.static is False, \
        "the PROOF eyebrow must ride with proof.0, not sit in the opening frame"
    assert label.reveal_with == "proof.0"
    assert _block(blocks, "proof.0").static is False


def test_proof_label_riding_does_not_change_measured_geometry():
    """The eyebrow rides as a Block of its OWN, never inside proof.0's mobject. A VGroup
    spanning label-to-row would hand the layout gates a box with a hollow middle, and the
    overlap / capacity guards read that empty span as content (it warned on
    _demo_tall_rows)."""
    riding = _block(_build(_THM_BASE, "Words. {show proof.0} The first step."), "proof.0").mobject
    plain = _block(_build(_THM_BASE, "Words only, no markers."), "proof.0").mobject
    assert abs(riding.get_left()[0] - plain.get_left()[0]) < 1e-6
    assert abs(riding.get_center()[1] - plain.get_center()[1]) < 1e-6
    assert abs(riding.height - plain.height) < 1e-6 and abs(riding.width - plain.width) < 1e-6


if __name__ == "__main__":
    import sys, traceback
    fails = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn(); print(f"PASS {name}")
            except Exception:
                fails += 1; print(f"FAIL {name}"); traceback.print_exc()
    sys.exit(1 if fails else 0)
