from selenium import webdriver
from scrapy.spiders import CrawlSpider
import time


class ParseJSSpider(CrawlSpider):
	def __init__(self):
		CrawlSpider.__init__(self)
		# use any browser you wish
		self.browser = webdriver.PhantomJS()

	def __del__(self):
		self.browser.quit()

	def handle_response(self, response):
		self.browser.get(response.url)
		# loading time interval
		time.sleep(5)
