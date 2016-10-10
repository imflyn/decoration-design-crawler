from scrapy import Spider
from twisted.internet import reactor


class RedirectionMiddleware(object):
	Failed_count = 0

	def process_response(self, request, response, spider: Spider):
		if response.status == 302 or response.status == 503:
			self.Failed_count += 1
			if self.Failed_count > 3:
				pass
		return response

	def process_exception(self, request, exception, spider):
		pass
