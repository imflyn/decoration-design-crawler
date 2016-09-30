import os
import sys
from os.path import dirname

path = dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(path)

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import signals
from pydispatch import dispatcher
from msic.proxy.proxy_pool import proxy_pool
from tubatu.spiders.room_spider import RoomSpider

proxy_pool.start()

process = CrawlerProcess(get_project_settings())


def start_scrapy():
	process.stop()
	process.crawl(RoomSpider())
	process.start()


dispatcher.connect(start_scrapy, signals.engine_stopped)
start_scrapy()
