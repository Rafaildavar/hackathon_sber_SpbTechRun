from typing import TypedDict, List, Optional

class UrbanAdvisorState(TypedDict):
    message: str
    is_toxic: bool
    classification: str
    history: List[dict]
    user_documents: Optional[List[dict]]
    has_user_documents: bool
    uploaded_files: Optional[List[dict]]
    requires_rag: bool
    requires_api: bool
    requires_web_search: bool
    is_clear: bool
    api_data: Optional[dict]
    web_search_results: Optional[List[dict]]
    rag_context: Optional[str]
    in_clarification_mode: bool
    clarification_questions: Optional[List[str]]
    system_prompt: Optional[str]
    context: Optional[str]
    total_tokens: int
    response: Optional[str]