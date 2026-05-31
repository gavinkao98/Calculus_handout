from __future__ import annotations

import os
import re
from pathlib import Path

from manim import *

try:
    from manim_voiceover import VoiceoverScene
except ModuleNotFoundError as exc:
    raise ModuleNotFoundError(
        "Missing manim_voiceover. Install it with: "
        'python -m pip install "manim-voiceover[gtts]"'
    ) from exc


BACKGROUND = "#0b0c10"
PRIMARY = "#e8e8f0"
TEXT = "#c8c8d8"
SECONDARY = "#4cc9f0"
ACCENT = "#f9a825"
GRID = "#2a2a3e"


def linear_word_boundaries(text: str, audio_seconds: float) -> list[dict]:
    from manim_voiceover.helper import remove_bookmarks
    from manim_voiceover.tracker import AUDIO_OFFSET_RESOLUTION

    clean_text = remove_bookmarks(text)
    text_length = max(len(clean_text), 1)
    boundaries = []
    for match in re.finditer(r"\S+", clean_text):
        start_ratio = match.start() / text_length
        boundaries.append(
            {
                "audio_offset": int(start_ratio * audio_seconds * AUDIO_OFFSET_RESOLUTION),
                "text_offset": match.start(),
                "word_length": len(match.group(0)),
                "text": match.group(0),
                "boundary_type": "Word",
            }
        )

    if not boundaries:
        boundaries.append(
            {
                "audio_offset": 0,
                "text_offset": 0,
                "word_length": text_length,
                "text": clean_text,
                "boundary_type": "Word",
            }
        )
    boundaries.append(
        {
            "audio_offset": int(audio_seconds * AUDIO_OFFSET_RESOLUTION),
            "text_offset": len(clean_text),
            "word_length": 1,
            "text": ".",
            "boundary_type": "Word",
        }
    )
    return boundaries


def add_linear_boundaries(data: dict, cache_dir: str | Path, text: str) -> dict:
    from manim_voiceover.modify_audio import get_duration

    audio_path = Path(cache_dir) / data["original_audio"]
    data["word_boundaries"] = linear_word_boundaries(text, get_duration(audio_path))
    return data


def build_speech_service():
    service_name = os.environ.get("MANIM_VOICEOVER_SERVICE", "gtts_linear").strip().lower()
    transcription_model = os.environ.get("MANIM_VOICEOVER_TRANSCRIPTION_MODEL", "").strip()
    transcription_kwargs = {}
    if transcription_model:
        transcription_kwargs["transcription_model"] = transcription_model

    if service_name in {"gtts", "gtts_linear", "linear_gtts"}:
        from manim_voiceover.services.gtts import GTTSService

        class LinearBoundaryGTTSService(GTTSService):
            def generate_from_text(self, text: str, cache_dir: str = None, path: str = None, **kwargs):
                data = super().generate_from_text(text, cache_dir=cache_dir, path=path, **kwargs)
                return add_linear_boundaries(data, cache_dir or self.cache_dir, text)

        service_class = LinearBoundaryGTTSService if service_name != "gtts" else GTTSService
        return service_class(lang=os.environ.get("MANIM_VOICEOVER_LANG", "en"), **transcription_kwargs)

    if service_name in {"gtts_transcribe", "gtts_whisper"}:
        from manim_voiceover.services.gtts import GTTSService

        transcription_kwargs.setdefault("transcription_model", "base")
        return GTTSService(lang=os.environ.get("MANIM_VOICEOVER_LANG", "en"), **transcription_kwargs)

    if service_name in {"coqui", "coqui_jenny", "jenny"}:
        from manim_voiceover.services.coqui import CoquiService

        return CoquiService(
            model_name=os.environ.get(
                "MANIM_VOICEOVER_COQUI_MODEL",
                "tts_models/en/jenny/jenny",
            ),
            **transcription_kwargs,
        )

    raise ValueError(
        "Unsupported MANIM_VOICEOVER_SERVICE. Use 'gtts_linear', 'gtts_transcribe', or 'coqui_jenny'."
    )


class ManimVoiceoverExperiment(VoiceoverScene):
    def construct(self) -> None:
        self.camera.background_color = BACKGROUND
        self.set_speech_service(build_speech_service())

        title = Tex(
            r"\textbf{Manim Voiceover timing test}",
            color=PRIMARY,
            font_size=42,
        ).to_edge(UP, buff=0.45)

        subtitle = Tex(
            r"duration control, then bookmark control",
            color=TEXT,
            font_size=26,
        ).next_to(title, DOWN, buff=0.18)

        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 4, 1],
            x_length=5.2,
            y_length=4.0,
            axis_config={"color": GRID, "stroke_width": 1.5},
            tips=True,
        ).shift(DOWN * 0.35)

        graph = axes.plot(lambda x: x**2, x_range=[0, 2], color=SECONDARY)
        inverse = axes.plot(lambda x: x**0.5, x_range=[0, 4], color=ACCENT)
        diagonal = axes.plot(lambda x: x, x_range=[0, 4], color=TEXT)

        f_label = MathTex(r"f(x)=x^2,\ x\ge 0", color=SECONDARY, font_size=34)
        f_label.next_to(axes, RIGHT, buff=0.35).shift(UP * 0.65)
        inv_label = MathTex(r"f^{-1}(x)=\sqrt{x}", color=ACCENT, font_size=34)
        inv_label.next_to(f_label, DOWN, buff=0.3)

        note = Tex(
            r"\parbox{8.5cm}{The second block uses bookmarks, so the animation waits for named points in the narration.}",
            color=TEXT,
            font_size=24,
        ).to_edge(DOWN, buff=0.45)

        with self.voiceover(
            text=(
                "This first sentence uses the total voiceover duration. "
                "The title and coordinate system finish while the narration is still running."
            )
        ) as tracker:
            self.play(FadeIn(title, shift=0.12 * DOWN), run_time=0.7)
            self.play(FadeIn(subtitle), Create(axes), run_time=max(tracker.duration - 0.7, 0.8))

        with self.voiceover(
            text=(
                "Now the function y equals x squared appears on the nonnegative half-line. "
                "The animation length is tied to the measured audio length."
            )
        ) as tracker:
            self.play(Create(graph), Write(f_label), run_time=max(tracker.duration * 0.7, 1.2))

        with self.voiceover(
            text=(
                "The inverse is built by swapping input and output. "
                "<bookmark mark='mirror'/> The mirror line y equals x appears first. "
                "<bookmark mark='inverse'/> Then the inverse curve appears across that mirror line. "
                "<bookmark mark='label'/> Finally, we label the inverse function."
            )
        ):
            self.wait_until_bookmark("mirror")
            self.play(Create(diagonal), run_time=0.55)
            self.wait_until_bookmark("inverse")
            self.play(TransformFromCopy(graph, inverse), run_time=0.9)
            self.wait_until_bookmark("label")
            self.play(Write(inv_label), FadeIn(note), run_time=0.65)

        self.wait(0.6)
