from typing import TypedDict, List, Optional

class ContextState(TypedDict):
    message: str
    history: List[dict]
    api_data: Optional[dict]
    web_search_results: Optional[List[dict]]
    rag_context: Optional[str]
    has_user_documents: bool
    user_documents: Optional[List[dict]]
    system_prompt: Optional[str]
    context: Optional[str]
    total_tokens: int