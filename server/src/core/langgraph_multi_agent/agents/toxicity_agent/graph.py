import asyncio
from langgraph.graph import StateGraph, END

from core.langgraph_multi_agent.agents.toxicity_agent.state import ToxicityState
from core.langgraph_multi_agent.agents.toxicity_agent.models import ToxicityCheckResult
from config.Config import CONFIG
from core.services.LLMService import LLMService
from utils.logger import get_logger
from utils.prompt_loader import render_prompt


log = get_logger("ToxicityAgent")


class ToxicityAgent:
    def __init__(self):
        self.llm_service = LLMService()

    async def check_toxicity(self, state: ToxicityState) -> ToxicityState:
        message = state["message"]
        log.info(f"Проверка токсичности сообщения: {message}")

        prompt = render_prompt("toxicity_check_prompt", message=message)

        response: ToxicityCheckResult = await self.llm_service.fetch_structured_completion(
            prompt, ToxicityCheckResult
        )

        toxicity_status = "токсичное" if response.is_toxic else "чистое"
        log.info(f"Результат проверки токсичности: {toxicity_status} — {response.reason}")

        return {
            "message": message,
            "is_toxic": response.is_toxic
        }

    def build_graph(self):
        workflow = StateGraph(ToxicityState)

        workflow.add_node("check_toxicity", self.check_toxicity)
        workflow.set_entry_point("check_toxicity")
        workflow.add_edge("check_toxicity", END)

        return workflow.compile()


async def main():
    agent = ToxicityAgent()
    graph = agent.build_graph()

    test_messages = [
        "Здравствуйте, подскажите, где находится ближайший МФЦ?",
        "Ты тупой болван.",
    ]

    for msg in test_messages:
        result = await graph.ainvoke({"message": msg, "is_toxic": False})
        print(f"Сообщение: {msg}")
        print(f"Токсичность: {result['is_toxic']}\n")


if __name__ == "__main__":
    asyncio.run(main())