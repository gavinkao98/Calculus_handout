"""LessonScene -- the single player that reveals Blocks uniformly.

Ground-aware: intro/outro render on the LIGHT paper ground, teaching scenes on
the DARK canvas. Background and the palette templates pull from are both chosen
from the scene kind here.

Reveal timing is audio-driven: when ``beat_durations`` is supplied (from the TTS
manifest), each beat ends exactly one narration clip after the one before it --
the hold runs until the CUMULATIVE target, read off ``renderer.time``, so manim's
per-play frame rounding cannot accumulate (see ``_play_content``). Without it,
``estimate_seconds`` (word count) stands in -- the alignment model is identical,
only the clock changes.
"""
from __future__ import annotations

from typing import Any

from manim import DOWN, UP, FadeIn, FadeOut, Rectangle, Scene

from . import _bootstrap
from . import focus
from .blocks import accent_role, play_block
from .narration import estimate_seconds, parse_say
from .templates import build_blocks
from .timing import (EXIT_FADE_SECONDS, MIN_BEAT_HOLD_SECONDS, SCENE_LEAD_SECONDS,
                     SCENE_TAIL_SECONDS, elapsed, stock_animation_seconds)
from .visuals import theme as T

LIGHT_KINDS = {"intro", "outro"}
MIN_HOLD = MIN_BEAT_HOLD_SECONDS  # floor so long reveal animation never yields negative wait


def dim_ids(spec: dict[str, Any], target: str, wanted: "list[str]") -> "list[str]":
    """A beat's `dim` list, minus the beat's OWN reveal target.

    Since the focus now runs BEFORE the reveal, dimming the block this same beat reveals
    would have `focus.apply` snapshot it (`save_state`) while it is still off screen -- and
    a later `dim: []` would then `restore()` it back to invisible, with no error anywhere.
    `schema._focus_issues` rejects such an entry outright (it is always a typo); this is the
    second line of defence for a spec that dodged the gate.
    """
    out = []
    for block_id in wanted:
        if block_id == target:
            print(f"[focus] {spec.get('id', '?')}: focus[at={target}].dim names its own "
                  f"reveal target {target!r}; skipped (it is not on screen yet)", flush=True)
        else:
            out.append(block_id)
    return out


class LessonScene(Scene):
    spec: dict[str, Any] | None = None
    meta: dict[str, Any] | None = None
    beat_durations: list[float] | None = None  # per-beat narration seconds, in say order
    # The whole deck, {scene id: spec}, so a `carry:` can rebuild the scene it carries from
    # (templates._apply_carry). Injected by make.py / scratch_frames.py next to `spec`.
    scenes_by_id: dict[str, dict[str, Any]] | None = None
    # The CURRENT beat's narration seconds while _play_content walks the beats, None
    # outside one. A block animation that should last as long as the narration it serves
    # ("圖跟旁白長") reads this via timing.beat_run_time(); every stock animation ignores
    # it and keeps its fixed duration.
    beat_seconds: float | None = None
    # How much of the CURRENT beat is already spoken for by something fixed-length that
    # plays before or after the reveal (a `focus[].indicate` flash AFTER it; a `dim` that
    # actually changes the dimmed set, or a `Block.reveal_with` rider, BEFORE it) -- 0
    # outside a beat, or in a beat with none of them. `timing.beat_run_time` subtracts this
    # from a beat-filling reveal's budget so that both land inside the beat, not past it.
    beat_reserved_seconds: float = 0.0

    def construct(self) -> None:
        if self.spec is None:
            raise RuntimeError("LessonScene was not configured (spec missing).")

        # Re-apply the Plex/lmodern TeX template every scene: manim's tempconfig (this
        # scene runs inside `with tempconfig(cfg):`) drops config.tex_template back to
        # the default on each block's exit, so without this only the batch's first scene
        # would build its Tex in Plex (see _bootstrap.apply_tex_template).
        _bootstrap.apply_tex_template()

        kind = self.spec.get("kind", "content")
        ground = "light" if kind in LIGHT_KINDS else "dark"
        self.camera.background_color = T.color(ground, "bg")

        ctx = {"ground": ground, "meta": self.meta or {}, "scenes_by_id": self.scenes_by_id}
        blocks = build_blocks(self.spec, ctx)
        by_id = {b.id: b for b in blocks}

        self._stage(blocks)

        self.wait(SCENE_LEAD_SECONDS)

        narration_end = None
        if kind == "content":
            narration_end = self._play_content(blocks, by_id, ground)
        elif kind == "intro":
            self._play_intro(blocks, ground, float(self.spec.get("duration", 6.0)))
        elif kind == "outro":
            self._play_outro(blocks, ground, float(self.spec.get("duration", 8.0)))
        else:
            self._play_timed(blocks, ground, float(self.spec.get("duration", 3.0)))

        self._tail(kind, by_id, narration_end)

    def _stage(self, blocks) -> None:
        """The opening frame: every static block, plus any dynamic block with a
        `pre_play` (a carried object waiting at its carried-in position -- see
        blocks.Block.pre_play), rewound first and then added."""
        for block in blocks:
            if block.static:
                self.add(block.mobject)
            elif block.pre_play is not None:
                block.pre_play(block.mobject)
                self.add(block.mobject)

    def _tail(self, kind, by_id, narration_end=None) -> None:
        """The SCENE_TAIL_SECONDS hold. `exit: [<block id>...]` (content scenes) fades those
        blocks out INSIDE the hold (EXIT_FADE_SECONDS), so what the next scene does not
        carry leaves before the cut while the clip length -- what the render/audio sync
        audit measures -- is unchanged. NB: the LAST frame, which critic.py / scratch_frames
        read as the scene's "fullest frame", is then the post-exit frame. An id naming no
        block is skipped (sizecheck errors on it before render, as for focus.dim).

        *narration_end* (content scenes on a real render) is the renderer clock the last
        beat was aligned to, so the hold can end SCENE_TAIL_SECONDS after the NARRATION --
        which is exactly what the sync audit measures -- instead of adding a flat second to
        wherever the scene happened to get to. Two things land between the last beat and
        here and neither is narration time: `_play_content`'s closing focus restore
        (FADE_SECONDS, on any scene that dimmed something) and a final beat that overran
        and fell back on MIN_HOLD. Both used to push the whole clip long; they are absorbed
        by the hold now, the same way the `exit` fade already is."""
        exits = (self.spec.get("exit") or []) if kind == "content" else []
        mobs = [by_id[i].mobject for i in exits if i in by_id]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=EXIT_FADE_SECONDS)
        now = elapsed(self)
        if narration_end is None or now is None:
            self.wait(SCENE_TAIL_SECONDS - (EXIT_FADE_SECONDS if mobs else 0.0))
        else:
            self.wait(max(narration_end + SCENE_TAIL_SECONDS - now, MIN_HOLD))

    def _play_content(self, blocks, by_id, ground) -> "float | None":
        """Play the beats; returns the renderer clock the narration ends on (None off a
        real render), which `_tail` holds SCENE_TAIL_SECONDS past."""
        revealed: set[str] = set()
        beats = parse_say(self.spec.get("say", ""))
        durations = self.beat_durations
        # `Block.reveal_with`: a block with no marker of its own that enters on another
        # block's beat (theorem_proof's PROOF eyebrow over proof.0). Grouped by target
        # once, here, so the beat loop stays a dict lookup.
        riders: dict[str, list] = {}
        for block in blocks:
            if block.reveal_with and not block.static:
                riders.setdefault(block.reveal_with, []).append(block)
        focus_plan = focus.scene_focus(self.spec)
        indicate_plan = focus.scene_indicate(self.spec)
        # A scene that declares no `accent` (graph / hook scenes) resolves to `aside_ink`, and a
        # grey flash reads as "dimming" -- the opposite of emphasis (ch03 06, 2026-09-13 pilot).
        # Those flash in the amber highlight ink instead.
        indicate_color = T.color(ground, f"{accent_role(self.spec)}_ink" if self.spec.get("accent")
                                 else "amber_ink")
        dimmed: set[str] = set()
        # Beat holds are aligned to a CUMULATIVE target rather than each beat holding for
        # `its own length - what its reveal consumed`. manim rounds both a `play` and a
        # `wait` up to a whole frame, so the per-beat form leaves every beat a fraction of
        # a frame long and an 8-beat scene a quarter-second long -- exactly the residue the
        # [sync] audit was still reporting after the hooks started measuring themselves.
        # Reading the renderer's clock before each hold instead means a beat that overran
        # is paid for by the next one and the error never accumulates. `start` is None off
        # a real render (the selftests' FakeScene), where the old arithmetic is kept.
        start = elapsed(self)
        elapsed_target = 0.0
        for index, beat in enumerate(beats):
            target = beat.reveal
            consumed = 0.0
            # Resolve THIS beat's length before playing it: an animation that wants to
            # run for the whole beat ("圖跟旁白長") reads it off the scene. Pure reorder
            # -- target_seconds never depended on play_block. `beat_seconds` is None
            # outside a beat (the end-of-scene sweep-up below), so a paced animation
            # falls back to its own default there.
            if durations is not None and index < len(durations):
                target_seconds = durations[index]
            else:
                target_seconds = estimate_seconds(beat.text)
            self.beat_seconds = target_seconds
            # `indicate` (below) always plays AFTER this beat's reveal, and `dim` (further
            # below, but resolved here) always plays BEFORE it -- either way, a reveal that
            # fills the whole beat via `timing.beat_run_time` (a paced walk, a hook's own
            # sweep) must leave both unspent up front, or the reveal overruns the beat by
            # whatever they cost (ch03 06's `ineq` beat -- paced reveal + rule-3 indicate in
            # one beat -- was the first to hit this for indicate; `evenness`'s hook reveal +
            # a declared `dim` is the same trap for dim, since `focus.apply`'s FADE_SECONDS
            # play is not part of the hook's own budget either). `wanted` mirrors
            # `focus.apply`'s own change test (its `by_id` filter included) so this beat
            # reserves FADE_SECONDS only when `apply` a few lines down will actually play
            # something -- a `dim: []` beat that already has nothing dimmed must reserve 0.
            # Both set BEFORE the reveal below so they are in effect while that reveal asks
            # for its budget; 0 in a beat with neither.
            wanted = dim_ids(self.spec, target, focus_plan[target]) if target in focus_plan else None
            dim_changes = False
            if wanted is not None:
                dim_target = {b for b in wanted if b in by_id}
                dim_changes = bool(dim_target - dimmed) or bool(dimmed - dim_target)
            # A `reveal_with` rider (below) plays BEFORE the beat's own reveal and is
            # fixed-length, so it is reserved for the same reason `dim` is: without this a
            # beat-filling reveal would ask for the whole beat and then overrun it by the
            # rider's fade.
            will_reveal = bool(target) and target in by_id and target not in revealed
            riding = ([r for r in riders.get(target, ()) if r.id not in revealed]
                      if will_reveal else [])
            self.beat_reserved_seconds = ((focus.INDICATE_SECONDS if indicate_plan.get(target)
                                          else 0.0)
                                          + (focus.FADE_SECONDS if dim_changes else 0.0)
                                          + sum(stock_animation_seconds(r.anim) or 0.0
                                                for r in riding))
            # The focus runs BEFORE the beat's own reveal. It used to run after, on the
            # reasoning that a just-revealed block earns full attention before anything
            # dims -- but what a `dim` dims is never the block being revealed, it is the
            # OTHER part of the screen that the narration has just steered away from, and
            # it says so in its FIRST sentence. Waiting for the reveal strands the focus at
            # the tail of the beat whenever that reveal fills the beat (a paced walk, a
            # hook): ch03 06's `ineq` restore snapped back only as the next beat started,
            # and ch03 24's `mirror` beat ("hold the bottom graph against the top") left the
            # velocity row lit until the beat's midpoint, because its hook reveal runs ~5 s
            # of an 11.5 s beat. `indicate` stays after the reveal -- it flashes blocks to
            # point at them rather than steering attention away from one.
            if wanted is not None:
                before = dimmed
                dimmed = focus.apply(self, by_id, wanted, dimmed)
                if dimmed != before:
                    consumed += focus.FADE_SECONDS
            if will_reveal:
                # the kicker first, then the block it labels: a "PROOF" eyebrow that
                # arrived after its own first row would read as an afterthought.
                for rider in riding:
                    consumed += play_block(self, rider, ground)
                    revealed.add(rider.id)
                consumed += play_block(self, by_id[target], ground)
                revealed.add(target)
            if target in indicate_plan:
                consumed += focus.indicate(self, by_id, indicate_plan[target], indicate_color)
            # Each beat's video length should equal its narration clip, so hold until the
            # cumulative target instead of for `this beat - what it consumed` (see `start`).
            elapsed_target += target_seconds
            now = elapsed(self)
            if start is None or now is None:
                self.wait(max(target_seconds - consumed, MIN_HOLD))
            else:
                self.wait(max(start + elapsed_target - now, MIN_HOLD))
        self.beat_seconds = None
        self.beat_reserved_seconds = 0.0
        # Leave the scene un-focused: the final frame (what the visual gates read, and
        # what a viewer sits on through the tail) must match the un-focused render.
        focus.apply(self, by_id, [], dimmed)
        for block in blocks:
            if not block.static and block.id not in revealed:
                play_block(self, block, ground)
        return None if start is None else start + elapsed_target

    def _play_timed(self, blocks, ground, duration: float) -> None:
        dynamic = [b for b in blocks if not b.static]
        gap = 0.25
        for block in dynamic:
            play_block(self, block, ground)
            self.wait(gap)
        self.wait(max(duration - gap * len(dynamic), 1.2))

    def _play_intro(self, blocks, ground, duration: float) -> None:
        brand_blocks = [b for b in blocks if not b.static and b.id.startswith("brand.")]
        timeline_blocks = [b for b in blocks if not b.static and b.id.startswith("timeline.")]
        transition = [b for b in blocks if b.id.startswith("transition.")]
        transition_dynamic = [b for b in transition if not b.static]
        by_id = {b.id: b for b in blocks}

        # stage 1: brand opening
        for block in brand_blocks:
            play_block(self, block, ground)
            self.wait(0.08)
        self.wait(max(duration * 0.07, 0.55))

        # stage 2: brand out -> timeline sequence
        if timeline_blocks:
            self.play(
                *[FadeOut(block.mobject, shift=0.05 * DOWN) for block in brand_blocks],
                run_time=0.65,
            )
            self.wait(0.08)

            play_block(self, by_id["timeline.header"], ground)
            self.wait(0.06)
            # optional course-map watermark (bottom-right summit bars): reveal it early so
            # it sits through the timeline animation, then stage 3 fades it out with the rest.
            if "timeline.motif" in by_id:
                play_block(self, by_id["timeline.motif"], ground)
            play_block(self, by_id["timeline.rail"], ground)
            self.wait(0.3)

            if "timeline.pulse" in by_id:
                play_block(self, by_id["timeline.pulse"], ground)
                self.wait(0.2)

            if "timeline.activate" in by_id:
                play_block(self, by_id["timeline.activate"], ground)
                self.wait(0.2)

            if "timeline.title" in by_id:
                play_block(self, by_id["timeline.title"], ground)

            self.wait(max(duration * 0.08, 0.55))

        # stage 3: timeline out -> gradual crossfade to dark
        if transition:
            fade_out_blocks = timeline_blocks if timeline_blocks else brand_blocks
            dark_bg = Rectangle(
                width=T.FRAME_W,
                height=T.FRAME_H,
                stroke_width=0,
                fill_color=T.color("dark", "bg"),
                fill_opacity=1.0,
            )
            self.play(
                *[FadeOut(block.mobject, shift=0.05 * DOWN) for block in fade_out_blocks],
                FadeIn(dark_bg),
                run_time=1.0,
            )
            self.camera.background_color = T.color("dark", "bg")
            self.remove(dark_bg)

            for block in transition_dynamic:
                if block.id == "transition.ground":
                    continue
                play_block(self, block, "dark")
                self.wait(0.06)

        self.wait(max(duration * 0.08, 0.55))

    def _play_outro(self, blocks, ground, duration: float) -> None:
        transition = [b for b in blocks if b.id.startswith("transition.")]
        transition_dynamic = [b for b in transition if not b.static]
        end_slate = [b for b in blocks if not b.static and b.id.startswith("end.")]

        if transition:
            self.camera.background_color = T.color("dark", "bg")
            for block in transition_dynamic:
                play_block(self, block, "dark")
                self.wait(0.06)
            self.wait(max(duration * 0.1, 0.8))
            light_bg = Rectangle(
                width=T.FRAME_W,
                height=T.FRAME_H,
                stroke_width=0,
                fill_color=T.color("light", "bg"),
                fill_opacity=1.0,
            )
            self.play(
                *[FadeOut(block.mobject, shift=0.05 * DOWN) for block in transition],
                FadeIn(light_bg),
                run_time=1.0,
            )
            self.camera.background_color = T.color("light", "bg")
            self.remove(light_bg)
            self.wait(0.25)

        for block in end_slate:
            play_block(self, block, ground)
            self.wait(0.12)

        self.wait(max(duration * 0.25, 2.0))
