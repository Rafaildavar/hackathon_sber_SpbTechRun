from typing import TypedDict, List

class RouterState(TypedDict):
    message: str
    classification: str
    history: List[dict]
    requires_api: bool
    requires_web_search: bool
    is_clear: bool