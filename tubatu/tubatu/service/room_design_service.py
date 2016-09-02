from msic.common import log
from msic.common import utils
from msic.core.service.bloom_filter_service import RedisBloomFilter
from tubatu import config

from tubatu.constants import PORJECT_NAME
from tubatu.items import RoomDesignItem
from tubatu.model.room_design import RoomDesignModel
from msic.core.service import mongodb_service

TABLE_NAME = "room_design"


class RoomDesignService(object):
	def __init__(self):
		self.collection = mongodb_service.get_collection(config.mongodb, TABLE_NAME)
		self.redis_bloom_filter = RedisBloomFilter()

	def get_model(self, room_design_item: RoomDesignItem) -> RoomDesignModel:
		room_design_model = RoomDesignModel()
		room_design_model._id = utils.get_uuid()
		room_design_model.title = room_design_item['title']
		room_design_model.html_url = room_design_item['html_url']
		room_design_model.tags = room_design_item['tags']
		room_design_model.description = room_design_item['description']
		room_design_model.image_url = room_design_item['image_url']
		room_design_model.image_width = room_design_item['image_width']
		room_design_model.image_height = room_design_item['image_height']
		room_design_model.create_time = utils.get_utc_time()
		room_design_model.image_name = "/" + PORJECT_NAME + "/" + room_design_model.create_time[0:10] + "/" + utils.get_md5(
			room_design_model.create_time + room_design_model.html_url)

		return room_design_model

	def save_to_database(self, room_design_model: RoomDesignModel):
		try:
			mongodb_service.insert(self.collection, room_design_model.__dict__)
		except Exception as e:
			log.error(e)

	def filter_item(self, value: str) -> bool:
		if self.redis_bloom_filter.is_contains(value, TABLE_NAME):
			return False
		else:
			self.redis_bloom_filter.insert(value, TABLE_NAME)
			return True

	def handle_item(self, room_design_item: RoomDesignItem):
		room_design_model = self.get_model(room_design_item)
		self.save_to_database(room_design_model)
