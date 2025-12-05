import asyncio
import tempfile
import shutil
from pathlib import Path
from typing import List

from core.services.ServiceManager import service_manager
from utils.logger import get_logger

log = get_logger("DocumentUploadEndpoint")


class DocumentUploadEndpoint:
    def __init__(self):
        self.service_manager = service_manager
        self.chunk_processor = service_manager.chunk_processor

    async def process_uploaded_file(self, file_path: str, filename: str) -> dict:
        try:
            log.info(f"Начинаем обработку файла: {filename}")

            temp_chunks_dir = tempfile.mkdtemp(prefix="chunks_")

            try:
                await self.chunk_processor.process_file(file_path, temp_chunks_dir)

                chunks_path = Path(temp_chunks_dir)
                chunk_files = list(chunks_path.glob("chunk_*.txt"))

                if not chunk_files:
                    return {
                        "success": False,
                        "message": f"Не удалось извлечь текст из файла {filename}",
                        "chunks_count": 0
                    }

                self.service_manager.add_vectorized_chunks(temp_chunks_dir)

                log.info(f"Файл {filename} успешно обработан, создано {len(chunk_files)} чанков")

                return {
                    "success": True,
                    "message": f"Файл {filename} успешно обработан и добавлен в базу знаний",
                    "chunks_count": len(chunk_files),
                    "filename": filename
                }

            finally:
                shutil.rmtree(temp_chunks_dir, ignore_errors=True)

        except Exception as e:
            log.error(f"Ошибка при обработке файла {filename}: {e}")
            return {
                "success": False,
                "message": f"Ошибка при обработке файла {filename}: {str(e)}",
                "chunks_count": 0
            }

    async def process_multiple_files(self, file_paths: List[tuple]) -> dict:
        results = []
        total_chunks = 0
        successful_files = 0

        for file_path, filename in file_paths:
            result = await self.process_uploaded_file(file_path, filename)
            results.append(result)

            if result["success"]:
                successful_files += 1
                total_chunks += result["chunks_count"]

        return {
            "success": successful_files > 0,
            "message": f"Обработано {successful_files} из {len(file_paths)} файлов",
            "total_chunks": total_chunks,
            "files_processed": successful_files,
            "total_files": len(file_paths),
            "details": results
        }

    def clear_knowledge_base(self) -> dict:
        try:
            self.service_manager.clear_all_chunks()
            log.info("База знаний успешно очищена")

            return {
                "success": True,
                "message": "База знаний успешно очищена"
            }
        except Exception as e:
            log.error(f"Ошибка при очистке базы знаний: {e}")
            return {
                "success": False,
                "message": f"Ошибка при очистке базы знаний: {str(e)}"
            }

    def get_knowledge_base_info(self) -> dict:
        try:
            info = self.service_manager.qdrant_service.get_collection_info()
            return {
                "success": True,
                "collection_name": info.get("name", ""),
                "documents_count": info.get("points_count", 0),
                "vectors_count": info.get("vectors_count", 0),
                "status": info.get("status", "unknown")
            }
        except Exception as e:
            log.error(f"Ошибка при получении информации о базе знаний: {e}")
            return {
                "success": False,
                "message": f"Ошибка при получении информации: {str(e)}"
            }


async def main():
    endpoint = DocumentUploadEndpoint()

    info = endpoint.get_knowledge_base_info()
    print(f"Информация о базе знаний: {info}")


if __name__ == "__main__":
    asyncio.run(main())