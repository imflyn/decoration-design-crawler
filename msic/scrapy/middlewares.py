import random

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver

from msic.common import log, agents, proxy


class CustomHttpProxyMiddleware(object):
	def process_request(self, request, spider):
		if self.use_proxy(request) and len(proxy.FREE_PROXIES) > 0:
			p = random.choice(proxy.FREE_PROXIES)
			try:
				request.meta['proxy'] = "http://%s" % p['ip_port']
			except Exception as e:
				log.error(e)

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
		agent = random.choice(agents.AGENTS_ALL)
		request.headers['User-Agent'] = agent


class JavaScriptMiddleware(object):
	@classmethod
	def from_crawler(cls, crawler):
		middleware = cls()
		crawler.signals.connect(middleware.spider_opened, signals.spider_opened)
		crawler.signals.connect(middleware.spider_closed, signals.spider_closed)
		return middleware

	def process_request(self, request, spider):
		if 'javascript' in request.meta and request.meta['javascript'] is True:
			self.driver.get(request.url)
			body = self.driver.page_source
			return HtmlResponse(self.driver.current_url, body=body, encoding='utf-8', request=request)

	def spider_opened(self, spider):
		self.driver = webdriver.PhantomJS(service_args=["--webdriver-loglevel=ERROR"])

	def spider_closed(self, spider):
		self.driver.quit()
