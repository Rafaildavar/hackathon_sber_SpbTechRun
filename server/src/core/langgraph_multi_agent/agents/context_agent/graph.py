import asyncio
import json
from langgraph.graph import StateGraph, END
from langchain_core.messages import trim_messages, HumanMessage, AIMessage
from core.langgraph_multi_agent.agents.context_agent.state import ContextState
from core.services.LLMService import LLMService
from utils.logger import get_logger
from utils.prompt_loader import render_prompt

log = get_logger("ContextAgent")

class ContextAgent:
    def __init__(self):
        self.llm_service = LLMService()

    async def prepare_system_prompt(self, state: ContextState) -> ContextState:
        message = state["message"]
        history = state.get("history", [])

        log.info(f"Подготовка системного промпта")

        prompt = render_prompt("context_system_prompt",
                             message=message,
                             history=history)

        return {**state, "system_prompt": prompt}

    async def prepare_context(self, state: ContextState) -> ContextState:
        message = state["message"]
        history = state.get("history", [])
        api_data = state.get("api_data")
        web_search_results = state.get("web_search_results")
        rag_context = state.get("rag_context")
        has_user_documents = state.get("has_user_documents", False)
        user_documents = state.get("user_documents")

        log.info(f"Подготовка контекста для генерации ответа")

        api_data_str = json.dumps(api_data, ensure_ascii=False) if api_data else "Нет данных"
        web_search_str = json.dumps(web_search_results, ensure_ascii=False) if web_search_results else "Нет данных"
        rag_str = rag_context if rag_context else "Нет данных"
        user_docs_str = "Да" if has_user_documents and user_documents else "Нет"

        prompt = render_prompt("context_prepare_prompt",
                             message=message,
                             api_data=api_data_str,
                             web_search_results=web_search_str,
                             has_user_documents=user_docs_str,
                             history=history)

        context = await self.llm_service.fetch_completion(prompt)

        log.info(f"Контекст подготовлен")

        return {**state, "context": context}

    async def save_to_history(self, state: ContextState) -> ContextState:
        message = state["message"]
        history = state.get("history", [])

        log.info(f"Сохранение сообщения в историю (текущий размер: {len(history)})")

        new_history = history.copy()
        new_history.append({
            "role": "user",
            "content": message
        })

        langchain_messages = []
        for msg in new_history:
            if msg["role"] == "user":
                langchain_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                langchain_messages.append(AIMessage(content=msg["content"]))

        trimmed_messages = trim_messages(
            langchain_messages,
            max_tokens=4000,
            strategy="last",
            token_counter=len
        )

        trimmed_history = []
        for msg in trimmed_messages:
            if isinstance(msg, HumanMessage):
                trimmed_history.append({"role": "user", "content": msg.content})
            elif isinstance(msg, AIMessage):
                trimmed_history.append({"role": "assistant", "content": msg.content})

        log.info(f"История после trim: {len(trimmed_history)} сообщений")

        return {**state, "history": trimmed_history}

    async def update_tokens(self, state: ContextState) -> ContextState:
        total_tokens = self.llm_service.total_input_token + self.llm_service.total_output_token

        log.info(f"Всего токенов использовано: {total_tokens}")

        return {**state, "total_tokens": total_tokens}

    def build_graph(self):
        workflow = StateGraph(ContextState)

        workflow.add_node("prepare_system_prompt", self.prepare_system_prompt)
        workflow.add_node("prepare_context", self.prepare_context)
        workflow.add_node("save_to_history", self.save_to_history)
        workflow.add_node("update_tokens", self.update_tokens)

        workflow.set_entry_point("prepare_system_prompt")
        workflow.add_edge("prepare_system_prompt", "prepare_context")
        workflow.add_edge("prepare_context", "save_to_history")
        workflow.add_edge("save_to_history", "update_tokens")
        workflow.add_edge("update_tokens", END)

        return workflow.compile()

async def main():
    agent = ContextAgent()
    graph = agent.build_graph()

    test_state = {
        "message": "Где находится ближайший МФЦ?",
        "history": [],
        "api_data": {"mfc": "data"},
        "web_search_results": None,
        "rag_context": "Контекст из RAG",
        "has_user_documents": False,
        "user_documents": None,
        "system_prompt": None,
        "context": None,
        "total_tokens": 0
    }

    result = await graph.ainvoke(test_state)
    print(f"Системный промпт: {result['system_prompt']}")
    print(f"Контекст: {result['context']}")
    print(f"Всего токенов: {result['total_tokens']}")

if __name__ == "__main__":
    asyncio.run(main())