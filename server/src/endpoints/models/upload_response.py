from pydantic import BaseModel
from typing import List, Optional

class UploadResponse(BaseModel):
    success: bool
    message: str
    chunks_count: Optional[int] = None
    files_processed: Optional[int] = None
    total_files: Optional[int] = None
    details: Optional[List[dict]] = None