import asyncio
from langgraph.graph import StateGraph, END
from core.langgraph_multi_agent.agents.router_agent.state import RouterState
from core.langgraph_multi_agent.agents.router_agent.models import RouteClassification
from core.services.LLMService import LLMService
from utils.logger import get_logger
from utils.prompt_loader import render_prompt

log = get_logger("RouterAgent")

class RouterAgent:
    def __init__(self):
        self.llm_service = LLMService()

    async def classify_route(self, state: RouterState) -> RouterState:
        message = state["message"]
        classification = state.get("classification", "")
        history = state.get("history", [])

        log.info(f"Классификация маршрута для сообщения")

        prompt = render_prompt("router_classify_prompt",
                             message=message,
                             classification=classification,
                             history=history)

        response = await self.llm_service.fetch_structured_completion(prompt, RouteClassification)

        log.info(f"Маршрутизация: RAG={response.requires_rag}, API={response.requires_api}, Web={response.requires_web_search}, Clear={response.is_clear}")
        log.info(f"Reasoning: {response.reasoning}")

        return {
            **state,
            "requires_rag": response.requires_rag,
            "requires_api": response.requires_api,
            "requires_web_search": response.requires_web_search,
            "is_clear": response.is_clear
        }

    def build_graph(self):
        workflow = StateGraph(RouterState)

        workflow.add_node("classify_route", self.classify_route)

        workflow.set_entry_point("classify_route")
        workflow.add_edge("classify_route", END)

        return workflow.compile()

async def main():
    agent = RouterAgent()
    graph = agent.build_graph()

    test_messages = [
        "Где находится ближайший МФЦ к Невскому проспекту 1?",
        "Какая сейчас погода в Петербурге?",
        "Расскажи о процедуре получения паспорта",
    ]

    for msg in test_messages:
        test_state = {
            "message": msg,
            "classification": "",
            "history": [],
            "requires_rag": False,
            "requires_api": False,
            "requires_web_search": False,
            "is_clear": False
        }

        result = await graph.ainvoke(test_state)
        print(f"Сообщение: {msg}")
        print(f"RAG: {result['requires_rag']}, API: {result['requires_api']}, Web: {result['requires_web_search']}, Clear: {result['is_clear']}\n")

if __name__ == "__main__":
    asyncio.run(main())