import os
from functools import lru_cache
from typing import Dict, Any

import jinja2
import yaml


@lru_cache(maxsize=1)
def load_prompts() -> Dict[str, str]:
    prompts_path = os.path.join(os.path.dirname(__file__), "../prompts.yml")
    langgraph_prompts_path = os.path.join(os.path.dirname(__file__), "../core/langgraph_multi_agent/prompts.yml")

    all_prompts = {}

    if os.path.exists(prompts_path):
        with open(prompts_path, "r", encoding="utf-8") as f:
            prompts = yaml.safe_load(f)
            if prompts:
                all_prompts.update(prompts)

    if os.path.exists(langgraph_prompts_path):
        with open(langgraph_prompts_path, "r", encoding="utf-8") as f:
            prompts = yaml.safe_load(f)
            if prompts:
                all_prompts.update(prompts)

    return all_prompts


def render_prompt(prompt_name: str, **kwargs: Any) -> str:
    prompts = load_prompts()
    template = jinja2.Template(prompts[prompt_name])
    return template.render(**kwargs)