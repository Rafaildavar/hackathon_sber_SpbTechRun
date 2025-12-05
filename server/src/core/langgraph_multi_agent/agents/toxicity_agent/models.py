from pydantic import BaseModel, Field

class ToxicityCheckResult(BaseModel):
    is_toxic: bool = Field(description="True если сообщение токсичное, False если нет")