from scrapy.crawler import CrawlerProcess, Crawler
from scrapy.settings import Settings

from msic import reload_proxy
from tubatu.tubatu import settings
from scrapy.utils.project import get_project_settings
from tubatu.tubatu.spiders.room_spider import RoomSpider

reload_proxy.start()
settings = get_project_settings()
process = CrawlerProcess(settings)
process.crawl(RoomSpider())
process.start()
