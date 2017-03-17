from tubatu.items import DesignTopicItem
from tubatu.model.design_topic import DesignTopicModel
from tubatu.service.design_service import DesignService

from msic.common import log
from msic.common import utils


class DesignTopicService(DesignService):
    TABLE_NAME = "design_topic"
    REDIS_KEY = "tubatu_design_topic_filter"

    def __init__(self):
        super(DesignTopicService, self).__init__()

    def get_model(self, design_topic_item: DesignTopicItem) -> DesignTopicModel:
        design_topic_model = DesignTopicModel()
        design_topic_model._id = utils.get_uuid()
        design_topic_model.title = design_topic_item['title']
        design_topic_model.description = design_topic_item['description']
        design_topic_model.html_url = design_topic_item['html_url']
        design_topic_model.article = design_topic_item['article']
        design_topic_model.create_time = utils.get_utc_time()
        return design_topic_model

    def handle_item(self, design_topic_item: DesignTopicItem):
        if self.is_duplicate_url(design_topic_item['html_url']):
            return
        design_topic_model = self.get_model(design_topic_item)
        self.save_to_database(self.collection, design_topic_model)
        self.insert_to_redis(design_topic_model.html_url)

        log.info("=========================================================================================")
        log.info("html_url:" + design_topic_item['html_url'])
        log.info("title:" + design_topic_item['title'])
        log.info("description:" + design_topic_item['description'])
        log.info("=========================================================================================")
