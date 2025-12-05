import re
import bm25s
from pathlib import Path
from typing import List, Tuple, Dict, Any
from pymorphy3 import MorphAnalyzer

from config.Config import CONFIG
from utils.logger import get_logger

BM25_DATA_DIR = Path("/data/bm25")
from core.services.QdrantService import QdrantService

log = get_logger("BM25Service")


class BM25Service:

    def __init__(self):
        self.top_samples = CONFIG.bm25.top_samples
        self.metadata: List[Dict[str, Any]] = []
        self.bm25: bm25s.BM25 | None = None
        self.morph = MorphAnalyzer()

        log.info("BM25Service инициализирован")

    def sync_with_qdrant(self, qdrant_service: 'QdrantService'):
        """Синхронизация BM25 индекса с коллекцией Qdrant

        Args:
            qdrant_service: Экземпляр QdrantService для получения данных
        """
        try:
            if self.load():
                log.info("BM25 индекс загружен с диска, пропускаем синхронизацию с Qdrant")
                return

            collection_info = qdrant_service.get_collection_info()
            points_count = collection_info.get("points_count", 0)

            if points_count == 0:
                log.info("Коллекция Qdrant пуста, пропускаем синхронизацию BM25")
                return

            scroll_result = qdrant_service.client.scroll(
                collection_name=qdrant_service.collection_name,
                limit=10000,
                with_payload=True,
                with_vectors=False
            )

            points, _ = scroll_result

            documents = []
            for point in points:
                doc = {
                    "text": point.payload.get("text", ""),
                    "id": point.id,
                    "url": point.payload.get("url", ""),
                    "title": point.payload.get("title", ""),
                    "filename": point.payload.get("filename", ""),
                    "chunk_id": point.payload.get("chunk_id", "")
                }
                documents.append(doc)

            if documents:
                self.index_documents(documents)
                self.save()
                log.info(f"BM25 синхронизирован с Qdrant: {len(documents)} документов")

        except Exception as e:
            log.error(f"Ошибка при синхронизации BM25 с Qdrant: {e}")

    def _tokenize(self, text: str) -> List[str]:
        """Токенизация текста с лемматизацией для русского языка"""
        # Remove punctuation and split into words
        words = re.findall(r'[а-яёa-z0-9]+', text.lower())

        # Lemmatize each word
        lemmas = []
        for word in words:
            parsed = self.morph.parse(word)
            if parsed:
                lemma = parsed[0].normal_form
                lemmas.append(lemma)
            else:
                lemmas.append(word)

        return lemmas

    def index_documents(self, documents: List[Dict[str, Any]]):
        """Индексация документов для BM25 поиска

        Args:
            documents: Список документов с полями 'text' и опциональными метаданными
        """
        self.metadata = documents

        corpus_tokens = [self._tokenize(doc.get("text", "")) for doc in documents]

        self.bm25 = bm25s.BM25()
        self.bm25.index(corpus_tokens)

        log.info(f"Проиндексировано {len(documents)} документов для BM25")

    def search(self, query: str) -> List[Tuple[int, str, float, Dict[str, Any]]]:
        """Поиск документов с использованием BM25

        Args:
            query: Поисковый запрос

        Returns:
            Список кортежей (индекс, текст, score, метаданные)
        """
        if self.bm25 is None or len(self.metadata) == 0:
            log.warning("BM25 индекс пуст. Необходимо проиндексировать документы.")
            return []

        tokenized_query = [self._tokenize(query)]

        results_obj, scores = self.bm25.retrieve(tokenized_query, k=self.top_samples)

        results = []
        for i, idx in enumerate(results_obj[0]):
            score = scores[0][i]
            if score > 0:
                doc = self.metadata[idx]
                text = doc.get("text", "")
                results.append((idx, text, float(score), doc))

        log.info(f"BM25 поиск: найдено {len(results)} релевантных документов")
        for i, (idx, doc_text, score, _) in enumerate(results[:5], 1):
            preview = doc_text[:100] + "..." if len(doc_text) > 100 else doc_text
            log.info(f"{i} чанк. [Score: {score:.4f}] (Индекс: {idx}) - {preview}")

        return results

    def add_documents(self, new_documents: List[Dict[str, Any]]):
        """Добавление новых документов к существующему индексу

        Args:
            new_documents: Список новых документов для добавления
        """
        if not new_documents:
            return

        self.metadata.extend(new_documents)

        corpus_tokens = [self._tokenize(doc.get("text", "")) for doc in self.metadata]

        self.bm25 = bm25s.BM25()
        self.bm25.index(corpus_tokens)

        log.info(f"Добавлено {len(new_documents)} документов. Всего в индексе: {len(self.metadata)}")
        self.save()

    def clear(self):
        """Очистка индекса BM25"""
        self.metadata = []
        self.bm25 = None
        log.info("BM25 индекс очищен")

    def get_index_size(self) -> int:
        """Получение количества документов в индексе"""
        return len(self.metadata)

    def save(self):
        """Сохранение BM25 индекса на диск"""
        try:
            BM25_DATA_DIR.mkdir(parents=True, exist_ok=True)

            if self.bm25 is not None:
                self.bm25.save(str(BM25_DATA_DIR), corpus=self.metadata)

            log.info(f"BM25 индекс сохранён в {BM25_DATA_DIR}: {len(self.metadata)} документов")

        except Exception as e:
            log.error(f"Ошибка при сохранении BM25 индекса: {e}")

    def load(self) -> bool:
        """Загрузка BM25 индекса с диска

        Returns:
            True если загрузка успешна, False иначе
        """
        try:
            index_path = BM25_DATA_DIR / "index.json"

            if not index_path.exists():
                log.info("BM25 индекс не найден на диске")
                return False

            self.bm25 = bm25s.BM25.load(str(BM25_DATA_DIR), load_corpus=True, mmap=True)
            self.metadata = list(self.bm25.corpus)

            log.info(f"BM25 индекс загружен из {BM25_DATA_DIR}: {len(self.metadata)} документов")
            return True

        except Exception as e:
            log.error(f"Ошибка при загрузке BM25 индекса: {e}")
            return False
