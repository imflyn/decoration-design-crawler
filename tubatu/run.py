import os
import sys
from os.path import dirname

path = dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(path)

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from msic.scrapy import ip_pool
from tubatu.spiders.room_spider import RoomSpider

ip_pool.start()

process = CrawlerProcess(get_project_settings())
process.crawl(RoomSpider())
process.start()
