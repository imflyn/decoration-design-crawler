import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule

from msic.common import constant, log
from tubatu.items import RoomDesignItem


class RoomSpider(CrawlSpider):
	start_url_domain = 'xiaoguotu.to8to.com'
	name = 'room_spider'
	allowed_domains = ['to8to.com']
	start_urls = ['http://xiaoguotu.to8to.com/meitu/']
	rules = (
		Rule(LinkExtractor(allow="/meitu/p_\d+.html"), follow=True, callback='parse_list'),
	)
	custom_settings = {
		'ITEM_PIPELINES': {
			'tubatu.pipelines.RoomPipeline': 301,
			'tubatu.pipelines.ImageCachePipeline': 302,
		}
	}

	def parse_list(self, response):
		selector = Selector(response)
		items_selector = selector.xpath('//div[@class="xmp_container"]//div[@class="item"]')
		for items_selector in items_selector:
			original_width = items_selector.xpath('@original_width').extract()[0]
			original_height = items_selector.xpath('@original_height').extract()[0]
			# http://xiaoguotu.to8to.com/p10221610.html
			next_url = constant.PROTOCOL_HTTP + self.start_url_domain + items_selector.xpath('div//a/@href').extract()[0]
			title = items_selector.xpath('div//a/@title').extract()[0]

			room_design_item = RoomDesignItem(
				html_url=next_url,
				title=title,
				image_width=original_width,
				image_height=original_height,
			)
			yield scrapy.Request(next_url, self.parse_content, meta={'item': room_design_item, 'javascript': True})

	def parse_content(self, response):
		selector = Selector(response)
		try:
			img_url = selector.xpath('//img[@id="bigImg"]/@src').extract()[0]
		except:
			img_url = selector.xpath('//img[@id="show_img"]/@src').extract()[0]
		tags = selector.xpath('//div[@class="hot_tag xg_tag"]//text()').extract()

		room_design_item = response.meta['item']  # type: RoomDesignItem
		room_design_item['image_url'] = img_url
		room_design_item['tags'] = tags
		room_design_item['description'] = room_design_item['title']

		log.info("=========================================================================================")
		log.info("title:" + room_design_item['title'])
		log.info("original_width:" + room_design_item['image_width'])
		log.info("original_height:" + room_design_item['image_height'])
		log.info("html_url:" + room_design_item['html_url'])
		log.info("image_url:" + room_design_item['image_url'])
		log.info("description:" + room_design_item['description'])
		log.info("tags:%s" % ','.join(map(str, room_design_item['tags'])))
		log.info("=========================================================================================")

		return room_design_item
