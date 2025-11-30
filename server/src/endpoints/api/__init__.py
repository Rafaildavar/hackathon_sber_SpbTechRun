from fastapi import APIRouter
from endpoints.api.clear_base import router as clear_base_router
from endpoints.api.health import router as health_router
from endpoints.api.info_base import router as info_base_router
from endpoints.api.rag_answer import router as rag_answer_router


main_router = APIRouter()

main_router.include_router(clear_base_router)
main_router.include_router(health_router)
main_router.include_router(info_base_router)
main_router.include_router(rag_answer_router)