# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.project import get_project_settings
from tubatu.constants import PORJECT_NAME
from msic.common import utils
from tubatu.service.room_design_service import RoomDesignService


class RoomPipeline(object):
	def process_item(self, item, spider):
		create_time = utils.get_utc_time()
		item['image_name'] = "/" + PORJECT_NAME + "/" + create_time[0:10] + "/" + utils.get_md5(create_time + item['html_url'])
		return item


class CustomImagesPipeline(ImagesPipeline):
	MIN_WIDTH = 0
	MIN_HEIGHT = 0
	EXPIRES = 90
	THUMBS = {
		'small': (200, 200),
		'big': (500, 500)
	}

	def get_media_requests(self, item, info):
		if 'image_url' in item:
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


class RoomImagePipeline(CustomImagesPipeline):
	def __init__(self, store_uri, download_func=None, settings=None):
		super(RoomImagePipeline, self).__init__(store_uri, settings=settings, download_func=download_func)
		self.room_design_service = RoomDesignService()

	def item_completed(self, results, item, info):
		self.room_design_service.handle_item(item)
		print(results)
