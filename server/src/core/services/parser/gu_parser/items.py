import scrapy


class KnowledgeBaseItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    image = scrapy.Field()
    content = scrapy.Field()
    category = scrapy.Field()
    scraped_at = scrapy.Field()
    metadata = scrapy.Field()