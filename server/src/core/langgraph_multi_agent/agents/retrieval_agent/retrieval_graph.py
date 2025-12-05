import asyncio
import json
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

# Маппинг имен функций на их реализации
FUNCTION_MAP = {
    "find_nearest_mfc": tools.find_nearest_mfc,
    "get_mfc_by_district": tools.get_mfc_by_district,
    "get_polyclinics_by_address": tools.get_polyclinics_by_address,
    "get_schools_by_district": tools.get_schools_by_district,
    "get_linked_schools": tools.get_linked_schools,
    "get_dou": tools.get_dou,
    "pensioner_service": tools.pensioner_service,
    "afisha_all": tools.afisha_all,
    "get_beautiful_places": tools.get_beautiful_places,
}

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

    async def get_rag_data(self, state: RetrievalState) -> RetrievalState:
        message = state["message"]
        requires_rag = state.get("requires_rag", False)

        if not requires_rag:
            log.info("RAG поиск не требуется")
            return {"rag_context": None}

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
                log.info(f"RAG ответ: {answer}")
                return {"rag_context": answer}
            else:
                log.error(f"Ошибка RAG endpoint: {response.status_code}")
                return {"rag_context": None}
        except Exception as e:
            log.error(f"Ошибка RAG поиска: {str(e)}")
            return {"rag_context": None}

    async def get_api_data(self, state: RetrievalState) -> RetrievalState:
        message = state["message"]
        requires_api = state.get("requires_api", False)

        if not requires_api:
            log.info("API поиск не требуется")
            return {"api_data": None}

        log.info(f"Выполнение API поиска с function calling")

        try:
            prompt = f"Пользователь запросил: {message}\n\nИспользуй доступные функции для получения информации из городских API Санкт-Петербурга."

            raw_response = await self.llm_service.fetch_completion_with_tools(
                prompt,
                {"tools": CITY_API_TOOLS, "tool_choice": "auto"}
            )

            log.info(f"Получен ответ от LLM с function calling")

            if not raw_response.choices[0].message.tool_calls:
                log.warning("LLM не вернул tool_calls")
                return {"api_data": {"error": "No tool calls returned"}}

            tool_calls = raw_response.choices[0].message.tool_calls
            results = []

            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                log.info(f"Вызов функции {function_name} с аргументами {function_args}")

                if function_name in FUNCTION_MAP:
                    function_to_call = FUNCTION_MAP[function_name]
                    try:
                        function_result = function_to_call(**function_args)
                        results.append({
                            "function": function_name,
                            "arguments": function_args,
                            "result": function_result
                        })
                        log.info(f"Результат {function_name}: успешно")
                        log.info(f"Данные: {function_result}")
                    except Exception as func_error:
                        log.error(f"Ошибка выполнения функции {function_name}: {str(func_error)}")
                        results.append({
                            "function": function_name,
                            "arguments": function_args,
                            "error": str(func_error)
                        })
                else:
                    log.error(f"Функция {function_name} не найдена в FUNCTION_MAP")
                    results.append({
                        "function": function_name,
                        "error": "Function not found"
                    })

            return {"api_data": {"tool_calls": results}}
        except Exception as e:
            log.error(f"Ошибка API поиска: {str(e)}")
            return {"api_data": None}

    async def get_web_data(self, state: RetrievalState) -> RetrievalState:
        message = state["message"]
        requires_web_search = state.get("requires_web_search", False)

        if not requires_web_search:
            log.info("Web search не требуется")
            return {"web_search_results": None}

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

            return {"web_search_results": results}
        except Exception as e:
            log.error(f"Ошибка web search через Tavily: {str(e)}")
            return {"web_search_results": None}

    async def retrieve_all_parallel(self, state: RetrievalState) -> RetrievalState:
        """
        Выполняет все три задачи параллельно: RAG, API, Web Search
        """
        log.info("Запуск параллельного поиска: RAG + API + Web")

        # Запускаем все три задачи параллельно
        rag_task = self.get_rag_data(state)
        api_task = self.get_api_data(state)
        web_task = self.get_web_data(state)

        # Ждем завершения всех задач
        results = await asyncio.gather(rag_task, api_task, web_task, return_exceptions=True)

        # Объединяем результаты - теперь каждая функция возвращает только свои поля
        final_state = {**state}
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                log.error(f"Ошибка при параллельном выполнении задачи {i}: {str(result)}")
                continue
            if isinstance(result, dict):
                # Теперь безопасно объединяем, так как каждая функция возвращает только свое поле
                final_state.update(result)

        log.info("Параллельный поиск завершен")
        log.info(f"Финальный state: rag_context={final_state.get('rag_context') is not None}, "
                 f"api_data={final_state.get('api_data') is not None}, "
                 f"web_search_results={final_state.get('web_search_results') is not None}")
        return final_state

    def build_graph(self):
        workflow = StateGraph(RetrievalState)

        # Добавляем одну ноду, которая выполняет все три задачи параллельно
        workflow.add_node("retrieve_all_parallel", self.retrieve_all_parallel)

        # Устанавливаем её как точку входа и выхода
        workflow.set_entry_point("retrieve_all_parallel")
        workflow.add_edge("retrieve_all_parallel", END)

        return workflow.compile()

async def main():
    agent = RetrievalAgent()
    graph = agent.build_graph()

    test_state = {
        "message": "Где находится ближайший МФЦ к Невскому проспекту 1?",
        "requires_rag": False,
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