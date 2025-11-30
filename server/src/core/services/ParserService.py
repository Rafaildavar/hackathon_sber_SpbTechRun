import os
import sys
from pathlib import Path

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from core.services.parser.gu_parser.spiders.knowledge_base_spider import KnowledgeBaseSpider
from core.services.parser.gu_parser.spiders.life_situations_spider import LifeSituationsSpider
from utils.logger import get_logger

log = get_logger("ParserService")


class ParserService:
    def __init__(self):
        self.parser_dir = Path(__file__).parent / "parser"
        self.scrapy_cfg = self.parser_dir / "scrapy.cfg"
        log.info("ParserService init")

    def run_spider(self, spider_name: str):
        log.info(f"Starting spider: {spider_name}")

        os.chdir(self.parser_dir)

        settings = get_project_settings()
        settings.set("SCRAPY_SETTINGS_MODULE", "core.services.parser.gu_parser.settings")

        process = CrawlerProcess(settings)

        if spider_name == "knowledge_base":
            process.crawl(KnowledgeBaseSpider)
        elif spider_name == "life_situations":
            process.crawl(LifeSituationsSpider)
        else:
            raise ValueError(f"Unknown spider: {spider_name}")

        process.start()
        log.info(f"Spider {spider_name} finished")

    def run_all_spiders(self):
        log.info("Starting all spiders")

        os.chdir(self.parser_dir)

        settings = get_project_settings()
        settings.set("SCRAPY_SETTINGS_MODULE", "core.services.parser.gu_parser.settings")

        process = CrawlerProcess(settings)

        process.crawl(KnowledgeBaseSpider)
        process.crawl(LifeSituationsSpider)

        process.start()
        log.info("All spiders finished")


if __name__ == "__main__":
    service = ParserService()

    if len(sys.argv) > 1:
        spider_name = sys.argv[1]
        service.run_spider(spider_name)
    else:
        service.run_all_spiders()