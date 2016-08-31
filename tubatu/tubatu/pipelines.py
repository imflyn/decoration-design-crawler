# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from tubatu.service.room_design_service import RoomDesignService


class RoomPipeline(object):
	def process_item(self, item, spider):
		room_design_service = RoomDesignService()
		room_design_model = room_design_service.get_model(item)



		return item
