from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor as sle
from msic import log
from scrapy.selector import Selector
from scrapy.http import HtmlResponse


class RoomSpider(CrawlSpider):
	name = 'to8to.com'
	allowed_domains = ['to8to.com']
	start_urls = ['http://xiaoguotu.to8to.com/meitu/']
	rules = (
		Rule(sle(allow="/meitu/p_\d+.html"), follow=True, callback='parse_item'),
	)

	def parse_item(self, response):
		selector = Selector(response)
		items_selector = selector.xpath('//div[@class="xmp_container"]//div[@class="item"]')
		for items_selector in items_selector:
			original_width = items_selector.xpath('@original_width').extract()[0]
			original_height = items_selector.xpath('@original_height').extract()[0]
			href = self.name + items_selector.xpath('div//a/@href').extract()[0]
			title = items_selector.xpath('div//a/@title').extract()[0]

			log.info("parse " + response.url)
			log.info("title:" + title)
			log.info("original_width:" + original_width)
			log.info("original_height:" + original_height)
			log.info("href:" + href)
			log.info("=========================================================================================")
