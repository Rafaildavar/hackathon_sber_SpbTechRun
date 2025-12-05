import os
from typing import List, Dict
from utils.logger import get_logger

log = get_logger("ParserAgentTools")

class DocumentProcessor:
    def __init__(self):
        pass

    def process_uploaded_files(self, uploaded_files: List[Dict]) -> List[Dict]:
        processed_docs = []

        for file_info in uploaded_files:
            file_path = file_info.get("path")
            file_type = file_info.get("type")
            file_name = file_info.get("name")

            if not file_path or not os.path.exists(file_path):
                log.warning(f"Файл не найден: {file_path}")
                continue

            log.info(f"Обработка файла: {file_name} ({file_type})")

            processed_docs.append({
                "path": file_path,
                "name": file_name,
                "type": file_type,
                "processed": True
            })

        return processed_docs