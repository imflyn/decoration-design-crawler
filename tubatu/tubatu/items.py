# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DesignPictureItem(scrapy.Item):
    fid = scrapy.Field()
    title = scrapy.Field()
    sub_title = scrapy.Field()
    html_url = scrapy.Field()
    tags = scrapy.Field()
    description = scrapy.Field()
    img_url = scrapy.Field()
    img_width = scrapy.Field()
    img_height = scrapy.Field()
    img_name = scrapy.Field()


class DesignTopicItem(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
    html_url = scrapy.Field()
    article = scrapy.Field()
    create_time = scrapy.Field()
