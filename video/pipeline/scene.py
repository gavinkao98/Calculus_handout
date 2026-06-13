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

from .blocks import play_block
from .narration import estimate_seconds, parse_say
from .templates import build_blocks
from .visuals import theme as T

LIGHT_KINDS = {"intro", "outro"}
MIN_HOLD = 0.3  # floor so a long reveal animation never yields a negative wait


class LessonScene(Scene):
    spec: dict[str, Any] | None = None
    meta: dict[str, Any] | None = None
    beat_durations: list[float] | None = None  # per-beat narration seconds, in say order

    def construct(self) -> None:
        if self.spec is None:
            raise RuntimeError("LessonScene was not configured (spec missing).")

        kind = self.spec.get("kind", "content")
        ground = "light" if kind in LIGHT_KINDS else "dark"
        self.camera.background_color = T.color(ground, "bg")

        ctx = {"ground": ground, "meta": self.meta or {}}
        blocks = build_blocks(self.spec, ctx)
        by_id = {b.id: b for b in blocks}

        for block in blocks:
            if block.static:
                self.add(block.mobject)

        self.wait(0.3)

        if kind == "content":
            self._play_content(blocks, by_id, ground)
        elif kind == "intro":
            self._play_intro(blocks, ground, float(self.spec.get("duration", 6.0)))
        elif kind == "outro":
            self._play_outro(blocks, ground, float(self.spec.get("duration", 8.0)))
        else:
            self._play_timed(blocks, ground, float(self.spec.get("duration", 3.0)))

        self.wait(0.6)

    def _play_content(self, blocks, by_id, ground) -> None:
        revealed: set[str] = set()
        beats = parse_say(self.spec.get("say", ""))
        durations = self.beat_durations
        for index, beat in enumerate(beats):
            target = beat.reveal
            consumed = 0.0
            if target and target in by_id and target not in revealed:
                consumed = play_block(self, by_id[target], ground)
                revealed.add(target)
            if durations is not None and index < len(durations):
                target_seconds = durations[index]
            else:
                target_seconds = estimate_seconds(beat.text)
            # Each beat's video length should equal its narration clip; the reveal
            # animation already ran inside that window, so only hold the remainder.
            self.wait(max(target_seconds - consumed, MIN_HOLD))
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
