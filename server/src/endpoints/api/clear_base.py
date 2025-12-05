from fastapi import APIRouter, HTTPException

from endpoints.document_upload_endpoint import DocumentUploadEndpoint
from endpoints.models.upload_response import UploadResponse

from utils.logger import get_logger

router = APIRouter()

log = get_logger("clear_base_endpoint")

@router.delete("/clear", response_model=UploadResponse)
async def clear_knowledge_base():
    try:
        upload_endpoint = DocumentUploadEndpoint()
        result = upload_endpoint.clear_knowledge_base()

        return UploadResponse(**result)

    except Exception as e:
        log.error(f"Ошибка при очистке базы знаний: {e}")
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {str(e)}")

