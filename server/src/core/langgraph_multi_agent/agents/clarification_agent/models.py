from pydantic import BaseModel, Field
from typing import List

class ClarificationCheck(BaseModel):
    needs_clarification: bool = Field(description="True если нужны уточнения для ответа")
    questions: List[str] = Field(description="Список вопросов для уточнения (если нужны)")
    reason: str = Field(description="Причина почему нужны или не нужны уточнения")