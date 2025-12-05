from typing import TypedDict, List, Optional

class ConversationalState(TypedDict):
    message: str
    context: Optional[str]
    history: List[dict]
    response: Optional[str]