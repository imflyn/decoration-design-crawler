from msic.common import log
from msic.common import utils
from msic.config import redis_client
from msic.core.service import mongodb_service
from msic.core.service.bloom_filter_service import RedisBloomFilter
from tubatu import config
from tubatu.items import RoomDesignItem
from tubatu.model.room_design import RoomDesignModel

REDIS_KEY = "tubatu_room_design_filter"


class RoomDesignService(object):
	def __init__(self):
		self.collection = mongodb_service.get_collection(config.mongodb, REDIS_KEY)
		self.redis_bloom_filter = RedisBloomFilter(redis_client)

	def get_model(self, room_design_item: RoomDesignItem) -> RoomDesignModel:
		room_design_model = RoomDesignModel()
		room_design_model._id = utils.get_uuid()
		room_design_model.title = room_design_item['title']
		room_design_model.html_url = room_design_item['html_url']
		for tag in room_design_item['tags'][:]:
			if tag.strip() == '':
				room_design_item['tags'].remove(tag)
		room_design_model.tags = room_design_item['tags']
		room_design_model.description = room_design_item['description']
		room_design_model.image_url = room_design_item['image_url']
		room_design_model.image_width = room_design_item['image_width']
		room_design_model.image_height = room_design_item['image_height']
		room_design_model.image_name = room_design_item['image_name']
		return room_design_model

	def save_to_database(self, room_design_model: RoomDesignModel):
		try:
			mongodb_service.insert(self.collection, room_design_model.__dict__)
		except Exception as e:
			log.error(e)

	def is_duplicate_url(self, value: str) -> bool:
		return self.redis_bloom_filter.is_contains(value, REDIS_KEY)

	def insert_to_redis(self, value: str):
		self.redis_bloom_filter.insert(value, REDIS_KEY)

	def handle_item(self, room_design_item: RoomDesignItem):
		room_design_model = self.get_model(room_design_item)
		if self.is_duplicate_url(room_design_model.html_url):
			return
		self.save_to_database(room_design_model)
		self.insert_to_redis(room_design_model.html_url)

		log.info("=========================================================================================")
		log.info("title:" + room_design_item['title'])
		log.info("original_width:" + room_design_item['image_width'])
		log.info("original_height:" + room_design_item['image_height'])
		log.info("html_url:" + room_design_item['html_url'])
		log.info("image_url:" + room_design_item['image_url'])
		log.info("description:" + room_design_item['description'])
		log.info("tags:%s" % ','.join(map(str, room_design_item['tags'])))
		log.info("=========================================================================================")
