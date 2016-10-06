from msic.common import log
from msic.common import utils
from tubatu.items import DesignPictureItem
from tubatu.model.design_picture import DesignPictureModel
from tubatu.service.design_service import DesignService


class DesignPictureService(DesignService):
	TABLE_NAME = "design_picture"
	REDIS_KEY = "tubatu_design_picture_filter"

	def __init__(self):
		super(DesignPictureService, self).__init__()

	def get_model(self, design_picture_item: DesignPictureItem) -> DesignPictureModel:
		design_picture_model = DesignPictureModel()
		design_picture_model._id = utils.get_uuid()
		design_picture_model._fid = design_picture_item['id']
		design_picture_model.title = design_picture_item['title']
		design_picture_model.html_url = design_picture_item['html_url']
		design_picture_model.tags = design_picture_item['tags']
		design_picture_model.description = design_picture_item['description']
		design_picture_model.image_url = design_picture_item['image_url']
		design_picture_model.image_width = design_picture_item['image_width']
		design_picture_model.image_height = design_picture_item['image_height']
		design_picture_model.image_path = design_picture_item['image_name']
		design_picture_model.image_name = design_picture_model.image_path[design_picture_model.image_path.rfind('/') + 1:]
		design_picture_model.create_time = utils.get_utc_time()
		return design_picture_model

	def handle_item(self, design_picture_item: DesignPictureItem):
		if self.is_duplicate_url(design_picture_item['html_url']):
			return
		design_picture_model = self.get_model(design_picture_item)
		self.save_to_database(design_picture_model)
		self.insert_to_redis(design_picture_model.image_url)

		log.info("=========================================================================================")
		log.info("title:" + design_picture_item['title'])
		log.info("sub_title:" + design_picture_item['sub_title'])
		log.info("original_width:" + design_picture_item['image_width'])
		log.info("original_height:" + design_picture_item['image_height'])
		log.info("html_url:" + design_picture_item['html_url'])
		log.info("image_url:" + design_picture_item['image_url'])
		log.info("description:" + design_picture_item['description'])
		log.info("tags:%s" % ','.join(map(str, design_picture_item['tags'])))
		log.info("=========================================================================================")
