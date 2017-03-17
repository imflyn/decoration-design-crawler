from tubatu.items import DesignPictureItem
from tubatu.model.design_picture import DesignPictureModel, DesignPictureSummaryModel
from tubatu.service.design_service import DesignService

from msic.common import log
from msic.common import utils
from msic.core.service import mongodb_service
from tubatu import config


class DesignPictureService(DesignService):
    TABLE_NAME = "design_picture"
    TABLE_NAME_SUMMARY = "design_picture_summary"
    REDIS_KEY = "tubatu_design_picture_filter"

    def __init__(self):
        super(DesignPictureService, self).__init__()
        self.summary_collection = mongodb_service.get_collection(config.mongodb, self.TABLE_NAME_SUMMARY)

    def get_design_picture_model(self, design_picture_item: DesignPictureItem) -> DesignPictureModel:
        design_picture_model = DesignPictureModel()
        design_picture_model.id = utils.get_uuid()
        design_picture_model.fid = design_picture_item['fid']
        design_picture_model.title = design_picture_item['title']
        design_picture_model.sub_title = design_picture_item['sub_title']
        design_picture_model.html_url = design_picture_item['html_url']
        design_picture_model.tags = design_picture_item['tags']
        design_picture_model.description = design_picture_item['description']
        design_picture_model.img_url = design_picture_item['img_url']
        design_picture_model.img_width = design_picture_item['img_width']
        design_picture_model.img_height = design_picture_item['img_height']
        design_picture_model.img_name = design_picture_item['img_name']
        design_picture_model.create_time = utils.get_utc_time()
        return design_picture_model

    def create_design_picture_summary_model(self, design_picture_model: DesignPictureModel) -> DesignPictureSummaryModel:
        design_picture_summary_model = DesignPictureSummaryModel()
        design_picture_summary_model.id = design_picture_model.fid
        design_picture_summary_model.cid = [design_picture_model.id]
        design_picture_summary_model.title = design_picture_model.title
        design_picture_summary_model.description = design_picture_model.description
        design_picture_summary_model.tags = design_picture_model.tags
        design_picture_summary_model.html_url = design_picture_model.html_url
        design_picture_summary_model.create_time = utils.get_utc_time()
        design_picture_summary_model.update_time = design_picture_summary_model.create_time
        design_picture_summary_model.cover_img_url = design_picture_model.img_url
        design_picture_summary_model.cover_img_width = design_picture_model.img_width
        design_picture_summary_model.cover_img_height = design_picture_model.img_height
        design_picture_summary_model.cover_img_name = design_picture_model.img_name
        return design_picture_summary_model

    def handle_item(self, design_picture_item: DesignPictureItem):
        if self.is_duplicate_url(design_picture_item['img_url']):
            return
        design_picture_model = self.get_design_picture_model(design_picture_item)
        self.save_to_database(self.collection, design_picture_model)

        summary_model = self.find_one(self.summary_collection, {'id': design_picture_model.fid})
        if summary_model is None:
            summary_model = self.create_design_picture_summary_model(design_picture_model)
            self.save_to_database(self.summary_collection, summary_model)
        else:
            tags = list(set(summary_model['tags']).union(set(design_picture_model.tags)))
            summary_model['cid'].append(design_picture_model.id)
            self.update_one(self.summary_collection, {'id': summary_model['id']},
                            {'update_time': utils.get_utc_time(), 'tags': tags, 'cid': summary_model['cid']})
        self.insert_to_redis(design_picture_model.img_url)

        log.info("=========================================================================================")
        log.info("title:" + design_picture_item['title'])
        log.info("sub_title:" + design_picture_item['sub_title'])
        log.info("original_width:" + design_picture_item['img_width'])
        log.info("original_height:" + design_picture_item['img_height'])
        log.info("html_url:" + design_picture_item['html_url'])
        log.info("img_url:" + design_picture_item['img_url'])
        log.info("description:" + design_picture_item['description'])
        log.info("tags:%s" % ','.join(map(str, design_picture_item['tags'])))
        log.info("=========================================================================================")
