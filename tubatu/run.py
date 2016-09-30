import os
import sys
from os.path import dirname

from twisted.internet import reactor

path = dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(path)

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import signals
from pydispatch import dispatcher
from tubatu.spiders.room_spider import RoomSpider


class Runner(object):
	def __init__(self):
		dispatcher.connect(self.crawl, signals.engine_stopped)
		self.setting = get_project_settings()
		self.process = None

	def start_scrapy(self):
		self.process = CrawlerProcess(self.setting)
		self.crawl()
		reactor.run()

	def crawl(self):
		self.process.crawl(RoomSpider())

	def start_proxy_pool(self):
		from msic.proxy.proxy_pool import proxy_pool
		proxy_pool.start()

	def run(self):
		self.start_proxy_pool()
		self.start_scrapy()


if __name__ == '__main__':
	Runner().run()
