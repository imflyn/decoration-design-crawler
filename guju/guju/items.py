# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DesignStrategyItem(scrapy.Item):
    title = scrapy.Field()
    html_url = scrapy.Field()
    description = scrapy.Field()
    content = scrapy.Field()
    category = scrapy.Field()
