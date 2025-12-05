from typing import TypedDict, List, Optional

class ParserState(TypedDict):
    message: str
    classification: str
    history: List[dict]
    user_documents: Optional[List[dict]]
    has_user_documents: bool
    uploaded_files: Optional[List[dict]]