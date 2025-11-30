#!/usr/bin/env python
"""
Скрипт для запуска парсера жизненных ситуаций GU SPB
"""
import sys
from pathlib import Path

# Добавляем корневую директорию в PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent))

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def main():
    """Основная функция для запуска парсера"""
    
    # Получаем настройки проекта
    settings = get_project_settings()
    
    # Создаем процесс краулера
    process = CrawlerProcess(settings)
    
    # Добавляем spider для жизненных ситуаций
    process.crawl('life_situations')
    
    try:
        # Запускаем парсинг
        process.start()
        
    except KeyboardInterrupt:
        sys.exit(0)
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
