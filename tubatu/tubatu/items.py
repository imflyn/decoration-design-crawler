# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RoomDesignItem(scrapy.Item):
	name = scrapy.Field()
	component = scrapy.Field()
	style = scrapy.Field()
	color = scrapy.Field()
	title = scrapy.Field()
	description = scrapy.Field()
	image_url = scrapy.Field()
	pass
