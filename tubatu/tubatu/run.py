from scrapy.crawler import CrawlerProcess
from msic import reload_proxy

from tubatu.tubatu.spiders.room_spider import RoomSpider

reload_proxy.start()

process = CrawlerProcess()
process.crawl(RoomSpider())
process.start()
