class GuParserPipeline:
    def open_spider(self, spider):
        self.items_count = 0

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        if item.get('title'):
            item['title'] = item['title'].strip()

        if item.get('content'):
            item['content'] = item['content'].strip()

        self.items_count += 1

        filtered_item = {
            'url': item.get('url'),
            'title': item.get('title'),
            'content': item.get('content')
        }

        return filtered_item