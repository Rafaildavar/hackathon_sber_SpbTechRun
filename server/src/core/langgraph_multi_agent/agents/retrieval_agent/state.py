from typing import TypedDict, List, Optional

class RetrievalState(TypedDict):
    message: str
    requires_rag: bool
    requires_api: bool
    requires_web_search: bool
    history: List[dict]
    api_data: Optional[dict]
    web_search_results: Optional[List[dict]]
    rag_context: Optional[str]