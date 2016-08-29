import random

from scrapy import signals

from msic import agents, log, proxy
from selenium import webdriver
from scrapy.http import HtmlResponse


class CustomHttpProxyMiddleware(object):
	def process_request(self, request, spider):
		if self.use_proxy(request):
			p = random.choice(proxy.FREE_PROXIES)
			try:
				request.meta['proxy'] = "http://%s" % p['ip_port']
			except Exception as e:
				log.error("Exception %s" % e)

	def use_proxy(self, request):
		"""
		using direct download for depth <= 2
		using proxy with probability 0.3
		"""
		if "depth" in request.meta and int(request.meta['depth']) <= 2:
			return False
		i = random.randint(1, 10)
		return i <= 2


class CustomUserAgentMiddleware(object):
	def process_request(self, request, spider):
		agent = random.choice(agents)
		request.headers['User-Agent'] = agent


class JavaScriptMiddleware(object):
	# def process_request(self, request, spider):
	# 	driver = webdriver.PhantomJS()
	# 	driver.get(request.url)
	#
	# 	body = driver.page_source
	# 	return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)

	@classmethod
	def from_crawler(cls, crawler):
		middleware = cls()
		crawler.signals.connect(middleware.spider_opened, signals.spider_opened)
		crawler.signals.connect(middleware.spider_closed, signals.spider_closed)
		return middleware

	def process_request(self, request, spider):
		self.driver.get(request.url)
		body = self.driver.page_source
		return HtmlResponse(self.driver.current_url, body=body, encoding='utf-8', request=request)

	def spider_opened(self, spider):
		self.driver = webdriver.PhantomJS()

	def spider_closed(self, spider):
		self.driver.close()
