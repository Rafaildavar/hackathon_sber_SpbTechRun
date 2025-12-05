import asyncio
from langgraph.graph import StateGraph, END
from core.langgraph_multi_agent.agents.parser_agent.state import ParserState
from core.langgraph_multi_agent.agents.parser_agent.tools import DocumentProcessor
from utils.logger import get_logger

log = get_logger("ParserAgent")

class ParserAgent:
    def __init__(self):
        self.doc_processor = DocumentProcessor()

    async def process_documents(self, state: ParserState) -> ParserState:
        uploaded_files = state.get("uploaded_files")
        has_user_documents = state.get("has_user_documents", False)

        if not has_user_documents or not uploaded_files:
            log.info("Нет документов для обработки")
            return {**state, "user_documents": None}

        log.info(f"Обработка {len(uploaded_files)} загруженных файлов")

        processed_docs = self.doc_processor.process_uploaded_files(uploaded_files)

        log.info(f"Обработано {len(processed_docs)} документов")

        return {**state, "user_documents": processed_docs}

    def build_graph(self):
        workflow = StateGraph(ParserState)

        workflow.add_node("process_documents", self.process_documents)

        workflow.set_entry_point("process_documents")
        workflow.add_edge("process_documents", END)

        return workflow.compile()

async def main():
    agent = ParserAgent()
    graph = agent.build_graph()

    test_state = {
        "message": "Обработай этот документ",
        "classification": "",
        "history": [],
        "user_documents": None,
        "has_user_documents": True,
        "uploaded_files": [
            {"path": "/core/data/sample.pdf", "type": "pdf", "name": "sample.pdf"}
        ]
    }

    result = await graph.ainvoke(test_state)
    print(f"Результат: {result}")

if __name__ == "__main__":
    asyncio.run(main())