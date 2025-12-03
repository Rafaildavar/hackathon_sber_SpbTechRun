import asyncio
import os
from pathlib import Path
from langgraph.graph import StateGraph, END
from core.langgraph_multi_agent.state import UrbanAdvisorState
from core.langgraph_multi_agent.agents.toxicity_agent import ToxicityAgent
from core.langgraph_multi_agent.agents.parser_agent import ParserAgent
from core.langgraph_multi_agent.agents.router_agent import RouterAgent
from core.langgraph_multi_agent.agents.retrieval_agent import RetrievalAgent
from core.langgraph_multi_agent.agents.clarification_agent import ClarificationAgent
from core.langgraph_multi_agent.agents.context_agent import ContextAgent
from core.langgraph_multi_agent.agents.conversational_agent import ConversationalAgent
from utils.logger import get_logger

log = get_logger("UrbanAdvisorSystem")

class UrbanAdvisorSystem:
    def __init__(self):
        self.toxicity_agent = ToxicityAgent()
        self.parser_agent = ParserAgent()
        self.router_agent = RouterAgent()
        self.retrieval_agent = RetrievalAgent()
        self.clarification_agent = ClarificationAgent()
        self.context_agent = ContextAgent()
        self.conversational_agent = ConversationalAgent()

    def should_end_toxic(self, state: UrbanAdvisorState) -> str:
        if state["is_toxic"]:
            log.info("Сообщение токсичное, завершаем работу")
            return "end"
        return "continue"

    def should_clarify(self, state: UrbanAdvisorState) -> str:
        if state.get("in_clarification_mode", False):
            log.info("Требуются уточнения, завершаем работу")
            return "end"
        return "continue"

    def build_graph(self):
        workflow = StateGraph(UrbanAdvisorState)

        workflow.add_node("toxicity_check", self.toxicity_agent.check_toxicity)
        workflow.add_node("parse_documents", self.parser_agent.process_documents)
        workflow.add_node("route", self.router_agent.classify_route)
        workflow.add_node("clarify", self.clarification_agent.check_clarification)
        workflow.add_node("retrieve", self.retrieval_agent.rag_search)
        workflow.add_node("retrieve_api", self.retrieval_agent.api_search)
        workflow.add_node("retrieve_web", self.retrieval_agent.web_search)
        workflow.add_node("prepare_system_prompt", self.context_agent.prepare_system_prompt)
        workflow.add_node("prepare_context", self.context_agent.prepare_context)
        workflow.add_node("save_to_history", self.context_agent.save_to_history)
        workflow.add_node("update_tokens", self.context_agent.update_tokens)
        workflow.add_node("generate_response", self.conversational_agent.generate_response)
        workflow.add_node("save_response_to_history", self.conversational_agent.save_response_to_history)

        workflow.set_entry_point("toxicity_check")

        workflow.add_conditional_edges(
            "toxicity_check",
            self.should_end_toxic,
            {
                "end": END,
                "continue": "parse_documents"
            }
        )

        workflow.add_edge("parse_documents", "route")
        workflow.add_edge("route", "clarify")

        workflow.add_conditional_edges(
            "clarify",
            self.should_clarify,
            {
                "end": END,
                "continue": "retrieve"
            }
        )

        workflow.add_edge("retrieve", "retrieve_api")
        workflow.add_edge("retrieve_api", "retrieve_web")
        workflow.add_edge("retrieve_web", "prepare_system_prompt")
        workflow.add_edge("prepare_system_prompt", "prepare_context")
        workflow.add_edge("prepare_context", "save_to_history")
        workflow.add_edge("save_to_history", "update_tokens")
        workflow.add_edge("update_tokens", "generate_response")
        workflow.add_edge("generate_response", "save_response_to_history")
        workflow.add_edge("save_response_to_history", END)

        return workflow.compile()

    def save_graph_visualization(self, graph, filename="urban_advisor_graph"):
        try:
            project_root = Path(__file__).parent.parent.parent.parent.parent
            output_dir = project_root / "data"
            output_dir.mkdir(exist_ok=True)

            png_path = output_dir / f"{filename}.png"

            with open(filename, "wb") as f:
                f.write(graph.get_graph().draw_mermaid_png())

            log.info(f"Граф сохранен в: {png_path}")
            return str(png_path)
        except Exception as e:
            log.error(f"Ошибка при сохранении графа: {str(e)}")
            return None

def create_initial_state(message: str, history: list) -> UrbanAdvisorState:
    return {
        "message": message,
        "is_toxic": False,
        "classification": "",
        "history": history,
        "user_documents": None,
        "has_user_documents": False,
        "uploaded_files": None,
        "requires_api": False,
        "requires_web_search": False,
        "is_clear": False,
        "api_data": None,
        "web_search_results": None,
        "rag_context": None,
        "in_clarification_mode": False,
        "clarification_questions": None,
        "system_prompt": None,
        "context": None,
        "total_tokens": 0,
        "response": None
    }

async def main():
    print("\n" + "="*80)
    print("🏙️  ГОРОДСКОЙ СОВЕТНИК - Интеллектуальный помощник для жителей Санкт-Петербурга")
    print("="*80 + "\n")

    log.info("Запуск системы Городской советник")

    system = UrbanAdvisorSystem()
    graph = system.build_graph()

    graph_path = system.save_graph_visualization(graph)
    if graph_path:
        print(f"📊 Визуализация графа сохранена: {graph_path}\n")

    conversation_history = []
    total_tokens_used = 0

    print("💬 Начните диалог! (введите 'exit' или 'quit' для выхода)\n")

    while True:
        try:
            user_input = input("\n👤 Вы: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ['exit', 'quit', 'выход']:
                print("\n👋 До свидания! Всегда рад помочь!")
                print(f"📊 Всего использовано токенов за сессию: {total_tokens_used}\n")
                break

            state = create_initial_state(user_input, conversation_history.copy())

            print("\n⏳ Обработка запроса...")
            log.info(f"История перед запросом: {len(conversation_history)} сообщений")

            result = await graph.ainvoke(state)

            print("-" * 80)

            if result.get('is_toxic'):
                print("🚫 Обнаружено токсичное сообщение. Пожалуйста, общайтесь уважительно.\n")
                continue

            if result.get('in_clarification_mode'):
                questions = result.get('clarification_questions', [])
                print("❓ Для ответа на ваш вопрос нужны уточнения:\n")
                for i, question in enumerate(questions, 1):
                    print(f"   {i}. {question}")
                print()
                continue

            response = result.get('response')
            if response:
                print(f"🤖 Городской советник:\n\n{response}\n")
            else:
                print("⚠️  Не удалось сгенерировать ответ. Попробуйте переформулировать вопрос.\n")

            conversation_history = result.get('history', [])
            log.info(f"История после запроса: {len(conversation_history)} сообщений")

            session_tokens = result.get('total_tokens', 0)
            if session_tokens > total_tokens_used:
                total_tokens_used = session_tokens

            print(f"📊 Использовано токенов: {session_tokens}")
            print(f"💬 Сообщений в истории: {len(conversation_history)}")
            print("-" * 80)

        except KeyboardInterrupt:
            print("\n\n👋 Прервано пользователем. До свидания!")
            print(f"📊 Всего использовано токенов за сессию: {total_tokens_used}\n")
            break
        except Exception as e:
            log.error(f"Ошибка при обработке запроса: {str(e)}")
            print(f"\n❌ Произошла ошибка: {str(e)}")
            print("Попробуйте снова или введите другой вопрос.\n")

if __name__ == "__main__":
    asyncio.run(main())