# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.project import get_project_settings

from msic.common import utils
from tubatu.service.design_picture_service import DesignPictureService


class CustomImagesPipeline(ImagesPipeline):
	MIN_WIDTH = 0
	MIN_HEIGHT = 0
	EXPIRES = 90
	THUMBS = {
		'small': (200, 200),
		'big': (500, 500)
	}

	def __init__(self, store_uri, download_func=None, settings=None):
		super(CustomImagesPipeline, self).__init__(store_uri, settings=settings, download_func=download_func)
		self.store_uri = get_project_settings()['IMAGES_STORE']

	def get_media_requests(self, item, info):
		if 'image_url' in item:
			return scrapy.Request(item['image_url'], meta={'image_name': item['image_name']})

	def file_path(self, request, response=None, info=None):
		image_name = request.meta['image_name']
		file_path = self.get_file_name(image_name)
		dir_name = file_path[0:file_path.rfind("/")]
		utils.make_dirs(self.store_uri + dir_name)
		path = '%s_original.jpg' % file_path
		return path

	def thumb_path(self, request, thumb_id, response=None, info=None):
		image_name = request.meta['image_name']
		file_path = self.get_file_name(image_name)
		dir_name = file_path[0:file_path.rfind("/")]
		utils.make_dirs(self.store_uri + dir_name)
		path = '%s_thumb.jpg' % file_path
		return path

	def get_file_name(self, image_name) -> str:
		name_data = image_name[1:].split("/")
		project_name = name_data[0]
		date = name_data[1]
		file_name = name_data[2]
		return "/" + project_name + "/" + date + "/" + file_name


class DesignPictureImagePipeline(CustomImagesPipeline):
	def __init__(self, store_uri, download_func=None, settings=None):
		super(DesignPictureImagePipeline, self).__init__(store_uri, settings=settings, download_func=download_func)
		self.design_picture_service = DesignPictureService()

	def item_completed(self, results, item, info):
		if True in results[0]:
			self.design_picture_service.handle_item(item)
