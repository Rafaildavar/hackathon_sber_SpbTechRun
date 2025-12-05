import asyncio
from langgraph.graph import StateGraph, END
from core.langgraph_multi_agent.agents.conversational_agent.state import ConversationalState
from core.services.LLMService import LLMService
from utils.logger import get_logger
from utils.prompt_loader import render_prompt

log = get_logger("ConversationalAgent")

class ConversationalAgent:
    def __init__(self):
        self.llm_service = LLMService()

    async def generate_response(self, state: ConversationalState) -> ConversationalState:
        message = state["message"]
        context = state.get("context", "")

        log.info(f"Генерация финального ответа")

        prompt = render_prompt("conversational_prompt",
                             context=context,
                             message=message)

        response = await self.llm_service.fetch_completion(prompt)

        log.info(f"Ответ сгенерирован")

        return {**state, "response": response}

    async def save_response_to_history(self, state: ConversationalState) -> ConversationalState:
        response = state.get("response")
        history = state.get("history", [])

        if not response:
            log.warning("Нет ответа для сохранения в историю")
            return state

        log.info(f"Сохранение ответа в историю (текущий размер: {len(history)})")

        new_history = history.copy()
        new_history.append({
            "role": "assistant",
            "content": response
        })

        log.info(f"История после добавления ответа: {len(new_history)} сообщений")

        return {**state, "history": new_history}

    def build_graph(self):
        workflow = StateGraph(ConversationalState)

        workflow.add_node("generate_response", self.generate_response)
        workflow.add_node("save_response_to_history", self.save_response_to_history)

        workflow.set_entry_point("generate_response")
        workflow.add_edge("generate_response", "save_response_to_history")
        workflow.add_edge("save_response_to_history", END)

        return workflow.compile()

async def main():
    agent = ConversationalAgent()
    graph = agent.build_graph()

    test_state = {
        "message": "Где находится ближайший МФЦ?",
        "context": "По данным из API, ближайший МФЦ находится по адресу...",
        "history": [
            {"role": "user", "content": "Где находится ближайший МФЦ?"}
        ],
        "response": None
    }

    result = await graph.ainvoke(test_state)
    print(f"Ответ: {result['response']}")

if __name__ == "__main__":
    asyncio.run(main())