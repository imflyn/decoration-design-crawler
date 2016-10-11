from scrapy import Spider
from scrapy.exceptions import CloseSpider


class RedirectionMiddleware(object):
	def process_response(self, request, response, spider: Spider):
		if response.status == 302 or response.status == 503:
			raise CloseSpider('error http code')
		return response

	def process_exception(self, request, exception, spider):
		pass
