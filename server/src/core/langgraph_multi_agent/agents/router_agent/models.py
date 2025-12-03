from pydantic import BaseModel, Field

class RouteClassification(BaseModel):
    requires_api: bool = Field(description="True если нужно обратиться к городским API (МФЦ, поликлиники, школы, детсады, афиша, места)")
    requires_web_search: bool = Field(description="True если нужна актуальная информация из интернета")
    is_clear: bool = Field(description="True если запрос понятен и можно дать ответ, False если нужны уточнения")
    reasoning: str = Field(description="Краткое объяснение принятого решения")