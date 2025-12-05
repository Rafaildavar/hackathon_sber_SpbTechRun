from pydantic import BaseModel
from typing import List, Optional

class KnowledgeBaseInfo(BaseModel):
    success: bool
    collection_name: Optional[str] = None
    documents_count: Optional[int] = None
    vectors_count: Optional[int] = None
    status: Optional[str] = None
    message: Optional[str] = None