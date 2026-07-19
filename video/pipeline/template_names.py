"""Manim-free single source for the content-template name set.

tts.py must stay importable in the TTS env (no manim), so it cannot read
pipeline/templates/__init__.py's REGISTRY (blocks.py imports manim at module
top). Both sides use THIS tuple; _selftest_template_registry.py (manim env)
asserts the REGISTRY still matches it, so the two can't drift apart again."""
CONTENT_TEMPLATES: tuple[str, ...] = (
    "callout", "definition_math", "derivation", "graph", "procedure_steps",
    "recap_cards", "sign_chart", "theorem_proof", "value_table",
)
