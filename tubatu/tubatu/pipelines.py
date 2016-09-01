# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from tubatu.service.room_design_service import RoomDesignService


class RoomPipeline(object):
	def __init__(self):
		super().__init__()
		self.room_design_service = RoomDesignService()

	def process_item(self, item, spider):
		room_design_model = self.room_design_service.get_model(item)
		self.room_design_service.saveToDatabase(room_design_model)
		item['image_name'] = room_design_model.image_name
		return item


class ImagePipeline(object):
	def process_item(self, item, spider):
		item['image_name']
		return item
