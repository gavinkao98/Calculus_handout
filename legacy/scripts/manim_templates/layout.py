"""Centralised layout manager for storyboard scenes.

Provides a ``SceneLayout`` that maps Manim coordinate space into
named zones (header, primary, support, progress) so that individual
templates can position content without hard-coding magic numbers.
"""

from __future__ import annotations

from typing import Any

from manim import LEFT, RIGHT, UP, DOWN, Mobject


class SceneLayout:
    """Manages the vertical-flow layout zones for a 16:9 Manim scene."""

    def __init__(self, theme: dict[str, Any]) -> None:
        layout = theme["layout"]
        self.margin = float(layout["side_margin"])
        self.content_width = float(layout["content_width"])

        # Zone boundaries (Manim y-coordinates, centre = 0)
        self.header_top = 3.5
        self.header_bottom = 2.5
        self.primary_top = 2.3
        self.primary_bottom = -1.5
        self.support_top = -1.7
        self.support_bottom = -3.5
        self.progress_y = -3.65

        # Horizontal edges for alignment
        self.left_edge = -self.content_width / 2
        self.right_edge = self.content_width / 2

    # -- placement helpers ------------------------------------------------

    def place_title(self, mob: Mobject) -> Mobject:
        """Position *mob* in the header zone, left-aligned."""
        mob.to_edge(UP, buff=0.35)
        mob.align_to([self.left_edge, 0, 0], LEFT)
        return mob

    def place_badge(self, badge: Mobject, title: Mobject) -> Mobject:
        """Position a type badge to the right of the title."""
        badge.next_to(title, RIGHT, buff=0.35)
        badge.align_to(title, DOWN)
        return badge

    def place_primary(self, mob: Mobject, reference: Mobject, *, buff: float = 0.5) -> Mobject:
        """Position primary content below *reference*, left-aligned."""
        mob.next_to(reference, DOWN, buff=buff)
        mob.align_to([self.left_edge, 0, 0], LEFT)
        return mob

    def place_primary_centered(self, mob: Mobject, reference: Mobject, *, buff: float = 0.5) -> Mobject:
        """Position primary content below *reference*, horizontally centred."""
        mob.next_to(reference, DOWN, buff=buff)
        return mob

    def place_math_below(self, mob: Mobject, reference: Mobject, *, buff: float = 0.45) -> Mobject:
        """Position a math block centred below *reference*."""
        mob.next_to(reference, DOWN, buff=buff)
        return mob

    def place_support(self, mob: Mobject, reference: Mobject, *, buff: float = 0.4) -> Mobject:
        """Position supporting content below *reference*, left-aligned."""
        mob.next_to(reference, DOWN, buff=buff)
        mob.align_to([self.left_edge, 0, 0], LEFT)
        return mob

    def place_progress(self, mob: Mobject) -> Mobject:
        """Position progress dots at the bottom-right corner."""
        mob.move_to([self.right_edge - 0.6, self.progress_y, 0])
        return mob

    # -- queries -----------------------------------------------------------

    def primary_height(self) -> float:
        return self.primary_top - self.primary_bottom

    def support_height(self) -> float:
        return self.support_top - self.support_bottom

    def usable_width(self) -> float:
        return self.content_width
