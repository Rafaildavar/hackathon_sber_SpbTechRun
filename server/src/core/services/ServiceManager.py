from typing import Optional

from core.services.QdrantService import QdrantService
from core.services.RerankerService import RerankerService
from core.services.СhunksService import ChunkProcessor
from core.services.LLMService import LLMService
from core.services.BM25Service import BM25Service
from utils.logger import get_logger

log = get_logger("ServiceManager")


class ServiceManager:

    _instance: Optional['ServiceManager'] = None
    _initialized: bool = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not ServiceManager._initialized:
            log.info("Инициализация всех сервисов...")
            self._qdrant_service: Optional[QdrantService] = None
            self._reranker_service: Optional[RerankerService] = None
            self._chunk_processor: Optional[ChunkProcessor] = None
            self._llm_service: Optional[LLMService] = None
            self._bm25_service: Optional[BM25Service] = None
            ServiceManager._initialized = True

    def initialize(self):
        log.info("Загрузка ML-моделей и инициализация сервисов...")

        log.info("1/5 Инициализация QdrantService...")
        self._qdrant_service = QdrantService()

        log.info("2/5 Инициализация RerankerService...")
        self._reranker_service = RerankerService()

        log.info("3/5 Инициализация ChunkProcessor...")
        self._chunk_processor = ChunkProcessor()

        log.info("4/5 Инициализация LLMService...")
        self._llm_service = LLMService()

        log.info("5/5 Инициализация BM25Service...")
        self._bm25_service = BM25Service()
        self._bm25_service.sync_with_qdrant(self._qdrant_service)

        log.info("Все сервисы успешно инициализированы и готовы к работе!")

    def clear_all_chunks(self):
        """Очистка всех чанков из Qdrant и BM25"""
        self.qdrant_service.clear_all_chunks()
        self.bm25_service.clear()
        log.info("Все чанки очищены из Qdrant и BM25")

    def add_vectorized_chunks(self, chunks_dir):
        """Добавление чанков из директории в Qdrant и BM25"""
        docs = self.qdrant_service.add_vectorized_chunks(chunks_dir)
        if docs:
            self.bm25_service.add_documents(docs)
        return len(docs)

    def add_chunks_directly(self, chunks):
        """Добавление чанков напрямую в Qdrant и BM25"""
        docs = self.qdrant_service.add_chunks_directly(chunks)
        if docs:
            self.bm25_service.add_documents(docs)
        return len(docs)

    @property
    def qdrant_service(self) -> QdrantService:
        if self._qdrant_service is None:
            raise RuntimeError("QdrantService не инициализирован. Вызовите initialize() сначала.")
        return self._qdrant_service

    @property
    def reranker_service(self) -> RerankerService:
        if self._reranker_service is None:
            raise RuntimeError("RerankerService не инициализирован. Вызовите initialize() сначала.")
        return self._reranker_service

    @property
    def chunk_processor(self) -> ChunkProcessor:
        if self._chunk_processor is None:
            raise RuntimeError("ChunkProcessor не инициализирован. Вызовите initialize() сначала.")
        return self._chunk_processor

    @property
    def llm_service(self) -> LLMService:
        if self._llm_service is None:
            raise RuntimeError("LLMService не инициализирован. Вызовите initialize() сначала.")
        return self._llm_service

    @property
    def bm25_service(self) -> BM25Service:
        if self._bm25_service is None:
            raise RuntimeError("BM25Service не инициализирован. Вызовите initialize() сначала.")
        return self._bm25_service


service_manager = ServiceManager()