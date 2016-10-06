# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DesignPictureItem(scrapy.Item):
	id = scrapy.Field()
	title = scrapy.Field()
	sub_title = scrapy.Field()
	html_url = scrapy.Field()
	tags = scrapy.Field()
	description = scrapy.Field()
	image_url = scrapy.Field()
	image_width = scrapy.Field()
	image_height = scrapy.Field()
	image_name = scrapy.Field()
	pass
