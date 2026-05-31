from __future__ import annotations

from importlib import import_module
from typing import Any, Callable

from . import templates


TemplateRenderer = Callable[[Any, dict[str, Any], dict[str, Any]], None]


TEMPLATE_REGISTRY: dict[str, TemplateRenderer] = {
    "title_bullets": templates.render_title_bullets,
    "definition_math": templates.render_definition_math,
    "example_walkthrough": templates.render_example_walkthrough,
    "graph_focus": templates.render_graph_focus,
    "procedure_steps": templates.render_procedure_steps,
    "recap_cards": templates.render_recap_cards,
    "section_transition": templates.render_section_transition,
    "theorem_proof": templates.render_theorem_proof,
    "comparison": templates.render_comparison,
}


def render_scene_template(scene, scene_spec: dict[str, Any], context: dict[str, Any]) -> None:
    renderer = TEMPLATE_REGISTRY[scene_spec["template"]]
    renderer(scene, scene_spec, context)

    hook_path = scene_spec.get("hook")
    if hook_path:
        resolve_hook(hook_path)(scene, scene_spec, context)


def resolve_hook(import_path: str) -> Callable[[Any, dict[str, Any], dict[str, Any]], None]:
    module_name, _, attribute_name = import_path.rpartition(".")
    if not module_name or not attribute_name:
        raise ValueError(f"Invalid hook path '{import_path}'. Expected '<module>.<callable>'.")

    try:
        module = import_module(module_name)
    except ModuleNotFoundError:
        if module_name.startswith("tools."):
            module = import_module(module_name.removeprefix("tools."))
        else:
            raise
    hook = getattr(module, attribute_name, None)
    if hook is None or not callable(hook):
        raise ValueError(f"Hook '{import_path}' could not be imported as a callable.")
    return hook
