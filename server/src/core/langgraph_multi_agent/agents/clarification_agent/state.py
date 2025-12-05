from typing import TypedDict, List, Optional

class ClarificationState(TypedDict):
    message: str
    history: List[dict]
    requires_web_search: bool
    is_clear: bool
    in_clarification_mode: bool
    clarification_questions: Optional[List[str]]