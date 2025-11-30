from fastapi import APIRouter, HTTPException

from utils.logger import get_logger
from endpoints.document_upload_endpoint import DocumentUploadEndpoint
from endpoints.models.knowledge_base_info import KnowledgeBaseInfo

router = APIRouter()

log = get_logger("info_base_endpoint")

@router.get("/info", response_model=KnowledgeBaseInfo)
async def get_knowledge_base_info():
    try:
        upload_endpoint = DocumentUploadEndpoint()
        result = upload_endpoint.get_knowledge_base_info()

        return KnowledgeBaseInfo(**result)

    except Exception as e:
        log.error(f"Ошибка при получении информации о базе знаний: {e}")
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {str(e)}")