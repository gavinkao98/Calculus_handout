"""House audio cue policy for lesson videos (see DESIGN.md 'Audio policy').

Maps a scene to its house music/effect cue at compose time. The default cue set
is **Candidate B ("溫暖低調")**, chosen by the user 2026-07-02. Per the policy the
video is narration-first: only the brand scenes carry a cue --

    intro   -> soft pad bed        (candidate_b_intro_bed.wav)
    outro   -> soft pad bed        (candidate_b_outro_bed.wav)
    divider -> soft one-shot stinger (candidate_b_divider_stinger.wav)

-- and every teaching template (definition_math / theorem_proof / derivation /
graph / value_table / sign_chart / callout / recap_cards) stays dry. The caution
ping is available in the set but OFF by default (DESIGN.md: enable per-deck only
for a real notation trap; §3.1 uses no ping).

Cues are the repo's own procedural WAVs (``assets/audio/house/``, no third-party
samples). They are 48 kHz stereo -- the compose output format -- so compose mixes
them without resampling. To change the policy, edit the CueSpec rows below.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

HOUSE_DIR = Path(__file__).resolve().parent / "assets" / "audio" / "house"
CUE_SET = "candidate_b"   # Candidate B -- warm / understated (user decision 2026-07-02)


@dataclass(frozen=True)
class CueSpec:
    """A house cue to lay under a (narration-less) brand scene.

    gain      linear gain applied to the already soft-normalized cue.
    fade_out  seconds; fade the cue out so it lands cleanly at the scene's end
              (beds are longer than the intro scene, so they must fade, not clip).
    """
    path: Path
    gain: float
    fade_out: float


# Policy table -- one CueSpec per brand-scene kind. Beds play near unity (they are
# already normalized soft, ~0.16 peak); the divider stinger is pulled down further
# ("音量淡", user decision). Edit these rows to retune levels or swap the cue set.
_INTRO = CueSpec(HOUSE_DIR / f"{CUE_SET}_intro_bed.wav", gain=1.0, fade_out=0.6)
_OUTRO = CueSpec(HOUSE_DIR / f"{CUE_SET}_outro_bed.wav", gain=1.0, fade_out=0.8)
_DIVIDER = CueSpec(HOUSE_DIR / f"{CUE_SET}_divider_stinger.wav", gain=0.6, fade_out=0.4)


def cue_for_scene(scene: dict) -> CueSpec | None:
    """Return the house cue for a scene, or None for a dry (narration-first) scene.

    Only brand scenes carry a cue: intro bed, outro bed, divider stinger. Every
    teaching template returns None. The caution ping is off by default -- to
    enable it for a deck, add a branch here matching ``template == 'callout'`` and
    ``type == 'caution'`` (compose would then amix the ping under the narration).
    """
    kind = scene.get("kind", "content")
    if kind == "intro":
        return _INTRO
    if kind == "outro":
        return _OUTRO
    if kind == "divider":
        return _DIVIDER
    return None
