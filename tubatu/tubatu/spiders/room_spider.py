import json

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule

from msic.common import log, constant
from msic.proxy.proxy_pool import proxy_pool
from tubatu.constants import ZONE_TYPE, STYLE_ID, AREA, COLOR_ID, HX_ID, PART_ID
from tubatu.items import RoomDesignItem
from tubatu.service.room_design_service import RoomDesignService


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
			'tubatu.pipelines.RoomImagePipeline': 302,
		}
	}

	def parse_list(self, response):
		selector = Selector(response)
		items_selector = selector.xpath('//div[@class="xmp_container"]//div[@class="item"]')
		for items_selector in items_selector:
			# http://xiaoguotu.to8to.com/p10221610.html
			aid = items_selector.xpath('div//a/@href').extract()[0][2:-5]
			# http://xiaoguotu.to8to.com/getxgtjson.php?a2=1&a12=&a11=10221610&a1=0
			next_url = (constant.PROTOCOL_HTTP + self.start_url_domain + '/getxgtjson.php?a2=1&a12=&a11={aid}&a1=0').format(aid=aid)
			room_design_service = RoomDesignService()
			if not room_design_service.is_duplicate_url(next_url):
				yield scrapy.Request(next_url, self.parse_content, meta={'aid': aid})
			# else:
			# 	log.info("filter url: %s" % next_url)

	def parse_content(self, response):
		aid = response.meta['aid']
		try:
			data = json.loads(response.text)
		except:
			print("-----------------------获取到json:" + response.text + "------------------------------")
		data_img_list = data['dataImg']
		data_img = None
		for _data_img in data_img_list:
			if _data_img['l']['aid'] == aid:
				data_img = _data_img['l']
				break
		# http://pic.to8to.com/case/1605/05/20160505_f0af86a239d0b02e9635a47ih5l1riuq_sp.jpg
		img_url = 'http://pic.to8to.com/case/{short_name}'.format(short_name=data_img['s'])
		title = data_img['t']
		original_width = data_img['w']
		original_height = data_img['h']
		tags = []
		try:
			zoom_type = ZONE_TYPE[data_img['zid']]
			if zoom_type is not None or not zoom_type.strip() == '':
				tags.append(zoom_type)
		except KeyError:
			pass
		try:
			style_id = STYLE_ID[data_img['sid']]
			if style_id is not None or not style_id.strip() == '':
				tags.append(style_id)
		except KeyError:
			pass
		try:
			area = AREA[data_img['a']]
			if area is not None or not area.strip() == '':
				tags.append(area)
		except KeyError:
			pass
		try:
			color_id = COLOR_ID[data_img['coid']]
			if color_id is not None or not color_id.strip() == '':
				tags.append(color_id)
		except KeyError:
			pass
		try:
			house_type = HX_ID[data_img['hxid']]
			if house_type is not None or not house_type.strip() == '':
				tags.append(house_type)
		except KeyError:
			pass
		try:
			part = PART_ID[data_img['pid']]
			if part is not None or not part.strip() == '':
				tags.append(part)
		except KeyError:
			pass
		try:
			room_design_item = RoomDesignItem()  # type: RoomDesignItem
			room_design_item['html_url'] = response.url
			room_design_item['image_url'] = img_url
			room_design_item['tags'] = tags
			room_design_item['title'] = title
			room_design_item['image_width'] = original_width
			room_design_item['image_height'] = original_height
			room_design_item['description'] = room_design_item['title']
			return room_design_item
		except Exception as e:
			log.warn("%s ( refer: %s )" % (e, response.url))
			proxy_pool.add_failed_time(response.meta['proxy'].replace('http://', ''))
