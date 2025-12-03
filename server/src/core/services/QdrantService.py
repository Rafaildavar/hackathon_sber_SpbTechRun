from typing import List, Dict, Any
from pathlib import Path
import uuid
import asyncio
import json

import torch
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer

from utils.logger import get_logger
from config.Config import CONFIG


def get_device():
    """Detect best available device for inference"""
    if torch.cuda.is_available():
        return "cuda"
    elif torch.backends.mps.is_available():
        return "mps"
    else:
        return "cpu"

log = get_logger("QdrantService")

class QdrantService:
    def __init__(self):
        self.host = CONFIG.qdrant.host
        self.port = CONFIG.qdrant.port
        self.collection_name = CONFIG.qdrant.collection_name
        self.model_name = CONFIG.qdrant.model_name
        self.vector_size = CONFIG.qdrant.vector_size
        self.top_samples = CONFIG.qdrant.top_samples
        self.batch_size = CONFIG.qdrant.batch_size

        try:
            self.client = QdrantClient(host=self.host, port=self.port, timeout=60)
            log.info(f"Подключение к Qdrant установлено: {self.host}:{self.port}")
        except Exception as e:
            log.error(f"Ошибка подключения к Qdrant: {e}")
            raise

        try:
            device = get_device()
            self.model = SentenceTransformer(self.model_name, device=device)
            log.info(f"Модель {self.model_name} загружена успешно на устройство: {device}")
        except Exception as e:
            log.error(f"Ошибка загрузки модели {self.model_name}: {e}")
            raise

        self._ensure_collection_exists()

    def _ensure_collection_exists(self) -> None:
        try:
            collections = self.client.get_collections()
            collection_names = [col.name for col in collections.collections]

            if self.collection_name not in collection_names:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=self.vector_size,
                        distance=Distance.COSINE
                    )
                )
                log.info(f"Коллекция '{self.collection_name}' создана")
            else:
                log.info(f"Коллекция '{self.collection_name}' уже существует")

        except Exception as e:
            log.error(f"Ошибка при создании коллекции: {e}")
            raise

    def clear_all_chunks(self):
        """Очистка всех чанков из Qdrant коллекции"""
        try:
            self.client.delete_collection(collection_name=self.collection_name)
            log.info(f"Коллекция '{self.collection_name}' удалена")

            self._ensure_collection_exists()

            log.info("Все чанки успешно удалены из Qdrant")

        except Exception as e:
            log.error(f"Ошибка при очистке чанков: {e}")

    def add_vectorized_chunks(self, chunks_dir) -> List[Dict[str, Any]]:
        """Добавление чанков из директории в Qdrant

        Returns:
            Список документов для индексации в других сервисах
        """
        try:
            chunks_path = Path(chunks_dir)
            if not chunks_path.exists():
                log.error(f"Директория {chunks_dir} не существует")
                return []

            chunk_files = list(chunks_path.glob("*.json"))

            if not chunk_files:
                log.warning(f"Не найдено файлов чанков в директории {chunks_dir}")
                return []

            log.info(f"Найдено {len(chunk_files)} файлов чанков")

            # Load all chunks data first
            chunks_data = []
            for chunk_file in chunk_files:
                try:
                    with open(chunk_file, 'r', encoding='utf-8') as f:
                        chunk_data = json.load(f)

                    content = chunk_data.get("content", "")

                    if not content:
                        log.warning(f"Файл {chunk_file.name} имеет пустой content, пропускаем")
                        continue

                    chunks_data.append({
                        "content": content,
                        "url": chunk_data.get("url", ""),
                        "title": chunk_data.get("title", ""),
                        "parsed_at": chunk_data.get("parsed_at", ""),
                        "filename": chunk_file.name,
                        "chunk_id": chunk_file.stem
                    })

                except Exception as e:
                    log.error(f"Ошибка при обработке файла {chunk_file}: {e}")
                    continue

            if not chunks_data:
                log.error("Не удалось обработать ни одного файла чанков")
                return []

            # Batch encode all texts at once
            log.info(f"Кодирование {len(chunks_data)} чанков...")
            texts = [chunk["content"] for chunk in chunks_data]
            embeddings = self.model.encode(texts, show_progress_bar=True, batch_size=16)
            log.info("Кодирование завершено")

            # Create points
            points = []
            for i, chunk in enumerate(chunks_data):
                point = PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embeddings[i].tolist(),
                    payload={
                        "text": chunk["content"],
                        "url": chunk["url"],
                        "title": chunk["title"],
                        "parsed_at": chunk["parsed_at"],
                        "filename": chunk["filename"],
                        "chunk_id": chunk["chunk_id"]
                    }
                )
                points.append(point)

            # Upload to Qdrant in batches
            total_uploaded = 0

            for i in range(0, len(points), self.batch_size):
                batch = points[i:i + self.batch_size]
                self.client.upsert(
                    collection_name=self.collection_name,
                    points=batch,
                    wait=True
                )
                total_uploaded += len(batch)
                log.info(f"Загружено {total_uploaded}/{len(points)} чанков")

            log.info(f"Успешно добавлено {len(points)} чанков в Qdrant")

            # Return documents for other services to index
            return [
                {
                    "text": point.payload["text"],
                    "id": point.id,
                    "url": point.payload.get("url", ""),
                    "title": point.payload.get("title", ""),
                    "filename": point.payload.get("filename", ""),
                    "chunk_id": point.payload.get("chunk_id", "")
                }
                for point in points
            ]

        except Exception as e:
            log.error(f"Ошибка при добавлении чанков: {e}")
            return []

    def add_chunks_directly(self, chunks: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """Добавление чанков напрямую в Qdrant

        Returns:
            Список документов для индексации в других сервисах
        """
        try:
            points = []

            for chunk_data in chunks:
                content = chunk_data.get("text", "")

                if not content:
                    log.warning("Пропущен чанк с пустым текстом")
                    continue

                embedding = self.model.encode(content).tolist()

                point = PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding,
                    payload={
                        "text": content,
                        "url": chunk_data.get("url", ""),
                        "title": chunk_data.get("title", ""),
                        "parsed_at": "",
                        "filename": "manual",
                        "chunk_id": str(uuid.uuid4())
                    }
                )

                points.append(point)

            if not points:
                log.error("Не удалось обработать ни одного чанка")
                return []

            total_uploaded = 0

            for i in range(0, len(points), self.batch_size):
                batch = points[i:i + self.batch_size]
                self.client.upsert(
                    collection_name=self.collection_name,
                    points=batch,
                    wait=True
                )
                total_uploaded += len(batch)
                log.info(f"Загружено {total_uploaded}/{len(points)} чанков")

            log.info(f"Успешно добавлено {len(points)} чанков в Qdrant")

            return [
                {
                    "text": point.payload["text"],
                    "id": point.id,
                    "url": point.payload.get("url", ""),
                    "title": point.payload.get("title", ""),
                    "filename": point.payload.get("filename", ""),
                    "chunk_id": point.payload.get("chunk_id", "")
                }
                for point in points
            ]

        except Exception as e:
            log.error(f"Ошибка при добавлении чанков: {e}")
            raise

    def get_collection_info(self) -> Dict[str, Any]:
        try:
            collection_info = self.client.get_collection(self.collection_name)

            vectors_count = getattr(collection_info, 'vectors_count', None) or getattr(collection_info, 'indexed_vectors_count', 0)

            return {
                "name": self.collection_name,
                "vectors_count": vectors_count,
                "points_count": collection_info.points_count,
                "status": collection_info.status
            }
        except Exception as e:
            log.error(f"Ошибка при получении информации о коллекции: {e}")
            return {}

    def search_similar(self, query: str) -> List[Dict[str, Any]]:
        try:
            query_embedding = self.model.encode(query).tolist()

            search_results = self.client.query_points(
                collection_name=self.collection_name,
                query=query_embedding,
                limit=self.top_samples
            )

            results = []
            for result in search_results.points:
                results.append({
                    "id": result.id,
                    "score": result.score,
                    "text": result.payload.get("text", ""),
                    "link": result.payload.get("url", ""),
                    "title": result.payload.get("title", ""),
                    "parsed_at": result.payload.get("parsed_at", ""),
                    "filename": result.payload.get("filename", ""),
                    "chunk_id": result.payload.get("chunk_id", "")
                })

            return results

        except Exception as e:
            log.error(f"Ошибка при поиске: {e}")
            return []


async def main():
    qdrant_service = QdrantService()

    chunks_dir = "./core/data/chunks"

    log.info("Очистка существующих чанков из Qdrant...")
    qdrant_service.clear_all_chunks()

    log.info("Добавление чанков в Qdrant...")
    docs = qdrant_service.add_vectorized_chunks(chunks_dir)
    log.info(f"Чанки успешно добавлены в векторную БД: {len(docs)} документов")

    info = qdrant_service.get_collection_info()
    log.info(f"Информация о коллекции: {info}")

    if info.get("points_count", 0) > 0:
        query = "Какая приоритетная группа для прохождения диспансеризации?"

        results = qdrant_service.search_similar(query)
        for i, result in enumerate(results, 1):
            log.info(f"{i}. Score: {result['score']:.3f}, File: {result['filename']}")
            log.info(f"Text: {result['text'][:100]}...")
            log.info(f"Link: {result['link']}")
            log.info(f"Title: {result['title']}")
    else:
        log.warning("Коллекция пуста, проверьте директорию с чанками")

if __name__ == "__main__":
    asyncio.run(main())