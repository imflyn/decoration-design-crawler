from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from msic import log
from scrapy.selector import Selector
from msic import constant
from tubatu.items import RoomDesignItem
import scrapy


class RoomSpider(CrawlSpider):
	start_url_domain = 'xiaoguotu.to8to.com'
	name = 'room'
	allowed_domains = ['to8to.com']
	start_urls = ['http://xiaoguotu.to8to.com/meitu/']
	rules = (
		Rule(LinkExtractor(allow="/meitu/p_\d+.html"), follow=True, callback='parse_list'),
	)

	def parse_list(self, response):
		log.info("parse :" + response.url)

		selector = Selector(response)
		items_selector = selector.xpath('//div[@class="xmp_container"]//div[@class="item"]')
		for items_selector in items_selector:
			original_width = items_selector.xpath('@original_width').extract()[0]
			original_height = items_selector.xpath('@original_height').extract()[0]
			# http://xiaoguotu.to8to.com/p10221610.html
			href = constant.PROTOCOL_HTTP + self.start_url_domain + items_selector.xpath('div//a/@href').extract()[0]
			title = items_selector.xpath('div//a/@title').extract()[0]

			room_design_item = RoomDesignItem(
				url=href,
				title=title,
				image_width=original_width,
				image_height=original_height,
			)
			yield scrapy.Request(href, self.parse_content, meta={'item': room_design_item, 'javascript': True})

	def parse_content(self, response):
		log.info("parse :" + response.url)

		selector = Selector(response)
		img_url = selector.xpath('//img[@id="bigImg"]/@src').extract()[0]

		room_design_item = response.meta['item']  # type: RoomDesignItem
		room_design_item['image_url'] = img_url

		log.info("=========================================================================================")
		log.info("title:" + room_design_item['title'])
		log.info("original_width:" + room_design_item['image_width'])
		log.info("original_height:" + room_design_item['image_height'])
		log.info("url:" + room_design_item['url'])
		log.info("image_url:" + room_design_item['image_url'])
		log.info("=========================================================================================")
