from fastapi import APIRouter

from utils.logger import get_logger
from endpoints.rag_answer_endpoint import RagAnswerEndpoint

router = APIRouter()

log = get_logger("rag_answer_endpoint")

@router.get("/get_answer")
async def get_answer(user_question: str):
    rag_answer_endpoint = RagAnswerEndpoint()
    answer = await rag_answer_endpoint.get_answer(user_question)
    return {
        "answer": answer
    }