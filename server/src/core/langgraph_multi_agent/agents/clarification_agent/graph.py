import asyncio
from langgraph.graph import StateGraph, END
from core.langgraph_multi_agent.agents.clarification_agent.state import ClarificationState
from core.langgraph_multi_agent.agents.clarification_agent.models import ClarificationCheck
from core.services.LLMService import LLMService
from utils.logger import get_logger
from utils.prompt_loader import render_prompt

log = get_logger("ClarificationAgent")

class ClarificationAgent:
    def __init__(self):
        self.llm_service = LLMService()

    async def check_clarification(self, state: ClarificationState) -> ClarificationState:
        message = state["message"]
        history = state.get("history", [])
        requires_web_search = state.get("requires_web_search", False)
        is_clear = state.get("is_clear", True)

        if is_clear:
            log.info("Запрос ясен, уточнения не требуются")
            return {**state, "in_clarification_mode": False, "clarification_questions": None}

        log.info(f"Проверка необходимости уточнения")

        prompt = render_prompt("clarification_check_prompt",
                             message=message,
                             history=history,
                             requires_web_search=requires_web_search)

        response = await self.llm_service.fetch_structured_completion(prompt, ClarificationCheck)

        log.info(f"Нужны уточнения: {response.needs_clarification}")

        if response.needs_clarification:
            log.info(f"Вопросы для уточнения: {response.questions}")

        return {
            **state,
            "in_clarification_mode": response.needs_clarification,
            "clarification_questions": response.questions if response.needs_clarification else None
        }

    def build_graph(self):
        workflow = StateGraph(ClarificationState)

        workflow.add_node("check_clarification", self.check_clarification)

        workflow.set_entry_point("check_clarification")
        workflow.add_edge("check_clarification", END)

        return workflow.compile()

async def main():
    agent = ClarificationAgent()
    graph = agent.build_graph()

    test_cases = [
        {
            "message": "Где МФЦ?",
            "history": [],
            "requires_web_search": False,
            "is_clear": False,
            "in_clarification_mode": False,
            "clarification_questions": None
        },
        {
            "message": "Где находится МФЦ на Невском проспекте 1?",
            "history": [],
            "requires_web_search": False,
            "is_clear": True,
            "in_clarification_mode": False,
            "clarification_questions": None
        }
    ]

    for test_state in test_cases:
        result = await graph.ainvoke(test_state)
        print(f"Сообщение: {test_state['message']}")
        print(f"Режим уточнения: {result['in_clarification_mode']}")
        print(f"Вопросы: {result['clarification_questions']}\n")

if __name__ == "__main__":
    asyncio.run(main())