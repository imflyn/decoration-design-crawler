from scrapy import Spider


class RedirectionMiddleware(object):
    ERROR_COUNT = 0

    def process_response(self, request, response, spider: Spider):
        if response.status == 302 or response.status == 503:
            self.ERROR_COUNT += 1
            print('错误次数%s' % self.ERROR_COUNT)
            if self.ERROR_COUNT > 100:
                spider.close(spider, 'http status error')
        return response

    def process_exception(self, request, exception, spider):
        pass
