from guju import config
from msic.common import log
from msic.config import redis_client
from msic.core.service import mongodb_service
from msic.core.service.bloom_filter_service import RedisBloomFilter


class DesignStrategyService(object):
	TABLE_NAME = "design_strategy"
	REDIS_KEY = "guju_design_strategy_filter"

	def __init__(self):
		self.collection = mongodb_service.get_collection(config.mongodb, self.TABLE_NAME)
		self.redis_bloom_filter = RedisBloomFilter(redis_client)

	def is_duplicate_url(self, value: str) -> bool:
		return self.redis_bloom_filter.is_contains(value, self.REDIS_KEY)

	def insert_to_redis(self, value: str):
		self.redis_bloom_filter.insert(value, self.REDIS_KEY)

	def save_to_database(self, collection, item):
		try:
			mongodb_service.insert(collection, item.__dict__)
		except Exception as e:
			log.error(e)
