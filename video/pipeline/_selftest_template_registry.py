"""Parity guard: templates REGISTRY (manim env) == pipeline/template_names.py.
Run (render/manim env): python video/pipeline/_selftest_template_registry.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline.template_names import CONTENT_TEMPLATES  # noqa: E402


def test_registry_matches_template_names():
    from pipeline.templates import REGISTRY
    content = set(REGISTRY) - {"intro", "outro", "divider"}
    assert content == set(CONTENT_TEMPLATES), (
        f"registry={sorted(content)} != template_names={sorted(CONTENT_TEMPLATES)}")


if __name__ == "__main__":
    test_registry_matches_template_names()
    print("[selftest] template registry parity green")
