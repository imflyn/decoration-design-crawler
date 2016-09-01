# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.project import get_project_settings
from msic.common import utils
from tubatu.service.room_design_service import RoomDesignService


class RoomPipeline(object):
	def __init__(self):
		super().__init__()
		self.room_design_service = RoomDesignService()

	def process_item(self, item, spider):
		room_design_model = self.room_design_service.get_model(item)
		self.room_design_service.save_to_database(room_design_model)
		item['image_name'] = room_design_model.image_name
		return item


class ImageCachePipeline(ImagesPipeline):
	MIN_WIDTH = 0
	MIN_HEIGHT = 0
	EXPIRES = 90
	THUMBS = {
		'small': (200, 200),
		'big': (500, 500)
	}

	def item_completed(self, results, item, info):
		print(results)

	def get_media_requests(self, item, info):
		return scrapy.Request(item['image_url'], meta={'image_name': item['image_name']})

	def file_path(self, request, response=None, info=None):
		image_name = request.meta['image_name']
		file_path = self.get_file_name(image_name)
		dir_name = file_path[0:file_path.rfind("/")]
		store_uri = get_project_settings()['IMAGES_STORE']
		utils.make_dirs(store_uri + dir_name)
		path = '%s_original.jpg' % file_path
		return path

	def thumb_path(self, request, thumb_id, response=None, info=None):
		image_name = request.meta['image_name']
		file_path = self.get_file_name(image_name)
		dir_name = file_path[0:file_path.rfind("/")]
		store_uri = get_project_settings()['IMAGES_STORE']
		utils.make_dirs(store_uri + dir_name)
		path = '%s_thumb.jpg' % file_path
		return path

	def get_file_name(self, image_name) -> str:
		name_data = image_name[1:].split("/")
		project_name = name_data[0]
		date = name_data[1]
		file_name = name_data[2]
		return "/" + project_name + "/" + date + "/" + file_name
