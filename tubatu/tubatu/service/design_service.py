from msic.common import log
from msic.config import redis_client
from msic.core.service import mongodb_service
from msic.core.service.bloom_filter_service import RedisBloomFilter
from tubatu import config


class DesignService(object):
	TABLE_NAME = ''
	REDIS_KEY = ''

	def __init__(self):
		self.collection = mongodb_service.get_collection(config.mongodb, self.TABLE_NAME)
		self.redis_bloom_filter = RedisBloomFilter(redis_client)

	def get_model(self, design_item):
		pass

	def save_to_database(self, design_model):
		try:
			mongodb_service.insert(self.collection, design_model.__dict__)
		except Exception as e:
			log.error(e)

	def is_duplicate_url(self, value: str) -> bool:
		return self.redis_bloom_filter.is_contains(value, self.REDIS_KEY)

	def insert_to_redis(self, value: str):
		self.redis_bloom_filter.insert(value, self.REDIS_KEY)

	def handle_item(self, design_item):
		pass
