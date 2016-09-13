import random

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver

from msic.common import log, agents
from msic.proxy.proxy_pool import proxy_pool


class CatchExceptionMiddleware(object):
	def process_response(self, request, response, spider):
		if response.status <= 200 or response.status >= 400:
			proxy_pool.add_failed_time(request.meta['proxy'].replace('http://', ''))
		return response

	def process_exception(self, request, exception, spider):
		proxy_pool.add_failed_time(request.meta['proxy'].replace('http://', ''))


class CustomHttpProxyMiddleware(object):
	def process_request(self, request, spider):
		try:
			request.meta['proxy'] = "http://%s" % proxy_pool.random_choice_proxy()
		except Exception as e:
			log.error(e)


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
		service_args = [
			"--webdriver-loglevel=ERROR"
		]
		self.driver = webdriver.PhantomJS(service_args=service_args)
		self.driver.set_page_load_timeout(60)

	def spider_closed(self, spider):
		self.driver.quit()
