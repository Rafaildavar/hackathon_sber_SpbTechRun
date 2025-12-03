import asyncio
import requests
from typing import List, Dict
from tavily import TavilyClient
from langgraph.graph import StateGraph, END
from core.langgraph_multi_agent.agents.retrieval_agent.state import RetrievalState
from core.langgraph_multi_agent.agents.retrieval_agent import tools
from core.services.LLMService import LLMService
from config.Config import CONFIG
from utils.logger import get_logger

log = get_logger("RetrievalAgent")

CITY_API_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "find_nearest_mfc",
            "description": "Найти ближайший МФЦ по адресу пользователя",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_address": {"type": "string", "description": "Адрес пользователя в Санкт-Петербурге"}
                },
                "required": ["user_address"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_mfc_by_district",
            "description": "Получить список МФЦ по названию района",
            "parameters": {
                "type": "object",
                "properties": {
                    "district": {"type": "string", "description": "Название района Санкт-Петербурга"}
                },
                "required": ["district"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_polyclinics_by_address",
            "description": "Найти поликлиники по адресу пользователя",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_address": {"type": "string", "description": "Адрес пользователя в Санкт-Петербурге"}
                },
                "required": ["user_address"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_schools_by_district",
            "description": "Получить список школ по названию района",
            "parameters": {
                "type": "object",
                "properties": {
                    "district": {"type": "string", "description": "Название района Санкт-Петербурга"}
                },
                "required": ["district"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_linked_schools",
            "description": "Найти школы привязанные к адресу",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_address": {"type": "string", "description": "Адрес в Санкт-Петербурге"}
                },
                "required": ["user_address"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_dou",
            "description": "Получить детские сады по фильтрам",
            "parameters": {
                "type": "object",
                "properties": {
                    "district": {"type": "string", "description": "Название района"},
                    "age_year": {"type": "integer", "description": "Возраст ребенка в годах"},
                    "age_month": {"type": "integer", "description": "Возраст ребенка в месяцах"}
                },
                "required": ["district"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "pensioner_service",
            "description": "Получить услуги для пенсионеров по району и категории",
            "parameters": {
                "type": "object",
                "properties": {
                    "district": {"type": "string", "description": "Название района"},
                    "category": {"type": "string", "description": "Категория услуг"}
                },
                "required": ["district"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "afisha_all",
            "description": "Получить список событий из афиши по датам",
            "parameters": {
                "type": "object",
                "properties": {
                    "start_date": {"type": "string", "description": "Дата начала в формате 2025-11-21T00:00:00"},
                    "end_date": {"type": "string", "description": "Дата окончания в формате 2025-12-22T00:00:00"},
                    "categoria": {"type": "string", "description": "Категория события"},
                    "kids": {"type": "boolean", "description": "Для детей"},
                    "free": {"type": "boolean", "description": "Бесплатные"}
                },
                "required": ["start_date", "end_date"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_beautiful_places",
            "description": "Получить список красивых мест по фильтрам",
            "parameters": {
                "type": "object",
                "properties": {
                    "area": {"type": "string", "description": "Область"},
                    "categoria": {"type": "string", "description": "Категория"},
                    "district": {"type": "string", "description": "Район"}
                }
            }
        }
    }
]

class RetrievalAgent:
    def __init__(self):
        self.llm_service = LLMService()
        self.rag_endpoint_url = CONFIG.rag.endpoint_url
        self.tavily_client = TavilyClient(api_key=CONFIG.tavily.api_key)

    async def rag_search(self, state: RetrievalState) -> RetrievalState:
        message = state["message"]
        log.info(f"Выполнение RAG поиска")

        try:
            response = requests.get(
                self.rag_endpoint_url,
                params={"user_question": message},
                timeout=30
            )
            if response.status_code == 200:
                answer = response.json().get("answer", "")
                log.info(f"RAG ответ получен")
                return {**state, "rag_context": answer}
            else:
                log.error(f"Ошибка RAG endpoint: {response.status_code}")
                return {**state, "rag_context": None}
        except Exception as e:
            log.error(f"Ошибка RAG поиска: {str(e)}")
            return {**state, "rag_context": None}

    async def api_search(self, state: RetrievalState) -> RetrievalState:
        message = state["message"]
        requires_api = state.get("requires_api", False)

        if not requires_api:
            log.info("API поиск не требуется")
            return {**state, "api_data": None}

        log.info(f"Выполнение API поиска с function calling")

        try:
            prompt = f"Пользователь запросил: {message}\n\nИспользуй доступные функции для получения информации из городских API Санкт-Петербурга."

            response = await self.llm_service.fetch_completion(
                prompt,
                {"tools": CITY_API_TOOLS, "tool_choice": "auto"}
            )

            log.info(f"Получен ответ от LLM с function calling")

            return {**state, "api_data": {"response": response}}
        except Exception as e:
            log.error(f"Ошибка API поиска: {str(e)}")
            return {**state, "api_data": None}

    async def web_search(self, state: RetrievalState) -> RetrievalState:
        message = state["message"]
        requires_web_search = state.get("requires_web_search", False)

        if not requires_web_search:
            log.info("Web search не требуется")
            return {**state, "web_search_results": None}

        log.info(f"Выполнение web search через Tavily")

        try:
            response = self.tavily_client.search(
                query=message,
                max_results=CONFIG.tavily.max_results,
                search_depth=CONFIG.tavily.search_depth,
                include_raw_content=CONFIG.tavily.include_raw_content
            )

            results = []
            for result in response.get("results", []):
                results.append({
                    "title": result.get("title"),
                    "url": result.get("url"),
                    "content": result.get("content"),
                    "score": result.get("score")
                })

            log.info(f"Найдено {len(results)} результатов через Tavily")

            return {**state, "web_search_results": results}
        except Exception as e:
            log.error(f"Ошибка web search через Tavily: {str(e)}")
            return {**state, "web_search_results": None}

    def build_graph(self):
        workflow = StateGraph(RetrievalState)

        workflow.add_node("rag_search", self.rag_search)
        workflow.add_node("api_search", self.api_search)
        workflow.add_node("web_search", self.web_search)

        workflow.set_entry_point("rag_search")
        workflow.add_edge("rag_search", "api_search")
        workflow.add_edge("api_search", "web_search")
        workflow.add_edge("web_search", END)

        return workflow.compile()

async def main():
    agent = RetrievalAgent()
    graph = agent.build_graph()

    test_state = {
        "message": "Где находится ближайший МФЦ к Невскому проспекту 1?",
        "requires_api": True,
        "requires_web_search": False,
        "history": [],
        "api_data": None,
        "web_search_results": None,
        "rag_context": None
    }

    result = await graph.ainvoke(test_state)
    print(f"Результат: {result}")

if __name__ == "__main__":
    asyncio.run(main())