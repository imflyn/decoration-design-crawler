from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor as sle
from msic import log


class RoomSpider(CrawlSpider):
	name = 'to8to.com'
	allowed_domains = ['to8to.com']
	start_urls = ['http://xiaoguotu.to8to.com/meitu/']
	rules = (
		Rule(sle(allow="/meitu/p_\d+.html"), follow=True, callback='parse_item'),
	)

	def parse_item(self, response):
		log.info("Parse " + response.url)



		pass
