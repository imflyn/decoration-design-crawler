import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule

from msic.common import constant
from tubatu.items import DesignTopicItem


class DesignTopicSpider(CrawlSpider):
	start_url_domain = 'xiaoguotu.to8to.com'
	name = 'design_topic'
	allowed_domains = ['to8to.com']
	start_urls = ['http://xiaoguotu.to8to.com/topic/']
	rules = (
		Rule(LinkExtractor(allow='/topic/p_\d+.html'), follow=True, callback='parse_list', process_links='process_links'),
	)
	custom_settings = {
		'ITEM_PIPELINES': {
			'tubatu.pipelines.DesignTopicPipeline': 301,
			# 'tubatu.pipelines.DesignPictureImagePipeline': 302,
		}
	}

	def process_links(self, links):
		for link in links:
			link.url = link.url.replace('%20', '')
		return links

	def parse_list(self, response):
		selector = Selector(response)
		items_selector = selector.xpath('//div[@class="xgt_topic"]')
		for item_selector in items_selector:
			# /topic/7334.html
			href = item_selector.xpath('div//a/@href').extract()[0]
			href = href.strip()
			# http://xiaoguotu.to8to.com/topic/7334.html
			next_url = (constant.PROTOCOL_HTTP + self.start_url_domain + href)
			yield scrapy.Request(next_url, self.parse_content)

	def parse_content(self, response):
		selector = Selector(response)
		title = selector.xpath('//div[@class="xdb_title"]/h1/text()').extract()[0]
		description = selector.xpath('//div[@class="xdbc_description"]//div//p/text()').extract()[0]
		items_selector = selector.xpath('//div[@class="xdbc_main_content"]//p')
		article = {}
		text = ''
		for index, item_selector in enumerate(items_selector):
			if index % 2 == 0:
				try:
					text = item_selector.xpath('span/text()').extract()[0]
				except IndexError:
					continue
			else:
				image_url = item_selector.xpath('img/@src').extract()[0]
				image_width = item_selector.xpath('img/@width').extract()[0]
				image_height = item_selector.xpath('img/@height').extract()[0]
				article[text] = [image_url, image_width, image_height]
		design_topic_item = DesignTopicItem()
		design_topic_item['title'] = title
		design_topic_item['description'] = description
		design_topic_item['article'] = article
		design_topic_item['html_url'] = response.url
		return design_topic_item
