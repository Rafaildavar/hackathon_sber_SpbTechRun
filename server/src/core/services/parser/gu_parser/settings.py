import os

BOT_NAME = "gu_parser"

SPIDER_MODULES = ["core.services.parser.gu_parser.spiders"]
NEWSPIDER_MODULE = "core.services.parser.gu_parser.spiders"

USER_AGENT = "gu_parser (+http://www.yourdomain.com)"

ROBOTSTXT_OBEY = True

CONCURRENT_REQUESTS = 32

DOWNLOAD_DELAY = 0.5

COOKIES_ENABLED = False

TELNETCONSOLE_ENABLED = False

DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ru,en;q=0.9",
}

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 0.5
AUTOTHROTTLE_MAX_DELAY = 5
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0

HTTPCACHE_ENABLED = False

FEED_EXPORT_ENCODING = "utf-8"

DATA_DIR = os.path.join(os.path.dirname(__file__), '../../../data')