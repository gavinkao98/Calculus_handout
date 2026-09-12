"""LessonScene -- the single player that reveals Blocks uniformly.

Ground-aware: intro/outro render on the LIGHT paper ground, teaching scenes on
the DARK canvas. Background and the palette templates pull from are both chosen
from the scene kind here.

Reveal timing is audio-driven: when ``beat_durations`` is supplied (from the TTS
manifest), each beat holds for exactly its measured narration-clip length, minus
the reveal animation already spent. Without it, ``estimate_seconds`` (word count)
stands in -- the alignment model is identical, only the clock changes.
"""
from __future__ import annotations

from typing import Any

from manim import DOWN, UP, FadeIn, FadeOut, Rectangle, Scene

from . import _bootstrap
from . import focus
from .blocks import play_block
from .narration import estimate_seconds, parse_say
from .templates import build_blocks
from .timing import (EXIT_FADE_SECONDS, MIN_BEAT_HOLD_SECONDS, SCENE_LEAD_SECONDS,
                     SCENE_TAIL_SECONDS)
from .visuals import theme as T

LIGHT_KINDS = {"intro", "outro"}
MIN_HOLD = MIN_BEAT_HOLD_SECONDS  # floor so long reveal animation never yields negative wait


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

        if kind == "content":
            self._play_content(blocks, by_id, ground)
        elif kind == "intro":
            self._play_intro(blocks, ground, float(self.spec.get("duration", 6.0)))
        elif kind == "outro":
            self._play_outro(blocks, ground, float(self.spec.get("duration", 8.0)))
        else:
            self._play_timed(blocks, ground, float(self.spec.get("duration", 3.0)))

        self._tail(kind, by_id)

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

    def _tail(self, kind, by_id) -> None:
        """The SCENE_TAIL_SECONDS hold. `exit: [<block id>...]` (content scenes) fades those
        blocks out INSIDE the hold (EXIT_FADE_SECONDS), so what the next scene does not
        carry leaves before the cut while the clip length -- what the render/audio sync
        audit measures -- is unchanged. NB: the LAST frame, which critic.py / scratch_frames
        read as the scene's "fullest frame", is then the post-exit frame. An id naming no
        block is skipped (sizecheck errors on it before render, as for focus.dim)."""
        exits = (self.spec.get("exit") or []) if kind == "content" else []
        mobs = [by_id[i].mobject for i in exits if i in by_id]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=EXIT_FADE_SECONDS)
            self.wait(SCENE_TAIL_SECONDS - EXIT_FADE_SECONDS)
        else:
            self.wait(SCENE_TAIL_SECONDS)

    def _play_content(self, blocks, by_id, ground) -> None:
        revealed: set[str] = set()
        beats = parse_say(self.spec.get("say", ""))
        durations = self.beat_durations
        focus_plan = focus.scene_focus(self.spec)
        dimmed: set[str] = set()
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
            if target and target in by_id and target not in revealed:
                consumed = play_block(self, by_id[target], ground)
                revealed.add(target)
            if target in focus_plan:
                before = dimmed
                dimmed = focus.apply(self, by_id, focus_plan[target], dimmed)
                if dimmed != before:
                    consumed += focus.FADE_SECONDS
            # Each beat's video length should equal its narration clip; the reveal
            # animation already ran inside that window, so only hold the remainder.
            self.wait(max(target_seconds - consumed, MIN_HOLD))
        self.beat_seconds = None
        # Leave the scene un-focused: the final frame (what the visual gates read, and
        # what a viewer sits on through the tail) must match the un-focused render.
        focus.apply(self, by_id, [], dimmed)
        for block in blocks:
            if not block.static and block.id not in revealed:
                play_block(self, block, ground)

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
