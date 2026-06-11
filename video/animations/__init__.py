"""Custom hook-animation factories, one module per section deck.

A factory is wired by a scene's `hook: "animations.<module>:<fn>"` field and
receives (spec, ctx, template_blocks) -- see pipeline/templates/__init__.py
(_apply_hook) for the contract and pipeline/blocks.py for callable anims.
"""
