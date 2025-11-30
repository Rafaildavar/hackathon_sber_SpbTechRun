import asyncio
import json
from urllib.parse import unquote

from core.services.ServiceManager import service_manager
from utils.prompt_loader import render_prompt
from utils.logger import get_logger

log = get_logger("RagAnswerEndpoint")

class RagAnswerEndpoint:
    def __init__(self):
        self.llm_service = service_manager.llm_service
        self.qdrant_service = service_manager.qdrant_service
        self.reranker = service_manager.reranker_service
        self.bm25_service = service_manager.bm25_service

    async def get_answer(self, user_question: str):
        bm25_results = self.bm25_service.search(user_question)

        if not bm25_results:
            log.warning("BM25 не вернул результатов, используем только векторный поиск")
            top_chunks_raw = self.qdrant_service.search_similar(user_question)
        else:
            log.info(f"BM25 вернул {len(bm25_results)} кандидатов")

            bm25_ids = [result[3].get("id") for result in bm25_results]

            vector_results = self.qdrant_service.search_similar(user_question)

            vector_ids = {chunk["id"] for chunk in vector_results}
            bm25_chunks = []
            for result in bm25_results:
                _, text, score, metadata = result
                if metadata.get("id") in vector_ids:
                    for chunk in vector_results:
                        if chunk["id"] == metadata.get("id"):
                            bm25_chunks.append(chunk)
                            break

            if not bm25_chunks:
                log.warning("Нет пересечений BM25 и векторного поиска, используем только векторный")
                top_chunks_raw = vector_results
            else:
                log.info(f"Найдено {len(bm25_chunks)} пересечений BM25 и векторного поиска")
                top_chunks_raw = bm25_chunks

        documents = [chunk["text"] for chunk in top_chunks_raw]

        reranked_results = self.reranker.rerank(user_question, documents)
        reranked_indices = [idx for idx, _, _ in reranked_results]

        reranked_chunks_raw = [top_chunks_raw[idx] for idx in reranked_indices]
        top_chunks = [chunk["text"] for chunk in reranked_chunks_raw]
        top_links = [unquote(chunk['link']) for chunk in reranked_chunks_raw]
        top_titles = [chunk["title"] for chunk in reranked_chunks_raw]

        top_docs = [{"title":top_titles[i], "link": top_links[i],'text':top_chunks[i]} for i in range(len(top_chunks))]

        top_docs_json = json.dumps(top_docs, indent=3, ensure_ascii=False)
        prompt = render_prompt("rag_answer_prompt", question=user_question, data=top_docs_json)
        llm_answer = await self.llm_service.fetch_completion(prompt)
        return llm_answer

async def main():
    ser = RagAnswerEndpoint()
    result = await ser.get_answer('В чем заключается успех прохождения испытательного срока?')

if __name__ == "__main__":
    asyncio.run(main())