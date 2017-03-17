from guju.items import DesignStrategyItem
from guju.model.design_picture import DesignStrategyModel

from guju import config
from msic.common import log
from msic.common import utils
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

    def handle_item(self, design_strategy_item: DesignStrategyItem):
        if self.is_duplicate_url(design_strategy_item['html_url']):
            return
        design_strategy_model = self.get_design_strategy_model(design_strategy_item)
        self.save_to_database(self.collection, design_strategy_model)
        self.insert_to_redis(design_strategy_model.html_url)
        log.info("=========================================================================================")
        log.info("title:" + design_strategy_item['title'])
        log.info("description:" + design_strategy_item['description'])
        log.info("category:" + design_strategy_item['category'])
        log.info("html_url:" + design_strategy_item['html_url'])
        log.info("=========================================================================================")

    def get_design_strategy_model(self, design_strategy_item: DesignStrategyItem) -> DesignStrategyModel:
        design_strategy_model = DesignStrategyModel()
        design_strategy_model.id = utils.get_uuid()
        design_strategy_model.title = design_strategy_item['title']
        design_strategy_model.html_url = design_strategy_item['html_url']
        design_strategy_model.description = design_strategy_item['description']
        design_strategy_model.content = design_strategy_item['content']
        design_strategy_model.category = design_strategy_item['category']
        design_strategy_model.create_time = utils.get_utc_time()
        return design_strategy_model
